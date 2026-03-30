### Include
```yaml
zone: !include_dir_merge_list zones/
```
---
### Structure
```yaml
- name: <nom sans accent, slug = entity_id>
  latitude: <decimal>
  longitude: <decimal>
  radius: <metres>
  icon: <icone>
  passive: <true|false>
```