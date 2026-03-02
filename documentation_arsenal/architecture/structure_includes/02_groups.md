### Rôle

Déclaration de groupes d’entités Home Assistant.

---

### Include

```yaml
group: !include_dir_merge_named 02_groups/
```

---

### Structure

```yaml
<nom_groupe>:
  name: <nom_lisible>
  entities:
    - <entity_id>
```

---

### Invariants

- Pas de hiérarchie imbriquée
- Pas de groupe dynamique
- Entités existantes uniquement