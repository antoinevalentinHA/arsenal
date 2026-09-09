# Contrat — Projection MQTT de l'audit Arsenal NAS — V1.0.2

**Version** : v1.0.2
**Révision** : v1.0.2 — ajout du champ `run_id` au schéma `latest.verdict.json` et au payload MQTT nominal, en anticipation du lot runtime C51 (durcissement AUDIT, dépôt `arsenal-ha-backup-timeline`, chantier [`c51_commandabilite_nas.md`](../../../audits/04_chantiers/transverses/c51_commandabilite_nas.md)). Contrat écrit avant le runtime correspondant, conformément à la doctrine « contrat avant runtime » : le champ n'est pas encore émis par le publisher actuel. Aucun changement de verdict métier, aucune admission MQTT introduite, aucun `request_id`.
**Statut** : actif / implémenté *(`run_id` : spécifié par anticipation, non encore émis — voir Révision)*
**Périmètre** : production du verdict JSON NAS et projection MQTT de l’état d’audit Arsenal NAS.
**Dépendances** :
- `audit.md` v1.1.1 — moteur d’audit patrimonial NAS ;
- `contrats/arsenal_self.md` v1.0.0 — exposition Home Assistant du domaine `arsenal_self`.

---

## 1. Objet

Le présent contrat spécifie la projection MQTT de l’état produit par le
moteur d’audit Arsenal NAS.

Il couvre :

- la production de `latest.verdict.json` par le wrapper NAS ;
- le topic MQTT publié ;
- le schéma du payload ;
- les modes d’erreur de publication ;
- la politique de fraîcheur côté transport.

Il ne couvre pas l’exposition Home Assistant détaillée, qui relève du
contrat `arsenal_self.md`.

---

## 2. Phrase centrale

> La projection MQTT transporte vers Home Assistant un verdict
> patrimonial synthétique, sans publier le détail du rapport d’audit NAS.

---

## 3. Frontière d’autorité

| Couche | Produit | Ne produit pas |
|---|---|---|
| `audit_engine.py` | Verdict patrimonial `ok` / `alert` | Statut de transport |
| `run_audit.sh` | `latest.verdict.json` | Entités Home Assistant |
| `publish_audit_mqtt.sh` | Payload MQTT nominal ou `error` | Analyse patrimoniale |
| Home Assistant `arsenal_self` | Entités HA dérivées | Payload MQTT |

---

## 4. Périmètre fonctionnel

### 4.1 Inclus

Sont publiés via MQTT :

- le verdict patrimonial ;
- les compteurs principaux ;
- l’identifiant de la version auditée ;
- l’identifiant d’exécution NAS (`run_id`) — pure corrélation technique,
  sans portée métier ;
- l’horodatage de publication ;
- un statut `error` si la chaîne ne peut pas produire de verdict exploitable.

### 4.2 Exclus

Ne sont jamais publiés via MQTT :

- la liste détaillée des anomalies ;
- la liste détaillée des observations patrimoniales ;
- les évidences ;
- les notes ;
- les fichiers source ;
- le contenu du rapport Markdown.

Le détail patrimonial reste porté exclusivement par le rapport NAS.

---

## 5. Format `latest.verdict.json`

### 5.1 Localisation

```text
/volume1/Backups_HA/ha_backup_timeline/audit/reports/latest.verdict.json
```

### 5.2 Schéma nominal

```json
{
  "contract_version": "1.0.2",
  "engine_version": "1.1.1",
  "published_at": "2026-05-11T13:00:00Z",
  "run_id": "20260511T130000",
  "version_auditee": "2026-05-11_03-15-00",
  "verdict": "ok",
  "total_anomalies": 0,
  "total_observations_patrimoniales": 603
}
```

### 5.3 Champs

| Champ | Type | Contrainte |
|---|---|---|
| `contract_version` | string | Version du présent contrat |
| `engine_version` | string | Version du moteur d’audit |
| `published_at` | string ISO 8601 UTC | Suffixe `Z` obligatoire |
| `run_id` | string \| null | Identifiant d’exécution NAS attribué par `run_audit.sh`. Obligatoire (non `null`) sur le payload nominal. Pure corrélation technique : n’entre dans aucune décision métier, ne modifie jamais `verdict`. Distinct du futur `request_id` et du `run_id` transactionnel que `nas_transactionnel.md` spécifiera à l’implémentation de l’admission NAS (chantier C51) — celui-ci est le précurseur produit par le wrapper, hors toute admission. Forme laissée à l’implémentation. |
| `version_auditee` | string | Nom de la version auditée |
| `verdict` | string | `ok` ou `alert` |
| `total_anomalies` | int | `0` si `ok`, `>= 1` si `alert` |
| `total_observations_patrimoniales` | int | Informatif, non bloquant |

---

## 6. Topic MQTT

```text
arsenal/nas/audit/state
```

| Propriété | Valeur |
|---|---|
| Retain | `true` |
| QoS | `1` |

---

## 7. Payload d’erreur

En cas d’incapacité à produire un verdict exploitable :

```json
{
  "contract_version": "1.0.2",
  "engine_version": null,
  "published_at": "2026-05-11T13:00:00Z",
  "run_id": null,
  "version_auditee": null,
  "verdict": "error",
  "total_anomalies": null,
  "total_observations_patrimoniales": null,
  "error_reason": "audit_engine_unexpected_exit_code",
  "error_detail": "exit_code=99"
}
```

Causes normalisées :

| `error_reason` | Sens |
|---|---|
| `verdict_json_missing` | Fichier absent |
| `verdict_json_malformed` | JSON invalide ou incomplet |
| `verdict_json_stale` | Fichier trop ancien en mode strict |
| `audit_engine_unexpected_exit_code` | Code retour audit inattendu |
| `mqtt_publish_failed` | Échec `mosquitto_pub`, conservé en log local |

### 7.1 Cas particulier — `run_id` sur `verdict_json_stale`

Lorsque `error_reason = verdict_json_stale`, `latest.verdict.json` existe et
reste lisible : il est seulement trop ancien pour le mode strict. Dans ce
cas uniquement, le payload d’erreur reprend le `run_id` déjà présent dans ce
JSON encore lisible — il n’est **pas** mis à `null`.

Pour toute autre cause d’erreur (`verdict_json_missing`,
`verdict_json_malformed`, `audit_engine_unexpected_exit_code`), aucun JSON
exploitable n’existe : `run_id` reste `null`. Cela ne constitue pas une
rupture de corrélation transactionnelle — la future couche transactionnelle
C51 (`nas_transactionnel.md`) portera son propre `run_id`, attribué en
amont du moteur par l’admission NAS, distinct de celui spécifié ici.

---

## 8. Fraîcheur

Le NAS ne publie pas de heartbeat.

La fraîcheur opérationnelle est portée par deux niveaux distincts :

| Niveau | Responsabilité |
|---|---|
| Publisher NAS | Vérifie le mtime de `latest.verdict.json` en mode strict |
| Home Assistant | Calcule l’âge du dernier message reçu |

Le seuil NAS strict reste fixé à 5 minutes et ne s’applique que lorsque
`publish_audit_mqtt.sh` est appelé immédiatement après `run_audit.sh`.

```sh
publish_audit_mqtt.sh --strict-freshness
```

Sans ce flag, le publisher est tolérant et republie le dernier état connu.

---

## 9. Chaîne d’exécution

```text
run_pipeline.sh
  ├── run_audit.sh
  │     ├── audit_engine.py
  │     ├── latest.md
  │     └── latest.verdict.json
  └── publish_audit_mqtt.sh --strict-freshness
        └── arsenal/nas/audit/state
```

`publish_audit_mqtt.sh` s’exécute après `run_audit.sh`, quel que soit
le code retour de ce dernier.

L’exit code propagé à DSM reste celui de l’audit. Le publisher observe
et projette ; il ne décide pas du résultat du pipeline.

---

## 10. Consommateur Home Assistant

Le consommateur Home Assistant officiel est le domaine :

```text
arsenal_self
```

Son contrat est situé dans :

```text
/homeassistant/00_documentation_arsenal/contrats/arsenal_self.md
```

Le présent contrat ne définit pas les entités HA. Il garantit seulement
le payload consommable par ce domaine.

---

## 11. Tests d’acceptation

Le contrat est valide si :

| Cas | Résultat attendu |
|---|---|
| Audit nominal sans anomalie | Payload `verdict=ok` |
| Audit avec anomalie | Payload `verdict=alert` |
| Crash moteur simulé | Payload `verdict=error` |
| JSON absent | Payload `verdict_json_missing` |
| JSON malformé | Payload `verdict_json_malformed` |
| JSON stale mais encore lisible (mode strict) | Payload `verdict_json_stale`, `run_id` repris du JSON encore lisible |
| Broker MQTT indisponible | Aucun payload ; erreur locale journalisée |
| Redémarrage HA | Dernier état restauré via retain |

Sur tout payload nominal (`verdict=ok` ou `alert`), `run_id` est présent et
non `null`.

---

## 12. Frontières assumées

La projection MQTT ne fait pas :

- l’analyse patrimoniale ;
- l’exposition détaillée HA ;
- l’historisation des audits dans HA ;
- la publication des anomalies individuelles ;
- la publication du rapport Markdown ;
- l’envoi de notifications ;
- la correction automatique.

---

## 13. Évolutions futures

- Sortie JSON native directement produite par le moteur d’audit.
- Payload structuré complet optionnel sur un topic séparé.
- Publication d’un résumé minimal de la dernière anomalie.
- Historisation indépendante des verdicts MQTT.

---

## 14. Gouvernance

Toute modification du topic, du schéma JSON ou des causes d’erreur
nécessite une évolution versionnée du présent contrat.

Toute modification des entités Home Assistant ou de leur sémantique
relève du contrat `arsenal_self.md`.

---

*Fin du contrat — Projection MQTT de l’audit Arsenal NAS v1.0.2.*
