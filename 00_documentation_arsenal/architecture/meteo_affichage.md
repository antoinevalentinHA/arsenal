# ==========================================================
# 🧠 ARSENAL — ARCHITECTURE
#     Affichage météo
# ==========================================================

## 🎯 Objet du document

Ce document décrit **l’architecture canonique de l’affichage météo**
dans le système ARSENAL.

Il formalise :
- la structuration des dashboards météo,
- la séparation stricte entre **donnée**, **interprétation** et **UI**,
- le rôle des **capteurs de couleur**,
- les règles d’assemblage des cartes météo,
- les flux de dépendance entre capteurs et affichage.

Ce document est **normatif sur la structure**,  
mais **ne définit aucune règle fonctionnelle**.

---

## 🧱 Positionnement architectural

L’affichage météo appartient à la couche :

> **UI de restitution passive**

Il est **en aval** :
- de la gouvernance météo (`contrats/meteo.md`),
- de l’architecture des capteurs (`architecture/capteurs_meteo.md`).

Il est **en amont** :
- de la lecture humaine,
- de la supervision visuelle.

Il ne participe **à aucune décision**.

---

## 🧠 Principe fondateur

L’architecture d’affichage météo repose sur une séparation stricte
en **trois couches indépendantes** :

  [ Capteurs météo ]
          ↓ 
  [ Capteurs couleur ]
          ↓ 
  [ UI / Dashboards ]

Aucune couche ne court-circuite la suivante.

---

## 🌡️ Couche 1 — Capteurs météo

Cette couche fournit :
- les **valeurs physiques**,
- déjà qualifiées par la gouvernance météo.

Exemples :
- `sensor.temperature_*`
- `sensor.humidite_relative_*`
- `sensor.humidite_absolue_*`
- `sensor.humidex_*`

Aucun capteur météo :
- ne connaît l’UI,
- ne connaît la couleur,
- ne connaît l’affichage.

---

## 🎨 Couche 2 — Capteurs de couleur

Cette couche :
- **interprète visuellement** une grandeur météo,
- sans produire de décision,
- sans piloter l’UI.

Chaque capteur couleur :
- dépend **d’une seule grandeur météo**,
- expose **un état textuel** (`green`, `yellow`, `red`, `grey`, etc.).

Conventions canoniques :
- `sensor.couleur_temperature_<zone>`
- `sensor.couleur_humidite_relative_<zone>`
- `sensor.couleur_humidite_absolue_<zone>`
- `sensor.couleur_humidex_<zone>`

Ces capteurs :
- sont **réévaluables à tout instant**,
- sont **idempotents**,
- ne déclenchent aucune action.

---

## 🖥️ Couche 3 — UI / Dashboards météo

La couche UI :
- **consomme directement** les capteurs météo et couleur,
- ne contient **aucune logique métier**,
- ne fait **aucune comparaison inter-capteurs**.

Chaque carte :
- référence **exactement une entité météo**,
- référence **exactement un capteur couleur associé**,
- affiche **une seule grandeur**.

---

## 🧩 Templates de cartes

Les templates `carte_*` :

- sont **génériques**,
- ne contiennent aucune logique métier,
- se contentent de :
  - afficher une valeur,
  - appliquer une couleur fournie.

Exemples :
- `carte_temperature`
- `carte_humidite`
- `carte_humidite_absolue`
- `carte_humidex`

Toute logique conditionnelle visible dans l’UI
est **strictement limitée à la mise en forme**.

---

## 🧭 Structuration des dashboards

Les dashboards météo sont structurés :

- par **grandeur physique** (un dashboard = un axe),
- par **zones géographiques** (jardin, RDC, chambres, etc.).

Navigation :
- explicite,
- non contextuelle,
- non conditionnelle.

Aucun dashboard :
- ne fusionne plusieurs grandeurs,
- ne déduit une information composite.

---

## 🚫 Anti-patterns interdits (architecture)

Sont considérés comme des ruptures d’architecture :

- calculer une couleur dans une carte UI,
- comparer deux capteurs météo dans l’UI,
- masquer un état invalide par un affichage neutre,
- faire dépendre l’UI d’un seuil métier,
- introduire une logique de fallback dans l’UI.

Ces points sont **structurellement exclus**.

---

## 🔁 Relation avec les contrats

Ce document :

- **implémente structurellement** :
  - `contrats/meteo.md`
  - `contrats/meteo_affichage.md`
- **ne les modifie pas**,
- **ne les complète pas**.

En cas de divergence :
➡️ **le contrat prime toujours**.

---

## 📌 Statut

- Type : Architecture
- Domaine : Affichage météo
- Caractère : Normatif (structure)
- Autorité : Aucune
- Dépendances :
  - `/contrats/meteo.md`
  - `/contrats/meteo_affichage.md`
  - `/architecture/capteurs_meteo.md`

Toute évolution de cette architecture
doit être motivée par une évolution contractuelle préalable.