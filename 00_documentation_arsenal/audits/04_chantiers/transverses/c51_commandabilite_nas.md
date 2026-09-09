# Chantier TRANSVERSE (C51) — Commandabilité Arsenal → NAS

| Champ | Valeur |
|---|---|
| **Chantier** | Permettre à Home Assistant/Arsenal de demander au NAS, via MQTT, l'exécution des deux opérations métier existantes `AUDIT` et `RELEASE_DIFF`, sans fusionner leurs chaînes, sans big bang sur les tâches DSM actuelles, et sans jamais confondre la transaction de commande et le résultat métier qu'elle produit. |
| **Domaine** | Transverse — dépôts `arsenal` et `arsenal-ha-backup-timeline` ; domaines Home Assistant `arsenal_self` (audit) et `arsenal_nas` (release_diff). |
| **Statut** | **Ouvert (2026-09-08) — socle transactionnel NAS local livré et mergé côté `arsenal-ha-backup-timeline` (2026-09-09).** Verrou RELEASE_DIFF (Lot 2), durcissement AUDIT + `run_id` corrélable (Lot 3) et moteur d'admission transactionnelle locale (Lot 4 — `admission/bin/admission_core.py`) livrés, mergés et testés **en dépôt** (concurrence même process et multi-process testée). Contrat `nas_transactionnel.md` v1.2.1. Chantier désormais en phase **transport/intégration MQTT → Arsenal → terrain** : aucun listener MQTT NAS, aucun daemon/service d'admission, aucune commande MQTT activée, aucune preuve terrain — voir §12.1. |
| **Priorité** | P2 — aucun risque fonctionnel actuel ; enjeu d'architecture et de gouvernance documentaire avant toute commandabilité. |
| **Ouvert le** | 2026-09-08. |
| **Registre** | Chantier **C51** — ① Actifs, cf. [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Mesure amont** | Audit terrain NAS en lecture seule (2026-09-08, DSM + SSH, aucune écriture) ; synthèse architecturale confrontant Git et terrain (même session) ; HEAD `arsenal` `a317b5b82c91bcbb79b02d787ed2e0ca2386398e` (branche par défaut) ; HEAD `arsenal-ha-backup-timeline` `033b1eff498ebd1107abe516bcca81c01f936f25` (branche `main`), confirmé identique entre le rapport terrain et l'API GitHub au moment de l'audit, `git status`/`diff` vides côté NAS hormis un fichier non suivi hors périmètre. |
| **Mise à jour** | 2026-09-09 — merge du socle transactionnel NAS local (RELEASE_DIFF, AUDIT, admission locale) dans `arsenal-ha-backup-timeline`. **Lot documentaire intermédiaire uniquement** : aucun runtime Arsenal, aucun runtime NAS supplémentaire, aucun nouveau contrat, aucun nouveau chantier ouverts par cette mise à jour. Voir §12.1. |

---

## 1. Objet et périmètre

Arsenal doit pouvoir demander au NAS, via MQTT, l'exécution de deux opérations
métier **distinctes**, chacune raccordée à sa chaîne existante :

- **`AUDIT`** — identification du backup pertinent, stabilité démontrée,
  extraction/idempotence, audit patrimonial, publication du résultat ;
- **`RELEASE_DIFF`** — génération des diffs sémantiques inter-releases, sans
  paramètre métier (`--couple` non exposé en V1).

Le diff patrimonial forensic (`ha_backup_timeline_diff.py`, `_diff/`, contrat
[`diff_auto.md`](../../../outils_externes/nas_arsenal/diff/diff_auto.md)) est
**hors périmètre**, sauf contradiction démontrée.

Vocabulaire fermé : `AUDIT` | `RELEASE_DIFF`. Aucune exécution de commande NAS
arbitraire, aucun chemin shell fourni par HA, aucune commande générique
extensible sans contrat.

---

## 2. Arbitrages Direction déjà tranchés (repris tels quels)

Ces points sont **acquis** pour ce chantier et ne sont pas rediscutés par les
lots suivants sans décision explicite contraire :

1. Deux commandes V1 seulement : `AUDIT`, `RELEASE_DIFF`.
2. `RELEASE_DIFF` sans `--couple` ni aucun autre paramètre métier transmis
   par HA en V1.
3. HA est autorité de **demande**. Le NAS reste seul autorité d'**admission**,
   d'**exécution**, de **concurrence** et de **résultat**. `arsenal_self.md`
   et `arsenal_nas.md` ne sont **pas** autorités du résultat métier : ils
   consomment, projettent et diagnostiquent la fraîcheur/disponibilité, sans
   jamais recalculer le verdict.
4. Backend Arsenal décide, UI Lovelace rend — aucune logique de transport
   MQTT dans le bouton.
5. Corrélation `request_id → run_id` obligatoire en V1, pour les deux
   opérations. Le NAS attribue le `run_id` au niveau admission/exécution,
   **avant** l'entrée dans le moteur métier — et non plus, comme aujourd'hui
   pour `release_diff.py`, à l'intérieur du moteur lui-même.
6. `BUSY` explicite et immédiat si l'opération demandée est déjà en cours.
   Aucune coalescence en V1. Aucune file d'attente.
7. Aucun verrou global `AUDIT`/`RELEASE_DIFF` sans invariant partagé
   démontré — les deux opérations peuvent tourner simultanément.
8. La garantie de stabilité du backup (aujourd'hui portée par
   `watch_new_backup.sh`) reste une **responsabilité NAS**, quel que soit le
   sort futur de son implémentation actuelle. Ce chantier contractualise la
   garantie, pas le script qui la porte aujourd'hui.
9. La transaction de commande et le résultat métier sont **formellement
   distincts** et ne sont jamais fusionnés, y compris dans le nommage des
   champs. Une transaction techniquement terminée avec succès peut produire
   un résultat métier en anomalie.
10. L'exclusion mutuelle `RELEASE_DIFF` (absente aujourd'hui — confirmé par
    lecture intégrale de `release_diff.py` et `run_release_diff.sh`, aucun
    verrou, aucun `flock`) est un **prérequis bloquant** avant toute
    activation d'une commande MQTT `RELEASE_DIFF`. Aucune tolérance V1.
11. Aucun ID d'automatisation Home Assistant n'est inventé par ce chantier
    (doctrine [`id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md)).
    Les IDs éventuels sont fournis par la Direction au moment de
    l'implémentation runtime.

---

## 3. Terminologie terrain — précision opposable

Formulation à respecter dans toute documentation de transition ou de
décommissionnement issue de ce chantier : il n'existe pas « trois
déclencheurs AUDIT ». Le terrain établit :

- **une tâche d'extraction périodique indépendante** (`Arsenal - Timeline
  Backups HA`, 5 minutes, extraction seule — n'appelle ni l'audit ni la
  publication MQTT) ;
- **deux chemins de déclenchement du pipeline AUDIT** (extraction + audit +
  MQTT) : le watcher (`Arsenal - Pipeline Watcher`, réactif, avec contrôle
  de stabilité) et la tâche directe quotidienne (`Pipeline HA`, 02:45,
  inconditionnelle).

La formulation « trois déclencheurs AUDIT », employée dans une version
antérieure de l'analyse de ce chantier, est erronée et ne doit pas être
reprise.

---

## 4. Matrice des autorités

| Strate | Autorité | Responsabilité | Interdictions |
|---|---|---|---|
| UI Arsenal (Lovelace) | Aucune | Exprimer une intention utilisateur | Ne parle jamais MQTT ; ne porte aucune logique de transport ni de concurrence |
| Backend Arsenal | Demande | Construire la commande, vocabulaire fermé, `request_id` | N'exécute rien ; ne décide jamais du résultat métier |
| Transport MQTT | Aucune | Acheminer commande et état | N'interprète pas le payload ; pas de retain sur le canal commande |
| Admission NAS | Admission | Vocabulaire fermé, déduplication, concurrence, ouverture/fermeture de transaction, attribution du `run_id` | Ne modifie jamais le vocabulaire reçu |
| Moteur AUDIT | Exécution (AUDIT) | Produit le verdict patrimonial existant | Ne décide pas de la concurrence globale |
| Moteur RELEASE_DIFF | Exécution (RELEASE_DIFF) | Produit le diff/résumé existant | Idem ; reste « clos » comme aujourd'hui pour sa sémantique propre |
| Domaine HA `arsenal_self` | Consommation/diagnostic | Expose, qualifie la fraîcheur du résultat AUDIT | Ne recalcule jamais le verdict patrimonial |
| Domaine HA `arsenal_nas` | Consommation/diagnostic | Expose l'état d'exécution RELEASE_DIFF | Ne recalcule jamais le résultat |

---

## 5. Contrat transactionnel commun

Le contrat sémantique (vocabulaire, identité de commande, admission,
idempotence, `BUSY`, corrélation `request_id`↔`run_id`, terminaison
transactionnelle, sécurité minimale) est intégralement porté par
[`contrats/nas_transactionnel.md`](../../../contrats/nas_transactionnel.md).

Ce document de chantier **ne duplique pas** ce contrat. Les spécialisations
moteur restent souveraines dans leurs contrats propres :
[`outils_externes/nas_arsenal/diff/diff_release.md`](../../../outils_externes/nas_arsenal/diff/diff_release.md),
[`diff/release_diff_mqtt.md`](../../../outils_externes/nas_arsenal/diff/release_diff_mqtt.md),
[`audit/audit.md`](../../../outils_externes/nas_arsenal/audit/audit.md),
[`audit/mqtt.md`](../../../outils_externes/nas_arsenal/audit/mqtt.md).

---

## 6. Invariants propres à AUDIT

- Couvre, à la manière de `run_pipeline.sh` : identification du backup
  pertinent, stabilité démontrée, extraction/idempotence, audit,
  publication du résultat. Le périmètre exact (déclenchement systématique
  d'une extraction, ou audit du dernier `versions/` déjà présent) reste à
  confirmer à l'implémentation — voir §14.
- La garantie de stabilité (aujourd'hui : double mesure de taille à 60 s
  d'intervalle) reste NAS, indépendamment de son implémentation actuelle.
- L'atomicité de publication dans `versions/` (rename atomique après
  marqueur de complétude) est préservée sans modification — c'est elle qui
  garantit qu'AUDIT et RELEASE_DIFF ne s'observent jamais en écriture
  partielle l'un l'autre.
- Un identifiant d'exécution corrélable (`run_id`) est créé — n'existe pas
  aujourd'hui dans la chaîne AUDIT.
- Le résultat métier existant (`arsenal_self`, `ok`/`alert`/`error`) n'est
  pas modifié par ce chantier.
- Concurrence AUDIT+AUDIT : non sûre aujourd'hui (verrou `run_audit.sh` non
  atomique, sans détection de PID vivant ; aucun verrou partagé entre
  extraction directe et extraction embarquée dans `run_pipeline.sh`). Une
  commande MQTT AUDIT réutilise et durcit les verrous existants plutôt que
  d'en créer un nouveau et incompatible.

## 7. Invariants propres à RELEASE_DIFF

- Aucune option `--couple` ni aucun autre paramètre métier exposé via MQTT
  en V1 (le mode batch consécutif de `release_diff.py` est seul concerné).
- Exclusion mutuelle RELEASE_DIFF+RELEASE_DIFF : **prérequis bloquant**
  avant activation (voir §2.10) — travail moteur/wrapper indépendant de
  MQTT.
- `run_id` corrélable à `request_id` : le mécanisme `run_id`/`event_id`
  déjà spécifié par `diff_release.md`/`release_diff_mqtt.md` est réutilisé,
  non redéfini ; seule son origine change (admission NAS, avant le moteur,
  au lieu du moteur lui-même).
- Les états métier existants (`ok`/`partial`/`error`, domaine
  `arsenal_nas`) restent inchangés.
- Jamais fusionné avec AUDIT — chaînes métier strictement distinctes.

---

## 8. Politique de concurrence

| Situation | Politique |
|---|---|
| AUDIT demandé, AUDIT déjà en cours | Rejet explicite `BUSY`. Aucune coalescence, aucune file. |
| RELEASE_DIFF demandé, RELEASE_DIFF déjà en cours | Rejet explicite `BUSY`. Aucune coalescence, aucune file. |
| AUDIT demandé, RELEASE_DIFF en cours | Autorisé — aucun invariant partagé démontré ne justifie un verrou global. |
| RELEASE_DIFF demandé, AUDIT en cours | Autorisé — même raison. |

Point de vigilance annexe, hors périmètre strict de ce chantier : la tâche
`Arsenal - Retention` (04:00) modifie `versions/` sans verrou partagé avec
RELEASE_DIFF (03:15) ; aucun chevauchement d'horaire aujourd'hui.

---

## 9. Architecture transitoire et décommissionnements possibles

Aucun big bang. Le canal MQTT s'ajoute comme chemin supplémentaire, sans
toucher aux tâches DSM existantes tant que leur garantie n'est pas reprise
et prouvée en terrain.

| Tâche DSM | Fonction actuelle | Conservation transitoire | Condition de suppression | Mécanisme cible |
|---|---|---|---|---|
| `Arsenal - Timeline Backups HA` (extraction directe, 5 min) | Ingestion continue de `versions/`, alimente aussi RELEASE_DIFF et la rétention | Oui | Décision produit (ingestion continue vs sur-demande), pas seulement technique | AUDIT-via-MQTT (si son périmètre inclut l'extraction) ou déclencheur d'ingestion dédié |
| `Arsenal - Pipeline Watcher` | Déclenchement réactif avec contrôle de stabilité | Oui | Preuve terrain que l'admission NAS porte elle-même la garantie de stabilité | Contrôle de stabilité migré dans la couche admission NAS |
| `Pipeline HA` (02:45, inconditionnel) | Filet de sécurité quotidien | Oui | Preuve qu'un déclenchement planifié MQTT ne laisse aucune fenêtre sans audit | Automatisation Arsenal planifiée émettant `AUDIT` |
| `Arsenal - Release Diff` (03:15) | Déclenchement quotidien inconditionnel | Oui | Verrou RELEASE_DIFF ajouté (§2.10) **et** preuve terrain du chemin MQTT | Automatisation Arsenal planifiée émettant `RELEASE_DIFF` |

`Arsenal - Retention` et `Arsenal - Quarantine Purger` restent hors
périmètre de ce chantier.

---

## 10. Sécurité (invariants minimaux)

- Vocabulaire fermé `AUDIT`/`RELEASE_DIFF`, rien d'autre n'est interprété.
- Aucun argument shell arbitraire transmis par HA.
- Commandes non retenues (`retain=false`) sur le canal de commande —
  contraste assumé avec les topics état, retenus.
- Déduplication applicative (mémoire persistante bornée côté NAS), en sus
  du QoS MQTT.
- Identité MQTT dédiée au canal de commande : **obligatoire**, distincte
  des comptes existants (`nas_audit`, `nas_imprimerie`, `boiler_bridge`,
  `rain_bird_mqtt`) — compte concret non choisi ici. Moindre privilège
  (cantonnement ACL par topic) reste la **cible normative** de cette
  identité dédiée, non garantie aujourd'hui — voir constat ci-dessous.
- **Constat terrain (audit broker, 2026-09-09).** Le broker MQTT de
  production est l'add-on officiel HA Mosquitto (`core_mosquitto`),
  authentification par comptes HA locaux, `customize.active = false` :
  aucune ACL par topic active aujourd'hui,
  pour aucun compte. Activer une ACL par topic impose une politique
  explicite globale à tous les comptes du broker, pas seulement au futur
  compte C51 — chantier broker transversal (HA, Zigbee2MQTT, chauffage,
  arrosage), **non ouvert par ce chantier**. Le cantonnement ACL par topic
  de `nas_admission` ne peut donc pas être garanti sans cette migration.
- **Dette explicite.** Identité dédiée sans cantonnement ACL par topic =
  dette de sécurité documentée, non tranchée par ce chantier — voir §13.

---

## 11. Documentation normative — ce que ce chantier modifie

### A. Modifié à l'ouverture (ce lot)

- `contrats/nas_transactionnel.md` *(nouveau)*.
- `contrats/arsenal_nas.md` — statut `proposé/non implémenté` → `actif`
  (démontré, §2.3 déjà correct) ; renvoi vers `nas_transactionnel.md`.
- `contrats/arsenal_self.md` — renvoi vers `nas_transactionnel.md`.
- `contrats/index.md` — ligne pour `nas_transactionnel.md`.
- `outils_externes/nas_arsenal/diff/release_diff_mqtt.md` — statut
  `proposé/non implémenté` → `actif/implémenté` (démontré).
- `outils_externes/nas_arsenal/diff/diff_auto.md` — fréquence 30→5 minutes
  (correction factuelle, même tâche DSM que le terrain) ; un renvoi vers
  la continuation du pipeline AUDIT.
- `outils_externes/nas_arsenal/pipeline_watcher.md` — statut
  `proposition initiale` → `actif/implémenté` ; note de coexistence avec
  les deux autres chemins de déclenchement.
- `architecture/ecosysteme_depots_satellites.md` — fiche manquante pour
  `arsenal-ha-backup-timeline` (absente du registre des dépôts gouvernés).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.

### A2. Lot documentaire intermédiaire (2026-09-09) — après merge NAS local

- Le présent document — Statut, `Mesure amont`/`Mise à jour`, §12.1
  (nouveau).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **non modifié** (toujours v1.1.1) ;
  vérifié conforme à l'état livré.
- Aucun autre contrat, aucune doc runtime, aucune UI, aucun CI touchés par
  ce lot.

### B. Référencés, non modifiés

`outils_externes/nas_arsenal/audit/audit.md`, `audit/mqtt.md`,
`diff/diff_release.md` (contenu substantif — exact pour son périmètre
actuel), `contrats/switchbot_transactionnel.md` (précédent transactionnel
réutilisé), `quarantine_purger.md`, `retention_manager.md` (hors
périmètre).

### C. À modifier au moment des lots runtime

- `diff/diff_release.md` — invariant de concurrence, une fois le verrou
  RELEASE_DIFF effectivement implémenté ; clause « `run_id` attribué par
  l'admission NAS ».
- `schemas_ascii/pipeline_nas_ha.md` — schéma à jour une fois
  l'admission implémentée ; correction de l'invariant I-8 (« la
  concurrence d'extraction est neutralisée par flock », qui surstate déjà
  la réalité aujourd'hui).
- Dérive de nommage `CONTRAT_AUDIT_MQTT.md` (référencée dans
  `publish_audit_mqtt.py` et 6 sensors Arsenal, alors que le contrat réel
  est `audit/mqtt.md`) — hors portée documentaire pure, nécessite de
  toucher `.py`/`.yaml`.
- Extension éventuelle des schémas `arsenal_nas.md`/`arsenal_self.md`/
  `audit/mqtt.md`/`release_diff_mqtt.md` pour porter `run_id`/`request_id`.
- Documentation locale dans `arsenal-ha-backup-timeline` — réévaluée à ce
  moment, non un principe définitif.

### D. À modifier à la clôture

- `audits/REGISTRE_CHANTIERS.md` — passage de ① Actifs à `Clos récent`.
- Le présent document — §15 renseigné.
- `architecture/ecosysteme_depots_satellites.md` — mise à jour de la fiche
  §4.8 si des tâches DSM sont effectivement décommissionnées.

---

## 12. Découpage en lots

| Lot | Dépôt | Objectif | Dépendances | Preuve | STOP | Risque principal |
|---|---|---|---|---|---|---|
| 1 (ce lot) | `arsenal` | Contrat transactionnel + ouverture chantier + corrections factuelles | Arbitrages §2 tranchés | Documents relus/validés, aucune implémentation | Un invariant reste ambigu | Contrat sous-spécifié |
| 2 | `arsenal-ha-backup-timeline` | Verrou RELEASE_DIFF (cycle lecture-calcul-écriture) | Aucune (correctif indépendant de MQTT) | Test de double-exécution simulée sans corruption | Régression de l'idempotence existante | Modifier un moteur en production quotidienne |
| 3 | `arsenal-ha-backup-timeline` | Verrou AUDIT durci + `run_id` corrélable | Lot 1 (forme du run_id) | Exécution de test `request_id`→`run_id` traçable | Casse le contrat MQTT état existant | Toucher `run_audit.sh`, en prod quotidienne |
| 4 | `arsenal-ha-backup-timeline` | Admission NAS minimale, une seule opération pilote | Lots 1–3 | Commande MQTT manuelle → run_id corrélé → résultat identique à un déclenchement DSM | Divergence avec le comportement DSM existant | Concurrence avec les tâches DSM si verrou non partagé |
| 5 | `arsenal` | Backend Arsenal — émission de commande | Lot 4 validé terrain | Appel de test hors UI | Vocabulaire plus large que le contrat | Couplage prématuré à une UI non stabilisée |
| 6 | `arsenal-ha-backup-timeline` + `arsenal` | Extension à la seconde opération | Lot 5 | Idem Lot 4 | Verrou partagé non justifié entre AUDIT et RELEASE_DIFF | Tentation de fusionner les deux chaînes |
| 7 | `arsenal` | UI Lovelace (bouton) | Lots 5–6 | Usage réel | Le bouton porte lui-même une logique MQTT | Régression backend décide/UI rend |
| 8 | NAS (hors Git) + doc | Décommissionnement conditionnel des tâches DSM | Lots 4–7 + observation terrain | N jours sans écart ancien/nouveau mécanisme | Toute perte de garantie constatée | Décommissionnement prématuré |
| 9 | `arsenal` + `arsenal-ha-backup-timeline` | Clôture documentaire | Lot 8 | Revue documentaire | — | Dette documentaire si sauté |

---

### 12.1 État d'avancement — mise à jour documentaire du 2026-09-09

Lot documentaire intermédiaire uniquement : ne modifie pas le découpage
ci-dessus, ne referme aucun lot, n'ouvre aucun nouveau lot. Documente l'état
réel après le merge du socle transactionnel NAS local dans
`arsenal-ha-backup-timeline`. Vocabulaire de statut : « livré, mergé » /
« livré, mergé, testé » (dépôt) — jamais « déployé » ni « validé terrain »
tant que la preuve terrain correspondante n'existe pas.

| Lot | État | Constat |
|---|---|---|
| 1 | Livré | Contrat `nas_transactionnel.md` (v1.1.1) et ouverture du chantier — inchangé par ce lot. |
| 2 — verrou RELEASE_DIFF | **Livré, mergé** | Exclusion mutuelle robuste, verrou métier `runtime/release_diff.lock`, RC 75 si occupé (chemin legacy), `--run-id` explicite, comportement legacy DSM conservé, aucun paramètre métier libre exposé. Non déployé, non validé terrain. |
| 3 — durcissement AUDIT + `run_id` | **Livré, mergé** | AUDIT commandable via `run_pipeline.sh` (sélection/extraction, contrôle de stabilité, audit, publication, extraction runtime informative), verrou métier `runtime/run_pipeline.lock`, RC 75 si occupé, source instable différée (RC extracteur 3 / pipeline 32) sans faux marquage traité par le watcher, `--run-id` propagé jusqu'au résultat AUDIT, compatibilité avec les déclenchements legacy préservée. Non déployé, non validé terrain. |
| 4 — admission NAS minimale | **Moteur livré, mergé, testé ; preuve du lot restante** | `admission/bin/admission_core.py` mergé : ledger persistant, verrou ledger court, fail-closed si ledger indisponible/corrompu, validation des demandes, opérations V1 (`AUDIT`/`RELEASE_DIFF`), `request_id` durable et identité immuable (`operation`/`ts`/`expires_at`/`source`), verdicts `rejected_precondition`/`rejected_stale`/`rejected_conflict`/`admission_unavailable`/`rejected_busy`, `run_id` UUID4 avec mapping durable request_id→run_id, persistance `admitted` avant wrapper, déduplication durable (aucune réexécution d'un `request_id` connu, replay terminal), réconciliation des `admitted`, terminaison `completed`/`technical_failure`, handoff du vrai verrou métier via fd dynamique hérité (conservé jusqu'à la fin réelle des descendants), validation fail-closed du fd reçu par les wrappers, compatibilité legacy préservée, concurrence même process et multi-process testée. **Preuve du lot** (« commande MQTT manuelle → run_id corrélé → résultat identique à un déclenchement DSM ») **non fournie** : aucun listener MQTT, aucun daemon/service d'admission. |
| 5 — backend Arsenal (émission) | Non commencé | Génération côté Arsenal des enveloppes `request_id`/`ts`/`expires_at`/`source`, backend de commande Arsenal/HA, suivi transactionnel côté Arsenal : non livrés. |
| 6 — extension seconde opération | Non applicable | Dépend du lot 5, non commencé. |
| 7 — UI Lovelace | Non commencé | Aucune UI de commande NAS livrée. |
| 8 — décommissionnement DSM | Non commencé | Aucun retrait ni rationalisation des anciens déclenchements DSM. |
| 9 — clôture documentaire | Non applicable | Chantier ouvert — aucune clôture. |

Non livré, à ne pas confondre avec ce qui précède (rappel exhaustif) :
listener MQTT NAS ; daemon/service d'admission ; choix définitif du mode
d'hébergement du listener ; compte MQTT dédié définitif ; ACL broker
vérifiées pour la commande ; activation de commandes MQTT ; backend de
commande Arsenal/HA ; génération côté Arsenal des enveloppes
`request_id`/`ts`/`expires_at`/`source` ; suivi transactionnel côté
Arsenal ; UI de commande NAS ; déploiement du nouveau noyau d'admission sur
le NAS de production ; preuves terrain de commande AUDIT, RELEASE_DIFF,
replay/BUSY/crash-reprise ; retrait ou rationalisation des anciens
déclenchements DSM ; clôture C51.

---

## 13. Vérifications encore nécessaires avant implémentation

*(ne bloquent pas la documentation — bloquent les lots 2+)*

- ACL MQTT réelles sur le broker — **vérifiées (2026-09-09)** : voir §10.
  Point de fait tranché ; **arbitrage Direction requis** avant toute
  activation terrain du canal de commande (Lot 4 preuve terrain / Lot 5+) :
  accepter la dette — identité dédiée sans cantonnement topic, avec les
  mesures de réduction du risque applicatif déjà présentes (vocabulaire
  fermé §5, validation `admit()`) — ou conditionner l'activation à une
  migration ACL globale du broker.
- Accès Docker/Container Manager pour utilisateur non-root, ou mécanisme
  de supervision alternatif du futur listener.
- Comportement réel de `ha_backup_timeline_extract_v2.py` sous collision
  effective (test à réaliser, pas seulement lecture de code).
- Périmètre exact de l'opération AUDIT via MQTT (§6, premier point).
- Validation du verrou RELEASE_DIFF sous double-exécution simulée réelle.

---

## 14. Interdictions opposables à tout lot futur de C51

- Aucun ID d'automatisation Home Assistant inventé par un lot de ce
  chantier.
- Aucune fusion des chaînes AUDIT et RELEASE_DIFF.
- Aucun verrou global AUDIT/RELEASE_DIFF sans invariant partagé
  nouvellement démontré.
- Aucune confusion entre transaction et résultat métier, y compris dans le
  nommage des champs d'un futur payload.
- Aucune activation d'une commande MQTT RELEASE_DIFF avant que le verrou
  d'exclusion mutuelle (Lot 2) soit livré et prouvé.
- Aucune suppression de tâche DSM sans preuve terrain que sa garantie est
  reprise ailleurs.
- Aucune activation terrain du canal de commande MQTT sans arbitrage
  Direction explicite sur la dette ACL constatée au §10.

---

## 15. Critères de clôture

1. Les quatre tâches DSM du §9 ont chacune une décision explicite
   (conservées, remplacées avec preuve, ou décommissionnées) — pas de
   statu quo non motivé.
2. Le contrat `nas_transactionnel.md` est implémenté et validé terrain pour
   les deux opérations.
3. Le verrou RELEASE_DIFF (Lot 2) et le durcissement AUDIT (Lot 3) sont
   livrés et prouvés.
4. Aucune interdiction du §14 n'a été violée sur l'ensemble des lots.
5. La documentation de catégorie C (§11.C) a été mise à jour au fil des
   lots runtime concernés, sans reste ouvert.

---

*Chantier ouvert le 2026-09-08. Source faisant foi pour la ligne C51 du
registre.*
