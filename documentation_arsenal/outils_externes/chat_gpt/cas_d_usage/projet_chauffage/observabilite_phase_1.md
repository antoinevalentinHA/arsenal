# ==========================================================

# 🧠 PROJET ARSENAL — OBSERVABILITÉ THERMIQUE

# Phase 1 — Référentiel des capteurs & métriques diagnostics

# ==========================================================

---

## 🎯 Objet

Ce document définit le **référentiel normatif de l’observabilité thermique – Phase 1** du projet Chauffage Arsenal.

Il formalise :

* les **familles de métriques autorisées**
* les **capteurs diagnostics à produire**
* leur **rôle exact**
* leur **statut architectural**
* leurs **dépendances**
* les **règles d’exploitation**

Ce document est :

* **NORMATIF**
* fondation de toute implémentation YAML Phase 1
* opposable à toute évolution ultérieure

Il ne décrit :

* ni logique d’auto-ajustement
* ni scripts d’action
* ni automatisme

---

## 🧠 Principe fondamental

La Phase 1 est **strictement observatoire**.

Tout capteur Phase 1 :

* ne décide jamais
* n’agit jamais
* ne modifie aucun paramètre
* n’introduit aucune boucle

Il **observe**, **mesure**, **qualifie**, et **documente**.

> L’auto-ajustement ne peut s’appuyer que sur des données
> explicables, traçables et stables.

---

## 🧱 Séparation fonctionnelle absolue

Trois catégories non miscibles :

### 1️⃣ Capteurs de faits physiques

* températures
* dérives
* vitesses
* durées

### 2️⃣ Capteurs de phénomènes thermiques

* inerties
* overshoots
* délais
* oscillations

### 3️⃣ Capteurs de synthèse

* moyennes
* distributions
* stabilités

Aucun capteur Phase 1 :

* ne lit d’offset
* ne lit de consigne cible
* ne lit de seuil décisionnel

Ils observent **le système réel**, pas la logique.

---

## 🌡️ Référentiel de base — Grandeur primaire

### Capteur de référence thermique unique

| Élément        | Valeur                                  |
| -------------- | --------------------------------------- |
| Capteur maître | `sensor.temperature_min_chambres`       |
| Rôle           | point thermique critique bâtiment       |
| Usage          | référence pour toutes métriques Phase 1 |

Règle absolue :

* **un seul capteur de référence** pour toute Phase 1
* aucune moyenne multi-zones
* aucune fusion

---

## 🔁 Événements structurants observables

Les métriques Phase 1 sont construites **exclusivement** autour de transitions décisionnelles :

### Transitions principales

| Transition        | Description       |
| ----------------- | ----------------- |
| reduced → comfort | reprise chauffage |
| comfort → reduced | arrêt chauffage   |

Source d’état :

* `input_select.chauffage_dernier_mode_decide`

Ces transitions sont les **seuls déclencheurs légitimes** de mesures d’inertie.

---

## 🧩 Famille A — Inertie post-reprise (offset présence)

### Phénomènes mesurés

* poursuite de refroidissement après reprise
* durée avant inversion de pente
* profondeur de sous-chauffe résiduelle

### Métriques canoniques

| Nom métrique             | Rôle                          |
| ------------------------ | ----------------------------- |
| ΔT_drop_presence         | amplitude de chute résiduelle |
| Δt_drop_presence         | durée de chute post-reprise   |
| vitesse_reprise_presence | vitesse moyenne de remontée   |

### Contraintes

* déclenchement uniquement sur transition reduced → comfort
* invalidation si régime ≠ CONFORT STABLE
* exclusion cycles < durée minimale

---

## 🧩 Famille B — Inertie post-arrêt (offset présence)

### Phénomènes mesurés

* poursuite de montée après arrêt
* overshoot thermique
* durée avant stabilisation

### Métriques canoniques

| Nom métrique              | Rôle                    |
| ------------------------- | ----------------------- |
| ΔT_rise_presence          | overshoot inertiel      |
| Δt_rise_presence          | durée overshoot         |
| vitesse_descente_presence | vitesse de décroissance |

### Contraintes

* déclenchement uniquement sur transition comfort → reduced
* invalidation si poêle actif ou blocage
* exclusion périodes instables

---

## 🧩 Famille C — Inertie en absence (offset absence)

### Phénomènes mesurés

* dérive thermique naturelle
* température plancher atteinte
* vitesse de perte thermique

### Métriques canoniques

| Nom métrique             | Rôle                       |
| ------------------------ | -------------------------- |
| T_min_absence            | minimum atteint en absence |
| vitesse_perte_absence    | pente moyenne de perte     |
| Δt_stabilisation_absence | temps avant stabilisation  |

### Contraintes

* régime ABSENCE PROLONGÉ uniquement
* exclusion inhibitions ponctuelles
* exclusion retours de présence

---

## 🔄 Famille D — Dynamique globale des cycles

### Phénomènes mesurés

* fréquence des bascules
* durée des phases
* amplitude des oscillations

### Métriques canoniques

| Nom métrique          | Rôle                |
| --------------------- | ------------------- |
| amplitude_oscillation | amplitude moyenne   |
| duree_cycle_moyenne   | durée cycle typique |
| cycles_par_jour       | fréquence           |

---

## 📊 Famille E — Synthèses temporelles

> Statut : NON IMPLÉMENTÉ EN PHASE 1  
> Nature : Couche analytique optionnelle post-instrumentation  
> Rôle : Consolidation long terme et préparation Phase 2  

La Famille E ne fait pas partie du socle instrumentale Phase 1.
Elle est activée uniquement après accumulation suffisante de cycles
et relève d’une extension analytique contrôlée (Phase 1.1 / Phase 2).

### Fenêtres autorisées

| Fenêtre                    | Usage              |
| -------------------------- | ------------------ |
| instantané                 | diagnostic brut    |
| glissant court (30–90 min) | phénomènes rapides |
| glissant long (6–24 h)     | stabilité          |

Règles :

* glissant court privilégié
* glissant long réservé synthèses
* aucune moyenne multi-régimes

---

## 🧠 Qualité & validité des données

Chaque métrique doit être qualifiée :

### États de validité

| État      | Signification       |
| --------- | ------------------- |
| valide    | exploitable         |
| invalide  | régime non conforme |
| incomplet | données manquantes  |

Aucune métrique invalide :

* ne doit alimenter Phase 2
* ne doit être agrégée

---

## 🔒 Exclusions formelles

Il est strictement interdit en Phase 1 :

* de lire des offsets
* de lire des seuils
* de lire des consignes
* de produire des recommandations
* de calculer des corrections
* de conditionner une action

Toute tentative constitue une **violation architecturale**.

---

## 🧠 Statut architectural

* Phase : Observabilité pure
* Autorité : Diagnostic
* Impact système : NUL
* Boucles : interdites
* Dépendance décision : aucune

---

## 📌 Finalité

Ce référentiel constitue :

* la **spécification directe des capteurs YAML Phase 1**
* la base unique de toute Phase 2
* la garantie de souveraineté thermique long terme

Aucun capteur Phase 1 ne peut être ajouté sans :

* appartenance claire à une famille
* rôle thermique explicite
* conformité aux régimes thermiques

---

## 🏷️ Statut

* Document projet Chauffage Arsenal
* Normatif et fondateur
* Applicabilité Phase 1 uniquement
* Toute évolution doit être documentée
