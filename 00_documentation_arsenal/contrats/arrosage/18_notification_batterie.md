# CONTRAT ARSENAL — ARROSAGE
## 18 — Notification mobile batterie faible Rain Bird

**Version contrat :** v0.2
**Statut :** **Normatif — runtime livré.** Ce document spécifie la notification
mobile « batterie faible / critique » du contrôleur Rain Bird ESP-BAT-BT2 et fixe
ses paramètres. **Runtime livré** : automation `10270000000004`
([`batterie_faible_notification.yaml`](../../../../11_automations/arrosage/batterie_faible_notification.yaml)).
Il **ne crée aucun** template sensor, helper, script ni élément d'UI : la détection
de franchissement est portée **en ligne** par l'automation.

> **Position dans le socle.** Ce contrat **dérive** de la classification des entités
> du pont ([`09_classification_entites.md`](09_classification_entites.md) §4 :
> `battery_level` / `battery_voltage` en classe **Observation**, lecture seule) et
> **réutilise** la doctrine transverse de fraîcheur/disponibilité
> ([`resilience_integrations.md`](../resilience_integrations.md)) et de notifications
> ([`notifications.md`](../notifications.md)). Il **reprend le modèle corrigé** de la
> notification batterie ScanWatch (garde sur `trigger.from_state` pour éliminer les
> faux positifs au reload/restart).

> **Garde-fou de lecture.** La batterie est une **observation de santé
> d'alimentation**, jamais une entrée de décision d'arrosage. Une batterie faible
> **n'autorise, ne déclenche ni ne bloque** aucun arrosage ([`01_metier.md`](01_metier.md)
> §4, [`09`](09_classification_entites.md) §6). Ce contrat ne produit qu'une
> **notification informative**.

---

## Objet

Définir, **avant tout runtime**, l'architecture contractuelle d'une **notification
mobile informative** signalant que la batterie du contrôleur Rain Bird franchit un
**seuil bas réel**. La notification doit :

- signaler le **franchissement réel** vers l'état faible (événement) ;
- **ne jamais** se déclencher sur un reload de templates, un redémarrage Home
  Assistant, ou une transition depuis un état non numérique
  (`unknown`/`unavailable`/`none`/chaîne vide) ;
- **ne pas** se répéter tant que la batterie reste faible ;
- **ne pas** produire de diagnostic trompeur lorsque le pont Rain Bird est
  indisponible.

---

## Périmètre

- **Détection de franchissement** : portée **en ligne** par l'automation
  `10270000000004` (gardes numériques + logique de seuils dans les conditions),
  **sans capteur dérivé** dans ce lot. Un capteur d'interprétation reste une
  **option future** (cf. § Entités dérivées prévues).
- **Couche notification mobile** : l'automation, événementielle, délègue l'envoi au
  canal central `script.notification_envoyer`.
- **Destinataire** : `input_text.telephone_parent_1_notify` (canal déjà utilisé par
  les notifications santé et arrosage existantes).

> Les deux couches sont **séparées** (décision/diagnostic ≠ notification), conformément
> à la doctrine Arsenal. Aucune couche n'écrit sur le matériel ni ne décide d'un
> arrosage.

---

## Hors périmètre

- ❌ Toute **action métier d'arrosage** liée à la batterie (run/stop/rain_delay/régime).
- ❌ Toute **commande native** Rain Bird, tout pilotage du pont.
- ❌ Toute **notification persistante** : l'état « batterie faible » n'est pas restitué
  comme état durable ici ; seul le **franchissement** (événement) est notifié, ce qui
  relève du **canal mobile** ([`notifications.md`](../notifications.md) §« Événements
  opérationnels → canal mobile »).
- ❌ Toute **modification de l'entité source** ou de sa customisation.
- ❌ Tout **runtime** (template, helper, script, automation) : ce lot est documentaire.

---

## Entités sources

Entités **réellement exposées** par le pont (relevé [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md),
classées **Observation** en [`09`](09_classification_entites.md) §4) :

| `entity_id` | Nature | Rôle dans ce contrat |
|---|---|---|
| `sensor.rain_bird_bat_bt_2_e9a3_battery_level` | **Pourcentage numérique** (%) | **Source principale** du franchissement de seuil |
| `sensor.rain_bird_bat_bt_2_e9a3_battery_voltage` | **Tension** (V) | **Source secondaire / diagnostic** (corroboration, non déclenchante par défaut) |

Disponibilité du pont (déjà utilisée par l'automation `10270000000001`,
[`pont_indisponible_notification.yaml`](../../../../11_automations/arrosage/pont_indisponible_notification.yaml)) :

| `entity_id` | Rôle |
|---|---|
| `binary_sensor.rain_bird_pont_donnees_disponibles` | Garde de **disponibilité** : pas de diagnostic batterie si le pont ne remonte plus de données exploitables |

> **Aucune** de ces entités n'est créée par Arsenal : ce sont des surfaces du pont,
> en lecture seule.

---

## Entités dérivées prévues

Le runtime V1 **ne crée aucun capteur dérivé** : la détection est inline dans
l'automation. Les capteurs ci-dessous restent des **options futures** (noms
**conceptuels**, non figés), p. ex. si une projection UI de l'état devenait utile :

- `‹rain_bird_batterie_faible›` — capteur d'interprétation booléen (template), vrai
  lorsque `battery_level` est numérique **et** sous le seuil faible, faux sinon ;
  rejette `unknown`/`unavailable`/`none`/chaîne vide ; déterministe et recalculable.
- `‹rain_bird_batterie_critique›` — second niveau (seuil critique).

> Aucun de ces capteurs n'est créé dans ce lot ; leur éventuelle ratification en
> `entity_id` réel relèverait d'un lot ultérieur ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)).

---

## Seuils et paramètres retenus

Paramètres **validés** (opérateur) et matérialisés dans l'automation
`10270000000004` :

| Paramètre | Description | Valeur retenue |
|---|---|---|
| `seuil_faible` | Bande faible sur `battery_level` (%) | **`10 < niveau <= 20`** |
| `seuil_critique` | Bande critique sur `battery_level` (%) | **`niveau <= 10`** (prioritaire) |
| `duree_stabilisation` | `for:` avant déclenchement | **non retenue** |
| `seuil_retour` | Hystérésis de retour à la normale | **sans objet** (retour normal non retenu) |
| `destinataire` | Cible mobile | `input_text.telephone_parent_1_notify` |
| `emoji_titre` | Emoji de domaine du titre | `🔋` |
| `id_automation` | ID de l'automation runtime | **`10270000000004`** |

> Les seuils sont matérialisés **explicitement** dans les conditions de l'automation
> (comparaisons `> 10` / `<= 10` / `> 20` / `<= 20`), sans constante implicite.

---

## Déclencheurs autorisés

Modèle retenu : **trigger `state`** sur `sensor.rain_bird_bat_bt_2_e9a3_battery_level`,
gardé par des conditions de transition numérique (réutilise le modèle ScanWatch
corrigé).

- **`platform: state`** sur le capteur batterie (sans `to:`), pour observer **toute**
  transition de niveau.
  - **Pourquoi pas `numeric_state below`** : un `numeric_state below: 20` ne se
    déclenche qu'à l'**entrée** dans la plage `< 20` ; il **manquerait** un
    franchissement critique partant d'une valeur **déjà** sous 20 (ex. `19 → 9`).
    Le trigger `state` + comparaisons `from`/`to` couvre ce cas et les seuils `<=`.
- **Gardes obligatoires** (conditions) :
  - **disponibilité** : `binary_sensor.rain_bird_pont_donnees_disponibles == 'on'` ;
  - **`from_state` ET `to_state` présents et numériques** (`is_number`), ce qui exclut
    `unknown`/`unavailable`/`none`/chaîne vide/non numérique et l'absence d'état.
- **Logique de franchissement** (dans un `choose`, **critique prioritaire**) :
  - **Critique** : `old > 10` **et** `new <= 10` ;
  - **Faible** : `old > 20` **et** `10 < new <= 20`.
  - L'exigence `old > seuil` garantit un franchissement **depuis une valeur non basse**
    (anti-reload/anti-restart et anti-répétition), et `choose` n'émet qu'**une** branche
    (chute directe `25 → 9` ⇒ **critique seul**).
- **Pas de `for:`** (aucune stabilisation) et **pas de notification de retour à la
  normale** (aucune branche `else`).

---

## Déclencheurs interdits

- ❌ Trigger `state … to: 'on'`/`to: 'low'` **sans contrôle de transition** (anti-pattern
  ScanWatch d'origine).
- ❌ Trigger qui reste vrai après reload (template booléen utilisé directement comme
  déclencheur sans garde `from_state`).
- ❌ Déclenchement lorsque `trigger.from_state` vaut `unknown`, `unavailable`, `none`,
  chaîne vide, ou **toute valeur non numérique**.
- ❌ Déclenchement sur `battery_voltage` seul (source diagnostic, non déclenchante par
  défaut).
- ❌ Tout déclencheur produisant une notification au **reload de templates** ou au
  **redémarrage** alors que la batterie était déjà faible avant.

---

## Conditions anti-spam / anti-reload

1. **Anti-reload / anti-restart** : la garde `is_number` sur `from_state` **et**
   `to_state` bloque toute transition issue d'un état non numérique. Au reload/restart,
   l'entité passe par `unavailable`/`unknown` → garde fausse → **aucune notification**.
2. **Anti-répétition** : chaque branche exige `old > seuil` (franchissement depuis une
   valeur non basse) ; tant que la batterie **reste** basse (décrue continue), `old`
   n'est plus au-dessus du seuil → **aucune répétition**. La bande faible ne re-notifie
   qu'après un retour réel `> 20`. `mode: single` complète la garde.
3. **Garde de disponibilité du pont** : si `binary_sensor.rain_bird_pont_donnees_disponibles`
   est `off` (pont muet), la lecture batterie est **non exploitable** ; la notification
   ne doit pas être émise sur une valeur potentiellement périmée (diagnostic trompeur).
4. **Retour à la normale** : **non retenu par défaut**. S'il est retenu ultérieurement,
   il devra utiliser une **hystérésis** (`seuil_retour > seuil_faible`) pour éviter le
   battement autour du seuil, et rester un **événement** mobile distinct.

---

## Notifications mobiles

- **Canal** : `script.notification_envoyer` (canal central Arsenal), **jamais** un
  appel `notify.*` direct.
- **Nature** : **événement** (franchissement) → **canal mobile** autorisé
  ([`notifications.md`](../notifications.md)). Ce n'est **pas** une projection d'état
  durable (pas de persistant ici).
- **Titre** : doit commencer par un **emoji de domaine** (règle emoji obligatoire du
  contrat Notifications), p. ex. `🔋 Arrosage – batterie Rain Bird faible`
  (emoji à arbitrer, cf. § Seuils et paramètres).
- **Message** : informatif, sans référence temporelle ni confirmation d'action ;
  décrit la situation (« batterie du contrôleur Rain Bird sous le seuil bas »).
- **Destinataire** : `input_text.telephone_parent_1_notify`.

---

## Critères d'acceptation runtime futur

Le lot runtime, lorsqu'il sera ouvert, devra démontrer :

1. **ID d'automation fourni par Parent 1** — **aucun ID inventé**. Le runtime n'est pas
   créé tant que l'ID n'est pas explicitement attribué.
2. **Reload templates / redémarrage HA** : aucune notification émise, même si la
   batterie était déjà faible avant (garde `from_state` numérique ≥ seuil).
3. **Franchissement réel** : une notification émise lorsque `battery_level` passe d'une
   valeur numérique ≥ seuil à une valeur < seuil.
4. **Pas de répétition** tant que la batterie reste sous le seuil.
5. **Pont indisponible** : aucune notification batterie sur lecture non exploitable.
6. **Aucune action d'arrosage** déclenchée, bloquée ou autorisée par la batterie.
7. **Conformité** des checkers `check_notifications_contracts.py` (titre emoji) et des
   gates docs/contrats applicables.
8. **Aucune valeur de seuil implicite** : seuils matérialisés explicitement.

---

## Renvois

- Classification des entités du pont (Observation) : [`09_classification_entites.md`](09_classification_entites.md)
- Relevé runtime du pont : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Fraîcheur / disponibilité / reprise : [`resilience_integrations.md`](../resilience_integrations.md)
- Doctrine notifications (emoji, état vs événement) : [`notifications.md`](../notifications.md)
- Notification de disponibilité du pont (modèle, ID `10270000000001`) :
  [`pont_indisponible_notification.yaml`](../../../../11_automations/arrosage/pont_indisponible_notification.yaml)
- Domaine batteries des capteurs (réf. seuil non contraignante) : [`batteries.md`](../batteries.md)
- Index du domaine : [`README.md`](README.md)

---

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 0.1 | 2026-06-29 | Création du contrat (spécification, **aucun runtime**). Architecture en deux couches (diagnostic d'interprétation + notification mobile), sources `battery_level` (principale, %) / `battery_voltage` (diagnostic), déclencheur futur `numeric_state below` avec garde `from_state` numérique ≥ seuil, exclusions `unknown`/`unavailable`/`none`/non numérique, anti-reload/anti-restart et anti-répétition, garde de disponibilité du pont, retour à la normale non retenu par défaut. Seuils laissés en paramètres à arbitrer ; ID d'automation runtime à fournir par Parent 1. |
| 0.2 | 2026-06-29 | **Runtime livré** : automation `10270000000004` ([`batterie_faible_notification.yaml`](../../../../11_automations/arrosage/batterie_faible_notification.yaml)). Paramètres figés : faible `10 < niveau <= 20`, critique `niveau <= 10` (prioritaire), retour normal **non retenu**, `for:` **non retenu**, emoji `🔋`. Mécanisme retenu : trigger `state` + gardes numériques `from_state`/`to_state` (au lieu de `numeric_state below`, pour couvrir un franchissement critique déjà sous 20, ex. `19 → 9`) ; détection **inline** (aucun capteur dérivé créé) ; tension ajoutée au message si numérique, sans bloquer l'envoi. |
