# Conception de la couche de navigation Arsenal (option S5)

> **Cadre.** Lecture seule. **Aucun fichier, hub, README, index ou patch produit.** Document de **conception** de la future couche de navigation, après décision : une **9ᵉ zone non normative** dédiée à la navigation, les 8 familles conservant leurs README/index avec un rôle **strictement intra-famille**. Fondé sur la taxonomie déjà arbitrée et les conventions réelles du dépôt.

---

## 1. Principes directeurs

1. **Deux couches, deux rôles.** Couche **contenu** = les 8 zones (contrats, architecture, audits, changelog, ui, outils_externes, schemas_ascii, evolutions_futures), normatives, inchangées. Couche **navigation** = la nouvelle zone, **non normative**, qui *agrège et oriente* sans jamais définir.
2. **Agréger sans dupliquer.** Un hub **pointe** vers le contenu ; il ne **recopie ni ne reformule** aucune règle, invariant ou entité. Cela neutralise par construction la dérive observée (Bouclage, Bluetti) : le hub référence un **document**, jamais une **entité** ou une **version** volatile.
3. **Précédence du contenu.** En cas de conflit hub ↔ document de famille, **le document de famille fait foi**. Le hub n'a aucune autorité.
4. **Symétrie des domaines.** Tout domaine canonique a sa place dans la navigation, **qu'il existe en dossier, en fichier-racine, ou seulement en audit** (c'est la raison d'être de S5 : lever l'asymétrie domaine≠famille).
5. **Le maillage descend.** Les liens vont de **navigation → contenu** ; le contenu reste majoritairement intra-famille, avec des **rétroliens optionnels** vers les hubs.

---

## 2. Arborescence cible

Zone unique, sous `00_documentation_arsenal/`, séparée des 8 familles :

```
00_documentation_arsenal/
├── README.md                      ← entrée globale (corrigée) : pointe vers navigation/ + familles
│
├── navigation/                    ← 9ᵉ ZONE — NON NORMATIVE
│   ├── README.md                  ← charte de la couche navigation (rôle, doctrine non-normative, règles)
│   ├── carte_domaines.md          ← PIVOT racine : référentiel canonique des domaines (taxonomie arbitrée)
│   │
│   ├── domaines/                  ← HUBS DE DOMAINE (1 par domaine de Tier 1)
│   │   ├── chauffage.md
│   │   ├── ecs.md                 (inclut la sous-section bouclage)
│   │   ├── alarme.md
│   │   ├── climatisation.md
│   │   ├── vacances.md
│   │   ├── meteo.md
│   │   ├── temperature_interieure.md
│   │   ├── humidite_relative_interieure.md
│   │   ├── ui_lovelace.md
│   │   └── … (un fichier par domaine Tier 1)
│   │
│   └── pivots/                    ← PAGES PIVOT TRANSVERSES (multi-domaines)
│       ├── matrice_cycle_audit.md     (domaine × étape rapport→clôture)
│       ├── registre_ch.md             (désambiguïsation « CH-x » par domaine)
│       └── cluster_meta.md            (audits documentation/ + perception_externe/)
│
├── contrats/        (inchangé — README méthode + index intra-famille)
├── architecture/    (inchangé)
├── audits/          (inchangé — index intra-famille à fiabiliser)
├── changelog/       (inchangé)
├── ui/  outils_externes/  schemas_ascii/  evolutions_futures/   (inchangés)
```

Notes de structure :
- **`carte_domaines.md` à la racine de `navigation/`** (et non dans `pivots/`) car c'est le **registre d'autorité** de la couche : tout hub en découle.
- **`domaines/` et `pivots/` séparés** : objets de natures distinctes (hub = un domaine ; pivot = traverse plusieurs domaines).
- Le nom `navigation/` reste un nom de zone plat, cohérent avec les autres ; un marqueur visuel (préfixe `_`) est une option mineure à trancher.

---

## 3. Conventions de nommage

| Objet | Convention | Exemple |
|---|---|---|
| Zone | `navigation/` (snake_case, plat) | `navigation/` |
| Charte de zone | `README.md` à la racine de la zone | `navigation/README.md` |
| Registre taxonomique | `carte_domaines.md` | `navigation/carte_domaines.md` |
| Hub de domaine | `domaines/<domaine_canonique>.md` | `domaines/temperature_interieure.md` |
| Sous-domaine | **section interne** au hub parent (pas de fichier) ; promotion en `domaines/<parent>/<sous>.md` **seulement si volume le justifie** (règle « grandit → dossier », déjà pratiquée côté contrats) | bouclage = section de `ecs.md` |
| Page pivot | `pivots/<role>.md` (rôle descriptif) | `pivots/matrice_cycle_audit.md` |
| Nom de domaine | **identique** au nom canonique de `carte_domaines.md` (1 domaine ⟺ 1 nom) | `ui_lovelace` (fusion actée) |

Règle de nommage transverse : **le nom du hub = le nom canonique du domaine** dans la carte. Aucun alias de fichier (interdit `clim.md` si le canonique est `climatisation`).

---

## 4. Granularité des hubs

Trois niveaux, pour **éviter la prolifération** de hubs vides :

- **Tier 1 — hub dédié** : domaine **inter-familles** (présent dans ≥ 2 familles) **ou** doté d'une **chaîne d'audit** **ou** **référencé** par d'autres domaines.
  Exemples : `chauffage`, `ecs`, `alarme`, `climatisation`, `vacances`, `meteo`, `temperature_interieure`, `humidite_relative_interieure`, `aeration_blocage_chauffage`, `pannes`, `boiler`, `eclairage`, `ouvertures`, `ui_lovelace`, `energie_chaudiere` (Bluetti), `voiture`…
- **Tier 2 — entrée légère (pas de hub dédié)** : domaine **feuille mono-fichier**, sans empreinte inter-familles ni audit. Il figure **dans `carte_domaines.md`** avec un lien direct vers son unique contrat.
  Exemples : `babysitting`, `visite`, `simulation_presence`, `notifications`, `batteries`, `bssid`, `volets_pluie`, `ups_arret_ha`, `cumulus_petite_maison`…
- **Hors hubs — pivots** : objets **non-domaines**. Les rapports **méta** (`audits/01_rapports/documentation/`, `perception_externe`) ne sont **pas** des hubs de domaine → ils vivent dans `pivots/cluster_meta.md`.

**Sous-domaines** (taxonomie arbitrée) : intégrés au hub parent (bouclage → section de `ecs.md`), sauf promotion sur volume. **Domaines propres logés ailleurs** (`temperature_interieure`/`humidite_relative_interieure`, physiquement sous `contrats/meteo/`) : hubs **distincts** de `meteo`, qui pointent vers leurs docs réels où qu'ils soient.

---

## 5. Relations entre hubs, README, index et pivots

### 5.1 Rôles (sans recouvrement)
| Objet | Couche | Portée | Contenu autorisé |
|---|---|---|---|
| `README` de famille | contenu | **intra-famille** | méthode/doctrine de la famille |
| `index` de famille | contenu | **intra-famille** | sommaire navigable des fichiers de la famille |
| **hub de domaine** | navigation | **inter-familles, 1 domaine** | orientation courte + liens sortants + statut de chaîne |
| **pivot** | navigation | **multi-domaines** | vue transverse (matrice, registre, méta) |
| `carte_domaines` | navigation | **tous domaines** | référentiel canonique + renvoi vers chaque hub/feuille |

### 5.2 Sens des liens (graphe cible)
```
README.md racine
   ├─→ navigation/README.md ─→ carte_domaines.md ─→ domaines/<x>.md   (hubs)
   │                                              └─→ pivots/*.md
   └─→ familles (README + index intra-famille)

domaines/<x>.md  ──(liens sortants)──→  contrat(s), architecture, chaîne d'audit, changelog du domaine x
index de famille ──(rétrolien optionnel)──→ hub du domaine concerné
pivots/*.md      ──→ hubs et/ou docs de famille
```
Invariants de liens :
- Un **hub** ne reçoit de liens **entrants** que de `carte_domaines`, des `pivots`, et (optionnel) des index de famille. Il **émet** vers le contenu.
- Le **contenu** n'est jamais obligé de connaître la navigation (rétroliens **optionnels**) → la couche navigation est **détachable** sans casser le contenu.

---

## 6. Gabarit de hub (spécification, non un fichier)

Squelette **fixe et minimal** (réduit la surface de dérive) :

1. **Bandeau non-normatif** — mention explicite « NAVIGATION — NON NORMATIF — agrège, ne définit pas ».
2. **Orientation** — 2–3 phrases : ce qu'est le domaine, sa relation taxonomique (parent/sous-domaine).
3. **Liens par famille** — Contrat(s) canonique(s) · Architecture · Chaîne d'audit (rapport→clôture) · Changelog de chantier (si existant).
4. **Statut de chaîne** — pointeur vers l'état faisant foi (ex. `audits/index.md`), **sans le recopier**.
5. **Sous-domaines** — sections renvoyant aux docs (ex. bouclage → `../../contrats/bouclage.md` canonique).
6. **Questions ouvertes** — renvoi vers les arbitrages en suspens, le cas échéant.

Interdits dans un hub : règles métier, invariants, noms d'entités, numéros de version, seuils — **tout ce qui peut dériver** vit dans le contenu, pas dans le hub.

---

## 7. Règles de gouvernance anti-dérive

- **G1 — Non-normativité.** Un hub/pivot ne contient **aucune** doctrine. La présence d'une règle/invariant/entité dans un hub est une **violation**.
- **G2 — Agréger sans dupliquer.** Le hub **lie**, ne **copie** pas. Toute information susceptible de changer (entité, version, seuil) est **référencée**, jamais **restituée**.
- **G3 — Source unique de vérité.** Le hub pointe vers le document **canonique** par famille (ex. bouclage → `contrats/bouclage.md`, **pas** le renvoi `ecs/04`). Les ambiguïtés déjà arbitrées sont **figées** dans `carte_domaines`.
- **G4 — Autorité de la carte.** `carte_domaines.md` est l'**unique** liste canonique des domaines : **1 hub ⟺ 1 entrée de carte**. Pas de hub sans entrée ; pas d'entrée sans résolution (hub Tier 1 ou feuille Tier 2).
- **G5 — Localisation des faits transverses.** Un fait transverse vit dans **un seul** pivot et est **référencé** ailleurs (ex. « CH-x est relatif au domaine » → uniquement dans `registre_ch.md`).
- **G6 — Précédence du contenu.** En cas de divergence hub ↔ famille, **la famille gagne** ; le hub est corrigé, jamais l'inverse.
- **G7 — Hygiène de liens.** Liens **relatifs** uniquement ; un hub dont un lien ne résout pas est **cassé** (vérifiable mécaniquement — la CI par domaine existe déjà dans le dépôt, donc une garde de résolution de liens est faisable, sans être conçue ici).
- **G8 — Gabarit imposé.** Tout hub suit le squelette du §6 ; un hub hors gabarit est non conforme. L'uniformité limite la dérive.
- **G9 — Détachabilité.** La couche navigation doit pouvoir être retirée **sans casser** le contenu (rétroliens optionnels seulement). Test : supprimer `navigation/` ne doit produire **aucun lien cassé** dans les 8 familles.
- **G10 — Cycle de vie.** Un domaine clos/déprécié voit son hub **marqué**, non supprimé (préserve les chemins — cohérent avec la culture renvoi/immuabilité du dépôt).

---

## 8. Dépendances et points à acter avant production

- **D1 — `carte_domaines.md` d'abord.** C'est le registre d'autorité (G4) : aucun hub ne peut être conçu avant que la carte ne fixe la liste canonique et le Tier de chaque domaine. *(La taxonomie est déjà arbitrée ; reste à la transcrire.)*
- **D2 — Question de fond résiduelle.** `humidite_relative_interieure` : hub Tier 1 **non audité** (à acter comme état de cycle, pas comme manque) — n'empêche pas son hub.
- **D3 — Nom/visuel de la zone.** `navigation/` (retenu par défaut) vs marqueur `_navigation/` : décision mineure.
- **D4 — Amorçage recommandé** (cohérent avec la cartographie d'artefacts) : `navigation/README.md` + `carte_domaines.md`, puis les **3 hubs à chaîne complète** (`alarme`, `chauffage`, `vacances`) comme **gabarits de référence** généralisant le patron `lovelace/CI`.

---

*Fin du document de conception. Aucun fichier produit, aucun hub créé : uniquement l'architecture cible de la future couche de navigation.*
