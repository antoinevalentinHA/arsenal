# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     INVALIDATION TENTATIVE NON CONFIRMÉE
# ==========================================================

## 🎯 OBJET

Définir le mécanisme garantissant qu’une tentative d’aération
en phase de grâce est annulée proprement si toutes les ouvertures
sont refermées avant confirmation.

Référence implémentation :
- Automation : "Aération - Invalidation tentative non confirmée"
- ID : `10170000000010`

---

## 🧩 CONTEXTE CONCEPTUEL

Certaines ouvertures (Séjour / Parents) utilisent un délai de confirmation
("phase de grâce") avant de qualifier un épisode d’aération réel.

Pendant cette phase :

- `aeration_episode_en_cours = on`
- `aeration_confirmee = off`
- aucun blocage chauffage n’est encore actif

Il s’agit d’un état transitoire.

---

## 🎯 RÔLE NORMATIF

Cette automation :

- annule proprement la tentative si la phase de grâce s’interrompt,
- évite qu’un pseudo-épisode persiste,
- empêche toute entrée accidentelle en M2.

Elle constitue un garde-fou logique pré-pipeline.

---

## 🔁 DÉCLENCHEMENT

Trigger :

- `binary_sensor.tentative_aeration_en_grace`
  passe de `on` à `off`

Ce passage signifie :

- fermeture complète avant confirmation.

---

## ✅ CONDITIONS STRICTES

L’invalidation n’est exécutée que si :

1) `input_boolean.systeme_stable = on`

2) `input_boolean.aeration_episode_en_cours = on`

3) `input_boolean.aeration_confirmee = off`

Donc :

- aucune aération confirmée
- aucun blocage chauffage actif
- aucune analyse DeltaT programmée

---

## 🔧 EFFET NORMATIF

Action unique :

- `input_boolean.aeration_episode_en_cours` → OFF

Aucun autre effet.

---

## 🚫 INTERDITS ABSOLUS

Il est strictement interdit :

- d’activer un blocage chauffage ici,
- de démarrer un timer,
- d’émettre une demande de recover,
- d’appeler le pipeline maître,
- d’altérer un snapshot thermique,
- de déclencher une décision métier.

---

## 🧠 POSITION DANS L’ARCHITECTURE

Ce mécanisme :

- agit en amont de M2,
- ne fait pas partie des branches M1..M5,
- garantit qu’un épisode ne peut exister sans confirmation.

Il prévient :

- les faux épisodes,
- les blocages fantômes,
- les analyses DeltaT injustifiées.

---

## 🛡️ PROPRIÉTÉS STRUCTURELLES

- Zéro wait
- Idempotent
- Strictement logique
- Non intrusif
- Compatible post-boot

# ==========================================================