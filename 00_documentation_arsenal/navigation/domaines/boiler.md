# 🔥 Hub de domaine — Boiler

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Interface physique HA↔chaudière via Boiler Pi (Raspberry Pi exécutant le boiler bridge). Domaine à **double présence** : contrats HA dans [`contrats/boiler/`](../../contrats/boiler/README.md) (socle transactionnel, MQTT/ACK, retry, guard) et documentation de l'outil dans [`outils_externes/boiler_pi/`](../../outils_externes/boiler_pi/). Architecture dans `architecture/chauffage/`. **Non audité** (état de cycle).

## Contrat — « ce que le système doit faire »

**Contrats HA :**
- Entrée : [`contrats/boiler/README.md`](../../contrats/boiler/README.md) *(réfère à `outils_externes/boiler_pi/` — voir vigilance)*
- Contrat transactionnel central : [`socle_transactionnel.md`](../../contrats/boiler/socle_transactionnel.md)

**Documentation outil :**
- [`outils_externes/boiler_pi/`](../../outils_externes/boiler_pi/) — README · architecture · guard · mqtt · workflow

## Architecture — « comment / pourquoi »

- [`interface_ha_boiler_bridge.md`](../../architecture/chauffage/interface_ha_boiler_bridge.md) — Interface HA↔Boiler Bridge MQTT *(hébergé sous `architecture/chauffage/`)*

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : `contrats/boiler/README.md` et `socle_transactionnel.md`.
> État de cycle : non audité — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v13`, `v14`, `v15_8_3`.

## Liens croisés (sens & appartenance)

- **Chauffage** — [`contrats/chauffage/`](../../contrats/chauffage/) ; consomme le pont HA↔chaudière pour l'exécution thermique (aval).
- **ECS** — [`contrats/ecs/`](../../contrats/ecs/) ; consomme le boiler comme source thermique eau chaude sanitaire (aval).

## Points de vigilance (non normatif)

- **Double présence documentaire** : `contrats/boiler/` (contrats HA) + `outils_externes/boiler_pi/` (outil) — domaine unique parmi les 21 Tier-1.
- **Double titre README** : `contrats/boiler/README.md` et `outils_externes/boiler_pi/README.md` partagent le même titre (« Boiler Pi · Documentation »). Le README dans `contrats/` est un redirect vers `outils_externes/`.
- **`guard_expostion_ha.md`** : typo dans le nom de fichier (« expostion »). Signalé, non corrigé.
- **`interface_ha_boiler_bridge.md`** hébergé sous `architecture/chauffage/` — non trouvable depuis `architecture/boiler/` (inexistant). Signalé, non corrigé.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
