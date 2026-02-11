# ==========================================================
# 🧠 ARSENAL — NOTE D’ARCHITECTURE STRUCTURANTE
#     Sécurisation des ouvertures Zigbee
#     Garde-fou physique anti-épisodes zombies
# ==========================================================

## 📌 STATUT

- Nature :
  NOTE D’ARCHITECTURE — TRACE STRUCTURANTE (non implémentée)

- Domaine :
  Ouvertures / Aération / Chauffage / Gouvernance décisionnelle / Observabilité thermique

- Objectif :
  Éliminer définitivement tout **blocage thermique persistant** dû à une
  incohérence Zigbee sur un ouvrant, sans altérer :
  - la Décision Centrale,
  - la hiérarchie des causes,
  - le pipeline d’aération existant,
  - ni les contrats normatifs en vigueur.

- Priorité :
  CRITIQUE — Sécurité thermique et autonomie système

---

## 🎯 PROBLÈME ARCHITECTURAL DE RÉFÉRENCE

### Situation pathologique observée

- Ouverture brève réelle  
- Fermeture réelle  
- Événement Zigbee de fermeture perdu  

Conséquences actuelles possibles :

- `binary_sensor.fenetre_ouverte_*` reste ON  
- `input_boolean.aeration_episode_en_cours` reste ON  
- Décision Centrale reçoit une **cause NIVEAU 2 invalide**  
- Chauffage bloqué **indéfiniment**  
- Aucune auto-récupération possible  

👉 Pipeline zombie thermique.

---

## 🧠 INVARIANT FAUX IDENTIFIÉ

Postulat actuellement implicite :

> “Un ouvrant déclaré ouvert est réellement ouvert.”

Ce postulat est **structurellement faux** dans un environnement Zigbee :

- non transactionnel  
- pertes d’événements possibles  
- pas de garantie de livraison de fermeture  

➡️ Une cause bloquante NIVEAU 2 peut être **corrompue à la source**.

---

## 🔥 PÉRIMÈTRE STRICT DE LA SOLUTION

### Ce qui est concerné

Uniquement :

- la phase **“fenêtre ouverte / épisode actif”**
- les causes NIVEAU 2 avant fermeture
- les états alimentés directement par Zigbee

### Ce qui est explicitement EXCLU

⛔ Post-aération  
⛔ Blocage inertiel  
⛔ Analyse ΔT  
⛔ Pipeline M2 / M3 / M4  
⛔ `input_boolean.chauffage_blocage_aeration`  

Rappel contractuel fondamental :

- `input_boolean.chauffage_blocage_aeration`  
  ➜ n’existe que **post-fermeture**  
  ➜ ne dépend plus de Zigbee  
  ➜ est intrinsèquement robuste  
  ➜ **ne doit jamais être modifié ni encapsulé**

---

## 🧩 PRINCIPE ARCHITECTURAL RETENU

### Règle cardinale

> ⚠️ La Décision Centrale ne doit **plus jamais consommer directement**
> un état Zigbee d’ouverture comme cause NIVEAU 2.

Elle ne consomme que :

> une **cause métier validée physiquement**

---

## 🧠 NOUVEL OBJET CANONIQUE ENVISAGÉ

### Entité cible

`binary_sensor.aeration_bloquante_valide`

### Rôle unique

Représenter exclusivement :

> “Une interdiction thermique réellement légitime au regard de la physique observée”

Ce capteur :

- ❌ ne représente pas un état d’ouvrant  
- ❌ ne représente pas l’état Zigbee  
- ❌ ne représente pas un épisode brut  
- ❌ ne représente pas un blocage post-aération  

Il représente uniquement :

> la **validité physique normative** de la cause bloquante “aération en cours”

---

## 🔍 SÉMANTIQUE NORMATIVE

| État | Signification canonique |
|------|------------------------|
| ON   | Interdiction NIVEAU 2 physiquement crédible |
| OFF  | Aucune interdiction thermique liée à l’aération |

---

## 🔁 POSITIONNEMENT DANS LA CHAÎNE

### Situation actuelle (fragile)

capteurs Zigbee  
→ temporisations  
→ agrégations  
→ Décision Centrale (NIVEAU 2)

### Situation cible (sécurisée)

capteurs Zigbee  
→ pipeline aération  
→ 🛡️ validation physique  
→ `binary_sensor.aeration_bloquante_valide`  
→ Décision Centrale (NIVEAU 2 certifié)

---

## 🛡️ WATCHDOG PHYSIQUE D’ÉPISODE ACTIF

### Périmètre

Actif uniquement :

- pendant `input_boolean.aeration_episode_en_cours = on`  
- avant toute fermeture  
- avant M2  
- avant tout blocage inertiel  

### Principe

Invariant exploité :

> Toute ouverture réelle prolongée produit une signature thermique mesurable.

---

## 🔎 CRITÈRE PHYSIQUE GÉNÉRIQUE

### Condition d’invalidation

SI :

- `aeration_episode_en_cours = true`  
- durée épisode ≥ T_suspect  
- aucune chute thermique mesurable  

ALORS :

- épisode physiquement invalide  
- interdiction levée  

---

### Paramètres indicatifs (non figés)

| Paramètre | Valeur indicative |
|-----------|------------------|
| T_suspect | 10 minutes |
| ΔT_min    | 0.05 à 0.2 °C |
| Source    | température de la pièce concernée |

---

## 🧩 PORTÉE MULTI-PIÈCES

Contraintes identifiées :

- les capteurs inertiels actuels ne couvrent que les chambres  
- une erreur Zigbee dans le séjour ou l’entrée ne serait pas détectée  

Principe retenu :

- validation physique **localisée par pièce**
- chaque ouvrant est associé à :
  - un capteur thermique de la même zone  

Capteurs cibles minimaux :

- `sensor.temperature_sejour`  
- `sensor.temperature_entree`  
- `sensor.temperature_chambre_parents`  
- `sensor.temperature_chambre_arnaud`  
- `sensor.temperature_chambre_matthieu`  

---

## 🧠 FORMULE CONCEPTUELLE CANONIQUE

```text
aeration_bloquante_valide =
    aeration_episode_en_cours
AND
    integrite_physique_episode = true

Avec :

integrite_physique_episode =
    chute_thermique_mesurable(zone_associee)

🛑 EFFET NORMATIF EN CAS D’INVALIDATION

Lorsque l’épisode est jugé physiquement invalide :

binary_sensor.aeration_bloquante_valide → OFF
Décision Centrale ne reçoit plus aucune cause NIVEAU 2
Chauffage redevient gouverné normalement

En parallèle (diagnostic uniquement) :

marquage :
episode_physiquement_invalide = true
episode_force_cloture = true

Sans :
reprise directe
exception hiérarchique
décision implicite

🔒 GARANTIES OBTENUES

Cette architecture garantit :

élimination définitive des pipelines zombies
suppression des blocages infinis
auto-récupération post-perte Zigbee
protection contre capteurs bloqués ON
indépendance complète Zigbee / Décision
respect strict des contrats Aération & Chauffage

🚫 INTERDICTIONS ABSOLUES

Il est STRICTEMENT INTERDIT :

de faire consommer Zigbee directement par la Décision Centrale
d’invalider un blocage post-aération
d’interférer avec chauffage_blocage_aeration
de déclencher une reprise thermique depuis ce mécanisme
d’introduire une logique réparatrice dans la décision

🧭 POSITIONNEMENT CONTRACTUEL

Ce mécanisme :
ne modifie aucun contrat existant
ne fusionne aucun domaine
n’introduit aucune nouvelle décision
agit exclusivement comme barrière de sécurité physique

Il constitue :
une couche d’intégrité intermédiaire
entre perception Zigbee et gouvernance thermique.

📌 STATUT FINAL

Type : Trace d’architecture structurante
Implémentation : NON DÉMARRÉE
Validation : conceptuelle uniquement
Dépendances :
pipeline aération existant
capteurs thermiques par pièce
Ce document constitue la référence canonique pour toute implémentation ultérieure.
==========================================================
🛑 FIN NOTE — RÉFÉRENCE ARCHITECTURALE OFFICIELLE
==========================================================