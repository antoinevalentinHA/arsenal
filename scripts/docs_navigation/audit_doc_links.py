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
    # Positions exactes du token dans la ligne (colonne 0-indexée), pour un
    # remplacement positionnel fiable. None pour les candidats non remplaçables
    # (tableaux, blocs de code, etc.).
    start: int | None = None
    end: int | None = None


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


def _contrats_domain(rel_posix: str) -> str | None:
    """Retourne <X> si le chemin est sous contrats/<X>/..., sinon None."""
    parts = rel_posix.split("/")
    if len(parts) >= 2 and parts[0] == "contrats":
        return parts[1]
    return None


def resolve_token(
    token: str,
    source: Path,
    doc_root: Path,
    by_name: dict[str, list[Path]],
    by_stem: dict[str, list[Path]],
    category: str,
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

    # Auto-référence : le token pointe vers le fichier source lui-même.
    self_present = source_resolved in unique_existing
    non_self = [
        p for p in unique_existing
        if p != source_resolved
    ]

    # Si la seule cible existante est la source elle-même, c'est une
    # auto-référence : on l'ignore explicitement plutôt que de la
    # comptabiliser comme cible morte.
    if not non_self and self_present:
        return STATUS_IGNORED, None, "self_reference"

    # Garde-fou doctrine : la couche navigation/ est détachable et ne doit
    # pas être ciblée automatiquement depuis la documentation. Si toutes les
    # cibles existantes sont sous navigation/, on classe la référence en
    # "ignored" plutôt qu'en "auto"/"ambiguous".
    doc_root_resolved = doc_root.resolve()
    if non_self and all(
        p.relative_to(doc_root_resolved).as_posix().startswith("navigation/")
        for p in non_self
    ):
        return STATUS_IGNORED, None, "navigation_layer"

    if len(non_self) == 1:
        rel = non_self[0].relative_to(doc_root_resolved).as_posix()
        # Garde-fou cross-domaine : une référence "extensionless" dont la
        # cible unique est dans un AUTRE domaine contrats/<...> que la source
        # est très probablement un identifiant technique (nom de sensor, etc.),
        # pas un lien documentaire. On l'ignore plutôt que de la classer auto.
        if category == CATEGORY_EXTENSIONLESS:
            try:
                src_rel = source_resolved.relative_to(doc_root_resolved).as_posix()
            except ValueError:
                src_rel = ""
            src_domain = _contrats_domain(src_rel)
            tgt_domain = _contrats_domain(rel)
            if src_domain and tgt_domain and src_domain != tgt_domain:
                return STATUS_IGNORED, None, "cross_domain_extensionless"
        return STATUS_AUTO, rel, "unique_target"

    if len(non_self) > 1:
        rels = [
            p.relative_to(doc_root.resolve()).as_posix()
            for p in non_self
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
                token, source, doc_root, by_name, by_stem, category
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
                    start=match.start(),
                    end=match.end(),
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
                token, source, doc_root, by_name, by_stem, category
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
                    start=match.start(),
                    end=match.end(),
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

    # Préserver le style visible de la source :
    # - références en backticks (et sans extension, toujours détectées en
    #   contexte backticks) -> libellé conservé en backticks ;
    # - texte brut et chemins absolus -> libellé sans backticks.
    if candidate.category in (CATEGORY_BACKTICK_MD, CATEGORY_EXTENSIONLESS):
        return f"[`{label}`]({href})"

    return f"[{label}]({href})"


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
        if status_filter is not None:
            # Filtre explicite : afficher uniquement ce statut, y compris
            # les références "ignored".
            visible_items = [
                c for c in items
                if c.status == status_filter
            ]
        else:
            # Sans filtre : comportement par défaut, on masque les "ignored".
            visible_items = [
                c for c in items
                if c.status != STATUS_IGNORED
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


def write_markdown_report(
    candidates: list[Candidate],
    doc_root: Path,
    files_scanned: list[Path],
    output_path: Path,
    status_filter: str | None = None,
    path_label: str = "",
) -> None:
    """
    Écrit le rapport d'audit au format Markdown.

    Reprend exactement l'agrégation et le filtrage de print_report() :
    - sans status_filter : les "ignored" ne sont pas détaillés ;
    - avec status_filter : seuls les candidats de ce statut sont détaillés
      (y compris "ignored").
    """
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

    def cell(text: str) -> str:
        # Échapper les barres verticales et neutraliser les retours ligne.
        return text.replace("|", "\\|").replace("\n", " ")

    def code_cell(text: str) -> str:
        text = text.replace("\n", " ")
        if "`" in text:
            # Un backtick dans le token casserait le code span : repli texte.
            return cell(text)
        return "`" + text.replace("|", "\\|") + "`"

    lines: list[str] = []
    lines.append("# ARSENAL — Audit navigation documentaire")
    lines.append("")
    lines.append(f"- Root : {doc_root.as_posix()}")
    lines.append(f"- Path : {path_label or doc_root.as_posix()}")
    lines.append(f"- Files scanned : {len(files_scanned)}")
    lines.append(f"- Files concerned : {len(concerned)}")
    lines.append(f"- Candidates total : {len(candidates)}")
    lines.append(f"- Detail filter : {status_filter or '(none)'}")
    lines.append("")

    lines.append("## Synthèse par statut")
    lines.append("")
    lines.append("| Statut | Nombre |")
    lines.append("|---|---:|")
    for key in (STATUS_AUTO, STATUS_AMBIGUOUS, STATUS_DEAD, STATUS_MULTI, STATUS_IGNORED):
        lines.append(f"| {key} | {by_status.get(key, 0)} |")
    lines.append("")

    lines.append("## Synthèse par catégorie")
    lines.append("")
    lines.append("| Catégorie | Nombre |")
    lines.append("|---|---:|")
    for key in sorted(by_category):
        lines.append(f"| {key} | {by_category[key]} |")
    lines.append("")

    lines.append("## Détails")
    lines.append("")

    any_detail = False
    for file in sorted(by_file):
        rel_file = file.relative_to(doc_root).as_posix()
        items = by_file[file]
        if status_filter is not None:
            visible_items = [c for c in items if c.status == status_filter]
        else:
            visible_items = [c for c in items if c.status != STATUS_IGNORED]

        if not visible_items:
            continue

        any_detail = True
        lines.append(f"### {rel_file}")
        lines.append("")
        lines.append("| Ligne | Statut | Catégorie | Token | Cible / raison |")
        lines.append("|---:|---|---|---|---|")
        for c in visible_items:
            target = c.target if c.target else c.reason
            lines.append(
                f"| {c.line_no} | {cell(c.status)} | {cell(c.category)} | "
                f"{code_cell(c.token)} | {cell(target)} |"
            )
        lines.append("")

    if not any_detail:
        lines.append("_Aucun détail à afficher pour ce filtre._")
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written: {output_path}")


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
        "--apply",
        action="store_true",
        help="Applique réellement les conversions --fix-auto.",
    )

    parser.add_argument(
        "--label-mode",
        choices=("original", "basename"),
        default="original",
        help="Mode de libellé des liens proposés par --fix-auto.",
    )

    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Écrire le rapport d'audit dans un fichier Markdown "
            "au lieu de la sortie console."
        ),
    )

    return parser.parse_args()


REPLACEABLE_CATEGORIES = (
    CATEGORY_BACKTICK_MD,
    CATEGORY_RAW_MD,
    CATEGORY_ABSOLUTE_DOC,
    CATEGORY_ABSOLUTE_HA,
    CATEGORY_EXTENSIONLESS,
)


def _split_eol(raw_line: str) -> tuple[str, str]:
    """Sépare une ligne en (contenu sans fin de ligne, fin de ligne)."""
    if raw_line.endswith("\r\n"):
        return raw_line[:-2], "\r\n"
    if raw_line.endswith("\n"):
        return raw_line[:-1], "\n"
    if raw_line.endswith("\r"):
        return raw_line[:-1], "\r"
    return raw_line, ""


def plan_file_replacements(
    file: Path,
    file_candidates: list[Candidate],
    doc_root: Path,
    label_mode: str,
) -> tuple[str, list[tuple[Candidate, str]], list[tuple[Candidate, str]]]:
    """
    Calcule le nouveau contenu d'un fichier par remplacement POSITIONNEL.

    - Aucun `line.replace()` : on remplace exactement `line[start:end]`.
    - Sur une même ligne, remplacements appliqués de droite à gauche
      (start décroissant), sans chevauchement : les positions à gauche
      restent valides tant qu'on ne touche jamais une zone déjà remplacée
      plus à droite.
    - Un candidat sans positions fiables n'est jamais remplacé ; il est
      reporté comme "skipped".

    Retourne (new_text, applied, skipped) où
      applied = [(candidate, replacement_str)]
      skipped = [(candidate, reason)]
    """
    original_text = file.read_text(encoding="utf-8", errors="replace")
    raw_lines = original_text.splitlines(keepends=True)
    contents: list[str] = []
    eols: list[str] = []
    for raw_line in raw_lines:
        content, eol = _split_eol(raw_line)
        contents.append(content)
        eols.append(eol)

    by_line: dict[int, list[Candidate]] = {}
    for candidate in file_candidates:
        by_line.setdefault(candidate.line_no, []).append(candidate)

    applied: list[tuple[Candidate, str]] = []
    skipped: list[tuple[Candidate, str]] = []

    for line_no, line_candidates in by_line.items():
        index = line_no - 1

        if index < 0 or index >= len(contents):
            for candidate in line_candidates:
                skipped.append((candidate, "line_out_of_range"))
            continue

        line = contents[index]

        usable: list[Candidate] = []
        for candidate in line_candidates:
            if candidate.start is None or candidate.end is None:
                skipped.append((candidate, "no_position"))
                continue
            if not (0 <= candidate.start < candidate.end <= len(line)):
                skipped.append((candidate, "invalid_position"))
                continue
            usable.append(candidate)

        usable.sort(key=lambda c: c.start, reverse=True)

        new_line = line
        boundary = len(line)
        for candidate in usable:
            if candidate.end > boundary:
                skipped.append((candidate, "overlap"))
                continue
            replacement = markdown_link_for_candidate(
                candidate, doc_root, label_mode=label_mode
            )
            new_line = (
                new_line[: candidate.start]
                + replacement
                + new_line[candidate.end :]
            )
            applied.append((candidate, replacement))
            boundary = candidate.start

        contents[index] = new_line

    new_text = "".join(content + eol for content, eol in zip(contents, eols))
    return new_text, applied, skipped


def _auto_candidates_by_file(
    candidates: list[Candidate],
) -> dict[Path, list[Candidate]]:
    by_file: dict[Path, list[Candidate]] = {}
    for candidate in candidates:
        if candidate.status == STATUS_AUTO:
            by_file.setdefault(candidate.source, []).append(candidate)
    return by_file


def _print_skipped(skipped: list[tuple[Candidate, str]], doc_root: Path) -> None:
    if not skipped:
        return
    print(f"Skipped (positions non fiables, non remplacés): {len(skipped)}")
    for candidate, reason in skipped:
        rel = candidate.source.relative_to(doc_root).as_posix()
        print(
            f"  {rel}:L{candidate.line_no} "
            f"{candidate.category} {candidate.token} [{reason}]"
        )
    print()


def print_fix_auto_dry_run(
    candidates: list[Candidate],
    doc_root: Path,
    label_mode: str = "original",
) -> None:
    by_file = _auto_candidates_by_file(candidates)
    total_auto = sum(len(items) for items in by_file.values())

    print()
    print("ARSENAL DOC NAVIGATION FIX-AUTO DRY-RUN")
    print("=======================================")
    print()
    print(f"Auto candidates: {total_auto}")
    print(f"Label mode: {label_mode}")
    print()

    total_planned = 0
    all_skipped: list[tuple[Candidate, str]] = []

    for file in sorted(by_file):
        _, applied, skipped = plan_file_replacements(
            file, by_file[file], doc_root, label_mode
        )
        all_skipped.extend(skipped)
        if not applied:
            continue

        print(file.relative_to(doc_root).as_posix())
        for candidate, replacement in sorted(
            applied, key=lambda pair: (pair[0].line_no, pair[0].start or 0)
        ):
            print(
                f"  L{candidate.line_no:<4} "
                f"{candidate.category:<24} "
                f"{candidate.token} -> {replacement}"
            )
        print()
        total_planned += len(applied)

    print(f"Planned replacements: {total_planned}")
    print()
    _print_skipped(all_skipped, doc_root)


def apply_fix_auto(
    candidates: list[Candidate],
    doc_root: Path,
    label_mode: str = "original",
) -> int:
    by_file = _auto_candidates_by_file(candidates)

    changed_files = 0
    total_replacements = 0
    all_skipped: list[tuple[Candidate, str]] = []

    for file in sorted(by_file):
        new_text, applied, skipped = plan_file_replacements(
            file, by_file[file], doc_root, label_mode
        )
        all_skipped.extend(skipped)
        if applied:
            file.write_text(new_text, encoding="utf-8")
            changed_files += 1
            total_replacements += len(applied)

    print()
    print("ARSENAL DOC NAVIGATION FIX-AUTO APPLY")
    print("=====================================")
    print()
    print(f"Files changed: {changed_files}")
    print(f"Replacements: {total_replacements}")
    print(f"Label mode: {label_mode}")
    print()
    _print_skipped(all_skipped, doc_root)

    return total_replacements


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
        if args.dry_run and args.apply:
            print("ERREUR: --dry-run et --apply sont incompatibles.")
            return 2

        if not args.dry_run and not args.apply:
            print("ERREUR: --fix-auto requiert --dry-run ou --apply.")
            return 2

        if args.dry_run:
            print_fix_auto_dry_run(
                all_candidates,
                doc_root,
                label_mode=args.label_mode,
            )
            return 0

        if args.apply:
            apply_fix_auto(
                all_candidates,
                doc_root,
                label_mode=args.label_mode,
            )
            return 0

    if args.output:
        write_markdown_report(
            all_candidates,
            doc_root,
            files_scanned,
            output_path=Path(args.output),
            status_filter=args.status,
            path_label=args.path or f"(scope: {args.scope})",
        )
    else:
        print_report(
            all_candidates,
            doc_root,
            files_scanned,
            status_filter=args.status,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())