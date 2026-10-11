# 🔁 ARSENAL — CHANTIER C55 · Résilience des intégrations — rechargement par `entry_id` (HA 2027.4) et défauts de résilience liés

## 📌 Statut

- **Ouvert (2026-10-11) — conception arbitrée, réserves 1 et 2 levées (§5.5, §5.6), plan validé sur le principe ; lot 1 engagé en PR distincte, aucun déploiement Home Assistant.**
- **Identifiant global** : **C55** — attribué selon la règle de gouvernance du registre (plus grand identifiant existant + 1 : `C54` → `C55`), unicité contrôlée sur le dépôt (aucune occurrence), le registre et l'historique des pull requests GitHub (aucune occurrence).
- **Domaine** : transverse — résilience des intégrations (contrat [`resilience_integrations.md`](../../../contrats/resilience_integrations.md) v3.4, registre CI [`resilience_integrations_registre.yaml`](../../../../scripts/arsenal_contracts/resilience_integrations_registre.yaml)).
- **Priorité** : **P1** — échéance externe datée (Home Assistant 2027.4) ; à cette version, l'action de **8 des 10 chaînes** de résilience cesserait de fonctionner **en silence** (§3.3).
- **Hors périmètre, explicitement** :
  - coordination entre power-cycle des stations Netatmo et rechargement HomeKit (« P3 » du diagnostic) — sujet distinct, non ouvert ;
  - dette des gardes d'inhibition sans reprise — **[C56](c56_dette_inhibition_tentative_sans_reprise.md)**, enregistrée séparément, non corrigée ici.
- **Changelog** : non créé — artefact de release produit sur déclenchement opérateur (doctrine [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1).

---

## 1. Constat d'entrée

Journal Home Assistant de l'instance (fourni par l'opérateur, 2026-10-11) :

> `homeassistant.components.homeassistant` — `components/homeassistant/__init__.py:351` — 3 occurrences (08:09:00 → 13:11:18) :
> *Reloading a config entry by target is deprecated and will stop working in Home Assistant 2027.4, please specify the config entry to reload in the 'entry_id' parameter instead.*

### 1.1 Origine — faits vérifiés dans le dépôt

- **Un seul appel par cible dans tout Arsenal** : [`10_scripts/system/resilience_integration_recover.yaml`](../../../../10_scripts/system/resilience_integration_recover.yaml), branche `reload_target` (`homeassistant.reload_config_entry` + `target.entity_id`).
- Ce ciblage **n'est pas un écart** : il est **prescrit** par le contrat (§12.5, R-ANCRAGE-5 et R-ANCRAGE-8) et vérifié par la règle CI **R18**.
- Aucun autre appel au service (automatisations, blueprints, cartes, composants personnalisés — ces derniers appellent `async_reload` en Python, hors service).

### 1.2 Chaînes concernées

| Chaîne | Automatisation | Périmètre / désignation | Concernée en 2027.4 |
|---|---|---|---|
| Netatmo | `10120000000008` | `group.netatmo_capteurs` (cible) | oui |
| Airstage | `10120000000013` | `group.fujitsu_capteurs` (cible) | oui |
| HomeKit Station Enfants | `10120000000019` | `group.homekit_station_enfants` (cible) | oui |
| HomeKit Station Salle de Jeux | `10120000000031` | `group.homekit_station_salle_de_jeux` (cible) | oui |
| Overkiz | `10120000000012` | `group.petite_maison_cumulus` (cible) | oui |
| SwitchBot BLE | `10120000000011` | `group.switchbot_ble_capteurs` (cible, 5 entrées) | oui |
| SwitchBot Cloud | `10120000000032` | `group.switchbot_cloud_capteurs` (cible) | oui |
| Synology | `10120000000021` | `group.synology_capteurs` (cible) | oui |
| HomeKit Prise Control | `10120000000029` | `entry_id` (secret) | non |
| Zigbee2MQTT | `10120000000010` | `hassio.addon_restart` | non |

### 1.3 Corrélation des 3 occurrences

**Non établie** : journaux, traces et historique de l'instance hors dépôt. Fait établi par le code HA : l'avertissement est émis **une fois par appel** porteur d'une cible, quel que soit le nombre d'entrées — 3 occurrences = 3 tentatives (`op: attempt`) sur les chaînes ciblées. Éléments nécessaires pour attribuer : traces des 8 automatisations, historique des compteurs `input_number.*_reload_tentatives`, notifications vers 08:09 et 13:11.

---

## 2. Comportement de Home Assistant — faits établis sur le code source

Source : `home-assistant/core`, étiquette **2026.10.1** (la ligne 351 de `components/homeassistant/__init__.py` y est l'appel `_LOGGER.warning` de cet avertissement — l'instance est très probablement en 2026.10.x). Lecture hors dépôt, aucune copie versionnée.

| # | Fait | Conséquence pour Arsenal |
|---|---|---|
| H1 | Schéma du service : `entry_id` est une **chaîne unique** (pas de liste) | un rechargement multi-entrées impose une boucle |
| H2 | Résolution d'une cible : liste des membres lue dans l'attribut d'état `entity_id` du groupe (tous les membres **configurés**, existants ou non, développés récursivement), puis `config_entry_id` lu au **registre des entités** | reproductible exactement par `state_attr(groupe, 'entity_id') \| map('config_entry_id')` sur un groupe plat |
| H3 | Rechargement par `asyncio.gather` sans `return_exceptions` ; booléen de résultat de `async_reload` **ignoré** | un échec de chargement n'est jamais une erreur de service ; une exception interrompt l'appel pendant que les autres rechargements continuent |
| H4 | Exceptions possibles : `UnknownEntry` (entrée disparue), `OperationNotAllowed` (état non récupérable : `migration_error`, `failed_unload`, `setup_in_progress`, `unload_in_progress`) — toutes deux `HomeAssistantError` | capturables par `continue_on_error` ; le `ValueError` du service sur ensemble vide ne l'est pas |
| H5 | Une entité enregistrée non désactivée **garde toujours un état** (`unavailable` + `restored`) après déchargement de son entrée | une entité indisponible reste résolue, y compris aux tentatives n° 2 et suivantes |
| H6 | `expand()` (template) **ignore** les membres sans état (entités désactivées) | ne reproduit pas exactement H2 ; reste l'outil du contrôle d'ancrage |
| H7 | Script en `mode: single` déjà en cours : nouvel appel **refusé** (« Already running », niveau warning) | voir D1, D2 |
| H8 | Appel `script.<nom>` depuis une automatisation : **bloquant** ; annulation de l'automatisation ⇒ arrêt **attendu** de l'exécution du script | exclusivité par chaîne (§5.6) |
| H9 | Exécution d'automatisation : contexte neuf, écrit dans l'état de l'automatisation à son démarrage ; appel manuel ou externe : contexte distinct | garde d'appelant authentifié (§5.6) |
| H10 | Timer restauré expiré pendant l'arrêt : `timer.finished` émis **pendant la mise en place**, avant l'armement des déclencheurs d'automatisation (armés juste avant la fin du démarrage) | événement **perdu** (T1) |
| H11 | Sauvegarde de l'état restauré : toutes les **15 min** et à l'arrêt propre | après arrêt brutal, timers et compteurs restaurés à une valeur vieille de 15 min au plus (T3) |
| H12 | SwitchBot : à l'installation d'une entrée, attente de la première annonce BLE, **30 s maximum** | borne du rechargement séquentiel (§5.2) |
| H13 | Recorder : un événement portant un `entity_id` hors liste blanche (`recorder.yaml`, `include`) **n'est pas enregistré** ; sans `entity_id`, il l'est | conditionne la valeur probatoire de `logbook.log` (§5.8) |
| H14 | `continue_on_error` : l'exception reste **journalisée** (`home-assistant.log`) et inscrite dans la trace, mais n'est **pas exposée** aux variables du script | le résultat technique par entrée n'est pas lisible en YAML (§5.4) |

---

## 3. Défauts constatés

### 3.1 Migration (cause du chantier)

- **M1** — l'action ciblée cessera de fonctionner en 2027.4.

### 3.2 Défauts de résilience liés (lecture du code — non observés en conditions réelles)

| # | Défaut | Conséquence |
|---|---|---|
| D1 | Au plafond, le script s'appelle lui-même (`op: block`) alors qu'il est en `mode: single` (H7) | l'appel est refusé : **la notification « ⛔ blocage sécurité » n'est jamais émise** — invariant 9 non tenu |
| D2 | Script unique en `mode: single` pour **toutes** les chaînes (H7) | une tentative d'une chaîne pendant l'exécution d'une autre est refusée ; compteur et timer inchangés, gel toujours `on` : **épisode figé** jusqu'au retour OK |
| D3 | Timer de backoff annulé avant l'action, relancé seulement après l'attente | erreur d'appel, redémarrage ou rechargement entre les deux : compteur incrémenté **sans relance programmée** |
| D4 | Ensemble d'entrées vide : `ValueError` non capturable | même chemin que D3 |
| T1 | Timer expiré pendant l'arrêt de HA (H10) | expiration perdue |
| T2 | Timer expirant dans les 45 s de stabilisation | expiration rejetée par la garde `systeme_stable` |
| T3 | Arrêt brutal (H11) | compteur ou timer restaurés en retard d'au plus 15 min |
| T4 | `retour_ok` passant `on` pendant le démarrage | transition perdue, épisode non refermé |

**Vérifications opérateur proposées (non bloquantes)** : présence de « Système - Résilience intégration: Already running » dans les journaux (confirmerait D1/D2 en conditions réelles) ; réception passée d'une notification « ⛔ … blocage sécurité ».

### 3.3 Conséquence prévisible en 2027.4 (hypothèse sur le comportement futur de HA)

Si HA refuse l'appel ciblé : le script s'arrête en erreur après incrément du compteur et annulation du timer, avant tout réarmement et toute notification (D3). Les 8 chaînes ciblées deviennent **inopérantes en silence**.

---

## 4. Arbitrages rendus

| Réf. | Décision (opérateur, 2026-10-11) |
|---|---|
| P1 | Conserver le périmètre contractuel `reload_target` ; résoudre les `entry_id` à l'exécution ; supprimer le ciblage déprécié |
| P1 bis, P2 | Traités dans ce chantier (robustesse aux erreurs, contrôle CI) |
| A1 | Résolveur sur la liste **déclarée** du groupe (`state_attr`), équivalence exacte avec H2 ; détection de divergence dans le contrôle d'ancrage |
| A2 | Rechargement **séquentiel** (`repeat` / `for_each`), borne documentée |
| A3 | Ensemble à recharger vide = **tentative en échec** comptée |
| A4 | Garde de domaine côté action par un champ `domaine_attendu`, recoupé en CI avec le registre |
| A4b | Entrée hors domaine ⇒ **refus explicite de l'action entière** — une incohérence contractuelle n'est pas masquée par une exécution partielle |
| A5 | Correction de D1 et D2 dans ce chantier |
| A6 | Observabilité par `logbook.log` ; aucune nouvelle entité |
| A7 | Contrat porté en **v3.5** |
| R-1 | Script canon en `mode: parallel`, `max` contrôlé en CI ; l'interdiction contractuelle de l'exécution manuelle **ne suffit pas** : garde-fou technique exigé (§5.6, réserve 1) |
| R-2 | Blocage **dès le 5ᵉ échec** |
| R-3 | Anomalie de domaine ⇒ **blocage immédiat**, **distingué** du blocage par épuisement dans les notifications et les preuves (§5.5) |
| R-4 | Reprise après stabilisation ajoutée aux automatisations des chaînes |
| R-5 | Critère de preuve `logbook.log` : constat d'une ligne en base après déploiement, sans niveau présumé (§5.8) |
| R-6 | Dette des gardes d'inhibition enregistrée séparément ([C56](c56_dette_inhibition_tentative_sans_reprise.md)) |
| Réserve 1 (2026-10-11) | La garde `context.user_id` n'est pas une preuve d'exclusivité ⇒ remplacée par la **garde d'appelant authentifié par contexte**, démontrée au §5.6 |
| Réserve 2 (2026-10-11) | Le blocage pour anomalie de domaine ne détourne pas le compteur ⇒ **prédicat recalculé** sur la configuration, compteur inchangé, timer arrêté, relance humaine après correction (§5.5) |
| Lot 1 | Autorisé par l'opérateur sous condition de levée démontrable des deux réserves ; PR distincte de la PR documentaire ; **aucun déploiement Home Assistant sans validation explicite** |

---

## 5. Architecture cible

### 5.1 Résolution des entrées (A1)

```jinja
{{ (state_attr(reload_target, 'entity_id') or []) | map('config_entry_id')
   | reject('none') | unique | sort | list }}
```

- **Équivalence avec le mécanisme actuel (H2)** : même source de membres (attribut `entity_id` du groupe), même lecture du registre ; membres indisponibles conservés (H5), membres désactivés conservés, membres inconnus ou sans entrée écartés.
- **Seule différence** : pas de développement récursif. Les 9 groupes de périmètre sont plats (vérifié le 2026-10-11) ; la CI les maintient plats (§7, contrôle d).
- La branche `entry_id` (HomeKit Prise Control) passe par le **même** chemin, avec une liste d'un élément.

### 5.2 Rechargement multi-entrées (A2)

- Boucle `repeat` / `for_each`, un `homeassistant.reload_config_entry` par entrée, `continue_on_error: true`.
- **Préservé** : toutes les entrées sont tentées ; le script attend la fin de toutes avant d'observer les axes.
- **Amélioré** : une exception n'interrompt plus les rechargements suivants (H3/H4).
- **Changé** : séquentiel au lieu de concurrent. Pire cas SwitchBot BLE ≈ 5 × 30 s (H12) ≈ 2 min 30, contre ≈ 30 s ; cas nominal inchangé (annonces toutes les quelques secondes). Le délai d'attente des axes démarre après la boucle.

### 5.3 Séquence d'une tentative

1. **Garde d'appelant** (§5.6) — refus de tout appel qui n'émane pas de l'exécution en cours de l'automatisation de la chaîne.
2. Gardes existantes (panne secteur, WAN, paramètres, cohérence des axes).
3. Plafond atteint ⇒ rien (bloqué par épuisement, déjà notifié — §5.5).
4. `op: reprise` et timer actif ⇒ rien (§5.7).
5. Incident non confirmé ⇒ arrêt (inchangé).
6. **Couche A — plan** (§5.4), calcul pur sans effet. Anomalie de domaine ⇒ **refus** (§5.5) : rien d'autre n'est écrit.
7. **Bail** : timer de backoff armé pour la durée calculée.
8. Incrément du compteur (`tentative + 1`).
9. Plan vide (A3) ⇒ échec compté (§5.5), sans appel ni attente.
10. **Couche B — appels**.
11. **Couche C — observation**.
12. **Couche D — décision** : attente sur les axes, puis succès (arrêt du timer, compteur à 0, notification) ou échec (timer relancé pour une durée pleine, notification ; **5ᵉ échec ⇒ blocage par épuisement**).
13. `logbook.log` (§5.8) à chaque issue : refus, échec, succès, blocage.

**Invariant du bail** : durée minimale du bail (10 min) > durée maximale de la boucle + délai d'attente (≈ 5 min 30 au pire). Toute interruption après l'étape 7 laisse un timer restauré qui provoquera une nouvelle tentative.

### 5.4 Séparation résultat technique / observation / décision

| Couche | Contenu | Effet sur la suite |
|---|---|---|
| **A. Plan** | entrées résolues ; entrées écartées avec motif (`inconnue`, `desactivee`, `etat_non_recuperable:<état>`) ; **refus** si une entrée est hors `domaine_attendu` (A4b) ou si l'ensemble à recharger est vide (A3) | décide seulement s'il y a des appels |
| **B. Résultat technique** | liste des appels **émis** | aucun |
| **C. Observation** | état de chaque entrée relevé une fois après la boucle (`config_entry_attr(e, 'state')`) | aucun — information seulement (`setup_retry` est normal juste après un rechargement BLE) |
| **D. Décision contractuelle** | les axes de détection uniquement (`wait_template` et condition de succès, **inchangés**) | seule source du verdict |

- **Limite assumée (H14)** : le YAML ne capture pas l'exception d'un appel. La couche B affirme « appel émis », **jamais** « rechargement réussi ». Les erreurs restent dans la trace et dans `home-assistant.log`.
- **Vérifiable en CI** : les conditions de la couche D ne référencent aucune variable des couches A, B ou C.
- **Notifications** : le titre ne dépend que de la couche D (ou du blocage, §5.5). Le corps reste à la maille opérateur (contrat [`notifications.md`](../../../contrats/notifications.md), § Frontière opérateur / mécanique interne) : **aucun `entry_id`, aucune mention de couche**. Le détail A/B/C va au journal (§5.8), pas au message.

### 5.5 Deux blocages distincts (R-2, R-3) — représentation et reprise

**Réserve opérateur du 2026-10-11** : le blocage pour anomalie de domaine doit garder une sémantique déterministe après redémarrage, **sans détourner le compteur de tentatives**. La proposition antérieure (compteur porté au plafond sans tentative) est **retirée**.

#### Représentation

| | Blocage par **épuisement** | Blocage pour **anomalie de domaine** |
|---|---|---|
| Nature | état **mémorisé** de l'épisode | prédicat **recalculé** sur la configuration |
| Représentation | compteur ≥ plafond (5 tentatives **réellement** faites), timer arrêté | `P(chaîne)` : une entrée résolue depuis la liste déclarée du groupe a un domaine ≠ `domaine_attendu` |
| Entrées de la représentation | `input_number` et `timer`, restaurés par HA | groupe déclaré, registre des entités, `domaine_attendu` — **configuration persistante**, indépendante de toute restauration d'état |
| Compteur | réel | **inchangé** par le refus (aucune tentative n'a lieu) |
| Timer | arrêté | arrêté par le refus (relancer est vain tant que la configuration est fausse) |
| Notification | `⛔ <Chaîne> — blocage sécurité` · « 5 tentatives consécutives échouées. Relances automatiques arrêtées. » | `⛔ <Chaîne> — relance refusée` · « Le groupe surveillé contient des éléments d'une autre intégration (<domaines>). Aucune relance automatique tant que le groupe n'est pas corrigé. » |
| Journal | `issue=blocage_epuisement` | `issue=refus_anomalie_domaine`, domaines trouvés et attendu |
| Indicateur persistant | `binary_sensor.recovery_en_cours_<chaîne>` (compteur > 0) | `binary_sensor.ancrage_chaines_resilience_non_conforme`, attribut `detail` (domaine attendu, §6) — recalculé au démarrage |
| Levée | retour constaté (R-RECOV-2) | correction du groupe : la tentative suivante ne refuse plus |

**Pourquoi aucun état mémorisé pour l'anomalie** : elle n'est pas un fait de l'épisode, c'est une propriété de la configuration. La mémoriser créerait une deuxième vérité qui pourrait diverger de la configuration réelle (groupe corrigé, état encore « bloqué », ou l'inverse). Recalculée, elle ne peut pas être périmée.

#### Distinction avec les autres états, à tout instant

| Compteur `n` | Timer | `P` | Incident | État |
|---|---|---|---|---|
| 0 | arrêté | — | non | nominal |
| ≥ 1 | **actif** | — | — | **attente normale** (backoff) |
| ≥ 5 | arrêté | — | — | bloqué par épuisement |
| < 5 | arrêté | **vrai** | oui | **bloqué pour anomalie** (refus à chaque évaluation) |
| 1 à 4 | arrêté | faux | oui | épisode à relancer (expiration perdue — T1/T2) |
| ≥ 1 | arrêté | faux | non | épisode en attente de `retour_ok` |

Les lignes sont exclusives : l'attente normale est la **seule** à timer actif ; l'anomalie est la **seule** où `P` est vrai sous le plafond ; l'épuisement est le **seul** au plafond.

#### Après redémarrage

- **Épuisement** : compteur et timer restaurés ; la reprise voit `n ≥ 5` ⇒ rien. **Maintenu.**
- **Anomalie** : rien à restaurer. À la reprise (§5.7), si l'incident est confirmé, le plan recalcule `P` :
  - `P` vrai ⇒ nouveau refus notifié — **maintenu**, une notification par stabilisation ;
  - `P` faux (groupe corrigé entre-temps) ⇒ tentative normale — **repris**.
- **Correction sans redémarrage** (rechargement des groupes) : aucune transition d'axe n'a lieu. La relance est **délibérément humaine** : déclencher manuellement l'automatisation de la chaîne (`automation.trigger`), qui passe la garde d'appelant (§5.6). Un blocage pour incohérence de configuration se lève par l'opérateur qui corrige ; il ne se lève pas tout seul. Faire réagir la chaîne au capteur d'ancrage aurait fait déclencher une action par la couche observation, ce que R-AXE3-5 et l'en-tête de `ancrage.yaml` interdisent.
- Fréquence des refus notifiés : au plus un par transition d'axe (gel, indisponibilité, échec de configuration, tous débouncés) et un par stabilisation après démarrage.

#### Interactions

- Refus avec `n ≥ 1` (anomalie apparue en cours d'épisode) : l'épisode reste ouvert (`recovery_en_cours` = on), `retour_ok` peut le refermer et la fermeture est notifiée (R-RECOV-3).
- Refus avec `n = 0` : aucun épisode n'est ouvert ; la notification de refus est la seule trace opérateur. Aucune fermeture n'est notifiée si l'intégration revient seule : le refus porte sur la configuration, pas sur l'épisode.

### 5.6 Exclusivité par chaîne — démonstration (R-1)

**Réserve opérateur du 2026-10-11** : la garde `context.user_id` n'est qu'un complément ; l'exclusivité doit être **démontrée** pour un appel concurrent en contexte système. Elle est **remplacée** par une garde d'appelant authentifié par contexte.

#### Ce qu'un appel concurrent corromprait sans garde

Deux exécutions de la même chaîne lisent `tentative` au démarrage puis écrivent `tentative + 1` : **mise à jour perdue**. L'une peut remettre le compteur à 0 et arrêter le timer pendant que l'autre relance le timer ou bloque : **couple compteur/timer incohérent**, notifications contradictoires. La garde doit donc rendre ce chevauchement impossible, pas seulement improbable.

#### Garde d'appelant authentifié

Chaque appel des automatisations transmet `appelant: "{{ this.entity_id }}"`. Première étape du script, pour **toutes** les opérations :

```yaml
- if:
    - condition: template
      value_template: >
        {{ appelant_safe | length == 0
           or states[appelant_safe] is none
           or states[appelant_safe].context.id != context.id }}
  then:
    - stop: "Appel refusé : pas l'exécution en cours de l'automatisation de la chaîne"
```

#### Faits HA mobilisés (code 2026.10.1)

| # | Fait |
|---|---|
| E1 | Chaque exécution d'automatisation crée un **contexte neuf** (`Context(parent_id=…)`, identifiant aléatoire) |
| E2 | Avant de lancer ses actions, l'automatisation écrit son état (`last_triggered`, `current`) **avec ce contexte** (`async_set_context` puis écriture au démarrage de l'exécution) |
| E3 | Un déclenchement refusé par `mode: single` n'écrit pas d'état (refus avant le démarrage) |
| E4 | L'appel `script.<nom>` est bloquant et propage le contexte de l'exécution ; le script le reçoit dans la variable `context` |
| E5 | Annuler l'exécution de l'automatisation arrête et attend l'exécution du script (H8) |
| E6 | Toute automatisation déclenchée par un événement porteur de ce contexte crée **son propre** contexte (E1) |

#### Démonstration

Soit une exécution S du script qui passe la garde avec `appelant = A`. Alors `context.id(S) = états[A].context.id = c`.

1. Par E2 et E3, `c` est le contexte de l'exécution `k` de A dont le démarrage a écrit l'état ; par E1 il n'a été créé que pour elle.
2. Seul du code qui détient l'objet contexte `c` peut appeler un service avec ce contexte. Le détiennent : l'exécution `k` de A et les services qu'elle appelle (E4). Une autre automatisation porte un autre contexte (E6). Un appel humain ou système porte le sien. Le script canon ne s'appelle pas lui-même (CI).
3. L'exécution `k` de A appelle le script **une seule fois** (structure vérifiée en CI : un appel par branche exclusive).
4. Donc au plus **une** exécution du script par exécution de A. Les exécutions de A sont séquentielles (`mode: single`, R11) et une exécution du script ne survit pas à la sienne (E5).
5. Chaque automatisation passe **son** compteur et **son** timer, propres à la chaîne (CI R16 et R20-f).

**Conclusion** : deux exécutions du script ne peuvent jamais manipuler simultanément le même compteur ou le même timer. Les écritures d'une chaîne sont totalement ordonnées ; aucune mise à jour perdue ni couple incohérent n'est possible.

#### Hypothèse et limite

- **Hypothèse unique** : aucun code ne **fabrique** un objet contexte portant l'identifiant de celui d'une exécution d'automatisation. Cela suppose un code Python exécuté dans HA avec accès à ses objets internes — hors du modèle de menace de la configuration YAML, et invisible à la CI.
- La garde subsume l'ancienne `context.user_id` : un appel humain porte un contexte neuf, donc refusé.
- Déclencher **l'automatisation** à la main (`automation.trigger`) reste possible et sûr : c'est une exécution de A au sens de la démonstration.
- **Écrivains hors script** : aucun fichier du dépôt n'écrit les compteurs ni les timers de backoff en dehors du script canon (vérifié le 2026-10-11 ; seul `etat.yaml` les lit). Une écriture manuelle depuis l'interface reste possible ; elle n'est pas concurrente d'une mise à jour perdue (pas de lecture-écriture), et la reprise ramène la chaîne dans un état du tableau §5.5.
- **Réserve indépendante (déjà présente)** : un rechargement qui ne se termine jamais immobilise la chaîne ; HA ne borne pas la durée d'un appel de service dans un script. Non corrigeable en YAML ; documenté.

### 5.7 Reprise après redémarrage (R-4)

**Pourquoi elle est nécessaire (fait HA 2026.10.1)** : les binaires de gel, d'indisponibilité et de retour OK sont des capteurs template à `delay_on` qui **restaurent** leur dernier état au démarrage. Un incident en cours au moment de l'arrêt revient donc à `on` **sans transition** : aucun déclencheur ne se réarme. Combinée à T1/T2, cette restauration laisse un épisode sans relance.

- Nouveau déclencheur dans chaque automatisation de chaîne : `input_boolean.systeme_stable` passe à `on` (id `reprise`).
- Décision dans l'automatisation : `retour_ok` à `on` ⇒ `op: reset` ; sinon ⇒ `op: reprise`.
- `op: reprise` dans le script — mêmes gardes et même procédure qu'une tentative, avec une seule différence : un timer actif n'est **pas** préempté.

| État restauré | Action |
|---|---|
| compteur ≥ plafond | rien (bloqué par épuisement, déjà notifié) |
| timer actif | rien (il expirera après la stabilisation) |
| incident non confirmé | rien ; `retour_ok` refermera un épisode ouvert |
| incident confirmé, `P` vrai | refus notifié (§5.5) |
| incident confirmé, `P` faux | **tentative** complète (bail, plan, appels, décision) |

- Le cas « compteur = 0, incident confirmé » est inclus : il couvre une transition d'axe perdue pendant le démarrage.
- **Invariant** : une fois le système stabilisé, toute chaîne en incident a un timer actif, ou est bloquée et notifiée, ou est relancée.
- T3 accepté : au pire une tentative non comptée ou un retour OK différé ; la reprise ramène toujours la chaîne à un état du tableau §5.5.

### 5.8 Journal `logbook.log` — conservation et valeur probatoire (A6, R-5)

- **Forme** : un `logbook.log` par tentative ou blocage, **sans `entity_id`** (H13), message structuré `clé=valeur` (chaîne, opération, tentative, plan, appels, observation, verdict, blocage).
- **Conservation** : `purge_keep_days: 30` ; `commit_interval: 60` (jusqu'à 60 s perdues en cas d'arrêt brutal).
- **Valeur probatoire — non présumée** :
  - enregistrable en base (L2 **conditionnel**), disponible 30 jours (L3), puis seulement en sauvegarde (L4) — **à démontrer** par constat d'une ligne `logbook_entry` en base après déploiement ;
  - c'est une **déclaration du script** : elle ne prouve ni que HA a rechargé, ni que l'intégration a récupéré. Le constat de récupération reste porté par les axes ; l'état des entrées n'est historisé nulle part ;
  - affichage dans l'interface Journal avec le filtre `logbook.yaml` (`include`) : **hypothèse non vérifiée**, sans effet sur la preuve en base.
- **Publication** : toute preuve versionnée cite le domaine et le nombre d'entrées, **jamais un `entry_id`**.

---

## 6. Contrôle d'ancrage — indépendance vis-à-vis de l'action

| Vérification | Source | Indépendante du résolveur de l'action |
|---|---|---|
| Action | liste déclarée (`state_attr`) | — |
| Ancrage existant | liste vue dans l'état (`expand`) | oui |
| **Ancrage étendu** : liste déclarée − liste vue ≠ ∅ | compare les deux chemins | oui — détecte membres désactivés ou supprimés |
| **Ancrage étendu** : domaine résolu ≠ domaine attendu du groupe | déclaration écrite en clair, recoupée en CI avec le registre | oui |
| Fermeture de domaine, mono-entrée | `config_entry_attr(domain)`, familles `mono`/`cibles` | oui |
| Rétrécissement d'un périmètre | [`couverture.yaml`](../../../../12_template_sensors/system/integrations/couverture.yaml) par `integration_entities()` | oui |
| R15, R18 | dépôt (statique) | oui |

- Élément partagé : `config_entry_id()` — lecture du registre des entités, **identique à celle de HA pour une cible**, c'est-à-dire la donnée de référence, pas une interprétation d'Arsenal.
- **Angle mort résiduel, inchangé** : une entrée sans aucune entité (limite 1 de `couverture.yaml`).

---

## 7. Contrôles CI prévus

Nouvelle règle **R20** du checker `check_resilience_integrations_contracts.py` (numérotation : plus grand numéro de règle existant + 1).

| # | Contrôle |
|---|---|
| a | Aucun `homeassistant.reload_config_entry` avec clé de cible (`target`, `entity_id`, `device_id`, `area_id`, `floor_id`, `label_id`) dans `10_scripts/` et `11_automations/` ; `entry_id` obligatoire |
| b | Dans le script canon, rechargement uniquement dans `repeat.for_each`, avec `continue_on_error: true` |
| c | Script canon : pas de `mode: single`, aucun appel à lui-même ; `max` ≥ nombre de chaînes du registre appelant le script |
| d | Groupes de périmètre des chaînes ciblées : aucun membre `group.` |
| e | `domaine_attendu` transmis par chaque automatisation = `domaine_integration` du registre ; même valeur dans la déclaration du contrôle d'ancrage |
| f | Chaque compteur et chaque timer de backoff référencés par une seule automatisation ; script canon appelé uniquement par les automatisations du registre, jamais via `script.turn_on` |
| g | Conditions de décision (attente, succès) sans référence aux variables des couches A, B, C |
| h | `logbook.log` du script canon sans `entity_id` |
| i | Garde d'appelant authentifié (`states[appelant].context.id == context.id`) en première étape du script canon ; chaque appel des automatisations transmet `appelant: "{{ this.entity_id }}"` |
| j | Opération `reprise` présente ; déclencheur `reprise` sur `input_boolean.systeme_stable` dans chaque automatisation de chaîne ; appel `op: reprise` identique à l'appel `op: attempt` hors `op` |

**Preuve de mutation exigée** : chaque contrôle doit échouer sur le code actuel (ou sur une mutation ciblée) avant d'être déclaré efficace. Les commentaires de **R18** sont mis à jour (le ciblage devient une résolution).

---

## 8. Projet d'amendement du contrat — v3.4 → v3.5

Texte **proposé**, appliqué au contrat dans le **même lot** que le runtime et la CI (§9, lot 1) : appliqué seul, le contrat décrirait un comportement que le runtime n'a pas.

1. **§4 Anatomie, ligne « Action »** — remplacer « `entry_id` désignant l'entrée effectivement observée » par : « entrées **résolues à l'exécution** depuis le périmètre observé (§12.5), rechargées une à une par `entry_id` ».
2. **§4.1** — ajouter :
   - **R-RECOV-4** — *Bail* : le timer de backoff est armé avant toute action ; tout chemin terminal d'une tentative laisse un timer actif, un compteur à zéro, un blocage notifié ou un refus notifié.
   - **R-RECOV-5** — *Reprise* : à la stabilisation après démarrage, toute chaîne en incident confirmé, sans timer actif et sous plafond, est réévaluée comme une tentative ; un `retour_ok` présent referme l'épisode.
   - **R-RECOV-6** — *Deux blocages* : le blocage par épuisement est un état mémorisé de l'épisode (compteur au plafond après 5 tentatives réelles) ; le blocage pour anomalie de domaine est un prédicat recalculé sur la configuration, qui ne modifie jamais le compteur. Ils sont distincts dans les notifications et le journal.
   - **R-RECOV-7** — *Exclusivité* : le script canon refuse tout appel qui n'émane pas de l'exécution en cours de l'automatisation de la chaîne (contexte d'appel égal au contexte d'état de l'automatisation appelante).
3. **§5 Invariants** — invariant 7 : « au 5ᵉ échec, blocage immédiat » ; invariant 9 : notification de blocage **effectivement émise** (correction D1) ; nouvel invariant 16 : **exclusivité par chaîne** (C1–C5) ; nouvel invariant 17 : **séparation plan / résultat technique / observation / décision** (§5.4).
4. **§6 Interdictions** — ajouter : appel `reload_config_entry` par cible ; appel du script canon par autre chose que l'exécution en cours de l'automatisation de la chaîne ; appel du script canon par `script.turn_on` ; condition de décision lisant le plan, le résultat technique ou l'observation.
5. **§12.5** — R-ANCRAGE-5 : distinguer le **principe** (l'action dérive du périmètre) du **moyen** (résolution à l'exécution, §12.5.3). Requalifier la note « comportement vérifié le 2026-08-24 » comme preuve **historique** de l'ancien moyen.
6. **Nouveau §12.5.3 « Résolution à l'exécution — Home Assistant 2027.4 »** :
   - **R-ANCRAGE-10** — *Équivalence* : la résolution lit la liste déclarée du groupe et le registre des entités ; les groupes de périmètre sont plats.
   - **R-ANCRAGE-11** — *Refus* : une entrée hors du domaine attendu fait refuser l'action entière (blocage pour anomalie de domaine) ; jamais d'exécution partielle.
   - **R-ANCRAGE-12** — *Indépendance du contrôle* : le contrôle d'ancrage compare la liste déclarée et la liste vue dans l'état, et le domaine attendu.
   - Exclusions du plan (entrée inconnue, désactivée, état non récupérable) : techniques, non contractuelles, journalisées.
   - Rechargement séquentiel ; borne du bail.
7. **§9 Séparation des couches** — préciser les couches A à D à l'intérieur de la couche Action, et la place du journal.
8. **§10** — mentionner **R20**.
9. **§13.3** — qualification probatoire de `logbook.log` (§5.8 du présent document).
10. **§16 Historique** — entrée v3.5.

---

## 9. Plan d'exécution

### Lot 0 — ouverture (le présent commit)

Document de chantier, ligne C55 au registre, dette [C56](c56_dette_inhibition_tentative_sans_reprise.md), règle d'attribution des identifiants au registre, entrées d'index. **Aucun runtime.**

### Lot 1 — contrat, CI et runtime (une pull request, commits ordonnés) — *soumis à validation du présent plan*

| Ordre | Contenu |
|---|---|
| 1a | Contrat v3.5 (§8) |
| 1b | Checker : R20 (a à j), commentaires R18 ; **preuve de mutation** sur le code actuel |
| 1c | Script canon : garde d'appelant authentifié, `mode: parallel` / `max`, blocage intégré, bail, `reprise`, résolution, couches A–D, `logbook.log`, champ `domaine_attendu`, notifications distinctes |
| 1d | 9 automatisations de chaîne : `domaine_attendu`, déclencheur `reprise` (aucun renommage, aucun nouvel identifiant) |
| 1e | `ancrage.yaml` : liste déclarée vs vue, domaine attendu par groupe |
| 1f | Registre C55 mis à jour (co-commit) |

**Contrôles avant fusion** : `check_resilience_integrations_contracts.py`, `check_notifications_contracts.py`, `check_registre_chantiers.py`, `check_configuration_includes.py`, gates `docs_lint` (`docs_lint`, `docs_ci_orphan_report`, `docs_ci_contract_counts`, `docs_ci_naming`, `docs_ci_navigation_leaf_pages`, `docs_ci_changelog_index`), ensemble `contracts_all`. Relecture adversariale du diff.

**Limite** : aucune CI ne valide le chargement par Home Assistant. Ce point relève du lot 2.

### Lot 2 — déploiement opérateur (après fusion, sur autorisation)

1. « Vérifier la configuration » dans HA, puis recharger scripts, automatisations et modèles.
2. **L1 — immédiat** :
   - outils de développement, rendu du résolveur pour les 9 périmètres : comparaison avec le contrôle d'ancrage (aucun écart attendu) ;
   - `binary_sensor.ancrage_chaines_resilience_non_conforme` à `off` ;
   - exécution manuelle du script : **refusée** par la garde d'appelant (trace) ;
   - aucune nouvelle occurrence de l'avertissement de dépréciation, aucune « Already running ».
3. **Opportuniste (réserve non bloquante)** : première tentative réelle :
   - ligne `logbook_entry` constatée en base (critère R-5) ;
   - trace de la boucle `entry_id` ;
   - verdict des axes.
4. **Opportuniste** : premier redémarrage avec un épisode ouvert — comportement de reprise.

### Lot 3 — clôture

Critères : §10.

---

## 10. Critères de clôture

1. Aucun appel par cible dans le dépôt (R20 a) et aucune occurrence de l'avertissement dans les journaux après déploiement.
2. Contrat v3.5 en vigueur ; R20 vert avec preuve de mutation.
3. Résolveur rendu égal au contrôle d'ancrage sur les 9 périmètres (L1).
4. Garde d'appelant constatée (L1).
5. Au moins une tentative réelle observée avec ligne de journal en base, **ou** réserve opportuniste explicitement qualifiée non bloquante (doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)).

---

## 11. Réserves ouvertes

| Réf. | Réserve | Qualification |
|---|---|---|
| RS-1 | Fabrication d'un objet contexte par du code Python interne à HA (§5.6) | hors modèle de menace YAML, documentée |
| RS-2 | Rechargement sans fin (§5.6) | résiduelle, non corrigeable en YAML |
| RS-3 | Arrêt brutal : écart de restauration de 15 min au plus (T3) | acceptée, bornée |
| RS-4 | Affichage UI des entrées `logbook.log` sans `entity_id` | hypothèse, sans effet probatoire |
| RS-5 | Axe indisponibilité franche aveugle à l'échec d'une entrée sur N (SwitchBot BLE) | antérieure, hors périmètre ; inchangée par la migration |
| RS-6 | Attribution des 3 occurrences du 2026-10-11 | non établie (§1.3) |
