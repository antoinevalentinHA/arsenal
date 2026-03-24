# `40_dashboards/chauffage/` — Architecture UI

---

## Nature du dossier

`chauffage/` est un **dashboard métier centré sur le moteur de décision thermique**.

Il expose :

- l’**intention calculée** du système,
- la **réalité physique** (brûleur, état réel),
- les **contraintes externes** (aération, poêle, météo, géofencing),
- les **synthèses diagnostiques globales**,
- les **indicateurs de réglage et de comportement thermique**.

Ce n’est ni une UI simplifiée utilisateur, ni une UI technique brute.

C’est une **UI métier de lecture, de cohérence et de diagnostic thermique**.

---

## Principes structurants

### UI ≠ décision

Aucune carte ne prend de décision.

- la décision est produite par le backend (`sensor.chauffage_mode_calcule`)
- la UI lit, confronte, interprète

---

### Cohabitation intention / réel

Le domaine chauffage repose sur une dualité structurante :

- **intention système**
- **état réel physique**

Certaines cartes lisent l’un, d’autres confrontent les deux.

---

### Contraintes thermiques explicites

Le chauffage est un système contraint :

- aération
- poêle
- géofencing
- météo
- protections thermiques

Ces contraintes sont **visibles en UI**, jamais implicites.

---

### Priorité au réel (dans certaines cartes)

Certaines cartes (ex : synthèse) donnent priorité :

> **au réel physique (brûleur)** sur l’intention

---

## Familles UI identifiées

### 1. Statut métier / intention

Cartes exposant l’état logique du système.

**Type UI : interprétative**

Exemples :

- `carte_chauffage_intention`
- `carte_chauffage_synthese`

Rôle :

- rendre lisible l’intention
- traduire l’état système en langage humain

---

### 2. Diagnostic décisionnel

Cartes évaluant la cohérence ou l’état logique du système.

**Type UI : diagnostic**

Exemples :

- `carte_chauffage_decision`
- `chauffage_diagnostic_global_compact`
- `poele_en_fonction_72`

Rôle :

- confronter intention / réel
- classifier les états
- détecter incohérences et blocages

> `carte_chauffage_decision` est une **carte pivot** du domaine.

---

### 3. Contexte thermique

Cartes exposant les conditions externes influençant la décision.

**Type UI : interprétative / agrégative**

Exemples :

- `chauffage_synthese_blocage_aeration_xl`
- `meteo_favorable_chauffage_72`
- `meteo_chauffage_actuelle_72`

Rôle :

- rendre visibles les contraintes
- expliciter le contexte de décision

---

### 4. Réglage et comportement de courbe

Cartes liées à l’ajustement thermique.

**Type UI : interprétative**

Exemples :

- `chauffage_auto_courbe_status_72`
- `chauffage_reglage_courbe_diag_72`

Rôle :

- afficher état d’auto-ajustement
- diagnostiquer les écarts de consigne

> Aucun calcul métier — lecture uniquement.

---

### 5. Thermostatique par pièce

Cartes de diagnostic local par pièce.

**Type UI : info**

Exemples :

- `thermo_plateau_strict_72`
- `thermo_plateau_affichage_72`
- `thermo_mean_12h_72`
- `thermo_variance_12h_72`

Rôle :

- afficher des indicateurs thermiques par pièce
- permettre l’analyse fine

> Routage dynamique via `input_select.adjustment_piece`.

---

## Taxonomie des types UI

| Type UI | Définition | Présence |
|--------|-----------|----------|
| pure | affichage direct sans transformation | non utilisé ici |
| interprétative | transformation locale non autoritative | majoritaire |
| agrégative | combinaison de plusieurs signaux | partielle |
| diagnostic | qualification de cohérence / état système | cœur du domaine |
| info | information brute ou locale | thermostatique |
| action | déclenchement utilisateur | absent |

---

## Architecture en couches

```text
20_statut_metier/
    ↓
30_diagnostic/
    ↓
40_contexte/
    ↓
50_reglage/
    ↓
60_thermostatique/
````

### Lecture du pipeline

1. **Statut métier**

   * intention et synthèse

2. **Diagnostic**

   * cohérence et classification

3. **Contexte**

   * contraintes externes

4. **Réglage**

   * comportement thermique

5. **Thermostatique**

   * granularité pièce

---

## Structure cible

```text
40_dashboards/chauffage/

  20_statut_metier/
    carte_chauffage_intention.yaml
    carte_chauffage_synthese.yaml

  30_diagnostic/
    carte_chauffage_decision.yaml
    chauffage_diagnostic_global_compact.yaml
    poele_en_fonction_72.yaml

  40_contexte/
    chauffage_synthese_blocage_aeration_xl.yaml
    meteo_chauffage_actuelle_72.yaml
    meteo_favorable_chauffage_72.yaml

  50_reglage/
    chauffage_auto_courbe_status_72.yaml
    chauffage_reglage_courbe_diag_72.yaml

  60_thermostatique/
    thermo_plateau_strict_72.yaml
    thermo_plateau_affichage_72.yaml
    thermo_mean_12h_72.yaml
    thermo_variance_12h_72.yaml
```

---

## Règles spécifiques au domaine

### 1. Décision vs synthèse

* `carte_chauffage_decision` → cohérence intention / réel
* `carte_chauffage_synthese` → lecture humaine consolidée

❌ Non interchangeables

---

### 2. Blocage ≠ erreur

* aération, poêle, absence = blocages **normaux**
* ils ne doivent pas être colorés comme des erreurs critiques

---

### 3. Réel prioritaire dans certaines vues

Le brûleur ON :

→ n’est pas une erreur
→ mais une **activité physique**

---

### 4. Seuils UI non décisionnels

Les seuils dans :

* `chauffage_reglage_courbe_diag_72`
* `meteo_chauffage_actuelle_72`

sont :

> **informatifs uniquement**

---

### 5. Routage dynamique thermostatique

Les cartes thermostatiques reposent sur :

```text
sensor.<nom>_<piece>
```

→ dépendance forte à la convention de nommage

---

### 6. Contexte ≠ décision

Les cartes :

* météo
* aération
* poêle

n’expriment jamais la décision finale.

---

## Cartes pivots

### `carte_chauffage_decision`

```yaml
# ⚠️ CARTE PIVOT : lit intention + état réel + cohérence
```

Rôle :

* point central de vérité UI sur la cohérence

---

### `chauffage_diagnostic_global_compact`

```yaml
# ⚠️ CARTE PIVOT : classification globale multi-signaux
```

Rôle :

* synthèse décisionnelle complète

---

## Plan de conformité

1. Vérifier que chaque template déclare :

```yaml
# 🧱 TYPE UI : ...
```

2. Supprimer :

```yaml
UI uniquement (aucune décision)
```

3. Ajouter :

* marquage des cartes pivot
* contraintes spécifiques dans les entêtes

4. Vérifier :

* aucune carte hybride multi-couches
* respect strict des responsabilités

---

## Positionnement dans l’écosystème Arsenal

| Domaine   | Nature                     |
| --------- | -------------------------- |
| aeration  | contexte décisionnel       |
| chauffage | cœur métier thermique      |
| boiler    | exécution transactionnelle |
| arsenal   | supervision transverse     |

---

## Conclusion

Le domaine `chauffage/` constitue :

> **le cœur métier thermique de l’UI Arsenal**

Il articule :

* intention
* réalité physique
* contraintes
* diagnostic
* réglage
* granularité pièce

Sa complexité est structurelle et justifiée.

Toute simplification excessive détruirait la lisibilité du système.