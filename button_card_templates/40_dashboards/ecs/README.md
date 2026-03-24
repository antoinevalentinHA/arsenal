# `40_dashboards/ecs/` — Architecture UI

## Nature du dossier

`ecs/` est un **dashboard métier compact de gestion sanitaire**, centré sur le pilotage ponctuel, la lecture de statut de fonctionnement / blocage et les KPI thermiques du ballon.

Ce n'est pas une UI d'observabilité transactionnelle comme `boiler/`, ni un domaine de régulation complexe. Le domaine est simple, mais à sémantique métier spécifique : booléen inversé, consigne rabaissée, couleur déléguée upstream.

La structure du domaine est :

```
action → statut → KPI thermique
```

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Actions utilisateur ponctuelles

Exemple : `carte_action_ecs_bouclage`

- Déclenchement explicite via script, avec lecture d'état courante en contexte secondaire
- **Type UI : action** (proxy UI d'une commande backend)

> L'entity n'est pas portée par la carte — action pilotée via script, état lu via `states[]`. Dépendance forte à `switch.prise_bouclage` à documenter dans l'entête. Cette carte constitue une exception d'action avec retour d'état indirect. Elle ne doit pas servir de modèle générique pour les cartes d'action ECS.

---

### B. Statuts métier (fonctionnement / blocage)

Exemple : `ecs_chauffe_planifiee_status`

- Lecture de `input_boolean.ecs_blocage_planifiee` à sémantique inversée : `on = blocage`, `off = fonctionnement normal`
- **Type UI : interprétative** (transformation locale, non source de vérité système)

> La sémantique est inversée par rapport à la lecture naïve. À documenter explicitement dans l'entête — sans quoi la lecture est trompeuse.

---

### C. Synthèses paramétriques compactes

Exemple : `ecs_synthese_status_72`

- Template paramétrique à comportement dépendant de `variables.kind`
- Deux modes : booléen de statut / consigne DHW spéciale à 10 °C (rabaissée)
- **Type UI : interprétative** (traduction métier locale, cas `dhw_setpoint_10` non brut)

> Template multifonction assumé. Les deux sous-comportements sont intentionnels et documentés — ne pas les séparer en deux cartes sans revoir la logique paramétrique.

---

### D. KPI thermique ECS

Exemple : `carte_ecs_etat_ballon`

- Température du ballon avec sémantique couleur entièrement déléguée au backend (`sensor.temperature_ecs_couleur`)
- **Type UI : interprétative** (KPI métier spécialisé, logique visuelle upstream)

> La logique visuelle est sortie du template — propre doctrinalement. En contrepartie, si `sensor.temperature_ecs_couleur` dérive, toute la sémantique UI dérive avec lui.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                              |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| pure           | aucune transformation *(non utilisé dans ce domaine)*                                           | —                                                                     |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `ecs_chauffe_planifiee_status`, `ecs_synthese_status_72`, `carte_ecs_etat_ballon` |
| action         | proxy UI d'une commande backend                                                                  | `carte_action_ecs_bouclage`                                           |
| diagnostic     | qualifie la cohérence du système *(non utilisé dans ce domaine)*                                | —                                                                     |
| info           | traçabilité technique *(non utilisé dans ce domaine)*                                           | —                                                                     |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes interprétatives. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Action  → 10_action/
Niveau 2 — Statut  → 20_statut/
Niveau 3 — KPI     → 30_kpi/
```

3 couches — adaptées à la compacité du domaine.

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/ecs/

  10_action/
    carte_action_ecs_bouclage.yaml

  20_statut/
    ecs_chauffe_planifiee_status.yaml
    ecs_synthese_status_72.yaml

  30_kpi/
    carte_ecs_etat_ballon.yaml
```

---

## Points de fragilité documentés

### 1. `carte_action_ecs_bouclage` — dépendance indirecte

Feedback indirect via `switch.prise_bouclage`. Si ce switch change de nom ou de comportement, la carte perd son observabilité sans avertissement.

### 2. `ecs_chauffe_planifiee_status` — sémantique inversée

`on = blocage`, `off = fonctionnement normal`. Non documenté dans l'entête = lecture trompeuse garantie.

### 3. `carte_ecs_etat_ballon` — dépendance upstream forte

La cohérence de la sémantique couleur dépend entièrement de `sensor.temperature_ecs_couleur`. Toute dérive upstream se propage directement à l'UI sans signal d'alerte.

---

## Frontière avec `boiler/`

`ecs/` et `boiler/` sont deux domaines distincts et complémentaires :

- `ecs/` porte la **lecture métier sanitaire** (pilotage, statut, KPI ballon)
- `boiler/` porte l'**observabilité technique d'exécution** (transactions, ACK, erreurs)

Les deux domaines ne doivent pas se substituer l'un à l'autre. Le domaine ECS ne nécessite ni couche diagnostique dédiée ni couche d'observabilité technique à ce stade.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Remplacer "UI uniquement (aucune décision)" par le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : interprétative
```

**Étape 3 — Documenter les points de fragilité**
Ajouter dans les entêtes : sémantique inversée (`ecs_chauffe_planifiee_status`), dépendance `switch.prise_bouclage` (`carte_action_ecs_bouclage`), dépendance upstream couleur (`carte_ecs_etat_ballon`).
