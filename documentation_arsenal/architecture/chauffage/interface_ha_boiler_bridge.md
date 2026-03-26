# ARSENAL — Contrat d'intégration Home Assistant

## Interface HA ↔ Boiler Bridge (MQTT)

| Champ | Valeur |
|---|---|
| **Version** | v1 |
| **Statut** | Normatif |
| **Portée** | Implémentation Home Assistant du bus MQTT chaudière |

---

## 1. Objet

Ce document définit la manière dont **Home Assistant intègre le bus MQTT chaudière** décrit dans le *Contrat de bus MQTT chaudière*.

Il ne redéfinit **pas** :

- les topics MQTT
- les payloads
- les règles protocolaires

Ces éléments sont considérés comme **source de vérité externe**.

---

## 2. Principe fondamental

Home Assistant est un **adaptateur du bus MQTT**, pas un acteur du protocole.

Il **fait** :

- consomme les topics MQTT
- expose des entités
- corrèle les transactions
- produit des états exploitables

Il **ne fait pas** :

- modifier le protocole
- interpréter la logique chaudière
- reconstruire un état métier

```
MQTT (vérité)
   ↓
Sensors HA (transport)
   ↓
Templates (extraction / corrélation)
   ↓
Arsenal (logique métier)
```

---

## 3. Découpage de l'interface

L'intégration HA est structurée en **5 blocs strictement séparés**.

---

### 3.1 Santé passerelle — brute

Mapping direct MQTT → HA, sans transformation.

| Topic |
|---|
| `boiler/bridge/online` |
| `boiler/bridge/version` |
| `boiler/bridge/vcontrold_status` |
| `boiler/bridge/optolink_status` |
| `boiler/bridge/heartbeat` |

---

### 3.2 Santé passerelle — dérivée

Traitements HA :

- extraction `ts` depuis heartbeat
- détection de dégradation (> 60 s)
- synthèse globale

Entités typiques :

```
sensor.boiler_bridge_heartbeat_timestamp
binary_sensor.boiler_bridge_degraded
sensor.boiler_bridge_sante
```

---

### 3.3 Télémétrie chaudière

Mapping direct des valeurs techniques :

- températures
- consignes
- courbe de chauffe
- état et modulation brûleur

> ⚠️ **Invariant** — Le bridge expose uniquement des valeurs techniques.  
> Toute sémantique (Confort / Eco / programme) appartient à Arsenal.

---

### 3.4 Transactions (ACK)

Chaque commande suit un modèle transactionnel strict.

#### Étapes

1. HA génère un `request_id`
2. HA publie une commande MQTT
3. HA stocke le `request_id` dans un helper
4. Le bridge publie un ACK JSON
5. HA reçoit l'ACK
6. HA corrèle avec le `request_id`
7. HA produit un résultat

#### Familles transactionnelles

| Famille |
|---|
| `heating/set_temperature` |
| `heating/set_curve_slope` |
| `heating/set_curve_shift` |
| `dhw/set_setpoint` |

#### Chaîne de traitement HA

```
ACK MQTT (JSON)
   ↓
sensor.*_raw
   ↓
sensor.*_status / reason
   ↓
sensor.*_request_id / ts
   ↓
corrélation
   ↓
sensor.*_result
```

#### Règle de succès (normative)

Une commande est réussie **uniquement si** :

```
request_id ACK == request_id courant
ET
status == applied
```

#### Statuts ACK

| Statut | Signification |
|---|---|
| `accepted` | Réception technique |
| `applied` | **Succès réel** |
| `rejected` | Rejet bridge |
| `timeout` | Délai dépassé |

> ⚠️ `accepted` n'est **jamais** un succès métier.

---

### 3.5 Erreurs

Le bridge publie sur `boiler/error/last`.

HA extrait :

- `reason`
- `domain`
- `action`
- `request_id`
- `ts`

HA qualifie ensuite : erreur récente (< 24 h).

---

## 4. Séparation des couches

| Couche | Rôle |
|---|---|
| MQTT | Vérité protocolaire |
| Sensors raw | Transport |
| Templates diagnostic | Extraction |
| Templates transaction | Corrélation |
| Arsenal | Décision métier |
| UI | Affichage |

---

## 5. Invariants architecturaux

### 5.1 Source de vérité

> Le protocole MQTT est la seule source de vérité.

### 5.2 Absence de logique métier dans HA

Les templates HA :

- n'inventent pas de valeur
- ne corrigent pas le bridge
- ne simulent pas d'état

### 5.3 Corrélation obligatoire

> Un ACK sans correspondance de `request_id` n'a aucune valeur transactionnelle.

### 5.4 Non-reconstruction

Home Assistant ne doit jamais :

- reconstruire un programme chauffage
- inférer confort / réduit depuis la chaudière
- déduire une consigne absente

### 5.5 Idempotence transactionnelle

> Deux commandes avec le même `request_id` sont considérées identiques par le système.

---

## 6. Position dans l'architecture Arsenal

```
Chaudière
   ↓
Boiler Bridge (exécution)
   ↓
MQTT (contrat)
   ↓
Home Assistant (adaptation + corrélation)
   ↓
Arsenal (décision)
```

---

## 7. Périmètre exclu

Ce document ne couvre pas :

- la logique chauffage Arsenal
- les seuils thermiques
- les automatisations
- la UI
- les registres vcontrold

---

## 8. Conclusion

Home Assistant agit comme un **adaptateur déterministe du bus MQTT chaudière**.

Il garantit :

- une exposition fidèle des données
- une corrélation transactionnelle robuste
- une séparation stricte entre protocole et métier

> Toute divergence entre HA et le contrat MQTT constitue une anomalie.
