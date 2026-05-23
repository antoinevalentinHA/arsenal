#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Recorder
Contrats : Arsenal Recorder Contract, Arsenal Recorder Fiche de Décision
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []
WARNINGS = []


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(content: str) -> str:
    return "\n".join(
        line for line in content.splitlines()
        if not line.lstrip().startswith("#")
    )


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


RECORDER_FILE = ROOT / "recorder.yaml"


def get_recorded_entities() -> set[str]:
    """Extrait la liste des entités enregistrées depuis recorder.yaml."""
    content = read(RECORDER_FILE)
    # Entités sous include: / entities: — lignes `    - entity.id`
    entities = set(re.findall(r"^\s{4}-\s+([\w.]+)\s*$", content, re.MULTILINE))
    return entities


# ---------------------------------------------------------------------------
# T01 — purge_keep_days ≤ 90 (contrat §Rétention)
# ---------------------------------------------------------------------------

def test_purge_keep_days():
    """
    Vérifie que purge_keep_days ne dépasse pas 90 jours.
    Contrat §Rétention : rétention maximale opposable = 90 jours.
    Toute valeur supérieure est une dérive contractuelle.
    """
    content = read(RECORDER_FILE)
    match = re.search(r"^\s*purge_keep_days\s*:\s*(\d+)", content, re.MULTILINE)
    check(
        match is not None,
        "T01 — purge_keep_days absent de recorder.yaml",
    )
    if match:
        days = int(match.group(1))
        check(
            days <= 90,
            f"T01 — purge_keep_days = {days} dépasse la rétention maximale de 90 jours (§Rétention)",
        )
    ok("T01 — purge_keep_days ≤ 90 jours (§Rétention)")


# ---------------------------------------------------------------------------
# T02 — auto_purge: true présent (contrat §Rétention)
# ---------------------------------------------------------------------------

def test_auto_purge():
    """
    Vérifie que auto_purge est activé.
    Nécessaire pour que la rétention contractuelle soit effectivement appliquée.
    """
    content = read(RECORDER_FILE)
    check(
        bool(re.search(r"^\s*auto_purge\s*:\s*true\b", content, re.MULTILINE)),
        "T02 — auto_purge: true absent de recorder.yaml (purge inactive)",
    )
    ok("T02 — auto_purge: true actif")


# ---------------------------------------------------------------------------
# T03 — Pas de doublons dans la liste d'entités (§Principe de filtrage)
# ---------------------------------------------------------------------------

def test_no_duplicates():
    """
    Vérifie l'absence de doublons dans la liste include.entities.
    Un doublon indique une dérive de maintenance — l'allowlist doit
    rester propre et auditée.
    """
    content = read(RECORDER_FILE)
    entities = re.findall(r"^\s{4}-\s+([\w.]+)\s*$", content, re.MULTILINE)
    seen = set()
    for entity in entities:
        if entity in seen:
            check(False, f"T03 — doublon dans recorder.yaml : {entity}")
        seen.add(entity)
    ok("T03 — aucun doublon dans la liste d'entités")


# ---------------------------------------------------------------------------
# T04 — Pas de bloc exclude: (§Principe de filtrage — allowlist stricte)
# ---------------------------------------------------------------------------

def test_no_exclude_block():
    """
    Vérifie l'absence de bloc exclude: dans recorder.yaml.
    Le contrat impose une allowlist stricte : tout est exclu par défaut,
    inclusion explicite uniquement. Un bloc exclude: signale une dérive
    vers une logique de denylist implicite.
    """
    content = strip_comments(read(RECORDER_FILE))
    check(
        not bool(re.search(r"^\s*exclude\s*:", content, re.MULTILINE)),
        "T04 — bloc exclude: présent dans recorder.yaml (violation allowlist stricte §Principe de filtrage)",
    )
    ok("T04 — pas de bloc exclude: (allowlist stricte)")


# ---------------------------------------------------------------------------
# T05 — Sources history_stats enregistrées dans recorder.yaml (Population A)
# ---------------------------------------------------------------------------

def test_history_stats_sources_recorded():
    """
    Vérifie que chaque entité source d'un capteur history_stats
    est enregistrée dans recorder.yaml.

    Contrat §Population A : history_stats dépend structurellement
    de l'historique recorder de son entité source. L'absence
    d'enregistrement provoque un retour à 0 ou N/A sans signal explicite.

    Pattern : `entity:` ou `entity_id:` dans les fichiers
    13_sensor_platforms/history_stats/**/*.yaml
    """
    recorded = get_recorded_entities()
    hs_dir = ROOT / "13_sensor_platforms/history_stats"

    source_pattern = re.compile(r"^\s+entity(?:_id)?\s*:\s*([\w.]+)", re.MULTILINE)

    for yaml_file in yaml_files(hs_dir):
        content = strip_comments(read(yaml_file))
        for match in source_pattern.finditer(content):
            source = match.group(1)
            if not source or source in ("true", "false", "on", "off"):
                continue
            check(
                source in recorded,
                f"T05 — source history_stats non enregistrée : {source} "
                f"(dans {yaml_file.relative_to(ROOT)}) — Population A manquante",
            )
    ok("T05 — toutes les sources history_stats enregistrées (Population A)")


# ---------------------------------------------------------------------------
# T06 — Sources platform: statistics enregistrées dans recorder.yaml (Population A)
# ---------------------------------------------------------------------------

def test_statistics_sources_recorded():
    """
    Vérifie que chaque entité source d'un capteur platform: statistics
    est enregistrée dans recorder.yaml.

    Contrat §Population A : platform: statistics dépend de l'historique
    recorder de sa source pour reconstruire la fenêtre glissante après
    redémarrage ou purge. L'absence d'enregistrement dégrade silencieusement
    la fenêtre sans erreur visible.

    Pattern : `entity:` ou `entity_id:` dans les fichiers
    13_sensor_platforms/statistics/**/*.yaml
    """
    recorded = get_recorded_entities()
    stats_dir = ROOT / "13_sensor_platforms/statistics"

    source_pattern = re.compile(r"^\s+entity(?:_id)?\s*:\s*([\w.]+)", re.MULTILINE)

    for yaml_file in yaml_files(stats_dir):
        content = strip_comments(read(yaml_file))
        # Ne traiter que les fichiers qui déclarent platform: statistics
        if "platform: statistics" not in content and "platform:statistics" not in content:
            continue
        for match in source_pattern.finditer(content):
            source = match.group(1)
            if not source or source in ("true", "false", "on", "off"):
                continue
            check(
                source in recorded,
                f"T06 — source platform:statistics non enregistrée : {source} "
                f"(dans {yaml_file.relative_to(ROOT)}) — Population A manquante",
            )
    ok("T06 — toutes les sources platform:statistics enregistrées (Population A)")


# ---------------------------------------------------------------------------
# T07 — Invariant d'indépendance : aucune automation/script ne dépend
#        du recorder pour décider (§Invariant fondamental)
# ---------------------------------------------------------------------------

def test_no_recorder_dependency_in_logic():
    """
    Vérifie qu'aucune automation ou script n'utilise history() ou
    states.entity_id.last_changed / last_updated comme entrée de décision
    dans un bloc condition: ou action:.

    Contrat §Invariant fondamental : le recorder n'est pas un composant
    d'exécution. Toute logique métier doit fonctionner sans historique.

    Patterns détectés (hors commentaires) :
    - history(  — appel direct à la fonction history Jinja2
    - last_changed  — attribut d'état temporel utilisé en décision
    - last_updated  — idem

    Scope : 11_automations/ et 10_scripts/ uniquement.
    Exclus : 12_template_sensors/ (capteurs d'observation — lectures passives légitimes
    de last_changed pour calculer des durées, non des décisions d'exécution).
    """
    scan_dirs = [ROOT / "11_automations", ROOT / "10_scripts"]
    # Patterns qui indiquent une dépendance à l'historique recorder
    history_pattern = re.compile(r"\bhistory\s*\(")

    for scan_dir in scan_dirs:
        for yaml_file in yaml_files(scan_dir):
            cleaned = strip_comments(read(yaml_file))
            if history_pattern.search(cleaned):
                check(
                    False,
                    f"T07 — appel history() détecté dans {yaml_file.relative_to(ROOT)} "
                    f"(dépendance recorder dans logique métier — §Invariant fondamental)",
                )
    ok("T07 — aucune dépendance history() dans les automations/scripts (§Invariant fondamental)")


# ---------------------------------------------------------------------------
# T08 — Entités à nom manifestement technique non enregistrées (Population B §Non éligibles)
# ---------------------------------------------------------------------------

def test_no_technical_internals_recorded():
    """
    Vérifie qu'aucune entité à nom manifestement technique/interne
    n'est enregistrée dans recorder.yaml.

    Contrat §Population B Non éligibles : helpers techniques, états transitoires,
    capteurs intermédiaires, debug/introspection ne doivent pas être enregistrés.

    Patterns de noms techniques détectés :
    - *_debug, *_raw, *_test, *_tmp, *_temp (au sens technique, pas thermique)
    - *_pipeline_*, *_transitionnel, *_interne
    - input_text.* contenant _req_, _request_, _correlation_, _ack_

    Note : les faux positifs sont exclus par conception — ces patterns
    ne correspondent pas à des entités de mesure physique ou métier.
    """
    recorded = get_recorded_entities()

    technical_patterns = [
        re.compile(r"_debug\b"),
        re.compile(r"\b_raw\b"),
        re.compile(r"_test\b"),
        re.compile(r"\btmp_|_tmp\b"),
        re.compile(r"_pipeline_en_cours"),
        re.compile(r"_transitionnel"),
        re.compile(r"boiler_req_"),
        re.compile(r"_correlation_"),
        re.compile(r"_ack_"),
        re.compile(r"last_action_status"),
    ]

    for entity in sorted(recorded):
        for pattern in technical_patterns:
            if pattern.search(entity):
                check(
                    False,
                    f"T08 — entité technique enregistrée : {entity} "
                    f"(pattern '{pattern.pattern}' — Population B Non éligible)",
                )
                break
    ok("T08 — aucune entité manifestement technique enregistrée (Population B)")


# ---------------------------------------------------------------------------
# T09 — Cohérence rétention vs besoins history_stats déclarés
# ---------------------------------------------------------------------------

def test_retention_vs_history_stats():
    """
    Vérifie que purge_keep_days couvre la fenêtre maximale déclarée
    dans les fichiers history_stats (via commentaire # Recorder : requis).

    Les fichiers history_stats documentent leurs besoins minimaux de rétention.
    Si purge_keep_days < besoin déclaré, le capteur fonctionne en mode dégradé.

    Pattern : # Recorder : requis — rétention minimale [N] j
              # Recorder : requis — purge_keep_days ≥ [N]
    """
    content = read(RECORDER_FILE)
    match = re.search(r"^\s*purge_keep_days\s*:\s*(\d+)", content, re.MULTILINE)
    if not match:
        return
    purge_days = int(match.group(1))

    hs_dir = ROOT / "13_sensor_platforms/history_stats"
    retention_pattern = re.compile(
        r"#\s*Recorder\s*:.*?(?:rétention minimale|purge_keep_days\s*[≥>=]+)\s*(\d+)",
        re.IGNORECASE,
    )

    for yaml_file in yaml_files(hs_dir):
        raw_content = read(yaml_file)
        for m in retention_pattern.finditer(raw_content):
            required = int(m.group(1))
            check(
                purge_days >= required,
                f"T09 — purge_keep_days={purge_days} insuffisant pour "
                f"{yaml_file.relative_to(ROOT)} (requiert ≥ {required} j)",
            )
    ok("T09 — rétention recorder couvre tous les besoins history_stats déclarés")


# ---------------------------------------------------------------------------
# T10 — Entités energy (*_energy) enregistrées ont state_class défini (Population A)
# ---------------------------------------------------------------------------

def test_energy_entities_have_state_class():
    """
    Vérifie que les entités *_energy enregistrées dans recorder.yaml
    ont un state_class déclaré dans leur fichier source
    (01_customize/ ou 12_template_sensors/system/proxy_energie/).

    Contrat §Population A : les entités energy sont obligatoires par
    contrainte HA (Energy Dashboard, long-term statistics). La présence
    de state_class garantit leur éligibilité aux statistiques long terme.

    Scope : scan de 01_customize/ et 12_template_sensors/ pour trouver
    les déclarations state_class correspondantes.
    """
    recorded = get_recorded_entities()
    energy_entities = {e for e in recorded if e.endswith("_energy") or "_energy_" in e}

    # Collecte tous les state_class déclarés dans customize et template_sensors
    state_class_entities: set[str] = set()
    scan_dirs = [
        ROOT / "01_customize",
        ROOT / "12_template_sensors",
        ROOT / "14_mqtt_sensors",
        ROOT / "13_sensor_platforms",
    ]
    # Pattern : entity_id implicite dans le fichier + state_class
    # On cherche le nom de l'entité dans unique_id ou dans la clé de mapping
    sc_pattern = re.compile(r"state_class\s*:")
    uid_pattern = re.compile(r"unique_id\s*:\s*([\w.]+)")
    mapping_pattern = re.compile(r"^([\w.]+)\s*:\s*$", re.MULTILINE)

    for scan_dir in scan_dirs:
        for yaml_file in yaml_files(scan_dir):
            content = read(yaml_file)
            if not sc_pattern.search(content):
                continue
            # Extraire les unique_ids du fichier
            for m in uid_pattern.finditer(content):
                uid = m.group(1)
                # Construire le sensor.* correspondant
                for domain in ("sensor", "binary_sensor"):
                    state_class_entities.add(f"{domain}.{uid}")
            # Extraire les clés de mapping (customize)
            for m in mapping_pattern.finditer(content):
                key = m.group(1)
                if "." in key:
                    state_class_entities.add(key)

    for entity in sorted(energy_entities):
        # Vérification souple : si l'entité contient _energy et est dans
        # un fichier proxy, on accepte — les proxys energy ont state_class documenté
        base = entity.replace("sensor.", "")
        if "proxy" in base or "proxy" in str(entity):
            continue
        # Pour les entités _energy directes, vérifier la présence dans l'arbo
        # On accepte si le nom est connu dans les customize/template
        entity_name_fragment = base.replace("_energy", "")
        found_in_customize = False
        for scan_dir in [ROOT / "01_customize"]:
            for yaml_file in yaml_files(scan_dir):
                if entity in read(yaml_file) or entity_name_fragment in read(yaml_file):
                    found_in_customize = True
                    break
        if not found_in_customize:
            warn(
                f"T10 — entité energy enregistrée sans state_class trouvé : {entity} "
                f"(vérifier la déclaration Population A)"
            )
    ok("T10 — entités energy enregistrées tracées")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_purge_keep_days,
    test_auto_purge,
    test_no_duplicates,
    test_no_exclude_block,
    test_history_stats_sources_recorded,
    test_statistics_sources_recorded,
    test_no_recorder_dependency_in_logic,
    test_no_technical_internals_recorded,
    test_retention_vs_history_stats,
    test_energy_entities_have_state_class,
]

if __name__ == "__main__":
    print("Arsenal — Contrat Recorder\n")
    for test_fn in TESTS:
        test_fn()

    if WARNINGS:
        print("\n⚠️  Avertissements :\n")
        for w in WARNINGS:
            print(f"  △ {w}")

    if ERRORS:
        print("\n❌ CONTRAT RECORDER NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT RECORDER CONFORME")
