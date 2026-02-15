## 🧱 SOCLES UI — Inventaire & catégorisation (V1) — Actions

### Socle : `socle_action_simple`
- Type : **SOCLE_ACTION / ACTION_TILE (72px)**
- Cible catalogue : **TPL-06 — tpl_tile_action** (variante “simple / volontaire”)
- Profil UI :
  - Affiche : **icon + name**
  - Masque : **state + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none) → l’action est fournie par la carte dérivée
- Severity / couleur :
  - **OFF/Repos** canon : `rgba(158, 158, 158, 0.2)` (gris neutre)
- Usage typique (couverture) :
  - **Navigation tiles** (menu), **Volets** (Ouvrir/Fermer), **NAS commandes** (si non-confirmées), **Eclairage** (actions directes)

---

### Socle : `socle_action_simple_sans_couleur`
- Type : **SOCLE_ACTION / ACTION_TILE (72px) — STRUCTUREL**
- Cible catalogue : **TPL-06 — tpl_tile_action** (variante “structurelle / neutre”)
- Profil UI :
  - Affiche : **icon + name**
  - Masque : **state + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none)
- Severity / couleur :
  - **Aucune** (ne fixe pas de `background-color`)
- Usage typique (couverture) :
  - Socle de base pour cartes métier qui imposent leur fond (ex : `bouton_navigation`)

---

### Socle : `socle_action_critical`
- Type : **SOCLE_ACTION_CRITIQUE / ACTION_TILE (72px)**
- Cible catalogue : **TPL-06 — tpl_tile_action** (variante “critique”)
- Profil UI :
  - Affiche : **icon + name**
  - Masque : **state + label**
  - Actions : **neutralisées** (tap/hold/double_tap = none) → carte dérivée impose action + confirmation
- Différences vs `socle_action_simple` :
  - **name font-weight: 600** (signal visuel de criticité)
- Severity / couleur :
  - **OFF/Repos** canon : `rgba(158, 158, 158, 0.2)`
- Usage typique (couverture) :
  - **Commandes système** (reboot, arrêt, actions “dangereuses”), actions domotiques à risque (ECS, chauffage, etc.) quand confirmation obligatoire

---

### Socle : `socle_action_label_compact`
- Type : **SOCLE_ACTION_LABEL / ACTION_TILE + FEEDBACK_LABEL (72px)**
- Cible catalogue : **TPL-06 — tpl_tile_action** (variante “action + feedback court”)
- Profil UI :
  - Affiche : **icon + name + label**
  - Masque : **state**
  - Actions : non fixées (hérite des défauts `carte_base_v2` si non override)
- Spécificité :
  - Label renforcé (lisibilité) :
    - `font-size: 14px`, `line-height: 1.3`, `color '#111'`
- Usage typique (couverture) :
  - Actions avec **retour textuel** type “Dernière exécution…”, “Seuil…”, “Δ …”, “Mode …”, sans exposer un état binaire

---

### Socle : `socle_action_script_confirme`
- Type : **SOCLE_ACTION_CONFIRMEE / ACTION_TILE + CONFIRM + FEEDBACK_STATE**
- Cible catalogue : **TPL-06 — tpl_tile_action** (variante “script/service confirmé”)
- Profil UI :
  - Affiche : **icon + name**
  - Masque : **state**
  - Action : **call-service + confirmation** (texte : “Confirmer l’action ?”)
  - Feedback visuel via `state` :
    - `on`  → **OK** `rgba(76, 175, 80, 0.2)`
    - `off` → **OFF/Repos** `rgba(158, 158, 158, 0.2)`
- Remarque de taxonomie :
  - C’est une **action** (TPL-06) avec **retour d’état** codé couleur (sans afficher le state).
- Usage typique (couverture) :
  - Scripts “bouton” avec **ack** (ex : remédiation, relance, actions ponctuelles) + indicateur ON/OFF

---

## Synthèse — rattachement au catalogue (templates)
- **TPL-06 / TILE_ACTION**
  - `socle_action_simple` : variante “action volontaire”
  - `socle_action_simple_sans_couleur` : variante “structurelle / sans fond”
  - `socle_action_critical` : variante “action critique”
  - `socle_action_label_compact` : variante “action + feedback label”
  - `socle_action_script_confirme` : variante “action confirmée + feedback ON/OFF”
