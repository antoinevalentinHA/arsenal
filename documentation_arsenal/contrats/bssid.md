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

## 7. Apprentissage

**Conditions d'entrée**

- `binary_sensor.wifi_nouveau_bssid = on`
- `person.valentin` ou `person.constance` dans `'Maison securite'`

> La condition de garde est évaluée par l'automation, pas par le sensor.
> Elle exclut explicitement : visiteur seul, babysitting, enfants sans adulte.

**Règles**

- seuls les BSSID normalisés sont intégrés
- aucun doublon autorisé
- fusion via ensemble logique (set)

### 7.1 Validation des candidats

Avant fusion, chaque candidat doit :

- être converti en chaîne
- être normalisé (§6)
- avoir exactement 12 caractères
- ne contenir que des caractères `[0-9a-f]`

Tout candidat ne respectant pas ces conditions est **ignoré sans écriture**. Les valeurs `unknown`, `None`, vide ou mal formées sont concernées.

---

## 8. Contraintes fortes

### 8.1 Limite de capacité

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

### 8.2 Stratégie en cas de dépassement

| Condition | Action |
|-----------|--------|
| longueur projetée > 255 | ❌ aucune écriture dans `input_text` |
| | ⚠️ journalisation obligatoire (`warning`) |
| | ⛔ ajout rejeté pour cette tentative |
| count > 14 | 🔴 signal d'anomalie — audit manuel obligatoire |

**Aucune purge automatique.** Le référentiel ne doit pas atteindre ce seuil dans des conditions normales d'exploitation. Un dépassement révèle une pollution ou une dérive à investiguer, pas un cas à absorber silencieusement.

---

## 9. Exploitation

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

## 10. Interdictions

- ❌ stocker des BSSID avec `:` ou `-`
- ❌ dépendre du format brut des intégrations
- ❌ écrire sans contrôle de capacité
- ❌ utiliser plusieurs helpers pour un même référentiel
- ❌ lire `input_text.bssid_maison` hors des contextes autorisés par §9

---

## 11. Invariants

- unicité des BSSID dans le référentiel
- format canonique respecté à l'écriture
- référentiel directement exploitable après simple découpage par virgule et normalisation élémentaire
- sérialisation déterministe : lors de toute écriture, les BSSID sont triés selon un ordre stable explicite (tri lexicographique)
- aucune dépendance à l'ordre pour les décisions métier
- tous les BSSID du référentiel appartiennent à l'infrastructure Wi-Fi locale contrôlée (bornes Deco de la maison, y compris les BSSID explicitement admis de cette infrastructure) ; tout BSSID d'origine extérieure ou non autorisée constitue une pollution

---

## 12. Limites connues

- capacité opérationnelle fiable : 16 BSSID maximum (seuil d'alerte métier : 14)
- limite de 255 caractères imposée par HA, non contournable via `max`
- dépendance au support `input_text`
- absence de TTL / purge automatique

---

## 13. Évolution future (hors périmètre)

- migration vers attribut de sensor
- stockage persistant externe
- gestion de vieillissement / purge

---

## 14. Entités du périmètre

Les entités suivantes sont gouvernées par ce contrat ou en constituent l'infrastructure directe.

### 14.1 Référentiel

| Entité | Rôle |
|--------|------|
| `input_text.bssid_maison` | Support de stockage du référentiel canonique |

### 14.2 Sources d'observation

| Entité | Rôle |
|--------|------|
| `sensor.telephone_antoine_bssid_dynamic` | BSSID actuel du téléphone d'Antoine — abstraction stable sur `input_text.telephone_antoine_wifi_bssid` |
| `sensor.telephone_constance_bssid_dynamic` | BSSID actuel du téléphone de Constance — abstraction stable sur `input_text.telephone_constance_wifi_bssid` |

### 14.3 Détection et apprentissage

| Entité | Rôle |
|--------|------|
| `binary_sensor.wifi_nouveau_bssid` | Détecte un BSSID inconnu du référentiel — expose les candidats en CSV canonique via l'attribut `candidats` |
| `automation.10120000000016` | Enrichit le référentiel sur déclenchement métier, sous condition de garde adulte |

### 14.4 Exploitation

| Entité | Rôle |
|--------|------|
| `binary_sensor.presence_wifi_maison` | Seul point d'accès décisionnel au référentiel pour la qualification de présence Wi-Fi |

### 14.5 Condition de garde

| Entité | Rôle |
|--------|------|
| `person.valentin` | Antoine — présence dans `'Maison securite'` requise pour autoriser l'apprentissage |
| `person.constance` | Constance — présence dans `'Maison securite'` requise pour autoriser l'apprentissage |
