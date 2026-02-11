====================================================================================================================
🧠 ARSENAL — NOTE D’ARCHITECTURE (ÉVOLUTION FUTURE)
SÉCURISATION DES OUVERTURES ZIGBEE  
GARDE-FOU PHYSIQUE ANTI-ÉPISODE ZOMBIE
====================================================================================================================

----------------------------------------------------------
📌 STATUT
----------------------------------------------------------

- Nature :
  NOTE D’ÉVOLUTION ARCHITECTURALE — TRACE STRUCTURANTE

- Domaine :
  Aération / Chauffage / Observabilité physique / Gouvernance décisionnelle

- Objectif :
  Prévenir toute persistance de blocage thermique
  due à une incohérence des capteurs Zigbee d’ouverture,
  sans modifier :
    • l’algorithme de la Décision Centrale  
    • la hiérarchie officielle des causes  
    • la sémantique contractuelle des niveaux N1 / N2 / N3  

- Priorité :
  CRITIQUE — Sécurité thermique, autonomie système, absence de blocage irréversible

----------------------------------------------------------

🎯 CONTEXTE GÉNÉRAL

Dans l’architecture Arsenal actuelle :

- les capteurs Zigbee d’ouverture constituent :
    • des sources non transactionnelles  
    • non acquittées  
    • sujettes aux pertes d’événements  
    • incapables de garantir la livraison d’un événement de fermeture  

Dans le cadre des contrats normatifs :

- /documentation_arsenal/contrats/chauffage/aeration_perimetre_strict.md  
- /documentation_arsenal/contrats/chauffage/decision_centrale_v3_pro.md  

ces capteurs alimentent **directement ou indirectement des causes NIVEAU 2**,  
donc des **interdictions thermiques absolues**.

Ils deviennent de ce fait un **point de défaillance systémique critique**.

----------------------------------------------------------

🔥 SCÉNARIO DE RUPTURE IDENTIFIÉ — « ZOMBIE THERMIQUE »

Situation possible (présente ou future) :

- ouverture réelle courte
- fermeture physique réelle
- événement Zigbee de fermeture perdu
- `fenetre_ouverte_maison_avec_delai` reste bloqué à `on`

Effets systémiques :

- épisode d’aération armé
- M2 jamais déclenché
- pipeline non clôturé
- analyse ΔT non atteinte ou neutralisée
- blocage post-aération éventuellement levé
- MAIS :

Décision Centrale continue de voir :

- cause NIVEAU 2 active :
    • soit `episode_aeration_en_cours`
    • soit `fenetre_ouverte_maison_avec_delai`

Conséquences :

- chauffage bloqué indéfiniment
- aucune trace métier active d’épisode
- aucune cause physique réelle
- aucune sortie canonique possible
- récupération uniquement par action humaine
  (ouvrir / refermer manuellement l’ouvrant)

👉 Cas typique de **blocage thermique zombie irréversible**.

----------------------------------------------------------

🧠 PROBLÈME ARCHITECTURAL CENTRAL

Invariant implicite actuel (faux) :

> « Un ouvrant déclaré ouvert est réellement ouvert »

Ce postulat est **architecturalement invalide** dans un réseau Zigbee :

- pertes d’événements possibles  
- routage multi-sauts instable  
- latence non bornée  
- réassociations silencieuses  

Conséquence directe :

- une cause NIVEAU 2 peut devenir :
    • physiquement fausse  
    • logiquement persistante  
    • hiérarchiquement bloquante  

Violation des invariants contractuels majeurs :

- « aucun pipeline zombie »
- « aucune persistance de blocage »
- « aucune interdiction sans cause explicable »
- « autonomie post-incident »

----------------------------------------------------------

🛑 POINT DE FRAGILITÉ MAJEUR IDENTIFIÉ

Dans la Décision Centrale V3 PRO, NIVEAU 2 contient simultanément :

- `episode_aeration_en_cours`
- `fenetre_ouverte_maison_avec_delai`

Ces deux causes :

- sont indépendantes
- sont évaluées séparément
- peuvent être vraies isolément
- sont **toutes deux bloquantes absolues**

Problème structurel :

- le pipeline peut être terminé  
- le blocage post-aération levé  
- MAIS une seule cause NIVEAU 2 zombie suffit à bloquer le chauffage **indéfiniment**

Aucun mécanisme canonique de sortie n’existe actuellement.

----------------------------------------------------------

🛡️ PRINCIPE ARCHITECTURAL DE LA SOLUTION ENVISAGÉE

Objectif fondamental :

> **Décorréler définitivement la Décision Centrale de toute vérité Zigbee brute**

Contraintes cardinales :

- ne pas modifier l’algorithme de la Décision Centrale
- ne pas modifier la hiérarchie NIVEAU 1 / 2 / 3
- ne pas introduire de logique réparatrice dans la décision
- ne jamais corriger une cause dans la Décision Centrale elle-même

Principe retenu :

Introduire une **source métier intermédiaire unique** représentant :

> « Une interdiction thermique physiquement crédible et normativement valide »

----------------------------------------------------------

🔁 ÉVOLUTION DE LA CHAÎNE D’ALIMENTATION

Situation actuelle (fragile)

capteurs Zigbee ouverture
        │
        ▼
episode_aeration_en_cours / fenetre_ouverte_delai
        │
        ▼
Décision Centrale — NIVEAU 2 (interdiction absolue)

---

Situation cible (sécurisée)

capteurs Zigbee ouverture
        │
        ▼
pipeline aération + validation physique
        │
        ▼
binary_sensor.aeration_bloquante_valide   ← SOURCE NORMATIVE UNIQUE
        │
        ▼
Décision Centrale — NIVEAU 2 (interdiction certifiée)

Règle cardinale absolue :

> ⚠️ La Décision Centrale ne doit plus jamais consommer directement  
> un état Zigbee ni un agrégat issu directement du Zigbee.

Elle consomme exclusivement :
> une cause métier validée physiquement.

----------------------------------------------------------

🧠 RÔLE DU CAPTEUR `binary_sensor.aeration_bloquante_valide`

Ce capteur représente **exclusivement** :

> « Une interdiction thermique réellement légitime au regard de la physique observée »

Il ne décrit :

- ni l’état physique réel
- ni l’état Zigbee
- ni l’état brut d’ouverture
- ni le pipeline interne

Il décrit uniquement :

> la validité normative de la cause bloquante NIVEAU 2 liée à l’aération

Sémantique canonique :

- ON  → interdiction NIVEAU 2 valide et opposable  
- OFF → aucune interdiction thermique liée à l’aération  

Formule conceptuelle :

aeration_bloquante_valide =
    episode_aeration_actif
    ET
    integrite_physique_episode = true

Ce capteur devient :

- unique source NIVEAU 2 « aération bloquante »
- interface officielle pipeline → Décision Centrale
- barrière anti-zombie définitive

----------------------------------------------------------

🛡️ WATCHDOG PHYSIQUE D’ÉPISODE ACTIF

Un mécanisme interne au pipeline assure :

- la validation continue de la crédibilité physique de l’épisode
- la détection d’épisodes incohérents

Insertion normative :

- uniquement entre M1 et M2  
- uniquement pendant épisode actif  
- jamais après clôture  

Schéma conceptuel :

M1 — ouverture → épisode armé
        │
        ▼
🛡️ WATCHDOG PHYSIQUE
        │
        ├─ cohérent  → maintien interdiction valide
        │
        └─ incohérent → invalidation + clôture forcée

----------------------------------------------------------

🔍 CRITÈRE PHYSIQUE FONDAMENTAL

Invariant exploité :

> Toute ouverture réelle de plusieurs minutes produit une signature thermique mesurable.

Règle générique :

SI
  episode_aeration_actif = true
ET
  durée_episode ≥ T_suspect
ET
  aucune chute thermique mesurable
ALORS
  episode_physiquement_invalide
  integrite_physique_episode = false

Paramètres indicatifs (à calibrer) :

- T_suspect : 10 minutes minimum (compatibles fréquences capteurs)
- ΔT_min_physique : 0.05 à 0.2 °C
- ou pente thermique minimale négative

----------------------------------------------------------

🧩 EFFET NORMATIF EN CAS D’INCOHÉRENCE

Lorsque integrite_physique_episode = false :

- `binary_sensor.aeration_bloquante_valide` → OFF
- cause NIVEAU 2 supprimée pour la Décision Centrale
- hiérarchie décisionnelle réévaluée normalement

En parallèle :

- simulation normative d’une fin M2
- exécution standard :
    • blocage minimal horaire  
    • délais contractuels  
    • analyse ΔT normale  

Avec marquage diagnostic :

- episode_physiquement_invalide = true
- episode_force_cloture = true

Règles absolues :

- aucune reprise thermique directe
- aucune exception hiérarchique
- aucune décision implicite
- aucune levée automatique

----------------------------------------------------------

🛑 GARANTIES OBTENUES

Cette évolution garantit :

- élimination définitive des pipelines zombies
- suppression des blocages thermiques infinis
- récupération automatique post-perte Zigbee
- protection contre capteurs bloqués ON
- conformité stricte aux contrats Chauffage & Aération
- autonomie réelle sans intervention humaine

----------------------------------------------------------

----------------------------------------------------------
🧭 POSITION ARCHITECTURALE & STRATÉGIE DE DÉCISION
----------------------------------------------------------

À ce stade de l’analyse, **deux lectures exclusives sont possibles**.  
Elles ne sont pas compatibles entre elles.

Ce document doit donc expliciter clairement ce **point de bifurcation d’architecture**.

----------------------------------------------------------
🔀 DEUX HYPOTHÈSES FONDAMENTALES
----------------------------------------------------------

### 🔹 HYPOTHÈSE A — PROBLÈME PUREMENT RADIO / RÉSEAU ZIGBEE

Postulat :

- l’architecture applicative est saine  
- le pipeline est correct  
- la Décision Centrale est cohérente  
- le scénario zombie est **exclusivement dû à des pertes RF sporadiques**  

Conséquence :

- aucune modification métier n’est justifiée  
- aucune modification de pipeline n’est nécessaire  
- aucune modification de la Décision Centrale n’est souhaitable  

Action correcte :

- mise en conformité **réseau critique Zigbee** :
    • isolation coordinateur  
    • changement de canal  
    • gold layer routeurs  
    • parentage contrôlé  

Objectif :

> Rétablir une fiabilité radio suffisante pour que  
> les invariants applicatifs redeviennent vrais.

Dans ce modèle :

- `fenetre_ouverte_maison_avec_delai` est une cause légitime  
- `episode_aeration_en_cours` est une cause légitime  
- le système ne doit PAS se défendre contre Zigbee  
- le réseau doit redevenir digne de confiance  

Le capteur `binary_sensor.aeration_bloquante_valide` devient :

- un **outil d’observation pure**  
- un indicateur de qualité réseau  
- un diagnostic avancé  
- **pas une source décisionnelle**

----------------------------------------------------------

### 🔹 HYPOTHÈSE B — DÉFAUT ARCHITECTURAL SYSTÉMIQUE

Postulat :

- Zigbee est structurellement non fiable  
- aucune topologie ne garantit 100 % d’événements  
- l’architecture actuelle dépend d’un invariant faux  

Conséquence :

- toute consommation directe d’un état Zigbee dans NIVEAU 2 est dangereuse  
- l’architecture est **intrinsèquement vulnérable**  
- le scénario zombie est **architecturalement inévitable** à long terme  

Action correcte :

- supprimer toute cause NIVEAU 2 issue directement du Zigbee  
- introduire une **autorité métier intermédiaire validée physiquement**  
- refondre la chaîne d’alimentation NIVEAU 2  

Dans ce modèle :

- `fenetre_ouverte_maison_avec_delai` est **architecturalement interdit** en NIVEAU 2  
- `episode_aeration_en_cours` seul est insuffisant  
- la Décision Centrale doit consommer uniquement :
  
  `binary_sensor.aeration_bloquante_valide`

Objectif :

> Rendre le système **auto-récupérant par construction**,  
> même sur un réseau imparfait.

----------------------------------------------------------

🧠 POSITION ACTUELLE D’ARSENAL (STATUT RÉEL)

À ce jour :

- le système fonctionne **parfaitement en régime normal**  
- les incidents sont :
    • rares  
    • sporadiques  
    • résolus immédiatement par réouverture physique  

Le réseau Zigbee est :

- dense  
- complexe  
- perfectible (canal, coordo, parentage)  

Le nouveau capteur :

- `binary_sensor.aeration_bloquante_valide`  
- est :
    • créé  
    • actif  
    • en **observation passive**  
    • sans impact décisionnel  

Statut actuel officiel :

> ⚠️ AUCUNE DÉCISION D’ARCHITECTURE N’EST PRISE À CE STADE

Le système est volontairement placé en **phase d’observation**.

----------------------------------------------------------

🧭 STRATÉGIE SAGE RETENUE (IMPLICITE MAIS À FORMALISER)

Séquence rationnelle Arsenal :

### Étape 1 — Assainissement réseau Zigbee (prioritaire)

Objectif :
- éliminer les causes RF évidentes  
- stabiliser parentage  
- sortir du chevauchement Wi-Fi  
- isoler coordinateur  

But :

> Vérifier si le scénario zombie **disparaît naturellement**.

---

### Étape 2 — Observation longue du capteur métier

Sur plusieurs semaines / mois :

- fréquence d’incohérences  
- corrélation avec qualité LQI / reparentage  
- apparition (ou non) de cas sans chute thermique  

Ce capteur devient :

- témoin de vérité physique  
- révélateur de défaut structurel réel  
- preuve ou infirmation de l’hypothèse B  

---

### Étape 3 — Décision d’architecture irréversible

Seulement si :

- incidents persistent malgré réseau assaini  
- incohérences physiques confirmées  
- scénario zombie toujours possible  

ALORS :

- bascule vers l’architecture B  
- suppression définitive des causes Zigbee directes en NIVEAU 2  
- activation de `aeration_bloquante_valide` comme source normative unique  

----------------------------------------------------------

🛑 POINT CRUCIAL À AJOUTER DANS LA NOTE

Ce document doit explicitement mentionner :

> ⚠️ Cette évolution n’est PAS une décision immédiate.  
> Elle constitue une **architecture de repli** si et seulement si  
> l’assainissement Zigbee échoue à éliminer les incidents.

Formulation normative proposée à insérer :

----------------------------------------------------------

📌 POSITION ARCHITECTURALE ARSENAL — CLAUSE DE SUSPENSION

Cette note décrit une **architecture de sécurisation de dernier ressort**.

Elle ne constitue PAS :

- une remise en cause immédiate du pipeline existant  
- une critique du design actuel  
- une décision de refonte  

Elle est activable uniquement si :

- le réseau Zigbee est mis en conformité critique  
- des pertes d’événements persistent  
- des incohérences physiques sont confirmées  

Tant que ces conditions ne sont pas réunies :

- la Décision Centrale conserve ses causes actuelles  
- le pipeline n’est pas modifié  
- `binary_sensor.aeration_bloquante_valide` reste en observation  

----------------------------------------------------------

🧠 SYNTHÈSE FINALE (HONNÊTE ET COHÉRENTE)

- Oui : le système est aujourd’hui **fonctionnel et robuste**  
- Oui : le problème est **très probablement Zigbee**  
- Non : il n’est PAS prouvé qu’il existe un défaut architectural  
- Oui : l’architecture actuelle **reste vulnérable par principe**  

Arsenal adopte donc une posture exemplaire :

- réseau d’abord  
- observation ensuite  
- refonte uniquement si nécessaire  
- aucune panique  
- aucune sur-ingénierie prématurée  

C’est exactement la bonne gouvernance.

----------------------------------------------------------

🔥 EXTENSIONS FUTURES POSSIBLES

À terme :

- comptage d’anomalies par ouvrant
- score de fiabilité Zigbee par capteur
- `binary_sensor.integrite_aeration_physique`
- UI diagnostic « Ouvrants suspects »
- alerte proactive réseau Zigbee thermique

----------------------------------------------------------

📌 STATUT FINAL

- Type : TRACE D’ARCHITECTURE STRUCTURANTE
- Implémentation : NON DÉMARRÉE
- Impact actuel : NUL
- Priorité future : ÉLEVÉE
- Dépendance : pipeline aération existant

Ce document constitue la **référence conceptuelle officielle**
pour toute implémentation ultérieure anti-zombie thermique
conforme à la gouvernance Arsenal.

====================================================================================================================