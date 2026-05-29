# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (M3)
#     PROLONGER LE BLOCAGE — MONOTONICITÉ
# ==========================================================

## 🎯 OBJET

Définir le comportement normatif du script :

- `script.aeration_m3_prolonger_blocage`

Ce script est appelé par l’orchestrateur M3 lorsque
`prolongation_heures > 0`.

Il a deux responsabilités :

- mettre à jour la trace/diagnostic `input_datetime.chauffage_fin_blocage_aeration`,
- prolonger le timer `timer.aeration_blocage` de façon strictement monotone.

---

## 🧩 ENTRÉES

Champs attendus :

- `delta_max` (float)
- `prolongation_heures` (int)

Normalisation interne :

- `d = delta_max | float(0)`
- `h = prolongation_heures | float(0) — valeur en heures, fraction possible.

---

## 📆 CALCUL D’ÉCHÉANCE (TRACE) — MONOTONE MAX

Échéance proposée :

- `fin_blocage_proposee = now + h heures`

Échéance actuelle :

- `fin_blocage_actuelle = input_datetime.chauffage_fin_blocage_aeration | as_datetime`

Validité “actuelle” :

- considérée invalide si `none`,
- ou si heure/minute/seconde = `00:00:00`.

Échéance cible (monotone) :

- si l’échéance actuelle est valide et strictement postérieure à la proposition :
  → conserver l’échéance actuelle
- sinon :
  → adopter la proposition

Ce mécanisme interdit toute réduction de fin de blocage.

Les `input_datetime` représentent la cible normative,
indépendamment de l’état courant du timer.

---

## ⏱ TIMER BLOCAGE — MONOTONE SUR REMAINING

Le script lit :

- `timer.aeration_blocage` état `active` ou non,
- `remaining` si actif, sinon `00:00:00`,
- conversion en secondes : `blocage_remaining_s`.

Puis calcule :

- `blocage_cible_s = max(0, fin_blocage_cible - now)` en secondes.

Durée réellement appliquée (monotone) :

- `blocage_start_s = max(blocage_cible_s, blocage_remaining_s)`.

Démarrage effectif :

- le timer n’est relancé que si
  `blocage_start_s > blocage_remaining_s`.

Ce script ne force jamais une réduction.

---

## 🧊 INTERACTION AVEC M5 / M6

Ce script :

- n’annule jamais un timer,
- ne force jamais une reprise si le timer a été gelé,
- ne modifie pas l’état de suspension.

La suspension éventuelle des timers relève exclusivement de M5.
La reprise éventuelle relève exclusivement de M6.

Ce script agit uniquement si son exécution est autorisée
par le pipeline (enveloppe fermée).

---

## 🔧 EFFETS NORMATIFS

1. Mise à jour trace :

- `input_datetime.chauffage_fin_blocage_aeration = fin_blocage_cible`

2. Prolongation timer (si et seulement si repousse) :

- `timer.start(timer.aeration_blocage, duration=blocage_duration)`

3. Trace runtime

Aucune journalisation `logbook.log` n’est requise dans ce script.

La traçabilité normative est assurée par :

- `input_datetime.chauffage_fin_blocage_aeration`
- l’état du `timer.aeration_blocage`

Le script reste volontairement silencieux côté logbook afin d’éviter
une pollution événementielle pour un mécanisme interne de pipeline.

---

## 🛑 INTERDITS

Le script ne doit jamais :

- lever le blocage (`chauffage_blocage_aeration`),
- désarmer le pipeline,
- raccourcir le timer blocage,
- modifier le timer analyse ΔT,
- initier une action thermique,
- contourner une suspension décidée par M5.

# ==========================================================