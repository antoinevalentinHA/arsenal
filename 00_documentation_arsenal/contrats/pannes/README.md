# ARSENAL — Contrats · Pannes

Ce dossier regroupe les contrats métier relatifs aux **pannes**, tels qu'ils
existent dans ce répertoire. Il est organisé en deux sous-systèmes :
**Internet** (pannes réseau) et **Secteur** (pannes électriques), chacun dans
son propre sous-dossier.

## Documents du domaine

### Internet (pannes réseau)

| Document | Rôle |
|---|---|
| [`internet/00_panne_internet_gouvernance.md`](internet/00_panne_internet_gouvernance.md) | Comportement normatif du système face aux pannes Internet — gouvernance |
| [`internet/10_campagne_remediation_internet.md`](internet/10_campagne_remediation_internet.md) | Campagne de remédiation comme unité logique |
| [`internet/20_execution_remediation_internet.md`](internet/20_execution_remediation_internet.md) | Règles d'exécution de la remédiation |
| [`internet/30_contexte_remediation_reseau.md`](internet/30_contexte_remediation_reseau.md) | Définition du contexte réseau-dépendant |
| [`internet/40_notifications_panne_internet.md`](internet/40_notifications_panne_internet.md) | Sémantique des notifications de panne Internet |

### Secteur (pannes électriques)

| Document | Rôle |
|---|---|
| [`secteur/10_socle.md`](secteur/10_socle.md) | Qualification d'une panne secteur et invariants système associés |
| [`secteur/11_temporalite.md`](secteur/11_temporalite.md) | Durées de confirmation normatives des transitions d'état |
| [`secteur/20_chauffage_et_ecs.md`](secteur/20_chauffage_et_ecs.md) | Effets métier autorisés d'une panne secteur sur chauffage et ECS |
| [`secteur/30_cycle_vie_et_signalisation.md`](secteur/30_cycle_vie_et_signalisation.md) | Cycle de vie et signalisation de la panne secteur |

## Navigation

- [Retour aux contrats](../README.md)
- [Index des contrats](../index.md)
- [Hub de navigation du domaine](../../navigation/domaines/pannes.md)
