# CONTRAT ARSENAL — ARROSAGE
## 03 — Coexistence contrôlée Arsenal ↔ Rain Bird

**Version contrat :** v0.2 — amendée **C18 (Lot 1)**, 2026-07-12 : sémantique normative de la santé du pont et séparation des trois couches (§6.1–§6.4)
**Statut :** Normatif — antérieur au runtime
**Objet :** Contrat **central** du domaine. Définit comment Arsenal et le
programme interne du Rain Bird coexistent sans conflit, et comment le secours
reprend automatiquement si Arsenal disparaît.

---

## 1. Principe directeur

> **Double autorité accidentelle = interdite.**
> **Autorité de secours assumée = souhaitée, documentée et bornée.**

Deux décideurs (Arsenal et Rain Bird) agissant **simultanément et à leur insu**
sur les mêmes électrovannes produiraient un sur-arrosage incontrôlé et une
observation illisible. À l'inverse, une autorité de secours **déclarée,
calendrée et bornée** est exactement ce qui protège le jardin si Arsenal tombe.

La différence entre les deux n'est pas technique mais **doctrinale** : une
autorité de secours est **connue d'Arsenal, disjointe dans le temps, et
réversible**.

---

## 2. Le Rain Bird conserve un programme minimal connu d'Arsenal

- La **programmation interne du Rain Bird n'est pas neutralisée par défaut** :
  le Rain Bird reste en **`Auto`** (programme interne actif). `mode Off` est
  l'exception R3, pas la règle (voir [`02_regimes.md`](02_regimes.md)).
- Le Rain Bird **conserve en permanence un programme de secours minimal** :
  arrosage de survie suffisant pour que le jardin ne meure pas, **pas** un
  programme optimisé.
- Ce programme minimal est **déclaré et connu d'Arsenal** : Arsenal sait
  *quand* le secours arroserait s'il prenait la main. C'est la condition pour
  garantir des fenêtres disjointes.

> Un programme de secours **inconnu d'Arsenal** rendrait toute coordination
> impossible et recréerait la double autorité accidentelle. Le programme minimal
> doit donc être **documenté** (`‹calendrier_secours_rainbird›`, conceptuel) et
> tenu à jour comme une donnée d'entrée d'Arsenal.

---

## 3. Calendrier de secours déclaré & fenêtres disjointes

| Notion (conceptuelle) | Sens |
|---|---|
| `‹calendrier_secours_rainbird›` | Créneaux où le programme minimal Rain Bird arroserait s'il était l'autorité active |
| `‹fenetre_arsenal›` | Créneaux où Arsenal est autorisé à décider et exécuter |
| `‹cooldown_secours›` | Marge temporelle de garde avant/après un créneau de secours |

**Règles :**

1. **Fenêtres disjointes** : `‹fenetre_arsenal›` et `‹calendrier_secours_rainbird›`
   ne se **chevauchent jamais**. À tout instant, **au plus un** décideur est
   légitime sur une zone donnée.
2. **Cooldown avant/après** : autour de chaque créneau de secours, un
   `‹cooldown_secours›` interdit à Arsenal de déclencher un cycle, afin d'absorber
   les imprécisions d'horloge, la latence du pont et l'observation latente
   (voir [`06_observation_et_preuves.md`](06_observation_et_preuves.md)).
3. **Priorité temporelle** : si les deux autorités venaient à se réclamer le même
   instant (dérive d'horloge, bug), la résolution **s'abstient côté Arsenal**
   (le secours prime sur ce créneau) — jamais une double exécution.

> Les bornes exactes des fenêtres, du cooldown et du programme minimal sont
> **non figées** : elles seront calibrées en Phase 0
> ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)).

---

## 4. `rain_delay` comme dead-man switch

Le pont expose `rain_delay` en lecture/écriture. Le comportement attendu : tant
qu'un `rain_delay` est actif, le programme **interne** du Rain Bird **s'abstient**
d'arroser de lui-même.

Arsenal s'en sert comme **dead-man switch** (homme-mort) :

- en régime **Arsenal prioritaire** (R1), Arsenal **maintient le secours dormant**
  en **renouvelant périodiquement** un `rain_delay` **court** ;
- si Arsenal **cesse de renouveler** (crash, coupure Wi-Fi/MQTT/BLE, arrêt HA),
  le `rain_delay` **expire**, et le **programme minimal Rain Bird reprend
  automatiquement** la main.

**Invariants `rain_delay` :**

1. **Court** : la durée d'un `rain_delay` est brève devant l'intervalle de
   reprise acceptable du secours.
2. **Borné** : jamais une valeur arbitrairement longue.
3. **Renouvelé** : maintenu par reconductions périodiques explicites tant
   qu'Arsenal est vivant et veut garder la main.
4. **Jamais permanent** : aucun `rain_delay` « infini » ou non expirant.
   Un `rain_delay` qui ne peut pas expirer **neutralise le secours** et viole F1
   ([`01_metier.md`](01_metier.md)).

> **Phase 0 obligatoire.** Le comportement réel de `rain_delay` (effet exact sur
> le programme interne, granularité, expiration, interaction avec `runStation` et
> `stop irrigation`) **doit être validé en terrain** avant de fonder le secours
> dessus ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)). Tant qu'il n'est pas
> validé, `rain_delay` reste un **mécanisme candidat**, pas un acquis.
>
> *Carve-out V1 (contrat [`17`](17_decision_v1.md)) : la coexistence `rain_delay`
> **minimale** de la V1 est **conçue à partir de la documentation officielle** (Rain
> Bird ESP-BAT-BT, protocole SIP, projets open source), jugée suffisante ; les
> **comportements fins** sont confirmés **en exploitation**, sans Phase 0 bloquante.
> Les invariants ci-dessus (court / borné / renouvelé / jamais permanent) restent
> **intacts**.*

---

## 5. Direction de défaillance

> **Toute défaillance doit faire dériver le système vers le Rain Bird, jamais
> vers l'absence d'arrosage.**

| Défaillance | Comportement exigé |
|---|---|
| Arsenal / HA tombe | `rain_delay` expire → secours Rain Bird reprend |
| MQTT / ESP32 / Wi-Fi / BLE coupé | Arsenal ne peut plus reconduire → secours reprend |
| Capteurs sol Zigbee indisponibles | Arsenal s'abstient d'optimiser ; le secours reste le filet |
| Pont en bonne santé mais incertitude d'observation | Abstention prudente côté Arsenal, secours préservé |

**Anti-pattern interdit :** une garde qui, en cas de doute, **bloque tout
arrosage** (Arsenal *et* secours). En cas de doute, on **laisse le secours
faire**, on ne coupe pas le jardin.

> Ceci inverse la garde habituelle « en cas de doute, ne rien faire » : pour
> l'arrosage, **ne rien faire peut tuer le jardin**. La garde devient « en cas
> de doute, **laisser le filet de survie opérer** ».

---

## 6. Santé du pont — entrée de coexistence

La coexistence dépend de la **santé observable du pont** (`‹sante_pont_rainbird›`,
conceptuel) : disponibilité ESP32, lien MQTT, dernier ACK BLE, fraîcheur du poll.
La distinction **fraîcheur ≠ disponibilité ≠ reprise** est reprise de
[`resilience_integrations.md`](../resilience_integrations.md).

- Un pont **sain** autorise Arsenal à garder la main (R1) et à reconduire le
  dead-man switch.
- Un pont **dégradé** doit faire **basculer vers le secours** (laisser
  `rain_delay` expirer), pas tenter des commandes incertaines.

### 6.1 Trois couches distinctes — ne jamais confondre

> **Invariant sémantique (chantier C18, Lot 1).** La **santé opérationnelle**
> qualifie la **capacité du pont à être piloté et observé** ; elle **ne mesure pas**
> la finesse du signal radio. **Trois notions distinctes** cohabitent, chacune avec
> sa propre autorité et son entité propriétaire — aucune ne doit être repliée dans une
> autre :

| Couche | Question | Autorité / seuil | Entité propriétaire |
|---|---|---|---|
| **Santé opérationnelle** | « le pont est-il pilotable / observable maintenant ? » | disponibilité + fraîcheur (ce §6) | `sensor.rain_bird_pont_sante` |
| **Exploitabilité runtime** | « la radio est-elle exploitable pour émettre une commande ? » | radio **≥ -90 dBm** + batterie connue ([`10_prerequis_runtime.md`](10_prerequis_runtime.md)) | `binary_sensor.arrosage_rain_bird_preconditions_runtime` |
| **Qualité radio** | « quelle est la finesse du lien ? » (bon / acceptable / faible) | -67 / -74 / **-75** dBm | `sensor.rain_bird_pont_qualite_wifi`, `…_qualite_ble` |

> La **qualité radio** est une **information graduée neutre** : un signal **moyen mais
> stable** (p. ex. ~-76 dBm) **supérieur au plancher d'exploitabilité** n'a **aucune
> conséquence opérationnelle** et **ne dégrade pas** la santé. La **valeur RSSI** — ni
> le seuil qualité **-75**, ni le plancher d'exploitabilité **-90** — **n'est pas** un
> critère de **dégradation de santé** : une défaillance radio **réelle** est **déjà**
> captée par la **disponibilité** et la **fraîcheur** des données (le pont cesse de
> remonter des télémétries exploitables), **sans** lire le RSSI.

### 6.2 Sémantique normative du verdict de santé

Le verdict `sensor.rain_bird_pont_sante` prend **quatre états**, par **priorité
descendante**, fondés **uniquement** sur la disponibilité et la fraîcheur (**jamais**
sur la valeur RSSI) :

| État | Condition normative | Sens opérationnel |
|---|---|---|
| **`inconnu`** | disponibilité **non évaluée** (signal amont `unknown` / `unavailable` / vide) | on ne sait pas encore — jamais maquillé en certitude |
| **`indisponible`** | **données cœur indisponibles** (`binary_sensor.rain_bird_pont_donnees_disponibles = off`) | incapacité opérationnelle / précondition non satisfaite |
| **`degrade`** | disponible **mais** données **non fraîches** (`binary_sensor.rain_bird_pont_donnees_fraiches = off`) | anomalie **réelle mais non bloquante** : données présentes mais **périmées** (poll interrompu) |
| **`ok`** | disponible **et** frais | fonctionnement **stable, frais et exploitable** |

> **Décision D-C18-A (tranchée — Lot 1).** La **valeur RSSI est retirée** du calcul de
> santé (option A du rapport d'audit). **Justification :** (1) l'autorité de la santé
> (ce §6) n'a **jamais** inclus la valeur RSSI ; (2) le plancher **-90** relève de
> l'**autorisation** (préconditions) et le seuil **-75** de l'**information** (qualité)
> — les replier dans la santé **violerait** la séparation des trois couches (§6.1) ;
> (3) une défaillance radio réelle est **déjà** captée par la disponibilité / fraîcheur
> (producteurs fiables), donc ce retrait **ne perd aucun signal** opérationnel et **ne
> crée aucun faux nominal** ; (4) il **n'introduit aucun nouveau critère** de
> dégradation. Les options **B** (aligner sur -90) et **C** (enrichir `degrade` de
> batterie / échecs récents) sont **écartées à ce stade** : B replie deux couches ; C
> introduirait des signaux **sans besoin démontré ni producteur / sémantique établis**
> (interdit tant que ces trois conditions ne sont pas réunies — cf. décision ouverte
> D-C18-C au dossier de chantier).

> **Écart runtime temporaire (tracé — contrat avant runtime).** Ce §6 fixe la **norme**
> (Lot 1). Le runtime `12_template_sensors/arrosage/pont_sante.yaml` **dégrade encore**
> sur radio ≤ -75 dBm et **n'est pas corrigé ici**. Cet **écart contrat ↔ runtime** est
> **temporaire et assumé** ; sa résorption est l'objet du **Lot 3** (correction backend
> minimale), sous les critères §6.3. Tant que le Lot 3 n'est pas livré, le verdict
> `degrade` **structurel** observé sur radio moyenne reste **non conforme** à la norme
> ci-dessus, sans conséquence fonctionnelle (le verdict **ne gate rien**, §6.4).

### 6.3 Critères d'acceptation du correctif runtime (Lot 3)

Le runtime `pont_sante` corrigé **devra** :

1. produire **`ok`** quand le pont est **disponible et frais**, **quelle que soit** une
   qualité radio moyenne stable **supérieure au plancher -90** ;
2. produire **`degrade`** **si et seulement si** disponible **et** non frais
   (`binary_sensor.rain_bird_pont_donnees_fraiches = off`) ;
3. produire **`indisponible`** sur données cœur indisponibles, **`inconnu`** sur signal
   amont non évalué ;
4. **ne lire aucune valeur RSSI** comme critère de dégradation ;
5. n'altérer **aucune** garde, décision, exécution ou notification d'arrosage
   (`pont_sante` reste **non-gating**, §6.4).

### 6.4 `pont_sante` est diagnostic, non décisionnel

`sensor.rain_bird_pont_sante` est une **synthèse de diagnostic / observabilité**. Il
**ne conditionne aucune** décision, garde de sûreté ni exécution d'arrosage : la
décision V1 s'autorise sur `binary_sensor.arrosage_rain_bird_preconditions_runtime`
(exploitabilité) **et** `binary_sensor.rain_bird_pont_donnees_disponibles`
(disponibilité), **jamais** sur le verdict de santé (cf. [`17_decision_v1.md`](17_decision_v1.md)
§2/§3, décision **D-C18-B**). Toute évolution qui rendrait `pont_sante` décisionnel
exigerait une **décision contractuelle explicite** (non prévue à ce jour).

---

## 7. Invariants de coexistence

1. **Au plus une autorité légitime** par zone et par instant (fenêtres
   disjointes + cooldown).
2. **Double autorité accidentelle interdite** ; **autorité de secours assumée**
   souhaitée, déclarée et bornée.
3. Le **programme minimal Rain Bird est connu d'Arsenal** ; il n'est jamais
   neutralisé par défaut.
4. `rain_delay` est **court, borné, renouvelé, jamais permanent**.
5. La **non-reconduction** du `rain_delay` **doit** permettre la reprise
   automatique du secours.
6. **Direction de défaillance = vers Rain Bird**, jamais vers l'absence
   d'arrosage.
7. Le comportement réel de `runStation`, `stop irrigation` et le nombre réel de
   stations sont **présumés** tant que la Phase 0 ne les a pas **confirmés**. Pour
   `rain_delay`, la **coexistence minimale V1** est conçue à partir de la
   **documentation officielle** ; ses comportements fins sont confirmés **en
   exploitation** (carve-out V1, [`17`](17_decision_v1.md)).

---

## Renvois

- Régimes opérateur : [`02_regimes.md`](02_regimes.md)
- Honnêteté d'observation (ACK ≠ preuve) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Validation terrain : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Fraîcheur / disponibilité / recovery : [`resilience_integrations.md`](../resilience_integrations.md)
- Niveaux de preuve transactionnels : [`boiler/README.md`](../boiler/README.md), [`switchbot_transactionnel.md`](../switchbot_transactionnel.md)
- Alimentation / arrêt HA : [`ups_arret_ha.md`](../ups_arret_ha.md)
- Index du domaine : [`README.md`](README.md)
