# 🗺️ Architecture — Index (English overview)

> 🇫🇷 **Version française complète : [index.md](./index.md)** — this page is a concise English entry point; the full, authoritative listing is maintained in French.
>
> For scope, principles and the golden rule: see the French architecture home [`README.md`](./README.md).

---

## What this zone is

The `architecture/` zone is Arsenal's **implementation reference**: *how* the system is built and *why*. It documents cross-cutting doctrines, the structure of Home Assistant includes, the recorder, labels, and per-subsystem architecture notes.

It **introduces no business rule** — that is the job of [`contrats/`](../contrats/index.md). If a contract and an architecture note disagree on *what* the system must do, the contract wins.

---

## How it is organised

**Root files** — cross-cutting architecture notes, grouped by theme:

- **System logging & observability** — `00_system_log.md`, `01_logger.md`, `02_logbook.md`.
- **Infrastructure & energy** — `energie.md`, `infrastructure_puissance.md`.
- **Sensors & data** — `capteurs_meteo.md`, `securisation_capteurs_externes.md`, `capteurs_couleur.md`.
- **Governed ecosystem** — `ecosysteme_depots_satellites.md`: the canonical reference for the six satellite repositories (Bluetti library and integration, Airstage, Linky, Rain Bird ESP32 bridge, boiler bridge), their integration patterns and responsibility boundaries.
- **Domain subsystems** — architecture notes for ventilation, ECS recirculation, garden lighting, heating maintenance, weather display/interpretation, mobile notifications, openings, car.

**Sub-folders:**

| Folder | Content |
|---|---|
| [`00_structure_includes/`](./00_structure_includes/index.md) | Normative structure of Home Assistant includes (dedicated index). |
| [`01_recorder/`](./01_recorder/) | Recorder contract + decision record. |
| [`02_etiquettes/`](./02_etiquettes/) | Label system (automations, sensors, helpers, scripts). |
| [`03_doctrines/`](./03_doctrines/) | **Foundational doctrine library**: naming, causality, time handling, decision/action separation, git, general principles, automation IDs and domain-prefix contract. |
| [`chauffage/`](./chauffage/) | Heating architecture: boiler bridge, auto-adjustment observability. |
| [`presence/`](./presence/) | Presence architecture: presence chain, WiFi. |

The `03_doctrines/` folder holds the most structuring documents of the whole system (general principles, time handling, etc.).

---

For the complete, file-by-file classified listing — including the flagged, uncorrected naming anomalies — read the **[French index](./index.md)**.
