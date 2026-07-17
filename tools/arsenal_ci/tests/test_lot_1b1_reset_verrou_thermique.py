"""Lot 1B.1 (C24) — Durcissement de la condition thermique de ``reset_verrou_cycle``.

Deux niveaux de preuve :

1. **Modèle comportemental contractuel** — l'oracle
   ``arsenal_ci.behavior.reset_verrou_thermique`` applique I-SEC-5 : la libération
   thermique n'est autorisée que si température ET consigne sont numériques et
   satisfont les seuils ; tout opérande invalide ⇒ ``False``.
2. **Assertions structurelles sur le YAML runtime** — la condition de
   ``11_automations/ecs/reset_verrou_cycle.yaml`` n'emploie plus de fallback
   numérique et garde les deux opérandes ; les autres filets (déclencheur,
   verrou, déblocage zombie de ``cycle_session_open``) restent inchangés.

⚠️ Frontière de preuve assumée : **pas** une exécution du moteur de templates HA.
Preuve **contractuelle et structurelle automatisée**.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from arsenal_ci.behavior.reset_verrou_thermique import (
    SEUIL_CONSIGNE,
    SEUIL_TEMPERATURE,
    liberation_thermique_autorisee,
)

_ROOT = Path(__file__).resolve().parents[3]
RESET = _ROOT / "11_automations" / "ecs" / "reset_verrou_cycle.yaml"
SESSION_OPEN = _ROOT / "10_scripts" / "ecs" / "cycle_session_open.yaml"


def _text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _code(p: Path) -> str:
    """Contenu YAML hors commentaires ``#`` (l'en-tête cite volontairement float(0))."""
    return "\n".join(
        ligne for ligne in _text(p).splitlines() if not ligne.lstrip().startswith("#")
    )


# ---------------------------------------------------------------------------
# Niveau 1 — modèle comportemental (température)
# ---------------------------------------------------------------------------

_CONSIGNE_OK = 10  # ≤ seuil


def test_temp_valide_sous_seuil():
    assert liberation_thermique_autorisee(temperature=25.0, consigne=_CONSIGNE_OK) is True


def test_temp_valide_egale_seuil():
    # 30 < 30 est faux : le seuil température est strict.
    assert liberation_thermique_autorisee(temperature=SEUIL_TEMPERATURE, consigne=_CONSIGNE_OK) is False


def test_temp_valide_au_dessus_seuil():
    assert liberation_thermique_autorisee(temperature=45.0, consigne=_CONSIGNE_OK) is False


@pytest.mark.parametrize("temp", ["unknown", "unavailable", "", "n/a", None])
def test_temp_non_numerique_jamais_liberation(temp):
    assert liberation_thermique_autorisee(temperature=temp, consigne=_CONSIGNE_OK) is False


def test_temp_provenance_retenue_reste_evaluable():
    # Une température retenue est fournie comme simple valeur numérique : évaluable.
    # (Limite consignée C24 : réconciliation possible sur une mesure réelle non fraîche.)
    assert liberation_thermique_autorisee(temperature=25.0, consigne=_CONSIGNE_OK) is True
    assert liberation_thermique_autorisee(temperature=48.0, consigne=_CONSIGNE_OK) is False


# ---------------------------------------------------------------------------
# Niveau 1 — modèle comportemental (consigne)
# ---------------------------------------------------------------------------

_TEMP_OK = 25  # < seuil


@pytest.mark.parametrize("consigne", ["unknown", "unavailable", "", "n/a", None])
def test_consigne_non_numerique_jamais_liberation(consigne):
    assert liberation_thermique_autorisee(temperature=_TEMP_OK, consigne=consigne) is False


def test_consigne_valide_egale_seuil_inclus():
    # consigne == 10 : seuil INCLUS (10 <= 10).
    assert liberation_thermique_autorisee(temperature=_TEMP_OK, consigne=SEUIL_CONSIGNE) is True


def test_consigne_valide_superieure_seuil():
    assert liberation_thermique_autorisee(temperature=_TEMP_OK, consigne=11.0) is False


def test_deux_operandes_requis():
    # Aucun opérande seul ne suffit ; les deux doivent être numériques et conformes.
    assert liberation_thermique_autorisee(temperature=25.0, consigne=9.9) is True
    assert liberation_thermique_autorisee(temperature="unknown", consigne="unknown") is False


# ---------------------------------------------------------------------------
# Niveau 2 — assertions structurelles sur le YAML runtime
# ---------------------------------------------------------------------------


def test_yaml_aucun_fallback_numerique_dans_la_condition():
    code = _code(RESET)
    assert "float(0" not in code, "aucun float(0) dans la condition (I-SEC-2)"
    assert "int(0" not in code, "aucun int(0) dans la condition (I-SEC-2)"
    assert not re.search(r"get\([^)]*,\s*0\s*\)", code)
    assert not re.search(r"default\(\s*0\s*\)", code)


def test_yaml_garde_numerique_sur_les_deux_operandes():
    code = _code(RESET)
    # Une garde is_number pour la consigne ET pour la température.
    assert re.search(r"consigne\s*\|\s*is_number", code), "garde is_number consigne requise"
    assert re.search(r"t_cuve\s*\|\s*is_number", code), "garde is_number température requise"


def test_yaml_autres_filets_inchanges():
    txt = _text(RESET)
    # Déclencheur boot et garde de verrou conservés (comportement hors condition thermique).
    assert re.search(r"entity_id:\s*input_boolean\.systeme_stable", txt)
    assert re.search(r"to:\s*[\"']?on[\"']?", txt)
    assert re.search(r"entity_id:\s*input_boolean\.ecs_cycle_en_cours", txt)
    assert re.search(r"input_boolean\.turn_off", txt)


def test_filet_anti_zombie_independant_intact():
    # Le déblocage zombie (âge > 5 min) de cycle_session_open est indépendant de la
    # température et n'est PAS modifié : il reste le chemin de récupération si la
    # condition thermique s'abstient sous donnée inconnue.
    code = _code(SESSION_OPEN)
    assert "300" in code, "seuil zombie 5 min (300 s) attendu, inchangé"
    assert "ecs_cycle_en_cours" in code
