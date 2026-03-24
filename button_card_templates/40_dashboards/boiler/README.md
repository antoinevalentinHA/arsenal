# `40_dashboards/boiler/` — Architecture UI

## Nature du dossier

`boiler/` est un **dashboard technique d'exploitation d'un sous-système transactionnel**.

Il ne sert pas à piloter, simplifier ou abstraire. Il sert à **observer, comprendre, diagnostiquer et vérifier l'exécution**. C'est une **UI d'observabilité technique**, pas une UI métier utilisateur.

---

## Structure implicite identifiée

Le dossier est organisé en **6 familles UI distinctes** :

### A. Status fonctionnel (état réel non normatif)

Exemple : `boiler_status_burner`

- État opérationnel brut, sans notion OK/KO, sans jugement
- **Type UI : pure**

> Le brûleur ON n'est pas "tout va bien". Le brûleur OFF n'est pas "problème". La couleur ne porte pas de sémantique normative — elle reflète l'état, pas sa valeur.

Un état fonctionnel ne doit jamais être interprété
comme un état de santé système.

---

### B. Status infrastructure

Exemples : `boiler_status_infra`, `boiler_status_infra_positif`

- Santé technique du système : OK / dégradé / KO
- Mapping direct à sémantique canonique infra
- **Type UI : pure (à convention canonique)**

> La sémantique couleur infra est canonique Arsenal. Elle ne doit pas être modifiée localement. Les templates de status infrastructure et de status fonctionnel sont strictement non interchangeables.

---

### C. Status dégradé (flag spécialisé)

Exemple : `boiler_status_degraded_flag`

- Binaire, sémantique métier spécifique : `off = sain`, `on = dégradé`
- **Type UI : pure (spécialisée)**

> Convention constitutive du template. Isolé du reste pour éviter toute confusion sémantique avec les autres status.

---

### D. Décision transactionnelle

Exemple : `boiler_decision_ack`

- Lecture du cycle transactionnel ACK
- Distinction état intermédiaire vs état final : `accepted ≠ succès`, `applied = succès`
- **Type UI : diagnostic** (lecture de fiabilité d'exécution transactionnelle)

> `boiler_decision_ack` constitue la référence canonique de lecture transactionnelle du système boiler. Aucune autre carte ne doit redéfinir cette sémantique.

→ Cœur sémantique du modèle boiler v11. Carte pivot du domaine transactionnel.

---

### E. Diagnostic erreur

Exemple : `boiler_diagnostic_error`

- Présence d'erreur = critique
- Absence d'erreur ≠ succès (selon implémentation)
- **Type UI : diagnostic**

→ Lecture d'anomalie pure. Non réutilisable comme simple carte de statut.

L'absence d'erreur ne constitue pas une validation système.

---

### F. Information technique

Exemples : `boiler_info_requete`, `boiler_info_timestamp`

- Traçabilité technique : flux de requêtes, horodatage
- Une requête émise n'est ni bonne ni mauvaise en soi
- **Type UI : info** (aucune interprétation superposée)

> Les templates de type `info` ne doivent jamais porter de sémantique de validation, d'erreur ou de succès.

Les templates de type info ne doivent pas intégrer
de seuils ni de logique de classification.

---

### G. KPI techniques

Exemples : `boiler_kpi_consigne`, `boiler_kpi_courbe`, `boiler_kpi_temperature`

- Lecture de valeurs opérationnelles avec seuils informatifs
- **Type UI : interprétative** (transformation locale, non source de vérité système)

Trois natures physiques distinctes au sein de ce bloc :

| KPI         | Nature réelle        |
|-------------|----------------------|
| consigne    | valeur cible         |
| courbe      | paramètre structurel |
| température | mesure physique      |

> Les seuils warning / critique des KPI sont purement informatifs et ne constituent pas une logique décisionnelle. Une mesure physique ne doit jamais être affichée en vert — le vert est réservé aux états normatifs (OK / autorisé).

Les KPI ne doivent jamais être utilisés comme source
de décision dans le système.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                           |
|----------------|--------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| pure           | aucune transformation                                                                            | `boiler_status_burner`, `boiler_status_infra`, `boiler_status_degraded_flag`       |
| interprétative | transformation locale tolérée (affichage, seuils, classification), non source de vérité système | `boiler_kpi_consigne`, `boiler_kpi_courbe`, `boiler_kpi_temperature`               |
| diagnostic     | qualifie la cohérence ou l'état d'exécution du système                                          | `boiler_decision_ack`, `boiler_diagnostic_error`                                   |
| info           | traçabilité technique, sans interprétation                                                      | `boiler_info_requete`, `boiler_info_timestamp`                                     |
| agrégative     | combinaison de plusieurs signaux *(non utilisé dans ce domaine)*                                | —                                                                                  |
| action         | proxy UI d'une commande backend *(non utilisé dans ce domaine)*                                 | —                                                                                  |

> Le libellé "UI uniquement (aucune décision)" présent dans les entêtes est **inexact** pour les cartes diagnostic et interprétatives. Le champ `TYPE UI` ci-dessus remplace cette formulation.

---

## Architecture en couches (lecture système)

```
Niveau 1 — Status fonctionnel     → 10_status/
Niveau 2 — Décision               → 20_decision/
Niveau 3 — Diagnostic             → 30_diagnostic/
Niveau 4 — Information technique  → 40_info/
Niveau 5 — KPI                    → 50_kpi/
```

5 couches — justifiées par la richesse sémantique du domaine transactionnel.

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/boiler/

  10_status/
    boiler_status_burner.yaml
    boiler_status_infra.yaml
    boiler_status_infra_positif.yaml
    boiler_status_degraded_flag.yaml

  20_decision/
    boiler_decision_ack.yaml

  30_diagnostic/
    boiler_diagnostic_error.yaml

  40_info/
    boiler_info_requete.yaml
    boiler_info_timestamp.yaml

  50_kpi/
    boiler_kpi_consigne.yaml
    boiler_kpi_courbe.yaml
    boiler_kpi_temperature.yaml
```

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Remplacer "UI uniquement (aucune décision)" par le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Verrouiller les conventions**
Ajouter dans les entêtes concernés :
- `boiler_status_infra` : sémantique couleur canonique Arsenal, non modifiable localement
- `boiler_status_degraded_flag` : convention `off = sain` constitutive du template
- `boiler_decision_ack` : référence canonique transactionnelle, sémantique non redéfinissable
- `boiler_kpi_temperature` : seuils purement informatifs, non décisionnels — pas de vert sur mesure physique
