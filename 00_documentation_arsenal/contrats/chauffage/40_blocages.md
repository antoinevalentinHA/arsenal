# ARSENAL — Contrat Normatif de Domaine
## Chauffage — Blocages & Interdictions Hiérarchiques V3

**Statut :** Contrat normatif de domaine — sûreté hiérarchique chauffage — opposable  
**Subordonné à :** [`contrats/chauffage/00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)  
**Utilisé par :** [`contrats/chauffage/30_decision_centrale.md`](30_decision_centrale.md)  
**Complémentaire de :** [`45_aeration.md`](45_aeration.md) · [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) · [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)  
**Date :** 2026-04-07

---

## 1. Objet du contrat

Ce contrat définit le comportement normatif des blocages hiérarchiques du sous-système Chauffage Arsenal.

Il formalise :

- la liste officielle des contextes bloquants,
- leur priorité absolue,
- leurs effets normatifs,
- leurs interactions avec la décision centrale,
- leurs garde-fous temporels.

Ces mécanismes constituent la **couche de sûreté hiérarchique** du système.

---

## 2. Rôle des blocages

Les blocages garantissent la cohérence thermique globale, évitent toute chauffe illégitime, préviennent les incohérences fonctionnelles, et assurent la sobriété structurelle.

Principes cardinaux :

- un blocage écrase toujours une autorisation ordinaire,
- un blocage écrase toujours une opportunité de confort ordinaire,
- un blocage ne peut jamais être contourné par une logique locale.

---

## 3. Position hiérarchique

Les blocages appartiennent au **niveau hiérarchique supérieur**. Ils sont évalués avant toute autorisation, avant toute décision confort, avant toute inhibition géofencing.

> Tant qu'un blocage pur est actif, toute décision de confort est strictement interdite.

---

## 4. Taxonomie des contextes contraignants

Ce contrat distingue deux natures :

**Blocages purs** : effet contraignant absolu sur la décision, pouvant être soit une contrainte en `reduced`, soit une abstention forcée selon la nature du blocage.

**Contextes majeurs à effet conditionnel** : effet nominal `reduced`, mais susceptibles de porter une exception normative explicite et documentée. Vacances appartient à cette catégorie.

Cette distinction est intentionnelle et opposable. Aucune exception implicite n'existe dans aucune des deux catégories.

---

## 5. Blocages purs

### 5.1 Fenêtres ouvertes

**Contexte :** une ou plusieurs fenêtres ouvertes, délai de stabilisation éventuellement actif.

**Objectifs :** éviter une chauffe vers l'extérieur, empêcher toute compensation absurde.

**Effet normatif :** décision forcée en `reduced`. Toute autorisation `comfort` est ignorée.

---

### 5.2 Épisode d'aération

**Contexte :** aération en cours, ou blocage post-aération actif.

**Objectifs :** préserver la dynamique thermique, éviter toute reprise prématurée, respecter l'inertie du bâti.

**Effet normatif :** décision forcée en `reduced`. Interdiction de toute reprise automatique. Temporisation obligatoire post-aération.

---

### 5.3 Poêle — blocage événementiel temporisé

**Contexte :** détection événementielle de fonctionnement du poêle.

**Caractéristiques architecturales :**

- le capteur poêle est strictement événementiel,
- le passage OFF est volontairement ignoré,
- aucune lecture thermique n'est effectuée,
- aucune estimation d'inertie n'est produite,
- aucune mémoire inter-cycle n'existe.

Le blocage est déclenché uniquement par événement ON, maintenu exclusivement par la durée du timer, levé uniquement à expiration du timer, totalement indépendant de l'état réel du poêle.

**Objectifs :** éviter toute double source de chauffe, prévenir une reprise prématurée, laisser se dissiper l'effet thermique du poêle.

**Effet normatif :** décision forcée en `reduced`. Toute autorisation `comfort` est ignorée. toute inhibition géofencing est sans effet. Aucune reprise automatique autorisée avant fin du timer.

---

### 5.4 Interdiction système chauffage

**Contexte :** chauffage global non autorisé système, maintenance, défaut critique.

**Objectifs :** préserver l'intégrité matérielle, éviter toute action risquée, garantir la sûreté système.

**Effet normatif :** décision strictement interdite. Aucun changement de programme autorisé. Abstention forcée.

---

## 6. Contexte majeur à effet conditionnel

### 6.1 Mode maison = Vacances

**Contexte :** maison déclarée en mode Vacances.

**Objectifs :** imposer une sobriété maximale, supprimer toute recherche de confort ordinaire, garantir une gestion minimale sécurisée.

**Effet normatif nominal :** décision forcée en `reduced`. Inhibition géofencing interdite.

**Exception normative explicite :** si `input_boolean.pre_confort_actif_calcule` est actif, la Décision Centrale peut produire `comfort`. Cette exception est bornée : elle ne vaut que dans le bloc Vacances, sous réserve d'absence de tout blocage pur actif, et sous réserve de validation complète par la Décision Centrale.

Cette exception ne constitue pas un contournement hiérarchique. Elle est une règle normative explicite, documentée et opposable, reconnue par `30_decision_centrale.md`.

Aucune autre exception n'existe en contexte Vacances. Toute autorisation ordinaire de confort reste écrasée.

---

## 7. Hystérésis & temporisations

Chaque blocage peut être assorti d'un délai d'activation, d'un délai de désactivation, ou d'une temporisation post-blocage.

Règles cardinales :

- la levée d'un blocage ne constitue jamais, à elle seule, un motif suffisant de reprise,
- aucune transition immédiate autorisée,
- l'inertie thermique est toujours respectée.

Ces règles s'appliquent également au pré-confort Vacances : toute reprise ultérieure, y compris via cette exception normative, doit repasser par la Décision Centrale complète.

---

## 8. Effets normatifs globaux

Lorsqu'un blocage pur est actif :

- la Décision Centrale est contrainte en `reduced`,
- toute autorisation `comfort` ordinaire est ignorée,
- toute inhibition géofencing est sans effet,
- toute opportunité de confort ordinaire est annulée.

Effets interdits :

- aucune reprise automatique par simple levée de blocage,
- aucune montée partielle en confort,
- aucune exception implicite.

L'exception normative du pré-confort Vacances (§6.1) ne relève pas de la logique des blocages purs. Elle est traitée dans le contexte Vacances par la Décision Centrale, après évaluation complète de la hiérarchie.

---

## 9. Autorisations contextuelles & blocages

L'entrée d'un blocage invalide immédiatement toute décision confort en cours. Aucune autorisation active au moment de l'entrée d'un blocage ne peut être mémorisée comme valide ni restaurée automatiquement après fin de blocage.

La fin d'un blocage ne provoque jamais de reprise automatique. Toute reprise ultérieure, y compris via une exception normative, doit repasser par une fenêtre légitime et une validation décisionnelle complète par la Décision Centrale.

---

## 10. Indépendance & neutralité

Les blocages ne connaissent pas les seuils thermiques, ne produisent aucune autorisation, ne déclenchent aucune décision autonome, ne pilotent aucun équipement.

Ils posent une interdiction hiérarchique que la Décision Centrale applique strictement.

---

## 11. Interdictions formelles

Un blocage ne doit jamais : déclencher une chauffe, forcer un confort, court-circuiter la décision centrale, annuler un verrou anti-rebond, ignorer une autre interdiction.

Toute dérive constitue une violation hiérarchique, une régression de sûreté, une erreur critique d'architecture.

---

## 12. Invariants des blocages

- tout blocage supérieur applicable écrase toute autorisation inférieure ordinaire,
- toute reprise par simple levée de blocage est interdite,
- l'effet normatif usuel d'un blocage pur est `reduced`, sans exception,
- les exceptions normatives explicites documentées sont admises uniquement pour les contextes majeurs à effet conditionnel (§6),
- aucune exception implicite n'existe dans aucune catégorie.

Toute violation constitue une perte de maîtrise thermique, une incohérence hiérarchique, une rupture de gouvernance.

---

## 13. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)

**Utilisé par :** [`30_decision_centrale.md`](30_decision_centrale.md)

**Complémentaire de :** [`45_aeration.md`](45_aeration.md) · [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md) · [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)

Gouverne directement : capteurs de blocage fenêtres, helpers poêle, états aération, `binary_sensor.chauffage_autorise_systeme`, toute interdiction hiérarchique du chauffage.

---

## 14. Portée & stabilité

Ce contrat est critique pour la sûreté thermique, stable long terme, modifié uniquement lors d'évolutions majeures, versionné explicitement, et opposable à toute implémentation.

Il constitue la **couche de sûreté hiérarchique officielle du Chauffage Arsenal V3**.
