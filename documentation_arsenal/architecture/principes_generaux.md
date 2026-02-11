# ==========================================================
# ⏱️ Robustesse au rechargement YAML
# ==========================================================

## 🧠 Principe fondamental

Dans l’architecture Arsenal, un **rechargement complet de la configuration YAML**
(Home Assistant restart ou reload global) est considéré comme :

→ **un test structurel volontaire de robustesse**,  
et non comme un événement exceptionnel ou tolérable.

Toute erreur apparaissant de manière fiable lors d’un reload
est interprétée comme le symptôme d’une **dette de conception réelle**.


## 🔍 Problème identifié (comportement Home Assistant)

Lors d’un rechargement global :

- Home Assistant évalue immédiatement les blocs `choose`
  et leurs conditions associées
- Certaines entités peuvent ne pas être encore enregistrées
  ou disponibles à cet instant

Toute utilisation de :

- `condition: state`
- ciblant une entité non garantie présente au reload

entraîne alors des erreurs systématiques du type :

- `unknown entity …`

Ce comportement est **déterministe**, reproductible,
et indépendant du fonctionnement nominal du système.


## ✅ Doctrine Arsenal

Les règles suivantes sont **désormais invariantes** :

- AUCUN `condition: state` dans un bloc `choose`
  lorsque l’existence de l’entité n’est pas strictement garantie
  au moment du reload

- Utilisation systématique de conditions `template`
  basées sur :
  - `states('…')`
  - comparaisons tolérantes aux états :
    • `unknown`
    • `unavailable`

- Toute automation doit être :
  - fonctionnelle en régime normal
  - ET structurellement saine au reload YAML


## 🧱 Conséquence architecturale

- Une automation peut sembler correcte en fonctionnement courant
  tout en étant architecturale­ment fragile
- Le reload YAML devient un **outil de diagnostic volontaire**
- Une erreur au reload n’est jamais considérée comme bénigne


## 🧩 Cas d’application canonique

Ce principe a notamment conduit à la correction de :

- Automations de gestion temporelle
- Automations à timers longs
- Automations d’absence prolongée

où des conditions `state` ont été remplacées par des
templates tolérants, éliminant définitivement
les erreurs post-rechargement.


## 🧠 Principe Arsenal renforcé

> Un système robuste ne se juge pas uniquement
> à son fonctionnement nominal,
> mais à sa capacité à se reconstruire proprement
> dans un état cohérent après redémarrage.

Ce principe s’applique **à l’ensemble du système Arsenal**,
tous domaines confondus.
