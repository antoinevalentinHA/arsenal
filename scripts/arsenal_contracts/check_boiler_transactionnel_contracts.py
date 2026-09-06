#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle : Socle transactionnel Boiler Bridge
Source normative : 00_documentation_arsenal/contrats/boiler/ (chapitres listés ci-dessous)
Contrats : socle_transactionnel, mqtt_ack_ha, script_executif,
           consommation_ack, retry_transactionnel, guard_exposition_ha
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERRORS = []


def error(msg: str) -> None:
    ERRORS.append(msg)


def ok(label: str) -> None:
    print(f"  ✔ {label}")


def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return [p for p in folder.rglob("*.yaml") if p.is_file()]


# ──────────────────────────────────────────────────────────────
# Dossiers et fichiers canoniques
# ──────────────────────────────────────────────────────────────

DIR_INPUT_TEXTS      = ROOT / "04_input_texts"
DIR_TEMPLATE_SENSORS = ROOT / "12_template_sensors"
DIR_SCRIPTS          = ROOT / "10_scripts"
DIR_AUTOMATIONS      = ROOT / "11_automations"

FILE_REQ_HELPERS     = DIR_INPUT_TEXTS / "boiler" / "request_id_transactionnels.yaml"
DIR_BOILER_SENSORS   = DIR_TEMPLATE_SENSORS / "boiler"
DIR_SCRIPTS_ECS      = DIR_SCRIPTS / "ecs"
DIR_SCRIPTS_CHAUFF   = DIR_SCRIPTS / "chauffage"

FILE_SCRIPT_ECS      = DIR_SCRIPTS_ECS / "appliquer_consigne_bridge.yaml"
FILE_SCRIPT_CHAUFF   = DIR_SCRIPTS_CHAUFF / "application_consigne.yaml"

# Exécuteur transactionnel par rôle — T03 (corrélation) porte sur eux, car
# c'est là que la corrélation est réellement évaluée (consommation_ack §5 v1.2).
SCRIPTS_BY_ROLE = {
    "dhw_set_setpoint":        FILE_SCRIPT_ECS,
    "heating_set_temperature": FILE_SCRIPT_CHAUFF,
    "heating_set_curve_slope": DIR_SCRIPTS_CHAUFF / "courbe_de_chauffe" / "application_pente.yaml",
    "heating_set_curve_shift": DIR_SCRIPTS_CHAUFF / "courbe_de_chauffe" / "application_parallele.yaml",
}

# Commandes transactionnelles
COMMANDS = [
    "dhw_set_setpoint",
    "heating_set_temperature",
    "heating_set_curve_shift",
    "heating_set_curve_slope",
]

# Commandes retryables (contrat retry §2.1)
RETRYABLE = {"dhw_set_setpoint", "heating_set_temperature"}
# Commandes non retryables
NON_RETRYABLE = {"heating_set_curve_shift", "heating_set_curve_slope"}


# ──────────────────────────────────────────────────────────────
# Détection
# ──────────────────────────────────────────────────────────────

def is_declared_as_mapping_key(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf'^\s*{re.escape(entity_id)}\s*:', re.MULTILINE)
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False


def is_declared_as_unique_id(entity_id: str, folder: Path) -> bool:
    pattern = re.compile(rf'unique_id\s*:\s*{re.escape(entity_id)}\b')
    for p in yaml_files(folder):
        if pattern.search(read(p)):
            return True
    return False



# ──────────────────────────────────────────────────────────────
# Corrélation transactionnelle — cœur pur (T03)
#
# La corrélation NE VIT PAS dans la couche template : elle est évaluée par les
# scripts exécutifs, qui comparent sensor.boiler_ack_<role>_request_id au
# request_id de la transaction en cours avant de conclure sur le statut.
# Source : consommation_ack.md v1.2 §5 (« la corrélation est une RÈGLE, pas une
# entité ») et §8 (interface consommée canonique : *_status CONJUGUÉ à
# *_request_id). Les projections *_correlation et *_result sont legacy
# supprimables (§11) — un test qui s'appuierait sur elles deviendrait faux.
#
# Ces fonctions sont pures (texte -> violations) pour être exerçables en
# --selftest sans écrire aucun fichier.
# ──────────────────────────────────────────────────────────────

def strip_yaml_comments(text: str) -> str:
    """Retire les commentaires YAML (`#` hors chaîne quotée).

    Indispensable : un simple commentaire d'en-tête citant un identifiant ne
    doit JAMAIS suffire à satisfaire un test de corrélation. C'est précisément
    la vacuité qui affectait la version antérieure de T03.
    """
    out = []
    for line in text.splitlines():
        in_s = in_d = False
        cut = None
        for i, ch in enumerate(line):
            if ch == "'" and not in_d:
                in_s = not in_s
            elif ch == '"' and not in_s:
                in_d = not in_d
            elif ch == "#" and not in_s and not in_d and (i == 0 or line[i - 1].isspace()):
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


def jinja_expressions(text: str) -> list[str]:
    """Extrait les expressions Jinja `{{ ... }}`, multilignes comprises.

    L'unité d'évaluation est l'expression, pas le fichier : exiger que deux
    lectures cohabitent dans le MÊME `{{ ... }}` interdit qu'une corrélation
    située dans un bloc sans rapport valide une conclusion faite ailleurs.
    """
    return re.findall(r"\{\{[\s\S]*?\}\}", text)


def _rx_ack(role: str, champ: str) -> str:
    return rf"""states\(\s*['"]sensor\.boiler_ack_{re.escape(role)}_{champ}['"]\s*\)"""


def _rx_req_courant(role: str) -> str:
    """Référence au request_id de la transaction en cours : la variable de
    script, ou une relecture du helper de corrélation du rôle."""
    return (
        rf"""(?:boiler_request_id"""
        rf"""|states\(\s*['"]input_text\.boiler_req_{re.escape(role)}['"]\s*\))"""
    )


def _rx_comparaison_correlee(role: str) -> "re.Pattern":
    ack = _rx_ack(role, "request_id")
    req = _rx_req_courant(role)
    return re.compile(rf"(?:{ack}\s*==\s*{req}|{req}\s*==\s*{ack})")


def verifier_correlation_role(role: str, script_text: str) -> list[str]:
    """Violations T03 pour un rôle, à partir du texte de son script exécutif.

    Propriété vérifiée — opposable et durable :
      C1  le script lit `sensor.boiler_ack_<role>_request_id` ;
      C2  il le compare au request_id de la transaction en cours ;
      C3  il lit `sensor.boiler_ack_<role>_status` ;
      C4  il ne conclut pas via la projection legacy `*_result` ;
      C5  au moins une expression Jinja conjugue statut ET corrélation ;
      C6  AUCUNE expression concluant au succès (`applied`) n'est dépourvue de
          la corrélation — c'est l'invariant de sûreté, pas une simple présence.
    """
    v: list[str] = []
    code = strip_yaml_comments(script_text)

    rx_req = re.compile(_rx_ack(role, "request_id"))
    rx_status = re.compile(_rx_ack(role, "status"))
    rx_corr = _rx_comparaison_correlee(role)
    rx_result = re.compile(rf"sensor\.boiler_ack_{re.escape(role)}_result")

    if not rx_req.search(code):
        v.append(f"C1 — {role} : sensor.boiler_ack_{role}_request_id jamais lu")
    if not rx_corr.search(code):
        v.append(
            f"C2 — {role} : aucune comparaison de "
            f"sensor.boiler_ack_{role}_request_id au request_id courant"
        )
    if not rx_status.search(code):
        v.append(f"C3 — {role} : sensor.boiler_ack_{role}_status jamais lu")
    if rx_result.search(code):
        v.append(
            f"C4 — {role} : conclusion via la projection legacy "
            f"sensor.boiler_ack_{role}_result (consommation_ack §11)"
        )

    exprs = jinja_expressions(code)
    if not any(rx_status.search(e) and rx_corr.search(e) for e in exprs):
        v.append(
            f"C5 — {role} : aucune expression ne conjugue le statut ACK et la "
            f"corrélation request_id — la conclusion n'est pas corrélée"
        )

    for e in exprs:
        if rx_status.search(e) and "applied" in e and not rx_corr.search(e):
            v.append(
                f"C6 — {role} : une expression conclut sur `applied` sans "
                f"corrélation request_id — succès non corrélé possible"
            )
            break

    return v


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────

def test_request_helpers_declared() -> None:
    """
    T01 — Les quatre helpers de corrélation transactionnels déclarés
    dans 04_input_texts/boiler/.
    Contrat consommation_ack §3 : helper dédié par commande.
    """
    folder = DIR_INPUT_TEXTS / "boiler"
    for cmd in COMMANDS:
        entity_id = f"boiler_req_{cmd}"
        if not is_declared_as_mapping_key(entity_id, folder):
            error(f"T01: input_text.{entity_id} introuvable dans {folder.relative_to(ROOT)}/")
    ok("T01 — helpers de corrélation transactionnels")


def test_transaction_sensors_declared() -> None:
    """
    T02 — Les quatre template sensors de transaction déclarés dans 12_template_sensors/boiler/.
    Contrat consommation_ack §4 (extraction des champs ACK) et §11 (table des
    projections conservées). La corrélation, elle, n'est pas de cette couche :
    voir T03.
    """
    for cmd in COMMANDS:
        filename = f"boiler_ack_{cmd}_transaction.yaml"
        p = DIR_BOILER_SENSORS / filename
        if not p.is_file():
            error(f"T02: {filename} introuvable dans {DIR_BOILER_SENSORS.relative_to(ROOT)}/")
    ok("T02 — template sensors transactionnels")


def test_transaction_sensors_correlate_request_id() -> None:
    """
    T03 — La corrélation transactionnelle est effective, LÀ OÙ ELLE VIT :
    dans les scripts exécutifs.

    Contrat consommation_ack v1.2 §5 (« la corrélation est une RÈGLE, pas une
    entité » — évaluée dans le consommateur), §8 (interface consommée
    canonique : `*_status` CONJUGUÉ à `*_request_id`) et §11 (projections
    conservées / legacy supprimables).

    Scope : 12_template_sensors/boiler/ (déclaration de la projection lue)
            + les 4 scripts exécutifs (évaluation de la corrélation).

    Historique — pourquoi ce test a changé de cible (chantier C49, A-4) :
    la version antérieure exigeait que chaque `boiler_ack_*_transaction.yaml`
    CONTIENNE la chaîne `boiler_req_<role>`. Elle plaçait donc la corrélation
    dans la couche template, où elle n'a jamais été évaluée par le runtime, et
    se satisfaisait d'une occurrence en COMMENTAIRE — un vert vacue. Le retrait
    des projections legacy `*_correlation` / `*_result` (C49, Lot 3) l'aurait
    rendue soit vacue, soit rouge, sans qu'aucune garantie n'ait bougé.
    """
    for role in COMMANDS:
        # Le terme de corrélation doit exister dans la couche template : c'est
        # la seule dépendance de T03 à cette couche, et elle survit au Lot 3.
        if not is_declared_as_unique_id(f"boiler_ack_{role}_request_id", DIR_BOILER_SENSORS):
            error(
                f"T03: sensor.boiler_ack_{role}_request_id non déclaré dans "
                f"{DIR_BOILER_SENSORS.relative_to(ROOT)}/ — terme de corrélation absent"
            )
            continue

        script = SCRIPTS_BY_ROLE[role]
        if not script.is_file():
            error(f"T03: script exécutif introuvable pour le rôle {role} : {script}")
            continue

        for violation in verifier_correlation_role(role, read(script)):
            error(f"T03: {script.relative_to(ROOT)} — {violation}")

    ok("T03 — corrélation request_id effective dans les 4 scripts exécutifs")


def test_script_ecs_checks_bridge_online() -> None:
    """
    T04 — Le script ECS vérifie que le bridge est online avant publication.
    Contrat script_executif §4.1 : précondition bridge disponible.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T04: appliquer_consigne_bridge.yaml introuvable dans 10_scripts/ecs/")
        return
    content = read(FILE_SCRIPT_ECS)
    if not re.search(r'boiler_bridge_online|bridge.*online|online.*bridge', content, re.IGNORECASE):
        error(
            "T04: script ECS ne vérifie pas l'état bridge online "
            "— précondition §4.1 non respectée"
        )
    ok("T04 — script ECS vérifie bridge online")


def test_script_ecs_writes_helper_before_publish() -> None:
    """
    T05 — Le script ECS écrit le request_id dans le helper avant publication MQTT.
    Contrat socle §2 : ordre critique — écriture helper avant publication.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    Vérifie la coprésence de input_text.set_value et mqtt.publish,
    et que set_value apparaît avant mqtt.publish dans le fichier.
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T05: appliquer_consigne_bridge.yaml introuvable")
        return
    content = read(FILE_SCRIPT_ECS)
    pos_set  = content.find("input_text.set_value") if "input_text.set_value" in content else -1
    pos_pub  = content.find("mqtt.publish") if "mqtt.publish" in content else -1
    if pos_set == -1:
        error("T05: script ECS ne contient pas input_text.set_value — armement helper absent")
    elif pos_pub == -1:
        error("T05: script ECS ne contient pas mqtt.publish — publication MQTT absente")
    elif pos_set > pos_pub:
        error(
            "T05: script ECS écrit le helper APRÈS mqtt.publish — "
            "ordre critique §2 violé"
        )
    ok("T05 — script ECS écrit le helper avant publication MQTT")


def test_script_ecs_verifies_helper_post_write() -> None:
    """
    T06 — Le script ECS vérifie le helper après écriture (post-write check).
    Contrat script_executif §7.2 : vérification post-écriture obligatoire.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
    """
    if not FILE_SCRIPT_ECS.is_file():
        error("T06: appliquer_consigne_bridge.yaml introuvable")
        return
    content = read(FILE_SCRIPT_ECS)
    # Le post-write check compare le helper au request_id généré
    POSTWRITE = re.compile(
        r'boiler_req_dhw_set_setpoint[\s\S]{0,100}!=[\s\S]{0,100}boiler_request_id'
        r'|boiler_request_id[\s\S]{0,100}!=[\s\S]{0,100}boiler_req_dhw_set_setpoint',
        re.MULTILINE
    )
    if not POSTWRITE.search(content):
        error(
            "T06: script ECS ne contient pas de vérification post-écriture du helper "
            "— invariant §7.2 / 15.7 non respecté"
        )
    ok("T06 — script ECS vérifie le helper après écriture")


def test_script_chauffage_checks_bridge_online() -> None:
    """
    T07 — Le script chauffage vérifie que le bridge est online avant publication.
    Contrat script_executif §4.1.
    Scope : 10_scripts/chauffage/application_consigne.yaml
    """
    if not FILE_SCRIPT_CHAUFF.is_file():
        error("T07: application_consigne.yaml introuvable dans 10_scripts/chauffage/")
        return
    content = read(FILE_SCRIPT_CHAUFF)
    if not re.search(r'boiler_bridge_online|bridge.*online|online.*bridge', content, re.IGNORECASE):
        error(
            "T07: script chauffage ne vérifie pas l'état bridge online "
            "— précondition §4.1 non respectée"
        )
    ok("T07 — script chauffage vérifie bridge online")


def test_script_chauffage_writes_helper_before_publish() -> None:
    """
    T08 — Le script chauffage écrit le request_id avant publication MQTT.
    Contrat socle §2 : ordre critique.
    Scope : 10_scripts/chauffage/application_consigne.yaml
    """
    if not FILE_SCRIPT_CHAUFF.is_file():
        error("T08: application_consigne.yaml introuvable")
        return
    content = read(FILE_SCRIPT_CHAUFF)
    pos_set = content.find("input_text.set_value") if "input_text.set_value" in content else -1
    pos_pub = content.find("mqtt.publish") if "mqtt.publish" in content else -1
    if pos_set == -1:
        error("T08: script chauffage ne contient pas input_text.set_value")
    elif pos_pub == -1:
        error("T08: script chauffage ne contient pas mqtt.publish")
    elif pos_set > pos_pub:
        error("T08: script chauffage écrit le helper APRÈS mqtt.publish — ordre §2 violé")
    ok("T08 — script chauffage écrit le helper avant publication MQTT")


def test_retry_automations_declared() -> None:
    """
    T09 — Les quatre automations de retry déclarées pour ECS et chauffage.
    Contrat retry §7.1 : orchestrateur = armement + etat + declenchement + reprise.
    """
    REQUIRED = [
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "armement.yaml",
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "etat.yaml",
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "declenchement.yaml",
        ROOT / "11_automations" / "ecs" / "retry_transactionnel" / "reprise.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "armement.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "etat.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "declenchement.yaml",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel" / "reprise.yaml",
    ]
    for p in REQUIRED:
        if not p.is_file():
            error(f"T09: {p.relative_to(ROOT)} introuvable — orchestrateur retry manquant")
    ok("T09 — automations retry transactionnel déclarées (4 par domaine)")


def test_retry_not_in_executive_scripts() -> None:
    """
    T10 — Les scripts exécutifs ne contiennent pas de logique de retry interne.
    Contrat retry §11.1 : le script exécutif ne porte jamais de logique de retry.
    Interdit : delay + boucle de retry dans les scripts exécutifs boiler.
    Scope : 10_scripts/ecs/appliquer_consigne_bridge.yaml
             10_scripts/chauffage/application_consigne.yaml
    """
    # Un retry interne se manifeste par un wait_template ou delay APRÈS
    # une publication MQTT suivie d'une seconde publication dans le même script
    RETRY_LOOP = re.compile(
        r'mqtt\.publish[\s\S]{0,2000}mqtt\.publish',
        re.MULTILINE
    )
    for p in [FILE_SCRIPT_ECS, FILE_SCRIPT_CHAUFF]:
        if not p.is_file():
            continue
        content = read(p)
        if RETRY_LOOP.search(content):
            error(
                f"T10: double mqtt.publish détecté dans {p.relative_to(ROOT)} "
                f"— retry interne interdit dans le script exécutif (contrat retry §11.1)"
            )
    ok("T10 — scripts exécutifs sans logique de retry interne")


def test_non_retryable_commands_absent_from_retry_automations() -> None:
    """
    T11 — Les commandes non retryables (curve_shift, curve_slope) ne sont pas
    référencées dans les automations de retry.
    Contrat retry §2.2 : commandes de calibration non retryables automatiquement.
    Scope : 11_automations/ecs/retry_transactionnel/ et
            11_automations/chauffage/retry_transactionnel/
    """
    RETRY_DIRS = [
        ROOT / "11_automations" / "ecs" / "retry_transactionnel",
        ROOT / "11_automations" / "chauffage" / "retry_transactionnel",
    ]
    for cmd in NON_RETRYABLE:
        for retry_dir in RETRY_DIRS:
            for p in yaml_files(retry_dir):
                content = read(p)
                # Distingue une référence de pilotage d'une mention passive en commentaire
                ACTIVE_REF = re.compile(
                    rf'(?:entity_id|topic|target)[\s\S]{{0,100}}{re.escape(cmd)}',
                    re.MULTILINE
                )
                if ACTIVE_REF.search(content):
                    error(
                        f"T11: commande non retryable '{cmd}' référencée activement "
                        f"dans {p.relative_to(ROOT)} — violation contrat retry §2.2"
                    )
    ok("T11 — commandes non retryables absentes des automations retry")


def test_guard_sensors_declared() -> None:
    """
    T12 — Les entités guard boiler déclarées dans 14_mqtt_sensors/ ou
    12_template_sensors/.
    Contrat guard_exposition_ha §4.
    """
    MQTT_SENSORS = ROOT / "14_mqtt_sensors"
    GUARD_SENSORS = [
        "boiler_guard_version",
        "boiler_guard_last_run",
        "boiler_guard_status",
        "boiler_guard_last_action",
    ]
    for entity_id in GUARD_SENSORS:
        found = (
            is_declared_as_unique_id(entity_id, MQTT_SENSORS)
            or is_declared_as_unique_id(entity_id, DIR_TEMPLATE_SENSORS)
        )
        if not found:
            error(
                f"T12: sensor.{entity_id} introuvable dans 14_mqtt_sensors/ "
                f"ou 12_template_sensors/ — entité guard manquante"
            )
    ok("T12 — sensors guard boiler déclarés")


def test_guard_stale_declared() -> None:
    """
    T13 — binary_sensor.boiler_guard_stale déclaré dans 12_template_sensors/.
    Contrat guard_exposition_ha §4.1 : dérivé de sensor.boiler_guard_last_run.
    """
    if not is_declared_as_unique_id("boiler_guard_stale", DIR_TEMPLATE_SENSORS):
        error(
            "T13: binary_sensor.boiler_guard_stale introuvable dans "
            f"{DIR_TEMPLATE_SENSORS.name}/"
        )
    ok("T13 — binary_sensor.boiler_guard_stale déclaré")


def test_guard_stale_based_on_last_run() -> None:
    """
    T14 — binary_sensor.boiler_guard_stale consomme sensor.boiler_guard_last_run.
    Contrat guard_exposition_ha §4.1.
    Scope : 12_template_sensors/ — fichier déclarant boiler_guard_stale.
    """
    UID = re.compile(r'unique_id\s*:\s*boiler_guard_stale\b')
    LAST_RUN = re.compile(r'boiler_guard_last_run')

    for p in yaml_files(DIR_TEMPLATE_SENSORS):
        content = read(p)
        if not UID.search(content):
            continue
        if not LAST_RUN.search(content):
            error(
                f"T14: binary_sensor.boiler_guard_stale ne consomme pas "
                f"sensor.boiler_guard_last_run : {p.relative_to(ROOT)}"
            )
    ok("T14 — boiler_guard_stale basé sur boiler_guard_last_run")


def test_no_guard_data_in_boiler_logic() -> None:
    """
    T15 — Les données guard (boiler/guard/*) ne conditionnent pas
    la logique métier ECS ou chauffage.
    Contrat guard_exposition_ha §2 : aucune donnée guard dans l'exécution métier.
    Scope : 10_scripts/ecs/ et 10_scripts/chauffage/ uniquement.
    """
    GUARD_REF = re.compile(r'boiler_guard_|boiler/guard/', re.IGNORECASE)
    for folder in [DIR_SCRIPTS_ECS, DIR_SCRIPTS_CHAUFF]:
        for p in yaml_files(folder):
            content = read(p)
            if GUARD_REF.search(content):
                error(
                    f"T15: référence à des données guard dans un script métier boiler : "
                    f"{p.relative_to(ROOT)} — violation §2 contrat guard"
                )
    ok("T15 — données guard absentes des scripts métier boiler")


def test_retry_helpers_declared() -> None:
    """
    T16 — Les helpers retry transactionnels déclarés dans leurs dossiers canoniques.
    Contrat retry §8.
    """
    DIR_IB = ROOT / "05_input_booleans"
    DIR_IN = ROOT / "03_input_numbers"
    DIR_IT = ROOT / "04_input_texts"
    DIR_TI = ROOT / "08_timers"

    HELPERS = [
        # ECS
        ("ecs_retry_pending",           DIR_IB / "ecs",         "input_boolean"),
        ("ecs_retry_attempt1_id",       DIR_IT / "ecs" / "retry", "input_text"),
        ("ecs_retry_attempt2_id",       DIR_IT / "ecs" / "retry", "input_text"),
        # Chauffage
        ("chauffage_retry_pending",     DIR_IB / "chauffage",   "input_boolean"),
        ("chauffage_retry_attempt1_id", DIR_IT / "chauffage",   "input_text"),
        ("chauffage_retry_attempt2_id", DIR_IT / "chauffage",   "input_text"),
        ("chauffage_retry_count",       DIR_IN,                 "input_number"),
        ("chauffage_retry",             DIR_TI,                 "timer"),
    ]
    for entity_id, folder, prefix in HELPERS:
        if not is_declared_as_mapping_key(entity_id, folder):
            error(
                f"T16: {prefix}.{entity_id} introuvable dans "
                f"{folder.relative_to(ROOT)}/"
            )
    ok("T16 — helpers retry transactionnels déclarés")


# ──────────────────────────────────────────────────────────────
# Auto-test du juge (on ne juge pas avec un juge défectueux)
#
# Exerce le cœur pur de T03 en mémoire, sur des corpus synthétiques. Objet :
# prouver que T03 ne passe PLUS vacuement — chaque cas négatif doit produire
# le code de violation attendu. Chantier C49, arbitrage A-4.
# ──────────────────────────────────────────────────────────────

ROLE_T = "dhw_set_setpoint"

# Cas positif — forme réellement en service sur les 4 rôles : attente d'une
# conclusion terminale corrélée, puis branches de conclusion corrélées.
_POSITIF = """
    - wait_template: >
        {{
          states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected', 'timeout']
          and states('sensor.boiler_ack_dhw_set_setpoint_request_id') == boiler_request_id
        }}
      timeout: "00:00:15"
    - choose:
        - conditions:
            - condition: template
              value_template: >
                {{
                  states('sensor.boiler_ack_dhw_set_setpoint_status') == 'applied'
                  and states('sensor.boiler_ack_dhw_set_setpoint_request_id') == boiler_request_id
                }}
"""

# N1 — la corrélation n'existe QUE dans un commentaire d'en-tête.
# C'est exactement le faux vert de l'ancien T03.
_N1_COMMENTAIRE = """
# Entités consommées :
#   - sensor.boiler_ack_dhw_set_setpoint_request_id
#   - input_text.boiler_req_dhw_set_setpoint
#   corrélation : states('sensor.boiler_ack_dhw_set_setpoint_request_id') == boiler_request_id
    - wait_template: >
        {{ states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected'] }}
"""

# N2 — lit le statut, ne corrèle jamais le request_id.
_N2_SANS_REQUEST_ID = """
    - wait_template: >
        {{ states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected', 'timeout'] }}
"""

# N3 — lit le request_id mais ne le compare pas au request_id courant.
_N3_SANS_COMPARAISON = """
    - wait_template: >
        {{
          states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected']
          and states('sensor.boiler_ack_dhw_set_setpoint_request_id') not in ['unknown', '']
        }}
"""

# N4 — conclut encore via la projection legacy *_result.
_N4_RESULT_LEGACY = """
    - wait_template: >
        {{
          states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected']
          and states('sensor.boiler_ack_dhw_set_setpoint_request_id') == boiler_request_id
        }}
    - condition: template
      value_template: "{{ states('sensor.boiler_ack_dhw_set_setpoint_result') == 'applied' }}"
"""

# N5 — la corrélation existe quelque part, mais la branche qui conclut au
# SUCCÈS en est dépourvue. Prouve que C5 seul ne suffirait pas.
_N5_SUCCES_NON_CORRELE = _POSITIF + """
        - conditions:
            - condition: template
              value_template: >
                {{ states('sensor.boiler_ack_dhw_set_setpoint_status') == 'applied' }}
"""

# Faux positifs à ne pas produire : comparaison en ordre inverse, et
# corrélation par relecture du helper plutôt que par la variable de script.
_FP_ORDRE_INVERSE = """
    - wait_template: >
        {{
          boiler_request_id == states('sensor.boiler_ack_dhw_set_setpoint_request_id')
          and states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected']
        }}
"""

_FP_VIA_HELPER = """
    - wait_template: >
        {{
          states('sensor.boiler_ack_dhw_set_setpoint_status') in ['applied', 'rejected']
          and states('sensor.boiler_ack_dhw_set_setpoint_request_id') == states('input_text.boiler_req_dhw_set_setpoint')
        }}
"""


def _selftest() -> int:
    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    def codes(text: str) -> set:
        return {v.split(" ", 1)[0] for v in verifier_correlation_role(ROLE_T, text)}

    # Cas positif — aucune violation.
    expect(verifier_correlation_role(ROLE_T, _POSITIF) == [], "positif-0-violation")

    # N1 — corrélation en commentaire seulement : le juge NE DOIT PAS s'en
    # satisfaire (c'est la vacuité que A-4 corrige).
    c1 = codes(_N1_COMMENTAIRE)
    expect("C1" in c1, "N1-commentaire-doit-echouer-C1")
    expect("C2" in c1, "N1-commentaire-doit-echouer-C2")
    expect("C5" in c1, "N1-commentaire-doit-echouer-C5")

    # N2 — statut sans corrélation.
    c2 = codes(_N2_SANS_REQUEST_ID)
    expect("C1" in c2, "N2-sans-request_id-C1")
    expect("C2" in c2, "N2-sans-request_id-C2")
    expect("C5" in c2, "N2-sans-request_id-C5")

    # N3 — request_id lu mais non comparé au request_id courant.
    c3 = codes(_N3_SANS_COMPARAISON)
    expect("C1" not in c3, "N3-request_id-bien-lu")
    expect("C2" in c3, "N3-sans-comparaison-C2")
    expect("C5" in c3, "N3-sans-comparaison-C5")

    # N4 — conclusion via *_result legacy.
    expect("C4" in codes(_N4_RESULT_LEGACY), "N4-result-legacy-C4")

    # N5 — succès non corrélé dans une branche, malgré une corrélation ailleurs.
    c5 = codes(_N5_SUCCES_NON_CORRELE)
    expect("C5" not in c5, "N5-C5-satisfait-ailleurs")
    expect("C6" in c5, "N5-succes-non-correle-C6")

    # Faux positifs à éviter.
    expect(verifier_correlation_role(ROLE_T, _FP_ORDRE_INVERSE) == [], "fp-ordre-inverse")
    expect(verifier_correlation_role(ROLE_T, _FP_VIA_HELPER) == [], "fp-via-helper")

    # Le retrait des projections legacy (C49, Lot 3) ne doit rien changer :
    # T03 ne lit ni *_ts, ni *_correlation, ni *_result côté template.
    expect(
        verifier_correlation_role(ROLE_T, _POSITIF)
        == verifier_correlation_role(ROLE_T, _POSITIF + "\n# *_ts, *_correlation, *_result retirés\n"),
        "lot3-neutre",
    )

    # Outillage : le retrait de commentaires ne doit pas amputer une chaîne
    # quotée contenant un '#'.
    expect(
        strip_yaml_comments("value: \"a # b\"  # vrai commentaire").strip()
        == 'value: "a # b"',
        "strip-commentaires-quotes",
    )

    if failures:
        print("❌ AUTO-TESTS CHECKER BOILER_TRANSACTIONNEL EN ÉCHEC")
        for f in failures:
            print(f"  • {f}")
        return 2
    print("✅ AUTO-TESTS CHECKER BOILER_TRANSACTIONNEL OK (T03 — corrélation)")
    return 0


# ──────────────────────────────────────────────────────────────
# Exécution
# ──────────────────────────────────────────────────────────────

TESTS = [
    test_request_helpers_declared,
    test_transaction_sensors_declared,
    test_transaction_sensors_correlate_request_id,
    test_script_ecs_checks_bridge_online,
    test_script_ecs_writes_helper_before_publish,
    test_script_ecs_verifies_helper_post_write,
    test_script_chauffage_checks_bridge_online,
    test_script_chauffage_writes_helper_before_publish,
    test_retry_automations_declared,
    test_retry_not_in_executive_scripts,
    test_non_retryable_commands_absent_from_retry_automations,
    test_guard_sensors_declared,
    test_guard_stale_declared,
    test_guard_stale_based_on_last_run,
    test_no_guard_data_in_boiler_logic,
    test_retry_helpers_declared,
]

if __name__ == "__main__":
    # Auto-test du juge — détecté par scripts/ci/run_checkers.py, qui le lance
    # avant le checker lui-même. Régression du juge => exit 2.
    if "--selftest" in sys.argv:
        sys.exit(_selftest())

    print("Arsenal — Contrat Socle Transactionnel Boiler Bridge\n")
    for test in TESTS:
        test()

    if ERRORS:
        print("\n❌ CONTRAT BOILER_TRANSACTIONNEL NON CONFORME\n")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT BOILER_TRANSACTIONNEL CONFORME")