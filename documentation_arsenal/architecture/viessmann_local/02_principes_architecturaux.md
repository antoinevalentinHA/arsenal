# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 2. Principes architecturaux

**2.1 Séparation des rôles**

- Arsenal **décide et émet les commandes**
- La passerelle **lit l'état chaudière, exécute les commandes et publie les acquittements**
- La chaudière **agit comme équipement piloté**

**2.2 Transport agnostique métier**

MQTT transporte des faits, des ordres et des acquittements.
Le bus MQTT NE DOIT PAS porter de logique métier.

**2.3 Symétrie contrôlée**

Les topics de commande ne sont pas la copie des topics de télémétrie.
Lecture et écriture appartiennent à des domaines distincts.

Un topic de télémétrie ne DOIT PAS être utilisé pour publier une commande.

**2.4 Local-first**

Le fonctionnement du bus MQTT ne dépend pas d'un service cloud tiers.

Le contrat suppose un fonctionnement purement local, indépendant du cloud constructeur.

**2.5 Observabilité native**

Tout ordre important DOIT être traçable, acquittable et diagnosticable
via le bus MQTT.

**2.6 Idempotence contrôlée**

Les commandes DOIVENT pouvoir être rejouées sans provoquer
d'exécution multiple indésirable.

La passerelle DOIT utiliser le champ `request_id`
afin de détecter et absorber les doublons.

Les commandes explicitement non idempotentes font l'objet
de règles de déduplication renforcées, définies dans la
politique de déduplication.

**2.7 Robustesse au redémarrage**

Le bus doit rester cohérent en cas de redémarrage
d'Arsenal, de la passerelle ou du broker MQTT.

Les mécanismes de déduplication, d'expiration métier
et d'acquittement garantissent cette cohérence.