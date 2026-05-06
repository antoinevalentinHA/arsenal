# `40_dashboards/deshumidificateur/` — Architecture UI

## Nature du dossier

`deshumidificateur/` est un **dashboard métier spécialisé de régulation locale**, centré sur la décision logique de démarrage, l'état réel matériel et les mesures d'humidité confrontées à des seuils.

Ce n'est ni un cockpit transverse, ni une UI d'observabilité technique. C'est une **UI métier compacte**, fondée sur un triptyque propre :

```
recommandation → état réel → mesure vs seuil
```

---

## Structure implicite identifiée

Le dossier est organisé en **3 familles UI distinctes** :

### A. Décision logique

Exemple : `carte_deshumidificateur_decision_logique`

- Lecture directe du résultat binaire du moteur de décision
- Aucune transformation métier significative
- **Type UI : pure**

→ Carte la plus proche du backend. Très saine doctrinalement.

---

### B. État réel matériel

Exemple : `carte_deshumidificateur_etat_reel`

- Affichage de l'état matériel réel, enrichi par la puissance mesurée
- Production d'une lecture "Actif / Arrêté / Inconnu"
- **Type UI : interprétative** (reformulation sémantique + contexte physique)

→ Matérialise la différence entre ce qui est recommandé et ce qui tourne réellement.

---

### C. Diagnostic capteur / seuil

Exemple : `deshumidificateur_capteur`

- Confrontation de la mesure d'humidité au seuil pertinent
- Seuil dépendant de l'état actif/inactif (hystérésis)
- Routage relatif / absolu selon le référentiel physique disponible
- **Type UI : diagnostic** (qualification d'une situation par rapport à un seuil variable)

→ `deshumidificateur_capteur` constitue la carte pivot du domaine. Aucune autre carte ne doit redéfinir localement la logique de lecture des seuils ON/OFF.

> Sémantique couleur : rouge = situation encore hors seuil / démarrage attendu — vert = seuil atteint / arrêt conforme. Ici, le vert signifie **situation conforme au comportement attendu**, pas "valeur basse".

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                               |
|----------------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| pure           | aucune transformation                                                                            | `carte_deshumidificateur_decision_logique`             |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `carte_deshumidificateur_etat_reel`                    |
| diagnostic     | qualifie une situation par rapport à un seuil ou un état attendu                                | `deshumidificateur_capteur`                            |
| agrégative     | combinaison de plusieurs signaux *(non utilisé dans ce domaine)*                                | —                                                      |
| action         | proxy UI d'une commande backend *(non utilisé dans ce domaine)*                                 | —                                                      |
| info           | traçabilité technique *(non utilisé dans ce domaine)*                                           | —                                                      |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes interprétatives et diagnostic. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Décision   → 10_decision/
Niveau 2 — État réel  → 20_etat_reel/
Niveau 3 — Diagnostic → 30_diagnostic/
```

3 couches — adaptées à la simplicité du domaine.

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/deshumidificateur/

  10_decision/
    carte_deshumidificateur_decision_logique.yaml

  20_etat_reel/
    carte_deshumidificateur_etat_reel.yaml

  30_diagnostic/
    deshumidificateur_capteur.yaml
```

---

## Points de fragilité documentés

### 1. Routage par `entity_id`

Dans `deshumidificateur_capteur`, la branche relative / absolue est déduite par nommage (`_ha_` ou `_absolue`). Acceptable dans Arsenal, fragile si non documenté. À mentionner dans l'entête.

### 2. `hass.states[]` spécifique

Utilisation directe de `hass.states[]` dans le template. Non neutre — à conserver dans les points de fragilité de l'entête.

### 3. Cohérence décision / réel non vérifiée explicitement

Le domaine porte naturellement la question : la recommandation logique et l'état réel concordent-ils ? Aucune carte de cohérence dédiée n'existe à ce stade. Elle ne devient nécessaire que si une divergence durable entre recommandation logique et état réel apparaît comme problème métier.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Remplacer "UI uniquement (aucune décision)" par le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter les points de fragilité**
Ajouter dans l'entête de `deshumidificateur_capteur` : convention de routage par nommage, usage de `hass.states[]`, sémantique couleur vert/rouge.
