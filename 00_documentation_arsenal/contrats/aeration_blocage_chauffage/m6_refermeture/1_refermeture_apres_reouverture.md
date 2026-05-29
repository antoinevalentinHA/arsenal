# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M6)
#     RÉFERMETURE APRÈS RÉOUVERTURE — CADRE GÉNÉRAL
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de M6 :

- intervenir lors de la fermeture d’un ouvrant
  après une réouverture survenue pendant blocage,
- réactiver l’exécution des échéances suspendues,
- préserver strictement la monotonicité définie en M2/M3.

M6 ne constitue pas une nouvelle analyse.
M6 ne constitue pas une nouvelle décision.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m6_refermeture`
- Appelé exclusivement par le pipeline maître.

Conditions imposées par le pipeline :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `binary_sensor.contact_fenetres_maison = off`
- au moins une réouverture préalablement tracée (M5)

---

## 🔁 RÔLE STRUCTUREL

M6 agit comme mécanisme de reprise.

Il intervient lorsque :

- une suspension temporelle a été déclenchée par M5,
- l’enveloppe redevient fermée,
- le blocage est toujours actif.

---

## 🎯 CONDITION D’EXÉCUTION

M6 ne peut exécuter une reprise que si :

- `input_boolean.aeration_suspension_active = on`

Sinon :

- M6 est neutre (no-op).

---

## 🔁 EFFETS NORMATIFS

1. Reprise des timers selon échéances existantes
2. `input_boolean.aeration_suspension_active` → OFF

---

## 🔧 EFFETS NORMATIFS

M6 :

1️⃣ Relit les échéances normatives existantes :

- `input_datetime.chauffage_fin_blocage_aeration`
- `input_datetime.analyse_deltat_disponible`

2️⃣ Recalcule les durées restantes :

- `fin_cible - now`
- bornées à `>= 0`

3️⃣ Redémarre les timers correspondants :

- `timer.aeration_blocage`
- `timer.aeration_analyse_delta_t`

M6 redémarre systématiquement les timers sur la base des échéances existantes.
Si l'échéance est expirée (fin_cible - now ≤ 0), 
le timer est redémarré avec la durée minimale 
(delai_stabilisation_capteurs pour l'analyse, delai_stabilisation_capteurs + 1 min pour le blocage).
M6 garantit toujours un timer actif à la sortie.

---

## 🧊 PROPRIÉTÉ STRUCTURELLE

M6 :

- ne modifie jamais les échéances datetime,
- ne prolonge jamais un blocage,
- ne réduit jamais une échéance,
- ne modifie jamais les snapshots T_REF,
- ne déclenche jamais M3 ou M4 directement.

Il restaure uniquement l’exécution des échéances existantes.

---

## 🛑 INTERDITS

M6 ne doit jamais :

- lever `chauffage_blocage_aeration`,
- désarmer `aeration_pipeline_arme`,
- créer une nouvelle échéance,
- altérer la monotonicité définie en M2/M3,
- initier une action thermique.

---

## 🧠 POSITION DANS LE CYCLE

Cycle canon :

    M1 → M2 → (M5 / M6 éventuels) → M3 → M4

M6 ne crée pas un nouveau cycle.
Il restaure l’exécution du cycle en cours.

# ==========================================================