# CONTRAT ARSENAL — ASPIRATEUR
## 01 — Finalité et périmètre

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Fixer la finalité métier du domaine, l'expérience opérateur cible de
la V1, et les frontières de ce que le domaine couvre.

---

## 1. Finalité

> **Le domaine `aspirateur` existe pour que l'opérateur n'ait plus à ouvrir
> l'application Roborock pour lancer un nettoyage courant.**

Ce n'est pas une finalité d'automatisation : **aucune décision autonome de
nettoyage n'est créée par ce contrat.** Le domaine sert une **intention
opérateur explicite**, exprimée geste par geste, et la porte jusqu'à l'appareil
avec les garanties que l'appareil n'offre pas.

La valeur apportée par Arsenal n'est pas de « pouvoir lancer » — l'application le
fait déjà. Elle est de **refuser proprement ce qui ne peut pas aboutir**, et de
**dire ce qui se passe** pendant et après.

---

## 2. Expérience opérateur cible — V1

L'opérateur doit pouvoir, dans cet ordre :

| # | Geste | Contrat portant la règle |
|---|---|---|
| 1 | **Choisir une carte** | [`02`](02_referentiel_cartes_et_pieces.md), [`06`](06_integrite_mono_carte.md) |
| 2 | **Sélectionner librement une ou plusieurs pièces de cette carte** | [`02`](02_referentiel_cartes_et_pieces.md), [`05`](05_intention_de_mission.md) |
| 3 | **Choisir un profil** | [`03`](03_profils_metier.md) |
| 4 | **Choisir `×1`, `×2` ou `×3`** | [`04`](04_nombre_de_passages.md) |
| 5 | **Lancer la mission** | [`07`](07_moteur_de_mission.md) |
| 6 | **Suivre son état** | [`08`](08_etats_et_observation.md) |
| 7 | **Mettre en pause, reprendre ou arrêter** — selon les capacités réellement exposées | [`08`](08_etats_et_observation.md) |
| 8 | **Demander le retour à la base** lorsque cela a un sens physique | [`08`](08_etats_et_observation.md) |

**Les raccourcis prédéfinis ne sont pas un neuvième geste** : ils **préremplissent**
les gestes 1 à 4 puis appellent le même moteur ([`10`](10_raccourcis.md)).

> **`ASP-INV-1` — un seul chemin de commande.** Quel que soit le point d'entrée
> (sélection libre ou raccourci), **une et une seule** chaîne de validation et
> d'émission existe dans le domaine. Un second chemin est une violation, pas une
> optimisation.

---

## 3. Ce que le domaine couvre

- La **désignation** d'un périmètre de nettoyage (carte + pièces) et sa
  validation.
- Le **réglage** du profil et du nombre de passages, et leur confirmation.
- L'**émission** d'une commande de mission unique, et la qualification de son
  issue.
- La **conduite** d'une mission ouverte : pause, reprise, arrêt, retour à la
  base, selon les capacités réellement exposées.
- L'**observation** honnête de l'état du robot et du dock, et la **restitution**
  d'un diagnostic lisible en cas de refus ou d'échec.

---

## 4. Ce que le domaine ne couvre pas — V1

| Hors couverture | Raison |
|---|---|
| **Toute décision autonome de nettoyage** (planification, déclenchement sur présence, sur salissure, sur absence…) | Aucune intention métier de ce type n'est exprimée. Le domaine sert une demande opérateur. |
| **Le Garage** | Observé dans le runtime — l'entité `image` de la carte existe — mais **sans aucun segment nommé** et **sans besoin V1 exprimé**. Voir §5. |
| **La cartographie** (création, édition, re-cartographie de cartes) | Geste opérateur dans l'application Roborock, hors Home Assistant et hors dépôt. |
| **Les routines Roborock** | Définies hors du dépôt, hors CI et hors contrat ; non paramétrables depuis Home Assistant ; déclenchement obligatoirement par le cloud. Explicitement écartées ([`07`](07_moteur_de_mission.md) §6). |
| **Le nettoyage zoné** (par coordonnées) | Ne satisfait pas la sélection de pièces, et porte une convention de répétition **incompatible** ([`04`](04_nombre_de_passages.md)). |
| **L'historisation** des cycles | Aucune reconstitution a posteriori n'est requise par le besoin. Extension optionnelle, hors chemin critique ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)). |
| **L'entretien** (station de vidange, lavage de serpillière, consommables) | Aucun besoin exprimé ; les prérequis matériels sont **observés**, jamais commandés ([`03`](03_profils_metier.md) §4). |

---

## 5. Le Garage — observé, non qualifié

**Fait retenu de l'audit.** Une carte `Garage` existe : son entité `image` est
exposée, et **sa description ne porte aucune pièce nommée**. La raison de cette
absence n'est pas déterminable en lecture seule.

**Règle opposable.**

> **`ASP-INV-2`** — Le Garage est **observé** et **jamais commandé** en V1.
> Aucun périmètre métier, aucun segment, aucun raccourci, aucun libellé de pièce
> ne lui est attribué par ce contrat.

Cette abstention est **délibérée** : lui inventer un périmètre reviendrait à
créer un référentiel sans preuve. Toute qualification du Garage relève d'un lot
ultérieur, sur besoin exprimé et relevé factuel préalable.

---

## 6. Un seul robot, un seul domaine

**Fait retenu.** Le runtime expose **un seul robot** et son dock. Le domaine est
donc **mono-équipement**.

> **`ASP-INV-3`** — Le domaine `aspirateur` possède **une autorité unique** au
> sens de [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
> §2 : l'**intention opérateur**, portée par le moteur de mission. Aucune autre
> couche — UI, raccourci, automatisme d'un autre domaine — ne décide d'une
> mission.

---

## 7. Dépendance sortante à préserver — domaine alarme

**Fait retenu.** Un consommateur en production existe déjà : l'exclusion de la
détection d'intrusion par mouvement
([`../alarme/50_intrusion_detection.md`](../alarme/50_intrusion_detection.md),
`11_automations/alarme/intrusion/mouvement.yaml`). Depuis sa correction en
production, cette exclusion repose sur l'**état du `vacuum`** — `cleaning` et
`returning` — c'est-à-dire sur le **mouvement réel** du robot.

> **`ASP-INV-4` — non-régression d'un acquis dont l'autorité est ailleurs.**
> Aucun chantier du domaine `aspirateur` ne doit faire régresser cette
> correction, ni ramener l'inhibition d'intrusion sur le témoin de session
> inachevée (`binary_sensor.roborock_q7_max_nettoyage`), dont la sémantique est
> **autre** ([`08`](08_etats_et_observation.md) §3).
>
> **L'autorité sur cette règle n'appartient pas à ce domaine.** Elle est portée
> par **`ALM-ROBO-1`**, dans
> [`../alarme/50_intrusion_detection.md`](../alarme/50_intrusion_detection.md),
> qui en est l'invariant propriétaire. Le domaine `aspirateur` **observe** cette
> contrainte et s'interdit de la contredire ; il ne la réénonce pas, ne l'étend
> pas, et ne légifère pas pour le domaine alarme.
>
> Le domaine `aspirateur` retient de `ALM-ROBO-1` un fait qui lui est **utile en
> propre** : côté entité `vacuum`, `returning_home` **et** `docking` sont tous
> deux mappés sur `returning`, l'état ne devenant `docked` qu'une fois le robot
> posé sur sa base. Ce fait fonde le classement de ces deux états en **classe
> A** ([`07`](07_moteur_de_mission.md) §5.0).

Ce contrat **n'ouvre aucun travail** sur le domaine alarme et n'en modifie
aucune règle.

---

## Renvois

- Référentiel de désignation : [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md)
- Intention de mission : [`05_intention_de_mission.md`](05_intention_de_mission.md)
- Hors périmètre, arbitrages et questions ouvertes : [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)
- Index du domaine : [`README.md`](README.md)
