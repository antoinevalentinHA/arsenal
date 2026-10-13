# Chantier TRANSVERSE (C43) — Réduction du churn d'attributs du Recorder

| Champ | Valeur |
|---|---|
| **Chantier** | Réduire le volume Recorder écrit **sans aucun changement d'état**, causé par des grandeurs continues ou d'ancienneté exposées en attributs et réévaluées à la minute. Deux lots disjoints : **A** suppression d'attributs redondants, **B** quantification de la valeur publiée. |
| **Domaine** | Transverse — observabilité, coût Recorder. Touche météo, arrosage, chauffage, climatisation. |
| **Statut** | **Ouvert (2026-08-31).** **Lots A (A1–A6) et B1/B2 : patch préparé, non commité.** Gate du lot A **franchi** par recherche opérateur sur l'instance (§4.3). |
| **Priorité** | **P2** — aucun risque fonctionnel ; enjeu de coût et de lisibilité de l'historique. |
| **Ouvert le** | 2026-08-31. |
| **Prochain jalon** | Déployer, puis **mesurer le gain réel** sur une sauvegarde postérieure d'au moins 30 j (critère §6.3). |
| **Registre** | Chantier **C43** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Mesure amont** | `arsenal-runtime/analyses/recorder_churn_attributs_20260831/` (hors dépôt gouverné) — `SYNTHESE.md`, `LOT_REDUCTION_CHURN.md`, simulations de granularité. |

> **⚠️ Portée.** **Aucun `recorder.yaml` modifié. Aucun microscope retiré. Aucun chantier clos.
> Aucun contrat amendé. Aucun changelog créé** (la doctrine
> [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1 interdit de
> fabriquer un changelog de sa propre initiative). Le lot ne touche que des **valeurs d'attributs
> publiées** ; aucune entrée de décision, aucun seuil, aucun calcul métier n'est modifié.

---

## 1. Constat

Sur la sauvegarde `recorder_20260831.db` (31 j, 920 562 lignes), **360 904 lignes — 39,2 %** sont écrites sans aucun changement d'état. Une ligne `states` est écrite dès que **l'état ou les attributs** changent : une grandeur continue exposée en attribut et réévaluée chaque minute produit une ligne par minute pour une information nulle.

Douze entités concentrent 328 611 de ces lignes. Le moteur a été **attribué par mesure** (comptage, pour chaque transition sans changement d'état, des clés d'attribut qui changent), pas supposé.

## 2. Lot A — suppression de six attributs redondants

Critère d'appartenance : **aucune exigence documentaire ne porte sur l'attribut sur l'entité historisée**. L'exigence vise soit une entité jumelle absente du Recorder, soit une entité source déjà historisée.

| # | Attribut | Entité historisée | Fichier | Exigence portée par | Lignes |
|---|---|---|---|---|---:|
| A1 | `age_memoire_s` | `sensor.temperature_jardin` | `12_template_sensors/meteo/mesures/temperature/jardin/facade.yaml:96` | `sensor.temperature_jardin_statut` — hors Recorder, **ligne 180 conservée** | 50 429 |
| A2 | `age_memoire_minutes` | `sensor.humidite_relative_jardin` | `.../humidite_relative/jardin/facade_finale.yaml:142` | `sensor.humidite_relative_jardin_age_memoire_minutes` — entité dédiée, hors Recorder | 46 404 |
| A3 | `uptime_age_secondes` | `binary_sensor.rain_bird_pont_donnees_fraiches` | `12_template_sensors/arrosage/pont_donnees_fraiches.yaml:114` | aucune | 45 287 |
| A4 | `snzb_age_s` | `binary_sensor.pluie_evidence_active` | `12_template_sensors/meteo/pluie/evidence_active.yaml:105` | aucune | 44 572 |
| A5 | `age_heures` | `sensor.chauffage_courbe_completude` | `.../courbe_de_chauffe/observabilite_completude_apprentissage.yaml:52` | aucune — ancre `dernier_cycle` conservée | 7 450 |
| A6 | `mediane` | `binary_sensor.arrosage_besoin_sol` | `12_template_sensors/arrosage/besoin_sol.yaml:80` | `sensor.jardin_humidite_sol_mediane` — **déjà historisé** | 4 334 |

**Total : 198 476 lignes, 21,6 % de la base. Lot APPLIQUÉ (2026-08-31) après franchissement du gate — voir §4.**

Dans chaque cas, l'attribut retiré est remplacé par un commentaire qui **nomme le porteur canonique** de l'information, afin qu'aucune relecture ultérieure ne prenne le retrait pour une perte d'observabilité. Les grandeurs de règle — `source_horloge` et `seuil_secondes` (A3), `snzb_rain` (A4), `dernier_cycle` et `seuil_fraicheur_h` (A5), `seuil` et `hysteresis` (A6) — sont **toutes conservées**.

## 3. Lot B — quantification de la valeur publiée

L'attribut **reste exposé** ; seule la granularité de la valeur publiée change. Les valeurs brutes consommées par les décisions, seuils et calculs sont **inchangées** : dans les deux cas l'attribut est une recopie, et l'état se recalcule indépendamment depuis les sources.

| # | Attribut | Entité | Avant | Après | Erreur max | Lignes |
|---|---|---|---|---|---|---:|
| B1 | `duree_ecoulee_h` | `binary_sensor.clim_extinction_absence_prolongee_autorisee` | `round(2)` | `round(1)` | 3 min | 29 944 |
| B2 | `tmean_c`, `tmin_c`, `tmax_c` | `sensor.arrosage_demande_climatique_et0` | recopie brute | `round(1)` sous garde `is_number` | 0,05 °C | 26 532 |

**Total : 56 476 lignes, 6,1 % de la base.**

**B3 (`valeur_modulante`, VMC) est exclu** par arbitrage propriétaire : obstacle contractuel frontal (`vmc.md` §10.2 exigence 21 « sa valeur courante » et §10.4 *Fidélité des frontières exposées*), plancher résiduel dû à `statut_grandeur_modulante`, gain de 0,33 à 0,50 % seulement.

### 3.1 Notation — décimales ≠ pas de quantification

`round(n)` en Jinja prend un **nombre de décimales**, pas un pas ; `round(0.5)` est invalide (l'argument est tronqué à 0). Toute granularité non décimale s'écrit `((x / q) | round(0)) * q`. Les deux traitements retenus sont **décimaux** (`round(1)`) et n'emploient donc pas cette seconde forme.

### 3.2 Amendements requis — aucun

| Clause | Verdict |
|---|---|
| `contrats/climatisation/15_absence_vacances_veto_cool.md` §76 | Impose l'**exposition** de `duree_ecoulee_h`, **ne spécifie aucune précision** → pas d'amendement |
| `contrats/climatisation/capteurs/blocages/10_blocages.md` §50 | Idem → pas d'amendement |
| `audits/04_chantiers/climatisation/protocole_validation_terrain_absence_cool.md` §4 | S1 « court de 0 vers le seuil » reste lisible à 0,1 h → pas d'amendement (le deviendrait à partir du pas 0,5 h) |
| `audits/04_chantiers/climatisation/runbook_s7_s8_…md` | `8 ≤ V < E` reste satisfiable à 0,1 h → pas d'amendement (le deviendrait à 1 h) |
| B2 | Aucune clause contractuelle ni runbook → sans objet |

## 4. Lot A — règle de passage franchie

### 4.1 Ce qui a été vérifié

| Surface | Méthode | Résultat |
|---|---|---|
| Dépôt Arsenal, tous fichiers | `grep` exhaustif sur les 6 attributs + sur `state_attr(` | **Aucun consommateur.** Seules occurrences : les définitions elles-mêmes et des mentions documentaires |
| Automatisations / scripts UI | `configuration.yaml` : `!include_dir_merge_list` ⇒ l'éditeur UI ne peut pas écrire | **Aucune source hors dépôt possible** |
| Helpers template UI | `core.config_entries` : aucun domaine `template` | **Aucun helper UI** |
| `packages/` hors dépôt | `configuration.yaml` : aucune clé `packages:` | **Sans objet** |
| Dashboard principal | `lovelace: !include 18_lovelace/lovelace_main.yaml` — mode YAML, dans le dépôt | **Couvert par le grep dépôt** |
| Registre d'entités | `core.entity_registry` (4 072 entités) | 2 correspondances, toutes deux **faux positifs de sous-chaîne** ou l'entité jumelle canonique |

### 4.2 Ce qui n'a PAS pu être vérifié

L'extrait `.storage` local est **volontairement partiel** : `arsenal-runtime/tools/update-runtime-from-nas.ps1` copie une **liste blanche de 12 registres** qui exclut les dashboards et les helpers. Le partage NAS était indisponible au moment de l'analyse. Trois poches restent donc non vérifiées :

1. **`.storage/lovelace.map`** — un dashboard en mode `storage` existe (`map`, `require_admin`, hors barre latérale). Son contenu est inconnu.
2. **Add-ons** — `hassio` (Supervisor) est présent. Node-RED et AppDaemon ne créent pas d'entrée de configuration : leur **absence ne peut pas être déduite** de `core.config_entries`.
3. **`/config/www/`** — JavaScript de cartes personnalisées susceptible de lire un attribut en dur.

**Conséquence à ce stade.** La règle « aucun consommateur ne doit être supposé absent » interdisait de conclure hors ligne. La levée est passée par une recherche **sur l'instance**.

### 4.3 Recherche opérateur sur l'instance — gate franchi (2026-08-31)

Exécutée en lecture seule sur `/config`, `.storage` compris, plus les emplacements Node-RED et AppDaemon :

```bash
grep -rn --binary-files=without-match -e age_memoire_s -e age_memoire_minutes \
  -e uptime_age_secondes -e snzb_age_s -e age_heures -e '"mediane"' \
  /config/.storage /config/www /config/packages 2>/dev/null
ls -d /config/node-red /config/appdaemon 2>/dev/null
```

**Résultat rapporté par l'opérateur :**

| Occurrence | Qualification |
|---|---|
| `core.restore_state` | **Artefact de persistance HA** — mémorise les attributs des entités restaurées. Conséquence de l'exposition, pas un consommateur |
| `trace.saved_traces` | **Artefact de traces d'automatisation** — enregistre des exécutions passées. Idem |
| Sauvegardes de `core.entity_registry` + registre courant | Registre d'entités — ne stocke aucun usage d'attribut |
| `automation.chauffage_memoire_standby_force` | **Faux positif de sous-chaîne** (`chauff`**`age_memoire_s`**`tandby`) |
| `sensor.humidite_relative_jardin_age_memoire_minutes` | **Entité canonique attendue** — conservée, non historisée |
| Dashboards `.storage`, `/config/www`, `/config/packages` | **Aucune occurrence** |
| `/config/node-red`, `/config/appdaemon` | **Aucun répertoire** — add-ons absents |

**Verdict.** Aucun consommateur actif. Les trois poches non vérifiables du §4.2 sont couvertes : dashboard `map` (aucune occurrence `.storage`), add-ons (répertoires absents), `/config/www` (aucune occurrence). **Règle « recherche vide ⇒ suppression autorisée » déclenchée.**

> **Note.** Le retrait des six attributs implique que `core.restore_state` cessera de les porter au prochain redémarrage — sans effet, aucune logique ne les relisant.

**Mitigation restée disponible et non nécessaire.** Pour A1, A2 et A6 l'attribut subsiste sur une entité canonique (`sensor.temperature_jardin_statut`, `sensor.humidite_relative_jardin_age_memoire_minutes`, `sensor.jardin_humidite_sol_mediane`) : un consommateur découvert plus tard serait **repointé** sans perte. Pour A3, A4 et A5 il n'existe pas de jumeau.

## 5. Hors périmètre

| Poste | Motif |
|---|---|
| `switch.clim_power` (`outdoor_tmp`…) | Attributs de l'intégration Airstage ; le Recorder ne filtre pas les attributs |
| `sensor.clim_fan_mode_recommande` (`ecart_reco_reel`, `ventilation_reelle`) | `14_recommandation_ventilation.md` §231/233/243 : « vivent en attributs » ; changements légitimes |
| `statut_grandeur_modulante` (VMC ×2) | Battement d'un statut amont, pas une grandeur continue — diagnostic séparé |
| Façades jardin (`cible_robuste`, `nb_sources_*`…) | Signaux réels du pipeline de fusion |

## 6. Critères de clôture

1. Lot B1/B2 déployé, chargement HA sans erreur, attributs toujours exposés.
2. Lot A statué : exécuté après recherche complète, ou explicitement abandonné.
3. Gain mesuré sur une sauvegarde postérieure d'au moins 30 jours.
4. Aucun consommateur cassé.

## 7. Mesure du gain (2026-10-12, L4)

Base `recorder_20261012.db` (2026-09-11 04:12 → 2026-10-12 02:30, 30,9 jours) ; analyse
`arsenal-runtime/analyses/c43_mesure_gain_churn_20261012`. Méthode de référence rejouée à l'identique :
le script d'origine tourne tel quel sur la nouvelle base, et la re-simulation sur la base du 2026-08-31
redonne exactement 254 952 lignes.

- **Déploiement établi par la base** : lots A et B ensemble le **2026-08-31 à 09:58:13**, par
  rechargement des templates, sans redémarrage. Première ligne sans attribut à 09:58:12–13 pour les six
  entités du lot A ; plus aucune clé retirée dans les bases du 2026-09-18 et du 2026-10-12. La fenêtre
  mesurée commence 10,8 jours après le déploiement : elle lui est entièrement postérieure.
- **Gain brut, à fenêtres de même durée** : lot A **197 620** lignes (attendu 198 476, soit 99,6 %) ;
  lot B **66 104** (attendu 56 476) ; **total 263 724 lignes, 28,6 %** de la base de référence
  (attendu 254 952, 27,7 %). À périmètre constant (357 entités), on passe de 920 521 à 639 606 lignes
  (−30,5 %), et la part de lignes écrites sans changement d'état tombe de **39,2 % à 18,4 %**. Les
  autres entités, qui servent de témoin, varient de +1,1 %.
- **À activité constante**, le lot A reste à 99,4 % de l'attendu. Le lot B dépend de l'activité :
  B1 est proportionnel à la durée d'absence cumulée (−83,0 % par heure d'absence, pour −83,1 % simulés) ; B2 interagit avec A1, qui avait déjà divisé par deux les
  changements de sa source — interaction non prévue par le §3.

**Critères 1 à 3 : remplis.** Le critère 1 l'est par preuve indirecte : la sauvegarde ne contient pas
le journal HA, mais les attributs restent exposés et quantifiés.

**Critère 4 : à arbitrer par le propriétaire.** Rien n'est en panne, mais le déploiement a changé le
comportement de trois consommateurs, ce que la recherche du §4.3 (consommateurs d'attributs) ne
pouvait pas voir : ils réagissaient aux **mises à jour** de leur source, attributs compris.
- **Statistique « Temperature exterieure moyenne jour »** (`sampling_size: 300`, source
  `sensor.temperature_jardin`) : elle échantillonnait chaque mise à jour, y compris d'attribut. Sa
  fenêtre effective est passée d'environ 2,9 h à environ 8,1 h, avec un saut au moment exact du
  déploiement. **C'est une entrée de la décision d'arrosage** (température moyenne de l'ET₀, donc
  `climat_statut`, C11) : l'affirmation « aucune entrée de décision modifiée » est donc inexacte en
  fonctionnement. L'effet est favorable (écart à une vraie moyenne 24 h, mesuré à 05 h : de 2,65 à
  1,05 °C), mais la statistique n'est une moyenne 24 h **ni avant ni après**. C'est un défaut antérieur
  à C43, du domaine arrosage/météo (contrat 16), signalé ici sans chantier ouvert d'office.
- **Automatisation `coexistence_rain_delay`** : son déclencheur `fraicheur` (sans `to:`) réagissait
  chaque minute au changement de `uptime_age_secondes`. Les appels du script de rain delay et de
  `number.set_value` passent d'environ 1 470 à environ 5 par jour : environ 1 465 commandes
  quotidiennes vers le pont Rain Bird ont disparu. Le comportement correspond désormais à l'en-tête de
  l'automatisation.
- **`update_temperature_max/min`** se déclenchent environ trois fois moins souvent. Aucune perte n'est
  attendue (elles ne lisent que l'état), mais c'est une inférence, pas une mesure.

---

*Chantier ouvert le 2026-08-31. Source faisant foi pour la ligne C43 du registre.*
