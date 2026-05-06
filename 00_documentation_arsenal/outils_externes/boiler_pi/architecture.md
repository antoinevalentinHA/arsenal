# ==========================================================
# 🧠 ARSENAL — CONTRAT INFRA
# Boiler Bridge — Architecture système locale
#
# 🗂️ COUCHE : Infrastructure / Exécution locale
# 🧱 TYPE : Contrat normatif
# 🔍 NIVEAU DE CONFIANCE : ÉLEVÉ — PRODUCTION
# 📅 VERSION : v1.1 (post-remédiation, contrat opposable)
# ==========================================================

## 🎯 OBJET

Définir le **modèle architectural officiel** du Boiler Bridge local :

* structure des fichiers
* séparation source / runtime
* gestion des services systemd
* stratégie de configuration
* mécanisme de déploiement
* périmètre de sauvegarde
* frontière d'autorité

Ce document est **opposable** et fait référence pour toute évolution.

---

## 🧭 FRONTIÈRE D'AUTORITÉ

* Le **repo** définit la vérité.
* Le **Pi exécute**, il ne décide pas de sa configuration.
* `deploy.sh` est le seul mécanisme autorisé pour aligner runtime et source.

👉 Toute dérive runtime est considérée comme une anomalie.

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
/home/pi/boiler-bridge/systemd/
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
* configuration d'exécution

👉 **Single Source of Truth**
👉 Aucun duplicat autorisé

---

### 4. Runtime systemd (état appliqué)

```
/etc/systemd/system/
```

Contient :

* services actifs (`boiler_bridge.service`, `boiler-guard.service`)
* timers (`boiler-guard.timer`)

⚠️ Les overrides (`.service.d/`) sont **interdits** en régime nominal.

👉 **État réel du système**
👉 Doit être strictement conforme à la source versionnée
👉 Doit être sauvegardé

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

## ⚙️ DÉPLOIEMENT (mécanisme officiel)

### Script canonique

```
/home/pi/boiler-bridge/deploy.sh
```

### Rôle

* synchroniser le dépôt (`git fetch` + `reset --hard`)
* vérifier l'intégrité du code (Python + Bash)
* déployer les unités systemd depuis le repo
* recharger systemd (`daemon-reload`)
* redémarrer les services
* appliquer les invariants Arsenal

### Invariants appliqués

Le script `deploy.sh` bloque le déploiement si :

* un override systemd est présent (`.service.d/`)
* une référence `/etc/arsenal` est détectée dans les unités runtime

👉 `deploy.sh` est le **point d'entrée unique de déploiement**.
👉 Toute modification manuelle du runtime est interdite.

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
  * variables hardcodées dans les unités systemd
  * divergence entre services

---

## 💾 STRATÉGIE DE BACKUP

### Périmètre obligatoire

#### Source

```
/home/pi/boiler-bridge/
/home/pi/boiler-bridge/systemd/
/home/pi/boiler-bridge/backup_boiler_bridge.sh
/home/pi/boiler_bridge.env
```

#### Runtime

```
/etc/systemd/system/boiler-guard.service
/etc/systemd/system/boiler_bridge.service
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
* overrides systemd en régime nominal
* modification directe des unités runtime
* déploiement hors `deploy.sh`

---

## ✅ INVARIANTS

* toute exécution systemd pointe vers `/home/pi/boiler-bridge`
* toute configuration passe par `/home/pi/boiler_bridge.env`
* tout service actif est sauvegardé (runtime inclus)
* tout script exécuté est marqué exécutable
* le contenu de `/etc/systemd/system/boiler*` est strictement issu de `/home/pi/boiler-bridge/systemd/`
* aucune modification directe des unités runtime n'est autorisée
* aucun override `.service.d/` ne doit exister en régime nominal

---

## 🚨 ANTI-DÉRIVE

Les situations suivantes sont considérées comme des **violations du contrat** :

* présence de `.service.d/` sous `/etc/systemd/system/boiler*`
* présence de `/etc/arsenal`
* référence à `/etc/arsenal` dans une unité runtime
* modification manuelle d'une unité systemd
* divergence entre repo et runtime
* configuration en dehors de `/home/pi/boiler_bridge.env`

👉 Ces cas sont bloqués par `deploy.sh`.
👉 Toute occurrence non bloquée constitue un défaut du contrat à corriger.

---

## 🧾 VERDICT

Le Boiler Bridge est désormais :

* déterministe
* reproductible
* observable
* restaurable
* protégé contre la dérive

👉 conforme aux exigences Arsenal niveau production.

# ==========================================================
