# Arbitrage — propriété des paramètres et ordonnancement des lots runtime (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Nature** | **Arbitrage propriétaire rendu (2026-07-22).** Tranche les deux points que L6 avait identifiés comme relevant du propriétaire et non de l'analyse |
| **Statut** | **Préparé sur branche.** **Aucun runtime modifié.** L7.0 n'est pas engagé |
| **Origine** | L6 — [`analyse_impact_runtime_vmc.md`](analyse_impact_runtime_vmc.md), PR #523, §2.5 (structure de stockage) et §9 (ordre des lots) |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §7.4 bis condition 1, §10.2, §10.4, §12.3, §14. **Non modifié par ce lot** |

> **Ce lot ne produit aucun patch.** Il fixe **où vit chaque paramètre** et
> **dans quel ordre les lots runtime s'exécutent**. La calibration est
> inchangée : les valeurs restent celles de la passe 5, provisoires et
> révisables.

---

## 1. Décision rendue

> **Structure mixte** — helpers persistants pour les paramètres opérationnellement
> configurables, **constantes versionnées** pour les coefficients de calibration
> `A`, `B` et `H`, différenciés par pièce.
>
> **Ordonnancement** — **L7.0 obligatoire avant L7.1**, **L7.7 obligatoire après
> L7.6**.

---

## 2. Répartition des paramètres

### 2.1 Helpers persistants

Réservés aux valeurs qui **doivent** être configurables ou exposées
opérationnellement.

| Paramètre | Portée | Nombre |
|---|---|---|
| `S` — frontière de niveau, entrée | par pièce | 2 |
| `W` — fenêtre d'observation glissante | par pièce | 2 |
| `D` — évolution d'entrée | par pièce | 2 |
| Borne **basse** de la frontière modulée | par pièce | 2 |
| Borne **haute** de la frontière modulée | par pièce | 2 |
| Durée minimale de haute vitesse | global | 1 |
| | **Sous-total** | **11** |

**Les bornes sont des helpers par obligation contractuelle** : le §7.4 bis
condition 1 exige qu'elles soient « configurables et exposables ». La décision ne
fait ici que constater une contrainte, elle ne l'arbitre pas.

**Ces helpers restent sans clé `initial:`**, conformément à la doctrine du dépôt.

### 2.2 Constantes versionnées

| Paramètre | Portée | Nombre |
|---|---|---|
| `A` — constante de la frontière | par pièce | 2 |
| `B` — pente sur la température extérieure | par pièce | 2 |
| `H` — bande morte | par pièce | 2 |
| | **Sous-total** | **6** |

**Motif de la décision, tel que rendu :**

> Ce sont des **choix de calibration**, non des réglages utilisateurs ordinaires.
> Les mettre dans des curseurs les rendrait modifiables **hors Git, sans revue,
> sans trace**, et potentiellement **en contradiction avec les preuves de L2b**.

**L'UI peut afficher leur valeur et leur provenance ; elle ne doit pas les
éditer.**

### 2.3 Réconciliation avec le dénombrement de L6

L6 comptait **19** paramètres. La décision en nomme **17**. Les deux manquants
sont les seuils CO₂ existants.

| Ensemble | Nombre |
|---|---|
| Helpers nommés par la décision | 11 |
| Constantes versionnées | 6 |
| **Seuils CO₂ existants** — `vmc_co2_seuil_on`, `vmc_co2_seuil_off` | **2** |
| **Total** | **19** |

> **Point non couvert par la décision, signalé et non tranché.** Les deux seuils
> CO₂ sont **déjà** des helpers et le demeurent par continuité — ce sont des
> réglages d'usage, pas des coefficients de calibration. En revanche,
> `vmc_co2_seuil_off` **n'est consommé par aucune décision** (L6 §2.2) : soit la
> voie CO₂ acquiert une libération qui le consomme, soit il doit disparaître au
> titre du §10.4. **Le point relève de L7.4 ou L7.6**, et reste ouvert.

### 2.4 Sort des seuils HR de libération

`input_number.vmc_seuil_off` n'a plus d'objet : la frontière de libération
devient `borne(A − B × T_ext)`. Il doit être **supprimé ou requalifié** en L7.0.
L'opération est **sans effet sur le comportement** — il n'est consommé par rien —
mais **visible pour l'utilisateur**, qui l'a réglé.

---

## 3. Invariant de propriété

> **Une seule définition autoritative de chaque valeur. Aucun doublon
> helper / constante. Aucun repli numérique silencieux.**

Trois conséquences d'implémentation, à respecter en L7 :

**3.1 Pas de duplication entre calcul et exposition.** Le §10.2 exigences 20 à
24 et le §10.4 imposent d'exposer la frontière courante, ses bornes et la
grandeur modulante. Une constante employée dans un fichier et **recopiée** dans
un autre pour l'affichage constituerait un doublon, donc une violation de
l'invariant. L'exposition doit donc être **portée par l'entité qui calcule**,
sous forme d'attributs, et non reconstruite ailleurs.

**3.2 Pas de repli numérique.** Le style `| float(70)` / `| int(15)` du runtime
actuel est **proscrit** pour les nouveaux paramètres : un helper indisponible
rend la frontière **non calculable**, état qui doit être **exposé** (§4.4 bis,
§10.2 exigence 24) et **ne vaut jamais libération**. Le contre-modèle existe déjà
dans le dépôt — `binary_sensor.parametres_invalides_vmc` emploie `| float(none)`
et revendique « pas d'optimisme silencieux ».

**3.3 Aucun writer permanent sur les helpers.** Après l'initialisation contrôlée
de L7.0, **aucune automatisation ne réécrit** un helper de paramètre.
L'utilisateur en demeure le seul auteur — règle déjà en vigueur, ici confirmée et
étendue aux nouveaux helpers.

---

## 4. Migration — le mandat de L7.0

**Problème posé par L6 :** un helper sans clé `initial:` vaut `unknown` à sa
première apparition ; aucun repli n'étant admis, la machine serait **non
calculable au premier démarrage suivant le déploiement**.

**Traitement arrêté :**

| # | Point | Règle |
|---|---|---|
| 1 | **Initialisation** | Les nouveaux helpers sont initialisés **de façon contrôlée lorsqu'ils sont `unknown`** — et à cette seule condition |
| 2 | **Après initialisation** | **Aucun writer permanent** ne vient les réécrire (§3.3) |
| 3 | **Valeurs d'amorce** | Celles de la passe 5, seule source de valeurs arbitrées |
| 4 | **Helper HR de libération** | `vmc_seuil_off` supprimé ou requalifié (§2.4) |
| 5 | **Réglage utilisateur existant** | `vmc_seuil_on` est aujourd'hui **global** ; il devient **par pièce**. Le devenir de la valeur réglée par l'utilisateur est à traiter explicitement, non par écrasement silencieux |

> **L'initialisation contrôlée n'est pas un repli déguisé.** Elle s'exécute
> **une fois**, sur un helper **sans valeur**, et laisse ensuite la main à
> l'utilisateur. Un repli, lui, s'applique **à chaque évaluation** et **masque**
> l'indisponibilité. Les deux sont distincts, et seul le second est proscrit.

---

## 5. Ordonnancement arrêté

| Rang | Lot | Objet |
|---|---|---|
| 1 | **L7.0** | **Propriété des paramètres et migration** — où vit chaque valeur, initialisation contrôlée, sortie propre de l'état `unknown` |
| 2 | **L7.1** | Besoins locaux et paramètres par pièce |
| 3 | **L7.2** | Retrait du veto d'aération |
| 4 | **L7.3** | Critère d'entrée dynamique et observabilité |
| 5 | **L7.4** | Machine hystérétique et libération modulée |
| 6 | **L7.5** | Restauration et indisponibilité |
| 7 | **L7.6** | Composition et commande |
| 8 | **L7.7** | **UI, intégrité et CI** — consolidation finale |

**L7.0 est bloquant.** Motif tel que rendu : *aucun calcul ne doit être
implémenté avant d'avoir déterminé où vit chaque paramètre et comment les
nouveaux helpers quittent proprement l'état `unknown`.*

**L7.7 est obligatoire, mais final** : il doit **contrôler et afficher
l'architecture réellement livrée**, non une architecture prévue. Son périmètre :

- suppression des **promesses mensongères** autour des seuils OFF actuels — le
  texte de la carte de réglages et la coloration de `vmc_capteur` (§10.4) ;
- **alignement de `sensor.vmc_intention`** sur la décision autoritative — c'est
  le sixième écart formel relevé par L6 (§11.2) ;
- **diagnostic** des paramètres invalides et des **états d'abstention** ;
- **retrait de l'ancien consommateur** de l'allowlist du checker d'aération ;
- **ajout des gardes CI** correspondant à l'architecture finale.

**Exception explicitement admise.** La modification du checker qui protège le
retrait d'`aeration_preferable_etage` **peut être réalisée avec L7.2** si elle
constitue **la preuve de ce lot**. L7.7 assure alors la **consolidation finale**
de l'intégrité et de l'UI.

> **Cette exception traite le point n° 7 de L6** — le critère de clôture 8 ne se
> vérifiant pas seul, le porter dans le lot qui produit le retrait est ce qui le
> rend vérifiable.

---

## 6. Effets sur le chantier

| Élément | Effet |
|---|---|
| Séquence du §5 du chantier | **L7 devient L7.0 à L7.7**, huit lots ordonnés |
| Verrou de L7.4 | **levé** depuis la passe 5 ; L7.4 prend son rang dans la séquence |
| Critère de clôture 7 — UI n'affichant plus de règle non appliquée | rattaché à **L7.7** |
| Critère de clôture 8 — allowlist du checker d'aération | rattaché à **L7.2** *(preuve)* et **L7.7** *(consolidation)* |
| Écart n° 6 — `sensor.vmc_intention` (§11.2) | rattaché à **L7.7** |
| Verrou général | **inchangé** : aucune correction runtime tant que la séquence probatoire n'est pas soldée |

---

## 7. Ce que ce lot ne décide pas

- il **ne modifie aucun runtime** et **ne produit aucun patch** — L7.0 n'est pas
  engagé ;
- il **ne recalibre rien** : `A`, `B`, `H`, `S`, `W`, `D`, les bornes et la durée
  minimale restent aux valeurs provisoires de la passe 5 ;
- il **ne modifie aucun contrat** ;
- il **ne tranche pas le sort des seuils CO₂** (§2.3), renvoyé à L7.4 ou L7.6 ;
- il **ne lève pas le verrou de séquence** : L5 demeure une référence terrain
  partielle, et aucune correction runtime n'est autorisée à ce stade ;
- il **ne fixe pas la forme technique** des constantes versionnées ni du
  mécanisme d'initialisation — cela relève de L7.0.
