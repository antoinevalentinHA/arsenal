# `40_dashboards/ouvertures/` — Architecture UI

## Nature du dossier

`ouvertures/` est un **dashboard métier de surveillance d'ouvrants**, centré sur l'état direct des contacts et la qualité de la redondance des capteurs.

Ce n'est pas un domaine de pilotage ni de mesure physique. C'est une **UI de lecture binaire et de diagnostic de fiabilité des ouvrants**.

La structure du domaine est :

```
état contact → diagnostic de redondance
```

---

## Structure implicite identifiée

Le dossier est organisé en **2 familles UI distinctes** :

### A. Capteurs de contact (lecture directe)

Exemple : `contact_sensor`

- Mapping direct : `on = ouvert`, `off = fermé`
- Pas d'agrégation, pas de logique de cohérence
- **Type UI : pure** (lecture binaire directe)

> Les icônes surchargeables via `variables` ne rendent pas cette carte interprétative — c'est une personnalisation d'affichage, pas une transformation métier. La sémantique `on = ouvert` est constitutive du template et ne doit pas être exportée à d'autres binaires sans revalidation.

---

### B. Diagnostic de redondance

Exemple : `diagnostic_redondance_contact`

- Expose une qualification de fiabilité déjà produite par le backend (couleur + résumé)
- Repose sur une convention de nommage forte (triplet de capteurs dérivés)
- **Type UI : diagnostic** (restitution d'une cohérence / santé capteur)

> La carte ne calcule pas la redondance elle-même — elle restitue une qualification déjà produite. Elle reste bien une carte `diagnostic` car elle expose un état de fiabilité, pas un état brut. C'est la carte pivot du domaine.

---

## Taxonomie des types UI

| Type UI        | Signification                                                    | Exemples                           |
|----------------|------------------------------------------------------------------|------------------------------------|
| pure           | lecture directe d'un état binaire                                | `contact_sensor`                   |
| diagnostic     | qualifie la cohérence / fiabilité d'un ouvrant                  | `diagnostic_redondance_contact`    |
| interprétative | *(non utilisé dans ce domaine)*                                  | —                                  |
| action         | *(non utilisé dans ce domaine)*                                  | —                                  |
| info           | *(non utilisé dans ce domaine)*                                  | —                                  |

---

## Architecture en couches (lecture système)

```
Niveau 1 — État contact       → 10_etat/
Niveau 2 — Diagnostic         → 20_diagnostic/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/ouvertures/

  10_etat/
    contact_sensor.yaml

  20_diagnostic/
    diagnostic_redondance_contact.yaml
```

---

## Points de fragilité documentés

### 1. Convention de nommage stricte — point critique du domaine

`diagnostic_redondance_contact` repose sur un triplet dérivé par convention :

```
sensor.diagnostic_redondance_*
sensor.couleur_diagnostic_redondance_*
sensor.resume_diagnostic_redondance_*
```

Toute rupture dans ce nommage casse la dérivation silencieusement, sans erreur visible. À verrouiller contractuellement dans l'entête.

### 2. `contact_sensor` — sémantique non universelle

`on = ouvert` est correct pour les contacts d'ouvrants. Ne pas réutiliser sur un binaire où `on` ne représente pas un état d'ouverture physique.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter les fragilités**
Ajouter dans l'entête de `diagnostic_redondance_contact` : convention de nommage stricte, risque de dérive silencieuse.
