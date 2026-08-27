# CONTRAT ARSENAL — ASPIRATEUR
## 06 — Intégrité mono-carte (`ASP-IMC-1`)

**Version contrat :** v1.0
**Statut :** Normatif — **contrainte de sûreté opposable**
**Objet :** Ratifier en clause contractuelle la contrainte de sécurité candidate
issue de l'audit, et en fixer les conditions de satisfaction.

---

## 1. Le fait technique — établi, indépendant de tout arbitrage

Trois faits, l'un de code, deux de terrain, fondent ce chapitre :

1. **Une commande segmentée ne transporte aucun index de carte.** Sa charge utile
   se réduit à une liste d'index de segments — nécessairement interprétée dans la
   **carte active du robot**.
2. **Ces index sont ambigus entre cartes.** L'index `16` désigne `Salon` au RDC,
   `Palier` à l'Étage, `Salle de bain` à l'Annexe.
3. **La couche d'exposition filtre, et échoue en silence.** Elle compare l'index
   de carte de chaque segment demandé à la carte active, **jette sans erreur**
   ceux qui ne correspondent pas, **n'émet rien du tout** si aucun ne subsiste, et
   **ne bascule jamais** de carte de sa propre initiative.

| Demande | Résultat sur l'appareil |
|---|---|
| Segments **tous** sur la carte active | Exécutée normalement |
| Segments **partiellement** hors carte active | **Tronquée en silence** — seul le sous-ensemble de la carte active est nettoyé |
| Segments **tous** hors carte active | **Aucune commande émise, aucune erreur levée** — l'action « réussit » et le robot ne bouge pas |

Les deux dernières issues sont **inacceptables** et **ne sont signalées par
aucune erreur** : *nettoyer la mauvaise pièce*, ou *prétendre avoir lancé sans
rien faire*.

---

## 2. La clause

> ### `ASP-IMC-1` — Intégrité mono-carte d'une mission segmentée
>
> **Aucune commande segmentée n'est émise tant que la carte active n'est pas
> explicitement sélectionnée, confirmée, et concordante avec l'intégralité des
> segments demandés.**

**Statut.** Cette clause était une **contrainte de sécurité candidate** dans
l'audit — un relevé, sans force normative. **Elle est ici ratifiée** : elle
devient une **clause opposable** du domaine. Le fait technique qui la motive, lui,
ne dépendait d'aucun arbitrage.

---

## 3. Conditions de satisfaction — dans cet ordre

Avant toute mission segmentée, **toutes** les conditions suivantes sont
satisfaites, **dans l'ordre** :

| # | Condition | Défaut ⇒ refus |
|---|---|---|
| 1 | **Une seule carte est demandée** par l'intention | `SELECTION_MULTI_CARTE` |
| 2 | Cette carte est **explicitement sélectionnée** sur l'appareil, sous l'**option exacte** du sélecteur ([`02`](02_referentiel_cartes_et_pieces.md) §2.1) | `CARTE_NON_CONFIRMEE` |
| 3 | La sélection est **confirmée par relecture**, par comparaison **littérale** à cette même option | `CARTE_NON_CONFIRMEE` |
| 4 | Les **pièces exposées** pour cette carte **contiennent l'intégralité** des segments du référentiel V1 de cette carte ([`02`](02_referentiel_cartes_et_pieces.md) §2, §2.1) — voir §3.1 | `CARTE_NON_CONFIRMEE` |
| 5 | **Tous** les segments demandés appartiennent à cette carte | `SEGMENT_INCONNU` |
| 6 | La carte active est **lisible** — ni `unknown`, ni `unavailable` | `CARTE_NON_CONFIRMEE` |

### 3.1 La condition 4 est une **inclusion**, jamais une égalité

> **`ASP-INV-63` — inclusion, pas égalité.** La confirmation exige que les pièces
> exposées par l'appareil pour la carte désignée **contiennent tous** les segments
> du référentiel V1 de cette carte. Elle **n'exige pas** que les deux ensembles
> soient égaux : la carte peut légitimement exposer des segments **hors
> référentiel métier V1**.
>
> **Pourquoi cette précision est structurante.** La carte Annexe porte **quatre**
> segments (`2_16`, `2_17`, `2_18`, `2_19`) alors que son référentiel V1 en compte
> **deux** (`2_16`, `2_19`). Sous une lecture par égalité, **toute mission Annexe
> serait refusée en permanence** au motif `CARTE_NON_CONFIRMEE` — y compris le
> raccourci « Annexe complète », alors que l'Annexe est l'un des trois périmètres
> métier visés. L'inclusion est donc la seule lecture exécutable.
>
> **Ce que l'inclusion ne relâche pas.** `Ext` (`2_17`) et `Chambre1` (`2_18`)
> restent **hors référentiel métier V1** et **non commandables** : les voir
> exposés confirme la carte, mais les **désigner** dans une intention reste
> refusé au motif `SEGMENT_INCONNU` ([`02`](02_referentiel_cartes_et_pieces.md)
> §2, `QO-1`). Confirmer une carte et autoriser un segment sont deux contrôles
> distincts — la condition 4 confirme, la condition 5 autorise.
>
> **Un segment du référentiel manquant à l'appel refuse.** Si l'appareil
> n'expose pas l'un des segments attendus, la carte chargée n'est pas celle que le
> contrat décrit : `CARTE_NON_CONFIRMEE`.
>
> **Comment l'inclusion se constate.** Les pièces exposées le sont **sous leur
> nom Roborock**, jamais sous leur index. La condition 4 confronte donc ces noms
> aux **noms Roborock exacts** des segments V1 de la carte désignée, tels que
> ratifiés en [`02`](02_referentiel_cartes_et_pieces.md) §2.1 — comparaison
> **littérale**, jamais approchée (`ASP-INV-66`, `ASP-INV-67`). C'est l'unique
> endroit du domaine où un nom de segment remonté par l'appareil est comparé, et
> il n'en sort **aucune désignation** : la condition 4 **confirme**, la condition
> 5 **autorise** — les segments demandés restent, eux, des paires
> `‹carte›_‹segment›`.

> **`ASP-INV-27` — le refus est la seule alternative.** Si **une** condition
> manque ou diverge, la mission est **refusée**, avec un motif lisible. Elle
> n'est **jamais** tronquée au sous-ensemble valide, **jamais** relancée sur une
> autre carte, **jamais** émise « pour voir ».

> **`ASP-INV-28` — aucune agrégation multi-carte.** Une mission **ne peut pas**
> agréger des segments de plusieurs cartes. Nettoyer deux étages est **deux
> missions**, séquentielles et distinctes — jamais une mission composite.

---

## 4. Ce qui fait office de confirmation — et ce qui n'en fait pas

**Fait établi terrain.** Après écriture explicite de la carte sur le sélecteur, la
bascule s'est vérifiée **par deux voies indépendantes** : la couche entités a
exposé les pièces attendues de la carte demandée, et le statut brut de l'appareil
a confirmé la bascule au **niveau protocolaire**. La bascule n'a provoqué **aucun
mouvement** du robot, resté amarré et en charge, et s'est **maintenue** plus de
quatre heures et à travers deux missions.

**Ce que le contrat retient comme confirmation.**

| Lecture | Statut contractuel |
|---|---|
| **Relecture du sélecteur de carte** (`select.roborock_q7_max_carte_selectionnee`) | **Obligatoire** — condition 3, comparaison littérale à l'option exacte ([`02`](02_referentiel_cartes_et_pieces.md) §2.1) |
| **Inclusion des pièces exposées** par rapport au référentiel V1 de la carte (`sensor.roborock_q7_max_piece_actuelle`) | **Obligatoire** — condition 4, **seconde lecture distincte** dans la même couche entités (§3.1), sur les noms exacts de [`02`](02_referentiel_cartes_et_pieces.md) §2.1 |
| **Statut protocolaire brut de la carte** (`mapStatus`, observé en diagnostic terrain) | **Non retenu comme dépendance runtime** — voir §5 |

> **`ASP-INV-29` — la double confirmation est la règle.** La confirmation repose
> sur **deux lectures distinctes de la couche entités**, non sur une seule : le
> sélecteur dit ce qui a été **demandé**, la liste des pièces exposées dit ce que
> l'appareil a **effectivement chargé**. Une seule des deux ne suffit pas.
>
> **Ces deux lectures ne sont pas des voies indépendantes.** Elles proviennent de
> la **même couche entités** et du même rafraîchissement. Elles se recoupent
> utilement — une demande sans chargement effectif est détectée — mais elles ne
> constituent **pas** une confirmation indépendante du chemin d'exposition. La
> seule confirmation réellement indépendante observée sur le terrain est
> **protocolaire**, et le contrat ne s'y adosse pas : elle reste une **question
> ouverte** (§5, `QO-2`).

---

## 5. `mapStatus` — observé, non promu

Le champ `mapStatus` a été relevé **dans les diagnostics terrain** et a fourni
une confirmation protocolaire précieuse. Il **n'est pas** promu en dépendance de
ce contrat.

> **`ASP-INV-30`** — Le domaine **ne dépend d'aucune primitive non prouvée
> exploitable dans Arsenal**. `mapStatus` n'est, à ce jour, adossé à **aucune
> entité ni primitive** dont l'exploitabilité par Arsenal soit établie : en faire
> une condition de sûreté reviendrait à inscrire une dépendance imaginaire dans
> un contrat opposable.
>
> Sa promotion éventuelle exigerait la **preuve** qu'une telle primitive existe et
> est consommable. Elle est inscrite comme **question ouverte**
> ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `QO-2`), pas
> comme obligation.

---

## 6. Ce que la sélection de carte n'est pas

- ❌ **Ce n'est pas une localisation.** Le sélecteur ne prouve **jamais** où se
  trouve le robot, et ne se recale pas après un déplacement physique.
- ❌ **Ce n'est pas un mouvement.** Basculer de carte, robot amarré, n'a provoqué
  aucun déplacement.
- ❌ **Ce n'est pas acquis en toutes circonstances.** L'acceptation d'un changement
  de carte **lorsque le robot se trouve physiquement sur une autre carte** n'est
  **pas établie** — le cas validé sur le terrain est celui d'un robot déjà présent
  sur la carte demandée. C'est précisément pourquoi la **confirmation** est
  exigée plutôt que présumée : le contrat n'a pas besoin de trancher ce cas, il
  exige seulement que la confirmation l'établisse **avant** chaque mission.

**Corroboration admise, jamais exigée.** Après une bascule, la pièce courante
remontée par l'appareil a désigné la pièce où se trouve la base : c'est la
**conjonction** du sélecteur et de la pièce courante qui devient informative,
**jamais le sélecteur seul**.

---

## 7. Portée de la clause

`ASP-IMC-1` s'applique à **toute** voie segmentée, quelle que soit sa forme
d'émission, et vaudrait de même — pour les mêmes raisons — pour une voie zonée,
qui ne transporte pas davantage d'index de carte. Aucune voie du domaine n'y
échappe.

---

## Renvois

- Référentiel et unicité de désignation : [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md)
- Séquence de lancement : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Refus `CARTE_NON_CONFIRMEE`, `SELECTION_MULTI_CARTE`, `SEGMENT_INCONNU` : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Index du domaine : [`README.md`](README.md)
