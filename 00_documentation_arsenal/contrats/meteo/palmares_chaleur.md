# Arsenal — Contrat métier
# Palmarès historique — Journées les plus chaudes
# Version : 1.2
# Statut : normatif
# Chemin : 00_documentation_arsenal/contrats/meteo/palmares_chaleur.md

---

## 1. Objet

Définir l'instance métier Arsenal dédiée au palmarès historique
des journées les plus chaudes observées au domicile.

Le système maintient un classement persistant des 10 journées civiles
ayant atteint les plus fortes températures maximales quotidiennes.

Le présent contrat spécialise la primitive « palmarès historique »
au domaine thermique extérieur.

---

## 2. Périmètre

Le présent contrat couvre exclusivement :

- les journées les plus chaudes ;
- le domaine météo jardin ;
- le cycle journalier civil ;
- les maxima quotidiens clôturés.

Le présent contrat ne couvre pas :

- les journées les plus froides ;
- les statistiques glissantes ;
- les records hebdomadaires ;
- les records mensuels ;
- les températures intérieures ;
- les prévisions météo.

---

## 3. Source métier canonique

### 3.1 Source attendue

```text
sensor.temperature_max_journaliere_jardin
```

Cette source représente :

```text
la température maximale atteinte
sur une journée civile clôturée
(00:00:00 → 23:59:59)
```

### 3.2 Architecture de la source

La source canonique repose sur un pipeline dédié à trois couches :

| Couche | Entité | Rôle |
|---|---|---|
| Mémoire courante | `input_number.temperature_max_jour_courant_jardin` | Max en cours de journée, mis à jour sur changement source |
| Mémoire clôturée | `input_number.temperature_max_journaliere_jardin` | Valeur stable de la dernière journée civile clôturée |
| Exposition | `sensor.temperature_max_journaliere_jardin` | Interface canonique consommable par le palmarès |

### 3.3 Pipeline temporel

```text
sensor.temperature_jardin change
  → automation update → input_number.temperature_max_jour_courant_jardin

23:59:55 → snapshot palmarès
         → input_number.temperature_max_jour_courant_jardin
         → input_number.palmares_temperature_journalier_chaud_snapshot_veille

00:00:05 → clôture
         → input_number.temperature_max_jour_courant_jardin
         → input_number.temperature_max_journaliere_jardin

00:00:10 → reset
         → input_number.temperature_max_jour_courant_jardin = -999

00:00:30 → évaluation palmarès
         → input_number.palmares_temperature_journalier_chaud_snapshot_veille
```

### 3.3.1 Doctrine anti-décalage temporel

Le snapshot palmarès doit capturer la mémoire courante du jour qui
se termine, avant la clôture et avant le reset.

Il ne doit pas lire `sensor.temperature_max_journaliere_jardin`, car
ce capteur expose une valeur déjà clôturée antérieure. Le lire à
23:59:55 créerait un risque d'association entre une valeur d'un jour
et la date civile du jour suivant.

Le snapshot existe pour figer la valeur du jour civil en cours avant
les opérations de minuit.

### 3.4 Interdiction des maxima glissants

Une fenêtre glissante 24 h ne constitue pas une journée civile clôturée.

En conséquence, un capteur construit via :

```yaml
platform: statistics
state_characteristic: value_max
max_age:
  hours: 24
```

est explicitement interdit comme source métier pour le présent contrat.

### 3.5 Justification doctrinale

Un maximum glissant peut encore contenir une valeur appartenant
à la journée précédente. Cela peut produire :

- des faux records ;
- des journées historiquement incorrectes ;
- des palmarès plausibles mais faux.

---

## 4. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `sensor.temperature_jardin` | source thermique robuste instantanée | bloquant |
| `input_number.temperature_max_jour_courant_jardin` | mémoire max en cours | bloquant |
| `input_number.temperature_max_journaliere_jardin` | mémoire clôturée | bloquant |
| `sensor.temperature_max_journaliere_jardin` | exposition canonique | bloquant |

---

## 5. Paramètres d'instance

| Paramètre | Valeur |
|---|---|
| `instance_id` | `temperature_journalier_chaud` |
| source | `sensor.temperature_max_journaliere_jardin` |
| cycle | `daily` |
| top_n | `10` |
| unite | `°C` |
| seuil_fraicheur_h | `36` |
| sentinelle_vide | `-999` |
| plage_metier | `[-10, 50]°C` |
| plage_technique_helpers | `[-999, 1000]` |

---

## 6. Convention de nommage

### 6.1 Capteurs exposés

```text
sensor.palmares_temperature_journalier_chaud
binary_sensor.palmares_temperature_journalier_chaud_anomalie
```

### 6.2 Helpers de rang

```text
input_number.palmares_temperature_journalier_chaud_rang_01_valeur
input_text.palmares_temperature_journalier_chaud_rang_01_date
```

jusqu'au rang 10.

### 6.3 Helpers mécaniques

```text
input_number.palmares_temperature_journalier_chaud_snapshot_veille
input_datetime.palmares_temperature_journalier_chaud_derniere_evaluation
```

### 6.4 Source pipeline

```text
input_number.temperature_max_jour_courant_jardin
input_number.temperature_max_journaliere_jardin
sensor.temperature_max_journaliere_jardin
```

### 6.5 Réserve nomenclature future

Le suffixe `_chaud` est réservé afin de permettre une future instance
`temperature_journalier_froid` sans collision de nomenclature.

---

## 7. Invariants métier

| ID | Invariant |
|---|---|
| INV-CH-1 | La source métier représente une journée civile clôturée. |
| INV-CH-2 | Une fenêtre glissante 24 h est interdite comme source. |
| INV-CH-3 | Le palmarès ne consomme jamais une température instantanée directe. |
| INV-CH-4 | Une date civile ne peut apparaître qu'une fois dans les rangs. |
| INV-CH-5 | Les records représentent des maxima quotidiens réels observés au domicile. |
| INV-CH-6 | La sentinelle `-999` est une valeur technique, jamais une valeur métier. |
| INV-CH-7 | `sensor.temperature_max_journaliere_jardin` n'expose jamais `-999`. |
| INV-CH-8 | FIFO sur égalité : l'antériorité prime, un record égal n'évince pas l'antérieur. |

---

## 8. Doctrine d'insertion

```text
1. Snapshot invalide (-999, unknown, unavailable) → absence d'insertion
2. date_veille déjà présente dans les rangs      → abstention
3. Palmarès plein ET snapshot ≤ rang_10          → abstention (FIFO)
4. Sinon                                          → insertion, tri descendant
```

Tri : `(valeur desc, index_anteriorite asc)` — garantit FIFO sur égalité.

Une mémoire intermédiaire consommée ultérieurement par le palmarès ne
doit jamais conserver une ancienne valeur si la source du jour est
invalide. Elle doit être explicitement replacée à la sentinelle `-999`.

Cette règle s'applique notamment au snapshot palmarès : une journée
sans valeur maximale valide ne doit pas laisser subsister le snapshot
d'une journée précédente.

---

## 9. Invariants de cohérence (binary_sensor anomalie)

Évalués dans l'ordre canonique suivant :

| ID | Invariant | Raison exposée |
|---|---|---|
| B1 | Ordre descendant : `valeur[i] >= valeur[i+1]` pour tout rang rempli | `ordre_rompu_rang_NN_MM` |
| B2 | Couplage : valeur > 0 ↔ date non vide | `incoherence_couplage_rang_NN` |
| B3 | Compacité : aucun rang rempli après un rang vide | `compacite_rompue_rang_NN` |
| B4 | Fraîcheur : dernière évaluation ≤ 36 h | `evaluation_manquante` |

Exemptions B4 :

- sentinelle `1970-01-01 00:00:00` → état initial légitime, pas d'anomalie
- `unknown` / `unavailable` → `evaluation_indisponible`

La comparaison de fraîcheur doit être robuste aux différences de
représentation temporelle entre datetime naïf et datetime avec fuseau.
L'implémentation doit comparer des timestamps, et non soustraire
directement deux objets datetime potentiellement hétérogènes.

---

### 9.1 Doctrine d'implémentation Jinja

Toute accumulation construite dans une boucle Jinja doit utiliser un
`namespace`.

La forme suivante est interdite pour construire une liste persistante
hors boucle :

```jinja
{% set paires = paires + [...] %}
```

La forme attendue est : 

```jinja
{% set ns = namespace(paires=[]) %}
{% set ns.paires = ns.paires + [...] %}
```

Cette règle évite la perte silencieuse des rangs existants lors de
l'évaluation du palmarès.

---

## 10. Précondition bloquante

Le système ne doit pas être considéré opérationnel tant que
`sensor.temperature_max_journaliere_jardin` n'est pas disponible
(non `unavailable`).

En l'absence d'une mémoire explicite de date de clôture, le capteur
d'exposition ne doit pas publier d'attribut `date_journee_cloturee`
calculé implicitement. Une telle date serait une déduction temporelle,
non une donnée clôturée mémorisée.

---

## 11. Recorder

### Population A

| Entité | Contrainte |
|---|---|
| `sensor.temperature_max_journaliere_jardin` | Source métier canonique historisée pour audit, relecture temporelle et cohérence des maxima clôturés |

### Population B

21 entités : 10 `input_number` valeurs + 10 `input_text` dates + 1 `input_datetime` dernière évaluation.

Fréquence : ≤ 1 écriture/jour par entité. Cardinalité finie. Logbook acceptable.

---

## 12. Hors périmètre

- les journées les plus froides ;
- les minima journaliers ;
- les records glissants ;
- les records saisonniers ou annuels ;
- les températures intérieures ;
- les statistiques Recorder ;
- les prévisions météo.

---

## 13. Extensions futures envisagées

- instance `temperature_journalier_froid` (nomenclature réservée) ;
- records hebdomadaires / mensuels / saisonniers ;
- dashboards records météo ;
- badges records historiques ;
- alertes record absolu.

Aucune de ces extensions n'a de valeur normative en v1.2.

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-05-26 | Brouillon normatif initial |
| 1.1 | 2026-05-26 | Architecture source formalisée (pipeline 3 couches), sentinelle -999, FIFO documenté, invariants B1-B4 avec exemption sentinelle 1970 |
| 1.2 | 2026-05-27 | Durcissement anti-stale data : snapshot palmarès fondé sur la mémoire courante, interdiction des dates de clôture implicites sans mémoire dédiée, clarification de l'invalidation par sentinelle, robustesse B4 par comparaison timestamp, et doctrine Jinja `namespace` pour l'accumulation des rangs. |