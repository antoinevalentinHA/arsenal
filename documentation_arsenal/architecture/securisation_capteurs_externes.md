# 🧠 ARSENAL — Architecture
# 🔐 Sécurisation des capteurs externes

## 📌 Statut

Document **normatif**  
Version **figée**

---

## 🎯 Objet

Ce document définit les **règles architecturales opposables**
relatives à la **sécurisation locale des capteurs issus d’intégrations externes**
au sein du système Arsenal.

Il formalise les **invariants de continuité d’état**, de **robustesse**
et de **non-dépendance directe à des services externes**
pour toute donnée exploitée par l’architecture Arsenal.

---

## 🧱 Périmètre

Cette architecture couvre exclusivement :

- les **capteurs dépendant d’API, de services cloud ou de tokens**,
- les **données physiques, numériques, statistiques ou de diagnostic**,
- les mécanismes de **conservation locale du dernier état valide**,
- les capteurs utilisés à des fins de **pilotage indirect, diagnostic ou observation**.

Elle ne couvre pas :

- la logique métier,
- les décisions centrales,
- les automatismes d’action,
- la représentation UI.

---

## 🧠 Principe architectural fondamental

Aucune donnée issue d’un service externe
ne constitue une **référence fiable par nature**.

Toute intégration externe est considérée comme :

- potentiellement indisponible,
- sujette à expiration d’accès (token),
- intermittente ou dégradée,
- non contractuelle en continuité.

L’architecture Arsenal repose exclusivement
sur des **états locaux sécurisés**, stables et maîtrisés.

---

## 🧱 Invariants architecturaux

### Invariant 1 — Continuité d’état obligatoire

Aucune rupture d’état ne doit être perceptible
au niveau de l’architecture Arsenal,
y compris lors :

- d’une coupure API,
- d’une erreur d’authentification,
- d’une absence temporaire de données,
- d’un redémarrage système.

---

### Invariant 2 — Conservation stricte du dernier état valide

Lorsqu’une source externe devient indisponible :

- la **dernière valeur valide connue** est conservée,
- aucune valeur n’est reconstruite,
- aucune valeur n’est extrapolée,
- aucune valeur arbitraire n’est injectée.

---

### Invariant 3 — Interdiction de propagation d’états indéterminés

Les états suivants ne doivent **jamais** être exposés
au reste de l’architecture Arsenal :

- `unknown`,
- `unavailable`,
- valeurs vides, nulles ou non typées.

---

### Invariant 4 — Séparation stricte source / état local sécurisé

Toute donnée externe doit être représentée par :

- une **entité source brute** (non fiable),
- une **entité locale sécurisée**,
  seule autorité architecturale.

Aucune décision, aucun calcul,
aucune analyse Arsenal
ne consomme directement une entité source brute.

---

### Invariant 5 — Neutralité fonctionnelle absolue

La sécurisation :

- n’ajoute aucune logique métier,
- ne modifie aucune intention fonctionnelle,
- n’interprète jamais la donnée,
- ne qualifie pas la valeur.

Elle se limite strictement à la
**stabilisation et à la continuité de l’état**.

---

### Invariant 6 — Déterminisme au redémarrage

Les entités locales sécurisées doivent garantir :

- un état cohérent après redémarrage,
- une stabilisation explicite du système,
- l’absence de transitions erratiques initiales.

---

### Invariant 7 — Indépendance vis-à-vis des services tiers

L’exploitation des données locales sécurisées doit permettre :

- un fonctionnement Arsenal indépendant du cloud,
- une consultation dashboard sans requêtes externes,
- une continuité statistique locale,
- une résilience totale aux pannes de service tiers.

---

## 🧱 Typologies de sécurisation reconnues

### États binaires physiques

- Acceptation exclusive de valeurs binaires valides,
- Rejet de tout autre état,
- Conservation stricte de la dernière valeur connue.

---

### États numériques critiques

- Acceptation exclusive de valeurs numériques valides,
- Conservation locale du dernier état valide,
- Absence totale de recalcul ou de normalisation.

---

### États statistiques ou de santé

- Stabilisation des mesures issues de services tiers,
- Continuité des historiques locaux,
- Absence de rupture en cas de données manquantes,
- Non-dépendance à la disponibilité temps réel du service externe.

---

### États de diagnostic et d’observation

- Valeur exploitable même en cas d’indisponibilité externe,
- Utilisation possible pour analyse, suivi ou corrélation,
- Aucune exigence de fraîcheur cloud.

---

## 🧱 Frontières de responsabilité

### Responsabilité des services externes

- Fourniture de données brutes,
- Disponibilité non garantie,
- Accès conditionné (tokens, quotas),
- Aucune obligation de continuité.

---

### Responsabilité de l’architecture Arsenal

- Sécurisation locale systématique,
- Continuité sémantique des états,
- Indépendance fonctionnelle,
- Exposition d’un état stable, durable et exploitable.

---

## 🚫 Interdictions architecturales

Il est strictement interdit :

- d’utiliser directement une entité externe brute
  dans une décision, un calcul ou une analyse Arsenal,
- de reconstruire ou corriger une valeur absente,
- d’injecter une valeur fictive pour masquer une panne,
- d’introduire une logique métier
  dans un mécanisme de sécurisation,
- de lier un usage critique
  à la disponibilité temps réel d’un service tiers.

---

## 📌 Statut

Référence architecturale **normative et opposable**.

Toute extension, dérogation ou spécialisation
doit faire l’objet d’un document d’architecture distinct,
explicitement qualifié et validé.