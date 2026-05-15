# Contrat — Domaine Home Assistant `arsenal_self`

**Version** : v1.0.0
**Statut** : actif
**Périmètre** : exposition Home Assistant de l’auto-observation Arsenal issue du pipeline NAS d’audit patrimonial.
**Contrats liés** :
- `outils_externes/nas_arsenal/audit/audit.md`
- `outils_externes/nas_arsenal/audit/mqtt.md`

---

## 1. Objet

Le domaine `arsenal_self` expose dans Home Assistant l’état de cohérence,
de fraîcheur et d’audit du système Arsenal lui-même.

Il constitue la couche Home Assistant de l’auto-supervision Arsenal.

Il ne produit pas le verdict patrimonial. Il consomme la projection MQTT
publiée par le NAS et la transforme en entités exploitables par :

- le dashboard système ;
- les alertes humaines ;
- les diagnostics de fraîcheur ;
- les vues synthétiques Arsenal.

---

## 2. Phrase centrale

> `arsenal_self` rend visible dans Home Assistant l’état de santé
> patrimoniale d’Arsenal, sans importer dans Home Assistant le détail
> du rapport d’audit NAS.

---

## 3. Frontière d’autorité

| Couche | Responsabilité |
|---|---|
| Moteur d’audit NAS | Produit le verdict patrimonial |
| Wrapper NAS | Produit le verdict JSON |
| Projection MQTT | Transporte le dernier état publié |
| Home Assistant `arsenal_self` | Expose, qualifie et rend exploitable l’état |
| Lovelace | Affiche la synthèse sans logique métier |

Home Assistant n’est pas autorité sur le contenu du rapport d’audit.

Il ne reconstitue pas les anomalies, ne parse pas le Markdown NAS et ne
corrige aucune divergence patrimoniale.

---

## 4. Source de données

La source unique consommée par Home Assistant est le topic MQTT :

```text
arsenal/nas/audit/state
```

Le format du payload, la politique retain, le QoS et les modes d’erreur
relèvent du contrat MQTT associé.

Le domaine `arsenal_self` ne définit pas le transport. Il définit
l’interprétation Home Assistant de ce transport.

---

## 5. Entités du domaine

### 5.1 Sensors

| Entité | Rôle |
|---|---|
| `sensor.arsenal_self_audit_statut` | Verdict exposé : `ok`, `alert`, `error` |
| `sensor.arsenal_self_audit_total_anomalies` | Nombre d’anomalies patrimoniales actionnables |
| `sensor.arsenal_self_audit_total_observations` | Nombre d’observations patrimoniales non actionnables |
| `sensor.arsenal_self_audit_version_auditee` | Version Home Assistant auditée |
| `sensor.arsenal_self_audit_published_at` | Horodatage de publication du dernier état |
| `sensor.arsenal_self_audit_age_minutes` | Âge calculé du dernier état publié |

### 5.2 Binary sensors

| Entité | Rôle |
|---|---|
| `binary_sensor.arsenal_self_audit_alerte` | Indique un verdict patrimonial `alert` |
| `binary_sensor.arsenal_self_audit_error` | Indique une erreur d’exécution ou de projection |
| `binary_sensor.arsenal_self_audit_stale` | Indique que le dernier état publié est trop ancien |

### 5.3 Helper

| Entité | Rôle |
|---|---|
| `input_number.arsenal_self_audit_stale_threshold_hours` | Seuil humain de péremption de l’état publié |

---

## 6. Sémantique des états

### 6.1 `ok`

Le dernier audit publié ne contient aucune anomalie patrimoniale
actionnable.

Des observations patrimoniales peuvent exister sans remettre en cause
l’état `ok`.

### 6.2 `alert`

Le dernier audit publié contient au moins une anomalie patrimoniale
actionnable.

Le détail n’est pas exposé dans Home Assistant. Il reste consultable
dans le rapport NAS `latest.md`.

### 6.3 `error`

La chaîne n’a pas pu produire ou publier un verdict patrimonial
exploitable.

`error` ne signifie pas qu’Arsenal contient une anomalie patrimoniale.
Il signifie que l’état patrimonial n’a pas pu être établi correctement.

### 6.4 `stale`

`stale` est une qualification de fraîcheur.

Ce n’est pas un statut d’audit.

Un état peut être simultanément :

```text
statut = ok
stale = on
```

Cela signifie que le dernier verdict était sain, mais qu’il est trop
ancien pour être considéré comme frais.

---

## 7. Invariants

- Home Assistant ne parse jamais le rapport Markdown NAS.
- Home Assistant ne connaît jamais la liste détaillée des anomalies.
- Home Assistant ne connaît jamais la liste détaillée des observations.
- Home Assistant ne déclenche aucune correction automatique.
- Le domaine `arsenal_self` ne supervise pas un équipement physique.
- Le domaine `arsenal_self` supervise Arsenal lui-même.
- `stale` n’est jamais une valeur de `sensor.arsenal_self_audit_statut`.
- `error` décrit une incapacité de projection ou d’exécution, pas une
  anomalie patrimoniale.
- Le dashboard système affiche une synthèse, pas le rapport complet.

---

## 8. Consommation Lovelace

La carte système peut consommer les entités du domaine pour afficher :

- le statut global ;
- le nombre d’anomalies ;
- le nombre d’observations ;
- la version auditée ;
- l’âge du dernier état ;
- les indicateurs `alerte`, `error` et `stale`.

La carte ne doit pas contenir de logique métier non portée par les
entités du domaine.

La consultation détaillée reste volontairement externe à Home Assistant
et s’effectue sur le NAS via le rapport Markdown.

---

## 9. Alertes

Le domaine expose des binary sensors utilisables par des automatisations
d’alerte.

Les alertes admissibles sont :

| Signal | Sens |
|---|---|
| `binary_sensor.arsenal_self_audit_alerte` | Une anomalie patrimoniale existe |
| `binary_sensor.arsenal_self_audit_error` | Le pipeline d’audit ou de projection est en échec |
| `binary_sensor.arsenal_self_audit_stale` | Aucun état frais n’a été reçu dans le délai attendu |

Toute notification doit rester informative.

Aucune action corrective automatique n’est autorisée dans ce domaine.

---

## 10. Frontières exclues

Le domaine `arsenal_self` ne fait pas :

- l’audit patrimonial ;
- la lecture du registry Home Assistant ;
- la lecture des fichiers YAML ;
- l’analyse des anomalies ;
- la génération du rapport Markdown ;
- la publication MQTT ;
- la correction automatique ;
- l’historisation détaillée des audits ;
- la duplication du rapport NAS dans Home Assistant.

---

## 11. Critère d’acceptation

Le domaine est conforme si :

1. les entités listées au §5 existent ;
2. `sensor.arsenal_self_audit_statut` reflète le verdict MQTT ;
3. `binary_sensor.arsenal_self_audit_alerte` s’active sur `alert` ;
4. `binary_sensor.arsenal_self_audit_error` s’active sur `error` ;
5. `binary_sensor.arsenal_self_audit_stale` s’active selon le seuil humain ;
6. le dashboard système affiche une synthèse exploitable ;
7. aucune logique Lovelace ne remplace une entité de décision ;
8. le détail patrimonial reste exclusivement porté par le rapport NAS.

---

## 12. Gouvernance

Toute modification des entités exposées, de leur sémantique ou de leur
responsabilité nécessite une évolution versionnée du présent contrat.

Toute modification du topic MQTT, du schéma JSON ou des règles de
publication relève du contrat MQTT associé.

---

*Fin du contrat — Domaine Home Assistant `arsenal_self` v1.0.0.*
