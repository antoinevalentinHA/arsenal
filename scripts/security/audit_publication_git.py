#!/usr/bin/env python3
# ==========================================================
# ARSENAL — AUDIT SECURITE PUBLICATION GIT
# ----------------------------------------------------------
# Contrat :
#   documentation_arsenal/contrats/publication/securite_publication_git.md
# Version contrat : v1.3.0
# Version script  : v1.4.0
#
# v1.4.0 (incident P0 — secrets Zigbee2MQTT publiés) :
#   - Périmètre : `zigbee2mqtt/` retiré de EXCLUDED_DIRS. Ce répertoire était
#     classé « tiers » (§ 3.4) alors qu'il contient de la CONFIGURATION porteuse
#     de credentials (mqtt.password) et de clés réseau. C'est l'angle mort à
#     l'origine de la publication de zigbee2mqtt/configuration.yaml avec ses
#     secrets : verdict PASS malgré un mot de passe MQTT littéral.
#   - S9 — Clés réseau Zigbee : network_key / ext_pan_id littéraux (bloc YAML
#     ou inline) => CRITICAL ; pan_id littéral => WARNING. Les valeurs
#     `GENERATE` (sémantique native Zigbee2MQTT) et `'!secret x'` sont admises.
#   - Placeholders : ajout de `GENERATE` et de la forme QUOTÉE `'!secret x'`
#     (syntaxe Zigbee2MQTT) — la forme non quotée HA était déjà admise.
#   - S2 : correction du motif « port exposé » — la liste blanche de ports
#     (1883, 8123…) était testée par lookahead APRÈS le match et ne
#     s'appliquait donc jamais au port matché lui-même (`:1883` était signalé).
#     La liste blanche est désormais testée sur le port lui-même.
#   - --selftest étendu : cas S9 positifs/négatifs, placeholders Zigbee2MQTT,
#     liste blanche de ports S2.
#
# v1.3.0 (C14 Lot 1E-c — préparation avant branchement CI) :
#   - S1 : réduction des faux positifs de CODE. Dans un fichier de code, un
#     mot-clé S1 (`token`, `secret`…) n'est CRITICAL que si sa valeur est un
#     littéral chaîne quoté (les identifiants/types/appels — `token: str`,
#     `_G_TOKEN = re.compile(...)` — ne sont plus signalés). Les vrais secrets
#     codés en dur (`API_TOKEN = "…"`) restent CRITICAL. Fichiers non-code
#     (YAML/.md) : comportement inchangé.
#   - S5a : le contrôle des fichiers interdits porte désormais sur les fichiers
#     VERSIONNÉS de tout l'arbre (git ls-files), indépendamment de EXCLUDED_DIRS
#     — lève l'angle mort `zigbee2mqtt/` (un `.log` suivi y échappait). Un
#     artefact runtime local non suivi (gitignoré) n'est pas signalé.
#   - S2/S3 : deux FP de motif corrigés — `.home-assistant.io` n'est plus lu
#     comme domaine local ; `synology.<ext>` (nom de fichier) n'est plus lu
#     comme accès distant.
#   - Ajout d'un mode `--selftest` (juge testé : FP code écartés, vrais secrets
#     conservés, extensions interdites reconnues).
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
    "scripts/security/check_publication_zigbee2mqtt_contracts.py",
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
# www / custom_components : tiers (code externe), hors périmètre Arsenal.
# zigbee2mqtt/ N'EST PLUS exclu (v1.4.0) : c'est de la configuration Arsenal
# porteuse de credentials — son exclusion « performance » a laissé passer un
# mot de passe MQTT et la network_key du réseau Zigbee (incident P0).
# Formalisées en contrat v1.1.0 § 3.4, amendées en v1.3.0 du contrat.
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
    r"|['\"]?!secret\s+\w+"       # référence secrets externalisés — HA (nue)
                                  # ou Zigbee2MQTT (quotée : '!secret x')
    r"|GENERATE\b"                # Zigbee2MQTT : clé/PAN générés au premier démarrage
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
# S1 — Réduction des faux positifs de code (C14 Lot 1E-c)
# ---------------------------------------------------------------------------
# Dans un fichier de CODE, un mot-clé S1 (`token`, `secret`, `password`, …) est
# le plus souvent un IDENTIFIANT, un TYPE ou un APPEL — pas un secret :
#   token: str            (annotation de type)
#   _G_TOKEN = re.compile( (identifiant + appel)
#   token=line.strip()    (argument nommé + appel)
#   RE_LAT_SECRET = re.compile(r"…!secret…")  (nom de constante + regex)
# Un secret réellement codé en dur, lui, est un LITTÉRAL CHAÎNE QUOTÉ :
#   API_TOKEN = "sk-…"    password = 'hunter2'
# => en fichier de code, S1 ne se déclenche QUE si la valeur commence par un
#    guillemet (littéral). Les fichiers non-code (YAML, .md, .txt) conservent
#    le comportement d'origine (une valeur non quotée peut être un vrai secret).
# Conforme au contrat § 2 : « un faux positif justifié fait évoluer le contrat,
# pas la documentation » — c'est une évolution de détection, pas un silence.
CODE_EXTENSIONS = {
    ".py", ".pyi", ".sh", ".bash", ".zsh", ".js", ".mjs", ".cjs", ".ts", ".tsx",
    ".rb", ".pl", ".pm", ".php", ".go", ".rs", ".java", ".kt", ".c", ".h",
    ".cpp", ".hpp", ".cs", ".lua", ".ps1", ".bat", ".cmd",
}

# Une valeur "littéral secret candidate" en contexte code commence par un guillemet.
_S1_QUOTED_VALUE = re.compile(r"[:=]\s*['\"]")


def _s1_value_is_code_not_secret(matched: str) -> bool:
    """En fichier de code : vrai si la valeur du match S1 n'est PAS un littéral
    chaîne quoté (donc un type / identifiant / appel), à ignorer.
    Le `bearer <token>` (sans séparateur `[:=]`) n'est jamais dégradé."""
    if "bearer" in matched.lower() and not re.search(r"[:=]", matched):
        return False
    return _S1_QUOTED_VALUE.search(matched) is None


def s1_labels_for_line(active: str, is_code: bool) -> list[str]:
    """Labels S1 déclenchés pour une ligne active (commentaire de fin retiré).
    Factorisé pour être exercé par --selftest."""
    labels: list[str] = []
    if is_placeholder(active):
        return labels
    for pattern, label in SECRET_PATTERNS:
        m = pattern.search(active)
        if not m:
            continue
        if is_code and _s1_value_is_code_not_secret(m.group(0)):
            continue
        labels.append(label)
    return labels

# ---------------------------------------------------------------------------
# Patterns S2 — Réseau / Exposition
# ---------------------------------------------------------------------------

NETWORK_CRITICAL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"192\.168\.\d{1,3}\.\d{1,3}"),                                          "IP privée 192.168.x.x"),
    (re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),                                   "IP privée 10.x.x.x"),
    (re.compile(r"172\.(1[6-9]|2[0-9]|3[01])\.\d{1,3}\.\d{1,3}"),                       "IP privée 172.16-31.x.x"),
    (re.compile(r"https?://[^\s\"']+\.(home|local|lan|internal|localdomain)(?![\w-])", re.I), "URL domaine local"),
    # Port explicite hors ports publics courants. La liste blanche est testée
    # sur le port matché lui-même (v1.4.0) — l'ancien lookahead regardait
    # APRÈS le match et ne neutralisait donc jamais `:1883` & co.
    (re.compile(r"(?<!\d):(?!(?:80|443|8080|8123|1883|5353)(?!\d))([0-9]{4,5})(?!\d)"), "port exposé"),
]

URL_WARNING_PATTERN = re.compile(r"https?://[^\s\"']{8,}", re.I)

# ---------------------------------------------------------------------------
# Patterns S3 — MQTT / NAS / SSH
# ---------------------------------------------------------------------------

MQTT_BROKER_PATTERN    = re.compile(r"broker\s*[:=]\s*\S+",  re.I)
USERNAME_PATTERN       = re.compile(r"username\s*[:=]\s*\S+", re.I)
PASSWORD_PATTERN       = re.compile(r"password\s*[:=]\s*\S+", re.I)
MQTT_TOPIC_SEN_PATTERN = re.compile(r"\b(alarm|code|presence)\b", re.I)   # dans un topic MQTT
# synology\. suivi d'une extension de FICHIER (synology.yaml, synology.py…) n'est
# pas un accès distant : c'est un nom de fichier. Exclu par lookahead (C14 Lot 1E-c).
REMOTE_ACCESS_PATTERN  = re.compile(
    r"(rsync://|ssh://"
    r"|synology\.(?!ya?ml|py|md|json|txt|sh|conf|cfg|ini|toml|png|jpe?g|svg|log|db|csv)[^\s\"']+"
    r"|https?://[^\s\"']*synology[^\s\"']*)", re.I
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
# Patterns S9 — Clés réseau Zigbee (v1.4.0, incident P0 zigbee2mqtt)
# ---------------------------------------------------------------------------
# La network_key Zigbee est la clé de chiffrement du réseau domotique : sa
# publication permet de déchiffrer/injecter le trafic (alarme, contacts,
# sirène). Elle ne matche AUCUN pattern S1 (pas de mot-clé token/password) :
# d'où un contrôle dédié.
#
# Formes littérales interdites :
#   1. BLOC — `network_key:` seul en fin de ligne : en YAML, une valeur vide
#      introduit un bloc (liste d'octets ligne à ligne). Les seules formes
#      légitimes versionnées étant `GENERATE` et `'!secret x'` (inline),
#      un en-tête de bloc est par construction de la matière de clé littérale.
#   2. INLINE — `network_key: [1, 2, …]` / valeur hex : toute valeur inline
#      non placeholder (GENERATE / !secret / vide) est littérale.
# `ext_pan_id` suit les mêmes règles (identifiant étendu du réseau, CRITICAL).
# `pan_id` littéral est signalé en WARNING (identifiant court, moins sensible,
# mais `GENERATE` reste la forme attendue en exemple versionné).
ZIGBEE_KEY_BLOCK_PATTERN  = re.compile(r"^\s*(network_key|ext_pan_id)\s*:\s*$", re.I)
ZIGBEE_KEY_INLINE_PATTERN = re.compile(r"\b(network_key|ext_pan_id)\s*[:=]\s*\S+", re.I)
ZIGBEE_PAN_ID_PATTERN     = re.compile(r"(?<![\w])pan_id\s*[:=]\s*\S+", re.I)


def s9_finding_for_line(active: str) -> tuple[str, str] | None:
    """(sévérité, motif) S9 pour une ligne active, None si rien.
    Factorisé pour être exercé par --selftest et les tests contractuels."""
    if ZIGBEE_KEY_BLOCK_PATTERN.search(active):
        return "CRITICAL", "clé réseau Zigbee en bloc littéral"
    if is_placeholder(active):
        return None
    if ZIGBEE_KEY_INLINE_PATTERN.search(active):
        return "CRITICAL", "clé réseau Zigbee inline littérale"
    if ZIGBEE_PAN_ID_PATTERN.search(active):
        return "WARNING", "pan_id Zigbee littéral"
    return None


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


def _git_tracked_files() -> list[str]:
    """Chemins versionnés (relatifs à ROOT). Vide si hors dépôt git."""
    out = run_git("ls-files")
    return out.splitlines() if out else []


def scan_forbidden_files(findings: list[Finding]) -> None:
    """Détecte les fichiers interdits par nom/extension (S5a).

    C14 Lot 1E-c — lève l'angle mort : le contrôle porte sur les fichiers
    VERSIONNÉS de TOUT l'arbre, indépendamment de EXCLUDED_DIRS (sinon un
    `.log` suivi sous `zigbee2mqtt/` échappait au contrôle). On se limite aux
    fichiers versionnés : « présence dans le dépôt » = suivi par git. Un
    artefact runtime local non suivi (gitignoré) ne sera pas publié — le
    signaler serait un faux positif.
    """
    for rel_path in _git_tracked_files():
        if rel_path in EXCLUDED_PATHS:
            continue
        name = Path(rel_path).name
        for pattern in FORBIDDEN_FILES:
            if fnmatch.fnmatch(name, pattern):
                add(findings, "CRITICAL", "S5", rel_path, None,
                    f"fichier interdit ({pattern})")


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
    is_code    = path.suffix.lower() in CODE_EXTENSIONS  # S1 : valeur littérale exigée
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
        # En fichier de code : ne retenir qu'un littéral chaîne quoté (les
        # identifiants / types / appels sont écartés). Cf. s1_labels_for_line.
        for label_pattern in s1_labels_for_line(active, is_code):
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

        # ── S9 — Clés réseau Zigbee ────────────────────────────────────────
        s9 = s9_finding_for_line(active)
        if s9 is not None:
            add_once(s9[0], "S9", idx, s9[1])

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
    # S9 — clé réseau Zigbee : forme exacte de la fuite historique
    # (network_key en bloc littéral dans zigbee2mqtt/configuration.yaml).
    ("S9", "CRITICAL", re.compile(r"\b(network_key|ext_pan_id)\s*[:=]", re.I)),
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
        "S9": "Clés réseau Zigbee",
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
        out.append("✅ Publication techniquement autorisée selon le contrat `securite_publication_git.md` (S8–S9 inclus, script v1.4.0).")

    out += [
        "",
        "---",
        "",
        "_Rapport généré par `scripts/security/audit_publication_git.py` v1.4.0_",
        "",
    ]

    REPORT_FILE.write_text("\n".join(out), encoding="utf-8")
    print(f"\nRapport écrit : {REPORT_FILE}")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def selftest() -> int:
    """Auto-test du juge (on ne juge pas avec un juge défectueux). C14 Lot 1E-c.
    Vérifie que S1 : (a) n'accroche plus les identifiants/types/appels de code ;
    (b) accroche toujours les littéraux secrets ; et que S5a reconnaît les
    extensions interdites."""
    # (a) FAUX POSITIFS de code — ne doivent PAS être S1 (is_code=True)
    negatives_code = [
        "token: str",
        "def normalize_token(token: str) -> str:",
        "token=line.strip(),",
        "token = os.path.relpath(os.path.abspath(f), index_dir)",
        "_G_TOKEN = re.compile(",
        'RE_LAT_SECRET = re.compile(r"latitude\\s*:\\s*!secret\\s+(\\S+)")',
        "password = get_password()",
        "secret = SomeType",
    ]
    for line in negatives_code:
        labels = s1_labels_for_line(line, is_code=True)
        assert not labels, f"selftest FP code non filtré : {line!r} -> {labels}"

    # placeholder / référence !secret — ne doivent PAS être S1 (même hors code)
    for line in ["token: !secret home_token", "password: CHANGEME", 'api_key: ""']:
        assert not s1_labels_for_line(line, is_code=False), f"selftest placeholder : {line!r}"

    # (b) VRAIS POSITIFS — doivent rester S1
    positives = [
        ('API_TOKEN = "sk-abcdef123456"', True, "token"),
        ("token = 'ghp_realtokenvalue'", True, "token"),
        ("password: hunter2realsecret", False, "password"),   # YAML non quoté
        ("api_key = \"AIzaRealKeyValue\"", True, "api_key"),
        ("Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6", False, "bearer"),
    ]
    for line, is_code, expected in positives:
        labels = s1_labels_for_line(line, is_code=is_code)
        assert expected in labels, f"selftest vrai positif manqué : {line!r} -> {labels}"

    # S9 — clés réseau Zigbee : littéraux signalés, formes neutralisées admises
    s9_cases: list[tuple[str, tuple[str, str] | None]] = [
        # positifs (littéraux) — l'incident P0 zigbee2mqtt
        ("  network_key:",                    ("CRITICAL", "clé réseau Zigbee en bloc littéral")),
        ("  ext_pan_id:",                     ("CRITICAL", "clé réseau Zigbee en bloc littéral")),
        ("  network_key: [13, 37, 42, 99]",   ("CRITICAL", "clé réseau Zigbee inline littérale")),
        ("  pan_id: 54321",                   ("WARNING",  "pan_id Zigbee littéral")),
        # négatifs (formes neutralisées / hors sujet)
        ("  network_key: GENERATE",           None),
        ("  ext_pan_id: GENERATE",            None),
        ("  pan_id: GENERATE",                None),
        ("  network_key: '!secret network_key'", None),
        ("  base_topic: zigbee2mqtt",         None),
    ]
    for line, expected in s9_cases:
        got = s9_finding_for_line(line)
        assert got == expected, f"selftest S9 : {line!r} attendu={expected} obtenu={got}"

    # Placeholders Zigbee2MQTT — GENERATE et '!secret x' quoté
    for line in [
        "password: '!secret mqtt_password'",
        'password: "!secret mqtt_password"',
        "network_key: GENERATE",
    ]:
        assert is_placeholder(line), f"selftest placeholder z2m : {line!r}"
    assert not is_placeholder("password: generated_by_hand_value"), \
        "selftest : 'generated…' ne doit pas être lu comme placeholder GENERATE"

    # S1 — le mot de passe MQTT littéral (forme de l'incident) reste CRITICAL
    assert "password" in s1_labels_for_line(
        "  password: Fixture-Only-Value-cabp8q77", is_code=False
    ), "selftest : mqtt.password littéral non détecté"

    # S2 — liste blanche de ports appliquée au port matché lui-même
    port_pattern = NETWORK_CRITICAL_PATTERNS[4][0]
    assert not port_pattern.search("server: mqtt://core-mosquitto:1883"), \
        "selftest S2 : le port 1883 (liste blanche) ne doit pas être signalé"
    assert port_pattern.search("server: http://example:9443"), \
        "selftest S2 : un port hors liste blanche doit rester signalé"

    # Périmètre — zigbee2mqtt/ doit être scanné (angle mort de l'incident P0)
    assert "zigbee2mqtt" not in EXCLUDED_DIRS, \
        "selftest : zigbee2mqtt ne doit plus être exclu du scan de contenu"

    # S5a — extensions interdites reconnues par fnmatch
    for name, forbidden in [
        ("migration-4-to-5.log", True),
        ("home-assistant_v2.db", True),
        ("id_rsa.key", True),
        ("configuration.yaml", False),
        ("check_x.py", False),
    ]:
        hit = any(fnmatch.fnmatch(name, p) for p in FORBIDDEN_FILES)
        assert hit == forbidden, f"selftest S5a : {name!r} attendu={forbidden} obtenu={hit}"

    print("selftest OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Arsenal — Audit sécurité pré-publication Git"
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="Exécuter les auto-tests du scanner (aucun scan du dépôt)",
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

    if args.selftest:
        return selftest()

    findings: list[Finding] = []
    files = iter_repo_files()

    scan_forbidden_dirs(findings)
    scan_forbidden_files(findings)

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