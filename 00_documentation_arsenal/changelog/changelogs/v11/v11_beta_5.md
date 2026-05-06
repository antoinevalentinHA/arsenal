# Arsenal — Changelog v11 beta 5

---

## Synthèse

Version de **structuration et fiabilisation forte**.

Trois axes majeurs :

1. **Climatisation → passage en exécution robuste avec résilience différée externalisée**
2. **ECS → fiabilisation du gel + signal canonique de fin de cycle**
3. **Recorder/Logbook → bascule en contrats opposables stricts**

Ajout d'un nouveau socle technique : **counters**.

---

## Indicateurs globaux

- Ajouts : +16
- Suppressions : -1
- Modifications : 40
- Impact dominant : scripts climatisation, ECS inertie, contrats recorder/logbook

---

## Nouveau socle — Counters

### Support `counter`

Ajout de `counter: !include_dir_merge_named 09_counters` dans `configuration.yaml`. Le dossier `09_counters` est désormais déclaré comme source de counters HA natifs.

Nouveau compteur introduit :

- `counter.clim_execution_retry_count` (`09_counters/clim_execution_retry_count.yaml`)

Nouveau document : `00_documentation_arsenal/architecture/structure_includes/08_b_counters.md`

---

## Climatisation — Refonte du moteur d'exécution

### `script.clim_execution` — Réécriture complète

Passage d'un script **simple idempotent** à un **exécuteur robuste avec post-condition**.

**Avant :**
Application directe du mode cible dans un `choose` monolithique. Aucune vérification post-exécution. Zéro résilience.

**Après :**
```
EXECUTION PURE
→ qualification (target_valid / entities_available / execution_possible)
→ délégation au sous-script atomique
→ stabilisation (5 s)
→ validation post-condition
→ décision retry externalisée
```

Trois états de sortie formalisés :

- cible invalide → abstention silencieuse
- échec infra (entités indisponibles) → retry différé
- échec post-condition (exécution possible mais état non conforme) → retry différé

Les deux derniers cas sont distincts : l'échec infra signifie qu'il était impossible d'agir ; l'échec post-condition signifie que l'action a été tentée mais n'a pas produit l'effet attendu.

La post-condition `off` est composite : `climate.clim = off` **et** `switch.clim_power = off`.

**Résilience différée :** en cas d'échec, `input_boolean.clim_execution_echec` est levé, `counter.clim_execution_retry_count` est incrémenté, et un timer de reprise est armé — +30 s à la première tentative, +90 s à la deuxième, abandon silencieux au-delà. Sur succès : flag effacé, compteur remis à zéro, timer annulé.

**Nouveaux helpers :**

- `input_boolean.clim_execution_echec` (`05_input_booleans/climatisation/echec_execution.yaml`)
- `timer.clim_retry` (`08_timers/climatisation/retry_execution.yaml`)
- `counter.clim_execution_retry_count` (`09_counters/clim_execution_retry_count.yaml`)

**Nouveaux sous-scripts atomiques :**

- `script.clim_exec_apply_cool` (`10_scripts/climatisation/cool.yaml`)
- `script.clim_exec_apply_dry` (`10_scripts/climatisation/dry.yaml`)
- `script.clim_exec_apply_heat` (`10_scripts/climatisation/heat.yaml`)
- `script.clim_exec_apply_off` (`10_scripts/climatisation/off.yaml`)

### `automation.clim_reprise_apres_echec` — Nouvelle automation

Déclenchée sur `timer.finished` de `timer.clim_retry`. Relance `script.clim_execution` après échec différé.

### Notifications clim — Remplacement

`11_automations/climatisation/notification.yaml` supprimé, remplacé par `notifications.yaml`. Mise en conformité avec les conventions de nommage Arsenal.

### Guard clim — Correction des triggers

**Avant :** trigger sur `presence_famille_unifiee`, `fenetre_ouverte_maison`, `climate.clim`, `switch.clim_power`.

**Après :** suppression de `switch.clim_power` de la liste. Le guard se déclenche sur les événements causaux uniquement et évalue l'état réel au moment de l'exécution. Il devient moins bavard, plus déterministe, mieux aligné avec la causalité réelle.

### `seuil_extinction_heat_atteint` — Correction de la logique d'état

**Avant :** comparaison `temperature_min_chambres >= seuil_extinction_chauffage_clim`.
**Après :** calcul direct `consigne_appliquee_locale - clim_offset_off`, conformément au contrat de seuil.

### Contrat climatisation `02_architecture.md` — Passage en v1.3

- Garantie d'exécution précisée : aucune commande redondante *au sein d'une même exécution*.
- Ajout : le script ne conserve aucune mémoire locale interne ; la mémoire de résilience est externalisée via helpers dédiés, sans altérer la nature idempotente de l'exécution.
- Watchdog précisé comme complémentaire de la couche Exécution : n'intervient qu'en cas de divergence persistante non résolue par les reprises courtes. Non encore déployé en v1.3.

### Chauffage — Représentativité thermique

- `06_input_selects/chauffage/representativite_thermique.yaml` — nouvel input_select
- `11_automations/chauffage/representativite_thermique.yaml` — automation associée

---

## ECS — Fiabilisation du cycle

### `ecs_gel_donnees_fin_de_cycle` — Signal canonique et sécurisation

**Avant :** logique orientée validation thermique, ambiguïté sur le max réel. Rôle implicitement composite.

**Après :** rôle clair en 6 étapes — mise à jour conservatoire, stabilisation, calcul des variables, écriture figée, miroir du résumé, **émission du signal canonique**.

**Changement critique :** ajout d'une étape 6 — `input_boolean.turn_on` sur `input_boolean.ecs_fin_cycle_signal`. Ce signal découple totalement la production des données de leur consommation aval.

**Sécurisation des lectures :** remplacement des casts `| float(0)` directs par un pattern de protection explicite contre `unknown`, `unavailable`, `none` et vide. Suppression des faux zéros silencieux.

**Simplification :** `sensor.ecs_temperature_max_reelle_cycle` retiré de la liste `update_entity` (calculé par ailleurs). Variables déjà typées float réutilisées directement dans `resume_valide`, sans double cast.

### `applique_consigne_post_delai` — Correction ACK

Remplacement de `sensor.boiler_ack_dhw_set_setpoint_result` par `sensor.boiler_ack_dhw_set_setpoint_status` — conformité avec le contrat MQTT boiler bridge. Correction appliquée dans la condition de vérification ACK et dans le message de notification d'échec.

### `sensor.ecs_temperature_max_reelle_cycle` — Refactoring

Refactoring profond. Nouveaux invariants : monotone sur cycle + inertie, reset uniquement sur front `OFF → ON`, conservation stricte hors cycle, utilisation de `this.state` comme mémoire interne, gestion propre du bootstrap HA.

### UI ECS — Correction affichage

`lovelace/includes/cartes/ecs_dernier_cycle.yaml` : affichage de la température max basculé sur `input_number.ecs_temperature_max_reelle_figee` (et non plus `ecs_temperature_max_figee`). Alignement UI / réalité physique.

---

## Éclairage Garage — Changement de modèle

### `script.garage_toggle` — Refactoring en script paramétrique

**Avant :** logique de bascule interne couplée à un `switch.garage` inversé (`turn_off` allumait, `turn_on` éteignait).

**Après :** point d'exécution physique pur. Introduction d'un paramètre `action` ∈ `{on, off, toggle}` (défaut : `toggle`).

Le script n'interprète plus — il exécute :

- `should_run` calculé pour garantir l'idempotence sur `on`/`off`
- choix de l'actionneur physique via table logique : `button.garage_1` (allumage) ou `button.garage_2` (extinction), appelés via `button.press`
- mise à jour de `input_boolean.garage_light_state` conservée post-action

**Nouveaux éléments :**

- `12_template_sensors/eclairage/garage_estimation_etat.yaml` — sensor d'estimation d'état
- `11_automations/eclairage/garage/recalage_nocturne_booleen.yaml` — recalage nocturne du booléen d'état logique
- `00_documentation_arsenal/contrats/eclairage/recalage_nocturne_garage.md` — contrat associé

### `00_documentation_arsenal/contrats/eclairage/garage.md` — Recentrage sur le contrat d'implémentation

Le document abandonne le statut de contrat métier principal pour devenir un contrat d'implémentation subordonné. Invariants renumérotés I1–I6 : périmètre exclusif, séquence obligatoire (Lecture → Décision → Action → Mise à jour), stratégie de choix actionneur, absence de validation post-action, atomicité logique. Interface d'appel formalisée.

---

## Logbook — Bascule en contrat opposable

### `logbook.yaml` — Épuration majeure

Suppressions notables :

- **Chauffage :** `poele_en_fonction`, scripts `chauffage_*`, capteurs `chauffage_raison_calculee`, `chauffage_autorisation_cible`
- **ECS :** automations de cycle internes (`gel_donnees`, `log_debut_cycle`, `gardien_*`, `watchdog_fin_de_cycle`), conservation des seules entités à valeur narrative
- **Sections entières supprimées :** Ventilation/VMC, Éclairage décoratif, Voiture, Météo/Extérieur, `compteur_reveils_*`
- `binary_sensor.coupure_secteur`, `binary_sensor.internet_disponible` — retrait (états continus, non événementiels)
- Scripts d'action retirés : `script.alarme_armer`, `script.reboot_netatmo`, `script.redemarrer_box`, `script.mode_panne_coupure_secteur`

### `00_documentation_arsenal/architecture/logbook.md` — Passage en contrat opposable

**Avant :** document de principes.
**Après :** contrat Arsenal formalisé avec :

- Règle de base opposable en trois conditions cumulatives : nature événementielle, impact fonctionnel observable, unicité explicative
- Typologie autorisée **fermée** — 4 catégories uniquement (décision système, transition d'état stable, événement sécurité/anomalie, action système explicite)
- Règle de fréquence : répétition anormale = signal système, pas motif de log (exception : sécurité/anomalie)
- Responsabilité d'émission : un émetteur désigné par événement, interdiction d'émissions concurrentes
- Structure d'entrée normée (Quoi / Pourquoi / Contexte)
- Règle de formulation : langage métier uniquement, noms d'entités bruts interdits
- **Test Arsenal en 4 points** (Nature / Impact / Densité / Formulation) — un seul échec → exclusion

---

## Recorder — Bascule en contrat opposable

### `recorder.yaml` — Nettoyage

Suppressions notables :

- `binary_sensor.zigbee_pluie_water_leak`
- `input_datetime.clim_mode_last_change`
- Section Aération : `input_number.delta_t_max_decisionnel_aeration`, `input_datetime.aeration_debut`, `ref_temp_*`, `duree_aeration_*`, `binary_sensor.fenetre_*_avec_delai`

### `00_documentation_arsenal/architecture/recorder.md` — Passage en contrat opposable

**Avant :** "on enregistre ce qui est utile dans le temps."
**Après :** double critère obligatoire et cumulatif — **utilité temporelle** + **acceptabilité logbook**.

Nouvelle structure à deux populations :

- **Population A — Obligatoires par contrainte HA :** entités requises par Energy Dashboard, long-term statistics, `history_stats`, `statistics_graph`. Taguées `# OBLIGATOIRE — contrainte HA`. Appartenance strictement limitée aux dépendances réelles et actives — toute extension injustifiée est une dérive contractuelle.
- **Population B — Discrétionnaires Arsenal :** soumises aux deux critères fondamentaux + critère de fréquence indicatif (>3–5 transitions/heure → présomption d'exclusion).

Apports structurants :

- Procédure de classification en 4 étapes formalisée
- Exigence de justification explicite dans la configuration pour toute entité Population B
- Transformation obligatoire des entités bruyantes mais utiles (agrégation, état consolidé, sentinel, marqueur d'événement) — jamais tolérées brutes
- Règle anti-dérive : absence de justification = entité réputée non éligible

---

## Batteries et groupes — Mise à jour matériel garage

### `01_customize/batteries.yaml`

Remplacement de `sensor.alarme_batterie` (Bouton alarme Imprimerie) par :

- `sensor.switchbot_bot_garage_1` — Bouton Garage 1
- `sensor.switchbot_bot_garage_2` — Bouton Garage 2

### `02_groups/batteries.yaml`

- Ajout de `sensor.switchbot_bot_garage_1` et `sensor.switchbot_bot_garage_2`
- Suppression de `sensor.jardin_batterie`

---

## Zigbee2MQTT

`zigbee2mqtt/coordinator_backup.json` — mise à jour : date `2026-03-22`, `frame_counter` incrémenté à `2021081`.

---

## Documentation — Archives

`00_documentation_arsenal/changelog/changelogs/v11/v11_beta_4.md` — ajout du changelog v11 beta 4 dans les archives.

---

## Lecture stratégique

**1. Passage à la résilience active (climatisation)**
L'introduction d'un vrai mécanisme détection d'échec / retry orchestré / post-condition est un changement de maturité majeur. On passe d'un système optimiste à un système résilient.

**2. Découplage fort ECS**
Le signal `ecs_fin_cycle_signal` transforme un pipeline implicite en bus événementiel propre. Les consommateurs aval ne sont plus couplés à la séquence de gel.

**3. Verrouillage du Recorder et du Logbook**
Le passage aux deux contrats opposables rend impossible l'ajout d'entités sans justification explicite. C'est une décision d'architecture long terme.

---

## Points de vigilance

**Retry clim** — le plafond à 2 tentatives est géré par `timer.cancel` sur le troisième échec. Surveiller les états bloqués pouvant générer une boucle zombie si `input_boolean.clim_execution_echec` n'est pas remis à zéro par une voie externe. Les divergences persistantes au-delà de ces 2 reprises resteront non traitées jusqu'au déploiement du Watchdog (prévu, non encore implémenté).

**Fallback à 0 au gel ECS** — assumé et explicite, limité au moment du gel uniquement. Conforme.

**Bootstrap HA** — plusieurs capteurs passent en logique stricte de protection contre `unknown`/`unavailable`. Surveiller les états au premier démarrage après redéploiement.

---

## Conclusion

Version **structurante et verrouillante**.

- robustesse : ✔️
- cohérence : ✔️
- gouvernance : ✔️

v11 beta 5 marque un basculement : **Arsenal devient un système contrôlé, résilient et explicitement gouverné.**
