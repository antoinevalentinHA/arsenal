# Références aux sources amont — **V3**

> **Aucune correction V3 sur ce fichier.**

> **Corrections V2 après audit :** garde de valeur absente restituée (§3) ;
> fait n° 8 requalifié en comportement prédit non testé (§5) ; fait n° 10
> corrigé — les intervalles sont nominaux, sans borne supérieure démontrable
> (§6) ; deux constantes hors périmètre retirées ; tableau de falsifiabilité
> refait (§8).

**Home Assistant `2026.8.3`** — dépôt `home-assistant/core`, tag `2026.8.3`.
**`python-roborock` `5.31.1`** — dépôt `Python-roborock/python-roborock`, tag `v5.31.1`.

La version de bibliothèque n'est pas supposée : elle est **lue dans le
manifeste de l'intégration** à ce tag.

---

## 1. Manifeste de l'intégration

`homeassistant/components/roborock/manifest.json`

```json
{
  "domain": "roborock",
  "integration_type": "hub",
  "iot_class": "local_polling",
  "quality_scale": "silver",
  "requirements": [
    "python-roborock==5.31.1",
    "vacuum-map-parser-roborock==0.1.5"
  ]
}
```

> **Fait n° 1.** L'intégration de Home Assistant `2026.8.3` épingle
> `python-roborock==5.31.1`. Toute la suite se lit à ce tag.

---

## 2. Plafonds d'usure — constantes littérales

`roborock/const.py` (v5.31.1)

```python
MAIN_BRUSH_REPLACE_TIME   = 1080000
SIDE_BRUSH_REPLACE_TIME   =  720000
FILTER_REPLACE_TIME       =  540000
SENSOR_DIRTY_REPLACE_TIME =  108000
MOP_ROLLER_REPLACE_TIME   = 1080000
STRAINER_REPLACE_TIME     =     150
CLEANING_BRUSH_REPLACE_TIME =   300
DUST_COLLECTION_REPLACE_TIME =   90
FLOOR_CLEANER_REPLACE_TIME  =   300
```

Commentaire d'origine : durée totale dont disposent les consommables avant que
le constructeur n'en recommande le remplacement.

> **Fait n° 2.** Les quatre plafonds du périmètre V1 valent, en secondes :
> **1 080 000 · 720 000 · 540 000 · 108 000**, soit **300 h · 200 h · 150 h · 30 h**.

> **Fait n° 3 — piège de lecture, signalé.** Les trois constantes
> `STRAINER_REPLACE_TIME`, `CLEANING_BRUSH_REPLACE_TIME` et
> `DUST_COLLECTION_REPLACE_TIME` (150, 300, 90) **ne sont pas des secondes** :
> les champs qu'elles bornent sont nommés au pluriel (`*_work_times`) et
> comptent des **occurrences**. Le commentaire du fichier est trompeur sur ce
> point. Aucune de ces trois constantes n'est utilisée par ce cadrage.

---

## 3. Calcul du temps restant

`roborock/data/v1/v1_containers.py` (v5.31.1) — classe `Consumable`

Champs :

```
main_brush_work_time · side_brush_work_time · filter_work_time
filter_element_work_time · sensor_dirty_time · strainer_work_times
dust_collection_work_times · cleaning_brush_work_times · moproller_work_time
```

Propriétés :

Chaque propriété porte une **garde de valeur absente** : le calcul n'a lieu que
si le champ de travail est renseigné, sinon la propriété vaut `None`.

| Propriété | Calcul |
|---|---|
| `main_brush_time_left` | `MAIN_BRUSH_REPLACE_TIME - main_brush_work_time` **si le champ est renseigné, sinon `None`** |
| `side_brush_time_left` | `SIDE_BRUSH_REPLACE_TIME - side_brush_work_time` **si renseigné, sinon `None`** |
| `filter_time_left` | `FILTER_REPLACE_TIME - filter_work_time` **si renseigné, sinon `None`** |
| `sensor_time_left` | `SENSOR_DIRTY_REPLACE_TIME - sensor_dirty_time` **si renseigné, sinon `None`** |
| `dust_collection_time_left` | `DUST_COLLECTION_REPLACE_TIME - dust_collection_work_times` **si renseigné, sinon `None`** |

> **Fait n° 4.** Le « temps restant » est calculé **par la bibliothèque**.
> Home Assistant n'en fait aucune arithmétique.

> **Fait n° 4 bis — ajouté en V2.** La garde de valeur absente est **portée
> jusqu'à l'entité** : une donnée protocolaire manquante produit une propriété
> nulle, donc un capteur **indisponible**, et non un zéro. Le témoin binaire
> d'entretien requis devra **classer explicitement** ce cas, sous peine de lire
> un trou comme « non dû ». Voir `06_ENTITES_ENTRETIEN.md` §8.

> **Fait n° 5.** `dust_collection_time_left` est **arithmétiquement invalide**
> sur cet appareil : le compteur observé dépasse largement la constante, ce qui
> produirait une valeur négative. Home Assistant **n'expose aucun capteur** pour
> cette propriété. Cela fonde la décision D-17.

---

## 4. Exposition côté Home Assistant

`homeassistant/components/roborock/sensor.py` (tag `2026.8.3`)

Quatre descriptions de capteur, de forme identique :

| Clé | `value_fn` |
|---|---|
| `main_brush_time_left` | `lambda data: data.consumable.main_brush_time_left` |
| `side_brush_time_left` | `lambda data: data.consumable.side_brush_time_left` |
| `filter_time_left` | `lambda data: data.consumable.filter_time_left` |
| `sensor_time_left` | `lambda data: data.consumable.sensor_time_left` |

Attributs communs : `native_unit_of_measurement = UnitOfTime.SECONDS`,
`device_class = SensorDeviceClass.DURATION`,
`entity_category = EntityCategory.DIAGNOSTIC`.
**Aucun `state_class`.**

Autres descriptions utiles :

| Clé | `value_fn` |
|---|---|
| `total_cleaning_time` | `lambda data: data.clean_summary.clean_time` |
| `last_clean_start` | `data.clean_summary.last_clean_record.begin_datetime` si présent, sinon `None` |
| `last_clean_end` | `data.clean_summary.last_clean_record.end_datetime` si présent, sinon `None` |

> **Fait n° 6.** L'unité native est la **seconde**. La restitution en heures est
> une conversion d'affichage. L'absence de `state_class` explique
> mécaniquement l'absence de statistiques longue durée.

---

## 5. Remise à zéro — primitive exacte

`roborock/devices/traits/v1/consumeable.py` (v5.31.1)

`ConsumableAttribute` :

```
SENSOR_DIRTY_TIME     = "sensor_dirty_time"
FILTER_WORK_TIME      = "filter_work_time"
SIDE_BRUSH_WORK_TIME  = "side_brush_work_time"
MAIN_BRUSH_WORK_TIME  = "main_brush_work_time"
STRAINER_WORK_TIME    = "strainer_work_times"
CLEANING_BRUSH_WORK_TIME = "cleaning_brush_work_times"
```

Méthode de remise à zéro :

```python
await self.rpc_channel.send_command(RoborockCommand.RESET_CONSUMABLE,
                                    params=[consumable.value])
...
await self.refresh()
```

`homeassistant/components/roborock/button.py` (tag `2026.8.3`) —
`RoborockButtonEntity.async_press` :

```python
await self._consumable.reset_consumable(self.entity_description.attribute)
```

encadré d'un seul `except RoborockException` traduit en `HomeAssistantError`.
**Aucun `async_request_refresh`, aucun `async_write_ha_state` ne suit.**

> **Fait n° 7.** La bibliothèque **relit immédiatement** l'état du consommable
> après la remise à zéro. En revanche, le bouton de Home Assistant **ne force
> aucun rafraîchissement d'entité** : l'état visible de l'entité ne change
> qu'au cycle suivant du coordinateur.
>
> *Contraste instructif, dans le même fichier :* la variante A01 appelle bien
> `await self.coordinator.async_request_refresh()` dans un bloc `finally`.
> L'absence est donc **spécifique** au chemin V1, pas un oubli de lecture.

> **Fait n° 8 — REQUALIFIÉ EN V2 : comportement prédit, non testé.**
>
> **Ce que les sources établissent :** la bibliothèque envoie la commande de
> remise à zéro avec le nom du champ de travail en paramètre, puis relit l'état
> du consommable.
>
> **Ce qu'elles n'établissent pas :** que l'appareil remette effectivement ce
> champ à zéro. **C'est un comportement de micrologiciel.** L'attente — le
> capteur remonte exactement au plafond — est une **prédiction**, non un fait
> de source.
>
> **Pourquoi la distinction compte.** C'est très exactement ce que la
> confirmation par relecture est censée vérifier. Classer ce point en fait
> acquis, comme le faisait la V1, **retirait son objet au contrôle**.

Conditionnement des boutons de dock : les remises à zéro de filtre à charpie et
de brosse de lavage ne sont créées **que si** le mode de lavage de serpillière
est présent sur l'appareil.

> **Fait n° 9.** Ces deux boutons n'existent pas sur l'appareil observé, ce qui
> confirme mécaniquement que le périmètre V1 se limite à **quatre** éléments.

---

## 6. Cadence du coordinateur

`homeassistant/components/roborock/const.py` (tag `2026.8.3`)

```python
V1_CLOUD_IN_CLEANING_INTERVAL  = timedelta(seconds=30)
V1_CLOUD_NOT_CLEANING_INTERVAL = timedelta(minutes=1)
V1_LOCAL_IN_CLEANING_INTERVAL  = timedelta(seconds=15)
V1_LOCAL_NOT_CLEANING_INTERVAL = timedelta(seconds=30)
IMAGE_CACHE_INTERVAL           = timedelta(seconds=30)
```

*(Les constantes propres aux familles A01 et Q10, citées par la V1, sont
retirées : elles ne concernent aucun appareil du périmètre.)*

Sélection de l'intervalle, `components/roborock/coordinator.py` :
le coordinateur est **construit** avec l'intervalle local au repos, puis, à
chaque cycle, choisit selon deux critères — en nettoyage ou non, connecté en
local ou non. Si la connexion locale échoue, il **bascule** sur l'intervalle
nuage au repos et signale un incident.

Planification, `homeassistant/helpers/update_coordinator.py` :
`_schedule_refresh()` est appelé **dans le bloc `finally` du rafraîchissement**,
donc **après** que celui-ci s'est terminé, et calcule
`next_refresh = int(loop.time()) + self._microsecond + update_interval`, où
`_microsecond` est un décalage aléatoire d'échelonnement. Un `retry_after`
porté par un échec **remplace** l'intervalle pour le cycle suivant. Sur échec,
l'indicateur de succès passe à faux et les auditeurs ne sont notifiés que sous
conditions : **l'état de l'entité peut ne pas avancer du tout**.

> **Fait n° 10 — CORRIGÉ EN V2.**
>
> **30 s en connexion locale, 60 s en repli nuage. Ces valeurs sont des
> périodes nominales de planification, pas des bornes.** Le coordinateur
> replanifie à la fin de chaque rafraîchissement : l'écart réel vaut au moins
> l'intervalle **augmenté de la durée du cycle** et d'un décalage
> d'échelonnement, et un échec ou un `retry_after` l'allonge.
> **Aucune borne temporelle supérieure n'est démontrable.**
>
> **60 s est en outre la cadence du mode dégradé**, atteinte seulement si la
> connexion locale échoue — pas un maximum. Et **le mode de connexion de
> l'instance n'a pas été relevé** : voir `05_DIAGNOSTICS_SANITISES.md` §11.
>
> **Conséquence directe sur le lot Maintenance.** Une fenêtre de confirmation
> adossée à l'idée de « couvrir au moins un cycle complet » **peut expirer sur
> une remise à zéro réussie**. Comme cette remise à zéro est unique,
> irréversible et sans seconde tentative, l'opérateur recevrait un **faux
> négatif sur un acte qu'il ne peut pas défaire**. C'est ce qui déplace
> l'arbitrage **A-2** du choix d'une durée vers le **comportement à
> l'expiration**.
>
> *La V1 affirmait « 60 s est la borne haute ». Cette affirmation est retirée.*

---

## 7. Vidage — ce que les sources disent exactement

### 7.1 Les commandes existent dans la bibliothèque

`roborock/roborock_typing.py` (v5.31.1) :

```
APP_START_COLLECT_DUST            = "app_start_collect_dust"
APP_STOP_COLLECT_DUST             = "app_stop_collect_dust"
GET_DUST_COLLECTION_MODE          = "get_dust_collection_mode"
SET_DUST_COLLECTION_MODE          = "set_dust_collection_mode"
GET_DUST_COLLECTION_SWITCH_STATUS = "get_dust_collection_switch_status"
SET_DUST_COLLECTION_SWITCH_STATUS = "set_dust_collection_switch_status"
GET_CONSUMABLE                    = "get_consumable"
RESET_CONSUMABLE                  = "reset_consumable"
```

### 7.2 Aucun trait V1 ne les déclenche

`roborock/devices/traits/v1/dust_collection_mode.py` n'expose que la lecture et
l'écriture du **mode**. **Aucune méthode de déclenchement de vidage.**

### 7.3 Home Assistant n'expose rien pour V1

Le seul bouton de vidage de `button.py` au tag `2026.8.3` est réservé aux
appareils de la famille **B01 Q10** et appelle `api.vacuum.empty_dustbin()`.
Aucun équivalent V1. Aucun service `vacuum.*` de vidage n'existe côté Home
Assistant.

### 7.4 Classification du dock par la bibliothèque

`roborock/data/v1/v1_code_mappings.py` — `RoborockDockTypeCode` :

```
o0_dock = 0 · o1_dock = 1 · o2_dock = 2 · o3_dock = 3 · oc_dock = 5
o3_plus_dock = 6 · o4_dock = 7 · pearl_dock = 8 · … · o6_dock = 18 · …
```

`roborock/device_features.py` — `RoborockDockFeatures` :

- `is_dust_bucket_supported` vaut vrai pour les types **3, 6 et 7** uniquement ;
- `is_cleaning_brush_supported` est réservé à la série X.

`RoborockDockDustCollectionModeCode` : `smart = 0 · light = 1 · balanced = 2 · max = 4`.

> **Fait n° 11.** Le dock observé est de **type 5**, qui **n'appartient pas** à
> l'ensemble des docks à bac reconnus par la bibliothèque, alors même que
> l'appareil déclare la collecte automatique active et compte 608 cycles.
>
> **Ce désaccord n'est pas tranché par les sources.** Il est tranché par la
> **déclaration opérateur** D-12, sous le régime de preuve de `ARB-3` / `ARB-5`.
> La classification de la bibliothèque est donc réputée **incomplète pour ce
> matériel**, et non contredite par un essai.

> **Fait n° 12.** Il en découle que la V1 ne perd **rien** : la fonction est
> native et autonome, et l'absence de primitive exposée n'est pas un manque
> fonctionnel (D-18).

---

## 8. Récapitulatif de falsifiabilité

| Fait | Statut | Comment le vérifier |
|---|---|---|
| 1 à 7, 9, 11, 12 | **Vérifiable hors ligne** | Relecture des fichiers cités aux tags cités |
| 4 bis — garde de valeur absente | **Vérifiable hors ligne** | idem |
| 10 — intervalles **nominaux** | **Vérifiable hors ligne** | `const.py`, `coordinator.py` et `helpers/update_coordinator.py` du tag |
| Arithmétique des restants | **Vérifiable hors ligne** | Recalcul depuis `05_DIAGNOSTICS_SANITISES.md` §3 |
| **8 — remise à zéro effective du champ** | **PRÉDIT, NON TESTÉ** | Comportement de micrologiciel ; aucune source ne l'établit |
| **Délai réel de propagation vers l'entité** | **NON ÉTABLI** | Aucune borne supérieure démontrable |
| **Mode de connexion de l'instance** | **NON RELEVÉ** | La cadence en dépend |
| D-12 — le dock vide réellement | **DÉCLARATION OPÉRATEUR** | Le compteur est cohérent ; il ne prouve pas |

> **Correction V2.** Les trois lignes en capitales figuraient auparavant, en
> tout ou partie, du côté « vérifiable hors ligne ».
