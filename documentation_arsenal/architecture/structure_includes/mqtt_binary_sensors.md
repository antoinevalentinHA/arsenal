### Include

```yaml
mqtt:
  binary_sensor: !include_dir_merge_list mqtt_binary_sensors/
```

---

### Structure

```yaml
- name: <nom_lisible>
  unique_id: <identifiant_unique>
  state_topic: <topic>
  payload_on: <on>
  payload_off: <off>
  device_class: <device_class>
```