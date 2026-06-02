# ==========================================================
# 🛡️ ARSENAL — RAPPORT D'AUDIT OFFICIEL
#     Domaine : Sécurité / Alarme
# ==========================================================

## 📌 Métadonnées

- **Statut** : rapport d'audit officiel — opposable
- **Domaine** : Sécurité / Alarme
- **Dépôt** : `antoinevalentinHA/arsenal` — HEAD `4336b1d`
- **Principe directeur** : *le runtime est la référence, le contrat documente le runtime*
- **Posture** : audit factuel et vérifiable. Aucun patch, aucune modification du dépôt.
- **Classes de gravité** : **Critique** · **Important** · **Mineur** · **Dette documentaire**
- **États** : *Confirmé* (lisible statiquement) · *À confirmer en runtime* (comportement d'exécution non observable statiquement)

---

## 🎯 Synthèse exécutive

Le domaine Alarme est **architecturalement sain** : pipeline canonique *Décision → Helpers → Application* réellement matérialisé, cerveau décisionnel pur, UI strictement découplée, watchdog de cohérence conforme, timers reboot-safe, garde post-reboot, mode test bifurqué dans les détections.

L'audit retient **14 constats** (après fusion des doublons), dont **3 critiques** touchant la sécurité fonctionnelle ou l'intégrité d'un accès :

- la **porte d'entrée et le garage** participent simultanément au chemin temporisé et au chemin de déclenchement immédiat (**faux positif** possible à l'entrée) ;
- le garde de fin de délai s'appuie sur un capteur **excluant porte et garage** (**faux négatif** sur la voie d'accès principale) ;
- le **code PIN clavier** est vraisemblablement inopérant (intégrité d'accès).

Le point structurant : **plusieurs angles morts de sécurité ne sont pas visibles depuis l'observabilité existante**, car certains diagnostics sont neutralisés (babysitting) ou alimentés par une donnée trompeuse (raison décisionnelle non publiée).

| Classe | Nombre | Constats |
|--------|:------:|----------|
| Critique | 3 | ALM-CRIT-1, ALM-CRIT-2, ALM-CRIT-3 |
| Important | 2 | ALM-IMP-1, ALM-IMP-2 |
| Mineur | 7 | ALM-MIN-1 → ALM-MIN-6, ALM-IMP-3 *(requalifié post-V4 — voir § Constats mineurs)* |
| Dette documentaire | 2 | ALM-DOC-1, ALM-DOC-2 |

---

## 🔴 Constats critiques

### ALM-CRIT-1 — Ouvrants d'entrée présents dans le chemin de déclenchement immédiat *(réf. initiale : C2)*

- **État** : Confirmé (écart contractuel) ; effet faux positif *à confirmer en runtime*
- **Contrat** : `50_intrusion_detection.md` — automation `1002000000007` : « déclencher l'alarme sur ouverture d'un capteur de contact surveillé **(hors ouvrants d'entrée)** ».
- **Runtime** : `11_automations/alarme/intrusion/ouverture/autres.yaml` (déclencheurs incluant `binary_sensor.contact_entree_porte` et `binary_sensor.contact_garage`) ; chemin temporisé `…/delai_entree_start.yaml` + `12_template_sensors/alarme/ouvrants_entree.yaml` (mêmes ouvertures physiques).
- **Impact** : à l'ouverture porte/garage en `armed_away`, `autres.yaml` et le démarrage du délai réagissent au même événement. La seule protection est le garde `delai_desarmement_en_cours == off`, dont la valeur dépend d'une **course** entre la chaîne du timer et la chaîne de réconciliation des contacts redondants.
- **Risque** : déclenchement réel **immédiat à l'entrée légitime**, non déterministe ; perte de confiance dans le système.
- **Orientation** : réserver `autres.yaml` aux contacts à déclenchement réellement immédiat ; sortir les ouvrants d'entrée de ce chemin (déjà couverts par le délai). Confirmer en runtime la latence relative des deux chaînes.

### ALM-CRIT-2 — Le garde de fin de délai exclut structurellement porte et garage *(réf. initiale : C3)*

- **État** : Confirmé
- **Contrat** : `50_intrusion_detection.md` — `binary_sensor.ouverture_qualifiee_maison` y est qualifié de « confirmation intrusion active » (table de dépendances + condition d'`automation 32`).
- **Runtime** : `11_automations/alarme/intrusion/ouverture/delai_entree_fin.yaml` (condition `ouverture_qualifiee_maison == on`) ; `12_template_sensors/ouvertures/ouverture_qualifiee_maison.yaml` (composition = `contact_entree_fenetre`, `contact_chambre_arnaud/matthieu`, `fenetre_sejour/chambre_parents` — **ni porte ni garage**).
- **Impact** : entrée par la porte ou le garage, ouvrant refermé, pas de désarmement, expiration du délai ⇒ garde `off` ⇒ **aucun `alarm_trigger`**. Couverture résiduelle limitée à la détection de mouvement.
- **Risque** : intrusion par la voie d'accès principale non sanctionnée à l'échéance du délai (**faux négatif**).
- **Orientation** : ne pas réutiliser un capteur à sémantique aération (M5) comme garde d'intrusion ; fonder le garde sur un état incluant les ouvrants d'entrée et mémorisant l'ouverture survenue pendant la fenêtre de délai. Aligner le contrat 50.

### ALM-CRIT-3 — Flux PIN clavier vraisemblablement inopérant *(réf. initiale : C4)*

- **État** : À confirmer en runtime (probabilité haute)
- **Contrat** : en-tête normatif du script `10_scripts/alarme/clavier.yaml` (« tous les claviers physiques passent par ce script » ; routage exclusif vers `alarme_armer`/`alarme_desarmer`).
- **Runtime** : `11_automations/alarme/armement/clavier.yaml` (`action: script.turn_on` sur `traitement_code_clavier`) ; `10_scripts/alarme/clavier.yaml` (reconstruit `code_saisi` et le clavier à partir de `trigger.entity_id`).
- **Impact** : `script.turn_on` ne propage ni l'objet `trigger` ni de `variables` ; le garde `trigger is defined` retombe sur `code_saisi = ''` et la première condition arrête le script ⇒ armement/désarmement par **code PIN sans effet**. Le **badge RFID** (automation `10020000000026`) n'est pas concerné.
- **Risque** : moyen d'accès clavier silencieusement hors service, non détecté par l'observabilité.
- **Orientation** : confirmer par un test PIN réel ; faire transiter le contexte du clavier vers le script de manière explicite plutôt que par `trigger`.

---

## 🟠 Constats importants

### ALM-IMP-1 — Babysitting demi-intégré : neutralise le diagnostic, n'inhibe pas la décision *(réf. initiale : C6)*

- **État** : Confirmé (fait structurel) ; réalisation du risque *à confirmer en runtime*
- **Contrat** : `99_hors_perimetre_et_extensions.md` (babysitting cité comme inhibiteur explicite admissible) ; `96_diagnostic_blocage_armement_incoherence.md` (un diagnostic ne doit jamais dépendre de `input_boolean.mode_babysitting`).
- **Runtime** : `10_scripts/alarme/decision_centrale.yaml` (ne lit pas `mode_babysitting`) ; `12_template_sensors/alarme/coherence.yaml` (force « cohérent » si `mode_babysitting == on`).
- **Impact** : si la présence sécurité retombe à `off` (membres tracqués absents) pendant qu'un baby-sitter et des enfants sont présents, le cerveau peut décider `ARMEMENT_AUTORISE` et armer ; un mouvement déclenche alors une fausse intrusion — **sans alerte de cohérence**, neutralisée par le babysitting.
- **Risque** : armement automatique en présence humaine non tracquée, sans filet d'observabilité. **Escalade en Critique** si la présence ne couvre pas le baby-sitter (à confirmer).
- **Orientation** : trancher le rôle du babysitting (inhibiteur du cerveau **ou** non-neutralisation du diagnostic) ; les deux comportements actuels ne peuvent coexister sans masquer le risque.

### ALM-IMP-2 — Autorité et observabilité de la raison décisionnelle *(fusion C1 + C14)*

- **État** : Confirmé
- **Contrat** : `30_decision_centrale.md` (helpers — `input_text.alarme_raison` écrit **exclusivement** par le cerveau ; interdit d'écrire `alarme_*` depuis une automation/script) ; `40_application_decision.md` (`alarme_raison` listée en sortie obligatoire). Contradiction documentaire interne avec `04_input_texts/alarme/raison.yaml` (« écrit par scripts d'armement/désarmement ET decision_centrale »).
- **Runtime** : `10_scripts/alarme/decision_centrale.yaml` (variable `raison` calculée mais **jamais publiée** ; seuls `alarme_decision` et `alarme_etat_cible` sont écrits) ; `armement.yaml`/`desarmement.yaml` (écrivent `alarme_raison = "armement"/"desarmement"`) ; `11_automations/alarme/system/alerte_incoherence.yaml` (affiche `alarme_raison` dans son alerte critique).
- **Impact** : la justification riche du cerveau n'est jamais exposée ; en cas d'échec d'application, l'alerte critique affiche `"armement"`/`"desarmement"` au lieu de la cause réelle. Inversion d'autorité interdite + code mort.
- **Risque** : diagnostic d'incident dégradé sur un système de sécurité ; doctrine contradictoire.
- **Orientation** : arbitrer une autorité unique sur `alarme_raison` (cerveau, ou séparation raison décisionnelle / dernier événement) puis aligner contrat 30, helper `raison.yaml` et `alerte_incoherence`.

### ALM-IMP-3 — Auto-extinction sirène *(réf. initiale : C8)* — ⤵ **requalifié en Mineur (post-V4)**

> Ce constat a été **requalifié de Important 🟠 vers Mineur 🟡** après la validation terrain **V4** (énoncé complet : § Constats mineurs › ALM-IMP-3). Repère conservé ici pour la **traçabilité** : le code `ALM-IMP-3` reste l'identifiant stable du constat ; seule sa gravité change.

---

## 🟡 Constats mineurs

### ALM-MIN-1 — Désynchronisation déclencheurs / entrées du cerveau (contexte visite) *(réf. initiale : C5)*

- **État** : Confirmé (impact opérationnel atténué)
- **Contrat** : `30_decision_centrale.md` (interfaces : `presence_visiteur` et `visite_en_cours` listés comme contexte visite).
- **Runtime** : `11_automations/alarme/application_decision_centrale.yaml` (déclenche sur `visite_en_cours`, non lu par le cerveau ; ne déclenche pas sur `presence_visiteur`) ; `10_scripts/alarme/decision_centrale.yaml` (lit `presence_visiteur` en première priorité).
- **Impact / risque** : incohérence de câblage ; effet atténué car `binary_sensor.presence_famille_securite` inclut `presence_visiteur` et reste un déclencheur. Risque résiduel si `presence_visiteur` et `visite_en_cours` divergent côté domaine source.
- **Orientation** : aligner la liste de déclencheurs sur les entrées réellement lues ; clarifier la source de vérité « visite active ».

### ALM-MIN-2 — Double bip de désarmement + absence de garde mode test *(réf. initiale : C7)*

- **État** : Confirmé — **correctif implémenté + déployé** (CH-4-A, commit `5892d35` ; pull + reload scripts/automatisations effectués). **Validation terrain opportuniste en attente** — constat **non clôturé**.
- **Contrat** : `05_input_booleans/alarme/mode_test.yaml` (« Tester un système ne doit jamais produire d'effets réels ») ; `50_intrusion_detection.md` I2 (bifurcation mode test obligatoire).
- **Runtime** : `10_scripts/alarme/desarmement.yaml` (`sirene_bip_bip` gardé `mode_test off`) ; `11_automations/alarme/sirene/bip_desactivation.yaml` (`sirene_bip_bip` sur `disarmed`, `condition: []`) *(automatisation supprimée en CH-4-A)*.
- **Impact / risque** : double émission sonore au désarmement nominal ; bip émis aussi en mode test et sur désarmement automatique (brèche du principe mode test).
- **Orientation** : émetteur de feedback unique ; ajouter une garde mode test si l'automatisation est conservée. → **Réalisé en CH-4-A** (`5892d35`) : émetteur unique = `script.alarme_desarmer` ; bip restreint aux origines explicites (`dashboard`/`clavier`/`badge`) ; `bip_desactivation.yaml` supprimée ; mode test silencieux conservé ; bips d'armement et de début de délai inchangés. **Implémenté + déployé HA ; validation terrain en attente.**

### ALM-MIN-3 — Durée de blocage incohérente (5 min déclarés / 3 min appliqués) *(réf. initiale : C9)*

- **État** : Confirmé
- **Contrat** : `60_delais_et_blocages.md` (timer dédié = mécanisme de levée canonique) ; en-tête de `08_timers/alarme/blocage_armement.yaml` (« Durée fixe (5 minutes) »).
- **Runtime** : `08_timers/alarme/blocage_armement.yaml` (`duration: "00:05:00"`) vs `11_automations/alarme/armement/blocage/blocage_start.yaml` (`timer.start … duration: "00:03:00"`).
- **Impact / risque** : qualification « durée fixe » fausse ; observabilité du temps restant trompeuse ; durée effective de blocage = 3 min.
- **Orientation** : source unique de la durée (timer ou surcharge documentée).

### ALM-MIN-4 — Code et conditions morts dans le cerveau *(réf. initiale : C13)*

- **État** : Confirmé
- **Contrat** : `40_application_decision.md` (« déterministe / sans effet de bord »).
- **Runtime** : `10_scripts/alarme/decision_centrale.yaml` (variable `alarme_etat` calculée et inutilisée ; branche `DELAI_ENTREE` testant `… and not presence_securite`, toujours vrai à ce stade de l'`elif`). Dépendance présence : `12_template_sensors/presence/securite/presence.yaml` (clauses `is_state('person.valentin'/'constance', 'Zone maison')`, jamais vraies — aucune zone n'est nommée « Zone maison »).
- **Impact / risque** : nul fonctionnellement (redondances) ; bruit de relecture, pièges de maintenance.
- **Orientation** : nettoyer variables/conditions mortes ; corriger ou retirer la comparaison de zone côté présence.

### ALM-MIN-5 — Double invocation de `sirene_brutale` en fin de délai *(réf. initiale : C15)*

- **État** : Confirmé
- **Contrat** : `50_intrusion_detection.md` §9 (dette documentée : `automation 32` court-circuite le pipeline en appelant `sirene_brutale` directement).
- **Runtime** : `11_automations/alarme/intrusion/ouverture/delai_entree_fin.yaml` (`alarm_trigger` + `script.sirene_brutale`) ; `11_automations/alarme/sirene/sirene_forte.yaml` (sur `triggered` → `script.sirene_brutale`).
- **Impact / risque** : `alarm_trigger` → état `triggered` → `sirene_forte` déclenche `sirene_brutale`, déjà appelée par `delai_entree_fin`. Effet pratique négligeable (`mode: single`, MQTT idempotent).
- **Orientation** : à traiter avec la refonte « intrusion confirmée » (dette §9) — chemin unique `triggered → sirene_forte`.

### ALM-MIN-6 — Mismatch nom de fichier ↔ identifiant d'entité *(réf. initiale : C11)*

- **État** : Confirmé
- **Contrat** : aucun (hygiène de dépôt ; conservé au titre de l'ancrage runtime).
- **Runtime** : `06_input_selects/alarme/mode_armement.yaml` (entité `mode_alarme`) ; `03_input_numbers/alarme/delai_desarmement.yaml` (entité `alarme_delai_entree`).
- **Impact / risque** : recherche par nom de fichier trompeuse ; friction d'indexation / Code Search. Aucun effet fonctionnel.
- **Orientation** : harmoniser nom de fichier et entité (sans renommer l'entité).

---

### ALM-IMP-3 — Auto-extinction sirène : mécanisme réel côté device *(réf. initiale : C8 ; requalifié Important → Mineur, post-V4)*

> **Requalification (post-V4, dépôt `e3d1349`) — traçabilité.** Gravité **Important 🟠 → Mineur 🟡**. Le code `ALM-IMP-3` est conservé comme identifiant stable ; la section a été déplacée ici depuis « Constats importants » (où subsiste un repère) pour refléter la nouvelle gravité, sans réécrire l'historique.

- **État** : **Requalifié** après validation terrain **V4**. `switch.sirene_alarm` **confirmé inexistant** (déclaré nulle part) → automatisation `11_automations/alarme/sirene/stop.yaml` **morte** ; `delay` long **non conforme mais latent** (jamais exécuté).
- **Mécanisme réel (établi par V4)** : l'auto-extinction est portée par le **device**. `script.sirene_brutale` publie `warning/burglar` avec `"duration": number.sirene_max_duration` (helper **réel**) ; la sirène **s'arrête seule** à l'échéance, et un **redémarrage Home Assistant pendant le hurlement ne modifie pas ce comportement** → coupe-circuit **reboot-safe côté device**. Coupe explicite au désarmement via `script.arret_sirene` (`warning/stop`).
- **Contrat** : `00_gouvernance_alarme.md` (interdiction des `delay` longs comme mécanisme de sûreté) — non-conformité **latente** (code mort) ; `70_sirene_actions_terminales.md` (actions terminales).
- **Impact résiduel** : **aucun risque de sécurité** (coupe-circuit assuré et reboot-safe). Résidu = **code mort** (`stop.yaml`, entité fantôme `switch.sirene_alarm`) + **non-conformité `delay` latente** + **dette de représentation** (l'en-tête promet une auto-extinction HA inopérante ; le mécanisme réel — durée device — n'est documenté nulle part comme canonique).
- **Orientation (dette technique / gouvernance)** : retirer l'automatisation morte et la référence fantôme ; **documenter la durée device comme coupe-circuit canonique** (et `arret_sirene` comme coupe immédiate). Traitement au titre de **CH-4** (lot CH-4-B), **sans urgence de sécurité**.

---

## 📚 Dette documentaire

### ALM-DOC-1 — Décalage systématique des en-têtes/chemins des contrats 20/30/40 *(réf. initiale : C10)*

- **État** : Confirmé
- **Contrat** : `20_interfaces_contexte_et_helpers.md` (contient « Modèle d'états & vocabulaire ») ; `30_decision_centrale.md` (contient « Interfaces contexte & helpers ») ; `40_application_decision.md` (contient « Décision centrale (pure) »).
- **Runtime** : sans objet (constat purement documentaire).
- **Impact / risque** : titres et balises `## Chemin` internes désalignés des noms de fichiers ; conséquence : **aucun contrat ne décrit réellement l'« application de la décision »** (le fichier `40` est occupé par la décision pure). Navigation et opposabilité dégradées.
- **Orientation** : réaligner en-têtes/chemins sur les noms de fichiers ; restaurer un contrat « application_decision » distinct.

### ALM-DOC-2 — Notification persistante visiteur documentée mais inexistante *(réf. initiale : C12)*

- **État** : Confirmé
- **Contrat** : `80_notifications_et_feedback.md` (« `notification_id: visiteur_etat` gérée uniquement par `11_automations/alarme/visite/notification_persistante.yaml` »).
- **Runtime** : absence du dossier/fichier `11_automations/alarme/visite/` (vérifiée par l'arborescence du domaine).
- **Impact / risque** : gestionnaire unique pointant un fichier absent ; le `notification_id visiteur_etat` n'est produit nulle part.
- **Orientation** : créer la notification ou retirer la clause du contrat 80.

---

## ✅ Points conformes (rappel)

- Pipeline canonique réellement matérialisé ; ordre décisionnel runtime identique au canon contractuel.
- UI strictement découplée : cartes en lecture seule, unique action `script.arret_sirene` confirmée ; aucune écriture de helper ni appel `alarm_control_panel` depuis l'UI.
- Watchdog de cohérence blocage conforme (diagnostic pur local, événementiel, garde 500 ms, `mode: single`, correction minimale).
- Scripts d'application idempotents (garde d'état) ; `arret_sirene` inconditionnel et prioritaire.
- Résilience reboot : timers `restore: true`, garde `systeme_stable`, cible `NOOP` en entrées dégradées.
- ID d'automatisations uniques (aucune collision) ; code d'accès chargé depuis `secrets.yaml` (`mode: password`).

---

## 🧭 Priorisation des suites

1. **ALM-CRIT-2** puis **ALM-CRIT-1** — sécurité fonctionnelle de la voie d'accès principale (faux négatif et faux positif).
2. **ALM-CRIT-3** — confirmer puis rétablir l'intégrité de l'accès clavier.
3. **ALM-IMP-1** — arbitrer le babysitting (potentiel d'escalade en critique).
4. **ALM-IMP-2** — restaurer une raison décisionnelle fiable pour le diagnostic d'incident.
5. **ALM-IMP-3** — statuer sur le coupe-circuit sirène.
6. **Mineurs / Dette documentaire** — à planifier hors chemin critique.

---

*Fin du rapport d'audit officiel. Tous les constats conservés reposent sur un contrat et/ou un fichier runtime cités. Les éléments « à confirmer en runtime » sont explicitement signalés. Aucun patch n'est proposé.*
