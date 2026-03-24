# Gouvernance du Niveau 2 — `generiques/`

## 1. Définitions normatives

**Niveau 2 — générique**
Un patron UI transverse, sans couplage métier, réutilisable par paramétrage pur.

**Transverse mutualisé**
Un composant concret réutilisé entre dashboards, fonctionnellement figé. N'est pas "générique" au sens architectural.

**Niveau 3 — métier**
Tout template contenant une entité, un script, un libellé ou une action hardcodés.

**Layout / structure**
Élément utilitaire de mise en page (spacer, alignement, respiration). Ni fonctionnel ni métier.

---

## 2. Règles de classement (normatives)

| # | Règle |
|---|-------|
| R1 | Un template `generiques/` décrit un **pattern UI transverse**, pas un objet concret. |
| R2 | Un composant concret réutilisé entre dashboards va dans `transverses/`, pas dans `generiques/`. |
| R3 | Tout template avec entité / script / libellé / action métier hardcodés est **niveau 3**. |
| R4 | Les composants de layout vivent dans `layout/` ou `structure/`, séparément des cartes fonctionnelles. |
| R5 | La couleur locale n'est autorisée que dans deux cas stricts : seuils locaux explicitement fournis par variables ; conventions transverses canoniques simples (binaire, actif/inactif). Tout mapping spécifique à un domaine ou à un état métier est interdit dans les TPL. |
| R6 | Un template générique ne dépend que de l'entité fournie et de variables explicites. Aucune entité externe ne doit être référencée directement dans un TPL (`states['...']` ou équivalent interdit). Aucune exception n'est autorisée. Toute dépendance externe doit être remontée en variable. |
| R7 | Les variantes comportementales (ex : `_sans_action`) doivent être implémentées par le socle ou par paramétrage. La duplication complète d'un template pour modifier uniquement un comportement est interdite. |
| R8 | Un TPL ne produit qu'un rendu UI. Il ne transforme pas la donnée métier au-delà de sa présentation. |
| R9 | Si un template nécessite une explication pour être classé, alors il n'est pas générique. |

---

## 3. Taxonomie cible

```
socle/                  → structure pure
generiques/             → patrons UI transverses uniquement
transverses/            → composants concrets mutualisés entre dashboards
dashboards/<domaine>/   → spécialisations métier (niveau 3)
layout/                 → spacer, alignement, éléments structurels
```

> La migration physique peut être différée. La doctrine s'applique immédiatement aux nouveaux templates.

---

## 4. Inventaire de décision

### 4.1 Conservés en `generiques/`

- `section_header`
- `sub_section_header`
- `bouton_navigation`
- `bouton_navigation_base`
- `badge_action_confirmee`
- `carte_action_standard`
- `carte_action_critique`
- `carte_bruit_seuils_variables`
- `carte_capteur_seuils`
- `carte_compteur_seuils_variables`
- `carte_mode_binaire_interprete`
- `carte_mode_toggle`
- `kpi_no_action`
- `status_72_info_transitoire`
- `status_72_on_off`
- `carte_alerte_binaire_critique`

### 4.2 À corriger, concept conservé

> Aucun template en attente de correction.

### 4.3 À déplacer vers `transverses/`

- `bouton_accueil_badge_carre`
- `bouton_retour_badge_carre`
- `bouton_diagnostics_badge_carre`
- `bouton_parametres_badge_carre`
- `bouton_navigation_badge_carre`
- `bouton_navigation_dynamique`

### 4.4 À déplacer vers niveau 3 métier

- `carte_action_ecs_bouclage`
- `carte_ecs_bouclage_timer`
- `carte_aeration_blocage_timer`
- `carte_aeration_delta_t_timer`

### 4.5 À déplacer vers `layout/`

- `bouton_spacer`

### 4.6 À fusionner / simplifier (application R7)

- `carte_capteur_seuils_sans_action` — évaluer fusion avec `carte_capteur_seuils` via paramètre `show_action`
- Variantes timer quasi identiques — identifier si un pattern transverse `timer_status` existe. Sinon, assumer explicitement qu'il s'agit de templates métier et les déplacer en niveau 3.

### 4.7 À auditer comme legacy

- `carte_base`

> Non utilisé — suppression autorisée après vérification finale des dépendances. `carte_base_v2` est une base active réelle, présente dans `00_socles/base.yaml` ; elle n'est pas legacy.

---

## 5. Priorités de chantier

| Priorité | Périmètre |
|----------|-----------|
| P1 | Reclassements évidents : métier → `dashboards/`, boutons concrets → `transverses/`, spacer → `layout/`. Pas de renommage, pas de refactor — reclassement pur. |
| P2 | Legacy : vérification finale des dépendances de `carte_base`, puis suppression. |
| P3 | Duplications mineures : variantes `_sans_action`, timers quasi identiques (application R7) |
| P4 | Doctrine couleur : purge des exceptions non gouvernées, en particulier `bouton_navigation_dynamique` (application R5) |

---

## 6. Note prospective — cohérence de nommage

Le mix actuel (`carte_*`, `bouton_*`, `status_*`, `kpi_*`) n'est pas bloquant à court terme mais nuit à la lisibilité systémique. Chantier à planifier en v11+, hors périmètre immédiat.

---

## 7. Condition d'ouverture du niveau 3

L'audit du niveau 3 ne s'ouvre qu'une fois P1 validé et ce document approuvé comme référence stable.
