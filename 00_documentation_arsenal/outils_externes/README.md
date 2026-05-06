# 🧰 Arsenal — Outils externes

## 🎯 Objet

Ce dossier documente les **outils externes** utilisés autour
d’Arsenal (Home Assistant), sans faire partie de l’instance HA
elle-même.

Ces outils :
- ne s’exécutent pas dans Home Assistant
- n’interagissent pas avec l’API HA
- travaillent sur les **fichiers**, les **sauvegardes** ou
  l’**analyse hors ligne**
- prolongent Arsenal en tant que **système opérable**,
  au-delà de l’automatisation

Ils font partie intégrante de l’écosystème Arsenal.

---

## 🧠 Principes généraux

Les outils externes Arsenal respectent les invariants suivants :

- **Simplicité**
  - scripts courts
  - comportement explicite
  - aucune magie cachée

- **Traçabilité**
  - code lisible
  - fonctionnement compréhensible
  - aucune boîte noire

- **Efficacité immédiate**
  - un besoin réel
  - une action simple
  - un résultat exploitable

- **Aucune dépendance inutile**
  - pas de cloud
  - pas d’APK spécifique
  - pas de service tiers obligatoire

---

## 📂 Organisation

outils_externes/
├── pc/
│ └── (scripts PC)
└── mobile/
└── (scripts mobile / Termux)

00_documentation_arsenal/outils_externes/
├── README.md
├── pc/
│ └── README.md
└── mobile/
└── README.md


- Le dossier `outils_externes/` contient le **code réel**
- Le dossier `00_documentation_arsenal/outils_externes/` contient
  la **documentation fonctionnelle associée**

---

## 🖥️ Outils externes PC

Les outils PC sont documentés dans :

00_documentation_arsenal/outils_externes/pc/README.md


Ils couvrent notamment :
- la recherche textuelle globale dans les fichiers Home Assistant
- l’audit de messages UI, templates et libellés
- la compréhension rapide de l’origine d’un comportement

---

## 📱 Outils externes Mobile

Les outils mobiles sont documentés dans :

00_documentation_arsenal/outils_externes/mobile/README.md


Ils couvrent notamment :
- le diagnostic et l’analyse depuis un smartphone
- la synchronisation des sauvegardes Home Assistant
- l’utilisation de widgets 1-tap (Termux)
- la continuité fonctionnelle PC ↔ mobile

---

## 🧭 Positionnement dans Arsenal

Les outils externes :
- ne remplacent pas Home Assistant
- ne prennent aucune décision automatique
- ne contournent pas les règles métier

Ils servent à :
- **comprendre**
- **auditer**
- **diagnostiquer**
- **agir plus vite et plus sereinement**

Ils réduisent la charge mentale et évitent les manipulations
manuelles répétitives.

---

## 🟢 Invariant Arsenal

> Si un outil externe devient indispensable à l’exploitation
> d’Arsenal, alors :
> - son **code** doit être centralisé dans `outils_externes/`
> - son **fonctionnement** doit être documenté ici
