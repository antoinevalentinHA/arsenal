# Architecture des notifications — **V3**

> **Aucune correction V3 sur ce fichier.**

> **Corrections V2 :** comportement réel après suppression manuelle, ajouté
> pour le canal de mission (§3.1) et corrigé pour le canal d'entretien (§4.3) ;
> variante de la couche centrale nommée et sa limite consignée (§5) ; cycle de
> vie du canal de mission réindexé sur les classes de la machine (§3).

Décisions acquises : D-26 à D-30.
Contrat opposable : `00_documentation_arsenal/contrats/notifications.md`.
Contrôles mécaniques : `scripts/arsenal_contracts/check_notifications_contracts.py`.

---

## 1. Les trois canaux

| # | Situation | Nature informationnelle | Canal | Identifiant de notification |
|---|---|---|---|---|
| 1 | Mission Arsenal en cycle | **état** | persistante **temporaire** | `aspirateur_mission` |
| 2 | Entretien requis | **état** | persistante **durable agrégée** | `aspirateur_entretien` |
| 3 | Erreur ou interruption urgente | **événement** | **mobile** opérateur | — |

Les trois décisions opérateur coïncident exactement avec la correspondance
normative du contrat : *un état se restitue par un canal persistant, un
événement par un canal éphémère*. Aucune dérogation n'est demandée.

---

## 2. Contraintes de forme opposables

| Contrainte | Origine | Application |
|---|---|---|
| Titre : emoji de domaine en tête | contrat + contrôle `T1`, `T6` | `🤖 Aspirateur – Mission en cours` · `🧰 Aspirateur – Entretien requis` |
| Séparateur **demi-cadratin** `–`, cadratin `—` **interdit** | contrôle `T2` | à respecter littéralement |
| Aucune formulation événementielle dans le titre | contrôle `T3` | mots refusés par le contrôle : *relance*, *arrêt*, *tentative*, *échoué*, *mise à jour*, *déblocage*, *redémarrage* |
| Aucune référence temporelle dans le bloc de création | contrôle `T4` | proscrit : horodatage courant, conversion d'horodatage, formatage de date, temps relatif, delta |
| Identifiant présent dans moins de quatre fichiers | contrôle `T5` | deux identifiants, chacun dans une seule automation |
| Aucun service de notification en dur | contrat + usage du dépôt | passage obligé par la couche d'abstraction centrale, cible résolue depuis un helper |

> **Piège de nommage.** Le mot **`arrêt`** est refusé dans un titre persistant.
> Une notification liée à un geste d'arrêt devra être formulée comme un
> **état**, jamais comme l'action qui l'a produit — ce que le contrat exige
> de toute façon.

---

## 3. Notification de mission — canal 1

**Source d'état :** le verdict persistant, mémoire de supervision (D-08).

| Étape du cycle de vie | Comportement |
|---|---|
| **Apparition** | Le verdict entre en **classe O** — mission Arsenal ouverte (`07_MACHINE_L2.md` §4.1) |
| **Maintien** | Tant que le verdict reste en classe O, sous-classe de chaîne de retour comprise |
| **Extinction** | **À toute valeur de classe T**, sans exception : les deux clôtures confirmées, les deux clôtures non confirmées, les deux échecs de supervision, et la clôture opaque de redémarrage |

**Anti-doublon.** La création d'une notification persistante **remplace** à
identifiant identique. L'anti-doublon est **structurel** : il n'y a rien à
construire, et rien ne peut s'empiler.

**Recalculabilité forte — satisfaite.** Le verdict est un helper textuel sans
valeur initiale déclarée : il est **restauré** au démarrage. La notification
se recalcule donc à partir du **seul état courant**, sans historique, sans
mémoire implicite et sans dépendance à une action passée.

**Réconciliation au démarrage.** Home Assistant ne restaure pas les
notifications persistantes. La re-projection est portée par le déclencheur
d'état stable du système, selon le patron de référence du dépôt. Elle applique
la table de réconciliation de `07_MACHINE_L2.md` §6 : **rien** sur un verdict de
classe T ou H, re-projection sur un verdict de classe O cohérent avec l'état
machine, **extinction** sur une chaîne devenue opaque.

### 3.1 Suppression manuelle de la persistante de mission — **ajouté en V2**

> La V1 ne disait **rien** de ce cas sur le canal de mission.

**Déclencheurs de cette projection :** tout changement du verdict, plus le
passage à l'état stable du système. **Rien d'autre.**

**Comportement réel, énoncé sans embellissement :**

> Une suppression manuelle de la notification de mission **tient jusqu'au
> prochain changement de verdict ou au prochain redémarrage.**

En pratique la fenêtre est courte : pendant une mission, le verdict bouge à
chaque geste, et l'issue terminale finit par arriver. Mais elle **n'est pas
nulle**, et la V2 ne prétend pas le contraire.

**Ce que cela ne casse pas.** La recalculabilité forte reste satisfaite : la
notification est **recalculée** à partir du seul verdict courant à chaque
évaluation. Aucun acquittement n'est mémorisé.

---

## 4. Notification d'entretien — canal 2

### 4.1 Les six exigences, une par une

| Exigence | Réponse |
|---|---|
| **Créée sans doublon** | Identifiant stable ⇒ remplacement natif |
| **Mise à jour quand la situation évolue** | Le message recense la **liste des éléments dus**, et rien d'autre |
| **Disparaît quand tout est soldé** | Le témoin binaire d'entretien requis repasse à faux ⇒ suppression |
| **Comportement défini au redémarrage** | Re-projection sur l'état stable ; la source est l'appareil ⇒ recalculabilité forte satisfaite |
| **Pas recréée à chaque interrogation** | Voir §4.2 — c'est le point de conception |
| **Acquittement manuel** | Voir §4.3 |

### 4.2 Ne pas être recréée à chaque interrogation

**Le problème.** Le coordinateur rafraîchit les quatre compteurs
simultanément, à une cadence **nominale** de 30 s en local ou 60 s en repli
nuage — sans borne supérieure garantie. Déclencher l'automation sur les
capteurs bruts la ferait réécrire la notification à chaque cycle.

**La solution : interposer deux entités dérivées.**

| Entité dérivée | Rôle |
|---|---|
| `sensor.aspirateur_entretien_du` | **Liste canonique** des éléments dus, en libellés Arsenal |
| `binary_sensor.aspirateur_entretien_requis` | Vrai si la liste n'est pas vide |

> **Trois situations, jamais deux — ajouté en V2.** Un compteur dont la donnée
> protocolaire est absente rend le capteur **indisponible**, et non nul. Les
> deux entités dérivées doivent donc distinguer **dû**, **non dû** et **non
> évaluable**, faute de quoi un trou d'information serait lu comme « non dû »,
> contre `ASP-INV-45`. Voir `06_ENTITES_ENTRETIEN.md` §8.1.
>
> **Conséquence sur cette notification :** elle ne doit pas disparaître au motif
> qu'un compteur est devenu illisible.

L'automation de projection ne se déclenche que sur **ces deux entités**, dont
l'état ne change qu'au **franchissement de seuil** — jamais au rythme du
coordinateur.

**Corollaire de forme.** Le message **ne porte aucune durée restante chiffrée**.
Deux raisons, toutes deux suffisantes : une durée changerait à chaque cycle et
réécrirait la notification en permanence ; et une notification persistante
décrit un **état**, pas une mesure qui court.

### 4.3 Acquittement manuel — traitement honnête

**Aucun helper d'acquittement ni de report n'est créé** (D-30).

Ce n'est pas seulement une décision de sobriété : c'est **la seule option
conforme**. Le test de recalculabilité forte du contrat interdit qu'une
notification persistante dépende *d'une action utilisateur*. Un acquittement
mémorisé serait donc contractuellement invalide.

**Comportement retenu — corrigé en V2.**

> Une suppression manuelle **tient jusqu'au prochain changement de la liste des
> éléments dus, ou au prochain redémarrage.**

C'est la **conséquence assumée** du choix de déclencheurs du §4.2 : puisque la
projection ne se réveille qu'au franchissement d'un seuil, aucune évaluation
n'a lieu tant qu'aucun seuil ne bouge. **Le délai peut donc se compter en
semaines.**

**Le message doit le dire**, pour que ce comportement soit compris plutôt que
subi.

> **Correction V2.** La V1 promettait une re-projection « à la prochaine
> évaluation », ce que ses propres déclencheurs contredisaient. La conception
> était bonne ; c'est la promesse qui était trop forte.

**Ce qui ne change pas.** Aucun acquittement n'est **mémorisé** : rien n'est
stocké, rien ne dépend d'une action passée, et la recalculabilité forte reste
satisfaite. La seule façon de faire disparaître durablement la notification est
de **solder l'entretien** — solde confirmé par relecture du compteur, non
déclaré sur parole.

### 4.4 Conséquence connue du déploiement

L'élément « nettoyage des capteurs » est consommé à **86,6 %**. Tout seuil
raisonnable rendra la notification **immédiatement due**. Ce n'est pas une
notification de test — c'est une projection d'état réelle et légitime — mais
il faut le savoir avant de déployer. Voir arbitrage **A-1**.

---

## 5. Canal mobile — canal 3

**Réservé aux événements** : `ECHEC/MISSION_INTERROMPUE` et
`ECHEC/ERREUR_EN_MISSION`.

**Jamais** pour : une échéance d'entretien (D-29, et interdiction contractuelle
du push pour un état durable), une clôture nominale, une clôture confirmée,
un refus de lancement.

**Voie d'appel.** Le dépôt n'autorise **aucun** service de notification en dur.
L'appel passe par la couche d'abstraction centrale, avec pour cible le helper
textuel qui porte le service de l'opérateur. Un changement de téléphone ne
touche aucun fichier du domaine.

**Variante retenue — précisé en V2.** La couche centrale expose trois variantes.
La proposition retient **la variante simple** — titre et message —, qui suffit
aux deux événements du domaine.

> **Limite à consigner, et non masquée.** Cette variante **ne garde pas** la
> valeur du helper cible : un helper à l'état inconnu produirait un appel de
> service invalide. Seule la variante avancée porte une garde vérifiant que la
> valeur est bien une chaîne préfixée par le domaine de notification.
>
> Le choix entre « accepter cette limite » et « retenir la variante avancée pour
> sa garde » est un **détail d'implémentation**, non un arbitrage de cadrage —
> mais il doit être **écrit** dans le lot, pas laissé au hasard de la rédaction.

**Titre mobile.** Soumis à la même règle d'emoji de tête que les persistantes.

---

## 6. Erreurs de dock et de vidage

Décision D-16 : Arsenal peut **observer et notifier une erreur** de dock ou de
vidage si un signal fiable existe.

**Le signal existe déjà et il est déjà contractualisé.** Le témoin d'erreur de
dock porte une énumération fermée de onze valeurs, dont quatre sont exactement
des défauts de vidage : absence de bac, absence de bac ou de filtre, obstruction
du conduit, défaut de ventilateur de vidage. Sa valeur nominale est arrêtée par
`ARB-5`, et le moteur L1 la lit **déjà** comme condition de lancement.

**Rien n'est à créer.** Le lot Notifications n'a qu'à router les valeurs non
nominales vers le canal d'alerte robot/dock déjà décidé.

**Deux bornes d'honnêteté, à écrire :**

1. Un vidage **en cours** n'est pas observable : le champ correspondant du
   protocole n'est exposé par **aucune entité**. Seule l'**erreur** est visible.
2. Arsenal **ne voit pas** la fenêtre d'heures interdites : les entités qui la
   porteraient sont désactivées. **Aucune alerte d'absence de vidage ne doit
   donc jamais être construite** — pendant la fenêtre, un silence est nominal,
   et le système ne peut pas le distinguer d'une panne.

**Reste ouvert :** une erreur de dock justifie-t-elle un envoi **mobile**, ou
seulement le refus de lancement déjà en place ? Arbitrage **A-8**.

---

## 7. Ce que l'architecture ne fait pas

- Aucune notification n'écrit un verdict. Les deux projections sont des
  **lecteurs purs**.
- Aucune notification persistante ne porte d'horodatage, de compteur, de numéro
  de tentative ni de référence à un fait passé.
- Aucune notification ne remplace un dashboard ni un diagnostic.
- Aucune notification n'est émise en phase de cadrage : **aucun objet de ce
  document n'existe dans le dépôt**.
