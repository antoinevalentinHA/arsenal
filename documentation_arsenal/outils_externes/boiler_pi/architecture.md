# ==========================================================

# 🧠 ARSENAL — CONTRAT INFRA

# Boiler Bridge — Architecture système locale

#

# 🗂️ COUCHE : Infrastructure / Exécution locale

# 🧱 TYPE : Contrat normatif

# 🔍 NIVEAU DE CONFIANCE : ÉLEVÉ — PRODUCTION

# ==========================================================

## 🎯 OBJET

Définir le **modèle architectural officiel** du Boiler Bridge local :

* structure des fichiers
* séparation source / runtime
* gestion des services systemd
* stratégie de configuration
* périmètre de sauvegarde

Ce document est **opposable** et fait référence pour toute évolution.

---

## 🧱 ARCHITECTURE GLOBALE

### 1. Source versionnée (vérité)

```
/home/pi/boiler-bridge/
```

Contient :

* code Python (`boiler_mqtt.py`)
* scripts associés
* logique métier

👉 **Seule source de vérité fonctionnelle**

---

### 2. Infrastructure déclarative (versionnée)

```
/home/pi/systemd/
```

Contient :

* unités systemd de référence
* version contrôlée des services

👉 **Source de vérité infrastructurelle**

---

### 3. Configuration runtime (unique)

```
/home/pi/boiler_bridge.env
```

Contient :

* variables MQTT (`ARSENAL_MQTT_*`)
* configuration d’exécution

👉 **Single Source of Truth**
👉 Aucun duplicat autorisé

---

### 4. Runtime systemd (état appliqué)

```
/etc/systemd/system/
```

Contient :

* services actifs (`boiler_bridge.service`, `boiler-guard.service`)
* overrides (`.service.d/`)
* timers

👉 **État réel du système**
👉 Peut diverger → doit être sauvegardé

---

## ⚙️ SERVICES

### Boiler Bridge

* Service : `boiler_bridge.service`
* Rôle :

  * interface MQTT ↔ chaudière
  * exécution transactionnelle
* Dépend de :

  * `/home/pi/boiler-bridge/boiler_mqtt.py`
  * `/home/pi/boiler_bridge.env`

---

### Boiler Guard

* Service : `boiler-guard.service`

* Rôle :

  * supervision locale
  * détection état stale
  * escalade

* Script :

```
/home/pi/boiler-bridge/boiler_guard.sh
```

---

## 🔐 CONFIGURATION

### Règles

* une seule source :

```
/home/pi/boiler_bridge.env
```

* interdit :

  * duplication dans `/etc/arsenal`
  * variables hardcodées dans les scripts
  * divergence entre services

---

## 💾 STRATÉGIE DE BACKUP

### Périmètre obligatoire

#### Source

```
/home/pi/boiler-bridge/
/home/pi/systemd/
/home/pi/boiler_bridge.env
/home/pi/backup_boiler_bridge.sh
```

#### Runtime

```
/etc/systemd/system/boiler-guard.service*
/etc/systemd/system/boiler_bridge.service*
/etc/systemd/system/boiler-guard.timer
```

---

### Objectif

Garantir une restauration :

* **sans perte**
* **sans hypothèse implicite**
* **sans reconstruction manuelle**

---

## 🚫 INTERDITS

* utiliser `/etc/arsenal` comme source active
* dépendre uniquement du repo sans runtime
* backup partiel (code seul)
* duplication des fichiers `.env`
* scripts non exécutables
* divergence source / runtime non documentée

---

## ✅ INVARIANTS

* toute exécution systemd pointe vers `/home/pi/boiler-bridge`
* toute configuration passe par `/home/pi/boiler_bridge.env`
* tout service actif est sauvegardé (runtime inclus)
* tout script exécuté est marqué exécutable

---

## 🧾 VERDICT

Le Boiler Bridge est désormais :

* déterministe
* reproductible
* observable
* restaurable

👉 conforme aux exigences Arsenal niveau production

# ==========================================================
