### Rôle

Déclaration des automatisations Home Assistant.

---

### Include

```yaml
automation: !include_dir_merge_list 10_automations/
```

---

### Structure attendue

```yaml
- id: <identifiant>
  alias: <nom_lisible>
  description: <texte_libre>
  mode: <mode>
  trigger:
    - <trigger>
  condition:
    - <condition>
  action:
    - <action | choose>
```

---

### Invariants

- ID fourni par Arsenal
- Pas d’auto-génération
- Pas de dépendance par alias
- Conditions explicites
- Idempotence requise