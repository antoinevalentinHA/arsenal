# 📜 CONTRAT — PARAMÈTRES INVALIDES

**Version** : 1.1
**Statut** : normatif
**Domaine** : observabilité système — intégrité des paramètres
**Portée** : transverse (tous sous-systèmes Arsenal)

---

## 🎯 RÔLE

Définir, de manière contractuelle et exhaustive, l'architecture de
détection et de signalisation des **incohérences de paramétrage** dans
Arsenal.

Une incohérence de paramétrage est une violation d'invariant logique
entre helpers (`input_number`, `input_datetime`, etc.) qui rendrait
indéfini ou dangereux le comportement d'un automatisme aval.

Exemple : `seuil_off >= seuil_on` sur un seuil bas/haut, ou
`fin_vacances <= debut_vacances` sur une fenêtre temporelle.

Le système ne **corrige rien**. Il **observe** et **signale**.

---

## 🧱 PRINCIPE

L'intégrité des paramètres est traitée comme une **couche d'observabilité
système** distincte des automatismes métier. Elle obéit aux principes
Arsenal :

- **Lecture pure** : aucun capteur de cette couche ne pilote de
  matériel, ne déclenche d'automation, ne corrige de helper.
- **Séparation des préoccupations** : la détection est dans les
  capteurs ; l'agrégation dans la sentinelle globale ; l'UI ne fait
  que révéler conditionnellement l'état global.
- **Aucun fallback silencieux** : toute valeur indisponible doit
  être détectée explicitement, jamais masquée par une valeur par
  défaut.
- **Diagnostic granulaire** : un capteur domaine ne dit pas seulement
  *"ça va pas"*, il dit *quel invariant a sauté* et, quand pertinent,
  *quelle source manque*.

---

## 🏛️ ARCHITECTURE EN COUCHES

Quatre couches, du bas vers le haut :

```
┌──────────────────────────────────────────────────────────┐
│  COUCHE 4 — UI                                           │
│  alerte_configuration_invalide.yaml                      │
│  Carte conditionnelle dans les dashboards                │
└──────────────────────────────────────────────────────────┘
                            ▲
                            │
┌──────────────────────────────────────────────────────────┐
│  COUCHE 3 — Sentinelle globale                           │
│  binary_sensor.parametres_invalides_global               │
│  OR sur le groupe + observabilité agrégée                │
└──────────────────────────────────────────────────────────┘
                            ▲
                            │
┌──────────────────────────────────────────────────────────┐
│  COUCHE 2 — Agrégateur                                   │
│  group.parametres_invalides_domaines                     │
│  Liste des capteurs domaine                              │
└──────────────────────────────────────────────────────────┘
                            ▲
                            │
┌──────────────────────────────────────────────────────────┐
│  COUCHE 1 — Capteurs domaine                             │
│  binary_sensor.parametres_invalides_<domaine>            │
│  Détection effective des invariants                      │
└──────────────────────────────────────────────────────────┘
```

Chaque couche a une responsabilité unique. Aucune ne fait le travail
d'une autre.

---

# 🔵 COUCHE 1 — CAPTEURS DOMAINE

C'est la couche **où le travail se fait**. Tout le reste agrège.

## 📍 ENTITÉ

```
binary_sensor.parametres_invalides_<domaine>
```

Où `<domaine>` est un identifiant snake_case unique correspondant au
sous-système surveillé (`modes_maison`, `chauffage`, `vmc`, `bouclage_ecs`,
`vacances`, `eclairage`, `deshumidificateur`, …).

## 📂 EMPLACEMENT FICHIER

```
/homeassistant/12_template_sensors/system/integrite_reglages/<domaine>.yaml
```

Un fichier = un capteur domaine = un sous-système.

## 🧬 CHAMPS OBLIGATOIRES

```yaml
- binary_sensor:
    - name: "<Domaine> — Paramètres invalides"
      unique_id: parametres_invalides_<domaine>
      default_entity_id: binary_sensor.parametres_invalides_<domaine>
      icon: >
        mdi:alert-circle-outline
      state: >
        ...
      attributes:
        ...
```

| Champ | Règle |
|---|---|
| `name` | Format strict : `"<Domaine> — Paramètres invalides"` (tiret cadratin `—`, accents respectés, domaine en tête) |
| `unique_id` | `parametres_invalides_<domaine>` |
| `default_entity_id` | `binary_sensor.parametres_invalides_<domaine>` (cohérence avec `unique_id`) |
| `icon` | Statique, **toujours** `mdi:alert-circle-outline` |
| `state` | Expression Jinja conforme à la doctrine ci-dessous |
| `attributes` | Diagnostic granulaire — voir plus bas |

## 🚨 DOCTRINE D'EXPRESSION — INTERDITS

Sont **interdits** dans toute expression `state` ou `attributes` :

- `| float(0)` ou tout fallback numérique silencieux non-`none`
- `| int(0)` idem
- Comparaison directe de chaînes ISO temporelles
  (ex : `states('input_datetime.x') < states('input_datetime.y')`)
- Tout mécanisme qui masque silencieusement `unknown`, `unavailable`,
  `none` ou `''`

Un fallback silencieux transforme une indisponibilité en valeur
plausible et casse la sentinelle. C'est l'erreur racine déjà rencontrée
sur l'`axe_temperature_jardin` (le `float(0)` post-restart). À proscrire
sans exception.

## ✅ DOCTRINE D'EXPRESSION — OBLIGATOIRES

- `| float(none)` pour parser un `input_number` (avec garde `is none`)
- `| int(none)` idem si applicable
- `as_datetime(...)` pour parser un `input_datetime`, **toujours
  précédé d'une garde** sur la chaîne brute
- **Variables Jinja en tête** d'expression (`{% set x = ... %}`) pour
  lire chaque source une seule fois et rendre la logique lisible

## 🧩 GABARIT DE STATE

```yaml
state: >
  {# 1. Lecture des sources, parsing, détection indisponibilités #}
  {% set src_a = states('input_number.xxx') | float(none) %}
  {% set src_b = states('input_number.yyy') | float(none) %}
  {% set indisponible = src_a is none or src_b is none %}

  {# 2. Évaluation des invariants (forme : invariant_violé = ...) #}
  {% set invariant_1_violé = indisponible or not (src_a > src_b) %}
  {% set invariant_2_violé = indisponible or not (...) %}

  {# 3. Aggregation : OR sur tous les invariants violés #}
  {{ invariant_1_violé or invariant_2_violé }}
```

**Convention sémantique** : la variable `<règle>_violé` (ou
`<règle>_invalide`) est **vraie quand l'invariant est cassé**. Le `state`
est le OR de toutes ces variables. Si une source est indisponible, on
considère **par défaut tous les invariants qui en dépendent comme
violés** — pas d'optimisme silencieux.

## 📊 ATTRIBUTS — RÈGLES STRICTES

### Obligatoires

**1. Un attribut booléen par invariant métier**

```yaml
<règle>_invalide: >
  {% set src_a = ... %}
  {% set src_b = ... %}
  {{ src_a is none or src_b is none or not (src_a > src_b) }}
```

Nommage : `<groupe_de_règles>_invalide` ou `<groupe_de_règles>_invalides`
selon le nombre — le suffixe doit refléter la sémantique (ex :
`seuils_hr_invalides`, `fenetre_inversee`).

L'attribut **n'est jamais** une simple recopie de l'expression `state` :
il isole **un seul invariant**.

**2. Un attribut `cause` énumératif priorisé**

```yaml
cause: >
  {% set ... %}
  {% if helpers_indisponibles %}
    helpers_indisponibles
  {% elif not (src_a > src_b) %}
    invariant_1_invalide
  {% elif not (...) %}
    invariant_2_invalide
  {% else %}
    none
  {% endif %}
```

Valeur unique parmi un domaine fini, **priorisée du plus structurel au
plus métier** (l'indisponibilité prime toujours sur la violation
métier — on ne peut pas affirmer qu'un invariant est violé si la source
manque). La valeur `none` est obligatoire pour le cas conforme.

### Obligatoires si source critique identifiable

**3. Indisponibilité granulaire — règle proportionnée**

Selon le nombre de sources critiques :

- **≤ 5 sources critiques** :
  un attribut booléen `<source>_indisponible` par source.

  ```yaml
  debut_indisponible: >
    {{ states('input_datetime.debut_vacances') in
       ['unknown', 'unavailable', 'none', ''] }}
  fin_indisponible: >
    {{ states('input_datetime.fin_vacances') in
       ['unknown', 'unavailable', 'none', ''] }}
  ```

- **> 5 sources critiques** :
  un attribut unique `helpers_indisponibles` exposant la **liste** des
  helpers défaillants.

  ```yaml
  helpers_indisponibles: >
    {% set sources = [
        'input_number.xxx',
        'input_number.yyy',
        'input_datetime.zzz',
    ] %}
    {% set ns = namespace(items=[]) %}
    {% for entity in sources %}
      {% if states(entity) in ['unknown', 'unavailable', 'none', ''] %}
        {% set ns.items = ns.items + [entity] %}
      {% endif %}
    {% endfor %}
    {{ ns.items }}
  ```

  La doctrine est : **liste discrète plutôt que sapin de Noël de
  booléens**. Un dashboard reste lisible avec une liste à 0–3 entrées,
  pas avec 25 attributs binaires.

Le seuil de 5 est indicatif. Le critère réel est la **lisibilité au
diagnostic** : si les attributs deviennent du bruit, basculer en liste.

### Interdits

- Attribut redondant avec `state` (ex : `parametres_invalides: <state>`)
- Attribut exposant une **valeur source brute** sans
  contexte de validation (sauf usage strictement diagnostique justifié
  en commentaire)
- Attribut sans nom métier explicite (ex : `cond1`, `check_a`)

## 🏛️ EN-TÊTE NORMATIVE

Tout fichier `<domaine>.yaml` commence par un en-tête structuré au
canevas suivant. Les sections sont **imposées et dans cet ordre** ; leur
contenu peut être bref mais elles doivent toutes être présentes.

```yaml
# ==========================================================
# 🧠 ARSENAL — BINARY SENSOR
#     Intégrité paramètres — <Domaine>
# ----------------------------------------------------------
# 🎯 RÔLE
#
#   <Une à trois lignes décrivant le périmètre métier>
#
# ----------------------------------------------------------
# 🧱 PRINCIPE
#
#   - Lecture pure
#   - Aucune action, aucune correction
#   - <Particularités éventuelles du domaine>
#
# ----------------------------------------------------------
# 🚨 INVARIANTS SURVEILLÉS
#
#   1) <invariant 1 en notation logique>
#   2) <invariant 2>
#   ...
#
#   Toute violation = paramètres INVALIDES
#
# ----------------------------------------------------------
# 🔗 DÉPENDANCES
#
#   - input_number.xxx
#   - input_datetime.yyy
#   - ...
#
# ----------------------------------------------------------
# 📊 ATTRIBUTS EXPOSÉS
#
#   - <règle>_invalide        : <description courte>
#   - cause                   : énumération priorisée
#   - <source>_indisponible   : <si applicable>
#   - helpers_indisponibles   : <si applicable>
#
# ----------------------------------------------------------
# 🚫 INTERDITS
#
#   - Aucun pilotage de switch / climate / cover
#   - Aucune correction automatique
#   - Aucune logique métier
#
# ----------------------------------------------------------
# 📍 ENTITÉ
#
#   binary_sensor.parametres_invalides_<domaine>
#
# ----------------------------------------------------------
# 🧠 STATUT
#
#   Capteur de diagnostic — Intégrité paramètres <Domaine>
# ==========================================================
```

---

# 🔵 COUCHE 2 — AGRÉGATEUR

## 📍 ENTITÉ

```
group.parametres_invalides_domaines
```

## 📂 EMPLACEMENT FICHIER

```
/homeassistant/02_groups/parametres_invalides.yaml
```

## 🧬 RÔLE

Lister tous les capteurs `binary_sensor.parametres_invalides_<domaine>`
de la couche 1. Conteneur pur, sans logique.

## 🧩 IMPLÉMENTATION CANONIQUE

```yaml
parametres_invalides_domaines:
  name: "Paramètres invalides — Domaines"
  entities:
    - binary_sensor.parametres_invalides_modes_maison
    - binary_sensor.parametres_invalides_bouclage_ecs
    - binary_sensor.parametres_invalides_chauffage
    - binary_sensor.parametres_invalides_deshumidificateur
    - binary_sensor.parametres_invalides_eclairage
    - binary_sensor.parametres_invalides_vacances
    - binary_sensor.parametres_invalides_vmc
    - binary_sensor.parametres_invalides_climatisation
    # ... tout nouveau domaine doit être ajouté ici
```

## 🏛️ EN-TÊTE NORMATIVE

Le fichier de groupe commence par un en-tête structuré au canevas
suivant. Sections imposées dans cet ordre.

```yaml
# ==========================================================
# 🧠 ARSENAL — GROUP
#     Paramètres invalides — Domaines
# ----------------------------------------------------------
# 🎯 RÔLE
#
#     Agréger l'ensemble des capteurs
#     `binary_sensor.parametres_invalides_<domaine>`
#     afin d'exposer une vision centralisée
#     des incohérences de paramètres par domaine.
#
# ----------------------------------------------------------
# 🧩 PÉRIMÈTRE
#
#     - Regroupement exclusif de capteurs de type :
#         binary_sensor.parametres_invalides_<domaine>
#     - Couverture multi-domaines, source unique pour
#       la sentinelle globale.
#
# ----------------------------------------------------------
# 🔗 DÉPENDANCES
#
#     - binary_sensor.parametres_invalides_modes_maison
#     - binary_sensor.parametres_invalides_bouclage_ecs
#     - binary_sensor.parametres_invalides_chauffage
#     - binary_sensor.parametres_invalides_deshumidificateur
#     - binary_sensor.parametres_invalides_eclairage
#     - binary_sensor.parametres_invalides_vacances
#     - binary_sensor.parametres_invalides_vmc
#     - binary_sensor.parametres_invalides_climatisation
#
# ----------------------------------------------------------
# 🚫 INTERDITS
#
#     - Aucune logique métier
#     - Aucune décision
#     - Aucune action
#     - Aucune détection d'invariant
#     - Aucun masquage ou filtrage d'un domaine
#
# ----------------------------------------------------------
# 🧠 STATUT
#
#     Agrégat diagnostique — Transversal
#     Source unique pour l'intégrité globale des paramètres
# ==========================================================
```

## 🚨 INVARIANTS

- Toute entité du groupe **doit** avoir un `unique_id` commençant par
  `parametres_invalides_`.
- L'ajout d'un nouveau capteur domaine **impose** sa déclaration dans
  ce groupe — sinon la sentinelle globale ne le voit pas.
- Aucune autre entité que des `binary_sensor.parametres_invalides_*`.
- La section `🔗 DÉPENDANCES` de l'en-tête doit refléter exactement
  la liste `entities` (pas de divergence en-tête / déclaration).

## 🚫 INTERDITS

- Pas de capteur métier dans ce groupe
- Pas de logique dans le groupe (le groupe est un conteneur, pas un
  évaluateur)
- Pas de filtrage conditionnel d'un domaine

---

# 🔵 COUCHE 3 — SENTINELLE GLOBALE

## 📍 ENTITÉ

```
binary_sensor.parametres_invalides_global
```

## 📂 EMPLACEMENT FICHIER

```
/homeassistant/12_template_sensors/system/integrite_reglages/global.yaml
```

## 🧬 RÔLE

Vue agrégée binaire : `on` ⇔ au moins un domaine invalide.

## 🧩 IMPLÉMENTATION CANONIQUE

```yaml
- binary_sensor:
    - name: "Système — Paramètres invalides"
      unique_id: parametres_invalides_global
      default_entity_id: binary_sensor.parametres_invalides_global
      icon: >
        mdi:alert-octagon-outline
      state: >
        {{ is_state('group.parametres_invalides_domaines', 'on') }}
      attributes:
        domaines_invalides: >
          {{
            expand('group.parametres_invalides_domaines')
            | selectattr('state', 'eq', 'on')
            | map(attribute='entity_id')
            | map('replace', 'binary_sensor.parametres_invalides_', '')
            | list
          }}
        nombre_domaines_invalides: >
          {{
            expand('group.parametres_invalides_domaines')
            | selectattr('state', 'eq', 'on')
            | list
            | count
          }}
```

## 🚨 INVARIANTS

- Icône statique distincte de la couche 1 : `mdi:alert-octagon-outline`
  (octogone = sévérité système, vs cercle = alerte unitaire).
- Attributs obligatoires : `domaines_invalides` (liste) et
  `nombre_domaines_invalides` (entier).
- Pas d'autre attribut métier — la couche 3 ne **sait rien** des
  invariants des couches inférieures, elle ne fait qu'agréger.

## 🚫 INTERDITS

- Aucune logique métier
- Aucune lecture directe d'`input_number` / `input_datetime`
- Aucune dépendance autre que `group.parametres_invalides_domaines`

---

# 🔵 COUCHE 4 — UI

## 📂 EMPLACEMENT FICHIER

```
/homeassistant/lovelace/includes/alerte_configuration_invalide.yaml
```

## 🧬 IMPLÉMENTATION CANONIQUE

```yaml
type: conditional
conditions:
  - entity: binary_sensor.parametres_invalides_global
    state: "on"
card:
  type: custom:button-card
  template: carte_alerte_binaire_critique
  entity: binary_sensor.parametres_invalides_global
  name: "⚠️ CONFIGURATION INVALIDE"
```

## 🧩 INCLUSION DASHBOARDS

L'include est **obligatoire en haut de la première vue** des dashboards
principaux Arsenal :

- `/homeassistant/lovelace/dashboards/arsenal.yaml`
- `/homeassistant/lovelace/dashboards/navigation.yaml`

Position : **immédiatement après le bloc météo de navigation**, avant
tout autre contenu fonctionnel.

```yaml
cards:
  - !include ../includes/navigation/meteo.yaml
  - !include ../includes/alerte_configuration_invalide.yaml
  # ... le reste
```

## 🚨 INVARIANTS

- Carte conditionnelle uniquement (`type: conditional`) — jamais
  affichée si tout est conforme.
- Lecture seule de `binary_sensor.parametres_invalides_global` —
  jamais d'un capteur de couche 1 directement.
- Visibilité globale : les deux dashboards principaux la portent.

## 🚫 INTERDITS

- Pas de carte alternative qui montrerait un état OK
- Pas d'inclusion conditionnelle sur des sous-vues métier (la
  visibilité globale est la garantie que le diagnostic ne se cache pas)
- Pas de lien direct vers un domaine spécifique — l'utilisateur drille
  via les attributs du capteur global

---

## ✅ CHECKLIST D'AJOUT D'UN NOUVEAU DOMAINE

Procédure normative à suivre pour ajouter un sous-système :

1. Créer
   `/homeassistant/12_template_sensors/system/integrite_reglages/<domaine>.yaml`
   en respectant l'en-tête canonique et le gabarit de `state`.
2. Vérifier que **tous les invariants métier** du domaine sont
   couverts. Lister les sources critiques.
3. Choisir le mode d'attribut d'indisponibilité selon la règle ≤ 5 / > 5.
4. Implémenter l'attribut `cause` priorisé.
5. Ajouter l'entité dans `group.parametres_invalides_domaines`.
6. Recharger les template sensors et le groupe.
7. Vérifier l'apparition du domaine dans
   `binary_sensor.parametres_invalides_global.attributes.domaines_invalides`
   en provoquant volontairement une violation.
8. Vérifier que l'alerte UI s'affiche bien sur les deux dashboards.
9. Mettre à jour ce contrat si un cas de figure nouveau a été découvert.

---

## 📜 CHANGELOG

| Version | Date       | Notes                                          |
|---------|------------|------------------------------------------------|
| 1.0     | 2026-04-30 | Version initiale. Couches 1–4 normatives.      |
| 1.1     | 2026-05-26 | Ajout du domaine climatisation.                |