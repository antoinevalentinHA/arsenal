# 💡 Hub de domaine — Éclairage

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Domaine éclairage couvrant 4 zones : entrée, jardin, garage, séjour. Chaque zone dispose de son ou ses contrat(s). **Architecture documentée pour la zone jardin uniquement** (cycles MATIN/SOIR, conditions de présence). **Domaine non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

- Entrée : [`entree.md`](../../contrats/eclairage/entree.md)
- Jardin : [`jardin.md`](../../contrats/eclairage/jardin.md)
- Séjour : [`sejour.md`](../../contrats/eclairage/sejour.md)
- Garage : [`garage.md`](../../contrats/eclairage/garage.md) *(`garage_implementation.md` coexiste — voir vigilance)*

## Architecture — « comment / pourquoi »

- [`eclairage_jardin.md`](../../architecture/eclairage_jardin.md) — Zone jardin : cycles MATIN/SOIR, déclencheurs de présence.

> Aucune architecture documentée pour les zones entrée, garage, séjour.

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : les contrats ci-dessus.
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : activité récente `v15_5_1`, `v15_6_1`, `v15_6_2`, `v15_7`.

## Liens croisés (sens & appartenance)

- **Présence** — [`contrats/presence.md`](../../contrats/presence.md) ; l'état de présence conditionne les cycles d'éclairage jardin (amont, documenté dans `eclairage_jardin.md`).

## Points de vigilance (non normatif)

- **`garage.md` et `garage_implementation.md`** partagent le même titre (« CONTRAT D'IMPLÉMENTATION — script.garage_toggle ») — doublon potentiel ou contenu différencié non évident depuis le nom de fichier. Signalé, non corrigé.
- **Architecture documentée pour la zone jardin uniquement** : aucune architecture pour les zones entrée, garage, séjour.
- **Domaine non audité** : absent de `audits/index.md`. État de cycle.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
