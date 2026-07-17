"""Oracle contractuel — gardes de fraîcheur thermique de l'orchestrateur ECS.

Modèle indépendant des prédicats de ``10_scripts/ecs/cycle.yaml`` (script
``chauffage_ecs_cycle``), dérivé de :

- **I-SEC-5** et §8.2/§8.3 du contrat
  ``contrats/ecs/sensor_ecs_temperature_ballon_securisee.md`` : une température
  inconnue ne constitue jamais une décision thermique positive ; aucun fallback
  numérique ;
- ``contrats/ecs/ecs_pipeline_global_cycle.md`` §4.5 : le boost 2 répond à une
  **non-atteinte** de la cible — établissable uniquement sur une mesure réelle.

Règle de fraîcheur commune :

    fraîche  ⟺  état numérique  ∧  provenance == "mesure"

Une valeur ``retenue`` (numérique mais non fraîche), ``indisponible``, ``unknown``,
``unavailable`` ou non numérique n'est **jamais** fraîche : elle ne peut ni fonder
``start_temp``, ni prouver l'atteinte, ni prouver la non-atteinte (boost 2), ni
autoriser le boost 1.

Ce module n'est PAS une transcription du Jinja : il exprime les prédicats
contractuels à partir d'entrées abstraites (état, provenance, cible, epsilon,
verdict de signature). Ce n'est pas une exécution du moteur de templates Home
Assistant : la preuve associée est **contractuelle et structurelle**, pas un
rendu Jinja réel.
"""

from __future__ import annotations

from arsenal_ci.behavior.temperature_ballon_securisee import est_numerique

#: Seul verdict de signature autorisant l'examen d'un boost 1 (les autres —
#: notamment ``indeterminee`` — l'interdisent, la signature restant l'autorité).
SIGNATURE_BOOST1 = "insuffisante"

#: Distance résiduelle minimale à la cible pour un boost 1 (constante contractuelle).
DISTANCE_BOOST1 = 1.0


def temperature_fraiche(state, provenance) -> bool:
    """Vraie ssi la donnée est une mesure réelle actuelle (numérique + provenance
    ``mesure``). ``retenue``/``indisponible``/non numérique ⇒ Faux."""
    return est_numerique(state) and provenance == "mesure"


def start_temp_admissible(state, provenance) -> bool:
    """``start_temp`` n'est capturable que sur une mesure fraîche (le calcul du
    delta, du bucket, de ``min_target`` et de la consigne en dépend)."""
    return temperature_fraiche(state, provenance)


def atteinte_cible(state, provenance, target, epsilon) -> bool:
    """Atteinte prouvée uniquement par une mesure fraîche ≥ ``target - epsilon``."""
    if not temperature_fraiche(state, provenance):
        return False
    return float(state) >= float(target) - float(epsilon)


def boost2_autorise(state, provenance, target, epsilon) -> bool:
    """Boost 2 autorisé uniquement sur preuve fraîche de non-atteinte
    (``state < target - epsilon``). La non-observation ne vaut pas non-atteinte."""
    if not temperature_fraiche(state, provenance):
        return False
    return float(state) < float(target) - float(epsilon)


def boost1_autorise(signature, state, provenance, target) -> bool:
    """Boost 1 : signature ``insuffisante`` (autorité) ET mesure fraîche à distance
    résiduelle ≥ ``DISTANCE_BOOST1``. Aucun boost sur signature autre, température
    inconnue ou retenue."""
    if signature != SIGNATURE_BOOST1:
        return False
    if not temperature_fraiche(state, provenance):
        return False
    return (float(target) - float(state)) >= DISTANCE_BOOST1
