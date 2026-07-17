"""Lot 1A (C24) — Sécurisation de ``sensor.ecs_temperature_ballon_securisee``.

Deux niveaux de preuve :

1. **Modèle comportemental contractuel** — l'oracle
   ``arsenal_ci.behavior.temperature_ballon_securisee`` applique les invariants
   I-SEC-1..5 aux dix scénarios obligatoires (+ cas de migration).
2. **Assertions structurelles sur le YAML runtime** — le producteur
   ``12_template_sensors/ecs/temperature.yaml`` ne réintroduit aucun fallback
   numérique, porte le déclencheur ``homeassistant start``, publie exactement les
   trois provenances, a retiré ``last_valid`` et n'a aucune garde ``availability``.

⚠️ Frontière de preuve assumée : ce n'est **pas** une exécution du moteur de
templates Home Assistant. En l'absence de moteur HA isolé, la preuve est
**contractuelle et structurelle automatisée**, pas un rendu Jinja réel. Le
comportement de restauration réel (redémarrage complet vs simple reload Template)
reste une limite documentée (voir ``test_limite_reload_vs_restart``).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from arsenal_ci.behavior.temperature_ballon_securisee import (
    ETAT_INCONNU,
    PROVENANCES,
    Resultat,
    est_numerique,
    evaluer,
)

_ROOT = Path(__file__).resolve().parents[3]
YAML = _ROOT / "12_template_sensors" / "ecs" / "temperature.yaml"


def _yaml_text() -> str:
    return YAML.read_text(encoding="utf-8")


def _yaml_code() -> str:
    """Contenu YAML **hors commentaires** (lignes ``#`` d'en-tête retirées).

    Un fallback interdit doit être cherché dans le code exécutable, jamais dans la
    prose documentaire de l'en-tête (qui cite volontairement ``float(0)``).
    """
    return "\n".join(
        ligne for ligne in _yaml_text().splitlines() if not ligne.lstrip().startswith("#")
    )


# ---------------------------------------------------------------------------
# Niveau 1 — modèle comportemental contractuel (10 scénarios + migrations)
# ---------------------------------------------------------------------------


def test_s1_source_invalide_aucun_etat_restaure():
    r = evaluer(source_valide=False, etat_restaure=None, provenance_restauree=None)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_s2_source_valide_premier_rendu():
    r = evaluer(source_valide=True, source_valeur=45.3)
    assert r == Resultat(etat=45.3, provenance="mesure")


def test_s3_source_invalide_ancienne_mesure_valide_restauree():
    r = evaluer(source_valide=False, etat_restaure=45.0, provenance_restauree="mesure")
    assert r == Resultat(etat=45.0, provenance="retenue")


def test_s4_source_invalide_ancien_unknown():
    r = evaluer(source_valide=False, etat_restaure="unknown", provenance_restauree="indisponible")
    assert r.etat == ETAT_INCONNU and r.provenance == "indisponible"


def test_s5_source_invalide_ancien_unavailable():
    r = evaluer(source_valide=False, etat_restaure="unavailable", provenance_restauree="indisponible")
    assert r.etat == ETAT_INCONNU and r.provenance == "indisponible"


def test_s6_source_invalide_ancien_zero_fabrique_sans_provenance():
    # Rejet structurel du 0.0 historique : numérique mais sans provenance.
    r = evaluer(source_valide=False, etat_restaure=0.0, provenance_restauree=None)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_s7_perte_source_apres_mesure_valide_en_session():
    # Après une mesure fraîche (provenance mesure) puis une perte : rétention.
    r = evaluer(source_valide=False, etat_restaure=52.1, provenance_restauree="mesure")
    assert r == Resultat(etat=52.1, provenance="retenue")
    # La rétention se chaîne (retenue -> retenue) tant que la source reste invalide.
    r2 = evaluer(source_valide=False, etat_restaure=52.1, provenance_restauree="retenue")
    assert r2 == Resultat(etat=52.1, provenance="retenue")


def test_s8_retour_source_nouvelle_valeur():
    # Le retour d'une mesure valide efface immédiatement la rétention.
    r = evaluer(source_valide=True, source_valeur=48.7, etat_restaure=52.1, provenance_restauree="retenue")
    assert r == Resultat(etat=48.7, provenance="mesure")


def test_s9_provenance_ensemble_ferme():
    assert PROVENANCES == ("mesure", "retenue", "indisponible")
    echantillons = [
        evaluer(source_valide=True, source_valeur=40.0),
        evaluer(source_valide=False, etat_restaure=40.0, provenance_restauree="mesure"),
        evaluer(source_valide=False, etat_restaure="unknown", provenance_restauree=None),
        evaluer(source_valide=False, etat_restaure=0.0, provenance_restauree=None),
    ]
    for r in echantillons:
        assert r.provenance in PROVENANCES
        assert r.provenance not in ("", "none", "None", None)


def test_s10_producteur_sans_fallback_numerique():
    # Miroir structurel — l'assertion complète est en niveau 2 (test_yaml_*).
    code = _yaml_code()
    assert "float(0" not in code
    assert "int(0" not in code


# --- cas de migration explicitement demandés -------------------------------


def test_migration_ancienne_valeur_reelle_sans_provenance_rejetee():
    # Première migration : une ancienne température réelle non nulle SANS provenance
    # est rejetée (retour à unknown). Coût accepté : ne jamais qualifier de réelle
    # une valeur historique non prouvable.
    r = evaluer(source_valide=False, etat_restaure=48.0, provenance_restauree=None)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


@pytest.mark.parametrize("prov", ["", "none", "None", "indisponible", "bogus", None])
def test_migration_provenance_vide_ou_invalide_rejetee(prov):
    r = evaluer(source_valide=False, etat_restaure=45.0, provenance_restauree=prov)
    assert r == Resultat(etat=ETAT_INCONNU, provenance="indisponible")


def test_est_numerique_rejette_sentinelles_et_booleens():
    for bon in (0.0, 0, 45.2, "45.2", "0"):
        assert est_numerique(bon) is True
    for mauvais in (None, True, False, "", "unknown", "unavailable", "none", "abc"):
        assert est_numerique(mauvais) is False


def test_limite_reload_vs_restart():
    """Limite documentée : un **redémarrage complet** HA émet ``homeassistant start``
    (réévaluation immédiate) ; un simple **reload des entités Template** ne l'émet
    pas nécessairement. Les déclencheurs source et ``systeme_stable`` restent alors
    le chemin de reconvergence. Non exécutable dans la suite isolée : vérifié
    structurellement (présence du déclencheur) au niveau 2.
    """
    assert True


# ---------------------------------------------------------------------------
# Niveau 2 — assertions structurelles sur le YAML runtime
# ---------------------------------------------------------------------------


def test_yaml_aucun_fallback_numerique():
    code = _yaml_code()
    assert "float(0" not in code, "fallback float(0) interdit (I-SEC-2)"
    assert "int(0" not in code, "fallback int(0) interdit (I-SEC-2)"
    # Aucun défaut numérique équivalent via get(..., 0) / default(0).
    assert not re.search(r"get\([^)]*,\s*0\s*\)", code), "get(..., 0) interdit"
    assert not re.search(r"default\(\s*0\s*\)", code), "default(0) interdit"


def test_yaml_declencheur_homeassistant_start_present():
    txt = _yaml_text()
    assert re.search(r"platform:\s*homeassistant", txt), "déclencheur homeassistant requis"
    assert re.search(r"event:\s*start", txt), "event: start requis"


def test_yaml_provenance_trois_valeurs_seulement():
    txt = _yaml_text()
    for jeton in ("mesure", "retenue", "indisponible"):
        assert jeton in txt, f"provenance '{jeton}' attendue"
    # Aucune provenance vide / None publiée.
    assert "provenance: ''" not in txt
    assert not re.search(r"provenance:\s*None", txt)


def test_yaml_last_valid_supprime():
    assert "last_valid" not in _yaml_text(), "l'attribut interne last_valid doit être retiré"


def test_yaml_aucune_garde_availability():
    assert not re.search(r"^\s*availability:", _yaml_text(), re.MULTILINE), (
        "aucune garde availability (l'absence = state unknown + provenance indisponible)"
    )
