# CONTRAT ARSENAL — CLIMATISATION
## 07 — Exécution — Application idempotente

**Version contrat :** v1.3

---

## Rôle

- Lire exclusivement la décision canonique (`sensor.clim_target_mode`)
- Émettre les commandes nécessaires pour amener l'état réel du système climatique en conformité avec la décision canonique
- Constater le résultat via post-condition et programmer une reprise différée en cas d'échec

---

## Entrées d'exécution

| Entité | Rôle |
|---|---|
| `sensor.clim_target_mode` | Mode cible — autorité décisionnelle unique |
| `sensor.consigne_clim_appliquee` | Consigne température appliquée selon présence *(non intégré en v1.3)* |
| `binary_sensor.clim_silencieux_autorise` | Mode silencieux — plage horaire et présence *(non intégré en v1.3)* |

Ces entrées sont lues, jamais produites par la couche Exécution.

---

## Helpers de résilience

| Entité | Rôle |
|---|---|
| `input_boolean.clim_execution_echec` | Matérialise un échec d'exécution en cours |
| `counter.clim_execution_retry_count` | Compte les échecs consécutifs |
| `timer.clim_retry` | Ordonne la reprise différée |

Ces helpers portent la mémoire de résilience. Ils ne prennent aucune décision thermique.

---

## Garanties

- N'embarque aucune logique métier
- N'effectue aucun arbitrage
- N'envoie aucune commande redondante au sein d'une même exécution
- Ne peut ni modifier ni requalifier la décision canonique
- Ne corrige jamais une décision
- N'effectue aucun retry immédiat ni boucle interne — toute ré-émission est strictement différée, bornée et pilotée par des mécanismes externes (timer + compteur)
- Ne conserve aucune mémoire locale interne au script — la mémoire de résilience est externalisée via des helpers dédiés
- Les scripts physiques (`clim_exec_apply_cool`, `clim_exec_apply_dry`,
  `clim_exec_apply_heat`) appliquent une garde de stabilisation après
  allumage physique avant émission d'une commande HVAC.
- Toute vérification d'état HVAC après allumage doit reposer sur une
  lecture fraîche de `climate.clim`, postérieure à la stabilisation.

---

## Conditions de non-émission

Aucune commande n'est envoyée si :
- la cible est hors contrat (`cool`, `dry`, `heat`, `off` sont les seules valeurs acceptées),
- l'état courant est déjà conforme à la cible (idempotence — chaque commande est précédée d'une vérification de l'état courant).

Si les entités d'exécution (`climate.clim`, `switch.clim_power`) sont `unknown` ou `unavailable` au moment de l'appel :
- aucune commande n'est émise,
- ce cas n'est pas une abstention neutre,
- il est qualifié comme un échec infra et déclenche la reprise différée.

---

## Résilience d'exécution

La couche Exécution est tolérante aux indisponibilités temporaires du système (ex : perte Wi-Fi du module climatisation).

En cas d'échec d'application, trois conclusions sont distinguées :

| Conclusion | Cause | Traitement |
|---|---|---|
| Abstention silencieuse | Cible hors contrat | Aucun marquage, aucune reprise |
| Échec infra | Entités indisponibles au moment de l'appel | Marquage + reprise différée |
| Échec post-condition | Commande émise mais état cible non atteint | Marquage + reprise différée |

La ré-émission en cas d'échec :
- est différée (pas de retry immédiat) : +30 s au premier échec, +90 s au deuxième
- est strictement bornée à deux reprises après la tentative initiale
- s'arrête en cas d'échec persistant avec émission d'une notification persistante

La couche Exécution reste pure : elle applique, constate et délègue la reprise. Elle ne décide pas de la stratégie thermique.

Les post-conditions ne sont pas évaluées immédiatement après émission
des commandes physiques. Une garde de stabilisation explicite est
appliquée avant qualification du résultat afin de tenir compte des
latences de propagation des intégrations climatisation.

---

## Automation de reprise

| Entité | Rôle |
|---|---|
| `automation.clim_reprise_apres_erreur` | Relance `script.clim_execution` à l'expiration de `timer.clim_retry` |

Conditions de relance :
- `input_boolean.clim_execution_echec` est `on`
- `sensor.clim_target_mode` est dans `['cool', 'dry', 'heat', 'off']`
- `counter.clim_execution_retry_count` ≤ 2

---

## Script d'exécution

| Entité | Rôle |
|---|---|
| `script.clim_execution` | Exécuteur principal — tentative unique, post-condition, conclusion |
