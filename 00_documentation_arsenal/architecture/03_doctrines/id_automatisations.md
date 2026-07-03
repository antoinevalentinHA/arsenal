# 🧠 ARSENAL — Architecture : Gestion des IDs d’automatisations

---

## 🎯 OBJET

Ce document définit le système **ARSENAL** de gestion des identifiants (**IDs**) d’automatisations Home Assistant.

Il formalise :

- la nature des IDs  
- leur mode d’attribution  
- leur gouvernance  
- les invariants associés  

Ce document est **NORMATIF**.  
Toute automatisation Arsenal doit s’y conformer.

Il ne décrit pas :

- la logique métier des automatisations  
- les comportements fonctionnels  
- l’implémentation détaillée des scripts associés  

---

## 🧠 PRINCIPE FONDAMENTAL

Un ID d’automatisation Arsenal est un identifiant :

- **STRUCTUREL**
- **STABLE**
- **NON AMBIGU**

Il n’est :

- ni décoratif  
- ni généré implicitement  
- ni dérivable automatiquement d’un contenu YAML  

L’ID est attribué **AVANT le codage**,  
et ne dépend jamais de l’implémentation.

---

## 🧩 NATURE DES IDs

Les IDs sont :

- numériques  
- longs  
- non signifiants individuellement  

Leur signification est portée par :

- leur **PRÉFIXE** (domaine fonctionnel)  
- leur **unicité dans le temps**  

Un ID :

- n’est jamais réutilisé  
- n’est jamais modifié  
- n’est jamais recyclé  

---

## 🧱 STRUCTURE D’UN ID

Un ID Arsenal est composé de :

   <PREFIXE><SUFFIXE>

### PREFIXE

- numérique  
- longueur fixe (4 chiffres)  
- associé à un domaine fonctionnel Arsenal  

### SUFFIXE

- numérique  
- incrémental  
- longueur fixe  

**Exemple :**

   10120000000015

---

## 🗂️ DOMAINE FONCTIONNEL & PRÉFIXE

Le préfixe d’ID :

- représente un **DOMAINE FONCTIONNEL Arsenal**
- est sélectionné **EXPLICITEMENT** par l’utilisateur  

Le lien domaine ↔ préfixe :

- est documenté  
- est piloté par des helpers Home Assistant  
- n’est jamais déduit automatiquement par un outil externe  

---

## 🆕 CRÉATION D’UN NOUVEAU DOMAINE FONCTIONNEL

Lorsqu’un nouveau domaine fonctionnel Arsenal est introduit  
(nouvelle famille d’automatisations),  
la création d’un **PRÉFIXE D’ID associé est OBLIGATOIRE**.

Cette création passe exclusivement par :

   /homeassistant/06_input_selects/system/prefix_id.yaml

### Règles impératives

- Chaque nouveau domaine fonctionnel doit disposer  
  d’un préfixe numérique unique (4 chiffres).

- Le préfixe est ajouté explicitement comme option du helper :

     input_select.prefix_id_select


- Le libellé de l’option associe :
  - le préfixe numérique  
  - le nom du domaine fonctionnel Arsenal  

**Exemple :**

     "1021 - nouveau_domaine"

- Aucun domaine fonctionnel ne peut produire  
  d’automatisations sans préfixe déclaré.

- La création du préfixe **précède** :
  - toute génération d’ID  
  - toute écriture YAML  
  - toute interaction avec un outil externe  

Tant qu’un domaine n’est pas déclaré dans `prefix_id_select`,  
il est considéré comme **NON AUTORISÉ** à produire des automatisations.

---

## ⚙️ GOUVERNANCE DE L’ATTRIBUTION

L’attribution d’un nouvel ID repose sur :

- un choix utilisateur explicite du préfixe actif  
- une observation de l’existant réel (automations déclarées)  
- un calcul externe au YAML (outil dédié)  

Aucun ID n’est :

- inventé  
- supposé  
- incrémenté « logiquement » sans observation du système  

---

## 🔒 INVARIANTS ABSOLUS

- Un ID est fourni **AVANT** toute écriture YAML  
- Un ID ne change jamais après création  
- Un ID n’est jamais généré par ChatGPT  
- Un ID n’est jamais modifié par ChatGPT  
- Un ID ne dépend pas :
  - du nom de l’automatisation  
  - de son contenu  
  - de sa logique métier  

Toute automatisation sans ID explicite est **NON CONFORME**.

---

## 🔤 Représentation YAML (invariant technique)

Dans les fichiers YAML Home Assistant :

- Un `id:` d’automatisation doit être fourni **obligatoirement comme une chaîne de caractères**.

Exemple valide :

    id: "10150000000005"

Exemple invalide :

    id: 10150000000005

Raison :

- Home Assistant impose un type `str` pour `id`,
- Un entier provoque une désactivation immédiate de l’automation.

Cet invariant est opposable à tout outil externe (ChatGPT inclus).

---

## 🛑 INTERDICTIONS FORMELLES

Il est strictement interdit :

- de générer un ID « temporaire »  
- de déduire un préfixe à partir d’un domaine  
- d’incrémenter un ID existant manuellement  
- de réutiliser un ID supprimé  
- de modifier un ID pour des raisons de lisibilité  

---

## 🤖 OUTILS EXTERNES (ChatGPT, IA, générateurs)

Les outils externes :

- consomment un ID fourni  
- ou s’arrêtent si l’ID n’est pas fourni  

Ils n’ont **AUCUN** droit de :

- génération  
- suggestion  
- correction d’ID  

Toute production YAML via un outil externe  
sans ID explicite est **INVALIDE**.

---

## 🧯 EXCEPTION TRACÉE — Reprise AID-006 (unique, datée : 2026-07-03)

La règle générale ci-dessus — **« un ID ne change jamais après création »** — **demeure pleinement en vigueur**. Une **exception unique**, explicitement décidée et documentée, est actée pour une **reprise de dette historique de format** :

- **Objet** : migration des **58 identifiants legacy à 13 chiffres** (suffixe 9) vers le format **canonique à 14 chiffres** (préfixe + suffixe 10), tel que produit par `script.generate_next_id_from_prefix`.
- **Mapping** : strictement déterministe — `PPPP + s9 → PPPP + 0 + s9` (insertion d'un `0` après le préfixe de 4 chiffres). Exemple : `1015000000001 → 10150000000001`.
- **Ce que l'exception N'autorise PAS** : aucune réattribution métier, aucun changement de préfixe, aucune invention ni incrémentation d'ID, aucune modification d'un ID pour toute autre raison (notamment pas « pour lisibilité »).
- **Justification** : dette identifiée par le garde-fou CI `AID-006` ; mapping **sans collision** (vérifié) ; opération **atomique et tracée**.
- **Traçabilité** : rapport d'opération — [`audits/01_rapports/transverses/migration_ids_automatisations_13_vers_14.md`](../../audits/01_rapports/transverses/migration_ids_automatisations_13_vers_14.md).
- **Durcissement acté (2026-07-03)** : après validation runtime (Git + CI + Home Assistant), le contrat a été **durci** — la longueur canonique **14 est exigée strictement par `AID-003` (ERROR)** et la tolérance `AID-006` (INFO) a été **retirée**. Toute régression vers un ID à 13 chiffres est désormais **bloquée en CI**.

Cette exception est **unique et close** : elle ne crée **aucun précédent** pour une modification d'ID hors de ce périmètre.

---

## 📌 STATUT

Document d’architecture Arsenal  
**Normatif et opposable**

Toute dérogation doit être :

- explicitement décidée  
- documentée  
- localisée  
