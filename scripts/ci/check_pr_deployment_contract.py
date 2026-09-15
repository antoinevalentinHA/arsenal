#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arsenal — Contrat de déploiement des Pull Requests.

Source normative : `.github/pull_request_template.md`, section `## Déploiement`.

Objet — volontairement ÉTROIT : ce contrôle vérifie que la **déclaration** de
déploiement d'une PR est structurellement complète et non ambiguë. Il ne juge
JAMAIS si le plan de déploiement est techniquement correct, suffisant ou
pertinent — cela relève exclusivement du jugement humain (revue de PR).
CI est une frontière, pas un oracle : rouge = déclaration incomplète/ambiguë
(état interdit), vert = déclaration structurellement recevable (admissible au
jugement humain).

Invariants vérifiés :

    DEP-001  Exactement un état de déploiement runtime est coché parmi
             « Déploiement runtime requis » / « Déploiement runtime : aucun ».
             Interdit : aucun coché, ou les deux.

    DEP-002  Si « Déploiement runtime : aucun » est coché, la section est
             structurellement suffisante — aucune autre exigence n'est
             imposée (pas de bureaucratie sur les PR doc/CI/outillage).

    DEP-003  Si « Déploiement runtime requis » est coché, les champs
             « Cible du déploiement », « Fichiers / composants concernés » et
             « Validation post-déploiement attendue » doivent être renseignés
             (non vides, hors commentaire HTML du gabarit).

    DEP-004  Si le déploiement runtime est requis, exactement un mode
             d'application Home Assistant est coché parmi les cinq proposés
             par le gabarit. Interdit : aucun coché, ou plusieurs.

    DEP-005  Si le mode coché appelle une précision (Reload ciblé, Reload
             d'un domaine/intégration, Redémarrage complet, Autre mécanisme),
             cette précision doit être présente. Le gabarit fait toujours
             finir le libellé de ces modes par `:` juste avant la zone de
             réponse : la précision est le texte non vide qui suit le
             DERNIER `:` du bloc (ligne du item + ses lignes de continuation
             indentées). « Aucun reload nécessaire » n'appelle aucune
             précision.

    DEP-006  Refuse un petit ensemble FERMÉ de formulations que le gabarit
             qualifie lui-même explicitement d'insuffisantes (« pull sur HA »,
             « reload si nécessaire », « redémarrer au besoin », « vérifier
             que ça marche »), quand l'une d'elles constitue la réponse d'un
             champ DEP-003 ou d'une précision DEP-005. Détection déterministe
             par expression régulière tolérante aux accents/espaces, PAS un
             moteur NLP : ne détecte que ces formulations précises, aucune
             paraphrase. Une réponse qui contient l'une de ces formulations en
             complément d'un contenu concret n'est pas visée : DEP-006 ne
             remplace pas la lecture humaine, il verrouille juste les
             réponses que le gabarit désigne lui-même comme des non-réponses.

Ce que ce contrôle NE fait PAS :
    - il ne valide aucune autre section du gabarit de PR (Intention, Couches
      touchées, Impact runtime, Conformité à la doctrine, Contrôles, Notes) ;
    - il n'évalue pas la pertinence technique du plan de déploiement déclaré ;
    - il n'exige rien au-delà de ce que le gabarit demande explicitement.

Entrée : le corps (Markdown) de la Pull Request. En CI, fourni via la
variable d'environnement `PR_BODY` (jamais interpolé dans un `run:` shell —
injection de script côté GitHub Actions). En local/tests, `--body-file`.

Sortie :
    - exit 0 : le contrat de déploiement est structurellement respecté ;
    - exit 1 : au moins une violation (rapport détaillé) ;
    - exit 2 : erreur d'exécution (aucun corps de PR fourni) ou régression
      du checker lui-même (`--selftest`).

Usage :
  PR_BODY="$(cat corps.md)" python scripts/ci/check_pr_deployment_contract.py
  python scripts/ci/check_pr_deployment_contract.py --body-file corps.md
  python scripts/ci/check_pr_deployment_contract.py --selftest
"""

from __future__ import annotations

import argparse
import os
import re
import sys

# ---------------------------------------------------------------------------
# Normalisation du texte brut de la PR
# ---------------------------------------------------------------------------

_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_APOSTROPHE_RE = re.compile(r"[‘’]")


def _strip_html_comments(text: str) -> str:
    """Retire les commentaires HTML du gabarit : ce n'est pas du contenu auteur."""
    return _HTML_COMMENT_RE.sub("", text)


def _normalize(text: str) -> str:
    """Neutralise les apostrophes typographiques ; ne touche à rien d'autre."""
    return _APOSTROPHE_RE.sub("'", text)


# ---------------------------------------------------------------------------
# Extraction de la section « ## Déploiement »
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^##\s+(.*?)\s*$", re.M)


def extract_section(body: str, title: str) -> str | None:
    """
    Renvoie le texte de la section de niveau 2 dont le titre correspond
    (comparaison insensible à la casse), du titre exclu jusqu'au prochain
    titre `## ` ou la fin du texte. `None` si la section est absente.
    """
    headings = list(_HEADING_RE.finditer(body))
    for idx, match in enumerate(headings):
        if match.group(1).strip().casefold() != title.casefold():
            continue
        start = match.end()
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(body)
        return body[start:end]
    return None


# ---------------------------------------------------------------------------
# Cases à cocher — repérage par libellé, robuste aux lignes de continuation
# ---------------------------------------------------------------------------

_CHECKBOX_LINE_RE = re.compile(r"^[ \t]*-\s*\[([ xX])\]\s*(.*)$")


def _iter_lines(section: str) -> list[str]:
    return section.splitlines()


def _bullet_block(lines: list[str], start: int) -> str:
    """
    Rejoint la ligne de bullet `start` avec ses lignes de continuation :
    toute ligne suivante non vide qui n'ouvre ni une nouvelle case à cocher,
    ni un nouveau titre, ni un nouveau champ en gras à la marge.
    """
    block = [lines[start]]
    i = start + 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            break
        if _CHECKBOX_LINE_RE.match(line):
            break
        if re.match(r"^#{1,6}\s", line):
            break
        if re.match(r"^\*\*", line.strip()):
            break
        block.append(line)
        i += 1
    return " ".join(l.strip() for l in block)


def find_checkbox(section: str, label_pattern: str) -> tuple[bool, str] | None:
    """
    Cherche la case à cocher dont le texte du item correspond à
    `label_pattern` (regex, insensible à la casse). Renvoie
    (coché, bloc_texte_complet) ou None si aucune case ne correspond.
    """
    lines = _iter_lines(section)
    pattern = re.compile(label_pattern, re.I)
    for i, line in enumerate(lines):
        m = _CHECKBOX_LINE_RE.match(line)
        if not m:
            continue
        if not pattern.search(m.group(2)):
            continue
        checked = m.group(1).strip().lower() == "x"
        block = _bullet_block(lines, i)
        return checked, block
    return None


_DECOR_RE = re.compile(r"[*_`~]")


def _precision_after_last_colon(block: str) -> str:
    """
    DEP-005 : la précision attendue est le texte non vide qui suit le
    DERNIER `:` du bloc (bullet + continuation). Le gabarit fait toujours
    finir sa consigne par `:` juste avant la zone de réponse — chercher le
    dernier `:` est donc insensible au nombre de `:` que porte la consigne
    elle-même (ex. « Autre mécanisme » en cite plusieurs). Les décorations
    Markdown pures (le gabarit ferme certaines consignes par `:**`) ne
    comptent pas comme contenu.
    """
    idx = block.rfind(":")
    tail = block[idx + 1 :] if idx != -1 else block
    return _DECOR_RE.sub("", tail).strip()


# ---------------------------------------------------------------------------
# Champs en gras (« **Libellé :** réponse »)
# ---------------------------------------------------------------------------


def extract_bold_field(section: str, label_pattern: str) -> str | None:
    """
    Renvoie le contenu du champ en gras `**<label_pattern>...:**` — tout ce
    qui suit jusqu'à la prochaine ligne vide, le prochain champ en gras en
    tête de ligne, ou la fin de la section. `None` si le champ est absent.
    """
    pattern = re.compile(
        r"\*\*\s*" + label_pattern + r"\s*:?\s*\*\*(.*?)(?=\n\*\*|\n#{1,6}\s|\Z)",
        re.I | re.S,
    )
    m = pattern.search(section)
    if not m:
        return None
    return _DECOR_RE.sub("", m.group(1)).strip()


# ---------------------------------------------------------------------------
# DEP-006 — formulations explicitement insuffisantes (liste FERMÉE, du gabarit)
# ---------------------------------------------------------------------------

_INSUFFICIENT_PATTERNS = {
    "pull sur HA": re.compile(r"pull\s+sur\s+ha\b", re.I),
    "reload si nécessaire": re.compile(r"reload\s+si\s+n[ée]cessaire", re.I),
    "redémarrer au besoin": re.compile(r"red[ée]marrer\s+au\s+besoin", re.I),
    "vérifier que ça marche": re.compile(r"v[ée]rifier\s+que\s+[çc]a\s+marche", re.I),
}


def insufficient_phrase(text: str) -> str | None:
    """Renvoie le libellé de la première formulation proscrite trouvée, sinon None."""
    for label, pattern in _INSUFFICIENT_PATTERNS.items():
        if pattern.search(text):
            return label
    return None


# ---------------------------------------------------------------------------
# Modes d'application Home Assistant (DEP-004 / DEP-005)
# ---------------------------------------------------------------------------

# clé -> (regex de libellé, précision requise ?)
_MODES = {
    "aucun_reload": (r"Aucun reload n[ée]cessaire", False),
    "reload_cible": (r"Reload cibl[ée]", True),
    "reload_domaine": (r"Reload d'un domaine ou d'une int[ée]gration", True),
    "restart_complet": (r"Red[ée]marrage complet Home Assistant", True),
    "autre_mecanisme": (r"Autre m[ée]canisme", True),
}


# ---------------------------------------------------------------------------
# Cœur de validation, pur (texte -> liste d'écarts)
# ---------------------------------------------------------------------------


def check_deployment_contract(body: str) -> list[str]:
    """Renvoie la liste des messages d'écart (vide = contrat respecté)."""
    body = _normalize(_strip_html_comments(body or ""))
    section = extract_section(body, "Déploiement")

    if section is None:
        return [
            "DEP-001  Section « ## Déploiement » absente du corps de la PR : "
            "exactement un état de déploiement runtime doit être déclaré."
        ]

    errors: list[str] = []

    requis = find_checkbox(section, r"D[ée]ploiement runtime requis")
    aucun = find_checkbox(section, r"D[ée]ploiement runtime\s*:\s*aucun")

    requis_checked = bool(requis and requis[0])
    aucun_checked = bool(aucun and aucun[0])

    # --- DEP-001 ------------------------------------------------------
    if requis_checked == aucun_checked:
        if requis_checked:
            errors.append(
                "DEP-001  Un seul état de déploiement runtime peut être coché "
                "(« requis » et « aucun » sont cochés simultanément)."
            )
        else:
            errors.append(
                "DEP-001  Exactement un état de déploiement runtime doit être "
                "coché (aucun des deux ne l'est)."
            )
        return errors

    # --- DEP-002 --------------------------------------------------------
    if aucun_checked:
        return errors  # section structurellement suffisante, rien de plus à exiger

    # --- DEP-003 : déploiement requis -> champs obligatoires -------------
    assert requis_checked
    required_fields = {
        "Cible du déploiement": r"Cible du d[ée]ploiement",
        "Fichiers / composants concernés": r"Fichiers\s*/\s*composants concern[ée]s",
        "Validation post-déploiement attendue": r"Validation post-d[ée]ploiement attendue",
    }
    for field_label, field_pattern in required_fields.items():
        content = extract_bold_field(section, field_pattern)
        if not content:
            errors.append(
                f"DEP-003  Champ « {field_label} » non renseigné alors que le "
                "déploiement runtime est requis."
            )
            continue
        phrase = insufficient_phrase(content)
        if phrase:
            errors.append(
                f'DEP-006  Champ « {field_label} » : formulation jugée '
                f'insuffisante par le gabarit (« {phrase} »).'
            )

    # --- DEP-004 : exactement un mode d'application coché -----------------
    checked_modes: list[str] = []
    blocks: dict[str, str] = {}
    for key, (pattern, _needs_precision) in _MODES.items():
        found = find_checkbox(section, pattern)
        if found and found[0]:
            checked_modes.append(key)
            blocks[key] = found[1]

    if len(checked_modes) == 0:
        errors.append(
            "DEP-004  Déploiement runtime requis mais aucun mode d'application "
            "Home Assistant n'est coché."
        )
    elif len(checked_modes) > 1:
        errors.append(
            "DEP-004  Déploiement runtime requis mais plusieurs modes "
            "d'application Home Assistant sont cochés (un seul est attendu)."
        )
    else:
        # --- DEP-005 : précision si le mode choisi en appelle une --------
        mode_key = checked_modes[0]
        _pattern, needs_precision = _MODES[mode_key]
        if needs_precision:
            precision = _precision_after_last_colon(blocks[mode_key])
            mode_labels = {
                "reload_cible": "Reload ciblé",
                "reload_domaine": "Reload d'un domaine ou d'une intégration",
                "restart_complet": "Redémarrage complet Home Assistant",
                "autre_mecanisme": "Autre mécanisme",
            }
            if not precision:
                errors.append(
                    f'DEP-005  « {mode_labels[mode_key]} » est coché mais aucune '
                    "précision n'est indiquée."
                )
            else:
                phrase = insufficient_phrase(precision)
                if phrase:
                    errors.append(
                        f'DEP-006  Précision de « {mode_labels[mode_key]} » : '
                        f'formulation jugée insuffisante par le gabarit (« {phrase} »).'
                    )

    return errors


# ---------------------------------------------------------------------------
# Auto-test du juge (on ne juge pas avec un juge défectueux)
# ---------------------------------------------------------------------------


def _selftest() -> int:
    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    def has_code(errs: list[str], code: str) -> bool:
        return any(e.startswith(code) for e in errs)

    HEADER = "## Déploiement\n\n"

    # 1. Aucun choix de déploiement -> DEP-001
    body = HEADER + (
        "- [ ] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-001"), "cas 1 : aucun choix -> DEP-001 attendu")

    # 2. Les deux cochés -> DEP-001
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [x] **Déploiement runtime : aucun**\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-001"), "cas 2 : deux choix -> DEP-001 attendu")

    # 3. « runtime : aucun » seul -> PASS
    body = HEADER + (
        "- [ ] **Déploiement runtime requis**\n"
        "- [x] **Déploiement runtime : aucun** (changement doc)\n"
    )
    errs = check_deployment_contract(body)
    expect(errs == [], f"cas 3 : runtime aucun seul -> PASS attendu, eu {errs!r}")

    # 4. « runtime requis » avec champs correctement remplis -> PASS
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** `/homeassistant/`\n\n"
        "**Fichiers / composants concernés :**\n\n"
        "automations/chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [x] Reload ciblé — préciser l'élément concerné :\n"
        "automation.reload\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** vérifier que "
        "`automation.chauffage_relance` passe à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(errs == [], f"cas 4 : requis + champs complets -> PASS attendu, eu {errs!r}")

    # 5. « runtime requis » avec cible absente -> DEP-003
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** <!-- guidance du gabarit -->\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [x] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-003"), f"cas 5 : cible absente -> DEP-003 attendu, eu {errs!r}")

    # 6. mode HA absent -> DEP-004
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** /homeassistant/\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-004"), f"cas 6 : mode absent -> DEP-004 attendu, eu {errs!r}")

    # 7. plusieurs modes HA cochés -> DEP-004
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** /homeassistant/\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [x] Aucun reload nécessaire\n"
        "- [x] Reload ciblé — préciser l'élément concerné :\n"
        "automation.reload\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-004"), f"cas 7 : deux modes -> DEP-004 attendu, eu {errs!r}")

    # 8. reload ciblé sans cible -> DEP-005
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** /homeassistant/\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [x] Reload ciblé — préciser l'élément concerné (ex. "
        "`automation.reload`) :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-005"), f"cas 8 : reload ciblé sans cible -> DEP-005 attendu, eu {errs!r}")

    # 9. restart complet sans justification -> DEP-005
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** /homeassistant/\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [x] Redémarrage complet Home Assistant — **à ne cocher que si "
        "aucun reload ciblé ou de domaine/intégration ne suffit ; justifier "
        "pourquoi ci-dessous, jamais par commodité ou par défaut :**\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-005"), f"cas 9 : restart sans justification -> DEP-005 attendu, eu {errs!r}")

    # 10. autre mécanisme sans précision -> DEP-005
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** /homeassistant/\n\n"
        "**Fichiers / composants concernés :** chauffage.yaml\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [x] Autre mécanisme (préciser — ex. contenu YAML d'un dashboard "
        "Lovelace : ouvrir le dashboard concerné → menu ⋮ → Actualiser) :\n\n"
        "**Validation post-déploiement attendue :** entité X à `on`.\n"
    )
    errs = check_deployment_contract(body)
    expect(has_code(errs, "DEP-005"), f"cas 10 : autre mécanisme sans précision -> DEP-005 attendu, eu {errs!r}")

    # 11. commentaires HTML seuls -> ne comptent pas comme réponse (DEP-003)
    body = HEADER + (
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun**\n\n"
        "**Cible du déploiement :** <!-- par défaut le dépôt `/homeassistant/` -->\n\n"
        "**Fichiers / composants concernés :** <!-- lister les fichiers -->\n\n"
        "**Mode d'application Home Assistant** :\n"
        "- [x] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné :\n"
        "- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** <!-- entité et état -->\n"
    )
    errs = check_deployment_contract(body)
    dep003 = [e for e in errs if e.startswith("DEP-003")]
    expect(len(dep003) == 3, f"cas 11 : 3 champs en commentaire seul -> 3×DEP-003 attendus, eu {errs!r}")

    # 12. corps de PR réaliste conservant le reste du gabarit -> parsing correct
    body = (
        "## Intention\n\n"
        "Corrige un seuil de température.\n\n"
        "## Couche(s) touchée(s)\n\n"
        "- [x] **Décision** (template sensors, helpers, admissibilité)\n"
        "- [ ] **Action** (automatisations, scripts souverains, exécutants bornés)\n\n"
        "## Impact runtime\n\n"
        "Nouveau seuil appliqué en décision.\n\n"
        "## Déploiement\n\n"
        "- [x] **Déploiement runtime requis**\n"
        "- [ ] **Déploiement runtime : aucun** (le changement peut être "
        "présent dans le clone après merge, mais n'exige aucune application "
        "au runtime Home Assistant)\n\n"
        "**Cible du déploiement :** `/homeassistant/`\n\n"
        "**Fichiers / composants concernés :**\n\n"
        "12_template_sensors/chauffage/seuils.yaml\n\n"
        "**Mode d'application Home Assistant** — choisir le mode le moins "
        "intrusif qui suffit :\n"
        "- [ ] Aucun reload nécessaire\n"
        "- [ ] Reload ciblé — préciser l'élément concerné (ex. "
        "`automation.reload`) :\n"
        "template.reload\n"
        "- [x] Reload d'un domaine ou d'une intégration — préciser lequel :\n"
        "template (Outils de développement > YAML > Recharger les entités template)\n"
        "- [ ] Redémarrage complet Home Assistant :\n"
        "- [ ] Autre mécanisme (préciser) :\n\n"
        "**Validation post-déploiement attendue :** `sensor.seuil_chauffage` "
        "reflète la nouvelle valeur.\n\n"
        "## Conformité à la doctrine\n\n"
        "- [x] La séparation décision / action / diagnostic / UI est respectée.\n"
        "- [ ] Aucun ID inventé.\n\n"
        "## Contrôles\n\n"
        "- [x] CI verte.\n"
    )
    errs = check_deployment_contract(body)
    expect(errs == [], f"cas 12 : corps réaliste complet -> PASS attendu, eu {errs!r}")

    # Cas additionnel : section absente -> DEP-001 (pas de crash)
    errs = check_deployment_contract("## Intention\n\nRAS.\n")
    expect(has_code(errs, "DEP-001"), "section absente -> DEP-001 attendu")

    # Robustesse : corps vide / None
    expect(has_code(check_deployment_contract(""), "DEP-001"), "corps vide -> DEP-001")

    # Robustesse : case cochée avec un X majuscule
    body = HEADER + (
        "- [ ] **Déploiement runtime requis**\n"
        "- [X] **Déploiement runtime : aucun**\n"
    )
    expect(check_deployment_contract(body) == [], "case cochée en X majuscule doit être reconnue")

    if failures:
        print("SELFTEST KO :")
        for f in failures:
            print(f"  - {f}")
        return 2
    print("SELFTEST OK — 12 cas requis + robustesse exercés.")
    return 0


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Contrat de déploiement de la section ## Déploiement d'une PR."
    )
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument(
        "--body-file",
        help="Lire le corps de la PR depuis un fichier (usage local/tests). "
        "En CI, le corps vient de la variable d'environnement PR_BODY.",
    )
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if args.selftest:
        return _selftest()

    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as fh:
            body = fh.read()
    elif "PR_BODY" in os.environ:
        body = os.environ["PR_BODY"]
    else:
        print(
            "::error::Aucun corps de PR fourni (ni --body-file, ni variable "
            "d'environnement PR_BODY).",
            file=sys.stderr,
        )
        return 2

    errors = check_deployment_contract(body)

    if errors:
        print("PR deployment contract: FAIL\n")
        for err in errors:
            print(err)
        print(
            "\n::error::Contrat de déploiement de la PR non respecté "
            "(section « ## Déploiement ») — voir le détail ci-dessus."
        )
        return 1

    print("PR deployment contract: OK — section « ## Déploiement » conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
