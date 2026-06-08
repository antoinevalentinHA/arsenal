# 🏭 Hub de domaine — Imprimerie

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Monitoring acoustique des machines industrielles d'**Imprimerie** : Bobst, Komori, Media. Trois contrats homogènes (Perception / Signal industriel) — conversion du signal brut en régime acoustique de chaque machine. Domaine **métier/professionnel**, distinct du périmètre résidentiel Arsenal. Aucune architecture dédiée. **Domaine non audité** (état de cycle). Conservé en Tier 1 pour explicitation (carte §6).

## Contrat — « ce que le système doit faire »

- Bruit Bobst : [`bruit_bobst.md`](../../contrats/imprimerie/bruit_bobst.md) (v1.0 — régime acoustique presse Bobst)
- Bruit Komori : [`bruit_komori.md`](../../contrats/imprimerie/bruit_komori.md) (v1.1 — régime acoustique presse Komori)
- Bruit Media : [`bruit_media.md`](../../contrats/imprimerie/bruit_media.md) (v1.0 — régime acoustique capteur Media)

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : les trois contrats ci-dessus.
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v13_2`, `v15`, `v15_7_1`, `v15_7_2`.

## Liens croisés (sens & appartenance)

Aucun consommateur ou fournisseur documenté identifié dans les autres domaines Arsenal.

> Note : les contrats `axe_humidite_relative_jardin.md` et `axe_temperature_jardin.md` (meteo jardin) excluent explicitement la zone imprimerie de leur périmètre — **clauses d'exclusion**, non des liens croisés.

## Points de vigilance (non normatif)

- **Domaine métier/professionnel** : spécifique à un contexte non résidentiel, isolé des autres domaines Arsenal.
- **Domaine non audité** : absent de `audits/index.md`. État de cycle.
- **Clauses d'exclusion meteo jardin** : la zone imprimerie a ses propres capteurs environnementaux, gouvernés séparément.
- **Domaine léger** (Tier 1 par folderisation) : conservé pour explicitation (carte §6).

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
