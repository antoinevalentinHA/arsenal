#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Paramètres invalides
Contrat (source normative) : 00_documentation_arsenal/contrats/parametres_invalides.md
Script  : scripts/arsenal_contracts/check_parametres_invalides_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers et dossiers canoniques
# ---------------------------------------------------------------------------
F_GROUPE    = REPO_ROOT / "02_groups/parametres_invalides.yaml"
F_GLOBAL    = REPO_ROOT / "12_template_sensors/system/integrite_reglages/global.yaml"
F_UI        = REPO_ROOT / "18_lovelace/includes/alerte_configuration_invalide.yaml"
DIR_DOMAINES = REPO_ROOT / "12_template_sensors/system/integrite_reglages"

# Dashboards principaux devant inclure la carte UI
DASHBOARDS = [
    REPO_ROOT / "18_lovelace/dashboards/arsenal.yaml",
    REPO_ROOT / "18_lovelace/dashboards/navigation.yaml",
]

# Icônes normatives par couche
ICON_COUCHE1 = "mdi:alert-circle-outline"
ICON_COUCHE3 = "mdi:alert-octagon-outline"

# Attributs obligatoires de la sentinelle globale (§ Couche 3)
ATTRS_GLOBAL = ["domaines_invalides", "nombre_domaines_invalides"]

# Fallbacks silencieux interdits (§ Doctrine d'expression)
FORBIDDEN_FALLBACKS = [
    re.compile(r"\|\s*float\s*\(\s*0\s*\)"),
    re.compile(r"\|\s*int\s*\(\s*0\s*\)"),
]

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def domain_files() -> list[Path]:
    """Retourne les fichiers capteurs domaine (tous sauf global.yaml)."""
    if not DIR_DOMAINES.is_dir():
        return []
    return [
        p for p in DIR_DOMAINES.glob("*.yaml")
        if p.is_file() and p.name != "global.yaml"
    ]


def extract_unique_ids(content: str, prefix: str = "parametres_invalides_") -> list[str]:
    """Extrait les unique_id commençant par le préfixe donné."""
    return re.findall(
        rf"unique_id\s*:\s*({re.escape(prefix)}[^\s\n]+)",
        content
    )


def extract_group_entities(content: str) -> list[str]:
    """Extourne les entity_id listés dans le fichier de groupe."""
    return re.findall(
        r"-\s*(binary_sensor\.parametres_invalides_[^\s\n]+)",
        content
    )


# ---------------------------------------------------------------------------
# T1 — Présence des fichiers canoniques des couches 2, 3, 4
# ---------------------------------------------------------------------------

def test_canonical_files_present() -> None:
    all_ok = True
    for label, path in [
        ("T1a — groupe (couche 2)", F_GROUPE),
        ("T1b — sentinelle globale (couche 3)", F_GLOBAL),
        ("T1c — UI (couche 4)", F_UI),
    ]:
        if not path.is_file():
            ERRORS.append(f"T1 — Fichier canonique manquant ({label}) : "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
    if all_ok:
        print("✔ T1 — Fichiers canoniques couches 2/3/4 présents")


# ---------------------------------------------------------------------------
# T2 — Capteurs domaine : unique_id et default_entity_id conformes (§ Couche 1)
#
# Invariant : chaque fichier dans integrite_reglages/ (hors global.yaml)
# doit déclarer unique_id: parametres_invalides_<domaine> et
# default_entity_id: binary_sensor.parametres_invalides_<domaine>.
# ---------------------------------------------------------------------------

def test_domain_sensors_unique_id() -> None:
    files = domain_files()
    if not files:
        ERRORS.append("T2 — Aucun capteur domaine trouvé dans "
                      f"{DIR_DOMAINES.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for path in sorted(files):
        content = read(path)
        uid_match = re.search(r"unique_id\s*:\s*(parametres_invalides_\S+)", content)
        if not uid_match:
            ERRORS.append(f"T2 — unique_id: parametres_invalides_* absent de "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
            continue
        uid = uid_match.group(1)
        expected_deid = f"binary_sensor.{uid}"
        if expected_deid not in content:
            ERRORS.append(f"T2 — default_entity_id: {expected_deid} absent de "
                          f"{path.relative_to(REPO_ROOT)}")
            all_ok = False
    if all_ok:
        print(f"✔ T2 — unique_id et default_entity_id conformes sur "
              f"{len(files)} capteur(s) domaine")


# ---------------------------------------------------------------------------
# T3 — Cohérence groupe ↔ capteurs domaine (§ Couche 2)
#
# Invariant : tout capteur domaine présent dans integrite_reglages/
# doit être listé dans le groupe, et inversement.
# ---------------------------------------------------------------------------

def test_group_coherence() -> None:
    groupe_content = read(F_GROUPE)
    if not groupe_content:
        ERRORS.append(f"T3 — Fichier groupe inaccessible : "
                      f"{F_GROUPE.relative_to(REPO_ROOT)}")
        return

    # Entités déclarées dans le groupe
    groupe_entities = set(extract_group_entities(groupe_content))

    # Entités dans les fichiers domaine
    domain_entities = set()
    for path in domain_files():
        content = read(path)
        uid_match = re.search(r"unique_id\s*:\s*(parametres_invalides_\S+)", content)
        if uid_match:
            domain_entities.add(f"binary_sensor.{uid_match.group(1)}")

    manquants_dans_groupe = domain_entities - groupe_entities
    orphelins_dans_groupe = groupe_entities - domain_entities

    if manquants_dans_groupe:
        for e in sorted(manquants_dans_groupe):
            ERRORS.append(f"T3 — Capteur domaine absent du groupe : {e} "
                          f"(doit être ajouté dans {F_GROUPE.relative_to(REPO_ROOT)})")
    if orphelins_dans_groupe:
        for e in sorted(orphelins_dans_groupe):
            ERRORS.append(f"T3 — Entité dans le groupe sans fichier domaine : {e}")
    if not manquants_dans_groupe and not orphelins_dans_groupe:
        print(f"✔ T3 — Groupe cohérent avec les {len(domain_entities)} "
              f"capteur(s) domaine")


# ---------------------------------------------------------------------------
# T4 — Sentinelle globale : consomme uniquement le groupe (§ Couche 3)
#
# Invariant : le state de global.yaml doit lire exclusivement
# group.parametres_invalides_domaines, sans référence directe à des
# input_number, input_datetime, ou capteurs domaine spécifiques.
# ---------------------------------------------------------------------------

def test_global_consumes_only_group() -> None:
    content = read(F_GLOBAL)
    if not content:
        ERRORS.append(f"T4 — Fichier global inaccessible : "
                      f"{F_GLOBAL.relative_to(REPO_ROOT)}")
        return

    # Doit consommer le groupe
    has_group = "group.parametres_invalides_domaines" in content
    if not has_group:
        ERRORS.append("T4 — group.parametres_invalides_domaines absent de "
                      f"{F_GLOBAL.relative_to(REPO_ROOT)}")
        return

    # Ne doit pas lire directement des helpers
    forbidden = [
        re.compile(r"states\s*\(\s*['\"]input_number\."),
        re.compile(r"states\s*\(\s*['\"]input_datetime\."),
    ]
    for pattern in forbidden:
        if pattern.search(content):
            ERRORS.append(f"T4 — Lecture directe d'helper dans global.yaml "
                          f"(couche 3 ne doit lire que le groupe) : "
                          f"{F_GLOBAL.relative_to(REPO_ROOT)}")
            return

    print("✔ T4 — Sentinelle globale consomme uniquement le groupe")


# ---------------------------------------------------------------------------
# T5 — Sentinelle globale : attributs obligatoires présents (§ Couche 3)
# ---------------------------------------------------------------------------

def test_global_attributes() -> None:
    content = read(F_GLOBAL)
    if not content:
        ERRORS.append(f"T5 — Fichier global inaccessible : "
                      f"{F_GLOBAL.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for attr in ATTRS_GLOBAL:
        if attr not in content:
            ERRORS.append(f"T5 — Attribut obligatoire '{attr}' absent de "
                          f"{F_GLOBAL.relative_to(REPO_ROOT)} (§ Couche 3)")
            all_ok = False
    if all_ok:
        print("✔ T5 — Attributs domaines_invalides + nombre_domaines_invalides "
              "présents dans la sentinelle globale")


# ---------------------------------------------------------------------------
# T6 — Icône couche 1 = mdi:alert-circle-outline (§ Couche 1)
# ---------------------------------------------------------------------------

def test_icon_couche1() -> None:
    files = domain_files()
    violations = []
    for path in sorted(files):
        content = read(path)
        # L'icône est déclarée statiquement
        if ICON_COUCHE1 not in content:
            violations.append(path.relative_to(REPO_ROOT))
    if violations:
        for v in violations:
            ERRORS.append(f"T6 — Icône '{ICON_COUCHE1}' absente de {v}")
    else:
        print(f"✔ T6 — Icône {ICON_COUCHE1} présente dans tous les capteurs domaine")


# ---------------------------------------------------------------------------
# T7 — Icône couche 3 = mdi:alert-octagon-outline (§ Couche 3)
# ---------------------------------------------------------------------------

def test_icon_couche3() -> None:
    content = read(F_GLOBAL)
    if not content:
        ERRORS.append(f"T7 — Fichier global inaccessible : "
                      f"{F_GLOBAL.relative_to(REPO_ROOT)}")
        return
    if ICON_COUCHE3 not in content:
        ERRORS.append(f"T7 — Icône '{ICON_COUCHE3}' absente de "
                      f"{F_GLOBAL.relative_to(REPO_ROOT)} (§ Couche 3)")
    else:
        print(f"✔ T7 — Icône {ICON_COUCHE3} présente dans la sentinelle globale")


# ---------------------------------------------------------------------------
# T8 — Absence de fallbacks silencieux | float(0) / | int(0) (§ Doctrine)
#
# Invariant : les capteurs domaine ne doivent jamais utiliser de fallback
# numérique non-none. Seuls | float(none) et | int(none) sont autorisés.
# Scope : fichiers domaine uniquement (global.yaml ne lit pas de helpers).
# ---------------------------------------------------------------------------

def test_no_silent_fallbacks() -> None:
    files = domain_files()
    violations = []
    for path in sorted(files):
        content = read(path)
        for pattern in FORBIDDEN_FALLBACKS:
            for line in content.splitlines():
                if line.strip().startswith("#"):
                    continue
                if pattern.search(line):
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"fallback silencieux «{line.strip()[:80]}»"
                    )
                    break
    if violations:
        for v in violations:
            ERRORS.append(f"T8 — Fallback silencieux interdit : {v}")
    else:
        print("✔ T8 — Aucun fallback silencieux | float(0) / | int(0) "
              "dans les capteurs domaine")


# ---------------------------------------------------------------------------
# T9 — Attribut 'cause' présent dans chaque capteur domaine (§ Attributs)
#
# Invariant : chaque capteur domaine doit exposer un attribut cause
# énumératif priorisé.
# ---------------------------------------------------------------------------

def test_cause_attribute_present() -> None:
    files = domain_files()
    violations = []
    for path in sorted(files):
        content = read(path)
        if not re.search(r"^\s*cause\s*:", content, re.MULTILINE):
            violations.append(path.relative_to(REPO_ROOT))
    if violations:
        for v in violations:
            ERRORS.append(f"T9 — Attribut 'cause' absent de {v} (§ Attributs)")
    else:
        print("✔ T9 — Attribut 'cause' présent dans tous les capteurs domaine")


# ---------------------------------------------------------------------------
# T10 — UI incluse dans les deux dashboards principaux (§ Couche 4)
#
# Invariant : alerte_configuration_invalide.yaml doit être incluse dans
# arsenal.yaml et navigation.yaml.
# ---------------------------------------------------------------------------

def test_ui_included_in_dashboards() -> None:
    # Pattern d'inclusion — chemin relatif possible sous plusieurs formes
    pattern = re.compile(r"alerte_configuration_invalide")
    all_ok = True
    for dashboard in DASHBOARDS:
        content = read(dashboard)
        if not content:
            ERRORS.append(f"T10 — Dashboard inaccessible : "
                          f"{dashboard.relative_to(REPO_ROOT)}")
            all_ok = False
            continue
        if not pattern.search(content):
            ERRORS.append(f"T10 — alerte_configuration_invalide non incluse dans "
                          f"{dashboard.relative_to(REPO_ROOT)} (§ Couche 4)")
            all_ok = False
    if all_ok:
        print("✔ T10 — alerte_configuration_invalide incluse dans les "
              "deux dashboards principaux")


# ---------------------------------------------------------------------------
# T11 — Groupe ne contient que des binary_sensor.parametres_invalides_* (§ Couche 2)
#
# Invariant : pas de capteur métier dans le groupe.
# ---------------------------------------------------------------------------

def test_group_only_valid_entities() -> None:
    content = read(F_GROUPE)
    if not content:
        ERRORS.append(f"T11 — Fichier groupe inaccessible : "
                      f"{F_GROUPE.relative_to(REPO_ROOT)}")
        return
    violations = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # Lignes commençant par "- " dans la section entities
        m = re.match(r"^-\s+(binary_sensor\.\S+)", stripped)
        if m:
            entity = m.group(1)
            if not entity.startswith("binary_sensor.parametres_invalides_"):
                violations.append(entity)
    if violations:
        for v in violations:
            ERRORS.append(f"T11 — Entité non conforme dans le groupe : {v} "
                          f"(seuls binary_sensor.parametres_invalides_* autorisés)")
    else:
        print("✔ T11 — Groupe ne contient que des "
              "binary_sensor.parametres_invalides_*")


# ---------------------------------------------------------------------------
# T12 — UI consomme uniquement binary_sensor.parametres_invalides_global (§ Couche 4)
#
# Invariant : la carte UI lit la sentinelle globale, jamais un capteur
# domaine directement.
# ---------------------------------------------------------------------------

def test_ui_consumes_only_global() -> None:
    content = read(F_UI)
    if not content:
        ERRORS.append(f"T12 — Fichier UI inaccessible : "
                      f"{F_UI.relative_to(REPO_ROOT)}")
        return

    # Cherche des références à des capteurs domaine spécifiques
    domain_refs = re.findall(
        r"binary_sensor\.parametres_invalides_(?!global)\S+",
        content
    )
    # Filtrer les commentaires
    domain_refs_active = [
        r for r in domain_refs
        if not any(
            line.strip().startswith("#")
            for line in content.splitlines()
            if r in line
        )
    ]
    if domain_refs_active:
        for ref in domain_refs_active:
            ERRORS.append(f"T12 — Référence directe à un capteur domaine dans "
                          f"l'UI (doit lire uniquement le global) : {ref}")
    else:
        print("✔ T12 — UI consomme uniquement binary_sensor.parametres_invalides_global")


# ---------------------------------------------------------------------------
# T13 — Fail-closed des sources non-numériques (input_datetime / input_boolean)
#
# Doctrine (§ Doctrine d'expression) : « toute source indisponible → invariant
# violé, pas d'optimisme silencieux ». Les input_number sont gardés par
# | float(none) + is none (le fallback | float(0) est déjà interdit par T8).
# Les input_datetime / input_boolean, eux, ne passent pas par float() : leur
# indisponibilité doit être testée EXPLICITEMENT dans le state, via une
# appartenance « <var> in ['unknown', 'unavailable', 'none', ''] » (littérale
# ou via une variable liste, ex. « <var> in indispos »).
#
# Ce test capte le trou PARAM-01 (climatisation inv9) : une source datetime /
# boolean lue dans le state mais jamais testée pour indisponibilité — l'état
# devient alors fail-OPEN (une borne absente n'est pas signalée). Scope : bloc
# `state` uniquement. Deux motifs sanctionnés :
#   1. « {% set VAR = states('input_datetime|boolean...') %} » sans « VAR in … »
#   2. « is_state('input_datetime|boolean...') » (collapse unavailable → False)
# ---------------------------------------------------------------------------

STATE_BLOCK_RE = re.compile(
    r"state\s*:\s*>\s*\n(.*?)(?:\n\s+attributes\s*:|\Z)",
    re.DOTALL,
)

BINDING_RE = re.compile(
    r"{%\s*set\s+(\w+)\s*=\s*states\(\s*['\"]"
    r"(input_(?:datetime|boolean)\.[^'\"]+)['\"]\s*\)\s*(?:\|\s*string\s*)?%}"
)

IS_STATE_NON_NUMERIC_RE = re.compile(
    r"is_state\(\s*['\"](input_(?:datetime|boolean)\.[^'\"]+)"
)


def extract_state_block(content: str) -> str:
    m = STATE_BLOCK_RE.search(content)
    return m.group(1) if m else ""


def test_non_numeric_sources_guarded() -> None:
    files = domain_files()
    violations = []
    for path in sorted(files):
        state = extract_state_block(read(path))
        if not state:
            continue
        # 1. Variables liées à states('input_datetime|boolean...') non testées
        for var, entity in BINDING_RE.findall(state):
            if not re.search(rf"\b{re.escape(var)}\s+in\b", state):
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : source non-numérique "
                    f"{entity} (var «{var}») lue dans le state sans garde "
                    f"d'indisponibilité (attendu : «{var} in ['unknown', "
                    f"'unavailable', 'none', '']»)"
                )
        # 2. is_state() direct sur une source datetime/boolean dans le state
        for m in IS_STATE_NON_NUMERIC_RE.finditer(state):
            violations.append(
                f"{path.relative_to(REPO_ROOT)} : is_state({m.group(1)}) dans le "
                f"state masque l'indisponibilité (lire la valeur brute via "
                f"states(...) puis tester explicitement l'appartenance)"
            )
    if violations:
        for v in violations:
            ERRORS.append(f"T13 — Source non-numérique non gardée (fail-closed) : {v}")
    else:
        print("✔ T13 — Sources non-numériques (datetime/boolean) du state "
              "gardées contre l'indisponibilité")


# ---------------------------------------------------------------------------
# T14 — Verrouillage local ECS : anti-refabrication numérique (chantier C24)
#
# Portée STRICTEMENT locale ECS — ce n'est PAS une interdiction transverse de
# tout `float(0)`. Les zéros canoniques et les usages hors périmètre ne sont
# PAS arbitrés ici. Deux axes seulement :
#
#   Axe 1 — fichiers cœur C24 contractualisés : aucune fabrication numérique
#           (`float(0)`/`float(0.0)`, `int(0)`, `else 0`, `get(..., 0)`,
#           `default(0)`).
#   Axe 2 — lecteurs directs des DEUX capteurs sécurisés : aucune lecture
#           `states('sensor.ecs_temperature_ballon_securisee')` ou
#           `states('sensor.ecs_consigne_chaudiere_securisee')` ne porte, sur
#           la même expression, un fallback fabriqué.
#
#           Tolérance : une garde `is_number` sur la MÊME lecture sécurisée,
#           dans la même expression Jinja et TEXTUELLEMENT AVANT la conversion,
#           rend le fallback structurellement inatteignable → conforme. Une
#           garde portant sur une autre valeur, placée après la conversion, ou
#           située dans une expression Jinja distincte (branche ne protégeant
#           pas la conversion) ne tolère PAS le fallback.
#
# Robustesse : chaque expression Jinja (`{% ... %}` / `{{ ... }}`) est
# reconstituée en ligne logique (commentaires retirés, blancs — dont les sauts
# de ligne — normalisés) avant application des motifs. Le découpage d'une
# expression sur plusieurs lignes ne contourne donc pas la règle.
# ---------------------------------------------------------------------------

CORE_C24_FILES = (
    "12_template_sensors/ecs/temperature.yaml",
    "12_template_sensors/ecs/consigne_effective.yaml",
    "10_scripts/ecs/cycle.yaml",
    "11_automations/ecs/reset_verrou_cycle.yaml",
)

SECURED_SENSORS = (
    "sensor.ecs_temperature_ballon_securisee",
    "sensor.ecs_consigne_chaudiere_securisee",
)

# Dossiers de configuration HA balayés pour l'axe 2 (le filtrage réel se fait
# sur la présence du nom d'entité sécurisée : périmètre = vrais lecteurs).
AXIS2_DIRS = (
    "10_scripts",
    "11_automations",
    "12_template_sensors",
    "14_mqtt_sensors",
    "18_lovelace",
)

_ZERO = r"0(?:\.0+)?"

# Fabrications numériques interdites dans les fichiers cœur C24 (axe 1).
FABRICATION_PATTERNS = (
    (re.compile(rf"\|\s*float\s*\(\s*{_ZERO}\s*\)"), "float(0)"),
    (re.compile(rf"\|\s*int\s*\(\s*{_ZERO}\s*\)"), "int(0)"),
    (re.compile(rf"\|\s*default\s*\(\s*{_ZERO}\s*\)"), "default(0)"),
    (re.compile(rf"\.get\(\s*[^)]*,\s*{_ZERO}\s*\)"), "get(..., 0)"),
    (re.compile(rf"\belse\s+{_ZERO}\b(?!\s*\.)"), "else 0"),
)

_SECURED_ALT = "|".join(re.escape(s) for s in SECURED_SENSORS)

# Lecture d'un capteur sécurisé suivie (même expression) d'un fallback fabriqué.
SECURED_READ_FABRICATION_RE = re.compile(
    rf"states\(\s*['\"](?:{_SECURED_ALT})['\"]\s*\)\s*"
    rf"\|\s*(?:float|int|default)\s*\(\s*{_ZERO}\s*\)"
)

# Garde `is_number` portant sur une lecture sécurisée (tolérance axe 2).
SECURED_ISNUMBER_GUARD_RE = re.compile(
    rf"states\(\s*['\"](?:{_SECURED_ALT})['\"]\s*\)\s*\|\s*is_number"
)

_JINJA_EXPR_RE = re.compile(r"\{%.*?%\}|\{\{.*?\}\}", re.DOTALL)
_JINJA_COMMENT_RE = re.compile(r"\{#.*?#\}", re.DOTALL)


def _strip_yaml_comments(text: str) -> str:
    """Retire les lignes de commentaire YAML (`#`) — cohérent avec T8/T13."""
    return "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("#")
    )


def expressions_jinja(text: str) -> list[str]:
    """Reconstitue chaque expression Jinja en ligne logique.

    Commentaires YAML (`#`) et Jinja (`{# #}`) retirés, blancs (dont sauts de
    ligne) normalisés en espaces : une expression découpée sur plusieurs lignes
    est réassemblée avant l'application des motifs.
    """
    code = _strip_yaml_comments(text)
    code = _JINJA_COMMENT_RE.sub(" ", code)
    flat = re.sub(r"\s+", " ", code)
    return _JINJA_EXPR_RE.findall(flat)


def violations_axe1(rel_path: str, text: str) -> list[str]:
    """Axe 1 — fabrications numériques interdites dans un fichier cœur C24."""
    out: list[str] = []
    for expr in expressions_jinja(text):
        for pattern, label in FABRICATION_PATTERNS:
            if pattern.search(expr):
                out.append(
                    f"{rel_path} : fabrication «{label}» interdite (fichier "
                    f"cœur C24) dans «{expr.strip()[:90]}»"
                )
    return out


def violations_axe2(rel_path: str, text: str) -> list[str]:
    """Axe 2 — refabrication sur une lecture directe d'un capteur sécurisé."""
    out: list[str] = []
    for expr in expressions_jinja(text):
        for m in SECURED_READ_FABRICATION_RE.finditer(expr):
            # Tolérance : garde is_number sur la même lecture sécurisée,
            # textuellement AVANT la conversion (fallback inatteignable).
            garde = SECURED_ISNUMBER_GUARD_RE.search(expr)
            if garde is not None and garde.start() < m.start():
                continue
            out.append(
                f"{rel_path} : lecture d'un capteur sécurisé avec fallback "
                f"fabriqué dans «{expr.strip()[:90]}» (attendu : float(none) "
                f"+ garde explicite, ou is_number avant conversion)"
            )
    return out


def test_ecs_secured_no_fabrication() -> None:
    violations: list[str] = []

    # Axe 1 — fichiers cœur C24 (chemins littéraux, périmètre fermé).
    for rel in CORE_C24_FILES:
        path = REPO_ROOT / rel
        if not path.is_file():
            violations.append(f"fichier cœur C24 introuvable : {rel}")
            continue
        violations.extend(violations_axe1(rel, read(path)))

    # Axe 2 — lecteurs directs des deux capteurs sécurisés (clé = nom d'entité).
    for d in AXIS2_DIRS:
        base = REPO_ROOT / d
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.yaml")):
            text = read(path)
            if not any(s in text for s in SECURED_SENSORS):
                continue
            rel = str(path.relative_to(REPO_ROOT))
            violations.extend(violations_axe2(rel, text))

    if violations:
        for v in violations:
            ERRORS.append(f"T14 — {v}")
    else:
        print("✔ T14 — Aucune refabrication numérique (cœur C24 + lecteurs "
              "des capteurs sécurisés) [verrouillage local ECS]")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_canonical_files_present,
    test_domain_sensors_unique_id,
    test_group_coherence,
    test_global_consumes_only_group,
    test_global_attributes,
    test_icon_couche1,
    test_icon_couche3,
    test_no_silent_fallbacks,
    test_cause_attribute_present,
    test_ui_included_in_dashboards,
    test_group_only_valid_entities,
    test_ui_consumes_only_global,
    test_non_numeric_sources_guarded,
    test_ecs_secured_no_fabrication,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Paramètres invalides v1.0\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT PARAMÈTRES INVALIDES NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT PARAMÈTRES INVALIDES CONFORME")
