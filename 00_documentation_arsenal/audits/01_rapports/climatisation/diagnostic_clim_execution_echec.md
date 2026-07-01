# DIAGNOSTIC — CHAÎNE D'EXÉCUTION CLIMATISATION
## La clim ne démarre pas — `input_boolean.clim_execution_echec` latché à `on`

> **Nature.** Diagnostic **statique** de la chaîne d'exécution climatisation, mené
> à partir de la structure du dépôt (aucune exécution de Home Assistant, aucun
> accès au Recorder de l'incident). L'analyse porte sur la logique de code :
> décision → transit → exécution → application physique → post-condition →
> résilience.
>
> **Statut.** Constats stabilisés. **Aucune modification fonctionnelle décidée,
> aucun réglage proposé, aucun contrat / automatisation / YAML runtime touché.**
> Le booléen de défaut n'a **pas** été réinitialisé, aucune automatisation n'a
> été désactivée, aucun contournement n'a été introduit.
>
> **Conclusion en une ligne.** La chaîne de code est **saine** sur l'ensemble des
> points audités. Le symptôme observé est la **signature exacte d'un échec
> `infra`** au sens de la couche Exécution : `climate.clim` et/ou
> `switch.clim_power` indisponibles (intégration **Fujitsu Airstage** gelée /
> déconnectée) au moment de la tentative. Il ne s'agit **pas d'un défaut de
> code** mais d'une **indisponibilité runtime de l'intégration**, gérée
> *as-designed* (latch du défaut jusqu'à une exécution réussie).

---

> ⚠️ **ADDENDUM (réfutation runtime).** Ce diagnostic statique concluait en
> §4/Q1 que la course du Guard était **improbable** (« les deux entités
> proviennent du même snapshot coordinator »). Un relevé **Recorder** ultérieur
> a **réfuté** cette hypothèse : avec `sensor.clim_target_mode = cool` stable,
> `climate.clim` ne parvient **jamais** à `cool` tandis que `switch.clim_power`
> clignote ON→OFF toutes les quelques secondes, le Guard appelant `apply_off`
> (trace confirmée). Cause racine réelle = **INV-3 du Guard** (`climate.clim`
> actif **ET** `switch.clim_power == off`) qui se déclenche sur le **snapshot
> transitoire d'allumage** — `climate.clim` (mode) précède `switch.clim_power`
> (alim) côté intégration — et **avorte chaque démarrage** (bagarre
> `apply_cool` ↔ `apply_off`). L'assertion « même snapshot cohérent » est donc
> fausse **pendant les transitions**. Correctif : retrait d'INV-3 du Guard
> immédiat, cohérence power/mode persistante déléguée au Watchdog (voir
> `contrats/climatisation/09_securite.md` v1.5). Les §4/Q1 et la piste
> d'amélioration GUARD INV-3 ci-dessous sont **à lire à la lumière de cette
> réfutation**.

---

## 1. SYMPTÔME ET FAITS

- La climatisation aurait dû démarrer (décision attendue = `cool` / `heat` / `dry`)
  mais ne s'est pas allumée.
- `input_boolean.clim_execution_echec` est passé à `on`.
- Reset manuel du booléen à `off` puis relance manuelle de scripts / automations :
  **sans succès** (échec persistant).
- Le booléen de défaut est un **symptôme**, pas la cause.

Fait de contexte décisif : **`script.clim_execution` ne porte aucune condition
`systeme_stable`** (`10_scripts/climatisation/execution_mode_cible.yaml`). Le
relais manuel du script **contourne** donc toutes les gardes systèmes. Qu'il
échoue **quand même** de façon répétée exclut les causes « en amont »
(stabilité système, transit, décision) et concentre la cause **au point
d'émission de la commande** ou **au device**.

---

## 2. CHAÎNE D'EXÉCUTION COMPLÈTE (cartographie)

```
[ADMISSIBILITÉ]         input_boolean.besoin_clim_{cool,dry,heat}_admissible
  │                       ← 11_automations/climatisation/{cool,dry,heat}/admissibilite.yaml
  ▼                       (doctrine 2 portes : besoin × autorisation)
[DÉCISION PURE]         sensor.clim_target_mode
  │                       ← 12_template_sensors/climatisation/decision/mode_target.yaml
  │                       cool > dry > heat > off (ThermalPriorityPolicy)
  ▼
[TRANSIT]               automation "Clim - Application automatique" (id 10030000000105)
  │                       ← 11_automations/climatisation/trigger_execution.yaml
  │                       trigger: état sensor.clim_target_mode
  │                       condition: input_boolean.systeme_stable == on
  ▼
[EXÉCUTION]             script.clim_execution
  │                       ← 10_scripts/climatisation/execution_mode_cible.yaml
  │                       1. lecture/qualification (target_valid, entities_available)
  │                       2. garde cible invalide (abstention silencieuse)
  │                       3. choose → script.clim_exec_apply_{cool,dry,heat,off}
  │                       4. stabilisation (delay 15 s)
  │                       5. post-condition (is_state climate.clim == target)
  │                       6. conclusion → succès | échec (infra | postcondition)
  ▼
[APPLICATION PHYSIQUE]  script.clim_exec_apply_cool | _dry | _heat | _off
  │                       ← 10_scripts/climatisation/{cool,dry,heat,off}.yaml
  │                       power ON (switch.clim_power) + delay 10 s
  │                       garde : climate.clim ∉ [unknown, unavailable]
  │                       climate.set_hvac_mode <mode>
  ▼
[ÉTAT RÉEL]             climate.clim (hvac_mode) / switch.clim_power (on/off)
                          ← custom_components/fujitsu_airstage/{climate,switch}.py

[GARDES / FILETS]
  - GUARD (id 10030000000101)   11_automations/climatisation/guard.yaml
      INV-1/2/3 cohérence décision↔exécution → force apply_off
  - WATCHDOG (id 10030000000106) 11_automations/climatisation/watchdog.yaml
      incohérence persistante ≥ 60 s → relance script.clim_execution
  - REPRISE (id 10030000000108)  11_automations/climatisation/reprise_apres_echec.yaml
      timer.clim_retry finished + echec on + counter ≤ 2 → relance

[MÉMOIRE DE RÉSILIENCE]
  - input_boolean.clim_execution_echec       05_input_booleans/climatisation/echec_execution.yaml
  - counter.clim_execution_retry_count
  - timer.clim_retry

[RÉSILIENCE INTÉGRATION AIRSTAGE]
  - sensor.fujitsu_age_donnees               12_template_sensors/system/integrations/age_des_donnees.yaml
  - binary_sensor.gel_avere_airstage (≥45 min, delay_on 5 min)
  - binary_sensor.indisponibilite_franche_airstage
  - binary_sensor.retour_ok_airstage / recovery_en_cours_airstage
      ← 12_template_sensors/system/integrations/etat.yaml
  - automation "Système - Relance Airstage" (id 1012000000013)
      ← 11_automations/system/reload_integrations/fujitsu.yaml
      → script.resilience_integration_recover (reload config_entry, backoff, plafond)
```

---

## 3. MÉCANISME QUI POSITIONNE `clim_execution_echec`

Fichier : `10_scripts/climatisation/execution_mode_cible.yaml`.

```
target_valid       = target ∈ [cool, dry, heat, off]
entities_available = climate.clim ∉ [unknown, unavailable]
                     ET switch.clim_power ∉ [unknown, unavailable]      (lignes 48-50)
execution_possible = target_valid ET entities_available                (ligne 51)
```

Qualification du résultat (lignes 116-139) :

| Situation | `echec_type` | Effet |
|---|---|---|
| `execution_possible = false` | **`infra`** | `input_boolean.turn_on` echec + reprise différée |
| Commande émise, `climate.clim` ≠ cible après 15 s | **`postcondition`** | `input_boolean.turn_on` echec + reprise différée |
| Cible atteinte | `none` | `input_boolean.turn_off` echec + reset counter + cancel timer |

Le booléen est donc **latché** dès qu'une tentative n'atteint pas la
post-condition, **et il reste `on` tant qu'aucune exécution ne réussit**. Le
reset manuel à `off` est écrasé au tour suivant si la cause persiste : le
symptôme se ré-affirme, fidèlement.

---

## 4. CAUSE LA PLUS PROBABLE

**Indisponibilité runtime de l'intégration Fujitsu Airstage** (`climate.clim`
et/ou `switch.clim_power` en `unavailable` / `unknown`, ou device injoignable /
données gelées), produisant un **échec `infra`** (voire un échec
`postcondition` si la commande part mais que le device n'atteint pas le mode).

Deux chemins de code convergent vers ce verdict, tous deux *by-design* :

1. **Couche Exécution** — si `entities_available = false`,
   `execution_possible = false` → aucune commande émise → `echec_type = infra`
   (`execution_mode_cible.yaml:132-139, 170-172`). C'est **exactement** l'état
   « le booléen passe à `on` et la clim ne s'allume pas ».

2. **Application physique** — chaque script `apply_{cool,dry,heat}` porte la garde
   `condition: {{ states('climate.clim') not in ['unknown','unavailable'] }}`
   (`cool.yaml:39-40`, idem `dry.yaml`, `heat.yaml`). Tant que `climate.clim`
   est `unavailable`, `climate.set_hvac_mode` **n'est jamais émis** — y compris
   sur relance **manuelle** du script. D'où l'échec **persistant malgré le
   re-run manuel**.

Le dépôt embarque une infrastructure de résilience **dédiée à ce cas précis**
(gel de données Airstage : `sensor.fujitsu_age_donnees`,
`binary_sensor.gel_avere_airstage` ≥ 45 min, reload de config_entry avec
backoff — `reload_integrations/fujitsu.yaml`). Sa seule existence confirme que
l'indisponibilité Airstage est un **incident runtime connu et attendu**, pas un
défaut logique.

### Points examinés et écartés (aucun défaut de code certain)

| # | Hypothèse | Verdict | Preuve |
|---|---|---|---|
| Q1 | GUARD éteint la clim juste après l'allumage | Écartée | `guard.yaml:129-137` — INV-1/2 exigent `target_off` (faux si cible=cool) ; INV-3 exige `climate.clim` actif **et** `switch.clim_power=off` **simultanément**, or les deux proviennent du **même snapshot coordinator** (`switch.py:270-281`, `climate.py:230-240`) → cohérents en fonctionnement nominal |
| Q2 | Post-condition qui échoue toujours (device OK) | Écartée | `execution_mode_cible.yaml:116-131` — compare la **même** entité pilotée, mode attendu correct par branche, OFF vérifie clim **et** power ; 15 s + 10 s de stabilisation ; refresh coordinator immédiat après `set_operation_mode` (`climate.py:334`) |
| Q3 | `systeme_stable` bloqué à `off` | Écartée | `script.clim_execution` **sans** condition `systeme_stable` → le re-run manuel le contourne ; s'il échoue, la cause n'est pas là |
| Q4 | Helper / verrou / timer bloque définitivement la reprise | Écartée (limitation, pas verrou) | `counter.clim_execution_retry_count` réinitialisé **au succès** ; un re-run manuel ou un succès réarme tout ; pas de lock permanent |
| Q5 | Entité cassée / renommée | Écartée | `switch.clim_power` / `climate.clim` réels et cohérents partout (`02_groups/integrations/fujitsu.yaml:33-34`, `switch.py:259-298`, `climate.py:139`) ; « ça marche d'habitude » exclut un ID mort |
| Q6 | Admissibilité cool bloquée à tort | Écartée / hors sujet | Une cible `off` erronée n'aurait **pas** latché le défaut (off → apply_off → succès → echec `off`). Le défaut `on` **prouve** que la cible était active et que l'exécution a bien tenté |

---

## 5. SCÉNARIO DE REPRODUCTION

1. Décision légitime : `sensor.clim_target_mode` = `cool` (besoin + autorisation
   satisfaits).
2. L'intégration Airstage perd la liaison (Wi-Fi module / API cloud / gel de
   données) : `climate.clim` et/ou `switch.clim_power` passent `unavailable`.
3. `automation.clim_application_automatique` relaie la décision →
   `script.clim_execution`.
4. `entities_available = false` → `execution_possible = false` → **aucune
   commande** → `echec_type = infra` → `input_boolean.clim_execution_echec = on`.
5. Reprises différées (+30 s, +90 s) puis épuisement (counter > 2) : chaque
   tentative retrouve les entités indisponibles → re-latch.
6. Reset manuel du booléen + relance manuelle de `script.clim_exec_apply_cool` :
   la garde `climate.clim ∉ [unknown, unavailable]` **stoppe** le script avant
   `set_hvac_mode` → aucune commande → la clim reste éteinte, le booléen se
   ré-affirme au tour d'exécution suivant. **Symptôme reproduit à l'identique.**

**Vérification empirique recommandée (Recorder / Logbook, fenêtre de
l'incident)** — pour confirmer avant toute action :

- `climate.clim` et `switch.clim_power` : y avait-il un intervalle
  `unavailable` / `unknown` couvrant l'heure attendue de démarrage ?
- `sensor.fujitsu_age_donnees` : dépassait-il 45 min ?
- `binary_sensor.gel_avere_airstage` / `indisponibilite_franche_airstage` :
  passés à `on` ?
- `input_number.airstage_reload_tentatives` / `timer.airstage_reload_backoff` :
  la procédure de reload a-t-elle tourné ?

Si ces signaux confirment l'indisponibilité → cause **certaine**, hors code.

---

## 6. CORRECTION RECOMMANDÉE

**Aucune correction de code.** La chaîne est conforme à son contrat
(`00_documentation_arsenal/contrats/climatisation/08_execution.md`) : elle
applique, constate, et délègue la reprise ; le défaut `infra` est **le
comportement attendu** face à une intégration indisponible.

La « correction » relève de l'**infrastructure**, pas du dépôt :

1. **Rétablir la liaison Airstage** (Wi-Fi du module intérieur, connectivité
   cloud Fujitsu, reload de l'intégration). Laisser la résilience intégrée
   (`reload_integrations/fujitsu.yaml`) faire son travail ; vérifier qu'elle
   s'est bien déclenchée.
2. **Après retour en ligne**, la reprise se ré-arme via un changement de
   décision, la ré-assertion d'incohérence (watchdog), ou un re-run manuel ;
   une exécution réussie éteint `clim_execution_echec` et remet le counter à 0.

### Pistes d'amélioration (NON appliquées — hors périmètre, non bloquantes)

À arbitrer par le mainteneur, elles ne corrigent **pas** l'incident présent :

- **Réarmement de l'auto-reprise après épuisement.** Après 3 échecs
  (`counter > 2`, `execution_mode_cible.yaml:206-208`), l'auto-reprise ne se
  réactive plus seule tant qu'aucun succès n'a lieu ; elle dépend alors d'un
  changement de décision, d'une ré-assertion d'incohérence (watchdog) ou d'une
  action manuelle. Comportement borné **voulu**, mais qui peut prolonger un
  latch après une panne longue. Un réarmement sur `binary_sensor.retour_ok_airstage`
  serait envisageable.
- **Robustesse théorique de GUARD INV-3.** L'invariant `clim_active and power==off`
  (`guard.yaml:135-136`) ne teste pas `target` ; il n'est sûr **que** parce que
  power et mode partagent le même snapshot coordinator. À documenter comme
  hypothèse, au cas où les deux entités proviendraient un jour de sources
  désynchronisées.

Ces pistes sont **signalées**, non retenues : la mission demande de corriger la
cause racine de l'incident, or celle-ci est une indisponibilité d'intégration,
sans défaut de code à modifier.

---

## 7. FICHIERS ET LIGNES CONCERNÉS (référence)

| Fichier | Lignes | Rôle dans le diagnostic |
|---|---|---|
| `10_scripts/climatisation/execution_mode_cible.yaml` | 42-51, 116-139, 149-208 | Qualification `infra`/`postcondition`, latch du booléen, reprises bornées |
| `10_scripts/climatisation/cool.yaml` | 31-48 | Garde `climate.clim` indisponible → bloque `set_hvac_mode` (idem dry/heat) |
| `11_automations/climatisation/trigger_execution.yaml` | 42-60 | Transit décision → exécution, condition `systeme_stable` |
| `11_automations/climatisation/guard.yaml` | 101-140 | Invariants de cohérence (aucun ne se déclenche en cool nominal) |
| `11_automations/climatisation/watchdog.yaml` | 18-43 | Relance sur incohérence persistante |
| `11_automations/climatisation/reprise_apres_echec.yaml` | 27-43 | Reprise bornée (`counter ≤ 2`) |
| `12_template_sensors/climatisation/decision/mode_target.yaml` | 35-43 | Décision canonique |
| `12_template_sensors/system/integrations/etat.yaml` | 106-… | Détecteurs de gel / indisponibilité Airstage |
| `11_automations/system/reload_integrations/fujitsu.yaml` | 26-95 | Résilience : reload config_entry Airstage |
| `custom_components/fujitsu_airstage/climate.py` | 230-240, 325-334 | `hvac_mode` / `async_set_hvac_mode` |
| `custom_components/fujitsu_airstage/switch.py` | 259-298 | `switch.clim_power` (`get_device_on_off_state`) |
