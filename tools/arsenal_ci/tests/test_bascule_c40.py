"""C40 (bascule) — R-CALL-DESHUM : numerus clausus de l'ecrivain + anti-routage.

Statut epistemique : CONTROLES (lecture seule du runtime reel) + META-TEST de
gouvernance, analogues au lot 3.2 de CH-4 mais pour le domaine deshumidificateur.

  1. CONTROLE runtime : seuls {application, retry_on, retry_off} invoquent
     `script.set_deshumidificateur_state` ; aucun routage deshum via
     `script.bot_transaction_execute`.
  2. PAS de divergence inverse (un appelant contractualise sans site d'appel).
  3. META-TEST : la constante `APPELANTS_AUTORISES` == l'allow-list NORMATIVE du
     contrat (bloc sentinelle). Un rouge = derive contrat <-> code.
"""
from arsenal_ci.execution import r_call_deshum
from arsenal_ci.rules.policy import Severity


# --------------------------------------------------------- 1. controle runtime

def test_numerus_clausus_conforme():
    bloquants = [
        v for v in r_call_deshum.analyser() if v.severity is Severity.BLOCKING
    ]
    assert bloquants == [], (
        "Appelant(s) non autorise(s) / routage deshum interdit detecte(s) : "
        + ", ".join(f"{v.source}->{v.target}" for v in bloquants)
    )


def test_pas_de_divergence_inverse():
    warnings = [
        v for v in r_call_deshum.analyser() if v.severity is Severity.WARNING
    ]
    assert warnings == [], (
        "Appelant(s) contractualise(s) sans site d'appel : "
        + ", ".join(v.source for v in warnings)
    )


# ----------------------------------------------------- 2. meta-test contrat

def test_allowlist_constante_egale_contrat():
    assert r_call_deshum.lire_allowlist_contrat() == r_call_deshum.APPELANTS_AUTORISES


def test_allowlist_contient_les_trois_appelants():
    assert r_call_deshum.APPELANTS_AUTORISES == frozenset(
        {
            "11_automations/deshumidificateur/application.yaml",
            "11_automations/deshumidificateur/retry_on.yaml",
            "11_automations/deshumidificateur/retry_off.yaml",
        }
    )


# ------------------------------ 3. appel direct switch.deshumidificateur (I1, C40)

def test_appel_direct_switch_deshum_reserve_a_l_ecrivain():
    """Le seul site legitime d'appel direct a switch.deshumidificateur est
    l'ecrivain unique (forcer_etat.yaml). Toute autre occurrence = BLOCKING."""
    directs = [
        v for v in r_call_deshum.analyser()
        if v.severity is Severity.BLOCKING and v.target == r_call_deshum.ENTITE_PHYSIQUE
    ]
    assert directs == [], (
        "Appel direct interdit a switch.deshumidificateur hors ecrivain unique : "
        + ", ".join(v.source for v in directs)
    )


def test_ecrivain_physique_est_bien_l_ecrivain_unique():
    assert (
        r_call_deshum.ECRIVAIN_PHYSIQUE_FICHIER
        == "10_scripts/deshumidificateur/forcer_etat.yaml"
    )
