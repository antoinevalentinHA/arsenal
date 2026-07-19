# Chantier TRANSVERSE (C31) — Doctrine de solvabilité probatoire des chantiers Arsenal

| Champ | Valeur |
|---|---|
| **Chantier** | Poser une doctrine transverse de **solvabilité probatoire** : avant qu'une preuve terrain devienne condition de clôture, vérifier qu'elle est **productible** par le runtime et **conservable** par l'installation. |
| **Domaine** | Transverse — gouvernance des chantiers, administration de la preuve. |
| **Statut** | **Ouvert — Lots 1 et 2 livrés (2026-07-19).** Doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md) publiée (Lot 1), puis raccords réalisés chez leurs propriétaires et **correction factuelle du §7** (Lot 2). **Lot 3 non engagé.** C31 **reste non clôturable** (§9). |
| **Priorité** | **P1** — non pour un risque technique immédiat, mais parce que des chantiers restent ouverts en attendant des preuves que l'installation ne peut ni produire, ni conserver, ni qualifier correctement. |
| **Ouvert le** | 2026-07-19. |
| **Prochain jalon** | **Lot 3 — application démonstrative** de la doctrine à des cas réels (C29, C4, C27). |
| **Registre** | Chantier **C31** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |

> **⚠️ Portée — mise à jour du 2026-07-19 (Lot 1).** L'échelle L1–L5, les trois verdicts, la
> qualification des réserves et la règle sur les verrous **sont désormais opposables** : elles sont
> portées par [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
> (v1.0), **propriétaire unique** de la règle. Le présent document reste le **cadrage du chantier**, non
> la norme — en cas de divergence, **la doctrine fait foi**.
>
> L'ouverture de C31 **ne vaut toujours ni décision de requalifier un chantier existant, ni engagement
> des Lots 2 et 3.** **Aucun `recorder.yaml`, runtime, contrat métier, checker, navigation, workflow ni
> changelog n'est créé ou modifié.** Aucune procédure d'archivage ou d'extraction n'est créée : celles
> qui existent restent propriété de leurs détenteurs.

---

## 1. L'angle mort démontré

Un audit transverse en lecture seule (2026-07-19) a passé en revue une vingtaine de chantiers — actifs,
parqués, dormants et clos avec réserve — ainsi que `recorder.yaml`, le corpus Recorder, les doctrines de
journalisation et les protocoles de preuve. Trois constats en ressortent.

**A. Le défaut touche les deux extrémités du cycle de vie.** **Des chantiers actifs attendent des preuves
non productibles ou non conservables, tandis que certains chantiers clos conservent des réserves
impossibles, héritées ou perpétuelles.**

- Côté **actif**, l'exemple le plus net : le protocole de C20 désignait explicitement l'Historique comme
  instrument de preuve, alors que cinq de ses entités décisives n'étaient pas enregistrées — 11 de ses 12
  scénarios n'étaient **pas exerçables**, et le chantier était indéfiniment non clôturable quelle que soit
  la diligence de l'opérateur.
- Côté **clos**, l'audit a relevé des réserves qui ne pourront jamais être soldées en l'état : une réserve
  exigeant de constater l'absence d'une erreur alors que ni la trace ni le contexte ne sont conservés ; une
  réserve de « surveillance continue » sans date, sans seuil de sortie ni propriétaire de la levée, donc
  perpétuelle par construction ; une réserve **héritée** d'un autre chantier sans réexamen de sa
  solvabilité propre, masquant un angle mort spécifique.

**B. Le registre confond ces régimes sous les mêmes mots.** « Preuve terrain différée » désigne
aujourd'hui aussi bien une preuve solvable qu'une preuve impossible. Une réserve insolvable devient alors
une **dette perpétuelle silencieuse** : jamais soldée, jamais relancée, jamais fermée.

**Quatre qualifications à distinguer** — c'est le vocabulaire que la doctrine devra rendre disponible :

| Qualification | Sens |
|---|---|
| **Verrou actif insolvable** | conditionne la clôture, mais la preuve ne peut être ni produite ni conservée ⇒ à débloquer ou à requalifier |
| **Réserve différée solvable** | la preuve est productible et conservable ; il manque l'occurrence ⇒ légitime, à suivre |
| **Réserve différée non solvable en l'état** | la preuve exige un moyen qui n'existe pas encore ⇒ légitime **si dite comme telle**, jamais bloquante par défaut |
| **Réserve sans objet** | la cause a été supprimée structurellement ⇒ la preuve n'a plus d'objet, la réserve doit être close |

**C. Corrélation inverse entre couverture et criticité.** Des chantiers déclarés *non bloquants* sont
instrumentés à près de 100 %, tandis que plusieurs verrous **bloquants** ne disposent que d'une fraction
de leurs entités nommées. L'effort d'observabilité a été investi là où la preuve n'était pas exigée.

**Ce qui manque n'est pas une culture probatoire** — Arsenal en a une : preuve statique, mutation-testing,
oracles comportementaux, preuve négative, et la formule « les corrections ne valent pas validation
terrain » appliquée avec constance. **Il manque une question, posée à un seul moment :**

> *Avant d'inscrire une réserve terrain ou un verrou de clôture : cette preuve est-elle productible et
> conservable par l'installation actuelle ?*

---

## 2. Matière à contractualiser — échelle L1–L5

**Non opposable à ce stade.** Consignée pour instruction au Lot 1.

| Niveau | Question | Mode de défaillance |
|---|---|---|
| **L1** | La preuve est-elle **produite par le runtime** ? | l'événement n'existe pas ⇒ rien à enregistrer |
| **L2** | Est-elle **conservée comme état Recorder**, ou **reconstructible via les événements** ? | entité hors allowlist et non reconstructible |
| **L3** | Est-elle **disponible dans la base courante** ? | purgée (`purge_keep_days`) |
| **L4** | Est-elle **récupérable dans une ou plusieurs sauvegardes analysées hors ligne** ? | sauvegarde non prise ou non conservée |
| **L5** | Preuve **physique, visuelle ou externe** nécessitant un opérateur. | irréductible — pas un défaut |

### 2.1 La distinction `states` / `events`

Distinction **démontrée par le précédent historique**, et décisive pour savoir s'il faut instrumenter :

- les **`states`** sont soumis à l'**allowlist** `recorder.yaml` (`include: entities:`, allowlist stricte
  par entité nommée) ;
- les **`events`** — notamment **`call_service`** et **`homeassistant_start`** — **subsistent même
  lorsque l'état d'une entité n'est pas enregistré** ;
- en conséquence, un **helper écrit par un appel de service** (`set_value`, `set_datetime`,
  `turn_on`/`turn_off`, `counter.*`) est **partiellement reconstructible** ;
- un **template purement dérivé** reste **invisible** s'il n'est pas inclus dans le Recorder : aucun
  service ne l'écrit.

Les événements datent une écriture ; ils ne restituent ni une valeur avant/après, ni un attribut. Ils sont
une source **complémentaire**, jamais un substitut à l'historisation d'état.

### 2.2 Les trois notions déjà établies

Formulées par
[`investigation_historique_cloture_terrain_c16_c15_c13.md`](../../01_rapports/transverses/investigation_historique_cloture_terrain_c16_c15_c13.md)
(§1), **à citer et relier, non à réécrire** :

1. **Absence de séquence exploitable** — la donnée ne contient pas la situation permettant d'exercer le
   critère. Rien à évaluer.
2. **Absence de preuve suffisante** — une séquence partielle existe mais ne couvre pas intégralement le
   critère ; elle contextualise sans prouver.
3. **Non-conformité fonctionnelle** — la donnée montre le runtime se comporter contrairement au contrat.

Avec son **résultat cardinal** : « non clôturable par historique » signifie *preuve absente*, **jamais**
*correctif invalidé*.

---

## 3. Règle cible à instruire

**Non opposable à ce stade.** Formulation de travail :

> Tout verrou de clôture doit être **solvable dans les conditions autorisées du chantier**. Une preuve non
> productible, non conservable ou exclusivement opportuniste **ne peut être bloquante qu'après création du
> moyen de preuve nécessaire**. À défaut, elle doit être explicitement qualifiée comme **non bloquante**,
> **opportuniste**, **différée mais non solvable en l'état**, ou **sans objet**.

**La doctrine n'interdira pas les preuves L5, opportunistes ou non reproductibles.** Elles sont
légitimes — plusieurs chantiers clos en portent honnêtement. Ce qui doit être interdit est qu'une preuve
insolvable devienne **silencieusement** un verrou bloquant.

---

## 4. Précédents réels

| Précédent | Ce qu'il apporte |
|---|---|
| **C18** — [`protocole_validation_c18_sante_pont.md`](../arrosage/protocole_validation_c18_sante_pont.md) | **Modèle de protocole bien qualifié** : classe chaque ligne par type de preuve (*terrain (live)* / *historique*), admet la non-reproductibilité d'avance, interdit l'action intrusive. La brique méthodologique existe déjà — elle n'a jamais été généralisée. |
| **C20** — [`protocole_validation_terrain_absence_cool.md`](../climatisation/protocole_validation_terrain_absence_cool.md) | **Premier chantier rendu solvable par instrumentation Recorder** (#439, 2026-07-19) : cinq entités décisives ajoutées en microscope Population B, qualification L1–L5 des douze scénarios, S12 qualifié L5 opérateur. Cas d'usage fondateur de la règle. |
| **Investigation C16/C15/C13** — [`investigation_historique_cloture_terrain_c16_c15_c13.md`](../../01_rapports/transverses/investigation_historique_cloture_terrain_c16_c15_c13.md) | **Deux sauvegardes HA non chiffrées** combinées ⇒ couverture continue ~50 jours, au-delà de la fenêtre Recorder. Source des trois notions du §2.2 et de la distinction `states`/`events`. |
| **Dépôt d'audit runtime** (`arsenal-runtime`) | **Canal probatoire local déjà existant et éprouvé** : extraction hors ligne, analyse SQLite en lecture seule, empreintes SHA-256, suppression des archives et bases après usage, conservation des seules preuves dérivées. **À reconnaître, pas à réinventer.** |

---

## 5. Frontière avec les niveaux A/B/C SwitchBot

À énoncer explicitement dans la doctrine, pour éviter deux vocabulaires de preuve concurrents :

- les niveaux **A/B/C** de [`switchbot_transactionnel.md`](../../../contrats/switchbot_transactionnel.md)
  restent **propriétaires de la qualité et du niveau de preuve d'une exécution transactionnelle
  SwitchBot** (attribut de niveau, invariant, garde CI) ;
- **L1–L5** qualifie la **productibilité, la conservation et le mode d'obtention** des preuves
  nécessaires à un **chantier** ;
- les deux échelles sont **complémentaires et ne doivent pas être fusionnées**.

---

## 6. Raccords documentaires — *réalisés au Lot 2 (2026-07-19)*

Chacun est resté chez son **propriétaire existant** ; aucun nouveau document en dehors de la doctrine.

1. **Écosystème des dépôts** — ✅ [`ecosysteme_depots_satellites.md`](../../../architecture/ecosysteme_depots_satellites.md)
   §1.1 : `arsenal-runtime` reconnu comme **dépôt local sans remote**, espace de travail pour analyses
   hors ligne, **hors** du tableau des satellites gouvernés ; « seul dépôt modifiable » circonscrit aux
   satellites.
2. **Frontière patrimoine / analyses hors ligne** — ✅ [`diff_auto.md`](../../../outils_externes/nas_arsenal/diff/diff_auto.md) :
   l'exclusion des bases SQLite est un invariant **de la timeline patrimoniale** ; l'analyse hors ligne
   est un **usage distinct** qui ne modifie ni la source unique, ni le pipeline, ni l'invariant.
3. **Doctrine** — ✅ [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
   créée au Lot 1, **§7 corrigé au Lot 2**.

Les **règles internes** du dépôt local (contenu, interdits) sont portées par son propre `README.md` et ne
sont pas recopiées ici. **Aucune procédure d'acquisition, d'extraction ou d'analyse n'est établie** — le
corpus ne documente que des **précédents**.

---

## 7. Séquencement

- **Lot 1 — Doctrine. ✅ LIVRÉ (2026-07-19).**
  [`architecture/03_doctrines/solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
  v1.0, normative et opposable : échelle L1–L5 avec la distinction `states`/`events` (R-L2-1, R-L2-2),
  trois verdicts (R-VERDICT-1), six qualifications de réserve (R-QUALIF-1 à 3), règle centrale
  (R-VERROU-1), dix exigences d'ouverture (R-OUVERTURE-1), gouvernance de l'instrumentation temporaire
  (R-INSTR-1), reconnaissance de L4 (R-L4-1), frontière SwitchBot (R-FRONTIERE-1).
  **Reste à faire : revue de la doctrine.**
- **Lot 2 — Raccords. ✅ LIVRÉ (2026-07-19).** Les trois extensions du §6, chez leurs propriétaires :
  `ecosysteme_depots_satellites.md` (§1.1 — dépôt local hors écosystème satellite, sans remote, espace de
  travail pour analyses hors ligne ; « seul dépôt modifiable » circonscrit aux satellites gouvernés) ·
  `diff_auto.md` (frontière — l'exclusion SQLite est un invariant **de la timeline patrimoniale** ;
  l'analyse hors ligne est un **usage distinct** qui ne l'altère pas) · `arsenal-runtime/README.md`
  (`analyses/` reconnu ; interdit précisé).
  **Correction factuelle du §7 de la doctrine** dans le même lot : retrait de « mécanisme existant,
  éprouvé et outillé », de la propriété d'une méthode ou d'un canal par `arsenal-runtime`, et de toute
  disponibilité automatique ou permanente de L4. Les sauvegardes manuelles de release sont désignées
  source durable privilégiée ; les automatiques restent opportunistes ; aucune sauvegarde ne doit être
  créée ou renommée pour un chantier. **R-L4-1 inchangée.**
- **Lot 3 — Application démonstrative. Non engagé.** Qualifier des réserves existantes selon la doctrine,
  notamment **C29**, **C4** et **C27**. Ce lot **prouve que la doctrine est utilisable** ; sans lui, C31
  est un texte non éprouvé. **Aucune requalification n'est effectuée à ce stade.**

Lots 1 et 2 parallélisables. **C30-A1 et C30-A2 sont traités séparément dans C30**, et n'entrent pas dans
C31. **Aucune régularisation globale des anciens blocs de gouvernance temporelle du Recorder** n'est
engagée — elle supposerait d'appliquer une règle qui n'existe pas encore.

---

## 8. Ce que ce chantier ne décide PAS

Hors périmètre, explicitement :

- toute **modification de `recorder.yaml`** ;
- tout **runtime** ;
- toute **modification de contrat** à l'ouverture ;
- tout **checker**, toute **navigation**, tout **workflow**, tout **changelog** ;
- toute **nouvelle procédure d'archivage ou d'extraction** ;
- toute **duplication de la chaîne NAS** ou de la méthode déjà existante dans le dépôt d'audit runtime ;
- toute **requalification immédiate** de C29, C4 ou C27 (Lot 3, après doctrine) ;
- toute **modification de C20 ou C30**.

---

## 9. Critères de non-clôture

C31 **n'est pas clôturable** tant que :

- la doctrine n'est pas rédigée, mergée et propriétaire unique de sa règle ;
- les trois raccords du §6 ne sont pas faits ;
- la doctrine n'a pas été **appliquée à au moins deux cas réels** (Lot 3) ;
- aucun cas où la doctrine **a changé une décision** n'est constaté — c'est le test d'utilité, pas de
  conformité.

> **Cohérence interne.** Ces critères sont **documentaires, donc solvables sans preuve terrain** : C31 ne
> s'impose pas un verrou qu'il jugerait insolvable chez un autre chantier.

---

## 10. Stop point

Ouverture documentaire uniquement. Prochaine étape : **Lot 1**, après arbitrage propriétaire sur le
périmètre exact de la doctrine.

---

## 11. Renvois

- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Investigation fondatrice : [`investigation_historique_cloture_terrain_c16_c15_c13.md`](../../01_rapports/transverses/investigation_historique_cloture_terrain_c16_c15_c13.md)
- Preuve terrain par sauvegarde unique : [`preuve_terrain_c15_survie_persistantes_reboot.md`](../../01_rapports/notifications/preuve_terrain_c15_survie_persistantes_reboot.md)
- Gouvernance temporelle du Recorder : [`audit_recorder_instrumentation_temporaire.md`](../../01_rapports/architecture/audit_recorder_instrumentation_temporaire.md) · [`plan_action_cloture_validation_terrain_c13_c15_c16_c18.md`](../../03_plans_action/transverses/plan_action_cloture_validation_terrain_c13_c15_c16_c18.md)
- Contrat Recorder (inclusion, Population A/B) : [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md)
- Protocole modèle : [`protocole_validation_c18_sante_pont.md`](../arrosage/protocole_validation_c18_sante_pont.md)
- Cas fondateur : [`protocole_validation_terrain_absence_cool.md`](../climatisation/protocole_validation_terrain_absence_cool.md)
- Frontière d'échelle : [`switchbot_transactionnel.md`](../../../contrats/switchbot_transactionnel.md)
