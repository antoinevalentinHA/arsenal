# `40_dashboards/prises/` — Architecture UI

## Nature du dossier

`prises/` est un **dashboard de pilotage direct d'équipements électriques**, centré sur la commande manuelle de prises connectées.

Le domaine ne porte ni logique métier, ni diagnostic, ni agrégation. Il expose uniquement une **commande utilisateur explicite avec retour d'état réel**.

---

## Structure implicite identifiée

Le dossier contient une seule famille UI :

### Commande de prise

Exemple : `prise_template`

- Toggle ON/OFF avec confirmation modale
- Retour visuel immédiat basé sur l'état réel
- **Type UI : action** (proxy UI d'une commande backend)

> La confirmation modale est constitutive du template. Ne pas la supprimer sans revalidation du risque utilisateur. Le template est volontairement générique — toute logique spécifique (temporisation, dépendance, séquencement) doit être implémentée dans un template dérivé, jamais dans ce template.

---

## Taxonomie des types UI

| Type UI        | Signification                                                  | Exemples          |
|----------------|----------------------------------------------------------------|-------------------|
| action         | commande utilisateur explicite avec effet sur le système réel  | `prise_template`  |
| pure           | *(non utilisé dans ce domaine)*                                | —                 |
| interprétative | *(non utilisé dans ce domaine)*                                | —                 |
| diagnostic     | *(non utilisé dans ce domaine)*                                | —                 |
| info           | *(non utilisé dans ce domaine)*                                | —                 |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action → 10_action/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/prises/

  10_action/
    prise_template.yaml
```

---

## Points de fragilité documentés

### 1. Absence de logique de protection

Le template ne contient ni verrou de sécurité, ni condition métier, ni séquencement. Toute logique de protection doit être implémentée côté backend.

### 2. Confirmation modale — contrainte constitutive

Constitutive du template. Ne pas supprimer sans revalidation explicite du risque utilisateur.

### 3. Généricité du template

Toute spécialisation (temporisation, dépendance, logique conditionnelle) doit être faite dans un template dérivé, pas dans `prise_template` directement.

---

## Plan d'action

**Étape 1 — Déplacer le fichier**
Créer `10_action/` et y placer `prise_template.yaml`.

**Étape 2 — Mettre à jour l'entête**

```yaml
# 🧱 TYPE UI : action
```

**Étape 3 — Documenter les contraintes**
Ajouter dans l'entête : absence de logique de protection, confirmation modale constitutive, template générique non spécialisable en place.
