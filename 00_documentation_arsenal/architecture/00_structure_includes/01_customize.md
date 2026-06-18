# Structure — 01_customize

## Rôle

Personnalisation déclarative des entités existantes
(métadonnées, affichage UI, classification).

Aucune logique n’est autorisée.

---

## Doctrine Arsenal

Les fichiers `01_customize/` constituent une couche de présentation pure.

Ils ne doivent contenir :
- ni logique métier,
- ni calcul,
- ni interprétation fonctionnelle,
- ni comportement dynamique.

Leur rôle est exclusivement déclaratif et cosmétique.

---

## Include

```yaml
homeassistant:
  customize: !include_dir_merge_named 01_customize/
```

---

## Structure

```yaml
<entity_id>:
  <cle>: <valeur>
```

---

## Clés supportées

- friendly_name
- icon
- unit_of_measurement
- device_class
- state_class
- unit_class
- entity_category
- translation_key
- suggested_display_precision
- assumed_state
- initial_state
- enabled_by_default
- hidden
- attribution
- options
- device_info

---

## Invariants

- Pas de template Jinja
- Pas de logique conditionnelle
- Pas de dépendance croisée
- Pas de création d’entité
- Pas de documentation métier détaillée
- Pas d’effet fonctionnel sur le système

---

## friendly_name & surfaces d'affichage (Android Auto)

`friendly_name` est l'étiquette **globale** d'une entité. Toute surface qui ne fixe
pas son propre nom la reprend : logbook, historique, notifications, Assist — et
l'interface de conduite **Android Auto**.

- **Android Auto affiche le `friendly_name`** des entités exposées (catégorie
  *Favoris*, configurée dans l'application compagnon, **hors dépôt** — cf.
  [`contrats/meteo/tendance_temperature.md`](../../contrats/meteo/tendance_temperature.md) §2).
  Il **n'utilise jamais** les `name:` des cartes Lovelace.
- **`customize` est la couche Arsenal des libellés courts Android Auto.** Un nom
  trop long pour la conduite se raccourcit ici via `friendly_name`, **jamais** en
  renommant la source (`name:` runtime, `unique_id`, `alias` restent inchangés).
- **Le `name:` d'une carte Lovelace protège le rendu dashboard** : il découple
  l'affichage de la carte du `friendly_name`. Côté Lovelace : [`18_lovelace.md`](18_lovelace.md).

### Procédure avant tout changement de `friendly_name`

1. **Auditer Lovelace** pour les entités concernées : recenser chaque carte qui
   les affiche.
2. **Verrouiller** par un `name:` explicite (figé sur le libellé courant) toute
   carte qui dépend **implicitement** du `friendly_name` — carte sans `name:`,
   série `history-graph` / `mini-graph-card`, socle à `show_name: true`. Sans ce
   verrou, un changement global de `friendly_name` modifie le rendu du dashboard.
3. **Appliquer** le `friendly_name` court en `customize`, une fois les cartes
   verrouillées.

### Invariants

- **Icônes dynamiques : jamais de clé `icon:` en `customize`** sur une entité dont
  l'icône est produite au runtime (familles à icône d'état, notamment les tendances
  thermiques). Une `icon:` statique écraserait l'icône dynamique. Ces entités ne
  reçoivent que `friendly_name` en `customize` (cf. INV-TEND-8,
  [`contrats/meteo/tendance_temperature.md`](../../contrats/meteo/tendance_temperature.md)).
- **Entités miroir dédiées Android Auto : écartées** sauf nécessité forte
  (duplication d'état, charge recorder, exposition supplémentaire — contraires au
  minimalisme Arsenal). Le couple `customize` + verrou `name:` couvre le besoin
  sans entité supplémentaire.

---

## Modèle d’entête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — CUSTOMIZE
#     <Domaine> — <Famille d'entités>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Centraliser les métadonnées d'affichage des entités
#   à destination des consommateurs UI du domaine.
#
# 🧩 PÉRIMÈTRE
#   - Attributs de présentation uniquement (friendly_name, icon…)
#   - Ne calcule aucune valeur
#   - Ne porte aucune logique métier
#   - Ne déclenche aucune action
#
# 🚫 INTERDITS
#   - Modifier une valeur fonctionnelle
#   - Introduire une logique conditionnelle
#   - Documenter ici le modèle métier du domaine
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```