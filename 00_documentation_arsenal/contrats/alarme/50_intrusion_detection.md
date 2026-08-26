# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Détection d'intrusion

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/50_intrusion_detection.md`

---

## 🎯 Objet

Définir les règles de détection d'intrusion dans Arsenal :

- les automations de détection,
- leurs conditions de déclenchement,
- leur séparation stricte avec la décision,
- le traitement du mode test.

---

## 🧱 Principe fondamental

La détection d'intrusion est **événementielle et réactive**.

Les automations de détection :

- détectent un événement physique,
- vérifient les conditions contractuelles,
- appliquent une action terminale (déclenchement ou notification test),
- **ne re-déduisent pas** la stratégie d'armement.

---

## ✅ Automations canoniques

### `10020000000031` — Délai d'entrée (start)

- **Rôle** : démarrer le timer de délai d'entrée sur ouverture d'un ouvrant d'entrée.
- **Triggers** : `binary_sensor.alarme_ouverture_entree`, `binary_sensor.alarme_ouverture_garage` — front `off → on`.
- **Conditions** :
  - `alarm_control_panel.alarme_maison == armed_away`
  - `timer.delai_entree == idle` (non-réentrant)
- **Action** : démarrage de `timer.delai_entree` + `script.sirene_bip` (hors mode test)
- **Mode** : `single`

### `10020000000032` — Délai d'entrée (fin)

- **Rôle** : déclencher l'alarme si le délai d'entrée expire sans désarmement.
- **Trigger** : `timer.finished` sur `timer.delai_entree`
- **Conditions** :
  - `input_boolean.systeme_stable == on` (garde post-reboot)
  - `alarm_control_panel.alarme_maison == armed_away`
- **Action** : hors mode test → `alarm_control_panel.alarm_trigger` + notification critique ; en mode test → notification de test uniquement, aucun déclenchement réel (bifurcation `input_boolean.mode_test_alarme`, conforme à I2 — **ALM-A2-2 résolu**, commit `db9fba8c`). La sirène est déclenchée par le **seul** chemin canonique `triggered → script.sirene_forte` (CH-1 C1). Le garde `binary_sensor.ouverture_qualifiee_maison` n'intervient plus : `timer.finished` vaut à lui seul preuve d'intrusion non désarmée (CH-1 B2).
- **Mode** : `single`
- **⚠️ Dette architecturale documentée** : court-circuite le pipeline canonique (voir §9).

### `10020000000009` — Intrusion mouvement

- **Rôle** : déclencher l'alarme sur détection de mouvement dans une zone sensible.
- **Triggers** : `binary_sensor.mouvement_sejour`, `binary_sensor.mouvement_entree`, `binary_sensor.mouvement_garage` — front `off → on`, **débounce `for: 2 s`** (anti-course, voir I4 — **ALM-A2-3**)
- **Conditions** :
  - `input_boolean.systeme_stable == on` (garde post-reboot, cf. I8)
  - `alarm_control_panel.alarme_maison == armed_away`
  - `timer.delai_entree != active` (délai d'entrée non en cours)
  - `not is_state('vacuum.roborock_q7_max', ['cleaning', 'returning'])` —
    **exclusion pendant le mouvement normal du robot**, fail-open jusqu'à l'absence
    de l'entité, cf. I7
- **Action** : `alarm_control_panel.alarm_trigger` + notification (réel) ou notification test uniquement (mode test)
- **Mode** : `single`

### `10020000000007` — Intrusion ouverture (autres capteurs)

- **Rôle** : déclencher l'alarme sur ouverture d'un capteur de contact surveillé (hors ouvrants d'entrée).
- **Triggers** : liste de `binary_sensor.contact_*` — transition vers `on`
- **Conditions** :
  - capteur valide (`state not in ['unknown', 'unavailable']`)
  - `alarm_control_panel.alarme_maison == armed_away`
  - `binary_sensor.delai_desarmement_en_cours == off`
- **Action** : `alarm_control_panel.alarm_trigger` + notification (réel) ou notification test (mode test)
- **Mode** : `queued`, max 10

---

## 🔒 Invariants contractuels

### I1 — Séparation détection / décision

Les automations de détection ne calculent aucune décision d'armement.
Elles ne modifient pas `input_text.alarme_etat_cible`.

### I2 — Mode test obligatoire

Toute automation de détection doit implémenter un comportement distinct en mode test :

- en mode test : notification uniquement, aucun déclenchement réel.
- hors mode test : déclenchement réel + notification critique.

La bifurcation est portée par `input_boolean.mode_test_alarme`.

> **ALM-A2-2 (audit 2026-06) — RÉSOLU.** `10020000000032` (fin de délai) bifurque
> désormais sur `input_boolean.mode_test_alarme` (commit `db9fba8c`) : hors mode test,
> déclenchement réel + notification critique ; en mode test, notification de test
> uniquement, **sans** déclenchement réel du panneau. L'écart à I2 est levé.
>
> **Conséquence pour `S3`.** En mode test, l'expiration du délai ne produit plus de
> `triggered` ni de sirène (notification de test seule). La validation **positive** de
> la détection à l'échéance (`ALM-CRIT-2`) doit donc être conduite **hors mode test**.
> Les mentions « S3 → triggered + sirène en mode test » des snapshots datés
> (`etat_post_CH6.md`, `cloture_ch1_alarme.md` §10) sont antérieures à cette résolution.

### I3 — Garde `armed_away`

Aucune automation de détection ne déclenche l'alarme si `alarm_control_panel.alarme_maison != armed_away`.

### I4 — Garde délai d'entrée

L'automation mouvement ne déclenche pas pendant le délai d'entrée (`timer.delai_entree == active`).

L'automation ouvrants d'entrée (délai start) est la seule à réagir pendant cette fenêtre.

> **Fenêtre d'établissement (ALM-A2-3, audit 2026-06) — résolu.** L'inhibition repose
> sur `timer.delai_entree == active`, état posé par une chaîne plus longue (contact →
> `alarme_ouverture_*` trigger-based → `delai_entree_start` → `timer.start`) que la
> détection mouvement (capteurs `mouvement_*` agrégés en **template pur, synchrone**).
> Un mouvement quasi simultané à l'ouverture (cas **garage** / rafale d'entrée, cf.
> backpressure acceptée au contrat `30_…` Position A) pouvait être évalué alors que le
> timer était encore `idle` → faux déclenchement rare. Le trigger mouvement porte donc
> un **débounce `for: 2 s`** (commit `e3f14563`) qui laisse la chaîne d'inhibition
> s'établir avant l'évaluation. Détection préservée (rémanence PIR ≫ 2 s) ; coût = +2 s
> de latence sur la détection par mouvement seul. Valeur ajustable (résidu de queue
> extrême si l'établissement dépasse 2 s).

### I5 — Garde capteur valide

Toute automation réagissant à l'état d'un capteur doit ignorer les états `unknown` et `unavailable`.

### I6 — Sirène forte : déclenchement contractuellement qualifié uniquement

`script.sirene_brutale` est appelé uniquement sur :

- intrusion confirmée (délai d'entrée expiré sans désarmement)
- mouvement réel détecté en mode armé

Jamais sur un simple feedback d'armement/désarmement.

### I7 — Exclusion robot : mouvement normal, et rien d'autre

La détection par mouvement (`10020000000009`) est inhibée **uniquement** lorsque
l'entité standard `vacuum.roborock_q7_max` représente un **mouvement normal du
robot**. La liste des régimes suppressifs est **exhaustive et fermée** :

| État `vacuum.roborock_q7_max` | Détection mouvement |
|---|---|
| `cleaning` | **inhibée** |
| `returning` | **inhibée** |
| `idle` | active |
| `paused` | active |
| `error` | active |
| `docked` | active |
| `unknown` | active |
| `unavailable` | active |
| **entité absente du state machine** | active |

**Fail-open explicite, jusqu'à l'absence de l'entité.** `unknown` et `unavailable`
ne sont jamais assimilés à un nettoyage, et une entité **totalement absente** du
state machine — intégration Roborock retirée, entité supprimée — ne l'est pas
davantage. Une lecture absente ou dégradée du robot **n'inhibe jamais** l'alarme :
l'indisponibilité d'un équipement de confort ne doit pas désarmer silencieusement
un garde de sécurité. La condition est la **négation** de la liste fermée
`[cleaning, returning]` — tout état hors de cette liste, connu ou non, et l'absence
d'état, laissent la détection active.

**Forme imposée.** L'expression est un `condition: template` minimal :

```yaml
- condition: template
  value_template: >-
    {{ not is_state('vacuum.roborock_q7_max', ['cleaning', 'returning']) }}
```

`is_state()` accepte nativement une **liste** d'états (signature
`is_state(entity_id: str, state: str | list[str])`, appartenance testée par
`state_obj.state in state`) : un seul appel suffit, et **aucune comparaison
textuelle à `unknown` ou `unavailable`** n'a à figurer dans la condition — ces
états sortent de la liste fermée par construction.

> **Pourquoi la forme `not` + `condition: state` est proscrite ici.** Elle
> satisfait les huit premiers régimes mais **pas le neuvième**. Sur une entité
> absente du state machine, `condition: state` lève une `ConditionError` ; le
> compound `not` ne convertit **pas** cette erreur en vrai — il la collecte et la
> propage (`NotConditionChecker`), et l'automation est abandonnée. Le garde
> deviendrait alors **fail-closed** : l'alarme silencieusement inhibée par la
> disparition d'une entité de confort, c'est-à-dire l'inverse de I7. `is_state()`,
> lui, rend `False` sans lever lorsque le state object vaut `None` — la négation
> vaut `true`, la détection reste active. C'est la seule raison du recours au
> template, et elle est **normative** : toute réécriture en primitives `state`
> réintroduirait le défaut.

> **ALM-ROBO-1 (correctif 2026-08) — le témoin précédent était faux dans les deux
> sens.** L'exclusion reposait sur `binary_sensor.roborock_q7_max_nettoyage == off`.
> Ce binaire ne reflète pas « le robot nettoie » : il reflète le champ `in_cleaning`
> du statut, dont l'énumération est `0` terminé · `1` nettoyage global inachevé ·
> `2` zoné inachevé · `3` par segments inachevé. Sa sémantique réelle est **« une
> session n'est pas terminée »**, c'est-à-dire *reprenable* — c'est d'ailleurs ce
> que l'intégration en fait, `vacuum.start` le consultant pour choisir une commande
> de **reprise** plutôt qu'un démarrage (audit
> `aspirateur/audit_faisabilite_roborock_q7_max.md` §3.2 et §7).
>
> Le défaut est **bidirectionnel** — c'est ce qui interdit de le corriger en
> resserrant ou en élargissant simplement le garde existant :
>
> 1. **Sur-exclusion** — session inachevée, robot immobile, en pause ou arrêté en
>    erreur (`wheels_suspended`) : le binaire restait `on` des heures durant,
>    l'exclusion tenait, et la détection restait **inhibée trop longtemps** sans
>    qu'aucun robot ne bouge.
> 2. **Sous-exclusion** — le binaire repasse `off` dès la session déclarée
>    terminée, alors que le robot **roule encore vers sa base**. La détection était
>    donc **réactivée trop tôt**, robot en mouvement.
> 3. **Indisponibilité suppressive** — la condition stricte `state: 'off'` faisait
>    en outre de `unknown` et `unavailable` des états suppressifs : une simple
>    perte de lecture inhibait l'alarme.
>
> **Événement terrain établissant (2).** Le **2026-08-24 à 13:25:21 UTC**,
> `alarm_control_panel.alarme_maison` est passé à `triggered` et `10020000000009` a
> exécuté ses actions. Ses quatre conditions étaient donc vraies à cet instant, ce
> qui **établit que le témoin Roborock valait `off`**. L'opérateur atteste que le
> déclenchement a eu lieu **pendant le retour du robot vers sa base**.
>
> *Qualification probatoire.* Le capteur PIR exact et l'état Roborock détaillé ne
> sont **pas récupérables** — ni historisation ni trace conservée (cf. doctrine
> `solvabilite_probatoire.md` : la chaîne d'états attendue relèverait de L2/L3, non
> productible ici). La causalité robot → mouvement est donc une **preuve terrain
> opérateur (L5), corroborée par la trace de déclenchement mais non intégralement
> reconstituable**. Elle est consignée comme telle, sans être présentée comme une
> reconstitution runtime.
>
> **Ce que le correctif doit couvrir des deux côtés** : ne **pas** inhiber lorsque
> le robot est immobile, bloqué, en pause ou en erreur ; **continuer** à inhiber
> pendant le retour réel vers la base **et pendant l'accostage**, tant que le robot
> se déplace.
>
> L'entité standard `vacuum.*` lit, elle, la **machine d'état vive** de l'appareil
> (champ `state` du statut, distinct de `in_cleaning`) et satisfait les deux côtés :
> les nettoyages global, zoné et segmenté y valent tous `cleaning` ; le retour à la
> base **et** l'accostage y valent `returning` (`returning_home` et `docking` y sont
> mappés tous deux), l'état ne devenant `docked` qu'une fois le robot posé sur sa
> base ; une immobilisation en erreur y vaut `error`, jamais `cleaning`. C'est le
> seul témoin de **déplacement** exposé par l'intégration — c'est donc lui qui porte
> l'exclusion.

### I8 — Garde de stabilité système

`10020000000009` et `10020000000032` portent la condition
`input_boolean.systeme_stable == on`. Elle interdit tout déclenchement pendant la
fenêtre de recomposition qui suit un redémarrage de Home Assistant, où les états
d'entités se rétablissent dans un ordre non garanti.

Cette condition est un **garde**, jamais une autorisation : son absence ne rend
aucune détection admissible.

---

## 🛑 Interdictions

- Déclencher `alarm_control_panel.alarm_trigger` depuis une automation de détection sans vérification `armed_away`.
- Appeler `script.sirene_brutale` en mode test.
- Armer ou désarmer l'alarme depuis une automation d'intrusion.
- Introduire un délai (`delay`) dans une automation de détection.
- Contourner le mode test sur une action de déclenchement réel.
- Élargir l'exclusion robot au-delà de `[cleaning, returning]`, faire de
  `unknown` / `unavailable` des états suppressifs, ou réécrire la condition sous
  une forme qui échoue lorsque l'entité est absente du state machine (I7).

---

## ⚠️ §9 — Dette architecturale documentée

Les automations `10020000000032` (délai fin) et `10020000000009` (mouvement) et `10020000000007` (ouverture) court-circuitent le pipeline canonique Arsenal (Décision → Helpers → Application) en appelant directement :

- `alarm_control_panel.alarm_trigger`
- `script.sirene_brutale`

sans passer par `script.alarme_decision_centrale` ni `input_text.alarme_etat_cible`.

**Refonte cible (v2)** : matérialiser "intrusion confirmée" comme état contractuel persisté (`input_boolean.intrusion_confirmee` ou équivalent), puis déclencher panneau et sirène depuis cet état via le pipeline canonique.

Cette dette est **assumée et documentée**. Elle ne constitue pas une violation en l'état — elle est identifiée comme limitation technique V1 dans les en-têtes des automations concernées.

---

## 🔗 Dépendances contractuelles

| Entité | Rôle |
|--------|------|
| `alarm_control_panel.alarme_maison` | Source de vérité réelle |
| `timer.delai_entree` | Fenêtre de désarmement post-ouverture |
| `input_number.alarme_delai_entree` | Durée du délai (paramètre) |
| `input_boolean.mode_test_alarme` | Bifurcation test / réel |
| `binary_sensor.delai_desarmement_en_cours` | Projection du timer (état `active`) |
| `binary_sensor.ouverture_qualifiee_maison` | Confirmation intrusion active |
| `vacuum.roborock_q7_max` | Exclusion pendant le mouvement normal du robot — `cleaning` / `returning` (I7) |
| `script.sirene_bip` | Feedback sonore délai d'entrée |
| `script.sirene_brutale` | Action terminale intrusion |
| `script.arret_sirene` | Arrêt prioritaire |
| `script.notification_envoyer_avance` | Notification critique |
