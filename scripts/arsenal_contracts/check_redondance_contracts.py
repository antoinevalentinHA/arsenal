"""
Arsenal — Vérification contractuelle : Réconciliation des capteurs de contact (redondance)
Contrat : ARSENAL v2.2 — Réconciliation des capteurs de contact — Capteurs critiques
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "homeassistant"
ERRORS = []


def check(label: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  ✔ {label}")
    else:
        ERRORS.append(f"{label}{': ' + detail if detail else ''}")


# ---------------------------------------------------------------------------
# T1 — Input text de contexte déclaré dans 04_input_texts/ouvertures/
# ---------------------------------------------------------------------------
def test_t1_input_text_present():
    target = ROOT / "04_input_texts" / "ouvertures" / "contact_reconciliation_contexts.yaml"
    check(
        "T1 — input_text contexte réconciliation présent",
        target.is_file(),
        str(target),
    )


# ---------------------------------------------------------------------------
# T2 — Les 5 scripts canoniques présents dans reconciliation_redondance/
# ---------------------------------------------------------------------------
def test_t2_scripts_canoniques():
    base = ROOT / "10_scripts" / "ouvertures" / "reconciliation_redondance"
    scripts = [
        "traiter_source.yaml",
        "traiter_expiration.yaml",
        "appliquer_transition.yaml",
        "inhiber_tous.yaml",
        "lever_inhibition.yaml",
    ]
    for s in scripts:
        p = base / s
        check(f"T2 — script canonique présent : {s}", p.is_file(), str(p))


# ---------------------------------------------------------------------------
# T3 — Timer déclaré dans 08_timers/ouvertures/
# ---------------------------------------------------------------------------
def test_t3_timer_present():
    target = ROOT / "08_timers" / "ouvertures" / "contact_reconciliation.yaml"
    check(
        "T3 — timer réconciliation présent",
        target.is_file(),
        str(target),
    )


# ---------------------------------------------------------------------------
# T4 — Template sensor porteur déclaré dans 12_template_sensors/ouvertures/
# ---------------------------------------------------------------------------
def test_t4_template_sensor_present():
    target = ROOT / "12_template_sensors" / "ouvertures" / "capteurs_redondants.yaml"
    check(
        "T4 — template sensor capteurs_redondants présent",
        target.is_file(),
        str(target),
    )


# ---------------------------------------------------------------------------
# T5 — Attributs §7 tous exposés dans capteurs_redondants.yaml
# ---------------------------------------------------------------------------
def test_t5_attributs_observabilite():
    target = ROOT / "12_template_sensors" / "ouvertures" / "capteurs_redondants.yaml"
    if not target.is_file():
        ERRORS.append("T5 — fichier capteurs_redondants.yaml absent, test ignoré")
        return
    content = target.read_text(encoding="utf-8", errors="ignore")
    attributs = [
        "observed_event",
        "business_state",
        "reconciliation_status",
        "suspect_event",
        "last_corroborated_at",
        "last_divergence_at",
        "divergence_source",
    ]
    for attr in attributs:
        check(
            f"T5 — attribut §7 présent dans capteurs_redondants.yaml : {attr}",
            attr in content,
        )


# ---------------------------------------------------------------------------
# T6 — Format pipe-séparé 5 champs présent dans capteurs_redondants.yaml
# ---------------------------------------------------------------------------
def test_t6_format_contexte():
    target = ROOT / "12_template_sensors" / "ouvertures" / "capteurs_redondants.yaml"
    if not target.is_file():
        ERRORS.append("T6 — fichier capteurs_redondants.yaml absent, test ignoré")
        return
    content = target.read_text(encoding="utf-8", errors="ignore")
    # La signature runtime confirmée (L24) : les 5 champs nommés dans l'ordre
    signature = "reconciliation_status | business_state | pending_source | suspect_event | observed_event"
    check(
        "T6 — format contexte 5 champs pipe-séparé documenté dans capteurs_redondants.yaml",
        signature in content,
    )


# ---------------------------------------------------------------------------
# T7 — traiter_expiration.yaml encode divergent et on_non_corroborated (§6.2)
# ---------------------------------------------------------------------------
def test_t7_divergent_encode():
    target = ROOT / "10_scripts" / "ouvertures" / "reconciliation_redondance" / "traiter_expiration.yaml"
    if not target.is_file():
        ERRORS.append("T7 — traiter_expiration.yaml absent, test ignoré")
        return
    content = target.read_text(encoding="utf-8", errors="ignore")
    check(
        "T7 — traiter_expiration.yaml encode 'divergent'",
        "divergent" in content,
    )
    check(
        "T7 — traiter_expiration.yaml encode 'on_non_corroborated'",
        "on_non_corroborated" in content,
    )


# ---------------------------------------------------------------------------
# T8 — inhiber_tous.yaml encode inhibited et préserve business_state (§5.2)
# ---------------------------------------------------------------------------
def test_t8_inhibited_encode():
    target = ROOT / "10_scripts" / "ouvertures" / "reconciliation_redondance" / "inhiber_tous.yaml"
    if not target.is_file():
        ERRORS.append("T8 — inhiber_tous.yaml absent, test ignoré")
        return
    content = target.read_text(encoding="utf-8", errors="ignore")
    check(
        "T8 — inhiber_tous.yaml encode 'inhibited'",
        "inhibited" in content,
    )
    # Signature runtime confirmée (L64) : 'inhibited|' ~ current_business_state
    check(
        "T8 — inhiber_tous.yaml préserve current_business_state dans le contexte",
        "current_business_state" in content,
    )


# ---------------------------------------------------------------------------
# T9 — lever_inhibition.yaml encode stable, n'encode pas business_state = on (§5.3)
# ---------------------------------------------------------------------------
def test_t9_lever_inhibition():
    target = ROOT / "10_scripts" / "ouvertures" / "reconciliation_redondance" / "lever_inhibition.yaml"
    if not target.is_file():
        ERRORS.append("T9 — lever_inhibition.yaml absent, test ignoré")
        return
    content = target.read_text(encoding="utf-8", errors="ignore")
    check(
        "T9 — lever_inhibition.yaml encode 'stable'",
        "stable" in content,
    )
    # §5.3 : à la levée, les événements on reçus pendant inhibition sont abandonnés.
    # Le script NE DOIT PAS écrire 'stable|on' comme nouveau business_state.
    # Signature runtime confirmée (L76) : 'stable|' ~ current_business_state
    check(
        "T9 — lever_inhibition.yaml préserve current_business_state (pas de promotion on arbitraire)",
        "current_business_state" in content,
    )


# ---------------------------------------------------------------------------
# T10 — Aucun script hors reconciliation_redondance/ n'écrit l'input_text de contexte
# Scope : 10_scripts/ouvertures/ entier, hors reconciliation_redondance/
# ---------------------------------------------------------------------------
def test_t10_ecriture_input_text_hors_perimetre():
    scripts_root = ROOT / "10_scripts" / "ouvertures"
    autorise = ROOT / "10_scripts" / "ouvertures" / "reconciliation_redondance"

    if not scripts_root.is_dir():
        ERRORS.append("T10 — dossier 10_scripts/ouvertures/ absent")
        return

    # Patterns d'écriture réelle sur un input_text (service + cible dans rayon borné)
    # On cherche la coprésence de "input_text.set_value" et "contact_reconciliation"
    # dans un rayon de 300 chars — hors dossier autorisé.
    violations = []
    for p in scripts_root.rglob("*.yaml"):
        if not p.is_file():
            continue
        # Exclure le périmètre autorisé
        try:
            p.relative_to(autorise)
            continue
        except ValueError:
            pass
        content = p.read_text(encoding="utf-8", errors="ignore")
        # Recherche de la coprésence dans une fenêtre de 300 chars
        keyword = "contact_reconciliation"
        service = "input_text.set_value"
        idx = 0
        while True:
            pos = content.find(service, idx)
            if pos == -1:
                break
            window = content[max(0, pos - 150):pos + 150]
            if keyword in window:
                violations.append(str(p.relative_to(ROOT)))
            idx = pos + 1

    check(
        "T10 — aucune écriture sur input_text contact_reconciliation hors reconciliation_redondance/",
        len(violations) == 0,
        "fichiers en violation : " + ", ".join(violations) if violations else "",
    )


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------
TESTS = [
    test_t1_input_text_present,
    test_t2_scripts_canoniques,
    test_t3_timer_present,
    test_t4_template_sensor_present,
    test_t5_attributs_observabilite,
    test_t6_format_contexte,
    test_t7_divergent_encode,
    test_t8_inhibited_encode,
    test_t9_lever_inhibition,
    test_t10_ecriture_input_text_hors_perimetre,
]

if __name__ == "__main__":
    print("Arsenal — Vérification contractuelle : Réconciliation capteurs de contact\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT REDONDANCE NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT REDONDANCE CONFORME")