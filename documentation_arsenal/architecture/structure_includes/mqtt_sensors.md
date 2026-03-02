### Include

```yaml
mqtt:
  sensor: !include_dir_merge_list mqtt_sensors/
```

---

### Structure

```yaml
- name: <nom_lisible>
  unique_id: <identifiant_unique>
  state_topic: <topic>
  value_template: <jinja>
  icon: <icone>
```