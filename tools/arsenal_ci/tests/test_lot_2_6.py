"""Lot 2.6 — meta-test d'immuabilite (region decision).

Garde la DISCIPLINE d'immuabilite, pas une cascade. Un registre des artefacts
canoniques geles porte deux proprietes meta :

  - INTEGRITE : chaque artefact enregistre a, sur disque, l'empreinte gelee
    (SHA256 des octets bruts). Toute modification d'octet => echec.
  - COUVERTURE : tout *.yaml du repertoire canonique immuable est enregistre.
    Un artefact non enregistre => echec (force un gel explicite).

Niveau de digest = octets bruts (agnostique du type, lock l'artefact entier,
en-tete compris). Complementaire du lot 2.2 (qui verrouille le scalaire de la
cascade) : defense en profondeur a deux niveaux.

Chemins STABLES : le manifeste indexe par NOM DE FICHIER relatif au repertoire
canonique, resolu a l'execution. Le registre est invariant quel que soit le
chemin de clonage.

--------------------------------------------------------------------------
RE-BENEDICTION (changement delibere d'un artefact gele) :
  Modifier un artefact gele est autorise mais explicite. Recalculer son
  SHA256 (octets bruts) et mettre a jour l'entree du manifeste — un diff
  d'une ligne, trace en PR. Aucun changement silencieux : un echec
  d'integrite est soit une regression, soit une re-benediction a acter.
--------------------------------------------------------------------------
"""
import hashlib
from pathlib import Path

# Repertoire canonique immuable : tout *.yaml ici est repute gele.
# Les fixtures jetables / non gelees vivent AILLEURS, jamais ici.
CANONIQUE = Path(__file__).resolve().parent / "fixtures" / "decision"

# Manifeste : nom de fichier relatif a CANONIQUE -> SHA256 des octets bruts.
# Chemins relatifs uniquement (invariants au chemin de clonage).
MANIFESTE = {
    "d2_reason_pre_correction.yaml":
        "81f8705f10683dbbf500abfcafba13e6d030be215872ba2c518e5b3e83a99d8e",
}


def _sha256_octets(chemin: Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


# ----------------------------------------------------------------- integrite

def test_integrite_artefacts_geles():
    for nom, empreinte_gelee in MANIFESTE.items():
        chemin = CANONIQUE / nom
        assert chemin.is_file(), f"artefact gele manquant : {nom}"
        trouvee = _sha256_octets(chemin)
        assert trouvee == empreinte_gelee, (
            f"artefact '{nom}' modifie : empreinte {trouvee} != gelee "
            f"{empreinte_gelee}. Regression, ou re-benediction a acter "
            f"(mettre a jour le manifeste)."
        )


# ----------------------------------------------------------------- couverture

def test_couverture_repertoire_canonique():
    sur_disque = {p.name for p in CANONIQUE.glob("*.yaml")}
    enregistres = set(MANIFESTE)

    non_geles = sur_disque - enregistres
    assert not non_geles, (
        f"artefact(s) canonique(s) non gele(s) : {sorted(non_geles)}. "
        f"Les enregistrer au manifeste avec leur empreinte, ou les deplacer "
        f"hors du repertoire canonique."
    )

    entrees_mortes = enregistres - sur_disque
    assert not entrees_mortes, (
        f"entree(s) de manifeste sans fichier : {sorted(entrees_mortes)}."
    )


# ----------------------------------------------------------------- mecanisme

def test_mecanisme_digest():
    # Le verrou lui-meme calcule correctement.
    attendu = hashlib.sha256(b"arsenal").hexdigest()
    assert (
        attendu
        == "15c6d611193988e468c7431229c59ce13b0407fba24f11d36c42680d7fa11e98"
    )