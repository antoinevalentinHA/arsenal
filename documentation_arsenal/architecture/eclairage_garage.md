# ==========================================================
# 🧠 ARSENAL — ARCHITECTURE
# Éclairage Garage
# ==========================================================
#
# 📌 Statut :
# Document ARCHITECTURE — Document de référence
#
# 📌 Domaine :
# Éclairage — Zones techniques / aveugles / multi-commandes
#
# 📌 Portée :
# Garage et toutes zones similaires présentant :
#   - absence de retour d’état fiable
#   - coexistence commandes physiques / Zigbee / UI / automatismes
#   - topologie va-et-vient ou multi-interrupteurs
#
# ==========================================================

## 🎯 Objet

Ce document définit l’**architecture canonique Arsenal** du sous-système  
**Éclairage Garage**.

Il formalise :

- la chaîne fonctionnelle minimale,
- les autorités hiérarchiques,
- les flux normalisés,
- les interdictions architecturales,
- le modèle de référence pour tous éclairages **sans retour d’état fiable**.

Ce document décrit **l’architecture**.  
Il ne définit pas :

- les politiques horaires,
- les durées d’éclairage,
- les stratégies métiers transverses.

---

## 🧱 Contrainte matérielle structurante

L’éclairage garage est commandé par :

- va-et-vient mécaniques traditionnels,
- boutons physiques type SwitchBot,
- interrupteurs Zigbee partiels,

avec caractéristiques suivantes :

- absence de retour d’état fiable,
- concurrence de plusieurs points de commande,
- incohérence potentielle entre état réel et état perçu.

Conséquence :

> **L’état matériel ne peut jamais être utilisé comme source de vérité.**

---

## 🧠 Principe fondamental de vérité

L’architecture repose sur un principe unique :

### 🔒 Vérité fonctionnelle logique

- Une entité logique unique porte la vérité :
  - `input_boolean.<zone>_light_state`

Ce booléen représente :

- l’état attendu du système,
- la référence fonctionnelle canonique,
- l’unique base de décision.

Interdictions :

- toute lecture de `switch.*` comme état,
- toute correction automatique depuis le matériel,
- toute resynchronisation implicite.

---

## 🧠 Autorité d’action centralisée

### 🔧 Script autoritaire

Chaque zone est gouvernée par :

- `script.<zone>_toggle`

Rôle exclusif :

- appliquer une bascule logique ↔ action physique,
- maintenir la cohérence de l’état logique.

Caractéristiques :

- aucune lecture matérielle,
- aucune vérification d’exécution,
- aucune décision métier.

Interdictions absolues :

- appel direct au matériel ailleurs,
- duplication de logique de bascule,
- pilotage concurrent hors script.

---

## 🧩 Séparation stricte des rôles

L’architecture impose un découplage normatif :

| Couche        | Rôle autorisé                                   |
|---------------|------------------------------------------------|
| Événement     | Produire un fait brut (mouvement, bouton, porte) |
| Autorisation  | Autoriser ou interdire l’automatisme            |
| État          | Porter la vérité logique unique                 |
| Pilotage      | Appliquer la bascule physique                   |
| UI            | Déclencher explicitement                        |

Règle :

> **Aucune entité ne peut porter deux rôles simultanément.**

---

## 🔄 Chaîne fonctionnelle canonique

Flux normalisé :

  Événement physique / UI 
           ↓
  Automation d’interface
           ↓
  Vérification autorisation 
           ↓
  Vérification état logique
           ↓
  Appel script autoritaire 
           ↓ 
  Action physique aveugle 
           ↓
  Mise à jour état logique

Garanties :

- cohérence d’état persistante,
- indépendance matérielle,
- tolérance aux commandes concurrentes.

---

## 🧠 Gestion multi-commandes concurrentes

Le modèle autorise simultanément :

- va-et-vient mécaniques,
- boutons Zigbee,
- UI,
- automatismes.

Règle structurante :

> **Toutes les commandes convergent vers le script autoritaire.**

Aucune commande directe ne peut :

- modifier le matériel hors script,
- écrire l’état logique directement.

---

## 🚫 Interdictions architecturales

Sont strictement interdits :

- lecture d’état depuis `switch.*`,
- pilotage matériel hors script autoritaire,
- automatisations combinant décision + pilotage,
- UI pilotant directement le relais,
- tentative de resynchronisation matérielle,
- recalcul d’état depuis la consommation.

---

## 🔒 Garanties architecture

Cette architecture garantit :

- tolérance aux incohérences matérielles,
- robustesse multi-commandes,
- cohérence persistante,
- indépendance vis-à-vis du matériel,
- extensibilité contrôlée.

---

## 🧩 Modèle de référence Arsenal

Ce document constitue :

- le **modèle canonique Arsenal** pour :
  - éclairages aveugles
  - zones techniques
  - ateliers, caves, couloirs multi-interrupteurs

Toute implémentation future similaire doit :

- respecter cette hiérarchie,
- réutiliser ce schéma,
- s’aligner sur ce contrat.

# ==========================================================
# FIN DOCUMENT ARCHITECTURE — ÉCLAIRAGE GARAGE
# ==========================================================