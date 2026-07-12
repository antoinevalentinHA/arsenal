# Audit — Rain Bird : santé du pont vs qualité radio (verdict « dégradé » permanent)

| Champ | Valeur |
|---|---|
| **Type** | Audit **statique, lecture seule** — sémantique du verdict de santé du pont Rain Bird |
| **Domaine** | Arrosage — pont `rainbird-esp32` (diagnostic / synthèse de santé) |
| **Statut** | **Ouvert — diagnostic + options sans code.** Aucun runtime, aucun contrat, aucune UI, aucun checker modifié. La correction n'est **pas figée** (options documentées, §16). |
| **Version** | 0.1 |
| **Chantier pressenti** | **C18** (prochain code libre — allocation formelle réservée à l'ouverture du chantier, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)) |
| **Déclencheur** | Constat terrain : le dashboard affiche « Santé : Dégradé » alors que tous les autres indicateurs sont nominaux (Données ON, Fraîcheur ON, Pont exploitable, RSSI -76 dBm ≥ plancher -90, batterie 100 %, heartbeat online, uptime > 16 j). |
| **Contrats normatifs de référence** | [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md), [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md), [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md), [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md), [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md), [`resilience_integrations.md`](../../../contrats/arrosage/../resilience_integrations.md) |

> **Garde-fou de lecture.** Ce rapport **ne modifie aucun fichier** runtime / YAML /
> Lovelace / helper / template / script / automation / recorder / customize / contrat /
> checker, **n'invente aucun `entity_id`**, **ne renomme rien** et **ne fixe aucune
> correction**. Les seuils et options évoqués sont des **hypothèses d'audit**, jamais des
> décisions d'implémentation. Toute suite reste à **arbitrer** puis à ouvrir formellement
> en chantier (Phase 3).

---

## 1. Contexte

La chaîne Rain Bird comprend **deux équipements distincts** : le **contrôleur** Rain Bird
BAT-BT-2 et le **pont** ESP32 (firmware `rainbird-esp32`). Leur **topologie a évolué dans le
temps** ; il faut distinguer l'inventaire historique de la configuration actuellement
déployée :

- **Topologie antérieure** — telle que **décrite (correctement à l'époque)** par l'inventaire
  [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md) §2
  et les pré-requis [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
  P6/P7 : contrôleur **dans une fosse sous plaque d'acier**, pont ESP32 **dans la petite
  maison**.
- **Topologie actuelle** — contrôleur **sorti de la fosse, en surface** ; pont ESP32 **dans le
  jardin, dans un meuble en béton**.

Cet audit raisonne sur la **topologie actuellement déployée**. Sur cette configuration, les
niveaux radio observés — Wi-Fi du pont et BLE pont↔contrôleur — sont **moyens mais stables,
autour de -76 dBm** et, de l'aveu de l'opérateur, **jamais sensiblement meilleurs** ; ils
restent **nettement au-dessus du plancher d'exploitabilité (-90 dBm)**, sans conséquence
fonctionnelle (aucun incident, pont exploitable). La mesure ~-76 dBm **n'est attribuée à
aucune cause physique particulière** dans ce rapport (ni plaque d'acier — désormais absente
de la chaîne — ni meuble béton).

> **Note topologie.** Les documents 08/10 **ne sont pas erronés** : ils décrivent la
> topologie **antérieure**. Ils **ne reflètent plus complètement** l'installation actuelle.
> Leur mise à jour éventuelle est **hors périmètre** de cet audit (candidate à un arbitrage
> ultérieur, cf. §18) ; le présent rapport se borne à **préciser le contexte**, sans corriger
> ni requalifier ces contrats.

Le dashboard `dashboards/systeme/rain_bird.yaml` affiche pourtant un verdict global
**« Santé : Dégradé »**, alors que toutes les autres tuiles attestent un fonctionnement
pleinement exploitable et stable. L'opérateur constate une dissonance : « Pont exploitable »
et « Santé dégradée » cohabitent en permanence, sans incident fonctionnel.

Cet audit explique **pourquoi** ce verdict se produit, **quelle notion** il devrait porter
selon les contrats, et **quelles options** existent — sans trancher.

---

## 2. Périmètre

**Dans le périmètre :**
- le producteur du verdict de santé `sensor.rain_bird_pont_sante` et sa logique ;
- ses dépendances amont (disponibilité, fraîcheur, RSSI bruts) ;
- la sémantique contractuelle de « santé du pont » et sa distinction d'avec la qualité radio
  et l'exploitabilité runtime ;
- les consommateurs réels du verdict et les risques de bord d'une éventuelle correction.

**Hors périmètre (cf. §18) :** toute modification de code, la couche décision/exécution de
l'arrosage (déjà auditée par ailleurs), les seuils métier d'humidité, la validation terrain
multi-cycles de C10.

---

## 3. État observé

Valeurs terrain au déclencheur (prises comme entrée, non relevées par l'audit) :

| Indicateur | Entité | Valeur | Verdict tuile |
|---|---|---|---|
| Santé | `sensor.rain_bird_pont_sante` | `degrade` | 🟠 **Dégradé** |
| Données | `binary_sensor.rain_bird_pont_donnees_disponibles` | `on` | 🟢 ON |
| Fraîcheur | `binary_sensor.rain_bird_pont_donnees_fraiches` | `on` | 🟢 ON |
| Garde runtime arrosage | `binary_sensor.arrosage_rain_bird_preconditions_runtime` | `on` | 🟢 Pont exploitable |
| BLE RSSI | `sensor.…_ble_rssi` | -76 dBm | (≥ -90) |
| Wi-Fi RSSI | `sensor.…_bridge_wifi_rssi` | -76 dBm | (≥ -90) |
| Batterie | `sensor.…_battery_level` | 100 % | connue |
| Heartbeat | `sensor.…_bridge_heartbeat` | online | — |
| Station active | `sensor.…_active_station` | Idle | — |
| Uptime | `sensor.…_bridge_uptime` | > 16 j | — |

Seul le verdict de **santé** est en anomalie apparente. Tous les autres signaux sont nominaux.

---

## 4. Chaîne de causalité

```
Source brute
  sensor.…_bridge_wifi_rssi = -76 dBm
  sensor.…_ble_rssi         = -76 dBm
        │
        ▼  Interprétation  (pont_sante.yaml, l.55-61)
  wifi_faible      = (wifi_raw in indispo) or wifi >= 0 or wifi <= -75  → True (car -76 <= -75)
  ble_non_qualifie = (ble_raw  in indispo) or ble  >= 0 or ble  <= -75  → True
        │
        ▼  Synthèse santé  (pont_sante.yaml, l.63-73 — priorité descendante)
  dispo='on' (pas 'inconnu' ni 'indisponible') ; frais='on' (pas le gate fraîcheur)
  wifi_faible OR ble_non_qualifie = True  →  state = 'degrade'
        │
        ▼  Entité exposée
  sensor.rain_bird_pont_sante = "degrade"
        │
        ▼  Carte UI  (rendu fidèle, aucune décision côté UI)
  button-card rain_bird_status_health_72  →  "Dégradé", fond orange
  dashboards/systeme/rain_bird.yaml (tuile Santé) + dashboards/systeme/principal.yaml (tuile Rain Bird)
```

**Cause exacte :** le gate `wifi_faible or ble_non_qualifie` (lignes 69-70 de
[`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml)) dégrade la
santé dès qu'un RSSI est **≤ -75 dBm**. Or, à l'emplacement réel, les RSSI observés sont
**stables autour de -76 dBm** et, selon l'opérateur, **jamais sensiblement meilleurs** :
tant que le signal reste à ce niveau, le verdict est **en pratique toujours `degrade`**,
indépendamment de toute anomalie opérationnelle — alors même que -76 dBm demeure **largement
au-dessus du plancher d'exploitabilité (-90)**.

---

## 5. Sources et producteurs

**Producteur unique du verdict :** `sensor.rain_bird_pont_sante`
([`12_template_sensors/arrosage/pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml)).

Il lit :
- **signaux dérivés Arsenal** : `binary_sensor.rain_bird_pont_donnees_disponibles`,
  `binary_sensor.rain_bird_pont_donnees_fraiches` ;
- **radio brute** (pour le niveau `degrade`) : `sensor.…_bridge_wifi_rssi`,
  `sensor.…_ble_rssi`.

Producteurs amont :
- [`pont_donnees_disponibles.yaml`](../../../../12_template_sensors/arrosage/pont_donnees_disponibles.yaml)
  — `on` si les entités cœur (heartbeat, uptime, version, active_station) ne sont pas
  unknown/unavailable ;
- [`pont_donnees_fraiches.yaml`](../../../../12_template_sensors/arrosage/pont_donnees_fraiches.yaml)
  — `on` si données exploitables **et** pont disponible **et** `bridge_uptime.last_reported`
  < 3 h (horloge de liveness).

Producteurs voisins (couche qualité/diagnostic, **indépendants** du verdict de santé) :
- [`pont_qualite_wifi.yaml`](../../../../12_template_sensors/arrosage/pont_qualite_wifi.yaml),
  [`pont_qualite_ble.yaml`](../../../../12_template_sensors/arrosage/pont_qualite_ble.yaml)
  — libellé lisible (bon ≥ -67 / acceptable -74..-68 / **faible ≤ -75**) ;
- [`pont_diagnostic_resume.yaml`](../../../../12_template_sensors/arrosage/pont_diagnostic_resume.yaml)
  — phrase de synthèse (mêmes seuils -67/-74).

Garde d'exploitabilité (couche autorisation, **indépendante**) :
- [`preconditions_runtime.yaml`](../../../../12_template_sensors/arrosage/preconditions_runtime.yaml)
  — `binary_sensor.arrosage_rain_bird_preconditions_runtime`, `on` si BLE/Wi-Fi **exploitables**
  (numériques, négatifs, **≥ -90 dBm**) et batterie connue.

---

## 6. Contrats applicables

| Contrat | Apport pour la santé du pont |
|---|---|
| [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6 | **Autorité de la notion.** `‹sante_pont_rainbird›` = « disponibilité ESP32, lien MQTT, dernier ACK BLE, **fraîcheur du poll** ». Distinction **fraîcheur ≠ disponibilité ≠ reprise**. Un pont **dégradé** doit faire **basculer vers le secours**. → **La qualité radio (RSSI) n'y figure pas comme critère de dégradation de santé.** |
| [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md) | Plancher d'**exploitabilité** radio = **-90 dBm** (porté par `preconditions_runtime`). Note §2 : « Santé pont `degrade` mais **exploitable** (préconditions `on`, données fraîches) ». |
| [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md) §9 | « **Pont exploitable** malgré santé `degrade`, **préconditions runtime `on`** ». |
| [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 | Liste `sensor.rain_bird_pont_sante` comme **entrée de décision** V1 (« santé pont suffisante pour exécuter et observer ») — **mais** le runtime ne l'implémente pas comme gate (cf. §10). |
| [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md) §2 | Relevé runtime des RSSI et des sources (**topologie antérieure**, cf. §1) ; `ble_status`/`ble_last_error` **explicitement écartés** des capteurs de santé. Mesure actuelle : ~-76 dBm, au-dessus du plancher -90. |
| [`resilience_integrations.md`](../../../contrats/arrosage/../resilience_integrations.md) | Doctrine **fraîcheur ≠ disponibilité ≠ reprise**, référencée par 03 §6. |

---

## 7. Comportement normatif (ce que le système DOIT faire)

Le contrat **central** du domaine (03 §6) fonde la **santé du pont** sur la **disponibilité,
le lien, l'ACK et la fraîcheur du poll** — c'est-à-dire la **capacité opérationnelle** du
pont à être piloté et observé. La portée de `degrade` y est **décisionnelle** (basculer vers
le secours). Aucun contrat ne définit un seuil radio (-75 ou autre) comme critère de
**dégradation de santé** : la qualité radio fine relève d'une couche **informative**
distincte, et l'exploitabilité radio est plancher à **-90 dBm**.

Les contrats 10 et 11 **actent déjà** que « santé `degrade` » et « pont exploitable »
coexistent dans l'état courant — mais ils le **constatent** comme un état de fait présent,
sans l'**ériger en norme** : le texte normatif de la santé reste celui de 03 §6.

---

## 8. Comportement runtime (ce qui est implémenté)

`pont_sante.yaml` calcule le verdict par priorité descendante :

1. `inconnu` — disponibilité non évaluée ;
2. `indisponible` — `pont_donnees_disponibles = off` ;
3. `degrade` — disponible **mais** `pont_donnees_fraiches = off` **OU** **radio faible
   (Wi-Fi/BLE ≤ -75)** ;
4. `ok` — disponible **et** frais **et** radio « correcte » (> -75).

Les niveaux 1-3 (hors branche radio) sont **conformes** à la notion contractuelle
(disponibilité + fraîcheur). C'est **l'ajout du critère radio ≤ -75** (niveau 3, seconde
branche) qui **excède** le contrat : ce seuil est **hérité verbatim de la couche qualité**
(`pont_qualite_*`, où « faible » = ≤ -75) et **transposé au niveau santé**, sans base
normative — et inatteignable positivement dans les conditions physiques réelles.

---

## 9. Comportement UI (ce qui est rendu)

L'UI **rend fidèlement** le verdict backend et **ne décide rien** : le template
`rain_bird_status_health(_72)` mappe `ok/degrade/indisponible/inconnu` vers libellé +
couleur, l'en-tête du dashboard affirmant explicitement « la santé reflète honnêtement
'degrade' ». **Aucun écart UI ↔ backend.** L'UI n'est **pas** en cause : elle est le
messager exact d'un verdict backend sur-sévère.

---

## 10. Consommateurs du verdict

| Consommateur | Type | Lit `pont_sante` ? | Effet |
|---|---|---|---|
| `dashboards/systeme/rain_bird.yaml` | UI | ✅ | affichage tuile Santé |
| `dashboards/systeme/principal.yaml` | UI | ✅ | affichage tuile Rain Bird |
| `recorder.yaml` (l.306) | Historisation | ✅ | trace l'état |
| `10_scripts/arrosage/station_1_courte_supervisee.yaml` (l.204) | Notification | ✅ | **texte descriptif** d'un message (« Santé pont : … »), **non décisionnel** |
| `contrats/arrosage/17_decision_v1.md` | Contrat | 📄 cité | **listé** en entrée de décision, **non implémenté** comme gate |
| `12_template_sensors/arrosage/intention.yaml` | Décision V1 | ❌ | gate sur `preconditions_runtime` + `pont_donnees_disponibles` — **pas** pont_sante |
| `11_automations/arrosage/declenchement.yaml` | Exécution | ❌ | garde = `binary_sensor.arrosage_intention` |
| `11_automations/arrosage/pont_indisponible_notification.yaml` | Notification | ❌ | source = `pont_donnees_disponibles` |
| `11_automations/arrosage/batterie_faible_notification.yaml` | Notification | ❌ | source = `battery_level` + `pont_donnees_disponibles` |

**Conclusion :** `pont_sante` est **strictement diagnostic/UI + historisation + une phrase de
notification**. **Aucune** garde de sûreté, **aucune** autorisation runtime, **aucune**
décision, **aucune** exécution d'arrosage, **aucun** autre domaine ne dépend de sa valeur.
La décision V1 s'appuie sur `preconditions_runtime` (exploitabilité -90) et
`pont_donnees_disponibles`, jamais sur le verdict de santé.

---

## 11. Analyse des seuils

| Seuil | Fichier(s) | Sens | Couche |
|---|---|---|---|
| **-90 dBm** | `preconditions_runtime.yaml`, contrat 10 | radio **exploitable** (présence, pas idéale) | **exploitabilité runtime** (autorisation) |
| **-75 dBm** | `pont_qualite_wifi/ble.yaml`, `pont_diagnostic_resume.yaml` | radio « **faible** » (vs acceptable/bon) | **qualité radio** (information) |
| **-75 dBm** | `pont_sante.yaml` (l.57, 61) | déclenche **`degrade` de santé** | **santé opérationnelle** ← *seuil emprunté à la couche qualité* |
| **-67 / -74 dBm** | `pont_qualite_*`, `pont_diagnostic_resume` | bon / acceptable | **qualité radio** (information) |

Le seuil -75 est **légitime** dans sa couche d'origine (qualité). Le problème n'est **pas sa
valeur** mais **sa présence au niveau santé** : la santé opérationnelle emprunte un critère
de la couche informative. Un simple remplacement `-75 → -90` **résoudrait le symptôme** (le
verdict repasserait `ok`), mais **replierait une notion d'exploitabilité dans la santé** —
au lieu de restaurer la séparation des trois couches. C'est pourquoi la correction **n'est
pas figée ici** (cf. §16).

---

## 12. Distinction : qualité radio / exploitabilité / santé

Le dépôt distingue **déjà** trois notions, portées par trois entités distinctes :

- **Qualité radio** (`pont_qualite_wifi`, `pont_qualite_ble`, `pont_diagnostic_resume`) :
  information graduée (bon / acceptable / faible), seuils -67 / -74 / -75. **Neutre** — décrit
  la finesse du lien, sans conséquence opérationnelle par elle-même.
- **Exploitabilité runtime** (`preconditions_runtime`) : garde binaire d'**autorisation**,
  plancher **-90 dBm** + batterie connue. Répond à « le pont est-il radio-exploitable pour
  exécuter/observer ? ».
- **Santé opérationnelle** (`pont_sante`) : verdict **synthétique** censé qualifier l'**état
  opérationnel réel** (disponibilité + fraîcheur, contrat 03 §6).

La séparation existe donc **par construction**. L'anomalie est que `pont_sante` **franchit la
frontière** en important le seuil -75 de la couche qualité. La cible d'une correction doit
**préserver** cette séparation, pas la brouiller davantage.

---

## 13. Écarts constatés

- **É1 — Frontière qualité → santé franchie (principal).** `pont_sante` dégrade sur la
  **qualité radio** (-75), critère absent de la notion contractuelle de santé (03 §6).
  Confusion entre **qualité radio informative** et **santé opérationnelle**.
- **É2 — Verdict durablement bloqué.** À l'emplacement réel, le RSSI stable (~-76 dBm,
  jamais sensiblement meilleur) reste ≤ -75 → santé **jamais `ok`** ; le verdict perd sa
  valeur de signal (il ne distingue plus nominal et anomalie).
- **É3 — Divergence contrat ↔ runtime (17).** Le contrat 17 §2/§3.6 liste `pont_sante` comme
  entrée de décision ; le runtime `intention.yaml` **ne le lit pas** (documenté « non
  bloquant »). Le runtime est **plus sûr** que le contrat ; l'écart est **inoffensif** mais
  **réel** (sémantique contractuelle imprécise).
- **É4 — Trois sémantiques radio cohabitantes.** -90 (exploitabilité), -75 (qualité), -75
  (santé). Seule la troisième est problématique ; les deux premières sont cohérentes.
- **É5 — Aucun garde-fou CI.** Aucun checker ne contraint la sémantique de `pont_sante` ni
  n'interdit la réintroduction d'un critère radio non contractuel dans la santé.

---

## 14. Risques

**Risques du statu quo :**
- verdict de santé **non informatif** (toujours dégradé) → l'opérateur s'habitue à l'orange
  et **rate une vraie dégradation** future (désensibilisation) ;
- divergence contrat 17 ↔ runtime non tranchée.

**Risques d'une correction mal cadrée (à maîtriser en Phases ultérieures) :**
- **Faux nominal / masquage** : si l'on retire trop de critères, un pont réellement muet ou à
  radio absente (RSSI positif / unknown) pourrait passer `ok`. → **préserver** les gates
  `pont_donnees_disponibles` (→ `indisponible`) et `pont_donnees_fraiches` (→ `degrade`), et
  le traitement des états `indispo`/`>= 0`.
- **Brouillage des couches** : un remplacement -75 → -90 replierait l'exploitabilité dans la
  santé (cf. §11) — techniquement vert, doctrinalement discutable.
- **Régression de notification** : **nulle** sur le déclenchement (les notifs ne lisent pas
  pont_sante) ; seule la **ligne descriptive** du Run changerait de valeur (inoffensif).
- **Divergence contrat ↔ runtime aggravée** : une correction runtime **sans** clarification
  contractuelle préalable (03/17) creuserait É3. → **contrat avant runtime**.
- **Effet sur l'arrosage / gardes** : **aucun** (pont_sante ne gate rien — §10).

---

## 15. Qualification du problème

**Combinaison de causes, dominée par la sémantique contractuelle :**
- **(Principal)** confusion **qualité radio ↔ santé opérationnelle** (É1) ;
- **(Contributif)** seuil -75 **mal placé** (couche qualité importée dans la santé) et
  inatteignable en conditions réelles (É2) ;
- **(Contributif)** **sémantique contractuelle incomplète** (17 liste une entrée que le
  runtime écarte à raison — É3).

**Ce que ce n'est PAS :** ni un **bug runtime** (le code fait ce que son en-tête décrit), ni
une **incohérence UI** (rendu fidèle), ni un **risque de sûreté** arrosage (pont_sante ne
gate rien).

---

## 16. Options de correction (documentées, non figées)

> Ces options sont présentées pour arbitrage. **Aucune n'est retenue** à ce stade. La règle
> **contrat avant runtime** impose de trancher d'abord la sémantique (03/17) puis, seulement
> si nécessaire, d'ajuster le runtime.

| Option | Description | Préserve la séparation 3 couches ? | Effet verdict (état courant) | Coût / risque |
|---|---|---|---|---|
| **A — Santé = disponibilité + fraîcheur seulement** | Retirer entièrement la branche radio du calcul de santé ; la qualité radio reste portée par `pont_qualite_*`. S'appuie directement sur 03 §6. | ✅ **Oui** (radio hors santé) | `ok` | faible ; clarifie 03 (radio informative) |
| **B — Santé dégrade sous exploitabilité (-90)** | Remplacer le gate `≤ -75` par « radio **hors exploitabilité** » (`< -90` / unknown / ≥ 0), aligné sur `preconditions_runtime`. | ⚠️ **Partiel** (importe l'exploitabilité dans la santé) | `ok` (à -76) | faible ; mais replie 2 couches |
| **C — Requalifier les niveaux de santé** | Introduire/clarifier `ok` (stable+frais+exploitable) / `degrade` (anomalie réelle **non bloquante** : fraîcheur limite, batterie faible, échecs récents) / `indisponible` (précondition non satisfaite). La radio moyenne stable **> plancher** reste neutre. | ✅ **Oui** (santé = opérationnel ; radio informative) | `ok` | moyen ; nécessite décision doctrinale 03 + éventuel checker |
| **D — Statu quo documenté** | Ne rien changer ; documenter que « dégradé » est l'état attendu au niveau radio observé (~-76 dBm). | — | `degrade` | verdict reste non informatif (rejeté implicitement par le déclencheur) |

**Combinaisons possibles :** A ou C peuvent intégrer un **critère batterie faible** et/ou un
**compteur d'échecs récents** pour donner à `degrade` un sens **positif** (anomalie réelle),
au lieu d'un `degrade` systématique. Ceci relève d'un arbitrage de fond (Phase 3+), pas du
présent rapport.

---

## 17. Recommandation

1. **Contrat avant runtime.** Trancher d'abord la **sémantique de santé** dans
   [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6 —
   confirmer que la santé = **disponibilité + fraîcheur + exploitabilité (plancher -90)**, et
   que la **qualité radio fine (-75) reste informative** — puis **réconcilier**
   [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 (statut réel de
   `pont_sante` : diagnostic, non gate).
2. **Correction runtime minimale** ensuite, conforme à l'arbitrage : privilégier une option
   qui **préserve la séparation des trois couches** (A ou C plutôt que le simple B), tout en
   **conservant** les gates disponibilité/fraîcheur.
3. **Garde-fou CI** si l'arbitrage l'exige (interdire la réintroduction d'un critère radio non
   contractuel dans la santé).
4. **UI et diagnostic inchangés** : l'UI rend déjà fidèlement ; la qualité fine reste portée
   par `pont_qualite_*`.
5. **Ne rien implémenter** avant l'ouverture formelle du chantier et l'arbitrage des options.

---

## 18. Périmètre proposé du chantier (C18 pressenti)

Lots pressentis, **à démontrer nécessaires** à l'ouverture (ne pas présumer que tous le
sont) :

1. **Clarification contractuelle** (03 §6 + réconciliation 17) — **probablement nécessaire**.
2. **Checker CI** de non-régression sémantique — **conditionnel** (selon 1).
3. **Correction backend minimale** de `pont_sante.yaml` — **probablement nécessaire**.
4. **Diagnostic** — **a priori inutile** (couche qualité déjà correcte).
5. **UI** — **a priori inutile** (rendu déjà fidèle).
6. **Validation sur états réels** puis **clôture documentaire**.

> **Point de contexte connexe (hors périmètre de cette PR).** L'inventaire 08 et les
> pré-requis 10 décrivent la **topologie antérieure** (fosse/plaque, ESP32 en petite maison)
> et **ne reflètent plus complètement** l'installation actuelle (contrôleur en surface, ESP32
> en meuble béton au jardin). Une **mise à jour de ces documents sur la topologie actuelle**
> est un **arbitrage distinct**, à décider à l'ouverture du chantier — il **n'est pas** un
> lot du présent audit et **ne conditionne pas** le diagnostic technique (§13), lequel tient
> sur la configuration actuelle.

---

## 19. Hors périmètre

- ❌ toute **modification de code** (runtime / contrat / UI / checker) — réservée aux phases
  ultérieures ;
- ❌ la couche **décision / exécution** de l'arrosage (V1), auditée par ailleurs
  ([`audit_arrosage_executions_longues_rain_bird.md`](audit_arrosage_executions_longues_rain_bird.md)) ;
- ❌ les **seuils métier d'humidité** et le canal réservoir sol ;
- ❌ la **validation terrain multi-cycles** de C10 (suivi opportuniste) ;
- ❌ tout **renommage** d'entité ou de fichier.

---

## 20. Critères d'acceptation pressentis (indicatifs, à figer en Phase 3)

1. Le verdict `sensor.rain_bird_pont_sante` **n'est plus `degrade` du seul fait** d'une radio
   moyenne stable **supérieure au plancher d'exploitabilité (-90 dBm)**.
2. Le verdict **reste `degrade`** en cas de **perte de fraîcheur** (`pont_donnees_fraiches =
   off`) et **`indisponible`** en cas de **données cœur indisponibles** — signaux
   opérationnels préservés.
3. La **séparation des trois couches** (qualité / exploitabilité / santé) est **préservée ou
   renforcée**, jamais brouillée.
4. La sémantique retenue est **portée par un contrat** (03/17 alignés) **avant** tout runtime.
5. **Aucune régression** sur les gardes, décisions, exécutions et notifications d'arrosage
   (inchangées par construction — pont_sante ne les alimente pas).
6. Les checkers documentaires et de domaine restent **verts**.

---

## 21. Fichiers potentiellement concernés (par une suite éventuelle)

**Contrats (si clarification) :**
- `00_documentation_arsenal/contrats/arrosage/03_coexistence_rainbird.md` (§6)
- `00_documentation_arsenal/contrats/arrosage/17_decision_v1.md` (§2/§3.6)

**Runtime (si correction) :**
- `12_template_sensors/arrosage/pont_sante.yaml` (**siège de la cause**)

**Checker (conditionnel) :**
- `scripts/arsenal_contracts/` (nouveau checker de non-régression sémantique)

**Registres / index (gouvernance) :**
- `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md` (ouverture C18 — Phase 3)
- `00_documentation_arsenal/audits/index.md` (indexation du présent rapport — même commit)

> **Rappel :** aucun de ces fichiers n'est modifié par le présent audit. Cette liste est
> **prospective**, pour cadrer un futur chantier.

---

## Renvois

- Coexistence / autorité « santé du pont » : [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md)
- Pré-requis runtime / plancher -90 : [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
- Mode manuel supervisé (exploitable malgré degrade) : [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md)
- Décision V1 (entrée pont_sante à réconcilier) : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Inventaire du pont (RSSI, sources écartées) : [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md)
- Audit voisin (exécutions longues Rain Bird) : [`audit_arrosage_executions_longues_rain_bird.md`](audit_arrosage_executions_longues_rain_bird.md)
- Cockpit de pilotage des chantiers : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Index des audits : [`index.md`](../../index.md)
