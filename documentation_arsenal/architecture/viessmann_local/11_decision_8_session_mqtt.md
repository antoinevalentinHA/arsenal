# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## 11. Décision 8 — Session MQTT

```
clean_session : false
client_id     : arsenal-boiler-bridge  (stable, prévisible)
```

### Motifs

- Permettre la livraison différée des messages QoS 1 après reconnexion
- Assurer la continuité de session après redémarrage passerelle
- Garantir que les commandes publiées pendant une courte déconnexion sont délivrées

### Règle sur le client_id

La passerelle DOIT utiliser un `client_id` fixe et stable.
Un `client_id` généré aléatoirement EST INTERDIT — il produit une session propre de facto malgré `clean_session: false`.

### Conséquence sur la déduplication

Avec `clean_session: false`, le broker peut rejouer des messages QoS 1 en file au reconnect. La passerelle DOIT donc traiter tout message rejoué par le broker via la déduplication `request_id` (décision 6).

### Règle sur l'accumulation de file

Si la passerelle est hors ligne durablement,
le broker accumule les messages QoS 1 non délivrés.

À la reconnexion, ces messages peuvent être rejoués
en rafale.

La passerelle DOIT vérifier le champ `expires_at`
avant toute tentative d'exécution de la commande.

Une commande expirée DOIT être rejetée
avec `reason: expired`.

La politique d'expiration métier est définie dans la décision 9
(12_decision_9_expiration_metier.md).