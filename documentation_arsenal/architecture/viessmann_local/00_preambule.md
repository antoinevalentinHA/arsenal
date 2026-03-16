# Arsenal — Contrat de bus MQTT chaudière

**Interface Arsenal ↔ passerelle chaudière (Optolink / KM-Bus)**
Version : v1
Date : 13/03/2026
Statut : normatif
Portée : locale (LAN uniquement)

---

## Préambule

Ce document définit le bus MQTT utilisé pour la communication entre Arsenal et la passerelle chaudière locale.

Il ne décrit ni :
- la logique métier chauffage
- la logique interne vcontrold
- les registres Optolink
- les automatismes Home Assistant

Ces éléments sont documentés séparément.

Il encadre exclusivement :
- la télémétrie chaudière
- les commandes Arsenal vers la passerelle
- la validation et l'exécution des commandes
- les acquittements d'exécution
- la santé technique de la passerelle

> La chaudière n'est pas exposée directement à Arsenal.
> Arsenal dialogue avec une passerelle locale via ce bus MQTT contractuel.

---

## Définitions

Arsenal
    Système d'automatisation domestique pilotant la logique métier chauffage.

Passerelle chaudière
    Processus logiciel connecté au bus KM-Bus via interface Optolink,
    exposant l'API chaudière sur MQTT.

Bus MQTT chaudière
    Ensemble des topics et règles de communication MQTT définis par ce contrat.

Commande
    Message publié par Arsenal demandant une action à la passerelle.

Acquittement (ack)
    Message publié par la passerelle indiquant le résultat d'une commande.

Télémétrie
    Information publiée par la passerelle décrivant l'état de la chaudière.

Passerelle dégradée
    État dans lequel la passerelle ne publie plus de heartbeat valide dans la fenêtre contractuelle définie par ce document

request_id
    Identifiant unique (UUIDv4) attribué par Arsenal à chaque commande.
    Il sert à la traçabilité et à la déduplication des commandes.

    Deux commandes portant le même request_id sont considérées comme
    identiques par la passerelle.

Session MQTT
    Contexte de connexion maintenu par le broker et identifié par le
    client_id du client MQTT.

    Selon la valeur de clean_session, la session est soit détruite à
    la déconnexion (session propre), soit conservée pour permettre la
    livraison différée des messages QoS 1 (session persistante).

Expiration métier
    Limite de validité temporelle d'une commande, exprimée par le champ
    expires_at dans le payload.

    Une commande expirée ne DOIT PAS être exécutée par la passerelle,
    même si elle est techniquement délivrable par le broker MQTT.