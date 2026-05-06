# `40_dashboards/mouvements/` — Architecture UI

## Nature du dossier

`mouvements/` est un **mini-domaine de lecture binaire de présence locale**, centré sur l'affichage d'états de capteurs de mouvement.

Le domaine ne porte ni action, ni diagnostic, ni agrégation, ni logique de décision. Il expose uniquement une **lecture directe d'un état de mouvement**.

---

## Structure implicite identifiée

Le dossier contient une seule famille UI :

### Statut binaire de mouvement

Exemple : `carte_mouvement`

- Lecture directe d'un `binary_sensor` de mouvement
- **Type UI : pure** (aucune transformation)
- Sémantique : `on` → mouvement détecté / `off` → calme / `unknown/unavailable` → indisponible

> La sémantique `on = rouge` est constitutive du template. Ne pas réutiliser sur un capteur où `on` représente un état souhaité ou neutre.

---

## Taxonomie des types UI

| Type UI        | Signification                                              | Exemples          |
|----------------|------------------------------------------------------------|-------------------|
| pure           | aucune transformation                                      | `carte_mouvement` |
| interprétative | *(non utilisé dans ce domaine)*                            | —                 |
| diagnostic     | *(non utilisé dans ce domaine)*                            | —                 |
| action         | *(non utilisé dans ce domaine)*                            | —                 |
| info           | *(non utilisé dans ce domaine)*                            | —                 |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Statut → 10_statut/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/mouvements/

  10_statut/
    carte_mouvement.yaml
```

---

## Points de fragilité documentés

### 1. Sémantique `on = rouge` — convention constitutive

Convention non universelle. Ne pas réutiliser sur un capteur dont l'état `on` n'est pas sémantiquement une détection indésirable.

### 2. Nom seul porteur d'information

`show_state` et `show_label` sont désactivés. Toute l'information utile est portée par le nom et la couleur — le nommage de l'instance est donc critique.

---

## Plan d'action

**Étape 1 — Déplacer le fichier**
Créer `10_statut/` et y placer `carte_mouvement.yaml`.

**Étape 2 — Mettre à jour l'entête**

```yaml
# 🧱 TYPE UI : pure
```

**Étape 3 — Documenter la convention**
Ajouter dans l'entête que `on = rouge` est une convention constitutive non réutilisable sans revalidation de la sémantique.
