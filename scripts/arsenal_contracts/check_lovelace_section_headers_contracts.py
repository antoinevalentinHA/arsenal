#!/usr/bin/env python3

"""R-LL-HEADER-EMOJI-1 — Tout « section header » Lovelace porte un emoji visible.

Contrat  : R-LL-HEADER-EMOJI-1
Slug     : lovelace_section_headers
Doctrine : 00_documentation_arsenal/ui/socle_ui/11_header.md
           00_documentation_arsenal/ui/pattern_dashboard.md

Pourquoi ce checker
-------------------
La doctrine UI Arsenal structure les dashboards par des en-têtes (« headers »)
non interactifs hérités de `socle_header_base` : `section_header` (titre de
section) et `sub_section_header` (sous-section). Le pattern canonique
(`pattern_dashboard.md`) et 100 % du runtime préfixent le `name` de ces en-têtes
par un emoji (ex. `🌡️ Calibration Zigbee`). Cet emoji n'est pas décoratif : il
porte le repère visuel de section. Ce checker rend cette règle **opposable**.

Définition retenue de « section header »
----------------------------------------
Toute carte `custom:button-card` dont la clé `template` vaut `section_header`
OU `sub_section_header`. Les deux héritent du même socle (`socle_header_base`)
et sont décrits par `11_header.md` comme « titres de sections et sous-sections ».
Ne sont PAS visés : les titres Markdown documentaires, les `name:` de cartes
métier (état/action/kpi…), les libellés d'entités.

Périmètre scanné
----------------
`18_lovelace/**/*.yaml` — lieu d'INSTANCIATION des en-têtes (dashboards ET
includes `section_headers/` / `sub_section_headers/`). Le dossier
`19_button_card_templates/` n'est PAS scanné : il DÉFINIT les templates, il ne
les instancie pas avec un `name`.

Méthode
-------
Chaque fichier YAML source est chargé UNE fois. Les tags Home Assistant sont
neutralisés : `!include` n'est PAS suivi (chaque fichier inclus est lui-même un
fichier source scanné à part — pas de double comptage), `!include_dir_*` -> {}/[],
`!secret` -> sentinelle. Le `name` d'un en-tête est toujours co-localisé avec son
`template` dans la même carte ; aucune résolution d'include n'est nécessaire.

Règle contrôlée
---------------
  ERROR — un en-tête dont le `name` est absent, vide, non-textuel, ou ne contient
          AUCUN emoji visible.

Détection d'emoji : plages Unicode usuelles (pictogrammes, symboles, dingbats,
flèches, sélecteurs de variante, supplément alphanumérique encadré p. ex. 🆔…).
Implémentation `re` pure — aucune dépendance lourde. Les lettres accentuées
françaises (é, è, à, ç…) ne sont jamais comptées comme emoji.

Sortie / codes
--------------
  - exit 0 : conforme.
  - exit 1 : au moins un en-tête sans emoji.
  - exit 2 : erreur d'usage/infra (PyYAML absent) ou auto-test en échec.

Lecture seule, déterministe. Dépend de PyYAML (comme les autres checkers
Lovelace).
"""

from __future__ import annotations

import re
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

HEADER_TEMPLATES = {"section_header", "sub_section_header"}

# ==========================================================
# Détection d'emoji (re pur, sans dépendance)
# ==========================================================

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # pictogrammes & symboles étendus
    "\U00002600-\U000027BF"  # symboles divers + dingbats (❄ ⚖ …)
    "\U0001F000-\U0001F0FF"  # mahjong / dominos / cartes
    "\U0001F100-\U0001F1FF"  # supplément alphanumérique encadré (🆔 🆘 …) + indicateurs régionaux
    "\U00002B00-\U00002BFF"  # flèches / étoiles (⭐ …)
    "\U00002190-\U000021FF"  # flèches
    "\U00002300-\U000023FF"  # technique (⏱ ⏳ …)
    "\U0000FE00-\U0000FE0F"  # sélecteurs de variante
    "\U000024C2"             # Ⓜ
    "\U00002139"             # ℹ
    "]+",
    flags=re.UNICODE,
)


def has_emoji(value: str) -> bool:
    return bool(EMOJI_RE.search(value))


# ==========================================================
# Loader YAML : tags Home Assistant neutralisés (pas de suivi d'include)
# ==========================================================

def _make_loader():
    class _L(yaml.SafeLoader):
        pass

    def _construct_mapping(loader, node, deep=False):
        mapping = yaml.SafeLoader.construct_mapping(loader, node, deep=deep)
        # Ligne (1-indexée) du début de la carte, pour des messages exploitables.
        mapping["__line__"] = node.start_mark.line + 1
        return mapping

    _L.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
    )
    _L.add_constructor("!include", lambda l, n: None)
    _L.add_constructor("!include_dir_merge_named", lambda l, n: {})
    _L.add_constructor("!include_dir_named", lambda l, n: {})
    _L.add_constructor("!include_dir_list", lambda l, n: [])
    _L.add_constructor("!include_dir_merge_list", lambda l, n: [])
    _L.add_constructor("!secret", lambda l, n: "SECRET")
    return _L


_LOADER = _make_loader()


def load_yaml(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    return yaml.load(text, Loader=_LOADER)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Collecte des en-têtes
# ==========================================================

def collect_headers(node, acc):
    """Ajoute à `acc` tout mapping {template ∈ HEADER_TEMPLATES}."""
    if isinstance(node, dict):
        tmpl = node.get("template")
        if isinstance(tmpl, str) and tmpl in HEADER_TEMPLATES:
            acc.append(node)
        for key, value in node.items():
            if key == "__line__":
                continue
            collect_headers(value, acc)
    elif isinstance(node, list):
        for value in node:
            collect_headers(value, acc)


def analyze(lovelace_dir: Path):
    """Retourne (n_headers, n_files, errors[str])."""
    errors: list[str] = []
    n_headers = 0
    files = sorted(lovelace_dir.rglob("*.yaml"))

    for path in files:
        try:
            data = load_yaml(path)
        except Exception as exc:
            errors.append(f"{rel(path)} : YAML illisible — {exc}")
            continue

        headers: list[dict] = []
        collect_headers(data, headers)

        for node in headers:
            n_headers += 1
            tmpl = node.get("template")
            line = node.get("__line__", "?")
            name = node.get("name")

            if name is None:
                errors.append(
                    f"{rel(path)}:{line} : en-tête «{tmpl}» sans `name` "
                    f"— un emoji visible est requis (doctrine 11_header.md)"
                )
                continue

            if not isinstance(name, str):
                errors.append(
                    f"{rel(path)}:{line} : en-tête «{tmpl}» avec `name` non "
                    f"textuel ({type(name).__name__}) — emoji visible requis"
                )
                continue

            if not has_emoji(name):
                errors.append(
                    f"{rel(path)}:{line} : en-tête «{tmpl}» sans emoji "
                    f"— name={name!r} (préfixer d'un emoji visible, "
                    f"doctrine 11_header.md)"
                )

    return n_headers, len(files), errors


# ==========================================================
# Auto-test (garde-fou du détecteur d'emoji et du walker)
# ==========================================================

def selftest() -> list[str]:
    failures: list[str] = []

    # 1) Détecteur d'emoji : vrais positifs (dont 🆔) et garde accent FR.
    for ok in ("🌡️ Seuils", "❄️ Mode Cool", "🆔 ID", "⚖️ Critères", "ℹ️ Info"):
        if not has_emoji(ok):
            failures.append(f"auto-test : emoji non détecté dans {ok!r}")
    for ko in ("Seuils de déclenchement", "Offsets", "Présence", "Café crème"):
        if has_emoji(ko):
            failures.append(
                f"auto-test : faux positif emoji sur du texte FR {ko!r}"
            )

    # 2) Walker + règle sur une arborescence jouet (dashboard + include).
    with tempfile.TemporaryDirectory() as tmp:
        ll = Path(tmp) / "18_lovelace"
        (ll / "dashboards").mkdir(parents=True)
        (ll / "includes" / "section_headers").mkdir(parents=True)

        (ll / "dashboards" / "ok.yaml").write_text(
            "views:\n"
            "  - cards:\n"
            "      - type: custom:button-card\n"
            "        template: section_header\n"
            "        name: 🔌 Etat\n",
            encoding="utf-8",
        )
        (ll / "dashboards" / "ko.yaml").write_text(
            "views:\n"
            "  - cards:\n"
            "      - type: custom:button-card\n"
            "        template: sub_section_header\n"
            "        name: Seuils de déclenchement\n",
            encoding="utf-8",
        )
        # Include unitaire (mapping racine) conforme.
        (ll / "includes" / "section_headers" / "sejour.yaml").write_text(
            "type: custom:button-card\n"
            "template: section_header\n"
            "name: 🛋️ Séjour\n",
            encoding="utf-8",
        )
        # Un !include dans un dashboard ne doit PAS être suivi (pas de double compte).
        (ll / "dashboards" / "host.yaml").write_text(
            "views:\n"
            "  - cards:\n"
            "      - !include ../includes/section_headers/sejour.yaml\n",
            encoding="utf-8",
        )

        n_headers, _, errors = analyze(ll)

        # 3 en-têtes attendus : ok + ko + l'include (scanné une seule fois,
        # via host.yaml l'include est neutralisé donc non recompté).
        if n_headers != 3:
            failures.append(
                f"auto-test : comptage attendu 3, obtenu {n_headers} "
                f"(double comptage d'include ou walker cassé ?)"
            )
        if not any("ko.yaml" in e and "sans emoji" in e for e in errors):
            failures.append("auto-test : en-tête sans emoji non détecté")
        if any("ok.yaml" in e for e in errors):
            failures.append("auto-test : faux positif sur en-tête conforme")
        if any("sejour.yaml" in e for e in errors):
            failures.append("auto-test : faux positif sur include conforme")

    return failures


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    print("Arsenal — Validation contractuelle : Section headers Lovelace "
          "(R-LL-HEADER-EMOJI-1)")
    print("Règle : tout en-tête section_header / sub_section_header porte un "
          "emoji visible dans son `name`.\n")

    st_failures = selftest()
    if st_failures:
        print("❌ AUTO-TEST EN ÉCHEC")
        for f in st_failures:
            print(f"  - {f}")
        return 2
    print("✔ auto-test conforme (détecteur d'emoji + walker + non double comptage)")

    n_headers, n_files, errors = analyze(LOVELACE)

    if errors:
        print(f"\n❌ ERREURS ({len(errors)}) :")
        for e in errors:
            print(f"  - {e}")
    else:
        print("\n✔ Tous les en-têtes portent un emoji visible.")

    print("\n— Résumé —")
    print(f"  fichiers Lovelace scannés : {n_files}")
    print(f"  en-têtes analysés         : {n_headers}")
    print(f"  erreurs                   : {len(errors)}")

    if errors:
        print("\n❌ CONTRAT LOVELACE_SECTION_HEADERS NON CONFORME")
        return 1

    print("\n✅ CONTRAT LOVELACE_SECTION_HEADERS CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
