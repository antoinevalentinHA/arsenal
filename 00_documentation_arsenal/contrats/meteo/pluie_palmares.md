# Arsenal — Contrat opérationnel
## Palmarès historique
### Version 1.0

---

## 1. Statut et portée

### 1.1 Statut
**STRICT.** Contrat normatif Arsenal en vigueur. Document de référence pour toute implémentation de la primitive **palmarès historique** et de ses instances métier.

### 1.2 Portée
Le présent contrat définit :

- la primitive Arsenal **palmarès historique**, indépendamment de tout domaine métier ;
- la grammaire d'instanciation de cette primitive ;
- l'instance V1 unique : **pluie journalière**.

### 1.3 Hors portée
Le contrat ne définit pas :

- l'agrégation amont de la source métier (utility_meter, capteurs stabilisés, pipelines de fusion) ;
- la présentation UI (cartes, dashboards) ;
- les instances métier autres que pluie journalière, qui feront l'objet de déclarations ultérieures conformes à la grammaire de la section 3.

---

## 2. Définition de la primitive « palmarès historique »

### 2.1 Nature
Un palmarès historique est une **mémoire qualitative bornée** qui maintient un classement des N valeurs extrêmes observées sur une série temporelle de périodes métier clôturées.

Il ne s'agit pas :

- d'une statistique glissante ;
- d'un agrégat Recorder ;
- d'un historique temporel exhaustif.

Il s'agit d'un **registre d'extrêmes**, sélectif et persistant.

### 2.2 Vocabulaire canonique

| Terme | Définition |
|---|---|
| **Primitive** | Mécanique générique définie par le présent contrat. |
| **Instance** | Application de la primitive à un domaine métier précis (pluie, humidex, CO₂, ECS, etc.). |
| **Période** | Unité temporelle clôturée évaluée par l'instance (un jour, une semaine, une heure). |
| **Source** | Capteur HA stabilisé fournissant la valeur métier d'une période clôturée. |
| **Rang** | Position d'une entrée dans le palmarès, de 1 (extrême maximal) à N. |
| **Top N** | Profondeur du palmarès, paramètre de l'instance. |
| **Snapshot** | Capture de la valeur de la période en cours juste avant sa clôture. |
| **Évaluation** | Décision d'insertion ou de rejet d'une période close dans le palmarès. |
| **Anomalie** | Incohérence interne du palmarès détectée par le capteur de santé dédié. |

### 2.3 Invariants génériques

| ID | Invariant |
|---|---|
| **INV-1** | Le palmarès doit être déterministe : à entrées identiques, classement identique. |
| **INV-2** | Le palmarès doit être recalculable à partir de la séquence d'évaluations. |
| **INV-3** | Une valeur indisponible (`unknown`, `unavailable`, absente) ne doit jamais générer de record. |
| **INV-4** | Une période non close ne doit jamais être évaluée. |
| **INV-5** | Le Recorder Home Assistant ne doit pas être utilisé comme source métier. |
| **INV-6** | La UI doit consommer une entité stabilisée, jamais contenir la logique de classement. |
| **INV-7** | Aucune écriture fichier, aucun script externe, aucune dépendance hors HA en V1. |
| **INV-8** | Chaque rang occupé doit être entièrement défini (date ET valeur). Pas de rang partiel. |
| **INV-9** | Le palmarès doit être compact : pas de trous entre rangs occupés. |
| **INV-10** | Politique d'ex æquo : **FIFO**. L'antériorité prime, une valeur égale n'évince pas un record antérieur. |

---

## 3. Grammaire d'instance

### 3.1 Paramètres d'instanciation
Toute instance est définie par les paramètres suivants :

| Paramètre | Type | Description |
|---|---|---|
| `instance_id` | identifiant snake_case | Identifie l'instance dans le nommage des entités. |
| `source` | entity_id HA | Capteur HA stabilisé exposant la valeur de la période close. |
| `cycle` | enum { `daily`, `weekly`, `monthly` } | Cycle de la période métier. V1 : `daily` uniquement. |
| `top_n` | entier ≥ 1 | Profondeur du palmarès. |
| `unite` | chaîne | Unité physique de la valeur (mm, °C, kWh, ppm, etc.). |
| `seuil_fraicheur_h` | entier (heures) | Seuil au-delà duquel l'absence d'évaluation déclenche l'anomalie B4. |

### 3.2 Convention de nommage canonique

**Helpers techniques** (mémoire, snapshots, horodatages) :

```text
input_number.palmares_<instance_id>_rang_<NN>_valeur
input_text.palmares_<instance_id>_rang_<NN>_date
input_number.palmares_<instance_id>_snapshot_veille
input_datetime.palmares_<instance_id>_derniere_evaluation
```

`<NN>` est un entier sur deux chiffres, de `01` à `top_n` inclus.

**Capteurs exposés** (façade UI, santé) :

```text
sensor.palmares_<instance_id>
binary_sensor.palmares_<instance_id>_anomalie
```

**Note doctrinale.** Les helpers portent le préfixe court `palmares_` (registre technique). Les capteurs exposés portent le même préfixe sans suffixe technique : la qualification « historique » appartient à la documentation conceptuelle, pas au runtime. Le runtime reste court, lisible, exploitable dans templates et UI.

### 3.3 Conventions de format

| Élément | Format |
|---|---|
| Date de rang | ISO 8601 `YYYY-MM-DD`, chaîne dans `input_text` |
| Valeur de rang | numérique dans `input_number`, précision adaptée à l'unité |
| Snapshot veille | numérique dans `input_number` |
| Dernière évaluation | datetime ISO 8601 dans `input_datetime` |

Les helpers de fraîcheur temporelle peuvent utiliser une sentinelle explicite
pour représenter l’état “jamais évalué”.
La sentinelle canonique V1 est :
1970-01-01 00:00:00

---

## 4. Instance V1 : pluie journalière

### 4.1 Source
La source canonique de l'instance pluie journalière est :

```text
sensor.pluie_journaliere
```

construite via `utility_meter` en cycle `daily` sur `sensor.pluie_total_local`.

**Prérequis V1.** Si `sensor.pluie_journaliere` n'existe pas au moment de la mise en œuvre, sa création est un prérequis bloquant. Le palmarès ne doit pas être mis en service sans sa source canonique.

**Note sur la source amont.** Le contrat ne prescrit pas la `state_class` de `sensor.pluie_total_local`. Il prescrit seulement que `sensor.pluie_journaliere` soit construit par `utility_meter` cycle `daily` sur cette source, en respectant le schéma de la chaîne hebdomadaire existante (`sensor.pluie_hebdomadaire`, exposée par l'instance `utility_meter` de clé `pluie_semaine` en cycle `weekly` ; l'entity_id dérive du `name`, pas de la clé). Toute modification de l'amont sort du périmètre du présent contrat et doit faire l'objet d'une instruction dédiée.

Déclaration `utility_meter` attendue :

```yaml
pluie_journaliere:
  source: sensor.pluie_total_local
  cycle: daily
  name: "Pluie (journalière)"
```

### 4.2 Paramètres retenus

| Paramètre | Valeur |
|---|---|
| `instance_id` | `pluie_journalier` |
| `source` | `sensor.pluie_journaliere` |
| `cycle` | `daily` |
| `top_n` | `10` |
| `unite` | `mm` |
| `seuil_fraicheur_h` | `36` |

### 4.3 Liste exhaustive des entités HA à déclarer

**Helpers de rangs** (20 helpers) :

```text
input_number.palmares_pluie_journalier_rang_01_valeur
input_text.palmares_pluie_journalier_rang_01_date
input_number.palmares_pluie_journalier_rang_02_valeur
input_text.palmares_pluie_journalier_rang_02_date
input_number.palmares_pluie_journalier_rang_03_valeur
input_text.palmares_pluie_journalier_rang_03_date
input_number.palmares_pluie_journalier_rang_04_valeur
input_text.palmares_pluie_journalier_rang_04_date
input_number.palmares_pluie_journalier_rang_05_valeur
input_text.palmares_pluie_journalier_rang_05_date
input_number.palmares_pluie_journalier_rang_06_valeur
input_text.palmares_pluie_journalier_rang_06_date
input_number.palmares_pluie_journalier_rang_07_valeur
input_text.palmares_pluie_journalier_rang_07_date
input_number.palmares_pluie_journalier_rang_08_valeur
input_text.palmares_pluie_journalier_rang_08_date
input_number.palmares_pluie_journalier_rang_09_valeur
input_text.palmares_pluie_journalier_rang_09_date
input_number.palmares_pluie_journalier_rang_10_valeur
input_text.palmares_pluie_journalier_rang_10_date
```

**Helpers de mécanique** (2 helpers) :

```text
input_number.palmares_pluie_journalier_snapshot_veille
input_datetime.palmares_pluie_journalier_derniere_evaluation
```

input_datetime.palmares_pluie_journalier_derniere_evaluation
est initialisé avec la sentinelle canonique.

**Capteurs exposés** (2 capteurs) :

```text
sensor.palmares_pluie_journalier
binary_sensor.palmares_pluie_journalier_anomalie
```

**Automations** (2 automations) :

```text
automation.palmares_pluie_journalier_snapshot
automation.palmares_pluie_journalier_evaluation
```

**Total instance V1** : 20 helpers de rangs + 2 helpers de mécanique + 2 capteurs + 2 automations = **26 entités**.

### 4.4 Convention de rang vide
Un rang est dit **vide** lorsque :

- `input_text.palmares_pluie_journalier_rang_NN_date` est égal à la chaîne vide `""` ;
- `input_number.palmares_pluie_journalier_rang_NN_valeur` est égal à `0`.

Les deux conditions doivent être conjointes (INV-8). L'état initial du palmarès est : tous les rangs vides.

---

## 5. Mécanique d'évaluation

### 5.1 Snapshot pré-minuit

**Automation.** `automation.palmares_pluie_journalier_snapshot`

**Déclenchement.** Tous les jours à `23:59:55`.

**Comportement.**

1. Lire `sensor.pluie_journaliere`.
2. Si la valeur est `unknown`, `unavailable`, ou non numérique : ne rien faire. Le snapshot conserve sa valeur précédente.
3. Sinon : écrire la valeur dans `input_number.palmares_pluie_journalier_snapshot_veille`.

**Justification.** Le snapshot fige la valeur de la journée avant le reset de l'`utility_meter` à minuit. L'absence de snapshot lors d'une journée à source indisponible est volontaire : elle se traduira par l'absence d'évaluation à 00:00:30 (voir 5.4).

### 5.2 Évaluation post-minuit

**Automation.** `automation.palmares_pluie_journalier_evaluation`

**Déclenchement.** Tous les jours à `00:00:30`.

**Comportement.**

1. Lire `input_number.palmares_pluie_journalier_snapshot_veille` (valeur `V`) et la date de la veille (`D` = veille de `now()`).
2. **Garde d'abstention.** Si `V` n'est pas un nombre fini, ou si le snapshot n'a pas été mis à jour depuis plus de 23 heures (cas où le snapshot a été figé sur une valeur ancienne), ne rien faire. Sortie sans modification du palmarès.
3. **Garde d'unicité.** Si `D` est déjà présent dans l'un des rangs occupés (`input_text.palmares_pluie_journalier_rang_NN_date` = `D`), ne rien faire. Une journée ne peut figurer qu'une fois.
4. **Décision d'insertion.** Déterminer le rang d'insertion `R` selon la politique d'insertion (5.3).
5. **Application.** Si `R ≤ top_n`, exécuter l'insertion (5.3). Sinon, ne rien faire.
6. **Horodatage.** Quelle que soit l'issue (insertion ou rejet), écrire `now()` dans `input_datetime.palmares_pluie_journalier_derniere_evaluation`.

**Note.** L'horodatage est mis à jour même en cas de rejet, parce qu'il signe que l'évaluation a effectivement eu lieu. Le capteur d'anomalie B4 surveille la fraîcheur de **l'évaluation**, pas de la dernière insertion.

### 5.3 Insertion et politique d'ex æquo

**Politique d'ex æquo : FIFO.** Une nouvelle valeur s'insère **strictement après** tout record antérieur de valeur égale.

**Algorithme de détermination du rang d'insertion `R`.**

Soit la liste ordonnée des rangs occupés du palmarès `[(v_1, d_1), (v_2, d_2), ..., (v_k, d_k)]` avec `v_1 ≥ v_2 ≥ ... ≥ v_k`.

`R` est le plus petit entier tel que `v_R < V`.
Si aucun tel `R` n'existe (tous les rangs occupés ont une valeur supérieure ou égale à `V`), alors `R = k + 1`.

**Application de l'insertion** lorsque `R ≤ top_n` :

1. Décaler vers le bas tous les rangs occupés de position `≥ R` :
   pour `i` de `min(k, top_n - 1)` à `R`, copier `(v_i, d_i)` dans le rang `i + 1`.
2. Écrire `(V, D)` dans le rang `R`.
3. Si après décalage, le rang `top_n + 1` aurait dû recevoir une valeur, elle est silencieusement perdue (eviction naturelle).

**Compacité préservée.** L'algorithme garantit qu'à l'issue de l'insertion, les rangs occupés restent contigus à partir du rang 1 (INV-9).

### 5.4 Comportements d'abstention

Le moteur s'abstient (n'insère rien et n'évince rien) dans les cas suivants :

| Cas | Détection | Conséquence |
|---|---|---|
| Source indisponible au snapshot | Snapshot non actualisé à 23:59:55 | Évaluation à 00:00:30 détecte un snapshot obsolète, abstention. |
| Source numérique invalide | Valeur non finie | Snapshot ignore, évaluation s'abstient. |
| Journée déjà présente | Date veille dans un rang | Abstention silencieuse. |
| Valeur strictement inférieure au rang `top_n` occupé | Rang d'insertion `R > top_n` | Rejet sans modification. |
| Palmarès en anomalie **structurelle** (B1, B2 ou B3) | `binary_sensor.palmares_pluie_journalier_anomalie` = `on` ET `motif` ∈ `{ "ordre_invalide", "couplage_invalide", "compacite_invalide" }` | Abstention. **Voir section 8.** |

**Note importante.** L'anomalie B4 (`motif = "evaluation_obsolete"`) **n'est pas bloquante**. Elle signale une obsolescence d'évaluation et doit pouvoir être résorbée par une nouvelle évaluation valide. Si B4 bloquait l'évaluation, une source revenue après gel resterait piégée par sa propre anomalie d'obsolescence. Seules les anomalies structurelles B1, B2, B3 — qui invalident la sémantique même du palmarès — bloquent l'insertion.

---

## 6. Capteur de synthèse

### 6.1 Entité
`sensor.palmares_pluie_journalier`

### 6.2 État
Valeur numérique du rang 1 (`input_number.palmares_pluie_journalier_rang_01_valeur`) **si et seulement si** le rang 1 est occupé au sens de 4.4.

Sinon : `unavailable`.

**Justification doctrinale.** L'état `unavailable` exprime explicitement « pas encore de vérité métier ». Un état à `0` induirait l'UI en erreur (« le record est de 0 mm »). Cohérent avec la doctrine Arsenal d'abstention.

### 6.3 Attributs

| Attribut | Valeur |
|---|---|
| `unite` | `mm` |
| `instance_id` | `pluie_journalier` |
| `cycle` | `daily` |
| `top_n` | `10` |
| `records` | Liste ordonnée des rangs occupés. Chaque entrée : `{ rang, date, valeur }`. |
| `derniere_evaluation` | Valeur de `input_datetime.palmares_pluie_journalier_derniere_evaluation`. |
| `nombre_records` | Entier, nombre de rangs occupés (0 à `top_n`). |

### 6.4 Invariant de cohérence
Le capteur de synthèse ne contient **aucune logique de classement**. Il reflète l'état des helpers. Toute incohérence du palmarès se reflète mécaniquement dans le capteur et est détectée par le capteur d'anomalie (section 7), jamais corrigée silencieusement par le capteur de synthèse.

---

## 7. Capteur d'anomalie

### 7.1 Entité
`binary_sensor.palmares_pluie_journalier_anomalie`

### 7.2 État
`on` si **au moins une** des quatre conditions B1, B2, B3, B4 est violée. `off` sinon.

### 7.3 Conditions

| ID | Nom | Définition |
|---|---|---|
| **B1** | Cohérence d'ordre | Pour tout couple de rangs occupés `(i, j)` avec `i < j`, on doit avoir `v_i ≥ v_j`. Violation si un rang occupé inférieur a une valeur strictement supérieure à un rang occupé supérieur. |
| **B2** | Cohérence de couplage | Pour tout rang `N`, soit `(date_N = "" ET valeur_N = 0)`, soit `(date_N ≠ "" ET valeur_N > 0 ET date_N valide ISO 8601)`. Violation sinon. |
| **B3** | Cohérence de compacité | Si le rang `N` est occupé, alors tous les rangs `1` à `N-1` doivent être occupés. Violation si un rang occupé est précédé d'un rang vide. |
| **B4** | Fraîcheur d'évaluation | `now() - input_datetime.palmares_pluie_journalier_derniere_evaluation ≤ 36 heures`. Violation au-delà. |

**Exception B4 — état initial.** 

Si derniere_evaluation = 1970-01-01 00:00:00,
l’instance est considérée en état initial,
et la condition B4 est exemptée.

### 7.4 Attributs

| Attribut | Valeur |
|---|---|
| `motif` | Identifiant de la première condition violée détectée, dans l'ordre B1 → B2 → B3 → B4. Valeur dans `{ "ordre_invalide", "couplage_invalide", "compacite_invalide", "evaluation_obsolete", null }`. |
| `detail` | Chaîne descriptive précisant la nature de la violation (ex. : `"rang 03 vide alors que rang 04 occupé"`, `"valeur rang 02 (15.3) > valeur rang 01 (12.1)"`). |
| `derniere_evaluation` | Recopie de `input_datetime.palmares_pluie_journalier_derniere_evaluation`. |

### 7.5 Priorité de motif
En cas de violations multiples simultanées, `motif` reporte la première détectée dans l'ordre canonique : B1, puis B2, puis B3, puis B4. Cet ordre reflète la gravité décroissante : une incohérence d'ordre invalide la sémantique même du palmarès, alors qu'une évaluation obsolète n'invalide que sa fraîcheur.

---

## 8. Comportements en cas d'incident

### 8.1 État initial (mise en service)
Tous les rangs vides. Snapshot à `0`. `derniere_evaluation` non défini.

- `sensor.palmares_pluie_journalier` = `unavailable`.
- `binary_sensor.palmares_pluie_journalier_anomalie` = `off` (B4 exempté tant que `derniere_evaluation` est non défini).

État initial légitime, aucune intervention requise.

### 8.2 Source `sensor.pluie_journaliere` durablement indisponible
- Le snapshot n'est pas mis à jour.
- L'évaluation s'abstient quotidiennement.
- `derniere_evaluation` **n'est pas** mis à jour (puisque l'évaluation s'abstient).
- Au bout de 36 heures, B4 déclenche : `binary_sensor.palmares_pluie_journalier_anomalie` = `on`, `motif` = `"evaluation_obsolete"`.

Le palmarès n'est pas corrompu, il est simplement « gelé ». **L'anomalie B4 n'est pas bloquante** : dès que la source revient, l'évaluation reprend normalement (B4 ne figure pas dans les motifs d'abstention de 5.4). À la première évaluation effective, `derniere_evaluation` est rafraîchi et l'anomalie se résorbe automatiquement.

### 8.3 Incohérence structurelle détectée (B1, B2, B3)
- Le capteur d'anomalie passe à `on` avec le motif correspondant (`ordre_invalide`, `couplage_invalide`, `compacite_invalide`).
- **Le moteur s'abstient de toute nouvelle insertion** tant que l'anomalie structurelle persiste (cf. 5.4).
- Aucune écriture par-dessus, aucun « auto-réparé ».
- Résolution : intervention manuelle (correction des helpers via UI HA, ou réinitialisation explicite).

**Doctrine REJECT-not-clamp.** Une incohérence structurelle n'est jamais corrigée silencieusement. Elle est exposée, et l'opérateur tranche.

**Distinction B4.** Une anomalie B4 seule (`motif = "evaluation_obsolete"`) ne déclenche pas l'abstention. Le moteur continue d'évaluer chaque jour, et toute évaluation effective résorbe l'anomalie. Voir 5.4 et 8.2.

### 8.4 Réinitialisation manuelle
Procédure documentaire (non automatisée en V1) :

1. Mettre tous les `input_text.palmares_pluie_journalier_rang_NN_date` à `""`.
2. Mettre tous les `input_number.palmares_pluie_journalier_rang_NN_valeur` à `0`.
3. Laisser `input_datetime.palmares_pluie_journalier_derniere_evaluation` inchangé (ou le réinitialiser explicitement si on souhaite que B4 soit exempté à nouveau).
4. Le capteur d'anomalie repasse à `off` à la prochaine évaluation.

---

## 9. Invariants V1 récapitulés

| ID | Invariant | Origine |
|---|---|---|
| **INV-1** à **INV-10** | Voir section 2.3 | Primitive |
| **INV-V1-A** | Instance unique : `pluie_journalier`. Aucune autre instance n'est implémentée en V1. | Scope V1 |
| **INV-V1-B** | Hébergement strict Home Assistant. Aucune dépendance externe : pas de fichier, pas de script externe, pas de pyscript, pas d'AppDaemon, pas de NAS. | Doctrine V1 |
| **INV-V1-C** | Topologie A1 : un helper par champ et par rang. Pas de JSON, même par cellule. | Choix structurel |
| **INV-V1-D** | `sensor.pluie_journaliere` est la source canonique unique. Aucune source alternative tolérée. | Source |
| **INV-V1-E** | Top 10 strict. Aucune profondeur supérieure ou inférieure tolérée en V1. | Paramètre |
| **INV-V1-F** | Cycle `daily` exclusivement. `weekly`, `monthly` hors V1. | Cycle |

---

## 10. Hors-scope V1

Les éléments suivants sont explicitement exclus du périmètre V1 :

- toute instance autre que `pluie_journalier` (humidex, CO₂, ECS, chaleur, conso, etc.) ;
- le cycle `weekly` et toute autre granularité que `daily` ;
- toute mécanique d'abstraction visant à réduire la verbosité des 20 helpers de rangs (factorisation par template, génération auto) ;
- toute persistance hors HA (fichier JSON, base externe, export NAS) ;
- toute UI dédiée (cartes Lovelace, dashboards) : la consommation UI est définie hors contrat ;
- toute procédure automatisée de réinitialisation ou de réparation : la résolution d'anomalie reste manuelle en V1 ;
- toute extension du capteur d'anomalie au-delà de B1+B2+B3+B4 ;
- toute exposition de l'historique des évaluations passées (le palmarès ne mémorise que les extrêmes, pas la séquence).

---

## 11. Extensions futures envisagées

Les évolutions suivantes sont identifiées comme pistes naturelles, **sans aucune valeur normative** dans la V1 :

- **Cycle hebdomadaire** : instance `utility_meter` de clé `pluie_semaine` (cycle `weekly`), exposant l'entité runtime `sensor.pluie_hebdomadaire` (entity_id dérivé du `name` « Pluie (hebdomadaire) », non de la clé). Sans changement du contrat de primitive, simple ajout d'une instance.
- **Autres domaines métier** : humidex, CO₂, ECS, conso électrique, cardio. Chaque instance suit la grammaire de la section 3.
- **Topologie A2** : remplacement des 20 helpers par rang par 10 `input_text` contenant un mini-JSON. Optimisation de verbosité, contractuellement neutre si le mini-JSON reste observable.
- **Records de minima** : symétrique, registre des N valeurs les plus basses. Nécessite une extension de la grammaire (paramètre `sens` ∈ `{ max, min }`).
- **Records par sous-période** : records par mois, records par année. Nécessite une grammaire d'agrégation supplémentaire.
- **Procédure de réinitialisation automatisée** : `script.palmares_<instance_id>_reset`. Pertinent si le nombre d'instances croît.

Aucune de ces extensions ne doit être implémentée tant qu'elle n'a pas fait l'objet d'une instruction dédiée et d'une mise à jour explicite du présent contrat.

---

## 12. Conformité

Une implémentation est conforme au présent contrat si et seulement si :

1. Toutes les entités listées en 4.3 existent avec les noms exacts spécifiés.
2. Les deux automations respectent les déclenchements et comportements définis en 5.1 et 5.2.
3. La politique d'insertion respecte 5.3 (FIFO, compacité, eviction au-delà du top_n).
4. Le capteur de synthèse expose les attributs définis en 6.3 et son état suit 6.2.
5. Le capteur d'anomalie évalue les quatre conditions B1+B2+B3+B4 conformément à 7.3.
6. Tous les invariants de la section 9 sont respectés.

Toute déviation par rapport à ces six points constitue une non-conformité et doit être traitée comme une dette à résorber ou une évolution explicite du contrat.

---

## Attributs de présentation (dérivés)

Le capteur synthèse `sensor.palmares_pluie_journalier` enrichit chaque objet de
l'attribut `records` d'un champ de **présentation** destiné à l'affichage humain.

| Clé de `records[]` | Nature | Format | Rôle |
|---|---|---|---|
| `date` | **canonique** | ISO `YYYY-MM-DD` | tri, comparaison, parsing, fraîcheur |
| `date_affichage` | **dérivé (présentation)** | `DD/MM/YYYY` | restitution UI uniquement |

- La date ISO `records[].date` reste l'**unique donnée canonique** : toute logique
  (classement, comparaison, `strptime('%Y-%m-%d')`, fraîcheur) la consomme.
- `records[].date_affichage` est une **projection de présentation** dérivée de la
  date ISO — **aucune incidence** sur le classement, les valeurs météo ou la fraîcheur.
- L'UI Lovelace affiche `records[].date_affichage` **sans transformation locale**
  (pas de `strftime` / `split` / `replace` / `as_datetime` côté carte).
- Date vide ou invalide → restitution de la valeur brute (aucune date fabriquée).

> Ajout 2026-07-07 — attribut de présentation dérivé `records[].date_affichage`.
> La date ISO reste canonique ; aucun impact sur classement, valeurs ou fraîcheur.

---

*Fin du contrat — version 1.1.*
