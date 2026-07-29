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

🟨 GÉOMÉTRIE DES GRILLES LOCALES — R-LL-GRID-1 / R-LL-GRID-2

Portée
Ces règles s'appliquent à toute carte `type: grid` de la couche Lovelace
Arsenal, qu'elle soit déclarée dans un dashboard ou dans un include de
`18_lovelace/includes/`. Elles ne s'appliquent qu'aux cartes déclarant
`type: grid`.

Hors périmètre (modèles distincts, non régis par ces règles) :
- `custom:grid-layout` et les géométries CSS `grid-template-columns` ;
- `custom:auto-entities` (nombre d'éléments déterminé au runtime) ;
- `horizontal-stack` ;
- toute structure ne déclarant pas `type: grid`.
Ces structures pourront faire l'objet de règles propres si un besoin est établi.

Cellule directe
La géométrie d'une grille se compte en CELLULES DIRECTES :
- chaque entrée directe de `cards:` compte pour exactement une cellule ;
- une stack, une grille imbriquée ou une carte complexe reste UNE seule
  cellule de la grille parente ;
- un `!include` en entrée directe compte pour une cellule à condition qu'il
  résolve vers une carte-racine unique ;
- le contenu interne d'une cellule n'affecte jamais le nombre de cellules de
  la grille parente.

────────────────────────────────────────────────────────
R-LL-GRID-1 — Grille STATIQUE : complétude structurelle (BLOQUANT)
────────────────────────────────────────────────────────
Une grille est STATIQUE lorsque chacune de ses cellules directes conserve sa
présence dans la géométrie (aucune cellule directe susceptible de disparaître
au runtime).
Toute grille statique DOIT respecter les quatre invariants :
1. `columns` est déclaré explicitement ;
2. `columns` est un entier strictement positif ;
3. `cards` est une liste non vide ;
4. le nombre de cellules directes est divisible par `columns`.
Les grilles à `columns: 1` restent dans le périmètre : leur divisibilité est
triviale, mais les invariants 1 à 3 leur demeurent opposables.

────────────────────────────────────────────────────────
R-LL-GRID-2 — Grille DYNAMIQUE : maîtrise de la géométrie (BLOQUANT)
────────────────────────────────────────────────────────
Une grille est DYNAMIQUE lorsqu'elle contient directement au moins une carte
susceptible de disparaître de la géométrie, notamment `type: conditional`.

Exigence de garantie
Une grille dynamique DOIT garantir, pour TOUTES les combinaisons d'états
admises, un nombre de cellules visibles divisible par `columns` (aucune rangée
partiellement remplie).
Les cardinalités admises sont donc `0`, `columns`, `2 × columns`, etc. Une
cardinalité nulle ne produit aucune rangée incomplète : elle n'est pas, à elle
seule, visée par la présente règle. L'éventuelle interdiction d'une grille
runtime vide constitue un invariant UX distinct, hors du présent périmètre.

Démontrabilité statique
Cette garantie DOIT être statiquement démontrable. Le contrôle ne reconnaît
que des motifs dont la complétude est prouvable sans exécution : il ne simule
jamais les combinaisons d'états Home Assistant.
Lorsque la garantie n'est PAS statiquement démontrable, la grille est NON
CONFORME. Elle doit alors être restructurée en une forme dont la complétude
est démontrable, ou la carte fautive retirée. Il n'existe aucun mécanisme
déclaratif de dérogation ni de qualification manuelle.

Deux mises en garde (ni l'une ni l'autre ne vaut autorisation générale) :
- la divisibilité structurelle du YAML NE PROUVE PAS la complétude visuelle :
  une grille structurellement divisible dont les cellules conditionnelles
  dépendent de conditions INDÉPENDANTES peut afficher une rangée incomplète
  (p. ex. une seule cellule visible dans une grille à 2 colonnes) — elle est
  non conforme ;
- un nombre de cellules structurellement NON divisible peut produire une
  géométrie constante et complète lorsque des cellules conditionnelles sont
  régies par des conditions COMPLÉMENTAIRES sur une même entité (partition
  exhaustive et mutuellement exclusive) : ce motif est un candidat à une
  reconnaissance G2 précise, non une dispense.

Un succès R-LL-GRID-1 ne constitue jamais une preuve R-LL-GRID-2.

Responsabilité de la CI
- R-LL-GRID-1 (grilles statiques) : contrôle bloquant, déterministe, statique.
- R-LL-GRID-2 (grilles dynamiques) : contrôle bloquant, limité aux motifs dont
  la complétude est statiquement démontrable ; tout autre motif dynamique est
  non conforme (à restructurer ou refuser).
- Aucune simulation générale des états Home Assistant.
- Aucun mécanisme de dérogation déclarative ni de qualification manuelle.
- Un succès R-LL-GRID-1 ne prouve jamais R-LL-GRID-2.

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