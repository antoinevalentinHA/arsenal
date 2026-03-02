### Rôle

Déclaration de scripts Home Assistant exécutables.

---

### Include

```yaml
script: !include_dir_merge_named 09_scripts/
```

---

### Structure

```yaml
<nom_script>:
  alias: <nom_lisible>
  mode: <mode>
  sequence:
    - <action | condition | choose>
```

---

### Invariants

- Pas de logique décisionnelle globale
- Pas d’appel circulaire
- Idempotence requise