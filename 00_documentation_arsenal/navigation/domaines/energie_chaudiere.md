# 🔋 Hub de domaine — Énergie chaudière

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Supervision du Bluetti AC180 comme alimentation tampon locale de la chaîne thermique. Assure la continuité électrique du domaine boiler et du chauffage en cas de panne secteur. **Contrat canonique : [`contrats/bluetti.md`](../../contrats/bluetti.md)** — nommé d'après le dispositif, non le domaine (voir vigilance). Un doc architecture. **Non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

- [`contrats/bluetti.md`](../../contrats/bluetti.md) — Contrat Arsenal — Domaine `energie_chaudiere` v1.3

## Architecture — « comment / pourquoi »

- [`infrastructure_puissance.md`](../../architecture/infrastructure_puissance.md) — Stratégie de disponibilité électrique Arsenal — continuité de gouvernance thermique sur défaillance réseau.

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : [`contrats/bluetti.md`](../../contrats/bluetti.md).
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v12_0_0`, `v13`.

## Liens croisés (sens & appartenance)

`energie_chaudiere` est un fournisseur de continuité électrique (amont) :

- **Boiler** — [`contrats/boiler/`](../../contrats/boiler/) ; alimentation de la chaîne boiler (aval direct).
- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; continuité thermique assurée (aval indirect).
- **Pannes secteur** — [`contrats/pannes/secteur/`](../../contrats/pannes/secteur/) ; contexte de défaillance électrique dans lequel le Bluetti intervient.

## Points de vigilance (non normatif)

- **`contrats/bluetti.md`** : nommé d'après le dispositif (Bluetti AC180), non d'après le domaine (`energie_chaudiere`). Seul contrat Tier-1 dont le nom de fichier n'identifie pas directement le domaine. Ce hub est la seule entrée établissant le lien domaine↔fichier.
- **`architecture/energie.md`** (racine `architecture/`) couvre la séparation des couches du monitoring énergie — appartient au domaine `energie` (dashboard), **pas** à `energie_chaudiere` (alimentation tampon). Noms proches, périmètres distincts.
- **Domaine non audité** : absent de `audits/index.md`. État de cycle.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
