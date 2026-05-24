#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Réconciliation des capteurs de contact critiques
Contrat : ARSENAL v2.2 — Réconciliation des capteurs de contact — Capteurs critiques
Script  : scripts/arsenal_contracts/check_redondance_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal (chemin relatif depuis la racine du repo)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques du domaine redondance
# ---------------------------------------------------------------------------
F_CAPTEURS_REDONDANTS = REPO_ROOT / "12_template_sensors/ouvertures/capteurs_redondants.yaml"
F_DIAGNOSTIC          = REPO_ROOT / "12_template_sensors/ouvertures/diagnostic/redondance_contacts.yaml"
F_RECONCILIATION_CTX  = REPO_ROOT / "04_input_texts/ouvertures/contact_reconciliation_contexts.yaml"
F_MOTEUR              = REPO_ROOT / "11_automations/ouvertures/moteur_capteurs_redondants.yaml"
F_TRAITER_SOURCE      = REPO_ROOT / "10_scripts/ouvertures/reconciliation_redondance/traiter_source.yaml"
F_LEVER_INHIBITION    = REPO_ROOT / "10_scripts/ouvertures/reconciliation_redondance/lever_inhibition.yaml"
F_INHIBER_TOUS        = REPO_ROOT / "10_scripts/ouvertures/reconciliation_redondance/inhiber_tous.yaml"
F_SYSTEME_STABLE      = REPO_ROOT / "05_input_booleans/system/systeme_fiable.yaml"

# Sous-dossier fonctionnel restreint pour les tests comportementaux
DIR_AUTOMATIONS_OUVERTURES = REPO_ROOT / "11_automations/ouvertures"
DIR_SCRIPTS_REDONDANCE     = REPO_ROOT / "10_scripts/ouvertures/reconciliation_redondance"

# Valeurs normatives de reconciliation_status (§7 du contrat)
RECONCILIATION_STATUS_VALUES = ["stable", "quarantine", "divergent", "inhibited"]

# Plage admissible de T_corroboration en secondes (§4.2)
T_CORROBORATION_MIN = 2
T_CORROBORATION_MAX = 10

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def check(condition: bool, error_msg: str) -> None:
    if not condition:
        ERRORS.append(error_msg)


# ---------------------------------------------------------------------------
# T1 — Déclaration de input_boolean.systeme_stable
#
# Invariant (§5.1) : le signal de stabilité système est la référence normative
# pour l'inhibition. Il doit être déclaré dans 05_input_booleans/.
# Pattern : clé de mapping YAML (!include_dir_merge_named).
# ---------------------------------------------------------------------------

def test_systeme_stable_declared() -> None:
    content = read(F_SYSTEME_STABLE)
    if not content:
        ERRORS.append(
            f"T1 — Fichier manquant ou vide : {F_SYSTEME_STABLE.relative_to(REPO_ROOT)}"
        )
        return
    found = bool(re.search(r"^\s*systeme_stable\s*:", content, re.MULTILINE))
    check(
        found,
        f"T1 — input_boolean.systeme_stable non déclaré dans "
        f"{F_SYSTEME_STABLE.relative_to(REPO_ROOT)} "
        f"(clé de mapping attendue : 'systeme_stable:')",
    )
    if found:
        print("✔ T1 — input_boolean.systeme_stable déclaré")


# ---------------------------------------------------------------------------
# T2 — Présence des fichiers canoniques du domaine
#
# Invariant structurel : les fichiers identifiés comme canonical runtime
# doivent exister. Leur absence est une régression contractuelle immédiate.
# ---------------------------------------------------------------------------

CANONICAL_FILES = {
    "T2a": F_CAPTEURS_REDONDANTS,
    "T2b": F_DIAGNOSTIC,
    "T2c": F_RECONCILIATION_CTX,
    "T2d": F_MOTEUR,
    "T2e": F_TRAITER_SOURCE,
    "T2f": F_LEVER_INHIBITION,
    "T2g": F_INHIBER_TOUS,
}

def test_canonical_files_present() -> None:
    all_ok = True
    for label, path in CANONICAL_FILES.items():
        if not path.is_file():
            ERRORS.append(
                f"{label} — Fichier canonique manquant : {path.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T2 — Tous les fichiers canoniques du domaine redondance sont présents")


# ---------------------------------------------------------------------------
# T3 — Attributs d'observabilité présents dans le template sensor source
#
# Invariant (§7) : capteurs_redondants.yaml doit exposer les attributs
# reconciliation_status et business_state. Ce sont les couches d'état
# normatives produites par le moteur de réconciliation.
# Scope restreint : fichier source uniquement.
# ---------------------------------------------------------------------------

REQUIRED_ATTRS_SOURCE = ["reconciliation_status", "business_state"]

def test_observability_attrs_in_source() -> None:
    content = read(F_CAPTEURS_REDONDANTS)
    if not content:
        ERRORS.append(
            f"T3 — Fichier source inaccessible : {F_CAPTEURS_REDONDANTS.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for attr in REQUIRED_ATTRS_SOURCE:
        if attr not in content:
            ERRORS.append(
                f"T3 — Attribut '{attr}' absent de "
                f"{F_CAPTEURS_REDONDANTS.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T3 — Attributs d'observabilité présents dans le template sensor source")


# ---------------------------------------------------------------------------
# T4 — Attributs d'observabilité complets dans le fichier de diagnostic
#
# Invariant (§7) : le fichier de diagnostic doit exposer tous les attributs
# normatifs, dont suspect_event, observed_event, last_corroborated_at,
# last_divergence_at, divergence_source — en plus des attributs de base.
# Scope restreint : fichier de diagnostic uniquement.
# ---------------------------------------------------------------------------

REQUIRED_ATTRS_DIAGNOSTIC = [
    "reconciliation_status",
    "business_state",
    "suspect_event",
    "observed_event",
    "last_corroborated_at",
    "last_divergence_at",
    "divergence_source",
]

def test_observability_attrs_in_diagnostic() -> None:
    content = read(F_DIAGNOSTIC)
    if not content:
        ERRORS.append(
            f"T4 — Fichier de diagnostic inaccessible : {F_DIAGNOSTIC.relative_to(REPO_ROOT)}"
        )
        return
    all_ok = True
    for attr in REQUIRED_ATTRS_DIAGNOSTIC:
        if attr not in content:
            ERRORS.append(
                f"T4 — Attribut normatif '{attr}' absent de "
                f"{F_DIAGNOSTIC.relative_to(REPO_ROOT)}"
            )
            all_ok = False
    if all_ok:
        print("✔ T4 — Attributs d'observabilité complets dans le fichier de diagnostic")


# ---------------------------------------------------------------------------
# T5 — Cohérence source + diagnostic sur les 4 valeurs de reconciliation_status
#
# Invariant (§7, instruction Antoine) :
#   - capteurs_redondants.yaml produit les 4 valeurs normatives
#     (définition source — contrat runtime produit ici)
#   - diagnostic/redondance_contacts.yaml interprète les 4 valeurs
#     (consommation diagnostic — garantit que l'UI sait les lire)
# Les deux vérifications sont requises.
# ---------------------------------------------------------------------------

def test_reconciliation_status_values_coherence() -> None:
    src_content  = read(F_CAPTEURS_REDONDANTS)
    diag_content = read(F_DIAGNOSTIC)

    missing_src  = []
    missing_diag = []

    for val in RECONCILIATION_STATUS_VALUES:
        if val not in src_content:
            missing_src.append(val)
        if val not in diag_content:
            missing_diag.append(val)

    if missing_src:
        ERRORS.append(
            f"T5 — Valeurs de reconciliation_status absentes du fichier source "
            f"({F_CAPTEURS_REDONDANTS.relative_to(REPO_ROOT)}) : {missing_src}"
        )
    if missing_diag:
        ERRORS.append(
            f"T5 — Valeurs de reconciliation_status absentes du fichier de diagnostic "
            f"({F_DIAGNOSTIC.relative_to(REPO_ROOT)}) : {missing_diag}"
        )
    if not missing_src and not missing_diag:
        print(
            "✔ T5 — Les 4 valeurs normatives de reconciliation_status sont cohérentes "
            "(source + diagnostic)"
        )


# ---------------------------------------------------------------------------
# T6 — T_corroboration dans la plage admissible [2, 10] secondes
#
# Invariant (§4.2) : toute valeur encodée en dur pour T_corroboration
# doit être comprise entre 2 et 10 secondes inclus.
# Scope restreint : fichiers canoniques du domaine redondance uniquement.
# Méthode : extraction de tous les littéraux numériques adjacents à
# 'corroboration' dans un rayon de 80 caractères.
# ---------------------------------------------------------------------------

def test_t_corroboration_in_range() -> None:
    files_to_scan = [
        F_CAPTEURS_REDONDANTS,
        F_MOTEUR,
        F_TRAITER_SOURCE,
        F_LEVER_INHIBITION,
        F_INHIBER_TOUS,
    ]
    violations = []
    for path in files_to_scan:
        content = read(path)
        if not content:
            continue
        # Cherche des entiers isolés dans un contexte 'corroboration'
        # Pattern : nombre entier dans un rayon de 80 chars autour du mot
        windows = re.findall(
            r".{0,80}corroboration.{0,80}", content, re.IGNORECASE
        )
        for window in windows:
            for match in re.finditer(r"\b(\d+)\b", window):
                val = int(match.group(1))
                # Exclure les numéros de version (ex. v2, 2026…) > 100
                if val > 100:
                    continue
                # Exclure 0 (valeur neutre / désactivation)
                if val == 0:
                    continue
                if not (T_CORROBORATION_MIN <= val <= T_CORROBORATION_MAX):
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"valeur {val}s hors plage [{T_CORROBORATION_MIN}, {T_CORROBORATION_MAX}]"
                        f" — contexte : «{window.strip()[:120]}»"
                    )
    if violations:
        for v in violations:
            ERRORS.append(f"T6 — T_corroboration hors plage : {v}")
    else:
        print(
            f"✔ T6 — T_corroboration dans la plage admissible "
            f"[{T_CORROBORATION_MIN}, {T_CORROBORATION_MAX}]s"
        )


# ---------------------------------------------------------------------------
# T7 — T_quarantaine = T_corroboration (pas de dissociation)
#
# Invariant (§6.1) : les deux durées doivent être intentionnellement alignées.
# Une dissociation sans justification fonctionnelle explicite est proscrite.
# Méthode : extraction de la valeur numérique associée à chaque terme
# dans le fichier source, vérification d'égalité.
# Scope : capteurs_redondants.yaml + traiter_source.yaml.
# ---------------------------------------------------------------------------

def _extract_duration_values(content: str, keyword: str) -> list[int]:
    """Extrait les entiers dans un rayon de 80 chars autour d'un mot-clé."""
    values = []
    windows = re.findall(
        rf".{{0,80}}{keyword}.{{0,80}}", content, re.IGNORECASE
    )
    for window in windows:
        for m in re.finditer(r"\b(\d+)\b", window):
            val = int(m.group(1))
            if 1 <= val <= 100:  # plage sémantiquement plausible pour une durée
                values.append(val)
    return values


def test_t_quarantaine_equals_t_corroboration() -> None:
    files_to_scan = [F_CAPTEURS_REDONDANTS, F_TRAITER_SOURCE, F_MOTEUR]
    all_corroboration: list[int] = []
    all_quarantaine:   list[int] = []

    for path in files_to_scan:
        content = read(path)
        if not content:
            continue
        all_corroboration.extend(_extract_duration_values(content, "corroboration"))
        all_quarantaine.extend(_extract_duration_values(content, "quarantaine"))

    if not all_corroboration and not all_quarantaine:
        # Aucune valeur encodée en dur — non testable, pas une violation
        print("✔ T7 — T_quarantaine / T_corroboration : aucune valeur encodée en dur (non testable)")
        return

    # Si des valeurs existent des deux côtés, elles doivent être identiques
    unique_c = set(all_corroboration)
    unique_q = set(all_quarantaine)

    if len(unique_c) > 1:
        ERRORS.append(
            f"T7 — Valeurs de T_corroboration incohérentes entre fichiers : {sorted(unique_c)}"
        )
        return
    if len(unique_q) > 1:
        ERRORS.append(
            f"T7 — Valeurs de T_quarantaine incohérentes entre fichiers : {sorted(unique_q)}"
        )
        return

    if unique_c and unique_q and unique_c != unique_q:
        ERRORS.append(
            f"T7 — Dissociation interdite : T_corroboration={sorted(unique_c)[0]}s "
            f"≠ T_quarantaine={sorted(unique_q)[0]}s (§6.1)"
        )
    else:
        val = sorted(unique_c or unique_q)[0]
        print(f"✔ T7 — T_quarantaine = T_corroboration = {val}s")


# ---------------------------------------------------------------------------
# T8 — Absence de timer fixe substituant systeme_stable dans le moteur
#
# Invariant (§5.1) : toute substitution de input_boolean.systeme_stable
# par un timer fixe (delay:/for:) dans le moteur ou les scripts de
# réconciliation est une déviation contractuelle.
# Scope restreint : fichiers canoniques du domaine redondance uniquement.
# Exclusion explicite : les timers de corroboration/quarantaine sont légitimes.
# ---------------------------------------------------------------------------

# Pattern d'un timer fixe d'inhibition post-startup : delay/for avec une durée
# en dehors d'un contexte de corroboration ou quarantaine.
_TIMER_FIXED_PATTERN = re.compile(
    r"(delay|for)\s*:\s*\n?\s*(seconds|minutes|hours)\s*:\s*\d+",
    re.IGNORECASE,
)
_CORROBORATION_CONTEXT = re.compile(
    r"corroboration|quarantaine|T_corr|T_quar",
    re.IGNORECASE,
)

def test_no_fixed_timer_substituting_systeme_stable() -> None:
    """
    Vérifie qu'aucun timer fixe ne remplace systeme_stable comme garde
    d'inhibition post-startup dans les fichiers du domaine redondance.
    Un delay/for légitime doit apparaître dans un contexte de corroboration
    ou quarantaine. Un delay/for sans ce contexte dans un fichier qui
    consomme aussi systeme_stable est suspect.
    """
    files_to_scan = [F_MOTEUR, F_TRAITER_SOURCE, F_LEVER_INHIBITION, F_INHIBER_TOUS]
    violations = []

    for path in files_to_scan:
        content = read(path)
        if not content:
            continue

        # Le fichier consomme-t-il systeme_stable ?
        uses_systeme_stable = "systeme_stable" in content

        for m in _TIMER_FIXED_PATTERN.finditer(content):
            start = max(0, m.start() - 200)
            end   = min(len(content), m.end() + 200)
            window = content[start:end]

            # Timer dans un contexte corroboration/quarantaine → légitime
            if _CORROBORATION_CONTEXT.search(window):
                continue

            # Timer fixe hors contexte de corroboration dans un fichier
            # qui utilise systeme_stable → substitution suspecte
            if uses_systeme_stable:
                violations.append(
                    f"{path.relative_to(REPO_ROOT)} : timer fixe hors contexte "
                    f"corroboration/quarantaine — «{m.group(0).strip()}»"
                )

    if violations:
        for v in violations:
            ERRORS.append(f"T8 — Timer fixe substituant systeme_stable : {v}")
    else:
        print("✔ T8 — Aucun timer fixe ne substitue input_boolean.systeme_stable")


# ---------------------------------------------------------------------------
# T9 — Le moteur de réconciliation consomme systeme_stable
#
# Invariant (§5.2) : le moteur et/ou les scripts souverains doivent
# référencer input_boolean.systeme_stable comme condition d'inhibition.
# Scope : moteur + traiter_source (seuls fichiers où l'inhibition est active).
# ---------------------------------------------------------------------------

def test_moteur_consumes_systeme_stable() -> None:
    files_to_check = {
        "moteur": F_MOTEUR,
        "traiter_source": F_TRAITER_SOURCE,
    }
    all_ok = True
    for label, path in files_to_check.items():
        content = read(path)
        if not content:
            ERRORS.append(
                f"T9 — Fichier inaccessible ({label}) : {path.relative_to(REPO_ROOT)}"
            )
            all_ok = False
            continue
        if "systeme_stable" not in content:
            ERRORS.append(
                f"T9 — input_boolean.systeme_stable absent de {label} "
                f"({path.relative_to(REPO_ROOT)}) — inhibition post-startup non garantie"
            )
            all_ok = False
    if all_ok:
        print(
            "✔ T9 — input_boolean.systeme_stable consommé par le moteur "
            "et traiter_source"
        )


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_systeme_stable_declared,
    test_canonical_files_present,
    test_observability_attrs_in_source,
    test_observability_attrs_in_diagnostic,
    test_reconciliation_status_values_coherence,
    test_t_corroboration_in_range,
    test_t_quarantaine_equals_t_corroboration,
    test_no_fixed_timer_substituting_systeme_stable,
    test_moteur_consumes_systeme_stable,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : redondance (capteurs critiques)\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT REDONDANCE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT REDONDANCE CONFORME")
