# Arsenal CI — Changelog du chantier CH-3

**Chantier** : CH-3 — Invariants comportementaux pivots de l'étage 2 (région `decision`)
**Domaine** : Chauffage
**Date** : 2026-05-30
**État** : clos — 119 tests verts, verdict décision conforme, 0 modification du runtime Chauffage

---

## Résumé architectural

CH-3 complète l'**étage 2** du validateur Arsenal CI avec les deux invariants
comportementaux à fort rendement issus de la dette D6 : la non-remontée d'une
conséquence en cause (`R-CAUSE-1`) et l'iso-comportement de la décision centrale
au niveau du squelette de tête (`R-ISO-1`). Le substrat de modélisation des
cascades gagne une émission dynamique, ce qui rend la cascade `desired_mode`
analysable. Les deux règles sont intégrées au verdict étage 2 sur le runtime
vivant. L'étage 1, la clôture CH-1 et les contrôles existants restent intacts.

Le domaine Chauffage dispose désormais d'une couverture comportementale qui ne
se limite plus à l'atteignabilité (`R-COV-1`) et à la synchronie cerveau ↔
miroir (`R-MIRROR-1`) : la **causalité honnête** des raisons émises et la
**non-désynchronisation des causes majeures** entre l'axe thermique et l'axe
narration sont maintenant garanties en continu.

---

## 1. Nouveaux invariants (région `decision`)

### R-CAUSE-1 — non-remontée conséquence → cause (`r_cause_1.py`, libellé doctrinal INV-D1/D3)
Le système garantit qu'aucune branche de la cascade de raison n'émet un jeton
classé comme **conséquence** — un nom d'état d'autorisation composé, dérivé de la
décision — à la place d'une cause déclenchante. La règle généralise en garde
permanent la pathologie D1/D2 (« causalité menteuse »), dont D2 est le spécimen
canonique. Émissions statiques inspectées en profondeur (tête et sous-cascades) ;
émissions dynamiques exclues, non classables statiquement.

La partition cause/conséquence est une **prémisse externe re-déclarée**
(`partition_causes.py`), jamais lue du runtime, de source contrat
`30_decision_centrale.md` §4 et table des raisons. Elle contient le seul jeton
réellement caractérisé comme conséquence : `chauffage_non_autorise` (catégorie
Niveau 1 réservée, non émise depuis CH-2, qui nomme le composé
`binary_sensor.chauffage_autorise_systeme`). Partition volontairement minimale.

**Doubles cibles permanentes**, par construction :
- runtime corrigé → **vert** (contrôle négatif ; un rouge ultérieur = la
  conséquence est redevenue émise, régression réelle du domaine) ;
- fixture gelée `d2_reason_pre_correction.yaml` → **rouge** (contrôle positif ;
  elle émet `chauffage_non_autorise` ; un vert = régression du vérificateur).

La fixture D2 devient ainsi le contrôle positif permanent de `R-COV-1` **et** de
`R-CAUSE-1`.

### R-ISO-1 — iso-comportement de la décision centrale (`r_iso_1.py`, libellé doctrinal INV-30-5)
Le système garantit que les deux axes de la décision centrale arbitrent les
**mêmes causes majeures de premier rang dans le même ordre** : l'axe thermique
(cascade `desired_mode`) et l'axe narration (cascade `reason`). La comparaison
porte sur la séquence des gardes de tête et leur ordre. Une branche de tête ne
peut être ajoutée, retirée ou réordonnée sur un axe sans être reflétée sur
l'autre, sous peine de violation localisée — c'est la désynchronisation que D2
incarnait au niveau de la composition d'autorisation. Vert sur le runtime
corrigé (gardes de tête `reason` ≡ `desired_mode`).

**Portée assumée.** `R-ISO-1` ne prouve pas l'iso-comportement complet de la
décision centrale ; il garantit uniquement l'isomorphisme des gardes de tête —
la non-désynchronisation des causes majeures de premier rang. Sont exclus de la
garantie : l'équivalence interne des sous-cascades (présence, vacances), dont la
profondeur peut légitimement diverger entre les deux axes, et l'équivalence des
**valeurs** de `desired_mode` (iso thermique par cas), dont la preuve reste la
table de vérité avant/après établie hors-ligne en CH-2.

---

## 2. Évolution du substrat de décision

### Émission dynamique (`model.py`, `normaliseur.py`)
Le modèle canonique de cascade représente désormais fidèlement une **feuille
dynamique** `{{ <variable> }}` simple — une valeur transmise telle quelle au
runtime —, distincte d'une émission de jeton statique et dotée de sa propre
variante de signature structurelle. Le normaliseur l'accepte ; toute expression
`{{ }}` plus riche (appel, opérateur) reste *fail-closed*.

Conséquence dans le système : la cascade `desired_mode` de la décision centrale,
qui collapse la branche présence en `{{ cible }}`, est désormais **normalisable**
— condition préalable à `R-ISO-1`. La surface modélisable du substrat décision
est étendue sans rupture : `R-COV-1` et `R-MIRROR-1` sont **fonctionnellement
inchangés**, les cascades `reason`/`state` ne portant aucune feuille dynamique et
conservant des signatures identiques.

---

## 3. Intégration au verdict étage 2

### Surface de verdict (`cli_decision.py`)
Le verdict décision sur le runtime vivant applique désormais **quatre** règles —
`R-COV-1`, `R-MIRROR-1`, `R-CAUSE-1`, `R-ISO-1` — agrégées en un unique `Result`
aux codes de sortie 0/1/2 inchangés. Les deux nouvelles règles lisent le runtime
en seule lecture via l'**autorité unique de localisation** (`r_mirror_1`) ; aucun
chemin runtime n'est codé en dur dans la surface de verdict. `R-CAUSE-1` porte
sur la cascade `reason` ; `R-ISO-1` sur le couple `reason` ↔ `desired_mode` du
même fichier.

### Couverture des tests (`test_lot_2_8.py`, `test_lot_2_9.py`)
Le self-test porte deux nouveaux lots : 2.8 (R-CAUSE-1) et 2.9 (R-ISO-1), chacun
distinguant la preuve hermétique du mécanisme du constat en lecture seule sur le
dépôt. Le lot de clôture CH-1 (`test_lot_2_7`) et ses invariants globaux G1–G5
restent intacts ; l'isolation étage 1 / étage 2 (`orchestrator.RULES`) est
préservée.

---

## 4. Garanties apportées

- **Causalité honnête** : aucune raison émise par la décision Chauffage ne peut
  nommer une conséquence à la place de sa cause sans faire rougir la CI —
  garantie permanente, vérifiée par double contrôle (fixture rouge, runtime
  vert).
- **Non-désynchronisation des causes majeures** : le squelette de décision de
  premier rang ne peut diverger entre l'axe thermique et l'axe narration sans
  faire rougir la CI.
- **Fidélité du substrat** : la feuille dynamique du runtime est modélisée, non
  silencieusement rejetée ; la cascade `desired_mode` entre dans le périmètre
  d'analyse.
- **Non-régression de l'existant** : `R-COV-1`, `R-MIRROR-1` et l'étage 1 sont
  inchangés ; la fixture D2 reste gelée et devient contrôle positif partagé.
- **Verdict élargi sans dette de divergence** : les quatre règles partagent un
  même substrat de normalisation et une même autorité de localisation.

---

## 5. Hors périmètre (explicite)

- **Iso-comportement complet** : l'équivalence interne des sous-cascades et
  l'équivalence des valeurs de `desired_mode` ne sont pas couvertes par
  `R-ISO-1` ; la preuve thermique par cas demeure la table avant/après de CH-2.
- **Invariants résiduels de l'étage 2** (`R-VOC-1/2`, `R-REG-MIX-1`,
  `INV-STANDBY-*`) : non construits — rendement marginal décroissant une fois
  les pivots posés. Réactivables seulement sur régression concrète.
- **CH-4 — contractualisation du retry** : non traité.
- **Runtime Chauffage, fixture D2, changelogs historiques, workflow CI** :
  intacts. Les nouveaux lots sont ramassés par le job self-test existant ; les
  nouvelles règles sont portées par la surface de verdict existante. Aucun fichier
  hors `tools/arsenal_ci/` n'est modifié.

---

## État de validation

- 119 tests Arsenal CI verts (lots 1.x, 2.0 à 2.9).
- verdict `cli_decision` conforme : R-COV-1 = 0, R-MIRROR-1 = [], R-CAUSE-1 = 0,
  R-ISO-1 = [] sur le runtime corrigé.
- contrôles positifs sur la fixture D2 gelée : R-COV-1 rouge, R-CAUSE-1 rouge.
- isolation étage 1 / étage 2 préservée (`orchestrator.RULES` inchangé).

---

## Clôture du chantier CH-3

CH-3 est clos. L'étage 2 du validateur Arsenal CI couvre désormais la causalité
des raisons (`R-CAUSE-1`) et l'iso-comportement de premier rang de la décision
centrale (`R-ISO-1`), en sus de la couverture (`R-COV-1`) et de la synchronie
(`R-MIRROR-1`). Le substrat de décision modélise la feuille dynamique du
runtime ; le verdict étage 2 porte les quatre règles sur la configuration
vivante. La fixture D2 demeure le contrôle positif permanent, étendu à
`R-CAUSE-1`.

Le sous-ensemble pivot de D6 est livré ; la suite résiduelle d'invariants reste
explicitement différée. La frontière vers CH-4 (contractualisation du retry
transactionnel) demeure ouverte et indépendante.
