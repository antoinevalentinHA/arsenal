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

## Conformité — détection résolue (P0), actions à arbitrer

> **Non normatif — traces d'audit.**
> **Détection (résolu, P0)** — le signal canonique `binary_sensor.coupure_secteur` était dérivé d'un point **secouru par l'UPS** (`sensor.prise_onduleur_voltage`), violant l'invariant « source observable pendant l'événement » du socle ([`10_socle.md`](10_socle.md)) ; une coupure réelle compensée par l'onduleur n'était pas détectée. **Correction P0 appliquée** (runtime `f963128`) — requalification sur témoins UPS/Bluetti, défaut `float(230)` supprimé. Audit : [`audit_panne_detection_coupure_secteur.md`](../../../audits/01_rapports/pannes/audit_panne_detection_coupure_secteur.md).
> **Actions (ouvert, P0 conception)** — la détection corrigée, les actions du mode panne restent **non contextualisées**. Analyse séparée : **ECS 45 °C = consommation réelle** sur batterie (toute saison) ; **chauffage confort = signal non gardé**, probablement inerte en été. Audit métier : [`audit_actions_mode_panne_secteur.md`](../../../audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md). **Sans patch runtime — doctrine à trancher.**

## Navigation

- [README du domaine pannes](../README.md)
- [Index des contrats](../../index.md)
- [Hub — pannes](../../../navigation/domaines/pannes.md)
