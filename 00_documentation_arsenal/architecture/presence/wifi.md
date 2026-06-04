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