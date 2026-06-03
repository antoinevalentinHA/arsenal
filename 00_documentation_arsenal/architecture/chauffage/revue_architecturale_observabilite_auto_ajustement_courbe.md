# 🔍 ARSENAL — REVUE ARCHITECTURALE
## Chantier d'observabilité — Auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Revue architecturale / préparation de conception |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Revue amont — phase Architecture → Conception |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Document revu** | `architecture/chauffage/observabilite_auto_ajustement_courbe.md` (figé) |
| **Chantier de référence** | `audits/04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md` |
| **Cadre** | Aucun YAML, aucun code, aucun contrat rédigé, aucune implémentation, aucun runtime |

> **Question de la revue : sommes-nous prêts à construire ?**
> Réponse anticipée : **non — l'architecture est saine mais incomplète pour être implémentée.** Plusieurs décisions opérationnelles restent ouvertes ; elles doivent être tranchées en phase de conception avant tout développement.

---

# 1. Relecture critique

L'architecture est conceptuellement solide (pipeline étanche, distinctions justes, invariants clairs). Mais une revue sérieuse révèle des **zones différées ou implicites** qui bloqueraient l'implémentation.

## 1.1 Ambiguïtés de frontière

- **CR-1 — Cardinalité de l'identifiant de corrélation.** L'architecture pose un « identifiant de corrélation de décision » reliant décision → application → acquittement, mais un cycle quotidien peut produire **jusqu'à deux applications** (pente *et* parallèle), chacune avec son propre identifiant d'exécution côté boiler. La relation est **un-à-plusieurs** et non résolue : l'identifiant de décision est-il le parent des identifiants d'exécution, ou confondu avec eux ? Frontière à définir.
- **CR-2 — Valeur effective : inférée ou mesurée ?** « Valeur effective = confirmée par acquittement » suppose que l'acquittement `applied` **vaut** lecture de la courbe réelle. Or « confirmé envoyé » n'est pas « relu sur l'appareil ». Si aucun retour de lecture de la courbe n'existe, la trajectoire « effective » est en réalité **intentionnel-confirmé**, pas **mesuré** — et ne détecterait pas une divergence d'origine externe. Hypothèse implicite à expliciter.
- **CR-3 — Couture avec le diagnostic chauffage existant.** « S'appuie sur les métriques de régulation déjà existantes » ne dit pas si elles sont **référencées en place** (création d'une dépendance de cycle de vie) ou **réimportées** (redondance). Frontière non tranchée.

## 1.2 Angles morts

- **CR-4 — L'« effet » est la partie la moins constructible.** À cadence 1 ajustement/jour et délai de stabilisation pluri-journalier, **plusieurs ajustements se chevauchent** dans une même fenêtre d'effet → l'attribution par ajustement est impossible. L'architecture le dit (« jamais causal par ajustement isolé »), mais ne définit pas l'**unité d'attribution** de remplacement (agrégat de fenêtre régime ? cohorte ?). Sans cette décision, la question 5 reste un vœu, pas un livrable.
- **CR-5 — Le coût de l'observabilité n'est pas borné.** « Additif, read-only » est présenté comme sans effet. Mais l'émission d'événements et la persistance ont des **effets réels non décisionnels** : croissance de la base Recorder, charge du bus d'événements, recomputation de capteurs dérivés. L'architecture ne pose aucun **budget de volume**. C'est l'angle mort de la sur-observabilité.
- **CR-6 — Complétude mal bornée.** « La complétude est signalée » n'a de sens que pour les événements à **cadence attendue** (le cycle quotidien : ~1/jour → un jour manquant = trou). Pour les événements **continus** (suggestion modifiée), il n'existe pas de cadence de référence → un « manque » est indétectable. L'exigence de complétude est sur-revendiquée.
- **CR-7 — Typage nominal/anomal statique.** Certaines causes nominales deviennent anomales **par persistance** : un `gel_apprentissage` bref est sain ; un gel de plusieurs semaines (système qui n'apprend jamais) ne l'est plus. L'axe binaire ne capte pas la dimension **durée/fréquence**.

## 1.3 Hypothèses implicites & sequencing

- **CR-8 — Rétention en conflit avec la politique Recorder existante.** « Rétention ≥ un cycle saisonnier » se heurte à la politique Recorder en place (purge ~30 jours). Soit allonger globalement la rétention (impacte tout le système), soit un stockage long terme dédié. L'architecture pose l'exigence sans confronter cette réalité. Décision structurante à prendre **avant** implémentation.
- **CR-9 — Cycle de vie en simulation tronqué.** Une décision simulée produit des événements mais **ni application, ni acquittement, ni effet**. Le cycle de vie canonique suppose implicitement l'exécution réelle ; la forme **raccourcie** du cycle en simulation n'est pas définie.
- **CR-10 — Désalignement avec la note de généralisation.** L'architecture liste le contrat `76` comme livrable sans intégrer la recommandation « semer la doctrine transversale, confirmer sur ECS avant de canoniser ». Le **séquencement** doctrine-d'abord vs local-d'abord n'est pas tranché → risque de churn (écrire `76`, puis le refactorer sous la doctrine).

## 1.4 Conformité aux principes Arsenal

| Principe | Respect | Réserve |
|---|---|---|
| Contrat/architecture avant YAML | ✅ | — |
| Séparation stricte des couches (capture→persist→derive→present) | ✅ conceptuel | INV-2 (étanchéité diagnostic↔décision) **énoncé mais non protégé** (pas de CI) |
| Contrats explicites (vocabulaire fermé des raisons) | ✅ | typage statique insuffisant (CR-7) |
| Read-only / aucun changement de comportement | ✅ décisionnel | coût d'observabilité non reconnu (CR-5) |
| Observabilité de première classe | ✅ | — |

**Conclusion de la critique :** architecture **valable mais non close**. Dix points (CR-1…10) doivent être tranchés en conception. Aucun ne remet en cause le modèle ; tous conditionnent sa constructibilité.

---

# 2. Cartographie logique des composants

Sans implémentation — composants **logiques** requis, par couche, en distinguant l'existant du nouveau.

## Couche capture (runtime — émission de faits)
| Composant | État | Note |
|---|---|---|
| Événement « cycle évalué » (snapshot complet) | **Nouveau** | porteur du contexte minimal + corrélation |
| Événement « suggestion modifiée » | **Nouveau** | continu |
| Événement « ajustement appliqué » | partiel (existe `chauffage_adjustment`) | à enrichir (corrélation, intentionnel/effectif) |
| Événement « ajustement refusé » | **Nouveau** | raison typée |
| Événement « abstention / gel » | **Nouveau** | cause typée (distinct du refus) |
| Événement « issue d'exécution » | partiel (ACK existe côté exécution) | à corréler |
| Événement « transition représentativité » | **Existant** | contexte |
| Événement « épisode de gel » | **Nouveau** | début/fin + cause |

## Helpers éventuels
| Candidat | État | Note |
|---|---|---|
| Porteur d'identifiant de corrélation | **À décider** | helper vs attribut d'événement — décision de conception (CR-1) |
| Instantané structuré du dernier cycle | partiel (`input_text.chauffage_last_adjustment`, dégénéré) | l'historique d'événements peut suffire — éviter le helper redondant |

## Entités de diagnostic (dérivées, lecture de l'historique)
Trajectoire effective de la courbe • indicateur de convergence • compteur de réversions • agrégat de fenêtre d'effet (unité à définir, CR-4) • taux de jours apprenants • indicateur de complétude (périodique seulement, CR-6) • indicateur de persistance de gel (CR-7).

## Stockage historique
Ensemble à persister : pente/parallèle **intentionnels et effectifs**, suggestions, erreurs lissées, état de représentativité, journal décisions/refus/abstentions, épisodes de gel — **joints** aux métriques de régulation existantes (oscillation, overshoot, cycles). **Question ouverte de rétention** (CR-8).

## Dashboards
Vue supervision : trajectoire effective • registre d'ajustements (avant→après, suggéré, raison typée, acquittement, corrélation) • panneau effet (tendance régime, limites explicites) • panneau contexte (représentativité, gel) • bandeau complétude/trou • lisibilité nominal/anomal.

## Journaux
Logbook (existant, partiel) — flux lisible par l'humain ; **couture à définir** avec les événements (éviter double source de vérité).

## Couches de dérivation
Pipeline **capture → persistance → dérivation → présentation**, frontière étanche (le diagnostic lit l'historique, jamais le runtime vivant ; aucune grandeur dérivée ne redevient entrée de décision).

---

# 3. Analyse des dépendances

| Dépendance | Classe | Justification |
|---|---|---|
| Cascade de décision Chauffage (suggestions, consignes, événement d'ajustement, représentativité, poêle stable, mode maison) | **Obligatoire** | Objet même de l'observation |
| Couche d'exécution (identifiant de requête / acquittement) | **Obligatoire** | Corrélation (CR-1) + valeur effective (CR-2) |
| Politique Recorder existante | **Obligatoire** | Conflit de rétention à résoudre (CR-8) |
| Observabilité existante (logbook, événements, includes recorder) | **Obligatoire** | Réutiliser, éviter la redondance (CR-3, journaux) |
| Métriques de régulation existantes (oscillation, overshoot, cycles) | **Souhaitable** (obligatoire si question 5 dans le périmètre) | Alimentent le panneau effet |
| Doctrine transversale d'observabilité (note de généralisation) | **Souhaitable** | Héritage ; décision de séquencement (CR-10) |
| Domaine ECS | **Optionnel** | Cible de **validation de la doctrine**, pas dépendance du build chauffage |
| Stratégie / garde CI | **Souhaitable** | Protéger INV-2 (étanchéité) — l'audit a montré l'absence de CI sur la chaîne courbe |

---

# 4. Registre de risques

| ID | Risque | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| **R-FONC-1** | La couche effet sur-promet ; attribution par ajustement impossible | Élevée | Moyen | Hiérarchiser : Q1–Q4 livrables, Q5 en tendance régime seulement ; définir l'unité d'attribution ou assumer « visualisation, pas score » (CR-4) |
| **R-FONC-2** | « Effectif » = inféré de l'ACK ≠ réalité appareil | Faible-Moy. | Moyen | Déclarer la sémantique ; à défaut de relecture, nommer la trajectoire « intentionnel confirmé » (CR-2) |
| **R-DETTE-1** | Rétention en conflit avec Recorder 30 j → soit gonflement de base, soit perte de l'historique saisonnier | Élevée | Élevé | Décider en conception la stratégie de long terme (statistiques / store dédié) **avant** build (CR-8) |
| **R-SUR-OBS-1** | Sur-observabilité : gonflement Recorder, charge événements/templates | Moyenne | Moyen | Borner l'ensemble persisté ; privilégier agrégats ; budget de volume (CR-5) |
| **R-SUR-OBS-2** | Trop d'indicateurs → bruit, superviseur décroche | Moyenne | Moyen | Jeu minimal viable lié aux 5 questions ; différer les « nice-to-have » |
| **R-REDOND-1** | Duplication des métriques diagnostic / du logbook existants | Moyenne | Faible | Référencer en place ; définir la couture (CR-3, journaux) |
| **R-REDOND-2** | Identifiant de corrélation en doublon/contradiction avec l'identifiant d'exécution | Moyenne | Moyen | Définir la cardinalité parent/enfant (CR-1) |
| **R-DOC-1** | `76` écrit puis refactoré sous la doctrine → churn | Moyenne | Faible | Trancher le séquencement doctrine/local en conception (CR-10) |
| **R-DOC-2** | Typage nominal/anomal trompeur sur gel persistant | Moyenne | Moyen | Ajouter une dimension durée/fréquence (CR-7) |
| **R-GOUV-1** | INV-2 (étanchéité) violé plus tard sans CI | Moyenne | Moyen | Stratégie CI pour les invariants d'observabilité |
| **R-COMPLET-1** | Complétude indéfinissable pour les événements continus | Faible | Faible | Restreindre la complétude aux événements périodiques (CR-6) |

---

# 5. Dossier de conception cible

Documents qui **doivent exister avant la moindre implémentation** :

```
00_documentation_arsenal/
├── architecture/chauffage/
│   ├── observabilite_auto_ajustement_courbe.md            [FIGÉ]
│   └── revue_architecturale_observabilite_...md           [CE DOCUMENT]
│
├── architecture/chauffage/conception/                     [À CRÉER]
│   ├── dossier_conception_observabilite.md
│   │     • Rôle : trancher CR-1…CR-10 (corrélation, intentionnel/effectif,
│   │       unité d'effet + délai de stabilisation, couture diagnostic,
│   │       ensemble persisté + rétention, jeu minimal d'indicateurs,
│   │       cycle simulation, périmètre complétude)
│   │     • Justification : pièce manquante n°1 ; sans elle, pas de build
│   │     • Dépend de : architecture figée
│   │
│   ├── registre_decisions_observabilite.md
│   │     • Rôle : journal des décisions (ADR) closant chaque ambiguïté
│   │     • Justification : tracer le « pourquoi » des choix de conception
│   │     • Dépend de : dossier de conception
│   │
│   ├── strategie_validation_observabilite.md
│   │     • Rôle : comment prouver que l'observabilité répond aux 5 questions
│   │       sur une période échantillon (test de reconstitution)
│   │     • Justification : définir le critère d'acceptation avant de coder
│   │     • Dépend de : dossier de conception
│   │
│   └── strategie_ci_observabilite.md  (ou section de validation)
│         • Rôle : protéger statiquement INV-2 (étanchéité) et le
│           vocabulaire fermé des raisons
│         • Justification : combler l'absence de CI relevée par l'audit
│         • Dépend de : dossier de conception
│
└── contrats/
    ├── chauffage/76_observabilite_auto_ajustement_courbe.md   [APRÈS conception — non rédigé]
    │     • Rôle : contrat métier local (allégé, héritant de la doctrine)
    │     • Dépend de : dossier de conception + décision de séquencement
    │
    └── transverses/observabilite_doctrine.md                  [CANDIDAT — note de généralisation]
          • Rôle : grammaire transversale (statut « candidat », à confirmer sur ECS)
          • Dépend de : décision de séquencement (CR-10)
```

**Pièce manquante critique : le `dossier_conception_observabilite.md`.** C'est lui qui transforme l'architecture (le *quoi*) en spécification constructible (le *comment décidé*), en closant CR-1…CR-10.

---

# 6. Roadmap documentaire

| Phase | Document | État |
|---|---|---|
| **Architecture** | `observabilite_auto_ajustement_courbe.md` | ✅ figé |
| **Architecture (méta)** | `note_observabilite_generalisation.md` | ✅ recommandation rendue |
| **Revue** | *ce document* | ✅ rendu |
| **Conception** | `dossier_conception_observabilite.md` + `registre_decisions` | ❌ **manquant — prochaine étape** |
| **Conception** | `strategie_validation` + `strategie_ci` | ❌ manquant |
| **Séquencement doctrine** | décision doctrine-first vs local-first (CR-10) | ❌ à trancher |
| **Contrat** | `76_…` (local, allégé) | ❌ après conception |
| **Implémentation** | — | ⛔ **bloquée** tant que la conception n'a pas tranché CR-1…CR-10 et la rétention |
| **Validation** | exécution de la stratégie de validation | ⛔ après implémentation |
| **Clôture** | — | — |

Ordre logique : **Architecture ✅ → Revue ✅ → Conception ❌ → (séquencement doctrine) → Contrat → Implémentation → Validation → Clôture.**

---

# 7. Sommes-nous prêts à construire ?

**Non — et c'était l'objet de la revue.** L'architecture est cohérente, conforme aux principes Arsenal au niveau conceptuel, et ne contient aucune erreur de modèle. Mais elle **diffère dix décisions opérationnelles** (CR-1…CR-10), dont **trois bloquantes** :

1. la **stratégie de rétention** face au Recorder 30 jours (R-DETTE-1) ;
2. la **sémantique de la valeur effective** (inférée vs mesurée, CR-2) ;
3. l'**unité d'attribution de l'effet** et le délai de stabilisation (CR-4).

Tant que ces points ne sont pas tranchés dans un **dossier de conception**, toute implémentation produirait des choix implicites non gouvernés — exactement le travers que l'audit reprochait au domaine d'origine.

**Nous sommes prêts à concevoir, pas à construire.** La prochaine étape unique est le `dossier_conception_observabilite.md` (et son registre de décisions), qui clôt CR-1…CR-10 et la question de rétention. Après lui — et après la décision de séquencement de la doctrine — viendra le contrat `76`, puis seulement l'implémentation.

---
*Revue architecturale — 2026-06-03. Phase Architecture → Conception. Aucun runtime, aucun YAML, aucun contrat rédigé.*
