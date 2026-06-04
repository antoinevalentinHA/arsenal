# `40_dashboards/climatisation/` — Architecture UI

---

## Nature du dossier

`climatisation/` est un **dashboard métier décisionnel multi-modes**.

Il expose :

- l’**intention du moteur de décision climatisation**,
- le **mode réellement actif**,
- la **cohérence entre décision et exécution**,
- les **contraintes externes bloquantes**,
- les **conditions d’éligibilité des modes**.

Ce n’est ni une UI technique brute, ni une UI simplifiée utilisateur.

C’est une **UI métier orientée décision, contraintes et activation conditionnelle**.

---

## Principes structurants

### UI ≠ décision

Aucune carte ne décide.

- la décision est produite par le backend (`sensor.clim_mode_local`, `sensor.clim_intention`, etc.)
- la UI lit, interprète, confronte

---

### Système multi-modes

La climatisation fonctionne par **modes discrets** :

- `cool`
- `dry`
- `heat`
- `off`

La UI doit :
- représenter ces modes,
- rester cohérente quel que soit le mode actif.

---

La climatisation étant réversible, le domaine inclut
des logiques de chauffage (mode HEAT).

Certaines cartes peuvent donc exposer des conditions
de chauffe (besoin thermique, blocages aération),
sans relever du domaine `chauffage/`.

Ces cartes sont interprétées comme :

→ conditions d’éligibilité ou contraintes du mode HEAT

---

### Contraintes explicites

Le système est fortement contraint :

- aération
- fenêtres ouvertes
- blocages horaires
- post-aération

Ces contraintes sont :
> **visibles, explicites, jamais implicites**

---

### Éligibilité (concept central)

Contrairement au chauffage, la clim introduit une couche explicite :

> **conditions d’éligibilité**

Exemples :
- humidex suffisant → DRY éligible
- température extérieure → COOL autorisé
- température intérieure → déclenchement possible
- présence / babysitting → autorisation

---

### Sémantique couleur spécifique

Dans ce domaine :

| Couleur | Signification |
|--------|--------------|
| 🟢 vert | condition remplie / éligible / actif |
| ⚪ gris | non requis / non applicable / contrainte |
| 🔴 rouge | incohérence ou blocage global |
| 🔵 bleu | activité (cool principalement) |
| 🟠 orange | état indéterminé ou blocage explicite |

> ⚠️ Le vert ne signifie pas toujours “nominal”  
> → il signifie souvent **“condition remplie”**

---

## Familles UI

---

### 1. Statut métier / décision

Cartes exposant l’intention ou le mode décidé.

**Type UI : interprétative**

Exemples :

- `clim_decision_synthetique_72`
- `carte_clim_synthese`
- `clim_synthese_status_72`

Rôle :

- afficher le mode ou l’intention
- rendre lisible la décision backend
- sans confrontation au réel

---

### 2. Diagnostic décisionnel

Cartes évaluant la cohérence ou l’état logique.

**Type UI : diagnostic**

Exemples :

- `carte_clim_decision` ✅ **CARTE PIVOT**
- `carte_clim_diagnostic_aeration_etage`
- `carte_clim_diagnostic_fenetres_maison`
- `carte_clim_diagnostic_presence_babysitting`
- `carte_clim_diagnostic_chauffage_hiver_actif`

Rôle :

- confronter état réel / raison
- qualifier les contraintes
- rendre explicite le contexte décisionnel

---

### 3. Contraintes / blocages

Cartes de synthèse des blocages.

**Type UI : agrégative**

Exemples :

- `clim_blocages_synthese_xl`

Rôle :

- agréger plusieurs blocages
- fournir une lecture globale

---

### 4. Conditions d’éligibilité

Cartes évaluant si un mode peut être activé.

**Type UI : interprétative**

Exemples :

- `carte_clim_diagnostic_humidex_max_chambres`
- `carte_clim_diagnostic_temperature_exterieure_hiver`
- `carte_clim_diagnostic_temperature_exterieure`
- `carte_clim_diagnostic_temperature_min_chambres`
- `carte_clim_diagnostic_extinction_temperature_min_chambres`

Rôle :

- comparer mesure vs seuil
- indiquer si une action est possible

> Ces cartes sont centrales dans la logique clim.

---

## Taxonomie des types UI

| Type UI | Signification |
|--------|--------------|
| `interprétative` | transformation locale sans autorité |
| `diagnostic` | qualification d’un état ou d’une cohérence |
| `agrégative` | synthèse multi-signaux |
| `info` | (peu présent ici) information brute |
| `action` | absent |

---

## Architecture en couches

```text
20_statut_metier/
    ↓
30_diagnostic/
    ↓
40_contraintes/
    ↓
50_eligibilite/
````

### Lecture

1. **Statut**
   → intention / mode

2. **Diagnostic**
   → cohérence et contexte

3. **Contraintes**
   → blocages explicites

4. **Éligibilité**
   → conditions d’activation

---

## Structure cible

```text
40_dashboards/climatisation/

  20_statut_metier/
    clim_decision_synthetique_72.yaml
    carte_clim_synthese.yaml
    clim_synthese_status_72.yaml

  30_diagnostic/
    carte_clim_decision.yaml
    carte_clim_diagnostic_aeration_etage.yaml
    carte_clim_diagnostic_fenetres_maison.yaml
    carte_clim_diagnostic_presence_babysitting.yaml
    carte_clim_diagnostic_chauffage_hiver_actif.yaml

  40_contraintes/
    clim_blocages_synthese_xl.yaml
    carte_diagnostic_chauffage_blocage_aeration.yaml

  50_eligibilite/
    carte_clim_diagnostic_humidex_max_chambres.yaml
    carte_clim_diagnostic_temperature_exterieure_hiver.yaml
    carte_clim_diagnostic_temperature_exterieure.yaml
    carte_clim_diagnostic_temperature_min_chambres.yaml
    carte_clim_diagnostic_extinction_temperature_min_chambres.yaml
    carte_diagnostic_besoin_chauffe_temperature_min_chambres.yaml
```

---

## Règles spécifiques

### 1. Décision vs synthèse

* `carte_clim_decision` → cohérence décision / réel
* `carte_clim_synthese` → état local

❌ non interchangeables

---

### 2. Contrainte ≠ erreur

* fenêtre ouverte
* aération
* babysitting

→ **gris**, jamais rouge

---

### 3. Vert = éligible

Dans les cartes d’éligibilité :

* vert = seuil atteint
* pas vert = non requis

---

### 4. Blocage global

* rouge réservé aux **synthèses de blocage**
* pas aux contraintes unitaires

---

### 5. Multi-mode

Certaines cartes changent de comportement selon :

```yaml
variables.kind
```

→ abstraction nécessaire au domaine clim

---

### 6. Détection par préfixe

Exemple :

```text
blocage_*
```

→ toute nouvelle valeur est automatiquement couverte

---

### 7. Dépendance forte aux seuils backend

Les cartes d’éligibilité reposent sur :

* `input_number`
* ou `sensor.*_applique`

→ la logique métier reste **hors UI**

---

## Cartes pivots

### `carte_clim_decision`

```yaml
# ⚠️ CARTE PIVOT : cohérence état réel / raison
```

---

## Points de vigilance

### 1. Sémantique couleur non uniforme

* vert ≠ toujours nominal
* gris ≠ toujours neutre

→ normal mais doit rester documenté

---

### 2. Hétérogénéité des seuils

* parfois `input_number`
* parfois `sensor`

→ dette de symétrie acceptable

---

### 3. Logique dupliquée

* `clim_synthese_status_72`

→ duplication JS à surveiller

---

### 4. Couplage chauffage

Exemple :

* `chauffage_blocage_aeration` utilisé

→ couplage transverse assumé

---

### 5. Intrusions chauffage (à corriger)

```text
carte_diagnostic_besoin_chauffe_temperature_min_chambres
carte_diagnostic_chauffage_blocage_aeration
```

❌ à déplacer vers `chauffage/`

---

## Positionnement Arsenal

| Domaine   | Rôle                                  |
| --------- | ------------------------------------- |
| chauffage | régulation thermique continue         |
| clim      | activation conditionnelle multi-modes |
| aeration  | contrainte environnementale           |
| boiler    | exécution physique                    |

---

## Conclusion

Le domaine `climatisation/` constitue :

> **un système décisionnel sous contraintes avec activation conditionnelle**

Il est structuré par :

* modes
* cohérence
* contraintes
* éligibilité

Sa complexité est maîtrisée car :

* les responsabilités sont bien séparées
* la UI reste non décisionnelle
* les contraintes sont explicites
* les conditions d’activation sont visibles

Toute simplification masquerait des règles métier essentielles.

```
```
