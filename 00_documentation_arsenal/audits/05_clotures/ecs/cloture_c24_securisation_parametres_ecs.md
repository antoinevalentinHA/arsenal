# ✅ ARSENAL — CLÔTURE DE CHANTIER
## ECS — Sécurisation des paramètres (suppression des fallbacks numériques artificiels)

| Champ | Valeur |
|---|---|
| **Type** | Clôture de chantier (C24) |
| **Domaine** | ECS — intégrité des grandeurs / paramètres |
| **Statut** | ✅ CLÔTURÉ — écart **I1** résorbé |
| **Version** | 1.0 |
| **Date** | 2026-07-17 |
| **Écart traité** | **I1** — fabrication d'un `0.0` artificiel par la couche de sécurisation ECS |
| **Chantier** | [`../../04_chantiers/ecs/chantier_securisation_parametres_ecs.md`](../../04_chantiers/ecs/chantier_securisation_parametres_ecs.md) |
| **Audit d'origine** | [`../../01_rapports/ecs/audit_exposition_diagnostics_ecs.md`](../../01_rapports/ecs/audit_exposition_diagnostics_ecs.md) (PR #394) |
| **Contrats de référence** | [`sensor_ecs_temperature_ballon_securisee.md`](../../../contrats/ecs/sensor_ecs_temperature_ballon_securisee.md) · [`sensor_ecs_consigne_chaudiere_securisee.md`](../../../contrats/ecs/sensor_ecs_consigne_chaudiere_securisee.md) · [`parametres_invalides.md`](../../../contrats/parametres_invalides.md) (v1.3) |

---

## 1. Objet

Clore le chantier **C24** de sécurisation des paramètres ECS : suppression de la
**fabrication et de la propagation d'un `0.0` artificiel** par les capteurs
« sécurisés » ECS au bootstrap froid / sans restauration / sans valeur valide
(écart **I1**). Cette clôture **ne rouvre pas** l'audit ECS et **ne clôt pas** le
domaine ECS (le watchdog, le futur chantier « Durcissement CI ECS » et les autres
sujets restent **distincts et ouverts**).

## 2. Écart résorbé

Les capteurs `sensor.ecs_temperature_ballon_securisee` et
`sensor.ecs_consigne_chaudiere_securisee` publiaient un `0.0` **numérique** au
bootstrap froid (repli conçu pour « ne jamais être `unavailable` »). Ce `0.0`
passait les gardes des consommateurs (qui ne dépistaient que
`unknown`/`unavailable`/`none`) et pouvait être interprété comme une **mesure /
consigne réelle** (capteurs `tmax`, mémoire de cycle, offsets, verrou). C'est une
violation de [`parametres_invalides.md`](../../../contrats/parametres_invalides.md)
(« Aucun fallback silencieux »).

Politique cible désormais gravée et implémentée : **`unknown` avant toute valeur
réelle valide**, conservation **non silencieuse** (attribut `provenance`) après,
**jamais** de sentinelle numérique fabriquée.

## 3. Chaîne de livraison (PR)

| PR | Livrable |
|---|---|
| **#396** | Contrat propriétaire `sensor_ecs_temperature_ballon_securisee.md` (I-SEC-1..5) |
| **#397** | Lot 1A — producteur `12_template_sensors/ecs/temperature.yaml` conforme |
| **#398** | Lot 1B.1 — `11_automations/ecs/reset_verrou_cycle.yaml` durci (I-SEC-5) |
| **#399** | Lot 1B.2 — `10_scripts/ecs/cycle.yaml` (garde précoce fail-closed + fraîcheur) |
| **#400** | Lot 2 — capteur sœur `consigne_effective.yaml` + contrat dédié (I-SEC-CONS-1..5) |
| **#401** | Verrouillage CI local ECS — contrôle **T14** + correctif A1 de `log/fin.yaml` |

## 4. Matrice finale des neuf critères de clôture

> Les critères 1–8 étaient satisfaits à l'issue de la revue de clôturabilité.
> Le critère **9** (dossier de clôture + registre synchronisés) était alors
> **« NON SATISFAIT par construction »** — c'était le **dernier acte restant**.
> Il est **satisfait par la présente PR** (création de ce dossier + bascule du
> registre dans le **même commit**).

| # | Critère | Verdict | Preuve |
|---|---|---|---|
| 1 | Contrat propriétaire capteur ballon mergé | **SATISFAIT** | #396 |
| 2 | Runtime Lot 1 mergé | **SATISFAIT** | #397 (`temperature.yaml`) |
| 3 | Consommateurs durcis | **SATISFAIT** | #398 (`reset_verrou_cycle`), #399 (`cycle`), `log/debut.yaml` conforme **par vérification** (`float(0)` gardé par `is_number`, sinon `'—'`) |
| 4 | Tests isolés couvrant les 8 scénarios | **SATISFAIT** | oracles Python indépendants + pytest + assertions structurelles + T14 — **frontière : pas de rendu Jinja HA réel** (§6) |
| 5 | Preuve d'absence de zéro artificiel | **SATISFAIT — avec réserves explicites** | §5 ci-dessous |
| 6 | Validation du verrou sous donnée inconnue | **SATISFAIT** | #398, I-SEC-5, oracle `reset_verrou_thermique.py` |
| 7 | Décision documentée **et réalisée** sur le Lot 2 | **SATISFAIT** | #400 (inclus et livré) |
| 8 | Décision CI mise en œuvre | **SATISFAIT** | #401 (T14, Option A locale ECS) |
| 9 | Dossier de clôture + registre synchronisés | **SATISFAIT** | **présente PR** (ce dossier + `REGISTRE_CHANTIERS.md`) |

**Bilan : 9 / 9 SATISFAIT** (dont C5 avec réserves explicites). **C24 clôturé.**

## 5. Critère 5 — décomposition et réserves explicites

Aucun zéro artificiel n'est **actuellement fabriqué ni propagé** dans le
périmètre C24 :

- **Producteurs sécurisés conformes** : `temperature.yaml` et
  `consigne_effective.yaml` émettent `unknown` sans valeur valide (aucun
  `float(0)`), **verrouillés par T14** (axe 1).
- **Consommateurs décisionnels durcis** : `reset_verrou_cycle.yaml` et
  `cycle.yaml` n'évaluent leurs conditions que sur données numériques
  (`is_number` / provenance).
- **`log/debut.yaml`** produit `'—'` sous donnée invalide (le `float(0)` est
  inatteignable, gardé par `is_number`) — conforme **par vérification**.
- **`log/fin.yaml`** corrigé (#401) : `float(none)` + garde `temp is not none` —
  sous température inconnue, « consigne atteinte » reste **faux** sans fabriquer
  de `0`.
- **Capteurs `tmax` conformes sous invalidité** :
  `temperature_max_reelle_cycle.yaml` utilise `float` gardé (jamais de `0`) ;
  `ecs_temperature_max_cycle` porte une garde `availability` (devient
  `unavailable`, **et non `0`**, quand la température est invalide).
- **T14** protège les **4 fichiers cœur** et les **lecteurs directs** des deux
  capteurs sécurisés.

**Réserves explicites (limites assumées — PAS un reste à corriger dans C24) :**

1. Les anciens `0.0` **déjà inscrits dans Recorder avant correction** subsistent
   jusqu'à la **purge naturelle de 30 jours** (`recorder.yaml`,
   `purge_keep_days: 30`). Aucune purge manuelle rétroactive n'est engagée.
2. `log/debut.yaml` et `log/temperature_max.yaml` **ne sont pas intégralement
   couverts par T14**, bien que leur conformité actuelle soit **démontrée**
   (gardes `is_number` / `availability`).
3. La preuve est **contractuelle, structurelle et par oracle** : **pas**
   d'exécution isolée du moteur de templates Jinja Home Assistant.

## 6. Frontière de preuve

Toute la preuve C24 repose sur des **modèles contractuels indépendants**
(oracles `tools/arsenal_ci/behavior/*.py`), des **assertions structurelles** sur
le YAML runtime (pytest `tools/arsenal_ci/tests/`) et le **checker** T14. C'est
une garantie de conformité du **texte et du modèle**, **non** un rendu du moteur
Home Assistant en conditions réelles.

## 7. Observations hors périmètre (non bloquantes, non rouvertes)

- **`consigne_reelle`** dans `11_automations/ecs/inertie/gel.yaml` : variable
  **morte** (unique occurrence repo-wide ; aucun état, aucun helper, aucune
  décision). **Hors périmètre — aucun engagement de suppression.**
- **Boost enfant**, **D2**, **D3**, **UI**, **généralisation transverse de
  T14**, **nettoyage manuel des historiques**, **autres écarts de l'audit ECS** :
  restent **hors C24**. Aucun ne constitue une réserve de clôture.

## 8. Conséquences documentaires

- `REGISTRE_CHANTIERS.md` : C24 basculé de **① Actifs** vers **⑤ Clos récents**
  (même commit — co-commit).
- `chantier_securisation_parametres_ecs.md` : statut final **CLÔTURÉ LE
  2026-07-17**, renvoi vers ce dossier ; historique des lots **conservé**.
- `audits/index.md` : référencement sous `## Clôtures`.
- `navigation/domaines/ecs.md` : ligne C24 requalifiée (clôturé) ; le **domaine
  ECS reste non clôturé** (sujets distincts ouverts).

**Aucun** fichier runtime, contrat, checker, workflow, Recorder, dashboard ni
changelog n'est modifié par cet acte de clôture.

---

*Clôture de chantier — acte documentaire terminal de C24. Ne rouvre pas l'audit
ECS et ne clôt pas le domaine ECS.*
