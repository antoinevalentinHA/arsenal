#!/usr/bin/env python3
"""
Arsenal — Validation structurelle : résolution des includes de configuration.yaml

Contrat (source normative) : configuration.yaml (déclaration des includes Arsenal)
Cadrage : 00_documentation_arsenal/audits/04_chantiers/transverses/
          c14_lot1c_validation_chargement_ha.md

Niveau 1 (C14 Lot 1C) : vérifie que CHAQUE include déclaré dans
configuration.yaml pointe vers une cible EXISTANTE.
  - !include <fichier>            -> un FICHIER existant
  - !include_dir_* <répertoire>   -> un RÉPERTOIRE existant
Résolution : chemins relatifs à la racine du dépôt (= /config).

Périmètre STRICT (volontairement limité) :
  - existence des cibles UNIQUEMENT ;
  - ne valide PAS les schémas Home Assistant ;
  - ne charge PAS les secrets (`!secret` neutralisé) ;
  - n'exige PAS HACS / custom components ;
  - ne lance PAS Home Assistant (`hass --script check_config`) ;
  - se limite aux includes DIRECTS de configuration.yaml — les includes
    imbriqués de la couche Lovelace relèvent de check_lovelace_includes.

Garantit : configuration.yaml ne référence pas d'include mort.
NE garantit PAS : schémas HA, secrets réels, HACS, intégrations, runtime.

Logique Arsenal habituelle : ERROR => exit 1.

Usage :
  python scripts/arsenal_contracts/check_configuration_includes.py
  python scripts/arsenal_contracts/check_configuration_includes.py --selftest
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configuration.yaml"

FILE_TAGS = {"!include"}
DIR_TAGS = {
    "!include_dir_list",
    "!include_dir_named",
    "!include_dir_merge_list",
    "!include_dir_merge_named",
}


class IncludeRef:
    """Référence d'include capturée dans le YAML (tag + chemin cible)."""

    __slots__ = ("tag", "target")

    def __init__(self, tag: str, target: str):
        self.tag = tag
        self.target = target


def _make_loader():
    """Loader tolérant : capture les tags d'include, neutralise les autres tags HA."""

    class _Loader(yaml.SafeLoader):
        pass

    def _ref(tag):
        def ctor(loader, node):
            return IncludeRef(tag, str(loader.construct_scalar(node)))

        return ctor

    for tag in FILE_TAGS | DIR_TAGS:
        _Loader.add_constructor(tag, _ref(tag))

    # Tout autre tag HA (!secret, !input, ...) -> None : sans incidence ici.
    _Loader.add_multi_constructor("!", lambda loader, suffix, node: None)
    return _Loader


def collect_includes(obj, acc):
    """Parcourt récursivement la structure et collecte les IncludeRef."""
    if isinstance(obj, IncludeRef):
        acc.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            collect_includes(value, acc)
    elif isinstance(obj, list):
        for value in obj:
            collect_includes(value, acc)


def check(config_path: Path, base: Path):
    """Retourne (liste des includes, liste des erreurs) pour un configuration.yaml donné."""
    errors: list[str] = []
    data = yaml.load(
        config_path.read_text(encoding="utf-8", errors="ignore"),
        Loader=_make_loader(),
    )
    refs: list[IncludeRef] = []
    collect_includes(data, refs)
    for ref in refs:
        target = (base / ref.target).resolve()
        if ref.tag in FILE_TAGS:
            if not target.is_file():
                errors.append(
                    f"{config_path.name} : {ref.tag} {ref.target} -> FICHIER introuvable"
                )
        elif not target.is_dir():
            errors.append(
                f"{config_path.name} : {ref.tag} {ref.target} -> REPERTOIRE introuvable"
            )
    return refs, errors


def main() -> None:
    if not CONFIG.is_file():
        print(f"ERROR : {CONFIG} introuvable")
        sys.exit(1)
    refs, errors = check(CONFIG, ROOT)
    if errors:
        print("Includes non resolus dans configuration.yaml :")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    print(f"OK - {len(refs)} include(s) de configuration.yaml resolu(s).")


def selftest() -> None:
    """Auto-test du juge (on ne juge pas avec un juge défectueux)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "dir_ok").mkdir()
        (base / "file_ok.yaml").write_text("- a\n", encoding="utf-8")
        conf = base / "configuration.yaml"

        # 1. cas conforme (+ tag !secret toléré)
        conf.write_text(
            "a: !include file_ok.yaml\n"
            "b: !include_dir_merge_named dir_ok/\n"
            "c: !secret un_secret\n",
            encoding="utf-8",
        )
        refs, errs = check(conf, base)
        assert not errs, f"selftest conforme : {errs}"
        assert len(refs) == 2, f"selftest nb includes : {len(refs)}"

        # 2. include FICHIER manquant -> erreur
        conf.write_text("a: !include manquant.yaml\n", encoding="utf-8")
        _, errs = check(conf, base)
        assert errs and "FICHIER introuvable" in errs[0], "selftest fichier manquant"

        # 3. include DOSSIER manquant -> erreur
        conf.write_text("b: !include_dir_merge_list manquant_dir/\n", encoding="utf-8")
        _, errs = check(conf, base)
        assert errs and "REPERTOIRE introuvable" in errs[0], "selftest dossier manquant"

    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
