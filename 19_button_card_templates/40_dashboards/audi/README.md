# `40_dashboards/audi/` — Architecture UI

## Nature du dossier

`audi/` est un **dashboard métier spécialisé véhicule**, centré sur l'état du véhicule, l'autonomie, la batterie, la charge et quelques informations de contexte.

Contrairement à `arsenal/` (cockpit transverse), il s'agit ici d'une **lecture métier spécialisée d'un sous-système unique**.

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Cartes de seuils / évaluation quantitative

Exemples : `carte_autonomie_seuils_variables`, `carte_batterie_seuils_variables`

- Valeur numérique qualifiée selon des seuils variables
- Production d'une lecture de risque lisible
- **Type UI : interprétative** (transformation locale, non source de vérité système)

Ces deux cartes sont sœurs : même socle, même pattern, même logique d'évaluation, même risque de divergence. Bloc le plus structurant du lot — voir problème ouvert ci-dessous.

---

### B. Cartes d'état binaire véhicule

Exemple : `audi_etat_capteur`

- État binaire avec sémantique véhicule
- **Type UI : pure**

> La sémantique `off = nominal` est une convention constitutive du template. Elle fait partie de sa définition et ne doit pas être modifiée localement. Ce template est spécifique au domaine Audi — toute réutilisation dans un autre domaine doit faire l'objet d'une revalidation explicite de la sémantique.

---

### C. Cartes d'information simple

Exemples : `audi_etat_info`, `carte_duree_stationnement`

- Information non binaire, sans seuil, sans logique d'alerte
- La couleur marque uniquement "info disponible / indisponible"
- **Type UI : pure**

---

### D. Cartes d'état métier simplifié

Exemple : `carte_etat_charge_vehicule`

- Réduction volontaire du modèle d'état : en charge / non en charge / indisponible
- La carte ne permet pas de distinguer les états `idle`, `complete`, `disconnected`, etc.
- Tous les états non `charging` sont aplatis en "non en charge" — simplification assumée
- **Type UI : interprétative** (réduction documentée, perte d'information intentionnelle)

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                        |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| pure           | aucune transformation                                                                            | `audi_etat_capteur`, `audi_etat_info`, `carte_duree_stationnement` |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `carte_autonomie_seuils_variables`, `carte_batterie_seuils_variables`, `carte_etat_charge_vehicule` |
| agrégative     | combinaison de plusieurs signaux *(non utilisé dans ce domaine)*                                | —                                                               |
| action         | proxy UI d'une commande backend *(non utilisé dans ce domaine)*                                 | —                                                               |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes interprétatives. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — État              → 10_etat/
Niveau 2 — Mesures évaluées  → 20_mesures/
```

Le domaine est simple et homogène — deux couches suffisent.

---

## Structure cible recommandée

```
40_dashboards/audi/

  10_etat/
    audi_etat_capteur.yaml
    audi_etat_info.yaml
    carte_etat_charge_vehicule.yaml
    carte_duree_stationnement.yaml

  20_mesures/
    carte_autonomie_seuils_variables.yaml
    carte_batterie_seuils_variables.yaml
```

---

## Problème ouvert : bloc `20_mesures/`

`carte_autonomie_seuils_variables` et `carte_batterie_seuils_variables` partagent exactement le même pattern. Deux options, **mutuellement exclusives** :

**Option A — Duplication assumée**
Chaque carte reste indépendante. La duplication est acceptée et maîtrisée. Pas de patron commun.

**Option B — Pattern structurel commun**
Un patron explicite est formalisé (variables, seuils, mapping couleur). Les cartes en dérivent.

> Ce bloc DOIT être implémenté selon UNE SEULE des deux stratégies. Toute implémentation hybride est considérée comme non conforme.

> Même décision à prendre que pour `20_mesures/` dans `aeration/`. La stratégie choisie doit être cohérente entre les deux domaines — il s'agit du même problème d'architecture transverse.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Remplacer "UI uniquement (aucune décision)" par le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : interprétative
```

**Étape 3 — Trancher sur `20_mesures/`**
Choisir entre duplication assumée et pattern factorisé. Décision à aligner avec `aeration/`.

**Étape 4 — Documenter les points de fragilité**
Ajouter une note dans les entêtes de `audi_etat_capteur` (convention binaire, périmètre domaine) et `carte_etat_charge_vehicule` (réduction volontaire, états masqués).
