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
| `sensor.consigne_clim_appliquee` | Consigne dérivée selon présence (COOL) |
| `input_number.consigne_heat_clim` | Consigne HEAT envoyée à `climate.clim` |
| `binary_sensor.clim_silencieux_autorise` | Mode silencieux — plage horaire et présence |

Ces entrées sont lues, jamais produites par la couche Exécution.

L'application de la consigne HEAT est portée par une automation dédiée
(`automation.clim_application_consigne_heat`) qui réagit à un changement
du slider ou à l'entrée effective en mode HEAT, sans jamais forcer le
mode ni l'allumage.

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

## Réarmement après récupération

La reprise différée est **volontairement bornée** (au plus deux reprises après
la tentative initiale). Une fois la borne atteinte pendant une indisponibilité
prolongée de l'infrastructure, plus aucun filet ne relance l'exécution : la
reprise est neutralisée (`counter > 2`), le watchdog ne se déclenche que sur le
**front** d'incohérence (déjà consommé), et le transit attend un **changement**
de décision. L'exécution peut alors rester en état « échec latché » alors même
que l'infrastructure Airstage a récupéré et que la décision réclame toujours
une action.

Une automation de réarmement lève cet angle mort :

| Entité | Rôle |
|---|---|
| `automation.clim_rearmement_apres_recuperation` | Réarme le budget de reprise et relance `script.clim_execution` sur un **front de récupération** de l'infrastructure |

Déclenchement — **fronts de récupération uniquement** (jamais en continu) :
- retour de disponibilité d'une entité d'exécution (`climate.clim` ou
  `switch.clim_power` quittant `unavailable`/`unknown`, stabilisé 15 s), ou
- `binary_sensor.retour_ok_airstage` passe `on` (reload Airstage abouti).

Conditions de réarmement :
- `input_boolean.clim_execution_echec` est `on`
- `sensor.clim_target_mode` est dans `['cool', 'dry', 'heat', 'off']`
- `input_boolean.systeme_stable` est `on` et `binary_sensor.panne_secteur_en_cours` est `off`
- `climate.clim` et `switch.clim_power` sont réellement disponibles

Action : `counter.reset` puis relance unique de `script.clim_execution`. La
post-condition du script re-borne aussitôt la reprise. Le réarmement reste donc
**strictement borné** (au plus trois tentatives par front de récupération),
sans polling ni matraquage de l'actionneur.

Garantie de non-régression : un device **disponible mais qui refuse
durablement** la commande (échec post-condition sans indisponibilité) ne
produit aucun front de récupération — il **n'est pas** réarmé, et la borne
d'origine tient. Seule une récupération d'infrastructure ré-ouvre un budget.

---

## Script d'exécution

| Entité | Rôle |
|---|---|
| `script.clim_execution` | Exécuteur principal — tentative unique, post-condition, conclusion |
