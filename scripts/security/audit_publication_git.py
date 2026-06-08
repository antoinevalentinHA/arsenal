#!/usr/bin/env python3
# ==========================================================
# ARSENAL — AUDIT SECURITE PUBLICATION GIT
# ----------------------------------------------------------
# Contrat :
#   documentation_arsenal/contrats/publication/securite_publication_git.md
# Version contrat : v1.1.0  (S8 à promouvoir : voir § 9 du contrat)
# Version script  : v1.2.0
#
# v1.2.0 :
#   - Implémentation du contrôle S8 — Coordonnées GPS (état courant + historique).
#     S8 était listé en « Évolutions prévues (hors scope v1.1) » dans le contrat
#     mais non implémenté : c'est l'angle mort à l'origine de la fuite des
#     coordonnées du domicile dans 17_zones/*_securite.yaml.
#   - Correctif scan_history : git grep invoqué en mode Perl (-P). Les patterns
#     historiques (\s, \d, |, {n}) étaient sinon interprétés en BRE et ne
#     matchaient rien — l'invariant « un CRITICAL en historique bloque » était
#     de fait inopérant.
#   - scan_history respecte désormais EXCLUDED_DIRS (cohérence avec l'état courant ;
#     évite le bruit des répertoires tiers www/custom_components/zigbee2mqtt).
# ==========================================================

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROOT = Path.cwd()
REPORT_FILE = ROOT / "security_audit_report.md"

EXCLUDED_PATHS: set[str] = {
    "security_audit_report.md",
    "00_documentation_arsenal/contrats/publication/securite_publication_git.md",
    "scripts/security/audit_publication_git.py",
}

FORBIDDEN_FILES = [
    "secrets.yaml",
    "*.key",
    "*.pem",
    "*.crt",
    "*.env",
    "*.db",
    "*.log",
]

# Répertoires ignorés par le walker (contenu non scanné).
# Ne pas y mettre .storage / backups : ils doivent rester visibles pour S5.
# www / custom_components / zigbee2mqtt : tiers, hors périmètre Arsenal.
# Formalisées en contrat v1.1.0 § 3.4.
EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    "www",
    "custom_components",
    "zigbee2mqtt",
}

MAX_FILE_SIZE = 2 * 1024 * 1024

FORBIDDEN_DIRS = {
    ".storage",
    "backups",
}

# Valeurs considérées comme placeholders — ne déclenchent pas CRITICAL sur S1.
# Un pattern S1 correspondant à l'une de ces valeurs est ignoré.
_PLACEHOLDER_PATTERN = re.compile(
    r"[:=]\s*("
    r'""'                         # vide double-quote
    r"|''"                        # vide single-quote
    r"|null|~|none"               # YAML null
    r"|YOUR_.*|CHANGEME|REDACTED|PLACEHOLDER"
    r"|example|dummy|test|sample|demo"  # termes documentaires
    r"|!secret\s+\w+"             # référence HA secrets.yaml
    r"|1234|0000|9999|12345|000000"  # codes numériques placeholder
    r"|\.\.\.|'\.\.\.|\"\.\.\.\""
    r"|<[a-z_]+>|x{3,}|\*{3,}"      # <password> <secret> xxxx ****
    r")",
    re.I,
)


# ---------------------------------------------------------------------------
# Patterns S1 — Secrets évidents (CRITICAL)
# ---------------------------------------------------------------------------

SECRET_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"token\s*[:=]\s*\S+",           re.I), "token"),
    (re.compile(r"password\s*[:=]\s*\S+",         re.I), "password"),
    (re.compile(r"api_key\s*[:=]\s*\S+",          re.I), "api_key"),
    (re.compile(r"bearer\s+[a-zA-Z0-9\-._~+/]+=*",re.I), "bearer"),
    (re.compile(r"secret\s*[:=]\s*\S+",           re.I), "secret"),
    (re.compile(r"client_secret\s*[:=]\s*\S+",    re.I), "client_secret"),
    (re.compile(r"webhook\s*[:=]\s*https?://\S+", re.I), "webhook"),
    (re.compile(r"refresh_token\s*[:=]\s*\S+",    re.I), "refresh_token"),
]

# ---------------------------------------------------------------------------
# Patterns S2 — Réseau / Exposition
# ---------------------------------------------------------------------------

NETWORK_CRITICAL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"192\.168\.\d{1,3}\.\d{1,3}"),                                          "IP privée 192.168.x.x"),
    (re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),                                   "IP privée 10.x.x.x"),
    (re.compile(r"172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}"),                       "IP privée 172.16-31.x.x"),
    (re.compile(r"https?://[^\s\"']+\.(home|local|lan|internal|localdomain)", re.I),      "URL domaine local"),
    # Port explicite hors ports publics courants
    (re.compile(r"(?<!\d):([0-9]{4,5})(?!\d)(?!.*(?:80|443|8080|8123|1883|5353))"), "port exposé"),
]

URL_WARNING_PATTERN = re.compile(r"https?://[^\s\"']{8,}", re.I)

# ---------------------------------------------------------------------------
# Patterns S3 — MQTT / NAS / SSH
# ---------------------------------------------------------------------------

MQTT_BROKER_PATTERN    = re.compile(r"broker\s*[:=]\s*\S+",  re.I)
USERNAME_PATTERN       = re.compile(r"username\s*[:=]\s*\S+", re.I)
PASSWORD_PATTERN       = re.compile(r"password\s*[:=]\s*\S+", re.I)
MQTT_TOPIC_SEN_PATTERN = re.compile(r"\b(alarm|code|presence)\b", re.I)   # dans un topic MQTT
REMOTE_ACCESS_PATTERN  = re.compile(
    r"(rsync://|ssh://|synology\.[^\s\"']+|https?://[^\s\"']*synology[^\s\"']*)", re.I
)
NAS_VALUE_PATTERN      = re.compile(r"[:=]\s*['\"]?[^#\n]*\b(synology|nas)\b", re.I)

# ---------------------------------------------------------------------------
# Patterns S4 — Sécurité domestique
# ---------------------------------------------------------------------------

ALARM_CODE_PATTERN      = re.compile(r"alarm_code\s*[:=]\s*\d+",          re.I)
BSSID_PATTERN           = re.compile(r"bssid\s*[:=]\s*([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", re.I)
ARM_DISARM_CODE_PATTERN = re.compile(r"\b(arm|disarm)\b.*\b(code|pin)\b.*[:=]\s*\d+", re.I)
DOMESTIC_WARN_PATTERN   = re.compile(r"[:=]\s*['\"]?[^#\n]*\b(alarme|clavier|intrusion)\b", re.I)
NOMINATIVE_PATTERN      = re.compile(r"\bpresence\b.*\bantoine\b|\bantoine\b.*\bpresence\b", re.I)


# ---------------------------------------------------------------------------
# Patterns S8 — Coordonnées GPS (position physique du domicile)
# ---------------------------------------------------------------------------
# Contrat § 9 : « S8 — Coordonnées GPS (latitude, longitude, zone home) ».
# Catégorie la plus sensible du dépôt : une coordonnée en clair localise le
# domicile au mètre près. La parade fonctionnelle est l'externalisation via
# !secret (capturée par _PLACEHOLDER_PATTERN, donc non signalée).
#
# Trois formes complémentaires, calibrées sur le dépôt réel (0 FP CRITICAL) :
#   1. KEYED — clé géo + valeur décimale. Séparateur ':' '=' (YAML/JSON/INI)
#      ou '|' (tableau Markdown : « | Latitude | 44.8522979 | »).
#   2. PAIR  — deux décimales haute précision adjacentes séparées par une
#      virgule (« 44.8522979, -0.5875885 ») : forme narrative / liste / GeoJSON.
#   3. BARE  — filet heuristique (WARNING) : décimale isolée à signature GPS
#      (>= 6 décimales, dernier chiffre non nul pour exclure les valeurs
#      « rondes » type températures). Attrape les littéraux de coordonnées
#      sans clé ni paire (ex. constantes LATITUDE_REF = "44.8522979").
GEO_COORD_KEYED_PATTERN = re.compile(
    r"\b(?:latitude|longitude)\b\s*[:=|]\s*[+-]?\d{1,3}\.\d+", re.I
)
GEO_COORD_PAIR_PATTERN = re.compile(
    r"[+-]?\d{1,3}\.\d{3,}\s*,\s*[+-]?\d{1,3}\.\d{3,}"
)
GEO_COORD_BARE_PATTERN = re.compile(
    r"(?<![\w.])[+-]?\d{1,3}\.\d{5,}[1-9](?![\d.])"
)


# ---------------------------------------------------------------------------
# Structures de données
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    severity:   str
    control:    str
    path:       str
    line:       int | None
    pattern:    str
    historical: bool = False
    annotation: str = ""     # 'scope=doc' | 'ignore' | ''


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def is_excluded(path: Path) -> bool:
    return rel(path) in EXCLUDED_PATHS


def is_text_file(path: Path) -> bool:
    try:
        return b"\0" not in path.read_bytes()[:4096]
    except OSError:
        return False


def is_placeholder(line: str) -> bool:
    return bool(_PLACEHOLDER_PATTERN.search(line))


# Annotation audit:ignore — présente sur la ligne active (hors partie commentaire retirée)
_IGNORE_PATTERN   = re.compile(r"#\s*audit:ignore(?:\s*[-—]\s*(?P<reason>.+))?", re.I)
_IGNORE_NO_REASON = re.compile(r"#\s*audit:ignore\s*$", re.I)

# Annotation audit:scope=doc — présente dans les 5 premières lignes
_SCOPE_DOC_PATTERN = re.compile(r"audit:scope=doc", re.I)


def has_ignore(raw_line: str) -> tuple[bool, str]:
    """Retourne (présent, justification). Justification vide = annotation invalide."""
    m = _IGNORE_PATTERN.search(raw_line)
    if not m:
        return False, ""
    reason = (m.group("reason") or "").strip()
    return True, reason


def is_scope_doc(lines: list[str]) -> bool:
    """True si l'une des 5 premières lignes contient audit:scope=doc."""
    for line in lines[:5]:
        if _SCOPE_DOC_PATTERN.search(line):
            return True
    return False


def iter_repo_files() -> list[Path]:
    files: list[Path] = []

    for base, dirs, filenames in os.walk(ROOT):
        base_path = Path(base)

        dirs[:] = [
            d for d in dirs
            if d not in EXCLUDED_DIRS
        ]

        for filename in filenames:
            path = base_path / filename

            if is_excluded(path):
                continue

            try:
                if path.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue

            files.append(path)

    return files


def add(findings: list[Finding], severity: str, control: str,
        path: str, line: int | None, pattern: str,
        historical: bool = False) -> None:
    findings.append(Finding(severity, control, path, line, pattern, historical))


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Scan S5 — Fichiers et répertoires interdits
# ---------------------------------------------------------------------------

# Extensions signalant un contenu de backup système dans un répertoire backups/
_BACKUP_CONTENT_EXTENSIONS = {'.db', '.log', '.tar', '.gz', '.zip', '.bak', '.sql'}


def _backups_dir_is_forbidden(path: Path) -> bool:
    """Règle S5 v1.1 pour backups/ : interdit si racine/premier niveau,
    ou si contient des extensions de backup système.
    Un sous-répertoire métier Arsenal (YAML fonctionnel uniquement) est autorisé.
    """
    # Profondeur relative depuis ROOT (0 = racine)
    try:
        rel_parts = path.relative_to(ROOT).parts
    except ValueError:
        return True
    depth = len(rel_parts) - 1  # nombre de répertoires parents
    if depth <= 1:
        return True  # racine ou premier niveau = toujours interdit
    # Profondeur > 1 : interdit seulement si contenu système détecté
    try:
        for child in path.iterdir():
            if child.suffix.lower() in _BACKUP_CONTENT_EXTENSIONS:
                return True
    except OSError:
        pass
    return False


def scan_forbidden_dirs(findings: list[Finding]) -> None:
    """Détecte la présence de répertoires interdits (S5).
    Parcourt ROOT indépendamment du walker pour ne pas dépendre de EXCLUDED_DIRS.
    Applique la règle contextuelle v1.1 pour backups/.
    """
    for base, dirs, _ in os.walk(ROOT):
        base_path = Path(base)
        if ".git" in base_path.parts:
            dirs[:] = []
            continue
        to_remove: list[str] = []
        for d in dirs:
            dir_path = base_path / d
            if d == ".storage":
                add(findings, "CRITICAL", "S5", rel(dir_path), None, "répertoire interdit (.storage/)")
                to_remove.append(d)
            elif d == "backups":
                if _backups_dir_is_forbidden(dir_path):
                    add(findings, "CRITICAL", "S5", rel(dir_path), None, "répertoire interdit (backups/)")
                    to_remove.append(d)
                # sinon : répertoire métier Arsenal — pas de finding, on descend
        for d in to_remove:
            dirs.remove(d)


def scan_forbidden_files(files: list[Path], findings: list[Finding]) -> None:
    """Détecte la présence de fichiers interdits par nom/extension (S5)."""
    for path in files:
        label = rel(path)
        for pattern in FORBIDDEN_FILES:
            if fnmatch.fnmatch(path.name, pattern):
                add(findings, "CRITICAL", "S5", label, None, f"fichier interdit ({pattern})")


# ---------------------------------------------------------------------------
# Scan état courant (S1–S4)
# ---------------------------------------------------------------------------

def scan_text_file(path: Path, findings: list[Finding]) -> None:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return

    label      = rel(path)
    full_text  = "\n".join(lines)
    scope_doc  = is_scope_doc(lines)  # fichier entièrement documentaire
    in_mqtt_block = False
    _seen: set[tuple[str, int | None, str, str]] = set()  # (control, line, pattern, severity)

    def add_once(
        severity: str, control: str, line_no: int | None, pattern: str,
        annotation: str = "",
    ) -> None:
        # scope=doc : dégrader CRITICAL → WARNING
        effective_severity = severity
        effective_annotation = annotation
        if scope_doc and severity == "CRITICAL":
            effective_severity = "WARNING"
            effective_annotation = "scope=doc"
        key = (control, line_no, pattern, effective_severity)
        if key not in _seen:
            _seen.add(key)
            f = Finding(effective_severity, control, label, line_no, pattern,
                        annotation=effective_annotation)
            findings.append(f)

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Ignorer lignes vides et commentaires purs (sauf si audit:ignore présent)
        if not stripped:
            continue

        # Détecter audit:ignore AVANT de retirer le commentaire
        ignored, reason = has_ignore(line)
        if ignored:
            if not reason:
                # Annotation sans justification : WARNING de forme
                add_once("WARNING", "S1", idx, "audit:ignore sans justification",
                         annotation="ignore-malformed")
            continue  # ligne ignorée dans tous les cas

        # Ignorer commentaires purs (après test audit:ignore)
        if stripped.startswith("#"):
            continue

        # Retirer la partie commentaire en fin de ligne avant analyse
        active = re.sub(r"\s+#.*$", "", line)

        # ── S1 — Secrets évidents ──────────────────────────────────────────
        for pattern, label_pattern in SECRET_PATTERNS:
            if pattern.search(active) and not is_placeholder(active):
                add_once("CRITICAL", "S1", idx, label_pattern)

        # ── S2 — Réseau / Exposition ───────────────────────────────────────
        for pattern, label_pattern in NETWORK_CRITICAL_PATTERNS:
            if pattern.search(active):
                add_once("CRITICAL", "S2", idx, label_pattern)

        if URL_WARNING_PATTERN.search(active):
            # Seulement si l'URL ne correspond déjà pas à un CRITICAL S2
            already_critical = any(
                p.search(active) for p, _ in NETWORK_CRITICAL_PATTERNS
            )
            if not already_critical:
                add_once("WARNING", "S2", idx, "URL externe")

        # ── S3 — MQTT / NAS / SSH ──────────────────────────────────────────
        if MQTT_BROKER_PATTERN.search(active) and not is_placeholder(active):
            add_once("CRITICAL", "S3", idx, "broker MQTT")

        # Détection de bloc MQTT (platform: mqtt ou type: mqtt)
        # Fermeture testée EN PREMIER : une ligne non-indentée ferme le bloc,
        # sauf si c'est elle-même la déclaration "platform: mqtt".
        is_mqtt_decl = bool(re.search(r"^\s*(platform|type)\s*:\s*mqtt\b", line, re.I))
        if re.match(r"^\S", line) and in_mqtt_block and not is_mqtt_decl:
            in_mqtt_block = False
        if is_mqtt_decl:
            in_mqtt_block = True

        if in_mqtt_block and MQTT_TOPIC_SEN_PATTERN.search(active):
            add_once("WARNING", "S3", idx, "topic MQTT sensible")

        if REMOTE_ACCESS_PATTERN.search(active):
            add_once("CRITICAL", "S3", idx, "accès distant (rsync/ssh/synology)")

        if NAS_VALUE_PATTERN.search(active) and not is_placeholder(active):
            add_once("WARNING", "S3", idx, "référence NAS en valeur")

        # ── S4 — Sécurité domestique ───────────────────────────────────────
        for pattern, label_pattern in [
            (ALARM_CODE_PATTERN,      "alarm_code numérique"),
            (BSSID_PATTERN,           "BSSID MAC"),
            (ARM_DISARM_CODE_PATTERN, "code arm/disarm"),
        ]:
            if pattern.search(active):
                add_once("CRITICAL", "S4", idx, label_pattern)

        if DOMESTIC_WARN_PATTERN.search(active):
            add_once("WARNING", "S4", idx, "terme sécurité domestique")

        if NOMINATIVE_PATTERN.search(active):
            add_once("WARNING", "S4", idx, "présence nominative")

        # ── S8 — Coordonnées GPS ───────────────────────────────────────────
        # is_placeholder neutralise « latitude: !secret home_latitude » et les
        # exemples documentaires (« <decimal> », « ... »).
        geo_critical = False
        for pattern, label_pattern in [
            (GEO_COORD_KEYED_PATTERN, "coordonnée géographique (clé + valeur)"),
            (GEO_COORD_PAIR_PATTERN,  "paire de coordonnées géographiques"),
        ]:
            if pattern.search(active) and not is_placeholder(active):
                add_once("CRITICAL", "S8", idx, label_pattern)
                geo_critical = True

        # Filet heuristique : seulement si la ligne n'est pas déjà CRITICAL S8
        # (mime la logique S2 URL_WARNING / already_critical).
        if (
            not geo_critical
            and GEO_COORD_BARE_PATTERN.search(active)
            and not is_placeholder(active)
        ):
            add_once("WARNING", "S8", idx, "valeur à signature de coordonnée GPS")

    # S3 — username + password dans le même fichier (CRITICAL)
    # is_placeholder vérifié ligne par ligne : un seul "password: null" ailleurs
    # ne doit pas masquer un vrai mot de passe sur une autre ligne.
    username_lines = [l for l in lines if USERNAME_PATTERN.search(l) and not is_placeholder(l)]
    password_lines = [l for l in lines if PASSWORD_PATTERN.search(l) and not is_placeholder(l)]
    if username_lines and password_lines:
        add(findings, "CRITICAL", "S3", label, None,
            "username + password dans le même fichier")


# ---------------------------------------------------------------------------
# Scan S6 — Historique Git (via git grep, O(patterns) pas O(commits×fichiers))
# ---------------------------------------------------------------------------

_HISTORY_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("S1", "CRITICAL", re.compile(r"(token|password|api_key|bearer|secret|client_secret|webhook|refresh_token)\s*[:=]\s*\S+", re.I)),
    ("S2", "CRITICAL", re.compile(r"(192\.168\.|10\.\d+\.\d+\.|172\.(1[6-9]|2[0-9]|3[01])\.)", re.I)),
    ("S2", "WARNING",  re.compile(r"https?://[^\s\"']{8,}", re.I)),
    ("S3", "CRITICAL", re.compile(r"(broker\s*[:=]|rsync://|ssh://|synology\.)", re.I)),
    ("S3", "WARNING",  re.compile(r"\b(synology|nas)\b", re.I)),
    ("S4", "CRITICAL", re.compile(r"(alarm_code\s*[:=]\s*\d+|bssid\s*[:=])", re.I)),
    ("S4", "WARNING",  re.compile(r"\b(alarme|clavier|intrusion)\b", re.I)),
    # S8 — coordonnée GPS keyed : forme exacte de la fuite historique
    # (« latitude: 44.8522979 » dans 17_zones/*_securite.yaml@parent-du-fix).
    ("S8", "CRITICAL", re.compile(r"\b(latitude|longitude)\b\s*[:=|]\s*[+-]?\d{1,3}\.\d+", re.I)),
]


def scan_history(findings: list[Finding]) -> None:
    """
    Scan de l'historique Git complet via `git grep` sur chaque commit.
    rev-list --all fournit la liste exhaustive des commits accessibles.
    Déduplication par (file_path, lineno, pattern) : un secret dans N commits
    génère un seul finding.
    """
    commits = run_git("rev-list", "--all").splitlines()
    if not commits:
        return

    _seen: set[tuple[str, str, str]] = set()  # (file_path, lineno, pattern)

    for control, severity, pattern in _HISTORY_PATTERNS:
        for commit in commits:
            # -P (PCRE) : les patterns utilisent \s \d \b | {n} — non interprétés
            # par le BRE par défaut de git grep, qui ne matcherait alors rien.
            raw = run_git(
                "grep", "-I", "-n", "-P", "-e", pattern.pattern,
                commit, "--",
            )
            if not raw:
                continue
            # Format git grep <commit> : « <commit>:<file>:<lineno>:<content> »
            # (le préfixe <commit> est présent car on grep une révision explicite).
            for line in raw.splitlines():
                parts = line.split(":", 3)
                if len(parts) < 4:
                    continue
                _commit_prefix, file_path, lineno, content = parts
                if not lineno.isdigit():
                    continue

                if file_path in EXCLUDED_PATHS:
                    continue
                # Cohérence avec le walker de l'état courant : les répertoires
                # tiers / techniques (EXCLUDED_DIRS) sont hors périmètre Arsenal.
                if any(part in EXCLUDED_DIRS for part in Path(file_path).parts):
                    continue
                if is_placeholder(content):
                    continue

                dedup_key = (file_path, lineno, pattern.pattern)
                if dedup_key in _seen:
                    continue
                _seen.add(dedup_key)

                add(
                    findings,
                    severity,
                    control,
                    f"{file_path}@{commit[:8]}",
                    int(lineno),
                    pattern.pattern,
                    historical=True,
                )


# ---------------------------------------------------------------------------
# Verdict global
# ---------------------------------------------------------------------------

def global_verdict(findings: list[Finding]) -> str:
    if any(f.severity == "CRITICAL" for f in findings):
        return "CRITICAL"
    if any(f.severity == "WARNING" for f in findings):
        return "WARNING"
    return "PASS"


# ---------------------------------------------------------------------------
# Sortie console
# ---------------------------------------------------------------------------

SEVERITY_ICON = {"CRITICAL": "❌", "WARNING": "⚠️ ", "PASS": "✅"}


def print_console(findings: list[Finding]) -> None:
    if not findings:
        print("✅ [PASS]  S1-S6 — aucun signal détecté")
        return

    for f in sorted(findings, key=lambda x: (x.control, x.severity, x.path, x.line or 0)):
        icon   = SEVERITY_ICON.get(f.severity, "  ")
        line   = f":{f.line}" if f.line else ""
        suffix = "  (historique Git)" if f.historical else ""
        ann    = f"  [{f.annotation}]" if f.annotation else ""
        print(f"{icon} [{f.severity:<8}] {f.control} — {f.path}{line} — {f.pattern}{suffix}{ann}")


# ---------------------------------------------------------------------------
# Rapport Markdown
# ---------------------------------------------------------------------------

def write_report(findings: list[Finding], verdict: str, history_enabled: bool) -> None:
    head = run_git("rev-parse", "--short", "HEAD") or "non disponible"
    now  = dt.datetime.now().isoformat(timespec="seconds")

    icon = SEVERITY_ICON.get(verdict, "")

    out: list[str] = [
        "# Rapport d'audit sécurité — Arsenal",
        "",
        f"| Champ | Valeur |",
        f"|---|---|",
        f"| Date | `{now}` |",
        f"| Commit HEAD | `{head}` |",
        f"| Historique Git | `{'oui' if history_enabled else 'non'}` |",
        f"| **Verdict global** | **{icon} {verdict}** |",
        "",
        "## Résumé",
        "",
    ]

    for sev in ("CRITICAL", "WARNING"):
        count = sum(1 for f in findings if f.severity == sev)
        icon_s = SEVERITY_ICON.get(sev, "")
        out.append(f"- {icon_s} `{sev}` : {count} signal(s)")

    if verdict == "PASS":
        out.append("- ✅ Aucun signal détecté")

    out += ["", "---", "", "## Détail par contrôle", ""]

    control_labels = {
        "S1": "Secrets évidents",
        "S2": "Réseau / Exposition",
        "S3": "MQTT / NAS / SSH",
        "S4": "Sécurité domestique",
        "S5": "Fichiers interdits",
        "S6": "Historique Git",
        "S8": "Coordonnées GPS",
    }

    for control, label in control_labels.items():
        cf = [f for f in findings if f.control == control]
        # S6 est virtuel : les hits historiques sont tagués sur leur contrôle d'origine
        if control == "S6":
            cf = [f for f in findings if f.historical]

        out.append(f"### {control} — {label}")
        out.append("")

        if not cf:
            out.append("✅ Aucun signal détecté.")
            out.append("")
            continue

        for f in sorted(cf, key=lambda x: (x.path, x.line or 0)):
            line       = f":{f.line}" if f.line else ""
            suffix     = " — *(historique)*" if f.historical else ""
            ann        = f"  `[{f.annotation}]`" if f.annotation else ""
            icon_f     = SEVERITY_ICON.get(f.severity, "")
            out.append(f"- {icon_f} `{f.severity}` — `{f.path}{line}` — `{f.pattern}`{suffix}{ann}")

        out.append("")

    concerned = sorted({f.path for f in findings})
    out += ["---", "", "## Fichiers concernés", ""]

    if concerned:
        for fp in concerned:
            out.append(f"- `{fp}`")
    else:
        out.append("Aucun.")

    out += ["", "---", "", "## Recommandations", ""]

    if verdict == "CRITICAL":
        out.append("❌ **Publication interdite** tant que les signaux `CRITICAL` ne sont pas corrigés ou justifiés.")
    elif verdict == "WARNING":
        out.append("⚠️  **Revue manuelle obligatoire** avant toute publication. Chaque `WARNING` doit être explicitement accepté ou corrigé.")
    else:
        out.append("✅ Publication techniquement autorisée selon le contrat `securite_publication_git.md` (S8 inclus, script v1.2.0).")

    out += [
        "",
        "---",
        "",
        "_Rapport généré par `scripts/security/audit_publication_git.py` v1.2.0_",
        "",
    ]

    REPORT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"\nRapport écrit : {REPORT_FILE}")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Arsenal — Audit sécurité pré-publication Git"
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Inclure le scan de l'historique Git complet (lent sur grands dépôts)",
    )
    parser.add_argument(
        "--fail-on",
        choices=["warning", "critical"],
        default="warning",
        dest="fail_on",
        help="Seuil de retour non-zéro (défaut : warning)",
    )
    args = parser.parse_args()

    findings: list[Finding] = []
    files = iter_repo_files()

    scan_forbidden_dirs(findings)
    scan_forbidden_files(files, findings)

    for path in files:
        if is_text_file(path):
            scan_text_file(path, findings)

    if args.history:
        scan_history(findings)

    verdict = global_verdict(findings)
    print_console(findings)
    write_report(findings, verdict, args.history)

    if verdict == "CRITICAL":
        return 2
    if verdict == "WARNING" and args.fail_on == "warning":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())