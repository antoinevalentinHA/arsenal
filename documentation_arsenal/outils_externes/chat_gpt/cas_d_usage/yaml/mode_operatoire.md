# 🧠 ARSENAL — ChatGPT
# Cas d’usage — YAML Home Assistant
# Mode opératoire contractuel

## 🎯 Objet

Ce document définit le **mode opératoire obligatoire**
lors de l’utilisation de ChatGPT pour :

- la **modification** de YAML Home Assistant existant,
- la **création** de YAML Home Assistant (régime renforcé — Option B),

dans le cadre du système Arsenal.

Il ne définit ni les règles d’autorisation,
ni les interdictions structurelles ou sémantiques
(cf. `contrat.md`).

Les règles relatives aux en-têtes de fichiers sont définies dans
`/homeassistant/documentation_arsenal/architecture/en_tetes_fichiers.md`
et font partie intégrante du présent mode opératoire.

---

## 🧱 Principe opératoire fondamental

Aucune production YAML exécutable n’est autorisée
sans que **toutes les étapes préalables** aient été
explicitement respectées et validées.

ChatGPT doit **s’arrêter** à la moindre ambiguïté.

---

## 🔁 Séquence opératoire obligatoire

### 🟦 Étape 0 — Qualification de la demande

Avant toute action, l’utilisateur doit fournir explicitement :

- le **type d’opération** :
  - modification
  - création (Option B)

- le **chemin exact** du fichier cible

- la **nature technique** :
  - automation
  - script
  - sensor / binary_sensor
  - helper
  - template
  - lovelace YAML

- le **périmètre précis** de l’intervention

- **pour toute automation** :
  - l’`id:` d’automatisation à utiliser, fourni explicitement
  - ou l’indication explicite que l’ID sera fourni ultérieurement
    (auquel cas aucune génération YAML exécutable n’est autorisée)

Sans ces éléments, ChatGPT **ne produit rien**.

---

### 🟦 Étape 1 — Fourniture de la matière source

#### Cas A — Modification

L’utilisateur fournit :

- le **fichier YAML complet** concerné
- sans découpe
- sans omission

Les extraits partiels sont **interdits**, sauf demande explicite
de travail non exécutable (analyse uniquement).

---

#### Cas B — Création (Option B)

L’utilisateur confirme explicitement qu’il s’agit d’une **création**.

ChatGPT **ne génère encore aucun YAML**.

---

### 🟦 Étape 2 — Analyse structurelle préalable (obligatoire)

ChatGPT doit identifier et confirmer explicitement :

- le **dossier cible** (conforme à `structure_includes.md`)
- la **forme d’include attendue**
- la **structure YAML canonique** associée
- les **contraintes de reload YAML**
- les **dépendances** (entités lues / services appelés)
- la présence et la nature de l’en-tête de fichier attendu
  (ou existant),
- le rôle, le périmètre et les interdictions portées par cet en-tête
  le cas échéant.

👉 Cette étape est **descriptive**, jamais productive.

---

### 🟦 Étape 3 — Pré-validation (création uniquement)

*(Applicable uniquement en cas de création — Option B)*

ChatGPT produit une **fiche de création proposée**, contenant exclusivement :

- type d’objet Home Assistant
- dossier cible exact
- type d’en-tête Arsenal attendu
  (rôle, périmètre, interdits, statut)
- forme d’include attendue
- **nom d’entité proposé** (conforme à `nommage_entites.md`)
- liste des entités référencées
- analyse de robustesse au reload YAML

👉 Cette fiche **ne contient jamais** :
- de YAML exécutable
- de champ `id:`
- de proposition ou de calcul d’identifiant d’automatisation

L’utilisateur doit **valider explicitement** cette fiche
avant toute génération.

👉 L’en-tête fait partie intégrante de la validation.
Aucune génération YAML n’est autorisée tant que
l’en-tête proposé n’est pas validé.

---

### 🟦 Étape 4 — Production YAML exécutable

Uniquement après validation explicite de l’étape précédente.

ChatGPT produit alors :

- soit un **fichier YAML complet**
- soit un **bloc YAML complet** destiné à un include existant

Contraintes absolues :

- indentation strictement respectée
- aucune clé non demandée ajoutée
- aucune clé existante modifiée hors périmètre
- aucun renommage
- aucune optimisation implicite
- aucune correction “préventive” non demandée

---

### 🟦 Étape 5 — Contrôle de sortie

Avant livraison finale, ChatGPT vérifie et confirme que :

- la structure correspond exactement au dossier cible
- le YAML est **reload-safe** selon les principes Arsenal
- aucune entité n’est supposée disponible sans garantie
- aucune hypothèse implicite n’a été introduite

Si ce contrôle échoue, ChatGPT **n’émet pas la sortie**.

---

## 🛑 Règles d’arrêt immédiat

ChatGPT doit interrompre le processus et demander clarification si :

- le chemin cible est ambigu
- la nature technique n’est pas déductible
- un nom d’entité est incertain
- une dépendance n’est pas fournie
- la robustesse reload ne peut être garantie
- une instruction entre en conflit avec le contrat

---

## 📌 Statut

- Document procédural
- Applicabilité stricte
- Toute dérogation doit être explicitement demandée
  et validée avant production
