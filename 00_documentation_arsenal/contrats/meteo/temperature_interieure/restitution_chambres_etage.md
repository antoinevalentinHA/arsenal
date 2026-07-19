# 🧠 ARSENAL — CONTRAT · Restitution thermique des bornes des chambres de l'étage

**Version :** 1.0
**Domaine :** Météo — Température intérieure — restitution des bornes MIN/MAX des chambres de l'étage
**Statut :** Normatif et opposable

---

## 1. Objet

Ce contrat gouverne la **restitution thermique** des deux bornes des chambres de l'étage :

- `sensor.temperature_min_chambres` — borne **basse** ;
- `sensor.temperature_max_chambres` — borne **haute** ;

c'est-à-dire la **catégorie thermique** attribuée à chaque borne et son **rendu couleur** sur les deux cartes du dashboard Arsenal.

Il définit :

- les **deux références physiques** (basse et haute) contre lesquelles chaque borne est qualifiée ;
- les **catégories backend** MIN (`froid` / `dans_plage`) et MAX (`chaud` / `dans_plage`), plus l'indisponibilité native ;
- les **règles de comparaison** ;
- l'**obligation de mapping** vers l'**Exception 2 thermique étendue** ;
- les **obligations** respectives du backend et de l'UI.

Ce contrat **consomme** les bornes produites par le contrat de production (§3) et **ne redéfinit pas** leur valeur, leur périmètre ni leur disponibilité.

---

## 2. Modèle de restitution — plage thermique appliquée (P2)

Les deux cartes restituent la **plage thermique actuellement choisie et appliquée par Arsenal** selon les réglages utilisateur et le contexte de maison — **et non** une plage absolue et universelle.

La catégorie **`dans_plage`** (rendue en vert) signifie **exclusivement** :

> la borne concernée **ne franchit pas** la frontière thermique **actuellement appliquée** par Arsenal.

Elle **ne signifie pas** :

- un confort absolu ou universel ;
- une absence de besoin HVAC ;
- une autorisation de chauffer ou de climatiser ;
- une décision HVAC ;
- une action HVAC ;
- le fonctionnement effectif d'un équipement.

Chaque carte qualifie **exclusivement sa propre borne** contre **sa propre frontière**.

---

## 3. Dépendance au contrat de production

Ce contrat **consomme** les bornes définies par
[`bornes_thermiques_chambres_etage.md`](bornes_thermiques_chambres_etage.md) :

- `sensor.temperature_min_chambres` (MIN des deux chambres de l'étage) ;
- `sensor.temperature_max_chambres` (MAX des deux chambres de l'étage).

Il **ne redéfinit pas** leur périmètre (les deux chambres de l'étage — Chambre Enfants + Chambre Parents, Salle de Jeux exclue par C32/A2), leur calcul, leur mémoire, leur abstention, leur fraîcheur ni leur couverture. Toute question de **production** (dont l'alignement runtime de l'abstention) relève **exclusivement** du contrat de production et n'est **pas** traitée ici.

> **Dépendance normative :** en cas de conflit sur la valeur, la disponibilité ou le périmètre des bornes, **le contrat de production prévaut**.

---

## 4. Définitions

- **Borne** : `sensor.temperature_min_chambres` (borne basse) ou `sensor.temperature_max_chambres` (borne haute), telle que produite par le contrat de production.
- **Frontière thermique appliquée** : le seuil physique, **effectivement appliqué par Arsenal au contexte courant**, contre lequel une borne est qualifiée. Une frontière est une **valeur de seuil**, **jamais** une autorisation, une décision, un franchissement binaire ou une action.
- **Référence physique basse** : la frontière appliquée qualifiant la borne basse (§5.1).
- **Référence physique haute** : la frontière appliquée qualifiant la borne haute (§5.2).
- **Catégorie thermique** : l'état sémantique produit par le backend pour une borne — MIN : `froid` / `dans_plage` ; MAX : `chaud` / `dans_plage` — ou l'indisponibilité native.
- **Franchissement strict** : `MIN < référence basse` (froid) ou `MAX > référence haute` (chaud), au sens de l'inégalité **stricte**.

---

## 5. Références physiques

Les deux références sont des **frontières thermiques appliquées** (modèle P2). Elles peuvent être réglables par l'utilisateur et appartenir aux domaines Chauffage ou Climatisation ; ce qui est **interdit**, c'est qu'une catégorie **reproduise** une autorisation, une décision ou une action HVAC, ou **recalcule** localement une frontière déjà exposée.

### 5.1 Référence physique basse (borne MIN)

La référence basse est le **seuil intérieur d'allumage Chauffage en mode confort** :

> `input_number.chauffage_consigne_confort − input_number.chauffage_offset_on`

C'est la frontière thermique intérieure sous laquelle le Chauffage **confort** s'autoriserait. Elle est **ancrée sur la consigne confort** et son offset ON : elle **ne suit pas** automatiquement les bascules Réduit, Vacances, absence, pré-confort ou tout autre mode d'application Chauffage — ces bascules pilotent l'**usage** du Chauffage, non la **lecture physique annuelle** de la borne basse. Si l'utilisateur modifie explicitement la consigne confort ou l'offset ON, la frontière évolue ; sinon elle reste stable toute l'année.

Sont **exclus** de la référence basse :

- le seuil intérieur **OFF** (`consigne_confort + offset_off`) — hystérésis de la machine Chauffage ;
- les seuils **extérieurs** (`chauffage_seuil_ext_on/off`) ;
- la **consigne réduite** et la **consigne vacances** ;
- le **blocage poêle** ;
- l'**anticipation météo** ;
- `sensor.chauffage_autorisation_cible` (décision ternaire) et toute **décision** ou **action** Chauffage.

**Exposition — autorité unique publiée.** Cette frontière n'est aujourd'hui **pas** publiée en capteur (elle n'existe qu'inline dans une décision). Le backend doit l'**exposer comme unique autorité publiée** d'un seuil intérieur ON Chauffage confort, afin que la catégorie MIN la **consomme** sans dupliquer la formule `consigne − offset`.

> **Identifiant.** L'identifiant exact du capteur d'exposition est **fixé à l'audit runtime** (le pattern du dépôt est `seuil_<action>_<domaine>_applique`, mais `sensor.seuil_allumage_chauffage_clim` existe déjà et désigne un seuil clim-HEAT distinct : l'identifiant retenu devra lever toute ambiguïté). Identifiant **conceptuel provisoire** : `sensor.seuil_interieur_on_chauffage_applique`. Ce contrat contractualise la **sémantique** de la frontière, pas son identifiant.

### 5.2 Référence physique haute (borne MAX)

La référence haute est le **seuil de déclenchement COOL appliqué au contexte courant**, déjà publié :

> `sensor.seuil_allumage_clim_applique`

Sa valeur suit le contexte maison, tel qu'appliqué par Arsenal :

- **présence hors mode nuit** → `input_number.clim_seuil_declenchement_presence` ;
- **absence ou mode nuit** → `input_number.clim_seuil_declenchement_absence`.

Ce **déplacement contextuel est voulu** (P2) : la carte restitue la plage effectivement appliquée. La catégorie MAX **consomme** ce capteur **tel quel** et **ne reproduit pas** la logique de sélection présence/nuit.

Sont **exclus** de la référence haute :

- le seuil COOL **OFF** (`sensor.seuil_extinction_clim_applique`) — hystérésis ;
- le **franchissement binaire** (`binary_sensor.clim_seuil_allumage_cool_atteint`) ;
- l'**état ON/OFF** réel de la climatisation ;
- l'**autorisation** de climatiser et toute **action** COOL.

> **Honnêteté de la référence haute (résultat cible).** La référence haute n'est exploitable que si le seuil appliqué est produit à partir d'**opérandes elles-mêmes exploitables**. **Aucun fallback numérique silencieux, notamment `0`**, ne peut transformer une impossibilité de calcul en frontière thermique valide.

Le contrat retient `sensor.seuil_allumage_clim_applique` comme **autorité cible** de la frontière haute ; son **comportement runtime actuel** (qui recourt à un repli numérique `float(0)`) **doit être audité et, si nécessaire, aligné** sur cette interdiction (lot runtime, §15). Une **valeur de repli technique** ne constitue **jamais** une référence physique appliquée : le contrat gouverne le **résultat cible**, même si le runtime actuel n'y est pas encore conforme.

### 5.3 Disponibilité des références

Les deux frontières **doivent pouvoir être produites toute l'année**, indépendamment de l'activation effective des équipements HVAC. Leur valeur peut dépendre des **réglages utilisateur** et, pour la frontière haute, du **contexte présence/nuit** défini au §5.2. Cette **disponibilité fonctionnelle** n'autorise **aucun fallback numérique** : si les opérandes nécessaires à une frontière sont inexploitables, la **frontière s'abstient** et la **catégorie correspondante devient indisponible** (§8).

À distinguer strictement :

- **disponibilité toute l'année** — propriété fonctionnelle *visée* (la frontière n'est pas conditionnée à l'état ON/OFF d'un équipement) ;
- **exploitabilité réelle à l'instant courant** — la frontière n'est exploitable que si ses opérandes le sont (§8) ;
- **interdiction de fabriquer une valeur par défaut** — aucune sentinelle ni repli technique ne peut suppléer une opérande inexploitable.

---

## 6. Catégories backend (obligation O3)

La sémantique thermique est portée par **deux template sensors dédiés** (un par borne), distincts des agrégats de production :

- **catégorie MIN** — consomme `sensor.temperature_min_chambres` **et** la référence basse (§5.1) ;
- **catégorie MAX** — consomme `sensor.temperature_max_chambres` **et** la référence haute (§5.2).

Chaque catégorie produit un **état sémantique** :

- **MIN** : `froid` / `dans_plage` (+ indisponibilité native) ;
- **MAX** : `chaud` / `dans_plage` (+ indisponibilité native).

Interdictions backend :

- **aucune RGBA** produite par le backend ;
- **aucune clé de couleur** produite par le backend (le backend expose une **catégorie sémantique**, pas une couleur) ;
- **aucune mémoire propre** ni continuité via l'état précédent ;
- **aucun fallback silencieux** ;
- **aucun `float(0)`, valeur sentinelle ou défaut numérique** transformant une entrée invalide en référence exploitable ;
- **aucune classification** si l'agrégat **ou** la frontière n'est pas **honnêtement exploitable** ;
- **aucune validation** reposant uniquement sur le fait qu'un état est **convertible en nombre** (la catégorie consomme une référence **valide**, pas seulement numérique) ;
- **aucun état textuel** `indisponible`, `neutre` ou `non_calculable` : l'indisponibilité est **native** (§8).

> **Forme et identifiants.** La forme exacte (deux template sensors dédiés) est acquise ; les **identifiants** des deux catégories sont fixés à l'audit runtime selon les conventions du dépôt.

---

## 7. Règles de comparaison

Comparaison **stricte** au franchissement, **égalité incluse** dans `dans_plage` :

### MIN
- `MIN < référence basse` → **`froid`** ;
- `MIN >= référence basse` → **`dans_plage`** (égalité exacte incluse).

### MAX
- `MAX > référence haute` → **`chaud`** ;
- `MAX <= référence haute` → **`dans_plage`** (égalité exacte incluse).

Une couleur défavorable (bleu froid / rouge chaud) n'apparaît qu'au **franchissement strict et démontré** de la frontière appliquée à la borne concernée.

---

## 8. Disponibilité native et abstention

La catégorie d'une borne devient **indisponible** si et seulement si :

- l'**agrégat** correspondant (`temperature_min_chambres` / `temperature_max_chambres`) est inexploitable (`unknown` / `unavailable`, ou abstention à zéro façade selon le contrat de production) ; **ou**
- la **référence** correspondante (§5.1 / §5.2) est inexploitable.

Une **référence est inexploitable** notamment lorsque :

- son état est `unknown` ou `unavailable` ;
- une de ses **opérandes nécessaires** est inexploitable (p. ex. la consigne confort ou l'offset ON pour la frontière basse ; le helper sélectionné pour la frontière haute) ;
- sa valeur résulte d'un **fallback** ou d'une **sentinelle technique** ;
- elle n'est **pas** une valeur numérique thermique valide **produite selon sa formule contractuelle**.

*(Ce contrat fixe l'**honnêteté de production** de la référence ; il n'introduit **aucune plage de plausibilité numérique nouvelle** ni validation parallèle.)*

Effets normatifs :

- l'indisponibilité est **native** (la catégorie elle-même devient indisponible) ;
- **aucun état textuel** `indisponible` / `neutre` / `non_calculable` n'est publié ;
- **aucune catégorie périmée** n'est maintenue ni republiée ;
- l'UI restitue l'indisponibilité par le **gris indisponibilité `rgba(158,158,158,0.1)`**, **prioritaire** (doctrine générale `ui/couleurs/05_regles.md`).

> **Résultat normatif vs mécanisme.** Ce contrat fixe le **résultat** (catégorie indisponible, sans état textuel ni valeur périmée). Le **mécanisme** Home Assistant (`availability`, `unknown`, …) est déterminé à l'audit d'implémentation, sous réserve de produire ce résultat.

---

## 9. Séparation MIN/MAX (aucun cross-entity)

- La catégorie MIN **ne lit jamais** `temperature_max_chambres` ni la référence haute ;
- la catégorie MAX **ne lit jamais** `temperature_min_chambres` ni la référence basse ;
- **aucun état global partagé** n'est injecté dans les deux cartes ;
- le modèle **cross-entity** (RED de MIN piloté par un franchissement basé sur MAX) est **interdit**.

---

## 10. Interdiction des couches décisionnelles HVAC

Les catégories et les cartes **n'expriment ni ne consomment** aucune couche décisionnelle HVAC :

- **aucun** besoin, admissibilité, autorisation, décision (`clim_target_mode`, `chauffage_autorisation_cible`), ou action ;
- **aucun** franchissement binaire (`clim_seuil_allumage_cool_atteint`) ;
- **aucune** lecture directe, par l'UI, d'un helper Chauffage/Climatisation ni recalcul local d'une frontière ;
- une frontière **appliquée** (§5) est consommée en tant que **valeur de seuil**, jamais en tant qu'autorisation, décision ou action.

Restituer la plage **appliquée** (P2) **ne transforme pas** les cartes en cartes décisionnelles HVAC : elles qualifient une **borne physique** contre une **frontière physique**, sans afficher les décisions Chauffage/Climatisation correspondantes.

---

## 11. Mapping UI vers l'Exception 2 étendue

Le backend fournit la **catégorie** ; l'UI applique **trivialement** la palette de l'**Exception 2 thermique étendue** (`ui/couleurs/03_exceptions.md`) :

| Catégorie | Couleur |
|---|---|
| `froid` | 🔵 bleu thermique `rgba(144, 202, 249, 0.25)` |
| `dans_plage` | 🟢 vert `rgba(76, 175, 80, 0.2)` |
| `chaud` | 🔴 rouge thermique `rgba(244, 67, 54, 0.2)` |
| indisponibilité native | ⚪ gris indisponibilité `rgba(158, 158, 158, 0.1)` (prioritaire) |

Obligations UI :

- **aucune comparaison de seuil** dans les cartes ;
- **aucune lecture directe** d'un helper Chauffage/Climatisation ni du franchissement COOL ;
- **aucun recalcul** de couleur ni de frontière ;
- suppression de tout bloc de couleur local reproduisant une logique métier ;
- préservation du **titre**, de la **valeur** (°C), de l'**unité** et du **contexte de l'extrême** (chambre portant l'extrême) ;
- aucun **gris neutre `0.2`** intermédiaire pour ces catégories.

> **Support du mapping.** Le porteur exact du mapping (socle KPI et/ou template dédié) et l'ajout éventuel des clés de palette relèvent de l'**implémentation UI** (hors de ce contrat).

---

## 12. Obligations backend et UI (synthèse)

- **Backend** : produit, par borne, la **catégorie sémantique** (§6) à partir de l'agrégat et de la frontière appliquée (§5) ; expose la frontière basse comme **autorité unique publiée** (§5.1) ; ne produit aucune couleur ; s'abstient nativement (§8).
- **UI** : **mappe** la catégorie vers l'Exception 2 étendue (§11) ; ne décide rien ; restitue l'indisponibilité prioritaire.

---

## 13. Invariants opposables

*(Convention d'identifiant : `INV-RCE-*` — Restitution Chambres Étage.)*

- **INV-RCE-1** — La restitution qualifie la **plage thermique appliquée** (P2), non une plage absolue.
- **INV-RCE-2** — La borne MIN est qualifiée **exclusivement** contre la **référence basse** (§5.1) ; la borne MAX **exclusivement** contre la **référence haute** (§5.2).
- **INV-RCE-3** — Référence basse = `chauffage_consigne_confort − chauffage_offset_on`, **ancrée sur la consigne confort** ; ni OFF, ni extérieur, ni réduite/vacances, ni poêle, ni météo, ni autorisation/décision.
- **INV-RCE-4** — Référence haute = `sensor.seuil_allumage_clim_applique` ; son déplacement présence↔absence/nuit est **voulu** ; ni OFF, ni franchissement binaire, ni état ON/OFF, ni autorisation/action.
- **INV-RCE-5** — Catégories : **MIN `froid`/`dans_plage`**, **MAX `chaud`/`dans_plage`**, + indisponibilité native ; aucun autre état textuel.
- **INV-RCE-6** — Comparaison **stricte** ; **égalité exacte ∈ `dans_plage`**.
- **INV-RCE-7** — Une catégorie est **indisponible** si son agrégat **ou** sa référence est inexploitable ; **aucune catégorie périmée** maintenue.
- **INV-RCE-8** — **Aucune RGBA ni clé de couleur** produite par le backend ; le backend expose une **catégorie sémantique**.
- **INV-RCE-9** — **Aucun cross-entity** ; MIN et MAX qualifient chacune leur propre borne.
- **INV-RCE-10** — **Aucune couche décisionnelle HVAC** (besoin, admissibilité, autorisation, décision, action, franchissement binaire) n'est consommée ni exprimée.
- **INV-RCE-11** — Le mapping UI applique l'**Exception 2 étendue** (froid→bleu thermique, `dans_plage`→vert, chaud→rouge, indispo→gris `0.1` prioritaire), sans comparaison ni recalcul en UI.
- **INV-RCE-12** — La frontière basse est portée par une **autorité unique publiée** ; la formule `consigne − offset` **n'est pas dupliquée** dans la catégorie.
- **INV-RCE-13** — Aucune frontière ni catégorie ne peut être rendue exploitable par un **fallback numérique**, une **valeur sentinelle** ou une **conversion par défaut** lorsque ses opérandes sont inexploitables.

---

## 14. Critères de conformité

Une implémentation est **conforme** si, sans écrire ici le YAML ni le checker :

- la catégorie MIN lit **uniquement** `temperature_min_chambres` + la référence basse publiée ; la catégorie MAX **uniquement** `temperature_max_chambres` + `sensor.seuil_allumage_clim_applique` ;
- les comparaisons sont strictes et l'**égalité** produit `dans_plage` ;
- la référence basse est exposée par un **capteur d'autorité unique** (`consigne_confort − offset_on`, confort), sans OFF/extérieur/réduite/vacances/poêle/météo/décision ;
- la référence haute est le **seuil COOL ON appliqué** publié, sans OFF/franchissement/état/autorisation ;
- une catégorie est **indisponible** dès que son agrégat **ou** sa référence est inexploitable, **sans** état textuel ni valeur périmée ;
- la **référence haute s'abstient** si sa sélection ou le helper sélectionné est inexploitable ;
- la **future référence basse publiée s'abstient** si la consigne confort ou l'offset ON est inexploitable ;
- **aucune valeur `0`** ni autre défaut technique n'est interprétée comme frontière valide ;
- les **catégories s'abstiennent** dès que la frontière correspondante n'est pas **honnêtement calculable** ;
- le backend ne produit **aucune couleur** ; l'UI mappe **trivialement** vers l'Exception 2 étendue ;
- aucun cross-entity, aucune couche décisionnelle HVAC, aucun gris neutre `0.2` intermédiaire ;
- les invariants `INV-RCE-1…13` sont vérifiables.

---

## 15. Hors périmètre

Sont **hors** de ce contrat :

- la **création** du capteur d'exposition de la frontière basse et des deux catégories (relève de l'implémentation runtime) ;
- la **modification** du runtime, de l'UI, du socle KPI, des checkers ou de la CI ;
- l'**alignement `{{ last }}`** / l'abstention des agrégats (relève du **contrat de production** et du lot runtime) ;
- l'**alignement de `sensor.seuil_allumage_clim_applique`** avec l'interdiction de fallback silencieux (§5.2) relève du **futur lot runtime** ; ce contrat **n'affirme pas** que ce comportement est déjà conforme ;
- la **réouverture** du contrat de production (périmètre, calcul, mémoire, couverture) ;
- l'**affichage de la couverture partielle** sur les cartes ;
- l'imposition d'une **mutualisation UI** des deux templates ;
- le **HEAT d'appoint** Climatisation, le **RDC**, la **petite maison** ;
- les **valeurs numériques** des réglages (elles appartiennent à l'utilisateur) et l'**identifiant exact** du capteur d'exposition basse (audit runtime).

---

## 16. Synthèse

> **Les deux cartes des chambres de l'étage restituent la plage thermique *appliquée* par Arsenal : la borne basse est *froide* sous le seuil intérieur ON Chauffage confort (`consigne_confort − offset_on`), la borne haute est *chaude* au-dessus du seuil COOL ON appliqué (`sensor.seuil_allumage_clim_applique`), et chacune est `dans_plage` (vert) sinon — égalité incluse. Le backend produit une catégorie sémantique par borne (jamais une couleur), s'abstient nativement si l'agrégat ou la référence est inexploitable, et l'UI mappe trivialement vers l'Exception 2 étendue, sans cross-entity ni logique décisionnelle HVAC.**

---

## 📌 Statut & évolution

- Contrat Arsenal, **normatif et opposable**.
- Domaine : Météo — température intérieure, restitution des bornes des chambres de l'étage.
- Dépendances : [`bornes_thermiques_chambres_etage.md`](bornes_thermiques_chambres_etage.md) (production, consommée) ; `ui/couleurs/03_exceptions.md` (Exception 2 étendue) ; `sensor.seuil_allumage_clim_applique`, `input_number.chauffage_consigne_confort`, `input_number.chauffage_offset_on` (frontières appliquées).
- Toute évolution des **références**, des **catégories** ou des **invariants** exige une modification explicite de ce contrat, une validation humaine et la traçabilité documentaire requise par la gouvernance Arsenal.
