# axe_temperature.md
# Arsenal — Contrat d'axe : Température intérieure
# Version : 1.1
# Statut : normatif
# Dépend de : meteo.md, validation.md,
#             fallback.md

---

## 1. Objet

Définir les paramètres locaux applicables à l'axe température
intérieure dans Arsenal.

Ce contrat ne redéfinit pas la validation ni le fallback.
Il fournit uniquement les paramètres que ces contrats
lui délèguent.

---

## 2. Sources déclarées

| Rôle     | Gabarit d'entité            | Technologie |
|----------|-----------------------------|-------------|
| Primaire | sensor.temperature_<zone>_1 | HomeKit     |
| Secours  | sensor.temperature_<zone>_2 | Zigbee      |

`<zone>` représente l'identifiant de la zone thermique
(chambre_arnaud, chambre_matthieu, sejour, etc.).

Les deux sources doivent mesurer la même grandeur physique
et être situées dans la même zone thermique.
Aucune autre substitution n'est autorisée.

---

## 3. Plage de plausibilité

| Borne   | Valeur |
|---------|--------|
| Minimum | 8 °C   |
| Maximum | 40 °C  |

Toute valeur hors de cette plage est invalide
au sens de validation.md §4,
même si elle est techniquement exploitable.

---

## 4. Dépendances critiques

Aucune dépendance critique déclarée pour cet axe.
Les sources sont indépendantes entre elles.

---

## 5. Niveau 3 — mémoire de continuité

Le niveau 3 est **autorisé** pour cet axe.

TTL_effectif = TTL_DEFAULT (30 minutes).
Aucune dérogation.

Toute implémentation Home Assistant de cet axe DOIT embarquer
un trigger `time_pattern` de période ≤ 30 minutes afin de
permettre l'expiration effective du TTL.

---

## 6. Unité et arrondi

| Paramètre | Valeur |
|-----------|--------|
| Unité     | °C     |
| Arrondi   | 0.1 °C |

---

## 7. Renvois contractuels

- Cadre du domaine → [`meteo.md`](meteo.md)
- Validation       → [`validation.md`](validation.md)
- Fallback         → [`fallback.md`](fallback.md)