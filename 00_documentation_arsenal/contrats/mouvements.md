# ==========================================================
# 📜 CONTRAT ARSENAL — MOUVEMENTS
# ----------------------------------------------------------
# 📛 Domaine : Détection de mouvement (capteurs PIR)
# 🧠 Nature : Normalisation et agrégation des événements
#
# Version : v1.0
# Statut  : Stable
#
# Ce document définit la structure officielle des capteurs
# de mouvement dans Arsenal et leur niveau d’utilisation
# autorisé dans l’architecture.
# ==========================================================



# 1) Objectif

Garantir que les événements de détection de mouvement soient :

- robustes
- lisibles
- découplés du matériel
- utilisables par les automatisations sans bruit événementiel.

Le système repose sur une **architecture en couches** séparant :

- les capteurs matériels
- la normalisation
- l’agrégation par zone
- l’agrégation globale.

Cette structure évite que les automatisations dépendent
directement des entités Zigbee2MQTT.



# 2) Architecture des couches



## N0 — Matériel (source physique)

Entités issues des intégrations (Zigbee2MQTT).

Exemples :

```
binary_sensor.capteur_mouvements_sejour_1_occupancy
binary_sensor.capteur_mouvements_sejour_2_occupancy
binary_sensor.capteur_mouvements_garage_1_occupancy
binary_sensor.capteur_mouvements_garage_2_occupancy
binary_sensor.capteur_mouvements_garage_3_occupancy
binary_sensor.capteur_mouvements_entree_occupancy
```

Caractéristiques :

- état matériel brut
- peut devenir `unknown` ou `unavailable`
- dépend de l’intégration Zigbee
- peut changer de nom ou de structure

⚠️ **Ces entités ne doivent jamais être consommées directement
par les automatisations ou les capteurs métier.**



# 3) Couche N1 — Normalisation



## Rôle

Fournir une représentation stable des capteurs physiques.

Chaque capteur matériel possède un **miroir Arsenal normalisé**.

Exemples :

```
binary_sensor.mouvement_sejour_1
binary_sensor.mouvement_sejour_2
binary_sensor.mouvement_garage_1
binary_sensor.mouvement_garage_2
binary_sensor.mouvement_garage_3
binary_sensor.mouvement_entree_1
```



## Propriétés

Les capteurs N1 :

- restent **toujours évaluables**
- ne retournent jamais `unknown` ou `unavailable`
- exposent l’indisponibilité en **attribut**.

Exemple :

```
state: off
attributes:
  unavailable: true
  source_entity: binary_sensor.capteur_mouvements_sejour_1_occupancy
```



## Usage autorisé

Les capteurs N1 sont utilisés pour :

- dashboards de diagnostic
- visualisation des capteurs physiques
- analyse fine des événements.

Ils **ne doivent pas être utilisés directement** par les
automatisations métier sauf cas exceptionnel.



# 4) Couche N2 — Agrégation par zone



## Rôle

Représenter l’état de mouvement d’une **zone logique**.

Exemples :

```
binary_sensor.mouvement_sejour
binary_sensor.mouvement_garage
binary_sensor.mouvement_entree
```



## Principe

Les capteurs N2 utilisent une agrégation **OR** des N1.

Exemple :

```
mouvement_sejour =
    mouvement_sejour_1
 OR mouvement_sejour_2
```



## Avantages

Cette couche :

- supprime le bruit événementiel des capteurs PIR
- abstrait le nombre réel de capteurs
- permet des automatisations plus simples
- fournit un `last_changed` pertinent au niveau zone.



## Usage autorisé

Les capteurs N2 doivent être utilisés pour :

- automatisations d’éclairage
- règles de présence locale
- logiques d’absence
- déclenchement d’alarme par zone.



# 5) Couche N3 — Agrégation globale



## Rôle

Représenter l’état de mouvement **global de la maison**.

Exemple :

```
binary_sensor.mouvement_maison
```



## Principe

Agrégation OR des capteurs N2.

```
mouvement_maison =
    mouvement_sejour
 OR mouvement_garage
 OR mouvement_entree
```



## Usage autorisé

Les capteurs N3 sont utilisés pour :

- indicateurs UI globaux
- dashboards
- navigation
- synthèse d’activité.



⚠️ Ils ne doivent pas être utilisés pour des automatisations
de sécurité ou de logique locale.



# 6) Règles d’utilisation

Les règles suivantes sont **obligatoires**.



## Règle 1 — Interdiction du matériel brut

Les entités Zigbee2MQTT ne doivent jamais être utilisées
directement dans :

- automatisations
- capteurs métier
- dashboards principaux.



## Règle 2 — Automatisations locales → N2

Toute automation liée à une pièce ou une zone doit utiliser
les capteurs **N2**.

Exemple :

```
binary_sensor.mouvement_sejour
binary_sensor.mouvement_garage
```



## Règle 3 — UI détaillée → N1

Les dashboards de diagnostic peuvent afficher les capteurs
N1 pour visualiser chaque détecteur.



## Règle 4 — Synthèse globale → N3

Les indicateurs globaux de la maison utilisent uniquement
le capteur :

```
binary_sensor.mouvement_maison
```



# 7) Avantages architecturaux

Cette structure apporte :

- découplage complet du matériel Zigbee
- automatisations simplifiées
- suppression des rafales de déclenchements
- scalabilité (ajout de capteurs sans modifier les règles)
- lisibilité des événements de sécurité.



# 8) Exemple de chaîne complète

```
Capteur PIR (Zigbee2MQTT)
        │
        ▼
binary_sensor.capteur_mouvements_sejour_1_occupancy
        │
        ▼
N1
binary_sensor.mouvement_sejour_1
        │
        ▼
N2
binary_sensor.mouvement_sejour
        │
        ▼
N3
binary_sensor.mouvement_maison
```



# 9) Compatibilité

Compatible avec :

- Home Assistant 2024.8+
- Zigbee2MQTT
- architecture Arsenal multi-couches.



# 10) Historique

```
v1.0
- Création du modèle N0/N1/N2/N3
- Refactorisation complète des automatisations mouvements
- Suppression des dépendances aux capteurs Zigbee bruts
```