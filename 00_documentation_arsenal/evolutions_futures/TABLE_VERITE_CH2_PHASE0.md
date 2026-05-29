# Table de vérité avant/après — Gate Phase 0 (CH-2, Option A)

**Objet :** preuve d'iso-comportement avant diff. Gate bloquant (§8.1).
**Décision fail-safe actée :** **Option A** — `binary_sensor.chauffage_autorise_systeme` devient un **hook réservé pur, constant `on` (`true`)**.
**Source :** runtime `antoinevalentinHA/arsenal`, `HEAD 2f335a5`, 2026-05-29.
**Changement modélisé :** retrait de la branche N1 (`not autorise`) des 4 cascades + `state:` de `autorisation.yaml` constant `true`.

**Conventions de lecture :**
- Une **valeur unique** dans une cellule = **identique avant et après**.
- La notation **`avant → après`** = **changement** (les deux valeurs sont explicites).
- Chaque scénario **isole sa cause dominante** : toutes les conditions de priorité supérieure sont `off` (convention de table de vérité). Override = `off` sauf ligne 1.
- `desired_mode` ∈ {comfort, reduced, neutre} (script) ; `mode_calcule` ∈ {Confort, Eco, Neutre} (capteur diagnostic).

---

## 1. Table principale

| # | Cause dominante | `blocage_aeration` (entrée) | `chauffage_autorise_systeme` | `desired_mode` | `reason` | `mode_calcule` | Δ |
|---|---|---|---|---|---|---|---|
| 1 | Override opérateur | off | on → on | comfort | confort_force | Confort | — |
| 2 | Aération en cours confirmée | off | on → on | reduced | aeration_en_cours | Eco | — |
| 3 | **Blocage post-aération (nominal)** | **on** | **off → on** | reduced | **chauffage_non_autorise → blocage_aeration_en_cours** | Eco | **reason** |
| 4 | Fenêtre ouverte (avec délai) | off | on → on | reduced | fenetre_ouverte_maison | Eco | — |
| 5 | Vacances sans pré-confort | off | on → on | reduced | mode_maison_vacances | Eco | — |
| 6 | Vacances + pré-confort actif | off | on → on | comfort | pre_confort_vacances | Confort | — |
| 7 | Poêle actif | off | on → on | reduced | poele_actif | Eco | — |
| 8 | Présence, cible = comfort | off | on → on | comfort | besoin_thermique | Confort | — |
| 9 | Présence, cible = neutre | off | on → on | neutre | presence_on | Neutre | — |
| 10 | Présence, cible = reduced | off | on → on | reduced | confort_suffisant | Eco | — |
| 11 | Inhibition géofencing | off | on → on | comfort | stabilisation_absence | Confort | — |
| 12 | Défaut (absence nominale) | off | on → on | reduced | absence | Eco | — |
| 13 | **`blocage_aeration` unknown/unavailable — contexte par défaut** | **unknown / unavailable** | **off → on** | reduced | **chauffage_non_autorise → absence** | Eco | **reason** |
| 14 | **`blocage_aeration` unknown/unavailable + présence réelle (cible = comfort) ¹** | **unknown / unavailable** | **off → on** | **reduced → comfort** | **chauffage_non_autorise → besoin_thermique** | **Eco → Confort** | **desired_mode + reason + mode** |

¹ *Ligne représentative de l'edge dégradé avec une cause de confort active en aval. Comportement équivalent si l'inhibition géofencing est active à la place de la présence (`reduced → comfort`, `… → stabilisation_absence`).*

---

## 2. Synthèse des deltas (uniquement)

| # | Delta | Nature | Statut |
|---|---|---|---|
| 3 | `reason` : `chauffage_non_autorise` → `blocage_aeration_en_cours` | Réparation d'observabilité D2. `desired_mode` et `mode_calcule` **inchangés** (`reduced` / `Eco`). Iso-comportement thermique. | **Attendu — intentionnel** |
| 13 | `reason` : `chauffage_non_autorise` → `absence` | Edge dégradé, contexte par défaut. `desired_mode` (`reduced`) et `mode_calcule` (`Eco`) **inchangés** : le défaut de cascade reproduit fortuitement l'ancien repli. | **Attendu — exception Option A consignée** |
| 14 | `desired_mode` : `reduced` → `comfort` ; `reason` → `besoin_thermique` ; `mode_calcule` → `Confort` | Edge dégradé **avec** cause de confort active. Le repli conservateur accidentel (porté jadis par N1) **n'est plus appliqué** : la cascade descend jusqu'au niveau présence/géoloc. | **Exception Option A assumée — résiduel 4-1** |

**Aucun autre delta.** Les 11 lignes nominales hors blocage (1, 2, 4–12) sont **strictement identiques** avant/après sur les trois sorties.

---

## 3. Lectures de contrôle

- **Iso-comportement thermique nominal prouvé.** `desired_mode` est identique avant/après sur **toutes** les lignes nominales (1–12). L'unique delta nominal est la `reason` de la ligne 3 — précisément la réparation visée (la conséquence `chauffage_non_autorise` cède la place à la cause réelle `blocage_aeration_en_cours`), sans effet thermique.
- **Invariant `mode_calcule` (R7) confirmé.** Eco→Eco sur la ligne 3 ; aucune sortie diagnostic nominale ne bascule. Le puits diagnostic ne peut donc induire aucune régression de contrôle.
- **Coïncidence fixture (§8.1).** Le volet **avant** de la ligne 3 (`chauffage_non_autorise` dominant `blocage_aeration_en_cours`) **est** l'état pathologique gelé dans `d2_reason_pre_correction.yaml`. La table avant/après et la fixture canonique décrivent le même « avant » par deux artefacts distincts.
- **Edge dégradé — conséquence Option A.** Lignes 13–14 : `autorise` n'ayant plus aucun lecteur de décision, sa réécriture en constante ne porte plus le repli. L'edge suit la cascade : `reduced` tant qu'aucune cause de confort n'est active (13), `comfort` sinon (14). Exposition faible (`input_boolean`, fenêtre de redémarrage). Ligne consignée comme exigé (§8.6). Si une garantie de prudence est requise, elle se traite **à la couche décision** (token honnête), hors de ce correctif.

---

## 4. Verdict du gate

> ## ✅ GO — passage au diff autorisé.

**Conditions du GO, toutes satisfaites :**
1. `desired_mode` identique ligne à ligne sur le nominal (1–12). ✔
2. Unique delta nominal = `reason` de la ligne 3 (réparation d'observabilité, iso-thermique). ✔
3. Edge `blocage ∈ {unavailable, unknown}` explicitement décidé (Option A) et consigné (lignes 13–14). ✔
4. `mode_calcule` invariant sur le nominal (Eco→Eco ligne 3). ✔

**Réserve portée au GO (non bloquante) :** la ligne 14 matérialise la perte du repli conservateur accidentel sur l'edge dégradé. Elle est **GO sous Option A** parce qu'Antoine a acté cette option et l'exception associée. *Si ce comportement (`reduced → comfort` sur capteur aveugle) devait être refusé, le verdict basculerait en **STOP** jusqu'à implémentation d'une garde dégradée au niveau décision — ce qui n'est pas le cas retenu.*

**Le diff peut être préparé** selon le noyau atomique §2.1 du plan d'implémentation : retrait N1 dans les 4 cascades + `state:` constant `true` + triplet CI + contrat 30, en un commit réversible.

*Gate Phase 0. À archiver avec `PLAN_IMPLEMENTATION_CH2.md` et `REVUE_CLOTURE_CH2.md`. Runtime de référence : `HEAD 2f335a5`.*
