# Registre des anomalies transverses Arsenal

> **Document de gouvernance transverse — non normatif.**
> Inventaire vivant des anomalies connues, signalées et non corrigées.
> Chaque entrée indique la source, la nature et le statut.
> Ce registre ne se substitue pas aux rapports d'audit de domaine.

---

## 1. Anomalies de nommage / fichiers

### 1.1 Double underscore — `contrats/aeration_blocage_chauffage/socle_transversal/`

| Champ | Valeur |
|---|---|
| Fichier | `socle_transversal/01__objet_perimetre_statut.md` |
| Convention attendue | `01_objet_perimetre_statut.md` (simple underscore) |
| Source | Audit README `contrats/aeration_blocage_chauffage/` |
| Statut | **✅ CLOS — 2026-06-05.** Fichier renommé en `01_objet_perimetre_statut.md` (plan, Étape 4) ; réf `changelog/v14.md` mise à jour ; README déjà aligné. Entrée conservée pour trace. |
| Impact | Lien mort depuis le README (pointe vers `01_`) |

### 1.2 Typo — `contrats/boiler/guard_expostion_ha.md`

| Champ | Valeur |
|---|---|
| Fichier | `contrats/boiler/guard_expostion_ha.md` |
| Coquille | `expostion` → `exposition` |
| Source | Hub navigation `boiler` — Points de vigilance |
| Statut | **✅ CLOS — 2026-06-05.** Fichier renommé en `guard_exposition_ha.md` (plan, Étape 3) ; réfs `dependances_inter_domaines.md` et `changelog/v12_2.md` mises à jour. Entrée conservée pour trace. |
| Impact | Cosmétique — nom trompeur |

### 1.3 Référence morte — `contrats/chauffage/30_decision_centrale.md`

| Champ | Valeur |
|---|---|
| Fichier | `contrats/chauffage/30_decision_centrale.md` (ligne 8) |
| Référence | `AUDIT_CHAINE_MQTT_ACK_ECS.md` (supprimé en v12.3) |
| Source | Arbitrage audit README `contrats/boiler/` |
| Statut | **✅ CLOS — 2026-06-05.** Ligne 8 corrigée (plan, Étape 1) : réfs mortes `CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` + `AUDIT_CHAINE_MQTT_ACK_ECS.md` supprimées, renvoi unique vers `contrats/boiler/socle_transactionnel.md` (cible existante). Entrée conservée pour trace. |
| Impact | Lien mort dans un contrat normatif |

### 1.4 Nommage hérité — `resilience_electrique` (migration documentaire — **clôturée**)

**Cause :** nommage hérité après **refonte du domaine `pannes`** ; **6 références internes non mises à jour**. Les liens morts en sont la *conséquence*, pas la nature du défaut.

| Champ | Valeur |
|---|---|
| Cause | Refonte du domaine `pannes` : le contenu de `resilience_electrique` a été **relocalisé** sous `contrats/pannes/secteur/`, mais 6 renvois internes n'ont pas suivi la migration. Défaut de migration documentaire, pas sous-domaine manquant. |
| Fichiers porteurs | `contrats/pannes/secteur/` : `10_socle.md` (×2, L49 + L121), `10_temporalite.md` (L18), `20_chauffage_et_ecs.md` (L16), `30_cycle_vie_et_signalisation.md` (×2, L16 + L22) |
| Renvois | 6 liens vers deux racines inexistantes : `contrats/resilience_electrique/…` (×4) et `architecture/resilience_electrique/…` (×2) |
| Cibles réelles | `00_panne_secteur_socle` → `10_socle.md` · `01_panne_secteur_resilience_thermique` → `20_chauffage_et_ecs.md` · `10_temporalite` → `10_temporalite.md` (à plat) · `20_fallback` → contenu **inline** dans `10_socle.md` (pas de fichier) |
| Conséquence (historique) | 6 liens morts dans des contrats normatifs — **résorbés le 2026-06-05** par le reroute. Aucune perte de contenu. |
| Source | Revue contradictoire du plan P1 + note d'arbitrage `resilience_electrique` |
| Arbitrage | **B1 — reroute à plat vers `pannes/secteur/`** (acté). Aucun paquet `resilience_electrique/` créé (éviterait une double source de vérité). |
| Statut | **✅ CLOS — 2026-06-05.** Reroute des 6 renvois exécuté (plan, Étape 6) et renommage `10_`→`11_temporalite` exécuté (Étape 2). 0 référence `resilience_electrique` résiduelle dans les contrats. Entrée conservée pour trace. |
| Dépendance d'ordre (honorée) | Le renvoi temporalité (`10_socle.md:49`) vise bien `11_temporalite.md` post-renommage ; Étapes 2 et 6 exécutées en commits séparés. |

---

## 2. Anomalies structurelles documentaires

### 2.1 Doublon garage — `contrats/eclairage/`

| Champ | Valeur |
|---|---|
| Fichiers | `garage.md` et `garage_implementation.md` |
| Problème | Même titre (`CONTRAT D'IMPLÉMENTATION — script.garage_toggle`), même cible |
| Source | Hub navigation `eclairage` — Points de vigilance |
| Statut | **À arbitrer** — fusion ou distinction à documenter |
| Impact | Ambiguïté sur le contrat de référence |

### 2.2 Double titre README — domaine `boiler`

| Champ | Valeur |
|---|---|
| Fichiers | `contrats/boiler/README.md` et `outils_externes/boiler_pi/README.md` |
| Problème | Même titre (`Boiler Pi · Documentation`) — README contrats = redirect vers outils_externes |
| Source | Hub navigation `boiler` — Points de vigilance |
| Statut | **Accepté en l'état** — redirect explicite, à clarifier si confusion |
| Impact | Confusion potentielle pour un lecteur externe |

### 2.3 Double emplacement — `bouclage`

| Champ | Valeur |
|---|---|
| Fichiers | `contrats/bouclage.md` (racine) et `contrats/ecs/04_*/` |
| Problème | Deux ancrages pour le même sous-domaine |
| Source | Hub navigation `ecs` — Points de vigilance (`Conflit ecs/04 ↔ bouclage.md`) |
| Statut | **À arbitrer** — décision d'hébergement unique requise |
| Impact | Ambiguïté de source de vérité |

### 2.4 Double préfixe `10_` — `contrats/pannes/secteur/`

| Champ | Valeur |
|---|---|
| Fichiers | `secteur/10_socle.md` et `secteur/10_temporalite.md` |
| Problème | Même préfixe numérique, pas d'ordre relatif documenté |
| Source | Hub navigation `pannes` — Points de vigilance |
| Statut | **✅ CLOS — 2026-06-05.** `10_temporalite.md` renommé `11_temporalite.md` (Étape 2) ; séquence `secteur/` déterministe (10/11/20/30). Trace conservée. |
| Impact | Séquence non déterministe |

### 2.5 Description obsolète — `contrats/README.md`

| Champ | Valeur |
|---|---|
| Fichier | `contrats/README.md` |
| Problème | Décrit la famille comme plate alors que 14 domaines sont folderisés |
| Source | Audit README `contrats/` — P2 non traité |
| Statut | **✅ CLOS — 2026-06-05.** Description mise à jour (plan, Étape 5) : structure mixte (14 domaines folderisés + fichiers plats), « dossier ou fichier ». Entrée conservée pour trace. |
| Impact | Description partiellement inexacte |

---

## 3. Anomalies de gouvernance documentaire (hubs navigation)

### 3.1 Alarme — cycle CH-x

| Anomalie | Détail |
|---|---|
| Absent de `audits/index.md` | Les chantiers alarme ne sont pas référencés dans l'index d'audit |
| Trous CH3 / CH5 | Aucun artefact pour ces chantiers |
| CH4 clôture orpheline | Clôture sans rapport ni plan d'action |
| CH6 atypique | Structure hors-norme vs CH1/CH2/CH4 |
| Double numérotation | Convention `CH-x` partagée avec chauffage mais non qualifiée |

### 3.2 Chauffage — gouvernance CI

| Anomalie | Détail |
|---|---|
| `validation_L1` | Entité de validation non contractualisée |
| Double numérotation CH-x | Chantiers classés dans `changelog/chantiers/climatisation/` malgré appartenance chauffage |
| CH-x mal classés | Voir `navigation/pivots/registre_ch.md` |

### 3.3 ECS — cohérence multi-sources

| Anomalie | Détail |
|---|---|
| Conflit `ecs/04` ↔ `bouclage.md` | Double emplacement (voir §2.3) |
| Double stage-2 inédit | Structure d'audit sans équivalent dans les autres domaines |
| Deux états d'audit coexistants | Rapport actif + éléments de clôture simultanés |
| Thread offsets thermiques | Chantier ouvert sans plan d'action formalisé |
| Aucun chantier runtime watchdog | Lacune identifiée, non adressée |

### 3.4 Vacances — cohérence pipeline

| Anomalie | Détail |
|---|---|
| Deux sens de « clos » | Ambiguïté sémantique dans les artefacts d'audit |
| Validation runtime à situer | Stade de validation non assigné |
| Hétérogénéité de pipeline | Phases VAC-IMP-x de longueur et nature variables |
| `mode_maison` | Référence à une entité non contractualisée |

---

## 4. Anomalies d'architecture hébergée

### 4.1 `capteurs_meteo.md` — périmètre étendu

| Champ | Valeur |
|---|---|
| Fichier | `architecture/capteurs_meteo.md` |
| Problème | Titre « météo & **climat intérieur** » — couvre les domaines co-hébergés `temperature_interieure` et `humidite_relative_interieure` |
| Source | Hub navigation `meteo` — Points de vigilance |
| Statut | **Accepté** — doc antérieur à l'arbitrage de séparation |

### 4.2 `axe_temperature.md` — hébergement incohérent

| Champ | Valeur |
|---|---|
| Fichier | `contrats/meteo/axe_temperature.md` |
| Problème | Axe température **intérieure** hébergé dans `contrats/meteo/` par héritage |
| Source | Hub navigation `meteo` — Points de vigilance |
| Statut | **Accepté** — arbitrage carte §5.3 acté |

### 4.3 `interface_ha_boiler_bridge.md` — hébergement sous `chauffage/`

| Champ | Valeur |
|---|---|
| Fichier | `architecture/chauffage/interface_ha_boiler_bridge.md` |
| Problème | Architecture du domaine `boiler` hébergée sous `architecture/chauffage/` |
| Source | Hub navigation `boiler` — Points de vigilance |
| Statut | **Accepté** — logique (interface chauffage↔boiler) |

---

## 5. Synthèse et priorisation

| Priorité | Anomalie | Action |
|---|---|---|
| **Clos** | `01__objet_perimetre_statut.md` — double underscore | Renommage exécuté (Étape 4) — voir §1.1 |
| **Clos** | `guard_expostion_ha.md` — typo | Renommage exécuté (Étape 3) — voir §1.2 |
| **Clos** | `30_decision_centrale.md` — référence morte | Référence corrigée (Étape 1) — voir §1.3 |
| **Clos** | `pannes/secteur/` — double `10_` | Renommage `10_`→`11_temporalite` exécuté (Étape 2) — voir §2.4 |
| **Clos** | `resilience_electrique` — nommage hérité / 6 renvois | Reroute à plat exécuté (B1, Étape 6) — voir §1.4 |
| **P2** | `eclairage/garage.md` vs `garage_implementation.md` | Arbitrage fusion/distinction |
| **P2** | Double emplacement `bouclage` | Arbitrage hébergement unique |
| **Clos** | `contrats/README.md` — structure plate vs dossiers | Description mise à jour (Étape 5) — voir §2.5 |
| **Accepté** | Double titre README `boiler` | Intentionnel — redirect explicite |
| **Accepté** | `capteurs_meteo.md` périmètre étendu | Antérieur à l'arbitrage |
| **Accepté** | `axe_temperature.md` dans `contrats/meteo/` | Arbitrage carte §5.3 |
| **Accepté** | `interface_ha_boiler_bridge.md` sous `chauffage/` | Logique fonctionnelle |

---

> Dernière mise à jour : issue de la session d'audit README (juin 2026).
> Source : hubs navigation (Points de vigilance), audits README, session de travail.
