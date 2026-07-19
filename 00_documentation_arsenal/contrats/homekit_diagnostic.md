# Contrat — Diagnostic station météo Netatmo
**Arsenal** · Couche observation · v1.3

---

## Objet

Ce contrat définit la logique de diagnostic des stations météo Netatmo dans Arsenal.

Le diagnostic ne répond pas à : *« le module jardin va-t-il bien ? »*

Il répond à : **« la station entière est-elle suffisamment vivante pour qu'un redémarrage global soit injustifié ? »**

---

## 1. Périmètre utile par station

### Station 1 — `diagnostic_netatmo_enfants`

| Catégorie | Entités |
|-----------|---------|
| **Ping** | `binary_sensor.station_meteo_netatmo_1` |
| **Températures** | `sensor.temperature_chambre_enfants_1` · `sensor.temperature_chambre_parents_1` · `sensor.temperature_jardin_1` · `sensor.temperature_petite_maison` · `sensor.temperature_sejour_1` |
| **Humidités** | `sensor.humidite_relative_chambre_enfants_1` · `sensor.humidite_relative_chambre_parents_1` · `sensor.humidite_relative_jardin_1` · `sensor.humidite_relative_petite_maison` · `sensor.humidite_relative_sejour_1` |
| **CO2** | `sensor.co2_chambre_enfants` · `sensor.co2_chambre_parents` · `sensor.co2_petite_maison` · `sensor.co2_sejour` |
| **Bruit** | `sensor.bruit_chambre_enfants` |

### Station 2 — `diagnostic_netatmo_matthieu`

| Catégorie | Entités |
|-----------|---------|
| **Ping** | `binary_sensor.station_meteo_netatmo_2` |
| **Températures** | `sensor.temperature_chambre_matthieu_1` · `sensor.temperature_entree_1` · `sensor.temperature_jardin_2` |
| **Humidités** | `sensor.humidite_relative_chambre_matthieu_1` · `sensor.humidite_relative_entree_1` · `sensor.humidite_relative_jardin_2` |
| **CO2** | `sensor.co2_chambre_matthieu` · `sensor.co2_entree` |
| **Bruit** | `sensor.bruit_chambre_matthieu` |

---

## 2. Principes architecturaux

### 2.1 Sonde jardin — désignation documentaire uniquement

Le module jardin (`sensor.temperature_jardin_*`) est historiquement désigné comme sonde primaire de fraîcheur car il se met à jour plus fréquemment que les modules intérieurs.

**Cette désignation est documentaire uniquement et n'a aucun effet sur la logique de décision du diagnostic.**

Dans la logique métier, toutes les entités de la station ont strictement le même poids comme preuve de vie. Le jardin reste utile pour le diagnostic visuel dans les dashboards Arsenal (gel visible rapidement), mais le capteur de diagnostic n'agit pas sur cette intuition.

### 2.2 Preuves de vie — toutes catégories confondues

Les preuves de vie exploitables sont l'ensemble des mesures numériques de la station :

- températures
- humidités relatives
- CO2
- bruit

La logique est la suivante :

- **jardin présent** → très bon signal, mais pas de statut privilégié
- **jardin absent, autres mesures présentes** → station vivante
- **aucune donnée exploitable** → seulement là on entre dans la branche de diagnostic muet

### 2.3 Rôle du ping

Le ping (`binary_sensor.station_meteo_netatmo_*`) ne prouve **rien** sur la fonctionnalité métier de la station. Il prouve uniquement qu'**une stack IP répond encore à une sollicitation**. Une station Netatmo physiquement figée peut continuer à répondre au ping — ce cas a été observé en terrain (cf. §11).

Le ping sert uniquement à **départager observationnellement** la nature d'un silence déjà constaté :

- silence avec ping qui répond
- silence avec ping qui ne répond pas

> **Le ping ne doit jamais écraser l'existence de données réelles.**
> Si des mesures numériques remontent, la station est de fait vivante, même si le ping est contradictoire.

> **Le ping ne désigne aucune cause de panne.** Il est descriptif, pas explicatif.

---

## 3. États métier

Les noms d'états sont **strictement observationnels**. Ils décrivent ce qui est mesuré, pas ce qui est supposé en être la cause.

### `ok`

La station est considérée fonctionnelle si **au moins une entité utile de la station est exploitable**, quelle qu'elle soit.

> Toute donnée réelle de la station vaut preuve de vie suffisante.

### `muet_ping_ok`

La station ne fournit plus de mesures exploitables, mais répond encore au ping.

Conditions :

- aucune entité utile n'est exploitable
- **et** `binary_sensor.station_meteo_netatmo_*` est `on`

Lecture honnête :

> Quelque chose, dans la chaîne entre la station physique et HA, ne livre plus de mesures. La cause réelle n'est pas déductible de cette seule observation. Plusieurs causes sont compatibles : station physiquement figée mais firmware réseau encore actif, bridge HomeKit gelé, intégration Netatmo cloud désynchronisée, etc.

> **Remédiation (v1.3).** Un `muet_ping_ok` **persistant** déclenche désormais un power-cycle borné de la station — voir la politique explicite en §9.1. C'est la levée de l'abstention v1.1–v1.2 (cf. §11), motivée par la preuve terrain. Comme pour `muet_ping_ko`, cette remédiation est subordonnée à `input_boolean.systeme_stable = on` : un `muet_ping_ok` observé pendant l'instabilité post-redémarrage de HA (preuves encore `unavailable`, ping déjà remonté) est un artefact d'initialisation, non un gel réel.

### `muet_ping_ko`

La station ne fournit plus de mesures exploitables, et ne répond plus au ping.

Conditions :

- aucune entité utile n'est exploitable
- **et** `binary_sensor.station_meteo_netatmo_*` n'est pas `on`

Lecture honnête :

> La station est silencieuse à tous les niveaux observables. Cause la plus probable : panne réseau ou perte d'alimentation de la station. Une remédiation par alimentation (reboot prise) est défendable.

> **Garde de démarrage.** Un `muet_ping_ko` observé pendant la phase d'instabilité post-redémarrage de Home Assistant est un **artefact d'initialisation** (preuves encore `unavailable`, ping pas encore remonté), non une panne réelle. Toute remédiation automatique consommant cet état — le redémarrage électrique de station — n'est donc exécutée que lorsque `input_boolean.systeme_stable` est `on`. Tant qu'il ne l'est pas, le power-cycle physique de la station est bloqué.

---

## 4. Règle centrale du contrat

> **L'absence de `sensor.temperature_jardin_*` seule n'a aucune valeur de condamnation globale de station.**

C'est la correction directe du vice du premier capteur, qui faisait implicitement `jardin → vérité station`. Le nouveau contrat fait `station → vérité station`. Ce changement est une inversion conceptuelle : on passe d'un diagnostic mono-signal fragile à un diagnostic multi-preuves robuste.

---

## 5. Définition d'une entité exploitable

Une entité est exploitable si et seulement si son état est **numériquement interprétable** — c'est-à-dire convertible en nombre sans erreur.

Tout state non convertible est considéré non exploitable, notamment : `unavailable`, `unknown`, `none`, `''`, toute string non numérique.

> **La validité d'une preuve de vie ne doit jamais être déduite de la simple présence d'un state texte.**

---

## 6. Contrainte d'implémentation — sélection positive

L'implémentation YAML DOIT reposer sur une **logique de sélection positive** des états valides.

Elle NE DOIT PAS reposer sur l'exclusion partielle d'états invalides connus (`unavailable`, `unknown`, etc.).

Pièges à ne pas reproduire :

```jinja
{# INTERDIT — liste toujours truthy #}
{% if preuves %}

{# INTERDIT — exclut seulement 'unavailable' #}
{% if 'unavailable' not in preuves %}

{# INTERDIT — reject partiel #}
{% set valides = preuves | reject('equalto', 'unavailable') | list %}
{% if valides | count > 0 %}
```

Forme correcte :

```jinja
{# CORRECT — sélection positive par numéricité #}
{% set valides = preuves
   | map('float', default=none)
   | reject('eq', none)
   | list %}
{% if valides | count > 0 %}
```

---

## 7. Contrainte sur la liste des preuves de vie

Les entités listées comme preuves de vie **DOIVENT** être des `sensor` à état numérique continu.

Sont **interdits** dans cette liste :

- tout `binary_sensor`
- tout `input_boolean`
- toute entité à état textuel discret (`on` / `off`, labels, etc.)

> Cette contrainte est vérifiable statiquement à la relecture du YAML. Elle ne génère aucune erreur à l'exécution en cas de violation — une entité non numérique serait silencieusement exclue, sans avertissement. C'est précisément pour cette raison qu'elle doit être verrouillée contractuellement.

---

## 8. Ordre logique impératif

L'évaluation DOIT suivre cet ordre strict :

```
1. Évaluer les preuves de vie (entités numériques exploitables)
2. Si au moins une → ok
3. Sinon, lire le ping
4. Si ping = on → muet_ping_ok
5. Sinon → muet_ping_ko
```

En pseudo-code :

```python
if preuves_valides:
    ok
elif ping == 'on':
    muet_ping_ok
else:
    muet_ping_ko
```

Il est **interdit** de combiner ping et preuves de vie dans une même condition (`and`). Le ping n'intervient qu'en branche `else` de l'évaluation des preuves.

---

## 9. Ce que le diagnostic autorise et interdit

### Autorisé

- Décrire factuellement l'état observable d'une station
- Servir d'entrée à une politique de remédiation **externe**, qui décidera elle-même de l'action

### Interdit

- Diagnostiquer un module individuel (jardin, chambre, etc.)
- Forcer une action lourde sur la base de l'absence d'une seule mesure
- Confondre absence locale d'une mesure et panne globale de station
- **Désigner une cause de panne dans le nom d'un état**
- **Pré-câbler une remédiation à un état observationnel sans politique explicite**

### 9.1 Politique de remédiation externe (v1.3)

> Cette politique est **externe** au diagnostic : elle est portée par des automatisations dédiées (`11_automations/meteo/reboot_station/*.yaml`) qui *consomment* l'état. Le capteur de diagnostic reste strictement observationnel (§9 « Autorisé ») et les noms d'états restent descriptifs (§10). L'existence de cette section satisfait l'exigence §9 d'une **politique explicite** : la remédiation n'est plus ni implicite ni absente.

Les deux états muets autorisent une remédiation par l'alimentation. L'action est identique — un **unique** power-cycle de la prise de la station concernée (`switch.prise_chambre_enfants` pour la station 1, `switch.prise_chambre_matthieu` pour la station 2) via `script.reboot_netatmo` — mais leur **déclenchement diffère** selon la force de la preuve :

| État | Preuve observée | Déclenchement | Fondement |
|------|-----------------|---------------|-----------|
| `muet_ping_ko` | silence total (mesures **et** ping) | **immédiat** | Cause probable : perte réseau / alimentation. Remédiation par l'alimentation défendable sans délai (§3). |
| `muet_ping_ok` | silence des mesures, ping vivant | **après persistance ≥ 20 min** | Un silence *bref* avec ping vivant peut être un trou de report transitoire. Un silence *persistant* constitue la « preuve suffisante » qui manquait en v1.1–v1.2 (cf. §11) : la leçon terrain établit qu'un power-cycle le résout. |

Invariants de la politique :

- **Ciblage par station.** Chaque station a sa prise et son diagnostic ; la remédiation n'agit que sur la prise de la station effectivement muette — jamais globalement. La détection agrégée par fraîcheur (`sensor.homekit_age_donnees`) est **inapte** au ciblage : elle suit le capteur le plus frais du groupe combiné, si bien qu'une station muette y est masquée par l'autre station saine. Le diagnostic **par station** est donc la seule autorité de déclenchement légitime.
- **Débounce sur `muet_ping_ok` uniquement.** La temporisation (`for: 00:20:00`) confirme la persistance. `muet_ping_ko` reste immédiat.
- **Tir unique, aucune boucle ni retry.** Une impulsion par épisode (`mode: single`) ; aucune escalade ni relance automatique en cas d'échec.
- **Gardes communes aux deux états.** L'action n'est exécutée que si : `input_boolean.systeme_stable = on` (garde de démarrage, §3), `binary_sensor.panne_secteur_en_cours = off` (un silence sous coupure secteur est un KO attendu, non un gel — la prise est elle-même sur secteur), `input_boolean.reboot_box_en_cours = off` et `binary_sensor.acces_externe = on` (pas de superposition à une campagne de remédiation réseau).

---

## 10. Règle de nommage des états

> Un nom d'état dans ce contrat décrit **une preuve observable**, jamais **une cause supposée**.

Cette règle est née d'une leçon terrain (cf. §11). L'état historiquement nommé `ko_homekit` désignait observationnellement « silencieux avec ping qui répond » mais suggérait causalement « HomeKit est en panne ». Cette ambiguïté a poussé vers une remédiation (reload HomeKit) qui n'était pas justifiée par les preuves.

Les noms `muet_ping_ok` et `muet_ping_ko` sont volontairement **descriptifs et symétriques**. Ils ne suggèrent aucune remédiation.

Toute évolution future de ce contrat doit respecter cette règle : si un nouvel état est introduit, son nom doit décrire l'observation, pas l'hypothèse.

---

## 11. Leçon terrain — 2026-05-06

Cas observé sur la station Matthieu :

- aucune mesure exploitable
- ping `on`
- diagnostic en `muet_ping_ok` (ex-`ko_homekit`)

Hypothèse implicite portée par l'ancien nom de l'état : « HomeKit est cassé, il faut recharger l'intégration ».

Remédiation effective : **débrancher / rebrancher physiquement la prise de la station**. Retour immédiat des mesures.

Conclusions verrouillées par ce cas :

```
1. ping IP qui répond ≠ station fonctionnelle
2. absence de mesures ≠ panne HomeKit
3. un reboot électrique de station peut résoudre un silence avec ping vivant
```

Conséquence architecturale (v1.1 → v1.2) : à ce stade, aucune remédiation automatique n'était câblée sur `muet_ping_ok`. L'état était traité comme **terminal observationnel** — Arsenal n'avait pas encore de preuve suffisante pour choisir une action, et s'abstenait légitimement. L'abstention n'était pas un trou de remédiation : c'était une décision contractuelle assumée **tant qu'une preuve terrain ne désignerait pas une remédiation efficace pour ce cas**.

**Levée de l'abstention (v1.3).** La condition posée est désormais remplie. La leçon terrain ci-dessus — confirmée par une récurrence en 2026-07 (station muette, ping vivant, intégration HomeKit en échec de configuration, résolution par power-cycle manuel de la prise) — désigne le power-cycle comme remédiation efficace du `muet_ping_ok`. L'abstention est remplacée par une **politique explicite et bornée** (§9.1) : un unique power-cycle de la prise de la station, ciblé par station, déclenché seulement après **persistance ≥ 20 min** de l'état (débounce anti-transitoire) et sous les gardes communes. Le `muet_ping_ok` cesse d'être terminal ; il reste néanmoins **strictement observationnel** (§10) — la décision d'agir vit dans une automatisation externe qui le consomme, pas dans le nom de l'état.

---

## 12. Cas de test métier

| # | Situation | État attendu |
|---|-----------|--------------|
| 1 | Station 1 — `temperature_jardin_1` absente, `temperature_sejour_1` présente | `ok` |
| 2 | Station 1 — toutes températures absentes, `co2_chambre_parents` présent | `ok` |
| 3 | Station 2 — plus aucune température ni humidité, `co2_entree` présent | `ok` |
| 4 | Station 2 — aucune donnée exploitable, `binary_sensor.station_meteo_netatmo_2` = `on` | `muet_ping_ok` |
| 5 | Station 1 — aucune donnée exploitable, `binary_sensor.station_meteo_netatmo_1` ≠ `on` | `muet_ping_ko` |

---

## 13. Historique de version

- **v1.0** — Contrat initial. États : `ok` / `ko_homekit` / `ko_reseau`.
- **v1.1** — Renommage des états vers une forme strictement observationnelle suite à une leçon terrain (§11). `ko_homekit` → `muet_ping_ok`, `ko_reseau` → `muet_ping_ko`. Ajout du §10 (règle de nommage), du §11 (leçon terrain), précision en §2.3 sur la portée réelle du ping. Aucune modification de la logique d'évaluation.
- **v1.2** — Précision de la garde de démarrage en §3 (`muet_ping_ko`) : la remédiation automatique consommant cet état (redémarrage électrique de station) est subordonnée à `input_boolean.systeme_stable = on`, afin d'éviter un power-cycle parasite déclenché par un `muet_ping_ko` artefact d'initialisation post-redémarrage de Home Assistant. Aucune modification de la logique d'évaluation.
- **v1.3** — Levée de l'abstention de remédiation sur `muet_ping_ok` (§11) au profit d'une **politique explicite et bornée** (§9.1), motivée par la leçon terrain 2026-05-06 et sa récurrence 2026-07 : un unique power-cycle de la prise de la station, **ciblé par station**, déclenché sur `muet_ping_ok` **après persistance ≥ 20 min** (débounce), `muet_ping_ko` restant immédiat. Extension explicite de la garde de démarrage `systeme_stable` à `muet_ping_ok` (§3). Gardes communes inchangées (`systeme_stable`, `panne_secteur_en_cours`, `reboot_box_en_cours`, `acces_externe`). **Aucune modification de la logique d'évaluation du diagnostic** ni des noms d'états, qui restent purement observationnels (§10).

---

*Arsenal — document contractuel · couche observation · diagnostic Netatmo · v1.3*
