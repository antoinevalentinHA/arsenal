# 🏠 Hub de domaine — Présence

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Présence maison — contexte global. Contrat normatif et opposable. Domaine **transversal** : il est consommé en amont par de nombreux autres domaines (alarme, vacances, chauffage, modes de présence). Deux documents d'architecture dédiés : présence générale et chaîne Wi-Fi. **Domaine non audité** (état de cycle — voir `carte_domaines.md`).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/presence.md`](../../contrats/presence.md) (mono-fichier — normatif et opposable).

## Architecture — « comment / pourquoi »

- [`architecture/presence/presence.md`](../../architecture/presence/presence.md) — architecture présence maison
- [`architecture/presence/wifi.md`](../../architecture/presence/wifi.md) — chaîne métier présence Wi-Fi

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, aucune source d'état d'audit disponible.
> Référence normative du domaine : [`contrats/presence.md`](../../contrats/presence.md) (normatif et opposable).
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses dans les snapshots `v15_8_3`, `v15_8_4`, `v15_8_5`, `v15_8_8`.

## Liens croisés (sens & appartenance)

Présence est un **fournisseur transversal** (amont). Consommateurs principaux :

- **Alarme** (armement selon présence) — [`contrats/alarme/`](../../contrats/alarme/) consomme (aval).
- **Vacances** (mode présence/absence) — [`contrats/vacances.md`](../../contrats/vacances.md) consomme (aval).
- **Chauffage** (absence / géofencing) — [`60_absence_inhibition_geofencing.md`](../../contrats/chauffage/60_absence_inhibition_geofencing.md) consomme (aval).

Modes dérivés de présence (Tier 2, consomment en aval) : [`simulation_presence.md`](../../contrats/simulation_presence.md) · [`mouvements.md`](../../contrats/mouvements.md) · [`visite.md`](../../contrats/visite.md) · [`babysitting.md`](../../contrats/babysitting.md).

> Cette liste couvre les consommateurs principaux — elle **n'est pas exhaustive** : présence est une dépendance implicite de nombreux autres domaines.

## Points de vigilance (non normatif)

- **Domaine non audité** : aucun artefact d'audit, absent de `audits/index.md`. État de cycle, pas un manque structurel.
- **Couplage transversal à fort impact aval** : toute évolution du contrat ou des entités de présence peut affecter silencieusement de nombreux domaines consommateurs.
- **Liens croisés non exhaustifs** (R5) : la liste ci-dessus ne recense pas tous les consommateurs.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
