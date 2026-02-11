# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     AÉRATION — PÉRIMÈTRE STRICT
# ==========================================================

# ----------------------------------------------------------
# 📌 STATUT CONTRACTUEL
# ----------------------------------------------------------
#
# - Nature :
#     CONTRAT NORMATIF DE DOMAINE — ACTIF
#
# - Domaine :
#     Chauffage / Climatisation (mode HEAT uniquement)
#
# - Autorité :
#     Ce contrat est opposable à toute implémentation YAML,
#     automatisation, script ou capteur lié à :
#       • l’aération physique,
#       • au blocage thermique associé,
#       • au post-traitement thermique.
#
# - Hiérarchie :
#     Subordonné à :
#       /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#     Indépendant de :
#       • décision centrale chauffage,
#       • offsets thermiques,
#       • présence / absence,
#       • UI et pédagogie.
#
# ----------------------------------------------------------


## 🎯 OBJET DU CONTRAT

Ce contrat définit **exclusivement** le comportement normatif du système Arsenal
lors d’un **épisode d’aération physique** impactant la régulation thermique.

Il encadre **uniquement** :

- la détection d’un épisode d’aération,
- son cycle de vie (début → fin → post-traitement),
- le **blocage thermique associé** :
  - du **chauffage**,
  - de la **climatisation en mode HEAT uniquement**,
- la temporalité et les garde-fous liés à cet épisode.

👉 Toute autre logique liée à l’aération est **explicitement hors périmètre**.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- l’ouverture et la fermeture d’ouvrants (fenêtres / portes),
- la qualification d’un **épisode d’aération**,
- la prise de **snapshots thermiques de référence**,
- le **blocage temporaire du chauffage**,
- l’analyse différée de la **chute thermique réelle (ΔT)**,
- la levée ou la prolongation du blocage,
- la robustesse face aux redémarrages et incohérences d’état.

---

## 🚫 HORS PÉRIMÈTRE EXPLICITE

Ce contrat **NE COUVRE PAS** :

- la recommandation d’aérer (hygrométrie, CO₂, météo, saison),
- les capteurs `aeration_preferable_*`,
- toute aide à la décision utilisateur,
- toute logique UI ou pédagogique,
- tout redémarrage ou forçage du chauffage,
- toute interaction avec la climatisation hors **mode HEAT**.

Ces aspects feront l’objet de **contrats distincts**.

---

## 🧠 CONCEPT FONDAMENTAL : ÉPISODE D’AÉRATION

Une aération est modélisée comme un **épisode atomique** :

- borné dans le temps,
- non fusionnable avec un autre épisode,
- disposant de références thermiques figées à son démarrage.

Un épisode est :
- **créé** à l’ouverture confirmée,
- **clôturé** à la fermeture complète,
- **analysé** après stabilisation,
- **désarmé** définitivement en fin de cycle.

Aucun état intermédiaire ambigu n’est autorisé.

---

## 🔁 MACHINE À ÉTATS NORMATIVE

### M1 — Début d’aération
Conditions :
- système stable,
- aucun épisode en cours,
- ouverture détectée (immédiate ou différée).

Effets normatifs :
- armement de l’épisode,
- horodatage de début,
- snapshots des températures de référence,
- armement explicite du pipeline.

---

### M2 — Fin d’aération
Conditions :
- épisode actif,
- fermeture complète confirmée,
- pipeline armé.

Effets normatifs :
- clôture de l’épisode,
- **activation immédiate du blocage chauffage**,
- programmation :
  - d’un délai minimal de blocage,
  - d’une analyse différée du ΔT,
- aucun redémarrage thermique.

---

### M3 — Analyse ΔT différée
Conditions :
- délai de stabilisation écoulé,
- pipeline toujours armé,
- absence de réouverture récente.

Principe :
- le ΔT mesure **uniquement le manque thermique**,
- il **n’est jamais** un critère de redémarrage.

Effets normatifs :
- calcul du ΔT maximal global,
- décision :
  - prolongation du blocage,
  - ou levée définitive.

---

### M4 — Fin de blocage horaire (filet de sécurité)
Conditions :
- blocage actif,
- analyse ΔT échue ou neutralisée.

Effets normatifs :
- levée du blocage,
- neutralisation des horodatages,
- désarmement final du pipeline.

---

### M5 — Réouverture pendant blocage
Rôle :
- **informatif uniquement**.

Effets normatifs :
- horodatage de la réouverture,
- protection contre une analyse ΔT prématurée,
- aucune modification du blocage en cours.

---

## 🛑 INVARIANTS ABSOLUS

Il est **strictement interdit** que :

- le chauffage redémarre directement suite à une aération,
- une analyse ΔT déclenche une action thermique,
- un épisode survive sans :
  - ouverture,
  - blocage,
  - pipeline armé.

Le contrat impose :
- **blocage uniquement**, jamais de reprise,
- **désarmement obligatoire** en fin de cycle.

---

## 🧩 SÉPARATION DES RESPONSABILITÉS

- Les **automatisations d’aération** :
  - détectent,
  - temporisent,
  - bloquent,
  - analysent.

- Le **script de décision centrale chauffage** :
  - est l’unique autorité de reprise thermique,
  - consomme passivement l’état de blocage,
  - n’est jamais appelé par le pipeline d’aération.

Aucune dépendance circulaire n’est autorisée.

---

## 🛡️ ROBUSTESSE & SÉCURITÉ

Le système garantit :

- aucune persistance de blocage après reboot,
- aucun pipeline « zombie »,
- aucune activation thermique indésirable,
- compatibilité avec restaurations partielles.

Des garde-fous dédiés assurent :
- la neutralisation des horodatages obsolètes,
- la cohérence post-démarrage.

---

## 📌 PORTÉE CONTRACTUELLE

Ce document constitue la **référence normative unique**
pour toute évolution liée à :

- l’aération physique,
- le blocage chauffage associé,
- la temporalité post-aération.

Toute extension fonctionnelle devra :
- soit créer un **nouveau contrat**,
- soit faire l’objet d’une **fusion contractuelle ultérieure explicite**.

---

## ✅ STATUT

- Contrat normatif : **ACTIF**
- Périmètre : **STRICT**
- Fusion : **NON**
- Dépendances externes : **AUCUNE**

# ==========================================================