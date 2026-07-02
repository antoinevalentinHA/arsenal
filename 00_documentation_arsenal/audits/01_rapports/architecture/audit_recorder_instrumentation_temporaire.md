# Audit — Instrumentation temporaire du Recorder (frontière microscope / permanent)

**Périmètre** : fichier `recorder.yaml` (racine du dépôt), **340 entités** historisées, 35 blocs thématiques.
**Base** : HEAD `12deca6` (post-#241) — branche `claude/audit-recorder-entities-o28dqd`.
**Date** : 2026-07-02.
**Nature** : audit statique **en lecture seule**, sous un angle **temporel** inédit — distinguer l'**instrumentation permanente** de l'**instrumentation temporaire de chantier** (« microscope »). Ce document **fige** le constat à date ; il **ne s'auto-applique pas** et ne modifie ni le runtime, ni le contrat, ni `recorder.yaml`.
**Angle** : complémentaire, non redondant, des deux audits existants —
- [`audit_recorder_conformite_contrat.md`](audit_recorder_conformite_contrat.md) : conformité au contrat (allowlist, Population A/B, justification) ;
- [`audit_recorder_delta_population_a_statistiques.md`](audit_recorder_delta_population_a_statistiques.md) : cartographie exhaustive de la Population A.

Ces deux audits établissent que le fichier est **fonctionnellement sain** et que « la mise en conformité consiste à déclarer l'existant, pas à retirer des entités ». Le présent audit **ne rejuge pas la conformité** : il répond à une question orthogonale — *quelle part de l'instrumentation est un microscope temporaire de chantier, et quelle part est de l'observabilité permanente ?*

**Référentiel opposable** : [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md), [`architecture/01_recorder/fiche_decision.md`](../../../architecture/01_recorder/fiche_decision.md).

---

## 1. Question posée et méthode

Le backup Home Assistant a grossi. L'hypothèse de travail : une **extension volontaire du recorder** pendant plusieurs chantiers d'observabilité (arrosage, VPD/ET₀, humidité sol, clim, chauffage auto-ajustement courbe). Certaines entités ont été ajoutées **pour valider un chantier** et n'ont pas nécessairement vocation à rester en instrumentation permanente.

**Méthode (lecture seule)** :
1. Extraction des 340 entités et segmentation en 35 blocs (bannières `# ====`).
2. Pour chaque bloc, **reconstitution de l'intention** à partir de la langue documentaire intégrée (le fichier est fortement commenté) : marqueurs `observation v0`, `chantier`, `phase P3/P4/P5/P6`, `avant tout câblage`, `observer ce que ferait une logique future`, `diagnostic`, `qualifier dans la durée`.
3. Datation indicative par l'historique git (limite ci-dessous).
4. Classement de chaque bloc sur l'**axe temporel** en 5 catégories (§4).

**Limite de datation** : `recorder.yaml` ne compte que **7 commits** en git, tous entre le 2026-07-01 et le 2026-07-02 — le fichier a été (re)structuré massivement le 2026-07-01 (#194, tag des 95 Population A). La datation par bloc via `git log -S` **n'est donc pas fiable** (tout remonte à la réorg). Le signal exploitable est l'**intention documentée dans le fichier** et les titres des derniers commits incrémentaux (#215, #218, #227, #236, #237). C'est le critère retenu, conforme à l'étape « reconstituer l'intention de chaque bloc ».

**Ce que l'audit statique ne peut pas établir** (posé en présomption, jamais en verdict) : la **fréquence d'écriture réelle** d'une entité et son **poids réel** dans la base — cela exige l'observation Recorder runtime et l'inspection de la base SQLite, hors périmètre.

---

## 2. Synthèse

Le périmètre recorder est **maîtrisé et gouverné** : allowlist stricte, checker CI 14/14 conforme, tags Population A/B par bloc, justifications structurées sur les blocs récents. **Aucune dérive au sens du contrat** n'est constatée. La croissance du backup n'est **pas** le symptôme d'un débordement anarchique : c'est le coût **assumé et documenté** de plusieurs chantiers d'observabilité **actifs**.

Constat central sur l'axe temporel :

- **~180 entités** relèvent d'une **instrumentation permanente** (Population A obligatoire + registres métier stables : palmarès, énergie, modes). Rien à faire.
- **~55 entités** réparties sur **11 blocs** sont une **instrumentation temporaire de chantier** (« microscope ») : arrosage observation v0, chauffage auto-ajustement courbe P3→P6, perception clim. Elles sont **légitimes** et **ne doivent pas être retirées tant que le chantier est actif** — or plusieurs le sont *maximalement* (les blocs P4/P5/P6 ont atterri **le 2026-07-02, jour de l'audit**).
- **~30 entités** sont du **diagnostic long** (observabilité de chaîne décisionnelle sur plusieurs semaines).
- **10 entités** (capteurs de bruit maison + imprimerie) sont un **bruit probable** — présomption de fréquence héritée de l'audit conformité (C4), à lever par observation, **pas** par retrait à l'aveugle.
- **~7 entités** de trace/raison sont **indéterminées** (cardinalité à confirmer, C5) — à ne pas toucher sans validation humaine.

**Verdict d'action : aucun retrait ne peut être justifié avec certitude aujourd'hui.** Les blocs temporaires correspondent à des chantiers **en cours** (le dernier a été committé le jour même). Conformément à la contrainte Arsenal — *« La valeur diagnostique prime pendant un chantier actif »* — la seule action mûre est **documentaire** : rendre la frontière temporaire/permanent **opposable** par un marqueur de gouvernance temporelle, sans retirer aucune entité. Cette action est **proposée** en Annexe A (plan de suivi), **non appliquée** par ce document.

> Le vrai déficit n'est pas un excès d'entités, mais l'**absence de condition de sortie documentée** pour le microscope : les blocs disent « observation v0 » / « phase Px » mais ne portent ni **échéance de réévaluation**, ni **condition de retrait**. La frontière existe dans l'intention ; elle n'est pas encore opposable.

---

## 3. Cartographie complète — 35 blocs

Colonnes : **Bloc** · **Domaine** · **Entités / familles** · **Rôle** · **Classe temporelle** · **Justification** · **Action recommandée**.

Classes : `PERMANENT_CONTRACTUEL` · `TEMPORAIRE_CHANTIER` · `DIAGNOSTIC_LONG` · `BRUIT_PROBABLE` · `INDETERMINE`.

### 3.1 Instrumentation permanente

| Bloc | Domaine | Entités / familles | Rôle | Classe | Justification | Action |
|---|---|---|---|---|---|---|
| Températures maison (L17-35) | Thermique | 18 `sensor.temperature_*` | Sources `platform: statistics` + mesures vives | `PERMANENT_CONTRACTUEL` | Population A tag « OBLIGATOIRE — contrainte HA » ; sans historique, fenêtre statistics tronquée | Conserver |
| Palmarès chaud / froid / nuits chaudes (L37-195) | Thermique | 66 `input_number`/`input_text`/`input_datetime` + 2 `sensor` | Registres métier de records (valeur/date/éval) | `PERMANENT_CONTRACTUEL` | Population B justifiée bloc par bloc, cardinalité bornée, ≤ 1/j | Conserver |
| Humidité relative (L199-213) | Hygro | 11 `sensor.humidite_relative_*` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée | Conserver |
| Humidité absolue (L217-231) | Hygro | 11 `sensor.humidite_absolue_*` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée | Conserver |
| CO2 (L235-245) | Air | 6 `sensor.co2_*` | `co2_sejour` source statistics ; autres pièces | `PERMANENT_CONTRACTUEL` | Population A (co2_sejour) + grandeurs physiques lentes | Conserver |
| Pluie / Pression (L255-295) | Météo | 36 : pluvio, cumuls, palmarès pluie, pression | `pluie_total_local` source statistics + registres palmarès | `PERMANENT_CONTRACTUEL` | Population A + registres métier bornés | Conserver |
| Modes maison (L412-414) | Métier | `input_select.mode_maison`, `input_boolean.mode_babysitting` | États globaux à cardinalité finie | `PERMANENT_CONTRACTUEL` | Paradigme éligibilité Pop B | Conserver |
| Alarme (L419) | Sécurité | `alarm_control_panel.alarme_maison` | État consolidé | `PERMANENT_CONTRACTUEL` | Cardinalité finie, événement structurant | Conserver |
| Présence (L424-426) | Métier | 3 `binary_sensor.presence_*` | États présence unifiée/sécurité/confort | `PERMANENT_CONTRACTUEL` | Binaire, structurant | Conserver |
| Aération (L467-472) | Thermique | 6 (2 sources `history_stats` + helpers épisode) | Sources `fenetre_ouverte_*` | `PERMANENT_CONTRACTUEL` | Population A taguée (history_stats) | Conserver |
| Santé plateforme (L481-485) | Système | 4 CPU/mémoire + `uptime_jours` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée ; coût logbook accepté (contrat) | Conserver |
| Stabilité réseau (L493-494) | Système | `internet_disponible`, `coupure_secteur` | Source `history_stats` + panne secteur | `PERMANENT_CONTRACTUEL` | Population A (internet) ; `coupure_secteur` = observabilité panne secteur permanente | Conserver |
| Chauffage (L502-508) | Thermique | 7 : programme + booléens/select régime | Source `history_stats` + états métier | `PERMANENT_CONTRACTUEL` | Population A (programme_chauffage) + états stables | Conserver |
| Chauffage auto-ajustement (L517-519) | Thermique | 3 `sensor.ecart_consigne_instantane*` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée | Conserver |
| ECS socle (L538-543) | ECS | 6 `sensor`/`binary_sensor` ballon/consigne | États métier consolidés | `PERMANENT_CONTRACTUEL` | Grandeurs bornées, décisions finales | Conserver |
| Déshumidificateur (L564) | Confort | `binary_sensor.deshumidificateur_actif` | État binaire | `PERMANENT_CONTRACTUEL` | Binaire stable | Conserver |
| VMC (L569) | Confort | `input_boolean.vmc_haute_vitesse` | État binaire | `PERMANENT_CONTRACTUEL` | Binaire stable | Conserver |
| Withings (L577-580) | Santé | 4 `sensor.withings_*_local` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée | Conserver |
| Sommeil snapshot (L589-604) | Santé | 16 (snapshot nuit + moyennes 7/14/30j + cardio) | Sources statistics + agrégats bornés | `PERMANENT_CONTRACTUEL` | Population A (total/score) + dérivées lentes | Conserver |
| Imprimerie temp/humidité (L622-641) | Pro | 20 `sensor.temperature_*`/`humidite_*` | Sources `platform: statistics` | `PERMANENT_CONTRACTUEL` | Population A taguée | Conserver |
| Automobile (L650-663) | Mobilité | 14 (autonomie/charge/km Audi) | Sources statistics + `input_number` bornés | `PERMANENT_CONTRACTUEL` | Population A (2 input_number) + grandeurs lentes | Conserver |
| Consommation prises (L670-685) | Énergie | 16 `*_energy` / `*_energy_proxy` | LTS `total_increasing` + sources `utility_meter` | `PERMANENT_CONTRACTUEL` | Population A énergie | Conserver |
| Consommation cumulus (L692) | Énergie | 1 modbuslink | LTS `total_increasing` | `PERMANENT_CONTRACTUEL` | Population A énergie | Conserver |

### 3.2 Instrumentation temporaire de chantier (« microscope »)

| Bloc | Domaine | Entités / familles | Rôle | Classe | Justification (langue du fichier) | Action |
|---|---|---|---|---|---|---|
| Arrosage — canal réservoir sol OBSERVATION v0 (L318-332) | Arrosage / humidité sol | 5 `sensor.jardin_*sol*`/`reservoir_sol_etat` + `input_number.arrosage_seuil_humidite_declenchement` | Observer tarissement / fenêtres de fraîcheur (Point 2) — plan_observation_hydrique_v0 | `TEMPORAIRE_CHANTIER` | « OBSERVATION v0 … observation / diagnostic uniquement — aucune recommandation, aucune action » | **Conserver** (chantier v0 actif) ; marquer condition de sortie |
| Arrosage — canal demande climatique OBSERVATION v0 (L335-372) | Arrosage / VPD / ET₀ | `sensor.arrosage_demande_climatique_et0` / `_etat` / `_vpd` | Corréler demande climatique ↔ tarissement sol | `TEMPORAIRE_CHANTIER` | « observation v0 … aucune logique métier ne lit cet historique » ; **VPD sous dérogation fréquence datée 2026-07-01** (#215) | **Conserver** (chantier v0 actif) ; marquer condition de sortie |
| Arrosage — chaîne décisionnelle V1 (L376-387) | Arrosage | `binary_sensor.arrosage_besoin_sol`/`_intention`, `sensor.arrosage_dernier_effectif`, `input_boolean.arrosage_automatique_actif` | Lire la décision V1 (besoin→intention→effectif) au lieu de la reconstruire | `TEMPORAIRE_CHANTIER` | « corréler les décisions et arrosages réels avec le graphe humidité sol déjà historisé » ; helpers de réglage volontairement EXCLUS | **Conserver** ; marquer condition de sortie |
| Arrosage — durée de base appliquée OBSERVATION (L391-408) | Arrosage | `input_number.arrosage_rainbird_station_1_duree_minutes` | Observer la durée réglée dans le temps — prérequis futur chantier « durée variable » C11 | `TEMPORAIRE_CHANTIER` | « instrumentation du futur chantier durée variable (C11, prérequis P1) » (#218) | **Conserver** ; marquer condition de sortie |
| Clim — intensité besoin froid (L451-452) | Climatisation | `sensor.clim_intensite_besoin_froid` / `_niveau` | Caler les bandes et vérifier l'effet nuit (C2) **avant tout câblage** | `TEMPORAIRE_CHANTIER` | « Observationnel : caler les bandes … avant tout câblage » | **Conserver** ; marquer condition de sortie |
| Clim — fan_mode recommandé (L456) | Climatisation | `sensor.clim_fan_mode_recommande` | Observer ce que ferait une logique automatique **future** (besoin→vitesse) | `TEMPORAIRE_CHANTIER` | « Observationnel : observer ce que ferait une logique future » | **Conserver** ; marquer condition de sortie |
| Chauffage courbe — P3 termes de décision (L695-721) | Chauffage | 6 : `input_select`/`input_boolean`/`input_number`/`input_text` (représentativité, gate, pente, parallèle, last_adjustment) | Historiser entrées de garde + résultat appliqué — phase P3 (Persistance), contrat 76 | `TEMPORAIRE_CHANTIER` | « Concrétise la phase P3 … origine : rapport d'écart runtime 16/06/2026 (D-CRIT-1) » | **Conserver** (chantier courbe actif) ; marquer condition de sortie |
| Chauffage courbe — P4 complétude & apprentissage (L724-755) | Chauffage | 5 : `input_datetime`/`input_select`/`input_text`/2 `sensor` | Rendre Q7 répondable a posteriori — phase P4, contrat 76 §4/§8 | `TEMPORAIRE_CHANTIER` | « Concrétise la phase P4 … » ; **committé le 2026-07-02 (#227)** | **Conserver** (chantier committé le jour même) ; marquer condition de sortie |
| Chauffage courbe — P5 dérivation diagnostic (L758-786) | Chauffage | `sensor.chauffage_courbe_derive_pente`/`_parallele`, `counter.…reversions`, `sensor.…persistance` | Répondre Q6/Q8 a posteriori — phase P5, contrat 76 §3 | `TEMPORAIRE_CHANTIER` | « Concrétise la phase P5 … » ; **committé le 2026-07-02 (#236)** | **Conserver** ; marquer condition de sortie |
| Chauffage courbe — P6 effet / fenêtre régime (L789-812) | Chauffage | `sensor.chauffage_courbe_effet_pente`/`_parallele` | Effet par fenêtre régime (Q5) — phase P6, contrat 76 §3 | `TEMPORAIRE_CHANTIER` | « Concrétise la phase P6 … » ; **committé le 2026-07-02 (#237), jour de l'audit** | **Conserver** (chantier maximalement actif) ; marquer condition de sortie |

### 3.3 Diagnostic long terme

| Bloc | Domaine | Entités / familles | Rôle | Classe | Justification | Action |
|---|---|---|---|---|---|---|
| Rain Bird — pont / qualification P2 & P6 (L299-315) | Arrosage | 12 (santé pont, wifi/ble RSSI, batterie, données fraîches) | Qualifier **dans la durée** P2 (batterie/RSSI) et P6 (Wi-Fi) | `DIAGNOSTIC_LONG` | « qualifier dans la durée les pré-requis P2 et P6 » — observation multi-semaines, lecture seule | Conserver ; réévaluer à qualification P2/P6 close |
| Clim — chaîne décisionnelle (L442-447) | Climatisation | `sensor.clim_target_mode`/`_raison_decision`, 3 `binary_sensor.autorisation_*`, `blocage_horaire_reel` | Lire décision/cause/autorisations au lieu de reconstruire | `DIAGNOSTIC_LONG` | « audit historique … lecture seule, faible volume » — observabilité stable | Conserver (cf. C5 pour `raison_decision`) |
| Clim — ventilation diagnostic (L459) | Climatisation | `sensor.clim_ventilation_diagnostic` | Verdict conformité réel/recommandé | `DIAGNOSTIC_LONG` | Observabilité dashboard | Conserver (cf. C5 cardinalité) |
| Chauffage — diagnostic thermique (L523-533) | Chauffage | 10 `sensor.*_presence_chambres`/`_absence_chambres` (cycles, amplitudes, overshoot) | Caractériser la réponse thermique du logement | `DIAGNOSTIC_LONG` | Observation multi-semaines des cycles ; grandeurs dérivées | Conserver ; réévaluable à froid |
| ECS — apprentissage offsets ECS-OFF-1 (L546-559) | ECS | 9 `input_number`/`input_boolean`/`input_text` offsets | Trajectoire des offsets, contexte d'apprentissage | `DIAGNOSTIC_LONG` | « observabilité ECS-OFF-1 … aucun changement runtime » ; 2 `input_text` → cf. C5 | Conserver ; `input_text` cardinalité à confirmer |

### 3.4 Bruit probable

| Bloc | Domaine | Entités / familles | Rôle | Classe | Justification | Action |
|---|---|---|---|---|---|---|
| Bruit maison (L250-251) | Acoustique | `sensor.bruit_chambre_arnaud`, `sensor.bruit_chambre_matthieu` | Niveau sonore vif | `BRUIT_PROBABLE` | Présomption fréquence > 5/h (audit conformité C4) ; **non-source** de statistics → Population B | **Ne pas retirer à l'aveugle** ; observer fréquence, puis dérogation datée **ou** transformer (agrégat fenêtré) |
| Imprimerie bruit (L609-614) | Acoustique / pro | `sensor.bruit_komori`/`bobst`/`media` (brut) + `sensor.regime_acoustique_numerique_*` | Niveau brut + régime stabilisé | `BRUIT_PROBABLE` (brut) | Le brut relève de C4 ; les `regime_acoustique_numerique_*` sont déjà la **dérivée stabilisée** (à conserver) | Observer fréquence du brut ; conserver les dérivées régime |

### 3.5 Indéterminé — ne pas toucher sans validation humaine

| Bloc / entités | Domaine | Rôle | Classe | Justification | Action |
|---|---|---|---|---|---|
| `input_text.ecs_dernier_ajustement`, `input_text.ecs_resume_dernier_cycle_fige` (L558-559) | ECS | Trace lisible / résumé de cycle | `INDETERMINE` | Risque texte semi-libre — cardinalité à confirmer (audit conformité C5) | Confirmer l'énumération avant toute action |
| `input_text.chauffage_last_adjustment` (L721), `input_text.chauffage_courbe_gel_cause` (L751) | Chauffage | Trace décision / cause de gel | `INDETERMINE` | Vocabulaire annoncé « fermé §6 » mais non vérifié statiquement | Confirmer vocabulaire fermé |
| `sensor.clim_raison_decision` (L443), `sensor.rain_bird_pont_diagnostic` (L308), `sensor.clim_ventilation_diagnostic` (L459) | Clim / arrosage | « raison » / « diagnostic » | `INDETERMINE` | Conformes **seulement si** ensemble fini de codes documentés (C5) | Confirmer cardinalité finie |

---

## 4. Décompte par classe temporelle

| Classe | Blocs | Entités (approx.) | Peut-on retirer aujourd'hui ? |
|---|---|---|---|
| `PERMANENT_CONTRACTUEL` | 23 | ~238 | Non — Population A obligatoire ou registres métier stables |
| `TEMPORAIRE_CHANTIER` | 10 | ~35 | **Non — chantiers actifs** (P4/P5/P6 committés le jour de l'audit) |
| `DIAGNOSTIC_LONG` | 5 | ~37 | Non — observation multi-semaines en cours |
| `BRUIT_PROBABLE` | 2 (5 entités brutes) | 5 | Non sans observation runtime (présomption, pas verdict) |
| `INDETERMINE` | — (7 entités transverses) | ~7 | Non — validation humaine requise |

> Les compteurs se recoupent en bordure (une entité de trace d'un bloc chantier peut être aussi `INDETERMINE`). Ils donnent l'ordre de grandeur, pas une partition stricte.

**Nombre d'entités explicitement incluses : 340.**
**Blocs récemment ajoutés (derniers commits incrémentaux) :** #215 (canal demande climatique, 2026-07-01), #218 (durée de base, 2026-07-01), #227 (courbe P4, 2026-07-02), #236 (courbe P5, 2026-07-02), #237 (courbe P6, 2026-07-02).
**Blocs probablement temporaires :** §3.2 (10 blocs). **Blocs devant rester permanents :** §3.1 (23 blocs).
**Zones où le commentaire documentaire est insuffisant :** conditions de sortie absentes sur tous les blocs §3.2 ; blocs `PERMANENT_CONTRACTUEL` de grandeurs physiques sans bloc de justification formel (constat C1 de l'audit conformité, inchangé) ; `BRUIT_PROBABLE` sans dérogation ni décision (C4).

---

## 5. Attention aux domaines récemment travaillés (demande explicite)

- **Arrosage** — 4 blocs (§3.2) : réservoir sol, demande climatique, chaîne décisionnelle V1, durée de base. Tous `TEMPORAIRE_CHANTIER`, tous annotés « observation / diagnostic uniquement, aucune action, aucune lecture par la logique métier ». Périmètre **maîtrisé** (helpers de réglage explicitement exclus). Rien à retirer : observation v0 en cours.
- **Humidité sol** — bloc réservoir sol (5 sensors + 1 seuil). `TEMPORAIRE_CHANTIER`. `jardin_humidite_sol_*` confirmés Population B légitime par le delta (aucun consommateur statistics). Volume faible.
- **VPD / ET₀** — bloc demande climatique. `sensor.arrosage_demande_climatique_vpd` porte une **dérogation fréquence en règle** (format contractuel, datée 2026-07-01). C'est précisément une entité « courante » (> 5/h) dont l'historisation n'a de valeur que pendant le chantier v0 → candidate **prioritaire** à réévaluation à la clôture v0.
- **Climat / climatisation** — chaîne décisionnelle (`DIAGNOSTIC_LONG`, stable) vs perception besoin froid + fan_mode recommandé (`TEMPORAIRE_CHANTIER`, « avant câblage » / « logique future »). Frontière nette dans l'intention.
- **Chauffage** — le plus gros microscope actif : courbe auto-ajustement P3→P6 (17 entités sur 4 blocs), dont **3 blocs committés le 2026-07-02**. Chantier de fond (contrat 76, incident D-CRIT-1) — instrumentation légitime et récente. **Aucun retrait envisageable.**
- **Bluetti / panne secteur** — pas de bloc « Bluetti » dédié dans `recorder.yaml`. Le seul point rattaché est `binary_sensor.coupure_secteur` (bloc Stabilité réseau), classé `PERMANENT_CONTRACTUEL` (observabilité panne secteur permanente, binaire, faible volume). **Aucune instrumentation Bluetti bavarde détectée** au recorder — la croissance backup ne vient pas de là.

---

## 6. Contrôles exécutés et résultats

| Contrôle | Commande | Résultat |
|---|---|---|
| Contrat recorder (CI) | `python3 scripts/arsenal_contracts/check_recorder_contracts.py` | **14/14 conforme** (`exit=0`). Warnings transitoires connus : T10 (1 énergie), T11 (1 bloc P3 sans justif. structurée complète), T14 (blocs hors bannière A/B). Aucun bloqueur. |
| Décompte entités | script Python (regex du checker) | **340** entités, 10 domaines, 35 blocs |
| Datation blocs | `git log -S … -- recorder.yaml` | Fichier = 7 commits (2026-07-01→02) ; datation par bloc non fiable (réorg #194) → intention documentaire retenue |
| Résidu | non applicable | Aucun retrait proposé → pas de recherche résiduelle d'entités retirées à mener |
| Diff | `git diff --check` | `recorder.yaml` **non modifié** par cet audit (livrable documentaire uniquement) |

---

## 7. Risques résiduels

1. **Fréquence réelle non mesurée** — `BRUIT_PROBABLE` (5 capteurs) et VPD (dérogation) reposent sur présomption ; le vrai poids base exige l'observation Recorder / inspection SQLite (hors périmètre statique).
2. **Poids réel non attribué** — l'audit n'établit pas *quel* bloc a fait grossir le backup. Hypothèse la plus probable au vu des volumes : le microscope chauffage courbe (17 entités récentes) + les grandeurs physiques haute fréquence Population A (températures/humidités, coût assumé). À confirmer par inspection base.
3. **Conditions de sortie absentes** — sans marqueur de réévaluation, les blocs temporaires risquent de **se sédimenter en permanent par défaut** — exactement le glissement « microscope → instrumentation permanente » que ce chantier veut prévenir.
4. **Cardinalité `INDETERMINE`** — 7 entités de trace/raison non vérifiées statiquement ; risque texte semi-libre (contrat).
5. **Datation git aveugle** — impossible de distinguer par git un bloc « ajouté hier » d'un bloc « stabilisé depuis longtemps » ; l'analyse repose sur l'auto-déclaration documentaire (fiable ici car le fichier est très commenté, mais non indépendante).

---

## 8. Proposition de suite (plan de suivi)

Conformément à la contrainte Arsenal (*diagnostic d'abord ; aucun retrait sans certitude ; la valeur diagnostique prime pendant un chantier actif*), **aucun retrait n'est proposé** et `recorder.yaml` **n'est pas modifié** par cet audit.

Plan ordonné valeur/coût :

1. **S1 — Rendre la frontière opposable (documentaire, coût quasi nul).** Ajouter à chaque bloc `TEMPORAIRE_CHANTIER` (§3.2) un marqueur de **gouvernance temporelle** standardisé : référence chantier + intention (microscope) + **condition de réévaluation** (pas de date de retrait couperet). Patch prêt à l'emploi en **Annexe A** — à appliquer comme étape séparée et délibérée, comme le veut la culture d'audit du dépôt (ces rapports ne s'auto-appliquent pas).
2. **S2 — Mesurer avant de trancher (coût = observation runtime).** Sur `BRUIT_PROBABLE` (5 capteurs) et VPD : relever la fréquence réelle et le poids base. Puis, par entité : dérogation datée **ou** transformation (agrégat fenêtré, sur le modèle `temperature_sejour_mean_10min/30min` et `regime_acoustique_numerique_*`).
3. **S3 — Réévaluation programmée des chantiers.** À la **clôture** de chaque chantier (arrosage observation v0 ; chauffage courbe P3→P6 ; perception clim / câblage C2), rejouer la procédure de classification du contrat sur le bloc : reste-t-il en observabilité permanente, ou le microscope se retire-t-il ? Candidat n°1 au retrait post-chantier : `sensor.arrosage_demande_climatique_vpd` (dérogation fréquence, valeur liée à l'observation v0).
4. **S4 — Confirmer la cardinalité `INDETERMINE`** (7 entités) par lecture des définitions ; documenter l'énumération ou transformer.
5. **S5 — (optionnel) Attribuer le poids base.** Inspecter la base recorder pour attribuer la croissance backup par entité — seul moyen de passer de la présomption au verdict sur « qui pèse ».

---

## Annexe A — Patch de gouvernance temporelle **proposé** (non appliqué)

Marqueur commentaire uniquement, additif, **zéro entité retirée, zéro renommage, zéro changement runtime**. À insérer sous la bannière de chaque bloc `TEMPORAIRE_CHANTIER`, après les commentaires existants. Format proposé (n'utilise **aucun** caractère de bannière `====`/`----` pour ne pas perturber la segmentation du checker, et ne contient ni « Population A/B » ni « DÉROGATION FRÉQUENCE ») :

```yaml
    # ⏳ GOUVERNANCE TEMPORELLE — instrumentation de chantier (microscope)
    # Chantier   : <référence — ex. arrosage observation v0 / chauffage courbe P6 (contrat 76)>
    # Ajouté     : <PR #… , date>
    # Réévaluer  : à la clôture du chantier — rejouer la procédure de classification
    #              (rester en observabilité permanente OU retirer le microscope).
    # Ne pas retirer tant que le chantier est actif (valeur diagnostique prioritaire).
```

Blocs cibles : réservoir sol v0, demande climatique v0, chaîne décisionnelle V1, durée de base, clim intensité besoin froid, clim fan_mode recommandé, chauffage courbe P3, P4, P5, P6.

Message de commit suggéré si ce patch est appliqué (étape séparée) : `Clarify recorder temporary instrumentation`.

---

## 9. Limites

- Établi à HEAD `12deca6` ; **périssable** — toute évolution de `recorder.yaml` invalide les compteurs et les classes.
- Audit **statique** : fréquence réelle, poids base, cardinalité runtime et existence de cards/dashboards UI **non vérifiables** (posés en présomption).
- **Aucune** modification appliquée à `recorder.yaml`, au contrat ou au runtime. Document d'aide à la décision, figé, non auto-applicable.

---

*Fin de l'audit. Lecture seule — le périmètre recorder est sain et gouverné ; la croissance du backup est le coût assumé de chantiers d'observabilité actifs. Aucun retrait justifiable aujourd'hui ; le levier est de rendre la frontière microscope/permanent opposable, sans rien supprimer.*
