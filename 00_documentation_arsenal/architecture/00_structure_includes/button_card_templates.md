# Structure — button_card_templates

## Rôle

Déclaration des templates `custom:button-card`
réutilisables dans l’interface Arsenal.

Les templates constituent :
- des socles UI,
- des cartes métier,
- des briques de composition,
- des conventions d’affichage,
- des mécanismes de standardisation visuelle.

Ils permettent :
- l’uniformisation graphique,
- la mutualisation des comportements UI,
- la cohérence ergonomique,
- la réduction de duplication Lovelace.

---

## Doctrine Arsenal

Les templates `button-card` appartiennent exclusivement
à la couche UI.

Ils peuvent :
- afficher,
- interpréter visuellement,
- mettre en forme,
- guider l’utilisateur,
- exposer des actions explicites,
- matérialiser des états.

Mais ils ne doivent jamais :
- produire une décision métier,
- contenir une logique système cachée,
- devenir une source de vérité,
- remplacer une automatisation,
- contourner la séparation décision / action / UI.

---

## Gouvernance / Références normatives

Les templates `button-card` relèvent de la gouvernance UI Arsenal.

La doctrine UI complète est documentée dans :

- `/homeassistant/00_documentation_arsenal/ui/architecture.md`

Le présent document décrit uniquement :
- la structure attendue des fichiers,
- les règles d’inclusion,
- les invariants structurels,
- les modèles d’en-tête.

---

## Include

```yaml
button_card_templates: !include_dir_merge_named button_card_templates/
```

---

## Invariants

- Aucun template ne doit produire une décision métier
- Aucun template ne doit piloter directement un équipement
- Toute action utilisateur doit être explicitement visible
- Toute logique métier doit exister hors UI
- Les templates doivent rester composables
- Les socles ne doivent jamais être utilisés directement comme cartes métier
- Toute carte métier doit expliciter son niveau de confiance
- Les couleurs doivent respecter la gouvernance Arsenal
- Les templates ne doivent jamais devenir une source de vérité système

---

## Typologies Arsenal

### Nature des templates

- socle_ui
- carte_metier
- carte_pivot
- carte_satellite
- carte_action
- carte_diagnostic
- carte_interpretative
- carte_navigation
- badge_ui

### Types UI

- statut
- statut_explicatif
- action
- diagnostic
- interpretative
- navigation
- kpi
- synthese
- alerte
- contexte

---

## Structure

```yaml
<nom_template>:

  template:
    - <template_parent>                  # optionnel

  variables:                             # optionnel
    <cle>: <valeur>

  show_name: <true|false>                # optionnel
  show_state: <true|false>               # optionnel
  show_icon: <true|false>                # optionnel

  icon: <icone>                          # optionnel
  name: <nom>                            # optionnel

  tap_action:                            # optionnel
    action: <type>

  hold_action:                           # optionnel
    action: <type>

  double_tap_action:                     # optionnel
    action: <type>

  styles:
    <section>:
      - <propriete>: <valeur>

  custom_fields:                         # optionnel
    <champ>: <valeur>

  state:                                 # optionnel
    - value: <etat>
      styles:
        <section>:
          - <propriete>: <valeur>
```

---

## Clés courantes

- template
- variables
- show_name
- show_state
- show_icon
- icon
- name
- tap_action
- hold_action
- double_tap_action
- styles
- custom_fields
- state

---

## Modèles d’en-tête recommandés

### Socle UI

```yaml
# ==========================================================
# 🧠 ARSENAL — SOCLE UI
#     <Domaine> — <Fonction>
#
# 🔖 NATURE  : socle_ui
# 🖼️ TYPE UI : <type_ui>
# ==========================================================
# 🎯 RÔLE
#   Fournir un socle visuel réutilisable
#   destiné à être dérivé par des cartes métier.
#
# 🧩 PÉRIMÈTRE
#   - Structure graphique et styles mutualisés uniquement
#   - Aucune logique métier
#   - Aucune autorité décisionnelle
#   - Non utilisable directement comme carte métier
#
# 🔗 DÉPENDANCES
#   Néant — socle structurel pur
#
# 🚫 INTERDITS
#   - Embarquer une logique métier locale
#   - Produire une décision
#   - Être utilisé directement sans dérivation
#   - Piloter directement un équipement
#
# 🏷️ STATUT
#   Socle UI — Arsenal v14.x
# ==========================================================
```

### Carte métier

```yaml
# ==========================================================
# 🧠 ARSENAL — CARTE UI
#     <Domaine> — <Fonction>
#
# 🔖 NATURE  : carte_metier
# 🖼️ TYPE UI : <type_ui>
# 🎚️ CONFIANCE : <niveau>
# ==========================================================
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Affichage et interprétation visuelle uniquement
#   - Aucune logique métier exécutive
#   - Aucune autorité système
#
# 🔗 DÉPENDANCES
#   Lit      : <entité principale + attributs utilisés>
#   Template : <socle parent éventuel>
#
# 🚫 INTERDITS
#   - Prendre une décision métier
#   - Remplacer une automatisation
#   - Produire un effet matériel
#   - Devenir une source de vérité système
#
# 🏷️ STATUT
#   Carte UI — Arsenal v14.x
# ==========================================================
```

### Carte action

```yaml
# ==========================================================
# 🧠 ARSENAL — CARTE UI
#     <Domaine> — <Fonction>
#
# 🔖 NATURE  : carte_action
# 🖼️ TYPE UI : action
# 🎚️ CONFIANCE : <niveau>
# ==========================================================
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Déclenchement explicite d'action backend uniquement
#   - Interaction utilisateur visible
#   - Aucune décision embarquée
#
# 🔗 DÉPENDANCES
#   Appelle  : <service déclenché>
#   Template : <socle parent éventuel>
#
# 🚫 INTERDITS
#   - Déclenchement implicite ou automatique
#   - Logique métier locale
#   - Automatisme caché
#   - Piloter directement un équipement sans service intermédiaire
#
# 🏷️ STATUT
#   Carte UI — Arsenal v14.x
# ==========================================================
```

### Carte pivot

```yaml
# ==========================================================
# 🧠 ARSENAL — CARTE UI
#     <Domaine> — <Fonction>
#
# 🔖 NATURE  : carte_pivot
# 🖼️ TYPE UI : synthese
# 🎚️ CONFIANCE : <niveau>
# ==========================================================
# 🎯 RÔLE
#   <Finalité système exacte — une phrase>
#
# 🧩 PÉRIMÈTRE
#   - Synthèse visuelle transverse uniquement
#   - Navigation éventuelle
#   - Aucune décision système
#
# 🔗 DÉPENDANCES
#   Lit      : <agrégations et entités de synthèse>
#   Template : <socle parent éventuel>
#
# 🚫 INTERDITS
#   - Devenir une autorité métier
#   - Embarquer une logique transverse cachée
#   - Être utilisé simultanément comme carte satellite
#
# 🏷️ STATUT
#   Carte UI — Arsenal v14.x
# ==========================================================
```