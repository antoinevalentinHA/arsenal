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
  R4 (ERROR)   — **segments de vue non canoniques**. BLOQUANT : Arsenal est
                 mono-vue, la forme canonique d'un `navigation_path` interne est
                 STRICTEMENT `/<clé>` (cibler le dashboard, pas une vue interne).
                 Tout `/<clé>/<segment>` est rejeté — Y COMPRIS `/<clé>/0`
                 (ancienne forme de transition, désormais interdite). Forme
                 canonique proposée : toujours `/<clé>`, jamais `/<clé>/0`.
                 Seule exemption résiduelle : un segment égal à un `path:` de vue
                 réellement déclaré (aucun `path:` n'est ajouté par ce checker).
  R5 (WARNING) — **dette latente** : défauts des templates de badge
                 Paramètres/Diagnostics pointant vers une clé inexistante
                 (surchargés partout aujourd'hui — sans impact runtime).

  R6 (ERROR)   — **topologie déclarative valide** : la structure de
                 `00_documentation_arsenal/ui/navigation_topology.yaml`
                 elle-même (clés/types attendus, doublons, clés B/C/D
                 référençant des dashboards ou fichiers réellement
                 existants, non-chevauchement B/C/D).
  R7 (ERROR)   — **Classe B conforme** : pour chaque relation déclarée
                 `enfant: parent` de `hierarchie`, l'enfant porte un Retour
                 contextuel unique dont la cible effective résolue est le
                 parent déclaré, et le parent navigue réellement (hors
                 gestes secondaires Classe E) vers l'enfant.
  R8 (ERROR)   — **Classe C conforme** : chaque fichier de
                 `groupes_lateraux` existe, relie des dashboards réellement
                 déclarés (membres lus depuis le fichier, jamais recopiés),
                 et aucun de ses membres ne porte de Retour contextuel dédié.
  R9 (ERROR)   — **Classe D conforme** : chaque ressource de
                 `ressources_partagees` existe et ne porte aucun Retour
                 contextuel dédié, indépendamment de son nombre courant de
                 prédécesseurs.
  R10 (ERROR)  — **Retour B effectif non déclaré** : sens inverse de R7 —
                 tout dashboard portant en runtime un Retour contextuel
                 réellement surchargé (`tap_action.navigation_path` explicite
                 sur le template `bouton_retour_badge_carre`) doit être
                 déclaré comme enfant dans `hierarchie`. Une intention
                 Classe B ne doit jamais exister de fait sans que l'autorité
                 déclarative n'en sache rien.

L'autorité déclarative est `navigation_topology.yaml` (§6.6 de
`navigation.md`) : l'humain y déclare l'intention Classe B/C/D, ce checker
vérifie sa réalisation runtime. Aucune heuristique structurelle (nombre de
prédécesseurs, absence dans Navigation, emplacement de fichier, asymétrie
Réglages/Diagnostics, convention de nommage, forme du graphe brut) ne s'y
substitue.

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

# Autorité déclarative Classe B/C/D (§6.6 navigation.md). Machine-readable,
# sans tags Home Assistant : chargée avec un loader strict dédié
# (`_StrictTopologyLoader`, ci-dessous), pas le loader `!include` ci-dessus.
TOPOLOGY_PATH = ROOT / "00_documentation_arsenal" / "ui" / "navigation_topology.yaml"
ALLOWED_TOPOLOGY_KEYS = {"hierarchie", "groupes_lateraux", "ressources_partagees"}

# Gestes secondaires (Classe E, §6.1) : un navigation_path qui ne vit que
# sous l'une de ces clés ne crée jamais de parenté hiérarchique.
SECONDARY_ACTION_KEYS = {"hold_action", "double_tap_action"}


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


def primary_navigation_paths(node) -> list[str]:
    """Comme `all_navigation_paths`, mais ignore tout sous-arbre porté par un
    geste secondaire (`hold_action`, `double_tap_action`, Classe E, §6.1) :
    ces actions ne créent jamais de parenté hiérarchique (§6.6)."""
    out: list[str] = []
    if isinstance(node, dict):
        np = node.get("navigation_path")
        if isinstance(np, str):
            out.append(np)
        for k, v in node.items():
            if k in SECONDARY_ACTION_KEYS:
                continue
            out.extend(primary_navigation_paths(v))
    elif isinstance(node, list):
        for item in node:
            out.extend(primary_navigation_paths(item))
    return out


class _StrictTopologyLoader(yaml.SafeLoader):
    """`SafeLoader` durci : une clé de mapping dupliquée (ex. deux entrées
    `hierarchie` pour le même enfant) est une déclaration ambiguë. PyYAML,
    par défaut, la résout silencieusement en gardant la dernière valeur —
    inacceptable pour une autorité déclarative (§6.6) : l'ambiguïté doit
    échouer explicitement, jamais être écrasée sans trace."""


def _construct_mapping_no_dup(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                None, None, f"clé de mapping dupliquée : {key!r}", node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_StrictTopologyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping_no_dup
)


def load_topology(path: Path):
    """Charge `navigation_topology.yaml` : YAML brut, aucun tag Home
    Assistant à résoudre (autorité déclarative pure, §6.6 navigation.md).
    Lève `yaml.YAMLError` sur toute clé de mapping dupliquée."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return yaml.load(text, Loader=_StrictTopologyLoader)


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
        # Bilan topologie déclarative (R6-R9) : compte de relations/entrées
        # déclarées vs. effectivement conformes, pour le résumé final.
        self.b_total = 0
        self.b_ok = 0
        self.c_total = 0
        self.c_ok = 0
        self.d_total = 0
        self.d_ok = 0


def count_includes(lovelace_root: Path) -> int:
    n = 0
    for path in sorted(lovelace_root.rglob("*.yaml")):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            n += len(INCLUDE_FILE_RE.findall(line))
    return n


def check_topology(res: Result, dash_keys: set, config_root: Path, topology_path: Path) -> None:
    """Consomme l'autorité déclarative `navigation_topology.yaml` (R6) et en
    vérifie la réalisation runtime pour les Classes B (R7), C (R8) et D (R9).

    Principe (§6.6 navigation.md) : l'humain déclare l'intention ; ce
    contrôle vérifie que le runtime la réalise encore — il ne la déduit
    jamais d'une heuristique structurelle (§6.3)."""

    if not topology_path.is_file():
        res.errors.append(
            f"R6 topologie déclarative introuvable | fichier={rel(topology_path)}"
        )
        return

    try:
        raw = load_topology(topology_path)
    except yaml.YAMLError as e:
        # yaml.YAMLError couvre aussi bien une clé de mapping dupliquée
        # (`_StrictTopologyLoader`) qu'une syntaxe/indentation YAML invalide :
        # le libellé reste générique, le détail de l'exception (conservé
        # ci-dessous) précise le cas réel (ex. « clé de mapping dupliquée »).
        res.errors.append(
            f"R6 YAML invalide dans la topologie déclarative | fichier={rel(topology_path)} "
            f"| {e}"
        )
        return

    if not isinstance(raw, dict):
        res.errors.append(
            f"R6 racine de la topologie invalide | fichier={rel(topology_path)} "
            f"| attendu=mapping, obtenu={type(raw).__name__}"
        )
        return

    for cle in sorted(set(raw.keys()) - ALLOWED_TOPOLOGY_KEYS):
        res.errors.append(f"R6 clé inconnue dans la topologie déclarative | clé={cle}")

    hierarchie = raw.get("hierarchie") or {}
    groupes_lateraux = raw.get("groupes_lateraux") or []
    ressources_partagees = raw.get("ressources_partagees") or []

    if not isinstance(hierarchie, dict):
        res.errors.append("R6 `hierarchie` doit être un mapping enfant: parent")
        hierarchie = {}
    if not isinstance(groupes_lateraux, list):
        res.errors.append("R6 `groupes_lateraux` doit être une liste de fichiers")
        groupes_lateraux = []
    if not isinstance(ressources_partagees, list):
        res.errors.append("R6 `ressources_partagees` doit être une liste de clés")
        ressources_partagees = []

    for enfant, parent in hierarchie.items():
        if not isinstance(enfant, str) or not isinstance(parent, str):
            res.errors.append(
                f"R6 relation Classe B mal typée | enfant={enfant!r} | parent={parent!r}"
            )

    vus: set = set()
    for g in groupes_lateraux:
        if g in vus:
            res.errors.append(f"R6 groupe Classe C déclaré en double | fichier={g}")
        vus.add(g)

    vus = set()
    for r in ressources_partagees:
        if r in vus:
            res.errors.append(f"R6 ressource Classe D déclarée en double | clé={r}")
        vus.add(r)

    # --- Membres réels des groupes C, lus depuis chaque fichier (jamais
    # recopiés depuis la déclaration, §6.6) ---
    group_members: dict[str, set] = {}
    for g in groupes_lateraux:
        if not isinstance(g, str):
            continue
        gpath = (topology_path.parent / g).resolve()
        if not gpath.is_file():
            res.errors.append(f"R6 fichier de groupe Classe C introuvable | fichier={g}")
            continue
        data = load_yaml(gpath, config_root)
        members: set = set()
        invalides: set = set()
        for np in all_navigation_paths(data):
            if is_native(np):
                continue
            dk = path_dashkey(np)
            if not dk:
                continue
            if dk in dash_keys:
                members.add(dk)
            else:
                invalides.add(dk)
        group_members[g] = members
        for dk in sorted(invalides):
            res.errors.append(
                f"R8 membre de groupe Classe C inexistant | fichier={g} | clé absente={dk}"
            )

    all_c_members: set = set()
    for members in group_members.values():
        all_c_members |= members

    hierarchie_enfants = {k for k in hierarchie if isinstance(k, str)}
    ressources_set = {r for r in ressources_partagees if isinstance(r, str)}

    for dk in sorted(hierarchie_enfants & ressources_set):
        res.errors.append(f"R6 dashboard à la fois Classe B et Classe D | dashboard={dk}")
    for dk in sorted(hierarchie_enfants & all_c_members):
        res.errors.append(f"R6 dashboard à la fois Classe B et Classe C | dashboard={dk}")

    # ================= Classe B (R7) =================
    # Graphe de prédécesseurs dédié : exclut les gestes secondaires Classe E
    # (hold_action, double_tap_action) de la parenté hiérarchique (§6.1/§6.6).
    hier_preds: dict = {}
    for key, page in res.pages.items():
        for np in primary_navigation_paths(page["data"]):
            if is_native(np):
                continue
            tgt = path_dashkey(np)
            if tgt in dash_keys and tgt != key:
                hier_preds.setdefault(tgt, set()).add(key)

    for enfant, parent in hierarchie.items():
        if not isinstance(enfant, str) or not isinstance(parent, str):
            continue  # déjà signalé (R6, mal typé)

        res.b_total += 1

        if enfant == parent:
            res.errors.append(f"R7 boucle Classe B (enfant=parent) | dashboard={enfant}")
            continue

        enfant_absent = enfant not in dash_keys
        parent_absent = parent not in dash_keys
        if enfant_absent:
            res.errors.append(f"R6 enfant Classe B inexistant | enfant={enfant} | parent={parent}")
        if parent_absent:
            res.errors.append(f"R6 parent Classe B inexistant | enfant={enfant} | parent={parent}")
        if enfant_absent or parent_absent:
            continue

        page = res.pages.get(enfant)
        if page is None:
            res.errors.append(
                f"R6 page introuvable pour l'enfant Classe B déclaré | enfant={enfant}"
            )
            continue

        ok = True
        retours = page["retours"]
        if len(retours) == 0:
            res.errors.append(
                f"R7 Retour absent sur un enfant Classe B | enfant={enfant} "
                f"| parent déclaré={parent}"
            )
            ok = False
        elif len(retours) > 1:
            res.errors.append(
                f"R7 ambiguïté de Retour sur un enfant Classe B | enfant={enfant} "
                f"| cibles={retours}"
            )
            ok = False
        else:
            cible = path_dashkey(retours[0])
            if cible != parent:
                res.errors.append(
                    f"R7 Retour vers une mauvaise cible | enfant={enfant} "
                    f"| retour→{retours[0]} | parent déclaré={parent}"
                )
                ok = False

        if parent not in hier_preds.get(enfant, set()):
            res.errors.append(
                f"R7 parent ne navigue plus vers l'enfant déclaré | enfant={enfant} "
                f"| parent={parent}"
            )
            ok = False

        if ok:
            res.b_ok += 1

    # ================= R10 — Retour B effectif non déclaré =================
    # Sens inverse de R7 : toute relation déclarée doit être réalisée (R7),
    # mais tout Retour contextuel réellement surchargé en runtime doit aussi
    # être déclaré — sinon une intention Classe B existe de fait sans que
    # l'autorité déclarative n'en sache rien (§6.6).
    for key, page in res.pages.items():
        if key in hierarchie_enfants:
            continue
        cibles = [
            (b.get("tap_action") or {}).get("navigation_path")
            for b in page["badges"]
            if b.get("template") == RETOUR_TEMPLATE
            and isinstance((b.get("tap_action") or {}).get("navigation_path"), str)
        ]
        if cibles:
            res.errors.append(
                f"R10 Retour Classe B effectif non déclaré dans navigation_topology.yaml "
                f"| dashboard={key} | retour(s)→{cibles}"
            )

    # ================= Classe C (R8) =================
    for g in groupes_lateraux:
        if not isinstance(g, str):
            continue
        res.c_total += 1
        members = group_members.get(g)
        if members is None:
            continue  # fichier introuvable, déjà signalé (R6)

        ok = True
        if not members:
            res.errors.append(f"R8 groupe Classe C sans membre valide | fichier={g}")
            ok = False

        for m in sorted(members):
            mp = res.pages.get(m)
            if mp and mp["retours"]:
                res.errors.append(
                    f"R8 Retour contextuel dédié sur un membre Classe C | fichier={g} "
                    f"| membre={m} | retour(s)={mp['retours']}"
                )
                ok = False

        if ok:
            res.c_ok += 1

    # ================= Classe D (R9) =================
    for ressource in ressources_partagees:
        if not isinstance(ressource, str):
            continue
        res.d_total += 1

        if ressource not in dash_keys:
            res.errors.append(f"R6 ressource Classe D inexistante | dashboard={ressource}")
            continue

        page = res.pages.get(ressource)
        if page is None:
            res.errors.append(
                f"R6 page introuvable pour la ressource Classe D déclarée | dashboard={ressource}"
            )
            continue

        # Volontairement : aucune lecture de `res.preds`/`hier_preds` ici — le
        # statut D ne dépend jamais du nombre courant de prédécesseurs (§6.6).
        if page["retours"]:
            res.errors.append(
                f"R9 Retour contextuel dédié sur une ressource Classe D | dashboard={ressource} "
                f"| retour(s)={page['retours']}"
            )
        else:
            res.d_ok += 1


def analyze(lovelace_root: Path, config_root: Path, topology_path: Path | None = None) -> Result:
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

    # R4 — segments de vue non canoniques (ERROR bloquant)
    # Doctrine FINALE : Arsenal est mono-vue ; la forme canonique d'un
    # navigation_path interne est STRICTEMENT /<dashboard-key> (cibler le
    # dashboard, pas une vue interne). Tout /<dashboard-key>/<segment> est une
    # régression bloquante — Y COMPRIS le segment numérique /0 (ancienne forme
    # de transition, désormais interdite). La forme canonique proposée est
    # toujours /<dashboard-key>, JAMAIS /<dashboard-key>/0.
    # Seule exemption résiduelle : un segment égal à un path: de vue réellement
    # déclaré par le dashboard cible (aucun path: n'est ajouté par ce checker).
    noncanon = set()
    for key, page in res.pages.items():
        for np in set(page["nps"]):
            if is_native(np):
                continue
            dk = path_dashkey(np)
            seg = path_view_segment(np)
            if dk not in dash_keys or seg is None:
                continue
            target = res.pages.get(dk)
            declared = declared_view_paths(target["data"]) if target else set()
            if seg not in declared:
                noncanon.add(np)
    for np in sorted(noncanon):
        dk = path_dashkey(np)
        res.errors.append(
            f"R4 segment de vue non canonique | navigation_path={np} "
            f"| forme canonique attendue=/{dk} "
            f"(Arsenal est mono-vue ; cibler le dashboard, pas une vue interne)"
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

    check_topology(res, dash_keys, config_root, topology_path or TOPOLOGY_PATH)

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
            "          navigation_path: /hub-dashboard\n"
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

        # R4 DURCI — un /<dashboard-key>/<segment nommé> non déclaré est désormais
        # une ERREUR bloquante ; la forme canonique attendue est /<dashboard-key>.
        # page-a-dashboard existe, est mono-vue et ne déclare aucun path:.
        (ll / "dashboards" / "other.yaml").write_text(
            "views:\n"
            "  - badges:\n"
            "      - type: custom:button-card\n"
            "        template: bouton_accueil_badge_carre\n"
            "    cards:\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /page-a-dashboard/page-a\n"   # nommé -> ERROR
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /hub-dashboard\n"             # canonique -> OK
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /hub-dashboard/0\n",          # numérique -> ERROR
            encoding="utf-8",
        )
        res4 = analyze(ll, config_root=base)
        r4 = [e for e in res4.errors if "R4 segment de vue non canonique" in e]

        # /foo-dashboard/foo (segment nommé) -> bloquant, canonique /foo-dashboard
        if not any("/page-a-dashboard/page-a" in e and "attendue=/page-a-dashboard" in e
                   for e in r4):
            failures.append(
                "auto-test : R4 final — /foo-dashboard/foo doit être bloquant "
                "(forme canonique /foo-dashboard)"
            )
        # /foo-dashboard/0 (segment numérique) -> DÉSORMAIS bloquant, canonique /foo-dashboard
        if not any("/hub-dashboard/0" in e and "attendue=/hub-dashboard" in e
                   for e in r4):
            failures.append(
                "auto-test : R4 final — /foo-dashboard/0 doit DÉSORMAIS être bloquant "
                "(forme canonique /foo-dashboard)"
            )
        # /foo-dashboard (sans segment) -> accepté, jamais signalé
        if any("navigation_path=/hub-dashboard " in (e + " ") for e in r4):
            failures.append(
                "auto-test : R4 final — la forme canonique /<clé> ne doit jamais être signalée"
            )
        # La forme canonique proposée n'est JAMAIS /<clé>/0
        if any("attendue=" in e and e.split("attendue=", 1)[1].split()[0].endswith("/0")
               for e in r4):
            failures.append(
                "auto-test : R4 final — /0 ne doit jamais être proposé comme forme canonique"
            )

    return failures


def selftest_topology() -> list[str]:
    """Vérifie R6-R10 : consommation de `navigation_topology.yaml` (autorité
    déclarative, §6.6 navigation.md) et conformité runtime des relations
    Classe B, des groupes Classe C et des ressources Classe D déclarés.

    Le cas B2 (« Retour supprimé ») est le cas critique : il prouve que la
    régression type NAS (Retour contextuel disparu sans reclassification
    silencieuse, cf. PR #828) est désormais bloquante."""
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ll = base / "18_lovelace"
        nav_inc = ll / "includes" / "navigation"
        badges_inc = ll / "includes" / "badges"
        dashdir = ll / "dashboards"
        ui = base / "00_documentation_arsenal" / "ui"
        for d in (nav_inc, badges_inc, dashdir, ui):
            d.mkdir(parents=True, exist_ok=True)

        (badges_inc / "base.yaml").write_text(
            "- type: custom:button-card\n"
            "  template: bouton_accueil_badge_carre\n"
            "- type: custom:button-card\n"
            "  template: bouton_navigation_badge_carre\n",
            encoding="utf-8",
        )

        (ll / "dashboards.yaml").write_text(
            "child-b-dashboard:\n  filename: 18_lovelace/dashboards/child_b.yaml\n"
            "parent-b-dashboard:\n  filename: 18_lovelace/dashboards/parent_b.yaml\n"
            "other-dashboard:\n  filename: 18_lovelace/dashboards/other.yaml\n"
            "group-member-a-dashboard:\n  filename: 18_lovelace/dashboards/group_a.yaml\n"
            "group-member-b-dashboard:\n  filename: 18_lovelace/dashboards/group_b.yaml\n"
            "resource-d-dashboard:\n  filename: 18_lovelace/dashboards/resource_d.yaml\n",
            encoding="utf-8",
        )

        def write_child_b(retour_np):
            if retour_np is None:
                (dashdir / "child_b.yaml").write_text(
                    "views:\n"
                    "  - badges: !include ../includes/badges/base.yaml\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )
            else:
                (dashdir / "child_b.yaml").write_text(
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
                    f"          navigation_path: {retour_np}\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )

        def write_parent_b(link: str):
            # "tap" -> lien direct (tap_action) vers l'enfant ; "hold" ->
            # UNIQUEMENT via hold_action (Classe E — ne doit jamais compter
            # comme navigation hiérarchique, §6.1/§6.6) ; "none" -> aucun lien.
            if link == "tap":
                extra = (
                    "      - type: custom:button-card\n"
                    "        tap_action:\n"
                    "          action: navigate\n"
                    "          navigation_path: /child-b-dashboard\n"
                )
            elif link == "hold":
                extra = (
                    "      - type: custom:button-card\n"
                    "        hold_action:\n"
                    "          action: navigate\n"
                    "          navigation_path: /child-b-dashboard\n"
                )
            else:
                extra = ""
            (dashdir / "parent_b.yaml").write_text(
                "views:\n"
                "  - badges: !include ../includes/badges/base.yaml\n"
                "    cards:\n"
                f"{extra}"
                "      - type: custom:button-card\n"
                "        tap_action:\n"
                "          action: navigate\n"
                "          navigation_path: /other-dashboard\n",
                encoding="utf-8",
            )

        (dashdir / "other.yaml").write_text(
            "views:\n"
            "  - badges: !include ../includes/badges/base.yaml\n"
            "    cards: []\n",
            encoding="utf-8",
        )

        def write_group_member(name: str, with_retour: bool):
            if with_retour:
                (dashdir / name).write_text(
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
                    "          navigation_path: /other-dashboard\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )
            else:
                (dashdir / name).write_text(
                    "views:\n"
                    "  - badges: !include ../includes/badges/base.yaml\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )

        write_group_member("group_a.yaml", with_retour=False)
        write_group_member("group_b.yaml", with_retour=False)

        def write_group_file(with_invalid_member: bool):
            invalid = (
                "  - type: custom:button-card\n"
                "    template: bouton_navigation_badge_carre\n"
                "    tap_action:\n"
                "      action: navigate\n"
                "      navigation_path: /missing-member-dashboard\n"
            ) if with_invalid_member else (
                "  - type: custom:button-card\n"
                "    template: bouton_navigation_badge_carre\n"
                "    tap_action:\n"
                "      action: navigate\n"
                "      navigation_path: /group-member-b-dashboard\n"
            )
            (nav_inc / "group.yaml").write_text(
                "type: custom:layout-card\n"
                "cards:\n"
                "  - type: custom:button-card\n"
                "    template: bouton_navigation_badge_carre\n"
                "    tap_action:\n"
                "      action: navigate\n"
                "      navigation_path: /group-member-a-dashboard\n"
                f"{invalid}",
                encoding="utf-8",
            )

        write_group_file(with_invalid_member=False)

        def write_resource_d(with_retour: bool):
            if with_retour:
                (dashdir / "resource_d.yaml").write_text(
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
                    "          navigation_path: /other-dashboard\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )
            else:
                (dashdir / "resource_d.yaml").write_text(
                    "views:\n"
                    "  - badges: !include ../includes/badges/base.yaml\n"
                    "    cards: []\n",
                    encoding="utf-8",
                )

        write_resource_d(with_retour=False)

        topo_path = ui / "navigation_topology.yaml"

        def write_topology(hierarchie: str, groupes: str, ressources: str):
            topo_path.write_text(
                f"hierarchie:\n{hierarchie}"
                f"groupes_lateraux:\n{groupes}"
                f"ressources_partagees:\n{ressources}",
                encoding="utf-8",
            )

        def run() -> Result:
            return analyze(ll, config_root=base, topology_path=topo_path)

        def has(errs, needle: str) -> bool:
            return any(needle in e for e in errs)

        BASE_HIER = "  child-b-dashboard: parent-b-dashboard\n"
        BASE_GROUPES = "  - ../../18_lovelace/includes/navigation/group.yaml\n"
        BASE_RESSOURCES = "  - resource-d-dashboard\n"

        # ---------- B1 : cas valide ----------
        write_child_b("/parent-b-dashboard")
        write_parent_b("tap")
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)
        res = run()
        if (
            has(res.errors, "R7")
            or has(res.errors, "R6 enfant")
            or has(res.errors, "R6 parent")
            or has(res.errors, "R10")
        ):
            failures.append(f"topologie B1 (cas valide) : erreur inattendue -> {res.errors}")
        if res.b_ok != 1 or res.b_total != 1:
            failures.append("topologie B1 (cas valide) : b_ok/b_total inattendus")

        # ---------- B2 : Retour supprimé (bug type NAS, PR #828) ----------
        write_child_b(None)
        res = run()
        if not has(res.errors, "R7 Retour absent sur un enfant Classe B"):
            failures.append(
                "topologie B2 : suppression du Retour B non détectée "
                "(régression type NAS non bloquée)"
            )
        write_child_b("/parent-b-dashboard")  # restaure

        # ---------- B3 : Retour vers le mauvais parent ----------
        write_child_b("/other-dashboard")
        res = run()
        if not has(res.errors, "R7 Retour vers une mauvaise cible"):
            failures.append("topologie B3 : mauvaise cible de Retour B non détectée")
        write_child_b("/parent-b-dashboard")  # restaure

        # ---------- B4 : enfant déclaré inexistant ----------
        write_topology(
            "  missing-child-dashboard: parent-b-dashboard\n", BASE_GROUPES, BASE_RESSOURCES
        )
        res = run()
        if not has(res.errors, "R6 enfant Classe B inexistant"):
            failures.append("topologie B4 : enfant B inexistant non détecté")

        # ---------- B5 : parent déclaré inexistant ----------
        write_topology(
            "  child-b-dashboard: missing-parent-dashboard\n", BASE_GROUPES, BASE_RESSOURCES
        )
        res = run()
        if not has(res.errors, "R6 parent Classe B inexistant"):
            failures.append("topologie B5 : parent B inexistant non détecté")
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)  # restaure

        # ---------- B6 : le parent ne navigue plus vers l'enfant ----------
        write_parent_b("none")
        res = run()
        if not has(res.errors, "R7 parent ne navigue plus vers l'enfant déclaré"):
            failures.append("topologie B6 : relation B orpheline (parent muet) non détectée")

        # ---------- E : un hold_action ne crée pas de parent hiérarchique ----------
        write_parent_b("hold")
        res = run()
        if not has(res.errors, "R7 parent ne navigue plus vers l'enfant déclaré"):
            failures.append(
                "topologie E : un hold_action du parent vers l'enfant a, à tort, "
                "compté comme navigation hiérarchique"
            )
        write_parent_b("tap")  # restaure

        # ---------- B7 : boucle enfant=parent ----------
        write_topology(
            "  child-b-dashboard: child-b-dashboard\n", BASE_GROUPES, BASE_RESSOURCES
        )
        res = run()
        if not has(res.errors, "R7 boucle Classe B"):
            failures.append("topologie B7 : boucle enfant=parent non détectée")
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)  # restaure

        # ---------- C1 : groupe valide ----------
        res = run()
        if has(res.errors, "R8"):
            failures.append(f"topologie C1 (cas valide) : erreur R8 inattendue -> {res.errors}")
        if res.c_ok != 1 or res.c_total != 1:
            failures.append("topologie C1 (cas valide) : c_ok/c_total inattendus")

        # ---------- C2 : fichier de groupe inexistant ----------
        write_topology(
            BASE_HIER,
            "  - ../../18_lovelace/includes/navigation/missing_group.yaml\n",
            BASE_RESSOURCES,
        )
        res = run()
        if not has(res.errors, "R6 fichier de groupe Classe C introuvable"):
            failures.append("topologie C2 : fichier de groupe C manquant non détecté")
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)  # restaure

        # ---------- C3 : membre dashboard inexistant ----------
        write_group_file(with_invalid_member=True)
        res = run()
        if not has(res.errors, "R8 membre de groupe Classe C inexistant"):
            failures.append("topologie C3 : membre de groupe C inexistant non détecté")
        write_group_file(with_invalid_member=False)  # restaure

        # ---------- C4 : Retour contextuel ajouté sur un membre C ----------
        write_group_member("group_a.yaml", with_retour=True)
        res = run()
        if not has(res.errors, "R8 Retour contextuel dédié sur un membre Classe C"):
            failures.append("topologie C4 : Retour ajouté sur un membre C non détecté")
        write_group_member("group_a.yaml", with_retour=False)  # restaure

        # ---------- D1 : ressource valide ----------
        res = run()
        if has(res.errors, "R9"):
            failures.append(f"topologie D1 (cas valide) : erreur R9 inattendue -> {res.errors}")
        if res.d_ok != 1 or res.d_total != 1:
            failures.append("topologie D1 (cas valide) : d_ok/d_total inattendus")
        preds_avant = len(res.preds.get("resource-d-dashboard", set()))

        # ---------- D2 : ressource inexistante ----------
        write_topology(BASE_HIER, BASE_GROUPES, "  - missing-resource-dashboard\n")
        res = run()
        if not has(res.errors, "R6 ressource Classe D inexistante"):
            failures.append("topologie D2 : ressource D inexistante non détectée")
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)  # restaure

        # ---------- D3 : Retour contextuel ajouté sur une ressource D ----------
        write_resource_d(with_retour=True)
        res = run()
        if not has(res.errors, "R9 Retour contextuel dédié sur une ressource Classe D"):
            failures.append("topologie D3 : Retour ajouté sur une ressource D non détecté")
        write_resource_d(with_retour=False)  # restaure

        # ---------- D4 : le nombre de prédécesseurs ne doit jamais changer le verdict D ----------
        (dashdir / "other.yaml").write_text(
            "views:\n"
            "  - badges: !include ../includes/badges/base.yaml\n"
            "    cards:\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /resource-d-dashboard\n",
            encoding="utf-8",
        )
        res = run()
        preds_apres = len(res.preds.get("resource-d-dashboard", set()))
        if preds_apres == preds_avant:
            failures.append(
                "topologie D4 : fixture invalide — le nombre de prédécesseurs n'a pas changé"
            )
        if has(res.errors, "R9") or res.d_ok != 1:
            failures.append(
                "topologie D4 : le verdict D a changé avec le nombre de prédécesseurs "
                "(heuristique interdite, §6.3/§6.6)"
            )

        # ---------- R10 : Retour B effectif non déclaré ----------
        # parent-b-dashboard n'est jamais une clé (enfant) de `hierarchie` :
        # lui ajouter un Retour réellement surchargé doit être bloquant même
        # si aucune relation B ne le déclare.
        (dashdir / "parent_b.yaml").write_text(
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
            "          navigation_path: /other-dashboard\n"
            "    cards:\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /child-b-dashboard\n"
            "      - type: custom:button-card\n"
            "        tap_action:\n"
            "          action: navigate\n"
            "          navigation_path: /other-dashboard\n",
            encoding="utf-8",
        )
        res = run()
        if not any(
            "R10 Retour Classe B effectif non déclaré" in e and "dashboard=parent-b-dashboard" in e
            for e in res.errors
        ):
            failures.append(
                "topologie R10 : Retour B effectif non déclaré (dashboard non présent "
                "dans hierarchie) non détecté"
            )
        write_parent_b("tap")  # restaure (sans Retour)

        # ---------- R6 : clé dupliquée dans `hierarchie` (deux parents différents) ----------
        # PyYAML resout silencieusement une clé de mapping dupliquée en ne
        # gardant que la dernière valeur ; l'autorité déclarative doit
        # échouer explicitement plutôt que perdre la contradiction.
        write_topology(
            "  child-b-dashboard: parent-b-dashboard\n"
            "  child-b-dashboard: other-dashboard\n",
            BASE_GROUPES,
            BASE_RESSOURCES,
        )
        res = run()
        # Le libellé R6 reste générique (yaml.YAMLError couvre aussi une
        # syntaxe YAML invalide) : on vérifie donc à la fois le libellé
        # générique ET que le détail de l'exception nomme bien le cas réel
        # (clé de mapping dupliquée), pour ne pas affaiblir ce test.
        dup_errors = [e for e in res.errors if "R6 YAML invalide dans la topologie déclarative" in e]
        if not dup_errors:
            failures.append(
                "topologie R6 : clé `hierarchie` dupliquée (deux parents différents) "
                "non détectée — PyYAML a pu l'écraser silencieusement"
            )
        elif not any("clé de mapping dupliquée" in e for e in dup_errors):
            failures.append(
                "topologie R6 : erreur générique levée, mais le détail de l'exception "
                "ne précise plus « clé de mapping dupliquée »"
            )
        write_topology(BASE_HIER, BASE_GROUPES, BASE_RESSOURCES)  # restaure

    return failures


# ==========================================================
# Exécution
# ==========================================================

def main() -> int:
    print("Arsenal — Validation contractuelle : Navigation Lovelace (R-LL-NAV-1)")
    print("Méthode : résolution des !include et des surcharges d'instance "
          "AVANT toute conclusion.\n")

    # Garde-fou : l'auto-test valide la mécanique de résolution avant le réel.
    st_failures = selftest() + selftest_topology()
    if st_failures:
        print("❌ AUTO-TEST DE RÉSOLUTION EN ÉCHEC")
        for f in st_failures:
            print(f"  - {f}")
        return 2
    print("✔ auto-test de résolution conforme (badges inclus vus, R1/R2 validées, "
          "pas de faux positif retour)")
    print("✔ auto-test topologie déclarative conforme (R6-R10 : Classes B/C/D, "
          "y compris la régression type NAS et l'exclusion Classe E)")

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
    print(f"  Classe B (hiérarchie)      : {res.b_ok}/{res.b_total} conformes")
    print(f"  Classe C (groupes latéraux) : {res.c_ok}/{res.c_total} conformes")
    print(f"  Classe D (ressources partagées) : {res.d_ok}/{res.d_total} conformes")
    print(f"  erreurs                    : {len(res.errors)}")
    print(f"  warnings                   : {len(res.warnings)}")

    if res.errors:
        print("\n❌ CONTRAT LOVELACE_NAVIGATION NON CONFORME")
        return 1

    print("\n✅ CONTRAT LOVELACE_NAVIGATION CONFORME")
    return 0


if __name__ == "__main__":
    sys.exit(main())
