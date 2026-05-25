#!/usr/bin/env python3
# ==========================================================
# ARSENAL — AUDIT SECURITE PUBLICATION GIT
# ----------------------------------------------------------
# Contrat :
#   documentation_arsenal/contrats/publication/securite_publication_git.md
# Version contrat : v1.0.0
# Version script  : v1.0.1
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
    "documentation_arsenal/contrats/publication/securite_publication_git.md",
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
# Note contractuelle : ces exclusions de performance seront formalisées en v1.1.
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
    r"|!secret\s+\w+"             # référence HA secrets.yaml
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

def scan_forbidden_dirs(findings: list[Finding]) -> None:
    """Détecte la présence de répertoires interdits (S5).
    Parcourt ROOT indépendamment du walker pour ne pas dépendre de EXCLUDED_DIRS.
    """
    for base, dirs, _ in os.walk(ROOT):
        base_path = Path(base)
        if ".git" in base_path.parts:
            dirs[:] = []
            continue
        for d in dirs:
            if d in FORBIDDEN_DIRS:
                label = rel(base_path / d)
                add(findings, "CRITICAL", "S5", label, None, f"répertoire interdit ({d}/)")
                dirs.remove(d)  # ne pas descendre dedans


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

    label     = rel(path)
    full_text = "\n".join(lines)
    in_mqtt_block = False  # détection de bloc MQTT pour les topics sensibles
    _seen: set[tuple[str, int | None, str, str]] = set()  # (control, line, pattern, severity)

    def add_once(severity: str, control: str, line_no: int | None, pattern: str) -> None:
        key = (control, line_no, pattern, severity)
        if key not in _seen:
            _seen.add(key)
            add(findings, severity, control, label, line_no, pattern)

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Ignorer lignes vides et commentaires purs
        if not stripped or stripped.startswith("#"):
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
            raw = run_git(
                "grep", "-I", "-n", "-e", pattern.pattern,
                commit, "--",
            )
            if not raw:
                continue
            # Format : <file>:<lineno>:<content>
            for line in raw.splitlines():
                parts = line.split(":", 2)
                if len(parts) < 3:
                    continue
                file_path, lineno, content = parts

                if file_path in EXCLUDED_PATHS:
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
                    int(lineno) if lineno.isdigit() else None,
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

    for f in sorted(findings, key=lambda x: (x.severity, x.control, x.path)):
        icon = SEVERITY_ICON.get(f.severity, "  ")
        line = f":{f.line}" if f.line else ""
        suffix = "  (historique Git)" if f.historical else ""
        print(f"{icon} [{f.severity:<8}] {f.control} — {f.path}{line} — {f.pattern}{suffix}")


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
            line   = f":{f.line}" if f.line else ""
            suffix = " — *(historique)*" if f.historical else ""
            icon_f = SEVERITY_ICON.get(f.severity, "")
            out.append(f"- {icon_f} `{f.severity}` — `{f.path}{line}` — `{f.pattern}`{suffix}")

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
        out.append("✅ Publication techniquement autorisée selon le contrat `securite_publication_git.md` v1.0.0.")

    out += [
        "",
        "---",
        "",
        "_Rapport généré par `scripts/security/audit_publication_git.py` v1.0.1_",
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