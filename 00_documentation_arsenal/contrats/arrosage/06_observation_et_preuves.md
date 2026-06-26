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

## Renvois

- Besoin (consomme le dernier arrosage connu) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Coexistence / santé du pont : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Source de vérité unique (modèle déshumidificateur) : [`deshumidificateur/README.md`](../deshumidificateur/README.md)
- Niveaux de preuve transactionnels : [`boiler/README.md`](../boiler/README.md), [`switchbot_transactionnel.md`](../switchbot_transactionnel.md)
- Fraîcheur / disponibilité / recovery : [`resilience_integrations.md`](../resilience_integrations.md)
- Validation terrain des signaux : [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Index du domaine : [`README.md`](README.md)
