# Dossier de conception — Lot L1
## Observabilité auto-ajustement courbe — Capture des faits de décision

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception de lot (détaillé) |
| **Lot** | **L1** (phase **P1** du plan d'action) — *uniquement* |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception de lot — aucune implémentation |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `4d23e0df` |
| **Amont figé** | `76_observabilite_auto_ajustement_courbe.md`, `plan_action_…md`, `dossier_implantation_…md` |
| **Cadre** | Lecture seule. Aucun YAML, code ou patch. Aucun document figé rouvert. **L2 à L9 non traités.** |

> **Objet :** spécifier, sans implémentation, la **couche de capture des faits de décision** — l'événement de cycle universel, l'identifiant de corrélation parent, et le vocabulaire refus/abstention — de manière à pouvoir l'implémenter ensuite en sécurité.

---

## 1. Périmètre exact du lot L1

**Inclus (L1) :**
- Émettre un **événement de cycle pour TOUS les cycles** quotidiens, y compris refusés, abstenus et silencieux (écart É-2).
- Doter chaque cycle d'un **identifiant de corrélation parent** (écart É-1) — **mint et portage** dans l'événement de cycle.
- Porter, dans cet événement, le **vocabulaire de raison refus/abstention** typé, **distinct** du `chauffage_raison` existant (écart É-3).
- Porter le **contexte minimal obligatoire** (contrat 76 §3.1).

**Explicitement hors L1 (différé) :**
- Rattachement de la **feuille d'exécution** (`request_id`) au parent et capture de la valeur confirmée → **L2**.
- Historisation → **L3**. Complétude / jour apprenant → **L4**. Dérivation diagnostic → **L5**. Effet → **L6**. Dashboard / logbook → **L7**. Validation de conformité globale / calibration → **L8**. Clôture → **L9**.

L1 ne produit **que de la capture**. Il ne persiste rien, ne dérive rien, ne présente rien.

---

## 2. Fichiers concernés

| Fichier | Rôle dans L1 | Nature de l'intervention (logique) |
|---|---|---|
| `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml` | **Principal** : émission de l'événement de cycle universel + mint du parent + calcul de la raison | Émission **en observation pure**, sur toutes les branches ; relocalisation du verrou d'abort sans modifier les prédicats |
| `11_automations/chauffage/courbe_de_chauffe/log_auto_ajustement.yaml` | Consommateur de `chauffage_adjustment` | **Inchangé en L1** (vérifier la non-régression) |
| `12_template_sensors/chauffage/diagnostic/raison.yaml` | **Patron de référence** (raison canonique) | **Non réutilisé** comme entité ; sert de modèle de style pour la raison courbe |
| `04_input_texts/chauffage/raison.yaml` (`chauffage_raison`) | Raison **centrale** d'exécution | **Non réutilisé** — canal distinct exigé |

Aucun autre fichier n'entre dans L1. Le portage persistant du parent vers l'exécution relève de L2.

---

## 3. Événements à enrichir

### 3.1 Décision retenue : un événement de cycle **nouveau et additif**

- **Problème.** Aujourd'hui `chauffage_adjustment` n'est émis que sur les branches **agissantes** (sim/réelle) ; le verrou de tête de `auto_ajustement.yaml` **abandonne** l'automatisation sur les cycles non agissants → aucun événement.
- **Options.** (a) **réaffecter** `chauffage_adjustment` pour qu'il se déclenche à chaque cycle ; (b) **ajouter** un événement de cycle distinct, universel, en laissant `chauffage_adjustment` intact.
- **Compromis.** (a) modifie la sémantique d'un événement **déjà consommé** par `log_auto_ajustement.yaml` → risque de régression du consommateur ; (b) additif, risque minimal, au prix d'une légère redondance sur les cycles agissants (deux événements partageant le parent).
- **Décision.** **(b)** — un **événement de cycle évalué** (libellé de conception : *cycle évalué*), émis **une fois par cycle, sur toutes les branches**. `chauffage_adjustment` **reste inchangé** et devient une **spécialisation** corrélable au cycle par le parent commun.
- **Justification.** Préserve l'existant et son consommateur (INV-1) ; rend la capture universelle ; évite la divergence (l'événement reflète la décision **réelle**, pas une ré-évaluation).

### 3.2 Charge utile de l'événement de cycle (logique, non implémentation)
- **identifiant de corrélation parent** (§4) ;
- **mode** : simulation / réel ;
- **issue par paramètre** (pente, parallèle) : appliqué / refusé / abstenu ;
- **raison typée** (§5) ;
- **contexte minimal** (76 §3.1) : pente & parallèle courants ; suggérés + erreur source ; représentativité (contexte) ; poêle stable ; mode maison ; auto actif.

### 3.3 Relocalisation du verrou — exigence structurelle
Le verrou de tête (auto actif, mode Normal, suggestions numériques, ≥1 diffère) **abandonne** actuellement l'automatisation. Pour émettre sur toutes les branches, il doit être **relocalisé** d'un verrou d'abort vers un **branchement interne**, de sorte que :
- l'**action** (application) se déclenche sous **exactement les mêmes prédicats** qu'aujourd'hui ;
- l'**événement** se déclenche **toujours**, sur toutes les branches.
La **logique de décision est préservée mot pour mot** ; seule sa **position** change. C'est le point sensible du lot (cf. §7).

`chauffage_representativite_thermique_transition` : **non touché** en L1.

---

## 4. Modèle de corrélation parent

- **Maille = le cycle** (conforme à la conception et au 76 §7).
- L'identifiant parent est **émis une fois par cycle**, **unique**, et **stable** sur l'ensemble des événements du cycle.
- Il est **généré par le cycle de décision** et **circule vers l'extérieur uniquement** (jamais relu par la décision — cf. INV-2).
- Portée L1 : le parent est **présent dans l'événement de cycle**. Sur un cycle agissant, il est **disponible** pour que `chauffage_adjustment` puis l'exécution s'y rattachent — mais **le rattachement de la feuille (`request_id`) est L2**.
- Réutilisation prévue (documentée pour L2, non réalisée ici) : la feuille sera le **`request_id` d'exécution existant** (`application_pente.yaml`/`application_parallele.yaml`, porteurs `retry_attempt1_id`/`retry_attempt2_id`) — aucun système d'identifiant parallèle créé.
- Cas refusé / abstenu : le cycle possède un parent **sans feuille** — pleinement représentable (76 §7).

---

## 5. Vocabulaire refus / abstention (extraction fidèle du 76 §6)

L1 implémente le **vocabulaire fermé et typé**, porté dans l'événement, **distinct** de `chauffage_raison`. **Refus ≠ abstention** (INV-5).

**Refus** *(une suggestion exploitable existait, la décision a décliné)* :
| Raison | Type |
|---|---|
| `suggestion_identique` | nominal |
| `bande_morte` | nominal |
| `baisse_bloquee_poele` | nominal |
| `hors_domaine` | anomal |

**Abstention / gel** *(aucun signal à décider)* :
| Cause | Type |
|---|---|
| `auto_desactive` | nominal |
| `hors_mode_normal` | nominal |
| `gel_apprentissage` (précisant : fenêtre / aération / poele_actif / absence / vacances) | nominal |
| `suggestion_indisponible` | anomal |

- L1 **ne crée aucune raison nouvelle** : il porte celles du contrat.
- La **persistance** d'une raison nominale (re-typage en « à surveiller ») relève de **L5**, pas de L1.
- Le canal est **propre à l'auto-ajustement courbe** ; `chauffage_raison`/`chauffage_raison_calculee` (raison centrale) ne sont **pas** réutilisés.

---

## 6. Critères de validation du lot L1

| # | Critère | Preuve attendue |
|---|---|---|
| V1 | **Équivalence comportementale** | L'action (application pente/parallèle) se déclenche sous des prédicats **identiques** avant/après L1, vérifiée sur un jeu représentatif de cycles **réels et simulés** |
| V2 | **Universalité** | Un événement de cycle est produit pour **chaque** cycle : agissant, refusé, abstenu, silencieux |
| V3 | **Raison correcte** | Chaque événement porte une raison du **vocabulaire fermé**, **typée** nominal/anomal ; refus distingué d'abstention |
| V4 | **Parent présent et unique** | Identifiant parent présent dans chaque événement de cycle, unique et stable ; un cycle agissant est corrélable à son `chauffage_adjustment` |
| V5 | **Capture pure** | Aucune entité **lue par la décision** n'est écrite par l'émission d'observation |
| V6 | **Existant préservé** | `chauffage_adjustment` et `log_auto_ajustement.yaml` **inchangés** et fonctionnels |
| V7 | **Simulation tronquée** | Les cycles simulés sont **marqués** et ne produisent **ni** feuille d'exécution **ni** prétention d'effet |

La validation **fonctionnelle complète** (les 8 questions) n'est **pas** un critère de L1 ; L1 ne couvre que la capture.

---

## 7. Risques de régression

| ID | Risque | Probabilité | Impact | Maîtrise |
|---|---|---|---|---|
| RR-1 | La **relocalisation du verrou** change *quand* l'action se déclenche | Moyenne | **Élevé** | Préserver les prédicats **mot pour mot** ; V1 (équivalence) comme **gate bloquant** avant tout déploiement |
| RR-2 | Réaffecter `chauffage_adjustment` casserait `log_auto_ajustement.yaml` | — (écartée) | — | Décision §3.1 : **ne pas réaffecter** ; événement distinct |
| RR-3 | Collision sémantique avec `chauffage_raison` (raison centrale) | Moyenne | Moyen | **Canal distinct** (§5) ; ne pas réutiliser l'entité |
| RR-4 | Une **faute dans l'émission d'observation** (ex. suggestion indisponible) interrompt l'automatisation et empêche l'action | Faible | Élevé | Émission **isolée des fautes** : une erreur d'observation ne doit **jamais** pouvoir abandonner la branche d'action ; émission positionnée après le calcul de décision |
| RR-5 | Cycle simulé produisant une feuille/effet fantôme | Faible | Moyen | Marquage `mode=simulation` ; troncature (V7) |

---

## 8. Démonstration de respect du contrat 76

| Obligation 76 | Contribution de L1 |
|---|---|
| §5 Événements obligatoires | **Avance** : « cycle évalué » (universel), « ajustement refusé », « abstention/gel » via l'événement + raison |
| §3.1 Contexte minimal | **Satisfait** dans l'événement de cycle |
| §6 Raisons obligatoires | **Satisfait** : vocabulaire fermé, typé, refus≠abstention |
| §7 Corrélation | **Avance** : parent (maille cycle) mint et porté ; feuille = L2 |
| §10 INV-5 (distinctions opposables) | **Satisfait** par le modèle de raison |
| §4 Trajectoire confirmée | **Non traité** (L3) |
| §8 Complétude | **Non traité** (L4) |
| §11 Validation globale | **Non traité** (L8) — L1 fournit V1–V7 locaux |

L1 **n'introduit aucun concept** hors du contrat ; il en réalise fidèlement la **première couche**.

---

## 9. Démonstration INV-1 et INV-2

**INV-1 — Read-only / aucun changement de comportement.**
- L'émission d'observation **n'écrit aucune entrée lue par la décision** (V5).
- Les **prédicats de décision sont préservés mot pour mot** ; seule leur position change (§3.3).
- L'**équivalence comportementale** (V1) est un **critère bloquant** : si l'action ne se déclenche pas sous des conditions identiques, le lot est rejeté.
- Une **faute d'observation ne peut pas abandonner** la branche d'action (RR-4).

**INV-2 — Étanchéité diagnostic ↔ décision.**
- L1 **ne fait que capter** : il ne crée **aucune grandeur dérivée** et ne présente rien.
- L'identifiant parent est **généré par le cycle** et **circule vers l'extérieur uniquement** ; il n'est **jamais relu** par la décision.
- **Rien de ce qui est émis ne réentre** dans `auto_ajustement.yaml` comme entrée de décision.
- Le sens **capture → (persistance → dérivation → présentation)** reste strictement unidirectionnel ; L1 occupe le seul premier maillon.

---

## Rattachement

- **Réalise :** le lot **L1** du plan d'action, au service du contrat `76`.
- **Diffère explicitement :** L2 à L9.
- **Ne rouvre :** aucun document figé. Lecture seule ; aucune entité inventée ; fichiers vérifiés sur HEAD `4d23e0df`.

*Dossier de conception L1 — 2026-06-03. Capture des faits de décision uniquement. Aucun patch, aucun YAML, aucun code.*
