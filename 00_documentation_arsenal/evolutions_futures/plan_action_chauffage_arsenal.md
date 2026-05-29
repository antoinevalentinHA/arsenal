# Plan d'action Chauffage — Arsenal

**Type :** plan d'action priorisé (gouvernance de dette)
**Source de vérité :** `audit_chauffage_arsenal_rapport_final.md` (29/05/2026) — constats non rediscutés
**Périmètre :** dettes actives D2 → D9 (D1 soldé, hors périmètre)
**Principe d'arbitrage :** un chantier qui répare la **cohérence causale**, la **doctrine** ou la **maintenabilité** prime sur un chantier cosmétique. Une dette dont le coût excède le bénéfice reste ouverte ou est acceptée explicitement.
**Date :** 29/05/2026

---

## 1. Décisions par dette

| # | Dette (rappel court) | Verdict | Valeur métier | Risque (du correctif) | Coût | Urgence | Tier |
|---|----------------------|---------|---------------|------------------------|------|---------|------|
| D2 | Branche `blocage_aeration_en_cours` morte + `chauffage_non_autorise` mensonger | **Corrigée** | Haute (cohérence causale, intégrité de l'observabilité) | Moyen (touche cœur décision + double cascade + composition `autorise_systeme`) | Moyen | Élevée* | **P0** |
| D3 | Contrat `30_decision_centrale.md` porte encore `absence_protection_thermique` | **Corrigée** (alignement contrat) | Moyenne (vérité contrat↔runtime) | Quasi nul | Quasi nul (1 fichier) | Faible | **P0** (absorbée par D2) |
| D5 | Double cascade miroir non gardée par CI | **Corrigée** (`R-MIRROR-1`) | Haute (meilleur rapport valeur/effort) | Faible (test seul) | Faible | Moyenne (rehaussée : protège D2) | **P0** |
| D6 | Étage 2 CI absent (atteignabilité, iso-comportement, miroir) | **Corrigée partiellement** ; reste de bas rendement différé | Haute pour le sous-ensemble pivot (`R-COV-1`, iso-comportement, non-remontée) | Faible (infra test) | Moyen | Moyenne (rehaussée : verrou de D2) | **P0** (`R-COV-1`) + **P1** (reste pivot) + **P3** (suite résiduelle) |
| D7 | Retry = 2ᵉ appelant de `appliquer_consigne` non contractualisé | **Documentée** (exception bornée) | Moyenne (souveraineté / clarté doctrine) | Faible (contrat + annotation) | Faible | Faible | **P1** |
| D4 | Registres UI aplatis (S2) + `confort_suffisant` sans catégorie (S3) | **Corrigée** | Moyenne (lisibilité utilisateur) | Faible–Moyen (mapping causes→registres) | Moyen | Faible–Moyenne | **P2** |
| D8 | Pas de document transversal des dépendances inter-domaines | **Documentée** | Moyenne (gouvernance / sécurité des refactors) | Faible | Faible–Moyen | Faible | **P2** |
| D9 | Nomenclature `offsets/protection_absence/` | **Acceptée** | Faible | — | — | — | **P3** |

\* *Urgence élevée au sens « à traiter en premier parmi les dettes ouvertes », **pas** au sens hotfix : D2 n'a aucun impact thermique (`reduced` des deux côtés). Le défaut est diagnostique, donc planifiable sans précipitation.*

**Lecture architecte.** La seule dette runtime active (D2) est une **causalité menteuse recréée** — la pathologie même que D1 avait corrigée. Sa valeur de réparation est doctrinale, pas thermique. Son correctif touche un point sensible (cascade décision + miroir + composition d'autorisation) : il faut donc l'entourer de garde-fous **avant** de l'appliquer, d'où l'inversion d'ordre assumée ci-dessous (CI d'abord, correctif ensuite).

---

## 2. Plan d'action priorisé

### P0 — À traiter immédiatement

#### Chantier 1 — Verrouillage CI étage 2 (amorce) : `R-COV-1` + `R-MIRROR-1`
*Couvre D5 intégralement et amorce D6.*

- **Objectif.** Construire le socle minimal de l'étage 2 comportemental, puis poser deux invariants : `R-COV-1` (atteignabilité de toutes les branches de raison) et `R-MIRROR-1` (synchronisation des deux cascades). `R-COV-1` doit virer **rouge sur D2** (preuve que la branche 2b est morte) ; il deviendra vert au Chantier 2.
- **Fichiers impactés.** Harnais de test selon l'arborescence de l'étage 1 existant (taxonomie `registres_entites.yaml` réutilisée) ; nouveaux modules d'invariants `R-COV-1`, `R-MIRROR-1` ; workflow GitHub Actions (`antoinevalentinHA/arsenal`) étendu d'un job étage 2. **Aucun fichier runtime touché.**
- **Risques.** Faux négatifs si le parseur d'atteignabilité ne modélise pas correctement la chaîne `elif` (le court-circuit Niveau 1 doit être visible). `R-MIRROR-1` doit comparer **ordre + conditions**, pas seulement l'ensemble des raisons.
- **Tests à exécuter.** `R-COV-1` (attendu : **rouge**, signale 2b inatteignable) ; `R-MIRROR-1` (attendu : **vert** sur l'état courant, les cascades étant aujourd'hui synchrones dans leur défaut) ; non-régression étage 1 (`R-CI-1`, double fixture, `META-2`).
- **Critères d'acceptation.** `R-COV-1` rouge et pointant nommément `blocage_aeration_en_cours` ; `R-MIRROR-1` opérationnel ; étage 1 toujours vert ; job étage 2 intégré au pipeline.
- **Estimation d'effort.** Moyen (`R-MIRROR-1` faible ; scaffold + `R-COV-1` moyen).
- **Dépendances.** Aucune en amont. Prérequis du Chantier 2 (garde-fous posés avant le correctif).

#### Chantier 2 — Correctif D2 + alignement contrat (absorbe D3)
*Couvre D2 et D3.*

- **Prérequis doctrinal (gate, sans code).** Trancher la nature de `blocage_aeration` : **Niveau 2 (limite)**, par cohérence avec le traitement de `standby_force`. Décision induite sur la couche Niveau 1 : faute de cause d'interdiction système réelle subsistante, **retirer** `chauffage_non_autorise` de la cascade et documenter Niveau 1 comme **point d'extension réservé** (à réintroduire uniquement avec sa première vraie cause). *Variante :* si une cause système légitime existe et doit être affichée (p. ex. pont durablement hors-ligne au-delà du transitoire G2), la câbler dans `autorise_systeme` plutôt que retirer la couche — à arbitrer, mais ne pas conserver une catégorie vide (lie-in-waiting).
- **Objectif.** Sortir `blocage_aeration` de la composition d'état de `autorise_systeme`, ranimer la branche 2b (`blocage_aeration_en_cours`), aligner le miroir, et traiter la couche Niveau 1 selon la décision ci-dessus. **Iso-comportement thermique garanti** : seul le nom de la raison change pour le cas blocage post-aération.
- **Fichiers impactés.**
  - `12_template_sensors/chauffage/autorisation.yaml` (state l.56-57 ; attributs l.76-77 inchangés)
  - `10_scripts/chauffage/decision_centrale.yaml` (cascade `reason` l.245-254 ; `desired_mode` l.201-209 **inchangés**)
  - `12_template_sensors/chauffage/diagnostic/raison.yaml` (miroir l.80-91)
  - `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` (table des raisons + statut Niveau 1 ; **et** remplacement `absence_protection_thermique` → `stabilisation_absence` ⇒ **D3 soldée dans le même commit**, le fichier n'étant touché qu'une fois)
- **Risques.** Désync transitoire au reload (R-DIV-1, qualifié « correction, pas régression ») ; oubli de propagation au miroir (couvert par `R-MIRROR-1` posé au Chantier 1) ; régression d'ordre dans la chaîne `elif`. Cross-domaine **déjà dégagé** (R-DIV-3/4 : la clim ne lit pas `autorise_systeme=off` comme proxy).
- **Tests à exécuter.** **Table de vérité avant/après** (artefact de preuve hors-ligne, obligatoire avant application) ; `R-COV-1` (attendu : **passe au vert**) ; `R-MIRROR-1` (reste vert) ; étage 1 (reste vert) ; revue des 4 briques pivots.
- **Critères d'acceptation.**
  - `desired_mode` **identique avant/après** sur toutes les lignes de la table (preuve iso-comportement thermique).
  - Cas blocage post-aération : raison passe de `chauffage_non_autorise` → `blocage_aeration_en_cours` ; `desired_mode == reduced` inchangé.
  - Cas aération en cours (2a) : inchangé (`aeration_en_cours`, `reduced`).
  - `R-COV-1` vert (zéro branche morte) ; `R-MIRROR-1` vert ; étage 1 vert.
  - Contrat `30` aligné sur le runtime (raison Niveau 2 vivante, Niveau 1 documenté selon décision, plus aucune occurrence de `absence_protection_thermique`).
  - Changelogs `v11_1_3.md` / `v12_1.md` **non modifiés** (historique figé).
- **Estimation d'effort.** Moyen (le diff runtime est petit ; le coût est dans l'arbitrage doctrinal, la table de vérité et la synchro du miroir).
- **Dépendances.** Gate doctrinal + Chantier 1 (garde-fous). **Prérequis du Chantier 6 (D4).**

---

### P1 — Important

#### Chantier 3 — Étage 2 : invariants comportementaux pivots
*Couvre le reste à valeur de D6.*

- **Objectif.** Compléter l'étage 2 avec les invariants à fort rendement : `INV-30-5` (iso-comportement), `INV-D1/D3` (non-remontée conséquence→cause — généralise la pathologie D1/D2 en garde permanent), et les `INV-30-x` structurants de la décision centrale.
- **Fichiers impactés.** Modules d'invariants de l'étage 2 (suite du Chantier 1) ; workflow CI. Aucun fichier runtime.
- **Risques.** Sur-spécification d'invariants fragiles aux refactors légitimes ; tenir la frontière « doctrine » et non « implémentation ».
- **Tests à exécuter.** Les nouveaux invariants verts sur `main` post-D2 ; double fixture étage 1 inchangée.
- **Critères d'acceptation.** `INV-30-5` et `INV-D1/D3` opérationnels et verts ; aucune catégorie de raison ne peut afficher une conséquence à la place de sa cause sans faire rougir la CI.
- **Estimation d'effort.** Moyen.
- **Dépendances.** Chantier 1 (scaffold étage 2). Postérieur à D2 pour valider l'iso-comportement sur l'état corrigé.

#### Chantier 4 — Contractualisation du retry transactionnel
*Couvre D7.*

- **Objectif.** Formaliser le retry comme **exception bornée** : second appelant légitime de `appliquer_consigne` au titre de la **ré-application** d'une décision déjà prise (jamais d'une nouvelle décision), sans repasser par le cerveau.
- **Fichiers impactés.** Contrat de souveraineté de la frontière d'exécution (clause d'exception) ; éventuelle annotation d'en-tête dans `11_automations/chauffage/retry_transactionnel/`. Aucune logique modifiée.
- **Risques.** Très faibles (documentaire). Veiller à ce que la clause interdise explicitement toute décision nouvelle par cette voie.
- **Tests à exécuter.** Relecture de cohérence ; le cas échéant, invariant CI « seuls `decision_centrale` et le retry appellent `appliquer_consigne` » (interdit tout 3ᵉ appelant futur).
- **Critères d'acceptation.** Le contrat nomme le retry comme exception bornée et en délimite le mandat (ré-application uniquement) ; aucun écart runtime introduit.
- **Estimation d'effort.** Faible.
- **Dépendances.** Aucune. Parallélisable.

---

### P2 — Amélioration

#### Chantier 5 — Document transversal des dépendances inter-domaines
*Couvre D8.*

- **Objectif.** Créer `dependances_inter_domaines.md` recensant les couplages : la clim lit `input_boolean.chauffage_blocage_aeration` et la consigne appliquée locale ; `binary_sensor.boiler_bridge_online` (domaine boiler, gardé G2). Supprime l'angle mort des refactors chauffage.
- **Fichiers impactés.** Nouveau `00_documentation_arsenal/contrats/.../dependances_inter_domaines.md` (emplacement selon convention de gouvernance).
- **Risques.** Document qui dérive du runtime s'il n'est pas relié à la CI — prévoir, à terme, un invariant de cohérence (optionnel, hors périmètre immédiat).
- **Tests à exécuter.** Vérification manuelle du recensement face au runtime (lectures cross-domaine réelles).
- **Critères d'acceptation.** Tout lecteur cross-domaine du domaine chauffage est listé avec l'entité lue et le sens du couplage.
- **Estimation d'effort.** Faible–Moyen.
- **Dépendances.** Aucune (le check ad hoc R-DIV-3 a déjà couvert le besoin spécifique de D2 ; ce chantier le **généralise**, il ne bloque pas D2).

#### Chantier 6 — Éclatement des registres UI + promotion `confort_suffisant`
*Couvre D4 (S2 + S3).*

- **Objectif.** Éclater le bloc « Bloqué » en causes distinctes (sécurité système / stabilisation / contexte majeur) ; promouvoir `confort_suffisant` de libellé à **catégorie**.
- **Fichiers impactés.** Les 4 briques pivots consommatrices de `sensor.chauffage_raison_calculee` : `carte_chauffage_synthese`, `carte_chauffage_decision`, `carte_chauffage_intention`, `chauffage_diagnostic_global_compact`. **Lecture seule** — aucun calcul métier ajouté côté UI.
- **Risques.** Faible–Moyen : mapping raison→registre incomplet ; tenir l'invariant « l'UI ne calcule pas, elle affiche ».
- **Tests à exécuter.** Revue visuelle des 4 briques sur chaque raison ; vérifier que le cas post-aération s'affiche désormais distinctement (rendu possible par D2).
- **Critères d'acceptation.** Causes hétérogènes affichées séparément ; `confort_suffisant` présenté comme catégorie ; le cas post-aération apparaît comme « post-aération » et non « Interdit — sécurité système » ; zéro logique métier côté UI.
- **Estimation d'effort.** Moyen.
- **Dépendances.** **Chantier 2 (D2) obligatoire** : tant que la branche 2b est morte, le registre « post-aération » resterait vide ; éclater l'UI avant D2 serait prématuré.

---

### P3 — Dette acceptée / différée

#### Chantier 7 — Clôture des dettes acceptées et différées
- **D9 — Nomenclature `offsets/protection_absence/` : acceptée, figée.** Aucune action. Renommer propagerait un changement cosmétique dans une arborescence stable sans gain doctrinal ni de maintenabilité → **coût > bénéfice**, reste en l'état.
- **Suite résiduelle d'invariants étage 2 : différée.** `R-VOC-1/2`, `R-REG-MIX-1`, `INV-STANDBY-1/2/4` sont de **rendement marginal décroissant** une fois les invariants pivots posés (Chantiers 1 & 3). **Décision : ne pas les construire spéculativement.** Les réactiver seulement si une régression concrète les justifie. Le coût de construction et de maintenance dépasse aujourd'hui le bénéfice.
- **Estimation d'effort.** Nulle (statu quo documenté).

---

## 3. Feuille de route recommandée

Séquence exacte. L'ordre privilégie la cohérence causale et la maintenabilité : on **pose les garde-fous avant de toucher le cœur de décision**, ce qui rend le correctif D2 vérifiable par la CI (rouge → vert) au lieu de reposer sur une seule table de vérité manuelle.

```
GATE        Décision doctrinale D2  (Niveau 2 ; sort de la couche Niveau 1)
              │
P0 ─ CH-1   Étage 2 : R-COV-1 (→ ROUGE sur D2) + R-MIRROR-1 (vert)      [D5 + amorce D6]
              │   (garde-fous en place : le miroir et l'atteignabilité protègent le refactor)
P0 ─ CH-2   Correctif D2 + alignement contrat 30  → R-COV-1 VERT        [D2 + D3]
              │   (table de vérité iso-comportement prouvée hors-ligne avant commit)
              ├───────────────┐
P1 ─ CH-3   Étage 2 pivot     │  P1 ─ CH-4  Contractualisation retry     [reste D6] [D7]
            (INV-30-5,        │             (parallélisable, indépendant)
             INV-D1/D3)       │
              │               │
P2 ─ CH-6   Éclatement UI + confort_suffisant   ← dépend de CH-2        [D4]
P2 ─ CH-5   Doc dépendances inter-domaines      (parallélisable)        [D8]
              │
P3 ─ CH-7   D9 acceptée figée + suite d'invariants résiduels différée   [D9 + reste D6]
```

**Chemin critique :** GATE → CH-1 → CH-2 → CH-6. Tout le reste (CH-3, CH-4, CH-5) est parallélisable hors de ce chemin.

**Variante pragmatique (si priorité au « défaut éteint au plus vite »).** Permuter CH-1 et CH-2 : corriger D2 d'abord, puis poser `R-COV-1`/`R-MIRROR-1` en verrou rétroactif. Acceptable car D2 n'a aucun impact thermique, **mais** on perd la preuve rouge → vert et le miroir n'est plus gardé pendant l'édition à double cascade. L'ordre recommandé reste garde-fous d'abord.

**Discipline transverse (toutes phases).** Commit atomique et réversible ; iso-comportement prouvé hors-ligne avant application ; aucune modification d'ordre, de seuil ou de garde hors périmètre du chantier ; changelogs historiques jamais réécrits.
