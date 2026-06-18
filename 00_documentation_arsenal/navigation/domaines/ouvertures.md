# 🪟 Hub de domaine — Ouvertures

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Observation des états de portes et fenêtres. Domaine purement observationnel : **« aucun pilotage, aucune décision »** (`global.md`). Fournisseur transversal : son état est consommé par alarme, aération, chauffage et climatisation. Trois contrats (global, interface alarme, redondance). Un document d'architecture dédié. **Domaine non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

- Contrat principal : [`global.md`](../../contrats/ouvertures/global.md) — observation seule, aucun pilotage, aucune décision.
- Interface alarme : [`alarme.md`](../../contrats/ouvertures/alarme.md) — contrat normatif alarme/ouvrants, **hébergé dans ce domaine** (voir vigilance).
- Redondance : [`redondance.md`](../../contrats/ouvertures/redondance.md)

## Architecture — « comment / pourquoi »

- [`architecture/ouvertures.md`](../../architecture/ouvertures.md)

## Audits & état

> **Domaine non audité** — aucun artefact d'audit dédié, absent de [`audits/index.md`](../../audits/index.md) comme domaine propre. Les 4 occurrences du mot « ouvert » dans l'index sont des mentions incidentes d'autres domaines (ECS, chauffage, vacances) — pas de section état ouvertures.
> Référence normative : [`contrats/ouvertures/global.md`](../../contrats/ouvertures/global.md).
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v15_8_3`, `v15_8_4`, `v15_8_7`, `v15_8_8` ; clôture **OUV-R1** en `v16_0_4` (normalisation N1 — maintien du dernier état valide à l'indisponibilité).

## Liens croisés (sens & appartenance)

Ouvertures est un **fournisseur transversal** (amont). Consommateurs principaux :

- **Alarme** — [`contrats/alarme/`](../../contrats/alarme/) ; consomme l'état des ouvrants d'entrée (aval). Interface gouvernée par [`contrats/ouvertures/alarme.md`](../../contrats/ouvertures/alarme.md) (propriétaire : ouvertures).
- **Aération / blocage chauffage** — [`contrats/aeration_blocage_chauffage/`](../../contrats/aeration_blocage_chauffage/) ; référence le contrat ouvertures comme interface externe (aval).
- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; consomme l'état fenêtres comme condition de blocage (aval).
- **Climatisation** — [`contrats/climatisation/`](../../contrats/climatisation/) ; consomme l'état fenêtres comme condition de blocage (aval).

> Cette liste couvre les consommateurs principaux — elle **n'est pas exhaustive** : l'état des ouvertures est une donnée transversale.

## Points de vigilance (non normatif)

- **`contrats/ouvertures/alarme.md`** est titré « Domaine : Sécurité / Alarme » mais hébergé dans le domaine ouvertures — l'interface alarme/ouvrants est gouvernée depuis ouvertures, pas depuis alarme. Anomalie de rattachement signalée, non corrigée.
- **Domaine non audité** : absent de `audits/index.md` comme domaine propre ; les 4 occurrences dans l'index sont incidentes.
- **Fournisseur transversal** : toute évolution du contrat ou des entités peut affecter alarme, aération, chauffage, climatisation.
- **Liens croisés non exhaustifs** (R5).

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
