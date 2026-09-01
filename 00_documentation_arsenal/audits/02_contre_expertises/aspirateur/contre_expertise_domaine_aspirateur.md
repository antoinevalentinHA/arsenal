# Contre-expertise — domaine Aspirateur (intégration, conformité, commandabilité, clôture)

> ## CONTRE-EXPERTISE INDÉPENDANTE NON ARBITRÉE
>
> **Statut :** contre-expertise **indépendante** de domaine — **NON ARBITRÉE**. Document **non normatif et non opposable**. Aucun constat n'est tranché ; aucune gravité n'est officielle ; aucune requalification n'est prononcée.
> **Domaine :** `aspirateur` — pilotage du robot Roborock Q7 Max : mission segmentée mono-carte, conduite, supervision, entretien des consommables, interface.
> **SHA audité :** `31afb9fde567aa46e62a81d75fc1d3874f556011`
> **Destination d'archivage :** `00_documentation_arsenal/audits/02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md`
> **Mode :** lecture seule intégrale — aucun contrat, runtime, checker, registre, changelog ou arbitrage modifié ; `git status` propre à l'ouverture et à la fermeture de l'analyse.
> **Indépendance :** analyse construite **de bout en bout depuis l'arbre du SHA**. **Aucun rapport d'audit du domaine postérieur à ce SHA n'a été consulté**, aucune branche d'audit, aucune PR, aucune issue, aucune liste d'écarts présupposée. Le périmètre, les vérifications et les conclusions ont été reconstruits.
> **Documents de référence (en dépôt, au SHA audité) :**
> - `00_documentation_arsenal/contrats/aspirateur/` — README + 15 chapitres
> - `00_documentation_arsenal/architecture/03_doctrines/` — principes généraux, séparation décision/action, commandabilité, en-têtes de fichiers, solvabilité probatoire
> - `00_documentation_arsenal/audits/01_rapports/aspirateur/releve_entites_entretien.md`
> - `scripts/arsenal_contracts/check_aspirateur_contracts.py`
> **Principe directeur :** *un checker vert ne prouve pas la conformité fonctionnelle ; il prouve que la propriété qu'il balaie tient.*

---

## 1. Identification et statut

| Point | Valeur |
|---|---|
| Nature | Contre-expertise indépendante de domaine |
| Statut | **NON ARBITRÉ** — aucun constat tranché |
| Portée normative | **Aucune.** Document non opposable |
| SHA audité | `31afb9fde567aa46e62a81d75fc1d3874f556011` |
| État Git à l'ouverture et à la fermeture de l'analyse | arbre propre, un seul worktree, aucun stash |
| Contrats modifiés | **aucun** |
| Runtime modifié | **aucun** |
| Checker modifié | **aucun** |
| État de clôture modifié | **aucun** |
| Chantier créé ou modifié | **aucun** |
| Changelog créé | **aucun** |
| Arbitrage rendu | **aucun** |

> Ce document **consigne une analyse**. Il ne décide de rien. Toute suite — correction, arbitrage, ouverture de chantier, requalification — relève de l'opérateur et d'actes distincts.

---

## 2. Question centrale

Au SHA exact `31afb9f`, le domaine `aspirateur` peut-il être considéré comme :

1. **fonctionnellement intégré** ;
2. **contractuellement conforme** ;
3. **documentairement cohérent** ;
4. **opérable sans geste proposé mais inexécutable ou silencieusement ignoré** ;
5. **suffisamment prouvé pour être considéré comme clos** selon la gouvernance Arsenal ?

Les réponses figurent au §14, chacune sous l'une des quatre valeurs admises : `ÉTABLIE`, `ÉTABLIE AVEC RÉSERVES`, `NON ÉTABLIE`, `INDÉCIDABLE EN L'ÉTAT`.

---

## 3. Méthode et garanties d'indépendance

### 3.1 Garanties

- Travail exclusif sur l'arbre du SHA demandé, déjà `HEAD` au démarrage — **aucun checkout n'a été nécessaire**, aucune branche créée.
- **Aucun rapport d'audit du domaine postérieur à ce SHA n'a été lu**, aucune conclusion antérieure ou postérieure n'a servi de point de départ.
- Le seul recours à l'historique a porté sur l'**ascendance** du SHA audité, restreinte aux chemins du domaine, pour dater les lots (`#726` → `#751`).
- Toutes les commandes exécutées sont en **lecture seule** : `git rev-parse`, `git status`, `git grep`, `git ls-files`, `grep`, `sed`, `cat`, `wc`, `sha256sum`, exécution des checkers et des gates documentaires.

### 3.2 Régimes de preuve employés

| Régime | Définition retenue |
|---|---|
| `[FAIT]` | Établi par lecture statique du dépôt ou par commande reproductible |
| `[HYP]` | Comportement plausible, non observé — signalé comme tel |
| `[LECTURE]` | Interprétation d'une clause, ou articulation de plusieurs clauses |
| `[TERRAIN]` | Observation réelle nécessaire, non réalisable depuis le dépôt |
| `[NON ÉTABLI]` | Question posée, non tranchable au SHA audité |

> **Règle appliquée sans exception :** conformément à `R-VERDICT-1` de la doctrine de solvabilité probatoire, **aucune non-conformité fonctionnelle n'est déclarée acquise sur une absence**. Là où la doctrine exige une observation positive absente, le résultat est classé « à confirmer », jamais « non conforme ». Aucune reproduction relatée par un document du dépôt n'est présentée comme une observation propre à cette contre-expertise.

### 3.3 Passe de stabilisation

Une passe critique de stabilisation a été appliquée avant consignation. Elle a **borné** trois formulations qui dépassaient leur niveau de preuve, **fusionné** un constat qui doublonnait, **requalifié** deux constats acquis à tort en faits soumis à arbitrage, et **retiré** une sur-interprétation. **Seules les formulations finales stabilisées figurent dans ce document.** Les formulations retirées n'y sont pas reproduites.

---

## 4. Périmètre recensé et limites d'exhaustivité

### 4.1 Critère de recensement

| Balayage | Commande | Résultat |
|---|---|---|
| Par chemin | `git ls-files \| grep -ic aspirateur` | **67 fichiers** |
| Par contenu, hors chemin | `git grep -lIi -e aspirateur -e vacuum -e roborock` | **46 fichiers**, dont **28 vendorisés** (`custom_components/hacs/**`, `www/*-card*.js`) — traductions du frontal Home Assistant, hors de tout balayage CI du domaine, **non lus, exclusion justifiée** |

### 4.2 Limites d'exhaustivité — énoncées, non contournées

Le recensement est **exhaustif sur le critère employé**. Il ne l'est pas sur les **gabarits transverses que l'interface du domaine consomme** : le relevé `grep -ho "template:"` sur les cinq fichiers Lovelace du domaine identifie **11 gabarits hors périmètre recensé**.

| Ce qui est exhaustif | Ce qui ne l'est pas |
|---|---|
| **Contrats** — les 16 fichiers, 3 758 lignes, **lus intégralement** | Le **checker** du domaine (11 995 lignes) — lecture ciblée |
| **Runtime fonctionnel recensé** — les 26 fichiers, **lus intégralement** | L'**audit de faisabilité** (789 lignes) — lecture ciblée, document explicitement non normatif |
| La **chaîne d'héritage complète** des cartes d'action employées — 4 gabarits, lus intégralement | Le **dossier de cadrage** (17 fichiers) — lecture ciblée, conception subordonnée aux contrats |
| | **7 des 11 gabarits transverses** consommés par l'UI — non lus |

> **Aucune exhaustivité globale du domaine n'est revendiquée.** Ce document établit une exhaustivité **sur les contrats** et **sur le runtime fonctionnel recensé** ; il déclare une **inspection ciblée** des artefacts secondaires. Cette limite borne la portée d'une conclusion d'exhaustivité — elle ne l'annule pas sur les plans normatif et fonctionnel, elle l'annule pour un audit du **juge** lui-même.

---

## 5. Doctrine applicable

| Document | Lecture | Règles retenues comme opposables |
|---|---|---|
| `principes_generaux.md` | intégrale | §2 autorité unique · §3 séparation des couches · §6 trois régimes d'un état externe · §8 disponibilité explicite · §9 traçabilité |
| `separation_decision_action.md` | intégrale | « Une entité décide. Une autre agit. Jamais les deux à la fois. » |
| `commandabilite.md` | intégrale | §5 **A (impossible physiquement)** vs **B (interdit par politique)** · §6.1 symétrie obligatoire pour A · §6.2 override légitime pour B · §10 aucune implémentation imposée |
| `entetes_fichiers.md` | intégrale | **NORMATIF** — « le contenu du fichier ne peut jamais contredire son en-tête » ; « en cas de divergence, **l'en-tête fait foi** » ; toute violation est une **anomalie architecturale** |
| `solvabilite_probatoire.md` | intégrale | Échelle **L1–L5** · §1.1 `states` sous allowlist vs `events` (**R-L2-1**, **R-L2-2**) · §2 trois verdicts et **R-VERDICT-1** · §3 six qualifications et **R-QUALIF-1/2/3** · §4 **R-VERROU-1** · §5 dix exigences d'ouverture · « **aucun garde-fou CI à ce jour** » |
| `contrats/README.md` | intégrale | Statut des contrats : normatifs, prioritaires sur le code — « si une implémentation contredit un contrat, **l'implémentation est fausse** » |
| `redaction_changelog.md` | §1–§2 | Un changelog = une release ; hors déclenchement opérateur, la trace est **le merge/PR et la ligne de clôture du registre** |
| `REGISTRE_CHANTIERS.md` — gouvernance et cycle de vie | intégrale | Source canonique de « ce qui est réellement ouvert » ; co-commit obligatoire ; `Actif → Clos récent (≈90 j) → retiré` |
| `nommage_entites.md`, `id_automatisations.md`, `prefixe_domaine_automatisations.md`, `restauration_etat_helpers.md`, `causalite_metier.md`, `autorite_de_domaine.md`, `gestion_du_temps.md`, `git.md` | **non lues intégralement** — vérifiées **par leurs checkers**, tous verts | — |

---

## 6. Inventaire avec niveaux de lecture

### 6.1 Contrats — 16 fichiers, 3 758 lignes — **lus intégralement**

`README.md` · `01_finalite_et_perimetre` · `02_referentiel_cartes_et_pieces` · `03_profils_metier` · `04_nombre_de_passages` · `05_intention_de_mission` · `06_integrite_mono_carte` · `07_moteur_de_mission` · `08_etats_et_observation` · `09_refus_et_diagnostics` · `10_raccourcis` · `11_frontiere_ui` · `12_identifiants_a_fournir` · `13_hors_perimetre_arbitrages_et_questions_ouvertes` · `14_entretien` · `15_conduite_et_supervision`.

### 6.2 Runtime fonctionnel recensé — 26 fichiers — **lus intégralement**

| Famille | Nombre | Fichiers |
|---|---:|---|
| Helpers (17 entités) | 6 | `04_input_texts/aspirateur/{mission,entretien}` · `05_input_booleans/aspirateur/segments` (14 booléens) · `06_input_selects/aspirateur/{intention_carte,intention_passages,intention_profil}` |
| Scripts (2 609 lignes) | 6 | `lancer_mission` · `conduire_mission` · `composer_intention` · `appliquer_raccourci` · `reinitialiser_composition` · `declarer_entretien` |
| Automations | 4 | `10280000000001` supervision · `…02` projection de mission · `…03` projection d'entretien · `…04` remise à zéro de composition |
| Template sensors du domaine (6 entités) | 5 | `etat_canonique` · `motif_lisible` · `carte_courante` · `conditions_lancement_hors_carte` · `entretien` |
| Colorant de navigation | 1 | `12_template_sensors/system/cartes_dashboard_navigation/aspirateur.yaml` |
| Dashboards | 3 | `principal` · `carte` · `entretien` |
| Cartes Lovelace (1 289 lignes) | 4 | `panneau_operationnel` · `carte_robot` · `entretien` · `entretien_action` |
| Bandeau de navigation | 1 | `18_lovelace/includes/navigation/aspirateur.yaml` |
| Gabarit button-card du domaine | 1 | `carte_action_aspirateur_option` |

### 6.3 Artefacts secondaires — lecture ciblée, justifiée

| Fichier | Lecture | Justification |
|---|---|---|
| `check_aspirateur_contracts.py` (11 995 l.) | **ciblée** — en-tête doctrinal, `run()`, `check_ecrivain_unique` (ASP-CI-11), **`check_lovelace` (ASP-CI-7) intégral**, `check_referentiel_intention` (ASP-CI-28), `check_ui_entretien` (ASP-CI-42), `load_yaml_depot`, constantes fermées | L'objet est la **couverture réelle** de la CI, établie par le périmètre balayé et par l'exécution — non par la relecture d'un juge dont le selftest à 670 cas est lui-même exécuté |
| `audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md` (789 l.) | **ciblée** — synthèse, relevés d'entités, §8.1, tableau V4, observation discordante du 2026-08-26 | Relevé explicitement **non normatif et non opposable** ; il fonde le contrat, il ne le gouverne pas |
| `audits/01_rapports/aspirateur/releve_entites_entretien.md` (133 l.) | **intégrale** — empreintes SHA-256 **recalculées et vérifiées identiques** | Attestation de référence du périmètre Maintenance |
| `audits/02_conception/aspirateur/cadrage_l2_maintenance_ui/` (17 fichiers) | **ciblée** — `10_LOTS` §1–§3, `09_UI` §4 et §5, `11_ARBITRAGES_RENDUS`, `03_REFERENCES_CONTRATS`, `05_DIAGNOSTICS_SANITISES`, `06_ENTITES_ENTRETIEN` par empreinte | Conception **ratifiée** (`D-44`), subordonnée aux contrats |
| `REGISTRE_CHANTIERS.md` | **intégrale** sur les cinq sections d'état | — |
| `REGISTRE_COUVERTURE_VERIFICATION.md`, `audits/index.md`, `contrats/index.md`, `contrats/index.en.md` | **ciblée** sur les lignes du domaine | — |

### 6.4 Références croisées influençant réellement le comportement

| Fichier | Lecture | Effet |
|---|---|---|
| `11_automations/alarme/intrusion/mouvement.yaml` | **ciblée, bloc décisif intégral** | Consommateur de `vacuum.roborock_q7_max` (`ASP-INV-4` / `ALM-ROBO-1`) |
| `18_lovelace/dashboards.yaml`, `dashboards/navigation.yaml` | **ciblée, blocs intégraux** | Déclaration des 3 écrans ; tuile de navigation |
| `recorder.yaml`, `logbook.yaml` | **ciblée, régime de configuration établi** | Voir `LP-02` |
| Chaîne d'héritage des cartes d'action : `carte_base_v2` → `socle_action_simple` → `carte_action_standard` → `carte_action_standard_warning` | **intégrale, 4 fichiers** | Établit qu'**aucun état désactivé ni garde de disponibilité** n'existe sur les boutons d'action |
| 7 autres gabarits transverses consommés | **non lus** | Limite déclarée au §4.2 |

---

## 7. Modèle fonctionnel reconstruit

Reconstruit **depuis les fichiers**, sans partir d'une conclusion préexistante.

| # | Étape du modèle | Ce qui la porte au SHA audité |
|---|---|---|
| 1 | **Intentions opérateur** | 17 helpers : carte (3 options d'interface), 14 booléens de segment suffixés par la **paire canonique**, profil (**6 options**), passages (3 options). Aucun `initial:` — remise à zéro par l'automation `…04` au readiness |
| 2 | **Prérequis matériels et logiques** | Serpillière posée (catégorie **A**) pour les profils avec eau · état machine en classe **R** · témoins d'erreur à `none` / `ok` · aucune session ouverte · contexte cartographique confirmé par **double lecture fraîche** · **aucun seuil de batterie** |
| 3 | **Décision d'autorisation ou d'abstention** | `lancer_mission` — 13 étapes, 13 codes de refus, 8 branches de garde **rejouées intégralement** à l'étape 11 (`g2_*` ne réutilise aucun `g1_*`). Arbitrage `MISSION_DEJA_OUVERTE` / `SESSION_INACHEVEE` déterministe. **Étape 0a** : arrêt sec si le verdict courant appartient aux 9 valeurs de classe O/O-R |
| 4 | **Écritures préparatoires** | Trois, en `continue_on_error`, chacune avec son **instant de référence propre** : sélection de carte (avec **garde d'abstention** si le postétat est atteint), intensité d'eau (**avant** la confirmation de carte — c'est elle qui provoque le rafraîchissement publiant les cinq entités probantes), puissance d'aspiration. Le **mode de nettoyage n'est jamais écrit** |
| 5 | **Lancement effectif** | Trace d'intention → `COMMANDE/ISSUE_NON_ETABLIE` → **une seule** `vacuum.send_command` / `app_segment_clean`, charge utile **enveloppée**, `repeat` **absent** pour ×1. **Aucun `continue_on_error`** : l'exception remonte intacte |
| 6 | **Publication du verdict** | Vocabulaire **fermé à 34 valeurs**, trois écrivains disjoints — **W1** moteur (18), **W2** conduite (11), **W3** supervision (5). Deux codes du catalogue restent **non atteignables et le disent** : `CANAL_INDISPONIBLE`, `COMMANDE_REJETEE` |
| 7 | **Supervision de mission** | Automation `…01`, `mode: queued`, 5 déclencheurs. Porte d'entrée = **verdict classe O**. Amarrage prouvé **positivement** par disjonction (`vacuum == docked` **ou** état `charging`). Cessation prouvée **positivement** sur `idle`, et sur lui seul |
| 8 | **Conduite d'une mission ouverte** | `conduire_mission` — 4 gestes : garde de sens physique → **engagement écrit avant la commande** → **une** émission littérale → relecture 30 s → **relecture du verdict** avant conclusion (aucun `default:`) |
| 9 | **Notifications** | Persistante `aspirateur_mission` (lecteur pur du verdict, 9 phrases ≤ 120 car., extinction sur les 8 valeurs terminales) · persistante `aspirateur_entretien` (déclencheur borné à `attribute: postes_dus`) · **mobile exclusivement** dans les deux branches d'échec de W3 |
| 10 | **Refus et motifs opérateur** | `sensor.aspirateur_motif_lisible` traduit **36 valeurs** (18 codes du catalogue + 18 valeurs de cycle de vie). **Trois familles de refus n'écrivent aucun verdict** — voir `RC-02`, `FA-01` |
| 11 | **Entretien** | **M1** : autorité unique — périmètre fermé, 4 plafonds, seuil 10 % dans **un seul** bloc `variables:` ; témoin binaire **indisponible** quand la question n'est pas tranchable. **M2** : capture **avant** pression, trois gardes d'entrée, **une** pression littérale par branche, postcondition = **transition**, deux issues terminales |
| 12 | **Projection UI de chaque geste** | Trois écrans, bandeau commun. Le panneau appelle **quatre scripts et quatre seulement**. Aucune entité native d'action, aucun `button.press`, aucun libellé d'appareil, aucun index nu |
| 13 | **Missions lancées hors Arsenal** | **Structurellement non adoptées** par le backend : `ASP-INV-87` fait du verdict la seule porte d'entrée. **Mais** l'état canonique, l'attribut `mission_ouverte` et la tuile de navigation les **rendent** — voir `RC-02` |
| 14 | **Retour, pause, erreur, indisponibilité, fin de session** | Image totale à **dix états canoniques**, `mission_ouverte` porté en **attribut séparé**. Réconciliation au redémarrage : table à 6 lignes, **totale**, avec `CLOTURE/ISSUE_OPAQUE_APRES_REDEMARRAGE` distincte. `unknown` / `unavailable` ne produisent **jamais** d'issue métier |

### 7.1 Confrontation UI ↔ backend ↔ diagnostic ↔ contrat ↔ CI

| Parcours | Ce que l'UI présente | Ce que le backend accepte | Ce qu'il refuse | Ce que le diagnostic publie | Ce que la CI contrôle |
|---|---|---|---|---|---|
| Composition | 17 helpers, filtrés par carte | tout — aucune validation | rien | rien | ASP-CI-28 |
| Lancement | bouton **toujours** visible, confirmé | intention atomique + 13 gardes | 13 codes | motif lisible **visible** | ASP-CI-11 … 27 |
| Lancement pendant mission ouverte | **bouton visible** | — | arrêt 0a, **aucune écriture** | **rien à l'écran** ; journal et trace HA | **aucun** |
| Conduite ×4 | conditionnée à l'**état canonique / témoin natif** | **verdict classe O** + sens physique | arrêt sans écriture | **rien à l'écran** ; journal et trace HA | **aucun** |
| Profils avec eau | **toujours visibles** | serpillière posée | `PREREQUIS_MATERIEL_ABSENT` | motif **visible** | **aucun** |
| Entretien ×4 | toujours visibles | mesure numérique + restant < plafond | arrêt sans écriture | **rien** ; **causes co-visibles à l'écran** | ASP-CI-40 / 41 / 42 |

---

## 8. Matrice des gestes opérateur — trois écrans

> L'**écran 2** (`/aspirateur-carte-dashboard`) **ne porte aucun geste** : `tap_action`, `hold_action` et `double_tap_action` valent `none` sur les trois `picture-entity`. Seul le bandeau y est cliquable.

| # | Geste | Emplacement | Condition d'affichage | Activation | Service appelé | Gardes backend | Effets écrits | Motif si accepté | Retour opérateur si refusé | Si le prérequis disparaît entre affichage et exécution | Prédicats |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-3 | Carte ×3 | É1 · Composition | toujours | tap | `input_select.select_option` | aucune | sélecteur de carte | — | — | sans objet | coïncident |
| 4-17 | Pièce — 14 helpers, 2 à 8 visibles | É1 · Pièces | `conditional` sur la carte, **en-tête compris** | tap | `input_boolean.toggle` | aucune | booléen de segment | — | — | sans objet | coïncident — masquage = sens physique |
| 18-23 | Profil ×6 | É1 · Profil | **toujours** | tap | `input_select.select_option` | aucune | sélecteur de profil | — | — | sans objet | **divergent** (`RC-01`) sur les 2 profils avec eau |
| 24-26 | Passages ×3 | É1 · Passages | toujours | tap | `input_select.select_option` | aucune | sélecteur de passages | — | — | sans objet | coïncident |
| 27 | RDC — aspiration complète | É1 · Raccourcis | toujours | confirmation | `appliquer_raccourci` `rdc_aspiration` | champ fermé à 3 clés | carte + 14 booléens + profil + passages | — | motif d'arrêt (clé invalide) | sans objet | coïncident |
| 28 | RDC — serpillière complète | É1 · Raccourcis | **toujours** | confirmation | `appliquer_raccourci` `rdc_serpilliere` | idem | idem, profil `Serpillière moyenne` | — | — | sans objet | **divergent** (`RC-01`) |
| 29 | Étage — aspiration complète | É1 · Raccourcis | toujours | confirmation | `appliquer_raccourci` `etage_aspiration` | idem | idem | — | — | sans objet | coïncident |
| 30 | **Lancer la mission** | É1 · Lancement | **toujours — aucune condition** | confirmation ⚠️ | `composer_intention` → `lancer_mission` | 13 gardes **+ garde 0a** | verdict, trace, 3 réglages, commande | verdict de cycle de vie, motif **affiché** | 13 codes **affichés** ; **garde 0a : journal et trace HA seuls** | refus tardif étape 11, **avec motif affiché** | **divergent sur la seule garde 0a** (`FA-01`) |
| 31 | Réinitialiser la composition | É1 · Lancement | toujours | confirmation | `reinitialiser_composition` | aucune | 17 helpers | — | — | sans objet | coïncident |
| 32 | **Mettre en pause** | É1 · Conduite | `etat_canonique == nettoyage_reel` | confirmation | `conduire_mission` `pause` | **verdict classe O** + état ∈ activité | `PAUSE_ENGAGEE` → confirmée / non confirmée | motif affiché | **journal et trace HA seuls** | perte de la classe O ⇒ arrêt sans écriture | **divergent** (`RC-02`) |
| 33 | **Reprendre la mission** | É1 · Conduite | `etat_canonique == pause` | confirmation | `conduire_mission` `reprise` | classe O **+ `paused` + session `on` + 2 erreurs nominales** | `REPRISE_ENGAGEE` → … | motif affiché | **journal et trace HA seuls** | idem | **divergent** (`RC-02`, sous-cas *b*) |
| 34 | **Renvoyer à la base** | É1 · Conduite | `attr mission_ouverte == oui` **et** état ∉ {retour_base, amarrage, charge} | confirmation | `conduire_mission` `retour_base` | classe O + état ∉ {returning_home, docking, charging} | `RETOUR_ENGAGE` — O-R ; W3 conclut l'amarrage | motif affiché | **journal et trace HA seuls** | idem | **divergent** (`RC-02`) |
| 35 | **Arrêter la mission** | É1 · Conduite | `attr mission_ouverte == oui` | confirmation ⚠️ | `conduire_mission` `arret` | **classe O seule** (`ASP-INV-43`) | `ARRET_ENGAGE` → clôture confirmée / non confirmée | motif affiché | **journal et trace HA seuls** | idem | **divergent, dans les deux sens** (`RC-02`) |
| 36-39 | Déclarer un entretien ×4 | É3 · carte d'action séparée | **toujours** | confirmation nommant le poste | `declarer_entretien` `poste` | poste ∈ 4 · mesure numérique · restant **<** plafond | verdict d'entretien | verdict affiché sur É3 | **rien écrit** — mais les **deux causes sont lisibles sur le même écran** | mesure devenue illisible ⇒ arrêt, causes visibles | coïncident **en pratique**, par co-visibilité |
| 40-42 | Navigation ×3 | 3 écrans · bandeau | toujours | tap | `navigate` | — | — | — | — | clés vérifiées existantes (ASP-CI-42) | coïncident |

### 8.1 Synthèse de la matrice

- **8 surfaces d'action** portent un prédicat d'affichage qui **ne coïncide pas** avec le prédicat d'acceptation du backend : 3 relevant de `RC-01` (deux profils avec eau, un raccourci), 4 relevant de `RC-02` (les gestes de conduite), 1 relevant de `FA-01` (le lancement, sur sa seule garde 0a).
- Ces 8 surfaces relèvent de **2 constats autonomes** et **1 fait soumis à arbitrage** — elles ne sont **jamais** comptées comme 8 écarts.
- **Aucun état désactivé** n'existe sur la chaîne d'héritage des cartes d'action : `tap_action: call-service` + `confirmation` est inconditionnel `[FAIT]`.
- **Aucune occurrence** de refus n'a été observée sur l'instance par cette contre-expertise.

---

## 9. Couverture réelle de la CI

### 9.1 Commandes exécutées — lecture seule, reproductibles

| Commande | Résultat |
|---|---|
| `check_aspirateur_contracts.py` | **rc=0** — 40 lignes pour **42 contrôles logiques**, **0 écart**. Périmètre : 16 contrats · **463** fichiers Lovelace · 5 runtime L1 · 3 runtime L2 · **1 800** YAML (ASP-CI-11) · **1 814** YAML fonctionnels (ASP-CI-31) · 51 identifiants attestés · 1 M1 · 4 automations · 7 U0 |
| `check_aspirateur_contracts.py --selftest` | **rc=0** — 670 cas (103 conformes, **567 violations** rejouées) |
| `scripts/ci/run_checkers.py` sur les 88 checkers | **88/88 conformes** |
| `check_configuration_includes.py` | rc=0 — 22 includes résolus |
| `docs_lint.py` · `docs_ci_contract_counts.py` · `docs_ci_orphan_report.py` · `docs_ci_naming.py` · `docs_ci_navigation_leaf_pages.py` | rc=0 — DOC-CI-2 : 16 compteurs, 0 écart |
| `sha256sum` sur `06_ENTITES_ENTRETIEN.md` et `05_DIAGNOSTICS_SANITISES.md` | **empreintes identiques** à celles déclarées dans le relevé d'attestation |

### 9.2 Ce qui est réellement couvert

Numérotation `ASP-INV-*` · référentiels métier et technique, espace finale comprise · catalogue de codes total · partition R/A/E/N **rendue** sur 44 valeurs · six profils **dans le chapitre 03** · attestation des entités natives · absence d'entité native d'action dans 463 fichiers Lovelace · deux constantes temporelles · écrivain unique sur 1 800 YAML · disjonction et totalité des trois writers · charge utile **rendue** · convention `repeat` · mode jamais écrit · ordre de séquence · fraîcheur `last_reported` · branches de refus tardives · allowlist d'exception `continue_on_error` · référentiel U0 et les 3 raccourcis · périmètre d'entretien à 4 postes et 8 entités · seuil de 10 % · **visiteur YAML récursif** de la primitive irréversible sur 1 814 fichiers, dont l'état **dérive d'un essai réel sur six formes adverses** · séquence M2 rendue · écran d'entretien.

### 9.3 Trous établis

| # | Trou | Preuve |
|---|---|---|
| **T-1** | **Aucun contrôle ne confronte les conditions d'affichage du panneau opérationnel aux gardes du backend.** `check_lovelace` (ASP-CI-7) — **seul contrôle recevant les 463 fichiers Lovelace** — a été **lu intégralement** : il applique exactement deux expressions régulières (entité native d'action ; nom de service sous clé d'action) et n'ouvre **aucun** bloc `conditional`. `grep panneau_operationnel` sur le checker : **0**. ASP-CI-42 est borné à 3 fichiers de l'écran Entretien | `[FAIT]` |
| **T-2** | **Aucun contrôle ne vérifie la symétrie de `ASP-INV-13`.** `binary_sensor.…_serpilliere_fixee` n'apparaît dans aucun fichier Lovelace, et **aucun capteur dérivé du domaine ne l'expose** — `conditions_lancement_hors_carte` l'exclut nommément | `[FAIT]` |
| **T-3** | **ASP-CI-5 ne lit que `03_profils_metier.md`.** Les décomptes de prose des chapitres 05, 09, 12 et du README ne sont confrontés à rien | `[FAIT]` |
| **T-4** | **Aucun contrôle ne confronte un en-tête à son corps** : `sans_commentaires_yaml()` retire les commentaires avant analyse | `[FAIT]` |
| **T-5** | **`index.en.md` n'est gardé par aucune gate** : DOC-CI-2 déclare un périmètre « `contrats/index.md` UNIQUEMENT » | `[FAIT]` |
| **T-6** | **Aucun garde-fou CI pour la doctrine de solvabilité probatoire** — la doctrine le déclare elle-même | `[FAIT]` |
| **T-7** | **La CI ne prouve ni la réponse réelle de l'appareil aux quatre commandes de conduite, ni l'aboutissement d'une chaîne de retour, ni l'effet réel d'une pression de remise à zéro** — le registre de couverture l'écrit explicitement | `[FAIT]` |

---

## 10. Constats stabilisés

> **Aucun constat de cette section n'est arbitré.** Chacun porte son régime de preuve, sa couverture CI, son effet opérateur, sa confiance et l'élément susceptible de l'infirmer ou de le requalifier.

### 10.1 Divergences runtime / contrat statiquement démontrées — **2**

#### `RC-01` — L'interface ne porte aucune règle conditionnelle sur le prérequis matériel de catégorie A

| Rubrique | Contenu |
|---|---|
| **Fichiers et blocs** | `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` — grille « Profil de nettoyage », options `Serpillière moyenne` et `Serpillière intensive` ; grille « Raccourcis », bouton « RDC — serpillière complète » (`raccourci: rdc_serpilliere`) |
| **Clause applicable** | `ASP-INV-13` (`03` §4) — « **Symétrie obligatoire** : aucun chemin — ni raccourci, ni UI, ni appel direct au moteur — ne présente ces profils comme lançables lorsque le prérequis est absent. Une impossibilité physique n'admet **aucun** override. » ; `11` §2 ; `commandabilite.md` §6.1 |
| **Divergence structurelle statiquement démontrée** `[FAIT]` | (a) Aucune surface Lovelace ne lit `binary_sensor.roborock_q7_max_serpilliere_fixee` — **ni directement, ni via un capteur dérivé du domaine** : les deux voies sont fermées par balayage reproductible, `conditions_lancement_hors_carte` excluant nommément ce témoin de son périmètre. (b) Les trois surfaces ne portent **aucune** condition d'affichage ni d'activation. (c) La **chaîne d'héritage complète** des cartes d'action, lue intégralement, n'offre **aucun** état désactivé ni garde de disponibilité |
| **Interprétation engagée** `[LECTURE]` | `ASP-INV-13` impose une **obligation conditionnelle de présentation**. Une interface dépourvue de toute règle conditionnelle ne peut satisfaire une obligation conditionnelle. Cette lecture est **minimale** : elle ne dépend d'aucune interprétation du mot « lançable », seulement de l'existence d'une règle |
| **Occurrence réelle** | **Non observée par cette contre-expertise.** L'état du témoin au moment d'un usage n'est pas établi |
| **Preuve terrain** | `RT-09` — **utile, non nécessaire à l'existence du constat structurel** : celui-ci porte sur l'absence de la règle, indépendante de la valeur du capteur |
| **Question d'interprétation résiduelle** | `QA-04` — « présenté comme lançable » couvre-t-il l'affichage d'une option de sélecteur d'intention ? **Elle ne conditionne pas le constat** : sous la lecture restrictive, c'est le bouton « Lancer » qui devrait porter la garde, et il ne la porte pas davantage |
| **Effet opérateur allégué** | L'opérateur peut composer une intention refusée d'avance ; le refus n'intervient qu'après confirmation du lancement, **avec un motif correct, lisible et nommant le geste attendu** |
| **Couverture CI** | **aucune** — T-2 |
| **Sévérité proposée, non arbitrée** | moyenne — le backend refuse proprement ; le défaut est d'affordance, non de sûreté |
| **Confiance** | **élevée** sur les faits ; **élevée** sur la lecture minimale |
| **Ce qui l'infirmerait ou le requalifierait** | Une clause, absente au SHA, restreignant `ASP-INV-13` au seul geste de lancement **et** une garde correspondante posée sur ce geste |
| **Arbitrage** | **aucun** |

#### `RC-02` — Le prédicat d'affichage des surfaces de conduite ne coïncide pas avec le prédicat d'acceptation du backend

| Rubrique | Contenu |
|---|---|
| **Fichiers et blocs** | `panneau_operationnel.yaml`, section « Conduite » — `conditional` d'enveloppe `OR(état == nettoyage_reel, état == pause, attr mission_ouverte == oui)` et quatre `conditional` internes. Face à `10_scripts/aspirateur/conduire_mission.yaml` **étape 2** — `states('input_text.aspirateur_mission_verdict') not in verdict_ouvert` → `stop`. Et `12_template_sensors/aspirateur/etat_canonique.yaml`, attribut `mission_ouverte`, dérivé de `binary_sensor.roborock_q7_max_nettoyage` |
| **Clauses applicables** | `ASP-INV-87` (`15` §2) — « une mission Arsenal est ouverte **si et seulement si** le verdict appartient à la classe O … **aucun témoin natif ne l'établit ni ne s'y substitue** » ; `ASP-INV-48` (`08` §4) ; `ASP-INV-43` ; `11` §2 et §3 ; `commandabilite.md` §6 |
| **Divergence structurelle statiquement démontrée** `[FAIT]` | Les quatre conditions d'affichage lisent **exclusivement** `sensor.aspirateur_etat_canonique` (état ou attribut) ; la garde backend lit **exclusivement** le verdict, borné à 9 valeurs. Les deux prédicats ne coïncident pas |
| **Racine structurelle** `[FAIT]` | `ASP-CI-11` interdit **mécaniquement** à tout fichier hors des 8 nommés de mentionner `input_text.aspirateur_mission_verdict`, et son périmètre (`load_yaml_depot`, répertoires `NN_`) **inclut `18_lovelace/**`**. Le dossier de cadrage l'écrit — « la contrainte 4 est structurante … la seule alternative serait une seconde exception nominative. **Ce choix n'est pas rendu ici** ». **L'interface ne peut donc pas, par construction, aligner ses conditions sur l'autorité** |
| **Combinaisons logiquement possibles** `[FAIT — implication dérivée de deux prédicats purs, non une observation]` | **(a) Sur-offre** — verdict ∉ classe O **et** prédicat UI vrai : la ou les surfaces s'affichent, et `conduire_mission` s'arrête à son étape 2 **sans écriture**. Le cas d'une mission lancée depuis l'application Roborock satisfait cette combinaison **par construction**. **(b) Sous-offre** — verdict ∈ classe O **et** prédicat UI faux : la section entière, **en-tête compris**, disparaît, et l'arrêt devient inaccessible alors que le backend l'accepterait (`ASP-INV-43` : « en cas de doute, on **n'empêche pas** l'arrêt ») |
| **Sous-cas *b* — « Reprendre »** | Le bouton ajoute, au-delà de la garde de verdict, **trois conditions natives non projetées** — session `on`, `err_vac == none`, `err_dock == ok` — que rien n'empêcherait l'interface de lire, `ASP-CI-11` ne les frappant pas. **Sous-cas et non constat autonome** : il partage la cause principale |
| **Reproductions consignées** | 53 s, 25 s et 28,3 s de déplacement avec témoin de session à `off` — **relatées par `08` §3 et par l'en-tête de `lancer_mission.yaml`. NON observées par cette contre-expertise.** Elles étayent la plausibilité de la combinaison (b) ; elles ne la fondent pas |
| **Occurrence réelle** | **Non observée par cette contre-expertise** |
| **Preuve terrain** | `RT-07` et `RT-08` — **utiles, non nécessaires à l'existence de la divergence structurelle**, qui est démontrée par lecture des prédicats |
| **Effet opérateur allégué** | Boutons offerts et sans effet visible sur une mission externe ; perte de la commande d'arrêt pendant les phases où le témoin natif est `off` alors que la mission Arsenal reste ouverte |
| **Couverture CI** | **aucune** — T-1 ; `ASP-CI-11` **empêche activement** l'alignement direct |
| **Sévérité proposée, non arbitrée** | élevée — écart le plus structurant du domaine |
| **Confiance** | **très élevée** sur la divergence de prédicats et sur la racine ; **moyenne** sur la fréquence des occurrences |
| **Ce qui l'infirmerait ou le requalifierait** | Une lecture retenant que `ASP-INV-48` s'apprécie sur le sens physique seul — mais la garde backend deviendrait alors plus restrictive que le contrat, sans motif rendu à l'écran |
| **Arbitrage** | **aucun** — questions ouvertes `QA-01`, `QA-02`, `QA-03` |

### 10.2 Contradictions contractuelles certaines — **2**

#### `CC-01` — « Mission ouverte » porte deux définitions concurrentes

| Rubrique | Contenu |
|---|---|
| **Blocs** | `08` §1 (dixième état canonique = « une session est ouverte ») · `08` §3 (« c'est son **seul** usage contractuel ») · `ASP-INV-68` (« ne dérive pas de l'état machine mais du **témoin de session** ») **contre** `15` §2 `ASP-INV-87` (« **si et seulement si** le verdict … **aucun témoin natif** ne l'établit ni ne s'y substitue ») |
| **Fait** `[FAIT]` | Le runtime matérialise **les deux** — attribut `mission_ouverte` (natif) et liste `verdict_ouvert` (verdict) — et `11` §3.3 impose à l'interface de restituer le dixième état canonique séparément, ce qu'elle fait avec la définition **native** |
| **Preuve terrain** | **sans objet** — contradiction établie par lecture |
| **Effet opérateur** | Le libellé « Mission : Ouverte » peut être vrai au sens de `08` et faux au sens de `15` simultanément. **Cause proximale de `RC-02`** |
| **Couverture CI** | aucune — les deux notions sont vérifiées séparément, et chacune est cohérente |
| **Sévérité proposée, non arbitrée** | élevée, structurante |
| **Confiance** | très élevée |
| **Ce qui l'infirmerait** | Une clause, absente au SHA, distinguant nommément « session ouverte » et « mission Arsenal ouverte » dans le vocabulaire canonique |
| **Arbitrage** | **aucun** — question `QA-01` |

#### `CC-02` — `01` §4 exclut l'entretien du périmètre ; le chapitre `14` le contractualise

| Rubrique | Contenu |
|---|---|
| **Blocs** | `01` §4, ligne « **L'entretien** (station de vidange, lavage de serpillière, consommables) — **aucun besoin exprimé** », **non amendée**, contre `14` en entier et les lots livrés. `08` §6 **a** été amendé pour ce motif ; `01` §4 ne l'a pas été |
| **Fait** `[FAIT]` | Lecture directe des deux chapitres au même SHA |
| **Interprétation** `[LECTURE]` | `01` fixe le périmètre du domaine ; `14` l'étend sans amender `01`. Le chapitre spécial l'emporte en pratique ; la table du périmètre reste fausse |
| **Preuve terrain** | **sans objet** |
| **Effet opérateur** | **aucun** |
| **Couverture CI** | aucune |
| **Sévérité proposée, non arbitrée** | faible |
| **Confiance** | très élevée |
| **Ce qui l'infirmerait** | Un amendement de `01` §4, absent au SHA |
| **Arbitrage** | **aucun** — question `QA-06` |

### 10.3 Divergences documentaires certaines — **9**

Toutes sont `[FAIT]`, établies par lecture directe ou balayage reproductible. Preuve terrain : **sans objet** pour toutes. Arbitrage : **aucun**.

| ID | Formulation | Emplacements | Clause de référence | Effet opérateur | CI | Sévérité proposée | Ce qui l'infirmerait |
|---|---|---|---|---|---|---|---|
| `DD-01` | « **cinq** profils » alors que la table en arrête **six** | `contrats/aspirateur/README.md` · `05` §2 et §4 · `09` §2 · `12` §2.1 · **`12_template_sensors/aspirateur/motif_lisible.yaml`** · `contrats/index.md` · `index.en.md` · registre de couverture · `03_REFERENCES_CONTRATS.md` | `03` §1 « **Six profils, et six seulement** » | **OUI** — le motif `PROFIL_INCONNU` **affiché à l'opérateur** annonce cinq profils | T-3 | moyenne | une lecture retenant « cinq » comme le compte de référence — contredite par `03` §1 |
| `DD-02` | En-tête annonçant **cinq raccourcis** et **cinq clés inexistantes** (`rdc_complet`, `entree_escaliers_wc_rdc`, `sejour_seul`, `etage_complet`, `annexe_complete`) ; corps et champ `fields` en portent **trois** (`rdc_aspiration`, `rdc_serpilliere`, `etage_aspiration`) | `10_scripts/aspirateur/appliquer_raccourci.yaml` | `entetes_fichiers.md` — « le contenu ne peut jamais contredire son en-tête », « **l'en-tête fait foi** », toute violation est une **anomalie architecturale** ; `ASP-INV-57` | non depuis le panneau (les 3 clés employées sont valides) ; **oui pour tout appel programmatique guidé par l'en-tête** | T-4 | moyenne | un amendement de l'en-tête, absent au SHA |
| `DD-03` | « **Réalisation : aucune** » · « runtime, checker, dashboard, navigation : **hors lot** » · « conception du dashboard : **lot ultérieur** » | `README.md` · `13` §1 · `11` §4 | prose périmée au même SHA | non | aucune | faible | — |
| `DD-04` | « la couche **U0 n'existe pas** » | `conduire_mission.yaml` · `notification_mission.yaml` | `entetes_fichiers.md` | non | T-4 | faible | — |
| `DD-05` | « **deux écrans** » alors qu'il y en a trois | `dashboards/aspirateur/principal.yaml` · `panneau_operationnel.yaml` · `dashboards/aspirateur/carte.yaml` | `entetes_fichiers.md` | non | T-4 | faible | — |
| `DD-06` | Compteur **14** au lieu de 16 ; « ahead of runtime » ; « five fixed profiles » | `contrats/index.en.md` | `13` §4 affirmait avoir inscrit la ligne « **à son compte réel** » | non | T-5 | faible | — |
| `DD-07` | « lots Maintenance, L2 et UI **à venir** » · « modèle d'états à **huit** situations » · « Dashboard **hors lot** » | `contrats/index.md` | tous livrés ; dix états | non | DOC-CI-2 ne vérifie que l'entier | faible | — |
| `DD-08` | Dossier de cadrage ratifié listant **cinq** profils | `09_UI.md` · `11_ARBITRAGES_RENDUS.md` · `03_REFERENCES_CONTRATS.md` | conception subordonnée aux contrats | non | aucune | faible | — |
| `DD-09` | Table « Raccourcis attendus — V1 » à **deux** lignes sous un texte annonçant **trois** raccourcis | `10` §3 | résolu par `10` §3.1 | non | aucune | négligeable | — |

### 10.4 Lacunes de preuve — **4**

#### `LP-01` — Aucune qualification de solvabilité probatoire dans le domaine

| Rubrique | Contenu |
|---|---|
| **Fait** `[FAIT]` | Balayage reproductible de **10 motifs** — `solvab`, `L1–L5`, `L1-L5`, `verrou actif`, `réserve différée`, `non solvable`, `opportuniste`, `critère de retrait`, `date de réévaluation` — sur le **périmètre documentaire et runtime complet du domaine** : **une seule occurrence**, `TEMPORISATEUR OPPORTUNISTE` dans un commentaire de code, **sans rapport** |
| **Clauses** | `solvabilite_probatoire.md` §3 **R-QUALIF-1** (« une réserve non qualifiée est réputée **verrou actif** … dette perpétuelle silencieuse ») · §4 **R-VERROU-1** · §5 (dix exigences d'ouverture : identifier la preuve, qualifier L1–L5, vérifier le producteur, la conservation, l'horizon, le propriétaire, la date de réévaluation, le critère de retrait) |
| **Réserves concernées** | `ARB-1` à `ARB-5` · `QO-1` à `QO-6` · la postcondition « **prédit, non testé** » du relevé d'attestation · les cinq validations terrain dues au registre |
| **Interprétation** `[LECTURE]` | Par `R-QUALIF-1`, toutes ces réserves sont **réputées verrous actifs**. Aucune des dix exigences du §5 n'est satisfaite pour aucune d'elles |
| **Preuve terrain** | **sans objet** — constat documentaire |
| **Effet opérateur** | aucun direct ; effet de gouvernance sur la clôture |
| **Couverture CI** | **impossible** — la doctrine déclare n'avoir « aucun garde-fou CI à ce jour » (T-6) |
| **Sévérité proposée, non arbitrée** | élevée au regard de la question de clôture |
| **Confiance** | **très élevée** sur le fait ; **élevée** sur la lecture |
| **Ce qui l'infirmerait** | Une qualification portée ailleurs qu'aux emplacements balayés, ou sous un vocabulaire non couvert par les 10 motifs |
| **Arbitrage** | **aucun** — question `QA-07` |

#### `LP-02` — Le moyen de preuve des validations dues n'est pas formellement qualifié

| Rubrique | Contenu |
|---|---|
| **Régime de `recorder` établi** `[FAIT]` | `recorder.yaml` porte **exactement quatre clés de tête** — `auto_purge`, `purge_keep_days: 30`, `commit_interval`, `include` ; `include:` ne contient que `entities:` ; **aucun `exclude:`, aucun `domains:`, aucun `glob`, aucun `event_types`**. C'est une **allowlist stricte par entité**. `logbook.yaml` : `include: entities:` également |
| **Conséquence sur les états et les attributs** `[FAIT]` | **Aucune entité `aspirateur*` ou `roborock*` ne figure dans l'allowlist** (balayage reproductible). Sous ce régime, une entité absente n'est pas enregistrée : il en résulte l'**absence de tout historique d'état et d'attribut** pour les 6 entités dérivées et les 17 helpers du domaine. Les attributs porteurs des mesures d'entretien (`postes`, `restant_h`, `plafond_h`) ne sont donc conservés par **aucun instrument du dépôt** |
| **Conformité de cette absence** | Elle est **contractuellement voulue** — `08` §6, `12` §3, `QO-5`. Ce n'est pas un écart |
| **Reconstructibilité par événements** `[NON ÉTABLI]` | La reconstructibilité des écritures de verdict par les événements `call_service` est **postulée par la doctrine du dépôt** (`R-L2-1`). Elle **n'est pas établie au SHA audité** : aucune configuration d'événements n'existe, et le comportement effectif dépend d'un runtime hors de l'arbre |
| **Observation directe L5** | **Reste possible et pleinement légitime** — la doctrine la qualifie de « mode d'obtention », non de défaut. Elle n'exige aucun instrument du dépôt |
| **Ce qui manque réellement** `[FAIT]` | Le registre énumère cinq validations terrain **sans désigner de moyen de preuve ni qualifier de niveau**. **Aucun protocole formellement qualifié n'existe dans le domaine.** Ce qui n'est pas satisfait est le **§5 de la doctrine** — les dix exigences d'ouverture. Aucun défaut de couverture d'un instrument désigné n'est allégué : **aucun instrument n'est désigné** |
| **Preuve terrain** | `RT-01` à `RT-09` |
| **Effet opérateur** | aucun direct ; effet de gouvernance sur la clôture |
| **Couverture CI** | aucune — T-6 |
| **Sévérité proposée, non arbitrée** | élevée pour la clôture |
| **Confiance** | **très élevée** sur le régime de `recorder` et sur ses conséquences ; le volet reconstructibilité est explicitement **non tranché** |
| **Ce qui l'infirmerait** | Un protocole qualifié posé ailleurs dans le dépôt ; ou l'établissement, hors de l'arbre, de la rétention effective des événements |
| **Arbitrage** | **aucun** — question `QA-07` |

#### `LP-03` — Aucun contrôle CI ne confronte l'interface opérationnelle au backend

| Rubrique | Contenu |
|---|---|
| **Fait** `[FAIT]` | Établi par lecture **intégrale** d'`ASP-CI-7` — seul contrôle recevant les 463 fichiers Lovelace — et de `run()`. Voir T-1 et T-2 |
| **Conséquence** | `RC-01` et `RC-02` sont **invisibles à une CI verte** |
| **Preuve terrain** | **sans objet** |
| **Effet opérateur** | indirect — absence de filet mécanique |
| **Couverture CI** | par définition, aucune |
| **Sévérité proposée, non arbitrée** | élevée |
| **Confiance** | très élevée |
| **Ce qui l'infirmerait** | Un contrôle non identifié dans les parties du checker non lues — écarté par la lecture intégrale de `run()`, qui énumère les entrées de chacun des 42 contrôles |
| **Arbitrage** | **aucun** |

#### `LP-04` — Aucun contrôle ne confronte les décomptes de prose ni les en-têtes aux corps

| Rubrique | Contenu |
|---|---|
| **Fait** `[FAIT]` | `ASP-CI-5` ne lit que `03_profils_metier.md` (T-3) · `sans_commentaires_yaml()` retire les commentaires avant analyse, donc aucun en-tête n'est confronté à son corps (T-4) · DOC-CI-2 déclare un périmètre « `contrats/index.md` UNIQUEMENT » (T-5) |
| **Conséquence** | `DD-01` à `DD-08` sont **invisibles à une CI verte** |
| **Preuve terrain** | **sans objet** |
| **Effet opérateur** | indirect |
| **Couverture CI** | par définition, aucune |
| **Sévérité proposée, non arbitrée** | moyenne |
| **Confiance** | très élevée |
| **Ce qui l'infirmerait** | — |
| **Arbitrage** | **aucun** |

### 10.5 Faits soumis à arbitrage, sans qualification d'écart acquise — **2**

#### `FA-01` — Affordance de lancement permanente, arrêt sans écriture, canal journal présent

| Rubrique | Contenu |
|---|---|
| **Faits établis** `[FAIT]` | (a) L'affordance « Lancer la mission » est **toujours présente** — aucune `conditional`, aucun état désactivé. (b) L'étape 0a du moteur produit un `stop` **avant toute écriture** lorsque le verdict appartient à la classe O/O-R. (c) Aucune surface du panneau ne change : `sensor.aspirateur_motif_lisible` dérive du verdict, qui n'a pas muté. (d) **Le canal prévu par le contrat — journal et trace Home Assistant — est présent et fonctionnel** : `ASP-INV-91` le désigne, et le `stop` porte un motif littéral |
| **Pourquoi aucune divergence n'est déclarée** `[LECTURE]` | `ASP-INV-91` **désigne** le journal et la trace comme canal de `ASP-INV-50`. **La lettre du contrat est tenue.** L'absence de retour **dans l'interface** est établie ; **l'absence de trace ne l'est pas, et est contredite par la conception** |
| **Ce qui reste ouvert** | Ce canal est-il suffisant, au regard de `ASP-INV-50` (« un bouton inerte … est non conforme »), pour un opérateur qui ne consulte pas les traces ? Par ailleurs, « mission déjà ouverte » relève de la **catégorie B** de `commandabilite.md`, où la doctrine admet un **override manuel** ; le runtime n'offre ni override ni refus visible |
| **Preuve terrain** | **sans objet** pour les quatre faits |
| **Effet opérateur allégué** | Le geste est confirmé et ne produit aucun changement visible sur l'écran |
| **Couverture CI** | aucune |
| **Confiance** | **élevée** sur les quatre faits |
| **Ce qui le requalifierait** | Un arbitrage retenant que le canal journal ne satisfait pas `ASP-INV-50` — ou l'inverse |
| **Arbitrage** | **aucun** — question `QA-05` |

#### `FA-02` — Le registre ne porte aucune ligne pour les huit lots antérieurs

| Rubrique | Contenu |
|---|---|
| **Faits établis** `[FAIT]` | Le registre des chantiers ne contient **qu'une ligne aspirateur** — `C42`, section Actifs, « Ouvert, validation terrain due ». **Aucune ligne** pour les lots L1, M0, M1, N1, L2, U0, U1, U2, ni en Actifs, ni en Clos récents, dont la fenêtre est d'environ 90 jours alors que les lots L2, U0 et U2 datent de la fin août 2026. Les livraisons sont en revanche **tracées par leurs merges** (`#726` → `#751`) |
| **Deux lectures coexistent** `[LECTURE]` | (a) `redaction_changelog.md` §1 fait de la trace « le **commit de merge / la PR** … **et la ligne de clôture du registre** » : les PR existent, la ligne de clôture manque. (b) Si ces lots n'ont jamais été ouverts comme chantiers, aucune ligne n'était due — mais le registre cesse alors d'être « la source canonique de ce qui est réellement ouvert » pour un domaine porteur de réserves terrain non soldées |
| **Preuve terrain** | **sans objet** |
| **Effet opérateur** | aucun direct ; effet de gouvernance |
| **Couverture CI** | `check_registre_chantiers.py` vérifie les **liens**, non la complétude |
| **Confiance** | **élevée** sur le fait ; **moyenne** sur chacune des deux lectures |
| **Ce qui le requalifierait** | Un arbitrage retenant l'une des deux lectures |
| **Arbitrage** | **aucun** — question `QA-08` |

---

## 11. Risques et questions terrain — `RT-01` à `RT-09`

> Neuf entrées, sans trou ni doublon. **Aucune n'a été observée par cette contre-expertise.** Aucune ne conditionne l'existence des constats structurels `RC-01` et `RC-02`.

| ID | Question terrain | Ce que le dépôt en dit | Constat étayé | Sévérité proposée, non arbitrée |
|---|---|---|---|---|
| `RT-01` | L'effet réel d'une pression de remise à zéro : le compteur remonte-t-il ? | **« Prédit, non testé »** — assumé par le relevé d'attestation | `LP-02` | moyenne |
| `RT-02` | Réponse réelle de l'appareil aux **quatre** commandes de conduite, et aboutissement d'une chaîne de retour | « ni l'un ni l'autre jamais observés » — registre de couverture | `RC-02`, `LP-02` | élevée |
| `RT-03` | `×3` produit-il bien `repeat: 3` et trois passages ? | `ARB-4` — déduction protocolaire, acceptée explicitement | `LP-01` | faible |
| `RT-04` | Quelles sont les énumérations exactes des deux témoins d'erreur ? | `ARB-5` — valeurs `none` / `ok` **déclarées par l'opérateur**, non relevées | `LP-01` | faible |
| `RT-05` | Une mission depuis `charger_disconnected`, robot transporté, aboutit-elle ? | `ARB-1` — autorisé **sans preuve** | `LP-01` | moyenne |
| `RT-06` | Les fenêtres de **30 s** et **60 s** sont-elles suffisantes en régime réel ? | `ARB-3` — valeurs **déclarées**, « adossées à aucune mesure terrain » | `LP-01` | moyenne |
| `RT-07` | Sur un retour complet, quelle est la fenêtre réelle de désalignement du témoin de session ? | Trois durées **relatées** par `08` §3 et l'en-tête du moteur — 53 s, 25 s, 28,3 s — **non observées ici** | `RC-02` (b) | élevée |
| `RT-08` | Quel est le rendu réel de la section Conduite face à une mission lancée depuis l'application Roborock ? | Non observé ; la combinaison est satisfaite **par construction** | `RC-02` (a) | élevée |
| `RT-09` | Quel est l'état réel du témoin `binary_sensor.roborock_q7_max_serpilliere_fixee` lors d'un usage, et quel est le rendu observé des trois surfaces concernées ? | `off` au moment du relevé d'audit — **observation datée, non rejouable** | `RC-01` — **utile, non nécessaire** au constat structurel | moyenne |

---

## 12. Questions d'arbitrage — `QA-01` à `QA-08`

> Huit questions. **Aucune n'est tranchée ici.** Elles relèvent de l'opérateur et d'actes distincts de ce document.

| ID | Question | Constats concernés |
|---|---|---|
| `QA-01` | Laquelle des deux définitions de « mission ouverte » — `08` §1 native, ou `15` §2 par le verdict — l'interface doit-elle rendre, et sous quel libellé chacune ? | `CC-01`, `RC-02` |
| `QA-02` | **Bloquante.** Faut-il une **seconde exception nominative à `ASP-CI-11`** ouvrant la lecture du verdict au panneau opérationnel ? Le dossier de cadrage a posé la question et a écrit qu'il ne la tranchait pas. Sans elle, `RC-02` ne peut être corrigée — seulement déplacée | `RC-02` |
| `QA-03` | « Mission déjà ouverte » et « mission externe » relèvent-elles de la catégorie **A** ou **B** de `commandabilite.md` ? En **B**, faut-il un override manuel ou un masquage ? | `RC-02`, `FA-01` |
| `QA-04` | « Présenter comme lançable » vise-t-il l'affichage d'une **option de profil**, ou seulement le **geste de lancement** ? | `RC-01` |
| `QA-05` | Le canal journal et trace Home Assistant, désigné par `ASP-INV-91`, satisfait-il `ASP-INV-50` (« un bouton inerte … est non conforme ») pour un opérateur qui ne consulte pas les traces ? | `FA-01`, `RC-02` |
| `QA-06` | Faut-il amender `01` §4 après l'entrée en vigueur du chapitre `14` ? | `CC-02` |
| `QA-07` | Les réserves du domaine doivent-elles être qualifiées L1–L5, avec propriétaire, horizon, date de réévaluation et critère de retrait, **avant** toute clôture, conformément à `R-QUALIF-1` et `R-VERROU-1` ? | `LP-01`, `LP-02` |
| `QA-08` | Les huit lots antérieurs doivent-ils recevoir une ligne au registre des chantiers, ou la trace par merge suffit-elle ? | `FA-02` |

---

## 13. Vérifications sans écart — **12**

| # | Vérification | Méthode |
|---|---|---|
| 1 | Historisation conforme à `08` §6 et `12` §3 — aucune entité au `recorder`, comme le contrat l'exige | balayage de `recorder.yaml` et `logbook.yaml` |
| 2 | `ASP-INV-4` préservé — l'exclusion d'intrusion repose sur `vacuum.roborock_q7_max` en `cleaning` / `returning`, **jamais** sur le témoin de session | lecture du bloc décisif de l'automation alarme |
| 3 | IDs d'automation et préfixe de domaine `1028` | `check_automation_ids`, `check_automation_prefix_domain` |
| 4 | **Absence de clé `initial:`** sur les 17 helpers | vérification **directe**, plus `check_initial_key` |
| 5 | Includes de configuration résolus | `check_configuration_includes` — 22 includes |
| 6 | Navigation Lovelace et existence réelle des clés de dashboard | `check_lovelace_navigation`, `ASP-CI-42` |
| 7 | Palette et hiérarchie de couleurs | 4 checkers UI |
| 8 | Absence de templating inline en Lovelace | `check_lovelace_no_inline_templating` |
| 9 | En-têtes de sections Lovelace | `check_lovelace_section_headers` |
| 10 | Gabarits button-card | `check_19_button_card_templates` |
| 11 | **Empreintes SHA-256 du relevé d'attestation d'entretien recalculées et identiques** aux valeurs déclarées | `sha256sum` |
| 12 | Registre de couverture CI cohérent — 88 checkers, 7 workflows | `check_ci_coverage_registry` |

---

## 14. Réponses aux cinq dimensions

| # | Dimension | Réponse | Fondement |
|---|---|---|---|
| **1** | **Intégration fonctionnelle** | **ÉTABLIE AVEC RÉSERVES** | La chaîne complète existe et se tient — 17 helpers, composition atomique, moteur à écrivain unique, conduite, supervision, deux projections persistantes, canal mobile, trois écrans. Les modes d'échec identifiés par l'audit factuel — troncature silencieuse, écrasement du profil, publication non fraîche, conclusion sur un fourre-tout de classe N, course entre écrivains — sont tous traités. **Réserves :** `RC-01`, `RC-02`. **Portée bornée** au périmètre recensé et lu intégralement (§4.2) |
| **2** | **Conformité contractuelle** | **ÉTABLIE AVEC RÉSERVES** | Le runtime respecte sans exception démontrée les invariants structurants : `ASP-IMC-1`, `ASP-INV-31` à `36`, la partition R/A/E/N, la totalité du modèle d'états, la disjonction des trois écrivains, l'allowlist nominative de la primitive irréversible, les deux constantes temporelles. **Réserves :** `RC-01`, `RC-02`, `CC-01`, `CC-02` |
| **3** | **Cohérence documentaire** | **NON ÉTABLIE** | Neuf divergences certaines, dont **une projetée dans l'interface opérateur** (`DD-01`) et **une violation directe de la doctrine des en-têtes**, normative et faisant de l'en-tête l'autorité locale (`DD-02`). Quatre chapitres du contrat, deux index, le registre de couverture, trois fichiers de cadrage et six en-têtes runtime portent des affirmations fausses au même SHA. **Aucune n'est couverte par la CI** |
| **4** | **Commandabilité opérateur** | **NON ÉTABLIE** | Le critère est : « opérable **sans geste proposé mais inexécutable ou silencieusement ignoré** ». Pour le déclarer **établi**, il faudrait que les prédicats d'affichage et d'acceptation coïncident. Il est **statiquement démontré** qu'ils ne coïncident pas — `RC-02` — et que la **règle conditionnelle exigée par `ASP-INV-13` est absente** — `RC-01`. **Le verdict ne repose sur aucune occurrence : il repose sur l'absence et la divergence des règles, toutes deux établies par lecture.** `FA-01` est **exclu** de ce fondement : la lettre du contrat y est tenue |
| **5** | **Clôture probatoire** | **NON ÉTABLIE** | Le registre porte le domaine « Ouvert, validation terrain due ». Le balayage sur dix motifs et le périmètre complet établit **zéro qualification de solvabilité** — par `R-QUALIF-1`, toutes les réserves sont réputées **verrous actifs** (`LP-01`). Le régime d'allowlist, vérifié, établit qu'**aucun historique d'état ni d'attribut n'existe** pour les entités sur lesquelles portent plusieurs des preuves attendues, et **aucun protocole formellement qualifié n'existe dans le domaine** (`LP-02`). Enfin, **une CI verte à 88/88 ne couvre aucun des écarts de la dimension 4** (`LP-03`) |

---

## 15. Conclusion générale

Le domaine `aspirateur` est, au SHA `31afb9f`, un sous-système dont le **backend** est construit avec une rigueur peu commune : refuser plutôt que présumer, prouver positivement plutôt que par négation, nommer l'absence de preuve plutôt que la combler. Cette contre-expertise n'a pas trouvé de faille de sûreté dans la chaîne de décision et d'émission ; elle a trouvé un **décalage entre ce que le backend décide et ce que l'interface propose**, une **prose désynchronisée de son propre runtime**, et une **absence complète de qualification probatoire**.

### 15.1 Ce qui est prouvé

L'intégralité du backend : séquence normative à treize étapes, ordre contractuel, double confirmation cartographique avec exigence de **fraîcheur**, garde d'abstention, revérification tardive intégrale, émission unique enveloppée, partition d'états totale, vocabulaire fermé à trente-quatre valeurs à trois écrivains disjoints, sérialisation par le verdict sans helper, réconciliation totale au redémarrage, allowlist nominative de la seule primitive irréversible, postcondition d'entretien exprimée comme **transition**. Côté écarts : **2** divergences de prédicat, **2** contradictions contractuelles, **9** divergences documentaires, **4** lacunes de preuve, **2** faits soumis à arbitrage. Côté outillage : 42 contrôles logiques, 670 cas de selftest, 88 checkers sur 88, 6 gates documentaires — tous exécutés, tous verts.

### 15.2 Ce qui est seulement proposé

**Huit surfaces d'action** dont le prédicat d'affichage ne coïncide pas avec le prédicat d'acceptation du backend. Ce sont des **propositions d'interface dont la condition d'aboutissement n'est pas celle qui les fait paraître** — ni des capacités démontrées, ni des défaillances observées.

### 15.3 Ce qui nécessite une observation terrain

Les neuf questions `RT-01` à `RT-09`. Deux sont décisives pour la commandabilité : le rendu réel face à une mission externe, et la fenêtre réelle de désalignement du témoin de session. **Les trois reproductions de ce désalignement — 53 s, 25 s, 28,3 s — sont relatées par le dépôt et n'ont pas été observées par cette contre-expertise** ; elles étayent les constats, elles ne les fondent pas. **Aucune non-conformité fonctionnelle n'est déclarée acquise sur une absence.**

### 15.4 Ce qui nécessite un arbitrage humain

Les huit questions `QA-01` à `QA-08`. **`QA-02` demeure bloquante** : tant que `ASP-CI-11` interdit mécaniquement à l'interface de lire le verdict, `RC-02` ne peut être corrigée — seulement déplacée. Le dossier de cadrage ratifié a posé cette question et a écrit qu'il ne la tranchait pas.

### 15.5 Ce que les checkers ne couvrent pas

Sept trous, dont trois établis par lecture intégrale du code de contrôle concerné : **aucun contrôle ne confronte l'interface opérationnelle au backend** ; **aucun ne confronte un en-tête à son corps**, alors que la doctrine des en-têtes est normative et fait de l'en-tête l'autorité locale ; **la doctrine de solvabilité probatoire n'a, de son propre aveu, aucun garde-fou CI** — et le domaine n'a produit aucune qualification, sur aucune de ses réserves.

### 15.6 Formulation finale

> Le domaine `aspirateur` est **fonctionnellement intégré et contractuellement conforme dans son backend**, **documentairement incohérent**, **incomplètement commandable depuis son interface** — au sens précis où les règles d'affichage exigées par le contrat sont absentes ou divergent des gardes d'acceptation, ce qui est **statiquement démontré**, tandis que les occurrences ne sont **pas observées** — et **probatoirement non clos**, **faute de moyen de preuve formellement qualifié et documenté pour les validations dues**.
>
> Une CI verte à 88/88 atteste la conformité de ce qu'elle balaie ; elle ne balaie ni les conditions d'affichage du panneau opérationnel, ni les en-têtes de fichiers, ni la solvabilité des réserves.

---

## 16. Limites et absence d'arbitrage

### 16.1 Limites assumées

1. **Aucune exhaustivité globale du domaine n'est revendiquée.** L'exhaustivité est établie sur les **contrats** et sur le **runtime fonctionnel recensé** ; elle ne l'est pas sur le checker, l'audit de faisabilité, le dossier de cadrage, ni sur 7 des 11 gabarits transverses consommés par l'interface (§4.2).
2. **Aucune observation d'instance n'a été réalisée.** Les neuf questions terrain restent entières. Aucune reproduction relatée par un document du dépôt n'est présentée comme une observation propre à cette contre-expertise.
3. **Les comportements dynamiques de Home Assistant** — ordre d'exécution, instant de recalcul d'un template, rétention effective des événements — ne sont pas tranchables depuis le seul dépôt. Là où une conclusion en dépendrait, elle est classée `[NON ÉTABLI]`.
4. **Le checker n'a pas été audité ligne à ligne.** Sa couverture a été établie par la lecture intégrale de `run()`, qui énumère les entrées de chacun des 42 contrôles, et par la lecture intégrale du seul contrôle recevant l'ensemble des fichiers Lovelace.

### 16.2 Absence d'arbitrage

**Aucun constat de ce document n'est arbitré.** Les sévérités proposées sont des **propositions**, non des qualifications officielles. Les questions `QA-01` à `QA-08` sont **ouvertes**. Aucune requalification, aucune clôture, aucune ouverture de chantier, aucun correctif n'est prononcé ni proposé sous forme exécutable.

**Ce document ne modifie ni ne contredit aucun contrat, aucun runtime, aucun checker, aucun registre, aucun état de clôture.** En cas de divergence entre ce document et un contrat, **le contrat fait foi**.

---

*Contre-expertise indépendante en lecture seule, consignée comme acte d'analyse archivé. Aucun contrat, runtime, checker, registre de chantiers, changelog ou arbitrage n'a été créé ni modifié pendant l'analyse. Document **non normatif, non opposable et NON ARBITRÉ** : il consigne des constats et des questions, il ne décide de rien.*
