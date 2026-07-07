# Arsenal — Contrat métier
# Palmarès historique — Journées les plus froides
# Version : 1.0.2
# Statut : normatif
# Chemin : 00_documentation_arsenal/contrats/meteo/palmares_froid.md

---

## 1. Objet

Définir l'instance métier Arsenal dédiée au palmarès historique
des journées les plus froides observées au domicile.

Le système maintient un classement persistant des 10 journées civiles
ayant atteint les plus faibles températures minimales quotidiennes.

Le présent contrat spécialise la primitive « palmarès historique »
au domaine thermique extérieur, en miroir symétrique du contrat
`temperature_journalier_chaud`.

---

## 2. Périmètre

Le présent contrat couvre exclusivement :

- les journées les plus froides ;
- le domaine météo jardin ;
- le cycle journalier civil ;
- les minima quotidiens clôturés.

Le présent contrat ne couvre pas :

- les journées les plus chaudes (cf. contrat dédié) ;
- les statistiques glissantes ;
- les records hebdomadaires ;
- les records mensuels ;
- les températures intérieures ;
- les prévisions météo.

---

## 3. Source métier canonique

### 3.1 Source attendue

```text
sensor.temperature_min_journaliere_jardin
```

Cette source représente :

```text
la température minimale atteinte
sur une journée civile clôturée
(00:00:00 → 23:59:59)
```

### 3.2 Architecture de la source

La source canonique repose sur un pipeline dédié à trois couches :

| Couche | Entité | Rôle |
|---|---|---|
| Mémoire courante | `input_number.temperature_min_jour_courant_jardin` | Min en cours de journée, mis à jour sur changement source |
| Mémoire clôturée | `input_number.temperature_min_journaliere_jardin` | Valeur stable de la dernière journée civile clôturée |
| Exposition | `sensor.temperature_min_journaliere_jardin` | Interface canonique consommable par le palmarès |

### 3.3 Pipeline temporel

```text
sensor.temperature_jardin change
  → automation update → input_number.temperature_min_jour_courant_jardin

00:00:05 → clôture → input_number.temperature_min_journaliere_jardin
00:00:10 → reset   → input_number.temperature_min_jour_courant_jardin = 999
00:00:30 → évaluation palmarès
```

### 3.4 Interdiction des minima glissants

Une fenêtre glissante 24 h ne constitue pas une journée civile clôturée.

En conséquence, un capteur construit via :

```yaml
platform: statistics
state_characteristic: value_min
max_age:
  hours: 24
```

est explicitement interdit comme source métier pour le présent contrat.

### 3.5 Justification doctrinale

Un minimum glissant peut encore contenir une valeur appartenant
à la journée précédente. Cela peut produire :

- des faux records ;
- des journées historiquement incorrectes ;
- des palmarès plausibles mais faux.

---

## 4. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `sensor.temperature_jardin` | source thermique robuste instantanée | bloquant |
| `input_number.temperature_min_jour_courant_jardin` | mémoire min en cours | bloquant |
| `input_number.temperature_min_journaliere_jardin` | mémoire clôturée | bloquant |
| `sensor.temperature_min_journaliere_jardin` | exposition canonique | bloquant |

---

## 5. Paramètres d'instance

| Paramètre | Valeur |
|---|---|
| `instance_id` | `temperature_journalier_froid` |
| source | `sensor.temperature_min_journaliere_jardin` |
| cycle | `daily` |
| top_n | `10` |
| unite | `°C` |
| seuil_fraicheur_h | `36` |
| sentinelle_vide | `999` |
| plage_metier_source | `[-30, 30]°C` |
| plage_helpers_metier | `[-50, 50]°C` |
| plage_helpers_technique | `[-50, 1000]°C` |

### 5.1 Doctrine de la sentinelle froide

La sentinelle `999` est une valeur technique signifiant « absence métier ».
Elle doit être strictement supérieure à toute valeur métier plausible,
afin que la comparaison d'extrême (min courant) ne soit jamais piégée
au démarrage ou après reset.

Trois plages doivent être distinguées :

| Plage | Bornes | Rôle |
|---|---|---|
| `plage_metier_source` | `[-30, 30]°C` | Valeurs réelles attendues au domicile pour la source thermique |
| `plage_helpers_metier` | `[-50, 50]°C` | Marge métier robuste : tolère tout extrême plausible sans saturation |
| `plage_helpers_technique` | `[-50, 1000]°C` | Plage effective des `input_number`, étendue pour autoriser le stockage de la sentinelle `999` |

La distinction métier/technique est nécessaire car Home Assistant
refuse d'écrire dans un `input_number` toute valeur hors de ses bornes
`min`/`max`. La sentinelle `999` étant doctrinalement hors plage métier,
les bornes techniques `min: -50, max: 1000` autorisent son stockage
sans contredire la grammaire métier.

La sentinelle reste reconnaissable :

- `999 > 30` → hors `plage_metier_source` (jamais une vraie mesure)
- `999 > 50` → hors `plage_helpers_metier` (jamais un extrême plausible)
- `999 ≤ 1000` → dans `plage_helpers_technique` (stockable par HA)

Cette construction préserve l'invariant INV-FR-6 : la sentinelle est
technique, jamais métier.

### 5.2 Convention de rang vide

Pour l'instance froide :

```text
- sentinelle_vide = 999
- tout rang vide a valeur = 999 et date = ''
- toute valeur métier doit être différente de 999
- B2 = valeur != 999 ↔ date non vide
```

Cette convention rompt délibérément la symétrie avec le contrat chaud
(où le rang vide a valeur `0`). Cette rupture est nécessaire car
une valeur métier froide peut légitimement être `0`, ce qui rendrait
ambigu tout test « rang rempli ↔ valeur != 0 ».

---

## 6. Convention de nommage

### 6.1 Capteurs exposés

```text
sensor.palmares_temperature_journalier_froid
binary_sensor.palmares_temperature_journalier_froid_anomalie
```

### 6.2 Helpers de rang

```text
input_number.palmares_temperature_journalier_froid_rang_01_valeur
input_text.palmares_temperature_journalier_froid_rang_01_date
```

jusqu'au rang 10.

### 6.3 Helpers mécaniques

```text
input_number.palmares_temperature_journalier_froid_snapshot_veille
input_datetime.palmares_temperature_journalier_froid_derniere_evaluation
```

### 6.4 Source pipeline

```text
input_number.temperature_min_jour_courant_jardin
input_number.temperature_min_journaliere_jardin
sensor.temperature_min_journaliere_jardin
```

### 6.5 Symétrie avec l'instance chaude

Le suffixe `_froid` est le pendant explicite du suffixe `_chaud`
réservé par le contrat `temperature_journalier_chaud` v1.1.
Les deux instances coexistent sans collision de nomenclature.

---

## 7. Invariants métier

| ID | Invariant |
|---|---|
| INV-FR-1 | La source métier représente une journée civile clôturée. |
| INV-FR-2 | Une fenêtre glissante 24 h est interdite comme source. |
| INV-FR-3 | Le palmarès ne consomme jamais une température instantanée directe. |
| INV-FR-4 | Une date civile ne peut apparaître qu'une fois dans les rangs. |
| INV-FR-5 | Les records représentent des minima quotidiens réels observés au domicile. |
| INV-FR-6 | La sentinelle `999` est une valeur technique, jamais une valeur métier. |
| INV-FR-7 | `sensor.temperature_min_journaliere_jardin` n'expose jamais `999`. |
| INV-FR-8 | FIFO sur égalité : l'antériorité prime, un record égal n'évince pas l'antérieur. |
| INV-FR-9 | Tout rang vide a valeur `999` et date `''` — couplage strict. |
| INV-FR-10 | Le rang 1 contient la valeur la plus basse (record absolu de froid). |

---

## 8. Doctrine d'insertion

```text
1. Snapshot invalide (999, unknown, unavailable) → abstention
2. date_veille déjà présente dans les rangs      → abstention
3. Palmarès plein ET snapshot ≥ rang_10          → abstention (FIFO)
4. Sinon                                          → insertion, tri ascendant
```

Tri : `(valeur asc, index_anteriorite asc)` — garantit FIFO sur égalité.

La plus froide gagne le rang 1. Le rang 10 contient la moins froide
des journées du palmarès. Une journée plus froide que le rang 10
mérite l'insertion ; une journée égale au rang 10 ne l'évince pas
(FIFO strict).

---

## 9. Invariants de cohérence (binary_sensor anomalie)

Évalués dans l'ordre canonique suivant :

| ID | Invariant | Raison exposée |
|---|---|---|
| B1 | Ordre ascendant : `valeur[i] <= valeur[i+1]` pour tout rang rempli | `ordre_rompu_rang_NN_MM` |
| B2 | Couplage : valeur != `999` ↔ date non vide | `incoherence_couplage_rang_NN` |
| B3 | Compacité : aucun rang rempli après un rang vide | `compacite_rompue_rang_NN` |
| B4 | Fraîcheur : dernière évaluation ≤ 36 h | `evaluation_manquante` |

Un rang est considéré « rempli » si `date != ''` (autrement dit,
si `valeur != 999`). Les deux conditions sont strictement équivalentes
par INV-FR-9 ; toute divergence relève de B2.

Exemptions B4 :

- sentinelle `1970-01-01 00:00:00` → état initial légitime, pas d'anomalie
- `unknown` / `unavailable` → `evaluation_indisponible`

---

## 10. Précondition bloquante

Le système ne doit pas être considéré opérationnel tant que
`sensor.temperature_min_journaliere_jardin` n'est pas disponible
(non `unavailable`) avec une date clôturée valide dans son attribut
`date_journee_cloturee`.

---

## 11. Recorder

### Population A

| Entité | Contrainte |
|---|---|
| `sensor.temperature_min_journaliere_jardin` | Source métier canonique du palmarès froid — valeur clôturée persistante, non glissante |

### Population B

21 entités : 10 `input_number` valeurs + 10 `input_text` dates + 1 `input_datetime` dernière évaluation.

Fréquence : ≤ 1 écriture/jour par entité. Cardinalité finie. Logbook acceptable.

---

## 12. Hors périmètre

- les journées les plus chaudes (cf. contrat dédié) ;
- les maxima journaliers ;
- les records glissants ;
- les records saisonniers ou annuels ;
- les températures intérieures ;
- les statistiques Recorder ;
- les prévisions météo.

---

## 13. Extensions futures envisagées

- records hebdomadaires / mensuels / saisonniers ;
- dashboards records météo ;
- badges records historiques ;
- alertes record absolu froid (vague de froid).

Aucune de ces extensions n'a de valeur normative en v1.0.

---

## 14. Différences notables avec le contrat chaud v1.1

Cette section consigne les sept points de spécialisation où l'instance
froide ne se déduit pas mécaniquement de l'instance chaude.

| # | Point | Chaud v1.1 | Froid v1.0 |
|---|---|---|---|
| 1 | Sentinelle mémoire courante | `-999` (< toute valeur métier) | `999` (> toute valeur métier) |
| 2 | Plage physique source | `[-10, 50]°C` | `[-30, 30]°C` |
| 3 | Tri et insertion | `(valeur desc, index asc)` | `(valeur asc, index asc)` |
| 4 | Invariant B1 | `valeur[i] >= valeur[i+1]` | `valeur[i] <= valeur[i+1]` |
| 5 | Invariant B2 | `valeur > 0 ↔ date != ''` | `valeur != 999 ↔ date != ''` |
| 6 | Seuil mérite (palmarès plein) | `snapshot > rang_10` | `snapshot < rang_10` |
| 7 | Convention rang vide | valeur `0`, date `''` | valeur `999`, date `''` |

Le point 7 est doctrinalement le plus structurant : il aligne la
convention de rang vide sur la sentinelle de la mémoire courante,
établissant une grammaire unique « `999` = absence métier » pour
tout le pipeline froid.

---

## Attributs de présentation (dérivés)

Le capteur synthèse `sensor.palmares_temperature_journalier_froid` expose, en
complément des attributs canoniques, des attributs de **présentation** destinés
à l'affichage humain.

| Attribut | Nature | Format | Rôle |
|---|---|---|---|
| `rang_NN_date` | **canonique** | ISO `YYYY-MM-DD` | tri, comparaison, parsing, fraîcheur |
| `rang_NN_date_affichage` | **dérivé (présentation)** | `DD/MM/YYYY` | restitution UI uniquement |

- La date ISO `rang_NN_date` reste l'**unique donnée canonique** : toute logique
  (classement, comparaison, `strptime('%Y-%m-%d')`, fraîcheur) la consomme.
- `rang_NN_date_affichage` est une **projection de présentation** dérivée de la
  date ISO — **aucune incidence** sur le classement, les valeurs météo ou la fraîcheur.
- L'UI Lovelace affiche `rang_NN_date_affichage` **sans transformation locale**
  (pas de `strftime` / `split` / `replace` / `as_datetime` côté carte).
- Date vide ou invalide → l'attribut de présentation restitue la valeur brute
  (aucune date fabriquée).

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-05-27 | Brouillon normatif initial — miroir du contrat chaud v1.1 avec les sept points de spécialisation explicitement traités |
| 1.0.1 | 2026-05-27 | Correction §11 Population A : la phrase héritée du chaud (« fenêtre tronquée silencieusement ») était fausse pour le froid — le contrat interdit explicitement les minima glissants comme source métier (§3.4). Remplacée par la qualification correcte : source clôturée persistante, non glissante. |
| 1.0.2 | 2026-05-27 | Correction §5 — contradiction bloquante détectée : la plage helpers `[-50, 50]` rendait techniquement impossible le stockage de la sentinelle `999` (HA refuse les valeurs hors `min`/`max`). Distinction explicite désormais entre `plage_metier_source` `[-30, 30]`, `plage_helpers_metier` `[-50, 50]` et `plage_helpers_technique` `[-50, 1000]`. La sentinelle `999` reste hors plage métier (préserve INV-FR-6) mais entre dans la plage technique (stockable par HA). |
| 1.0.3 | 2026-07-07 | Ajout d'attributs de présentation dérivés `rang_NN_date_affichage` (`DD/MM/YYYY`) exposés côté backend. La date ISO `rang_NN_date` reste canonique ; aucun impact sur classement, valeurs ou fraîcheur. |
