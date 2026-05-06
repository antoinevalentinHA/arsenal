## 🛠️ Procédure — Ajouter un script Termux avec raccourci Android

Cette procédure décrit **intégralement et précisément** comment :
- ajouter un script personnalisé dans Termux
- le rendre exécutable
- créer un raccourci Android via widget
- lancer l’outil en **un tap**, sans accès direct à Home Assistant

---

## 🎯 Objectif

- Exécuter un script Arsenal depuis un smartphone Android
- Utiliser une boîte de dialogue native
- Lancer l’outil via un widget sur l’écran d’accueil
- Ne créer aucune dépendance réseau
- Ne pas exposer Home Assistant

---

## 📦 Prérequis

Application Android :
- **Termux**

---

## ⚙️ Étape 1 — Préparer Termux

Ouvrir Termux puis exécuter :

```bash
pkg update
pkg install ripgrep jq
termux-setup-storage

Créer l’arborescence Arsenal :

mkdir -p ~/scripts
mkdir -p /storage/emulated/0/HA/data
mkdir -p /storage/emulated/0/HA/results

## 🧠 Étape 2 — Ajouter le script

Créer le fichier du script :

nano ~/scripts/nom_du_script

Coller intégralement le script Arsenal, puis sauvegarder :

Ctrl + O → Entrée
Ctrl + X

Rendre le script exécutable :
chmod +x ~/scripts/nom_du_script

Test direct (sans raccourci) :
~/scripts/nom_du_script

## 🔗 Étape 3 — Créer le raccourci pour widget

Termux:Widget utilise exclusivement le dossier :
~/.shortcuts

Créer le dossier (si absent) :
mkdir -p ~/.shortcuts

Créer le lien symbolique :
ln -s ~/scripts/ha_find_contexte ~/.shortcuts/nom_du_script

Vérification :
ls -l ~/.shortcuts
