# ARSENAL — Cartographie des dépendances inter-domaines
## Chauffage — Document transversal de référence (CH-5)

**Statut :** Cartographie de référence — descriptive, non doctrinale
**Rôle :** Recenser les couplages d'entités entre le domaine Chauffage et les autres domaines, dans les deux sens
**Subordonné à :** [`contrats/chauffage/00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)
**Renvoie à (sans redéfinir) :** les contrats d'autorité listés au §6
**Chantier :** CH-5 (dette D8) · **Date :** 2026-05-30
**Périmètre :** dépôt réel à `HEAD = 961f1e6` (post CH-1 → CH-4)

---

## 0. Objet et nature du document

Ce document **cartographie** les dépendances d'entités qui franchissent la frontière du domaine Chauffage. Il existe parce qu'un refactor Chauffage peut casser un consommateur situé dans un autre domaine — ou inversement — sans qu'aucun fichier du domaine ne le signale.

Ce document **n'est pas normatif sur la doctrine**. Il ne décide rien, n'autorise rien, n'interdit rien. La règle métier de chaque couplage reste portée par son **contrat d'autorité** (§6). En cas de divergence entre cette cartographie et un contrat d'autorité, **le contrat d'autorité prime**. En cas de divergence entre cette cartographie et le runtime, **le runtime prime** et la cartographie est à corriger.

Deux directions sont documentées :

- **Direction A** — entités **possédées par le Chauffage**, lues par d'autres domaines (§2).
- **Direction B** — entités **possédées par d'autres domaines**, lues par le Chauffage (§3).

La « possession » d'une entité est déterminée par l'arborescence où elle est **définie** (`unique_id` / déclaration de l'helper), pas par son nom. Plusieurs entités au nom trompeur sont requalifiées en conséquence (§1).

---

## 1. Méthode et limites de l'inventaire

**Méthode.** Extraction par lecture des arbres `05_input_booleans/`, `03_input_numbers/`, `06_input_selects/`, `10_scripts/`, `11_automations/`, `12_template_sensors/`. Propriété établie par localisation de la définition. Couplage retenu = référence effective d'une entité d'un domaine A dans un fichier d'un domaine B.

**Critère d'inclusion (frontière inter-domaines).** Un couplage est listé **uniquement** s'il participe à une **décision**, une **inhibition**, une **action** ou un **diagnostic** chauffage. Les lectures d'infrastructure générique (soleil, horloge, date, helpers de pur affichage sans incidence métier) sont **exclues** par principe.

**Requalifications de propriété notables** (nom trompeur ≠ propriétaire réel) :

- `binary_sensor.bruleur_chauffage_actif`, `binary_sensor.bruleur_mode_chauffage` → **boiler** (définies dans `12_template_sensors/boiler/bruleur/`). Leur lecture par poêle/system est un couplage **boiler↔autres**, hors périmètre de ce document.
- `binary_sensor.meteo_favorable_chauffage` → **météo**.
- `binary_sensor.parametres_invalides_chauffage` → **system** (`integrite_reglages/`).
- `binary_sensor.chauffage_aeration_coherence_ko` → **aération**.
- `sensor.seuil_allumage_chauffage_clim`, `sensor.seuil_extinction_chauffage_clim`, `input_boolean.chauffage_clim_active_en_hiver` → **climatisation** (seuils/mode de la pompe à chaleur en mode chaud) ; lues uniquement en intra-clim → **hors périmètre**.
- `sensor.*_presence_chambres` (inertie/reprise), `binary_sensor.chauffage_inhibition_geofencing_requise`, `binary_sensor.pre_confort_fenetre_valide` → **chauffage** (capteurs internes) → non comptés comme couplage.

**Limites explicites de l'inventaire :**

1. **Couplages textuels sans entité.** Les domaines **ECS**, **bouclage** et **bluetti/énergie** contiennent le mot « chauffage » (commentaires, noms d'automatisations, scripts homonymes) **mais ne lisent aucune entité du domaine Chauffage**, et le Chauffage ne lit aucune de leurs entités. Aucun couplage d'entité réel n'existe à `HEAD`. Ils figuraient dans le périmètre d'arbitrage CH-5 ; le dépôt établit l'absence de couplage. Voir §5.
2. **Appels dynamiques non résolus.** Toute référence construite dynamiquement (`states('...' ~ var)`) échappe à l'extraction statique. Aucune n'a été identifiée sur ce périmètre, mais l'inventaire ne peut le garantir.
3. **Couplages par template Lovelace / button-card.** Les arbres `18_lovelace/` et `19_button_card_templates/` lisent massivement des entités chauffage pour l'affichage. Ces lectures sont **de présentation**, sans incidence sur décision/inhibition/action ; elles sont **exclues** au titre du critère d'inclusion, sauf le diagnostic métier déjà couvert par les contrats UI.
4. **Instantané.** Cet inventaire reflète `HEAD = 961f1e6`. Il n'est lié à aucun invariant CI (décision CH-5 : pas de `R-DEP-x`). Il peut donc dériver et doit être relu à chaque refactor de frontière.

---

## 2. Direction A — entités Chauffage lues par d'autres domaines

### 2.1 Aération

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `input_boolean.chauffage_blocage_aeration` | aération | `10_scripts/aeration/{m0_remediation_incoherence,m2_fin_episode,m4_fin_blocage_horaire}.yaml` · `11_automations/aeration/blocage_chauffage/{guard,pipeline,securite_blocage}.yaml` · `12_template_sensors/aeration/coherence.yaml` | Inhibition partagée : l'aération est productrice de l'état, la décision chauffage en est consommatrice | `aeration_blocage_chauffage/` (V3 PRO) · `chauffage/40_blocages.md` · `chauffage/45_aeration.md` · `chauffage/46_aeration_observation_thermique.md` | **CRITIQUE** |
| chauffage | `input_boolean.blocage_chauffage_aeration_active` | aération | `11_automations/aeration/blocage_chauffage/pipeline.yaml` | État de pipeline du blocage (drapeau d'activité) | `aeration_blocage_chauffage/socle_transversal` | Moyen |

> `chauffage_blocage_aeration` est l'entité la plus couplée du domaine et **celle reclassée par CH-2** (Niveau 1 → Niveau 2). Tout changement de sémantique impacte simultanément l'aération (production) et la climatisation (cf. 2.2). C'est l'angle mort que ce document a vocation à supprimer.

### 2.2 Climatisation

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `input_boolean.chauffage_blocage_aeration` | climatisation | `12_template_sensors/climatisation/{autorisation/heat,blocages/diagnotic,decision/raison}.yaml` | La clim lit le blocage d'aération chauffage comme entrée d'autorisation/diagnostic | `climatisation/04_entrees_metier.md` · `climatisation/06_doctrine_blocages.md` | **CRITIQUE** |
| chauffage | `sensor.temperature_consigne_appliquee_locale` | climatisation | `12_template_sensors/climatisation/seuils_on_off/heat/{on,off}.yaml` | La clim aligne ses seuils on/off mode chaud sur la consigne **appliquée** par le chauffage | `climatisation/05_decision_candidats.md` · `chauffage/30_decision_centrale.md` | **CRITIQUE** |

> Couplage **unidirectionnel** : la clim lit le chauffage ; le chauffage ne lit **aucune** entité clim. Un renommage ou un changement d'unité de `temperature_consigne_appliquee_locale` casse silencieusement le calcul de seuils de la clim.

### 2.3 Poêle

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `input_number.poele_duree_blocage_chauffage_minutes` | poêle | `11_automations/poele/{blocage_chauffage,application_duree_blocage_poele}.yaml` | Paramètre **possédé par le chauffage** mais consommé par la logique poêle (durée de blocage) | `chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md` | Moyen |

### 2.4 Boiler

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `sensor.programme_chauffage` | boiler | `12_template_sensors/boiler/bruleur/{bruleur_actif,mode}.yaml` | Le boiler dérive l'état du brûleur en partie depuis le programme chauffage | `contrats/boiler/socle_transactionnel.md` · `chauffage/90_semantique_thermique.md` | Moyen |

### 2.5 Météo (axes thermiques internes)

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `input_number.chauffage_consigne_confort` | météo | `12_template_sensors/meteo/{meteo_favorable,temperature_maison_moyenne}.yaml` · `12_template_sensors/couleurs/meteo/temperature_moyenne_maison.yaml` | La météo lit la consigne confort comme référence de calcul d'axes thermiques/couleurs | `contrats/meteo/meteo.md` · `chauffage/30_decision_centrale.md` | Faible |
| chauffage | `input_number.chauffage_offset_on` | météo | `12_template_sensors/meteo/temperature_maison_moyenne.yaml` · `12_template_sensors/couleurs/meteo/temperature_moyenne_maison.yaml` | Offset chauffage utilisé dans un calcul météo dérivé | `chauffage/72_offsets_thermiques_lecture_physique.md` | Faible |

### 2.6 System (intégrité, navigation, panne)

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| chauffage | `input_number.chauffage_consigne_confort` · `chauffage_consigne_reduite` · `chauffage_seuil_ext_on` · `chauffage_seuil_ext_off` | system | `12_template_sensors/system/integrite_reglages/chauffage.yaml` | Contrôle d'intégrité des réglages (lecture seule, diagnostic) | `contrats/parametres_invalides.md` · `chauffage/70_autorisation_thermostat.md` | Faible |
| chauffage | `sensor.programme_chauffage` | system | `12_template_sensors/system/cartes_dashboard_navigation/chauffage.yaml` | Navigation/affichage de dashboard (diagnostic) | `contrats/ressources_lovelace.md` | Faible |
| chauffage | `input_boolean.mode_confort_chauffage` | system · panne | `10_scripts/system/coupure_secteur.yaml` · `11_automations/panne/secteur/{activation,desactivation}_mode_panne.yaml` | Le mode confort chauffage est sauvegardé/restauré lors d'une coupure secteur | `contrats/pannes/` · `chauffage/00_gouvernance_chauffage.md` | Moyen |

---

## 3. Direction B — entités d'autres domaines lues par le Chauffage

### 3.1 Boiler — surface transactionnelle (la plus sensible)

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| boiler | `binary_sensor.boiler_bridge_online` | chauffage | `application_consigne.yaml` · `decision_centrale.yaml` · `retry_transactionnel/*` | **Gate d'exécution** : aucune consigne appliquée si le bridge est hors-ligne (gardé G2) | `contrats/boiler/guard_exposition_ha.md` · `chauffage/10_souverainete_execution.md` (+ amendement CH-4) | **CRITIQUE** |
| boiler | `sensor.boiler_heating_setpoint` | chauffage | `12_template_sensors/chauffage/consigne_appliquee.yaml` | Relecture du point de consigne réellement appliqué côté chaudière | `contrats/boiler/socle_transactionnel.md` | **CRITIQUE** |
| boiler | `sensor.boiler_ack_heating_set_temperature_{request_id,status,reason}` | chauffage | `application_consigne.yaml` · `retry_transactionnel/{armement,declenchement,etat,reprise}.yaml` | ACK transactionnel de la commande **température** (corrélation `request_id`, statut, raison) | `contrats/boiler/mqtt_ack_ha.md` · `contrats/boiler/retry_transactionnel.md` | **CRITIQUE** |
| boiler | `sensor.boiler_ack_heating_set_curve_shift_{request_id,status,reason}` | chauffage | `courbe_de_chauffe/{application_parallele,application_pente}.yaml` · `courbe_de_chauffe/correction_demarrage.yaml` · `retry_transactionnel/*` | ACK transactionnel de la commande **décalage de courbe** | `contrats/boiler/mqtt_ack_ha.md` · `contrats/boiler/retry_transactionnel.md` | **CRITIQUE** |
| boiler | `sensor.boiler_ack_heating_set_curve_slope_{request_id,status,reason}` | chauffage | `courbe_de_chauffe/{application_parallele,application_pente,application}.yaml` · `retry_transactionnel/*` | ACK transactionnel de la commande **pente de courbe** | `contrats/boiler/mqtt_ack_ha.md` · `contrats/boiler/retry_transactionnel.md` | **CRITIQUE** |

> Cette surface est **régie intégralement** par les contrats `boiler/`. Ce document la **recense** ; il ne redéfinit ni la corrélation `request_id`, ni les états d'ACK, ni le plafond de tentatives (cf. CH-4, §5 « Hors périmètre »). C'est la surface que la description D8 d'origine (un seul `boiler_bridge_online`) sous-estimait.

### 3.2 Poêle

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| poêle | `input_boolean.blocage_chauffage_poele` | chauffage | `10_scripts/chauffage/decision_centrale.yaml` · `11_automations/chauffage/decision_centrale_trigger.yaml` · `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` | **Inhibition au niveau décision** : le poêle en fonction bloque la chauffe | `chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md` | **CRITIQUE** |
| poêle | `binary_sensor.poele_en_fonction_stable` | chauffage | `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml` | Gate de stabilité avant auto-ajustement de courbe | `chauffage/15_capteurs/03_capteurs_blocages_niveau1/signature_thermique_poele.md` · `chauffage/75_auto_ajustement_courbe.md` | Moyen |

### 3.3 Météo

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| météo | `binary_sensor.meteo_favorable_chauffage` | chauffage | `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml` | Entrée d'autorisation cible selon conditions météo | `contrats/meteo/axe_temperature.md` · `chauffage/70_autorisation_thermostat.md` | Moyen |

### 3.4 Présence

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| présence | `binary_sensor.presence_famille_unifiee` | chauffage | `decision_centrale.yaml` · `decision_centrale_trigger.yaml` | Entrée présence de la décision (régime présent/absent) | `contrats/presence.md` · `chauffage/60_absence_inhibition_geofencing.md` | Moyen |

### 3.5 Ouvertures

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| ouvertures | `binary_sensor.fenetre_ouverte_maison_avec_delai` | chauffage | décision / inhibition fenêtre | Inhibition sur fenêtre ouverte (avec délai) | `contrats/ouvertures/` · `chauffage/40_blocages.md` | Moyen |

### 3.6 Modes maison (mode global, vacances)

| Propriétaire | Entité | Domaine lecteur | Fichier(s) lecteur(s) | Nature | Contrat d'autorité | Risque refactor |
|---|---|---|---|---|---|---|
| modes | `input_select.mode_maison` | chauffage | `decision_centrale.yaml` · `decision_centrale_trigger.yaml` | Mode maison global, entrée d'arbitrage | `contrats/zones.md` · `chauffage/00_gouvernance_chauffage.md` | Moyen |
| modes | `binary_sensor.vacances_actives` | chauffage | décision · pré-confort retour | Bascule régime vacances | `contrats/vacances.md` · `chauffage/65_pre_confort_retour_vacances.md` · `chauffage/66_adaptation_consigne_vacances.md` | Moyen |

---

## 4. Synthèse de criticité

**Couplages CRITIQUES** (chemin de décision ou d'exécution ; une rupture provoque une décision fausse ou une consigne non appliquée) :

1. `input_boolean.chauffage_blocage_aeration` — chauffage → aération + climatisation (Direction A). Point de couplage le plus dense ; entité reclassée par CH-2.
2. Toute la **surface ACK boiler** + `boiler_bridge_online` + `boiler_heating_setpoint` — boiler → chauffage (Direction B). Surface transactionnelle.
3. `input_boolean.blocage_chauffage_poele` — poêle → chauffage, **au niveau décision**.
4. `sensor.temperature_consigne_appliquee_locale` — chauffage → climatisation (pilote les seuils on/off de la clim en mode chaud).

**Couplages MOYENS** (décision/inhibition secondaire ou paramètre partagé) : `poele_en_fonction_stable`, `meteo_favorable_chauffage`, `presence_famille_unifiee`, `vacances_actives`, `mode_maison`, `fenetre_ouverte_maison_avec_delai`, `programme_chauffage`, `mode_confort_chauffage`, `poele_duree_blocage_chauffage_minutes`.

**Couplages FAIBLES** (lecture de configuration ou diagnostic, sans incidence sur la décision) : lectures de consignes/seuils/offsets par météo et par `system/integrite_reglages`, navigation dashboard.

---

## 5. Domaines du périmètre d'arbitrage sans couplage d'entité réel

Le périmètre CH-5 listait **ECS / bouclage** et **bluetti / énergie**. Le dépôt à `HEAD` établit qu'**aucune entité du domaine Chauffage n'est lue par ces domaines, et réciproquement** : les occurrences du mot « chauffage » y sont textuelles (commentaires, noms d'automatisations, scripts homonymes), sans référence d'entité. Ce constat est volontairement consigné : l'absence de couplage est une information de gouvernance au même titre que sa présence. Si un couplage d'entité y apparaît plus tard, ce document doit être mis à jour.

---

## 6. Index des contrats d'autorité référencés

Ce document **renvoie** à ces contrats et n'en duplique aucune règle :

- **Aération ↔ chauffage :** `contrats/aeration_blocage_chauffage/` · `chauffage/40_blocages.md` · `45_aeration.md` · `46_aeration_observation_thermique.md`
- **Boiler (transactionnel) :** `contrats/boiler/{socle_transactionnel,retry_transactionnel,mqtt_ack_ha,guard_exposition_ha,consommation_ack,script_executif}.md` · `chauffage/10_souverainete_execution.md` (+ amendement CH-4)
- **Poêle :** `chauffage/15_capteurs/03_capteurs_blocages_niveau1/{poele_en_fonction,signature_thermique_poele}.md` · `chauffage/75_auto_ajustement_courbe.md`
- **Climatisation :** `contrats/climatisation/{04_entrees_metier,05_decision_candidats,06_doctrine_blocages}.md`
- **Météo :** `contrats/meteo/{meteo,axe_temperature}.md`
- **Présence / géofencing :** `contrats/presence.md` · `chauffage/60_absence_inhibition_geofencing.md`
- **Modes / vacances / zones :** `contrats/{vacances,zones}.md` · `chauffage/{65_pre_confort_retour_vacances,66_adaptation_consigne_vacances}.md`
- **Ouvertures :** `contrats/ouvertures/`
- **Réglages / intégrité :** `contrats/parametres_invalides.md` · `chauffage/{30_decision_centrale,70_autorisation_thermostat,72_offsets_thermiques_lecture_physique}.md`
- **Pannes :** `contrats/pannes/`

---

## 7. Ce que ce document n'est pas

- ❌ une doctrine globale de tous les domaines (il est ancré au domaine Chauffage et renvoie au reste) ;
- ❌ une source de vérité métier sur un couplage (le contrat d'autorité l'est) ;
- ❌ un invariant CI (décision CH-5 : pas de `R-DEP-x` ; liaison CI différée) ;
- ❌ un inventaire exhaustif de toutes les lectures Home Assistant (les lectures d'affichage et d'infrastructure générique sont exclues) ;
- ❌ un instantané auto-actualisé (il reflète `HEAD = 961f1e6` et doit être relu à chaque refactor de frontière).

**Phrase de synthèse.** Le domaine Chauffage est couplé en lecture à l'aération, la climatisation, le poêle, le boiler, la météo, la présence, les ouvertures et les modes maison ; ses quatre couplages critiques sont le blocage d'aération partagé, la surface transactionnelle boiler, le blocage poêle au niveau décision, et la consigne appliquée lue par la climatisation.
