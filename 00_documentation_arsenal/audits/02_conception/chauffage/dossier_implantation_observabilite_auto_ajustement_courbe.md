# Dossier d'implantation — Observabilité auto-ajustement courbe

| Champ | Valeur |
|---|---|
| **Type** | Dossier d'implantation technique (préalable, lecture seule) |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Cartographie de terrain — aucun patch |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `4d23e0df` |
| **Contrat réalisé** | `contrats/chauffage/76_observabilite_auto_ajustement_courbe.md` |
| **Plan de référence** | `audits/03_plans_action/chauffage/plan_action_observabilite_auto_ajustement_courbe.md` |
| **Cadre** | Lecture seule. Aucun YAML, code ou patch. Aucune entité inventée. Aucun document figé rouvert. |

> **Objet :** cartographier le terrain réel du dépôt **avant** tout patch, pour réutiliser l'existant plutôt que le recréer. Les fichiers cités ont été vérifiés sur le HEAD courant.

---

## 1. Inventaire du terrain existant

### Automatisations — `11_automations/chauffage/courbe_de_chauffe/`
- `auto_ajustement.yaml` — décision quotidienne ; émet l'event **`chauffage_adjustment`** (branches simulation et réelle uniquement).
- `application.yaml` — déclenche l'application via les scripts.
- `correction_demarrage.yaml` — réapplication au redémarrage.
- `log_auto_ajustement.yaml` — journalisation ; ré-émet/consomme `chauffage_adjustment`.
- `11_automations/chauffage/representativite_thermique.yaml` — écrit l'état de représentativité ; émet **`chauffage_representativite_thermique_transition`**.

### Scripts — `10_scripts/chauffage/courbe_de_chauffe/`
- `application_pente.yaml`, `application_parallele.yaml` — application **transactionnelle** : génération d'un `request_id` unique, attente d'un **ACK terminal corrélé**, états applied/rejected/timeout, retry tracé.

### Helpers
- `03_input_numbers/chauffage/courbe_de_chauffe.yaml` — `pente_consigne`, `parallele_consigne` (valeurs courantes appliquées).
- `05_input_booleans/chauffage/courbe_auto.yaml` — `reglages_auto`, `courbe_auto_simulation`.
- `06_input_selects/chauffage/representativite_thermique.yaml` — état de représentativité.
- `04_input_texts/chauffage/dernier_ajustement_auto_courbe.yaml` — `chauffage_last_adjustment` (**registre dégénéré : dernière ligne seulement**).
- `04_input_texts/chauffage/raison.yaml` — `chauffage_raison` (raison **d'exécution** centrale).
- `04_input_texts/chauffage/retry_attempt1_id.yaml`, `retry_attempt2_id.yaml` — **porteurs de `request_id`** pour corrélation post-mortem du retry.

### Sensors
- Suggestion — `12_template_sensors/chauffage/courbe_de_chauffe/pente_suggeree.yaml`, `parallele_suggeree.yaml`.
- Détection écart — `12_template_sensors/chauffage/ecart_consigne/{ecart_confort,ecart_doux,ecart_froid,ecart_instantane,moyennes}.yaml`.
- Statistiques — `13_sensor_platforms/statistics/chauffage/ecarts_consigne.yaml`.
- Diagnostic — `12_template_sensors/chauffage/diagnostic/raison.yaml` (`chauffage_raison_calculee`, raison **canonique de la décision**), `mode.yaml`.
- Métriques de régulation — `nombre_cycles_*`, `duree_cycle_moyenne_*`, `amplitude_oscillation_cycle_*`, `amplitude_overshoot_arret_*`, `duree_overshoot_arret_*`.

### Binary_sensors
- `binary_sensor.poele_en_fonction_stable` et la mémoire `poele_recent` (frontière d'immunité poêle) — domaine poêle, consommés par la décision courbe.

### input_text
Voir Helpers : `chauffage_last_adjustment`, `chauffage_raison`, `retry_attempt1_id`, `retry_attempt2_id`.

### Recorder — `recorder.yaml` (allowlist explicite)
- Historisés : `sensor.ecart_consigne_instantane{,_froid,_doux}` (lignes 294-296) ; métriques de régulation `nombre_cycles_*`, `duree_cycle_moyenne_*`, `amplitude_oscillation_cycle_*`, `amplitude_overshoot_arret_*`, `duree_overshoot_arret_*` (lignes 304-310).
- **Non historisés** : `pente_consigne`/`parallele_consigne`, `pente_suggeree`/`parallele_suggeree`, représentativité, `chauffage_last_adjustment`.
- Repère de patron : section **« 🧠 ECS — Apprentissage des offsets (observabilité ECS-OFF-1) »** (lignes 323-325) — historisation lecture seule trajectoire/contexte/journal.

### Dashboards — `18_lovelace/`
- `dashboards/reglages/chauffage.yaml` — réglages courbe (toggles + sliders). **Aucun** dashboard diagnostic de la courbe.
- Patron ECS : `includes/cartes/ecs_apprentissage_offsets.yaml`, `includes/cartes/ecs_apprentissage_courbes.yaml`, `dashboards/diagnostics/ecs.yaml`.

### Logbook / Events
- `logbook.yaml` — configure `sensor.programme_chauffage`, `input_boolean.chauffage_blocage_aeration`, `script.chauffage_ecs_cycle`. **N'inclut pas** les events `chauffage_adjustment` ni `chauffage_representativite_thermique_transition`.
- Events existants : `chauffage_adjustment`, `chauffage_representativite_thermique_transition`.

### CI
- `.github/workflows/arsenal-ci-chauffage.yml` ; framework `tools/arsenal_ci/` (`decision`, `execution`, `graph`, `parsing`, `registers`, `rules`, `tests`).
- `tools/arsenal_ci/registres_entites.yaml` — **ne liste aucune entité de la chaîne courbe** (suggestion / consigne / représentativité absentes).

### ACK / corrélation
- `14_mqtt_sensors/boiler/boiler_command_feedback.yaml` — `boiler_ack_heating_set_curve_slope_raw`, `boiler_ack_heating_set_curve_shift_raw` (topics `boiler/ack/heating/set_curve_*`).
- Règle opposable côté scripts : « seul un ACK corrélé fait foi », aucun `request_id` réutilisé.

---

## 2–3. Matrice contrat 76 → existant / manquant

| Obligation 76 | État | Fichier(s) concernés | Justification |
|---|---|---|---|
| **Cycle évalué** | **Partiel → Absent** sur cycles non agissants | `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml` | Event `chauffage_adjustment` seulement sur branches sim/réelle ; cycles refusés/abstenus/silencieux bloqués par le bloc conditions → aucun event |
| **Suggestion** | **Partiel** | `12_template_sensors/chauffage/courbe_de_chauffe/pente_suggeree.yaml`, `parallele_suggeree.yaml` | Sensors présents ; event « suggestion modifiée » absent ; non historisés |
| **Décision** | **Partiel** | `auto_ajustement.yaml`, `log_auto_ajustement.yaml` | Décision capturée pour cycles agissants ; raison de refus absente |
| **Refus / abstention** | **Absent / Ambigu** | `auto_ajustement.yaml` ; (patron : `12_template_sensors/chauffage/diagnostic/raison.yaml`, `04_input_texts/chauffage/raison.yaml`) | Vocabulaire de refus non émis ; abstention = pas d'event ; refus ≠ abstention non distingués. Les « raison » existantes portent la décision **centrale**, pas le refus **courbe** |
| **Application** | **Partiel** | `03_input_numbers/chauffage/courbe_de_chauffe.yaml`, `application.yaml`, `application_pente.yaml`, `application_parallele.yaml` | Écritures + event avant/après partiels |
| **Acquittement** | **Partiel** | `14_mqtt_sensors/boiler/boiler_command_feedback.yaml`, `application_pente.yaml`, `application_parallele.yaml`, `retry_attempt1_id.yaml`, `retry_attempt2_id.yaml` | ACK corrélé complet **côté exécution** ; mais `request_id` par script, **non relié à un identifiant de cycle de décision** ; journalisé hors observabilité |
| **Trajectoire confirmée** | **Absent** | `03_input_numbers/chauffage/courbe_de_chauffe.yaml`, `recorder.yaml` | `pente_consigne`/`parallele_consigne` non historisés ; pas de distinction confirmé/intentionnel ; aucune série temporelle |
| **Complétude** | **Absent** | — | Aucun concept présent |
| **Gel / jour apprenant** | **Partiel** | `06_input_selects/chauffage/representativite_thermique.yaml`, `11_automations/chauffage/representativite_thermique.yaml`, event `chauffage_representativite_thermique_transition` | État + transition de représentativité présents ; gel implicite (consigne≠confort), pas de marqueur d'épisode ; « jour apprenant » non matérialisé |
| **Effet par fenêtre régime** | **Partiel** | `recorder.yaml` (304-310) | Métriques de régulation présentes et historisées ; aucune dérivation d'effet par fenêtre régime |

---

## 4. Briques réutilisables

| Source | Brique | Réutilisation |
|---|---|---|
| **ECS** | `18_lovelace/includes/cartes/ecs_apprentissage_offsets.yaml`, `ecs_apprentissage_courbes.yaml`, `dashboards/diagnostics/ecs.yaml`, section recorder ECS-OFF-1 (`recorder.yaml` 323-325) | **Patron complet** d'observabilité d'apprentissage (recorder + dashboard diagnostic) à **mirroir** pour la courbe |
| **Chauffage existant** | Events `chauffage_adjustment`, `chauffage_representativite_thermique_transition` | **Extensibles** (corrélation, contexte) plutôt que recréés |
| **Chauffage existant** | `input_text.chauffage_last_adjustment` (`dernier_ajustement_auto_courbe.yaml`) | Registre dégénéré **à dépasser, pas à dupliquer** |
| **Diagnostics** | `12_template_sensors/chauffage/diagnostic/raison.yaml`, `mode.yaml`, `04_input_texts/chauffage/raison.yaml` | **Modèle d'exposition de raison** (pas couverture du vocabulaire 76 — canal distinct requis) |
| **Logbook / events** | `logbook.yaml` | **Extensible** aux events courbe (non inclus aujourd'hui) |
| **Corrélation ACK** | `application_pente.yaml`/`application_parallele.yaml`, `boiler_command_feedback.yaml`, `boiler_req_heating_set_curve_slope`, `retry_attempt1_id`/`retry_attempt2_id` | **Patron de corrélation feuille (exécution) prêt** ; conforme à la décision de conception (réutiliser le `request_id` comme feuille) ; manque le **parent** (identifiant de cycle) |
| **CI** | `tools/arsenal_ci/` (framework), `arsenal-ci-chauffage.yml` | **Réutilisable** pour la garde d'étanchéité / conformité ; `registres_entites.yaml` à étendre (entités courbe absentes) |

---

## 5. Écarts techniques à combler

*(constats d'écart, sans solution technique)*

- **É-1 — Identifiant de cycle de décision (parent)** reliant les `request_id` d'exécution existants (feuilles). Aujourd'hui : feuilles présentes, parent absent.
- **É-2 — Event de cycle pour TOUS les cycles** (refus, abstention, silence inclus), hors du bloc conditions actuel qui les supprime.
- **É-3 — Vocabulaire de raison refus/abstention typé** nominal/anomal, **distinct** des `chauffage_raison` existants (raison centrale ≠ refus courbe).
- **É-4 — Historisation de la trajectoire confirmée** (`pente_consigne`/`parallele_consigne`), des suggestions et de la représentativité — absentes de `recorder.yaml`.
- **É-5 — Statut intentionnel-confirmé / effectif-mesuré** : vérifier l'existence d'une relecture de courbe (les ACK `boiler_command_feedback.yaml` confirment l'envoi ; une relecture continue de la pente/parallèle n'est pas établie).
- **É-6 — Indicateur de complétude** sur le flux périodique du cycle.
- **É-7 — Marqueur explicite d'épisode de gel** + matérialisation du **statut jour apprenant**.
- **É-8 — Couche de dérivation diagnostic** (trajectoire, convergence, réversions, persistance) lisant l'historique, sans réentrer dans la décision.
- **É-9 — Dérivation d'effet par fenêtre régime** référençant les métriques existantes (`recorder.yaml` 304-310).
- **É-10 — Dashboard diagnostic courbe** (miroir du patron ECS offsets).
- **É-11 — Couverture CI / garde d'étanchéité** de la chaîne courbe (`registres_entites.yaml` + règles `tools/arsenal_ci/`).

---

## 6. Lots d'implémentation proposés (alignés P0→P9)

| Lot | Phase plan | Contenu (capacité, pas implémentation) | Terrain concerné |
|---|---|---|---|
| **L0** | P0 | Vérifier la relecture de courbe (É-5) ; recenser les entités courbe ; figer les défauts de paramètres | `boiler_command_feedback.yaml` (vérif) ; `tools/arsenal_ci/registres_entites.yaml` (à étendre) |
| **L1** | P1 | Event de cycle universel (É-2) + vocabulaire de raison distinct (É-3) + identifiant de décision parent (É-1) | `auto_ajustement.yaml` (émission élargie, **hors chemin décisionnel**) ; canal de raison distinct (patron `diagnostic/raison.yaml`) |
| **L2** | P2 | Corrélation feuille = `request_id` existant rattaché au parent ; capture de la valeur confirmée | `application_pente.yaml`/`application_parallele.yaml`, `boiler_command_feedback.yaml`, `retry_attempt*_id.yaml` |
| **L3** | P3 | Historisation indispensable (trajectoire confirmée, suggestions, représentativité) selon la politique de rétention | `recorder.yaml` (miroir de la section ECS-OFF-1) |
| **L4** | P4 | Complétude (É-6) + statut apprenant/épisode de gel (É-7) | dérivés nouveaux ; `representativite_thermique.yaml` (existant) |
| **L5** | P5 | Couche de dérivation diagnostic (É-8) + garde d'étanchéité | `12_template_sensors/chauffage/diagnostic/` (nouveaux dérivés) ; `tools/arsenal_ci/rules` |
| **L6** | P6 | Effet par fenêtre régime (É-9), référence aux métriques existantes | référence `recorder.yaml` 304-310 |
| **L7** | P7 | Dashboard diagnostic courbe (É-10) + extension logbook | miroir `ecs_apprentissage_offsets.yaml`/`diagnostics/ecs.yaml` ; `logbook.yaml` |
| **L8** | P8 | Validation conformité 76 §11 + calibration des paramètres | transverse |
| **L9** | P9 | Clôture | transverse |

---

## 7. Risques d'implantation

| Risque | Nature | Maîtrise |
|---|---|---|
| Émettre l'event de cycle hors du bloc conditions sans toucher la **logique** de décision | Technique / régression | Émission en **observation pure**, jamais dans le chemin décisionnel ; critère : comportement inchangé (INV-1) |
| Dupliquer un système d'identifiant au lieu de réutiliser le `request_id` d'exécution | Redondance | Réutiliser la feuille existante (`retry_attempt*_id`, `boiler_req_*`) ; parent = cycle uniquement |
| Confondre `chauffage_raison`/`chauffage_raison_calculee` (raison **centrale**) avec le vocabulaire de **refus courbe** | Documentaire / sémantique | **Canal distinct** ; ne pas réutiliser l'entité existante |
| Historiser trajectoire/suggestions à mauvaise cadence | Dette / sur-observabilité | Cadence cycle (~1/jour), miroir de la section ECS-OFF-1 ; budget opposable (INV-7) |
| Capteurs dérivés réentrant dans `auto_ajustement.yaml` | Rupture d'étanchéité (INV-2) | Sens unique capture→persist→derive→present ; garde CI dédiée (É-11) |
| CI chauffage en **warn-only** : la garde d'étanchéité pourrait ne pas bloquer | Gouvernance | Étendre `registres_entites.yaml` + règles ; statut d'enforcement à arbitrer hors de ce dossier |
| « Effectif » revendiqué sans relecture réelle (É-5 non tranché) | Fonctionnel | Étiqueter « intentionnel confirmé » à défaut ; ne pas promettre l'effectif |

---

## Rattachement

- **Réalise (terrain) :** le plan d'action P0→P9 et le contrat `76`.
- **Ne rouvre :** aucun document figé (audit, architecture, revue, conception, contrat).
- **Lecture seule :** aucune entité créée, aucun fichier modifié ; fichiers vérifiés sur HEAD `4d23e0df`.

*Dossier d'implantation — 2026-06-03. Cartographie de terrain préalable. Aucun patch, aucun YAML, aucun code.*
