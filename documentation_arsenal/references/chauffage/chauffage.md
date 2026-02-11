# ==========================================================
# ⚠️ DOCUMENT HISTORIQUE — ARCHIVÉ
#     Chauffage — Contrat Monolithique Hérité
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT ARCHIVÉ — NON NORMATIF — RÉFÉRENCE HISTORIQUE
#
# 🔒 AUTORITÉ :
#   Ce document n’est PLUS une référence normative active.
#
#   Il est remplacé par la série de contrats modulaires :
#
#     00_gouvernance_chauffage.md
#     10_souverainete_execution.md
#     20_triggers_decisionnels.md
#     30_decision_centrale.md
#     40_blocages.md
#     50_standby_hysteresis.md
#     60_absence_inhibition_geofencing.md
#     70_autorisation_thermostat.md
#     80_table_decision_canonique.md
#     90_semantique_thermique.md
#
# 🧠 RÔLE ACTUEL :
#   - Archive de conception
#   - Historique d’évolution
#   - Source de contexte ancien
#
# ❌ INTERDIT :
#   - Toute référence normative
#   - Toute utilisation comme autorité
#   - Toute citation en implémentation
#
# ==========================================================

# ==========================================================
# 🕰️ ARSENAL — DOCUMENT HISTORIQUE
#     Chauffage — Contrat Monolithique d’Origine
# ==========================================================

## 🎯 OBJET HISTORIQUE DU DOCUMENT

Ce document constitue le **contrat monolithique fondateur**
ayant servi de base à la conception initiale du sous-système Chauffage Arsenal.

Il décrit :
- les responsabilités initialement envisagées,
- les premières hiérarchies décisionnelles,
- les règles fondatrices de comportement,
- les garanties systémiques recherchées à l’origine.

Depuis la version Chauffage V3 PRO :

- ce document n’a PLUS de valeur normative,
- il est remplacé par des contrats spécialisés modulaires,
- toute autorité est transférée aux fichiers du dossier `contrats/chauffage/`.

Ce document est conservé uniquement à des fins :

- historiques,
- pédagogiques,
- de traçabilité d’architecture.

❌ Il ne fait plus foi.  
❌ Il ne constitue plus une référence valide.  
❌ Il ne doit plus être utilisé pour guider une implémentation.

---

# ----------------------------------------------------------
# 🧭 RÉFÉRENCES ACTUELLES — ARCHITECTURE MODULAIRE
# ----------------------------------------------------------

Le moteur Chauffage Arsenal est désormais gouverné par les contrats actifs suivants :

| Domaine | Contrat de référence |
|--------|----------------------|
| Gouvernance globale | 00_gouvernance_chauffage.md |
| Souveraineté d’exécution | 10_souverainete_execution.md |
| Triggers décisionnels | 20_triggers_decisionnels.md |
| Décision centrale | 30_decision_centrale.md |
| Blocages hiérarchiques | 40_blocages.md |
| Standby & hystérésis | 50_standby_hysteresis.md |
| Absence & inhibition géofencing | 60_absence_inhibition_geofencing.md |
| Autorisation thermostat | 70_autorisation_thermostat.md |
| Table décision canonique | 80_table_decision_canonique.md |
| Sémantique thermique | 90_semantique_thermique.md |

Toute règle métier, toute implémentation et toute évolution
doivent désormais se référer exclusivement à ces contrats.

---

## 🧱 PÉRIMÈTRE

Le contrat couvre :
- l’intention thermique (Comfort / Eco / Neutre),
- la **coordination avec les contextes bloquants**,
- la **non-régression comportementale**.

Il ne couvre PAS :
- le pilotage matériel direct,
- les consignes ViCare,
- la régulation fine de température,
- la performance énergétique.

---

## 🧠 ARCHITECTURE DE RÉFÉRENCE

Le chauffage Arsenal repose sur une séparation stricte :

1. **Capteurs & helpers**
   - Fournissent des faits et des intentions
   - Ne prennent aucune décision
   
2. **Script de décision centrale**
   - Autorité UNIQUE de décision thermique
   - Produit une intention :
     • Comfort
     • Eco
     • ou une abstention volontaire (Neutre)

3. **Capteurs décisionnels**
   - Exposent l’intention et la raison
   - Sans accès au réel

4. **Automatismes d’application**
   - Appliquent la décision
   - Sous contraintes matérielles et API

Aucun autre composant n’est autorisé à décider.

---

## 🔒 SOUVERAINETÉ MATÉRIELLE & REPRISE POST-RESYNCHRONISATION ViCare

Cette section formalise les **invariants architecturaux de souveraineté**
garantissant que le chauffage réel reste strictement subordonné
aux décisions Arsenal, malgré les comportements autonomes de l’API ViCare.

Elle couvre deux dimensions distinctes et complémentaires :

- la **souveraineté de la source de vérité exécutoire** (état),
- la **sérialisation stricte des voies d’exécution** (temps).

---

## 🧠 Principe général — Décision vs exécution

Le système Chauffage Arsenal repose sur une séparation stricte entre :

- **l’autorité de décision** (unique),
- et les **voies d’exécution** (potentiellement multiples).

> **Une seule entité est autorisée à décider du mode chauffage :**  
> le script *Chauffage – Décision Centrale*.

Toute autre brique est formellement interdite de :

- produire une décision thermique,
- transformer une intention en une autre,
- initier une transition de mode de sa propre initiative.

---

## 🧠 Problématique ViCare — Réinjection passive d’état

En cas de :

- micro-indisponibilités de l’API ViCare,
- redémarrage Home Assistant,
- resynchronisation cloud,
- ouverture de l’application mobile ViCare,

le programme réel peut être **réinjecté passivement** par le cloud  
(`comfort` ou `reduced`) **sans qu’aucune décision Arsenal n’ait été prise**.

Ce comportement est considéré comme une **anomalie architecturale majeure** :

> Un état matériel ne peut jamais devenir dominant  
> s’il n’est pas issu d’une décision Arsenal.

---

## 🧱 Mémoire souveraine d’exécution — Source de vérité exécutoire

Un objet structurant est introduit :

- `input_select.chauffage_dernier_mode_decide`

Rôle exact :

- mémoriser la **dernière décision légitime effectivement appliquée au matériel**,
- valeurs autorisées :
  - `comfort`
  - `reduced`

Règles strictes :

- écrit **exclusivement** par :
  - `script.chauffage_consigne_confort`
  - `script.chauffage_consigne_reduite`
- écrit **uniquement après confirmation réelle cloud**,
- jamais modifié par une automation,
- jamais déduit d’un état ViCare.

Cette entité constitue la **référence souveraine post-exécution**.

---

## 🔒 Invariant de souveraineté matérielle (état)

L’invariant suivant est désormais **opposable** :

> **À tout instant, le programme réel doit être égal  
> à `input_select.chauffage_dernier_mode_decide`.**

Conséquences normatives :

- si programme réel = dernier_mode_decide  
  → état conforme → aucune action

- si programme réel ≠ dernier_mode_decide  
  → état divergent → correction obligatoire

Ce principe s’applique :

- quel que soit :
  - le mode décisionnel courant (comfort / neutre / reduced),
  - le régime (présence / absence),
  - l’état de ViCare.

En particulier :

- le mode `neutre` **ne délègue jamais** la décision au cloud,
- toute transition passive ViCare est considérée comme **illégitime**.

---

## 🧠 Rôle des composants dans la souveraineté d’état

### 🔹 Décision Centrale

- produit :
  - `sensor.chauffage_autorisation_cible`
    (`comfort` / `neutre` / `reduced`)
- ne connaît **pas** l’état réel ViCare,
- reste l’unique autorité de décision métier.

---

### 🔹 Scripts exécutifs ViCare

Responsabilités normatives :

- appliquer la consigne réelle,
- attendre confirmation cloud,
- puis :
  - écrire `input_select.chauffage_dernier_mode_decide`,
  - écrire la `raison` uniquement si fournie.

Ils sont les **seuls points de mise à jour** de la mémoire souveraine.

---

### 🔹 Automation de garde défensive

Rôle strict :

- ne prend **aucune décision métier**,
- ne lit jamais `autorisation_cible`,
- compare uniquement :
  - `sensor.programme_chauffage`
  - vs `input_select.chauffage_dernier_mode_decide`.

Elle agit exclusivement comme :

> **Mécanisme de correction structurelle**,  
> jamais comme mécanisme décisionnel.

---

## ⏱️ ORDONNANCEMENT & SÉRIALISATION DES VOIES D’EXÉCUTION

Cette section formalise les invariants de **gouvernance temporelle**
garantissant l’absence totale de concurrence entre :

- application active d’une décision,
- et correction post-resynchronisation.

---

## 🧠 Problématique de concurrence interne

Deux voies d’exécution coexistent :

- les **scripts exécutifs ViCare** (application active),
- l’**automation de garde défensive** (correction).

Sans mécanisme de sérialisation :

- une correction peut être déclenchée  
  **pendant même qu’une décision est en cours d’application**,

provoquant :

- annulation de la décision en cours,
- oscillations,
- perte de souveraineté effective,
- ou blocage transactionnel.

Ce scénario constitue une **anomalie critique d’ordonnancement interne**.

---

## 🧱 Verrou de sérialisation d’exécution

Un verrou logique est introduit :

- `input_boolean.chauffage_application_en_cours`

Rôle exact :

- matérialiser qu’une **transaction d’application est active**,
- interdire toute action concurrente de correction.

Règles strictes :

- positionné à `on` **au début** de chaque script exécutif,
- remis à `off` **uniquement après confirmation réelle cloud**  
  et fin complète de l’exécution,
- lu obligatoirement par toute automation de garde avant toute action.

---

## 🔒 Invariant de non-concurrence (temps)

L’invariant suivant est désormais **opposable** :

> **Si `chauffage_application_en_cours == on` :**  
> – aucune correction ne peut être tentée,  
> – aucune divergence ne peut être traitée,  
> – aucune réapplication ne peut être déclenchée.

Conséquences normatives :

- toute automation de garde :
  - doit vérifier ce verrou,
  - doit s’abstenir de toute action si une application est en cours.

- aucun mécanisme n’est autorisé à :
  - corriger un état matériel pendant une transaction active,
  - interrompre une application en cours,
  - provoquer une double écriture concurrente.

---

## 🧠 Nature du verrou de sérialisation

Ce verrou :

- ❌ ne constitue PAS une décision métier  
- ❌ ne constitue PAS une logique thermique  
- ❌ ne constitue PAS un mécanisme de blocage  

Il est un **mécanisme d’ordonnancement**, garantissant :

- atomicité des exécutions,
- absence de boucle,
- absence de yo-yo,
- absence de concurrence entre :
  - voies d’exécution,
  - et voie de garde de cohérence.

Toute violation de cet invariant constitue une :

> **rupture de sérialisation**,  
> une **perte de déterminisme**,  
> et une **régression architecturale majeure**.

---

## 📌 Principe cardinal de souveraineté exécutive

> **La Décision Centrale est souveraine sur l’intention.**  
> **`chauffage_dernier_mode_decide` est souverain sur l’exécution.**  
> **Toute exécution est atomique et non interruptible.**  
> **ViCare n’est jamais souverain.**

Ce principe est désormais constitutif  
du contrat Chauffage Arsenal V3 PRO.

---

## 🧱 AUTORITÉ DÉCISIONNELLE

### 🔒 Principe fondamental

> **Une seule autorité décide du mode chauffage :**
> le script **Chauffage – Décision Centrale**.

Aucune automation, capteur ou helper ne peut :
- forcer un mode,
- court-circuiter la hiérarchie,
- redémarrer le chauffage par principe.

---

## 🧠 HIÉRARCHIE DÉCISIONNELLE (ORDRE STRICT)

### 🛑 NIVEAU 1 — INTERDICTIONS ABSOLUES

Ces états écrasent TOUTE autre logique :

- Chauffage non autorisé système
- Standby forcé
- Sécurité / cohérence globale

➡️ Résultat imposé : **Eco**

---

### 🧠 NIVEAU 2 — CONTEXTES BLOQUANTS MAJEURS

Ces contextes imposent **TOUJOURS** le mode Eco :

- Aération en cours
- Blocage post-aération
- Fenêtre ouverte (qualifiée, avec délai)
- Poêle actif (instantané ou mémoire)
- Mode maison = Vacances

➡️ Résultat imposé : **Eco**

Aucune exception.
Aucune négociation.
Aucune temporisation.

---

### 🌡️ NIVEAU 3 — CONFORT D’OPPORTUNITÉ

Ces contextes ne constituent **PAS une décision thermique directe**.

Ils ont pour SEUL rôle :
- d’**autoriser** un passage ultérieur en Comfort
- de **lever l’interdiction** liée à l’absence
- de permettre à la **physique du bâtiment**
  d’exprimer un besoin réel

Ils ne s’appliquent QUE SI :
- aucun niveau 1 ou 2 n’est actif

Contextes concernés :
- Forçage confort explicite
- Pré-confort (retour anticipé)
- Présence réelle du foyer

En l’absence de besoin thermique confirmé,
le système peut décider explicitement de ne pas agir.

➡️ Résultat possible : **Neutre**
(autorisation thermique sans action)

⚠⚠️ RÈGLE CARDINALE

> La présence n’est **JAMAIS** une décision thermique.

Elle :
- n’impose aucun passage immédiat en Comfort
- n’initie aucune chauffe par principe
- n’a aucune autorité sans confirmation thermique

La présence constitue **une autorisation conditionnelle**,
strictement subordonnée à l’apparition d’un
**besoin thermique réel**.

---

### 🔁 NIVEAU 4 — ABSENCE AVEC PROTECTION THERMIQUE HYSTÉRÉSÉE

En l’absence de tout contexte prioritaire (N1 à N3),
le système entre en **régime d’absence** par défaut.

Ce régime vise une **sobriété thermique maximale**
et n’implique **aucune recherche de confort occupant**.

Cependant, l’absence peut être **temporairement protégée**
afin d’éviter une dérive thermique excessive du bâtiment.

---

### 🌡️ Protection thermique (absence)

Lorsque le foyer est en absence confirmée,
le système surveille la température de la
**pièce de référence la plus froide**.

Si cette température franchit un seuil critique défini par :

> **consigne confort − offset ON (protection absence)**

alors :

- la logique de géolocalisation est **inhibée**,
- une **chauffe ponctuelle de protection** est autorisée,
- l’objectif est d'éviter une chute trop importante de la température.

⚠️ Cette activation :
- ne constitue **PAS** une décision thermique,
- ne modifie **PAS** le régime d’absence,
- n’implique **AUCUN retour durable en mode Confort**.

NB : 🔥 La protection thermique en absence peut nécessiter un passage temporaire 
du programme réel en Confort, sans que cela ne constitue une décision Confort.

---

### 🔁 Hystérésis obligatoire (stabilité)

La protection thermique d’absence est **hystérésée**.

Elle est pilotée par un **état logique stabilisé**
(`input_boolean.chauffage_inhibition_geofencing`),
et NON par un seuil instantané.

Une fois activée :
- elle reste active tant que la température
  n’a pas franchi un **seuil OFF distinct**,
- elle ne peut pas osciller au voisinage d’un seuil unique,
- elle garantit l’absence totale d’effet **yo-yo thermique**.

La désactivation peut également survenir si :
- la présence est rétablie,
- un contexte bloquant prioritaire apparaît (N1 à N3),
- le mode maison change.

---

### 📌 RÈGLES CARDINALES

Cette protection :

- n’est **JAMAIS** une reprise automatique du chauffage,
- n’est **JAMAIS** un confort par principe,
- ne produit **AUCUNE intention thermique** distincte
et ne modifie jamais la décision Eco,
- constitue un **mécanisme de sûreté d’exécution**, jamais une décision métier.

Elle reste strictement subordonnée :
- aux niveaux 1 à 3,
- à la décision centrale Chauffage,
- au contrat Chauffage Arsenal.

---

## 🔒 MÉCANISME DE VERROU — `chauffage_standby_force`

Le verrou logique `input_boolean.chauffage_standby_force`
constitue un **mécanisme d’application**, et NON une logique
métier autonome.

### 🧠 Rôle exact

- Il est :
  • piloté exclusivement par les automatismes d’application
  • relu par la décision centrale comme FAIT ÉTABLI

- Il permet :
  • d’appliquer mécaniquement une décision thermique
  • de stabiliser le système face aux délais matériels / API
  • d’éviter toute oscillation ou écriture inutile

### ⚠️ Principe fondamental

> Le verrou n’a AUCUNE intelligence métier propre.

Toute logique, seuil ou stratégie :
- DOIT être décidée en amont
- NE DOIT JAMAIS être implémentée dans l’automation d’application

Le verrou est un **effet**, jamais une cause.

### 🌡️ Nature thermique du verrou

- `chauffage_standby_force` représente un **état d’attente thermique contrôlée**
- Il matérialise un **mécanisme d’hystérésis thermique** décidé en amont par la décision centrale
- Il signifie :
  • chauffage momentanément suspendu  
  • surveillance thermique **active** (intérieure et extérieure)  
  • reprise **automatique attendue** dès que le seuil bas est atteint

Ce verrou :
- ❌ n’est PAS un blocage thermique
- ❌ n’est PAS une interdiction absolue
- ❌ ne suspend PAS la logique de décision ni de surveillance

Il constitue l’**expression mécanique** d’une abstention thermique temporaire,
et non un mécanisme de sécurité ou de protection.

---

### ⚖️ Priorité sémantique — Blocage vs Standby

Un **blocage thermique métier** (fenêtre ouverte, aération ou post-aération,
poêle actif, mode Vacances, interdiction système) est **toujours prioritaire**
sur tout mécanisme de standby ou d’hystérésis.

Conséquences normatives :

- Si un **blocage thermique est actif** :
  - le chauffage est considéré comme **bloqué**
  - aucune notion d’« attente thermique » ne doit être exposée
  - aucune reprise automatique n’est surveillée ou annoncée

- Le mécanisme `chauffage_standby_force` :
  - peut être **actif mécaniquement** en parallèle
  - mais ne constitue **jamais** la cause dominante
  - et ne doit **jamais** être rendu visible tant qu’un blocage persiste

➡️ **Règle cardinale :**

> Un effet mécanique (standby / hystérésis)
> ne peut jamais masquer une cause métier bloquante.

Toute UI, diagnostic ou narration qui expose une
**attente thermique en présence d’un blocage actif**
est considérée comme **non conforme au contrat Chauffage Arsenal**.

---

## 🔁 HYSTÉRÉSIS & STABILITÉ

### 🔒 Principe fondamental

Le retour de présence ne constitue
**PAS un déclencheur thermique**,
mais une **levée d’interdiction conditionnelle**.

Le système de chauffage Arsenal applique
une hystérésis décisionnelle stricte :

- Fin de blocage ≠ reprise automatique
- Aucun redémarrage “par principe”
- Passage en Comfort uniquement si
  le BESOIN THERMIQUE est confirmé

Objectifs :
- Zéro effet yo-yo
- Respect de l’inertie thermique
- Protection du matériel et de l’API

---

## 🧠 CAPTEURS CANONIQUES

### 🔹 Chauffage mode calculé

- Expose l’INTENTION thermique pure
- Miroir exact de la décision centrale
- Vocabulaire canonique :
  - `Confort`
  - `Eco`
  - `Neutre` (abstention volontaire de décision)

Il ne reflète PAS l’état réel.

---

### 🔹 Chauffage raison calculée

- Expose la CAUSE DOMINANTE de la décision
- Strictement alignée sur la hiérarchie
- Une seule raison à la fois
- Stable, explicite, traçable
- Peut exposer une raison d’attente sans déclencher d’action

---

## 🧾 STATUTS THERMIQUES — DÉFINITION SÉMANTIQUE

Cette section définit les **statuts thermiques lisibles**
utilisés à des fins de diagnostic, d’UI et de compréhension humaine.

Ces statuts :
- ne constituent PAS des décisions
- ne déclenchent AUCUNE action
- n’ont AUCUNE autorité métier
- traduisent uniquement l’état résultant
  de la décision + du contexte + de la physique

Ils sont **strictement descriptifs** et soumis au présent contrat.

---

### ⏳ Attente thermique — Confort

L’attente thermique (confort) correspond au cas où :

- le chauffage est **autorisé**
- aucun contexte bloquant n’est actif
- la présence ou un contexte de confort d’opportunité est établi
- le système a **décidé de ne pas chauffer pour l’instant**
  par absence de besoin thermique réel

Caractéristiques :

- le mode décisionnel peut rester `Eco`
- ou être explicitement fixé à `Neutre`
- cette absence de chauffe est **volontaire et intelligente**
- le système surveille le **seuil bas de confort**
  de la pièce de référence la plus froide
- ce seuil n’est pas encore franchi

Dans ce cas :
- le chauffage ne chauffe pas
- le confort est jugé **suffisant**
- une chauffe sera déclenchée
  **au premier signe de dérive thermique**

---

### 🟦 Attente thermique — Protection (absence)

L’**attente thermique (protection)** correspond à un cas distinct,
actif **en situation d’absence**, lorsque le système est configuré
pour éviter un refroidissement excessif du bâtiment.

Conditions caractéristiques :
- le mode de chauffage décidé est `Eco`
- l’absence est confirmée
- le mécanisme de protection thermique d’absence est activé
- aucun contexte bloquant n’est actif
- le système surveille un **seuil de protection thermique**
  défini par : consigne_confort - écart_acceptable
- ce seuil n’est pas encore atteint

Dans ce cas :
- le chauffage ne chauffe pas en continu
- mais une **chauffe ponctuelle est autorisée**
si le seuil de protection est franchi
- il n’y a **pas de retour durable au confort**
tant que l’absence persiste

Cette attente :
- repose sur une **surveillance thermique réelle**
- ne constitue PAS une attente de confort
- reste strictement subordonnée aux contextes bloquants

---

### ⛔ Blocage thermique

Un **blocage thermique** correspond à une
**interdiction volontaire de chauffer**, imposée par le contexte.

Exemples de contextes bloquants :
- fenêtre ouverte
- aération en cours ou post-aération
- poêle actif
- standby forcé
- mode maison = Vacances
- chauffage non autorisé système

Dans un état de blocage :
- le chauffage **n’attend RIEN**
- aucune reprise n’est surveillée
- aucun seuil n’est pertinent
- aucune chauffe n’est attendue

Un blocage thermique ne peut **JAMAIS**
être qualifié d’attente thermique.

---

### 📌 RÈGLE SÉMANTIQUE CARDINALE

Le terme **« attente thermique »** est réservé
aux **DEUX cas définis ci-dessus** :

- ⏳ Attente thermique — Confort
- 🟦 Attente thermique — Protection (absence)

Toute autre utilisation du mot :
- pour un blocage
- pour une interdiction
- pour une suspension logique
- pour une abstention décisionnelle non qualifiée

constitue une **erreur sémantique**,
sans impact fonctionnel,
mais contraire au présent contrat.

---

## 🛑 INTERDICTIONS FORMELLES

Il est STRICTEMENT interdit de :

- décider du mode chauffage hors du cerveau central
- forcer Comfort via une automation locale
- faire dépendre le chauffage directement de la présence
- contourner les contextes bloquants
- créer un redémarrage automatique implicite

Toute violation est une régression.

---
--------------------------------------------------
🧠 CHAUFFAGE — TABLE DE DÉCISION CANONIQUE (V7.3.1)
--------------------------------------------------

Cette table définit EXHAUSTIVEMENT le comportement attendu
de la Décision Centrale Chauffage.

Elle distingue strictement :
- le régime ABSENCE (protection thermique / geofencing)
- le régime PRÉSENCE (hystérésis / thermostat logique)

Toute implémentation divergente constitue une régression métier.

---

## 0) PRIORITÉ ZÉRO — FORÇAGE CONFORT (override utilisateur)

Le forçage confort est un choix utilisateur explicite :
il écrase toutes les logiques de confort/opportunité et les blocages usuels.
Exception : l’interdiction système (chauffage_autorise_systeme = OFF) reste prioritaire.

| Condition active | Décision | Régime | Raison |
|------------------|----------|--------|--------|
| chauffage_autorise_systeme = OFF | Eco | Indifférent | chauffage_non_autorise |
| mode_confort_chauffage = ON | Confort | Indifférent | confort_force |

---

## 1) NIVEAU 1 — INTERDICTIONS ABSOLUES (blocages majeurs)

Ces conditions imposent Eco, sans discussion.

| Condition active | Décision | Régime | Raison |
|------------------|----------|--------|--------|
| chauffage_standby_force = ON | Eco | Indifférent | standby_force |
| aeration_episode_en_cours = ON | Eco | Indifférent | aeration_en_cours |
| chauffage_blocage_aeration = ON | Eco | Indifférent | blocage_aeration_en_cours |
| fenetre_ouverte_maison_avec_delai = ON | Eco | Indifférent | fenetre_ouverte_maison |
| mode_maison = Vacances | Eco | Indifférent | mode_maison_vacances |
| blocage_chauffage_poele = ON | Eco | Indifférent | poele_actif |

---

## 2) SÉLECTION DU RÉGIME (structurant)

| Présence foyer | Régime actif |
|---------------|--------------|
| presence_famille_unifiee = OFF | ABSENCE |
| presence_famille_unifiee = ON  | PRÉSENCE |

---

## 3A) RÉGIME ABSENCE — PROTECTION THERMIQUE

Objectif :
Éviter une chute thermique excessive sans retour durable au confort.

Règles :
- La décision reste **Eco** en permanence.
- La décision centrale reste souveraine ;
la protection agit uniquement via des mécanismes d’application autorisés par celle-ci.
- Neutre est **strictement interdit** en absence.

| État inhibition | Décision | Raison | Commentaire |
|-----------------|----------|--------|-------------|
| chauffage_inhibition_geofencing = ON | Eco | absence_protection_bati | Protection thermique active |
| chauffage_inhibition_geofencing = OFF | Eco | absence | Absence normale |

---

## 3B) RÉGIME PRÉSENCE — HYSTÉRÉSIS / THERMOSTAT LOGIQUE

Objectif :
Assurer le confort réel sans oscillation, via une zone morte explicite.

Capteur maître :
- sensor.chauffage_autorisation_cible (comfort / neutre / reduced)

Règles :
- La présence autorise la décision, mais ne décide jamais.
- Neutre est valide uniquement en présence.
- Si un besoin thermique est détecté : Comfort obligatoire.

| chauffage_autorisation_cible | Décision | Raison | Signification |
|-----------------------------|----------|--------|---------------|
| comfort | Confort | besoin_thermique | Besoin thermique réel (seuil bas franchi) |
| neutre  | Neutre  | presence_on | Zone morte : abstention volontaire |
| reduced | Eco     | confort_suffisant | Confort jugé suffisant (seuil haut atteint) |

---

## 4) ÉTATS INTERDITS (non négociables)

| Situation | Interdiction |
|---------|--------------|
| Absence | Neutre interdit |
| Présence + chauffage_autorisation_cible = comfort | Neutre interdit |
| Blocage majeur actif | Confort interdit (hors forçage confort) |
| Présence seule (sans seuil) | Confort automatique interdit |

Cette table fait foi.

---

## ✅ STATUT

- Table **CANONIQUE**
- Version : Chauffage V3 PRO
- Référence unique pour :
  - décision centrale
  - capteurs canoniques
  - UI diagnostics
  - analyse de cohérence

---

## 🧾 OBSERVABILITÉ & TRAÇABILITÉ

Toute décision explicite doit produire :

- un changement de programme observable
- une notification persistante d’état **si pertinente**
- un logbook lisible
- une raison métier cohérente

L’utilisateur doit toujours pouvoir répondre à :
> **Pourquoi le chauffage est dans cet état ?**

Une notification persistante n’est créée que pour
les états thermiques structurants (ex. Confort).

Les états par défaut ou d’abstention (Eco, Neutre)
ne doivent produire aucune notification persistante.

---

## 📌 STATUT DU CONTRAT

- Contrat **STRUCTURANT**
- Version : Chauffage V3 PRO
- Toute évolution nécessite :
  - une mise à jour de ce document
  - une entrée de changelog Arsenal
  - une validation explicite

---

## ✅ CONCLUSION

Le chauffage Arsenal n’est pas un automatisme.
C’est un **système de décision gouverné**.

> **On ne chauffe pas parce qu’on peut.**
> **On chauffe parce que c’est justifié.**

Ce contrat est la référence.
