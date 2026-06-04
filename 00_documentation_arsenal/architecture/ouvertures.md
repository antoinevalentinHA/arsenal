# 🧠 ARSENAL — ARCHITECTURE : OUVERTURES
# Domaine :
#   Ouvertures (portes / fenêtres)
#
# Nature :
#   Document ARCHITECTURAL
#
# Rôle :
#   Décrire le positionnement, les responsabilités
#   et les flux du sous-système « Ouvertures » dans
#   l’architecture globale Arsenal.
#
# ⚠️ Ce document :
#   - N’est PAS contractuel
#   - Ne définit AUCUNE règle métier
#   - Ne reformule AUCUN invariant
#   - Ne remplace PAS le contrat Ouvertures
# ==========================================================


## 1. 🎯 RÔLE ARCHITECTURAL DU SOUS-SYSTÈME OUVERTURES

Le sous-système **Ouvertures** constitue un pipeline structuré
d’observation, de transformation et de qualification des
événements physiques liés aux portes et fenêtres.

Il transforme :

- des signaux physiques bruts,
- en états structurellement stables,
- puis en agrégats exploitables,
- puis en faits métier explicites.

Il expose ces états aux moteurs décisionnels externes.

Il ne prend aucune décision métier.


---

# 🧱 2. ARCHITECTURE EN COUCHES

Le sous-système est organisé en couches distinctes.

---

## 2.1 N0 — Détection physique (signal brut)

- Capteurs matériels `binary_sensor.capteur_*`
- Rôle :
  - fournir un état physique brut
- Caractéristiques :
  - dépend du matériel
  - peut être indisponible
  - aucune logique embarquée

### ⚠️ Évolution structurelle : redondance physique N0 (ouvrants critiques)

Pour certains ouvrants critiques, N0 peut désormais être **redondé** :

- **A** : capteur historique
- **B** : capteur redondant (suffixe `_bis`)

Exemples :

- `binary_sensor.contact_chambre_parents_gauche_1` + `binary_sensor.contact_chambre_parents_gauche_2`
- `binary_sensor.contact_sejour_3_1` + `binary_sensor.contact_sejour_3_2`
- `binary_sensor.contact_garage_1` + `binary_sensor.contact_garage_2`

Cette redondance reste **strictement N0** :
elle n’introduit aucun fait métier, aucune temporisation, aucune décision.

---

## 2.2 N1 — Normalisation (contact stable)

- Entités `binary_sensor.contact_*`
- Rôle :
  - produire un état structurellement stable
  - encapsuler l’indisponibilité
  - découpler le reste du système des capteurs bruts

### ⚙️ Mode N1 : source unique vs réconciliation A/B

N1 peut être alimenté selon deux modes exclusifs :

1) **Source unique** (cas nominal historique)  
   `contact_*` = normalisation directe d’une seule source N0.

2) **Réconciliation A/B** (ouvrants redondés)  
   `contact_*` = réconciliation déterministe de deux sources N0 (A/B),
   avec exposition d’attributs d’observabilité (`degrade`, `divergence`, états bruts).

Dans les deux cas, l’API N1 reste identique pour les consommateurs :

- mêmes entités finales : `binary_sensor.contact_*`
- mêmes attentes structurelles : état exploitable (`on/off`)
- absence de temporisation et de qualification

N1 stabilise la structure, indépendamment du fait que N0 soit simple ou redondé.

---

## 2.3 N2 — Agrégation (OR logique)

- Entités `binary_sensor.contact_<zone>`
- Rôle :
  - agréger les ouvertures par pièce / zone / maison
  - exposer un état instantané consolidé

Caractéristiques :

- dépend uniquement de N1
- calcul instantané
- sans temporisation
- sans interprétation

N2 consolide la topologie.

---

## 2.4 Canons d’orchestration (stabilisation locale)

Certaines entités dérivées (ex. fermeture stable) fournissent
des signaux robustes destinés aux moteurs externes.

Rôle :

- stabilisation temporelle localisée
- prévention des oscillations rapides
- simplification des consommateurs en aval

Ces entités restent structurelles :
elles ne qualifient aucun fait métier.

---

## 2.5 Cadres temporels

- Timers de grâce

Rôle :

- fournir un cadre temporel
- introduire la dimension temps dans le pipeline

Caractéristiques :

- aucun calcul métier
- aucune décision
- état `idle` structurellement ambigu
  (expiration naturelle ou annulation)

La fin d’une temporisation n’est jamais déduite
directement de l’état du timer.

Elle est matérialisée explicitement
par un helper de type `input_boolean`
activé exclusivement sur l’événement `timer.finished`.

Les timers introduisent le temps.
Les helpers matérialisent son interprétation.

---

## 2.6 Automatisations de qualification

Les automatisations :

- surveillent les états stabilisés,
- réagissent aux événements des timers,
- matérialisent explicitement la fin de grâce via helpers dédiés,
- posent des faits métier explicites lorsque les conditions sont réunies.

Elles constituent la jonction entre :

structure → temporalité → matérialisation → qualification.

---

## 2.7 Helpers

Les helpers matérialisent :

- des paramètres temporels,
- des faits métier explicites.

Ils servent de points d’ancrage pour les moteurs externes.

---

## 2.8 UI (Restitution)

Les dashboards :

- exposent les états N1 / N2 / canons / helpers,
- fournissent observabilité et diagnostic,
- ne modifient jamais la structure interne.


---

# 🔄 3. FLUX ARCHITECTURAL GLOBAL

Flux conceptuel détaillé :

N0  Capteur physique brut
            ↓
  N1  Normalisation structurelle
            ↓
  N2  Agrégation topologique
            ↓
  Canon (stabilisation locale)
            ↓
  Timer (cadre temporel)
            ↓
  Helper (fin de grâce explicite)
            ↓
  Automation de qualification
            ↓
  Helper (fait métier explicite)
            ↓
  Moteurs externes
            ↓
  Restitution UI

Chaque couche :

- a une responsabilité unique,
- ne connaît pas les règles métier globales,
- n’agit pas hors de son rôle.

---

# 🔗 4. RELATIONS AVEC LES AUTRES DOMAINES

### Chauffage
Consomme des états qualifiés issus du pipeline Ouvertures.

### Aération
Consomme le fait métier explicite.

### Alarme
Consomme les états d’ouverture stabilisés.

Le sous-système Ouvertures reste neutre :
il fournit des faits, il ne décide pas.

---

# 🧠 5. PRINCIPES ARCHITECTURAUX CLÉS

- Découplage matériel / logique
- Stabilisation avant qualification
- Qualification explicite
- Séparation observation / décision
- Responsabilité unique par couche

Ce document décrit la structure et le flux.
Les règles et interdictions relèvent exclusivement
du contrat Ouvertures.

---

# ==========================================================
# 📐 ARCHITECTURE OUVERTURES — DOCUMENT DE RÉFÉRENCE
# ==========================================================