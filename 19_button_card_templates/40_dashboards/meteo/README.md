# `40_dashboards/meteo/` — Architecture UI

## Nature du dossier

`meteo/` est un **dashboard transversal de lecture environnementale qualifiée**, couvrant des KPI physiques directs (CO₂, humidité, température), des comparaisons de cohérence locale (Δ zone) et des indicateurs météo extérieurs à seuils.

Ce n'est pas un domaine métier unique. C'est un agrégat de signaux environnementaux, avec deux logiques de qualification distinctes :

```
qualification absolue  : valeur → seuil → couleur
qualification relative : valeur → Δ vs référence → couleur
```

> Le domaine `meteo/` ne produit aucune décision et ne pilote aucun système. Il qualifie uniquement des mesures environnementales. Les cartes du domaine météo n'affichent pas des mesures brutes neutres ; elles produisent toujours une qualification diagnostique. Il n'y a pas de couche action, pas de couche décision, pas de couche état réel vs logique.

---

## Structure implicite identifiée

Le dossier est organisé en **2 familles UI distinctes** :

### A. Diagnostic à seuils (qualification absolue)

Exemples : `carte_co2_seuils_variables`, `carte_precipitations_seuils_variables`, `carte_precipitations_seuils_variables_tap`

- Valeur brute qualifiée via seuils (classification vert / bleu / rouge)
- Lecture métier : qualité d'air, intensité des précipitations
- **Type UI : diagnostic** (comparaison à seuils, classification métier)

---

### B. Diagnostic de cohérence (qualification relative)

Exemples : `humidite`, `temperature`

- Comparaison d'un capteur à un référentiel maître via Δ
- Qualification de la cohérence inter-capteurs d'une même zone
- Logique relative — pas un seuil absolu
- **Type UI : diagnostic** (lecture de cohérence système, Δ vs référence)

> Cette famille est distincte de la qualification absolue : elle ne mesure pas une valeur, elle mesure un **écart**. C'est un pattern Arsenal à part entière.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                    |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| diagnostic     | qualifie une mesure ou une cohérence par rapport à une référence                                | toutes les cartes du domaine                                                |
| pure           | aucune transformation *(non utilisé dans ce domaine)*                                           | —                                                                           |
| interprétative | transformation locale tolérée *(non utilisé dans ce domaine)*                                   | —                                                                           |
| action         | proxy UI d'une commande backend *(non utilisé dans ce domaine)*                                 | —                                                                           |
| info           | traçabilité technique *(non utilisé dans ce domaine)*                                           | —                                                                           |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Diagnostic à seuils     → 10_diagnostic_seuils/
Niveau 2 — Diagnostic de cohérence → 20_diagnostic_coherence/
```

2 couches — adaptées à la dualité du domaine (absolu / relatif). Les deux couches sont strictement non interchangeables : l'une qualifie une valeur, l'autre qualifie un écart.

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/meteo/

  10_diagnostic_seuils/
    carte_co2_seuils_variables.yaml
    carte_precipitations_seuils_variables.yaml
    carte_precipitations_seuils_variables_tap.yaml

  20_diagnostic_coherence/
    humidite.yaml
    temperature.yaml
```

---

## Points de fragilité documentés

### 1. Routage par nommage (`_1`, `_2`…)

Présent dans `temperature` et `humidite`. Même pattern que dans d'autres domaines — acceptable dans Arsenal, fragile si non verrouillé contractuellement dans l'entête.

### 2. Hardcode Netatmo jardin

`_jardin_1` / `_jardin_2` codés en dur dans les cartes de cohérence. Dette technique identifiée — à isoler dans l'entête.

### 3. Duplication précipitations (tap / no tap)

`carte_precipitations_seuils_variables` et `carte_precipitations_seuils_variables_tap` sont factorisables via une variable :

```yaml
variables:
  tap_action: more-info  # ou none
```

À traiter lors d'une prochaine itération — ne pas laisser diverger les deux cartes en attendant.

### 4. `seuil_ok` inutile dans `carte_co2_seuils_variables`

Paramètre sans effet dans l'API du template. Bruit à nettoyer à terme.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Ajouter le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter les points de fragilité**
Ajouter dans les entêtes : convention de nommage `_1/_2`, hardcode Netatmo jardin.

**Étape 4 — Factoriser les précipitations (optionnel)**
Fusionner `_tap` et `_no_tap` via `variables.tap_action`. Ne pas laisser les deux cartes diverger en attendant.
