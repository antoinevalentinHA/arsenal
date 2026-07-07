# CONTRAT ARSENAL — ARROSAGE
## 06 — Observation & preuves (honnêteté d'état)

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Contrat d'**honnêteté d'observation**. Le système ne doit **jamais**
présenter une présomption comme un fait. Distingue ce qui est **confirmé**,
**présumé** et **inconnu**.

---

## 1. Principe — l'observation est partielle et honnête

Le pont `rainbird-esp32` (MQTT ↔ ELEGOO ESP32 classique ↔ BLE) offre une observation **réelle
mais partielle** : il y a un **ACK BLE** de commande, un **poll périodique** du
contrôleur, un **état de station active** possiblement latent — mais **aucun
débitmètre**, **aucune preuve que l'eau coule réellement**.

> **Invariant fondateur.**
> **ACK BLE ≠ preuve hydraulique.**
> **Station « active » ≠ eau qui coule.**
> Le système doit modéliser ce qu'il **sait**, ce qu'il **présume**, et ce qu'il
> **ignore** — et ne jamais maquiller l'un en l'autre.

Cette doctrine reprend la séparation **source de vérité / présomption** du
déshumidificateur ([`deshumidificateur/README.md`](../deshumidificateur/README.md))
et les **niveaux de preuve transactionnels** du boiler / SwitchBot
([`boiler/README.md`](../boiler/README.md),
[`switchbot_transactionnel.md`](../switchbot_transactionnel.md)).

---

## 2. Trois niveaux de vérité d'arrosage

| Niveau | Définition | Exemple |
|---|---|---|
| **Confirmé** (`‹rainbird_detecte›`) | Fait **observé** par un signal réel et frais | Station rapportée active par un poll **récent** |
| **Présumé** (`‹rainbird_presume›`) | **Déduit** d'une commande acquittée, **sans** confirmation d'effet | Commande `runStation` **ACK BLE**, mais aucun poll d'état postérieur |
| **Inconnu** | Ni observé, ni déductible avec confiance | Pont injoignable, poll périmé, état latent ambigu |

> **`‹rainbird_detecte›` ≠ `‹rainbird_presume›`.** Ces deux notions conceptuelles
> sont **distinctes par construction** et ne doivent **jamais** être fusionnées
> en un seul état « arrosage = oui ». La frontière entre elles est la **preuve**,
> pas la **commande**.

---

## 3. Ce qu'un ACK BLE prouve — et ne prouve pas

| L'ACK BLE prouve | L'ACK BLE ne prouve PAS |
|---|---|
| La commande a été **reçue** par le contrôleur | Que l'électrovanne s'est **ouverte** |
| Le lien BLE était **vivant** à cet instant | Que **l'eau a coulé** |
| Le pont **fonctionne** | Que la **zone a été arrosée** |

> Sans débitmètre, la **preuve hydraulique** n'existe pas dans ce système. Le
> meilleur niveau atteignable est **« station active confirmée par poll récent »**
> — qui reste une preuve d'**état du contrôleur**, pas d'**écoulement d'eau**.
> Toute UI ou tout historique doit refléter cette limite.

---

## 4. Observation latente / partielle

- L'**état de station active** peut être **latent** : rapporté avec retard, ou
  partiellement, par le poll périodique.
- Un poll **périmé** ne vaut pas « pas d'arrosage » : il vaut **inconnu** (cf.
  fraîcheur ≠ disponibilité, [`resilience_integrations.md`](../resilience_integrations.md)).
- Le **dernier arrosage connu** consommé par le besoin
  ([`04_besoin_hydrique.md`](04_besoin_hydrique.md)) doit **porter son niveau de
  vérité** (confirmé / présumé / inconnu), jamais une date « propre » qui
  masquerait une présomption.

---

## 5. Honnêteté d'UI et d'historique

> **Interdit cardinal.** L'UI et l'historique **ne doivent jamais présenter une
> présomption comme un fait**.

Règles :

1. Un arrosage **présumé** (ACK sans confirmation) est affiché **comme présumé**,
   visuellement distinct d'un arrosage **confirmé**.
2. Un état **inconnu** est affiché **comme inconnu**, jamais replié
   silencieusement sur « pas d'arrosage » ni sur « arrosé ».
3. L'historique conserve la **distinction** confirmé / présumé / inconnu — il ne
   réécrit pas un présumé en confirmé a posteriori sans preuve.
4. Aucune couleur/icône « vert = tout va bien » ne doit recouvrir un état
   seulement **présumé** ou **inconnu**.

---

## 6. Invariants d'observation

1. **ACK BLE ≠ preuve hydraulique** ; **station active ≠ eau qui coule**.
2. Trois niveaux de vérité **distincts** : confirmé / présumé / inconnu.
3. `‹rainbird_detecte›` (confirmé) et `‹rainbird_presume›` (présumé) **ne
   fusionnent jamais**.
4. Un **poll périmé** ou un pont injoignable → **inconnu**, jamais « pas
   d'arrosage ».
5. Le **dernier arrosage connu** porte toujours son **niveau de vérité**.
6. **UI et historique ne présentent jamais une présomption comme un fait.**
7. Les noms d'état sont **conceptuels** ; leur ratification relève de la Phase 0
   et du runtime futur.

---

## 7. Observation de la pluie — cumul glissant honnête

Le même principe « distinguer l'absence de fait de l'absence de donnée »
s'applique à la **pluie observée**, entrée de la suspension d'arrosage
([`suspension_pluie`](../../../12_template_sensors/arrosage/suspension_pluie.yaml)).

### 7.1 Limite connue du couple `statistics/change` + source rare

Les cumuls glissants `sensor.pluie_cumul_24h/48h/72h` étaient produits par des
capteurs `platform: statistics` en `state_characteristic: change`
(= plus récent − plus ancien **dans la fenêtre**), sourcés sur
`sensor.pluie_total_local`. Cette source, monotone, **n'émet un état que
lorsqu'elle change** : par temps sec prolongé, la fenêtre se vide et le capteur
`statistics` retourne **`unknown`**. Le moteur brut **confond alors deux
situations distinctes** : « fenêtre sans échantillon récent » (source saine,
il n'a pas plu → **0.0 mm**) et « donnée absente » (source injoignable →
**inconnu**). C'est une violation locale de l'honnêteté d'observation (§1).

### 7.2 Règle — couche métier au-dessus du moteur brut

Les moteurs `statistics` sont **rétrogradés en produits internes**
(`sensor.pluie_cumul_*_brut`, non consommés). Une **couche métier template**
([`meteo/pluie/cumul_glissant.yaml`](../../../12_template_sensors/meteo/pluie/cumul_glissant.yaml))
porte les entités stables `sensor.pluie_cumul_24h/48h/72h` avec la sémantique :

| Situation | État exposé | Niveau de vérité (§2) |
|---|---|---|
| Source `pluie_total_local` invalide / injoignable | `unavailable` (via `availability`) | **inconnu** |
| Source saine + fenêtre brute vide (`unknown`) | **`0.0` mm** | **confirmé** (fait observé : aucune pluie) |
| Source saine + valeur brute numérique | `max(0, brut)` mm | **confirmé** |

Le **clamp `max(0, brut)`** neutralise la fenêtre négative transitoire d'un
reset du store (cf. hypothèse des moteurs bruts) : un cumul de pluie **ne peut
pas être négatif** ; un négatif est un **artefact technique**, pas une valeur
métier exploitable — il est donc ramené à 0.0 et non présenté.

### 7.3 Conséquences (honnêteté et sécurité)

- **UI** : les cartes « Cumul 24 h / 48 h » affichent `0.0 mm` par temps sec
  (fait), et un état indisponible **uniquement** si la source est réellement
  défaillante — jamais un 0 masquant une panne (§5-6).
- **Décision** : la suspension pluie reçoit un `0.0` numérique au lieu de
  `unknown`. Le comportement décisionnel est **inchangé** (`0.0 < seuil` ⇒ pas
  de suspension, exactement comme `unknown` était déjà traité en `indispo`) ;
  la doctrine F1 (doute ⇒ ne pas priver le jardin) est préservée. La suspension
  n'est qu'un **frein additif** de `binary_sensor.arrosage_intention`
  ([contrat 17](17_decision_v1.md)) : un `0.0` **relâche un frein, il n'actionne
  aucun accélérateur** (besoin sol, fenêtre, préconditions/fraîcheur pont).
- **Redémarrage** : au boot, le moteur brut reconstruit sa fenêtre depuis
  l'historique Recorder de `sensor.pluie_total_local` (source historisée,
  Population A). Un `0.0` transitoire de reconstruction **ne peut pas** provoquer
  d'arrosage prématuré : les préconditions runtime exigent un pont Rain Bird
  **joignable et frais**, indisponible dans les premières secondes. **Aucune
  garde supplémentaire n'est requise** — les gardes de décision existantes
  suffisent.

### 7.4 Invariant ajouté

8. **Cumul de pluie honnête.** Un cumul glissant expose un **fait 0.0** quand la
   source est saine et la fenêtre vide, et **inconnu** (`unavailable`) quand la
   source est défaillante. Il ne replie jamais une source défaillante sur 0, ni
   n'expose un cumul négatif. La logique métier vit dans une couche template
   dédiée ; les moteurs `statistics` bruts ne sont **pas** consommés directement.

---

## Renvois

- Besoin (consomme le dernier arrosage connu) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Coexistence / santé du pont : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Source de vérité unique (modèle déshumidificateur) : [`deshumidificateur/README.md`](../deshumidificateur/README.md)
- Niveaux de preuve transactionnels : [`boiler/README.md`](../boiler/README.md), [`switchbot_transactionnel.md`](../switchbot_transactionnel.md)
- Fraîcheur / disponibilité / recovery : [`resilience_integrations.md`](../resilience_integrations.md)
- Validation terrain des signaux : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Index du domaine : [`README.md`](README.md)
