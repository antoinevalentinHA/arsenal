==================================================
🧠 ARSENAL — HISTORIQUE TRANSVERSAL DES ÉVOLUTIONS (2025→2026)
==================================================

Ce document décrit **l’évolution du système ARSENAL dans le temps** (lecture “signal”), en reliant :
- **doctrine / gouvernance**
- **architecture décision / action / UI**
- **domaines fonctionnels** (Chauffage, ECS, Clim, Réseau/Zigbee, Sécurité, UI, Docs, Observabilité)

📌 Source temporelle utilisée : **tes jalons datés** (Europe/Paris).
📌 Quand un changelog interne porte une autre date, on le considère comme **date documentaire**, pas comme jalon.

---

# 0) Timeline — jalons & inflexions (vue synthétique)

| Date / heure | Jalon | Signal dominant (résumé 1 ligne) |
|---|---|---|
| 31/08/2025 21:42 | 2025-08 Final  | Base antérieure (pré-Arsenal) — jalon de fin (contenu non détaillé ici). |
| 20/09/2025 22:57 | 20250920 Final | Stabilisation pré-Arsenal (contenu non détaillé ici). |
| 10/10/2025 13:51 | 20251010 Final | Dernier jalon “pré-Arsenal” (contenu non détaillé ici). |
| 01/12/2025 15:37 | Arsenal v1     | Naissance Arsenal (fondations — contenu non détaillé ici). |
| 02/12/2025 11:16 | Arsenal v2     | Consolidation initiale (contenu non détaillé ici). |
| 06/12/2025 16:57 | Arsenal v3     | Structuration initiale (contenu non détaillé ici). |
| 17/12/2025 18:31 | Arsenal v4     | Montée en gouvernance (contenu non détaillé ici). |
| 22/12/2025 18:19 | Arsenal v5     | Stabilisation avant série v6 (contenu non détaillé ici). |
| 05/01/2026 12:38 | Arsenal v6     | Pivot v6 (préambule à v6.4/v6.5). |
| 08/01/2026 xx:xx | v6.4           | Stabilisation architecturale majeure : normalisation en-têtes + robustesse reboot-safe. |
| 09/01/2026 xx:xx | v6.5           | Consolidation Chauffage V3 PRO + Clim silencieux + Vacances/ECS/robustesse reload. |
| 11/01/2026 21:33 | Arsenal v7     | Transition d’ère : doctrine documentée + UI industrialisée + énergie verrouillée. |
| 14/01/2026 10:19 | v7.2           | Chauffage : intention **Neutre** (abstention) + taxonomie UI complétée + débruitage observabilité. |
| 15/01/2026 10:32 | v7.3           | ECS : **signal fin de cycle + ACK** ; Chauffage : verrou présence via autorisation cible ; diagnostics/UI renforcés. |
| 16/01/2026 09:13 | v7.3.3         | Panne secteur : fin des pilotages chauffage hors décision centrale ; sémantique UI corrigée (standby/attente/repos). |
| 19/01/2026 22:42 | v8.0.0         | Réforme transverse **Notifications** + MCO Batteries + métriques mobilité + durcissement UI Chauffage. |
| 20/01/2026 21:00 | v8.1.0         | Chauffage post-cloud : souveraineté d’exécution + anti-yo-yo ; auto-ajustement courbe propositionnel ; ECS bouclage auto. |
| 23/01/2026 16:03 | v8.1.1         | Chauffage 100% événementiel + observabilité inertielle A/B/C/D ; migration “vicare → domaines” + gouvernance IDs. |
| 25/01/2026 09:40 | v8.2           | “Silence utile” : Overkiz silencieux ; stats long-terme températures ; hiver idempotent ; bouclage AUTO/MANUEL corrigé ; includes navigation UI. |
| 27/01/2026 11:10 | v8.2.1         | Durcissement multi-domaines : cohérence ViCare/decision, Zigbee canal 25, aération durable, Z2M résilience, garage toggle fiable. |
| 27/01/2026 15:38 | v8.2.2         | Durcissement ciblé : Présence (latence réduite), LQI source unique, géofencing hystérésis qualifiée, Overkiz cadence réduite. |
| 27/01/2026 23:20 | v8.3.0         | Consignes Chauffage : **HA maître / ViCare esclave** ; Wi-Fi BSSID “signal métier” ; doc architecture structurante. |
| 28/01/2026 19:05 | v8.3.1         | Clim : pipeline canonique (target_mode + execution + watchdog) ; UI Min/Max ; hygiène ressources ; ScanWatch local. |
| 04/02/2026 22:17 | v8.3.2         | Templates : **factorisation par ancres YAML** ; Modes maison recentrés sur ECS ; déparasitage effets de bord. |
| 08/02/2026 12:03 | v9.0.0         | Extinction complète legacy templates ; assainissement arborescences ; modernisation loader Lovelace ; UI Chauffage rebuild fiable. |
| 08/02/2026 23:38 | v9.0.1         | Consolidation doctrinale : **override opérateur souverain (N0)** ; UI Chauffage “observable only” ; ECS au niveau constitutionnel (corpus). |

---

# 1) Grandes phases (lecture “évolution” plutôt que “versions”)

## Phase A — Pré-Arsenal (2025-08 → 20251010)
**Objectif global présumé :** stabiliser une base HA avant institution Arsenal.  
**Données disponibles dans cet échange :** jalons temporels uniquement (pas de contenu).  
➡️ Cette phase est conservée comme **repère historique** (pas d’analyse doctrinale possible ici).

## Phase B — Arsenal v1 → v5 (01/12/2025 → 22/12/2025)
**Objectif global :** naissance Arsenal, premières règles, montée en structuration.  
**Données disponibles ici :** jalons temporels uniquement.  
➡️ À compléter si tu fournis 1 digest par version (même 5 lignes).

## Phase C — Série v6 (05/01/2026 → 09/01/2026) : lisibilité + reboot-safe comme socle
### v6.4 (08/01)
- **Normalisation totale des en-têtes** (helpers) : rôle / non-rôle explicite, séparation paramètre/mémoire/planification/décision/action.
- **Hygiène structurelle** : suppression orphelins, alignement doc↔code↔entités.
- **Scripts** : clarification responsabilité (unitaire/orchestration/décision).
- **Réseau** : script bas niveau unique `script.cycle_alimentation_box` (une seule vérité physique).
- **Éclairage jardin** : passage au modèle **état métier continu** + automations réactionnelles reboot-safe.
- **Alarme** : mode visiteur sans polling via `binary_sensor.creneau_visiteur_actif`.
- **Vacances** : état métier opportuniste via `binary_sensor.vacances_actives`.

### v6.5 (09/01)
- **Chauffage V3 PRO** : présence reléguée, Eco imposé en contextes bloquants ; justification canonique (fin des raisons trompeuses).
- **Clim silencieux** : décision portée par `binary_sensor.clim_silencieux_autorise`, exécution événementielle, mode `queued`.
- **Éclairage jardin** : consolidation matin/soir, mémoire métier matin (`input_boolean.jardin_eclairage_matin_actif`) pour anti-spam.
- **Vacances** : décision + raison + UI dédiées (lecture seule).
- **Robustesse reload YAML** : fin des `condition: state` fragiles, templates tolérants.

➡️ **Inflexion de phase (v6.x) :** “on verrouille les couches (doc/structure) avant d’ajouter”.

## Phase D — Arsenal v7 (11/01/2026 → mi-janvier) : doctrine opposable + UI industrialisée
### v7.0 (transition d’ère)
- **Documentation canonique** : pivot vers `documentation_arsenal/` (doctrine opposable).
- **Énergie** : verrouillage sources monotones, interdiction capteurs instables en source dashboard Énergie.
- **UI** : industrialisation par bibliothèque de templates segmentée ; dashboards déclaratifs (UI ne décide jamais).
- **Temps** : timers structurants (temps = objet gouverné).
- **Éclairage jardin / ECS vacances / réseau reboot** : patterns métier consolidés.

### v7.1 (clarification sémantique)
- VMC : séparation stricte aération vs VMC ; diagnostic relocalisé.
- Chauffage : distinction “attente confort” vs “attente protection” ; UI alignée sans toucher au moteur.

### v7.2 (intention **Neutre**)
- Chauffage : **Neutre = autorisé sans action** (abstention volontaire), fin des décisions implicites de présence.
- UI : complétion taxonomie templates génériques.
- Observabilité : débruitage (logbook/system log) + refactor docs UI/outils.

### v7.3 → v7.3.5 (durcissements Chauffage/ECS/UI)
- **ECS** : fin de cycle = **signal explicite + ACK** (`ecs_fin_cycle_signal`) ; production/consommation séparées.
- Chauffage : présence = autorisation, pas raccourci ; alignements diagnostics/UI.
- Géofencing absence : hystérésis qualifiée + réduction bruit triggers décision centrale.
- Paramètres invalides : garde-fous systémiques (capteurs + groupe + alerte UI).
- UI Chauffage : correction attente/repos/standby/bloquages ; dashboard diagnostics resserré.
- Vannes thermostatiques : dashboard diagnostic séparé (lecture seule).

➡️ **Inflexion de phase (v7.x) :** passage d’un “système qui marche” à un “système gouverné, lisible, opposable”.

## Phase E — Série v8 (19/01/2026 → 04/02/2026) : souveraineté + silence utile + durcissement infra
### v8.0.0 (réforme Notifications + MCO)
- **Notifications** : persistantes = projection d’état “en cours/dégradé” uniquement ; plus de persistantes de succès.
- **Batteries** : gouvernance via `group.batteries`, script unique, verrou journalier.
- Mobilité : `utility_meter` distance.
- Chauffage UI : enrichissements et robustesse.

### v8.1.0 / v8.1.1 (post-cloud Chauffage + événementiel total)
- Chauffage : anti-yo-yo (`chauffage_application_en_cours`) ; mémoire “confirmée cloud”.
- Réalignement dédié ViCare↔HA + `dernier_mode_applique` (puis supprimé plus tard).
- Auto-ajustement courbe : propositionnel, souveraineté humaine, journalisé.
- Pré-confort fin vacances : signal métier + automation bornée.
- ECS : bouclage auto gouverné (plage + présence).
- v8.1.1 : décision centrale **100% événementielle** (fin polling) + observabilité inertielle A/B/C/D ; migration “vicare → domaines” + refonte IDs.

### v8.2 / v8.2.1 / v8.2.2 (silence utile + Zigbee + qualification capteurs)
- Overkiz : résilience silencieuse, cadence réduite ensuite (/2h).
- Chauffage : fiabilisation B0, stats long-terme températures, Famille C absence contractualisée.
- ECS bouclage : arbitrage AUTO/MANUEL corrigé via `binary_sensor.bouclage_autorise`.
- UI : factorisation navigation via `lovelace/includes/navigation/`.
- Zigbee : migration canal 11→25 + reconstruction maillage ; LQI : groupe source unique + capteur redevenu vérifiable.
- Aération : abandon push mobile pour états durables ; persistantes zonées.
- Zigbee2MQTT : backoff réel + notification persistante recentrée.
- Présence : temporisations drastiquement réduites, tout en interdisant l’usage comme déclencheur d’écriture directe.

➡️ **Inflexion de phase (v8.x) :** “le système devient sobre : bruit réduit, sources uniques, résilience outillée”.

## Phase F — Série v8.3 (27/01/2026 → 04/02/2026) : souveraineté HA, factorisation templates, pipeline clim
### v8.3.0
- Chauffage consignes : **HA maître absolu / ViCare esclave passif** (monodirection HA→ViCare).
- Alarme/Wi-Fi : apprentissage BSSID piloté par **signal métier** (capteur → action → mémoire).
- UI : include alerte intégrité paramètres factorisée.
- Documentation : corpus architecture structurant (socle).

### v8.3.1
- Clim : refonte canonique (autorité `sensor.clim_target_mode`, exécution idempotente `script.clim_execution`, watchdog + incohérence).
- UI : dashboard Températures Min/Max (pattern Arsenal) + hygiène ressources Lovelace (suppression composants non utilisés).
- Santé : capteur local ScanWatch batterie + notification factuelle.

### v8.3.2
- Templates : factorisation par **ancres YAML** + `this.entity_id` (réduction duplication).
- Modes maison : recentrage Vacances/Normal/Désinfection sur périmètre ECS, suppression actions annexes.

➡️ **Inflexion (v8.3.x) :** “souveraineté HA + industrialisation interne (factorisation) + pipelines canoniques”.

---

# 2) Série v9 (08/02/2026) : modernisation totale templates + doctrine Chauffage/UI/ECS

## v9.0.0
- Extinction complète **legacy templates** (`platform: template`) → `template:` moderne.
- Assainissement arborescences capteurs / bascule `12_sensor_platforms`.
- Modernisation loader Lovelace (`resource_mode: yaml`).
- UI Chauffage : fin des persistantes gérées dans le script ; reconstruction fiable via automation dédiée.

## v9.0.1 (doctrine)
- Chauffage : `mode_confort_chauffage` devient **override opérateur souverain (N0)**, prioritaire, bypass contrôlé d’abstentions.
- Diagnostics : `confort_force` au sommet ; capteurs deviennent miroir contractuel strict.
- UI Chauffage : “observable only” — persistante **Confort uniquement**, source **exclusive** `sensor.programme_chauffage`.
- ECS : passage au niveau constitutionnel documentaire (corpus normatif spécialisé, contrat monolithique déclassé).

➡️ **Inflexion v9 :** “modernisation technique totale + clarification politique : qui est souverain, et que l’UI a le droit de dire”.

---

# 3) Matrice transversale (où se déplacent les responsabilités)

## A) Autorité / décision / exécution
- v6.x : clarification & séparation (en-têtes + scripts).
- v7.x : doctrine opposable + UI industrialisée (UI non décisionnelle).
- v8.x : souveraineté d’exécution post-cloud (anti-yo-yo, réalignements, événementiel).
- v8.3 : HA maître (consignes), ViCare canal non fiable.
- v9.0.1 : souveraineté opérateur explicitée (N0 override).

## B) UI (projection)
- v7.0 : UI = consommation, templates segmentés par domaine.
- v7.2 : taxonomie UI consolidée.
- v8.2 : includes navigation (structure factorisée).
- v9.0.0 : persistantes Chauffage découplées des scripts.
- v9.0.1 : projection “observable only” pour Chauffage (programme réel).

## C) Observabilité
- v7.3 : ECS fin de cycle = événement consommable (ACK).
- v8.1.1 : observabilité inertielle A/B/C/D (descriptive, sans seuils métier).
- v8.2 : stats natives long-terme température.
- v7.2–v8.2 : débruitage (silence utile) + suppression diagnostics journaliers lourds.

## D) Réseau/Zigbee
- v6.4 : reboot box centralisé (script bas niveau unique).
- v8.2.1–v8.2.2 : migration Zigbee canal 25 + LQI vérifiable via groupe source unique.
- v8.2.1 : résilience Zigbee2MQTT (backoff, notification durable).

## E) Documentation / gouvernance
- v7.0 : naissance `documentation_arsenal/` (doctrine opposable).
- v8.x : extension “outils externes” + prompts/guides.
- v8.1.1 : découpage contrats Chauffage.
- v9.0.1 : ECS “constitutionnel” (corpus spécialisé + changelog).

==================================================
FIN DU DOCUMENT
==================================================
