# 💧 Hub de domaine — Humidité relative intérieure

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Fournisseur de mesure d'humidité relative intérieure. Pipeline multi-couches : *capteurs bruts → consolidation (`humidite_relative_brute_consolidee_<zone>`) → stabilisation (`humidite_relative_stabilisee_<zone>`)*. Rôle pur de mesure — aucune décision. Domaine propre, **physiquement logé sous `contrats/meteo/` par héritage** (arbitrage acté — voir [`carte_domaines.md`](../carte_domaines.md) §5.3 et §6). **Pas de contrat d'axe dédié** (contrairement à `temperature_interieure`). Aucune architecture-famille. **Domaine non audité** (état de cycle acté en carte §6).

## Contrat — « ce que le système doit faire »

Tous logés sous `contrats/meteo/` (héritage — domaine propre) :

- Consolidation : [`humidite_relative_interieure/consolidation.md`](../../contrats/meteo/humidite_relative_interieure/consolidation.md) (v1.1 — `sensor.humidite_relative_brute_consolidee_<zone>`)
- Stabilisation : [`humidite_relative_interieure/stabilisation.md`](../../contrats/meteo/humidite_relative_interieure/stabilisation.md) (v1.1 — `sensor.humidite_relative_stabilisee_<zone>`)

## Audits & état

> **Domaine non audité** — aucun artefact d'audit, absent de [`audits/index.md`](../../audits/index.md).
> Référence normative : les deux contrats ci-dessus.
> État de cycle : non audité (acté en carte §6) — cf. [`carte_domaines.md`](../carte_domaines.md).

> **Changelog** : aucune mention vXX significative identifiée.

## Liens croisés (sens & appartenance)

Humidité relative intérieure est un **fournisseur de mesure** (amont). Consommateurs principaux :

- **Déshumidificateur** — [`contrats/deshumidificateur/`](../../contrats/deshumidificateur/) ; consomme l'humidité relative (RH) pour piloter la déshumidification cave (aval).
- **Climatisation** — [`contrats/climatisation/`](../../contrats/climatisation/) ; le mode DRY utilise l'humidex des chambres (dérivé de humidité + température) — consommation **indirecte via humidex** (aval).

> D'autres domaines peuvent consommer l'humidité intérieure ; liste non exhaustive.

## Points de vigilance (non normatif)

- **Domaine propre logé sous `contrats/meteo/`** : héritage physique, pas la taxonomie (arbitrage acté — carte §5.3).
- **Pas de contrat d'axe** : `axe_humidite_relative_jardin.md` (extérieure / meteo) cohabite sous `contrats/meteo/` — objet distinct. Aucun équivalent intérieur, contrairement à `temperature_interieure` qui dispose de `axe_temperature.md`.
- **Domaine non audité** : absent de `audits/index.md` — état de cycle acté en carte §6, pas un manque.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
