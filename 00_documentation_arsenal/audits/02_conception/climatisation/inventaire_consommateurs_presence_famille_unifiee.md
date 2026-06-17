# Inventaire de périmètre — Consommateurs de `binary_sensor.presence_famille_unifiee`

| Champ | Valeur |
|---|---|
| **Type** | Inventaire de périmètre / support de décision |
| **Domaine** | Climatisation / Présence — cadrage du rebranchement COOL |
| **Statut** | **Implémenté V1+V2 — support de décision, mis à jour post-déploiement** (voir §*État de déploiement V1+V2*) |
| **Version** | 0.1 |
| **Date** | 2026-06-15 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `84066894` |
| **Cadre** | Lecture seule. Aucun YAML, aucun patch. Vérifié sur le HEAD courant. |

> **Objet :** recenser **exhaustivement** les consommateurs de `binary_sensor.presence_famille_unifiee` et les classer en trois catégories pour cadrer le rebranchement vers `presence_confort_thermique_stabilisee`. **26 consommateurs** (hors la définition dans `12_template_sensors/presence/global.yaml`). Classement conservateur : 7 à rebrancher, 14 à laisser, 5 à discuter.

---

## Catégorie 1 — À rebrancher (7)

Points où un faux-absent **court** coupe **instantanément** une décision de confort thermique (aucun garde-temps amont).

| Fichier | Rôle | Lecture actuelle | Risque si rebranché | Risque si laissé |
|---|---|---|---|---|
| `12_template_sensors/climatisation/seuils_on_off/cool/on.yaml` | Seuil d'allumage appliqué (présence/absence) | `is_state(unifiee,'on')` (état) + `unifiee` en `entity_id:` | aucun au-delà du décalage de tenue | **fuite primaire** : seuil bascule absence → `besoin` chute → `target=off` |
| `12_template_sensors/climatisation/seuils_on_off/cool/off.yaml` | Seuil d'extinction appliqué | idem on.yaml | aucun | hystérésis ON/OFF faussée si désynchronisé |
| `12_template_sensors/climatisation/decision/consigne.yaml` | Consigne clim appliquée (présence/absence) | `is_state(unifiee,'on')` (+ attribut d'affichage) | attribut `presence:` reflètera la stabilisée (cosmétique) | consigne absence poussée sur glitch |
| `11_automations/climatisation/cool/maj_consignes/absence.yaml` | Applique la consigne absence | `condition: state, unifiee = off` | ne s'active que sur absence stabilisée (visé) | coupure de confort effective sur glitch |
| `11_automations/climatisation/cool/maj_consignes/presence.yaml` | Applique la consigne présence | `condition: state, unifiee = on` | cohérence du couple présence/absence | asymétrie si seul `absence.yaml` bouge |
| `10_scripts/chauffage/decision_centrale.yaml` | Décision centrale chauffage (cible régime) | `elif is_state(unifiee,'on')` | régime tenu pendant glitch (visé) | même défaut transposé au chauffage |
| `11_automations/chauffage/decision_centrale_trigger.yaml` | Déclencheur de réévaluation chauffage | `trigger: state, unifiee` | aucun (peut garder `unifiee` en trigger additionnel) | décision figée en confort après vraie absence |

> **Plumbing** : (on/off) rebrancher la liste `entity_id:` **et** la lecture d'état ; (script+trigger chauffage) bouger ensemble.
> **Note de périmètre** : les deux derniers (chauffage) sont décisionnels confort thermique mais le **chauffage est hors périmètre minimal validé** (qui se limite aux 5 fichiers COOL clim). Ils figurent ici comme *décisionnels par nature* ; leur rebranchement effectif relève d'une décision séparée.

## Catégorie 2 — À laisser impérativement sur `presence_famille_unifiee` (14)

Observationnel, autre domaine, vérité brute, ou artefact de test. Pour tous : **risque si rebranché = décalage/incohérence indésirable** ; **risque si laissé = aucun (comportement voulu)**.

| Fichier | Rôle | Raison du maintien |
|---|---|---|
| `12_template_sensors/chauffage/diagnostic/mode.yaml` | Affichage mode chauffage | doit refléter la présence réelle |
| `12_template_sensors/chauffage/diagnostic/raison.yaml` | Affichage raison chauffage | vérité brute |
| `12_template_sensors/chauffage/diagnostic_thermique/absence/temperature_plancher.yaml` | Mesure sur cycle d'absence réel | doit voir l'absence brute |
| `12_template_sensors/chauffage/diagnostic_thermique/absence/duree_stabilisation.yaml` | Mesure de stabilisation en absence | idem |
| `12_template_sensors/climatisation/decision/verdict_mode.yaml` | `clim_verdict_*` (étiquette) — **consommé uniquement par l'UI** (`18_lovelace/dashboards/clim.yaml`, `carte_clim_decision.yaml`) | observational → vérité brute |
| `12_template_sensors/eclairage/jardin/intention.yaml` | Éclairage jardin | autre domaine |
| `12_template_sensors/modes/vacances_actives.yaml` | `vacances = demandees AND unifiee off …` | **critique** : repose sur l'absence réelle |
| `12_template_sensors/modes/vacances_raison.yaml` | Raison vacances | vérité brute |
| `01_customize/divers.yaml` | `friendly_name` | cosmétique |
| `18_lovelace/dashboards/reglages/climatisation.yaml` | Affichage UI | affichage |
| `19_button_card_templates/40_dashboards/climatisation/30_diagnostic/carte_clim_diagnostic_presence_babysitting.yaml` | Carte diagnostic présence | montre `unifiee` brut (son objet) |
| `recorder.yaml` | Historisation de `unifiee` | ne pas rebrancher ; le nouveau signal sera **ajouté** (additif, hors inventaire) |
| `00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml` | Registre CI de l'entité existante | le nouveau signal aura sa propre entrée |
| `tools/arsenal_ci/tests/fixtures/decision/d2_reason_pre_correction.yaml` | Fixture figeant le comportement « pré-correction » | référence de non-régression |

## Catégorie 3 — À discuter / ambigu (5)

Décisionnels mais soit **déjà protégés**, soit **hors périmètre thermique strict**. Avis penché indiqué.

| Fichier | Rôle / lecture | Raison du doute | Risque si rebranché | Risque si laissé | Avis |
|---|---|---|---|---|---|
| `12_template_sensors/climatisation/blocages/absence_longue.yaml` | `clim_extinction_absence_prolongee_autorisee = (unifiee off AND timer idle)` — consommé par `autorisation/cool.yaml` | **déjà immunisé** par le timer sur les drops courts | aucun fonctionnel ; touche l'entrée d'`autorisation/cool` | aucun pour les drops courts | **laisser** (sauf cohérence ; alors avec le timer) |
| `11_automations/climatisation/cool/start_timer_absence.yaml` | Démarre/annule `timer.absence_longue_clim` sur transition `unifiee` | couple indissociable d'`absence_longue` ; effet net nul sur glitch | évite démarrages parasites | démarrages/annulations parasites sans effet | **laisser** ou rebrancher **en paire** |
| `12_template_sensors/climatisation/autorisation/dry.yaml` | `autorisation_clim_dry`, `presence = is_state(unifiee,'on')` — consommé par `dry/admissibilite.yaml` | décisionnel mais mode **DRY**, secondaire à COOL | DRY tenu sur glitch ; touche l'entrée d'admissibilité DRY | DRY sensible aux faux-absents (impact non observé) | inclure **seulement** si couverture DRY voulue |
| `12_template_sensors/climatisation/autorisation/heat.yaml` | `autorisation_clim_heat`, `… and is_state(unifiee,'on')` — consommé par `heat/admissibilite.yaml` | décisionnel mode **HEAT appoint** | appoint tenu sur glitch ; touche l'entrée d'admissibilité HEAT | appoint sensible aux faux-absents | idem DRY — hors périmètre minimal |
| `12_template_sensors/climatisation/silence/autorisation.yaml` | `clim_silencieux_autorise`, `presence = is_state(unifiee,'on')` — consommé par `silence.yaml` | décisionnel mais **acoustique**, pas thermique | suit la stabilisée (hors scope thermique) | fenêtre silence peut basculer sur glitch (bruit) | **laisser** — hors périmètre thermique |

---

## Synthèse de périmètre

- **Périmètre minimal validé** = **5 fichiers COOL clim** (Catégorie 1, hors les 2 chauffage) : `seuils_on_off/cool/on.yaml`, `seuils_on_off/cool/off.yaml`, `decision/consigne.yaml`, `cool/maj_consignes/absence.yaml`, `cool/maj_consignes/presence.yaml`.
- **Hors périmètre par construction** : aucun fichier sécurité/alarme, aucun maillon `besoin`/`admissibilite`/`target_mode`, `presence/global.yaml`. `autorisation/cool.yaml` **ne lit pas** `unifiee` directement (présence via `absence_prolongee`, Catégorie 3, timer-gardée).

## État de déploiement V1+V2

> Réconciliation entre le classement initial (ci-dessus) et ce qui a été
> **réellement rebranché**. Le classement initial est conservé tel quel comme
> trace d'audit ; cette section le corrige là où la contre-expertise runtime l'a
> infirmé.

- **V1 — rebranché** : les **5 fichiers COOL** de la Catégorie 1 (hors les 2
  chauffage). Conforme au périmètre minimal.
- **V2 — rebranché** : **2 fichiers initialement classés Catégorie 3 (« à
  discuter »)**, requalifiés en chemins de coupure **actifs** :
  - `blocages/absence_longue.yaml` — le verdict initial « **déjà immunisé par le
    timer** sur les drops courts » est **infirmé** : la fenêtre de ~5 s **avant**
    le démarrage du timer (`cool/start_timer_absence.yaml`, `delay: 5 s`) ouvre
    une coupure COOL transitoire (via `clim_extinction_absence_prolongee_autorisee`
    → `autorisation/cool.yaml`). Rebranché sur la stabilisée.
  - `autorisation/dry.yaml` — le verdict initial « impact **non observé** » est
    **dépassé** : impact DRY observé le 15/06 (coupure immédiate sur présence
    brute). Rebranché sur la stabilisée.
- **Maintenu hors périmètre** : les **2 fichiers chauffage** de la Catégorie 1
  (`10_scripts/chauffage/decision_centrale.yaml`,
  `11_automations/chauffage/decision_centrale_trigger.yaml`) — **non rebranchés**
  (pas d'élargissement chauffage) ; `autorisation/heat.yaml` et
  `silence/autorisation.yaml` (Catégorie 3) — laissés (HEAT hors saison, silence
  hors périmètre thermique).
- **`cool/start_timer_absence.yaml`** : **laissé sur présence brute**. Le garde
  stabilisé étant porté par `absence_longue.yaml` (point de lecture), le timer
  reste sur la présence brute — démarrage de l'horloge 8 h à l'instant du départ
  réel, churn invisible à COOL.

Bilan : **7 fichiers rebranchés** (5 en V1 + 2 en V2), tous sur
`presence_confort_thermique_stabilisee`. Suivi d'observation :
[`suivi_post_deploiement_presence_confort_thermique_stabilisee.md`](../../04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md).

## Liens

- Cadrage contractuel associé : [`cadrage_contrat_presence_confort_thermique_stabilisee.md`](cadrage_contrat_presence_confort_thermique_stabilisee.md)
- Note de calibration `T` : [`note_calibration_tenue_T_presence_confort_thermique.md`](note_calibration_tenue_T_presence_confort_thermique.md)
- Hub présence : [`navigation/domaines/presence.md`](../../../navigation/domaines/presence.md)
- Hub climatisation : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
- Index audits : [`audits/index.md`](../../index.md)
