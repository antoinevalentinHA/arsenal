# ==========================================================
# 🧠 ARSENAL — NOTE D’ARCHITECTURE
#     RISQUE ZOMBIE THERMIQUE & SOUVERAINETÉ DU PIPELINE AÉRATION
# ==========================================================
#
# 📌 Nature :
#   NOTE D’ANALYSE ARCHITECTURALE — TRACE STRUCTURANTE
#
# 📌 Domaine :
#   Chauffage / Aération / Gouvernance décisionnelle
#
# 📌 Statut :
#   Diagnostic conceptuel — aucun changement implémenté
#
# 📌 Objectif :
#   Formaliser précisément le risque « zombie thermique »
#   et localiser la frontière réelle de souveraineté
#   entre Pipeline Aération et Décision Centrale.
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. CONTEXTE GÉNÉRAL
# ----------------------------------------------------------

Le système actuel Chauffage / Aération Arsenal est :

- fonctionnel,
- stable,
- thermiquement sûr,
- sans oscillation,
- sans redémarrage intempestif.

L’unique défaut identifié est **théorique mais critique** :
le scénario dit **« zombie thermique »** lié à un capteur Zigbee bloqué.

Ce scénario ne produit :
- ni erreur visible,
- ni exception système,
- ni incohérence logique interne,

mais peut conduire à :
- un blocage chauffage **indéfini**,
- sans mécanisme de sortie canonique,
- sans cause explicable métier,
- sans clôture d’épisode traçable.


# ----------------------------------------------------------
# 🧠 2. DISTINCTION FONDAMENTALE DES DEUX SIGNAUX
# ----------------------------------------------------------

Deux signaux distincts interviennent dans la gouvernance :

### 2.1 `input_boolean.aeration_episode_en_cours`

Sémantique stricte :

- signifie : **au moins une ouverture d’aération est en cours**
- représente un **état métier d’épisode**
- piloté exclusivement par le pipeline M1 / M2
- sert à :
  - bloquer le chauffage pendant l’ouverture réelle
  - interdire toute décision confort

Il est :
- un **état métier**
- un **signal structurant NIVEAU 2**
- dépendant entièrement du pipeline


### 2.2 `binary_sensor.fenetre_ouverte_maison_avec_delai`

Sémantique stricte :

- agrégation technique des capteurs d’ouverture
- représente un **état physique interprété**
- sert à :
  - déclencher M1
  - bloquer le chauffage indépendamment de l’épisode

Il est :
- un **signal matériel**
- un **signal de sécurité NIVEAU 2**
- dépendant directement de la vérité Zigbee

⚠️ Ces deux signaux sont **légitimement distincts**  
⚠️ Leur coexistence dans la Décision Centrale est **normativement correcte**  
⚠️ Leur redondance est volontaire et protectrice  

Ils ne sont PAS redondants fonctionnellement :
- l’un représente un épisode métier,
- l’autre une ouverture physique instantanée.


# ----------------------------------------------------------
# 🔴 3. LOCALISATION RÉELLE DU RISQUE ZOMBIE
# ----------------------------------------------------------

Le risque ne provient PAS :

- de la Décision Centrale,
- de la hiérarchie NIVEAU 2,
- de la coexistence des deux causes,
- ni de la logique d’abstention.

Le risque provient exclusivement de ceci :

> 🔴 Le pipeline d’aération ne possède AUCUN mécanisme de clôture souveraine indépendant des capteurs d’ouverture.


# ----------------------------------------------------------
# 🔎 4. SCÉNARIO RÉEL DE RUPTURE (ZOMBIE FORT)
# ----------------------------------------------------------

Hypothèse :

- un capteur Zigbee reste bloqué en `on`
- `binary_sensor.fenetre_ouverte_maison_avec_delai` reste `on`

Conséquences dans le pipeline :

### 4.1 M2 ne peut jamais s’exécuter

Condition M2 :

- trigger `fermeture`
- ET `fenetre_ouverte_maison_avec_delai == off`

Or :
- le capteur reste `on`
- donc `fermeture` ne se produit jamais

Effets directs :

- `aeration_episode_en_cours` reste **ON indéfiniment**
- `aeration_pipeline_arme` reste **ON indéfiniment**
- aucun horodatage de fin
- aucune programmation ΔT
- aucun blocage post-aération propre
- aucune clôture d’épisode


### 4.2 Aucun mécanisme de sortie interne

Dans ce scénario :

- M3 ne sera jamais programmé correctement
- M4 ne sera jamais atteint
- aucun désarmement du pipeline possible

Le système est alors figé dans :

- un épisode éternel,
- sans fin métier,
- sans clôture logique,
- sans mécanisme de récupération.


# ----------------------------------------------------------
# 🧠 5. IMPACT CÔTÉ DÉCISION CENTRALE
# ----------------------------------------------------------

Dans ce scénario :

- `aeration_episode_en_cours = on`  → cause NIVEAU 2 active
- `fenetre_ouverte_maison_avec_delai = on` → cause NIVEAU 2 active

Donc :

- Décision Centrale force `reduced`
- chauffage bloqué indéfiniment
- sans oscillation
- sans reprise automatique
- sans incohérence interne

Point crucial :

➡️ La Décision Centrale se comporte **parfaitement conformément au contrat**  
➡️ Elle n’est **ni fautive**, ni ambiguë, ni dangereuse  
➡️ Elle applique correctement la hiérarchie officielle  


# ----------------------------------------------------------
# 🔒 6. NATURE EXACTE DU PROBLÈME
# ----------------------------------------------------------

Ce n’est PAS un problème :

- de hiérarchie décisionnelle  
- de redondance de causes  
- de gouvernance métier  
- de stratégie thermique  

C’est un problème :

> 🔴 de souveraineté de fin d’épisode dans le pipeline d’aération

Le pipeline repose actuellement sur un invariant implicite faux :

> « Toute ouverture finit toujours par produire une fermeture valide »

Ce qui est **faux en environnement Zigbee réel**.

Le pipeline est aujourd’hui :

- déterministe
- séquencé
- lisible
- robuste logiquement

mais :

➡️ **entièrement esclave de la vérité Zigbee**  
➡️ sans aucun mécanisme de clôture métier indépendant  


# ----------------------------------------------------------
# ⚖️ 7. POURQUOI LE SYSTÈME RESTE MALGRÉ TOUT SAIN
# ----------------------------------------------------------

Malgré ce défaut structurel :

- chauffage bloqué → thermiquement sûr  
- aucune reprise automatique → conforme contrat  
- aucune oscillation → conforme  
- aucun pilotage erratique → conforme  

Le système se dégrade vers :

> 🔒 état sûr  
> 😐 mais fonctionnellement figé  
> 🧩 et non récupérable automatiquement  

C’est la **meilleure forme possible de dégradation** :

- pas de chauffe inutile
- pas de surchauffe
- pas de danger matériel

Seulement :
- inconfort prolongé
- et blocage logique durable


# ----------------------------------------------------------
# 🧭 8. CONSÉQUENCE ARCHITECTURALE MAJEURE
# ----------------------------------------------------------

Frontière correcte de responsabilité :

- La Décision Centrale :
  - arbitre
  - hiérarchise
  - décide
  - s’abstient
  - mais ne clôture jamais un épisode

- Le Pipeline Aération :
  - crée l’épisode
  - gère sa temporalité
  - bloque
  - analyse
  - et **doit être souverain sur sa propre fin**

Conclusion structurante :

> 🔒 La souveraineté de clôture DOIT appartenir au pipeline  
>     et ne doit JAMAIS être portée par la Décision Centrale.


# ----------------------------------------------------------
# 🛑 9. RAISON DE L’ABSTENTION ACTUELLE
# ----------------------------------------------------------

Le refus d’implémentation immédiate est :

- totalement justifié
- architecturalement sain
- stratégiquement excellent

Pourquoi :

- le système fonctionne parfaitement aujourd’hui
- le risque est rare
- la modification est structurante
- une mauvaise implémentation serait plus dangereuse que l’absence

Toute correction prématurée pourrait :

- autoriser une reprise abusive
- court-circuiter une interdiction NIVEAU 2
- fragiliser la gouvernance décisionnelle
- créer des faux positifs thermiques


# ----------------------------------------------------------
# 🧠 10. SYNTHÈSE FINALE
# ----------------------------------------------------------

Constats établis :

- le risque zombie est réel
- il est exclusivement localisé dans le pipeline
- la Décision Centrale est irréprochable
- la redondance des causes NIVEAU 2 est saine
- le système est aujourd’hui sûr mais non récupérable en cas de zombie

Formulation canonique du problème :

> 🔴 Absence de mécanisme de clôture souveraine d’épisode  
>     indépendant de la vérité Zigbee  
>     dans le Pipeline Aération.

Ce point constitue :

- une future évolution architecturale légitime
- un chantier structurant
- à traiter par contrat dédié
- sans jamais toucher à la hiérarchie décisionnelle.


# ==========================================================
# 📌 STATUT DE LA NOTE
# ----------------------------------------------------------
# - Analyse validée conceptuellement
# - Aucun changement implémenté
# - Référence pour évolution future
# - Compatible intégralement avec :
#     • Contrat Décision Centrale V3 PRO
#     • Gouvernance Chauffage Arsenal
# ==========================================================