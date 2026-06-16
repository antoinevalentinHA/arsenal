#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Notifications
Contrat : Arsenal Notifications (normatif, transverse)
Script  : scripts/arsenal_contracts/check_notifications_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Dossiers à scanner
# ---------------------------------------------------------------------------
DIR_AUTOMATIONS = REPO_ROOT / "11_automations"
DIR_SCRIPTS     = REPO_ROOT / "10_scripts"

# ---------------------------------------------------------------------------
# Séparateur normatif (demi-cadratin U+2013)
# Le cadratin long (U+2014 —) est interdit comme séparateur de titre.
# ---------------------------------------------------------------------------
SEPARATEUR_NORMATIF = "\u2013"   # –
SEPARATEUR_INTERDIT = "\u2014"   # —

# ---------------------------------------------------------------------------
# Emoji normatif de tête
#
# Le test ne se contente pas de vérifier un caractère non-ASCII :
#   - "Énergie – Batterie faible" est non-ASCII mais n'est pas conforme.
#   - "🔋 Énergie – Batterie faible" est conforme.
#
# Le pattern couvre les blocs Unicode utilisés par les emojis courants,
# avec prise en charge des sélecteurs de variation et séquences ZWJ.
# ---------------------------------------------------------------------------
EMOJI_AT_START = re.compile(
    r"^("
    r"[\U0001F1E6-\U0001F1FF]{2}"                  # drapeaux régionaux
    r"|[\U0001F300-\U0001FAFF]"                    # emojis principaux
    r"|[\u2139\u2600-\u27BF]"                      # symboles emoji BMP (dont ℹ U+2139)
    r")"
    r"(?:\ufe0f)?"
    r"(?:\u200d(?:[\U0001F300-\U0001FAFF]|[\u2600-\u27BF])(?:\ufe0f)?)*"
    r"\s+"
)

# Verbes et formulations interdits dans les titres (§ Format normatif)
MOTS_INTERDITS_TITRE = [
    "relance", "relancé",
    "arrêt", "arret",
    "tentative",
    "échoué", "echoue",
    "mise à jour", "mise a jour",
    "déblocage", "deblocage",
    "redémarrage", "redemarrage",
]

# Patterns de référence temporelle interdits dans les blocs create (§ Interdiction du passé)
TEMPORAL_PATTERNS = [
    re.compile(r"\bnow\(\)", re.IGNORECASE),
    re.compile(r"\bas_timestamp\b", re.IGNORECASE),
    re.compile(r"\bstrftime\b", re.IGNORECASE),
    re.compile(r"\brelative_time\b", re.IGNORECASE),
    re.compile(r"\btimedelta\b", re.IGNORECASE),
]

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def yaml_files(*directories: Path) -> list[Path]:
    result = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_persistent_create_blocks(content: str) -> list[str]:
    """
    Extrait les blocs de texte dans un rayon de 300 chars après chaque
    appel persistent_notification.create (hors commentaires).
    Retourne une liste de fenêtres de contexte.
    """
    blocks = []
    for m in re.finditer(r"persistent_notification\.create", content):
        start = m.start()
        # Remonter pour vérifier que ce n'est pas un commentaire
        line_start = content.rfind("\n", 0, start) + 1
        line = content[line_start:start]
        if line.strip().startswith("#"):
            continue
        window = content[start:start + 400]
        blocks.append(window)
    return blocks


def extract_title_from_block(block: str) -> str | None:
    """Extrait la valeur du champ title: dans un bloc."""
    m = re.search(r'title\s*:\s*["\']?([^"\'\n]+)["\']?', block)
    if m:
        return m.group(1).strip().strip('"\'')
    return None


def extract_mobile_titre_blocks(content: str) -> list[str]:
    """
    Extrait une fenêtre de contexte après chaque appel au canal mobile central
    (script.notification_envoyer / _famille / _avance), hors commentaires.

    L'ancrage sur le préfixe `script.` ne capture que les SITES D'APPEL : la
    définition des wrappers (`notification_envoyer:` en tête de ligne, sans
    préfixe) n'est jamais matchée, ce qui évite de lire les `titre:` de
    description de champ du fichier de définition.
    """
    blocks = []
    for m in re.finditer(r"script\.notification_envoyer\w*", content):
        start = m.start()
        line_start = content.rfind("\n", 0, start) + 1
        line = content[line_start:start]
        if line.strip().startswith("#"):
            continue
        blocks.append(content[start:start + 500])
    return blocks


def extract_titre_from_block(block: str) -> str | None:
    """Extrait la valeur du champ titre: (canal mobile) dans un bloc."""
    m = re.search(r'titre\s*:\s*["\']([^"\'\n]+)["\']', block)
    if not m:
        m = re.search(r'titre\s*:\s*([^\n#]+)', block)
    if m:
        return m.group(1).strip().strip('"\'')
    return None


# ---------------------------------------------------------------------------
# T1 — Chaque titre de notification persistante commence par un emoji
#
# Invariant (§ Format normatif) : tout titre doit commencer par un emoji
# identifiant le domaine fonctionnel.
# Méthode : le premier caractère doit être hors de la plage ASCII standard.
# Scope : tous les fichiers YAML des automations et scripts.
# ---------------------------------------------------------------------------

def test_titre_commence_par_emoji() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    violations = []

    for path in files:
        content = read(path)
        for block in extract_persistent_create_blocks(content):
            title = extract_title_from_block(block)
            if title is None:
                continue
            # Ignorer les titres dynamiques (templates Jinja)
            if title.startswith("{{"):
                continue
            if not EMOJI_AT_START.match(title):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"titre sans emoji normatif en tête : «{title}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T1 — Emoji de tête obligatoire : {v}")
    else:
        print("✔ T1 — Tous les titres de notifications persistantes commencent par un emoji normatif")


# ---------------------------------------------------------------------------
# T2 — Présence du séparateur normatif – (U+2013) dans les titres à deux parties
#
# Invariant (§ Format normatif) : le séparateur canonique est –.
# Le cadratin long — (U+2014) est interdit comme séparateur.
# Un titre sans séparateur est acceptable s'il est d'une seule partie
# (ex. « 🔒 Alarme activée »).
# Ce test vérifie uniquement que, quand un séparateur est présent,
# c'est bien – et non —.
# ---------------------------------------------------------------------------

def test_separateur_normatif() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    violations = []

    for path in files:
        content = read(path)
        for block in extract_persistent_create_blocks(content):
            title = extract_title_from_block(block)
            if title is None or title.startswith("{{"):
                continue
            if SEPARATEUR_INTERDIT in title:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"séparateur — (cadratin) au lieu de – (demi-cadratin) : «{title}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T2 — Séparateur non conforme : {v}")
    else:
        print("✔ T2 — Aucun séparateur — (cadratin) dans les titres de notifications persistantes")


# ---------------------------------------------------------------------------
# T3 — Absence de formulations événementielles dans les titres
#
# Invariant (§ Format normatif) : le titre décrit un état, jamais un fait
# passé ni une action. Les verbes et formulations événementiels sont interdits.
# Scope : automations et scripts.
# ---------------------------------------------------------------------------

def test_titre_sans_formulation_evenementielle() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    violations = []

    for path in files:
        content = read(path)
        for block in extract_persistent_create_blocks(content):
            title = extract_title_from_block(block)
            if title is None or title.startswith("{{"):
                continue
            title_lower = title.lower()
            for mot in MOTS_INTERDITS_TITRE:
                if mot in title_lower:
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"formulation événementielle «{mot}» dans le titre : «{title}»"
                    )
                    break  # une violation par titre suffit

    if violations:
        for v in violations:
            ERRORS.append(f"T3 — Formulation événementielle : {v}")
    else:
        print("✔ T3 — Aucune formulation événementielle dans les titres de notifications persistantes")


# ---------------------------------------------------------------------------
# T4 — Absence de référence temporelle dans les blocs create (§ Interdiction du passé)
#
# Invariant (§ Interdictions temporelles) : une notification persistante
# ne doit contenir aucune information temporelle (now(), as_timestamp,
# strftime, relative_time, timedelta).
# Scope : fenêtre de 400 chars après chaque persistent_notification.create.
# ---------------------------------------------------------------------------

def test_absence_reference_temporelle() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    violations = []

    for path in files:
        content = read(path)
        for block in extract_persistent_create_blocks(content):
            for pattern in TEMPORAL_PATTERNS:
                m = pattern.search(block)
                if m:
                    # Extraire le titre pour le contexte
                    title = extract_title_from_block(block) or "(titre non extrait)"
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"référence temporelle «{m.group(0)}» dans la notification «{title}»"
                    )
                    break  # une violation par bloc suffit

    if violations:
        for v in violations:
            ERRORS.append(f"T4 — Référence temporelle interdite : {v}")
    else:
        print("✔ T4 — Aucune référence temporelle dans les blocs persistent_notification.create")


# ---------------------------------------------------------------------------
# T5 — Unicité des notification_id dans le repo
#
# Invariant (§ Identité & Unicité) : une notification persistante est unique
# par état métier. Un même notification_id dans plusieurs fichiers distincts
# peut signifier soit un remplacement légitime (create + dismiss pairs),
# soit un doublon invalide.
# Ce test signale les notification_id présents dans 4 fichiers ou plus —
# seuil calibré pour tolérer les paires create/dismiss réparties sur
# plusieurs automations d'un même domaine (ex. vacances : create, dismiss,
# dismiss fin, réconciliation = 3 fichiers légitimes).
# ---------------------------------------------------------------------------

def test_unicite_notification_id() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    id_to_files: dict[str, list[str]] = {}

    pattern = re.compile(r'notification_id\s*:\s*["\']?([^\s"\']+)["\']?')

    for path in files:
        content = read(path)
        for line in content.splitlines():
            if line.strip().startswith("#"):
                continue
            m = pattern.search(line)
            if m:
                nid = m.group(1)
                rel = str(path.relative_to(REPO_ROOT))
                if nid not in id_to_files:
                    id_to_files[nid] = []
                if rel not in id_to_files[nid]:
                    id_to_files[nid].append(rel)

    violations = {
        nid: files_list
        for nid, files_list in id_to_files.items()
        if len(files_list) >= 4
    }

    if violations:
        for nid, files_list in sorted(violations.items()):
            ERRORS.append(
                f"T5 — notification_id «{nid}» présent dans {len(files_list)} fichiers "
                f"(seuil ≥ 4) : {', '.join(files_list[:4])}{'…' if len(files_list) > 4 else ''}"
            )
    else:
        print("✔ T5 — Aucun notification_id présent dans 4 fichiers ou plus (unicité)")


# ---------------------------------------------------------------------------
# T6 — Chaque titre de notification mobile commence par un emoji
#
# Invariant (§ Titre mobile — Emoji obligatoire / § Format normatif) : toute
# notification mobile émise via le canal central (script.notification_envoyer*)
# doit fournir un `titre:` commençant par un emoji de domaine.
# Scope : sites d'appel script.notification_envoyer{,_famille,_avance} dans les
# automations et scripts.
# Exception : un titre entièrement dynamique (template Jinja {{ … }}) ne peut
# pas être vérifié statiquement — même tolérance que pour T1 (persistant).
# ---------------------------------------------------------------------------

def test_titre_mobile_commence_par_emoji() -> None:
    files = yaml_files(DIR_AUTOMATIONS, DIR_SCRIPTS)
    violations = []

    for path in files:
        content = read(path)
        for block in extract_mobile_titre_blocks(content):
            titre = extract_titre_from_block(block)
            if titre is None:
                continue
            # Ignorer les titres dynamiques (templates Jinja) — non vérifiables
            if titre.startswith("{{"):
                continue
            if not EMOJI_AT_START.match(titre):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : "
                    f"titre mobile sans emoji normatif en tête : «{titre}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T6 — Emoji de tête obligatoire (mobile) : {v}")
    else:
        print("✔ T6 — Tous les titres de notifications mobiles commencent par un emoji normatif")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_titre_commence_par_emoji,
    test_separateur_normatif,
    test_titre_sans_formulation_evenementielle,
    test_absence_reference_temporelle,
    test_unicite_notification_id,
    test_titre_mobile_commence_par_emoji,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Notifications (transverse)\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT NOTIFICATIONS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT NOTIFICATIONS CONFORME")
