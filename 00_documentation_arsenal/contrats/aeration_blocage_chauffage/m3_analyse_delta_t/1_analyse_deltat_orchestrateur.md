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
- Appelé exclusivement par le pipeline maître.
- Déclenché par événement :
  `timer.finished` sur `timer.aeration_analyse_delta_t`.

L’exécution est conditionnée côté pipeline à :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `binary_sensor.contact_fenetres_maison = off`
- respect du délai post-réouverture (M5)

M3 ne s’exécute jamais si une fenêtre est ouverte.

---

## 🔁 SÉQUENCE NORMATIVE (ORDRE STRICT)

1. Calcul `delta_max`
2. Détermination `prolongation_heures` (0..3)
3. Publication diagnostic :
   `input_number.delta_t_max_decisionnel_aeration`
4. Routage :
   - si `prolongation_heures > 0`
     → `script.aeration_m3_prolonger_blocage`
   - sinon
     → `script.aeration_m3_maintenir_blocage`

---

## 🧊 INTERACTION AVEC M5 / M6

Si une réouverture survient pendant blocage :

- M5 peut suspendre l’analyse,
- les timers peuvent être gelés,
- M3 est neutralisé tant que la maison reste ouverte.

M6 réarme l’exécution des timers après fermeture stable.

Les échéances définies en M2 restent monotones ;
M3 ne modifie jamais rétroactivement une cible.

---

## 🛑 INTERDITS

M3 ne doit jamais :

- lever `chauffage_blocage_aeration`,
- arrêter `timer.aeration_blocage`,
- désarmer `aeration_pipeline_arme`,
- piloter un actionneur thermique,
- contourner la monotonicité
  (toute prolongation doit être monotone),
- s’exécuter si une fenêtre est ouverte.

# ==========================================================