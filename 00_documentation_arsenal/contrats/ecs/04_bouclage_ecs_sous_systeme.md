# ↪️ RENVOI — Bouclage ECS (point d'entrée ECS)

> **Ce document n'est pas un contrat autonome.** Le **Bouclage** est un
> sous-système de l'ECS, mais sa **doctrine normative canonique** est tenue dans
> un fichier unique, hors de ce dossier. Ce fichier conserve le **chemin
> historique** comme point d'entrée depuis l'ECS et **ne porte plus aucune
> doctrine autonome**.

## Contrat canonique

➡️ [`../bouclage.md`](../bouclage.md) — *ARSENAL — CONTRAT NORMATIF · ECS — BOUCLAGE*

Toute règle métier, tout invariant, toute machine d'état et tout interdit du
bouclage ECS sont définis **là**, et **uniquement là**. En cas de divergence,
[`../bouclage.md`](../bouclage.md) **fait foi**.

## Pourquoi un renvoi plutôt qu'une doctrine locale ?

- La doctrine que portait historiquement ce fichier (autorisation par **plage
  horaire** : `input_boolean.bouclage_plage_active`,
  `input_datetime.heure_debut_bouclage_ecs`,
  `input_datetime.heure_fin_bouclage_ecs`, présence
  `binary_sensor.presence_famille_unifiee`) **ne correspond plus au runtime** :
  ces objets n'existent plus dans la configuration.
- Le runtime implémente le modèle **AUTO opportuniste** décrit par le contrat
  canonique (`binary_sensor.bouclage_autorise` v2.3 : activation utilisateur du
  sous-système AUTO + disponibilité thermique + occupation stricte foyer ou
  visiteur).
- Conserver deux doctrines concurrentes créait un risque de **divergence** et de
  **référence de vérité ambiguë**. Le renvoi supprime ce risque **sans déplacer
  ni renommer aucun fichier** et **préserve ce chemin** attendu côté ECS.

## Statut

- **Nature** : renvoi documentaire — point d'entrée ECS vers le contrat canonique.
- **Périmètre** : recirculation ECS (sous-système non thermique).
- **Autorité** : aucune en propre — l'autorité normative est portée par
  [`../bouclage.md`](../bouclage.md).
