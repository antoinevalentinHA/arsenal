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

### Points de vigilance (sans dramatiser, mais réels)
- **Rupture de chargement** si un include/chemin canonique manque : c’est une transition “socle”, pas une feature isolée.
- **Retrait `scene:`** : si des scènes étaient “réellement” consommées, elles sortent de ce chemin (attention aux dépendances historiques).
- **UI navigation (paths)** : dépendance à des chemins stables (`/dashboard-accueil/0`, `/dashboard-navigation/0`) → liens morts si renommage ultérieur.
- **Zigbee2MQTT** : réordonnancement devices OK, mais **perte** d’un `friendly_name` = casse identitaire en cascade.
- **Cohérence métriques** : autonomie Audi (libellé vs variable) → risque de confusion lecture/diagnostic.

### Bruit identifié
- Suppression de logs Zigbee2MQTT : bruit d’artefacts
- Styles UI (padding/arrondis/couleurs) quand ça n’emporte pas un pattern de navigation

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

**Vigilances :**
- Effet domino “timers + scripts”
- ViCare : dépendance attributs attendus (`active_vicare_program`)
- Pluie : bascule “mesure → état” (`input_boolean.pluie_en_cours`)
- Recorder/Logbook : exclusions larges possibles
- UI/palette : dette potentielle (cosmétique mais doctrine à tenir)

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

==================================================
FIN INDEX
==================================================
