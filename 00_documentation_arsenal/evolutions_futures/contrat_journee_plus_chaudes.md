# Arsenal — Contrat métier

# Palmarès historique — Journées les plus chaudes

# Version : 1.0

# Statut : brouillon normatif

# Dépend de :

# - contrat_palmares_historique.md

# - contrat_axe_temperature_jardin.md

---

# 1. Objet

Définir l'instance métier Arsenal dédiée au
palmarès historique des journées les plus chaudes
observées au domicile.

Le système maintient un classement persistant
des N journées civiles ayant atteint les
plus fortes températures maximales quotidiennes.

Le présent contrat spécialise la primitive
« palmarès historique » au domaine thermique
extérieur.

---

# 2. Périmètre

Le présent contrat couvre exclusivement :

* les journées les plus chaudes ;
* le domaine météo jardin ;
* le cycle journalier civil ;
* les maxima quotidiens clôturés.

Le présent contrat ne couvre pas :

* les journées les plus froides ;
* les statistiques glissantes ;
* les records hebdomadaires ;
* les records mensuels ;
* les températures intérieures ;
* les prévisions météo.

---

# 3. Source métier canonique

## 3.1 Source attendue

La source métier canonique est :

```text
sensor.temperature_max_journaliere_jardin
```

Cette source représente :

```text
la température maximale atteinte
sur une journée civile clôturée
(00:00:00 → 23:59:59)
```

---

## 3.2 Interdiction des maxima glissants

Une fenêtre glissante 24 h
ne constitue pas une journée civile clôturée.

En conséquence, un capteur construit via :

```yaml
platform: statistics
state_characteristic: value_max
max_age:
  hours: 24
```

est explicitement interdit comme source métier
pour le présent contrat.

---

## 3.3 Justification doctrinale

Un maximum glissant peut encore contenir
une valeur appartenant à la journée précédente.

Cela peut produire :

* des faux records ;
* des journées historiquement incorrectes ;
* des palmarès plausibles mais faux.

Le présent contrat interdit explicitement
ce mélange temporel.

---

# 4. Dépendances

| Dépendance                                | Rôle                            | Caractère |
| ----------------------------------------- | ------------------------------- | --------- |
| contrat_palmares_historique.md            | primitive générique             | bloquant  |
| contrat_axe_temperature_jardin.md         | axe thermique robuste           | bloquant  |
| sensor.temperature_jardin                 | température robuste instantanée | bloquant  |
| sensor.temperature_max_journaliere_jardin | maximum journalier civil        | bloquant  |

---

# 5. Paramètres d'instance

| Paramètre         | Valeur                                    |
| ----------------- | ----------------------------------------- |
| instance_id       | temperature_journalier_chaud              |
| source            | sensor.temperature_max_journaliere_jardin |
| cycle             | daily                                     |
| top_n             | 10                                        |
| unite             | °C                                        |
| seuil_fraicheur_h | 36                                        |

---

# 6. Convention de nommage

## 6.1 Capteurs exposés

```text
sensor.palmares_temperature_journalier_chaud
binary_sensor.palmares_temperature_journalier_chaud_anomalie
```

---

## 6.2 Helpers de rang

```text
input_number.palmares_temperature_journalier_chaud_rang_01_valeur
input_text.palmares_temperature_journalier_chaud_rang_01_date
```

jusqu'au rang 10.

---

## 6.3 Helpers mécaniques

```text
input_number.palmares_temperature_journalier_chaud_snapshot_veille
input_datetime.palmares_temperature_journalier_chaud_derniere_evaluation
```

---

## 6.4 Réserve nomenclature future

Le suffixe :

```text
_chaud
```

est réservé afin de permettre
une future instance :

```text
temperature_journalier_froid
```

sans collision de nomenclature
ni refonte structurelle.

---

# 7. Invariants métier

| ID       | Invariant                                                                  |
| -------- | -------------------------------------------------------------------------- |
| INV-CH-1 | La source métier représente une journée civile clôturée.                   |
| INV-CH-2 | Une fenêtre glissante 24 h est interdite.                                  |
| INV-CH-3 | Le palmarès ne consomme jamais une température instantanée directe.        |
| INV-CH-4 | Une date civile ne peut apparaître qu'une fois.                            |
| INV-CH-5 | Les records représentent des maxima quotidiens réels observés au domicile. |

---

# 8. Précondition bloquante

Le système ne doit pas être implémenté tant que :

```text
sensor.temperature_max_journaliere_jardin
```

n'existe pas sous forme conforme.

Toute implémentation basée sur :

```text
sensor.temperature_max_jour_jardin
```

construit via :

```yaml
statistics:
  max_age: 24h
```

est non conforme au présent contrat.

---

# 9. Hors périmètre

Le présent contrat exclut explicitement :

* les journées les plus froides ;
* les minima journaliers ;
* les records glissants ;
* les records saisonniers ;
* les records annuels ;
* les températures intérieures ;
* les statistiques Recorder ;
* les prévisions météo.

---

# 10. Extensions futures envisagées

Les évolutions suivantes sont considérées compatibles :

* instance :
  `temperature_journalier_froid`
* records hebdomadaires ;
* records mensuels ;
* records saisonniers ;
* dashboards records météo ;
* badges records historiques ;
* alertes record absolu.

Aucune de ces extensions
n'a de valeur normative en v1.0.
