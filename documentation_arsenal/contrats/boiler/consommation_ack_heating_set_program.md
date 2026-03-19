# Contrat HA — Consommation ACK `heating/set_program`

**Domaine** : Chauffage / Arsenal  
**Version** : v1.1  
**Date** : 18/03/2026  
**Statut** : normatif  
**Portée** : couche observation Arsenal — consommation MQTT ACK

---

## 1. Objectif

Permettre à Home Assistant de conclure de façon déterministe sur le résultat d'une commande `set_program` envoyée à la passerelle chaudière.

Règle fondamentale :

> Le succès d'une commande `set_program` est établi **uniquement** par la réception d'un ACK `applied` corrélé au `request_id` de la commande émise.  
> Aucun autre état HA ne constitue une preuve de succès.

---

## 2. Source brute

| Entité | Type | Topic MQTT |
|--------|------|------------|
| `sensor.boiler_ack_heating_set_program_raw` | MQTT sensor | `boiler/ack/heating/set_program` |

Cette entité expose le payload JSON complet en état brut. Elle est la source unique de vérité pour ce contrat.

---

## 3. Inventaire des entités

Le socle transactionnel pour `set_program` comprend **7 entités**.

### 3.1 Helper de référence transactionnelle

| Entité | Type | Rôle |
|--------|------|------|
| `input_text.boiler_req_heating_set_program` | `input_text` | Stocker le `request_id` de la commande en cours |

Comportement :

- Écrit par le script immédiatement avant `mqtt.publish`
- Sert d'ancre de corrélation pour tous les sensors dérivés
- Persistant au redémarrage HA
- Réinitialisé à vide sur **tous** les chemins de sortie du script : succès (`applied`), échec (`rejected`, `timeout`), et abandon sur dépassement de timeout interne
- La remise à vide doit être placée dans un bloc de libération final systématique — jamais conditionnelle
- Un `input_text` non réinitialisé après une transaction interrompue constitue un faux contexte transactionnel persistant

### 3.2 Sensors d'extraction ACK

Tous dérivés de `sensor.boiler_ack_heating_set_program_raw`.

| Entité | Champ extrait | Valeur si absent / invalide |
|--------|--------------|----------------------------|
| `sensor.boiler_ack_heating_set_program_request_id` | `request_id` | `unknown` |
| `sensor.boiler_ack_heating_set_program_status` | `status` | `unknown` |
| `sensor.boiler_ack_heating_set_program_reason` | `reason` | `none` |
| `sensor.boiler_ack_heating_set_program_ts` | `ts` | `unknown` |

Règle commune : si le raw est `unknown`, `unavailable`, vide, ou ne commence pas par `{`, tous les sensors d'extraction retournent leur valeur de repli respective.

### 3.3 Sensor de corrélation

| Entité | Type | Rôle |
|--------|------|------|
| `sensor.boiler_ack_heating_set_program_correlation` | template sensor | Comparer l'ACK reçu avec la transaction en cours |

Valeurs normatives :

| Valeur | Condition |
|--------|-----------|
| `match` | `ack.request_id == input_text.boiler_req_heating_set_program` — les deux non vides, égalité stricte |
| `mismatch` | Les deux présents et non vides, mais différents |
| `inconnu` | Raw invalide, `request_id` absent, ou `input_text` vide |

### 3.4 Sensor de conclusion transactionnelle

| Entité | Type | Rôle |
|--------|------|------|
| `sensor.boiler_ack_heating_set_program_result` | template sensor | Exposer la conclusion exploitable par le script |

Valeurs normatives :

| Valeur | Condition |
|--------|-----------|
| `applied` | `correlation = match` ET `status = applied` |
| `rejected` | `correlation = match` ET `status = rejected` |
| `timeout` | `correlation = match` ET `status = timeout` |
| `pending` | `correlation ≠ match` OU `status = accepted` |
| `inconnu` | Raw invalide ou absent |

Distinction `pending` / `inconnu` :

- `pending` : état transitoire indifférencié — regroupe délibérément "ACK non encore reçu" et "ACK d'une transaction précédente". Le script n'a pas besoin de distinguer ces deux cas : dans les deux situations, il attend ou il timeout. Ce caractère fourre-tout est assumé.
- `inconnu` : raw illisible ou helper vide — état anormal, potentiellement signalable

---

## 4. Séquence d'utilisation par le script

```
1. Générer request_id
2. Écrire dans input_text.boiler_req_heating_set_program
3. Publier mqtt.publish sur boiler/command/heating/set_program
4. Attendre sensor.boiler_ack_heating_set_program_result
5. Succès seulement si result = applied
6. Écrire input_select.chauffage_dernier_mode_decide = comfort
7. Remettre input_text.boiler_req_heating_set_program à vide
```

Le script NE DOIT PAS lire `sensor.boiler_ack_heating_set_program_status` directement comme preuve de succès.  
Le script NE DOIT PAS lire `sensor.programme_chauffage` comme preuve de succès.

---

## 5. Ce que ce contrat ne couvre pas (dettes explicites)

| Dette | Description |
|-------|-------------|
| Freshness TTL | Absence de validation temporelle sur `ts` — un ACK ancien corrélé sera accepté si le `request_id` correspond |
| Watchdog | Pas de détection automatique d'un `input_text` périmé après redémarrage HA |
| Retries | La politique de retry en cas de `rejected` ou `timeout` est déléguée au script appelant |

---

## 6. Relation avec le contrat de bus MQTT chaudière

Ce contrat est subordonné au contrat de bus MQTT Arsenal v1.  
Les quatre statuts ACK admis (`accepted`, `applied`, `rejected`, `timeout`) sont définis dans ce contrat parent.  
`accepted` n'est jamais un succès métier dans ce contrat.

---

## 7. Nommage

Les noms sont volontairement longs. Critères retenus :

- explicites sans contexte
- homogènes entre domaines
- greppables
- sans ambiguïté

L'ambiguïté a un coût supérieur à la longueur dans ce domaine.
