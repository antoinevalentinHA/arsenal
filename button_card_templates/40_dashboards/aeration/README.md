# `40_dashboards/aeration/` — Architecture UI

## Structure implicite identifiée

Le dossier est organisé en **5 familles UI distinctes** :

### A. Cartes binaires métier simples

Exemples : `carte_aeration_preferable`, `carte_pluie`

- 1 entité / 1 état / 1 mapping couleur+libellé
- Traduction directe d'un état backend
- **Type UI : pure** (aucune transformation)

→ Famille saine et canonique. À conserver telle quelle.

---

### B. Cartes de mesure évaluée

Exemples : `carte_delta_ha`, `carte_delta_t`, `carte_duree_aeration`

- Valeur numérique + interprétation par seuil
- Classification couleur (seuil statique ou dynamique)
- **Type UI : interprétative** (transformation locale, non autoritative)

→ Bloc à factoriser en priorité. Même pattern, même logique, même risque de divergence.

---

### C. Cartes de synthèse d'état (format 72)

Exemples : `aeration_synthese_72`, `aeration_episode_status_72`

- `synthese_72` → état global du système aération
- `episode_status_72` → état opérationnel détaillé d'un épisode
- **Type UI : agrégative** (combinaison de signaux)

> ⚠️ Ces deux cartes ne sont pas exactement sur la même couche. Voir structure cible.

→ Famille cohérente. À structurer, pas à fusionner.

---

### D. Cartes de contexte thermique (format 72)

Exemples : `aeration_deltat_chute_72`, `aeration_reference_thermique_72`

- Lecture du contexte thermique d'un épisode (ΔT, référence, blocage)
- Ce n'est pas "thermique global" — c'est du **contexte d'analyse interne au domaine aération**
- Lié à l'épisode, au blocage, à l'analyse ΔT
- **Type UI : interprétative / contexte métier**

→ Sous-domaine métier spécifique. À isoler clairement.

---

### E. Carte de supervision agrégée (XL)

Exemple : `chauffage_blocage_aeration_xl`

- Synthèse riche multi-entités
- **Type UI : supervision** (synthèse multi-entités riche)

→ À part. Ne pas mélanger avec le reste.

---

## Taxonomie des types UI

| Type UI        | Signification                           | Exemples                                    |
|----------------|-----------------------------------------|---------------------------------------------|
| pure           | aucune transformation                   | `carte_pluie`, `carte_aeration_preferable`  |
| interprétative | transformation locale, non autoritative | `delta_t`, `delta_ha`, `duree`              |
| agrégative     | combinaison de signaux                  | `synthese_72`, `episode_status_72`          |
| supervision    | synthèse multi-entités riche            | `blocage_xl`                                |

> Le libellé "UI uniquement (aucune décision)" présent dans certains entêtes est **inexact** pour les cartes interprétatives et agrégatives, qui embarquent des seuils, classifications ou priorités. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

Le dossier exprime implicitement un **pipeline UI à 5 niveaux** :

```
Niveau 1 — État brut          → 10_etat/
Niveau 2 — Mesure interprétée → 20_mesures/
Niveau 3 — Synthèse           → 30_synthese/
Niveau 4 — Contexte métier    → 40_contexte_thermique/
Niveau 5 — Supervision        → 90_supervision/
```

Cette structure était déjà présente implicitement. L'objectif est de la rendre explicite sans rupture.

---

## Structure cible recommandée

```
40_dashboards/aeration/

  10_etat/
    carte_aeration_preferable.yaml
    carte_pluie.yaml

  20_mesures/
    carte_delta_ha.yaml
    carte_delta_t.yaml
    carte_duree_aeration.yaml

  30_synthese/
    aeration_synthese_72.yaml

  31_statut/
    aeration_episode_status_72.yaml

  40_contexte_thermique/
    aeration_deltat_chute_72.yaml
    aeration_reference_thermique_72.yaml

  90_supervision/
    chauffage_blocage_aeration_xl.yaml
```

> `30_synthese/` et `31_statut/` peuvent être fusionnés si la distinction état global / état opérationnel n'est pas jugée utile à ce stade.

---

## Problème ouvert : bloc `20_mesures/`

`delta_ha`, `delta_t`, `duree` partagent le même pattern. Deux options, **mutuellement exclusives** :

**Option A — Duplication assumée**
Chaque carte reste indépendante. La duplication est acceptée et maîtrisée. Pas de patron commun.

**Option B — Pattern structurel commun**
Un patron explicite est formalisé (variables, seuils, mapping couleur). Les cartes en dérivent.

> Ne pas rester entre les deux : choisir une option et la tenir. La zone grise entraîne une divergence progressive.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Ajouter `TYPE UI` dans les entêtes**

```yaml
# 🧱 TYPE UI : mesure
```

**Étape 3 — Trancher sur `20_mesures/`**
Choisir entre duplication assumée et pattern factorisé. Appliquer.

**Étape 4 — Doctrine (optionnel)**
Formaliser la taxonomie UI (pure / interprétative / agrégative / supervision) comme référence Arsenal transverse.
