# Contrat — Diagnostic station météo Netatmo
**Arsenal** · Couche observation · v1.0

---

## Objet

Ce contrat définit la logique de diagnostic des stations météo Netatmo dans Arsenal.

Le diagnostic ne répond pas à : *« le module jardin va-t-il bien ? »*

Il répond à : **« la station entière est-elle suffisamment vivante pour qu'un redémarrage global soit injustifié ? »**

---

## 1. Périmètre utile par station

### Station 1 — `diagnostic_netatmo_arnaud`

| Catégorie | Entités |
|-----------|---------|
| **Ping** | `binary_sensor.station_meteo_netatmo_1` |
| **Températures** | `sensor.temperature_chambre_arnaud_1` · `sensor.temperature_chambre_parents_1` · `sensor.temperature_jardin_1` · `sensor.temperature_petite_maison` · `sensor.temperature_sejour_1` |
| **Humidités** | `sensor.humidite_relative_chambre_arnaud_1` · `sensor.humidite_relative_chambre_parents_1` · `sensor.humidite_relative_jardin_1` · `sensor.humidite_relative_petite_maison` · `sensor.humidite_relative_sejour_1` |
| **CO2** | `sensor.co2_chambre_arnaud` · `sensor.co2_chambre_parents` · `sensor.co2_petite_maison` · `sensor.co2_sejour` |
| **Bruit** | `sensor.bruit_chambre_arnaud` |

### Station 2 — `diagnostic_netatmo_matthieu`

| Catégorie | Entités |
|-----------|---------|
| **Ping** | `binary_sensor.station_meteo_netatmo_2` |
| **Températures** | `sensor.temperature_chambre_matthieu_1` · `sensor.temperature_entree_1` · `sensor.temperature_jardin_2` |
| **Humidités** | `sensor.humidite_relative_chambre_matthieu_1` · `sensor.humidite_relative_entree_1` · `sensor.humidite_relative_jardin_2` |
| **CO2** | `sensor.co2_chambre_matthieu` · `sensor.co2_entree` |
| **Bruit** | `sensor.bruit_chambre_matthieu` |

---

## 2. Principes architecturaux

### 2.1 Sonde jardin — désignation documentaire uniquement

Le module jardin (`sensor.temperature_jardin_*`) est historiquement désigné comme sonde primaire de fraîcheur car il se met à jour plus fréquemment que les modules intérieurs.

**Cette désignation est documentaire uniquement et n'a aucun effet sur la logique de décision du diagnostic.**

Dans la logique métier, toutes les entités de la station ont strictement le même poids comme preuve de vie. Le jardin reste utile pour le diagnostic visuel dans les dashboards Arsenal (gel visible rapidement), mais le capteur de diagnostic n'agit pas sur cette intuition.

### 2.2 Preuves de vie — toutes catégories confondues

Les preuves de vie exploitables sont l'ensemble des mesures numériques de la station :

- températures
- humidités relatives
- CO2
- bruit

La logique est la suivante :

- **jardin présent** → très bon signal, mais pas de statut privilégié
- **jardin absent, autres mesures présentes** → station vivante
- **aucune donnée exploitable** → seulement là on entre dans la branche de diagnostic KO

### 2.3 Rôle du ping

Le ping (`binary_sensor.station_meteo_netatmo_*`) ne prouve pas que HomeKit remonte correctement les mesures. Il sert uniquement à **départager** la nature d'une panne déjà constatée :

- panne logique / chaîne HomeKit
- panne réseau

> **Le ping ne doit jamais écraser l'existence de données réelles.**
> Si des mesures numériques remontent, la station est de fait vivante, même si le ping est contradictoire.

---

## 3. États métier

### `ok`

La station est considérée fonctionnelle si **au moins une entité utile de la station est exploitable**, quelle qu'elle soit.

> Toute donnée réelle de la station vaut preuve de vie suffisante.

### `ko_homekit`

La station est considérée en panne logique / chaîne de remontée si :

- aucune entité utile n'est exploitable
- **et** `binary_sensor.station_meteo_netatmo_*` est `on`

> Le réseau semble vivant, mais plus aucune donnée capteur ne remonte.

### `ko_reseau`

La station est considérée en panne réseau si :

- aucune entité utile n'est exploitable
- **et** `binary_sensor.station_meteo_netatmo_*` n'est pas `on`

> Plus de données, plus de preuve réseau.

---

## 4. Règle centrale du contrat

> **L'absence de `sensor.temperature_jardin_*` seule n'a aucune valeur de condamnation globale de station.**

C'est la correction directe du vice du premier capteur, qui faisait implicitement `jardin → vérité station`. Le nouveau contrat fait `station → vérité station`. Ce changement est une inversion conceptuelle : on passe d'un diagnostic mono-signal fragile à un diagnostic multi-preuves robuste.

---

## 5. Définition d'une entité exploitable

Une entité est exploitable si et seulement si son état est **numériquement interprétable** — c'est-à-dire convertible en nombre sans erreur.

Tout state non convertible est considéré non exploitable, notamment : `unavailable`, `unknown`, `none`, `''`, toute string non numérique.

> **La validité d'une preuve de vie ne doit jamais être déduite de la simple présence d'un state texte.**

---

## 6. Contrainte d'implémentation — sélection positive

L'implémentation YAML DOIT reposer sur une **logique de sélection positive** des états valides.

Elle NE DOIT PAS reposer sur l'exclusion partielle d'états invalides connus (`unavailable`, `unknown`, etc.).

Pièges à ne pas reproduire :

```jinja
{# INTERDIT — liste toujours truthy #}
{% if preuves %}

{# INTERDIT — exclut seulement 'unavailable' #}
{% if 'unavailable' not in preuves %}

{# INTERDIT — reject partiel #}
{% set valides = preuves | reject('equalto', 'unavailable') | list %}
{% if valides | count > 0 %}
```

Forme correcte :

```jinja
{# CORRECT — sélection positive par numéricité #}
{% set valides = preuves
   | map('float', default=none)
   | reject('eq', none)
   | list %}
{% if valides | count > 0 %}
```

---

## 7. Contrainte sur la liste des preuves de vie

Les entités listées comme preuves de vie **DOIVENT** être des `sensor` à état numérique continu.

Sont **interdits** dans cette liste :

- tout `binary_sensor`
- tout `input_boolean`
- toute entité à état textuel discret (`on` / `off`, labels, etc.)

> Cette contrainte est vérifiable statiquement à la relecture du YAML. Elle ne génère aucune erreur à l'exécution en cas de violation — une entité non numérique serait silencieusement exclue, sans avertissement. C'est précisément pour cette raison qu'elle doit être verrouillée contractuellement.

---

## 8. Ordre logique impératif

L'évaluation DOIT suivre cet ordre strict :

```
1. Évaluer les preuves de vie (entités numériques exploitables)
2. Si au moins une → ok
3. Sinon, lire le ping
4. Si ping = on → ko_homekit
5. Sinon → ko_reseau
```

En pseudo-code :

```python
if preuves_valides:
    ok
elif ping == 'on':
    ko_homekit
else:
    ko_reseau
```

Il est **interdit** de combiner ping et preuves de vie dans une même condition (`and`). Le ping n'intervient qu'en branche `else` de l'évaluation des preuves.

---

## 9. Ce que le diagnostic autorise et interdit

### Autorisé

- Déterminer si un redémarrage global de station peut être envisagé

### Interdit

- Diagnostiquer un module individuel (jardin, chambre, etc.)
- Forcer une action lourde sur la base de l'absence d'une seule mesure
- Confondre absence locale d'une mesure et panne globale de station

---

## 10. Cas de test métier

| # | Situation | État attendu |
|---|-----------|--------------|
| 1 | Station 1 — `temperature_jardin_1` absente, `temperature_sejour_1` présente | `ok` |
| 2 | Station 1 — toutes températures absentes, `co2_chambre_parents` présent | `ok` |
| 3 | Station 2 — plus aucune température ni humidité, `co2_entree` présent | `ok` |
| 4 | Station 2 — aucune donnée exploitable, `binary_sensor.station_meteo_netatmo_2` = `on` | `ko_homekit` |
| 5 | Station 1 — aucune donnée exploitable, `binary_sensor.station_meteo_netatmo_1` ≠ `on` | `ko_reseau` |

---

*Arsenal — document contractuel · couche observation · diagnostic Netatmo · v1.0*
