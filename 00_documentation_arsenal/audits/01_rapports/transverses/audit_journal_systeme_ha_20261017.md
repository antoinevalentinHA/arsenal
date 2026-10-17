# Audit — Journal système Home Assistant (relevé du 2026-10-17)

> **NAVIGATION — NON NORMATIF, NON DÉCISIONNEL.** Rapport d'audit probatoire. N'amende aucun contrat, ne modifie aucun YAML, ne décide rien.
> Index audits : [`../../index.md`](../../index.md) · Registre : [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
> Documents faisant foi pour les constats retenus : [`contrats/aeration_blocage_chauffage/m3_analyse_delta_t/2_calcul_delta_max.md`](../../../contrats/aeration_blocage_chauffage/m3_analyse_delta_t/2_calcul_delta_max.md) · [`05_clotures/voiture/cloture_c25_commande_climatisation_distante.md`](../../05_clotures/voiture/cloture_c25_commande_climatisation_distante.md)

| Champ | Valeur |
|---|---|
| **Nature** | Revue du journal système de l'instance, preuve **L3** (base courante, [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)). Lecture seule. Aucune proposition implémentée. |
| **Date** | 2026-10-17 (dépôt de référence `origin/main` = `adfa4738` ; Home Assistant 2026.10.1). |
| **Sources** | Journal système (`system_log/list`, 23 entrées dédupliquées sur trois jours), historique et registres de l'instance, lus par l'interface web en session opérateur ; YAML et contrats du dépôt. |
| **Version intégrale** | `arsenal-runtime/analyses/journal_systeme_20261017/RAPPORT.md` (hors dépôt gouverné) : relevé brut des 23 entrées, horodatages, chronologies. |
| **Rattachement** | Aucun chantier ouvert ni modifié par ce rapport. Constat A : aucun chantier existant, ouverture à arbitrer. Constat B : **C25** (réserve E6). Cf. §6. |

> **Version publiée, volontairement agrégée.** Ce dépôt est public. Elle ne contient **aucune adresse réseau ou matérielle**, **aucun identifiant de compte**, **aucune localisation** et **aucun horaire** d'ouverture de fenêtre ou d'usage du véhicule. Les relevés horodatés restent dans la version intégrale.

---

## 1. Question et réponse courte

**Question.** Parmi les erreurs et avertissements du journal système, lesquels sont un signal réel et lesquels sont du bruit ?

**Réponse courte.** Sur 23 entrées, **deux défauts Arsenal** et **une indisponibilité externe** :

| # | Constat | Nature | Gravité proposée |
|---|---|---|---|
| **A** | Aération : une sonde indisponible fait **avorter** l'analyse ΔT (M3), au lieu du biais vers la prolongation que le contrat déclare assumé | défaut Arsenal, écart contrat ↔ runtime | P2 |
| **B** | Climatisation distante Audi : intégration éteinte ⇒ `input_select.audi_climatisation_commande_etat` **figé sur « En cours »** | défaut Arsenal, nouveau mode d'échec de C25 | P3 |
| **C** | Audi Connect hors service depuis le 2026-10-14 (authentification refusée côté constructeur) | externe, aucune action locale | — |

Les 20 autres entrées sont du bruit qualifié au §5.

---

## 2. Constat A — Aération : M3 avorte sur sonde indisponible

### 2.1 Fait observé

Le 2026-10-17, `script.aeration_m3_analyse_deltat` a échoué sur sa première action :
`input_number.delta_t_max_decisionnel_aeration` ne peut recevoir 22.0, hors de sa plage 0–10.
L'échec a été journalisé trois fois (automation `aeration_pipeline`, branche M3 du `choose`, script).

### 2.2 Cause établie

1. `sensor.temperature_salle_de_jeux` était indisponible pendant 2 h 24 autour de l'analyse.
2. [`delta_t_piece.yaml`](../../../../12_template_sensors/aeration/delta_t_piece.yaml) remplace une température indisponible par 0 : `deltat_salle_de_jeux = max(ref − 0, 0) = ref`, soit **22.0**, la référence figée par M1. La valeur rejetée est exactement celle-là.
3. [`m3_0_analyse_deltat.yaml`](../../../../10_scripts/aeration/m3_0_analyse_deltat.yaml) publie `delta_max` dans le `input_number` diagnostic **avant** de décider. `input_number.set_value` hors bornes lève une erreur de validation : le script s'arrête avant la mémoire monotone et avant le choix entre `aeration_m3_prolonger_blocage` et `aeration_m3_maintenir_blocage`.
4. Le blocage chauffage a été levé dans la minute suivante, sans prolongation.

### 2.3 Écart au contrat

[`2_calcul_delta_max.md`](../../../contrats/aeration_blocage_chauffage/m3_analyse_delta_t/2_calcul_delta_max.md) §Robustesse décrit précisément ce cas : une indisponibilité de `temperature_*` produit un ΔT égal à la référence, « biais conservateur vers la prolongation », comportement « assumé ».
**Ce biais n'est jamais atteint en runtime.** Dès que la référence dépasse 10 °C, c'est-à-dire toujours en saison de chauffe, une sonde indisponible fait avorter M3. Le contrat est faux sur le comportement qu'il dit garantir.

### 2.4 Effet

- **Le 2026-10-17 : nul.** Le vrai ΔT était faible (toutes pièces sous 1 °C) ; le maintien aurait été décidé.
- **En général :** une perte de sonde pendant un refroidissement réel lève le blocage à l'horizon initial, sans analyse. C'est l'inverse de l'intention contractuelle.
- `input_number.aeration_delta_t_utilise` a la même plage 0–10 et le même risque.

### 2.5 Facteur aggravant — disponibilité de la sonde Salle de Jeux

La façade Salle de Jeux est passée cinq fois à `unavailable` en 24 h. Sa chaîne combine deux sources : un module Netatmo via HomeKit et un capteur Zigbee. La consolidée tient une mémoire de 1800 s, dont l'âge est mesuré sur `last_changed`. Une indisponibilité de 2 h 24 implique donc que les deux sources étaient invalides en même temps pendant l'essentiel de la fenêtre.
**Non vérifiable** : ni les deux sources ni la consolidée ne sont historisées, donc ce n'est établissable ni en L3 ni en L4.

### 2.6 Propositions (non implémentées)

| # | Proposition | Préalable |
|---|---|---|
| **A1** | **Arbitrer la règle d'indisponibilité de M3** : soit exclure du maximum les pièces dont la température est indisponible et publier la couverture effective (un ΔT inventé n'est pas une mesure), soit conserver le biais vers la prolongation mais le rendre réellement exécutable. Fixer le cas « toutes pièces indisponibles ». | arbitrage opérateur, puis amendement du contrat M3 |
| **A2** | **Rendre la publication diagnostic incapable de faire échouer la décision** : borner la valeur écrite aux limites des deux `input_number` (ou les élargir), ou publier après la décision. | indépendant de A1 ; patch runtime + checker M3 |
| **A3** | **Instrumenter la chaîne Salle de Jeux** si la cause des décrochages doit être établie : microscope Recorder sur les deux sources et la consolidée, avec échéance conforme à la gouvernance des microscopes (C44). | décision opérateur |

---

## 3. Constat B — Climatisation distante Audi : état figé « En cours »

### 3.1 Fait observé

Le 2026-10-15, alors que l'intégration Audi Connect était éteinte (constat C), `script.audi_climatisation_distante` a été lancé :

1. la garde « véhicule introuvable » est franchie, car le device reste au registre même intégration éteinte ;
2. `input_select.audi_climatisation_commande_etat` ← « En cours » ;
3. `audiconnect.start_climate_control` ⇒ action introuvable ⇒ le script s'arrête.

Au relevé, l'état affiché est **toujours « En cours »**, deux jours plus tard. La réconciliation existante (INV-CMD-8) ne traite que `Confirmée → Au repos`.

### 3.2 Lien avec C25

C25 est en clôture conditionnelle avec une seule réserve, **E6** (comportement en échec), que le registre demande déjà de redéfinir après le constat L4 du 2026-10-12. Ce cas est un **mode d'échec non couvert par E6** : l'échec ne vient pas du véhicule mais de l'absence de l'intégration. Il produit une restitution mensongère et durable.

### 3.3 Propositions (non implémentées)

| # | Proposition |
|---|---|
| **B1** | Garde d'entrée : refuser la commande, sans passer par « En cours », si `sensor.audi_a3_sportback_e_tron_climatisation_state` est `unavailable` ou `unknown` (signe observable d'une intégration non chargée) ; journaliser le refus. |
| **B2** | Filet de restitution : un « En cours » plus ancien que la fenêtre d'observation du script (2 à 3 min) est réconcilié vers un état honnête. Selon l'arbitrage, réutiliser « Non confirmée (timeout) » ou ajouter une option d'échec. |
| **B3** | Intégrer ce mode d'échec à la redéfinition d'E6 (C25). |

Remise à zéro immédiate : l'état actuel peut être ramené à « Au repos » à la main ; ce geste ne corrige pas la cause.

---

## 4. Constat C — Audi Connect hors service (externe)

- L'entrée d'intégration est en attente de nouvel essai depuis le redémarrage du 2026-10-14. Environ 475 échecs de connexion ont eu lieu en trois jours, avec le motif « Token refresh rejected: invalid assertion headers ».
- La version chargée est la **2.5.1**, versionnée par `adfa4738`. Cette version reformule précisément ce message : ne pas supprimer l'intégration, car la cause est côté constructeur et une réinstallation pourrait être impossible tant qu'elle dure.
- **Aucune action locale.** Ne pas supprimer ni reconfigurer l'entrée ; surveiller le correctif amont. Conséquence fonctionnelle : capteurs véhicule et commande de climatisation indisponibles (cf. constat B).

---

## 5. Bruit qualifié

| Entrées | Source | Qualification | Vérification |
|---|---|---|---|
| Atmo France (2) | API externe | réponse vide ou erreur 500 du fournisseur, deux jours | — |
| Synology (1), Supervisor (1) | intégrations | échec unique et passager | aucune répétition |
| Proxy BLE n° 3 et Bluetti (9) | ESPHome, `bluetti_bt`, BlueZ | grappe de six minutes le 2026-10-16, concomitante d'une mise à jour du micrologiciel du proxy ; erreurs Bluetooth « 133 » isolées et non rattrapées par l'intégration Bluetti | données Bluetti fraîches ; micrologiciel à jour |
| Fujitsu Airstage (4) | intégration locale | quatre injoignabilités en trois jours, récupérées | équipement disponible au relevé ; non historisé, fréquence non qualifiable |
| Netatmo `rf_status` en double (2) | intégration Netatmo | identifiant dupliqué à chaque démarrage ; la seconde création est ignorée | `sensor.jardin_1_puissance_rf` disponible et à jour |
| Aspirateur `load_multi_map` (1) | Roborock | cas déjà documenté dans [`lancer_mission.yaml`](../../../../10_scripts/aspirateur/lancer_mission.yaml) (étape 5) : `continue_on_error`, la postcondition tranche | verdict de la mission non vérifiable (entités non historisées) |
| ECS vaisselle « Already running » (1) | `mode: single` | le créneau suivant tombe pendant le cycle ECS lancé au créneau précédent : comportement attendu | `max_exceeded: silent` supprimerait l'avertissement (cosmétique) |

---

## 6. Rattachement et suites

| Constat | Rattachement | Suite proposée |
|---|---|---|
| A | **Aucun chantier existant.** C19 (aération) traite la clôture d'épisode, pas M3. | Arbitrer l'ouverture d'un chantier aération (A1 puis A2) ; A2 seul est un correctif borné. |
| B | **C25**, réserve E6 | Verser B1–B3 à la redéfinition d'E6. |
| C | — | Aucune ; surveiller l'amont. |

Ce rapport ne change l'état d'aucun chantier : le registre n'est pas modifié.

**Déploiement.** Rien n'est à déployer : aucun YAML n'est modifié.
