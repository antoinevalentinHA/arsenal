# Structure — 13_sensor_platforms

## Rôle

Déclaration de capteurs basés sur des plateformes natives Home Assistant.

Ces plateformes servent à :
- agréger des historiques,
- produire des statistiques,
- calculer des tendances,
- exposer des métriques temporelles,
- mesurer des durées,
- compter des occurrences,
- fournir des références quantitatives.

Les plateformes natives constituent une couche de mesure dérivée standardisée.

---

## Doctrine Arsenal

Les plateformes natives représentent une couche de calcul standard Home Assistant.

Elles doivent être privilégiées lorsque :
- le besoin est couvert nativement,
- la plateforme est documentée et stable,
- aucun calcul métier spécifique Arsenal n’est requis.

Une plateforme native peut :
- agréger,
- mesurer,
- compter,
- lisser,
- exposer une statistique.

Mais elle ne doit jamais :
- porter une logique métier,
- piloter un équipement,
- contenir une décision,
- remplacer un template métier spécialisé.

---

## Include

```yaml
sensor: !include_dir_merge_list 13_sensor_platforms/
```

---

## Invariants

- Aucun template Jinja
- Aucun calcul métier spécifique Arsenal
- Utilisation exclusive de plateformes natives documentées
- Toute dépendance au recorder doit être explicitement documentée
- Toute fenêtre temporelle doit être explicitement justifiée
- Toute métrique dérivée doit rester interprétable et traçable
- Aucun capteur de plateforme native ne constitue à lui seul une autorité décisionnelle

---

## Typologies Arsenal

### Statistics

- moyenne_glissante
- mediane_glissante
- tendance
- reference_statistique
- lissage
- agregat_quantitatif

### History stats

- duree_cumulee
- compteur_occurrences
- ratio_temporel
- fenetre_historique
- mesure_glissante
- disponibilite_historique

---

## Structure — statistics

```yaml
- platform: statistics
  name: <nom_lisible>

  entity_id: <entity_id>

  state_characteristic: <caracteristique>

  sampling_size: <valeur>                  # optionnel
  max_age:                                 # optionnel
    hours: <valeur>

  precision: <valeur>                      # optionnel
```

---

## Structure — history_stats

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

## Clés courantes

### statistics

- name
- entity_id
- state_characteristic
- sampling_size
- max_age
- precision

### history_stats

- name
- entity_id
- state
- type
- start
- end

---

## Modèles d’en-tête recommandés

### Statistics

```yaml
# ==========================================================
# 🧠 ARSENAL — STATISTICS SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Produire une statistique dérivée à partir
#   d’une série temporelle existante.
#
# 🧩 PÉRIMÈTRE
#   Type Arsenal :
#   - moyenne_glissante
#   - mediane_glissante
#   - tendance
#   - reference_statistique
#
# 📡 SOURCES
#   - Entité source observée
#
# 🚫 INTERDITS
#   - Introduire une logique métier
#   - Piloter directement un équipement
#   - Confondre statistique et décision
# ==========================================================
```

### History stats

```yaml
# ==========================================================
# 🧠 ARSENAL — HISTORY_STATS SENSOR
#     <Domaine> — <Fonction>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Produire une métrique historique calculée
#   à partir du recorder Home Assistant.
#
# 🧩 PÉRIMÈTRE
#   Type Arsenal :
#   - duree_cumulee
#   - compteur_occurrences
#   - ratio_temporel
#   - disponibilite_historique
#
# 📡 SOURCES
#   - Recorder Home Assistant
#   - Entité observée
#
# 🚫 INTERDITS
#   - Introduire une logique métier
#   - Utiliser un historique incomplet sans justification
#   - Confondre mesure historique et état temps réel
# ==========================================================
```