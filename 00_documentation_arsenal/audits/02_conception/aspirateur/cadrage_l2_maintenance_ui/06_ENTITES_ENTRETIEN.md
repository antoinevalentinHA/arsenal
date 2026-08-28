# Entités d'entretien et plafonds — **V3**

> **Aucune correction V3 sur ce fichier.**

> **Corrections V2 :** le comportement après remise à zéro est reclassé en
> **prédit, non testé** (§5, §8) ; la « borne haute de 60 s » est retirée et
> remplacée par la question réellement ouverte (§6) ; le cas d'une valeur
> absente et d'un capteur indisponible est ajouté (§8.1).

Périmètre V1 : **quatre éléments** (décision D-20). Le vidage en est retiré
(D-14) et qualifié de fonction native autonome (D-13).

---

## 1. Table des entités

Attributs communs aux quatre capteurs : `device_class: duration`,
`entity_category: diagnostic`, unité native **seconde**, unité restituée `h`,
précision d'affichage 2 décimales, **aucun `state_class`**, aucun attribut de
plafond ni d'échéance.

| Élément | Capteur | Bouton de remise à zéro | Champ protocolaire | Attribut de remise à zéro |
|---|---|---|---|---|
| **Filtre** | `sensor.roborock_q7_max_temps_restant_filtre` | `button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air` | `filter_work_time` | `filter_work_time` |
| **Brosse principale** | `sensor.roborock_q7_max_temps_restant_brosse_principale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale` | `main_brush_work_time` | `main_brush_work_time` |
| **Brosse latérale** | `sensor.roborock_q7_max_temps_restant_brosse_laterale` | `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale` | `side_brush_work_time` | `side_brush_work_time` |
| **Nettoyage des capteurs** | `sensor.roborock_q7_max_temps_restant_capteurs` | `button.roborock_q7_max_reinitialiser_le_consommable_du_capteur` | `sensor_dirty_time` | `sensor_dirty_time` |

---

## 2. Plafonds

Constantes littérales de la bibliothèque amont — voir
`04_REFERENCES_SOURCES.md` §2.

| Élément | Constante | Secondes | Heures |
|---|---|---|---|
| Brosse principale | `MAIN_BRUSH_REPLACE_TIME` | 1 080 000 | **300 h** |
| Brosse latérale | `SIDE_BRUSH_REPLACE_TIME` | 720 000 | **200 h** |
| Filtre | `FILTER_REPLACE_TIME` | 540 000 | **150 h** |
| Nettoyage des capteurs | `SENSOR_DIRTY_REPLACE_TIME` | 108 000 | **30 h** |

---

## 3. Vérification croisée — le contrôle falsifiable

Calcul : `restant = plafond − temps de travail cumulé`.

| Élément | Travail cumulé (s) | Plafond (s) | Restant calculé (s) | État d'entité (h) | État × 3 600 (s) | Concordance |
|---|---|---|---|---|---|---|
| Brosse principale | 793 132 | 1 080 000 | **286 868** | 79.6855555555556 | 286 868 | **exacte** |
| Brosse latérale | 51 701 | 720 000 | **668 299** | 185.638611111111 | 668 299 | **exacte** |
| Filtre | 298 747 | 540 000 | **241 253** | 67.0147222222222 | 241 253 | **exacte** |
| Capteurs | 93 553 | 108 000 | **14 447** | 4.01305555555556 | 14 447 | **exacte** |

**Pourquoi ce contrôle falsifie.** Chaque restant observé doit tomber dans
l'intervalle `[0, plafond]` **et** égaler la différence à la seconde près.
Le cas de la brosse latérale est le plus discriminant : son restant vaut
668 299 s, ce qui **exclut** les plafonds 108 000 et 540 000, et n'est
compatible qu'avec 720 000 parmi les quatre constantes du périmètre. Une
erreur d'attribution des constantes serait donc immédiatement visible.

---

## 4. Taux de consommation au relevé

| Élément | Consommé | Restant |
|---|---|---|
| **Nettoyage des capteurs** | **86,62 %** | 13,38 % — 4,01 h |
| Brosse principale | 73,44 % | 26,56 % — 79,69 h |
| Filtre | 55,32 % | 44,68 % — 67,01 h |
| Brosse latérale | 7,18 % | 92,82 % — 185,64 h |

> **Point d'attention pour l'arbitrage A-1.** Tout seuil raisonnable rendra
> l'élément « capteurs » **dû dès le déploiement**.

---

## 5. Sémantique établie

| Question posée | Réponse établie | Source |
|---|---|---|
| Donnée protocolaire d'origine | Temps de travail **cumulé, en secondes**, renvoyé par la commande de lecture des consommables | `04` §3 |
| Calcul du temps restant | `plafond − travail cumulé`, effectué **par la bibliothèque** | `04` §3 |
| Plafond codé en source | **Oui**, littéral | `04` §2 |
| Unité et conversion | Native seconde, restituée en heures par unité suggérée | `04` §4 |
| Sens de variation | **Décroissant**, et **seulement pendant le nettoyage** | déduit de la nature du compteur |
| Seuil natif d'entretien requis | **Aucun.** Le seul repère natif serait zéro | `04` §4 — pas d'attribut d'échéance |
| Commandabilité du capteur | **Non** — capteur pur | — |
| Primitive exacte de remise à zéro | Commande de remise à zéro de consommable, paramètre = **nom du champ de travail** | `04` §5 |
| Comportement après remise à zéro | **PRÉDIT, NON TESTÉ.** Les sources établissent l'envoi de la primitive et la relecture par la bibliothèque ; elles n'établissent **pas** que le micrologiciel remette le champ à zéro. L'attente — remontée exacte au plafond — est une prédiction | `04` §5, fait n° 8 requalifié · voir §8 |
| Confirmation par relecture | **Possible**, mais **différée**, d'un délai **non borné** | `04` §5 et §6 |
| Action immédiate ou réversible | **Immédiate et irréversible** — aucune primitive de restauration | `04` §5 |

---

## 6. Deux niveaux de confirmation, à ne pas confondre

1. **Confirmation de pression.** L'entité de type bouton passe d'un état
   inconnu à un horodatage. Cela atteste que la **pression** a eu lieu.
   **Cela n'atteste rien de l'effet.**
2. **Confirmation d'effet.** Seule la **remontée du compteur au plafond**
   prouve la remise à zéro. C'est la seule confirmation honnête, et c'est
   elle que le script de déclaration doit exiger — d'autant plus que l'effet
   lui-même est **prédit et non testé** (§5).

### Fenêtre de confirmation — **corrigé en V2**

Le bouton de Home Assistant ne force **aucun** rafraîchissement d'entité.
L'entité n'avance donc qu'au cycle suivant du coordinateur.

> **Il n'existe aucune borne supérieure démontrable à ce délai.**
> 30 s en connexion locale et 60 s en repli nuage sont des **périodes nominales
> de planification** : le coordinateur replanifie **à la fin** de chaque
> rafraîchissement, de sorte que l'écart réel vaut au moins l'intervalle
> augmenté de la durée du cycle et d'un décalage d'échelonnement ; un échec ou
> un `retry_after` l'allonge. De plus, **le mode de connexion de l'instance n'a
> pas été relevé**.
>
> *La V1 affirmait « la borne haute est 60 s, la fenêtre doit donc couvrir au
> moins un cycle complet ». Les deux propositions sont retirées : la première
> est fausse, la seconde en découlait.*

**Ce que cela ouvre, et qui n'est pas tranché ici.**

> **Que vaut une confirmation non obtenue sur un acte irréversible et non
> répétable ?**

La remise à zéro est unique, irréversible et sans seconde tentative
(D-23, D-24, D-25). Une fenêtre expirée sur une remise à zéro **réussie**
donnerait un **faux négatif** sur un acte que l'opérateur ne peut pas défaire.
Aucune durée ne supprime ce risque : elle ne fait que le rendre plus ou moins
probable.

L'arbitrage **A-2** porte donc sur le **comportement à l'expiration**, non sur
le choix d'une durée. Il est également établi que le **coût contractuel** d'une
valeur de 30 s ou 60 s est **nul** — `ASP-CI-10` admet déjà ces deux durées, et
`ASP-CI-20` ne balaie que les cinq fichiers L1 —, de sorte que l'invariant des
deux constantes temporelles **n'est pas nécessairement amendé**, contrairement
à ce qu'annonçait la V1.

---

## 7. Éléments hors périmètre, et pourquoi

| Élément | Statut | Motif |
|---|---|---|
| Filtre à charpie du dock | **Absent** | Bouton conditionné à une capacité de lavage que cet appareil n'a pas |
| Brosse de lavage du dock | **Absent** | idem |
| Rouleau de serpillière | **Absent** | Aucun capteur ni bouton créé |
| **Bac à poussière** | **Hors périmètre** | Fonction native autonome — D-13, D-14 |
| Compteur de cycles de vidage | **Proscrit comme durée de vie** | D-17 ; la constante amont vaut 90 alors que le compteur observé vaut 608 — aucune durée de vie n'en est calculable |

---

## 8. Ce qui n'est **pas** établi

- **Le résultat effectif d'une remise à zéro.** Comportement de micrologiciel :
  les sources établissent l'envoi de la primitive et la relecture, **pas** la
  remise à zéro du champ. **Prédit, non testé.** *(Ajouté en V2 : la V1 le
  classait parmi les faits acquis.)*
- **Le délai réel de propagation vers l'entité.** **Aucune borne supérieure
  n'est démontrable.** *(Corrigé en V2 : la V1 le disait « borné par la source
  à un cycle de coordinateur ».)*
- **Le mode de connexion de l'instance** — local ou repli nuage. **Non relevé.**
- Le **seuil métier** d'échéance — arbitrage **A-1**.
- Le comportement des compteurs en cas de remplacement physique **sans** remise
  à zéro : le compteur continue simplement de décroître. Consigné pour mémoire.

### 8.1 Valeur absente et capteur indisponible — **ajouté en V2**

La propriété amont porte une **garde** : si la donnée protocolaire du champ de
travail est absente, la propriété vaut `None`, et **le capteur devient
indisponible** — il ne vaut pas zéro, et il ne conserve pas sa dernière valeur.

**Conséquence de conception, non triviale.**

> Le témoin binaire d'entretien requis **doit classer explicitement** le cas
> indisponible, sous peine de convertir un **trou d'information** en
> « **non dû** ».

C'est l'application directe de `ASP-INV-45` : l'indisponibilité est un état,
pas un trou, et elle ne vaut ni `false`, ni un état nominal, ni la dernière
valeur connue.

**Ce que cela impose au lot M1.** Le capteur de liste des éléments dus et le
témoin binaire doivent distinguer **trois** situations, jamais deux :
élément **dû**, élément **non dû**, élément **non évaluable**. La restitution
de la troisième relève de la même exigence d'honnêteté que le reste du domaine.

**Ce que cela impose au lot N1.** Une notification d'entretien ne doit pas
disparaître au motif qu'un compteur est devenu illisible.
