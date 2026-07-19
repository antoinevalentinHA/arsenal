# 🧭 ARSENAL — DOCTRINE SYSTÈME · Solvabilité probatoire des chantiers

---

## 📌 Statut

- Doctrine système transverse Arsenal.
- **NORMATIVE et OPPOSABLE**.
- Applicabilité globale : tout chantier, tout audit, tout protocole de validation
  attendant une preuve runtime ou terrain.
- Version : **v1.0** — 2026-07-19 (création, chantier C31 Lot 1).

**Propriétaire unique** de la règle de solvabilité probatoire : qualification de la
**productibilité**, de la **conservation** et du **mode d'obtention** des preuves
attendues par un chantier.

---

## 🎯 Portée

Cette doctrine s'applique dès qu'un document de chantier, d'audit, de plan d'action ou
de protocole **subordonne une clôture, une décision ou une requalification à une preuve**
issue du runtime ou du terrain.

Elle répond à une question, posée à un seul moment — **avant** d'inscrire la preuve
comme condition :

> *Cette preuve est-elle productible et conservable par l'installation actuelle ?*

### Ce que cette doctrine ne fait pas

- Elle **ne décrit aucune procédure** d'archivage, d'extraction ou d'analyse historique.
  Celles qui existent restent propriété de leurs détenteurs (§7).
- Elle **ne redéfinit pas** les critères d'inclusion, la classification Population A/B ni
  l'admissibilité des entités : le contrat Recorder en reste seul propriétaire (§6.3).
- Elle **ne fusionne pas** son vocabulaire avec les niveaux A/B/C SwitchBot (§8).
- Elle **ne transforme aucune preuve L5 ou opportuniste en non-conformité** (§3, §4).

---

## 1. Échelle de solvabilité L1–L5

Toute preuve attendue **DOIT** être qualifiée sur cette échelle. Chaque niveau a un mode
de défaillance et un remède distincts.

| Niveau | Définition | Défaillance | Remède |
|---|---|---|---|
| **L1** | Preuve **produite par le runtime** : l'événement, la transition ou l'état existe. | l'événement n'est pas émis ⇒ rien à enregistrer | correctif runtime |
| **L2** | Preuve **enregistrée ou reconstructible** (cf. §1.1) | ni historisée ni reconstructible | instrumentation ciblée (§6) |
| **L3** | Preuve **disponible dans la base courante** | purgée avant lecture | recours à L4 |
| **L4** | Preuve **récupérable dans une ou plusieurs sauvegardes analysées hors ligne** | sauvegarde non prise ou non conservée | cf. §7 |
| **L5** | Preuve **physique, visuelle ou externe**, nécessitant un opérateur ou une source indépendante | — *(pas un défaut : un mode d'obtention)* | observation qualifiée |

Un même chantier peut relever de plusieurs niveaux selon ses preuves. Le niveau se
qualifie **preuve par preuve**, jamais globalement.

### 1.1 L2 — `states` et `events` ne suivent pas la même règle

Distinction **normative**, décisive pour savoir s'il faut instrumenter :

- les **`states`** sont soumis à l'**allowlist** du Recorder : une entité non inscrite
  nominativement n'a **aucun** historique d'état, ni dans la base courante, ni dans une
  sauvegarde ;
- les **`events`** — notamment **`call_service`** et **`homeassistant_start`** — peuvent
  **subsister hors allowlist**, et rester exploitables alors même que l'état de l'entité
  concernée n'est pas enregistré.

Il en découle deux règles de qualification :

> **R-L2-1.** Un **helper écrit par un appel de service** (`set_value`, `set_datetime`,
> `turn_on`/`turn_off`, opérations de compteur) est **partiellement reconstructible** via
> les événements.
>
> **R-L2-2.** Un **template purement dérivé** reste **invisible** s'il n'est pas
> historisé : aucun appel de service ne l'écrit.

**Les événements datent une écriture ; ils ne restituent ni une valeur avant/après, ni un
attribut.** Ils sont une source **complémentaire**, jamais un substitut à l'historisation
d'état lorsque la preuve porte sur une comparaison, une persistance ou un attribut.

---

## 2. Trois verdicts à ne jamais confondre

Notions établies par l'investigation historique de clôture terrain (§9) et **reprises ici
comme normatives**, sans réécriture :

1. **Absence de séquence exploitable** — la donnée ne contient pas la *situation*
   permettant d'exercer le critère. Rien à évaluer.
2. **Absence de preuve suffisante** — une séquence partielle existe mais **ne couvre pas
   intégralement** le critère ; elle *contextualise* sans *prouver*.
3. **Non-conformité fonctionnelle** — la donnée montre le runtime se comporter
   **contrairement** au contrat.

> **R-VERDICT-1 (opposable).** Une **impossibilité de clôture par historique ne vaut
> jamais, à elle seule, preuve de non-conformité fonctionnelle.** « Non clôturable par
> historique » signifie *preuve absente*, **jamais** *correctif invalidé*.

Toute conclusion relevant du verdict 3 **DOIT** être étayée par une observation positive
du comportement, jamais par une absence.

---

## 3. Qualification des réserves et des verrous

Toute preuve attendue **DOIT** porter l'une de ces six qualifications, explicitement
écrite dans le document de chantier et reprise au registre.

| Qualification | Définition | Effet sur la clôture |
|---|---|---|
| **Verrou actif solvable** | conditionne la clôture ; la preuve est productible et conservable dans les conditions autorisées | **bloquant** — légitime |
| **Verrou actif non solvable en l'état** | conditionne la clôture, mais la preuve ne peut être ni produite ni conservée | **interdit** tel quel (§4) — à débloquer ou requalifier |
| **Réserve différée solvable** | la preuve est productible et conservable ; il manque l'occurrence | **non bloquant**, à suivre |
| **Réserve différée non solvable en l'état** | la preuve exige un moyen de preuve qui n'existe pas encore | **non bloquant**, tant qu'elle est dite comme telle |
| **Réserve opportuniste ou L5** | preuve physique, visuelle, externe, ou dépendant d'une occurrence non provocable | **non bloquant** — pleinement légitime |
| **Réserve sans objet** | la cause a été **supprimée structurellement** ; la preuve n'a plus d'objet | **close** — ne doit pas rester ouverte |

> **R-QUALIF-1.** Une réserve non qualifiée est réputée **verrou actif**. C'est
> précisément ce défaut que la doctrine corrige : une réserve insolvable non qualifiée
> devient une **dette perpétuelle silencieuse** — jamais soldée, jamais relancée, jamais
> fermée.
>
> **R-QUALIF-2.** Une réserve **héritée** d'un autre chantier **DOIT** être requalifiée
> pour son périmètre propre. L'héritage ne transporte pas la solvabilité.
>
> **R-QUALIF-3.** Une réserve **sans critère de levée** (ni date, ni seuil de sortie, ni
> propriétaire) est **interdite** : elle est perpétuelle par construction.

---

## 4. Règle centrale

> **R-VERROU-1 (opposable).**
> **Tout verrou de clôture doit être solvable dans les conditions autorisées du
> chantier. Une preuve non productible, non conservable ou exclusivement opportuniste ne
> peut être bloquante qu'après création du moyen de preuve nécessaire. À défaut, elle
> doit être explicitement qualifiée comme non bloquante, opportuniste, différée mais non
> solvable en l'état, ou sans objet.**

> **R-VERROU-2 (définition opposable).** La solvabilité s'évalue **dans les limites posées
> par le chantier lui-même** : absence de **panne fabriquée**, absence de **forçage**
> d'état, absence d'**action intrusive**, absence de toute **manipulation interdite** par
> le protocole ou le contrat applicable — observation naturelle et non provoquée.
>
> **Une preuve techniquement obtenable uniquement en violant ces limites est non solvable
> dans le cadre du chantier.** Elle relève alors de R-VERROU-1 : elle doit être qualifiée,
> ou le chantier doit lever explicitement la limite par un arbitrage propriétaire tracé
> (par exemple l'autorisation d'un test provoqué).

**Ce qui est interdit** n'est pas la preuve difficile, rare ou humaine : c'est qu'une
preuve insolvable devienne **silencieusement** un verrou bloquant.

---

## 5. Exigences à l'ouverture et au cadrage

Pour **toute** preuve runtime ou terrain attendue, le document d'ouverture ou de cadrage
**DOIT** :

1. **identifier précisément la preuve** — quelle observation, sur quelle entité ou quel
   événement, dans quelle situation ;
2. **qualifier son niveau L1–L5** ;
3. **vérifier l'existence du producteur** — l'événement ou l'état est-il réellement émis
   par le runtime ;
4. **vérifier sa conservation** — l'entité est-elle historisée, ou la preuve est-elle
   reconstructible via les événements (§1.1) ;
5. **vérifier l'horizon nécessaire** et le confronter à la rétention effective ; si
   l'horizon excède la fenêtre courante, prévoir explicitement le recours à L4 ;
6. **prévoir une instrumentation temporaire si nécessaire** (§6) ;
7. **définir le propriétaire** de la preuve et de son instrumentation ;
8. **fixer une date de réévaluation** calendaire ;
9. **définir un critère de retrait** ;
10. **ne poser aucun verrou techniquement insolvable non déclaré** (§4).

> **R-OUVERTURE-1.** Un protocole qui désigne un instrument de preuve (Historique,
> journal, capteur) **DOIT** avoir vérifié que cet instrument couvre effectivement les
> entités ou événements qu'il cite. Un protocole fondé sur un instrument aveugle à son
> propre objet est **non conforme**.

---

## 6. Instrumentation temporaire

Lorsqu'une preuve exige une instrumentation, celle-ci **DOIT** respecter les règles
suivantes.

### 6.1 Règles opposables

1. **Périmètre strictement lié à la preuve** — aucune entité au-delà de ce que la preuve
   exige.
2. **Justification explicite** — rôle, utilité probatoire, et rattachement au chantier.
3. **Horizon** déclaré, lié aux situations que la preuve doit capter.
4. **Date de réévaluation calendaire**, calculée depuis la **date réelle de pose**.
5. **Critère de retrait** explicite.
6. **Aucun maintien silencieux** : à l'échéance, une décision propriétaire **explicite et
   datée** est obligatoire — maintien motivé, retrait, modification de la stratégie de
   preuve, ou autorisation d'un test provoqué. La réévaluation **n'est pas** une
   suppression automatique.
7. **Aucune mutualisation entre chantiers** sans besoin commun démontré : chaque
   instrumentation porte son propriétaire, son horizon, sa date et son critère de retrait
   **propres**.

### 6.2 Réévaluation

À l'échéance, la **procédure de classification est rejouée** : l'instrumentation devient
observabilité permanente, ou elle est retirée. Une instrumentation utile au-delà de sa
preuve n'est pas un échec — un maintien non décidé, si.

### 6.3 Frontière avec le contrat Recorder

> **R-INSTR-1.** Cette doctrine détermine **quand** une preuve exige une instrumentation
> et **sous quelles conditions de gouvernance** elle est posée. Le **contrat Recorder**
> reste propriétaire de la **classification Population A/B**, des **critères
> d'admissibilité** des entités, des seuils de cardinalité et de fréquence, et de la
> politique de rétention.
>
> Une instrumentation conforme à la présente doctrine mais **inadmissible** au regard du
> contrat Recorder est **refusée** : la doctrine ne crée aucune dérogation.

---

## 7. L4 — canal probatoire hors ligne

**L4 est un mécanisme existant, éprouvé et outillé.** Cette doctrine le **reconnaît et le
référence** ; elle **ne le décrit pas** et **ne crée aucune procédure**.

Ce qu'il faut en retenir pour qualifier une preuve :

- des **investigations historiques** ont déjà été menées sur des sauvegardes Home
  Assistant non chiffrées, avec extraction de la base Recorder et analyse hors ligne en
  lecture seule (§9) ;
- **plusieurs sauvegardes peuvent être combinées** pour dépasser la fenêtre de rétention
  courante — un précédent a produit une couverture continue d'environ cinquante jours ;
- l'**exécution** de ce canal (méthode, scripts, empreintes, conservation, destruction
  après usage) est **propriété du dépôt local d'audit runtime** ; le **sens et les
  verdicts** restent propriété des rapports d'audit Arsenal ;
- la distinction du §1.1 s'applique **intégralement** à L4 : une sauvegarde restitue les
  `states` **soumis à l'allowlist** et les `events` **présents en base**. Une entité hors
  allowlist est absente de la sauvegarde **comme** de la base courante.

> **R-L4-1.** L4 **ne corrige jamais** un défaut L1 ou L2. Il ne traite que la
> **disponibilité dans le temps** d'une preuve déjà produite et déjà enregistrée.

---

## 8. Frontière avec les niveaux A/B/C SwitchBot

Deux échelles coexistent dans Arsenal. Elles ne se recouvrent pas.

- Les niveaux **A/B/C** de `contrats/switchbot_transactionnel.md` restent **propriétaires
  du niveau de preuve d'une exécution transactionnelle SwitchBot** — qualité et
  honnêteté du constat d'exécution d'une commande.
- **L1–L5** qualifie la **productibilité, la conservation et le mode d'obtention** des
  preuves nécessaires à un **chantier**.

> **R-FRONTIERE-1.** Les deux échelles sont **complémentaires et non substituables**.
> Elles ne doivent être ni fusionnées, ni traduites l'une dans l'autre. Un niveau A/B/C
> ne qualifie pas la solvabilité d'un verrou de clôture ; un niveau L1–L5 ne qualifie pas
> la qualité d'une exécution transactionnelle.

---

## 9. Références — propriétaires existants

Cette doctrine **référence** et ne recopie pas :

- **Trois verdicts (§2)** — [`investigation_historique_cloture_terrain_c16_c15_c13.md`](../../audits/01_rapports/transverses/investigation_historique_cloture_terrain_c16_c15_c13.md) §1.
- **Précédent L4 mono-sauvegarde** — [`preuve_terrain_c15_survie_persistantes_reboot.md`](../../audits/01_rapports/notifications/preuve_terrain_c15_survie_persistantes_reboot.md).
- **Inclusion, Population A/B, rétention** — [`architecture/01_recorder/contrat.md`](../01_recorder/contrat.md) *(propriétaire)*.
- **Gouvernance temporelle du Recorder** — [`audit_recorder_instrumentation_temporaire.md`](../../audits/01_rapports/architecture/audit_recorder_instrumentation_temporaire.md) · [`plan_action_cloture_validation_terrain_c13_c15_c16_c18.md`](../../audits/03_plans_action/transverses/plan_action_cloture_validation_terrain_c13_c15_c16_c18.md).
- **Protocole modèle, typage des preuves** — [`protocole_validation_c18_sante_pont.md`](../../audits/04_chantiers/arrosage/protocole_validation_c18_sante_pont.md).
- **Cas fondateur d'instrumentation** — [`protocole_validation_terrain_absence_cool.md`](../../audits/04_chantiers/climatisation/protocole_validation_terrain_absence_cool.md).
- **Frontière d'échelle** — [`switchbot_transactionnel.md`](../../contrats/switchbot_transactionnel.md) *(propriétaire)*.
- **Robustesse et régimes d'état** — [`principes_generaux.md`](principes_generaux.md).

---

## 📌 Statut d'opposabilité

- Document d'architecture Arsenal, **normatif et opposable**, applicabilité globale
  (tous domaines, tous chantiers).
- Positionné dans la couche doctrinale (`architecture/03_doctrines/`), entre les contrats
  fonctionnels et les documents d'architecture domaine.
- **Propriétaire unique** de la règle de solvabilité probatoire. Ne crée aucune procédure
  d'archivage ou d'extraction ; ne redéfinit aucun critère d'inclusion Recorder.
- **Aucun garde-fou CI à ce jour** : la conformité repose sur la relecture à l'ouverture
  et au cadrage. Un contrôle automatisé n'est ni écrit ni promis.
- Stable, modifié uniquement lors d'évolutions doctrinales, versionné explicitement.

# ==========================================================
