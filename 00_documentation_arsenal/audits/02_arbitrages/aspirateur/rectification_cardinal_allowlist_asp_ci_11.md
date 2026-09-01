# Rectification factuelle — cardinal de l'allowlist d'`ASP-CI-11` cité par `Q1`

| Champ | Valeur |
|---|---|
| **Nature** | **Rectification factuelle** d'un cardinal. **Aucun nouvel arbitrage n'est rendu.** |
| **Date** | 2026-09-01. |
| **Acte concerné** | [`Q1`](arbitrage_mission_arsenal_ouverte_et_session_robot_active.md) §2, tableau des faits, **fait n° 8**. `Q1` n'est **pas** réécrite et reste scellée sur son SHA. |
| **SHA scellé par `Q1`** | `54106296b1fe7357a6c3220d3d4fa3c2a3757e1e`. |
| **SHA probant** | `d35e465839188132f80cda46aa82be6f32319adf` (`main`, arbre propre) — `check_aspirateur_contracts.py` y est **identique** au SHA de `Q1`. |
| **Portée** | **Le cardinal, et rien d'autre** : « huit » → « neuf ». Aucune clause amendée, aucun choix technique, aucun identifiant attribué. |
| **Véhicule** | Décidé le 2026-09-01 — [`C45`](../../04_chantiers/aspirateur/c45_propagation_arbitrages_q1_q2.md) §4.1 ; exécuté au Lot 1. |

---

## 1. Correction

**Formulation erronée**, reproduite et non effacée — `Q1` §2, fait n° 8, au SHA scellé :

> « `ASP-CI-11` interdit mécaniquement à tout fichier hors des **huit** nommés — les arbres Lovelace
> inclus — de mentionner l'entité de verdict. […] »

**Formulation rectifiée :**

> « `ASP-CI-11` interdit mécaniquement à tout fichier hors des **neuf** nommés — les arbres Lovelace
> inclus — de mentionner l'entité de verdict. […] »

**Seul le mot « huit » devient « neuf ».** Le reste du fait, sa source (`RC-02`) et sa conclusion
sont repris à l'identique.

---

## 2. Preuve du décompte

Dans `scripts/arsenal_contracts/check_aspirateur_contracts.py`, l'allowlist n'est pas déclarée d'un
bloc : elle est **calculée** comme l'**union** de `RUNTIME_FICHIERS`, des clés de `WRITERS_VERDICT`
et de `LECTEURS_VERDICT`. Le cardinal est donc celui de cette union, jamais la somme des périmètres :

**5 + 3 + 2 − 1 = 9**

Le **− 1** est l'**unique recouvrement** : `lancer_mission.yaml` appartient à la fois à
`RUNTIME_FICHIERS` et aux clés de `WRITERS_VERDICT` — un seul fichier, compté une seule fois.
Écrivains et lecteurs purs sont **disjoints**, et aucun lecteur pur n'est un fichier runtime `L1` :
il n'existe **aucun autre double comptage**.

| # | Fichier | Rôle vis-à-vis du verdict |
|---|---|---|
| 1 | `10_scripts/aspirateur/lancer_mission.yaml` | runtime `L1` **et** écrivain `W1` — le recouvrement |
| 2 | `04_input_texts/aspirateur/mission.yaml` | runtime `L1` |
| 3 | `12_template_sensors/aspirateur/etat_canonique.yaml` | runtime `L1` |
| 4 | `12_template_sensors/aspirateur/motif_lisible.yaml` | runtime `L1` |
| 5 | `12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml` | runtime `L1` |
| 6 | `10_scripts/aspirateur/conduire_mission.yaml` | écrivain `W2` |
| 7 | `11_automations/aspirateur/supervision_mission.yaml` | écrivain `W3` |
| 8 | `11_automations/aspirateur/notification_mission.yaml` | lecteur pur nominatif |
| 9 | `11_automations/aspirateur/remise_a_zero_composition.yaml` | lecteur pur nominatif (amendement `U0`) |

**Le compte était déjà de neuf au SHA de `Q1`** : le neuvième fichier est entré dans
`LECTEURS_VERDICT` par l'amendement `U0` — commit `a360bfe`, 2026-08-29 —, **antérieur** au SHA
`5410629` de `Q1`. L'écart n'est donc pas une péremption par évolution ultérieure du dépôt.

**Le compte exact était déjà établi**, sur ces mêmes constantes, par
[`Q2`](arbitrage_projection_mission_arsenal_ouverte_vers_interface.md) §3, fait n° 7 : « cette
allowlist compte **neuf fichiers** […] ». La présente rectification ne fait qu'y aligner `Q1`.

---

## 3. Effets

`Q1` n'invoque le fait n° 8 que pour la **nominativité** de l'allowlist — un fichier non nommé ne
peut mentionner le verdict —, propriété vraie **quel que soit** le cardinal ; `Q2` §3 fait n° 6
l'énonce d'ailleurs sans cardinal. **Le raisonnement et la décision de `Q1` sont intacts.**

Demeurent **inchangés** :

- la **distinction** tranchée par `Q1` entre « mission Arsenal ouverte » et « session robot active » ;
- les **autorités** qu'elle décide — verdict de classe `O` et témoin natif Roborock ;
- l'**interdiction faite à Lovelace** de lire directement le helper de verdict ;
- **`Q2`** et tous ses énoncés.

La rectification **ne retient aucun choix technique**, **n'attribue aucun identifiant**, **ne ferme
ni ne requalifie aucun constat** — `AUD-ASP-01`, `CC-01`, `RC-02`, `AUD-ASP-04` —, **ne ferme aucun
chantier** et **ne modifie aucun état de clôture** du domaine `aspirateur`.

---

## 4. Traçabilité

- [`Q1`](arbitrage_mission_arsenal_ouverte_et_session_robot_active.md) — acte rectifié sur ce seul
  cardinal, **non réécrit**.
- [`Q2`](arbitrage_projection_mission_arsenal_ouverte_vers_interface.md) — établissement ultérieur
  du compte exact (§3, fait n° 7), **non modifié**.
- [`C45`](../../04_chantiers/aspirateur/c45_propagation_arbitrages_q1_q2.md) — véhicule décidé
  (§4.1), exécution au Lot 1 (§5.1).

Les rapports historiques —
[audit initial](../../01_rapports/aspirateur/audit_conformite_domaine_post_integration.md),
[contre-expertise](../../02_contre_expertises/aspirateur/contre_expertise_domaine_aspirateur.md),
[confrontation](../../02_contre_expertises/aspirateur/confrontation_audit_contre_expertise_aspirateur.md)
— portent le même cardinal inexact et sont **laissés intacts** : ils sont datés de leur SHA, `Q1`
§4.4 et `Q2` §10 posant explicitement qu'ils ne sont pas réécrits.
