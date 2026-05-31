# 🚗 ARSENAL — RAPPORT D'AUDIT — DOMAINE AUDI (« Voiture — Audi A3 e-tron »)

> Audit réalisé sur le dépôt `github.com/antoinevalentinHA/arsenal`, HEAD `92a8ff7` (release v15.8.5, 2026-05-31).
> Méthode : priorité au runtime, puis contrats, puis documentation, puis dashboards. Toute affirmation est tracée à un fichier.

## ⚠️ Limite épistémique préalable (à lire avant tout)

L'audit porte sur le **dépôt** (la configuration qui *génère* le runtime), pas sur le runtime live. Or plusieurs constats dépendent de l'`entity_registry` réel de Home Assistant, que le dépôt ne contient pas (`git ls-files | grep entity_registry` → vide).

Point technique central : pour un template sensor portant à la fois `name:` et `unique_id:`, l'**`entity_id` par défaut dérive du `name` slugifié**, pas du `unique_id` (qui n'est que la clé de registre). Tout le domaine repose sur cette mécanique. Les constats AUDI-01, AUDI-02, AUDI-09 et AUDI-10 ne peuvent être **tranchés définitivement** qu'en inspectant le registre d'entités live. Le dépôt permet de les **identifier** et d'en **qualifier le risque**, ce que fait ce rapport.

---

## 1. Cartographie du domaine

Le domaine est désigné **`voiture`** dans l'arborescence (le mot « Audi » apparaît dans les noms d'entités et le contrat). Il s'étend sur les couches suivantes :

### Fichiers

| Couche | Fichier | Rôle |
|---|---|---|
| Contrat | `00_documentation_arsenal/contrats/voiture.md` | Contrat normatif du domaine |
| Helpers | `03_input_numbers/voiture/autonomie.yaml` | 3 `input_number` snapshots |
| Helpers | `04_input_texts/voiture/autonomie.yaml` | 1 `input_text` historique |
| Capteurs locaux | `12_template_sensors/voiture/batterie/{autonomie,etat_charge,pourcentage}.yaml` | 3 trigger sensors stabilisés |
| Capteurs locaux | `12_template_sensors/voiture/{kilometrage,derniere_maj,stationnement}.yaml` | 3 trigger sensors |
| Capteurs locaux | `12_template_sensors/voiture/revision/{distance,temps}.yaml` | 2 trigger sensors |
| Capteurs locaux | `12_template_sensors/voiture/ouvertures/**` | ~13 trigger **binary_sensors** (portes, fenêtres, coffre, toit) |
| Exposition | `12_template_sensors/voiture/batterie/snapshots_pleine_charge.yaml` | 2 sensors miroirs |
| Statistiques | `13_sensor_platforms/statistics/voiture/{autonomie,temperature_charge}.yaml` | 2 `platform: statistics` |
| Compteurs | `utility_meter.yaml` (l. 256-272) | distance mensuelle/annuelle |
| Automatisations | `11_automations/voiture/{autonomie,archive,notification_etat_charge}.yaml` | 3 automatisations |
| Automatisations | `11_automations/voiture/archive.yaml` (note) | un 4ᵉ fichier `archive.yaml` ≠ automation `archive` du contrat — voir §4 |
| Navigation UI | `12_template_sensors/system/cartes_dashboard_navigation/voiture.yaml` | `sensor.etat_voiture_dashboard` |
| Dashboards | `18_lovelace/dashboards/voiture/{audi,audi_batterie,audi_securite}.yaml` | 3 vues |
| Persistance | `recorder.yaml` (l. 405-420, section « 🚗 AUTOMOBILE ») | inclusions recorder |
| CI / Garde | `scripts/arsenal_contracts/check_voiture_contracts.py` + `.github/workflows/contracts_voiture.yml` | checker contractuel |
| Intégration tierce | `custom_components/audiconnect/` (v1.19.2, `cloud_polling`) | source cloud (hors périmètre contrat) |

### Entités (par catégorie)

**Helpers (`input_number`)** — `autonomie_audi_etron_full`, `audi_temperature_charge`, `audi_autonomie_corrigee_temperature`.
**Helper (`input_text`)** — `historique_autonomie_audi_etron`.
**Capteurs locaux stabilisés** — `entity_id` dérivé du `name` : `sensor.audi_e_tron_{autonomie,pourcentage_moteur_principal,etat_de_charge,kilometrage,derniere_mise_a_jour,temps_stationnement,prochaine_inspection_*}_local` ; `unique_id` dérivé de la source Audi : `audi_a3_sportback_e_tron_{range,primary_engine_percent,charging_state,mileage,last_update,park_time,service_inspection_*}_local`.
**Binary sensors ouvrants** — `binary_sensor.audi_e_tron_{porte_*,fenetre_*,coffre_verrouille,toit_ouvrant}_local`.
**Miroirs** — `sensor.audi_temperature_charge`, `sensor.audi_autonomie_corrigee_temperature`.
**Statistiques** — `sensor.autonomie_audi_etron_mensuelle` (produit), `sensor.audi_temperature_charge_mensuelle` (produit, sans `unique_id`).
**Compteurs** — `sensor.audi_e_tron_distance_mois`, `sensor.audi_e_tron_distance_an`.
**Navigation** — `sensor.etat_voiture_dashboard`.

### Dépendances inter-domaines

| Sens | Entité | Domaine |
|---|---|---|
| Consommé | `sensor.temperature_jardin` | Météo (`contrats/meteo/axe_temperature_jardin.md`) — dépendance contractualisée |
| Consommé | `script.notification_envoyer`, `input_text.telephone_antoine_notify` | Notifications (transverse) |
| Source amont | `custom_components/audiconnect` (`sensor.audi_a3_sportback_e_tron_*`) | Intégration cloud tierce |

---

## 2. Architecture observée (factuelle)

La chaîne réellement implémentée est conforme à l'intention du contrat :

```
audiconnect (cloud, instable)
   └─► trigger template sensors *_local  (stabilisation : dernière valeur valide, reload-safe)
          ├─► automation 1015000000001  (déclenche à pleine charge >98.9 %)
          │      └─► écrit 3 input_number (snapshot atomique : autonomie + T° + autonomie corrigée 20 °C)
          │              └─► statistics (moyenne 31 j) ─► archive mensuelle (input_text) ─► dashboard batterie
          ├─► automation 10150000000005 (notification persistante « charge en cours »)
          ├─► sensor.etat_voiture_dashboard (couleur bouton navigation)
          └─► dashboards audi / audi_securite (lecture pure)
```

La séparation perception → décision → mémorisation → historisation → UI est matériellement présente. La correction thermique `autonomie / (1 + 0.007 × (20 − T_obs))` est implémentée à l'identique du contrat (`11_automations/voiture/autonomie.yaml`, l. 60-65).

---

## 3. Forces du domaine

- **Architecture contract-first réellement appliquée** : le contrat `voiture.md` décrit une chaîne que le runtime respecte (couche de stabilisation, snapshot atomique, séparation UI/décision).
- **Couche de stabilisation systématique** : toute donnée cloud transite par un trigger sensor `*_local` avec fallback `this.state`, conforme à l'invariant « le cloud mesure, le local sécurise » (vérifié sur les 8 sensors + 13 binary_sensors).
- **Snapshot atomique** : les 3 `input_number` sont écrits dans une seule séquence d'actions, par une **autorité unique** (`1015000000001`). Le checker `check_voiture_contracts.py` (T05, T08) garde cet invariant.
- **Garde CI existante** : un checker contractuel dédié est câblé dans `.github/workflows/contracts_voiture.yml` — démarche rare et saine.
- **Notification d'état correctement modélisée** : `notification_etat_charge.yaml` est une pure matérialisation d'état (apparition/extinction), sans logique ni horodatage, conforme au contrat (et gardé par T09).
- **Documentation d'en-tête riche** : chaque fichier porte un cartouche rôle/périmètre/interdits cohérent.

---

## 4. Constats

> Gravité : **Critique** (chaîne potentiellement morte) · **Majeur** (fragilité systémique) · **Moyen** · **Faible** · **Info**.

### AUDI-02 — Mismatch de nommage de la statistique d'autonomie (`etron` vs `e_tron`) — **CRITIQUE**
- **Description** : le capteur statistique **produit** l'`entity_id` `sensor.autonomie_audi_etron_mensuelle` (slug du `name` « Autonomie Audi etron Mensuelle »), mais **tous** ses consommateurs référencent `sensor.autonomie_audi_e_tron_mensuelle` (avec underscore). Du point de vue du dépôt, les deux ne coïncident pas.
- **Preuve** :
  - Producteur : `13_sensor_platforms/statistics/voiture/autonomie.yaml:39` → `name: "Autonomie Audi etron Mensuelle"` (et `unique_id: autonomie_audi_etron_mensuelle`).
  - Consommateurs : `11_automations/voiture/archive.yaml:38,47` ; `18_lovelace/dashboards/voiture/audi_batterie.yaml:56,105,131` ; `recorder.yaml:410`.
  - `git grep` confirme qu'**aucune** entité `…e_tron_mensuelle` n'est définie.
- **Impact** : si l'`entity_id` n'a pas été renommé en UI hors-dépôt, l'**archivage mensuel ne s'exécute jamais** (condition `not in ['unknown',…]` toujours fausse) et la carte batterie est vide. S'il *a* été renommé, le système fonctionne mais **viole le principe « le dépôt est la vérité »** (état non reproductible depuis un clone). À trancher en priorité sur le registre runtime.

### AUDI-01 — Double convention `entity_id` (slug du `name`) vs `unique_id` sur tous les capteurs locaux — **MAJEUR**
- **Description** : chaque trigger sensor porte `name: "Audi e-tron – X (Local)"` (slug → `audi_e_tron_X_local`) mais `unique_id: audi_a3_sportback_e_tron_X_local`. Les consommateurs utilisent le slug du `name` ; le `unique_id` suit une convention différente. Le domaine fonctionne « par défaut » mais n'est pas auto-cohérent.
- **Preuve** : `12_template_sensors/voiture/batterie/autonomie.yaml:25-26` (name vs unique_id), idem `pourcentage.yaml`, `etat_charge.yaml`, `kilometrage.yaml`, `derniere_maj.yaml`, `stationnement.yaml`, `revision/*`, `ouvertures/**`. Consommateurs : `11_automations/voiture/autonomie.yaml:45,52,59` (`sensor.audi_e_tron_autonomie_local`, `…_pourcentage_moteur_principal_local`).
- **Impact** : tout renommage du `name:` casse **silencieusement** l'ensemble des automatisations et dashboards, sans qu'aucun `unique_id` ne le signale. Le `unique_id` est trompeur (il décrit une entité qui n'est pas celle consommée). Dette de fragilité sur 20+ entités.

### AUDI-03 — Lignes recorder fantômes + entités distance non historisées — **MOYEN**
- **Description** : `recorder.yaml` mélange `entity_id` réels et `unique_id` (qui ne sont pas des `entity_id`), et référence des entités distance inexistantes.
- **Preuve** :
  - `recorder.yaml:415-417` liste `sensor.audi_a3_sportback_e_tron_{range,charging_state,primary_engine_percent}_local` = des `unique_id`, donc 3 lignes ne capturent rien (les vrais `entity_id` sont déjà aux l. 411-413).
  - `recorder.yaml:419-420` liste `sensor.distance_audi_e_tron_{mensuelle,annuelle}` ; or `utility_meter.yaml:261,268` crée `sensor.audi_e_tron_distance_{mois,an}`. Les 2 lignes recorder sont fantômes **et** les vraies entités distance ne sont pas historisées.
- **Impact** : pollution du recorder (5 lignes mortes) ; **historique long terme de la distance parcourue non persisté**.

### AUDI-04 — Sous-système « ouvrants / sécurité » totalement hors contrat — **MOYEN**
- **Description** : le contrat `voiture.md` ne couvre ni portes, ni fenêtres, ni coffre, ni toit ouvrant, alors qu'un sous-système complet existe et alimente un dashboard dédié.
- **Preuve** : `grep -ciE 'porte|fenetre|coffre|ouvrant|toit|window|door|trunk|verrou' voiture.md` = **0** ; pourtant `12_template_sensors/voiture/ouvertures/**` (13 binary_sensors) et `18_lovelace/dashboards/voiture/audi_securite.yaml` (l. 53-141) en dépendent.
- **Impact** : un pan entier du domaine échappe à la gouvernance normative et au checker CI (qui ne le teste pas). Aucune autorité, aucun invariant documenté sur ces entités.

### AUDI-05 — Angle mort du checker contractuel (CI verte malgré les écarts) — **MOYEN**
- **Description** : `check_voiture_contracts.py` valide les capteurs locaux par `unique_id` (T03) mais ne vérifie jamais que l'`entity_id` réellement **consommé** correspond (T04 = simple présence d'un motif `sensor.*_local`). Il ne teste ni AUDI-02 (naming statistique), ni AUDI-03 (recorder), ni AUDI-04 (ouvrants).
- **Preuve** : `scripts/arsenal_contracts/check_voiture_contracts.py` — `is_declared_as_unique_id` (l. 60-66), `test_consolidation_triggered_by_local_sensor` (regex `sensor\.\w+_local` seule), `test_no_cloud_sensor_in_automations` (T11) dont les commentaires mélangent eux-mêmes les deux familles de nommage.
- **Impact** : faux sentiment de conformité — la CI passe au vert pendant qu'AUDI-01/02/03/04 subsistent.

### AUDI-06 — Dashboard batterie divergent du contrat + libellé trompeur — **FAIBLE**
- **Description** : le contrat (Couche 5) impose l'axe droit = `sensor.audi_temperature_charge` (miroir instantané) ; le dashboard utilise `sensor.audi_temperature_charge_mensuelle` (moyenne statistique non documentée). De plus le libellé « Moyenne hebdomadaire (km) » est posé sur un capteur à fenêtre 31 j (mensuelle).
- **Preuve** : `voiture.md` (§ Carte normative — Co-visualisation) vs `audi_batterie.yaml:115` (`…_mensuelle`) et `audi_batterie.yaml:57` (libellé « hebdomadaire »).
- **Impact** : incohérence doc↔runtime ; libellé numériquement faux pour l'utilisateur.

### AUDI-07 — Rupture du schéma d'ID d'automatisation — **FAIBLE**
- **Description** : `1015000000001` et `1015000000004` ont 13 chiffres ; `10150000000005` en a **14**.
- **Preuve** : `11_automations/voiture/notification_etat_charge.yaml` (`id: "10150000000005"`), repris à l'identique dans le contrat et le checker T02.
- **Impact** : entorse au schéma de préfixe numérique canonique d'Arsenal ; lisibilité/risque de collision.

### AUDI-08 — Capteur statistique température sans `unique_id` — **FAIBLE**
- **Description** : `13_sensor_platforms/statistics/voiture/temperature_charge.yaml` ne définit pas de `unique_id`.
- **Preuve** : fichier (absence de la clé ; présent dans `autonomie.yaml` voisin).
- **Impact** : entité non gérable en UI, `entity_id` figé sur le `name` ; un changement de `name` casse l'historique. Asymétrie avec son jumeau autonomie.

### AUDI-09 — Plage de plausibilité des `input_number` autonomie (max 100 km) — **INFO / À vérifier runtime**
- **Description** : `autonomie_audi_etron_full` et `audi_autonomie_corrigee_temperature` plafonnent à `max: 100`. Si la source `sensor.audi_a3_sportback_e_tron_range` reporte une autonomie **combinée** (électrique + thermique) plutôt qu'électrique seule, écrêtage possible.
- **Preuve** : `03_input_numbers/voiture/autonomie.yaml` (`max: 100`).
- **Impact** : faible — l'autonomie électrique d'une A3 e-tron (~40-50 km) reste < 100 ; à confirmer sur les valeurs runtime.

### AUDI-10 — Sémantique du déclencheur pleine charge — **INFO / À vérifier runtime**
- **Description** : l'automation déclenche sur `sensor.audi_e_tron_pourcentage_moteur_principal_local > 98.9`, interprété par le contrat comme « % batterie ». Pour un PHEV, `primary_engine_percent` (audiconnect) peut désigner autre chose que l'état de charge batterie.
- **Preuve** : `11_automations/voiture/autonomie.yaml:43-46` (trigger) vs `voiture.md` § Couche 3 (« % batterie local »).
- **Impact** : à vérifier — si la sémantique diffère, les snapshots se déclenchent au mauvais moment.

---

## 5. Dette technique (priorisée)

1. **AUDI-02** — naming statistique `etron`/`e_tron` : chaîne archivage + carte batterie potentiellement mortes. *À trancher en premier sur le runtime.*
2. **AUDI-01** — double convention `entity_id`/`unique_id` : fragilité systémique sur 20+ entités, casse silencieuse au moindre renommage.
3. **AUDI-05** — angle mort du checker : c'est la **dette qui masque les autres** ; tant qu'elle existe, la CI ne protège pas le domaine.
4. **AUDI-03** — recorder fantôme + distance non historisée.
5. **AUDI-04** — contrat incomplet (ouvrants/sécurité hors gouvernance).
6. **AUDI-06 / 07 / 08** — incohérences cosmétiques et asymétries de maintenance.

---

## 6. Recommandations

### 🔴 Critique
- **Vérifier sur le registre d'entités runtime** l'`entity_id` réel de la statistique d'autonomie (AUDI-02). Deux issues : soit l'archivage est mort (à réparer), soit l'entité a été renommée en UI → **réaligner le `name:` du dépôt** sur l'`entity_id` runtime pour restaurer la reproductibilité.
- **Statuer sur la convention de nommage** (AUDI-01) : choisir une règle unique — soit forcer un `entity_id:` explicite dans chaque template, soit aligner `unique_id` et slug du `name` — et l'appliquer à toutes les entités du domaine.

### 🟠 Importante
- **Renforcer `check_voiture_contracts.py`** (AUDI-05) pour cross-valider que chaque `entity_id` consommé par les automatisations/dashboards correspond à une entité réellement produite (résolution name→slug), et ajouter des tests pour la statistique, le recorder et les ouvrants.
- **Nettoyer `recorder.yaml`** (AUDI-03) : retirer les 5 lignes fantômes, ajouter les vraies entités `sensor.audi_e_tron_distance_{mois,an}`.
- **Étendre le contrat** (AUDI-04) au sous-système ouvrants/sécurité, ou le sortir explicitement du périmètre — mais le statuer.

### 🟢 Confort
- Ajouter un `unique_id` au capteur statistique température (AUDI-08).
- Aligner le dashboard batterie sur l'entité contractuelle et corriger le libellé « hebdomadaire » → « mensuelle » (AUDI-06).
- Harmoniser l'ID `10150000000005` sur le schéma 13 chiffres (AUDI-07).
- Confirmer la sémantique de `primary_engine_percent` et la plage `max: 100` (AUDI-09/10) sur les valeurs runtime.

---

## Annexe — Périmètre exclu de l'audit
- `custom_components/audiconnect/` : intégration tierce explicitement hors contrat (le contrat ne couvre pas « l'intégration Audi elle-même »). Notée v1.19.2, `cloud_polling`, vendue dans le dépôt (non gérée via HACS) — point de maintenance amont à surveiller, mais hors scope normatif.
- `00_documentation_arsenal/contrats/batteries.md` : concerne les **piles des capteurs Zigbee/Netatmo** (`group.batteries`, seuil 28 %), **sans rapport** avec la batterie de traction Audi. Hors périmètre du domaine Voiture.
- Historique git : clone superficiel (`--depth 50`) — l'archéologie des commits anciens n'a pas été exploitée.
