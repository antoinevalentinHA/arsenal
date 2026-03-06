# Arsenal — Cartographie des entités (v10.4)

> **Audit structurel** · Source : `core.entity_registry` (registre officiel Home Assistant), extrait via sauvegarde + analyse `jq`

---

## Chiffre fondamental

**3 398 entités persistantes structurées**

Ce chiffre représente uniquement les entités enregistrées, hors entités temporaires et hors runtime.

### Évolution depuis l'audit précédent

| Version | Entités | Évolution |
|---|---|---|
| Audit précédent | 3 066 | — |
| Arsenal v10.4 | **3 398** | **+332 (+10,8 %)** |

---

## Répartition par plateforme

| Plateforme | Volume |
|---|---|
| template | 1 099 |
| mqtt | 512 |
| mobile_app | 486 |
| automation | 195 |
| input_number | 149 |
| netatmo | 125 |
| script | 85 |
| input_boolean | 84 |
| input_datetime | 57 |
| input_text | 56 |
| hassio | 56 |
| homekit_controller | 55 |
| audiconnect | 48 |
| statistics | 46 |
| switchbot_cloud | 45 |
| roborock | 42 |
| withings | 40 |
| vicare | 39 |
| synology_dsm | 38 |
| timer | 30 |
| ping | 28 |
| overkiz | 25 |
| hacs | 15 |
| sun | 10 |
| input_select | 10 |
| fujitsu_airstage | 8 |
| backup | 5 |
| person | 4 |
| zone | 1 |
| uptime | 1 |
| time_date | 1 |
| rpi_power | 1 |
| met | 1 |
| html5 | 1 |

---

## Architecture en couches

### Couche Perception (~1 000 entités · ~30 %)

Entités provenant directement d'équipements physiques ou d'API cloud :
MQTT, Netatmo, Roborock, AudiConnect, ViCare, Synology DSM, Withings, HomeKit Controller, Ping.

---

### Couche Modèle (~1 530 entités · ~45 %)

Couche logicielle basée sur le calcul et la dérivation.

**Capteurs dérivés**

| Plateforme | Volume |
|---|---|
| template | 1 099 |
| statistics | 46 |

**Helpers persistants**

| Type | Volume |
|---|---|
| input_number | 149 |
| input_boolean | 84 |
| input_datetime | 57 |
| input_text | 56 |
| timer | 30 |
| input_select | 10 |

---

### Couche Orchestration (~280 entités · ~8 %)

| Type | Volume |
|---|---|
| automation | 195 |
| script | 85 |

---

## Ratio structurel

| Couche | Volume | Ratio |
|---|---|---|
| Modèle logiciel | ~1 530 | ~45 % |
| Perception terrain | ~1 000 | ~30 % |
| Orchestration | ~280 | ~8 % |
| Infrastructure / divers | ~588 | ~17 % |

---

## Indicateur notable

La plateforme `template` représente à elle seule **1 099 entités**, soit **32 % de l'ensemble du registre**.

Dans la majorité des installations Home Assistant, le nombre de templates est inférieur à 100. Arsenal possède donc une couche modèle **plus de dix fois supérieure à la moyenne**.

---

## Conclusion structurelle

Arsenal confirme une architecture **MODEL-DRIVEN dominante**, caractérisée par :

- une couche modèle logiciel très développée
- une perception terrain importante mais non dominante
- une orchestration relativement compacte

Cette structure indique que la logique métier est largement dérivée et centralisée, que les automatisations servent principalement d'orchestration, et que Home Assistant est utilisé comme **moteur d'exécution d'un modèle logiciel**.

> **Note :** Avec 3 398 entités, le système entre dans la zone où la croissance naturelle des entités devient exponentielle — phénomène classique dans les architectures model-driven, atteint par très peu d'installations Home Assistant.
