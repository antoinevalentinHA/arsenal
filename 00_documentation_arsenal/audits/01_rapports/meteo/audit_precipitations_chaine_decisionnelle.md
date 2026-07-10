# Audit Arsenal — Chaîne décisionnelle « précipitations » / protection des ouvrants

> Type : rapport d'audit architectural statique (lecture seule).
> Portée : représentation de la notion de « pluie » et protection des ouvrants
>          (fenêtres / volets) — sources physiques, normalisation, consolidation
>          d'épisode, intentions, cumuls, décision volets, orchestration, affichage.
> Mode : lecture seule — aucun runtime, contrat, checker, dashboard ou en-tête
>          modifié dans cette passe. Aucun patch, aucune opportunité imposée.
> Principe directeur : en **audit**, le **runtime observé** est la **référence
>          factuelle** ; en **gouvernance Arsenal**, le **contrat** reste
>          l'**autorité normative**. Ce rapport n'inverse pas cette hiérarchie.
> Constat déclencheur : le détecteur Zigbee SONOFF SNZB-05
>          (`binary_sensor.zigbee_pluie_water_leak`) signale les premières gouttes
>          alors que le pluviomètre Netatmo affiche encore `0,0 mm` ; la logique de
>          fermeture des ouvrants « ne considère pas encore qu'il pleut ».
> Neutralité : ce rapport décrit et cartographie ; les « opportunités » (§11) et
>          « recommandations d'architecture » (§12) sont des pistes, **pas** des
>          décisions d'implémentation.

---

## 1. Résumé exécutif

Arsenal dispose d'une chaîne pluie **riche, stratifiée et globalement conforme** à
sa propre doctrine de séparation décision / action. La partie *réaction des volets*
est **contractualisée** (`contrats/volets_pluie.md` v2.2.1) et **vérifiée en CI**
(`scripts/arsenal_contracts/check_volets_pluie_contracts.py`,
workflow `contracts_volets_pluie.yml`).

Le point central de l'audit : **la notion de « pluie » n'est pas une notion unique,
mais trois notions concurrentes**, chacune câblée sur une source différente et
alimentant une famille de décisions différente.

| Notion métier | Entité | Source réelle | Décision alimentée |
|---|---|---|---|
| Épisode en cours (faible ou forte) | `input_boolean.pluie_en_cours` | SNZB-05 prioritaire + Netatmo secours (**entrée**) ; Netatmo **seul** (**sortie**) | Volets **chambres**, aération |
| Pluie forte | `binary_sensor.intention_pluie_forte` | Netatmo **uniquement** (≥ 2,5 mm) | Volets **séjour** |
| Pluie récente (≤ 1 h) | `binary_sensor.pluie_recente` | Netatmo `last_hour` > 0 | Aération, affichage |

Conséquence directe sur le cas observé (SNZB détecte, Netatmo à 0,0 mm) :

- **Chambres** : la chaîne *devrait* réagir aux premières gouttes — le SNZB-05 est
  la source **prioritaire** de `pluie_en_cours` — **sous réserve que le maillon
  SNZB → `pluie_en_cours` soit sain** (capteur `available` **et** `on`).
- **Séjour** : la chaîne **ne peut pas** réagir aux premières gouttes,
  **par conception** : `intention_pluie_forte` dépend exclusivement du pluviomètre
  Netatmo (≥ 2,5 mm). Tant que Netatmo affiche 0,0 mm, le séjour n'est pas protégé.

Le système **distingue** donc plusieurs concepts de pluie, mais (1) il **ne les
unifie pas** derrière une autorité de domaine unique ; (2) les **décisions
consomment des sources brutes externes** (Netatmo cloud, Zigbee) au lieu d'entités
locales sécurisées ; (3) les mécanismes d'entrée / sortie d'épisode sont
**asymétriques**, créant des angles morts en pluie faible et un risque de blocage
si Netatmo devient indisponible.

**Criticité.** MODÉRÉE côté système (idempotence d'exécution, verrou global,
reprise redémarrage en place) ; **notable côté usage** (séjour aveugle aux premières
gouttes ; risque d'épisode collant) et côté **gouvernance** (frontière de
production non contractualisée).

---

## 2. Cartographie complète des dépendances

### 2.1 Sources physiques

| Source | Entité(s) | Type | Sémantique physique |
|---|---|---|---|
| Pluviomètre Netatmo (cloud) | `sensor.pluviometre_precipitation` (intensité, mm) · `…_last_hour` · `…_aujourd_hui` | Mesure quantitative | Pluie **mesurée** (bascule après accumulation) |
| SONOFF SNZB-05 (Zigbee, device `zigbee_pluie` `0xa4c1380550bda762`) | `binary_sensor.zigbee_pluie_water_leak` (+ `…_battery`, `…_linkquality`) | Détecteur de présence d'eau | Premières **gouttes** / contact d'eau |
| Prévision Met.no | `weather.forecast_maison` → `sensor.pluie_prevue` | Présomption | Pluie **prévue** (jamais un fait) |

> Ni Netatmo ni le SNZB-05 ne sont définis en YAML dans le dépôt : ce sont des
> entités d'intégration / Zigbee2MQTT, **uniquement consommées**.

### 2.2 Normalisation matérielle (abstraction du SNZB-05)

- `05_input_booleans/meteo/pluie_zigbee_virtuel.yaml` → `input_boolean.pluie_zigbee_virtuel`
  (impulsion normalisée **et** injection manuelle de test / secours).
- `08_timers/meteo/pluie.yaml` → `timer.pluie_zigbee_rearm` (2 min, `restore: true`).
- `11_automations/meteo/pluie/impulsion/debut.yaml` (`10160000000005`, mode `restart`) :
  anti-rebond 1 s, coupe-circuit « capteur bloqué » à 10 min.
- `11_automations/meteo/pluie/impulsion/fin.yaml` (`10160000000006`, mode `single`) :
  réarmement à la fin du timer.

### 2.3 Consolidation « vérité métier » et intentions

- `05_input_booleans/meteo/pluie_en_cours.yaml` → `input_boolean.pluie_en_cours`
  (vérité consolidée, produite **impérativement** par des automations).
  - Entrée : `11_automations/meteo/pluie/maj_sensor/on.yaml` (`10160000000002`, `restart`) —
    SNZB-05 prioritaire, Netatmo (> 0) en secours.
  - Sortie : `11_automations/meteo/pluie/maj_sensor/off.yaml` (`10160000000003`, `single`) —
    Netatmo < 0,1 mm pendant 5 min + watchdog 1 min. **Ignore explicitement le Zigbee.**
- `12_template_sensors/volets/intention_pluie_detectee.yaml` → `binary_sensor.intention_pluie_forte`
  (**déclaratif**, Netatmo ≥ `input_number.seuil_pluie_fermeture_volets`, défaut 2,5 mm).
- `12_template_sensors/meteo/pluie/recente.yaml` → `binary_sensor.pluie_recente` (Netatmo `last_hour` > 0).

### 2.4 Chaîne de mesure / cumuls (statistiques)

- `12_template_sensors/meteo/pluie/capteurs_locaux.yaml` → `sensor.pluie_aujourdhui_local`,
  `sensor.pluie_total_local` (façade du store).
- `03_input_numbers/meteo/pluie_cumul.yaml` → `input_number.pluie_total_local_store`, `…pluie_today_last`.
- `11_automations/meteo/pluie/totaliseur_cumulatif.yaml` (`10160000000009`) — total **monotone**.
- `13_sensor_platforms/statistics/meteo/pluie/cumul_{24,48,72}h.yaml` → `…_brut` (moteurs `statistics`).
- `12_template_sensors/meteo/pluie/cumul_glissant.yaml` → `sensor.pluie_cumul_{24,48,72}h` (couche métier).
- `utility_meter.yaml` → `sensor.pluie_journaliere`, `sensor.pluie_hebdomadaire` (sur `pluie_total_local`).

### 2.5 Couche décision (volets)

- `12_template_sensors/volets/autorisation_fermeture_volets_pluie_sejour.yaml` → binary_sensor (politique présence + verrou).
- `12_template_sensors/volets/cibles_volets_pluie_chambres.yaml` → sensor (covers chambres à fermer).
- `12_template_sensors/volets/cibles_volets_pluie_sejour.yaml` → sensor (covers séjour, **indépendant des contacts séjour**).
- `12_template_sensors/volets/intention_fenetres_concernees_ouvertes_pluie.yaml` → binary_sensor (≥ 1 fenêtre du périmètre ouverte).

### 2.6 Paramètres

- `05_input_booleans/meteo/volets_auto_pluie.yaml` → `input_boolean.fermeture_volets_pluie` (verrou global).
- `06_input_selects/volets/pluie.yaml` → `input_select.activation_volets_pluie` (`Toujours` / `En présence uniquement` / `En absence uniquement`).
- `03_input_numbers/meteo/pluie_volets.yaml` → `input_number.seuil_pluie_fermeture_volets` (0–5 mm, défaut 2,5).
- `03_input_numbers/arrosage/seuils_pluie.yaml` → seuils cumuls 24/48/72 h + prévue + horizon (chaîne arrosage).

### 2.7 Exécution

- `10_scripts/volets/fermeture_execute.yaml` → `script.volets_fermeture_execute`
  (`mode: queued`, idempotent, **exécutif pur** : aucune lecture de capteur, aucune politique).

### 2.8 Orchestration

- `11_automations/meteo/pluie/pluie_volets_chambres.yaml` (`10160000000011`) — trigger `pluie_en_cours → on`.
- `11_automations/meteo/pluie/pluie_volets_sejour.yaml` (`10160000000010`) — trigger `intention_pluie_forte → on`.

### 2.9 Affichage

- `sensor.resume_fenetres_concernees_ouvertes_pluie` (texte, UI).
- Dashboards : `18_lovelace/dashboards/meteo/meteo_precipitations.yaml`,
  `18_lovelace/dashboards/volets/diagnostic.yaml`, `…/volets/reglages.yaml`,
  cartes aération pluie, palmarès et graphes semaine / année.

### 2.10 Consommateurs « pluie » hors volets

- **Aération** : `12_template_sensors/aeration/conseillee/{rdc,etage,global}.yaml` consomment
  `pluie_en_cours` **et** `pluie_recente`.
- **Arrosage** : `binary_sensor.arrosage_suspension_pluie` consomme les cumuls + `pluie_prevue`.
- **Palmarès** : `sensor.palmares_pluie_journalier` + anomalie (mémoire d'extrêmes, hors temps réel).

### 2.11 Documentation & CI

- `contrats/volets_pluie.md` (v2.2.1, **normatif**) — *réaction* volets uniquement ;
  **exclut** explicitement la détection / qualification / seuil pluviométrique (§2).
- `contrats/meteo/pluie_palmares.md` — records journaliers (hors décision temps réel).
- `scripts/arsenal_contracts/check_volets_pluie_contracts.py` — vérificateur CI.
- **Aucun contrat normatif** ne couvre la *production* de `pluie_en_cours` /
  `intention_pluie_forte` : `volets_pluie.md` §5.2 délègue cette « frontière » à
  « un contrat météo distinct » **inexistant** ; le contrat météo général
  (`contrats/meteo/meteo.md`) ne reconnaît pas la précipitation parmi ses axes
  (température / HR / HA / humidex).

---

## 3. Chaîne décisionnelle : qui décide, qui affiche, qui statistique

| Entité | Décision | Affichage | Statistiques | Consommateur(s) |
|---|:--:|:--:|:--:|---|
| `binary_sensor.zigbee_pluie_water_leak` | ● (indirect, via impulsion) | ● (graphe 24 h) | ● (recorder) | impulsion → `pluie_zigbee_virtuel` |
| `input_boolean.pluie_zigbee_virtuel` | ● (relais) | — | — | `maj_sensor/on` |
| `input_boolean.pluie_en_cours` | ● | ● (carte aération) | — | volets chambres, aération |
| `binary_sensor.intention_pluie_forte` | ● | ● (diagnostic volets) | — | volets séjour, `cibles_sejour` |
| `binary_sensor.pluie_recente` | ● (aération) | ● | — | aération, cartes |
| `sensor.pluviometre_precipitation` | ● (source directe) | ● | ● | `maj_sensor on/off`, `intention_pluie_forte` |
| `sensor.pluie_cumul_{24,48,72}h` | ● (arrosage) | ● | ● | `arrosage_suspension_pluie` |
| `sensor.pluie_prevue` | ● (arrosage) | ● | ● | `arrosage_suspension_pluie` |
| `sensor.cibles_volets_pluie_{chambres,sejour}` | ● | ● (KPI) | — | automations volets |
| `binary_sensor.autorisation_fermeture_volets_pluie_sejour` | ● | ● | — | `cibles_sejour` |
| `binary_sensor.intention_fenetres_concernees_ouvertes_pluie` | ◐ « référence canonique » mais **non utilisée comme garde** | ● | — | diagnostic |
| `sensor.resume_fenetres_concernees_ouvertes_pluie` | — | ● | — | UI |
| `sensor.pluie_journaliere` / `_hebdomadaire` / palmarès | — | ● | ● | palmarès, graphes |

**Déclencheurs réels de décision :** volets **chambres** ⇐ `pluie_en_cours` (toute
pluie) ; volets **séjour** ⇐ `intention_pluie_forte` (Netatmo ≥ 2,5 mm) ; **aération**
⇐ `pluie_en_cours` + `pluie_recente` ; **arrosage** ⇐ cumuls + `pluie_prevue`.

**Nuance de classification.** `intention_fenetres_concernees_ouvertes_pluie` est
désignée « référence canonique du périmètre ouvrants » (contrat §3), mais dans les
faits l'automation chambres recalcule sa propre liste de fenêtres et le séjour
ignore les contacts : cette entité est **de facto diagnostique**, pas décisionnelle.

---

## 4. Sémantique métier : concepts distingués vs confondus

| Concept | Représenté ? | Entité | Remarque |
|---|:--:|---|---|
| Premières gouttes | ◐ partiellement | `zigbee_pluie_water_leak` (brut) | **Non exposé** comme concept nommé de premier niveau ; absorbé dans `pluie_en_cours` |
| Pluie mesurée (instantanée) | oui | `sensor.pluviometre_precipitation` | — |
| Pluie récente (≤ 1 h) | oui | `binary_sensor.pluie_recente` | — |
| Épisode en cours | oui | `input_boolean.pluie_en_cours` | Binaire, sans notion d'intensité ni de durée |
| Pluie persistante | non | — | Non modélisée (ni durée d'épisode, ni intensité intégrée) |
| Pluie forte | oui | `binary_sensor.intention_pluie_forte` | Seuil instantané, **sans hystérésis** |
| Pluie terminée | ◐ implicite | `pluie_en_cours = off` / `pluie_recente = off` | Sortie Netatmo seule |
| Pluie prévue | oui (bien isolée) | `sensor.pluie_prevue` | Marquée « présomption / présumé », jamais 0 par défaut |
| Cumuls 24/48/72 h | oui | `sensor.pluie_cumul_*` | Distinction « fenêtre vide » vs « source morte » soignée |

**Confusions / recouvrements observés :**
- **« Il pleut »** existe en **trois versions concurrentes** (`pluie_en_cours`,
  `intention_pluie_forte`, `pluie_recente`) aux sources et sémantiques différentes,
  pouvant diverger simultanément.
- **« Premières gouttes »** et **« épisode de pluie »** sont **fusionnés** : le signal
  SNZB-05 (détection de contact d'eau) est promu directement au rang d'épisode métier.
- Le **SNZB-05 est sémantiquement un détecteur de fuite d'eau** (`water_leak`) : il se
  déclenche au mouillage d'une surface et se réarme au séchage. L'employer comme
  détecteur d'*apparition* de pluie est un usage détourné (d'où le coupe-circuit
  « capteur bloqué » à 10 min).

---

## 5. Robustesse : situations potentiellement sous-optimales

1. **Premières gouttes avant bascule Netatmo (cas rapporté).** Séjour non protégé par
   conception (seuil 2,5 mm Netatmo). Chambres protégées *seulement si* le maillon
   SNZB → `pluie_en_cours` est sain (SNZB-05 `available` **et** `on`).
2. **Sortie d'épisode asymétrique (angle mort pluie faible / bruine).** Un épisode ouvert
   par le SNZB-05 alors que Netatmo reste ~0 mm : le SNZB se réarme après 2 min, puis
   `maj_sensor/off` (Netatmo < 0,1 mm pendant 5 min) **éteint `pluie_en_cours` alors
   qu'il bruine encore**. Entrée multi-source, sortie Netatmo seul.
3. **Blocage `pluie_en_cours = on` si Netatmo indisponible.** `maj_sensor/off` exige un
   Netatmo valide (déclencheur direct **et** watchdog). Si Netatmo tombe pendant un
   épisode ouvert par le SNZB-05, aucune autorité ne peut refermer l'épisode →
   **état collant**.
4. **Absence d'hystérésis sur `intention_pluie_forte`.** Comparaison `>=` brute au seuil :
   oscillation possible autour de 2,5 mm (orage à intensité fluctuante) → re-déclenchements
   en cascade de l'automation séjour (fermeture idempotente, mais chaque front `on`
   re-notifie).
5. **Pluie discontinue / averses.** Chaque impulsion SNZB se réarme après 2 min ;
   `pluie_en_cours` peut rebondir entre averses, sans notion d'« épisode englobant ».
6. **Incohérence multi-sources non réconciliée / non observée.** SNZB « eau détectée » vs
   Netatmo « 0 mm » : aucune logique de réconciliation au-delà de la priorité codée dans
   `maj_sensor/on`, et **aucune trace exposée** de la source ayant déclenché l'épisode.
7. **Deux représentations Zigbee mélangées.** `maj_sensor/on` **se déclenche** sur le
   signal normalisé (`pluie_zigbee_virtuel`) mais **teste en condition** le brut
   (`zigbee_pluie_water_leak`) — la normalisation anti-rebond est contournée dans la condition.
8. **Sémantique matérielle du SNZB-05.** Latence de détection (mouillage) et de réarmement
   (séchage) intrinsèques : le capteur peut rester « on » après la fin de la pluie (mitigé
   par le coupe-circuit 10 min) et réagir avec retard aux premières gouttes selon l'exposition.

---

## 6. Architecture : matériel spécifique vs capteur d'intention abstrait

### 6.1 État actuel

- **Séjour** est lié **en dur** à un matériel unique (pluviomètre Netatmo) via
  `intention_pluie_forte`.
- **Chambres / aération** consomment `pluie_en_cours`, qui **est** une mini-abstraction à
  deux sources — mais construite de façon **impérative** (input_boolean piloté par
  automations, état persistant, dépendant du redémarrage, mitigé par `systeme_stable` +
  watchdog).
- Il n'existe **pas** de `binary_sensor.intention_pluie` **abstrait, déclaratif et
  partagé** fusionnant SNZB-05 + Netatmo (+ récente / prévue), avec `availability`
  explicite et hystérésis, que **tous** les régimes consommeraient.

### 6.2 Confrontation à la doctrine Arsenal

| Principe doctrinal | Source | Constat pluie |
|---|---|---|
| Sécurisation des capteurs externes : aucune décision ne consomme une source brute externe | `architecture/securisation_capteurs_externes.md` | Écart : les décisions lisent **directement** le Netatmo cloud (`sensor.pluviometre_precipitation`) et le Zigbee brut (`zigbee_pluie_water_leak`). Une façade locale sécurisée existe pour les **cumuls** (`pluie_total_local`) mais **pas pour la décision** |
| Autorité unique par domaine | `03_doctrines/principes_generaux.md` §2 | Écart : domaine « pluie » sans autorité unique — trois notions décisionnelles concurrentes |
| Séparation décision / action | `03_doctrines/separation_decision_action.md` | Respectée dans la réaction volets ; deux paradigmes coexistent pour « il pleut » (impératif `pluie_en_cours` vs déclaratif `intention_pluie_forte`) |
| Décision stateless / recalculable | idem | Écart : `pluie_en_cours` est un état événementiel persistant, pas un template recalculable |
| Disponibilité explicite | `principes_generaux.md` §8 | Cumuls et prévue honnêtes ; pas de disponibilité consolidée pour la décision pluie |
| Nommage par représentation | `03_doctrines/nommage_entites.md` §7 | Écart : `zigbee_pluie_water_leak` nomme le matériel / calcul, pas la représentation (« premières gouttes ») |

### 6.3 Comparaison avec les patterns Arsenal existants

Le domaine **chauffage** applique le modèle cible : une **décision souveraine unique**
évalue plusieurs entrées et produit des états lisibles que des exécutants bornés
appliquent (`README.fr.md`). La pluie n'a pas cet équivalent : sa « décision » est
éclatée entre un input_boolean impératif, un template Netatmo-only et un binary_sensor
de récence.

---

## 7. Gouvernance : conformité aux principes Arsenal

| Principe | Verdict | Détail |
|---|:--:|---|
| Séparation décision / action | Conforme | Réaction volets : intention / autorisation / cibles (décision) vs `volets_fermeture_execute` (action pur) ; contractualisé + CI |
| Observabilité | Partiel | Attributs riches (`source`, `seuil`, `valeur`, `mode`, `presence`), dashboard diagnostic ; **mais** pas de trace de la source ayant déclenché `pluie_en_cours` |
| Robustesse | Partiel | `systeme_stable` (reprise), watchdog, `timer … restore: true`, anti-rebond, coupe-circuit ; **mais** risque d'état collant si Netatmo indisponible |
| Idempotence | Conforme / partiel | Script `queued` + saut si déjà `closed` ; `pluie_en_cours` gardé par précondition `off` ; **mais** `intention_pluie_forte` sans hystérésis |
| Absence de duplication | Partiel | Liste des ouvrants dupliquée (intention_fenetres / resume / automation chambres) ; double représentation Zigbee (brut vs virtuel) |
| Cohérence documentaire | Écarts | Voir §7.1 |

### 7.1 Écarts de cohérence documentaire relevés

- Fichier `12_template_sensors/volets/intention_pluie_detectee.yaml` → entité
  `intention_pluie_forte` (nom de fichier ≠ entité ; aucune entité `intention_pluie_detectee`
  n'existe).
- Fichier `05_input_booleans/meteo/volets_auto_pluie.yaml` → entité `fermeture_volets_pluie` (idem).
- `binary_sensor.pluie_recente` et `input_number.seuil_pluie_fermeture_volets` sont **exposés
  dans les dashboards volets mais non nommés** dans `contrats/volets_pluie.md` (le contrat
  exclut pourtant en §2 le seuil pluviométrique, qui figure dans l'écran de réglages volets).
- **Aucun contrat de production** pour la « frontière » `pluie_en_cours` /
  `intention_pluie_forte` : `volets_pluie.md` §5.2 la délègue à « un contrat météo distinct »
  **inexistant** ; le contrat météo général ne reconnaît pas la précipitation parmi ses axes.

---

## 8. Points forts

- Couche d'exécution **exécutive pure** et idempotente (`script.volets_fermeture_execute`),
  isolée de toute décision — modèle exemplaire de séparation.
- **Contractualisation + CI** de la réaction volets (rare et précieux).
- **Robustification du signal Zigbee** (anti-rebond 1 s, réarmement 2 min, coupe-circuit
  10 min) : reconnaissance explicite que le SNZB-05 est un capteur imparfait.
- **Honnêteté d'état** sur les cumuls (distinction « fenêtre vide = 0,0 » vs « source morte
  = unavailable ») et sur la prévision (« présomption », jamais 0 par défaut).
- **Verrou global** clair, n'inhibant que l'action (jamais la notification d'exposition).
- **Reprise après redémarrage** pensée (`systeme_stable`, watchdog, `restore`).
- **Prévision bien séparée du fait** (`pluie_prevue` explicitement non consommable comme
  pluie tombée).

---

## 9. Limites observées

- Notion de « pluie » **fragmentée** en trois signaux non unifiés, aux sources hétérogènes.
- **Décisions sur sources brutes externes**, en écart avec la doctrine de sécurisation.
- **Asymétrie entrée / sortie** d'épisode (multi-source à l'entrée, Netatmo seul à la sortie).
- **Séjour aveugle aux premières gouttes** (par conception, mais c'est le cœur du cas rapporté).
- **Premières gouttes non modélisées** comme concept propre ; SNZB-05 promu directement en épisode.
- **Pas d'hystérésis** sur « pluie forte » ; **pas de notion** de pluie persistante /
  d'intensité intégrée.
- **Écarts nom de fichier ↔ entité** et **couverture contractuelle incomplète** de la production.

---

## 10. Risques

| Risque | Déclencheur | Effet | Gravité |
|---|---|---|:--:|
| Épisode collant | Netatmo indisponible pendant un épisode ouvert par SNZB | `pluie_en_cours` reste `on` indéfiniment | Élevée |
| Fermeture prématurée d'épisode | Bruine détectée SNZB, Netatmo ~0 | `pluie_en_cours` éteint après 5 min malgré pluie | Moyenne |
| Séjour non protégé | Pluie faible < 2,5 mm | Volets séjour restent ouverts | Moyenne |
| Chatter volets séjour | Orage oscillant autour de 2,5 mm | Re-déclenchements / notifications répétées | Faible-Moyenne |
| Fast-path muet | SNZB indisponible / retard de mouillage | Retour au seul Netatmo (lent) sans alerte | Moyenne |
| Dérive documentaire | Contrat production absent | Évolutions non bornées par contrat / CI | Moyenne |

---

## 11. Opportunités d'amélioration (sans implémentation)

> Classées par axe. Ce sont des **opportunités**, pas des recommandations d'action.

### Gain fonctionnel
- Un **capteur d'intention « pluie détectée » abstrait et partagé** (fusion SNZB-05 +
  Netatmo, voire récente / prévue), consommé par **tous** les régimes — permettrait au
  séjour de réagir aux premières gouttes.
- **Nommer explicitement « premières gouttes »** comme concept de premier niveau, distinct
  de l'épisode.
- Introduire une notion de **pluie persistante / intensité intégrée** si utile aux décisions.

### Robustesse
- **Sécuriser localement** les sources de décision (entités locales sécurisées) conformément
  à `securisation_capteurs_externes.md`.
- **Symétriser entrée / sortie** d'épisode (faire participer le SNZB-05 — ou une fenêtre de
  grâce — à la sortie).
- Supprimer le **risque d'état collant** (source de sortie alternative / délai de sécurité).
- **Hystérésis** sur « pluie forte » ; **réconciliation multi-source explicite et observable**.

### Simplicité
- **Unifier le paradigme** (déclaratif recalculable) entre `pluie_en_cours` et
  `intention_pluie_forte`.
- **Référentiel unique des ouvrants** (éliminer la triple duplication de la liste des fenêtres).
- **Aligner noms de fichiers et entités** ; supprimer la double représentation Zigbee dans
  `maj_sensor/on`.

### Coût de maintenance
- **Contrat normatif de détection / qualification pluie** (combler la frontière orpheline
  `volets_pluie.md` §5.2).
- **Reconnaître (ou documenter l'exclusion de) la précipitation** comme axe météo.
- **Étendre la couverture CI** au sous-système de détection (pas seulement à la réaction volets).

---

## 12. Recommandations d'architecture (neutres)

Deux directions se dégagent, **sans préjuger d'un chantier** :

1. **Autorité de domaine unique pour la pluie.** Une couche « intention pluie » déclarative,
   à source multiple, avec disponibilité explicite et hystérésis, produisant des états
   lisibles gradués (p. ex. gouttes / pluie / pluie forte / terminée) — sur le modèle éprouvé
   du **domaine chauffage** (décision souveraine → exécutants bornés).
2. **Découplage décision / matériel.** Les décisions volets / aération consommeraient cette
   autorité abstraite plutôt qu'un matériel nommé (Netatmo pour le séjour, SNZB-05 pour les
   chambres), les sources restant interchangeables derrière une façade sécurisée.

Ces directions **prolongent** des principes déjà présents dans Arsenal (sécurisation des
capteurs externes, autorité unique, séparation décision / action, capteurs d'intention)
plutôt qu'elles n'en introduisent de nouveaux.

---

*Fin de l'audit — lecture seule. Aucune modification de runtime, contrat, checker ou UI
n'a été effectuée dans cette passe.*
