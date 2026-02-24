# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M4)
#     FIN BLOCAGE HORAIRE — CADRE GÉNÉRAL
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de M4 :

- lever le blocage chauffage,
- annuler explicitement les timers liés à l’épisode,
- neutraliser les traces temporelles résiduelles,
- désarmer le pipeline (clôture totale),
- journaliser.

M4 constitue l’unique mécanisme normatif de levée du blocage thermique.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m4_fin_blocage_horaire`
- Appelé exclusivement par le pipeline maître lorsque M4 est autorisé.

Le pipeline impose notamment :

- déclencheur : `timer.finished` sur `timer.aeration_blocage`
- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `timer.aeration_analyse_delta_t` **non actif**

---

## 🔁 EFFETS NORMATIFS (ORDRE STRICT)

1. Levée blocage :
   `chauffage_blocage_aeration` → OFF
2. Annulation timers :
   `timer.aeration_blocage` + `timer.aeration_analyse_delta_t` → cancel
3. Neutralisation traces datetime :
   `chauffage_fin_blocage_aeration` → `YYYY-MM-DD 00:00:00`
   `analyse_deltat_disponible` → `YYYY-MM-DD 00:00:00`
4. Désarmement pipeline :
   `aeration_pipeline_arme` → OFF
5. Logbook

---

## 🛑 INTERDITS

M4 ne doit jamais :

- démarrer un timer,
- déclencher M1/M2/M3,
- initier une action thermique,
- modifier des snapshots T_REF.

# ==========================================================