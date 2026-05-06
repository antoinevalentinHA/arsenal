# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF FONDATEUR
#     CHAUFFAGE — GOUVERNANCE GÉNÉRALE (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF FONDAMENTAL — CONSTITUTION DU DOMAINE CHAUFFAGE
#
# 🔒 AUTORITÉ :
#   Ce document est la RÉFÉRENCE ABSOLUE du sous-système Chauffage Arsenal.
#   Il prime sur tout autre document, contrat de domaine, automatisme,
#   script, capteur ou interface.
#
#   Toute divergence fonctionnelle, sémantique ou architecturale
#   doit être arbitrée à partir de ce document.
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit la **doctrine fondatrice** du sous-système Chauffage Arsenal.

Il établit :

- le modèle mental officiel,
- la séparation des responsabilités,
- la hiérarchie des causes,
- la souveraineté décisionnelle,
- les invariants non négociables,
- la sémantique centrale du domaine thermique.

Il constitue la **constitution du Chauffage Arsenal V3 PRO**.

---

# ----------------------------------------------------------
# 🧠 2. PHILOSOPHIE GÉNÉRALE
# ----------------------------------------------------------

Le système Chauffage Arsenal est un **système décisionnel gouverné**, et non :

- un thermostat classique,
- un correcteur direct par écart,
- un asservissement mécanique continu.

Principes fondateurs :

- la décision thermique est **centralisée**,
- aucune action thermique n’est légitime sans décision récente valide,
- la présence n’est jamais une décision,
- la température n’est jamais une cause directe,
- l’abstention est un état normal,
- la sobriété est un objectif structurel.

Le système vise simultanément :

- le confort en présence,
- la sobriété en absence,
- la **qualité de reprise thermique (éviter le pompage)**,
- la robustesse logicielle,
- la souveraineté vis-à-vis du Cloud.

---

# ----------------------------------------------------------
# 🧱 3. SÉPARATION DES RESPONSABILITÉS
# ----------------------------------------------------------

Le système est structuré selon une séparation stricte.

## 3.1 Faits thermiques

Sources d’observation :

- capteurs de température,
- capteurs de présence,
- états de fenêtres,
- états de poêle,
- états système.

Ils décrivent **ce qui est**.  
Ils ne décident jamais.

---

## 3.2 Autorisation thermique

Une couche intermédiaire produit une **autorisation d’intention** :

- `comfort`
- `neutre`
- `reduced`

Cette couche :

- n’est jamais une décision,
- ne déclenche aucune action,
- ne lit jamais l’état matériel,
- ne connaît pas la table de décision.

Elle définit uniquement **ce qui est autorisé**, jamais ce qui est ordonné.

---

### Producteurs d’autorisation thermique

L’autorisation thermique peut être produite par plusieurs mécanismes amont
explicitement reconnus, sans jamais constituer une décision thermique.

Ces mécanismes :

- ne sont jamais des causes métier,
- ne produisent aucune action directe,
- ne lisent jamais l’état matériel,
- ne connaissent jamais la table de décision,
- se limitent à produire une **autorisation d’intention**.

Sources officiellement reconnues d’autorisation :

#### a) Autorisation manuelle utilisateur

- portée par `input_boolean.mode_confort_chauffage`,
- représente un ordre explicite utilisateur,
- est souveraine vis-à-vis de toute autorisation automatique,
- ne peut jamais être annulée par un mécanisme système.

---

#### b) Inhibition géofencing (préservation de la reprise)

- mécanisme autorisé en contexte Absence,
- documenté en section 5.5,
- simule temporairement une autorisation de confort,
- ne constitue pas une décision autonome.

---

#### c) Pré-confort retour vacances

Mécanisme d’autorisation contextuelle transitoire destiné à anticiper le retour
après une période de Vacances.

Caractéristiques cardinales :

- ne constitue PAS une présence,
- ne constitue PAS une décision thermique,
- ne modifie AUCUN régime officiel,
- ne lève AUCUNE interdiction,
- n’agit que par activation indirecte de `input_boolean.mode_confort_chauffage`.

Conditions normatives d’activation :

- `input_select.mode_maison == "Vacances"`
- `binary_sensor.pre_confort_actif == ON`

Effet autorisé :

- activation automatique de `input_boolean.mode_confort_chauffage`
  uniquement si celui-ci est inactif.

Règles cardinales :

- l’autorisation est strictement bornée temporellement,
- l’autorisation est strictement réversible,
- l’autorisation automatique ne peut jamais annuler un confort utilisateur,
- l’autorisation ne peut jamais prévaloir sur une interdiction NIVEAU 1,
- toute autorisation automatique doit être traçable par une paternité explicite.

Toute autorisation hors de ces règles constitue une violation de la gouvernance amont.

---

## 3.3 Décision centrale

Une autorité unique produit une **décision thermique officielle**.

Elle :

- applique une hiérarchie stricte,
- arbitre les conflits,
- produit une intention légitime,
- est souveraine de toute action.

Toute action thermique doit dériver d’une décision centrale valide.

---

## 3.4 Application matérielle

L’application :

- exécute une décision,
- transmet des commandes au matériel via un protocole local,
- observe le résultat d’exécution,
- ne décide jamais,
- ne modifie jamais l’intention.

Toute application est considérée comme valide uniquement après
réception d’une confirmation explicite d’exécution.

---

# ----------------------------------------------------------
# 🔒 4. SOUVERAINETÉ DÉCISIONNELLE
# ----------------------------------------------------------

Le système Arsenal est **souverain de ses décisions thermiques et de leur validation**.

Règles cardinales :

- aucune décision ne dépend d’un système externe,
- aucune action n’est considérée comme réussie sans validation explicite,
- l’état interne prévaut tant qu’une confirmation d’exécution n’est pas reçue,
- toute divergence est traitée comme un défaut d’exécution, jamais comme une vérité externe.

La décision centrale est :

- unique,
- centrale,
- déterministe,
- traçable,
- opposable.

---

Toute action thermique légitime doit :

- être précédée d’une décision récente,
- être exécutée via une commande traçable,
- être suivie d’une validation explicite (ACK),
- être cohérente avec la table canonique.

---

# ----------------------------------------------------------
# ⚖️ 5. HIÉRARCHIE DES CAUSES (OFFICIELLE)
# ----------------------------------------------------------

La décision est gouvernée par une hiérarchie descendante stricte.

Aucune cause de niveau inférieur ne peut contredire un niveau supérieur.

## 5.1 NIVEAU 1 — INTERDICTIONS ABSOLUES

Causes structurantes bloquantes :

- fenêtre ouverte,
- poêle actif,
- mode vacances,
- épisode d’aération.

Effet normatif :

- chauffage **forcé en `reduced` / eco**,
- toute autre cause est ignorée.

---

## 5.2 NIVEAU 2 — POST-BLOCAGE SYSTÈME

Mécanismes de protection post-interdiction :

- hystérésis de sécurité,
- temporisation système.

Effet normatif :

- maintien de l’interdiction thermique,
- aucune reprise automatique,
- aucune décision confort autorisée.

---

## 5.3 NIVEAU 3 — STANDBY MÉCANIQUE

Mécanisme de stabilisation d’application.

Caractéristiques :

- n’est PAS une cause métier,
- n’est PAS un niveau décisionnel,
- ne produit aucune intention,
- ne peut jamais bloquer une cause métier.

Effet :

- abstention temporaire d’application,
- neutralité stricte.

---

## 5.4 NIVEAU 4 — AUTORISATION DE CONFORT (PRÉSENCE)

La présence :

- autorise un régime confortable,
- ne décide jamais,
- peut produire :
  - `comfort`
  - `neutre`
  - `reduced`

Règle cardinale :

> ⚠️ La présence n’est JAMAIS une décision thermique.

---

## 5.5 NIVEAU 5 — INHIBITION GÉOFENCING (PRÉSERVATION DE LA REPRISE)

Mécanisme de confort différé en absence, destiné à préserver la qualité de la reprise.

Objectif principal :

- empêcher qu’une zone froide ne descende trop bas,
- garantir une reprise en confort **douce et suffisamment rapide**,
- limiter le pompage thermique lors du retour en présence.

Caractéristiques :

- ne vise PAS la protection du bâti,
- ne constitue PAS une décision métier autonome,
- ne modifie PAS le régime d’absence de référence,
- simule temporairement un contexte de présence,
- autorise un passage contrôlé en mode confort en absence.

Ce mécanisme est désigné dans le système comme :

- **inhibition du géofencing**.

---

# ----------------------------------------------------------
# 🌡️ 6. RÉGIMES OFFICIELS
# ----------------------------------------------------------

Le système reconnaît trois régimes fondamentaux.

### Présence

- confort possible,
- sobriété conditionnelle,
- abstention autorisée.

### Absence

- `reduced` par défaut,
- **inhibition géofencing autorisée**,
- aucune recherche permanente de confort.

### Vacances / Interdiction

- `reduced` forcé,
- aucune exception.

En contexte Vacances :

- aucune décision confort n’est autorisée,
- aucune levée d’interdiction n’est permise.

Toutefois, certains mécanismes d’autorisation amont peuvent être actifs
sans constituer une exception de régime ni une décision thermique.

Règles cardinales :

- une autorisation amont active ne modifie jamais le régime Vacances,
- elle ne lève jamais une interdiction NIVEAU 1,
- elle ne constitue jamais une décision thermique,
- elle n’implique aucune simulation de présence,
- elle reste entièrement soumise à la souveraineté décisionnelle centrale.

Le pré-confort retour vacances appartient exclusivement à cette catégorie.

---

# ----------------------------------------------------------
# 🧠 7. ABSTENTION & ÉTAT NEUTRE
# ----------------------------------------------------------

L’abstention est un **état légitime et central** du système.

Définition :

- aucune action thermique requise,
- inertie du bâtiment suffisante,
- stabilité thermique atteinte.

Règles :

- `neutre` est un état normal,
- `neutre` n’est pas une erreur,
- `neutre` n’est pas une attente dégradée,
- `neutre` est un objectif de sobriété.

---

# ----------------------------------------------------------
# 🔁 8. DÉTERMINISME & RAFRAÎCHISSEMENT DÉCISIONNEL
# ----------------------------------------------------------

Toute action thermique légitime doit :

- être précédée d’une décision récente,
- être déclenchée par un trigger référencé,
- être cohérente avec la table canonique.

Règles :

- aucune action sans décision valide,
- aucune décision sans cause référencée,
- aucune transition silencieuse.

---

# ----------------------------------------------------------
# 🧠 9. SÉMANTIQUE CENTRALE
# ----------------------------------------------------------

États thermiques officiels :

- `comfort`   : autorisation haute
- `neutre`    : abstention
- `reduced`   : sobriété / blocage

États fonctionnels :

- attente_confort
- attente_protection
- blocage_thermique

Règles :

- chaque état a une définition unique,
- aucun état implicite n’est autorisé,
- toute UI doit respecter cette sémantique.

---

### Confort forcé (autorisation amont)

Définition :

Autorisation explicite ou contextuelle produisant un état `comfort` en amont
de la décision centrale, sans constituer une décision thermique.

Caractéristiques :

- indépendant de la présence,
- indépendant de la température,
- ne constitue jamais une cause métier,
- ne déclenche aucune action directe,
- reste entièrement soumis à la hiérarchie des causes.

Sources légitimes :

- utilisateur (ordre manuel),
- inhibition géofencing,
- pré-confort retour vacances.

Règles cardinales :

- toute autorisation forcée doit être explicitement traçable,
- toute autorisation forcée doit être strictement réversible,
- toute autorisation automatique doit respecter la souveraineté utilisateur,
- aucune autorisation amont ne peut survivre hors de son contexte légitime.

---

# ----------------------------------------------------------
# 🔒 10. INVARIANTS NON NÉGOCIABLES
# ----------------------------------------------------------

Invariants absolus :

- la décision centrale est unique,
- la présence n’est jamais une décision,
- la température n’est jamais une cause directe,
- aucun mécanisme d’application ne décide,
- aucune reprise automatique post-blocage,
- aucune chauffe implicite hors décision.

La levée d’un blocage doit être explicitement définie
par les contrats de niveau inférieur.

Toute violation constitue :

- une régression architecturale,
- une rupture de gouvernance,
- une erreur critique de conception.

---

# ----------------------------------------------------------
# 🧱 11. HIÉRARCHIE DOCUMENTAIRE
# ----------------------------------------------------------

Ce contrat gouverne :

- tous les contrats de domaine Chauffage,
- tous les triggers décisionnels,
- la décision centrale,
- la table canonique,
- la sémantique thermique.

Il est la racine unique de :

- `/00_documentation_arsenal/contrats/chauffage/*`

---

# ----------------------------------------------------------
# 📌 12. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce document est :

- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **charte constitutionnelle du Chauffage Arsenal V3 PRO**.

# ==========================================================