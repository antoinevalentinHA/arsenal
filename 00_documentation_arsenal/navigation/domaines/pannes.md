# ⚡ Hub de domaine — Pannes

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Gestion des pannes critiques du système Arsenal. Deux sous-systèmes : **`internet/`** (panne internet — remédiation, notifications) et **`secteur/`** (panne secteur — résilience thermique, cycle de vie, signalisation). L'entrée documentaire se fait par ces deux sous-domaines : `internet/` pour les pannes réseau, `secteur/` pour les coupures électriques. Aucune architecture dédiée. **Domaine non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

**Panne internet :**
- Entrée : [`00_panne_internet_gouvernance.md`](../../contrats/pannes/internet/00_panne_internet_gouvernance.md) — gouvernance + pipeline remédiation (00→40)

**Panne secteur :**
- Entrée : [`10_socle.md`](../../contrats/pannes/secteur/10_socle.md) — socle résilience électrique + pipeline (10→30)

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : les deux entrées ci-dessus.
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v11`, `v13`, `v15_7_1`.

## Liens croisés (sens & appartenance)

- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; résilience thermique documentée dans `secteur/20_chauffage_et_ecs.md` (aval panne secteur).
- **ECS** — [`contrats/ecs/`](../../contrats/ecs/) ; idem (aval panne secteur).
- **UPS / arrêt HA** — [`contrats/ups_arret_ha.md`](../../contrats/ups_arret_ha.md) ; contrat connexe dans la racine `contrats/` — arrêt contrôlé de HA sur panne secteur.

## Points de vigilance (non normatif)

- **Aucun fichier racine** dans `contrats/pannes/` : ce hub est la seule porte d'entrée qui présente les deux sous-domaines ensemble.
- **Double préfixe `10_`** dans `secteur/` : **corrigé** — `10_temporalite.md` renommé `11_temporalite.md`, séquence désormais déterministe (10/11/20/30). _(Anomalie historique, résolue.)_
- **`resilience_electrique`** : nommage hérité après refonte du domaine `pannes` — **reroute exécuté** (B1, à plat vers `pannes/secteur/`). Plus aucune référence héritée dans les contrats. _(Anomalie historique, résolue ; trace : `audits/registre_anomalies_transverses.md` §1.4 + `audits/plan_action_anomalies_p1.md` Étape 6.)_
- **Domaine non audité** : absent de `audits/index.md`. État de cycle.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
