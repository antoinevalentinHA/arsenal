# Rapport — Gouvernance documentaire de l'écosystème des dépôts satellites

> **Cadre.** Chantier **exclusivement documentaire**. Aucun runtime, YAML,
> automatisation, script ni intégration Home Assistant n'a été modifié. Objet :
> formaliser la manière dont Arsenal gouverne un écosystème de dépôts logiciels
> satellites et cartographier leurs responsabilités respectives.
>
> **Nature.** Rapport en lecture-analyse. **Non normatif** (n'édicte aucune règle
> métier), **non remédiant runtime** (aucune correction de code). Les
> recommandations sont **documentaires uniquement**.
>
> **Date :** 2026-07-03.

---

## 1. Documents créés

| Chemin | Rôle |
|---|---|
| [`architecture/ecosysteme_depots_satellites.md`](../../../architecture/ecosysteme_depots_satellites.md) | **Livrable principal.** Référence canonique de la couche « composants gouvernés » : vue d'ensemble (3 patrons d'intégration), fiche détaillée par dépôt (12 champs), frontières de responsabilité, incohérences relevées. |
| `audits/01_rapports/documentation/rapport_ecosysteme_depots_satellites.md` | Le présent rapport. |

## 2. Documents modifiés (documentaire uniquement)

| Chemin | Modification |
|---|---|
| [`architecture/index.md`](../../../architecture/index.md) | Nouvelle section « Racine — Écosystème / dépôts gouvernés » référençant le document canonique. |
| [`outils_externes/README.md`](../../../outils_externes/README.md) | Section « Voir aussi » reliant le pont chaudière au dépôt `boiler-bridge` et au document écosystème. |
| [`navigation/domaines/energie_chaudiere.md`](../../../navigation/domaines/energie_chaudiere.md) | Lien croisé (amont) vers `hassio-bluetti-bt` + `bluetti-bt-lib` (§4.1–4.2). |
| [`navigation/domaines/boiler.md`](../../../navigation/domaines/boiler.md) | Lien croisé (amont) vers `boiler-bridge` (§4.6). |
| [`navigation/domaines/arrosage.md`](../../../navigation/domaines/arrosage.md) | Lien croisé (amont) vers `rainbird-esp32-elegoo` (§4.5). |
| [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md) | Lien croisé (amont) vers `ha_airstage` (§4.3). |
| [`navigation/domaines/energie.md`](../../../navigation/domaines/energie.md) | Lien croisé (amont) vers `ha-linky` + signalement de l'incohérence documentaire (§6.1). |

> Les 5 hubs modifiés relèvent de la couche `navigation/`, **non normative et
> conçue pour porter des liens croisés** (règle R6 : direction & appartenance).
> Aucun contrat (`contrats/`) ni fragment runtime n'a été touché.

## 3. Emplacement documentaire retenu — justification

Le document canonique a été placé sous **`architecture/`** (fichier racine
`ecosysteme_depots_satellites.md`), et **non** dans une nouvelle zone de premier
rang, pour trois raisons :

1. **Fidélité à la taxonomie existante.** Le `README.md` racine fixe **neuf zones
   de premier rang**. Le précédent [`rapport_perception_externe_depot.md`](../perception_externe/rapport_perception_externe_depot.md)
   pose explicitement la règle « aucune zone de premier rang n'est créée » : on
   adosse un objet nouveau à une famille existante par parallélisme.
2. **`architecture/` est la « référence d'implémentation ».** La couche
   supply-chain / composants relève du *comment le système est construit*.
   `architecture/` héberge déjà des documents de frontière analogues
   (`chauffage/interface_ha_boiler_bridge.md`, `securisation_capteurs_externes.md`).
3. **Découvrabilité.** Le document est indexé dans `architecture/index.md` et
   maillé depuis les 5 hubs de domaine concernés + `outils_externes/README.md`.

## 4. Résumé de l'analyse

Six dépôts sous le compte `antoinevalentinHA` participent au fonctionnement
d'Arsenal. L'analyse a croisé **le runtime local** (`custom_components/`,
`configuration.yaml`, manifestes, contrats existants) et **les dépôts GitHub**
(README, manifest.json, config.yaml, code, releases).

Chaque dépôt a été qualifié sur les 12 axes attendus (objectif, propriétaire,
type, domaine, méthode d'intégration, stratégie de version, dépendances,
criticité, interfaces, contrats, documentation). Le détail est dans le document
canonique. Les trois faits structurants :

- **Trois patrons d'intégration distincts** coexistent (voir §5), ce qui explique
  pourquoi certains composants sont visibles dans l'arborescence (custom
  components) et d'autres non (add-on, ponts matériels externes).
- **La frontière de responsabilité est déjà tenue** par les contrats existants
  (Bluetti, boiler, arrosage) : Arsenal décide, les satellites transportent /
  mesurent / exécutent. Le document formalise cette frontière transversalement.
- **Un seul dépôt était totalement absent du corpus** : `ha-linky` (voir §7).

## 5. Architecture identifiée

### Trois patrons d'intégration

| Patron | Où s'exécute le composant | Consommation HA | Dépôts |
|---|---|---|---|
| **A — Custom component + lib Python** | Dans le processus HA (`custom_components/`) | Entités via manifeste + `requirements` | `bluetti-bt-lib` + `hassio-bluetti-bt` ; `ha_airstage` |
| **B — Add-on Supervisor** | Conteneur à côté de HA | Statistiques long-terme via WebSocket | `ha-linky` |
| **C — Pont matériel externe / MQTT** | Matériel dédié (Pi / ESP32), hors HA | HA = adaptateur aval d'un bus MQTT | `boiler-bridge` ; `rainbird-esp32-elegoo` |

### Correspondance dépôt → domaine → composant local

| Dépôt satellite | Domaine Arsenal | Ancrage local | Criticité |
|---|---|---|---|
| `bluetti-bt-lib` | `energie_chaudiere` | `requirements` du manifeste `bluetti_bt` (wheel v1.0.0) | Moyenne |
| `hassio-bluetti-bt` | `energie_chaudiere` | `custom_components/bluetti_bt/` (v0.2.1) | Moyenne |
| `ha_airstage` | `climatisation` | `custom_components/fujitsu_airstage/` (v1.7.1) | Élevée |
| `ha-linky` | `energie` | Add-on Supervisor (v1.7.0) — **hors arborescence dépôt** | Faible |
| `rainbird-esp32-elegoo` | `arrosage` | MQTT auto-discovery (relevé `arrosage/08`) | Moyenne (fail-safe) |
| `boiler-bridge` | `boiler` / `chauffage` | Bus MQTT (contrat `boiler_pi` + `interface_ha_boiler_bridge`) | **Critique** |

### Lignée des forks

- `hassio-bluetti-bt` ⟵ `Patrick762/hassio-bluetti-bt` ; `bluetti-bt-lib` ⟵ `Patrick762/bluetti-bt-lib`.
- `ha_airstage` ⟵ `danielkaldheim/ha_airstage` (branche par défaut `arsenal-stable`).
- `ha-linky` ⟵ `bokub/ha-linky`.
- `rainbird-esp32-elegoo` ⟵ variante ELEGOO WROOM-32 de `antoinevalentinHA/rainbird-esp32` (lui-même fork de `maillme/rainbird-esp32`).
- `boiler-bridge` : **dépôt original** (non forké), privé, « Conçu pour Arsenal ».

## 6. Ce qui appartient à qui — synthèse des frontières

| Concern | Arsenal | Satellite | Jamais dupliqué |
|---|---|---|---|
| Protocole appareil (SIP, Optolink, BLE, Conso API) | — | ✔ | Le protocole |
| Transport (MQTT raw, wheel, statistiques) | Consommation | ✔ Production | Le mapping au-delà de l'extraction |
| Valeur brute (SOC, tension, kWh, modulation) | Lecture seule | ✔ Émission | La valeur (jamais simulée côté HA) |
| Sémantique métier (santé, confort/éco, panne) | ✔ | — | Toute sémantique côté satellite |
| Décision & seuils | ✔ | Rejet domaine physique (bridge) | La décision côté satellite |
| Version du composant | Épinglage | Publication | Une seule source d'épinglage |

## 7. Incohérences constatées (non corrigées — documentaires)

1. **`ha-linky` sans aucune trace documentaire (finding principal).** Seul des six
   dépôts à n'apparaître **nulle part** dans le corpus (grep `linky`/`enedis` :
   zéro occurrence). Son patron (add-on écrivant des statistiques) explique son
   absence du runtime, pas l'absence de renvoi documentaire. **Recommandation :**
   nommer `ha-linky` comme source de statistiques gouvernée dans
   [`contrats/energie.md`](../../../contrats/energie.md) et le hub `energie`
   (renvoi ajouté côté hub par ce chantier ; le contrat reste à mailler par
   l'auteur).

2. **Manifestes de fork pointant vers l'amont.** `bluetti_bt` et `fujitsu_airstage`
   conservent `codeowners` / `documentation` / `issue_tracker` amont
   (`Patrick762`, `danielkaldheim`). Constat de traçabilité — non bloquant.

3. **Dérive de version lib Bluetti.** Manifeste épinglé `v1.0.0` ; `v1.0.1`
   publiée côté lib non reprise. Épinglage possiblement volontaire.

4. **Origine d'image firmware Rain Bird « à clarifier ».** Déjà signalé par
   `arrosage/08` §2 ; le document relie le relevé au dépôt `rainbird-esp32-elegoo`
   sans trancher l'image flashée.

5. **`boiler-bridge` privé et sans licence.** Constat de gouvernance ; sans
   incidence documentaire, la vérité protocolaire restant le bus MQTT décrit dans
   `outils_externes/boiler_pi/`.

## 8. Recommandations documentaires (non exécutées ici)

Au-delà des liens croisés déjà posés dans les hubs, et **sans aucune modification
runtime** :

- **R1 —** Mailler `ha-linky` dans le corps du contrat
  [`contrats/energie.md`](../../../contrats/energie.md) (source admissible de
  statistiques), pour résorber l'incohérence §7.1 au niveau normatif.
- **R2 —** Optionnel : ajouter un renvoi « dépôt satellite » en tête des contrats
  directement concernés (`contrats/bluetti.md`, `contrats/arrosage/08`,
  `architecture/chauffage/interface_ha_boiler_bridge.md`) vers le document
  écosystème. Non fait ici pour ne pas altérer l'en-tête de documents normatifs ;
  laissé à l'appréciation de l'auteur.
- **R3 —** Optionnel : consigner au registre de résilience
  ([`resilience_integrations.md`](../../../contrats/resilience_integrations.md)) le
  statut des intégrations satellites qui n'y figurent pas encore (Bluetti est
  BLE local, Linky est un add-on) — arbitrage de couverture, pas une dette.

## 9. Contraintes respectées

- ✅ Aucune modification de runtime, YAML, automatisation, script, intégration HA.
- ✅ Aucun dépôt satellite modifié (étude en lecture seule).
- ✅ Aucune architecture inventée : seules les relations réellement présentes sont
  décrites ; les zones d'incertitude sont signalées comme telles.
- ✅ Aucune nouvelle règle métier, aucune dépendance nouvelle, aucune proposition
  de fusion de dépôts.
- ✅ Neuf zones de premier rang préservées ; découvrabilité assurée par index et
  hubs existants.

---

*Fin du rapport. Chantier documentaire clos côté production de livrables ; les
recommandations R1–R3 restent à la main de l'auteur.*
