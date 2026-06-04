# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · MINI-GUARD PIPELINE — ANTI-ZOMBIE (V3 PRO)

## 🎯 OBJET

Définir le garde-fou runtime empêchant tout état "pipeline zombie" :

- pipeline armé alors qu’aucun épisode n’est actif,
- aucun blocage chauffage n’est actif,
- aucune ouverture physique n’est active.

Référence implémentation :
- Automation : "Chauffage – Aération – Mini-guard pipeline (anti-zombie)"
- ID : `10010000000024`

---

## 🧩 RÔLE NORMATIF

Cette automation :

- n’initie rien,
- ne décide rien,
- ne fait que remettre en cohérence par :
  - annulation des timers aération résiduels,
  - désarmement du pipeline.

Elle protège contre :

- les triggers `timer.finished` fantômes,
- la persistance indue d’un pipeline armé.

---

## 🚫 CE QUE CE GARDE-FOU NE FAIT PAS

- ne crée pas d’épisode (M1),
- n’active pas de blocage (M2),
- n’analyse pas le ΔT (M3),
- ne lève pas un blocage (M4),
- ne modifie pas de snapshots T_REF,
- ne pilote aucun actionneur thermique.

---

## 🔁 DÉCLENCHEURS (SURVEILLANCE LARGE)

La mini-guard se déclenche sur :

### États fonctionnels
- `input_boolean.aeration_episode_en_cours`
- `input_boolean.chauffage_blocage_aeration`
- `binary_sensor.fenetre_ouverte_maison`
- `input_boolean.aeration_pipeline_arme`

### Timers aération (anti réveil fantôme)
- `timer.aeration_analyse_delta_t`
- `timer.aeration_blocage`

### Post-boot
- `input_boolean.systeme_stable` passe à `on`

Finalité :

- revalider la cohérence à chaque changement pertinent,
- neutraliser immédiatement tout résidu.

---

## ✅ CONDITIONS STRICTES (CAS "PIPELINE ZOMBIE")

Pré-requis :

- `input_boolean.aeration_pipeline_arme = on`

Et simultanément :

- `input_boolean.aeration_episode_en_cours = off`
- `input_boolean.chauffage_blocage_aeration = off`
- `binary_sensor.fenetre_ouverte_maison = off`

Ce garde-fou ne s’exécute que dans ce cas.

---

## 🔧 EFFETS NORMATIFS (ORDRE STRICT)

1) Annulation timers résiduels :
- `timer.aeration_analyse_delta_t` → cancel
- `timer.aeration_blocage` → cancel

2) Désarmement pipeline :
- `input_boolean.aeration_pipeline_arme` → off

3) Journalisation logbook :
- name : "Chauffage - Aération - Mini-guard"
- message : pipeline désarmé + timers annulés
- entity_id : `input_boolean.aeration_pipeline_arme`

---

Après désarmement du pipeline, neutraliser les datetimes résiduelles :
- input_datetime.chauffage_fin_blocage_aeration → YYYY-MM-DD 00:00:00
- input_datetime.analyse_deltat_disponible → YYYY-MM-DD 00:00:00

L'état résultant doit correspondre à l'état canon 1 (repos total).

---

## 🧠 POSITIONNEMENT DANS LA GOUVERNANCE

Ce garde-fou :

- corrige un état zombie de façon immédiate,
- sans passer par un mécanisme de "recover demandé".

Il est donc :

- **complémentaire** de `binary_sensor.chauffage_aeration_coherence_ko`
  (détection exhaustive multi-cas),
- **complémentaire** de `10010000000029` (signal recover),
- **compatible** avec M0 (recover ciblé) qui traite d’autres cas.

---

## 🛑 INTERDITS ABSOLUS

Il est strictement interdit :

- d’annuler des timers si un épisode est actif,
- de désarmer le pipeline si une ouverture est active,
- de déclencher une action thermique ou une remédiation métier.

# ==========================================================