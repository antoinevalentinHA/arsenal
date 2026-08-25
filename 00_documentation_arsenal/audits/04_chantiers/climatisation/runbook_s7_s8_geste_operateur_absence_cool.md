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
- l'attribut `duree_ecoulee_h` de `binary_sensor.clim_extinction_absence_prolongee_autorisee` affiche des **heures écoulées** (noter cette valeur, `E`) ;
- **pour S7 uniquement : `E > 8 h`.** Le helper est borné à **`min: 8`** (contrat [`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md) §3 ; runtime `03_input_numbers/climatisation/absence/duree.yaml`). Descendre **sous `E`** est donc impossible tant que `E ≤ 8 h` : un `set_value` hors bornes est refusé. **S8 n'est pas soumis à cette contrainte.**

Le geste se fait très bien **à distance** (app HA), mais **S7 exige une absence de type journée entière** — une sortie de quelques heures ne suffit pas. Si tout le monde est présent (`clim_debut_absence` = sentinelle), **attendre une absence** : le geste ne qualifie rien hors absence.

## S7 — réduction sous la durée écoulée ⇒ qualification immédiate

1. Relever `E` = `duree_ecoulee_h` et l'état courant de `binary_sensor.clim_extinction_absence_prolongee_autorisee` (attendu `off` si `E < 14`).
2. Choisir une valeur `V` respectant **`8 ≤ V < E`** — bornes réelles du helper : `min: 8`, `max: 48`, `step: 1` — puis régler `input_number.clim_duree_absence_longue` à `V`.
   **Exemple exécutable** : `E = 11 h` ⇒ `V = 8`, `9` ou `10`.
3. **Attendu (immédiat)** :
   - `binary_sensor.clim_extinction_absence_prolongee_autorisee` → **`on`** ;
   - attribut `echeance` **recalculé** (≈ `debut_absence + nouvelle durée`, donc déjà dépassé) ;
   - `binary_sensor.autorisation_clim_cool` → **`off`** ; `sensor.clim_raison_decision` cohérent.
4. **Capturer l'Historique** de ces 3 entités autour de l'instant du réglage (preuve S7).

> **Fenêtre praticable : `8 h < E < 14 h`.** La borne basse est celle du helper (`min: 8`, ci-dessus) ; la borne haute est celle qu'énonce déjà l'étape 1 — au-delà de la durée nominale, l'extinction est **déjà** `on` avant le geste, et la transition `off → on` attendue à l'étape 3 n'est plus observable (seul le recalcul d'`echeance` le reste). Ni l'une ni l'autre n'est une règle nouvelle : elles découlent des bornes déployées et de l'attendu déjà écrit.

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
