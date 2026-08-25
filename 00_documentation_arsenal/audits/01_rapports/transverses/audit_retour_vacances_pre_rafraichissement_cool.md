# Audit terrain — Retour de Vacances et absence de pré-rafraîchissement estival (COOL)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit **terrain** de la chaîne conduisant du retour de Vacances planifié à la reprise du refroidissement, et de l'absence d'anticipation thermique côté climatisation. Élément déclencheur : maison jugée encore chaude, chambres trop chaudes et ventilation forte à l'arrivée, au retour d'une absence d'environ trois semaines en période de forte chaleur. |
| **Domaines** | transverse — `vacances` · `climatisation` (veto COOL, ventilation) · `chauffage` (pré-confort) · `vmc` · `aeration` |
| **Date de l'audit** | **2026-08-24** |
| **Nature** | **Audit statique + terrain, strictement lecture seule.** Aucun reboot, reload, appel de service ni changement d'état provoqué. **Aucun runtime, contrat, chantier, checker, changelog, README, YAML, test, CI, UI ni registre modifié.** Aucun correctif appliqué pendant l'audit. |
| **Base de preuves** | Dépôt `arsenal` @ `main` `dc0ce0a0` (arbre propre) · base Recorder extraite de la sauvegarde HA `arsenal_v17_2_0.tar` · `.storage/core.restore_state` de la même sauvegarde |
| **Portée normative** | **Nulle.** Aucune architecture cible décidée, aucun chantier ouvert, aucune piste promue en décision. Les formulations normatives citées renvoient à des contrats **déjà** opposables et sont signalées comme telles. |
| **Antécédents** | [`audit_absence_vacances_chauffage_climatisation_cool.md`](audit_absence_vacances_chauffage_climatisation_cool.md) (#361) · [`audit_pre_confort_vacances_saisonnalite.md`](../chauffage/audit_pre_confort_vacances_saisonnalite.md) (#695) · chantiers [`C20`](../../04_chantiers/climatisation/chantier_politique_absence_cool.md) et [`C21`](../../04_chantiers/climatisation/chantier_preparation_retour_vacances_cool.md) |

> **Ce rapport ne propose aucune implémentation.** Il ne contient ni code, ni pseudo-code de correctif, ni patch YAML. Les chaînes décrites en section B sont des **constats** du comportement déployé, pas des cibles.

---

## État Git au moment de l'audit

| Champ | Valeur |
|---|---|
| Branche | `main` |
| HEAD | `dc0ce0a070cd197888d23a8ed56cfe9787fefbe7` (`dc0ce0a0`) — *fix(system/resilience): une dérogation de couverture se déclare par témoin (#719)* |
| `git status --porcelain` | **vide** (arbre propre) |
| Commit décisif pour l'analyse | `0fa1c217` — *fix(chauffage/pré-confort): subordonner l'exception Vacances à l'autorité thermique — contrat puis runtime (#696)*, daté du **2026-08-22 16:02:38 +0200** |

> L'audit s'est déroulé **intégralement en lecture seule** sur cet arbre propre. La consignation du présent fichier au corpus est un acte **postérieur et distinct**, réalisé sur autorisation explicite du propriétaire, et **limitée à ce seul fichier** : ni `audits/index.md`, ni aucun contrat, chantier, registre, changelog ou runtime n'a été touché.
>
> **Conséquence CI assumée et signalée.** `scripts/docs_lint/docs_ci_orphan_report.py` (DOC-CI-3) exige que tout `.md` sous `audits/01_rapports/**` soit référencé dans `audits/index.md`. Mesure avant création : *183 analysés, 183 référencés, 0 orphelin*. Ce fichier sera donc compté **orphelin** tant qu'un ajout humain d'une ligne à l'index n'aura pas eu lieu. Écart **connu, volontaire et documenté ici**, non une dérive silencieuse.

---

## Environnement analysé et sauvegarde utilisée

| Champ | Valeur |
|---|---|
| Sauvegarde | `C:\dev\arsenal-runtime\arsenal_v17_2_0.tar` |
| Slug / nom | `043b449a` — « Arsenal v17.2.0 », type `partial`, `protected: false` |
| Horodatage de la sauvegarde | `2026-08-24T15:37:54Z` = **2026-08-24 17:37:54 +02:00** |
| Versions | Home Assistant Core `2026.8.3` · Supervisor `2026.07.5` |
| Base de données | `exclude_database: false` → `data/home-assistant_v2.db` présent et exploitable |
| Registres complémentaires | `data/.storage/core.restore_state` (valeurs des helpers à l'instant de la sauvegarde) |
| Couverture Recorder | **2026-07-25 04:12:00** → **2026-08-24 17:37:51** (heure locale), **929 792** états, **361** entités (allowlist `recorder.yaml`) |
| Mode d'accès | extraction vers un répertoire **temporaire de session**, hors des dépôts ; base ouverte en `file:…?mode=ro` (SQLite lecture seule). Aucune écriture dans `arsenal` ni `arsenal-runtime`. |
| Home Assistant live | **non sollicité** — non nécessaire, toutes les questions ayant été tranchées sur sources déterministes |

> **Chaîne de provenance conforme au dépôt `arsenal-runtime`** : Home Assistant → sauvegarde HA `.tar` → NAS → dépôt local. Aucun accès API, token ou SSH à Home Assistant.

---

## Périmètre réellement audité

**Normatif (lu intégralement ou sur les sections décisives)**

- `00_documentation_arsenal/contrats/vacances.md` (v1.4.0, *Normatif — Clos*)
- `00_documentation_arsenal/contrats/climatisation/` : `README.md`, `13_intensite_besoin_froid.md` (v1.1), `14_recommandation_ventilation.md` (v2.0), `15_absence_vacances_veto_cool.md` (v1.1), `12_ventilation_intention.md`
- `00_documentation_arsenal/contrats/chauffage/` : `65_pre_confort_retour_vacances.md` (V3.1) et `65_pre_confort_retour_vacances__amendement.md`
- `00_documentation_arsenal/contrats/vmc.md` (v2.8) — structure et entrées métier
- `00_documentation_arsenal/contrats/aeration_recommandation.md`
- `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md` (lignes C20, C21, C35, C37, C39)
- `00_documentation_arsenal/audits/04_chantiers/climatisation/chantier_preparation_retour_vacances_cool.md` (C21)
- `00_documentation_arsenal/audits/01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md` (#361)
- `00_documentation_arsenal/audits/01_rapports/chauffage/audit_pre_confort_vacances_saisonnalite.md` (#695)

**Runtime — dépôt @ `dc0ce0a0`**

- `12_template_sensors/climatisation/autorisation/cool.yaml`
- `12_template_sensors/climatisation/blocages/veto_absence_vacances.yaml`
- `12_template_sensors/climatisation/besoin/cool_admissible.yaml`
- `11_automations/climatisation/cool/admissibilite.yaml` (`10030000000114`)
- `11_automations/climatisation/ventilation/application_mode.yaml` (`10030000000120`)
- `10_scripts/chauffage/decision_centrale.yaml` (branche Vacances, deux axes)
- `11_automations/chauffage/pre_confort_vacances/{orchestrateur,cycle,notification}.yaml`
- `12_template_sensors/chauffage/pre_confort/{pre_confort_debut_ts,pre_confort_fenetre_valide,preconfort_raison}.yaml`
- `03_input_numbers/chauffage/duree_prechauffage_vacances.yaml`
- `recorder.yaml` (allowlist, pour établir les trous de preuve)
- `scripts/docs_lint/{docs_ci_orphan_report,docs_ci_naming,docs_lint}.py`

**Runtime — version déployée (extraite de la sauvegarde, pour confronter dépôt et terrain)**

- `data/10_scripts/chauffage/decision_centrale.yaml`

---

## Convention de lecture

Le corpus Arsenal qualifie habituellement **FAIT** (vérifié sur pièce) · **INTERPRÉTATION** (lecture fonctionnelle proposée) · **QUESTION OUVERTE** (arbitrage propriétaire requis). Cette échelle qualifie une lecture **statique** du code et des contrats ; elle est conservée pour tout ce qui relève de la conformité documentaire.

Cet audit étant **terrain**, il ajoute une seconde échelle, qui qualifie la **force probante des données historisées** :

| Qualificateur terrain | Signification | Équivalent statique |
|---|---|---|
| **PROUVÉ** | établi directement par un enregistrement Recorder ou par une valeur de `core.restore_state` | FAIT |
| **FORTEMENT INFÉRÉ** | non enregistré directement, mais établi par corrélation temporelle serrée entre plusieurs séries indépendantes | INTERPRÉTATION à fort appui |
| **NON DÉTERMINABLE** | l'entité n'est pas historisée ; aucune conclusion n'est tirée | — |

> **Règle appliquée.** Une absence de donnée n'est **jamais** convertie en preuve. Les entités hors allowlist `recorder.yaml` sont recensées en section J plutôt que suppléées par une hypothèse. Le verdict porte sur le **code déployé** (confronté à la sauvegarde), pas sur la seule prose contractuelle ; lorsque runtime et contrat divergent, la divergence est signalée et le runtime n'est jamais présumé faire autorité.

---

## A. Cadrage terrain — ce qui a réellement eu lieu

Trois éléments du cadrage initial sont **rectifiés par les données**. Ils sont consignés ici parce qu'ils conditionnent toute la suite.

### A.1 La date du retour — PROUVÉ

| Fait | Valeur |
|---|---|
| `input_datetime.debut_vacances` | `2026-08-01 10:00:00` |
| `input_datetime.fin_vacances` | `2026-08-22 14:30:00` |
| Durée de la fenêtre | 21 j 4 h 30 (cohérent avec « environ trois semaines ») |
| `binary_sensor.vacances_actives` → `off` | **2026-08-22 14:30:00** |
| `input_select.mode_maison` `Vacances` → `Normal` | 2026-08-22 14:30:10 |
| `binary_sensor.presence_famille_unifiee` → `on` | **2026-08-22 15:13:48** |

Le retour terrain est le **22 août 2026**, non le 24. Le 24 août est la date de l'audit.

**Corroboration physique indépendante — PROUVÉ.** Trois séries sans lien avec la chaîne de présence concordent :

| Grandeur | 20/08 | 21/08 | **22/08** | 23/08 | 24/08 |
|---|---|---|---|---|---|
| `sensor.co2_sejour` (max jour, ppm) | 431 | 420 | **838** | 813 | 774 |
| `sensor.bruit_chambre_enfants` (max jour, dB) | 32 | 32 | **58** | 55 | 43 |
| `switch.clim_power` (durée `on`, h) | 0,00 | 0,00 | **6,90** | 7,17 | 7,47 |

Le bruit en chambre enfants quitte son plancher de 32 dB entre **15:12:03 et 15:22:02** le 22/08 — l'arrivée physique se situe dans cette fenêtre, cohérente avec la détection de présence à 15:13:48.

### A.2 L'état thermique au retour — PROUVÉ

La maison n'était **pas** proche de 30 °C à l'arrivée : elle était à **26,6 °C** en chambres.

| Date | `temperature_moyenne_maison` (moy. jour) | `temperature_max_chambres` (max jour) | `temperature_jardin` (max jour) |
|---|---|---|---|
| 01/08 (départ) | 24,8 | 26,8 | 31,0 |
| 08/08 | 27,5 | 28,6 | 35,0 |
| 13/08 | 29,4 | 30,9 | **38,2** |
| **14/08 (pic intérieur)** | **30,0** | **31,2** | 35,2 |
| 18/08 | 28,8 | 29,7 | 32,1 |
| 20/08 | 28,1 | 28,7 | 25,0 |
| 21/08 | 27,2 | 28,0 | 25,4 |
| **22/08 (retour)** | 26,0 | 27,1 | 29,1 |

Le pic à 30,8–31,2 °C date du **14 août**. Un épisode extérieur frais les 20–22/08 (maxima 25,0 / 25,4 °C) a permis une décroissance **passive** de 30,0 → 26,4 °C entre le 14/08 et le 22/08 au matin, soit **≈ 0,45 °C/jour ≈ 0,019 °C/h**. Le souvenir d'une maison « proche de 30 °C » correspond à la réalité du séjour, pas à celle de l'arrivée.

### A.3 Le refroidissement n'a pas commencé avant l'arrivée — PROUVÉ

`switch.clim_power` passe à `on` le **2026-08-22 à 15:18:49**, soit **5 minutes et 1 seconde après** la détection de présence (15:13:48) et **quelques minutes après** l'arrivée physique (15:12–15:22). Le refroidissement a été **déclenché par** le retour, pas engagé en anticipation de celui-ci. Le ressenti « ça avait déjà commencé » est exact à la minute près et parfaitement compatible avec ce mécanisme — mais la cause n'est pas une anticipation.

---

## B. Comportement actuel — chaînes exactes (constat)

### B.1 Domaine Vacances — amont commun

`contrats/vacances.md` v1.4.0 impose cinq niveaux séparés : Paramétrage → Support temporel → Demande → **Effectivité** → Application de contexte.

La vérité métier finale est `binary_sensor.vacances_actives`, qui vaut `on` si et seulement si `vacances_demandees = on` **ET** `presence_famille_unifiee = off` **ET** `visite_en_cours = off` (§4.3).

> **Point structurant.** `vacances_actives` **s'effondre dès le retour de présence**. C'est le contrat. Toute préparation adossée à cette vérité cesse mécaniquement au moment même où les occupants rentrent, et ne peut donc jamais couvrir la phase de rattrapage post-arrivée.

Le domaine est boot-proof : l'orchestrateur de fenêtre (§4.1.1) couvre six déclencheurs dont `homeassistant: start`, et `now()` n'apparaît dans aucun template du domaine (§12, invariant 3).

### B.2 Chauffage — pré-confort retour Vacances (seule anticipation existante)

Contrats : `chauffage/65_pre_confort_retour_vacances.md` (V3.1) et son amendement.

Chaîne constatée dans le runtime déployé :

- `input_datetime.fin_vacances` et `input_number.duree_prechauffage_retour_vacances` alimentent `sensor.pre_confort_debut_ts` (= `fin_vacances` moins la durée en secondes) et `sensor.pre_confort_fin_ts` (= `fin_vacances`), dans `12_template_sensors/chauffage/pre_confort/pre_confort_debut_ts.yaml` ;
- `binary_sensor.pre_confort_fenetre_valide` contrôle `debut < fin` ;
- l'automation `10240000000020` (`orchestrateur.yaml`) matérialise la fenêtre dans `input_datetime.pre_confort_debut_calcule` / `_fin_calcule`, pilote la vérité opérationnelle `input_boolean.pre_confort_actif_calcule` et deux timers strictement instrumentaux `timer.pre_confort_jusqua_debut` / `_jusqua_fin` ;
- son éligibilité exige `pre_confort_enable` **ET** `systeme_stable` **ET** `vacances_actives = on` **ET** `fenetre_valide` **ET** l'absence de `pre_confort_cycle_consomme` et de `pre_confort_cycle_override` ;
- la mémoire de cycle (anti-rebond, `65` §7) est portée par l'automation `10240000000026` (`cycle.yaml`) ;
- `10_scripts/chauffage/decision_centrale.yaml`, branche Vacances, consomme cette vérité sur **les deux axes** `desired_mode` et `reason` ;
- l'aval est inchangé : `sensor.chauffage_mode_commande` → `automation.chauffage_application` → pont MQTT chaudière.

Diagnostic dédié : `sensor.pre_confort_raison`.

### B.3 Climatisation — veto composite, **aucune anticipation**

Contrat : `climatisation/15_absence_vacances_veto_cool.md` v1.1 (chantier C20).

- `binary_sensor.clim_veto_absence_vacances` (`blocages/veto_absence_vacances.yaml`) est la **disjonction** de `clim_extinction_absence_prolongee_autorisee` et de `vacances_actives`, avec un attribut `cause` ∈ `{vacances, absence_prolongee, cumulé, aucune}`. Aucun écrivain : vérité calculée.
- `binary_sensor.autorisation_clim_cool` (`autorisation/cool.yaml`) est la conjonction de **cinq** conditions : `temperature_jardin ≥ clim_seuil_temperature_exterieure_minimum`, `clim_blocage_aeration_etage_reel = off`, `fenetre_ouverte_maison_avec_delai = off`, `clim_blocage_horaire_reel = off`, et `clim_veto_absence_vacances = off`. Elle **lit** le composite sans dupliquer sa formule (INV-VETO-6).
- L'admissibilité est un verrou de requalification porté par l'automation `10030000000114` : **porte 1** = front montant de `besoin_clim_cool` sous autorisation active ; **porte 2** = `autorisation_clim_cool` à `on` **pendant 5 minutes** avec besoin déjà vrai.
- L'aval suit `sensor.clim_target_mode` → `clim_mode_commande` → exécution idempotente (autorité de domaine, C37).

Le fichier runtime porte lui-même la frontière, en commentaire d'en-tête :

> « 🚧 FRONTIÈRE C21 : ce veto est INCONDITIONNEL ici (C20). La préparation du retour (C21) pourra le neutraliser dans une fenêtre bornée — **non implémentée à ce stade**. »

Le contrat `15` §9 déclare formellement le point d'extension et en borne l'usage futur : la neutralisation *« ne concernera jamais les autres blocages (aération, fenêtres, horaire, température extérieure) »*, et *« C20 ne crée aucune préparation, aucune fenêtre, aucune exception provisoire »* (INV-VETO-9).

Le chantier `C21` est au registre en statut **« réservé/parqué (2026-07-14) — dépend de C20 »**, *« gouvernance seule, aucun runtime »*, avec pour condition de réveil la livraison **et la validation** de C20. Or C20 est lui-même **non clôturable** tant que le scénario S7 (réduction du helper de durée pendant une absence active) n'a pas été exercé.

**Recherche exhaustive — PROUVÉ.** Aucune occurrence de `fin_vacances`, `pre_confort`, ni d'une quelconque entité `preparation_cool*` dans `12_template_sensors/climatisation/` ou `11_automations/climatisation/`. Constat identique à celui déjà consigné par #361 :

> **F-COOL-4.** *« Il n'existe aucun pré-refroidissement ni mécanisme d'anticipation du retour. La remise en route est purement réactive au retour de présence. »*

### B.4 Ventilation de la climatisation — axe orthogonal

Contrats `12_ventilation_intention.md` (Modèle B), `13_intensite_besoin_froid.md` (v1.1), `14_recommandation_ventilation.md` (v2.0).

- **Perception** : `sensor.clim_intensite_besoin_froid` = `max(0, temperature_max_chambres − seuil_extinction_clim_applique)`, projeté en ordinal `sensor.clim_intensite_besoin_froid_niveau` ∈ `{satisfait, faible, moyen, eleve, extreme}`, **mono-axe strict** (`13` §5.2 : ne lit ni `min`, ni l'écart inter-chambres, ni le CO₂, ni la présence).
- **Recommandation** : `sensor.clim_fan_mode_recommande`, grille + frein min + plafond silencieux. Lecture pure, ne pilote rien (`14` §2).
- **Résolution** : automation `10030000000120` (`application_mode.yaml`), autorité unique. Hors plage silencieuse, elle applique — en « Auto Arsenal » et clim active — un forçage **absence → Fort**, l'absence étant définie par `presence_confort_thermique_stabilisee = off` **ET** `presence_visiteur = off` ; sinon elle suit la recommandation ; en manuel elle mappe l'intention.
- **Diagnostic** : `sensor.clim_ventilation_diagnostic` ∈ `{repos, conforme, ecart, indisponible}`.

### B.5 VMC et aération naturelle — domaines distincts

- `contrats/vmc.md` v2.8 gouverne la ventilation **hygrométrique et CO₂** (humidité salles de bains, CO₂ séjour), avec veto sanitaire pollution (§17) et autorité de domaine (§16). **Aucune entrée thermique décisionnelle.**
- `contrats/aeration_recommandation.md` porte la **recommandation** d'aération naturelle : ΔHA et ΔT au-dessus de seuils saisonniers, absence de pluie, absence de canicule, avec dérogation sanitaire prioritaire sur CO₂ fort. Le contrat est explicite : la recommandation est *« non contraignante, informative uniquement »*, et *« Utilisateur → Décision finale »*.

---

## C. Horizon d'anticipation réel

### C.1 Climatisation — **zéro heure. PROUVÉ.**

Le mécanisme n'existe pas (§B.3). Mais le constat va plus loin que « zéro », et c'est le point le plus important de cet audit :

Le 22/08 à **14:30:00**, `fin_vacances` est franchi et `vacances_actives` tombe à `off`. Pourtant `sensor.clim_verdict_cool` passe de `absence_et_vacances` à **`absence_prolongee`** : la **seconde branche** du veto composite — l'absence longue qualifiée, seuil `input_number.clim_duree_absence_longue = 14,0 h` — reste vraie, puisque la présence est toujours absente. Le COOL demeure interdit.

Le veto ne tombe qu'à **15:13:48**, sur retour de présence.

> **Conséquence structurelle — PROUVÉ.** L'horizon d'anticipation du refroidissement n'est pas gouverné par la date de retour mais par la **présence effective**. Avancer `fin_vacances` de vingt-quatre heures ne déclencherait rien, `clim_extinction_absence_prolongee_autorisee` restant `on`. Toute anticipation calendaire est **inopérante** tant que la neutralisation sélective du composite prévue par C21 (I-C21-2) n'existe pas.

### C.2 Chauffage — **8 heures. PROUVÉ.**

Valeurs relevées dans `core.restore_state` de la sauvegarde :

| Élément | Valeur constatée |
|---|---|
| Valeur nominale | `input_number.duree_prechauffage_retour_vacances` = **8,0 h** |
| Bornes runtime | `min: 3`, `max: 24`, `step: 1`, `mode: box`, **clé `initial` absente** (`03_input_numbers/chauffage/duree_prechauffage_vacances.yaml`) |
| Fenêtre | `[fin_vacances − 8 h ; fin_vacances[` — **aucun arrondi calendaire**, résolution à la seconde |
| Fenêtre du cycle observé | `pre_confort_debut_calcule` = `2026-08-22 06:30:00` · `pre_confort_fin_calcule` = `2026-08-22 14:30:00` |
| État des mémoires de cycle | `pre_confort_enable = on` · `pre_confort_cycle_consomme = off` · `pre_confort_cycle_override = off` |
| Conditions nécessaires | cf. §B.2 — six conditions cumulatives, dont `vacances_actives = on` |
| Horaires ou fenêtres calendaires | **aucun** — la fenêtre est purement relative à `fin_vacances` |
| Déclencheurs | `homeassistant: start` · `systeme_stable → on` · changement de `pre_confort_enable`, `vacances_actives`, `pre_confort_debut_ts`, `pre_confort_fin_ts`, `pre_confort_fenetre_valide` · `timer.finished` (deux timers). **Aucun `time_pattern`, aucun polling** (`65` §5ter, invariants techniques V3). |
| Effet du redémarrage HA | **réconciliation complète et idempotente** : automation en `mode: restart`, recalcul systématique, timers relancés sur le delta restant, aucune activation fantôme |
| Cas où le démarrage réel serait postérieur au théorique | `systeme_stable` tardant à passer à `on` après boot ; ou chute de `vacances_actives` (une micro-bascule de présence invalide le cycle) |

**Constat de bornage — PROUVÉ.** Un helper plafonné à `max: 24` interdit **par construction** toute anticipation supérieure à J-1, y compris côté chauffage. Or `65` §5bis prescrit un délai physique `D_préchauffage = (ΔT_rattrapage / V_reprise) + D_chute + marge_sécurité` et n'énonce **aucune borne supérieure**. L'implémentation transitoire (§5ter) borne donc ce que le contrat ne borne pas.

---

## D. Chronologie terrain horodatée — 2026-08-22

Heures locales (Europe/Paris). Chaque ligne est issue d'un enregistrement Recorder sauf mention contraire.

| Heure | Fait constaté | Qualification |
|---|---|---|
| 06:30:00 | `pre_confort_debut_calcule` atteint — ouverture de la fenêtre de pré-confort chauffage | PROUVÉ |
| 06:30:09 | `input_select.chauffage_dernier_mode_decide` : `reduced` → **`comfort`** | PROUVÉ |
| 06:30:21 | `sensor.programme_chauffage` : `Eco` → **`Confort`** | PROUVÉ |
| 14:30:00 | `binary_sensor.vacances_actives` : `on` → **`off`** (franchissement de `fin_vacances`) | PROUVÉ |
| 14:30:00 | `sensor.clim_verdict_cool` : `absence_et_vacances` → **`absence_prolongee`** — **veto COOL maintenu** | PROUVÉ |
| 14:30:10 | `chauffage_dernier_mode_decide` → `reduced` ; `mode_maison` → `Normal` | PROUVÉ |
| 14:30:18 | `sensor.programme_chauffage` → `Eco` | PROUVÉ |
| 15:12:03 → 15:22:02 | `sensor.bruit_chambre_enfants` quitte son plancher : 32 → 38 dB — arrivée physique | FORTEMENT INFÉRÉ |
| **15:13:48** | `presence_famille_unifiee` et `presence_confort_thermique_stabilisee` → **`on`** | PROUVÉ |
| 15:13:48 | `clim_veto_absence_vacances` et `clim_extinction_absence_prolongee_autorisee` → **`off`** | PROUVÉ |
| 15:13:48 | `autorisation_clim_cool` → **`on`** ; `clim_verdict_cool` → `autorise_attente` | PROUVÉ |
| 15:13:48 | `clim_intensite_besoin_froid` : 2,1 → **2,6 °C** ; niveau `eleve` ; `clim_fan_mode_recommande` = **`Fort`** | PROUVÉ |
| 15:13:53 | `input_datetime.clim_debut_absence` effacé (sentinelle `1970-01-01 01:00:00`) | PROUVÉ |
| **15:18:48** | `besoin_clim_cool_admissible` → `on` — **porte 2 : autorisation stable depuis 5 min** ; `clim_target_mode` → `cool` | PROUVÉ |
| **15:18:49** | `switch.clim_power` → **`on`** ; `sensor.clim_mode_local` = `cool` | PROUVÉ |
| 15:18:50 | `clim_ventilation_diagnostic` → `conforme` (cible `Fort` appliquée) | PROUVÉ |
| 15:20:46 | `binary_sensor.fenetre_ouverte_rdc` → `on` — **action humaine** | PROUVÉ |
| 15:21:36 | `aeration_confirmee`, `aeration_episode_en_cours`, `ouverture_qualifiee_maison` → `on` | PROUVÉ |
| **15:21:37** | `switch.clim_power` → **`off`**, raison `fenetre_ouverte` — **après 2 min 48 s de fonctionnement** | PROUVÉ |
| 15:46:04 | `fenetre_ouverte_etage` → `on` | PROUVÉ |
| 16:02:12 → 16:38:59 | `temperature_max_chambres` : **26,7 → 27,1 °C** pendant l'aération, `temperature_jardin` à **29,0 °C** | PROUVÉ |
| 16:02:38 | (dépôt) commit `0fa1c217` — PR #696, garde thermique du pré-confort | PROUVÉ |
| 16:05:19 → 16:05:25 | indisponibilité générale des templates (≈ 3 s) — rechargement de configuration, déploiement de #696 | FORTEMENT INFÉRÉ |
| 16:32:31 | `clim_intensite_besoin_froid_niveau` → **`extreme`** | PROUVÉ |
| 16:48:54 | fenêtres refermées ; `aeration_*` → `off` | PROUVÉ |
| **16:53:54** | `switch.clim_power` → **`on`**, `cool`, ventilation `Fort` — reprise **après 1 h 32 min d'arrêt** | PROUVÉ |
| 19:34:17 | `clim_fan_mode_recommande` : `Fort` → `Moyen` (intensité retombée à 1,4 °C) | PROUVÉ |
| 20:15:00 | recommandation → `Faible` ; `clim_target_mode` : `cool` → `dry` (besoin de froid satisfait) | PROUVÉ |
| 20:52:14 et 21:27:58 | deux nouvelles ouvertures brèves → deux coupures supplémentaires de la clim | PROUVÉ |
| **23/08 00:00:00** | `temperature_max_chambres` passe sous **25,0 °C** — soit **8 h 47** après l'arrivée | PROUVÉ |
| **23/08 05:55:29** | `temperature_min_chambres` passe sous **24,0 °C** (seuil d'extinction présence) — **14 h 42** après l'arrivée | PROUVÉ |

### D.1 Le séjour, en synthèse — PROUVÉ

Répartition de `sensor.clim_verdict_cool` du 01/08 10:00 au 22/08 15:14 (509,2 h couvertes) :

| Verdict | Durée | Part |
|---|---|---|
| **`absence_et_vacances`** | **472,2 h** | **92,7 %** |
| `exterieur_trop_froid` | 20,1 h | 3,9 % |
| `vacances` | 14,0 h | 2,7 % |
| autres (`admissible`, `absence_prolongee`, `aucun_besoin`, `autorise_attente`, `unavailable`) | 2,9 h | 0,6 % |

Les verdicts `absence_et_vacances`, `vacances` et `absence_prolongee` sont émis **sous garde `cool_besoin`** (`15` §7, cascade `raison` rang 9) : leur présence atteste que **le besoin de froid existait**. Le refroidissement a donc été **nécessaire et refusé pendant 92,7 % du séjour** — conformément au contrat, la sobriété en absence étant une politique imposée et non un défaut.

`switch.clim_power` totalise **0 h d'allumage du 02/08 au 21/08 inclus**.

### D.2 Vitesse de rattrapage mesurée — PROUVÉ

Mesure du 22/08 16:53:54 → 20:40, climatisation en `cool`, ventilation `Fort`, extérieur passant de 26,9 à 24,9 °C :

| Grandeur | Début | Fin | Vitesse |
|---|---|---|---|
| `sensor.temperature_max_chambres` | 27,0 °C | 25,0 °C | **−0,56 °C/h** |
| `sensor.temperature_min_chambres` | 27,0 °C | 24,6 °C | **−0,65 °C/h** |
| `sensor.temperature_moyenne_maison` | 26,8 °C | 24,7 °C | **−0,54 °C/h** |

> **Portée de cette mesure.** C'est la **première caractérisation** de la vitesse de refroidissement mécanique dont Arsenal dispose. Le chantier C21 la déclarait explicitement manquante (risque R2 : *« Absence de modèle de vitesse de refroidissement »* ; I-C21-8 : *« aucune promesse de température exacte à l'échéance tant qu'aucune observation de vitesse de refroidissement n'existe »*). Elle est consignée ici comme **observation isolée**, sur un seul épisode et un seul jeu de conditions extérieures — elle ne constitue pas une calibration.

---

## E. Analyse causale

### E.1 Causes PROUVÉES

**C1 — Absence totale d'anticipation du rafraîchissement (cause racine).** Le chantier C21 est parqué, aucun runtime n'existe. Le COOL a été interdit 92,7 % du séjour puis autorisé au retour de présence. Le système n'a **jamais eu l'intention** de préparer la maison. Ce n'est pas une défaillance d'exécution : c'est le périmètre assumé et déclaré de C20 (§9, INV-VETO-9).

**C2 — Le verrou réel est la présence, pas la date.** Développé en §C.1. Le franchissement de `fin_vacances` à 14:30 n'a libéré aucune des deux branches du composite ; seul le retour de présence à 15:13:48 l'a fait.

**C3 — Cinq minutes de délai supplémentaire par verrou de requalification.** L'automation `10030000000114` déclenche la porte 2 sur `autorisation_clim_cool` à `on` `for: 5 minutes`. Écart mesuré : 15:13:48 → 15:18:48, soit **exactement 5 min 00 s**. Comportement **conforme** au verrou de requalification (`README` climatisation, principe de séparation des couches : *« un besoin préexistant à une interdiction ne devient jamais admissible par simple retour de l'autorisation »*), mais il s'ajoute au retard total.

**C4 — Aération humaine thermiquement défavorable : 1 h 32 de refroidissement perdu et +0,5 °C repris.** Fenêtres ouvertes à 15:20:46 avec **29,0 °C extérieurs contre 26,6 °C intérieurs**. Arsenal a réagi **correctement** en coupant la climatisation (blocage par `fenetre_ouverte_maison_avec_delai` puis épisode d'aération). Le résultat net est néanmoins un **réchauffement** de 26,6 à 27,1 °C et le passage de l'intensité de besoin en `extreme`. En volume horaire, c'est **le premier contributeur mesuré** au constat « chambres encore trop chaudes le soir ».

**C5 — Capacité de rattrapage limitée face à l'inertie du bâti.** 0,56 °C/h de refroidissement mécanique contre 0,019 °C/h de décroissance passive. Ramener les chambres de 27,1 à 24,0 °C demande **≈ 5 h 30 de fonctionnement continu** ; avec les coupures d'aération, il en a fallu **14 h 42**.

**C6 — Pré-confort chauffage déclenché en plein été (déjà audité et corrigé).** `sensor.programme_chauffage` = `Confort` de 06:30:21 à 14:30:18 le 22/08, maison à 26,8 °C, extérieur atteignant 29 °C. Il s'agit de la **seule occurrence** de décision `comfort` sur tout le mois couvert par Recorder, et elle coïncide **exactement** avec `[fin_vacances − 8 h ; fin_vacances[`.

La cause est établie : la garde thermique n'était **pas encore déployée**. La version déployée dans la sauvegarde du 24/08 porte bien, dans `data/10_scripts/chauffage/decision_centrale.yaml`, la condition `and is_state('sensor.chauffage_autorisation_cible', 'comfort')` sur les deux axes — mais le commit qui l'introduit (`0fa1c217`, PR #696) est daté du **22/08 à 16:02:38**, soit **1 h 32 après la fermeture de la fenêtre**, et son déploiement correspond au rechargement observé à 16:05:19.

Cet épisode est **déjà audité** par #695 et **corrigé le jour même**. Il est consigné ici parce qu'il constitue la démonstration terrain la plus directe du principe énoncé par l'amendement de `65` : **une anticipation purement temporelle, sans garde physique opposable, produit un effet contraire à son objet.** Sans effet sur le froid, il éclaire directement l'évaluation de la section G.

### E.2 Causes PROBABLES (faisceau concordant, non prouvées faute d'historisation)

**P1 — Durcissement de la référence de satisfaction au retour de présence.** `input_number.clim_seuil_extinction_absence` = 24,5 °C contre `_presence` = 24,0 °C. À 15:13:48, `clim_intensite_besoin_froid` saute de 2,1 à 2,6 °C **sans que la température ait bougé** — signature du basculement de référence contextualisée (`13` §3, contextualisation C2 assumée). Effet modeste (+0,5 °C de déficit affiché), mais il **allonge** mécaniquement la phase de rattrapage. `sensor.seuil_extinction_clim_applique` n'étant pas historisé, la démonstration reste indirecte.

**P2 — Sensibilité de la mémoire de cycle du pré-confort aux micro-bascules de présence.** Réserve déjà consignée par #361 (§9.2), liée au débruitage limité de `presence_famille_unifiee`. **Non observée** sur ce cycle.

### E.3 Causes ÉCARTÉES, avec la preuve de leur mise à l'écart

| Hypothèse examinée | Verdict | Preuve |
|---|---|---|
| Horizon d'anticipation trop court côté froid | **ÉCARTÉE** — il n'existe aucun horizon | Recherche runtime exhaustive · C21 parqué · #361 F-COOL-4 |
| Trigger trop tardif | **ÉCARTÉE** — chaîne événementielle, réaction en 5 min 01 s après la présence | Horodatage 15:13:48 → 15:18:49 |
| Fréquence d'évaluation insuffisante | **ÉCARTÉE** — aucun `time_pattern` dans la chaîne ; convergence sur événements | `orchestrateur.yaml` invariants V3 · `application_mode.yaml` |
| Pré-confort limité par une autre condition | **ÉCARTÉE côté froid** (il n'existe pas) ; **côté chaud il s'est au contraire déclenché** | §E.1 C6 |
| Redémarrage HA ayant perdu l'état pendant la fenêtre critique | **ÉCARTÉE** — le seul rechargement du 22/08 est à 16:05:19, postérieur à toute la séquence décisive | Recorder |
| VMC forte concurrençant la climatisation | **ÉCARTÉE** — `input_boolean.vmc_haute_vitesse` est **`off` sans interruption depuis le 2026-07-30 08:14:11** et ne bascule à aucun moment du séjour | Recorder, historique complet de l'entité |
| Température extérieure défavorable au retour | **ÉCARTÉE** — 25,8 °C à 15:13, sous la température intérieure. Le seul épisode défavorable (29,0 °C) coïncide avec l'aération humaine | Recorder |
| Retour de présence modifiant trop tôt le régime | **ÉCARTÉE** — le régime a changé au bon moment ; le problème est qu'il **ne pouvait pas** changer avant | §C.1 |
| Stratégie jour/nuit défavorable | **ÉCARTÉE** — `clim_mode_nuit_effectif` sans effet sur la plage 15:00–20:00 | `13` §3 |
| Capacité frigorifique insuffisante | **NUANCÉE, non retenue comme cause** — 0,56 °C/h est modeste mais suffisante : le déficit initial de 2,6 °C était rattrapable en ≈ 5 h. Le paramètre déficient est l'**heure de départ**, pas la puissance | §D.2 |

---

## F. Ventilation — conclusion spécifique

### F.1 De quelle ventilation s'agissait-il ? — **la climatisation, pas la VMC. PROUVÉ.**

`input_boolean.vmc_haute_vitesse` est resté **`off` du 2026-07-30 08:14:11 jusqu'à la fin de la période couverte**. `binary_sensor.vmc_haute_vitesse_requise` est `off` sur toute la période (seuls des `unavailable` transitoires lors des rechargements). Les trois porteurs de besoin — `vmc_etat_besoin_co2_sejour`, `vmc_etat_besoin_sdb_parents`, `vmc_etat_besoin_sdb_enfants` — sont `off`. **La VMC n'a jamais été en haute vitesse pendant le séjour ni au retour.**

Ce qui soufflait fort était le **ventilateur interne de l'unité Fujitsu**, `fan_mode = high` (« Fort »).

### F.2 Pourquoi « Fort » ? — décision métier identifiée, conforme au contrat

`sensor.clim_fan_mode_recommande` valait **`Fort`** dès avant l'arrivée et jusqu'à 19:34:17, puis `Moyen`, puis `Faible` à 20:15:00. Le moteur est `clim_intensite_besoin_froid`, à 2,6 puis 3,1 °C, niveau `eleve` puis **`extreme`** à 16:32:31. `sensor.clim_ventilation_diagnostic` est resté **`conforme`**, ce qui atteste que le réel suivait la cible.

Deux voies pouvaient produire `Fort`. **Une seule s'applique ici :**

- l'arbitrage **absence → Fort** (`12` §2) exige `presence_confort_thermique_stabilisee = off` **et** climatisation active. Or la clim ne s'allume qu'**après** le retour de présence. **Cet arbitrage n'a donc jamais été exercé** — FORTEMENT INFÉRÉ, `input_select.clim_fan_mode_cible` et `sensor.clim_mode_de_ventilation_local` n'étant pas historisés ; `core.restore_state` confirme toutefois `clim_fan_mode_cible = « Auto Arsenal »`.
- la **grille de recommandation** sur déficit `eleve`/`extreme` produit `Fort`. **C'est la cause réelle.**

### F.3 La ventilation aidait-elle, ou concurrençait-elle le refroidissement ?

**Elle aidait, sans réserve.** Il s'agit du ventilateur **interne** de l'unité en mode `cool` : il augmente le débit sur la batterie froide et la diffusion vers les chambres. Il n'introduit **aucun** air extérieur. À 26,6 °C intérieurs et 3,1 °C de déficit, `Fort` est le réglage physiquement correct.

**Aucune concurrence entre refroidissement mécanique et ventilation mécanique n'a eu lieu.** La seule concurrence observée oppose la climatisation à l'**aération naturelle humaine** (§E.1 C4), et Arsenal l'a arbitrée conformément au contrat en coupant la climatisation.

Le constat « ventilation forte à l'arrivée » n'est donc **pas un défaut** : c'est la restitution fidèle d'un déficit thermique important, par un mécanisme contractualisé.

### F.4 Arsenal distingue-t-il correctement les quatre notions ? — trois sur quatre

| Notion | Porteur | Statut |
|---|---|---|
| Rafraîchissement gratuit par air extérieur favorable | `aeration_recommandation.md` → `binary_sensor.aeration_conseillee` (ΔT, ΔHA, canicule, pluie, priorité CO₂) | ✅ modélisé — mais **recommandation non contraignante**, décision humaine |
| Ventilation sanitaire (humidité / CO₂) | `vmc.md` v2.8 — hygro/CO₂ pur, veto sanitaire pollution | ✅ modélisé, étanche au thermique |
| Refroidissement mécanique | `clim_target_mode` et sa chaîne d'autorisation/blocage | ✅ modélisé |
| **Rattrapage thermique massif avant occupation** | — | ❌ **n'existe pas** (C21 parqué) |

**Point de doctrine à signaler.** `binary_sensor.aeration_conseillee` n'est consommé par aucune couche du domaine climatisation, alors que son contrat prévoit qu'il *« peut être utilisé comme contrainte inhibitrice par des domaines consommateurs »*. Le 22/08 à 15:20, avec 29 °C dehors et 26,6 °C dedans, la recommandation était nécessairement défavorable — mais rien ne l'a signalé, et **aucune trace décisionnelle de cet arbitrage n'existe**. Comportement fonctionnel non documenté (§I, É3).

---

## G. Hypothèse « J-1 » — évaluation

L'hypothèse soumise à l'audit — avancer d'environ vingt-quatre heures le déclenchement du rafraîchissement — est ici **évaluée, non entérinée**.

### G.1 Effet dans le cas observé

Fenêtre J-1 = 21/08 14:30 → 22/08 14:30. Sur ces 24 h, `temperature_jardin ≥ 19,0 °C` (garde `input_number.clim_seuil_temperature_exterieure_minimum`, inconditionnellement opposable) pendant **14,9 h, soit 62 %**. La maison était à 27,4 °C au 21/08 14:30. À 0,56 °C/h mesurés, atteindre 24,0 °C en chambres demande **≈ 6 h**.

**Thermiquement, la cible aurait été atteinte largement avant le retour**, avec environ 9 h de fenêtre inutilisée.

### G.2 Mais J-1 seul n'aurait rien changé — trois raisons prouvées

1. **Le veto ne serait pas tombé.** Avancer la fenêtre n'agit sur rien tant que `clim_extinction_absence_prolongee_autorisee` reste `on`. Il faut la neutralisation **sélective** du composite prévue par C21 (I-C21-2), c'est-à-dire le chantier entier, pas un paramètre.
2. **Il n'existe aucun helper à régler.** Le mécanisme est absent du runtime.
3. **Le plafond `max: 24`** du helper chauffage montre que même l'anticipation existante ne peut structurellement dépasser J-1.

### G.3 Grille d'évaluation

| Critère | Verdict |
|---|---|
| Aurait-il suffi dans le cas observé ? | **Oui thermiquement** (6 h nécessaires pour 14,9 h utilisables) — **non structurellement** (veto d'absence longue) |
| Compatible avec l'architecture actuelle ? | **Oui** — le patron existe (`65` §5ter), la frontière est déclarée (`15` §9), les invariants cibles sont déjà écrits (C21 §4) |
| Coût énergétique | **Excessif en l'état** : ≈ 15 h de fenêtre pour ≈ 6 h de besoin, en maison vide, avec cycles d'extinction/relance sur hystérésis. Contraire à `65` §5bis (*« déclencher le pré-confort au plus tard nécessaire »*, *« éviter toute anticipation excessive »*, *« préserver strictement la sobriété en absence »*) |
| Risque de refroidir pour rien lors d'un retour décalé | **Élevé.** `65` §7 consomme le droit de cycle **dès la première activation** ; I-C21-5 impose qu'une fenêtre écoulée sans retour rétablisse le veto. Un retour retardé produirait donc 24 h de climatisation en pure perte, **suivies d'aucune reprise** |
| Gestion d'un changement de date de retour | **Traitée contractuellement** (D13, I-C21-6 : une modification explicite de `fin_vacances` recalcule et peut réarmer), mais **jamais implémentée ni testée** côté froid. Le risque R1 du chantier (oscillation ou préparation manquée) reste entier |
| Une durée fixe est-elle conceptuellement suffisante ? | **Non.** `65` §5bis l'énonce déjà : *« aucune valeur fixe ne peut s'y substituer durablement »*. Le 22/08 il fallait ≈ 6 h ; le 15/08, maison à 30,5 °C, il en aurait fallu ≈ 12 h ; par 15 °C extérieurs, aucune |

### G.4 Conclusion sur l'hypothèse

L'hypothèse J-1 est **plausible et architecturalement recevable**, mais elle **ne constitue pas le correctif** : elle règle un paramètre d'un mécanisme inexistant, laisse intact le verrou réel (la branche « absence longue » du veto composite), et fige une durée que le contrat de référence interdit explicitement de figer durablement.

---

## H. Options architecturales

Comparaison de **principes**, sans conception ni implémentation. Aucune de ces options n'est décidée par le présent rapport.

**Socle commun à A, B et C — sans lui, aucune option ne fonctionne.** Livrer C21 tel qu'il est déjà cadré : vérité de préparation à écrivain unique, neutralisation **sélective** du seul composite `(absence_longue OR vacances)`, gardes physiques (température extérieure, aération, fenêtres, blocage horaire) demeurant **inconditionnellement opposables**, fail-closed, boot idempotent, présence terminale, fin de fenêtre rétablissant le veto. Doctrine transverse déjà consolidée par l'amendement de `65` (§11) :

> **« Préparation du retour ≠ suppression des gardes physiques propres au système concerné. »**

| Critère | **Option 0 — statu quo** | **Option A — horizon fixe (J-1)** | **Option B — horizon adaptatif** | **Option C — hybride** |
|---|---|---|---|---|
| Principe | Reprise réactive au retour de présence | Fenêtre bornée avant `fin_vacances`, durée fixe réglable | Durée déduite du déficit et de la vitesse de refroidissement observée, recalculée à chaque cycle | Horizon plancher court, étendu **seulement** en cas de déficit important |
| Compatibilité doctrinale | ✅ contrat actuel | ⚠️ **explicitement qualifié transitoire** par `65` §5ter et I-C21-8 | ✅ **c'est la cible normative** de `65` §5bis | ✅ conforme §5bis, avec repli borné |
| Sobriété | maximale | **faible** — fenêtre dimensionnée sur le pire cas | **optimale** — « au plus tard nécessaire » | bonne — l'extension ne se paie qu'en cas de déficit réel |
| Risque de retour décalé | nul | **élevé** (droit de cycle consommé, aucune reprise) | modéré | **faible** |
| Risque de sous-préparation | **certain** — c'est le cas observé | faible | faible si la vitesse est bien caractérisée | faible |
| Comportement sur donnée indisponible | sans objet | faible risque (temporel pur) | **réel** : impose un repli explicite, jamais une valeur par défaut | **structurellement traité** : le plancher **est** le repli |
| Représentation de l'inertie | ❌ | ❌ | ✅ indirecte | ✅ indirecte |
| Prérequis d'observation | — | aucun | **bloquant** : la vitesse de refroidissement n'existe pas comme capteur (R2, I-C21-8) | plancher livrable sans prérequis, adaptation ajoutée ensuite |
| Testabilité | sans objet | triviale | difficile | **incrémentale** |

> **Lecture.** L'Option C est la seule qui soit exempte de prérequis d'observation tout en restant **sur le chemin** de la cible normative de `65` §5bis : elle transforme l'Option B d'un préalable bloquant en une évolution additive du même mécanisme. Elle suit un motif déjà accepté dans Arsenal — `13` §5.3 fixe les bandes d'intensité *« empiriquement, après observation historique réelle »*.

---

## I. Écarts contrat ↔ implémentation

| # | Écart constaté | Qualification |
|---|---|---|
| **É1** | L'amendement de `65` (§12) affirme : *« Tant que ce lot runtime n'est pas livré, le runtime demeure en écart connu et documenté »*. **Or le runtime est conforme** : `10_scripts/chauffage/decision_centrale.yaml` porte la garde `and is_state('sensor.chauffage_autorisation_cible', 'comfort')` sur **les deux axes** `desired_mode` et `reason`, en égalité positive sans valeur par défaut — conformément à INV-PCV-1, INV-PCV-2 et INV-PCV-6. Livré par PR #696 (`0fa1c217`, 2026-08-22 16:02:38) et **présent dans la version déployée** de la sauvegarde. **C'est le document d'autorité qui est périmé, pas le code.** | **Écart documentaire actif** — PROUVÉ |
| **É2** | `climatisation/15` §9 déclare le point d'extension C21 ; le runtime n'en implémente que la partie C20. **Écart déclaré et assumé** (INV-VETO-9, C21 parqué au registre) — conformité par construction | Conforme (dette déclarée) |
| **É3** | `binary_sensor.aeration_conseillee` n'est consommé par aucune couche du domaine climatisation, alors que son contrat prévoit cet usage inhibiteur possible. Le 22/08, une aération thermiquement défavorable a coûté 1 h 32 de refroidissement et +0,5 °C **sans aucune trace décisionnelle ni signalement** | **Comportement fonctionnel non documenté — à signaler** |
| **É4** | `input_number.duree_prechauffage_retour_vacances` est borné `max: 24`. `65` §5bis n'énonce **aucune borne supérieure** et prescrit un délai physique calculé. Borne d'implémentation non adossée à une règle contractuelle | **À signaler** (mineur) — PROUVÉ |
| **É5** | `sensor.clim_ventilation_diagnostic` produit **405 à 471 transitions par jour** dès que la climatisation fonctionne (2 par jour le reste du temps), pour un cumul de **1,0 h en état `ecart` contre 99,2 h en `conforme`** sur le mois couvert. Le contrat `14` ne décrit pas ce régime d'oscillation `conforme ↔ ecart` de quelques secondes. Sans conséquence décisionnelle établie | **À signaler** (mineur, hors périmètre — appelle une vérification propre) — PROUVÉ |

**Conformité vérifiée par ailleurs, sans écart constaté :** domaine Vacances (cinq niveaux respectés, `now()` absent des templates, boot-proof, effectivité correctement séparée de la demande) · veto composite C20 (INV-VETO-1, 2, 6 et 7 tenus ; `clim_duree_absence_longue = 14,0` sans clé `initial`, conforme à INV-VETO-3 et INV-VETO-4) · Modèle B de ventilation (recommandation non pilotante, résolution unique, arbitrage absence → Fort correctement localisé dans `application_mode.yaml` et non dans la recommandation) · VMC (aucune entrée thermique décisionnelle).

---

## J. Limites des preuves — ce qu'Arsenal n'enregistre pas

Les entités suivantes sont **hors allowlist `recorder.yaml`**. Leur état pendant l'épisode est **NON DÉTERMINABLE**. Elles sont recensées ici comme limite de l'expertise, non comme demande de modification.

**Bloquant pour l'analyse a posteriori**

1. `input_boolean.pre_confort_actif_calcule` et `sensor.pre_confort_raison` — le déclenchement du pré-confort du 22/08 n'est établi que **par corrélation** (`chauffage_dernier_mode_decide` à 06:30:09 face à `pre_confort_debut_calcule` = 06:30:00). Le mécanisme central de l'anticipation n'a **aucune trace propre**.
2. `sensor.chauffage_autorisation_cible` — impossible d'établir si la garde thermique, si elle avait été déployée, aurait effectivement bloqué le passage en Confort du 22/08.
3. `input_datetime.fin_vacances`, `input_datetime.debut_vacances`, `input_boolean.vacances_fenetre_active`, `binary_sensor.vacances_demandees`, `binary_sensor.vacances_planifiees_actives` — la date de retour connue d'Arsenal n'est reconstituable que via `core.restore_state`, donc **uniquement à l'instant de la sauvegarde**. Un changement de `fin_vacances` en cours de séjour serait **invisible**.
4. `sensor.seuil_extinction_clim_applique` — la référence de tout le calcul d'intensité, donc de toute la ventilation, n'est pas historisée. Les 2,6 °C d'intensité au retour ne sont convertibles en température cible que par déduction (cf. P1).
5. `binary_sensor.besoin_clim_cool` et `binary_sensor.besoin_clim_cool_admissible` — l'existence du besoin pendant le séjour n'est établie qu'**indirectement**, par la garde `cool_besoin` de la cascade `clim_verdict_cool`.

**Bloquant pour évaluer une option adaptative**

6. **Aucun capteur de vitesse de refroidissement.** Le pendant froid du `V_reprise` de `65` §5bis n'existe ni en contrat ni en runtime. Les −0,56 °C/h de ce rapport ont dû être calculés hors ligne. Le chauffage dispose pourtant d'une famille complète d'observabilité thermique historisée (`sensor.amplitude_chute_reprise_presence_chambres`, `sensor.duree_chute_reprise_presence_chambres`, `sensor.temperature_plancher_absence_chambres`, `sensor.duree_stabilisation_absence_chambres`) — **le froid n'a aucun équivalent**.
7. **Aucune représentation, même indirecte, de l'énergie accumulée dans le bâti** (développé ci-dessous).

**Limites de confort d'analyse**

8. `input_select.clim_fan_mode_cible` et `sensor.clim_mode_de_ventilation_local` — le régime auto/manuel de la ventilation et le `fan_mode` réel ne sont pas historisés. La valeur « Fort » est **FORTEMENT INFÉRÉE** (recommandation `Fort` + diagnostic `conforme` + `clim_fan_mode_cible = « Auto Arsenal »` dans `core.restore_state`), non directement prouvée.
9. `binary_sensor.aeration_conseillee` et `binary_sensor.aeration_preferable_*` — impossible d'établir si Arsenal jugeait l'aération du 22/08 16:00 défavorable.
10. `sensor.clim_consommation_estimee_aujourd_hui` relève **0,0** les 22 et 23/08 alors que la climatisation a fonctionné environ 7 h chaque jour. **Capteur apparemment non fonctionnel**, à vérifier séparément. Toute évaluation chiffrée du surcoût énergétique d'un pré-refroidissement en est privée.

### J.1 Le piège conceptuel — Arsenal ne modélise pas l'énergie du bâti

Vérification explicitement demandée à l'audit ; réponse : **Arsenal ne dispose d'aucune représentation, même indirecte, de l'inertie thermique côté froid.**

Toute la chaîne raisonne sur une **température d'air instantanée** :

- `clim_intensite_besoin_froid` est un écart instantané entre `temperature_max_chambres` et le seuil d'extinction appliqué ;
- les seuils d'allumage et d'extinction sont des températures d'air ;
- l'ordinal `satisfait…extreme` est **mono-axe strict** par contrat (`13` §5.2) : il ne lit ni durée, ni tendance, ni historique.

**Conséquence directe, démontrée par les chiffres de cet audit :** une maison à 26,6 °C après trois semaines de canicule et une maison à 26,6 °C après une seule après-midi chaude présentent **exactement le même état** pour Arsenal. La première a pourtant stocké dans ses murs, dalles et cloisons une énergie qui se restitue à **0,019 °C/h** — environ trente fois plus lentement que la climatisation ne l'extrait. C'est précisément pourquoi 5 h 30 de rattrapage théorique se sont converties en 14 h 42 réelles.

Le contrat `65` §5bis avait anticipé la difficulté en nommant `D_chute` (*« durée chute post-reprise »*) et l'*« inertie post-reprise éventuellement observée »*. **Ce concept n'a jamais été porté côté froid.**

Des grandeurs déjà historisées pourraient en constituer des approximations — `sensor.temperature_moyenne_maison` (agrégat plus inertiel que les chambres seules), l'intégrale temporelle du déficit sur les 24 à 72 h précédentes, l'écart entre `temperature_max_chambres` et `temperature_moyenne_maison`. **Aucune ne suppose de capteur physique supplémentaire.** Ce constat est consigné comme **fait d'observation**, sans que le présent rapport ne propose de mécanisme.

---

## Qualification

| Question | Réponse |
|---|---|
| Le constat terrain est-il confirmé ? | **Oui, intégralement.** Maison encore chaude, chambres trop chaudes, ventilation forte : les trois observations sont vérifiées et chiffrées. |
| Le cadrage initial est-il exact ? | **Non, sur trois points.** Retour le 22/08 et non le 24 ; maison à 26,6 °C et non ~30 °C ; refroidissement déclenché **par** l'arrivée et non avant elle. Rectifié en §A. |
| Y a-t-il défaillance d'un mécanisme ? | **Non.** Chaque composant a fonctionné conformément à son contrat. L'insuffisance provient d'un **mécanisme absent**, pas d'un mécanisme fautif. |
| L'absence de pré-rafraîchissement est-elle une dérive ? | **Non.** Elle est déclarée, bornée et tracée : `15` §9, INV-VETO-9, C21 parqué au registre, #361 F-COOL-4. |
| Le comportement de la ventilation est-il un défaut ? | **Non.** Il est conforme, explicable et physiquement utile. |
| Existe-t-il un écart contrat ↔ implémentation actif ? | **Oui, un seul, documentaire** : É1 — l'amendement de `65` décrit un écart runtime qui n'existe plus. |
| Des comportements non documentés ont-ils été relevés ? | **Oui, deux** : É3 (aération défavorable sans arbitrage ni trace) et É5 (oscillation du diagnostic de ventilation). |

---

## Risques

| # | Risque | Portée |
|---|---|---|
| **R1** | **Récurrence certaine.** Le mécanisme étant absent, tout retour de Vacances en période chaude reproduira le même schéma : besoin vétoé pendant tout le séjour, puis rattrapage engagé après l'arrivée, à ≈ 0,6 °C/h. La sévérité croît avec la température atteinte pendant l'absence. | fonctionnel |
| **R2** | **Mémoire de cycle et retour décalé.** Une fenêtre de préparation consommée puis un retour retardé laisserait la maison sans reprise (I-C21-5). I-C21-6 prévoit le réarmement sur modification **explicite** de `fin_vacances`, mais **pas** sur un retard non déclaré. C'est le risque R1 du chantier C21, **non résolu**. | conception future |
| **R3** | **Ancrage temporel ambigu.** `fin_vacances` est une frontière de **régime**, pas une **heure d'arrivée**. Les deux ont coïncidé à 43 minutes près le 22/08, mais rien ne le garantit. | conception future |
| **R4** | **Aération défavorable non signalée.** Premier contributeur mesuré au retard (1 h 32 et +0,5 °C), sans trace ni avertissement (É3). | fonctionnel |
| **R5** | **Sur-anticipation.** Toute durée fixe longue est soit trop courte au pire moment, soit consommatrice le reste du temps — contraire à la sobriété prescrite par `65` §5bis. | conception future |
| **R6** | **Absence d'observation du refroidissement.** Sans caractérisation de la vitesse, tout horizon retenu resterait une constante arbitraire, reproduisant côté froid la dette que `65` §5ter assume côté chaud depuis l'origine. | conception future |

---

## GO / NO-GO

### GO — pour l'ouverture d'un chantier **documentaire** de réveil et de cadrage de C21

Preuves jugées suffisantes :

- l'absence de pré-rafraîchissement est **prouvée** par trois sources concordantes et indépendantes — runtime, contrat, registre — et déjà consignée par #361 (F-COOL-4) ;
- l'insuffisance est **mesurée et non ressentie** : 92,7 % du séjour en veto sous besoin établi, chambres sous 24,0 °C seulement 14 h 42 après l'arrivée, +0,5 °C repris pendant l'aération ;
- les **deux grandeurs physiques qui manquaient à C21** sont désormais chiffrées : vitesse de refroidissement mécanique ≈ 0,56 °C/h et décroissance passive ≈ 0,019 °C/h (§D.2) ;
- le point d'extension est **déjà déclaré contractuellement** (`15` §9, INV-VETO-9) et les invariants cibles **déjà écrits** (C21 §4) : il s'agit de réveiller un chantier cadré, non d'inventer une architecture ;
- le précédent chauffage du même jour (#695 / #696) fournit une **doctrine transverse directement applicable**, déjà consolidée dans le corpus.

### NO-GO — sur trois points précis

1. **NO-GO sur « J-1 » comme correctif.** Le levier est inopérant seul : sans neutralisation sélective du veto composite, avancer `fin_vacances` ne déclenche rien (§C.1, §G.2). Et une durée fixe longue est **contraire à `65` §5bis**, que le contrat lui-même déclare non substituable durablement.
2. **NO-GO sur toute ouverture runtime immédiate.** C20 n'est pas clôturé — scénario S7 non exercé, trace §4 incomplète — et C21 en dépend formellement au registre. La séquence de gouvernance Arsenal (contrat → checkers → runtime → dashboard → validation terrain → clôture) doit être respectée.
3. **NO-GO sur un chantier qui ne traiterait pas l'inertie.** Sans caractérisation préalable du refroidissement réel (§J.1, R6), tout horizon retenu serait une constante arbitraire de plus.

### Périmètre recommandé pour l'ouverture *(sans préjuger de la solution)*

Ce que le chantier devrait **couvrir**, sans que le présent rapport ne tranche le « comment » :

- **l'observabilité du refroidissement** — caractériser, en perception pure et sans pilotage, la vitesse réellement observée et la profondeur du déficit récent, sur le patron d'observabilité thermique **déjà accepté côté chauffage**. Comble le trou n° 6 de §J et lève R6 ;
- **la préparation COOL elle-même** — telle que déjà cadrée par C21 §2 à §5, avec neutralisation strictement sélective et gardes physiques inconditionnelles ;
- **l'ancrage temporel** — trancher entre `fin_vacances` et une échéance de retour distincte (R3) ;
- **le comportement en cas de retour décalé, avancé ou annulé** (R2) ;
- **l'observabilité diagnostique** — distinguer explicitement « pas de préparation » de « préparation active mais non permise », distinction que la doctrine sait déjà nommer sans l'avoir matérialisée ;
- **l'arbitrage de l'aération pendant une phase de rattrapage** (É3, R4).

Ce que le chantier devrait **exclure** : toute suppression ou assouplissement des gardes physiques du domaine climatisation ; toute anticipation hors contexte Vacances (différée par D15) ; la dette `_reel` et la garde opérateur (lot séparé, D14).

**Trois arbitrages propriétaires sont requis avant toute conception :** le droit de cycle unique de `65` §7 est-il transposable au froid ? L'ancrage doit-il rester `fin_vacances` ? La recommandation d'aération doit-elle devenir opposable, ou seulement signalée, pendant un rattrapage ?

**Hors chantier, à traiter séparément :** É1 (mise à jour de l'amendement de `65` §12, le runtime étant conforme depuis #696) ; É5 ; le capteur de consommation clim apparemment inopérant (§J n° 10) ; l'opportunité d'élargir l'allowlist `recorder.yaml` aux entités des points 1 à 5 de §J, sur le précédent de l'instrumentation probatoire posée pour C20 le 2026-07-19.

---

## Ce que cet audit n'a pas fait

- **Aucun correctif appliqué**, ni pendant l'audit ni à l'occasion de sa consignation.
- Aucun contrat, chantier, plan d'action, changelog, README, index, registre, YAML de runtime, test ou workflow CI modifié.
- Aucun chantier ouvert, réveillé ou réordonnancé ; aucune ligne du registre touchée.
- Aucune architecture cible décidée ; aucune option promue en décision.
- Aucune écriture, aucun appel de service, aucun rechargement et aucun redémarrage sur Home Assistant. L'instance live n'a pas été sollicitée.
- Aucune modification des bases de données ni des sauvegardes : la base Recorder a été lue en mode `read-only` depuis une copie temporaire hors dépôts.
- Aucun commit, aucun push, aucune pull request.

> La décision de conserver, modifier, référencer dans `audits/index.md`, committer ou ouvrir un chantier appartient au propriétaire.

---

*Rapport d'audit terrain — trace documentaire. Portée normative nulle. En cas de divergence avec un contrat, le contrat fait foi.*
