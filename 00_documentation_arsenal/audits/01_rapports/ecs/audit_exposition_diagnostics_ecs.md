# 🚿 ARSENAL — RAPPORT D'AUDIT · ECS — Exposition diagnostique vs contrats

## 📌 Métadonnées

- **Statut** : rapport d'audit — **lecture seule, opposable**
- **Domaine** : ECS (eau chaude sanitaire) — observabilité diagnostique
- **Dépôt** : `antoinevalentinHA/arsenal`
- **Révision auditée** : `af68a6c`
- **Posture** : audit **strictement documentaire**. Aucun runtime, capteur, automation, script, helper, `recorder.yaml`, dashboard, template, checker ou contrat modifié. Aucune remédiation codée.
- **Autorité normative** : les **contrats fonctionnels ECS** ([`contrats/ecs/`](../../../contrats/ecs/)) — *le contrat précède l'implémentation*.

### Précision d'autorité

- Les **contrats ECS** sont l'**unique autorité normative**. Ce rapport ne s'y substitue pas.
- Le rapport **consigne de manière opposable** les preuves et constats établis **sur la révision auditée** ; il **ne crée aucune nouvelle exigence**.
- La **CI n'est pas source d'exigence**. Le **runtime existant** et les **dépassements positifs** ne deviennent pas normatifs par leur seule existence.
- Le rapport porte l'**axe exposition diagnostique** ; il est **distinct** des rapports ECS existants (watchdog, offsets, consigne souhaitée), qu'il cite en connexe sans les réécrire.

### Précédent méthodologique

La méthode (chaîne de preuve, typologie de canaux, discipline anti-wishlist) reprend le précédent **Alarme** [`audit_exposition_diagnostics_alarme.md`](../alarme/audit_exposition_diagnostics_alarme.md), **sans transposition** : aucun type de diagnostic, canal, entité, gravité, verdict, ni structure d'exigence n'a été reporté depuis l'Alarme. L'inventaire est **entièrement dérivé des contrats ECS**.

---

## 🎯 1. Objet & périmètre

**Objet unique** : déterminer si les diagnostics (décisionnels, gardiens, dégradation, indisponibilité, abstention, notification) **exigés par les contrats ECS** sont (a) **produits par le runtime**, puis (b) **exposés de façon exploitable** sur le **canal contractuellement imposé** (constatabilité, historisation, journal, notification, traçabilité démontrable).

**Dans le périmètre** : la chaîne diagnostique de bout en bout — exigence contractuelle → production runtime → exposition → compréhension.

**Hors périmètre** : la justesse/sûreté des décisions ECS (on audite l'**observabilité**, pas la décision), la performance, la CI (jamais source d'exigence), et **l'audit général des dashboards** — aucun contrat ECS n'impose de projection UI dédiée (voir §13).

---

## 📚 2. Corpus contractuel lu (source d'autorité)

**29 documents** [`contrats/ecs/`](../../../contrats/ecs/) lus isolément avant toute ouverture du runtime.

**Socle constitutionnel numéroté (00→11)** : `00_fondations_et_statut`, `01_principes_perimetre_et_roles`, `02_gouvernance_autorites_et_chaine`, `03_orchestration_et_wrappers`, `04_bouclage_ecs_sous_systeme` (renvoi), `05_etats_memoire_planification`, `06_temps_timers_watchdogs`, [`07_gardiens_et_securite_active`](../../../contrats/ecs/07_gardiens_et_securite_active.md), `08_journalisation_et_tracabilite`, `09_invariants_et_interdictions`, `10_resilience_et_defaillances`, [`11_ajustement_des_offsets`](../../../contrats/ecs/11_ajustement_des_offsets.md).

**Contrats d'exécution** : `ecs_pipeline_global_cycle`, `ecs_cycle_session_open`, `ecs_cycle_session_close`, `ecs_appliquer_consigne_confirmee`, `application_consigne`, `ecs_armer_gardien_post_prelevement`, `ecs_cycle_boost_si_necessaire`, `ecs_fin_cycle_signal`, `ecs_fin_de_cycle`, `fenetre_inertie_post_cycle`, `reference_thermique_post_inertie_ecs`, `signature_thermique_chauffe`, `sensor_ecs_temperature_max_cycle`, `sensor_ecs_temperature_max_reelle_cycle`, `automation_10250000000019`, `automation_10250000000026`. + `README`.

> `04_bouclage_ecs_sous_systeme` est un **renvoi** vers le contrat canonique [`bouclage.md`](../../../contrats/bouclage.md) (sous-domaine, autorité distincte — voir §14).

---

## 🔬 3. Méthode & chaîne de preuve

Pour chaque exigence diagnostique, la chaîne suivante est établie, chaque maillon attesté par une preuve citée :

```
P-C    Contrat normatif (exigence citée)
        ↓
P-R    Production runtime (porteur, écrivains, valeurs, unicité, persistance/historisation)
        ↓
P-EXPO Exposition sur le canal exigé (constatabilité | historisation | journal | notification | traçabilité)
        ↓
P-COMP Compréhension (lisibilité, distinction des états, indisponibilité)
```

**Règle d'or** : aucune non-conformité sans base contractuelle démontrable ; le maillon rompu localise la couche fautive et détermine le verdict. Typologie : `CONFORME · PARTIEL · RUNTIME_MANQUANT · CONTRAT_AMBIGU`.

**Canaux imposés (déterminés par les contrats, non par le confort)** : silence imposé · constatabilité · historisation (Recorder) · journal/logbook · notification · traçabilité démontrable. **Aucun contrat ECS n'impose de projection UI dédiée.**

---

## 🧭 4. Normalisation contractuelle (statuts)

Chaque ligne candidate a été normalisée pour ne **pas** assimiler un helper contractuel, une mémoire transactionnelle, un état de pipeline ou une donnée persistante à une **exigence diagnostique**.

| Statut | Signification | Entre au verdict d'exposition ? |
|---|---|---|
| **DIAG_EXPLICITE** | Clause impérative d'observabilité/lecture/preuve/trace/journal/alerte | ✅ Oui |
| **DIAG_IMPLICITE_VALIDÉ** | Exposition = conséquence nécessaire validée d'un invariant | ✅ Oui |
| **INTERFACE_FONCTIONNELLE** | Interface interne nécessaire au système, sans clause d'exposition | ⚙️ Dépendance, pas de verdict |
| **CONTRAT_AMBIGU** | Obligation réelle mais paramètres/canal non définis par le contrat | ⚠️ Reste ambigu |
| **HORS_CONTRAT_DIAG** | Comportement fonctionnel / silence imposé / description de résorption | ❌ Non |

---

## 📋 5. Inventaire final — 19 exigences opposables

`DIAG_EXPLICITE` (16) + `DIAG_IMPLICITE_VALIDÉ` (3). IDs `ECS-DIAG-*` **nouveaux** (aucune renumérotation des IDs ECS existants).

| ID | Exigence | Nature | Canal imposé | Statut |
|---|---|---|---|---|
| **D1** | Statut ACK normalisé de chaque application de consigne | décisionnel | Constatabilité | DIAG_EXPLICITE |
| **D2** | Signature de démarrage : composantes nommées + verdict | décisionnel | Constatabilité | DIAG_EXPLICITE |
| **D3** | Disqualification analytique + motifs distincts | décisionnel / dégradation | Constatabilité | DIAG_EXPLICITE |
| **D4a** | Données de cycle figées, persistantes, immuables | décisionnel | Constatabilité + histo. | DIAG_EXPLICITE |
| **D6** | Trace d'auto-ajustement + offset lisible + historisation | décisionnel | Constatabilité + histo. | DIAG_EXPLICITE |
| **D7** | Horodatages opposables persistants | décisionnel | Constatabilité | DIAG_EXPLICITE |
| **D8** | Projection d'observabilité désinfection-retour (1:1) | décisionnel | Constatabilité | DIAG_EXPLICITE |
| **G2** | Gardien post-prélèvement — échec répété → alerte + journal critique | gardiens / notification | Notification + journal | DIAG_EXPLICITE |
| **G3** | Gardien post-cycle — « toujours traçable » | gardiens | Traçabilité démontrable | DIAG_EXPLICITE |
| **G4** | Watchdog — événement critique traçable | gardiens | Traçabilité | DIAG_EXPLICITE |
| **G5** | Déblocage zombie → notification persistante unique | gardiens / notification | Notification persistante | DIAG_EXPLICITE |
| **G6** | Refus d'ouverture (verrou légitime) → logbook | gardiens | Logbook | DIAG_EXPLICITE |
| **G7** | Armement gardien — mode invalide → logbook | gardiens | Logbook | DIAG_EXPLICITE |
| **DG1** | Anomalie ACK boost → logbook (notification exclue) | dégradation | Logbook | DIAG_EXPLICITE |
| **DG3** | Cycle interrompu/invalidé → traçabilité complète | dégradation | Traçabilité | DIAG_EXPLICITE |
| **I5** | Indisponibilité couche d'exécution → journalisation | indisponibilité | Journal | DIAG_EXPLICITE |
| **I1** | Capteurs tmax : indisponibilité non neutralisée (pas de valeur artificielle) | indisponibilité | Constatabilité | DIAG_IMPLICITE_VALIDÉ |
| **I2** | Référence thermique : invalidité sans valeur artificielle | indisponibilité | Constatabilité | DIAG_IMPLICITE_VALIDÉ |
| **I3** | Signature `indeterminee` en cas d'indisponibilité | indisponibilité | Constatabilité | DIAG_IMPLICITE_VALIDÉ |

Répartition par nature : décisionnel 7 · gardiens 6 · dégradation 2 · indisponibilité 3 · santé **0** · abstention **0** (requalifiée). Le canal **notification** est transversal : imposé pour G2/G5 ; exclu pour G1/DG1.

---

## 🧩 6. Interfaces fonctionnelles & hors-contrat (séparés)

**INTERFACE_FONCTIONNELLE** (dépendances vérifiées au runtime, **sans** verdict d'exposition) :
- `input_boolean.ecs_fin_cycle_signal` (handshake pipeline — ex-D5) ; `ecs_pipeline_en_cours` / `ecs_cycle_en_cours` (verrous — ex-D9) ; inhibition panne du gardien permanent (ex-A1) ; sauvegarde/restauration `mode_vaisselle` (ex-A4, porté par Vacances) ; arrêt fail-closed des offsets (ex-I4) ; volets fonctionnels de G4 (action de sûreté) et I5 (interdiction de chauffe).

**HORS_CONTRAT_DIAG** :
- Agrégat « santé ECS » (aucune clause — ne pas transposer un capteur de cohérence) ; gardien permanent hors cycle **silencieux** (ex-G1, silence imposé) ; abstention offsets (ex-A2, silence ≠ diagnostic) ; `indeterminee` interdit boost 1 (ex-A3, décision) ; dashboard « Apprentissage des offsets » (ex-D6-ui, description d'une résorption antérieure `ECS-OFF-1`) ; taxonomie de gravité graduée ; projection UI générale ; distinction inertie/prélèvement ; corrélation `request_id` (dette V1 assumée).

---

## 🔧 7. Matrice runtime consolidée (P-R)

| ID | Porteur constaté | Écrivains / unicité | Persistance / Historisation | Verdict P-R |
|---|---|---|---|---|
| D1 | `input_text.ecs_cycle_last_action_status` | `appliquer_consigne_confirmee` (valeurs signifiantes) — unique ; reset `""` par `cycle_session_open` | Non persistant (`initial:""` VOULU) | **CONFORME** |
| D2 | `sensor.ecs_signature_thermique_chauffe` | moteur template (unique) | Non historisé (non exigé) | **PARTIEL** |
| D3 | ∅ (preuve d'absence) | — | — | **RUNTIME_MANQUANT** |
| D4a | 6 helpers figés (voir §11) | gel `inertie/gel.yaml` unique (sauf miroir) | Persistants ; 3/6 historisés (exigés) | **CONFORME** |
| D6 | `input_text.ecs_dernier_ajustement` + `ecs_off_*` | flux d'apprentissage unique (`ecs_autocorrect_offsets`) | Recorder complet L683-691 | **CONFORME** |
| D7 | `input_datetime.ecs_dernier_cycle_datetime`, `ecs_tmax_timestamp` | écrivains uniques par rôle (`log/*`) | Persistants (0 `initial`) | **CONFORME** |
| D8 | `binary_sensor.ecs_desinfection_retour_vacances_autorisee` (1:1) | booléen souverain — unique par transition (pose id 032 / reset id 021) | Persistant | **CONFORME** |
| G2 | `consigne_10/applique_consigne_post_delai.yaml` (id 0005) | — | — | **PARTIEL** |
| G3 | ∅ (preuve d'absence) | — | — | **RUNTIME_MANQUANT** |
| G4 | `consigne_10/watchdog.yaml` (id 0008) | — | — | **RUNTIME_MANQUANT** (volet trace) |
| G5 | `cycle_session_open.yaml` §4 | — | — | **RUNTIME_MANQUANT** |
| G6 | `cycle_session_open.yaml:71-85` | logbook | — | **CONFORME** |
| G7 | `armer_gardien_post_prelevement.yaml:62-88` | logbook | — | **CONFORME** |
| DG1 | `cycle_boost_si_necessaire.yaml:106-118` | logbook (notification exclue) | — | **CONFORME** |
| DG3 | traçabilité éclatée (voir §12) | — | — | **PARTIEL** |
| I5 | `appliquer_consigne_bridge.yaml` + `cycle.yaml` | — | — | **PARTIEL** |
| I1 | `sensor.ecs_temperature_max_cycle` + `..._reelle_cycle` | — | — | **PARTIEL** (voir §13) |
| I2 | `sensor.ecs_temperature_max_reelle_cycle` (+ figé via gel) | — | — | **CONFORME** |
| I3 | `sensor.ecs_signature_thermique_chauffe` | — | — | **CONFORME** |

---

## 🖥️ 8. Matrice exposition / compréhension (P-EXPO / P-COMP)

Pour les `RUNTIME_MANQUANT`, la chaîne s'arrête au runtime (pas de recherche de second défaut UI). Pour les `PARTIEL`, seuls les éléments **effectivement produits** sont évalués.

| ID | P-EXPO (canal exigé) | P-COMP |
|---|---|---|
| D1 | Helper lisible (applied/rejected/timeout/"") | Valeurs techniques univoques |
| D4a | Helpers figés lisibles ; 3/6 historisés | Résumé `date\|mode\|consigne\|t0\|boost\|valide` lisible |
| D6 | Trace + offsets lisibles ; Recorder (rétention 30 j) | Trace `dd/mm • bucket • old→new • err ±x.x°C` lisible |
| D7 | Horodatages lisibles, persistants | Constatable (divergences de nom sans effet sur lecture) |
| D8 | Projection 1:1 on/off lisible | Due/non-due clair |
| DG1 | Logbook « Boost ECS non confirmé (status/boost/mode) » | Lisible |
| G6 | Logbook « Ouverture refusée … age … seuil » | Refus + âge + seuil explicites |
| G7 | Logbook « Mode invalide … » | Lisible |
| I2 | Valeur sans artefact | Pas de valeur trompeuse |
| I3 | Verdict via `state` + icône | `indeterminee` distinct |
| D2 | Produit : verdict + deltas + cohérence | `start_temp` mal étiqueté vs `t_ack_start` |
| G2 | Produit : notification mobile (événementielle) | Message clair |
| I5 | Produit : `system_log` sur rejected/timeout | Technique lisible |
| DG3 | Produit : logbook purge reboot + marqueur `\|pending` | `\|pending` implicite/technique |
| I1 | Produit : valeurs incluant `0.0` fabriqué | **Zéro artificiel indistinct d'une mesure réelle** |
| D3, G3, G4, G5 | — (chaîne arrêtée au runtime) | — |

---

## ✅ 9. Bilan final

**10 CONFORME · 5 PARTIEL · 4 RUNTIME_MANQUANT** (sur 19 opposables).

- **CONFORME (10)** : D1, D4a, D6, D7, D8, DG1, G6, G7, I2, I3.
- **PARTIEL (5)** : D2, G2, I5, DG3, I1.
- **RUNTIME_MANQUANT (4)** : D3, G3, G4, G5.

**Hors chiffrage** : 2 `CONTRAT_AMBIGU` (D4b, DG2 — voir §10).

---

## ⚖️ 10. Traitement séparé — D4b & DG2 (CONTRAT_AMBIGU)

Ces deux points restent **hors chiffrage**, **sans verdict `RUNTIME_MANQUANT`**, **sans résolution déduite du runtime**, et **soumis à un arbitrage normatif futur distinct — non ouvert dans cette consignation**.

- **D4b — artefact JSON diagnostique autonome** : les clauses `05`§7 (« sauvegardes JSON ») et `08`§7 (« archives JSON ») **nomment JSON comme forme de support**, sans imposer un objet JSON distinct, nommé et consultable. Recherche runtime : le seul JSON existant est le **backup planning/réglages** (`backup_and_restore/*_sauvegarde.yaml`) — objet différent. L'implémentation ne peut lever l'ambiguïté normative → **CONTRAT_AMBIGU maintenu**.
- **DG2 — alerte sur désynchronisation exécution/local persistante** (`10`§6 « alerte si persistance ») : seuil de persistance, entité/condition et modalité d'alerte **non définis** par le contrat. Aucune alerte de désynchronisation dédiée au runtime ; l'artefact le plus proche, `binary_sensor.ecs_consigne_hors_cycle_incoherente`, alimente une **correction silencieuse** (gardien permanent), sans alerte. Le seuil/canal ne sont **pas déduits du code** → **CONTRAT_AMBIGU maintenu**.

---

## 🔎 11. Décomposition D4a par composante

| Composante | Gel exigé | Persist. exigée | Histo. exigée | Runtime constaté | Verdict |
|---|:--:|:--:|:--:|---|:--:|
| `input_number.ecs_duree_dernier_cycle_figee` | Oui | Oui | **Oui** (`11`§9) | gel unique ; recorder L688 | CONFORME |
| `input_number.ecs_temperature_max_reelle_figee` | Oui | Oui | **Oui** (`11`§9) | gel unique ; recorder L687 | CONFORME |
| `input_text.ecs_resume_dernier_cycle_fige` | Oui | Oui | **Oui** (`11`§9) | gel unique ; recorder L691 | CONFORME |
| `input_number.ecs_temperature_max_figee` (max cycle pur) | Oui | Oui | **Non** | gel unique ; absent recorder (non exigé) | CONFORME |
| `input_number.ecs_duree_chauffe_reel_backup` | Oui | Oui | **Non** | gel unique ; absent recorder ; manque `unit`/`mode` (cosmétique) | CONFORME |
| `input_text.ecs_dernier_cycle_resume` (miroir) | Oui | Oui | **Non** | écrit par gel **et** `log/debut` (`\|pending`) — miroir non-unique **par conception** ; absent recorder | CONFORME |

**Distinctions** : historisées (`duree_figee`, `temperature_max_reelle_figee`, `resume_fige`) — présentes dans Recorder ; seulement persistante et immuable (`temperature_max_figee`) ; miroir/backup techniques (`duree_chauffe_reel_backup`, `dernier_cycle_resume`). Les entités absentes de Recorder **ne sont soumises à aucune clause d'historisation** → **D4a CONFORME**.

---

## 🩺 12. Détail des neuf écarts

### 12.1 Écarts PARTIEL (exposition partielle des éléments produits)

- **D2 — signature de démarrage.** Volet conforme : `state ∈ {favorable, insuffisante, indeterminee}` + attributs `delta_court`/`delta_confirmation`/`coherence_montee`. Écarts : (a) `t_ack_start` (post-ACK) matérialisé par `start_temp` **figé à l'entrée mode ECS** — divergence sémantique ; (b) observables `boost_1_active`, `disqualif_reason` explicitement exigés (`§13`) mais **absents** (recoupe D3) ; (c) `chauffe_active` = **dette contractuelle** (indicateur « à nommer », proxy `mode_bruleur=='ECS'` — **pas** `RUNTIME_MANQUANT`) ; (d) seuils **hors conformité** (non audités).
- **G2 — gardien post-prélèvement.** Verdict diagnostique `PARTIEL` fondé **exclusivement sur l'absence de journalisation critique** ; l'alerte utilisateur est **produite** (notification mobile via `script.notification_envoyer`, événementielle). Double tentative présente (repeat 2 + ACK). *Constat fonctionnel associé, hors preuve diagnostique* : pas de voie de **fallback matériel distinct** (les deux tentatives et le reset passent par le même exécuteur bridge).
- **I5 — indisponibilité couche d'exécution.** Interdiction de chauffe **présente** (precheck `boiler_bridge_online` + garde `≠ applied`), aucune hypothèse de succès (ACK `applied` corrélé exclusif). Journalisation **partielle** : présente sur `rejected`/`timeout` (`system_log.write`), **absente sur l'abort bridge-offline du precheck** (`stop:` sans journal).
- **DG3 — cycle interrompu/invalidé.** Traçabilité **éclatée et implicite** : logbook « État ECS incohérent purgé au démarrage » (`guard_pipeline_demarrage`, reboot seulement) ; watchdog **silencieux** ; reprise/reboot mi-inertie silencieux. Seul marqueur a posteriori : résumé bloqué `|pending`. **Signal non émis pour un cycle réellement interrompu : confirmé** (producteur unique `gel.yaml`, jamais atteint si `timer.cancel`/reboot). `10`§7 exige « traçabilité **complète** » → écart.
- **I1 — capteurs tmax face à l'indisponibilité.** Voir analyse approfondie §13.

### 12.2 Écarts RUNTIME_MANQUANT (preuve d'absence par recherche ciblée)

- **D3 — disqualification motivée.** `cycle_disqualifie` / `disqualif_reason` / `boost_1_requested` / `boost_2_requested` : **0 occurrence runtime** (grep dépôt) — présents uniquement en doc contrat. Substitut : segment `boost` (index 4) du résumé, **binaire `oui/non`**, ne distinguant **pas** boost 1 de boost 2.
- **G3 — gardien post-cycle.** Le **gardien lui-même est introuvable** : aucun mécanisme keyé sur `ecs_fin_cycle_signal` ne vérifie le rabaissement (seul consommateur du signal = `auto_ajustement_offset`, offsets). L'absence de trace est la **conséquence** de cette absence fonctionnelle plus amont.
- **G4 — traçabilité watchdog.** `consigne_10/watchdog.yaml` : **0** `logbook.log` / `system_log.write` / notification (en-tête « Aucun log utilisateur »). L'action de sûreté (rabaissement + libération verrou) est présente (dépendance vérifiée), mais **l'événement critique n'est tracé nulle part**.
- **G5 — notification persistante de déblocage zombie.** **0 `persistent_notification`** dans tout le domaine ECS. Le déblocage zombie de `cycle_session_open` est **silencieux**.

---

## 🌡️ 13. Analyse approfondie I1 — racine `sensor.ecs_temperature_ballon_securisee`

**Racine amont.** Les deux capteurs tmax sourcent `sensor.ecs_temperature_ballon_securisee` (`12_template_sensors/ecs/temperature.yaml`), **conçu pour ne jamais être `unavailable`** et qui **fabrique `0.0`** au bootstrap froid :

```
# temperature.yaml — branche else (source non numérique, aucun état/last_valid)
{{ this.attributes.get('last_valid', 0) | float(0) | round(1) }}   → 0.0
```

Ce `0.0` **numérique** (jamais un sentinel) passe le filtrage des capteurs tmax, qui ne dépistent que `unknown`/`unavailable`/`none`.

**`sensor.ecs_temperature_max_cycle`** — chaque `float(0)` et sa garde :

| `float(0)` | Ligne | Garde | Résultat bootstrap froid |
|---|---|---|---|
| `current … if t_valid` | 43 | `t_valid = t_raw ∉ {unknown,unavailable,none}` | source `"0.0"` → valide → `current=0.0` |
| `prev_max = get('last_valid_max', current…0)` | 52 | attribut restauré sinon `current` | pas d'attribut → `prev_max=0.0` |
| `else (current \| float(0))` / `[base,current]\|max` | 60-61 | branche `in_cycle` | `0.0` |

- L'`availability` (source ∉ sentinels) est **toujours vraie** car la source sécurisée n'émet **jamais** de sentinel → le capteur n'est **jamais** `unknown` ni `unavailable`.
- Hors cycle, au bootstrap : branche `else` → `{{ prev_max }}` = **`0.0`** publié.
- L'invariant 5 du contrat `sensor_ecs_temperature_max_cycle` (« ne produit jamais de valeur numérique par défaut — reste `unknown` jusqu'à la première valeur valide » ; §5.1 « `0.0` n'est jamais acceptable ») est **structurellement inatteignable** : c'est **exactement** le cas « aucun état restauré » que le contrat §5.1 exige à `unknown`, et que le runtime rend à `0.0`.

**`sensor.ecs_temperature_max_reelle_cycle`** — **aucun `float(0)`**, invalides incluant `''` ; hors cycle → `this.state` = **`unknown`** (conforme). **Mais** en cycle ou au front `off→on` pendant la fenêtre `0.0`, branche `{{ current }}` = **`0.0`**. Protégé hors cycle, **non protégé** en cycle au bootstrap froid.

**Verdict I1 = PARTIEL.** Publication d'un **zéro artificiel démontrée** (structurelle pour `max_cycle` hors cycle ; conditionnelle en cycle pour `max_reelle`) — **pas un cas dégénéré exclu**. Racine amont dans la couche de sécurisation (frontière doctrine `parametres_invalides`/sécurisation — §14), à instruire hors de cette consignation.

---

## 🧷 14. Observations fonctionnelles connexes (hors preuve diagnostique)

- **Signal potentiellement émis après forçage watchdog** : un cycle **forcé** par le watchdog (`turn_off ecs_cycle_en_cours`) réarme la fenêtre d'inertie et peut donc **émettre ultérieurement `ecs_fin_cycle_signal`** ~15 min plus tard, **sans distinction nominal/forcé**. Observation fonctionnelle à instruire ; **ne modifie pas** le verdict `PARTIEL` de DG3.
- **G2 sans fallback matériel distinct** : constat fonctionnel associé, hors preuve diagnostique.
- **Divergences onomastiques** : `ecs_pic_thermique` (contrat) → `ecs_tmax_timestamp` (runtime, `ecs_pic_thermique` inexistant) ; `ecs_dernier_cycle` → `ecs_dernier_cycle_datetime` ; fichier `fin_de_cycle_signal.yaml` → entité `ecs_fin_cycle_signal` (entité conforme au contrat) ; ACK `_result` (doc `application_consigne`) → `_status` (runtime).
- **D7 non-modifiable** : garantie **documentaire** seulement (aucune garde technique).

---

## 🟢 15. Dépassements positifs non opposables

Présents au runtime, **au-delà** des 19 exigences ; **à ne pas transformer en exigence** :
- `binary_sensor.ecs_consigne_hors_cycle_incoherente` (détecteur riche alimentant la correction silencieuse) ;
- `alerte_rebond.yaml` (id 018) : notification mobile sur chauffe ECS sans demande HA ;
- `reset_verrou_cycle.yaml` (id 022) : notification mobile « Verrou cycle ECS levé » au reboot ;
- signature : `elapsed_s`, `mode_bruleur`, `temperature_actuelle` au-delà du minimum ;
- surface diagnostique `12_template_sensors/ecs/log/*` + `input_number.ecs_diagnostic`.

---

## 🚧 16. Frontières de domaine

- **Boiler** : `sensor.boiler_ack_dhw_set_setpoint_status`, `binary_sensor.boiler_bridge_online`, `input_text.boiler_req_dhw_set_setpoint` — possédés par [`contrats/boiler/`](../../../contrats/boiler/) ; l'ECS **consomme**.
- **Résilience intégrations** : fraîcheur/disponibilité/recovery de la couche d'exécution — `resilience_integrations.md` (recoupe I5).
- **Pannes secteur** : `input_boolean.panne_secteur_active` conditionne l'inhibition du gardien permanent.
- **Vacances** : `binary_sensor.vacances_actives`, `timer.vacances_longues_ecs`, `input_select.mode_maison` (D8, `ecs_blocage_planifiee`, `mode_vaisselle`).
- **Notifications** : toute notification (G2/G5) transite par `script.notification_envoyer*`.
- **Bouclage** : autorité canonique [`bouclage.md`](../../../contrats/bouclage.md) (sous-domaine, hors périmètre).
- **Sécurisation des paramètres** : `sensor.ecs_temperature_ballon_securisee` (racine I1) — frontière doctrine `parametres_invalides`/sécurisation.

---

## 📺 17. Absence d'obligation contractuelle de dashboard dédié

**Aucun contrat ECS n'impose de projection UI dédiée.** Les 19 exigences sont satisfaites (ou non) sur les canaux **constatabilité / historisation / journal / notification / traçabilité**. La seule mention d'un dashboard (trajectoire d'apprentissage des offsets, `11`§9) est la **description d'une résorption antérieure** (`ECS-OFF-1`), **non impérative** — classée `HORS_CONTRAT_DIAG`. L'absence de carte n'est jamais un écart. L'évaluation UI relèverait d'une étape ultérieure distincte, **sur les seuls canaux réellement exigés**, sans inventer d'obligation de carte.

---

## 🏁 18. Suites possibles — explicitement non autorisées

Les éléments suivants **ne sont pas ouverts** par cette consignation et **ne doivent pas** être regroupés d'office :
- cadrage/remédiation des **4 `RUNTIME_MANQUANT`** (D3, G3, G4, G5) ;
- cadrage/remédiation des **5 `PARTIEL`** (D2, G2, I5, DG3, I1) — dont la racine amont I1 (`sensor.ecs_temperature_ballon_securisee`) ;
- **arbitrage normatif** de D4b et DG2 (dossier distinct) ;
- instruction de l'observation fonctionnelle « signal après forçage watchdog » ;
- toute évaluation UI.

Chacune de ces suites requiert une **autorisation distincte** et, le cas échéant, l'ouverture d'un chantier tracé au registre.

---

*Rapport d'audit lecture seule. Aucune modification runtime, Recorder, UI ou contractuelle. Identifiants `ECS-DIAG-*` nouveaux, non renumérotés.*
