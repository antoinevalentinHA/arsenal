# 🚿 Hub de domaine — ECS

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Alimentation en eau chaude sanitaire. Sous-domaine : **bouclage** (recirculation ECS, non thermique). Chaîne d'audit par threads : watchdog (domaine ECS **non clôturé**) et bouclage (sous-domaine **clôturé**). Deux états d'audit coexistent dans ce hub.

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/ecs/`](../../contrats/ecs/) (colonne `00→11` + contrats d'implémentation).

- Fondations : [`00_fondations_et_statut.md`](../../contrats/ecs/00_fondations_et_statut.md) · [`02_gouvernance_autorites_et_chaine.md`](../../contrats/ecs/02_gouvernance_autorites_et_chaine.md)
- Watchdog : [`06_temps_timers_watchdogs.md`](../../contrats/ecs/06_temps_timers_watchdogs.md) · [`07_gardiens_et_securite_active.md`](../../contrats/ecs/07_gardiens_et_securite_active.md)
- Invariants : [`09_invariants_et_interdictions.md`](../../contrats/ecs/09_invariants_et_interdictions.md)
- Résilience : [`10_resilience_et_defaillances.md`](../../contrats/ecs/10_resilience_et_defaillances.md)
- Offsets : [`11_ajustement_des_offsets.md`](../../contrats/ecs/11_ajustement_des_offsets.md)
- Journalisation : [`08_journalisation_et_tracabilite.md`](../../contrats/ecs/08_journalisation_et_tracabilite.md)

> Les contrats d'implémentation (`ecs_*`, `automation_*`, `sensor_*`…) forment un groupe homogène ; leur liste exhaustive relèvera du futur index intra-famille.

**Sous-domaine — Bouclage** (recirculation ECS, non thermique) :
- Contrat **canonique** : [`contrats/bouclage.md`](../../contrats/bouclage.md) (arbitrage acté, runtime vérifié AUTO v2.3)
- [`contrats/ecs/04_bouclage_ecs_sous_systeme.md`](../../contrats/ecs/04_bouclage_ecs_sous_systeme.md) — **renvoi** vers le contrat canonique, sans doctrine autonome.

## Architecture

- Sous-domaine bouclage : [`architecture/bouclage.md`](../../architecture/bouclage.md)
- Aucune architecture dédiée au domaine ECS principal.

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md).
> État : domaine ECS **non clôturé** ; sous-domaine bouclage **clôturé**.

**Thread watchdog (ECS principal)** :
1. Rapport — [`audit_ecs_domaine.md`](../../audits/01_rapports/ecs/audit_ecs_domaine.md)
2. Contre-expertise — [`contre_expertise_watchdog_ecs.md`](../../audits/02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md) *(doctrine watchdog arrêtée ; ECS-WD-1 clos ; ECS-WD-2 requalifié)*
3. Arbitrage — [`arbitrage_watchdog_ecs.md`](../../audits/02_arbitrages/ecs/arbitrage_watchdog_ecs.md) *(décision rendue — acte terminal ; aucun chantier runtime watchdog)*
4. Backlog — [`backlog_ecs.md`](../../audits/04_chantiers/ecs/backlog_ecs.md)

**Thread offsets** (rapport seul) :
- [`audit_ecs_offsets.md`](../../audits/01_rapports/ecs/audit_ecs_offsets.md)

**Thread exposition diagnostique** (rapport seul, lecture seule) :
- [`audit_exposition_diagnostics_ecs.md`](../../audits/01_rapports/ecs/audit_exposition_diagnostics_ecs.md) *(exposition des diagnostics vs contrats ; 19 exigences opposables — bilan 10 CONFORME / 5 PARTIEL / 4 RUNTIME_MANQUANT ; 2 CONTRAT_AMBIGU hors chiffrage ; arbitrage normatif distinct non ouvert)*
- Chantier **C24** — [`chantier_securisation_parametres_ecs.md`](../../audits/04_chantiers/ecs/chantier_securisation_parametres_ecs.md) *(C24 clôturé le 2026-07-17 — sécurisation des paramètres ECS, écart I1 résorbé ; voir le [dossier de clôture](../../audits/05_clotures/ecs/cloture_c24_securisation_parametres_ecs.md))*

**Thread bouclage — clôturé** :
- [`audit_bouclage_ecs.md`](../../audits/01_rapports/bouclage/audit_bouclage_ecs.md) *(rapport final, clôturé)*

> **Changelog** (pas de chantier dédié) : mentions diffuses dans les snapshots `vXX` (v1, v4, v9, v13).

## Liens croisés (sens & appartenance)

- **Vacances** (désinfection retour VAC-IMP-5) — propriétaire : ECS ; vacances **consomme** (aval) → [`contrats/vacances.md`](../../contrats/vacances.md).
- **Boiler** (source thermique ECS) — propriétaire : [`contrats/boiler/`](../../contrats/boiler/) ; ECS **consomme** (amont).
- **Cumulus petite maison** — adjacent ECS (Tier 2) : [`contrats/cumulus_petite_maison.md`](../../contrats/cumulus_petite_maison.md).

## Points de vigilance (non normatif)

- **Double stage-2 inédit** : ECS est le seul domaine à employer séquentiellement `02_contre_expertises` *et* `02_arbitrages` pour le même thread. La contre-expertise est l'analyse ; l'arbitrage en est la résolution (acte terminal).
- **Deux états d'audit coexistants** : bouclage clôturé, ECS principal non clôturé.
- **Thread offsets** : rapport seul, pas d'aval documenté.
- **Aucun chantier runtime watchdog** : décision explicite de l'arbitrage (constaté, non manquant).

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas les contrats, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*
