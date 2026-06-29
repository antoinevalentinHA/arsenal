# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Interfaces contexte & helpers

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : [`20_interfaces_contexte_et_helpers.md`](20_interfaces_contexte_et_helpers.md)

---

## 🎯 Objet

Définir les **entrées contextuelles** consommées par l’alarme et les **sorties**
publiées par le cerveau alarme via helpers.

---

## 🔌 Entrées contractuelles (lecture)

### Stratégie alarme

- `input_select.mode_alarme`
  - Valeurs attendues :
    - `Manuel`
    - `Automatique`
    - `Désactivé`

### Présence sécurité (autorité contractuelle : présence)

- `binary_sensor.presence_famille_securite`

### Absence stabilisée (projection temporelle)

- `binary_sensor.presence_famille_securite_absence_confirmee_alarme`
  - Projection confirmée d’absence (`delay_on: 5 min`), réservée à l’armement automatique.
  - État atomique “prêt à consommer” : la temporisation est portée par le capteur lui-même, reconstructible à partir d’un seul état persistant.
  - _Historique :_ l’ancien déterminant d’armement `binary_sensor.presence_famille_securite_absent_depuis_5_min` (timer + automatisation tierce, dépendance non atomique) a été **supprimé en phase 2** (commit `c4637ee`, #160).

### Blocage armement auto (verrou logique)

- `input_boolean.blocage_armement_auto`

### Délai d’entrée (projection temporelle)

- `binary_sensor.delai_desarmement_en_cours`
  - Contractuellement : ON si `timer.delai_entree` est `active`.

### Contexte visite (signal externe au noyau alarme)

- `input_boolean.presence_visiteur`
- `input_boolean.visite_en_cours`
- `binary_sensor.creneau_visiteur_actif`
- `input_boolean.mode_visiteur`
- `input_select.jour_visiteur`
- `input_datetime.visiteur_start`
- `input_datetime.visiteur_end`

Remarque :
- La visite est un **contexte humain explicite**, pas une présence.
- Le noyau alarme peut la consommer comme **inhibition / neutralisation**.

---

## 📤 Sorties contractuelles (écriture)

Les helpers suivants sont **exclusivement écrits** par :

- `script.alarme_decision_centrale`

### Décision

- `input_text.alarme_decision`

### État cible

- `input_text.alarme_etat_cible`

### Raison humaine

- `input_text.alarme_raison`

---

## 🔒 Interdictions formelles

Il est interdit :

- d’écrire `input_text.alarme_*` depuis une automation, un capteur, ou l’UI,
- de recalculer une “décision alarme” ailleurs que dans le cerveau,
- de remplacer présence sécurité par une autre présence.

---

## ⚠️ Avertissement Home Assistant — `Maximum number of runs exceeded` (acceptation contractuelle)

Le warning suivant peut apparaître ponctuellement dans les logs Home Assistant lors des **rafales légitimes** (entrée / sortie du domicile) :

- `Maximum number of runs exceeded`

### Interprétation contractuelle

Ce warning signifie qu’un nombre de déclenchements supérieur à la capacité du buffer d’exécution (`mode` / `max`) est survenu sur l’automation d’application.  
Il s’agit d’un **signal de backpressure / shedding** du scheduler Home Assistant, **pas** d’un défaut métier.

### Acceptation Arsenal (Position A)

Ce warning est **accepté** dans Arsenal **tant que** les invariants suivants sont respectés :

- Le cerveau `script.alarme_decision_centrale` ne consomme **que des états persistants** (states), jamais des événements éphémères non persistés.
- La décision est **reconstructible** à tout instant à partir des entrées contractuelles.
- Les scripts d’application (`script.alarme_armer`, `script.alarme_desarmer`) restent **idempotents** vis-à-vis de l’état réel (`alarm_control_panel.alarme_maison`).

### Lignes rouges (non acceptables)

Le warning devient **non acceptable** si l’une des conditions suivantes apparaît :

- introduction d’une entrée décisionnelle **non persistante** (event clavier, MQTT event, webhook, etc.) sans persistance préalable en helper,
- dépendance à un **événement unique** pour atteindre l’état final (non reconstructible par state),
- apparition d’une boucle de rétroaction conduisant à une saturation permanente.

### Conséquence opérationnelle

- Le warning peut être considéré comme **bruit maîtrisé** dans les rafales.
- Toute augmentation de fréquence ou apparition hors rafales doit déclencher une **revue de déclencheurs** et de la **durée des actions applicatives**.