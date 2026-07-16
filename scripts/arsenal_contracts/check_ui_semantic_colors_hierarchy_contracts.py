#!/usr/bin/env python3
"""
Arsenal — Contrat UI Couleurs SÉMANTIQUES : hiérarchie (invariant I2)

Source normative :
  00_documentation_arsenal/ui/couleurs/05_regles.md — « Priorités sémantiques »
    · R1 — Le rouge prime toujours sur toute autre couleur.
    · R2 — L'orange ne masque jamais un rouge.
    · R3 — Le jaune ne masque jamais un orange ni un rouge.
    · R4 — Le vert n'apparaît que s'il n'existe aucune anomalie active.
  Ordre de sévérité : 🔴 rouge > 🟠 orange > 🟡 jaune > 🟢 vert.

Complément du contrat I1 (`check_ui_semantic_colors_contracts.py`, garde
indisponibilité). I2 vérifie l'ORDRE des couleurs dans une cascade de masquage.

--------------------------------------------------------------------------
PÉRIMÈTRE — VOLONTAIREMENT ÉTROIT (heuristique zéro faux positif)
--------------------------------------------------------------------------
Dans une cascade `if (…) return X; … return défaut;`, la PREMIÈRE condition
vraie gagne. L'ordre ne porte un risque de masquage QUE si les conditions se
CHEVAUCHENT (cascade dite « de masquage », ex. `v > crit` implique `v > warn`).
Il ne porte AUCUN risque quand les conditions sont MUTUELLEMENT EXCLUSIVES :

  - paliers à bandes (`v <= s1` / `v <= s2` … , ex. bruit, humidex) — l'ordre
    suit la VALEUR croissante, souvent l'inverse de la sévérité ; LÉGITIME ;
  - mappings état→couleur discrets (`state === 'x'`, modes HVAC — Exception R7) ;
  - couleur décidée par le backend (`p[key]`, socle KPI) ;
  - palette thermique (froid = bleu).

Sur ce dépôt, ~80 % des blocs `background-color` multi-couleurs relèvent de ces
cas exclusifs : une règle d'ordre naïve y produirait des faux positifs massifs.
I2 ne juge donc QUE les cascades de MASQUAGE, identifiées par un discriminant
robuste (cf. étude de corpus) :

  DÉCLENCHEUR — un bloc `background-color` est une cascade de masquage ssi :
    (a) il contient une comparaison numérique (`<` ou `>`), ET
    (b) il n'est PAS catégoriel (aucune égalité de chaîne `=== '…'`, aucun
        `.includes(`, aucun mapping `p[…]`), ET
    (c) il n'est PAS thermique (pas de bleu froid `rgba(144,202,249,…)`), ET
    (d) le VERT est en position de FALLBACK — il apparaît APRÈS toutes les
        couleurs plus sévères (R4 : « le vert n'apparaît que s'il n'existe
        aucune anomalie »). Si le vert est en tête, c'est une bande → ignoré.

  CONTRÔLE — pour un tel bloc, la séquence des `return` colorés qui PRÉCÈDENT
  le vert doit être de sévérité NON CROISSANTE (le plus sévère d'abord :
  rouge → orange → jaune). Une inversion (ex. orange retourné avant rouge, avec
  vert en fallback) masque la couleur la plus sévère → viole R1/R2/R3.

Bornes assumées :
  - `background-color` uniquement (le texte relève de la typographie).
  - Blocs `[[[ ]]]` uniquement ; les machines `state:` de button-card (cascade
    éclatée en items YAML) ne sont PAS jugées (faux négatif assumé, jamais FP).
  - I2 ne prouve pas l'absence de masquage dans les cas exclusifs (par nature
    hors R1–R4). Un bloc réellement non idiomatique s'exempte par l'annotation
    `# arsenal:semantic-colors:ack` (exemption tracée).

Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python3 scripts/arsenal_contracts/check_ui_semantic_colors_hierarchy_contracts.py
  python3 scripts/arsenal_contracts/check_ui_semantic_colors_hierarchy_contracts.py --selftest
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

ACK_MARKER = "arsenal:semantic-colors:ack"

# ==========================================================
# Sévérité des couleurs (rang : 0 = plus sévère)
#   rouge / rouge foncé = 0 ; orange = 1 ; jaune (2 teintes) = 2 ; vert = 3
# Le bleu est informatif : hors du cœur R1–R4, non classé ici.
# ==========================================================

GREEN = "rgba(76,175,80,"

SEVERITY = [
    ("rgba(244,67,54,", 0),   # 🔴 rouge
    ("rgba(183,28,28,", 0),   # 🔴 rouge foncé (apex humidex)
    ("rgba(255,152,0,", 1),   # 🟠 orange
    ("rgba(255,235,59,", 2),  # 🟡 jaune
    ("rgba(255,193,7,", 2),   # 🟡 jaune renforcé
]

THERMAL_COLD = "rgba(144,202,249,"

# Signature « catégoriel / backend » : égalité de chaîne, includes, map p[…].
CATEGORICAL_PATTERN = re.compile(r"===?\s*['\"]|\.includes\(|\bp\[")

# Comparaison numérique (seuils).
NUMERIC_COMPARISON_PATTERN = re.compile(r"[<>]")

BLOCK_PATTERN = re.compile(r"\[\[\[(.*?)\]\]\]", re.S)

BACKGROUND_KEY_PATTERN = re.compile(r"background-color\s*:\s*[|>]?\s*\n?\s*$")


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


def strip_spaces(body: str):
    return re.sub(r"\s+", "", body).lower()


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
    for match in BLOCK_PATTERN.finditer(content):
        pre_window = content[max(0, match.start() - 160):match.start()]
        if not BACKGROUND_KEY_PATTERN.search(pre_window):
            continue
        yield match.group(1), pre_window


def is_acked(body: str, pre_window: str):
    return ACK_MARKER in body or ACK_MARKER in pre_window


def severe_positions(compact: str):
    """Positions (index, rang) de chaque occurrence de couleur plus sévère
    que le vert, dans le bloc compacté."""
    hits = []
    for token, rank in SEVERITY:
        idx = compact.find(token)
        while idx != -1:
            hits.append((idx, rank))
            idx = compact.find(token, idx + 1)
    return sorted(hits)


def masking_verdict(body: str, pre_window: str = ""):
    """
    Retourne :
      'hors-perimetre' — pas une cascade de masquage (exclusif / bande / etc.)
      'acke'           — exempté par annotation
      'ok'             — cascade de masquage bien ordonnée
      'viole'          — cascade de masquage à ordre inversé
    """
    compact = strip_spaces(body)

    green_pos = compact.find(GREEN)
    severe = severe_positions(compact)

    # (pré-requis) au moins une couleur sévère ET le vert présents
    if green_pos == -1 or not severe:
        return "hors-perimetre"

    # (a) comparaison numérique présente
    if not NUMERIC_COMPARISON_PATTERN.search(compact):
        return "hors-perimetre"

    # (b) non catégoriel / backend
    if CATEGORICAL_PATTERN.search(compact):
        return "hors-perimetre"

    # (c) non thermique
    if THERMAL_COLD in compact:
        return "hors-perimetre"

    # (d) vert en fallback (après toute couleur plus sévère) ; sinon bande
    if green_pos < min(pos for pos, _ in severe):
        return "hors-perimetre"

    if is_acked(body, pre_window):
        return "acke"

    # contrôle : rangs pré-vert non croissants (plus sévère d'abord)
    pre_green_ranks = [rank for pos, rank in severe if pos < green_pos]
    inversion = any(
        pre_green_ranks[i] > min(pre_green_ranks[i + 1:])
        for i in range(len(pre_green_ranks) - 1)
    )
    return "viole" if inversion else "ok"


# ==========================================================
# T1 — Invariant I2 : ordre de sévérité dans les cascades de masquage
# ==========================================================

def test_masking_cascade_severity_order():

    for path in iter_yaml_files():

        content = path.read_text(encoding="utf-8", errors="ignore")

        for body, pre_window in iter_background_color_blocks(content):

            verdict = masking_verdict(body, pre_window)

            if verdict == "viole":
                fail(
                    f"{path} : cascade background-color de masquage à ordre "
                    f"inversé — une couleur moins sévère est retournée avant "
                    f"une plus sévère (vert en fallback) ; viole R1/R2/R3 "
                    f"(05_regles.md : le rouge prime, l'orange/jaune ne masque "
                    f"jamais un rouge). Exemption possible via "
                    f"`# {ACK_MARKER}` si cascade non idiomatique."
                )

    if not ERRORS:
        print("✔ ordre de sévérité des cascades de masquage conforme (I2)")


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_masking_cascade_severity_order",
]


def test_test_registry_matches_functions():
    missing = [t for t in TESTS if t not in globals()]
    if missing:
        for name in missing:
            fail(f"fonction absente du registre TESTS : {name}")
    if not ERRORS:
        print("✔ registre TESTS cohérent")


# ==========================================================
# Auto-test du juge (on ne juge pas avec un juge défectueux)
# ==========================================================

def selftest():

    def verdict(js_body, key="background-color"):
        content = (
            f"      - {key}: |\n"
            "          [[[\n" + js_body + "\n          ]]]\n"
        )
        found = list(iter_background_color_blocks(content))
        if not found:
            return "no-bloc"
        body, pre = found[0]
        return masking_verdict(body, pre)

    # 1. masquage bien ordonné (rouge → orange → vert fallback) : conforme
    assert verdict(
        "if(!isNaN(crit)&&v>crit) return 'rgba(244,67,54,0.2)';\n"
        "if(!isNaN(warn)&&v>warn) return 'rgba(255,152,0,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "ok", "selftest I2 masquage conforme"

    # 1b. masquage seuils bas (rouge → orange → jaune → vert), `<` : conforme
    assert verdict(
        "if(v<s_crit) return 'rgba(244,67,54,0.2)';\n"
        "if(v<s_low) return 'rgba(255,152,0,0.2)';\n"
        "if(v<s_mid) return 'rgba(255,193,7,0.25)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "ok", "selftest I2 masquage bas conforme"

    # 2. masquage INVERSÉ (orange avant rouge, vert fallback) : violation
    assert verdict(
        "if(v>warn) return 'rgba(255,152,0,0.2)';\n"
        "if(v>crit) return 'rgba(244,67,54,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "viole", "selftest I2 inversion orange<rouge"

    # 3. bande ascendante (vert en PREMIER) : hors périmètre (légitime)
    assert verdict(
        "if(v<=s1) return 'rgba(76,175,80,0.2)';\n"
        "if(v<=s2) return 'rgba(255,152,0,0.2)';\n"
        "return 'rgba(244,67,54,0.2)';"
    ) == "hors-perimetre", "selftest I2 bande vert-premier"

    # 4. catégoriel (égalité de chaîne) : hors périmètre même vert-fallback + inversion
    assert verdict(
        "if(entity.state==='warn') return 'rgba(255,152,0,0.2)';\n"
        "if(entity.state==='error') return 'rgba(244,67,54,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "hors-perimetre", "selftest I2 catégoriel exclu"

    # 5. thermique (bleu froid présent) : hors périmètre
    assert verdict(
        "if(v>seuil) return 'rgba(244,67,54,0.2)';\n"
        "if(v<0) return 'rgba(144,202,249,0.25)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "hors-perimetre", "selftest I2 thermique exclu"

    # 6. backend map p[key] : hors périmètre
    assert verdict(
        "const p={ok:'rgba(76,175,80,0.2)',ko:'rgba(244,67,54,0.2)'};\n"
        "if(v>0) return p[k]||p.ok; return p.ok;"
    ) == "hors-perimetre", "selftest I2 backend map exclu"

    # 7. opt-out explicite sur un masquage inversé : exempté
    assert verdict(
        "// " + ACK_MARKER + "\n"
        "if(v>warn) return 'rgba(255,152,0,0.2)';\n"
        "if(v>crit) return 'rgba(244,67,54,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "acke", "selftest I2 opt-out"

    # 8. une seule couleur sévère + vert (pas de hiérarchie à ordonner) : ok trivial
    assert verdict(
        "if(v>crit) return 'rgba(244,67,54,0.2)';\n"
        "return 'rgba(76,175,80,0.2)';"
    ) == "ok", "selftest I2 mono-sévère"

    # 9. clé `color` (texte) : bloc non reconnu comme fond
    txt = (
        "      - color: |\n          [[[\n"
        " if(v>crit) return 'rgba(244,67,54,0.2)'; return 'rgba(76,175,80,0.2)';\n"
        "          ]]]\n"
    )
    assert not list(iter_background_color_blocks(txt)), "selftest I2 borne au fond"

    print("✅ SELFTEST check_ui_semantic_colors_hierarchy OK")


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
        print("\n❌ CONTRAT UI_SEMANTIC_COLORS_HIERARCHY NON CONFORME")
        for error in ERRORS:
            print(f"- {error}")
        sys.exit(1)

    print("\n✅ CONTRAT UI_SEMANTIC_COLORS_HIERARCHY CONFORME")
