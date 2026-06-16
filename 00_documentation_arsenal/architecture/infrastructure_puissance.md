# ⚡ ARCHITECTURE — INFRASTRUCTURE & ÉNERGIE

## 🎯 STRATÉGIE DE DISPONIBILITÉ (UPTIME)
Le système Arsenal est conçu pour maintenir sa gouvernance thermique même en cas de défaillance du réseau électrique public. La continuité de service est assurée par une segmentation de l'alimentation de secours.

### 🔋 1. Cœur du Système (Brain & Network)
**Équipements** : NAS (Stockage), Serveur HA (Intelligence), Box Internet/Switch (Communication).
- **Protection** : Onduleur (UPS).
- **Rôle** : Garantir l'intégrité de la base de données, éviter les corruptions de fichiers lors des reboots brutaux et maintenir le réseau local (LAN) actif.

### 🔥 2. Terminaux de Chauffe (Hardware)
**Équipements** : Chaudière **gaz** Viessmann (électronique de commande), Boîtier Vitoconnect, boiler bridge.
- **Protection** : **Bluetti** (rail thermique).
- **Rôle** : Alimenter l'**électronique de commande** de la chaudière et la liaison Cloud/HA, même disjoncteur général déclenché. La **chaleur provient du gaz** : le Bluetti ne chauffe pas l'eau, il maintient la chaîne de commande active.

### 🛰️ 3. Souveraineté en mode Dégradé
Cette architecture électrique permet à Arsenal de :
1. **Notifier** l'utilisateur d'une coupure de courant.
2. **Maintenir** le script de décision en vie pour arbitrer la dépense de secours **par réservoir**, et non selon une « sobriété batterie » globale :
   - **Rail UPS (compute/réseau/données)** — *sobriété critique* : ne rien gaspiller, arrêt propre sous seuil. Aucune charge thermique ne le touche.
   - **Rail Bluetti (chaîne thermique)** — réserve **à dépenser utilement**, bornée par le SOC : autoriser le **stockage thermique utile** (ECS haute / désinfection = eau chaude stockée + hygiène) ; **suspendre le confort d'ambiance inutile** (été, absence, SOC bas) qui, lui, ne stocke rien.
3. **Assurer** la reprise immédiate sans cycle de "re-découverte" des entités au retour du courant.

> Doctrine : les deux réservoirs ont des finalités opposées. Dépenser le Bluetti en eau chaude est un **usage** (stockage thermique), pas un gaspillage ; le poste réellement sacrifiable est le **confort d'ambiance**. Réf. audit : [`audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md`](../audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md).

---

## 🔌 TOPOLOGIE D'ALIMENTATION DES PRISES COMMANDABLES

Les prises pilotables exposées sur le dashboard Prises n'ont pas toutes la même dépendance électrique. Cette topologie détermine leur **commandabilité pendant une panne secteur globale** (cf. doctrine [`03_doctrines/commandabilite.md`](03_doctrines/commandabilite.md)) : une prise alimentée en secteur direct devient **physiquement non commandable** dès la perte du secteur, tandis qu'une prise secourue (rail UPS) reste commandable. **Cette table est la source de vérité de cette topologie ; l'UI (`prise_secteur_template`) en est une conséquence, pas la source.**

### Prises secteur direct (mains-dépendantes — gate de commandabilité appliqué)

Alimentées directement par le secteur, **sans secours UPS ni Bluetti**. Pendant une panne secteur globale (`binary_sensor.panne_secteur_en_cours` à `on`), elles perdent leur alimentation : l'action est impossible et l'UI la neutralise via `prise_secteur_template`.

| Entité | Équipement alimenté | Topologie | Secourue ? | Comportement en panne secteur | Conséquence commandabilité UI | Statut / preuve |
|---|---|---|---|---|---|---|
| `switch.prise_chambre_arnaud` | Station Netatmo (Arnaud) | Secteur direct | Non | Perte d'alimentation ; entité peut rester `on`/`off` transitoirement (latence z2m) | Gatée (`prise_secteur_template`) | Mains prouvé — reboot automatique déjà gaté panne |
| `switch.prise_chambre_matthieu` | Station Netatmo (Matthieu) | Secteur direct | Non | Perte d'alimentation ; latence z2m | Gatée | Mains prouvé — reboot automatique déjà gaté panne |
| `switch.prise_bouclage` | Pompe de bouclage ECS | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_deshumidificateur` | Déshumidificateur | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_palier` | Bridge iDiamant (volets) | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_lampe_sejour` | Lumière séjour | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_sejour_baies_vitrees` | Lumière (baies vitrées) | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_lampe_parents` | Lampe chambre parents | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_jardin` | Éclairage jardin | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_refrigerateur` | Réfrigérateur | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_lave_vaisselle` | Lave-vaisselle | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_buanderie` | Machines à linge | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_sdb_enfants` | SDB enfants | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_cage_escalier_rdc` | Cage d'escalier RDC | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |
| `switch.prise_sejour_placard` | Séjour placards | Secteur direct | Non | Perte d'alimentation | Gatée | Secteur direct confirmé |

### Prises exclues du gate secteur

| Entité | Équipement alimenté | Topologie | Secourue ? | Comportement en panne secteur | Conséquence commandabilité UI | Statut / preuve | Remarque |
|---|---|---|---|---|---|---|---|
| `switch.prise_box` | Box Internet / réseau | Rail UPS | Oui (UPS) | Reste alimentée | **Non** gatée — reste commandable (`prise_template`) | UPS prouvé (§1 Cœur du Système) | Le reboot box inhibé en panne relève d'une **politique** (catégorie B), pas d'une impossibilité physique — ne pas gater |
| `switch.prise_onduleur` | Onduleur (témoin secteur) | Amont UPS (non secouru) | Non | Perte d'alimentation → passe `unavailable` | Non gatée par le signal panne ; neutralisée par l'indisponibilité native (`prise_template`) | Amont UPS prouvé (contrat panne secteur, `contrats/pannes/secteur/README.md`) | Ex-témoin de détection de coupure secteur |

> **Cohérence UI ↔ topologie.** Le sous-ensemble « secteur direct » ci-dessus correspond exactement aux cartes utilisant `prise_secteur_template` ; les deux exclusions restent sur `prise_template`. Toute évolution de cette topologie doit être répercutée dans les deux : **cette table est la source, l'UI la conséquence.**

---

## 🛠️ MAINTENANCE & MONITORING
L'état de l'onduleur et des batteries est intégré à Arsenal :
- **Entité** : `sensor.ups_status` / `binary_sensor.on_battery`.
- **Action de sécurité** : Si la batterie de l'onduleur passe sous 20%, Arsenal ordonne l'arrêt propre (Graceful Shutdown) du NAS et de HA pour protéger les données.

---

## ⚠️ LIMITES
Le système protège contre les coupures de courte et moyenne durée. En cas de coupure prolongée (> 4h), la priorité est donnée à la protection des données (extinction logicielle) plutôt qu'au maintien de la température.
