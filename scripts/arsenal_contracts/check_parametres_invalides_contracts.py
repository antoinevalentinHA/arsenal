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
