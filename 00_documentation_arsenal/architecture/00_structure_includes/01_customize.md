# Structure — 01_customize

## Rôle

Personnalisation déclarative des entités existantes
(métadonnées, affichage UI, classification).

Aucune logique n’est autorisée.

---

## Doctrine Arsenal

Les fichiers `01_customize/` constituent une couche de présentation pure.

Ils ne doivent contenir :
- ni logique métier,
- ni calcul,
- ni interprétation fonctionnelle,
- ni comportement dynamique.

Leur rôle est exclusivement déclaratif et cosmétique.

---

## Include

```yaml
homeassistant:
  customize: !include_dir_merge_named 01_customize/
```

---

## Structure

```yaml
<entity_id>:
  <cle>: <valeur>
```

---

## Clés supportées

- friendly_name
- icon
- unit_of_measurement
- device_class
- state_class
- unit_class
- entity_category
- translation_key
- suggested_display_precision
- assumed_state
- initial_state
- enabled_by_default
- hidden
- attribution
- options
- device_info

---

## Invariants

- Pas de template Jinja
- Pas de logique conditionnelle
- Pas de dépendance croisée
- Pas de création d’entité
- Pas de documentation métier détaillée
- Pas d’effet fonctionnel sur le système

---

## Modèle d’entête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — CUSTOMIZE
#     <Domaine> — <Famille d'entités>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Centraliser les métadonnées d'affichage des entités
#   à destination des consommateurs UI du domaine.
#
# 🧩 PÉRIMÈTRE
#   - Attributs de présentation uniquement (friendly_name, icon…)
#   - Ne calcule aucune valeur
#   - Ne porte aucune logique métier
#   - Ne déclenche aucune action
#
# 🚫 INTERDITS
#   - Modifier une valeur fonctionnelle
#   - Introduire une logique conditionnelle
#   - Documenter ici le modèle métier du domaine
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```