# Revue architecturale — Chantier CH-2 (Correctif D2 + alignement contrat)

**Rôle :** architecte de revue, en amont de toute modification runtime.
**Sources de vérité :** `plan_action_chauffage_arsenal.md` (29/05/2026) ; `CHANGELOG_CH1.md` (CH-1 clos).
**Posture :** aucune hypothèse optimiste ; recherche active d'angles morts, de dépendances cachées et d'effets de bord.
**Périmètre :** ne réanalyse pas CH-1, ne rouvre aucun arbitrage déjà tranché (disposition (a), `blocage_aeration = Niveau 2`, fixture canonique). Vérifie la cohérence de CH-2 *après* la réalisation réelle de CH-1.
**Aucun code, aucune modification runtime proposée.**

---

## 1. Ce que CH-1 a réellement livré

CH-1 a posé l'**étage 2** du validateur Arsenal CI (région autonome `tools/arsenal_ci/decision/`), sans toucher une seule ligne du runtime Chauffage. Livré et clos (103 tests verts) :

- **Modèle canonique de cascade** (`model.py`) : représentation immuable, ordonnée, à signature structurelle déterministe (provenance exclue).
- **Normaliseur** (`normaliseur.py`) : conversion Jinja → modèle canonique, grammaire close, discipline *fail-closed*.
- **Table d'alias** (`alias.py`) : normalisation **syntaxique seule** — aucune sémantique de domination, d'implication ni d'atteignabilité.
- **R-COV-1** (`r_cov_1.py`) : moteur général d'inatteignabilité en sémantique premier-match. Décide la satisfiabilité `A ∧ G_i ∧ (et_{j<i} non G_j)`, où `A` est un jeu d'**axiomes optionnel**. Sous `A = ()` : domination purement structurelle ; sous `A ≠ ()` : domination conditionnée par axiomes déclarés.
- **R-MIRROR-1** (`r_mirror_1.py`) : synchronie structurelle cerveau ↔ miroir (garde, liaisons, issue, sous-cascade, nombre de branches), sur représentation normalisée. **Autorité unique des chemins** cerveau/miroir.
- **Surface CI** (`cli_decision.py`) + **job GitHub Actions** `decision` (parallèle à `lint`, conditionné au self-test).
- **Fixture canonique D2** (`d2_reason_pre_correction.yaml`) : photographie figée de la cascade `reason` pré-correction (branche `blocage_aeration_en_cours` structurellement présente, logiquement morte).
- **Axiome `AX-D2-BLOCAGE-AUTORISE`** (`axiomes.py`) : prémisse externe `blocage_aeration='on' ⇒ autorise_systeme!='on'`, **issue de la composition de `autorise_systeme` dans `autorisation.yaml`**, fournie au moteur sans l'inscrire dans la fixture ni l'alias.
- **Registre d'immuabilité** (`test_lot_2_6.py`) : empreintes SHA256, intégrité + couverture, procédure de re-bénédiction.
- **Bascule `ARSENAL_CI_ENFORCE`** (warn-only → bloquant) ; **invariant de clôture transitoire `G2`**.

**État actuel de la dette D2 :** mesurée, gelée, surveillée en **warn-only**. R-COV-1 émet la violation **sur le runtime vivant, sous l'axiome `AX-D2`**. La fixture (avec l'axiome) sert le **self-test** ; le verdict CI porte sur la configuration vivante.

---

## 2. Nouveaux leviers/invariants disponibles grâce à CH-1

1. **R-COV-1 sur le runtime** (avec `AXIOMES_D2`) : verdict machine sur la mort de branche. Cible post-CH-2 : **vert**.
2. **R-MIRROR-1** : garde-fou de l'édition simultanée `decision_centrale.yaml` ↔ `diagnostic/raison.yaml`. Détecte toute édition asymétrique.
3. **Fixture D2 figée + self-test** (R-COV-1 rouge sous `AX-D2`) : contrôle positif permanent, adossé au registre d'immuabilité — base du volet « avant » de la table de vérité.
4. **Registre d'immuabilité** : interdit la dérive silencieuse de la fixture ; impose une re-bénédiction explicite.
5. **Normaliseur + modèle canonique** : raisonnement iso-comportement sur forme normalisée.
6. **Autorité unique des chemins** (`r_mirror_1`) : pas de chemin runtime codé en dur ailleurs.
7. **`axiomes.py`** : point explicite pour **déclarer/retirer** une prémisse de domaine — levier central de CH-2 (cf. §5.3).
8. **Bascule `ARSENAL_CI_ENFORCE`** : arme la non-régression après correction.
9. **`G2` transitoire** : tripwire du franchissement CH-1 → CH-2.

**Ce qui n'existe PAS encore (et qui pèse sur CH-2) :**
- **Aucun invariant de sous-couverture** (cause réelle orpheline tombant au `else`). R-COV-1 détecte les branches **mortes** (sur-couverture), pas les **causes orphelines**.
- **Aucun invariant énumérant les consommateurs** de `chauffage_autorise_systeme`.
- **`INV-30-5` (iso-comportement) et `INV-D1/D3` sont planifiés en CH-3, donc APRÈS CH-2.** Le garde-fou thermique le plus direct **n'est pas armé pendant l'édition la plus risquée**. À CH-2, l'iso-comportement repose sur une **table de vérité manuelle**, pas sur la CI.

---

## 3. Écarts plan ↔ implémentation réelle de CH-1

Trois écarts, dont un structurant pour CH-2.

**É1 — Modèle de détection : structurel (plan) vs axiomatique (réel). [structurant]**
Le plan supposait une détection **structurelle** de D2 (Chantier 1, risque : « le court-circuit Niveau 1 doit être visible »). CH-1 a établi que la mort de 2b **n'est pas structurelle** : elle exige l'axiome externe `AX-D2-BLOCAGE-AUTORISE` (`A ≠ ()`). Conséquence directe : **le correctif D2, en sortant `blocage_aeration` de la composition de `autorise_systeme`, falsifie cet axiome.** Le plan, croyant la détection structurelle, **n'a prévu aucune gestion du cycle de vie de l'axiome en CH-2** (cf. risque R3, le plus sérieux côté CI).

**É2 — Localisation du contrôle positif R-COV-1.**
Le plan voyait « deux cibles permanentes pour R-COV-1 » (runtime vert / fixture rouge) sur une même surface. CH-1 a **bifurqué par plan** : le rouge-fixture vit dans le **self-test** (mécanisme), le verdict vivant (`job decision`) porte sur le **runtime**. Cohérent et plus propre, mais : le critère CH-2 « R-COV-1 sur la fixture (reste rouge) » correspond en réalité à « le **self-test** reste vert + le **registre d'immuabilité** reste intègre », pas à une cible-fixture dans le job `decision`.

**É3 — Artefacts de CH-1 absents du plan CH-2.**
`G2` (clôture transitoire) et le **registre d'immuabilité** ne figurent nulle part dans le périmètre CH-2 du plan, alors que `G2` **doit se déclencher au franchissement** et qu'une re-bénédiction du registre peut être requise.

---

## 4. Validation des prérequis

### 4.1 Prérequis explicitement énoncés par le plan
| Prérequis | État | Réserve |
|---|---|---|
| GATE doctrinal (N1 = retirée / N2 = déclinée ; `blocage = N2`) | **Satisfait** comme règle | Appliqué à `blocage` ; **non appliqué** au reste du jeu de raisons (cf. `stabilisation_absence`, §5.2 / R6) |
| CH-1 réalisé (garde-fous + fixture) | **Satisfait** (clos, 103 verts) | Détection axiome-dépendante (É1) |
| Décision disposition Niveau 1 = (a) | **Enregistrée** | Sa **sécurité** dépend d'un préalable non vérifié (R2) |
| `R-COV-1` rouge « en main » pour la pause | **Satisfait** (rouge runtime, warn-only) | — |

### 4.2 Prérequis load-bearing NON énoncés (et non vérifiés dans les artefacts fournis)
Ce sont les angles morts. Aucun n'est démontrable à partir du plan + changelog seuls.

- **P-a — Composition complète de `chauffage_autorise_systeme`.** Confirmer que `blocage_aeration` est le **seul** contributeur « off » que la branche N1 capturait — ou que tout autre contributeur « off » est un vrai Niveau 2 doté de sa propre branche. **Préalable obligatoire de la disposition (a).**
- **P-b — Dépendance de `desired_mode` à `autorise_systeme`.** Confirmer que la sortie `reduced` du cas blocage post-aération est atteinte par une garde **indépendante** de `autorise_systeme=off`. **Préalable obligatoire de l'iso-comportement.**
- **P-c — `stabilisation_absence` : jeton réellement émis + niveau doctrinal.** Le nom émis par le runtime et sa classification (N1/N2, impact sur `autorise_systeme`) couplent D3 et la disposition (a).
- **P-d — Énumération exhaustive des consommateurs intra-domaine** de `chauffage_autorise_systeme` (le plan ne liste que `mode.yaml`).
- **P-e — Cycle de vie de l'axiome `AX-D2`** (conserver pour la fixture, retirer/remplacer pour le runtime).
- **P-f — Plan de traitement de `G2` + re-bénédiction du registre** au franchissement.

**Conclusion §4 :** les prérequis *déclarés* sont substantiellement satisfaits ; **plusieurs prérequis porteurs sont implicites et non vérifiés.** C'est ce qui fonde un verdict conditionnel.

---

## 5. Analyse du correctif D2

### 5.1 Iso-comportement thermique — **confirmé ? NON. Plausible mais NON prouvé.**

Le piège central : **« fichier inchangé » ≠ « sortie inchangée ».** Le plan déclare `desired_mode` (l.201-209) *inchangé* et en déduit l'iso-comportement. Mais le correctif **change la valeur de `autorise_systeme`** (off → on dans le cas blocage post-aération). Si `desired_mode` **lit** `autorise_systeme` (directement ou via un intermédiaire) sur une garde atteignable dans ce cas, alors un code identique produit une **sortie différente** → régression thermique.

Réduction logique : **l'iso-comportement tient si et seulement si la garde menant à `reduced`, pour le cas blocage post-aération, ne dépend pas de `autorise_systeme=off`.**
- Pré-correction : `autorise_systeme=off` (blocage dans la composition) → `reason=chauffage_non_autorise` → `desired_mode=reduced`.
- Post-correction : `autorise_systeme=on` → `reason=blocage_aeration_en_cours` → `desired_mode` doit **rester** `reduced`.

Pour que `reduced` persiste avec `desired_mode` inchangé, il faut qu'une **autre garde** (pilotée par `blocage_aeration` / la logique d'aération, à la manière de `standby_force`) produise déjà `reduced` **sans** s'appuyer sur `autorise_systeme=off`. **Cela n'est pas démontrable depuis les documents fournis** (l.201-209 non disponibles).

**Verdict iso-comportement : à rétrograder de « garanti » à « conditionnel, à prouver ».** La preuve exige (R13) une table de vérité portant `autorise_systeme` en **colonne explicite** et calculant `desired_mode` par la **formule réelle** — sans quoi la table peut « prouver » l'iso-comportement tout en masquant la dépendance.

### 5.2 Suppression de la branche Niveau 1 (disposition (a)) — sécurité conditionnelle

La disposition (a) supprime la branche runtime `chauffage_non_autorise`. **Retirer la première branche d'une chaîne `elif` modifie ce que captent les branches suivantes et le `else`.** Avant, N1 captait **tous** les cas « non autorisé », pas seulement le blocage.

**Risque d'orphelinage :** s'il existe un contributeur « off » de `autorise_systeme` **autre** que `blocage_aeration`, la suppression de N1 laisse ce cas **tomber au `else`** — cause réelle mal étiquetée. Le plan pose lui-même la condition : suppression « tant qu'aucune cause réelle de type option retirée n'existe ». **Cette condition n'est pas vérifiée** (P-a). Vérifier la disposition (a) n'est pas rouvrir l'arbitrage : c'est **faire respecter le préalable que le plan exige déjà**.

**Angle mort CI :** **R-COV-1 ne couvre PAS ce mode de défaillance.** Il détecte les branches mortes (sur-couverture), pas les **causes orphelines** (sous-couverture). Aucun invariant de CH-1 ni de CH-2 ne garde la sous-couverture ; `INV-D1/D3` (non-remontée conséquence→cause) traite un autre objet et arrive en CH-3. **Garde manuel obligatoire.**

### 5.3 Déplacement de `blocage_aeration` vers le Niveau 2

Mécanique : retirer `blocage` de la composition de `autorise_systeme` + ranimer la branche 2b (`blocage_aeration_en_cours`) en raison N2, calquée sur `standby_force`.

Effets :
1. **`autorise_systeme` bascule off → on** dans le cas blocage → **ripple vers tous ses consommateurs** (§5.4).
2. Raison du cas blocage : `chauffage_non_autorise` → `blocage_aeration_en_cours` (réparation d'observabilité voulue).
3. **`desired_mode` doit rester `reduced`** (risque conditionnel §5.1).
4. **Ordre 2a/2b :** si `aeration_en_cours` et `blocage_aeration` peuvent être vrais simultanément, l'ordre (2a avant 2b) **décide** la raison affichée. À confirmer comme précédence doctrinale et identique au miroir.

**Conséquence CI majeure (É1 → R3) :** le correctif **falsifie `AX-D2-BLOCAGE-AUTORISE`** (la composition d'où l'axiome est tiré disparaît). Il faut **bifurquer l'axiome par plan**, sans quoi :
- **suppression globale de `AX-D2`** → le **self-test fixture passe au vert** (sans l'axiome, 2b n'est plus détectée morte sur la fixture) = **régression du vérificateur** (exactement le cauchemar du plan) ;
- **maintien de `AX-D2` dans le verdict runtime** → prémisse **fausse** injectée dans le verdict vivant : vert épistémiquement corrompu et fragile (une réintroduction future d'une garde sur `autorise_systeme` ressusciterait une fausse domination).

**Correct :** conserver `AX-D2` pour le **self-test fixture** (rouge perpétuel) ; **retirer/remplacer** l'axiome dans l'**invocation runtime** (axiomes re-dérivés de la **nouvelle** composition). **`axiomes.py` / la liaison `executer_*` doivent entrer dans le périmètre et les fichiers impactés de CH-2** — ils en sont absents.

### 5.4 Consommateurs (in)directs de `chauffage_autorise_systeme`

- **Cross-domaine : dégagé** (réserve levée ; R-DIV-3/4 : la clim ne lit pas `autorise_systeme=off` comme proxy). **Ne pas étendre ce dégagement à l'intra-domaine.**
- **Intra-domaine : non exhaustif.** Le plan ne cite que `diagnostic/mode.yaml`. **Aucun invariant n'énumère les lecteurs** de `autorise_systeme`. Tout lecteur non listé qui branche sur `autorise_systeme` voit son comportement **silencieusement modifié** dans le cas blocage. → grep exhaustif obligatoire (P-d).
- **`diagnostic/mode.yaml` :** consomme `autorise_systeme` ; sa sortie **changera probablement** (bascule off→on). Le plan l'accepte comme réparation d'observabilité — **valide uniquement si rien en aval de `mode.yaml` ne re-branche thermiquement** sur cette sortie. **Tracer la formule de `mode.yaml` ET ses propres consommateurs** (P-d/R7).

### 5.5 Impact par fichier

| Fichier | Impact | Réserve d'architecte |
|---|---|---|
| `autorisation.yaml` | Sortie de `blocage` de la composition de `autorise_systeme` (state l.56-57) | Lire la **composition complète**, pas seulement l.56-57 : confirmer l'unicité du contributeur « off » (P-a / R2) |
| `decision_centrale.yaml` | Ranimation 2b + suppression N1 dans `reason` (l.245-254) ; `desired_mode` (l.201-209) **déclaré inchangé** | « Inchangé » porte sur le **texte**, pas la **sortie** si `desired_mode` lit `autorise_systeme` (R1). Ordre 2a/2b à confirmer |
| `diagnostic/raison.yaml` | Miroir (l.80-91) : suppression N1 + ranimation 2b **symétriques** | R-MIRROR-1 garde la synchronie **si** édition symétrique et **atomique** ; confirmer le miroir 1:1 aujourd'hui |
| `diagnostic/mode.yaml` | Consommateur de `autorise_systeme` ; sortie **à prédire** | Prédire par lecture de la **formule réelle** + tracer ses consommateurs aval (R7) |
| `30_decision_centrale.md` | Table des raisons (2b N2 vivante, N1 = catégorie réservée vide) + `absence_protection_thermique` → `stabilisation_absence` (D3) | **Couplage caché** : niveau + impact-`autorise` de `stabilisation_absence` conditionne la disposition (a) (R6). Vérifier le **jeton réellement émis** avant de renommer, sinon la divergence est **déplacée, pas soldée** |
| `axiomes.py` / liaison `executer_*` | **Manquant au plan** : bifurcation de `AX-D2` (R3) | À ajouter explicitement au périmètre |
| Registre / `G2` | **Manquant au plan** : `G2` se déclenche au franchissement ; re-bénédiction éventuelle | À prévoir dans la définition de « fait » de CH-2 |

---

## 6. Risques (exhaustif, sans optimisme)

**Critiques**
- **R1 — Iso-comportement non prouvé.** `desired_mode` textuellement inchangé n'implique pas une sortie inchangée si `desired_mode` lit `autorise_systeme` sur la garde du cas blocage. Tient ssi cette garde est indépendante de `autorise_systeme=off`. *Non vérifié.*
- **R2 — Orphelinage par suppression de N1.** Sûr seulement si `blocage` est le seul contributeur « off » capté par N1 (ou les autres sont N2 avec branche propre). **R-COV-1 aveugle à ce cas.** *Composition non vérifiée.*
- **R3 — Axiome `AX-D2` falsifié par le correctif.** Bifurquer (fixture : garder / runtime : retirer-remplacer). Suppression globale → self-test fixture vert (régression vérificateur) ; maintien runtime → vert corrompu/fragile. **Absent des fichiers impactés du plan.**

**Élevés**
- **R4 — Écart de modèle de détection (structurel→axiomatique).** Racine de R3 ; impose une gestion d'axiome que le plan ignore.
- **R5 — Consommateurs `autorise_systeme` possiblement incomplets** (intra-domaine non exhaustif, aucun invariant d'énumération).
- **R6 — `stabilisation_absence` : niveau + jeton.** Si c'est une vraie cause N1 pilotant `autorise=off`, la disposition (a) casse. Renommage D3 doit cibler le **vrai** jeton émis.

**Moyens**
- **R7 — Aval de `diagnostic/mode.yaml`** non tracé (sortie qui change ; re-branchement thermique éventuel).
- **R8 — `G2` se déclenche au franchissement** (par conception) : à anticiper et retirer/mettre à jour, ne pas confondre avec une régression ; re-bénédiction possible.
- **R9 — Séquencement de `ARSENAL_CI_ENFORCE`** non explicité (bascule trop tôt = blocage sur désync transitoire ; oubli = non-régression non armée).
- **R10 — Édition non atomique** cerveau/miroir → R-MIRROR-1 rouge transitoire + désync R-DIV-1 au reload.
- **R11 — `INV-30-5` en CH-3, après CH-2** : garde thermique non armé pendant l'édition la plus risquée ; preuve iso-comportement seulement manuelle.

**Faibles à moyens**
- **R12 — Ordre 2a/2b** si `aeration` et `blocage` peuvent coexister.
- **R13 — Table de vérité auto-aveugle** : doit porter `autorise_systeme` en colonne + `desired_mode` par formule réelle.
- **R14 — Contrat 30 : N1** doit apparaître comme catégorie **réservée vide**, sans raison fantôme active.
- **R15 — `standby_force` comme patron** : vérifier que l'exemplaire est lui-même correct et transposable.

---

## 7. Points à vérifier avant implémentation

1. **Composition complète de `chauffage_autorise_systeme`** (tous contributeurs « off ») → unicité de `blocage` ou N2-avec-branche pour les autres. *(P-a / R2)*
2. **Cascade `desired_mode` (l.201-209)** : la garde `reduced` du cas blocage est-elle indépendante de `autorise_systeme` ? Si non → `desired_mode` peut nécessiter une édition **non planifiée**. *(R1)*
3. **`stabilisation_absence`** : jeton réellement émis par le runtime + niveau doctrinal + impact `autorise`. Réconcilier avec la disposition (a) et D3. *(R6)*
4. **Grep exhaustif** de `chauffage_autorise_systeme` (template sensors, automations, briques UI, scripts) → ensemble de consommateurs + delta prédit par consommateur. *(R5)*
5. **Formule et consommateurs de `diagnostic/mode.yaml`** → effet aval éventuel. *(R7)*
6. **Cycle de vie de `AX-D2`** : conserver (fixture/self-test) / retirer-remplacer (verdict runtime) ; intégrer `axiomes.py` / `executer_*` au périmètre. *(R3)*
7. **Traitement de `G2`** : attendu déclenché ; plan de retrait/mise à jour ; re-bénédiction registre éventuelle. *(R8)*
8. **Miroir 1:1 aujourd'hui** (R-MIRROR-1 vert) → édition symétrique N1/2b planifiée.
9. **Table de vérité avant/après** avec `autorise_systeme` en colonne explicite et `desired_mode` par formule réelle ; `desired_mode` identique sur toutes les lignes. *(R13)*
10. **Ordre 2a/2b** + disjonction + conformité au patron `standby_force`. *(R12/R15)*
11. **Timing de la bascule `ARSENAL_CI_ENFORCE`** (après vert runtime + preuve complète). *(R9)*

---

## 8. Pièges possibles

- **T1 — « Fichier inchangé donc sortie inchangée ».** Faux dès qu'une entrée (`autorise_systeme`) change de valeur. Prouver sur les **sorties**, pas sur les diffs.
- **T2 — Suppression globale de `AX-D2`** pour « verdir » le runtime → verdit aussi la fixture = perte silencieuse du contrôle positif.
- **T3 — « Faire passer le test »** en bricolant moteur/alias au lieu de corriger la cause réelle (la fixture doit rester rouge *par* l'axiome, pas par complaisance).
- **T4 — Table de vérité qui abstrait `autorise_systeme`** : prouve un faux iso-comportement.
- **T5 — Traiter le déclenchement de `G2` comme une régression** et revenir en arrière : c'est un tripwire **voulu**.
- **T6 — Renommer le jeton du contrat (D3) sans vérifier l'émission runtime** : déplace la divergence.
- **T7 — Commit non atomique** : R-MIRROR-1/R-DIV-1 rouges en cours d'édition ; si `ENFORCE` déjà bloquant, blocage en plein milieu.
- **T8 — Confondre dégagement cross-domaine et intra-domaine** : R-DIV-3/4 ne couvrent que la clim.
- **T9 — Déléguer entièrement l'iso-comportement à `INV-30-5` (CH-3)** : à CH-2 il n'est pas armé.

---

## 9. Recommandations

1. **Promouvoir les prérequis implicites en GATES écrits** (P-a composition, P-b `desired_mode`, P-c `stabilisation_absence`, P-d consommateurs) — un constat documenté **avant toute édition**.
2. **Intégrer le cycle de vie de l'axiome** à CH-2 (fichiers : `axiomes.py`, liaison `executer_*`) avec la bifurcation explicite fixture/runtime.
3. **Spécifier la table avant/après** avec `autorise_systeme` en colonne et `desired_mode` par formule réelle ; en faire la **preuve liante** d'iso-comportement.
4. **Avancer `INV-30-5` en warn-only** sur le runtime corrigé dans l'acceptation de CH-2 — ou **accepter explicitement** le garde manuel, les yeux ouverts.
5. **Inscrire `G2` + re-bénédiction** dans la définition de « fait » de CH-2.
6. **Séquencer la bascule `ENFORCE`** : seulement après R-COV-1 runtime vert **et** preuve avant/après complète.
7. **Commit atomique et réversible** (composition + cerveau + miroir + contrat + CI-axiome) ; iso-comportement prouvé **hors-ligne avant** commit.
8. **Clause d'arrêt :** si l'audit de composition révèle un contributeur « option retirée » réel, **stopper** et reconsidérer la disposition (a) (conserver/relibeller N1) — **ne pas** supprimer la branche dans ce cas. *(Application de la condition que le plan pose déjà, sans réouverture de l'arbitrage.)*

---

## 10. Verdict

### NO-GO en l'état — GO conditionnel

L'architecture de CH-1 est saine et fournit de bons garde-fous (R-COV-1, R-MIRROR-1, fixture, immuabilité). Le plan CH-2 est globalement cohérent et l'iso-comportement est **plausible**. Mais trois prérequis **porteurs et non vérifiés** dans les artefacts fournis interdisent de toucher le runtime maintenant :

- **R1** — la dépendance de `desired_mode` à `autorise_systeme` (l'iso-comportement n'est pas prouvé) ;
- **R2** — l'unicité du contributeur « off » de `autorise_systeme` (la suppression de N1 peut orpheliner une cause réelle, hors radar R-COV-1) ;
- **R3** — la falsification de `AX-D2` par le correctif (bifurcation d'axiome absente du plan).

**Conditions de bascule en GO** — fermer, par constat écrit :
1. `desired_mode` : garde `reduced` du cas blocage **indépendante** de `autorise_systeme` ; *(sinon, replanifier une édition de `desired_mode`)*
2. composition de `autorise_systeme` : `blocage` **seul** contributeur « off » capté par N1, ou autres contributeurs **N2 dotés de branche** ;
3. `stabilisation_absence` : **jeton réel** + **niveau** réconciliés avec la disposition (a) et D3 ;
4. cycle de vie de `AX-D2` **spécifié** (fixture : conserver / runtime : retirer-remplacer) et `axiomes.py` intégré au périmètre ;
5. ensemble des consommateurs de `autorise_systeme` **énuméré** et delta prédit ;
6. `G2` + re-bénédiction **planifiés**.

Tant que 1 à 4 (a minima) ne sont pas tranchés par lecture du runtime, **l'iso-comportement reste non prouvé et la disposition (a) reste non sûre.** Une fois ces gates fermés, CH-2 redevient un correctif petit, atomique et bien gardé : **GO.**
