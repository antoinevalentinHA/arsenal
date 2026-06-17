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

## 3. Liste normative à historiser

Classes : **CRITIQUE** (sans quoi la décision n'est pas reconstituable) · **IMPORTANT** (amont /
résultat nécessaires à l'explication) · **UTILE** (confort de diagnostic).

| Entité | Couche | Pourquoi indispensable | Classe |
|---|---|---|---|
| `input_select.chauffage_representativite_thermique` | Décision | Précondition prioritaire §7/§8 ; cœur de l'écart du 16/06 | **CRITIQUE** |
| `input_boolean.chauffage_reglages_auto` | Décision | Gate d'activation ; distingue inaction « auto off » d'une abstention | **CRITIQUE** |
| `input_boolean.courbe_auto_simulation` | Décision | Distingue une décision réelle d'une simulation | **CRITIQUE** |
| `input_number.chauffage_pente_consigne` | Exécution | Cible **et** résultat appliqué ; trajectoire du paramètre | **CRITIQUE** |
| `input_number.chauffage_parallele_consigne` | Exécution | Idem ; c'est la grandeur écrite le 16/06 | **CRITIQUE** |
| `sensor.chauffage_pente_suggeree` | Décision | Proposition amont ; explique pourquoi un cycle est actionnable | **IMPORTANT** |
| `sensor.chauffage_parallele_suggeree` | Décision | Idem (parallèle) | **IMPORTANT** |
| `sensor.ecart_consigne_stats_froid` | Perception | Entrée de la suggestion pente ; détecte les valeurs gelées | **IMPORTANT** |
| `sensor.ecart_consigne_stats_24h` | Perception | Entrée de la suggestion parallèle | **IMPORTANT** |
| `sensor.boiler_ack_heating_set_curve_slope_status` | Exécution | ACK corrélé ; prouve l'application physique (pente) | **IMPORTANT** |
| `sensor.boiler_ack_heating_set_curve_shift_status` | Exécution | ACK corrélé (parallèle) | **IMPORTANT** |
| `input_text.chauffage_last_adjustment` | Diagnostic | Trace lisible de la dernière décision (déjà event-portée) | **UTILE** |

Déjà historisés (à conserver, pour rappel) : `input_select.mode_maison`,
`sensor.ecart_consigne_instantane`, `input_boolean.blocage_chauffage_poele`.

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
