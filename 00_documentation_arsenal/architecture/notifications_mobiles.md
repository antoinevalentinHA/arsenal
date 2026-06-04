# 📱 ARSENAL — ARCHITECTURE · Notifications mobiles
#
# 📌 Statut :
# Document ARCHITECTURE
# Référence technique interne Arsenal
#
# 📌 Domaine :
# Notifications — Mobile / Push
#
# 📌 Portée :
# Couche d’abstraction d’envoi de notifications
# vers les téléphones des utilisateurs.
#
# ==========================================================

## 🎯 Objet

Ce document décrit l’**architecture technique** de la couche
**Notifications mobiles** d’Arsenal.

Il formalise :

* le rôle exact des scripts fournis,
* leur position dans l’architecture globale,
* les garanties apportées,
* les usages autorisés et interdits,
* le contrat implicite entre logique métier et infrastructure.

Ce document ne définit **pas** :

* quand notifier,
* quelles notifications sont pertinentes,
* la politique d’alerting.

Il décrit uniquement la **couche d’exécution**.

---

## 🧱 Positionnement architectural

Couche concernée :

* **Infrastructure — Notifications**

Rôle :

* Fournir une **API interne unique** d’envoi de notifications
* Abstraire totalement :

  * le matériel,
  * l’application mobile,
  * le service notify réel Home Assistant

Chaîne simplifiée :

```
Logique métier
      │
      ▼
script.notification_*   (abstraction Arsenal)
      │
      ▼
service notify réel     (Home Assistant)
      │
      ▼
Téléphone utilisateur
```

Aucun code métier ne doit descendre sous ce niveau.

---

## 🧠 Principe fondamental

> **Toute notification mobile Arsenal passe EXCLUSIVEMENT
> par les scripts du fichier :**
>
> `/homeassistant/10_scripts/system/notifications_mobiles.yaml`

Conséquences directes :

* Aucun `notify.mobile_app_*` dans les automatisations métier
* Aucun service notify codé en dur
* Aucune dépendance directe à un téléphone

La notification est vue comme :

* un **service d’infrastructure**,
* interchangeable,
* totalement découplé du reste du système.

---

## 🧩 Mécanisme d’abstraction des cibles

*(Cette section est complétée par la couche de synchronisation automatique décrite plus loin.)

Les téléphones sont référencés par des helpers :

* `input_text.telephone_antoine_notify`
* `input_text.telephone_constance_notify`

Chaque helper contient **le nom du service notify réel**.

Exemples :

* `notify.mobile_app_pixel_7a`
* `notify.mobile_app_samsung_s22`

Avantages :

* Changement de téléphone → modification d’un helper uniquement
* Changement d’application → aucune modification de code
* Possibilité de rediriger temporairement une cible

C’est un **pattern d’indirection obligatoire**.

---

## 🔄 Couche de synchronisation des téléphones

Cette architecture repose sur une **configuration maître unique par téléphone**

Helpers maîtres :

* `input_text.telephone_antoine`
* `input_text.telephone_constance`

Ces helpers contiennent **le nom logique brut du téléphone** (ex: `pixel_7a`).

À partir de cette valeur unique sont dérivés automatiquement :

* le service notify : `notify.mobile_app_<tel>`
* le capteur Wi‑Fi : `sensor.<tel>_wi_fi_bssid`
* le device_tracker : `device_tracker.<tel>`

### 🧠 Automation de synchronisation

Fichier :

* `/homeassistant/11_automations/system/telephones_synchro_helpers.yaml`
* ID : `10120000000017`

Rôle :

* Écouter toute modification d’un helper maître `input_text.telephone_*`
* Reconstruire dynamiquement toutes les entités dérivées
* Mettre à jour automatiquement les helpers suivants :

  * `input_text.telephone_<user>_notify`
  * `input_text.telephone_<user>_wifi_bssid`
  * `input_text.telephone_<user>_tracker`

Propriétés clés :

* Mapping dynamique
* Boucle générique (`repeat`)
* Zéro duplication de code
* Zéro dépendance matérielle

Cette automation garantit :

* Cohérence stricte entre nom logique et entités réelles
* Changement de téléphone sans refactor
* Centralisation absolue de la configuration mobile

---

## 📌 Scripts fournis

### 1️⃣ `script.notification_envoyer`

Rôle :

* Envoi d’une notification vers **une cible dynamique**

Entrées :

* `cible` : helper input_text contenant le service notify
* `titre`
* `message`

Usage typique :

* Notifications individuelles
* Alertes personnelles

---

### 2️⃣ `script.notification_envoyer_famille`

Rôle :

* Envoi simultané vers **les deux téléphones**

Cibles :

* `input_text.telephone_antoine_notify`
* `input_text.telephone_constance_notify`

Usage typique :

* Événements critiques
* Alertes de sécurité
* Situations nécessitant double réception

---

### 3️⃣ `script.notification_envoyer_avance`

Rôle :

* Variante avec paramètres avancés Android

Supporte via `extra` :

* priorité
* ttl
* importance
* tag
* group

Usage typique :

* Notifications persistantes côté OS
* Regroupement
* Priorisation forte

---

## 🔒 Garanties architecturales

Cette couche garantit :

* Aucune dépendance matérielle dans la logique métier
* Uniformisation totale des notifications
* Remplacement transparent des téléphones
* Centralisation des évolutions futures

Elle interdit structurellement :

* la duplication de logique d’envoi
* la dispersion des services notify
* les couplages directs automation ↔ téléphone

---

## 🚫 Responsabilités explicitement exclues

Ces scripts **ne font jamais** :

* décision de notification
* filtrage métier
* temporisation
* anti-spam
* journalisation
* accusé de réception
* gestion d’état

Ils sont **purement exécutifs**.

Toute intelligence doit rester :

* dans les capteurs décisionnels
* dans les automatisations métier
* dans les contrats fonctionnels

---

## 📐 Règles d’usage obligatoires

1. Toute notification mobile passe par un script `notification_*`
2. Aucun service notify direct dans le code métier
3. Toute nouvelle notification doit être justifiée fonctionnellement
4. Toute évolution de cette couche est **structurante**

Violation de ces règles = dette architecturale.

---

## 🧱 Classification

* Type : Couche infrastructure
* Niveau : Bas niveau
* Stabilité attendue : Très élevée
* Fréquence d’évolution : Rare

---

## 🔗 Fichiers de référence

* `/homeassistant/10_scripts/system/notifications_mobiles.yaml`

Helpers associés :

* `input_text.telephone_antoine_notify`
* `input_text.telephone_constance_notify`

---

## 🧩 Lien avec les autres contrats

Ce document est complémentaire de :

* Contrat Notifications (général)
* Audit des notifications persistantes
* Charte UI (sémantique des alertes)

Il définit la **couche technique**, pas la politique d’usage.

# ==========================================================
# Fin du document
# ==========================================================
