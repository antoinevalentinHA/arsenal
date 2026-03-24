# `40_dashboards/systeme/` — Architecture UI

## Nature du dossier

`systeme/` est un **dashboard de supervision opérationnelle du socle maison**, centré sur la disponibilité, la stabilité, la connectivité et la santé des composants critiques.

Ce n'est pas un domaine métier utilisateur, ni une UI transactionnelle. C'est une **UI de supervision et d'alerte**, orientée détection d'incident, visibilité de stabilité, lecture de santé synthétique et accès optionnel à une action de remédiation manuelle.

La structure du domaine est :

```
information → statut / santé → diagnostic / supervision → action de remédiation optionnelle
```

---

## Structure implicite identifiée

Le dossier est organisé en **5 familles UI distinctes** :

### A. Information de stabilité

Exemple : `carte_uptime_systeme`

- Uptime transformé en lecture sémantique : bleu si récent, vert si stable
- **Type UI : interprétative** (transformation locale, pas une info neutre)

---

### B. Supervision d'incident / alerte

Exemples : `carte_compteur_alerte`, `systeme_bandeau_stabilite`

- Signalement rapide d'un état d'alerte ou d'instabilité avec forte priorité visuelle
- `systeme_bandeau_stabilite` : fonction de signal prioritaire, pas d'analyse fine
- `carte_compteur_alerte` : compteur transformé en état binaire (`0 = normal`, `> 0 = incident`)
- **Type UI : diagnostic**

---

### C. Diagnostic de connectivité

Exemple : `carte_etat_internet`

- Connectivité instantanée + qualité à 7 jours, classification composite
- Action de remédiation manuelle disponible en hold — secondaire, ne fait pas de cette carte une carte d'action
- **Type UI : diagnostic**

> La carte combine deux horizons temporels (instantané + historique) sous une seule couleur — lecture compacte mais composite. À documenter dans l'entête.

---

### D. Diagnostic d'intégrations

Exemples : `carte_integration_critique`, `netatmo_diagnostic`

- Supervision binaire ou temporelle d'une intégration critique, avec action de récupération optionnelle
- `carte_integration_critique` : **carte canonique générique du domaine** — logique la plus réutilisable (binaire ou âge, seuil, action optionnelle)
- `netatmo_diagnostic` : spécialisation à états textuels normalisés Arsenal
- **Type UI : diagnostic**

> `carte_integration_critique` constitue le socle canonique de supervision d'intégration. Aucune autre carte ne doit redéfinir cette logique. L'action de récupération reste secondaire et conditionnelle — ce template ne doit pas dériver vers une carte d'action déguisée.

---

### E. Santé de sous-système

Exemple : `boiler_status_health`

- Health synthétique multi-états d'un sous-système spécifique
- **Type UI : diagnostic**

> Ce template est cohérent dans `systeme/` comme supervision transversale de santé. À distinguer de `boiler/` : `boiler/` expose l'observabilité interne du sous-système, `systeme/` en expose la santé synthétique depuis l'extérieur.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                                 |
|----------------|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| interprétative | transformation locale tolérée, non source de vérité système                                    | `carte_uptime_systeme`                                                                   |
| diagnostic     | qualifie un état de santé, une cohérence ou une disponibilité                                   | `carte_compteur_alerte`, `systeme_bandeau_stabilite`, `carte_etat_internet`, `carte_integration_critique`, `netatmo_diagnostic`, `boiler_status_health` |
| pure           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                        |
| action         | *(non utilisé dans ce domaine — les remédiations sont secondaires dans les cartes diagnostic)*  | —                                                                                        |
| info           | *(non utilisé dans ce domaine)*                                                                  | —                                                                                        |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Information stabilité    → 10_info_stabilite/
Niveau 2 — Supervision / Alerte     → 20_supervision/
Niveau 3 — Connectivité             → 30_diagnostic_connectivite/
Niveau 4 — Intégrations / Santé     → 40_diagnostic_integrations/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/systeme/

  10_info_stabilite/
    carte_uptime_systeme.yaml

  20_supervision/
    carte_compteur_alerte.yaml
    systeme_bandeau_stabilite.yaml

  30_diagnostic_connectivite/
    carte_etat_internet.yaml

  40_diagnostic_integrations/
    carte_integration_critique.yaml
    netatmo_diagnostic.yaml
    boiler_status_health.yaml
```

> `20_supervision/` et `30_diagnostic_connectivite/` peuvent être fusionnés en une seule couche si la compacité prime. La séparation est recommandée car les deux familles ont des rôles distincts (signal prioritaire vs diagnostic qualifié).

---

## Points de fragilité documentés

### 1. `carte_integration_critique` — hybride action/diagnostic à surveiller

Combine diagnostic et action manuelle optionnelle. Acceptable, car l'action est secondaire et conditionnelle. Ne pas laisser dériver vers une carte d'action déguisée — la finalité reste diagnostique.

### 2. `carte_etat_internet` — deux horizons temporels, une couleur

Mélange connectivité instantanée et qualité historique à 7 jours. Utile, mais composite. À documenter dans l'entête pour éviter une mauvaise lecture.

### 3. `carte_uptime_systeme` — lecture `states[]` directe

Dépendance forte à l'entity sous-jacente. À documenter dans l'entête comme dépendance non découplée.

### 4. `boiler_status_health` dans `systeme/`

Cohérent ici comme vue externe de santé. Risque de doublon conceptuel avec `boiler/` si mal utilisé. La règle : `boiler/` = observabilité interne, `systeme/` = santé synthétique vue de l'extérieur.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Ajouter le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Documenter `carte_integration_critique` comme canonique**
Ajouter dans son entête : rôle canonique de supervision d'intégration, action secondaire et conditionnelle, non généralisable comme carte d'action.

**Étape 4 — Documenter les fragilités**
Ajouter dans les entêtes : dualité temporelle (`carte_etat_internet`), dépendance `states[]` (`carte_uptime_systeme`), frontière `boiler/` vs `systeme/` (`boiler_status_health`).
