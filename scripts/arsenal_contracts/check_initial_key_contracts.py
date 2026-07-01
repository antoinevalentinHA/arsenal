#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : clé `initial` dans les helpers HA (HINIT)
Contrat : architecture/03_doctrines/restauration_etat_helpers.md (v1.0, opposable)
Audit source : audits/01_rapports/transverses/audit_initial_helpers.md (#198)

CI de conformité active (durcissement Phase 4) : garde-fou opposable.
Logique Arsenal habituelle : ERROR => exit 1 ; WARN => exit 0 ; INFO => exit 0.

La source de vérité des exceptions est le marqueur IN-FILE `# initial VOULU — <cat>`,
JAMAIS la prose des en-têtes `NATURE`. Aucun système d'exceptions externe.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ERRORS: list[str] = []
WARNINGS: list[str] = []
INFOS: list[str] = []
INVENTORY: list[dict] = []


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ---------------------------------------------------------------------------
# Périmètre et vocabulaire contractuel
# ---------------------------------------------------------------------------

# Dossier helper -> type de helper
HELPER_DIRS = {
    "03_input_numbers": "input_number",
    "04_input_texts": "input_text",
    "05_input_booleans": "input_boolean",
    "06_input_selects": "input_select",
    "07_input_datetimes": "input_datetime",
    "09_counters": "counter",
}

# Fichiers config-seed reconnus : exception valide UNIQUEMENT via marqueur
# in-file `initial VOULU — config-seed`.
CONFIG_SEED_FILES = {
    "04_input_texts/alarme/badges.yaml",
    "04_input_texts/alarme/code.yaml",
}

# Vocabulaire clos des catégories du marqueur `initial VOULU`.
# Union du contrat (§Format : `booleen-technique-reset`) et de la matrice CI
# du lot (`technique-reset`) : les deux formes sont acceptées.
VALID_CATEGORIES = {
    "sentinelle-cold-start",
    "transactionnel",
    "sentinelle-jamais",
    "compteur",
    "config-seed",
    "technique-reset",
    "booleen-technique-reset",
}
# Catégorie explicitement refusée : un paramètre réglable n'est pas justifiable.
FORBIDDEN_CATEGORY = "parametre-reglable"


KEY_RE = re.compile(r"^([A-Za-z_][\w]*)\s*:\s*(?:#.*)?$")
INITIAL_RE = re.compile(r"^\s+initial\s*:\s*(.*)$")
RESTORE_RE = re.compile(r"^\s+restore\s*:")
MARKER_RE = re.compile(r"#\s*initial VOULU\s*[—–-]?\s*([A-Za-z][\w-]*)?")


def helper_type_of(rel: str) -> str | None:
    top = rel.split("/", 1)[0]
    return HELPER_DIRS.get(top)


def clean_value(raw: str) -> str:
    raw = raw.strip()
    if raw[:1] in ("\"", "'"):
        q = raw[0]
        end = raw.find(q, 1)
        if end != -1:
            return raw[: end + 1]
        return raw
    if "#" in raw:
        raw = raw.split("#", 1)[0].strip()
    return raw


def parse_blocks(content: str) -> list[dict]:
    """
    Segmente un fichier helper en blocs d'entité (clé de mapping à l'indent 0).
    Chaque bloc : {key, line (1-based de la clé), header (commentaires au-dessus),
    body (lignes jusqu'à la clé suivante)}.
    """
    lines = content.splitlines()
    key_idx = [
        i for i, l in enumerate(lines)
        if KEY_RE.match(l) and (not l[:1].isspace())
    ]
    blocks = []
    for n, start in enumerate(key_idx):
        end = key_idx[n + 1] if n + 1 < len(key_idx) else len(lines)
        key = KEY_RE.match(lines[start]).group(1)
        header = []
        j = start - 1
        while j >= 0 and (lines[j].strip().startswith("#") or not lines[j].strip()):
            header.append(lines[j])
            j -= 1
        header.reverse()
        blocks.append({
            "key": key,
            "line": start + 1,
            "header": header,
            "body": lines[start:end],
        })
    return blocks


# ---------------------------------------------------------------------------
# Scan : inventaire des occurrences `initial:`
# ---------------------------------------------------------------------------

def scan() -> None:
    for top in HELPER_DIRS:
        for path in yaml_files(ROOT / top):
            rel = path.relative_to(ROOT).as_posix()
            htype = helper_type_of(rel)
            content = read(path)
            for block in parse_blocks(content):
                initial_val = None
                initial_line = None
                for offset, line in enumerate(block["body"]):
                    m = INITIAL_RE.match(line)
                    if m:
                        initial_val = clean_value(m.group(1))
                        initial_line = block["line"] + offset
                        break
                if initial_val is None:
                    continue

                text = "\n".join(block["header"] + block["body"])
                mk = MARKER_RE.search(text)
                marker_present = mk is not None
                category = mk.group(1) if (mk and mk.group(1)) else None
                restore_explicit = any(
                    RESTORE_RE.match(l) for l in block["body"]
                )

                INVENTORY.append({
                    "rel": rel,
                    "line": initial_line,
                    "htype": htype,
                    "key": block["key"],
                    "value": initial_val,
                    "marker": marker_present,
                    "category": category,
                    "restore_explicit": restore_explicit,
                })


# ---------------------------------------------------------------------------
# Classification : une occurrence -> une règle -> une sévérité
# ---------------------------------------------------------------------------

def classify() -> None:
    for occ in INVENTORY:
        rel = occ["rel"]
        key = occ["key"]
        htype = occ["htype"]

        # HINIT-006 — config-seed alarme : résolu (INFO) si marqueur `config-seed`
        # valide, sinon INTERDIT (ERROR). La valeur n'est jamais imprimée
        # (badges = jetons d'accès, code = secret).
        if rel in CONFIG_SEED_FILES:
            occ["rule"] = "HINIT-006"
            if occ["marker"] and occ["category"] == "config-seed":
                occ["sev"] = "INFO"
                INFOS.append(
                    f"HINIT-006 — config-seed justifié par marqueur « config-seed » : "
                    f"{key} ({rel}:{occ['line']})"
                )
            elif occ["marker"] and occ["category"] in VALID_CATEGORIES:
                occ["sev"] = "ERROR"
                ERRORS.append(
                    f"HINIT-006 — marqueur `initial VOULU` de catégorie "
                    f"« {occ['category']} » inadaptée à un config-seed : "
                    f"{key} ({rel}:{occ['line']})"
                )
            else:
                occ["sev"] = "ERROR"
                ERRORS.append(
                    f"HINIT-006 — config-seed sans marqueur `config-seed` valide "
                    f"(marqueur obligatoire) : {key} ({rel}:{occ['line']})"
                )
            continue

        # HINIT-004 — counter : régime distinct (INFO), WARN si restore implicite.
        if htype == "counter":
            occ["rule"] = "HINIT-004"
            if occ["restore_explicit"]:
                occ["sev"] = "INFO"
                INFOS.append(
                    f"HINIT-004 — counter avec initial (restore explicite) : "
                    f"{key} = {occ['value']} ({rel}:{occ['line']})"
                )
            else:
                occ["sev"] = "WARN"
                WARNINGS.append(
                    f"HINIT-004 — counter avec initial mais `restore:` IMPLICITE "
                    f"(R05 exige restore explicite) : {key} ({rel}:{occ['line']})"
                )
            continue

        # HINIT-002 — input_boolean : interdiction dure (ERROR immédiat).
        if htype == "input_boolean":
            occ["rule"], occ["sev"] = "HINIT-002", "ERROR"
            ERRORS.append(
                f"HINIT-002 — initial INTERDIT sur input_boolean : "
                f"{key} = {occ['value']} ({rel}:{occ['line']})"
            )
            continue

        # input_number / input_text / input_datetime / input_select
        if occ["marker"]:
            cat = occ["category"]
            if cat == FORBIDDEN_CATEGORY or cat not in VALID_CATEGORIES:
                occ["rule"], occ["sev"] = "HINIT-003", "ERROR"
                ERRORS.append(
                    f"HINIT-003 — marqueur `initial VOULU` invalide "
                    f"(catégorie « {cat} » hors vocabulaire clos) : "
                    f"{key} ({rel}:{occ['line']})"
                )
            else:
                # Marqueur valide : initial justifié (traçabilité assurée).
                occ["rule"], occ["sev"] = "HINIT-003", "OK"
                INFOS.append(
                    f"HINIT-003 — initial justifié par marqueur « {cat} » : "
                    f"{key} ({rel}:{occ['line']})"
                )
            continue

        # Pas de marqueur -> HINIT-001.
        occ["rule"], occ["sev"] = "HINIT-001", "ERROR"
        ERRORS.append(
            f"HINIT-001 — initial INTERDIT sans justification contractuelle "
            f"(marqueur `initial VOULU` absent) : {key} = {occ['value']} "
            f"({rel}:{occ['line']})"
        )


# ---------------------------------------------------------------------------
# Sortie
# ---------------------------------------------------------------------------

def print_inventory() -> None:
    print("Inventaire des occurrences `initial:` (périmètre helpers)\n")
    header = f"  {'type':<15} {'entité/clé':<52} {'valeur':<26} {'marqueur':<10} sévérité"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for occ in sorted(INVENTORY, key=lambda o: (o["htype"] or "", o["rel"], o["line"])):
        marker = occ["category"] if occ["marker"] else "absent"
        if occ["rel"] in CONFIG_SEED_FILES:
            # Valeur sensible (jetons de badges / secret) — jamais imprimée en clair.
            val = "<config-seed masqué>"
        else:
            val = occ["value"] if len(occ["value"]) <= 24 else occ["value"][:23] + "…"
        key = occ["key"] if len(occ["key"]) <= 50 else occ["key"][:49] + "…"
        print(
            f"  {occ['htype']:<15} {key:<52} {val:<26} "
            f"{marker:<10} {occ.get('sev', '?')}"
        )
    print()


def print_rule_summary() -> None:
    def count(rule, sev=None):
        return sum(
            1 for o in INVENTORY
            if o.get("rule") == rule and (sev is None or o.get("sev") == sev)
        )

    print("Résultats par règle :\n")
    n001 = count("HINIT-001")
    print(f"  {'❌' if n001 else '✔'} HINIT-001 — input_* sans marqueur `initial VOULU` : {n001} ERROR")
    n002 = count("HINIT-002")
    print(f"  {'❌' if n002 else '✔'} HINIT-002 — initial sur input_boolean : "
          f"{'AUCUN (OK)' if not n002 else str(n002) + ' ERROR'}")
    n003e = count("HINIT-003", "ERROR")
    n003ok = count("HINIT-003", "OK")
    print(f"  {'❌' if n003e else '✔'} HINIT-003 — marqueur invalide : {n003e} ERROR "
          f"({n003ok} marqueur(s) valide(s))")
    n004i = count("HINIT-004", "INFO")
    n004w = count("HINIT-004", "WARN")
    print(f"  {'△' if n004w else '•'} HINIT-004 — counter : {n004i} INFO, {n004w} WARN (restore implicite)")
    n006e = count("HINIT-006", "ERROR")
    n006i = count("HINIT-006", "INFO")
    print(f"  {'❌' if n006e else ('•' if n006i else '✔')} HINIT-006 — config-seed alarme : {n006e} ERROR / {n006i} INFO")
    print()


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("Arsenal — Contrat clé `initial` (HINIT) — garde-fou de conformité\n")

    scan()
    classify()

    print_inventory()
    print_rule_summary()

    if INFOS:
        print("ℹ️  Informations :\n")
        for i in INFOS:
            print(f"  • {i}")
        print()

    if WARNINGS:
        print("⚠️  Avertissements (non bloquants) :\n")
        for w in WARNINGS:
            print(f"  △ {w}")
        print()

    total = len(INVENTORY)
    print(
        f"Synthèse : {total} occurrence(s) `initial` — "
        f"{len(ERRORS)} ERROR / {len(WARNINGS)} WARN / {len(INFOS)} INFO."
    )

    if ERRORS:
        print("\n❌ CONTRAT INITIAL NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT INITIAL CONFORME")
