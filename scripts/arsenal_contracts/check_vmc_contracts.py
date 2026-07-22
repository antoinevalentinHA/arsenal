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
# C35 L7.4 — la voie est DEVENUE DÉCISIONNELLE. Le contrôle « la référence
# glissante n'entre pas dans `state` », posé par L7.3 et explicitement daté,
# est RETIRÉ : il a rempli son office, qui était d'empêcher une
# décisionnalisation prématurée tant que la libération se confondait avec la
# frontière d'entrée.
#
# Ce qui subsiste :
#   - l'exposition des exigences 11 à 19 EXISTE ;
#   - l'évolution demeure une condition d'ENTRÉE : elle ne doit apparaître ni
#     dans la libération, ni dans le maintien (§2.2 bis).

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

# Les exigences 11 à 19 sont propres à l'observation glissante, donc à la
# VOIE HUMIDITÉ. Le §5.2 pose que « les voies peuvent avoir des critères
# internes différents » : la voie CO₂ n'a pas de critère d'évolution, et le
# §10.2 conditionne ces exigences au cas « lorsqu'un critère d'évolution est
# retenu ». Les y soumettre serait exiger l'exposition d'un critère inexistant.
besoins_humidite = [p for p in besoins if p.name.startswith("humidite_")]

if not besoins:
    fail("§2.2 bis — aucun besoin local trouvé")
if not besoins_humidite:
    fail("§2.2 bis — aucun besoin de la voie humidité trouvé")

for path in besoins_humidite:
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

    # §2.2 bis — l'observation glissante est une condition d'ENTRÉE
    # uniquement : elle ne participe ni au maintien ni à la libération.
    attributs = entite.get("attributes") or {}
    for cle in ("condition_liberation", "condition_maintien"):
        if REFERENCE_GLISSANTE in str(attributs.get(cle, "")):
            fail(
                f"§2.2 bis — la référence glissante intervient dans "
                f"`{cle}` de {path.name} : elle est une condition d'ENTRÉE "
                "uniquement et ne participe ni au maintien ni à la libération"
            )

if not [e for e in ERRORS if "§2.2 bis" in e or "§10.2" in e]:
    print(f"✔ Observation glissante exposée, condition d'entrée seule "
          f"({len(besoins_humidite)} besoins humidité, §2.2 bis / §10.2)")


# ==========================================================
# TEST 7 — Machine hystérétique et frontière modulée (§7.4 bis, §10.4)
# ==========================================================
#
# Contrat vmc.md §7.4 bis : la frontière modulée doit être bornée à double
# sens, exposable, et son indisponibilité doit MAINTENIR le besoin actif.
# §10.4 : toute frontière exposée doit être celle que le système consomme.
#
# Engagement L7.0 §2 bis : `A`, `B` et `H` sont des constantes versionnées,
# DÉFINIES UNE SEULE FOIS et exposées PAR L'ENTITÉ QUI CALCULE.

FRONTIERES = ROOT / "12_template_sensors" / "vmc" / "frontieres"
MACHINES = sorted((ROOT / "11_automations" / "vmc").glob("machine_besoin_*.yaml"))

EXPOSITIONS_FRONTIERE = [
    "grandeur_modulante",     # 20
    "valeur_modulante",       # 21
    "borne_basse",            # 23
    "borne_haute",            # 23
    "calculable",             # 24
    "cause_non_calculable",   # 24
    "constante_a",
    "constante_b",
    "bande_morte_h",
    "plancher_evolution",
]

frontieres = sorted(FRONTIERES.glob("*.yaml")) if FRONTIERES.is_dir() else []

if not frontieres:
    fail("§7.4 bis — aucune frontière de libération trouvée")
if not MACHINES:
    fail("§6 — aucune machine hystérétique trouvée")

for path in frontieres:
    try:
        entite = yaml.safe_load(path.read_text(encoding="utf-8"))[0]["sensor"][0]
    except Exception as exc:                              # noqa: BLE001
        fail(f"§7.4 bis — frontière illisible : {path.name} ({exc})")
        continue
    attributs = entite.get("attributes") or {}
    manquants = [e for e in EXPOSITIONS_FRONTIERE if e not in attributs]
    if manquants:
        fail(
            f"§10.2 exigences 20 à 24 — non exposées par {path.name} : "
            f"{manquants}"
        )
    # La frontière ne doit lire AUCUNE mesure de pièce (§6.4 : seule la
    # mesure comparée est celle de la pièce ; la frontière est un point de
    # comparaison).
    if "humidite_relative_sdb" in read(path):
        fail(
            f"§6.4 — la frontière {path.name} lit une mesure de pièce : elle "
            "est un point de comparaison, pas une grandeur comparée"
        )

# Les constantes ne doivent être définies QUE dans les frontières.
CONSTANTES = ("constante_a", "constante_b", "bande_morte_h")
for cible in (ROOT / "12_template_sensors" / "vmc",
              ROOT / "11_automations" / "vmc"):
    for path in _fichiers(cible):
        if path.parent.name == "frontieres":
            continue
        contenu = read(path)
        for c in CONSTANTES:
            if f"{c}:" in contenu:
                fail(
                    f"Engagement L7.0 — la constante `{c}` est redéfinie hors "
                    f"de l'entité calculatrice : {path.relative_to(ROOT)}. "
                    "Une seule définition autoritative est admise"
                )

# §9.1 — l'état restauré doit être confronté aux mesures dès le démarrage.
# Sans déclencheur `homeassistant.start`, un état restauré incohérent avec la
# mesure subsisterait jusqu'à la publication suivante du capteur, alors que les
# cas 1 et 2 du §9.1 « priment inconditionnellement ».
for path in MACHINES:
    try:
        auto_m = yaml.safe_load(path.read_text(encoding="utf-8"))[0]
    except Exception as exc:                              # noqa: BLE001
        fail(f"§9.1 — machine illisible : {path.name} ({exc})")
        continue
    declencheurs = auto_m.get("trigger") or auto_m.get("triggers") or []
    if not any(t.get("platform") == "homeassistant"
               or t.get("trigger") == "homeassistant" for t in declencheurs):
        fail(
            f"§9.1 — {path.name} ne réévalue pas l'état restauré au "
            "démarrage : un état incohérent avec la mesure subsisterait "
            "jusqu'à la publication suivante, alors que les cas 1 et 2 "
            "priment inconditionnellement"
        )

# La machine ne doit jamais libérer sur une frontière non calculable.
for path in MACHINES:
    contenu = read(path)
    if "liberation:" not in contenu:
        fail(f"§6.4 — {path.name} n'expose aucune condition de libération")
        continue
    bloc = contenu.split("liberation:", 1)[1].split("\n\n", 1)[0]
    if "is not none" not in bloc:
        fail(
            f"§7.4 bis condition 4 — la libération de {path.name} ne vérifie "
            "pas que la frontière est calculable : `unknown` vaudrait "
            "libération"
        )
    if "float(" in bloc and "float(none)" not in bloc and "| float(none)" not in contenu:
        fail(
            f"§7.4 bis — repli numérique silencieux dans la libération de "
            f"{path.name}"
        )

# ==========================================================
# TEST 8 — Indisponibilité et reconstruction (§4.4, §9.1 cas 4, §10.2)
# ==========================================================
#
# §4.4 : un besoin actif est MAINTENU sur mesure inexploitable. §12.3 range
# parmi les non-conformités « la libération d'un besoin actif sur mesure
# inexploitable » et « un besoin maintenu faute de mesure présenté comme un
# besoin observé ».
#
# §9.1 cas 4 : lorsqu'aucun état valide n'a pu être restauré, le besoin est
# initialisé inactif, et la situation doit être EXPOSABLE (§10.2 exigence 10).

EXPOSITIONS_INDISPONIBILITE = [
    "maintenu_faute_de_mesure",      # §10.2 exigence 8, §4.4 cas 2
    "maintenu_faute_de_frontiere",   # §10.2 exigence 8, §7.4 bis
    "mesure_exploitable",
]

# §10.2 exigence 10 — situation de reconstruction (§9.1 cas 4) : NON SERVIE.
# Vérifié sur les 38 bases (`arsenal-runtime` 704a056) : un `input_boolean`
# sans état restaurable apparaît à `off`, jamais à `unknown`/`unavailable` —
# 0 occurrence sur 21 964 lignes d'état. Le cas 4 n'est donc pas détectable
# avec ce porteur, et aucun indicateur n'est exigé ici : un indicateur qui ne
# se déclencherait jamais serait une affirmation non fondée.
#
# Ce test GARDE l'absence : aucun indicateur de reconstruction ne doit être
# réintroduit sans une preuve de détectabilité.
INDICATEUR_NON_FONDE = "vmc_reconstruction_"

for path in besoins:
    try:
        entite = yaml.safe_load(path.read_text(encoding="utf-8"))[0]["binary_sensor"][0]
    except Exception:                                     # noqa: BLE001
        continue
    attributs = entite.get("attributes") or {}
    manquants = [e for e in EXPOSITIONS_INDISPONIBILITE if e not in attributs]
    if manquants:
        fail(
            f"§4.4 / §9.1 — situations d'indisponibilité non exposées par "
            f"{path.name} : {manquants}"
        )

# Aucun indicateur de reconstruction ne doit être écrit : il ne pourrait pas
# se déclencher, et afficherait donc en permanence une absence non établie.
for path in MACHINES:
    contenu = read(path)
    for ligne in contenu.splitlines():
        nu = ligne.strip()
        if nu.startswith("#"):
            continue
        if INDICATEUR_NON_FONDE in nu:
            fail(
                f"§10.2 exigence 10 — {path.name} écrit un indicateur de "
                "reconstruction alors que le cas 4 n'est pas détectable avec "
                "un porteur `input_boolean` (arsenal-runtime 704a056). Un "
                "indicateur qui ne se déclenche jamais est une affirmation "
                "non fondée, pas une exposition"
            )
            break
    if "mesure_exploitable" not in contenu:
        fail(
            f"§4.4 — {path.name} ne rend pas explicite l'exploitabilité de la "
            "mesure : le maintien serait subi plutôt que construit"
        )

# Aucun dispositif de sortie temporel ne doit libérer un besoin maintenu :
# le §8.3 interdit qu'une durée tienne lieu de condition métier.
for path in MACHINES:
    contenu = read(path)
    if "for:" in contenu or "delay:" in contenu:
        fail(
            f"§8.3 — {path.name} emploie une durée dans la machine de besoin : "
            "une durée ne peut pas tenir lieu de condition métier"
        )

if not [e for e in ERRORS if "§4.4" in e or "§9.1 cas 4" in e or "§8.3" in e]:
    print(f"✔ Indisponibilité exposée, sans dispositif temporel ni "
          f"indicateur non fondé ({len(besoins)} besoins, §4.4 / §8.3)")


# ==========================================================
# TEST 9 — La commande ne reconstruit aucune décision (§2.1, §8.2, §8.4)
# ==========================================================
#
# Contrat vmc.md : l'application de la décision est une couche d'EXÉCUTION.
# §8.4 pose que le reflet n'alimente pas la décision, et le §12.3 range parmi
# les non-conformités « une décision lisant l'état physique de l'actionneur ».
#
# La contrepartie doit être vraie dans l'autre sens : la couche d'exécution ne
# doit RIEN RECONSTRUIRE de la décision. Elle lit le verdict agrégé, et rien
# de ce qui a servi à le former.

COMMANDE = ROOT / "11_automations" / "vmc" / "gestion_auto.yaml"

# Grandeurs et paramètres qui ont servi à FORMER la décision. Les relire dans
# la couche de commande serait la reconstruire.
INGREDIENTS_DECISION = (
    "sensor.humidite_relative_",
    "sensor.co2_sejour",
    "sensor.vmc_minimum_glissant_",
    "sensor.vmc_frontiere_liberation_",
    "input_number.vmc_seuil_on",
    "input_number.vmc_evolution_",
    "input_number.vmc_fenetre_",
    "input_number.vmc_borne_",
    "input_number.vmc_co2_seuil",
    "input_boolean.vmc_etat_besoin_",
    "binary_sensor.vmc_besoin_",
    "aeration_preferable",
)

if not COMMANDE.is_file():
    fail(f"§8.2 — automatisation de commande introuvable : {COMMANDE}")
else:
    contenu_cmd = read(COMMANDE)
    for ingredient in INGREDIENTS_DECISION:
        if ingredient in contenu_cmd:
            fail(
                f"§8.2 — la couche de commande reconstruit la décision : "
                f"{COMMANDE.name} lit '{ingredient}', qui a servi à la former. "
                "Elle ne doit lire que le verdict agrégé"
            )
    if DECISION not in contenu_cmd:
        fail(
            f"§8.2 — {COMMANDE.name} ne lit pas le verdict agrégé "
            f"{DECISION} : la commande ne serait rattachée à aucune décision"
        )
    # §8.4 — le reflet ne doit pas remonter dans la commande.
    if "input_boolean.vmc_haute_vitesse" in contenu_cmd:
        fail(
            f"§8.4 — {COMMANDE.name} lit le reflet d'exécution : le sens est "
            "unique, le reflet n'alimente ni la décision ni la commande"
        )

if not [e for e in ERRORS if "§8.2" in e or "§8.4" in e]:
    print("✔ Commande rattachée au seul verdict agrégé, sans reconstruction "
          "(§8.2, §8.4)")


if not [e for e in ERRORS if "§7.4 bis" in e or "Engagement L7.0" in e
        or "§6.4" in e or "§6 —" in e or "§9.1 —" in e]:
    print(f"✔ Frontière modulée exposée, constantes uniques, libération "
          f"gardée, état réévalué au démarrage "
          f"({len(frontieres)} frontières, {len(MACHINES)} machines)")


# ==========================================================
# RESULTAT
# ==========================================================

if ERRORS:

    print("\n❌ CONTRAT VMC NON CONFORME\n")

    for error in ERRORS:
        print(f"- {error}")

    sys.exit(1)

print("\n✅ CONTRAT VMC CONFORME")