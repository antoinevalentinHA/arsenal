# CONTRAT ARSENAL — DOMAINE VACANCES

**Version** : 1.4.0
**Statut** : Normatif — Clos
**Domaine** : `vacances`
**Dépendances** : `presence`, `mode_maison`, `visite`
**Dépendance transverse** : `system/integrite_reglages` — convention `binary_sensor.parametres_invalides_*`
**Dernière révision** : 2026-04

---

## 1. Objet

Le domaine Vacances gouverne un contexte global d'absence prolongée.

Il permet au système Arsenal de :

- représenter une **demande** de mode Vacances,
- déterminer si cette demande est **effectivement réalisée** sur le terrain,
- exposer cette information de manière **explicable et traçable**,
- appliquer un **contexte global cohérent** à l'entrée et à la sortie du mode.

**Ce domaine ne confond jamais :**

| Niveau | Nature |
|--------|--------|
| Paramétrage | Configuration et intentions utilisateur |
| Support temporel | Matérialisation de la fenêtre planifiée par orchestration |
| Demande | Vérité calculée de la demande métier |
| Effectivité | Vérité terrain consolidée |
| Application de contexte | Conséquences globales sur la maison |

> **Séparation de responsabilités** : ce domaine répond aux questions métier (y a-t-il une demande ? les vacances sont-elles effectives ? pourquoi ?). Il ne répond pas à la question de qualité de configuration (les réglages sont-ils cohérents ?). Cette responsabilité appartient au domaine `system/integrite_reglages` (voir §5).

---

## 2. Principe fondamental

> Vacances n'est pas une date.
> Vacances n'est pas une intention UI.
> Vacances est un domaine structuré en **5 niveaux**.

**Invariant fondamental** : chaque niveau porte une responsabilité distincte. Les couches calculées ne doivent jamais dépendre d'actions de contexte pour établir leur vérité métier.

> Note : `input_select.mode_maison` peut être écrit en retour par des automations de projection autorisées. Cette écriture descendante est une projection d'état décidé — elle ne constitue pas une dépendance de calcul, et `mode_maison` ne constitue jamais une source de demande du domaine Vacances.

---

## 3. Architecture normative

### 3.1 Paramétrage

Couche de configuration pure. Ne décide rien, ne pilote rien.

| Entité | Rôle |
|--------|------|
| `input_datetime.debut_vacances` | Début de la fenêtre calendaire |
| `input_datetime.fin_vacances` | Fin de la fenêtre calendaire |
| `input_boolean.mode_vacances_auto` | Autorisation de la planification automatique |
| `input_boolean.vacances_demande_manuel` | Demande manuelle explicite de Vacances |
| `input_select.mode_maison` | Projection écrite du contexte global actif (voir §6) |

> Ces entités expriment une configuration ou une intention. Elles ne constituent pas à elles seules une décision métier. Elles ne pilotent aucun équipement.

---

### 3.2 Support temporel

Couche de matérialisation de la fenêtre planifiée. Ne décide rien, ne pilote rien. Sert uniquement de signal d'entrée pour la couche Demande.

| Entité | Rôle |
|--------|------|
| `input_boolean.vacances_fenetre_active` | La fenêtre planifiée est actuellement ouverte |

**Sémantique :**
- `on` : l'instant courant est dans la fenêtre `[debut_vacances ; fin_vacances[`
- `off` : hors fenêtre, ou fenêtre non encore ouverte, ou déjà fermée

**Règles :**
- état matérialisé par un orchestrateur dédié — jamais calculé par `now()` dans un template
- pas une vérité métier finale : c'est un signal temporel rendu explicite
- boot-proof : l'orchestrateur se réconcilie au démarrage et rétablit l'état correct sans avoir "vu passer" les échéances

---

### 3.3 Demande

Couche de décision calculée. Produit la vérité de la demande, indépendamment du terrain.

| Entité | Rôle |
|--------|------|
| `binary_sensor.vacances_planifiees_actives` | La fenêtre est active, les paramètres sont valides et l'auto est autorisé |
| `binary_sensor.vacances_demandees` | Consolidation de la demande (manuelle OU planifiée) |

**Règles :**
- calcul pur, stateless, déterministe
- aucune action directe
- boot-proof et recalculable à tout instant
- indépendant de la réalité terrain

> `binary_sensor.vacances_planifiees_actives` ne contient aucun calcul temporel direct. Il lit `input_boolean.vacances_fenetre_active` comme signal déjà matérialisé par l'orchestrateur. Si les réglages sont invalides, il retombe à `off` — le détail est porté par `binary_sensor.parametres_invalides_vacances` et ses attributs.

---

### 3.4 Effectivité

Couche de vérité métier finale. Source de vérité unique du domaine pour tous les consommateurs.

| Entité | Rôle |
|--------|------|
| `binary_sensor.vacances_actives` | Les vacances sont réellement effectives maintenant |
| `sensor.vacances_raison` | Raison métier de l'état courant (voir §4.4) |

**Règles :**

- calcul pur, stateless, déterministe
- ne déclenche aucune action par elle-même
- consommable par tous les sous-systèmes métier

---

### 3.5 Application de contexte

Couche d'action. Consomme un état déjà calculé, applique des conséquences globales.

**Exemples :**

- projection du contexte dans `input_select.mode_maison`
- gestion des inhibitions transverses
- démarrage / annulation de timers de support

**Règles :**

- ne décide pas si les vacances sont vraies
- consomme une couche déjà calculée du domaine
- actions idempotentes
- zéro logique métier cachée

---

## 4. Décisions métier

### 4.1 `binary_sensor.vacances_planifiees_actives`

**Rôle** : la fenêtre planifiée est valide et englobe l'instant courant.

**ON si et seulement si :**

```
input_boolean.mode_vacances_auto                = on
ET  binary_sensor.parametres_invalides_vacances = off
ET  input_boolean.vacances_fenetre_active       = on
```

**Dégradation :** `parametres_invalides_vacances = on`, `mode_vacances_auto = off`, ou `vacances_fenetre_active = off` → `off` immédiat. Aucun calcul temporel direct dans ce capteur.

---

### 4.1.1 Orchestrateur de fenêtre planifiée

**Automation dédiée** — *Vacances – Orchestrateur fenêtre planifiée*

**Rôle** : matérialiser l'état de `input_boolean.vacances_fenetre_active` au fil du temps et le réconcilier au démarrage.

**Déclencheurs :**

| Déclencheur | Raison |
|-------------|--------|
| `homeassistant: start` | Réconciliation au boot |
| `state` sur `input_datetime.debut_vacances` | Changement de paramètre |
| `state` sur `input_datetime.fin_vacances` | Changement de paramètre |
| `state` sur `input_boolean.mode_vacances_auto` | Changement d'autorisation |
| `time` calculé sur `debut_vacances` | Franchissement d'entrée de fenêtre |
| `time` calculé sur `fin_vacances` | Franchissement de sortie de fenêtre |

**Logique d'exécution :**

```
SI parametres_invalides_vacances = on
    → vacances_fenetre_active = off

SINON SI mode_vacances_auto = off
    → vacances_fenetre_active = off

SINON SI now() ∈ [debut_vacances ; fin_vacances[
    → vacances_fenetre_active = on

SINON
    → vacances_fenetre_active = off
```

**Garanties :**
- `now()` est autorisé dans l'orchestrateur **uniquement au moment d'un déclenchement explicite** (réconciliation boot, franchissement d'échéance, changement de paramètre) — pas dans un template à tick implicite. Son usage ici est ponctuel et contrôlé, pas périodique.
- après tout redémarrage, l'état est rétabli sans avoir "vu passer" les échéances
- idempotent : peut être rejoué sans effet de bord

---

### 4.2 `binary_sensor.vacances_demandees`

**Rôle** : consolider la demande métier de Vacances, quelle que soit sa source.

**ON si et seulement si :**

```
input_boolean.vacances_demande_manuel       = on
OU  binary_sensor.vacances_planifiees_actives = on
```

> **Note structurante** : cette entité est indispensable pour briser la boucle logique. `binary_sensor.vacances_demandees` ne dépend jamais de `input_select.mode_maison` — qui est une projection d'état, pas une source de demande. Sans cette séparation, la fin d'une fenêtre planifiée ne peut pas provoquer le retour à `Normal` si `mode_maison` est encore sur `Vacances`.

---

### 4.3 `binary_sensor.vacances_actives`

**Rôle** : vérité métier finale — les vacances sont-elles réellement effectives ?

**ON si et seulement si :**

```
binary_sensor.vacances_demandees            = on
ET  binary_sensor.presence_famille_unifiee  = off
ET  input_boolean.visite_en_cours           = off
```

**Dégradation :** présence ou visite indisponible → `off` immédiat, sans ambiguïté.

**Interdiction absolue :**

> `binary_sensor.vacances_actives` ne doit jamais dépendre directement et uniquement de `input_select.mode_maison` si le domaine supporte la planification.

---

### 4.4 `sensor.vacances_raison`

**Rôle** : expliquer la raison **métier** de l'état courant du domaine Vacances, y compris les cas de dégradation des capteurs terrain.

Ce capteur répond à la question : *pourquoi les vacances sont-elles actives ou non ?*

Il ne répond pas à : *les réglages sont-ils cohérents ?*
Cette question relève de `binary_sensor.parametres_invalides_vacances` et de ses attributs diagnostiques, dans le domaine `system/integrite_reglages`.

**Priorité de calcul (ordre décroissant) :**

| Priorité | Condition | Valeur retournée |
|----------|-----------|-----------------|
| 1 | Aucune demande active (ni manuelle, ni planifiée) | `"aucune_demande"` |
| 2 | Demande active, `presence_famille_unifiee` indisponible | `"presence_indisponible"` |
| 3 | Demande active, `visite_en_cours` indisponible | `"visite_indisponible"` |
| 4 | Demande active, présence famille détectée | `"presence_famille"` |
| 5 | Demande active, visite en cours | `"visite_en_cours"` |
| 6 | Toutes conditions réunies | `"vacances_actives"` |

> **Nota** : l'état `aucune_demande` recouvre tous les cas où ni `vacances_demande_manuel = on` ni `vacances_planifiees_actives = on` — auto désactivé, hors fenêtre, réglages invalides, ou demande manuelle non active. Le détail des sous-causes de planification est du ressort de `binary_sensor.parametres_invalides_vacances` et de ses attributs diagnostiques, pas de ce capteur.

> Les états `presence_indisponible` et `visite_indisponible` sont des gardes de vérité terrain : ils signalent que `vacances_actives` est `off` par prudence défensive, non par présence confirmée. Cette distinction est essentielle pour le diagnostic UI.

---

## 5. Intégrité des réglages — convention Arsenal

La cohérence des paramètres de planification Vacances est gouvernée par la convention Arsenal `parametres_invalides_*`, dans le fichier :

```
homeassistant/12_template_sensors/system/integrite_reglages/vacances.yaml
```

### 5.1 Entité produite

| Entité | Rôle | Sémantique |
|--------|------|-----------|
| `binary_sensor.parametres_invalides_vacances` | Invalidité des paramètres de planification | `on` = domaine invalide / `off` = domaine cohérent |

Cette convention est uniforme dans Arsenal. L'entité est agrégée dans `group.parametres_invalides_domaines`, qui alimente l'intégrité globale sans modification de `global.yaml`.

### 5.2 Règle de calcul

`binary_sensor.parametres_invalides_vacances` est **ON** (invalide) si :

```
debut_vacances  absent, indisponible ou vide
OU  fin_vacances    absent, indisponible ou vide
OU  fin_vacances ≤  debut_vacances
```

**OFF** (cohérent) si toutes les conditions ci-dessus sont fausses.

### 5.3 Attributs diagnostiques

Le détail de la cause d'invalidité est porté par les attributs du capteur — pas par un sensor séparé.

| Attribut | Type | Signification |
|----------|------|--------------|
| `debut_indisponible` | `bool` | `debut_vacances` absent ou indisponible |
| `fin_indisponible` | `bool` | `fin_vacances` absent ou indisponible |
| `fenetre_inversee` | `bool` | `fin_vacances ≤ debut_vacances` avec les deux dates disponibles |

### 5.4 Intégration dans l'agrégat global

Ajouter dans `group.parametres_invalides_domaines` :

```yaml
- binary_sensor.parametres_invalides_vacances
```

L'attribut `map('replace', 'binary_sensor.parametres_invalides_', '')` de `global.yaml` produira automatiquement `vacances` dans la liste des domaines invalides. Aucune autre modification de `global.yaml` n'est requise.

---

## 6. Rôle de `input_select.mode_maison`

`input_select.mode_maison` est la **projection écrite du contexte global actif**.

Il peut être alimenté :
- par une **action utilisateur explicite** (UI, scène, commande vocale),
- par une **automation de projection autorisée** du domaine Vacances ou d'un autre domaine.

Sa valeur est **lisible par tous**. Son écriture est **contrôlée** : seules les automations de projection autorisées peuvent l'écrire.

| Ce qu'il est | Ce qu'il n'est pas |
|---|---|
| La projection écrite du contexte global actif | Une source de demande du domaine Vacances |
| Lisible par tous les sous-systèmes | Une preuve d'effectivité terrain |
| Écrit par l'utilisateur ou par projection autorisée | Écrit librement par n'importe quelle automation |

> `input_select.mode_maison` est exclusivement une projection écrite du contexte global actif. Il ne constitue jamais une source de demande du domaine Vacances. Toute demande manuelle de Vacances est portée par `input_boolean.vacances_demande_manuel`, entité dédiée et distincte de la projection, ce qui garantit la réversibilité automatique en fin de demande planifiée.

---

## 7. Écriture autorisée des entités du domaine

| Entité | Qui peut écrire |
|--------|----------------|
| `input_datetime.debut_vacances` | Utilisateur / UI de réglage uniquement |
| `input_datetime.fin_vacances` | Utilisateur / UI de réglage uniquement |
| `input_boolean.mode_vacances_auto` | Utilisateur / UI uniquement |
| `input_boolean.vacances_demande_manuel` | Utilisateur / UI uniquement |
| `input_boolean.vacances_fenetre_active` | Orchestrateur de fenêtre uniquement |
| `input_select.mode_maison` | Utilisateur + automations de projection autorisées |
| `binary_sensor.*` du domaine | Calcul uniquement — jamais écrits directement |
| `sensor.vacances_raison` | Calcul uniquement — jamais écrit directement |

> Toute automation qui tente d'écrire directement un `binary_sensor` ou `sensor` du domaine Vacances viole ce contrat.

---

## 8. Automations autorisées

### 8.1 Projection du mode global

Une automation peut écrire `input_select.mode_maison` en projection de la demande calculée.

```
SI  vacances_demandees devient ON  ET  mode_maison ≠ "Vacances"
    → écrire "Vacances"

SI  vacances_demandees devient OFF  ET  mode_maison = "Vacances"
    → écrire "Normal"
```

**Règle** : ces automations **consomment** un état calculé. Elles ne le fabriquent pas.

### 8.2 Application du contexte

Les automations d'application se rattachent à la couche appropriée selon leur nature :

| Source | Cas d'usage |
|--------|-------------|
| `mode_maison = "Vacances"` | Conséquences de **contexte global** |
| `binary_sensor.vacances_demandees = on` | Conséquences de **demande consolidée** |
| `binary_sensor.vacances_actives = on` | Conséquences **métier d'absence effective** |

Cette distinction doit être **explicite dans chaque automation**.

---

## 9. Réconciliation au démarrage

Toute automation de projection ou d'application critique du domaine Vacances doit être compatible avec un redémarrage Home Assistant.

**Exigence :**

> Après tout redémarrage, le domaine Vacances doit pouvoir se réconcilier intégralement à partir des états calculés courants, sans intervention manuelle et sans délai fonctionnel anormal.

**Conséquences pratiques :**

- les `binary_sensor` de demande et d'effectivité sont des templates recalculés au boot,
- les automations de projection s'appuient sur `homeassistant: start` ou sur une évaluation immédiate à l'initialisation,
- aucun état de contexte ne peut rester incohérent après un redémarrage propre.

---

## 10. Consommation par les sous-systèmes

| Besoin | Source autorisée |
|--------|-----------------|
| Inhibition générale, préparation de contexte, timers de support | `input_select.mode_maison` ou `binary_sensor.vacances_demandees` |
| Logique d'absence effective : ECS, chauffage, présence | `binary_sensor.vacances_actives` **uniquement** |
| Diagnostic UI réglages | `binary_sensor.parametres_invalides_vacances` + ses attributs |

---

## 11. Robustesse et états dégradés

### 11.1 Principe général

En cas de données invalides, le système échoue de manière **prudente et explicable**.

### 11.2 Tableau de dégradation

| Situation | Comportement dans ce domaine | Explication portée par |
|-----------|------------------------------|------------------------|
| `debut_vacances` absent ou indisponible | `vacances_planifiees_actives = off` | `binary_sensor.parametres_invalides_vacances` → attribut `debut_indisponible` |
| `fin_vacances` absent ou indisponible | `vacances_planifiees_actives = off` | `binary_sensor.parametres_invalides_vacances` → attribut `fin_indisponible` |
| `fin_vacances ≤ debut_vacances` | `vacances_planifiees_actives = off` | `binary_sensor.parametres_invalides_vacances` → attribut `fenetre_inversee` |
| `presence_famille_unifiee` indisponible | `vacances_actives = off` | `sensor.vacances_raison` → `"presence_indisponible"` |
| `visite_en_cours` indisponible | `vacances_actives = off` | `sensor.vacances_raison` → `"visite_indisponible"` |

> Les deux dernières lignes expriment un **échec prudent** : l'indisponibilité d'un capteur terrain n'est pas assimilée à une présence ou une visite confirmée. `vacances_actives` retombe à `off` par défaut défensif, et la raison exposée reflète l'indisponibilité — pas un état métier positif.

---

## 12. Invariants non négociables

1. Les `input_datetime` ne déclenchent aucune vérité métier à eux seuls.
2. La planification est portée par des capteurs calculés — jamais par des automations horaires brutes.
3. `now()` n'apparaît jamais dans un template sensor du domaine. Son usage est autorisé dans l'orchestrateur de fenêtre, uniquement au moment d'un déclenchement explicite de réconciliation ou de franchissement.
4. La demande Vacances est une entité explicite et consolidée (`binary_sensor.vacances_demandees`).
5. L'effectivité Vacances est strictement séparée de la demande.
6. Aucune automation ne produit de boucle logique auto-bloquante. `binary_sensor.vacances_demandees` ne dépend jamais de `input_select.mode_maison`.
7. Les actions de contexte consomment une couche déjà calculée du domaine (`mode_maison`, `vacances_demandees` ou `vacances_actives` selon leur nature) — elles ne fabriquent jamais la vérité métier.
8. Chaque sous-système consomme la couche qui lui correspond.
9. Les entités calculées du domaine (`binary_sensor.*`, `sensor.*`) ne sont jamais écrites directement par une automation.
10. `input_boolean.vacances_fenetre_active` est écrit exclusivement par l'orchestrateur de fenêtre.
11. Le domaine est boot-proof : tout redémarrage propre produit une réconciliation automatique complète.
12. `sensor.vacances_raison` répond uniquement aux questions métier. Les questions de qualité de configuration sont du ressort exclusif du domaine `system/integrite_reglages`.

---

## 13. Périmètre du domaine

Le domaine Vacances **ne fait pas** :

- ❌ réduire directement le chauffage
- ❌ couper directement l'ECS
- ❌ décider des consignes dynamiques des sous-systèmes
- ❌ remplacer les moteurs spécialisés
- ❌ confondre calendrier et effectivité
- ❌ reposer sur une automation horaire brute comme source unique de vérité
- ❌ exposer la qualité de configuration dans `sensor.vacances_raison`

---

## 14. Critères de clôture du domaine

Le domaine est considéré **propre et clos** si :

- [ ] `input_boolean.vacances_fenetre_active` existe et est exclusivement écrit par l'orchestrateur de fenêtre
- [ ] l'orchestrateur de fenêtre couvre les 6 déclencheurs définis en §4.1.1
- [ ] la planification est portée par `binary_sensor.vacances_planifiees_actives` sans `now()` dans le template
- [ ] `input_boolean.vacances_demande_manuel` existe et est la seule source de demande manuelle
- [ ] la demande est consolidée dans `binary_sensor.vacances_demandees` sans dépendance à `input_select.mode_maison`
- [ ] l'effectivité est indépendante des actions dans `binary_sensor.vacances_actives`
- [ ] `sensor.vacances_raison` couvre les 6 états définis en §4.4 (dont `presence_indisponible` et `visite_indisponible`)
- [ ] `binary_sensor.parametres_invalides_vacances` existe dans `system/integrite_reglages/vacances.yaml` avec ses 3 attributs diagnostiques
- [ ] `binary_sensor.parametres_invalides_vacances` est ajouté à `group.parametres_invalides_domaines`
- [ ] les écrits sur `input_select.mode_maison` sont exclusivement des projections autorisées
- [ ] les automations projettent et appliquent sans fabriquer de vérité
- [ ] les sous-systèmes consomment la couche correcte
- [ ] la réconciliation au démarrage est garantie pour toutes les automations critiques

---

*Fin du contrat — Domaine Vacances v1.4.0*
