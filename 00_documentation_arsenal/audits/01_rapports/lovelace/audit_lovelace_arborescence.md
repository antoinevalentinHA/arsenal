# Audit — Refonte arborescence Lovelace (chantier *evolutions_futures*)

**Périmètre** : contre-expertise du document `00_documentation_arsenal/evolutions_futures/lovelace_arborescence.md`
**Base d'analyse** : dépôt public `antoinevalentinHA/arsenal`, HEAD `34bcd7e` (2026-06-04 10:00:46 +0200)
**Document audité** : dernière modif `3865655` (2026-06-02)
**Nature** : audit en lecture seule. Aucun patch, aucune modification, aucune proposition de migration.

---

## 0. Verdict en une phrase

Le chantier est **légitime sur le fond, sans valeur opérationnelle, et nettement moins dangereux que ne le laisse croire le document** : le risque qu'il met en avant en premier (rupture de navigation) est en réalité **structurellement découplé** de tout déplacement de fichier, tandis que le seul risque réel — les includes relatifs — est **borné, mécanique, mais aujourd'hui sans aucun filet CI**.

---

## 1. Cartographie complète de l'organisation Lovelace actuelle

### 1.1 Point d'entrée et chaîne de chargement

```
configuration.yaml
  └─ lovelace: !include 18_lovelace/lovelace_main.yaml
        ├─ resource_mode: yaml
        ├─ resources:  !include resources.yaml      (7 ressources JS /local/… — aucun couplage dashboard)
        └─ dashboards: !include dashboards.yaml      (REGISTRE CENTRAL — 83 entrées)
```

### 1.2 Arborescence physique `18_lovelace/`

```
18_lovelace/
├── lovelace_main.yaml            # 3 lignes, point d'entrée
├── resources.yaml                # ressources JS uniquement
├── dashboards.yaml               # registre : 83 entrées { mode, title, icon, sidebar, filename }
├── dashboards/                   # 83 fichiers .yaml répartis sur 3 niveaux de profondeur
│   ├── *.yaml                    # 24 dashboards « racine »  (profondeur 0)
│   ├── diagnostics/   (20)       # profondeur 1
│   ├── reglages/      (16)       # profondeur 1
│   ├── meteo/         (11)       # profondeur 1
│   ├── voiture/        (3)       # profondeur 1
│   └── imprimerie/     (5)       # profondeur 1
│       └── meteo/      (4)       # profondeur 2  ← seul point à 3 niveaux
└── includes/                     # fragments réutilisables (cible des !include relatifs)
    ├── badges/         (4)
    ├── cartes/        (40)
    ├── navigation/     (4)       # cartes de navigation partagées (meteo, imprimerie, voiture, ecs_planning)
    ├── section_headers/(28)
    └── sub_section_headers/(7)
```

### 1.3 Chiffres de référence

| Métrique | Valeur |
|---|---|
| Dashboards déclarés dans `dashboards.yaml` | **83** |
| Fichiers `.yaml` de dashboard sur disque | **83** (correspondance 1:1, **aucun orphelin**) |
| Dashboards mono-vue | **83 / 83 (100 %)** |
| Dashboards multi-vues | **0** |
| Occurrences `navigation_path` (dans les dashboards) | 110 |
| Cibles de nav dans le menu central `navigation.yaml` | 32 |
| Directives `!include` (toutes) | 288 |
| Fichiers utilisant un include **relatif** (`../`) | **62 / 83** |
| Fichiers **sans** include relatif | 21 |
| Vues avec `path:` explicite | **1 seule** (`imprimerie/nas.yaml`) |

---

## 2. Tableau de classement des 83 dashboards

> Difficulté calculée mécaniquement à partir du **changement de profondeur** induit par la cible du document
> (tous les domaines ramenés à `dashboards/<domaine>/`, soit profondeur 1).
> `includes/` est supposé rester en place → la profondeur relative est le seul facteur de réécriture.

### Synthèse par classe

| Difficulté | Nombre | Définition |
|---|---|---|
| **Triviale** | 21 | aucun include relatif → simple déplacement + 1 ligne `filename:` |
| **Faible** | 36 | includes présents mais **profondeur inchangée** → `../../` reste valide |
| **Moyenne** | 26 | la profondeur change → **includes à réécrire** (22 fichiers `+1` niveau ; 4 fichiers `-1` niveau) |
| **Élevée / Très élevée** | **0** | aucun cas |

**Conclusion factuelle : la migration ne contient aucun cas de difficulté élevée.** Le risque est concentré sur 26 fichiers, et il est de nature purement textuelle (réécriture de préfixe `../`).

### Détail (extrait représentatif — fichier complet ci-dessous reproduit l'intégralité)

| Fichier actuel | Domaine fonctionnel | Cible (doc) | Includes | Difficulté | Risque |
|---|---|---|---|---|---|
| `chauffage.yaml` | climat | `climat/` | 2 | Moyenne | 2 includes → `../` à `../../` |
| `clim.yaml` | climat | `climat/` | 3 | Moyenne | 3 includes (+1 niveau) |
| `ecs.yaml` | ecs | `ecs/` | 3 | Moyenne | 3 includes (+1 niveau) |
| `ouvertures.yaml` | sécurité | `securite/` | 4 | Moyenne | 4 includes (+1 niveau) |
| `volets.yaml` | sécurité | `securite/` | 0 | Triviale | aucun include |
| `sante.yaml` | santé | `sante/` | 0 | Triviale | aucun include |
| `system.yaml` | système | `systeme/` | 2 | Moyenne | 2 includes (+1 niveau) |
| `diagnostics/chauffage.yaml` | diagnostics | `diagnostics/` | 2 | Faible | profondeur inchangée |
| `reglages/ecs_planning.yaml` | reglages | `reglages/` | **15** | Faible | profondeur inchangée (volume élevé mais stable) |
| `meteo/meteo_temperature_min_max.yaml` | meteo | `meteo/` | 8 | Faible | profondeur inchangée |
| `imprimerie/meteo/temperature.yaml` | imprimerie | `imprimerie/` | 3 | Moyenne | **-1 niveau** : `../../../` à `../../` |
| `imprimerie/meteo/humidex.yaml` | imprimerie | `imprimerie/` | 2 | Moyenne | -1 niveau |

> Les 4 fichiers `imprimerie/meteo/` sont les seuls dont la profondeur **diminue** (ils remontent de 2 à 1).
> Les 22 dashboards « racine » avec includes voient leur profondeur **augmenter** (0 à 1).
> Les 36 fichiers déjà en sous-dossier (diagnostics, reglages, meteo, voiture, imprimerie direct) **ne bougent pas en profondeur**.

---

## 3. Cartographie des dépendances (le cœur de la contre-expertise)

C'est ici que le document se trompe de hiérarchie de risque. Voici le graphe réel des dépendances et leur sensibilité à un **déplacement de fichier**.

| Dépendance | Mécanisme HA | Couplée à l'emplacement du fichier ? | Verdict |
|---|---|---|---|
| **`filename:`** (dashboards.yaml) | chemin repo-relatif vers le fichier | **OUI** — directement | À mettre à jour : 83 lignes, **dans un seul fichier** |
| **slug d'URL** (`/xxx-dashboard/…`) | dérivé de la **CLÉ** de `dashboards.yaml`, **pas** du `filename` | **NON** | Insensible au déplacement |
| **`navigation_path`** (110 occ.) | pointe vers `/slug/vue` | **NON** (via slug) | Insensible au déplacement |
| **Boutons de navigation** (`19_button_card_templates/40_dashboards/…`, 14 slugs distincts) | référencent le slug | **NON** | Insensible au déplacement |
| **2ᵉ segment d'URL** (vue) | `path:` de vue, sinon index auto | **NON** | De plus, **100 % mono-vue** → segment cosmétique |
| **`!include ../…`** (relatif) | résolu par profondeur de répertoire | **OUI — par la PROFONDEUR** | **Seul vrai risque** ; 26 fichiers concernés |
| **`!include_dir_merge_named /config/19_button_card_templates`** | chemin **absolu** | **NON** | Insensible |
| **`resources.yaml`** | URLs `/local/…` | **NON** | Insensible |
| **Références externes au chemin fichier** (`18_lovelace/dashboards/…` hors lovelace) | — | — | **0 occurrence** dans tout le dépôt |

### Démonstration du découplage navigation ↔ fichier

`clim.yaml` est enregistré sous la clé `clim-dashboard`. Tous les liens entrants pointent vers `/clim-dashboard/…`. Déplacer le fichier vers `dashboards/climat/clim.yaml` n'exige **que** la mise à jour de la ligne `filename:` ; la clé `clim-dashboard` — donc le slug, donc tous les `navigation_path` et tous les boutons — **reste identique**. La navigation ne casse que si l'on renomme les **clés**, ce qu'un déplacement de fichier n'impose jamais.

### Démonstration du couplage include ↔ profondeur

- `dashboards/chauffage.yaml` (prof. 0) : `!include ../includes/section_headers/decision.yaml`
- `dashboards/meteo/meteo_co2.yaml` (prof. 1) : `!include ../../includes/badges/base.yaml`
- `dashboards/imprimerie/meteo/temperature.yaml` (prof. 2) : `!include ../../../includes/navigation/imprimerie.yaml`

Le nombre de `../` est strictement égal à la profondeur. **Tout changement de profondeur invalide l'include.**

---

## 4. Analyse de faisabilité et de risque — contre-expertise du document

### 4.1 Confrontation point par point des risques du document

| Risque affirmé dans le document | État réel observé au HEAD | Verdict |
|---|---|---|
| « `navigation_path` → risque de rupture UI » | Slug = clé `dashboards.yaml`, **découplé du fichier** ; de plus **100 % mono-vue** → 2ᵉ segment cosmétique | **SURÉVALUÉ** — risque quasi nul pour un simple déplacement |
| « includes relatifs (`../`) → fragiles » | Exact : 62/83 en dépendent, 26 à réécrire selon la profondeur | **VALIDE** — c'est le **seul** vrai risque |
| « `filename` → à maintenir cohérent » | Exact mais trivial : 83 lignes, **un seul fichier**, **0 référence externe** | **VALIDE mais FAIBLE** |
| « badges et navigation → dépendances implicites » | Badges = includes relatifs (se replie sur le risque includes) ; navigation = slug (sûr) | **PARTIELLEMENT VALIDE** |
| « erreurs silencieuses difficiles à diagnostiquer » | **Confirmé et aggravé** : voir 4.2 | **VALIDE — facteur déterminant** |
| « casse des dashboards existants » | Possible **uniquement** via include cassé ; navigation immunisée | **CIRConscrit aux includes** |

### 4.2 Le facteur décisif : absence totale de filet CI sur la couche Lovelace

C'est l'élément qui transforme un risque « faible » en risque « réel mais évitable ».

- La CI Arsenal compte **~60 workflows**, **tous** des validateurs de contrats métier (`arsenal_ci`, topologie décisionnelle, entités). **Aucun** ne valide la résolution des `!include` Lovelace.
- Les deux workflows qui *mentionnent* `18_lovelace/` (`climatisation_admissibilite`, `palmares_…_froid`) ne font que **déclencher** des validateurs d'entités via un filtre `paths:` — ils **ne valident pas** la structure Lovelace.
- Le workflow parapluie `validation.yml` exécute uniquement :
  ```yaml
  run: yamllint -f parsable . || true
  ```
  Deux faiblesses cumulées :
  1. **`|| true`** → même un échec yamllint **ne bloque pas** la CI.
  2. **yamllint ne résout pas `!include`** → un `../includes/…` cassé est traité comme un scalaire opaque et **passe inaperçu**.
- **Aucun `hass --script check_config`**, aucun résolveur d'includes nulle part.

**Conséquence** : un include mal réécrit après déplacement **ne serait détecté par aucune barrière automatique**. Il ne se manifesterait qu'au runtime HA (carte vide / erreur de config dans les logs). C'est exactement la « erreur silencieuse difficile à diagnostiquer » du document — et elle est aujourd'hui **réelle et non gardée**.

### 4.3 Le chantier est-il « réellement dangereux aujourd'hui » ?

**Non, pas au sens catastrophique** suggéré par le document :
- pas de cas de difficulté élevée ;
- navigation structurellement immunisée ;
- mise à jour `filename:` confinée à un fichier, sans référence externe ;
- réécriture d'includes bornée à 26 fichiers, intégralement scriptable et vérifiable.

**Oui, sur un point précis et non couvert** : sans validateur d'includes, la phase de réécriture peut introduire des régressions **silencieuses**.

### 4.4 Contre-point fort sur la stratégie du document

Le document recommande une **migration progressive domaine par domaine** et déconseille la migration globale. **Du point de vue de la couche include, c'est l'inverse qui est le plus sûr** :

- Une migration **globale scriptée** = une transformation atomique, une seule passe de réécriture cohérente, un seul PR, une seule validation.
- Une migration **progressive** = l'arborescence vit en **état hybride prolongé** (domaines à l'ancienne profondeur cohabitant avec des domaines migrés), augmentant la charge cognitive et la fenêtre d'erreurs de profondeur, et exigeant **N** passes de vérification.

Le document raisonne « petit lot = petit risque » (vrai pour du code métier), mais ici le risque est **structurel et homogène** : il se traite mieux en une transformation déterministe unique.

---

## 5. Estimation du coût réel

| Poste | Charge | Niveau |
|---|---|---|
| Mise à jour des 83 `filename:` | mécanique, 1 fichier, scriptable | très faible |
| Déplacement des 83 fichiers | `git mv`, scriptable | très faible |
| Réécriture des includes de **26** fichiers | textuel, déterministe (préfixe `../`) | faible-moyen |
| Réécriture des **36** fichiers à profondeur stable | **nulle** (rien à changer) | nul |
| Vérification d'intégrité (faute de CI dédiée) | **manuelle aujourd'hui** → c'est le vrai poste | moyen |

**Coût global : MOYEN.** (Le document affiche « Élevé » — **surévalué**.)
Le coût bascule en **FAIBLE** dès lors qu'un validateur d'includes existe ; il reste **MOYEN** tant que la vérification est manuelle. Le poste dominant n'est pas la transformation, c'est **l'absence d'outil de contrôle**.

---

## 6. Recommandation finale

### Décision recommandée : **MAINTIEN EN DETTE DOCUMENTAIRE** — mais avec correction du raisonnement de risque

Justification :

1. **Le document a raison sur la valeur** : gain fonctionnel, UX et robustesse **nuls**. Rien ne justifie d'engager le chantier *pour lui-même*. La conclusion « imparfait mais stable, non optimal mais maîtrisé » reste exacte.

2. **Le document a tort sur la hiérarchie du risque** : il agite la rupture de navigation (en réalité quasi impossible par simple déplacement) et sous-spécifie le seul danger réel (includes + absence de CI). À corriger dans le document.

3. **Action à valeur réelle, indépendante de toute migration** : ajouter un **contrôle de résolution des `!include` Lovelace** dans la CI (un simple résolveur qui vérifie que chaque cible `../…` existe). Ce garde-fou :
   - comble une faille **actuelle** (un include cassé passe aujourd'hui inaperçu, migration ou pas) ;
   - transforme le coût de toute migration future de MOYEN à FAIBLE ;
   - s'inscrit dans la doctrine Arsenal « contrats avant YAML / invariants explicites / CI gardienne ».

4. **Si la migration est un jour déclenchée** (condition du document : refonte Lovelace majeure), privilégier une **migration globale scriptée et atomique** plutôt que progressive — contrairement à la stratégie écrite — précisément parce que le risque est structurel et homogène.

### Hiérarchie des options

| Option | Évaluation |
|---|---|
| Abandon définitif | **Non** — la dette est réelle (hétérogénéité documentée), l'abandon effacerait une analyse correcte |
| **Maintien en dette documentaire** | **RETENU** — défaut rationnel ; aucun gain opérationnel n'impose d'agir |
| Migration progressive domaine par domaine | **Déconseillé** — paradoxalement le plus risqué pour la couche include (état hybride prolongé) |
| Migration globale | **Envisageable et techniquement la plus sûre** *si et seulement si* déclenchée par un besoin réel **et** précédée du validateur d'includes |

---

## 7. Synthèse exécutive

- 83 dashboards, 100 % mono-vue, registre 1:1 sans orphelin.
- La navigation est **découplée** de l'emplacement des fichiers (slug = clé, pas `filename`) → le risque « phare » du document est surévalué.
- Le **seul** vrai risque est l'include relatif couplé à la profondeur : **26 fichiers** à réécrire, transformation purement textuelle.
- Le **vrai** problème n'est pas la migration, c'est **l'absence de tout contrôle CI sur les includes** (`yamllint || true`, sans résolution d'`!include`).
- Coût réel : **MOYEN** (et non Élevé), → **FAIBLE** avec un validateur.
- Recommandation : **dette documentaire** + corriger la hiérarchie de risque du document + créer un validateur d'includes (utile indépendamment de toute migration).

*Audit en lecture seule. Aucune modification du dépôt n'a été effectuée.*
