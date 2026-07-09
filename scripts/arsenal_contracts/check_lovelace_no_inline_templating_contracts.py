#!/usr/bin/env python3

"""R-LL-SKEL-1 — Squelette pur : aucun template Jinja inline dans un dashboard.

Contrat  : R-LL-SKEL-1
Slug     : lovelace_no_inline_templating

Invariant
---------
Un dashboard Arsenal est un **squelette** : il compose des cartes via
`!include` et n'embarque aucune logique. Toute la logique de rendu
(templates Jinja `{% ... %}` / `{{ ... }}`) doit vivre dans un **include**
de contenu (`18_lovelace/includes/**`), jamais dans le fichier dashboard.

Concrètement, aucun fichier sous `18_lovelace/dashboards/**` ne doit
contenir de délimiteur de template Jinja :

  - `{%` … `%}`  (tag Jinja)
  - `{{` … `}}`  (expression Jinja)

Périmètre STRICT
----------------
  - vérifie UNIQUEMENT l'arbre `18_lovelace/dashboards/` ;
  - les `18_lovelace/includes/**` sont HORS périmètre : c'est précisément
    là que la logique Jinja est légitime et attendue ;
  - ne valide PAS le YAML, ni les entités, ni le rendu des cartes ;
  - contrôle purement textuel (détection de présence de délimiteurs) :
    déterministe, sans exécution ni résolution.

Comportement
------------
  - PASS (exit 0) si aucun dashboard ne contient de délimiteur Jinja ;
  - FAIL (exit 1, bloquant) sinon ;
  - rapport d'échec : fichier source, ligne, extrait fautif.

Implémentation : stdlib uniquement, lecture seule, déterministe.
"""

from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]

DASHBOARDS = ROOT / "18_lovelace" / "dashboards"

# Délimiteurs d'ouverture Jinja : un tag (`{%`) ou une expression (`{{`).
TEMPLATING_RE = re.compile(r"\{%|\{\{")

ERRORS = []


def fail(msg: str):
    ERRORS.append(msg)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Logique de détection (pure, paramétrable par racine)
# ==========================================================

def scan_dashboards(dashboards_dir: Path):
    """Retourne la liste des (fichier, ligne, extrait) portant un délimiteur.

    Purement textuel : on repère la présence d'un délimiteur d'ouverture
    Jinja sur chaque ligne des fichiers `*.yaml` du sous-arbre.
    """
    hits = []

    for path in sorted(dashboards_dir.rglob("*.yaml")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            # Un fichier illisible n'est pas un template ; on l'ignore
            # (le contrat de résolution des includes couvre l'existence).
            continue

        for lineno, line in enumerate(lines, start=1):
            if TEMPLATING_RE.search(line):
                hits.append((path, lineno, line.strip()))

    return hits


# ==========================================================
# T1 — aucun dashboard ne porte de template Jinja inline
# ==========================================================

def test_no_inline_templating_in_dashboards():
    hits = scan_dashboards(DASHBOARDS)

    for path, lineno, snippet in hits:
        extract = snippet if len(snippet) <= 120 else snippet[:117] + "…"
        fail(
            f"template Jinja inline dans un dashboard | "
            f"source={rel(path)}:{lineno} | extrait={extract}"
        )

    if not ERRORS:
        scanned = len(list(DASHBOARDS.rglob("*.yaml")))
        print(
            f"✔ aucun template Jinja inline dans les dashboards "
            f"({scanned} fichiers vérifiés)"
        )


# ==========================================================
# T2 — auto-test de la détection (fixtures jetables)
# ==========================================================

def test_detection_self_check():
    # Vérifie : détection d'un tag et d'une expression dans un dashboard,
    # non-détection d'un squelette pur, et exclusion stricte de l'arbre
    # `includes/` (où le Jinja est légitime). N'écrit jamais dans le dépôt.
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        dash = base / "18_lovelace" / "dashboards"
        incl = base / "18_lovelace" / "includes"
        (dash / "sous_domaine").mkdir(parents=True)
        incl.mkdir(parents=True)

        # Squelette pur : uniquement des !include et de la structure.
        (dash / "propre.yaml").write_text(
            "views:\n"
            "  - cards:\n"
            "      - type: vertical-stack\n"
            "        cards:\n"
            "          - !include ../../includes/cartes/x.yaml\n",
            encoding="utf-8",
        )
        # Dashboard fautif : une expression Jinja.
        (dash / "sous_domaine" / "expression.yaml").write_text(
            "type: markdown\n"
            "content: |\n"
            "  {{ states('sensor.x') }}\n",
            encoding="utf-8",
        )
        # Dashboard fautif : un tag Jinja.
        (dash / "sous_domaine" / "tag.yaml").write_text(
            "content: |\n"
            "  {% set x = 1 %}\n",
            encoding="utf-8",
        )
        # Include AVEC Jinja : doit être IGNORÉ (hors périmètre).
        (incl / "frag.yaml").write_text(
            "type: markdown\n"
            "content: |\n"
            "  {{ states('sensor.y') }}\n",
            encoding="utf-8",
        )

        found = {rel_to(base, p): lineno for p, lineno, _ in scan_dashboards(dash)}

        expected = {
            "18_lovelace/dashboards/sous_domaine/expression.yaml",
            "18_lovelace/dashboards/sous_domaine/tag.yaml",
        }
        got = set(found)

        for miss in expected - got:
            fail(f"auto-test : Jinja inline non détecté dans {miss}")

        for extra in got - expected:
            fail(f"auto-test : faux positif de détection sur {extra}")

        # Garde-fou d'exclusion : aucun hit ne doit provenir de includes/.
        if any("includes/" in k for k in got):
            fail("auto-test : l'arbre includes/ ne doit PAS être scanné")

    if not ERRORS:
        print("✔ auto-test de détection (présence / exclusion) conforme")


def rel_to(base: Path, path: Path) -> str:
    return str(path.resolve().relative_to(base.resolve()))


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_no_inline_templating_in_dashboards",
    "test_detection_self_check",
]


# ==========================================================
# validation registre ↔ fonctions
# ==========================================================

def test_test_registry_matches_functions():
    missing = []

    for test_name in TESTS:
        if test_name not in globals():
            missing.append(test_name)

    if missing:
        for name in missing:
            fail(f"fonction absente du registre TESTS : {name}")

    if not ERRORS:
        print("✔ registre TESTS cohérent")


# ==========================================================
# exécution
# ==========================================================

if __name__ == "__main__":

    for test_name in TESTS:
        globals()[test_name]()

    test_test_registry_matches_functions()

    if ERRORS:
        print("\n❌ CONTRAT LOVELACE_NO_INLINE_TEMPLATING NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT LOVELACE_NO_INLINE_TEMPLATING CONFORME")
