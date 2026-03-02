### Rôle

Déclaration de capteurs basés sur des plateformes natives.

---

### Include

```yaml
sensor: !include_dir_merge_list 12_sensor_platforms/
```

---

### Structure — statistics

```yaml
- platform: statistics
  name: <nom_lisible>
  entity_id: <entity_id>
  state_characteristic: <caracteristique>
  sampling_size: <valeur>
```

---

### Structure — history_stats

```yaml
- platform: history_stats
  name: <nom_lisible>
  entity_id: <entity_id>
  state: <etat_mesure>
  type: <type_calcul>
  start: <template_datetime>
  end: <template_datetime>
```

---

### Invariants

- Aucun template
- Aucun calcul métier
- Plateformes documentées uniquement
