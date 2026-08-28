# Extraits sanitaires de diagnostics — **V3**

> **Corrections V2 :** unité de la tolérance du §5 rectifiée ; mode de connexion
> de l'intégration ajouté au §11.1 comme **fait non relevé**.
>
> **Correction V3 :** l'énoncé « les trois entités qui porteraient la fenêtre
> d'heures interdites » est retiré — l'artefact n'a pas relevé lesquelles la
> portent, et la conclusion n'en dépend pas (`N-11`).

**Origine.** Relevés en **lecture seule** sur l'instance Home Assistant de
production, le 2026-08-27, via l'état des entités, le registre d'entités et le
diagnostic de l'entrée de configuration de l'intégration.

**Sanitisation appliquée.** Sont **retirés** : identifiant d'appareil, clé
locale, numéro de série, identifiant de produit, jetons, adresse de compte,
adresses réseau, points d'accès de messagerie, horodatages d'enregistrement
d'appareil, et le suffixe d'identifiant unique des entités. Ne subsistent que
les **faits strictement nécessaires** aux conclusions du cadrage.

**Aucune trace complète de diagnostic ne figure dans cet artefact.**

---

## 1. Identité matérielle retenue

| Fait | Valeur |
|---|---|
| Classe de protocole | **V1** |
| Modèle | `roborock.vacuum.a38` |
| Version de micrologiciel | `02.09.18` |
| Appareils créés par l'intégration | **2** — le robot et son dock |
| Enregistrement de l'appareil | **août 2022** (mois et année seuls) |

---

## 2. Traits exposés par l'intégration pour cet appareil

```
status · dnd · clean_summary · sound_volume · rooms · maps · map_content
consumables · device_features · network_info · child_lock · led_status
valley_electricity_timer · dust_collection_mode
```

> Aucun trait de **déclenchement** de vidage n'y figure. Voir
> `04_REFERENCES_SOURCES.md` §7.2.

---

## 3. Consommables — valeurs brutes du protocole

```json
{
  "mainBrushWorkTime":  793132,
  "sideBrushWorkTime":   51701,
  "filterWorkTime":     298747,
  "filterElementWorkTime":    0,
  "sensorDirtyTime":     93553,
  "dustCollectionWorkTimes": 608
}
```

Unité : **secondes de fonctionnement cumulé** pour les cinq premiers champs ;
**nombre d'occurrences** pour le dernier.

> **Ces six nombres sont la matière première du contrôle C2 du `README.md`.**
> L'auditeur doit pouvoir en dériver, seul, les états d'entités du §5.

---

## 4. État machine et dock

```json
{
  "state": 8,
  "cleanTime": 262,
  "cleanArea": 4637500,
  "errorCode": 0,
  "inCleaning": 0,
  "inFreshState": 1,
  "dockType": 5,
  "dustCollectionStatus": 0,
  "autoDustCollection": 1,
  "dockErrorStatus": 0
}
```

Mode de collecte de poussière lu : `{"mode": 0}` — soit le mode « intelligent »
de l'énumération amont.

Capacités déclarées par l'appareil, extrait restreint au sujet :

```
isDustCollectionSettingSupported = true
isCollectDustModeSupported       = true
isCollectDustCountShowSupported  = false
isAutoCollection2Supported       = false
```

> **Lecture.** L'appareil déclare la collecte automatique **active**
> (`autoDustCollection = 1`), n'est pas en train de collecter au moment du
> relevé (`dustCollectionStatus = 0`), et ne signale aucune erreur de dock
> (`dockErrorStatus = 0`). Le type de dock **5** n'appartient pas à l'ensemble
> des docks à bac reconnus par la bibliothèque — désaccord rapporté et tranché
> par la décision **D-12**.
>
> **`dustCollectionStatus` n'est exposé par aucune entité Home Assistant** :
> un vidage en cours n'est donc **pas observable** depuis Arsenal.

---

## 5. Entités de consommable — états relevés

| Entité | État | Unité | Valeur en secondes |
|---|---|---|---|
| `sensor.roborock_q7_max_temps_restant_brosse_principale` | `79.6855555555556` | `h` | 286 868 |
| `sensor.roborock_q7_max_temps_restant_brosse_laterale` | `185.638611111111` | `h` | 668 299 |
| `sensor.roborock_q7_max_temps_restant_filtre` | `67.0147222222222` | `h` | 241 253 |
| `sensor.roborock_q7_max_temps_restant_capteurs` | `4.01305555555556` | `h` | 14 447 |

Attributs communs : `device_class: duration`, `unit_of_measurement: h`.
Registre : `suggested_display_precision: 2`, unité suggérée par l'intégration
`h`, **pour les quatre**.

> **Vérification interne.** Chaque état, multiplié par 3 600, retombe sur un
> **entier de secondes**, à **bien moins d'une seconde près**. Cela confirme que
> la valeur native est un entier de secondes et que la conversion est un simple
> changement d'unité.
>
> *(Correction V2 : la V1 exprimait cette tolérance en heures — « 1,2 × 10⁻¹⁰ h »
> — alors que la quantité comparée est en secondes. La concordance était juste ;
> la formulation ne l'était pas.)*

---

## 6. Boutons de remise à zéro

| Entité | État |
|---|---|
| `button.roborock_q7_max_reinitialiser_le_consommable_du_filtre_a_air` | `unknown` |
| `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_principale` | `unknown` |
| `button.roborock_q7_max_reinitialiser_le_consommable_de_la_brosse_laterale` | `unknown` |
| `button.roborock_q7_max_reinitialiser_le_consommable_du_capteur` | `unknown` |

Aucun attribut hors le nom convivial. **Aucun n'a été pressé.**

Les boutons de remise à zéro de **filtre à charpie** et de **brosse de lavage**
du dock **n'existent pas** sur cet appareil.

---

## 7. Témoins d'erreur et prérequis

| Entité | État | Nature |
|---|---|---|
| `sensor.roborock_q7_max_erreur_de_l_aspirateur` | `none` | énumération fermée, > 50 valeurs |
| `sensor.roborock_q7_max_dock_erreur_de_dock` | `ok` | énumération fermée, 11 valeurs |
| `binary_sensor.entree_roborock_q7_max_penurie_d_eau` | `off` | classe `problem` |
| `binary_sensor.entree_roborock_q7_max_dock_sechage_de_la_serpilliere` | `off` | classe `running` |
| `binary_sensor.roborock_q7_max_serpilliere_fixee` | — | prérequis matériel, déjà lu par le moteur L1 |
| `binary_sensor.roborock_q7_max_nettoyage` | — | témoin de **session inachevée** |

Énumération complète du témoin d'erreur de **dock** :

```
ok · no_dustbin_or_filter · auto_empty_dock_fan_error · duct_blockage
auto_empty_dock_voltage_error · water_empty · waste_water_tank_full
maintenance_brush_jammed · dirty_tank_latch_open · no_dustbin
cleaning_tank_full_or_blocked
```

> **Fait décisif pour la décision D-16.** Quatre de ces onze valeurs —
> `no_dustbin`, `no_dustbin_or_filter`, `duct_blockage`,
> `auto_empty_dock_fan_error` — sont exactement des **défauts de vidage**.
> Le signal fiable demandé **existe déjà**, il est déjà contractualisé, et le
> moteur L1 le lit déjà comme condition de lancement. **Rien n'est à créer.**

L'énumération du témoin d'erreur **robot** comporte également `no_dustbin`,
`filter_blocked` et `strainer_error`.

---

## 8. Registre d'entités de la plateforme

| Mesure | Valeur |
|---|---|
| Entités enregistrées | **45** |
| Actives | **33** |
| Désactivées | **12** |
| Masquées | **0** |

Entités désactivées, par identifiant fonctionnel :

```
number  · volume
select  · dock_mode_de_vidage                 (catégorie : configuration)
sensor  · nombre_total_de_nettoyages
sensor  · surface_de_nettoyage_totale
switch  · dock_securite_enfant
switch  · ne_pas_deranger
switch  · recharge_en_heures_creuses          (désactivée par l'intégration)
time    · ne_pas_deranger_debut
time    · ne_pas_deranger_fin
time    · debut_des_heures_creuses            (désactivée par l'intégration)
time    · fin_des_heures_creuses              (désactivée par l'intégration)
button  · nettoyage_complet
```

> **Conséquence pour la décision D-16 — reformulée en V3.** Les entités
> **candidates** à porter une **fenêtre d'heures interdites** sont désactivées.
> Deux ensembles désactivés pourraient la porter — « ne pas déranger » et
> « heures creuses » —, et **l'artefact ne tranche pas** lequel correspond à la
> fenêtre déclarée par l'opérateur : il ne l'a pas relevé.
>
> **Ce qui suffit à la conclusion, et qui est vrai dans les deux cas :**
> **la fenêtre n'est pas observable par Arsenal.** Il ne doit donc **jamais**
> construire une alerte d'« absence de vidage » : pendant la fenêtre, un silence
> est nominal, et le système ne
> peut pas le distinguer d'une panne.

Le dock ne porte que **quatre** entités, dont deux désactivées.

---

## 9. Historisation

| Contrôle | Résultat |
|---|---|
| Historique interrogé sur 14 jours, capteur de consommable | **0 point** |
| Statistiques longue durée, quatre capteurs | **aucune** |
| Cause | Le fichier de configuration d'historisation du dépôt fonctionne en **liste d'autorisation** ; aucune entité de la plateforme n'y figure |

Conforme au chapitre `08` §6 du contrat : ce n'est pas un défaut.

---

## 10. Services exposés au moment du relevé

```
vacuum   : start · pause · return_to_base · clean_spot · clean_area
           locate · stop · set_fan_speed · send_command
roborock : get_maps · get_vacuum_current_position
           set_vacuum_goto_position · set_vacuum_zoned_cleaning
persistent_notification : create · dismiss · dismiss_all
```

> **Aucun service de vidage.** Aucun service de remise à zéro de consommable
> (la remise à zéro passe exclusivement par les entités de type bouton).

---

## 11. État du domaine Arsenal au relevé

| Entité | État |
|---|---|
| `input_text.aspirateur_mission_verdict` | `VALIDATION_EN_COURS` |
| `sensor.aspirateur_etat_canonique` | `charge` |
| `input_boolean.systeme_stable` | `on` |

Canal mobile : le dépôt ne contient **aucun** service de notification en dur ;
la cible opérateur est résolue à l'exécution depuis un helper textuel dédié,
via la couche d'abstraction centrale. Le nom du service concret n'est pas
reproduit ici.

### 11.1 Mode de connexion de l'intégration — **fait non relevé**

| Fait | Statut |
|---|---|
| L'intégration est-elle connectée à l'appareil **en local** ou **en repli nuage** ? | **NON RELEVÉ** |

**Pourquoi cela compte.** Le coordinateur est construit avec l'intervalle local
au repos (30 s) et ne bascule sur l'intervalle nuage (60 s) que si la connexion
locale échoue. Sans ce relevé, **la cadence effective de l'instance est
inconnue**, et aucune fenêtre de confirmation ne peut être dimensionnée sur elle.

**Ce que cela ne change pas.** Même si le relevé était fait, il ne fournirait
**aucune borne supérieure** : le coordinateur replanifie après la fin de chaque
rafraîchissement, et un échec allonge l'écart sans limite. Le relevé
préciserait la période nominale, pas une garantie.

**Pourquoi il n'a pas été fait.** Le relevé exigerait un accès à l'instance,
exclu par la consigne opératoire en vigueur lors de la constitution de la V2.

> *Correction V2 : la V1 ne signalait pas cette lacune et fondait une
> conclusion de cadence sur une observation qui n'en était pas une.*

---

## 12. Ce qui a été délibérément omis

Contenu des notifications persistantes actives au moment du relevé, identité
des appareils mobiles, adresses réseau, identifiants de compte et d'appareil,
et l'intégralité des champs de diagnostic sans rapport avec les conclusions
du cadrage.
