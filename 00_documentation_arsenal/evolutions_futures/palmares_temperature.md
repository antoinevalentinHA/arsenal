# Arsenal — Évolutions futures

# Palmarès température journalière

# Version : 1.0

# Statut : réflexion architecturale

---

# 1. Objet

Documenter les travaux préparatoires nécessaires
à l'implémentation des palmarès historiques
liés à la température journalière.

Ce document n'est pas normatif.

---

# 2. Situation actuelle

Le système dispose actuellement de :

```text
sensor.temperature_max_jour_jardin
sensor.temperature_min_jour_jardin
```

Ces capteurs sont construits via :

```yaml
platform: statistics
max_age: 24h
```

Ils sont adaptés :

* à l'affichage UI ;
* à la visualisation récente ;
* aux usages glissants.

Ils ne sont pas adaptés :

* aux palmarès historiques ;
* aux records journaliers civils ;
* aux archives thermiques robustes.

---

# 3. Problème fondamental

Une fenêtre glissante 24 h :

```text
ne correspond pas
à une journée civile clôturée
```

Exemple :

```text
Jour J-1 :
max = 31.2°C

Jour J :
max réel actuel = 30.8°C
```

À 15:00 :

```text
statistics max 24 h
= 31.2°C
```

alors que :

```text
le maximum réel du jour J
est 30.8°C
```

Un palmarès construit sur cette base
produirait des records historiquement faux.

---

# 4. Orientation retenue

Créer des sources métier dédiées :

```text
sensor.temperature_max_journaliere_jardin
sensor.temperature_min_journaliere_jardin
```

reposant sur :

* des périodes civiles explicites ;
* une clôture quotidienne ;
* une capture stable ;
* une séparation claire entre :

  * instantané ;
  * glissant ;
  * journalier clôturé.

---

# 5. Nomenclature réservée

Les identifiants suivants sont réservés :

```text
temperature_journalier_chaud
temperature_journalier_froid
```

afin de permettre :

* une symétrie métier ;
* des contrats séparés ;
* des implémentations indépendantes ;
* des dashboards spécialisés.

---

# 6. Doctrine retenue

Arsenal privilégie ici :

```text
deux systèmes métier explicites
```

plutôt qu'un système générique :

```text
sens = max|min
```

Motifs :

* lisibilité ;
* auditabilité ;
* séparation métier ;
* simplicité des validations ;
* réduction des branchements conditionnels.

---

# 7. Chantiers futurs possibles

* source journalière clôturée canonique ;
* palmarès journées chaudes ;
* palmarès journées froides ;
* dashboards records météo ;
* badges records historiques ;
* alertes record absolu ;
* export statistique annuel ;
* records multi-zones.

---

# 8. Point doctrinal important

Un capteur :

```yaml
statistics:
  max_age: 24h
```

n'est pas faux.

Il répond simplement à une autre question métier.

Le problème apparaît uniquement
lorsqu'une fenêtre glissante est
confondue avec une période civile clôturée.
