# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M5)
#     INTERACTION AVEC M3 (GARDE-FOU STRUCTUREL)
# ==========================================================

## 🎯 OBJET

Décrire l’interaction normative entre M5 et M3.

M5 agit comme mécanisme de suspension
vis-à-vis de l’analyse ΔT.

---

## 🧩 MÉCANISME

Le pipeline impose, avant exécution de M3 :

1️⃣ Conditions structurelles :

- `chauffage_blocage_aeration = on`
- `aeration_pipeline_arme = on`
- `binary_sensor.contact_fenetres_maison = off`

2️⃣ Condition temporelle :

- délai minimal écoulé entre :
  `input_datetime.aeration_reouverture_last`
  et l’instant courant.

Ce délai est défini par :

- `input_number.delai_stabilisation_capteurs`

L’évaluation est réalisée au moment du déclencheur
`timer.finished` de `timer.aeration_analyse_delta_t`.

---

## 🔒 EFFET STRUCTUREL

Une réouverture récente :

- empêche l’analyse ΔT prématurée,
- empêche l’exécution de M3 tant que :
  - l’enveloppe n’est pas refermée,
  - le délai de stabilisation n’est pas écoulé.

M5 ne programme aucun déclenchement différé.
Il modifie uniquement l’état permettant ou non
l’exécution de M3.

---

## 🛑 INTERDIT

M5 ne doit jamais :

- déclencher M3 directement,
- contourner le pipeline,
- lever ou raccourcir un blocage,
- altérer la monotonicité des échéances,
- supprimer l’exigence d’enveloppe fermée.

La décision ΔT reste exclusivement de compétence M3.

# ==========================================================