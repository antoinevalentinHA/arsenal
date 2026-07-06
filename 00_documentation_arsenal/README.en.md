# 🧠 Arsenal — Reference Documentation (English overview)

> 🇫🇷 **Version française complète : [README.md](./README.md)** — this page is a concise English entry point; the full corpus is maintained in French.
>
> 🏠 Repository entry point: [`../README.md`](../README.md) (English) · [`../README.fr.md`](../README.fr.md) (French).

---

## Purpose

This folder holds the **functional, architectural and historical documentation** of the **Arsenal** system. It is neither Home Assistant help, nor a tutorial, nor a Git commit log.

It describes:

- what the system **must do** (contracts),
- **how** and **why** it is built this way (architecture),
- how it **evolved** over time (changelog, history),
- how it is **audited** and governed (audits),
- how it **interfaces** with external tools,
- how it is **navigated** transversally (navigation).

It is the system's **source of truth**.

> **Golden rule.** What is not documented here does not exist functionally. Conversely, what is documented here must be traceable in the system.

---

## General philosophy

Arsenal rests on a strict separation between **user intent**, **business rules**, **observable decisions** and **physical actions**. The documentation mirrors this separation: the **contract** (what the system must do) is distinct from the **architecture** (how it does it). If an implementation contradicts a contract, the implementation is wrong.

---

## The nine zones

The folder is organised into nine top-level zones, plus this README:

| Zone | Role |
|---|---|
| [`architecture/`](./architecture/index.md) | Implementation reference — how / why it is built. Introduces no business rule. |
| [`audits/`](./audits/index.md) | Per-domain audit life cycle: reports → arbitrations/analyses → action plans → work items → closures. |
| [`changelog/`](./changelog/index.md) | Versioned evolution over time + retrospective history. |
| [`contrats/`](./contrats/index.md) | Normative reference — what each subsystem **must do**. The contract precedes the implementation. |
| [`evolutions_futures/`](./evolutions_futures/README.md) | Airlock for prospective notes not yet formalised. |
| [`navigation/`](./navigation/README.md) | Cross-family orientation: domain map, hubs, thematic pivots. Non-normative. |
| [`outils_externes/`](./outils_externes/README.md) | Supervision of tools outside Home Assistant (boiler bridge, NAS tooling). |
| [`schemas_ascii/`](./schemas_ascii/README.md) | ASCII pipeline diagrams for quick plain-text reading. |
| [`ui/`](./ui/README.md) | Colour charter and Lovelace card foundation. |

---

## Where to look

| Question | Zone |
|---|---|
| "What **must** this domain do?" | [`contrats/`](./contrats/index.md) |
| "**How** is it implemented, and why?" | [`architecture/`](./architecture/index.md) |
| "**What changed** and when?" | [`changelog/`](./changelog/index.md) |
| "Has this been **audited**?" | [`audits/`](./audits/index.md) |
| "How does Arsenal talk to an **external tool**?" | [`outils_externes/`](./outils_externes/README.md) |
| "What does the **pipeline** look like?" | [`schemas_ascii/`](./schemas_ascii/README.md) |
| "Which **colour / card** should the UI use?" | [`ui/`](./ui/README.md) |
| "An **idea** not yet formalised?" | [`evolutions_futures/`](./evolutions_futures/README.md) |
| "**How to navigate** the documentation?" | [`navigation/`](./navigation/README.md) |

---

## What this documentation is *not*

- ❌ a Home Assistant configuration dump
- ❌ end-user documentation
- ❌ a Git commit log
- ❌ a scratch-notes space

---

## Status

- Scope: **the Arsenal system**
- Nature: **reference documentation**
- Authority: **functional contracts** (they take precedence over code)
- Updates: deliberate, reasoned, traced in the changelog

For the full detail — the nine zones described one by one, the "read before you modify" matrix for contributors and AI, and the CI gates that keep the corpus honest — read the **[French version](./README.md)**.
