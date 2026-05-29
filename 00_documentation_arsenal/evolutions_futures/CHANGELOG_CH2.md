# Arsenal CI — Changelog du chantier CH-2

**Chantier** : CH-2 — Correction de la cascade de décision Chauffage (retrait de la branche Niveau 1)
**Domaine** : Chauffage
**Date** : 2026-05-29
**État** : clos — 103 tests verts, verdict décision conforme, GitHub Actions vertes, runtime déployé

---

## Résumé

CH-2 retire la branche Niveau 1 `not is_state('binary_sensor.chauffage_autorise_systeme', 'on')` des quatre cascades du domaine Chauffage, place `binary_sensor.chauffage_autorise_systeme` à l'état constant `on` (réservé à la sécurité système), et reclasse `input_boolean.chauffage_blocage_aeration` en cause Niveau 2 portée par la Décision Centrale. La raison runtime `chauffage_non_autorise` n'est plus émise ; le cas blocage post-aération émet `blocage_aeration_en_cours`. Le verdict CI de couverture s'évalue sur le runtime sans l'axiome `AX-D2`, conservé pour la fixture.

---

## 1. Runtime Chauffage

### Décision Centrale (`decision_centrale.yaml`)
- branche Niveau 1 retirée de `desired_mode` et de `reason`.
- raison `chauffage_non_autorise` plus émise.
- cas blocage post-aération : raison `blocage_aeration_en_cours` ; `desired_mode` reste `reduced`.

### Autorisation système (`autorisation.yaml`)
- `binary_sensor.chauffage_autorise_systeme` à l'état constant `on`, réservé à la sécurité système sans cause active.
- `input_boolean.chauffage_blocage_aeration` reclassé en cause Niveau 2.
- attributs et icône conservés.

### Diagnostics (`raison.yaml`, `mode.yaml`)
- branche Niveau 1 retirée de `sensor.chauffage_raison_calculee` et de `sensor.chauffage_mode_calcule`.
- cascades diagnostiques alignées sur la Décision Centrale.

---

## 2. CI — région décision

- `cli_decision` applique R-COV-1 au runtime sans axiome (`A=()`) ; import `AXIOMES_D2` retiré.
- `AX-D2` et `AXIOMES_D2` conservés pour la fixture `d2_reason_pre_correction.yaml`, inchangée ; provenance requalifiée en prémisse de fixture.
- snapshot G2 (`test_lot_2_7`) : `R-COV-1 == 0` sur le runtime.
- assertions de structure de cascade mises à jour dans `test_lot_2_1` (9 branches).

---

## 3. Documentation

- contrat `30_decision_centrale.md` : Niveau 1 marqué catégorie réservée sans cause active ; `chauffage_non_autorise` réservée, non émise ; raison `absence_protection_thermique` renommée `stabilisation_absence`.

---

## État de validation

- 103 tests Arsenal CI verts.
- verdict `cli_decision` conforme : R-COV-1 = 0, R-MIRROR-1 = [].
- GitHub Actions vertes.
- runtime déployé.

---

## Clôture du chantier CH-2

CH-2 est clos. La branche Niveau 1 est retirée des cascades décisionnelle et diagnostiques, `binary_sensor.chauffage_autorise_systeme` est réservé à la sécurité système, et le verdict de couverture porte sur le runtime sans axiome. La fixture reste gelée.
