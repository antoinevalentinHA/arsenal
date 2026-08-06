#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : ECS Désinfection au retour de vacances
Contrat (source normative) : 00_documentation_arsenal/contrats/ecs/09_invariants_et_interdictions.md (§2 invariants absolus, §3 interdictions)

Couvre (ECS-DESINF-1) les invariants les plus critiques du sous-système
désinfection-retour, jusqu'ici non instrumentés :
  - légitimité établie EXCLUSIVEMENT par `timer.finished` de
    `timer.vacances_longues_ecs`, JAMAIS par `timer.cancel` (§2) ;
  - écrivain souverain UNIQUE par transition de
    `input_boolean.ecs_desinfection_retour_due` (pose ON / consommation OFF, §2) ;
  - idempotence : au plus une exécution par légitimité (§2) ;
  - état souverain PERSISTANT — aucun `initial` (§2) ;
  - décision NE lit JAMAIS l'attribut `remaining` / `finishes_at` (§3).

Couvre aussi (ECS-DESINF-2) la garde préventive de cardinalité de
`input_select.mode_maison` : le couplage `Vacances → Normal` du consommateur
n'est sûr qu'à 2 modes — toute extension doit trip la CI (T10).

Logique Arsenal habituelle : ERROR => exit 1 ; conforme => exit 0.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []


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


def ok(label: str) -> None:
    print(f"  ✔ {label}")


# ---------------------------------------------------------------------------
# Chemins & entités canoniques
# ---------------------------------------------------------------------------

POSER = ROOT / "11_automations/ecs/desinfection_retour_pose_due.yaml"
# Lanceur + réconciliation (Runtime Lot 2) : pose le verdict et lance le cycle ;
# n'écrit PLUS la dette (la consommation est portée par le verdict de complétion).
LAUNCHER = ROOT / "11_automations/ecs/desinfection_retour_vacances.yaml"
# Consommateur souverain de la dette (OFF) = automation de verdict de complétion (…033).
CONSUMER = ROOT / "11_automations/ecs/desinfection_retour_verdict.yaml"
SOVEREIGN_FILE = ROOT / "05_input_booleans/ecs/desinfection_retour_due.yaml"
TIMER_FILE = ROOT / "08_timers/ecs/desinfection_vacances.yaml"

# Vérité de séquence (Runtime Lot 2)
VERDICT_HELPER = ROOT / "06_input_selects/ecs/desinfection_retour_verdict.yaml"
VEILLE_HEBDO = ROOT / "11_automations/ecs/veilles/veille_desinfection.yaml"
VERDICT_ENTITY = "input_select.ecs_desinfection_retour_verdict"
FROZEN_RESUME = "ecs_resume_dernier_cycle_fige"
VERDICT_OPTIONS = ["en_attente", "en_cours", "reussite", "echec", "timeout", "preuve_indisponible"]

# Circulation post-réussite — réutilisation de la primitive de bouclage existante
BOUCLAGE_PRIMITIVE = "script.bouclage_ecs_5_minutes"
BOUCLAGE_FLAG = "bouclage_ecs_5_minutes_en_cours"

# Borne de timeout T-B — fenêtre d'inertie post-cycle et verrou de cycle
INERTIE_TIMER = "timer.fenetre_inertie_chauffe_ecs"
CYCLE_LOCK = "input_boolean.ecs_cycle_en_cours"

SCAN_DIRS = [ROOT / "11_automations", ROOT / "10_scripts"]

SOVEREIGN = "ecs_desinfection_retour_due"          # input_boolean (clé + suffixe)
TIMER_ENTITY = "timer.vacances_longues_ecs"
TIMER_KEY = "vacances_longues_ecs"

# ECS-DESINF-2 — garde de cardinalité du contexte de retour
MODE_MAISON_FILE = ROOT / "06_input_selects/modes/mode_maison.yaml"
MODE_MAISON_MODES = {"Normal", "Vacances"}         # cardinalité verrouillée (2 modes)


def files_calling_service_on_target(service: str, target: str) -> set[Path]:
    """
    Retourne l'ensemble des fichiers YAML (automations + scripts) où une ligne
    invoque `service` (ex. input_boolean.turn_on), avec `target` sur la même
    ligne ou dans les 5 lignes suivantes (bloc target/entity_id). Commentaires
    ignorés — seule la logique effective compte.
    """
    svc = re.compile(re.escape(service))
    tgt = re.compile(re.escape(target))
    hits: set[Path] = set()
    for scan_dir in SCAN_DIRS:
        for path in yaml_files(scan_dir):
            lines = strip_comments(read(path)).splitlines()
            for i, line in enumerate(lines):
                if not svc.search(line):
                    continue
                window = lines[i:i + 6]
                if any(tgt.search(w) for w in window):
                    hits.add(path)
                    break
    return hits


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# ---------------------------------------------------------------------------
# T01 — Poser présent et déclenché par timer.finished du timer souverain (§2)
# ---------------------------------------------------------------------------

def test_poser_present_declenche_par_finished():
    """
    §2 : la légitimité est établie EXCLUSIVEMENT par `timer.finished` de
    `timer.vacances_longues_ecs`. L'automation de pose doit exister et se
    déclencher sur cet événement pour ce timer précis.
    """
    check(POSER.is_file(), f"T01 — automation de pose absente ({rel(POSER)})")
    content = strip_comments(read(POSER))
    check(
        "timer.finished" in content,
        "T01 — la pose ne se déclenche pas sur `timer.finished` (§2)",
    )
    check(
        TIMER_ENTITY in content,
        f"T01 — la pose ne cible pas `{TIMER_ENTITY}` (§2)",
    )
    ok("T01 — pose présente, déclenchée par timer.finished du timer souverain (§2)")


# ---------------------------------------------------------------------------
# T02 — Aucune légitimité par timer.cancel (§2)
# ---------------------------------------------------------------------------

def test_aucune_legitimite_par_cancel():
    """
    §2 : la légitimité n'est JAMAIS établie par `timer.cancel` — complétion et
    annulation doivent rester discernables. Aucun écrivain ON de l'état souverain
    ne doit référencer `timer.cancel`.
    """
    on_writers = files_calling_service_on_target("input_boolean.turn_on", SOVEREIGN)
    for path in sorted(on_writers):
        content = strip_comments(read(path))
        check(
            "timer.cancel" not in content,
            f"T02 — un écrivain ON de {SOVEREIGN} référence `timer.cancel` "
            f"({rel(path)}) — légitimité par annulation interdite (§2)",
        )
    ok("T02 — aucune légitimité de désinfection-retour par timer.cancel (§2)")


# ---------------------------------------------------------------------------
# T03 — Écrivain ON unique = la pose (§2 souveraineté)
# ---------------------------------------------------------------------------

def test_ecrivain_on_unique():
    """
    §2 : `input_boolean.ecs_desinfection_retour_due` a un écrivain souverain
    unique par transition. La transition ON (pose) doit avoir pour unique
    auteur l'automation de pose.
    """
    on_writers = files_calling_service_on_target("input_boolean.turn_on", SOVEREIGN)
    check(
        POSER in on_writers,
        f"T03 — la pose n'écrit pas ON {SOVEREIGN} ({rel(POSER)})",
    )
    extra = sorted(rel(p) for p in on_writers if p != POSER)
    check(
        not extra,
        f"T03 — écrivain(s) ON supplémentaire(s) de {SOVEREIGN} : {extra} "
        f"— souveraineté unique violée (§2)",
    )
    ok("T03 — écrivain ON unique de l'état souverain = la pose (§2)")


# ---------------------------------------------------------------------------
# T04 — Écrivain OFF unique = le consommateur (§2 souveraineté)
# ---------------------------------------------------------------------------

def test_ecrivain_off_unique():
    """
    §2 : la transition OFF (réinitialisation à la consommation) doit avoir pour
    unique auteur l'automation consommatrice de la désinfection-retour.
    """
    off_writers = files_calling_service_on_target("input_boolean.turn_off", SOVEREIGN)
    check(
        CONSUMER in off_writers,
        f"T04 — le consommateur n'écrit pas OFF {SOVEREIGN} ({rel(CONSUMER)})",
    )
    extra = sorted(rel(p) for p in off_writers if p != CONSUMER)
    check(
        not extra,
        f"T04 — écrivain(s) OFF supplémentaire(s) de {SOVEREIGN} : {extra} "
        f"— souveraineté unique violée (§2)",
    )
    ok("T04 — écrivain OFF unique de l'état souverain = le consommateur (§2)")


# ---------------------------------------------------------------------------
# T05 — Aucune écriture diffuse (toggle) de l'état souverain (§2)
# ---------------------------------------------------------------------------

def test_aucun_toggle_souverain():
    """
    §2 : l'écriture est unique PAR TRANSITION (ON / OFF explicites). Un
    `input_boolean.toggle` sur l'état souverain rendrait la transition
    indéterminée et briserait la souveraineté.
    """
    togglers = files_calling_service_on_target("input_boolean.toggle", SOVEREIGN)
    check(
        not togglers,
        f"T05 — toggle diffus de {SOVEREIGN} : {sorted(rel(p) for p in togglers)} "
        f"— transition non déterministe interdite (§2)",
    )
    ok("T05 — aucune écriture diffuse (toggle) de l'état souverain (§2)")


# ---------------------------------------------------------------------------
# T06 — Idempotence : le consommateur est gardé par l'état ON et le consomme (§2)
# ---------------------------------------------------------------------------

def test_idempotence_consommation():
    """
    §2 : la désinfection-retour est idempotente — au plus une exécution par
    légitimité établie. Le consommateur doit (a) se conditionner à l'état
    souverain == on, et (b) le remettre à off (consommation) dans son action.
    """
    lines = strip_comments(read(CONSUMER)).splitlines()

    # (a) condition d'état sur le souverain == on : occurrence du souverain
    #     avec un `state: on` dans une fenêtre proche.
    gated = False
    on_re = re.compile(r"state\s*:\s*['\"]?on['\"]?")
    for i, line in enumerate(lines):
        if SOVEREIGN in line and "turn_off" not in line and "turn_on" not in line:
            lo = max(0, i - 4)
            if any(on_re.search(w) for w in lines[lo:i + 5]):
                gated = True
                break
    check(gated, f"T06 — le consommateur n'est pas gardé par {SOVEREIGN} == on (§2)")

    # (b) consommation : écrit OFF le souverain
    off_writers = files_calling_service_on_target("input_boolean.turn_off", SOVEREIGN)
    check(
        CONSUMER in off_writers,
        f"T06 — le consommateur ne consomme pas (OFF) {SOVEREIGN} (§2)",
    )
    ok("T06 — idempotence : consommateur gardé par l'état ON et le consomme (§2)")


# ---------------------------------------------------------------------------
# T07 — État souverain persistant : déclaré sans `initial` (§2)
# ---------------------------------------------------------------------------

def test_souverain_sans_initial():
    """
    §2 : l'état souverain est persistant (pas d'`initial`) ; valeur par défaut
    au tout premier démarrage = off (comportement HA natif d'un input_boolean
    sans initial). La déclaration canonique ne doit porter aucune clé `initial`.
    """
    content = read(SOVEREIGN_FILE)
    check(
        bool(re.search(rf"^\s*{re.escape(SOVEREIGN)}\s*:", content, re.MULTILINE)),
        f"T07 — {SOVEREIGN} non déclaré dans {rel(SOVEREIGN_FILE)}",
    )
    check(
        not re.search(r"^\s*initial\s*:", strip_comments(content), re.MULTILINE),
        f"T07 — clé `initial` interdite sur {SOVEREIGN} "
        f"({rel(SOVEREIGN_FILE)}) — l'état souverain doit rester persistant (§2)",
    )
    ok("T07 — état souverain persistant, sans `initial` (§2)")


# ---------------------------------------------------------------------------
# T08 — La décision ne lit jamais `remaining` / `finishes_at` (§3)
# ---------------------------------------------------------------------------

def test_pas_de_lecture_remaining():
    """
    §3 : il est interdit de fonder la décision de désinfection-retour sur
    l'attribut `remaining` du timer (non fiable à l'état `idle`). Par extension,
    `finishes_at` relève de la même dépendance temporelle fragile. Ni la pose ni
    le consommateur ne doivent lire ces attributs.
    """
    for path in (POSER, CONSUMER, LAUNCHER):
        content = strip_comments(read(path))
        check(
            "remaining" not in content,
            f"T08 — lecture de `remaining` détectée dans {rel(path)} "
            f"(interdit §3 — non fiable à l'état idle)",
        )
        check(
            "finishes_at" not in content,
            f"T08 — lecture de `finishes_at` détectée dans {rel(path)} "
            f"(dépendance temporelle fragile, §3)",
        )
    ok("T08 — décision sans lecture de `remaining` / `finishes_at` (§3)")


# ---------------------------------------------------------------------------
# T09 — Timer souverain déclaré et référencé (§2 socle de légitimité)
# ---------------------------------------------------------------------------

def test_timer_souverain_declare():
    """
    §2 : la légitimité repose sur `timer.vacances_longues_ecs`. Le timer doit
    être déclaré dans son fichier canonique et référencé par la pose.
    """
    content = read(TIMER_FILE)
    check(
        bool(re.search(rf"^\s*{re.escape(TIMER_KEY)}\s*:", content, re.MULTILINE)),
        f"T09 — timer `{TIMER_KEY}` non déclaré dans {rel(TIMER_FILE)}",
    )
    check(
        TIMER_ENTITY in strip_comments(read(POSER)),
        f"T09 — la pose ne référence pas `{TIMER_ENTITY}`",
    )
    ok("T09 — timer souverain déclaré et référencé par la pose (§2)")


# ---------------------------------------------------------------------------
# T10 — Garde de cardinalité de mode_maison (ECS-DESINF-2)
# ---------------------------------------------------------------------------

def test_mode_maison_cardinalite():
    """
    ECS-DESINF-2 — Robustesse du couplage à `mode_maison`.

    Le consommateur (10250000000021) se déclenche sur la transition
    `Vacances → Normal`. Ce couplage n'est sûr que tant que `mode_maison`
    possède exactement 2 modes {Normal, Vacances} : l'ajout d'un 3ᵉ mode le
    fragilise (un retour de Vacances pourrait aboutir ailleurs que `Normal`,
    et la désinfection-retour ne se déclencherait pas).

    Garde préventive : toute extension de `mode_maison` doit trip la CI et
    forcer une revue explicite du trigger de la désinfection-retour (trigger
    plus robuste, ou mise à jour coordonnée assumée).
    """
    body = strip_comments(read(MODE_MAISON_FILE))
    m = re.search(r"options\s*:\s*(.*)$", body, re.DOTALL)
    options = set(re.findall(r"-\s+([A-Za-z0-9_]+)", m.group(1))) if m else set()
    check(
        options == MODE_MAISON_MODES,
        f"T10 — cardinalité de mode_maison modifiée : {sorted(options)} "
        f"≠ {sorted(MODE_MAISON_MODES)} — revoir le couplage Vacances→Normal "
        f"de la désinfection-retour (ECS-DESINF-2)",
    )
    ok("T10 — cardinalité mode_maison verrouillée {Normal, Vacances} (ECS-DESINF-2)")


# ---------------------------------------------------------------------------
# Runtime Lot 2 — consommation post-verdict, corrélation, déconfliction
# Réalise les invariants « désinfection au retour » de 09 §2 et le mécanisme
# souverain de 05 §3.2/§3.3. Détection sémantique (commentaires retirés),
# sans dépendance externe (le runner CI n'a pas PyYAML).
# ---------------------------------------------------------------------------

_OPT_RE = lambda opt: re.compile(r"option\s*:\s*['\"]?" + re.escape(opt) + r"['\"]?")
_STATE_RE = lambda opt: re.compile(r"state\s*:\s*['\"]?" + re.escape(opt) + r"['\"]?")


def test_dette_consommee_seulement_sur_reussite():
    """
    §2/§3.3 : la dette n'est éteinte QUE dans un contexte de réussite corrélée
    (verdict `reussite`), jamais après un simple appel de script. Chaque
    `turn_off` de la dette doit être précédé d'un basculement de verdict
    `reussite` (fenêtre proche).
    """
    lines = strip_comments(read(CONSUMER)).splitlines()
    found_gated = False
    for i, line in enumerate(lines):
        if "input_boolean.turn_off" not in line:
            continue
        window = "\n".join(lines[max(0, i - 10):i + 6])
        if SOVEREIGN not in window:
            continue
        preceding = "\n".join(lines[max(0, i - 14):i])
        if _OPT_RE("reussite").search(preceding):
            found_gated = True
        else:
            check(False, f"T11 — turn_off de {SOVEREIGN} non gardé par le verdict "
                         f"`reussite` ({rel(CONSUMER)}, ligne ~{i + 1})")
    check(found_gated, f"T11 — aucune consommation de {SOVEREIGN} gardée par `reussite` "
                       f"dans {rel(CONSUMER)}")
    ok("T11 — dette consommée uniquement sur réussite corrélée (§2/§3.3)")


def test_launcher_ne_consomme_pas():
    """§3.2 : le lanceur (…021) n'écrit JAMAIS la dette OFF — la consommation
    immédiate après l'appel du script est interdite."""
    off_writers = files_calling_service_on_target("input_boolean.turn_off", SOVEREIGN)
    check(
        LAUNCHER not in off_writers,
        f"T12 — le lanceur {rel(LAUNCHER)} écrit OFF {SOVEREIGN} — consommation "
        f"immédiate après l'appel du script interdite (§3.2)",
    )
    ok("T12 — le lanceur ne consomme pas la dette (§3.2)")


def test_launcher_pose_en_cours_avant_lancement():
    """§3.3 : le lanceur pose le verdict `en_cours` AVANT d'appeler le cycle."""
    body = strip_comments(read(LAUNCHER))
    m_en_cours = _OPT_RE("en_cours").search(body)
    m_call = re.search(r"script\.chauffage_ecs_cycle", body)
    check(m_en_cours is not None, "T13 — le lanceur ne pose pas le verdict `en_cours`")
    check(m_call is not None, "T13 — le lanceur n'appelle pas `script.chauffage_ecs_cycle`")
    if m_en_cours and m_call:
        check(m_en_cours.start() < m_call.start(),
              "T13 — le verdict `en_cours` doit être posé AVANT l'appel du cycle")
    ok("T13 — lanceur : `en_cours` posé avant le lancement (§3.3)")


def test_launcher_reprise_boot_gardee():
    """§3.3 / 10 §4.1 : le lanceur porte une réconciliation au démarrage
    (trigger `systeme_stable → on` ou `homeassistant: start`)."""
    body = strip_comments(read(LAUNCHER))
    check(
        ("systeme_stable" in body) or ("homeassistant" in body),
        "T14 — le lanceur n'a aucune reprise au démarrage (systeme_stable / homeassistant)",
    )
    ok("T14 — reprise au démarrage présente dans le lanceur (10 §4.1)")


def test_launcher_verrou_et_anti_double():
    """Déconfliction : le lanceur pré-vérifie le verrou `ecs_cycle_en_cours` et
    empêche un double lancement (garde d'état sur le verdict `en_cours`)."""
    body = strip_comments(read(LAUNCHER))
    check("ecs_cycle_en_cours" in body,
          "T15 — le lanceur ne pré-vérifie pas le verrou `ecs_cycle_en_cours`")
    check(_STATE_RE("en_cours").search(body) is not None,
          "T15 — le lanceur ne garde pas contre une tentative déjà `en_cours` (anti-double)")
    ok("T15 — lanceur : pré-vérif verrou + anti-double-lancement")


def test_verdict_helper_declare():
    """05 §3.3 : l'input_select verdict est déclaré avec les 6 options canoniques."""
    body = read(VERDICT_HELPER)
    check(
        bool(re.search(r"^\s*ecs_desinfection_retour_verdict\s*:", body, re.MULTILINE)),
        f"T16 — verdict `ecs_desinfection_retour_verdict` non déclaré ({rel(VERDICT_HELPER)})",
    )
    for opt in VERDICT_OPTIONS:
        check(re.search(rf"-\s*{re.escape(opt)}\b", body) is not None,
              f"T16 — option `{opt}` absente du verdict")
    ok("T16 — verdict input_select déclaré (6 options, 05 §3.3)")


def test_deconfliction_hebdo():
    """09 §2 / 05 §3.4 : l'hebdomadaire (…002) s'abstient tant qu'une tentative
    de retour est active (garde sur le verdict `en_cours`)."""
    body = strip_comments(read(VEILLE_HEBDO))
    check(
        VERDICT_ENTITY in body and _STATE_RE("en_cours").search(body) is not None,
        f"T17 — la veille hebdomadaire ne se déconflicte pas du retour "
        f"(garde `{VERDICT_ENTITY} == en_cours` absente) — {rel(VEILLE_HEBDO)}",
    )
    ok("T17 — déconfliction hebdo par le verdict de retour (09 §2 / 05 §3.4)")


def test_timeout_distinct_de_reussite():
    """§3.3 : la branche timeout existe et NE consomme PAS la dette
    (timeout ≠ réussite ; aucun fallback vers `reussite`)."""
    lines = strip_comments(read(CONSUMER)).splitlines()
    body = "\n".join(lines)
    check(_OPT_RE("timeout").search(body) is not None,
          "T18 — le verdict de complétion ne produit pas d'état `timeout`")
    for i, line in enumerate(lines):
        if _OPT_RE("timeout").search(line):
            window = "\n".join(lines[i:i + 8])
            check(
                not ("input_boolean.turn_off" in window and SOVEREIGN in window),
                "T18 — la branche `timeout` consomme la dette (timeout traité comme réussite)",
            )
    ok("T18 — timeout distinct de réussite, dette conservée (§3.3)")


def test_correlation_fin_canonique():
    """§3.3 : la réussite est corrélée — le verdict lit le résumé figé
    (mode désinfection) ET la complétion canonique, pas le seul signal global."""
    body = strip_comments(read(CONSUMER))
    check("ecs_fin_cycle_signal" in body,
          "T19 — le verdict n'observe pas la complétion canonique `ecs_fin_cycle_signal`")
    check(FROZEN_RESUME in body,
          f"T19 — le verdict ne lit pas le résumé figé `{FROZEN_RESUME}` (corrélation)")
    check("desinfection" in body,
          "T19 — le verdict ne corrèle pas sur `mode == desinfection`")
    ok("T19 — réussite corrélée (résumé figé + complétion canonique) (§3.3)")


# ---------------------------------------------------------------------------
# Circulation bouclage 5 min après réussite (réutilisation de la primitive)
# Invariants : appel du primitif UNIQUEMENT dans la branche `reussite` corrélée ;
# aucun appel sur echec/timeout/preuve_indisponible ; ECS ne pilote jamais la
# pompe ; unicité par les gardes existantes. Détection sémantique, sans PyYAML.
# ---------------------------------------------------------------------------

def _index_of(lines, needle):
    return next((i for i, l in enumerate(lines) if needle in l), None)


def test_bouclage_appele_dans_reussite():
    """L'appel de `script.bouclage_ecs_5_minutes` existe et suit le verdict
    `reussite` ET la corrélation (branche réussite corrélée)."""
    lines = strip_comments(read(CONSUMER)).splitlines()
    idx = _index_of(lines, BOUCLAGE_PRIMITIVE)
    check(idx is not None, f"T20 — appel de `{BOUCLAGE_PRIMITIVE}` introuvable dans {rel(CONSUMER)}")
    if idx is not None:
        preceding = "\n".join(lines[:idx])
        check(_OPT_RE("reussite").search(preceding) is not None,
              "T20 — l'appel du bouclage n'est pas dans la branche `reussite`")
        check("desinfection" in preceding and FROZEN_RESUME in preceding,
              "T20 — l'appel du bouclage n'est pas gardé par la corrélation (mode désinfection/résumé figé)")
    ok("T20 — bouclage appelé dans la branche `reussite` corrélée")


def test_bouclage_pas_dans_branches_negatives():
    """Aucun appel du primitif dans les fenêtres `echec` / `timeout` /
    `preuve_indisponible` (le bouclage ne part que sur réussite)."""
    lines = strip_comments(read(CONSUMER)).splitlines()
    for opt in ("echec", "timeout", "preuve_indisponible"):
        for i, line in enumerate(lines):
            if _OPT_RE(opt).search(line):
                window = "\n".join(lines[i:i + 12])
                check(BOUCLAGE_PRIMITIVE not in window,
                      f"T21 — `{BOUCLAGE_PRIMITIVE}` appelé dans une branche `{opt}` (interdit)")
    ok("T21 — aucun bouclage sur echec / timeout / preuve_indisponible")


def test_ecs_ne_pilote_pas_le_switch():
    """ECS ne pilote JAMAIS `switch.prise_bouclage` directement ; aucun nouvel
    écrivain du switch n'est introduit côté ECS."""
    for path in (LAUNCHER, CONSUMER):
        body = strip_comments(read(path))
        bad = re.search(r"switch\.turn_(on|off)[\s\S]{0,120}prise_bouclage", body)
        check(bad is None,
              f"T22 — {rel(path)} pilote directement `switch.prise_bouclage` "
              f"(interdit ; passer par `{BOUCLAGE_PRIMITIVE}`)")
    ok("T22 — ECS n'écrit jamais le switch (primitive existante uniquement)")


def test_appel_unique_par_reussite():
    """Unicité de l'appel : garde par les vérités EXISTANTES — l'automation de
    finalisation se conditionne à `verdict == en_cours` ET `dette == on`
    (retombées après consommation), sans nouveau verrou. Un seul appel figure
    dans le fichier."""
    body = strip_comments(read(CONSUMER))
    check(_STATE_RE("en_cours").search(body) is not None,
          "T23 — garde d'unicité absente : le finaliseur ne se conditionne pas à `verdict == en_cours`")
    check(re.search(r"entity_id\s*:\s*input_boolean\.ecs_desinfection_retour_due", body) is not None
          and _STATE_RE("on").search(body) is not None,
          "T23 — garde d'unicité absente : le finaliseur ne se conditionne pas à `dette == on`")
    check(body.count(BOUCLAGE_PRIMITIVE) == 1,
          f"T23 — `{BOUCLAGE_PRIMITIVE}` apparaît {body.count(BOUCLAGE_PRIMITIVE)} fois "
          f"(attendu 1 : un seul appel par réussite)")
    ok("T23 — appel unique par réussite via les gardes existantes")


# ---------------------------------------------------------------------------
# T24 — Le timeout n'est jamais posé au démarrage de la tentative (§3.3)
# ---------------------------------------------------------------------------

def test_timeout_non_pose_au_demarrage_de_la_tentative():
    """
    §3.3 — `timeout` signifie « attente bornée expirée sans preuve d'atteinte ».
    Il ne doit JAMAIS pouvoir être posé au démarrage de la tentative elle-même.

    Défaut fermé ici : `10250000000027` annule la fenêtre d'inertie sur CHAQUE
    transition `ecs_cycle_en_cours` off→on, et Home Assistant émet
    `timer.cancelled` même sur un timer déjà `idle`. Un trigger sur l'événement
    brut posait donc `timeout` au démarrage du cycle de la tentative, rendant
    `reussite` structurellement inatteignable et la dette inconsommable.

    Le finaliseur doit donc :
      (a) ne pas s'armer sur l'événement `timer.cancelled` ;
      (b) détecter la disparition de fenêtre par la transition d'état
          `active` → `idle` (seule une fenêtre réellement ouverte la produit) ;
      (c) discriminer préemption / échéance naturelle par le verrou de cycle
          `on` (seule une reprise de cycle annule la fenêtre ; à l'échéance
          naturelle le verrou est `off` et la complétion canonique suit).
    """
    body = strip_comments(read(CONSUMER))
    lines = body.splitlines()

    # (a) — l'événement brut est structurellement ambigu : interdit
    check(
        "timer.cancelled" not in body,
        f"T24 — {rel(CONSUMER)} s'arme sur l'événement `timer.cancelled` : HA l'émet "
        f"même sur un timer `idle` et 10250000000027 annule la fenêtre au démarrage "
        f"de CHAQUE cycle ⇒ `timeout` posé sur la tentative elle-même",
    )

    # (b) — trigger d'état qualifié `active` → `idle` sur la fenêtre d'inertie
    trigger_ok = False
    for i, line in enumerate(lines):
        if INERTIE_TIMER not in line:
            continue
        window = "\n".join(lines[max(0, i - 3):i + 5])
        if (re.search(r"platform\s*:\s*state", window)
                and re.search(r"from\s*:\s*['\"]?active['\"]?", window)
                and re.search(r"to\s*:\s*['\"]?idle['\"]?", window)):
            trigger_ok = True
            break
    check(
        trigger_ok,
        f"T24 — {rel(CONSUMER)} ne détecte pas la disparition de la fenêtre par "
        f"transition d'état `active` → `idle` de `{INERTIE_TIMER}` (une annulation "
        f"de timer `idle` ne doit pas pouvoir armer le timeout)",
    )

    # (c) — branche préemption gardée par le verrou de cycle `on`
    branch_ok = False
    for i, line in enumerate(lines):
        if not re.search(r"id\s*:\s*['\"]?preemption['\"]?", line):
            continue
        preceding = "\n".join(lines[max(0, i - 3):i])
        if "condition" not in preceding or "trigger" not in preceding:
            continue  # définition du trigger, pas la branche du `choose`
        window = lines[i:i + 10]
        for j, wline in enumerate(window):
            if CYCLE_LOCK not in wline:
                continue
            near = "\n".join(window[j:j + 3])
            if re.search(r"state\s*:\s*['\"]?on['\"]?\s*$", near, re.MULTILINE):
                branch_ok = True
                break
    check(
        branch_ok,
        f"T24 — la branche `preemption` de {rel(CONSUMER)} n'est pas gardée par "
        f"`{CYCLE_LOCK} == on` : une échéance naturelle de la fenêtre serait "
        f"traitée comme un timeout (perte de la réussite corrélée)",
    )

    ok("T24 — timeout jamais posé au démarrage de la tentative (§3.3)")


# ---------------------------------------------------------------------------
# Registre
# ---------------------------------------------------------------------------

TESTS = [
    test_poser_present_declenche_par_finished,
    test_aucune_legitimite_par_cancel,
    test_ecrivain_on_unique,
    test_ecrivain_off_unique,
    test_aucun_toggle_souverain,
    test_idempotence_consommation,
    test_souverain_sans_initial,
    test_pas_de_lecture_remaining,
    test_timer_souverain_declare,
    test_mode_maison_cardinalite,
    test_dette_consommee_seulement_sur_reussite,
    test_launcher_ne_consomme_pas,
    test_launcher_pose_en_cours_avant_lancement,
    test_launcher_reprise_boot_gardee,
    test_launcher_verrou_et_anti_double,
    test_verdict_helper_declare,
    test_deconfliction_hebdo,
    test_timeout_distinct_de_reussite,
    test_correlation_fin_canonique,
    test_bouclage_appele_dans_reussite,
    test_bouclage_pas_dans_branches_negatives,
    test_ecs_ne_pilote_pas_le_switch,
    test_appel_unique_par_reussite,
    test_timeout_non_pose_au_demarrage_de_la_tentative,
]

if __name__ == "__main__":
    print("Arsenal — Contrat ECS Désinfection au retour de vacances\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT ECS_DESINFECTION_RETOUR NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT ECS_DESINFECTION_RETOUR CONFORME")
