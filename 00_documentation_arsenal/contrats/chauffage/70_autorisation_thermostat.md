# 🧠 ARSENAL — CONTRAT NORMATIF PIVOT · CHAUFFAGE — AUTORISATION THERMOSTAT LOGIQUE (V3 PRO)
#
# 📌 STATUT :
#   CONTRAT NORMATIF PIVOT — INTERFACE ENTRE FAITS & DÉCISION
#
# 🔒 AUTORITÉ :
#   Ce document définit la COUCHE D’AUTORISATION THERMIQUE
#   du sous-système Chauffage Arsenal.
#
#   Il formalise le comportement du « thermostat logique »
#   qui produit une INTENTION, jamais une décision.
#
#   Il est OPPOSABLE à toute implémentation :
#     • capteurs template,
#     • helpers d’autorisation,
#     • scripts de calcul d’intention,
#     • toute lecture par la Décision Centrale.
#
#   Subordonné à :
#     /00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif de la **couche d’autorisation thermique**.

Il formalise :

- le rôle du thermostat logique Arsenal,
- la production d’une intention thermique autorisée,
- la sémantique des états `comfort`, `neutre`, `reduced`,
- les règles d’abstention,
- l’indépendance stricte vis-à-vis de la décision centrale,
- l’absence totale de pilotage matériel.

Cette couche constitue la **frontière officielle entre faits thermiques et décision métier**.

---

# ----------------------------------------------------------
# 🧠 2. RÔLE FONDAMENTAL DE L’AUTORISATION
# ----------------------------------------------------------

L’autorisation thermique :

- n’est PAS une décision,
- ne déclenche AUCUNE action,
- ne pilote AUCUN équipement,
- ne connaît PAS la hiérarchie métier,
- ne connaît PAS les blocages,
- ne connaît PAS l’état matériel.

Elle produit uniquement :

> 🧠 **UNE INTENTION AUTORISÉE**

valant proposition pour la Décision Centrale.

Elle répond à une seule question :

> *« Dans le contexte actuel, quel régime est autorisé ? »*

---

### Autorisations forcées amont

Certaines autorisations thermiques peuvent être produites
par des mécanismes amont non liés à l’évaluation thermique locale.

Ces autorisations :

- ne constituent jamais une décision,
- ne constituent jamais une cause hiérarchique,
- ne modifient jamais la hiérarchie métier,
- ne produisent jamais d’action directe.

Sources reconnues :

- forçage utilisateur via `mode_confort_chauffage`,
- inhibition géofencing,
- pré-confort retour vacances.

Règle cardinale :

> ⚠️ Toute autorisation forcée est strictement équivalente
> à une autorisation locale `comfort` et reste intégralement
> soumise à la hiérarchie décisionnelle supérieure.

---

# ----------------------------------------------------------
# 🧱 3. PÉRIMÈTRE COUVERT
# ----------------------------------------------------------

La couche d’autorisation couvre exclusivement :

- l’évaluation locale du confort thermique,
- la lecture des capteurs thermiques métier,
- l’application des seuils d’autorisation,
- la production d’un état d’intention stable.

Hors périmètre strict :

- toute hiérarchie décisionnelle,
- toute notion de blocage,
- toute lecture de présence globale,
- toute gestion absence / vacances,
- toute interaction avec la couche matérielle,
- toute logique d’anti-rebond,
- toute traçabilité.

---

# ----------------------------------------------------------
# 🌡️ 4. ÉTATS D’AUTORISATION OFFICIELS
# ----------------------------------------------------------

La couche produit exactement **trois états exclusifs**.

## 4.1 `comfort`

Définition :

- le besoin thermique est avéré,
- un régime confortable est légitime,
- une action de chauffe est autorisée.

Règles :

- `comfort` autorise une montée en confort,
- ne force JAMAIS une action,
- ne garantit PAS qu’une action sera décidée.

---

## 4.2 `neutre`

Définition :

- le confort est suffisant,
- aucune action n’est nécessaire,
- l’abstention est légitime.

Règles cardinales :

- `neutre` est un état NORMAL,
- `neutre` n’est PAS une erreur,
- `neutre` n’est PAS une attente dégradée,
- `neutre` est un objectif de sobriété.

Effet normatif :

- toute décision ultérieure doit s’abstenir.

---

## 4.3 `reduced`

Définition :

- le confort est inutile ou indésirable,
- une sobriété locale est autorisée,
- une chauffe est déconseillée.

Règles :

- `reduced` n’est PAS un blocage,
- `reduced` n’est PAS une interdiction,
- `reduced` est une préférence locale de sobriété.

---

# ----------------------------------------------------------
# 🧠 5. PRINCIPES CARDINAUX
# ----------------------------------------------------------

Principes absolus :

- l’autorisation n’est JAMAIS une décision,
- l’autorisation n’est JAMAIS prioritaire,
- l’autorisation n’est JAMAIS souveraine,
- l’autorisation ne connaît JAMAIS le matériel,
- l’autorisation ne lit JAMAIS la couche matérielle.

Règle centrale :

> ⚠️ L’autorisation peut être ignorée par la Décision Centrale  
> si un niveau hiérarchique supérieur l’impose.

---

# ----------------------------------------------------------
# 🔁 6. ABSTENTION & SOBRIÉTÉ
# ----------------------------------------------------------

L’abstention est un objectif structurel de cette couche.

Règles :

- `neutre` doit être l’état dominant,
- aucune oscillation `comfort` / `neutre` n’est recherchée,
- la stabilité est prioritaire sur la réactivité,
- l’inertie du bâtiment est respectée.

Objectifs :

- limiter les cycles courts,
- favoriser les plateaux thermiques,
- réduire le pompage énergétique,
- stabiliser la décision centrale.

---

# ----------------------------------------------------------
# 🧩 7. INDÉPENDANCE VIS-À-VIS DE LA DÉCISION
# ----------------------------------------------------------

La couche d’autorisation :

- ne connaît PAS les blocages,
- ne connaît PAS l’aération,
- ne connaît PAS les fenêtres,
- ne connaît PAS le poêle,
- ne connaît PAS les vacances,
- ne connaît PAS l’inhibition géofencing.

Elle ignore volontairement :

- la hiérarchie métier,
- la présence globale,
- les contextes système.

Elle décrit uniquement :

> 🧠 **LA SITUATION THERMIQUE LOCALE**

---

### Neutralité vis-à-vis des autorisations automatiques

La couche d’autorisation locale est strictement indépendante :

- des mécanismes d’anticipation,
- du pré-confort retour vacances,
- de toute autorisation temporelle prédictive.

Règles cardinales :

- l’autorisation locale ne connaît jamais l’existence du pré-confort,
- elle ne s’adapte jamais à une anticipation,
- elle ne modifie jamais ses seuils ou son état
  en fonction d’un contexte temporel.

Le pré-confort retour vacances agit exclusivement
en écriture amont sur l’état d’autorisation final,
sans jamais influencer le calcul thermique local.

---

# ----------------------------------------------------------
# 🔒 8. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

La couche d’autorisation ne doit JAMAIS :

- appeler un service,
- modifier un helper décisionnel,
- piloter un script,
- déclencher une automatisation,
- écrire un état matériel,
- produire une trace décisionnelle,
- intégrer une règle métier.

Toute tentative de pilotage constitue :

- une rupture de séparation des responsabilités,
- une erreur majeure d’architecture.

---

# ----------------------------------------------------------
# 🧱 9. INVARIANTS D’AUTORISATION
# ----------------------------------------------------------

Invariants absolus :

- un seul état actif à la fois,
- aucun état implicite,
- aucune valeur hors `{ comfort | neutre | reduced }`,
- aucune dépendance hiérarchique,
- aucune dépendance matérielle,
- aucune mémoire inter-cycle.

---

### Invariants des autorisations forcées

Invariants absolus :

- aucune autorisation forcée ne peut persister hors de son contexte,
- aucune autorisation forcée ne peut survivre à un changement de régime,
- aucune autorisation forcée ne peut être restaurée automatiquement,
- aucune autorisation forcée ne peut écraser une intention utilisateur explicite.

Règles cardinales :

- toute autorisation forcée est strictement transitoire,
- toute sortie de contexte impose un retour immédiat
  à l’autorisation locale naturelle,
- toute priorité utilisateur écrase toute autorisation automatique.

Le pré-confort retour vacances est intégralement soumis à ces invariants.

---

Toute violation constitue :

- une dérive thermostat classique,
- une perte de sobriété,
- une rupture de gouvernance.

---

# ----------------------------------------------------------
# 🧠 10. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- utilisé directement par :
  - `30_decision_centrale.md`

- complémentaire de :
  - `60_absence_inhibition_geofencing.md`
  - `80_table_decision_canonique.md`

Il gouverne directement :

- le capteur `sensor.chauffage_autorisation_cible`,
- toute logique de calcul d’intention thermique.

---

# ----------------------------------------------------------
# 📌 11. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- un pivot fondamental de l’architecture Chauffage,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue le **thermostat logique officiel du Chauffage Arsenal V3 PRO**.

# ==========================================================