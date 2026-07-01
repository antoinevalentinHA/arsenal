# Audit de conformité — `recorder.yaml` vs Contrat Recorder

**Périmètre** : fichier `recorder.yaml` (racine du dépôt), 323 entités historisées.
**Base** : HEAD `8c50118` (post-#191, sections Humidex vides retirées).
**Nature** : audit statique **en lecture seule**. Aucun runtime, aucun `recorder.yaml`, aucun contrat modifié. Ce document **fige** le constat à date ; il ne s'auto-applique pas.
**Référentiel opposable** :
- [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md) — contrat Recorder (source de vérité).
- [`architecture/01_recorder/fiche_decision.md`](../../../architecture/01_recorder/fiche_decision.md) — fiche de décision opérationnelle.

---

## 1. Méthode et limites de portée

L'audit confronte chaque section de `recorder.yaml` aux règles opposables du contrat :
allowlist stricte, deux populations (A obligatoire HA / B discrétionnaire), exigence
de justification, seuil de fréquence (> 5 changements/heure = présomption d'exclusion),
cardinalité finie, rétention ≤ 90 jours, invariant d'indépendance fonctionnelle.

**Ce qu'un audit statique peut établir** : présence/absence des blocs de justification,
classification déclarée, cardinalité *déclarée*, cohérence des dépendances Population A
avec le reste du dépôt YAML, paramètres de rétention.

**Ce qu'il ne peut pas établir** (marqué « à confirmer ») : la **fréquence réelle**
d'écriture d'une entité (nécessite l'observation Recorder runtime), et le fait qu'un
capteur `platform: statistics` ou une carte/helper soit défini **en configuration UI**
plutôt qu'en YAML. Les constats de ces natures sont posés en présomption, pas en verdict.

---

## 2. Synthèse

Le fichier est **fonctionnellement sain** et applique correctement le principe d'allowlist,
la rétention et l'invariant d'indépendance. Les blocs récents (palmarès météo, Rain Bird,
arrosage, chaîne décisionnelle clim, offsets ECS, courbe chauffage) sont **exemplaires** :
ils appliquent au mot près le format de justification du contrat.

Le constat dominant est **documentaire et systémique** : sur 323 entités, **12 blocs de
justification** seulement sont présents. La majorité des entités est incluse **sans la
justification exigée** par le contrat (C1). S'y ajoutent une classification Population A à
consolider (C2, C3), des présomptions de fréquence à lever ou formaliser (C4), et quelques
points de cardinalité à confirmer (C5).

Aucun de ces constats n'introduit de risque runtime ; ils portent sur la **traçabilité**,
que le contrat érige en règle : « Le contrat ne se défend pas par l'intention. Il se défend
par la traçabilité des décisions. »

| # | Constat | Sévérité | Nature |
|---|---|---|---|
| C1 | Déficit de justification Population B (≈ majorité des 323 entités) | **Majeur** | Documentaire |
| C2 | Capteurs d'énergie `state_class: total_increasing` non classés Population A | Modéré | Classification |
| C3 | Le seul tag Population A déclare une dépendance `platform: statistics` non tracée dans le dépôt | Modéré | Traçabilité Pop A |
| C4 | Entités présumées > 5/h sans dérogation documentée (CPU/mémoire, bruit, écart instantané) | Modéré | Fréquence |
| C5 | `input_text` de trace et capteurs « raison/diagnostic » — cardinalité à confirmer | Mineur→Modéré | Cardinalité |
| C6 | Organisation thématique vs séparation par population | Mineur | Structure |
| C7 | Renvois « contrat §… » non résolus dans les commentaires | Mineur | Cohérence hypertexte |

---

## 3. Conformités confirmées

- **Allowlist stricte** — la configuration n'expose qu'un `include.entities` ; tout le reste
  est exclu par défaut. Conforme au § *Principe de filtrage*.
- **Rétention** — `purge_keep_days: 30`, soit **≤ 90 jours** (contrat). Le réglage est même
  plus strict que le plafond ; conforme et sobre.
- **Purge** — `auto_purge: true`. Conforme à l'objectif « lecture utile sur horizon
  opérationnel, pas archivage ».
- **Invariant d'indépendance fonctionnelle** — les blocs annotés répètent « lecture seule /
  observabilité / aucun pilotage » ; aucun signe, dans le périmètre statique, d'une logique
  métier conditionnée à la présence de données Recorder. Conforme (dans la limite du §1).
- **Anti-redondance** — le bloc « Palmarès nuits chaudes » **n'inscrit pas** la source déjà
  historisée au titre du palmarès froid. Bonne application du principe anti-redondance.
- **Format de justification** — là où il est présent, le format contractuel (Rôle / Utilité /
  Logbook / Cardinalité / Fréquence) est respecté fidèlement.

---

## 4. Constats détaillés

### C1 — Déficit de justification Population B *(Majeur, documentaire)*

**Règle** : « Toute entité incluse en Population B doit comporter une justification explicite
dans la configuration » (rôle métier, raison d'inclusion, confirmation de conformité).
« Une entité sans justification est réputée non conforme et doit être réévaluée. »

**Constat** : 323 entités, **12 blocs** `# RECORDER — Population`. Les sections suivantes sont
incluses **sans bloc de justification** :

- 🌡️ Températures maison, 💧 Humidité relative, 💦 Humidité absolue, 🫁 CO2, 🔊 Bruit ;
- 🌧️ Pluie / Pression (les rangs `palmares_pluie_*` n'ont **pas** le bloc que possèdent leurs
  homologues température) ;
- 🎛️ Modes, 🚨 Alarme, 🧍 Présence, 🪟 Aération ;
- 🍓 Santé plateforme, 🔌 Réseau, 🔥 Chauffage, 🔥 Chauffage auto-ajustement,
  🔥 Diagnostic thermique, 🚿 ECS (socle), 💨 Déshumidificateur, 🌬️ VMC ;
- 🛌 Withings, 🛌 Sommeil, 🏭 Imprimerie (bruit + températures/humidité), 🚗 Automobile,
  ⚡ Consommation (prises + cumulus).

**Lecture** : la plupart de ces entités sont des **grandeurs physiques** (température, humidité,
CO₂, pression) qui constituent le paradigme même d'éligibilité Population B — le défaut est
**documentaire, non de fond**. Mais le contrat ne reconnaît pas l'évidence : il exige la trace.
En l'état, la majorité du fichier est formellement « réputée non conforme » faute de justification.

**Résolution recommandée** : doter chaque section d'un **bloc de justification par famille**
(un bloc couvrant un groupe homogène suffit — le contrat n'impose pas un bloc par entité, mais
une justification opposable par inclusion). Priorité aux familles dont la conformité de *fond*
n'est **pas** triviale (santé plateforme, bruit, écart instantané — voir C4).

### C2 — Capteurs d'énergie non classés Population A *(Modéré, classification)*

**Règle** : « Long-term statistics — tout capteur `state_class: measurement / total /
total_increasing` **effectivement utilisé** » relève de **Population A**, à taguer
`# OBLIGATOIRE — contrainte HA`.

**Constat** : 16 entités d'énergie sont listées en sections génériques, sans tag ni justification :
les 11 `sensor.prise_*_energy`, les 3 `*_energy_proxy`, `sensor.clim_consommation_estimee_energie`
et `sensor.petite_maison_modbuslink_1_2_electric_energy_consumption`. Plusieurs sources sont
confirmées `state_class: total_increasing` dans le dépôt (`01_customize/proxys/proxy_energy.yaml`,
`12_template_sensors/system/proxy_energie/*`, `12_template_sensors/climatisation/consommation/cumul.yaml`).
HA compile automatiquement des long-term statistics pour ces capteurs.

**Lecture** : selon leur usage réel, ces capteurs sont **soit Population A** (stats long terme
consommées → alors *mal classés*, tag `OBLIGATOIRE` manquant), **soit Population B** (alors
justification + revue de fréquence dues). Dans les deux cas, la documentation actuelle est
non conforme. La résolution la plus probable est **Population A** (dépendance HA structurelle).

### C3 — Tag Population A à la dépendance non tracée *(Modéré, traçabilité)*

**Constat** : l'unique entité taguée Population A est `sensor.temperature_max_journaliere_jardin`,
justifiée par « source d'un capteur `platform: statistics` ». Or **aucun** `platform: statistics`
du dépôt ne source cette entité : le seul capteur statistics « jardin »
(`13_sensor_platforms/statistics/meteo/temperature_jardin.yaml`) source
`sensor.temperature_jardin` (la mesure vive), pas la journalière. Aucune occurrence de
`temperature_max_journaliere_jardin` comme source statistics n'existe sous `13_sensor_platforms/`.

**Lecture** : la dépendance Population A **n'est pas tracée en YAML**. Deux hypothèses :
(a) le capteur statistics est défini **en config UI** (hors YAML) → dépendance réelle mais non
traçable dans le dépôt ; (b) la dépendance n'existe plus / n'a jamais été câblée → **dérive
Population A** au sens du contrat (« Toute extension injustifiée de la Population A est considérée
comme une dérive contractuelle »). **À confirmer côté UI.** À défaut de confirmation, l'entité
devrait basculer en Population B (grandeur journalière ≤ 1/jour, éligible de plein droit).

> Corollaire : `sensor.temperature_min_journaliere_jardin`, symétrique, est classé Population B et
> n'a lui non plus **aucune** dépendance statistics tracée — ce qui est **cohérent** avec Pop B.
> L'anomalie n'est donc pas une asymétrie min/max mais bien le **tag A du max**, isolé et non tracé.

### C4 — Présomptions de fréquence non levées *(Modéré, fréquence)*

**Règle** : « Une entité qui change plus de **5 fois par heure** est **présumée non éligible** » ;
la présomption ne se lève que par une **dérogation documentée** (`# DÉROGATION FRÉQUENCE`).

**Constat** — entités dont la nature laisse présumer un dépassement, **sans dérogation** :

- `sensor.home_assistant_{supervisor,core}_{cpu,memory}_percent` (×4) — métriques système,
  rafraîchissement typiquement pluri-minute à sub-minute ;
- `sensor.bruit_chambre_arnaud`, `sensor.bruit_chambre_matthieu`, et côté imprimerie
  `sensor.bruit_komori/bobst/media` — niveaux sonores, très volatils par nature ;
- `sensor.ecart_consigne_instantane` / `_froid` / `_doux` (×3) — le qualificatif « instantané »
  suggère un suivi haute fréquence.

**Lecture** : présomption, **non verdict** — la fréquence réelle exige l'observation Recorder
(hors portée statique, §1). Résolution : pour chacune, **soit** formaliser une
`# DÉROGATION FRÉQUENCE` datée si l'inclusion est justifiée, **soit** exclure/transformer
(agrégat, moyenne fenêtrée — cf. `sensor.temperature_sejour_mean_10min/30min` qui, elles, sont
déjà des dérivées lissées, bon modèle à répliquer).

### C5 — Cardinalité à confirmer *(Mineur→Modéré)*

**Règle** : cardinalité finie, énumérable, stable — **texte libre interdit**. Les « raisons
calculées / états verbeux / messages explicatifs » sont explicitement **non éligibles**.

**Constat** :

- `input_text.ecs_dernier_ajustement`, `input_text.ecs_resume_dernier_cycle_fige`,
  `input_text.chauffage_last_adjustment` — décrits comme « trace lisible » / « résumé de cycle ».
  Risque de **texte semi-libre**. (Les `input_text.*_date` de palmarès, eux, sont bornés à des
  dates ISO 8601 et **conformes**.)
- `sensor.clim_raison_decision`, `sensor.rain_bird_pont_diagnostic`,
  `sensor.clim_ventilation_diagnostic` — sémantique « raison / diagnostic ». Conformes **seulement
  si** leurs valeurs forment un ensemble **fini et documenté** de codes ; non conformes si texte
  libre. `sensor.clim_fan_mode_recommande` est *a priori* borné (modes de ventilation) — OK sous
  réserve.

**Lecture** : à confirmer par lecture des définitions (états possibles). Là où la cardinalité est
finie et documentée, ajouter la mention `Cardinalité : finie — [énumération]` suffit à conformer.
Sinon, transformer en état consolidé à cardinalité finie.

### C6 — Organisation thématique vs séparation par population *(Mineur, structure)*

**Règle** : « Les entités Population A font l'objet d'une section `include` dédiée et commentée.
Les entités Population B font l'objet d'une section `include` séparée. »

**Constat** : le fichier est organisé en **29 sections thématiques par domaine**, mêlant Pop A
et Pop B. Une séparation **littérale** en deux blocs `include` est **impossible** sous HA (une
seule clé `include.entities`). L'**intention** de la règle — rendre la Population A **énumérable
d'un coup d'œil** — n'est cependant pas satisfaite : l'unique entité Pop A est noyée dans la
section Température.

**Lecture** : l'organisation thématique est défendable (lisibilité d'usage) et n'est pas à
condamner. Résolution *a minima* : **taguer systématiquement** chaque entité Population A
(cf. C2/C3) et/ou maintenir un **inventaire Population A** en tête de fichier ou en annexe du
contrat, pour préserver l'énumérabilité voulue par la règle.

### C7 — Renvois de contrat non résolus *(Mineur, cohérence hypertexte)*

**Constat** : plusieurs commentaires citent « contrat §11 » (bloc nuits chaudes), « §7/§8 » et
« contrat 76 » (bloc courbe chauffage). Le contrat Recorder (`contrat.md`) n'est **pas** numéroté
en paragraphes ; ces renvois visent vraisemblablement d'autres contrats (chauffage/arrosage) mais
ne sont ni résolus ni hyperliés.

**Lecture** : sans impact fonctionnel ; cohérence documentaire. Résolution : expliciter le contrat
cible (ex. « contrat chauffage 76 ») ou retirer le renvoi ambigu.

---

## 5. Recommandations (non appliquées)

Classées par rapport valeur/coût. **Aucune n'est appliquée par ce document** — elles relèvent
d'un chantier de remédiation à ouvrir si l'auteur le décide.

1. **R1 (C3) — Trancher le tag Population A `temperature_max_journaliere_jardin`.** Vérifier
   l'existence d'un capteur `platform: statistics` en config UI. Confirmé → conserver ; infirmé →
   reclasser en Population B. **Coût quasi nul, valeur de traçabilité élevée.**
2. **R2 (C2) — Consolider la classe des capteurs d'énergie.** Décider Pop A (tag `OBLIGATOIRE`)
   ou Pop B (justification + fréquence), et l'appliquer aux 16 entités. **Coût faible.**
3. **R3 (C4) — Lever les présomptions de fréquence.** Observer la fréquence Recorder des entités
   listées ; formaliser une dérogation datée **ou** transformer/exclure. **Coût = observation.**
4. **R4 (C5) — Confirmer la cardinalité** des `input_text` de trace et des capteurs
   « raison/diagnostic ». Documenter l'énumération, ou transformer.
5. **R5 (C1) — Résorber le déficit de justification** par blocs de famille, en commençant par les
   familles à conformité de fond non triviale (santé plateforme, bruit) plutôt que par les
   grandeurs physiques évidentes. **Coût étalable, à traiter au fil de l'eau.**
6. **R6 (C6/C7) — Hygiène structurelle** : inventaire Population A + résolution des renvois de
   contrat. **Cosmétique, faible priorité.**

> Ordre logique : **R1 → R2** (classification, coût nul et effet de traçabilité immédiat), puis
> **R3 → R4** (points nécessitant une observation ou une lecture de définitions), enfin **R5 → R6**
> (résorption documentaire de fond, étalable).

---

## 6. Limites

- Établi à HEAD `8c50118` ; **périssable** — toute évolution de `recorder.yaml` ou du contrat
  invalide les compteurs.
- Audit **statique** : les constats de fréquence (C4) et l'existence d'un capteur statistics UI
  (C3) ne sont pas vérifiables sans runtime / config UI, et sont posés en présomption.
- **Aucune** modification appliquée à `recorder.yaml`, au contrat ou au runtime. Document
  d'aide à la décision, figé.

---

*Fin de l'audit. Lecture seule — le fichier est fonctionnellement sain ; le levier dominant est
la traçabilité documentaire, pas le retrait d'entités.*
