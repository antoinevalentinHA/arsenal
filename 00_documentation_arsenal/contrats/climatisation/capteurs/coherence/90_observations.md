# Arsenal — Climatisation · Cohérence décision / réel
## Observations techniques

> **Document non-normatif.**
> Ce fichier documente les choix de structure, les asymétries et les particularités observées dans le YAML.
> Il ne constitue pas une spécification contractuelle et ne contient aucun jugement de valeur.

---

## 1. Capteur purement diagnostique

### Observation

Le commentaire YAML explicite :
- "Diagnostic PUR"
- "Aucune décision"
- "Aucune action"

### Signification structurelle

L'entité observe une divergence mais n'embarque aucun mécanisme correctif.
Elle est positionnée comme signal de diagnostic, pas comme composant d'arbitrage ou d'exécution.

---

## 2. Anti-bruit porté par les triggers, pas par la logique d'état

### Observation

Le `for: "00:01:00"` est défini dans les triggers, pas dans le template `state:`.

### Signification structurelle

La persistance de 60 s conditionne le moment du recalcul.
Le template lui-même reste une comparaison instantanée entre les trois valeurs lues.

---

## 3. Diagnostic croisé sur deux dimensions du réel

### Observation

Le capteur ne compare pas seulement la cible à un mode réel.
Il compare :
- la cible à `switch.clim_power`
- la cible à `sensor.clim_mode_local`

### Signification structurelle

La cohérence attendue porte à la fois sur :
- l'alimentation effective
- le mode local observé

Une divergence sur l'un ou l'autre suffit à produire l'incohérence.

---

## 4. Traitement asymétrique de `off` versus modes actifs

### Observation

Le template distingue deux familles :
- `target == off`
- `target in ['cool', 'dry', 'heat']`

### Signification structurelle

Pour `off`, la cohérence attend un arrêt complet :
- alimentation coupée
- mode local `off`

Pour les modes actifs, la cohérence attend :
- alimentation `on`
- mode local identique à la cible

L'arrêt est donc traité comme un état nominal complet, pas comme l'absence d'un mode.

---

## 5. Valeurs hors périmètre de `target` neutralisées

### Observation

Toute valeur de `sensor.clim_target_mode` autre que `off`, `cool`, `dry` ou `heat` retourne `false`.

### Signification structurelle

Le capteur ne qualifie pas ces états comme incohérents.
Ils sont explicitement sortis du périmètre de détection dans cette implémentation.

---

## 6. Dépendance indirecte à la stabilisation locale

### Observation

Le capteur lit `sensor.clim_mode_local`, qui est lui-même un capteur à fallback local et à trigger de stabilisation.

### Signification structurelle

La cohérence n'est pas comparée directement à `climate.clim`, mais à une lecture locale déjà stabilisée par une couche intermédiaire.
Le capteur de cohérence hérite donc indirectement des propriétés de résilience de `clim_mode_local`.

---

## 7. Pas de distinction entre divergence partielle et divergence totale

### Observation

Le résultat est binaire :
- `on` si au moins une condition d'incohérence est vraie
- `off` sinon

### Signification structurelle

Le capteur ne distingue pas :
- "puissance correcte mais mode faux"
- "mode correct mais puissance fausse"
- "les deux faux"

Toutes ces situations sont agrégées dans un unique état `on`.

---

## 8. `device_class: problem` donne une sémantique HA native

### Observation

Le YAML définit `device_class: problem`.

### Signification structurelle

L'entité porte explicitement une sémantique native Home Assistant d'anomalie / problème.
Contrairement à plusieurs capteurs précédents du domaine, cette sémantique est portée directement par le contrat technique du capteur.

---

## 9. Capteur de cohérence mono-cible

### Observation

Le diagnostic repose exclusivement sur `sensor.clim_target_mode` comme vérité décisionnelle.

### Signification structurelle

La chaîne de cohérence est centrée sur une cible finale unique.
Le capteur ne compare pas les besoins, les autorisations ou les blocages séparément ; il compare seulement le résultat décisionnel final au réel observé.
