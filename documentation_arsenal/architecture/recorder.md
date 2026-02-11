# 🧱 Arsenal — Principes du Recorder Home Assistant

---

## 🎯 OBJECTIF

Définir des règles **claires, stables et non négociables**
concernant l’usage du **Recorder Home Assistant** dans Arsenal.

Le Recorder n’est **pas un historique exhaustif**.
C’est un **outil d’observation fonctionnelle**, au service :

- de la compréhension du système
- de l’analyse dans le temps
- de la vérification des décisions métier

---

## 🧠 PRINCIPE FONDAMENTAL

> **On n’enregistre que ce qui a un sens dans le temps.**

Toute entité incluse dans le Recorder doit répondre à la question :

> *« Cette donnée est-elle utile à relire dans 1 jour, 1 semaine ou 1 mois ? »*

Si la réponse est non → elle ne doit pas être enregistrée.

---

## 🧩 TYPOLOGIE DES ENTITÉS FACE AU RECORDER

### ✅ Entités ÉLIGIBLES au Recorder

Ce sont des **faits observables**, stables et interprétables :

#### 🌡️ Données physiques
- températures
- humidité (relative / absolue)
- CO₂
- bruit
- pression
- humidex

#### 🧠 États fonctionnels
- modes (maison, chauffage, ECS, clim…)
- autorisations
- décisions calculées
- états consolidés (présence, blocage, alerte)

#### ⚡ Énergie & consommation
- capteurs d’énergie cumulée
- proxy énergie conformes aux exigences HA
- utility meters

#### 🕒 Repères temporels
- timers
- input_datetime structurants
- marqueurs de cycle (début / fin)

---

### ❌ Entités NON ÉLIGIBLES au Recorder

Ce sont des **outils techniques**, transitoires ou bruités :

- capteurs intermédiaires
- capteurs purement techniques
- valeurs de calcul instantané
- entités de debug
- entités de confort UI
- helpers de travail (input_text, input_number techniques)
- entités à forte fréquence sans valeur d’analyse

> **Le Recorder n’est pas un logger technique.**

---

## 🧱 PRINCIPE DE FILTRAGE STRICT (ALLOWLIST)

Arsenal applique une règle volontairement stricte :

> **Tout ce qui n’est pas explicitement inclus est exclu.**

Le fichier `recorder.yaml` fonctionne exclusivement en **include**.

Avantages :
- maîtrise totale du volume de données
- lisibilité long terme
- absence de pollution historique
- performance constante

---

## ⏳ RÉTENTION & PERFORMANCE

### Politique retenue

- purge automatique activée
- durée de conservation volontairement limitée
- engagement clair : **qualité > quantité**

Le Recorder n’est **pas** une archive.
Il est un **outil de lecture récente et moyenne durée**.

---

## 🔗 RELATION AVEC LES AUTRES COMPOSANTS

### Recorder ≠ Logbook

- **Recorder** : données continues, analytiques
- **Logbook** : événements significatifs, narratifs

Ils sont **complémentaires**, jamais redondants.

---

### Recorder ≠ Historique UI brut

L’UI Home Assistant n’est qu’un **client de lecture**.
Le Recorder reste **maître des données**, pas l’interface.

---

## 🧠 CAS PARTICULIER : CAPTEURS PROXY

Certains capteurs existent **uniquement** pour satisfaire
les contraintes du Recorder (énergie, statistiques long terme).

Règles associées :
- usage strictement technique
- jamais utilisés dans la logique métier
- jamais affichés directement à l’utilisateur
- documentés comme tels

---

## 🚫 DÉRIVES EXPLICITEMENT REFUSÉES

- « On enregistre tout, on verra plus tard »
- « Ça peut servir un jour »
- « Le stockage est pas cher »
- « Home Assistant le fait par défaut »

Arsenal refuse ces logiques.

---

## 🧾 RÈGLE D’OR ARSENAL

> **Si une donnée n’est pas relisible intelligemment dans le temps,
> elle n’a rien à faire dans le Recorder.**

---

## 📌 STATUT

- Nature : **principe architectural**
- Champ : **Recorder Home Assistant**
- Applicabilité : globale
- Évolution : rare, réfléchie, documentée

---