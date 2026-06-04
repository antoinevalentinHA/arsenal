# 💨 Hub de domaine — Déshumidificateur

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Déshumidification de la cave. Deux contrats : comportement principal et garde d'exécution post-commande. Consomme la mesure d'humidité relative intérieure pour conditionner son activation. **Aucune architecture dédiée. Domaine non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

- Contrat principal : [`deshumidificateur.md`](../../contrats/deshumidificateur/deshumidificateur.md) — logique d'activation et seuils (Déshumidificateur Cave).
- Guard d'exécution : [`guard.md`](../../contrats/deshumidificateur/guard.md) (v1.0.2 — garde post-commande).

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : les deux contrats ci-dessus.
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v13_2`, `v15_7_1`, `v15_7_3`, `v15_8_7`.

## Liens croisés (sens & appartenance)

- **Humidité relative intérieure** — [`contrats/meteo/humidite_relative_interieure/`](../../contrats/meteo/humidite_relative_interieure/) ; fournit la mesure RH qui conditionne l'activation (amont).

## Points de vigilance (non normatif)

- **Domaine non audité** : absent de `audits/index.md`. État de cycle.
- **Domaine léger** (2 contrats) : Tier 1 par folderisation.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
