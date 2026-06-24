#!/usr/bin/env python3
"""
Arsenal — Vérification contractuelle
Climatisation — Ventilation (recommandation, application, silence, diagnostic, UI)

Référence :
  - 00_documentation_arsenal/contrats/climatisation/12_ventilation_intention.md
  - 00_documentation_arsenal/contrats/climatisation/13_intensite_besoin_froid.md
  - 00_documentation_arsenal/contrats/climatisation/14_recommandation_ventilation.md

Objet :
  Figer STRUCTURELLEMENT le runtime ventilation tel qu'il existe après le
  recalibrage « référentiel unique x » (grille de vitesse fondée sur le
  numérique sensor.clim_intensite_besoin_froid) et les arbitrages effectifs
  portés par l'application 10030000000120.

  MODÈLE PROTÉGÉ (hub, PAS une chaîne en série) :
    - sensor.clim_intensite_besoin_froid        = source NUMÉRIQUE amont (x) ;
    - sensor.clim_intensite_besoin_froid_niveau = projection ORDINALE
      (observabilité).
    x alimente EN PARALLÈLE (a) la projection ordinale ET (b) la grille de
    recommandation de fan_mode_recommande.yaml.

  GARDE ANTI-FAUX-INVARIANT (sens correct) :
    Le bloc `state` de fan_mode_recommande.yaml lit le NUMÉRIQUE
    clim_intensite_besoin_froid. L'ordinal clim_intensite_besoin_froid_niveau
    n'est PAS une entrée de DÉCISION ; il n'est lu qu'en attribut
    d'observabilité (niveau_besoin_lu).

Nature :
  Checker STRUCTUREL (lecture statique : regex / parsing léger). Aucune
  exécution Home Assistant, aucune simulation sémantique.

Position du script dans le repo :
  scripts/arsenal_contracts/
  ROOT = Path(__file__).resolve().parents[2]  → racine du dépôt

Usage :
    python check_climatisation_ventilation_contracts.py

Retourne :
    0 — tous les contrôles passent
    1 — au moins un contrôle échoue
"""

import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# ROOT — racine du dépôt
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# Chemins canoniques (confirmés par lecture du runtime réel)
# ---------------------------------------------------------------------------

INTENSITE_NUM = (
    ROOT / "12_template_sensors" / "climatisation" / "ventilation"
    / "intensite_besoin_froid.yaml"
)
INTENSITE_NIVEAU = (
    ROOT / "12_template_sensors" / "climatisation" / "ventilation"
    / "intensite_besoin_froid_niveau.yaml"
)
FAN_MODE_RECO = (
    ROOT / "12_template_sensors" / "climatisation" / "ventilation"
    / "fan_mode_recommande.yaml"
)
DIAGNOSTIC = (
    ROOT / "12_template_sensors" / "climatisation" / "ventilation"
    / "diagnostic.yaml"
)
APPLICATION_MODE = (
    ROOT / "11_automations" / "climatisation" / "ventilation"
    / "application_mode.yaml"
)
SILENCE = ROOT / "11_automations" / "climatisation" / "silence.yaml"
SET_FAN_MODE = ROOT / "10_scripts" / "climatisation" / "set_fan_mode.yaml"
CARTE_DIAG_XL = (
    ROOT / "19_button_card_templates" / "40_dashboards" / "climatisation"
    / "30_diagnostic" / "carte_clim_ventilation_diagnostic_xl.yaml"
)

# Scope « domaine clim » pour la garde presence_famille_securite (C12)
SCAN_FOLDERS_CLIM = [
    ROOT / "11_automations" / "climatisation",
    ROOT / "12_template_sensors" / "climatisation",
    ROOT / "10_scripts" / "climatisation",
    ROOT / "18_lovelace" / "dashboards" / "climatisation",
    ROOT / "19_button_card_templates" / "40_dashboards" / "climatisation",
]

# ---------------------------------------------------------------------------
# Accumulateur d'erreurs
# ---------------------------------------------------------------------------

ERRORS = []


def fail(msg):
    ERRORS.append(msg)


def read(path):
    return path.read_text(encoding="utf-8", errors="ignore")


# ---------------------------------------------------------------------------
# Helpers structurels (lecture statique)
# ---------------------------------------------------------------------------

def strip_comments(content):
    """Retire les commentaires Jinja {# ... #} puis les commentaires '#'
    jusqu'en fin de ligne. Sert aux invariants « hors commentaire »
    (forme exacte demandée : '# ...' et '{# ... #}')."""
    content = re.sub(r"\{#.*?#\}", "", content, flags=re.DOTALL)
    out = []
    for line in content.splitlines():
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
        out.append(line)
    return "\n".join(out)


def extract_block(content, start_re, end_re):
    """Retourne la sous-chaîne entre la 1re occurrence de start_re et la
    1re occurrence suivante de end_re (exclus). None si start_re absent.
    Si end_re absent après start_re, retourne jusqu'à la fin."""
    m = re.search(start_re, content)
    if not m:
        return None
    rest = content[m.end():]
    m2 = re.search(end_re, rest)
    return rest[: m2.start()] if m2 else rest


def has_pair(content, key, value):
    """Vrai si 'key': 'value' (tolérant aux espaces) est présent."""
    return re.search(
        r"['\"]" + re.escape(key) + r"['\"]\s*:\s*['\"]" + re.escape(value) + r"['\"]",
        content,
    ) is not None


# ---------------------------------------------------------------------------
# 0. Présence des fichiers
# ---------------------------------------------------------------------------

ALL_FILES = {
    "intensite_besoin_froid.yaml": INTENSITE_NUM,
    "intensite_besoin_froid_niveau.yaml": INTENSITE_NIVEAU,
    "fan_mode_recommande.yaml": FAN_MODE_RECO,
    "diagnostic.yaml": DIAGNOSTIC,
    "application_mode.yaml": APPLICATION_MODE,
    "silence.yaml": SILENCE,
    "set_fan_mode.yaml": SET_FAN_MODE,
    "carte_clim_ventilation_diagnostic_xl.yaml": CARTE_DIAG_XL,
}


def test_00_fichiers_presents():
    """Tous les fichiers runtime/UI ciblés existent."""
    for label, path in ALL_FILES.items():
        if not path.is_file():
            fail(f"Fichier absent : {path.relative_to(ROOT)}")
        else:
            print(f"  ✔ présent : {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# [A] Chaîne recommandation
# ---------------------------------------------------------------------------

def test_01_intensite_num_existe():
    """1. sensor.clim_intensite_besoin_froid existe (unique_id)."""
    if not INTENSITE_NUM.is_file():
        return
    if re.search(r"unique_id\s*:\s*clim_intensite_besoin_froid\b", read(INTENSITE_NUM)):
        print("  ✔ unique_id: clim_intensite_besoin_froid")
    else:
        fail(
            "unique_id 'clim_intensite_besoin_froid' absent de "
            f"{INTENSITE_NUM.relative_to(ROOT)}"
        )


def test_02_intensite_niveau_existe():
    """2. sensor.clim_intensite_besoin_froid_niveau existe (unique_id)."""
    if not INTENSITE_NIVEAU.is_file():
        return
    if re.search(
        r"unique_id\s*:\s*clim_intensite_besoin_froid_niveau\b", read(INTENSITE_NIVEAU)
    ):
        print("  ✔ unique_id: clim_intensite_besoin_froid_niveau")
    else:
        fail(
            "unique_id 'clim_intensite_besoin_froid_niveau' absent de "
            f"{INTENSITE_NIVEAU.relative_to(ROOT)}"
        )


def _reco_state_block():
    """Bloc `state:` de fan_mode_recommande.yaml (entre 'state: >' et
    'attributes:'), commentaires retirés. None si introuvable."""
    if not FAN_MODE_RECO.is_file():
        return None
    block = extract_block(read(FAN_MODE_RECO), r"\n\s*state:\s*>", r"\n\s*attributes:")
    return strip_comments(block) if block is not None else None


def test_03_reco_state_lit_numerique():
    """3. Le bloc `state` de fan_mode_recommande.yaml lit le NUMÉRIQUE
    clim_intensite_besoin_froid (négation (?!_niveau) — l'ordinal contient
    le token en sous-chaîne)."""
    block = _reco_state_block()
    if block is None:
        fail("fan_mode_recommande.yaml : bloc `state:` introuvable")
        return
    if re.search(r"clim_intensite_besoin_froid(?!_niveau)", block):
        print("  ✔ state lit le numérique clim_intensite_besoin_froid (x)")
    else:
        fail(
            "fan_mode_recommande.yaml : le bloc `state:` ne lit pas le "
            "numérique clim_intensite_besoin_froid (référentiel x attendu)."
        )


def test_04_reco_state_sans_ordinal():
    """4. L'ordinal clim_intensite_besoin_froid_niveau N'apparaît PAS dans le
    bloc `state` ; il est lu UNIQUEMENT en attribut niveau_besoin_lu."""
    block = _reco_state_block()
    if block is None:
        return
    if re.search(r"clim_intensite_besoin_froid_niveau", block):
        fail(
            "fan_mode_recommande.yaml : l'ordinal "
            "clim_intensite_besoin_froid_niveau est lu dans le bloc `state:` "
            "(interdit — moteur de décision = numérique ; l'ordinal est "
            "observabilité). Faux-invariant à NE PAS introduire."
        )
    else:
        print("  ✔ state ne lit pas l'ordinal (_niveau hors décision)")
    # L'ordinal doit rester présent en observabilité (attribut niveau_besoin_lu)
    if FAN_MODE_RECO.is_file():
        attrs = extract_block(read(FAN_MODE_RECO), r"\n\s*attributes:", r"\Z") or ""
        if re.search(r"niveau_besoin_lu\s*:", attrs) and \
           re.search(r"clim_intensite_besoin_froid_niveau", attrs):
            print("  ✔ ordinal lu en attribut niveau_besoin_lu (observabilité)")
        else:
            fail(
                "fan_mode_recommande.yaml : attribut 'niveau_besoin_lu' "
                "(lecture de l'ordinal en observabilité) absent."
            )


def test_05_reco_sans_seuil_allumage():
    """5. fan_mode_recommande.yaml ne lit plus aucun plancher fondé sur
    seuil_allumage_clim_applique : 0 occurrence hors commentaires."""
    if not FAN_MODE_RECO.is_file():
        return
    stripped = strip_comments(read(FAN_MODE_RECO))
    if "seuil_allumage_clim_applique" in stripped:
        fail(
            "fan_mode_recommande.yaml : 'seuil_allumage_clim_applique' "
            "encore présent hors commentaire (double référentiel ON/OFF "
            "abandonné — plancher ON interdit)."
        )
    else:
        print("  ✔ aucun seuil_allumage_clim_applique hors commentaire")


def test_06_reco_mapping_technique():
    """6. Mapping technique Silencieux→quiet / Faible→low / Moyen→medium /
    Fort→high ; attribut mode_technique présent."""
    if not FAN_MODE_RECO.is_file():
        return
    content = read(FAN_MODE_RECO)
    pairs = [("Silencieux", "quiet"), ("Faible", "low"),
             ("Moyen", "medium"), ("Fort", "high")]
    ok = True
    for fr, tech in pairs:
        if not has_pair(content, fr, tech):
            fail(f"fan_mode_recommande.yaml : mapping '{fr}'->'{tech}' absent.")
            ok = False
    if not re.search(r"\n\s*mode_technique\s*:", content):
        fail("fan_mode_recommande.yaml : attribut 'mode_technique' absent.")
        ok = False
    if ok:
        print("  ✔ mapping technique + attribut mode_technique")


def test_07_reco_plancher_faible_et_caps():
    """7. Plancher Faible : motif '3 if lf else (2 if lm else 1)' (jamais 0) ;
    caps silence→2 et frein→1 présents dans le bloc `state`."""
    block = _reco_state_block()
    if block is None:
        return
    ok = True
    if not re.search(r"3\s+if\s+lf\s+else\s*\(\s*2\s+if\s+lm\s+else\s+1\s*\)", block):
        fail(
            "fan_mode_recommande.yaml : plancher Faible "
            "'3 if lf else (2 if lm else 1)' absent (idx minimal = Faible)."
        )
        ok = False
    if not re.search(r"silence\s+and\s+ns\.idx\s*>\s*2", block):
        fail("fan_mode_recommande.yaml : cap silence→Moyen (idx>2 → 2) absent.")
        ok = False
    if not re.search(r"frein\s+and\s+ns\.idx\s*>\s*1", block):
        fail("fan_mode_recommande.yaml : cap frein→Faible (idx>1 → 1) absent.")
        ok = False
    if ok:
        print("  ✔ plancher Faible + caps silence→2 / frein→1")


# ---------------------------------------------------------------------------
# [B] Seuils & hystérésis — vérifier l'endroit réel
# ---------------------------------------------------------------------------

def test_08_seuils_reco_dans_fan_mode():
    """8. Le couple Moyen 1.0/0.6 et Fort 2.0/1.5 est dans
    fan_mode_recommande.yaml : 'x >= (0.6 if pm else 1.0)' et
    'x >= (1.5 if pf else 2.0)'."""
    if not FAN_MODE_RECO.is_file():
        return
    content = read(FAN_MODE_RECO)
    ok = True
    if not re.search(r"x\s*>=\s*\(\s*0\.6\s+if\s+pm\s+else\s+1\.0\s*\)", content):
        fail("fan_mode_recommande.yaml : latch Moyen 'x >= (0.6 if pm else 1.0)' absent.")
        ok = False
    if not re.search(r"x\s*>=\s*\(\s*1\.5\s+if\s+pf\s+else\s+2\.0\s*\)", content):
        fail("fan_mode_recommande.yaml : latch Fort 'x >= (1.5 if pf else 2.0)' absent.")
        ok = False
    if ok:
        print("  ✔ latches reco Moyen 1.0/0.6 et Fort 2.0/1.5 (fan_mode_recommande)")


def test_09_jeu_ordinal_distinct():
    """9. (informatif / garde anti-confusion) intensite_besoin_froid_niveau.yaml
    porte le jeu ORDINAL distinct ups [0.3,1.0,2.0,3.0] / downs [0.1,0.7,1.7,2.7]
    et NE contient PAS les seuils reco 0.6/1.5."""
    if not INTENSITE_NIVEAU.is_file():
        return
    content = read(INTENSITE_NIVEAU)
    ok = True
    if not re.search(r"\[\s*0\.3\s*,\s*1\.0\s*,\s*2\.0\s*,\s*3\.0\s*\]", content):
        fail("intensite_besoin_froid_niveau.yaml : ups [0.3, 1.0, 2.0, 3.0] absent.")
        ok = False
    if not re.search(r"\[\s*0\.1\s*,\s*0\.7\s*,\s*1\.7\s*,\s*2\.7\s*\]", content):
        fail("intensite_besoin_froid_niveau.yaml : downs [0.1, 0.7, 1.7, 2.7] absent.")
        ok = False
    if "0.6" in content or "1.5" in content:
        fail(
            "intensite_besoin_froid_niveau.yaml : seuils reco 0.6/1.5 présents "
            "(confusion ordinal ↔ grille reco — jeux à garder distincts)."
        )
        ok = False
    if ok:
        print("  ✔ jeu ordinal distinct (ups/downs) sans seuils reco 0.6/1.5")


# ---------------------------------------------------------------------------
# [C] Application — application_mode.yaml
# ---------------------------------------------------------------------------

def test_10_absence_high_auto_arsenal():
    """10. absence → high UNIQUEMENT en Auto Arsenal : branche
    'if en_auto and absence' produisant 'high'."""
    if not APPLICATION_MODE.is_file():
        return
    content = read(APPLICATION_MODE)
    if re.search(r"en_auto\s+and\s+absence\s*%\}\s*high", content):
        print("  ✔ absence → high gardé par 'en_auto and absence'")
    else:
        fail(
            "application_mode.yaml : branche 'en_auto and absence → high' "
            "introuvable (absence → Fort doit être réservée à Auto Arsenal)."
        )


def test_11_definition_absence():
    """11. absence = presence_confort_thermique_stabilisee == off ET
    presence_visiteur == off."""
    if not APPLICATION_MODE.is_file():
        return
    content = read(APPLICATION_MODE)
    ok = True
    if not re.search(
        r"is_state\(\s*'binary_sensor\.presence_confort_thermique_stabilisee'\s*,\s*'off'\s*\)",
        content,
    ):
        fail("application_mode.yaml : absence ne lit pas presence_confort_thermique_stabilisee == off.")
        ok = False
    if not re.search(
        r"is_state\(\s*'input_boolean\.presence_visiteur'\s*,\s*'off'\s*\)", content
    ):
        fail("application_mode.yaml : absence ne lit pas presence_visiteur == off.")
        ok = False
    if ok:
        print("  ✔ absence = stabilisee off ET visiteur off")


def test_12_pas_de_presence_famille_securite():
    """12. Aucune lecture brute de presence_famille_securite dans tout le
    domaine clim : 0 occurrence."""
    occurrences = []
    for folder in SCAN_FOLDERS_CLIM:
        if not folder.is_dir():
            continue
        for f in folder.rglob("*.yaml"):
            try:
                if "presence_famille_securite" in f.read_text(encoding="utf-8", errors="ignore"):
                    occurrences.append(f.relative_to(ROOT))
            except Exception:
                continue
    if occurrences:
        fail(
            "presence_famille_securite (brut sécurité) présent dans le domaine "
            "clim (contrat présence R1-b — interdit) : "
            + ", ".join(str(p) for p in occurrences[:5])
            + (" …" if len(occurrences) > 5 else "")
        )
    else:
        print("  ✔ presence_famille_securite absent du domaine clim")


def test_13_mode_manuel_mapping_fr_technique():
    """13. Mode manuel inchangé : mapping FR→technique
    {'Silencieux':'quiet','Faible':'low','Moyen':'medium','Fort':'high'}."""
    if not APPLICATION_MODE.is_file():
        return
    content = read(APPLICATION_MODE)
    pairs = [("Silencieux", "quiet"), ("Faible", "low"),
             ("Moyen", "medium"), ("Fort", "high")]
    missing = [f"{fr}->{tech}" for fr, tech in pairs if not has_pair(content, fr, tech)]
    if missing:
        fail("application_mode.yaml : mapping manuel FR→technique incomplet : " + ", ".join(missing))
    else:
        print("  ✔ mapping manuel FR→technique complet")


def test_14_quiet_borne_low():
    """14. quiet → low défensif : motif \"'low' if raw == 'quiet' else raw\"."""
    if not APPLICATION_MODE.is_file():
        return
    content = read(APPLICATION_MODE)
    if re.search(r"'low'\s+if\s+raw\s*==\s*'quiet'\s+else\s+raw", content):
        print("  ✔ quiet borné à low ('low' if raw == 'quiet' else raw)")
    else:
        fail(
            "application_mode.yaml : borne 'low' if raw == 'quiet' else raw "
            "absente (quiet ne doit jamais être appliqué via fan_mode)."
        )


def test_15_aucune_emission_auto():
    """15. Aucune émission fan_mode: auto (hors commentaires) dans
    application_mode.yaml ni set_fan_mode.yaml ; pas d'option 'auto' dans le
    selector du script."""
    ok = True
    for path in (APPLICATION_MODE, SET_FAN_MODE):
        if not path.is_file():
            continue
        stripped = strip_comments(read(path))
        if re.search(r"fan_mode\s*:\s*['\"]?auto\b", stripped):
            fail(f"{path.relative_to(ROOT)} : 'fan_mode: auto' émis hors commentaire (interdit).")
            ok = False
    # Selector du script : options quiet/low/medium/high, pas d'auto
    if SET_FAN_MODE.is_file():
        sel = extract_block(read(SET_FAN_MODE), r"\n\s*options:", r"\n\s*sequence:") or ""
        if re.search(r"-\s*auto\b", sel):
            fail("set_fan_mode.yaml : option 'auto' présente dans le selector (interdit).")
            ok = False
        for opt in ("quiet", "low", "medium", "high"):
            if not re.search(r"-\s*" + opt + r"\b", sel):
                fail(f"set_fan_mode.yaml : option '{opt}' absente du selector.")
                ok = False
    if ok:
        print("  ✔ aucune émission/option 'auto' (application + script)")


def test_16_pas_de_trigger_nu_climate_clim():
    """16. Aucun trigger nu sur climate.clim : chaque trigger d'état sur
    climate.clim possède un from: (ou to:/attribute:)."""
    if not APPLICATION_MODE.is_file():
        return
    block = extract_block(read(APPLICATION_MODE), r"\n\s*trigger:", r"\n\s*variables:")
    if block is None:
        fail("application_mode.yaml : bloc `trigger:` introuvable.")
        return
    block = strip_comments(block)
    items = re.split(r"-\s*platform\s*:", block)
    nu = 0
    total = 0
    for item in items:
        if re.search(r"entity_id\s*:\s*climate\.clim\b", item):
            total += 1
            if not re.search(r"\b(from|to|attribute)\s*:", item):
                nu += 1
    if total == 0:
        print("  ✔ aucun trigger d'état sur climate.clim (rien à borner)")
    elif nu:
        fail(
            f"application_mode.yaml : {nu} trigger(s) nu(s) sur climate.clim "
            "(sans from:/to:/attribute:) — boucle de rétroaction possible."
        )
    else:
        print(f"  ✔ {total} trigger(s) climate.clim, tous bornés (from/to/attribute)")


def test_17_garde_silence_override():
    """17. Garde silence/abstention : override_actif défini sur
    binary_sensor.clim_silencieux_autorise + condition 'not override_actif'."""
    if not APPLICATION_MODE.is_file():
        return
    content = read(APPLICATION_MODE)
    ok = True
    if not re.search(
        r"override_actif\s*:\s*['\"]?\{\{\s*is_state\(\s*'binary_sensor\.clim_silencieux_autorise'\s*,\s*'on'\s*\)",
        content,
    ):
        fail("application_mode.yaml : 'override_actif' non défini sur clim_silencieux_autorise == on.")
        ok = False
    cond = extract_block(content, r"\n\s*condition:", r"\n\s*action:") or ""
    if not re.search(r"not\s+override_actif", cond):
        fail("application_mode.yaml : condition 'not override_actif' absente du bloc condition:.")
        ok = False
    if ok:
        print("  ✔ override_actif (silencieux) + condition not override_actif")


# ---------------------------------------------------------------------------
# [D] Silence
# ---------------------------------------------------------------------------

def test_18_quiet_gouverne_par_silence():
    """18. quiet gouverné par le domaine silence : silence.yaml agit sur
    switch.clim_quiet_fan ; application_mode borne quiet→low (n'applique
    jamais quiet par fan_mode)."""
    ok = True
    if SILENCE.is_file():
        sc = read(SILENCE)
        if not (re.search(r"switch\.turn_on", sc) and re.search(r"switch\.turn_off", sc)
                and "switch.clim_quiet_fan" in sc):
            fail("silence.yaml : ne pilote pas switch.clim_quiet_fan (turn_on/turn_off).")
            ok = False
    if APPLICATION_MODE.is_file():
        if not re.search(r"'low'\s+if\s+raw\s*==\s*'quiet'\s+else\s+raw", read(APPLICATION_MODE)):
            fail("application_mode.yaml : borne quiet→low absente (quiet appliqué par fan_mode ?).")
            ok = False
    if ok:
        print("  ✔ quiet via switch.clim_quiet_fan (silence) + borne quiet→low (application)")


def test_19_silence_prime_sur_absence():
    """19. silence > absence : 'not override_actif' est une condition de TÊTE
    du bloc condition: (elle neutralise aussi la branche absence → high)."""
    if not APPLICATION_MODE.is_file():
        return
    cond = extract_block(read(APPLICATION_MODE), r"\n\s*condition:", r"\n\s*action:")
    if cond is None:
        fail("application_mode.yaml : bloc `condition:` introuvable.")
        return
    # Condition de tête : item '- condition: template' dont le value_template
    # est exactement 'not override_actif' (gate global, AND implicite).
    if re.search(
        r"-\s*condition\s*:\s*template\b.{0,160}?not\s+override_actif", cond, re.DOTALL
    ):
        print("  ✔ 'not override_actif' = condition de tête (silence prime sur absence)")
    else:
        fail(
            "application_mode.yaml : 'not override_actif' n'est pas une condition "
            "de tête du bloc condition: — la branche absence → high ne serait "
            "pas neutralisée par le silence."
        )


# ---------------------------------------------------------------------------
# [E] Diagnostic — diagnostic.yaml
# ---------------------------------------------------------------------------

def test_20_raison_arbitrage_couvre():
    """20. raison_arbitrage couvre : absence_fort, silence_quiet,
    frein_chambre_froide, quiet_reserve_silence."""
    if not DIAGNOSTIC.is_file():
        return
    block = extract_block(read(DIAGNOSTIC), r"\n\s*raison_arbitrage\s*:\s*>", r"\n\s*reel\s*:")
    block = block if block is not None else ""
    manquants = [k for k in
                 ("absence_fort", "silence_quiet", "frein_chambre_froide", "quiet_reserve_silence")
                 if k not in block]
    if manquants:
        fail("diagnostic.yaml : raison_arbitrage ne couvre pas : " + ", ".join(manquants))
    else:
        print("  ✔ raison_arbitrage couvre les 4 arbitrages")


def test_21_auto_jamais_cible_conforme():
    """21. auto jamais cible conforme : cible_effective ∈ {quiet,low,medium,high}
    (jamais 'auto') ; cas 'reel == auto' traité en écart (auto_fujitsu)."""
    if not DIAGNOSTIC.is_file():
        return
    content = read(DIAGNOSTIC)
    ok = True
    cible = extract_block(content, r"\n\s*cible_effective\s*:\s*>", r"\n\s*raison_arbitrage\s*:")
    cible = cible if cible is not None else ""
    if re.search(r"['\"]auto['\"]", cible):
        fail("diagnostic.yaml : cible_effective peut valoir 'auto' (interdit — jamais cible conforme).")
        ok = False
    if not re.search(r"reel\s*==\s*'auto'", content) or "auto_fujitsu" not in content:
        fail("diagnostic.yaml : cas 'reel == auto' → auto_fujitsu (écart) absent.")
        ok = False
    if ok:
        print("  ✔ cible_effective sans 'auto' ; reel==auto traité en écart (auto_fujitsu)")


def test_22_principe_reel_egal_cible():
    """22. Principe 'reel == cible_effective' présent dans le bloc state."""
    if not DIAGNOSTIC.is_file():
        return
    state = extract_block(read(DIAGNOSTIC), r"\n\s*state:\s*>", r"\n\s*attributes:")
    state = state if state is not None else ""
    if re.search(r"reel\s*==\s*cible_effective", state):
        print("  ✔ verdict state fondé sur 'reel == cible_effective'")
    else:
        fail("diagnostic.yaml : 'reel == cible_effective' absent du bloc state (verdict).")


# ---------------------------------------------------------------------------
# [F] UI — carte_clim_ventilation_diagnostic_xl.yaml
# ---------------------------------------------------------------------------

def test_23_ui_rend_les_4_arbitrages():
    """23. Les 4 arbitrages sont rendus lisibles dans la carte :
    absence_fort, silence_quiet, frein_chambre_froide, quiet_reserve_silence."""
    if not CARTE_DIAG_XL.is_file():
        return
    content = read(CARTE_DIAG_XL)
    manquants = [k for k in
                 ("absence_fort", "silence_quiet", "frein_chambre_froide", "quiet_reserve_silence")
                 if k not in content]
    if manquants:
        fail("carte_clim_ventilation_diagnostic_xl.yaml : arbitrages non rendus : " + ", ".join(manquants))
    else:
        print("  ✔ carte rend les 4 arbitrages (absence/silence/frein/quiet)")


# ---------------------------------------------------------------------------
# Registre des tests
# ---------------------------------------------------------------------------

TESTS = [
    test_00_fichiers_presents,
    # [A] Chaîne recommandation
    test_01_intensite_num_existe,
    test_02_intensite_niveau_existe,
    test_03_reco_state_lit_numerique,
    test_04_reco_state_sans_ordinal,
    test_05_reco_sans_seuil_allumage,
    test_06_reco_mapping_technique,
    test_07_reco_plancher_faible_et_caps,
    # [B] Seuils & hystérésis
    test_08_seuils_reco_dans_fan_mode,
    test_09_jeu_ordinal_distinct,
    # [C] Application
    test_10_absence_high_auto_arsenal,
    test_11_definition_absence,
    test_12_pas_de_presence_famille_securite,
    test_13_mode_manuel_mapping_fr_technique,
    test_14_quiet_borne_low,
    test_15_aucune_emission_auto,
    test_16_pas_de_trigger_nu_climate_clim,
    test_17_garde_silence_override,
    # [D] Silence
    test_18_quiet_gouverne_par_silence,
    test_19_silence_prime_sur_absence,
    # [E] Diagnostic
    test_20_raison_arbitrage_couvre,
    test_21_auto_jamais_cible_conforme,
    test_22_principe_reel_egal_cible,
    # [F] UI
    test_23_ui_rend_les_4_arbitrages,
]

# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Arsenal — Vérification contractuelle")
    print("Climatisation — Ventilation (structurel)")
    print(f"ROOT : {ROOT}")
    print("=" * 60)

    for test in TESTS:
        print(f"\n[{test.__name__}]")
        test()

    print("\n" + "=" * 60)
    if ERRORS:
        print("\n❌ CONTRAT CLIMATISATION_VENTILATION NON CONFORME")
        for e in ERRORS:
            print(f"  • {e}")
        sys.exit(1)
    else:
        print("\n✅ CONTRAT CLIMATISATION_VENTILATION CONFORME")
        sys.exit(0)


if __name__ == "__main__":
    main()
