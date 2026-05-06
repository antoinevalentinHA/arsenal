# `40_dashboards/eclairage/` — Architecture UI

## Nature du dossier

`eclairage/` est un **dashboard métier orienté interaction utilisateur**, centré sur le pilotage direct et la lecture d'intention d'automatisation.

Ce n'est pas un domaine de régulation physique ni d'observabilité technique. Il n'y a pas de capteur pivot, pas de diagnostic, pas de couche décision visible — la décision est déjà digérée en intention lisible. La structure du domaine est :

```
intention → action
```

---

## Structure implicite identifiée

Le dossier est organisé en **2 familles UI distinctes** :

### A. Actions utilisateur (pilotage)

Exemples : `carte_action_eclairage`, `carte_action_eclairage_script`

- **Type UI : action** (proxy UI d'une commande backend)

Deux sous-types distincts dans cette famille :

**Action observable** (`carte_action_eclairage`)
- Action sur `light.*`
- État visible en retour
- Confirmation possible
- Action + état implicite

**Action non observable** (`carte_action_eclairage_script`)
- Pas d'entity associée
- Pas d'état visible
- Pure impulsion — aucun feedback, aucune vérité système

> Cette distinction est fondamentale Arsenal : **action observable ≠ action non observable**. `carte_action_eclairage_script` ne doit jamais être généralisée comme modèle de carte d'action — son absence d'observabilité est une exception documentée, pas une norme.

---

### B. Intention / autorisation (headers contextuels)

Exemples : `carte_garage_intention_eclairage`, `carte_jardin_intention_eclairage`

- Mapping de valeurs backend vers libellé métier avec sémantique enrichie
- Non interactif — structurel (bandeau de contexte)
- **Type UI : interprétative** (transformation locale, non source de vérité système)

> Le mapping jardin affiche la valeur brute si inconnue — choix correct : évite de masquer un bug backend ou une valeur non encore gérée.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                        |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| pure           | aucune transformation *(non utilisé dans ce domaine)*                                           | —                                                               |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `carte_garage_intention_eclairage`, `carte_jardin_intention_eclairage` |
| action         | proxy UI d'une commande backend                                                                  | `carte_action_eclairage`, `carte_action_eclairage_script`       |
| diagnostic     | qualifie la cohérence du système *(non utilisé dans ce domaine)*                                | —                                                               |
| info           | traçabilité technique *(non utilisé dans ce domaine)*                                           | —                                                               |

> L'absence de couches `diagnostic`, `décision` et `capteur` est intentionnelle et correcte — le domaine ne le nécessite pas.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action     → 10_action/
Niveau 2 — Intention  → 20_intention/
```

2 couches — adaptées à la nature interaction du domaine.

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/eclairage/

  10_action/
    carte_action_eclairage.yaml
    carte_action_eclairage_script.yaml

  20_intention/
    carte_garage_intention_eclairage.yaml
    carte_jardin_intention_eclairage.yaml
```

---

## Points de fragilité documentés

### 1. `carte_action_eclairage_script` — absence d'observabilité

Aucun feedback, aucune vérité système. Acceptable en tant qu'exception explicitement documentée. Ne pas généraliser comme modèle de carte d'action.

### 2. Headers avec styles codés en dur

Les cartes d'intention utilisent des styles `name` en dur (taille, couleur). Légère entorse au principe socle, acceptable en exception documentée : usage strictement limité au rôle de bandeau structurel, cohérence maintenue entre les deux cartes.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Remplacer "UI uniquement (aucune décision)" par le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : action
```

**Étape 3 — Documenter les points de fragilité**
Ajouter dans l'entête de `carte_action_eclairage_script` : absence d'observabilité, usage en exception, non généralisable.
