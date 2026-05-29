# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M5)
#     RÉOUVERTURE PENDANT BLOCAGE — SUSPENSION TEMPORAIRE
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de M5 :

- tracer une réouverture d’ouvrant
  survenant pendant un blocage chauffage actif,
- suspendre / repousser l’exécution des échéances
  liées à l’épisode en cours.

M5 n’est pas une nouvelle entrée d’épisode.
Il agit exclusivement à l’intérieur d’un blocage actif.

---

## 🧩 AUTORITÉ (mise à jour)

- Script exécuté : `script.aeration_m5_reouverture_pendant_blocage`
- Appelé exclusivement par le pipeline maître.

Conditions imposées par le pipeline :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `binary_sensor.ouverture_qualifiee_maison = on`

Définition normative :

> Une **réouverture qualifiée** correspond exclusivement à l’état  
> `binary_sensor.ouverture_qualifiee_maison`.

Ce capteur constitue la frontière contractuelle unique entre  
le sous-système *Ouvertures* et le moteur M5.

Il agrège :

- les ouvertures **immédiates** (entrée, chambres enfants),
- les ouvertures **confirmées après délai** (séjour, chambre parents),

sans inclure les tentatives en grâce ni les agrégats techniques bruts.

---

## 🔁 ACTIVATION DE SUSPENSION

En plus de l’horodatage :

- `input_boolean.aeration_suspension_active` → ON

Ce booléen matérialise l’état de suspension
des échéances temporelles.

Il est exclusivement géré par M5 et M6.

---

## 🔁 EFFETS NORMATIFS

### 1️⃣ Horodatage

M5 enregistre :

- `input_datetime.aeration_reouverture_last = now()`

Ce timestamp sert de référence
au garde-fou post-réouverture (M3).

---

### 2️⃣ Suspension / Réarmement temporel (monotone)

M5 peut :

- recalculer une durée minimale basée sur
  `input_number.delai_stabilisation_capteurs`,
- redémarrer les timers :
  - `timer.aeration_analyse_delta_t`
  - `timer.aeration_blocage`

uniquement de manière monotone :

- jamais de réduction,
- jamais de levée,
- jamais de déclenchement immédiat.

Objectif :

> Empêcher l’exécution de M3 ou M4
> tant que l’enveloppe n’est pas stabilisée.

---

## 🧊 PROPRIÉTÉ STRUCTURELLE

M5 ne modifie jamais :

- `chauffage_blocage_aeration`,
- `aeration_pipeline_arme`,
- les snapshots T_REF,
- les échéances datetime cibles définies en M2.

Il agit uniquement sur l’exécution des timers.

---

## 🛑 INTERDITS

M5 ne doit jamais :

- lever le blocage,
- désarmer le pipeline,
- initier une action thermique,
- créer un nouvel épisode,
- réduire une échéance existante.

La reprise normale des échéances relève de M6.

# ==========================================================