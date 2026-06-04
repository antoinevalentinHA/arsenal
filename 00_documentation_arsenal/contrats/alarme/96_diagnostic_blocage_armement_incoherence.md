# 🧠 ARSENAL — CONTRAT TECHNIQUE · Diagnostic — Cohérence structurelle du blocage armement

## 📌 Statut

- **Contrat technique local**
- Domaine : **Sécurité / Alarme**
- Nature : **diagnostic structurel**
- Portée : **mécanisme de blocage d’armement**
- Consommateur principal : automation `10020000000034`

---

## 🎯 Rôle

Exprimer **uniquement** l’existence d’une incohérence structurelle entre :

- `input_boolean.blocage_armement_auto`
- `timer.blocage_armement_auto`

Ce capteur constitue la **vérité diagnostique locale** du mécanisme de blocage.

Il ne porte :
- aucune logique métier globale
- aucune correction
- aucune temporisation métier
- aucune notification

---

## 🧱 Nature

Le capteur est un **binary_sensor de diagnostic brut**.

- `on`  → incohérence structurelle détectée
- `off` → cohérence structurelle du couple boolean / timer

Il ne doit jamais :
- masquer une incohérence
- interpréter un contexte métier
- neutraliser une anomalie pour des raisons fonctionnelles

---

## 🔍 Définition de l’incohérence

Le capteur passe à `on` dans les cas strictement suivants :

### Cas 1 — Blocage orphelin

input_boolean.blocage_armement_auto == on ET timer.blocage_armement_auto == idle

➡️ Interdit : absence de mécanisme de levée du blocage

---

### Cas 2 — Timer orphelin

input_boolean.blocage_armement_auto == off ET timer.blocage_armement_auto ∈ {active, paused}

➡️ Interdit : temporalité sans verrou associé

---

### Cas nominal

Dans tous les autres cas :

capteur = off

---

## 🚫 Hors périmètre

Le capteur ne doit **jamais dépendre** de :

- `alarm_control_panel.alarme_maison`
- `binary_sensor.presence_famille_securite`
- `binary_sensor.presence_famille_securite_absent_depuis_5_min`
- `input_boolean.mode_test_alarme`
- `input_boolean.mode_babysitting`
- tout autre état métier global

---

## 🧾 Sémantique

### État `off` — Cohérent

- `blocage on` + `timer active/paused`
- ou `blocage off` + `timer idle`

➡️ Le mécanisme est structurellement valide

---

### État `on` — Incohérent

- verrou sans temporalité
- ou temporalité sans verrou

➡️ Le mécanisme est structurellement invalide

---

## 🏷️ Attributs diagnostics

Le capteur expose des attributs purement informatifs :

### `blocage`
- état courant de `input_boolean.blocage_armement_auto`

### `timer_state`
- état courant de `timer.blocage_armement_auto`

### `type_anomalie`
- `blocage_orphelin`
- `timer_orphelin`
- `aucune`

Ces attributs :
- ne doivent pas influencer le comportement
- sont destinés à l’observabilité et aux notifications

---

## ⏱️ Temporalité

Le capteur est **brut**.

Il ne porte :
- aucune stabilisation
- aucun délai
- aucune mémoire

La stabilisation temporelle (500 ms) est déléguée à l’automation consommatrice.

---

## 🔒 Invariants

### Invariant 1 — Pureté diagnostique

Le capteur exprime uniquement une incohérence.  
Il ne corrige, ne temporise et ne notifie jamais.

---

### Invariant 2 — Localité stricte

Le capteur dépend exclusivement de :

- `input_boolean.blocage_armement_auto`
- `timer.blocage_armement_auto`

---

### Invariant 3 — Indépendance métier

Aucun contexte global ne doit altérer la détection.

Une incohérence structurelle reste une incohérence, quel que soit le contexte.

---

### Invariant 4 — Réversibilité immédiate

Toute correction du watchdog doit faire repasser le capteur à `off`.

---

## 🔗 Intégration avec le watchdog

L’automation `10020000000034` :

- ne doit plus être déclenchée sur les entités sources
- doit être déclenchée sur :

binary_sensor.blocage_armement_incoherent

Condition de déclenchement :

- passage `off → on`
- persistance ≥ 500 ms

---

## 🧪 Cas de test

### Cas nominal 1

blocage = on timer = active → capteur = off

---

### Cas nominal 2

blocage = off timer = idle → capteur = off

---

### Cas anomalie 1

blocage = on timer = idle → capteur = on → type_anomalie = blocage_orphelin

---

### Cas anomalie 2

blocage = off timer = active → capteur = on → type_anomalie = timer_orphelin

---

### Cas anomalie 3

blocage = off timer = paused → capteur = on → type_anomalie = timer_orphelin

---

### Après correction

correction watchdog appliquée → capteur = off

---

## 🏷️ Nommage

Nom recommandé :

binary_sensor.blocage_armement_incoherent

Justification :

- lecture directe
- déclenchement naturel sur `to: on`
- cohérent avec un watchdog correctif

---

## 🎯 Conclusion

Ce capteur permet :

- une séparation stricte **diagnostic / correction**
- une réduction drastique des déclenchements parasites
- une observabilité claire du mécanisme
- un alignement complet avec les principes Arsenal

Il constitue la base normative du watchdog de cohérence blocage.