# `40_dashboards/sante/` — Architecture UI

## Nature du dossier

`sante/` est un **dashboard de lecture qualitative d'indicateurs personnels**, centré sur l'affichage de KPI santé et activité sous une forme compacte, lisible et non décisionnelle.

Le domaine ne porte ni action, ni diagnostic système, ni cohérence backend / réel, ni pilotage. Il expose uniquement des **KPI qualifiés visuellement**.

La structure du domaine est :

```
valeur → qualification visuelle

  variante A : valeur → couleur backend
  variante B : valeur → couleur fixe informative
```

> Le domaine `sante/` ne produit pas de diagnostic local. Il restitue une lecture qualitative déjà produite en backend.

---

## Structure implicite identifiée

Le dossier est organisé en **2 familles UI distinctes** :

### A. KPI qualitatifs à couleur upstream

Exemples : `carte_activite_calories_quotidiennes`, `carte_activite_distance_quotidienne`, `carte_duree_qualitative`, `carte_frequence_respiratoire_qualitative`, `carte_activite_pas_quotidiens`, `carte_score_qualitatif`

- Affichage d'une valeur KPI avec sémantique couleur entièrement déléguée au backend (`sensor.couleur_sante_*`)
- **Type UI : interprétative** (restitution d'une qualification produite upstream)

> Ces cartes ne calculent pas la qualification — elles consomment une couleur déjà déterminée. Elles sont `interprétative` et non `diagnostic` : aucune logique de détection d'anomalie n'est produite localement.

→ Famille canonique du domaine.

---

### B. KPI informatifs à couleur fixe

Exemple : `carte_duree_ronflements`

- Affichage d'une mesure compacte sans seuil, sans qualification d'alerte, couleur fixe informationnelle
- **Type UI : info**

> Cette carte ressemble visuellement aux KPI qualitatifs mais n'appartient pas à la même famille fonctionnelle. Elle ne consomme aucune sémantique couleur backend.

---

### C. Compteur interprétatif à seuils locaux

Exemples : `carte_ronflements_episodes`, `carte_reveils_nocturnes`

- Compteur entier qualifié par seuils calculés localement (hérités de `carte_compteur_seuils_variables`, sans recopie de la logique de seuil/couleur)
- Libellé explicite au zéro (« Aucun *X* détecté ») au lieu de la valeur brute, pour éviter l'ambiguïté d'un compteur muet à 0 ; valeur brute conservée pour toute valeur strictement positive
- **Type UI : interprétative** (même classification que le générique parent)

> `carte_reveils_nocturnes` habille `input_number.reveils_nocturnes` (domaine `reveils`) ; sa surface UI est co-localisée ici avec le contexte « sommeil », hors périmètre du domaine `reveils` (`contrats/reveils.md` §6). Ce n'est pas une carte santé/Withings, mais son unique surface d'affichage vit dans ce dossier par co-localisation assumée.

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                              |
|----------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| interprétative | KPI avec qualification visuelle portée par le backend, ou compteur à seuils locaux              | `carte_activite_calories_quotidiennes`, `carte_duree_qualitative`, `carte_score_qualitatif`, `carte_ronflements_episodes`, `carte_reveils_nocturnes` |
| info           | KPI informatif sans qualification d'alerte                                                      | `carte_duree_ronflements`                                             |
| pure           | *(non utilisé dans ce domaine)*                                                                  | —                                                                     |
| diagnostic     | *(non utilisé dans ce domaine)*                                                                  | —                                                                     |
| action         | *(non utilisé dans ce domaine)*                                                                  | —                                                                     |

---

## Architecture en couches (lecture système)

```
Niveau 1 — KPI qualitatifs            → 10_kpi_qualitatifs/
Niveau 2 — KPI informatifs            → 20_info/
Niveau 3 — Compteur interprétatif à seuils locaux → 30_diagnostic_seuils/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.

---

## Structure cible recommandée

```
40_dashboards/sante/

  10_kpi_qualitatifs/
    carte_activite_calories_quotidiennes.yaml
    carte_activite_distance_quotidienne.yaml
    carte_duree_qualitative.yaml
    carte_cardio_nuit_synthese.yaml
    cartes_cardio_nuit.yaml
    carte_frequence_respiratoire_qualitative.yaml
    carte_activite_pas_quotidiens.yaml
    carte_score_qualitatif.yaml

  20_info/
    carte_duree_ronflements.yaml

  30_diagnostic_seuils/
    carte_ronflements_episodes.yaml
    carte_reveils_nocturnes.yaml
```

---

## Points de fragilité documentés

### 1. Dépendance forte au backend couleur

La quasi-totalité des cartes consomment une couleur upstream (`sensor.couleur_sante_*`). Toute dérive de ces capteurs se propage directement à l'UI sans signal local d'alerte.

### 2. Ressemblance trompeuse de `carte_duree_ronflements`

Partage l'apparence KPI des autres cartes, mais pas la même famille fonctionnelle. Couleur fixe, non qualitative, non pilotée. À maintenir explicitement dans `20_info/`.

### 3. Homogénéité de la famille qualitative à préserver

Les cartes `socle_kpi + sensor couleur upstream` forment une famille Arsenal cohérente. Toute nouvelle carte santé doit soit rejoindre explicitement cette famille, soit être documentée comme exception.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**

```yaml
# 🧱 TYPE UI : interprétative
```

```yaml
# 🧱 TYPE UI : info
```

**Étape 3 — Documenter la dépendance upstream**
Ajouter dans les entêtes des KPI qualitatifs que la sémantique couleur est entièrement déléguée au backend — toute modification doit passer par les capteurs `sensor.couleur_sante_*`.
