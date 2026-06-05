#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ARSENAL — Audit des références documentaires Markdown non cliquables.

V1 :
- Lecture seule.
- Aucun patch.
- Aucune correction automatique.
- Détection des références internes non cliquables.
- Classification : auto, ambiguous, dead, multi_target, ignored.

Usage :
  python scripts/docs_navigation/audit_doc_links.py --scope chauffage
  python scripts/docs_navigation/audit_doc_links.py --scope all
  python scripts/docs_navigation/audit_doc_links.py --path 00_documentation_arsenal/contrats/chauffage
"""

from __future__ import annotations

import argparse
import re
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DOC_ROOT_DEFAULT = "00_documentation_arsenal"

STATUS_AUTO = "auto"
STATUS_AMBIGUOUS = "ambiguous"
STATUS_DEAD = "dead"
STATUS_MULTI = "multi_target"
STATUS_IGNORED = "ignored"

CATEGORY_BACKTICK_MD = "backtick_md"
CATEGORY_RAW_MD = "raw_md"
CATEGORY_EXTENSIONLESS = "extensionless"
CATEGORY_ABSOLUTE_DOC = "absolute_doc_path"
CATEGORY_ABSOLUTE_HA = "absolute_homeassistant_path"
CATEGORY_BRACE_MULTI = "brace_multi"
CATEGORY_CODE_BLOCK = "code_block"
CATEGORY_TABLE = "table"


ENTITY_PREFIXES = (
    "sensor.",
    "binary_sensor.",
    "input_boolean.",
    "input_number.",
    "input_select.",
    "input_text.",
    "input_datetime.",
    "switch.",
    "climate.",
    "cover.",
    "button.",
    "script.",
    "automation.",
    "notify.",
    "zone.",
    "person.",
    "device_tracker.",
)


@dataclass(frozen=True)
class Candidate:
    source: Path
    line_no: int
    category: str
    status: str
    token: str
    target: str | None
    reason: str


def iter_markdown_files(root: Path) -> list[Path]:
    return sorted(
        p for p in root.rglob("*.md")
        if p.is_file()
    )


def is_external_url(token: str) -> bool:
    return token.startswith(("http://", "https://", "mailto:"))


def is_entity(token: str) -> bool:
    return token.startswith(ENTITY_PREFIXES)


def normalize_token(token: str) -> str:
    token = token.strip()
    token = token.strip("`")
    token = token.strip()
    token = token.rstrip(".,;:)")
    token = token.lstrip("(")
    return token


def is_markdown_link_line_fragment(line: str, start: int, end: int) -> bool:
    """
    Retourne True si le token est déjà dans un lien Markdown [texte](href).
    Heuristique suffisante pour éviter les doubles conversions.
    """
    before = line[:start]
    after = line[end:]

    last_open_bracket = before.rfind("[")
    last_close_bracket = before.rfind("]")

    if last_open_bracket > last_close_bracket and after.lstrip().startswith("]("):
        return True

    if before.endswith("]("):
        return True

    return False


def strip_fenced_code(lines: list[str]) -> list[tuple[int, str, bool]]:
    """
    Renvoie (line_no, line, in_fence).
    On garde les lignes, mais on marque les fenced blocks pour classement ignored.
    """
    result: list[tuple[int, str, bool]] = []
    in_fence = False

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("```"):
            result.append((idx, line, True))
            in_fence = not in_fence
            continue

        result.append((idx, line, in_fence))

    return result


def build_index(doc_root: Path) -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    """
    Index :
    - par chemin relatif POSIX complet
    - par basename
    - par stem
    """
    by_name: dict[str, list[Path]] = {}
    by_stem: dict[str, list[Path]] = {}

    for file in iter_markdown_files(doc_root):
        rel = file.relative_to(doc_root).as_posix()

        keys = {
            rel,
            file.name,
        }

        for key in keys:
            by_name.setdefault(key, []).append(file)

        by_stem.setdefault(file.stem, []).append(file)

    return by_name, by_stem


def resolve_token(
    token: str,
    source: Path,
    doc_root: Path,
    by_name: dict[str, list[Path]],
    by_stem: dict[str, list[Path]],
) -> tuple[str, str | None, str]:
    """
    Résout une référence documentaire.

    Retour :
      status, target_relative_to_doc_root, reason
    """
    raw = normalize_token(token)

    if " / " in raw:
        return STATUS_IGNORED, None, "slash_separated_concept"

    if "*" in raw:
        return STATUS_IGNORED, None, "wildcard"

    if raw.startswith("NN_"):
        return STATUS_IGNORED, None, "placeholder"

    if raw.endswith("/"):
        return STATUS_IGNORED, None, "directory_reference"

    suffix = Path(raw).suffix
    if suffix and suffix != ".md":
        return STATUS_IGNORED, None, "non_markdown_file"

    if not raw:
        return STATUS_IGNORED, None, "empty"

    if is_external_url(raw):
        return STATUS_IGNORED, None, "external_url"

    if is_entity(raw):
        return STATUS_IGNORED, None, "home_assistant_entity"

    if "{" in raw and "}" in raw and raw.endswith(".md"):
        return STATUS_MULTI, None, "brace_multi_target"

    candidates: list[Path] = []

    # Chemins absolus documentaires
    if raw.startswith("/homeassistant/"):
        marker = "00_documentation_arsenal/"
        if marker in raw:
            rel = raw.split(marker, 1)[1]
            candidates = [doc_root / rel]

    elif raw.startswith("/00_documentation_arsenal/"):
        rel = raw.removeprefix("/00_documentation_arsenal/")
        candidates = [doc_root / rel]

    elif raw.startswith("00_documentation_arsenal/"):
        rel = raw.removeprefix("00_documentation_arsenal/")
        candidates = [doc_root / rel]

    # Chemin relatif direct depuis le fichier source
    elif raw.endswith(".md"):
        direct = (source.parent / raw).resolve()
        if direct.exists():
            candidates = [direct]
        else:
            # Chemin depuis la racine doc
            root_relative = (doc_root / raw).resolve()
            if root_relative.exists():
                candidates = [root_relative]
            else:
                # Basename unique
                name = Path(raw).name
                candidates = by_name.get(name, [])

    elif "/" in raw:
        return STATUS_IGNORED, None, "non_markdown_path"

    # Référence sans extension
    else:
        stem = raw

        if "/" in stem:
            return STATUS_IGNORED, None, "extensionless_path_ignored"

        if " " in stem:
            return STATUS_IGNORED, None, "extensionless_with_space"

        candidates = by_stem.get(stem, [])

    existing = []
    for candidate in candidates:
        try:
            if candidate.exists() and candidate.is_file():
                existing.append(candidate.resolve())
        except OSError:
            pass

    unique_existing = sorted(set(existing))

    source_resolved = source.resolve()

    # Auto-référence
    unique_existing = [
        p for p in unique_existing
        if p != source_resolved
    ]

    if len(unique_existing) == 1:
        rel = unique_existing[0].relative_to(doc_root.resolve()).as_posix()
        return STATUS_AUTO, rel, "unique_target"

    if len(unique_existing) > 1:
        rels = [
            p.relative_to(doc_root.resolve()).as_posix()
            for p in unique_existing
        ]
        return STATUS_AMBIGUOUS, " | ".join(rels), "multiple_targets"

    return STATUS_DEAD, None, "target_not_found"


def detect_candidates_in_file(
    source: Path,
    doc_root: Path,
    by_name: dict[str, list[Path]],
    by_stem: dict[str, list[Path]],
) -> list[Candidate]:
    text = source.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    results: list[Candidate] = []

    # Backticks contenant .md ou stem potentiel
    backtick_pattern = re.compile(r"`([^`]+)`")

    # Chemins .md nus, incluant absolus.
    raw_md_pattern = re.compile(
        r"(?<![\]\(\w./-])"
        r"("
        r"(?:/homeassistant/00_documentation_arsenal/|/00_documentation_arsenal/|00_documentation_arsenal/)?"
        r"[\w./-]+\.md"
        r")"
    )

    for line_no, line, in_fence in strip_fenced_code(lines):
        stripped = line.strip()

        if in_fence:
            if ".md" in line:
                results.append(
                    Candidate(
                        source=source,
                        line_no=line_no,
                        category=CATEGORY_CODE_BLOCK,
                        status=STATUS_IGNORED,
                        token=line.strip(),
                        target=None,
                        reason="fenced_code_block",
                    )
                )
            continue

        is_table = stripped.startswith("|") and stripped.endswith("|")

        # Backticks
        for match in backtick_pattern.finditer(line):
            raw = match.group(1)
            token = normalize_token(raw)

            if is_markdown_link_line_fragment(line, match.start(), match.end()):
                continue

            if ".md" not in token and "/" not in token:
                # Sans extension : seulement si le stem existe.
                if token not in by_stem:
                    continue
                category = CATEGORY_EXTENSIONLESS
            elif "{" in token and "}" in token and token.endswith(".md"):
                category = CATEGORY_BRACE_MULTI
            elif token.startswith("/homeassistant/00_documentation_arsenal/"):
                category = CATEGORY_ABSOLUTE_HA
            elif token.startswith("/00_documentation_arsenal/"):
                category = CATEGORY_ABSOLUTE_DOC
            else:
                category = CATEGORY_BACKTICK_MD

            if is_table:
                results.append(
                    Candidate(
                        source=source,
                        line_no=line_no,
                        category=CATEGORY_TABLE,
                        status=STATUS_IGNORED,
                        token=token,
                        target=None,
                        reason="markdown_table",
                    )
                )
                continue

            status, target, reason = resolve_token(
                token, source, doc_root, by_name, by_stem
            )

            results.append(
                Candidate(
                    source=source,
                    line_no=line_no,
                    category=category,
                    status=status,
                    token=token,
                    target=target,
                    reason=reason,
                )
            )

        # Texte brut .md
        for match in raw_md_pattern.finditer(line):
            token = normalize_token(match.group(1))

            if is_markdown_link_line_fragment(line, match.start(), match.end()):
                continue

            # Éviter de recompter les tokens déjà capturés dans backticks.
            before = line[:match.start()]
            if before.count("`") % 2 == 1:
                continue

            if is_table:
                results.append(
                    Candidate(
                        source=source,
                        line_no=line_no,
                        category=CATEGORY_TABLE,
                        status=STATUS_IGNORED,
                        token=token,
                        target=None,
                        reason="markdown_table",
                    )
                )
                continue

            if "{" in token and "}" in token:
                category = CATEGORY_BRACE_MULTI
            elif token.startswith("/homeassistant/00_documentation_arsenal/"):
                category = CATEGORY_ABSOLUTE_HA
            elif token.startswith("/00_documentation_arsenal/"):
                category = CATEGORY_ABSOLUTE_DOC
            else:
                category = CATEGORY_RAW_MD

            status, target, reason = resolve_token(
                token, source, doc_root, by_name, by_stem
            )

            results.append(
                Candidate(
                    source=source,
                    line_no=line_no,
                    category=category,
                    status=status,
                    token=token,
                    target=target,
                    reason=reason,
                )
            )

    return results


def files_for_scope(doc_root: Path, scope: str | None, custom_path: Path | None) -> list[Path]:
    if custom_path is not None:
        base = custom_path
        if not base.is_absolute():
            base = Path.cwd() / base
        if base.is_file() and base.suffix == ".md":
            return [base]
        return iter_markdown_files(base)

    if scope == "all":
        return iter_markdown_files(doc_root)

    if scope == "chauffage":
        files: list[Path] = []

        scoped_dirs = [
            doc_root / "contrats" / "chauffage",
            doc_root / "architecture" / "chauffage",
        ]

        for folder in scoped_dirs:
            if folder.exists():
                files.extend(iter_markdown_files(folder))

        audits = doc_root / "audits"
        if audits.exists():
            files.extend(
                p for p in iter_markdown_files(audits)
                if "/chauffage/" in p.relative_to(doc_root).as_posix()
            )

        hub = doc_root / "navigation" / "domaines" / "chauffage.md"
        if hub.exists():
            files.append(hub)

        changelog = doc_root / "changelog"
        if changelog.exists():
            for file in iter_markdown_files(changelog):
                try:
                    content = file.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if "chauffage" in content.lower():
                    files.append(file)

        return sorted(set(files))

    raise ValueError(f"Scope inconnu : {scope}")


def markdown_href_from_target(
    source: Path,
    doc_root: Path,
    target_relative_to_doc_root: str,
) -> str:
    target_abs = (doc_root / target_relative_to_doc_root).resolve()
    source_dir = source.parent.resolve()
    return os.path.relpath(target_abs, source_dir).replace("\\", "/")


def markdown_link_for_candidate(
    candidate: Candidate,
    doc_root: Path,
    label_mode: str = "original",
) -> str:
    if candidate.target is None:
        raise ValueError("Candidate target is required for markdown link generation")

    href = markdown_href_from_target(
        source=candidate.source,
        doc_root=doc_root,
        target_relative_to_doc_root=candidate.target,
    )

    if label_mode == "basename":
        label = Path(candidate.target).name
    else:
        label = candidate.token

    return f"[`{label}`]({href})"
    if candidate.target is None:
        raise ValueError("Candidate target is required for markdown link generation")

    href = markdown_href_from_target(
        source=candidate.source,
        doc_root=doc_root,
        target_relative_to_doc_root=candidate.target,
    )

    return f"[`{candidate.token}`]({href})"


def print_report(
    candidates: list[Candidate],
    doc_root: Path,
    files_scanned: list[Path],
    status_filter: str | None = None,
) -> None:
    by_status: dict[str, int] = {}
    by_category: dict[str, int] = {}
    by_file: dict[Path, list[Candidate]] = {}

    for candidate in candidates:
        by_status[candidate.status] = by_status.get(candidate.status, 0) + 1
        by_category[candidate.category] = by_category.get(candidate.category, 0) + 1
        by_file.setdefault(candidate.source, []).append(candidate)

    concerned = {
        c.source for c in candidates
        if c.status != STATUS_IGNORED
    }

    print()
    print("ARSENAL DOC NAVIGATION AUDIT")
    print("============================")
    print()
    print(f"Root: {doc_root.as_posix()}")
    print(f"Files scanned: {len(files_scanned)}")
    print(f"Files concerned: {len(concerned)}")
    print(f"Candidates total: {len(candidates)}")

    if status_filter:
        print(f"Detail filter: {status_filter}")

    print()

    print("By status:")
    for key in (STATUS_AUTO, STATUS_AMBIGUOUS, STATUS_DEAD, STATUS_MULTI, STATUS_IGNORED):
        print(f"  {key}: {by_status.get(key, 0)}")
    print()

    print("By category:")
    for key in sorted(by_category):
        print(f"  {key}: {by_category[key]}")
    print()

    print("Details:")
    for file in sorted(by_file):
        rel_file = file.relative_to(doc_root).as_posix()
        items = by_file[file]
        visible_items = [
            c for c in items
            if c.status != STATUS_IGNORED
        ]

        if status_filter is not None:
            visible_items = [
                c for c in visible_items
                if c.status == status_filter
            ]

        if not visible_items:
            continue

        print()
        print(rel_file)

        for c in visible_items:
            target = f" -> {c.target}" if c.target else ""
            print(
                f"  L{c.line_no:<4} "
                f"{c.status:<12} "
                f"{c.category:<28} "
                f"{c.token}{target}"
            )

    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit Arsenal des références Markdown internes non cliquables."
    )

    parser.add_argument(
        "--root",
        default=DOC_ROOT_DEFAULT,
        help="Racine documentaire. Défaut : 00_documentation_arsenal",
    )

    parser.add_argument(
        "--scope",
        choices=("all", "chauffage"),
        default="all",
        help="Scope prédéfini. Défaut : all",
    )

    parser.add_argument(
        "--path",
        default=None,
        help="Chemin libre à scanner, prioritaire sur --scope",
    )

    parser.add_argument(
        "--status",
        choices=(
            STATUS_AUTO,
            STATUS_AMBIGUOUS,
            STATUS_DEAD,
            STATUS_MULTI,
            STATUS_IGNORED,
        ),
        default=None,
        help="Filtrer l'affichage détaillé par statut.",
    )

    parser.add_argument(
        "--fix-auto",
        action="store_true",
        help="Préparer la conversion des références auto en liens Markdown.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="N'écrit rien ; affiche uniquement les remplacements prévus.",
    )

    parser.add_argument(
        "--label-mode",
        choices=("original", "basename"),
        default="original",
        help="Mode de libellé des liens proposés par --fix-auto.",
    )

    return parser.parse_args()


def print_fix_auto_dry_run(
    candidates: list[Candidate],
    doc_root: Path,
    label_mode: str = "original",
) -> None:
    auto_candidates = [
        c for c in candidates
        if c.status == STATUS_AUTO
    ]

    print()
    print("ARSENAL DOC NAVIGATION FIX-AUTO DRY-RUN")
    print("=======================================")
    print()
    print(f"Auto candidates: {len(auto_candidates)}")
    print(f"Label mode: {label_mode}")
    print()

    by_file: dict[Path, list[Candidate]] = {}

    for candidate in auto_candidates:
        by_file.setdefault(candidate.source, []).append(candidate)

    for file in sorted(by_file):
        rel_file = file.relative_to(doc_root).as_posix()
        print(rel_file)

        for candidate in by_file[file]:
            replacement = markdown_link_for_candidate(
                candidate,
                doc_root,
                label_mode=label_mode,
            )
            print(
                f"  L{candidate.line_no:<4} "
                f"{candidate.category:<24} "
                f"{candidate.token} -> {replacement}"
            )

        print()


def main() -> int:
    args = parse_args()

    doc_root = Path(args.root)
    if not doc_root.is_absolute():
        doc_root = Path.cwd() / doc_root

    doc_root = doc_root.resolve()

    if not doc_root.exists():
        print(f"ERREUR: racine documentaire introuvable: {doc_root}")
        return 2

    custom_path = Path(args.path) if args.path else None

    files_scanned = files_for_scope(doc_root, args.scope, custom_path)
    by_name, by_stem = build_index(doc_root)

    all_candidates: list[Candidate] = []

    for file in files_scanned:
        all_candidates.extend(
            detect_candidates_in_file(
                source=file,
                doc_root=doc_root,
                by_name=by_name,
                by_stem=by_stem,
            )
        )

    if args.fix_auto:
        if not args.dry_run:
            print("ERREUR: --fix-auto est disponible uniquement avec --dry-run pour cette version.")
            return 2

        print_fix_auto_dry_run(
            all_candidates,
            doc_root,
            label_mode=args.label_mode,
        )
        return 0

    print_report(
        all_candidates,
        doc_root,
        files_scanned,
        status_filter=args.status,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())