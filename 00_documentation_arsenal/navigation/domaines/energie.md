# ⚡ Hub de domaine — Énergie

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Sécurisation et exposition des données de consommation énergétique. Chaîne : *capteur brut → **proxy énergie sécurisé** → Dashboard Énergie → utility_meter*. Le contrat gouverne les sources admissibles (monotones, persistantes, sans régression) ; l'architecture définit la couche proxy intermédiaire qui garantit la monotonie et la persistance des compteurs avant toute exposition. Contrat mono-fichier. Un document d'architecture dédié. **Domaine non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/energie.md`](../../contrats/energie.md) (mono-fichier — sources admissibles et invariants du dashboard).

## Architecture — « comment / pourquoi »

- [`architecture/energie.md`](../../architecture/energie.md) — séparation des couches (acquisition → proxy sécurisé → dashboard → utility_meter) ; rôle et garanties de la couche proxy.

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, aucune source d'état d'audit disponible.
> Référence normative du domaine : [`contrats/energie.md`](../../contrats/energie.md).
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses dans les snapshots `v7`, `v12_3`, `v15_8_3`.

## Liens croisés (sens & appartenance)

- **energie_chaudiere** (Bluetti AC180) — [`contrats/bluetti.md`](../../contrats/bluetti.md) ; ses capteurs (tension secteur entrée) alimentent potentiellement le pipeline énergie (amont).
- **Batteries** — [`contrats/batteries.md`](../../contrats/batteries.md) ; capteurs d'état batterie admissibles comme sources énergie (amont).
- **Pannes** — [`contrats/pannes/`](../../contrats/pannes/) ; domaine adjacent : surveille la défaillance secteur que le dashboard énergie rend visible (pair).

> Hors périmètre de ce hub : résilience d'alimentation (`architecture/infrastructure_puissance.md`) — disponibilité vs consommation, concern distinct.

## Points de vigilance (non normatif)

- **Domaine non audité** : absent de `audits/index.md`, aucun artefact. État de cycle, pas un manque structurel.
- **Périmètre : monitoring de consommation** — ne pas confondre avec les domaines de résilience énergétique (`batteries`, `energie_chaudiere`, `pannes`).

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
