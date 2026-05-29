# Brief opératoire — Session patch CH-2 (noyau atomique §2.1)

**Type :** plan d'exécution opératoire (handoff vers session patch). **Pas un document d'analyse.**
**Amont validé, non rediscuté :** `REVUE_CLOTURE_CH2.md` (GO) · `PLAN_IMPLEMENTATION_CH2.md` · `TABLE_VERITE_CH2_PHASE0.md` (gate Phase 0 → GO, Option A actée).
**Source de vérité runtime :** `antoinevalentinHA/arsenal`, **`HEAD 2f335a5`**, relu le 2026-05-29. Tous les numéros de ligne ci-dessous sont vérifiés sur ce commit.
**Décision fail-safe :** **Option A** — `binary_sensor.chauffage_autorise_systeme` devient hook réservé pur, constant `on`.
**Forme du livrable visé par la session suivante :** **un seul commit atomique réversible** (le « noyau CH-2 »), puis bascule enforcement en commit séparé ultérieur.

> Rappels de discipline pour la session patch : ne pas toucher la fixture, ne pas réécrire les changelogs gelés, ne pas basculer `ARSENAL_CI_ENFORCE` dans ce commit, ne réordonner/réécrire aucune branche hors périmètre.

---

## 1. Liste exacte des fichiers à modifier

Neuf fichiers, **tous dans le même commit** (sauf mention « séparable »). Ancrages = `HEAD 2f335a5`.

| # | Fichier | Nature de l'édition | Lié par |
|---|---|---|---|
| 1 | `10_scripts/chauffage/decision_centrale.yaml` | Retrait branche N1 dans `reason` **et** dans `desired_mode` | R-MIRROR-1 (reason) + squelette desired_mode/reason |
| 2 | `12_template_sensors/chauffage/diagnostic/raison.yaml` | Retrait branche N1 (miroir de `reason`) | R-MIRROR-1 |
| 3 | `12_template_sensors/chauffage/diagnostic/mode.yaml` | Retrait branche N1 (symétrie diagnostic) | symétrie §8.7 — *seul item réellement détachable* |
| 4 | `12_template_sensors/chauffage/autorisation.yaml` | Réécriture `state:` en constante `on` (Option A) | **linchpin** : rend `autorise` constant |
| 5 | `tools/arsenal_ci/decision/cli_decision.py` | Invocation R-COV-1 en `A=()` + retrait import `AXIOMES_D2` | G2 + verdict runtime |
| 6 | `tools/arsenal_ci/decision/axiomes.py` | Requalification de la **provenance** (constante conservée) | cohérence provenance ↔ runtime |
| 7 | `tools/arsenal_ci/tests/test_lot_2_7.py` | Re-snapshot G2 → `R-COV-1 == 0` | G2 |
| 8 | `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` | D3 + Niveau 1 réservé + `chauffage_non_autorise` réservé | vérité contrat ↔ runtime (non gardé CI) |

**Détachable (hors noyau, optionnel) :** `…/contrats/chauffage/ci/registres_entites.yaml` (note de rôle). Non bloquant.
**À NE PAS toucher :** fixture `d2_reason_pre_correction.yaml` ; `test_lot_2_3.py` ; `test_lot_2_5.py` ; `test_lot_2_6.py` ; `11_automations/chauffage/decision_centrale_trigger.yaml` (hook conservé) ; changelogs gelés.
**Commit séparé ultérieur :** bascule `ARSENAL_CI_ENFORCE → true` (jamais dans ce commit).

---

## 2. Ordre précis des modifications

Séquence d'édition à l'intérieur du commit unique (l'ordre n'introduit aucune fenêtre rouge car tout est livré atomiquement ; il optimise la cohérence de revue).

```
ÉTAPE A — Couche décision (paire R-MIRROR-1)
  A1. decision_centrale.yaml : retrait N1 dans `reason`
  A2. raison.yaml            : retrait N1 (miroir)
        → après A1+A2, signatures structurelles reason ↔ raison réalignées

ÉTAPE B — Symétrie cascade
  B1. decision_centrale.yaml : retrait N1 dans `desired_mode`
  B2. mode.yaml              : retrait N1 (diagnostic)

ÉTAPE C — Linchpin doctrinal
  C1. autorisation.yaml      : state: → constante `on` (Option A)
        (+ alignement en-tête doctrinal du fichier ; cf. §6 point a)

ÉTAPE D — Triplet CI (indissociable)
  D1. cli_decision.py        : A=() + retrait import AXIOMES_D2
  D2. axiomes.py             : requalification provenance (constante conservée)
  D3. test_lot_2_7.py        : re-snapshot G2 (count strict == 0)

ÉTAPE E — Contrat
  E1. 30_decision_centrale.md : D3 + Niveau 1 réservé + chauffage_non_autorise réservé
```

**Pourquoi cet ordre.** A en premier parce que la paire reason ↔ raison est la seule contrainte inter-fichiers gardée *à l'octet* (R-MIRROR-1) : la traiter d'un bloc évite tout raisonnement asymétrique. B prolonge la symétrie sur les deux cascades non gardées par le miroir. C (linchpin) après les cascades : une fois N1 retiré partout, `autorise` n'a plus aucun lecteur de décision, donc réécrire `state:` ne peut plus altérer une décision. D rend le verdict CI cohérent avec le runtime corrigé (les deux flips — N1 retiré + `A=()` — sont co-livrés, donc `G2` est re-figé dans le même mouvement). E aligne la vérité contrat en dernier (aucun gate CI ne le compare au runtime).

---

## 3. Extraits runtime concernés (état AVANT — `HEAD 2f335a5`)

> Extraits du runtime actuel, fournis comme ancrage de repérage. **Aucun code cible / aucun diff** ici : la transformation est décrite en prose.

### 3.A — `decision_centrale.yaml` · `reason` (N1 à retirer : l.246-248)
```
242  reason: >
243    {% if is_state('input_boolean.mode_confort_chauffage', 'on') %}
244      confort_force
245
246    {% elif not is_state('binary_sensor.chauffage_autorise_systeme', 'on') %}
247      chauffage_non_autorise
248
249    {% elif is_state('input_boolean.aeration_episode_en_cours', 'on')
```
**Transformation :** supprimer le bloc `elif not …autorise…` + `chauffage_non_autorise` (l.246-247) et la ligne vide associée (l.248). La branche `confort_force` enchaîne directement sur l'`elif` aération (l.249). Branche `blocage_aeration_en_cours` (l.253-254) conservée.

### 3.B — `decision_centrale.yaml` · `desired_mode` (N1 à retirer : l.201-203)
```
197  desired_mode: >
198    {% if is_state('input_boolean.mode_confort_chauffage', 'on') %}
199      comfort
200
201    {% elif not is_state('binary_sensor.chauffage_autorise_systeme', 'on') %}
202      reduced
203
204    {% elif is_state('input_boolean.aeration_episode_en_cours', 'on')
```
**Transformation :** supprimer `elif not …autorise…` + `reduced` (l.201-202) + ligne vide (l.203). Branche autonome `chauffage_blocage_aeration → reduced` (l.208-209) **conservée** (filet iso-comportement R1).

### 3.C — `raison.yaml` · miroir (N1 à retirer : l.80-81, + bandeau l.77-79)
```
77   {# ======================================================
78      🛑 NIVEAU 1 — INTERDICTIONS SYSTÈME
79      ====================================================== #}
80   {% elif not is_state('binary_sensor.chauffage_autorise_systeme', 'on') %}
81     chauffage_non_autorise
82
83   {# ======================================================
84      🧠 NIVEAU 2 — CONTEXTES MAJEURS
```
**Transformation :** supprimer l.80-81. Supprimer aussi le bandeau commentaire « NIVEAU 1 » (l.77-79) devenu orphelin (cosmétique, hors gate — R-MIRROR-1 ignore les commentaires).

### 3.D — `mode.yaml` · diagnostic (N1 à retirer : l.78-79)
```
75   {# ==================================================
76      2. BLOCAGES HIÉRARCHIQUES (HORS OVERRIDE)
77      ================================================== #}
78   {% elif not is_state('binary_sensor.chauffage_autorise_systeme', 'on') %}
79     Eco
80   {% elif is_state('input_boolean.aeration_episode_en_cours', 'on')
```
**Transformation :** supprimer l.78-79. Le bandeau « 2. BLOCAGES » (l.75-77) reste (couvre encore aération/blocage/fenêtre).

### 3.E — `autorisation.yaml` · `state:` (à réécrire : l.56-57)
```
56   state: >
57     {{ is_state('input_boolean.chauffage_blocage_aeration', 'off') }}
```
**Transformation (Option A) :** remplacer la formule par une constante vraie (`on`/`true`). Attributs `blocage_aeration`, `standby_force`, `resume` (l.67-87) **inchangés** (observabilité). *Points à trancher : en-tête doctrinal (l.1-48) et icône (l.59-65) — cf. §6.*

### 3.F — `cli_decision.py` · import (l.29) + invocation (l.53-54)
```
29   from .axiomes import AXIOMES_D2
…
53   violations: List[Violation] = list(
54       r_cov_1.analyser_fichier(CERVEAU_FICHIER, CERVEAU_CLE, AXIOMES_D2)
55   )
```
**Transformation :** retirer l'import l.29 ; à l.54, passer `A=()` (signature `analyser_fichier(chemin, cle, axiomes=())` — défaut vide vérifié dans `r_cov_1.py` l.211-215, donc soit `()` explicite, soit suppression du 3ᵉ argument).

### 3.G — `axiomes.py` · provenance (l.33-34 commentaire, l.41 chaîne)
```
33   # Source : autorisation.yaml (composition de autorise_systeme). RE-DECLARE ici,
34   # non lu depuis le runtime.
…
38   AX_D2 = Axiome(
39       identifiant="AX-D2-BLOCAGE-AUTORISE",
40       formule=Ou((Non(_BLOCAGE), Non(_AUTORISE))),
41       provenance="autorisation.yaml : composition de autorise_systeme",
42   )
…
45   AXIOMES_D2 = (AX_D2,)
```
**Transformation :** **conserver** `AX_D2`/`AXIOMES_D2`, identifiant et formule **intacts** (requis par `test_lot_2_3` et par G3 `hasattr(axiomes,"AXIOMES_D2")`). Requalifier uniquement la **provenance** (l.41 + commentaire l.33-34) : la composition live de `autorise_systeme` disparaissant, la provenance devient « prémisse de la fixture gelée `d2_reason_pre_correction.yaml` ».

### 3.H — `test_lot_2_7.py` · G2 (à re-figer : l.48-56, + note l.40-46)
```
48   def test_g2_snapshot_cloture_ch1():
49       r = cli_decision.executer_ch1()
50       assert r.execution_error is None
51       cov = [v for v in r.violations if v.rule == "R-COV-1"]
52       assert len(cov) == 1
53       assert cov[0].source == "blocage_aeration_en_cours"
54       # R-MIRROR-1 : cerveau <-> miroir synchrones.
55       assert [v for v in r.violations if v.rule == "R-MIRROR-1"] == []
```
**Transformation :** `assert len(cov) == 1` → **`== 0`** (count **strict**, cf. résiduel §4-3 du plan) ; **supprimer** l'assertion `cov[0].source …` (lèverait IndexError) ; conserver R-MIRROR-1 `== []` (l.55-56). Mettre à jour la note transitoire (l.40-46) pour acter le franchissement CH-1 → CH-2.

### 3.I — `30_decision_centrale.md` · trois zones
```
80   `binary_sensor.chauffage_autorise_systeme`
81
82   Impose `reduced`. Stop hiérarchique — aucune autre cause évaluée.
…
193  | Système non autorisé | `chauffage_non_autorise` |
…
203  | Inhibition géofencing | `absence_protection_thermique` |
```
**Transformations :** (1) **l.203** D3 : `absence_protection_thermique` → `stabilisation_absence` (token réellement émis par le runtime, vérifié `decision_centrale.yaml` l.282 / `raison.yaml` l.125). (2) **l.193** : marquer `chauffage_non_autorise` **réservé / non émise**. (3) **l.78-82** Niveau 1 : requalifier en **catégorie réservée sans cause active** (hook). *Note : le §3b géofencing existe déjà (l.100) — ne PAS créer de doublon ; cf. §6 point d.*

---

## 4. Impacts attendus, fichier par fichier

| Fichier | Effet sur la décision | Effet observable / CI | Risque |
|---|---|---|---|
| `decision_centrale.yaml` (`reason`) | Cas blocage post-aération : raison `chauffage_non_autorise` → `blocage_aeration_en_cours` (cause réelle). Aucun autre changement nominal. | Rend `blocage_aeration_en_cours` atteignable → R-COV-1 = 0. Signature reason réalignée sur raison. | Asymétrie si A2 oublié → R-MIRROR-1 rouge. |
| `decision_centrale.yaml` (`desired_mode`) | **Aucun** changement thermique nominal (branche `blocage → reduced` autonome maintient `reduced`). | — | Edge dégradé : `desired_mode` peut passer `reduced → comfort` (ligne 14 table, exception Option A assumée). |
| `raison.yaml` | Miroir : même réparation que `reason`. | Maintient R-MIRROR-1 = [] (synchronie). | Idem asymétrie. |
| `mode.yaml` | Branche N1 devient morte (autorise constant) puis retirée. Sortie diagnostic invariante (Eco→Eco). | Puits diagnostic (aucune automation) → zéro régression de contrôle (R7). | Nul (détachable, mais à inclure pour ne pas laisser de branche morte). |
| `autorisation.yaml` | `autorise` constant `on` → plus aucun lecteur de décision. Capteur = hook réservé. | État capteur ne ment plus (`OFF` ne signifierait plus « blocage N2 »). Trigger l.71 ne se déclenche plus (zéro réveil parasite). | En-tête/icône à aligner (cf. §6) sinon dérive de vérité interne au fichier. |
| `cli_decision.py` | — | Verdict runtime évalué `A=()` → couverture purement structurelle → R-COV-1 = 0. | Import résiduel oublié = lint mort (inoffensif). |
| `axiomes.py` | — | Constante toujours importable (G3 vert ; `test_lot_2_3` inchangé). | Toucher identifiant/formule = casse `test_lot_2_3` → **ne pas** y toucher. |
| `test_lot_2_7.py` (G2) | — | G2 re-figé cohérent : R-COV-1 = 0, R-MIRROR-1 = []. | Re-snapshot « mou » (source au lieu de count) = contrôle négatif affaibli → **count strict**. |
| `30_decision_centrale.md` | — | Vérité contrat ↔ runtime alignée (D3, Niveau 1 réservé). | Non gardé CI : seul garde-fou = relecture. |

**Surfaces explicitement hors périmètre (rappel) :** trigger conservé ; fixture/`test_lot_2_3`/`2_5`/`2_6` intacts ; staleness de la surface contrat élargie (4-2 du plan) **reportée**, non traitée ici.

---

## 5. Validations à exécuter immédiatement après modification

> Phase 0 (table de vérité) **déjà franchie** (`TABLE_VERITE_CH2_PHASE0.md` → GO). Les validations ci-dessous s'exécutent **après** application du noyau, **`ARSENAL_CI_ENFORCE` encore `false`**.

**V0 — Validité runtime (avant CI).** Vérifier que les 4 cascades restent des scalaires repliés `>` valides (indentation, pas de `elif`/`endif` orphelin après retrait). Lint YAML + contrôle de configuration Home Assistant.

**V1 — Suite complète.**
`PYTHONPATH=tools python -m pytest tools/arsenal_ci/tests`
Attendu : **tout passe**, dont en particulier —

| Test / gate | Attendu | Sens |
|---|---|---|
| Verdict via `cli_decision` | R-COV-1 = 0, R-MIRROR-1 = [], exit 0 | runtime corrigé VERT |
| `test_lot_2_3` | **PASSE** | fixture sous `A={AX-D2}` retourne toujours la violation (source `blocage_aeration_en_cours`, cible `chauffage_non_autorise`, mention `AX-D2`) **et** absence sous `A=()`. ⚠ « fixture ROUGE » = l'analyse *retourne* une violation ; le test reste **VERT**. |
| `test_lot_2_7::G2` | **PASSE** | `len(cov) == 0` strict sur le runtime |
| `test_lot_2_6` | **PASSE** | SHA256 fixture inchangé (`81f8705f…`) — preuve fixture non touchée |
| G1 / G3 / G4 / G5 | **PASSENT** | isolation étages ; surface étage-2 importable (dont `AXIOMES_D2`) ; source unique localisation ; bornage fichiers |

**V2 — Verdict runtime explicite.**
`PYTHONPATH=tools python -m arsenal_ci.decision.cli_decision --json ci_reports/decision.json`
Attendu : exit 0 ; `R-COV-1 == 0` ; `R-MIRROR-1 == []`.

**Triage des échecs (ne pas improviser) :**
- `R-MIRROR-1` rouge ⇒ retrait N1 asymétrique `reason`/`raison` → corriger la **paire** (étape A).
- `R-COV-1` runtime rouge ⇒ **régression réelle du domaine** → **ne pas** re-snapshoter G2 ; investiguer le runtime.
- `test_lot_2_3` rouge ⇒ régression du **vérificateur** ou fixture altérée → **jamais** « réparer » en touchant la fixture.
- `executer_ch1` en `execution_error` (exit 2) ⇒ runtime illisible / câblage cassé (pas un faux verdict) → trier comme erreur d'analyse.

**Après V1+V2 verts uniquement :** commit séparé `ARSENAL_CI_ENFORCE → true` (Phase 3, hors de ce patch).

---

## 6. Points à trancher au moment du patch (micro-décisions, non rouvertes en amont)

Détectés à la relecture runtime ; ni l'un ni l'autre ne rouvre un gate. À acter explicitement dans la session patch.

a. **En-tête doctrinal de `autorisation.yaml` (l.1-48).** Il décrit aujourd'hui la sémantique `OFF = interdit`. Sous Option A, `OFF` ne se produit plus. **Recommandé :** aligner l'en-tête sur « hook réservé, constant `on`, aucune cause de sécurité active » pour éviter une dérive de vérité interne au fichier. (Cohérent avec l'intention « linchpin doctrinal ».)

b. **Icône de `autorisation.yaml` (l.59-65).** Elle lit encore `blocage` (affiche `radiator-off` sur blocage) alors que `state` sera constant `on`. **Recommandé par défaut :** la **laisser** (indice visuel d'observabilité, cohérent avec le maintien des attributs ; l'autorité reste `state`). Variante possible : la rendre constante pour un hook « pur ». À choisir explicitement.

c. **Bandeau commentaire « NIVEAU 1 » dans `raison.yaml` (l.77-79).** Devient orphelin après retrait N1. **Recommandé :** le supprimer (cosmétique, hors gate).

d. **§3b du contrat 30 (l.100).** Le §3b « Inhibition géofencing » **existe déjà**. La recommandation de clôture « ajout 3b » est donc **sans objet** : ne pas dupliquer. Au plus, mentionner le token `stabilisation_absence` dans la prose existante de 3b pour la cohérence avec l.203.

e. **Forme de l'argument `A=()` dans `cli_decision.py`.** Passer `()` explicite **ou** omettre le 3ᵉ argument (défaut = `()`). Choisir une forme et s'y tenir ; préférer la plus lisible au regard du style du fichier.

---

## 7. Définition de « terminé » pour le commit noyau

1. 8 fichiers du §1 modifiés ; édition conforme aux transformations §3 ; micro-décisions §6 actées.
2. V0 + V1 + V2 **verts** (table §5), fixture intacte (SHA `81f8705f…`).
3. `desired_mode` iso-comportement nominal (lignes 1-12 de la table Phase 0) — déjà prouvé, confirmé par la non-régression pytest.
4. Commit **atomique et réversible** ; aucun fichier de la liste « à ne pas toucher » modifié ; `ARSENAL_CI_ENFORCE` inchangé.
5. Bascule enforcement **réservée** à un commit ultérieur, après verts observés.

*Document de handoff. À archiver avec `REVUE_CLOTURE_CH2.md`, `PLAN_IMPLEMENTATION_CH2.md`, `TABLE_VERITE_CH2_PHASE0.md`. Runtime de référence : `HEAD 2f335a5`, 2026-05-29.*
