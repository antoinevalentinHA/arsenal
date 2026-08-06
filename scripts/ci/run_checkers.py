#!/usr/bin/env python3
"""
Arsenal — Exécuteur agrégé de checkers de contrat (consolidation CI).

Rôle : lancer plusieurs `scripts/arsenal_contracts/check_*.py` dans UN seul
job GitHub Actions, au lieu d'un workflow (donc une VM) par checker. Chaque
checker Arsenal étant un scan de ~1 s, l'overhead de VM (~25-30 s) dominait :
ce regroupement supprime les VM redondantes sans rien changer aux checkers.

Garanties (parité de comportement avec « 1 workflow = 1 checker ») :
  - chaque checker est exécuté par un SOUS-PROCESSUS isolé (`python <check>.py`),
    exactement comme son ancien workflow — aucun état partagé entre checkers ;
  - un checker qui supporte `--selftest` (détecté dans sa source) le passe
    D'ABORD (« on ne juge pas avec un juge défectueux »), comme son workflow ;
  - TOUS les checkers sont lancés même si l'un échoue (pas d'arrêt au premier
    rouge) : on voit l'ensemble des échecs d'un coup, mieux qu'aujourd'hui ;
  - sortie de code 1 si UN SEUL checker (ou son selftest) échoue, 0 sinon.

La liste des checkers est fournie en arguments (la source de vérité du
regroupement est le workflow `contracts.yml`). Ce script ne découvre rien tout
seul : il exécute ce qu'on lui nomme. La complétude (aucun checker oublié) est
prouvée indépendamment par `check_ci_coverage_registry.py` (INTEG-1), inchangé.

Usage :
  python scripts/ci/run_checkers.py check_ecs_fondations.py check_bouclage_contracts.py ...
  python scripts/ci/run_checkers.py --dir scripts/arsenal_contracts <noms...>
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = ROOT / "scripts" / "arsenal_contracts"


def supports_selftest(path: Path) -> bool:
    try:
        return "--selftest" in path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def run_one(path: Path) -> tuple[bool, str]:
    """Renvoie (succès, détail). Lance le selftest d'abord si supporté."""
    if supports_selftest(path):
        st = subprocess.run(
            [sys.executable, str(path), "--selftest"],
            capture_output=True, text=True,
        )
        if st.returncode != 0:
            return False, "selftest KO\n" + (st.stdout or "") + (st.stderr or "")
    res = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, text=True,
    )
    ok = res.returncode == 0
    return ok, (res.stdout or "") + (res.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("checkers", nargs="+", help="noms de fichiers check_*.py")
    ap.add_argument("--dir", default=str(DEFAULT_DIR),
                    help="dossier des checkers (défaut: scripts/arsenal_contracts)")
    args = ap.parse_args()

    base = Path(args.dir)
    if not base.is_absolute():
        base = ROOT / base

    failures: list[str] = []
    print(f"▶ {len(args.checkers)} checker(s) — {base.relative_to(ROOT)}\n")
    for name in args.checkers:
        path = base / name
        if not path.is_file():
            print(f"  ✗ {name:<52} INTROUVABLE")
            failures.append(name)
            continue
        t0 = time.perf_counter()
        ok, detail = run_one(path)
        dt = (time.perf_counter() - t0) * 1000
        mark = "✓" if ok else "✗"
        print(f"  {mark} {name:<52} {dt:6.0f} ms")
        if not ok:
            failures.append(name)
            for line in detail.strip().splitlines()[-12:]:
                print(f"      │ {line}")

    total = len(args.checkers)
    passed = total - len(failures)
    print(f"\n{'─' * 60}")
    if failures:
        print(f"❌ {passed}/{total} OK — {len(failures)} en échec : {', '.join(failures)}")
        return 1
    print(f"✅ {passed}/{total} checkers conformes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
