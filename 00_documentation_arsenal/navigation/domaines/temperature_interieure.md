# 🌡️ Hub de domaine — Température intérieure

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Fournisseur de mesure de température intérieure. Pipeline multi-couches : *capteurs bruts → consolidation (`temperature_brute_consolidee_<zone>`) → stabilisation (`temperature_stabilisee_<zone>`)*. Rôle pur de mesure — aucune décision thermique (appartient à chauffage / climatisation). Domaine propre, **physiquement logé sous `contrats/meteo/` par héritage** (arbitrage acté — voir [`carte_domaines.md`](../carte_domaines.md) §5.3). Aucune architecture-famille dédiée. Chaîne d'audit partielle (rapport → arbitrage → plan, pas de clôture).

## Contrat — « ce que le système doit faire »

Tous logés sous `contrats/meteo/` (héritage — domaine propre) :

- Axe : [`axe_temperature.md`](../../contrats/meteo/axe_temperature.md) (v1.1 — gouvernance de l'axe, sources et validation)
- Consolidation : [`temperature_interieure/consolidation.md`](../../contrats/meteo/temperature_interieure/consolidation.md) (v1.4 — `sensor.temperature_brute_consolidee_<zone>`)
- Stabilisation : [`temperature_interieure/stabilisation.md`](../../contrats/meteo/temperature_interieure/stabilisation.md) (v1.1 — `sensor.temperature_stabilisee_<zone>`)

## Audits & état

> **Source d'état faisant foi** : [`audits/index.md`](../../audits/index.md). État : chaîne partielle, domaine **non clôturé**.

1. Rapport final — [`audit_temperature_interieure_rapport_final.md`](../../audits/01_rapports/temperature_interieure/audit_temperature_interieure_rapport_final.md)
2. Arbitrage agrégats — [`arbitrage_temperature_interieure_agregats.md`](../../audits/02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md)
3. Plan d'action — [`plan_action_temperature_interieure_agregats.md`](../../audits/03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md)

> **Changelog** (pas de chantier dédié) : mentions diffuses `v12_1`, `v15_8_6`.

## Liens croisés (sens & appartenance)

Température intérieure est un **fournisseur de mesure** (amont). Consommateurs principaux :

- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; consomme la mesure pour les offsets ([`72_offsets_thermiques_lecture_physique.md`](../../contrats/chauffage/72_offsets_thermiques_lecture_physique.md)) et l'auto-ajustement de courbe ([`75_auto_ajustement_courbe.md`](../../contrats/chauffage/75_auto_ajustement_courbe.md)). Chauffage = aval.
- **Climatisation** — [`contrats/climatisation/`](../../contrats/climatisation/) ; consomme la mesure stabilisée pour ses seuils on/off en mode chaud. Climatisation = aval.

## Points de vigilance (non normatif)

- **Domaine propre logé sous `contrats/meteo/`** : héritage physique, pas la taxonomie (arbitrage acté — carte §5.3).
- **Distinction vs `meteo` (extérieure)** : `axe_temperature.md` (intérieure — ce domaine) ≠ `axe_temperature_jardin.md` (extérieure / meteo) — deux fichiers au nom similaire, cohabitant sous `contrats/meteo/`.
- **Chaîne d'audit partielle** : rapport → arbitrage → plan_action. Pas de chantier ni clôture.
- **Aucune architecture-famille dédiée** malgré un pipeline à 3 couches explicites.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
