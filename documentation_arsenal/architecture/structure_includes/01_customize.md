### Rôle

Personnalisation déclarative des entités existantes
(métadonnées, affichage UI, classification).

Aucune logique n’est autorisée.

---

### Include

```yaml
homeassistant:
  customize: !include_dir_merge_named 01_customize/
```

---

### Structure

```yaml
<entity_id>:
  <cle>: <valeur>
```

---

### Clés supportées

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

### Invariants

- Pas de template Jinja
- Pas de logique conditionnelle
- Pas de dépendance croisée
- Pas de création d’entité