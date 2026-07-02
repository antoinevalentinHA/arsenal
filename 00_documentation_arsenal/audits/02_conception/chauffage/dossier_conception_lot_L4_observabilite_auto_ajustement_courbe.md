# Dossier de conception — Lot L4
## Observabilité auto-ajustement courbe — Complétude & statut apprenant / épisodes de gel

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception de lot (détaillé) |
| **Lot** | **L4** (phase **P4** du plan d'action) — *uniquement* |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception de lot — aucune implémentation |
| **Version** | 1.0 |
| **Date** | 2026-07-02 |
| **Amont figé** | `76_observabilite_auto_ajustement_courbe.md` ; `plan_action_…md` ; `dossier_conception_observabilite.md` (CR-6, CR-7) ; `dossier_implantation_…md` (É-6, É-7) ; `spec_persistance_termes_decision_courbe.md` (P3) |
| **Cadre** | Lecture seule. Aucun YAML, code ou patch. Aucun document figé rouvert. **L5 à L9 non traités.** |

> **Objet :** spécifier, sans implémentation, la **couche complétude & statut apprenant** — l'indicateur de complétude du flux périodique (É-6), le statut apprenant/gelé de chaque cycle et les épisodes de gel (É-7) — de manière à répondre à la **question opposable Q7** (76 §3) et à préparer Q8. Aucune dérivation diagnostic (trajectoire, convergence, réversions, persistance) : **c'est L5**.

---

## 1. Périmètre exact du lot L4

**Inclus (L4) :**
- Un **indicateur de complétude** du flux périodique (76 §8) : distinguer un **trou de trace** (le cycle quotidien n'a pas été évalué) d'une **absence légitime d'ajustement** (cycle évalué, non actionnable) — écart **É-6**.
- Un **statut apprenant / gelé** matérialisé **par cycle** (76 §4) : dériver, du contexte déjà porté par l'événement de cycle, si le cycle était **apprenant** (éligible à l'apprentissage) ou **gelé/non apprenant**, avec sa **cause** — écart **É-7**.
- Les **épisodes de gel** (76 §5, événement obligatoire #8) : matérialiser **début / fin / cause** d'un épisode de gel d'apprentissage.
- La **persistance faible-cadence** des nouvelles grandeurs L4 (marqueur de dernier cycle, statut apprenant) selon la politique de rétention de classes (CR-8), en miroir du bloc Recorder P3.
- Le **taux de jours apprenants** (budget §6 « indispensable ») dans sa forme minimale (compteur dérivé), la **donnée mûrissant** ensuite par accumulation.

**Explicitement hors L4 (différé) :**
- **Trajectoire confirmée**, **convergence par fenêtre régime**, **compteur de réversions**, **drapeau « nominal persistant »** (re-typage dérivé CR-7) → **L5**.
- **Effet par fenêtre régime** → **L6**. **Dashboard diagnostic + logbook** → **L7**. **Validation de conformité globale + calibration** → **L8**. **Clôture** → **L9**.

L4 **dérive et persiste**, il ne présente pas (aucun dashboard) et ne re-type aucun fait.

---

## 2. Fichiers concernés

| Fichier | Rôle dans L4 | Nature de l'intervention (logique) |
|---|---|---|
| `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml` | Émetteur de `chauffage_courbe_cycle_evalue` (L1) | **Inchangé.** L4 **consomme** l'événement existant ; il ne touche **pas** le chemin décisionnel |
| **Nouvelle automation** consommatrice de `chauffage_courbe_cycle_evalue` | **Principal** : écrit le marqueur de dernier cycle, dérive le statut apprenant, émet l'événement d'épisode de gel sur transition | Consommateur pur, **en miroir** de `log_auto_ajustement.yaml` |
| **Nouveau `input_datetime`** (marqueur de dernier cycle) | Marqueur durable « dernier cycle évalué » — socle de la complétude | Mémoire persistante ; **jamais lue par la décision** (INV-2) |
| **Nouvelles entités dérivées** (statut apprenant, complétude) | Statut apprenant/gelé courant ; verdict de complétude à_jour/trou | `template` read-only ; **jamais lues par la décision** |
| `recorder.yaml` | Historisation faible-cadence des grandeurs L4 | Ajout d'un sous-bloc au bloc courbe existant (P3), même classe Population B |
| `tools/arsenal_ci/registres_entites.yaml` | Enregistrement des entités L4 | Extension (chaîne courbe encore absente du registre — cf. implantation §1) |
| `log_auto_ajustement.yaml` / scripts d'exécution | — | **Inchangés** (vérifier la non-régression) |

Patrons de réutilisation : `07_input_datetimes/ecs/dernier_cycle.yaml` (marqueur temporel de cycle) ; `11_automations/chauffage/courbe_de_chauffe/log_auto_ajustement.yaml` (consommateur d'événement) ; `11_automations/chauffage/representativite_thermique.yaml` (émission d'événement de transition).

---

## 3. Concept 1 — Statut apprenant / gelé (É-7)

### 3.1 Décision : dériver l'éligibilité, ne rien ré-évaluer
- **Problème.** « Apprenant » doit qualifier un cycle **sans** recalculer une décision (INV-1) ni créer une entrée de décision (INV-2).
- **Options.** (a) recomposer l'éligibilité à partir des entrées brutes dans une nouvelle logique ; (b) **lire** les champs déjà portés par `chauffage_courbe_cycle_evalue` (représentativité, auto actif, mode maison, `cycle_reason`) et n'en tirer qu'une **projection**.
- **Décision.** **(b)** — statut **dérivé** du seul événement de cycle. Un cycle est **apprenant** ssi la **porte d'éligibilité** était ouverte : `representativite == REPRESENTATIF` **et** `auto_actif` **et** `mode_maison == Normal`. Sinon **gelé / non apprenant**.
- **Justification.** Ces trois prédicats sont exactement les préconditions §7/§8 déjà émises par L1 (`c0/c1/c2`) ; les relire ne recrée aucune logique de décision et ne réintroduit rien dans la cascade (INV-2). Le statut est un **fait projeté**, pas une re-décision.

### 3.2 Cause de gel : vocabulaire fermé, aligné sur le runtime L1
- Un cycle **gelé** porte une **cause** issue du vocabulaire d'abstention/gel (76 §6), telle qu'**effectivement émise** par L1 dans `cycle_reason` :

| Cause (runtime L1) | Type | Correspondance 76 §6 |
|---|---|---|
| `non_representatif` | nominal | `gel_apprentissage` (facette représentativité, absorbe fenêtre/aération/absence/vacances via le proxy éco 24 h) |
| `auto_desactive` | nominal | `auto_desactive` |
| `hors_mode_normal` | nominal | `hors_mode_normal` |
| `suggestion_indisponible` | anomal | `suggestion_indisponible` |

- **Note d'alignement (importante).** Le contrat §6 énumère `gel_apprentissage` avec facettes *fenêtre / aération / poele_actif / absence / vacances*. Le **runtime** ne matérialise pas ces facettes séparément : la **représentativité thermique** (proxy `pourcentage_consigne_eco_24h_proxy`) est le **verrou d'éligibilité unique** (contrat 75 §7/§8) et absorbe ces contextes. L4 **respecte le runtime** : la cause de gel nominale dominante est `non_representatif`. La **décomposition en facettes n'est pas rouverte** ici (elle relèverait d'un enrichissement de la représentativité, hors périmètre — cf. 76 hors-périmètre et backlog). L4 **ne crée aucune cause nouvelle**.
- `suggestion_indisponible` (anomal) reste classé **gelé** au sens éligibilité **si** la porte §7/§8 est ouverte mais la donnée manque : la porte d'éligibilité est ouverte mais le cycle n'est pas apprenant **faute de signal**. Décision : le statut apprenant est **`REPRESENTATIF ∧ auto ∧ Normal`** (porte ouverte) ; `suggestion_indisponible` est alors un cycle **apprenant mais stérile (anomal)** — distingué par sa cause typée, **jamais** re-typé (CR-7). Un cycle **hors porte** est **gelé**.

### 3.3 Matérialisation
- Une **entité d'état courant** porte le statut apprenant/gelé instantané (dérivé read-only). Elle **n'entre pas** dans la décision.
- Le **fait par cycle** est déjà dans l'événement `chauffage_courbe_cycle_evalue` (champs `cycle_reason`, `representativite`, `auto_actif`, `mode_maison`) : L4 **n'ajoute pas** de champ à l'événement, il **projette**.

---

## 4. Concept 2 — Épisodes de gel (76 §5 #8)

### 4.1 Définition opposable
- Un **épisode de gel** est une **suite maximale de cycles consécutifs non apprenants**.
- Il possède un **début** (premier cycle gelé succédant à un cycle apprenant, ou au démarrage si déjà gelé), une **fin** (premier cycle apprenant succédant à un cycle gelé) et une **cause d'entrée** (la cause de gel du cycle d'ouverture).

### 4.2 Décision : détection sur transition, en miroir de la représentativité
- **Options.** (a) recalculer l'épisode a posteriori depuis l'historique (dérivation lourde) ; (b) **détecter la transition** apprenant↔gelé à chaque cycle et **émettre un événement** de début/fin, en miroir de `chauffage_representativite_thermique_transition`.
- **Décision.** **(b)** — l'automation consommatrice (§2) détecte le **front** entre le statut du cycle courant et le statut mémorisé du cycle précédent, et **émet** `chauffage_courbe_gel_episode` (`phase: debut|fin`, `cause`, `decision_id`, horodatage). L'état « en gel / apprenant » courant est mémorisé pour permettre la détection de front.
- **Justification.** Faible coût, cadence cycle (~1/jour), pas de balayage d'historique, corrélable au cycle par `decision_id`. Cohérent avec le patron de transition existant. Les **bornes** d'épisode sont ainsi **event-first**, la durée se reconstituant par différence de bornes.

### 4.3 Corrélation
- L'événement d'épisode porte le **`decision_id`** du cycle de front → rattachement sans ambiguïté au cycle (76 §7). Un épisode n'a **pas** de feuille d'exécution (cohérent : gel = pas d'application).

---

## 5. Concept 3 — Complétude du flux périodique (É-6, 76 §8)

### 5.1 Le problème central : trou ≠ silence légitime
- Un cycle **évalué non actionnable** (`suggestion_identique`, `non_representatif`…) **produit un événement** (acquis L1) : c'est un **silence légitime**, pas un trou.
- Un **trou de trace** = le cycle quotidien **n'a pas été évalué du tout** (HA arrêté à 10:00, automation en échec) → **aucun** événement ce jour-là.
- 76 §8 : ces deux absences **ne doivent jamais être confondues**.

### 5.2 Décision : marqueur durable de dernier cycle + verdict de fraîcheur
- **Options.** (a) inférer les trous en balayant la table `events` (SQLite, non requêtable via API — écarté, c'est précisément le risque P3) ; (b) **persister un marqueur « dernier cycle évalué »** (horodatage) écrit **à chaque** émission de cycle, et en dériver un **verdict de complétude** par **fraîcheur**.
- **Décision.** **(b)** — un `input_datetime` **marqueur de dernier cycle** est écrit par l'automation consommatrice à **chaque** `chauffage_courbe_cycle_evalue` (donc **y compris** les cycles non actionnables — c'est ce qui distingue le silence légitime du trou). Un capteur dérivé rend le verdict : **`a_jour`** si l'écart `now − dernier_cycle` reste sous le **seuil de fraîcheur**, **`trou_detecte`** au-delà.
- **Justification.** Le marqueur est **durable et requêtable sans SQLite** (comble le manque signalé spec §3.4). Écrit sur **tous** les cycles évalués, il matérialise exactement la distinction 76 §8. Le verdict est un **dérivé read-only**.

### 5.3 Seuil de fraîcheur — paramètre à défaut conservateur
- La cadence attendue est **1 cycle/jour à 10:00**. Le seuil de trou est un **paramètre provisoire** (CR-5 / conception §9 : calibrable a posteriori), fixé à un **défaut conservateur ≈ 26 h** (une marge > 24 h évite un faux trou par simple jitter d'ordonnancement).
- Conforme au dossier de conception : `76` nomme ce type de valeur comme **paramètre à défaut conservateur**, **non bloquant**, recalibré en **P8**.

### 5.4 Taux de jours apprenants (budget §6 « indispensable »)
- Forme **minimale** en L4 : un **compteur/ratio dérivé** des cycles apprenants sur les cycles évalués d'une fenêtre glissante. La **capacité** est livrée par L4 ; la **donnée statistiquement significative mûrit** ensuite (cf. plan §6, distinction capacité/conséquence). Aucun scoring, aucun re-typage.

---

## 6. Persistance L4 (rétention, CR-8)

En miroir du bloc P3 « CHAUFFAGE – AUTO-AJUSTEMENT COURBE (TERMES DE DÉCISION) » de `recorder.yaml` (Population B, faible cadence) :

| Entité L4 | Classe | Cadence | Raison |
|---|---|---|---|
| marqueur `input_datetime` dernier cycle | **CRITIQUE** | ≤ 1/jour | Socle de la complétude ; sans lui, aucun trou détectable a posteriori |
| statut apprenant courant (état) | **IMPORTANT** | ≤ 1/jour | Répond « quels cycles gelés/non apprenants » (Q7) sur historique |
| verdict de complétude (dérivé) | selon volume | faible | Lecture directe du trou en historique |

- **Long terme agrégé** (CR-8) : le marqueur et le statut sont **nativement ~1/jour** → conservables une saison **sans gonflement**. Aucune modification de la politique Recorder globale (`purge_keep_days`) n'est requise.
- L'événement d'épisode de gel reste **court terme détaillé** (événements bruts, ~30 j) — les **bornes** significatives sont projetées par le statut persisté.

---

## 7. Critères de validation du lot L4

| # | Critère | Preuve attendue |
|---|---|---|
| V1 | **Trou distingué du silence** | Un jour **sans** cycle évalué produit `trou_detecte` ; un cycle évalué **non actionnable** produit `a_jour` — les deux ne sont **jamais** confondus (76 §8) |
| V2 | **Statut apprenant correct** | Chaque cycle est classé apprenant / gelé selon `REPRESENTATIF ∧ auto ∧ Normal`, cohérent avec le `cycle_reason` émis |
| V3 | **Cause de gel typée** | Un cycle gelé porte une cause du vocabulaire fermé (§3.2), typée nominal/anomal ; aucune cause nouvelle inventée |
| V4 | **Épisode borné et corrélé** | Un basculement apprenant→gelé émet `phase: debut` ; gelé→apprenant émet `phase: fin` ; chaque événement porte `decision_id` et la cause d'entrée |
| V5 | **Marqueur écrit sur tous les cycles** | Le marqueur de dernier cycle est mis à jour **y compris** sur cycle non actionnable (sinon un silence légitime deviendrait faux trou) |
| V6 | **Read-only / capture pure** | Aucune entité **lue par la décision** n'est écrite par L4 ; le chemin décisionnel de `auto_ajustement.yaml` est **inchangé** (INV-1) |
| V7 | **Étanchéité** | Aucune entité dérivée L4 (statut, complétude, taux) n'est relue par `auto_ajustement.yaml` (INV-2) |
| V8 | **Rétention conforme** | Le sous-bloc Recorder L4 passe `check_recorder_contracts.py` ; entités faible-cadence Population B |

La validation **fonctionnelle globale** (les 8 questions) reste **L8**. L4 fournit la capacité de **Q7** et prépare **Q8**.

---

## 8. Risques de régression

| ID | Risque | Prob. | Impact | Maîtrise |
|---|---|---|---|---|
| RR-1 | Le marqueur **non écrit** sur cycle non actionnable → silence légitime lu comme trou | Moyenne | Élevé | **V5** gate : écriture du marqueur sur **toutes** les branches de l'événement de cycle, avant tout filtrage |
| RR-2 | Une entité dérivée L4 **relue** par la décision → rupture INV-2 | Faible | Élevé | Nommage/canal distinct ; **V7** ; garde CI d'étanchéité (registre `tools/arsenal_ci/`) |
| RR-3 | Toucher `auto_ajustement.yaml` pour écrire le marqueur → risque sur le chemin décisionnel | Moyenne | Élevé | **Décision §2** : marqueur écrit par une **automation consommatrice distincte** (miroir `log_auto_ajustement.yaml`), `auto_ajustement.yaml` **non rouvert** |
| RR-4 | Seuil de fraîcheur trop serré (< 24 h) → faux trous par jitter | Moyenne | Moyen | Défaut conservateur **≈ 26 h** (§5.3), paramètre recalibré P8 |
| RR-5 | Décomposer `gel_apprentissage` en facettes non matérialisées → invention runtime | Moyenne | Moyen | **§3.2** : cause dominante `non_representatif` ; facettes **non rouvertes** |
| RR-6 | Détection d'épisode perdant le statut précédent au redémarrage HA → faux front | Faible | Moyen | Statut « en gel » **persisté** (Recorder / restore) ; front calculé sur état restauré, pas sur défaut |
| RR-7 | Volume Recorder | Faible | Faible | Cadence ~1/jour, Population B, **V8** |

---

## 9. Démonstration de respect du contrat 76

| Obligation 76 | Contribution de L4 |
|---|---|
| §4 Traçabilité — épisodes de gel & statut apprenant/non apprenant | **Satisfait** : statut par cycle + épisodes bornés |
| §5 #8 Épisode de gel (début/fin/cause) | **Satisfait** : événement `chauffage_courbe_gel_episode` corrélé |
| §8 Complétude (trou ≠ absence légitime) | **Satisfait** : marqueur durable + verdict de fraîcheur |
| §6 Raisons (typage, pas de re-typage) | **Respecté** : causes du vocabulaire fermé, `nominal` persistant **non** re-typé (renvoyé à L5) |
| §10 INV-5 (refus ≠ abstention) | **Respecté** : gel = abstention, distinct des refus |
| §10 INV-7 (pas d'observabilité orpheline) | **Respecté** : chaque composant sert **Q7** (budget §6 indispensable) |
| §10 INV-8 (complétude & persistance) | **Satisfait pour la complétude** ; le **drapeau persistance** (re-typage nominal→à surveiller) reste **L5** |
| §4 Trajectoire confirmée / §3 Q6, Q8 | **Non traité** (L5) |

L4 **n'introduit aucun concept** hors contrat ; il réalise la couche **complétude/apprenant** et prépare le signalement de persistance (L5).

---

## 10. Démonstration INV-1 et INV-2

**INV-1 — Read-only / aucun changement de comportement.**
- L4 **ne rouvre pas** `auto_ajustement.yaml` : il **consomme** l'événement de cycle existant depuis une automation distincte (§2, RR-3).
- Aucune entité écrite par L4 n'est une **entrée lue par la décision** (V6). Le marqueur, le statut et la complétude sont des **sorties d'observation**.
- Une faute dans l'automation consommatrice **ne peut pas** interrompre la décision : elle est **découplée** (déclenchée par événement, en aval).

**INV-2 — Étanchéité diagnostic ↔ décision.**
- Sens strictement unidirectionnel : `cycle_evalue (capture) → marqueur/statut (persistance) → complétude/taux (dérivation)`. Aucune de ces grandeurs **ne réentre** dans `auto_ajustement.yaml` (V7).
- La décision lit la **représentativité brute** (`input_select.chauffage_representativite_thermique`), **jamais** le statut apprenant dérivé — la frontière est préservée.
- La garde CI d'étanchéité (registre des entités courbe, `tools/arsenal_ci/`) est **étendue** en L4 pour rendre cette frontière **opposable**.

---

## Rattachement

- **Réalise :** le lot **L4** (phase P4) du plan d'action, au service du contrat `76` (§4, §5 #8, §8, INV-8) — écarts **É-6** et **É-7** du dossier d'implantation.
- **Diffère explicitement :** L5 (trajectoire, convergence, réversions, drapeau persistance), L6–L9.
- **Ne rouvre :** aucun document figé (audit, architecture, conception amont, contrat) ; la décomposition des facettes de `gel_apprentissage` **n'est pas rouverte**.
- **Lecture seule :** aucune entité créée, aucun fichier modifié par ce dossier ; fichiers vérifiés sur HEAD courant.

*Dossier de conception L4 — 2026-07-02. Complétude & statut apprenant / épisodes de gel uniquement. Aucun patch, aucun YAML, aucun code.*
