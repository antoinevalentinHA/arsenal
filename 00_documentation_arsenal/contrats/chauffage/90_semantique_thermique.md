# 🧠 ARSENAL — CONTRAT NORMATIF FONDATEUR · CHAUFFAGE — SÉMANTIQUE THERMIQUE OFFICIELLE (V3 PRO)
#
# 📌 STATUT :
#   CONTRAT NORMATIF FONDATEUR — RÉFÉRENCE SÉMANTIQUE GLOBALE
#
# 🔒 AUTORITÉ :
#   Ce document définit la **sémantique officielle et opposable**
#   de tous les termes thermiques utilisés dans le sous-système
#   Chauffage Arsenal.
#
#   Il constitue la RÉFÉRENCE UNIQUE pour :
#     • les contrats métier,
#     • les scripts,
#     • les automatismes,
#     • les capteurs,
#     • l’UI,
#     • les logs,
#     • les notifications,
#     • les diagnostics.
#
#   Toute utilisation divergente d’un terme défini ici constitue :
#     - une dérive sémantique,
#     - une perte de lisibilité système,
#     - une rupture de gouvernance.
#
#   Subordonné à :
#     [/homeassistant/00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md](00_gouvernance_chauffage.md)
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit la **sémantique thermique officielle** du Chauffage Arsenal.

Il formalise :

- le sens exact des états,
- le vocabulaire métier canonique,
- les différences entre notions proches,
- les usages autorisés et interdits,
- les confusions à proscrire.

Ce contrat garantit :

> 🧠 **UNE INTERPRÉTATION UNIQUE, STABLE ET PARTAGÉE  
> DE TOUT LE LANGAGE THERMIQUE DU SYSTÈME**

---

# ----------------------------------------------------------
# 🧠 2. PRINCIPES SÉMANTIQUES CARDINAUX
# ----------------------------------------------------------

Principes absolus :

- chaque terme possède **un sens unique**,
- aucun terme ne doit être polysémique,
- aucun terme ne doit être utilisé hors périmètre,
- aucune logique ne doit reposer sur une ambiguïté lexicale.

Règle cardinale :

> ⚠️ Toute dérive de vocabulaire produit inévitablement  
> une dérive de comportement.

---

# ----------------------------------------------------------
# 🔥 3. RÉGIMES THERMIQUES CANONIQUES
# ----------------------------------------------------------

## 3.1 `comfort`

Définition :

> Régime thermique de **recherche active de confort**.

Caractéristiques :

- autorise la chauffe,
- vise une élévation de température,
- correspond à un besoin thermique avéré,
- déclenche potentiellement des appels matériels.

N’est PAS :

- un état de présence,
- un forçage utilisateur,
- un confort permanent,
- une décision implicite.

---

## 3.2 `reduced`

Définition :

> Régime thermique de **sobriété active**.

Caractéristiques :

- autorise une température basse contrôlée,
- interdit toute recherche de confort,
- correspond à un régime nominal d’économie,
- peut maintenir un plancher thermique.

N’est PAS :

- un blocage,
- une interdiction système,
- un hors-gel,
- une absence de régulation.

---

## 3.3 `neutre`

Définition :

> État d’**abstention thermique volontaire**.

Caractéristiques :

- aucun besoin thermique détecté,
- aucune action souhaitable,
- confort jugé suffisant,
- stabilité prioritaire.

Règles :

- `neutre` est un état NORMAL,
- `neutre` est un objectif de sobriété,
- `neutre` produit toujours une abstention.

N’est PAS :

- une erreur,
- une attente dégradée,
- un reduced déguisé,
- une panne.

---

# ----------------------------------------------------------
# 🧱 4. ÉTATS FONCTIONNELS MAJEURS
# ----------------------------------------------------------

## 4.1 Décision

Définition :

> Acte souverain par lequel le moteur choisit un régime thermique.

Propriétés :

- unique,
- explicite,
- traçable,
- hiérarchique.

---

## 4.2 Autorisation

Définition :

> Intention thermique autorisée issue de la couche thermostat logique.

Propriétés :

- jamais une décision,
- jamais hiérarchique,
- jamais exécutoire,
- purement descriptive.

---

## 4.3 Application

Définition :

> Traduction mécanique d’une décision vers un état exécutable.

Propriétés :

- idempotente,
- sans interprétation,
- stabilisée par hystérésis,
- subordonnée strictement.

---

## 4.4 Exécution

Définition :

> Action matérielle effective sur la chaudière ou l’adaptateur.

Propriétés :

- passive,
- non décisionnelle,
- non interprétative,
- contrôlée.

---

# ----------------------------------------------------------
# 🛑 5. BLOCAGE
# ----------------------------------------------------------

Définition :

> Interdiction hiérarchique absolue de toute recherche de confort.

Caractéristiques :

- écrase toute autorisation,
- écrase toute opportunité,
- produit un `reduced` forcé,
- interdit toute reprise automatique.

Exemples :

- fenêtre ouverte  
- aération  
- poêle  
- vacances  
- interdiction système  

N’est PAS :

- un reduced  
- un standby  
- une absence  
- une hystérésis  

---

# ----------------------------------------------------------
# ⏳ 6. STANDBY / ATTENTE
# ----------------------------------------------------------

## 6.1 Standby

Définition :

> Verrou logique d’application servant à stabiliser l’exécution.

Caractéristiques :

- purement mécanique,
- post-décision,
- pré-matériel,
- sans logique métier.

N’est PAS :

- un blocage,
- un régime,
- une décision,
- une attente thermique métier.

---

## 6.2 Attente thermique

Définition :

> État fonctionnel de surveillance passive d’un seuil thermique.

Caractéristiques :

- aucun chauffage actif,
- seuil surveillé,
- déclenchement conditionnel futur,
- lié à un besoin anticipé.

N’est PAS :

- un standby,
- une abstention,
- un reduced,
- un confort latent.

---

# ----------------------------------------------------------
# 🔁 7. ABSTENTION
# ----------------------------------------------------------

Définition :

> Choix explicite de **ne produire aucune action**.

Caractéristiques :

- décision valide à part entière,
- état stable recherché,
- signe de confort suffisant,
- pilier de la sobriété.

Règles :

- `neutre` produit toujours une abstention,
- toute abstention est traçable,
- aucune abstention implicite n’est autorisée.

---

# ----------------------------------------------------------
# 🌬️ 8. ABSENCE / PRÉSENCE
# ----------------------------------------------------------

## 8.1 Présence

Définition :

> Régime contextuel autorisant une recherche normale de confort.

Caractéristiques :

- autorise l’usage du thermostat logique,
- ne force jamais le confort,
- reste soumis aux blocages.

---

## 8.2 Absence

Définition :

> Régime contextuel de sobriété par défaut.

Caractéristiques :

- confort interdit par défaut,
- reduced nominal,
- autorise l’inhibition géofencing sous conditions strictes.

---

# ----------------------------------------------------------
# 🧠 9. INHIBITION GÉOFENCING
# ----------------------------------------------------------

Définition :

> Mécanisme de confort différé simulant une présence en absence.

Caractéristiques :

- strictement temporaire,
- déclenché par seuil froid,
- orienté reprise douce,
- jamais permanent.

N’est PAS :

- un préchauffage classique,
- un confort absence,
- une protection bâti,
- un retour de présence.

---

# ----------------------------------------------------------
# 🔒 10. REPRISE
# ----------------------------------------------------------

Définition :

> Transition thermique post-absence ou post-blocage vers un régime confortable.

Caractéristiques :

- toujours arbitrée,
- jamais automatique,
- protégée par hystérésis,
- surveillée par seuils.

N’est PAS :

- un simple OFF → ON,
- une levée de blocage directe,
- une action par principe.

---

# ----------------------------------------------------------
# 🧾 11. RAISON DOMINANTE
# ----------------------------------------------------------

Définition :

> Cause hiérarchique principale expliquant la décision finale.

Caractéristiques :

- unique,
- stable durant la décision,
- affichable en UI,
- utilisée en diagnostic.

Règle :

> 🧠 Toute décision doit posséder UNE raison dominante canonique.

---

# ----------------------------------------------------------
# 🧱 12. INTERDICTIONS SÉMANTIQUES MAJEURES
# ----------------------------------------------------------

Il est STRICTEMENT INTERDIT :

- d’utiliser “blocage” pour “reduced”,
- d’utiliser “standby” pour “attente”,
- d’utiliser “absence” pour “reduced”,
- d’utiliser “neutre” pour “erreur”,
- d’utiliser “comfort” pour “présence”.

Toute confusion constitue :

- une dérive de conception,
- une perte de lisibilité,
- une dette cognitive majeure.

---

# ----------------------------------------------------------
# 🧠 13. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)

- transversal à :
  - [`10_souverainete_execution.md`](10_souverainete_execution.md)
  - [`20_triggers_decisionnels.md`](20_triggers_decisionnels.md)
  - [`30_decision_centrale.md`](30_decision_centrale.md)
  - [`40_blocages.md`](40_blocages.md)
  - [`50_standby_hysteresis.md`](50_standby_hysteresis.md)
  - [`60_absence_inhibition_geofencing.md`](60_absence_inhibition_geofencing.md)
  - [`70_autorisation_thermostat.md`](70_autorisation_thermostat.md)
  - [`80_table_decision_canonique.md`](80_table_decision_canonique.md)

Il gouverne directement :

- toute dénomination d’état,
- toute UI thermique,
- toute trace log,
- toute notification,
- toute documentation métier.

---

# ----------------------------------------------------------
# 📌 14. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- fondateur dans l’architecture Arsenal,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **référence sémantique officielle  
du Chauffage Arsenal V3 PRO**.

# ==========================================================