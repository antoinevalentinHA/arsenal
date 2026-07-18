# Audit — Exposition diagnostique du domaine Climatisation

> **Statut.** Rapport d'audit **documentaire, descriptif et non normatif**, en **lecture seule**.
> Il ne crée aucune exigence, n'ouvre aucun chantier, ne recommande aucun correctif.
> Les **contrats** (`00_documentation_arsenal/contrats/climatisation/**`) et la **doctrine UI**
> (`00_documentation_arsenal/ui/**`) restent les **seules autorités opposables** ; en cas de
> divergence, elles font foi. Les identifiants `CLIM-DIAG-*` sont **structurants pour cet audit**
> (traçabilité), non des exigences nouvelles.

---

## 1. Objet, périmètre et limites

**Objet.** Confronter, pour le domaine Climatisation résidentielle, **les besoins diagnostiques
opposables** issus des contrats, **la production réelle** de ces vérités au runtime, et **leur
exposition** sur les dashboards.

**Périmètre.** Uniquement ce qui est **diagnostiqué et restitué dans l'UI**. Il ne s'agit **pas**
d'un audit général du domaine Climatisation et l'audit ne recherche **aucune** amélioration
fonctionnelle.

**Limites.**
- Le runtime est lu comme **source de vérité constatée**, jamais comme cible de modification.
- Aucune transposition automatique des constats des domaines Alarme, ECS ou Chauffage.
- Aucun élargissement vers un audit transversal Chauffage ↔ Climatisation (cf. §12).
- Aucun verdict fondé sur une préférence ; les verdicts se rattachent à un énoncé opposable.

---

## 2. Base auditée et méthode

**Base auditée.** Dépôt `arsenal`, commit **`ba99ae0`**, branche
`claude/audit-climatisation-diagnostique-o4logz` (base de travail de l'audit, 2026-07-18).
Contrats domaine v1.x (README v1.4, sections `01`→`15`), doctrine UI
`00_documentation_arsenal/ui/**`.

**Méthode — quatre portes.**

| Porte | Objet |
|---|---|
| **P‑C** | Constitution du corpus contractuel + extraction des **besoins diagnostiques opposables**. |
| **P‑R** | Constat de la **production réelle** des vérités/diagnostics dans le code chargé (aucune confiance à la seule rétro-documentation). |
| **P‑EXPO** | Constat de l'**exposition réelle** sur les dashboards et cartes, et du rendu (état/libellé/raison/icône/couleur/indisponibilité). |
| **P‑COMP** | **Comparaison finale** contrat ↔ production ↔ exposition, verdicts et natures d'écart. |

Chaque porte a été validée avant la suivante. Le présent rapport est la restitution de P‑COMP.

---

## 3. Corpus contractuel et UI (exhaustif)

**Contrats Climatisation — racine (16).**
`README.md` · `01_finalite.md` · `02_architecture.md` · `03_decision_canonique.md` ·
`04_entrees_metier.md` · `05_decision_candidats.md` · `06_doctrine_blocages.md` ·
`07_arbitrage_politique.md` · `08_execution.md` · `09_securite.md` · `10_observabilite.md` ·
`11_perimetre_exclu.md` · `12_ventilation_intention.md` · `13_intensite_besoin_froid.md` ·
`14_recommandation_ventilation.md` · `15_absence_vacances_veto_cool.md`.

**Contrats — `capteurs/` (intégralité).** `capteurs/README.md` + les couches `besoins/`,
`admissibilite/`, `autorisations/`, `blocages/`, `decision/`, `coherence/`,
`seuils_et_franchissements/` (fichiers `00`/`10`/`20`/`30`/`90` selon la couche).
**Statut évalué document par document** (et non par présomption sur le dossier parent) : ces
documents **ont été lus intégralement** ; ils servent **principalement de description ou de
rétro-documentation** des entités ; les `90_observations.md` sont explicitement **non normatifs** ;
certains (`blocages/00·20·90`) sont **datés** (modèle pré-C20) et **signalés** comme tels (cf. §9).
Les **besoins opposables retenus** sont **ancrés dans les contrats racine `01`→`15` et la doctrine
`06`** ; les documents `capteurs/` n'en sont pas l'autorité lorsqu'ils ne portent pas eux-mêmes de
norme opposable.

**Doctrine UI (intégralité de `00_documentation_arsenal/ui/`).**
`README.md` · `architecture.md` · `architecture_transverse.md` · `navigation.md` ·
`pattern_dashboard.md` · `pattern_dashboard_reglages.md` · `template_header_modele.md` ·
`couleurs/01_principes.md` · `02_palette.md` · `02_1_palette_etiquettes.md` ·
`03_exceptions.md` · `04_typographie.md` · `05_regles.md` ·
`socle_ui/index.md` + `00_synthese.md` + `01_carte_base.md` → `11_header.md`.

Règles de restitution retenues (opposables) : **backend décide / UI observe** (`01_principes`,
`architecture_transverse`) ; **palette** et **R1–R7** (`05_regles`), dont **R6** « le gris
indisponibilité prime » et la distinction **gris neutre `rgba(158,158,158,0.2)`** / **gris
indisponibilité `rgba(158,158,158,0.1)`** ; **Exception 1 (Modes HVAC)** (`03_exceptions`) ;
**taxonomie des types UI** et **règles de transformation** (mapping état→couleur autorisé ;
recalcul métier et reproduction de logique backend interdits — `architecture_transverse`).

---

## 4. Besoins diagnostiques opposables `CLIM-DIAG-01…18`

Catégories : **P** = production diagnostique · **E** = exposition · **R** = restitution.

| ID | Cat. | Besoin (formulé sans extrapolation, aligné sur la catégorie) | Source opposable |
|---|---|---|---|
| **01** | E | Décision canonique (mode cible) **observable par l'UI et le diagnostic** | `03` §Propriétés |
| **02** | P | **Produire** une **raison priorisée** de la décision/non-activation | `10` §États exposés ; `15` §7 |
| **03** | P | **Produire l'état explicatif** de l'**action réelle** en cours | `10` §États exposés |
| **04** | R | **OFF/repos** rendu comme état **normal**, jamais erreur | `01` §États exclusifs ; `12` §7 |
| **05** | R | **Divergence temporaire** observabilité↔réel **≠ bug** | `10` §États exposés |
| **06** | P | Diagnostics **distinguent** absence longue / Vacances / cumulé / absence ordinaire / autorisation normale | `15` §7 |
| **07** | P | **Continuité physique** de l'absence exposée **en attributs** (`debut_absence`,`echeance`,`duree_ecoulee_h`) | `15` §4 |
| **08** | P | Attribut **`cause`** du veto composite (vacances/absence_prolongee/cumulé/aucune) | `15` §6 |
| **09** | P | **Origine de pilotage ventilation** déterministe, exclusive, finie, utilisable par l'UI | `12` §4 |
| **10** | P+R | Au **repos**, pas d'écart + rendu **gris neutre** distinct du gris indispo | `12` §7 |
| **11** | R | UI ventilation **non-tautologique** + explications (override, incompatibilité) | `12` §10 |
| **12** | R | Couleur ventilation : **R6**, jamais indispo en bleu, **pas de couleur de divergence** | `12` §11 |
| **13** | E | Divergence intention/réel **déductible** de {intention, réel, origine} | `12` §12 |
| **14** | P | Recommandation, **double exposition** FR + technique | `14` §Objet/§8 |
| **15** | P | Cascade explicable de la recommandation **observable** | `14` §9 |
| **16** | P | Dégradation **transparente** (abstention vs cause flaggée) | `14` §4 |
| **17** | P | Distinction **0 ≠ `unavailable`** de l'intensité du besoin de froid | `13` §4.2 |
| **18** | P | Voyant `clim_bloquee` agrège les **vérités effectives** (jamais brutes) | `06` §5/§8 |

---

## 5. Matrice finale — contrat ↔ production ↔ exposition

Producteurs runtime (**chemins complets**) et cartes consommatrices :

| ID · Cat. | Producteur réel (fichier) | Exposition (surface · carte) | Verdict |
|---|---|---|---|
| **01** · E | `sensor.clim_target_mode` — `12_template_sensors/climatisation/decision/mode_target.yaml` ; historisé dans `recorder.yaml` (section CLIMATISATION) | **Aucune carte** ne le consomme ; cartes « Décision » alimentées par le réel | **PARTIEL** |
| **02** · P | `sensor.clim_raison_decision` — `12_template_sensors/climatisation/decision/raison.yaml` (cascade complète, incl. vacances/absence_et_vacances) | Principale `carte_clim_decision` (label) ; Diagnostic `clim_decision_synthetique_72` | **CONFORME** |
| **03** · P | `sensor.clim_action_en_cours` — `12_template_sensors/climatisation/decision/action_en_cours.yaml` | `carte_clim_decision` ; Accueil `carte_clim_etat` | **CONFORME** |
| **04** · R | états off/arret/repos (sources ci-dessus + ventilation) | gris neutre (synthèse/synthétique/etat) · vert-cohérent (decision) · « Au repos » (vent.) ; jamais rouge | **CONFORME** |
| **05** · R | `binary_sensor.clim_incoherence_decision_reel` — `12_template_sensors/climatisation/coherence/incoherence_decision.yaml` (gate 60 s) | `carte_clim_decision` : rouge **seulement** persistant ; indispo→gris `0.1` (R6) | **CONFORME** |
| **06** · P | `sensor.clim_raison_decision` — `12_template_sensors/climatisation/decision/raison.yaml` ; `sensor.clim_verdict_cool` — `12_template_sensors/climatisation/decision/verdict_mode.yaml` ; attr `cause` — `12_template_sensors/climatisation/blocages/veto_absence_vacances.yaml` | Distinction atteint l'UI ; jetons `vacances`/`absence_et_vacances` **bruts** (cf. §8) | **CONFORME** |
| **07** · P | attrs de `binary_sensor.clim_extinction_absence_prolongee_autorisee` — `12_template_sensors/climatisation/blocages/absence_longue.yaml` | Non surfacés (Réglages n'expose que le helper de durée) | **CONFORME** |
| **08** · P | attr `cause` — `12_template_sensors/climatisation/blocages/veto_absence_vacances.yaml` | Non surfacé directement (atteint l'UI via `raison`) | **CONFORME** |
| **09** · P | `sensor.clim_origine_ventilation` — `12_template_sensors/climatisation/ventilation/origine.yaml` | Principale `carte_clim_ventilation` (label) | **CONFORME** |
| **10** · P+R | `sensor.clim_ventilation_diagnostic` (verdict `repos` + clé `couleur`) — `12_template_sensors/climatisation/ventilation/diagnostic.yaml` | Diagnostic `carte_clim_ventilation_diagnostic_xl` (fond gris neutre `0.2`) | **CONFORME** |
| **11** · R | `sensor.clim_mode_de_ventilation_local` — `12_template_sensors/climatisation/ventilation/etat.yaml` ; `sensor.clim_origine_ventilation` ; `input_select.clim_fan_mode_cible` | `carte_clim_ventilation` ; Réglages tile « Mode souhaité » | **CONFORME** |
| **12** · R | réel + clé `couleur` backend (`12_template_sensors/climatisation/ventilation/diagnostic.yaml`) | `carte_clim_ventilation` (R6, bleu technique, pas de couleur divergence) ; Diagnostic XL | **CONFORME** |
| **13** · E | intention/réel/origine (produits, sources ci-dessus) | déductible via `carte_clim_ventilation` + Diagnostic XL | **CONFORME** |
| **14** · P | `sensor.clim_fan_mode_recommande` (state FR + attr `mode_technique`) — `12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml` | Recommandation FR exposée (Diagnostic XL) ; `mode_technique` en attribut | **CONFORME** |
| **15** · P | attrs `vitesse_grille`/`cap_actif`/`reco_finale`/`cause_plafonnement`/`ecart_reco_*` — `12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml` ; historisé `recorder.yaml` | Cascade lisible Besoin→Reco→Cible→Réel+Arbitrage (Diagnostic XL) | **CONFORME** |
| **16** · P | `availability` + causes indispo — `12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml` | Diagnostic XL : « Indisponible » + cause | **CONFORME** |
| **17** · P | `sensor.clim_intensite_besoin_froid` — `12_template_sensors/climatisation/ventilation/intensite_besoin_froid.yaml` ; `_niveau` — `12_template_sensors/climatisation/ventilation/intensite_besoin_froid_niveau.yaml` | Diagnostic XL (« Besoin froid : {niveau} ({x} °C) ») | **CONFORME** |
| **18** · P | `binary_sensor.clim_bloquee` — `12_template_sensors/climatisation/blocages/diagnotic.yaml` (agrège vérités temporisées/effectives) | `carte_clim_decision` (nuance orange) | **CONFORME** |

**Cartes (chemins complets).**
- `19_button_card_templates/40_dashboards/climatisation/20_statut_metier/carte_clim_synthese.yaml`
- `19_button_card_templates/40_dashboards/climatisation/20_statut_metier/carte_clim_ventilation.yaml`
- `19_button_card_templates/40_dashboards/climatisation/20_statut_metier/carte_clim_verdict_mode.yaml`
- `19_button_card_templates/40_dashboards/climatisation/20_statut_metier/clim_decision_synthetique_72.yaml`
- `19_button_card_templates/40_dashboards/climatisation/30_diagnostic/carte_clim_decision.yaml`
- `19_button_card_templates/40_dashboards/climatisation/30_diagnostic/carte_clim_ventilation_diagnostic_xl.yaml`
- `19_button_card_templates/40_dashboards/climatisation/40_contraintes/clim_blocages_synthese_xl.yaml`
- `19_button_card_templates/40_dashboards/arsenal/20_etat_systeme/carte_clim_etat.yaml`

---

## 6. Bilan chiffré

| Verdict | Nombre |
|---|---|
| **CONFORME** | **17** |
| **PARTIEL** | **1** (`CLIM-DIAG-01`) |
| **NON CONFORME** | **0** |
| **Runtime manquant** | **0** |

**Typologie des résultats (à ne pas confondre).**
- **Écart de verdict :** `CLIM-DIAG-01` **uniquement**.
- **Imperfection de restitution hors verdict :** jetons `vacances` / `absence_et_vacances`
  rendus bruts (n'affecte **aucun** verdict).
- **Ambiguïtés documentaires :** sans verdict de non-conformité (cf. §9).
- **Dettes de rétro-documentation :** sans incidence sur la production constatée (cf. §9).

---

## 7. Écart de verdict démontré

**`CLIM-DIAG-01` — PARTIEL — exposition de la décision cible.**
`sensor.clim_target_mode` est **produit**
(`12_template_sensors/climatisation/decision/mode_target.yaml`) et **historisé** (`recorder.yaml`,
section CLIMATISATION) ; il **reste inspectable hors dashboard**. En revanche **aucune carte** ne
consomme `clim_target_mode` : les cartes intitulées « Décision » (`carte_clim_decision`,
`clim_decision_synthetique_72`) rendent l'**état réel** (`clim_action_en_cours` /
`clim_mode_local`) accompagné de la **raison**, non la **cible**.

- **Constat borné :** la vérité est **produite et historisée** ; elle demeure **inspectable hors
  dashboard** ; **la question de savoir si cela suffit à l'exigence « observable par l'UI et le
  diagnostic » reste ambiguë** (cf. §9). Le présent rapport **ne présente ni Recorder, ni
  `more-info`, ni les Outils de développement comme satisfaisant de façon certaine une composante
  de l'exigence**.
- **Nature d'écart :** exposition.
- **Conséquence :** la divergence cible/réel reste par ailleurs signalée par
  `clim_incoherence_decision_reel` ; **aucune conséquence fonctionnelle démontrée**.
- **Fondement du verdict :** c'est cette **ambiguïté de lecture** qui justifie le classement
  **PARTIEL** (ni CONFORME certain, ni NON CONFORME).

C'est le **seul** écart de verdict. **`CLIM-DIAG-06` n'est pas un second écart** : l'exigence
auditée y est une **exigence de production**, et elle est **satisfaite** — elle reste **CONFORME**.

---

## 8. Imperfections et observations hors verdict

- **Restitution brute de `vacances` / `absence_et_vacances`** — **imperfection de restitution UI
  démontrée**, **hors verdict** (le verdict `CLIM-DIAG-06` reste CONFORME). Les jetons,
  **correctement produits**, sont rendus **bruts** (token / « Code : … ») sur
  `carte_clim_verdict_mode`, `clim_decision_synthetique_72` et `carte_clim_decision`, faute de
  libellé FR dédié (`absence_prolongee` en dispose, eux non). La **couleur reste correcte**
  (rouge/verdict). **Sans conséquence fonctionnelle. Aucun traitement n'est proposé dans le présent
  rapport.**

- **Indisponibilité absorbée en amont** — `carte_clim_synthese`
  (`19_button_card_templates/40_dashboards/climatisation/20_statut_metier/carte_clim_synthese.yaml`)
  colore et libelle via `sensor.clim_mode_local`
  (`12_template_sensors/climatisation/decision/mode.yaml`). Chaîne réellement codée : lorsque
  `climate.clim` est `unknown`/`unavailable`, le template **replie d'abord sur sa dernière valeur
  locale (`this.state`)**, puis **sur `off` en dernier ressort** si cette valeur est elle-même
  inexploitable — l'entité **n'émet donc jamais `unavailable`**. Conséquence possible sur la carte
  de synthèse : pendant une coupure, elle rend le dernier mode connu (ou « Veille » en gris neutre
  `0.2`), sans chemin gris indisponibilité. **Aucune non-conformité UI n'est conclue** : la carte
  reste **fidèle à sa source**, et l'absorption relève du contrat de résilience amont (cohérent
  avec `10` : divergence temporaire non-bug). Observation.

- **Attributs `ecart_reco_intention` / `ecart_reco_reel`** de `sensor.clim_fan_mode_recommande`
  (`12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml`) — **produits mais non
  consommés** par les cartes. L'UI d'écart ventilation est pilotée par
  `sensor.clim_ventilation_diagnostic` (réel ↔ **cible effective**). Une vérité utile non consommée
  **n'est pas** automatiquement orpheline ni non conforme : **observation hors verdict** (AMB-3
  résolue sans écart).

- **Frontières F‑1 à F‑4** (hors exigence d'exposition dashboard) :
  - **F‑1** notification persistante d'échec —
    `11_automations/climatisation/notification_echec_execution.yaml` (canal notification, pas
    dashboard) ;
  - **F‑2** historisation Recorder — `recorder.yaml` (persistance) ;
  - **F‑3** `binary_sensor.clim_incoherence_decision_reel`
    (`12_template_sensors/climatisation/coherence/incoherence_decision.yaml`) — produit,
    **consommé par le Watchdog** (`11_automations/climatisation/watchdog.yaml`) ; par ailleurs
    **exposé** comme autorité couleur de `carte_clim_decision` ;
  - **F‑4** `sensor.clim_verdict_dry` / `sensor.clim_verdict_heat`
    (`12_template_sensors/climatisation/decision/verdict_mode.yaml`) — produits et **exposés**
    (sections conditionnelles), **sans exigence opposable**.
  Leur exposition éventuelle est **utile, non opposable** ; elle ne pèse sur aucun verdict.

- **Fragilité latente `entity_id` / `unique_id`** — `sensor.clim_mode_de_ventilation_local` est
  défini avec `unique_id: clim_fan_mode_local` **sans** `default_entity_id`
  (`12_template_sensors/climatisation/ventilation/etat.yaml`) ; l'`entity_id` repose sur la
  slugification du `name`. Résout aujourd'hui, fragilité consignée.

---

## 9. Ambiguïtés documentaires (non tranchées)

- **Portée du terme « observable » (`CLIM-DIAG-01`).** « Observable par l'UI et le diagnostic »
  (`03`) peut se lire comme **propriété d'entité** ou comme **exposition sur une surface**.
  `more-info`, Recorder et Outils de développement **ne sont pas présentés ici comme des
  équivalents certains** d'une exposition sur dashboard ; l'ambiguïté de lecture est **conservée**
  et sous-tend le verdict PARTIEL (cf. §7).

- **`AMB-UI-1` — fonds dynamiques sur `socle_decision_72`.** Trois cartes (`carte_clim_decision`,
  `carte_clim_verdict_mode`, `clim_decision_synthetique_72`) appliquent un `background-color`
  dynamique en spécialisant `socle_decision_72`, dont les Interdits (`socle_ui/03_decision.md`)
  le proscrivent **sans exception XL** — alors que `architecture_transverse.md` **autorise** le
  mapping état→couleur et que `socle_ui/07_status.md` ménage cette permission « en contexte
  synthèse XL ». **Aucune règle de priorité explicite** ne tranche ; les couleurs rendues sont
  **canoniques et R6-sûres**. **Ambiguïté documentaire / de sélection de socle — non tranchée
  ici** ; relève d'un arbitrage du propriétaire de la doctrine UI.

- **Dettes de rétro-documentation `capteurs/`.** Écarts **descriptifs** entre `capteurs/**` et le
  runtime, **sans incidence sur la production constatée** : ordre interne de `clim_action_en_cours`
  (`capteurs/decision/10_decision.md`) ; description de `clim_bloquee` (brut vs temporisé) dans
  `capteurs/blocages/10_blocages.md` ; extinction absence décrite **par timer** dans
  `capteurs/blocages/00_overview.md`, `20_chaines.md`, `90_observations.md` alors que le runtime
  (et le contrat `15`) est **horodaté**. Dette documentaire, **sans effet sur les verdicts**.

---

## 10. Surfaces UI cartographiées

| Surface | Fichier (chemin complet) | Rôle diagnostique |
|---|---|---|
| **Principale** | `18_lovelace/dashboards/climatisation/principal.yaml` (`/clim-dashboard`) | Synthèse, ventilation appliquée, décision globale (`carte_clim_decision`), section **Conditions** par mode, historique |
| **Diagnostic** | `18_lovelace/dashboards/climatisation/diagnostic.yaml` (`/diagnostics-climatisation-dashboard`) | Décision synthétique, seuils/besoins, **ventilation diagnostic XL**, **blocages XL** |
| **Réglages** | `18_lovelace/dashboards/climatisation/reglages.yaml` (`/reglages-climatisation-dashboard`) | Bandeau validité, consignes/seuils, **durée absence longue**, **« Mode souhaité »**, mode nuit/blocage dur |
| **Historique** | (intégré dans `18_lovelace/dashboards/climatisation/principal.yaml`) | `history-graph` de `switch.clim_power` |
| **Accueil (transversal)** | `19_button_card_templates/40_dashboards/arsenal/20_etat_systeme/carte_clim_etat.yaml` | Carte PIVOT « État réel » (clim-only), sur `clim_action_en_cours` — **incluse dans le périmètre Climatisation** |

**Helper `input_select.clim_conditions_mode`** — **outil d'observation `display-only`** :
consommé **uniquement** par les `visibility` / `conditional` du dashboard principal pour
sélectionner le mode inspecté ; **aucun producteur runtime ne le lit**. **Ce n'est pas une
autorité décisionnelle.** Cohérent avec l'architecture **mono-vue** (`navigation.md`) : un filtre
intra-vue n'est pas une navigation.

**Helper `input_select.clim_fan_mode_cible`** — intention utilisateur (« Mode souhaité »,
Modèle B), classe **Mode** (pattern Réglages), écrivain utilisateur unique.

---

## 11. Conclusion — maturité globale

L'exposition diagnostique du domaine Climatisation est **mature et robuste** :

- **Aucun manque de production constaté** — **0 runtime manquant** : aucune vérité diagnostique
  requise n'est absente du runtime ; les gardes d'indisponibilité sont présentes (`availability`,
  fail-closed, distinction 0 ≠ `unavailable`). Les exigences d'**exposition** et de **restitution**
  sont évaluées **séparément** (elles ne se déduisent pas de la seule production).
- **Restitution globalement conforme** — **17/18 CONFORME** ; **R6** et la distinction gris neutre
  `0.2` / gris indispo `0.1` respectées sur les surfaces diagnostiques ; le **diagnostic
  ventilation** est exemplaire (couleur décidée backend via clé `couleur`, sans reconstruction).
- **Un seul écart de verdict** — **`CLIM-DIAG-01` (PARTIEL)** : la décision **cible** n'est pas
  surfacée sur carte (écart d'**exposition**, sans conséquence fonctionnelle démontrée ; lecture du
  terme « observable » restant ambiguë).
- **Résidus strictement UI/documentaires** — une **imperfection de restitution visuelle** (jetons
  `vacances`/`absence_et_vacances` bruts, hors verdict), une **ambiguïté documentaire** de
  gouvernance de socle (`AMB-UI-1`), et une **dette de rétro-documentation** `capteurs/`. **Aucune
  conséquence fonctionnelle démontrée.**

En synthèse : **production saine, restitution fidèle, un point d'exposition et un point de
restitution mineurs, une ambiguïté doctrinale à arbitrer.** L'exposition diagnostique satisfait ses
exigences opposables, à l'exception de l'exposition directe de la décision cible (dont la lecture de
l'exigence reste ambiguë et sans impact fonctionnel démontré). **Aucun correctif proposé.**

---

## 12. Limites et objets hors périmètre

- **Cartes de température de l'Accueil Chauffage ↔ Climatisation** — toute carte thermique
  **conjointe** Chauffage + Climatisation est un **objet transversal hors périmètre** ; elle n'est
  **pas auditée** ici et serait seulement **candidate à une session dédiée**. `carte_clim_etat`
  reste clim-only et incluse dans ce rapport.
- **`19_button_card_templates/40_dashboards/imprimerie/carte_climat_zone.yaml`** — domaine
  **distinct** (site Imprimerie), hors périmètre.
- **Rapports Chauffage / ECS / Alarme, registre des chantiers, index, changelog** — non modifiés,
  hors périmètre de ce rapport.
- **Rétro-documentation `capteurs/`** — utilisée pour orientation P‑R ; **non autorité** lorsqu'elle
  ne porte pas de norme opposable.

---

*Rapport d'audit — exposition diagnostique Climatisation. Lecture seule, descriptif et non
normatif. Les contrats et `00_documentation_arsenal/ui` font foi. Aucune exigence créée, aucun
chantier ouvert, aucun correctif recommandé.*
