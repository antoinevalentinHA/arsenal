# PATCHES ARSENAL — fork `ha_airstage`

Registre des écarts de ce fork (`antoinevalentinHA/ha_airstage`, branche
`arsenal-stable`) par rapport à l'upstream `danielkaldheim/ha_airstage`.

- **Point de fork :** upstream `1.8.1` (`ba6abcd`).
- **Portée de ce document :** documentation *propre au fork* — quels patchs, sur
  quels fichiers, et pourquoi. La démarche et la philosophie de stabilisation
  (dossier méthodologique) vivent dans Arsenal, pas ici.

---

## Patchs par fichier

| Fichier | Nature du patch |
|---------|-----------------|
| `climate.py` | Lectures défensives : `current_temperature`, `target_temperature`, `min_temp`, `max_temp`, `hvac_mode` (repli sur constantes, aucun accès non gardé). `hvac_mode` renvoie `None` plutôt qu'un faux `OFF` sur données partielles. |
| `sensor.py` | `native_value` sécurisé (`INDOOR_TEMPERATURE`, `OUTDOOR_TEMPERATURE`) : gestion `KeyError`, prévention `Decimal(None)`, retour `None` si donnée absente. |
| `switch.py` | `is_on` sécurisés (état principal, energy save, quiet, autres). Quiet off restaure la dernière vitesse manuelle au lieu de forcer `AUTO`. |
| `entity.py`, `climate.py`, `switch.py` | Décorateur `airstage_command` : les échecs de transport des commandes d'écriture (`ApiError`, `aiohttp.ClientError`, `OSError`) sont traduits en `HomeAssistantError`. Sans cela l'appel de service remonte une exception « inattendue » — trace complète au journal, et surtout hors de portée de `continue_on_error`, qui ne contient que les `HomeAssistantError` : tout script commandant l'unité était avorté en cours de séquence. Les erreurs de programmation (`KeyError`…) et `CancelledError` ne sont jamais masquées. |
| `entity.py`, `climate.py`, `switch.py` | Écriture optimiste locale au lieu de `poll-after-set` : le coordinateur est patché en cache et notifie ses listeners, supprimant le flapping de la vitesse de ventilation. |
| `__init__.py` | Setup : `ConfigEntryNotReady` sur indisponibilité transitoire au boot. Coordinateur (refresh) : `ApiError` **et** fuites non-`ApiError` (`KeyError`/`ValueError`/`TypeError`, `OSError`) → `UpdateFailed`. |
| `const.py` | `AIRSTAGE_SYNC_LOCAL_INTERVAL` 10 s → 60 s. `AIRSTAGE_LOCAL_RETRY` = 5 (identique à l'upstream net : abaissé à 3 puis restauré à 5 dans l'historique interne). |
| `manifest.json` | Pin `pyairstage>=2.4.1,<3` (voir « Décision de dépendance »). `version` 1.8.1 → 1.7.1. `use_https` et `AIRSTAGE_LOCAL_TIMEOUT_SECONDS` retirés. |

Le détail versionné et daté de ces patchs est tenu dans `CHANGELOG.arsenal.md`.

> **Sens de synchronisation.** Cette copie vendorisée est normalement *tirée* du fork.
> Le patch `airstage_command` fait exception : il est né côté Arsenal, sur incident
> runtime (voir ci-dessous). Il doit être porté sur `antoinevalentinHA/ha_airstage`
> (branche `arsenal-stable`) avant la prochaine synchronisation, sans quoi elle
> l'effacera.

---

## Incident fondateur du patch `airstage_command` (2026-08-22)

Module injoignable (`Connect call failed ('192.168.1.21', 80)`) pendant une exécution
climatisation. `pyairstage` a épuisé ses 5 tentatives et remonté `ApiError` depuis
`AirstagePowerSwitch.async_turn_on`. N'étant pas une `HomeAssistantError`, l'exception
a traversé toute la pile de scripts : `clim_exec_apply_dry` avorté, puis
`clim_execution` avorté à son tour **avant** sa qualification de post-condition — donc
sans marquage d'échec (`input_boolean.clim_execution_echec`) ni reprise différée
(`timer.clim_retry`), alors même que le contrat d'exécution les prévoit. Une
indisponibilité réseau transitoire laissait ainsi la climatisation hors de sa cible,
sans filet, jusqu'à la décision suivante.

La traduction de l'exception rend l'échec maîtrisable par l'appelant ; côté
Arsenal, les scripts d'exécution portent le `continue_on_error` correspondant (contrat
climatisation `08_execution.md` §« Échec d'émission — non-fatalité obligatoire »).
L'échec reste un échec : rien n'est silencieusement ignoré.

---

## Décision de dépendance : pin `pyairstage>=2.4.1,<3`

**Fait vérifié.** Au point de fork, l'upstream `1.8.1` pinnait
`pyairstage>=3.2.0,<4`. Ce fork l'a ramené à `>=2.4.1,<3` (résout en pratique
vers `2.4.3`). C'est un downgrade **3.x → 2.4.x**, décidé dans le commit
fondateur.

**Raison — reconstruction corroborée, non journalisée à l'époque.**
`pyairstage` `3.0.0` (déc. 2025) est un *BREAKING change* qui a **retiré les
retries internes** de la librairie (sauf déconnexions) et **élargi la surface
d'exceptions** remontées à l'intégration. Sur un module Fujitsu instable (échecs
de communication fréquents, cf. issue upstream #89), cela se traduit par
davantage d'erreurs au rafraîchissement du coordinateur. Rester sur la lignée
`2.4.x` conserve le filet de retry de la librairie ; la borne `<3` empêche HACS
de réinstaller automatiquement la `3.x`.

**Statut probatoire.** Deux reconstructions indépendantes convergent — le
changelog de `pyairstage 3.0.0` croisé au diff du `manifest.json` d'une part, une
mémoire générale du contexte d'autre part — mais **aucune trace contemporaine**
de la décision n'a été retrouvée. À traiter comme hypothèse solide, pas comme
fait journalisé. (Les numéros de version « 1.2.5 / 1.3.0 » évoqués un temps sont
erronés : ces versions de `pyairstage` n'existent pas.)

**Orthogonal aux patchs défensifs.** Le crash `int(None)` de #89 relève de la
couche intégration (lectures défensives) et était déjà corrigé côté librairie en
`pyairstage 2.4.3`. Il est indépendant du choix de version : deux sujets, deux
causes.

**Révision.** La résilience étant désormais portée par le coordinateur
(`UpdateFailed`), une migration vers la `3.x` est envisageable — ce qui
aligerait le fork sur l'upstream. À valider sur le module réel avant tout
(la `3.x` a aussi remanié le chemin local : fusion de requêtes + `asyncio.sleep`
dans `ApiLocal.get_devices`).
