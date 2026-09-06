# 🧠 ARSENAL — CONTRAT INFRA · Boiler Bridge — Architecture système locale · 🗂️ COUCHE : Infrastructure / Exécution locale · 🧱 TYPE : Contrat normatif · 🔍 NIVEAU DE CONFIANCE : GUARD EN PRODUCTION, BRIDGE HISTORIQUE · 📅 VERSION : v1.1 (post-remédiation, contrat opposable — décrit le régime historique du service de pont)

## 📌 STATUT DE PRODUCTION (convergence C48, 2026-09-06)

* **Boiler Bridge** (`boiler_bridge.service`) : **historique, `disabled`/`inactive`**. Remplacé par **Boilerack**, écrivain souverain actif du bus MQTT chaudière (topics `boilerack/*`). Le présent document décrit l'architecture du **prédécesseur** ; il ne décrit plus le runtime de production pour la fonction d'écriture chaudière.
* **Boiler Guard** (`boiler-guard.service` / `.timer`) : reste **actif**, en **v1.3**, hébergé dans ce même dépôt `boiler-bridge`. Sa cible par défaut est désormais `boilerack.service` — voir [`guard.md`](guard.md) §7. Composant de **supervision externe**, distinct de la garde fonctionnelle HA composée (`contrats/chauffage/30_decision_centrale__amendement_garde_execution.md`, hors périmètre de cette mise à jour documentaire).
* **Topologie réelle actuelle** :

  ```
  Arsenal / Home Assistant
        │  MQTT (topics boilerack/*)
        ▼
  Boilerack (écrivain souverain, service actif)
        │  vcontrold / Optolink
        ▼
  Chaudière Viessmann
  ```

  Le guard (ce dépôt) supervise localement le Pi et sa mission, **indépendamment** de ce chemin MQTT (il n'interagit pas avec les topics boiler — voir [`guard.md`](guard.md) §1) — voir la section « Services » ci-dessous pour la topologie interne historique du bridge.
* Pour l'état de production détaillé côté Boilerack : dépôt public **Boilerack**
  (README, `docs/design/README.md`, `docs/operations.md`) et
  [`architecture/ecosysteme_depots_satellites.md`](../../architecture/ecosysteme_depots_satellites.md) §4.6.

---

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

### Boiler Bridge — **historique, désactivé**

* Service : `boiler_bridge.service` — **`disabled`/`inactive`** depuis la migration vers Boilerack (cf. statut en tête de document).
* Rôle (historique) :
  * interface MQTT ↔ chaudière
  * exécution transactionnelle
* Dépendait de :
  * `/home/pi/boiler-bridge/boiler_mqtt.py`
  * `/home/pi/boiler_bridge.env`
* **Fonction reprise par Boilerack** (`boilerack.service`, `enabled`/`active`), hors dépôt `boiler-bridge`.

---

### Boiler Guard — **actif, v1.3**

* Service : `boiler-guard.service`
* Rôle :
  * supervision locale
  * détection état stale
  * escalade
* Script :

```
/home/pi/boiler-bridge/boiler_guard.sh
```

* **Cible protégée par défaut : `boilerack.service`** (retargetée depuis `boiler_bridge.service` lors du Lot 1 guard/systemd — audité, mergé, déployé, validé terrain). Détail des axes d'évaluation et limites : [`guard.md`](guard.md).

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

Le Boiler Bridge **était** :

* déterministe
* reproductible
* observable
* restaurable
* protégé contre la dérive

👉 conforme aux exigences Arsenal niveau production — **pour le régime historique** qu'il décrit. Ce verdict ne s'applique plus à la fonction d'écriture chaudière, aujourd'hui assurée par Boilerack (statut en tête de document). Il reste valable pour le **guard**, toujours hébergé et déployé depuis ce dépôt.

# ==========================================================
