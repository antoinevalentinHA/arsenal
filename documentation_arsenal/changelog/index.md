==================================================
🧠 ARSENAL — CHANGELOG / INDEX (canon)
Fichier : documentation_arsenal/changelog/INDEX.md
==================================================

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
  - `alarm_control_panel/` → `template_alarm_panels/`
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
- Transition d’ère : doctrine documentée (`documentation_arsenal/`) + UI industrialisée (templates segmentés).
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
- **Assainissement d’arborescence capteurs** (extinction `12_template_binary_sensors`, 40+ moves vers `12_sensor_platforms`, includes nettoyés).
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

## 🧠 ARSENAL HA — v10 — STABLE — 2026-03-XX
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

## 🧠 ARSENAL HA — v10 — STABLE — 2026-03-XX
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

==================================================
FIN INDEX
==================================================