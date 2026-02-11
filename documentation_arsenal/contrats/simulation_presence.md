# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
# Simulation de présence
# ==========================================================

## 🎯 Finalité

La **simulation de présence** a pour objectif de **reproduire un comportement lumineux crédible** lors d’une absence réelle du foyer, afin de donner l’illusion d’une habitation occupée.

Elle est **strictement cosmétique** et ne doit **jamais** :

* compromettre la sécurité,
* perturber la logique de présence réelle,
* introduire de décisions implicites,
* piloter un équipement sans autorisation explicite.

---

## 🧠 Principes fondateurs Arsenal

* **Séparation stricte des rôles** :

  * Paramètres → Génération → Interprétation → Action → Vigilance
* **Aucune logique cachée dans l’UI**
* **Aucune action directe depuis un script de calcul**
* **Aucune dépendance temporelle implicite**
* **Tolérance totale aux redémarrages**

La simulation de présence est un **sous-système autonome**, lisible, testable et désactivable.

---

## 🧩 Architecture fonctionnelle

### 1️⃣ Paramètres métier (intention)

Helpers configurables par l’utilisateur :

* **Intensité** (nombre de cycles) :

  * `input_number.nb_cycles_simulation_presence_matin`
  * `input_number.nb_cycles_simulation_presence_soir`
  * `input_number.nb_cycles_simulation_presence_garage_matin`
  * `input_number.nb_cycles_simulation_presence_garage_soir`

* **Durées de cycle** :

  * `input_number.duree_min_cycle_simulation_presence`
  * `input_number.duree_max_cycle_simulation_presence`

* **Cadres horaires autorisés** (heure seule) :

  * `input_datetime.debut_cycle_simulation_presence_*`
  * `input_datetime.fin_cycle_simulation_presence_*`

Ces paramètres **n’entraînent aucune action directe**.

---

### 2️⃣ Génération des horaires (données)

* **Script** : `script.generer_horaires_simulation_presence`

Rôle exclusif :

* Générer **une fois par jour** des horaires pseudo-aléatoires
* Figer ces horaires dans des helpers persistants

Sorties :

* `input_text.horaires_simulation_presence_matin`
* `input_text.horaires_simulation_presence_soir`
* `input_text.horaires_simulation_presence_garage_matin`
* `input_text.horaires_simulation_presence_garage_soir`

Caractéristiques :

* Non déterministe (volontaire)
* Sans action matérielle
* Sans décision temps réel

---

### 3️⃣ Interprétation métier (vérité)

* **Binary sensors stateless** :

  * `binary_sensor.simulation_presence_plage_allumage_parents`
  * `binary_sensor.simulation_presence_plage_allumage_garage`

Vérité métier :

> ON si ∃ horaire HH:MM tel que :
> `today_at(HH:MM) ≤ now < today_at(HH:MM) + durée_cycle`

* Durée du cycle :

  * Déterministe sur la journée
  * Bornée strictement par `[durée_min ; durée_max]`

Ces capteurs sont **la seule vérité consommable** par les actions.

---

### 4️⃣ Autorisation d’exécution

La simulation de présence **n’est autorisée** que si :

* `input_select.mode_maison == "Vacances"`
  **OU**
* `input_boolean.test_simulation_presence == on`

En dehors de ces contextes, **aucune matérialisation n’est autorisée**.

---

### 5️⃣ Matérialisation physique (action)

* **Automations réactives pures** :

  * Parents : pilotage direct de `switch.prise_lampe_parents`
  * Garage : pilotage indirect via `script.garage_toggle`

Caractéristiques :

* Aucune logique horaire
* Aucune décision
* Réaction stricte à la vérité métier
* Notifications persistantes synchronisées

---

### 6️⃣ Vigilance hors boucle (sécurité douce)

* Automation de surveillance passive :

  * Détection d’un cycle anormalement long
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

Le mode test **n’altère pas** la logique métier.

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
* **Contractualisé Arsenal v7.x**
* **Aucune dépendance externe non maîtrisée**

Toute évolution future devra :

* respecter ce contrat,
* être explicitement documentée,
* ne jamais introduire de logique implicite.

# ==========================================================
