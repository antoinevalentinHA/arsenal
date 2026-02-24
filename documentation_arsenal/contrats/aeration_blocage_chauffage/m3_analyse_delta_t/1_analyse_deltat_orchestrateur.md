# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     ANALYSE DELTAT — ORCHESTRATEUR
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de M3 :

- calculer le ΔT maximal observé sur un ensemble de zones,
- déterminer une prolongation de blocage en heures (0..3),
- déléguer l’exécution à un script dédié :
  - prolongation monotone,
  - ou maintien du blocage.

M3 ne lève jamais le blocage.
M3 ne déclenche jamais de reprise thermique.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m3_analyse_deltat`
- Appelé exclusivement par le pipeline maître via événement :
  `timer.finished` sur `timer.aeration_analyse_delta_t`
- Exécution conditionnée côté pipeline à :
  - `chauffage_blocage_aeration = on`
  - `aeration_pipeline_arme = on`
  - garde-fou post-réouverture (voir M5)

---

## 🔁 SÉQUENCE NORMATIVE (ORDRE STRICT)

1. Calcul `delta_max`
2. Détermination `prolongation_heures` (0..3)
3. Publication diagnostic : `input_number.delta_t_max_decisionnel_aeration`
4. Routage :
   - si `prolongation_heures > 0` → `script.aeration_m3_prolonger_blocage`
   - sinon → `script.aeration_m3_maintenir_blocage`

---

## 🛑 INTERDITS

M3 ne doit jamais :

- lever `chauffage_blocage_aeration`,
- arrêter `timer.aeration_blocage`,
- désarmer `aeration_pipeline_arme`,
- piloter un actionneur thermique,
- contourner la monotonicité (toute prolongation doit être monotone).

# ==========================================================