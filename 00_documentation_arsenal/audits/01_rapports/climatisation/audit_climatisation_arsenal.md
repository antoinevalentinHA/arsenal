# AUDIT ARCHITECTURAL — DOMAINE CLIMATISATION ARSENAL

> Auditeur externe, mandat contradictoire. Runtime = source de vérité.
> Méthode : confrontation systématique contrat ↔ code réel du dépôt cloné
> (`github.com/antoinevalentinHA/arsenal`, branche par défaut).
> Statut contrat affiché : v1.4, « aligné runtime v15.x ».
>
> **Complément dynamique** : les comportements dynamiques absents de cet audit
> statique sont couverts par l'investigation historique (Recorder 30 j) —
> [`investigation_historique_clim_30j.md`](investigation_historique_clim_30j.md).

## Note de périmètre et de méthode

Audit **statique** du code. Home Assistant n'a pas été exécuté : les comportements
dynamiques (courses, latences réelles) sont déduits de la structure, pas observés.

Artefacts effectivement lus et confrontés : les 12 contrats (`00`→`11` +
`capteurs/`), l'intégralité des template/binary sensors clim (décision, cohérence,
blocages, autorisations, besoins, seuils ON/OFF, silence), les 5 scripts
d'exécution, les automatisations (guard, watchdog, trigger, modes, reprise,
silence, notifications, admissibilité ×3, réconciliation boot, maj_consignes ×3,
application consigne HEAT, timer absence), le capteur d'intégrité des paramètres,
les helpers (`input_number`, `input_boolean`), et les cartes dashboard
décisionnelles/diagnostic. Les dépendances transverses consommées par la chaîne
(`fenetre_ouverte_maison_avec_delai`, `aeration_preferable_etage`, présence,
consigne chauffage) ont été localisées mais leur **pipeline interne** n'a pas été
ré-audité (domaines distincts). Non couverts en détail : `energie/cumul_conso`,
`history_stats`, l'ensemble des cartes UI hors décision/blocages.

---

# 1. CARTOGRAPHIE DU DOMAINE

## Perception (entrées métier)

| Catégorie | Entités runtime |
|---|---|
| Température intérieure | `sensor.temperature_max_chambres`, `sensor.temperature_min_chambres` |
| Humidex | `sensor.humidex_max_chambres` + seuil `input_number.seuil_humidex_deshumidification` |
| Température extérieure | `sensor.temperature_jardin` |
| Présence | `binary_sensor.presence_famille_unifiee`, `input_boolean.mode_babysitting` |
| Ouvertures | `binary_sensor.fenetre_ouverte_maison_avec_delai` (chaîne décision), `fenetre_ouverte_maison`/`fenetre_ouverte_etage` (UI brute) |
| Aération | `binary_sensor.aeration_preferable_etage` (capteur composite, domaine aération) |
| Poêle | `binary_sensor.poele_en_fonction_stable` → `input_boolean.blocage_clim_poele` |
| Chauffage principal | `sensor.temperature_consigne_appliquee_locale`, `input_boolean.chauffage_blocage_aeration` |
| Contexte maison | `input_select.mode_maison` |

Seuils dérivés : `sensor.seuil_allumage_clim_applique` / `seuil_extinction_clim_applique`
(COOL, indexés présence), `sensor.seuil_allumage_chauffage_clim` /
`seuil_extinction_chauffage_clim` (HEAT, indexés sur la consigne chauffage ± offsets).

## Décision

```
Seuils franchis (binary_sensor.clim_seuil_*_atteint)
   └─ Besoin brut       binary_sensor.besoin_clim_{cool,dry,heat}        (hystérésis)
        └─ Admissibilité input_boolean.besoin_clim_*_admissible          (verrou 2 portes)
             exposée par binary_sensor.besoin_clim_*_admissible
                └─ DÉCISION sensor.clim_target_mode   ∈ {cool,dry,heat,off}
```

`clim_target_mode` : template pur, priorité **cool > dry > heat > off**
(ThermalPriorityPolicy v1). Conforme aux contrats 03 / 07.

Couche **autorisation** (alimente l'admissibilité, jamais la décision directement) :
`binary_sensor.autorisation_clim_{cool,dry,heat}`.

## Exécution

| Artefact | Rôle |
|---|---|
| `automation.clim_application_automatique` (105) | relais `target_mode` → `script.clim_execution` |
| `script.clim_execution` | tentative unique + stabilisation 15 s + post-condition + retry borné (+30 s / +90 s) |
| `script.clim_exec_apply_{cool,dry,heat,off}` | application physique idempotente (`switch.clim_power` + `climate.clim`) |
| `automation.clim_application_consigne_heat` (107) | consigne HEAT (`input_number.consigne_heat_clim`) |
| `automation.clim_consigne_{presence,absence,correction}` (010/008/009) | consigne COOL |
| `automation.clim_mode_silencieux` (020) | `switch.clim_quiet_fan` |
| `automation.clim_reprise_apres_erreur` (108) | reprise sur `timer.clim_retry` |

## Sécurité (voie orthogonale)

| Artefact | Rôle |
|---|---|
| `automation.clim_guard` (101) | INV-1/2/3 sur la relation `target_mode`/`climate.clim`/`switch.clim_power` → `apply_off` |
| `automation.clim_surveillance_fonctionnement` (106) | watchdog ré-assertion sur `clim_incoherence_decision_reel` |

## Diagnostic / Observabilité

`sensor.clim_raison_decision`, `binary_sensor.clim_bloquee`,
`sensor.clim_action_en_cours`, `binary_sensor.clim_incoherence_decision_reel`,
`binary_sensor.parametres_invalides_climatisation`, `sensor.clim_mode_local`,
`sensor.clim_mode_silencieux_local`.

## UI

`18_lovelace/dashboards/clim.yaml` + templates button-card
`19_button_card_templates/40_dashboards/climatisation/` (statut métier, diagnostic,
contraintes, éligibilité).

## Tests / CI

`contracts_climatisation_admissibilite.yml` **uniquement**. Aucune CI contractuelle
sur décision, raison, blocages, exécution, guard, observabilité.

---

# 2. CARTOGRAPHIE DES DÉPENDANCES — AUTORITÉS

## Autorité RÉELLE de la décision
`sensor.clim_target_mode` ← `besoin_clim_*_admissible` ← automations d'admissibilité
← (`besoin_clim_*` brut) **et** (`autorisation_clim_*`).

## Autorité RÉELLE des blocages (ce qui empêche réellement la clim d'agir)
Portée **exclusivement** par les `autorisation_clim_*`, qui consomment :

- COOL : `temperature_jardin ≥ seuil_ext_min`, `clim_blocage_aeration_etage_reel`,
  `fenetre_ouverte_maison_avec_delai`, `clim_blocage_horaire_reel`,
  `clim_extinction_absence_prolongee_autorisee`.
- DRY : (présence ∨ babysitting), `fenetre_…_avec_delai`,
  `clim_blocage_aeration_etage_reel`, `clim_blocage_horaire_reel`.
- HEAT : `temperature_jardin > seuil_hiver`, `chauffage_clim_active_en_hiver`,
  `chauffage_blocage_aeration`, présence, `fenetre_…_avec_delai`,
  `clim_blocage_horaire_reel`, `blocage_clim_poele`.

## Autorité APPARENTE (ce que l'utilisateur voit)
`clim_raison_decision`, `clim_bloquee`, `clim_blocages_synthese_xl`,
`clim_action_en_cours`.

## Écart fondamental
**Les autorités apparentes ne sont pas des projections fidèles des autorités
réelles.** Elles lisent un sous-ensemble partiel et partiellement obsolète des
signaux de blocage (versions brutes au lieu des `_reel`/`_avec_delai`, omission de
l'aération étage et de l'absence prolongée). Cet écart est la **racine commune**
des dettes D1, D2, D3 ci-dessous. La décision, elle, reste correcte : le défaut est
localisé dans la couche Observabilité/UI, pas dans la chaîne décisionnelle.

---

# 3. DETTES DÉTECTÉES

### D1 — Le capteur de raison masque des causes de décision réelles

**Gravité : Critique**

**Constat.** `sensor.clim_raison_decision` reconstruit la causalité en parallèle de
la décision, à partir d'un jeu de signaux différent de celui qui décide réellement.
Il **ne lit jamais** `binary_sensor.clim_blocage_aeration_etage_reel` ni
`binary_sensor.clim_extinction_absence_prolongee_autorisee`, alors que ces deux
signaux bloquent réellement COOL (et l'aération bloque aussi DRY) via les
autorisations. Conséquence : quand COOL/DRY est bloqué par l'aération étage ou par
l'absence prolongée, `target_mode = off`, et la raison « tombe » sur
`aucune_demande_admissible`.

**Preuves.**
- `12_template_sensors/climatisation/decision/raison.yaml` : la cascade teste
  `blocage_clim_poele`, `chauffage_blocage_aeration`, `clim_blocage_horaire_reel`,
  `fenetre_ouverte_maison`, puis les admissibles. Aucune mention de
  `clim_blocage_aeration_etage_reel` ni de l'absence prolongée.
- `autorisation/cool.yaml` et `autorisation/dry.yaml` : consomment bien
  `clim_blocage_aeration_etage_reel` ; `autorisation/cool.yaml` consomme
  `clim_extinction_absence_prolongee_autorisee`.
- La carte `clim_decision_synthetique_72` traduit `aucune_demande_admissible` par
  « Le système est au repos. **Aucune condition ne justifie une action.** »

**Impact.** L'UI affirme positivement qu'aucune cause n'explique l'inaction, dans
des cas où une cause existe et est connue du système. C'est le cœur des dérives
relevées sur le domaine Chauffage (« blocages mal contextualisés », « causes
invisibles »). Un utilisateur ne peut pas diagnostiquer une clim bloquée par
aération étage ou absence prolongée.

---

### D2 — Le capteur de raison et la décision lisent deux vérités différentes pour les fenêtres

**Gravité : Importante**

**Constat.** La raison lit `binary_sensor.fenetre_ouverte_maison` (brut,
instantané) alors que la décision (via l'autorisation) lit
`fenetre_ouverte_maison_avec_delai`. Pendant la temporisation, les deux divergent.

**Preuves.**
- `decision/raison.yaml` : branche `fenetre_ouverte` testée sur le signal brut,
  **placée avant** les branches `refroidissement`/`deshumidification`.
- `autorisation/cool.yaml` / `dry.yaml` / `heat.yaml` : `fenetre_…_avec_delai`.

**Impact.** Fenêtre tout juste ouverte : `target_mode` peut rester `cool` (délai non
écoulé, admissible encore actif) pendant que la raison affiche déjà
`fenetre_ouverte`. La narration contredit la décision en cours. Symétriquement, le
terme `blocage_aeration` de la raison désigne `chauffage_blocage_aeration`
(post-aération HEAT) et **non** l'aération étage clim → ambiguïté sémantique (voir D6).

---

### D3 — Le voyant `clim_bloquee` et la carte « blocages synthèse » mentent dans les deux sens

**Gravité : Importante**

**Constat.** Les deux artefacts censés exposer les blocages présentent un
sous-ensemble incohérent des vrais blocages.

`binary_sensor.clim_bloquee` agrège : `blocage_clim_poele`,
`chauffage_blocage_aeration`, `clim_blocage_horaire_reel`, `fenetre_ouverte_maison`,
`fenetre_ouverte_etage`.
- **Faux positif :** `fenetre_ouverte_etage` n'intervient **nulle part** dans la
  chaîne de décision → le voyant peut afficher `mdi:lock` pour une fenêtre d'étage
  qui ne bloque rien.
- **Faux négatifs :** n'inclut ni `clim_blocage_aeration_etage_reel`, ni l'absence
  prolongée, ni la température extérieure → affiche `lock-open` alors que la clim est
  réellement bloquée.

`clim_blocages_synthese_xl` (la carte « Blocages ») n'affiche **que** blocage horaire
+ post-aération HEAT. Elle omet aération étage, fenêtres, absence prolongée, poêle,
température extérieure. Quand l'un de ces blocages est actif, elle affiche
littéralement « **Aucun blocage en cours — Le système est pleinement autorisé à
agir.** »

**Preuves.** `blocages/diagnotic.yaml` (voyant), `40_contraintes/clim_blocages_synthese_xl.yaml`
(label JS), à comparer aux 3 fichiers `autorisation/*.yaml`.

**Impact.** L'artefact dont le rôle unique est d'expliquer les blocages affirme
faussement leur absence. Le contrat 06 §5/§8 reconnaît la dette « fenêtres brutes »
comme différée, mais la non-représentation de l'**aération étage** — devenue blocage
gardé en v15.8 et donc nouvelle autorité réelle — n'est pas couverte par cette dette
assumée : c'est une régression d'explicabilité introduite par le chantier v15.8 et
non corrigée côté UI.

---

### D4 — `correction.yaml` agit hors de la chaîne sanctionnée et entre en course avec le Guard

**Gravité : Critique**

**Constat.** `automation.clim_correction_consigne` (id `1003000000009`) **allume le
relais**, **force `climate.clim` en `cool`**, écrit la consigne, attend ~17 s, puis
restaure — le tout sur simple changement du slider `clim_consigne_presence` quand la
clim est OFF. C'est une action physique déclenchée hors des **trois** mécanismes
autorisés par le contrat 02 (transition de `target_mode`, watchdog, guard) et
explicitement exclue par le contrat 11 (« aucune action métier directe hors chaîne
Décision → Arbitrage → Exécution »).

De plus, le Guard se déclenche sur tout changement de `switch.clim_power`. Si
`target_mode == off` (cas attendu quand la clim est éteinte), `correction.yaml`
allume le relais → INV-2 (`power == on` ET `target_mode == off`) est violé → le Guard
appelle `clim_exec_apply_off` et **coupe le relais pendant que `correction.yaml`
tente de le maintenir allumé pour écrire la consigne**.

**Preuves.** `cool/maj_consignes/correction.yaml` (séquence
`switch.turn_on` → `set_hvac_mode cool` → `set_temperature` → restauration) ;
`guard.yaml` (trigger sur `switch.clim_power`, condition INV-2). Contrat 09 §
« Priorité sur la résilience » admet ne garantir « pas l'inhibition automatique »,
donc rien n'empêche la course.

**Impact.** Conflit non documenté entre une automation de confort et la couche
sécurité : écriture de consigne potentiellement avortée, clignotement on/off du
relais, comportement non déterministe. Une couche de sécurité qui sabote une
automation de confort « légitime » est exactement le type de couplage caché que
l'audit doit lever.

---

### D5 — Notification d'échec persistant : contrat non matérialisé

**Gravité : Moyenne**

**Constat.** Le contrat 08 (Résilience) stipule : la ré-émission « s'arrête en cas
d'échec persistant **avec émission d'une notification persistante** ». Aucun
artefact runtime n'émet cette notification.

**Preuves.** Branche par défaut de `script.clim_execution` (échec final) : annule
simplement `timer.clim_retry`, aucune notification. `notifications.yaml` ne traite
que le **mode actif** (heat/cool/dry), pas l'échec. Recherche globale
`persistent_notification` dans le domaine clim : seulement `notifications.yaml` et
`correction.yaml`. À noter que les domaines ECS et Chauffage disposent, eux, de
sous-systèmes `retry_transactionnel` complets — la clim diverge du pattern maison.

**Impact.** Un échec d'exécution persistant (perte Wi-Fi prolongée du module) reste
silencieux. Soit le runtime doit matérialiser la promesse, soit le contrat
sur-promet et doit être corrigé.

---

### D6 — Logique métier dans l'UI + violation de couche

**Gravité : Importante**

**Constat.** Deux violations de la doctrine « les dashboards ne contiennent aucune
logique métier » :

1. `clim_blocages_synthese_xl` **recalcule la plage de blocage horaire en
   JavaScript** (`inRange(hOn, hOff, nowH)` avec `new Date()` côté navigateur), au
   lieu de lire `binary_sensor.clim_blocage_horaire_reel` que le backend expose déjà.
   La vérité affichée dépend alors de l'**horloge et du fuseau du client**, pas du
   serveur HA.
2. `carte_clim_decision` réimplémente en JS un verdict de cohérence raison ↔ action
   (vert/orange/rouge), redondant avec `clim_incoherence_decision_reel`, et adossé à
   `clim_raison_decision` lui-même défaillant (D1/D2).

**Preuves.** Blocs `[[[ ... ]]]` de `clim_blocages_synthese_xl.yaml` et
`carte_clim_decision.yaml`.

**Impact.** Duplication de règles métier hors backend, divergence possible
backend/affichage, coût de maintenance accru, et propagation des erreurs de la
couche raison dans le verdict de cohérence UI.

---

### D7 — `clim_action_en_cours` affiche « bloquée » pendant un refroidissement actif

**Gravité : Moyenne**

**Constat.** `sensor.clim_action_en_cours` renvoie `bloquee` dès que
`blocage_clim_poele == on`, **quel que soit** l'état réel de `climate.clim`. Or le
poêle ne bloque que HEAT. Pendant un COOL actif avec poêle allumé, le survol affiche
« Bloquée » alors que la clim refroidit.

**Preuves.** `decision/action_en_cours.yaml` (test `blocage_clim_poele` en première
branche, avant la lecture de `climate.clim`). Propagation : `carte_clim_decision`
consomme `clim_action_en_cours` comme `entity` (vérifié dans `18_lovelace/dashboards/clim.yaml`,
ligne `entity: sensor.clim_action_en_cours`) → affiche orange « Bloquée » en plein
refroidissement.

**Impact.** Survol trompeur ; un blocage spécifique HEAT est présenté comme un
blocage global.

---

### D8 — Hystérésis COOL : condition d'extinction suspecte (à confirmer avec l'intention)

**Gravité : Importante** *(sous réserve de validation de l'intention initiale)*

**Constat.** Le besoin COOL s'allume sur `temperature_max_chambres ≥ seuil_allumage`
mais s'éteint sur `temperature_min_chambres ≥ seuil_extinction`. L'allumage est
indexé sur le **max**, l'extinction sur le **min**, les deux avec `≥`. Pour un
refroidissement, l'extinction devrait traduire « la température a suffisamment
baissé » (typiquement `temperature_max ≤ seuil_extinction`). Or
`temperature_min ≥ seuil_extinction` est vrai **tant que la pièce la plus froide
reste au-dessus du seuil bas** : l'extinction se déclenche sur de la chaleur
résiduelle, pas sur un refroidissement atteint. Le motif `≥` est correct pour HEAT
(`temperature_min ≥ consigne + offset_off`) mais semble avoir été transposé sur COOL
sans inverser la comparaison.

**Preuves.** `seuils_on_off/cool/seuil_extinction_cool_atteint.yaml`
(`temp_min ≥ seuil_off`), à comparer à `cool/seuil_allumage_cool_atteint.yaml`
(`temp_max ≥ seuil_on`) et `heat/seuil_extinction_heat_atteint.yaml`. Le capteur
d'intégrité `parametres_invalides_climatisation` confirme l'intention d'hystérésis
`déclenchement > extinction` (inv1/inv2), mais ne vérifie pas la cohérence min/max
de la comparaison.

**Impact.** En l'état, COOL ne réalise pas une hystérésis de refroidissement
cohérente : risque d'extinction prématurée et de court-cycle autour du seuil
d'allumage. À confronter à l'intention d'origine ; c'est le type d'erreur historique
silencieuse que l'audit doit signaler.

---

### D9 — Application de la consigne COOL incomplète et asymétrique avec HEAT

**Gravité : Moyenne**

**Constat.** HEAT possède `application_consigne.yaml` qui applique la consigne à
l'**entrée** en mode heat (`to: heat`) et sur changement de slider. COOL n'a aucun
équivalent « à l'entrée en cool » : la consigne n'est poussée qu'au changement de
slider, et seulement si la clim est **déjà** en cool. À l'entrée en COOL via la
décision, aucune consigne n'est appliquée (le script `clim_exec_apply_cool` ne fixe
que `hvac_mode`). Au passage présence→absence, `sensor.consigne_clim_appliquee`
recalcule sa valeur mais **aucune automation ne la réapplique** (les `maj_consignes`
ne se déclenchent que sur le slider).

**Preuves.** `cool/maj_consignes/{presence,absence}.yaml` (trigger = slider,
condition `clim_mode_local == cool`) ; absence de `cool/application_consigne.yaml` ;
`clim_exec_apply_cool` (pas de `set_temperature`).

**Impact.** `sensor.consigne_clim_appliquee`, présenté comme « consigne appliquée »,
peut diverger de la température réelle de `climate.clim`. Le nom sur-promet par
rapport au runtime.

---

### D10 — Duplication humidex DRY + organisation de fichiers trompeuse

**Gravité : Moyenne**

**Constat.** Deux binary_sensors calculent la même chose
(`humidex_max_chambres > seuil_humidex_deshumidification`) :
`binary_sensor.clim_humidex_sup_cible_dry` (nom UI « Demande », dans `dry/on.yaml`)
et `binary_sensor.chambre_max_humidex_au_dessus_seuil` (dans
`dry/seuil_allumage_dry_atteint.yaml`). Seul le second est consommé par le besoin DRY ;
le premier n'est lu que par un dashboard diagnostic → quasi-orphelin. Le fichier
`dry/on.yaml` produit l'entité **non consommée** par la décision, tandis que le seuil
réel est dans `seuil_allumage_dry_atteint.yaml`. Pas de `dry/off.yaml` (asymétrie
avec `cool/` et `heat/`).

**Preuves.** `seuils_on_off/dry/on.yaml`, `…/seuil_allumage_dry_atteint.yaml`,
`…/seuil_extinction_dry_atteint.yaml` ; consommateur réel : `besoin/dry.yaml`.

**Impact.** Duplication, capteur trompeur (un `name: "Demande"` portant un
`unique_id` humidex), navigation du domaine DRY contre-intuitive.

---

### D11 — Dérive sémantique : `chauffage_clim_active_en_hiver`

**Gravité : Moyenne**

**Constat.** L'`entity_id` et les commentaires parlent de « période hivernale », mais
l'automation `modes.yaml` calcule l'autorisation **uniquement** à partir du mode
maison (Normal/babysitting → on ; sinon off). Aucune logique saisonnière ni de
température. Le gating saisonnier réel est ailleurs (`autorisation_clim_heat` :
`temperature_jardin > seuil_hiver`). Le nom UI réel est d'ailleurs juste « Chauffage
activé ».

**Preuves.** `modes.yaml` (calcul `autorisation_cible`) ;
`05_input_booleans/climatisation/modes/chauffage.yaml`.

**Impact.** Terme « hiver » trompeur : conflation entre « autorisation par mode
maison » et « saison ». Coût de compréhension pour toute évolution future.

---

### D12 — Dette de maintenabilité et drift documentaire divers

**Gravité : Faible**

**Constat (cumulatif).**
- IDs d'automation hétérogènes : `1003000000008/009/010/015/020` (13 chiffres) vs
  `10030000000101/105/106/107/108/110/114/115/116` (14 chiffres).
- `clim_offset_off` a `min: -3.0` (autorise une valeur que le capteur d'intégrité
  inv6 marque ensuite comme invalide) ; `clim_offset_on` a `min: 0.1`. Asymétrie +
  piège de réglage.
- `carte_clim_decision` documente en en-tête `entity: sensor.clim_etat_reel` — entité
  **inexistante** dans tout le dépôt (présente uniquement dans ce commentaire) ; le
  dashboard réel passe `clim_action_en_cours`. Drift documentaire.
- Nommage `blocage_clim_poele` / `chauffage_blocage_aeration` hors convention
  `clim_blocage_*_actif` (assumé par le contrat §8.3, donc tracé).

**Impact.** Friction de maintenance, fausses pistes lors d'évolutions ; sans danger
fonctionnel immédiat.

---

### D13 — Couverture CI contractuelle partielle

**Gravité : Moyenne**

**Constat.** Seul `contracts_climatisation_admissibilite.yml` existe. Aucune CI ne
verrouille la décision, la raison, les blocages, l'exécution, le guard ou
l'observabilité de la clim — alors que Chauffage dispose d'une CI domaine complète et
ECS de plusieurs workflows.

**Preuves.** `.github/workflows/` (un seul `contracts_climatisation_*`).

**Impact.** Les artefacts les plus fragiles de ce rapport (raison, voyant, synthèse
blocages) ne sont protégés par aucun test : toute correction peut régresser
silencieusement.

---

## Ce qui est sain (à créditer)

L'audit doit aussi constater ce qui tient. La **chaîne décisionnelle** est solide et
conforme : décision pure et déterministe (`clim_target_mode`), verrou de
requalification à deux portes correctement et symétriquement implémenté sur les 3
modes (front montant besoin / requalification autorisation stable 5 min / extinction
immédiate), réconciliation boot séparée du runtime, exécution idempotente avec
post-condition et retry borné, **Guard v1.4 réellement purgé du métier** (ne lit que
la relation système, sans présence/fenêtres/météo). Les capteurs explicatifs **ne
sont consommés par aucune décision** (diagnostics sans autorité = conforme). La
couche énergie lit `clim_mode_local` (vrai mode), pas `action_en_cours`. Le défaut
majeur est **circonscrit à l'Observabilité/UI**, pas au cœur décisionnel.

---

# 4. ÉVALUATION GLOBALE

**Le domaine est-il cohérent ?** *Partiellement.* La chaîne
Perception → Admissibilité → Décision → Exécution → Sécurité est cohérente et bien
isolée. La couche Observabilité est **structurellement incohérente** avec la
causalité réelle (D1, D2, D3, D7). L'hystérésis COOL (D8) et la course
`correction.yaml`/Guard (D4) introduisent des incohérences fonctionnelles.

**Le domaine est-il gouverné ?** *Majoritairement, avec angles morts.* Contrats
riches et versionnés, autorité d'écriture unique sur `chauffage_clim_active_en_hiver`,
doctrine des blocages explicite avec dette **tracée**. Mais : `correction.yaml`
échappe à la doctrine de déclenchement (D4), les dettes volontaires §8 ne sont pas
résorbées, la CI ne couvre que l'admissibilité (D13).

**Le domaine est-il explicable ?** *Non, pour l'utilisateur final via les
dashboards.* C'est la conclusion la plus nette de l'audit. Plusieurs blocages réels
(aération étage, absence prolongée, fenêtres temporisées, température extérieure)
sont **invisibles** dans tous les artefacts d'observabilité ; deux d'entre eux
(`clim_bloquee`, `clim_blocages_synthese_xl`) peuvent **affirmer faussement** que la
clim est libre d'agir. La réponse à la question contractuelle « un utilisateur
peut-il comprendre pourquoi la clim agit ou n'agit pas ? » est **non** dans tous les
cas impliquant aération étage ou absence prolongée.

**Le domaine est-il maintenable ?** *Moyennement.* Duplications (humidex DRY,
logique horaire en JS), nomenclature hétérogène, dette volontaire, drift documentaire
et CI partielle élèvent le coût des évolutions futures.

**Le domaine est-il conforme à la doctrine Arsenal ?** *Partiellement.* Conforme sur
le cœur (séparation des couches, décision pure, diagnostics sans autorité). Trois
violations ponctuelles : action métier hors chaîne (`correction.yaml`, D4), logique
métier dans l'UI (`clim_blocages_synthese_xl`, D6), et — le plus grave au regard de
la doctrine — des **capteurs exposés à l'utilisateur qui ne représentent pas
fidèlement la causalité réelle** (D1, D2, D3, D7), en violation directe du principe
« les capteurs exposés à l'utilisateur doivent représenter fidèlement la causalité
réelle ».

---

# 5. PLAN D'ACTION (sans correction)

Ordre recommandé, dépendances, risques, bénéfices. Aucun patch ici.

**Chantier 1 — Réalignement de la couche Observabilité sur les autorités réelles**
*(Critique, risque quasi nul)*
Périmètre : `clim_raison_decision`, `clim_bloquee`, `clim_blocages_synthese_xl`,
`clim_action_en_cours`. Objectif : que ces artefacts dérivent des mêmes signaux que
les `autorisation_clim_*` (aération étage, fenêtres temporisées, absence prolongée,
température extérieure, poêle contextualisé HEAT). Risque : purement UI/observabilité,
aucun impact sur la décision. Bénéfice : restaure l'explicabilité — répond
directement à la conclusion « non explicable ». **À traiter en premier.**

**Chantier 2 — Statuer sur `correction.yaml` vs Guard** *(Important, risque matériel)*
Décision d'architecture : soit retirer cette action de confort de la chaîne (le Guard
la sabote), soit la contractualiser comme exception avec inhibition explicite du Guard
pendant la fenêtre d'écriture. Dépend de la confirmation de la course. Risque : touche
au relais physique → tester hors usage réel.

**Chantier 3 — Confirmer l'intention de l'hystérésis COOL** *(Important, risque
thermique)*
Trancher : `temp_min ≥ seuil_extinction` est-il voulu, ou inversion ? Si bug, c'est un
défaut de confort silencieux. Dépend de l'intention opérateur. Risque : modifie le
comportement thermique réel → valider hors canicule. Indépendant des chantiers 1/2.

**Chantier 4 — Aligner contrat 08 et runtime sur la notification d'échec**
*(Moyenne)* Soit matérialiser la notification persistante (en s'inspirant du pattern
`retry_transactionnel` ECS/chauffage), soit corriger le contrat. Décision « contrat
ou runtime fait foi ». Indépendant.

**Chantier 5 — Résorber ou requalifier les dettes §8 et la consigne COOL**
*(Moyenne)* Créer `clim_blocage_fenetres_reel` / `clim_blocage_absence_prolongee_reel`
(ou acter par écrit qu'ils restent bruts) ; compléter l'application consigne COOL
(symétrie HEAT) ou requalifier `consigne_clim_appliquee` en « consigne de référence ».
**Dépend du chantier 1** (mêmes artefacts UI touchés) — à enchaîner après lui.

**Chantier 6 — Nettoyage maintenabilité** *(Faible)* Dédupliquer l'humidex DRY,
homogénéiser les IDs d'automation, clarifier `chauffage_clim_active_en_hiver`,
corriger le commentaire `clim_etat_reel`, borner `clim_offset_off` à > 0.

**Chantier 7 — Étendre la CI contractuelle clim** *(Moyenne, transverse)*
Couvrir décision, raison, blocages, exécution, guard, observabilité.
**À placer après les chantiers 1–5** pour verrouiller les corrections et empêcher
toute régression future. C'est le filet qui rend les corrections précédentes
durables.

**Séquencement résumé.**
`1` (immédiat, sans risque) → `5` (suite directe de 1) ; `2`, `3`, `4` en parallèle
(isolés, chacun avec son risque propre — 2 et 3 sont les plus sensibles, à isoler) ;
`6` opportuniste ; `7` en clôture pour figer l'ensemble.

---

*Fin de l'audit. Le runtime a fait foi : chaque dette ci-dessus est adossée à un
fichier et une ligne de logique réelle, et non aux contrats, dashboards ou
changelogs.*
