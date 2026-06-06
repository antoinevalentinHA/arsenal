# 🌦️ ARSENAL — CONTRAT D'AFFICHAGE MÉTÉO
#
# 📌 Statut :
#   Contrat NORMATIF et OPPOSABLE
#
# 📌 Domaine :
#   Météo — Affichage & restitution UI
#
# 📌 Autorité :
#   Ce contrat fait foi pour toute représentation
#   visuelle des données météo dans ARSENAL.
#
# ==========================================================

## 🎯 Objet

Ce contrat définit **les règles normatives de restitution UI**
des données météo dans ARSENAL.

Il établit :
- ce qui peut être **affiché**,
- comment une donnée météo doit être **restituée visuellement**,
- la **séparation stricte** entre donnée, interprétation et affichage,
- les **invariants d'honnêteté visuelle**.

Ce contrat **ne gouverne pas la validité des données météo**
(couverte par `gouvernance.md`,
`validation.md`, `fallback.md`).

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- l'affichage des grandeurs météo suivantes :
  - température,
  - humidité relative,
  - humidité absolue,
  - humidex,
- l'utilisation de **capteurs de couleur dédiés**,
- la structuration des dashboards météo,
- la navigation entre vues météo.

Il ne couvre PAS :

- la production de la donnée,
- la qualification de validité,
- les mécanismes de fallback,
- les seuils métier,
- toute décision ou recommandation.

---

## 🧠 Principe fondamental

L'affichage météo ARSENAL est **strictement passif**.

👉 **L'UI observe. Elle n'interprète jamais.**

Aucune logique métier, seuil, comparaison ou extrapolation
n'est autorisée dans la couche UI.

---

## 🧩 Relation aux contrats météo

`gouvernance.md` définit le cadre normatif du domaine.
`validation.md` définit ce qu'est une donnée météo valide.
`fallback.md` définit la continuité et les conditions d'abstention.

Le présent contrat :

- **consomme exclusivement** des données déjà qualifiées,
- n'évalue jamais leur validité,
- ne déclenche aucun fallback.

➡️ Une donnée météo non conforme à l'architecture contractuelle météo
est réputée **inexploitable** et doit être affichée comme telle.

---

## 🔒 Invariants normatifs d'affichage

### Invariant 1 — Fidélité absolue

Toute carte météo affiche :

- la **valeur brute** du capteur référencé,
- sans transformation sémantique,
- sans correction,
- sans arrondi métier implicite.

---

### Invariant 2 — Séparation stricte valeur / couleur

- La **valeur numérique** est portée par un capteur météo.
- La **signification visuelle** est portée par un capteur distinct :
  - `sensor.couleur_temperature_*`
  - `sensor.couleur_humidite_relative_*`
  - `sensor.couleur_humidite_absolue_*`
  - `sensor.couleur_humidex_*`

👉 Aucune carte UI ne calcule une couleur à partir d'une valeur.

---

### Invariant 3 — Consommation directe des capteurs couleur

Les cartes UI :

- consomment **directement** l'état textuel des capteurs couleur,
- ne redéfinissent aucune correspondance seuil → couleur,
- n'introduisent aucune logique conditionnelle locale.

---

### Invariant 4 — États invalides visibles

Si une donnée est :
- `unknown`,
- `unavailable`,
- absente,

alors :

- l'état est affiché comme tel,
- la couleur associée est **grey**,
- aucune tentative de masquage n'est autorisée.

---

### Invariant 5 — Neutralité visuelle

La couleur affichée :

- est **descriptive**,
- n'est **jamais prescriptive**,
- ne suggère aucune action,
- ne qualifie aucun confort souhaitable.

---

## 🎨 Gestion des couleurs

### Principe

La palette et la logique de couleur :

- sont définies **en amont**, hors UI,
- exposées sous forme de **capteurs dédiés**,
- utilisées telles quelles par les templates de cartes (socle `socle_kpi`).

L'UI :
- n'invente pas de couleur,
- n'en substitue aucune,
- n'en déduit aucune.

---

## 🧭 Structuration des dashboards météo

Les dashboards météo respectent :

- une **séparation par grandeur** :
  - température,
  - humidité relative,
  - humidité absolue,
  - humidex,
- une navigation explicite entre vues,
- une lecture homogène par zone.

Chaque carte :

- référence **une seule entité météo**,
- affiche **une seule grandeur physique**.

---

## ⛔ Interdictions absolues

Il est strictement interdit :

- d'introduire une logique de seuil dans l'UI,
- de recalculer une couleur côté carte,
- de comparer plusieurs capteurs dans l'UI,
- de masquer une invalidité,
- de transformer une valeur pour "aider" la lecture,
- de fusionner plusieurs grandeurs sur une même carte.

Toute violation constitue une **non-conformité contractuelle**.

---

## 📌 Statut

- Contrat Arsenal
- Normatif et opposable
- Domaine : Affichage météo
- Dépendances :
  - [`gouvernance.md`](gouvernance.md)
  - [`validation.md`](validation.md)
  - [`fallback.md`](fallback.md)
  - [`/architecture/capteurs_meteo.md`](../../architecture/capteurs_meteo.md)

Toute évolution nécessite :
- modification explicite du contrat,
- validation humaine,
- traçabilité ARSENAL.
