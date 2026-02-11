# 🧠 ARSENAL — ChatGPT  
# Cas d’usage — YAML Home Assistant  
# Option B : création autorisée sous contrat renforcé

---

## 🎯 Objet

Ce document définit le **contrat d’usage normatif** applicable lorsque ChatGPT est utilisé pour :

- **modifier** du YAML Home Assistant existant dans Arsenal,
- **créer** de nouveaux objets YAML (entités, automatisations, scripts, helpers, templates, Lovelace YAML),
  selon un régime **renforcé et contrôlé**.

Il encadre strictement :

- les droits et limites de ChatGPT,
- les exigences de conformité structurelle Arsenal,
- les contraintes de robustesse (notamment au reload YAML),
- le respect des **en-têtes de fichiers comme contrats locaux**,
- les règles d’arrêt immédiat en cas d’ambiguïté.

Ce document est **NORMATIF**.  
Il ne décrit pas le déroulé opérationnel détaillé (cf. `mode_operatoire.md`).

---

## 🧱 Références normatives (autorité supérieure)

Toute production YAML via ChatGPT doit être **strictement conforme** aux documents suivants :

- `/homeassistant/documentation_arsenal/architecture/structure_includes.md`
- `/homeassistant/documentation_arsenal/architecture/nommage_entites.md`
- `/homeassistant/documentation_arsenal/architecture/principes_generaux.md`
- `/homeassistant/documentation_arsenal/architecture/id_automatisations.md`
- `/homeassistant/documentation_arsenal/architecture/en_tetes_fichiers.md`

En cas de contradiction apparente entre ces documents :

👉 ChatGPT **s’arrête immédiatement** et demande clarification.  
Aucune interprétation autonome, arbitrage implicite ou “correction logique” n’est autorisée.

---

## 🧠 Principe fondamental

ChatGPT est un **outil de transformation YAML contrôlée**.

Il n’est jamais :

- auteur métier,
- prescripteur architectural,
- validateur fonctionnel,
- arbitre de cohérence.

Une sortie YAML peut être syntaxiquement valide tout en étant
**architecturalement invalide** dans Arsenal.

👉 La conformité Arsenal prime toujours sur :
- les “bonnes pratiques” génériques,
- les standards Home Assistant non contextualisés,
- toute logique d’optimisation supposée.

---

## 🧩 Périmètre

### Inclus

- YAML Home Assistant :
  - automations
  - scripts
  - templates
  - sensors / binary_sensors
  - helpers
  - Lovelace YAML
  - fichiers de configuration associés
- corrections de robustesse au reload **strictement demandées**
- création d’objets YAML **uniquement** sous régime renforcé (Option B)

### Exclu

- modifications opportunistes ou implicites
- refactorisations structurelles
- renommages “pour clarté”
- optimisations de performance supposées
- changements d’architecture non explicitement demandés
- modification d’en-tête sans instruction explicite

---

## 🔒 Distinction contractuelle : modification vs création

### A) Modification d’existant (régime standard)

La modification d’un fichier existant est autorisée uniquement si :

- le fichier source **complet** est fourni,
- le périmètre de modification est explicitement défini,
- la structure Arsenal est strictement conservée,
- l’en-tête existant est respecté **sans extension de périmètre**.

---

### B) Création (régime renforcé — Option B)

La création est autorisée uniquement si :

- l’utilisateur demande explicitement une **création**,
- ChatGPT applique une phase préalable de **pré-validation** (cf. `mode_operatoire.md`),
- la structure, le nommage et le dossier cible sont validés **avant toute génération exécutable**,
- un **en-tête Arsenal conforme** est produit et validé.

Aucune création implicite n’est autorisée  
(aucun “j’ajoute aussi…”, aucun objet connexe non demandé).

---

## 🛑 Interdictions absolues (invariants)

ChatGPT ne doit **jamais** :

1. **Renommer** une entité existante (`entity_id`) ou “corriger” un nom.
2. Modifier un `id:` d’automatisation défini par l’utilisateur.
3. Modifier un `alias`, une casse, un libellé, ou introduire des accents
   dans des clés techniques lorsque cela a été interdit dans Arsenal.
4. Changer la **structure d’include** d’un dossier
   (ex. `!include_dir_merge_list` ↔ `!include_dir_merge_named`).
5. Reformater ou “nettoyer” un YAML complet sans demande explicite.
6. Déplacer des blocs entre fichiers, fusionner ou éclater des fichiers,
   sans instruction explicite.
7. Ajouter des fonctionnalités, triggers, conditions, services ou entités
   non demandés.
8. Remplacer une logique métier par une autre
   (“simplification”, “optimisation”, “meilleure approche”).
9. Déclarer qu’un résultat est “validé”, “robuste”, “stable”, “sans risque”
   ou “fonctionnera” sans validation terrain.
10. Générer, calculer, proposer ou deviner un `id:` d’automatisation.
11. Déduire un préfixe d’ID à partir d’un domaine fonctionnel ou d’un nom.
12. Introduire un champ `id:` si aucune valeur explicite n’est fournie.
13. Modifier, réordonner ou normaliser un `id:` fourni.
14. Réutiliser un `id:` existant pour une nouvelle automation.
15. Modifier, réduire, reformuler ou compléter un **en-tête de fichier**
    sans instruction explicite.

👉 En l’absence d’un `id:` fourni pour une automation,
ChatGPT **s’arrête immédiatement**.

Toute violation invalide la sortie.

---

## 🧱 En-têtes de fichiers (contrats locaux)

Tout fichier Arsenal est précédé d’un **en-tête contractuel normatif**
(cf. `en_tetes_fichiers.md`).

Règles impératives :

- l’en-tête :
  - définit le rôle exact du fichier,
  - borne strictement son périmètre,
  - liste explicitement les interdictions locales.
- le contenu du fichier :
  - ne peut jamais dépasser ce périmètre,
  - ne peut jamais contredire l’en-tête.

ChatGPT :

- respecte l’en-tête existant **sans interprétation**,
- n’en modifie aucun élément par défaut,
- ne crée un en-tête qu’en cas de création validée (Option B).

---

## 🧾 Nommage des entités (contrainte UX et stabilité)

Toute création d’entité doit respecter strictement `nommage_entites.md`.

Règles opposables :

- la grandeur en premier,
- la zone en dernier,
- aucun terme technique parasite,
- vocabulaire Arsenal canonique uniquement.

En cas de doute (grandeur, zone, qualificatif),
ChatGPT **s’arrête** et demande clarification.

---

## ⏱️ Robustesse au reload YAML (invariant défensif)

La robustesse au reload est **non négociable**
(cf. `principes_generaux.md`).

Conséquences :

- éviter toute dépendance fragile à l’ordre de chargement,
- traiter explicitement `unknown` / `unavailable` si pertinent,
- ne jamais introduire de fragilité connue ou probable.

En cas de doute :
👉 ChatGPT signale le risque et **s’arrête**.

---

## ✅ Exigences de sortie

Toute sortie YAML exécutable doit être :

- complète,
- copiable telle quelle,
- strictement conforme à la structure d’include,
- sans texte parasite,
- strictement limitée au périmètre demandé.

Si une information manque
(chemin, statut création/modification, indentation, entités, ID),
ChatGPT **ne produit rien** et demande l’élément manquant.

---

## 🛑 Causes d’invalidation immédiate

La sortie est invalide si elle contient :

- une création implicite,
- une hypothèse non signalée,
- un renommage non demandé,
- une modification d’en-tête non autorisée,
- une fragilité reload introduite,
- une extrapolation ou promesse de fonctionnement,
- du contenu hors périmètre.

---

## 📌 Statut

- Document contractuel Arsenal
- Normatif et opposable
- Stable par défaut

Toute dérogation doit être :
- explicitement demandée,
- clairement localisée,
- documentée.
