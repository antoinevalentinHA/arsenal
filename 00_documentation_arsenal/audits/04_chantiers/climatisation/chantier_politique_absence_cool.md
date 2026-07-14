# Chantier C20 — Politique d'absence COOL : veto immédiat Vacances + durée d'absence longue réglable

| Champ | Valeur |
|---|---|
| **Chantier** | **C20** — Politique d'absence COOL (veto immédiat Vacances + durée réglable + continuité physique) |
| **Domaine** | Climatisation — mode COOL : autorisation, absence, Vacances |
| **Statut** | **Ouvert — Lot 1 (contrats) mergé (#363), Lot 2 (checkers) mergé (#364), Lot 3 (runtime) livré, en revue (2026-07-14).** IDs C20 attribués. **Lot 3** : helper `input_number.clim_duree_absence_longue` (sans `initial:`), horodatage `input_datetime.clim_debut_absence` + automation écrivaine unique `10030000000122`, capteur d'extinction recomputé sur ancre horodatée + durée (timer `absence_longue_clim` **retiré**), vérité composite `binary_sensor.clim_veto_absence_vacances`, `autorisation_clim_cool` consomme le composite, diagnostics `clim_raison_decision`/`clim_verdict_cool` étendus (causes `vacances`/`absence_prolongee`/`absence_et_vacances`). **Gate live branché** : `tests/test_lot_5_2_cool_veto_runtime.py` (oracle sur le vrai runtime) + workflow `arsenal-ci-climatisation.yml` (bloquant) ; registre de couverture à jour (87 workflows). CI locale verte (arsenal_ci 169, yamllint, checkers clim/initial/ids/prefix). **Lot 3 mergé (#365).** **Lot 4 (dashboard) livré, en revue (2026-07-14)** : sous-section « ⏳ Absence longue » + tuile `input_number.clim_duree_absence_longue` dans `dashboards/climatisation/reglages.yaml` (affichage seul, checkers lovelace verts). **Lot 4 mergé (#366).** **Lot 5 (validation terrain) : protocole ouvert** ([`protocole_validation_terrain_absence_cool.md`](protocole_validation_terrain_absence_cool.md), 12 scénarios, lecture seule) — **aucune preuve recueillie, C20 non clôturable tant que la trace est vide.** |
| **Priorité** | **P2** — pas d'incident bloquant ; corrige un veto prématuré (départ Vacances non pris en compte immédiatement) et une durée non gouvernée. |
| **Note de décision** | [`cadrage_decision_politique_absence_vacances_cool.md`](../../02_conception/climatisation/cadrage_decision_politique_absence_vacances_cool.md) (D1–D7, D14–D15) |
| **Rapport d'audit source (mergé, intact)** | [`audit_absence_vacances_chauffage_climatisation_cool.md`](../../01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md) (#361) |
| **Plan d'action** | [`plan_action_politique_absence_vacances_cool.md`](../../03_plans_action/climatisation/plan_action_politique_absence_vacances_cool.md) |
| **Dépendance aval** | **C21** (préparation du retour) dépend de ce chantier |
| **Registre** | [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (ligne C20, co-commit) |

> **Nature de ce document.** Ouverture **formelle** et **gouvernance** : périmètre, décisions, invariants, critères d'acceptation, découpage en lots. Il **ne modifie aucun runtime, contrat, checker, UI ou entité** et **ne fige aucune correction**. Chaque lot fera l'objet d'un travail dédié avec point d'arrêt.

---

## 1. Objet

Corriger deux points de la politique d'absence COOL, sur la **seule autorité d'autorisation existante** `binary_sensor.autorisation_clim_cool`, **sans décision centrale** :

1. **Veto immédiat Vacances** (D1) : `binary_sensor.vacances_actives == on` doit interdire le COOL **sur-le-champ**, sans attendre l'écoulement du timer d'absence longue.
2. **Durée d'absence longue gouvernée et continue** (D3, D4, D5) : remplacer la durée figée de 8 h (`timer.absence_longue_clim`) par un **paramètre opérateur** persistant, avec **continuité physique** au redémarrage.

Ces deux causes de veto **coexistent** ; la préparation du retour (C21) en est la seule exception bornée.

---

## 2. Périmètre (inclus / exclu)

**Inclus :**
- consommation de `binary_sensor.vacances_actives` comme cause immédiate de veto COOL (couche autorisation) ;
- helper de durée d'absence longue — **ID à attribuer** (heures, sans `initial:`) ;
- horodatage de début d'absence — **ID à attribuer** — et échéance recalculée sur état (continuité physique, boot-proof) ;
- vérité intermédiaire du veto composite `(absence_longue OR vacances) AND NOT preparation` — **ID à attribuer**, calculée, sans écrivain ;
- diagnostics des **causes** de veto (extension de `sensor.clim_raison_decision` / `sensor.clim_verdict_cool`) : `vacances`, `absence_prolongee`, cumulé ;
- exposition du réglage de durée au dashboard Réglages climatisation (affichage seul) ;
- adaptation contractuelle et runtime correspondantes.

**Exclu (renvois) :**
- toute la **préparation du retour** → **C21** ;
- la **consigne de préparation** → C21 (D10) ;
- la dette `_reel` / garde opérateur `input_boolean.clim_blocage_absence_prolongee_actif` → **lot séparé** (D14), non intégré ;
- l'anticipation hors Vacances → **différée** (D15).

---

## 3. Invariants (opposables au futur contrat)

- **I-C20-1 — Autorité unique.** L'autorisation COOL reste `binary_sensor.autorisation_clim_cool`. Aucun second moteur, aucune décision centrale.
- **I-C20-2 — Effet immédiat Vacances.** `vacances_actives on` ⇒ veto COOL, indépendant du timer/durée/temps écoulé.
- **I-C20-3 — Coexistence sans conflit.** Les deux causes (absence longue, Vacances) produisent le même résultat et **coexistent** sans écrivain concurrent ; l'exclusion est un enjeu **de diagnostic**, pas de sûreté.
- **I-C20-4 — Continuité physique.** L'échéance d'absence longue est ancrée sur un horodatage de début et **recalculée au boot** ; **aucune remise à zéro arbitraire** au redémarrage.
- **I-C20-5 — Vérité composite sans écrivain.** La vérité intermédiaire du veto est **calculée**, jamais écrite ; source unique de la formule composite ; distincte de la dette `_reel`.
- **I-C20-6 — Pas de fallback silencieux.** Sources indisponibles / helper non restauré ⇒ repli **explicite** ; repli de lecture `float(<défaut>)` chez le consommateur du helper (doctrine `restauration_etat_helpers.md` R04).
- **I-C20-7 — UI non décisionnaire.** Le dashboard n'expose que le paramètre gouverné ; il ne porte aucune logique.
- **I-C20-8 — Périmètre du helper.** Le helper de durée gouverne **exclusivement** l'absence longue non qualifiée ; Vacances **ignore** ce seuil.

---

## 4. Critères d'acceptation

- Un départ Vacances qualifié coupe le COOL **immédiatement** (scénario S1 du plan) ;
- hors Vacances, la qualification d'absence longue survient **à l'échéance = début + durée helper**, réglable ;
- un redémarrage HA **ne réarme pas** la qualification à zéro (continuité physique) ;
- un changement de durée en cours d'absence est **pris en compte immédiatement** avec diagnostic explicite ;
- la formule composite est portée par **une** vérité calculée testable ;
- les diagnostics distinguent les **causes** ; l'UI n'affiche que ces états ;
- CI documentaire et checkers concernés verts ; contrat rédigé **avant** runtime.

---

## 5. Découpage en lots (détaillé dans le plan d'action)

1. **Contrat** — politique d'absence COOL (veto immédiat Vacances, durée gouvernée, continuité physique, vérité composite, bornes/granularité du helper).
2. **Checkers** — gate(s) de la nouvelle politique (présence de la cause Vacances, fail-closed, `initial` déjà couvert par CI).
3. **Runtime** — helper, horodatage, échéance recalculée, vérité composite, extension diagnostics, câblage dans l'autorisation.
4. **Dashboard** — exposition du réglage de durée (section « ❄️ Mode Cool »).
5. **Validation terrain** — S1–S3, S8–S9 (cf. plan).
6. **Clôture documentaire.**

---

## 6. Risques identifiés (à traiter en conception)

- **R1** — Vérité composite inline vs matérialisée : la note de décision retient la matérialisation (D7) pour l'observabilité ; arbitrage d'implémentation à confirmer au contrat.
- **R2** — `restore:` du timer devenu ambigu avec durée dynamique : à trancher (timer instrumental vs remplacement par horodatage).
- **R3** — Diagnostic des causes : ne pas recréer une décision parallèle ; rester en lecture d'états.

---

*Chantier ouvert — gouvernance seule. Aucune correction figée. Contrat avant runtime.*
