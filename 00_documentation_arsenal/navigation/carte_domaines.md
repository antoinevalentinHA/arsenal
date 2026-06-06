# 🗺️ Arsenal — Carte des domaines

> **NAVIGATION — NON NORMATIF.** Ce document **n'établit aucune règle** : il recense et classe les domaines pour orienter la navigation. En cas de divergence avec un document de famille (`contrats/`, `architecture/`, `audits/`, `changelog/`), **le document de famille fait foi**.
>
> **Rôle.** Registre **canonique** des domaines Arsenal et **autorité** de la couche navigation : tout futur hub découle d'une entrée de cette carte (1 hub ⟺ 1 entrée Tier 1).
>
> **Statut.** v2. **Maillé** — les 21 hubs de domaine sont liés en hypertexte depuis cette carte.

---

## Légende des familles

`C` contrat · `A` architecture · `Au` chaîne d'audit · `Ch` changelog de chantier dédié · `Ext` outil externe · `RT` couche runtime dérivée dédiée.

## Critères de Tier

- **Tier 1 — hub dédié** : au moins un de — (a) domaine **folderisé** en contrats, (b) **chaîne d'audit** présente, (c) présence dans **≥ 2 familles**, (d) **couche dérivée substantielle**.
- **Tier 2 — entrée feuille** : contrat **mono-fichier**, sans audit, sans architecture dédiée, sans couche substantielle. Pas de hub ; renvoi direct vers l'unique contrat.
- **Système / transverse** : contrat **non-domaine métier** (gouvernance, infrastructure, réseau, self). Pas de hub de domaine.
- **Hors hubs** : objets **non-domaine** (rapports méta, buckets transverses, infrastructure de famille). Traités par les **pivots** ou les index de famille.

---

## 1. Tier 1 — Domaines à hub dédié

| Domaine (nom canonique) | Familles | Note taxonomique |
|---|---|---|
| [`chauffage`](domaines/chauffage.md) | C·A·Au·Ch | Chaîne complète. `Ch` = les `CHANGELOG_CH1..6` (gouvernance CI Chauffage) **actuellement classés à tort** sous `changelog/chantiers/climatisation/`. |
| [`ecs`](domaines/ecs.md) | C·Au | Inclut le **sous-domaine `bouclage`** (cf. §5). Boucle d'arbitrage *watchdog* aboutie. |
| [`alarme`](domaines/alarme.md) | C·Au | Chaîne complète (CH1/CH2/CH6) ; **absente de `audits/index.md`**. « CH-x » **propre à alarme** (cf. §5). |
| [`climatisation`](domaines/climatisation.md) | C·Au | Chantier COOL livré (v15.8.4). **Pas de `Ch` propre** : le dossier `changelog/chantiers/climatisation/` contient en réalité les CH-x du **Chauffage**. |
| [`vacances`](domaines/vacances.md) | C·Au | Contrat mono-fichier mais **chaîne d'audit complète** (→ clôture partielle, VAC-IMP-5). Réfs croisées vers `contrats/chauffage/65_,66_`. |
| [`meteo`](domaines/meteo.md) | C·A·Au | **Météo extérieure** (sources, axe température/humidité *jardin*). Distincte de la température/humidité intérieures (cf. §5). |
| [`temperature_interieure`](domaines/temperature_interieure.md) | C·A·Au | **Domaine propre**, mais contrat **logé sous** `contrats/meteo/` (`axe_temperature`, `temperature_interieure/`). Chaîne audit autonome. |
| [`humidite_relative_interieure`](domaines/humidite_relative_interieure.md) | C·RT | **Domaine propre**, contrat **logé sous** `contrats/meteo/` ; pipeline dérivé + **CI dédiée** présents. **Non audité — état de cycle, pas un défaut.** |
| [`ui_lovelace`](domaines/ui_lovelace.md) | C·A·Au·Ch | **Fusion `ui` + `lovelace`** (un domaine, deux façades : référence `ui/` + cycle audit Lovelace). `Ch` = `CHANGELOG_CH-LL-CI-1`. |
| [`aeration_blocage_chauffage`](domaines/aeration_blocage_chauffage.md) | C | Folder (37) — machine d'état `m0→m6`. **Distinct** de `aeration_recommandation` (cf. §3 et §5). |
| [`pannes`](domaines/pannes.md) | C | Folder (9) — `internet` + `secteur`. Réf. résilience croisée avec `energie_chaudiere`. |
| [`boiler`](domaines/boiler.md) | C·Ext | Contrat HA (`contrats/boiler/`) **distinct** de l'outil `outils_externes/boiler_pi/` (pont Raspberry Pi). |
| [`eclairage`](domaines/eclairage.md) | C·A | Folder (6) + `architecture/eclairage_jardin.md`. |
| [`ouvertures`](domaines/ouvertures.md) | C·A | Folder (3) + `architecture/ouvertures.md`. **Léger — hub conservé** (carte explicite plutôt qu'invisibilisation). |
| [`voiture`](domaines/voiture.md) | C·A·Au | `architecture/voiture.md` porte un **contenu erroné** (copie d'aération) — signalé par l'audit structurel. |
| [`energie_chaudiere`](domaines/energie_chaudiere.md) | C·RT | Fichier `contrats/bluetti.md` (Bluetti AC180). Couche dérivée **vérifiée fidèle au runtime**. Nom de fichier ≠ nom canonique. |
| [`presence`](domaines/presence.md) | C·A | `contrats/presence.md` + `architecture/presence/` (`presence`, `wifi`). |
| [`energie`](domaines/energie.md) | C·A | `contrats/energie.md` + `architecture/energie.md`. |
| [`deshumidificateur`](domaines/deshumidificateur.md) | C | Folder (2). **Léger — hub conservé** (carte explicite plutôt qu'invisibilisation). |
| [`imprimerie`](domaines/imprimerie.md) | C | Folder (3) — domaine **métier/pro** (capteurs bruit Baillet). **Léger — hub conservé.** |
| [`sante`](domaines/sante.md) | C | Folder (2) — `cardio_nuit`, `sommeil`. **Léger — hub conservé.** `sommeil` = draft `v0.9` non validé. |

---

## 2. Tier 2 — Domaines feuilles (entrée légère, sans hub)

| Domaine | Note |
|---|---|
| `vmc` | Sous-système réel, mono-contrat. *Rich leaf* — promotion Tier 1 possible plus tard. |
| `visite` | Mono-contrat. **Consommé par ECS** (`presence_visiteur`) — réf. croisée à signaler. |
| `babysitting` | Mode de présence. |
| `simulation_presence` | Mode de présence. |
| `cumulus_petite_maison` | Adjacent ECS, mono-contrat. |
| `batteries` | Mono-contrat. |
| `volets_pluie` | Mono-contrat. Dérive **cosmétique** de slug d'automatisation repérée (triage). |
| `switchbot_transactionnel` | Patron transactionnel, mono-contrat. |
| `mouvements` | Mono-contrat. |
| `mobile.high_accuracy.contextuel` | Mobile, mono-contrat. |
| `bssid` | Réseau, mono-contrat (à la frontière du système). |

---

## 3. Contrats système / transverses (non-domaines métier — pas de hub de domaine)

| Contrat | Note |
|---|---|
| `arsenal_self` | Contrat du système sur lui-même. |
| `arsenal_nas` | Supervision NAS — **frontière externe** (partie hors HA). **Hors hub** (décision v1). |
| `parametres_invalides` | Doctrine des paramètres invalides ; entités citées = **placeholders** (`yyy/zzz`). |
| `notifications` (+ `architecture/notifications_mobiles.md`) | Mécanisme transverse de notification. |
| `ressources_lovelace` | Ressources UI — **rattaché à `ui_lovelace`** (facette). |
| `zones` | Zones HA. |
| `ping_lan_synthese` | Synthèse réseau LAN. |
| `homekit_diagnostic` | Diagnostic HomeKit. |
| `ups_arret_ha` | Arrêt HA sur UPS. |
| `publication` (`securite_publication_git`) | Gouvernance de publication Git. |
| `integrite_parametres` *(architecture seule)* | Intégrité des paramètres. |
| `infrastructure_puissance` *(architecture seule)* | Infrastructure d'alimentation. |
| `aeration_recommandation` (C·A) | **Contrat transverse / recommandation.** Distinct de `aeration_blocage_chauffage` ; **non rattaché** et **sans hub dédié** (décision v1). |

---

## 4. Hors hubs — objets non-domaine (pivots / index de famille)

| Objet | Nature | Destination |
|---|---|---|
| `documentation` *(audit)* | Rapports **méta** sur le dépôt (audit structurel, audit hypertexte) | pivot `cluster_meta` |
| `perception_externe` *(audit)* | Rapport **méta** « perception externe du dépôt » (non normatif, non remédiant) | pivot `cluster_meta` |
| `architecture` *(audit)* | Audit **de la famille** architecture (pas un domaine) | pivot `cluster_meta` / index architecture |
| `transverses` *(audit + changelog)* | Buckets cross-domaines (`hysteresis_5_domaines`, cadrage CI Lovelace) | pivots (`matrice_cycle_audit`, `registre_ch`) |
| Infra famille architecture (`00_system_log`, `01_logger`, `02_logbook`, `00_structure_includes/`, `01_recorder/`, `02_etiquettes/`, `03_doctrines/`) | Doctrine/infra **interne** à `architecture/` | index intra-famille `architecture/` |

---

## 5. Notes taxonomiques (arbitrages actés)

1. **`bouclage` ⊂ ECS.** Tous ses documents s'intitulent « ECS — BOUCLAGE ». Il est traité comme **sous-domaine** dans le hub `ecs`, **pas** comme hub propre. Contrat **canonique** = `contrats/bouclage.md` (le `contrats/ecs/04_bouclage_ecs_sous_systeme.md` est un **renvoi**).
2. **`ui` + `lovelace` = un domaine, deux façades.** Référence normative (`ui/`) + artefacts de cycle Lovelace (`audits/.../lovelace/`, `19_button_card_templates/`). Hub unique `ui_lovelace`.
3. **`temperature_interieure` et `humidite_relative_interieure` = domaines propres**, distincts de `meteo` (extérieure). Logés **physiquement** sous `contrats/meteo/` par héritage — l'emplacement n'est **pas** la taxonomie.
4. **`perception_externe` ≠ météo.** « perception externe » = regard méta sur le dépôt, **sans rapport** avec les « capteurs externes » météo. Faux ami à neutraliser.
5. **« CH-x » est relatif au domaine.** Deux séries homonymes : **Chauffage-CI** (`CHANGELOG_CH1..6`, mal classés sous `climatisation/`) et **Alarme** (`*_CHx_alarme`). La climatisation **n'utilise pas** « CH-x ». Détail dans le pivot `registre_ch`.
6. **`energie_chaudiere`** : nom canonique du domaine ; fichier réel `contrats/bluetti.md`. Couche dérivée vérifiée fidèle au runtime.
7. **`aeration_recommandation` vs `aeration_blocage_chauffage`** : deux objets distincts (recommandation vs machine d'état de blocage). `aeration_recommandation` reste un **contrat transverse sans hub** (décision v1).
8. **`voiture`** : `architecture/voiture.md` contient un **contenu erroné** (copie d'aération) ; le hub devra pointer vers le contrat, pas vers cette architecture, tant que non corrigée.
9. **`vacances` ↔ `chauffage`** : la chaîne vacances vise les contrats chauffage `65_pre_confort_retour_vacances` / `66_adaptation_consigne_vacances` — réf. croisée, à représenter sans double rattachement.

---

## 6. Décisions de cadrage actées (v1)

- **`humidite_relative_interieure`** : Tier 1, domaine propre **non audité** — absence d'audit = **état de cycle**, pas un défaut.
- **`aeration_recommandation`** : **non rattaché** à `aeration_blocage_chauffage` ; conservé comme **contrat transverse / recommandation** ; **pas de hub** en v1.
- **Tier 1 légers** (`deshumidificateur`, `ouvertures`, `imprimerie`, `sante`) : **conservés en Tier 1** — carte explicite plutôt qu'invisibilisation prématurée.
- **Contrats système / transverses** : **aucun hub de domaine** en v1 ; `arsenal_nas` reste **hors hub**, à la frontière externe.

---

*v1 de `navigation/carte_domaines.md`. Document non normatif. Aucun lien, aucun hub, aucun fichier de famille créé.*
