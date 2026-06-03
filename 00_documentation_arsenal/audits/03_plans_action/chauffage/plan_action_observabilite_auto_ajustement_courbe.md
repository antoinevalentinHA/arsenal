# 🚧 ARSENAL — PLAN D'ACTION
## Chauffage — Observabilité de l'auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Plan d'action / exécution de chantier |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Plan d'exécution — non démarré |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Contrat de référence** | `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` (validé) |
| **Conception de référence** | `architecture/chauffage/conception/dossier_conception_observabilite.md` |
| **Cadre** | Aucun YAML, aucun code, aucune conception technique — plan d'exécution uniquement |

> **Objet :** répondre à « comment exécuter le chantier en sécurité jusqu'à sa clôture ». Le plan découpe la réalisation du contrat `76` en phases incrémentales, chacune porteuse de valeur, validable seule, et réductrice d'un risque. Il ne rouvre ni l'audit, ni l'architecture, ni la conception, ni le contrat.

---

## 1. Découpage en phases

Principe : **beaucoup de petites phases**, suivant le pipeline opposable *capture → persistance → dérivation → présentation*. Chaque phase est **read-only** (INV-1) et respecte l'étanchéité (INV-2).

| Phase | Objectif | Valeur visible | Validable seule | Risque réduit |
|---|---|---|---|---|
| **P0 — Cadrage & verrous préalables** | Lever les deux items non structurants du dossier de conception | Décisions d'amorçage figées | oui (revue documentaire) | Construire sur un fait non vérifié / paramètres flous |
| **P1 — Capture des faits de décision** | Émettre cycle + issues (appliqué/refusé/abstenu) + contexte minimal + corrélation de cycle | Les faits existent et sont inspectables en direct | oui (inspection live) | « Aucune trace du pourquoi » (manque central de l'audit) ; prouve read-only (INV-1) |
| **P2 — Issue d'exécution corrélée** | Rattacher l'acquittement au cycle ; capter la valeur confirmée | Q4 répondable en direct | oui | Applications non attribuables (corrélation) |
| **P3 — Persistance** | Conserver l'ensemble indispensable selon la politique de rétention | Q1–Q4 répondables a posteriori | oui (relecture d'une période passée) | Cécité sans historique ; conflit de rétention ; sur-observabilité (volume) |
| **P4 — Complétude & statut apprenant** | Indicateur de complétude (flux périodique) ; statut apprenant/gelé ; épisodes de gel | Q7 répondable | oui | Trou lu comme « aucun ajustement » ; gel silencieux |
| **P5 — Dérivation diagnostic** | Trajectoire confirmée, convergence, réversions, drapeau persistance | Q6 et Q8 répondables | oui | Dérive indécidable (question centrale de l'audit) ; **étanchéité** (INV-2) démontrée |
| **P6 — Couche effet** | Tendance d'effet en fenêtre régime, référençant les métriques de régulation existantes | Q5 répondable avec limites | oui | Sur-promesse de l'effet (bornée en le construisant en dernier) |
| **P7 — Supervision** | Vue assemblant les 8 réponses, lisibilité nominal/anomal, bandeau complétude, effet borné | Un humain lit réellement les 8 réponses | oui (test de lecture) | Illisibilité ; multiplication d'indicateurs |
| **P8 — Validation & calibration** | Preuve de conformité `76` §11 sur période échantillon ; calibrage des paramètres provisoires | Conformité démontrée | oui | Conformité non prouvée ; paramètres non calibrés |
| **P9 — Clôture** | Conditions de fin réunies, dossier de clôture | Chantier déclarable terminé | — | Clôture prématurée |

---

## 2. Ordonnancement & justification

L'ordre **est** le pipeline opposable, lu de l'amont vers l'aval — il n'est pas arbitraire, il est imposé par la doctrine :

- **P0 avant tout** : on ne construit pas sur un fait non vérifié (existence d'une relecture de courbe) ni sur des paramètres indéfinis.
- **P1 → P2** : le cycle de décision est le **parent de corrélation** ; l'issue d'exécution est une **feuille** qui s'y rattache — la feuille ne peut précéder le parent.
- **P2 → P3** : on ne persiste que ce qu'on a capté.
- **P3 → P4** : la complétude est une **propriété du flux périodique persisté** ; elle suppose la persistance.
- **P4 → P5** : la dérivation **lit l'historique** (jamais le runtime vivant, INV-2) ; elle suppose un flux persisté et son intégrité.
- **P5 → P6** : l'effet est la dérivation **la moins confiante et la plus dépendante** (métriques existantes) ; le construire en dernier permet d'en cadrer les limites une fois le reste stable.
- **P6 → P7** : on ne présente que ce qui est dérivé.
- **P7 → P8 → P9** : la validation suppose le pipeline complet ; la clôture suppose la validation.

Respect doctrinal : le sens unique **capture → persistance → dérivation → présentation** garantit qu'aucune grandeur dérivée ne peut redevenir entrée de décision (séparation décision/action/diagnostic ; observabilité read-only).

---

## 3. Critères d'entrée / sortie par phase

| Phase | Prérequis | Livrables | Critères de succès | Risques résiduels |
|---|---|---|---|---|
| **P0** | Contrat `76` validé | Fait de relecture de courbe tranché (présent/absent) ; paramètres provisoires figés (défauts conservateurs) ; critère d'étanchéité défini | Les deux items non structurants sont clos ; chemin intentionnel-confirmé / effectif-mesuré arrêté | Paramètres provisoires à recalibrer (assumé, P8) |
| **P1** | P0 | Faits de cycle + issues + contexte minimal + référence de corrélation | Tout cycle produit un fait contextualisé et corrélé ; comportement de décision **inchangé** | Couverture des cas rares (cycles limites) |
| **P2** | P1 | Issue d'exécution rattachée ; valeur confirmée captée | Chaque application porte une issue corrélée ; refus/abstention **sans** feuille d'exécution | Cas de divergence intentionnel↔confirmé à surveiller |
| **P3** | P2 | Historique de l'ensemble indispensable ; trajectoire confirmée requêtable | Une période passée se reconstitue ; volume dans le **budget** ; rétention conforme à la politique de classes | Volume long terme à surveiller |
| **P4** | P3 | Indicateur de complétude ; statut apprenant/gelé ; épisodes de gel | Un trou est signalé et **distinct** d'une absence d'ajustement ; cycles gelés identifiés | Complétude bornée au flux périodique (assumé) |
| **P5** | P4 | Indicateurs dérivés (trajectoire, convergence, réversions, persistance) | Les indicateurs se calculent depuis l'historique seul ; **aucune** rétroaction vers la décision | Pertinence des seuils de persistance (provisoires) |
| **P6** | P5 + métriques de régulation existantes disponibles | Tendance d'effet par fenêtre régime, avec limites explicites | Effet présenté **au niveau fenêtre**, jamais par ajustement ; dégradation propre si métriques indisponibles | Confiance limitée de l'effet (assumée, bornée) |
| **P7** | P6 | Vue de supervision | Les 8 questions sont lisibles ; nominal/anomal distinct ; effet borné affiché | Sur-affichage à élaguer |
| **P8** | P7 | Preuve de conformité `76` §11 ; paramètres calibrés | Les 6 démonstrations passent ; paramètres calibrés ou défauts validés | Démonstration de dérive saisonnière à maturation post-clôture |
| **P9** | P8 | Dossier de clôture | Conditions de clôture réunies (§7) | — |

---

## 4. Validation

Distinguer deux natures de validation :

**A. Preuve de conformité au contrat `76` (opposable, §11)** — le système conforme doit démontrer, sur période échantillon :
1. répondre aux **8 questions opposables** sur données ;
2. **reconstituer** tout cycle sans ambiguïté via la corrélation ;
3. **distinguer** cycle apprenant / gelé / trou de trace ;
4. présenter l'**effet** en tendance de fenêtre régime, **avec limites** ;
5. exposer la **trajectoire confirmée** sur au moins un cycle saisonnier *(capacité établie ; la donnée saisonnière mûrit ensuite — cf. §6)* ;
6. établir que l'**étanchéité** (INV-2) tient — aucune grandeur d'observabilité ne nourrit la décision.

**B. Validation fonctionnelle (utilité)** — au-delà de la conformité : un superviseur peut-il *réellement* comprendre une décision passée et constater une dérive ? Calibrage des deux paramètres provisoires (délai de stabilisation, seuils de persistance) une fois la donnée disponible. La validation fonctionnelle **ne conditionne pas** la conformité, mais conditionne la clôture (§7).

---

## 5. Risques de chantier

| Risque | Nature | Maîtrise |
|---|---|---|
| Couverture incomplète des cas de décision (cycles limites) | Technique | Capture exhaustive validée en P1 sur cas réels + simulation |
| Conflit de rétention / gonflement de base | Technique / dette | Politique de classes appliquée dès P3 ; budget vérifié comme critère de sortie |
| **Sur-observabilité** (trop d'indicateurs, charge) | Observabilité excessive | INV-7 : tout composant doit servir une question opposable ; jeu minimal en P3–P5, « souhaitables » différés ; budget opposable |
| **Rupture d'étanchéité runtime/diagnostic** | Doctrine / gouvernance | INV-2 érigé en **critère de sortie de P5** ; pipeline unidirectionnel ; vérification que nulle grandeur dérivée n'entre en décision ; garde de conformité prévue |
| Effet sur-interprété (causal par ajustement) | Fonctionnel | INV-4 : effet borné à la fenêtre régime ; construit en dernier (P6) ; limites affichées |
| Dérive documentaire (plan ≠ contrat) | Documentaire | Le plan **n'introduit aucun concept** ; toute exigence trace au `76` ; aucun document amont rouvert |
| Régression de comportement | Technique | INV-1 read-only : critère de sortie de **chaque** phase = comportement de décision inchangé |

---

## 6. Stratégie de déploiement

Le caractère **read-only** rend le déploiement intrinsèquement sûr : aucune phase ne peut altérer la décision. On exploite cela pour un déploiement **progressif et observé**.

- **Ordre de mise en production** : activation **couche par couche**, dans l'ordre du pipeline (capture → persistance → dérivation → présentation). Chaque couche activée est observée avant la suivante.
- **Simulation d'abord** : valider la capture et la dérivation sur les **traces de simulation** (inoffensives) avant de se fier aux traces réelles — cohérent avec le cycle de vie simulé tronqué.
- **Période d'observation** : après activation complète, une fenêtre d'observation suffisante pour couvrir **au moins un changement de régime** (froid/doux) et confirmer la lisibilité des 8 réponses.
- **Validation progressive** : chaque couche doit satisfaire ses critères de sortie (§3) avant d'enchaîner ; un retour arrière sur une couche n'affecte pas la décision.
- **Distinction capacité / conséquence** : la **capacité** de reconstituer une trajectoire saisonnière (Q6) est livrée par le chantier ; la **donnée saisonnière** elle-même mûrit après la clôture, par simple accumulation. La clôture **n'attend pas** une saison complète.

---

## 7. Clôture

Le chantier pourra être déclaré **terminé** lorsque **toutes** les conditions suivantes seront réunies :

1. Les **6 démonstrations de conformité** (`76` §11) passent sur une période échantillon.
2. L'**étanchéité** (INV-2) est vérifiée : aucune grandeur d'observabilité n'entre dans la décision.
3. Le **budget d'observabilité** est respecté (aucun composant orphelin ; volume maîtrisé).
4. Les **deux paramètres provisoires** sont calibrés, ou maintenus à un défaut conservateur **avec note de calibration** explicite.
5. La **capture long terme tourne** (la donnée saisonnière s'accumule).
6. Le **comportement de décision est resté inchangé** sur toute la durée du chantier (INV-1).

Éléments devant exister pour **ouvrir la clôture officielle** :
- un **dossier de clôture** consignant les 6 démonstrations et leur résultat ;
- la mise à jour de l'**index des audits** et la **mention au backlog** que l'item différé D-1 (protections empruntées fenêtre/aération/poêle-actif) devient désormais **surveillable** via les épisodes de gel — sans le traiter (il reste différé) ;
- l'absence de toute décision structurante rouverte.

Hors périmètre de la clôture : la confirmation de la grammaire transversale sur l'ECS (piste doctrinale distincte) ; le traitement de D-1 ; toute évolution du comportement d'apprentissage.

---

## Dépendances & rattachement

- **Réalise** : `76_observabilite_auto_ajustement_courbe.md`.
- **S'appuie sur** : le dossier de conception (mécaniques, rétention, paramètres) ; la couche d'exécution (acquittement corrélé) ; les métriques de régulation existantes (référencées en place).
- **Ne rouvre** : aucun document figé.

*Plan d'action — 2026-06-03. Exécution incrémentale, read-only, jusqu'à clôture. Aucun YAML, aucun code, aucune conception technique.*
