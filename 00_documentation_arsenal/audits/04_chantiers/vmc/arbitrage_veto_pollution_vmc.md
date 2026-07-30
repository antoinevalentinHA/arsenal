# Arbitrage — Veto pollution sur la haute vitesse VMC

| Champ | Valeur |
|---|---|
| **Domaine** | VMC — composition exécutoire (§16.2) |
| **Nature** | Trace d'**arbitrage propriétaire**. Aucun runtime, helper, UI, Recorder ni `entity_id` figé |
| **Déclencheur** | Installation de l'intégration `atmofrance` — voir [`../../01_rapports/perception_externe/analyse_impact_integration_atmofrance.md`](../../01_rapports/perception_externe/analyse_impact_integration_atmofrance.md) |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.7** — §16.2 (amendé) + §17 (nouveau) |

## Contexte

VMC simple flux **sans filtration** (contrat §1.4) : la haute vitesse importe
davantage d'air extérieur. En épisode de pollution particulaire (p. ex. incendies
de proximité), cet import est indésirable. Besoin volontairement **simple** : un
veto en aval, sans requalifier les voies ni auditer leur efficacité.

## Décision

- En **régime automatique**, `haute vitesse commandée = requise ET NON veto`.
- **Veto actif** si l'indice **PM10 courant** ou **PM2.5 courant** ∈ **{4, 5, 6, 7}**
  (« Mauvais » ou pire ; `7 — Évènement` inclus). Seuil unique, **sans hystérésis**.
- La VMC reste en **basse vitesse** (ventilation permanente préservée).
- En **régime manuel**, l'humain reprend l'autorité (§16.1) : sa consigne
  **surpasse le veto**.
- Donnée non exploitable (`0`, `unknown`, `unavailable`, non numérique) →
  **aucun veto déduit**, indisponibilité **exposée** (« absence de preuve », jamais
  « air bon »).

## Portée

- Le veto agit **uniquement** à la composition exécutoire (§16.2).
- `binary_sensor.vmc_haute_vitesse_requise` (§3.1) et les voies (§5, §6) restent
  **strictement inchangées**.
- Vérification de la source (code `atmofrance` v2.1.2) : échelle ATMO `0–7`, state
  = entier ; **`0` est double** (« Indisponible » **et** valeur forcée en cas
  d'échec API) → traité comme non exploitable.

## Contreparties assumées

- Pendant un veto, un besoin **CO₂ ou humidité** actif n'est **pas servi** par la
  haute vitesse ; le niveau intérieur peut monter. Levier résiduel : prise de main
  manuelle.
- Sur **panne durable** de la donnée PM en épisode réel, le veto ne s'applique pas
  et la haute vitesse peut reprendre. Assumé à ce stade.
- Indice **communal** (non mesuré au logement) : représentativité locale limitée.

## Exclusions

Hystérésis, conservation temporisée, garde de panne durable, entités **J+1**,
**indice global** comme autorité, filtration matérielle, veto pollution de
l'aération naturelle (domaine distinct), et tout **runtime** (implémentation = lot
ultérieur). Les `entity_id` seront **préattribués avant runtime**.
