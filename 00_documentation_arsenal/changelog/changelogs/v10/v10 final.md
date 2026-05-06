# Arsenal — Changelog v10 final

## Résumé

Version finale de consolidation de l'architecture v10.

Cette version marque la transformation complète d'Arsenal en un système :

- **contractuel** : la documentation devient normative et structurante
- **déterministe** : validation, fallback et TTL sont explicitement définis
- **boot-safe** : toutes les couches reconvergent automatiquement après redémarrage
- **découplé** : séparation stricte entre capteurs physiques et vérités métier

Aucune logique métier centrale n'est modifiée, mais le système devient
**prévisible, auditable et résilient par construction**.

Cette version constitue le socle final avant v11.

---

## Axes structurants de la version

### 1. Documentation devient architecture

Les contrats ne décrivent plus le système : ils le définissent.
Toute implémentation YAML est désormais une projection directe des contrats.
Les documents passent d'un rôle de référence à un rôle prescriptif.

### 2. Passage à un modèle déterministe

Les capteurs suivent désormais un modèle strict à quatre niveaux :

1. validation (numérique + plage physique)
2. fallback multi-source
3. mémoire conditionnée (TTL 30 min)
4. abstention explicite

Aucun état ne persiste indéfiniment sans justification contractuelle.

### 3. Système boot-safe

Toutes les couches critiques intègrent un trigger `homeassistant.start`,
des délais de stabilisation, et la garde `input_boolean.systeme_stable`.
Le système reconverge automatiquement après chaque redémarrage.

### 4. Découplage physique / métier

Les automatisations ne consomment plus les capteurs physiques directement.
Elles s'appuient sur des signaux métier — plus stables, plus lisibles,
plus auditables. Exemple : l'alarme consomme `alarme_ouverture_entree`
et non plus `contact_entree_porte`.

### 5. Remplacement des heuristiques par la mesure directe

Certaines logiques abstraites sont remplacées par des mesures physiques
disponibles. Exemple : l'autorisation d'éclairage garage repose désormais
sur la luminosité réelle (`sensor.luminosite_garage_illuminance`) plutôt
que sur une inférence saison/période-météo — rendue possible par
l'intégration d'un nouveau capteur Zigbee.

### 6. Promotion du corpus Viessmann au rang d'architecture cible

Les 16 documents de décision ADR Viessmann local quittent
`evolutions_futures/` pour intégrer `architecture/`. Les décisions
sont actées — le corpus est désormais une référence normative active,
non un chantier en attente.

---

## 1. Documentation — Restructuration normative

### 1.1 Réorganisation des contrats

Les contrats monolithiques ont été éclatés en sous-dossiers thématiques :

- `contrats/eclairage_jardin.md` → `contrats/eclairage/jardin.md`
- `contrats/ouvertures.md` → `contrats/ouvertures/global.md`
- `contrats/ouvertures_redondance.md` → `contrats/ouvertures/redondance.md`
- `contrats/panne_internet.md` → `contrats/pannes/internet.md`
- `contrats/panne_secteur.md` → `contrats/pannes/secteur.md`
- `contrats/climatisation.md` (monolithe) → `contrats/climatisation/` (11 fichiers)
- `contrats/meteo.md` + `meteo_affichage.md` → `contrats/meteo/` (7 fichiers)
- `contrats/eclairage_garage.md` → `contrats/eclairage/garage.md`

Nouveaux contrats créés :
- `contrats/alarme/51_ouvrants_entree_alarme.md`
- `contrats/ouvertures/alarme.md`
- `contrats/homekit_diagnostic.md`

### 1.2 Promotion du corpus Viessmann local

L'intégralité de `evolutions_futures/viessmann_local/` (16 fichiers ADR)
est promue dans `architecture/viessmann_local/`. Ajout de deux documents :
`migration_vicare_vers_local.md` et `plan_migration.md`.

### 1.3 Nouveau contrat climatisation (éclaté)

Création de `contrats/climatisation/` en 11 sections : finalité, architecture,
décision canonique, entrées métier, candidats, arbitrage, exécution, sécurité,
observabilité, périmètre exclu, index.

### 1.4 Nouveaux contrats météo

Création de `contrats/meteo/` : contrat_meteo, contrat_axe_temperature,
contrat_axe_temperature_exterieure, contrat_validation, contrat_fallback,
affichage, gouvernance. Ces contrats formalisent le modèle
validation + plage + TTL désormais appliqué dans le YAML.

### 1.5 Documentation UI couleurs

Nouveau dossier `00_documentation_arsenal/ui/couleurs/` (6 fichiers) :
principes, palette, exceptions, typographie, règles.

### 1.6 Refonte `socle_ui/07_status.md`

Réécriture dans un format normatif structuré : tableaux
`show_icon/show_name/show_state/show_label`, actions, métriques-clés.
Les 9 variantes `socle_status_*` documentent désormais leur héritage,
leurs particularités contractuelles et leurs interdits explicites.
`socle_ui/00_synthese.md` mis à jour en conséquence.

### 1.7 Fichier de dette technique et pré-changelog v11

Création de `evolutions_futures/dette_technique_post_boot.md`.
Création de `changelog/changelogs/v11/v11_pre.md`.

---

## 2. Couche observation — Template sensors

### 2.1 Températures consolidées intérieures — modèle déterministe

Application du contrat `contrat_fallback.md` v2 avec TTL sur
mémoire de continuité :

- Trigger `time_pattern: minutes: "/5"` ajouté (requis pour expiration
  effective du TTL)
- Validation étendue : plage contractuelle 8..40 °C
- Niveau 3 (mémoire) conditionné à `age ≤ 1800 s` via `this.last_updated`
- Au-delà du TTL : abstention (`none`) — aucune persistance infinie
- Ancre YAML renommée : `temperature_consolidee_logic` → `temperature_consolidee`

### 2.2 Température jardin — contrat extérieur v2.0

Application de `contrat_axe_temperature_exterieure.md` :

- Sources consolidation : `jardin_1` + `jardin_2`, règle `min()`
- `jardin_3` (SwitchBot) : source observation seule, exclue de la
  consolidation, conservée en attribut `capteurs_observation`
- Plage : -10..50 °C
- Trigger `time_pattern` ajouté, TTL 30 min identique
- Attributs enrichis : `sources_consolidation`, `capteurs_observation`,
  valeurs brutes des 3 sources

### 2.3 Autorisation éclairage garage — pivot vers luminosité physique

`binary_sensor.garage_allumage_auto_autorise` :

- Abandon de la logique saison/période-météo
- Entrée : `sensor.luminosite_garage_illuminance`
- Seuil : `input_number.garage_seuil_luminosite_allumage_auto` (réglable UI)
- Logique : `lux < seuil` → `on`
- Availability conditionnée aux deux entités
- Suppression de toute dépendance à `input_select.saison`
  et `sensor.periode_meteo`

### 2.4 Nouveau capteur Zigbee luminosité garage

Intégration de `sensor.luminosite_garage` :
- `01_customize/batteries.yaml` : ajout friendly_name + icône
- `02_groups/batteries.yaml` + `zigbee_lqi.yaml` : intégré dans les groupes
- `03_input_numbers/eclairage/seuil_luminosite_garage.yaml` : nouveau
  `input_number`

### 2.5 Nouveaux capteurs boiler (migration Viessmann local)

- `12_template_sensors/boiler/boiler_bridge_degraded.yaml`
  (remplace `vicare/boiler_bridge_degraded.yaml`)
- `12_template_sensors/boiler/boiler_command_feedback.yaml`
- Ajout d'un sensor dans `14_mqtt_sensors/`

### 2.6 Capteur alarme ouvrants entrée

`12_template_sensors/alarme/ouvrants_entree.yaml` — signal métier dédié
au domaine alarme, consommé par l'automation `delai_entree_start`.

### 2.7 Diagnostic Netatmo — preuves de vie multi-sources

`sensor.diagnostic_netatmo_arnaud` et `diagnostic_netatmo_matthieu` :

- Preuve unique (température jardin) remplacée par un ensemble
  multi-sources : températures, humidités, CO₂, bruit de toutes les
  zones associées à chaque station
- Le ping réseau n'intervient qu'en dernier recours
- Contrainte : seuls les capteurs à état numérique continu sont admis

### 2.8 Seuils clim — trigger post-boot

Ajout de `homeassistant: start` sur `seuil_allumage_clim_applique`
et `seuil_extinction_clim_applique`.

### 2.9 Correction axe humidex clim

`clim_raison_decision` : remplacement de
`binary_sensor.clim_humidex_sup_cible_dry` par
`binary_sensor.chambre_max_humidex_au_dessus_seuil`
(alignement sur le nom contractuel de l'entité).

---

## 3. Automatisations

### 3.1 Alarme — délai entrée : pivot vers signaux métier

`10020000000031 — Alarme - Délai entrée (start)` :

- Trigger migré vers `binary_sensor.alarme_ouverture_entree`
  et `alarme_ouverture_garage` (couche métier, non réconciliation ouvrants)
- Contrainte `from: "off"` ajoutée (front montant strict)
- En-tête refondu au format normatif Arsenal (📥 Entrées / 📤 Sorties)

### 3.2 Climatisation — couverture post-boot

Trigger `homeassistant: start` + delay `00:00:05` ajoutés sur :
- `climatisation/modes.yaml`
- `climatisation/cool/start_timer_absence.yaml`

Trigger `homeassistant: start` + condition `systeme_stable: on` ajoutés sur :
- `climatisation/guard.yaml`

### 3.3 Suppression de `input_boolean.aeration_preferable`

- `05_input_booleans/climatisation/aeration_preferable.yaml` supprimé
- Références à `input_boolean.clim_ignore_aeration` supprimées dans
  les dashboards aération et climatisation

---

## 4. Interface Lovelace

### 4.1 Dashboard éclairage — contrôle luminosité garage

Ajout de la tuile `input_number.garage_seuil_luminosite_allumage_auto`.

### 4.2 Nettoyage dashboards climatisation et aération

- Bloc « Blocage Aération / Ignorer aération préférée » supprimé
  du dashboard climatisation
- Dashboard aération : section « Options » → « Notifications »,
  entrée `clim_ignore_aeration` supprimée

---

## Fichiers supprimés

- `05_input_booleans/climatisation/aeration_preferable.yaml`
- `12_template_sensors/vicare/boiler_bridge_degraded.yaml`
- `00_documentation_arsenal/contrats/climatisation.md`
- `00_documentation_arsenal/contrats/meteo.md` + `meteo_affichage.md`
- `00_documentation_arsenal/evolutions_futures/viessmann_local.md`
- `00_documentation_arsenal/ui/couleurs.md`
- `00_documentation_arsenal/outils_externes/chat_gpt/` (purge complète)
- `00_documentation_arsenal/outils_externes/gemini/reglages_chauffage.md`