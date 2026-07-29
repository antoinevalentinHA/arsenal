#!/usr/bin/env python3

"""R-LL-GRID-1 — Complétude structurelle des grilles Lovelace statiques.

Chantier : CH-LL-CI-2
Contrat  : R-LL-GRID-1
Slug     : lovelace_grid
Doctrine : 00_documentation_arsenal/ui/pattern_dashboard.md
           § « Géométrie des grilles locales »

Pourquoi ce checker
-------------------
La norme propriétaire (`pattern_dashboard.md`) rend opposable la géométrie des
cartes `type: grid`. Ce lot G1 contrôle, de façon **bloquante et déterministe**,
la seule **complétude structurelle statique** : une grille dont aucune cellule
directe ne peut disparaître au runtime doit déclarer `columns` (entier
strictement positif), porter une liste `cards` non vide, et présenter un nombre
de cellules directes divisible par `columns`.

Le contrôle G2 (géométrie dynamique) N'EST PAS implémenté dans ce lot : les
grilles dynamiques sont recensées, comptées à part, exclues de G1, et JAMAIS
annoncées comme conformes à G2.

Classification (trois états explicites)
---------------------------------------
  - STATIQUE démontrée : aucune cellule directe susceptible de disparaître ->
    les quatre invariants G1 s'appliquent.
  - DYNAMIQUE reconnue : au moins une cellule directe `type: conditional` ou
    portant une clé `visibility:` -> recensée, hors G1.
  - NON ANALYSABLE : structure/classification non déterminable de façon fiable
    -> échec explicite. Il est INTERDIT de classer statique par défaut une
    structure non comprise. Aucun fallback silencieux.

Cellule directe
---------------
Chaque entrée directe de `cards:` compte pour UNE cellule. Une stack, une grille
imbriquée ou une carte complexe reste UNE seule cellule de la grille parente ;
son contenu interne n'affecte pas le compte parent. Chaque grille imbriquée est
ensuite évaluée indépendamment.

Traitement des `!include`
-------------------------
Un `!include` en entrée directe de `cards:` ne compte pour une cellule que si sa
cible résout vers une carte-racine UNIQUE (mapping YAML) :
  - résolution relative au fichier source ;
  - cible existante et lisible ;
  - racine = mapping -> une cellule ;
  - racine liste / scalaire / null / autre -> échec explicite ;
  - cible absente / illisible / non analysable -> échec explicite ;
  - aucune expansion récursive générale (la résolution ne prouve que l'arité) ;
  - chaque fichier reste analysé indépendamment par le scan global (pas de
    double comptage fonctionnel).

Périmètre
---------
`18_lovelace/**/*.yaml` uniquement. Les structures ne déclarant pas `type: grid`
(`custom:grid-layout`, `custom:auto-entities`, `horizontal-stack`, …) sont hors
périmètre et ignorées.

Sortie / codes
--------------
  - exit 0 : conforme (toutes grilles statiques conformes, 0 non analysable) ;
  - exit 1 : violation contractuelle ou structure non analysable ;
  - exit 2 : échec interne ou auto-test défaillant.

Lecture seule, déterministe. Loader YAML structuré modelé sur
`check_lovelace_section_headers_contracts.py` (patron canonique Lovelace).
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML requis (pip install pyyaml).\n")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[2]
LOVELACE = ROOT / "18_lovelace"

MISSING = object()  # sentinelle « clé absente », distincte de None


# ==========================================================
# Représentation explicite des tags Home Assistant
# ==========================================================

class Tagged:
    """Représente un nœud tagué HA neutralisé, en conservant son type et sa cible.

    kind :
      - "include"      : `!include <cible>`  (résolvable pour prouver l'arité)
      - "include_dir"  : `!include_dir_*`    (non résolvable en carte unique)
      - "tag"          : tout autre tag `!foo` inconnu
    """

    __slots__ = ("kind", "raw")

    def __init__(self, kind: str, raw: str = ""):
        self.kind = kind
        self.raw = raw

    def __repr__(self):  # pragma: no cover - confort de debug
        return f"<{self.kind}:{self.raw}>"


# ==========================================================
# Loader YAML : structure + numéros de ligne + tags HA explicites
# ==========================================================

def _make_loader():
    class _L(yaml.SafeLoader):
        pass

    def _construct_mapping(loader, node, deep=False):
        mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
        mapping["__line__"] = node.start_mark.line + 1
        return mapping

    _L.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
    )
    # `!include` conservé explicitement (cible résolvable pour l'arité).
    _L.add_constructor("!include", lambda l, n: Tagged("include", l.construct_scalar(n)))
    # Familles `!include_dir_*` : représentées mais NON résolvables en carte unique.
    for _t in (
        "!include_dir_merge_named",
        "!include_dir_named",
        "!include_dir_list",
        "!include_dir_merge_list",
    ):
        _L.add_constructor(_t, lambda l, n, _t=_t: Tagged("include_dir", _t))
    _L.add_constructor("!secret", lambda l, n: "SECRET")
    # Tout autre tag `!...` inconnu : neutralisé en sentinelle (jamais un crash,
    # mais explicitement « non compris » -> NON ANALYSABLE s'il porte une cellule).
    _L.add_multi_constructor("!", lambda loader, suffix, node: Tagged("tag", suffix))
    return _L


_LOADER = _make_loader()


def load_yaml_text(text: str):
    return yaml.load(text, Loader=_LOADER)


def load_yaml_file(path: Path):
    return load_yaml_text(path.read_text(encoding="utf-8", errors="ignore"))


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Résolution d'arité d'un `!include` direct (mapping-racine unique)
# ==========================================================

def resolve_include_arity(source_file: Path, raw: str):
    """(ok: bool, motif: str). ok=True ssi la cible résout vers un mapping.

    Ne prouve QUE l'arité (racine mapping = une carte). Aucune expansion
    récursive : le contenu interne de la cible n'est pas parcouru ici.
    """
    if not isinstance(raw, str) or not raw.strip():
        return False, "cible d'include vide"
    if raw.startswith("/config/"):
        target = ROOT / raw[len("/config/"):]
    elif raw.startswith("/"):
        target = Path(raw)
    else:
        target = source_file.parent / raw

    try:
        if not target.is_file():
            return False, "cible absente"
    except OSError:
        return False, "cible inaccessible"
    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False, "cible illisible"
    try:
        data = load_yaml_text(text)
    except Exception:
        return False, "cible non analysable (YAML)"

    if isinstance(data, dict):
        return True, ""
    kind = "null" if data is None else type(data).__name__
    return False, f"racine {kind} (mapping attendu)"


# ==========================================================
# Évaluation d'une grille
# ==========================================================

# Classifications possibles.
CLS_STATIC_OK = "static_conform"
CLS_STATIC_KO = "static_violation"
CLS_DYNAMIC = "dynamic"
CLS_UNANALYSABLE = "non_analysable"


def _is_disappearing_cell(cell) -> bool:
    """Cellule directe susceptible de disparaître : `type: conditional` OU `visibility:`."""
    if isinstance(cell, dict):
        if cell.get("type") == "conditional":
            return True
        if "visibility" in cell:
            return True
    return False


def evaluate_grid(node: dict, source_file: Path):
    """Retourne (classification, [diagnostics])."""
    line = node.get("__line__", "?")
    p = f"{rel(source_file)}:{line} : R-LL-GRID-1 —"
    cards = node.get("cards", MISSING)
    columns = node.get("columns", MISSING)

    # --- 1) DYNAMIQUE : marqueur littéral direct (uniquement si cards est une liste) ---
    if isinstance(cards, list):
        if any(_is_disappearing_cell(c) for c in cards):
            return CLS_DYNAMIC, []

    # --- 2) `cards` non énumérable statiquement (tag) -> NON ANALYSABLE ---
    if isinstance(cards, Tagged):
        return CLS_UNANALYSABLE, [
            f"{p} `cards` non analysable (tag !{cards.kind}) — "
            f"impossible d'énumérer les cellules directes"
        ]

    diags: list[str] = []

    # --- 3) Invariant `columns` ---
    col_ok = (
        columns is not MISSING
        and isinstance(columns, int)
        and not isinstance(columns, bool)
        and columns > 0
    )
    if columns is MISSING:
        diags.append(f"{p} `columns` absent")
    elif not col_ok:
        diags.append(
            f"{p} `columns` doit être un entier strictement positif "
            f"(obtenu : {columns!r})"
        )

    # --- 4) Invariant `cards` = liste non vide ---
    if not isinstance(cards, list):
        diags.append(f"{p} `cards` doit être une liste non vide")
        return CLS_STATIC_KO, diags
    if len(cards) == 0:
        diags.append(f"{p} `cards` doit être une liste non vide")
        return CLS_STATIC_KO, diags

    # --- 5) Comptage des cellules directes (avec preuve d'arité des includes) ---
    n_cells = 0
    unanalysable = False
    for cell in cards:
        if isinstance(cell, Tagged):
            if cell.kind == "include":
                ok, why = resolve_include_arity(source_file, cell.raw)
                if ok:
                    n_cells += 1
                else:
                    diags.append(
                        f"{p} include direct non analysable ou ne résolvant pas "
                        f"vers une carte-racine unique — {cell.raw} ({why})"
                    )
                    unanalysable = True
            else:
                diags.append(
                    f"{p} cellule directe non analysable (tag !{cell.kind}) — "
                    f"arité indéterminable"
                )
                unanalysable = True
        elif isinstance(cell, dict):
            n_cells += 1
        else:
            kind = "null" if cell is None else type(cell).__name__
            diags.append(
                f"{p} cellule directe non analysable (type {kind}) — "
                f"carte attendue"
            )
            unanalysable = True

    if unanalysable:
        return CLS_UNANALYSABLE, diags

    # --- 6) Invariant de divisibilité (uniquement si `columns` valide) ---
    if not col_ok:
        return CLS_STATIC_KO, diags  # violation `columns` déjà consignée
    remainder = n_cells % columns
    if remainder != 0:
        diags.append(
            f"{p} grille statique incomplète : "
            f"columns={columns}, cells={n_cells}, remainder={remainder}"
        )
        return CLS_STATIC_KO, diags

    return (CLS_STATIC_KO, diags) if diags else (CLS_STATIC_OK, [])


# ==========================================================
# Marche récursive : toutes les grilles, imbriquées comprises
# ==========================================================

def collect_grids(node, source_file: Path, acc: list):
    if isinstance(node, dict):
        t = node.get("type")
        if isinstance(t, str) and t.strip().lower() == "grid":
            acc.append(node)
        for key, value in node.items():
            if key == "__line__":
                continue
            collect_grids(value, source_file, acc)
    elif isinstance(node, list):
        for value in node:
            collect_grids(value, source_file, acc)


# ==========================================================
# Analyse d'un arbre Lovelace
# ==========================================================

class Report:
    def __init__(self):
        self.files = 0
        self.grids_total = 0
        self.static = 0
        self.static_conform = 0
        self.dynamic = 0
        self.unanalysable = 0
        self.diagnostics: list[str] = []
        # (rel_file, line, classification) — pour l'auto-test
        self.records: list[tuple] = []


def analyze(lovelace_dir: Path) -> Report:
    r = Report()
    files = sorted(lovelace_dir.rglob("*.yaml"))
    r.files = len(files)

    for path in files:
        try:
            data = load_yaml_file(path)
        except Exception as exc:
            r.unanalysable += 1
            r.diagnostics.append(
                f"{rel(path)}:1 : R-LL-GRID-1 — fichier YAML non analysable — {exc}"
            )
            r.records.append((rel(path), 1, CLS_UNANALYSABLE))
            continue

        grids: list[dict] = []
        collect_grids(data, path, grids)

        for node in grids:
            r.grids_total += 1
            cls, diags = evaluate_grid(node, path)
            r.diagnostics.extend(diags)
            r.records.append((rel(path), node.get("__line__", "?"), cls))

            if cls == CLS_DYNAMIC:
                r.dynamic += 1
            elif cls == CLS_UNANALYSABLE:
                r.unanalysable += 1
            elif cls == CLS_STATIC_OK:
                r.static += 1
                r.static_conform += 1
            else:  # CLS_STATIC_KO
                r.static += 1

    return r


# ==========================================================
# Auto-test (fixtures jetables, jamais d'écriture dans le dépôt)
# ==========================================================

def _write(base: Path, relpath: str, content: str):
    p = base / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


def selftest() -> list[str]:
    failures: list[str] = []

    def card(name="X"):
        return (
            "      - type: custom:button-card\n"
            f"        name: {name}\n"
        )

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ll = base / "18_lovelace"
        (ll / "dashboards").mkdir(parents=True)
        inc = ll / "includes"
        inc.mkdir(parents=True)

        # Cibles d'include pour les cas 16/17/18.
        _write(inc, "carte_unique.yaml", "type: custom:button-card\nname: Incluse\n")
        _write(inc, "liste.yaml", "- type: custom:button-card\n- type: custom:button-card\n")

        # 1) statique 2 col / 4 cellules -> conforme
        _write(ll, "d/c01.yaml",
               "type: grid\ncolumns: 2\ncards:\n" + card() * 4)
        # 2) statique 2 col / 3 cellules -> violation
        _write(ll, "d/c02.yaml",
               "type: grid\ncolumns: 2\ncards:\n" + card() * 3)
        # 3) columns absent -> violation
        _write(ll, "d/c03.yaml",
               "type: grid\ncards:\n" + card() * 2)
        # 4) columns 0 -> violation
        _write(ll, "d/c04.yaml",
               "type: grid\ncolumns: 0\ncards:\n" + card() * 2)
        # 5) columns négatif -> violation
        _write(ll, "d/c05.yaml",
               "type: grid\ncolumns: -2\ncards:\n" + card() * 2)
        # 6) columns "2" (str) -> violation
        _write(ll, "d/c06.yaml",
               'type: grid\ncolumns: "2"\ncards:\n' + card() * 2)
        # 7) columns templatisé -> violation
        _write(ll, "d/c07.yaml",
               'type: grid\ncolumns: "{{ states(\'x\') }}"\ncards:\n' + card() * 2)
        # 8) cards absent -> violation
        _write(ll, "d/c08.yaml",
               "type: grid\ncolumns: 2\n")
        # 9) cards null -> violation
        _write(ll, "d/c09.yaml",
               "type: grid\ncolumns: 2\ncards:\n")
        # 10) cards [] -> violation
        _write(ll, "d/c10.yaml",
               "type: grid\ncolumns: 2\ncards: []\n")
        # 11) cards non-liste -> violation
        _write(ll, "d/c11.yaml",
               "type: grid\ncolumns: 2\ncards:\n  a: 1\n")
        # 12) columns 1 + cartes valides -> conforme
        _write(ll, "d/c12.yaml",
               "type: grid\ncolumns: 1\ncards:\n" + card() * 3)
        # 13) conditional enfant direct -> dynamique
        _write(ll, "d/c13.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: conditional\n"
                 "        conditions: []\n"
                 "        card:\n"
                 "          type: custom:button-card\n")
        # 14) visibility directe -> dynamique
        _write(ll, "d/c14.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: custom:button-card\n"
                 "        visibility:\n"
                 "          - condition: state\n")
        # 15) grille imbriquée : fille évaluée à part + 1 cellule pour la mère
        _write(ll, "d/c15.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - type: grid\n"
                 "        columns: 3\n"
                 "        cards:\n"
                 "          - type: custom:button-card\n"
                 "          - type: custom:button-card\n"
                 "          - type: custom:button-card\n")
        # 16) include direct -> racine mapping -> une cellule (2 col / 2 cellules)
        _write(ll, "d/c16.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/carte_unique.yaml\n")
        # 17) include direct -> racine liste -> non analysable
        _write(ll, "d/c17.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/liste.yaml\n")
        # 18) include cible absente -> non analysable
        _write(ll, "d/c18.yaml",
               "type: grid\ncolumns: 2\ncards:\n"
               + card()
               + "      - !include ../includes/introuvable.yaml\n")
        # 19) hors périmètre : grid-layout / auto-entities / horizontal-stack -> ignorés
        _write(ll, "d/c19a.yaml",
               "type: custom:grid-layout\nlayout: {}\ncards:\n" + card())
        _write(ll, "d/c19b.yaml",
               "type: custom:auto-entities\nfilter:\n  include: []\n")
        _write(ll, "d/c19c.yaml",
               "type: horizontal-stack\ncards:\n" + card() * 2)
        # 20) cards via tag (non énumérable) -> non analysable
        _write(ll, "d/c20.yaml",
               "type: grid\ncolumns: 2\ncards: !include ../includes/carte_unique.yaml\n")

        r = analyze(ll)

        def cls_of(fragment):
            hits = [c for (f, _, c) in r.records if fragment in f]
            return hits

        expect = {
            "c01.yaml": [CLS_STATIC_OK],
            "c02.yaml": [CLS_STATIC_KO],
            "c03.yaml": [CLS_STATIC_KO],
            "c04.yaml": [CLS_STATIC_KO],
            "c05.yaml": [CLS_STATIC_KO],
            "c06.yaml": [CLS_STATIC_KO],
            "c07.yaml": [CLS_STATIC_KO],
            "c08.yaml": [CLS_STATIC_KO],
            "c09.yaml": [CLS_STATIC_KO],
            "c10.yaml": [CLS_STATIC_KO],
            "c11.yaml": [CLS_STATIC_KO],
            "c12.yaml": [CLS_STATIC_OK],
            "c13.yaml": [CLS_DYNAMIC],
            "c14.yaml": [CLS_DYNAMIC],
            "c16.yaml": [CLS_STATIC_OK],
            "c17.yaml": [CLS_UNANALYSABLE],
            "c18.yaml": [CLS_UNANALYSABLE],
            "c20.yaml": [CLS_UNANALYSABLE],
        }
        for frag, exp in expect.items():
            got = cls_of(frag)
            if got != exp:
                failures.append(f"auto-test {frag} : attendu {exp}, obtenu {got}")

        # 15) grille imbriquée : deux grilles, toutes deux conformes
        got15 = sorted(cls_of("c15.yaml"))
        if got15 != sorted([CLS_STATIC_OK, CLS_STATIC_OK]):
            failures.append(
                f"auto-test c15.yaml (imbrication) : attendu 2 statiques conformes, "
                f"obtenu {got15}"
            )

        # 19) hors périmètre : aucune grille détectée dans ces 3 fichiers
        for frag in ("c19a.yaml", "c19b.yaml", "c19c.yaml"):
            if cls_of(frag):
                failures.append(
                    f"auto-test {frag} : structure hors périmètre détectée à tort "
                    f"comme grille ({cls_of(frag)})"
                )

        # Diagnostics ciblés (preuves négatives)
        joined = "\n".join(r.diagnostics)
        checks = [
            ("c02.yaml", "grille statique incomplète"),
            ("c03.yaml", "`columns` absent"),
            ("c04.yaml", "entier strictement positif"),
            ("c06.yaml", "entier strictement positif"),
            ("c08.yaml", "`cards` doit être une liste non vide"),
            ("c10.yaml", "`cards` doit être une liste non vide"),
            ("c17.yaml", "carte-racine unique"),
            ("c18.yaml", "carte-racine unique"),
        ]
        for frag, msg in checks:
            if not any(frag in d and msg in d for d in r.diagnostics):
                failures.append(
                    f"auto-test : diagnostic attendu introuvable — {frag} / «{msg}»"
                )

        # Comptes agrégés attendus sur les fixtures.
        # dynamiques = c13, c14
        if r.dynamic != 2:
            failures.append(f"auto-test : dynamiques attendu 2, obtenu {r.dynamic}")
        # non analysables = c17, c18, c20
        if r.unanalysable != 3:
            failures.append(
                f"auto-test : non analysables attendu 3, obtenu {r.unanalysable}"
            )

    return failures


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    print("Arsenal — Validation contractuelle : Grilles Lovelace (R-LL-GRID-1)")
    print("Règle : toute grille statique `type: grid` a `columns` entier > 0, "
          "`cards` liste non vide, cellules directes divisibles par `columns`.\n")

    # Auto-test AVANT le scan réel.
    st = selftest()
    if st:
        print("❌ AUTO-TEST EN ÉCHEC")
        for f in st:
            print(f"  - {f}")
        return 2
    print("✔ auto-test conforme (20 cas : statiques / dynamiques / non analysables "
          "/ includes / imbrication / hors périmètre)")

    r = analyze(LOVELACE)

    static_violations = r.static - r.static_conform

    if r.diagnostics:
        print(f"\n❌ DIAGNOSTICS ({len(r.diagnostics)}) :")
        for d in r.diagnostics:
            print(f"  - {d}")

    print("\n— Résumé —")
    print(f"  fichiers YAML analysés          : {r.files}")
    print(f"  grilles totales                 : {r.grids_total}")
    print(f"  grilles statiques               : {r.static}")
    print(f"  grilles dynamiques (exclues G1) : {r.dynamic}")
    print(f"  grilles non analysables         : {r.unanalysable}")
    print(f"  grilles statiques conformes     : {r.static_conform}")
    print(f"  violations G1 (grilles)         : {static_violations}")
    print("\n  Note : R-LL-GRID-2 (géométrie dynamique) N'EST PAS implémenté dans "
          "ce lot ;\n         les grilles dynamiques ne sont PAS déclarées conformes à G2.")

    if static_violations or r.unanalysable:
        print("\n❌ CONTRAT LOVELACE_GRID (R-LL-GRID-1) NON CONFORME")
        return 1

    print("\n✅ CONTRAT LOVELACE_GRID (R-LL-GRID-1) CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
