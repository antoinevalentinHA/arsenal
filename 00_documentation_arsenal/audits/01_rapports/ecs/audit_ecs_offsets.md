# Audit Arsenal — ECS / Auto-ajustement des offsets

> **🧷 AVENANT (clôture ECS-OFF-1).** Le constat **`ECS-OFF-1`** (trajectoire d'apprentissage non observable) est **RÉSORBÉ** : chantier d'observabilité réalisé et committé — historisation `recorder` (offsets, données figées, `autocorrect_active`, traces) + section « Apprentissage des offsets » dans le dashboard Diagnostics ECS (synthèse lecture seule + courbes). Justifié par l'état réel du dépôt, non par l'intention. Les §5 et §6 ci-dessous sont conservés **verbatim** comme snapshot d'audit (état au moment de l'audit) ; ils ne sont pas réécrits. Autres constats inchangés : OFF-5 ouvert (→ chantier CI) ; risques assumés OFF-3/OFF-7 (désormais surveillables via les courbes) ; dettes documentaires OFF-2/4/6/8 résorbées (contrat `11`).

> Type : rapport d'audit ciblé — version d'archivage
> Portée : mécanisme d'apprentissage des offsets ECS (automation `10250000000019`, script `ecs_autocorrect_offsets`, helpers `ecs_off_*`, données figées de cycle, traçabilité, contrat `11_ajustement_des_offsets`).
> Mode : lecture seule — aucun runtime, contrat, YAML, CI ni UI modifié ; aucun patch produit.
> Référence dépôt : branche `main`, HEAD `372b8d7`.
> Limite de méthode : audit sur l'état committé de `main` (clone). Le runtime Home Assistant n'a pas été observé ; « comportement runtime » = déduit des sources + sémantique d'exécution Home Assistant. Les constats conditionnés à des valeurs réelles (pics capteur, fréquence des cycles) sont signalés comme tels.
> Principe directeur : *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Contexte

Le mécanisme d'auto-ajustement des offsets ECS est en production et jugé opérationnel ; aucun incident runtime connu. Cet audit ciblé évalue sa robustesse, sa stabilité, sa convergence, son bornage et son observabilité, sans présumer de défaut. Il ne cherche pas un bug à tout prix : la cible est l'identification de dérives lentes, d'hypothèses implicites, de biais d'apprentissage, d'absences de garde, d'angles morts d'observabilité et de risques non documentés.

## 2. Cartographie

| Couche | Élément | Rôle |
|---|---|---|
| Déclencheur | `11_automations/ecs/auto_ajustement_offset.yaml` (`10250000000019`) | Consomme `ecs_fin_cycle_signal`, appelle le script, acquitte le signal. Gardé par `ecs_autocorrect_active`. Aucun calcul. |
| Algorithme | `10_scripts/ecs/auto_correction_offsets.yaml` | Correcteur proportionnel discret, zone morte, clamp, quantification. |
| Mémoire (offsets) | `03_input_numbers/ecs/offset.yaml` : `ecs_off_{tiny,medium,normal,desinfection}` | Stockage persistant borné ; `initial` commenté → restauration au reboot. |
| Gate | `05_input_booleans/ecs/autocorrection.yaml` : `ecs_autocorrect_active` | Active/désactive l'apprentissage. |
| Entrées figées | `ecs_resume_dernier_cycle_fige` (`date\|mode\|consigne\|t0\|boost\|valide`), `ecs_duree_dernier_cycle_figee`, `ecs_temperature_max_reelle_figee` | Produites/figées par `11_automations/ecs/inertie/gel.yaml`. |
| Trace | `04_input_texts/ecs/logs/dernier_ajustement_auto.yaml` : `ecs_dernier_ajustement` | 1 entrée (255 car.), non historique par conception. |
| Contrat | `contrats/ecs/11_ajustement_des_offsets.md` | Algorithme opposable. |
| CI | `check_ecs_cycle.py` T06/T07/T08 ; `check_ecs_securite.py` T12 | Testent la plomberie du signal + la gate ; pas l'algorithme. |

**Données exclues du calcul** (contrat §5) : `autocorrect_active≠on`, résumé vide/incomplet (<6 segments), `valide≠oui`, `boost=oui`, `t0≥consigne`, `duree∉]0;120[`, `tmax` absent, erreur en zone morte.

## 3. Chaîne complète (cycle réel → offset futur)

```
Cycle ECS → gel.yaml (échéance inertie) :
   valide ⟵ (duree>0 ∧ temp_max_reelle>0 ∧ t0≠none ∧ (temp_max_reelle−t0)≥0.5) ? oui : non
   écrit le résumé figé + émet ecs_fin_cycle_signal
→ automation 10250000000019 (si autocorrect_active=on) → script
→ FILTRES (valide=oui, ¬boost, t0<consigne, 0<duree<120, tmax présent)
→ erreur = temp_max_reelle_figee − consigne ; si −0.3≤erreur≤+0.5 → STOP
→ bucket via delta_init = consigne − t0  (desinf / <2.5 tiny / <7.0 medium / sinon normal)
→ offset_new = clamp_step_reclamp( offset + 0.25·erreur ) ; si |Δ|≤0.001 → STOP
→ set_value offset_bucket + trace
→ offset consommé au cycle SUIVANT : consigne_chaudière = consigne − offset_bucket
```
Rétroaction **négative, de signe correct** : un dépassement augmente l'offset → abaisse la consigne chaudière suivante → réduit le dépassement.

## 4. Évaluation de l'algorithme

**Sain et conforme au contrat `11` (alignement exact).** Correcteur proportionnel intégrant (la mémoire est l'offset lui-même) ; `alpha=0.25` → convergence ≈ 4 cycles pour erreur constante (sous gain plant ≈ 1, plausible), stable ; **dérive cumulative bornée** par le clamp par bucket ; reboot = apprentissage persistant ; amortissement = zone morte + `alpha<1` ; cycles atypiques exclus (boost, durée, `t0≥consigne`, validité) ; re-clamp post-quantification présent ; « une seule entité par exécution » respecté.

## 5. Observabilité

| Observable | Valeur courante | Historique (recorder) |
|---|---|---|
| `ecs_off_*` | ✅ dashboard | ❌ non historisé |
| `ecs_dernier_ajustement` | ✅ (dernier seul) | ❌ non historisé + 1 entrée par conception |
| `ecs_resume_dernier_cycle_fige`, `…max_reelle_figee`, `…duree_figee` | ✅ | ❌ non historisé |

`recorder.yaml` est en liste blanche (`include: entities:`, sans glob ni domaine) ; aucune entité d'apprentissage n'y figure → la **trajectoire** des offsets et la suite des ajustements ne sont conservées nulle part.

## 6. Constats classés par gravité

| ID | Gravité | Constat | Disposition | Preuve |
|---|---|---|---|---|
| **ECS-OFF-1** | 🟠 | Trajectoire d'apprentissage non observable (recorder en liste blanche ; trace = 1 entrée). Dérive lente / biais indétectables depuis le système. | **Constat ouvert → backlog (observabilité, additif)** | `recorder.yaml` ; `dernier_ajustement_auto.yaml` |
| **ECS-OFF-2** | 🟠 | `valide` plus faible que ce que le contrat lui prête. Réel : `oui ⟺ duree>0 ∧ tmax_reelle>0 ∧ t0≠none ∧ (tmax_reelle−t0)≥0.5` (« un vrai chauffage a eu lieu »), non « validation métier finale ». | **Dette documentaire (contrat `11` §3.3)** | `gel.yaml` L80-90 ; contrat §3.3 |
| **ECS-OFF-3** | 🟠 | Aucun rejet d'aberration sur `tmax` (ni en amont, ni borne sur `|erreur|`). Un pic capteur `valide=oui` déplace l'offset de `0.25·|erreur|`, borné par le clamp, récupéré ensuite. Dérive cumulative **bornée**, transitoire possible. | **Risque assumé** (mitigation = runtime → gated preuve forte) | script (pas de clamp erreur) ; `gel.yaml` |
| **ECS-OFF-4** | 🟡 | Zone morte asymétrique `[-0.3 ; +0.5]` → équilibre appris biaisé vers un léger dépassement. Rationnel non documenté. | **Dette documentaire (contrat `11` §6.1)** | script + contrat §6.1 |
| **ECS-OFF-5** | 🟡 | Paramètres contractuels §10 (alpha, zone morte, buckets, durée, format résumé — « rupture de contrat ») non verrouillés CI. | **Futur chantier CI** (fusion « Durcissement CI ECS ») | `check_ecs_cycle` T06-08, `check_ecs_securite` T12 ; contrat §10 |
| **ECS-OFF-6** | 🟡 | Pas de bootstrap depuis `unknown` (`initial` commenté). Au 1ᵉʳ boot / après purge, autocorrect inerte ; le cycle tourne sur le fallback. Seed manuel requis. | **Dette documentaire (contrat `11`)** | `offset.yaml` ; script (gate `unknown`) |
| **ECS-OFF-7** | 🟡 | Convergence par bucket inégale ; `desinfection` rarement exercé → offset potentiellement stationné. | **Risque assumé** (gain-scheduling) | buckets script/contrat §6.2 |
| **ECS-OFF-8** | ⚪ | Mémoire = état seul, sans lissage d'erreur ; robustesse au bruit reposant sur alpha + zone morte + clamp (contexte d'OFF-3). | **Note de conception (contrat `11`)** | script |

## 7. Risques latents (synthèse)

- **Pas de dérive cumulative non bornée** : le clamp par bucket l'exclut (point rassurant majeur).
- **Risque réel = transitoire d'apprentissage sur cycle « valide » mais non représentatif** (OFF-2 + OFF-3), invisible faute d'historique (OFF-1) — c'est la combinaison qui mérite attention.
- **Jonction avec un sujet clos** : un cycle de désinfection tronqué par le watchdog (comportement **assumé** sous doctrine (a), cf. `arbitrage_watchdog_ecs.md` / `ECS-WD-2`) est précisément un cycle « `valide=oui` mais non représentatif ». Ce croisement renforce le classement d'OFF-3 en risque assumé.

## 8. Alignement

- **runtime ↔ contrat `11` : exact** (alpha, zone morte, buckets, filtres, clamp/quantif, négligeabilité, trace).
- **runtime ↔ CI : partiel** (plomberie signal + gate seulement ; algorithme/filtres/paramètres §10 non couverts → OFF-5).
- **runtime ↔ doc** : aligné, à la nuance §3.3 près (OFF-2, résorbée par la présente consolidation).

## 9. Renvois

- Contrat aligné : `contrats/ecs/11_ajustement_des_offsets.md` (§3.3, §6.1, §9, §11).
- Backlog : `audits/04_chantiers/ecs/backlog_ecs.md` (OFF-1 ouvert, OFF-5 → chantier CI, risques assumés OFF-3/OFF-7).
- Jonction watchdog : `audits/02_arbitrages/ecs/arbitrage_watchdog_ecs.md` (`ECS-WD-2`).

---

*Rapport d'audit ciblé ECS — Offsets. Établi en lecture du dépôt (`origin/main` = `372b8d7`). Acte documentaire — aucune modification runtime, contrat, YAML ou CI. Domaine ECS non clôturé.*
