#!/usr/bin/env python3

# ==========================================================
# 🧠 ARSENAL — CONTRACT CHECK
# Domaine : VMC
# Contrat (source normative) : 00_documentation_arsenal/contrats/vmc.md
# Vérification des invariants structurels
# ==========================================================

from pathlib import Path
import sys

import yaml
from jinja2 import Environment


ERRORS = []


# ==========================================================
# CONFIGURATION
# ==========================================================

# Racine du dépôt ancrée sur l'emplacement du script (parents[2] =
# scripts/arsenal_contracts/ -> scripts/ -> racine), et NON sur le cwd :
# le checker donne le même verdict quel que soit le répertoire d'appel.
ROOT = Path(__file__).resolve().parents[2]


# ==========================================================
# HELPERS
# ==========================================================

def fail(message: str):
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ==========================================================
# TEST 1 — Capteur décisionnel unique
# ==========================================================

matches = []

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    content = read(path)

    if "binary_sensor.vmc_haute_vitesse_requise" in content:
        matches.append(path)

if not matches:
    fail(
        "Capteur décisionnel VMC introuvable : "
        "binary_sensor.vmc_haute_vitesse_requise"
    )

print("✔ Capteur décisionnel présent")


# ==========================================================
# TEST 2 — Scripts VMC sans logique métier
# ==========================================================

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    path_str = str(path.relative_to(ROOT)).lower()

    if "vmc" not in path_str:
        continue

    if "script" not in path_str:
        continue

    content = read(path)

    forbidden_terms = [
        "humidity",
        "humidite",
        "co2",
        "aeration_preferable",
        "vmc_seuil",
    ]

    for term in forbidden_terms:
        if term in content:
            fail(
                f"Logique métier interdite dans script VMC : "
                f"{path} -> '{term}'"
            )

print("✔ Scripts VMC sans logique métier")


# ==========================================================
# TEST 3 — Automatisation VMC avec mode
# ==========================================================

for path in ROOT.rglob("*.yaml"):

    if not path.is_file():
        continue

    path_str = str(path.relative_to(ROOT)).lower()

    if "vmc" not in path_str:
        continue

    if "automation" not in path_str:
        continue

    content = read(path)

    if "- id:" in content and "mode:" not in content:
        fail(
            f"Automatisation VMC sans mode : {path}"
        )

print("✔ Automatisations VMC avec mode")


# ==========================================================
# TEST 4 — Invariant de non-divergence de l'intention (§11.2)
# ==========================================================
#
# Contrat vmc.md §11.2 :
#   « Toute cause exposée doit être calculée à partir des mêmes grandeurs,
#     des mêmes frontières et des mêmes états que la décision. Une
#     approximation retenue pour la lisibilité, susceptible de diverger de
#     la décision réelle, est INTERDITE. »
#
# Le contrôle est COMPORTEMENTAL : le gabarit Jinja de `cause` est extrait du
# fichier contrôlé puis évalué. Aucune logique n'est reproduite ici — une
# copie du gabarit rendrait le test aveugle à toute dérive du fichier.

INTENTION = ROOT / "12_template_sensors" / "vmc" / "intention.yaml"
DECISION = "binary_sensor.vmc_haute_vitesse_requise"


def _gabarit_cause(path: Path) -> str:
    blocs = yaml.safe_load(path.read_text(encoding="utf-8"))
    for bloc in blocs or []:
        for entite in bloc.get("sensor", []) or []:
            if entite.get("unique_id") == "vmc_intention":
                return entite["attributes"]["cause"]
    raise ValueError("attribut `cause` de vmc_intention introuvable")


def _rendre(gabarit: str, etat: str, composition):
    env = Environment()
    return env.from_string(gabarit).render(
        states=lambda e: etat if e == DECISION else "unknown",
        state_attr=lambda e, a: composition
        if (e == DECISION and a == "composition") else None,
    ).strip()


if not INTENTION.is_file():
    fail(f"Capteur d'intention introuvable : {INTENTION}")
else:
    try:
        gabarit = _gabarit_cause(INTENTION)

        # 4a — aucune source indépendante de la décision.
        for interdit in ("sensor.humidite_relative_", "input_number.vmc_seuil",
                         "input_number.vmc_co2_seuil", "sensor.co2_sejour",
                         "aeration_preferable"):
            if interdit in gabarit:
                fail(
                    "§11.2 — la cause de l'intention lit une source "
                    f"indépendante de la décision : '{interdit}'"
                )

        # 4b — la cause dérive bien de l'attribut autoritatif.
        if "composition" not in gabarit:
            fail(
                "§11.2 — la cause de l'intention ne dérive pas de l'attribut "
                f"`composition` de {DECISION}"
            )

        # 4c — comportement, cas par cas.
        cas = [
            ("décision `on`, composition à une pièce",
             "on", "SdB parents", "SdB parents", "Séjour"),
            ("décision `on`, composition à deux pièces",
             "on", "SdB parents + SdB enfants", "SdB enfants", "Séjour"),
            ("décision `on`, composition contenant le séjour",
             "on", "CO₂ séjour", "séjour", None),
            ("décision `off`", "off", "Aucun besoin actif", None, "Séjour"),
        ]
        for libelle, etat, composition, attendu, interdit in cas:
            rendu = _rendre(gabarit, etat, composition)
            if not rendu:
                fail(f"§11.2 — cause vide ({libelle})")
                continue
            if attendu and attendu not in rendu:
                fail(
                    f"§11.2 — cause ne restitue pas la composition "
                    f"autoritative ({libelle}) : {rendu!r}"
                )
            if interdit and interdit in rendu:
                fail(
                    f"§11.2 — cause mentionne « {interdit} » alors que la "
                    f"composition autoritative ne le contient pas "
                    f"({libelle}) : {rendu!r}"
                )

        # 4d — comportement défini quand la source manque.
        for libelle, etat, composition in [
            ("composition absente", "on", None),
            ("composition vide", "on", "  "),
            ("décision indisponible", "unavailable", None),
            ("décision inconnue", "unknown", "SdB parents"),
        ]:
            rendu = _rendre(gabarit, etat, composition)
            if not rendu:
                fail(f"§11.2 — cause vide, comportement non défini ({libelle})")
            elif "Séjour" in rendu or "SdB" in rendu:
                fail(
                    f"§11.2 — cause invente une pièce en l'absence de source "
                    f"autoritative ({libelle}) : {rendu!r}"
                )

    except Exception as exc:                              # noqa: BLE001
        fail(f"§11.2 — contrôle de l'intention impossible : {exc}")

if not [e for e in ERRORS if "§11.2" in e]:
    print("✔ Intention dérivée de la décision, sans recalcul (§11.2)")


# ==========================================================
# TEST 5 — Aucun verrou d'aération dans la voie de décision (§4.3, §1.2)
# ==========================================================
#
# Contrat vmc.md §4.3 : le verdict d'aération est NON DÉCISIONNEL. Il évalue
# l'opportunité d'ouvrir des fenêtres, à l'échelle d'un VOLUME et sur une
# échelle de temps LONGUE : il relève de O3, et le §1.2 interdit qu'un critère
# servant O3 conditionne une extraction locale.
#
# L6 avait établi que le critère de clôture 8 de C35 « ne se vérifie pas seul » :
# la liste des consommateurs légitimes du checker d'aération n'interdit que les
# fichiers NON listés, de sorte qu'y laisser une entrée périmée ne fait échouer
# aucun contrôle. Ce test ferme ce trou PAR L'AUTRE BOUT : il interdit la
# consommation dans la voie de décision VMC, quelle que soit l'allowlist.

VERDICT_AERATION = "aeration_preferable_etage"

VOIE_DECISION = [
    ROOT / "12_template_sensors" / "vmc" / "haute_vitesse_requise.yaml",
    ROOT / "12_template_sensors" / "vmc" / "besoins",
    ROOT / "12_template_sensors" / "vmc" / "intention.yaml",
    ROOT / "11_automations" / "vmc",
    ROOT / "10_scripts" / "vmc",
]


def _fichiers(cible: Path):
    if cible.is_dir():
        return sorted(p for p in cible.rglob("*.yaml") if p.is_file())
    return [cible] if cible.is_file() else []


controles = 0
for cible in VOIE_DECISION:
    for path in _fichiers(cible):
        controles += 1
        if VERDICT_AERATION in read(path):
            fail(
                "§4.3 — le verdict d'aération est consommé dans la voie de "
                f"décision VMC : {path.relative_to(ROOT)}. Un critère servant "
                "O3 ne peut pas conditionner une extraction locale (§1.2)"
            )

if not [e for e in ERRORS if "§4.3" in e]:
    print(f"✔ Voie de décision VMC sans verrou d'aération "
          f"({controles} fichiers, §4.3)")


# ==========================================================
# TEST 6 — Observation glissante exposée et bornée (§2.2 bis, §10.2)
# ==========================================================
#
# Contrat vmc.md §2.2 bis : l'observation glissante est admissible comme
# condition d'ENTRÉE uniquement, bornée, et ne participe ni au maintien ni à
# la libération. §10.2 exigences 11 à 19 : elle doit être exposable.
#
# À ce stade (C35 L7.3), elle est INSTRUMENTÉE mais NON DÉCISIONNELLE : la
# libération se confond encore avec la frontière d'entrée, de sorte qu'un
# besoin ouvert par l'évolution serait libéré à l'évaluation suivante
# (`arsenal-runtime` 16326b1). Ce test garde les deux faces :
#   - l'exposition EXISTE ;
#   - la référence glissante N'ENTRE PAS dans `state`.
#
# Le second contrôle devra être RETIRÉ par L7.4, qui rend la voie
# décisionnelle. Son échec sera alors le signal attendu, non une régression.

BESOINS = ROOT / "12_template_sensors" / "vmc" / "besoins"
REFERENCE_GLISSANTE = "vmc_minimum_glissant"

EXPOSITIONS = [
    "evolution_fenetre_nominale",        # 11
    "evolution_profondeur_disponible",   # 12
    "evolution_valeur_courante",         # 13
    "evolution_valeur_reference",        # 14
    "evolution_calculee",                # 15
    "evolution_frontiere",               # 16
    "evolution_calculable",              # 17
    "evolution_satisfaite",              # 18
    "evolution_cause_non_calculable",    # 19
]

besoins = sorted(BESOINS.glob("*.yaml")) if BESOINS.is_dir() else []

if not besoins:
    fail("§2.2 bis — aucun besoin local trouvé")

for path in besoins:
    try:
        blocs = yaml.safe_load(path.read_text(encoding="utf-8"))
        entite = blocs[0]["binary_sensor"][0]
    except Exception as exc:                              # noqa: BLE001
        fail(f"§2.2 bis — besoin illisible : {path.name} ({exc})")
        continue

    attributs = entite.get("attributes") or {}
    manquants = [e for e in EXPOSITIONS if e not in attributs]
    if manquants:
        fail(
            f"§10.2 — exigences 11 à 19 non exposées par {path.name} : "
            f"{manquants}"
        )

    # La référence glissante ne doit pas gouverner l'état tant que la
    # libération n'est pas distincte de l'entrée (§2.2 bis, et constat
    # arsenal-runtime 16326b1).
    if REFERENCE_GLISSANTE in str(entite.get("state", "")):
        fail(
            f"§2.2 bis — la référence glissante entre dans l'état de "
            f"{path.name} alors que la libération se confond encore avec la "
            "frontière d'entrée : le besoin serait libéré à l'évaluation "
            "suivante. Ce contrôle doit être retiré par L7.4, pas contourné"
        )

if not [e for e in ERRORS if "§2.2 bis" in e or "§10.2" in e]:
    print(f"✔ Observation glissante exposée et non décisionnelle "
          f"({len(besoins)} besoins, §2.2 bis / §10.2)")


# ==========================================================
# RESULTAT
# ==========================================================

if ERRORS:

    print("\n❌ CONTRAT VMC NON CONFORME\n")

    for error in ERRORS:
        print(f"- {error}")

    sys.exit(1)

print("\n✅ CONTRAT VMC CONFORME")