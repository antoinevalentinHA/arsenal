# Arsenal CI — Changelog du chantier CH-1

**Chantier** : CH-1 — Verrouillage CI de l'étage 2 (région `decision`)
**Domaine** : Chauffage
**Date** : 2026-05-29
**État** : clos — 103 tests verts, 0 modification du runtime Chauffage

---

## Résumé architectural

CH-1 établit l'**étage 2** du validateur Arsenal CI. L'étage 1 valide la
*structure* de la configuration (graphe d'entités, taxonomies, règles
doctrinales). L'étage 2 valide la *logique décisionnelle* : il normalise les
cascades de décision Home Assistant en un modèle canonique, puis applique des
règles de couverture et de synchronie.

Le chantier livre une région autonome `tools/arsenal_ci/decision/`, deux règles
opérationnelles (R-COV-1, R-MIRROR-1), un moteur général de détection
d'inatteignabilité, une fixture canonique gelée, un registre d'immuabilité, une
surface CI dédiée et un job GitHub Actions associé. La dette D2 (branche morte
dans la cascade de décision Chauffage) est désormais **mesurée, gelée et
surveillée** — mais non corrigée : sa correction est réservée à CH-2.

---

## 1. Infrastructure Arsenal CI

Composants génériques, indépendants du domaine, réutilisables par tout futur
domaine doté de cascades décisionnelles.

### Région `tools/arsenal_ci/decision/`
Nouvel étage du validateur, isolé du pipeline graphe de l'étage 1. Objectif
métier : disposer d'un emplacement architectural unique pour l'analyse de la
logique de décision, distinct de l'analyse structurelle.

### Modèle canonique de cascade (`model.py`)
Représentation immuable et ordonnée d'une cascade `if/elif/else` : gardes
(`AtomeEtat`, `AtomeVar`, `Non`, `Et`, `Ou`, `Else`), liaisons, émissions,
sous-cascades. Expose une signature structurelle déterministe excluant la
provenance. Objectif métier : rendre une cascade *comparable* et *analysable* de
façon stable, condition préalable à toute vérification automatique.

### Normaliseur de cascades (`normaliseur.py`)
Conversion d'une cascade Jinja (lue en seule lecture) en modèle canonique, en
deux étages : extraction du scalaire via `yaml.safe_load`, puis analyse du flot
de contrôle par tokeniseur borné et mini-parseur de garde sur une grammaire
close (`is_state`, `not`, `and`, `or`, `==`, `in`). Discipline *fail-closed* :
toute construction hors grammaire lève une erreur explicite, jamais un silence.
Objectif métier : transformer une logique écrite pour l'exécution en un objet
vérifiable, sans dépendance nouvelle.

### Table d'alias syntaxique (`alias.py`)
Vocabulaire canonique d'atomes. Couche de **normalisation syntaxique
uniquement** : identité de référence, aucune sémantique métier, aucune relation
de domination, implication, atteignabilité ni connaissance de domaine. Objectif
métier : stabiliser la représentation des prédicats sans jamais déduire ni
fusionner d'atomes distincts.

### Moteur général d'inatteignabilité — R-COV-1 (`r_cov_1.py`)
Détection de branches de tête inatteignables en sémantique premier-match. La
satisfiabilité décidée est `A ∧ G_i ∧ (et_{j<i} non G_j)`, où l'ensemble
d'axiomes `A` est un jeu de contraintes additionnel, optionnel, par défaut vide.
Décision par évaluation exhaustive de table de vérité (stdlib seule, plafond
d'atomes en garde *fail-closed*). Objectif métier : signaler les branches de
décision mortes — bugs latents et complexité trompeuse — qu'aucune relecture
manuelle ne garantit de détecter. Sous `A = ()` le moteur détecte la domination
purement structurelle ; sous `A ≠ ()` il détecte la domination conditionnée par
des axiomes déclarés.

### Comparateur de synchronie — R-MIRROR-1 (`r_mirror_1.py`)
Comparaison structurelle de deux cascades normalisées via leur signature ;
divergences localisées par branche (garde, liaisons, issue, sous-cascade) ou par
nombre de branches. Objectif métier : garantir qu'un miroir diagnostic reflète
fidèlement la décision réelle. La forme (commentaires, espacement, style de
bloc) est ignorée ; seul le sens structurel est comparé.

### Surface CI étage 2 (`cli_decision.py`)
Agrégation des règles étage 2 en un `Result` réutilisant les primitives de
rapport de l'étage 1 (`Violation`, `Summary`, `ExitCode`, formatters). Codes de
sortie 0/1/2 identiques à l'étage 1. Objectif métier : porter le verdict de la
logique décisionnelle en intégration continue, avec un rapport JSON exploitable.

### Registre d'immuabilité (`tests/test_lot_2_6.py`)
Manifeste des artefacts canoniques gelés (empreinte SHA256 des octets bruts,
chemins relatifs invariants au clonage). Deux propriétés : **intégrité** (aucun
artefact enregistré n'a changé) et **couverture** (aucun artefact canonique
n'échappe au verrou). Procédure de re-bénédiction documentée. Objectif métier :
garantir qu'une référence gelée ne dérive jamais silencieusement.

### Workflow GitHub Actions (`arsenal-ci-chauffage.yml`)
Job `decision` dédié, parallèle au job `lint`, conditionné au self-test, avec
publication d'un artifact JSON. Objectif métier : exécuter le verdict étage 2 à
chaque évolution pertinente de la configuration ou de l'outil.

---

## 2. Chauffage

Instances spécifiques au domaine, liant les composants génériques à la
configuration Chauffage réelle.

### Fixture canonique D2 (`d2_reason_pre_correction.yaml`)
Photographie structurelle figée de la cascade `reason` de décision Chauffage,
dans son état pré-correction. La branche de blocage d'aération
(`blocage_aeration_en_cours`) y est structurellement présente mais logiquement
morte. Objectif métier : ancre de régression du moteur et référence stable de la
pathologie D2, indépendante de l'évolution du runtime.

### Axiome `AX-D2-BLOCAGE-AUTORISE` (`axiomes.py`)
Prémisse externe déclarée : `blocage_aeration='on' ⇒ autorise_systeme!='on'`,
issue de la composition de `autorise_systeme` dans `autorisation.yaml`. Objectif
métier : fournir au moteur la vérité de domaine qui démontre l'inatteignabilité
de la branche morte, sans l'inscrire dans la fixture ni dans la table d'alias.

### Pathologie D2 détectée (non corrigée)
La branche `blocage_aeration_en_cours` est dominée par la branche
`chauffage_non_autorise` sous l'axiome ci-dessus : le blocage d'aération retirant
l'autorisation système, la garde de blocage n'est jamais atteinte en premier.
R-COV-1 émet la violation correspondante. Objectif métier : rendre la dette
visible et qualifiée, en vue de sa correction en CH-2.

### Paire cerveau ↔ miroir
Descripteurs canoniques de localisation, source unique pour tout l'étage 2 :
cerveau `10_scripts/chauffage/decision_centrale.yaml` clé `reason`, miroir
`12_template_sensors/chauffage/diagnostic/raison.yaml` clé `state`. R-MIRROR-1
constate leur synchronie sur le runtime vivant. Objectif métier : empêcher que
le diagnostic affiché diverge silencieusement de la décision effective.

### Instance CH-1 du verdict (`cli_decision.executer_ch1`)
Liaison des règles aux entrées Chauffage : R-COV-1 sur la cascade `reason` du
runtime avec `AXIOMES_D2`, R-MIRROR-1 sur la paire runtime. La fixture est
réservée au self-test ; le verdict CI porte sur la configuration vivante.

---

## 3. Gouvernance / Qualité

### Invariants verrouillés
- **Table d'alias** : normalisation syntaxique seule ; deux entités distinctes
  restent deux atomes distincts, quelle que soit une relation logique ailleurs.
- **R-COV-1 généraliste** : moteur général ; les axiomes sont des contraintes
  additionnelles ; D2 est l'instance `A = {AX-D2}`, sans traitement particulier.
- **Fixture vs runtime** : la fixture est l'ancre de régression et
  d'immuabilité (self-test) ; le runtime est la cible du verdict vivant (job
  `decision`). Une dette figée n'est pas une cible de gouvernance.
- **Source unique de localisation** : `r_mirror_1` est l'autorité des chemins
  cerveau/miroir ; aucun chemin runtime n'est codé en dur ailleurs.

### Séparation des plans
- **self-test** : l'outil est-il sain ? (suite hermétique, binaire) ;
- **lint** : la configuration enfreint-elle la doctrine structurelle ? ;
- **decision** : la logique décisionnelle enfreint-elle couverture et
  synchronie ?

Les plans 2 et 3 produisent des verdicts gated ; le plan 1 reste un contrôle de
santé indépendant.

### Bascule warn-only → bloquant
La variable `ARSENAL_CI_ENFORCE` gouverne lint et decision. En phase warn-only,
une violation (exit 1) est signalée sans bloquer ; une erreur d'exécution
(exit 2) bloque dans toutes les phases. La bascule en mode bloquant est un diff
unique, traçable, postérieur à la correction de la dette qu'elle armerait.
Objectif métier : surveiller une dette connue sans bloquer la livraison, puis
verrouiller la non-régression une fois la dette résolue.

### Distinction du statut épistémique des tests
- Cas synthétiques : prouvent le mécanisme ; leur échec est un défaut d'outil.
- Constats runtime et snapshot de clôture : observent l'état du dépôt ; leur
  échec signale une dérive ou un franchissement de chantier, pas un défaut
  d'outil. L'invariant de clôture G2 est explicitement transitoire.

### Registre d'immuabilité comme gouvernance
Toute modification d'un artefact gelé est interdite silencieusement : elle exige
une re-bénédiction explicite (recalcul d'empreinte, diff d'une ligne, revue).

### Résultat qualité
103 tests verts (lots 1.x, 2.0 à 2.7). Isolation étage 1 / étage 2 vérifiée :
le jeu de règles graphe (`orchestrator.RULES`) reste inchangé ; aucune règle
étage 2 n'y est câblée.

---

## Réalisation sans modification du runtime Chauffage

CH-1 a été réalisé **sans aucune modification de la configuration Home Assistant
Chauffage**. Aucun fichier de `10_scripts/chauffage/` ni de
`12_template_sensors/chauffage/` n'a été altéré. La cascade de décision, son
miroir et la composition d'autorisation sont restés intacts. La pathologie D2
est observée et qualifiée, jamais corrigée. L'ensemble du chantier est confiné à
l'outillage (`tools/arsenal_ci/decision/`), aux tests, à la fixture gelée et au
workflow CI.

---

## Clôture du chantier CH-1

CH-1 est clos. L'étage 2 du validateur Arsenal CI est opérationnel : la logique
décisionnelle du domaine Chauffage est désormais normalisée, vérifiée en
couverture (R-COV-1) et en synchronie (R-MIRROR-1), portée en intégration
continue et protégée par un registre d'immuabilité. La dette D2 est mesurée,
gelée et surveillée en mode warn-only.

Le chantier laisse une frontière explicite vers CH-2 : la correction de D2 fera
disparaître la violation de couverture sur le runtime vivant et déclenchera le
snapshot de clôture transitoire (G2), signalant le franchissement CH-1 → CH-2.
La correction devra être appliquée simultanément au cerveau et au miroir, sous
peine de rupture de synchronie (R-MIRROR-1) ; elle ouvrira la voie à la bascule
de `ARSENAL_CI_ENFORCE` en mode bloquant, armant la non-régression définitive de
la logique décisionnelle Chauffage.
