# 🏗️ Architecture — Arsenal Home Assistant

## 🎯 Objet de ce dossier

Le dossier `architecture/` décrit les **choix architecturaux techniques**
du système **Arsenal Home Assistant**.

Il explicite **comment** le système est construit,
**pourquoi** certaines décisions ont été prises,
et **quelles règles techniques sont non négociables**.

Ces documents constituent la **référence d’implémentation** du système Arsenal.


## 📐 Périmètre

Les documents présents ici décrivent :

- l’architecture des sous-systèmes (ex : éclairage jardin),
- les principes techniques transversaux,
- les doctrines d’implémentation Home Assistant,
- les règles de robustesse, de résilience et de non-régression.

Ils ne décrivent **pas** :
- l’intention utilisateur,
- les règles métier fonctionnelles,
- les scénarios d’usage.

👉 Ces éléments relèvent des **contrats fonctionnels**.


## 🧠 Positionnement dans la documentation Arsenal

La documentation Arsenal est structurée en couches distinctes :

- **Contrats fonctionnels**
  - décrivent l’intention utilisateur
  - indépendants de toute implémentation

- **Architecture (ce dossier)**
  - décrit la traduction technique des contrats
  - fixe les invariants d’implémentation
  - garantit la cohérence et la robustesse du système

- **Changelog**
  - trace les consolidations successives
  - documente l’évolution du système dans le temps

Aucun document d’architecture ne doit modifier
ou redéfinir une intention utilisateur.


## 🧱 Principes architecturaux globaux

L’architecture Arsenal repose sur les principes suivants :

- séparation stricte des responsabilités :
  - décision métier
  - contexte d’exécution
  - réaction événementielle
  - action matérielle
- capteurs = vérité métier
- automatisations = réactions, jamais décisions
- scripts = autorité unique sur le matériel
- décisions déterministes, stateless et recalculables
- robustesse explicite aux redémarrages Home Assistant
- absence totale de polling non justifié

Ces principes sont détaillés et normés dans :
- [`03_doctrines/principes_generaux.md`](03_doctrines/principes_generaux.md)


## 📂 Contenu du dossier

Ce dossier est organisé en sous-dossiers thématiques et en documents
d’architecture par sous-système à la racine.

Sous-dossiers principaux :
- `03_doctrines/` — doctrines d’implémentation transversales Arsenal
- `00_structure_includes/` · `01_recorder/` · `02_etiquettes/` — infrastructure
- `chauffage/` · `presence/` · … — architectures de sous-systèmes (liste non exhaustive)

Exemples de documents doctrines :

- [`03_doctrines/principes_generaux.md`](03_doctrines/principes_generaux.md)  
  Principes architecturaux transversaux applicables
  à l’ensemble du système Arsenal.

- [`03_doctrines/gestion_du_temps.md`](03_doctrines/gestion_du_temps.md)  
  Doctrine officielle concernant l’usage du temps
  dans Home Assistant (interdits, usages autorisés,
  règles de sobriété et de déterminisme).

Exemple de document par sous-système :

- `eclairage_jardin.md`  
  Architecture détaillée de l’éclairage automatique
  du jardin (MATIN / SOIR).


## 🛡️ Statut des documents

Les documents de ce dossier sont :

- **normatifs**
- **stables**
- **opposables** à toute implémentation future

Toute modification :
- doit être volontaire,
- explicitement justifiée,
- alignée avec les principes Arsenal existants,
- traçable dans le changelog officiel.


## 🧭 Règle d’or

> Une implémentation conforme au contrat fonctionnel
> mais non conforme à l’architecture Arsenal
> est considérée comme invalide.

Ce dossier constitue donc la **clé de voûte technique**
du système Arsenal Home Assistant.
