# 🏗️ ARCHITECTURE — CHAUFFAGE (V3 PRO)

## 🏛️ MODÈLE DE CONCEPTION
Le système de chauffage Arsenal repose sur le pattern **"Trigger - Decision - Action - Guard"**. Ce modèle garantit que la logique thermique est totalement découplée des contraintes matérielles du cloud propriétaire (ViCare). Il intègre une couche de **Gouvernance Algorithmique** (Apprentissage statistique de la Loi d'eau) pour assurer une performance énergétique et un confort durable.

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
7.  **Le Pont des Consignes (Sync Bi-directionnelle)** : Automations `chauffage_sync_consigne_...`
    * *Rôle* : Assure la cohérence HA ↔ Cloud avec protection contre les boucles d'écriture.
8.  **Les Bras (Exécution)** : Scripts `chauffage_appliquer_...`
    * *Rôle* : Gestionnaires de transactions Cloud. Assurent l'atomicité et la gestion du verrouillage système.
9.  **La Police (Garde)** : `automation.realignement_vicare_ha`
    * *Rôle* : Surveillant de souveraineté. Corrige toute dérive passive du matériel par rapport à la mémoire locale.

---

## 🔒 INVARIANTS ET PATTERNS ARCHITECTURAUX

### A. Pattern de Souveraineté Matérielle
Arsenal ne fait jamais confiance à l'état Cloud instantané. Les `input_number` et `input_select` locaux sont la seule source de vérité. Le mirroring local (`sensor..._local`) assure la continuité de service en cas de coupure API.

### B. Pattern d'Apprentissage (Segmentation Thermique)
Le système optimise la courbe de chauffe en distinguant l'origine de la dérive :
1. **Dérive par Temps Doux** ($T_{ext} \ge 10^\circ\text{C}$) : Impacte le **Parallèle**. Le système ajuste l'offset global pour caler la base de la courbe.
2. **Dérive par Temps Froid** ($T_{ext} \le 5^\circ\text{C}$) : Impacte la **Pente**. Le système ajuste l'inclinaison pour répondre à une déperdition accrue.

### C. Pattern d'Atomicité (Locking)
Le verrou `input_boolean.chauffage_application_en_cours` suspend la Garde pendant toute écriture vers le Cloud pour éviter les conflits de réalignement.

### D. Pattern de Stabilité (Le "Neutre")
L'état `Neutre` préserve la mécanique en interdisant les bascules ON/OFF inutiles tant que la température est contenue dans la zone morte de l'hystérésis.

---

## 🛠️ FLUX DE DONNÉES (DATAFLOW)

1.  **ENTRÉES** : Capteurs physiques, Sliders utilisateur, ou temps (10h00).
2.  **FILTRAGE** : Les écarts instantanés sont capturés et triés par température extérieure (**Doux** vs **Froid**).
3.  **DÉCISION** : Le Cerveau ou l'Optimiseur calcule l'état cible basé sur ces données segmentées.
4.  **ACTION** : Les scripts synchronisent le Cloud ViCare et mettent à jour la mémoire locale.
5.  **GARDE** : La Police vérifie et maintient la conformité de l'état final.

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
* **Changer de matériel** -> Couche "Bras" (Scripts d'exécution) et capteurs de mirroring uniquement.
