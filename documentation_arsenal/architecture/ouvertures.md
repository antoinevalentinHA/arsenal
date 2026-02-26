# ==========================================================
# 🧠 ARSENAL — ARCHITECTURE : OUVERTURES
# ----------------------------------------------------------
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

N0 constitue l’entrée physique du pipeline.

---

## 2.2 N1 — Normalisation (contact stable)

- Entités `binary_sensor.contact_*`
- Rôle :
  - produire un état structurellement stable
  - encapsuler l’indisponibilité
  - découpler le reste du système des capteurs bruts

Caractéristiques :

- état toujours exploitable
- pas de délai
- pas de qualification
- abstraction pure

N1 stabilise la structure.

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
- Rôle :
  - fournir un cadre temporel
- Aucun calcul
- Aucune décision

Ils introduisent la dimension temps dans le pipeline.

---

## 2.6 Automatisations de qualification

Les automatisations :

- surveillent les états stabilisés,
- s’appuient sur les timers,
- posent explicitement des faits métier (helpers).

Elles constituent la jonction entre :

structure → temporalité → qualification.

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
  Automation de qualification
            ↓
  Helper (fait métier explicite)
            ↓
  Moteurs externes (chauffage / aération / alarme)
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