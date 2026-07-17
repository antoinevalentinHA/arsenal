"""Lot 3 (C24) — Verrouillage CI local ECS : anti-refabrication numérique (T14).

Premier test unitaire du checker ``check_parametres_invalides_contracts`` : il
exerce la logique du **T14** sur des **fixtures synthétiques** indépendantes du
runtime de production, puis vérifie une propriété **pérenne** sur le dépôt réel
(zéro refabrication same-family sur les lecteurs des deux capteurs sécurisés).

⚠️ Frontière de preuve assumée : **pas** une exécution du moteur de templates
Home Assistant. Le T14 est un verrouillage **local ECS** — il ne bannit pas tout
``float(0)`` du dépôt (cf. contrat ``parametres_invalides.md`` v1.3).

Note : la fixture ``_ANCIEN_FIN`` reproduit l'expression **historique** de
``12_template_sensors/ecs/log/fin.yaml`` (``| float(0)`` sur le capteur sécurisé)
pour prouver que la violation est bien détectée. Ce constat vit dans la fixture,
**pas** dans une recherche du hit « avant correction » au sein du dépôt corrigé.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[3]
_CHECKER_PATH = (
    _ROOT / "scripts" / "arsenal_contracts"
    / "check_parametres_invalides_contracts.py"
)


def _load_checker():
    """Charge le checker par chemin (hors package) sans exécuter ses tests.

    Le module est protégé par ``if __name__ == '__main__'`` : l'import ne
    déclenche aucune validation contre la production.
    """
    spec = importlib.util.spec_from_file_location(
        "check_parametres_invalides_contracts", _CHECKER_PATH
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CHK = _load_checker()

# Chemin cœur C24 (axe 1) et non-cœur (axe 2) — étiquettes de fixtures.
_CORE = "12_template_sensors/ecs/temperature.yaml"
_NONCORE = "12_template_sensors/ecs/log/fin.yaml"

_SECURED_T = "sensor.ecs_temperature_ballon_securisee"
_SECURED_C = "sensor.ecs_consigne_chaudiere_securisee"

# Reproduction synthétique de l'expression HISTORIQUE de log/fin.yaml.
_ANCIEN_FIN = (
    "      state: >\n"
    "        {% set temp = states('sensor.ecs_temperature_ballon_securisee') | float(0) %}\n"
)


# ---------------------------------------------------------------------------
# Axe 1 — fabrications numériques interdites dans les fichiers cœur C24
# ---------------------------------------------------------------------------


def test_axe1_this_state_float0_violation():
    yaml = "        {{ this.state | float(0) }}\n"
    assert CHK.violations_axe1(_CORE, yaml)


@pytest.mark.parametrize(
    "expr",
    [
        "{{ x | float(0) }}",
        "{{ x | float(0.0) }}",
        "{{ x | int(0) }}",
        "{{ x | default(0) }}",
        "{{ d.get('k', 0) }}",
        "{{ a if b else 0 }}",
    ],
)
def test_axe1_motifs_interdits(expr):
    assert CHK.violations_axe1(_CORE, f"        {expr}\n"), expr


@pytest.mark.parametrize(
    "expr",
    [
        "{{ x | float(2.2) }}",   # défaut helper non nul
        "{{ x | float(0.7) }}",   # défaut helper non nul
        "{{ a if b else 0.7 }}",  # else non nul
        "{{ x | float(none) }}",  # forme canonique
    ],
)
def test_axe1_defauts_non_zero_ou_none_conformes(expr):
    assert not CHK.violations_axe1(_CORE, f"        {expr}\n"), expr


# ---------------------------------------------------------------------------
# Axe 2 — refabrication sur lecture directe d'un capteur sécurisé
# ---------------------------------------------------------------------------


def test_axe2_ancien_fin_reproduit_violation():
    # Fixture pérenne : l'expression historique de log/fin.yaml est bien captée.
    assert CHK.violations_axe2(_NONCORE, _ANCIEN_FIN)


@pytest.mark.parametrize("sensor", [_SECURED_T, _SECURED_C])
def test_axe2_lecture_securisee_float0_violation(sensor):
    yaml = f"        {{{{ states('{sensor}') | float(0) }}}}\n"
    assert CHK.violations_axe2(_NONCORE, yaml), sensor


@pytest.mark.parametrize("filt", ["float(0)", "float(0.0)", "int(0)", "default(0)"])
def test_axe2_variantes_fallback_violation(filt):
    yaml = f"        {{{{ states('{_SECURED_T}') | {filt} }}}}\n"
    assert CHK.violations_axe2(_NONCORE, yaml), filt


def test_axe2_float_none_conforme():
    yaml = f"        {{{{ states('{_SECURED_T}') | float(none) }}}}\n"
    assert not CHK.violations_axe2(_NONCORE, yaml)


def test_axe2_capteur_non_securise_float0_ignore():
    # Un capteur NON sécurisé (ex. consigne_dernier_cycle) reste hors périmètre.
    yaml = "        {{ states('sensor.ecs_consigne_dernier_cycle') | float(0) }}\n"
    assert not CHK.violations_axe2(_NONCORE, yaml)


# ---------------------------------------------------------------------------
# Axe 2 — tolérance is_number (garde réellement applicable uniquement)
# ---------------------------------------------------------------------------


def test_axe2_garde_is_number_avant_conversion_conforme():
    # Garde sur la MÊME lecture, textuellement AVANT la conversion → inatteignable.
    yaml = (
        f"        {{{{ (states('{_SECURED_T}') | is_number) and "
        f"(states('{_SECURED_T}') | float(0)) > 40 }}}}\n"
    )
    assert not CHK.violations_axe2(_NONCORE, yaml)


def test_axe2_garde_is_number_autre_variable_violation():
    # Garde sur une AUTRE valeur → ne protège pas la lecture sécurisée.
    yaml = (
        f"        {{{{ (states('sensor.autre') | is_number) and "
        f"(states('{_SECURED_T}') | float(0)) > 40 }}}}\n"
    )
    assert CHK.violations_axe2(_NONCORE, yaml)


def test_axe2_garde_is_number_apres_conversion_violation():
    # Garde placée APRÈS la conversion → ne rend pas le fallback inatteignable.
    yaml = (
        f"        {{{{ (states('{_SECURED_T}') | float(0)) if "
        f"(states('{_SECURED_T}') | is_number) else 0 }}}}\n"
    )
    assert CHK.violations_axe2(_NONCORE, yaml)


def test_axe2_garde_is_number_branche_disjointe_violation():
    # Garde dans une expression Jinja distincte (branche ne protégeant pas la
    # conversion) → non tolérée.
    yaml = (
        f"        {{% if states('{_SECURED_T}') | is_number %}} ok {{% endif %}}\n"
        f"        {{{{ states('{_SECURED_T}') | float(0) }}}}\n"
    )
    assert CHK.violations_axe2(_NONCORE, yaml)


# ---------------------------------------------------------------------------
# Robustesse au découpage multi-lignes
# ---------------------------------------------------------------------------


def test_axe2_expression_multilignes_detectee():
    # states(...) sur une ligne, | float(0) sur la suivante : réassemblé, capté.
    yaml = (
        "        {% set temp = states('sensor.ecs_temperature_ballon_securisee')\n"
        "           | float(0) %}\n"
    )
    assert CHK.violations_axe2(_NONCORE, yaml)


def test_axe1_else_zero_multilignes_detecte():
    yaml = (
        "        {{ valeur\n"
        "           if frais\n"
        "           else 0 }}\n"
    )
    assert CHK.violations_axe1(_CORE, yaml)


# ---------------------------------------------------------------------------
# Commentaires : ne doivent jamais déclencher
# ---------------------------------------------------------------------------


def test_commentaire_yaml_non_capte():
    yaml = "        # exemple : states('x') | float(0) est interdit\n"
    assert not CHK.violations_axe1(_CORE, yaml)
    assert not CHK.violations_axe2(_NONCORE, yaml)


def test_commentaire_jinja_non_capte():
    yaml = "        {# states('sensor.ecs_temperature_ballon_securisee') | float(0) #}\n"
    assert not CHK.violations_axe2(_NONCORE, yaml)


# ---------------------------------------------------------------------------
# Preuve de détection (mutation) : retirer le motif rend la fixture verte
# ---------------------------------------------------------------------------


def test_mutation_retrait_motif_verdit_fixture(monkeypatch):
    yaml = "        {{ this.state | float(0) }}\n"
    assert CHK.violations_axe1(_CORE, yaml)  # détecté avec le motif
    sans_float0 = tuple(
        (pat, lbl) for pat, lbl in CHK.FABRICATION_PATTERNS if lbl != "float(0)"
    )
    monkeypatch.setattr(CHK, "FABRICATION_PATTERNS", sans_float0)
    assert not CHK.violations_axe1(_CORE, yaml)  # motif retiré → plus de détection


# ---------------------------------------------------------------------------
# Propriété pérenne sur le dépôt réel : zéro refabrication same-family
# ---------------------------------------------------------------------------


def test_depot_reel_zero_hit_same_family():
    """Après patch, aucun lecteur des deux capteurs sécurisés ne refabrique.

    Balaye les fichiers réels (pas une recherche du hit historique) et exige
    zéro violation d'axe 2 — la garantie que ``log/fin.yaml`` (et tout futur
    lecteur) n'introduit pas de fallback fabriqué.
    """
    hits: list[str] = []
    for d in CHK.AXIS2_DIRS:
        base = _ROOT / d
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.yaml")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if not any(s in text for s in CHK.SECURED_SENSORS):
                continue
            rel = str(path.relative_to(_ROOT))
            hits.extend(CHK.violations_axe2(rel, text))
    assert hits == [], f"refabrication same-family détectée : {hits}"


def test_depot_reel_fichiers_coeur_c24_propres():
    """Les 4 fichiers cœur C24 ne portent aucune fabrication numérique."""
    hits: list[str] = []
    for rel in CHK.CORE_C24_FILES:
        path = _ROOT / rel
        assert path.is_file(), rel
        hits.extend(CHK.violations_axe1(rel, path.read_text(encoding="utf-8")))
    assert hits == [], f"fabrication dans un fichier cœur C24 : {hits}"
