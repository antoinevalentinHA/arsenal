#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Climatisation — Franchissement d'extinction COOL (sens de comparaison)

Référence :
  - 00_documentation_arsenal/contrats/climatisation/capteurs/
    seuils_et_franchissements/20_binary_sensors_franchissement.md

Objet :
  Figer le sens de la comparaison du franchissement OFF COOL après la
  correction du bug D8 (extinction héritée à tort du pattern HEAT).

  Invariants :
    1. L'extinction COOL doit s'exprimer  temp_min <= seuil_off
       (le besoin de froid cesse quand la température DESCEND au seuil OFF).
    2. La forme inversée  temp_min >= seuil_off  est interdite
       (régression D8).
    3. Garde-fou : l'allumage COOL doit rester  temp_max >= seuil_on
       (ne pas inverser le mauvais front).

Position du script dans le repo :
  scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[2]  → racine du dépôt

Usage :
    python check_climatisation_seuils_cool_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROOT — racine du dépôt
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

EXTINCTION_COOL = (
    ROOT
    / "12_template_sensors"
    / "climatisation"
    / "seuils_on_off"
    / "cool"
    / "seuil_extinction_cool_atteint.yaml"
)

ALLUMAGE_COOL = (
    ROOT
    / "12_template_sensors"
    / "climatisation"
    / "seuils_on_off"
    / "cool"
    / "seuil_allumage_cool_atteint.yaml"
)

# ---------------------------------------------------------------------------
# Patterns (tolérants aux espaces)
# ---------------------------------------------------------------------------

RE_EXTINCTION_OK = re.compile(
    r"temp_min\s*\|\s*float\s*<=\s*seuil_off\s*\|\s*float"
)
RE_EXTINCTION_INVERSE = re.compile(
    r"temp_min\s*\|\s*float\s*>=\s*seuil_off"
)
RE_ALLUMAGE_OK = re.compile(
    r"temp_max\s*\|\s*float\s*>=\s*seuil_on\s*\|\s*float"
)
# Sens de comparaison HEAT (garde-fous, conservés par L3B)
RE_HEAT_ON_OK = re.compile(r"temp_min\s*\|\s*float\s*<\s*seuil_on\s*\|\s*float")
RE_HEAT_OFF_OK = re.compile(r"temp_min\s*\|\s*float\s*>=\s*seuil_off\s*\|\s*float")

# ---------------------------------------------------------------------------
# C28 L3B — honnêteté amont (COOL + HEAT) — chemins
# ---------------------------------------------------------------------------

_SEUILS = ROOT / "12_template_sensors" / "climatisation" / "seuils_on_off"
_BESOIN = ROOT / "12_template_sensors" / "climatisation" / "besoin"

# Seuils appliqués : {chemin: (operandes attendus dans l'availability)}
SEUILS_COOL = {
    _SEUILS / "cool" / "on.yaml": (
        "clim_seuil_declenchement_presence", "clim_seuil_declenchement_absence"),
    _SEUILS / "cool" / "off.yaml": (
        "clim_seuil_extinction_presence", "clim_seuil_extinction_absence"),
}
SEUILS_HEAT = {
    _SEUILS / "heat" / "on.yaml": "clim_offset_on",
    _SEUILS / "heat" / "off.yaml": "clim_offset_off",
}
# Franchissements : {chemin: (temperature, seuil applique)}
FRANCHISSEMENTS = {
    _SEUILS / "cool" / "seuil_allumage_cool_atteint.yaml": (
        "sensor.temperature_max_chambres", "sensor.seuil_allumage_clim_applique"),
    _SEUILS / "cool" / "seuil_extinction_cool_atteint.yaml": (
        "sensor.temperature_min_chambres", "sensor.seuil_extinction_clim_applique"),
    _SEUILS / "heat" / "seuil_allumage_heat_atteint.yaml": (
        "sensor.temperature_min_chambres", "sensor.seuil_allumage_chauffage_clim"),
    _SEUILS / "heat" / "seuil_extinction_heat_atteint.yaml": (
        "sensor.temperature_min_chambres", "sensor.seuil_extinction_chauffage_clim"),
}
# Besoins : {chemin: (franchissement ON, franchissement OFF)}
BESOINS = {
    _BESOIN / "cool.yaml": (
        "clim_seuil_allumage_cool_atteint", "clim_seuil_extinction_cool_atteint"),
    _BESOIN / "heat.yaml": (
        "clim_seuil_allumage_heat_atteint", "clim_seuil_extinction_heat_atteint"),
}
BESOIN_DRY = _BESOIN / "dry.yaml"
SELECTEURS_COOL = (
    "binary_sensor.presence_confort_thermique_stabilisee",
    "binary_sensor.clim_mode_nuit_effectif",
)


def block(content, key):
    """Extrait le corps d'un bloc scalaire `key: >` jusqu'à la clé sœur suivante
    (même indentation) ou la fin de fichier. Découpage textuel volontaire
    (pas de dépendance PyYAML — la CI n'en installe aucune)."""
    m = re.search(
        r"\n(?P<ind>[ ]*)" + re.escape(key) + r":\s*>\s*\n(?P<body>.*?)"
        r"(?=\n(?P=ind)[A-Za-z_]|\Z)",
        content, re.DOTALL,
    )
    return m.group("body") if m else ""


# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_fichiers_presents():
    for path in (EXTINCTION_COOL, ALLUMAGE_COOL):
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")


def test_extinction_cool_sens_correct():
    if not EXTINCTION_COOL.is_file():
        return
    content = read(EXTINCTION_COOL)

    if RE_EXTINCTION_INVERSE.search(content):
        fail(
            "Régression D8 : extinction COOL utilise 'temp_min >= seuil_off'. "
            "Le franchissement OFF doit être 'temp_min <= seuil_off'."
        )

    if not RE_EXTINCTION_OK.search(content):
        fail(
            "Extinction COOL : comparaison 'temp_min <= seuil_off' introuvable "
            f"dans {EXTINCTION_COOL.relative_to(ROOT)}."
        )


def test_allumage_cool_non_inverse():
    if not ALLUMAGE_COOL.is_file():
        return
    content = read(ALLUMAGE_COOL)
    if not RE_ALLUMAGE_OK.search(content):
        fail(
            "Garde-fou : l'allumage COOL doit rester 'temp_max >= seuil_on' "
            f"dans {ALLUMAGE_COOL.relative_to(ROOT)}."
        )


# ---------------------------------------------------------------------------
# Tests — C28 L3B (honnêteté amont, liés aux blocs)
# ---------------------------------------------------------------------------

def test_seuils_cool_availability_abstention():
    """COOL : pas de float(0) ; availability abstient sur sélecteur présence/nuit
    indisponible (jamais 'absence' silencieuse) et valide numériquement
    l'input_number sélectionné."""
    for path, (inp_p, inp_a) in SEUILS_COOL.items():
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")
            continue
        c = read(path)
        rel = path.relative_to(ROOT)
        if "float(0)" in c:
            fail(f"Seuil COOL {rel} : repli numérique 'float(0)' interdit (C28 L3B).")
        av = block(c, "availability")
        if not av:
            fail(f"Seuil COOL {rel} : bloc 'availability' absent.")
            continue
        for sel in SELECTEURS_COOL:
            if sel not in av:
                fail(f"Seuil COOL {rel} : availability n'inclut pas le sélecteur {sel}.")
        # abstention explicite (jamais 'absence') sur sélecteur indisponible
        if "['unknown', 'unavailable']" not in av or "false" not in av:
            fail(f"Seuil COOL {rel} : availability ne s'abstient pas ('false') sur "
                 f"sélecteur présence/nuit indisponible (interdit de le traiter en 'absence').")
        if "float(none) is not none" not in av:
            fail(f"Seuil COOL {rel} : availability ne valide pas numériquement l'opérande sélectionné.")
        if inp_p not in av or inp_a not in av:
            fail(f"Seuil COOL {rel} : availability ne référence pas les input_number sélectionnables "
                 f"({inp_p} / {inp_a}).")


def test_seuils_heat_availability_no_fallback():
    """HEAT : pas de float(20)/float(0.5) ; availability sur consigne + offset."""
    for path, offset in SEUILS_HEAT.items():
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")
            continue
        c = read(path)
        rel = path.relative_to(ROOT)
        for bad in ("float(20)", "float(0.5)"):
            if bad in c:
                fail(f"Seuil HEAT {rel} : repli numérique '{bad}' interdit (C28 L3B).")
        av = block(c, "availability")
        if "temperature_consigne_appliquee_locale" not in av:
            fail(f"Seuil HEAT {rel} : availability n'inclut pas la consigne appliquée.")
        if offset not in av:
            fail(f"Seuil HEAT {rel} : availability n'inclut pas l'offset {offset}.")
        if "float(none) is not none" not in av:
            fail(f"Seuil HEAT {rel} : availability ne valide pas numériquement consigne/offset.")


def test_franchissements_availability_no_false():
    """Franchissements : availability liée (température + seuil) dans le même bloc ;
    plus aucune branche transformant l'indisponibilité en 'false' ;
    comparaison nominale conservée."""
    for path, (temp, seuil) in FRANCHISSEMENTS.items():
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")
            continue
        c = read(path)
        rel = path.relative_to(ROOT)
        av = block(c, "availability")
        st = block(c, "state")
        if temp not in av or seuil not in av:
            fail(f"Franchissement {rel} : availability n'inclut pas, dans le même bloc, "
                 f"la température ({temp}) ET le seuil ({seuil}).")
        if "float(none) is not none" not in av:
            fail(f"Franchissement {rel} : availability ne valide pas numériquement température/seuil.")
        if "false" in st or "unavailable" in st or "unknown" in st:
            fail(f"Franchissement {rel} : le 'state' retourne 'false' / teste l'indisponibilité "
                 f"(interdit C28 : l'opérande mort doit produire 'unavailable', pas 'off').")


def test_besoins_availability_franchissements():
    """Besoins : availability liée aux DEUX franchissements ; aucune lecture directe
    de température/seuil ; maintien this.entity_id conservé."""
    for path, (fr_on, fr_off) in BESOINS.items():
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")
            continue
        c = read(path)
        rel = path.relative_to(ROOT)
        av = block(c, "availability")
        st = block(c, "state")
        if fr_on not in av or fr_off not in av:
            fail(f"Besoin {rel} : availability n'inclut pas les deux franchissements "
                 f"({fr_on} / {fr_off}).")
        if "['unknown', 'unavailable']" not in av:
            fail(f"Besoin {rel} : availability ne teste pas la vivacité des franchissements.")
        if "sensor.temperature_" in c or "sensor.seuil_" in c:
            fail(f"Besoin {rel} : lecture directe d'une température/seuil interdite "
                 f"(l'architecture impose de passer par les franchissements).")
        if "is_state(this.entity_id, 'on')" not in st:
            fail(f"Besoin {rel} : maintien d'hystérésis 'is_state(this.entity_id, 'on')' supprimé.")


def test_dry_besoin_sans_c28():
    """DRY hors périmètre : aucune doctrine C28 (availability) ajoutée au besoin DRY."""
    if not BESOIN_DRY.is_file():
        fail(f"Fichier absent : {BESOIN_DRY.relative_to(ROOT)}")
        return
    if re.search(r"^\s*availability\s*:", read(BESOIN_DRY), re.MULTILINE):
        fail(f"Besoin DRY {BESOIN_DRY.relative_to(ROOT)} : doctrine C28 (availability) "
             f"ajoutée indûment (DRY est hors périmètre).")


def test_franchissements_heat_sens_correct():
    """Garde-fou : sens de comparaison HEAT conservé (ON: temp_min < seuil_on ;
    OFF: temp_min >= seuil_off)."""
    on = _SEUILS / "heat" / "seuil_allumage_heat_atteint.yaml"
    off = _SEUILS / "heat" / "seuil_extinction_heat_atteint.yaml"
    if on.is_file() and not RE_HEAT_ON_OK.search(read(on)):
        fail(f"Franchissement HEAT ON : 'temp_min < seuil_on' introuvable ({on.relative_to(ROOT)}).")
    if off.is_file() and not RE_HEAT_OFF_OK.search(read(off)):
        fail(f"Franchissement HEAT OFF : 'temp_min >= seuil_off' introuvable ({off.relative_to(ROOT)}).")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    tests = [
        test_fichiers_presents,
        test_extinction_cool_sens_correct,
        test_allumage_cool_non_inverse,
        test_franchissements_heat_sens_correct,
        test_seuils_cool_availability_abstention,
        test_seuils_heat_availability_no_fallback,
        test_franchissements_availability_no_false,
        test_besoins_availability_franchissements,
        test_dry_besoin_sans_c28,
    ]
    for test in tests:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print("\n❌ CONTRAT CLIMATISATION_SEUILS_COOL NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CLIMATISATION_SEUILS_COOL CONFORME")
        sys.exit(0)


if __name__ == "__main__":
    main()
