# Contre-expertise — CH-6 Alarme (clavier PIN)

> **Constat audité :** ALM-CRIT-3 — « Le flux PIN clavier est inopérant »
> **Hypothèse initiale :** *l'inopérance vient de `script.turn_on` qui ne propagerait pas le `trigger` au script `traitement_code_clavier`.*
> **Base d'analyse :** dépôt réel `origin/main` = `e4dca15` + observations runtime fournies (Tests 1 & 2).
> **Nature :** contre-expertise — **diagnostic uniquement**. Aucun patch, aucun YAML, aucune proposition de correction.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Cartographie du flux réel

```
Clavier Frient (Zigbee2MQTT)
  publie en une fois : action="arm_all_zones"|"disarm", action_code="2802", action_user="unknown"
        │
        ├─ sensor.clavier_alarme_1_action        ← .../action  (verbe d'action)
        ├─ sensor.clavier_alarme_1_action_code    ← (entité présente au runtime ; NON déclarée par Arsenal)
        ├─ sensor.clavier_alarme_1_action_user    ← (entité présente au runtime ; NON déclarée par Arsenal)
        └─ sensor.clavier_alarme_1_badge          ← value_json.action_code  (déclaré par Arsenal = le code/UID)

   ── Chemin PIN ──────────────────────────────────────────────
   AUTO 1002000000005 « Armement clavier »
     trigger : sensor.clavier_alarme_*_action_code
     condition : states(trigger.entity_id) | regex_match('^[0-9]+$')   → vrai pour "2802"
     action : script.turn_on  script.traitement_code_clavier
        │
   SCRIPT traitement_code_clavier
     code_saisi = (trigger is defined) ? states(trigger.entity_id) : ''
     cond. 1  : code_saisi ∉ ['', 'unknown', 'unavailable', None]      → OBSERVÉ : true
     cond. 1b : code_saisi | regex_match('^[0-9]+$')                   → OBSERVÉ : FALSE  ◄── arrêt ici
     cond. 2  : code_saisi == states('input_text.alarm_code')          → jamais atteinte
     choose   : désarmer / ignorer / armer                            → jamais atteint

   ── Chemin BADGE (parallèle, même évènement) ────────────────
   AUTO 10020000000026 « Désarmement badge »
     trigger : sensor.clavier_alarme_*_action  to: "disarm"
     badge_utilise = states(sensor.clavier_alarme_1_badge)  (= action_code = "2802")
     choose : badge_utilise ∈ input_text.badges_autorises ? désarmer : NOTIF « Badge inconnu »
```

Deux automatisations distinctes réagissent **au même évènement clavier** : le chemin PIN (sur `_action_code`) et le chemin badge (sur `_action == "disarm"`).

---

## 2. Rôle des trois capteurs interrogés

- **`sensor.clavier_alarme_1_action`** — le **verbe d'action** publié par le clavier : `arm_all_zones` (cadenas fermé) ou `disarm` (cadenas ouvert). C'est lui qui déclenche le **chemin badge** (`desarmement_badge.yaml`, déclencheur `to: "disarm"`).
- **`sensor.clavier_alarme_1_action_code`** — le **code PIN saisi** (`2802`). C'est le déclencheur **et** la source de validation du **chemin PIN**. ⚠️ **Cette entité n'est pas déclarée par la couche MQTT Arsenal** (`14_mqtt_sensors/claviers.yaml` ne définit que `_action` et `_badge`). Elle existe au runtime via la découverte Zigbee2MQTT, mais le flux PIN **dépend d'une entité hors contrat de transport déclaré**.
- **`sensor.clavier_alarme_1_action_user`** — l'**identité de l'emplacement utilisateur** du clavier. Pour une saisie PIN sans emplacement nommé, sa valeur est `unknown`. Comme `_action_code`, elle **n'est pas déclarée** par Arsenal. Elle n'est lue par aucune des deux automatisations, mais sa valeur `unknown` reflète l'absence d'identité — point central de la confusion PIN/badge (cf. §5).

> **Divergence de contrat (certaine, dépôt) :** la logique consomme `_action_code` / `_action_user`, alors que le transport déclaré expose `_action` / `_badge`. Le code est exposé **deux fois** sous deux noms (`_action_code` non déclaré ; `_badge` déclaré = `action_code`). Cette dualité est au cœur du dysfonctionnement.

---

## 3. L'hypothèse initiale « trigger perdu via script.turn_on » est-elle crédible ?

**Partiellement — mais elle est infirmée comme *mécanisme opérant*.**

- **Ce qui reste vrai (certain, dépôt) :** `script.turn_on` ne transmet **pas** le `trigger` de l'automatisation au script. Or `code_saisi` **et** `nom_clavier` dérivent **exclusivement** de `trigger.entity_id`. Cette dépendance est **structurellement fragile** : le script n'a aucune source de code indépendante de `trigger`.
- **Ce que prédisait l'hypothèse :** `trigger` absent → `code_saisi = ''` → arrêt dès la **condition 1** (« code vide ») → le script « ne fait rien », silencieusement.
- **Ce que montre le runtime :** la condition 1 (« non vide / non unknown ») est **vraie**, la condition 1b (regex numérique) est **fausse**, et le script **reçoit une valeur exploitable**. Un `code_saisi` vide est **incompatible** avec une condition 1 vraie.

→ Le symptôme prédit (script muet sur code vide) **ne correspond pas** aux faits. L'hypothèse, dans sa formulation, est donc **infirmée** : le blocage n'est pas « le code n'arrive jamais », mais « **une valeur non numérique arrive et échoue la validation** ».

---

## 4. Étape exacte qui empêche l'armement

**Le script s'arrête à la condition 1b — le filtre `regex_match('^[0-9]+$')` renvoie `false`.** Les conditions 2 (comparaison au code attendu) et le bloc `choose` (désarmer / ignorer / **armer**) ne sont **jamais atteints**. Aucun armement ni désarmement n'est donc émis par le chemin PIN, dans **les deux tests**.

`code_saisi` est, au runtime, **non vide et non numérique**. La seule valeur cohérente avec les deux tests est le **verbe d'action** lui-même :
- Test 1 (cadenas fermé) : `code_saisi` ≈ `"arm_all_zones"` → non vide, non numérique → regex false.
- Test 2 (cadenas ouvert) : `code_saisi` ≈ `"disarm"` → non vide, non numérique → regex false.

Autrement dit, **la valeur soumise à la validation du code n'est pas le code, mais l'action**. Le couplage à `trigger.entity_id` sous `script.turn_on` ne délivre pas le champ attendu (`action_code`) au script : c'est l'action verbale qui parvient à `code_saisi`. La **provenance exacte** de cette substitution (trigger ambiant/rémanent en mode `queued`, ou `trigger.entity_id` pointant sur `_action`) **ne peut pas être tranchée par le seul dépôt** ; une trace runtime de `trigger.entity_id` et de `code_saisi` à l'intérieur du script la confirmerait en une ligne.

---

## 5. Pourquoi une notification « badge inconnu » avec un PIN valide ?

Cause **certaine** (lisible dans le dépôt), **indépendante** du chemin PIN :

1. Le geste de désarmement publie `sensor.clavier_alarme_1_action = "disarm"`.
2. `desarmement_badge.yaml` (`10020000000026`) se déclenche sur cette transition `to: "disarm"`.
3. Il calcule `badge_utilise = states('sensor.clavier_alarme_1_badge')`. Or `_badge` est défini comme `value_json.action_code` → pour une saisie PIN, **`badge_utilise = "2802"`** (le PIN lui-même).
4. Il teste `badge_utilise in badges_autorises`. La liste `input_text.badges_autorises` contient des **UID de badges RFID**, pas des codes PIN → « 2802 » n'y figure pas → branche `default` → **notification « Badge inconnu : 2802 »**.

→ Le **code PIN est interprété comme un UID de badge** par l'automatisation badge, qui rejette l'évènement. Le `user: unknown` observé est la valeur de `action_user` (aucun emplacement nommé) — il confirme l'absence d'identité, mais n'est **pas** ce que teste l'automatisation badge (elle teste `_badge` = le code). La notification est donc émise **alors que le PIN est correct**, parce qu'un **second chemin** traite le même évènement avec une **sémantique badge**.

---

## 6. Diagnostic de synthèse, cause probable, confiance

| Élément | Verdict | Confiance |
|---------|---------|-----------|
| Le PIN n'arme jamais (Test 1) | **Confirmé** (alarme reste `disarmed`) | **Élevée** |
| Le script s'exécute, évalue des conditions, reçoit une valeur | **Confirmé** (runtime) | **Élevée** |
| Blocage à la condition 1b (regex numérique = false) | **Confirmé** (runtime) | **Élevée** |
| `code_saisi` porte le verbe d'action, pas le code | **Très probable** (seule lecture cohérente des 2 tests) | **Moyenne-élevée** |
| Hypothèse « trigger perdu → code vide → script muet » | **Infirmée** comme mécanisme opérant | **Élevée** |
| Dépendance structurelle fragile du script à `trigger.entity_id` sous `script.turn_on` | **Confirmée** (dépôt) | **Élevée** |
| Dépendance à des entités non déclarées (`_action_code`, `_action_user`) | **Confirmée** (dépôt) | **Élevée** |
| « Badge inconnu » = PIN interprété comme UID par `desarmement_badge` | **Confirmée** (dépôt) | **Élevée** |
| Provenance exacte de la substitution code→action dans le script | **Indéterminée** sans trace runtime ciblée | **Moyenne** |

**Cause probable (synthèse) :** l'inopérance du PIN ne résulte **pas** d'un code « perdu » mais d'un **défaut de câblage sémantique** : (a) la valeur parvenant à la validation du script n'est pas le code mais l'action, ce qui fait échouer le filtre numérique avant tout armement ; (b) le même évènement est capté en parallèle par l'automatisation badge, qui interprète le code PIN comme un UID de badge et le rejette (« badge inconnu »). Le couplage du script à `trigger.entity_id` via `script.turn_on`, et la dépendance à des entités `_action_code`/`_action_user` non déclarées par la couche de transport, sont les fragilités structurelles sous-jacentes.

---

## 7. Qualification finale de CH-6

**REQUALIFIÉ.**

- **Le constat est CONFIRMÉ dans son effet** : le clavier PIN est inopérant pour l'armement (et pour le désarmement par PIN) — gravité **critique** maintenue.
- **La cause documentée est INFIRMÉE** : ce n'est pas « `script.turn_on` perd le trigger et le script ne fait rien ». Le script s'exécute et reçoit une valeur ; il **échoue à la validation du code** parce que la valeur reçue n'est pas numérique (vraisemblablement le verbe d'action), et l'évènement est **parasité** par l'automatisation badge.

**Énoncé requalifié proposé (pour le registre, sans correction) :**
> *ALM-CRIT-3 (requalifié) — Clavier PIN inopérant. La validation du code dans `script.traitement_code_clavier` échoue (condition regex numérique fausse) car la valeur soumise n'est pas le code PIN ; le script, couplé à `trigger.entity_id` sous `script.turn_on`, dépend en outre d'entités non déclarées (`_action_code`/`_action_user`). En parallèle, `desarmement_badge.yaml` interprète le code PIN comme un UID de badge et émet « badge inconnu ». Mécanisme « trigger perdu » initialement supposé : infirmé.*

**Vérification runtime décisive (non réalisée ici) :** journaliser, à l'entrée du script, `trigger is defined`, `trigger.entity_id` et `code_saisi` — cela confirmerait en une observation la substitution code→action et clôturerait le point de confiance « moyenne ».

---

*Contre-expertise CH-6 Alarme. Établie en lecture du dépôt (`origin/main` = `e4dca15`) et des observations runtime fournies. Diagnostic uniquement — aucun patch, aucun YAML, aucune proposition de correction.*
