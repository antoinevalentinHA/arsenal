# ARSENAL — Contrats · Panne secteur

Sous-domaine de `pannes/` : contrats normatifs de **résilience à une coupure
d'alimentation secteur** — socle et états, temporalité, conséquences sur le
chauffage et l'ECS, puis cycle de vie et signalisation.

## Documents du dossier

| Document | Rôle |
|---|---|
| [`10_socle.md`](10_socle.md) | Socle — définition, états et invariants de la panne secteur |
| [`11_temporalite.md`](11_temporalite.md) | Temporalité de la résilience électrique |
| [`20_chauffage_et_ecs.md`](20_chauffage_et_ecs.md) | Résilience thermique — chauffage et ECS |
| [`30_cycle_vie_et_signalisation.md`](30_cycle_vie_et_signalisation.md) | Cycle de vie et signalisation |

## Conformité — détection résolue, actions contextualisées (en production)

> **Non normatif — traces d'audit.**
> **Détection (résolu, P0)** — le signal canonique `binary_sensor.coupure_secteur` était dérivé de `sensor.prise_onduleur_voltage`, une prise connectée alimentée par le secteur **en amont de l'UPS** (donc non protégée par l'UPS), violant l'invariant « source observable pendant l'événement » du socle ([`10_socle.md`](10_socle.md)) : lors d'une coupure cette prise perd son alimentation et passe `unavailable`, et le défaut `float(230)` du template lisait cette indisponibilité comme « secteur présent » — la coupure n'était jamais détectée. **Correction P0 appliquée** (runtime `f963128`) — requalification sur témoins UPS/Bluetti, défaut `float(230)` supprimé. Audit : [`audit_panne_detection_coupure_secteur.md`](../../../audits/01_rapports/pannes/audit_panne_detection_coupure_secteur.md).
> **Actions (résolu, en production)** — doctrine des **deux réservoirs** appliquée : **UPS** (HA/box/réseau, *sobriété critique*) et **Bluetti** (électronique de la chaîne thermique gaz). En coupure : l'**ECS de secours** est un cycle **`desinfection`** (stockage thermique maximal) **borné par le budget SOC Bluetti** (déclenché si sortie AC active et SOC non critique) ; le **confort d'ambiance** est **conditionné par un veto** (besoin thermique réel + présence + SOC) et neutralisé sinon. À la sortie : réinitialisation ECS 10 °C (protégée par le verrou de cycle) + **réconciliation**. Les **remédiations** (reloads, reboot box, watchdog clim, reboot stations Netatmo) sont **inhibées pendant la panne** via le signal canonique `binary_sensor.panne_secteur_en_cours`. Contrats : [`20_chauffage_et_ecs.md`](20_chauffage_et_ecs.md), [`30_cycle_vie_et_signalisation.md`](30_cycle_vie_et_signalisation.md). Audit métier : [`audit_actions_mode_panne_secteur.md`](../../../audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md).

## Navigation

- [README du domaine pannes](../README.md)
- [Index des contrats](../../index.md)
- [Hub — pannes](../../../navigation/domaines/pannes.md)
