# ⚡ Hub de domaine — Pannes

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Gestion des pannes critiques du système Arsenal. Deux sous-systèmes : **`internet/`** (panne internet — remédiation, notifications) et **`secteur/`** (panne secteur — résilience thermique, cycle de vie, signalisation). L'entrée documentaire se fait par ces deux sous-domaines : `internet/` pour les pannes réseau, `secteur/` pour les coupures électriques. Aucune architecture dédiée. **Sous-domaine `secteur/` : audité (audit ciblé, voir ci-dessous)** ; sous-domaine `internet/` non audité.

## Contrat — « ce que le système doit faire »

**Panne internet :**
- Entrée : [`00_panne_internet_gouvernance.md`](../../contrats/pannes/internet/00_panne_internet_gouvernance.md) — gouvernance + pipeline remédiation (00→40)

**Panne secteur :**
- Entrée : [`10_socle.md`](../../contrats/pannes/secteur/10_socle.md) — socle résilience électrique + pipeline (10→30)

## Audits & état

**Panne secteur :**
- [`audits/01_rapports/pannes/audit_panne_detection_coupure_secteur.md`](../../audits/01_rapports/pannes/audit_panne_detection_coupure_secteur.md) — audit détection : coupure réelle non détectée (témoin sur point secouru UPS) ; **violation de l'invariant socle « source observable »** ; **correction P0 appliquée** (runtime `f963128`, requalification UPS/Bluetti).
- [`audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md`](../../audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md) — audit **métier** des actions : **doctrine des deux réservoirs** (UPS = HA/box/réseau, *sobriété critique* ; Bluetti = chaîne thermique). **ECS haute = stockage thermique utile** (pas une anomalie) ; le **confort d'ambiance** est le volet sacrifiable. Manque : **budget SOC Bluetti** + veto confort. Remplace la « sobriété batterie » globale. P0 doctrine. Indexé : [`audits/index.md`](../../audits/index.md).

**Panne internet :** non audité — référence normative : `internet/00_panne_internet_gouvernance.md`.

> **Changelog** (pas de chantier dédié) : mentions diffuses `v11`, `v13`, `v15_7_1`.

## Liens croisés (sens & appartenance)

- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; résilience thermique documentée dans `secteur/20_chauffage_et_ecs.md` (aval panne secteur).
- **ECS** — [`contrats/ecs/`](../../contrats/ecs/) ; idem (aval panne secteur).
- **UPS / arrêt HA** — [`contrats/ups_arret_ha.md`](../../contrats/ups_arret_ha.md) ; contrat connexe dans la racine `contrats/` — arrêt contrôlé de HA sur panne secteur.

## Points de vigilance (non normatif)

- **Aucun fichier racine** dans `contrats/pannes/` : ce hub est la seule porte d'entrée qui présente les deux sous-domaines ensemble.
- **Double préfixe `10_`** dans `secteur/` : **corrigé** — `10_temporalite.md` renommé `11_temporalite.md`, séquence désormais déterministe (10/11/20/30). _(Anomalie historique, résolue.)_
- **`resilience_electrique`** : nommage hérité après refonte du domaine `pannes` — **reroute exécuté** (B1, à plat vers `pannes/secteur/`). Plus aucune référence héritée dans les contrats. _(Anomalie historique, résolue ; trace : `audits/02_constats/transverses/registre_anomalies_transverses.md` §1.4 + `audits/03_plans_action/transverses/plan_action_anomalies_p1.md` Étape 6.)_
- **Audit** : sous-domaine `secteur/` désormais référencé dans `audits/index.md` (audit ciblé `panne_detection_coupure_secteur`) ; sous-domaine `internet/` non audité. État de cycle.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
