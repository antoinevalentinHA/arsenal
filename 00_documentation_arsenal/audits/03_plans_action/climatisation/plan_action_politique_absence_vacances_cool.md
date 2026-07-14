# PLAN D'ACTION — Politique estivale COOL : absence longue, Vacances, préparation du retour

> **Document de cadrage — aucune correction implémentée ici.**
> Traduit en lots actionnables les décisions **D1–D15** de la note de décision
> [`cadrage_decision_politique_absence_vacances_cool.md`](../../02_conception/climatisation/cadrage_decision_politique_absence_vacances_cool.md),
> pour les chantiers **C20** ([`chantier_politique_absence_cool.md`](../../04_chantiers/climatisation/chantier_politique_absence_cool.md))
> et **C21** ([`chantier_preparation_retour_vacances_cool.md`](../../04_chantiers/climatisation/chantier_preparation_retour_vacances_cool.md)).
> Source factuelle : rapport d'audit mergé (intact)
> [`audit_absence_vacances_chauffage_climatisation_cool.md`](../../01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md).
> **Aucun runtime, YAML, helper, checker, workflow ni contrat n'est modifié par ce plan.**

| Champ | Valeur |
|---|---|
| **Domaine** | Climatisation — COOL (absence / Vacances / préparation) |
| **Statut** | Cadrage — **aucune implémentation** |
| **Date** | 2026-07-14 |
| **Ordre Arsenal** | contrats → checkers → runtime → dashboard → validation terrain → clôture |
| **Découpage** | **Deux chantiers coordonnés** (C20 livrable seul ; C21 dépendant) + **un lot séparé** (dette `_reel`, D14) |

---

## 1. Découpage retenu et justification

**Deux chantiers plutôt qu'un** (D6/D9) : la **politique d'absence** (C20) est autonome et livrable seule ; elle **résout l'essentiel de l'incident** (départ Vacances qualifié + recalibrage de durée). La **préparation** (C21) s'appuie sur le veto composite défini par C20 — elle **dépend** donc de lui. Les mêler créerait un chantier trop large sans gain.

**Lot séparé** (D14) : la dette `_reel` / garde opérateur `input_boolean.clim_blocage_absence_prolongee_actif` **n'est pas** intégrée ; déjà tracée au backlog climatisation et à la vérification registre du 2026-06-17.

**Nouveaux rôles (aucun ID proposé — ID à attribuer par le propriétaire d'Arsenal)** : helper de durée d'absence longue ; horodatage de début d'absence ; vérité intermédiaire de veto composite ; vérité opérationnelle de préparation COOL ; helper de durée de préparation ; consigne de préparation ; diagnostic de préparation.

---

## 2. Chantier C20 — Politique d'absence COOL (lots)

| Lot | Étape Arsenal | Contenu | Décisions | Critère de sortie |
|---|---|---|---|---|
| **C20-L1** | **Contrat** | Politique d'absence COOL : veto immédiat Vacances ; durée gouvernée (bornes/granularité) ; continuité physique (horodatage + échéance recalculée, boot-proof) ; vérité composite `(absence_longue OR vacances) AND NOT preparation` ; fail-closed | D1,D3,D4,D5,D6,D7 | contrat rédigé, revu, opposable |
| **C20-L2** | **Checkers** | Gate(s) de la politique : présence de la cause Vacances dans l'autorisation ; fail-closed ; (rappel : `initial` couvert par CI existante `contracts_initial_key.yml`) | D1,D3 | checker vert, mutation vérifiée |
| **C20-L3** | **Runtime** | Helper de durée (sans `initial:`, repli `float`) ; horodatage de début d'absence + échéance recalculée sur état ; vérité composite calculée ; extension `sensor.clim_raison_decision`/`sensor.clim_verdict_cool` (causes) ; câblage dans `binary_sensor.autorisation_clim_cool` | D1–D7 | runtime conforme au contrat, CI verte |
| **C20-L4** | **Dashboard** | Exposition du réglage de durée (section « ❄️ Mode Cool », pattern `tile`+`numeric-input`) ; UI non décisionnaire | D3 | réglage visible, aucune logique en UI |
| **C20-L5** | **Validation terrain** | S1, S2, S3, S8, S9 (§4) | — | trace de validation remplie |
| **C20-L6** | **Clôture** | Bilan, mise à jour registre, clôture C20 | — | clôture prononcée |

---

## 3. Chantier C21 — Préparation du retour de Vacances (lots) — **après C20**

| Lot | Étape Arsenal | Contenu | Décisions | Critère de sortie |
|---|---|---|---|---|
| **C21-L1** | **Contrat** | Préparation COOL : fenêtre `[fin_vacances − durée ; fin_vacances]` ; gardes fail-closed ; neutralisation **sélective** du veto composite ; consigne dédiée ; durée transitoire ; boot ; `fin_vacances` (D13) ; fin de fenêtre (D12) | D8–D13 | contrat rédigé, opposable |
| **C21-L2** | **Checkers** | Gate(s) : écrivain unique de la préparation ; fail-closed ; neutralisation qui n'affecte **pas** les autres blocages | D9,D12,D13 | checker vert |
| **C21-L3** | **Runtime** | Orchestrateur + vérité de préparation (écrivain unique) ; fenêtre ; helper de durée de préparation ; consigne de préparation ; diagnostic de préparation ; câblage de la neutralisation | D9–D13 | runtime conforme, CI verte |
| **C21-L4** | **Dashboard** | Exposition durée de préparation + consigne de préparation ; UI non décisionnaire | D10,D11 | réglages visibles |
| **C21-L5** | **Validation terrain** | S4, S5, S6, S7, S10 + observation refroidissement réel (§4) | D11 | trace remplie |
| **C21-L6** | **Clôture** | Bilan, registre, clôture C21 | — | clôture prononcée |

---

## 4. Validation terrain (scénarios)

> **Avertissement.** Le passage à 14 h **supprime le mécanisme causal du veto prématuré** dans certains scénarios (S1), mais **le résultat thermique reste à valider**. Aucune garantie de confort n'est promise par le seul seuil.

| # | Scénario | Attendu | Chantier |
|---|---|---|---|
| **S1** | Départ 9 h, `vacances_actives on` 9 h 05, seuil 14 h, pas de préparation | **veto COOL immédiat à 9 h 05** (pas à 23 h) | C20 |
| **S2** | Très longue journée > seuil, sans Vacances | règles absence jusqu'au seuil, puis veto ; confort de retour **à observer** | C20 |
| **S3** | Week-end 48 h non déclaré, seuil 14 h | règles absence 14 h puis veto ; reprise réactive au retour | C20 |
| **S8** | Reboot **avant** puis **après** qualification / pendant Vacances | Vacances : veto reconstruit **immédiatement** ; absence : **continuité physique** (pas de remise à zéro) | C20 |
| **S9** | Changement du helper de durée pendant absence active | échéance recalculée immédiatement (raccourcie ⇒ qualification possible ; allongée ⇒ report) ; diagnostic explicite | C20 |
| **S4** | Vacances longues, `vacances_actives on` **et** absence qualifiée, fenêtre active | neutralisation du **veto global**, autres blocages actifs | C21 |
| **S5** | Retour réel pendant préparation | présence **terminale**, sortie Vacances, fin de préparation, règles présence | C21 |
| **S6** | Fin de fenêtre sans retour | préparation off ⇒ **veto réappliqué** ⇒ COOL off (pas de clim indéfinie) | C21 |
| **S7** | `fin_vacances` reculée / avancée pendant préparation | recul : arrêt + recalcul + réarmement possible ; avance : recalcul immédiat, éligibilité possible | C21 |
| **S10** | Clim indisponible, fenêtre active, retour imminent | **abstention** + diagnostic explicite ; présence reprend au retour | C21 |
| **Obs.** | Observation ultérieure du **temps réel de refroidissement** | données pour une future durée non-transitoire | C21 (suite) |

---

## 5. Critères d'entrée et de sortie

**Entrée (C20)** : décisions D1–D15 actées (note de décision) ; rapport d'audit mergé ; aucune dépendance amont.
**Entrée (C21)** : **C20 livré et validé** (veto composite disponible).
**Sortie (chaque chantier)** : contrat opposable + checkers verts + runtime conforme + réglage exposé + **validation terrain tracée** + clôture au registre (co-commit).

---

## 6. Hors périmètre (rappel)

- **Dette `_reel` / garde opérateur** (D14) — lot séparé, non ouvert ici.
- **Anticipation hors Vacances** (D15) — différée, chantier séparé si un jour ouverte.
- **Plafond thermique estival** (D8) — écarté faute de contrainte matérielle documentée.

---

*Plan d'action — cadrage. Aucune implémentation. Contrat avant runtime.*
