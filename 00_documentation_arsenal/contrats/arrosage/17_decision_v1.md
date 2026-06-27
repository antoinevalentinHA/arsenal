# CONTRAT ARSENAL — ARROSAGE
## 17 — Décision d'arrosage V1 (paramétrable, livrable)

**Version contrat :** v1.0
**Statut :** **Normatif — décision V1.** Définit la **fonction de décision**
d'un arrosage automatique **V1** mono-station : ses **entrées**, sa **règle
paramétrable**, ses **invariants de sûreté** et la **délégation** de l'exécution
au script Run supervisé **déjà validé terrain**. **Runtime non livré dans ce
document** : aucun template/helper/automation/script/UI n'est créé ici — leur
matérialisation relève des Lots 2 (helpers) et 3 (runtime).

> **Positionnement.** Ce contrat est la **spécialisation livrable** de l'intention
> ([`05_intention.md`](05_intention.md)) pour la **V1 mono-station** : là où 04/05
> décrivent la perception et la décision **conceptuelles, multi-zones**, ce
> document fixe une **décision concrète et paramétrable** fondée sur
> l'**observation v0 déjà livrée** (canal réservoir sol [`15`](15_canal_reservoir_sol.md),
> suspension pluie) et **exécutée** via le script Run supervisé existant
> ([`11`](11_mode_manuel_supervise.md)). Il **hérite** des régimes
> ([`02`](02_regimes.md)) et de la coexistence ([`03`](03_coexistence_rainbird.md)).

> **Garde-fou de lecture.** **On livre une V1 paramétrable d'abord** ;
> l'observation est un **moyen de calibration** (Lot 4), **jamais** une condition
> suspensive infinie. **Mono-station** (aucune station 2). **Aucune commande Rain
> Bird native nouvelle** : toute action passe par le script Run supervisé. En cas
> de doute, Arsenal **s'abstient** et **laisse le secours Rain Bird opérer** — il
> ne coupe jamais le jardin ([`03`](03_coexistence_rainbird.md) §5).

---

## 1. Objet & arbitrage V1

Décrire la **fonction** qui décide d'un arrosage automatique de la station 1 :
quand Arsenal **doit agir maintenant**, à partir d'observables durables et de
paramètres opérateur, en **déléguant l'exécution** au script supervisé éprouvé.

**Arbitrage V1 (décision opérateur — recadrage chantier).**

- L'objectif est de **livrer une V1 d'arrosage automatique** robuste, sûre et
  **entièrement paramétrable**, puis de l'améliorer avec les données réelles
  (comme chauffage / climatisation).
- La **clôture de la Phase 0** ([`07`](07_phase_0_terrain.md) §5) et la barrière
  P1–P7 ([`10`](10_prerequis_runtime.md)) **ne sont pas** une condition
  suspensive de la V1 : pour le **périmètre V1**, leur lecture suspensive est
  **levée par décision opérateur**. La sûreté est portée par les **invariants
  paramétrés** (§4), les **gardes runtime du script supervisé**
  ([`11`](11_mode_manuel_supervise.md) §6), l'**interrupteur maître** et la
  **fenêtre disjointe** du secours — **pas** par l'attente d'un feu vert terrain.
- La V1 **ne construit pas** le dead-man switch (`rain_delay`) ni les régimes
  sophistiqués : elle **coexiste** avec le **secours minimal Rain Bird laissé
  actif** (`Auto`, [`02`](02_regimes.md) R1), dans une **fenêtre Arsenal
  disjointe**. Le raffinement d'autorité (dead-man, `rain_delay`, R3/R5) est
  **réservé au Lot 5**, **uniquement si** l'observation en prouve le besoin.

> **Convention de nommage.** Les **paramètres et entités V1 non encore créés**
> sont **conceptuels** (`‹…›`) ; leur matérialisation est aux Lots 2/3. Les
> **entités déjà livrées** consommées ou déléguées sont citées telles quelles.

---

## 2. Entrées de la décision V1

| Entrée | Rôle dans la décision | Source (livrée ou `‹conceptuelle›`) |
|---|---|---|
| **Humidité représentative du sol** (médiane) | Mesure du « réservoir » : basse ⇒ besoin | `sensor.jardin_humidite_sol_mediane` ([`15`](15_canal_reservoir_sol.md)) |
| **État du canal réservoir sol** | Qualité de lecture : `indisponible`/`insuffisant` ⇒ prudence | `sensor.jardin_reservoir_sol_etat` ([`15`](15_canal_reservoir_sol.md)) |
| **Suspension pluie** | Pluie observée/prévue ⇒ **inhibe** l'arrosage | `binary_sensor.arrosage_suspension_pluie` |
| **Fenêtre horaire Arsenal** | Arsenal n'agit que dans `‹fenetre_arsenal›`, **disjointe** du secours | `‹fenetre_arsenal›` (helper, Lot 2) |
| **Cooldown / intervalle minimal** | Délai minimal entre deux arrosages Arsenal (anti-acharnement) | `‹cooldown_arrosage›` (helper, Lot 2) |
| **Plafond journalier** | Au plus **un** arrosage Arsenal par jour | `‹plafond_journalier›` (= 1, Lot 2) |
| **Interrupteur maître** | Autorise/coupe globalement l'automatisme Arsenal | `‹interrupteur_maitre_arrosage›` (helper, Lot 2) |
| **Préconditions runtime + santé pont** | Pont **exploitable** pour exécuter/observer | `binary_sensor.arrosage_rain_bird_preconditions_runtime`, `sensor.rain_bird_pont_sante` |
| **Historique d'arrosage** *(fonctionnel)* | « Quand a-t-on **réellement** arrosé pour la dernière fois ? » — applique cooldown + plafond | `‹dernier_arrosage_effectif›` — **matérialisé au Lot 3**, horodaté sur **démarrage prouvé par le switch natif** (jamais ACK seul, [`06`](06_observation_et_preuves.md)) |

> **Historique exprimé fonctionnellement.** La décision **tient compte d'un
> historique d'arrosage** pour éviter les déclenchements trop rapprochés. Ce
> contrat **ne fige pas** `sensor.arrosage_dernier_effectif` : sa création est un
> **sous-produit prouvé de l'exécution** (Lot 3), pas une entrée à inventer ici.

---

## 3. Règle de décision paramétrable

La décision se lit en deux temps — **besoin** puis **intention** — sur le modèle
besoin → décision de 04/05, mais **concret et paramétré**.

**Besoin V1 (`‹besoin_arrosage_v1›`).**

> Besoin actif **si** l'humidité représentative (médiane) est **sous** le seuil
> de déclenchement : `mediane < ‹seuil_humidite_declenchement›`, avec une
> **hystérésis** `‹hysteresis_humidite›` pour éviter le battement autour du seuil
> (le besoin retombe seulement au-dessus de `seuil + hystérésis`).

**Intention V1 (`‹intention_arrosage_v1›`) — `on` SEULEMENT si TOUTES réunies :**

1. **interrupteur maître** actif ;
2. **besoin V1** actif (médiane sous seuil, hystérésis appliquée) ;
3. instant **dans `‹fenetre_arsenal›`**, fenêtre **disjointe** du secours Rain Bird ;
4. **hors suspension pluie** (`binary_sensor.arrosage_suspension_pluie` = `off`) ;
5. **cooldown respecté** et **plafond journalier non atteint** (via l'historique
   `‹dernier_arrosage_effectif›`) ;
6. **préconditions runtime `on`** et **santé pont** suffisante pour exécuter et
   observer ;
7. **aucune inconnue critique** : état réservoir sol `indisponible`/`insuffisant`
   ⇒ **abstention prudente** (jamais conclure « sol humide » par défaut,
   [`04`](04_besoin_hydrique.md) §4).

Si une condition manque, l'intention est **inactive**, et la cause reste
**explicable** (motif dominant, modèle [`aeration_recommandation.md`](../aeration_recommandation.md)).
Tous les seuils/bornes/fenêtres sont des **paramètres** (Lot 2), **non figés
ici**.

---

## 4. Invariants de sûreté (opposables)

1. **Un arrosage Arsenal au plus par jour** (`‹plafond_journalier›` = 1).
2. **Cooldown** : intervalle minimal entre deux arrosages Arsenal respecté.
3. **Interrupteur maître** : un maître `off` **interdit** tout arrosage Arsenal,
   sans condition.
4. **Fenêtre Arsenal disjointe** du calendrier de secours minimal Rain Bird
   ([`03`](03_coexistence_rainbird.md) §3) : au plus **un** décideur légitime par
   instant.
5. **Direction de défaillance** : toute abstention/défaillance Arsenal **rend la
   main au secours** ; la décision V1 **ne neutralise jamais** le secours Rain
   Bird (pas de `mode Off`, pas de `rain_delay` en V1) et **ne bloque jamais à la
   fois** Arsenal **et** le secours ([`03`](03_coexistence_rainbird.md) §5).
6. **Anti-faux-négatif sol** : un capteur sol muet / canal `indisponible` **n'est
   jamais** lu comme « sol humide, pas besoin » ⇒ abstention, pas exécution
   optimiste ([`04`](04_besoin_hydrique.md) §4).
7. **Exécution déléguée uniquement** au script Run supervisé (§5) : la décision
   **n'émet aucune commande native** Rain Bird.
8. **Honnêteté d'historique** : le cooldown/plafond s'appuie sur un arrosage
   **prouvé** (switch natif), **jamais** sur un ACK présumé
   ([`06`](06_observation_et_preuves.md)).

---

## 5. Délégation d'exécution

Quand `‹intention_arrosage_v1›` est `on` (et les invariants §4 respectés),
l'exécution est **déléguée** au script supervisé **déjà validé terrain** :

- **`script.arrosage_rain_bird_station_1_courte_supervisee`** — seule frontière
  vers la commande native ([`11`](11_mode_manuel_supervise.md) §2).
- **Durée** : le réglage opérateur existant
  `input_number.arrosage_rainbird_station_1_duree_minutes` (borné), **réutilisé**,
  pas redéfini.
- Le script **porte ses propres gardes runtime** (préconditions, pont disponible,
  station au repos, preuve de démarrage par le switch natif, Stop supervisé) : la
  décision **ne les duplique pas** mais **s'abstient** si les préconditions sont
  `off` (§3.6).

> **Aucune commande Rain Bird native nouvelle** n'est introduite : la V1 ne fait
> qu'**appeler** un script existant, dans les conditions qu'elle décide.

---

## 6. Calibration par l'observation (renvoi Lot 4)

Les **paramètres** (`‹seuil_humidite_declenchement›`, `‹hysteresis_humidite›`,
`‹fenetre_arsenal›`, `‹cooldown_arrosage›`) sont des **helpers durables** (Lot 2),
**réglés** ensuite par l'observation (Lot 4) : ET₀/VPD
([`16`](16_canal_demande_climatique.md)), tendance, tarissement entrent comme
**modulateurs non destructeurs** (canaux non fondus, désactivables) servant à
**ajuster les helpers**, **jamais** à remettre en cause l'architecture de
décision ni à **retarder** l'automatisation.

---

## 7. Hors périmètre V1

- ❌ **Station 2** (mono-station définitive) ;
- ❌ **dead-man switch / `rain_delay` / régimes R3-R5 sophistiqués** (réservés au
  **Lot 5**, seulement si l'observation en prouve la valeur) ;
- ❌ `mode Off` Rain Bird / neutralisation du secours ;
- ❌ **commande native nouvelle** ; besoin **multi-zone** ;
- ❌ figer `sensor.arrosage_dernier_effectif` (Lot 3) ou tout `entity_id` de
  paramètre V1 (Lot 2) ;
- ❌ tout **cockpit de recette**, checklist Lovelace, entité temporaire de
  qualification ou helper manuel de validation ;
- ❌ tout **runtime / helper / automation / script / UI** **dans ce document**.

---

## 8. Invariants (synthèse)

1. La décision V1 est **livrable et paramétrable** ; l'observation la **calibre**,
   ne la **suspend** pas.
2. **Mono-station** ; **exécution déléguée** au seul script Run supervisé existant.
3. Intention `on` **uniquement** si **toutes** les conditions §3 sont réunies ;
   toute abstention est **explicable**.
4. **Plafond journalier**, **cooldown**, **maître**, **fenêtre disjointe** :
   invariants de sûreté non négociables.
5. **Abstention ⇒ secours** ; la V1 **ne neutralise jamais** le filet de survie et
   **ne bloque jamais tout arrosage**.
6. **Historique prouvé** (switch natif), jamais présumé.
7. **Aucune commande native nouvelle** ; **aucun seuil/`entity_id` V1 figé** ici.

---

## Renvois

- Intention (couche décision, modèle conceptuel) : [`05_intention.md`](05_intention.md)
- Besoin hydrique (perception) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Régimes opérateur (R1 nominal, fenêtres disjointes) : [`02_regimes.md`](02_regimes.md)
- Coexistence / cooldown / direction de défaillance : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Observation & preuves (switch ≠ ACK, historique prouvé) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Mode manuel supervisé (script Run délégué, gardes) : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Canal réservoir sol (médiane / état consommés) : [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)
- Canal demande climatique (calibration future) : [`16_canal_demande_climatique.md`](16_canal_demande_climatique.md)
- Pré-requis runtime (barrière documentaire P1–P7) : [`10_prerequis_runtime.md`](10_prerequis_runtime.md)
- Phase 0 terrain (référence, non suspensive pour la V1) : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Index du domaine : [`README.md`](README.md)
