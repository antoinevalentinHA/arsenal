# 🎨 Hub de domaine — UI / Lovelace

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Un domaine, deux façades : `ui/` (référence normative du design system Arsenal — couleurs, socle UI, patterns, architecture) et la chaîne d'audit Lovelace (arborescence, button-card templates, CI includes). Contrat : gouvernance des ressources frontend custom. Lovelace **absent de `audits/index.md`** (état faisant foi lu dans les rapports et chantiers). Domaine fusionné — arbitrage acté (voir `carte_domaines.md`).

## Contrat — « ce que le système doit faire »

**Référence normative de design — façade `ui/` :**

- Entrée : [`ui/README.md`](../../ui/README.md) (26 docs — design system normatif, s'impose à tous les dashboards)
- Architecture UI : [`ui/architecture.md`](../../ui/architecture.md) · [`ui/architecture_transverse.md`](../../ui/architecture_transverse.md) *(docs d'architecture dans la famille `ui/`, pas dans `architecture/`)*
- Socle UI (patterns) : [`ui/socle_ui/index.md`](../../ui/socle_ui/index.md)
- Couleurs : [`ui/couleurs/00_index.md`](../../ui/couleurs/00_index.md)
- Navigation : [`ui/navigation.md`](../../ui/navigation.md)

**Gouvernance ressources — façade Lovelace :**

- [`contrats/ressources_lovelace.md`](../../contrats/ressources_lovelace.md) (v1.2 — approvisionnement et figeage des ressources frontend custom)

## Architecture — « comment / pourquoi »

- [`architecture/00_structure_includes/18_lovelace.md`](../../architecture/00_structure_includes/18_lovelace.md) — structure du include dashboards
- [`architecture/00_structure_includes/button_card_templates.md`](../../architecture/00_structure_includes/button_card_templates.md) — structure button-card templates
- [`architecture/capteurs_couleur.md`](../../architecture/capteurs_couleur.md) — cartographie des capteurs producteurs des clés couleur consommées par les socles *(transverse ; non normatif)*

> `ui/architecture.md` et `ui/architecture_transverse.md` sont des docs d'architecture dans la **famille `ui/`**, pas dans `architecture/` — voir section Contrat ci-dessus.

## Audits & état

> Lovelace étant **absent de [`audits/index.md`](../../audits/index.md)**, l'état se lit dans les rapports et chantiers ci-dessous, et dans le changelog CH-LL-CI-1 (clos).

- Rapport arborescence — [`audit_lovelace_arborescence.md`](../../audits/01_rapports/lovelace/audit_lovelace_arborescence.md) *(contre-expertise de `evolutions_futures/lovelace_arborescence.md`)*
- Rapport button-card templates — [`audit_19_button_card_templates.md`](../../audits/01_rapports/lovelace/audit_19_button_card_templates.md) *(audit documentaire)*
- Chantier exploitation button-card templates — [`exploitation_audit_19_button_card_templates.md`](../../audits/04_chantiers/lovelace/exploitation_audit_19_button_card_templates.md)
- Cadrage CI includes (transverse CH-LL-CI-1) — [`cadrage_ci_includes_lovelace.md`](../../audits/04_chantiers/transverses/cadrage_ci_includes_lovelace.md)

## Changelog

- [`CHANGELOG_CH-LL-CI-1.md`](../../changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md) — **clos** (R-LL-INC-1 conforme, 290 cibles vérifiées). Série CH-LL-CI-n documentée au pivot [`registre_ch`](../pivots/registre_ch.md).
- Mentions diffuses : `v15_6_1`, `v15_7_2`, `v15_7_3`, `v15_8_0`.

## Liens croisés (sens & appartenance)

- **evolutions_futures** — [`evolutions_futures/lovelace_arborescence.md`](../../evolutions_futures/lovelace_arborescence.md) : le rapport arborescence en est une contre-expertise (propriétaire : evolutions_futures ; ui_lovelace audite en aval critique).

> La documentation `ui/` s'impose à tous les dashboards, toutes les cartes et tous les templates UI du système Arsenal (`ui/README.md`).

## Points de vigilance (non normatif)

- **`ui/architecture.md` et `ui/architecture_transverse.md`** dans la famille `ui/`, pas dans `architecture/` — ne pas confondre les deux familles.
- **Lovelace absent de `audits/index.md`** : anomalie signalée, non corrigée.
- **CH-LL-CI-1 clos (changelog) ≠ clôture formelle** du cycle d'audit lovelace.
- **Domaine fusionné** : ui + lovelace = une seule entrée Tier 1 (arbitrage acté).

---

*Hub de navigation non normatif (gabarit v2). N'énumère pas, ne duplique aucun contenu de famille, pointe les documents canoniques, signale les anomalies sans les corriger.*
