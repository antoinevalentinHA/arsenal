# Dossier de conception — Lot L5
## Observabilité auto-ajustement courbe — Dérivation diagnostic & garde d'étanchéité

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception de lot (détaillé) |
| **Lot** | **L5** (phase **P5** du plan d'action) — *uniquement* |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception de lot — aucune implémentation |
| **Version** | 1.0 |
| **Date** | 2026-07-02 |
| **Amont figé** | `76_…md` (§3 Q6/Q8, §4, §10 INV-2/INV-6/INV-8) ; `plan_action_…md` (P5) ; `dossier_conception_observabilite.md` (CR-2, CR-7, CR-8) ; `dossier_implantation_…md` (É-8, É-11) ; lots **L1–L4** livrés |
| **Cadre** | Lecture seule. Aucun YAML, code ou patch. Aucun document figé rouvert. **L6 à L9 non traités.** |

> **Objet :** spécifier, sans implémentation, la **couche de dérivation diagnostic** — trajectoire confirmée & dérive nette, réversions, drapeau « nominal persistant » — répondant aux questions opposables **Q6** (la courbe a-t-elle dérivé ?) et **Q8** (un état nominal s'est-il installé durablement ?), **et** la **garde d'étanchéité CI** (INV-2, É-11). L'effet sur la régulation (corrélation avec oscillation/overshoot/cycles) reste **L6**.

---

## 1. Périmètre exact du lot L5

**Inclus (L5) :**
- **Trajectoire confirmée & dérive nette** (Q6, 76 §4, INV-6) : indicateur de **variation nette** de la pente et du parallèle **confirmés appliqués** sur une fenêtre à l'échelle saison — écart **É-8** (volet trajectoire).
- **Réversions** (Q6, support) : comptage des **inversions de sens** d'un ajustement appliqué par rapport au précédent, par paramètre — écart **É-8** (volet oscillation de la courbe).
- **Drapeau « nominal persistant »** (Q8, 76 §10 INV-8, conception CR-7) : signaler qu'un **état nominal s'installe durablement** (gel persistant, refus récurrent) **sans re-typer** le fait — écart **É-8** (volet persistance).
- **Garde d'étanchéité CI** (76 §9/§10 INV-2) : rendre **opposable** que nulle grandeur d'observabilité courbe (L1–L5) ne **réentre** dans la décision — écart **É-11**.
- **Persistance faible-cadence** des grandeurs L5 (miroir des blocs P3/P4 de `recorder.yaml`).

**Explicitement hors L5 (différé) :**
- **Effet par fenêtre régime** — corrélation trajectoire ↔ métriques de régulation (oscillation, overshoot, cycles) → **L6** (frontière §2).
- **Indicateur de convergence *par fenêtre régime*** (conception §6, « souhaitable ») : borde l'effet → **L6**. En L5, la convergence est **lue** de la dérive (→ 0) et du taux de réversions (bas), sans indicateur dédié.
- **Indicateur de divergence confirmé↔mesuré** (CR-2) : subordonné à l'existence d'un signal de relecture de courbe, **non acquis** (P0) → hors L5.
- Dashboard / logbook → **L7**. Validation globale / calibration → **L8**. Clôture → **L9**.

---

## 2. Frontière P5 (dérivation) vs P6 (effet) — décision structurante

- **Problème.** « Convergence » et « effet » peuvent se confondre : mesurer si les ajustements *se calment* (P5) vs s'ils *améliorent la régulation* (P6).
- **Décision.** L5 dérive **exclusivement des grandeurs propres de la courbe** — ses **valeurs confirmées** (trajectoire/dérive), le **sens de ses ajustements** (réversions), et la **persistance de ses causes** (drapeau). Il **ne lit aucune** métrique de régulation (oscillation, overshoot, cycles). La mise en regard avec la régulation — seule à même de dire si la dérive *a amélioré* quoi que ce soit — est **L6**.
- **Justification.** Cette frontière rend L5 constructible et honnête : il répond « la courbe a-t-elle bougé, et comment (net, oscillant, gelé) ? » (Q6/Q8), jamais « était-ce bénéfique ? » (Q5, P6). Respecte l'unité d'effet CR-4 (fenêtre régime, en L6) et borne la sur-promesse.

---

## 3. Fichiers concernés

| Fichier | Rôle dans L5 | Nature de l'intervention (logique) |
|---|---|---|
| **Nouveaux `sensor` (statistics)** — dérive pente / parallèle | Variation nette confirmée sur fenêtre saison | `platform: statistics` (`change`) sur les consignes historisées (P3) |
| **Nouveau `counter`** + mémoire de sens + **automation consommatrice** de `chauffage_adjustment` | Comptage des réversions par paramètre | Consommateur pur, en miroir de `log_auto_ajustement.yaml` / L4 |
| **Nouveaux dérivés** (template) + éventuel `counter` | Drapeau « nominal persistant » (gel persistant / refus récurrent) | `template` read-only sur le statut L4 persisté + comptage |
| **Nouveau validateur CI** `check_chauffage_courbe_observabilite_etancheite…py` + workflow | Garde d'étanchéité INV-2 (É-11) | Assertion statique : la décision ne lit aucune entité d'observabilité courbe |
| `recorder.yaml` | Historisation faible-cadence des grandeurs L5 | Sous-bloc Population B (miroir P3/P4) |
| `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml` | Chemin décisionnel | **Inchangé** (INV-1) ; sert de cible à la garde d'étanchéité |

Réutilisations : P3 (`input_number.chauffage_pente_consigne` / `…parallele_consigne` historisés = base de trajectoire) ; L4 (`input_select.chauffage_courbe_apprentissage_statut`, événements `chauffage_courbe_gel_episode`) ; patrons `13_sensor_platforms/statistics/`, `09_counters/`, et le patron de checker `scripts/arsenal_contracts/`.

---

## 4. Concept 1 — Trajectoire confirmée & dérive nette (Q6, INV-6)

### 4.1 Base de trajectoire : les valeurs confirmées appliquées (INV-6)
- La trajectoire opposable repose **exclusivement** sur des valeurs **confirmées appliquées** (76 INV-6, conception CR-2). Or `input_number.chauffage_pente_consigne` / `…parallele_consigne` **sont** ces valeurs (écrites par la décision, historisées en P3). Aucune valeur suggérée/rejetée n'entre dans la trajectoire.

### 4.2 Décision : dérive nette par `statistics` sur l'historique
- **Options.** (a) reconstruire la série par balayage d'historique (lourd, non requêtable en template) ; (b) **`platform: statistics`** avec `state_characteristic: change` (dernier − premier sur la fenêtre) sur chaque consigne.
- **Décision.** **(b)** — deux capteurs de **dérive nette** : `sensor.chauffage_courbe_derive_pente` et `…derive_parallele`, `change` sur une fenêtre **à l'échelle saison** (défaut **180 j**, paramétrable). La source (`…consigne`) étant historisée (P3), la fenêtre initiale est reconstruite depuis Recorder puis **densifiée en mémoire** au-delà de `purge_keep_days` (30 j) — la capacité saisonnière est livrée, la donnée mûrit (plan §6).
- **Justification.** Read-only, faible coût, honnête (net change = dérive). Conforme T06 du contrat Recorder (source historisée puisque `max_age > purge_keep_days`).

### 4.3 Limite consignée
- La dérive est **intentionnel-confirmé** (CR-2, chemin par défaut) : un changement de courbe **externe au boiler** resterait invisible faute de signal de relecture (P0 non tranché). Étiquetage explicite ; aucune promesse d'« effectif ».

---

## 5. Concept 2 — Réversions (Q6, oscillation de la courbe)

### 5.1 Définition opposable
- Une **réversion** est un ajustement **appliqué** dont le **sens** (hausse / baisse) est **opposé** au dernier ajustement appliqué **du même paramètre**. Beaucoup de réversions = courbe qui **oscille** ; peu = courbe qui **converge**.

### 5.2 Décision : comptage sur l'événement, mémoire de sens persistée
- **Options.** (a) inférer les réversions par balayage d'historique ; (b) **consommer `chauffage_adjustment`** (déjà porteur de `pente_before/after`, `para_before/after`, `pente_applied`, `para_applied`, `mode`) et détecter, à chaque **application réelle**, un changement de sens vs une **mémoire de dernier sens** persistée.
- **Décision.** **(b)** — une automation consommatrice (miroir L4) : pour chaque paramètre appliqué en mode réel, calcule `sens = sign(after − before)`, le compare au sens mémorisé (`input_text`/`input_select` `chauffage_courbe_dernier_sens_{pente,parallele}`), incrémente un `counter.chauffage_courbe_reversions` sur inversion, puis met à jour la mémoire. Simulation exclue (CR-9).
- **Justification.** Cadence cycle (~1/jour), pas de balayage d'historique, corrélable au cycle par `decision_id`. Le compteur cumulé + la dérive nette (§4) suffisent à **lire la convergence** sans indicateur dédié (INV-7).

---

## 6. Concept 3 — Drapeau « nominal persistant » (Q8, INV-8, CR-7)

### 6.1 Principe : signaler la persistance sans re-typer (CR-7)
- CR-7 / INV-8 : le tag `nominal|anomal` **par événement** est immuable ; une cause **nominale qui s'installe** lève un **drapeau séparé** « à surveiller ». On ne re-type **jamais** le fait.

### 6.2 Décision : deux facettes de Q8, un drapeau dérivé
- **Q8** énumère deux formes : **gel persistant** et **refus récurrent**.
- **Décision.** Un dérivé `sensor.chauffage_courbe_persistance` d'état fermé `{ ras, gel_persistant, refus_recurrent }` :
  - **gel persistant** — `input_select.chauffage_courbe_apprentissage_statut == gel` **depuis** plus d'un **seuil de durée** (défaut conservateur, paramétrable) : template lisant l'ancienneté de la transition (`last_changed` du statut L4).
  - **refus récurrent** — nombre de cycles **`suggestion_identique` consécutifs** au-delà d'un **seuil de récurrence** : `counter.chauffage_courbe_refus_consecutifs` (incrémenté sur `suggestion_identique`, remis à zéro sur toute **application**), alimenté par la consommation de `chauffage_courbe_cycle_evalue`.
- **Justification.** Répond exactement à Q8, garde le fait intact (les statuts/causes L4 ne changent pas), seuils **paramétrables** calibrés en P8. Priorité d'affichage : `gel_persistant` ≻ `refus_recurrent` ≻ `ras`.

### 6.3 Nuance
- `suggestion_identique` **persistant** peut refléter une courbe **saine et stable** aussi bien qu'un apprentissage **bloqué** ; le drapeau **signale**, il ne **juge pas** (le jugement relève du superviseur, avec l'effet L6). Sémantique « à surveiller », non « anormal ».

---

## 7. Concept 4 — Garde d'étanchéité CI (INV-2, §9, É-11)

### 7.1 Invariant à rendre opposable
- 76 §9 / INV-2 : le flux est **unidirectionnel** (capture → conservation → dérivation → présentation) ; **aucune grandeur d'observabilité ne réentre** dans la cascade de décision. Jusqu'ici **non instrumenté** (warn-only côté graphe chauffage).

### 7.2 Décision : validateur statique dédié, bloquant
- **Options.** (a) durcir le graphe `arsenal_ci` (lourd, warn-only par gouvernance) ; (b) **validateur dédié** `scripts/arsenal_contracts/` (bloquant), à l'image des gardes ECS récentes.
- **Décision.** **(b)** — un checker asserte que **`auto_ajustement.yaml`** (chemin décisionnel) **ne lit aucune** entité d'observabilité courbe (liste fermée L1–L5 : `chauffage_courbe_dernier_cycle`, `…apprentissage_statut`, `…gel_cause`, `…completude`, `…apprenant_num`, `…taux_jours_apprenants`, `…derive_*`, `…reversions`, `…refus_consecutifs`, `…persistance`, `…dernier_sens_*`). Vérifie aussi que les **consommateurs d'observabilité n'écrivent que de l'observabilité** (jamais une entrée de décision). Workflow dédié (patron uniforme `setup-python` épinglé + `python3`).
- **Justification.** Rend INV-2 **opposable et bloquant** sans rouvrir la gouvernance du graphe ; mutation-testable ; cohérent avec la doctrine des validateurs Arsenal.

---

## 8. Persistance L5 (rétention, CR-8)

Miroir faible-cadence des blocs P3/P4 de `recorder.yaml` (Population B) :

| Entité L5 | Classe | Cadence | Raison |
|---|---|---|---|
| `sensor.chauffage_courbe_derive_pente` / `…parallele` | **CRITIQUE** | faible | Trajectoire/dérive saisonnière (Q6) requêtable a posteriori |
| `counter.chauffage_courbe_reversions` | **IMPORTANT** | ≤ 1/jour | Oscillation de la courbe (Q6) |
| `sensor.chauffage_courbe_persistance` | **IMPORTANT** | rare | Drapeau Q8 sur historique |

- Les mémoires de sens et compteurs intermédiaires (`dernier_sens_*`, `refus_consecutifs`) sont **perdables/court terme** (CR-8) : seule leur conséquence porte du sens. Statistics `max_age` **saison** avec source historisée (P3) → conforme T06.

---

## 9. Critères de validation du lot L5

| # | Critère | Preuve attendue |
|---|---|---|
| V1 | **Trajectoire = confirmé appliqué** | La dérive se calcule **exclusivement** sur `…_consigne` (valeurs appliquées), jamais sur suggérées/rejetées (INV-6) |
| V2 | **Dérive nette correcte** | `change` sur la fenêtre reflète la variation nette de la courbe ; étiquetée « intentionnel confirmé » |
| V3 | **Réversion correcte** | Une application de sens opposé au précédent (même paramètre) incrémente le compteur ; même sens ne l'incrémente pas ; simulation exclue |
| V4 | **Persistance sans re-typage** | `gel_persistant` / `refus_recurrent` se lèvent au-delà des seuils ; les statuts/causes L4 **restent inchangés** (CR-7) |
| V5 | **Étanchéité opposable** | Le validateur échoue si `auto_ajustement.yaml` lit une entité d'observabilité courbe (INV-2) — **mutation-testé** |
| V6 | **Read-only** | Aucune entité lue par la décision n'est écrite par L5 (INV-1) ; `auto_ajustement.yaml` inchangé |
| V7 | **Rétention conforme** | Sous-bloc Recorder L5 passe `check_recorder_contracts.py` ; sources statistics historisées (T06) |

La validation **fonctionnelle globale** (8 questions) reste **L8**. L5 livre la capacité de **Q6** et **Q8**.

---

## 10. Risques de régression

| ID | Risque | Prob. | Impact | Maîtrise |
|---|---|---|---|---|
| RR-1 | Dérive lue sur valeurs non confirmées → fausse trajectoire | Faible | Élevé | Source = `…_consigne` uniquement (V1) |
| RR-2 | Réversion comptée en simulation → bruit | Moyenne | Moyen | Gate `mode == real` (CR-9), **V3** |
| RR-3 | Drapeau re-typant le fait nominal | Faible | Élevé | Drapeau **séparé** (CR-7), statuts L4 non modifiés (**V4**) |
| RR-4 | Une entité dérivée L5 relue par la décision | Faible | Élevé | **Garde CI dédiée** (Concept 4), **V5** |
| RR-5 | `max_age` statistics > purge sans source historisée → T06 | Moyenne | Moyen | Source P3 historisée ; **V7** |
| RR-6 | Perte de la mémoire de sens au reboot → fausse réversion | Faible | Faible | Mémoire persistée (restore), première application post-reboot neutre |
| RR-7 | Seuils de persistance mal calibrés | Moyenne | Faible | Défauts conservateurs, **paramétrables**, calibrés P8 |

---

## 11. Démonstration de respect du contrat 76

| Obligation 76 | Contribution de L5 |
|---|---|
| §3 Q6 (dérive) / §4 trajectoire confirmée / INV-6 | **Satisfait** : dérive nette sur valeurs confirmées |
| §3 Q8 (état nominal installé) / INV-8 | **Satisfait** : drapeau persistance (gel persistant / refus récurrent), sans re-typage |
| §6 (pas de re-typage) / CR-7 | **Respecté** : tag par événement immuable ; persistance = signal dérivé séparé |
| §9 / INV-2 (étanchéité) | **Rendu opposable** : garde CI bloquante (É-11) |
| §10 INV-4 (effet au niveau régime) | **Non abordé** — effet différé L6 (frontière §2) |
| §11 Validation globale | **Non traité** (L8) — L5 fournit V1–V7 locaux |

L5 **n'introduit aucun concept** hors contrat ; il réalise la couche **dérivation diagnostic** et instrumente l'étanchéité.

---

## 12. Démonstration INV-1 et INV-2

**INV-1 — Read-only.** L5 **ne rouvre pas** `auto_ajustement.yaml` ; il dérive depuis l'historique (P3) et les événements (L1) via des capteurs/consommateurs distincts. Aucune entité écrite par L5 n'est une entrée de décision (V6).

**INV-2 — Étanchéité.** Sens strictement unidirectionnel `capture (L1) → persistance (P3/L4) → dérivation (L5)`. Aucune grandeur L5 ne réentre dans la décision — et cette frontière devient **opposable et bloquante** par la garde CI (Concept 4, V5). La décision lit les **entrées brutes** (représentativité, suggestions, consignes), **jamais** un dérivé d'observabilité.

---

## Rattachement

- **Réalise :** le lot **L5** (phase P5) du plan d'action, au service du contrat `76` (§3 Q6/Q8, §4, INV-2/INV-6/INV-8) — écarts **É-8** (dérivation) et **É-11** (garde d'étanchéité).
- **Diffère explicitement :** L6 (effet par fenêtre régime, convergence/divergence par régime), L7–L9.
- **Ne rouvre :** aucun document figé ; la frontière P5/P6 est **tranchée** ici (§2).
- **Lecture seule :** aucune entité créée, aucun fichier modifié par ce dossier ; fichiers vérifiés sur HEAD courant.

*Dossier de conception L5 — 2026-07-02. Dérivation diagnostic & garde d'étanchéité uniquement. Aucun patch, aucun YAML, aucun code.*
