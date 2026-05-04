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
- id: "<identifiant>"
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
- L'ID doit être une chaîne (string), même s'il est numérique
- L'absence de guillemets est interdite (Home Assistant exige un type string)
- Pas d’auto-génération
- Pas de dépendance par alias
- Conditions explicites
- Idempotence requise