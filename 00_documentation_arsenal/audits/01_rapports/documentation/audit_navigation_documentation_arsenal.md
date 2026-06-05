# 🧭 Audit d'expérience de navigation — `00_documentation_arsenal/`

> **Nature.** Audit orienté *expérience de navigation*, pas audit documentaire académique. Objectif : mesurer la facilité réelle, pour un lecteur pressé, à atteindre une information donnée et à rebondir vers les documents liés.
> **Méthode.** Clone local en lecture seule de `antoinevalentinHA/arsenal`. Aucune modification, aucun patch, aucun renommage, aucun déplacement.
> **Périmètre.** 554 fichiers `.md` sous `00_documentation_arsenal/`.
> **Verdict d'une phrase.** L'hypothèse de départ est **confirmée et précisée** : le corpus n'est pas pauvre en *relations* — il les déclare abondamment en texte — il est pauvre en relations **activées** ; l'hypertexte est concentré à 70 % dans une seule couche, à sens unique.

---

## 1. Chiffres de cadrage (l'ossature du diagnostic)

| Mesure | Valeur | Lecture |
|---|---:|---|
| Fichiers `.md` | 554 | — |
| Liens internes `.md` (occurrences) | 449 | — |
| Fichiers contenant **au moins un** lien interne | 44 (8 %) | **92 % des fichiers n'ont aucun lien sortant** |
| Liens portés par la seule couche `navigation/` | 315 / 449 = **70 %** | l'hypertexte est **mono-localisé** |
| Liens d'ancre internes (`](#...)`) | **0** | aucune navigation intra-document |
| Chemins `.md` cités **en backticks** (non cliquables) | **2 894** | le graphe relationnel existe… en texte mort |
| Fichiers citant un `.md` mais **sans aucun lien** | **269** | relations connues de l'auteur, inertes pour le lecteur |

### Répartition des liens par famille

| Famille | Fichiers | Fichiers avec ≥1 lien | Liens | Fichiers « citent un .md mais 0 lien » |
|---|---:|---:|---:|---:|
| `navigation/` | 24 | **24 (100 %)** | 315 | 0 |
| `architecture/` | 64 | 7 | 70 | 10 |
| `contrats/` | 246 | 4 | 42 | **104** |
| `audits/` | 70 | 4 | 9 | 61 |
| `changelog/` | 99 | 1 | 3 | **78** |
| `ui/` | 26 | 2 | 2 | — |
| `outils_externes/` | 20 | **0** | **0** | — |
| `schemas_ascii/` | 3 | 0 | 0 | — |

**Ce que ces chiffres disent.** La navigation repose presque entièrement sur la couche `navigation/`. Or cette couche est, **par charte**, *non normative* et *détachable* : `navigation/README.md` pose explicitement « aucun lien obligatoire depuis les familles vers cette zone ». Conséquence mécanique : **le maillage est unidirectionnel**. Depuis un hub, on descend partout ; depuis n'importe quel document de famille, on ne remonte vers rien. Le lecteur qui n'entre **pas** par un hub (recherche GitHub, deep link, exploration de l'arbre) se retrouve dans un cul-de-sac.

---

## 2. Le constat central : un graphe sémantique déjà écrit, mais inerte

Le contrat `contrats/chauffage/30_decision_centrale.md` déclare en entête, **en clair** :

```
Subordonné à : contrats/chauffage/00_gouvernance_chauffage.md
Complémentaire de : 20_triggers_decisionnels.md · 70_autorisation_thermostat.md · 80_table_decision_canonique.md
Références boiler : contrats/boiler/socle_transactionnel.md
```

Les **cinq** cibles existent et résolvent. L'auteur **connaît** et **écrit** les arêtes du graphe — il ne les rend simplement pas cliquables. Ce motif est massif :

| Vocabulaire relationnel | Fichiers concernés |
|---|---:|
| `Référence` / `Références` | 132 |
| `Autorité` | 63 |
| `Subordonné à` | 26 |
| `Dépend de` / `Source de vérité` | 32 |
| `Consommé par` / `Consomme` | 15 |
| `Complémentaire de` | 11 |

**Reformulation de votre hypothèse à la lumière des données.** « La doc manque de liens internes » est exact ; mais la cause n'est pas que l'information soit *isolée conceptuellement* (les relations sont documentées), c'est que **les arêtes déclarées ne sont pas instanciées en hyperliens**. C'est une excellente nouvelle pour le rapport valeur/effort : convertir du texte déjà présent en lien est l'opération la moins risquée qui soit (cible connue, sémantique connue, zéro rédaction).

---

## 3. Cartographie des six parcours

Notation difficulté : 🟢 fluide · 🟡 friction modérée · 🔴 friction forte (recherche/devinette obligatoire).

### 3.1 Depuis un **contrat** — 🟡/🔴

- **Descendant (vers capteurs, CI, amendements)** : 🔴. Les références sont en backticks. Exemple : `30_decision_centrale.md` cite `20_`, `70_`, `80_` sans lien. Le lecteur doit deviner le chemin ou utiliser le file-finder GitHub.
- **Montant (vers l'index / le hub)** : 🔴. Aucun contrat ne contient de fil d'Ariane ni de retour vers `contrats/index.md`, et **encore moins** vers le hub `navigation/domaines/<dom>.md` (interdit par la charte « détachable »).
- **Latéral (entre frères du dossier)** : 🟡 pour `chauffage/` (24 contrats portent l'entête `Subordonné à / Complémentaire de`, donc les frères sont *nommés*), 🔴 pour `ecs/` (28 fichiers, **0 entête relationnel**, **pas d'index** de dossier).
- **Vers audit / changelog** : 🔴. Un contrat ne sait pas dire « j'ai été audité ici / modifié dans telle version ».

### 3.2 Depuis un **audit** — 🔴 (le pire parcours)

- Le rapport `audits/01_rapports/chauffage/audit_auto_ajustement_courbe.md` contient **0 lien**. Il ne pointe **ni** vers le plan d'action, **ni** vers la conception, **ni** vers le chantier, **ni** vers la clôture — alors que ces cinq maillons forment *sa propre chaîne*.
- La chaîne d'un domaine est physiquement **éclatée sur cinq dossiers de phase** (`01_rapports/` → `02_*/` → `03_plans_action/` → `04_chantiers/` → `05_clotures/`). Suivre la chaîne « vacances » de bout en bout impose de visiter **5 répertoires parents distincts**, à la main.
- **Aucun** des 37 sous-dossiers de `audits/` ne possède d'index. La seule porte d'entrée, `audits/index.md`, liste **32 chemins en texte brut** pour **2 liens cliquables** seulement.

### 3.3 Depuis un **backlog** — 🔴 (parcours fantôme)

- Le dossier conçu pour ça, `evolutions_futures/`, ne contient **qu'un seul fichier** (`lovelace_arborescence.md`).
- Les **vrais** backlogs vivent ailleurs, enfouis : `audits/04_chantiers/<domaine>/backlog_*.md` (alarme, chauffage, climatisation, ecs). Rien ne signale cette relocalisation au lecteur depuis `evolutions_futures/`, et les backlogs ne pointent pas vers l'audit qui les a produits ni vers le contrat qu'ils visent.

### 3.4 Depuis un **changelog** — 🔴

- `changelog/index.md` : **1 245 lignes, 0 lien cliquable**. C'est un récit chronologique qui cite versions et fichiers en backticks.
- Une entrée comme `changelogs/v15/v15_8_9.md` référence un contrat (`76_...md`), des audits (`audit_ecs_offsets.md`) et **la version précédente** (`v15_8_8.md`) — tout en backticks. **Pas de navigation préc./suiv.** entre versions, pas de lien « ce changement a modifié *ce* contrat ».

### 3.5 Depuis un **cadrage de chantier** — 🟡/🔴

- Les chantiers (`audits/04_chantiers/`) citent leur audit-source et le contrat visé en texte. Pas de lien montant vers le plan d'action, pas de lien aval vers la clôture correspondante (`05_clotures/`), alors que le couple chantier↔clôture est *un* objet logique scindé en deux dossiers.

### 3.6 Depuis un **composant technique** (`architecture/`, `outils_externes/`) — 🟡 / 🔴

- `architecture/` est **le bon élève des familles** : `architecture/index.md` est correctement lié (21 liens), comme `contrats/index.md`. La descente index → fichier y est fluide (🟢) ; mais le fichier d'architecture ne renvoie pas vers le contrat qu'il implémente (🟡).
- `outils_externes/` (20 fichiers, dont `nas_arsenal/`, `boiler_pi/`) : **0 lien, dans aucun sens**. 🔴. C'est la zone la plus orpheline du corpus.

---

## 4. Endroits où le lecteur doit « tricher »

Pour chaque cas : *document source · information cherchée · parcours actuel · difficulté · amélioration*.

| # | Document source | Information cherchée | Parcours actuellement nécessaire | Difficulté | Amélioration |
|---|---|---|---|---|---|
| 1 | `contrats/chauffage/30_decision_centrale.md` | les 3 contrats « complémentaires » cités | lire le nom en backtick → file-finder GitHub `t` → taper le nom | 🔴 doit deviner le chemin | activer les 5 backticks d'entête en liens (cibles déjà vérifiées) |
| 2 | `audits/01_rapports/chauffage/audit_auto_ajustement_courbe.md` | « où est le plan d'action / le chantier qui en découle ? » | remonter à `audits/`, ouvrir `03_plans_action/chauffage/`, deviner le fichier | 🔴 connaître l'architecture par cœur + remonter 2 dossiers | bloc « Chaîne » en pied de rapport (5 liens) |
| 3 | `audits/index.md` | ouvrir un rapport listé | sélectionner le texte, le recoller dans la barre d'URL ou le file-finder | 🔴 recherche GitHub forcée | transformer les 32 chemins-texte en liens |
| 4 | `changelog/changelogs/v15/v15_8_9.md` | le contrat `76_...` que ce changelog a ajouté | recherche GitHub sur `76_observabilite` | 🔴 doit deviner / chercher | lier les backticks de contrat + préc./suiv. version |
| 5 | `contrats/ecs/` (n'importe lequel) | la liste des 28 contrats ECS et leur ordre | remonter à `contrats/index.md` (qui ne liste pas l'intérieur du dossier) puis explorer l'arbre | 🔴 pas d'index de dossier | créer un `contrats/ecs/index.md` (futur chantier) |
| 6 | `evolutions_futures/` | « où est le backlog climatisation ? » | savoir qu'il a migré sous `audits/04_chantiers/climatisation/` | 🔴 connaissance tacite | note de renvoi + liens dans `evolutions_futures/` |
| 7 | `outils_externes/nas_arsenal/…` | le contrat `arsenal_nas` correspondant | recherche GitHub | 🔴 zone 0-lien | liens outil ↔ contrat dans les deux sens |
| 8 | n'importe quel hub (ex. `chauffage.md`) | revenir au document depuis une section longue | scroll manuel | 🟡 0 ancre dans le corpus | sommaires d'ancre dans les longs docs |

**Synthèse des « triches » imposées :**
- **Recherche GitHub forcée** : `audits/index.md`, `changelog/index.md`, tout `outils_externes/`, toute entrée de changelog.
- **Remonter ≥ 2 dossiers** : toute la famille `audits/` (chaînes éclatées sur 5 phases sans index).
- **Deviner un nom de fichier** : 269 fichiers citant un `.md` en backtick sans lien.
- **Connaître l'architecture par cœur** : suivre une chaîne d'audit ; trouver un backlog (relocalisé) ; savoir qu'un domaine « température intérieure » est logé sous `contrats/meteo/`.

---

## 5. Opportunités d'hyperliens, par direction

L'objectif n'est **pas** « plus de liens partout ». La charte `navigation/` interdit à juste titre les liens *obligatoires* des familles vers la couche navigation (pour préserver la détachabilité). Les ajouts ci-dessous restent **dans les familles** et activent des relations **déjà déclarées** — ils ne créent donc aucune dépendance nouvelle ni aucune dette de duplication.

- **Descendants** (parent → enfant) : index de dossier vers ses fichiers. Manquants pour `contrats/ecs/`, `contrats/alarme/`, `contrats/meteo/`, et **tous** les sous-dossiers `audits/`.
- **Montants** (enfant → parent) : fil d'Ariane minimal en pied de page renvoyant à l'index de famille. Aucune famille ne le fait. *N.B. : montée vers l'index de **famille**, pas vers le hub navigation — conforme à la charte.*
- **Latéraux** (frère ↔ frère) : activer les entêtes `Complémentaire de` (déjà 11 fichiers les portent ; 24 dans `chauffage/`).
- **Vers contrats** : depuis architecture (`implémente …`), depuis audits (`audite le contrat …`), depuis changelog (`modifie le contrat …`).
- **Vers audits** : depuis un contrat audité, une ligne « Audité dans … ».
- **Vers chantiers / clôtures** : relier chaque chantier à sa clôture (`04_chantiers/ ↔ 05_clotures/`) et à son plan-source.
- **Vers implémentations** : depuis un contrat, lien vers son architecture (`architecture/<dom>/`) quand elle existe.
- **Vers changelogs** : préc./suiv. entre versions ; depuis un audit clôturé, lien vers la version de clôture.

---

## 6. Liste priorisée des améliorations

Priorité = (valeur navigation) × (nombre de lecteurs touchés) ÷ (effort & risque). Rappel contrainte : ceci est un **diagnostic**, aucune de ces actions n'est exécutée ici.

| Rang | Action | Pourquoi | Effort | Risque |
|---|---|---|---|---|
| **P1** | **Activer en liens les 32 chemins-texte de `audits/index.md`** | porte d'entrée unique d'une famille entière, aujourd'hui inutilisable au clic | très faible | nul (chemins déjà exacts) |
| **P2** | **Activer les entêtes relationnels des contrats `chauffage/`** (`Subordonné à`/`Complémentaire de`, 24 fichiers) | densité maximale de relations déjà écrites, domaine le plus consulté | faible | nul (cibles vérifiées) |
| **P3** | **Bloc « Chaîne d'audit » en pied des rapports** (lien rapport→plan→conception→chantier→clôture) | supprime le parcours le plus pénible (remonter 5 dossiers) | faible/moyen | faible |
| **P4** | **Index de dossier pour les gros contrats sans index** : `ecs/` (28), `alarme/` (15), `meteo/` (11) | rend navigables les plus gros silos | moyen | faible (chantier, hors périmètre) |
| **P5** | **Préc./suiv. + liens de cible dans les entrées de changelog** | relie l'histoire aux objets qu'elle modifie | moyen | faible |
| **P6** | **Liens bidirectionnels `outils_externes/ ↔ contrats/`** | sort la zone 0-lien de l'isolement | faible | nul |
| **P7** | **Note de renvoi dans `evolutions_futures/`** vers les backlogs réels sous `audits/04_chantiers/` | dissipe le parcours fantôme du backlog | très faible | nul |
| **P8** | **Sommaires d'ancre (`#`) dans les longs documents** (`changelog/index.md`, contrats `00_`, `80_`) | 0 ancre dans tout le corpus aujourd'hui | moyen | nul |

**Note de séquencement.** P1, P2, P6, P7 sont des micro-interventions « texte → lien » à valeur immédiate et risque nul : idéales pour une première passe avant tout chantier structurant. P3/P4/P5 relèvent d'un chantier documentaire à cadrer (et touchent au gabarit) — à n'engager qu'ensuite.

---

## 7. Les liens à meilleur rapport valeur / effort (lot de démarrage)

Tous **internes au corpus**, tous **vérifiés résolvables**, tous **activation d'une référence déjà présente en texte** (sauf mention « nouveau bloc »). Format : *source → cible (sens)*.

### Bloc A — Contrat `chauffage` : activer les entêtes (latéral + montant) — *risque nul*

1. `contrats/chauffage/30_decision_centrale.md` → `00_gouvernance_chauffage.md` (montant)
2. `…/30_decision_centrale.md` → `20_triggers_decisionnels.md` (latéral)
3. `…/30_decision_centrale.md` → `70_autorisation_thermostat.md` (latéral)
4. `…/30_decision_centrale.md` → `80_table_decision_canonique.md` (latéral)
5. `…/30_decision_centrale.md` → `contrats/boiler/socle_transactionnel.md` (latéral inter-domaine)
6. `…/30_decision_centrale.md` → `30_decision_centrale__amendement.md` (vers amendement)
7. `…/80_table_decision_canonique.md` → `80_…__reecriture_partielle.md` (vers réécriture)
8. `…/00_gouvernance_chauffage.md` → `00_…__amendement.md` (vers amendement)
9. `…/45_aeration.md` → `contrats/aeration_blocage_chauffage/` (amont, propriétaire)
10. `…/65_pre_confort_retour_vacances.md` → `contrats/vacances.md` (aval, consommateur)
11. `…/66_adaptation_consigne_vacances.md` → `contrats/vacances.md` (aval, consommateur)

### Bloc B — `audits/index.md` : texte → lien (descendant) — *risque nul*

12. `audits/index.md` → `01_rapports/chauffage/audit_auto_ajustement_courbe.md`
13. `audits/index.md` → `01_rapports/chauffage/audit_diagnostics_thermiques_chauffage.md`
14. `audits/index.md` → `01_rapports/chauffage/audit_blocage_post_aeration_adaptatif.md`
15. `audits/index.md` → `01_rapports/ecs/audit_ecs_domaine.md`
16. `audits/index.md` → `01_rapports/ecs/audit_ecs_offsets.md`
17. `audits/index.md` → `02_arbitrages/ecs/arbitrage_watchdog_ecs.md`
18. `audits/index.md` → `02_contre_expertises/ecs/contre_expertise_watchdog_ecs.md`
19. `audits/index.md` → `01_rapports/vacances/audit_vacances_rapport_final.md`
20. `audits/index.md` → `02_contre_expertises/vacances/contre_expertise_audit_vacances.md`
21. `audits/index.md` → `03_plans_action/vacances/plan_action_vacances_couches_consommation.md`
22. `audits/index.md` → `04_chantiers/vacances/chantier_vac_imp_5_desinfection_retour.md`
23. `audits/index.md` → `05_clotures/vacances/cloture_partielle_vacances.md`
24. *(…et les ~20 autres chemins-texte restants de ce même fichier — même opération mécanique)*

### Bloc C — Chaîne d'audit chauffage : nouveau bloc « Chaîne » en pied de chaque maillon (montant + aval)

25. `01_rapports/chauffage/audit_auto_ajustement_courbe.md` → `03_plans_action/chauffage/plan_action_observabilite_auto_ajustement_courbe.md`
26. `…/plan_action_observabilite…md` → `02_conception/chauffage/dossier_conception_lot_L1_observabilite_auto_ajustement_courbe.md`
27. `…/dossier_conception_lot_L1…md` → `04_chantiers/chauffage/ch_observabilite_auto_ajustement_courbe.md`
28. `04_chantiers/chauffage/ch_observabilite…md` → `04_chantiers/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md`
29. `04_chantiers/chauffage/ch_observabilite…md` → `04_chantiers/chauffage/backlog_auto_ajustement_courbe.md`
30. `04_chantiers/chauffage/validation_L1…md` → `05_clotures/chauffage/validation_L1_observabilite_auto_ajustement_courbe.md` (renvoi canonique↔pointeur)

### Bloc D — Contrat ↔ implémentation ↔ changelog (vers implémentations / changelogs)

31. `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` → `architecture/chauffage/observabilite_auto_ajustement_courbe.md` (vers implémentation)
32. `architecture/chauffage/interface_ha_boiler_bridge.md` → `contrats/boiler/socle_transactionnel.md` (montant, vers contrat)
33. `architecture/chauffage/observabilite_auto_ajustement_courbe.md` → `revue_architecturale_observabilite_auto_ajustement_courbe.md` (latéral)
34. `changelog/changelogs/v15/v15_8_9.md` → `v15_8_8.md` (préc.)
35. `changelog/changelogs/v15/v15_8_9.md` → `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` (vers contrat modifié)
36. `changelog/changelogs/v15/v15_8_9.md` → `audits/01_rapports/ecs/audit_ecs_offsets.md` (vers audit cité)

### Bloc E — Outils externes ↔ contrats (sort la zone 0-lien)

37. `outils_externes/boiler_pi/` (doc principale) → `contrats/boiler/` (vers contrat) **et** réciproque
38. `outils_externes/nas_arsenal/` (doc principale) → `contrats/arsenal_nas.md` (vers contrat) **et** réciproque
39. `contrats/boiler/socle_transactionnel.md` → `outils_externes/boiler_pi/` (vers outil, amont)
40. `navigation/domaines/boiler.md` → déjà OK (référence, sert de modèle de symétrie)

### Bloc F — Backlog : dissiper le parcours fantôme (montant + latéral)

41. `evolutions_futures/lovelace_arborescence.md` → `audits/04_chantiers/lovelace/` (renvoi)
42. *(note de renvoi)* `evolutions_futures/` → `audits/04_chantiers/<dom>/backlog_*.md` (où vivent réellement les backlogs)
43. `audits/04_chantiers/climatisation/backlog_climatisation_hysteresis.md` → `audits/01_rapports/climatisation/audit_climatisation_arsenal.md` (montant vers audit-source)
44. `audits/04_chantiers/ecs/backlog_ecs.md` → `audits/01_rapports/ecs/audit_ecs_offsets.md` (montant vers audit-source)

### Bloc G — Latéraux à forte valeur dans les familles déjà denses

45. `contrats/vacances.md` → `contrats/chauffage/65_pre_confort_retour_vacances.md` (amont, réf. croisée déclarée)
46. `contrats/vacances.md` → `contrats/chauffage/66_adaptation_consigne_vacances.md` (amont)
47. `contrats/bouclage.md` → `contrats/ecs/04_bouclage_ecs_sous_systeme.md` (canonique → renvoi)
48. `contrats/ecs/04_bouclage_ecs_sous_systeme.md` → `contrats/bouclage.md` (renvoi → canonique)
49. `audits/03_plans_action/vacances/etape_A_reecriture_contractuelle_vacances_chauffage.md` → `contrats/chauffage/65_…md` (vers contrat réécrit)
50. `changelog/index.md` → bloc d'ancres `#` en tête (1 245 lignes, navigation interne aujourd'hui inexistante)

---

## 8. Garde-fous (cohérence avec la doctrine Arsenal)

- **Sens des liens des familles** : monter vers l'**index de famille**, *pas* vers la couche `navigation/`. La détachabilité de `navigation/` reste intacte ; aucun lien obligatoire famille→navigation n'est créé.
- **Agréger sans dupliquer** : activer une référence existante ne duplique rien ; ne jamais transformer un lien en recopie de seuil/version/entité (règle de la charte).
- **Anomalies signalées, non corrigées** : les liens proposés *pointent* les objets mal classés (ex. CH-x sous `climatisation/`) sans les déplacer — conforme à votre contrainte « aucun renommage / déplacement ».
- **Une passe « texte → lien » d'abord** : Blocs A, B, E, F, G partiels sont à risque nul et à valeur immédiate ; les blocs touchant un gabarit (chaîne d'audit, ancres, index de dossier) relèvent d'un chantier à cadrer ensuite.

---

*Audit en lecture seule. Aucune écriture sur le dépôt. Les chemins cités ont été vérifiés résolvables au moment du clone.*
