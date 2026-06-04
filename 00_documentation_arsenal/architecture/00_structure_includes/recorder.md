# Include — recorder.yaml

```yaml
recorder: !include recorder.yaml
```

```yaml
auto_purge: <true|false>
purge_keep_days: <jours>
commit_interval: <secondes>

include:
  entities:
    - <entity_id>
```