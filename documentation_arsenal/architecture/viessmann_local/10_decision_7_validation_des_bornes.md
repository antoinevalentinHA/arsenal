# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 10. Décision 7 — Validation des bornes

La validation des valeurs de commande est **responsabilité de la passerelle**.

La passerelle DOIT vérifier :

- le type de la valeur
- le format
- les bornes admissibles
- l'existence du paramètre ciblé

Toute commande invalide DOIT être rejetée via un ack `rejected`
avec `reason: invalid_value`.

Les bornes admissibles par paramètre DOIVENT être documentées
dans une table annexe séparée à ce contrat (non définie ici).

Arsenal PEUT implémenter un pré-filtre de validation côté HA,
mais ce pré-filtre ne dispense pas la passerelle de sa propre validation.