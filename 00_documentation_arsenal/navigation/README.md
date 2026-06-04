# 🧭 Arsenal — Couche de navigation

> **NON NORMATIF.** Cette zone **n'établit aucune règle** : elle **oriente et agrège** la documentation. En cas de divergence avec un document de famille (`contrats/`, `architecture/`, `audits/`, `changelog/`, `ui/`…), **le document de famille fait foi**.

## Rôle

`navigation/` est une couche **distincte des familles de contenu** : elle ne contient ni contrat, ni architecture, ni audit, ni changelog. Elle **référence** ces documents pour rendre le corpus navigable, sans jamais les **redéfinir** ni les **dupliquer**. Elle est **détachable** : la retirer ne doit casser aucun document de famille.

## Contenu actuel

- [`carte_domaines.md`](carte_domaines.md) — **registre canonique des domaines** et **autorité** de la couche : tout futur hub découle d'une de ses entrées (1 hub ⟺ 1 entrée Tier 1).

## À venir (pas encore présent)

- `domaines/` — **hubs de domaine** (un par entrée Tier 1 de la carte), agrégeant pour un domaine ses documents de plusieurs familles.
- `pivots/` — **pages transverses** (ex. matrice du cycle d'audit, registre « CH-x », cluster méta).

Ces artefacts seront produits **ensuite**, un par un, à partir de la carte. Aucun n'existe à ce stade.

## Règles de la couche

- **Agréger sans dupliquer** : référencer un *document*, jamais une *entité*, une *version* ou un *seuil* (qui dérivent).
- **Non normatif** : la couche oriente, elle ne fait pas autorité ; le contenu prime.
- **Détachable** : aucun lien obligatoire depuis les familles vers cette zone.
- **Autorité de la carte** : `carte_domaines.md` fixe la liste des domaines ; aucun hub sans entrée correspondante.

---

*Charte de la couche `navigation/`. Document non normatif. Ne duplique pas la carte des domaines.*
