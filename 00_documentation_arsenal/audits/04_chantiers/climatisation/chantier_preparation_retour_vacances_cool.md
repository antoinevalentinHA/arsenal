# Chantier C21 — Préparation COOL du retour de Vacances (fenêtre bornée avant `fin_vacances`)

| Champ | Valeur |
|---|---|
| **Chantier** | **C21** — Préparation COOL du retour de Vacances |
| **Domaine** | Climatisation — mode COOL : préparation thermique du retour, contexte Vacances |
| **Statut** | **Réservé / parqué (2026-07-14) — dépend de C20.** Ouverture effective après livraison de la politique d'absence COOL (C20). Gouvernance seule, aucun runtime. |
| **Priorité** | **P3** — confort de retour de vacances ; sans incident bloquant ; dépendant. |
| **Dépendance amont** | **C20** — la préparation neutralise le **veto composite** défini par C20. Ne peut être livrée avant. |
| **Note de décision** | [`cadrage_decision_politique_absence_vacances_cool.md`](../../02_conception/climatisation/cadrage_decision_politique_absence_vacances_cool.md) (D8–D13) |
| **Rapport d'audit source (mergé, intact)** | [`audit_absence_vacances_chauffage_climatisation_cool.md`](../../01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md) (#361) |
| **Patron d'orchestration (référence, non copie)** | Pré-confort retour Vacances chauffage — [`contrats/chauffage/65_pre_confort_retour_vacances.md`](../../../contrats/chauffage/65_pre_confort_retour_vacances.md) |
| **Plan d'action** | [`plan_action_politique_absence_vacances_cool.md`](../../03_plans_action/climatisation/plan_action_politique_absence_vacances_cool.md) |
| **Registre** | [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (ligne C21, co-commit) |

> **Nature de ce document.** Réservation **formelle** et **gouvernance** d'un chantier **dépendant**. Il **ne modifie aucun runtime, contrat, checker, UI ou entité** et **ne fige aucune correction**.

---

## 1. Objet

Restaurer le confort **à l'approche du retour de Vacances** en ouvrant une **fenêtre bornée** avant `input_datetime.fin_vacances` pendant laquelle le **veto composite** (C20) est **temporairement neutralisé**, afin que la maison — laissée chauffer librement pendant le séjour (D8) — retrouve un confort approprié à l'échéance.

---

## 2. Périmètre (inclus / exclu)

**Inclus :**
- **fenêtre de préparation** `[fin_vacances − durée ; fin_vacances]`, calculée sur état, boot-proof ;
- **vérité opérationnelle de préparation COOL** — **ID à attribuer** — à **écrivain unique** (orchestrateur dédié, patron chauffage sans ses dettes) ;
- **helper de durée de préparation** — **ID à attribuer** — **réglable et explicitement transitoire** (D11) ;
- **consigne dédiée de préparation** — **ID à attribuer** — troisième contexte thermique (D10) ;
- **neutralisation bornée** du veto composite `(absence_longue OR vacances)` — jamais des autres blocages ;
- **diagnostic de préparation** dédié — **ID à attribuer** ;
- comportements : **boot** (recalcul idempotent), **modifications de `fin_vacances`** (D13), **fin de fenêtre sans retour** (D12), **présence réelle terminale**.

**Exclu (renvois) :**
- veto immédiat Vacances et durée d'absence longue → **C20** ;
- dette `_reel` / garde opérateur → lot séparé (D14) ;
- anticipation hors Vacances → différée (D15).

---

## 3. Gardes obligatoires de la préparation (fail-closed)

La vérité de préparation ne peut être active que si **toutes** les conditions suivantes sont vraies :
- `binary_sensor.vacances_actives == on` ;
- `input_datetime.fin_vacances` **valide** ; fenêtre **valide** (`début < fin`) ; **instant courant dans la fenêtre** ;
- système stable (recalcul post-boot) ;
- **non invalidée par override** opérateur ;
- **présence réelle non revenue** (adosser à `binary_sensor.presence_confort_thermique_stabilisee`, débruitée).

Toute valeur de préparation autre qu'un `on` franc (indisponible, non calculée) est traitée comme **« pas de préparation »** ⇒ **le veto tient** (fail-closed, sobriété par défaut, **pas de fallback silencieux**).

---

## 4. Invariants (opposables au futur contrat)

- **I-C21-1 — Écrivain unique.** La vérité de préparation a **un seul** écrivain (l'orchestrateur). `fin_vacances` reste propriété du domaine Vacances (lecture seule ici).
- **I-C21-2 — Neutralisation bornée et sélective.** La préparation neutralise **uniquement** `(absence_longue OR vacances)`, **jamais** aération / fenêtres / blocage horaire / température extérieure / indisponibilités.
- **I-C21-3 — Boot idempotent.** Fenêtre et état recalculés depuis `fin_vacances` au démarrage ; aucune activation fantôme.
- **I-C21-4 — Présence terminale.** Le retour réel effondre les causes et met fin à la préparation (D9).
- **I-C21-5 — Fin de fenêtre = retour au veto.** Fenêtre écoulée sans retour ⇒ préparation off ⇒ veto réappliqué (D12) ; pas de climatisation indéfinie.
- **I-C21-6 — Mémoire de cycle correcte.** L'anti-répétition protège une **fenêtre inchangée** ; une **modification explicite** de `fin_vacances` recalcule et peut réarmer (D13) — ne pas recopier la fragilité de réinitialisation sur bascule brute du patron chauffage.
- **I-C21-7 — Consigne dédiée.** La préparation vise une **consigne de préparation** propre (D10) ; la levée vers consigne d'absence n'est qu'une **variante transitoire assumée**, non la cible.
- **I-C21-8 — Transitoire assumé.** La durée de préparation est **réglable et transitoire** ; **aucune promesse** de température exacte à l'échéance (D11) tant qu'aucune observation de vitesse de refroidissement n'existe.

---

## 5. Critères d'acceptation

- Pendant le séjour hors fenêtre : COOL interdit (via veto C20) ;
- dans la fenêtre : veto composite neutralisé, COOL autorisé, **autres blocages toujours actifs** ;
- retour réel pendant préparation : reprise **régime présence** (terminale) ;
- fin de fenêtre sans retour : **veto réappliqué** ;
- recul/avance de `fin_vacances` : **recalcul** conforme à D13 ;
- reboot pendant préparation : **recalcul idempotent** ;
- diagnostic de préparation expose le cycle de vie (active / date invalide / terminée sans retour / clim indisponible) ; l'UI n'affiche que ces états.

---

## 6. Découpage en lots (détaillé dans le plan d'action)

1. **Contrat** — préparation COOL (fenêtre, gardes fail-closed, neutralisation sélective, consigne dédiée, durée transitoire, boot, `fin_vacances`, fin de fenêtre).
2. **Checkers** — gate(s) de la préparation (écrivain unique, fail-closed, neutralisation sélective).
3. **Runtime** — orchestrateur + vérité de préparation, fenêtre, helper de durée, consigne dédiée, diagnostic, câblage de la neutralisation.
4. **Dashboard** — exposition des réglages (durée de préparation, consigne de préparation).
5. **Validation terrain** — S4–S7, S10 (cf. plan) + observation ultérieure du refroidissement réel.
6. **Clôture documentaire.**

---

## 7. Risques identifiés (à traiter en conception)

- **R1** — Mémoire de cycle vs modification de `fin_vacances` (D13) : concevoir soigneusement pour éviter oscillation ou préparation manquée.
- **R2** — Absence de modèle de vitesse de refroidissement : la durée transitoire ne garantit pas le confort à l'échéance ; **observation terrain requise** avant toute ambition de cible horaire.
- **R3** — Clim indisponible pendant la fenêtre : abstention + diagnostic explicite ; confort non garanti ; présence reprend au retour.

---

*Chantier réservé/dépendant — gouvernance seule. Ouverture effective après C20. Contrat avant runtime.*
