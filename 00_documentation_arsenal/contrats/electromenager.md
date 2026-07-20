# 🧠 ARSENAL — CONTRAT NORMATIF
## Électroménager — Détection de cycle et notification (lave-vaisselle, buanderie)

## 📌 Statut

**v1.0 — NORMATIF.** Ce contrat documente le runtime réel. En cas de divergence,
le comportement réel des automations prévaut ; les libellés et descriptions ne
font pas autorité. Aucune entité, aucun seuil et aucune règle ne sont inventés.

**Portée volontairement restreinte.** Ce contrat **n'est pas** un contrat
« électroménager » général. Il couvre **exclusivement** la détection de cycle et
la notification des **deux appareils réellement implémentés** : le lave-vaisselle
et la buanderie (lave-linge). Toute autre prise ou tout autre appareil est hors
périmètre tant qu'il n'est pas implémenté et documenté.

## 🎯 Rôle

Signaler, par appareil, qu'un **cycle est en cours**, à partir de la **puissance
mesurée par sa prise connectée**, et **notifier** l'utilisateur au début et à la
fin du cycle. C'est de l'**observabilité + notification pure** : aucun pilotage
d'appareil, aucune décision énergétique.

## 🧱 Sources de vérité (entités réelles)

| Appareil | Source de puissance | Flag de cycle |
|---|---|---|
| Lave-vaisselle | `sensor.prise_lave_vaisselle_power` | `input_boolean.lave_vaisselle_cycle` |
| Buanderie (lave-linge) | `sensor.prise_buanderie_power` | `input_boolean.buanderie_cycle` |

Automations (préfixe d'identifiant `1008` — registre `prefix_id.yaml`) :

| Appareil | Début | Fin |
|---|---|---|
| Lave-vaisselle | `10080000000001` | `10080000000002` |
| Buanderie | `10080000000003` | `10080000000004` |

Canal de notification mobile : `script.notification_envoyer` vers
`input_text.telephone_parent_1_notify`.

## 1. Détection de début

`mode: single`. Déclencheur : la puissance de la prise dépasse un seuil pendant
3 minutes. Condition : le flag de cycle est `off`. Action : `turn_on` du flag +
`persistent_notification.create` (l'`notification_id` reprend le nom du flag).

| Appareil | Seuil de début | Durée |
|---|---|---|
| Lave-vaisselle | puissance > **30 W** | `00:03:00` |
| Buanderie | puissance > **50 W** | `00:03:00` |

Les seuils sont **propres à chaque prise** (asymétrie assumée, cf. §6).

## 2. Détection de fin (avec fenêtre de confirmation)

`mode: restart`. Déclencheur : la puissance passe sous un seuil bas pendant une
durée prolongée. Condition : le flag de cycle est `on`. L'arrêt n'est **pas**
confirmé immédiatement : l'automation attend (`wait_for_trigger` +
`timeout`, `continue_on_timeout: true`) une éventuelle **reprise** de puissance.
- Si une reprise survient avant le délai → aucune fin n'est actée (le cycle
  continue).
- Si aucune reprise (`wait.trigger is none`) → fin confirmée : `dismiss` de la
  notification persistante + notification mobile + `turn_off` du flag.

| Appareil | Seuil bas | Durée bas | Seuil de reprise | Délai de confirmation |
|---|---|---|---|---|
| Lave-vaisselle | < **2 W** | `00:10:00` | > **5 W** | `00:05:00` |
| Buanderie | < **2 W** | `00:15:00` | > **30 W** | `00:05:00` |

## 3. Notifications

- **Début** : notification **persistante** (`persistent_notification.create`,
  `notification_id` = nom du flag).
- **Fin confirmée** : suppression de la notification persistante
  (`persistent_notification.dismiss`) **et** notification **mobile**
  (`script.notification_envoyer`, cible `input_text.telephone_parent_1_notify`).

La notification n'est qu'un effet ; elle ne porte aucune décision.

## 4. Écrivain souverain par flag

Chaque `input_boolean.*_cycle` possède **un et un seul** ensemble d'écrivains :
ses automations de début (`turn_on`) et de fin (`turn_off`) du **même appareil**.
Aucune autre autorité n'écrit ces flags ; ils ne sont consommés par aucun
dashboard ni aucune décision à ce jour.

## 5. Hors périmètre

- **Aucun pilotage d'appareil** (pas de coupure/relance de prise, pas de
  commande machine).
- **Aucun automatisme énergétique** (pas d'effacement, pas de pilotage tarifaire).
- **Aucun dashboard** consommateur des flags.
- **Pas de généralisation** à d'autres prises ou appareils : seuls le
  lave-vaisselle et la buanderie sont couverts.
- **Pas d'usage des mesures `energy` / `linkquality`** (`sensor.prise_*_energy`,
  `sensor.prise_*_linkquality`) comme source de détection de cycle — seule la
  **puissance instantanée** (`*_power`) est utilisée.

## 6. Dettes / observations

- **DETTE-EM-1 — Seuils asymétriques.** Les seuils de début, de bas et de reprise
  diffèrent entre appareils (lave-vaisselle 30 / 5 W, buanderie 50 / 30 W) ; ils
  sont calibrés par prise et non factorisés. Observation, pas anomalie.
- **OBS-EM-1 — Flags sans consommateur aval.** Les `*_cycle` ne servent
  aujourd'hui qu'à la notification ; aucun dashboard ni décision ne les lit.

## 🔗 Renvois

- Notifications mobiles : [`notifications.md`](notifications.md)
  (`script.notification_envoyer`).

## 🔒 Statut d'autorité

Contrat normatif opposable pour le périmètre déclaré (lave-vaisselle + buanderie).
Le runtime fait foi ; tout écart d'implémentation est une non-conformité, pas une
interprétation. L'ajout d'un nouvel appareil exige une extension explicite de ce
contrat (entités réelles, seuils réels), jamais une généralisation implicite.

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-06-07 | Création depuis le runtime réel. Documentation de la détection de cycle par puissance (début > seuil / 3 min ; fin < seuil bas / durée + fenêtre de confirmation anti-reprise), des flags `input_boolean.*_cycle`, des notifications persistante (début) et mobile (fin), et de l'écrivain souverain par flag, pour les deux appareils implémentés (lave-vaisselle `1008000000001/2`, buanderie `1008000000003/4`). Portée restreinte aux appareils réels ; aucun pilotage, aucun usage `energy`/`linkquality`. |
