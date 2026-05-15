# Contrat — Système d'audit patrimonial Arsenal NAS — V1.1.1

**Version** : v1.1.1
**Statut** : contrat figé
**Amende** : v1.1.0 (`contrat_audit.md`)
**Périmètre** : refonte doctrinale — pluralité des autorités runtime,
classification des plateformes, séparation observation / anomalie.

---

## 1. Objet et changement de nature

### 1.1 Objet

Le système V1.1.1 amende structurellement V1.1.0 pour refléter ce que
le moteur est devenu en pratique : non plus un vérificateur statique
de références YAML, mais un **modèle d'existence runtime Home
Assistant exploitable hors-ligne**.

### 1.2 Changement de nature acté

V1.0 et V1.1.0 traitaient le `core.entity_registry` comme référentiel
quasi-unique d'existence, et l'index déclaratif Arsenal comme
correctif marginal.

V1.1.1 acte que :

> Le moteur d'audit n'est pas un détecteur de références cassées.
> C'est un modèle d'existence runtime Home Assistant, dont la
> détection de références cassées est un sous-produit.

Cette reformulation est doctrinale. Elle change la lecture des
verdicts du moteur et la façon dont les rapports sont structurés.

### 1.3 Conséquences directes

- L'existence d'une entité runtime peut être attestée par plusieurs
  autorités, dont aucune n'est universelle.
- Une entité absente du `core.entity_registry` n'est pas, par défaut,
  une anomalie : ce sont les autorités attendues pour chaque
  plateforme qui décident.
- Le rapport distingue formellement **anomalies actionnables** et
  **observations patrimoniales**.

---

## 2. Phrase centrale

> Une entité est considérée comme inexistante en runtime si et seulement
> si elle est absente de toutes les autorités attendues pour sa plateforme,
> après application du pipeline littéral → canonique → déclaratif.

---

## 3. Classification des autorités de plateformes

### 3.1 Principe — pluralité des autorités

Toute plateforme Home Assistant exposant des entités relève d'une et
une seule classe d'autorité au regard du moteur :

| Classe | Token | Sémantique |
|---|---|---|
| A | `registry_authority` | L'autorité attendue d'existence est `core.entity_registry`. Absence du registry = anomalie. |
| B | `runtime_yaml_authority` | L'autorité attendue d'existence est l'index déclaratif Arsenal. Absence du registry = observation patrimoniale normale. |

La classe d'une plateforme est une propriété **architecturale**, non
configurable au cas par cas. Elle est inscrite dans le contrat.

### 3.2 Plateformes classées `runtime_yaml_authority`

Au titre de V1.1.1, sont classées `runtime_yaml_authority` :

| Plateforme | Dossier source | Dérivation `entity_id` |
|---|---|---|
| `group` (YAML legacy) | `02_groups/` | `direct_key` |
| `utility_meter` | `utility_meter.yaml` | `direct_key` |
| `statistics` (sensor platform) | `13_sensor_platforms/` | `derived_from_name` |
| `history_stats` (sensor platform) | `13_sensor_platforms/` | `derived_from_name` |
| `alarm_control_panel` manual | `16_template_alarm_panels/` | `derived_from_name` |
| `zone` (YAML) | `17_zones/` | `direct_key` |

Toute autre plateforme est implicitement `registry_authority` jusqu'à
promotion formelle selon §9.4.

### 3.3 Hors périmètre V1.1.1

Restent hors périmètre, sans préjuger de leur classe future :

- `min_max`, `filter`, `derivative`, `integration`, `trend`, `threshold`
- déclarations dynamiques par pyscript, AppDaemon, intégrations custom
- blueprints, devices, areas, MQTT discovery, Lovelace

Cette fermeture est délibérée. Une plateforme hors périmètre est
traitée comme `registry_authority` par défaut.

---

## 4. Fonction `_ha_slugify`

Inchangée par rapport à V1.1.0. Voir §4 du contrat précédent.
Localisation, comportement, validation et garde-fou doctrinal
demeurent identiques.

---

## 5. Modèle de données

### 5.1 Champ `derivation` sur `DeclaredEntity`

Inchangé. Voir V1.1.0 §5.

### 5.2 Champ `authority_class` ajouté

```python
@dataclass(slots=True)
class DeclaredEntity:
    entity_id: str | None
    domain: str | None
    platform: str
    file_path: Path
    raw_name: str | None
    raw_unique_id: str | None
    confidence: str
    derivation: str
    authority_class: str  # nouveau : "registry_authority" | "runtime_yaml_authority"
```

### 5.3 Invariant

Toute `DeclaredEntity` produite par un extracteur V1.1.1 porte une
valeur `authority_class` non nulle, cohérente avec la classification
§3.

---

## 6. Pipeline de résolution à trois étages

### 6.1 Inchangé dans sa mécanique

Les trois étages — littéral, canonique, déclaratif — demeurent dans
l'ordre établi par V1.1.0 §6.2.

### 6.2 Amendement de l'étage 3

L'étage 3 ne produit plus systématiquement `declared_outside_registry`
lorsqu'une déclaration Arsenal est trouvée hors registry. Le verdict
dépend désormais de la classe d'autorité de la plateforme déclarante :

```text
Étage 3 — Match déclaratif Arsenal

référence présente dans l'index déclaratif Arsenal ?
  oui →
    si declared.authority_class == "runtime_yaml_authority":
        → émission de runtime_yaml_observation
        → cette observation N'EST PAS comptée dans total_anomalies
    sinon (registry_authority) ET entité high confidence
                                ET absente du registry:
        → émission de declared_outside_registry (P3)
        → comptée dans total_anomalies
    fin (pas de broken_reference)
  non → broken_reference selon V1.0
```

### 6.3 Invariants du pipeline

Identiques à V1.1.0 §6.3.

---

## 7. Catégories d'anomalies et observations

### 7.1 `non_canonical_entity_id_case`

Inchangée. P2, comptée dans `total_anomalies`. Voir V1.1.0 §7.1.

### 7.2 `runtime_yaml_observation` (nouveau)

| Champ | Valeur |
|---|---|
| Token code | `runtime_yaml_observation` |
| Libellé rapport | « Observation patrimoniale » |
| Sévérité | aucune (hors échelle P0–P3) |
| Confidence | high |
| Sémantique | Entité déclarée par plateforme `runtime_yaml_authority`, fonctionnelle en runtime, absence du registry conforme à la nature de la plateforme. |
| Évidence requise | `entity_id` reconstitué, plateforme, fichier source, `authority_class` |
| Comptée dans `total_anomalies` | **Non** |
| Section de rapport | « Observations patrimoniales » (séparée des anomalies) |
| Notes type | « Entité déclarée par plateforme `<platform>` (classe `runtime_yaml_authority`). Absence du registry conforme. Aucune action requise. » |

### 7.3 `declared_outside_registry` (redéfinie)

| Champ | Valeur |
|---|---|
| Token code | `declared_outside_registry` |
| Libellé rapport | « Déclaration hors registry attendu » |
| Sévérité | P3 |
| Confidence | high |
| Sémantique | Entité déclarée par plateforme classée `registry_authority`, dont la déclaration Arsenal est de haute confiance, mais qui est absente du `core.entity_registry`. Cas résiduel anormal. |
| Évidence requise | `entity_id`, plateforme, fichier, `authority_class = registry_authority` |
| Comptée dans `total_anomalies` | **Oui** |
| Notes type | « La plateforme `<platform>` devrait inscrire ses entités au registry. La déclaration est présente, l'enregistrement runtime ne l'est pas. Investigation requise : registry corrompu, migration en cours, ou divergence d'extracteur. » |

### 7.4 Statut opérationnel

| Catégorie | Comptée anomalies | Notification | Blocage |
|---|---|---|---|
| `non_canonical_entity_id_case` (P2) | Oui | Non | Non |
| `runtime_yaml_observation` | **Non** | Non | Non |
| `declared_outside_registry` (P3) | Oui | Non | Non |

---

## 8. Extracteurs V1.1.1

Les extracteurs V1.1.0 §8 sont reconduits avec ajout obligatoire du
champ `authority_class = "runtime_yaml_authority"` pour toutes les
plateformes listées §3.2. Deux extracteurs sont ajoutés :

### 8.5 `utility_meter` (`utility_meter.yaml`)

```yaml
nom_du_meter:
  source: sensor.xxx
  cycle: daily
```

→ `entity_id = sensor.<nom_du_meter>` (selon cycles déclarés)
→ `derivation = direct_key`
→ `authority_class = runtime_yaml_authority`
→ `confidence = high`

### 8.6 `zone` (`17_zones/`)

```yaml
- name: Maison
  latitude: ...
  longitude: ...
```

→ `entity_id = zone.<_ha_slugify(name)>`
→ `derivation = derived_from_name`
→ `authority_class = runtime_yaml_authority`
→ `confidence = high`

---

## 9. Statut d'autorité — refonte complète

### 9.1 Autorité registry

`core.entity_registry` est l'autorité d'existence des plateformes
classées `registry_authority` (§3.1, classe A).

Pour ces plateformes :

- présence au registry → entité existante runtime, confirmée
- absence au registry → entité présumée inexistante, sauf cas résiduel
  `declared_outside_registry`

### 9.2 Autorité runtime YAML

L'index déclaratif Arsenal est l'autorité d'existence des plateformes
classées `runtime_yaml_authority` (§3.1, classe B).

Pour ces plateformes :

- présence dans l'index déclaratif → entité existante runtime,
  attestée par la déclaration YAML
- absence simultanée de l'index ET du registry → entité présumée
  inexistante

Pour les plateformes runtime_yaml_authority,
le core.entity_registry n'est pas considéré comme
une autorité opposable d'existence ou d'absence runtime.
Sa présence éventuelle reste informative.

### 9.3 Hiérarchie des autorités

| Plateforme | Autorité primaire | Autorité secondaire | Autorité ignorée |
|---|---|---|---|
| classe A (`registry_authority`) | registry | index déclaratif (pour `declared_outside_registry`) | — |
| classe B (`runtime_yaml_authority`) | index déclaratif | — | registry |

**Aucune autorité n'est universelle.** Le moteur ne reconnaît pas de
« super-registry » qui trancherait entre A et B. La classification §3
est la seule trancheuse.

### 9.4 Conditions de promotion d'une plateforme en `runtime_yaml_authority`

Une plateforme ne peut être ajoutée à §3.2 que si l'ensemble des cinq
critères suivants est satisfait et documenté :

1. **Entité fonctionnelle observée** : présence vérifiée dans
   `states.json` ou équivalent runtime, avec valeur cohérente.
2. **Absence confirmée du registry** : vérification directe de
   `core.entity_registry` pour cette entité, négative.
3. **Reproductibilité** : au moins deux entités distinctes de la
   plateforme exhibent simultanément les points 1 et 2.
4. **Non-actionnabilité** : l'inscription manuelle de l'entité au
   registry n'apporte aucun bénéfice runtime, ou la plateforme HA ne
   prévoit pas cette inscription par conception.
5. **Preuve documentaire HA upstream** *(critère obligatoire)* :
   référence explicite à la documentation Home Assistant officielle ou
   au code source de la plateforme (`homeassistant/components/<platform>/`)
   établissant que la plateforme ne crée pas d'entrée registry par
   conception. À défaut de documentation, lecture argumentée du code
   upstream, citée en évidence.

L'absence d'un seul critère bloque la promotion. La classification
demeure `registry_authority` par défaut.

### 9.5 Garde-fou doctrinal

Le moteur ne décide jamais seul de la classe d'une plateforme.
Aucune heuristique runtime (« je vois beaucoup d'entités hors
registry, donc je classe la plateforme B ») n'est autorisée. La
classification §3 est exclusivement contractuelle.

---

## 10. Test d'acceptation V1.1.1

L'implémentation V1.1.1 est validée si et seulement si le rapport
produit sur la sauvegarde de référence satisfait les **quatre** cas
suivants simultanément :

| Cas | Comportement attendu V1.1.1 |
|---|---|
| `input_boolean.bouclage_visiteur` | `broken_reference` P0 (inchangé) |
| `alarm_control_panel.alarme_maison` | `runtime_yaml_observation`, **non comptée** dans `total_anomalies` |
| `sensor.deltat_chambre_arnaud` | `non_canonical_entity_id_case` P2 (inchangé) |
| **Compteur global** | `total_anomalies` ne comprend **aucune** `runtime_yaml_observation`. Le rapport expose `total_observations_patrimoniales` séparément. |

Aucun arbitrage à la baisse autorisé.

---

## 11. Frontières assumées V1.1.1

Le système V1.1.1 ne fait pas :

- la conformité formelle avec `homeassistant.util.slugify` au-delà du
  corpus de test embarqué ;
- la détection des `domain_mismatch` ;
- l'extension aux plateformes legacy hors §3.2 ;
- la mesure du taux de couverture par l'index déclaratif ;
- la classification automatique des plateformes (interdite par §9.5).

---

## 12. Évolutions futures (V1.2 et au-delà)

Pour mémoire, hors périmètre V1.1.1 :

- Mode `--validate-slugify` (V1.2 candidate).
- Détection `domain_mismatch`.
- Promotion éventuelle de `min_max`, `filter`, `integration` en
  `runtime_yaml_authority` après application stricte de §9.4.
- Mesure de la couverture déclarative.
- Sortie machine du rapport au format JSON structuré distinguant
  `anomalies[]` et `observations[]`.

---

## 13. Versionnage et gouvernance

Le contrat V1.1.1 amende V1.1.0 sur les points suivants :

| Section V1.1.0 | Statut V1.1.1 |
|---|---|
| §1 (Objet) | Réécrit — changement de nature acté |
| §3 (Périmètre) | Réécrit — classification des autorités |
| §5 (Modèle) | Étendu — champ `authority_class` |
| §6 (Pipeline) | Étage 3 amendé |
| §7 (Catégories) | Refonte — séparation observation / anomalie |
| §8 (Extracteurs) | Ajout `utility_meter`, `zone` |
| §9 (Autorité) | Réécriture complète — pluralité, hiérarchie, promotion |
| §10 (Acceptation) | Étendu — 4e cas sur compteur global |
| §2, §4, §11, §12 | Conservés ou ajustés à la marge |

---

## 14. Changelog doctrinal

**V1.0.0** — Le moteur considère `core.entity_registry` comme
référentiel quasi-unique. Toute absence est suspecte.

**V1.1.0** — Introduction d'un index déclaratif Arsenal comme
correctif pour quatre plateformes legacy nommées. Émergence implicite
de la notion de pluralité.

**V1.1.1** *(présent contrat)* — La pluralité est formalisée. Le
moteur change de nature : il devient un modèle d'existence runtime, et
non plus un vérificateur de références. Séparation stricte entre
anomalie actionnable et observation patrimoniale. Règle de promotion
durcie (5 critères, dont preuve documentaire upstream obligatoire).
Garantie doctrinale contre l'effet « liste poubelle ».

---

*Fin du contrat V1.1.1.*