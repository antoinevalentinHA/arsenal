# `40_dashboards/arsenal/` — Architecture UI

## Nature du dossier

`arsenal/` est un **cockpit transverse de pilotage et de lecture système**.

Ce n'est ni un domaine métier, ni un fourre-tout. C'est une surface de contrôle globale donnant accès simultané aux actions critiques et à une lecture synthétique de l'état de la maison.

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Actions explicites (pilotage)

Exemples : `carte_alarme`, `carte_mode_babysitting`, `carte_action_ecs_vaisselle`, `carte_action_bonne_nuit`

- Déclenchement utilisateur explicite
- Confirmation obligatoire
- Aucune logique backend embarquée
- **Type UI : action** (proxy UI d'une commande backend)

→ Isolées structurellement des cartes de lecture (contrat UI).

---

### B. États système clés (lecture rapide)

Exemples : `carte_aeration_intention_globale`, `carte_chauffage_etat`, `carte_clim_etat`, `carte_ecs_action`, `carte_mode_maison`

- Lecture immédiate des sous-systèmes majeurs
- Abstraction suffisante pour un cockpit
- **Type UI : pure** (`carte_aeration_intention_globale`) ou **interprétative** (autres)

→ Cœur du dashboard. Bonne densité d'information, aucune dérive métier en UI.

---

### C. Analyse / synthèse transverse

Exemples : `carte_ouvertures_diagnostic`, `carte_temperature_max_chambres`, `carte_temperature_min_chambres`

- Synthèse multi-entités (ouvertures) et interprétation thermique (confort chambres)
- Vision "système" sans qualification de cohérence backend
- **Type UI : agrégative** (`carte_ouvertures_diagnostic`) ou **interprétative** (`max/min_chambres`)

→ Supervision light. Pas de décision embarquée. Cohérent avec la nature cockpit du dossier.

---

### D. KPI / Contexte visuel

Exemples : `kpi_icone_meteo`, `carte_temperature_exterieure`

- Enrichissement visuel et contexte environnemental
- **Type UI : interprétative** légère

→ Non intrusif. Bonne place dans un cockpit.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                              |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| pure           | aucune transformation                                                                            | `carte_aeration_intention_globale`                                    |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `carte_chauffage_etat`, `carte_clim_etat`, `carte_ecs_action`, températures |
| agrégative     | combinaison de plusieurs signaux                                                                 | `carte_ouvertures_diagnostic`                                         |
| action         | proxy UI d'une commande backend                                                                  | `carte_alarme`, `carte_action_bonne_nuit`                             |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes interprétatives et agrégatives. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action               → 10_action/
Niveau 2 — État système         → 20_etat_systeme/
Niveau 3 — Analyse / Diagnostic → 30_diagnostic/
Niveau 4 — KPI / Contexte       → 40_kpi_contexte/
```

---

## Structure cible recommandée

```
40_dashboards/arsenal/

  10_action/
    carte_alarme.yaml
    carte_mode_babysitting.yaml
    carte_action_ecs_vaisselle.yaml
    carte_action_bonne_nuit.yaml

  20_etat_systeme/
    carte_aeration_intention_globale.yaml
    carte_chauffage_etat.yaml
    carte_clim_etat.yaml
    carte_ecs_action.yaml
    carte_mode_maison.yaml

  30_diagnostic/
    carte_ouvertures_diagnostic.yaml
    carte_temperature_max_chambres.yaml
    carte_temperature_min_chambres.yaml

  40_kpi_contexte/
    kpi_icone_meteo.yaml
    carte_temperature_exterieure.yaml
```

---

## Points de fragilité documentés

### 1. Sémantique couleur ECS ambiguë

`sensor.temperature_ecs_couleur = red` ne distingue pas entre "critique haute" et "surchauffe". Valeurs cibles plus explicites : `cold / warm / hot / overheat`. Problème backend, pas UI.

### 2. Mode maison — simplification binaire assumée

`normal` vs tout le reste. Volontaire et lisible aujourd'hui — mais destructif en information si le système évolue. À documenter comme choix explicite dans l'entête de la carte.

### 3. Ouvertures — dépendance au naming

Détection par `"fenetre" dans entity_id`. Acceptable dans Arsenal, fragile si non documenté. À mentionner dans l'entête.

### 4. Températures confort — dépendances fortes

`max_chambres` et `min_chambres` nécessitent 5 valeurs cohérentes simultanément. Comportement en cas de capteur absent à documenter.

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
Ajouter une note dans les entêtes des cartes concernées (ECS, mode maison, ouvertures, températures).
