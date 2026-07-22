# Réalisation L7.2 — retrait du verrou d'aération (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L7.2 — retrait du verrou d'aération.** Résorbe l'**écart contractuel n° 1** |
| **Statut** | **Préparé sur branche** |
| **Preuve opérationnelle** | `arsenal-runtime`, commit **`321f923`**, dossier `analyses/c35_l72_transitoire_20260722/` |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §1.2, §4.3, §10.5. **Non modifié par ce lot** |

> **L'écart n° 1 est résorbé.** Le verdict d'aération ne conditionne plus la
> voie humidité. Et **ce lot mesure ce que ce retrait apporte réellement** —
> moins que ce que l'on pouvait espérer.

---

## 1. Ce qui est retiré

Le verrou disparaît des **deux besoins locaux**
([`humidite_sdb_parents.yaml`](../../../../12_template_sensors/vmc/besoins/humidite_sdb_parents.yaml)
· [`humidite_sdb_enfants.yaml`](../../../../12_template_sensors/vmc/besoins/humidite_sdb_enfants.yaml)),
où L7.1 l'avait déplacé précisément pour pouvoir le supprimer **là où il devait
l'être**.

**Motif contractuel.** Le verdict d'aération évalue l'opportunité d'ouvrir des
fenêtres, à l'échelle d'un **volume** et sur une échelle de temps **longue** :
il relève de **O3**. Le **§1.2** interdit qu'un critère servant O3 conditionne
une extraction locale, et le **§4.3** le range explicitement parmi les
informations **non décisionnelles**.

Chaque besoin ne lit désormais **aucune grandeur extérieure à sa propre pièce**.

L'attribut `verrou_aeration` et la branche « verrou fermé » de
`condition_entree` disparaissent avec lui.

---

## 2. Ce que le retrait apporte — et ce qu'il n'apporte pas

Mesuré sur le corpus de 204 jours (`321f923`), salle de bain parents :

| | **AVANT** (trace L5) | **APRÈS L7.2** | **CIBLE** (passe 5) |
|---|---:|---:|---:|
| Couverture | 64/138 | **73/138 (53 %)** | 102/138 |
| Hiver | 27/32 | 26/32 | 26/32 |
| Printemps | 32/64 | **42/64** | 54/64 |
| **Été** | **5/42** | **5/42** | **22/42** |

> **Le gain est de 9 épisodes, entièrement au printemps. L'été ne gagne
> rien.**

### 2.1 Une hypothèse du solde de L5 est partiellement infirmée

Le solde de L5 avait posé, **comme hypothèse explicitement non démontrable**,
que le verrou refermait la voie humidité en été. **La mesure l'infirme en
partie** : en été, ce n'est pas le verrou qui bloque, **c'est le niveau
lui-même**. La dérive saisonnière d'environ 20 points, établie par L5, place le
seuil de 74 % hors d'atteinte pendant la saison chaude.

**Le verrou était le facteur limitant au printemps, pas en été.**

Cette correction est consignée ici plutôt que laissée en l'état : une
hypothèse formulée par un lot antérieur, et infirmée par un lot ultérieur, doit
être **dite**.

### 2.2 La salle de douche enfants n'exprime aucun besoin

| Grandeur | Valeur |
|---|---|
| Périodes de besoin | **0** |
| Couverture | **0/27** |

**Aucun des 27 épisodes n'atteint 74 %** — constat déjà posé par la passe 1, ici
confirmé comme **conséquence opérationnelle**. Entre L7.2 et L7.3, cette pièce
est **moins bien servie qu'avant** : la trace en couvrait 2 sur 27, par la voie
CO₂ ou par commande manuelle.

> **C'est une régression locale et temporaire, assumée et non masquée.** Elle ne
> se résorbe qu'avec la **voie d'évolution de L7.3**, seule capable de
> reconnaître un épisode qui n'atteint jamais la frontière de niveau.

---

## 3. Le coût de l'état transitoire est faible

Salle de bain parents, entre L7.2 et L7.4 :

| | Besoin brut | Commande amortie (durée min. 15 min) |
|---|---:|---:|
| Périodes | 309 — **46,1/mois** | **134 — 20,0/mois** |
| Part du temps | 1,0 % | **1,9 %** |
| Durée médiane | **2 min** | **31 min** |
| Périodes < 5 min | 199 (**64 %**) | — |
| Réduction | — | **57 %** |

Le besoin brut bat beaucoup — c'est attendu d'un comparateur sans bande morte.

> **Mais un besoin qui bat n'est pas une VMC qui bat.** La durée minimale
> exécutive fusionne les demandes rapprochées : **57 % des commutations
> disparaissent**, la durée médiane passe de 2 à 31 minutes, et le temps de
> fonctionnement reste à **1,9 %**.

**Vingt commutations par mois pour 1,9 % du temps.** Ce n'est pas le coût de
l'état transitoire qui pose problème, **c'est son inefficacité**.

> **Conséquence de gouvernance.** L'essentiel du gain attendu dépend de **L7.3
> et L7.4**, non de L7.2. S'arrêter durablement ici laisserait le système dans
> un état **non conforme** et **peu utile** — sans être pour autant dangereux.

---

## 4. Le critère de clôture 8 devient auto-vérifiable

L6 avait établi que ce critère **ne se vérifie pas seul** : le checker
d'aération n'interdit que les consommateurs **non listés**, de sorte qu'y
laisser une entrée périmée ne fait échouer aucun contrôle.

**Le trou est fermé par l'autre bout.** Un **test 5** est ajouté à
`check_vmc_contracts.py` : il interdit toute consommation du verdict d'aération
dans la **voie de décision VMC** — agrégation, besoins, intention,
automatisations et scripts —, **quelle que soit l'allowlist**. Onze fichiers
sont contrôlés.

**Preuve négative établie** : réintroduire le verrou dans un besoin fait
**échouer le checker**.

> **Effet de bord vertueux, à noter** : la seule **mention** de l'identifiant du
> capteur d'aération, fût-ce en commentaire, suffit à faire d'un fichier un
> consommateur au regard du contrôle T10. Les en-têtes des deux besoins
> **décrivent** donc le verdict retiré **sans le nommer**, et le disent.

### 4.1 Un fichier VMC reste listé — et il faut le dire

`vmc/delta_humidite_absolue_favorable.yaml` demeure dans la liste des
consommateurs légitimes. C'est un **reflet UI non décisionnel** (§4.3, §10.5),
qui ne conditionne aucune extraction.

> **La rédaction littérale du critère de clôture 8 — « la liste ne référence
> plus la VMC » — n'est donc pas atteinte**, alors que sa **substance** l'est :
> plus aucun fichier **décisionnel** de la VMC ne consomme le verdict.
>
> Deux issues, à arbitrer en **L7.7** : relire le critère comme portant sur la
> **voie de décision**, ou déplacer ce reflet hors du domaine VMC — il relève
> davantage de l'aération. **Ce lot ne tranche pas.**

---

## 5. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés**, tous passent, dont le **contrat
d'aération** et le **contrat VMC** enrichi du test 5. Les deux fichiers runtime
modifiés sont **valides au parseur YAML**. Les **gates documentaires** passent.

> **Deux échecs demeurent, ANTÉRIEURS à ce lot** et vérifiés comme tels :
> `lovelace_no_inline_templating` et `vacances`. Ni causés, ni aggravés.

---

## 6. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** ;
- il **n'introduit ni hystérésis, ni voie d'évolution, ni frontière modulée** ;
- il **ne corrige pas** l'inefficacité estivale, qui relève de L7.3 et L7.4 ;
- il **ne rétablit pas** la couverture de la salle de douche enfants ;
- il **n'applique pas le §4.4** ;
- il **n'expose rien de nouveau en UI** ;
- il **ne tranche pas** le sort de `delta_humidite_absolue_favorable.yaml` ;
- il **ne clôt pas C35** — les écarts n° 3 et 5 demeurent, les n° 2 et 4 sont
  partiellement traités.

---

## 7. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération conditionne la voie humidité | ✅ **résorbé** |
| 2 | frontières de libération non consommées | partiel |
| 3 | aucun besoin hystérétique | demeure — **L7.4** |
| 4 | aucun état humidité par pièce | partiel |
| 5 | restauration et indisponibilité | demeure — **L7.5** |
| 6 | intention divergente (§11.2) | ✅ résorbé (L7.1) |

**Prochain jalon : L7.3 — critère d'entrée dynamique et observabilité.** C'est
lui qui doit rendre la salle de douche enfants opérante et attaquer le déficit
estival.
