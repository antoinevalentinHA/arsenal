# ==========================================================
# 🚗 ARSENAL — CONTRAT NORMATIF
#     VOITURE — Audi A3 e-tron
# ==========================================================

## 🎯 OBJET DU CONTRAT

Ce contrat définit la **gouvernance normative complète** du domaine
**Voiture — Audi A3 e-tron** dans le système Arsenal.

Il établit :

- les **sources de vérité autorisées**,
- la **sécurisation des données cloud**,
- la **sélection des moments valides**,
- la **mémorisation et l’historisation**,
- la **gouvernance des automatisations métier**,
- la **restitution UI normative**,
- la **politique officielle de persistance**.

Ce contrat est **NORMATIF et OPPOSABLE**.

Il ne décrit pas :

- les détails d’implémentation YAML,
- les styles graphiques,
- les choix ergonomiques.

---

## 🧠 PRINCIPE FONDAMENTAL

Dans Arsenal, le sous-système Voiture repose sur une séparation stricte entre :

- **Donnée brute cloud**  
- **Donnée locale sécurisée**  
- **Décision métier**  
- **Mémorisation**  
- **Historisation**  
- **Restitution UI**

Aucune couche ne peut se substituer à une autre.

> **Le cloud mesure.  
> Le local sécurise.  
> L’automatisation décide.  
> Le helper mémorise.  
> Le recorder historise.  
> L’UI observe.**

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

1. Sécurisation des capteurs cloud Audi  
2. Capteurs stabilisés locaux (template triggered)  
3. Helpers métier (baselines, historiques)  
4. Automatisations métier :
   - enregistrement pleine charge  
   - archivage mensuel  
   - notification état de charge  
5. Capteurs statistiques  
6. Dashboards Voiture  
7. Templates UI normatifs  
8. Politique officielle de persistance Recorder  

Il ne couvre pas :

- l’intégration Audi elle-même,
- les API cloud,
- les mécanismes réseau.

---

## 🧩 ARCHITECTURE CANONIQUE DU DOMAINE

Le domaine Voiture est structuré selon la chaîne suivante :

1. **Capteurs cloud bruts** (non fiables par nature)
2. **Capteurs locaux stabilisés** (template triggered sensors)
3. **Automatisations de sélection métier**
4. **Helpers de mémorisation**
5. **Capteurs statistiques**
6. **Automatisations d’archivage**
7. **Persistance Recorder**
8. **UI & Dashboards normatifs**

Aucune donnée cloud brute n’est consommée directement par :

- une automation métier,
- un helper,
- une statistique,
- un dashboard.

---

## 🧪 COUCHE 1 — SÉCURISATION DES DONNÉES CLOUD

### 🎯 Principe

Toute donnée issue de l’intégration Audi est considérée comme :

- instable,
- sujette à `unknown` / `unavailable`,
- non fiable sans stabilisation.

### 🔒 Invariant

> Toute donnée cloud utilisée dans le domaine Voiture
> doit obligatoirement transiter par un **template triggered sensor local**.

### Capteurs concernés (exemples normatifs)

- Autonomie locale  
- Pourcentage moteur principal local  
- État de charge local  
- Kilométrage local  
- Dernière mise à jour locale  
- Temps de stationnement local  
- Prochaine inspection (temps)

Ces capteurs :

- conservent la **dernière valeur valide connue**,
- sont **reload-safe**,
- sont les **seules sources autorisées** pour les couches supérieures.

---

## 🧱 COUCHE 2 — HELPERS MÉTIER (MÉMORISATION)

### Helper canonique

  input_number.autonomie_audi_etron_full


### Rôle normatif

- mémoriser l’**autonomie réelle observée en pleine charge**,
- constituer une **baseline stable** par cycle de charge,
- servir de source unique pour les statistiques long terme.

### Invariants

- Mise à jour **uniquement** lorsque :
  - batterie ≥ 99 %
- Jamais :
  - estimation dynamique  
  - projection restante  
  - valeur instantanée  

---

## ⚙️ COUCHE 3 — AUTOMATISATIONS MÉTIER

### 1️⃣ Enregistrement pleine charge

Automation :

  /10_automations/voiture/autonomie.yaml
  ID : 1015000000001


Règles :

- déclenchée par variation du % batterie local,
- condition batterie ≥ 99 %,
- met à jour le helper baseline,
- envoie une notification **éphémère**.

---

### 2️⃣ Archivage mensuel

Automation :

  /10_automations/voiture/archive.yaml
  ID : 1015000000004


Règles :

- déclenchée mensuellement,
- archive la moyenne mensuelle,
- conserve 5 mois glissants.

---

### 3️⃣ Notification persistante — État de charge

Automation :

  /10_automations/voiture/notification_etat_charge.yaml
  ID : 10150000000005


Rôle normatif :

- matérialiser **un état métier unique** :
  > *Le véhicule est actuellement en charge*

Invariants absolus :

- notification = **projection d’un état courant**,
- aucune référence temporelle,
- aucun événement passé,
- cycle strict :
  - apparition quand état vrai,
  - extinction quand état faux,
- recalculable après reload YAML.

Cette automation est une :

> **Application — matérialisation d’état**

Elle ne contient :

- aucune logique décisionnelle,
- aucun calcul,
- aucun historique.

---

## 📊 COUCHE 4 — STATISTIQUES & ANALYSE

### Capteur statistique canonique

  sensor.autonomie_audi_e_tron_mensuelle


Source unique :

  input_number.autonomie_audi_etron_full


Règles :

- moyenne glissante 31 jours,
- utilisée exclusivement pour :
  - analyse de dérive batterie,
  - archivage mensuel,
  - dashboard batterie.

---

## 🖥️ COUCHE 5 — UI & DASHBOARDS (INTÉGRÉS AU CONTRAT)

### Dashboards normatifs

- `/lovelace/dashboards/voiture/audi.yaml`
- `/lovelace/dashboards/voiture/audi_securite.yaml`
- `/lovelace/dashboards/voiture/audi_batterie.yaml`

### Principe UI fondamental

L’UI :

- n’introduit **aucune logique métier**,
- ne décide jamais,
- ne corrige jamais une donnée,
- ne masque jamais une incohérence.

Elle est une :

> **Projection fidèle de l’état du système**

---

## 🎨 COUCHE 6 — TEMPLATES UI NORMATIFS

Les templates UI suivants sont **contractuellement intégrés** au domaine Voiture :

- carte_autonomie_seuils_variables  
- carte_batterie_seuils_variables  
- carte_etat_charge_vehicule  
- audi_etat_capteur  
- audi_etat_info  
- carte_duree_stationnement  
- carte_derniere_mise_a_jour  

### Invariants UI

- cartes **purement informationnelles**,
- aucune interaction,
- aucune action,
- aucun pilotage,
- couleur = **traduction d’un état**, jamais décision.

---

## 🗃️ COUCHE 7 — PERSISTANCE & HISTORISATION (RECORDER)

### 📂 Fichier de référence

  /homeassistant/recorder.yaml


Section officielle :

```yaml
# ==== 🚗 AUTOMOBILE ====
- sensor.autonomie_audi_e_tron_mensuelle
- sensor.audi_e_tron_pourcentage_moteur_principal_local
- sensor.audi_e_tron_kilometrage_local
- sensor.audi_e_tron_autonomie_local
- sensor.audi_e_tron_etat_de_charge_local
- sensor.audi_a3_sportback_e_tron_range_local
- sensor.audi_a3_sportback_e_tron_charging_state_local
- sensor.audi_a3_sportback_e_tron_primary_engine_percent_local
- input_number.autonomie_audi_etron_full
