#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

ERRORS = []

SCAN_DIRS = [
    ROOT / "18_lovelace",
    ROOT / "19_button_card_templates",
]

EXCLUDED_PARTS = [
    "/www/",
    "/00_documentation_arsenal/",
]

# ==========================================================
# Palette métier canonique
# ==========================================================

BASE_RGBA = {

    # ======================================================
    # Palette sémantique Arsenal
    # ======================================================

    "rgba(76,175,80,0.2)",
    "rgba(244,67,54,0.2)",
    "rgba(255,152,0,0.2)",
    "rgba(255,235,59,0.2)",
    "rgba(33,150,243,0.2)",
    "rgba(158,158,158,0.2)",
    "rgba(158,158,158,0.1)",
}

# ==========================================================
# Exceptions documentées Arsenal
# 00_documentation_arsenal/ui/couleurs/03_exceptions.md
# ==========================================================

EXCEPTION_RGBA = {

    # ======================================================
    # Exception 2 — Palette thermique
    # ======================================================

    "rgba(144,202,249,0.25)",

    # ======================================================
    # Exception 4 — NAV / HUB structure
    # ======================================================

    "rgba(90,110,130,0.08)",

    # ======================================================
    # Exception 6 — KPI / vigilance / transitions
    # ======================================================

    "rgba(255,193,7,0.25)",
    "rgba(255,152,0,0.25)",
    "rgba(255,152,0,0.3)",

    # ======================================================
    # Exception 7 — Palette hydrique
    # ======================================================

    "rgba(187,222,251,0.3)",
    "rgba(100,181,246,0.3)",
    "rgba(30,136,229,0.35)",

    # ======================================================
    # Exception 8 — Échelle absolue Humidex (apex axe rouge)
    # ======================================================

    "rgba(183,28,28,0.2)",
}

# ==========================================================
# RGB Arsenal autorisés pour graphes
# Exception 5 — Visualisations quantitatives
# ==========================================================

GRAPH_BASE_RGBA = {

    # ======================================================
    # Palette Arsenal canonique
    # ======================================================

    (76, 175, 80),
    (244, 67, 54),
    (255, 152, 0),
    (255, 235, 59),
    (33, 150, 243),
    (158, 158, 158),

    # ======================================================
    # Palette thermique
    # ======================================================

    (144, 202, 249),

    # ======================================================
    # KPI / vigilance
    # ======================================================

    (255, 193, 7),

    # ======================================================
    # Palette hydrique
    # ======================================================

    (187, 222, 251),
    (100, 181, 246),
    (30, 136, 229),
}

# ==========================================================
# Primitives graphiques UI autorisées
# ==========================================================

ALLOWED_GRAPHICS_RGBA = {
    "rgba(0,0,0,0)",
    "rgba(0,0,0,0.08)",
    "rgba(0,0,0,0.2)",
    "rgba(255,255,255,0.8)",
}

# ==========================================================
# RGB opaques NAV/HUB
# Exception 3
# ==========================================================

ALLOWED_RGB = {
    "rgb(244,67,54)",
    "rgb(255,193,7)",
    "rgb(76,175,80)",
    "rgb(33,150,243)",
    "rgb(158,158,158)",
}

# ==========================================================
# HEX interdits
# ==========================================================

FORBIDDEN_HEX = {
    "#000",
    "#222",
    "#333",
}

RGBA_PATTERN = re.compile(
    r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[0-9.]+\s*\)"
)

RGB_PATTERN = re.compile(
    r"rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)"
)

HEX_PATTERN = re.compile(
    r"#[0-9A-Fa-f]{3,6}\b"
)

# ==========================================================
# Détection composants graphiques
# ==========================================================

GRAPH_COMPONENT_HINTS = [
    "custom:apexcharts-card",
    "statistics-graph",
    "custom:bar-card",
    "mini-graph-card",
]

# ==========================================================
# Utilitaires
# ==========================================================

def fail(msg):
    ERRORS.append(msg)


def should_skip(path: Path):

    path_str = str(path)

    for excluded in EXCLUDED_PARTS:

        if excluded in path_str:
            return True

    return False


def normalize_color(value: str):

    value = value.strip()

    value = re.sub(r"\s+", "", value)

    value = re.sub(
        r"(\d+\.\d*?[1-9])0+\)",
        r"\1)",
        value,
    )

    value = value.replace(".0)", ")")

    return value.lower()


def is_graph_context(content: str):

    lowered = content.lower()

    for hint in GRAPH_COMPONENT_HINTS:

        if hint in lowered:
            return True

    return False


def is_allowed_graph_rgba(value: str):

    normalized = normalize_color(value)

    match = re.match(
        r"rgba\((\d+),(\d+),(\d+),([0-9.]+)\)",
        normalized,
    )

    if not match:
        return False

    rgb = (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
    )

    return rgb in GRAPH_BASE_RGBA


def iter_yaml_files():

    for base in SCAN_DIRS:

        if not base.exists():
            continue

        for path in base.rglob("*"):

            if not path.is_file():
                continue

            if path.suffix not in [".yaml", ".yml"]:
                continue

            if should_skip(path):
                continue

            yield path


# ==========================================================
# T1 — rgba autorisés uniquement
# ==========================================================

def test_only_allowed_rgba_are_used():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = RGBA_PATTERN.findall(content)

        graph_context = is_graph_context(content)

        for match in matches:

            normalized = normalize_color(match)

            # --------------------------------------------------
            # Palette métier canonique
            # --------------------------------------------------

            if normalized in BASE_RGBA:
                continue

            # --------------------------------------------------
            # Exceptions documentées
            # --------------------------------------------------

            if normalized in EXCEPTION_RGBA:
                continue

            # --------------------------------------------------
            # Primitives graphiques
            # --------------------------------------------------

            if normalized in ALLOWED_GRAPHICS_RGBA:
                continue

            # --------------------------------------------------
            # Exception 5 — Visualisations quantitatives
            # --------------------------------------------------

            if graph_context:

                if is_allowed_graph_rgba(normalized):
                    continue

            fail(
                f"{path} : couleur rgba interdite : {match}"
            )

    if not ERRORS:
        print("✔ rgba runtime conformes")


# ==========================================================
# T2 — rgb opaques whitelistés uniquement
# ==========================================================

def test_only_allowed_rgb_are_used():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = RGB_PATTERN.findall(content)

        for match in matches:

            normalized = normalize_color(match)

            if normalized not in ALLOWED_RGB:

                fail(
                    f"{path} : couleur rgb opaque interdite : {match}"
                )

    if not ERRORS:
        print("✔ rgb opaques conformes")


# ==========================================================
# T3 — noirs interdits
# ==========================================================

def test_forbidden_hex_colors():

    for path in iter_yaml_files():

        content = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        matches = HEX_PATTERN.findall(content)

        for match in matches:

            lowered = match.lower()

            if lowered in FORBIDDEN_HEX:

                fail(
                    f"{path} : noir interdit détecté : {match}"
                )

    if not ERRORS:
        print("✔ noirs interdits absents")


# ==========================================================
# T4 — C27 : restitution conforme des cartes MIN/MAX (contrat Lot 2B)
#      restitution_chambres_etage.md — backend décide, UI mappe.
# ==========================================================

def _nospace(s):
    return re.sub(r"\s+", "", s)


def _code(s):
    # Retire les lignes de commentaire YAML (#) : les vérifications de
    # consommation/interdiction portent sur le CODE, jamais sur la doc en-tête.
    return "\n".join(l for l in s.splitlines() if not l.lstrip().startswith("#"))


def test_c27_restitution_chambres_min_max():

    R = ROOT
    front = R / "12_template_sensors/chauffage/seuil_interieur_on_confort_applique.yaml"
    cmin = R / "12_template_sensors/meteo/mesures/temperature/chambres/restitution/categorie_thermique_min.yaml"
    cmax = R / "12_template_sensors/meteo/mesures/temperature/chambres/restitution/categorie_thermique_max.yaml"
    kmin = R / "19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_min_chambres.yaml"
    kmax = R / "19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_max_chambres.yaml"

    before = len(ERRORS)
    for label, p in [("frontière basse", front), ("catégorie MIN", cmin),
                     ("catégorie MAX", cmax), ("carte MIN", kmin), ("carte MAX", kmax)]:
        if not p.exists():
            fail(f"C27 : {label} absent ({p.relative_to(R)})")
    if len(ERRORS) > before:
        return  # fichiers manquants : on n'enchaîne pas les faux positifs

    # Code seul (commentaires d'en-tête retirés) : « consommer » = dans le code.
    F = _code(front.read_text(encoding="utf-8", errors="ignore"))
    CMIN = _code(cmin.read_text(encoding="utf-8", errors="ignore"))
    CMAX = _code(cmax.read_text(encoding="utf-8", errors="ignore"))
    KMIN = _code(kmin.read_text(encoding="utf-8", errors="ignore"))
    KMAX = _code(kmax.read_text(encoding="utf-8", errors="ignore"))

    # 1. Frontière basse PUBLIÉE, formule consigne − offset, availability, aucun repli
    if "unique_id: seuil_interieur_on_chauffage_applique" not in F:
        fail("C27 : frontière basse — unique_id attendu absent")
    if ("chauffage_consigne_confort')|float-states('input_number.chauffage_offset_on')|float"
            not in _nospace(F)):
        fail("C27 : frontière basse — formule `consigne_confort − offset_on` attendue")
    if not re.search(r"^\s*availability\s*:", F, re.M):
        fail("C27 : frontière basse — availability absente")
    if re.search(r"float\(\s*(?!none)\d", F):
        fail("C27 : frontière basse — repli numérique float(<n>) interdit")

    # 2-3. Catégories backend : bon agrégat + bonne frontière, états, pas de cross-entity, availability
    if "unique_id: categorie_thermique_min_chambres" not in CMIN:
        fail("C27 : catégorie MIN — unique_id absent")
    if "temperature_min_chambres" not in CMIN or "seuil_interieur_on_chauffage_applique" not in CMIN:
        fail("C27 : catégorie MIN — doit consommer l'agrégat MIN ET la référence basse")
    if "temperature_max_chambres" in CMIN or "seuil_allumage_clim_applique" in CMIN:
        fail("C27 : catégorie MIN — cross-entity interdit (ni MAX ni référence haute)")
    if "'froid'" not in CMIN or "'dans_plage'" not in CMIN:
        fail("C27 : catégorie MIN — états `froid`/`dans_plage` attendus")
    if not re.search(r"^\s*availability\s*:", CMIN, re.M):
        fail("C27 : catégorie MIN — availability absente")

    if "unique_id: categorie_thermique_max_chambres" not in CMAX:
        fail("C27 : catégorie MAX — unique_id absent")
    if "temperature_max_chambres" not in CMAX or "seuil_allumage_clim_applique" not in CMAX:
        fail("C27 : catégorie MAX — doit consommer l'agrégat MAX ET la référence haute")
    if "temperature_min_chambres" in CMAX or "seuil_interieur_on_chauffage_applique" in CMAX:
        fail("C27 : catégorie MAX — cross-entity interdit (ni MIN ni référence basse)")
    if "'chaud'" not in CMAX or "'dans_plage'" not in CMAX:
        fail("C27 : catégorie MAX — états `chaud`/`dans_plage` attendus")
    if not re.search(r"^\s*availability\s*:", CMAX, re.M):
        fail("C27 : catégorie MAX — availability absente")

    # 4-10. Cartes : consomment la catégorie, aucune logique métier, palette exacte, gris indispo prioritaire
    cartes = [
        ("MIN", KMIN, "categorie_thermique_min_chambres", "categorie_thermique_max_chambres",
         "temperature_min_chambres", "temperature_max_chambres", "chambre_la_plus_froide",
         "rgba(144,202,249,0.25)"),
        ("MAX", KMAX, "categorie_thermique_max_chambres", "categorie_thermique_min_chambres",
         "temperature_max_chambres", "temperature_min_chambres", "chambre_la_plus_chaude",
         "rgba(244,67,54,0.2)"),
    ]
    for tag, K, cat, other_cat, agg, other_agg, chambre, cat_color in cartes:
        Kn = _nospace(K)
        if cat not in K:
            fail(f"C27 : carte {tag} — ne consomme pas sa catégorie backend `{cat}`")
        for forbidden in ("input_number.chauffage", "clim_seuil_allumage_cool_atteint",
                          "seuil_allumage_clim_applique", "seuil_interieur_on_chauffage_applique"):
            if forbidden in K:
                fail(f"C27 : carte {tag} — lecture interdite `{forbidden}` (helper/franchissement/frontière)")
        if other_cat in K or other_agg in K:
            fail(f"C27 : carte {tag} — cross-entity interdit (référence à l'autre borne)")
        if agg not in K or chambre not in K:
            fail(f"C27 : carte {tag} — valeur/chambre non préservées ({agg} / {chambre})")
        if _nospace(cat_color) not in Kn:
            fail(f"C27 : carte {tag} — couleur catégorie {cat_color} attendue (Exception 2 étendue)")
        if "rgba(76,175,80,0.2)" not in Kn:
            fail(f"C27 : carte {tag} — vert `dans_plage` rgba(76,175,80,0.2) attendu")
        if "rgba(158,158,158,0.1)" not in Kn:
            fail(f"C27 : carte {tag} — gris indispo rgba(158,158,158,0.1) prioritaire attendu")
        if "rgba(158,158,158,0.2)" in Kn:
            fail(f"C27 : carte {tag} — gris neutre 0.2 interdit pour ces catégories")

    if len(ERRORS) == before:
        print("✔ C27 restitution chambres MIN/MAX conforme (Lot 2B)")


# ==========================================================
# registre des tests
# ==========================================================

TESTS = [
    "test_only_allowed_rgba_are_used",
    "test_only_allowed_rgb_are_used",
    "test_forbidden_hex_colors",
    "test_c27_restitution_chambres_min_max",
]


def test_test_registry_matches_functions():

    missing = []

    for test_name in TESTS:

        if test_name not in globals():
            missing.append(test_name)

    if missing:

        for name in missing:
            fail(
                f"fonction absente du registre TESTS : {name}"
            )

    if not ERRORS:
        print("✔ registre TESTS cohérent")


# ==========================================================
# exécution
# ==========================================================

if __name__ == "__main__":

    for test_name in TESTS:
        globals()[test_name]()

    test_test_registry_matches_functions()

    if ERRORS:

        print("\n❌ CONTRAT UI_RUNTIME_COLORS NON CONFORME")

        for error in ERRORS:
            print(f"- {error}")

        sys.exit(1)

    print("\n✅ CONTRAT UI_RUNTIME_COLORS CONFORME")