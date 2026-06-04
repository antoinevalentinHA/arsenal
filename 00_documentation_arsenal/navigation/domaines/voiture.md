# 🚗 Hub de domaine — Voiture

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Intégration des données du véhicule (Audi A3 e-tron) dans Arsenal : sécurisation, mémorisation, historisation et restitution. Contrat et architecture dédiés. Rapport d'audit final disponible (réconcilié runtime). **Domaine isolé** — aucun lien croisé documenté avec les autres domaines Arsenal.

## Contrat — « ce que le système doit faire »

- [`contrats/voiture.md`](../../contrats/voiture.md) — Contrat normatif Audi A3 e-tron

## Architecture — « comment / pourquoi »

- [`architecture/voiture.md`](../../architecture/voiture.md) — Chaîne canonique, ancrage dépôt, snapshot atomique.

> La section **« DETTE & POINTS D'ATTENTION »** de ce document incorpore les conclusions de l'audit du domaine.

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md). État : rapport final disponible, domaine **non clôturé** (pas de suite de cycle).

- Rapport final — [`audit_domaine_audi.md`](../../audits/01_rapports/voiture/audit_domaine_audi.md) — version finale réconciliée runtime.

> **Changelog** (pas de chantier dédié) : mentions diffuses `v15_5_1`, `v15_7_1`, `v15_7_2`, `v15_8_7`.

## Liens croisés (sens & appartenance)

Aucun consommateur ou fournisseur documenté identifié dans les autres domaines Arsenal.

## Points de vigilance (non normatif)

- **Domaine isolé** : aucun lien croisé documenté avec les autres domaines.
- **Audit partiel** : rapport seul — aucune suite de cycle (pas de plan_action, chantier, clôture). `architecture/voiture.md` incorpore les conclusions en section « DETTE & POINTS D'ATTENTION ».

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
