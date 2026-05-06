# 📱 Arsenal — Outils externes Mobile

## 🎯 Objet

Ce document décrit les **outils externes mobiles**
permettant d’exploiter Arsenal **directement depuis un smartphone**,
sans perte de puissance ni compromis fonctionnel.

Le mobile n’est pas un terminal passif :
il devient un **outil de diagnostic et de décision**.

---

## 🧠 Principes

- Le mobile est un poste de travail à part entière
- Aucun APK spécifique
- Aucune dépendance cloud
- Scripts simples, lisibles, maîtrisés
- UI minimale, native, sans surcouche

---

## 🔍 Outil — HA_Find (recherche textuelle mobile)

### Rôle

Permet de retrouver instantanément l’origine d’un texte
affiché dans Home Assistant, directement depuis le téléphone.

---

### Architecture

- Moteur : script shell (Termux)
- Interface : boîte de dialogue native
- Lancement : widget Android (1 tap)
- Résultat : fichier texte structuré

---

### Bénéfices

- Diagnostic immédiat, même hors PC
- Fin du « je regarderai plus tard »
- Alignement total avec l’outil PC

---

## 🔍 Outil — HA_Find_Contexte (recherche textuelle mobile avancée)

### Rôle

Permet de retrouver instantanément l’origine exacte
d’une entité ou d’un texte Home Assistant depuis un smartphone,
avec **contexte lisible et structuré** (avant / après).

---

### Architecture

- Environnement : Termux (Android)
- Moteur : script shell + ripgrep
- Interface : boîte de dialogue Android native
- Lancement : widget Android (1 tap)
- Données : sauvegarde Home Assistant locale (décompressée)
- Sortie : fichier texte formaté (style Arsenal)

---

### Fonctionnalités clés

- Recherche récursive dans `HA/data`
- Filtrage par extensions pertinentes (YAML, Jinja, Markdown…)
- Exclusion automatique des dossiers techniques
- Affichage du contexte ±N lignes
- Mise en évidence explicite de la ligne trouvée (`>>>`)
- Résultat immédiatement ouvrable sur mobile

---

### Bénéfices

- Diagnostic immédiat, même hors PC
- Lecture confortable sur écran mobile
- Traçabilité des recherches (fichiers résultats)
- Continuité fonctionnelle PC ↔ mobile

---

## 🔄 Outil — HA_Update (synchronisation des sauvegardes)

### Problème initial

La structure imbriquée des sauvegardes Home Assistant
rend leur exploitation manuelle pénible sur mobile.

---

### Solution

Script automatisé permettant :
- de détecter la **dernière sauvegarde téléchargée**
- d’extraire uniquement le dossier `data`
- de synchroniser l’environnement mobile en un seul geste

---

### Usage

- 1 tap sur le widget
- extraction
- remplacement de `HA/data`
- nettoyage automatique

---

### Valeur ajoutée

- Suppression totale de la friction
- Mise à jour fiable et reproductible
- Continuité PC ↔ mobile
