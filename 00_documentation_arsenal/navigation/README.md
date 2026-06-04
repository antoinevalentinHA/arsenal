# 🧭 Arsenal — Couche de navigation

> **NON NORMATIF.** Cette zone **n'établit aucune règle métier** : elle **oriente et agrège** la documentation. En cas de divergence avec un document de famille (`contrats/`, `architecture/`, `audits/`, `changelog/`, `ui/`…), **le document de famille fait foi**.

## Rôle

`navigation/` est une couche **distincte des familles de contenu** : elle ne contient ni contrat, ni architecture, ni audit, ni changelog. Elle **référence** ces documents pour rendre le corpus navigable, sans jamais les **redéfinir** ni les **dupliquer**. Elle est **détachable** : la retirer ne doit casser aucun document de famille.

## Contenu

- [`carte_domaines.md`](carte_domaines.md) — **registre canonique des domaines** et **autorité** de la couche : tout hub découle d'une de ses entrées (1 hub ⟺ 1 entrée Tier 1).
- `domaines/` — **hubs de domaine** (un par entrée Tier 1). Produits à ce jour : `chauffage`, `vacances`, `alarme` ; les autres suivront.
- `pivots/` — **pages pivot transverses** (à venir).

## Règles de la couche

- **Agréger sans dupliquer** : référencer un *document*, jamais une *entité*, une *version* ou un *seuil* (qui dérivent).
- **Non normatif** : la couche oriente, elle ne fait pas autorité ; le contenu prime.
- **Détachable** : aucun lien obligatoire depuis les familles vers cette zone.
- **Autorité de la carte** : `carte_domaines.md` fixe la liste des domaines ; aucun hub sans entrée correspondante.

## Gabarit de hub (v2)

**Sections obligatoires** : Bandeau non-normatif · Orientation · Contrat · Audits & état · Liens croisés · Points de vigilance.

**Sections conditionnelles** (rendues en section seulement si substance ; sinon repliées en une ligne dans Orientation ou Audits & état) : Architecture · Changelog.

## Règles des hubs (R1–R8)

- **R1 — Liens relatifs actifs** : uniquement des liens relatifs ; tout lien doit résoudre.
- **R2 — Ancrer, pas énumérer** : pointer l'entrée + les ancres canoniques ; jamais la liste exhaustive d'une famille.
- **R3 — Statut non recopié** : le hub renvoie vers l'état, il ne le duplique pas.
- **R4 — Anomalies signalées, non corrigées** : le hub note les particularités sans agir sur les familles.
- **R5 — Faits transverses délégués** : un fait partagé entre domaines est porté par un pivot, pas restitué dans chaque hub.
- **R6 — Direction & appartenance** : tout lien croisé précise le **propriétaire** et le **sens** (amont = consommé par le domaine ; aval = produit par le domaine).
- **R7 — Symétrie inter-hubs** : un artefact-frontière partagé est décrit de façon **cohérente** dans tous les hubs qui le référencent.
- **R8 — Source d'état explicite** : la section « Audits & état » **nomme** la source faisant foi (`audits/index.md` par défaut ; **substitution explicite** — rapport officiel, clôtures… — si le domaine en est absent).

---

*Charte de la couche `navigation/` (gabarit v2). Document non normatif. Ne duplique pas la carte des domaines.*
