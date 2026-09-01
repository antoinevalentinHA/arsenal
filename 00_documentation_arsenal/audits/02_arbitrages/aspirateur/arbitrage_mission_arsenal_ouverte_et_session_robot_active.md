# Note d'arbitrage — « Mission Arsenal ouverte » et « session robot active » (rendue)

> Type : note d'arbitrage — **décision rendue** (acte terminal de l'arbitrage sur `Q1`).
> Statut : **ARBITRAGE HUMAIN RENDU.**
> Domaine : **Aspirateur**.
> Date : **2026-09-01**.
> Portée : sémantique contractuelle de « mission ouverte » dans le domaine `aspirateur` —
> chapitres [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) et
> [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md), et leur restitution à
> l'opérateur.
> Origine : audit de conformité du domaine → contre-expertise indépendante → confrontation
> `A × B` → arbitrage opérateur sur la question `Q1`.
> Référence dépôt : branche `main`, HEAD `54106296b1fe7357a6c3220d3d4fa3c2a3757e1e` (arbre propre,
> documents sources mergés par #753).
> **Ce document ne modifie aucun contrat, aucun runtime, aucun checker, aucun registre et aucun
> changelog. Il n'ouvre aucun chantier et ne porte aucun correctif.**

---

## 1. Question arbitrée

**`Q1` — Sémantique de « mission ouverte »**, posée comme **arbitrage normatif préalable** par la
confrontation `A × B`
([`confrontation_audit_contre_expertise_aspirateur.md`](../../02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md) §11).

Elle portait sur cinq objets : la définition de « mission Arsenal ouverte » ; la distinction
éventuelle avec la notion de session physique ; les libellés rendus à l'opérateur ; l'autorité de
chaque notion ; leur contexte d'usage.

**Seule `Q1` est tranchée par le présent document.**

---

## 2. Faits établis ayant motivé l'arbitrage

Faits repris des trois rapports sources, non ré-ouverts ici.

| # | Fait | Source |
|---|---|---|
| 1 | Le domaine porte **deux** notions distinctes sous le même nom « mission ouverte », introduites par deux chapitres différents. | `AUD-ASP-01` · `CC-01` |
| 2 | [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 nomme un dixième état canonique **Mission ouverte** (`mission_ouverte`) : « Une session de nettoyage est **ouverte** — donc reprenable. **Ne dit rien** du mouvement du robot. » `ASP-INV-68` précise qu'il « ne dérive **pas** de l'état machine mais du **témoin de session** ». | `08` §1 |
| 3 | [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2, `ASP-INV-87` : « Une mission Arsenal est ouverte **si et seulement si** le verdict appartient à la classe O, sous-classe O-R comprise. Aucun témoin natif — état machine, témoin de session, entité `vacuum` — ne l'établit ni ne s'y substitue. » | `15` §2 |
| 4 | Le témoin natif de session est **désaligné du mouvement dans les deux sens**, et c'est prouvé : sur-inclusif (session ouverte, robot immobile hors dock, témoin `on`) et sous-inclusif (robot roulant en `returning_home`, témoin `off` — 53 s, 25 s puis 28,3 s consignées). | `08` §3 · en-tête de `10_scripts/aspirateur/lancer_mission.yaml` |
| 5 | Le runtime matérialise **les deux** notions : l'attribut natif `mission_ouverte` du capteur d'état canonique, dérivé du témoin natif, et la liste `verdict_ouvert` du moteur, dérivée du verdict. | `CC-01` |
| 6 | Le prédicat d'affichage des surfaces de conduite lit **exclusivement** l'état canonique (état ou attribut) ; la garde d'acceptation du backend lit **exclusivement** le verdict. Les deux prédicats **ne coïncident pas**. | `RC-02` |
| 7 | Deux combinaisons en découlent, dérivées des prédicats et **non observées** : **(a)** sur-offre — activité native sans verdict de classe O, notamment une mission lancée depuis l'application constructeur ; **(b)** sous-offre — verdict de classe O alors que le témoin natif est `off`, notamment pendant le retour au dock. | `AUD-ASP-01` · `RC-02` |
| 8 | `ASP-CI-11` interdit mécaniquement à tout fichier hors des huit nommés — les arbres Lovelace inclus — de mentionner l'entité de verdict. L'interface **ne peut donc pas, par construction, aligner directement ses conditions sur l'autorité métier**. | `RC-02` |
| 9 | **Aucune contradiction factuelle** n'existe entre l'audit et la contre-expertise sur ce noyau ; les questions factuelles de l'un reçoivent de l'autre des réponses concordantes. | Confrontation §11 |
| 10 | `AUD-ASP-01`, `CC-01` et `RC-02` forment **un seul noyau causal**, découpé en cause contractuelle et effet de projection ; les additionner comme trois écarts serait un double comptage. | Confrontation §10 et §11 |

---

## 3. Décision opérateur — texte reproduit fidèlement

> « Arsenal distingue contractuellement une “mission Arsenal ouverte”, établie exclusivement par le
> verdict de classe O, d'une “session robot active”, observée exclusivement par le témoin natif
> Roborock.
>
> Le témoin natif décrit l'activité physique du robot ; il n'autorise, n'ouvre ni ne clôt une mission
> Arsenal. Le verdict décrit la responsabilité métier d'Arsenal ; il ne prétend pas décrire à lui
> seul l'activité physique instantanée du robot.
>
> Les deux notions peuvent coexister et diverger sans incohérence. L'UI doit les restituer sous des
> libellés distincts et utiliser l'autorité adaptée à chaque usage. »

---

## 4. Portée normative exacte de la décision

La décision tranche **uniquement** :

1. l'**existence de deux notions distinctes** ;
2. leur **nom métier** — `mission Arsenal ouverte` et `session robot active` ;
3. leur **autorité respective** — le verdict de classe O pour la mission Arsenal, le témoin natif
   Roborock pour la session physique ;
4. la **possibilité légitime de divergence** entre les deux ;
5. l'**obligation de libellés UI distincts** ;
6. l'**obligation d'utiliser l'autorité correspondant à l'usage**.

### 4.1 Les deux notions

| Objet | Définition | Autorité |
|---|---|---|
| **Mission Arsenal ouverte** | responsabilité métier d'Arsenal encore ouverte | **verdict de classe O** |
| **Session robot active** | activité physique signalée par le robot | **témoin natif Roborock** |

### 4.2 Ce que chaque autorité ne fait pas

- Le **témoin natif** décrit l'activité physique du robot. Il **n'autorise pas**, **n'ouvre pas** et
  **ne clôt pas** une mission Arsenal.
- Le **verdict** décrit la responsabilité métier d'Arsenal. Il **ne prétend pas** décrire à lui seul
  l'activité physique instantanée du robot.

### 4.3 Divergence légitime

Les deux notions peuvent **coexister et diverger sans incohérence**. En particulier :

- une **session robot active peut exister sans mission Arsenal ouverte**, notamment pour une mission
  externe lancée hors d'Arsenal ;
- une **mission Arsenal ouverte peut subsister alors que le témoin natif est `off`**, notamment
  pendant certaines phases de retour ou de clôture ;
- cette divergence est **légitime** et **ne constitue plus une contradiction**.

### 4.4 Statut de la décision et ordre de propagation

- La **décision humaine est acquise**.
- Sa **sémantique doit être propagée dans les contrats avant toute modification runtime**.
- Les **rapports historiques restent inchangés** : ils sont datés de leur SHA et ne sont pas
  ré-écrits par le présent arbitrage.
- Aucun **état de clôture du domaine** n'est modifié par ce document.

---

## 5. Conséquences contractuelles nécessaires

Conséquences **sémantiques**, à instruire par le véhicule contractuel approprié. Le présent document
**n'amende aucune clause** et n'en rédige aucune.

1. **Deux notions nommées séparément.** Le vocabulaire canonique du domaine doit porter les deux
   notions sous **deux noms distincts** : `mission Arsenal ouverte` et `session robot active`.
2. **Le nom `mission_ouverte` devient contractuellement ambigu.** Employer ce même nom pour les deux
   notions n'est plus tenable : il désigne aujourd'hui à la fois l'état canonique natif de
   [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 et la notion métier de
   [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2. La levée de cette ambiguïté
   est une conséquence de la décision ; **le nom de remplacement, sa forme et son support ne sont pas
   choisis ici**.
3. **Chaque autorité reste souveraine dans son ordre.** `ASP-INV-87` demeure l'autorité de la mission
   Arsenal ; le témoin natif demeure l'observation de l'activité physique. La décision **ne
   subordonne ni n'abroge** l'une au profit de l'autre.
4. **La divergence cesse d'être un défaut contractuel.** Les clauses ne doivent plus lire une
   coexistence des deux valeurs comme une incohérence à résorber.
5. **Conduite de mission.** La conduite d'une **mission Arsenal** doit se fonder sur l'**autorité
   métier retenue**, sous réserve du mécanisme de projection encore à arbitrer en `Q2`.

---

## 6. Conséquences UI exigées — niveau sémantique uniquement

1. L'UI doit **restituer les deux notions sous des libellés distincts** : ce qui est rendu comme
   mission Arsenal ne doit pas être rendu sous le même libellé que ce qui est rendu comme session
   physique du robot.
2. L'UI doit **utiliser l'autorité adaptée à chaque usage** : l'autorité métier pour ce qui relève de
   la responsabilité d'Arsenal, l'autorité native pour ce qui relève de l'activité physique.
3. Ces obligations sont **sémantiques**. Le **mécanisme** par lequel l'interface reçoit la projection
   de l'autorité métier **n'est pas arbitré ici** : il relève de `Q2`.

**Aucun nom d'entité, d'attribut, de helper, de capteur, de libellé rendu ni de fichier futur n'est
choisi par le présent document.**

---

## 7. Éléments explicitement non arbitrés

Ne sont **pas** tranchés par cette décision :

- le mécanisme technique de projection vers l'UI ;
- une éventuelle évolution d'`ASP-CI-11`, de son allowlist ou de la projection canonique ;
- une exception nominative ;
- un nouvel attribut ;
- un nouveau capteur ;
- la modification d'un capteur existant ;
- le masquage ou la désactivation des gestes ;
- les conditions détaillées de chaque bouton ;
- le découpage en lots ;
- le numéro ou le périmètre d'un chantier ;
- les autres questions `Q2` à `Q8` ;
- les constats non convergents ;
- les validations terrain ;
- la clôture du domaine.

---

## 8. `Q2` — maintenue explicitement ouverte

> **Par quel mécanisme autorisé l'interface doit-elle recevoir la projection de l'autorité métier
> retenue pour une mission Arsenal ouverte, et faut-il pour cela faire évoluer `ASP-CI-11`, son
> allowlist ou la projection canonique ?**

`Q2` **reste ouverte**. Le présent arbitrage **ne la préjuge pas** et ne retient **aucune option
technique** — ni exception nominative supplémentaire, ni attribut, ni capteur, ni forme de
projection.

---

## 9. Effet sur les constats — ce que la consignation ne fait pas

- Les constats `AUD-ASP-01`, `CC-01` et `RC-02` ne sont **pas automatiquement « corrigés » par la
  seule consignation** du présent arbitrage.
- Leur **fermeture dépendra** de la propagation contractuelle de la sémantique décidée, de l'issue de
  `Q2`, de l'implémentation qui en découlera, et des preuves correspondantes.
- Aucune sévérité n'est officialisée, aucun constat n'est requalifié, aucun constat n'est clos par ce
  document.
- Aucun état de clôture du domaine `aspirateur` n'est modifié.

---

## 10. Rapports sources

- [`01_rapports/aspirateur/audit_conformite_domaine_post_integration.md`](../../01_rapports/aspirateur/audit_conformite_domaine_post_integration.md)
  — audit de conformité du domaine après intégration (constat `AUD-ASP-01`).
- [`02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md`](../../02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md)
  — contre-expertise indépendante (constats `CC-01` et `RC-02`).
- [`02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md`](../../02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md)
  — confrontation `A × B` (noyau `N1` ; questions `Q1` et `Q2`).

Clauses citées : [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 et §3
(`ASP-INV-68`, `ASP-INV-47`) ; [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2
(`ASP-INV-87`). Citées **fidèlement, pour référence** ; **non amendées** par ce document.

---

## 11. Chaîne de traçabilité

```
audit_conformite_domaine_post_integration.md (AUD-ASP-01, proposé, non arbitré)
   ├─→ contre_expertise_domaine_aspirateur.md (CC-01 cause, RC-02 effet)
   └─→ confrontation_audit_contre_expertise_aspirateur.md (noyau N1 ; Q1 posée, Q2 posée)
          └─→ arbitrage_mission_arsenal_ouverte_et_session_robot_active.md
                 (présent document — Q1 tranchée ; Q2 laissée ouverte)
```

---

*Note d'arbitrage Aspirateur — décision humaine rendue sur `Q1`, transcription documentaire. Acte de
gouvernance : aucun correctif, aucun contrat, runtime, checker, registre ou changelog modifié ; aucun
chantier ouvert ni numéroté. `Q2` reste ouverte. Domaine Aspirateur non clôturé.*
