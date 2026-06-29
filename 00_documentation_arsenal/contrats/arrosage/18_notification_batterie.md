# CONTRAT ARSENAL — ARROSAGE
## 18 — Notification mobile batterie faible Rain Bird

**Version contrat :** v0.1
**Statut :** **Normatif — antérieur au runtime.** Ce document **spécifie** la future
notification mobile « batterie faible » du contrôleur Rain Bird ESP-BAT-BT2. Il **ne
crée aucun** template sensor, helper, script, automation ou élément d'UI, et **ne
fige aucun `entity_id` dérivé, ID d'automation, seuil ni durée définitifs**. Aucun
lot runtime n'est ouvert ici.

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

- **Couche diagnostic/interprétation** (future) : un capteur dérivé qualifiant la
  batterie « faible » à partir de la source numérique, robuste aux états
  indéterminés.
- **Couche notification mobile** (future) : une automation séparée, événementielle,
  déléguant l'envoi au canal central `script.notification_envoyer`.
- **Destinataire** : `input_text.telephone_antoine_notify` (canal déjà utilisé par
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

Noms **conceptuels** (chevrons), **non figés** — ratification en `entity_id` réel
réservée au lot runtime futur :

- `‹rain_bird_batterie_faible›` — capteur d'interprétation booléen (template), vrai
  lorsque `battery_level` est numérique **et** sous le seuil faible, faux sinon ;
  rejette `unknown`/`unavailable`/`none`/chaîne vide ; conserve un comportement
  déterministe et recalculable.
- (optionnel, à arbitrer) `‹rain_bird_batterie_critique›` — second niveau si un seuil
  critique est retenu.

> Tant que le lot runtime n'est pas ouvert, **aucun** de ces capteurs n'existe ; leur
> nommage réel relève de la Phase 0 / d'un lot ultérieur ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)).

---

## Seuils et paramètres à arbitrer

Le dépôt **ne porte aucun seuil batterie Rain Bird**. Les valeurs ci-dessous sont des
**paramètres à arbitrer**, **non** des valeurs imposées :

| Paramètre | Description | Défaut proposé | À arbitrer |
|---|---|---|---|
| `seuil_faible` | Seuil bas sur `battery_level` (%) | **à décider** (réf. non contraignante : `28 %` utilisé par [`batteries.md`](../batteries.md)) | ✅ |
| `seuil_critique` | Second seuil, plus bas (optionnel) | non retenu par défaut | ✅ |
| `duree_stabilisation` | `for:` avant déclenchement (anti-rebond) | non retenue par défaut | ✅ |
| `seuil_retour` | Hystérésis de retour à la normale (> `seuil_faible`) | sans objet si retour non retenu | ✅ |
| `destinataire` | Cible mobile | `input_text.telephone_antoine_notify` | — |
| `emoji_titre` | Emoji de domaine du titre | `🔋` (alternative `💧` arrosage) | ✅ |

> **Aucune valeur définitive** n'est gravée par ce contrat. Le runtime futur devra
> matérialiser ces paramètres explicitement (helpers ou constantes documentées),
> sans constante implicite.

---

## Déclencheurs autorisés

Pour la **future** automation (modèle numérique, type Option A) :

- **`platform: numeric_state`** sur `sensor.rain_bird_bat_bt_2_e9a3_battery_level`,
  avec **`below: <seuil_faible>`**.
  - Un trigger `numeric_state below` ne se déclenche **qu'à l'entrée** dans la plage
    (franchissement descendant) ; il ne se répète pas tant que la valeur reste sous le
    seuil — anti-spam **intrinsèque**.
- **Garde obligatoire** (condition) : `trigger.from_state` **existe**, sa valeur est
  **numérique** et **supérieure ou égale au seuil** — c'est-à-dire que la batterie
  était réellement **non faible** avant le franchissement.
- (optionnel) **`for: <duree_stabilisation>`** si une stabilisation est retenue.

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

1. **Anti-reload / anti-restart** : la garde `from_state` numérique **≥ seuil** bloque
   toute transition issue d'un état non numérique. Au reload/restart, l'entité passe
   par `unavailable`/`unknown` → `from_state` non numérique → **aucune notification**.
2. **Anti-répétition** : `numeric_state below` ne re-déclenche pas tant que la valeur
   reste sous le seuil ; combiné à `mode: single`, aucune notification répétée tant que
   la batterie reste faible.
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
- **Destinataire** : `input_text.telephone_antoine_notify`.

---

## Critères d'acceptation runtime futur

Le lot runtime, lorsqu'il sera ouvert, devra démontrer :

1. **ID d'automation fourni par Antoine** — **aucun ID inventé**. Le runtime n'est pas
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
| 0.1 | 2026-06-29 | Création du contrat (spécification, **aucun runtime**). Architecture en deux couches (diagnostic d'interprétation + notification mobile), sources `battery_level` (principale, %) / `battery_voltage` (diagnostic), déclencheur futur `numeric_state below` avec garde `from_state` numérique ≥ seuil, exclusions `unknown`/`unavailable`/`none`/non numérique, anti-reload/anti-restart et anti-répétition, garde de disponibilité du pont, retour à la normale non retenu par défaut. Seuils laissés en paramètres à arbitrer ; ID d'automation runtime à fournir par Antoine. |
