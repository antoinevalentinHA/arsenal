# Audit documentaire — dépôt `antoinevalentinHA/arsenal`

> **Périmètre.** Branche `main`, commit `19a50f1` (2026-06-06). Audit **en lecture seule**, aucun patch, aucun renommage, aucun commit. Vérification du dépôt réel (584 `.md`, dont 558 sous `00_documentation_arsenal/`, 958 liens internes relatifs), pas seulement des index.
> **Posture.** Audit délibérément critique : recherche active de ce qui peut être simplifié, clarifié, rationalisé. Les forces sont mentionnées mais ne sont pas l'objet.

---

# Résumé exécutif

**État général.** La documentation Arsenal est, au sens strict de la navigation, **saine et solide** : un seul lien markdown défectueux sur 958, et il est inerte (dans un bloc de code). Le corpus est entièrement interne (aucun lien `http` susceptible de pourrir), structuré en 9 zones de premier rang cohérentes avec ce que les README annoncent, et il dispose d'un mécanisme rare et précieux : un **registre vivant d'anomalies** (`audits/02_constats/transverses/registre_anomalies_transverses.md`) dont les clôtures déclarées « 2026-06-05 » ont été **vérifiées réelles dans l'arbre** (renommages effectués, `garage_implementation.md` supprimé, 0 référence `resilience_electrique` résiduelle, typo `expostion` corrigée). Le dépôt sait se réparer.

**Le vrai problème n'est pas le contenu — ce sont les méta-documents.** Les contrats et l'architecture sont à jour ; ce qui **dérive systématiquement**, ce sont les **index, les notes de statut et les sections « à venir »**. Quand le corpus est corrigé, l'advertisement de la correction ne suit pas. On observe trois symptômes du même mal : (1) l'index canonique du changelog est **8 versions en retard**, (2) `navigation/README.md` sous-déclare sa propre couche de **18 hubs sur 21**, (3) `contrats/index.md` entretient une note d'anomalie pour un défaut **déjà clos**. Ces écarts ne cassent rien techniquement, mais ils érodent la confiance dans la couche d'orientation — précisément la couche censée inspirer confiance.

**Forces.**
- Liens quasi parfaits : 1 lien cassé sur 958, inerte. Aucune référence morte active dans un contrat normatif (les anciennes ont été résorbées).
- Registre d'anomalies exact et auto-réparateur — gouvernance documentaire d'un niveau peu commun.
- Doctrine claire (Perception/Décision/Exécution, contrat-avant-YAML), README racine et README doc excellents, table « où chercher quoi », charte de hub R1–R8 rigoureuse.
- Hubs de navigation (21/21) effectivement maillés depuis `carte_domaines.md`.

**Faiblesses.**
- **Dérive des index** : changelog (retard de 8 versions, 0 lien sortant), `contrats/index.md` (comptes faux ×4, colonne navigation fausse pour chauffage, anomalie #1 périmée), `audits/index.md` (3 sous-dossiers de rapports non référencés, section « Constats » auto-contradictoire).
- **Index de famille incohérents** : 4 conventions de nommage coexistent (`README.md`, `index.md`, `00_index.md`, `..._index.md`) ; 10 sous-domaines de contrats sur 14 n'ont **aucune** page d'atterrissage (dont `ecs/` 28 fichiers, `meteo/` 16, `alarme/` 15).
- **Notes de statut périmées** : `navigation/README.md` et `navigation/carte_domaines.md` se décrivent dans un état antérieur à leur contenu réel ; sections « à venir » obsolètes éparses.
- **Taux d'orphelins élevé** : 225/558 (40 %) sans lien entrant. Majoritairement atteignables par navigation de dossier, mais lourd pour un corpus qui se réclame de l'hypertexte (il possède même un `audit_maturite_hypertexte_documentation.md`).

**Risques.**
- **Risque de confiance** (principal) : un lecteur qui consulte l'index du changelog croit que v15.8.2 est la dernière version (8 manquent) ; un lecteur qui lit `navigation/README.md` croit que 3 hubs existent (21 existent) ; un lecteur qui lit `contrats/index.md` est invité à se méfier d'un README qui est en fait correct. La couche d'orientation ment par retard, pas par erreur.
- **Risque de double source de vérité** : deux registres d'anomalies non synchronisés (`contrats/index.md` §Anomalies vs le registre central) ; double hébergement `bouclage` toujours non arbitré.
- **Risque de fragilité éditoriale** : aucune CI ne vérifie la fraîcheur des index/comptes/sections « à venir » ; ces dérives sont invisibles jusqu'à lecture humaine.

---

# Anomalies critiques

*(Problèmes pouvant induire une erreur de compréhension ou de navigation.)*

### C1 — Index du changelog en retard de 8 versions et sans liens

`changelog/index.md` est l'« index chronologique canonique » désigné comme porte d'entrée par le README de la doc et le README racine. Or :

- Son récit **s'arrête à `v15.8.2`**. Le dossier `changelog/changelogs/v15/` contient **`v15_8_3`, `v15_8_4`, `v15_8_5`, `v15_8_6`, `v15_8_7`, `v15_8_8`, `v15_8_9`, `v15_9_0`** — soit **8 versions postérieures non indexées**. Un lecteur conclut à tort que v15.8.2 est l'état courant (alors que le dépôt vit en v15.9).
- Cet index **ne contient aucun lien hypertexte** (`0` lien markdown) vers les ~87 fichiers de version qu'il narre. Le récit et les artefacts sont **disjoints** : on ne peut pas naviguer de la synthèse vers le fichier détaillé.

**Impact.** L'artefact chronologique le plus consulté est non fiable pour « quelle est la dernière version » et non navigable vers le détail.

### C2 — Deux registres d'anomalies désynchronisés ; note d'anomalie périmée dans `contrats/index.md`

`contrats/index.md` se termine par une section « Anomalies signalées (non corrigées) » dont l'**anomalie #1** affirme que `contrats/README.md` est obsolète parce qu'il « référence `chauffage.md`, `ecs.md` et `ventilation.md` comme fichiers plats ».

- **Vérifié faux.** Le README actuel ne mentionne aucun de ces trois fichiers ; il décrit explicitement « 14 domaines organisés en sous-dossiers ». Le registre central confirme la correction (§2.5, **CLOS 2026-06-05**).
- Donc `contrats/index.md` **invite le lecteur à se méfier d'un README désormais correct**, et fait coexister un second registre d'anomalies en contradiction de statut avec le registre central.

**Impact.** Information trompeuse dans un index normatif ; double source de vérité sur l'état des anomalies.

---

# Anomalies majeures

*(Problèmes réels, non bloquants.)*

### M1 — `navigation/README.md` sous-déclare la couche de 18 hubs

Le README de la couche navigation (son autorité locale) écrit :
> « `domaines/` — hubs de domaine […]. **Produits à ce jour : `chauffage`, `vacances`, `alarme` ; les autres suivront.** »
> « `pivots/` — pages pivot transverses **(à venir)**. »

**Réalité :** `navigation/domaines/` contient **21 hubs** (tous produits) et `navigation/pivots/` contient `registre_ch.md`. Le README parent (`00_documentation_arsenal/README.md`) annonce d'ailleurs correctement « 21 hubs Tier-1 » → **contradiction interne** entre le README parent (juste) et le README de la couche (périmé).

### M2 — `navigation/carte_domaines.md` : note de statut contredite par son contenu

Ligne 7 : « **Statut.** v1. **Sans liens hypertexte à ce stade** (les chemins sont donnés en texte ; le maillage sera ajouté à une passe ultérieure). »
**Réalité :** le fichier contient **21 liens hypertexte actifs** `](domaines/*.md)`. Le maillage a été fait ; la note de statut décrit un état révolu. (C'est précisément ce maillage qui rend les 21 hubs non-orphelins — donc l'incohérence porte sur la note, pas sur la fonction.)

### M3 — `contrats/index.md` : comptes faux et colonne navigation erronée

| Domaine | Compte index | Compte réel | Écart |
|---|---:|---:|---|
| `chauffage/` | 50 | 52 | −2 |
| `climatisation/` | 38 | 39 | −1 |
| `eclairage/` | 6 | 5 | +1 (suppression `garage_implementation.md` non répercutée) |
| `meteo/` | 15 | 16 | −1 |

De plus, la colonne « Navigation » marque **`chauffage/` à « — »** (pas de page d'entrée) alors que **`contrats/chauffage/README.md` existe** et est bien structuré. L'index décrit donc le domaine le plus volumineux comme dépourvu de navigation, à tort.

### M4 — Couverture d'index incohérente entre sous-domaines de contrats

Sur 14 sous-domaines, **seuls 4** disposent d'une page d'atterrissage : `aeration_blocage_chauffage/` (README), `boiler/` (README), `chauffage/` (README), `climatisation/` (00_index). **10 n'en ont aucune**, dont des domaines substantiels :

- `ecs/` — **28** fichiers, aucun index
- `meteo/` — **16** fichiers, aucun index
- `alarme/` — **15** fichiers, aucun index
- `pannes/` (9), `eclairage/` (5), `imprimerie/` (3), `ouvertures/` (3), `deshumidificateur/` (2), `sante/` (2), `publication/` (1) — aucun index

`contrats/index.md` lie pourtant tous ces dossiers de manière uniforme ; pour les 10 sans index, le lien aboutit à la **liste de fichiers brute de GitHub**, sans orientation.

### M5 — `audits/index.md` omet trois sous-dossiers entiers de rapports

L'index d'audit couvre les domaines (bouclage, chauffage, ECS, clim, météo, température, vacances, voiture) mais **ne référence pas** :

- `01_rapports/documentation/` — **8 fichiers**, dont `audit_structure_documentaire.md`, `audit_navigation_documentation_arsenal.md`, `audit_maturite_hypertexte_documentation.md`, `cartographie_chaines_documentaires_arsenal.md`…
- `01_rapports/architecture/` — 2 fichiers (`audit_couverture_maturite_gouvernance_consolide.md`, `plan_action_gouvernance_revise.md`)
- `01_rapports/perception_externe/` — 1 fichier
- `04_chantiers/transverses/etat_avancement_chantier_navigation_documentaire_contrats.md`

Soit **13 documents d'audit** non atteignables depuis la porte d'entrée des audits — dont, ironie, les audits portant sur la documentation elle-même.

### M6 — `audits/index.md` : section « Constats » auto-contradictoire

La section `## Constats` affiche « *(emplacement réservé — aucun document à ce jour)* ». Or un document de constats existe bien — `02_constats/transverses/registre_anomalies_transverses.md` — et **l'index le lie lui-même**, mais plus bas, sous une rubrique distincte « ## Transverse ». La prose « aucun document » est donc fausse au sein du fichier qui la dément.

---

# Anomalies mineures

*(Améliorations possibles.)*

- **m1 — Quatre conventions de nommage d'index.** `README.md` (×11), `index.md` (×5), `00_index.md` (×3), `13_capteurs_index.md` (×1). Pas de nom canonique. La famille UI utilise `README.md` comme porte d'entrée quand les autres familles utilisent `index.md` (cf. table du `navigation/README.md`).
- **m2 — `changelog/changelogs/v10/v10 final.md` : espace dans le nom de fichier.** Rompt la convention par ailleurs stricte (`v10.md`, `v10_3.md`, …). Fragile pour l'outillage et les liens.
- **m3 — Sections « à venir » périmées.**
  - `architecture/presence/presence.md:168` : « contrat Alarme (à venir) » — or `contrats/alarme/` existe (15 fichiers, dont `00_gouvernance_alarme.md`).
  - `navigation/domaines/ui_lovelace.md:58` : note que `registre_ch` cite ce hub comme « à venir » — le hub existe désormais.
  - (Plusieurs autres « à venir » sont légitimes car réellement prospectifs : `outils_externes/.../quarantine_purger`, doc β UI… — non listés ici.)
- **m4 — `evolutions_futures/` quasi vide.** Le « sas » prospectif, zone de premier rang, ne contient plus qu'**un** fichier (`lovelace_arborescence.md`), les autres fiches ayant migré vers `contrats/`. Une zone Tier-1 pour un document — sur-structuration au regard du contenu courant.
- **m5 — Casse mixte des codes de chantier.** `CHANGELOG_CH1..6.md`, `CHANGELOG_CH-LL-CI-1.md` (majuscules) cohabitent avec le reste en `snake_case` minuscule. Acceptable comme « codes », mais hétérogène.

---

# Documents orphelins

*(Sans aucun lien markdown entrant. 225/558 = 40 %. Classés par nature ; « atteignable dossier » = visible par navigation GitHub mais non maillé.)*

**Justification du chiffre.** Un fichier est compté orphelin s'il ne reçoit aucun lien `[..](..)` d'un autre `.md` (les liens vers le dossier parent sont rabattus sur son index s'il existe). La majorité des orphelins ne sont pas « perdus » : ils sont atteignables en parcourant le dossier. Mais ils sont **hors du graphe hypertexte**, ce qui contredit la doctrine de navigabilité.

| Catégorie | Nb | Cause | Atteignable dossier ? |
|---|---:|---|---|
| `changelog/changelogs/v*` (versions) | 87 | `changelog/index.md` ne lie rien (cf. C1) | Oui (dossier) |
| `changelog/chantiers/climatisation/CHANGELOG_CH*` | 6 | non liés ; de surcroît mal classés (cf. registre §3.2) | Oui |
| `contrats/aeration_blocage_chauffage/m*/…` | 23 | feuilles de machine d'état ; README lie les modules, pas les feuilles | Partiel |
| `contrats/ecs/*` | ~20 | **aucun index `ecs/`** (M4) | Oui (dossier brut) |
| `contrats/climatisation/capteurs/**` | ~18 | `00_index.md` ne descend pas aux feuilles `10_*/20_*/90_*` | Partiel |
| `contrats/chauffage/*` (amendements, feuilles capteurs) | ~9 | README lie les points d'entrée, pas les amendements | Partiel |
| `ui/socle_ui/*`, `ui/couleurs/*` | 19 | feuilles non liées par les `00_index.md` UI | Partiel |
| `outils_externes/**` (boiler_pi, nas_arsenal, nas_imprimerie) | 14 | sous-pages non liées par les README/hubs | Oui (dossier) |
| `audits/01_rapports/{documentation,architecture,perception_externe}/*` | 13 | absents de `audits/index.md` (M5) | Non (réellement isolés) |
| `architecture/{01_recorder,02_etiquettes}/*` | 6 | dossiers liés mais **sans index** ; feuilles non maillées | Partiel |
| `schemas_ascii/*` | 3 | aucun index `schemas_ascii/` ; non liés | Non |
| `contrats/pannes/{internet,secteur}/*`, `contrats/eclairage/recalage_nocturne_garage.md`, `contrats/publication/securite_publication_git.md`, autres feuilles | ~7 | feuilles non maillées | Partiel |

**Orphelins les plus préoccupants** (réellement isolés, valeur élevée) :
- `audits/01_rapports/documentation/` (8) — les audits documentaires eux-mêmes.
- `schemas_ascii/` (3) — `pipeline_aeration.md`, `pipeline_nas_ha.md`, `regulation_thermique.md` : diagrammes utiles, non reliés.
- `architecture/01_recorder/{contrat,fiche_decision}.md` et `architecture/02_etiquettes/{automatisations,capteurs,helpers,scripts}.md` (6) — dossiers liés sans index, feuilles invisibles au graphe.

---

# Liens cassés

*(Liste exhaustive. 1 occurrence sur 958 liens internes.)*

### L1 — `audits/03_plans_action/transverses/plan_action_anomalies_p1.md`

- **Ligne 50**, dans un **bloc de code** (prescription de modification destinée à `audits/index.md`) :
  `[registre_anomalies_transverses.md](registre_anomalies_transverses.md)` — chemin relatif faux (le registre est sous `02_constats/transverses/`, pas à la racine `audits/`).
- **Ligne 38**, bloc de code : chemin annoncé `00_documentation_arsenal/audits/registre_anomalies_transverses.md` — **faux** (réel : `…/audits/02_constats/transverses/…`).

**Nature exacte (honnêteté requise).** Ce n'est **pas** un lien de navigation cassé : il est dans un bloc de code, et la prescription a été correctement appliquée dans `audits/index.md` (qui lie le registre via le bon chemin `02_constats/transverses/…`). C'est donc un **chemin obsolète/incorrect figé dans un document de plan** — défaut éditorial, non cassant. Ironie notable : il subsiste dans le document même qui corrige les références mortes.

**Aucun autre lien markdown cassé.** Toutes les mentions de documents supprimés (`AUDIT_CHAINE_MQTT_ACK_ECS`, `CONTRAT_BOILER`, `guard_expostion`, `garage_implementation`, `en_cours.md`, `backup_zigbee`, `moteur_cli`…) sont **textuelles** (récit de changelog, registre, plan) et **ne sont pas des liens actifs** — vérifié exhaustivement.

---

# Incohérences de gouvernance documentaire

*(Liste exhaustive des écarts entre organisation réelle et organisation décrite, et entre artefacts de gouvernance.)*

1. **Double registre d'anomalies désynchronisé** (cf. C2) : `contrats/index.md` §Anomalies vs `audits/02_constats/transverses/registre_anomalies_transverses.md`. Le registre central marque §2.5 CLOS ; l'index contrats le maintient ouvert.
2. **Changelog : récit ≠ artefacts** (cf. C1) : index 8 versions en retard, 0 lien vers les fichiers narrés.
3. **`navigation/README.md` ≠ contenu de `navigation/`** (cf. M1) : 3 hubs déclarés vs 21 réels ; pivots « à venir » vs présents.
4. **`carte_domaines.md` statut ≠ contenu** (cf. M2) : « sans liens » vs 21 liens.
5. **`contrats/index.md` comptes & colonne ≠ arbre** (cf. M3).
6. **`audits/index.md` couverture ≠ arbre** (cf. M5) et **prose Constats ≠ propre contenu** (cf. M6).
7. **Conventions d'index non unifiées** (cf. m1) : 4 schémas de nommage ; entrée UI en `README.md`, autres en `index.md`.
8. **Asymétrie d'atterrissage des sous-domaines de contrats** (cf. M4) : 4/14 dotés, 10/14 nus.
9. **Sections « à venir » non purgées** (cf. m3) : `presence.md` « contrat Alarme à venir » alors qu'il existe ; `ui_lovelace.md` self-référence « à venir ».
10. **Double hébergement `bouclage`** : `contrats/bouclage.md` (racine, 25 Ko) et `contrats/ecs/04_bouclage_ecs_sous_systeme.md` (1,9 Ko). Connu (registre §2.3, P2 ; contrats/index anomalie #2), **toujours non arbitré** — source de vérité ambiguë.
11. **Chantiers `CH-x` climatisation hébergeant du chauffage** : `changelog/chantiers/climatisation/CHANGELOG_CH1..6.md` documentés comme appartenant au chauffage (registre §3.2). Misclassement connu, non résolu.

> *Items connus et explicitement acceptés par le projet (non comptés comme écarts à corriger) : double titre README boiler (redirect intentionnel, registre §2.2) ; hébergement de `capteurs_meteo.md`, `axe_temperature.md`, `interface_ha_boiler_bridge.md` (registre §4, arbitrés). Mentionnés pour exhaustivité.*

---

# Chantiers documentaires recommandés

*(Classés par rapport effort / valeur. Recommandations — aucun patch produit, conformément à la consigne.)*

### Effort très faible / Valeur très élevée — « rattrapage des index »

1. **Régénérer la queue de `changelog/index.md`** : ajouter les entrées v15.8.3 → v15.9.0 (8 versions). Tarir la source de désinformation principale. *(C1)*
2. **Corriger `contrats/index.md`** : supprimer l'anomalie #1 (périmée), recaler les 4 comptes (chauffage 52, clim 39, eclairage 5, meteo 16), passer la colonne navigation de `chauffage/` à « README ✅ ». *(C2, M3)*
3. **Mettre à jour `navigation/README.md`** : « 21 hubs produits », pivots « présents (registre_ch) ». *(M1)*
4. **Corriger la note de statut de `carte_domaines.md`** : retirer « sans liens hypertexte à ce stade ». *(M2)*
5. **Réparer `audits/index.md`** : reformuler « Constats » (le registre y est) et ajouter les sections `documentation/`, `architecture/`, `perception_externe/` des rapports orphelins. *(M5, M6)*
6. **Corriger les deux chemins du registre dans `plan_action_anomalies_p1.md`** (lignes 38 et 50). *(L1)*
7. **Purger les « à venir » obsolètes** : `presence.md` (contrat Alarme existe), `ui_lovelace.md`. *(m3)*

### Effort faible / Valeur élevée

8. **Lier `changelog/index.md` aux fichiers de version** (au minimum un lien par entrée, ou un index par dossier `vXX/`). Reconnecte 87 orphelins au graphe. *(C1)*
9. **Doter d'un index les gros sous-domaines de contrats sans atterrissage** — prioriser `ecs/` (28), `meteo/` (16), `alarme/` (15), `pannes/` (9). *(M4, orphelins)*
10. **Renommer `v10 final.md`** (espace → underscore). *(m2)*

### Effort moyen / Valeur structurante

11. **Unifier la convention de nommage des index** (choisir `index.md` **ou** `README.md`, s'y tenir, traiter `00_index.md` et `13_capteurs_index.md`). *(m1)*
12. **Index de feuilles pour les zones à forte profondeur** non maillées : `ui/socle_ui/`, `ui/couleurs/`, `contrats/climatisation/capteurs/**`, `architecture/01_recorder` & `02_etiquettes`, `schemas_ascii/`. Réduit le taux d'orphelins là où il fait le plus mal.

### Effort moyen / Valeur de fond (décisions, pas éditorial)

13. **Arbitrer le double hébergement `bouclage`** (P2 ouvert depuis longtemps) : une seule source de vérité. *(gouvernance #10)*
14. **Industrialiser la non-régression des méta-documents** : un linter CI qui vérifie (a) que tout fichier `vXX_*` est cité dans `changelog/index.md`, (b) que les comptes des index correspondent au dépôt, (c) qu'aucune section « à venir » ne pointe un objet désormais présent. C'est le **chantier à plus haut levier** : il transforme les corrections ponctuelles ci-dessus en invariant permanent et tarit la classe entière « index qui dérive ».

---

# Verdict final

**Qualité structurelle — 9/10.** Arborescence claire, 9 zones cohérentes avec leur description, doctrine explicite et appliquée, séparation contrat/architecture/audit/changelog respectée. Les seuls défauts structurels sont le `evolutions_futures/` quasi vide (sur-structuré) et l'asymétrie d'atterrissage des sous-domaines de contrats.

**Qualité de navigation — 7/10.** Le maillage de premier niveau est excellent (1 lien cassé inerte sur 958, 21 hubs maillés, table « où chercher quoi »). Mais 40 % du corpus est hors graphe hypertexte, l'index du changelog ne lie rien, et 13 audits sont injoignables depuis leur porte d'entrée. La navigation est bonne tant qu'on reste dans les hubs ; elle se dégrade dès qu'on cherche une feuille.

**Cohérence documentaire — 6/10.** C'est le point faible. Le contenu est cohérent ; les **méta-documents dérivent**. Index du changelog (−8 versions), README navigation (−18 hubs), `contrats/index.md` (anomalie périmée + comptes faux + colonne fausse), `audits/index.md` (couverture partielle + prose auto-contradictoire), double registre désynchronisé. Aucun de ces écarts n'est grave isolément ; leur **accumulation** trahit l'absence de contrôle de fraîcheur des index.

**Maintenabilité — 8/10.** Très bonne, et c'est ce qui sauve le reste : le registre d'anomalies vivant **fonctionne réellement** (clôtures vérifiées dans l'arbre), la discipline un-fichier-par-patch et la traçabilité changelog sont là. Le dépôt corrige ses contrats ; il lui manque seulement d'étendre cette même discipline à ses index et notes de statut.

### Note globale — **7,5 / 10**

Une documentation **mature, honnête et auto-réparatrice sur le fond**, pénalisée par une **dette de fraîcheur concentrée dans la couche d'orientation**. Le paradoxe est net : le système qui maintient un registre d'anomalies exemplaire laisse ses propres index et notes « à venir » prendre du retard. La bonne nouvelle est que **tout ce qui pèse sur la note est éditorial et à coût quasi nul** (chantiers 1 à 7), et qu'un seul chantier de fond (n°14, linter de fraîcheur des méta-documents) supprimerait la cause racine plutôt que les symptômes. Corrigés, ces points portent l'ensemble à un niveau 9/10 sans toucher au contenu.

---

*Audit réalisé en lecture seule sur `main` @ `19a50f1` (2026-06-06). Aucun fichier du dépôt modifié, renommé ou déplacé.*
