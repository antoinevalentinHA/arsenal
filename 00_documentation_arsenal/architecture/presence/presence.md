# 🧠 ARSENAL — ARCHITECTURE · Présence maison

## 🎯 Objet du document

Ce document définit l’**architecture de référence de la notion de présence**
au sein du système Arsenal.

Il fixe :
- les **types de présence reconnus**,
- leur **périmètre sémantique exact**,
- les **règles d’usage inter-domaines**,
- les **interdictions structurelles**.

Ce document est **architectural** :
- il ne décrit **aucune implémentation**,
- il ne contient **aucun YAML**,
- il ne remplace **aucun contrat métier**.

Il constitue une **référence amont normative**
pour tous les contrats utilisant la notion de présence.

---

## 🧠 Principe fondamental

La présence est un **signal de contexte**.

Elle :
- n’est **jamais une décision**,
- n’entraîne **aucune action directe**,
- ne porte **aucune logique métier finale**.

Chaque domaine (chauffage, alarme, éclairage, etc.)
reste **pleinement souverain** dans son interprétation.

---

## 🧱 Typologie des présences Arsenal

Arsenal distingue **plusieurs présences non équivalentes**.
Elles ne sont **ni interchangeables, ni substituables**.

### 1️⃣ Présence sécurité

**Finalité exclusive :**
- protection du domicile,
- logique d’alarme et de sûreté.

**Caractéristiques :**
- conservatrice (tolérance aux faux positifs),
- basée sur zones, géolocalisation, Wi-Fi, états techniques,
- stabilisée par temporisations.

**Règles normatives :**
- utilisée **uniquement** par les systèmes de sécurité,
- **interdite** pour tout calcul de confort thermique,
- **jamais** utilisée pour déclencher chauffage ou climatisation.

---

### 2️⃣ Présence confort (présence unifiée)

**Finalité exclusive :**
- confort thermique,
- usage domestique quotidien.

**Caractéristiques :**
- plus permissive,
- agrégation de signaux humains (person.*, enfants, visiteurs),
- corrigée contre les fluctuations brèves.

**Règles normatives :**
- utilisée par :
  - chauffage,
  - climatisation,
  - éclairage de confort,
- **interdite** pour l’armement de l’alarme.

#### ⏱️ Temporalité et réactivité

La présence confort est conçue comme un signal **stabilisé mais potentiellement réactif**.

- Elle peut utiliser des temporisations courtes,
  dès lors que l’architecture garantit :
    • séparation stricte décision / écriture,
    • absence d’écriture matérielle directe déclenchée par présence,
    • décisions centralisées et filtrées,
    • anti-redondance systématique.

- La réactivité de la présence confort est un **choix d’architecture**,
  non une optimisation locale.

👉 La présence confort peut ainsi être exploitée comme
signal quasi temps réel de contexte,
sans créer de dépendance dangereuse ni d’oscillation thermique.

La présence confort **ne devient jamais un déclencheur** :
elle reste un **signal de contexte pur**, quelle que soit sa réactivité.

---

### 3️⃣ Présences contextuelles spécifiques

Présences **fonctionnelles**, non universelles.

Exemples :
- présence enfants,
- présence visiteur,
- babysitting,
- présence programmée.

**Caractéristiques :**
- périmètre métier limité,
- combinables avec présence confort,
- jamais utilisées seules pour la sécurité.

---

### 4️⃣ Présences techniques (sources)

Signaux **bruts**, non décisionnels :
- Wi-Fi,
- GPS,
- zones,
- capteurs physiques.

**Règles :**
- jamais consommées directement par un domaine métier,
- toujours encapsulées dans une présence de niveau supérieur.

---

## 🧭 Règles d’usage transverses (invariants)

Les règles suivantes sont **non négociables** :

- ❌ L’alarme **ne consomme jamais** la présence confort.
- ❌ Le chauffage **ne consomme jamais** la présence sécurité.
- ❌ Aucune automatisation ne doit :
  - écrire dans un capteur de présence,
  - modifier un état de présence à des fins métier.
- ❌ Une présence ne déclenche **jamais** une action matérielle directe.

---

## 🔀 Séparation décision / usage

La présence :
- **expose un état**,
- **n’interprète rien**,
- **ne décide rien**.

Les décisions sont prises :
- dans des scripts métier,
- ou des automations de domaine,
- sous contrat explicite.

---

## 📎 Relation avec les contrats Arsenal

Ce document est une **référence architecturale amont**.

Les contrats suivants s’y appuient explicitement :
- contrat Présence maison,
- contrat Chauffage,
- contrat Climatisation,
- contrat Alarme,
- contrat Éclairage.

Un contrat **ne redéfinit jamais** la notion de présence.
Il choisit **quelle présence consommer**, conformément à ce document.

---

## 🛑 Ce que ce document interdit explicitement

- toute fusion implicite des présences,
- toute redéfinition locale non documentée,
- toute dépendance cachée entre domaines,
- toute logique métier injectée dans un capteur de présence.

---

## 📌 Statut

- Document architectural Arsenal
- Normatif
- Transverse
- Stable

Toute évolution de ce document :
- est rare,
- doit être justifiée,
- entraîne une revue des contrats dépendants.

---