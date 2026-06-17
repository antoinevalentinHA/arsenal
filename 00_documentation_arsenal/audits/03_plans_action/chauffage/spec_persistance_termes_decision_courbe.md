# 🧭 ARSENAL — SPÉCIFICATION D'EXÉCUTION
## Chauffage — Persistance Recorder des termes de décision (auto-ajustement courbe)

| Champ | Valeur |
|---|---|
| **Type** | Spécification d'exécution (liste normative d'entités) |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Spec — non démarrée |
| **Version** | 1.0 |
| **Date** | 2026-06-17 |
| **Concrétise** | [`plan_action_observabilite_auto_ajustement_courbe.md`](plan_action_observabilite_auto_ajustement_courbe.md) — phase **P3 (Persistance)** |
| **Contrat de référence** | [`76_observabilite_auto_ajustement_courbe.md`](../../../contrats/chauffage/76_observabilite_auto_ajustement_courbe.md) |
| **Origine** | [`rapport d'écart runtime`](../../01_rapports/chauffage/rapport_ecart_runtime_representativite_courbe.md) §6 |
| **Cadre** | Liste d'entités + justification. Aucun YAML, aucune valeur de rétention fine. |

---

## 1. Objet

Fournir la **liste normative** des entités à historiser dans `recorder.yaml` pour que la chaîne
d'auto-ajustement de la courbe soit **diagnosticable a posteriori sans dépendre de la moisson de
la table `events`**. Cette spec opérationnalise la phase **P3 (Persistance)** du plan d'action
observabilité ; elle ne rouvre ni l'audit, ni le contrat `76`.

## 2. Constat de départ (preuve)

L'enquête du 16/06 (mode `--db`) a établi que `recorder.yaml` n'historise **aucun** terme de
décision de la chaîne courbe. Seuls trois éléments de contexte le sont :
`input_select.mode_maison`, `sensor.ecart_consigne_instantane`,
`input_boolean.blocage_chauffage_poele`. Reconstituer une décision a donc exigé de décoder les
`event_data` de `chauffage_courbe_cycle_evalue` / `chauffage_adjustment` — possible uniquement
via SQLite, non via l'API. C'est précisément le risque P3 (« cécité sans historique »).

> Les événements (P1/P2) **capturent** la décision ; la persistance Recorder (P3) **conserve les
> états d'entrée à l'instant du cycle**, rejouables sans décodage de la table `events`. Les deux
> sont complémentaires, non redondants.

## 3. Liste normative — issue de l'audit Recorder (2026-06-17)

> **Mise à jour (passe observabilité).** La sélection initiale a été confrontée au **contrat
> Recorder** (`scripts/arsenal_contracts/check_recorder_contracts.py`). Deux corrections en
> découlent : les ACK sont **inéligibles** (T08, motif `_ack_` — artefact transactionnel
> transitoire) ; les capteurs `platform: statistics` et les suggestions sont **différés** (volume
> / déjà couverts). Le set retenu est volontairement **minimal et faible-fréquence**.

### 3.1 Retenu — historisé dans `recorder.yaml` (Population B, ≤ 1 changement/jour)

| Entité | Couche | Pourquoi indispensable | Classe |
|---|---|---|---|
| `input_select.chauffage_representativite_thermique` | Décision | Précondition prioritaire §7/§8 ; cœur de l'écart du 16/06 | **CRITIQUE** |
| `input_boolean.chauffage_reglages_auto` | Décision | Gate d'activation ; distingue inaction « auto off » d'une abstention | **CRITIQUE** |
| `input_boolean.courbe_auto_simulation` | Décision | Distingue une décision réelle d'une simulation | **CRITIQUE** |
| `input_number.chauffage_pente_consigne` | Exécution | Cible **et** résultat appliqué ; trajectoire du paramètre | **CRITIQUE** |
| `input_number.chauffage_parallele_consigne` | Exécution | Idem ; c'est la grandeur écrite le 16/06 | **CRITIQUE** |
| `input_text.chauffage_last_adjustment` | Diagnostic | Trace lisible de la dernière décision appliquée (avant→après, mode) ; consultable en historique HA **sans SQLite** | **IMPORTANT** |

Ce set rend l'**incident-classe du 16/06 reconstituable depuis l'historique HA seul** : croiser
l'historique de `…representativite_thermique` (= `NON_REPRESENTATIF` à 10:00) avec celui de
`…parallele_consigne` (= 2.0→1.0 à 10:00) **prouve la violation sans extraire la base**.

### 3.2 Exclus — par contrat Recorder

| Entité | Motif d'exclusion |
|---|---|
| `sensor.boiler_ack_heating_set_curve_slope_status` | **T08** (`_ack_`, Population B Non éligible) ; l'« appliqué/refusé » est déjà porté par l'événement `chauffage_adjustment` (`pente_applied`) |
| `sensor.boiler_ack_heating_set_curve_shift_status` | **T08** ; idem (`para_applied`) |

### 3.3 Différés — risque de volume (à reconsidérer si besoin avéré)

| Entité | Motif de différé |
|---|---|
| `sensor.chauffage_pente_suggeree` / `…parallele_suggeree` | Churn d'attributs (miroir des écarts) → volume ; la valeur **au cycle** est déjà captée par `chauffage_last_adjustment` (action) et les événements |
| `sensor.ecart_consigne_stats_froid` / `…stats_24h` | `platform: statistics` recalculées à chaque échantillon → haute fréquence ; `sensor.ecart_consigne_instantane` **déjà historisé** couvre la perception |

Déjà historisés (à conserver, pour rappel) : `input_select.mode_maison`,
`sensor.ecart_consigne_instantane`, `input_boolean.blocage_chauffage_poele`.

### 3.4 Reste event-only — limite connue

Le **verdict dérivé** de cycle (`cycle_actionnable`, `cycle_reason`, p.ex. `non_representatif`
sur une **abstention**) n'est porté par **aucune entité d'état** : il ne vit que dans
`chauffage_courbe_cycle_evalue`. Une abstention reste donc invisible à l'historique d'états
(seules les **actions** écrivent `chauffage_last_adjustment` et les consignes). L'historiser comme
état queryable supposerait une **nouvelle entité** (code) — hors périmètre de cette passe minimale,
signalé comme suite possible si la visibilité des abstentions sans événements devient un besoin.

## 4. Garde-fous

- **Read-only / étanchéité (INV-1, INV-2).** La persistance n'introduit aucune logique de décision ;
  les entités historisées ne **réalimentent jamais** la décision.
- **Sur-observabilité bornée.** La liste se limite aux termes nécessaires aux 8 questions de
  supervision du contrat `76` ; les entités au-delà (diagnostics thermiques détaillés) restent
  hors périmètre P3. Tenir compte de la rétention (`purge_keep_days: 30`) et du `commit_interval`.
- **Cadence faible.** L'auto-ajustement est quotidien (10:00) : le volume incrémental est marginal.
- **Conformité CI.** Le changement `recorder.yaml` doit passer `check_recorder_contracts.py`.

## 5. Hors périmètre

Implémentation YAML (relève de l'exécution de P3), valeurs de rétention fines, dashboards de
dérivation (P5/P7), et toute reprise du débat sur la **qualité du signal** de représentativité
(§5.6 de l'audit), traitée séparément.
