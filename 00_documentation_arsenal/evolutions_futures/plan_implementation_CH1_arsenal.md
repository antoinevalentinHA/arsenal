# Plan d'implémentation — CH-1 (Verrouillage CI étage 2)

**Type :** plan d'implémentation d'exécution (chantier unique)
**Source de vérité amont :** `plan_action_chauffage_arsenal.md` (29/05/2026) — approuvé, non négociable
**Périmètre :** CH-1 uniquement (fixture canonique D2 + `R-COV-1` + `R-MIRROR-1` + raccordement CI). Couvre D5 intégralement, amorce D6.
**Hors périmètre (verrouillé) :** correctif runtime D2, alignement contrat 30, disposition Niveau 1 (→ CH-2 / PAUSE) ; invariants pivots `INV-30-5`, `INV-D1/D3` (→ CH-3).
**Invariant transverse du chantier :** **aucun fichier runtime modifié.** Le runtime est lu en seule lecture par le harnais. Tout artefact produit est nouveau et confiné à l'arbre `tests` / CI / fixtures / doc.
**Date :** 29/05/2026

---

## 1. Décomposition du chantier

Sept sous-tâches atomiques. T0→T1 posent le substrat partagé ; T2 fige l'oracle ; T3/T4 sont les deux invariants ; T5 raccorde la CI ; T6/T7 verrouillent l'immuabilité et la non-régression. Le substrat de normalisation (T1) est mutualisé entre `R-COV-1` et `R-MIRROR-1` : une seule couche de parsing, donc une seule source de dérive possible.

### T0 — Scaffold étage 2
- **Objectif.** Créer le squelette du harnais étage 2 calqué sur l'arborescence de l'étage 1 existant, découvrable par le même runner. Réutiliser la taxonomie `registres_entites.yaml` (pas de redéfinition).
- **Fichiers concernés.** Nouveau sous-arbre étage 2 (chemin hérité de l'étage 1, p. ex. `tests/etage2/`) ; point d'entrée du runner étendu pour collecter l'étage 2. Aucun fichier runtime.
- **Dépendances.** Aucune.
- **Critère de fin.** La suite étage 2 (vide d'invariants) est collectée et s'exécute en vert localement ; l'étage 1 reste collecté et inchangé.

### T1 — Normaliseur de cascade (substrat partagé)
- **Objectif.** Convertir une cascade `reason` (la chaîne `if/elif`) en **modèle abstrait ordonné** : liste de couples `(garde_normalisée, raison_émise)`, sur un **vocabulaire de prédicats canonique** (table d'alias explicite). Le normaliseur lit le runtime en lecture seule.
- **Fichiers concernés.** Module normaliseur dans l'arbre étage 2 ; table d'alias canonique (vocabulaire partagé). Lit `10_scripts/chauffage/decision_centrale.yaml` (cascade `reason`, l.245-254) et `12_template_sensors/chauffage/diagnostic/raison.yaml` (miroir, l.80-91). Aucune écriture runtime.
- **Dépendances.** T0.
- **Critère de fin.** Le normaliseur produit un modèle **déterministe** (stable au snapshot) pour les deux cascades ; toute garde non parsable lève une **erreur explicite** (fail-closed), jamais un silence.

### T2 — Fixture canonique D2 (capture-puis-gel)
- **Objectif.** Figer le snapshot structurel de la cascade `reason` **pré-correction** dans son format normalisé (état pathologique : branche `blocage_aeration_en_cours` morte, raison `chauffage_non_autorise` menteuse sur le cas blocage post-aération).
- **Fichiers concernés.** Nouveau fichier fixture autonome (arbre fixtures étage 2) + empreinte de référence enregistrée + bannière d'en-tête « immuable ». Aucun fichier runtime.
- **Dépendances.** T1 (le format de la fixture *est* la sortie normalisée). Le runtime étant aujourd'hui encore en état pré-correction, la capture s'effectue sur l'état courant **puis** est découplée : la fixture ne référence plus jamais le runtime vivant.
- **Critère de fin.** Fixture committée, autonome (zéro pointeur runtime), empreinte enregistrée, bannière présente.

### T3 — `R-COV-1` (atteignabilité)
- **Objectif.** Sur un modèle normalisé, déterminer pour **chaque branche présente** s'il existe une affectation d'entrées qui l'atteint (sa garde vraie, toutes les gardes antérieures fausses). Rouge si une branche présente est inatteignable, en la **nommant**.
- **Fichiers concernés.** Module `R-COV-1` (arbre étage 2). Aucun fichier runtime.
- **Dépendances.** T1, T2.
- **Critère de fin.** `R-COV-1` exécuté **sur la fixture** → **ROUGE**, désignant nommément `blocage_aeration_en_cours`. Le test enveloppant **passe** (vert CI) quand le détecteur rougit correctement la fixture (contrôle positif).

### T4 — `R-MIRROR-1` (synchronisation des cascades)
- **Objectif.** Comparer les deux cascades normalisées (cerveau `decision_centrale` vs miroir `diagnostic/raison`) sur **ordre + gardes + raisons**, par comparaison structurelle normalisée (cf. §4), pas par égalité textuelle.
- **Fichiers concernés.** Module `R-MIRROR-1` (arbre étage 2) ; réutilise la table d'alias de T1. Aucun fichier runtime.
- **Dépendances.** T1.
- **Critère de fin.** `R-MIRROR-1` exécuté sur le runtime courant → **VERT** (les deux cascades sont aujourd'hui synchrones dans leur défaut partagé).

### T5 — Raccordement au pipeline CI
- **Objectif.** Ajouter un job « étage 2 » au workflow GitHub Actions de `antoinevalentinHA/arsenal`, en aval (ou en dépendance) du job étage 1.
- **Fichiers concernés.** Workflow `.github/workflows/…` (job étage 2). Aucun fichier runtime.
- **Dépendances.** T0–T4.
- **Critère de fin.** Le pipeline complet est **vert** : étage 1 vert ; immuabilité fixture verte ; `R-COV-1` (contrôle positif fixture) vert ; `R-MIRROR-1` vert. Le **gate runtime de `R-COV-1` n'est pas activé** (relève de CH-2).

### T6 — Garde d'immuabilité de la fixture
- **Objectif.** Empêcher toute réécriture / régénération silencieuse de la fixture (extension de la famille `META-2`).
- **Fichiers concernés.** Méta-test d'empreinte (arbre étage 2). Aucun fichier runtime.
- **Dépendances.** T2.
- **Critère de fin.** Le méta-test échoue si le contenu de la fixture dérive de l'empreinte enregistrée ; vert sur la fixture committée.

### T7 — Non-régression étage 1
- **Objectif.** Garantir que l'ajout de l'étage 2 ne perturbe pas l'étage 1.
- **Fichiers concernés.** Aucun (exécution de la suite existante).
- **Dépendances.** T5.
- **Critère de fin.** `R-CI-1`, double fixture, `META-2` : inchangés et verts.

---

## 2. Fixture canonique D2

**Nature.** Snapshot **structurel** figé du bloc `reason` pré-correction de `decision_centrale.yaml`, sous forme normalisée (sortie de T1). C'est le **contrôle positif permanent** de `R-COV-1` : la première occurrence caractérisée de « conséquence remontée en cause ». **La table de vérité n'est pas la fixture** — la table avant/après reste un artefact comportemental complémentaire, produit hors-ligne en CH-2.

### Ce qui doit être figé
- La **liste ordonnée** des branches `reason` telles qu'elles existent pré-correction (l'ordre est porteur de la pathologie).
- Pour chaque branche : la **raison émise** et la **garde** sous forme normalisée (vocabulaire de prédicats canonique).
- La structure exacte qui rend `blocage_aeration_en_cours` (2b) inatteignable : la branche Niveau 1 `chauffage_non_autorise`, à garde trop large, placée **avant** 2b.

### Ce qui ne doit pas être figé
- La **table de vérité** (mappings entrées → `desired_mode`/`reason`) — artefact distinct.
- Le **fichier `decision_centrale.yaml` entier** — seul le bloc cascade `reason` est capturé, pas `desired_mode` (l.201-209) ni le reste.
- La **rédaction brute** : commentaires, indentation, ordre des opérandes d'une même garde, formatage Jinja. Seule la **logique** est figée (gardes canonicalisées), pas leur écriture.

### Emplacement recommandé
Dans l'arbre fixtures de l'étage 2, au même rang de gel que les changelogs historiques (jamais réécrits). Chemin hérité de l'arborescence étage 1 — illustrativement `tests/etage2/fixtures/d2_reason_cascade_precorrection.<ext>`, à conformer à la convention en place.

### Format recommandé
**Déclaratif structuré (YAML), pas YAML/Jinja runtime brut.** Justification : la fixture doit survivre à un reformatage du runtime sans changer de sens ; un snapshot brut figerait la rédaction (ce que le plan proscrit) et coupletait l'oracle à la syntaxe d'origine. Le format normalisé est exactement celui que `R-COV-1` consomme — un seul format pour l'oracle et le détecteur. JSON est une alternative acceptable (parsing plus stable) ; YAML est retenu pour cohérence Arsenal et lisibilité de revue.

### Stratégie d'immuabilité
Trois couches cumulatives, par robustesse croissante :
1. **Bannière d'en-tête** déclarant l'artefact immuable et son rôle de contrôle positif (convention, lisible humainement).
2. **Empreinte enregistrée + méta-test** (T6) : la CI échoue si le contenu dérive. C'est la garde **machine** — la seule réellement opposable.
3. **Absence de tout script de régénération câblé à la CI** : la fixture est gelée à la main, jamais reconstruite depuis le runtime (un regen post-CH-2 « réparerait » à tort le spécimen).

**Auto-test du détecteur.** La fixture est aussi l'auto-test de `R-COV-1` : si un jour `R-COV-1(fixture)` vire au vert, ce n'est pas le chauffage qui a guéri, c'est le vérificateur qui a régressé.

---

## 3. R-COV-1

- **Entrée.** Un modèle de cascade normalisé (sortie T1) : liste ordonnée de `(garde, raison)` sur le vocabulaire canonique. Cible interchangeable (fixture **ou** runtime), l'engine étant agnostique à la cible.
- **Méthode.** Modélisation de la chaîne `elif` avec **court-circuit** (priorité) : pour la branche d'indice *i*, tester la satisfiabilité de « garde_*i* vraie ∧ toutes les gardes_*j<i* fausses » sur le domaine **borné** des prédicats (booléens / énumérés). Atteignable ⇔ satisfiable.
- **Sortie.** Verdict par branche présente (atteignable / inatteignable) ; **rouge** global si au moins une branche présente est inatteignable, avec son nom ; vert sinon.
- **Critères de succès.** Sur la fixture : **rouge**, désignant `blocage_aeration_en_cours` (le test enveloppant passe sur ce rouge attendu). Déterminisme et nommage explicite de la branche fautive.
- **Cas d'échec attendus (rouge légitime).** Une branche présente **dominée** par la disjonction de ses gardes antérieures (garde_*i* ⟹ ⋁ gardes_*j<i*) → inatteignable. C'est exactement D2 : le cas blocage post-aération satisfait la garde Niveau 1 `chauffage_non_autorise`, donc n'atteint jamais 2b.

### Vérifications explicitement requises

**(a) Une catégorie doctrinale peut exister sans branche runtime.**
`R-COV-1` **n'énumère que les branches physiquement présentes** dans la cascade. Il ne possède **aucune règle du type « toute catégorie doctrinale doit avoir une branche »**. Une catégorie sans branche est **invisible** au détecteur — elle n'est pas « une branche manquante », elle n'est simplement pas une branche. Aucune notion de complétude catégorielle n'est introduite.

**(b) Seules les branches runtime présentes sont concernées.**
Le périmètre d'atteignabilité = l'ensemble des branches issues de la **structure de la cascade**, jamais la liste des catégories doctrinales. C'est une propriété d'**atteignabilité de l'existant**, pas de couverture du doctrinal.

**(c) L'option (a) du Niveau 1 ne provoque aucun faux positif.**
Conséquence directe de (a) + (b) : lorsque (en CH-2, hors périmètre ici) la branche Niveau 1 `chauffage_non_autorise` sera **supprimée**, elle deviendra **absente** — pas « présente et inatteignable ». Une branche absente n'entre pas dans l'énumération de `R-COV-1`. Le Niveau 1 reste une catégorie doctrinale réservée sans branche : invisible au détecteur, donc **zéro faux positif**. CH-1 doit seulement garantir que `R-COV-1` est conçu sur ce principe (énumération de l'existant, jamais exigence de complétude) ; la vérification du vert runtime relève de CH-2.

**Soundness sans faux positif.** `R-COV-1` ne rougit que sur une **domination prouvable** sur le domaine modélisé. Garde hors domaine modélisé (p. ex. seuil numérique) → traitée conservativement : pas de revendication d'inatteignabilité sans preuve (sound, possiblement incomplet). Le cas D2 étant purement booléen/catégoriel (états aération / blocage / autorisation), il tombe dans le domaine décidable, et la fixture garantit qu'il est attrapé.

---

## 4. R-MIRROR-1 — stratégie de comparaison

Objectif : détecter une **divergence logique** entre le cerveau (`decision_centrale`, l.245-254) et le miroir (`diagnostic/raison`, l.80-91), sur **ordre + gardes + raisons** — sans figer la rédaction.

| # | Stratégie | Robustesse | Simplicité | Verdict |
|---|-----------|-----------|-----------|---------|
| A | Égalité textuelle naïve | Très faible (casse sur espaces/commentaires/reformatage) | Élevée | **Rejetée** (proscrite par le plan) |
| B | Égalité d'ensemble des raisons | Faible (ignore ordre **et** gardes) | Élevée | **Rejetée** (le plan exige ordre + conditions) |
| C | **Comparaison structurelle normalisée** : canonicaliser chaque cascade en liste ordonnée `(garde_normalisée, raison)` (alias résolus, opérandes triés, format neutralisé), puis comparer les séquences | Bonne (capte ordre + logique des gardes ; tolère la rédaction) | Bonne (réutilise le normaliseur T1) | **Recommandée** |
| D | Équivalence comportementale : énumérer le domaine d'entrées, évaluer les deux cascades, comparer les tables de sortie | Très bonne (tolère aussi la restructuration) | Moyenne (exige évaluateur + domaine ; localise mal la divergence) | Complément optionnel, **hors périmètre CH-1** |

**Recommandation : C (comparaison structurelle normalisée).** Trois raisons :
1. Elle satisfait **littéralement** l'exigence « ordre + conditions » du plan, là où D compare les conditions seulement *à travers* les sorties (et déclarerait égales deux cascades de structures différentes mais de sorties identiques — ce qui contredit l'intention « miroir »).
2. Elle **réutilise le normaliseur T1**, donc une seule couche de parsing partagée avec `R-COV-1` → moins de surface de dérive.
3. Elle **localise** précisément la divergence (quelle branche, quelle garde), ce que D ne donne pas.

Le miroir est *par conception* structurellement parallèle (c'est le sens de la dette D5) ; C protège exactement cette parallélisme : un refactor d'une cascade sans propagation à l'autre rougit. D est mentionnée comme renfort possible **uniquement** lorsque le domaine d'entrées de la table de vérité existera (CH-2) ; elle n'est **pas** construite en CH-1 (pas de dette spéculative).

**Statut attendu en CH-1 :** `R-MIRROR-1` **vert** sur le runtime courant. Vert ne signifie pas « correct » mais « synchrone » : les deux cascades partagent aujourd'hui le **même** défaut D2. `R-MIRROR-1` garde la synchronisation ; la correction relève de `R-COV-1`. Ce vert est attendu et ne doit pas être lu comme un quitus de justesse.

---

## 5. Pipeline CI

**Où raccorder.** Un nouveau job **« étage 2 »** dans le workflow GitHub Actions de `antoinevalentinHA/arsenal`, réutilisant le runner de l'étage 1. L'étage 1 reste prérequis (le job étage 2 s'exécute sur un étage 1 vert).

**Ordre d'exécution recommandé (au sein du job étage 2) :**
1. **Immuabilité fixture** (T6) — en premier : si la fixture a dérivé, tout l'aval est suspect.
2. **`R-COV-1` sur la fixture** (contrôle positif) — attendu rouge ⇒ test **vert**.
3. **`R-MIRROR-1` sur le runtime** — attendu vert.

L'étage 1 (`R-CI-1`, double fixture, `META-2`) s'exécute en amont (ou en parallèle avec gate), conservé strictement inchangé.

**`R-COV-1` runtime :** **non câblé en gate en CH-1.** Le runtime est encore pathologique (D2 non corrigé), donc `R-COV-1(runtime)` serait rouge ; le câbler en gate rendrait `main` rouge. Le gate runtime (contrôle négatif) est activé en CH-2, une fois le runtime corrigé. CH-1 ne pose que le **contrôle positif** (fixture). L'engine reste agnostique à la cible et **peut** être lancé sur le runtime à titre informatif (il sera rouge, cohérent avec l'état non corrigé) sans gater.

**Statut attendu avant ouverture de CH-2 :** pipeline **entièrement vert**, au sens :
- étage 1 vert (non-régression) ;
- immuabilité fixture verte ;
- `R-COV-1` rougit correctement la fixture (contrôle positif → test vert) ;
- `R-MIRROR-1` vert ;
- gate runtime `R-COV-1` **absent** (réservé à CH-2) ;
- diff confiné à `tests` / CI / fixtures / doc — **zéro fichier runtime**.

---

## 6. Risques d'implémentation

Risques techniques réels du chantier uniquement.

1. **Fidélité du normaliseur à la chaîne `elif`.** Si la priorité (court-circuit) n'est pas modélisée, `R-COV-1` rate la mort de 2b (faux négatif). *Garde-fou :* la fixture est l'oracle — si `R-COV-1` ne la rougit pas, le parseur est faux. La fixture *est* l'auto-test du détecteur.
2. **Couverture Jinja partielle.** Une garde non gérée → mauvaise classification silencieuse. *Garde-fou :* **fail-closed** (garde non parsable ⇒ erreur explicite) ; restriction au vocabulaire de prédicats borné ; assertion que toutes les gardes parsent.
3. **Dérive / aliasing du vocabulaire entre les deux cascades.** Cerveau et miroir peuvent nommer une même condition différemment → `R-MIRROR-1` faux positif sur rédaction bénigne, ou faux négatif si la table d'alias est fausse. *Garde-fou :* table d'alias canonique unique, partagée par les deux invariants ; assertion de clôture du vocabulaire.
4. **Recouplage accidentel fixture↔runtime.** Une régénération depuis le runtime « réparerait » la fixture (surtout post-CH-2). *Garde-fou :* gel manuel + empreinte (T6) + bannière + aucun script de regen en CI.
5. **Décidabilité de l'atteignabilité.** Gardes plus riches que le domaine borné (numérique) → atteignabilité exacte indécidable. *Garde-fou :* `R-COV-1` ne rougit que sur domination **prouvable** (sound, possiblement incomplet) ⇒ pas de faux positif ; le cas D2 est dans le domaine décidable et garanti par la fixture.
6. **Rougissement prématuré du pipeline entre CH-1 et CH-2.** Câbler le contrôle négatif runtime en CH-1 rendrait `main` rouge. *Garde-fou :* discipline de séquencement — seul le contrôle positif (fixture) gate en CH-1.
7. **Mauvaise lecture du vert de `R-MIRROR-1`.** Vert = synchrone, pas correct (défaut partagé). *Garde-fou :* documenter ce sens dans le module et l'en-tête, pour ne pas confondre synchronisation et justesse.
8. **Effet de bord sur l'étage 1.** Le runner / normaliseur partagé pourrait perturber l'étage 1. *Garde-fou :* l'étage 2 est purement additif ; non-régression étage 1 exécutée (T7).

---

## 7. Go / No-Go

**GO — conditions cumulatives pour déclarer CH-1 terminé et ouvrir CH-2 :**
- Fixture committée, autonome (zéro pointeur runtime), empreinte enregistrée, bannière présente, dans l'arbre fixtures étage 2 ; immuabilité (T6) verte.
- `R-COV-1` implémenté, agnostique à la cible, et tel que câblé en CI il **rougit la fixture en nommant `blocage_aeration_en_cours`** (contrôle positif → test vert). Vérifié par conception : (a) énumère seulement les branches présentes ; (b) aucune règle de complétude catégorielle ; (c) une branche absente n'est pas comptée ⇒ pas de faux positif sur l'option (a) ; rougissement uniquement sur domination prouvable.
- `R-MIRROR-1` implémenté (comparaison structurelle normalisée, ordre + gardes + raisons), **vert** sur le runtime courant.
- Job étage 2 intégré au workflow ; **pipeline entièrement vert** au sens du §5 ; gate runtime `R-COV-1` non câblé (réservé CH-2).
- Normaliseur **déterministe** (snapshot-stable) et **fail-closed** sur garde non parsable.
- **Aucun fichier runtime modifié** : diff confiné à `tests` / CI / fixtures / doc.

**NO-GO — déclencheurs :**
- `R-COV-1` ne rougit pas la fixture, ou la rougit sans nommer la branche.
- `R-COV-1` rougit pour un motif autre que la mort connue de 2b d'une manière suggérant un bug de parseur (faux positif).
- `R-MIRROR-1` **rouge** sur le runtime courant (les cascades seraient déjà désynchronisées — à investiguer avant tout passage à CH-2).
- Un fichier runtime touché, ou fixture non stable à l'empreinte.

**Précision de séquencement.** `R-COV-1(runtime)` rouge en CH-1 **n'est pas** un No-Go : c'est l'état attendu d'un runtime non encore corrigé. Seuls le contrôle positif (fixture rouge / test vert), `R-MIRROR-1` vert, l'étage 1 vert et l'intégrité du périmètre runtime gouvernent le Go de CH-1.

---

**Discipline transverse rappelée.** Commit atomique et réversible ; fixture canonique conservée, jamais réécrite (même rang que les changelogs historiques) ; aucune modification d'ordre, de seuil ou de garde hors périmètre ; aucun fichier runtime touché en CH-1.
