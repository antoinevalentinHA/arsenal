# 🛠️ ARSENAL — CHANTIER · CH-LL-CI-2 — Géométrie des grilles Lovelace (R-LL-GRID-1 / R-LL-GRID-2)

> **Statut : CLOS (2026-07-29).** Chantier livré de bout en bout : norme mergée
> (#629) → ouverture (#630) → **G1 bloquant** (#631) → **qualification NAS**
> (#632) → **résolution NAS** (#633) → **G2 bloquant** (#635). Tous les critères
> de clôture sont satisfaits (voir plus bas). Ce document est le
> **propriétaire de suivi** du chantier ; le statut vivant est au
> [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md).

## 📌 Cadre

- **Chantier** : CH-LL-CI-2 — rendre opposable en CI la **géométrie des grilles
  Lovelace** (`type: grid`), selon les invariants normatifs `R-LL-GRID-1`
  (grilles statiques) et `R-LL-GRID-2` (grilles dynamiques).
- **Norme propriétaire** :
  [`ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md) §
  « Géométrie des grilles locales » (mergée, PR #629).
- **Origine** : audit lecture seule des grilles Lovelace (273 grilles ;
  270 statiques toutes conformes ; 3 dynamiques). La norme précède
  l'implémentation.
- **Nature de ce document** : suivi de chantier multi-lots. Aucun code n'y est
  produit ; chaque lot a sa propre PR. Ce document décrit l'**état courant** du
  chantier.

### Interdits (périmètre de l'ouverture)

- aucun checker, workflow, ni registre de couverture écrit à l'ouverture ;
- aucun dashboard, include, ni fichier NAS modifié ;
- aucune correction des grilles existantes ;
- l'ouverture ne crée/modifie que : ce document, le registre des chantiers
  ([`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)), l'index des audits
  ([`index.md`](../../index.md)).

## 🎯 Périmètre

Couvre, par lots séquentiels :

1. **G1** — contrôle bloquant de la complétude structurelle des grilles statiques ;
2. **Qualification préalable des deux grilles du NAS maison** — statut des cas
   dynamiques non encore qualifiés au regard de `R-LL-GRID-2`, **sans présumer
   d'un défaut runtime** ;
3. **G2** — contrôle bloquant de la géométrie dynamique, limité aux motifs
   statiquement démontrables ;
4. **Clôture**.

Hors périmètre (rappel de la norme) : `custom:grid-layout`,
`custom:auto-entities`, `horizontal-stack`, toute structure ne déclarant pas
`type: grid`.

## 🧱 Lots

### Lot G1 — Complétude structurelle statique (BLOQUANT)

- Checker `check_lovelace_grid_contracts.py` (slug `lovelace_grid`, contrat
  `R-LL-GRID-1`) : sur toute grille **statique démontrée**, vérifie `columns`
  déclaré, entier strictement positif, `cards` liste non vide, cellules directes
  divisibles par `columns`.
- Classification à **trois états explicites** :
  - **STATIQUE** démontrée → contrôlée par G1 ;
  - **DYNAMIQUE** reconnue (`type: conditional` enfant direct ou `visibility:`
    directe) → comptée à part, hors G1 ;
  - **NON ANALYSABLE** / classification indéterminée → **échec explicite**.
    Il est interdit de classer statique par défaut une structure non comprise.
- Garde `!include` : une entrée directe `!include` compte pour **une** cellule
  **seulement si** sa cible résout vers une **carte-racine mapping** (résolution
  relative au fichier source, sans développer l'arborescence Lovelace — la
  résolution ne sert qu'à prouver l'arité de l'entrée directe). Racine liste ou
  autre type, cible absente / illisible / non analysable → non-conformité
  explicite, jamais comptage silencieux.
- Grilles imbriquées : chaque grille est évaluée indépendamment ; une grille
  imbriquée compte pour une cellule de sa grille parente.
- Workflow `contracts_lovelace_grid.yml` bloquant, filtré `paths:` :
  `18_lovelace/**`, le checker, le workflow, **et**
  `00_documentation_arsenal/ui/pattern_dashboard.md` (le document propriétaire de
  la norme réexécute le contrôle).
- Co-commit du registre de couverture
  ([`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md)).
- **Preuve de corpus initiale** (preuve du lot, non figée dans le checker) :
  273 grilles totales, 270 statiques, 3 dynamiques, **270/270 statiques
  conformes** → exit 0.

### Lot NAS — Qualification des deux grilles du NAS maison

Cas dynamiques non encore qualifiés au regard de `R-LL-GRID-2`
(`18_lovelace/dashboards/systeme/nas.yaml`). Ce lot, **sans présumer ni défaut
ni correction** :

- identifie l'intention UI des deux grilles ;
- détermine les cardinalités effectivement possibles ;
- établit le comportement visuel produit lorsque 0, 1 ou 2 cartes sont visibles ;
- conclut **conforme**, **non conforme** ou **non démontré** au regard de
  `R-LL-GRID-2` ;
- ne modifie le YAML **que si** une incompatibilité est démontrée, et **après
  arbitrage dédié**.

Aucune activation bloquante de G2 avant qualification de ces cas.

**Qualification (2026-07-29) — grilles `nas.yaml:187` (section Disque 1) et
`:246` (section Disque 2).** Les deux grilles sont `columns: 2` avec deux cartes
`type: conditional` en enfants directs (socle `carte_alerte_binaire_critique`).

- **Intention UI** : rangée d'alertes SMART critiques par disque ; chaque carte
  n'apparaît que si son `binary_sensor` vaut `on` (« Durée de vie restante » et
  « Secteurs défectueux »).
- **Cardinalités effectivement possibles** : les deux conditions portent sur deux
  `binary_sensor` **indépendants** (aucune exclusion mutuelle ni complémentarité)
  → nombre de cellules visibles ∈ **{0, 1, 2}**.
- **Comportement visuel (`columns: 2`)** : `0` → grille vide (cardinalité nulle
  **admise**, hors périmètre) ; **`1` → rangée partiellement remplie** ; `2` →
  rangée complète.
- **Conclusion : NON CONFORME** au regard de `R-LL-GRID-2`. La cardinalité `1`
  est admissible et non divisible par `columns` (=2) ; la garantie « toute
  combinaison d'états admise divisible par `columns` » **n'est pas démontrable**
  (conditions indépendantes, aucun motif reconnu tel que « conditions
  complémentaires sur une même entité »). Incompatibilité **structurelle
  démontrée**, indépendante de l'état runtime des disques ; **aucun défaut runtime
  présumé**.

**Résolution (2026-07-29).** Sur arbitrage : les deux grilles passent en
`columns: 1` — alertes SMART **en pleine largeur** (`18_lovelace/dashboards/systeme/nas.yaml`).
Toute cardinalité admise (0, 1, 2) devient divisible par `columns` (=1) →
**conforme `R-LL-GRID-2`**, statiquement démontrable. L'affichage à l'état sain
(0 alerte) est **inchangé** ; seul le cas « 1 alerte » passe de demi- à pleine
largeur. Correction réalisée **avant** toute activation bloquante de G2.

**Observation incidente** (hors géométrie, hors `R-LL-GRID-2`, ni présumée défaut
ni corrigée) : la grille d'alertes de la section « Disque 1 » (`:187`) référence
des capteurs `…drive_2…`, comme celle de « Disque 2 » (`:246`). Signalée pour
arbitrage distinct.

### Lot G2 — Géométrie dynamique (BLOQUANT)

- Contrôle `R-LL-GRID-2` limité aux motifs **statiquement démontrables**
  (premier motif candidat : conditions complémentaires sur une même entité).
- Aucune simulation d'états Home Assistant ; aucun mécanisme de dérogation ni de
  qualification manuelle.
- **Pré-requis** : qualification préalable des deux grilles du NAS maison
  effectuée (lot NAS).

### Lot Clôture — soldé (2026-07-29)

Bilan des lots, tous livrés et mergés :
- **G1** (#631) — complétude structurelle statique bloquante (`R-LL-GRID-1`).
- **NAS** — qualification (#632, verdict non conforme au regard de `R-LL-GRID-2`,
  sans présumer de défaut runtime) puis résolution (#633, alertes SMART en
  `columns: 1` pleine largeur → conforme ; affichage sain inchangé).
- **G2** (#635) — géométrie dynamique bloquante (`R-LL-GRID-2`) par **extension**
  du checker : motifs A (`columns==1`) / B (paires complémentaires strictes sur
  une même entité) ; tout autre cas non conforme par défaut, aucune dérogation.

Garde-fou d'un invariant déjà vrai : scan réel **273 grilles · 270 statiques
(270 G1-conformes) · 3 dynamiques (3 G2-conformes) · 0 violation**.

Reste optionnel, **hors chantier** : l'observation incidente `drive_2` sous la
section « Disque 1 » de `nas.yaml` (hors géométrie, arbitrage distinct).

Registre des chantiers passé en « Clos récents ».

## ✅ Critères de clôture

- G1 bloquant en CI, base de corpus verte, registre de couverture à jour ;
- NAS maison qualifié au regard de G2 ; éventuelle incompatibilité démontrée
  traitée ou explicitement arbitrée avant activation bloquante de G2 ;
- G2 bloquant en CI sur les motifs statiquement démontrables ;
- ligne de clôture au [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md).

## 🔗 Liens

- Norme propriétaire :
  [`ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md)
- Registre de couverture CI :
  [`REGISTRE_COUVERTURE_VERIFICATION.md`](../../REGISTRE_COUVERTURE_VERIFICATION.md)
- Sibling Lovelace-CI :
  [`cadrage_ci_includes_lovelace.md`](cadrage_ci_includes_lovelace.md) (CH-LL-CI-1)
