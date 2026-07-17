"""Oracle contractuel — condition thermique de libération du verrou ECS.

Modèle indépendant du prédicat évalué par ``11_automations/ecs/reset_verrou_cycle.yaml``
(automation ``10250000000022`` « ECS - Gardien verrou »), dérivé de l'invariant
**I-SEC-5** du contrat ``contrats/ecs/sensor_ecs_temperature_ballon_securisee.md``
(§8.3) et de ``contrats/parametres_invalides.md`` (aucun fallback numérique).

Règle contractuelle :

    libération thermique autorisée
      ⟺  température numérique  ∧  consigne numérique
         ∧  consigne <= SEUIL_CONSIGNE  ∧  température < SEUIL_TEMPERATURE

Toute grandeur non numérique (``unknown`` / ``unavailable`` / ``""`` /
non convertible) rend la condition **indéterminée** ⇒ ``False`` : une donnée
inconnue ne peut jamais autoriser la libération, et n'est jamais convertie en
faux « froid ».

Ce module n'est PAS une transcription du Jinja : il exprime le prédicat
contractuel à partir d'entrées abstraites. Ce n'est pas une exécution du moteur
de templates Home Assistant (preuve **contractuelle et structurelle**, pas un
rendu Jinja réel).

Portée : ce prédicat ne décide que de la **branche thermique**. Les autres filets
de récupération du verrou (déblocage zombie de ``ecs_cycle_session_open`` sur âge,
watchdog) sont **indépendants** et hors de ce modèle.
"""

from __future__ import annotations

from arsenal_ci.behavior.temperature_ballon_securisee import est_numerique

#: Seuils contractuels hérités du runtime (non réintroduits ailleurs).
SEUIL_CONSIGNE = 10.0
SEUIL_TEMPERATURE = 30.0


def liberation_thermique_autorisee(
    *,
    temperature,
    consigne,
    seuil_consigne: float = SEUIL_CONSIGNE,
    seuil_temperature: float = SEUIL_TEMPERATURE,
) -> bool:
    """Vrai ssi les DEUX opérandes sont numériques et satisfont les seuils.

    ``temperature`` et ``consigne`` sont des grandeurs abstraites : nombre réel,
    chaîne numérique, ou marqueur non numérique (``"unknown"``/``"unavailable"``/
    ``""``/``None``…). Une température ``provenance: retenue`` est fournie ici comme
    une simple valeur numérique (le contrat du verrou n'exige pas de fraîcheur).
    """
    # I-SEC-5 : indéterminé dès qu'un opérande n'est pas une grandeur numérique.
    if not (est_numerique(temperature) and est_numerique(consigne)):
        return False
    return float(consigne) <= seuil_consigne and float(temperature) < seuil_temperature
