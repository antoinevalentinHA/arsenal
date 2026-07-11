#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Production des signaux de précipitation
Contrat (source normative) : 00_documentation_arsenal/contrats/meteo/pluie_production.md
Script  : scripts/arsenal_contracts/check_pluie_production_contracts.py

Vérifie les invariants de PRODUCTION / QUALIFICATION de la pluie (pas la réaction
volets, régie par check_volets_pluie_contracts.py). Contrôle textuel déterministe,
lecture seule. ERROR => exit 1.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Fichiers canoniques
# ---------------------------------------------------------------------------
F_CONTRAT   = REPO_ROOT / "00_documentation_arsenal/contrats/meteo/pluie_production.md"
F_EVIDENCE  = REPO_ROOT / "12_template_sensors/meteo/pluie/evidence_active.yaml"
F_FORTE     = REPO_ROOT / "12_template_sensors/volets/intention_pluie_detectee.yaml"
F_RECENTE   = REPO_ROOT / "12_template_sensors/meteo/pluie/recente.yaml"
F_PREVUE    = REPO_ROOT / "12_template_sensors/meteo/pluie/prevue.yaml"
F_EN_COURS  = REPO_ROOT / "05_input_booleans/meteo/pluie_en_cours.yaml"
F_MAJ_ON    = REPO_ROOT / "11_automations/meteo/pluie/maj_sensor/on.yaml"
F_MAJ_OFF   = REPO_ROOT / "11_automations/meteo/pluie/maj_sensor/off.yaml"
F_VOLETS    = REPO_ROOT / "00_documentation_arsenal/contrats/volets_pluie.md"

ERRORS: list[str] = []


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def has_uid(content: str, uid: str) -> bool:
    return bool(re.search(rf"unique_id\s*:\s*{re.escape(uid)}\b", content))


# ---------------------------------------------------------------------------
# T1 — Contrat présent
# ---------------------------------------------------------------------------
def test_contrat_present() -> None:
    if not F_CONTRAT.is_file():
        ERRORS.append(f"T1 — Contrat manquant : {F_CONTRAT.relative_to(REPO_ROOT)}")
    else:
        print("✔ T1 — Contrat pluie_production.md présent")


# ---------------------------------------------------------------------------
# T2 — Qualifications canoniques déclarées (§5)
# ---------------------------------------------------------------------------
def test_qualifications_declarees() -> None:
    checks = {
        "pluie_evidence_active": F_EVIDENCE,
        "intention_pluie_forte": F_FORTE,
        "pluie_recente_1h":      F_RECENTE,
        "pluie_prevue":          F_PREVUE,
    }
    all_ok = True
    for uid, path in checks.items():
        if not has_uid(read(path), uid):
            ERRORS.append(f"T2 — unique_id: {uid} absent de "
                          f"{path.relative_to(REPO_ROOT)} (§5)")
            all_ok = False
    # input_boolean.pluie_en_cours (clé de mapping)
    if not re.search(r"^\s*pluie_en_cours\s*:", read(F_EN_COURS), re.MULTILINE):
        ERRORS.append(f"T2 — input_boolean.pluie_en_cours absent de "
                      f"{F_EN_COURS.relative_to(REPO_ROOT)} (§5)")
        all_ok = False
    if all_ok:
        print("✔ T2 — Qualifications canoniques déclarées "
              "(evidence, forte, récente, prévue, pluie_en_cours)")


# ---------------------------------------------------------------------------
# T3 — INV-PROD-3 : « pluie forte » = mesure quantitative uniquement
# ---------------------------------------------------------------------------
def test_forte_source_quantitative() -> None:
    content = read(F_FORTE)
    if not content:
        ERRORS.append(f"T3 — Fichier inaccessible : {F_FORTE.relative_to(REPO_ROOT)}")
        return
    if "sensor.pluviometre_precipitation" not in content:
        ERRORS.append("T3 — intention_pluie_forte ne lit pas la mesure quantitative "
                      "`sensor.pluviometre_precipitation` (INV-PROD-3)")
    elif "zigbee_pluie_water_leak" in content:
        ERRORS.append("T3 — intention_pluie_forte référence le détecteur binaire "
                      "`zigbee_pluie_water_leak` : un binaire ne qualifie jamais "
                      "« forte » (INV-PROD-3)")
    else:
        print("✔ T3 — « pluie forte » qualifiée par la seule mesure quantitative "
              "(INV-PROD-3)")


# ---------------------------------------------------------------------------
# T4 — INV-PROD-6 : évidence honnête (availability) + ≥ 1 source réelle
# ---------------------------------------------------------------------------
def test_evidence_disponibilite() -> None:
    content = read(F_EVIDENCE)
    if not content:
        ERRORS.append(f"T4 — Fichier inaccessible : {F_EVIDENCE.relative_to(REPO_ROOT)}")
        return
    ok = True
    if not re.search(r"^\s*availability\s*:", content, re.MULTILINE):
        ERRORS.append("T4 — pluie_evidence_active sans `availability` (INV-PROD-6)")
        ok = False
    for src in ("sensor.pluviometre_precipitation",
                "binary_sensor.zigbee_pluie_water_leak"):
        if src not in content:
            ERRORS.append(f"T4 — pluie_evidence_active ne référence pas la source "
                          f"réelle `{src}` (acquisition multi-source)")
            ok = False
    if ok:
        print("✔ T4 — Évidence honnête sur sa disponibilité + acquisition "
              "multi-source (INV-PROD-6)")


# ---------------------------------------------------------------------------
# T5 — INV-PROD-5 : verrou anti-régression C16 (sortie non figée par Netatmo)
# ---------------------------------------------------------------------------
def test_sortie_consomme_evidence() -> None:
    content = read(F_MAJ_OFF)
    if not content:
        ERRORS.append(f"T5 — Fichier inaccessible : {F_MAJ_OFF.relative_to(REPO_ROOT)}")
        return
    ok = True
    if "binary_sensor.pluie_evidence_active" not in content:
        ERRORS.append("T5 — la sortie d'épisode ne consomme pas l'évidence "
                      "consolidée (régression C16 — INV-PROD-5)")
        ok = False
    if "input_boolean.systeme_stable" not in content:
        ERRORS.append("T5 — la sortie d'épisode n'a pas de réconciliation "
                      "`systeme_stable` au démarrage (INV-PROD-5)")
        ok = False
    if "time_pattern" not in content:
        ERRORS.append("T5 — la sortie d'épisode n'a pas de backstop dégradé "
                      "(`time_pattern`) (INV-PROD-5)")
        ok = False
    if ok:
        print("✔ T5 — Sortie d'épisode : évidence + réconciliation boot + backstop "
              "dégradé (verrou anti-régression C16, INV-PROD-5)")


# ---------------------------------------------------------------------------
# T6 — Symétrie : l'entrée consomme aussi l'évidence
# ---------------------------------------------------------------------------
def test_entree_consomme_evidence() -> None:
    content = read(F_MAJ_ON)
    if not content:
        ERRORS.append(f"T6 — Fichier inaccessible : {F_MAJ_ON.relative_to(REPO_ROOT)}")
        return
    if "binary_sensor.pluie_evidence_active" not in content:
        ERRORS.append("T6 — l'entrée d'épisode ne consomme pas l'évidence "
                      "consolidée (symétrie entrée/sortie)")
    else:
        print("✔ T6 — Entrée d'épisode consomme l'évidence (symétrie)")


# ---------------------------------------------------------------------------
# T7 — INV-PROD-7 : présomption ≠ fait (prévue jamais repliée à 0)
# ---------------------------------------------------------------------------
def test_prevue_presomption() -> None:
    content = read(F_PREVUE)
    if not content:
        ERRORS.append(f"T7 — Fichier inaccessible : {F_PREVUE.relative_to(REPO_ROOT)}")
        return
    if "unknown" not in content:
        ERRORS.append("T7 — pluie_prevue ne préserve pas l'état `unknown` "
                      "(présomption repliée en fait — INV-PROD-7)")
    else:
        print("✔ T7 — pluie_prevue préserve `unknown` (présomption ≠ fait, INV-PROD-7)")


# ---------------------------------------------------------------------------
# T8 — INV-PROD-9 : frontière contractuelle (volets_pluie référence ce contrat)
# ---------------------------------------------------------------------------
def test_frontiere_contractuelle() -> None:
    content = read(F_VOLETS)
    if not content:
        ERRORS.append(f"T8 — Fichier inaccessible : {F_VOLETS.relative_to(REPO_ROOT)}")
        return
    if "pluie_production.md" not in content:
        ERRORS.append("T8 — volets_pluie.md ne référence pas le contrat de "
                      "production `pluie_production.md` (frontière — INV-PROD-9)")
    else:
        print("✔ T8 — Frontière contractuelle : volets_pluie.md référence "
              "pluie_production.md (INV-PROD-9)")


TESTS = [
    test_contrat_present,
    test_qualifications_declarees,
    test_forte_source_quantitative,
    test_evidence_disponibilite,
    test_sortie_consomme_evidence,
    test_entree_consomme_evidence,
    test_prevue_presomption,
    test_frontiere_contractuelle,
]

if __name__ == "__main__":
    print("Arsenal — Validation contractuelle : Production pluie v1.0\n")
    for test_fn in TESTS:
        test_fn()
    if ERRORS:
        print("\n❌ CONTRAT PRODUCTION PLUIE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    print("\n✅ CONTRAT PRODUCTION PLUIE CONFORME")
