# 🧠 ARSENAL — DOCUMENTATION DE RÉFÉRENCE

---

## 🎯 OBJET

Ce dossier contient la **documentation fonctionnelle, architecturale et historique**
du système **Arsenal**.

Il ne s'agit **ni** d'une aide Home Assistant,
**ni** d'un tutoriel,
**ni** d'un journal de commits Git.

Cette documentation décrit :

- ce que le système **doit faire** (contrats),
- **comment** et **pourquoi** il est construit ainsi (architecture),
- comment il a **évolué** dans le temps (changelog, historique),
- comment il est **audité** et gouverné (audits),
- comment il s'**interface** avec des outils externes,
- comment il se **navigue** transversalement (navigation).

Elle constitue la **référence de vérité** du système Arsenal.

> **Règle d'or.** Ce qui n'est pas documenté ici n'existe pas fonctionnellement.
> Inversement, ce qui est documenté ici doit pouvoir être retrouvé dans le système.

---

## 🧱 PHILOSOPHIE GÉNÉRALE

Arsenal repose sur une séparation stricte entre :

- **Intention utilisateur**
- **Règles métier**
- **Décisions observables**
- **Actions matérielles**

La documentation reflète cette séparation. En particulier, le **contrat** (ce que
le système doit faire) est distinct de l'**architecture** (comment il le fait) :
si une implémentation contredit un contrat, c'est l'implémentation qui est fausse.

---

## 📁 STRUCTURE RÉELLE DU DOSSIER

Le dossier est organisé en **neuf zones de premier rang**, plus ce README.

```
00_documentation_arsenal/
│
├── README.md                ← ce fichier
│
├── architecture/            ← référence d'implémentation (comment / pourquoi)
├── audits/                  ← cycle de vie d'audit par domaine
├── changelog/               ← évolution versionnée + récit historique
├── contrats/                ← référence normative (ce que le système doit faire)
├── evolutions_futures/      ← fiches prospectives (sas)
├── navigation/              ← orientation inter-familles (hubs, carte, pivots)
├── outils_externes/         ← supervision d'outils hors Home Assistant
├── schemas_ascii/           ← diagrammes ASCII de pipelines
└── ui/                      ← charte couleurs + socle de cartes Lovelace
```

---

## 📂 LES NEUF ZONES

### 🏗️ `architecture/`
Décrit **comment** le système est construit et **pourquoi** : doctrines transverses
(`03_doctrines/`), structure des includes (`00_structure_includes/`), recorder,
étiquettes, et documents d'architecture par sous-système.
👉 Référence d'implémentation. **N'introduit aucune règle métier.**
Voir [`architecture/README.md`](architecture/README.md).

### 🔍 `audits/`
Trace le **cycle de vie d'audit** par domaine, en étapes successives :
`01_rapports/` → `02_{arbitrages, conception, constats, contre_expertises}/` →
`03_plans_action/` → `04_chantiers/` → `05_clotures/`.
👉 Point d'entrée : [`audits/index.md`](audits/index.md).

### 📜 `changelog/`
Trace **l'évolution du système** dans le temps. Versionnage atomique et diffable
sous `changelogs/vXX/`, changelogs de chantiers sous `chantiers/`, récit
rétrospectif des inflexions dans `historique.md`.
👉 Point d'entrée : [`changelog/index.md`](changelog/index.md).
👉 Récit : [`changelog/historique.md`](changelog/historique.md).

### 📘 `contrats/`
Définit **ce que chaque sous-système DOIT faire** : intention utilisateur, règles
métier, invariants, dérives interdites. Domaines folderisés (`chauffage/`,
`climatisation/`, `alarme/`, `ecs/`, `meteo/`, `aeration_blocage_chauffage/`,
`boiler/`, `pannes/`…) et contrats de domaine à la racine.
👉 Principe : **le contrat précède l'implémentation.**
👉 Voir [`contrats/README.md`](contrats/README.md).

### 🌱 `evolutions_futures/`
Sas de **fiches prospectives**. Une fiche y séjourne tant qu'elle n'est pas
formalisée ; une fois actée, elle migre vers `contrats/` ou `outils_externes/`.

### 🧰 `outils_externes/`
Documente la **supervision d'outils hors Home Assistant** : pont chaudière
(`boiler_pi/`), outillage NAS Arsenal (`nas_arsenal/`), NAS Imprimerie
(`nas_imprimerie/`), ainsi que des gabarits d'autoring (prompts de génération).

### 🧭 `navigation/`
Couche d'**orientation inter-familles** : carte des domaines (`carte_domaines.md`),
21 hubs Tier-1 (un par domaine, point d'entrée transversal), pivots thématiques.
👉 **Non normative** — oriente sans redéfinir. Porte d'entrée : [`navigation/README.md`](navigation/README.md).

### 🗺️ `schemas_ascii/`
Diagrammes **ASCII** de pipelines (aération, NAS↔HA, régulation thermique),
destinés à une lecture rapide en texte brut.

### 🎨 `ui/`
**Charte couleurs** (`couleurs/`) et **socle de cartes** Lovelace (`socle_ui/`),
plus les documents d'architecture UI transverse.
👉 Voir [`ui/README.md`](ui/README.md).

---

## 🧭 OÙ CHERCHER QUOI

| Question | Zone |
|---|---|
| « Que **doit** faire ce domaine ? » | `contrats/` |
| « **Comment** est-ce implémenté, et pourquoi ? » | `architecture/` |
| « **Qu'est-ce qui a changé** et quand ? » | `changelog/` |
| « Cet état a-t-il été **audité** ? » | `audits/` |
| « Comment Arsenal parle à un **outil externe** ? » | `outils_externes/` |
| « À quoi ressemble le **pipeline** ? » | `schemas_ascii/` |
| « Quelle **couleur / carte** UI utiliser ? » | `ui/` |
| « Une **idée** pas encore formalisée ? » | `evolutions_futures/` |
| « **Comment naviguer** dans la documentation ? » | `navigation/` |

---

## 🚫 CE QUE CETTE DOCUMENTATION N'EST PAS

- ❌ un dump de configuration Home Assistant
- ❌ une documentation utilisateur finale
- ❌ un journal de commits Git
- ❌ un espace de notes temporaires

---

## 📌 STATUT

- Portée : **système Arsenal**
- Nature : **documentation de référence**
- Autorité : **contrats fonctionnels** (prioritaires sur le code)
- Mise à jour : volontaire, réfléchie, tracée dans le changelog

---

## ✍️ NOTE FINALE

Cette documentation n'est pas figée, mais elle ne doit évoluer **que** lorsqu'une
intention utilisateur, une décision d'architecture ou un fait d'évolution le
justifie. Toute modification doit être **consciente, explicitée et tracée**.
