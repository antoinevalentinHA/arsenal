#!/usr/bin/env python3
"""
Arsenal — Contrat UI Couleurs SÉMANTIQUES (invariant I1 — garde indisponibilité)

Source normative :
  00_documentation_arsenal/ui/couleurs/02_palette.md
    · « ⚪ Gris indisponibilité — Donnée indisponible / inconnue » :
      unknown / unavailable / entité absente / valeur non exploitable
      => rgba(158, 158, 158, 0.1) (« Prime sur toute autre couleur en cas
      d'indisponibilité » ; « Ne doit jamais être confondu avec un état
      neutre valide », distinct du gris neutre 0.2).
  00_documentation_arsenal/ui/couleurs/05_regles.md
    · Règle R6 — « Le gris indisponibilité prime sur toute couleur sémantique ».
    · Interdit global — « Masquer unknown / unavailable par une couleur
      sémantique » (interdit absolu).
  00_documentation_arsenal/ui/couleurs/03_exceptions.md
    · Chaque exception (HVAC, thermique, NAV, quantitatif, KPI, hydrique,
      humidex) réaffirme « le gris indisponibilité prime toujours » : aucune
      n'autorise une autre couleur pour un état unavailable / unknown.

Positionnement (3e étage couleurs, complémentaire) :
  - check_ui_couleurs_contracts.py        → cohérence DOCUMENTAIRE de la charte
  - check_ui_runtime_colors_contracts.py  → vocabulaire LEXICAL (valeurs whitelistées)
  - check_ui_semantic_colors_contracts.py → sens SÉMANTIQUE (la bonne couleur
                                            pour la bonne réalité métier)

Le contrôle lexical laisse passer une carte qui rend le gris NEUTRE
`rgba(158,158,158,0.2)` (valeur de palette valide) pour un état `unavailable` :
bon vocabulaire, mauvais sens. C'est le trou que ferme l'invariant I1.

INVARIANT I1 — Garde indisponibilité
  Tout bloc JS `[[[ ... ]]]` qui calcule un `background-color` ET qui résout un
  état d'entité littéral `'unavailable'` / `'unknown'` DOIT retourner le gris
  indisponibilité `rgba(158, 158, 158, 0.1)`. À défaut, l'état indisponible est
  peint par une autre couleur — gris neutre 0.2 (« inactif », état valide,
  interdit de confusion) ou couleur sémantique (interdit absolu R6).

Périmètre volontairement BORNÉ (heuristique inattaquable, zéro faux positif) :
  - `background-color` UNIQUEMENT. La table « indisponibilité » régit le FOND ;
    la couleur de TEXTE relève de la typographie (04_typographie.md, #111).
  - Déclencheur = littéral EXPLICITE `'unavailable'` / `'unknown'`. Le bare
    `isNaN(...)` N'EST PAS un déclencheur : la charte autorise une valeur non
    numérique à virer au ROUGE (« donnée invalide critique », 05_regles) ou au
    gris neutre 0.2 (« valeur non numérique », exceptions 2 thermique / 8
    humidex). Déclencher sur `isNaN` produirait un faux positif sur ces cas
    documentés. On ne juge donc que l'état d'indisponibilité NOMMÉ, dont la
    couleur est absolue et sans exception.
  - la garde et la couleur doivent vivre dans le MÊME bloc `[[[ ]]]`. Un template
    qui délègue la garde ailleurs n'est pas jugé (faux négatif assumé, jamais
    faux positif).
  - ce contrôle NE prouve PAS la hiérarchie complète R1–R5 (ordre rouge → vert) :
    il se limite à la garde indisponibilité R6, l'interdit absolu de la charte.

Opt-out explicite (jamais d'exemption silencieuse) :
  Un bloc réellement non idiomatique peut être exempté par l'annotation
  `# arsenal:semantic-colors:ack` placée dans le bloc ou juste au-dessus de la
  clé `background-color`. L'exemption est tracée dans le code de la carte,
  auditable en revue.

Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python3 scripts/arsenal_contracts/check_ui_semantic_colors_contracts.py
  python3 scripts/arsenal_contracts/check_ui_semantic_colors_contracts.py --selftest
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []

SCAN_DIRS = [
    ROOT / "18_lovelace",
    ROOT / "19_button_card_templates",
]

EXCLUDED_PARTS = [
    "/www/",
    "/00_documentation_arsenal/",
]

# ==========================================================
# Gris indisponibilité contractuel (charte 02_palette.md)
# ==========================================================

GRIS_INDISPONIBILITE = "rgba(158,158,158,0.1)"

# ==========================================================
# Annotation d'opt-out (exemption tracée)
# ==========================================================

ACK_MARKER = "arsenal:semantic-colors:ack"

# ==========================================================
# Détection d'une garde d'indisponibilité dans un bloc JS
#
# Déclencheur = état d'entité littéral 'unavailable' / 'unknown'.
# (Le bare isNaN n'est PAS un déclencheur : cf. docstring — la charte
#  autorise non-numérique -> rouge ou gris neutre 0.2 dans des cas
#  documentés hors périmètre.)
# ==========================================================

UNAVAILABILITY_LITERAL_PATTERN = re.compile(r"unavailable|unknown")


def has_availability_guard(body: str):

    return bool(UNAVAILABILITY_LITERAL_PATTERN.search(body))


# ==========================================================
# Blocs JS button-card : [[[ ... ]]]
# ==========================================================

BLOCK_PATTERN = re.compile(r"\[\[\[(.*?)\]\]\]", re.S)

# La clé qui INTRODUIT le bloc doit être `background-color` (le fond).
# `[|>]?` : bloc YAML littéral/plié ; `\n\s*` : le `[[[` est sur la ligne suivante.
BACKGROUND_KEY_PATTERN = re.compile(
    r"background-color\s*:\s*[|>]?\s*\n?\s*$"
)


# ==========================================================
# Utilitaires
# ==========================================================

def fail(msg):
    ERRORS.append(msg)


def should_skip(path: Path):

    path_str = str(path)

    for excluded in EXCLUDED_PARTS:

        if excluded in path_str:
            return True

    return False


def normalize_color(value: str):

    value = value.strip()

    value = re.sub(r"\s+", "", value)

    value = re.sub(
        r"(\d+\.\d*?[1-9])0+\)",
        r"\1)",
        value,
    )

    value = value.replace(".0)", ")")

    return value.lower()


def normalize_color_block(body: str):
    """Normalise chaque littéral rgba du bloc pour comparaison tolérante
    (espaces, casse, opacité 0.10 ≡ 0.1)."""

    def _norm(match):
        return normalize_color(match.group(0))

    return re.sub(
        r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[0-9.]+\s*\)",
        _norm,
        body,
    ).lower()


def iter_yaml_files():

    for base in SCAN_DIRS:

        if not base.exists():
            continue

        for path in base.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix not in [".yaml", ".yml"]:
                continue

            if should_skip(path):
                continue

            yield path


def iter_background_color_blocks(content: str):
    """
    Émet (body, pre_window) pour chaque bloc `[[[ ]]]` qui est la valeur d'une
    clé `background-color`. `pre_window` couvre la clé et les commentaires qui
    la précèdent immédiatement (support de l'opt-out placé au-dessus).
    """

    for match in BLOCK_PATTERN.finditer(content):

        pre_window = content[max(0, match.start() - 160):match.start()]

        if not BACKGROUND_KEY_PATTERN.search(pre_window):
            continue

        yield match.group(1), pre_window


def is_acked(body: str, pre_window: str):

    return ACK_MARKER in body or ACK_MARKER in pre_window


# ==========================================================
# T1 — Invariant I1 : garde indisponibilité
# ==========================================================

def test_unavailability_guard_returns_gris_indispo():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        for body, pre_window in iter_background_color_blocks(content):

            # --------------------------------------------------
            # Pas d'état d'indisponibilité nommé → hors périmètre I1
            # --------------------------------------------------

            if not has_availability_guard(body):
                continue

            # --------------------------------------------------
            # Exemption explicite et tracée
            # --------------------------------------------------

            if is_acked(body, pre_window):
                continue

            # --------------------------------------------------
            # L'état indisponible doit peindre le gris indispo
            # --------------------------------------------------

            if GRIS_INDISPONIBILITE not in normalize_color_block(body):

                fail(
                    f"{path} : bloc background-color résolvant un état "
                    f"'unavailable'/'unknown' sans gris indisponibilité "
                    f"{GRIS_INDISPONIBILITE} — viole R6 (05_regles.md) / "
                    f"02_palette.md (gris indispo distinct du gris neutre 0.2). "
                    f"Exemption possible via `# {ACK_MARKER}` si non idiomatique."
                )

    if not ERRORS:
        print("✔ garde indisponibilité conforme (I1)")


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_unavailability_guard_returns_gris_indispo",
]


def test_test_registry_matches_functions():

    missing = []

    for test_name in TESTS:

        if test_name not in globals():
            missing.append(test_name)

    if missing:

        for name in missing:
            fail(
                f"fonction absente du registre TESTS : {name}"
            )

    if not ERRORS:
        print("✔ registre TESTS cohérent")


# ==========================================================
# Auto-test du juge (on ne juge pas avec un juge défectueux)
# ==========================================================

def selftest():

    def blocks(content):
        return list(iter_background_color_blocks(content))

    def verdict(js_body):
        """Reproduit la décision de T1 pour un bloc isolé."""
        content = (
            "      - background-color: |\n"
            "          [[[\n" + js_body + "\n          ]]]\n"
        )
        found = blocks(content)
        assert found, "fixture : bloc background-color non reconnu"
        js, pre = found[0]
        if not has_availability_guard(js):
            return "hors-perimetre"
        if is_acked(js, pre):
            return "acke"
        return "ok" if GRIS_INDISPONIBILITE in normalize_color_block(js) else "viole"

    # 1. état 'unavailable' → gris indispo présent : conforme
    assert verdict(
        "const s=entity?.state;\n"
        "if(s==='unavailable'||s==='unknown') return 'rgba(158,158,158,0.1)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "ok", "selftest I1 conforme"

    # 2. état 'unavailable' → gris NEUTRE 0.2 (état « inactif », pas indispo) : violation
    assert verdict(
        "if(entity.state==='unavailable') return 'rgba(158,158,158,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "viole", "selftest I1 gris neutre = violation"

    # 3. état 'unknown' → couleur sémantique (masquage) : violation
    assert verdict(
        "if(entity.state==='unknown') return 'rgba(76,175,80,0.2)';\n"
        "return 'rgba(244,67,54,0.2)';"
    ) == "viole", "selftest I1 unknown masqué"

    # 4. opacité écrite 0.10 ≡ 0.1 : conforme (normalisation)
    assert verdict(
        "if(entity.state==='unavailable') return 'rgba(158, 158, 158, 0.10)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "ok", "selftest I1 normalisation 0.10"

    # 5. aucun état d'indisponibilité nommé : hors périmètre (jamais flaggé)
    assert verdict(
        "return entity.state>0 ? 'rgba(244,67,54,0.2)' : 'rgba(76,175,80,0.2)';"
    ) == "hors-perimetre", "selftest I1 hors perimetre"

    # 5b. bare isNaN SANS littéral : hors périmètre — la charte autorise
    #     non-numérique → rouge (invalide-critique) ou gris neutre 0.2
    #     (thermique/humidex). On ne le juge donc pas (zéro faux positif).
    assert verdict(
        "const v=Number(entity?.state);\n"
        "if(isNaN(v)) return 'rgba(158,158,158,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "hors-perimetre", "selftest I1 isNaN seul hors perimetre"

    # 6. opt-out explicite : exempté même si non conforme
    assert verdict(
        "// " + ACK_MARKER + "\n"
        "if(entity.state==='unavailable') return 'rgba(158,158,158,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "acke", "selftest I1 opt-out"

    # 7. clé `color` (texte) NON assujettie à I1 : bloc non reconnu comme fond
    txt = (
        "      - color: |\n          [[[\n"
        " if(entity.state==='unavailable') return '#111';\n          ]]]\n"
    )
    assert not blocks(txt), "selftest I1 borne au fond (color texte ignoré)"

    print("✅ SELFTEST check_ui_semantic_colors OK")


# ==========================================================
# exécution
# ==========================================================

if __name__ == "__main__":

    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)

    for test_name in TESTS:
        globals()[test_name]()

    test_test_registry_matches_functions()

    if ERRORS:

        print("\n❌ CONTRAT UI_SEMANTIC_COLORS NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT UI_SEMANTIC_COLORS CONFORME")
