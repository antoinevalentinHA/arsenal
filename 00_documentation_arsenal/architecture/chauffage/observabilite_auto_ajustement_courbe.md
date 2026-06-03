# 🧠 ARSENAL — ARCHITECTURE D'OBSERVABILITÉ
## Chauffage — Auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Document d'architecture (normatif amont) |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Modèle figé — préalable à toute discussion de runtime |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Origine** | Audit clôturé `audits/01_rapports/chauffage/audit_auto_ajustement_courbe.md` |
| **Cadre** | Read-only, additif, **aucun changement de comportement** ; runtime considéré correct |
| **Subordonné à** | `contrats/chauffage/75_auto_ajustement_courbe.md` |

> Ce document **fige le modèle** d'observabilité. Il ne décrit aucune implémentation, aucun YAML, aucun runtime. Il enchaîne : critique du modèle initial → architecture cible → contrat d'observabilité → livrables → chantier.

---

# 1. Critique du modèle d'observabilité initial

Le premier modèle (cascade *Suggestion → Décision → Application → Acquittement → Effet* ; événements métier ; raisons de refus ; couches Runtime/Diagnostic/Historique/Supervision) est globalement valable mais comporte des défauts à corriger **avant** de figer.

## 1.1 Incohérences

- **C1 — La « cascade » mélange trois bases de temps.** La suggestion est continue/réactive ; la décision est quotidienne ; l'effet s'étale sur plusieurs jours. Les présenter comme une chaîne linéaire laisse croire à une correspondance 1:1 entre étages, qui n'existe pas (une suggestion bouge plusieurs fois entre deux décisions ; un effet couvre plusieurs cycles).
- **C2 — « Effet » n'est pas un étage de même nature.** Suggestion / Décision / Application / Acquittement sont des **faits produits** par le système. L'effet est une **inférence faite a posteriori** par un humain, avec incertitude d'attribution. Le placer en 5ᵉ maillon de la même chaîne laisse croire que le système « connaît » son effet — il ne le connaît pas.
- **C3 — « Refus » et « abstention » sont confondus.** Le modèle classait `gel_apprentissage` parmi les *raisons de refus*. Or refuser (une suggestion existait, la décision a décliné) et s'abstenir (aucun signal frais à évaluer) sont deux catégories distinctes. Les fondre brouille la lecture du « pourquoi rien ne s'est passé ».

## 1.2 Angles morts

- **A1 — Le jour nominal silencieux.** Le cas le plus fréquent est « rien ne s'est passé ». Le modèle traite les refus mais n'érige pas en observable de premier rang le **jour où le système a évalué et n'a légitimement rien fait**. Sans cela, le silence reste ambigu entre *immobilité saine* et *cécité / gel*.
- **A2 — Valeur intentionnelle vs valeur effective.** Le helper de consigne et la consigne réellement portée par la chaudière peuvent **diverger** (acquittement `rejected`/`timeout` : le domaine « croit » avoir appliqué X, la chaudière garde Y). Toute analyse de dérive doit porter sur la **courbe effective**, pas intentionnelle. Le modèle ne distingue pas les deux.
- **A3 — Corrélation des événements.** Le cycle de vie traverse plusieurs événements (décision → application → acquittement → fenêtre d'effet) qui doivent être **reliés par un identifiant**. La couche exécution possède déjà un identifiant de requête ; le modèle ne définit pas d'**identifiant de corrélation de décision** pour recoudre la chaîne.
- **A4 — Intégrité de la trace.** Si un événement manque (redémarrage en cours de décision, trou d'historisation), la reconstitution comporte des trous. Le modèle ne prévoit aucun **signalement de complétude** : un trou serait lu comme « aucun ajustement ».

## 1.3 Redondances

- **R1 — La représentativité joue trois rôles** (annotation de contexte, indicateur « taux de jours apprenants », événement de transition) → risque de double comptage et de confusion sur son statut.
- **R2 — Frontière Diagnostic ↔ Historique floue.** Certains indicateurs ont besoin de l'historique pour être calculés ; le modèle laissait le Diagnostic potentiellement lire le runtime en direct. Le sens de circulation n'est pas normé.

## 1.4 Concepts manquants

- **M1 — Identifiant de corrélation de décision** (cf. A3).
- **M2 — Distinction intentionnel / effectif** (cf. A2).
- **M3 — Typage nominal / anomal** des issues. Le modèle livrait une liste plate de raisons. Or `baisse_bloquee_poele`, `bande_morte`, `suggestion_identique`, `gel` sont **nominaux** (système conforme) ; `bridge_offline`, `rejected`, `timeout`, `hors_domaine` sont **anomaux**. Sans ce typage, un superviseur risque d'alarmer sur du silence sain.
- **M4 — Signalement de complétude** de la trace (cf. A4).

## 1.5 Risques d'interprétation

- **I1 — Effet lu comme causal.** Même annoté « corrélation », un panneau d'effet par ajustement invite à un verdict causal. L'effet doit être cadré comme **tendance au niveau régime**, jamais comme score d'un ajustement isolé.
- **I2 — Silence nominal lu comme anomalie** (corollaire de A1/M3).
- **I3 — Représentativité relue comme verrou.** L'affichage de l'état représentatif ne doit jamais être interprété comme une condition décisionnelle (décision déjà actée : proxy médiocre, non promu en verrou).

---

# 2. Architecture cible

## 2.1 Objectifs

Permettre à un humain de répondre **a posteriori, sur données**, à cinq questions :

1. **Qu'a proposé le système ?** (suggestion, son erreur source, son écrêtage)
2. **Qu'a décidé le système ?** (appliqué / refusé / abstenu, par paramètre et par sens)
3. **Pourquoi ?** (raison normalisée, contexte d'entrée complet)
4. **Qu'a réellement appliqué la chaudière ?** (valeur effective + acquittement)
5. **Quel a été l'effet observé ?** (tendance de régulation, au niveau régime, après stabilisation)

## 2.2 Principes

- **P1 — Read-only & additif.** L'observabilité enregistre, conserve, dérive, présente. Elle ne gèle, n'autorise, ne décide jamais. Aucun comportement existant n'est modifié.
- **P2 — Pipeline à sens unique : capture → persistance → dérivation → présentation.** Le Diagnostic lit l'Historique, **jamais** le runtime en direct.
- **P3 — Le runtime n'émet que des faits.** Chaque fait porte son **contexte d'entrée complet**, son **identifiant de corrélation** et son **typage nominal/anomal**. Le runtime ne calcule jamais d'effet, ne juge jamais.
- **P4 — L'effet est inférentiel, au niveau régime, post-stabilisation.** Jamais un événement runtime, jamais un score causal d'ajustement isolé.
- **P5 — Distinguer intentionnel et effectif.** La courbe analysée pour la dérive est la **courbe effective** (confirmée par acquittement).
- **P6 — Représentativité = contexte unique.** Annotation informative ; jamais verrou, jamais filtre silencieux.
- **P7 — Le silence est un observable.** Un jour évalué sans action produit une trace explicite (abstention nominale), distincte d'un trou de trace.
- **P8 — Complétude signalée.** L'absence d'événement « non survenu » et l'absence d'événement « non enregistré » doivent être distinguables.
- **P9 — Simulation séparable.** Les traces de simulation forment un flux distinct, jamais mêlé aux indicateurs d'effet.

## 2.3 Responsabilités par couche

| Couche | Responsabilité | Interdits |
|---|---|---|
| **Runtime (capture)** | Émettre les faits métier au moment où ils surviennent, avec contexte complet, corrélation et typage | Calculer un effet ; juger ; influencer une décision |
| **Historique (persistance)** | Conserver les faits et les grandeurs nécessaires à la reconstitution, sur ≥ un cycle saisonnier ; tracer intentionnel **et** effectif ; signaler les trous | Transformer / interpréter |
| **Diagnostic (dérivation)** | Calculer les indicateurs (convergence, trajectoire, réversions, fenêtres d'effet, jours apprenants) à partir de l'Historique | Lire le runtime en direct ; rétroagir sur la décision |
| **Supervision (présentation)** | Donner à lire les 5 réponses ; distinguer nominal/anomal ; afficher l'effet en tendance régime | Affirmer une causalité par ajustement ; déclencher une action |

## 2.4 Frontière runtime ↔ diagnostic (normative)

C'est la frontière critique. Elle est **unidirectionnelle et étanche** :

- Le runtime **produit** des faits horodatés et corrélés ; il ne lit pas le diagnostic.
- Le diagnostic **consomme** l'historique de ces faits ; il ne lit pas l'état runtime vivant ni n'écrit dans le domaine.
- Aucune grandeur de diagnostic ne peut redevenir une entrée de décision (sinon l'observabilité créerait une boucle — violation de P1).

## 2.5 Vocabulaire métier canonique

| Terme | Définition |
|---|---|
| **Suggestion** | Valeur proposée (pente/parallèle), produite en continu à partir de l'erreur lissée, bornée au domaine d'auto-ajustement |
| **Écrêtage** | Réduction d'une suggestion à la borne du domaine d'auto-ajustement ; l'écart écrêté est un fait à tracer |
| **Décision** | Verdict quotidien par paramètre : *appliquer*, *refuser* ou *s'abstenir* |
| **Application** | Inscription de la valeur décidée comme **valeur intentionnelle** |
| **Valeur intentionnelle** | Ce que le domaine a voulu appliquer |
| **Valeur effective** | Ce que la chaudière porte réellement, **confirmé par acquittement** |
| **Acquittement** | Issue d'exécution : `applied` / `rejected` / `timeout` |
| **Refus** | Une suggestion exploitable existait ; la décision a décliné (avec raison) |
| **Abstention / gel** | Aucun signal frais à évaluer (consigne ≠ confort, suggestion indisponible) ; il n'y avait rien à décider |
| **Effet inféré** | Tendance de l'erreur/régulation observée après stabilisation, au niveau régime — jamais un score causal |
| **Jour apprenant / jour gelé** | Cycle où l'écart a été échantillonné / non échantillonné |
| **Représentativité (contexte)** | Annotation d'éligibilité théorique ; jamais verrou |
| **Identifiant de corrélation** | Clé reliant décision → application → acquittement → fenêtre d'effet |
| **Complétude** | Propriété indiquant si la trace d'une période est intègre ou trouée |

## 2.6 Cycle de vie d'un ajustement

Trois régimes temporels, reliés par l'identifiant de corrélation :

```
RÉGIME CONTINU            RÉGIME QUOTIDIEN (1 cycle)         RÉGIME LENT (post-stabilisation)
─────────────────         ───────────────────────────       ───────────────────────────────
[Suggestion évolue]  →    [Décision]                    →    [Effet inféré]
  erreur source              ├─ appliquer → [Application:        tendance erreur / régulation
  écrêtage ?                 │   valeur intentionnelle]          au niveau régime, jours
                            │      → [Acquittement:               apprenants uniquement
                            │         valeur effective]
                            ├─ refuser  (raison, nominal/anomal)
                            └─ s'abstenir / gel (cause)
```

États canoniques d'un cycle : `suggéré` → (`appliqué` → `acquitté{applied|rejected|timeout}`) | `refusé{raison}` | `abstenu{cause}`. La valeur **effective** ne devient la référence de trajectoire que sur `applied`. L'effet n'est rattaché qu'aux cycles `applied` sur jours apprenants représentatifs, après délai de stabilisation.

---

# 3. Contrat d'observabilité (normatif, indépendant de l'implémentation)

> Destiné à être extrait en `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md`. Opposable à toute future implémentation. Ne décrit aucun mécanisme technique.

## 3.1 Événements obligatoires

Un événement **DOIT** être produit pour chacun des faits suivants :

1. **Cycle évalué** — à chaque cycle quotidien, quel que soit son issue (y compris abstention et silence nominal).
2. **Suggestion modifiée** — à chaque changement d'une valeur suggérée.
3. **Ajustement appliqué** — par paramètre, lors d'une application.
4. **Ajustement refusé** — par paramètre, avec raison (§3.2).
5. **Abstention / gel** — par cycle, avec cause (§3.2).
6. **Issue d'exécution** — résultat d'acquittement et valeur effective résultante.
7. **Transition de représentativité** — changement d'état (contexte).
8. **Épisode de gel d'apprentissage** — début/fin et cause.

## 3.2 Raisons autorisées (vocabulaire fermé, typé)

**Refus (une suggestion existait)**
| Raison | Type |
|---|---|
| `suggestion_identique` | nominal |
| `bande_morte` | nominal |
| `baisse_bloquee_poele` | **nominal** (asymétrie correcte) |
| `hors_domaine` | anomal |

**Abstention / gel (aucun signal à décider)**
| Cause | Type |
|---|---|
| `auto_desactive` | nominal |
| `hors_mode_normal` | nominal |
| `gel_apprentissage` (préciser : fenêtre / aération / poele_actif / absence / vacances) | nominal |
| `suggestion_indisponible` | anomal |

**Exécution**
| Issue | Type |
|---|---|
| `applied` | nominal |
| `rejected` (motif bridge) | anomal |
| `timeout` (corrélé / local) | anomal |
| `bridge_offline` / `hors_bornes_physiques` / `non_conforme_au_pas` | anomal |

**Annotation non bloquante** : `journee_non_representative` — informe, ne refuse jamais.

Toute issue **DOIT** porter son type `nominal | anomal`. Refus et abstention **NE DOIVENT PAS** être confondus.

## 3.3 Contexte minimal obligatoire

Tout événement de **cycle / décision** DOIT porter, autosuffisant :
- pente & parallèle **courants** ;
- valeurs **suggérées** et leur erreur source (froid, global) ;
- état de **représentativité** (contexte) ;
- état **poêle stable**, **mode maison**, **auto actif** ;
- **mode** (simulation / réel) ;
- **identifiant de corrélation**.

## 3.4 Règles de traçabilité

- **T1** — Chaque cycle porte un **identifiant de corrélation** reliant décision → application → acquittement → fenêtre d'effet.
- **T2** — Horodatage en **format exploitable** (chronologique, non d'affichage).
- **T3** — Chaque événement est **autosuffisant** : relisible sans dépendre d'un état runtime ultérieurement écrasé.
- **T4** — La **valeur effective** (post-acquittement) est tracée distinctement de la valeur intentionnelle.
- **T5** — Les traces de **simulation** sont marquées et séparables ; elles ne nourrissent jamais l'effet.

## 3.5 Exigences de reconstitution historique

- **H1** — Sont persistés : pente/parallèle **intentionnels et effectifs**, suggestions, erreurs lissées, état de représentativité, journal des décisions/refus/abstentions, épisodes de gel — joints aux métriques de régulation déjà historisées.
- **H2** — Rétention ≥ **un cycle saisonnier complet** (voir l'affaissement de demi-saison et son rattrapage).
- **H3** — La **complétude** d'une période est signalée : un trou de trace est distinguable d'une absence d'ajustement.

## 3.6 Exigences de supervision humaine

- **S1** — Les **cinq questions** (§2.1) sont répondables sur données.
- **S2** — Nominal et anomal sont **lisibles d'un coup d'œil** ; le silence nominal n'alarme pas.
- **S3** — L'effet est présenté en **tendance régime**, jamais en verdict causal par ajustement.
- **S4** — La **trajectoire effective** de la courbe est visible dans le temps.
- **S5** — Représentativité et gel sont présentés en **contexte**, jamais en justification d'une action automatique.

## 3.7 Invariants & interdictions

- **INV-1** — L'observabilité ne modifie aucun comportement (P1).
- **INV-2** — Aucune grandeur de diagnostic ne redevient entrée de décision (étanchéité P2/2.4).
- **INV-3** — La représentativité n'est jamais promue en verrou décisionnel.
- **INV-4** — Aucun effet n'est affirmé causal pour un ajustement isolé.
- **INV-5** — Refus ≠ abstention ; nominal ≠ anomal — distinctions opposables.

---

# 4. Livrables Arsenal

| Document | Chemin proposé | Rôle | Justification | Dépendances |
|---|---|---|---|---|
| **Architecture** (ce document) | `00_documentation_arsenal/architecture/chauffage/observabilite_auto_ajustement_courbe.md` | Fige le modèle conceptuel | Préalable à toute discussion runtime | Audit clôturé ; contrat `75` |
| **Contrat d'observabilité** | `00_documentation_arsenal/contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` | Norme opposable (extraction du §3) | Donner force normative aux événements, raisons, traçabilité, reconstitution, supervision | Subordonné à `75` ; référence la couche exécution (corrélation / acquittement) `10_souverainete_execution` |
| **Chantier d'implémentation** | `00_documentation_arsenal/audits/04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md` (enrichir l'existant) | Tracker de réalisation | Ancrer le chantier déjà ouvert sur l'architecture + le contrat | Architecture + contrat `76` |

Rien d'autre n'est créé à ce stade (pas de plan d'action tant que le chantier n'est pas ordonnancé ; pas de spécification de dashboard isolée — couverte par §3.6).

---

# 5. Chantier d'implémentation

> Enrichit le chantier déjà ouvert, désormais ancré sur l'architecture et le contrat `76`. Définition seule — aucun code.

- **Périmètre** — Réaliser la capture des événements obligatoires (§3.1) avec contexte minimal (§3.3) et corrélation (§3.4) ; persister le nécessaire à la reconstitution (§3.5) ; dériver les indicateurs (convergence, trajectoire effective, réversions, fenêtres d'effet, jours apprenants) ; présenter les cinq réponses avec typage nominal/anomal (§3.6).
- **Hors périmètre** — Toute modification de la cascade de décision ; câblage de la représentativité ; évolution des garde-fous poêle/fenêtre/aération ; changement des bornes/pas/cadence/bande morte ; couche d'exécution transactionnelle (saine). L'observabilité **observe**, elle ne corrige pas.
- **Valeur métier** — Rendre le système **supervisable** ; rendre la dérive **mesurable** (lever l'indécidable de l'audit) ; rendre la protection empruntée **surveillable** ; fonder toute évolution future de l'apprentissage sur des faits.
- **Risques couverts** — Aveuglement du domaine (Important) ; invisibilité de la protection empruntée (Important différé) ; impossibilité de démontrer l'efficacité ; ambiguïté du silence (sain vs gelé vs trou).
- **Critères de succès** — Sans avoir changé le comportement : (1) reconstituer la trajectoire **effective** de la courbe ; (2) retrouver, par cycle, suggestion / décision / raison typée / acquittement / corrélation ; (3) distinguer jour apprenant, jour gelé et trou de trace ; (4) lire l'effet en tendance régime sur jours représentatifs ; (5) répondre aux cinq questions sans hypothèse.

---

## Statut

**Modèle figé.** Ce document et le contrat `76` qui en dérive constituent le préalable normatif. Toute discussion de runtime intervient **après** ce gel, et doit s'y conformer.

*Architecture d'observabilité — 2026-06-03. Aucun runtime, aucun YAML, aucun patch.*
