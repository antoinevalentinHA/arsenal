# ARSENAL — Contrats · Température intérieure

Sous-domaine de `meteo/` : chaîne de **vérité thermique intérieure par zone**,
de la consolidation des sources brutes jusqu'à la valeur stabilisée exposée à
l'UI et à l'historique.

Le dossier héberge trois natures de contrats :

- la **production générique par zone** (consolidation → stabilisation → façade),
  qui gouverne chaque zone intérieure indépendamment ;
- une **agrégation spatiale bornée**, gouvernant un sous-ensemble nommé de zones —
  ici, les **trois chambres de l'étage** uniquement. Ces agrégats ne représentent
  **pas** toute la température intérieure ;
- la **restitution thermique** de ces bornes MIN/MAX (catégories et couleur des
  deux cartes), qui **consomme** l'agrégation bornée sans la redéfinir et ne
  gouverne **pas** toute la température intérieure ni toute la maison.

## Documents du dossier

| Document | Rôle |
|---|---|
| [`consolidation.md`](consolidation.md) | Vérité thermique consolidée **par zone**, à partir de deux sources hétérogènes |
| [`stabilisation.md`](stabilisation.md) | Valeur thermique lissée, stable, destinée à l'UI et à l'historique |
| [`bornes_thermiques_chambres_etage.md`](bornes_thermiques_chambres_etage.md) | Bornes thermiques MIN/MAX **des trois chambres de l'étage** uniquement (agrégation spatiale bornée ; ni le RDC, ni la petite maison, ni la température intérieure globale) |
| [`restitution_chambres_etage.md`](restitution_chambres_etage.md) | **Restitution thermique** des bornes MIN/MAX des trois chambres de l'étage : catégories `froid`/`dans_plage`/`chaud` (plage appliquée P2) et mapping vers l'Exception 2 étendue ; consomme la production, sans gouverner toute la température intérieure |

## Navigation

- [README du domaine météo](../README.md)
- [Index des contrats](../../index.md)
- [Hub — température intérieure](../../../navigation/domaines/temperature_interieure.md)
