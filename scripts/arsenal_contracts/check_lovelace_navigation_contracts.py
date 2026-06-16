#!/usr/bin/env python3

"""R-LL-NAV-1 — Cohérence de la navigation Lovelace (après résolution des `!include`).

Contrat  : R-LL-NAV-1
Slug     : lovelace_navigation
Origine  : 00_documentation_arsenal/audits/01_rapports/lovelace/
           audit_navigation_ui_lovelace.md  (Révision v2)

Pourquoi ce checker
-------------------
L'audit de navigation v1 avait produit des faux positifs (faux culs-de-sac,
faux « sans retour », fausse redondance Accueil/Retour) parce qu'il concluait
à partir du **texte brut** des fichiers dashboards, sans résoudre les `!include`.
Or Arsenal factorise massivement ses badges et bandeaux via includes et
**surcharge le `navigation_path` du bouton Retour par instance**.

POINT MÉTHODOLOGIQUE NON NÉGOCIABLE
-----------------------------------
Ce checker **résout les `!include` et les surcharges d'instance AVANT toute
conclusion**. Il ne cherche jamais un badge / un retour / un cul-de-sac dans le
fichier dashboard brut seul. Un contrôle purement textuel est explicitement
proscrit (il reproduirait l'erreur de l'audit v1).

Méthode de résolution
----------------------
  - Chargement YAML avec un loader dérivé de `yaml.SafeLoader` muni de
    constructeurs pour les tags Home Assistant :
      * `!include <cible>`  -> chargé récursivement (relatif au fichier source ;
                               `/config/` -> racine du dépôt). Le contenu inclus
                               (liste de badges, bandeau, carte) est inliné.
      * `!include_dir_*`    -> neutralisé ({}/[]) : non requis pour la navigation.
      * `!secret`           -> valeur sentinelle.
  - Les badges d'une vue (`badges: !include includes/badges/base.yaml`, etc.)
    deviennent donc une liste de dictionnaires exploitable.
  - La cible **effective** d'un badge = surcharge d'instance
    (`tap_action.navigation_path`) sinon défaut du template.

Règles contrôlées
-----------------
  R1 (ERROR)   — tout `navigation_path` interne cible une **clé de dashboard
                 existante** dans `18_lovelace/dashboards.yaml`.
  R2 (ERROR)   — cohérence du **bouton Retour** : sa cible effective doit être un
                 **parent réel** de la page (prédécesseur dans le graphe de
                 navigation) OU un hub structurel (Accueil / Navigation / Système).
                 Détecte le cas connu `reglages/sommeil.yaml` (Retour -> Bruit météo).
  R3 (ERROR)   — **cul-de-sac strict** : page sans badge Accueil/Navigation/Retour
                 ET sans aucune action `navigate`, APRÈS résolution. Attendu : 0.
  R4 (WARNING) — **segments de vue non canoniques** (`/clé/segment` sans vue
                 `path: segment` déclarée). Non bloquant : Arsenal est mono-vue,
                 le repli sur la 1re vue fonctionne ; politique P2 non tranchée ici.
  R5 (WARNING) — **dette latente** : défauts des templates de badge
                 Paramètres/Diagnostics pointant vers une clé inexistante
                 (surchargés partout aujourd'hui — sans impact runtime).

Les chemins **Home Assistant natifs** (`/config/*`, `/developer-tools/*`,
`/history`, `/logbook`, `/energy`, `/app/*`, …) sont classés à part et exemptés
du contrôle de clé.

Sortie / codes
--------------
  - `ERROR`   -> bloquant (exit 1).
  - `WARNING` -> non bloquant (exit 0 si aucune erreur).
  - Résumé final : dashboards, includes résolus, navigation_path analysés,
    erreurs, warnings.
  - exit 2 : erreur d'usage/infra (ex. PyYAML absent).

Implémentation : lecture seule, déterministe. Dépend de PyYAML (comme
`check_19_button_card_templates_contracts.py`).
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML requis (pip install pyyaml).\n")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[2]
LOVELACE = ROOT / "18_lovelace"

CONFIG_PREFIX = "/config/"

# Préfixes de chemins Home Assistant natifs (classés à part, pas de contrôle de clé).
NATIVE_PREFIXES = (
    "/config",
    "/developer-tools",
    "/history",
    "/logbook",
    "/energy",
    "/app",
    "/profile",
    "/media-browser",
)

# Badges dont la présence (résolue) prouve qu'une page n'est pas un cul-de-sac.
BACK_BADGES = {
    "bouton_accueil_badge_carre",
    "bouton_navigation_badge_carre",
    "bouton_retour_badge_carre",
}
RETOUR_TEMPLATE = "bouton_retour_badge_carre"

# Défauts de `navigation_path` portés par les templates de badge (cible effective
# si l'instance ne surcharge pas). Source : templates 20_transverses/navigation/badges/.
BADGE_DEFAULTS = {
    "bouton_accueil_badge_carre": "/arsenal-dashboard/arsenal",
    "bouton_navigation_badge_carre": "/navigation-dashboard/home",
    "bouton_retour_badge_carre": "/arsenal-dashboard/arsenal",
    "bouton_parametres_badge_carre": "/dashboard-reglages/0",
    "bouton_diagnostics_badge_carre": "/diagnostics-dashboard/diagnostics",
}

# Templates de badge dont on contrôle le défaut latent (R5).
LATENT_DEFAULT_BADGES = {
    "bouton_parametres_badge_carre":
        "19_button_card_templates/20_transverses/navigation/badges/"
        "bouton_parametres_badge_carre.yaml",
    "bouton_diagnostics_badge_carre":
        "19_button_card_templates/20_transverses/navigation/badges/"
        "bouton_diagnostics_badge_carre.yaml",
}

# Hubs structurels : cibles de Retour toujours acceptables.
HUB_KEYS = {"arsenal-dashboard", "navigation-dashboard", "system-dashboard"}

INCLUDE_FILE_RE = re.compile(r"!include\s+(?!_dir)(\S+)")


def rel(path: Path) -> str:
    try:
        return str(Path(path).resolve().relative_to(ROOT.resolve()))
    except Exception:
        return str(path)


# ==========================================================
# Loader YAML résolvant les tags Home Assistant
# ==========================================================

def _loader_for(curdir: Path, config_root: Path):
    class _L(yaml.SafeLoader):
        pass

    def _include(loader, node):
        raw = loader.construct_scalar(node)
        if raw.startswith(CONFIG_PREFIX):
            target = config_root / raw[len(CONFIG_PREFIX):]
        elif raw.startswith("/"):
            target = Path(raw)
        else:
            target = curdir / raw
        try:
            target = target.resolve()
        except Exception:
            return None
        if target.is_file():
            return load_yaml(target, config_root)
        # Cible absente : la couverture d'existence des !include relève du
        # contrat lovelace_includes ; ici on ne casse pas la résolution.
        return None

    def _empty_map(loader, node):
        return {}

    def _empty_list(loader, node):
        return []

    def _secret(loader, node):
        return "SECRET"

    _L.add_constructor("!include", _include)
    _L.add_constructor("!include_dir_merge_named", _empty_map)
    _L.add_constructor("!include_dir_named", _empty_map)
    _L.add_constructor("!include_dir_list", _empty_list)
    _L.add_constructor("!include_dir_merge_list", _empty_list)
    _L.add_constructor("!secret", _secret)
    return _L


def load_yaml(path: Path, config_root: Path):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    return yaml.load(text, Loader=_loader_for(Path(path).parent, config_root))


# ==========================================================
# Extraction (sur structures RÉSOLUES)
# ==========================================================

def iter_dicts(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from iter_dicts(value)
    elif isinstance(node, list):
        for item in node:
            yield from iter_dicts(item)


def all_navigation_paths(data) -> list[str]:
    out = []
    for d in iter_dicts(data):
        np = d.get("navigation_path")
        if isinstance(np, str):
            out.append(np)
    return out


def view_badges(data) -> list[dict]:
    badges = []
    for view in (data or {}).get("views") or []:
        if not isinstance(view, dict):
            continue
        b = view.get("badges")
        if isinstance(b, list):
            badges += [x for x in b if isinstance(x, dict)]
    return badges


def declared_view_paths(data) -> set[str]:
    out = set()
    for view in (data or {}).get("views") or []:
        if isinstance(view, dict) and isinstance(view.get("path"), str):
            out.add(view["path"])
    return out


def badge_effective_target(badge: dict):
    ta = badge.get("tap_action") or {}
    np = ta.get("navigation_path")
    if isinstance(np, str):
        return np
    return BADGE_DEFAULTS.get(badge.get("template"))


def is_native(np: str) -> bool:
    return np.startswith(NATIVE_PREFIXES)


def path_dashkey(np: str) -> str:
    seg = np.strip("/").split("/")
    return seg[0] if seg and seg[0] else ""


def path_view_segment(np: str):
    seg = np.strip("/").split("/")
    return seg[1] if len(seg) > 1 else None


# ==========================================================
# Cœur d'analyse (réutilisable réel / auto-test)
# ==========================================================

class Result:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.pages: dict = {}
        self.preds: dict = {}
        self.n_navpaths = 0
        self.n_native = 0
        self.n_includes = 0


def count_includes(lovelace_root: Path) -> int:
    n = 0
    for path in sorted(lovelace_root.rglob("*.yaml")):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            n += len(INCLUDE_FILE_RE.findall(line))
    return n


def analyze(lovelace_root: Path, config_root: Path) -> Result:
    res = Result()

    decl_path = lovelace_root / "dashboards.yaml"
    decl = load_yaml(decl_path, config_root) or {}
    dash_keys = set(decl.keys())

    key2file = {}
    for key, val in decl.items():
        if isinstance(val, dict) and "filename" in val:
            key2file[key] = (config_root / val["filename"]).resolve()

    # 1) Résolution par page (badges, navigation_path, retour, présence d'issue)
    for key, fpath in key2file.items():
        if not fpath.is_file():
            continue
        data = load_yaml(fpath, config_root)
        badges = view_badges(data)
        nps = all_navigation_paths(data)
        res.n_navpaths += len(nps)
        retours = [
            badge_effective_target(b)
            for b in badges
            if b.get("template") == RETOUR_TEMPLATE
        ]
        res.pages[key] = {
            "file": fpath,
            "data": data,
            "badges": badges,
            "nps": nps,
            "has_back": any(b.get("template") in BACK_BADGES for b in badges),
            "retours": [r for r in retours if isinstance(r, str)],
        }

    # 2) Graphe de prédécesseurs (qui navigue VERS qui), via navigation_path effectifs
    preds = {k: set() for k in dash_keys}
    for key, page in res.pages.items():
        for np in page["nps"]:
            if is_native(np):
                continue
            tgt = path_dashkey(np)
            if tgt in dash_keys and tgt != key:
                preds[tgt].add(key)
    res.preds = preds

    # R1 — clés de dashboard inexistantes réellement référencées (ERROR)
    for key, page in res.pages.items():
        for np in sorted(set(page["nps"])):
            if is_native(np):
                res.n_native += 1
                continue
            dk = path_dashkey(np)
            if dk and dk not in dash_keys:
                res.errors.append(
                    f"R1 clé de dashboard inexistante | source={rel(page['file'])} "
                    f"| navigation_path={np} | clé absente={dk}"
                )

    # R2 — cohérence du bouton Retour (ERROR)
    for key, page in res.pages.items():
        for rt in page["retours"]:
            if is_native(rt):
                continue
            rk = path_dashkey(rt)
            if rk not in dash_keys:
                continue  # déjà signalé par R1
            acceptable = preds.get(key, set()) | HUB_KEYS
            if rk not in acceptable:
                attendus = sorted(preds.get(key, set())) or ["∅"]
                res.errors.append(
                    f"R2 retour incohérent | page={key} ({rel(page['file'])}) "
                    f"| retour→{rt} | parent(s) attendu(s)={attendus} "
                    f"ou hub {sorted(HUB_KEYS)}"
                )

    # R3 — cul-de-sac strict (ERROR), APRÈS résolution
    for key, page in res.pages.items():
        if not page["has_back"] and not page["nps"]:
            res.errors.append(
                f"R3 cul-de-sac (aucun retour ni navigation après résolution) "
                f"| page={key} ({rel(page['file'])})"
            )

    # R4 — segments de vue non canoniques (WARNING, agrégé)
    noncanon = set()
    for key, page in res.pages.items():
        for np in set(page["nps"]):
            if is_native(np):
                continue
            dk = path_dashkey(np)
            seg = path_view_segment(np)
            if dk not in dash_keys or seg is None or seg == "0" or seg.isdigit():
                continue
            target = res.pages.get(dk)
            declared = declared_view_paths(target["data"]) if target else set()
            if seg not in declared:
                noncanon.add(f"{np}")
    if noncanon:
        sample = "; ".join(sorted(noncanon)[:6])
        res.warnings.append(
            f"R4 segments de vue non canoniques : {len(noncanon)} occurrence(s) "
            f"(mono-vue ; repli sur la 1re vue ; politique P2 non tranchée). "
            f"Exemples : {sample}"
        )

    # R5 — défauts latents des templates de badge Paramètres/Diagnostics (WARNING)
    for tpl, relpath in LATENT_DEFAULT_BADGES.items():
        default = BADGE_DEFAULTS.get(tpl)
        if not default or is_native(default):
            continue
        dk = path_dashkey(default)
        if dk and dk not in dash_keys:
            res.warnings.append(
                f"R5 défaut latent | template={tpl} | défaut={default} "
                f"| clé absente={dk} (surchargé par instance partout aujourd'hui — "
                f"sans impact runtime)"
            )

    res.n_includes = count_includes(lovelace_root)
    return res


# ==========================================================
# Auto-test de la résolution (fixtures jetables — n'écrit pas dans le dépôt)
# ==========================================================

def selftest() -> list[str]:
    """Vérifie que la résolution voit bien les badges fournis par include
    (pas de faux cul-de-sac), détecte une clé absente et un retour incohérent."""
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ll = base / "18_lovelace"
        (ll / "dashboards").mkdir(parents=True)
        (ll / "includes" / "badges").mkdir(parents=True)

        # Include de badges : Accueil + Navigation + Retour (surchargé par instance plus bas)
        (ll / "includes" / "badges" / "base_like.yaml").write_text(
            "- type: custom:button-card\n"
            "  template: bouton_accueil_badge_carre\n"
            "- type: custom:button-card\n"
            "  template: bouton_navigation_badge_carre\n",
            encoding="utf-8",
        )

        # dashboards.yaml : 3 clés
        (ll / "dashboards.yaml").write_text(
            "page-a-dashboard:\n  filename: 18_lovelace/dashboards/page_a.yaml\n"
            "hub-dashboard:\n  filename: 18_lovelace/dashboards/hub.yaml\n"
            "other-dashboard:\n  filename: 18_lovelace/dashboards/other.yaml\n",
            encoding="utf-8",
        )

        # hub.yaml : navigue VERS page-a (=> hub est prédécesseur de page-a)
        (ll / "dashboards" / "hub.yaml").write_text(
            "views:\n"
            "  - badges:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_accueil_badge_carre\n"
            "    cards:\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /page-a-dashboard/0\n",
            encoding="utf-8",
        )

        (ll / "dashboards" / "other.yaml").write_text(
            "views:\n"
            "  - badges:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_accueil_badge_carre\n"
            "    cards: []\n",
            encoding="utf-8",
        )

        # page_a.yaml : badges via include ; un lien vers une clé ABSENTE ;
        # un Retour surchargé vers other-dashboard (qui n'est PAS prédécesseur => incohérent)
        (ll / "dashboards" / "page_a.yaml").write_text(
            "views:\n"
            "  - badges: !include ../includes/badges/base_like.yaml\n"
            "    cards:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_retour_badge_carre\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /other-dashboard/x\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /missing-dashboard/x\n",
            encoding="utf-8",
        )
        # NB : le Retour est ici dans `cards` pour le fixture ; en production il est
        # en `badges`. On teste donc aussi un Retour porté en badge :
        # on ajoute un badge retour incohérent directement.
        # (page_a a déjà accueil+navigation via include => pas de cul-de-sac)

        res = analyze(ll, config_root=base)

        page_a = res.pages.get("page-a-dashboard", {})
        if not page_a.get("has_back"):
            failures.append(
                "auto-test : badges inclus NON résolus (faux cul-de-sac) — "
                "la résolution des !include de badges est cassée"
            )

        if not any("missing-dashboard" in e for e in res.errors):
            failures.append("auto-test : clé absente non détectée (R1)")

        # Le Retour de page_a (badge) doit être incohérent : ajoutons-le en badge
        # via une seconde passe ciblée pour valider R2 sur un badge retour réel.
        (ll / "dashboards" / "page_a.yaml").write_text(
            "views:\n"
            "  - badges:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_accueil_badge_carre\n"
            "      - type: custom:button-card\n"
            "        template: bouton_navigation_badge_carre\n"
            "      - type: custom:button-card\n"
            "        template: bouton_retour_badge_carre\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /other-dashboard/x\n"
            "    cards: []\n",
            encoding="utf-8",
        )
        res2 = analyze(ll, config_root=base)
        if not any("R2 retour incohérent" in e and "page-a-dashboard" in e
                   for e in res2.errors):
            failures.append("auto-test : retour incohérent non détecté (R2)")

        # Cohérence inverse : un Retour vers le prédécesseur (hub) ne doit PAS être flaggé.
        (ll / "dashboards" / "page_a.yaml").write_text(
            "views:\n"
            "  - badges:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_retour_badge_carre\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /hub-dashboard/0\n"
            "    cards: []\n",
            encoding="utf-8",
        )
        res3 = analyze(ll, config_root=base)
        if any("R2 retour incohérent" in e and "page-a-dashboard" in e
               for e in res3.errors):
            failures.append(
                "auto-test : faux positif R2 — un Retour vers le prédécesseur réel "
                "ne doit pas être signalé"
            )

    return failures


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    print("Arsenal — Validation contractuelle : Navigation Lovelace (R-LL-NAV-1)")
    print("Méthode : résolution des !include et des surcharges d'instance "
          "AVANT toute conclusion.\n")

    # Garde-fou : l'auto-test valide la mécanique de résolution avant le réel.
    st_failures = selftest()
    if st_failures:
        print("❌ AUTO-TEST DE RÉSOLUTION EN ÉCHEC")
        for f in st_failures:
            print(f"  - {f}")
        return 2
    print("✔ auto-test de résolution conforme (badges inclus vus, R1/R2 validées, "
          "pas de faux positif retour)")

    res = analyze(LOVELACE, config_root=ROOT)

    if res.errors:
        print(f"\n❌ ERREURS ({len(res.errors)}) :")
        for e in res.errors:
            print(f"  - {e}")
    else:
        print("\n✔ Aucune erreur (R1 clés / R2 retours / R3 culs-de-sac).")

    if res.warnings:
        print(f"\n⚠️  WARNINGS ({len(res.warnings)}) — non bloquants :")
        for w in res.warnings:
            print(f"  - {w}")
    else:
        print("\n✔ Aucun warning.")

    print("\n— Résumé —")
    print(f"  dashboards analysés        : {len(res.pages)}")
    print(f"  !include (fichiers) résolus : {res.n_includes}")
    print(f"  navigation_path analysés   : {res.n_navpaths} "
          f"(dont {res.n_native} natifs HA classés à part)")
    print(f"  erreurs                    : {len(res.errors)}")
    print(f"  warnings                   : {len(res.warnings)}")

    if res.errors:
        print("\n❌ CONTRAT LOVELACE_NAVIGATION NON CONFORME")
        return 1

    print("\n✅ CONTRAT LOVELACE_NAVIGATION CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
