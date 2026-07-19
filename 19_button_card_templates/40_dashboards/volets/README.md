# `40_dashboards/volets/` — Architecture UI

## Nature du dossier

`volets/` est un **dashboard métier de commande et de protection des volets**, centré sur les actions manuelles, les décisions pluie, les gates d'exposition et les indicateurs de protection.

Ce n'est pas un domaine de simple pilotage mécanique, ni un domaine météo pur. C'est une **UI métier de commande + décision de protection**, fortement liée au sous-système pluie.

La structure du domaine est :

```
action → décision pluie → exposition / risque → ciblage / protection
```

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Actions volets

Socle : `shutter_action_base`
Spécialisations finales : `shutter_open`, `shutter_close`

- Socle d'action paramétrable pour montée / descente via `variables`
- Aucune lecture d'état
- **Type UI : action** (proxy UI d'une commande backend)

> `shutter_action_base` est un **socle fonctionnel**, pas une carte métier finale. Il ne doit pas être utilisé directement sans spécialisation.

> Les deux spécialisations finales `shutter_open` / `shutter_close` fixent le libellé, l'icône (grosses flèches ⬆️ / ⬇️) et la couleur de **sens de commande** (montée 🟢 / descente 🔵). Cette couleur est **catégorielle et non décisionnelle** : elle n'exprime aucun état (les volets Bubendorf n'ont aucun retour d'état). Elle est encadrée par la charte couleurs — **Exception 9 (sens de commande des volets)**, sur le modèle de l'Exception 1 (modes HVAC). Le dashboard `principal.yaml` n'utilise que ces deux spécialisations (aucune couleur ni logique inline côté Lovelace).

> ⚠️ **Pas de tuile « stop »** : ces volets (HomeKit, `supported_features = 7`) ne supportent pas `cover.stop_cover`. On n'expose donc pas de commande d'arrêt. L'arrêt existe au niveau matériel (bouton dédié dans Home + Control) mais n'est pas atteignable par HAP.

---

### B. Décisions pluie

Exemples : `decision_pluie_forte_72`, `decision_pluie_recente_72`, `pluie_decision_72`

- Restitution d'états décisionnels pluie produits par le backend, avec lecture de sévérité
- **Type UI : interprétative** (restitution d'une décision upstream)

Deux patterns coexistent :

- `decision_pluie_forte_72` / `decision_pluie_recente_72` : templates mono-sémantique, plus lisibles métier
- `pluie_decision_72` : template fusionné, sévérité déduite depuis `entity_id`

> `pluie_decision_72` est plus générique mais dépend d'une convention de nommage Arsenal stricte. Voir question d'architecture ouverte ci-dessous.

---

### C. Exposition / risque d'ouverture

Exemples : `exposition_fenetres_concernees_ouvertes_72`, `pluie_exposition_resume_72`

- Lecture du risque d'exposition pluie lié aux ouvrants
- `on = rouge = risque` — diagnostic métier, pas un état binaire neutre
- **Type UI : diagnostic** (qualification d'un danger d'exposition)

> Sémantique différente de `clim/` : ici une fenêtre ouverte = rouge = risque, alors que dans `clim/` une fenêtre ouverte pouvait être grise comme contrainte de confort. La divergence est correcte, mais doit être explicitement assumée dans les entêtes.

> `pluie_exposition_resume_72` : toute valeur non vide upstream devient rouge. Robuste côté protection, potentiellement bruité si les valeurs sources changent sans normalisation.

---

### D. KPI de ciblage / protection

Exemple : `pluie_cibles_volets_kpi_72`

- Nombre de volets concernés par la logique pluie : `0 = nominal`, `> 0 = attention`
- **Type UI : interprétative** (indicateur de portée de la logique de protection)

> Ce n'est pas un KPI quantitatif neutre — c'est un indicateur de portée de protection. Sémantique atypique (`0 = vert` est ici un état souhaitable) à documenter dans l'entête.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                                     |
|----------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| action         | commande utilisateur explicite, socle fonctionnel                                               | `shutter_action_base` (socle), `shutter_open`, `shutter_close`                              |
| interprétative | restitution locale d'une décision ou d'un indicateur métier                                    | `decision_pluie_forte_72`, `decision_pluie_recente_72`, `pluie_decision_72`, `pluie_cibles_volets_kpi_72` |
| diagnostic     | qualification d'un risque ou d'une exposition                                                   | `exposition_fenetres_concernees_ouvertes_72`, `pluie_exposition_resume_72`                   |
| pure           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                            |
| info           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                            |

> Les cartes pluie de ce dossier ne sont pas des cartes météo génériques — elles expriment une décision ou un risque dans le contexte spécifique des volets.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action               → 10_action/
Niveau 2 — Décision pluie       → 20_decision_pluie/
Niveau 3 — Exposition / Risque  → 30_exposition/
Niveau 4 — Ciblage / Protection → 40_kpi_protection/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/volets/

  10_action/
    shutter_action_base.yaml
    shutter_open.yaml
    shutter_close.yaml

  20_decision_pluie/
    decision_pluie_forte_72.yaml
    decision_pluie_recente_72.yaml
    pluie_decision_72.yaml

  30_exposition/
    exposition_fenetres_concernees_ouvertes_72.yaml
    pluie_exposition_resume_72.yaml

  40_kpi_protection/
    pluie_cibles_volets_kpi_72.yaml
```

---

## Questions d'architecture ouvertes

### 1. Coexistence `decision_pluie_*` vs `pluie_decision_72`

Deux approches coexistent — mutuellement exclusives à terme :

**Option A — Coexistence assumée**
`decision_pluie_forte_72` et `decision_pluie_recente_72` restent comme cartes explicites lisibles métier. `pluie_decision_72` coexiste comme version générique.

**Option B — Rationalisation**
`pluie_decision_72` devient canonique. Les deux cartes mono-sémantique sont dépréciées.

> Ne pas laisser cette coexistence dériver sans doctrine. Les deux options sont valides, mais doivent être assumées et documentées dans les entêtes des trois cartes.

### 2. `shutter_action_base` — socle vs carte finale — ✅ tranchée

Les spécialisations finales existent désormais dans ce même dossier
(`shutter_open`, `shutter_close`) et sont documentées ci-dessus.
Le socle `shutter_action_base` reste réservé à l'héritage et n'est plus
utilisé directement par les dashboards.

> Pas de `shutter_stop` : l'arrêt n'est pas exposé par la passerelle en HAP
> (`supported_features = 7`), on n'expose donc pas cette commande.

---

## Points de fragilité documentés

### 1. `shutter_action_base` — convention `cover.stop_cover*`

Injection de `entity_id` dans `data` au lieu de `target` pour le service stop. Convention spécifique Home Assistant — rupture silencieuse si HA change ce comportement.

### 2. `pluie_decision_72` — dépendance au nommage

La sévérité rouge / orange dépend de la présence de `pluie_forte` dans `entity_id`. Toute rupture de convention de nommage casse la lecture silencieusement.

### 3. Divergence sémantique fenêtres vs `clim/`

Ici `on = risque = rouge`. Dans `clim/`, une fenêtre ouverte pouvait être grise. Les deux sont corrects dans leur contexte — mais ne pas transférer un template de l'un à l'autre sans revalidation.

### 4. `pluie_exposition_resume_72` — rouge sur valeur non vide

Toute valeur inattendue upstream devient rouge. Protection forte, mais potentiellement bruité si les valeurs sources évoluent sans normalisation.

### 5. `pluie_cibles_volets_kpi_72` — sémantique atypique

`0 = vert` est ici l'état souhaitable. À ne pas confondre avec un KPI quantitatif neutre.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**

```yaml
# 🧱 TYPE UI : interprétative
```

**Étape 3 — Trancher la doctrine pluie**
Choisir Option A ou Option B pour la coexistence `decision_pluie_*` / `pluie_decision_72`. Documenter la décision dans les entêtes des trois cartes concernées.

**Étape 4 — Documenter les conventions critiques**
Ajouter dans les entêtes : convention `cover.stop_cover*`, dépendance nommage `pluie_decision_72`, divergence sémantique fenêtres, rouge sur valeur non vide.
