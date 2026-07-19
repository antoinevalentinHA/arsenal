# 🧠 ARSENAL — CONTRAT NORMATIF · OBSERVATION THERMIQUE D’AÉRATION · Détection d’intégrité physique & anti-épisode zombie

# ----------------------------------------------------------
# 📌 STATUT CONTRACTUEL
# ----------------------------------------------------------
#
# - Nature :
#     CONTRAT NORMATIF DE FONDATION — ACTIF
#
# - Domaine :
#     Chauffage / Aération / Observabilité physique
#
# - Autorité :
#     Ce contrat est opposable à toute implémentation
#     visant à :
#       • qualifier un épisode d’aération,
#       • détecter une incohérence thermique,
#       • sécuriser le pipeline aération,
#       • neutraliser les épisodes zombies.
#
# - Hiérarchie :
#     Subordonné à :
#       [45_aeration.md](45_aeration.md)
#
#     Indépendant de :
#       • décision centrale chauffage,
#       • offsets thermiques,
#       • présence / absence,
#       • météo,
#       • UI et pédagogie.
#
# ----------------------------------------------------------


## 🎯 OBJET DU CONTRAT

Ce contrat définit **le cadre normatif d’observation thermique**
permettant de :

- vérifier la **réalité physique** d’un épisode d’aération,
- détecter toute **incohérence capteur Zigbee**,
- neutraliser tout **épisode zombie**,
- garantir que toute aération reconnue a produit
  un **impact thermique mesurable**.

Il encadre exclusivement :

- les capteurs thermiques autorisés,
- les règles physiques minimales,
- la temporalité d’observation,
- les invariants de cohérence,
- les critères de validation / invalidation.

👉 Ce contrat **ne décide rien**.  
Il **observe, qualifie et protège**.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- l’observation thermique post-aération,
- la validation physique d’un épisode,
- la détection d’anomalies capteurs,
- la sécurisation du pipeline d’aération,
- la protection contre :
  - ouvertures fantômes,
  - fermetures manquées,
  - capteurs figés,
  - désynchronisations Zigbee.

---

## 🚫 HORS PÉRIMÈTRE EXPLICITE

Ce contrat **NE COUVRE PAS** :

- la décision de bloquer ou relancer le chauffage,
- les seuils de confort,
- les offsets thermiques,
- la recommandation d’aérer,
- la météo,
- la UI.

Ces aspects relèvent de contrats distincts.

---

## 🧠 PRINCIPE FONDAMENTAL

> **Toute aération physique réelle produit une chute thermique mesurable
> dans au moins une pièce concernée.**

L’absence totale de chute thermique constitue :

- soit une ouverture fantôme,
- soit une incohérence capteur,
- soit un épisode zombie.

---

## 🌡️ CAPTEURS THERMIQUES AUTORISÉS

Seuls sont autorisés comme sources d’observation :

- `sensor.temperature_chambre_parents`
- `sensor.temperature_chambre_enfants`
- `sensor.temperature_chambre_matthieu`
- `sensor.temperature_sejour`
- `sensor.temperature_entree`

Ces capteurs doivent être :

- physiques,
- conformes au contrat météo,
- sans filtrage métier,
- non dérivés,
- utilisés exclusivement via leurs ΔT associés.

---

## 🧊 MÉTRIQUE CANONIQUE — ΔT (MANQUE THERMIQUE)

L’observation repose **exclusivement** sur :
  ΔT_zone = max(T_ref_zone – T_actuelle_zone, 0)

Propriétés normatives :

- toujours numérique,
- jamais négatif,
- monotone croissant tant que la chute continue,
- indépendant de la cadence de publication,
- robuste aux silences capteurs.

Aucune autre métrique n’est autorisée.

---

## ⏱️ TEMPORALITÉ PHYSIQUE DE RÉFÉRENCE

### Invariants établis expérimentalement

- cadence minimale utile des capteurs : **≈ 10 minutes**
- première variation réelle observable :
  - entre **5 et 15 minutes**
- silence prolongé possible sans anomalie :
  - jusqu’à **60–150 minutes**

---

### Fenêtres normatives

| Phase | Délai minimal | Rôle |
|------|---------------|------|
| Stabilisation capteurs | 10 minutes | éviter lectures prématurées |
| Fenêtre d’observation primaire | 10–30 minutes | détection chute attendue |
| Fenêtre maximale tolérée | 60 minutes | limite physique haute |

Aucune observation avant **10 minutes** n’est autorisée.

---

## 🧩 CORRESPONDANCE ZONE — OUVRANT

Chaque ouvrant est associé **à une seule zone thermique canonique**.

L’observation est réalisée :

- exclusivement sur la zone de l’ouvrant ouvert,
- jamais sur une autre zone,
- jamais par agrégation globale.

Une incohérence entre ouvrant et zone invalide l’épisode.

---

## 🔒 INVARIANTS PHYSIQUES ABSOLUS

Il est **strictement obligatoire** que :

- au moins une zone ouverte présente :
  - `ΔT_zone ≥ ΔT_min_physique`
- dans la fenêtre :
  - [10 min ; 30 min] après fin d’aération.

À défaut :

- l’épisode est réputé **thermiquement incohérent**.

---

## 🧯 SEUIL PHYSIQUE MINIMAL

### ΔT_min_physique canonique

Valeur normative :

- **0.2 °C**

Justification :

- résolution effective capteurs : 0.1 °C  
- bruit thermique négligeable  
- chute réelle toujours ≥ 0.2 °C lors d’une aération effective  

Toute chute < 0.2 °C est réputée **non significative**.

---

## 🚨 DÉTECTION D’ÉPISODE ZOMBIE

Un épisode est qualifié **ZOMBIE** si :

- au moins un ouvrant a été reconnu,
- le pipeline a été armé,
- mais :
  - aucune zone correspondante ne présente
    `ΔT_zone ≥ 0.2 °C`
  - dans les 30 minutes suivant la fermeture.

---

## 🛑 EFFETS NORMATIFS D’UNE INCOHÉRENCE

Lorsqu’un épisode est qualifié incohérent :

- l’épisode est invalidé,
- le pipeline est désarmé,
- le blocage thermique est neutralisé,
- l’événement est journalisé,
- le système est replacé en état stable.

Aucune décision thermique ne doit dépendre d’un épisode incohérent.

---

## 🛡️ ROBUSTESSE & SÉCURITÉ

Le système garantit :

- indépendance totale vis-à-vis de la cadence Zigbee,
- tolérance aux silences prolongés,
- absence de faux négatifs sur aération réelle,
- neutralisation automatique des épisodes fantômes.

---

## 🧭 POSITIONNEMENT ARCHITECTURAL

Ce contrat :

- n’anticipe rien,
- ne décide rien,
- ne pilote rien.

Il constitue une **couche de vérité physique**
entre :

- les capteurs Zigbee
- et les décisions métier supérieures.

---

## 📌 STATUT

- Contrat normatif : **ACTIF**
- Domaine : Observabilité thermique d’aération
- Rôle : Sécurité physique & anti-épisode zombie
- Fusion : **NON**
- Dépendances externes : **AUCUNE**

Toute évolution nécessite :
- validation humaine,
- traçabilité Arsenal,
- mise à jour contractuelle explicite.

# ==========================================================