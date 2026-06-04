# 🧠 ARSENAL — Intégrité des paramètres

## 🎯 Objet

Ce document définit le **mécanisme d’intégrité des paramètres** dans le système
**Arsenal (Home Assistant)**.

Il formalise :
- les **règles d’invariants logiques** applicables aux paramètres utilisateur,
- l’architecture de **détection des incohérences**,
- les **garanties systémiques** apportées,
- et les **choix volontairement exclus**.

Ce mécanisme est **transverse**, **structurel** et **antérieur** à toute logique métier.

---

## 🧠 Problématique fondatrice

Les helpers (`input_number`, `input_datetime`, etc.) sont :
- libres par conception,
- modifiables manuellement,
- non contraignables dynamiquement par Home Assistant.

Une configuration incohérente peut donc :
- ne produire **aucune erreur technique**,
- conduire à des **comportements paradoxaux**,
- provoquer un **effondrement silencieux** du système.

> Un système qui continue de fonctionner avec des paramètres invalides
> est **plus dangereux** qu’un système explicitement en erreur.

---

## 🧱 Principe fondamental Arsenal

> **Tout paramètre invalide rend toute décision suspecte.**

Conséquences :
- l’incohérence doit être **détectée explicitement**,
- elle ne doit **jamais être silencieuse**,
- elle ne doit **jamais être corrigée automatiquement**.

---

## 🧩 Architecture retenue

### 1️⃣ Détection par domaine

Chaque sous-système dispose d’un **binary_sensor dédié** :

- `binary_sensor.parametres_invalides_chauffage`
- `binary_sensor.parametres_invalides_vmc`
- `binary_sensor.parametres_invalides_deshumidificateur`
- `binary_sensor.parametres_invalides_eclairage`
- `binary_sensor.parametres_invalides_alarme`

Règle :
- `on`  → **au moins un invariant violé**
- `off` → **paramètres cohérents**

Ces capteurs sont :
- purement observateurs,
- sans correction,
- sans action,
- sans logique métier.

---

### 2️⃣ Source déclarative — Group

Les capteurs de domaine sont regroupés dans un **group dédié** :
group.parametres_invalides_domaines


Ce group :
- centralise la liste des domaines surveillés,
- permet l’extension du système **sans modifier les templates**,
- sert de base unique pour l’agrégation globale.

---

### 3️⃣ Agrégat global d’intégrité

Un capteur unique expose la **vérité système** :
binary_sensor.parametres_invalides_global


Caractéristiques :
- état binaire simple (ON / OFF),
- basé exclusivement sur le group,
- enrichi par des **attributs diagnostiques** :
  - domaines en défaut,
  - nombre de domaines invalides,
  - indicateurs par sous-système.

Ce capteur constitue le **point d’entrée unique** pour :
- l’UI,
- les diagnostics,
- les analyses humaines.

---

## 🚨 Signalisation et anti-silence

Lorsque des paramètres sont invalides :
- le système **le sait**,
- l’utilisateur **le voit**,
- l’information est **centralisée et lisible**.

Aucune incohérence ne peut subsister sans :
- un indicateur explicite,
- un accès rapide au détail,
- une visibilité UI claire.

---

## ❌ Choix volontairement exclus

Le mécanisme d’intégrité des paramètres **NE FAIT PAS** :

- ❌ correction automatique des valeurs,
- ❌ normalisation silencieuse,
- ❌ blocage forcé des automatisations,
- ❌ logique métier déguisée,
- ❌ dépendance entre helpers.

Ces choix sont intentionnels et assumés.

---

## 🔧 Extension du système

### Ajouter un nouveau domaine
1. Créer un `binary_sensor.parametres_invalides_<domaine>`
2. L’ajouter au `group.parametres_invalides_domaines`
3. Aucune autre modification n’est requise

### Ajouter un invariant
- Modifier uniquement le capteur du domaine concerné
- L’architecture globale reste inchangée

---

## 🧠 Positionnement architectural

Le mécanisme d’intégrité des paramètres est :
- **transverse**,
- **non métier**,
- **non décisionnel**,
- **fondamental**.

Il constitue un **socle de sûreté** sur lequel reposent
tous les sous-systèmes Arsenal.

---

## 📌 Conclusion

Ce mécanisme garantit que :
- le système ne ment jamais par omission,
- aucune incohérence n’est invisible,
- toute décision reste traçable et critiquable.

> **Arsenal préfère une alerte claire à une stabilité trompeuse.**

Ce document fait foi.
