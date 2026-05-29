# Plan d'implémentation — Chantier CH-2 (correctif D2 + alignement contrat)

**Type :** plan d'exécution technique (pré-implémentation, sans code)
**Statut amont :** revue de clôture **GO** ; gates R1, R2, R3, R5, R6, R7 fermés.
**Source de vérité :** runtime `antoinevalentinHA/arsenal`, branche `main`, **HEAD `2f335a5`**, lu le 2026-05-29.
**Gouvernance applicable :** `plan_action_chauffage_arsenal.md` · `CHANGELOG_CH1.md` · `REVUE_CLOTURE_CH2.md`.
**Périmètre :** préparation de l'implémentation. Aucun gate clos n'est rouvert.

---

## 0. Vérification d'entrée (corroboration runtime, pas ré-audit)

Avant d'ordonnancer, j'ai relu directement le runtime pour confirmer que les hypothèses du plan d'exécution tiennent encore sur `HEAD 2f335a5`. **Aucune contradiction factuelle** n'a été trouvée ; les conclusions de la clôture sont intégralement corroborées. Les constats utiles à l'implémentation :

- **Cinq lecteurs runtime** de `binary_sensor.chauffage_autorise_systeme`, tous intra-domaine, confirmés par grep exhaustif du dépôt : `decision_centrale.yaml` (`desired_mode` l.201, `reason` l.246), `raison.yaml` (l.80), `mode.yaml` (l.78), et le **trigger** (l.71). Aucun lecteur cross-domaine. Le reste des occurrences est documentaire, fixture gelée, ou ré-déclaration CI (atome de l'axiome).
- **Filet iso-comportement (R1) présent** : `desired_mode` conserve une branche `blocage_aeration` autonome (l.208-209 → `reduced`) en aval de la branche N1. Sa suppression de N1 laisse donc le cas blocage post-aération en `reduced`.
- **Composition `autorise_systeme` = terme unique (R2)** : `state` = `is_state(blocage_aeration,'off')` (l.56-57). `blocage` est le seul pilote de l'état `off`.
- **`R-MIRROR-1` lie exactement** `decision_centrale.yaml:reason` ↔ `raison.yaml:state` (descripteurs `CERVEAU_*`/`MIROIR_*` dans `r_mirror_1.py`). **Il ne couvre ni `desired_mode` ni `mode.yaml`.** Constat déterminant pour l'atomicité (§2).
- **Verdict runtime CI** = `cli_decision.executer_ch1()`, qui invoque `r_cov_1.analyser_fichier(CERVEAU_FICHIER, "reason", AXIOMES_D2)` (l.53-54). `R-COV-1` accepte `A=()` par défaut (domination purement structurelle).
- **`G2`** (`test_lot_2_7.py::test_g2_snapshot_cloture_ch1`) lit ce verdict et **affirme aujourd'hui 1 violation `R-COV-1`** de source `blocage_aeration_en_cours` + `R-MIRROR-1` vide. Snapshot **transitoire**, à re-figer en CH-2.
- **Token D3** : le runtime émet déjà `stabilisation_absence` (`decision_centrale.yaml` l.282, `raison.yaml` l.125). La cible du renommage est donc vérifiée comme **réellement émise** ; seul le **contrat 30** porte encore `absence_protection_thermique` (l.203) sur la surface opérante (les changelogs gelés sont hors critère).

---

## 1. Ordre d'implémentation recommandé

L'ordre est dicté par une règle simple : **décider hors-ligne ce qui fixe la forme des éditions, prouver hors-ligne l'iso-comportement, appliquer en un seul commit atomique le noyau gardé par la CI, puis seulement basculer l'enforcement.**

```
PHASE 0 — Hors-ligne (aucune écriture dépôt)
  1. Décision fail-safe (Option A vs B, §5)  ──┐ détermine la réécriture du state:
  2. Table de vérité avant/après (preuve)   ──┘ et la ligne d'edge consignée
  3. Re-vérification du token stabilisation_absence (déjà OK, §0)

PHASE 1 — COMMIT ATOMIQUE UNIQUE (réversible)  → le « noyau CH-2 »
  a. Couche décision (paire R-MIRROR-1) :
       decision_centrale.yaml : reason (retrait N1)  +  raison.yaml (retrait N1)
  b. Symétrie cascade :
       decision_centrale.yaml : desired_mode (retrait N1)  +  mode.yaml (retrait N1)
  c. Linchpin doctrinal :
       autorisation.yaml : réécriture du state: selon la décision §5
  d. Triplet CI :
       cli_decision.py (A=() + retrait import AXIOMES_D2)
       + test_lot_2_7.py (re-snapshot G2 : R-COV-1 == 0)
       + axiomes.py (requalification de la provenance — constante conservée)
  e. Contrat :
       30_decision_centrale.md (D3 + Niveau 1 réservé + chauffage_non_autorise réservé)

PHASE 2 — Validation (warn-only, ENFORCE encore false)  → §3
  pytest complet + verdict cli_decision vert observé en PR.

PHASE 3 — Bascule enforcement (commit séparé, ultérieur)
  ARSENAL_CI_ENFORCE → true  (uniquement après vert observé)

PHASE 4 — Suites séparables (optionnel, hors chemin critique)
  registres_entites.yaml (note de rôle) · alignement du reste de la surface contrat (§4-2)
```

**Justification de l'ordre :**

- **La décision fail-safe précède toute édition** parce qu'elle fixe la réécriture exacte de `state:` *et* la ligne `blocage ∈ {unavailable, unknown}` de la table de vérité. Éditer avant de décider, c'est risquer une réflexion incohérente entre les cascades (la clôture exige le reflet **identique** de la décision, §8.6) et du re-travail.
- **La table de vérité précède le commit** parce qu'elle est le gate d'iso-comportement (§8.1). La produire force à calculer, ligne à ligne, le comportement post-édition de chaque cascade — y compris la **sortie prédite de `mode.yaml`** (§8.6) — et fait remonter toute surprise hors-ligne (coût nul) plutôt qu'en CI (coût élevé).
- **Le noyau est un commit unique** parce que les invariants `R-MIRROR-1` et `G2` sont des contraintes **inter-fichiers** : elles virent au rouge dès que l'ensemble est partiellement appliqué (démontré §2). Tout fractionnement du noyau crée une fenêtre rouge.
- **La bascule enforcement est postérieure et séparée** (§8.9) : basculer avant le vert observé reviendrait à faire juger le commit correcteur par une CI bloquante avant d'avoir constaté qu'il produit bien le vert — fragile sur un transitoire, et inversion de l'ordre prudent. Diff d'une ligne, traçable.
- **Inversion CI-d'abord déjà consommée par CH-1.** La feuille de route plan (« garde-fous avant correctif ») a placé `R-COV-1`/`R-MIRROR-1`/fixture en CH-1, déjà sur `main`. CH-2 hérite donc d'un contrôle positif posé : l'ordre ci-dessus est la **suite** de cette discipline, pas sa rediscussion.

---

## 2. Atomicité

### 2.1 Le noyau atomique (impérativement un seul commit)

| Fichier | Modification | Lié par |
|---|---|---|
| `decision_centrale.yaml` | retrait branche N1 dans `reason` (l.246-247) | **R-MIRROR-1** + G2 |
| `raison.yaml` | retrait branche N1 (l.80-81) | **R-MIRROR-1** |
| `decision_centrale.yaml` | retrait branche N1 dans `desired_mode` (l.201-202) | squelette `desired_mode`/`reason` (§4.1 clôture) |
| `mode.yaml` | retrait branche N1 (l.78-79) | symétrie (§8.7) — *voir 2.2, seul cas réellement détachable* |
| `autorisation.yaml` | réécriture `state:` (l.56-57) selon §5 | **linchpin** : rend `autorise` constant / hook réservé |
| `cli_decision.py` | invocation `R-COV-1` en `A=()` (l.53-54) + retrait import `AXIOMES_D2` (l.29) | **G2** + verdict runtime |
| `test_lot_2_7.py` | re-snapshot G2 → `R-COV-1 == 0`, `R-MIRROR-1 == []` (l.48-56) | **G2** |
| `axiomes.py` | requalification provenance (l.33/41) ; **conserver** `AX_D2`/`AXIOMES_D2` (l.38-45) | cohérence : la provenance « composition live » devient fausse |
| `30_decision_centrale.md` | D3 (l.203) + Niveau 1 réservé (l.78-82) + `chauffage_non_autorise` réservé (l.193) | non gardé CI, mais vérité contrat↔runtime |

**Pourquoi chaque liaison impose le même commit :**

- **`reason` ↔ `raison.yaml` (R-MIRROR-1).** La règle compare les **signatures structurelles normalisées** (ordre des branches, garde canonique, liaisons, émissions). Retirer N1 d'un seul côté ⇒ signatures divergentes ⇒ **R-MIRROR-1 ROUGE**. C'est précisément la fenêtre à proscrire.
- **`reason` + `cli_decision (A=())` + `G2` (verdict).** `G2` affirme la sortie de `executer_ch1()`. Cette sortie passe de « 1 violation `R-COV-1` » à « 0 » dès que **l'une** de ces deux choses change :
  - le retrait de N1 dans `reason` rend la branche `blocage_aeration_en_cours` (l.253-254) atteignable structurellement (la garde `aération` en amont est indépendante de `blocage`) ⇒ 0 violation *même avec l'axiome* ;
  - le passage CLI à `A=()` retire l'axiome ⇒ plus de domination sous-axiome ⇒ 0 violation *même avec N1 présent*.
  Les deux flips sont indépendants : appliquer l'un sans re-figer `G2` ⇒ **G2 INCOHÉRENT (rouge)**. Donc runtime `reason` + `cli_decision` + `G2` sont indissociables.
- **`autorisation.yaml` (linchpin doctrinal).** Sans cette réécriture, `autorise` continue de passer `off` sur blocage. Les décisions resteraient correctes (plus aucun lecteur N1), mais le capteur **mentirait** : son `OFF` (« interdit de sécurité, sans glose », cf. en-tête du fichier) signifierait en réalité « blocage post-aération » — une cause Niveau 2, donc une glose interdite. De plus, la **requalification de provenance de l'axiome** (« composition de autorise_systeme ») ne devient vraie *qu'une fois* `autorisation.yaml` réécrit ; la requalifier sans réécrire serait prématuré et faux. ⇒ même commit, sous peine de divergence **runtime ↔ documentation/CI**.
- **`axiomes.py` — provenance, pas suppression.** `AX_D2`/`AXIOMES_D2` **doivent rester** : ils sont importés par `test_lot_2_3.py` (contrôle positif sur fixture) et affirmés présents par `G3` (`hasattr(axiomes,"AXIOMES_D2")`). Seule la **provenance** change : de « composition live de `autorise_systeme` » à « prémisse de la fixture gelée ». Le retrait de l'import côté `cli_decision` est sûr (les deux consommateurs restants importent l'axiome directement).

### 2.2 Ce qui est techniquement séparable

- **`mode.yaml` (retrait N1, l.78-79) — seul item réellement détachable sans fenêtre rouge.** `mode.yaml` n'est lu ni par `R-MIRROR-1`, ni par `R-COV-1`, ni par aucune automation (puits diagnostic pur, cf. en-tête + R7). Après le noyau, `autorise` étant constant `true`, la branche N1 de `mode.yaml` (`not is_state(autorise,'on')`) devient un `elif` **constamment faux** : code mort inoffensif. **Recommandation : l'inclure quand même** dans le noyau, par symétrie (§8.7) et pour ne pas laisser une branche morte (mini-D2) dans un capteur de diagnostic. Si une raison d'ordonnancement impose de le détacher, la seule conséquence est cette branche morte transitoire — aucun gate, aucun impact de contrôle.
- **`30_decision_centrale.md`.** Aucun workflow ne compare le texte du contrat au runtime (vérifié sur `.github/workflows/`). Donc détachable sans rouge. Mais la clôture solde D3 *dans* le commit D2 (fichier touché une seule fois), c'est un seul fichier, et le détacher ouvre un écart transitoire de vérité contrat↔runtime (le contrat décrirait encore une porte active). **Recommandation : même commit.**
- **`registres_entites.yaml` (note de rôle, optionnelle).** Détachable, non bloquant (§7 clôture).
- **Bascule `ARSENAL_CI_ENFORCE`.** À l'inverse : **doit être détachée** et **postérieure** (§8.9). Jamais dans le noyau.

### 2.3 Fenêtres explicitement évitées

| Fenêtre redoutée | Cause possible | Prévention |
|---|---|---|
| `R-MIRROR-1` rouge | retrait N1 asymétrique `reason`/`raison` | les deux dans le noyau |
| `G2` incohérent | runtime `reason` *ou* `cli A=()` modifié sans re-snapshot | triplet `reason`+`cli`+`G2` dans le noyau |
| runtime ↔ CI/doc divergent | `autorisation.yaml`/provenance axiome/contrat décalés du retrait N1 | linchpin + provenance + contrat dans le noyau |
| enforcement bloque le correctif | bascule trop tôt | bascule en commit séparé, après vert |

---

## 3. Validation

Périmètre d'exécution : `tools/` (PYTHONPATH), suite `pytest` de `arsenal_ci`, et la surface verdict `cli_decision`. Le workflow `arsenal-ci-chauffage.yml` rejoue ces deux niveaux (job *Lint structurel* étage 1 ; job *Verdict decision* étage 2).

### Phase 0 — hors-ligne (avant toute écriture)
- **Vérif locale :** table de vérité avant/après calculée par la **formule réelle**, colonne `autorise_systeme` explicite, ligne d'edge `blocage ∈ {unavailable, unknown}` renseignée selon §5.
- **Succès :** `desired_mode` identique avant/après sur **toutes** les lignes nominales ; unique écart assumé = la raison du cas blocage post-aération (`chauffage_non_autorise` → `blocage_aeration_en_cours`, `reduced` inchangé) ; ligne d'edge cohérente avec la décision §5.
- **Échec :** toute ligne nominale où `desired_mode` change ⇒ **stop**, l'iso-comportement est rompu, l'édition ne doit pas être appliquée.

### Phase 1 — sur l'arbre de travail / PR (après le noyau, ENFORCE encore false)
- **Commandes :**
  - `PYTHONPATH=tools python -m pytest tools/arsenal_ci/tests` (suite complète) ;
  - `PYTHONPATH=tools python -m arsenal_ci.decision.cli_decision --json ci_reports/decision.json` (verdict runtime).
- **Critères de succès (alignés §8.3-8.4) :**
  - **Verdict runtime VERT** : `R-COV-1 == 0` et `R-MIRROR-1 == []` sur le runtime corrigé ; exit 0.
  - **`test_lot_2_3` PASSE** : le contrôle positif sur la **fixture** continue d'affirmer la violation `R-COV-1` sous `A={AX-D2}` (source `blocage_aeration_en_cours`, cible `chauffage_non_autorise`, mention `AX-D2`) **et** l'absence de violation sous `A=()` (bascule). ⚠️ « fixture ROUGE » = l'analyse de la fixture *retourne* une violation ; le **test qui l'affirme reste VERT**. Un `test_lot_2_3` rouge n'est jamais attendu.
  - **`G2` re-snapshoté PASSE** : `R-COV-1 == 0` sur le runtime.
  - **`test_lot_2_6` PASSE** : SHA256 de la fixture inchangé (`81f8705f…`) — preuve que la fixture n'a pas été touchée.
  - **`G1/G3/G4/G5` PASSENT** : isolation des étages, surface étage-2 importable (dont `AXIOMES_D2` présent), source unique de localisation, bornage des fichiers.
- **Signaux d'échec et triage :**
  - `R-MIRROR-1` rouge ⇒ retrait N1 asymétrique `reason`/`raison` → corriger la paire.
  - `R-COV-1` runtime rouge ⇒ **régression réelle du domaine** (branche redevenue dominée) → ne pas re-snapshoter, investiguer le runtime.
  - `test_lot_2_3` rouge ⇒ régression du **vérificateur** ou fixture altérée → ne jamais « réparer » en touchant la fixture.
  - `executer_ch1` en `execution_error` (exit 2) ⇒ runtime illisible / câblage cassé, **pas** un faux verdict (cf. `test_lot_2_5` smoke live) → trier comme erreur d'analyse.

### Phase 3 — après bascule `ARSENAL_CI_ENFORCE=true`
- **Succès :** le job *Verdict decision* du workflow chauffage passe **bloquant** sur le runtime corrigé (exit 0) ; une régression future fera désormais échouer la PR.
- **Échec :** si le vert n'a pas été observé en Phase 2, ne pas basculer.

---

## 4. Risques résiduels (postérieurs à la clôture)

Uniquement ce qui subsiste après R1-R7. Les gates fermés ne sont pas réénumérés.

**4-1. Edge `blocage` dégradé — disparition du repli conservateur (la réserve §6, précisée).**
Aujourd'hui le `reduced` sur `blocage ∈ {unavailable, unknown}` est un **sous-produit accidentel** du biconditionnel `is_state(blocage,'off')` (faux sur l'état dégradé ⇒ `autorise off` ⇒ N1 ⇒ `reduced`). Après retrait de N1, **plus aucun lecteur de décision ne consulte `autorise`** ; et la branche `blocage` de la cascade teste `== 'on'`, donc **ne capte pas** l'état dégradé. Conséquence factuelle, vérifiable sur le runtime : sur l'edge dégradé, la cascade **traverse** la branche blocage et descend jusqu'aux niveaux inférieurs (présence / inhibition géoloc / défaut), pouvant aboutir à `comfort`. Le repli n'est donc **pas** préservé par une simple réécriture de `state:` (cf. §5). Exposition réelle **faible** : `chauffage_blocage_aeration` est un `input_boolean` (helper HA), qui ne tombe en `unknown`/`unavailable` qu'en fenêtre de redémarrage avant restauration d'état — fenêtre où d'autres gardes (G2/G3) et la ré-évaluation par trigger interviennent. Résiduel **borné**, à clore explicitement au niveau décision si l'on veut une garantie (§5), pas par le hook de sécurité.

**4-2. Staleness de la surface contrat élargie (au-delà du fichier 30).**
La clôture a sciemment borné la modification documentaire au **contrat 30**. Le grep dépôt montre que d'autres contrats décrivent encore `autorise_systeme` comme une **porte Niveau 1 active** imposant `reduced` / « interdiction immédiate » : `20_triggers_decisionnels.md` (l.151-152) et son amendement (l.68-69), `30 §Niveau 1` (l.78-82, dans le périmètre), `01_doctrine_registres.md`, `40_blocages.md`, `50/60/80…`, `15_capteurs/02`. Après CH-2 (capteur = hook réservé, constant), ces surfaces deviennent **partiellement inexactes**. *Aucun impact de contrôle ; dette de vérité documentaire.* Note : l'**amendement** `30_decision_centrale__amendement.md` anticipe déjà la requalification (« une fois ce capteur redevenu sécurité… », l.116 ; trigger « reste utile », l.157-158), donc la dette porte surtout sur les contrats de base. **Ce n'est pas une réouverture de gate** : c'est une observation de cadrage, étayée par grep. L'architecte tranche : balayage doc dans CH-2, ou report (rapprochement naturel avec D8/CH-5).

**4-3. Discipline du re-snapshot G2.**
`G2` est transitoire par conception. Risque d'implémentation : re-figer mollement (ex. « pas de `R-COV-1` de telle source » au lieu de **count == 0**), ce qui affaiblirait le contrôle négatif. Mitigation : affirmer l'**absence stricte** de `R-COV-1` sur le runtime + `R-MIRROR-1 == []` ; le contrôle **positif** demeure `test_lot_2_3` sur la fixture.

**4-4. Latence de garde sur re-couplage futur de `autorise`.**
La CLI passant désormais `A=()` sur le runtime, un futur ré-ajout d'un test `autorise` dans la cascade `reason` ne serait **pas** repris par `R-COV-1`-runtime. Gap latent mineur : le contrôle positif sur fixture garde le **motif historique**, mais la garde **générale** contre la remontée conséquence→cause est `INV-D1/D3`, planifiée en **CH-3**. À clore par CH-3, pas par CH-2.

---

## 5. Décision fail-safe — recommandation argumentée

**Recommandation : Option A (`state` constant `true`), avec traitement explicite et séparé de l'edge dégradé au niveau décision si une garantie est souhaitée.**

### Le constat qui reformule le choix
La clôture §6 oppose A (« constante `true` ») et B (« prédicat conservant le repli »). Le runtime impose une précision : **après le retrait de N1, `autorise_systeme` n'a plus aucun lecteur de décision** (les quatre lecteurs sont supprimés ; le trigger n'utilise pas la valeur, il réveille le cerveau). Donc une Option B implémentée **comme simple réécriture du `state:`** est **décisionnellement inerte** : faire passer `autorise` à `off` sur blocage dégradé ne changerait que l'état affiché et les attributs du capteur, **pas** la décision. Le repli conservateur n'est *pas* récupérable par la couche autorisation. Le vrai choix n'est donc pas « A vs B sur `autorisation.yaml` », mais : **veut-on un repli sur l'edge dégradé, et si oui, à quelle couche le placer ?**

### Pourquoi A, au regard des trois critères demandés
- **Doctrine Arsenal.** L'en-tête de `autorisation.yaml` est explicite : `OFF = interdit, sans glose` ; capteur « strictement sécurité système ». Un capteur `blocage` aveugle n'est pas une **cause positive de sécurité** ; c'est une **inconnue**. Encoder « je ne vois pas le capteur » en `autorise = off` (Niveau 1 = interdit) serait exactement la **glose** et le **déguisement de catégorie** que D0/D1/D3 proscrivent. La prudence sur capteur aveugle n'appartient pas au Niveau 1.
- **Sémantique des niveaux.** Le repli est une **prudence par défaut**, sémantiquement un Niveau 2 (« contexte majeur ») ou un défaut de cascade, pas une interdiction de sécurité. Le loger au bon niveau préserve la lisibilité de la hiérarchie ; le loger dans `autorise` la corrompt.
- **Rôle futur de hook réservé.** A maintient le hook **vierge et honnête** : « aucune cause de sécurité active ⇒ autorisé ». Quand une vraie cause Niveau 1 apparaîtra, on la composera proprement. B pré-charge le hook d'une sémantique non-sécuritaire (disponibilité capteur) et **ré-introduit un couplage à `blocage`** — défaisant partiellement la désintrication D2. Argument annexe mais net : sous A, `autorise` étant constant, le trigger l.71 **ne se déclenche jamais** (zéro réveil parasite) ; sous B, il se déclencherait sur l'edge dégradé pour un effet décisionnel nul.

### Si Antoine veut préserver la prudence sur l'edge
Ne pas le faire via `autorisation.yaml`. Le placer **à la couche décision**, en micro-décision séparée, documentée, avec un **token de raison honnête** (ne pas émettre `blocage_aeration_en_cours` quand la vérité est « capteur aveugle »). Deux formes possibles, à arbitrer ensuite : élargir la garde de la branche blocage pour couvrir l'état non-`off`, ou ajouter un défaut défensif explicite. C'est un ajout délibéré, borné, hors du présent correctif iso-comportement — pas un effet de bord du fail-safe.

### Consignation exigée (§8.6)
Quelle que soit la variante retenue, la ligne `blocage ∈ {unavailable, unknown}` de la table avant/après doit être renseignée et **reflétée identiquement** dans `desired_mode`, `mode.yaml` et le miroir. Sous A sans garde additionnelle, cette ligne s'écrit : *edge dégradé ⇒ branche blocage non prise ⇒ traversée jusqu'au défaut de cascade (typiquement `reduced`, sauf présence/inhibition géoloc active)* — comportement **identique** dans les trois, puisque aucun ne lit plus `autorise`.

---

## Synthèse opérationnelle

1. Trancher §5 (recommandé : **Option A**), puis produire la table de vérité avant/après (incl. ligne d'edge et sortie `mode.yaml` prédite).
2. Appliquer le **noyau atomique** §2.1 en **un commit réversible** ; `mode.yaml` inclus par symétrie.
3. Valider §3 en warn-only : verdict runtime **vert**, `test_lot_2_3` vert (fixture rouge), `G2` re-figé, SHA fixture intact.
4. Basculer `ARSENAL_CI_ENFORCE → true` en **commit séparé** une fois le vert observé.
5. Suivre les résiduels §4 — surtout l'edge dégradé (4-1, décision §5) et le cadrage du balayage doc (4-2).

*Document de préparation d'implémentation. À archiver aux côtés de `plan_action_chauffage_arsenal.md`, `CHANGELOG_CH1.md` et `REVUE_CLOTURE_CH2.md`. Runtime de référence : `HEAD 2f335a5`, 2026-05-29.*
