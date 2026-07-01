# Delta d'audit — Population A statistiques du Recorder

**Périmètre** : `recorder.yaml` (323 entités) confronté à l'ensemble des dépendances
Recorder actives du dépôt (`platform: statistics`, `history_stats`, `utility_meter`,
`state_class`).
**Base** : HEAD `5f3c98d` (post-#192).
**Nature** : reprise ciblée, **en lecture seule**, du point « statistiques Home Assistant »
de [`audit_recorder_conformite_contrat.md`](audit_recorder_conformite_contrat.md). Aucun
runtime, aucun `recorder.yaml`, aucun contrat modifié.
**Référentiel** : [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md)
(rows Population A « Long-term statistics », « history_stats », « platform: statistics »).

---

## 1. Hypothèse et verdict

**Hypothèse testée** : l'audit initial a **sous-évalué la Population A** en limitant le constat
C2 aux capteurs d'énergie `state_class: total_increasing`.

**Verdict : confirmée, et l'ampleur dépasse l'hypothèse.** L'audit initial estimait ~**16**
entités Population A (énergie). Le croisement exhaustif en établit **95 sur 323** — un facteur
**× 6**. La sous-évaluation ne tient pas à un oubli de quelques familles mais à une **erreur de
critère** : C2 a raisonné « énergie / `total_increasing` » alors que la voie dominante de
dépendance Population A dans ce dépôt est **`platform: statistics`** (des dizaines de capteurs
statistics dérivés dont les sources doivent être historisées).

---

## 2. Méthode (lecture seule)

1. Extraction des 323 entités de `recorder.yaml`.
2. Extraction de **toutes** les sources `entity_id` des `platform: statistics`
   (`13_sensor_platforms/statistics/**`, 39 fichiers, 443 sources uniques).
3. Extraction des sources des `history_stats` (`13_sensor_platforms/history_stats/**`, 5 fichiers).
4. Recensement des `utility_meter` (`utility_meter.yaml`) et des `state_class` déclarés en YAML
   (102 déclarations : 96 `measurement`, 5 `total_increasing`, 1 `total`).
5. Intersections avec `recorder.yaml` et classement par **usage actif démontré** vs **simple
   éligibilité** aux long-term statistics.

**Limites** : l'appartenance à l'**Energy Dashboard** et l'usage par des **cards
`statistics_graph`** vivent dans `.storage` (hors YAML) — **non vérifiables statiquement** ; les
points qui en dépendent sont marqués « à confirmer (UI) ». Les capteurs d'intégration
(Netatmo…) portent un `state_class` fixé par l'intégration, invisible en YAML — l'analyse
retient donc l'**usage actif tracé** (source d'un `platform: statistics`/`history_stats`) comme
critère Population A robuste, plus fort que la seule éligibilité LTS.

---

## 3. Résultat — trois compartiments

### 3.1 Population A **confirmée** (dépendance HA active, tracée en YAML) — **95 entités**

| Route de dépendance (contrat) | Nb | Nature |
|---|---|---|
| Source d'un `platform: statistics` actif | **76** | Sans historique de la source, la fenêtre glissante est tronquée après purge/redémarrage, sans signal — exactement le cas visé par le contrat |
| Source d'un `history_stats` actif | **4** | Le helper renvoie 0/N-A sans historique de la source |
| Énergie `total_increasing` (LTS + source `utility_meter`) | **15** | Long-term statistics compilées par HA ; `utility_meter` consommateur confirmé |

**Total dédupliqué : 95** (`clim_consommation_estimee_energie` compte à la fois comme source
statistics et comme énergie). Détail nominatif en **Annexe A**.

> Familles concernées : **toute** la température (maison + imprimerie), **toute** l'humidité
> relative et absolue, `co2_sejour`, `pluie_total_local`, CPU/mémoire core+supervisor,
> `ecart_consigne_instantane` (+froid/+doux), `uptime_jours`, Withings, deux `input_number`
> Audi + deux `input_number` sommeil, les fenêtres d'aération, `internet_disponible`,
> `programme_chauffage`, et toute la famille énergie (prises + proxies + cumulus).

### 3.2 Population A **douteuse / à requalifier**

| Entité(s) | Problème | Résolution |
|---|---|---|
| **`sensor.temperature_max_journaliere_jardin`** | **Seule** entité taguée `OBLIGATOIRE` ; justifiée « source d'un `platform: statistics` ». **Aucun** `platform: statistics` du dépôt ne la source (0/443). Le capteur statistics « jardin » source `sensor.temperature_jardin`, pas la journalière. | Confirmer une éventuelle def **UI** ; à défaut, **justification fausse → reclasser Population B** (grandeur ≤ 1/jour, éligible de plein droit). |
| **15 capteurs énergie** | Pop A quasi-certaine (`total_increasing` + `utility_meter`), mais appartenance **Energy Dashboard** non vérifiable en YAML. | Confirmer côté UI ; le classement Pop A tient de toute façon par la LTS. |
| **`sensor.pluie_cumul_24h/48h/72h`** | **Sorties** `platform: statistics` (sourçant `pluie_total_local`, lui-même Pop A). Pop A seulement si consommées par une card `statistics_graph`. | À confirmer (UI) ; sinon **Pop B dérivé** légitime. |

### 3.3 Population B — reste (**228 entités**)

Non concernées par une dépendance Population A tracée. La majorité **reste sans bloc de
justification** (constat **C1** de l'audit initial, inchangé). Sous-catégorie **(ii)
« éligible LTS mais sans usage statistique actif démontré »** :

- `sensor.jardin_humidite_sol_{mediane,minimum,heterogeneite,points_frais}` — `state_class: measurement`,
  **aucun** `platform: statistics`/`history_stats` consommateur trouvé → **Pop B légitime**
  (et **déjà justifiés** par le bloc « Arrosage — canal réservoir sol »). `jardin_reservoir_sol_etat`
  n'a pas de `state_class` (état) → Pop B pur.
- `sensor.temperature_sejour_mean_10min/30min` — dérivées lissées, `state_class: measurement`,
  sans consommateur statistics → Pop B, **à justifier**.

---

## 4. Corrections à porter à l'audit initial

Ce delta **corrige** trois constats de `audit_recorder_conformite_contrat.md` :

| Constat initial | État | Correction |
|---|---|---|
| **C2** « capteurs d'énergie `total_increasing` non classés Pop A » | **Trop étroit** | Élargir : **95** entités Pop A par dépendance active (76 statistics + 4 history_stats + 15 énergie), pas 16. La voie dominante est `platform: statistics`, pas l'énergie. |
| **C3** « tag Pop A `temperature_max_journaliere_jardin` non tracé » | **Confirmé et durci** | 0 occurrence sur 443 sources statistics → justification **fausse** en l'état du dépôt (sauf def UI à confirmer). |
| **C4** « présomption fréquence > 5/h » sur CPU/mémoire (×4) + `ecart_consigne_instantane` (×3) | **Mal cadré** | Ces **7** entités sont **Population A** (sources statistics) : le contrat **accepte** leur coût logbook. Elles **sortent** de C4. Restent en C4 les seuls capteurs de **bruit** (maison + imprimerie), non-sources statistics. |

**Anomalie de classification majeure (A1/A2)** : sur **95** entités Population A, **aucune n'est
taguée** `OBLIGATOIRE` ; la **seule** entité taguée l'est **à tort**. Le contrat érige la
traçabilité de la Population A en garde-fou anti-dérive — l'écart est ici **inversé** (Pop A
massive non déclarée, tag existant non fondé).

---

## 5. Recommandations (non appliquées)

Aucune n'est appliquée par ce document. Ordre valeur/coût :

1. **RD1** — Taguer `# OBLIGATOIRE — contrainte HA` les **95** entités Population A confirmées
   (§3.1, Annexe A), en nommant la route (`platform: statistics` / `history_stats` /
   Energy-LTS). Coût mécanique, valeur de traçabilité maximale.
2. **RD2** — Trancher `sensor.temperature_max_journaliere_jardin` (def UI ? sinon → Pop B). Coût nul.
3. **RD3** — Confirmer côté UI : membres Energy Dashboard (15 énergie) et cards `statistics_graph`
   éventuelles (`pluie_cumul_*`).
4. **RD4** — Justifier la sous-catégorie (ii) Pop B restante (`temperature_sejour_mean_*`).
5. **RD5** — Reporter ces corrections dans C2/C3/C4 de l'audit contrat (fait conjointement à ce delta).

> Rappel doctrinal : « L'appartenance à [la Population A] doit rester exceptionnelle. » Ici, la
> Population A **est** structurellement large parce que le dépôt exploite massivement
> `platform: statistics` — ce n'est pas une dérive, c'est une **dépendance réelle non déclarée**.
> La mise en conformité consiste à **déclarer** l'existant, pas à retirer des entités.

---

## 6. Limites

- Établi à HEAD `5f3c98d` ; **périssable**.
- Energy Dashboard et cards `statistics_graph` **non vérifiables** hors `.storage` (§2).
- L'analyse retient l'**usage actif tracé en YAML** comme critère Pop A ; un capteur éligible LTS
  mais sans consommateur tracé est classé Pop B (§3.3), conformément au critère « effectivement
  utilisé » du contrat.
- **Aucune** modification runtime/contrat/recorder. Document d'aide à la décision, figé.

---

## Annexe A — Population A confirmée (95)

**Via `platform: statistics` (76)** — `input_number.audi_temperature_charge`,
`input_number.autonomie_audi_etron_full`, `input_number.sommeil_derniere_nuit_score`,
`input_number.sommeil_derniere_nuit_total`, `sensor.clim_consommation_estimee_energie`,
`sensor.co2_sejour`, `sensor.ecart_consigne_instantane`, `sensor.ecart_consigne_instantane_doux`,
`sensor.ecart_consigne_instantane_froid`, `sensor.home_assistant_core_cpu_percent`,
`sensor.home_assistant_core_memory_percent`, `sensor.home_assistant_supervisor_cpu_percent`,
`sensor.home_assistant_supervisor_memory_percent`, `sensor.humidite_absolue_{cave,chambre_arnaud,chambre_matthieu,chambre_parents,direction,entree,exterieur,garage,jardin,petite_maison,sdb_enfants,sdb_parents,sejour}`,
`sensor.humidite_relative_{bobst,cave,chambre_arnaud,chambre_matthieu,chambre_parents,direction,entree,exterieur,garage,jardin,komori,media,petite_maison,sdb_enfants,sdb_parents,sejour,stock_carton,stock_pf}`,
`sensor.pluie_total_local`,
`sensor.temperature_{bobst,cave,chambre_arnaud,chambre_matthieu,chambre_parents,commercial,compta,devis,direction,entree,exterieur,garage,jardin,komori,max_chambres,media,min_chambres,moyenne_maison,palier,petite_maison,qualite,sdb_enfants,sdb_parents,sejour,stock_carton,stock_pf}`,
`sensor.uptime_jours`,
`sensor.withings_{average_respiratory_rate_local,distance_travelled_today_local,steps_today_local,total_calories_burnt_today_local}`.

**Via `history_stats` (4)** — `binary_sensor.fenetre_ouverte_etage`,
`binary_sensor.fenetre_ouverte_rdc`, `binary_sensor.internet_disponible`,
`sensor.programme_chauffage`.

**Via énergie `total_increasing` — LTS + `utility_meter` (15)** —
`sensor.deshumidificateur_energy_proxy`, `sensor.lave_vaisselle_energy_proxy`,
`sensor.petite_maison_modbuslink_1_2_electric_energy_consumption`, `sensor.prise_bouclage_energy`,
`sensor.prise_box_energy`, `sensor.prise_buanderie_energy`, `sensor.prise_deshumidificateur_energy`,
`sensor.prise_jardin_energy`, `sensor.prise_lampe_sejour_energy`, `sensor.prise_lave_vaisselle_energy`,
`sensor.prise_onduleur_energy`, `sensor.prise_refrigerateur_energy`, `sensor.prise_sdb_enfants_energy`,
`sensor.prise_sejour_baies_vitrees_energy`, `sensor.refrigerateur_energy_proxy`.

---

*Fin du delta. Lecture seule — la mise en conformité consiste à déclarer une Population A réelle
non tracée, pas à retirer des entités.*
