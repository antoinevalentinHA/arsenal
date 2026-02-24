# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M5)
#     INTERACTION AVEC M3 (GARDE-FOU)
# ==========================================================

## 🎯 OBJET

Décrire l’interaction normative entre M5 et M3.

---

## 🧩 MÉCANISME

Le pipeline impose, avant exécution de M3 :

- un délai minimal entre :
  `input_datetime.aeration_reouverture_last`
  et l’instant courant.

Ce délai est défini par :

- `input_number.delai_stabilisation_capteurs`

---

## 🔒 EFFET STRUCTUREL

Une réouverture récente :

- empêche l’analyse ΔT prématurée,
- garantit que M3 ne se déclenche pas
  tant que les capteurs ne sont pas stabilisés.

---

## 🛑 INTERDIT

M5 ne doit jamais :

- déclencher M3 directement,
- prolonger ou raccourcir un blocage,
- altérer la monotonicité des échéances.

# ==========================================================