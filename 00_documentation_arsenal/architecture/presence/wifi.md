# 🧠 ARSENAL — CHAÎNE MÉTIER · Présence Wi-Fi

## 🎯 Objet

Ce document décrit la **chaîne fonctionnelle canonique**
de construction de la présence Wi-Fi métier dans Arsenal.

Il ne s’agit pas :
- d’un contrat
- d’une décision
- d’un changelog
- d’une implémentation

Mais d’une **vue d’architecture fonctionnelle**.

---

## 🧩 Chaîne fonctionnelle

capteurs Wi-Fi bruts (Android / iOS)
        ↓
sensor.telephone_*_bssid_dynamic
        ↓
binary_sensor.wifi_nouveau_bssid     (diagnostic pur, événementiel)
        ↓
automation 10120000000016             (apprentissage contrôlé)
        ↓
input_text.bssid_maison               (base d’apprentissage)
        ↓
binary_sensor.presence_wifi_maison    (présence Wi-Fi métier)

---

## 🧠 Rôles sémantiques

### capteurs Wi-Fi bruts
- sources physiques
- non fiables
- non gouvernées
- non métier

### sensor.telephone_*_bssid_dynamic
- normalisation
- exposition brute
- aucune logique métier

### binary_sensor.wifi_nouveau_bssid
- diagnostic pur
- événementiel
- non persistant
- non décisionnel

### automation 10120000000016
- action contrôlée
- apprentissage gouverné
- aucune logique de détection
- aucune décision métier

### input_text.bssid_maison
- mémoire canonique
- base d’apprentissage
- référence fonctionnelle

### binary_sensor.presence_wifi_maison
- signal métier final
- exploitable inter-domaines
- stable
- contractuel
- compare **après normalisation des deux côtés** (contrat `bssid.md` §6, §11) le BSSID du capteur
  Companion (format brut `aa:bb:…`) et le référentiel canonique
- applique la **règle de fraîcheur** (`bssid.md` §11.1) : le Wi-Fi d'un téléphone ne compte plus si son
  GPS a signalé `not_home` plus récemment que le dernier changement de son BSSID
- contributeur direct de la présence sécurité (`binary_sensor.presence_famille_securite`, terme OU) :
  une connexion au Wi-Fi domestique suffit à établir la présence, sans confirmation GPS simultanée

---

## 🔒 Invariant de chaîne

- Aucun maillon ne cumule :
  - diagnostic + action
  - action + décision
  - décision + mémoire
- Toute la chaîne respecte la séparation :
  **source → diagnostic → action → mémoire → signal métier**

---

## 📌 Statut

- Document d’architecture fonctionnelle
- Référence lisible humaine
- Non contractuel
- Non exécutable
- Stable