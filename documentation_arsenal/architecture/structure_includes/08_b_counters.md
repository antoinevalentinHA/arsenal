# 📁 `homeassistant/documentation_arsenal/architecture/structure_includes/08b_counters.md`

## Déclaration d'inclusion

```yaml
counter: !include_dir_merge_named 08b_counters/
```

## Gabarit de fichier inclus

```yaml
<nom_counter>:
  name: <nom_lisible>
  initial: <valeur_initiale>
  step: <pas_increment>
  icon: <mdi_icon>
```

---

## Exemple de fichier attendu

> Analogie avec le gabarit `08_timers` :

**Déclaration d'inclusion**

```yaml
timer: !include_dir_merge_named 08_timers/
```

**Gabarit de fichier inclus**

```yaml
<nom_timer>:
  name: <nom_lisible>
  duration: "HH:MM:SS"
  restore: <true|false>
```
