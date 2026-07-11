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
| `entity.py`, `climate.py`, `switch.py` | Écriture optimiste locale au lieu de `poll-after-set` : le coordinateur est patché en cache et notifie ses listeners, supprimant le flapping de la vitesse de ventilation. |
| `__init__.py` | Setup : `ConfigEntryNotReady` sur indisponibilité transitoire au boot. Coordinateur (refresh) : `ApiError` **et** fuites non-`ApiError` (`KeyError`/`ValueError`/`TypeError`, `OSError`) → `UpdateFailed`. |
| `const.py` | `AIRSTAGE_SYNC_LOCAL_INTERVAL` 10 s → 60 s. `AIRSTAGE_LOCAL_RETRY` = 5 (identique à l'upstream net : abaissé à 3 puis restauré à 5 dans l'historique interne). |
| `manifest.json` | Pin `pyairstage>=2.4.1,<3` (voir « Décision de dépendance »). `version` 1.8.1 → 1.7.1. `use_https` et `AIRSTAGE_LOCAL_TIMEOUT_SECONDS` retirés. |

Le détail versionné et daté de ces patchs est tenu dans `CHANGELOG.arsenal.md`.

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
