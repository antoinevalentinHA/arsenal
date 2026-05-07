# Structure — 02_groups

## Rôle

Déclaration de groupes statiques d’entités Home Assistant.

Les groupes servent à agréger plusieurs entités sous une
référence unique afin de simplifier :
- les diagnostics,
- certaines évaluations techniques,
- les consommations transverses.

Un groupe ne porte aucune logique métier.

---

## Doctrine Arsenal

Les groupes constituent une couche d’agrégation statique.

Ils ne doivent contenir :
- ni logique conditionnelle,
- ni calcul,
- ni comportement dynamique,
- ni décision métier.

Un groupe référence uniquement des entités existantes.

---

## Include

```yaml
group: !include_dir_merge_named 02_groups/
```

---

## Structure

```yaml
<nom_groupe>:
  name: <nom_lisible>
  icon: <mdi:icone>   # optionnel
  entities:
    - <entity_id>
```

---

## Invariants

- Pas de groupe dynamique
- Pas de logique métier
- Pas de calcul d’état implicite
- Pas d’usage de `all:`
- Pas d’utilisation comme autorité décisionnelle
- Entités existantes uniquement
- Aucun `entity_id` listé ne doit commencer par `group.`

---

## Modèle d’en-tête recommandé

```yaml
# ==========================================================
# 🧠 ARSENAL — GROUP
#     <Domaine> — <Fonction du groupe>
# ----------------------------------------------------------
# 🎯 RÔLE
#   Regrouper un ensemble cohérent d'entités sous une
#   référence statique unique.
#
# 🧩 PÉRIMÈTRE
#   - Agrégation statique uniquement
#   - Aucune logique métier
#   - Aucun calcul d'état implicite
#   - Aucun comportement dynamique
#
# 🚫 INTERDITS
#   - Introduire une logique conditionnelle
#   - Utiliser le groupe comme autorité décisionnelle
#   - Mélanger des familles fonctionnelles incohérentes
#   - Référencer un group.* comme entité membre
#   - Utiliser la clé all:
#
# 🏷️ STATUT
#   Socle — Arsenal v14.x
# ==========================================================
```