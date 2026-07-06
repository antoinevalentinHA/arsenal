# 📋 Functional Contracts — Index (English overview)

> 🇫🇷 **Version française complète : [index.md](./index.md)** — this page is a concise English entry point; the full, authoritative listing is maintained in French.
>
> For the role, status and principles of contracts: see the French contracts home [`README.md`](./README.md).

---

## What a contract is

A contract states **what a subsystem must do**: user intent, business rules, invariants, forbidden drifts. The core principle is **the contract precedes the implementation** — if the YAML contradicts the contract, the implementation is wrong, however elegant it may be.

---

## Flat contracts (root)

Single-file contracts, grouped by theme:

- **Presence & human context** — presence, holidays, visits, babysitting, night wake-ups, presence simulation, high-accuracy geolocation, home BSSID reference.
- **System & infrastructure** — `arsenal_nas`, `arsenal_self`, Lovelace resources, zones, invalid parameters, LAN ping synthesis, SwitchBot transactional core, Netatmo/HomeKit diagnostics, integration resilience, UPS-driven HA shutdown, notifications.
- **Energy & equipment** — batteries, Bluetti (`energie_chaudiere`), authorised energy sources, small-house water heater, appliance cycle detection.
- **Physical environment & safety** — ventilation recommendation, wood stove (exogenous heat input), ECS recirculation, MHRV, rain-driven shutters, motion, car.

> Note: the "transversal" qualifier in the French index means "cross-domain impact"; it does **not** designate a domain-prefix of ID `transversal`. Each of these contracts still has a single owning domain.

---

## Domain contracts (sub-folders)

Folderised domains, each with its own `README.md` navigation entry:

| Domain | Files | Scope |
|---|:--:|---|
| [`aeration_blocage_chauffage/`](./aeration_blocage_chauffage/) | 37 | Ventilation → heating-block state machine (m0→m6). |
| [`alarme/`](./alarme/) | 16 | Alarm pipeline, numbered 00→99. |
| [`arrosage/`](./arrosage/) | 19 | Garden irrigation — governed Arsenal ↔ Rain Bird coexistence, hydric observation. |
| [`boiler/`](./boiler/) | 7 | Boiler / boiler bridge. |
| [`chauffage/`](./chauffage/) | 52 | Heating pipeline + sensors + amendments. |
| [`climatisation/`](./climatisation/) | 42 | Air conditioning (15 root + 27 sensors). |
| [`deshumidificateur/`](./deshumidificateur/) | 3 | Cellar dehumidifier. |
| [`eclairage/`](./eclairage/) | 7 | Lighting. |
| [`ecs/`](./ecs/) | 29 | Domestic hot water — foundation + execution contracts. |
| [`imprimerie/`](./imprimerie/) | 4 | Industrial-machine noise (print shop). |
| [`meteo/`](./meteo/) | 21 | Weather — axes, rankings, validation, sub-domains. |
| [`ouvertures/`](./ouvertures/) | 4 | Openings (doors / windows). |
| [`pannes/`](./pannes/) | 11 | Outages — internet + mains. |
| [`publication/`](./publication/) | 2 | Publication. |
| [`sante/`](./sante/) | 3 | Health — night cardio + Withings sleep. |

---

For the complete, contract-by-contract listing — including per-domain file counts and the flagged, uncorrected anomalies — read the **[French index](./index.md)**.
