# Arsenal — Climatisation · Couche Décision
## Observations techniques

> **Document non-normatif.**
> Ce fichier documente les choix de structure, les asymétries et les particularités observées dans le YAML.
> Il ne constitue pas une spécification contractuelle et ne contient aucun jugement de valeur.

---

## 1. Le groupe ne suit pas un patron unique

### Observation

Les cinq entités transmises ne relèvent pas toutes de la décision au sens strict :
- `clim_target_mode` est décisionnel
- `clim_action_en_cours` et `clim_raison_decision` sont explicatifs
- `consigne_clim_appliquee` est un paramètre dérivé
- `clim_mode_local` est une lecture locale stabilisée

### Signification structurelle

Le regroupement "couche décision" est ici fonctionnel plutôt que strictement architectural.
Il agrège la décision centrale et plusieurs capteurs de support à la lecture ou à l'explication.

---

## 2. `clim_target_mode` fusionne décision et arbitrage

### Observation

Le commentaire YAML explicite que la couche Décision et la couche Arbitrage sont fusionnées dans cette implémentation.
Les candidats n'ont pas d'existence matérielle distincte.

### Signification structurelle

Le template produit directement le mode cible final.
L'arbitrage est porté par l'ordre des branches `if / elif`, sans capteurs intermédiaires de candidats.

---

## 3. Priorité structurelle `cool` > `dry` > `heat`

### Observation

L'ordre du template `clim_target_mode` est : `cool` → `dry` → `heat` → `off`.

### Signification structurelle

Si plusieurs couples besoin + autorisation sont simultanément vrais, la décision retient le premier mode rencontré.
Cette priorité est codée structurellement, non paramétrée.

---

## 4. Deux entités utilisent une mémoire locale via `this.*`

### Observation

- `consigne_clim_appliquee` utilise `states(this.entity_id)` comme fallback de valeur
- `clim_mode_local` utilise `this.state` comme fallback d'état et d'icône

### Signification structurelle

Le groupe mélange des capteurs purement combinatoires et des capteurs à persistance locale implicite.
Cette persistance n'est pas externalisée dans un helper.

---

## 5. `clim_mode_local` est la seule entité trigger-based du groupe

### Observation

`clim_mode_local` est défini avec un bloc `trigger:` et non comme template state-based simple.

### Signification structurelle

L'entité est recalculée sur des événements explicites (changement de `climate.clim`, stabilisation système), et non en évaluation continue dépendante du graphe d'états.

---

## 6. `clim_action_en_cours` priorise un blocage unique

### Observation

`clim_action_en_cours` teste uniquement `input_boolean.blocage_clim_poele` avant l'état de `climate.clim`.
Il ne lit ni `binary_sensor.clim_bloquee`, ni `binary_sensor.clim_blocage_horaire_reel`, ni `binary_sensor.fenetre_ouverte_maison`.

### Signification structurelle

Le statut `bloquee` de ce capteur ne représente pas l'ensemble des blocages du domaine.
Il représente un cas prioritaire explicitement limité à `blocage_clim_poele`.

---

## 7. `clim_raison_decision` consomme les vérités métier admissibles

### Observation

`clim_raison_decision` consomme exclusivement :
- les blocages structurels du domaine (poêle, aération chauffage,
  blocage horaire, ouvertures),
- les besoins admissibles (`binary_sensor.besoin_clim_*_admissible`).

Aucune primitive brute (franchissement de seuil, humidex, présence)
n'est lue.

### Signification structurelle

L'explication est alignée sur la décision : la même couche d'admissibilité
alimente `clim_target_mode` et `clim_raison_decision`. La hiérarchie
décroissante reflète d'abord les blocages, puis les modes dans l'ordre de
la politique d'arbitrage active.

---

## 8. Hiérarchie des modes alignée sur la politique d'arbitrage

### Observation

Les trois causes climatiques (`refroidissement`, `deshumidification`,
`soutien_chauffage`) sont produites à partir des admissibles
correspondants, dans l'ordre `cool` → `dry` → `heat`.

### Signification structurelle

Cet ordre est identique à celui de `clim_target_mode` (politique
`ThermalPriorityPolicy v1`). Aucune asymétrie de condition n'est
introduite entre les modes : la cohérence avec la décision repose sur
l'amont (la couche Admissibilité applique déjà les contraintes spécifiques
à chaque mode, dont la présence pour HEAT).


---

## 9. `consigne_clim_appliquee` et `clim_mode_local` embarquent une sémantique d'attribut ou d'icône

### Observation

- `consigne_clim_appliquee` expose deux attributs : `presence` et `source`
- `clim_mode_local` produit une icône dynamique par mapping du mode

### Signification structurelle

Ces entités portent à la fois de l'information métier et une couche de présentation ou d'observabilité minimale dans le YAML lui-même.

---

## 10. `clim_raison_decision` retourne une cause unique, pas une explication exhaustive

### Observation

Le template est strictement séquentiel et s'arrête à la première cause reconnue.

### Signification structurelle

En présence de plusieurs causes simultanées, toutes les causes de rang inférieur sont masquées.
Le capteur exprime une raison principale priorisée, pas un diagnostic exhaustif.
