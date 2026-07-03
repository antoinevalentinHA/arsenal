# 💧 Hub de domaine — Arrosage

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Arrosage automatique du jardin, en **coexistence gouvernée** avec le contrôleur Rain Bird via un pont ESP32. Le domaine couvre : le **pont Rain Bird** (santé / disponibilité, observation), l'**observation hydrique** (canal réservoir sol), les **capteurs d'humidité sol** (trois points de mesure d'une zone unique), et la **supervision transverse** des sondes (batteries / LQI Zigbee). **La décision et l'action d'arrosage V1 sont livrées** (V1 automatique mono-station : besoin sol → intention → exécution déléguée au script Run supervisé, coexistence `rain_delay` minimale), aux côtés de la couche **observation / diagnostic v0** (canal réservoir sol).

## Contrat — « ce que le système doit faire »

- Index du domaine (porte d'entrée) : [`README.md`](../../contrats/arrosage/README.md) — doctrine, structure des contrats, chaîne conceptuelle.
- Coexistence Arsenal ↔ Rain Bird : [`03_coexistence_rainbird.md`](../../contrats/arrosage/03_coexistence_rainbird.md).
- Décision d'arrosage V1 (capacité livrée) : [`17_decision_v1.md`](../../contrats/arrosage/17_decision_v1.md).
- Observation hydrique (chapeau v0) : [`13_observation_hydrique_jardin.md`](../../contrats/arrosage/13_observation_hydrique_jardin.md).
- Capteurs humidité sol : [`12_capteurs_humidite_sol.md`](../../contrats/arrosage/12_capteurs_humidite_sol.md).

> Le README est la porte d'entrée et liste l'ensemble des contrats ; les ancres ci-dessus n'en sont qu'un point d'accès — voir l'index pour le détail.

## Réalisation runtime (technique, non détaillée)

- La couche d'observation / diagnostic v0 (canal réservoir sol, santé du pont) est réalisée sous `12_template_sensors/arrosage/`. La **V1 automatique** (décision besoin sol → intention, déclenchement, exécution supervisée, coexistence `rain_delay`) est réalisée sous `12_template_sensors/arrosage/`, `11_automations/arrosage/` et `10_scripts/arrosage/`. **Réalisation technique uniquement** : le *quoi* est fixé par les contrats, le *comment* relève du runtime ; non détaillée ici.

## Audits & état

> **Source d'état faisant foi** : le cockpit [`REGISTRE_CHANTIERS.md`](../../audits/REGISTRE_CHANTIERS.md) (ligne **C10**) — V1 automatique (décision / action) livrée ; observation v0 livrée.
> Artefacts d'audit : conception (cadrage besoin hydrique, plan d'observation v0) — voir [`cadrage_besoin_hydrique_decision_arrosage.md`](../../audits/02_conception/arrosage/cadrage_besoin_hydrique_decision_arrosage.md). Chaîne d'audit **partielle** (conception ; pas de clôture).

## Liens croisés (sens & appartenance)

- **Batteries** — [`contrats/batteries.md`](../../contrats/batteries.md) ; les sondes sol alimentent le périmètre canonique de supervision batteries (aval : produit par le domaine, consommé par la maintenance).
- **Connectivité Zigbee (LQI)** — [`carte_domaines.md`](../carte_domaines.md) (supervision transverse) ; les liens radio des sondes sont agrégés par la supervision LQI (aval).
- **Météo / pluie** — [`contrats/meteo/`](../../contrats/meteo/), [`volets_pluie.md`](../../contrats/volets_pluie.md) ; signaux pluie / climat **pressentis** comme modulateurs futurs (amont, hors v0).
- **Dépôt satellite (amont, gouverné)** — [`architecture/ecosysteme_depots_satellites.md`](../../architecture/ecosysteme_depots_satellites.md) §4.5 ; le pont Rain Bird est le firmware `rainbird-esp32-elegoo` (BLE⇄MQTT auto-discovery), relevé côté runtime par [`08_inventaire_pont_runtime.md`](../../contrats/arrosage/08_inventaire_pont_runtime.md).

## Points de vigilance (non normatif)

- **Décision / action V1 livrées** : le domaine est actionnable (V1 automatique mono-station) ; la calibration par l'observation (modulateurs) reste un chantier ultérieur.
- **Une zone Rain Bird, trois points de mesure** d'humidité (pas trois zones d'arrosage).
- **Chaîne d'audit partielle** : conception présente, pas de clôture ; l'état réel est porté par le registre (C10).

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
