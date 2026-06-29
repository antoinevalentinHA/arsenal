#!/usr/bin/env python3
"""
Arsenal — Validation contractuelle : Présence (séparation & confinement)
Script   : scripts/arsenal_contracts/check_presence_contracts.py

Instrumente UNIQUEMENT des invariants déjà vrais (anti-régression) :

  R1 — Séparation confort <-> sûreté
       - presence_famille_unifiee / presence_confort_thermique_stabilisee
         ne lisent NI presence_famille_securite_confirmee_alarme NI alarm_control_panel.*
       - clim / chauffage ne lisent NI presence_famille_securite (brut)
         NI presence_famille_securite_confirmee_alarme
  R2 — Confinement de binary_sensor.presence_famille_securite_confirmee_alarme
       au seul périmètre alarme runtime (définisseur exclu ; Lovelace NON autorisé
       dans cette première passe).
  R3 — Voies armement / désarmement alarme verrouillées.

Sources normatives citées :
  - 00_documentation_arsenal/contrats/alarme/30_decision_centrale.md
  - 00_documentation_arsenal/contrats/presence.md
  - 00_documentation_arsenal/architecture/presence/presence.md
  - 00_documentation_arsenal/audits/02_constats/transverses/cadrage_dette_modelisation_presence.md

Lecture seule : ce script n'écrit, ne crée et ne supprime aucun fichier.
Code de sortie : 0 = conforme, 1 = violation(s), 2 = échec des auto-tests internes.

Usage :
  python scripts/arsenal_contracts/check_presence_contracts.py
  python scripts/arsenal_contracts/check_presence_contracts.py --selftest
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Racine du repo Arsenal
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Entités canoniques
# ---------------------------------------------------------------------------
ENT_CONFIRMEE   = "binary_sensor.presence_famille_securite_confirmee_alarme"
ENT_ABSENCE_CONFIRMEE = "binary_sensor.presence_famille_securite_absence_confirmee_alarme"
ENT_BRUT        = "binary_sensor.presence_famille_securite"
PREFIX_PANEL    = "alarm_control_panel."

# Fichiers définisseurs des projections confirmées (exclus de R2).
F_DEFINISSEUR = REPO_ROOT / "12_template_sensors/alarme/presence_securite_confirmee.yaml"
F_DEFINISSEUR_ABSENCE = REPO_ROOT / "12_template_sensors/alarme/presence_securite_absence_confirmee.yaml"

# Cœur décisionnel alarme (R3).
F_DECISION    = REPO_ROOT / "10_scripts/alarme/decision_centrale.yaml"
F_ARMEMENT    = REPO_ROOT / "12_template_sensors/alarme/armement_possible.yaml"

# R1 — fichiers "vérité confort" qui ne doivent pas importer la sûreté/l'alarme.
R1_FICHIERS_CONFORT = [
    REPO_ROOT / "12_template_sensors/presence/global.yaml",
    REPO_ROOT / "12_template_sensors/presence/confort_thermique_stabilisee.yaml",
]

# R1 — dossiers confort (clim/chauffage) qui ne doivent pas lire la sûreté.
R1_DOSSIERS_CONFORT = [
    REPO_ROOT / "12_template_sensors/climatisation",
    REPO_ROOT / "11_automations/climatisation",
    REPO_ROOT / "10_scripts/chauffage",
    REPO_ROOT / "11_automations/chauffage",
    REPO_ROOT / "12_template_sensors/chauffage",
]

# R2 — périmètre alarme runtime autorisé à consommer la projection confirmée.
R2_DOSSIERS_ALARME = [
    REPO_ROOT / "10_scripts/alarme",
    REPO_ROOT / "11_automations/alarme",
    REPO_ROOT / "12_template_sensors/alarme",
]

# R2 — racines runtime à balayer pour détecter toute consommation hors périmètre.
R2_RACINES_RUNTIME = [
    REPO_ROOT / "10_scripts",
    REPO_ROOT / "11_automations",
    REPO_ROOT / "12_template_sensors",
    REPO_ROOT / "02_groups",
    REPO_ROOT / "05_input_booleans",
    REPO_ROOT / "18_lovelace",
]

# Lignes de DÉCLARATION (n'expriment pas une consommation) — ignorées pour R2.
DECL_PREFIXES = ("name:", "unique_id:", "default_entity_id:")

ERRORS: list[str] = []


# ---------------------------------------------------------------------------
# Helpers (idiomes Arsenal : read / yaml_files / active_lines)
# ---------------------------------------------------------------------------

def read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def yaml_files(*directories: Path) -> list[Path]:
    result: list[Path] = []
    for d in directories:
        if d.is_dir():
            result.extend(p for p in d.rglob("*.yaml") if p.is_file())
    return result


def active_lines(content: str) -> list[str]:
    """Lignes hors commentaires YAML pleins (ligne dont le 1er caractère
    non blanc est '#'). Aligne le comportement sur check_alarme_contracts."""
    return [l for l in content.splitlines() if not l.strip().startswith("#")]


def references_entity(content: str, entity: str, *, skip_decl: bool = False) -> bool:
    """Vrai si `entity` (référence QUALIFIÉE binary_sensor.<nom> / alarm_control_panel.)
    apparaît dans une ligne active. Le préfixe qualifiant évite les faux positifs
    sur les noms de variables Jinja (ex. `{% set presence_famille_securite = ... %}`).
    Si skip_decl, ignore les lignes de déclaration d'entité (name/unique_id/...)."""
    # Frontière à GAUCHE = non-mot (évite de matcher un suffixe d'un autre nom) ;
    # à DROITE = \b (l'entité peut être suivie de ', ", ), espace...).
    pattern = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(entity) + r"\b")
    for line in active_lines(content):
        if skip_decl and line.strip().startswith(DECL_PREFIXES):
            continue
        if pattern.search(line):
            return True
    return False


def references_prefix(content: str, prefix: str) -> bool:
    """Vrai si une référence commençant par `prefix` (ex. 'alarm_control_panel.')
    apparaît dans une ligne active."""
    pattern = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(prefix))
    for line in active_lines(content):
        if pattern.search(line):
            return True
    return False


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


# ---------------------------------------------------------------------------
# R1 — Séparation confort <-> sûreté
# ---------------------------------------------------------------------------

def test_r1_confort_n_importe_pas_alarme() -> None:
    """R1-a — les vérités confort ne lisent ni la projection alarme ni le panneau."""
    ok = True
    for f in R1_FICHIERS_CONFORT:
        content = read(f)
        if not content:
            ERRORS.append(f"R1-a — fichier confort introuvable : {rel(f)}")
            ok = False
            continue
        if references_entity(content, ENT_CONFIRMEE):
            ERRORS.append(f"R1-a — {rel(f)} référence {ENT_CONFIRMEE} (séparation confort/sûreté)")
            ok = False
        if references_prefix(content, PREFIX_PANEL):
            ERRORS.append(f"R1-a — {rel(f)} référence {PREFIX_PANEL}* (séparation confort/alarme)")
            ok = False
    if ok:
        print("✔ R1-a — confort (unifiee / stabilisee) sans dépendance alarme")


def test_r1_clim_chauffage_sans_surete() -> None:
    """R1-b — clim/chauffage ne consomment ni le brut sécurité ni la projection alarme."""
    ok = True
    for path in yaml_files(*R1_DOSSIERS_CONFORT):
        content = read(path)
        if references_entity(content, ENT_CONFIRMEE):
            ERRORS.append(f"R1-b — {rel(path)} référence {ENT_CONFIRMEE} (clim/chauffage ne doit pas lire la projection alarme)")
            ok = False
        if references_entity(content, ENT_BRUT):
            ERRORS.append(f"R1-b — {rel(path)} référence {ENT_BRUT} brut (clim/chauffage doit passer par une projection stabilisée)")
            ok = False
    if ok:
        print("✔ R1-b — clim/chauffage sans référence à la présence sécurité brute ni à la projection alarme")


# ---------------------------------------------------------------------------
# R2 — Confinement de la projection confirmée
# ---------------------------------------------------------------------------

def _in_perimetre_alarme(path: Path) -> bool:
    return any(_is_within(path, d) for d in R2_DOSSIERS_ALARME)


def _is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def test_r2_confinement_alarme() -> None:
    """R2 — toute consommation des projections confirmées (présence / absence)
    reste dans le périmètre alarme. Les fichiers définisseurs sont exclus
    (déclaration, pas consommation)."""
    projections = (
        (ENT_CONFIRMEE, F_DEFINISSEUR),
        (ENT_ABSENCE_CONFIRMEE, F_DEFINISSEUR_ABSENCE),
    )
    fuites = []
    for path in yaml_files(*R2_RACINES_RUNTIME):
        content = read(path)
        for entity, definisseur in projections:
            if path.resolve() == definisseur.resolve():
                continue  # définisseur exclu
            # skip_decl : tolère name/unique_id/default_entity_id si l'entité se redéclarait
            if references_entity(content, entity, skip_decl=True):
                if not _in_perimetre_alarme(path):
                    fuites.append((entity, rel(path)))
    if fuites:
        for entity, f in sorted(fuites):
            ERRORS.append(f"R2 — {entity} consommée hors périmètre alarme : {f}")
    else:
        print("✔ R2 — projections confirmées (présence / absence) confinées au périmètre alarme (Lovelace inclus dans le scan)")


# ---------------------------------------------------------------------------
# R3 — Voies armement / désarmement alarme
# ---------------------------------------------------------------------------

def _bloc_variable(content: str, var: str) -> str:
    """Retourne la ligne active déclarant `var:` (ex. 'presence_securite:'), vide sinon."""
    for line in active_lines(content):
        if line.strip().startswith(var):
            return line
    return ""


def test_r3_desarmement_lit_confirmee() -> None:
    """R3-a — presence_securite (déterminant de désarmement) lit la projection confirmée."""
    content = read(F_DECISION)
    if not content:
        ERRORS.append(f"R3-a — fichier introuvable : {rel(F_DECISION)}")
        return
    ligne = _bloc_variable(content, "presence_securite:")
    if not ligne:
        ERRORS.append(f"R3-a — variable 'presence_securite:' absente de {rel(F_DECISION)}")
        return
    pat = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(ENT_CONFIRMEE) + r"\b")
    if not pat.search(ligne):
        ERRORS.append(f"R3-a — 'presence_securite:' ne lit pas {ENT_CONFIRMEE} dans {rel(F_DECISION)}")
    else:
        print("✔ R3-a — désarmement fondé sur la projection confirmée")


def test_r3_desarmement_pas_de_brut() -> None:
    """R3-c — le déterminant de désarmement ne réintroduit pas le signal brut."""
    content = read(F_DECISION)
    if not content:
        return  # déjà signalé par R3-a
    ligne = _bloc_variable(content, "presence_securite:")
    # Référence au brut EXACT, sans matcher le confirmé ni l'absent (frontière droite \b
    # + lookahead négatif pour exclure les suffixes _confirmee_alarme / _absent_...).
    pat_brut = re.compile(
        r"(?<![A-Za-z0-9_.])" + re.escape(ENT_BRUT) + r"\b(?!_)"
    )
    if ligne and pat_brut.search(ligne):
        ERRORS.append(f"R3-c — 'presence_securite:' réintroduit le brut {ENT_BRUT} dans {rel(F_DECISION)} (risque yoyo)")
    else:
        print("✔ R3-c — désarmement ne réintroduit pas la présence sécurité brute")


def test_r3_absence_stable_lit_confirmee() -> None:
    """R3-b — absence_stable lit la projection confirmée d'absence (armement atomique)."""
    content = read(F_DECISION)
    if not content:
        return
    ligne = _bloc_variable(content, "absence_stable:")
    if not ligne:
        ERRORS.append(f"R3-b — variable 'absence_stable:' absente de {rel(F_DECISION)}")
        return
    pat = re.compile(r"(?<![A-Za-z0-9_.])" + re.escape(ENT_ABSENCE_CONFIRMEE) + r"\b")
    if not pat.search(ligne):
        ERRORS.append(f"R3-b — 'absence_stable:' ne lit pas {ENT_ABSENCE_CONFIRMEE} dans {rel(F_DECISION)}")
    else:
        print("✔ R3-b — absence stable fondée sur la projection confirmée d'absence")


def test_r3_armement_lit_confirmee() -> None:
    """R3-b (gate) — l'armement possible référence la projection confirmée d'absence."""
    content = read(F_ARMEMENT)
    if not content:
        ERRORS.append(f"R3-b — fichier introuvable : {rel(F_ARMEMENT)}")
        return
    if references_entity(content, ENT_ABSENCE_CONFIRMEE):
        print("✔ R3-b — armement_possible fondé sur la projection confirmée d'absence")
    else:
        ERRORS.append(f"R3-b — {rel(F_ARMEMENT)} ne référence pas {ENT_ABSENCE_CONFIRMEE}")


# ---------------------------------------------------------------------------
# Auto-tests internes (cas négatifs / faux positifs) — synthétiques, en mémoire.
# N'écrivent aucun fichier. Échec => sortie 2 (régression du checker lui-même).
# ---------------------------------------------------------------------------

def _selftest() -> int:
    failures: list[str] = []

    def expect(cond: bool, label: str) -> None:
        if not cond:
            failures.append(label)

    # Négatif : clim consomme le brut -> doit être détecté
    expect(references_entity("state: \"{{ is_state('%s','on') }}\"" % ENT_BRUT, ENT_BRUT),
           "neg-clim-brut")
    # Négatif : référence à la projection confirmée détectée
    expect(references_entity("  value: %s" % ENT_CONFIRMEE, ENT_CONFIRMEE),
           "neg-confirmee")
    # Négatif : panneau alarme détecté
    expect(references_prefix("  state: alarm_control_panel.alarme_maison", PREFIX_PANEL),
           "neg-panel")
    # Faux positif à éviter : commentaire mentionnant l'entité -> NON détecté
    expect(not references_entity("# voir %s pour le désarmement" % ENT_CONFIRMEE, ENT_CONFIRMEE),
           "fp-commentaire")
    # Faux positif à éviter : variable Jinja homonyme SANS préfixe binary_sensor. -> NON détecté
    expect(not references_entity("{% set presence_famille_securite = 1 %}", ENT_BRUT),
           "fp-variable-jinja")
    # Faux positif à éviter : le brut ne matche PAS la projection confirmée
    # (la frontière \b échoue avant le suffixe _confirmee_alarme).
    expect(not references_entity("  x: %s" % ENT_CONFIRMEE, ENT_BRUT + ""),
           "fp-brut-vs-confirmee-note")
    # Déclaration ignorée si skip_decl
    decl = "    unique_id: presence_famille_securite_confirmee_alarme"
    expect(not references_entity(decl, ENT_CONFIRMEE, skip_decl=True), "fp-declaration-skip")

    if failures:
        print("❌ AUTO-TESTS CHECKER PRÉSENCE EN ÉCHEC")
        for f in failures:
            print(f"  • {f}")
        return 2
    print("✅ AUTO-TESTS CHECKER PRÉSENCE OK")
    return 0


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_r1_confort_n_importe_pas_alarme,
    test_r1_clim_chauffage_sans_surete,
    test_r2_confinement_alarme,
    test_r3_desarmement_lit_confirmee,
    test_r3_desarmement_pas_de_brut,
    test_r3_absence_stable_lit_confirmee,
    test_r3_armement_lit_confirmee,
]


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_selftest())

    print("Arsenal — Validation contractuelle : Présence (séparation & confinement)\n")
    for test_fn in TESTS:
        test_fn()

    if ERRORS:
        print("\n❌ CONTRAT PRÉSENCE NON CONFORME\n")
        for err in ERRORS:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT PRÉSENCE CONFORME")
