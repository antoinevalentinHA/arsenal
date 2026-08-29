# Registre des décisions opérateur acquises — **V4, ratifiée**

> ### 2026-08-28 — **`D-44` : ratification du cadrage**
>
> Le bloc **`G bis`** porte l'acte opérateur de ratification. Il **supersède**
> `D-37` sur sa clause d'antériorité et `D-38` en totalité — les deux étant
> **conservées intégralement** et datées, au bloc `F`.
>
> **Aucune autre décision n'est modifiée**, et **aucun arbitrage n'est rouvert**.

> **V4 — quatre décisions ajoutées, aucune retirée ni modifiée.** Le bloc
> **`E bis`** porte les décisions `D-40` à `D-43`, relatives à la place de la
> tuile Aspirateur dans Navigation et à son patron de restitution. Le décompte
> du §G est recalculé en conséquence.
>
> Ces quatre décisions ne sont **pas** des arbitrages rendus : les quinze
> arbitrages `A-1` à `A-15` et leur statut vivent dans
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).

> **Contenu inchangé de la V1 à la V3.2.** Aucune décision n'avait été ajoutée,
> retirée ni modifiée par les corrections d'audit. Décompte de référence au §G.

Ces décisions sont **prises**. Elles ne sont pas rouvertes par le présent
cadrage et ne figurent pas parmi les arbitrages ouverts.
Elles n'ont **aucune traduction dans le dépôt** à ce jour : aucune n'est
implémentée.

---

## A. Conduite et supervision (lot L2)

| Réf. | Décision |
|---|---|
| **D-01** | Le geste de conduite passe par un script dédié, rôle `script.aspirateur_conduire_mission`. |
| **D-02** | Quatre gestes, et quatre seulement : **pause, reprise, arrêt, retour à la base**. |
| **D-03** | Une automation de supervision, intitulée `Aspirateur - Supervision de mission`. |
| **D-04** | Son identifiant est `10280000000001`. |
| **D-05** | **Aucun identifiant supplémentaire n'est inventé.** Tout identifiant nouveau est attribué par l'opérateur. |
| **D-06** | **Aucune mission externe n'est adoptée.** Une activité du robot non ouverte par Arsenal n'est jamais supervisée ni reprise. |
| **D-07** | La **reprise** n'est autorisée que pour une **mission Arsenal ouverte**. |
| **D-08** | Le **verdict persistant** sert de **mémoire de supervision**. |
| **D-09** | **Trois writers** du verdict, à **ensembles de valeurs exactes disjoints**. La disjonction porte sur les valeurs, **pas** sur les préfixes : aucun writer n'est tenu de posséder un préfixe exclusif. |
| **D-10** | `CLOTURE/APRES_ARRET_NON_CONFIRME` et `CLOTURE/APRES_RETOUR_NON_CONFIRME` sont **distincts** et **terminaux**. |
| **D-11** | Les codes du catalogue sont **conservés tels quels**. Il est interdit de leur substituer des préfixes plus commodes pour la CI. Sont notamment conservés : `ECHEC/MISSION_INTERROMPUE`, `ECHEC/ERREUR_EN_MISSION`, `CLOTURE/APRES_ARRET_NON_CONFIRME`, `CLOTURE/APRES_RETOUR_NON_CONFIRME`. |

### Règles de redémarrage — acquises

| Réf. | Règle |
|---|---|
| **D-R1** | Ne **jamais inventer** une transition non observée. |
| **D-R2** | **Poursuivre** une chaîne de retour déjà qualifiée dans le verdict. |
| **D-R3** | **Clôturer honnêtement** une chaîne devenue opaque. |
| **D-R4** | Ne **jamais adopter** une mission externe. |
| **D-R5** | Ne **jamais réarmer** depuis un verdict terminal périmé. |

---

## B. Vidage du bac

| Réf. | Décision |
|---|---|
| **D-12** | **Le dock vide physiquement et automatiquement le bac**, en dehors des heures interdites configurées. Les 608 cycles relevés sont cohérents avec ce fonctionnement réel. *Déclaration opérateur — même régime de preuve que `ARB-3` et `ARB-5` du contrat.* |
| **D-13** | Le vidage **n'est pas un geste physique** de l'opérateur. C'est une **fonction native autonome** du couple robot/dock. |
| **D-14** | Le vidage est **retiré de la V1 Maintenance** et déclaré **non bloquant**. |
| **D-15** | **Aucun** bouton, script, commande brute ou lot Arsenal de vidage n'est créé. |
| **D-16** | Arsenal pourra **seulement observer et notifier** une erreur de dock ou de vidage, **si** un signal fiable existe. |
| **D-17** | `dustCollectionWorkTimes` **ne doit pas** être utilisé comme compteur de durée de vie d'un sac. |
| **D-18** | L'absence de primitive Home Assistant confirmable **n'est plus un manque fonctionnel** pour la V1. |
| **D-19** | Aucune entité ni compteur maison ne sera créé pour le bac. |

---

## C. Périmètre Maintenance V1

| Réf. | Décision |
|---|---|
| **D-20** | Périmètre exact : **filtre**, **brosse principale**, **brosse latérale**, **nettoyage des capteurs**. |
| **D-21** | **Notification persistante agrégée** pour l'entretien. |
| **D-22** | **Déclaration explicite** de l'opérateur après entretien physique. |
| **D-23** | **Remise à zéro unique**, suivie d'une **confirmation par relecture**. |
| **D-24** | **Aucune remise à zéro automatique.** |
| **D-25** | **Aucune répétition automatique.** |

---

## D. Notifications

| Réf. | Décision |
|---|---|
| **D-26** | Mission en cours → notification **persistante temporaire**. |
| **D-27** | Entretien requis → notification **persistante durable agrégée**. |
| **D-28** | Erreur ou interruption urgente → **notification mobile opérateur**. |
| **D-29** | **Aucune notification mobile** pour une échéance normale d'entretien. |
| **D-30** | **Aucun helper d'acquittement ni de report** pour l'instant. |

---

## E. Interface

| Réf. | Décision |
|---|---|
| **D-31** | La carte NAS du dashboard Navigation est **remplacée** par la carte Aspirateur. |
| **D-32** | L'accès NAS est **déplacé** dans le dashboard Système, avec une carte récapitulative et un raccourci vers le dashboard NAS existant. |
| **D-33** | Le dashboard **Navigation** ne porte qu'un **raccourci** Aspirateur — une tuile. Le détail opérationnel vit dans un **dashboard Aspirateur dédié**. |
| **D-34** | **Aucun hub documentaire Aspirateur.** |
| **D-35** | **Aucune entrée Aspirateur Tier 1** dans la carte des domaines. |
| **D-36** | La carte Navigation doit permettre **à terme le lancement**, pas seulement la lecture et la conduite. |

---

## E bis. Navigation et tuile Aspirateur — **ajouté en V4**

| Réf. | Décision |
|---|---|
| **D-40** | **Place de la tuile Aspirateur.** Aspirateur occupe la place actuellement tenue par **Santé**, **à droite de Prises**. **Santé descend en ligne 5.** **NAS quitte Navigation**, son accès étant porté par Système. **Aucune ligne n'est ajoutée** et le dashboard n'est **pas restructuré**. **L'ordre complet de la ligne 5 n'est pas figé.** |
| **D-41** | **Patron de la tuile.** Coloration **dynamique de l'icône**, selon le patron des tuiles dynamiques de Navigation — **jamais** un fond de carte métier. La **logique d'état est produite côté backend** ; la carte Lovelace ne fait que la **restituer**. |
| **D-42** | **Classes d'état et priorité.** Priorité de restitution : **alerte persistante > cycle en cours > nominal**. L'alerte persistante couvre notamment un **entretien dû**. Le **cycle en cours** est un état **distinct**. L'**indisponibilité** est **distinguée** du nominal et **jamais rabattue** sur lui. |
| **D-43** | **Restitution et notification sont indépendantes.** L'absence de notification hors mission décidée en `A-8` **ne supprime pas** la restitution visuelle **rouge** dans Navigation. |

> **Ce que ce bloc ne décide pas.** Ni le vocabulaire d'état, ni la couleur
> exacte, ni le capteur support, ni son emplacement, ni l'ordre de la ligne 5.
> Les contraintes issues des patrons existants sont relevées dans
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §5.3 et
> [`09_UI.md`](09_UI.md) §5.3 ; **les choix restent à l'opérateur**.

---

## F. Discipline de session

> ### ⚠ Passage partiellement caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **`D-37` et `D-38` sont supersédées par `D-44`** (bloc `G bis`), acte de
> ratification du cadrage. Elles sont **conservées intégralement** : elles
> décrivent exactement la discipline appliquée de la V1 à la V4 non ratifiée, et
> c'est cette discipline qui a rendu la ratification possible.
>
> | Réf. | Ce qui reste vrai | Ce qui est supersédé |
> |---|---|---|
> | **`D-37`** | Le cadrage est un **livrable opposable** — `D-44` le **confirme et le renforce** | « **antérieur à toute implémentation** » : la ratification autorise l'implémentation, **lot par lot**, sous les conditions de [`10_LOTS.md`](10_LOTS.md) §5.2 |
> | **`D-38`** | rien — la condition est levée | « la préparation du lot combiné est **interrompue** tant que le cadrage n'est pas audité » : le cadrage **a été audité**, ses réserves corrigées, puis **ratifié** |
>
> **L'autorité courante est `D-44`.**

> ### ⚠ `D-39` — partiellement caduque, conservée pour l'historique, annotée le 2026-08-28
>
> **Cause distincte de celle de `D-37` et `D-38`.** Celles-ci sont supersédées par
> la **ratification** ; `D-39` l'est par l'**intégration documentaire** elle-même,
> et à une autre date.
>
> **Ce constat décrivait l'état antérieur à l'intégration documentaire V4.** Il
> est devenu **caduc dès le premier commit V4**, qui a écrit dans le dépôt.
>
> | Clause de `D-39` | Statut |
> |---|---|
> | « Aucune **écriture de dépôt** » | **Caduque.** La V4 a produit des écritures — **documentaires uniquement**, sous `00_documentation_arsenal/` : le dossier de chantier et l'entrée de navigation `audits/index.md` |
> | « Aucune **commande Home Assistant** » | **Toujours vraie** |
> | « Aucune **notification** » | **Toujours vraie** |
> | « Aucune **commande robot** » | **Toujours vraie** |
>
> **Ce que la V4 n'a écrit nulle part**, et qui borne exactement la caducité :
> **aucune écriture fonctionnelle**, **aucun contrat normatif réel** —
> `14_entretien.md` et `15_conduite_et_supervision.md` restent **décrits, non
> écrits** —, **aucun checker, helper, script, automation ni fichier Lovelace**
> créé ou modifié.
>
> **Autorités applicables :** **`D-44`** pour le statut du cadrage, et l'**état
> Git courant** pour ce qui a réellement été écrit — le commit et son arbre font
> foi, jamais ce paragraphe.

| Réf. | Décision |
|---|---|
| **D-37** | Le cadrage est traité comme un **livrable opposable antérieur à toute implémentation**. |
| **D-38** | La préparation du lot combiné est **interrompue** tant que le cadrage n'est pas audité. |
| **D-39** | Aucune écriture de dépôt, aucune commande Home Assistant, aucune notification, aucune commande robot. |

*(`D-37` et `D-38` : énoncés d'origine, exacts jusqu'au 2026-08-28. Supersédés
par `D-44` — voir l'encadré ci-dessus et le bloc `G bis`.
`D-39` : énoncé d'origine, exact jusqu'au premier commit V4. **Partiellement**
caduque — sa seule clause d'écriture de dépôt — voir l'encadré ci-dessus.)*

---

## G bis. Ratification — **ajouté le 2026-08-28**

| Réf. | Décision |
|---|---|
| **D-44** | **Le cadrage Aspirateur V4 est ratifié.** Il devient la **référence architecturale opposable** pour les futurs lots **L2**, **Maintenance**, **Notifications** et **UI**. **Cette ratification n'autorise aucune implémentation hors du périmètre et des dépendances propres à chaque lot.** |

**Acte opérateur, daté du 2026-08-28.** Il supersède `D-37` sur sa clause
d'antériorité et `D-38` en totalité.

> ### Ce que `D-44` fait, et ce qu'il ne fait pas
>
> | Il fait | Il ne fait pas |
> |---|---|
> | Rend le cadrage **opposable** aux lots à venir | **Rendre tous les lots exécutables** — chaque lot garde ses dépendances propres |
> | Lève la condition de ratification préalable | **Combler** les points restés ouverts ([`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §7) |
> | Permet à un lot **sans dépendance ouverte** de devenir engageable | **Autoriser une implémentation** dans la passe qui le consigne |
> | Confirme la portée **opposable** de `D-37` | Rouvrir un arbitrage, un identifiant, une durée, un writer ou le vocabulaire |
>
> **Un lot engageable n'est pas un lot engagé.** La table d'engageabilité vit
> dans [`10_LOTS.md`](10_LOTS.md) §5.2, et elle se lit lot par lot.

---

## G. Décompte de référence

Ce décompte est la **source de vérité** des compteurs cités ailleurs dans
l'artefact. Il est vérifiable par simple lecture du présent fichier.

| Bloc | Références | Nombre |
|---|---|---|
| A — Conduite et supervision | `D-01` → `D-11` | 11 |
| A — Règles de redémarrage | `D-R1` → `D-R5` | **5** |
| B — Vidage du bac | `D-12` → `D-19` | 8 |
| C — Périmètre Maintenance V1 | `D-20` → `D-25` | 6 |
| D — Notifications | `D-26` → `D-30` | 5 |
| E — Interface | `D-31` → `D-36` | 6 |
| **E bis — Navigation et tuile Aspirateur** *(V4)* | `D-40` → `D-43` | **4** |
| F — Discipline de session | `D-37` → `D-39` | 3 |
| **G bis — Ratification** *(2026-08-28)* | `D-44` | **1** |

**Décisions `D-xx` : 44. Règles `D-Rx` : 5. Total : 49.**
**Vidage et Maintenance réunis (`D-12` → `D-25`) : 14.**

> **Décomptes antérieurs, pour mémoire :** V3.2 — `D-xx` **39**, total **44** ;
> V4 avant ratification — `D-xx` **43**, total **48**.

> **`D-37` et `D-38` restent comptées.** Une décision supersédée n'est pas
> retirée du registre : elle est **datée**, et son autorité est reportée sur
> `D-44`. Le décompte mesure ce que le registre **contient**, jamais ce qui est
> encore en vigueur.

> **Note de numérotation.** Le bloc `E bis` est inséré **après** le bloc `E` par
> cohérence de sujet, alors que ses références `D-40` à `D-43` sont
> **postérieures** à celles du bloc `F` (`D-37` → `D-39`). Les références ne
> sont **jamais** réattribuées : l'ordre des blocs est thématique, celui des
> références est chronologique.

> **Correction V2.** Le manifeste de la V1 annonçait « 12 acquises pour le
> vidage et la maintenance, 36 au total ». Les deux compteurs étaient faux.

---

## Note de traçabilité

Les décisions **D-12 à D-19** corrigent une qualification erronée d'une version
antérieure du cadrage, qui présentait le vidage comme un geste physique opéré
par l'humain. Cette qualification est **retirée**.

**La V2 n'ajoute, ne retire et ne modifie aucune décision.** Les corrections
issues de l'audit portent exclusivement sur des **propositions**, des **faits**
et des **arbitrages** — jamais sur ce registre. En particulier, aucun des six
arbitrages ajoutés (`A-9` à `A-14`) n'a été transformé en décision.

**La V4 ajoute quatre décisions et n'en modifie aucune.** Les décisions `D-40` à
`D-43` portent sur un objet que **nul arbitrage `A-n` ne couvrait** : la place et
le patron de la tuile Aspirateur dans Navigation. **Aucun des quinze arbitrages
n'a été transformé en décision** : leur statut est consigné séparément, dans
[`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).
