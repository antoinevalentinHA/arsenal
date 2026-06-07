# Rapport d’avancement — Chantier « Couverture normative des domaines »

- **Périmètre :** suites de l’audit [`etat_couverture_normative_domaines.md`](etat_couverture_normative_domaines.md) (couverture normative des domaines fonctionnels).
- **Référence (photographie figée) :** l’audit initial, observé sur `main` @ `20d909df` (2026-06-07). Ce rapport d’audit **n’est pas réécrit** : il reste une photographie d’état opposable.
- **Statut :** point d’étape consolidé — **1 point P1 traité**, **1 divergence fermée** ; backlog de couverture toujours ouvert.
- **Méthode :** suites documentaires par patches atomiques validés CI (lint `docs_lint`). Aucun chantier métier nouveau ouvert ; aucune modification du runtime, des scripts ou des dashboards.

---

## 1. Périmètre et rattachement

L’audit `etat_couverture_normative_domaines.md` est une **photographie d’état** datée et épinglée à un commit. Pour préserver sa valeur d’opposabilité, il ne doit pas être édité au fil des corrections.

Ce document est le **point d’étape vivant** qui lui est rattaché, dans le même dossier `04_chantiers/transverses/`, suivant la convention déjà employée pour le chantier voisin [`etat_avancement_chantier_navigation_documentaire_contrats.md`](etat_avancement_chantier_navigation_documentaire_contrats.md). Il consigne : ce qui a été réalisé depuis l’audit, ce qui reste ouvert, et le prochain ordre de traitement. Il a vocation à être mis à jour, puis **clôturé** dans `05_clotures/` une fois le backlog résorbé.

## 2. Évolutions réalisées depuis l’audit

### 2.1 P1 — fichier vide trompeur `05_capteurs_parametrage_canonique.md` → contrat normatif

- **Constat audit (P1) :** `contrats/chauffage/15_capteurs/05_capteurs_parametrage_canonique.md` réduit à un titre (38 o, 1 ligne), donnant une fausse impression de couverture.
- **Réalisé :** réécriture en **contrat normatif complet** — frontière d’autorité « Paramétrage canonique » (références thermiques métier durables : consignes confort / réduite / vacances), entités et bornes ancrées sur `03_input_numbers/chauffage/consignes.yaml` et le registre, distinction explicite norme (contrat) / preuve d’exposition (dashboard `reglages/chauffage.yaml`).
- **Trace :** commit `bb50e76d` (`docs(chauffage): document canonical sensor parameterization`).
- **Statut :** **P1 clos.**

### 2.2 Divergence `input_number.chauffage_consigne_reduite_sauvegarde` — fermée

- **Constat audit / contrat 05 :** slot de sauvegarde réel présent dans `consignes.yaml`, absent de la section `parametres:` du registre et non exposé au dashboard ; laissé « à aligner ».
- **Réalisé :** entité **alignée** dans `contrats/chauffage/ci/registres_entites.yaml` (`role: parametre`, `exclus_invariants_registre`, contrat causal `66_adaptation_consigne_vacances.md`) ; **contrat 05 ajusté** pour acter l’alignement tout en maintenant le slot **hors** population canonique des références de régime (mémoire interne, non surface de réglage).
- **Traces :** commits `2a9bef67` (`align reduced setpoint backup registry`) et `1984ce09` (`mark reduced setpoint backup as registry-aligned`).
- **Statut :** **divergence close** côté registre **et** contrat.

> Note : l’indexation du rapport d’audit lui-même (gate orphelin DOC-CI-3) a été corrigée par le commit `879eb4a0`.

## 3. Reste ouvert — backlog de couverture normative

Les éléments ci-dessous restent ouverts ; ils renvoient aux listes compactes `DOMAINES_NON_DOCUMENTES`, `CONTRATS_DRAFT_OU_NON_NORMATIFS` et `FICHIERS_VIDES_OU_PLACEHOLDERS` de l’audit, qui demeurent la source détaillée.

| Priorité | Élément | Nature | État |
|---|---|---|---|
| P1 | `reveils` / `babyphone` | domaine actif non documenté | ouvert |
| P2 | `electromenager` | domaine actif non documenté | ouvert |
| P2 | `poele` | couvert indirectement (côté chauffage), pas de contrat souverain | ouvert |
| P2 | `sante/sommeil.md` | contrat draft `v0.9 (non validé)` | ouvert |
| P2 | `meteo/extrema_jour_courant.md` | pré-normatif `v0.1.0` à figer | ouvert |
| P2 | `meteo/fallback.md` | stub « à consolider » | ouvert |
| P3 | `chauffage/15_capteurs/12_capteurs_observabilite_pure.md` | stub déclaré vide | ouvert |
| P3 | `deshumidificateur/guard.md` (§12) | helpers diagnostiques « à créer » | ouvert |
| P3 | `sante/cardio_nuit.md` | statut `READY` + renvoi mort `CONTRAT_ALERTE_SANTE.md` | ouvert |
| P3 | `couleurs`, `boutons`, `statistiques` | rattachement à clarifier (architecture/UI vs contrat) | ouvert |
| P4 | `modes/normal` | renvoi à acter depuis `vacances.md` | ouvert |

## 4. Prochain ordre de traitement

1. **P1 — `reveils` / `babyphone` :** créer le contrat racine du domaine non documenté (prioriser `babyphone`, potentiellement sensible).
2. **P2 — contrats draft à figer :** `sante/sommeil.md` (→ v1.0), `meteo/extrema_jour_courant.md` (→ v1.0), `meteo/fallback.md` (consolider / fusionner).
3. **P2 — domaines à documenter :** `electromenager` (contrat léger), `poele` (contrat souverain **ou** renvoi explicite acté côté chauffage).
4. **P3 — consolidations :** `deshumidificateur/guard.md §12`, `sante/cardio_nuit.md` (statut + renvoi), arbitrage `12_capteurs_observabilite_pure.md`, clarification `couleurs` / `boutons` / `statistiques`.
5. **P4 — `modes/normal` :** renvoi depuis `vacances.md`.

Chaque suite suit le même principe : patch documentaire / registre atomique, validé CI, sans toucher au runtime, et **sans rouvrir l’audit figé**.

## 5. Portée et invariants de ce suivi

- L’audit initial n’est **pas modifié** (photographie d’état épinglée).
- Ce document est le **point d’étape** rattaché ; il est vivant et sera clôturé dans `05_clotures/` lorsque le backlog P1–P4 sera résorbé.
- **Aucun chantier métier nouveau** n’est ouvert : les suites sont strictement documentaires et de registre.
- Source de détail des éléments ouverts : les listes compactes de l’audit, non recopiées ici pour éviter toute divergence.
