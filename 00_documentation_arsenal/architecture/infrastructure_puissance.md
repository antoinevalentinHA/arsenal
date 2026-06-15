# ⚡ ARCHITECTURE — INFRASTRUCTURE & ÉNERGIE

## 🎯 STRATÉGIE DE DISPONIBILITÉ (UPTIME)
Le système Arsenal est conçu pour maintenir sa gouvernance thermique même en cas de défaillance du réseau électrique public. La continuité de service est assurée par une segmentation de l'alimentation de secours.

### 🔋 1. Cœur du Système (Brain & Network)
**Équipements** : NAS (Stockage), Serveur HA (Intelligence), Box Internet/Switch (Communication).
- **Protection** : Onduleur (UPS).
- **Rôle** : Garantir l'intégrité de la base de données, éviter les corruptions de fichiers lors des reboots brutaux et maintenir le réseau local (LAN) actif.

### 🔥 2. Terminaux de Chauffe (Hardware)
**Équipements** : Chaudière Viessmann, Boîtier Vitoconnect.
- **Protection** : Batteries de secours dédiées.
- **Rôle** : Permettre l'exécution physique de la chauffe et le maintien de la liaison avec le Cloud/HA, même si le disjoncteur général est déclenché.

### 🛰️ 3. Souveraineté en mode Dégradé
Cette architecture électrique permet à Arsenal de :
1. **Notifier** l'utilisateur d'une coupure de courant.
2. **Maintenir** le script de décision en vie pour arbitrer la dépense de secours **par réservoir**, et non selon une « sobriété batterie » globale :
   - **Rail UPS (compute/réseau/données)** — *sobriété critique* : ne rien gaspiller, arrêt propre sous seuil. Aucune charge thermique ne le touche.
   - **Rail Bluetti (chaîne thermique)** — réserve **à dépenser utilement**, bornée par le SOC : autoriser le **stockage thermique utile** (ECS haute / désinfection = eau chaude stockée + hygiène) ; **suspendre le confort d'ambiance inutile** (été, absence, SOC bas) qui, lui, ne stocke rien.
3. **Assurer** la reprise immédiate sans cycle de "re-découverte" des entités au retour du courant.

> Doctrine : les deux réservoirs ont des finalités opposées. Dépenser le Bluetti en eau chaude est un **usage** (stockage thermique), pas un gaspillage ; le poste réellement sacrifiable est le **confort d'ambiance**. Réf. audit : [`audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md`](../audits/01_rapports/pannes/audit_actions_mode_panne_secteur.md).

---

## 🛠️ MAINTENANCE & MONITORING
L'état de l'onduleur et des batteries est intégré à Arsenal :
- **Entité** : `sensor.ups_status` / `binary_sensor.on_battery`.
- **Action de sécurité** : Si la batterie de l'onduleur passe sous 20%, Arsenal ordonne l'arrêt propre (Graceful Shutdown) du NAS et de HA pour protéger les données.

---

## ⚠️ LIMITES
Le système protège contre les coupures de courte et moyenne durée. En cas de coupure prolongée (> 4h), la priorité est donnée à la protection des données (extinction logicielle) plutôt qu'au maintien de la température.
