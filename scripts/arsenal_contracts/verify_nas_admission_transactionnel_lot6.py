#!/usr/bin/env python3
"""
Arsenal — Vérification statique : Socle transactionnel NAS — C51 Lot 6
Contrat (source normative) : 00_documentation_arsenal/contrats/nas_transactionnel.md
Chantier : 00_documentation_arsenal/audits/04_chantiers/transverses/
           c51_commandabilite_nas.md (Lot 6 — extension RELEASE_DIFF)

Portee et statut CI (important, lire avant d'etendre ce script)
-----------------------------------------------------------------
Ce fichier est un verificateur statique autonome, calque sur le patron
`scripts/arsenal_contracts/check_*_contracts.py` (memes conventions :
ERRORS/print, run direct, exit 1 si erreur). Il est INTENTIONNELLEMENT
NON prefixe `check_` et NON enregistre dans `.github/workflows/contracts_all.yml`
ni dans `check_ci_coverage_registry.py` (INTEG-1) : le cablage CI complet
implique de mettre a jour `00_documentation_arsenal/audits/
REGISTRE_COUVERTURE_VERIFICATION.md` (compteurs §2/§3, journal §8 date),
un registre hors perimetre strict du Lot 6 (cf. mission Lot 6, §1 et §13 —
diff limite au helper/script/diagnostic/doc C51). Cablage CI complet laisse
en suite explicite (voir RAPPORT de la PR Lot 6, "Ce qui reste a prouver
terrain" / suites possibles) — ce script reste executable manuellement des
aujourd'hui :

  python3 scripts/arsenal_contracts/verify_nas_admission_transactionnel_lot6.py

Verifie, pour l'extension RELEASE_DIFF (Lot 6) ET pour l'absence de
regression sur AUDIT (Lot 5, non modifie) :
  - operation figee (AUDIT / RELEASE_DIFF) dans chaque script
  - topic exact, QoS 1, retain=false
  - source fixe "arsenal" (litteral, non interpole)
  - aucun parametre metier libre (--couple, chemin, argument shell,
    selection de release, parametre batch)
  - helper transactionnel dedie et distinct par operation (aucun partage)
  - cleanup systematique de l'ancrage (y compris hors cas nominal)
  - corrélation sur request_id ET operation dans l'attente du resultat
  - 'admitted' jamais traite comme verdict terminal
  - vocabulaire de verdict terminal complet et correct (contrat §10)
  - aucune lecture du resultat metier (sensor.arsenal_self_audit_statut /
    sensor.arsenal_nas_release_diff_statut) pour conclure la transaction
  - AUDIT (Lot 5) inchange fonctionnellement (memes invariants relus)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def read_active(path: Path) -> str:
    """Contenu du fichier hors lignes entièrement commentées (`# ...`).

    Les fichiers Arsenal portent des en-têtes documentaires abondants qui
    mentionnent volontairement l'autre opération/l'autre helper à titre
    explicatif (ex. « --couple non exposé », « ne référence jamais
    input_text.nas_admission_req_audit »). Les tests de couplage/paramètres
    interdits doivent porter sur le code YAML actif, pas sur la prose.
    """
    return "\n".join(
        line for line in read(path).splitlines()
        if not line.strip().startswith("#")
    )


# ---------------------------------------------------------------------------
# Fichiers canoniques
# ---------------------------------------------------------------------------

F_SCRIPT_AUDIT = ROOT / "10_scripts/system/nas_admission_demander_audit.yaml"
F_SCRIPT_RELEASE_DIFF = ROOT / "10_scripts/system/nas_admission_demander_release_diff.yaml"

F_HELPER_AUDIT = ROOT / "04_input_texts/system/nas_admission/request_id_transactionnels.yaml"
F_HELPER_RELEASE_DIFF = ROOT / "04_input_texts/system/nas_admission/request_id_transactionnels_release_diff.yaml"

F_RAW_SENSOR = ROOT / "14_mqtt_sensors/system/nas_admission_result_raw.yaml"
F_CORRELATION = ROOT / "12_template_sensors/system/nas_admission/nas_admission_result_correlation.yaml"

F_DIAG_AUDIT = ROOT / "12_template_sensors/system/nas_admission/nas_admission_audit_etat_transaction.yaml"
F_DIAG_RELEASE_DIFF = ROOT / "12_template_sensors/system/nas_admission/nas_admission_release_diff_etat_transaction.yaml"

TOPIC_COMMAND = "arsenal/nas/admission/command"

VERDICTS_REJET = [
    "rejected_precondition",
    "rejected_stale",
    "rejected_busy",
    "rejected_conflict",
    "admission_unavailable",
]
VERDICTS_TERMINAUX = VERDICTS_REJET + ["completed", "technical_failure"]

FORBIDDEN_BUSINESS_PARAMS = ["--couple", "--dry-run", "--force", "--limit", "--strict"]


# ---------------------------------------------------------------------------
# Helpers de test communs (parametres par operation)
# ---------------------------------------------------------------------------

OPERATIONS = {
    "AUDIT": {
        "script": F_SCRIPT_AUDIT,
        "helper_entity": "input_text.nas_admission_req_audit",
        "business_sensor": "sensor.arsenal_self_audit_statut",
        "other_helper_entity": "input_text.nas_admission_req_release_diff",
    },
    "RELEASE_DIFF": {
        "script": F_SCRIPT_RELEASE_DIFF,
        "helper_entity": "input_text.nas_admission_req_release_diff",
        "business_sensor": "sensor.arsenal_nas_release_diff_statut",
        "other_helper_entity": "input_text.nas_admission_req_audit",
    },
}


def test_scripts_present() -> None:
    for op, cfg in OPERATIONS.items():
        if not cfg["script"].is_file():
            error(f"T1 — Script {op} manquant : {cfg['script'].relative_to(ROOT)}")
    if not ERRORS:
        ok("T1 — Les deux scripts exécutifs (AUDIT, RELEASE_DIFF) sont présents")


def test_operation_fixee() -> None:
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        if not text:
            continue
        if f'"operation": "{op}"' not in text:
            error(f"T2 — {op} : littéral operation \"{op}\" absent du payload MQTT")
        # aucune autre valeur d'operation ne doit apparaître dans CE script
        other_ops = [o for o in OPERATIONS if o != op]
        for other in other_ops:
            if f'"operation": "{other}"' in text:
                error(f"T2 — {op} : le script émet aussi operation \"{other}\" (vocabulaire non fixé)")
    if not ERRORS:
        ok("T2 — operation figée par script (AUDIT↔AUDIT, RELEASE_DIFF↔RELEASE_DIFF)")


def test_topic_qos_retain() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        if f'topic: "{TOPIC_COMMAND}"' not in text:
            error(f"T3 — {op} : topic \"{TOPIC_COMMAND}\" absent")
            ok_all = False
        if not re.search(r"qos:\s*1\b", text):
            error(f"T3 — {op} : qos: 1 absent")
            ok_all = False
        if not re.search(r"retain:\s*false\b", text):
            error(f"T3 — {op} : retain: false absent")
            ok_all = False
    if ok_all:
        ok(f"T3 — Topic unique {TOPIC_COMMAND}, QoS 1, retain=false pour les deux opérations")


def test_source_fixe() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        if '"source": "arsenal"' not in text:
            error(f"T4 — {op} : littéral source \"arsenal\" absent")
            ok_all = False
        # aucune interpolation Jinja dans le champ source (pas de {{ }} sur cette ligne)
        m = re.search(r'"source"\s*:\s*"([^"]*)"', text)
        if m and "{{" in m.group(1):
            error(f"T4 — {op} : champ source interpolé (Jinja détecté) — doit rester un littéral fixe")
    if ok_all:
        ok("T4 — source \"arsenal\" fixe (littéral, non interpolé) pour les deux opérations")


def test_no_business_params() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        active = read_active(cfg["script"])
        for forbidden in FORBIDDEN_BUSINESS_PARAMS:
            if forbidden in active:
                error(f"T5 — {op} : paramètre métier interdit détecté ({forbidden})")
                ok_all = False
        # Le payload publié ne doit contenir QUE les 5 champs contractuels.
        m = re.search(r"payload:\s*>-\s*\n((?:\s{10,}.*\n)+)", text)
        if m:
            payload_block = m.group(1)
            declared_fields = set(re.findall(r'"(\w+)"\s*:', payload_block))
            expected = {"request_id", "operation", "ts", "expires_at", "source"}
            extra = declared_fields - expected
            if extra:
                error(f"T5 — {op} : champ(s) non contractuel(s) dans le payload MQTT : {sorted(extra)}")
                ok_all = False
        else:
            error(f"T5 — {op} : bloc payload MQTT introuvable (format inattendu)")
            ok_all = False
    if ok_all:
        ok("T5 — Aucun paramètre métier libre ; payload limité aux 5 champs contractuels")


def test_helper_dedicated_and_distinct() -> None:
    if not F_HELPER_AUDIT.is_file():
        error("T6 — Helper AUDIT introuvable (Lot 5 modifié ou supprimé — interdit)")
        return
    if not F_HELPER_RELEASE_DIFF.is_file():
        error("T6 — Helper RELEASE_DIFF introuvable (Lot 6 non livré)")
        return

    helper_audit_active = read_active(F_HELPER_AUDIT)
    helper_rd_active = read_active(F_HELPER_RELEASE_DIFF)

    if "nas_admission_req_release_diff" in helper_audit_active:
        error("T6 — Le helper AUDIT (Lot 5) référence le helper RELEASE_DIFF — partage interdit")
    if "nas_admission_req_audit" in helper_rd_active:
        error("T6 — Le helper RELEASE_DIFF référence le helper AUDIT — partage interdit")

    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        active = read_active(cfg["script"])
        if cfg["helper_entity"] not in text:
            error(f"T6 — {op} : n'ancre pas sur son propre helper {cfg['helper_entity']}")
        if cfg["other_helper_entity"] in active:
            error(f"T6 — {op} : référence le helper de l'autre opération ({cfg['other_helper_entity']}) — verrou/état partagé interdit")

    if not ERRORS:
        ok("T6 — Helpers transactionnels dédiés et strictement distincts (aucun partage AUDIT↔RELEASE_DIFF)")


def test_cleanup_systematique() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        # Le cleanup final doit exister : dernière occurrence de set_value avec value: ""
        cleanup_matches = re.findall(
            r'input_text\.set_value[\s\S]{0,200}?value:\s*""', text
        )
        if not cleanup_matches:
            error(f"T7 — {op} : aucun nettoyage (input_text.set_value value: \"\") détecté")
            ok_all = False
        # Le cleanup doit être présent hors du bloc de vérification post-écriture
        # (c'est-à-dire : au moins 2 occurrences — l'une en garde d'échec précoce,
        # l'autre en libération finale systématique).
        if len(cleanup_matches) < 2:
            error(f"T7 — {op} : nettoyage non systématique (attendu : garde d'échec post-écriture + libération finale)")
            ok_all = False
    if ok_all:
        ok("T7 — Nettoyage transactionnel systématique de l'ancrage (échec précoce + libération finale)")


def test_correlation_request_id_and_operation() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        wait_match = re.search(r"wait_template:\s*>\s*\n((?:.*\n)+?)\s*timeout:", text)
        if not wait_match:
            error(f"T8 — {op} : wait_template introuvable")
            ok_all = False
            continue
        block = wait_match.group(1)
        if "nas_admission_result_request_id" not in block:
            error(f"T8 — {op} : wait_template ne corrèle pas sur request_id")
            ok_all = False
        if f"'{op}'" not in block:
            error(f"T8 — {op} : wait_template ne corrèle pas sur operation == '{op}'")
            ok_all = False
    if ok_all:
        ok("T8 — Attente corrélée sur request_id ET operation pour les deux opérations")


def test_admitted_never_terminal() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        wait_match = re.search(r"wait_template:\s*>\s*\n((?:.*\n)+?)\s*timeout:", text)
        if not wait_match:
            continue
        block = wait_match.group(1)
        if "'admitted'" in block or '"admitted"' in block:
            error(f"T9 — {op} : 'admitted' apparaît dans la liste des verdicts terminaux attendus (interdit — non terminal)")
            ok_all = False
    if ok_all:
        ok("T9 — 'admitted' jamais traité comme verdict terminal (aucune des deux opérations)")


def test_verdict_vocabulary_complete() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        for v in VERDICTS_TERMINAUX:
            if v not in text:
                error(f"T10 — {op} : verdict terminal '{v}' absent du script (contrat §10)")
                ok_all = False
    if ok_all:
        ok(f"T10 — Vocabulaire de verdict terminal complet ({len(VERDICTS_TERMINAUX)} verdicts) pour les deux opérations")


def test_no_business_result_used_to_conclude() -> None:
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        biz = cfg["business_sensor"]
        # Le sensor métier ne doit jamais être lu via states()/state_attr() —
        # seule une mention textuelle (log, pointeur documentaire) est tolérée.
        if re.search(rf"states\(\s*['\"]{re.escape(biz)}['\"]", text):
            error(f"T11 — {op} : lit {biz} (résultat métier) — interdit, séparation transaction/métier (contrat §12)")
            ok_all = False
        if re.search(rf"state_attr\(\s*['\"]{re.escape(biz)}['\"]", text):
            error(f"T11 — {op} : lit un attribut de {biz} (résultat métier) — interdit")
            ok_all = False
    if ok_all:
        ok("T11 — Aucun script ne lit son sensor de résultat métier pour conclure la transaction")


def test_diagnostics_filter_and_latch_per_operation() -> None:
    diag_files = {"AUDIT": F_DIAG_AUDIT, "RELEASE_DIFF": F_DIAG_RELEASE_DIFF}
    ok_all = True
    for op, path in diag_files.items():
        text = read(path)
        if not text:
            error(f"T12 — Diagnostic {op} manquant : {path.relative_to(ROOT)}")
            ok_all = False
            continue
        if f"== '{op}'" not in text:
            error(f"T12 — Diagnostic {op} : ne filtre pas sur operation == '{op}'")
            ok_all = False
        if "this.state" not in text:
            error(f"T12 — Diagnostic {op} : ne latche pas via this.state (risque d'écrasement par l'autre opération)")
            ok_all = False
        other = "RELEASE_DIFF" if op == "AUDIT" else "AUDIT"
        if f"== '{other}'" in text:
            error(f"T12 — Diagnostic {op} : référence aussi operation == '{other}' (mélange des deux diagnostics)")
            ok_all = False
    if ok_all:
        ok("T12 — Chaque diagnostic filtre et latche sur sa seule opération, sans écrasement croisé")


def test_shared_layer_unfiltered() -> None:
    """Le sensor raw et la couche de corrélation restent, par construction,
    partagés et NON filtrés par opération (contrat §13.1) — Lot 6 ne doit
    pas y introduire de filtre par opération (ce serait dupliquer le plan
    transport, interdit — §6 mission Lot 6)."""
    ok_all = True
    for path, label in [(F_RAW_SENSOR, "sensor raw"), (F_CORRELATION, "corrélation")]:
        text = read(path)
        if not text:
            error(f"T13 — {label} introuvable : {path}")
            ok_all = False
            continue
        if "== 'AUDIT'" in text or "== 'RELEASE_DIFF'" in text:
            error(f"T13 — {label} : filtre par opération détecté — devrait rester générique (délégué aux diagnostics)")
            ok_all = False
    if ok_all:
        ok("T13 — Sensor raw + couche de corrélation restent génériques, sans filtre par opération")


def test_mode_single_scoped_not_global() -> None:
    """mode: single de chaque script ne doit borner QUE ce script — aucun
    verrou/état HA partagé entre les deux scripts (contrat §11 ; chantier
    C51 §8 : pas de verrou global AUDIT/RELEASE_DIFF)."""
    ok_all = True
    for op, cfg in OPERATIONS.items():
        text = read(cfg["script"])
        if not re.search(r"^\s*mode:\s*single\s*$", text, re.MULTILINE):
            error(f"T14 — {op} : mode: single absent (chaque script doit rester non ré-entrant sur lui-même)")
            ok_all = False
    # Vérifie qu'aucun des deux scripts n'appelle l'autre script (script.turn_on / script.nas_admission_demander_*)
    active_audit = read_active(F_SCRIPT_AUDIT)
    active_rd = read_active(F_SCRIPT_RELEASE_DIFF)
    if "nas_admission_demander_release_diff" in active_audit:
        error("T14 — Le script AUDIT référence le script RELEASE_DIFF — couplage interdit")
        ok_all = False
    if "nas_admission_demander_audit" in active_rd:
        error("T14 — Le script RELEASE_DIFF référence le script AUDIT — couplage interdit")
        ok_all = False
    if ok_all:
        ok("T14 — mode: single scope à chaque script ; aucun appel croisé AUDIT↔RELEASE_DIFF")


TESTS = [
    test_scripts_present,
    test_operation_fixee,
    test_topic_qos_retain,
    test_source_fixe,
    test_no_business_params,
    test_helper_dedicated_and_distinct,
    test_cleanup_systematique,
    test_correlation_request_id_and_operation,
    test_admitted_never_terminal,
    test_verdict_vocabulary_complete,
    test_no_business_result_used_to_conclude,
    test_diagnostics_filter_and_latch_per_operation,
    test_shared_layer_unfiltered,
    test_mode_single_scoped_not_global,
]


if __name__ == "__main__":
    print("Arsenal — Vérification statique : socle transactionnel NAS "
          "(C51 Lot 6 — RELEASE_DIFF + non-régression AUDIT)\n")

    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONFORME — RELEASE_DIFF (Lot 6) + AUDIT (Lot 5) inchangé")
