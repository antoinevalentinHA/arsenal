# 🏗️ ARCHITECTURE — CHAUFFAGE (V3 PRO)

## Modèle de conception

Le système de chauffage Arsenal repose sur le pattern **Trigger → Decision → Action → Guard**.

Il garantit une séparation stricte entre :
- perception des états ;
- décision thermique ;
- exécution matérielle ;
- validation d'exécution.

Le pilotage repose sur un modèle **local transactionnel** :
- chaque commande est émise avec un `request_id` ;
- chaque commande attend une validation explicite (ACK) ;
- aucune action n'est considérée comme réussie sans confirmation.

### 🧩 1. Segmentation des Responsabilités
L'architecture est découpée en couches fonctionnelles étanches pour garantir la résilience et la clarté du diagnostic :

1.  **Le Diapason (Mesure & Mirroring)** : `sensor.ecart_consigne_...`
    * *Rôle* : Mesure de la tension thermique. Utilise des miroirs locaux (`sensor..._local`) pour calculer l'écart en temps réel. 
    * *Spécialisation* : Les écarts sont segmentés par conditions : 
        - **Mode Doux** ($T_{ext} \ge 10^\circ\text{C}$) : Isole les besoins de réglage du **Parallèle**.
        - **Mode Froid** ($T_{ext} \le 5^\circ\text{C}$) : Isole les besoins de réglage de la **Pente**.
2.  **La Partition (Cible)** : `sensor.chauffage_autorisation_cible`
    * *Rôle* : Traduction des faits physiques en intention ternaire (`comfort`, `reduced`, `neutre`) via une double hystérésis.
3.  **L'Expertise Statistique (Conseil)** : `sensor.chauffage_pente_suggeree` & `parallele_suggeree`
    * *Rôle* : Analyse les dérives segmentées du Diapason. Propose des ajustements de Pente (réaction au froid) ou de Parallèle (offset global par temps doux).
4.  **L'Étincelle (Trigger)** : `automation.chauffage_trigger_decision_centrale`
    * *Rôle* : Observateur de contexte. Réveille le cerveau sur changement d'état (fenêtre, poêle, présence) ou via watchdog.
5.  **Le Cerveau (Décision)** : `script.chauffage_decision_centrale`
    * *Rôle* : Arbitre souverain. Croise l'intention thermique avec les blocages métiers (Poêle, Aération).
6.  **L'Optimiseur (Loi d'eau)** : `automation.chauffage_decision_auto_ajustement_courbe`
    * *Rôle* : Instance décisionnelle quotidienne (10h00). Applique les suggestions de l'Expertise Statistique si le contexte est stable.
7.  **Le Pont des Consignes (Projection locale)** : Automations `chauffage_sync_consigne_...`
    * *Rôle* : Projette les consignes décidées vers la couche d’exécution.
    * Ne réalise aucune synchronisation externe.
8.  **Les Bras (Exécution)** : Scripts `chauffage_appliquer_...`
    * *Rôle* : Exécution transactionnelle locale via boiler bridge.
    * Chaque commande :
        - génère un `request_id`
        - est envoyée via MQTT
        - attend un ACK (`applied`, `rejected`, `timeout`)
9.  **La Police (Garde)** : mécanismes de validation
    * *Rôle* : Surveille la cohérence entre :
        - la consigne demandée
        - le résultat d’exécution (ACK)
    * Détecte les échecs d’application (timeout, mismatch, rejet)

---

## 🔒 INVARIANTS ET PATTERNS ARCHITECTURAUX

### A. Pattern de Souveraineté Matérielle
La source de vérité est locale.

- Les `input_number` et `input_select` portent les décisions.
- L’état matériel n’est validé qu’après réception d’un ACK.
- Aucun état n’est supposé appliqué sans confirmation explicite.

### B. Pattern d'Apprentissage (Segmentation Thermique)
Le système optimise la courbe de chauffe en distinguant l'origine de la dérive :
1. **Dérive par Temps Doux** ($T_{ext} \ge 10^\circ\text{C}$) : Impacte le **Parallèle**. Le système ajuste l'offset global pour caler la base de la courbe.
2. **Dérive par Temps Froid** ($T_{ext} \le 5^\circ\text{C}$) : Impacte la **Pente**. Le système ajuste l'inclinaison pour répondre à une déperdition accrue.

### C. Pattern d'Atomicité (Transaction)
Chaque commande est traitée comme une transaction :

- émission avec `request_id`
- attente d’un ACK
- absence de chevauchement via verrou logique

### D. Pattern de Stabilité (Le "Neutre")
L'état `Neutre` préserve la mécanique en interdisant les bascules ON/OFF inutiles tant que la température est contenue dans la zone morte de l'hystérésis.

---

## 🛠️ FLUX DE DONNÉES (DATAFLOW)

1.  **ENTRÉES** : Capteurs physiques, helpers, temps.
2.  **FILTRAGE** : Calcul des écarts segmentés (Doux / Froid).
3.  **DÉCISION** : Calcul de la consigne cible.
4.  **ACTION** : Envoi d’une commande transactionnelle via MQTT.
5.  **VALIDATION** : Réception d’un ACK (applied / rejected / timeout).
6.  **GARDE** : Vérification de cohérence entre intention et résultat.

---

## 🧾 OBSERVABILITÉ ET DIAGNOSTIC
Le système est une "boîte de verre" grâce à ses capteurs de transparence :
* **La Raison** (`sensor.chauffage_raison_calculee`) : Cause dominante de l'état actuel.
* **L'Intention** (`sensor.chauffage_mode_calcule`) : Vérification de la priorité logique.
* **Le Diagnostic Doux/Froid** : Visualisation des écarts segmentés pour valider la loi d'eau.
* **La Trace** (`input_text.chauffage_last_adjustment`) : Journal du dernier ajustement automatique.

---

## ⚠️ MAINTENANCE ET ÉVOLUTION
* **Modifier la règle métier** -> `contrats_arsenal/chauffage.md`.
* **Ajuster la finesse de l'analyse** -> Modifier les seuils ($\pm 0.4$ ou $\pm 0.5$) dans les capteurs de suggestion.
* **Changer de matériel** -> Couche "Bras" (scripts d’exécution + protocole MQTT) uniquement.
