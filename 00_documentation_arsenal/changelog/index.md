# 🧠 ARSENAL — CHANGELOG / INDEX (canon)
Fichier : 00_documentation_arsenal/changelog/index.md

# 🎯 Rôle
Index chronologique des versions/époques Arsenal.
- Donne une lecture "signal net" (3 bullets max) par version.
- Sépare clairement :
  - les **TRANSITIONS pré-V6** (snapshots `arsenal_v*` + digests),
  - les **VERSIONS ARSENAL HA v6+** (STABLE/CLOSE/CONSOLIDATION).

# 🧾 Légende
- **DIGEST** : transition (diff) entre snapshots, orientée gouvernance/architecture.
- **STABLE** : consolidation validée (système mature, restaurable).
- **CLOSE** : clôture de chantier (pas forcément une "version majeure").
- **CONSOLIDATION** : synthèse/alignement (sans intention nouvelle).

# 🧭 Tags (vocabulaire)
`chauffage` `ecs` `vicare` `clim` `ui` `docs` `energie` `reseau` `zigbee` `aeration` `volets` `modes` `mco` `integrite`


==================================================
🦴 PRÉHISTOIRE — INDEX (archives)
==================================================

## DIGEST — 2025_08_final → 20250920_final — CONSOLIDATION STRUCTURANTE (G1) — 2025-09-20
**Tags :** socle, configuration, includes, gouvernance_arborescence, ui_navigation, button_card_templates, utility_meter, zigbee2mqtt, secrets, recorder, history, logbook, migration

**Indicateurs (macro) :**
- Added (raw) **541** | Removed (raw) **88** | Changed **37** | Renamed/Moved **11**
- Added (net) **530** | Removed (net) **77**

### Signal net (ce qui change vraiment)
- **Pivot d’architecture “dossiers canoniques”**
  - `automatisations/` → `automations/`
  - `sensors/` → `template_sensors/`
  - `binary_sensors/` → `template_binary_sensors/`
  - `alarm_control_panel/` → `16_template_alarm_panels/`
  - retrait explicite du chargement `scene: !include scenes.yaml`
- **Normalisation/moves “packs → fichiers dédiés”**
  - gros “packs historiques” reclassés en fichiers cibles lisibles (alarme, modes, volets, scripts, aération…)
  - move **très signal** : `scenes.yaml` → `input_booleans/modes.yaml` (reclassement de nature : correction de gouvernance d’un “tiroir historique”)
- **UI Lovelace : refonte navigation + gabarits**
  - vue “Accueil” (réglages), pattern de navigation via badges
  - gabarits `button-card` structurants : `bouton_accueil`, `bouton_navigation_cercle`, `battery_status`, etc.
- **Mesure/énergie : extension `utility_meter`**
  - industrialisation des compteurs daily/weekly/monthly/yearly (plusieurs prises)
  - extension “mobilité” (autonomie Audi) → **métriques deviennent une couche** et pas un bricolage local
- **Zigbee2MQTT : nouveaux devices + backup coordinateur**
  - ajout net prises + capteurs météo Zigbee
  - backup coordinateur mis à jour (frame_counter/date)
- **Secrets : gouvernance des intégrations via `entry_id`**
  - `netatmo_entry_id`, `vicare_entry_id`, `mqtt_entry_id` externalisés

### Durcissements (micro-signal utile)
- MQTT : `value_template` rendu défensif (tolérance payload inattendu)
- Exclusions `recorder/history/logbook` autour de `browser_mod_*` (débruitage volontaire)

**Lecture gouvernance :**
Transition d’ère : abandon des agrégats legacy, adoption d’une arborescence atomisée “par rôle”.
Le risque principal est structurel (chargement/chemins), pas thermique ni métier.

---

## DIGEST — 20250920_final → 20251010_final — INDUSTRIALISATION / DURCISSEMENT (G4-like) — 2025-10-10
**Tags :** infrastructure, configuration, timers, scripts_unifies, observabilite, modes, alarme, chauffage, ecs, clim, meteo, aeration, zigbee, recorder, logbook, ui, arborescence, panne_secteur

**Indicateurs :**
- Fichiers : **+858 / -103**
- Dossiers impactés : `template_sensors/` (+359), `sensor_platforms/` (+100), `dashboards/` (+25)

**Signal net :**
- `timer:` devient un pilier (watchdogs / anti-rebond / remplacement de `delay`)
- Découplage orchestration → **scripts unifiés** (alarme, ECS, chauffage, panne secteur)
- Structuration par domaines (relocalisations massives)

---

✅ **Âge de pierre : bouclé.**
Chaîne préhistorique complète jusqu’aux bases `2025_08_final` (puis G1 20250920, puis industrialisation 20251010).

==================================================
🧱 ÈRE SNAPSHOTS — `arsenal_v1 … arsenal_v5` (pré-V6)
==================================================

## DIGEST — arsenal_v1 → arsenal_v2 — DURCISSEMENT CIBLÉ (G2) — (date : non fournie)
**Tags :** aeration, chauffage, ouvertures, ui, robustesse
**Signal net :**
- Aération ↔ Chauffage : blocage + récupération thermique → **machine d’état explicite** (plus d’implicite).
- Chauffage : apparition d’un **cerveau décision centrale** + capteurs diagnostic (`mode_calcule`, `raison_calculee`).
- Ouvertures “avec délai” : bascule sémantique (ON = **délai expiré + ouverture persistante**) → alignement chauffage.

**Points de vigilance (doc) :**
- Risque de confusion naming “avec délai / grâce” (ON ≠ délai en cours).
- Couverture complète de l’ancien paquet “fenêtres ↔ chauffage” vs décision centrale.

---

## DIGEST — arsenal_v2 → arsenal_v3 — DURCISSEMENT CIBLÉ (G2) — (date : non fournie)
**Tags :** aeration, chauffage, ouvertures, ui, gouvernance
**Signal net (tel que documenté) :**
- Aération : blocage chauffage + récupération thermique consolidés (états + timers + diagnostics).
- Chauffage : décision centrale + observabilité UI renforcée (mode/raison + antirebond visibles).
- Ouvertures “avec délai” : doctrine chauffage (ne pas réagir aux micro-ouvertures).

---

## DIGEST — arsenal_v2 → arsenal_v3 — CONSOLIDATION STRUCTURANTE (G4) — (date : non fournie)
**Tags :** architecture, notifications, aeration, vicare, reseau, zigbee, gouvernance
**Signal net :**
- Point d’entrée HA : refonte via `!include_dir_merge_*` → risque principal = **chargement incomplet** si include manquant.
- Notifications : standardisation via scripts façade (`script.notification_envoyer*`) → gouvernance transverse.
- Aération : anti-spam persisté (`input_datetime`) au lieu de `last_triggered` → reboot-safe.
- Chauffage/ViCare : durcissement auto-ajustement (garde-fous contexte).
- Réseau : pivot de vérité (entité réseau) → impact sémantique potentiel.

---

## DIGEST — arsenal_v3 → arsenal_v4 — TRANSITION (doc daté 2026-02-09)
**Tags :** ui, aeration, chauffage, ecs, volets, eclairage, integrations
**Signal net :**
- UI : abandon navigation par scripts → **navigation directe** + template sensors dédiés aux cartes.
- Aération : refonte/consolidation (micro-automations supprimées → logique plus centralisée) + vocabulaire V5 (épisode/blocage).
- Volets : passage “groupe cover open/close” → scripts unitaires + “open=100% garanti” (set_cover_position) + **renames cover (risque casse)**.
- Jardin : sortie “état présumé” (bouton SwitchBot + boolean) → commande directe switch/prise + garde-fous horaires.
- Suppression Browser Mod : rupture potentielle popups/overlays.

---

## DIGEST — arsenal_v4 → arsenal_v5 — TRANSITION (date : non fournie)
**Tags :** gouvernance, boot, systeme_stable, alarme, chauffage, clim, zigbee, ui
**Signal net :**
- Pivot “BOOT” → `input_boolean.systeme_stable` (déclenchements post-reboot gouvernés) sur plusieurs domaines.
- Extension Alarme (helpers + scripts + timer) : industrialisation type “décision centrale”.
- Chauffage : déclenchement plus événementiel, baisse du bruit (moins de garde-fous boot aveugles).
- Risque structurel : si `systeme_stable` est mal piloté → pertes d’initialisations critiques.

==================================================
🏠 ÈRE ARSENAL HA — Versions v6.x → v8.x
==================================================

## 🧠 ARSENAL HA — v6.0 — STABLE — (date : à renseigner)
**Tags :** architecture, ui, temps, chauffage, clim, ecs, energie, gouvernance
**Signal net :**
- Socle V6 : décisions centralisées + applicateurs idempotents + UI gouvernée.
- Modèle temporel ECS-like (temps = donnée, fin du polling).
- Doctrine Énergie (séparation proxy/utility_meter/capteurs bruts) initiée et structurée.

---

## 🧠 ARSENAL HA — v6.1 — STABLE — (date : non fournie)
**Tags :** chauffage, geofencing, poele, robustesse, clim
**Signal net :**
- Garde-fou thermique geofencing (absence non destructrice).
- Poêle non connecté : blocage temporisé + neutralisation auto-ajustement (événementiel).
- Alignements diagnostics et explicabilité (raison injectée, décision observable).

---

## 🧠 ARSENAL HA — v6.2 — CLOSE — (date : non fournie)
**Tags :** clim, chauffage, ui, diagnostics, recorder
**Signal net :**
- Clim : vérités métier explicites (seuils) via binary_sensors, triggers sémantiques.
- Chauffage : clarification finale “attente vs blocage”, capteur raison explicatif.
- UI/Recorder/Logbook alignés (faits → interprétation → paramètres).

---

## 🧠 ARSENAL HA — v6.3 — STABLE — (date : non fournie)
**Tags :** chauffage, autorisation, poele, energie, robustesse
**Signal net :**
- Chauffage : `sensor.chauffage_autorisation_cible` = autorité, automation = application idempotente.
- Poêle : durée blocage configurable (fin du hardcode).
- Énergie : bascule fondatrice vers **proxys monotones** (sécurisation dashboard Énergie).

---

## 🧠 ARSENAL HA — v6.4 — CONSOLIDATION — 2026-01-08
**Tags :** gouvernance, helpers, scripts, robustesse, eclairage, alarme, modes
**Signal net :**
- Normalisation totale des en-têtes helpers/scripts (doc honnête, auditabilité).
- Hygiène structurelle (orphelins, vestiges) + reboot-safe généralisé.
- Jardin : modèle à état métier continu (cycles matin/soir), événementiel.

---

## 🧠 ARSENAL HA — v6.5 — CONSOLIDATION — 2026-01-09
**Tags :** chauffage, clim, eclairage, vacances, alarme, vmc, robustesse
**Signal net :**
- Chauffage V3 PRO : alignement décision ↔ diagnostic ↔ UI (présence non autorité thermique).
- Clim “silencieux” : exécution événementielle + idempotence (mode queued).
- Jardin : consolidation matin/soir + mémoire anti-spam robuste.
- Vacances : décision métier (binaire + raison) + UI lecture seule.

---

## 🧠 ARSENAL HA — v7.0 — STABLE — (date : à renseigner)
**Tags :** ui, docs, energie, temps, gouvernance, chauffage, clim, ecs
**Signal net :**
- Transition d’ère : doctrine documentée (`00_documentation_arsenal/`) + UI industrialisée (templates segmentés).
- Énergie : verrouillage définitif des sources (proxy monotone only pour Energy dashboard).
- Temps : timers/états gouvernés (modèle ECS-like généralisé).

---

## 🧠 ARSENAL HA — v7.1 — STABLE — (date : non fournie)
**Tags :** ui, chauffage, vmc, sémantique
**Signal net :**
- VMC : séparation stricte aération naturelle vs VMC (UI lecture fidèle).
- Chauffage : clarification officielle des “attentes” (confort vs protection absence).
- Élimination des dettes sémantiques UI (sans changement fonctionnel).

---

## 🧠 ARSENAL HA — v7.2 — STABLE — 2026-01-13
**Tags :** chauffage, ui, aeration, docs, observabilite
**Signal net :**
- Chauffage : intention **Neutre** (abstention gouvernée), fin des décisions implicites de présence.
- UI : finalisation taxonomie templates génériques.
- Aération : migration capteur ΔT + refonte dashboard diagnostic.

---

## 🧠 ARSENAL HA — v7.2.1 — STABLE — (date : non fournie)
**Tags :** ui, chauffage, diagnostics, observabilite
**Signal net :**
- UI supervision automatisations : diagnostic binaire mature (Normal/Incident).
- Chauffage : restructuration Diagnostics Chauffage autour de l’état global.
- Observabilité : débruitage logbook + retrait diagnostic journalier “lourd”.

---

## 🧠 ARSENAL HA — v7.3 — STABLE — (date : non fournie)
**Tags :** ecs, chauffage, diagnostics, docs, gouvernance
**Signal net :**
- ECS : fin de cycle canonique + ACK explicite (signal consommable).
- Chauffage : verrou décisionnel présence (autorisation_cible réintégrée).
- Diagnostics/UI : recentrage état global + réduction surface “diagnostic jour”.

---

## 🧠 ARSENAL HA — v7.3.1 — STABLE — (date : non fournie)
**Tags :** chauffage, geofencing, robustesse
**Signal net :**
- Inhibition geofencing : offsets ON/OFF + booléen stabilisé (hystérésis externalisée).
- Décision centrale : consommation d’un état qualifié, plus de seuil brut.
- Triggers décision : réduction bruit (faits stables seulement).

---

## 🧠 ARSENAL HA — v7.3.2 — STABLE — (date : non fournie)
**Tags :** integrite, chauffage, ui
**Signal net :**
- Intégrité paramètres : capteurs par domaine + agrégat global (signal, pas correction).
- Chauffage : clarification Eco/protection absence, capteurs canoniques plus explicites.
- UI : suppression faux positifs d’incohérence (lecture fidèle).

---

## 🧠 ARSENAL HA — v7.3.3 — STABLE — (date : non fournie)
**Tags :** panne_secteur, chauffage, ecs, ui
**Signal net :**
- Panne secteur : chauffage 100% via décision centrale, exception ECS bornée assumée.
- Décision centrale : bypass temporisation pour override prioritaire.
- UI : correction attente vs repos nominal, standby vs blocage (alignement strict).

---

## 🧠 ARSENAL HA — v7.3.4 — STABLE — 2026-01-16
**Tags :** ui, chauffage, clim
**Signal net :**
- UI températures chambres : socle neutre, logique chauffage/clim portée par cartes dédiées.
- Chauffage : normalisation consignes Présence/Absence → Confort/Réduit (migration contrôlée).
- Clim : garde-fou absence prolongée (interdiction application).

---

## 🧠 ARSENAL HA — v7.3.5 — STABLE — 2026-01-16
**Tags :** diagnostics, chauffage, ui
**Signal net :**
- Diagnostics Chauffage : réorganisation autour diagnostic global (moins de redondance).
- Vannes thermostatiques : dashboard diagnostic dédié, lecture seule.
- Nettoyage : retrait capteurs/bruit logbook (sans changement décision).

---

## 🧠 ARSENAL HA — v8.0.0 — STABLE — 2026-01-19
**Tags :** notifications, mco, batteries, mobilite, chauffage, ui, docs
**Signal net :**
- Notifications : persistantes = projection d’état uniquement (fin des succès persistants).
- MCO batteries : périmètre group + script unique + verrou journalier + contrat.
- Mobilité : utility_meter mensuel/annuel + source unique kilométrage.
- Chauffage UI/diagnostics : triggers réactifs + meilleure distinction inhibition/standby.

---

## 🧠 ARSENAL HA — v8.1.0 — STABLE — 2026-01-20
**Tags :** chauffage, vicare, souverainete, ecs, bouclage, ui, docs
**Signal net :**
- Chauffage : anti-yo-yo (sémaphore applicatif) + mémoire souveraine après confirmation cloud.
- Chauffage : réalignement ViCare ↔ HA dédié + miroir d’état appliqué.
- Chauffage : watchdog /10 min désactivé → régime plus événementiel.
- Auto-ajustement courbe : contractualisation complète + capteurs propositionnels (pas de boucle fermée).
- ECS : bouclage auto gouverné (plage horaire + présence) + section UI réglages.

---

## 🧠 ARSENAL HA — v8.1.1 — STABLE — 2026-01-23  
**Tags :** chauffage, ecs, gouvernance, observabilite, docs, vicare, architecture

**Signal net :**
- **Chauffage : décision centrale 100% événementielle** (suppression du polling `/10`, couverture exhaustive des causes contractuelles, idempotence conservée).
- **Observabilité thermique structurée (A/B/C/D)** : création d’un domaine diagnostic passif (inertie, cycles, stabilisation), reload-safe et strictement non décisionnel.
- **Architecture : migration “vicare → domaines” + gouvernance explicite des IDs** (préfixes 1024/1025/1026, 104 mouvements, resynchronisation documentaire complète).

---

## 🧠 ARSENAL HA — v8.2 — STABLE — 2026-01-24  
**Tags :** chauffage, ecs, ui, observabilite, reseau, clim, docs

**Signal net :**
- **Chauffage : fiabilisation B0 + observabilité long terme** (capteur fondation strictement numérique, statistiques natives HA activées, Famille C absence refondue sous contrat normatif).
- **Gouvernance idempotente hiver (chauffage/clim)** : calcul état cible explicite, écriture uniquement en cas de divergence réelle, suppression transitions fantômes.
- **UI : factorisation structurelle des navigations Lovelace** (`lovelace/includes/navigation/`), socle includes canonisé.

---

## 🧠 ARSENAL HA — v8.2.1 — STABLE — 2026-01-27  
**Tags :** chauffage, vicare, zigbee, aeration, ui, reseau, observabilite, docs

**Signal net :**
- **Chauffage : cohérence matériel ↔ décision** via `binary_sensor.chauffage_incoherence_vicare_decision` (ViCare canal surveillé non fiable, ré-alignement déclenché uniquement sur incohérence qualifiée).
- **Observabilité thermique structurée étendue + recorder gouverné** (A1/B0/cycles/absence, séparation stricte décision ↔ diagnostic).
- **Zigbee : migration canal 11 → 25 + reconstruction maillage** (LQI homogènes, résilience radio consolidée).

---

## 🧠 ARSENAL HA — v8.2.2 — STABLE — 2026-01-27  
**Tags :** chauffage, zigbee, reseau, modes, observabilite, integrite

**Signal net :**
- **Présence : réactivité maîtrisée sans autorité d’écriture** (temporisations fortement réduites, invariants confirmés : aucune action directe chauffage/clim).
- **Zigbee : LQI enfin vérifiable via source unique** (`group.zigbee_linkquality_all` + capteur triggered canon), migration arborescence système.
- **Chauffage : géofencing qualifié par capteur métier** (`binary_sensor.chauffage_inhibition_geofencing_requise`) — hystérésis déplacée hors automation, séparation stricte qualification ↔ mémoire.

---

## 🧠 ARSENAL HA — v8.3.0 — STABLE — 2026-01-27  
**Tags :** chauffage, vicare, ui, zigbee, docs, securite, observabilite

**Signal net :**
- **Chauffage : souveraineté consignes (HA maître / ViCare esclave passif)** — fin de toute sync inverse, scripts d’application matériels uniques, réalignement déclenché uniquement sur incohérence qualifiée.
- **Alarme/Wi-Fi : apprentissage BSSID piloté par signal métier** (capteur → automation → helper), logique déductive supprimée.
- **Documentation : socle architecture formalisé** (cartographie entités, couches, supervision) + structuration sous-domaines templates.

---

## 🧠 ARSENAL HA — v8.3.1 — STABLE — 2026-01-28  
**Tags :** clim, chauffage, ui, observabilite, docs, integrite

**Signal net :**
- **Climatisation : pipeline canonique complet** (`sensor.clim_target_mode` → `script.clim_execution` → watchdog + capteur d’incohérence), suppression du script monolithique historique.
- **Chauffage : observabilité cycles fiabilisée** (anti-replay reload/restart, incrément strictement événementiel).
- **UI : dashboard Températures Min/Max + hygiène ressources Lovelace** (suppression composants inutilisés, includes normalisées).

---

## 🧠 ARSENAL HA — v8.3.2 — STABLE — 2026-02-04  
**Tags :** chauffage, ecs, clim, ui, docs, gouvernance, integrite

**Signal net :**
- **Templates : factorisation interne par ancres YAML** (moteurs uniques + déduction via `this.entity_id`), réduction massive de duplication sans changement fonctionnel.
- **Modes maison recentrés sur le contexte ECS** (Vacances / Normal / Désinfection) : suppression d’actions annexes, périmètre clarifié, modèle capteur → action.
- **Réalignements sémantiques d’arborescence** (déshumidification rattachée aux seuils clim via humidex).

---

## 🧠 ARSENAL HA — v9.0.0 — STABLE — 2026-02-05 / 2026-02-06  
**Tags :** architecture, ui, chauffage, docs, integrite

**Signal net :**
- **Extinction complète des legacy templates** (`platform: template`) → moteur moderne `template:` exclusivement.
- **Assainissement d’arborescence capteurs** (extinction `12_template_binary_sensors`, 40+ moves vers `13_sensor_platforms`, includes nettoyés).
- **Chauffage : notifications persistantes découplées des scripts** (automation UI dédiée, idempotente, projection fiable).

---

## 🧠 ARSENAL HA — v9.0.1 — CONSOLIDATION — 2026-02-08  
**Tags :** chauffage, ecs, ui, docs, gouvernance

**Signal net :**
- **Chauffage : override opérateur institutionnalisé (N0)** — `mode_confort_chauffage` devient commande souveraine prioritaire sur le régime automatique.
- **UI Chauffage : “observable only”** — notification persistante limitée au **Confort**, source exclusive `sensor.programme_chauffage`.
- **ECS : institutionnalisation documentaire** — éclatement du contrat monolithique en corpus normatif spécialisé, ancien document déclassé en référence.

---

## 🧠 ARSENAL HA — v9.0.2 — CONSOLIDATION — 2026-02-10  
**Tags :** docs, gouvernance, integrite

**Signal net :**
- **Refactor complet du système de changelog** : passage d’un fichier monolithique à un modèle versionné (`changelogs/vXX_X_X.md` + historique transversal).
- Suppression du legacy `changelog.md` au profit d’une gouvernance diffable et industrialisable.
- Nettoyage mineur ViCare : retrait d’un capteur local `modulation_local` (vérifications requises si dépendances).

---

## 🧠 ARSENAL HA — v9.0.3 — CONSOLIDATION — 2026-02-10  
**Tags :** alarme, presence, gouvernance, architecture, docs

**Signal net :**
- **Alarme institutionnalisée** : création d’un corpus normatif complet (`contrats/alarme/`), sous-système désormais opposable et extensible.
- **“Visite” migrée d’Alarme vers Présence** (helpers, timers, automations + changement d’ID) : recentrage sémantique et séparation des domaines.
- **Domainisation des helpers système** (`input_selects/`, `input_booleans/`) : arborescence clarifiée, sous-dossiers par domaine.

---

## 🧠 ARSENAL HA — v9.0.4 — CONSOLIDATION — 2026-02-11  
**Tags :** meteo, pluie, presence, visite, templates, hygiene_repo

**Signal net :**
- **Météo / Pluie enrichie** : introduction d’un cumul hebdomadaire (utility_meter) + totalisation locale + intégration recorder + UI long terme (52 semaines).
- **Visite consolidée côté Présence** : migration d’`input_select` + création d’un contrat opposable dédié.
- **Standardisation des en-têtes templates** : montée en qualité documentaire (opposabilité, lisibilité, invariants explicités).
- **Éclairage jardin** : clarification sémantique “plage_active” + ajout d’un capteur d’heure d’allumage.

**Anomalie snapshot :**
- Import massif non fonctionnel du dossier `git/` (+4034 fichiers) → bruit structurel majeur à exclure des diffs futurs.

---

## 🧠 ARSENAL HA — v9.1.0 — STABLE — 2026-02-14  
**Tags :** ui, docs, modes, integrite, reseau

**Signal net :**
- **UI : architecture à 3 niveaux** (socle → TPL génériques → métier) + application réelle sur plusieurs dashboards (CO₂, Clim diag, VMC, Éclairage).
- **Lovelace : factorisation par includes structurels** (headers / sous-headers) + nettoyage d’agrégats historiques côté button-card.
- **Compat webhooks : accès externe migré** `8443 → 9443` (`external_url`), pour Netatmo/Withings et validations.

---

## 🧠 ARSENAL HA — v9.1.1 — STABILISATION — 2026-02-14  
**Tags :** upgrade, home_assistant, webhooks, stabilisation

**Signal net :**
- Mise à jour **Home Assistant Core → 2026.2.2**.
- Stabilisation post-upgrade (validation webhooks Netatmo / Withings via port 9443).
- Aucune évolution fonctionnelle Arsenal revendiquée.

**Contexte :**
- Séquence réelle : migration port (8443 → 9443) → v9.1 → upgrade HA → v9.1.1.
- v9.1.1 acte la compatibilité complète après montée de version HA.

---

## 🧠 ARSENAL HA — v9.1.2 — CONSOLIDATION — 2026-02-15  
**Tags :** ui, charte_couleurs, navigation, volets, diagnostics, logger

**Signal net :**
- **Charte couleurs enrichie** : distinction explicite couleur métier vs couleur structure UI + introduction sémantique NAV/HUB (`rgba(90, 110, 130, 0.08)`).
- **Nouveau socle ACTION (TPL-06)** : `socle_action_simple_sans_couleur` → base structurelle neutre (sans fond, sans action imposée).
- **Navigation rebasée proprement** sur le nouveau socle (fond défini localement, pas au niveau socle).
- **Volets refactorisés** : variantes déterministes (`open/close/stop`) basées sur `socle_kpi_72`, suppression logique “tone”.
- **Diagnostics Chauffage/Aération clarifiés** : lecture explicite du verrou post-aération + renommage “Blocage chauffage” → “Effet sur chauffage”.
- **Logger durci** : réduction bruit via niveaux `warning/error` sur intégrations bavardes.

---

## 🧠 ARSENAL HA — v9.1.4 — CONSOLIDATION — 2026-02-15  
**Tags :** ui, nas, templates, lecture_seule, monitoring

**Signal net :**
- **Nouveau template générique** : `capteur_seuil_sans_action` (lecture seule, sans interaction).
- **Dashboard NAS sécurisé en lecture seule** : remplacement des tuiles à seuils interactives par `carte_capteur_seuils_sans_action`.
- Périmètre : CPU, RAM, charge, volumes, températures disques, etc. → monitoring pur, aucune action possible.

**Intention :**
- Séparer clairement **supervision** et **action**.
- Éviter toute interaction accidentelle sur un dashboard technique.

---

## 🧠 ARSENAL HA — v9.1.5 — CONSOLIDATION — 2026-02-15  
**Tags :** ui, nettoyage, climatisation, navigation, meteo

**Signal net :**
- **Suppression du dashboard “Diagnostics Sommeil”** + retrait de toutes les références associées (dashboards.yaml, bouton Météo/Bruit).
- **Climatisation — UI corrigée et structurée** :
  - titres nettoyés (“Climatisation” sans espaces parasites),
  - section “Décision” restructurée (header dédié + grille 2 colonnes).
- **Navigation normalisée** :
  - `/clim-dashboard/climatisation_` → `/clim-dashboard/climatisation`
  - correction appliquée dans `navigation.yaml` et templates concernés.

**Intention :**
- Élimination d’un dashboard obsolète.
- Alignement sémantique et visuel côté Clim.
- Suppression d’un path incohérent (underscore résiduel).

---

## 🧠 ARSENAL HA — v9.2.0 — STABLE — 2026-02-17  
**Tags :** ui, ergonomie, pipeline_couleur, diagnostics, reglages

**Signal net :**
- **Refonte massive des dashboards Réglages** : passage `entities` → `grid` + `tile` avec `numeric-input` inline (ergonomie homogène multi-domaines : éclairage, aération, ecs, chauffage, clim, alarme, vmc, volets, ouvertures, déshumidificateur).
- **Pipeline couleur généralisé** : externalisation des couleurs vers des capteurs dédiés (`sensor.couleur_*`) + migration KPI Santé / CO₂ / Bruit vers `socle_kpi` + `ui_profile: arsenal`.
- **Diagnostics renforcés** :
  - Alarme : cartes dédiées cohérence / raison / divergence persistante (fin du markdown bricolé).
  - Chauffage : bloc performance rationalisé (bar-card 24h/7j sans couleurs codées en dur).
- **Nettoyage UI Chauffage** : suppression définitive de `input_select.chauffage_mode` (retrait helper + retrait dashboard).

---

## 🧠 ARSENAL HA — v9.2.1 — STABLE — 2026-02-17  
**Tags :** ui, navigation, factorisation, ecs, bouclage, changelog

**Signal net :**
- **Navigation simplifiée** : retrait des raccourcis système (Automations, Scripts, Logs, États, Entités, etc.) + suppression de l’action “Reboot HA”.
- **Factorisation Bouclage ECS** : remplacement des cartes inline par un include canon (`includes/cartes/bouclage.yaml`) partagé entre dashboards.
- **Template générique ajouté** : `bouclage_timer.yaml` ; suppression de l’ancien template spécifique Arsenal (remplacé proprement).
- **Changelog versionné v9.2 ajouté** + alignement de `en_cours.md`.

**Intention :**
- Alléger l’UI utilisateur (moins d’accès “système brut”).
- Réduire la duplication (include unique pour Bouclage).
- Stabiliser la gouvernance documentaire.

---

## 🧠 ARSENAL HA — v9.2.2 — STABLE — 2026-02-17  
**Tags :** ui, ouvertures, diagnostics, templates, navigation, secrets

**Signal net :**
- **Diagnostics Ouvertures refactorisés** : remplacement des blocs `markdown` par des cartes statut structurées (fenêtres, délais, timers) → UI homogène Arsenal.
- **Enrichissement capteurs Ouvertures** : ajout d’icônes explicites (`mdi:window-open`, `mdi:lock`) pour meilleure lisibilité métier.
- **Nouveau template générique** : `status_72_on_off` + ajustements sur `bouclage_timer` et `compteur_seuils_variables` (alignement socle compact).
- **Navigation ajustée** : Historique repositionné, retrait File Editor (ingress), ajout bouton Logs HA.
- **Maintenance intégration ViCare** : mise à jour `vicare_entry_id` dans `secrets.yaml`.

**Intention :**
- Supprimer le rendu texte fragile au profit de cartes statut canoniques.
- Renforcer la cohérence visuelle des Ouvertures.
- Maintenir l’alignement intégration ViCare après changement d’entry id.

---

## 🧠 ARSENAL HA — v9.2.3 — STABLE — 2026-02-17  
**Tags :** sante, sommeil, withings, templates, factorisation, changelog

**Signal net :**
- **Dashboard Santé (Sommeil) enrichi et densifié** : grille 2→3 colonnes, ajout KPI “Réveils” + bloc Ronflements (épisodes & durée), UI plus sobre (bar-card sans labels visibles).
- **Capteurs Withings _local industrialisés** : dérivation automatique de la source depuis `this.entity_id` + fallback robuste sur `this.state` + factorisation via ancres YAML (fin de la duplication Jinja).
- **Nouveau template Santé** : `duree_ronflements.yaml` ; suppression d’un template générique transitoire devenu inutile.
- **Gouvernance changelog alignée** : ajout `v09_2_2.md` + mise à jour de `en_cours.md`.

**Intention :**
- Fiabiliser les capteurs locaux face aux `unknown/unavailable`.
- Réduire la duplication template (maintenance simplifiée).
- Enrichir la lecture sommeil sans ajouter de logique métier.

---

## 🧠 ARSENAL HA — v9.2.4 — STABLE — 2026-02-17  
**Tags :** ui, ecs, planning, navigation, volets, templates, documentation

**Signal net :**
- **Planning ECS refondu** : structure `grid` + `vertical-stack`, sous-sections Matin/Soir standardisées (`sub_section_header`) + `tile` homogènes (ergonomie claire, compacte).
- **Navigation “outillage” réintroduite** : accès directs (Sauvegardes, Automations, Scripts, Logs, États, Entités, Dashboards, Intégrations, Templates, File Editor) + bloc actions (Reboot HA, Ressources).
- **Volets normalisés** : suppression variantes colorées au profit de `shutter_action_base` neutre + icônes cohérentes (`mdi:window-shutter*`) + section Chambres regroupée.
- **Template volets simplifié** : fond neutre canon (`rgba(158, 158, 158, 0.2)`), fin des couleurs vert/rouge embarquées.
- **Helper Chauffage** : icône `inhibition_geofencing_etat` alignée (`mdi:shield-check`).
- **Documentation gouvernée** : ajout `v09_2_3.md` + note prospective `zigbee_reseau.md`.

**Intention :**
- Harmoniser l’ergonomie Réglages (planning ECS).
- Assumer un menu Navigation “expert” complet.
- Supprimer les couleurs décisionnelles des actions volets (neutralité UI).

---

## 🧠 ARSENAL HA — v9.2.5 — STABLE — 2026-02-18  
**Tags :** ui, diagnostics, reglages, templates, climatisation, robustesse

**Signal net :**
- **Industrialisation des Diagnostics** : retrait massif des pavés `markdown` Jinja au profit de cartes statut 72px (Chauffage / Clim / ECS / Aération) + titres uniformisés “Diagnostics X”.
- **Socle templates Diagnostics enrichi** : base dédiée Chauffage + templates spécifiques Climatisation / ECS (cartes compactes réutilisables).
- **Réglages homogénéisés** : titres alignés “Réglages X” + bascule ponctuelle `entities` → `tile` (contrôles natifs, plus lisibles).
- **Climatisation durcie** : script `execution_mode_cible` sécurisé (lecture explicite `states('climate.clim')` + garde-fous `unknown/unavailable`).
- **Changelog complété** : ajout versionné v9.2.4.

**Intention :**
- Remplacer le diagnostic narratif par un diagnostic structuré, lisible, canon Arsenal.
- Unifier la grammaire visuelle (Diagnostics / Réglages).
- Éviter toute décision basée sur un état HVAC non fiable.

---

## 🧠 ARSENAL HA — v9.2.6 — STABLE — 2026-02-19  
**Tags :** ui, diagnostics, chauffage, ouvertures, pluie, vicare, robustesse

**Signal net :**
- **Diagnostics Éclairage industrialisés** : disparition des blocs markdown “Simulation” au profit de grilles 3 colonnes homogènes (status_72_on_off + socle_info_72).
- **Chauffage — Diagnostics durcis** : refactor profond des templates (objet `variables.diag` / `variables.diagnostic`) → catégorisation explicite (ok/warn/ko/info/indisponible), couleurs pilotées par type, labels normalisés.
- **Ouvertures — Icônes dynamiques** : intégration des états temporisés (grâce) via `mdi:timer-sand` + variants ouverts/fermés cohérents (lecture pure, sans impact décisionnel).
- **Pluie & ViCare — Fallback unifié** : factorisation Jinja via ancres (`this.entity_id` → source) + suppression `default_entity_id` → robustesse homogène des capteurs locaux.
- **ViCare Gaz refactorisé** : rationalisation des templates (périodique / total) en remplacement des anciens fichiers segmentés.

**Intention :**
- Rendre les diagnostics 100 % structurés (plus aucun rendu narratif lourd).
- Centraliser la logique d’étiquetage / couleur côté templates (UI déterministe).
- Uniformiser tous les fallbacks “_local” (pluie, électricité, gaz) pour éviter les états incohérents après indisponibilité API.
- Améliorer la lisibilité opérationnelle des ouvertures temporisées sans toucher aux invariants métier.

---

## 🧠 ARSENAL HA — v9.2.7 — STABLE — 2026-02-18  
**Tags :** ui, factorisation, meteo, thermique, sante, robustesse, imprimerie

**Signal net :**
- **Factorisation Lovelace massive** : disparition des blocs markdown/auto-entities monolithiques au profit d’`includes/cartes/*` et `section_headers/*` gouvernables (Météo Min/Max, Diagnostics thermique, Clim, ECS, Zigbee, Batteries, Imprimerie, Déshumidificateur).
- **Diagnostics Thermique Chauffage industrialisés** : décomposition en cartes dédiées (interprétation, inertie, oscillateur, contexte…) → maintenance fine, lisibilité accrue.
- **`sensor.temperature_moyenne_maison` contractuel** :
  - renommage + normalisation,
  - seuils calculés exposés en attributs (`seuil_chauff_on`, `seuil_clim_on`),
  - couleur Arsenal en attribut (`arsenal_bg`),
  - alignement customize + recorder.
- **Pluie & Santé durcies** :
  - fallback numérique explicite sur capteurs pluie locaux,
  - parsing robuste sommeil Withings (regex + gestion chaînes vides).
- **Template chauffage (`*_courbe_diag_72`) renforcé** :
  - normalisation `kind`,
  - fallback explicite,
  - couleurs strictement conformes à la charte Arsenal.

**Intention :**
- Éliminer les “monolithes UI” au profit de briques réutilisables, diffables et gouvernables.
- Transformer la température moyenne maison en **KPI thermique central contractuel**.
- Durcir les pipelines capteurs (météo / santé) face aux sources intermittentes.

---

## 🧠 ARSENAL HA — v9.4 — RECONSTRUCTION POST-ROLLBACK — 2026-02-23  
**Type :** G4 — Consolidation stratégique  
**Tags :** resilience, aeration_v3, volets_pluie, architecture, canonisation, timers, refactor_majeur

**Signal net :**
- **Résilience canonisée** : script unique `resilience_integration_recover` + backoff réel via timers dédiés → suppression totale des `time_pattern` et logiques anti-spam implicites.
- **Intégrations structurées** : reload événementiel homogène (Netatmo, ViCare, Overkiz, SwitchBot, Airstage, Zigbee2MQTT, Synology, HomeKit) avec condition `systeme_stable`.
- **Capteurs système consolidés** : centralisation `age_donnees_integrations` + `etat_integrations`, fin des fragments `age_des_donnees/*`.
- **Aération V3 PRO atomique** : pipeline découpé (M1→M5), timers explicites, guard anti-zombie renforcé, séparation stricte détection / décision / action / analyse.
- **Volets pluie industrialisés** : capteurs décisionnels dédiés + automatisation métier + templates UI 72 intégrés au socle.
- **Nettoyage structurel massif** : suppression anciens reload, ancien `aeration.yaml`, logs zigbee, duplications diverses.
- **Secrets rationalisés** : alignement `*_entry_id`, suppression doublons obsolètes.

---

## 🧠 ARSENAL HA — v9.5 — STABLE — 2026-02-XX  
**Tags :** aeration, anticipation_meteo, chauffage, integrite, ui, architecture  
**Signal net :**
- Aération : M2 blindé + ΔT 100 % paramétrable (seuils & durées), fin des incohérences fantômes.
- Chauffage : module Anticipation météo intégré au cœur décisionnel (confort différé si favorable).
- Intégrité : invariants automatiques sur seuils/prolongations (impossible de configurer incohérent).
- UI : diagnostic chauffage refactoré (anticipation intégrée), suppression includes legacy.
- Documentation : hiérarchie v9 rationalisée, fin du modèle en_cours.

---

## 🧠 ARSENAL HA — v9.6 — STABLE — 2026-02-27  
**Tags :** ouvertures, aeration, chauffage, alarme, observabilite, normalisation  
**Signal net :**
- Ouvertures : migration totale vers `contact_*` (N1/N2 canonique), capteurs “avec délai” fiabilisés (anti faux positifs reboot, cohérence timer).
- Aération : pipeline M1–M6 consolidé (fermeture stable canonique, M5 sécurisé, déclenchement M1 unifié).
- Chauffage : triggers rationalisés — alignement exclusif sur `fenetre_ouverte_maison_avec_delai` (fin recalculs parasites).
- Alarme : alignement structurel sur couche `contact_*`, sans dérive métier.
- Système : observabilité étendue (internet / stats) — couche purement diagnostic.

---

## 🧠 ARSENAL HA — v10 — STABLE — 2026-03-XX — Ouvertures / Aération / Anti-zombie
**Tags :** ouvertures, aeration, chauffage, temporalite, robustesse, anti_zombie, architecture  
**Signal net :**
- Fin de grâce explicitée (writer unique) : booléens `*_grace_echue` → causalité exclusivement portée par `timer.finished`.
- Qualification d'ouverture refondée : marqueurs métier explicites + `binary_sensor.ouverture_qualifiee_maison` → fin des confirmations tardives.
- Temporalité thermique canonisée : généralisation `as_timestamp`, calculs bornés, hiérarchie stricte `analyse < blocage`, M6 refondu.
- Neutralisation des traces datetime : remise à zéro explicite des `input_datetime` → fin des états orphelins post-reboot.
- Anti-zombie renforcé (M0) : détection blocages orphelins, cohérence enveloppe / timers / traces.
- Pipeline blocage enrichi : déclenchement sur `ouverture_qualifiee_maison` → gestion déterministe des réouvertures (M5).
- Observabilité étendue : bandeau de stabilité + outillage diagnostic.

---

## 🧠 ARSENAL HA — v10.3 — STABLE — 2026-03-XX
**Tags :** infrastructure, ecs, vacances, eclairage, vicare, simplification, robustesse  
**Signal net :**
- Infrastructure : suppression complète de Pyscript → migration intégrale vers scripts natifs HA, élimination d'un custom component.
- ECS : timestamp de début de cycle → fiabilisation des offsets, refactor logs + capacité sauvegardes JSON étendue.
- Mode vacances : nouveau pipeline préconfort dédié (helpers + capteurs + automation) → gouvernance explicite des fenêtres, suppression ancien mécanisme.
- Vicare : capteur + alerte gateway → détection explicite des pertes de connectivité.
- Éclairage garage : capteur d'autorisation métier + alignement UI (template + couleurs canoniques).
- Documentation : archivage versionné des changelogs v10.x, suppression journaux internes non versionnés.

---

## 🧠 ARSENAL HA — v10.7 — STABLE — 2026-03-XX
**Tags :** ouvertures, zigbee, mouvements, aeration, chauffage, ui, documentation, robustesse  
**Signal net :**
- Ouvertures : généralisation redondance Zigbee (`_1/_2`) + fusion événementielle, harmonisation schéma `contact_<zone>_<type>` sur toutes les couches, extension porte d'entrée full stack.
- Mouvements : couche N2 agrégée par zone (`binary_sensor.mouvement_<zone>`) → découplage total des automatisations des capteurs physiques.
- Éclairage / Alarme : migration vers capteurs agrégés → robustesse accrue face aux défaillances Zigbee.
- Aération : mémoire monotone ΔT de cycle (M3) + neutralisation systématique des artefacts fin de cycle (M4).
- Chauffage : refonte normative des contrats capteurs (N1 / structurants / stabilisation), recadrage `chauffage_autorisation_cible`.
- UI : observabilité chauffage enrichie (poêle, météo) + harmonisation palettes barres (opacité 0.2).
- Système : métriques séjour (ΔT, CO₂) + capteur uptime + rétention recorder 30 jours.
- Documentation : restructuration massive (contrats extraits, nettoyage obsolètes, archivage v10.4–v10.7).

---

## 🧠 ARSENAL HA — v10.8 — STABLE — 2026-03-11
**Tags :** ouvertures, redondance, zigbee, architecture, automatisations, templates, robustesse  
**Signal net :**
- Ouvertures : passage last-valid-state (v2.0) → moteur de corroboration temporelle (v2.2) avec quarantaine et inhibition système.
- Ouvertures : séparation stricte `observed_event` / `business_state` / `reconciliation_status` → fin des états ambigus.
- Ouvertures : politique asymétrique fail-safe — `off` immédiat, `on` soumis à corroboration → suppression des faux positifs Zigbee.
- Ouvertures : fenêtres de corroboration + statuts `divergent`, `quarantine`, `inhibited`.
- Templates : refonte auto-paramétré (`this.entity_id`) + ancres YAML → suppression logique inline par capteur, externalisation totale de la décision.
- Automations : moteur centralisé de réconciliation → pilotage timers, contextes (`input_text`) et timestamps.
- Helpers : contextes de réconciliation, timestamps de transition et timers dédiés par capteur.
- Diagnostic : alignement `reconciliation_status` v2.2 + états étendus (`quarantine`, `inhibited`).
- UI : navigation dynamique pilotée par l'état système → suppression des couleurs statiques.
- Infrastructure : nettoyage anciens diagnostics globaux + simplification architecture templates.

---

## 🧠 ARSENAL HA — v10.9 — STABLE — 2026-03-12
**Tags :** ouvertures, scripts, meteo, ui, refactor, structure, nettoyage  
**Signal net :**
- Ouvertures : moteur de réconciliation → orchestrateur pur, logique métier extraite vers 5 scripts spécialisés, automation réduite au routage.
- Scripts : module dédié `reconciliation_redondance` (traitement source, expiration, inhibition, levée, application).
- Météo : KPI température min/max journaliers fusionnés → exploitation directe en UI.
- Couleurs météo : reclassement structurel sans modification fonctionnelle.
- Diagnostic : simplification résumé redondance → retrait statut métier ligne `A/B`, séparation UI / diagnostic.
- Zigbee : simplification template reload → réutilisation variable locale, suppression redondance.
- Documentation : purge changelogs v6/v7 + refonte historique en phases d'inflexion.
- Timers : nettoyage cosmétique global sans impact fonctionnel.

---

## 🧠 ARSENAL HA — v10.9.1 — STABLE — 2026-03-12
**Tags :** ouvertures, ui, nettoyage, semantique, normalisation  
**Signal net :**
- Ouvertures : clarification sémantique `aeration_confirmee` → renommage automation (rôle garantie de cohérence, non clôture d'épisode).
- Réconciliation : normalisation typographique aliases (`Réconciliation`, `Résilience`) sur automations et scripts.
- UI : libellés contacts séjour → identifiants minimalistes (`1–4`), suppression cartes météo min/max héritées.
- Système : nettoyage global sans impact fonctionnel (moteurs décisionnels et pipeline aération inchangés).

---

## 🧠 ARSENAL HA — v10 (consolidation finale) — STABLE — 2026-03-XX — Système contractuel / Viessmann
**Tags :** architecture, contrats, meteo, chauffage, eclairage, viessmann, ui, robustesse  
**Signal net :**
- Architecture : transformation en système contractuel, déterministe, boot-safe et découplé → documentation prescriptive.
- Contrats : éclatement des monolithes en sous-domaines (climatisation, météo, ouvertures, éclairage, pannes) + création contrats alarme et diagnostic.
- Viessmann : promotion corpus ADR en architecture cible active + documents de migration.
- Météo : modèle déterministe validation / fallback / TTL / abstention → fin des états persistants non bornés.
- Température : consolidation intérieure/extérieure TTL 30 min + triggers temporels → mémoire strictement conditionnée.
- Éclairage garage : pivot vers mesure physique (`lux < seuil`) → suppression heuristiques saison/météo + exposition UI du seuil.
- Boiler : capteurs bridge local (état dégradé, feedback commande) + migration hors Vicare.
- Alarme : signal métier `ouvrants_entree` → découplage total des capteurs physiques.
- Automatisations : triggers `homeassistant.start` + garde `systeme_stable` → reconvergence post-boot généralisée.
- UI : contrôle luminosité garage + nettoyage blocs clim/aération obsolètes.
- Documentation : corpus UI couleurs, refonte socles UI status, dette technique, pré-changelog v11.
- Nettoyage : contrats legacy, capteurs Vicare, helpers obsolètes et documentation non gouvernée supprimés.

---

## 🧠 ARSENAL HA — v11 — STABLE — 2026-03-23
**Tags :** boiler, ecs, chauffage, climatisation, transactionnel, local, execution, robustesse  
**Signal net :**
- Boiler : exécution transactionnelle (request_id + ACK) → validation obligatoire (`applied`), suppression complète ViCare, souveraineté locale totale.
- ECS : refonte modulaire transactionnelle sur température réelle post-inertie + température max de cycle → autocorrection physique des offsets, écriture centralisée via `ecs_appliquer_consigne_bridge`.
- Chauffage : vérité interne Arsenal réaffirmée, script unifié `chauffage_appliquer_consigne` + verrou ACK, courbe de chauffe migrée en transactionnel (MQTT + ACK corrélé).
- Climatisation : moteur résilient post-condition + retry contrôlé, séparation orchestrateur / exécution, helpers dédiés (retry, compteur, état échec).
- Alarme : automation centrale v3 → exécution `restart` + garde `systeme_stable`.
- Éclairage garage : recalage nocturne + formalisation contractuelle de l'action physique.
- Système : capteurs transactionnels boiler (ACK, heartbeat, brûleur), helpers request_id, domaine `counter` introduit.
- Recorder / UI : nettoyage massif entités obsolètes + restructuration dashboard système.
- Documentation : refonte chauffage/ECS transactionnel + contrats boiler, ECS pipeline et recorder.

---

## 🧠 ARSENAL HA — v11.1 — STABLE — 2026-03-25
**Tags :** systeme, panne, ecs, reseau, netatmo, boiler, ui, normalisation  
**Signal net :**
- Système : contexte explicite (panne secteur, campagne réseau, stabilité) → conditionne tout comportement nominal.
- Panne secteur / réseau : sous-système structuré (helpers, timer, compteur, pipeline de remédiation cadencé) + orchestration réseau globale → fin des automations Netatmo concurrentes.
- ECS : transactionnel vérifié sous contexte système → inhibition nominale en régime dérogatoire, clarification guard de démarrage.
- Aération : persistance boot durcie + suppression massive `logbook.log` sur tout le pipeline.
- Chauffage : nettoyage traces logbook diagnostic et décision centrale.
- Boiler bridge : capteurs métier ajoutés (modulation brûleur, erreur récente, santé bridge, couleur modulation).
- UI : refonte `button_card_templates/` en architecture déclarative (`socles` / `génériques` / `dashboards`), introduction `carte_timer_status` et `carte_base_v2`, suppression variantes redondantes.
- Dashboard système : synthèse ECS remplacée par lecture santé boiler bridge.
- Recorder / logbook / documentation : nettoyage structurel, recentrage entités métier observables, invariants ECS mis à jour.

---

## 🧠 ARSENAL HA — v11.1.1 — STABLE — 2026-03-25  
**Tags :** chauffage, boiler, verite, contrats, ui, normalisation  
**Signal net :**
- Chauffage : bascule complète en vérité chaudière → `programme_chauffage` et consigne appliquée dérivés du `boiler_heating_setpoint`, fin de toute reconstruction locale.
- Chauffage : abandon de la mémoire décisionnelle comme source → les capteurs deviennent des lectures du réel, plus des projections Arsenal.
- Chauffage : introduction assumée de l’état `Inconnu` → signal explicite des désynchronisations ou influences externes.
- Chauffage : stabilisation des dérivations (tolérance flottante) + disponibilité alignée sur le bridge → capteurs cohérents avec la réalité système.
- Contrats : correction conceptuelle majeure → passage de “frontière d’exécution” à “cohérence d’exécution”, séparation nette logique / physique.
- Contrats : repositionnement des capteurs chauffage comme interfaces de lecture réelle.
- Boiler : affirmation du bridge comme source unique de vérité exposée → Arsenal cesse toute reconstruction thermique.
- UI : correction sémantique ACK → passage en logique statut (`socle_status_72`), clarification du cycle transactionnel (accepted ≠ applied).
- Documentation : alignement complet des contrats chauffage avec le modèle boiler bridge.
- Infrastructure : normalisation changelog v11 + nettoyage mineur sans impact fonctionnel.

---

## 🧠 ARSENAL HA — v11.1.2 — STABLE — 2026-03-26  
**Tags :** climatisation, alarme, boiler, correction, normalisation, robustesse  
**Signal net :**
- Climatisation : correction critique d’un `binary_sensor` invalide (`seuil_extinction_heat_atteint`) → passage valeur numérique → condition booléenne réelle, rétablissement du seuil OFF.  
- Climatisation : fiabilisation complète des capteurs seuils (COOL / HEAT / DRY) → suppression des conversions `float(default)`, introduction guard `unknown/unavailable`, fin des faux positifs silencieux.  
- Climatisation : nettoyage structurel templates → suppression `default_entity_id`, homogénéisation Jinja, recentrage strict sur logique booléenne.  
- Alarme : externalisation de la temporalité du blocage d’armement → suppression logique locale (`delay`), adoption `timer.blocage_armement_auto` comme mécanisme canonique.  
- Alarme : introduction invariant structurel blocage ↔ timer + watchdog dédié → détection et correction minimale des incohérences (fin des blocages orphelins).  
- Boiler : alignement complet du contrat MQTT avec l’implémentation réelle → suppression modèle confort/réduit/programme, unification `set_temperature`, clarification ACK et payload.  
- Boiler : enrichissement télémétrie (modulation brûleur) + clarification frontière → chaudière = réalité technique, Arsenal = sémantique métier.  
- Documentation : structuration massive des contrats climatisation (besoins, autorisations, blocages, cohérence, décision, seuils) → disparition des zones grises.  
- Documentation : refonte contrats alarme (blocage, watchdog, diagnostic) → séparation stricte diagnostic vs correction structurelle.  
- Système : nettoyage silencieux global (scripts, automations, incohérences diffuses) sans impact fonctionnel visible.  

---

## 🧠 ARSENAL HA — v11.1.3 — STABLE — 2026-03-27
**Tags :** chauffage, boiler, execution, contrats, normalisation, determinisme  
**Signal net :**
- Boiler : formalisation du socle transactionnel → contrats ACK, script exécutif et frontière MQTT ; le bridge devient la frontière contractuelle entre logique Arsenal et réalité physique.
- Chauffage : introduction du guard `boiler_bridge_online` dans la décision centrale → point d'entrée canonique de la capacité d'exécution pour tout le domaine chauffage.
- Chauffage : propagation de la condition bridge dans les automations (application courbe + démarrage) → fin de toute exécution hors capacité physique réelle.
- Chauffage : séparation stricte domaine physique Viessmann / domaine d'apprentissage Arsenal → `input_number` alignés sur les bornes réelles, auto-ajustement limité au sous-domaine contrôlé, zéro retour progressif.
- Chauffage : capteurs de suggestion refondus → propagation native `unknown/unavailable`, suppression des `float(default)` implicites, blocage hors domaine avec attributs diagnostics.
- Climatisation : GUARD `mode: single → restart` → idempotence réelle, zéro événement perdu.
- Notifications : `notification_envoyer_avance` sécurisé → validation service, résolution stricte `extra`, suppression des comportements implicites silencieux.
- Système : suppression des plans `evolutions_futures/` absorbés par l'implémentation → corpus documentaire strictement aligné sur l’implémentation réelle.

---

## 🧠 ARSENAL HA — v11.1.4 — STABLE — 2026-03-28
**Tags :** retry, transactionnel, robustesse, alarme, diagnostic, contrats, normalisation  
**Signal net :**
- Chauffage / ECS : déploiement du retry transactionnel comme couche externe de résilience → infrastructure complète (helpers, timers, pipeline 4 automations par domaine), aucune logique de retry dans les scripts exécutifs, invariant ACK préservé.
- Alarme : watchdog rebranché sur déclencheur structurel (`binary_sensor.blocage_armement_incoherent`) → fin de la stabilisation par `delay` interne, alignement strict diagnostic → action.
- Boiler / Alarme : normalisation kebab-case des contrats (`CONTRAT_*.md` → `socle_transactionnel.md`, `mqtt_ack_ha.md`, `script_executif.md`, `51_ouvrants_entree.md`, `90_ui.md`) → fin du suffixe redondant avec le dossier parent, aucun changement fonctionnel.

---

## 🧠 ARSENAL HA — v11.1.5 — STABLE — 2026-03-29
**Tags :** presence, mobile, alarme, high_accuracy, securite, templates  
**Signal net :**
- Présence : introduction du sous-système High Accuracy mobile contextuel → capteur d'approche, timer anti-spam GPS, canal unifié `script.envoi_commande_mobile`, contrat dédié encadrant le signal probabiliste hors décision centrale.
- Alarme : désarmement basé sur présence réelle fiabilisé → réduction des faux négatifs à l'entrée domicile.
- Templates : écarts de consigne migrés vers `availability:` natif → suppression des fallbacks `unknown/unavailable` dans `state:`, propagation correcte des indisponibilités.

---

## 🧠 ARSENAL HA — v11.1.6 — STABLE — 2026-03-30
**Tags :** zones, presence, securite, aeration, architecture, cleanup  
**Signal net :**
- Architecture : introduction du domaine spatial `zone` comme brique de premier rang Arsenal (`zone: !include_dir_merge_list zones/`) → passage d'un géofencing implicite à un socle spatial explicite et contractuel, contrats `zones.md` + `structure_includes/zones.md` ajoutés.
- Aération : suppression complète du sous-système de notifications (4 booleans + 4 automations + 1 datetime) → l'aération redevient un domaine purement informatif.
- Aération : ancrage temporel via `sensor.periode_meteo` (`'nuit'`) en remplacement du hardcode `now().hour >= 22 or < 9` → fin d'une dépendance fragile au mur d'horloge.

---

## 🧠 ARSENAL HA — v11.1.7 — STABLE — 2026-04-XX
**Tags :** presence, volets, pluie, garage, netatmo, bluetooth, data_driven, sensors, decision, refactor_majeur  
**Signal net :**
- Bascule data-driven généralisée : sensors porteurs de vérité métier, scripts réduits à des exécutants purs, automations cantonnées à l'orchestration → externalisation totale des décisions sur volets/pluie, présence, garage.
- Volets / pluie : pipeline décomposé en `template sensor → automation → script` avec politiques contractuelles asymétriques exposées en attribut (`sejour_protection_totale` vs `chambres_conditionnelles`) → fin des branches conditionnelles dans le script exécutif.
- Présence : trigger natif `platform: zone` sur `zone.approche_securite` en remplacement des `binary_sensor.approche_*` intermédiaires → déclenchement structurel aligné sur le modèle Home Assistant natif.
- Système : sous-système diagnostic Netatmo / Bluetooth complet (scores WiFi/RF agrégés, alertes `*_degrade` et `connectivite_ko`, customize, groupes, dashboard) → couche "qualité du monde réel" formalisée.
- Cleanup massif : corrections en lot de références d'entités inexistantes (Zigbee LQI, point de rosée, BSSID, chauffage retry timer, batteries SwitchBot, déshumidificateur) → réduction silencieuse de la dette de cohérence.

---

## 🧠 ARSENAL HA — v12.0.0 — DURCISSEMENT ARCHITECTURAL — 2026-04-XX
**Tags :** architecture, climatisation, meteo, vacances, vmc, bssid, eclairage, integrite, durcissement, refactor_majeur  
**Signal net :**
- Pattern "verrou d'admissibilité" généralisé (climatisation HEAT/COOL/DRY) → l'exécution directe sans admissibilité devient contractuellement interdite, séparation stricte besoin admissible / exécution.
- Météo : monolithes `jardin.yaml` (température + humidité relative) remplacés par pipelines contractuelles complètes (sources validées → cible robuste → diagnostic fusion → façade), EWMA orchestré, contrats `axe_temperature_jardin` et `axe_humidite_relative_jardin` formalisés.
- Mode Vacances : passage d'un booléen plat à un socle quatre composantes (calendrier, demande, effectivité, intégrité) → fin de la vérité plate.
- VMC : reconstruction de la vérité depuis les deux relais physiques `switch.vmc_l1/l2`, déclassement explicite du booléen UI, watchdog et capteur de cohérence introduits.
- Système : introduction des capteurs d'intégrité des réglages (`integrite_reglages/`) → un état système n'est exploitable que s'il est explicitement valide, validation explicite en prérequis à l'exécution.

---

## 🧠 ARSENAL HA — v12.1 — STABLE — 2026-04-XX
**Tags :** chauffage, preconfort, vacances, decision_centrale, diagnostic, meteo_interieure, ui, dashboard  
**Signal net :**
- Chauffage : refonte majeure du pré-confort retour Vacances → pipeline complet (orchestrateur + cycle + 3 template sensors), sortie du domaine `modes` vers `chauffage`, exception contractuellement explicite au comportement Vacances standard.
- Décision centrale : hiérarchie diagnostique étendue de 5 à 9 niveaux (`chauffage_raison_calculee` + `chauffage_mode_calcule`) → ordre d'évaluation revu, condition aération renforcée (`episode_en_cours AND aeration_confirmee`), nouvelle raison `pre_confort_vacances`.
- Météo intérieure : nouveau domaine pipeline multi-capteurs (sources → consolidation → stabilisation → façade) sur température et humidité relative, contrats formalisés, remplacement des `backup_zigbee.yaml`.
- Dashboard système : convention binaire `alert` / `off` généralisée → suppression systématique des états intermédiaires sur les capteurs d'agrégation.

---

## 🧠 ARSENAL HA — v12.1.1 — STABLE — 2026-04-XX
**Tags :** chauffage, deshumidificateur, meteo, jardin, ewma, humidite, robustesse, normalisation  
**Signal net :**
- Température jardin : durcissement contractuel du pipeline EWMA v1.2 → `float(none)` au lieu de `float(0)` (fin de la fabrication silencieuse de S(t-1)), qualification explicite de S(t-1) en précondition CAS 3, CAS 2bis de reseed de secours, gardes défensives multiples, sentinelle `-20` propagée jusqu'à `unavailable` sur la façade.
- Déshumidificateur : passage des automations on/off en strict événementiel (suppression du polling et de `systeme_stable` en trigger) → suppression de `guard.yaml` et `logique.yaml`, nouveau `demarrage_recommande.yaml`, validation des prérequis de sécurité dans `forcer_etat.yaml`.
- Chauffage : rappel décisionnel sur `boiler_bridge_online` (montée uniquement) couvre l'espace décisionnel bloqué pendant la déconnexion bridge, bypass override opérateur sur l'anti-rebond géoloc formalisé.
- Humidité relative intérieure : pipeline stabilisation v1.1 (fraîcheur mémoire par zone, double TTL 1800 s nominal / 7200 s post-boot), états passés en valeurs numériques arrondies.

---

## 🧠 ARSENAL HA — v12.2 — STABLE — 2026-04-09
**Tags :** transactionnel, switchbot, deshumidificateur, boiler, guard, bots, esphome, ble, refactor_majeur  
**Signal net :**
- Généralisation du modèle transactionnel `request → execution → guard → verdict → trace` à tous les actionneurs physiques (SwitchBot, déshumidificateur, boiler) → socle `transactions_bots/` multi-domaines extensible sans duplication, contrat `switchbot_transactionnel.md`.
- Déshumidificateur : rupture architecturale → suppression des automations monolithiques on/off, pipeline structuré 6 automations + script d'application pur + script guard comme seul juge de vérité post-commande, contrat `deshumidificateur_guard.md`.
- Boiler : exposition HA du guard (cohérence bridge + fraîcheur diagnostics) via template sensor `guard_stale` et 4 cartes synthèse, contrat `guard_exposition_ha.md`.
- ESPHome : scan BLE agressif activé sur proxies 2/3/4 (window = interval = 1100 ms, active=true) → charge radio accrue assumée en échange de latence réduite et stabilité bots.
- Documentation : introduction du système d'étiquettes Arsenal (automatisations, capteurs, helpers, scripts, palette UI) → base normative pour audit et tooling.

---

## 🧠 ARSENAL HA — v12.2.1 — STABLE — 2026-04-XX
**Tags :** invariants, vacances, deshumidificateur, ui, projection, verite_metier, normalisation, palette  
**Signal net :**
- Invariants formalisés et rendus systématiques → la fin d'une contrainte temporelle est un trigger de premier ordre (timers déshumidificateur en triggers), l'UI lit exclusivement la vérité métier (jamais la projection ni la source physique brute), une condition exprime un état atomique indépendant et ne réplique pas le trigger.
- Vacances : scission `actions.yaml` en `application_debut.yaml` + `application_fin.yaml`, enrichissement normatif des automations de projection avec périmètre négatif explicite → consolidation de la séparation projection (`input_select.mode_maison`) / vérité métier (`binary_sensor.vacances_actives`) établie en v12.2.
- Déshumidificateur : scission `retry.yaml` en `retry_on.yaml` / `retry_off.yaml`, conditions `template` remplacées par `state` atomiques, timeout guard porté de 35 s à 125 s (alignement empirique sur latence ACK SwitchBot réelle).
- UI : `carte_mode_maison` corrigée → `socle_toggle` (interactif) → `socle_status` (lecture seule) sur `binary_sensor.vacances_actives`, notifications climatisation rebranchées sur `sensor.clim_mode_local` au lieu de `climate.clim` brut, palette structure alignée (info bleu canonique, vacances actives vert au lieu de jaune).
- Pipeline météo jardin : 4 fichiers renommés selon `physical quantity first, functional qualifier second, zone last` → chaque fichier porte le nom de l'entité qu'il produit, pas la famille YAML.

---

## 🧠 ARSENAL HA — v12.2.2 — STABLE — 2026-04-XX
**Tags :** invariants, vacances, chauffage, contexte_parametre, autorisation, simulation_presence, lovelace, outillage_externe, robustesse  
**Signal net :**
- Nouveau pattern architectural : **contexte = transformation réversible d'un paramètre métier** → trois propriétés obligatoires (réversibilité avec sauvegarde + sentinelle, idempotence reconnaissant son propre état, encapsulation dans un script dédié portant la transaction). Premier emploi : adaptation contextuelle de la consigne réduite chauffage pendant les vacances (`script.vacances_adapter_consigne_reduite` / `script.vacances_retirer_consigne_reduite`), réutilisable pour toute paire (contexte, paramètre).
- Moteur d'autorisation extrait dans un capteur canonique → `binary_sensor.simulation_presence_autorisee` remplace trois conditions `or` dupliquées dans les automations de simulation de présence (entrée, garage, chambre parents), alignement sur le pattern du climatisation admissibility lock.
- Invariant d'exécution explicité : **tolérance au démarrage** → toute automation consommant un état métier au boot absorbe une phase de stabilisation, application via `delay: "00:00:20"` conditionné au trigger `homeassistant.start` sur les automations `application_debut` / `application_fin` du domaine Vacances.
- Convention UI généralisée : ~25 dashboards Lovelace ramenés à la forme minimale `views: - badges: cards:`, métadonnées sidebar centralisées dans `lovelace/dashboards.yaml` → fin d'un facteur de désynchronisation silencieuse.
- Standard d'outillage externe formalisé : verrou d'exécution + détection d'idempotence + stratégie de rollback pour scripts critiques hors Arsenal → premier emploi sur `update_from_latest_backup.sh` (Termux), grille de revue pour les futurs scripts d'import/export/migration/déploiement.

---

## 🧠 ARSENAL HA — v12.3 — ÉLARGISSEMENT CONTRÔLÉ — 2026-04-XX
**Tags :** nas, imprimerie, outils_externes, ups, shutdown, logbook, system_log, alarme, principes_generaux, refactor_majeur  
**Signal net :**
- Ouverture d'un nouveau type de domaine : la **supervision d'outils externes**, avec patron stratifié réutilisable (mesures → état → santé par axe → santé synthèse → alerte) → premier emploi sur le NAS Imprimerie (9 capteurs `nas_*`, automation `alerte_nas`, dashboard dédié, contrat `outils_externes/nas_imprimerie/monitoring.md`). Règle : un capteur ne saute jamais une couche, l'UI ne consomme que la synthèse et l'alerte.
- Fermeture de la boucle UPS : politique d'arrêt HA déclarée et exécutée → `binary_sensor.critere_ups_sur_batterie` comme critère canonique, automation `ha_shutdown_ups` (seuil + délai + action), chaîne `sensor.ups_*` consolidée, dashboard dédié, contrat `ups_arret_ha.md`. Fin de la coupure implicite à l'extinction de l'UPS.
- Bifurcation du contrat journalisation → `logbook.md` v2.1 (narratif fonctionnel destiné à l'humain) et `system_log.md` v1.1 (technique destiné à l'opérateur et au diagnostic) deviennent jumeaux et mutuellement exclusifs, chacun avec sa règle d'admission ABC. Impact immédiat : suppression du `system_log.write` d'abstention dans le script de fin de vacances.
- `principes_generaux.md` promu au rang de **recueil normatif des invariants universels d'Arsenal** → passage d'un document monothématique (robustesse au rechargement YAML) à un document de version dont les instanciations plateforme (HA, MQTT, shell) sont traitées dans des documents dédiés qui citent les principes.
- Alarme : réécriture de tous les en-têtes au format contractuel canonique (🗂️ COUCHE, 🧱 TYPE, 🔍 NIVEAU DE CONFIANCE, 🎯 RÔLE, 📡 SOURCE, ⚙️ LOGIQUE, 🔗 SATELLITE) → alignement opposable sans changement de logique, plus retouche sémantique sur le pipeline humidité intérieure (`'unknown'` littéral → `none` natif).

---

## 🧠 ARSENAL HA — v13 — STABLE — 2026-04-XX
**Tags :** bouclage_ecs, visite, decouplage, bluetti, panne_secteur, imprimerie, ui, layout_card, navigation, refactor_majeur  
**Signal net :**
- Bouclage ECS : changement de paradigme → modèle thermique opportuniste + présence remplace modèle plage horaire + présence (contrat v2.1.2), `binary_sensor.bouclage_autorise` conserve son nom mais sa sémantique est entièrement remplacée. Helper renommé (`bouclage_plage_active` → `bouclage_auto_active`), suppression des `input_datetime` de plage horaire, seuils ON/OFF dynamiques exposés en UI.
- Visite : découplage complet du bouclage ECS → retrait de toutes les actions `switch.prise_bouclage` (activation, désactivation, securite_reboot, notification), section Énergie supprimée du contrat visite, invariant I5 reformulé. Migration UI de la carte Mode Visiteur du dashboard alarme vers le dashboard modes.
- Nouveau domaine Bluetti : 7 template sensors stratifiés (`secteur_present`, `sortie_ac_active`, `sur_batterie`, `batterie_faible`, `batterie_critique`, `alerte_active`, `sante_synthese`), automation d'alerte panne secteur, contrat dédié, carte de supervision système → application du patron outils externes établi en v12.3.
- Migration UI navigation : `type: grid` / `horizontal-stack` → `custom:layout-card` sur toutes les barres de navigation (météo, imprimerie, voiture), ressource JS ajoutée, suppression définitive de `bouton_spacer.yaml` remplacé par `grid-template-columns` + `view_layout` déclaratif.
- Imprimerie : agrégation humidex par zone (administratif / atelier) via `carte_climat_zone`, refonte du bruit en `bruit_activite`, NAS factorisé en include partagé entre dashboard imprimerie et dashboard NAS, réorganisation arborescente `imprimerie/nas_*.yaml` → sous-dossier `imprimerie/nas/`.

---

## 🧠 ARSENAL HA — v13.1 — STABLE — 2026-04-XX
**Tags :** bssid, bouclage_ecs, ecs_petite_maison, decouplage, defense_profondeur, contrats, normalisation, maturite  
**Signal net :**
- BSSID : refondation architecturale → passage d'une garde globale ("un adulte dans Maison securite") à une **garde locale par source** avec couplage canonique strict source ↔ personne (`telephone_antoine_bssid_dynamic` → `person.valentin`, `telephone_constance_bssid_dynamic` → `person.constance`). Sources évaluées indépendamment, fusion après filtrage, défense en profondeur niveau sensor + garde résiduelle à l'écriture. Élimine la pollution silencieuse du référentiel (un BSSID observé par le téléphone d'une personne en déplacement ne pouvait plus être validé par la présence d'une autre au domicile).
- Bouclage ECS : séparation stricte état logique / état physique → fin de cycle manuel éteint le flag `bouclage_ecs_5_minutes_en_cours` **inconditionnellement**, switch `prise_bouclage` arbitré séparément (éteint uniquement si AUTO non autorisé), suppression de la dépendance d'AUTO au flag manuel → AUTO devient idempotent et autonome. Contrat `bouclage.md` v2.2.1.
- ECS Petite Maison : extraction complète en sous-domaine autonome → dashboards dédiés (`ecs-petite-maison-dashboard` + `reglages-ecs-petite-maison-dashboard`), sortie des dashboards Réglages ECS et Diagnostics ECS, templates de cartes spécialisés, capteur couleur dédié.
- ECS Petite Maison : changement de source canonique → `water_heater.petite_maison.current_temperature` avec validation `[20, 80] °C` remplace `sensor.petite_maison_bottom_tank_water_temperature` et son fallback `float(0)` → fin des valeurs `0.0 °C` post-restart, repli explicite vers la dernière valeur valide ou `unknown`. Contrat `cumulus_petite_maison.md` étendu.
- Templates UI : introduction de `carte_kpi_bleu` générique → remplace l'ad-hoc `nas_imprimerie_info` (supprimé), 5 cartes du dashboard NAS Imprimerie migrées. Nouveau contrat `ressources_lovelace.md`.

---

## 🧠 ARSENAL HA — v13.2 — STABLE — 2026-04-XX
**Tags :** sommeil, withings, snapshot, integrite_parametres, taxonomie, vmc, atomicite, conformite, imprimerie, regime_acoustique, refactor_majeur  
**Signal net :**
- Sommeil : refonte complète autour d'un **snapshot consolidé Arsenal** → rupture de la dépendance directe aux capteurs Withings, helpers Population A (`input_number.sommeil_derniere_nuit_*`), automations de consolidation et de détection nuit manquante, capteurs dérivés rebranchés via garde `sommeil_derniere_nuit_valide`, statistiques redimensionnées (1000/2000/4000 → 20/30/60 échantillons reflétant la cardinalité réelle), dashboard `sommeil-dashboard` dédié, contrat `sommeil.md`.
- Intégrité paramètres : taxonomie unifiée appliquée à 6 capteurs `parametres_invalides_*` (chauffage, VMC, déshumidificateur, éclairage, vacances, bouclage ECS) → patron normatif unique (state booléen + attribut `cause` priorisé + `helpers_indisponibles` + attributs par invariant), principe d'**indisponibilité stricte** (toute source `unknown/unavailable` rend l'invariant violé, pas d'optimisme silencieux), nouveau capteur `modes_maison`, contrat `parametres_invalides.md` centralisé.
- VMC : durcissement de la chaîne exécutive → capteur de demande purgé de toute mémoire d'état, scripts de bascule passés en `mode: single` avec `delay 200 ms` entre `turn_off` et `turn_on` (séquence atomique non interruptible), capteur de cohérence physique tolérant les transitoires < 2 s (`delay_off: 2 s`), automation `gestion_auto` réécrite (triggers restreints `on/off`, conditions `state` atomiques, garde explicite post-délai, branche `default` fail-safe), nouveau capteur de conformité décision.
- Déshumidificateur : capteur de conformité d'exécution observable (commande émise vs état physique observé), `request_source` alignés sur les noms canoniques des automations retry → suppression d'une dérivation héritée.
- Imprimerie : nouveau régime acoustique en pipeline 3 niveaux (numérique brut par machine → qualification → agrégation atelier), 3 contrats par machine (Komori, Bobst, Media), suppression de l'ancien `bruit_activite`. Éclatement du dashboard météo agrégé en 4 dashboards spécialisés (température, HR, HA, humidex), navigation 9 colonnes.

---

## 🧠 ARSENAL HA — v13.3 — STABLE — 2026-05-XX
**Tags :** cardio_nuit, sante, snapshot, baseline, reference_personnelle, respiratoire, sommeil, volets_pluie, recorder, etiquettes  
**Signal net :**
- Cardio nuit : nouveau sous-système complet → pipeline `mesure Withings → snapshot Arsenal → état qualitatif + delta baseline → anomalie binaire → confirmation de persistance → 3 capteurs couleur UI → dashboard dédié`. Application directe du pattern snapshot/interprétation établi pour le sommeil en v13.2, avec couche supplémentaire de **confirmation de persistance** sémantiquement distincte de la détection brute (`anormal` non confirmé → orange, confirmé → rouge). Saut sémantique : le système expose désormais un état physiologique interprété, plus seulement l'état brut.
- Couleur respiratoire : bascule vers référence personnelle → seuils absolus universels (11/17/20/23 rpm) remplacés par delta vs moyenne glissante 14 j, plage de validité explicite `[8, 30]` rpm, attributs diagnostic exposés (`reason` priorisé, `reference_7j/14j/30j`, `delta_14j`). Cohérence inter-domaines avec cardio. Point d'attention assumé : dérive lente de la baseline elle-même à instruire en v13.4+.
- Sommeil : sécurisation de la consolidation → triggers temporels de rattrapage (`06:00`, `09:00`) ajoutés au trigger événementiel, couvre les cas où la transition de `donnees_exploitables` survient avant le démarrage de HA ou échappe à la fenêtre de stabilisation. Contrat migré `contrats/sommeil.md` → `contrats/sante/sommeil.md` (cohérence avec `sante/cardio_nuit.md`).
- Volets pluie : correction de fiabilité → cibles alignées sur le nommage canonique `cover.<piece>` du registre HA (`cover.volet_arnaud` → `cover.chambre_arnaud`, etc.), logique décisionnelle et invariants préservés.
- Documentation : structuration par sous-domaines → `architecture/recorder.md` → `architecture/recorder/{contrat,fiche_decision}.md`, `architecture/etiquettes_*.md` → `architecture/etiquettes/{automatisations,capteurs,helpers,scripts}.md`, fichiers plats devenus domaines structurés. Allègement de `recorder.yaml` (suppression des blocs de commentaires détaillés Population A/B, doctrine portée par le contrat).

---

## 🧠 ARSENAL HA — v14 — STRUCTURELLE MAJEURE — 2026-05-XX
**Tags :** nomenclature, arborescence, contrats, gouvernance, voiture, autonomie, snapshot_atomique, cumulus_petite_maison, refactor_majeur, durcissement  
**Signal net :**
- Nomenclature canonique formalisée → préfixe numérique strict `00_*` à `19_*` sur tous les dossiers consommés par `configuration.yaml` (renommages : `08b_counters` → `09_counters`, `09_scripts` → `10_scripts`, `10_automations` → `11_automations`, `11_template_sensors` → `12_template_sensors`, `12_sensor_platforms` → `13_sensor_platforms`, `mqtt_sensors` → `14_mqtt_sensors`, `zones` → `17_zones`, `lovelace` → `18_lovelace`, `button_card_templates` → `19_button_card_templates`, `documentation_arsenal` → `00_documentation_arsenal`). Le numéro n'est plus décoratif : il fixe l'ordre canonique de lecture (documentation → helpers → timers → counters → scripts → automations → templates → sensors → MQTT → panels → zones → UI), et la documentation précède strictement le code rendant visible la primauté du contrat sur l'implémentation. 1263 fichiers déplacés / renommés.
- Corpus de contrats normatifs formalisé → `00_documentation_arsenal/contrats/` devient le **point d'entrée unique** de la gouvernance Arsenal, avec contrats publiés, opposables et versionnés sur Alarme (13 fichiers numérotés `00_gouvernance` à `99_hors_perimetre`), Chauffage (13 fichiers avec sous-arborescence `15_capteurs/`), ECS (`00_fondations` → `03_orchestration`), Boiler, Bouclage, Babysitting, Cumulus petite maison, Aération. Principe : aucun YAML d'un domaine couvert ne doit plus exister sans contrat amont, toute évolution passe d'abord par le contrat.
- Voiture / Autonomie : passage à un **snapshot atomique** → trio de helpers cohérents (`autonomie_audi_etron_full` conservé + `audi_temperature_charge` nouveau + `audi_autonomie_corrigee_temperature` nouveau, normalisé à 20 °C), invariant critique posé en en-tête (tous écrits dans la même automation au même instant logique, snapshot pleine charge ≈ 100 %). La valeur figée devient un tuple cohérent permettant l'analyse de l'influence thermique sur l'autonomie.
- Suppressions assumées sans remplacement direct → 5 templates boiler ACK/feedback (couverts par `contrats/boiler/README.md`), 3 templates pré-confort (couverts par contrat), 4 templates + 1 automation ouvertures redondantes (sous-domaine sorti du périmètre), consolidation sommeil retirée (2 automations + 1 template), notifications domaine chauffage et climatisation absorbées par le canal central `notifications_mobiles.yaml`.
- Cumulus petite maison entre dans l'observabilité → nouvelle catégorie recorder « CONSOMMATION – CUMULUS PETITE MAISON » avec `sensor.petite_maison_modbuslink_1_2_electric_energy_consumption`, alignement sur le contrat dédié `cumulus_petite_maison.md`. Ajouts symétriques côté véhicule pour les helpers Audi température/correction.

---

## 🧠 ARSENAL HA — v14.1 — STABLE — 2026-05-08
**Tags :** ping_lan, supervision_reseau, high_accuracy, reentrance, cardio, hygiene_headers, normalisation, lovelace  
**Signal net :**
- Nouveau domaine **Ping LAN** : supervision réseau introduite de bout en bout avec contrat cadre, 6 groupes, capteur de synthèse `sensor.ping_lan_synthese` (lecture seule, aucune logique décisionnelle ni d'action en v14.1), template de bouton et intégration au dashboard de diagnostic système.
- High Accuracy : invariant **I-9 de réentrance** ajouté au contrat `mobile.high_accuracy.contextuel.md` (promu hors Draft) → chaque entrée valide dans la zone d'approche en mode armé absent ouvre un cycle indépendant sans considération des cycles antérieurs, implémenté par le passage de `mode: parallel` à `mode: restart` sur `high_accuracy_on.yaml`.
- Cardio : bascule en pipeline purement événementiel → suppression du déclencheur horaire fixe `06:00:00` dans `cardio_consolidation.yaml` (cohérent avec la philosophie données → consolidation établie en v13.3, et inverse partiellement le rattrapage temporel ajouté au sommeil en v13.3).
- Documentation : formalisation explicite de la **gouvernance Git** dans `architecture/git.md`, trois nouvelles fiches d'intention (cumulus petite maison à périmètre élargi, arborescence Lovelace, records de précipitations).
- Hygiène : campagne de normalisation des en-têtes sur **175 fichiers** consécutive à v14 (input_numbers 99, sensor_platforms 46, MQTT 14, groups 11, counters 4, customize 1) → purge des rubriques redondantes désormais portées par les contrats (hiérarchie décisionnelle, dépendances, lecture métier), grammaire typographique unifiée (majuscules, apostrophes typographiques), aucune logique modifiée.

---

## 🧠 ARSENAL HA — v14.2 — DOCS — 2026-05-09
**Tags :** outils_externes, nas_arsenal, search, audit, documentation_pure  
**Signal net :**
- Retrait complet de l'outillage mobile/PC obsolète → suppression des scripts Termux (`ha_find.sh`, `ha_find_contexte.sh`, `update_from_latest_backup.sh`) et PC (`ha_find_pc.py`, `ha_find_context.py`) + leurs documentations d'accompagnement (`README.md`, `script_termux.md`). Fin d'un écosystème externe.
- Formalisation de la future suite d'outillage **NAS Arsenal** → spécifications Arsenal Search (`vision_domaine.md`, `moteur_cli.md`, `webapp.md` dans `outils_externes/nas_arsenal/search/`), automatisation des diffs (`diff_auto.md`), fiches d'intention pour le moteur d'audit patrimonial et la rétention des sauvegardes.
- Correction éditoriale du changelog v14.1 → recentrage sur les fichiers à changement de comportement fonctionnel réel (les modifications strictement éditoriales d'en-têtes restent listées séparément).

---

## 🧠 ARSENAL HA — v15 — STABLE — 2026-05-12
**Tags :** self_audit, nas_arsenal, mqtt, supervision, contrats, quarantine_purger, retention_manager, normalisation, slugs  
**Signal net :**
- **Arsenal Self Audit** — supervision de l'audit patrimonial exécuté côté NAS exposée à HA : 5 capteurs MQTT (`audit_published_at`, `audit_statut`, `audit_total_anomalies`, `audit_total_observations`, `audit_version_auditee`), 4 template sensors de dérivation (`audit_age_minutes`, `audit_stale`, `audit_error`, `audit_alerte`), helper de seuil de fraîcheur, carte UI dédiée sur le dashboard système. Application directe du patron outils externes (mesures → état → santé par axe → synthèse) établi en v12.3 et appliqué à Bluetti en v13.
- Formalisation contractuelle de la suite d'outils NAS Arsenal → migration des fiches d'intention `evolutions_futures/moteur_audit.md` et `nas_gestion_retention_sauvegardes.md` vers 4 contrats publiés sous `outils_externes/nas_arsenal/` : `audit/audit.md`, `audit/mqtt.md`, `quarantine_purger.md`, `retention_manager.md`. Passage du statut prospective au statut opposable.
- Aération : normalisation lexicale des slugs → `sensor.deltaT_*` (camelCase) → `sensor.deltat_*` (minuscules strictes) sur les 6 zones (entrée, séjour, palier, chambres Arnaud / Matthieu / parents), propagation dans l'orchestrateur `m3_0_analyse_deltat.yaml`, template `blocage_chauffage_valide.yaml` et contrats associés.
- UPS NAS Imprimerie : francisation du capteur `nas_imprimerie_ups_on_battery` → `nas_imprimerie_ups_sur_batterie`, alignement contrat `synthese_sante.md` + template `nas_ups.yaml`.
- Hygiène modes : retrait définitif des actions sur `input_boolean.bouclage_visiteur` lors de l'activation du mode Normal (réactivation retirée) et du mode Vacances (désactivation retirée) → clôture définitive du découplage Visite ↔ Bouclage initié en v13. Réorganisation : helpers `reload_integrations.*` déplacés vers `system/reload_integrations/`.

---

## 🧠 ARSENAL HA — v15.1 — STABLE — 2026-05-12
**Tags :** self_audit, arsenal_self, contrats, meteo, palmares_pluie, utility_meter, snapshot  
**Signal net :**
- Self Audit consolidé → contrat `audit/mqtt.md` passé en v1.0.1 (état actif et implémenté acté, clarification des payloads d'erreur via `error_reason`, du fichier `latest.verdict.json` côté NAS, et de la frontière d'autorité collecte brute / entités HA). Nouveau **contrat cadre `arsenal_self.md`** régissant l'exposition des entités du domaine d'auto-observation.
- Nouveau sous-domaine **palmarès journalier de pluie** → matérialisation de la fiche d'intention `precipitations_records.md` (supprimée) : `utility_meter.pluie_journaliere` à reset quotidien sur `sensor.pluie_total_local`, deux automations (`palmares_journalier_snapshot` pour isolement du cumul de veille avant reset + `palmares_journalier_evaluation` pour analyse et mise à jour du classement), helpers de stockage (10 rangs × valeur + 10 rangs × date, snapshot veille, traçabilité dernière évaluation), capteurs de synthèse et d'anomalie structurelle, carte UI dédiée, contrat `meteo/pluie_palmares.md`.
- Persistance : historisation complète des nouvelles entités du palmarès dans `recorder.yaml` (helpers de rangs, dates, synthèse, anomalie, utility meter).

---

## 🧠 ARSENAL HA — v15.2 — DOCS — 2026-05-12
**Tags :** nas_arsenal, diff, release, documentation_pure, outils_externes  
**Signal net :**
- Domaine NAS Arsenal : structuration du sous-système de gestion des diffs → `diff_auto.md` déplacé dans un sous-domaine dédié `outils_externes/nas_arsenal/diff/`, fin du stockage plat à la racine de `nas_arsenal/`.
- Nouveau guide `diff_release.md` → formalisation documentaire de la génération et de la gestion des rapports de release côté NAS Arsenal.
- Historisation : intégration du changelog `v15_1.md` dans le suivi officiel de la branche v15.

---

## 🧠 ARSENAL HA — v15.3 — STABLE — 2026-05-15
**Tags :** nas_arsenal, arsenal_search, export, webapp, pipeline, cardio_nuit, pluie_palmares, lovelace, documentation  
**Signal net :**
- Arsenal Search : introduction d'une route `POST /export` sur la webapp → export Markdown direct des résultats de recherche sans persistance NAS ni reformatage intermédiaire, encapsulant le flux brut monochrome du moteur CLI. Normalisation forte du nommage (`arsenal_search_<slug>_<date>.md`) avec slugification ASCII stricte et limite dure de longueur.
- Arsenal Search : durcissement documentaire → `vision_domaine.md` et `webapp.md` mis à jour avec clarification explicite des non-objectifs v1 (pas d'historique, pas de planification, pas d'exports structurés multi-formats). Ajout des documents `pipeline_watcher.md` et `pipeline_nas_ha.md` pour la supervision et la visualisation textuelle du pipeline NAS ↔ HA.
- Cardio nuit : suppression de `initial: "[]"` sur `input_text.cardio_nuit_historique_7j` → abandon d'une initialisation artificielle au profit d'un état natif vide.
- UI Modes : simplification volontaire du dashboard réglages → suppression du bloc de pilotage global `mode_maison` et retrait du bouton d'activation directe Babysitting.
- Pluie palmarès : refonte du rendu UI → abandon du tableau Markdown au profit d'un affichage textuel hiérarchisé avec médailles emoji, plus robuste en mobile. Sécurisation supplémentaire du template via fallback `or []` sur l'attribut `records`.

---

## 🧠 ARSENAL HA — v15.4 — STABLE — 2026-05-17
**Tags :** alarme, intrusion, eclairage_jardin, race_condition, soleil, systeme_stable, recorder, cardio  
**Signal net :**
- Alarme intrusion : durcissement du délai d'entrée → ajout d'une garde `input_boolean.systeme_stable` et revalidation explicite de l'intrusion (`binary_sensor.ouverture_qualifiee_maison`) à l'échéance du timer avant toute action. Documentation assumée d'une dette technique temporaire : appel direct des actions sirène/panneau hors pipeline canonique.
- Éclairage jardin matin : campagne complète de fiabilisation temporelle → suppression des déclenchements parasites liés aux transitions `unavailable`, arbitrage explicite avec le cycle soir, abandon du trigger astronomique au profit d'un recalcul journalier fixe `00:01`, correction des ambiguïtés de jour civil (`next_rising` / `last_rising`) et remplacement de la dépendance à `sun.sun` par une comparaison mathématique directe sur timestamps.
- Éclairage jardin matin : validation structurelle renforcée → une plage devient invalide si `h_fin <= h_debut`, couvrant explicitement les cas où le soleil se lève avant l'heure programmée d'allumage.
- Recorder : extension de l'observabilité cardio avec historisation longue durée de `sensor.cardio_baseline_7j`.
- Historisation : intégration du changelog `v15_3.md` et suppression du document de planification obsolète `AUDIT_RELEASE_0.2.1.md`.

---

## 🧠 ARSENAL HA — v15.5 — STRUCTURELLE — 2026-05-20
**Tags :** eclairage_jardin, deadlines_persistantes, stateless, cumulus_petite_maison, robustesse_templates, mqtt, contrats, refactor_majeur  
**Signal net :**
- Éclairage jardin soir : bascule architecturale majeure → abandon des décisions temps réel basées sur états volatils au profit d'un modèle à **deadlines persistantes explicites** stockées dans des helpers `input_datetime`. Les décisions d'extinction deviennent entièrement déterministes et rejouables après restart.
- Jardin : clarification des responsabilités → `binary_sensor.lumiere_jardin_soir_extinction_autorisee` rétrogradé en capteur d'observabilité UI/diagnostic sans aucun rôle causal dans la chaîne exécutive. La causalité est désormais portée exclusivement par les deadlines persistantes et les automations temporelles.
- Éclairage jardin soir : refonte complète des automations `allumage.yaml` et `extinction.yaml` → enregistrement immédiat de l'heure d'allumage et de la deadline d'extinction, remplacement des triggers événementiels par des déclencheurs horaires stricts, ajout de routines de rattrapage post-redémarrage (`homeassistant.start`, `automation_reloaded`) protégées par revalidation temporelle.
- Nouveau pipeline séjour → introduction de `mouvements_sejour.yaml` chargé d'alimenter explicitement la chaîne de calcul des deadlines d'inactivité du cycle jardin.
- Cumulus petite maison : durcissement des templates → abandon des conversions `float` permissives et des filtres textuels `'unknown'` au profit de validations natives `is number` avec propagation explicite de `none` en cas de donnée invalide ou absente.
- Documentation NAS Arsenal : nettoyage du domaine Search avec suppression des anciens documents `moteur_cli.md`, `vision_domaine.md` et `webapp.md`. Ajout du document prospectif `EVOLUTION_MQTT_RELEASE_DIFF-1.md`.

---

## 🧠 ARSENAL HA — v15.5.1 — STRUCTURELLE — 2026-05-22
**Tags :** doctrines, eclairage, deadlines_persistantes, restart_safe, causalite_metier, separation_decision_action, lovelace, robustesse  
**Signal net :**
- Architecture : formalisation du corpus doctrinal Arsenal → création du sous-domaine `architecture/03_doctrines/` et migration des documents fondateurs (`principes_generaux`, `gestion_du_temps`, `separation_decision_action`, `git`, `nommage_entites`, `id_automatisations`). Ajout des doctrines `causalite_metier.md` et `entetes_fichiers.md`.
- Éclairage : généralisation du modèle à **deadlines persistantes** initié sur le jardin → abandon des temporisations `for:` au profit de deadlines stockées dans des helpers `input_datetime`, avec rattrapage explicite après restart (`homeassistant.start`) et reload (`automation_reloaded`).
- Éclairage entrée / garage / séjour : introduction d'un pipeline normatif commun `ecriture_deadline → extinction temporelle`, avec validation systématique du dépassement réel des deadlines via templates Jinja avant extinction.
- Éclairage entrée : normalisation de la perception → remplacement du capteur brut `binary_sensor.capteur_mouvements_entree_occupancy` par l'entité métier `binary_sensor.mouvement_entree`.
- Standardisation YAML : homogénéisation des en-têtes structurels Arsenal (Identifiant, Périmètre, Nature, Mode, Déclencheurs, Dépendances, Autorité, Idempotence, Interdits) sur les automations d'éclairage.
- Contrats métier : publication des nouveaux contrats `eclairage/entree.md` et `eclairage/sejour.md`.
- Lovelace voiture : amélioration de lisibilité analytique des graphes Audi avec lissage (`curve: smooth`) et agrégation hebdomadaire moyenne sur les séries autonomie/température.

---

## 🧠 ARSENAL HA — v15.6 — STABLE — 2026-05-22
**Tags :** climatisation, autorisations, fenetres, dry, cool, heat, diagnostic_ui, nas_arsenal, diff_release  
**Signal net :**
- Climatisation : harmonisation complète des chaînes d'autorisation COOL / HEAT / DRY → remplacement de `binary_sensor.fenetre_ouverte_maison` par `binary_sensor.fenetre_ouverte_maison_avec_delai` comme primitive métier canonique d'ouverture.
- DRY : suppression d'un risque d'arrêt transitoire lors d'ouvertures brèves de fenêtres → alignement comportemental avec les chaînes COOL et HEAT.
- Contrats climatisation : enrichissement documentaire des comportements temporisés d'ouverture, clarification des invariants des chaînes d'autorisation et des comportements par zone (`10_autorisations.md`, `20_chaines.md`, `90_observations.md`).
- UI diagnostic climatisation : mise à jour de `carte_clim_diagnostic_fenetres_maison` avec bascule sur la primitive temporisée et renommage des libellés diagnostic pour cohérence métier.
- NAS Arsenal Diff : extension du contrat `diff_release.md` au support des versions patch (`v15.5.1`), clarification de la gestion des collisions d'ancres et du tri canonique des releases.

---

## 🧠 ARSENAL HA — v15.6.1 — STABLE — 2026-05-22
**Tags :** climatisation, dry, admissibilite, deadlines_persistantes, restart_safe, lovelace, changelog, documentation  
**Signal net :**
- Climatisation DRY : refonte de `input_boolean.clim_dry_admissible` → suppression de l'activation immédiate, introduction d'une validation par stabilité temporelle continue de l'autorisation DRY via calcul basé sur `last_changed`.
- DRY : ajout des recalculs automatiques sur changement d'autorisation, démarrage Home Assistant et rechargement des automatisations → comportement désormais cohérent après restart et reload.
- DRY : enrichissement diagnostique avec les attributs `requalification_possible`, `age_autorisation_minutes` et `stable_depuis_minutes`, exposant explicitement l'état temporel de qualification.
- UI diagnostic climatisation : extension de `carte_clim_diagnostic_fenetres_maison` avec affichage direct de `input_boolean.clim_dry_admissible` et des métriques temporelles de stabilité DRY.
- Éclairage entrée / garage : poursuite de la migration vers les deadlines persistantes → remplacement complet des temporisations `for:`, ajout des triggers `homeassistant.start` et `automation_reloaded`, passage des automations d'extinction de `single` vers `restart` pour suppression des warnings `Already running`.
- Documentation : création de `prompt_changelog.md` fixant les règles rédactionnelles des changelogs Arsenal (style technique, priorité runtime, suppression des formulations narratives/doctrinales).
- Changelogs historiques : réécriture massive des versions v14 → v15.5.1 avec recentrage sur les comportements runtime, entités, helpers, triggers et fichiers réellement modifiés.

---

## 🧠 ARSENAL HA — v15.6.2 — STABLE — 2026-05-22
**Tags :** eclairage, extinction_automatique, deadlines, as_local, logs, warnings, temporisation  
**Signal net :**
- Éclairage : ajustement du mode d'exécution des automations d'extinction automatique → retour de `restart` vers `single` avec `max_exceeded: silent`, supprimant les warnings `Already running` sans réintroduire de concurrence d'exécution.
- Deadlines persistantes : homogénéisation des comparaisons temporelles via `| as_local` avant confrontation à `now()` → correction des ambiguïtés potentielles liées aux datetimes naïfs/localisés.
- Éclairage entrée / garage / séjour : alignement des vérifications temporelles dans les automations d'extinction automatique (`entree/extinction.yaml`, `garage/extinction_automatique.yaml`, `sejour/off.yaml`).
- Documentation inline : normalisation des commentaires `# ⚙️ MODE` et suppression d'un bloc documentaire redondant dans `sejour/off.yaml`.
- Historisation : intégration du changelog `v15_6_1.md` dans la branche v15.

---

## 🧠 ARSENAL HA — v15.7 — STABLE — 2026-05-23
**Tags :** babysitting, simulation_presence, bouclage_ecs, arsenal_self, mode_single, recorder, contrats, documentation  
**Signal net :**
- Babysitting : réécriture complète du contrat `babysitting.md` → structuration des sections, ajout des entités constitutives du domaine (helpers, timers, automations), clarification des règles d'écriture sur `input_boolean.mode_babysitting` et des impacts sur présence, chauffage et alarme.
- Simulation de présence : extension du domaine avec ajout de la zone `entree`, séparation des plages horaires par zone/période et formalisation de `binary_sensor.simulation_presence_autorisee` comme primitive d'autorisation d'exécution.
- Bouclage ECS : durcissement des règles d'autorité → restriction explicite des écrivains autorisés sur `switch.prise_bouclage`, autorisation nominative de `script.bouclage_ecs_5_minutes`, interdiction de pilotage par scripts tiers.
- Arsenal Self : clarification de la séparation entre capteurs MQTT bruts et capteurs calculés, enrichissement documentaire autour de `sensor.arsenal_self_audit_age_minutes`.
- Éclairage garage : ajout du contrat d'implémentation `garage_implementation.md`.
- Automatisations : campagne d'harmonisation avec ajout de `mode: single` sur plusieurs automations système/métier (`chauffage`, `electromenager`, `presence`, `sante`, `system`) afin de verrouiller les réentrances implicites.
- Recorder : extension de l'historisation aux capteurs `binary_sensor.fenetre_ouverte_etage` et `binary_sensor.fenetre_ouverte_rdc`.
- Publication GitHub : ajout du document `prompt_contrat_github.md` pour formaliser les règles de génération de contrats publiés.

---

## 🧠 ARSENAL HA — v15.7.1 — STABLE — 2026-05-25
**Tags :** audit_documentaire, alarme, notifications, humidite_relative, publication_github, climatisation, secrets, nettoyage  
**Signal net :**
- Audit documentaire : ajout du marqueur `<!-- audit:scope=doc -->` sur plusieurs changelogs et contrats afin de qualifier explicitement les documents purement documentaires pour les outils d'audit. Publication du contrat `publication/securite_publication_git.md`.
- Alarme intrusion : publication du contrat `50_intrusion_detection.md` → formalisation des automatisations d'intrusion, du délai d'entrée, de la séparation détection/décision et de l'usage direct de `alarm_control_panel.alarm_trigger`.
- Notifications : migration des automations NAS / Bluetti / voiture vers `script.notification_envoyer` avec usage de `cible: input_text.telephone_antoine_notify` et `titre:` → centralisation du canal de notification mobile.
- Notifications persistantes : homogénéisation des titres/messages et suppression de timestamps utilisateur dans plusieurs notifications système/métier.
- Coupure Internet : suppression de `persistent_notification.create` dans `script.coupure_internet`.
- Humidité relative intérieure : migration contractuelle vers `none` natif dans les branches d'abstention des templates `sensor.humidite_relative_brute_consolidee_<zone>` en remplacement de `'unknown'`.
- Climatisation UI : remplacement de `sensor.consigne_clim_appliquee_locale` par `sensor.consigne_clim_appliquee` dans les cartes `carte_clim_etat` et `carte_clim_synthese`.
- Déshumidificateur : renommage du `unique_id` `deshum_conformite_execution` → `deshumidificateur_conformite_execution`.
- Configuration système : déplacement de `trusted_proxies`, `external_url` et `internal_url` vers `secrets.yaml`.
- Nettoyage système : correction de `icone:` → `icon:` dans `01_customize/batteries.yaml`, correction d'en-tête `INPUT NUMBER` → `INPUT_NUMBER`, suppression de `12_template_sensors/system/ip_raspberry.yaml`.

---

## 🧠 ARSENAL HA — v15.7.2 — STABLE — 2026-05-26
**Tags :** climatisation, parametres_invalides, notifications, ui_couleurs, netatmo, aeration, m3, m4, diagnostics  
**Signal net :**
- Climatisation : abandon du modèle `offset_on/off` au profit de seuils explicites de déclenchement/extinction → ajout de 4 helpers dédiés (`clim_seuil_declenchement_*`, `clim_seuil_extinction_*`) et mise à jour du dashboard réglages avec nouveau markdown récapitulatif.
- Climatisation : clarification contractuelle de `clim_target_mode` → remplacement des couples `besoin_clim_*` + `autorisation_clim_*` par les primitives consolidées `besoin_clim_*_admissible`.
- Intégrité paramètres : création de `binary_sensor.parametres_invalides_climatisation` avec intégration dans `groups/parametres_invalides.yaml` et dans le contrat central `parametres_invalides.md`.
- Notifications : ajout d'une règle contractuelle imposant un emoji en préfixe des `persistent_notification.create`. Mise à jour des titres utilisateurs (`🚨 Badge inconnu`, `🔋 Audi A3 e-tron`).
- Aération M3/M4 : enrichissement documentaire des helpers de seuils/prolongations (`tiny/medium/high`), clarification des fallbacks runtime autorisés et suppression des anciennes exigences `logbook.log` au profit de traces runtime via helpers/timers.
- UI couleurs : extension de `03_exceptions.md` avec nouvelles catégories d'exceptions (NAV/HUB, visualisations quantitatives, accentuation intermédiaire, palette hydrique). Campagne de réalignement des couleurs UI sur les gris Arsenal canoniques.
- Navigation : mise à jour des couleurs `normal` et `eco` dans `bouton_navigation_dynamique.yaml`.
- Netatmo : refonte des états diagnostics → remplacement de `ko_homekit` / `ko_reseau` par `muet_ping_ok` / `muet_ping_ko`, avec mise à jour cohérente des textes, icônes et couleurs UI.
- Documentation : ajout des changelogs `v15_7.md`, `v15_7_1.md` et remplacement de `prompt_contrat_github.md` par `prompt_contrat_github_v2.md`.

---

## 🧠 ARSENAL HA — v15.7.3 — STABLE — 2026-05-27
**Tags :** climatisation, admissibilite, reconciliation_boot, dry, meteo, palmares_temperature, recorder, contrats  
**Signal net :**
- Climatisation admissibilité : ajout du contrat `capteurs/admissibilite/00_admissibilite.md`, de la chaîne DRY (`dry/admissibilite.yaml`) et des automatisations `reconciliation_boot.yaml` pour COOL, HEAT et DRY → recalculs post-redémarrage Home Assistant et post-rechargement des automatisations, harmonisation des trois chaînes. Mise à jour des contrats décision `10_decision.md`, `20_chaines.md`, `90_observations.md`, `08_securite.md`.
- UI climatisation : `clim_decision_synthetique_72.yaml` lit `sensor.clim_raison_decision` en remplacement de `input_text.climatisation_raison` (helper supprimé), ajout du cas `fenetre_ouverte` dans les blocages UI. Suppressions : `carte_clim_intention.yaml`, helper `climatisation/modes/deshumidificateur.yaml`, automatisation `dry_admissibilite.yaml` (déplacée vers `dry/`).
- Météo palmarès : ajout des sous-systèmes palmarès chaud et froid → contrats `palmares_chaleur.md` / `palmares_froid.md`, helpers `input_number` / `input_text` / `input_datetime`, capteurs template (palmarès chaud, froid, anomalies) et cartes Lovelace dédiées.
- Météo température jardin : ajout de `temperature_max_jardin.yaml` / `temperature_min_jardin.yaml` et des automatisations de clôture, reset, update, snapshot et évaluation min/max.
- Recorder : extension aux nouveaux helpers et capteurs météo, historisation des palmarès température chaud/froid.
- Historisation : intégration du changelog `v15_7_2.md`.

---

## 🧠 ARSENAL HA — v15.8 — STABLE — 2026-05-28
**Tags :** chauffage, geofencing, climatisation, guard, securite, doctrine_registres, hysteresis, contrats  
**Signal net :**
- Inhibition géofencing chauffage : réécriture du contrat `60_absence_inhibition_geofencing.md` et passage à une architecture deux couches → capteur de qualification `binary_sensor.chauffage_inhibition_geofencing_requise` (lecture pure, sans mémoire) et helper d'état `input_boolean.chauffage_inhibition_geofencing` (mémoire d'hystérésis). Abrogation de la règle « une seule activation par cycle d'absence » : le mécanisme devient réactivable. Suppression de la borne de durée maximale au profit d'une sortie gouvernée par hystérésis (offsets ON/OFF). Gating absence délégué à la Décision Centrale (présence évaluée avant inhibition), verrouillé par l'invariant CI `INV-GEO-3`. Suppression du helper `inhibition_geofencing_mode.yaml` et de la tuile `input_boolean.blocage_geofencing` du dashboard réglages.
- Autorisation système chauffage : `binary_sensor.chauffage_autorise_systeme` recentré sur la sécurité système → retrait de `input_boolean.chauffage_standby_force` de la condition d'état, désormais conditionné par le seul `chauffage_blocage_aeration`. Le `standby_force` reste exposé en attribut informatif.
- Doctrine chauffage : ajout de `01_doctrine_registres.md` et d'une série d'amendements aux contrats existants (`00`, `20`, `30`, `40`, `50`, `70`, `90`), réécriture partielle de la table de décision canonique (`80`) et ajout du fichier CI `registres_entites.yaml`.
- Climatisation Guard : retrait des triggers et variables présence/ouvertures → le Guard ne surveille plus que la cohérence interne `target_mode ↔ climate.clim ↔ switch.clim_power`. Remplacement des anciens invariants par INV-1/2/3. Contrat `08_securite.md` v1.3 → v1.4 : introduction du test d'universalité (volets modes/paramètres) comme critère de démarcation Sécurité/Métier, et documentation du recouvrement assumé Guard/Watchdog sur INV-1.
- Raison de décision clim : `sensor.clim_raison_decision` contextualise les blocages chauffage (`blocage_poele`, `blocage_aeration`) au seul contexte HEAT via le calcul `heat_contexte`, `blocage_horaire` et `fenetre_ouverte` restant transversaux.
- Historisation : intégration du changelog `v15_7_3.md`.

---

## 🧠 ARSENAL HA — v15.8.1 — STABLE — 2026-05-29
**Tags :** climatisation, blocages, aeration, cool, dry, diagnostics, ui, contrats, normalisation

**Signal net :**
- Climatisation : ajout du helper `input_boolean.clim_blocage_aeration_etage_actif` et du capteur `binary_sensor.clim_blocage_aeration_etage_reel` afin de dissocier la recommandation d’aération de l’application effective du blocage climatisation.
- Autorisations COOL / DRY : remplacement de la dépendance directe à `binary_sensor.aeration_preferable_etage` par `binary_sensor.clim_blocage_aeration_etage_reel`.
- Réglages climatisation : ajout d’un paramètre utilisateur permettant d’activer ou désactiver le blocage automatique lié à l’aération de l’étage.
- Diagnostics UI : réécriture de la carte d’aération étage pour afficher l’état réel du blocage climatisation et non plus la simple recommandation d’aération.
- Contrats climatisation : ajout de `06_doctrine_blocages.md`, renumérotation des documents suivants et mise à jour de l’index documentaire.
- Chauffage UI : corrections de structure YAML et d’indentation sur plusieurs templates `button-card` sans changement fonctionnel.
- Dépôt : normalisation des fins de ligne et harmonisation éditoriale sur plus de 1000 fichiers du patrimoine sans modification de logique métier.

---

## 🧠 ARSENAL HA — v15.8.2 — STABLE — 2026-05-29
**Tags :** chauffage, decision_centrale, autorisation, cascades, diagnostics, ci, contrats

**Signal net :**
- Décision Centrale chauffage : retrait de la branche Niveau 1 `not chauffage_autorise_systeme` de `desired_mode` et `reason` → la raison `chauffage_non_autorise` n'est plus émise ; le cas blocage post-aération émet `blocage_aeration_en_cours`, `desired_mode` restant `reduced`.
- Autorisation système : `binary_sensor.chauffage_autorise_systeme` passe à l'état constant `on`, réservé à la sécurité système sans cause active ; `input_boolean.chauffage_blocage_aeration` reclassé en cause Niveau 2 portée par la Décision Centrale.
- Diagnostics : même retrait de branche Niveau 1 dans `sensor.chauffage_raison_calculee` et `sensor.chauffage_mode_calcule`, cascades réalignées sur la décision.
- CI région décision : `cli_decision` applique R-COV-1 au runtime sans l'axiome `AX-D2` (`A=()`), import `AXIOMES_D2` retiré ; `AX-D2` conservé pour la fixture `d2_reason_pre_correction.yaml` (inchangée) ; snapshot G2 re-figé à `R-COV-1 == 0` ; assertions de `test_lot_2_1` mises à jour (9 branches).
- Contrat `30_decision_centrale.md` : Niveau 1 marqué réservé sans cause active, `chauffage_non_autorise` réservée, renommage de la raison `absence_protection_thermique` en `stabilisation_absence`.

---

## 🧠 ARSENAL HA — [v15.8.3](changelogs/v15/v15_8_3.md) — STABLE — 2026-05-30
**Tags :** chauffage, ui, raisons, source_unique, charte

**Signal net :**
- Source unique `chauffage_registres_raison` (libellé court/long, icône, couleur par raison) ; les cartes synthèse/décision/diagnostic la consomment → fin des traductions d'affichage dupliquées d'une carte à l'autre.
- Éclatement des causes de sécurité affichées : `aeration_en_cours`, `blocage_aeration_en_cours` et `fenetre_ouverte_maison` distinctes ; `confort_suffisant` promue catégorie métier nominale.

---

## 🧠 ARSENAL HA — [v15.8.4](changelogs/v15/v15_8_4.md) — STABLE — 2026-05-30
**Tags :** climatisation, cool, correctif_runtime, ci, observabilite

**Signal net :**
- Correctif critique extinction COOL (D8) : comparateur `>=` → `<=` dans `binary_sensor.clim_seuil_extinction_cool_atteint` → suppression d'un deadlock thermique (front d'extinction jamais atteignable, chemin réel vers OFF rétabli).
- CI dédiée figeant le sens du comparateur d'extinction COOL (gèle `<=`, interdit le retour `>=`).

---

## 🧠 ARSENAL HA — [v15.8.5](changelogs/v15/v15_8_5.md) — STABLE — 2026-05-30
**Tags :** climatisation, cool, application_consigne, idempotence, restart_safe

**Signal net :**
- Automation `cool/application_consigne.yaml` : applique `sensor.consigne_clim_appliquee` à `climate.clim` en mode COOL (entrée mode, changement de consigne, reconvergence post-boot sous `systeme_stable`).
- Envoi idempotent et robuste (pose seulement si cible valide et actuelle inconnue/différente) ; sélection présence/absence portée en amont par la consigne, pas dans l'automation.

---

## 🧠 ARSENAL HA — [v15.8.6](changelogs/v15/v15_8_6.md) — STABLE — 2026-06-01
**Tags :** vacances, chauffage, decision_centrale, effectivite

**Signal net :**
- Passage à l'effectivité Vacances : `binary_sensor.vacances_actives` remplace `input_select.mode_maison = Vacances` dans la Décision Centrale chauffage (ajout du trigger + diagnostics `mode`/`raison`).
- Retrait de la dépendance Vacances dans `sensor.chauffage_autorisation_cible` ; token technique `mode_maison_vacances` conservé.

---

## 🧠 ARSENAL HA — [v15.8.7](changelogs/v15/v15_8_7.md) — STABLE — 2026-06-01
**Tags :** ecs, vacances, desinfection, timer_finished

**Signal net :**
- Désinfection au retour de vacances : helper `input_boolean.ecs_desinfection_retour_due` + automation `ecs/desinfection_retour_pose_due.yaml`, pilotée par l'événement `timer.finished` (remplace la détection sur `timer.vacances_longues_ecs.remaining`).
- `binary_sensor.ecs_desinfection_retour_vacances_autorisee` mis à jour ; autorisation réinitialisée après consommation du cycle ECS.

---

## 🧠 ARSENAL HA — [v15.8.8](changelogs/v15/v15_8_8.md) — STABLE — 2026-06-02
**Tags :** alarme, sirene, desarmement, nettoyage

**Signal net :**
- Alarme : bip de désarmement restreint aux origines `dashboard`/`clavier`/`badge` (en complément de la garde `mode_test off`) ; suppression des automatisations `sirene/bip_desactivation.yaml` et `sirene/stop.yaml` (delay long).
- Mise à jour d'en-tête `intrusion/ouverture/delai_entree_fin.yaml` + ajustements capteurs et dashboards.

---

## 🧠 ARSENAL HA — [v15.8.9](changelogs/v15/v15_8_9.md) — STABLE — 2026-06-03
**Tags :** chauffage, auto_ajustement, observabilite, contrats, audits

**Signal net :**
- Observabilité de l'auto-ajustement de courbe : ajout du contrat `76_observabilite_auto_ajustement_courbe.md`, de la documentation d'architecture associée et du corpus d'audits dédié.

---

## 🧠 ARSENAL HA — [v15.9](changelogs/v15/v15_9_0.md) — STABLE — 2026-06-03
**Tags :** nas_arsenal, release_diff, mqtt, observabilite, etat_run

**Signal net :**
- `release_diff` (NAS Arsenal) : ajout de `state/release_diff_last_run.json`, écrit en fin de chaque run mené à terme (y compris échec contrôlé), schéma défini par `release_diff_mqtt.md` §5.
- Artefact non patrimonial régénéré à chaque run (hors idempotence et hors régénérabilité de `_diff/releases/`) ; champ `produced[]` = couples produits pendant le run.

---

---

## 🧠 ARSENAL HA — [v15.9.1](changelogs/v15/v15_9_1.md) — STABLE — 2026-06-04
**Tags :** documentation, navigation, audits, contrats, lovelace, ci

**Signal net :**
- Documentation Arsenal : ajout de la navigation documentaire, des index d’architecture/contrats, et d’un lot d’audits couvrant documentation, Lovelace, architecture et perception externe.
- Contrats : ajout des README chauffage/climatisation, renvoi ECS vers le contrat canonique Bouclage, correction `script.bouclage_ecs_5_minutes`.
- Lovelace / CI : ajout du contrôle des includes Lovelace, suppression de `carte_mode_toggle.yaml`, mise à jour des README `modes` et `sante`.

---

## 🧠 ARSENAL HA — [v15.9.2](changelogs/v15/v15_9_2.md) — STABLE — 2026-06-06
**Tags :** documentation, lint, contrats, audits, meteo, navigation, ui

**Signal net :**
- Outillage documentaire : ajout du lint documentaire, des contrôles CI docs, du contrôle des liens et des rapports associés.
- Contrats : corrections et renommages documentaires sur chauffage, boiler, météo, pannes secteur, éclairage garage, UI couleurs et socle UI.
- Audits / navigation : ajout de l’audit documentaire global, du plan d’action documentaire et des vagues de correction immédiates ; mise à jour large de l’index des audits et du changelog.

---

## 🧠 ARSENAL HA — [v15.9.3](changelogs/v15/v15_9_3.md) — STABLE — 2026-06-08
**Tags :** contrats, sommeil, couverture_normative, navigation, documentation

**Signal net :**
- CI Sommeil : ajout du workflow `contracts_sommeil.yml` et du checker `check_sommeil_contracts.py`.
- Contrats : ajout des contrats `reveils.md`, `electromenager.md` et `poele.md` ; mise à jour des contrats Santé / Sommeil.
- Couverture normative : ajout du suivi transverse de couverture des domaines et clôture du chantier documentaire du 06/06/2026.

---

## 🧠 ARSENAL HA — [v16.0.0](changelogs/v16/v16_0_0.md) — STABLE — 2026-06-08
**Tags :** documentation, navigation, contrats, ui, ci

**Signal net :**
- Navigation documentaire : ajout de README dans plusieurs dossiers feuilles et ajout de liens internes dans les index Architecture, Contrats, UI et outils externes.
- Contrats : ajout de README de domaine pour alarme, ECS, météo, pannes, santé, publication, ouvertures, éclairage, imprimerie et déshumidificateur ; mise à jour de `contrats/index.md`.
- CI documentation : ajout du contrôle `DOC-CI-6` sur les pages feuilles de navigation et intégration dans `.github/workflows/docs.yml`.

---

## 🧠 ARSENAL HA — [v16.0.1](changelogs/v16/v16_0_1.md) — STABLE — 2026-06-16
**Tags :** panne_secteur, presence, climatisation, aeration, meteo, ecs, chauffage, recorder, documentation

**Signal net :**
- Panne secteur : réécriture de `binary_sensor.coupure_secteur` (état dérivé par OR de `binary_sensor.critere_ups_sur_batterie` et `binary_sensor.bluetti_secteur_present`, source tension rétrogradée en diagnostic) ; ajout du signal `binary_sensor.panne_secteur_en_cours` et de gardes d'inhibition des remédiations.
- Mode panne : confort conditionné par `choose`, ECS de secours via `script.chauffage_ecs_cycle` (désinfection) bornée SOC, ajout d'un trigger de réconciliation et d'une réinitialisation ECS à la sortie.
- Présence : ajout de `binary_sensor.presence_confort_thermique_stabilisee` ; bascule des consommateurs clim COOL depuis `binary_sensor.presence_famille_unifiee`.
- Climatisation : extension de la cascade de `sensor.clim_raison_decision` (causes `blocage_aeration_etage`, `absence_prolongee`, `exterieur_trop_froid`, garde `heat_contexte`) ; ajout des verdicts par mode (`sensor.clim_verdict_cool/dry/heat`) et cartes associées.
- Aération : réordonnancement `co2_priorite` avant `pluie_recente` dans les recommandations étage/rdc/global ; suppression de réglages et tuiles inutilisés.
- Météo / ECS / Chauffage : ajout d'un capteur de tendance température (+ contrat `meteo/tendance_temperature.md`) ; borne max `input_number.ecs_off_desinfection` portée à 4.0 ; cartes thermostatiques en gris indisponibilité sur source `unknown`/`unavailable`.
- HomeKit / Netatmo : ajout de la garde `input_boolean.systeme_stable == on` sur le reboot des stations (`contrats/homekit_diagnostic.md` v1.2).
- Recorder : ajout de `binary_sensor.presence_confort_thermique_stabilisee` et des entités de la chaîne décisionnelle clim ; suppression de `sensor.withings_temperature_du_corps_local`.
- Documentation : ajout des rapports d'audit (climatisation, ECS, Lovelace, pannes), des documents de conception/chantiers climatisation et de la clôture aération ; mise à jour des contrats pannes secteur, climatisation, aération et des hubs de navigation.

---

## 🧠 ARSENAL HA — [v16.0.2](changelogs/v16/v16_0_2.md) — STABLE — 2026-06-17
**Tags :** navigation, lovelace, prises, commandabilite, notifications, climatisation, panne_secteur, documentation, ci

**Signal net :**
- Navigation Lovelace : passage des chemins de vue aux chemins canoniques `/<dashboard-key>` (suppression des suffixes `/home`, `/0`, `/aeration`, `/chauffage`, `/diagnostics-*`, `/reglages-*`), `/reglages-dashboard/maison` → `/reglages-maison-dashboard`, correction des liens de retour (dashboards, diagnostics, réglages, includes) ; ajout du checker `check_lovelace_navigation_contracts.py` et du workflow `contracts_lovelace_navigation.yml` (clés de dashboards, chemins de retour, culs-de-sac, segments de vue non canoniques).
- Prises / Commandabilité UI : ajout du socle `socle_toggle_confirme_indispo` (consommé par `prise_template`) et du template `prise_secteur_template` ; bascule des prises secteur direct vers `prise_secteur_template`, conservation de `prise_template` pour les prises hors gate secteur ; table de topologie des prises commandables dans `infrastructure_puissance.md`, exclusions `switch.prise_box` et `switch.prise_onduleur` documentées.
- Panne secteur : correction documentaire de l'analyse de `sensor.prise_onduleur_voltage` (« prise alimentée en amont de l'UPS » au lieu de « point secouru UPS »), maintenu en diagnostic secondaire non décisionnel ; mise à jour de l'audit `audit_panne_detection_coupure_secteur.md`, du README contrat `pannes/secteur` et des commentaires de `12_template_sensors/system/coupure_secteur.yaml`.
- Notifications : ajout du test T6 dans `check_notifications_contracts.py` (emoji initial obligatoire sur les titres mobiles statiques de `script.notification_envoyer`/`_famille`/`_avance`, exception pour les titres entièrement dynamiques Jinja, `ℹ` ajouté à la regex) ; ajout de `👶` aux titres des notifications babyphone Arnaud et Matthieu.
- Climatisation UI : `carte_clim_etat` lit `sensor.clim_action_en_cours` au lieu du mode HVAC direct, libellés remappés (`cool_actif`/`dry_actif`/`heat_actif`/`bloquee`/`arret`), gris indisponibilité sur `unknown`/`unavailable`/`none`/vide, couleur par mode HVAC conservée, navigation corrigée vers `/clim-dashboard`.
- Architecture / Doctrine : ajout de la doctrine `architecture/03_doctrines/commandabilite.md`, liée depuis `architecture/README.md`, `architecture/03_doctrines/README.md` et `infrastructure_puissance.md`, et ajoutée aux index Architecture et Doctrines.
- Documentation / Changelog : gel de `v16_0_1.md` et ajout de son entrée d'index, déplacement de `prompt_changelog.md` de `outils_externes/` vers `changelog/` (retrait du README `outils_externes` et de la mention des gabarits d'autoring dans `00_documentation_arsenal/README.md`), réécriture de `historique.md` (convention distinguant faits et interprétation), mise à jour de `docs_lint_exceptions.txt` et de l'exemple d'exception dans `docs_lint.py`.

---

## 🧠 ARSENAL HA — [v16.0.3](changelogs/v16/v16_0_3.md) — STABLE — 2026-06-17
**Tags :** chauffage, climatisation, presence, meteo, aeration, deshumidificateur, recorder, contrats, ci, documentation

**Signal net :**
- Chauffage auto-ajustement : ajout de la garde `input_select.chauffage_representativite_thermique == REPRESENTATIF` (bloquante) dans `auto_ajustement.yaml` (`cycle_actionnable`), raison de cycle `non_representatif` ; historisation Recorder des termes de décision (6 entités : représentativité, gate auto, simulation, pente, parallèle, dernier ajustement).
- Météo tendance : ajout des moyennes glissantes courtes 15 min (`sensor.temperature_<axe>_moyenne_15_min`), grandeur de décision passée à `moyenne_15_min − moyenne_60_min`, seuils 0.4/0.2 → 0.15/0.08 ; contrat `tendance_temperature.md` v1.0 → v1.1 (ajout §18 écart contrat/runtime, `INV-TEND-13`/`INV-TEND-14`).
- Climatisation présence : `autorisation/dry.yaml` et `blocages/absence_longue.yaml` rebranchés de `binary_sensor.presence_famille_unifiee` vers `binary_sensor.presence_confort_thermique_stabilisee` (V2).
- Climatisation UI : `carte_clim_etat` n'affiche plus la consigne (`cool_actif` → « Refroidissement »), suppression de la lecture de `sensor.consigne_clim_appliquee`.
- Déshumidificateur : `cave_rh_cible_on`/`cave_rh_cible_off` — ajout de `initial` (78/73) et resserrement des plages (max OFF 74 < min ON 75) ; `guard.md` §12 « helpers à créer » → « implémentés » ; retrait de l'item H1 du backlog hystérésis.
- Aération UI : `carte_delta_ha` lit `seuils_utilises.ha_min_applique` en lecture seule (suppression du fallback saisonnier JS) ; `carte_aeration_intention_globale` gère `unavailable`/`inconnue`.
- Vannes thermostatiques : ajout du contrat `contrats/chauffage/vannes_thermostatiques_plateaux.md`, suppression du stub `contrats/chauffage/15_capteurs/12_capteurs_observabilite_pure.md`.
- Documentation : ajout du registre `audits/REGISTRE_CHANTIERS.md`, du checker `check_registre_chantiers.py` et du workflow `contracts_registre_chantiers.yml` ; gel de `v16_0_2.md` et ajout de son entrée d'index ; ajout de `19_button_card_templates/README.md`.

==================================================
FIN INDEX
==================================================