# Chantier ASPIRATEUR (C45) — Propagation et exécution des arbitrages `Q1` et `Q2`

| Champ | Valeur |
|---|---|
| **Chantier** | Propager dans les contrats, la CI, le runtime et l'interface la sémantique tranchée par les arbitrages `Q1` et `Q2` : deux notions distinctes — **mission Arsenal ouverte** (autorité : verdict de classe `O`) et **session robot active** (autorité : témoin natif Roborock) —, une **projection métier dédiée** en lecteur pur nominatif sous `ASP-CI-11`, la **migration atomique** de l'attribut ambigu `mission_ouverte`, et les **règles d'offre** des gestes de conduite. |
| **Domaine** | Aspirateur. |
| **Nature** | **Propagation gouvernée d'un arbitrage rendu.** Ce n'est **pas** une exploration architecturale : les options ont été examinées et tranchées en `Q2` §4, et ce chantier n'en rouvre aucune. |
| **Statut** | **Ouvert — Lots 1 et 2 exécutés (Lot 1 : 2026-09-01 · Lot 2 : 2026-09-02). Lots 3 à 7 non exécutés.** **Lot 1** — la rectification documentaire `D1` est **produite, datée, classée et indexée** ([`rectification_cardinal_allowlist_asp_ci_11.md`](../../02_arbitrages/aspirateur/rectification_cardinal_allowlist_asp_ci_11.md)), conformément au véhicule décidé au §4.1 ; `Q1`, `Q2`, l'audit, la contre-expertise et la confrontation sont **prouvés inchangés**. **Lot 2** — les chapitres `08`, `11`, `12` et `15` portent la sémantique de `Q1` et `Q2` ; **`ASP-INV-96`**, **`ASP-INV-97`** et **`ASP-INV-98`** sont déclarés ; la dette `D2` est soldée **en commentaire seul** ; le recensement du §3.2 est **rectifié**. **Checker Aspirateur vert et inchangé** ; aucun Lovelace, aucune ligne exécutable de runtime, aucun changelog. **Ce qui reste devant** : aucun checker, aucun runtime et aucune interface n'ont encore été modifiés — c'est l'objet des Lots 3 à 6, et le **code technique** de l'attribut ambigu ne bascule qu'au **Lot 5** (décision `H-3`, §5.2). |
| **Priorité** | **P2** — aucun risque de sûreté établi ; le backend refuse déjà correctement. L'enjeu est la **cohérence de l'offre à l'opérateur** et la levée de la cause structurelle de `RC-02`. |
| **Ouvert le** | 2026-09-01. |
| **Prochain jalon** | **Lot 3 — extension CI** (§5.3). Les **Lots 1 et 2 sont exécutés** ; la dette `D2` est **soldée** au Lot 2 item 2.11. Le Lot 3 garde ce que le Lot 2 vient d'écrire — `ASP-INV-96`, `ASP-INV-97`, `ASP-INV-98` — et son item 3.5 porte désormais sur **quatre** représentations non gardées (§3.2 rectifié). |
| **Registre** | Chantier **C45** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Autorités amont** | [`arbitrage_mission_arsenal_ouverte_et_session_robot_active.md`](../../02_arbitrages/aspirateur/arbitrage_mission_arsenal_ouverte_et_session_robot_active.md) (`Q1`) · [`arbitrage_projection_mission_arsenal_ouverte_vers_interface.md`](../../02_arbitrages/aspirateur/arbitrage_projection_mission_arsenal_ouverte_vers_interface.md) (`Q2` et décision subsidiaire sur les gestes). |
| **Constats couverts** | `AUD-ASP-01`, `CC-01`, `RC-02` — **un seul noyau causal** (confrontation §10 et §11), jamais additionnés comme trois écarts. `AUD-ASP-04` — **dette contractuelle locale**, distincte de ce noyau — est **rattaché au Lot 2** par décision rendue (§4.2). |

> **⚠️ Portée du présent acte — ouverture, et rien d'autre.**
> Aucun contrat amendé. Aucun checker modifié. Aucun runtime touché. Aucun arbre Lovelace touché.
> Aucun changelog créé (doctrine [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1 — artefact de release).
> **Aucun identifiant technique n'est attribué ni proposé** : ni nom d'entité, ni nom d'attribut, ni
> numéro d'invariant, ni identifiant d'automation, ni nom de fichier runtime futur. `Q2` §8 les a
> explicitement laissés hors arbitrage, et ce document ne s'y substitue pas.
> **Aucun constat n'est fermé, requalifié ni doté d'une sévérité officielle par cette ouverture.**
> **Aucun état de clôture du domaine `aspirateur` n'est modifié.**

---

## 1. Origine

La chaîne est close en amont et n'est pas rouverte ici :

```
audit_conformite_domaine_post_integration.md      (AUD-ASP-01, proposé, non arbitré)   #753
   ├─→ contre_expertise_domaine_aspirateur.md     (CC-01 cause, RC-02 effet)           #753
   └─→ confrontation_audit_contre_expertise_…md   (noyau N1 ; Q1 et Q2 posées)         #753
          └─→ arbitrage … mission_arsenal_ouverte_et_session_robot_active.md (Q1)      #755
                 └─→ arbitrage … projection_mission_arsenal_ouverte_vers_interface.md  (Q2)  #758
                        └─→ **C45 — le présent chantier** (propagation et exécution)
```

`Q1` §4.4 et `Q2` §10 posent tous deux la même contrainte d'ordre : **la sémantique décidée doit être
propagée dans les contrats avant toute modification runtime.** Ce chantier n'existe que pour exécuter
cet ordre, dans cet ordre.

---

## 2. Ce qui est déjà tranché — rappel non ré-ouvrable

Reproduit pour cadrage. En cas d'écart entre ce rappel et les notes d'arbitrage, **les notes priment**.

### 2.1 Acquis de `Q1`

1. « Mission Arsenal ouverte » = **responsabilité métier d'Arsenal encore ouverte**, établie
   **exclusivement** par le verdict de classe `O` (`ASP-INV-87`, sous-classe `O-R` comprise).
2. « Session robot active » = **activité physique** observée **exclusivement** par le témoin natif
   Roborock.
3. Les deux notions sont **distinctes** et peuvent **légitimement diverger**.
4. L'interface doit les restituer sous **libellés distincts** et employer **l'autorité adaptée à
   chaque usage**.

### 2.2 Acquis de `Q2`

1. La projection de « mission Arsenal ouverte » vers l'UI est portée par une **projection métier
   dédiée**, dérivée de la **seule** appartenance du verdict à la classe `O`.
2. Cette projection est un **lecteur pur**, autorisé **nominativement** par `ASP-CI-11`, **sans aucun
   droit d'écriture**.
3. **Lovelace ne lit jamais directement le helper de verdict.**
4. L'attribut aujourd'hui nommé `mission_ouverte` — qui porte en réalité la **session robot active** —
   est **remplacé par migration atomique**, sans coexistence temporaire.
5. `unknown`, `unavailable` et le hors-vocabulaire **ne sont jamais rabattus sur `false`**
   (`ASP-INV-45`).
6. **Toute** liste runtime embarquant une classe de verdict est confrontée par la CI **à égalité
   exacte** avec l'ensemble canonique fermé correspondant, **y compris celles qui ne le sont pas
   aujourd'hui**.
7. La **navigation** Aspirateur reste adossée à l'**activité physique** du robot.

### 2.3 Acquis de la décision subsidiaire — gestes de conduite

| Règle | Contenu |
|---|---|
| **Portée générale** | Les gestes de conduite **Arsenal** ne sont proposés que **tant que la mission Arsenal est ouverte** (verdict ∈ classe `O`). |
| **Arrêt** | Disponible **pendant toute la classe `O`**, **sans dépendre du témoin natif de session**. |
| **Retour base** | Disponible pendant la classe `O`, **sauf** robot déjà **en retour**, **amarré** ou **en charge** — exclusions de **sens physique**, non d'autorité. |
| **Sortie de classe `O`** | Arrêt et Retour base **disparaissent**, même si le robot reste physiquement actif. |
| **Mission externe** | **N'expose pas** les gestes de conduite Arsenal. |
| **Pilotage physique hors mission Arsenal** | **Hors périmètre.** Capacité distincte, exigeant un contrat propre (`Q2` §6.4). Voir §8. |

> **Pause et Reprise ne sont pas arbitrées** (`Q2` §6 in fine et §8). Leurs conditions restent celles du
> contrat [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §3.1 et **ne sont pas
> ouvertes par ce chantier**.

---

## 3. État factuel établi — inventaire d'entrée

Relevé par lecture directe du dépôt à `origin/main` = `3270291`, arbre propre. **Aucun de ces
fichiers n'est modifié par le présent acte.**

### 3.1 Allowlist réelle d'`ASP-CI-11` — **neuf fichiers**

Constituée dans `scripts/arsenal_contracts/check_aspirateur_contracts.py` par l'union de
`RUNTIME_FICHIERS`, des clés de `WRITERS_VERDICT` et de `LECTEURS_VERDICT` :

| # | Fichier | Rôle vis-à-vis du verdict |
|---|---|---|
| 1 | `10_scripts/aspirateur/lancer_mission.yaml` | runtime `L1` **et** écrivain `W1` |
| 2 | `04_input_texts/aspirateur/mission.yaml` | runtime `L1` (porteur du helper) |
| 3 | `12_template_sensors/aspirateur/etat_canonique.yaml` | runtime `L1` |
| 4 | `12_template_sensors/aspirateur/motif_lisible.yaml` | runtime `L1` |
| 5 | `12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml` | runtime `L1` |
| 6 | `10_scripts/aspirateur/conduire_mission.yaml` | écrivain `W2` |
| 7 | `11_automations/aspirateur/supervision_mission.yaml` | écrivain `W3` |
| 8 | `11_automations/aspirateur/notification_mission.yaml` | **lecteur pur nominatif** |
| 9 | `11_automations/aspirateur/remise_a_zero_composition.yaml` | **lecteur pur nominatif** (amendement `U0`) |

**Le précédent du lecteur pur nominatif est donc déjà constitué et déjà gardé** (deux occurrences,
n° 8 et 9) : la CI vérifie fichier par fichier que ces lecteurs **mentionnent** le verdict sans jamais
l'**écrire**, l'écriture restant au trio `W1`/`W2`/`W3` (`ASP-INV-86`). La projection décidée par `Q2`
s'inscrit dans ce précédent et ne crée pas de mécanisme nouveau.

### 3.2 Listes locales de valeurs de classe — recensement exhaustif

> **⚠️ Recensement RECTIFIÉ au Lot 2 — cinq entrées portées à SEPT.** La version d'ouverture de ce
> chantier dénombrait **cinq** représentations, établies par recherche de la clé littérale
> `verdict_ouvert` / `verdict_terminal`. Ce dénombrement était **incomplet**, et il l'était pour la
> raison que la version d'ouverture énonçait elle-même : *« une liste de classe portée sous un autre
> nom de clé ne serait pas capturée par cette recherche »*. **Deux telles représentations existent.**
> Le texte erroné est conservé au §3.2 bis, à côté de sa correction. Véhicule décidé le 2026-09-02
> (`H-6`) : rectification **sur place**, ce document étant **vivant** et non scellé sur un SHA — à la
> différence de `Q1`, `Q2` et des trois rapports historiques, qui restent **intacts**.

**Sept** représentations runtime embarquent une classe du verdict, ou un **sous-ensemble
contractuellement nommé** de classe. **Quatre** ne sont pas confrontées à égalité exacte :

| # | Fichier | Clé | Contenu | Confrontée à égalité exacte ? | Contrôle |
|---|---|---|---|---|---|
| 1 | `10_scripts/aspirateur/lancer_mission.yaml` | `verdict_ouvert` | 9 valeurs, classe `O`/`O-R` | **Oui** | `ASP-CI-16` |
| 2 | `11_automations/aspirateur/notification_mission.yaml` | `verdict_ouvert` | 9 valeurs | **Oui** | `ASP-CI-37` |
| 3 | `11_automations/aspirateur/notification_mission.yaml` | `verdict_terminal` | 8 valeurs, classe `T` | **Oui** | `ASP-CI-37` |
| 4 | `10_scripts/aspirateur/conduire_mission.yaml` | `verdict_ouvert` | 9 valeurs | **NON** | **aucun** — la clé n'est lue par aucun contrôle de contenu |
| 5 | `11_automations/aspirateur/supervision_mission.yaml` | `verdict_ouvert` | 9 valeurs | **NON** | `ASP-CI-18` ne teste que la **présence** de la clé dans une condition, jamais le **contenu** |
| 6 | `11_automations/aspirateur/supervision_mission.yaml` | **`engagements`** | 4 valeurs — **sous-ensemble strict de la classe `O`**, les engagements de W2 | **NON** | `ASP-CI-18` teste la seule **présence** de la clé. La constante `ENGAGEMENTS_W2` **existe** au checker, mais **n'est jamais confrontée** à la représentation runtime |
| 7 | `11_automations/aspirateur/notification_mission.yaml` | **`phrases`** (clés du mapping) | 9 clés — **exactement la classe `O`** | **NON** | **aucun** |

> **Constat d'entrée, inchangé quant au fond.** Les sept représentations sont aujourd'hui
> **matériellement exactes** — vérifié par exécution au HEAD. Ce n'est pas une garantie : c'est un
> état, et **quatre** d'entre elles peuvent dériver sans qu'aucun contrôle ne le voie. C'est
> exactement l'exigence 5 de `Q2` §7.2, désormais portée au contrat par **`ASP-INV-98`**
> ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2).

> **Portée du recensement, corrigée.** Il n'est plus établi par recherche d'une clé littérale — c'est
> précisément ce qui avait manqué les entrées 6 et 7 — mais par **lecture des variables déclarées**
> dans les fichiers du **périmètre nominatif du checker**, puis confrontation de chaque énumération au
> vocabulaire canonique. `ASP-INV-98` rend la règle **indifférente au nom de la clé** : elle suit
> l'**énumération**, jamais l'étiquette qui l'héberge.

### 3.2 bis Texte erroné du recensement, conservé

**Traçabilité de la rectification `H-6`** — l'écart reste lisible, il n'est pas effacé. Version
d'ouverture, au commit `28dc746` :

> **Quatre** listes `verdict_ouvert`, portant chacune les **neuf** valeurs de classe `O`/`O-R`, et
> **une** liste `verdict_terminal` portant la classe `T` […] Une liste de classe portée sous un
> **autre nom de clé** ne serait pas capturée par cette recherche.

**Nature de l'écart : dénombrement incomplet, et rien d'autre.** Aucun raisonnement de `C45` ne
dépendait du nombre : l'exigence invoquée est celle de `Q2` §7.2, qui porte sur **toute** liste, et
non sur un cardinal. Les lots, leurs dépendances et leurs conditions d'arrêt sont **inchangés** ; seul
le **périmètre du Lot 3 item 3.5** s'en trouve élargi, de deux représentations à quatre.

### 3.3 Producteur et lecteurs de l'attribut ambigu `mission_ouverte`

| Rôle | Emplacement | Nature |
|---|---|---|
| **Producteur** | `12_template_sensors/aspirateur/etat_canonique.yaml` (attribut du capteur d'état canonique) | Runtime — dérivé du **seul témoin natif de nettoyage** |
| **Contrat** | [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 — dixième état canonique, tableau et alinéa *« Mission ouverte est orthogonal »* (`ASP-INV-68`) | Normatif |
| **Contrat** | [`12`](../../../contrats/aspirateur/12_identifiants_a_fournir.md) §2.3 — rôle `‹etat_canonique›`, mention `‹mission_ouverte›` rendu séparément | Normatif |
| **Contrat** | [`11`](../../../contrats/aspirateur/11_frontiere_ui.md) §3 — *« **Mission ouverte** se superpose aux neuf autres et se rend **séparément** »* | Normatif |
| **CI** | `check_aspirateur_contracts.py` — constante de vocabulaire des dix états, constante d'état orthogonal, et contrôle `ASP-CI-23` | Mécanique |
| **UI** | `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` — **quatre** sites (§3.4) | Restitution |

### 3.4 Consommateurs UI concernés

Tous dans `18_lovelace/includes/cartes/aspirateur/panneau_operationnel.yaml` :

| Site | Ce qu'il fait aujourd'hui | Autorité correcte après `Q1`/`Q2` |
|---|---|---|
| **Tuile « Mission »** | Rend l'attribut natif sous les libellés `Ouverte` / `Aucune` / `Indisponible`, sous le nom **« Mission »** | **Deux restitutions distinctes** : la mission Arsenal, sur la **projection métier** ; la session physique, sur l'attribut renommé — libellés distincts (`Q1` §6.1) |
| **Condition d'affichage de la section « 🎛️ Conduite »** | Disjonction : état `nettoyage_reel` **ou** `pause` **ou** attribut natif `= oui` | **Projection métier** — la section de conduite Arsenal suit la mission Arsenal (`Q2` §6.1) |
| **Geste « Renvoyer à la base »** | Attribut natif `= oui` **et** état ∉ {`retour_base`, `amarrage`, `charge`} | **Projection métier** pour l'autorité ; les **trois exclusions physiques sont conservées** telles quelles (`Q2` §6.3) |
| **Geste « Arrêter la mission »** | Attribut natif `= oui` | **Projection métier seule** — l'offre d'Arrêt **cesse de dépendre du témoin natif** (`Q2` §6.2) |

Les conditions de **Pause** et de **Reprise** du même fichier sont **hors périmètre** (§8).

### 3.5 Navigation — inchangée, et c'est une décision

`12_template_sensors/system/cartes_dashboard_navigation/aspirateur.yaml` produit la couleur de la
tuile Aspirateur à partir de la **classe de partition physique** de l'état canonique et du témoin
d'entretien. **Il ne lit pas le verdict** et s'abstient explicitement sur indisponibilité. `Q2` §4
option **G** a été **écartée** : la navigation **reste adossée à l'activité physique**. Ce fichier
n'entre au périmètre du chantier que pour y être **prouvé non modifié**.

### 3.6 Invariants et contrôles en dépendance

| Référence | Ce qu'elle impose au chantier |
|---|---|
| `ASP-INV-87` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2) | Autorité unique de la mission Arsenal — la projection en dérive, ne s'y substitue pas |
| `ASP-INV-86` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §1) | Trois écrivains du verdict, et trois seulement — la projection n'en devient pas un quatrième |
| `ASP-INV-68` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1) | Orthogonalité et exposition séparée — à réécrire sous le nom exact décidé |
| `ASP-INV-45` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1) | L'indisponibilité est un état, pas un trou — la projection rend un **troisième régime explicite** |
| `ASP-INV-47` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §3) | Jamais une preuve de mouvement — le témoin natif ne conclut rien sur la mission |
| `ASP-INV-44` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1) | Aucune agrégation « occupé / libre » — deux objets, deux rendus |
| `ASP-INV-91` ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §3.2) | Un geste sans objet n'écrit rien — cohérent avec le retrait de l'offre |
| `ASP-INV-52` ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1, par analogie) | L'extension du vocabulaire est un **acte contractuel** — le renommage aussi |
| `ASP-CI-11` | Allowlist **nominative** — l'exception doit nommer un fichier, jamais un motif |
| `ASP-CI-16` | Étape 0a du moteur — arrêt sec gardé par la classe du verdict **avant toute écriture** ; c'est ce qui rend caduc l'en-tête de `notification_mission.yaml` (§4.2) |
| `ASP-CI-18` | Porte d'entrée de la supervision — sa garde teste la **présence** de la clé, pas le contenu de la liste (§3.2) |
| `ASP-CI-23` | Contrôle de l'attribut ambigu — suit le renommage |
| `ASP-CI-37` | Égalité exacte des deux ensembles de la projection persistante — **patron** à généraliser au Lot 3 |

---

## 4. Dettes documentaires préalables

> **Les deux dettes sont instruites et leurs préalables sont tranchés.** Le propriétaire d'Arsenal a
> rendu, le **2026-09-01**, la décision de **véhicule** pour `D1` (§4.1) et la décision de
> **qualification et de rattachement** pour `D2` (§4.2). **Aucune des deux ne reste une question
> ouverte** ; toutes deux sont désormais des **tâches d'exécution** affectées à un lot nommé — `D1` au
> **Lot 1**, `D2` au **Lot 2**. Aucune n'est exécutée par la passe d'ouverture.

### 4.1 D1 — « huit » contre neuf fichiers dans l'allowlist d'`ASP-CI-11`

**Fait.** Le document normatif `Q1`, §2 fait 8, écrit que l'allowlist compte **huit** fichiers. Elle en
compte **neuf** (§3.1). La même erreur figure, aux mêmes termes, dans deux **rapports historiques
scellés sur leur SHA** — la contre-expertise et la confrontation.

**Vérification du moment de l'écart.** L'amendement `U0`, qui a porté l'allowlist de huit à neuf, est
antérieur au SHA `31afb9f` auquel l'audit et la contre-expertise sont scellés, et antérieur au SHA
`5410629` auquel `Q1` est scellé. **Le compte était déjà de neuf lorsque chacun de ces documents a été
écrit** : il ne s'agit pas d'une péremption par évolution ultérieure du dépôt, mais d'un compte
inexact repris de proche en proche.

**Nature.** **Écart de décompte, et rien d'autre.** Aucun raisonnement de `Q1` ne dépend du nombre :
la doctrine invoquée est la **nominativité** de l'allowlist, pas son cardinal. `Q1` n'est ni affaibli
ni remis en cause. `Q2` §3 fait 7 **établit déjà le compte de neuf**, sourcé sur les trois constantes
du checker.

**Ce qui est acquis sans arbitrage :**

- les **rapports historiques** — audit, contre-expertise, confrontation — **ne sont pas retouchés**.
  Ils sont datés de leur SHA. `Q1` §4.4 et `Q2` §10 le posent explicitement ;
- le compte de **neuf** est le compte exact, et il est déjà écrit et sourcé en `Q2`.

#### Décision humaine rendue — véhicule de rectification (2026-09-01)

Le dépôt ne fournissait **pas de convention univoque** pour corriger ou annoter une **note
d'arbitrage rendue**, elle-même scellée sur un SHA. **Le propriétaire d'Arsenal a tranché ; la
décision est acquise et le véhicule n'est plus une option ouverte.**

> « Le « huit » figurant dans `Q1` est une **erreur factuelle de cardinal** ; la doctrine et
> l'arbitrage `Q1` restent **inchangés**.
>
> Véhicule retenu : une **rectification documentaire autonome et explicitement datée**, classée
> auprès des arbitrages Aspirateur selon la convention existante, **limitée à la correction factuelle
> « huit » → « neuf »**. Elle ne réécrit ni `Q1`, ni les rapports `A`/`B`, ni la confrontation. Elle
> **ne rend aucun nouvel arbitrage**. Elle cite `Q2` comme **établissement ultérieur du compte
> exact**. Elle **conserve la traçabilité** du texte erroné et de sa correction. »

**Propriétés opposables du véhicule retenu :**

| Propriété | Contenu |
|---|---|
| **Forme** | Document **autonome**. Ni annotation posée dans `Q1`, ni patch réécrivant sa cible. |
| **Datation** | **Explicitement datée**, comme acte distinct de `Q1` et de `Q2`. |
| **Classement** | Auprès des **arbitrages Aspirateur**, selon la convention existante — `02_arbitrages/aspirateur/`, aux côtés de `Q1` et `Q2`. **Le nom de fichier est attribué au Lot 1, pas ici.** |
| **Portée** | **Strictement limitée** au cardinal « huit » → « neuf ». Rien d'autre : aucune clause amendée, aucun constat requalifié, aucune sévérité officialisée. |
| **Statut normatif** | **Ne rend aucun nouvel arbitrage.** C'est un acte de rectification factuelle, pas un acte d'arbitrage. |
| **Sourcing** | Cite `Q2` §3 fait 7 comme **établissement ultérieur du compte exact**. |
| **Intangibilité des sources** | Ne réécrit **ni `Q1`**, **ni les rapports `A`/`B`**, **ni la confrontation**. |
| **Traçabilité** | **Conserve** le texte erroné **et** sa correction — l'écart reste lisible, il n'est pas effacé. |

> **Moment d'exécution — opposable.** La rectification est produite **dans le Lot 1 de `C45`**, et
> **jamais dans la passe d'ouverture du chantier**. À la passe d'ouverture, **le document de
> rectification n'existait pas encore**, et **aucune écriture n'a été faite** dans `Q1`, `Q2`, la
> confrontation ni les rapports historiques.

> **✅ Exécuté au Lot 1 — 2026-09-01.** La rectification existe :
> [`rectification_cardinal_allowlist_asp_ci_11.md`](../../02_arbitrages/aspirateur/rectification_cardinal_allowlist_asp_ci_11.md),
> classée dans `02_arbitrages/aspirateur/` aux côtés de `Q1` et `Q2`, **datée**, **limitée** au
> cardinal « huit » → « neuf », **citant `Q2` §3 fait 7**, et **conservant** le texte erroné à côté
> de sa correction. Elle **ne rend aucun arbitrage**. `Q1`, `Q2` et les trois rapports historiques
> sont **prouvés inchangés**. **La décision ci-dessus n'est ni amendée ni rouverte par ce constat
> d'exécution.**

### 4.2 D2 — en-tête périmé de `11_automations/aspirateur/notification_mission.yaml`

**Fait.** Le bloc *« 🕳️ CE QUE LE `choose` NE COUVRE PAS »*, alinéa *« CONSÉQUENCE ASSUMÉE, ÉCRITE
PLUTÔT QUE MASQUÉE »*, déclare comme défaut assumé et non corrigeable la perte de la mémoire de
mission lorsque le moteur est appelé sur une mission déjà ouverte. **L'étape 0a de
`10_scripts/aspirateur/lancer_mission.yaml` s'arrête avant toute écriture** dans ce cas, et
`ASP-CI-16` rend cette propriété **opposable en CI**. Le texte décrit donc un défaut refermé.

**Identifiant.** Ce fait est déjà consigné sous `AUD-ASP-04` dans l'audit de conformité du domaine, où
il figure comme **constat proposé**. La décision ci-dessous en tranche la **qualification** et le
**rattachement à un lot** ; elle ne le **ferme pas** — voir §6.

#### Décision humaine rendue — qualification et rattachement (2026-09-01)

La doctrine documentaire d'Arsenal pose que **l'en-tête de fichier vaut contrat local**
([`entetes_fichiers.md`](../../../architecture/03_doctrines/entetes_fichiers.md)). Le propriétaire
d'Arsenal a tranché sur ce fondement, et **la question de rattachement est close**.

> « L'en-tête de fichier est un **contrat local** selon la doctrine documentaire d'Arsenal. Le
> scénario périmé de `notification_mission.yaml` constitue donc une **dette contractuelle locale**, et
> **non une simple correction rédactionnelle opportuniste**.
>
> `D2` est rattachée au **Lot 2 de propagation contractuelle**. Sa correction intervient **après
> l'alignement des contrats canoniques concernés** et **dans la même séquence normative**. Elle
> **précède** les modifications du checker et du comportement runtime. `AUD-ASP-04` **n'est pas fermé**
> par cette seule qualification ; sa fermeture exigera la **correction effective**, sa **cohérence avec
> les contrats canoniques** et les **validations documentaires applicables**. »

**Conséquences opposables :**

| Point | Contenu |
|---|---|
| **Nature** | **Dette contractuelle locale**, non rédactionnelle. La question de contre-vérification `C-7` de l'audit est ainsi **tranchée dans le sens contractuel** : l'en-tête vaut contrat local, son réalignement est un acte normatif. |
| **Lot** | **Lot 2**, et lui seul. Le rattachement au **Lot 3 est écarté** : le Lot 3 ne porte plus `D2`. |
| **Rang dans le lot** | **Après** l'alignement des contrats canoniques `08`, `11`, `12` et `15` — un contrat local ne peut être aligné que sur des contrats canoniques déjà alignés — et **dans la même séquence normative**, non dans une passe séparée. |
| **Antériorité** | **Précède** toute modification du checker (Lot 3) et tout changement de comportement runtime (Lots 4 à 6). |
| **Effet sur `AUD-ASP-04`** | **Aucune fermeture par la seule qualification.** Conditions cumulatives au §6. |

**Contrainte de la passe d'ouverture.** `11_automations/aspirateur/notification_mission.yaml` **n'est
pas modifié** par le présent acte : sa correction appartient au **Lot 2**, item 2.11.

---

## 5. Lots

**Convention de nommage.** Les lots sont **numérotés** (`Lot 1` … `Lot 7`), sur le modèle des chantiers
`C20` et `ECS-DESINF-VAC`. Ils ne reçoivent **pas** de lettre de lot du domaine : les familles `M`,
`L`, `N` et `U` sont celles du cadrage ratifié `D-44`, et en ouvrir une nouvelle serait **attribuer un
identifiant** que ni `Q1` ni `Q2` n'ont décidé.

### 5.1 Lot 1 — Régularisation documentaire préalable — **EXÉCUTÉ (2026-09-01)**

> **État : exécuté.** Items **1.1**, **1.2** et **1.3** faits. La rectification `D1` est
> [`rectification_cardinal_allowlist_asp_ci_11.md`](../../02_arbitrages/aspirateur/rectification_cardinal_allowlist_asp_ci_11.md),
> indexée en section *Arbitrages / Aspirateur* de [`index.md`](../../index.md), la ligne `C45`
> du [`registre`](../../REGISTRE_CHANTIERS.md) étant mise à jour **au même commit**. **Aucun
> arbitrage rendu, aucun identifiant attribué, aucune source historique réécrite, et ni
> `notification_mission.yaml`, ni contrat, ni checker, ni runtime, ni Lovelace touché.**

| Item | Contenu |
|---|---|
| **1.1** | **Produire** la **rectification documentaire autonome et explicitement datée** de la dette **D1**, conforme au véhicule **décidé** au §4.1 : classée dans `02_arbitrages/aspirateur/` aux côtés de `Q1` et `Q2`, **limitée** au cardinal « huit » → « neuf », citant `Q2` §3 fait 7 comme établissement ultérieur du compte exact, et **conservant la traçabilité** du texte erroné et de sa correction. Le **nom de fichier** est attribué à ce lot. |
| **1.2** | **Indexer** la rectification selon la convention de navigation — section *Arbitrages / Aspirateur* de [`index.md`](../../index.md) — et mettre à jour la ligne `C45` du [`registre`](../../REGISTRE_CHANTIERS.md) **au même commit** (règle de co-commit du registre). |
| **1.3** | **Ne réécrire ni `Q1`, ni `Q2`, ni les rapports `A`/`B`, ni la confrontation.** Ce lot **ne rend aucun arbitrage** : il exécute une décision déjà rendue. |
| **Ne fait pas** | Ne touche **ni** `notification_mission.yaml` — dette **D2** portée par le **Lot 2** (§4.2) —, **ni** aucun contrat, **ni** aucun checker, **ni** aucun runtime, **ni** Lovelace. |
| **Preuve** | Le document de rectification existe, est daté, est classé et est indexé ; le cardinal **neuf** est exact partout où il est affirmé hors documents scellés ; **`git diff` vide** sur `Q1`, `Q2`, l'audit, la contre-expertise et la confrontation ; gates documentaires vertes. |

### 5.2 Lot 2 — Propagation contractuelle — **EXÉCUTÉ (2026-09-02)**

**Aucun code avant ratification de ce lot.** C'est la contrainte d'ordre de `Q1` §4.4 et `Q2` §10.

> **État : exécuté.** Items **2.1** à **2.9** faits dans les chapitres `08`, `11`, `12` et `15` ;
> item **2.10** déclaré **sans objet** (décision `H-7`) ; item **2.11** — dette `D2` — fait **après**
> eux, **dans la même séquence normative**, **en commentaire seul**. **Aucun identifiant technique
> n'est écrit dans les contrats** (`ASP-INV-58`) : la projection y est désignée par le **rôle**
> `‹projection_mission_arsenal_ouverte›`. **Checker Aspirateur vert et inchangé**, **aucun Lovelace
> touché**, **aucune ligne exécutable de runtime touchée**, **aucun changelog créé**.

#### Décisions humaines rendues — préalables au lot (2026-09-02)

Huit décisions ont été rendues par le propriétaire d'Arsenal avant exécution. **Aucune n'est un
arbitrage nouveau** : elles tranchent des points que `Q1` et `Q2` avaient explicitement laissés hors
arbitrage, ou que ce chantier avait laissés ouverts.

| Réf. | Objet | Décision |
|---|---|---|
| `H-1` | Identifiant de la projection métier | **Attribué.** N'est **pas** écrit au contrat — employé au Lot 4 |
| `H-2` | Nouveau nom de l'attribut de session | **Attribué.** N'est **pas** écrit au contrat — employé au Lot 5 |
| `H-3` | **Rang du renommage du code technique** | **Lot 5** — voir l'encadré ci-dessous |
| `H-4` | Invariants nouveaux | **`ASP-INV-96`** (ch. `08`), **`ASP-INV-97`** et **`ASP-INV-98`** (ch. `15`). L'interdiction faite à Lovelace reste une **ligne du tableau des interdits** du ch. `11`, sans invariant |
| `H-5` | Périmètre de l'exigence 5 de `Q2` §7.2 | **Couvre** les représentations portées sous un autre nom de clé, et les **sous-ensembles contractuellement nommés** — d'où la rédaction d'`ASP-INV-98` |
| `H-6` | Véhicule de rectification du §3.2 | **Sur place, au Lot 2**, ce document étant vivant. Texte erroné **conservé** au §3.2 bis |
| `H-7` | Registre de couverture (item 2.10) | **Sans objet** : le lot ne crée ni checker, ni workflow, ni chapitre |
| `H-8` | Vocabulaire de valeurs de l'attribut | **Conservé tel quel.** Seul le **nom** change, au Lot 5 |

> **⚠️ `H-3` — contradiction interne du présent chantier, tranchée.** L'item **2.2** plaçait le
> renommage du **code technique** au Lot 2 ; l'item **5.2** plaçait les contrats `08`, `11` et `12`
> dans le **mouvement atomique du Lot 5**. Les deux ne pouvaient être vrais ensemble.
>
> **Fait établi par exécution.** Le contrôle `ASP-CI-9` lit le chapitre `08` §1 et confronte les codes
> qu'il y trouve à une **constante figée du checker**. Renommer le code dans le contrat **sans**
> toucher le checker rend `ASP-CI-9` **rouge** — deux écarts : code attendu absent, code inconnu
> ajouté. Or le Lot 2 exige un checker **vert et inchangé**, et le Lot 3 vient **après**.
>
> **Décision rendue : le code technique bascule au Lot 5**, avec la constante du checker et les quatre
> sites Lovelace, **en un seul mouvement**. Le Lot 2 aligne le **libellé contractuel** et la
> **sémantique**, ce qui laisse `ASP-CI-9` vert — vérifié.
>
> **L'item 2.2 est lu en conséquence**, et l'item 5.2 prime sur lui. `Q2` §7.1.5 est **respecté** :
> « le nom contractuel et le nom technique changent **ensemble**, en une seule fois » impose
> l'**atomicité** du mouvement, non son rang. L'état transitoire — libellé aligné, code encore
> ancien — est **écrit au contrat** ([`08`](../../../contrats/aspirateur/08_etats_et_observation.md)
> §1.3), et il n'ouvre **aucune** coexistence de deux noms : il n'y a toujours qu'**un seul** code
> pour cet état.

| Item | Contenu |
|---|---|
| **2.1** | Inscrire au vocabulaire canonique les **deux notions sous deux noms distincts** — mission Arsenal ouverte / session robot active — et **leurs autorités respectives**. |
| **2.2** | Amender [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1 : le dixième état est **renommé**. **Décision `H-3`** — le **libellé contractuel** et la sémantique sont alignés **ici** ; le **code technique** bascule au **Lot 5**, avec la constante du checker et les quatre sites Lovelace, **en un seul mouvement** (`Q2` §7.1.5 : l'atomicité porte sur le mouvement, non sur son rang). `ASP-INV-68` réécrit sous le libellé retenu, sa proposition de **totalité sur la partition** restant intacte. **✅ Fait** — §1 table, §1.1, §1.2, §1.3. |
| **2.3** | Reconnaître au contrat la **projection métier dédiée** : source **exclusive** (classe `O`, `O-R` comprise), **statut de lecteur pur** sans droit d'écriture, **disponibilité et régime d'indisponibilité** explicites (`ASP-INV-45`), et **fraîcheur** — définis **contractuellement avant tout code**. |
| **2.4** | Porter au contrat l'**exception nominative** à `ASP-CI-11` : elle **nomme un fichier**, jamais un motif, une famille ni un répertoire. |
| **2.5** | Rendre opposable, au chapitre [`11`](../../../contrats/aspirateur/11_frontiere_ui.md), l'**interdiction faite à Lovelace de lire directement le helper de verdict** : l'UI consomme la projection. Aligner le §3 du même chapitre sur le nouveau nom. |
| **2.6** | Inscrire au chapitre [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) les **règles d'offre** des gestes (§2.3) : Arrêt indépendant du témoin natif ; Retour base et ses trois exclusions de sens physique ; **disparition à la sortie de classe `O`** ; **exclusion des missions externes**, écrite comme **propriété voulue** et non comme effet de bord d'une condition d'affichage. |
| **2.7** | Aligner [`12`](../../../contrats/aspirateur/12_identifiants_a_fournir.md) §2.3 sur le renommage, et déclarer le **rôle** de la projection sans lui attribuer d'identifiant (`ASP-INV-58` — le contrat n'en propose aucun). |
| **2.8** | Poser au contrat que la **divergence des deux notions n'est plus un défaut** (`Q1` §5.4). |
| **2.9** | Poser au contrat que la **navigation reste adossée à l'activité physique** (`Q2` §5.10). |
| **2.10** | Mettre à jour le **registre de couverture de vérification** si le lot crée un contrôle ou un chapitre, selon la règle appliquée aux lots `M0` et `L2` du cadrage `D-44`. |
| **2.11** | **Dette `D2`** (§4.2) — corriger l'**en-tête périmé** de `11_automations/aspirateur/notification_mission.yaml`. Le bloc *« CONSÉQUENCE ASSUMÉE, ÉCRITE PLUTÔT QUE MASQUÉE »* est réaligné sur l'état réel : le scénario qu'il déclare non corrigeable est refermé par l'**étape 0a** du moteur et rendu **opposable** par `ASP-CI-16`. **Rang opposable** : **après** les items 2.2 à 2.9 — un contrat local s'aligne sur des contrats canoniques déjà alignés — **dans la même séquence normative**, et **avant** toute modification du checker (Lot 3) ou du runtime (Lots 4 à 6). **Commentaire seul.** |
| **Ne fait pas** | **N'attribue aucun identifiant technique** : ni nom d'entité, ni nom d'attribut de remplacement, ni numéro d'invariant CI. Ces choix appartiennent au propriétaire et sont **exclus de l'arbitrage** par `Q2` §8. **Ne modifie aucune ligne exécutable de runtime** : la seule touche runtime admise dans ce lot est le **bloc d'en-tête** de l'item 2.11. Aucun checker, aucun Lovelace. |
| **Preuve** | Les deux notions sont nommées séparément dans les chapitres `08`, `11`, `12` et `15` ; aucune clause ne lit plus la coexistence comme une incohérence ; l'en-tête de `notification_mission.yaml` est **cohérent** avec les contrats canoniques alignés et avec `ASP-CI-16` ; **checker Aspirateur vert et inchangé** ; `git diff` limité aux contrats et au **seul bloc de commentaires** de l'item 2.11 — aucune ligne exécutable, aucun Lovelace. |

### 5.3 Lot 3 — Extension CI

**Dépend de la ratification du Lot 2.** Le checker ne peut garder que ce que le contrat a écrit.
**Ce lot ne porte pas la dette `D2`** : elle est rattachée au Lot 2 par décision rendue (§4.2).

| Item | Contenu |
|---|---|
| **3.1** | Ajouter la projection à l'**exception nominative de lecture** d'`ASP-CI-11`, et **prouver** la propriété « lit le verdict, ne l'écrit jamais », comme elle l'est déjà pour les deux lecteurs purs existants (§3.1). |
| **3.2** | **Nominativité préservée** — refuser toute autorisation par motif, famille ou répertoire. |
| **3.3** | **Aucune lecture directe par Lovelace** : l'interdiction faite aux arbres Lovelace de mentionner le helper doit rester **mécaniquement** garantie **après** l'ajout de l'exception. C'est une **non-régression**, à prouver dans les deux sens. |
| **3.4** | **Source exclusive** : prouver que la projection ne fait intervenir **aucun** témoin natif — ni état machine, ni témoin de session, ni entité `vacuum`. |
| **3.5** | **Égalité exacte des représentations de classe** — désormais opposable par **`ASP-INV-98`** ([`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §2). Étendre le patron `ASP-CI-37` aux **QUATRE représentations non gardées** du §3.2 rectifié : `verdict_ouvert` du script de conduite · `verdict_ouvert` de la supervision · **`engagements`** de la supervision, sous-ensemble nommé de la classe `O` · **clés de `phrases`** de la projection, énumération exacte de la classe `O`. Le recensement s'établit **par lecture des variables déclarées** dans le périmètre nominatif du checker, **jamais** par recherche d'une clé littérale — c'est précisément ce qui avait manqué les deux dernières. |
| **3.6** | **Indisponibilité non rabattue** : refuser une projection faisant valoir `false` à `unknown`, `unavailable` ou à une valeur hors vocabulaire. |
| **3.7** | **Reliquats de l'ancien nom — DEUX RÉGIMES MÉCANIQUES SUCCESSIFS.** Le contrôle ne peut pas exiger zéro occurrence dès le Lot 3 : la décision `H-3` **autorise** l'ancien code jusqu'au mouvement atomique du Lot 5. Il doit néanmoins être **immédiatement actif et utile**, sans prétendre que la migration a déjà eu lieu.<br><br>**① Régime transitoire — livré au Lot 3, actif dès le Lot 3.** Contrôle **actif** des occurrences de l'ancien nom, adossé à une **allowlist transitoire fermée et nominative** énumérant les occurrences **encore autorisées** — celles qui existent au HEAD du Lot 2, et elles seules. **Rouge** : toute occurrence **supplémentaire**, toute occurrence **hors allowlist**, et **toute apparition prématurée du nouveau code** avant le Lot 5. Ce régime **ne crée aucun alias** et **aucune double exposition runtime** : il n'autorise pas un second nom, il **gèle** la population du premier.<br><br>**② Régime permanent — activé au Lot 5, dans le mouvement atomique.** **Suppression** de l'allowlist transitoire, **activation** de la règle permanente exigeant **zéro occurrence** de l'ancien nom dans **tout le périmètre gouverné**, et **suppression obligatoire** de la clause transitoire du chapitre [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) §1.3. La bascule entre les deux régimes est **livrée dans le même commit** que la migration (§5.5).<br><br>**Preuve du Lot 3** : mutation rouge sur chacun des trois refus du régime ① — une occurrence ajoutée, une occurrence déplacée hors allowlist, une apparition anticipée du nouveau code. **Preuve du Lot 5** : recherche d'absence à **zéro occurrence**, allowlist transitoire **absente du checker**, clause `08` §1.3 **absente du contrat**. |
| **3.8** | **Offre des gestes** confrontée à la règle du §2.3, y compris l'**indépendance d'Arrêt** à l'égard du témoin natif. |
| **Ne fait pas** | **N'attribue aucun numéro d'invariant CI dans ce document.** Le plus haut `ASP-CI-*` constaté au dépôt est `ASP-CI-42` ; le numéro du ou des contrôles neufs sera attribué au lot, jamais ici. |
| **Preuve** | Contrôles neufs verts ; **mutations rouges** sur chacun — une liste amputée, une liste enrichie, une lecture Lovelace du helper, un rabattement d'indisponibilité sur `false`, un reliquat de l'ancien nom ; auto-test du checker étendu, aucun contrôle existant affaibli. |

### 5.4 Lot 4 — Implémentation de la projection métier

**Dépend de la ratification du Lot 2 et de la livraison du Lot 3.**

| Item | Contenu |
|---|---|
| **4.1** | Créer la projection métier — **lecteur pur**, dérivée de la **seule** appartenance du verdict à la classe `O` (`O-R` comprise). |
| **4.2** | Rendre le **troisième régime explicite** d'indisponibilité, conformément à `ASP-INV-45` et au §2.3 du contrat amendé. |
| **4.3** | Inscrire le fichier à l'exception nominative livrée au Lot 3. |
| **Ne fait pas** | **Le nom technique n'est ni inventé ni proposé ici** : aucun précédent du dépôt ne le détermine, et `Q2` §8 l'exclut explicitement de l'arbitrage. Il sera proposé au moment du lot, par le propriétaire. |
| **Preuve** | La projection existe, ne lit que le verdict, n'écrit rien ; les trois régimes — mission ouverte, pas de mission, indisponible — sont distincts et observables. |

### 5.5 Lot 5 — Migration atomique de l'attribut ambigu

**Un seul mouvement.** `Q2` §5.6 et §5.7 : l'attribut est **renommé**, pas dupliqué ; **aucune
coexistence des deux noms n'est admise, fût-elle transitoire**.

| Item | Contenu |
|---|---|
| **5.1** | Remplacer le nom chez le **producteur** — `12_template_sensors/aspirateur/etat_canonique.yaml`. |
| **5.2** | Remplacer le nom chez **tous les porteurs** recensés au §3.3 et §3.4, **dans le même mouvement**. **Décision `H-3`** : le **code technique** du chapitre `08` §1, laissé inchangé par le Lot 2, bascule **ici**. Inventaire **nominatif et exhaustif** de ce qui change :<br><br>**Contrats** — `08` §1 (code du dixième état) · `11` · `12`. **Interface** — les **quatre sites** Lovelace du §3.4. **Runtime** — le producteur, `12_template_sensors/aspirateur/etat_canonique.yaml`, **corps et en-tête**.<br><br>**Checker**, et pas seulement ses constantes — quatre porteurs, tous nommés : ① la **constante de vocabulaire** des dix états et ② la **constante d'état orthogonal**, que `ASP-CI-9` et `ASP-CI-23` lisent ; ③ le **commentaire d'en-tête** du module et le **commentaire de la constante**, qui énoncent l'un et l'autre l'ancien nom ; ④ les **deux messages d'erreur d'`ASP-CI-23`** qui le citent littéralement. Un renommage qui ne toucherait que les constantes laisserait le module **décrire un nom qui n'existe plus** — l'en-tête vaut contrat local.<br><br>**Contrat, enfin** : la **clause d'état transitoire** du chapitre [`08`](../../../contrats/aspirateur/08_etats_et_observation.md) **§1.3** est **retirée par ce lot**, l'écart qu'elle décrit cessant d'exister ; et l'**allowlist transitoire** du Lot 3 item 3.7 est **supprimée**, son régime permanent activé.<br><br>**Preuve** : recherche d'absence de l'ancien nom rendant **zéro occurrence** sur **tout le périmètre gouverné** — contrats, runtime, interface **et checker, commentaires compris**. |
| **5.3** | **Aucune compatibilité silencieuse permanente** : ni alias, ni double exposition, ni repli sur l'ancien nom. |
| **Ne fait pas** | Ne modifie **pas la dérivation** de l'attribut : il continue de dériver du **seul témoin natif**. Seul son **nom** change — le nom devient exact, la sémantique était déjà celle-là. |
| **Preuve** | Recherche d'absence de l'ancien nom sur **tout** le dépôt gouverné, rendant zéro occurrence ; contrôle 3.7 vert ; aucun commit intermédiaire où les deux noms coexistent. |

### 5.6 Lot 6 — Adaptation de l'interface

**Dépend des Lots 4 et 5.**

| Item | Contenu |
|---|---|
| **6.1** | La **section Mission** et les **gestes de conduite** se fondent sur la **projection métier**. |
| **6.2** | La **navigation** et le rendu de l'**état physique** restent fondés sur la **session robot** — fichier de navigation **inchangé** (§3.5). |
| **6.3** | **Libellés distincts** pour les deux notions (`Q1` §6.1) : ce qui est rendu comme mission Arsenal ne porte pas le libellé de ce qui est rendu comme session physique. |
| **6.4** | **Arrêt** : offert pendant toute la classe `O`, **sans condition sur le témoin natif**. |
| **6.5** | **Retour base** : offert pendant la classe `O`, **sauf** `retour_base`, `amarrage`, `charge` — les trois exclusions existantes sont **conservées telles quelles**. |
| **6.6** | **Mission externe** : aucun geste de conduite Arsenal exposé. |
| **6.7** | **Aucun bouton présenté puis ignoré** : la condition d'affichage et la garde d'acceptation du backend doivent coïncider. C'est la levée effective de `RC-02`. |
| **Ne fait pas** | Ne touche **ni Pause ni Reprise** (§8). Ne crée **aucun** contrôle physique pour missions externes ou états post-terminaux (§8). |
| **Preuve** | Les quatre sites du §3.4 lisent la bonne autorité ; aucune mention du helper de verdict dans les arbres Lovelace (contrôle 3.3) ; scénarios statiques du Lot 7. |

### 5.7 Lot 7 — Vérification et clôture

| Item | Contenu |
|---|---|
| **7.1** | **Gates documentaires** : lint documentaire, gates `DOC-CI-*`, contrôle structurel du registre des chantiers. |
| **7.2** | **Checker Aspirateur** vert, batterie d'auto-test étendue, **aucun contrôle existant affaibli**. |
| **7.3** | **Recherches d'absence** : ancien nom d'attribut — zéro occurrence ; mention du helper de verdict hors des fichiers de l'allowlist — zéro occurrence. |
| **7.4** | **Scénarios statiques** — dérivés des deux combinaisons du noyau causal (`Q2` §6.5) : **(a) sur-offre** — verdict hors classe `O`, témoin natif actif (mission lancée depuis l'application constructeur) : **aucun geste Arsenal proposé** ; **(b) sous-offre** — verdict de classe `O`, témoin natif `off` (retour au dock) : **Arrêt proposé**, **Retour base exclu par le seul motif de sens physique**. |
| **7.5** | **Scénarios terrain réellement nécessaires** — à établir au lot, **restreints à ce que la preuve statique ne peut pas atteindre**, et **distincts de ceux de `C42`** (§7). |
| **7.6** | **Conditions de fermeture** des trois constats (§6). |

---

## 6. Conditions de fermeture de `AUD-ASP-01`, `CC-01` et `RC-02`

Les trois constats forment **un seul noyau causal** et ne sont **pas additionnables comme trois
écarts**. **Aucun n'est fermé par l'ouverture de ce chantier.** Ils ne sont pas non plus fermés par la
seule livraison d'un lot.

| Constat | Substance | Conditions **cumulatives** de fermeture |
|---|---|---|
| `AUD-ASP-01` · `CC-01` | Double sémantique sous un nom unique — le backend garde sur le verdict, l'interface sur le témoin de session | **(1)** Lot 2 ratifié : deux notions, deux noms, deux autorités inscrits au contrat · **(2)** Lot 5 livré : migration atomique achevée, **zéro occurrence** de l'ancien nom · **(3)** Lot 3 item 3.7 vert et **mutation rouge** démontrée · **(4)** aucun document normatif du domaine n'emploie plus le nom ambigu |
| `RC-02` | Divergence de prédicat entre l'affichage et la garde d'acceptation du backend | **(1)** Lot 4 livré : la projection existe et est gardée · **(2)** Lot 6 livré : les quatre sites lisent l'autorité correcte · **(3)** Lot 3 items 3.3 et 3.8 verts · **(4)** **scénarios statiques 7.4 (a) et (b) passés** · **(5)** aucun bouton présenté puis refusé par le backend |

> **Ce que l'ouverture ne fait pas.** Aucune sévérité n'est officialisée. Aucun constat n'est
> requalifié. Aucun constat n'est clos.

**`AUD-ASP-04` — conditions cumulatives de fermeture.** La décision du §4.2 le **qualifie** — dette
contractuelle locale — et le **rattache** au Lot 2. Elle **ne le ferme pas**. Sa fermeture exige, de
façon cumulative :

1. la **correction effective** de l'en-tête, livrée au **Lot 2 item 2.11** ;
2. sa **cohérence avec les contrats canoniques** `08`, `11`, `12` et `15` tels qu'alignés aux items
   2.2 à 2.9, et avec `ASP-CI-16` qui rend la propriété opposable ;
3. les **validations documentaires applicables** vertes.

Aucune de ces trois conditions n'est satisfaite par la seule qualification, ni par la seule ouverture
du chantier.

---

## 7. Articulation avec `C42` — sans double comptage

`C42` (*Aspirateur — déclaration d'entretien et écran dédié, lot `M2`*) **reste ouvert et inchangé**.
Son objet propre n'est **ni transféré, ni renuméroté, ni réécrit** par ce chantier.

| Reste à `C42`, et à lui seul | Appartient à `C45` |
|---|---|
| Validations terrain du parcours **Entretien** | Propagation contractuelle de `Q1`/`Q2` |
| Effet réel de la pression sur le micrologiciel ; valeur remontée après remise à zéro | Projection métier dédiée et son statut de lecteur pur |
| **Délai de propagation** | Migration atomique de l'attribut ambigu |
| **Disparition de la notification** d'entretien | Règles d'offre des gestes de conduite |
| **Effet réel des commandes** de déclaration d'entretien | Extension CI — égalité exacte des listes de classe |
| Étiquette **`script:execution`** au registre d'entités | Adaptation UI de la section Mission et des gestes |
| Autres validations déjà inscrites à son périmètre | Preuves de clôture **du présent** chantier |

**Règle de non-double-comptage.** Une preuve terrain déjà due à `C42` **ne peut pas** être invoquée
comme preuve de clôture de `C45`, et réciproquement. Le Lot 7 item 7.5 doit **nommer** ses scénarios
terrain et **établir qu'aucun n'est déjà porté par `C42`**. Les deux chantiers touchent le même
domaine et, en partie, le même panneau Lovelace : **la seule articulation admise est un ordre de
passage**, jamais un partage de preuve.

---

## 8. Hors périmètre — explicitement

| Objet | Motif |
|---|---|
| **Conditions de Pause et de Reprise** | Non arbitrées (`Q2` §6 in fine et §8). Restent celles de [`15`](../../../contrats/aspirateur/15_conduite_et_supervision.md) §3.1. |
| **Contrôle physique du robot hors mission Arsenal** — mission externe, état post-terminal | **Capacité distincte**, exigeant un **contrat propre** (`Q2` §6.4). **N'est pas créée** par `Q2` et n'est pas ouverte ici. |
| **Coloration et composition de la tuile de navigation** | `Q2` §4 option **G écartée** : la navigation **reste** adossée à l'activité physique. Le fichier n'entre au périmètre que pour être prouvé **non modifié**. |
| **Questions `Q3` à `Q8`** de la confrontation, et **`P1` à `P9`** en attente de preuve ou de terrain | Restent ouvertes. Non instruites ici. |
| **`QO-1` à `QO-6`**, `ARB-1`, `ARB-2`, `ARB-4` du chapitre [`13`](../../../contrats/aspirateur/13_hors_perimetre_arbitrages_et_questions_ouvertes.md) | Déjà déclarés ouverts par ailleurs. Non requalifiés. |
| **Toute dette de `C42`** | Voir §7. Aucun transfert. |
| **Clôture du domaine `aspirateur`** | Aucun état de clôture n'est modifié, ni par l'ouverture, ni par un lot pris isolément. |
| **Réécriture des rapports historiques, de `Q1` et de `Q2`** | Scellés sur leur SHA (`Q1` §4.4, `Q2` §10). **La décision `D1` du §4.1 l'exclut expressément** : la rectification est un document **autonome** ; elle ne réécrit aucune de ses sources. |
| **Changelog** | Non exigé à ce stade (doctrine [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1 — artefact de release). |

---

## 9. Dépendances entre lots

```
Lot 1  (régularisation documentaire)  ──┐
                                        ├─►  Lot 2  (propagation contractuelle)   ── RATIFICATION
                                        │         │
                                        │         ├─►  Lot 3  (extension CI)
                                        │         │         │
                                        │         │         ├─►  Lot 4  (projection métier)
                                        │         │         │         │
                                        │         │         │         ▼
                                        │         │         └─────►  Lot 5  (migration atomique)
                                        │         │                       │
                                        │         │                       ▼
                                        │         └────────────────►  Lot 6  (adaptation UI)
                                        │                                 │
                                        └─────────────────────────────────┴─►  Lot 7  (vérification, clôture)
```

**Règles d'ordre, opposables :**

1. **Aucun code avant la ratification du Lot 2.** Contrainte d'ordre de `Q1` §4.4 et `Q2` §10.
2. **Le Lot 3 précède le Lot 4** : le contrôle existe avant l'objet qu'il garde, faute de quoi
   l'exception nominative serait une **autorisation dormante**.
3. **Le Lot 5 est indivisible** : producteur, contrats, checker et interface basculent dans le
   **même mouvement**. Un lot 5 fractionné **viole** `Q2` §5.7.
4. **Le Lot 6 suit les Lots 4 et 5** : l'UI ne peut consommer une projection qui n'existe pas, ni
   lire un attribut au nom qui n'est plus le sien.
5. **La dette `D2` est portée par le Lot 2** (§4.2, décision rendue) : **après** l'alignement des
   contrats canoniques, **dans la même séquence normative**, et **avant** toute modification du
   checker ou du runtime. **Le Lot 3 ne la porte pas.**
6. **La dette `D1` est portée par le Lot 1** (§4.1, décision rendue) et n'est **pas** un préalable
   d'arbitrage : le véhicule est acquis, le Lot 1 l'exécute.

---

## 10. Conditions d'arrêt et critères GO/NO-GO

### 10.1 Conditions d'arrêt — le chantier s'interrompt sans écriture si

| # | Condition |
|---|---|
| A1 | La rectification **`D1`** ne pourrait être produite **sans réécrire** `Q1`, `Q2` ou un rapport scellé, ou **sans excéder** le cardinal « huit » → « neuf » : arrêt — le véhicule décidé au §4.1 l'interdit, et l'outrepasser rouvrirait un arbitrage rendu. |
| A2 | Un **identifiant technique** — entité, attribut, invariant, automation, fichier — serait à **inventer** faute de décision du propriétaire. Le chantier s'arrête et **demande la décision** ; il n'invente pas. |
| A3 | Le Lot 5 ne peut pas être exécuté **en un seul mouvement** : il est **suspendu**, jamais fractionné. |
| A4 | Une **égalité exacte** de liste de classe (item 3.5) révèle une **divergence réelle** entre deux listes : le chantier s'arrête et **qualifie la divergence** avant de la corriger — une liste qui diverge peut être la **bonne**. |
| A5 | Une preuve invoquée pour `C45` se révèle **déjà due à `C42`** : arrêt, et requalification, sans double comptage (§7). |
| A6 | L'ajout de l'exception nominative **affaiblit** l'interdiction faite à Lovelace (item 3.3) : arrêt immédiat, l'exception est refusée en l'état. |
| A7 | L'item 2.11 (**`D2`**) devrait être exécuté **avant** l'alignement des contrats canoniques, **après** une modification du checker ou du runtime, ou en touchant une **ligne exécutable** : arrêt — le rang et la portée décidés au §4.2 sont opposables. |

### 10.2 GO / NO-GO par lot

| Lot | **GO** si | **NO-GO** si |
|---|---|---|
| **1** | La rectification **`D1`** est produite conforme au véhicule décidé — autonome, datée, classée auprès des arbitrages Aspirateur, limitée au cardinal, citant `Q2`, traçabilité du texte erroné **conservée** — puis indexée | Elle réécrirait `Q1`, `Q2`, un rapport `A`/`B` ou la confrontation ; ou elle rendrait un **arbitrage** ; ou elle **excéderait** la correction du cardinal ; ou elle **effacerait** le texte erroné au lieu d'en conserver la trace |
| **2** | Les contrats sont amendés **sans qu'aucun identifiant technique soit attribué**, la sémantique des deux notions est intégralement inscrite, et l'en-tête de `notification_mission.yaml` (**`D2`**, item 2.11) est réaligné **après** eux, **avant** tout checker ou runtime, **en commentaire seul** | Un chapitre resterait en contradiction avec `Q1` ou `Q2` ; un identifiant serait inventé pour rendre la rédaction possible ; ou l'item 2.11 toucherait une **ligne exécutable**, ou serait exécuté hors de son rang |
| **3** | Contrôles neufs verts, **mutations rouges** démontrées, non-régression de l'interdiction Lovelace prouvée dans les deux sens, aucun contrôle existant affaibli | Un contrôle passerait en confondant **présence** de clé et **contenu** de liste — le défaut exact constaté au §3.2 |
| **4** | La projection existe sous un nom **attribué par le propriétaire**, prouvée dérivée de la seule classe `O`, avec régime d'indisponibilité explicite | Le nom serait choisi par défaut ou par analogie ; ou la projection lirait un témoin natif |
| **5** | Recherche d'absence de l'ancien nom rendant **zéro occurrence**, en un seul mouvement | Une seule occurrence subsisterait, ou un alias de compatibilité serait posé |
| **6** | Les quatre sites lisent l'autorité correcte, les libellés sont distincts, aucun bouton n'est présenté puis refusé | La navigation serait adossée au verdict ; ou un geste serait offert hors classe `O` |
| **7** | Gates vertes, scénarios statiques (a) et (b) passés, scénarios terrain **nommés et disjoints de `C42`** | Une preuve serait partagée avec `C42` ; ou un constat serait déclaré fermé sans que **toutes** ses conditions du §6 soient réunies |

---

## 11. Preuves attendues — synthèse

| Nature | Preuve |
|---|---|
| **Documentaire** | Rectification **`D1`** produite, datée, classée et indexée, traçabilité conservée ; `Q1`, `Q2` et les trois rapports historiques prouvés **intacts** (`git diff` vide) ; en-tête **`D2`** réaligné au **Lot 2**, en commentaire seul, cohérent avec les contrats canoniques |
| **Contractuelle** | Chapitres `08`, `11`, `12`, `15` cohérents entre eux et avec `Q1`/`Q2` ; aucune clause ne lit plus la divergence comme une incohérence ; registre de couverture à jour si un contrôle ou un chapitre est créé |
| **Mécanique** | Checker Aspirateur vert ; contrôles neufs accompagnés de **mutations rouges** ; auto-test étendu ; aucun contrôle existant affaibli |
| **Structurelle** | Recherches d'absence à zéro occurrence : ancien nom d'attribut ; mention du helper de verdict hors allowlist |
| **Statique** | Scénarios 7.4 (a) sur-offre et (b) sous-offre, dérivés de `Q2` §6.5 |
| **Terrain** | Restreinte à ce que le statique ne peut pas atteindre ; **nommée au Lot 7** ; **disjointe de `C42`** |

---

## 12. Ce que l'ouverture de ce chantier ne fait pas

- Elle **ne ferme aucun constat** — ni `AUD-ASP-01`, ni `CC-01`, ni `RC-02`, ni `AUD-ASP-04`.
- Elle **ne modifie aucun état de clôture** du domaine `aspirateur`.
- Elle **n'attribue et ne propose aucun identifiant technique**.
- Elle **ne modifie aucun contrat, aucun checker, aucun fichier runtime, aucun arbre Lovelace**.
- Elle **ne réécrit ni `Q1`, ni `Q2`, ni la confrontation, ni les rapports historiques**.
- Elle **ne produit pas** le document de rectification `D1` : son véhicule est **décidé** (§4.1), son
  exécution appartient au **Lot 1**.
- Elle **ne corrige pas** l'en-tête de `notification_mission.yaml` : son rattachement est **décidé**
  (§4.2), sa correction appartient au **Lot 2**, item 2.11.
- Elle **ne transfère, ne renumérote et ne réécrit aucune dette de `C42`**.
- Elle **ne crée aucun changelog**.
- Elle **ne rouvre aucune option** déjà écartée par `Q2` §4 — A, B, C, E, F, G restent écartées.

---

*Chantier ouvert le 2026-09-01. Source faisant foi pour la ligne `C45` du registre.*
