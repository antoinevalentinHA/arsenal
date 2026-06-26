# CONTRAT ARSENAL — ARROSAGE
## 12 — Capteurs d'humidité du sol (Zigbee) — relevé & doctrine d'observation

**Version contrat :** v0.1
**Statut :** **Factuel (relevé) + doctrine d'observation — antérieur au runtime.**
Ce document **constate** les capteurs d'humidité du sol Zigbee réellement appairés
dans Zigbee2MQTT / Home Assistant et **fixe la doctrine** qui borne leur usage. À
l'image de [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md), il
**ne crée aucune entité Arsenal** (helper, capteur dérivé, automation, script,
dashboard) et **ne fige rien** : il **relève** une surface réelle.

---

## 1. Principe — une couche d'observation, recensée sans être ratifiée

> **Invariant cardinal.**
> Les capteurs d'humidité du sol sont **d'abord une couche d'observation**.
> **Recenser une entité Zigbee ≠ en faire une entrée de décision Arsenal.**

- Ces capteurs **ne déclenchent pas seuls l'arrosage** et **ne remplacent pas**
  les préconditions Rain Bird ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md),
  [`10_prerequis_runtime.md`](10_prerequis_runtime.md)).
- Ils **alimenteront plus tard** l'entrée conceptuelle `‹humidite_sol_zone›` du
  **besoin hydrique** ([`04_besoin_hydrique.md`](04_besoin_hydrique.md) §2) : pour
  **qualifier le besoin** par zone, **comparer les zones**, **détecter excès / sec**
  et **préparer une décision supervisée** ([`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)).
- **Aucune automatisation d'arrosage** n'est créée tant que l'**observation terrain
  n'est pas stabilisée** (Phase 0, [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
  §2, T01–T06).
- Les `entity_id` ci-dessous **confirmés** sont **relevés** (exposés par
  Zigbee2MQTT), **non inventés** et **non figés comme entités Arsenal**. La doctrine
  « aucun `entity_id` Arsenal figé avant la Phase 0 » ([`README.md`](README.md))
  reste **intacte** : aucun de ces identifiants n'est un helper, un capteur dérivé,
  une automation ou un script Arsenal.

---

## 2. Nommage canonique des appareils

Trois sondes sont prévues, une par zone. Le **nom d'appareil** retenu dans
Zigbee2MQTT / Home Assistant est canonique :

| Zone | Nom d'appareil canonique |
|---|---|
| Zone 1 | `Jardin - Humidité sol - Zone 1` |
| Zone 2 | `Jardin - Humidité sol - Zone 2` |
| Zone 3 | `Jardin - Humidité sol - Zone 3` |

> Le **mapping zone ↔ station Rain Bird** **n'est pas** établi par ce nommage : il
> reste une **inconnue Phase 0** ([`07`](07_phase_0_terrain.md) T02,
> [`04`](04_besoin_hydrique.md) §5). Le numéro de zone du capteur est une étiquette
> d'inventaire, **pas** une affectation hydraulique.

---

## 3. Entités Zone 1 — **confirmées** (relevé réel)

Sonde **appairée**. Entités exposées telles que relevées dans Home Assistant :

| `entity_id` exposé | Type | Rôle (cf. §6) |
|---|---|---|
| `sensor.jardin_humidite_sol_zone_1_soil_moisture` | `sensor` | Observation hydrique (candidate besoin) |
| `sensor.jardin_humidite_sol_zone_1_temperature` | `sensor` | Observation secondaire |
| `number.jardin_humidite_sol_zone_1_celsius_degree_calibration` | `number` | Réglage technique manuel (interdit au runtime auto) |
| `number.jardin_humidite_sol_zone_1_fahrenheit_degree_calibration` | `number` | Réglage technique manuel (interdit au runtime auto) |

> **Statut : confirmé (appairé).** Ces quatre entités sont **relevées**, non
> inventées. Aucune n'est un actionneur ; aucune n'est consommée par une
> automatisation dans ce lot.

---

## 4. Entités Zone 2 / Zone 3 — **attendues par dérivation** (non confirmées)

> **Attendues, NON confirmées.** Les sondes Zone 2 et Zone 3 **ne sont pas encore
> appairées**. Les `entity_id` ci-dessous sont **déduits par dérivation** du
> schéma de nommage de la Zone 1 — ils **doivent être confirmés au relevé réel**
> après appairage, **jamais** traités comme acquis.

**Zone 2 (attendu) :**

- `sensor.jardin_humidite_sol_zone_2_soil_moisture`
- `sensor.jardin_humidite_sol_zone_2_temperature`
- `number.jardin_humidite_sol_zone_2_celsius_degree_calibration`
- `number.jardin_humidite_sol_zone_2_fahrenheit_degree_calibration`

**Zone 3 (attendu) :**

- `sensor.jardin_humidite_sol_zone_3_soil_moisture`
- `sensor.jardin_humidite_sol_zone_3_temperature`
- `number.jardin_humidite_sol_zone_3_celsius_degree_calibration`
- `number.jardin_humidite_sol_zone_3_fahrenheit_degree_calibration`

> Tant que l'appairage n'est pas fait, ces lignes restent une **prévision de
> surface**, pas un relevé. Distinguer **confirmé** (Zone 1) de **attendu**
> (Zone 2/3) est un invariant de ce document (§7).

---

## 5. Entités à relever après appairage complet — **ne pas inventer**

Plusieurs entités habituelles de ces sondes Zigbee (alimentation, lien, mise à
jour) **n'ont pas été relevées précisément** et **ne doivent pas être inventées** :

| Entité (rôle) | Statut | Observation connue |
|---|---|---|
| Batterie (`sensor.*_battery` ou diagnostic) | **à relever** | **100 %** vue dans les **diagnostics** de l'appareil (Zone 1) — `entity_id` exact non relevé |
| Linkquality (`sensor.*_linkquality` si exposé) | **à relever** | non relevé |
| Autres diagnostics Zigbee (LQI, dernière vue, etc.) | **à relever** | non relevé |
| Mise à jour firmware (`update.*` si exposé) | **à relever** | **update disponible** signalée (Zone 1), **non traitée** dans ce lot |

> **Honnêteté de relevé.** Une valeur **observée dans l'UI** (batterie 100 %,
> update disponible) **n'autorise pas** à écrire un `entity_id` supposé. L'`entity_id`
> exact de la batterie, de la linkquality et de l'`update` sera **relevé** après
> appairage complet — d'ici là, ces lignes restent **à relever**.

---

## 6. Table de mapping des zones — **à compléter**

Référentiel d'inventaire à compléter au fil des appairages et de la Phase 0. Les
cellules `à relever` / `à établir` ne sont **pas** des trous d'erreur : elles
**marquent** ce qui n'est pas encore un fait.

| Zone | Appareil Zigbee2MQTT | `entity_id` humidité | `entity_id` température | Batterie | Linkquality | Emplacement physique réel | Station Rain Bird concernée | Statut |
|---|---|---|---|---|---|---|---|---|
| Zone 1 | `Jardin - Humidité sol - Zone 1` | `sensor.jardin_humidite_sol_zone_1_soil_moisture` | `sensor.jardin_humidite_sol_zone_1_temperature` | à relever (100 % vu en diagnostic) | à relever | à relever | à établir (Phase 0 T02) | **confirmé (appairé)** |
| Zone 2 | `Jardin - Humidité sol - Zone 2` | `sensor.jardin_humidite_sol_zone_2_soil_moisture` *(attendu)* | `sensor.jardin_humidite_sol_zone_2_temperature` *(attendu)* | à relever | à relever | à relever | à établir (Phase 0 T02) | **attendu (non appairé)** |
| Zone 3 | `Jardin - Humidité sol - Zone 3` | `sensor.jardin_humidite_sol_zone_3_soil_moisture` *(attendu)* | `sensor.jardin_humidite_sol_zone_3_temperature` *(attendu)* | à relever | à relever | à relever | à établir (Phase 0 T02) | **attendu (non appairé)** |

---

## 7. État initial observé — Zone 1 (valeurs **non interprétables comme seuils**)

Premières valeurs relevées juste après appairage, **avant** pose dans le sol réel :

| Grandeur | Valeur initiale observée |
|---|---|
| Humidité sol | ≈ **33,33 %** |
| Température | ≈ **29,2 °C** |
| Batterie | **100 %** (vue dans les diagnostics de l'appareil) |
| Calibration humidité | **0 %** |
| Calibration température °C | **0** |
| Calibration température °F | **0** |
| Firmware | **mise à jour disponible — non appliquée** (hors périmètre) |

> **Ces valeurs ne sont PAS des seuils.** Elles décrivent un capteur **hors sol**,
> non encore représentatif. Aucune de ces valeurs ne fonde un seuil hydrique, un
> « sol humide / sec », ni une décision. Les **seuils d'humidité ne sont pas
> fixés** dans ce lot.

---

## 8. Classification doctrinale (par renvoi à [`09`](09_classification_entites.md))

Les sondes sol s'inscrivent dans la **taxonomie existante** du domaine
([`09_classification_entites.md`](09_classification_entites.md) §2), sans en créer
de nouvelle :

| Famille d'entité | Classe ([`09`](09_classification_entites.md)) | Sort vis-à-vis d'Arsenal |
|---|---|---|
| `sensor.*_soil_moisture` | **Observation** (hydrique candidate) | Lecture seule ; entrée pressentie du besoin ([`04`](04_besoin_hydrique.md)). Ne décide ni n'écrit jamais. |
| `sensor.*_temperature` | **Observation** (secondaire) | Lecture seule ; contexte, non moteur de décision. |
| Batterie / linkquality / diagnostics | **Observation** (supervision capteur) | Lecture seule ; santé du capteur, jamais une base d'action. |
| `number.*_calibration` (°C / °F / humidité) | **Interdit au runtime automatique** | **Aucune écriture automatique Arsenal.** Réglage technique **manuel**, réservé à une **intervention documentée** ([`11`](11_mode_manuel_supervise.md) §2.3 — paramètre borné, jamais un `number.…` librement piloté). |
| `update.*` firmware (si exposé) | **Interdit** (maintenance) | **Hors runtime arrosage.** Même doctrine OTA que le pont ([`09`](09_classification_entites.md) §3, [`07`](07_phase_0_terrain.md) T16). |

> **Aucun de ces capteurs n'est un actionneur.** Aucune sonde sol n'ouvre une
> station, ne pose un `rain_delay`, ni ne touche au secours Rain Bird.

---

## 9. Doctrine d'usage — observation d'abord, seuils plus tard

1. **Observation d'abord.** Les sondes servent à **observer**, pas à décider. Leur
   exploitation en besoin/intention relève d'un **lot ultérieur**, après Phase 0.
2. **Ne pas calibrer trop tôt.** **Aucune calibration** tant que les capteurs n'ont
   pas été **observés dans leur sol réel** : une correction appliquée hors sol
   fausserait durablement la mesure. La calibration **reste à observer avant toute
   correction**.
3. **Durée d'observation.** Observer **au moins 24–48 h** après pose, puis
   **idéalement plusieurs cycles météo / arrosage** ([`07`](07_phase_0_terrain.md)
   T03, T04) **avant** d'envisager des seuils.
4. **Pas de seuils figés.** Aucun **seuil hydrique final** n'est fixé ici ; les
   valeurs initiales (§7) ne sont **pas** des seuils.
5. **Firmware hors périmètre.** Les **mises à jour firmware** des sondes sont
   **hors de ce lot** (maintenance), même lorsqu'une update est signalée.
6. **Pas de décision d'arrosage.** Ce document **n'introduit aucune** chaîne
   besoin → exécution ; il **précède** [`04`](04_besoin_hydrique.md) côté perception
   et reste **en deçà** de [`05_intention.md`](05_intention.md).

---

## 10. Ce que ce document NE fait PAS

- ❌ il **ne crée** aucun template sensor, helper, automation, script ou
  dashboard ;
- ❌ il **ne calibre** aucun capteur et **n'applique** aucune mise à jour
  firmware ;
- ❌ il **ne fixe** aucun seuil hydrique ni aucune décision d'arrosage ;
- ❌ il **n'invente** aucun `entity_id` batterie / linkquality / `update` non
  relevé, ni aucune entité Zone 2 / Zone 3 confirmée ;
- ❌ il **ne ratifie** aucun mapping zone ↔ station Rain Bird (reste Phase 0) ;
- ❌ il **ne modifie** ni le runtime Rain Bird, ni Zigbee2MQTT.

---

## 11. Invariants

1. Les sondes sol sont une **couche d'observation** ; elles **ne déclenchent jamais
   seules** l'arrosage et **ne remplacent pas** les préconditions Rain Bird.
2. **Recenser ≠ ratifier** : un `entity_id` relevé n'est ni un helper Arsenal, ni
   une entrée de décision branchée.
3. **Confirmé** (Zone 1) et **attendu par dérivation** (Zone 2/3) ne se confondent
   **jamais** ; ce qui n'est pas relevé est marqué **à relever**.
4. Les `number.*_calibration` sont **interdits au runtime automatique** : réglage
   **manuel documenté** uniquement ; l'`update` firmware est **hors runtime
   arrosage**. **Aucun capteur sol n'est un actionneur.**
5. **Aucun seuil** hydrique n'est fixé ; les valeurs initiales (§7) ne sont pas des
   seuils ; la **calibration attend l'observation en sol réel**.
6. L'exploitation en **besoin par zone** reste subordonnée au **mapping Phase 0**
   ([`07`](07_phase_0_terrain.md) T02) et à la **stabilisation de l'observation
   terrain**.

---

## Renvois

- Besoin hydrique (consomme `‹humidite_sol_zone›`) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Observation & preuves (honnêteté d'état) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Phase 0 terrain (tests capteurs sol T01–T06) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Relevé factuel du pont Rain Bird (document sœur) : [`08_inventaire_pont_runtime.md`](08_inventaire_pont_runtime.md)
- Classification doctrinale des entités : [`09_classification_entites.md`](09_classification_entites.md)
- Pré-requis runtime (barrière de sortie) : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Mode manuel supervisé (réglage borné, jamais d'entité native libre) : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Index du domaine : [`README.md`](README.md)
