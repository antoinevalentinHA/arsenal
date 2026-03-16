# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 1. Périmètre

### Inclus dans ce contrat

- publication de télémétrie chaudière
- publication d'état de santé passerelle
- réception de commandes Arsenal
- validation des commandes
- publication d'acquittements d'exécution
- publication d'erreurs d'exécution

### Exclus de ce contrat

- logique de décision chauffage Arsenal
- stratégie ECS
- UI Lovelace
- représentation métier dérivée (template sensors)
- gouvernance des helpers HA
- protocole KM-Bus et registres chaudière