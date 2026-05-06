# ARSENAL — CONTRAT : Référentiel BSSID Maison

## 1. Rôle

Ce contrat définit le référentiel canonique des BSSID Wi-Fi de la maison, utilisé pour :

- qualifier la présence Wi-Fi locale
- fiabiliser les décisions de sécurité
- éviter toute dépendance à des SSID (non fiables)

---

## 2. Nature du référentiel

Le référentiel BSSID est :

- **dynamique** → enrichi automatiquement
- **persistant** → conservé entre redémarrages
- **déterministe** → sans ambiguïté de format, sérialisation triée stable
- **non ordonné** → ensemble logique (set) — l'ordre n'a pas de sens métier

---

## 3. Support de stockage

**Support actuel (imposé)**

```
input_text.bssid_maison
```

**Contraintes structurelles**

- longueur maximale effective : **255 caractères** (limite HA, non contournable)
- stockage sous forme de chaîne plate
- séparation par virgule

---

## 4. Format canonique d'un BSSID

Un BSSID est stocké sous la forme :

```
xxxxxxxxxxxx
```

| Propriété | Valeur |
|-----------|--------|
| longueur | 12 caractères |
| alphabet | `[0-9a-f]` |
| casse | minuscules uniquement |
| séparateurs | aucun (ni `:` ni `-`) |

**Exemple**

```
3460f9386080
```

---

## 5. Format du référentiel

```
bssid1, bssid2, bssid3
```

**Règles**

- séparateur : `,`
- espaces autorisés mais ignorés à la lecture
- unicité obligatoire
- ordre non significatif

---

## 6. Normalisation obligatoire

Toute donnée manipulée doit être normalisée avant usage.

**Transformation canonique**

```
| lower
| replace(':', '')
| replace('-', '')
| trim
```

**Champ d'application** : apprentissage, lecture, comparaison.

---

## 7. Principe de cohérence source ↔ personne

Ce principe est **fondateur** du mécanisme d'apprentissage. Il prévaut sur toute autre logique d'autorisation.

### 7.1 Énoncé

Un BSSID ne peut être intégré au référentiel **que si** la personne associée à la source qui l'observe est elle-même présente dans la zone `'Maison securite'` au moment de l'apprentissage.

### 7.2 Couplage canonique source / personne

| Source d'observation | Personne associée |
|----------------------|-------------------|
| `sensor.telephone_antoine_bssid_dynamic` | `person.valentin` |
| `sensor.telephone_constance_bssid_dynamic` | `person.constance` |

Ce couplage est **strict, unidirectionnel et non substituable**. Il constitue un invariant du contrat.

### 7.3 Règle d'exclusion absolue

Un BSSID observé par la source d'une personne A **ne peut jamais** être appris au seul motif qu'une personne B est présente dans `'Maison securite'`.

La présence d'un tiers — même adulte, même titulaire de la condition de garde — **ne légitime aucun apprentissage** sur une source qui ne lui est pas couplée.

### 7.4 Indépendance des sources

Chaque source est évaluée **indépendamment** des autres :

- une source dont la personne associée est absente est **inerte**
- une source dont la personne associée est présente est **éligible**
- l'éligibilité d'une source n'a aucun effet sur les autres sources
- la fusion des candidats issus de plusieurs sources éligibles est autorisée mais s'effectue source par source

### 7.5 Justification architecturale

La condition de présence globale précédente (« un adulte dans `'Maison securite'` ») était insuffisante : elle créait une asymétrie entre la **localisation autorisante** et la **localisation observante**. Un BSSID externe observé par le téléphone d'une personne en déplacement pouvait être validé par la simple présence d'une autre personne au domicile, polluant le référentiel.

Le principe de cohérence source ↔ personne supprime cette asymétrie en rendant l'autorisation d'apprentissage **locale à la source**.

---

## 8. Apprentissage

### 8.1 Conditions d'éligibilité par source

Pour chaque source `S` couplée à la personne `P` (cf. §7.2), la source est **éligible** si et seulement si :

- `P.state == 'Maison securite'`
- `S.state` est défini, non vide, distinct de `unknown` / `unavailable` / `None`

L'éligibilité est évaluée **indépendamment** pour chaque source, à chaque déclenchement de l'automation d'apprentissage.

### 8.2 Construction de l'ensemble candidat

L'ensemble des candidats à l'apprentissage est construit comme l'**union** des BSSID issus des seules sources éligibles, après normalisation (§6) et validation (§8.4).

Formellement :

```
candidats = ⋃ { normalize(S.state) | S éligible ∧ valide(S.state) }
```

Aucun BSSID issu d'une source non éligible ne peut figurer dans cet ensemble, indépendamment de la présence d'autres personnes.

### 8.3 Détection des nouveaux BSSID

`binary_sensor.wifi_nouveau_bssid` est `on` si et seulement si :

```
candidats \ référentiel ≠ ∅
```

c'est-à-dire s'il existe au moins un BSSID candidat (issu d'une source éligible) absent du référentiel actuel.

### 8.4 Validation des candidats

Avant intégration, chaque candidat doit :

- être converti en chaîne
- être normalisé (§6)
- avoir exactement 12 caractères
- ne contenir que des caractères `[0-9a-f]`

Tout candidat ne respectant pas ces conditions est **ignoré sans écriture**. Les valeurs `unknown`, `unavailable`, `None`, vide ou mal formées sont concernées.

### 8.5 Règles d'intégration

- seuls les BSSID normalisés et validés sont intégrés
- aucun doublon autorisé
- fusion via ensemble logique (set)
- la fusion respecte la sérialisation déterministe (§13)

### 8.6 Garde résiduelle (défense en profondeur)

L'automation d'apprentissage ré-évalue, **au moment de l'écriture**, la cohérence source ↔ personne pour chaque candidat retenu. Tout candidat dont la source est devenue non éligible entre la détection et l'écriture est **rejeté**.

Cette garde couvre les cas de transition (cf. §10) où l'état d'une personne change pendant la fenêtre de traitement.

---

## 9. Contraintes fortes

### 9.1 Limite de capacité

```
longueur totale <= 255 caractères
```

**Capacité opérationnelle maximale : 16 BSSID**

Calcul : 1 BSSID = 12 car. + 2 car. de séparateur `, ` = 14 car. par entrée.
`255 / 14 ≈ 18.2` — avec marge de sécurité et dernier élément sans séparateur : **16 BSSID maximum fiable**.

**Seuil d'alerte métier : 14 BSSID**

L'infrastructure Wi-Fi de la maison comprend environ 10 BSSID attendus (~5 bornes Deco × 2 BSSID par borne).
Tout dépassement du seuil de 14 BSSID est considéré comme **anormal** et doit déclencher un audit manuel.
Il ne s'agit pas d'un cas de saturation normale à gérer automatiquement.

### 9.2 Stratégie en cas de dépassement

| Condition | Action |
|-----------|--------|
| longueur projetée > 255 | ❌ aucune écriture dans `input_text` |
| | ⚠️ journalisation obligatoire (`warning`) |
| | ⛔ ajout rejeté pour cette tentative |
| count > 14 | 🔴 signal d'anomalie — audit manuel obligatoire |

**Aucune purge automatique.** Le référentiel ne doit pas atteindre ce seuil dans des conditions normales d'exploitation. Un dépassement révèle une pollution ou une dérive à investiguer, pas un cas à absorber silencieusement.

---

## 10. Cas limites

### 10.1 Latence d'état

Les états de `person.*` et des sources `sensor.*_bssid_dynamic` ne sont pas synchronisés instantanément. Une transition de zone peut précéder ou suivre la mise à jour du BSSID observé de plusieurs secondes.

**Règle** : l'éligibilité est évaluée sur l'**état courant** au moment du déclenchement. Aucune fenêtre de tolérance n'est admise. La garde résiduelle (§8.6) absorbe les transitions intervenant pendant le traitement.

### 10.2 Transition Wi-Fi

Lors d'un changement de borne Deco (roaming), la source publie successivement plusieurs BSSID en quelques secondes. Chaque transition déclenche une réévaluation indépendante de l'éligibilité et de la validation.

**Règle** : aucun lissage, aucune mémorisation inter-transition. Chaque BSSID observé est traité comme un événement indépendant.

### 10.3 Démarrage / redémarrage

Au boot, les entités `person.*` et `sensor.*_bssid_dynamic` peuvent transiter par `unknown` / `unavailable` avant de se stabiliser.

**Règles** :

- toute source en état non défini est **inerte** (cf. §8.1) → aucun apprentissage possible
- toute personne en état non défini est **non présente** au sens du contrat → la source couplée est inerte
- aucune écriture spéculative au démarrage

### 10.4 Personne en transit

Une personne quittant ou rejoignant `'Maison securite'` produit, pendant la transition, des observations potentiellement incohérentes (BSSID maison perçu depuis l'extérieur immédiat, ou BSSID externe perçu depuis l'intérieur via réseau invité voisin).

**Règle** : la cohérence source ↔ personne ne lève pas ces ambiguïtés à elle seule. Elle garantit uniquement que la **personne couplée** est dans la zone autorisante. La validation §8.4 et l'invariant §13 (appartenance à l'infrastructure locale) restent les remparts contre la pollution résiduelle.

### 10.5 Sources désactivées ou supprimées

Si une source est physiquement supprimée (téléphone non remplacé, intégration déconnectée), son éligibilité est durablement à `false`. Aucun apprentissage n'a lieu via ce canal. Le couplage §7.2 doit être mis à jour explicitement par évolution de contrat.

---

## 11. Exploitation

Le référentiel est utilisé comme :

- source unique pour `binary_sensor.presence_wifi_maison`
- base de comparaison avec les BSSID observés

**Règle** : la comparaison doit se faire après normalisation des deux côtés.

`binary_sensor.presence_wifi_maison` est le **seul point d'accès décisionnel** au référentiel pour la qualification de présence.

La lecture directe de `input_text.bssid_maison` n'est autorisée que pour :

- le mécanisme d'apprentissage du référentiel
- les capteurs ou scripts explicitement dédiés à sa normalisation, validation ou diagnostic

Toute autre lecture directe constitue une violation de ce contrat.

---

## 12. Interdictions

- ❌ stocker des BSSID avec `:` ou `-`
- ❌ dépendre du format brut des intégrations
- ❌ écrire sans contrôle de capacité
- ❌ utiliser plusieurs helpers pour un même référentiel
- ❌ lire `input_text.bssid_maison` hors des contextes autorisés par §11
- ❌ apprendre un BSSID issu d'une source dont la personne couplée n'est pas dans `'Maison securite'`
- ❌ utiliser la présence d'une personne pour autoriser l'apprentissage sur la source d'une autre personne
- ❌ fusionner les candidats avant filtrage par éligibilité de source

---

## 13. Invariants

- unicité des BSSID dans le référentiel
- format canonique respecté à l'écriture
- référentiel directement exploitable après simple découpage par virgule et normalisation élémentaire
- sérialisation déterministe : lors de toute écriture, les BSSID sont triés selon un ordre stable explicite (tri lexicographique)
- aucune dépendance à l'ordre pour les décisions métier
- tous les BSSID du référentiel appartiennent à l'infrastructure Wi-Fi locale contrôlée (bornes Deco de la maison, y compris les BSSID explicitement admis de cette infrastructure) ; tout BSSID d'origine extérieure ou non autorisée constitue une pollution
- **cohérence source ↔ personne** : tout BSSID intégré au référentiel a été observé par une source dont la personne couplée était dans `'Maison securite'` au moment de l'apprentissage
- **étanchéité inter-sources** : aucune source ne peut tirer parti de l'éligibilité d'une autre source

---

## 14. Limites connues

- capacité opérationnelle fiable : 16 BSSID maximum (seuil d'alerte métier : 14)
- limite de 255 caractères imposée par HA, non contournable via `max`
- dépendance au support `input_text`
- absence de TTL / purge automatique
- couplage source ↔ personne défini en dur dans le contrat ; toute évolution du parc téléphonique requiert une révision contractuelle
- la cohérence source ↔ personne ne couvre pas les pollutions par BSSID externe perçu depuis le domicile (cf. §10.4) ; ce vecteur reste couvert par la validation §8.4 et l'invariant d'appartenance §13

---

## 15. Évolution future (hors périmètre)

- migration vers attribut de sensor
- stockage persistant externe
- gestion de vieillissement / purge
- élargissement du couplage à d'autres sources (tablettes, ordinateurs portables)

---

## 16. Structure d'attributs recommandée pour `binary_sensor.wifi_nouveau_bssid`

Le sensor expose, en plus de son état booléen, les attributs suivants. Cette structure est **normative** et constitue l'interface de diagnostic et d'apprentissage.

| Attribut | Type | Description |
|----------|------|-------------|
| `candidats` | `string` | Union CSV des BSSID candidats nouveaux, normalisés et validés, issus des seules sources éligibles. Tri lexicographique. Chaîne vide si aucun candidat. |
| `candidats_antoine` | `string` | CSV des BSSID candidats issus de `sensor.telephone_antoine_bssid_dynamic`, uniquement si `person.valentin` est dans `'Maison securite'`. Chaîne vide sinon. |
| `candidats_constance` | `string` | CSV des BSSID candidats issus de `sensor.telephone_constance_bssid_dynamic`, uniquement si `person.constance` est dans `'Maison securite'`. Chaîne vide sinon. |
| `sources_eligibles` | `string` | CSV des sources actuellement éligibles : `antoine`, `constance`. |
| `sources_inertes` | `string` | CSV des sources actuellement inertes : `antoine`, `constance`. |

**Règles** :

- les attributs sont recalculés à chaque évaluation du sensor
- `candidats` est l'union de `candidats_antoine` et `candidats_constance`
- aucune source non éligible ne contribue à `candidats`, `candidats_antoine` ou `candidats_constance`
- la sérialisation des chaînes CSV respecte l'ordre lexicographique stable (§13)

---

## 17. Entités du périmètre

Les entités suivantes sont gouvernées par ce contrat ou en constituent l'infrastructure directe.

### 17.1 Référentiel

| Entité | Rôle |
|--------|------|
| `input_text.bssid_maison` | Support de stockage du référentiel canonique |

### 17.2 Sources d'observation et couplage

| Entité | Personne couplée | Rôle |
|--------|------------------|------|
| `sensor.telephone_antoine_bssid_dynamic` | `person.valentin` | BSSID actuel du téléphone d'Antoine — abstraction stable sur `input_text.telephone_antoine_wifi_bssid` |
| `sensor.telephone_constance_bssid_dynamic` | `person.constance` | BSSID actuel du téléphone de Constance — abstraction stable sur `input_text.telephone_constance_wifi_bssid` |

Le couplage source ↔ personne est **normatif** (cf. §7.2). Toute modification requiert une évolution de contrat.

### 17.3 Détection et apprentissage

| Entité | Rôle |
|--------|------|
| `binary_sensor.wifi_nouveau_bssid` | Détecte un BSSID inconnu du référentiel, issu d'une source éligible — expose les candidats en CSV canonique, globalement et par source, via les attributs définis en §16 |
| `automation.10120000000016` | Enrichit le référentiel sur déclenchement métier, sous condition de cohérence source ↔ personne, avec garde résiduelle à l'écriture |

### 17.4 Exploitation

| Entité | Rôle |
|--------|------|
| `binary_sensor.presence_wifi_maison` | Seul point d'accès décisionnel au référentiel pour la qualification de présence Wi-Fi |

### 17.5 Personnes du couplage

| Entité | Rôle |
|--------|------|
| `person.valentin` | Antoine — sa présence dans `'Maison securite'` conditionne l'éligibilité de `sensor.telephone_antoine_bssid_dynamic` |
| `person.constance` | Constance — sa présence dans `'Maison securite'` conditionne l'éligibilité de `sensor.telephone_constance_bssid_dynamic` |
