# ARSENAL — Contrats · Température intérieure

Sous-domaine de `meteo/` : chaîne de **vérité thermique intérieure par zone**,
de la consolidation des sources brutes jusqu'à la valeur stabilisée exposée à
l'UI et à l'historique.

Le dossier héberge deux natures de contrats :

- la **production générique par zone** (consolidation → stabilisation → façade),
  qui gouverne chaque zone intérieure indépendamment ;
- une **agrégation spatiale bornée**, gouvernant un sous-ensemble nommé de zones —
  ici, les **trois chambres de l'étage** uniquement. Ces agrégats ne représentent
  **pas** toute la température intérieure.

## Documents du dossier

| Document | Rôle |
|---|---|
| [`consolidation.md`](consolidation.md) | Vérité thermique consolidée **par zone**, à partir de deux sources hétérogènes |
| [`stabilisation.md`](stabilisation.md) | Valeur thermique lissée, stable, destinée à l'UI et à l'historique |
| [`bornes_thermiques_chambres_etage.md`](bornes_thermiques_chambres_etage.md) | Bornes thermiques MIN/MAX **des trois chambres de l'étage** uniquement (agrégation spatiale bornée ; ni le RDC, ni la petite maison, ni la température intérieure globale) |

## Navigation

- [README du domaine météo](../README.md)
- [Index des contrats](../../index.md)
- [Hub — température intérieure](../../../navigation/domaines/temperature_interieure.md)
