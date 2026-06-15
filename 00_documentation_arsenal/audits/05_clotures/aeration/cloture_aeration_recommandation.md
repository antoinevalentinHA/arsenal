# Clôture — Audit Recommandation d'aération

- **Périmètre :** recommandation d'aération naturelle — capteurs `binary_sensor.aeration_preferable_rdc` / `…_etage` / `aeration_conseillee` et leur restitution UI. Contrat de référence : [`aeration_recommandation.md`](../../../contrats/aeration_recommandation.md).
- **Date :** 2026-06-15
- **Statut :** audit **CLÔTURÉ**. Correctif minimal appliqué et **validé runtime**. Chantiers résiduels **non bloquants** laissés ouverts (backlog).
- **Méthode :** audit lecture seule → passe corrective minimale ciblée (sans refonte, sans factorisation) → validation runtime côté Home Assistant → clôture documentaire.

---

## 1. Objet

Acter la fin de l'audit du moteur de recommandation d'aération. L'audit a conclu à un système **fonctionnellement pertinent et globalement conforme au contrat**, avec un défaut principal d'**explicabilité** (incohérence état ↔ motif dans le corner pluie + CO₂ fort) et plusieurs limites d'**observabilité UI**.

## 2. Règle normative actée

La **priorité sanitaire CO₂ prime sur la pluie**. En cas de `CO₂ ≥ seuil fort`, la recommandation est `on` même sous la pluie, avec motif `co2_priorite` et **jamais** `pluie_recente`. La hiérarchie de décision est **unique** et **cohérente** entre l'état, l'attribut `decision`, l'attribut `decision_globale` et l'icône. Détail et table de précédence : section *« Précédence normative — CO₂ vs pluie »* du contrat.

## 3. Travaux actés

| Unité | Objet | Nature |
|---|---|---|
| **P0-1** | Alignement de la hiérarchie état / `decision` / `decision_globale` / icône. `co2_priorite` hissé au-dessus de la pluie sur RDC, étage et global. | Capteurs templates `12_template_sensors/aeration/conseillee/{rdc,etage,global}.yaml` |
| **P1-5** | Synthèse globale rendue visible : `binary_sensor.aeration_conseillee` affiché en tête du dashboard aération (réutilisation de la carte existante via un alias `decision` = `decision_globale`, sans logique UI). | `18_lovelace/dashboards/aeration.yaml` + alias attribut sur `global.yaml` |
| **P2-1** | CO₂ rendu visible : affichage brut de `sensor.co2_rdc` et `sensor.co2_etage` (KPI générique, sans logique métier). | `18_lovelace/dashboards/aeration.yaml` |

> Aucun identifiant technique renommé, aucun accent ajouté aux ID, aucun réglage inerte modifié, aucune refonte.

## 4. État final mesuré (runtime)

Snapshot Home Assistant post-correctif (cas **canicule**, cohérent) :

- `binary_sensor.aeration_conseillee` = `off`
- `rdc_decision` = `canicule`
- `etage_decision` = `canicule`
- `decision_globale` = `canicule`
- `decision` (alias) = `canicule`
- `icon` = `mdi:weather-sunny-alert`

➡️ Confirme la **propagation de l'alias** (`decision` ≡ `decision_globale`) et la **cohérence** état / motif / icône. La correction du corner pluie + CO₂ fort a été prouvée par simulation lors de la passe corrective (motif `co2_priorite`, jamais `pluie_recente`).

## 5. Hors périmètre / différé — chantiers volontairement ouverts

Laissés ouverts **en connaissance de cause**, sans correction dans cette passe (aucun risque runtime) :

- **Logique métier résiduelle dans `carte_delta_ha`** : la carte recalcule un seuil saisonnier en JavaScript (fallback) — fuite de logique métier UI, contraire au contrat. À traiter en lecture seule d'attribut. *(P1-2, backlog)*
- **Réglages déclaratifs / inertes** exposés dans le dashboard réglages (`aeration_rain_max_mm`, hystérésis, durées) : présentés comme actifs mais non consommés par le moteur. À implémenter, marquer « inactif » ou retirer. *(P1-4, backlog)*
- **Absence de dashboard diagnostic dédié à la recommandation** : `seuils_utilises` / `decision` / disponibilité par niveau ne sont pas exposés dans une vue diagnostic propre (l'actuel `diagnostics/aeration` couvre le domaine physique/blocage). *(P2-4, backlog)*
- **Normalisation du `unique_id` étage** (`humidite_absolue_interieur_etage`, sans « e ») : incohérence latente avec son entity_id runtime et le sibling RDC. **À ne pas modifier sans validation runtime/registre** (un changement de `unique_id` peut recréer l'entité). *(P1-3, backlog, prudence)*
- **Factorisation future de la logique de décision** : le moteur ré-implémente la sélection de seuils plusieurs fois par capteur (source de divergence). **À traiter dans une passe séparée**, hors de cette clôture. *(P1-1, backlog)*

## 6. Critères de clôture (satisfaits)

- [x] P0-1 appliqué sur RDC, étage et global ; corner pluie + CO₂ fort prouvé corrigé.
- [x] Règle normative CO₂ > pluie consignée au contrat (table de précédence + invariant de cohérence).
- [x] P1-5 et P2-1 appliqués et validés runtime.
- [x] Chantiers résiduels documentés et classés backlog, sans risque runtime.

## 7. Contrôles post-clôture (documentaires)

    python scripts/docs_lint/docs_lint.py --exceptions scripts/docs_lint/docs_lint_exceptions.txt   # exit 0
    python scripts/docs_lint/docs_ci_contract_counts.py                                              # exit 0
    python scripts/docs_lint/docs_ci_orphan_report.py                                                # exit 0
    python scripts/docs_lint/docs_ci_naming.py                                                       # exit 0
    python scripts/docs_lint/docs_ci_navigation_leaf_pages.py                                        # exit 0

---

*Audit recommandation d'aération clôturé. Le contrat reste la référence normative unique ; les chantiers résiduels sont au backlog.*

## Navigation

- [Index des audits](../../index.md)
- [Contrat — Recommandation d'aération](../../../contrats/aeration_recommandation.md)
