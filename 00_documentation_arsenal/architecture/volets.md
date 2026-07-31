# 🧠 ARSENAL — ARCHITECTURE : VOLETS
# Domaine :
#   Volets roulants (pont iDiamant)
#
# Nature :
#   Document ARCHITECTURAL
#
# Rôle :
#   Décrire le positionnement, le pont matériel, les couches
#   et les frontières de responsabilité du sous-système
#   « Volets » dans l'architecture globale Arsenal.
#
# ⚠️ Ce document :
#   - N'est PAS contractuel
#   - Ne définit AUCUNE règle métier
#   - Ne reformule AUCUN invariant
#   - Ne remplace PAS le contrat volets_pluie.md
# ==========================================================


## 1. 🎯 OBJET ET PÉRIMÈTRE

Ce document décrit l'**architecture technique** du sous-système Volets :
le **pont matériel** qui relie les volets roulants à Home Assistant, la
chaîne de couches qui va de ce pont jusqu'aux scripts exécutifs, et la
**frontière de responsabilité** entre le pont (commercial) et Arsenal.

Il **ne définit aucune règle métier**. Les règles de réaction des volets
(pluie, présence, autorisations) relèvent du contrat fonctionnel
[`contrats/volets_pluie.md`](../contrats/volets_pluie.md), qui fait seul
autorité. Ce document décrit le **comment technique** ; le contrat décrit
le **quoi métier**.

| Inclus | Exclu |
|---|---|
| Le pont iDiamant comme composant d'architecture | Règles de fermeture pluie / présence (→ `volets_pluie.md`) |
| Chaîne transport → intégration HA → covers → exécution | Qualification météo / production des signaux pluie |
| Frontière de responsabilité, mode de défaillance | Détection d'ouvrants (→ `architecture/ouvertures.md`) |
| Renvois vers supervision et alimentation | Sémantique métier des scénarios volets |


## 2. 🧭 POSITIONNEMENT — POURQUOI iDiamant N'EST PAS UN DÉPÔT SATELLITE GOUVERNÉ

Le pont iDiamant est **un pont matériel**, au même titre architectural que
`boiler-bridge` (chaudière) ou `rainbird-esp32-elegoo` (arrosage) : il fait
l'interface entre un protocole d'appareil et Home Assistant.

Il **ne figure pourtant pas** dans
[`architecture/ecosysteme_depots_satellites.md`](ecosysteme_depots_satellites.md),
et c'est **volontaire** : ce document recense les *dépôts satellites
**gouvernés*** — des dépôts logiciels (forks ou code original) dont Arsenal
possède et gouverne le code. Ses critères :

> « Arsenal décide ; les satellites transportent, mesurent ou exécutent. »
> « Le seul dépôt modifiable est Arsenal. »

L'iDiamant est une **passerelle commerciale propriétaire** (produit
Netatmo / Legrand) : Arsenal n'en possède **ni le code, ni le firmware, ni
le protocole**. Ce n'est donc **pas** un dépôt satellite gouverné, et l'ajouter
à ce catalogue en briserait la cohérence.

👉 **La distinction est doctrinale, pas une omission** : un pont matériel
peut être *gouverné* (code Arsenal → catalogue des satellites) ou
*commercial* (boîte noire → documenté ici, en architecture, comme composant
d'intégration). Le présent document est le **home des ponts commerciaux**
côté Volets.


## 3. 🧱 LE PONT iDiamant — FAITS RELEVÉS

> Faits observables dans le corpus Arsenal. La **vérité protocolaire**
> reste le produit commercial lui-même ; Arsenal n'en réimplémente rien.

| Champ | Valeur relevée |
|---|---|
| **Rôle** | Contrôleur / pont des volets roulants (canal « RF / Volets ») |
| **Type** | Passerelle commerciale propriétaire (Netatmo / Legrand) — boîte noire |
| **Adresse LAN** | Adresse fixe sur le LAN — mapping hôte/IP porté par [`ping_lan_synthese.md`](../contrats/ping_lan_synthese.md) |
| **Sonde de présence réseau** | `binary_sensor.idiamant` (intégration Ping native) |
| **Alimentation** | `switch.prise_palier` — secteur direct (cf. [`infrastructure_puissance.md`](infrastructure_puissance.md)) |
| **Criticité (supervision LAN)** | *importante* (classe « RF / Volets », cf. [`ping_lan_synthese.md`](../contrats/ping_lan_synthese.md)) |
| **Covers exposés (relevés)** | `cover.sejour_gauche`, `cover.sejour_droit`, `cover.chambre_enfants`, `cover.salle_de_jeux` — liste non exhaustive |

> ⚠️ **À confirmer :** la **méthode d'intégration exacte** des `cover.*`
> dans Home Assistant (intégration native, cloud, ou locale) n'est pas
> tranchée par le corpus relevé. Ce document ne préjuge pas de ce point ;
> il constate les entités `cover.*` consommées en aval. À figer lors d'une
> Phase 0 dédiée si le domaine Volets est formalisé en contrat.


## 4. 🔀 PATRON D'INTÉGRATION

Les ponts matériels d'Arsenal se répartissent en patrons. Le pont iDiamant
constitue une **variante commerciale** du patron « pont matériel externe » :

| | `boiler-bridge` | `rainbird-esp32` | **iDiamant** |
|---|---|---|---|
| Gouvernance | Dépôt Arsenal | Dépôt Arsenal | **Produit commercial** |
| Transport vers HA | MQTT **contractuel** (ACK) | MQTT auto-discovery | **Entités `cover.*`** (produit) |
| Modèle transactionnel | Oui (`request_id`) | Non | Non |
| Vérité protocolaire | Bus MQTT documenté | Firmware Arsenal | **Boîte noire commerciale** |
| Documenté dans | `outils_externes/boiler_pi/` + écosystème | écosystème + `contrats/arrosage/` | **ce document** |

👉 Différence structurante : pour le boiler et le Rain Bird, Arsenal
**gouverne le transport**. Pour l'iDiamant, le transport (`cover.*`) est
**produit par la boîte noire** ; Arsenal en est un **consommateur aval**,
sans aucune prise sur le protocole.


## 5. 🔄 CHAÎNE ARCHITECTURALE EN COUCHES

```
Volets roulants (moteurs RF)
        ↓  (protocole propriétaire — boîte noire)
Pont iDiamant (produit commercial)          ← hôte fixe sur le LAN
        ↓  (entités cover.*)
Entités cover.* Home Assistant (transport)  ← PRODUIT PAR LE PONT
        ↓
Scripts exécutifs Arsenal                    ← APPARTIENT À ARSENAL
  · script.volets_fermeture_execute (idempotent, pur exécutif)
  · scripts de commande groupée (ouvrir/fermer tout, séjour…)
        ↓
Orchestration & décision métier              ← APPARTIENT À ARSENAL
  · contrat volets_pluie.md (réaction pluie)
        ↓
Restitution UI (dashboard Volets)
```

Chaque couche a une responsabilité unique. Les **scripts** sont l'**autorité
unique sur le matériel** (doctrine Arsenal) : ils reçoivent une liste de
`cover.*` et agissent, sans porter de politique ni de décision métier.


## 6. 🚧 FRONTIÈRE DE RESPONSABILITÉ

> Ce que **produit** le pont (protocole RF, état `cover.*`) ne doit **jamais**
> être réimplémenté dans Arsenal ; ce que **décide** Arsenal (quand fermer,
> pour qui, sous quelles autorisations) ne doit **jamais** dépendre du pont.

| Concern | Appartient à Arsenal | Appartient au pont iDiamant |
|---|---|---|
| Protocole RF moteurs | — | Pont (boîte noire) |
| Entités `cover.*` (transport / état) | Consommation aval | **Production** |
| Commande matérielle (open/close) | Émission via scripts | Exécution physique |
| Décision « quand / pour qui fermer » | **Arsenal** (`volets_pluie.md`) | — |
| Autorisations, présence, verrous | **Arsenal** | — |


## 7. 🚨 MODE DE DÉFAILLANCE CONNU

Le contrat [`ping_lan_synthese.md`](../contrats/ping_lan_synthese.md) relève
explicitement un mode de panne du pont :

> « iDiamant répond au ping tout en étant planté applicativement. »

👉 **Ping = couche transport uniquement.** La sonde `binary_sensor.idiamant`
prouve la **joignabilité réseau**, jamais le **fonctionnement applicatif**
des volets. La supervision Ping ne se substitue donc pas à une éventuelle
supervision métier du pont — laquelle n'est **pas** formalisée à ce jour
(voir §9).


## 8. 🔗 RELATIONS AVEC LES AUTRES DOMAINES

| Domaine / doc | Lien |
|---|---|
| [`contrats/volets_pluie.md`](../contrats/volets_pluie.md) | Règles métier de réaction des volets à la pluie (autorité) |
| [`architecture/ouvertures.md`](ouvertures.md) | Détection des ouvrants (fenêtres) — amont décisionnel des règles chambres |
| [`architecture/infrastructure_puissance.md`](infrastructure_puissance.md) | Alimentation du pont (`switch.prise_palier`, secteur direct) |
| [`contrats/ping_lan_synthese.md`](../contrats/ping_lan_synthese.md) | Supervision réseau du pont (classe RF/Volets, criticité *importante*) |
| [`architecture/ecosysteme_depots_satellites.md`](ecosysteme_depots_satellites.md) | Catalogue des ponts **gouvernés** (dont l'iDiamant est explicitement exclu, §2) |


## 9. 📌 POINTS À CONFIRMER / ÉVOLUTIONS POSSIBLES

Constats de couverture documentaire. **Aucun n'entraîne de modification
runtime, YAML ou intégration.**

1. **Méthode d'intégration `cover.*` non tranchée** (native / cloud / locale) —
   à figer en Phase 0 si le domaine Volets est formalisé en contrat (§3).
2. **Pas de supervision métier du pont** au-delà du Ping réseau, alors même
   qu'un mode de panne applicatif est déjà identifié (§7).
3. **Cadrage écosystème** : ajouter dans
   [`ecosysteme_depots_satellites.md`](ecosysteme_depots_satellites.md) une
   note de périmètre expliquant que les **ponts commerciaux** (iDiamant, …)
   existent mais ne sont pas des dépôts gouvernés, avec renvoi vers le présent
   document — afin que l'absence d'iDiamant du catalogue ne se relise pas comme
   un oubli.


# ==========================================================
# 📐 ARCHITECTURE VOLETS — DOCUMENT DE RÉFÉRENCE
# ==========================================================
