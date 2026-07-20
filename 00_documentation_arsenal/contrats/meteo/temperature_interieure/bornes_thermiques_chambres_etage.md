# 🧠 ARSENAL — CONTRAT · Bornes thermiques MIN/MAX des chambres de l'étage

**Version :** 1.1
**Domaine :** Météo — Température intérieure — sous-ensemble spatial (chambres de l'étage)
**Statut :** Normatif et opposable

> **v1.1 (C32 / A2 — déménagement) :** périmètre réduit de **3 à 2 chambres** de l'étage
> (**Chambre Enfants** + **Chambre Parents**). La **Salle de Jeux** est
> **exclue** : pièce sans usage sommeil, elle ne doit pas piloter le besoin de chauffe nocturne.
> Les façades sont désormais nommées `…_chambre_enfants`
> et `…_chambre_parents` ; l'alignement du **runtime** (retrait de la Salle de Jeux des agrégats) reste
> porté par **C32/L4**. Chantier :
> [`chantier_restructuration_chambres_enfants.md`](../../../audits/04_chantiers/transverses/chantier_restructuration_chambres_enfants.md).

---

## 1. Objet

Ce contrat gouverne la **production** des deux **bornes thermiques** :

- `sensor.temperature_min_chambres` — borne **basse** ;
- `sensor.temperature_max_chambres` — borne **haute** ;

en tant que **minimum** et **maximum** du **sous-ensemble spatial formé exclusivement par les deux chambres de l'étage**.

> **Ces bornes ne représentent pas** la température intérieure globale, ni la température de toute la maison, ni la température de tout l'étage, ni le rez-de-chaussée, ni une synthèse de toutes les zones intérieures. Elles représentent **uniquement** les extrêmes thermiques des **deux chambres de l'étage** définies au §2.

Les identifiants historiques `sensor.temperature_min_chambres` / `sensor.temperature_max_chambres` sont **conservés** ; ce contrat en définit le **périmètre réel** sans ambiguïté malgré leur nom historique (qui ne porte pas la mention « étage »).

---

## 2. Périmètre souverain

L'**ensemble des chambres de l'étage** est composé **exactement** des deux façades suivantes :

- `sensor.temperature_chambre_enfants` — **Chambre Enfants** (pièce partagée ; `entity_id` renommé `…_chambre_enfants` au **C32/L3**)
- `sensor.temperature_chambre_parents` — **Chambre Parents**

Sont **explicitement exclus** du calcul, présents ou futurs :

- la **Salle de Jeux** (`sensor.temperature_salle_de_jeux`) : pièce **sans usage sommeil**, **retirée** du périmètre par **C32/A2** — elle ne pilote **pas** le besoin de chauffe des chambres ;
- le séjour (`sensor.temperature_sejour`) ;
- l'entrée (`sensor.temperature_entree`) ;
- la petite maison (`sensor.temperature_petite_maison`) ;
- le rez-de-chaussée et l'agrégat `sensor.temperature_max_rdc` ;
- toute autre façade ou zone intérieure, présente ou future, **non ajoutée par une évolution contractuelle explicite** de ce document.

Le périmètre **ne doit jamais** être formulé comme « toutes les températures intérieures », « l'intérieur de la maison », « la température de l'étage » ou « une température globale ».

L'ajout ou le retrait d'une chambre du périmètre est une **modification normative de ce contrat**, jamais un effet de bord d'implémentation.

---

## 3. Dépendances normatives

Ce contrat **consomme** les façades du §2 telles qu'elles sont produites par la chaîne générique de **température intérieure par zone** :

- consolidation des sources par zone ;
- stabilisation par zone ;
- projection en façade par zone ;
- règles de disponibilité et d'abstention des sources.

Ce contrat **ne redéfinit pas**, pour les façades sources :

- leur validation ni leur plage de plausibilité ;
- leur TTL ni leur mémoire bornée ;
- leur fraîcheur ;
- leur mécanisme d'abstention.

La **fraîcheur temporelle** des mesures est donc **entièrement héritée des façades** (cf. §6). Ce contrat gouverne uniquement l'**agrégation spatiale bornée** de ces façades et sa **couverture**.

> Autorités des façades sources : `consolidation.md`, `stabilisation.md` (dossier `meteo/temperature_interieure/`).

---

## 4. Définitions

- **Façade exploitable** : une des deux façades du §2 dont l'état est une **valeur numérique** (ni `unknown`, ni `unavailable`, ni non numérique).
- **Ensemble des façades exploitables** : le sous-ensemble des deux façades qui sont exploitables à l'instant de l'évaluation (cardinal 0 à 2).
- **Borne MIN** : la **plus basse** des valeurs numériques des façades exploitables.
- **Borne MAX** : la **plus haute** des valeurs numériques des façades exploitables.
- **Couverture complète** : les **deux** façades sont exploitables.
- **Couverture partielle** : **une ou deux** façades exploitables.
- **Perte totale de couverture** : **zéro** façade exploitable.
- **Contexte de l'extrême** : information identifiant la chambre ou les chambres dont la façade exploitable porte la valeur de la borne concernée.
- **Sources utilisées** : la liste des façades effectivement retenues dans le calcul courant.

---

## 5. Calcul

Règles normatives :

- **MIN** = minimum des valeurs numériques des **façades exploitables** ;
- **MAX** = maximum des valeurs numériques des **façades exploitables** ;
- une façade **indisponible ou non numérique** est **exclue** du calcul ;
- **une seule** façade exploitable **suffit** à produire MIN et MAX ;
- avec une seule façade exploitable, **MIN et MAX peuvent être identiques** ;
- **aucune** façade hors périmètre (§2) ne participe au calcul ;
- aucune transformation métier de la valeur (pas de seuil, pas de couleur, pas de catégorie) n'est effectuée ici (cf. §11) ;
- une égalité entre plusieurs chambres sur la valeur extrême **ne crée aucune ambiguïté** sur la valeur produite : MIN reste le minimum mathématique et MAX le maximum mathématique.

---

## 6. Mémoire et fraîcheur

**Interdictions absolues** pour les deux bornes :

- **aucune mémoire propre** aux agrégats ;
- **aucun usage de l'état précédent** (`this.state`) comme continuité fonctionnelle ;
- **aucune républication** d'une ancienne valeur ;
- **aucun TTL propre** à l'agrégat ;
- **aucune horloge propre** ;
- **aucun nouvel horodatage** ni helper temporel dédié ;
- **aucun canal de confiance parallèle**.

La **fraîcheur temporelle** est héritée **exclusivement** des façades (§3). Les bornes ne recréent **aucune** politique de fraîcheur au-dessus de leurs opérandes.

---

## 7. Disponibilité et abstention

Formulation normative :

> **Une borne thermique est exploitable si et seulement si au moins une des deux façades du périmètre est exploitable. Lorsque zéro façade est exploitable, la borne s'abstient et aucun ancien état numérique ne peut être maintenu ou republié.**

Effets attendus :

- en **perte totale de couverture**, la borne est **non exploitable** par les consommateurs ;
- **aucune valeur numérique périmée** n'est conservée ni republiée ;
- dès qu'**une** façade redevient exploitable, la borne **reprend** une valeur numérique (calculée sur les façades exploitables).

> **Résultat normatif vs mécanisme.** Ce contrat fixe le **résultat** (« non exploitable, sans valeur périmée, lorsque zéro façade n'est exploitable »). Il **ne fige pas** le mécanisme Home Assistant (`availability`, `unknown`, ou autre) : le choix concret relève de l'audit d'implémentation ultérieur, sous réserve de produire ce résultat normatif.

---

## 8. Cycle de vie

Comportements attendus, dérivés du §7 :

1. **Démarrage sans aucune façade exploitable** → borne **non exploitable** (aucune valeur numérique).
2. **Apparition de la première façade** → borne exploitable ; MIN = MAX = valeur de cette façade.
3. **Apparition progressive des autres façades** → recalcul sur l'ensemble des façades exploitables.
4. **Perte d'une ou deux façades** → recalcul sur les **façades restantes exploitables** (couverture partielle) ; la borne reste exploitable.
5. **Perte des deux façades** → **abstention** ; aucune ancienne valeur maintenue.
6. **Retour d'une façade après perte totale** → reprise immédiate d'une valeur numérique.
7. **Rechargement des templates** → aucun état numérique périmé restauré ; l'exploitabilité découle de l'état courant des façades.
8. **Redémarrage Home Assistant** → idem : aucune valeur périmée ne survit fonctionnellement à une perte totale de couverture.

> **Invariant de survie :** aucune ancienne valeur ne doit survivre **fonctionnellement** à une perte totale de couverture.

---

## 9. Couverture observable

Les bornes exposent une **observabilité de couverture**, dont la **sémantique est obligatoire** même si les identifiants d'attributs exacts sont déterminés à l'implémentation :

- **nombre de façades exploitables** (0 à 3) ;
- **nombre de façades attendues**, contractuellement **égal à deux** ;
- **sources réellement utilisées** dans le calcul courant ;
- **contexte de l'extrême**, permettant d'identifier la chambre ou les chambres portant la valeur de la borne concernée, selon une représentation déterministe définie à l'implémentation.

Ne sont **pas** requis (et ne doivent pas être ajoutés par principe) :

- un attribut de « couverture complète » redondant avec le nombre de façades exploitables ;
- une liste de fraîcheur ou un âge (portés par les façades, §6) ;
- une mémoire ou une entité compagnon dédiée.

Les **noms YAML exacts** de ces attributs peuvent rester à déterminer lors de l'audit d'implémentation si aucune convention stable ne s'impose ; leur **sémantique**, elle, est **obligatoire et non ambiguë**.

---

## 10. Consommateurs

Familles de consommateurs établies des bornes :

- **Chauffage** ;
- **Climatisation** ;
- **Aération** ;
- **point de rosée** ;
- **UI** (dont les deux cartes du dashboard Arsenal) ;
- **diagnostic** éventuel.

Principes :

- ce contrat produit une **vérité honnête** et **ne maintient jamais** une valeur périmée pour satisfaire un consommateur ;
- **chaque consommateur** reste responsable de sa **propre abstention ou fallback** lorsque la borne est non exploitable ;
- la **compatibilité runtime** des gardes existantes des consommateurs devra être **auditée avant mise en œuvre** ; ce contrat **ne présente pas** ces gardes comme validées en conditions réelles.

---

## 11. Séparation des responsabilités

Ce contrat **ne gouverne pas** :

- les catégories thermiques `froid`, `chaud`, `neutre` ;
- les références physiques basse et haute des catégories ;
- les couleurs et l'Exception 2 thermique ;
- le dashboard Arsenal ni aucun rendu UI ;
- le Chauffage, la Climatisation, ni aucune de leurs vérités ;
- les besoins, admissibilités, autorisations, décisions ou actions HVAC.

Ces éléments relèvent du **contrat de restitution** (à venir) ou des **contrats de leurs domaines respectifs**.

---

## 12. Invariants opposables

*(Convention d'identifiant : `INV-BTE-*` — Bornes Thermiques Étage ; alignée sur les contrats de production météo à identifiants `INV-*`.)*

- **INV-BTE-1** — Le périmètre est **exactement** les **deux** chambres de l'étage : **Chambre Enfants** (`chambre_enfants`) et **Chambre Parents** (`chambre_parents`) ; la **Salle de Jeux** (`salle_de_jeux`) et toute autre façade ne participent pas.
- **INV-BTE-2** — Le calcul n'utilise que les **façades exploitables** (valeur numérique) ; les façades non numériques sont exclues.
- **INV-BTE-3** — Les bornes sont **exploitables dès qu'au moins une** façade du périmètre est exploitable.
- **INV-BTE-4** — MIN est le **minimum** et MAX le **maximum** des valeurs numériques des façades exploitables.
- **INV-BTE-5** — **Aucune mémoire propre** : ni continuité via l'état précédent, ni valeur reconstruite.
- **INV-BTE-6** — **Aucune républication** d'une ancienne valeur.
- **INV-BTE-7** — **Aucun TTL ni horloge propre** à l'agrégat.
- **INV-BTE-8** — En **perte totale de couverture**, les bornes **s'abstiennent** (non exploitables, sans valeur périmée).
- **INV-BTE-9** — La **couverture partielle est observable** (nombre de façades exploitables / attendues, sources utilisées).
- **INV-BTE-10** — La **fraîcheur** est **héritée des façades** ; l'agrégat n'en produit aucune.
- **INV-BTE-11** — **Aucune logique HVAC** (besoin, admissibilité, autorisation, décision, action), ni dépendance à la présence ou au mode de la maison.
- **INV-BTE-12** — **Aucune sémantique de couleur ni catégorie thermique** (`froid/neutre/chaud`) n'est produite par ce contrat.

---

## 13. Interdictions

Il est **strictement interdit** :

- d'ajouter silencieusement une nouvelle pièce au périmètre ;
- d'inclure le RDC (séjour, entrée) ou `sensor.temperature_max_rdc` ;
- d'inclure la petite maison ;
- de recourir à un **fallback vers une autre zone** en cas de perte de couverture ;
- de **maintenir ou republier** une ancienne valeur numérique ;
- d'introduire un **second TTL**, une horloge, ou un horodatage propre ;
- de mémoriser un **nouvel état** dérivé ;
- de **reconstruire une fraîcheur** au niveau de l'agrégat ;
- d'introduire une **logique de couleur** ou de **catégorie thermique** ;
- d'introduire une **logique décisionnelle HVAC** ;
- de rendre les bornes **dépendantes de la présence** ou du **mode** de la maison.

Toute violation constitue une **non-conformité contractuelle**.

---

## 14. Critères de conformité

Une implémentation est **conforme** si, sans écrire ici le YAML ni le checker, elle satisfait tout ce qui suit :

- le calcul ne lit **que** les deux façades du §2 ;
- MIN/MAX sont les extrêmes mathématiques des façades exploitables ;
- une seule façade exploitable produit des bornes valides (MIN/MAX possiblement égales) ;
- aucune valeur n'est produite lorsque zéro façade est exploitable, et aucune ancienne valeur n'est republiée ;
- après rechargement ou redémarrage, aucune valeur périmée ne survit à une perte totale de couverture ;
- la couverture est observable : façades exploitables, façades attendues, sources utilisées, contexte de l'extrême ;
- aucune mémoire, aucun TTL, aucune horloge, aucune couleur, aucune catégorie thermique, aucune logique HVAC n'est présente ;
- les invariants `INV-BTE-1…12` sont vérifiables.

---

## 15. Hors périmètre

Sont **hors** de ce contrat (traités ailleurs) :

- le **contrat de restitution** des bornes (sémantique et couleur) ;
- les **références physiques** basse et haute des catégories ;
- les **catégories backend** `froid` / `neutre` / `chaud` ;
- le **mapping UI** et l'Exception 2 thermique ;
- le **renommage** des entités historiques (`…_chambre_enfants → …_chambre_enfants`), porté par **C32/L3** — conservées ici en forme historique ;
- l'**implémentation runtime**, les **checkers** et la **CI** ;
- les **autres agrégats spatiaux** (RDC, petite maison, étage élargi) ;
- le **RDC** et la **petite maison**.

---

## 16. Synthèse

> **Les bornes `temperature_min_chambres` et `temperature_max_chambres` sont les extrêmes thermiques honnêtes des deux chambres de l'étage : calculées uniquement sur les façades exploitables, valides dès une seule d'entre elles, sans mémoire ni horloge propres, s'abstenant lorsque toutes les façades se sont abstenues, et n'embarquant aucune logique de couleur ni de décision HVAC.**

---

## 📌 Statut & évolution

- Contrat Arsenal, **normatif et opposable**.
- Domaine : Météo — température intérieure, sous-ensemble spatial (chambres de l'étage).
- Dépendances : `consolidation.md`, `stabilisation.md` (façades sources).
- Toute évolution du **périmètre** ou des **invariants** exige une modification explicite de ce contrat, une validation humaine et la traçabilité documentaire requise par la gouvernance Arsenal.
