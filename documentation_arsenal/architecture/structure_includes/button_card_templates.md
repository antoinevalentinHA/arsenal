### Gouvernance / Références normatives

Les templates `button-card` sont des briques UI réutilisables.
Ils relèvent de la gouvernance UI d’Arsenal et sont documentés dans :

- `/homeassistant/documentation_arsenal/ui/architecture.md`

Ce présent document ne décrit que :
- la forme structurelle des fichiers,
- et les règles d’inclusion.

---

### Include

```yaml
button_card_templates: !include_dir_merge_named button_card_templates/
```

---

### Structure

```yaml
<nom_template>:
  <cle>: <valeur>
  styles:
    <section>:
      - <propriete>: <valeur>
```