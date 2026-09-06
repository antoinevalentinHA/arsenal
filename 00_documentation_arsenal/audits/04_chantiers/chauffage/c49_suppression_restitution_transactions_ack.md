# Chantier CHAUFFAGE (C49) — Boiler — suppression de la restitution Transactions et des projections ACK legacy

| Champ | Valeur |
|---|---|
| **Chantier** | Supprimer la section UI `🔁 Transactions` du corps Boiler partagé et les **12 projections ACK legacy** (`*_ts`, `*_correlation`, `*_result`) devenues sans consommateur, en préservant intégralement le runtime transactionnel réellement exploité (`*_raw`, `*_status`, `*_request_id`, `*_reason`, helpers de requête, commandabilité par rôle). |
| **Domaine** | Chauffage / boiler — la surface ACK est partagée avec l'ECS (rôle `dhw_setpoint`). Rangé sous `chauffage/`, comme le socle transactionnel et la migration Boilerack. |
| **Statut** | **CLOS (2026-09-06).** Les 5 lots sont livrés et les 4 arbitrages tranchés ; les 14 critères du §7 sont satisfaits. Voir §10. |
| **Priorité** | P2 — aucun risque fonctionnel courant ; la section incriminée est en lecture seule et n'entre dans aucune boucle de décision. Enjeu de véracité de restitution et de dette runtime morte. |
| **Ouvert le** | 2026-09-06. |
| **Registre** | Chantier **C49** — ① Actifs, cf. [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Sources normatives amont** | [`contrats/boiler/consommation_ack.md`](../../../contrats/boiler/consommation_ack.md) (§4 constate déjà la disparition de `ts` du payload) · [`contrats/boiler/mqtt_ack_ha.md`](../../../contrats/boiler/mqtt_ack_ha.md) §10 · [`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md) §16 (clôture fonctionnelle du recâblage). |
| **Relation à C48** | **Distinct et disjoint.** C48 gouverne la convergence *documentaire* de la migration Boiler Bridge → Boilerack et reste arrêté à son point d'avancement. C49 traite une **conséquence runtime + UI** de cette migration : la surface ACK laissée en place « faute de lot runtime » par `consommation_ack.md` §4. C49 **n'exécute aucun lot de C48** et ne modifie aucun de ses axes. |

> **⚠️ Portée de cette ouverture.** Strictement documentaire.
> Aucun fichier Lovelace, template sensor, script, automatisation, checker,
> helper ou dashboard n'est créé, modifié ou retiré par ce document. Aucun accès
> à Home Assistant, au Raspberry Pi ou au dépôt Boilerack. Aucun redémarrage,
> aucun rechargement, aucun déploiement. **Aucun changelog créé** — voir §8.

---

## 1. Constat

### 1.1 La section `🔁 Transactions` est devenue trompeuse en régime établi

Le corps Boiler partagé
[`18_lovelace/includes/cartes/systeme/boiler_corps.yaml`](../../../../18_lovelace/includes/cartes/systeme/boiler_corps.yaml)
expose, aux lignes 132–189, une section `🔁 Transactions` composée de quatre
paires `ACK / Timestamp`, une par rôle d'écriture :

| Rôle affiché | Statut ACK | Timestamp |
|---|---|---|
| ECS | `sensor.boiler_ack_dhw_set_setpoint_status` | `sensor.boiler_ack_dhw_set_setpoint_ts` |
| Chauffage | `sensor.boiler_ack_heating_set_temperature_status` | `sensor.boiler_ack_heating_set_temperature_ts` |
| Pente | `sensor.boiler_ack_heating_set_curve_slope_status` | `sensor.boiler_ack_heating_set_curve_slope_ts` |
| Décalage | `sensor.boiler_ack_heating_set_curve_shift_status` | `sensor.boiler_ack_heating_set_curve_shift_ts` |

Cette restitution est **structurellement fausse en régime établi**, pour deux
raisons cumulatives :

1. **Le Timestamp est mort.** Les quatre `*_ts` extraient le champ `ts` du
   payload d'ACK. Or l'écrivain souverain Boilerack **ne publie plus `ts`** :
   l'ACK est déterministe et sans horloge (`{request_id, status}`, plus `reason`
   / `reason_class` sur le seul cas `rejected`). Le fait est déjà **acté au
   contrat**, `consommation_ack.md` §4 : *« `sensor.*_ts` subsiste mais ne
   portera plus jamais de valeur. Il vaudra `unknown` en permanence. »* Les
   quatre cartes `Timestamp` affichent donc en permanence une absence de valeur.
2. **Le statut ACK est figé sur la dernière transaction historique.** Un
   `sensor.*_status` conserve la valeur du dernier ACK reçu, sans expiration ni
   corrélation à la commande courante. En dehors de la brève fenêtre
   d'exécution d'une transaction, la carte affiche donc un `Appliqué` **ancien**,
   dans un contexte visuel — une section intitulée « Transactions », adjacente à
   un Timestamp — qui invite à le lire comme un état courant.

La combinaison des deux produit la seule lecture réellement possible pour un
opérateur : *« la dernière commande a été appliquée, à une date inconnue »* —
énoncé qui n'informe sur rien, et dont la première moitié **peut être fausse**,
au sens où l'`Appliqué` lu ne décrit pas nécessairement la dernière commande
émise.

### 1.2 La section n'a pas de valeur opérationnelle durable

La restitution transactionnelle n'a de sens que **pendant** une transaction,
c'est-à-dire pendant une fenêtre de l'ordre de la vingtaine de secondes, à un
moment où l'opérateur n'est pas devant le dashboard. Hors de cette fenêtre,
elle n'a rien à restituer. Le diagnostic réellement utile — les erreurs et
leur cause — est déjà porté par la section voisine **Dernière erreur**
([`boiler_bloc_erreur_recente.yaml`](../../../../18_lovelace/includes/cartes/systeme/boiler_bloc_erreur_recente.yaml)),
horodatée par la réception Home Assistant.

### 1.3 Aucun contrat n'impose une restitution Lovelace des ACK

Vérifié : `mqtt_ack_ha.md` §10 (« UI — règles ») énonce une règle
**conditionnelle** — *si* un ACK est affiché, alors la correspondance
affichage ↔ état est celle du tableau §10.1, et les interdictions §10.2
s'appliquent. Ce paragraphe **n'oblige à afficher** ni les ACK, ni un
horodatage, ni une section dédiée. Supprimer la section ne viole donc aucune
obligation contractuelle : elle rend la règle §10 **sans objet** sur cette
surface, ce qui est une conformité et non une infraction.

### 1.4 Les projections `*_correlation` et `*_result` sont sans consommateur

Les quatre fichiers `12_template_sensors/boiler/boiler_ack_*_transaction.yaml`
définissent chacun **quatre** capteurs : `_request_id`, `_ts`, `_correlation`,
`_result`. Recherche exhaustive sur le dépôt (runtime YAML, scripts,
automatisations, checkers, dashboards) :

| Projection | Consommateurs runtime | Consommateurs UI | Verdict |
|---|---|---|---|
| `*_request_id` | **oui** — 4 scripts d'application + 4 automatisations de retry | non | **VIVANT — à conserver** |
| `*_ts` | **aucun** | 4 cartes de la section Transactions **uniquement** | **MORT dès la section retirée** |
| `*_correlation` | **aucun** — hors le `*_result` du même fichier | aucun | **MORT** |
| `*_result` | **aucun** | aucun | **MORT** |

Le point mérite d'être énoncé sans détour : **`*_result` n'est lu par aucun
script**, alors que `consommation_ack.md` §8 en fait la quatrième étape de sa
séquence normative et interdit d'utiliser `*_status` directement. Les quatre
exécuteurs réels — `10_scripts/ecs/appliquer_consigne_bridge.yaml`,
`10_scripts/chauffage/application_consigne.yaml`,
`10_scripts/chauffage/courbe_de_chauffe/application_pente.yaml`,
`10_scripts/chauffage/courbe_de_chauffe/application_parallele.yaml` — concluent
tous sur la conjonction **`*_status` ∧ (`*_request_id` == `request_id`
courant)**, c'est-à-dire sur la corrélation explicite que la dernière phrase du
§8 admet déjà comme équivalente. **La garantie contractuelle est tenue ; c'est
la formulation de la séquence qui est périmée.** C49 constate cet écart et le
solde au Lot 1 ; il ne l'a pas créé.

### 1.5 Le runtime transactionnel nécessaire est clairement séparé du legacy

| Objet | Statut | Motif |
|---|---|---|
| `sensor.boiler_ack_<role>_raw` | **conserver** | source brute unique de la chaîne ACK |
| `sensor.boiler_ack_<role>_status` | **conserver** | consommé par les 4 exécuteurs et les 4 retries |
| `sensor.boiler_ack_<role>_request_id` | **conserver** | porte la corrélation, seul invariant de succès |
| `sensor.boiler_ack_<role>_reason` | **conserver** | consommé (message d'échec) et affiché en « Dernière erreur » |
| `input_text.boiler_req_<role>` | **conserver** | référence transactionnelle écrite par les scripts |
| `binary_sensor.boiler_commandable_<role>` | **conserver** | garde composée d'exécution, en production (C48) |
| `sensor.boiler_ack_<role>_ts` (×4) | **supprimer** | ne portera plus jamais de valeur (contrat §4) |
| `sensor.boiler_ack_<role>_correlation` (×4) | **supprimer** | consommé par le seul `*_result`, lui-même mort |
| `sensor.boiler_ack_<role>_result` (×4) | **supprimer** | aucun consommateur, runtime ni UI |

---

## 2. Décision

1. **Supprimer intégralement la section `🔁 Transactions`** du corps Boiler
   partagé — en-tête de section comprise, soit les 4 `horizontal-stack` et leur
   `section_header`.
2. **Supprimer les 12 projections legacy** identifiées au §1.5, réparties sur
   les 4 fichiers `boiler_ack_*_transaction.yaml`.
3. **Ne pas remplacer `ts` par `last_changed` / `last_updated`.** Un horodatage
   de réception Home Assistant répondrait à la question « quand cette entité
   a-t-elle changé », jamais à « quand cette commande a-t-elle été appliquée ».
   Le substituer reconduirait exactement l'ambiguïté que ce chantier supprime,
   avec en plus l'apparence de la fraîcheur. **Refusé.**
4. **Ne pas toucher au runtime transactionnel utile** — les six familles
   « conserver » du §1.5 sont hors périmètre de toute suppression, à tous les
   lots.
5. **Ne pas supprimer le template partagé `boiler_info_timestamp`** : il reste
   utilisé par la carte **Heartbeat** (`sensor.boiler_bridge_heartbeat_timestamp`)
   et par le bloc **Dernière erreur**. Sa suppression serait une régression
   étrangère au périmètre.

---

## 3. Invariants à préserver

Opposables à **tout** lot de C49 :

- **INV-C49-1 — Corrélation `request_id`.** La règle de succès reste
  « `request_id` ACK == `request_id` courant **ET** `status == applied` ».
  Aucune projection retirée n'entre dans cette règle.
- **INV-C49-2 — ACK / status.** Les quatre `*_status` restent définis, publiés
  et lisibles, avec la même sémantique.
- **INV-C49-3 — Reason.** Les quatre `*_reason` restent définis et restent
  affichés dans la section « Dernière erreur ».
- **INV-C49-4 — Helpers de transaction.** Les quatre
  `input_text.boiler_req_<role>` sont inchangés — définition, écriture,
  libération.
- **INV-C49-5 — Commandabilité par rôle.** Les quatre
  `binary_sensor.boiler_commandable_<role>` et la garde composée d'exécution
  sont inchangés.
- **INV-C49-6 — Aucune commande chaudière impactée.** Aucun topic, payload,
  TTL, fenêtre d'attente, séquence d'exécution ou politique de retry n'est
  modifié. Le comportement observable de la chaudière est strictement
  identique avant et après C49.
- **INV-C49-7 — Aucun affaiblissement de garantie.** La suppression de
  `*_result` ne retire aucune garantie : la conclusion transactionnelle reste
  fondée sur une corrélation explicite, conformément à la clause d'équivalence
  déjà présente au §8 de `consommation_ack.md`.

---

## 4. Roadmap proposée

Ordre **contraignant** : la documentation précède l'UI, l'UI précède le
runtime. Retirer une projection avant d'avoir retiré son lecteur produirait une
entité indisponible en dashboard ; amender le contrat après coup ferait du
runtime la source de vérité, contre la doctrine « contrat avant runtime ».

### Lot 1 — Documentation / contrat *(préalable obligatoire)* — **LIVRÉ 2026-09-06**

> **Réalisé** : 1a, 1b, 1c (A-1 tranché, §5 supra), 1f, 1g amendés ;
> `contrats/boiler/README.md` doté d'un bloc de statut d'interface.
> **Zéro diff assumé** sur 1d (`mqtt_ack_ha.md` : contrat purement protocolaire,
> il ne nomme aucune projection) et sur le hub `navigation/domaines/boiler.md`
> (aucune mention de la section Transactions ni d'une projection).
> Aucun runtime, aucune UI, aucun checker touché.

| # | Action | Fichier |
|---|---|---|
| 1a | Retirer du §4 la décision de **conserver** `sensor.*_ts` (« l'entité n'est pas retirée — la retirer relèverait d'un lot de runtime, et celui-ci n'en est pas un ») et lui substituer la décision de suppression, en renvoyant à C49 | [`contrats/boiler/consommation_ack.md`](../../../contrats/boiler/consommation_ack.md) §4 |
| 1b | Documenter explicitement la suppression de `*_ts`, `*_correlation`, `*_result` : retirer `*_correlation` du tableau §5 et `*_result` des §6/§7, ou les marquer supprimés | `consommation_ack.md` §5, §6, §7 |
| 1c | Réécrire la séquence normative §8 sur le mécanisme **réellement** en vigueur (`*_status` ∧ corrélation `*_request_id`), et lever l'interdiction devenue contradictoire « NE PAS utiliser `*_status` directement ». **Arbitrage propriétaire requis** — voir §5, A-1 | `consommation_ack.md` §8 |
| 1d | Vérifier §10 (« UI — règles ») : la règle devient sans objet sur la surface Boiler après le Lot 2. À amender uniquement si elle prétend décrire une surface existante | [`contrats/boiler/mqtt_ack_ha.md`](../../../contrats/boiler/mqtt_ack_ha.md) §10 |
| 1e | Vérifier le README boiler et le hub de navigation du domaine | [`contrats/boiler/README.md`](../../../contrats/boiler/README.md) · [`navigation/domaines/boiler.md`](../../../navigation/domaines/boiler.md) |
| 1f | **Écart hors-boiler à solder** : le contrat ECS désigne `sensor.boiler_ack_dhw_set_setpoint_result` comme capteur ACK de référence et comme résultat lisible par l'appelant, alors que le script lit `*_status` + `*_request_id`. À réaligner dans le même lot, sous peine de laisser un contrat pointant une entité supprimée | [`contrats/ecs/application_consigne.md`](../../../contrats/ecs/application_consigne.md) lignes 59, 107, 149 |
| 1g | Mettre à jour le schéma de chaîne ACK (`sensor.*_request_id / ts` → `corrélation` → `sensor.*_result`) et la ligne « Templates transaction \| Corrélation » du tableau de séparation des couches | [`architecture/chauffage/interface_ha_boiler_bridge.md`](../../../architecture/chauffage/interface_ha_boiler_bridge.md) §3.4, §4 |

> Les changelogs `changelog/changelogs/v11/v11_beta*.md` mentionnant `*_result`
> sont des **sauvegardes de release** : ils décrivent un état passé et ne sont
> jamais réécrits.

### Lot 2 — UI — **LIVRÉ 2026-09-06**

> **Réalisé** : section `🔁 Transactions` retirée du corps partagé (58 lignes,
> en-tête de fichier réaligné) ; les 3 dashboards héritiers vérifiés — chacun
> n'inclut le corps qu'une fois, comme unique carte, aucune structure YAML
> touchée ; **A-2 tranché : `boiler_decision_ack` SUPPRIMÉ — ORPHELIN**, avec
> son README de famille réaligné. `boiler_info_timestamp` **conservé**
> (Heartbeat + « Dernière erreur »). Aucun runtime, contrat ou checker touché.

- Supprimer la section `🔁 Transactions` de
  [`boiler_corps.yaml`](../../../../18_lovelace/includes/cartes/systeme/boiler_corps.yaml)
  (bloc `SECTION — TRANSACTIONS`, `section_header` inclus).
- Vérifier les **3 dashboards héritiers** du corps partagé :
  `18_lovelace/dashboards/systeme/boiler.yaml`,
  `boiler_chauffage.yaml`, `boiler_ecs.yaml`. Aucun ne référence les entités
  directement (héritage par `!include` du corps commun) — à **confirmer** au
  lot, pas à présumer.
- Statuer sur le template `boiler_decision_ack`
  (`19_button_card_templates/40_dashboards/boiler/20_decision/`), dont la
  section supprimée est **l'unique consommateur** : suppression ou conservation
  explicitement motivée. Aucune suppression par effet de bord. → **A-2 tranché :
  supprimé**, avec son dossier `20_decision/` et le réalignement de
  [`README.md`](../../../../19_button_card_templates/40_dashboards/boiler/README.md).
- **Ne pas toucher** à `boiler_info_timestamp` (Heartbeat + Dernière erreur).

### Lot 3 — Runtime legacy — **LIVRÉ 2026-09-06, activation terrain confirmée**

> **Réalisé** : les 12 projections retirées des 4 `boiler_ack_*_transaction.yaml` ;
> chaque fichier ne déclare plus que `*_request_id`, dont le corps est inchangé
> — le diff n'ajoute **aucune ligne de logique**, uniquement des suppressions et
> la réécriture des en-têtes devenus faux. `*_status` / `*_reason`
> (`boiler_command_feedback.yaml`), `*_raw` (`14_mqtt_sensors/`), les helpers
> `input_text.boiler_req_*` et les gardes `binary_sensor.boiler_commandable_*`
> sont intouchés, de même que les 4 scripts exécutifs et les 4 automatisations
> de retry. T03 reste vert.
>
> **Activation** : le rechargement qui rend le retrait effectif côté Home
> Assistant a été fait au Lot 4, sous GO opérateur, et son effet est observé —
> voir la preuve terrain du Lot 4 et A-3 (§5).

> **Préalable A-4 : LEVÉ (2026-09-06).** T03 est ancré sur les scripts
> exécutifs et reste vert après retrait des 3 projections legacy — vérifié par
> simulation avant le patch, puis confirmé sur le patch réel.

- Retirer les 12 projections mortes des 4 fichiers
  `12_template_sensors/boiler/boiler_ack_*_transaction.yaml`.
- Conserver dans chacun `_request_id` ; ne pas toucher aux `_status` /
  `_reason`, définis ailleurs (`boiler_command_feedback.yaml`).
- L'attribut `ack_ts` du bloc `attributes` de `*_result` disparaît **avec** le
  capteur qui le porte ; mettre l'en-tête `🎯 RÔLE` de chaque fichier en
  cohérence (il annonce « extraction request_id / ts », « corrélation » et
  « conclusion exploitable par les scripts »).

### Lot 4 — Validation — **LIVRÉ 2026-09-06, PREUVE TERRAIN ACQUISE**

> **Verdict terrain : GO.** Aucun incident. Le retrait des 12 projections est
> effectif sur l'instance, sans effet fonctionnel d'aucune sorte.

**Geste effectué — un seul, ciblé.** *Outils de développement → YAML →
« Entités basées sur modèle »*, le **2026-09-06 à ≈ 13:33:25 locale
(≈ 11:33:25 UTC)**. **Aucun redémarrage**, aucun rechargement global, aucun
rechargement d'automatisations ni de scripts.

**Préconditions vérifiées avant le geste** : aucune transaction en vol — les 4
`input_text.boiler_req_<role>` vides —, dashboard Boiler stable, état des 24
entités relevé.

#### Preuve avant reload

| Objet | Constat |
|---|---|
| 12 projections legacy | **encore fournies** (définitions retirées du dépôt, instance pas encore rechargée — la divergence attendue) |
| `*_raw`, `*_status`, `*_reason`, `*_request_id` | présentes et cohérentes |
| 4 × `binary_sensor.boiler_commandable_<role>` | **`on`** |
| 4 × `input_text.boiler_req_<role>` | **vides** — aucune transaction active |
| Dashboard Boiler | propre, section `Transactions` absente (Lot 2) |

#### Preuve après reload

| Objet | Constat terrain |
|---|---|
| **12/12 projections legacy** | **`unavailable`, attribut `restored: true`** — Home Assistant indique explicitement qu'elles **ne sont plus fournies par l'intégration `template`** |
| `*_raw`, `*_status`, `*_reason`, `*_request_id` | **inchangées**, vivantes et cohérentes |
| 4 × `binary_sensor.boiler_commandable_<role>` | **`on`** — 4/4, gardes intactes |
| 4 × `input_text.boiler_req_<role>` | **toujours vides** |
| Automatisations de retry | **aucune déclenchée** |
| Commande chaudière | **aucune observée** |
| Dashboard Boiler | **propre** — pas de carte vide, pas d'`Inconnu` hérité, pas d'erreur de rendu ; Heartbeat et « Dernière erreur » corrects |
| Exception / erreur HA | **aucune** |

**L'attente posée au Lot 3 est confirmée par l'observation**, et elle l'est
dans sa forme exacte : les entrées de registre **survivent** en `restored`,
elles ne disparaissent pas. C'est le comportement nominal de Home Assistant
pour une entité à `unique_id` dont l'intégration cesse la fourniture.

**Le point de sûreté annoncé se vérifie** : le rechargement n'a déclenché
aucune commande chaudière ni aucun retry. Les 4 automatisations de retry sont
armées sur les helpers `input_text.boiler_req_<role>`, que le rechargement des
templates ne détruit pas ; `*_request_id` n'est lu qu'en condition, jamais en
déclencheur.

**Checkers** : verts au Lot 3 (#788) — `contracts` 87/87 en CI, dont T03 et son
`--selftest`, plus `doctrine`, `validate` (chargement de la configuration HA) et
`docs-lint`.

**Aucune entrée du registre d'entités n'a été supprimée** — voir A-3 (§5).

### Lot 5 — Clôture documentaire — **LIVRÉ 2026-09-06**

Revue des 14 critères du §7, un par un, sur pièces : **14/14 SATISFAITS**,
aucun non satisfait, aucun non applicable. Le détail des preuves est porté par
les lots eux-mêmes (commits/PR #784 à #789) et par les §1 à §7 du présent
document ; il n'est pas recopié ici, conformément à la règle « la source prime,
le registre n'analyse pas ».

**C49 est clos.**

---

## 5. Points à arbitrer par le propriétaire

Ouverts, non tranchés par cette ouverture :

- **A-1 — Formulation du §8 de `consommation_ack.md` (Lot 1c). TRANCHÉ le
  2026-09-06 : option (i), `*_result` est LEGACY SUPPRIMABLE.** Preuves
  opposables : (a) les 4 exécuteurs concluent tous sur `*_status` ∧
  (`*_request_id` == `request_id` courant), aucun ne lit `*_result` ; (b)
  `retry_transactionnel.md` §5.1 **normait déjà** `sensor.boiler_ack_*_status ==
  'timeout'` ET `request_id` corrélé — un contrat boiler frère codifiait donc
  l'interface réelle avant cet arbitrage ; (c) la dernière phrase du §8 v1.1
  admettait déjà l'équivalence ; (d) `*_result` **perd** une information que les
  scripts portent : il agrège sous `pending` l'absence d'ACK et l'ACK d'une
  transaction antérieure, là où les scripts distinguent l'ACK `timeout` corrélé
  du timeout local HA. L'option (ii) — recréer un consommateur — aurait donc
  dégradé la finesse de diagnostic pour un gain de sûreté nul. **Amendé en
  v1.2 ; aucun consommateur `*_result` créé.**
- **A-2 — Sort du template `boiler_decision_ack` (Lot 2). TRANCHÉ le
  2026-09-06 : SUPPRIMÉ — ORPHELIN.** Preuves : après retrait de la section,
  recherche exhaustive sur le dépôt entier — **zéro consommateur** (aucune
  carte, aucun include, aucun dashboard) ; les 95 dashboards déclarés sont
  **tous** en `mode: yaml`, donc le dépôt est l'autorité complète de la surface
  Lovelace et aucun consommateur masqué en `.storage` n'est possible ; les
  templates sont chargés par `!include_dir_merge_named`, le retrait d'un
  fichier n'affecte donc aucun chargement. **La sémantique n'est pas perdue** :
  `accepted ≠ succès` / `applied = succès` appartient aux contrats
  (`mqtt_ack_ha.md` §4/§10, `consommation_ack.md` §6–§8), non au template — la
  clause « aucune autre carte ne doit redéfinir cette sémantique » reste
  opposable à toute restitution future. `19_button_card_templates/40_dashboards/boiler/README.md`
  réaligné en conséquence (famille D marquée retirée, taxonomie et arbre).
- **A-3 — Retrait des 12 entités du registre HA. TRANCHÉ le 2026-09-06, sur
  preuve terrain : purge du registre = FACULTATIVE.**

  **Constat observé après le rechargement ciblé** (Lot 4) : les 12 entités sont
  **`unavailable` avec l'attribut `restored: true`**, Home Assistant indiquant
  explicitement qu'elles ne sont plus fournies par l'intégration `template`.
  Les entrées de registre **survivent** — elles ne disparaissent pas. C'est le
  comportement nominal pour une entité à `unique_id` dont l'intégration cesse
  la fourniture, et **l'attente posée au Lot 3 est confirmée dans sa forme
  exacte**.

  > **Correction d'une formulation antérieure.** La roadmap du Lot 4 annonçait
  > « 12 entités disparaissent du registre HA ». **C'est faux, et le terrain le
  > démontre** : elles y demeurent, à l'état `restored`. Seule la *fourniture*
  > cesse. La phrase est corrigée au Lot 4.

  **Verdict : FACULTATIVE.** Motifs :

  - **aucune dépendance fonctionnelle** — recensement exhaustif au Lot 3 :
    zéro consommateur, runtime comme UI ; le terrain le confirme (aucun retry,
    aucune commande, dashboard propre, gardes `on`) ;
  - **aucun effet runtime à les laisser** — une entrée `restored` n'a ni état
    exploitable, ni consommateur, ni déclencheur ;
  - **Home Assistant propose la suppression** dans *Paramètres → Appareils et
    services → Entités* : le geste est disponible, non requis ;
  - **les supprimer ne serait qu'un nettoyage cosmétique** — lisibilité du
    registre, rien d'autre.

  **La purge n'est PAS une condition** : ni du GO terrain, déjà prononcé, ni de
  la clôture fonctionnelle de C49. Elle reste à la seule main de l'opérateur,
  à tout moment, sans échéance opposable.

  **État à ce jour : aucune entrée supprimée.** Aucune session d'agent ne doit
  l'exécuter.
- **A-4 — `check_boiler_transactionnel_contracts.py` T03 (Lot 3). TRAITÉ le
  2026-09-06 — le Lot 3 n'est plus bloqué.** Constat d'origine, vérifié par
  simulation avant correction : Le test T03 vérifie que
  chaque `boiler_ack_*_transaction.yaml` **contient** la chaîne
  `boiler_req_<cmd>`, au motif « corrélation transactionnelle absente ». Il
  place donc la corrélation dans la **couche template**, alors que le §5 amendé
  (v1.2) la situe dans les **scripts exécutifs** — où elle est réellement
  évaluée. Aujourd'hui la chaîne apparaît 4 fois par fichier : 1 commentaire
  d'en-tête, `*_correlation`, l'état de `*_result` et son attribut
  `request_id_en_cours`. **Après le Lot 3, il n'en reste que le commentaire
  d'en-tête** : T03 passerait **vacuement**, sur un commentaire — et virerait au
  **rouge** si l'en-tête est remis en cohérence comme le Lot 3 le prévoit.
  **Correction retenue — ancrer T03 là où la garantie vit.** T03 vérifie
  désormais, **pour les 4 rôles et sur leur script exécutif**, six propriétés :
  la projection `sensor.boiler_ack_<role>_request_id` est déclarée (seule
  dépendance subsistante à la couche template, et elle survit au Lot 3) ; le
  script la lit (C1) ; il la compare au `request_id` courant (C2) ; il lit
  `*_status` (C3) ; il ne conclut pas via `*_result` (C4) ; **au moins une
  expression Jinja conjugue statut et corrélation** (C5) ; et surtout
  **aucune expression concluant au succès `applied` n'est dépourvue de la
  corrélation** (C6) — l'invariant de sûreté, pas une simple présence.
  Les commentaires sont retirés avant analyse et l'unité d'évaluation est
  l'expression `{{ … }}`, non le fichier : un identifiant cité en commentaire,
  ou une corrélation située dans un bloc sans rapport, ne peuvent plus valider
  quoi que ce soit. Le checker porte un `--selftest` (convention du dépôt,
  lancé par `scripts/ci/run_checkers.py` avant le checker lui-même) couvrant
  les cas N1 à N5 et deux faux positifs à éviter ; **5 mutations du cœur de
  T03 sur 5 le font virer au rouge**, preuve que ces auto-tests ne sont pas
  vacués à leur tour.
  **Simulation du Lot 3, avant de l'exécuter** : projections `*_ts` /
  `*_correlation` / `*_result` retirées des 4 fichiers, dans les deux variantes
  (en-tête conservé, en-tête nettoyé). L'ancien T03 passait **vert vacuement**
  dans la première et **rouge** dans la seconde ; le nouveau T03 est **vert
  dans les deux**, et rouge dès que la corrélation des scripts est atteinte.
  **Le Lot 3 est donc déblocable sans faux vert ni faux rouge.**

---

## 6. Ce que cette ouverture fait, précisément

- Crée le présent document.
- Ajoute la ligne **C49** à `REGISTRE_CHANTIERS.md`, section ① Actifs.
- Ajoute l'entrée correspondante à `audits/index.md`.
- Ne modifie **aucun** autre document, contrat, fichier UI ou runtime.
- N'exécute **aucun** des lots 1 à 5.

---

## 7. Critères de clôture de C49

Le chantier est déclarable clos quand — **revue du Lot 5, 2026-09-06 :
14/14 SATISFAITS, sur pièces (§10)** :

1. la section `🔁 Transactions` n'existe plus dans le corps Boiler partagé ;
2. les 3 dashboards héritiers sont vérifiés propres, sans entité indisponible ;
3. les 12 projections `*_ts` / `*_correlation` / `*_result` n'existent plus
   dans les 4 fichiers `boiler_ack_*_transaction.yaml` ;
4. les 4 `*_request_id` y subsistent, inchangés ;
5. `consommation_ack.md` ne prescrit plus de conserver `*_ts` et ne décrit plus
   `*_correlation` / `*_result` comme existants ;
6. la séquence normative §8 décrit le mécanisme réellement en vigueur (A-1
   tranché) ;
7. `contrats/ecs/application_consigne.md` ne pointe plus une entité supprimée ;
8. `interface_ha_boiler_bridge.md` décrit la chaîne ACK réelle ;
9. aucun horodatage de substitution (`last_changed` / `last_updated`) n'a été
   introduit ;
10. les 7 invariants du §3 sont vérifiés — en particulier INV-C49-6, prouvé par
    l'absence de diff sur les 4 exécuteurs et les 4 automatisations de retry ;
11. les checkers du Lot 4 sont verts — **fait** (87/87 en CI, #788) ;
11 bis. la **preuve terrain** du retrait est acquise : les 12 projections ne
    sont plus fournies, les familles conservées et les 4 gardes sont
    intactes, aucun retry ni commande chaudière déclenchés — **fait**
    (Lot 4, 2026-09-06) ;
12. le sort du template `boiler_decision_ack` est tranché et écrit (A-2) — **fait** ;
13. la traçabilité repose sur le registre et les commits/PR, **sans changelog
    fabriqué** (§8).

---

## 8. Changelog — non créé, par doctrine

Conformément à
[`architecture/03_doctrines/redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md)
§1 : *« Ne jamais fabriquer ni numéroter un changelog de sa propre initiative
pour acter un changement […]. Hors du déclenchement [dépôt de diffs de release
par l'opérateur], un changement livré se trace via le commit de merge / la PR
dans les contrats et la ligne de clôture du registre, jamais via un changelog
inventé. »*

**Aucun changelog n'est créé par C49, à aucun de ses lots**, sauf déclenchement
explicite de la procédure standard par l'opérateur (dépôt de diffs dans
`changelog/diffs_temporaires/` + demande de rédaction).

---

## 9. Interdictions (opposables à tout lot futur de C49)

Aucune modification des 4 scripts d'application · aucune modification des 4
automatisations de retry · aucun horodatage de substitution · aucune
suppression de `boiler_info_timestamp` · aucune suppression de `*_raw`,
`*_status`, `*_request_id`, `*_reason`, des helpers `input_text.boiler_req_*`
ou des `binary_sensor.boiler_commandable_*` · aucune modification du dépôt
Boilerack · aucun accès au Raspberry Pi · aucune exécution de lot C48 · aucun
nouvel identifiant de chantier · aucun nettoyage cosmétique opportuniste ·
aucun changelog fabriqué.

---

## 10. Clôture — C49 CLOS le 2026-09-06

**Ce que le chantier a fait, en six lignes :**

- la section Lovelace `🔁 Transactions` est **supprimée**, sans remplacement ;
- les **12 projections ACK legacy** (`*_ts`, `*_correlation`, `*_result` × 4
  rôles) sont **supprimées** du runtime ;
- le checker **T03 est réaligné** sur les scripts exécutifs, où la corrélation
  est réellement évaluée, et porte des auto-tests ;
- la suppression est **validée terrain** (2026-09-06, ≈ 13:33:25 locale) ;
- la **purge du registre d'entités HA reste facultative**, et n'a jamais été
  une condition de clôture ;
- **aucun impact transactionnel ni chaudière** : les 4 exécuteurs et les 4
  automatisations de retry sont **strictement inchangés** sur toute la durée du
  chantier, la surface MQTT est intacte.

**Traçabilité** — six PR, aucun changelog fabriqué (§8) : ouverture #784 ·
Lot 1 contrat #785 · Lot 2 UI #786 · A-4 checker #787 · Lot 3 runtime #788 ·
Lot 4 terrain #789 · Lot 5 clôture (présent commit).

**Arbitrages, tous tranchés** : A-1 (`*_result` legacy supprimable) · A-2
(`boiler_decision_ack` supprimé, orphelin) · A-3 (purge du registre
facultative) · A-4 (T03 réancré sur les scripts exécutifs).

**Ce que la clôture n'absorbe pas.** La purge du registre d'entités HA reste
disponible à l'opérateur, sans échéance opposable. **C48 n'est pas touché** —
il poursuit son propre cours. Aucune autre dette n'est reprise ni éteinte par
C49.

> **Dernier alignement, fait à la clôture.** Le paragraphe de clôture du §11 de
> [`consommation_ack.md`](../../../contrats/boiler/consommation_ack.md) avait
> été écrit au Lot 1, avant l'exécution des Lots 2 et 3 : il énonçait encore le
> retrait comme seulement *autorisé*, et la section Lovelace `Transactions`
> comme lecteur subsistant de `*_ts`. Les faits l'avaient dépassé. Le §11
> **constate désormais** que les trois familles legacy ont été retirées du
> runtime par C49 et que le retrait a été validé terrain. **Sa règle normative
> est inchangée** : la table qualifie les mêmes statuts, et `*_status` +
> `*_request_id` demeure l'interface consommée canonique. **Aucun résidu
> documentaire ne reste ouvert.**

---

## 11. Renvois

- Consommation des ACK (contrat propriétaire) :
  [`contrats/boiler/consommation_ack.md`](../../../contrats/boiler/consommation_ack.md)
- Contrat MQTT ACK HA :
  [`contrats/boiler/mqtt_ack_ha.md`](../../../contrats/boiler/mqtt_ack_ha.md)
- Socle transactionnel :
  [`contrats/boiler/socle_transactionnel.md`](../../../contrats/boiler/socle_transactionnel.md)
- Retry transactionnel :
  [`contrats/boiler/retry_transactionnel.md`](../../../contrats/boiler/retry_transactionnel.md)
- Application de consigne ECS :
  [`contrats/ecs/application_consigne.md`](../../../contrats/ecs/application_consigne.md)
- Interface HA ↔ boiler :
  [`architecture/chauffage/interface_ha_boiler_bridge.md`](../../../architecture/chauffage/interface_ha_boiler_bridge.md)
- Migration Boiler Bridge → Boilerack :
  [`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)
- Chantier C48 (convergence documentaire, disjoint) :
  [`c48_convergence_documentaire_boilerack.md`](c48_convergence_documentaire_boilerack.md)
- Hub de navigation du domaine :
  [`navigation/domaines/boiler.md`](../../../navigation/domaines/boiler.md)
- Doctrine changelog :
  [`architecture/03_doctrines/redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md)
- Registre des chantiers :
  [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
