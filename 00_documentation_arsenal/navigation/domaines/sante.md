# 🫀 Hub de domaine — Santé

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Monitoring santé : cardio nocturne et sommeil (intégration Withings). Domaine léger (2 contrats), conservé dans la carte pour explicitation. **Aucune architecture dédiée. Domaine non audité** (état de cycle). Le hub référence deux contrats de maturité distincte : `cardio_nuit.md` (READY FOR IMPLEMENTATION) et `sommeil.md` (v1.0 normatif, aligné runtime).

## Contrat — « ce que le système doit faire »

- Cardio nocturne : [`cardio_nuit.md`](../../contrats/sante/cardio_nuit.md) (v2.0.2 — **READY FOR IMPLEMENTATION**)
- Sommeil Withings : [`sommeil.md`](../../contrats/sante/sommeil.md) (v1.0 — **NORMATIF**)

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Références documentaires : `cardio_nuit.md` (READY FOR IMPLEMENTATION) et `sommeil.md` (v1.0 normatif, aligné runtime).
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v15`, `v15_3`, `v15_4`, `v15_7`.

## Liens croisés (sens & appartenance)

Aucun consommateur ou fournisseur documenté identifié dans les contrats existants.

## Points de vigilance (non normatif)

- **Maturité différenciée mais clarifiée** : `cardio_nuit.md` (v2.0.2, READY FOR IMPLEMENTATION) et `sommeil.md` (v1.0, normatif). `sommeil.md` porte désormais une autorité normative opposable ; `cardio_nuit.md` reste à traiter dans une passe dédiée.
- **`sommeil.md` est normatif (v1.0)** — réécrit et aligné sur le runtime réel ; à traiter comme contrat opposable.
- **Domaine léger** (Tier 1 par folderisation) : conservé dans la carte pour explicitation, pas pour la richesse de sa chaîne.
- **Aucune architecture dédiée.**

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
