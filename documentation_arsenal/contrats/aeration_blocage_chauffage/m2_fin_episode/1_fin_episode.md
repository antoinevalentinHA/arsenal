# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M2)
#     FIN D'ÉPISODE — CADRE GÉNÉRAL
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de l’étape M2 :

- clôture de l’épisode d’aération,
- activation du blocage chauffage,
- calcul des échéances M3 (analyse ΔT) et M4 (fin blocage),
- programmation monotone des timers,
- journalisation.

M2 ne prend aucune décision métier.
Il ne déclenche aucun redémarrage thermique.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m2_fin_episode`
- Appelé exclusivement par le pipeline maître.
- M2 n’est jamais appelé directement par M0, M3, M4 ou M5.

---

## 🔁 SÉQUENCE STRUCTURELLE (ORDRE STRICT)

1. `aeration_episode_en_cours` → OFF  
2. `chauffage_blocage_aeration` → ON  
3. Calcul des échéances cibles (monotone)  
4. Mise à jour des `input_datetime` de diagnostic  
5. Démarrage / extension monotone des timers  
6. `aeration_confirmee` → OFF  
7. Logbook

---

## 🛑 INTERDITS

M2 ne doit jamais :

- lever le blocage,
- appeler M3 ou M4 directement,
- déclencher une action thermique,
- raccourcir une échéance existante,
- modifier les snapshots T_REF.

# ==========================================================