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

## Écart de conformité connu (runtime)

> **Non normatif — trace d'audit.** Le signal canonique `binary_sensor.coupure_secteur` est actuellement dérivé d'un point **secouru par l'UPS** (`sensor.prise_onduleur_voltage`), ce qui **viole l'invariant « source observable pendant l'événement »** du socle ([`10_socle.md`](10_socle.md), § Invariants d'architecture). Une coupure réelle compensée par l'onduleur n'a pas été détectée.
> Audit : [`audit_panne_detection_coupure_secteur.md`](../../../audits/01_rapports/pannes/audit_panne_detection_coupure_secteur.md). **Correction P0 préparée, non appliquée.**

## Navigation

- [README du domaine pannes](../README.md)
- [Index des contrats](../../index.md)
- [Hub — pannes](../../../navigation/domaines/pannes.md)
