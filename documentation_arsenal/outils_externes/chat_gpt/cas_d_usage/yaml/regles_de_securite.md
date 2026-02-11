# 🧠 ARSENAL — ChatGPT
# Cas d’usage — YAML Home Assistant
# Règles de sécurité (pare-feu défensif)

## 🎯 Objet

Ce document définit les **règles de sécurité transverses**
applicables à toute interaction impliquant :

- la génération,
- la modification,
- ou la création

de YAML Home Assistant via **ChatGPT** dans le système **Arsenal**.

Il agit comme un **pare-feu défensif** :
toute règle violée entraîne un **arrêt immédiat** du processus.

---

## 🧱 Principe fondamental

Toute production YAML est considérée comme :

> **potentiellement destructrice par défaut**

jusqu’à preuve explicite du contraire.

Aucune tolérance implicite n’est admise.

---

## 🔒 Règles de sécurité globales

### 🔴 Règle 1 — YAML = exécution persistante

Un YAML Home Assistant :

- est **exécutable**,
- est **persistant**,
- survit aux redémarrages,
- peut produire des effets différés.

Conséquence :
- toute modification est traitée comme **critique**,
- aucun “petit ajustement” n’est considéré bénin.

---

### 🔴 Règle 2 — ChatGPT n’est jamais un validateur

ChatGPT :

- ne valide jamais une configuration,
- ne garantit jamais un fonctionnement,
- ne certifie jamais une absence de régression,
- ne remplace jamais un test réel.

Toute affirmation de validité est **interdite**.

---

### 🔴 Règle 3 — Respect absolu de l’architecture Arsenal

Toute production doit être conforme aux documents d’architecture :

- `structure_includes.md`
- `nommage_entites.md`
- `principes_generaux.md`
- `id_automatisations.yaml`

En cas de doute ou de contradiction apparente :
→ **arrêt immédiat**

---

### 🔴 Règle 4 — IDs : autorité externe obligatoire

Pour toute automation :

- l’ID est **fourni par l’utilisateur**,
- issu du système Arsenal de gestion des IDs,
- jamais généré, calculé ou suggéré par ChatGPT.

Toute automation sans `id:` explicite est **bloquante**.

---

### 🔴 Règle 5 — Reload YAML comme test structurel

Toute production doit être pensée **reload-first** :

- aucune dépendance implicite à l’ordre de chargement,
- aucune entité supposée disponible sans garantie,
- aucune condition fragile (`condition: state`) introduite.

Une configuration fragile au reload est **non conforme**,
même si elle fonctionne en régime nominal.

---

### 🔴 Règle 6 — Création = risque maximal

Toute création YAML :

- est considérée plus risquée qu’une modification,
- nécessite une **pré-validation obligatoire**,
- interdit toute génération exécutable immédiate.

Aucune exception.

---

### 🔴 Règle 7 — Absence d’information = arrêt

Si une information critique manque, notamment :

- chemin exact,
- type d’objet,
- structure d’include,
- nom d’entité,
- ID d’automatisation,
- dépendances,
- contraintes de reload,

ChatGPT **doit s’arrêter immédiatement**
et demander explicitement l’élément manquant.

---

### 🔴 Règle 8 — Zéro initiative implicite

ChatGPT ne doit jamais :

- compléter un silence,
- “faire au mieux”,
- proposer une alternative,
- optimiser sans demande,
- corriger un élément “manifestement incorrect”.

Toute initiative non demandée est interdite.

---

## 🛑 Conditions d’arrêt immédiat

Le processus est interrompu sans production si :

- une règle ci-dessus est violée,
- une ambiguïté persiste,
- une instruction entre en conflit avec l’architecture,
- une création est demandée sans phase de pré-validation,
- un ID d’automatisation est absent.

---

## 📌 Statut

- Document de sécurité Arsenal
- Transversal à tous les cas d’usage YAML
- Opposable à tout outil externe (IA incluse)

Toute dérogation doit être :
- explicitement décidée,
- documentée,
- et limitée dans son périmètre.
