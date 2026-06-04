#!/usr/bin/env python3

"""R-LL-INC-1 — Résolution des `!include` de la couche Lovelace.

Chantier : CH-LL-CI-1
Contrat  : R-LL-INC-1
Slug     : lovelace_includes
Cadrage  : 00_documentation_arsenal/audits/04_chantiers/transverses/
           cadrage_ci_includes_lovelace.md

Invariant
---------
Tout `!include` présent dans `18_lovelace/` doit pointer vers une cible
existante :

  - `!include <fichier>`          -> un FICHIER existant
                                     (résolu depuis le dossier du fichier
                                      source ; `/config/` -> racine du dépôt)
  - `!include_dir_*  <répertoire>` -> un RÉPERTOIRE existant
                                     (`/config/` -> racine du dépôt)

Périmètre STRICT (cf. cadrage §3)
---------------------------------
  - vérifie UNIQUEMENT l'existence des cibles ;
  - ne valide PAS le contenu YAML, ni les entités, ni les cartes ;
  - ne couvre PAS `filename:` de `dashboards.yaml` (ce n'est pas un `!include`) ;
  - ne couvre PAS les ressources `/local/...` de `resources.yaml` ;
  - se limite à l'arbre `18_lovelace/`.

Comportement (cf. cadrage §4)
-----------------------------
  - PASS (exit 0) si toutes les cibles existent ;
  - FAIL (exit 1, bloquant) si au moins une cible manque ;
  - rapport d'échec : fichier source, ligne, chemin déclaré, chemin résolu.

Implémentation : stdlib uniquement, lecture seule, déterministe.
"""

from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]

LOVELACE = ROOT / "18_lovelace"

# `/config` est l'alias runtime Home Assistant de la racine de configuration ;
# dans Arsenal il correspond à la racine du dépôt.
CONFIG_PREFIX = "/config/"

# Capture la directive (`!include` ou `!include_dir_*`) et sa cible littérale.
INCLUDE_RE = re.compile(r"!include(_dir_[a-z_]+)?\s+(\S+)")

ERRORS = []


def fail(msg: str):
    ERRORS.append(msg)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Logique de résolution (pure, paramétrable par racine)
# ==========================================================

def resolve_target(source_file: Path, raw: str, config_root: Path) -> Path:
    """Chemin cible d'un `!include`, sans aucune I/O."""
    if raw.startswith(CONFIG_PREFIX):
        return config_root / raw[len(CONFIG_PREFIX):]
    if raw.startswith("/"):
        return Path(raw)
    return source_file.parent / raw


def scan_directives(lovelace_root: Path):
    """Itère (source_file, lineno, raw_target, is_dir) sur tous les `!include`."""
    files = sorted(
        list(lovelace_root.rglob("*.yaml")) + list(lovelace_root.rglob("*.yml"))
    )
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in INCLUDE_RE.finditer(line):
                is_dir = match.group(1) is not None
                raw = match.group(2)
                yield path, lineno, raw, is_dir


def check_tree(lovelace_root: Path, config_root: Path):
    """Vérifie un arbre. Retourne (source, line, declared, resolved, is_dir, ok)."""
    results = []
    for source, lineno, raw, is_dir in scan_directives(lovelace_root):
        resolved = resolve_target(source, raw, config_root)
        try:
            ok = resolved.is_dir() if is_dir else resolved.is_file()
        except OSError:
            ok = False
        results.append((source, lineno, raw, resolved, is_dir, ok))
    return results


# Analyse du dépôt réel, calculée une fois.
REAL = check_tree(LOVELACE, ROOT)


# ==========================================================
# T1 — toutes les cibles `!include` Lovelace résolvent
# ==========================================================

def test_all_includes_resolve():
    for source, lineno, raw, resolved, is_dir, ok in REAL:
        if not ok:
            kind = "répertoire" if is_dir else "fichier"
            fail(
                f"{kind} cible introuvable | source={rel(source)}:{lineno} "
                f"| déclaré={raw} | résolu={rel(resolved)}"
            )

    if not ERRORS:
        print(f"✔ toutes les cibles !include Lovelace résolvent ({len(REAL)} vérifiées)")


# ==========================================================
# T2 — garde-fou anti-régression du parseur
# ==========================================================

def test_include_families_detected():
    # Bornes basses volontairement tolérantes : on détecte un parseur cassé
    # (zéro correspondance), pas une variation légitime de volume.
    plain = [r for r in REAL if not r[4]]
    dirs = [r for r in REAL if r[4]]

    if not plain:
        fail("aucun !include fichier détecté — parseur suspect")

    if not dirs:
        fail("aucun !include_dir_* détecté — parseur suspect")

    if not ERRORS:
        print(
            f"✔ familles d'include détectées "
            f"(fichiers={len(plain)}, répertoires={len(dirs)})"
        )


# ==========================================================
# T3 — auto-test de la logique de résolution (fixtures jetables)
# ==========================================================

def test_resolution_self_check():
    # Vérifie la double-détection sur une arborescence temporaire :
    # aucun faux positif sur cible présente, aucun faux négatif sur cible
    # absente. N'écrit jamais dans le dépôt.
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ll = base / "18_lovelace"
        (ll / "dashboards").mkdir(parents=True)
        (ll / "includes").mkdir(parents=True)
        (base / "dir_merge_ok").mkdir()
        (base / "dir_list_ok").mkdir()

        (ll / "includes" / "frag.yaml").write_text("x: 1\n", encoding="utf-8")
        (ll / "dashboards" / "voisin.yaml").write_text("y: 2\n", encoding="utf-8")
        (ll / "dashboards" / "page.yaml").write_text(
            "a: !include ../includes/frag.yaml\n"                  # relatif présent
            "b: !include ../includes/absent.yaml\n"               # relatif absent
            "c: !include voisin.yaml\n"                           # même dossier présent
            "d: !include_dir_merge_named /config/dir_merge_ok\n"  # dir présent
            "e: !include_dir_merge_named /config/absent_dir\n"    # dir absent
            "f: !include_dir_list /config/dir_list_ok\n",         # autre forme dir reconnue
            encoding="utf-8",
        )

        found = {
            raw: (is_dir, ok)
            for _, _, raw, _, is_dir, ok in check_tree(ll, config_root=base)
        }

        expected = {
            "../includes/frag.yaml": (False, True),
            "../includes/absent.yaml": (False, False),
            "voisin.yaml": (False, True),
            "/config/dir_merge_ok": (True, True),
            "/config/absent_dir": (True, False),
            "/config/dir_list_ok": (True, True),  # exige la reconnaissance de _dir_list
        }

        for decl, (exp_is_dir, exp_ok) in expected.items():
            if decl not in found:
                fail(f"auto-test : directive non détectée : {decl}")
                continue
            is_dir, ok = found[decl]
            if is_dir != exp_is_dir:
                fail(
                    f"auto-test : type mal classé pour {decl} "
                    f"(attendu dir={exp_is_dir}, obtenu={is_dir})"
                )
            if ok != exp_ok:
                fail(
                    f"auto-test : existence mal jugée pour {decl} "
                    f"(attendu={exp_ok}, obtenu={ok})"
                )

    if not ERRORS:
        print("✔ auto-test de résolution (présence / absence) conforme")


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_all_includes_resolve",
    "test_include_families_detected",
    "test_resolution_self_check",
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
        print("\n❌ CONTRAT LOVELACE_INCLUDES NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT LOVELACE_INCLUDES CONFORME")
