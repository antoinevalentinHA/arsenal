# Arsenal — Contrat métier
# Palmarès historique — Nuits les plus chaudes
# (température minimale journalière la plus haute)
# Version : 1.0
# Statut : normatif
# Chemin : 00_documentation_arsenal/contrats/meteo/palmares_min_haute.md

---

## 1. Objet

Définir l'instance métier Arsenal dédiée au palmarès historique des
nuits les plus chaudes observées au domicile.

Le système maintient un classement persistant des 10 journées civiles
dont la température minimale quotidienne a été la plus ÉLEVÉE.

La grandeur classée est donc la même que celle du contrat
`temperature_journalier_froid` (le minimum journalier clôturé), mais le
classement est inversé : la valeur la plus haute gagne le rang 1.

Cette instance répond au besoin métier des épisodes de chaleur : une
température minimale journalière très élevée est un indicateur direct
d'absence de rafraîchissement nocturne, de nuit tropicale, d'accumulation
thermique du bâtiment et de stress thermique potentiel pour les occupants.

---

## 2. Périmètre

Le présent contrat couvre exclusivement :

- les nuits les plus chaudes, au sens du minimum journalier le plus haut ;
- le domaine météo jardin ;
- le cycle journalier civil ;
- les minima quotidiens clôturés.

Le présent contrat ne couvre pas :

- les journées les plus froides (cf. contrat `palmares_froid`) ;
- les journées les plus chaudes au sens du maximum (cf. contrat `palmares_chaleur`) ;
- les statistiques glissantes ;
- les records hebdomadaires, mensuels, saisonniers ou annuels ;
- les températures intérieures ;
- les prévisions météo.

---

## 3. Source métier canonique

### 3.1 Source attendue

```text
input_number.temperature_min_journaliere_jardin
```

Cette source représente :

```text
la température minimale atteinte
sur une journée civile clôturée
(00:00:00 → 23:59:59)
```

### 3.2 Réutilisation de la chaîne de capture existante

La présente instance NE DÉFINIT PAS de chaîne de capture propre. Elle
réutilise intégralement le pipeline du minimum journalier déjà en place
pour le contrat `palmares_froid` :

| Couche | Entité | Rôle |
|---|---|---|
| Mémoire courante | `input_number.temperature_min_jour_courant_jardin` | Min en cours de journée, mis à jour sur changement source |
| Mémoire clôturée | `input_number.temperature_min_journaliere_jardin` | Valeur stable de la dernière journée civile clôturée |

La grandeur classée (minimum journalier clôturé) est strictement
identique à celle du palmarès froid. Créer une seconde capture
(snapshot dédié, automation de snapshot dédiée) constituerait un
mécanisme redondant : explicitement proscrit. La présente instance se
limite à une étape d'évaluation qui LIT la mémoire clôturée.

### 3.3 Pipeline temporel

```text
sensor.temperature_jardin change
  → automation update → input_number.temperature_min_jour_courant_jardin

00:00:05 → clôture     → input_number.temperature_min_journaliere_jardin
00:00:10 → reset       → input_number.temperature_min_jour_courant_jardin = 999
00:00:30 → évaluation palmarès froid (tri ascendant)
00:00:35 → évaluation palmarès nuits chaudes (tri descendant)
```

L'évaluation de la présente instance est ordonnancée à 00:00:35, soit
APRÈS la clôture (00:00:05). À cet instant, la mémoire clôturée porte le
minimum de la journée qui vient de se terminer, et `date_veille` calculée
par `now() - 1 jour` lui correspond. L'alignement temporel est exact.

### 3.4 Robustesse de la mémoire clôturée

La mémoire clôturée s'auto-invalide à `999` lorsque la journée n'a pas
produit de mesure valide (cf. `cloture_temperature_min`, doctrine « pas
d'abstention silencieuse »). Une valeur ancienne ne peut donc pas être
associée par erreur à une nouvelle `date_veille`, ce qui prémunit contre
le « palmarès plausible mais faux ».

### 3.5 Interdiction des minima glissants

Une fenêtre glissante 24 h ne constitue pas une journée civile clôturée
et est interdite comme source, pour les mêmes raisons que le contrat
froid (§3.4/§3.5 de `palmares_froid`).

---

## 4. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `input_number.temperature_min_jour_courant_jardin` | mémoire min en cours | bloquant (pipeline partagé) |
| `input_number.temperature_min_journaliere_jardin` | mémoire clôturée — source lue | bloquant |
| `cloture_temperature_min` | alimente et invalide la mémoire clôturée | bloquant (pipeline partagé) |

---

## 5. Paramètres d'instance

| Paramètre | Valeur |
|---|---|
| `instance_id` | `temperature_min_journaliere_haute` |
| source | `input_number.temperature_min_journaliere_jardin` |
| cycle | `daily` |
| top_n | `10` |
| unite | `°C` |
| heure_evaluation | `00:00:35` |
| seuil_fraicheur_h | `36` |
| sentinelle_vide | `-999` |
| sentinelle_absence_source | `999` |
| plage_metier_source | `[-30, 30]°C` |
| plage_helpers_metier | `[-50, 50]°C` |
| plage_helpers_technique | `[-1000, 1000]°C` |

### 5.1 Doctrine des deux sentinelles

La présente instance manipule deux sentinelles distinctes, héritées de la
nature de la source et imposées par le sens du tri.

`999` — absence de mesure source. La mémoire clôturée porte `999` lorsque
la journée n'a pas produit de minimum valide. Cette valeur est filtrée par
la garde métier de l'évaluation et n'est jamais inscrite dans un rang.

`-999` — rang vide. Le tri étant descendant, un rang vide doit porter une
valeur strictement inférieure à tout minimum journalier réel afin de couler
en bas du classement. `-999` satisfait cette propriété et reste
reconnaissable comme valeur technique.

### 5.2 Convention de rang vide

Pour l'instance des nuits chaudes :

```text
- sentinelle_vide = -999
- tout rang vide a valeur = -999 et date = ''
- toute valeur métier doit être différente de -999
- B2 = valeur != -999 ↔ date non vide
```

Le rang vide ne peut PAS valoir `0`, contrairement à l'instance chaude.
Une température minimale journalière de `0 °C` est une valeur métier
parfaitement plausible en hiver ; l'utiliser comme marqueur de rang vide
rendrait ambigu tout test « rang rempli ↔ valeur != 0 ». Cette instance
applique donc, en miroir descendant, la même précaution que l'instance
froide applique en ascendant avec `999`.

### 5.3 Bornes techniques

Home Assistant refuse d'écrire dans un `input_number` toute valeur hors de
ses bornes `min`/`max`. La sentinelle de rang vide `-999` étant
doctrinalement hors plage métier, les bornes techniques `min: -1000,
max: 1000` autorisent son stockage sans contredire la grammaire métier.

La sentinelle reste reconnaissable :

- `-999 < -30` → hors `plage_metier_source` (jamais une vraie mesure)
- `-999 < -50` → hors `plage_helpers_metier` (jamais un extrême plausible)
- `-999 ≥ -1000` → dans `plage_helpers_technique` (stockable par HA)

---

## 6. Convention de nommage

### 6.1 Capteurs exposés

```text
sensor.palmares_temperature_min_journaliere_haute
binary_sensor.palmares_temperature_min_journaliere_haute_anomalie
```

### 6.2 Helpers de rang

```text
input_number.palmares_temperature_min_journaliere_haute_rang_01_valeur
input_text.palmares_temperature_min_journaliere_haute_rang_01_date
```

jusqu'au rang 10.

### 6.3 Helpers mécaniques

```text
input_datetime.palmares_temperature_min_journaliere_haute_derniere_evaluation
```

La présente instance ne possède PAS de helper `snapshot_veille` : elle ne
crée pas de capture propre (cf. §3.2) et lit directement la mémoire
clôturée partagée.

### 6.4 Source pipeline (partagée)

```text
input_number.temperature_min_jour_courant_jardin
input_number.temperature_min_journaliere_jardin
```

### 6.5 Choix du qualificateur

Le qualificateur d'instance reprend le nom exact de la grandeur source
(`temperature_min_journaliere`) suivi de la direction de classement
(`haute`). Ce choix est délibérément plus explicite que l'insertion dans
le seul créneau `journalier_<adjectif>` des instances `chaud`/`froid` : il
écarte toute confusion avec `_chaud`, qui classe le MAXIMUM journalier et
non le minimum. Les trois instances coexistent sans collision de
nomenclature.

---

## 7. Invariants métier

| ID | Invariant |
|---|---|
| INV-NH-1 | La source métier représente une journée civile clôturée. |
| INV-NH-2 | Une fenêtre glissante 24 h est interdite comme source. |
| INV-NH-3 | Le palmarès ne consomme jamais une température instantanée directe. |
| INV-NH-4 | Une date civile ne peut apparaître qu'une fois dans les rangs. |
| INV-NH-5 | Les records représentent des minima quotidiens réels observés au domicile. |
| INV-NH-6 | La sentinelle `-999` est une valeur technique, jamais une valeur métier. |
| INV-NH-7 | `sensor.palmares_temperature_min_journaliere_haute` n'expose jamais `-999`. |
| INV-NH-8 | FIFO sur égalité : l'antériorité prime, un record égal n'évince pas l'antérieur. |
| INV-NH-9 | Tout rang vide a valeur `-999` et date `''` — couplage strict. |
| INV-NH-10 | Le rang 1 contient la valeur la plus haute (minimum journalier le plus élevé). |

---

## 8. Doctrine d'insertion

```text
1. Source hors plage métier [-50, 50] (dont 999, unknown, unavailable) → abstention
2. date_veille déjà présente dans les rangs                           → abstention
3. Palmarès plein ET source ≤ rang_10                                 → abstention (FIFO)
4. Sinon                                                              → insertion, tri descendant
```

Tri : `(valeur desc, index_anteriorite asc)` — garantit FIFO sur égalité.

La minimale la plus haute gagne le rang 1. Le rang 10 contient la moins
haute des minimales du palmarès. Une journée dont la minimale est plus
haute que le rang 10 mérite l'insertion ; une journée égale au rang 10 ne
l'évince pas (FIFO strict).

---

## 9. Invariants de cohérence (binary_sensor anomalie)

Évalués dans l'ordre canonique suivant :

| ID | Invariant | Raison exposée |
|---|---|---|
| B1 | Ordre descendant : `valeur[i] >= valeur[i+1]` pour tout rang rempli | `ordre_rompu_rang_NN_MM` |
| B2 | Couplage : valeur != `-999` ↔ date non vide | `incoherence_couplage_rang_NN` |
| B3 | Compacité : aucun rang rempli après un rang vide | `compacite_rompue_rang_NN` |
| B4 | Fraîcheur : dernière évaluation ≤ 36 h | `evaluation_manquante` |

Un rang est considéré « rempli » si `date != ''` (autrement dit, si
`valeur != -999`). Les deux conditions sont strictement équivalentes par
INV-NH-9 ; toute divergence relève de B2.

Exemptions B4 :

- sentinelle `1970-01-01 00:00:00` → état initial légitime, pas d'anomalie
- `unknown` / `unavailable` → `evaluation_indisponible`

---

## 10. Précondition bloquante

Le système ne doit pas être considéré opérationnel tant que la mémoire
clôturée `input_number.temperature_min_journaliere_jardin` n'a pas été
alimentée par au moins une clôture valide. Tant que la mémoire vaut la
sentinelle d'absence `999`, l'évaluation s'abstient.

---

## 11. Recorder

### Population B

21 entités : 10 `input_number` valeurs + 10 `input_text` dates + 1
`input_datetime` dernière évaluation.

La source `input_number.temperature_min_journaliere_jardin` et son
exposition `sensor.temperature_min_journaliere_jardin` sont déjà
historisées au titre du contrat `palmares_froid` ; aucune réinscription
n'est nécessaire (anti-redondance).

Fréquence : ≤ 1 écriture/jour par entité. Cardinalité finie. Logbook
acceptable.

---

## 12. Hors périmètre

- les journées les plus froides (cf. contrat `palmares_froid`) ;
- les maxima journaliers (cf. contrat `palmares_chaleur`) ;
- les records glissants ;
- les records saisonniers ou annuels ;
- les températures intérieures ;
- les statistiques Recorder ;
- les prévisions météo.

---

## 13. Différences notables avec le contrat froid v1.0.2

Cette section consigne les points de spécialisation où l'instance des
nuits chaudes ne se déduit pas mécaniquement de l'instance froide, alors
même qu'elle partage la source.

| # | Point | Froid v1.0.2 | Nuits chaudes v1.0 |
|---|---|---|---|
| 1 | Sens du classement | minimale la plus basse | minimale la plus haute |
| 2 | Tri et insertion | `(valeur asc, index asc)` | `(valeur desc, index asc)` |
| 3 | Invariant B1 | `valeur[i] <= valeur[i+1]` | `valeur[i] >= valeur[i+1]` |
| 4 | Seuil mérite (palmarès plein) | `source < rang_10` | `source > rang_10` |
| 5 | Sentinelle de rang vide | `999` | `-999` |
| 6 | Invariant B2 | `valeur != 999 ↔ date != ''` | `valeur != -999 ↔ date != ''` |
| 7 | Capture du minimum | snapshot dédié à 23:59:55 | aucune — lecture de la mémoire clôturée à 00:00:35 |
| 8 | Heure d'évaluation | 00:00:30 | 00:00:35 |

Le point 7 est structurant : la présente instance n'introduit aucune
chaîne de capture parallèle. Elle réutilise la mémoire clôturée déjà
produite par le pipeline froid, conformément au principe de non-redondance.

---

## Attributs de présentation (dérivés)

Le capteur synthèse `sensor.palmares_temperature_min_journaliere_haute` expose,
en complément des attributs canoniques, des attributs de **présentation**
destinés à l'affichage humain.

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
| 1.0 | 2026-06-22 | Brouillon normatif initial — classement descendant du minimum journalier clôturé, réutilisation de la chaîne de capture froide, double sentinelle (999 absence source, -999 rang vide). |
| 1.1 | 2026-07-07 | Ajout d'attributs de présentation dérivés `rang_NN_date_affichage` (`DD/MM/YYYY`) exposés côté backend. La date ISO `rang_NN_date` reste canonique ; aucun impact sur classement, valeurs ou fraîcheur. |
