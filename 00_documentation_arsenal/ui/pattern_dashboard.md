# 🧠 ARSENAL — UI PATTERN CANONIQUE · Pattern Dashboard — Navigation & Structure Verticale
#
# 📌 Statut :
# DOCUMENT NORMATIF — RÉFÉRENCE UI OFFICIELLE
#
# 📌 Domaine :
# UI / Lovelace / Dashboards
#
# 📌 Portée :
# Définir le **pattern unique autorisé** pour la structure
# des dashboards Arsenal utilisant une navigation de domaine
# et un flux vertical maîtrisé.
#
# Ce document est **contraignant** pour toute création
# ou refonte de dashboard Arsenal.
#
# ==========================================================


## 🎯 OBJECTIF

Ce document définit :

- la structure canonique d’un dashboard Arsenal,
- les règles de gouvernance UI,
- les composants autorisés et interdits,
- le pattern officiel de navigation par domaine.

Finalités :

- alignement vertical parfait entre dashboards,
- comportement responsive stable (mobile / desktop),
- gouvernance centralisée de la navigation,
- maintenabilité long terme,
- cohérence UX globale Arsenal.


---

## 🧱 PRINCIPES FONDATEURS

### 1️⃣ Racine unique obligatoire

Tout dashboard Arsenal DOIT respecter :

- une **seule racine `cards:`**,
- contenant **un seul `vertical-stack`**,
- aucun autre flux parallèle.

Structure minimale obligatoire :

```yaml
cards:
  - type: vertical-stack
    cards:
      - …

Interdictions absolues :

- plusieurs cartes racines
- mélange vertical-stack + horizontal-stack au niveau racine
- flux parallèles Lovelace

### 2️⃣ Flux vertical strict

Règle fondamentale :
Tout dashboard Arsenal est un flux vertical linéaire.

Autorisé :
- vertical-stack (structure principale)
- horizontal-stack (contenu local uniquement)

Interdit :
- grid comme structure principale
- sections
- layout-card
- view_layout
- toute grille servant de squelette global

🟦 NAVIGATION DE DOMAINE — PATTERN OFFICIEL

Principe

Chaque famille fonctionnelle (météo, ECS, chauffage, etc.)
doit disposer :

- d’un fichier de navigation dédié,
- inclus systématiquement en tête de dashboard.

Exemple canon :
- !include ../../includes/navigation/meteo.yaml

Ce fichier constitue :
- la barre de navigation officielle du domaine,
- l’identité visuelle du domaine,
- la source unique de vérité navigation.

Règles de gouvernance navigation

Obligatoire :
- un fichier par domaine :
  navigation/meteo.yaml
  navigation/chauffage.yaml
  navigation/ecs.yaml
  etc. 

Interdit :
- dupliquer une barre de navigation directement dans un dashboard
- redéfinir localement des boutons de domaine
- modifier l’ordre des boutons hors fichier navigation

Objectif :
Toute évolution de navigation doit se faire
dans un seul fichier central.

🧱 STRUCTURE CANONIQUE D’UN DASHBOARD ARSENAL

Structure type officielle

badges:
  - …

cards:
  - type: vertical-stack
    cards:

      # Navigation domaine (OBLIGATOIRE si dashboard métier)
      - !include ../../includes/navigation/<domaine>.yaml

      # Contenu métier
      - section_header
      - cartes
      - sous-sections
      - actions

Ordre strict :
1. badges (si présents)
2. navigation domaine (si applicable)
3. contenu métier uniquement

---

🚫 COMPOSANTS INTERDITS (STRUCTURELS)

Les composants suivants sont formellement interdits
comme structure principale de dashboard :

⛔ sections
- provoque un décalage vertical global
- casse l’alignement badges / cartes
- comportement responsive instable

Interdiction absolue dans Arsenal.


⛔ grid comme squelette principal
Interdit pour :
- structurer un dashboard entier
- positionner des colonnes globales
- remplacer un vertical-stack

Autorisé uniquement :
- à l’intérieur d’un vertical-stack
- pour disposer localement des cartes métier


⛔ Multiples racines

Interdit :
cards:
  - horizontal-stack
  - vertical-stack

Toujours :
cards:
  - vertical-stack

---

🟩 COMPOSANTS AUTORISÉS

Structure principale

vertical-stack   |   🟩 Obligatoire (racine)
horizontal-stack |   🟩 Local uniquement
grid             |   🟡 Local métier uniquement
entities         |   🟩 Autorisé
markdown         |   🟩 Autorisé
conditional      |   🟩 Autorisé


UI Arsenal
- section_header
- cartes button-card Arsenal
- includes navigation
- includes section_headers

---

📐 ALIGNEMENT VERTICAL — RÈGLE FONDAMENTALE

But :
tous les dashboards Arsenal commencent
à la même hauteur visuelle sous les badges.

Garanties :
- suppression totale de sections
- suppression de grid racine
- inclusion navigation en première carte

Résultat :
alignement parfait entre :
- météo
- réglages
- ECS
- chauffage
- clim
- bruit
- diagnostics

---

🧠 EXEMPLE CANON COMPLET — DASHBOARD RÉGLAGES MÉTÉO

cards:
  - type: vertical-stack
    cards:

      - !include ../../includes/navigation/meteo.yaml

      - type: custom:button-card
        template: section_header
        name: 🌡️ Calibration Zigbee

      - type: custom:button-card
        template: carte_action_standard_warning
        entity: script.calibration_capteurs_zigbee
        name: Calibration Zigbee

Ce pattern est désormais référence officielle Arsenal.

---

🧩 EXTENSION DU PATTERN

Ce pattern est applicable à :
- Dashboards métier
- Dashboards réglages
- Dashboards diagnostics
- Dashboards supervision
- Dashboards programmation

Familles concernées :
- Météo
- Chauffage
- ECS
- Climatisation
- Aération
- Alarme
- Bruit
- Energie
- Diagnostics

Spécialisation Réglages :
- Pour les dashboards `reglages/**`, voir le pattern dédié
  [`pattern_dashboard_reglages.md`](pattern_dashboard_reglages.md) (normatif).

---

🔒 RÈGLES DE CONFORMITÉ

Tout nouveau dashboard Arsenal DOIT :
- commencer par un vertical-stack racine
- inclure la navigation domaine si applicable
- n’utiliser aucun sections
- ne jamais utiliser de grid racine
- respecter l’ordre : navigation → contenu métier

Tout dashboard non conforme est :
- instable UI
- non maintenable
- hors gouvernance Arsenal
- sujet à refonte obligatoire

---

🔚 CONCLUSION

Ce pattern constitue :
- la fondation UI d’Arsenal,
- la garantie de cohérence globale,
- un socle de maintenabilité long terme,
- un framework Lovelace maîtrisé.

À partir de ce document :
Arsenal ne construit plus des dashboards.
Arsenal déploie une architecture UI gouvernée.

Fin du document.

==========================================================