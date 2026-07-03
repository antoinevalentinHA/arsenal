#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : cohérence préfixe d'ID ↔ domaine (APD)

Contrat (NORMATIF, opposable) :
  00_documentation_arsenal/architecture/03_doctrines/prefixe_domaine_automatisations.md
Doctrine des IDs (forme, attribution) :
  00_documentation_arsenal/architecture/03_doctrines/id_automatisations.md

Périmètre : 11_automations/**/*.yaml.
Sources de vérité :
  - préfixes déclarés : 06_input_selects/system/prefix_id.yaml
    (input_select.prefix_id_select) ;
  - exceptions opposables : scripts/arsenal_contracts/prefix_domain_exceptions.yaml.

Modèle de résolution du domaine attendu (conforme au contrat — PAS de règle
naïve dossier = préfixe) :
  1. le dossier RACINE sous 11_automations/ crée une PRÉSOMPTION de domaine
     fonctionnel propriétaire (présomption simple, réfutable — jamais une
     preuve) ; les sous-dossiers n'ont aucune autorité ;
  2. la présomption n'est levée QUE par une entrée valide du registre
     d'exceptions (id + fichier concordants) — le registre est opposable :
     explicite, justifié cas par cas, versionné ;
  3. verdict : le domaine d'identité (déclaré par le préfixe de l'ID) doit
     égaler le domaine présumé, sauf exception opposable valide ;
  4. le registre est lui-même contrôlé (existence des fichiers, concordance
     des IDs, préfixes déclarés, absence d'exception périmée ou dupliquée).

Règles :
  APD-000  YAML illisible ou structure racine invalide (ERROR).
  APD-001  Préfixe d'ID non déclaré dans prefix_id_select (ERROR) —
           garde redondante d'AID-004 (référence croisée assumée).
  APD-002  Préfixe incohérent avec le domaine présumé (dossier racine),
           sans exception opposable au registre (ERROR).
  APD-003  Domaine attendu non résolu : dossier racine inconnu des domaines
           déclarés, sans exception opposable (ERROR).
  APD-010  Exception référençant un fichier inexistant (ERROR).
  APD-011  Exception dont l'ID ne correspond à aucune automation réelle du
           fichier référencé (ERROR).
  APD-012  Exception incohérente : champ `prefixe` ≠ 4 premiers chiffres de
           l'ID, préfixe non déclaré, ou `domaine_prefixe` ≠ domaine déclaré
           du préfixe (ERROR).
  APD-013  Exception périmée : plus aucune divergence à couvrir (le préfixe
           égale déjà le domaine présumé) — à supprimer (ERROR).
           Le registre est strictement limité aux vraies exceptions : une
           clarification résolue vit dans l'en-tête du fichier, pas ici.
  APD-014  Exception dupliquée : même ID inscrit plusieurs fois (ERROR).

Hors périmètre (juridiction AID, pas de double signalement) :
  absence d'`id`, `id` non-chaîne, format ≠ 14 chiffres, unicité globale.

Aucun faux positif connu sur le corpus aligné : exit 0 attendu sur main.
Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python scripts/arsenal_contracts/check_automation_prefix_domain_contracts.py
  Options (tests uniquement — les défauts sont les chemins du dépôt) :
    --automations-dir DIR  --prefix-file FILE  --exceptions-file FILE
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUTO_DIR = ROOT / "11_automations"
DEFAULT_PREFIX_FILE = ROOT / "06_input_selects" / "system" / "prefix_id.yaml"
DEFAULT_EXCEPTIONS_FILE = Path(__file__).resolve().parent / "prefix_domain_exceptions.yaml"

PREFIX_LEN = 4
CANONICAL_RE = re.compile(r"^\d{14}$")  # juridiction AID-003 ; ici simple filtre

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Chargement YAML tolérant aux tags HA (!secret, !include, ...)
# ---------------------------------------------------------------------------

class _Loader(yaml.SafeLoader):
    pass


# Les tags HA n'ont aucune incidence sur les `id` : on les neutralise.
_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8", errors="ignore"), Loader=_Loader)


def declared_prefixes(prefix_file: Path) -> dict[str, str]:
    """Préfixe (4 chiffres) -> nom de domaine, depuis prefix_id_select."""
    data = load_yaml(prefix_file) or {}
    options = ((data.get("prefix_id_select") or {}).get("options")) or []
    out: dict[str, str] = {}
    for opt in options:
        m = re.match(r"\s*(\d{4})\s*-\s*(.+?)\s*$", str(opt))
        if m:
            out[m.group(1)] = m.group(2)
    return out


def load_exceptions(exceptions_file: Path) -> list[dict]:
    """Entrées du registre opposable (liste vide si le fichier est absent :
    l'absence de registre n'est pas une erreur, l'absence d'exception non plus)."""
    if not exceptions_file.is_file():
        return []
    data = load_yaml(exceptions_file) or {}
    entries = data.get("prefix_domain_exceptions") or []
    return [e for e in entries if isinstance(e, dict)]


# ---------------------------------------------------------------------------
# Inventaire du corpus
# ---------------------------------------------------------------------------

def scan_corpus(auto_dir: Path, root: Path) -> list[dict]:
    """Inventaire : une entrée par automation portant un `id` canonique.
    Les manquements de forme (id absent, non-chaîne, format) relèvent d'AID."""
    corpus: list[dict] = []
    for path in sorted(auto_dir.rglob("*.yaml")):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.as_posix()
        folder = path.relative_to(auto_dir).parts[0] if path.relative_to(auto_dir).parts[:-1] else "<racine>"

        try:
            data = load_yaml(path)
        except yaml.YAMLError as exc:
            ERRORS.append(f"APD-000 — YAML illisible : {rel} ({exc})")
            continue

        if data is None:
            continue
        if not isinstance(data, list):
            ERRORS.append(
                f"APD-000 — {rel} : la racine doit être une LISTE d'automations "
                f"(include_dir_merge_list), trouvé {type(data).__name__}"
            )
            continue

        for item in data:
            if not isinstance(item, dict):
                continue  # APD-000 fin : AID-000 signale déjà ce cas
            raw = item.get("id")
            if not isinstance(raw, str) or not CANONICAL_RE.match(raw.strip()):
                continue  # juridiction AID-001/002/003
            aid = raw.strip()
            corpus.append({
                "rel": rel,
                "folder": folder,
                "alias": str(item.get("alias") or "<sans alias>"),
                "id": aid,
                "prefix": aid[:PREFIX_LEN],
            })
    return corpus


# ---------------------------------------------------------------------------
# Contrôle du registre d'exceptions (APD-010..014)
# ---------------------------------------------------------------------------

def check_exceptions(entries: list[dict], corpus: list[dict],
                     prefixes: dict[str, str], root: Path) -> dict[str, dict]:
    """Valide le registre et retourne les exceptions APPLICABLES par ID."""
    domains = set(prefixes.values())
    by_file_ids: dict[str, set[str]] = defaultdict(set)
    by_id: dict[str, dict] = {}
    for row in corpus:
        by_file_ids[row["rel"]].add(row["id"])
        by_id[row["id"]] = row

    seen_ids: set[str] = set()
    applicable: dict[str, dict] = {}

    for entry in entries:
        eid = str(entry.get("id") or "").strip()
        efile = str(entry.get("fichier") or "").strip()
        eprefix = str(entry.get("prefixe") or "").strip()
        edomain = str(entry.get("domaine_prefixe") or "").strip()
        label = f"id « {eid} », fichier {efile or '<absent>'}"

        # APD-014 — doublon
        if eid in seen_ids:
            ERRORS.append(f"APD-014 — exception dupliquée au registre : {label}")
            continue
        seen_ids.add(eid)

        # APD-010 — fichier inexistant
        if not efile or not (root / efile).is_file():
            ERRORS.append(f"APD-010 — exception vers un fichier inexistant : {label}")
            continue

        # APD-011 — ID absent du fichier référencé
        if eid not in by_file_ids.get(efile, set()):
            ERRORS.append(
                f"APD-011 — exception dont l'ID ne correspond à aucune automation "
                f"réelle du fichier référencé : {label}"
            )
            continue

        # APD-012 — cohérence interne de l'entrée
        if eprefix != eid[:PREFIX_LEN]:
            ERRORS.append(
                f"APD-012 — exception incohérente : champ prefixe « {eprefix} » ≠ "
                f"préfixe réel « {eid[:PREFIX_LEN]} » : {label}"
            )
            continue
        if eprefix not in prefixes:
            ERRORS.append(
                f"APD-012 — exception vers un préfixe non déclaré dans "
                f"prefix_id_select : « {eprefix} » : {label}"
            )
            continue
        if edomain != prefixes[eprefix]:
            ERRORS.append(
                f"APD-012 — exception incohérente : domaine_prefixe « {edomain} » ≠ "
                f"domaine déclaré « {prefixes[eprefix]} » du préfixe {eprefix} : {label}"
            )
            continue
        if edomain not in domains:
            ERRORS.append(
                f"APD-012 — exception vers un domaine inconnu : « {edomain} » : {label}"
            )
            continue

        # APD-013 — exception périmée (plus de divergence à couvrir)
        row = by_id[eid]
        if prefixes.get(row["prefix"]) == row["folder"]:
            ERRORS.append(
                f"APD-013 — exception périmée (préfixe « {row['prefix']} » = domaine "
                f"présumé « {row['folder']} », aucune divergence à couvrir) — à "
                f"supprimer du registre : {label}"
            )
            continue

        applicable[eid] = entry

    return applicable


# ---------------------------------------------------------------------------
# Contrôle du corpus (APD-001..003)
# ---------------------------------------------------------------------------

def check_corpus(corpus: list[dict], prefixes: dict[str, str],
                 exceptions: dict[str, dict]) -> dict[str, int]:
    domains = set(prefixes.values())
    stats = {"presumption": 0, "exception": 0}

    for row in corpus:
        rel, folder, alias, aid, prefix = (
            row["rel"], row["folder"], row["alias"], row["id"], row["prefix"],
        )
        id_domain = prefixes.get(prefix)

        # APD-001 — préfixe non déclaré (garde redondante d'AID-004)
        if id_domain is None:
            ERRORS.append(
                f"APD-001 — préfixe « {prefix} » non déclaré dans "
                f"prefix_id_select : {alias} — id {aid} ({rel})"
            )
            continue

        exc = exceptions.get(aid)

        # APD-003 — dossier racine sans domaine résolu
        if folder not in domains:
            if exc is not None:
                stats["exception"] += 1
                continue
            ERRORS.append(
                f"APD-003 — domaine attendu non résolu : le dossier racine "
                f"« {folder} » n'est pas un domaine déclaré et aucune exception "
                f"opposable ne couvre l'automation : {alias} — id {aid}, "
                f"préfixe {prefix} ({id_domain}) ({rel})"
            )
            continue

        # Cas nominal — présomption satisfaite
        if id_domain == folder:
            stats["presumption"] += 1
            continue

        # Divergence — seule une exception opposable la couvre
        if exc is not None:
            stats["exception"] += 1
            continue

        ERRORS.append(
            f"APD-002 — préfixe incohérent avec le domaine présumé, sans "
            f"exception opposable : {alias} — id {aid}, préfixe {prefix} "
            f"(domaine d'identité « {id_domain} »), domaine présumé "
            f"« {folder} » ({rel}). Corriger le préfixe (procédure "
            f"exceptionnelle) ou inscrire une exception justifiée au registre "
            f"prefix_domain_exceptions.yaml (décision propriétaire requise)."
        )

    return stats


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--automations-dir", type=Path, default=DEFAULT_AUTO_DIR)
    parser.add_argument("--prefix-file", type=Path, default=DEFAULT_PREFIX_FILE)
    parser.add_argument("--exceptions-file", type=Path, default=DEFAULT_EXCEPTIONS_FILE)
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("Arsenal — Contrat préfixe d'ID ↔ domaine fonctionnel (APD) — garde-fou de conformité\n")

    root = args.automations_dir.resolve().parent

    prefixes = declared_prefixes(args.prefix_file)
    if not prefixes:
        print(f"❌ Aucun préfixe déclaré lisible dans {args.prefix_file}")
        return 1

    corpus = scan_corpus(args.automations_dir, root)
    entries = load_exceptions(args.exceptions_file)
    applicable = check_exceptions(entries, corpus, prefixes, root)
    stats = check_corpus(corpus, prefixes, applicable)

    print(
        f"Périmètre : {len(corpus)} automation(s), {len(prefixes)} préfixe(s) "
        f"déclaré(s), {len(entries)} exception(s) au registre "
        f"({len(applicable)} applicable(s)).\n"
        f"  • conformes par présomption (dossier racine) : {stats['presumption']}\n"
        f"  • couvertes par exception opposable          : {stats['exception']}\n"
    )

    print(f"Synthèse : {len(ERRORS)} ERROR.")

    if ERRORS:
        print("\n❌ CONTRAT PRÉFIXE/DOMAINE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        return 1

    print("\n✅ CONTRAT PRÉFIXE/DOMAINE CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
