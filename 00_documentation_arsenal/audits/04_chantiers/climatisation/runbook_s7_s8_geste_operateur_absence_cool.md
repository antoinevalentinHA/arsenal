# Runbook — geste opérateur S7/S8 (C20, dernier verrou de clôture)

| Champ | Valeur |
|---|---|
| **Chantier** | **C20** — Politique d'absence COOL, Lot 5 (validation terrain) |
| **Objet** | Exercer **S7** (réduction du helper de durée pendant une absence active) et **S8** (augmentation), les **deux seuls scénarios non couverts** par l'analyse L4 |
| **Nature** | Acte opérateur (`set_value`), **~2 min**, en lecture d'Historique — aucun runtime/contrat modifié |
| **Pourquoi** | L'analyse L4 (`arsenal-runtime/analyses/c20_absence_cool_terrain_20260811`, reconfirmée le 2026-08-17) a démontré **9/12 scénarios PASS, 0 FAIL**. S7/S8 exigent un **changement de valeur du helper**, jamais survenu (durée restée à 14 h) ⇒ **aucun historique passif ne les produira**. C'est le **seul reste bloquant** de la clôture (S12 = lecture UI, L5, non bloquant). |

## Pré-requis : une absence active

Le geste n'a de sens que pendant une **absence longue en cours** — c'est-à-dire quand :
- `input_datetime.clim_debut_absence` porte un **horodatage réel** (≠ sentinelle `1970-01-01 01:00:00`) ;
- l'attribut `duree_ecoulee_h` de `binary_sensor.clim_extinction_absence_prolongee_autorisee` affiche des **heures écoulées** (noter cette valeur, ex. `E = 5 h`).

Se fait très bien **à distance** (app HA) lors d'une sortie de quelques heures. Si tout le monde est présent (`clim_debut_absence` = sentinelle), **attendre une absence** : le geste ne qualifie rien hors absence.

## S7 — réduction sous la durée écoulée ⇒ qualification immédiate

1. Relever `E` = `duree_ecoulee_h` (ex. 5 h) et l'état courant de `binary_sensor.clim_extinction_absence_prolongee_autorisee` (attendu `off` si `E < 14`).
2. Régler `input_number.clim_duree_absence_longue` **sous `E`** (ex. `E = 5 h` ⇒ mettre **3 h**).
3. **Attendu (immédiat)** :
   - `binary_sensor.clim_extinction_absence_prolongee_autorisee` → **`on`** ;
   - attribut `echeance` **recalculé** (≈ `debut_absence + nouvelle durée`, donc déjà dépassé) ;
   - `binary_sensor.autorisation_clim_cool` → **`off`** ; `sensor.clim_raison_decision` cohérent.
4. **Capturer l'Historique** de ces 3 entités autour de l'instant du réglage (preuve S7).

## S8 — augmentation ⇒ extinction différée

5. Régler `input_number.clim_duree_absence_longue` **au-dessus de `E`** (ex. **14 h**, ou plus).
6. **Attendu (immédiat)** :
   - `echeance` **repoussée** (≈ `debut_absence + 14 h`) ;
   - `binary_sensor.clim_extinction_absence_prolongee_autorisee` → **`off`** (si `E < 14 h`), extinction **différée** en conséquence.
7. **Capturer l'Historique** (preuve S8).

## Clôture

8. **Restaurer** `input_number.clim_duree_absence_longue` à sa valeur nominale (**14 h**).
9. Consigner les deux captures dans la trace §4 du protocole
   ([`protocole_validation_terrain_absence_cool.md`](protocole_validation_terrain_absence_cool.md)),
   passer **S7/S8 à PASS**, puis **clôturer C20** (co-commit registre).
10. La clôture de C20 **débloque mécaniquement C21** (préparation COOL du retour de Vacances, parqué en dépendance).

> **Fail-safe.** Aucun de ces réglages n'est dangereux : la durée revient à 14 h à l'étape 8, et
> la logique d'extinction est `fail-closed` (prouvé S11). En cas de doute, remettre 14 h : l'état
> se réévalue immédiatement sur l'ancre et la durée courantes.
