# cardio_nuit.md
**Arsenal — Domaine Santé / Cardio nocturne**
Version : 2.1
Statut : NORMATIF (implémenté — documente le runtime existant)
Auteur : Arsenal Architecture
Date : 2026-06-07

---

## 1. Objet

Ce contrat définit les règles de collecte, de consolidation, d'interprétation et d'exposition des données de fréquence cardiaque nocturne dans Arsenal.

Il couvre :
- le snapshot cardio (couche Perception)
- les capteurs métier dérivés (couche Décision)
- les invariants et seuils de validité
- les règles d'alimentation de l'UI

Il ne couvre pas :
- la fréquence cardiaque diurne (hors périmètre v1)
- la variabilité HRV (réservée v2 si donnée disponible)
- les automations d'alerte santé : **hors périmètre de ce contrat et non contractualisées à ce jour** (aucun contrat d'alerte santé n'existe dans Arsenal ; ce contrat ne prétend pas qu'elles sont couvertes)

---

## 2. Source de données

| Propriété | Valeur |
|---|---|
| Source unique | Withings Sleep Analyzer (via intégration Home Assistant locale) |
| Entité source | `sensor.withings_average_heart_rate_local` |
| Valeur exposée | FC moyenne sur l'épisode de sommeil, consolidée par le Sleep Analyzer. Arsenal ne recalcule pas cette valeur. |
| Fenêtre temporelle | Non calculée par Arsenal. La valeur est déjà consolidée par Withings sur l'épisode de sommeil. Arsenal lit uniquement la dernière valeur stable disponible lors de la consolidation matinale. |
| Déclenchement | Au réveil détecté (via snapshot sommeil) ou à 08h30 au plus tard |
| Règle de stabilité | Une valeur est consolidable si : (1) elle est numérique, (2) elle est différente de 0, (3) elle est dans la plage physiologique définie (§3.2), (4) elle est identique depuis au moins 30 minutes ou confirmée sur deux lectures successives. Arsenal retient la valeur stable la plus récente au moment de la consolidation. Si aucune valeur stable n'est disponible → `raison_invalidite = source_indisponible`. `duree_stabilite` = durée écoulée depuis le dernier changement d'état observé sur la source Withings. |

**Règle d'or** : aucune entité UI, aucun script décisionnel ne lit directement les entités Withings. Toute consommation passe par le snapshot.

---

## 3. Snapshot cardio (couche Perception)

### 3.1 Entités

| Entité | Type | Unité | Description |
|---|---|---|---|
| `input_number.cardio_nuit_moyenne` | input_number | bpm | FC moyenne sur l'épisode de sommeil, lue depuis Withings |
| `input_number.cardio_nuit_duree_stabilite` | input_number | min | Durée depuis le dernier changement d'état observé sur la source Withings, au moment de la consolidation |
| `input_boolean.cardio_nuit_valide` | input_boolean | — | TRUE si la valeur est consolidable (règle de stabilité §2 respectée) |
| `input_boolean.cardio_anomalie_nuit_precedente` | input_boolean | — | TRUE si une condition d'anomalie était active la nuit J-1. Permet le calcul de l'attribut `confirmation` sur `binary_sensor.cardio_anomalie`. Mis à jour par `script.consolider_cardio_nuit` en fin de consolidation. |
| `input_text.cardio_nuit_raison_invalidite` | input_text | — | Raison d'invalidation : `hors_plage` / `source_indisponible` / `valeur_zero`. Valeur `none` si snapshot valide. |
| `input_text.cardio_nuit_historique_7j` | input_text | JSON | Tableau JSON des FC moyennes des 7 dernières nuits valides. Utilisé par `sensor.cardio_baseline_7j`. Seules les nuits où `cardio_nuit_valide = TRUE` alimentent ce tableau. |
| `input_datetime.cardio_nuit_horodatage` | input_datetime | — | Timestamp de la dernière consolidation |

### 3.2 Plages de validité technique

Ces plages définissent les bornes physiologiquement impossibles. Toute valeur hors plage → snapshot invalidé, `cardio_nuit_valide = FALSE`, `raison_invalidite = hors_plage`.

| Champ | Borne min | Borne max |
|---|---|---|
| `cardio_nuit_moyenne` | 35 bpm | 90 bpm |

### 3.3 Responsabilité de mise à jour

Un script unique `script.consolider_cardio_nuit` est seul autorisé à écrire dans les helpers du snapshot. Il est déclenché :
- par l'automation de consolidation matinale (après détection réveil ou à 08h30)
- jamais manuellement en production

---

## 4. Baseline dynamique (couche Décision — niveau 1)

### 4.1 Entité

| Entité | Type | Unité | Description |
|---|---|---|---|
| `sensor.cardio_baseline_7j` | sensor (template) | bpm | Moyenne glissante des FC moyennes nocturnes sur les 7 dernières nuits valides, calculée depuis `input_text.cardio_nuit_historique_7j` |

### 4.2 Règles de calcul

- Lit `input_text.cardio_nuit_historique_7j` (tableau JSON, max 7 entrées, FIFO)
- N'utilise que les valeurs présentes dans ce tableau — toutes sont déjà issues de nuits valides
- Si moins de 4 entrées disponibles → état `indisponible`, pas de valeur exposée
- Arrondi à 1 bpm près

### 4.3 Invariant

> La baseline ne peut jamais être calculée à partir d'une nuit invalidée. Aucune exception.

---

## 5. Capteurs métier (couche Décision — niveau 2)

### 5.1 `sensor.cardio_nuit_delta_baseline`

| Propriété | Valeur |
|---|---|
| Type | sensor (template) |
| Unité | bpm |
| Description | `cardio_nuit_moyenne − cardio_baseline_7j` |
| Disponibilité | Uniquement si `cardio_nuit_valide = TRUE` ET baseline disponible |
| État si indisponible | `indisponible` |

Interprétation :
- `< −5 bpm` → récupération exceptionnelle
- `[−5 ; +3]` → dans la norme personnelle
- `[+3 ; +8]` → légèrement élevé
- `> +8 bpm` → anormal

---

### 5.2 `sensor.cardio_nuit_etat`

| Propriété | Valeur |
|---|---|
| Type | sensor (template) |
| États possibles | `optimal` / `normal` / `eleve` / `anormal` / `indisponible` |
| Description | Évaluation qualitative de la nuit cardio |

Logique de qualification (priorité descendante) :

1. Si `cardio_nuit_valide = FALSE` → `indisponible`
2. Si baseline indisponible → qualification sur valeurs absolues uniquement (§5.2.1)
3. Si `delta_baseline > +8` → `anormal`
4. Si `delta_baseline > +3` → `eleve`
5. Si `delta_baseline < −5` → `optimal`
6. Sinon → `normal`

**5.2.1 Qualification sans baseline (valeurs absolues)**

| État | Condition |
|---|---|
| `anormal` | `cardio_nuit_moyenne > 72` |
| `eleve` | `cardio_nuit_moyenne > 65` |
| `optimal` | `cardio_nuit_moyenne ≤ 55` |
| `normal` | tous autres cas |

> Ces seuils absolus sont des valeurs Arsenal par défaut. Ils doivent être revus après 30 nuits de baseline disponible.

---

### 5.3 `binary_sensor.cardio_anomalie`

| Propriété | Valeur |
|---|---|
| Type | binary_sensor (template) |
| État ON | anomalie détectée |
| État OFF | pas d'anomalie ou données insuffisantes |

Conditions d'activation :
- `sensor.cardio_nuit_etat = anormal`

**Attribut `confirmation`** : booléen exposé par le binary_sensor.
- `true` si `input_boolean.cardio_anomalie_nuit_precedente = TRUE` (anomalie également présente la nuit J-1)
- `false` si c'est la première occurrence

L'UI doit distinguer visuellement `confirmation = false` (vigilance) de `confirmation = true` (anomalie confirmée). Une anomalie non confirmée ne justifie pas de notification active.

**Invariant** : `binary_sensor.cardio_anomalie` ne peut pas être ON si `cardio_nuit_valide = FALSE`. Une nuit invalide n'est jamais une anomalie, c'est une absence de donnée.

**Comportement sur nuit invalide** : en cas de nuit invalide, `input_boolean.cardio_anomalie_nuit_precedente` n'est pas modifié. Une nuit invalide ne casse pas la continuité de détection d'anomalie entre deux nuits valides. La confirmation peut donc rester active à travers une nuit invalide intercalée.

---

## 6. Règles d'exposition UI

- L'UI lit exclusivement : `sensor.cardio_nuit_etat`, `sensor.cardio_nuit_delta_baseline`, `binary_sensor.cardio_anomalie`
- L'UI ne lit jamais : les helpers `input_number.*` directement, ni les entités Withings
- En cas d'état `indisponible` : afficher un indicateur neutre (pas d'alerte, pas de valeur fictive)
- Le delta baseline est affiché avec signe explicite (`+3 bpm`, `−2 bpm`)

---

## 7. Interactions avec les autres domaines

| Domaine | Nature de l'interaction |
|---|---|
| Sommeil ([`sommeil.md`](sommeil.md)) | Fournit le signal de réveil déclenchant la consolidation matinale. `cardio_nuit_etat` peut enrichir l'évaluation qualité sommeil (corrélation, non substitution). Couplage unidirectionnel : cardio consomme sommeil, jamais l'inverse. |
| Alertes santé | `binary_sensor.cardio_anomalie` (avec `confirmation = true`) est l'input candidat pour un contrat d'alerte dédié |
| Journalisation | Chaque consolidation est loggée avec horodatage, statut de validité et raison d'invalidation |

---

## 8. Évolutions réservées (hors périmètre v1)

| Évolution | Version cible |
|---|---|
| FC min / max / amplitude nocturne (si Withings expose ces données) | v2 |
| HRV / variabilité fine (si Withings expose la donnée) | v2 |
| Cardio diurne (activité, effort) | v2 |
| Baseline 30j (dérive lente, fatigue chronique) + double lecture delta | v2 |
| Corrélation cardio × sommeil × activité (score composite) | v3 |
| Seuils personnalisés auto-ajustés (apprentissage baseline longue) | v3 |

---

## 9. Violations du contrat

Constituent une violation :
- Écriture dans un helper snapshot par autre chose que `script.consolider_cardio_nuit`
- Écriture dans `input_text.cardio_nuit_historique_7j` par autre chose que `script.consolider_cardio_nuit`
- Lecture directe des entités Withings par l'UI ou un script décisionnel
- Activation de `binary_sensor.cardio_anomalie` sur nuit invalide
- Alimentation de `cardio_nuit_historique_7j` avec une valeur issue d'une nuit invalide
- Calcul de baseline avec moins de 4 entrées dans l'historique
- Exposition d'une valeur numérique quand l'état est `indisponible`

---

## 10. Changelog du contrat

| Version | Date | Motif |
|---|---|---|
| 1.0.0 | 2026-05-04 | Création initiale — périmètre nocturne, baseline 7j, trois capteurs métier |
| 1.1.0 | 2026-05-04 | Fenêtre temporelle dérivée snapshot sommeil (+ fallback) ; variabilité fixée à amplitude uniquement ; attributs `raison_invalidite` + `duree_donnees` sur `cardio_nuit_valide` ; attribut `confirmation` sur `cardio_anomalie` ; faux positifs documentés ; arrondi baseline ramené à 1 bpm ; baseline 30j ajoutée en évolutions réservées v2 ; interactions domaines précisées (couplage unidirectionnel) |
| 1.2.0 | 2026-05-04 | Mémoire `confirmation` contractualisée : ajout de `input_boolean.cardio_anomalie_nuit_precedente` dans le snapshot ; statut passé en READY FOR IMPLEMENTATION |
| 2.0.0 | 2026-05-05 | **Refonte sur audit source réelle.** Entité source corrigée (`sensor.withings_average_heart_rate_local`). Suppression de `cardio_nuit_min`, `cardio_nuit_max`, `cardio_nuit_variabilite` (entités fantômes). Fenêtre temporelle supprimée. Règle de stabilité 30 min ajoutée. Logique `cardio_nuit_etat` et `cardio_anomalie` allégées. |
| 2.0.1 | 2026-05-05 | Ajout `input_number.cardio_nuit_duree_stabilite` et `input_text.cardio_nuit_historique_7j` dans le snapshot. Précision "valeur stable la plus récente". Baseline §4.2 mise à jour. Violations complétées. |
| 2.0.2 | 2026-05-05 | §5.3 : comportement sur nuit invalide documenté — `cardio_anomalie_nuit_precedente` préservé (non remis à zéro). Continuité de détection maintenue à travers une nuit invalide intercalée. |
| 2.1 | 2026-06-07 | Promotion du statut pré-implémentation vers **NORMATIF (implémenté)** : le contrat documente un runtime existant et conforme (consolidation `cardio_consolidation.yaml`, capteurs métier `cardio_nuit_etat` / `cardio_nuit_delta_baseline` / `cardio_anomalie` / `cardio_baseline_*`, snapshot helpers, couleur UI). Réparation de deux références héritées : renvoi sommeil corrigé vers `sommeil.md` ; retrait du renvoi d'alerte santé inexistant (alerte santé hors périmètre, non contractualisée à ce jour). Aucun changement de règle ni d'entité. |
