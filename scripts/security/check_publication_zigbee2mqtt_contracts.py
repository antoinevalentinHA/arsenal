#!/usr/bin/env python3
# ==========================================================
# ARSENAL — CONTRAT : publication Zigbee2MQTT (incident P0)
# ----------------------------------------------------------
# Verrou de non-régression de l'incident « secrets Zigbee2MQTT publiés » :
# le scanner rendait PASS sur un mot de passe MQTT littéral et une
# network_key réelle parce que zigbee2mqtt/ était exclu du scan de contenu,
# et le workflow CI était non bloquant (continue-on-error).
#
# Ce fichier est dans EXCLUDED_PATHS du scanner (contrat § 3.3) : il
# contient par construction des motifs de secrets FACTICES dans ses
# fixtures. Aucune valeur réelle ne doit jamais y figurer.
#
# Contrôles :
#   Z1 (positif)  — l'exemple neutralisé versionné passe sans CRITICAL.
#   Z2 (négatif)  — un mqtt.password littéral déclenche CRITICAL S1.
#   Z3 (négatif)  — une network_key littérale (bloc YAML) déclenche CRITICAL S9.
#   Z4 (négatif)  — une network_key inline littérale déclenche CRITICAL S9.
#   Z5 (périmètre)— zigbee2mqtt/ n'est plus dans EXCLUDED_DIRS et le walker
#                   atteint réellement zigbee2mqtt/configuration.example.yaml.
#   Z6 (hygiène)  — la configuration réelle n'est pas suivie par Git et
#                   .gitignore l'exclut (ainsi que backups et secret.yaml).
#   Z7 (gate CI)  — le workflow d'audit publication est bloquant
#                   (pas de continue-on-error) et gate sur --fail-on critical.
# ==========================================================

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / "scripts" / "security" / "audit_publication_git.py"
EXAMPLE = ROOT / "zigbee2mqtt" / "configuration.example.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "security_publication_audit.yml"

FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str) -> None:
    status = "OK " if ok else "FAIL"
    print(f"[{status}] {label} — {detail}")
    if not ok:
        FAILURES.append(f"{label} — {detail}")


def load_scanner():
    spec = importlib.util.spec_from_file_location("audit_publication_git", SCANNER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # requis par @dataclass (résolution des annotations)
    spec.loader.exec_module(module)
    return module


def scan_findings(module, path: Path):
    findings: list = []
    module.scan_text_file(path, findings)
    return findings


def criticals(findings) -> list:
    return [f for f in findings if f.severity == "CRITICAL"]


def main() -> int:
    module = load_scanner()

    # ── Z1 — positif : l'exemple neutralisé versionné passe ────────────────
    if EXAMPLE.is_file():
        crits = criticals(scan_findings(module, EXAMPLE))
        check(
            "Z1", not crits,
            "l'exemple neutralisé ne doit produire aucun CRITICAL"
            + (f" (obtenu : {[(f.control, f.pattern) for f in crits]})" if crits else ""),
        )
    else:
        check("Z1", False, f"exemple neutralisé absent : {EXAMPLE}")

    # ── Fixtures négatives (valeurs FACTICES, jamais les valeurs réelles) ──
    with tempfile.TemporaryDirectory() as tmp:
        z2m_dir = Path(tmp) / "zigbee2mqtt"
        z2m_dir.mkdir()

        # Z2 — mot de passe MQTT littéral (la forme exacte de l'incident)
        fx_password = z2m_dir / "configuration.yaml"
        fx_password.write_text(
            "mqtt:\n"
            "  base_topic: zigbee2mqtt\n"
            "  server: mqtt://core-mosquitto:1883\n"
            "  user: addons\n"
            "  password: Fixture-Only-NotARealCredential-cabp8q77\n",
            encoding="utf-8",
        )
        findings = scan_findings(module, fx_password)
        hit = [f for f in criticals(findings) if f.control == "S1" and f.pattern == "password"]
        check("Z2", bool(hit), "un mqtt.password littéral doit déclencher CRITICAL S1")

        # Z3 — network_key littérale en bloc YAML (la forme exacte de l'incident)
        fx_block = z2m_dir / "configuration_block.yaml"
        fx_block.write_text(
            "advanced:\n"
            "  channel: 25\n"
            "  network_key:\n"
            + "".join(f"    - {n}\n" for n in range(16))
            + "  ext_pan_id:\n"
            + "".join(f"    - {n}\n" for n in range(8)),
            encoding="utf-8",
        )
        findings = scan_findings(module, fx_block)
        hit = [f for f in criticals(findings) if f.control == "S9"]
        check("Z3", len(hit) >= 2,
              "network_key et ext_pan_id en bloc littéral doivent déclencher CRITICAL S9")

        # Z4 — network_key inline littérale
        fx_inline = z2m_dir / "configuration_inline.yaml"
        fx_inline.write_text(
            "advanced:\n"
            "  network_key: [13, 37, 42, 99, 7, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]\n",
            encoding="utf-8",
        )
        findings = scan_findings(module, fx_inline)
        hit = [f for f in criticals(findings) if f.control == "S9"]
        check("Z4", bool(hit), "une network_key inline littérale doit déclencher CRITICAL S9")

        # Z4-bis — contre-épreuve : les formes neutralisées ne déclenchent rien
        fx_neutral = z2m_dir / "configuration_neutral.yaml"
        fx_neutral.write_text(
            "mqtt:\n"
            "  user: '!secret mqtt_user'\n"
            "  password: '!secret mqtt_password'\n"
            "advanced:\n"
            "  pan_id: GENERATE\n"
            "  ext_pan_id: GENERATE\n"
            "  network_key: GENERATE\n",
            encoding="utf-8",
        )
        crits = criticals(scan_findings(module, fx_neutral))
        check("Z4-bis", not crits,
              "les formes neutralisées ('!secret x', GENERATE) ne doivent produire aucun CRITICAL"
              + (f" (obtenu : {[(f.control, f.pattern) for f in crits]})" if crits else ""))

    # ── Z5 — périmètre : zigbee2mqtt/ est scanné ────────────────────────────
    check("Z5a", "zigbee2mqtt" not in module.EXCLUDED_DIRS,
          "zigbee2mqtt ne doit plus figurer dans EXCLUDED_DIRS")
    walked = {p for p in module.iter_repo_files()}
    check("Z5b", EXAMPLE in walked,
          "le walker du scanner doit atteindre zigbee2mqtt/configuration.example.yaml")

    # ── Z6 — hygiène Git : la configuration réelle n'est plus versionnée ───
    tracked = subprocess.run(
        ["git", "ls-files", "zigbee2mqtt/"],
        cwd=ROOT, text=True, stdout=subprocess.PIPE, check=False,
    ).stdout.splitlines()
    leaked = [
        t for t in tracked
        if Path(t).name in ("configuration.yaml", "secret.yaml")
        or Path(t).name.startswith("configuration_backup")
    ]
    check("Z6a", not leaked,
          "aucune configuration réelle/backup/secret Zigbee2MQTT suivie par Git"
          + (f" (suivi : {leaked})" if leaked else ""))
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    missing = [
        p for p in (
            "zigbee2mqtt/configuration.yaml",
            "zigbee2mqtt/configuration_backup*.yaml",
            "zigbee2mqtt/secret.yaml",
        ) if p not in gitignore
    ]
    check("Z6b", not missing,
          ".gitignore doit exclure la configuration réelle"
          + (f" (manquant : {missing})" if missing else ""))

    # ── Z7 — gate CI : le workflow d'audit est bloquant ─────────────────────
    if WORKFLOW.is_file():
        wf = WORKFLOW.read_text(encoding="utf-8")
        active_wf = "\n".join(
            line for line in wf.splitlines() if not line.lstrip().startswith("#")
        )
        check("Z7a", "continue-on-error" not in active_wf,
              "le job d'audit ne doit plus être en continue-on-error")
        check("Z7b", "--fail-on critical" in active_wf,
              "le scanner doit être invoqué avec --fail-on critical")
    else:
        check("Z7", False, f"workflow absent : {WORKFLOW}")

    if FAILURES:
        print(f"\n{len(FAILURES)} contrôle(s) en échec.")
        return 1
    print("\nTous les contrôles publication Zigbee2MQTT sont conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
