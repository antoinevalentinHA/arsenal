# Réalisation L7.7 — UI, intégrité et CI (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.4 |
| **Lot** | **L7.7 — UI, intégrité et CI.** Lot **obligatoire et final** de la séquence de correction runtime |
| **Statut** | **Préparé sur branche** |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.3 → v2.4** — §9.1 cas 4, **§9.1 quater (nouveau)**, §10.2 exigence 10, §12.3. **CO-CHANGEMENT CONTRACTUEL** — voir §1 |
| **Arbitrage porté** | **Option A**, rendue le 2026-07-22 : conserver l'`input_boolean`, accepter que l'origine du `off` ne soit pas distinguable, contractualiser la limite |

> **La séquence de correction runtime est achevée. Les six écarts contractuels
> sont résorbés.**

---

## 1. Co-changement contractuel — `vmc.md` v2.3 → v2.4

L7.5 avait **démontré** qu'un `input_boolean` sans état restaurable apparaît à
`off`, jamais à `unknown` — 0 occurrence sur 21 964 lignes d'état — et que le
§9.1 cas 4 n'est donc **pas détectable** avec ce porteur. L'écart n° 5 était
resté **partiel** : prescription satisfaite, exposabilité du §10.2 exigence 10
non servie.

**L'arbitrage propriétaire retient l'option A** : conserver le porteur, accepter
la limite, la **contractualiser**.

### 1.1 Ce que l'amendement porte

**§9.1 quater — Origine d'un état initialisé inactif** *(nouveau)*, dans la
formulation arrêtée :

> **Lorsqu'aucun état restaurable n'existe, le besoin est initialisé inactif. Si
> le porteur ne permet pas de distinguer cet état d'un état inactif restauré,
> cette origine peut rester non exposée. Aucune information de reconstruction ne
> doit être fabriquée ou inférée.**

Trois interdits l'encadrent :

| Interdit | Motif |
|---|---|
| **Fabriquer** une information de reconstruction | un indicateur qui ne peut pas se déclencher affiche en permanence une absence **non établie** : c'est une affirmation, pas une exposition |
| **Inférer** l'origine d'un délai, d'un compteur ou d'un historique | ce serait reconstituer une mémoire d'épisode, prohibée par le §2.2 |
| Étendre la dispense **au-delà de cette origine** | l'état du besoin, ses conditions et ses frontières demeurent exposables sans réserve |

**§9.1 cas 4** — l'exposition est désormais « **conditionnée au porteur
d'état** » ; **§10.2 exigence 10** — « **sauf si le porteur ne rend pas cette
origine distinguable** » ; **§12.3** — une **information de reconstruction
fabriquée ou inférée** devient une non-conformité caractérisée.

### 1.2 Ce que l'amendement ne fait pas

> **La dispense porte sur une origine non observable, jamais sur une observation
> que l'on renoncerait à exposer.** Si un porteur rendant cette origine
> distinguable était retenu, l'exigence 10 redeviendrait pleinement applicable :
> la clause décrit une **limite du porteur**, non une tolérance de principe.

**La prescription du §9.1 cas 4 — besoin initialisé inactif — demeure
obligatoire et n'est en rien assouplie.**

**Aucun nouveau porteur, aucune modification de la machine**, conformément à
l'arbitrage.

---

## 2. Intégrité des paramètres — refonte complète

Les invariants surveillés portaient sur les seuils **globaux**, que la mise en
conformité a supprimés. Ils sont remplacés par ceux de l'architecture
**réellement livrée** :

| # | Invariant | Motif |
|---|---|---|
| 1 | `borne basse < borne haute`, par pièce | §7.4 bis condition 1 — bornage à double sens |
| 2 | **`seuil de niveau > borne haute`**, par pièce | **invariant découvert en calibration** : la borne haute fixe la bande morte de la voie de niveau (`S − borne haute`). Trop haute, un besoin ouvert au niveau serait libéré aussitôt — ce que le §7.4 bis condition 2 proscrit |
| 3 et 4 | `fenêtre > 0`, `évolution > 0` | une voie d'évolution inopérante ou permanente |
| 5 | `co2_seuil_on > co2_seuil_off` | hystérésis CO₂ (§5.1) — invariant qui **existait déjà mais portait sur une frontière consommée par rien** avant L7.6 |
| 6 | `durée minimale > 0` | — |

L'attribut `bande_morte_niveau` **affiche la valeur courante de la bande morte
par pièce** : l'invariant le plus subtil du chantier devient lisible d'un coup
d'œil.

**Aucun repli numérique** : `float(none)` partout, et toute source illisible
rend les invariants violés — « pas d'optimisme silencieux », doctrine déjà en
vigueur dans ce fichier et ici étendue.

---

> ## ⚠️ CORRECTIF DU 2026-07-22 — LA DOCTRINE UI N'AVAIT PAS ÉTÉ LUE
>
> `00_documentation_arsenal/ui/` contient **27 documents normatifs**,
> dont `pattern_dashboard.md` et `pattern_dashboard_reglages.md`
> (*normatif — opposable*). **Aucun n'a été consulté avant ce lot.**
>
> Deux défauts en ont résulté : des **grilles à 3 colonnes** dans les
> réglages, illisibles à largeur courante, et **trois cartes
> `type: entities`** dans le diagnostic — seul dashboard de diagnostic du
> dépôt à en employer, sur treize.
>
> Les deux sont corrigés par [`correctif_deploiement_l7_vmc.md`](correctif_deploiement_l7_vmc.md). Ce qui suit décrit l'intention
> du lot, **pas la forme livrée**.

## 3. UI — ce qui est affiché est ce qui est appliqué

### 3.1 Le texte trompeur disparaît

L'ancien texte annonçait « retour sous le seuil d'arrêt » alors que ce seuil
n'était consommé par **aucune décision** — ce que le §10.4 qualifie de
non-conformité.

Il est remplacé par
[`explication_reglages.yaml`](../../../../18_lovelace/includes/vmc/explication_reglages.yaml),
dont **chaque phrase décrit une règle effectivement appliquée** : les deux voies
d'entrée, la frontière **qui suit la température extérieure**, le rôle de la
borne haute dans la bande morte, la voie CO₂, la durée minimale — et le fait
qu'une mesure illisible **maintient** la demande au lieu de la relâcher.

### 3.2 Les paramètres consommés sont exposés

Le dashboard de réglages expose désormais les **treize** paramètres réellement
consommés, groupés par pièce puis par voie : niveau, fenêtre, évolution et les
deux bornes pour chaque salle d'eau ; les deux seuils CO₂ ; la durée minimale.

**La frontière d'arrêt courante est affichée sous les bornes de chaque pièce** —
elle varie, et son affichage évite d'avoir à la déduire.

**Les seuils globaux `vmc_seuil_on` et `vmc_seuil_off` sont supprimés** : plus
consommés par aucune décision, les laisser aurait été maintenir la
non-conformité §10.4 que ce lot corrige.

> **Conséquence assumée sur la notification de migration de L7.0.** Elle
> rapportait la valeur du seuil global au moment de la bascule ; ce helper
> n'existant plus, elle ne peut plus la lire. Elle **signale désormais le
> retrait** au lieu d'afficher `unknown`. L'information est perdue, et il vaut
> mieux le dire que l'afficher faussement.

### 3.3 La carte de diagnostic ne colore plus d'après une règle fictive

`vmc_capteur` lisait les seuils **globaux** et le **reflet d'exécution**. Elle
lit désormais, **par pièce** : le seuil de niveau **local**, la **frontière
modulée telle que calculée**, et l'**état du besoin de cette pièce**.

**La pièce est passée explicitement** par `variables.piece` — la déduire de
l'unité de mesure était un raccourci qu'une nouvelle pièce aurait rompu en
silence.

La carte du **séjour** disparaît de la voie humidité : il n'y contribue plus
depuis L7.1.

### 3.4 Le contexte non décisionnel est présenté comme tel

La carte « Extraction utile / inutile » laissait croire que le verdict d'aération
gouvernait l'extraction. Il n'y participe plus depuis L7.2. Elle devient **« Air
extérieur — plus sec / plus humide dehors »** : un **fait**, non un verdict
d'action (§10.5).

### 3.5 Le diagnostic expose la machine

Trois sections nouvelles : les **besoins par pièce et par voie** avec leurs
conditions d'entrée, de libération et leurs deux situations de maintien ; les
**frontières modulées** avec leur plancher, leur cause de non-calculabilité, la
grandeur modulante et **le statut de son axe** ; l'**intégrité des paramètres**
avec sa cause et la **bande morte courante**.

---

## 4. Critère de clôture 8 — satisfait à la lettre comme au fond

L7.2 avait retiré le verrou d'aération de la voie de décision, mais
`vmc/delta_humidite_absolue_favorable.yaml` demeurait dans la liste des
consommateurs légitimes : **la rédaction littérale du critère 8 n'était pas
atteinte**, alors que sa substance l'était.

**Ce reflet est déplacé sous `12_template_sensors/aeration/`**, dont il relève
réellement — c'est un reflet UI de l'écart d'humidité absolue publié par le
verdict d'aération, sans aucun rôle VMC.

`unique_id` inchangé → **`entity_id` conservé, aucune migration d'historique**.

> **Plus aucun fichier du domaine VMC ne figure dans cette liste.**

---

## 5. Le dernier repli silencieux disparaît

`gestion_auto.yaml` employait `| int(15)` sur la durée minimale — signalé par
L7.6, hors de son périmètre strict, traité ici.

**Le repli est retiré.** Une durée illisible ne doit ni prolonger indéfiniment
la haute vitesse, ni la couper sans délai : **la descente est suspendue**, le
système demeure dans son état courant, et `binary_sensor.parametres_invalides_vmc`
en expose la cause.

> Le §12.3 proscrit « une mesure inexploitable traitée comme une valeur
> numérique ». Le même principe vaut pour un **paramètre exécutif** : le refuser
> pour la décision et l'accepter pour la commande aurait été une distinction de
> convenance.

**La valeur de 15 minutes demeure celle qu'amorce L7.0** ; elle n'est simplement
plus refabriquée à chaque évaluation.

---

## 6. Contrôles

**86 checkers `arsenal_contracts` exécutés**, tous passent — dont les **neuf
tests** du contrat VMC, le contrat d'aération, le contrat recorder, l'intégrité
des paramètres et l'initialisation. **Gates documentaires vertes**, dont
`DOC-CI-2` sur les compteurs de contrat.

**Vérifié explicitement** : plus aucune lecture de `vmc_seuil_on` ni
`vmc_seuil_off` dans le dépôt, hors commentaires historiques ; plus aucun
fichier VMC dans l'allowlist d'aération.

> **Deux échecs demeurent, ANTÉRIEURS** : `lovelace_no_inline_templating` et
> `vacances`. Ni causés, ni aggravés.

---

## 7. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** : le dépôt est le miroir versionné, **son
  déploiement est un acte distinct**, qui n'a jamais été engagé ;
- il **ne recalibre rien** ;
- il **ne modifie aucune machine de besoin** — l'arbitrage l'excluait
  explicitement ;
- il **ne crée aucun nouveau porteur d'état** ;
- il **ne clôt pas C35** : restent **L8** (preuve après changement), **L9**
  (vérification du §15.1) et **L10** (passe documentaire finale).

---

## 8. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération décisionnel | ✅ résorbé (L7.2) |
| 2 | frontières de libération non consommées | ✅ résorbé (L7.4, L7.6) |
| 3 | aucun besoin hystérétique | ✅ résorbé (L7.4, L7.6) |
| 4 | aucun état humidité par pièce | ✅ résorbé (L7.4) |
| 5 | restauration et indisponibilité | ✅ **résorbé** — prescription appliquée, limite d'exposabilité **contractualisée** (§9.1 quater) |
| 6 | intention divergente (§11.2) | ✅ résorbé (L7.1) |

**Critères de clôture de C35 :**

| # | Critère | État |
|---|---|---|
| 1, 1 bis | contrats intégrés | ✅ |
| 2 | paramètres §14 calibrés et tracés | ✅ *(provisoire)* |
| 3 | dispositif de preuve défini | ✅ |
| 4 | `arsenal-runtime` audité | ✅ |
| 5 | référence avant changement | ✅ |
| **6** | **les six écarts résorbés** | ✅ **acquis sur le code et la CI** — reste à confirmer sur le comportement observé |
| **7** | **UI n'affiche plus de règle non appliquée** | ✅ |
| **8** | **allowlist ne référence plus la VMC** | ✅ |
| 9 | effet §15.1 vérifié | **L9** |
| 10 | passe documentaire finale | **L10** |

> **Trois critères sont acquis par ce lot.** Les deux derniers dépendent d'un
> déploiement et d'une observation — ils ne peuvent pas l'être par du code.

---

## 9. Prochain jalon

**Le déploiement vers `/config` est le prochain acte, et il vous appartient.**
Rien n'a jamais été écrit dans le runtime en exploitation.

**L8 — preuve après changement** ne peut commencer qu'une fois le système
déployé et observé, sur la base de comparaison **fixée avant le changement** par
le solde de L5 et instrumentée par l'ajout Recorder de L7.6.
