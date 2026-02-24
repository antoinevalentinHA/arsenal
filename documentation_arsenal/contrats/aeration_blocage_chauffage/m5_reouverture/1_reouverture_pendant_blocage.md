# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M5)
#     RÉOUVERTURE PENDANT BLOCAGE — CADRE GÉNÉRAL
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif de M5 :

- tracer une réouverture d’ouvrant
  survenant pendant un blocage chauffage actif.

M5 est strictement informatif.

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m5_reouverture_pendant_blocage`
- Appelé exclusivement par le pipeline maître.

Le pipeline impose notamment :

- déclencheur : ouverture détectée,
- `chauffage_blocage_aeration = on`,
- `aeration_pipeline_arme = on`,
- `fenetre_ouverte_maison_avec_delai = on`.

---

## 🔁 EFFET NORMATIF UNIQUE

M5 enregistre :

- `input_datetime.aeration_reouverture_last = now()`

Format :
- `YYYY-MM-DD HH:MM:SS`

---

## 🛑 INTERDITS

M5 ne doit jamais :

- modifier le blocage,
- modifier un timer,
- déclencher une analyse ΔT,
- désarmer le pipeline,
- déclencher une action thermique.

# ==========================================================