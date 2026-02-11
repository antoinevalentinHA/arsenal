# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     CHAUFFAGE — BLOCAGES & INTERDICTIONS HIÉRARCHIQUES (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — SÛRETÉ HIÉRARCHIQUE CHAUFFAGE
#
# 🔒 AUTORITÉ :
#   Ce document définit l’ensemble des **blocages et interdictions**
#   applicables au sous-système Chauffage Arsenal.
#
#   Il formalise les contextes dans lesquels toute recherche de confort
#   est interdite, quelle que soit l’autorisation thermique locale.
#
#   Il est OPPOSABLE à toute implémentation :
#     • capteurs de blocage,
#     • helpers d’interdiction,
#     • scripts de décision,
#     • automatismes d’application.
#
#   Subordonné à :
#     /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif des **blocages hiérarchiques**
du sous-système Chauffage Arsenal.

Il formalise :

- la liste officielle des contextes bloquants,
- leur priorité absolue,
- leurs effets normatifs,
- leurs interactions avec la décision centrale,
- leurs garde-fous temporels.

Ces mécanismes constituent la **couche de sûreté hiérarchique** du système.

---

# ----------------------------------------------------------
# 🧠 2. RÔLE DES BLOCAGES
# ----------------------------------------------------------

Les blocages ont pour rôle :

- garantir la cohérence thermique globale,
- éviter toute chauffe illégitime,
- prévenir les incohérences fonctionnelles,
- protéger contre des situations dangereuses ou absurdes,
- assurer la sobriété structurelle.

Principes cardinaux :

- un blocage écrase toujours une autorisation,
- un blocage écrase toujours une opportunité de confort,
- un blocage ne peut jamais être contourné par une logique locale.

---

# ----------------------------------------------------------
# ⚖️ 3. POSITION HIÉRARCHIQUE
# ----------------------------------------------------------

Les blocages appartiennent au :

> 🛑 **NIVEAU HIÉRARCHIQUE SUPÉRIEUR**

Ils sont évalués :

- avant toute autorisation,
- avant toute décision confort,
- avant toute inhibition géofencing.

Règle absolue :

> ⚠️ Tant qu’un blocage est actif,  
> toute décision de confort est strictement interdite.

---

# ----------------------------------------------------------
# 🔒 4. LISTE OFFICIELLE DES BLOCAGES
# ----------------------------------------------------------

Les blocages reconnus officiellement sont :

### 4.1 Fenêtres ouvertes

Contexte :

- une ou plusieurs fenêtres sont ouvertes,
- un délai de stabilisation peut être actif.

Objectifs :

- éviter une chauffe inutile vers l’extérieur,
- empêcher toute compensation absurde.

Effet normatif :

- décision forcée en `reduced`,
- toute autorisation `comfort` est ignorée.

---

### 4.2 Épisode d’aération

Contexte :

- aération en cours,
- ou blocage post-aération actif.

Objectifs :

- préserver la dynamique thermique,
- éviter toute reprise prématurée,
- respecter l’inertie du bâti.

Effet normatif :

- décision forcée en `reduced`,
- interdiction de toute reprise automatique,
- temporisation obligatoire post-aération.

---

### 4.3 Poêle — Blocage événementiel temporisé

Contexte :

- détection événementielle de fonctionnement du poêle,
- activation immédiate d’un verrou de blocage chauffage,
- déclenchement d’un timer de sûreté.

Caractéristiques architecturales :

- le capteur poêle est STRICTEMENT événementiel,
- le passage OFF est volontairement ignoré,
- aucune lecture thermique n’est effectuée,
- aucune estimation d’inertie n’est produite,
- aucune mémoire inter-cycle n’existe.

Le blocage est :

- déclenché uniquement par événement ON,
- maintenu exclusivement par la durée du timer,
- levé uniquement à expiration du timer,
- totalement indépendant de l’état réel du poêle.

Objectifs :

- éviter toute double source de chauffe,
- prévenir une reprise prématurée,
- laisser se dissiper l’effet thermique du poêle,
- garantir une fenêtre de sécurité énergétique.

Effet normatif :

- décision forcée en `reduced`,
- toute autorisation `comfort` est ignorée,
- toute inhibition géofencing est désactivée,
- aucune reprise automatique autorisée avant fin du timer.

---

### 4.4 Mode maison = Vacances

Contexte :

- maison déclarée en mode Vacances.

Objectifs :

- imposer une sobriété maximale,
- supprimer toute recherche de confort,
- garantir une gestion minimale sécurisée.

Effet normatif :

- décision forcée en `reduced`,
- inhibition géofencing interdite,
- aucune exception autorisée.

---

---

### Autorisations amont en contexte Vacances

En contexte `mode_maison = Vacances` :

- toute interdiction hiérarchique demeure absolue,
- aucune autorisation de confort ne peut produire une décision active,
- aucune anticipation ne peut lever un blocage.

Toute autorisation amont active dans ce contexte :

- est immédiatement écrasée par le blocage Vacances,
- ne constitue jamais une exception hiérarchique,
- ne peut jamais produire une reprise anticipée.

Le pré-confort retour vacances :

- ne lève jamais le blocage Vacances,
- ne modifie jamais l’effet normatif `reduced`,
- ne bénéficie d’aucun privilège temporel ou hiérarchique.

---

### 4.5 Interdiction système chauffage

Contexte :

- chauffage global non autorisé système,
- maintenance,
- défaut critique.

Objectifs :

- préserver l’intégrité matérielle,
- éviter toute action risquée,
- garantir la sûreté système.

Effet normatif :

- décision strictement interdite,
- aucun changement de programme autorisé,
- abstention forcée.

---

# ----------------------------------------------------------
# 🔁 5. HYSTÉRÉSIS & TEMPORISATIONS
# ----------------------------------------------------------

Chaque blocage peut être assorti :

- d’un délai d’activation,
- d’un délai de désactivation,
- d’une temporisation post-blocage.

Règles cardinales :

- fin de blocage ≠ reprise automatique,
- aucune transition immédiate autorisée,
- inertie thermique toujours respectée.

Objectifs :

- éviter les oscillations,
- stabiliser le système,
- éliminer les effets yo-yo.

---

# ----------------------------------------------------------
# 🛑 6. EFFETS NORMATIFS GLOBAUX
# ----------------------------------------------------------

Lorsqu’un blocage est actif :

- la Décision Centrale est contrainte en `reduced`,
- toute autorisation `comfort` est ignorée,
- toute inhibition géofencing est désactivée,
- toute opportunité de pré-confort est annulée.

Effets interdits :

- aucune reprise automatique,
- aucune montée partielle en confort,
- aucune exception locale.

---

---

### Autorisations contextuelles automatiques & blocages

Toute autorisation contextuelle automatique active lors de l’entrée d’un blocage :

- est immédiatement annulée,
- ne peut jamais être mémorisée comme valide,
- ne peut jamais être restaurée automatiquement après fin de blocage.

Règles cardinales :

- aucun pré-confort ne peut survivre à l’entrée d’un blocage,
- aucun pré-confort ne peut être réactivé automatiquement après fin de blocage,
- toute réactivation ultérieure doit repasser par une fenêtre légitime
  et une validation décisionnelle complète.

Le pré-confort retour vacances est intégralement soumis à ces règles.

---

# ----------------------------------------------------------
# 🧩 7. INDÉPENDANCE & NEUTRALITÉ
# ----------------------------------------------------------

Les blocages :

- ne connaissent PAS les seuils thermiques,
- ne produisent AUCUNE autorisation,
- ne déclenchent AUCUNE décision autonome,
- ne pilotent AUCUN équipement.

Ils se contentent de :

> 🧠 **POSER UNE INTERDICTION HIÉRARCHIQUE**

que la Décision Centrale applique strictement.

---

# ----------------------------------------------------------
# 🔒 8. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Un blocage ne doit JAMAIS :

- déclencher une chauffe,
- forcer un confort,
- court-circuiter la décision centrale,
- annuler un verrou anti-rebond,
- ignorer une autre interdiction.

Toute dérive constitue :

- une violation hiérarchique,
- une régression de sûreté,
- une erreur critique d’architecture.

---

# ----------------------------------------------------------
# 🧱 9. INVARIANTS DES BLOCAGES
# ----------------------------------------------------------

Invariants absolus :

- tout blocage écrase toute autorisation,
- tout blocage interdit toute reprise automatique,
- un seul effet normatif : `reduced`,
- aucune mémoire inter-cycle non contrôlée,
- aucune exception implicite.

Toute violation constitue :

- une perte de maîtrise thermique,
- une incohérence hiérarchique,
- une rupture de gouvernance.

---

# ----------------------------------------------------------
# 🧠 10. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- utilisé par :
  - `30_decision_centrale.md`

- complémentaire de :
  - `45_aeration.md`
  - `60_absence_inhibition_geofencing.md`
  - `70_autorisation_thermostat.md`

Il gouverne directement :

- les capteurs de blocage fenêtres,
- les helpers poêle,
- les états aération,
- `binary_sensor.chauffage_autorise_systeme`,
- toute interdiction hiérarchique du chauffage.

---

# ----------------------------------------------------------
# 📌 11. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- critique pour la sûreté thermique,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **couche de sûreté hiérarchique officielle  
du Chauffage Arsenal V3 PRO**.

# ==========================================================