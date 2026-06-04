# Cartographie des futurs artefacts de navigation — Arsenal

> **Cadre.** Lecture seule. **Aucun fichier, README, index ou lien n'est créé** ici : ce document **cartographie** les artefacts de navigation à produire plus tard, pour décider de l'ordre. Fondé sur les rapports déjà produits (audit structurel, audit hypertexte, cartographie des chaînes, arbitrage des ambiguïtés) et sur l'état réel du dépôt.
>
> **État de départ (rappel chiffré).** 9 points d'entrée pour ~90 dossiers. Les « index » existants sont des **catalogues en texte brut** (0 lien) ; les README de zone `contrats/`/`architecture/` sont des **documents de méthode**, pas des sommaires. Atteignabilité par liens ≈ 1,4 %. Le **seul** patron déjà maillé est le cluster `lovelace/CI` — modèle à généraliser.

---

## Principes de cadrage

1. **Distinguer trois objets** souvent confondus : *index* (sommaire intra-zone), *hub de domaine* (pivot **inter-familles** d'un domaine), *page pivot transverse* (navigation multi-domaines).
2. **Prérequis dur** : la **carte des domaines** (issue de l'arbitrage) conditionne tous les hubs — sans taxonomie figée, un hub ne sait pas quoi agréger.
3. **Footprint minimal** : privilégier les emplacements existants ; signaler explicitement chaque décision de placement à risque structurel.

---

## A. README de zone (points d'entrée de 1er rang)

| Chemin proposé | Rôle | Agrège | Prio | Justification | Risque |
|---|---|---|:--:|---|---|
| `outils_externes/README.md` | Entrée de zone | `boiler_pi/`, `nas_arsenal/`, `nas_imprimerie/` + statut des `prompt_*` | **Moy.** | Zone **sans aucun point d'entrée** ; 2 intrus (`prompt_*`) à cadrer | Faible |
| `schemas_ascii/README.md` | Entrée de zone | les 3 diagrammes + renvoi vers les domaines illustrés | Basse | Zone isolée sans entrée | Minimal |
| `evolutions_futures/README.md` | Statut de zone | l'unique fiche + doctrine « sas » (cf. arbitrage) | Basse | Zone quasi vide : clarifier *sas vivant vs vestige* | Devient inutile si la zone se vide |

*(Les zones `architecture/`, `contrats/`, `ui/` ont déjà un README ; `audits/`, `changelog/` un `index.md`. Pas de doublon à créer — voir §B pour leur fiabilisation.)*

---

## B. Index (sommaires **navigables** intra-zone)

| Chemin proposé | Rôle | Agrège | Prio | Justification | Risque |
|---|---|---|:--:|---|---|
| `contrats/index.md` *(distinct du README de méthode)* | Sommaire fonctionnel des 244 contrats | tous les domaines folderisés + 28 contrats racine | **Haute** | **Plus grande zone, la plus isolée**, sans sommaire navigable | Exige d'avoir figé la taxonomie (racine vs dossier) ; dérive si non maintenu |
| `audits/index.md` *(fiabilisation de l'existant)* | Index du cycle d'audit | les ~62 fichiers réels (vs 31 listés) + statuts | **Haute** | Index actuel **incomplet (~50 %)** et 0 lien ; tout `alarme` absent | Dérive index↔fichiers déjà constatée |
| `changelog/changelogs/index.md` | Index **par version** des 90 `vXX` | les snapshots `v00`→`v15` | Moy. | Aucune entrée par version ; seul le monolithe (109 Ko) existe | Doublonner le monolithe — séparer *récit* vs *index* |
| `contrats/ecs/index.md` | Sommaire ECS | colonne `00`→`11` + fiches d'implémentation + renvoi bouclage | Moy. | 28 fichiers hétérogènes, pas de sommaire | Lisibilité des fiches nommées par ID |

*(Modèles déjà en place à imiter : `contrats/climatisation/00_index.md`, `contrats/chauffage/15_capteurs/13_capteurs_index.md`.)*

---

## C. Hubs de domaine (pivots **inter-familles**)

> Cœur du futur système : une page par domaine agrégeant **contrat ↔ architecture ↔ chaîne d'audit ↔ changelog**. **Aucun n'existe** aujourd'hui (sauf le proto `lovelace/CI`). Décision de placement à trancher (voir risque).

| Chemin proposé | Rôle | Agrège | Prio | Justification | Risque |
|---|---|---|:--:|---|---|
| hub **chauffage** | Pivot domaine | `contrats/chauffage/`, `architecture/chauffage/`, chaîne audit auto-ajustement, changelogs CH-x (Chauffage-CI) | **Haute** | Domaine le plus riche, **chaîne complète** existante | Volume ; CH-x mal classés (cf. §E) |
| hub **alarme** | Pivot domaine | `contrats/alarme/`, chaîne CH1/CH2/CH6 complète, clôtures | **Haute** | **Chaînes complètes mais invisibles dans l'index** → ROI fort | Trous CH3/CH5, CH4 orpheline à signaler |
| hub **vacances** | Pivot domaine | `contrats/vacances.md`, chaîne VAC-IMP-5 → clôtures, cross-réfs chauffage 65/66 | **Haute** | Chaîne quasi complète, domaine actif | Cross-domaine vacances↔chauffage |
| hub **ecs** (+ bouclage) | Pivot domaine | `contrats/ecs/`, sous-système **bouclage** (`../bouclage.md`), boucle watchdog | Moy. | Boucle arbitrage aboutie ; bouclage à rattacher **sous** ECS | Contrat bouclage canonique encore à acter |
| hub **climatisation** | Pivot domaine | `contrats/climatisation/`, chantier COOL livré, changelog | Moy. | Chaîne livrée | Pas de maillon clôture explicite |
| hub **météo** / **temp. intérieure** | 2 pivots distincts | météo extérieure vs `temperature_interieure` (domaine propre) | Moy. | Taxonomie tranchée par l'arbitrage | Recouvrement à expliciter |

**Risque de placement (commun).** Un hub est **inter-familles** : le loger dans une seule famille (`contrats/<domaine>/`) est impur mais à footprint minimal ; une zone transverse dédiée est plus propre mais réorganise. **Décision à prendre avant production** — c'est le principal point ouvert de ce chantier.

---

## D. Tables des matières (sommaires intra-dossier)

| Chemin proposé | Rôle | Agrège | Prio | Justification | Risque |
|---|---|---|:--:|---|---|
| `contrats/chauffage/` (TOC en tête) | Sommaire du domaine le plus gros | colonne `00`→`92` + amendements + `15_capteurs/` | Moy. | 50 fichiers, pas de sommaire de tête (seulement `00_gouvernance`) | Confusion avec le hub (§C) : TOC = intra-dossier, hub = inter-familles |
| `contrats/aeration_blocage_chauffage/` (TOC) | Sommaire machine d'état | `m0`→`m6` + `socle_transversal/` | Basse | A déjà un README ; à enrichir en sommaire | Faible |
| `contrats/climatisation/capteurs/` (TOC) | Sommaire des 7 familles capteurs | `admissibilite`…`seuils_et_franchissements` | Basse | Arbre profond + noms répétés | Faible |

---

## E. Pages pivot transverses

| Chemin proposé | Rôle | Agrège | Prio | Justification | Risque |
|---|---|---|:--:|---|---|
| `README.md` (racine doc) *(correction)* | Hub d'entrée | les 8 zones + renvois | **Haute** | L'audit structurel le dit **faux** (décrit une arborescence inexistante) : l'entrée ment | Faible (correction de contenu) |
| **carte des domaines / taxonomie** | Référentiel canonique des domaines | domaines, sous-domaines (bouclage⊂ECS), domaines propres (temp/humidité int.), ui+lovelace, méta (perception_externe) | **Haute** | **Prérequis de tous les hubs** (§C) | Dépend de 2 décisions auteur ouvertes (contrat bouclage, audit humidité) |
| **matrice cycle d'audit (domaine × étape)** | Carte d'état des chaînes | tous les `audits/**` par domaine et étape | Moy.-haute | Vue navigable rapport→clôture ; chaînes complètes/incomplètes | Dérive avec les fichiers d'audit |
| **registre CH-x** | Désambiguïsation d'identifiant | CH-x **Chauffage-CI** (mal classés sous `climatisation/`) vs CH-x **Alarme** | Moy. | « CH-x » surchargé (cf. arbitrage) ; pointe sans déplacer | Expose le mauvais classement (à signaler, pas à corriger ici) |
| **cluster méta** | Entrée « regard sur le dépôt » | audits `documentation/` + `perception_externe/` | Basse | Rapports méta de même nature, à regrouper | Faible |

---

## Synthèse — quoi produire en premier

Ordre recommandé (fondé sur dépendances + ROI navigation), **à décider, non exécuté** :

1. **`README.md` racine (correction)** + **carte des domaines** — fondations : une entrée juste et une taxonomie canonique. Tout le reste en dépend.
2. **`contrats/index.md`** — débloque la plus grande zone isolée.
3. **Hubs des 3 chaînes complètes** (`alarme`, `chauffage`, `vacances`) — généralisent le patron `lovelace/CI` là où la matière existe déjà ; ROI maximal. *(Trancher d'abord le placement des hubs, §C.)*
4. **Fiabilisation `audits/index.md`** (complétude + liens).
5. Le reste (index par version, TOC, matrice transverse, registre CH-x, README de zones, cluster méta) au fil de l'eau.

**Deux décisions bloquantes à prendre avant tout** : (i) **où logent les hubs de domaine** (dans la famille vs zone transverse) ; (ii) la **carte des domaines** suppose d'acter les 2 questions de fond restantes (contrat bouclage canonique, ouverture d'un audit humidité intérieure).

---

*Fin de la cartographie. Aucun fichier modifié ni créé. Uniquement une carte des artefacts candidats, pour décider de l'ordre de production.*
