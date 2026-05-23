# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
# Simulation de présence
# ==========================================================

## 🎯 Finalité

La **simulation de présence** a pour objectif de **reproduire un comportement lumineux crédible** lors d'une absence réelle du foyer, afin de donner l'illusion d'une habitation occupée.

Elle est **strictement cosmétique** et ne doit **jamais** :

* compromettre la sécurité,
* perturber la logique de présence réelle,
* introduire de décisions implicites,
* piloter un équipement sans autorisation explicite.

---

## 🧠 Principes fondateurs Arsenal

* **Séparation stricte des rôles** :

  * Paramètres → Génération → Interprétation → Action → Vigilance
* **Aucune logique cachée dans l'UI**
* **Aucune action directe depuis un script de calcul**
* **Aucune dépendance temporelle implicite**
* **Tolérance totale aux redémarrages**

La simulation de présence est un **sous-système autonome**, lisible, testable et désactivable.

---

## 🧩 Architecture fonctionnelle

### Zones couvertes

Trois zones sont actives :

* `chambre_parents`
* `garage`
* `entree`

---

### 1️⃣ Paramètres métier (intention)

Helpers configurables par l'utilisateur :

* **Intensité** (nombre de cycles par zone) :

  * `input_number.nb_cycles_simulation_presence_matin_chambre_parents`
  * `input_number.nb_cycles_simulation_presence_matin_garage`
  * `input_number.nb_cycles_simulation_presence_matin_entree`
  * `input_number.nb_cycles_simulation_presence_soir_chambre_parents`
  * `input_number.nb_cycles_simulation_presence_soir_garage`
  * `input_number.nb_cycles_simulation_presence_soir_entree`

* **Durées de cycle** (communes à toutes les zones) :

  * `input_number.duree_min_cycle_simulation_presence`
  * `input_number.duree_max_cycle_simulation_presence`

* **Cadres horaires autorisés** (par zone et période) :

  * `input_datetime.debut_cycle_simulation_presence_matin_chambre_parents`
  * `input_datetime.fin_cycle_simulation_presence_matin_chambre_parents`
  * `input_datetime.debut_cycle_simulation_presence_soir_chambre_parents`
  * `input_datetime.fin_cycle_simulation_presence_soir_chambre_parents`
  * `input_datetime.debut_cycle_simulation_presence_matin_garage`
  * `input_datetime.fin_cycle_simulation_presence_matin_garage`
  * `input_datetime.debut_cycle_simulation_presence_soir_garage`
  * `input_datetime.fin_cycle_simulation_presence_soir_garage`
  * `input_datetime.debut_cycle_simulation_presence_matin_entree`
  * `input_datetime.fin_cycle_simulation_presence_matin_entree`
  * `input_datetime.debut_cycle_simulation_presence_soir_entree`
  * `input_datetime.fin_cycle_simulation_presence_soir_entree`

Ces paramètres **n'entraînent aucune action directe**.

---

### 2️⃣ Génération des horaires (données)

* **Script** : `script.generer_horaires_simulation_presence`

Rôle exclusif :

* Générer **une fois par jour** des horaires pseudo-aléatoires
* Figer ces horaires dans des helpers persistants

Sorties (par zone et période) :

* `input_text.horaires_simulation_presence_matin_chambre_parents`
* `input_text.horaires_simulation_presence_soir_chambre_parents`
* `input_text.horaires_simulation_presence_matin_garage`
* `input_text.horaires_simulation_presence_soir_garage`
* `input_text.horaires_simulation_presence_matin_entree`
* `input_text.horaires_simulation_presence_soir_entree`

Caractéristiques :

* Non déterministe (volontaire)
* Sans action matérielle
* Sans décision temps réel

---

### 3️⃣ Interprétation métier (vérité)

* **Binary sensors stateless** (un par zone) :

  * `binary_sensor.simulation_presence_plage_allumage_parents`
  * `binary_sensor.simulation_presence_plage_allumage_garage`
  * `binary_sensor.simulation_presence_plage_allumage_entree`

Vérité métier :

> ON si ∃ horaire HH:MM tel que :
> `today_at(HH:MM) ≤ now < today_at(HH:MM) + durée_cycle`

* Durée du cycle :

  * Déterministe sur la journée
  * Bornée strictement par `[durée_min ; durée_max]`

Ces capteurs sont **la seule vérité consommable** par les actions.

---

### 4️⃣ Autorisation d'exécution

Les conditions d'autorisation sont agrégées dans :

* `binary_sensor.simulation_presence_autorisee`

Ce capteur est **ON** si et seulement si :

* `input_boolean.test_simulation_presence == on`
  **OU**
* `binary_sensor.vacances_actives == on`
  **ET** `input_boolean.activation_simulation_presence_vacances == on`

Les automations de matérialisation consomment exclusivement ce capteur agrégat.
En dehors de ces contextes, **aucune matérialisation n'est autorisée**.

Helpers d'autorisation :

* `input_boolean.test_simulation_presence`
* `input_boolean.activation_simulation_presence_vacances`

---

### 5️⃣ Matérialisation physique (action)

* **Automations réactives pures** (une par zone) :

  * `chambre_parents` : pilotage direct de `switch.prise_lampe_parents`
  * `garage` : pilotage indirect via `script.garage_toggle`
  * `entree` : pilotage de l'équipement d'entrée

Caractéristiques :

* Aucune logique horaire
* Aucune décision
* Réaction stricte à la vérité métier (`binary_sensor.simulation_presence_plage_allumage_<zone>`)
* Condition d'autorisation vérifiée via `binary_sensor.simulation_presence_autorisee`
* Notifications persistantes synchronisées

---

### 6️⃣ Vigilance hors boucle (sécurité douce)

* Automation de surveillance passive :

  * Détection d'un cycle anormalement long
  * Référence : `duree_max_cycle_simulation_presence + marge`

Comportement :

* **Aucune correction automatique**
* **Notification utilisateur uniquement**
* Hors boucle de décision

---

## 🧪 Mode test

* **Helper** : `input_boolean.test_simulation_presence`

Rôle :

* Autoriser la simulation hors absence réelle
* Permettre :

  * validation fonctionnelle
  * diagnostic
  * observation UI

Le mode test **n'altère pas** la logique métier.

---

## 🚫 Ce que la simulation de présence ne fait PAS

* Ne simule pas une présence réelle
* Ne remplace pas les capteurs de présence
* Ne pilote aucun autre domaine (chauffage, alarme, VMC, etc.)
* Ne corrige jamais un état anormal
* Ne prend aucune décision implicite

---

## 📌 Statut

* **Système complet et clos**
* **Contractualisé Arsenal v12.x** — révisé sur base runtime 2026.5
* **Aucune dépendance externe non maîtrisée**

Toute évolution future devra :

* respecter ce contrat,
* être explicitement documentée,
* ne jamais introduire de logique implicite.

# ==========================================================