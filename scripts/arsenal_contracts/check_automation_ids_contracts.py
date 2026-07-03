#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : IDs d'automatisations (AID)

Doctrine (NORMATIVE, opposable) :
  00_documentation_arsenal/architecture/03_doctrines/id_automatisations.md
Structure d'include :
  00_documentation_arsenal/architecture/00_structure_includes/11_automations.md

Garde-fou opposable des invariants d'IDs. Périmètre : 11_automations/.
Source de vérité des préfixes : 06_input_selects/system/prefix_id.yaml
(JAMAIS déduit d'un dossier ou d'un contenu — cf. doctrine §Gouvernance).

Règles :
  AID-001  Toute automation possède un `id` explicite (ERROR).
  AID-002  `id` est une CHAÎNE — un entier non quoté est interdit (ERROR).
           Motif : Home Assistant impose `str`; un entier désactive l'automation.
  AID-003  `id` numérique = préfixe(4 chiffres) + suffixe(10 chiffres), longueur
           EXACTE 14 (gabarit canonique de generate_next_id_from_prefix) (ERROR).
  AID-004  Le préfixe (4 premiers chiffres) est déclaré dans
           input_select.prefix_id_select (ERROR).
  AID-005  Unicité globale des `id` — aucun ID réutilisé (ERROR).

  AID-006 (retiré) : la tolérance legacy 13 chiffres (INFO) a été supprimée après la
  migration du 2026-07-03 (cf. audits/01_rapports/transverses/
  migration_ids_automatisations_13_vers_14.md). La longueur canonique 14 est
  désormais imposée strictement par AID-003.

Logique Arsenal habituelle : ERROR => exit 1.
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
AUTO_DIR = ROOT / "11_automations"
PREFIX_FILE = ROOT / "06_input_selects" / "system" / "prefix_id.yaml"

PREFIX_LEN = 4
CANONICAL_LEN = 14  # préfixe(4) + suffixe(10) — gabarit du générateur d'ID
FORMAT_RE = re.compile(r"^\d{14}$")  # longueur canonique stricte (durci post-migration AID-006)

ERRORS: list[str] = []
INVENTORY: list[dict] = []


# ---------------------------------------------------------------------------
# Chargement YAML tolérant aux tags HA (!secret, !include, ...)
# ---------------------------------------------------------------------------

class _Loader(yaml.SafeLoader):
    pass


# Les tags HA n'ont aucune incidence sur les `id` : on les neutralise.
_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8", errors="ignore"), Loader=_Loader)


def declared_prefixes() -> dict[str, str]:
    """Préfixe (4 chiffres) -> nom de domaine, depuis prefix_id_select."""
    data = load_yaml(PREFIX_FILE) or {}
    options = ((data.get("prefix_id_select") or {}).get("options")) or []
    out: dict[str, str] = {}
    for opt in options:
        m = re.match(r"\s*(\d{4})\s*-\s*(.+?)\s*$", str(opt))
        if m:
            out[m.group(1)] = m.group(2)
    return out


def find_line(text: str, id_value: str) -> int | None:
    """Meilleure estimation de la ligne portant l'`id` (affichage humain)."""
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(rf"\bid\s*:\s*['\"]?{re.escape(id_value)}\b", line):
            return i
    return None


def item_label(item: dict) -> str:
    alias = item.get("alias")
    return str(alias) if alias else "<sans alias>"


# ---------------------------------------------------------------------------
# Scan du périmètre
# ---------------------------------------------------------------------------

def scan(prefixes: dict[str, str]) -> None:
    seen: dict[str, list[str]] = defaultdict(list)

    for path in sorted(AUTO_DIR.rglob("*.yaml")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")

        try:
            data = load_yaml(path)
        except yaml.YAMLError as exc:
            ERRORS.append(f"AID-000 — YAML illisible : {rel} ({exc})")
            continue

        if data is None:
            continue
        if not isinstance(data, list):
            ERRORS.append(
                f"AID-000 — {rel} : la racine doit être une LISTE d'automations "
                f"(include_dir_merge_list), trouvé {type(data).__name__}"
            )
            continue

        for item in data:
            if not isinstance(item, dict):
                ERRORS.append(f"AID-000 — {rel} : item de liste non-mapping ({item!r})")
                continue

            label = item_label(item)

            # AID-001 — présence
            if "id" not in item or item.get("id") is None:
                ERRORS.append(f"AID-001 — automation sans `id` : {label} ({rel})")
                INVENTORY.append({"rel": rel, "id": None, "sev": "ERROR"})
                continue

            raw = item["id"]

            # AID-002 — type chaîne
            if not isinstance(raw, str):
                ERRORS.append(
                    f"AID-002 — `id` non quoté ({type(raw).__name__} {raw}) — "
                    f"Home Assistant exige une chaîne, sinon l'automation est "
                    f"désactivée : {label} ({rel})"
                )
                INVENTORY.append({"rel": rel, "id": str(raw), "sev": "ERROR"})
                continue

            aid = raw.strip()
            line = find_line(text, aid)
            loc = f"{rel}:{line}" if line else rel

            # AID-003 — format
            if not FORMAT_RE.match(aid):
                ERRORS.append(
                    f"AID-003 — `id` de format invalide (attendu 14 chiffres : préfixe 4 + suffixe 10) : "
                    f"« {aid} » — {label} ({loc})"
                )
                INVENTORY.append({"rel": rel, "id": aid, "sev": "ERROR"})
                continue

            prefix = aid[:PREFIX_LEN]

            # AID-004 — préfixe déclaré
            if prefix not in prefixes:
                ERRORS.append(
                    f"AID-004 — préfixe « {prefix} » non déclaré dans "
                    f"input_select.prefix_id_select : « {aid} » — {label} ({loc})"
                )

            seen[aid].append(loc)
            INVENTORY.append({
                "rel": rel,
                "id": aid,
                "prefix": prefix,
                "domain": prefixes.get(prefix, "?"),
                "sev": "OK",
            })

    # AID-005 — unicité
    for aid, locs in sorted(seen.items()):
        if len(locs) > 1:
            ERRORS.append(
                f"AID-005 — id dupliqué « {aid} » sur {len(locs)} automations : "
                + ", ".join(locs)
            )


# ---------------------------------------------------------------------------
# Sortie
# ---------------------------------------------------------------------------

def print_summary(prefixes: dict[str, str]) -> None:
    ok = [o for o in INVENTORY if o["sev"] == "OK"]
    by_len = defaultdict(int)
    for o in ok:
        by_len[len(o["id"])] += 1
    print(
        f"Périmètre : {len(INVENTORY)} automation(s) dans "
        f"{AUTO_DIR.name}/ — {len(prefixes)} préfixe(s) déclaré(s).\n"
    )
    print("Longueurs d'id (conformes) :")
    for length in sorted(by_len):
        print(f"  • {length} chiffres : {by_len[length]}")
    print()


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("Arsenal — Contrat IDs d'automatisations (AID) — garde-fou de conformité\n")

    prefixes = declared_prefixes()
    if not prefixes:
        print(f"❌ Aucun préfixe déclaré lisible dans {PREFIX_FILE.relative_to(ROOT).as_posix()}")
        sys.exit(1)

    scan(prefixes)
    print_summary(prefixes)

    print(f"Synthèse : {len(ERRORS)} ERROR.")

    if ERRORS:
        print("\n❌ CONTRAT IDs AUTOMATISATIONS NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)

    print("\n✅ CONTRAT IDs AUTOMATISATIONS CONFORME")
