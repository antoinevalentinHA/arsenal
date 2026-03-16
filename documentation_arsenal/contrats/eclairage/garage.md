# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER PRINCIPAL
# Éclairage Garage
# ==========================================================
#
# 📌 Statut :
# CONTRAT MÉTIER PRINCIPAL — Domaine Éclairage aveugle
#
# 📌 Domaine :
# Éclairage — Zones sans retour d’état fiable
#
# 📌 Portée :
# Garage et zones similaires :
#   - va-et-vient physiques
#   - boutons Zigbee / SwitchBot
#   - coexistence manuel / automatique / UI
#
# ==========================================================

## 🎯 Objet du contrat

Ce contrat définit les **règles normatives obligatoires**  
régissant le sous-système **Éclairage Garage**.

Il formalise :

- les invariants de vérité,
- les autorités contractuelles,
- les droits et interdictions,
- les garanties de cohérence,
- les interfaces autorisées.

Ce contrat est :

- principal pour ce domaine,
- référence pour tous cas analogues Arsenal.

---

## 🔒 Invariant 1 — Vérité fonctionnelle unique

### Définition

La seule source de vérité autorisée est :

- `input_boolean.<zone>_light_state`

Règles :

- cet état représente l’état attendu du système,
- il est persistant,
- il est contractuellement prioritaire.

Interdictions :

- lecture d’état matériel comme vérité,
- recalcul depuis relais, consommation ou Zigbee,
- correction automatique depuis le matériel.

---

## 🔒 Invariant 2 — Autorité d’action unique

### Définition

Le seul point de pilotage autorisé est :

- `script.<zone>_toggle`

Droits exclusifs :

- commander le matériel,
- mettre à jour l’état logique.

Interdictions absolues :

- appel direct à `switch.*` hors script,
- duplication de logique de bascule,
- pilotage concurrent.

---

## 🔒 Invariant 3 — Séparation contractuelle des rôles

Chaque entité appartient à une catégorie unique :

| Catégorie     | Rôle autorisé                        |
|---------------|--------------------------------------|
| Événement     | produire un fait brut                |
| Autorisation  | autoriser / interdire l’automatisme  |
| État          | porter la vérité logique             |
| Pilotage      | appliquer l’action physique          |
| Interface     | déclencher volontairement            |

Règle :

> **Aucune entité ne peut cumuler deux rôles contractuels.**

---

## 🔒 Invariant 4 — Aveuglement matériel volontaire

Le système est contractuellement :

- aveugle à l’état réel,
- indépendant du relais,
- non synchronisé matériellement.

Interdictions :

- lecture de retour d’état,
- tentative de resynchronisation,
- validation d’exécution,
- correction post-action.

---

## 🔒 Invariant 5 — Concurrence multi-commandes autorisée

Le système doit accepter simultanément :

- commandes mécaniques,
- boutons Zigbee,
- UI,
- automatisations.

Règle :

- toutes les commandes passent par le script autoritaire,
- l’état logique reste l’unique référence.

---

## 🧠 Règles d’autorisation automatique (Garage)

L’automatisme d’éclairage du garage est gouverné par **deux garde-fous cumulatifs** :

- `input_boolean.garage_auto_light`
  → autorisation globale de l’automatisme

- `binary_sensor.garage_allumage_auto_autorise`
  → autorisation contextuelle d’allumage (luminosité locale)

La décision repose sur la luminosité mesurée localement
dans le garage (sensor.luminosite_garage_illuminance)
comparée au seuil configuré via :

input_number.garage_seuil_luminosite_allumage_auto

Règles :

- si `input_boolean.garage_auto_light = off` :
  - aucune automation ne peut demander une action (allumage ou extinction)

- si `input_boolean.garage_auto_light = on` :
  - l’extinction automatique peut être autorisée sous conditions d’état
  - l’allumage automatique est autorisé **uniquement si**
    `binary_sensor.garage_allumage_auto_autorise = on`

---

### Catégorie contractuelle

`binary_sensor.garage_allumage_auto_autorise` appartient à la catégorie :

| Catégorie    | Rôle autorisé                         |
|--------------|---------------------------------------|
| Autorisation | autoriser / interdire l’allumage auto |

Règle :

> Ce capteur ne pilote rien et ne modifie aucun état.

---

### Interdictions

`binary_sensor.garage_allumage_auto_autorise` ne doit jamais :

- appeler `script.garage_toggle`
- piloter un `switch.*`
- écrire `input_boolean.garage_light_state`
- contenir une logique de temporisation

Il agit uniquement comme **garde d’autorisation**.

---

## 🧠 Règles de bascule

Toute bascule doit :

- lire l’état logique courant,
- appliquer une action physique aveugle,
- mettre à jour l’état logique correspondant.

Interdictions :

- bascule sans mise à jour d’état,
- écriture d’état sans action physique,
- double écriture concurrente.

---

## 🧠 Règles d’allumage automatique

Conditions minimales :

- autorisation automatique active,
- état logique actuellement OFF,
- événement physique valide.

Garanties :

- aucune décision métier portée ici,
- aucune temporisation incluse,
- aucune politique globale.

---

## 🧠 Règles d’extinction automatique

Conditions minimales :

- autorisation automatique active,
- état logique actuellement ON,
- absence prolongée confirmée.

Règles :

- extinction uniquement par script autoritaire,
- aucune réactivation implicite,
- aucune stratégie transversale intégrée.

---

## 🧩 Interfaces autorisées

Interfaces contractuellement valides :

- boutons MQTT Zigbee
- UI appelant le script
- automatisations événementielles
- automatisations temporisées

Obligation :

- toute interface appelle exclusivement le script autoritaire.

---

## 🚫 États et comportements interdits

Sont contractuellement interdits :

- état logique incohérent avec dernière action,
- pilotage matériel hors script,
- correction d’état depuis matériel,
- automatisme sans autorisation,
- cumul décision + pilotage dans une automation.

---

## 🔒 Garanties contractuelles

Ce contrat garantit :

- cohérence persistante multi-commandes,
- robustesse face aux incohérences matérielles,
- indépendance complète du matériel,
- extensibilité contrôlée,
- compatibilité humaine (manuel + automatique).

---

## 🧩 Réutilisation normative

Ce contrat constitue :

- la référence Arsenal pour :
  - éclairages aveugles
  - zones techniques
  - ateliers, caves, couloirs multi-interrupteurs

Toute implémentation analogue doit :

- respecter ces invariants,
- réutiliser ce modèle,
- ne jamais affaiblir ces garanties.

# ==========================================================
# FIN CONTRAT MÉTIER PRINCIPAL — ÉCLAIRAGE GARAGE
# ==========================================================