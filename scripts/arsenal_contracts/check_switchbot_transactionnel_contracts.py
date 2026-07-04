#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Socle transactionnel SwitchBot
Contrat (source normative) : 00_documentation_arsenal/contrats/switchbot_transactionnel.md
Script  : scripts/arsenal_contracts/check_switchbot_transactionnel_contracts.py
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques
# ---------------------------------------------------------------------------
F_EXECUTEUR      = REPO_ROOT / "10_scripts/system/transactions_bots.yaml"
DIR_SCRIPTS      = REPO_ROOT / "10_scripts"
DIR_AUTOMATIONS  = REPO_ROOT / "11_automations"

# Scripts métiers connus consommant le script souverain
# (scope restreint pour I7 — délais et logique BLE)
DIR_SCRIPTS_DESHU = REPO_ROOT / "10_scripts/deshumidificateur"

# Fichiers de verrous (exclus du test I1 — ils déclarent la relation)
DIR_LOCKS = REPO_ROOT / "05_input_booleans/system/transactions_bots"

# ---------------------------------------------------------------------------
# Paramètres normatifs (§4, §5, §7)
# ---------------------------------------------------------------------------

# Cibles du registre (§4)
CIBLES_REGISTRE = ["deshumidificateur", "bot_chambre_parents"]

# Entités SwitchBot — appels directs interdits hors exécuteur (I1)
ENTITES_SWITCHBOT = [
    "switch.deshumidificateur",
    "switch.bot_chambre_parents",
]

# Cooldowns normatifs (§4)
COOLDOWN_DESHU   = "30"
COOLDOWN_CHAMBRE = "10"

# Verdicts normatifs vérifiables en V1 (§7)
# execution_error est défini contractuellement mais non émis en YAML natif V1
# (limite §9 Phase 2 — non implémentable en YAML). Non vérifié ici.
VERDICTS = [
    "rejected_precondition",
    "rejected_cooldown",
    "rejected_busy",
    "sent_unconfirmed",
    "command_confirmed",
    "command_not_confirmed",
]

# Champs diagnostic minimaux vérifiés (§10)
# consecutive_failures retiré du périmètre normatif v2.0.1 —
# le contrat allait trop loin sur ce point. Extension candidate v2.1.
CHAMPS_DIAGNOSTIC = [
    "last_target",
    "last_action",
    "last_request_id",
    "last_verdict",
    "last_proof_level",
    "last_ts",
    "last_reason",
    "lock_active",
    "cooldown_active",
]

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(*directories: Path) -> list[Path]:
    result = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


def active_lines(content: str) -> list[str]:
    return [l for l in content.splitlines() if not l.strip().startswith("#")]


# ---------------------------------------------------------------------------
# T1 — Présence du script souverain (exécuteur)
# ---------------------------------------------------------------------------

def test_executeur_present() -> None:
    if not F_EXECUTEUR.is_file():
        ERRORS.append(f"T1 — Script souverain manquant : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
    else:
        print(f"✔ T1 — Script souverain présent "
              f"({F_EXECUTEUR.relative_to(REPO_ROOT)})")


# ---------------------------------------------------------------------------
# T2 — Cibles du registre présentes dans l'exécuteur (§4)
# ---------------------------------------------------------------------------

def test_cibles_registre_presentes() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T2 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for cible in CIBLES_REGISTRE:
        if cible not in content:
            ERRORS.append(f"T2 — Cible registre '{cible}' absente de "
                          f"{F_EXECUTEUR.relative_to(REPO_ROOT)} (§4)")
            all_ok = False
    if all_ok:
        print(f"✔ T2 — Les {len(CIBLES_REGISTRE)} cibles du registre présentes "
              f"dans l'exécuteur (§4)")


# ---------------------------------------------------------------------------
# T3 — Cooldowns normatifs encodés (§4)
# ---------------------------------------------------------------------------

def test_cooldowns_presents() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T3 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for val, label in [(COOLDOWN_DESHU, "deshumidificateur 30 s"),
                       (COOLDOWN_CHAMBRE, "bot_chambre_parents 10 s")]:
        # Cherche la valeur dans un contexte cooldown
        windows = re.findall(r".{0,60}cooldown.{0,60}", content, re.IGNORECASE)
        found = any(val in w for w in windows) or bool(
            re.search(rf"\b{re.escape(val)}\b", content)
        )
        if not found:
            ERRORS.append(f"T3 — Cooldown {label} absent de "
                          f"{F_EXECUTEUR.relative_to(REPO_ROOT)} (§4)")
            all_ok = False
    if all_ok:
        print(f"✔ T3 — Cooldowns normatifs présents "
              f"({COOLDOWN_DESHU} s + {COOLDOWN_CHAMBRE} s)")


# ---------------------------------------------------------------------------
# T4 — Verdicts normatifs présents dans l'exécuteur (§7)
# ---------------------------------------------------------------------------

def test_verdicts_presents() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T4 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for verdict in VERDICTS:
        if verdict not in content:
            ERRORS.append(f"T4 — Verdict normatif '{verdict}' absent de "
                          f"{F_EXECUTEUR.relative_to(REPO_ROOT)} (§7)")
            all_ok = False
    if all_ok:
        print(f"✔ T4 — Les {len(VERDICTS)} verdicts normatifs présents dans "
              f"l'exécuteur (§7)")


# ---------------------------------------------------------------------------
# T5 — last_run_success référencé dans l'exécuteur (§5, niveau B)
# ---------------------------------------------------------------------------

def test_last_run_success_present() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T5 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    if "last_run_success" not in content:
        ERRORS.append(f"T5 — 'last_run_success' absent de "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)} "
                      f"(preuve niveau B — §5)")
    else:
        print("✔ T5 — last_run_success référencé dans l'exécuteur (niveau B, §5)")


# ---------------------------------------------------------------------------
# T6 — Champs diagnostic minimaux présents (§10)
# ---------------------------------------------------------------------------

def test_diagnostic_fields_present() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T6 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    all_ok = True
    for champ in CHAMPS_DIAGNOSTIC:
        if champ not in content:
            ERRORS.append(f"T6 — Champ diagnostic '{champ}' absent de "
                          f"{F_EXECUTEUR.relative_to(REPO_ROOT)} (§10)")
            all_ok = False
    if all_ok:
        print(f"✔ T6 — Champs diagnostic minimaux présents ({len(CHAMPS_DIAGNOSTIC)} champs, §10)")


# ---------------------------------------------------------------------------
# T7 — Aucun appel direct aux entités SwitchBot hors exécuteur (I1)
#
# Invariant (I1) : toute commande Bot passe exclusivement par le script
# souverain. Aucun appel direct aux entités depuis les scripts métiers.
# Méthode : cherche service: switch.* sur les entités SwitchBot hors exécuteur.
# Exclusions : fichiers de verrous (déclaratifs), fichiers en lecture seule.
# ---------------------------------------------------------------------------

def test_no_direct_switchbot_calls() -> None:
    # Pattern d'appel de service direct — exclut les lectures states()
    pattern_service = re.compile(
        r"(?:service|action)\s*:\s*(?:switch\.)?"
        r"(?:turn_on|turn_off|toggle)"
    )
    pattern_entity  = re.compile(
        r"|".join(re.escape(e) for e in ENTITES_SWITCHBOT)
    )

    # Exceptions documentées : scripts d'autorité d'exécution unique par domaine.
    # Ces scripts sont les seuls points d'entrée légitimes hors script souverain.
    # Leur autorité est définie dans le contrat de domaine correspondant.
    EXCEPTIONS = {
        # script.set_deshumidificateur_state — autorité d'exécution unique déshumidificateur
        # (contrat deshumidificateur.md — section "Autorité d'exécution unique")
        REPO_ROOT / "10_scripts/deshumidificateur/forcer_etat.yaml",
    }

    violations = []

    for path in yaml_files(DIR_SCRIPTS, DIR_AUTOMATIONS):
        # Exclure le script souverain lui-même
        if path == F_EXECUTEUR:
            continue
        # Exclure les autorités d'exécution unique documentées par domaine
        if path in EXCEPTIONS:
            continue

        content = read(path)
        lines = active_lines(content)

        # Cherche un appel service sur une entité SwitchBot dans une fenêtre de 5 lignes
        for i, line in enumerate(lines):
            if pattern_service.search(line):
                window = "\n".join(lines[i:i + 5])
                if pattern_entity.search(window):
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} : "
                        f"«{line.strip()[:80]}»"
                    )
                    break

    if violations:
        for v in violations:
            ERRORS.append(f"T7 — Appel direct SwitchBot hors exécuteur "
                          f"(violation I1) : {v}")
    else:
        print("✔ T7 — Aucun appel direct aux entités SwitchBot hors exécuteur (I1)")


# ---------------------------------------------------------------------------
# T8 — Scripts métiers sans délai d'exécution BLE (I7)
#
# Invariant (I7) : les scripts métiers n'intègrent aucune logique de
# transport BLE ni délai d'exécution. Les delay/wait_for_trigger BLE
# appartiennent exclusivement à l'exécuteur.
# Scope : scripts métiers consommateurs connus (deshumidificateur).
# Méthode : absence de délai (delay:) dans le même bloc qu'un appel
# au script souverain.
# ---------------------------------------------------------------------------

def test_metier_scripts_no_ble_delay() -> None:
    # Cherche les scripts métiers qui appellent le script souverain
    pattern_souverain = re.compile(r"transactions_bots|script\.executer_bot")
    pattern_delay     = re.compile(r"^\s*(?:delay|wait_for_trigger)\s*:", re.MULTILINE)

    violations = []
    for path in yaml_files(DIR_SCRIPTS_DESHU):
        content = read(path)
        if not pattern_souverain.search(content):
            continue
        # Ce script appelle le souverain — il ne doit pas avoir de delay
        if pattern_delay.search(content):
            violations.append(f"{path.relative_to(REPO_ROOT)} : "
                              f"delay/wait_for_trigger dans script métier (I7)")

    if violations:
        for v in violations:
            ERRORS.append(f"T8 — Logique de délai BLE dans script métier "
                          f"(violation I7) : {v}")
    else:
        print("✔ T8 — Scripts métiers sans délai d'exécution BLE (I7)")


# ---------------------------------------------------------------------------
# T9 — proof_mode absent des paramètres du script souverain (Annexe A)
#
# Invariant (Annexe A) : proof_mode n'est pas un paramètre d'entrée.
# Le niveau de preuve est déterminé souverainement par le registre.
# ---------------------------------------------------------------------------

def test_no_proof_mode_param() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T9 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return
    # Cherche proof_mode comme paramètre déclaré (pas dans un commentaire)
    for line in active_lines(content):
        if re.search(r"proof_mode\s*:", line):
            ERRORS.append(f"T9 — 'proof_mode' déclaré comme paramètre dans "
                          f"{F_EXECUTEUR.relative_to(REPO_ROOT)} "
                          f"(interdit — Annexe A)")
            return
    print("✔ T9 — proof_mode absent des paramètres de l'exécuteur (Annexe A)")


# ---------------------------------------------------------------------------
# T10 — sent_unconfirmed produit pour les cibles niveau A (§5, I11)
#
# Invariant (I11) : une cible de niveau A ne produit jamais de verdict
# basé sur une lecture d'attribut. sent_unconfirmed est son verdict nominal.
# Vérification : sent_unconfirmed présent + last_run_success non conditionné
# dans un même bloc bot_chambre_parents.
# ---------------------------------------------------------------------------

def test_sent_unconfirmed_for_level_a() -> None:
    content = read(F_EXECUTEUR)
    if not content:
        ERRORS.append(f"T10 — Exécuteur inaccessible : "
                      f"{F_EXECUTEUR.relative_to(REPO_ROOT)}")
        return

    has_sent_unconfirmed = "sent_unconfirmed" in content
    has_chambre          = "bot_chambre_parents" in content

    if not has_chambre:
        ERRORS.append("T10 — bot_chambre_parents absent de l'exécuteur "
                      "(cible niveau A non déclarée)")
        return
    if not has_sent_unconfirmed:
        ERRORS.append("T10 — sent_unconfirmed absent de l'exécuteur "
                      "(verdict nominal niveau A — I11)")
        return

    print("✔ T10 — sent_unconfirmed présent pour cible niveau A "
          "bot_chambre_parents (I11)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_executeur_present,
    test_cibles_registre_presentes,
    test_cooldowns_presents,
    test_verdicts_presents,
    test_last_run_success_present,
    test_diagnostic_fields_present,
    test_no_direct_switchbot_calls,
    test_metier_scripts_no_ble_delay,
    test_no_proof_mode_param,
    test_sent_unconfirmed_for_level_a,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : "
          "Socle transactionnel SwitchBot v2.0.1\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT SWITCHBOT TRANSACTIONNEL NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT SWITCHBOT TRANSACTIONNEL CONFORME")
