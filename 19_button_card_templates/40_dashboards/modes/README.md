# `40_dashboards/modes/` — Architecture UI

## Nature du dossier

`modes/` est un **dashboard métier de gouvernance domestique**, centré sur les modes explicites commandables, les modes de synthèse, les modes dérivés / conditionnels et leurs justifications.

Ce n'est pas un domaine de mesure physique ni d'exécution technique. C'est une **UI de lecture et de commande d'états logiques de la maison**, structurée autour de deux classes de modes distinctes :

- **modes commandables** : pilotés directement par l'utilisateur (babysitting)
- **modes calculés / conditionnels** : résultat de conditions réunies (vacances)

La structure du domaine est :

```
commande → état / synthèse → diagnostic conditionnel → justification
```

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Modes commandables (pilotage)

Exemple : `carte_mode_babysitting_synthese`

- Toggle explicite, confirmation, navigation de réglage en hold
- Lecture d'état intégrée en retour visuel
- **Type UI : action** (proxy UI d'une commande backend)

> À distinguer absolument des cartes de lecture seule. Le nom contient "synthese" mais il s'agit d'une carte de commande — la sémantique prime sur le nommage.

---

### B. Modes de synthèse / état global

Exemple : *(aucune carte n'implémente actuellement cette famille)*

- Réduction forte du mode maison : `normal → vert`, tout le reste → autre
- Lecture simplifiée, non exhaustive — perte d'information assumée
- **Type UI : interprétative** (transformation locale, non source de vérité système)

> Synthèse visuelle rapide, pas une lecture complète de l'état. À documenter comme tel dans l'entête.

---

### C. Diagnostic conditionnel de mode

Exemple : `carte_vacances_decision`

- État binaire contextualisé par la raison active
- Lecture des conditions réunies ou du blocage en cours
- **Type UI : diagnostic** (qualification d'état + conditions actives)

→ Carte pivot du domaine dans ce lot.

---

### D. Justification / contexte de mode

Exemple : `carte_vacances_justification`

- Expose la raison active seule, sans qualification d'état
- Couleur fixe non sémantique
- **Type UI : info** (contextualisation satellite)

> Carte satellite de `carte_vacances_decision`. Ne doit pas être utilisée seule — son rattachement à la carte parente est obligatoire.

```yaml
# 🔗 SATELLITE DE : carte_vacances_decision
```

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                              |
|----------------|--------------------------------------------------------------------------------------------------|---------------------------------------|
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | —                                     |
| diagnostic     | qualifie un état conditionnel ou une cohérence                                                  | `carte_vacances_decision`             |
| action         | proxy UI d'une commande backend                                                                  | `carte_mode_babysitting_synthese`     |
| info           | contextualise ou justifie, sans qualification d'état                                            | `carte_vacances_justification`        |
| pure           | aucune transformation *(non utilisé dans ce domaine)*                                           | —                                     |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes diagnostic et interprétatives. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action              → 10_action/
Niveau 2 — Synthèse / Statut   → 20_statut/
Niveau 3 — Diagnostic          → 30_diagnostic/
Niveau 4 — Justification       → 40_info/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/modes/

  10_action/
    carte_mode_babysitting_synthese.yaml

  30_diagnostic/
    carte_vacances_decision.yaml

  40_info/
    carte_vacances_justification.yaml
```

---

## Points de fragilité documentés

### 1. `carte_vacances_justification` — satellite non rattaché

Doit être explicitement liée à `carte_vacances_decision` dans son entête. Une carte `info` sans carte parente documentée est une dette documentaire.

### 2. `carte_mode_babysitting_synthese` — nommage trompeur

Le suffixe `_synthese` évoque une carte de lecture. C'est une carte de commande. À clarifier dans l'entête pour éviter une mauvaise catégorisation future.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Ajouter le champ `TYPE UI` normalisé et, pour `carte_vacances_justification`, le rattachement satellite :

```yaml
# 🧱 TYPE UI : info
# 🔗 SATELLITE DE : carte_vacances_decision
```

**Étape 3 — Documenter les points de fragilité**
Ajouter dans les entêtes : nommage trompeur (`babysitting_synthese`), synthèse non exhaustive (`mode_maison_synthese`).
