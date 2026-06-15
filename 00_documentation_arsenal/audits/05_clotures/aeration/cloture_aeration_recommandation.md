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
- **Réglages déclaratifs / inertes** exposés dans le dashboard réglages : audit décisionnel mené, verdicts par helper et passe suivante préparés en **§ 5.1**. *(P1-4, backlog)*
- **Absence de dashboard diagnostic dédié à la recommandation** : `seuils_utilises` / `decision` / disponibilité par niveau ne sont pas exposés dans une vue diagnostic propre (l'actuel `diagnostics/aeration` couvre le domaine physique/blocage). *(P2-4, backlog)*
- **Normalisation du `unique_id` étage** (`humidite_absolue_interieur_etage`, sans « e ») : incohérence latente avec son entity_id runtime et le sibling RDC. **À ne pas modifier sans validation runtime/registre** (un changement de `unique_id` peut recréer l'entité). *(P1-3, backlog, prudence)*
- **Factorisation future de la logique de décision** : le moteur ré-implémente la sélection de seuils plusieurs fois par capteur (source de divergence). **À traiter dans une passe séparée**, hors de cette clôture. *(P1-1, backlog)*

### 5.1 Backlog — réglages déclaratifs (P1-4)

Audit décisionnel ciblé (références vérifiées par grep exhaustif). **Cause commune** des inerties : le moteur de recommandation est un **comparateur Jinja sans état** ; il ne peut honorer aucun réglage supposant une **mémoire d'état ou une temporisation** (anti-flapping, cadence, cap de durée).

| Helper | Statut runtime observé | Statut après passe de retrait (2026-06-15) |
|---|---|---|
| `aeration_duree_cible_minutes` | **Actif** — seuil d'affichage lu par `carte_duree_aeration` (dashboard principal) | ✅ **Conservé visible** (réglage d'**affichage**, hors moteur de reco) |
| `aeration_rain_max_mm` | Lu uniquement dans l'attribut `seuils_utilises` (affichage), **jamais** dans la décision | 👁️ **Masqué de l'UI**, **runtime conservé** (encore lu dans `seuils_utilises`) ; idée « porte pluie au cumul mm » au backlog |
| `aeration_hysteresis_ha` / `aeration_hysteresis_t` | **Non câblés** (aucun lecteur runtime) | 👁️ **Masqués de l'UI**, **runtime conservé** ; rattachés au chantier transverse [hystérésis 5 domaines](../../04_chantiers/transverses/hysteresis_5_domaines.md) |
| `aeration_intervalle_min_heures` | **Aucun** consommateur (def + UI réglages) | 🗑️ **Retiré du runtime** (helper + tuile supprimés) |
| `aeration_stabilisation_minutes` | **Aucun** consommateur (def + UI réglages) | 🗑️ **Retiré du runtime** (helper + tuile supprimés) |
| `aeration_duree_grand_froid_max_minutes` | **Aucun** consommateur (pas même `carte_duree_aeration`) | 🗑️ **Retiré du runtime** (helper + tuile supprimés) |

**Passe de retrait exécutée (2026-06-15)** :

1. **Retiré du runtime** — helpers sans aucun consommateur : `aeration_intervalle_min_heures`, `aeration_stabilisation_minutes` (fichier `03_input_numbers/aeration/conseil/system.yaml` supprimé, devenu vide) et `aeration_duree_grand_froid_max_minutes` (retiré de `duree.yaml`). Tuiles correspondantes retirées de `18_lovelace/dashboards/reglages/aeration.yaml`.
2. **Masqués de l'UI, runtime conservé** : `aeration_rain_max_mm`, `aeration_hysteresis_ha`, `aeration_hysteresis_t` (tuiles retirées du dashboard réglages ; définitions `input_number` inchangées). Le bloc « 🚧 Réglages déclaratifs » du dashboard est supprimé (devenu vide).
3. **Conservé visible** : `aeration_duree_cible_minutes` (réglage d'affichage actif).

**Reliquat résiduel (non traité ici, passe capteur dédiée)** : la ligne `rain_max` de l'attribut `seuils_utilises` dans `12_template_sensors/aeration/conseillee/{rdc,etage}.yaml` n'a **pas** été touchée (interdit dans cette passe). `aeration_rain_max_mm` reste donc référencé par ces capteurs — c'est la raison pour laquelle il a été **masqué et non supprimé**.

> ⚠️ Fait Home Assistant : supprimer un `input_number` supprime l'entité **et son historique recorder**. La présente fiche assure la **traçabilité de l'intention** avant tout retrait.



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
