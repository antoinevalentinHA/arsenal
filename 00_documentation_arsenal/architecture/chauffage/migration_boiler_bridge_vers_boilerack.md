# ARSENAL — Cadrage de migration Boiler Bridge → Boilerack

## Lot 0 — contrat avant code

| Champ | Valeur |
|---|---|
| **Version** | v6 |
| **Statut** | Cadrage — normatif pour le Lot 1 ; **§12 et §13 consignent deux épreuves terrain** |
| **Portée** | Recâblage des consommateurs Home Assistant du bus MQTT chaudière |
| **Complète** | `interface_ha_boiler_bridge.md` — qu'il **ne remplace pas encore** |

> **AMENDÉ — le Lot 1 est intégré et la chaîne d'écriture est éprouvée.**
> Le cadrage demeure inchangé : aucun contrat, aucun mapping, aucune décision
> n'est révisé. Le §12 consigne l'épreuve terrain A-5, sur le seul rôle
> `dhw_setpoint`.
>
> **Ce que le terrain change au §10, sans amalgame :**
>
> | | Portée exacte |
> |---|---|
> | **§10.3** helper transactionnel | **LEVÉE** |
> | **§10.5** budget de confirmation / attente | **CONFRONTÉE seulement** — la réserve quantitative est **MAINTENUE** |
> | **§10.6** préfixe déployé | **valeur observée et corroborée** — l'exigence de revérification est **MAINTENUE** |
>
> Une seule réserve du §11 est levée, la troisième, et **pour les seuls rôles
> éprouvés**. Le §13 consigne l'épreuve A-6, sur `heating_setpoint`.
> **`heating_curve_shift` et `heating_curve_slope` demeurent non éprouvés en
> écriture.**

---

## 1. Objet, et ce que ce document n'est pas

Le pont historique est **arrêté et désactivé** ; **Boilerack** est l'écrivain
souverain côté chaudière. Les consommateurs Home Assistant, eux, sont **toujours
câblés sur l'arbre `boiler/`**, dont les topics sont **retenus** : ils affichent
donc des valeurs figées, et le garde de commandabilité refuse toute émission.

**Ce document fige le contrat de migration.** Il ne modifie **aucun** capteur,
script, garde, tableau de bord ni CI.

> **Boilerack est une SOURCE DE VÉRITÉ EXTERNE, et rien d'autre.** Le présent
> chantier est un chantier **consommateur**, il siège dans Arsenal, et son
> cadrage aussi. Aucune décision Arsenal n'est prise ailleurs, et aucune
> obligation n'est créée pour Boilerack.

---

## 2. Préfixes et topics — **ce que le code garantit, et ce que la config décide**

### 2.1 La distinction, et pourquoi elle n'est pas cosmétique

Boilerack **ne fixe pas** son préfixe de lecture : il le **configure**.

| | Valeur | Nature |
|---|---|---|
| **Défaut du CODE** | **`boiler`** | contractuel, dans `ReadSurfaceConfig` — **le même arbre que le pont historique** |
| **Racine unique** | `read_surface.prefix` | **une seule racine, pour les TROIS surfaces** |
| **Lecture** | `<racine>/telemetry/…`, `<racine>/bridge/…` | dérivée de la racine |
| **Commande** | `<racine>/command` | **dérivée de la racine, au runtime** |
| **Acquittements** | `<racine>/ack/<role>` | **dérivée de la racine, au runtime** |

### 2.2 La chaîne d'appel réelle — **et c'est elle qui fait autorité**

**Dans le runtime réellement composé, `read_surface.prefix` dérive les TROIS
surfaces** : la lecture, `<prefix>/command`, et `<prefix>/ack/<role>`.

**Chaîne suivie de bout en bout, du point d'entrée au topic injecté :**

```
load_config                      charge read_surface.prefix
      |                          et REFUSE command_topic / ack_topic_prefix
      v                          comme cles utilisateur
build_runtime                    applique la fabrique transactionnelle
      v
_composer_transaction            rend la fermeture qui construira la surface
      v
_config_mqtt_transactionnelle    racine = config.read_surface.prefix
      |                          command_topic     = <racine>/command
      |                          ack_topic_prefix  = <racine>/ack
      v
build_transaction_surface        lit command_topic et ack_topic_prefix
                                 sur le MqttConfig DERIVE qu'il recoit
```

**Exercé sur le code installé, chaîne complète, client factice, sans réseau :**

```
prefix = boiler     ->  TransactionSurface.command_topic = boiler/command
                        moteur ack prefix                = boiler/ack
prefix = boilerack  ->  TransactionSurface.command_topic = boilerack/command
                        moteur ack prefix                = boilerack/ack
prefix = autre      ->  autre/command   ·   autre/ack
```

> **UN CHANGEMENT DE `read_surface.prefix` DÉPLACE LES TROIS SURFACES ENSEMBLE.**
> Lecture, commande et acquittements partent **d'un bloc**. Il n'existe **aucun
> réglage indépendant** de la commande ou des ACK.

### 2.3 Défauts structurels ≠ valeurs injectées au runtime

| | Valeur | Portée |
|---|---|---|
| **Défauts structurels de `MqttConfig`** | `boilerack/command`, `boilerack/ack` | **jamais atteignables par la configuration** : le chargeur **refuse** ces deux clés, *« hors surface utilisateur »*. Ils servent à bâtir une configuration de test sans composition |
| **Valeurs injectées au runtime** | `<prefix>/command`, `<prefix>/ack` | produites par **`_config_mqtt_transactionnelle`**, et **remplaçant systématiquement** les défauts ci-dessus avant que la surface ne soit construite |

> **Les deux coïncident AUJOURD'HUI**, parce que la configuration déployée porte
> `prefix = "boilerack"` : le défaut structurel vaut `boilerack/command`, et la
> dérivation aussi. **Aucune observation en production ne peut donc les
> départager** — seule une racine différente les sépare, et c'est ce qui a été
> exercé.
>
> **Lire les défauts structurels comme des topics fixes serait une erreur de
> niveau**, et elle serait invisible tant que le préfixe ne bouge pas.

> **La précondition « préfixe » N'EST donc PAS levée par le dépôt Boilerack.**
> Elle ne peut l'être que par la configuration de l'instance visée.

### 2.4 Fait terrain — l'instance déployée

| | |
|---|---|
| **Source** | fichier de configuration déployé sur la machine, section `[read_surface]` |
| **Valeur** | `prefix = "boilerack"` |
| **Corroboration 1** | topics composés par le **service installé** : `boilerack/telemetry/…`, `boilerack/bridge/online`, `boilerack/bridge/telemetry_status`, `boilerack/bridge/heartbeat`, `boilerack/command`, `boilerack/ack` |
| **Corroboration 2** | **treize topics observés en direct** sur le courtier, tous sous `boilerack/` |
| **Commentaire d'origine** | *« préfixe DISTINCT de celui du pont historique »* |

> **C'est un fait de configuration déployée, à une date donnée — pas une vérité
> du code.** Le Lot 1 doit le **revérifier au moment d'agir**, et non le tenir
> d'ici. **Un changement de cette clé déplacerait les trois surfaces à la fois**,
> et un recâblage Arsenal figé sur `boilerack/` deviendrait muet **sans aucun
> message d'erreur** : les topics existeraient toujours, simplement ailleurs.

**Valeurs retenues pour la suite du présent cadrage**, sous cette réserve :
lecture `boilerack/telemetry/…`, commande **`boilerack/command`**,
acquittements **`boilerack/ack/<role>`**.

### 2.5 Arbitrage d'audit — la question est close

Une divergence a opposé deux lectures : **A**, la racine de lecture dérive la
commande et les ACK ; **B**, lecture et transaction seraient deux autorités
indépendantes, la commande restant sur les défauts structurels.

**Elle a été tranchée en lecture seule**, par **suivi complet de la chaîne
d'appel** du point d'entrée jusqu'au topic injecté, puis par **exercice de la
fabrique transactionnelle** sur le code installé, avec un client factice.
**Les huit fichiers de la chaîne sont byte-identiques entre le dépôt et
l'installation** — la même réponse vaut donc des deux côtés.

> **`A` est ÉTABLI. `B` est écarté.** **Aucune ambiguïté résiduelle ne subsiste**,
> et le présent document ne doit pas en réintroduire.

---

## 3. `chain.status`, `chain.cause`, `last_result` — trois notions, jamais mêlées

Publiées dans `<racine>/bridge/telemetry_status`, retenu.

| Notion | Portée | Valeurs |
|---|---|---|
| **`chain.status`** | **synthèse de la chaîne de lecture** | **`ok`** · **`degraded`** · **`unavailable`** — **trois états, pas davantage** |
| **`chain.cause`** | **cause transport détaillée**, quand applicable | `daemon_unreachable` · `unsupported_command` · `timeout` · `unusable_output` · `transport_error` — **`null` si et seulement si `status` vaut `ok`** |
| **`last_result`** | **par mesure**, indépendant de la synthèse | **le MÊME vocabulaire public**, plus `ok` : `ok` · `daemon_unreachable` · `unsupported_command` · `timeout` · `unusable_output` · `transport_error` |

> **Aucune des trois ne se substitue aux autres.** `chain.status` dit *à quel
> point* la chaîne va ; `chain.cause` dit *pourquoi* ; `last_result` dit *ce
> qu'a donné la dernière tentative d'une mesure précise*. Les confondre
> produirait un diagnostic faux.

### 3.1 Le vocabulaire publié est une PROJECTION, jamais l'état interne

`chain.cause` et `last_result` passent tous deux par la **même projection
publique**. L'état interne `unknown_command` y est projeté en
**`unsupported_command`**.

> **`unknown_command` n'apparaît JAMAIS sur le fil.** C'est un état interne du
> transport, et rien d'autre.
>
> **Le contrat Arsenal MUST matcher la projection publique, jamais les états
> internes.** Un gabarit comparant à `unknown_command` ne s'apparierait à aucune
> valeur émise, et échouerait en silence — sans erreur, sans trace, sans jamais
> se déclencher.

Chaque mesure porte en outre `age_s`, `fresh`, `has_value`, `last_success`.
**`fresh` est normatif** : `age_s ≤ fresh_max`, borne incluse, avec
`fresh_max = 3 × période`.

---

## 4. Mapping de lecture — **ce qui existe réellement côté Arsenal**

### 4.1 Les huit entités à re-sourcer

**Établi par relevé exhaustif des `state_topic` des capteurs MQTT du domaine.**

| Topic consommé aujourd'hui | Topic Boilerack |
|---|---|
| `boiler/telemetry/temperatures/supply` | `boilerack/telemetry/temperatures/supply` |
| `boiler/telemetry/temperatures/dhw` | `boilerack/telemetry/temperatures/dhw` |
| `boiler/telemetry/dhw/setpoint` | `boilerack/telemetry/dhw/setpoint` |
| `boiler/telemetry/heating/setpoint` | `boilerack/telemetry/heating/setpoint` |
| `boiler/telemetry/heating/curve/slope` | `boilerack/telemetry/heating/curve/slope` |
| `boiler/telemetry/heating/curve/shift` | `boilerack/telemetry/heating/curve/shift` |
| `boiler/telemetry/burner/modulation` | `boilerack/telemetry/burner/modulation` |
| **`boiler/telemetry/burner/state`** | **`boilerack/telemetry/burner/state`** — **change de forme, §4.3** |

**Plus deux topics de service** : `boiler/bridge/online` → `boilerack/bridge/online`
et `boiler/bridge/heartbeat` → `boilerack/bridge/heartbeat`
(**QoS 0, NON retenu**, période 30 s).

### 4.2 Disponibles chez Boilerack, **sans entité Arsenal**

| Topic Boilerack | Statut |
|---|---|
| `boilerack/telemetry/temperatures/outdoor` | **aucune entité Arsenal ne le consomme** |
| `boilerack/telemetry/heating/reduced_reference` | **aucune entité Arsenal ne le consomme** |

> **Leur création éventuelle est un ARBITRAGE ULTÉRIEUR, pas du recâblage.**
> Le Lot 1 **ne les crée pas**. Créer une entité qui n'existait pas serait
> ajouter une capacité sous couvert de migration.

### 4.3 La seule différence de forme à traiter

| | Pont historique | Boilerack |
|---|---|---|
| `burner/state` | chaîne **`on` / `off`** | **scalaire `0.0` / non-nul** — projection binaire de la modulation |

Les valeurs numériques passent par ailleurs de `10.000000` à la **forme courte**
`10.0`. **Aucune autre différence de forme n'est connue.**

### 4.4 Ce qui n'est PAS un manque

`comfort_temperature`, `reduced_temperature`, `program` sont publiés par le pont
historique et **absents de Boilerack** — mais **aucune entité Arsenal vivante ne
les consomme**, relevé exhaustif à l'appui.

> **Ce n'est donc ni une perte, ni une inconnue.** Le noter comme tel serait
> inventer un problème.

---

## 5. Nommage — substitution en place

| Règle | Motif |
|---|---|
| **Aucun capteur double**, même transitoire | deux capteurs vivants pour une même grandeur créeraient une ambiguïté d'autorité |
| **Les `entity_id` sont CONSERVÉS**, seul le `state_topic` change | ils sont référencés par les scripts, les groupes, les synthèses et l'UI |
| **Aucun renommage cosmétique** | `boiler_*` nomme le **domaine**, pas le service. Un renommage est un lot séparé, ultérieur, optionnel |
| **Les entités sans équivalent sont RETIRÉES** | un capteur pointant un topic mort garde sa **dernière valeur retenue** et ment en silence |

> **Le dernier point est le principal risque du chantier.** Les topics `boiler/…`
> sont retenus : un capteur oublié n'affichera pas « indisponible », mais **une
> valeur plausible et fausse**.

---

## 6. Renoncements — et un faux renoncement

| | Entité Arsenal existante | Décision |
|---|---|---|
| **`bridge/version`** | oui | **RENONCÉ** — Boilerack n'en publie pas. Entité retirée |
| **`bridge/vcontrold_status`** | oui | **RENONCÉS comme couple.** Remplacés par `chain.status` + `chain.cause`. **La granularité change de nature** : on ne distingue plus « démon » et « liaison optique », on qualifie **la chaîne**, avec sa cause |
| **`bridge/optolink_status`** | oui | idem |
| **`error/last`** | oui | **RENONCÉ** — hors périmètre de la surface Boilerack. Remplacé par `last_result` **par mesure** et par le `reason` des ACK rejetés |
| **`ts` natif dans l'ACK** | — | **RENONCÉ.** L'ACK Boilerack est déterministe et sans horloge. Corrélation sur le **seul `request_id`** ; l'horodatage est celui de la réception Arsenal |
| **`guard/*`** | oui, quatre entités | **CE N'EST PAS UN RENONCEMENT.** Le superviseur publie toujours `boiler/guard/status`, `last_action`, `last_run`, `version` — **surface vivante, inchangée, observée en `v1.2`**. Elle n'appartient pas à Boilerack. **Rien à faire, et surtout rien à retirer.** |

---

## 7. Garde de commandabilité

### 7.1 Pourquoi `online` ne suffit pas

Le code de Boilerack l'énonce lui-même : **aucune politique de reconnexion n'est
implémentée**. Après une déconnexion inattendue, le testament fait passer le
retenu `bridge/online` à `offline` ; **si la bibliothèque se reconnecte seule, le
composant ne le voit pas**, et le retenu **restera `offline` alors que le service
est vivant**, jusqu'au prochain démarrage.

> **Un garde fondé sur `online` seul produirait un refus DURABLE sur un service
> parfaitement vivant.** Faux négatif permanent, pas incident.

### 7.2 Composition proposée — **quatre conditions, toutes contractuelles**

**Commandable si et seulement si :**

| # | Condition | Signal |
|---|---|---|
| **1** | `<racine>/bridge/online` vaut `online` | **nécessaire, jamais suffisant** — un `offline` franc reste un refus légitime |
| **2** | `telemetry_status.ts` récent au regard de l'heure Arsenal | le topic est **retenu** : sans ce contrôle, un instantané figé passerait pour vivant |
| **3** | `telemetry_status.chain.status == "ok"` | ni `degraded`, ni `unavailable` |
| **4** | `telemetry_status.measurements[<role>].fresh == true` | **booléen normatif**, rien à inventer |

Le **heartbeat** — non retenu, 30 s — est un second signal de vivacité utilisable
en appui de la condition 2.

> **Les seuils d'âge des conditions 1 et 2 ne sont PAS fixés ici.** Le contrat
> donne la période et l'instant, **pas une tolérance**. **Le Lot 1 les décidera
> explicitement, et les écrira comme des décisions**, jamais comme des évidences.

### 7.3 Ce que le garde ne fait pas

Il **autorise l'émission**, il **ne conclut pas la transaction**. **Seul `applied`
corrélé au même `request_id` vaut succès.** À confronter : **budget de
confirmation Boilerack `5,0 s`** contre **attente Arsenal `15 s`** — jamais
confrontés en régime réel.

---

## 8. `binary_sensor.boiler_bridge` — **conservé**

**Ce n'est pas un capteur MQTT.** Il n'est défini dans **aucun YAML** : entité de
l'intégration `ping`, créée par l'interface, référencée par les deux groupes de
ping et par la synthèse de connectivité, aux côtés d'entités ping homogènes.

> **Il mesure la joignabilité ICMP de la machine**, laquelle n'a pas changé et
> héberge toujours Boilerack. **Indépendant du transport MQTT**, donc indifférent
> au recâblage. **Ni renommé, ni déplacé, ni retiré.**
>
> **Réserve** : sa cible exacte n'est pas vérifiable depuis le dépôt.

---

## 9. Périmètre du Lot 1 — minimal

**DANS le périmètre :**

1. **re-sourcer les huit entités de télémétrie réellement existantes**, plus
   `bridge/online` et `bridge/heartbeat`, en **conservant les `entity_id`** ;
2. **adapter `burner/state`** à sa forme scalaire, et les valeurs numériques
   courtes ;
3. **introduire `telemetry_status`** — sans équivalent legacy — et **le garde du
   §7**, seuils inclus et **écrits comme décisions** ;
4. **retirer** les entités sans équivalent : `bridge/version`,
   `bridge/vcontrold_status`, `bridge/optolink_status`, `error/last` ;
5. **commande et acquittements : SEULEMENT si le cadrage Arsenal l'autorise
   explicitement.** À défaut, le Lot 1 s'arrête à la lecture et au garde.

**HORS périmètre, et à ne pas anticiper :**

- **créer `outdoor` ou `reduced_reference`** — arbitrage ultérieur ;
- les **retries** transactionnels ;
- l'**interface** et les tableaux de bord ;
- la **CI** ;
- **Boilerack**, en quoi que ce soit ;
- tout **renommage** d'entité ;
- le **superviseur** et sa surface `guard/*` ;
- le **message retenu** historique sur la surface de commande.

---

## 10. Inconnues restantes

1. **La cible ICMP exacte** de `binary_sensor.boiler_bridge` — définie hors YAML.
2. **Les seuils d'âge** des conditions 1 et 2 du garde.
3. ~~**L'état résiduel** du helper transactionnel `input_text.boiler_req_*`~~ —
   **LEVÉE par A-5** : le `PRECHECK` a été franchi, le helper ancré puis libéré,
   sur **trois exécutions consécutives** du script. Voir §12.
4. **Le sort du message retenu** historique sur la surface de commande : le pont
   étant arrêté, il ne déclenche rien ; le traiter serait une décision propre.
5. ~~**Le budget de confirmation `5,0 s` contre l'attente `15 s`** — jamais
   confrontés en régime réel.~~ — **CONFRONTÉS par A-5**, et sans conflit :
   l'acquittement terminal est parvenu dans la fenêtre d'attente. **Un seul
   échantillon ne caractérise pas la marge** : la réserve quantitative demeure.
   Voir §12.
6. **La valeur de `read_surface.prefix` au moment d'agir** — fait de
   configuration, à revérifier, jamais à supposer. Relevée en source primaire
   avant le Lot 1 : `boilerack`. **L'exigence de revérification demeure** — elle
   vaut pour chaque mutation, non une fois pour toutes.

---

## 11. Réserves conservées

1. **Les topics legacy sont RETENUS.** Toute entité non traitée conservera une
   valeur plausible et fausse. C'est le principal risque du Lot 1.
2. **La limite de reconnexion de Boilerack n'est pas corrigée** par ce chantier :
   elle est **contournée** par le garde. La corriger relèverait de Boilerack.
3. ~~**Aucune capacité de production n'est revendiquée** : ce document fige un
   contrat, il ne l'éprouve pas.~~ — **LEVÉE pour DEUX rôles sur quatre** :
   `dhw_setpoint` par A-5 (§12), `heating_setpoint` par A-6 (§13). La chaîne
   Arsenal → Boilerack → chaudière est éprouvée de bout en bout, écriture réelle
   comprise, par **deux chemins d'appel distincts**.
   **`heating_curve_shift` et `heating_curve_slope` demeurent NON ÉPROUVÉS en
   écriture.**

---

## 12. Épreuve terrain A-5 — la chaîne d'écriture, de bout en bout

> **Une exécution unique, autorisée nommément, sur le seul rôle `dhw_setpoint`.**
> Elle éprouve ce que les Lots 0 à 1-TER n'avaient que contractualisé.

### 12.1 Ce qui a été exécuté

**TROIS exécutions du script exécutif, non deux** — l'aller, puis les deux
tentatives du garde. Le garde appelle en effet le script une première fois,
patiente dix secondes, puis le rappelle si l'incohérence persiste.

| # | Origine | Valeur émise | Constat |
|---|---|---|---|
| **1** | épreuve A-5, aller | **11** | acquittement **`applied`**, corrélé au bon `request_id` ; consigne **11 observée** sur la chaudière, relecture télémétrique à l'appui |
| **2** | garde hors cycle, tentative 1 | **10** | le garde a détecté la consigne hors cycle et réimposé 10 **par le même script exécutif** |
| **3** | garde hors cycle, tentative 2 | **10** | second appel du garde, après sa temporisation de dix secondes |
| — | — | — | **retour télémétrique à 10 confirmé** |

**La restauration n'a demandé aucun geste manuel.** Le garde métier a refermé la
boucle de lui-même — c'est un résultat en soi : la chaîne d'écriture est
opérante, et le dispositif de correction hors cycle l'est aussi.

**Une seule écriture était autorisée ; trois ont eu lieu.** Les deux suivantes
sont le fait du garde, non de l'opérateur : c'est son comportement nominal, et
il est consigné ici pour que le compte soit exact.

**Valeur choisie sans effet de confort** : le ballon était très au-dessus de la
consigne, aucune demande de chauffe n'a été créée par le pas de +1 °C.

### 12.2 Ce que cette épreuve établit

1. La chaîne **Arsenal → `boilerack/command` → chaudière → `boilerack/ack/<role>`
   → Arsenal** fonctionne de bout en bout, écriture réelle comprise.
2. Le **payload à six champs**, `role` compris, est accepté par la surface amont.
3. La **corrélation stricte sur `request_id`** conclut correctement.
4. Le **`PRECHECK`** — garde composée et helper vide — laisse passer une
   transaction légitime, et le helper est libéré en fin de transaction.
5. Le **garde métier hors cycle** agit sur la nouvelle surface sans retouche.

### 12.3 Une alerte levée, et pourquoi elle était fausse

Une réutilisation apparente du `request_id` entre l'aller et la seconde tentative
du garde a été signalée, puis **écartée** : il s'agissait d'une **mauvaise
corrélation lors d'une lecture tardive du capteur d'acquittement**.

**Le mécanisme mérite d'être consigné, car il se reproduira.**

`boilerack/ack/<role>` est publié en **QoS 1 et NON retenu**. Ce n'est pas une
supposition : le fait est lu en **source primaire** dans le code de l'écrivain
souverain — `core/engine.py`, constantes `_ACK_QOS = 1` et
`_ACK_RETAIN = False`, employées à l'appel de publication de la même unité — et
**corroboré sur le code réellement installé**, où les deux constantes portent ces
valeurs.

Un topic non retenu ne délivre rien à la souscription : l'entité
`sensor.boiler_ack_*_raw` conserve donc en mémoire le dernier acquittement reçu
jusqu'à l'arrivée du suivant. Toute lecture faite dans cet intervalle — trace,
notification, gabarit — affiche l'identifiant de la transaction **précédente**,
alors que la commande émise en porte un autre.

> **Règle de lecture, à retenir** : pour établir l'identifiant d'une émission, la
> source est le **payload publié**, jamais l'état d'une entité dérivée de
> l'acquittement.

Le corpus l'anticipait déjà — `retry_transactionnel/etat.yaml` exige
explicitement `ack2_request_id != attempt1_id`, « ce n'est pas un résidu T1 ».

**Aucune collision réelle. Aucun correctif n'est requis, et le générateur
d'identifiant n'est pas mis en cause.**

### 12.4 Ce que A-5 n'établit pas

- Les **trois autres rôles** en écriture — `heating_setpoint`,
  `heating_curve_shift`, `heating_curve_slope` — demeurent **non éprouvés** *à la
  date de A-5*. `heating_setpoint` l'a été depuis, par A-6 : voir §13.
- Le **comportement en refus** : aucune commande n'a été rejetée sur bornes, sur
  pas ou sur expiration.
- La **marge** entre budget de confirmation et attente : un seul échantillon.
- La divergence **TTL 30 s / attente 20 s au contrat contre 15 s / 15 s au
  runtime** reste ouverte, et A-5 ne la tranche pas.

---

## 13. Épreuve terrain A-6 — `heating_setpoint`, par le chemin natif

> **Une exécution unique, autorisée nommément, sur le seul rôle
> `heating_setpoint`.** Elle éprouve un **chemin d'appel différent de celui de
> A-5**, et c'est là son intérêt principal.

### 13.1 Pourquoi A-6 n'a pas la forme de A-5

`script.chauffage_appliquer_consigne` **n'accepte aucune valeur numérique** : ses
seules entrées sont un régime — `confort` ou `reduite` — et une raison. La valeur
émise est **dérivée** de `input_number.chauffage_consigne_confort` ou
`…_reduite` selon le régime en vigueur.

Il n'existait donc **aucun geste équivalent à celui de A-5**. Trois voies, dont
deux fermées : publier à la main aurait contourné la garde composée, le helper et
l'écrivain unique ; basculer de régime aurait été une décision métier à effet de
confort. **La seule voie conforme était de modifier le paramètre du régime
actif** et de laisser l'architecture faire le reste.

`automation.chauffage_modification_consigne` se déclenche en effet sur tout
changement de ces deux `input_number` et, **si l'input touché correspond au
régime en vigueur**, appelle l'écrivain unique de lui-même.

> **A-6 n'a donc pas commandé : elle a modifié un paramètre métier et observé
> l'architecture émettre.** C'est un acte de nature différente de A-5, et il faut
> le dire ainsi.

### 13.2 Ce qui a été exécuté

| # | Geste | Constat |
|---|---|---|
| 0 | régime en vigueur relevé | **`reduite`**, valeur initiale **15** |
| 1 | `input_number.chauffage_consigne_reduite` **15 → 16** | **modification native**, aucun appel direct du script |
| 2 | déclenchement | **automatisation native déclenchée**, écrivain unique appelé par elle |
| 3 | émission | payload `role = heating_setpoint`, `value = 16` |
| 4 | acquittement | **`applied`**, corrélé |
| 5 | relecture chaudière | **16** |
| 6 | restauration **16 → 15** | **par le même chemin**, aucun raccourci |
| 7 | acquittement | **`applied`**, corrélé |
| 8 | relecture finale | **15** — état initial rétabli |
| 9 | état terminal | helper **vide**, application **au repos**, garde **`on`** |

**Aucun MQTT manuel. Aucun appel direct du script exécutif.** L'essai a emprunté
exactement le chemin que la production emprunte.

**Sans effet de confort** : la consigne est une température de pièce visée.
Extérieur au-dessus de 27 °C, brûleur à l'arrêt — passer de 15 à 16 ne pouvait
créer aucune demande de chauffe.

### 13.3 Ce que A-6 établit, et que A-5 n'établissait pas

1. Le rôle **`heating_setpoint`** est écrit et confirmé de bout en bout.
2. Le **chemin d'appel indirect** fonctionne : un paramètre métier change,
   l'automatisation décide d'appliquer, l'écrivain unique émet. **A-5 avait
   éprouvé l'appel direct ; A-6 éprouve l'appel dérivé.**
3. **La restauration a emprunté le même chemin**, sans intervention hors
   architecture — et sans qu'un garde métier ait eu à corriger, contrairement à
   A-5.
4. Le **verrou d'application** et la **garde composée par rôle** ont laissé
   passer deux transactions légitimes et sont revenus au repos.

### 13.4 Ce que A-6 n'établit pas

- **`heating_curve_shift` et `heating_curve_slope` demeurent NON ÉPROUVÉS en
  écriture.** Ce sont des grandeurs de **calibration**, que le contrat de retry
  classe explicitement **non retryables** : leur épreuve appellera des
  précautions propres, et ne se déduit pas de A-6.
- Le **comportement en refus** reste non éprouvé, pour aucun rôle.
- La **marge** entre budget de confirmation et attente : deux échantillons de
  plus, toujours pas une caractérisation.
- L'essai a porté sur le régime **`reduite`**. Le régime `confort` emprunte le
  même chemin et le même écrivain, mais **n'a pas été exercé**.
