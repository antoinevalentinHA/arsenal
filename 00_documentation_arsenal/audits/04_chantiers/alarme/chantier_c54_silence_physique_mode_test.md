# 🚨 ARSENAL — CHANTIER C54 · Alarme — Silence physique en mode test & commande d'arrêt sonore

## 📌 Statut

- **Ouvert (2026-10-03) — lot 1 implémenté et déployé (HA rechargé le 2026-10-03 à 19:04:32, établi en L4) ; volet automatique du critère 2 acquis en L4 le 2026-10-12 ; restent le désarmement dashboard, le constat sonore opérateur (L5) et le lot 2 (§8).**
- **Identifiant global** : **C54**
- **Domaine** : Sécurité / Alarme — actionneurs sonores (contrat [`70_sirene_actions_terminales.md`](../../../contrats/alarme/70_sirene_actions_terminales.md))
- **Priorité** : **P1** — nuisance sonore réelle et répétée (plusieurs fois par jour) sur le foyer, et réserve ouverte sur l'**efficacité** de la coupe sirène en alarme réelle.
- **Changelog** : non créé — artefact de release produit sur déclenchement opérateur (doctrine `redaction_changelog.md` §1).

---

## 1. Règle fonctionnelle (arbitrée par l'opérateur, 2026-10-03)

- **Mode test OFF** — comportement réel intégral : détection, délais, déclenchement, notifications, signaux prévus, sirène forte. **Aucun affaiblissement.**
- **Mode test ON** — la chaîne logique reste complète et observable (détection, décision, timers, transitions, notifications, traces), mais **silence physique absolu** pour tout actionneur sonore de l'alarme.

---

## 2. Incident (2026-10-03) — chronologie établie par traces runtime

Sources : traces HA (`trace/get`), historique recorder, journaux Zigbee2MQTT (`info`), lus en lecture seule.

| Temps (T0 = ouverture de l'accès) | Événement | Effet |
|---|---|---|
| T0 − 15 min 10 s | Armement automatique (`script.alarme_armer`) | mode test lu `on` → pas de `sirene_bip` |
| T0 | Ouverture de l'accès → `10020000000031` | `timer.delai_entree` (60 s) ; bip non exécuté (mode test `on`) |
| T0 + 26 s | `binary_sensor.presence_famille_securite` → `on` | — |
| T0 + 41,1 s | Présence confirmée → `10020000000027` → `DISARMED` → `script.alarme_desarmer` (origine `automatisme`) | — |
| **T0 + 41,1 s (+ 5 ms)** | `script.arret_sirene` → `mqtt.publish zigbee2mqtt/sirene/set {"warning":{"mode":"stop"}}` | **son émis par la sirène** |

- Panneau jamais `triggered` ; `sirene_bip`, `sirene_bip_bip`, `sirene_brutale`, `sirene_test` sans aucune trace d'exécution ; aucune action clavier (Zigbee2MQTT : rapports périodiques seuls) ; aucun événement spontané de la sirène.
- **Reproduction opérateur** : armement puis désarmement dashboard à 2 s d'intervalle, en mode test → seul `warning/stop` envoyé → séquence à deux tons (~4 cycles) ; bouton UI « Arrêt sirène » → même payload, même son. **Attribution confirmée par l'opérateur.**
- Incident antérieur de la semaine (bruits subis en mode test) : chaque désarmement automatique tracé sur deux jours (5 au total) a émis ce même `warning/stop` — mécanisme identique, très probable ; heure du bruit non disponible.

## 3. Cause

1. **Comportement matériel** : sur la Develco/Frient SIRZB-111, `{"warning":{"mode":"stop"}}` (payload partiel, complété par les valeurs par défaut de Zigbee2MQTT) **produit un son** au lieu d'un silence. Trame Zigbee non observée (journal z2m en `info`).
2. **Doctrine** : le contrat 70 imposait l'appel **inconditionnel** de `script.arret_sirene` à chaque désarmement ⇒ chaque désarmement, automatique compris, mode test compris, faisait sonner la sirène.
3. **Garde au mauvais niveau** (constat d'audit, non causal ici) : le mode test n'était contrôlé que par les appelants, jamais par les actionneurs — un nouvel appelant ou un appel direct contournait l'invariant.

Les gardes existantes (armement, délai d'entrée, bifurcations d'intrusion, sirène forte) ont **toutes** fonctionné : prouvé par traces.

## 4. Lot 1 — implémenté (sans essai matériel)

| Surface | Changement |
|---|---|
| `10_scripts/alarme/desarmement.yaml` | `script.arret_sirene` appelé **uniquement si** le panneau est `triggered` (seul état où Arsenal lance la sirène forte), **indépendamment du mode test** (une sirène réelle reste coupable si le mode test est activé pendant le hurlement). |
| `10_scripts/alarme/sirene/{bip,bip_bip,brutale,test}.yaml` | **Verrou mode test** en première étape, **fail-open** : `{{ not is_state('input_boolean.mode_test_alarme', 'on') }}`. Gardes appelantes conservées. |
| Contrat 70 | § Verrou mode test ; § Chemin d'arrêt amendé (appel restreint à `triggered`, constat « stop sonore », réserves, contrainte `sirene_max_duration ≤ trigger_time`) ; interdictions. |
| Contrats 50 (I2), 90 (UI) | Renvoi au verrou ; bouton « Arrêt sirène » qualifié sonore. |
| `check_alarme_contracts.py` | **S3** verrou fail-open en tête des 4 scripts émetteurs ; **S4** aucune publication vers `zigbee2mqtt/sirene/set` hors `10_scripts/alarme/sirene/` ; **S5** `arret_sirene` appelé par le désarmement uniquement sous garde `triggered`. Mutation vérifiée : S3/S5 échouent sur le code antérieur, S4 sur une publication hors scripts canoniques. |

**Ce que le lot 1 ne change pas** : détection, décision centrale, timers, transitions, notifications, keypads, sirène forte hors mode test, `script.arret_sirene` lui-même (toujours sans condition), bouton UI.

## 5. Risques de régression examinés

- **Vraie alarme** : verrou fail-open (seul `on` explicite bloque) ; hors mode test, les scripts émettent comme avant. Un mode test **oublié à `on`** rend la sirène muette — c'est déjà la sémantique du mode, désormais globale (voir réserve R4).
- **Coupe en alarme réelle** : inchangée sur `triggered`. Fenêtre de cohérence : `number.sirene_max_duration` (60 s, réglage device, **hors dépôt, non vérifiable par CI**) doit rester ≤ `trigger_time` (180 s).
- **Délais / keypads / logique de test** : non touchés.
- **Double autorité** : aucune — le verrou est un veto physique, pas une décision.

## 6. Réserves ouvertes / lot 2 (non engagé)

- **R1** — Le bouton UI « Arrêt sirène » reste **sonore**.
- **R2** — L'**efficacité** de `warning/stop` sur une sirène en plein hurlement n'est **pas établie** (V4 a prouvé l'auto-extinction par durée, pas la coupe par `stop`) : si le `stop` relance une séquence d'avertissement, la coupe d'urgence n'est pas fiable.
- **R3** — Payload `stop` silencieux et efficace à concevoir : **essai réel sur la Develco uniquement avec autorisation explicite de l'opérateur**, journal Zigbee2MQTT temporairement en `debug` pour observer la trame.
- **R4** — Visibilité d'un mode test resté actif (notification persistante / rappel) — à arbitrer.
- **R5** — Exposition à Assist de `switch.sirene_alarm` relevée au registre du 2026-08-17, entité **absente** au 2026-10-03 : à revérifier, sans action à ce stade.

## 7. Critères de clôture

1. Lot 1 mergé **et** déployé (clone runtime à jour, HA rechargé) — quatre états distincts (merge ≠ runtime ≠ HA ≠ terrain).
2. **Preuve terrain** : un désarmement en mode test (automatique et dashboard) ne produit **aucun** son, traces à l'appui (`arret_sirene` non exécuté).
3. Lot 2 instruit : R1–R3 résolues (payload validé par essai autorisé) **ou** requalifiées explicitement par l'opérateur.

## 8. Constat L4 du 2026-10-12

Source : sauvegarde `recorder_20261012.db` (états du 2026-09-11 au 2026-10-12 02:28), analyse `arsenal-runtime/analyses/c54_c1_c23_c55_c57_preuves_l4_20261012`. Les appels de service sont historisés hors liste blanche ; ils portent la preuve.

- **Critère 1 — déploiement établi côté Home Assistant.** #864 est fusionnée le 2026-10-03 à 19:03:47 ; un `script.reload` utilisateur suit à 19:04:32. Le dernier désarmement à l'ancien comportement précède immédiatement le déploiement.
- **Critère 2, volet automatique — acquis en L4.** Avant le déploiement, chaque désarmement appelait `script.arret_sirene` puis publiait `warning/stop` (74 appels `arret_sirene` sur la fenêtre). Après le déploiement : **21 désarmements automatiques, 0 appel `arret_sirene`, 0 publication vers `zigbee2mqtt/sirene/set`, 0 appel `sirene_bip` / `sirene_bip_bip` / `sirene_brutale` / `sirene_test`**. Home Assistant n'émet donc plus la commande sonore. Le silence physique lui-même reste une preuve L5, à constater par l'opérateur.
- **Non exercé.** Aucun désarmement depuis le dashboard après le déploiement (0 sur 21) ; il ne surviendra pas de lui-même et relève d'un acte opérateur. Le verrou en tête des scripts sirène n'a pas été sollicité, les appelants filtrant déjà en amont.
- **Observation hors critère.** Consignée hors dépôt (`arsenal-runtime/analyses/c54_c1_c23_c55_c57_preuves_l4_20261012`).
