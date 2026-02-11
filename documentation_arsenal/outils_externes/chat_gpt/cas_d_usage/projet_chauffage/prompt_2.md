# 🧠 CONTEXTE — PROJET ARSENAL : OBSERVABILITÉ & AUTO-AJUSTEMENT THERMIQUE

Tu interviens dans un projet Home Assistant avancé nommé **ARSENAL**.
Architecture très contractuelle, orientée robustesse, souveraineté locale et observabilité thermique.

Objectif global :
Construire une **couche d’observabilité thermique de niveau industriel**
pour :
- mesurer inertie bâtiment + chaudière
- qualifier dynamiques post-reprise / post-arrêt
- rendre les offsets présence / absence mesurables et justifiables
- préparer un futur auto-ajustement contrôlé

Le système est déjà stable :
- décision centrale souveraine
- offsets ON / OFF existants
- auto-ajustement de courbe de chauffe déjà actif (pente / parallèle)
- suppression des injections ViCare parasites

---

## 🧱 PRINCIPES ARCHITECTURAUX NON NÉGOCIABLES

### Séparation stricte des rôles
- décision centrale ≠ diagnostic ≠ auto-ajustement
- aucun capteur diagnostic ne :
  - lit d’offset
  - lit de seuil
  - déclenche quoi que ce soit
  - modifie un état décisionnel

### Doctrine temporelle Arsenal (critique)

Tous les horodatages internes :
- sont stockés en `now().timestamp()` (float brut)

Tous les calculs de durée :
- utilisent uniquement `now().timestamp() - t0`

Interdiction absolue de :
- `as_timestamp()`
- parsing ISO
- datetime HA
- timezone

Objectif :
- reload-safe
- runtime-safe
- déterminisme total

---

## 🌡️ SOURCE THERMIQUE UNIQUE

Capteur de référence unique :
- `sensor.temperature_min_chambres`

Capteur décisionnel officiel :
- `input_select.chauffage_dernier_mode_decide`

Zone finale figée :
- **Chambres uniquement**
(Aucune extension prévue à d’autres zones)

---

## 📂 STRUCTURE DE TRAVAIL

Dossier racine capteurs diagnostic :

/homeassistant/11_template_sensors/chauffage/diagnostic_thermique/

Sous-familles actives :

- inertie_reprise/        (famille A)
- inertie_arret/          (famille B + C2)
- absence/                (famille C)
- cycles/                 (famille D)

Tous les fichiers :
- triggered template sensors
- en-têtes Arsenal obligatoires
- reload-safe strict

---

## ✅ CAPTEURS DÉJÀ VALIDÉS ET OPÉRATIONNELS

Famille A — reprise :
- A1 — détection reprise
- A2 — amplitude chute post-reprise
- A3 — durée chute post-reprise
- A4 — vitesse reprise

Famille B — arrêt :
- B1 — détection arrêt
- B2 — durée overshoot arrêt
- B4 — vitesse refroidissement présence

Famille C :
- C2 — vitesse perte thermique présence (refroidissement naturel)

Famille D :
- D1 — amplitude oscillation cycle présence

Tous ces capteurs :
- intra-cycle uniquement
- aucune accumulation inter-cycle
- figés naturellement
- compatibles recorder
- robustes reload

---

## 🧾 RECORDER

Ajout déjà décidé dans /homeassistant/recorder.yaml :

    # =====================================================
    # ==== 🔥 CHAUFFAGE - DIAGNOSTIC THERMIQUE ====
    # =====================================================
    - sensor.amplitude_chute_reprise_presence_chambres
    - sensor.duree_chute_reprise_presence_chambres
    - sensor.amplitude_overshoot_arret_presence_chambres
    - sensor.duree_overshoot_arret_presence_chambres
    - sensor.vitesse_reprise_presence_chambres
    - sensor.vitesse_refroidissement_presence_chambres
    - sensor.amplitude_oscillation_cycle_presence_chambres

Recorder = outil d’analyse fonctionnelle uniquement.

---

## 📑 DOCUMENTATION PROJET EXISTANTE

Dossier :

/homeassistant/documentation_arsenal/outils_externes/chat_gpt/cas_d_usage/projet_chauffage/

Documents normatifs déjà créés :

- architecture.md  
- phenomenes_thermiques.md  
- regimes_thermiques.md  
- strategie_auto_ajustement_offsets.md  
- observabilite_phase1.md  
- plan_implantation_capteurs_phase1.md  
- nomenclature_capteurs_phase1.md  

Ils définissent :
- architecture fonctionnelle
- régimes thermiques
- métriques cibles
- plan d’implantation

---

## 🎯 ÉTAT ACTUEL DU PROJET

Phase 1 en cours : **observabilité thermique pure**

Objectifs immédiats restants :
- compléter Famille C (absence) :
  - C1 — T_min_absence  
  - C3 — Δt_stabilisation_absence  

- compléter Famille D :
  - D2 — cycles_par_jour  
  - éventuellement D3 — durée_cycle_moyenne  

Puis :
- consolider recorder
- premières lectures réelles
- préparer design Phase 2 (auto-ajustement offsets)

---

## 🛑 RÈGLES DE TRAVAIL AVEC MOI

Tu dois impérativement :

- respecter l’architecture Arsenal
- ne jamais proposer de logique décisionnelle
- ne jamais introduire de dépendance fragile reload
- ne jamais utiliser condition: state fragile dans choose
- ne jamais proposer as_timestamp / datetime
- toujours produire des capteurs :
  - intra-cycle
  - déterministes
  - figés naturellement
  - explicables physiquement

Tu es ici :
- architecte thermique
- ingénieur instrumentation
- pas optimiseur prématuré
- pas prescripteur métier

---

## 🔧 PREMIÈRE DEMANDE APRÈS REPRISE

(à formuler explicitement dans la nouvelle session)

> Reprenons sur la **Famille D — Inertie en absence**.  
> Je veux concevoir proprement :
> - D2 — cycles_par_jour
> - D3 — durée_cycle_moyenne  
> en respectant strictement la doctrine Arsenal.

