# CONTRAT_ARSENAL_SEARCH_MOTEUR_CLI

**Domaine** : Outils externes / NAS Arsenal / Recherche
**Date de figeage** : 2026-05-08
**Statut** : Actif — implémenté et validé
**Backend nominal validé** : ripgrep 15.1.0 (`/opt/bin/rg`)
**Document parent** : `vision_domaine.md`
**Document frère** : `contrat_webapp.md`

---

## Objet

Ce contrat fige les décisions d'implémentation du script `ha_search.py` :

- backend de recherche,
- structure interne,
- résolution des versions,
- garde-fous de périmètre,
- bornes,
- format de sortie,
- interface CLI.

Il est opposable : toute implémentation qui dévie d'un point de ce contrat doit être soit corrigée, soit faire l'objet d'un amendement explicite.

---

## Place dans l'architecture Arsenal

```text
Arsenal Search (vision)
  └── Phase 1 — moteur backend CLI       ← CE CONTRAT
        └── ha_search.py
  └── Phase 2 — webapp Docker
        └── consommateur officiel du moteur CLI
```

La Phase 1 est strictement un moteur backend. Elle n'est pas une interface utilisateur. Elle valide la logique de filtrage, la grammaire de requête et les bornes de résultats avant emballage en service Phase 2.

---

## Invariants

Hérités du contrat parent. Rappelés ici parce qu'ils gouvernent toutes les décisions techniques qui suivent.

- **Lecture seule** : aucune écriture sur `versions/`, ni sur Home Assistant, ni sur la timeline.
- **Périmètre borné** : confinement strict à `ha_backup_timeline/versions/`. Vérifié à chaque exécution.
- **Aucun shell libre** : la requête n'est jamais interprétée comme une commande système.
- **Aucune exposition publique** : Phase 1 = NAS local uniquement.
- **Résultats bornés** : nombre de résultats, profondeur de contexte et durée plafonnés côté serveur.
- **Autorité fonctionnelle** : le moteur CLI reste l'autorité. La webapp ne réimplémente jamais la logique de recherche. Toute recherche passe par `ha_search.py`. Aucune logique grep n'est dupliquée côté Flask.

---

## Backend de recherche

### Doctrine

Le backend est un **détail d'implémentation interne**, pas une fonctionnalité utilisateur.

| Backend | Statut |
|---------|--------|
| `ripgrep` (`rg`) | nominal |
| `grep` GNU | fallback de compatibilité |

### Sélection automatique

Au démarrage :

- détection de `rg` dans le `PATH`,
- si présent → backend nominal,
- si absent → fallback `grep` avec **avertissement explicite sur stderr** :

```text
[ha_search] avertissement : ripgrep indisponible, fallback grep activé
```

L'avertissement n'est pas désactivable. Il documente l'écart par rapport au backend nominal.

### Aucun flag utilisateur

Le contrat exclut explicitement tout flag du type `--backend rg|grep` :

- pas de surface CLI inutile,
- pas de couplage utilisateur / implémentation,
- pas d'API de debug permanente.

Le comportement fonctionnel doit être **identique** entre les deux backends. Tout écart fonctionnel observable est un bug de l'adaptateur, pas une feature.

---

## Architecture du script

### Structure

```text
ha_search.py
  │
  ├── main()
  │     ├── parse_args()
  │     ├── select_backend()           ← rg ou grep
  │     ├── resolve_versions()         ← --latest / --version / --all-versions
  │     ├── build_path_filters()       ← --exclude-docs / --docs-only
  │     ├── enforce_perimeter()        ← invariant : chemins ⊂ versions/
  │     ├── run_search()               ← UNIQUE frontière subprocess
  │     ├── format_output()            ← compact / contexte
  │     └── print_footer()             ← compteurs + troncature
  │
  └── constantes
        ├── VERSIONS_ROOT
        ├── EXTENSIONS
        ├── EXCLUDED_DIRS
        └── LIMITS
```

### Principes

- **Mono-fichier** en Phase 1.
- **Pas de classe**, pas de framework. Fonctions pures, données circulant par paramètres et retours.
- **Aucun état global mutable**.
- **`run_search()` est la seule fonction qui invoque `subprocess`**. C'est l'unique frontière vers le système et l'unique endroit où l'invariant *aucun shell libre* est appliqué techniquement.
- **`enforce_perimeter()` est la garde de l'invariant *périmètre borné***. Elle est appelée après `resolve_versions()`, avant `run_search()`. Aucun chemin ne sort d'elle sans avoir été validé.

---

## Résolution des versions

### Format de nommage attendu

```text
YYYY-MM-DD_HH-MM_<suffixe libre>
```

Exemples valides :

```text
2026-05-08_08-39_Arsenal_v14.1_d4d230b8
2026-05-08_12-00
2026-05-08_18-45_post_changelog
```

Seul **le préfixe ISO `YYYY-MM-DD_HH-MM`** fait partie du contrat. Le suffixe est libre. Le tri lexicographique sur ce préfixe est strictement équivalent au tri chronologique : le moteur ne doit pas dépendre d'un parsing datetime pour l'ordre des versions.

### Trois flags exclusifs

| Flag | Comportement |
|------|--------------|
| `--latest` | dernière version (tri lexicographique décroissant, premier élément) |
| `--version <nom>` | version désignée par préfixe non ambigu |
| `--all-versions` | toutes les versions, ordre chronologique |

### Règle d'exclusivité

| Cas | Comportement |
|-----|--------------|
| Aucun flag | `--latest` implicite |
| Un seul flag | OK |
| Plusieurs flags | erreur immédiate, sortie code non nul |

### Résolution `--version <nom>`

La valeur passée est traitée comme **préfixe**. Le moteur cherche les répertoires de `versions/` dont le nom commence par cette valeur.

| Cas | Comportement |
|-----|--------------|
| 1 répertoire match | OK, version sélectionnée |
| 0 répertoire match | erreur explicite |
| >1 répertoires match | erreur explicite + liste des matchs |

Aucun fuzzy matching. Aucune heuristique. Préfixe déterministe uniquement.

### Comportements d'erreur

- `versions/` absent → erreur claire, code non nul.
- `versions/` vide → erreur claire, code non nul.
- Aucune version match `--version` → liste des 10 premières versions disponibles + indication `et N autres` si dépassement.

Aucune stack trace utilisateur. Aucun fallback silencieux.

---

## Périmètre et garde-fous

### `enforce_perimeter()`

Fonction de garde, appelée systématiquement avant toute lecture.

Pour chaque chemin résolu :

1. application de `os.path.realpath()` (résolution symlinks et `..`),
2. vérification que le chemin réel commence par `realpath(VERSIONS_ROOT)`,
3. si non → exception immédiate, **pas de fallback**.

### Filtrage extensions

```text
.yaml  .yml  .json  .txt
.j2  .jinja  .jinja2
.md  .py  .js  .ts  .css  .html
```

Implémentation :

- backend `rg` → `--type-add` ou `--glob`,
- backend `grep` → `--include='*.<ext>'`.

### Exclusion répertoires (défense en profondeur)

```text
.storage/
.git/
__pycache__/
deps/
node_modules/
temp/
logs/
```

Ces répertoires ne sont en principe pas présents dans `versions/` (filtrage amont par la timeline). L'exclusion explicite est une garantie redondante.

### Filtrage documentation

| Mode | Comportement |
|------|--------------|
| (par défaut) | inclut `00_documentation_arsenal/` |
| `--exclude-docs` | exclut `00_documentation_arsenal/` |
| `--docs-only` | recherche **uniquement** dans `00_documentation_arsenal/` |

`--exclude-docs` et `--docs-only` sont **mutuellement exclusifs**. Si les deux sont passés → erreur immédiate, pas de priorité implicite.

---

## Bornes

| Paramètre | Valeur par défaut | Plafond dur |
|-----------|-------------------|-------------|
| Nombre de résultats | 200 | 2000 |
| Contexte (lignes) | 5 | 50 |
| Timeout requête | 10 s | 30 s |

- Toutes les bornes sont appliquées **côté serveur**, jamais déléguées au client.
- Une valeur utilisateur supérieure au plafond est ramenée au plafond **sans erreur**.
- Le timeout est appliqué via `subprocess.run(..., timeout=...)`. Dépassement → erreur explicite ; aucun résultat partiel ne doit être présenté comme complet.

### Comportement de troncature

```text
résultats tronqués : 200 affichés sur 1247  •  durée 0.32 s
```

---

## Format de sortie

### Mode compact

Format figé : `[version] chemin_relatif:ligne: contenu`

```text
[2026-05-08_08-39_Arsenal_v14.1_d4d230b8] 11_automations/chauffage/regulation.yaml:42: condition: state sensor.temperature_jardin
[2026-05-08_08-39_Arsenal_v14.1_d4d230b8] 11_automations/chauffage/regulation.yaml:78:   - sensor.temperature_jardin
[2026-04-15_18-12_Arsenal_v14.0]          11_automations/chauffage/regulation.yaml:42: condition: state sensor.temperature_jardin
```

- Chemin **relatif** à la racine de la version, jamais absolu.
- Version entre crochets en tête de ligne (grep-able, awk-able).
- `:` après le numéro de ligne (compatible éditeurs : `vim path:42`).

### Mode contexte

```text
═══════════════════════════════════════════════════════════
[2026-05-08_08-39_Arsenal_v14.1_d4d230b8] 11_automations/chauffage/regulation.yaml:42
───────────────────────────────────────────────────────────
  37  - alias: Régulation chauffage salon
  38    trigger:
  39      - platform: state
  40        entity_id: sensor.temperature_jardin
  41    condition:
> 42      - condition: state
  43        entity: sensor.temperature_jardin
  44        state: 'on'
  45    action:
  46      - service: climate.set_temperature
  47        target:
═══════════════════════════════════════════════════════════
```

- Séparateur `═` épais entre matchs.
- Séparateur `─` fin entre en-tête et contenu.
- Ligne de match préfixée `> ` (un caractère + espace, copier/coller propre).
- Numéros de ligne alignés à droite sur 4 chiffres.

### Footer obligatoire

Toujours présent, même à 0 résultat.

```text
───────────────────────────────────────────────────────────
3 résultats sur 2 versions  •  durée 0.18 s
```

```text
───────────────────────────────────────────────────────────
0 résultat sur 1 version  •  durée 0.04 s
```

```text
───────────────────────────────────────────────────────────
résultats tronqués : 200 affichés sur 1247  •  durée 0.32 s
```

Le footer permet de distinguer *aucun match* de *moteur silencieusement défaillant*.

### Couleur

- `stdout` est un TTY → sortie colorée.
- `stdout` est redirigé (fichier, pipe) → sortie monochrome.
- Détection automatique via `sys.stdout.isatty()`. Aucun flag utilisateur.

---

## Interface CLI

### Synopsis

```text
ha_search.py --query <texte> [options de version] [options de filtrage] [options de sortie]
```

### Options figées

```text
--query <texte>          requête (obligatoire)

# Sélection de version (mutuellement exclusives, défaut : --latest)
--latest
--version <préfixe>
--all-versions

# Filtrage documentation (mutuellement exclusives)
--exclude-docs
--docs-only

# Recherche
--case-sensitive
--regex

# Sortie
--mode compact|context   défaut : compact
--context N              défaut : 5, plafond : 50

# Bornes
--max-results N          défaut : 200, plafond : 2000
```

### Comportements par défaut

| Sans flag | Comportement |
|-----------|--------------|
| Aucun flag de version | `--latest` |
| Aucun flag de docs | inclut la documentation |
| `--mode` non précisé | `compact` |
| `--context` non précisé | 5 lignes (mode contexte uniquement) |
| `--case-sensitive` non précisé | recherche insensible à la casse |
| `--regex` non précisé | recherche texte littérale |

### Code de sortie

| Code | Signification |
|------|---------------|
| 0 | OK (avec ou sans résultats) |
| 1 | erreur d'utilisation (flags incompatibles, valeur invalide) |
| 2 | erreur d'environnement (`versions/` absent, backend indisponible critique) |
| 3 | timeout requête |

---

## Qualités exigées

- **lisible** — un relecteur Arsenal doit pouvoir le parcourir entièrement en une session,
- **auditable** — chaque garde-fou et chaque borne doit être localisable rapidement,
- **mono-fichier** en Phase 1,
- **sans framework**,
- **à responsabilités explicites** — une fonction, une responsabilité,
- **sans état global mutable**,
- **sans dépendance Python tierce** (stdlib uniquement).

---

## Non-objectifs du moteur CLI

Hors champ du moteur CLI lui-même :

- sortie JSON,
- interface graphique ou web,
- service Docker,
- accès distant (HTTP, SSH automatisé, etc.),
- cache de résultats,
- index inversé,
- statistiques d'usage,
- comparaison entre versions (diff intégré),
- export markdown structuré.

Ces fonctions relèvent de la Phase 2 ou d'évolutions ultérieures et ne doivent pas pré-contaminer l'architecture du moteur.

---

## Compatibilité Phase 2 validée

Les contraintes de conception ont permis l'intégration Phase 2 sans rupture :

- fonctions pures et importables — la webapp invoque le moteur sans couplage,
- structures de données simples (dict, list, tuple) — pas de sérialisation propriétaire,
- logique métier découplée du formatage texte — la webapp consomme stdout sans parser du rendu terminal,
- API CLI conservée intégralement — `subprocess` côté Flask appelle exactement les mêmes flags.

Évolutions restant compatibles sans casser l'API :

- ajout d'un flag `--output-format text|json` (texte reste défaut),
- ajout de filtres de chemin supplémentaires (`--include-path`, `--exclude-path`),
- pagination (`--offset N`).

---

## Validation

Validation réalisée sur NAS Synology `NAS_VALENTIN`.

### Tests validés — Phase 1

- recherche compacte sur dernière version,
- recherche contexte avec 3 lignes avant/après,
- exclusion de la documentation via `--exclude-docs`,
- recherche limitée à la documentation via `--docs-only`,
- requête contenant `/`,
- backend nominal `ripgrep`,
- footer obligatoire.

### Décisions confirmées par l'implémentation

- **Backend nominal** : ripgrep 15.1.0, accessible via `/opt/bin/rg`, utilisable par utilisateur NAS non-root.
- **Parsing backend** : sortie normalisée par séparateur `\0` pour parsing non ambigu sur les chemins contenant `:` ou `-`.
  - rg : `--null`
  - grep : `-Z`
- **Discipline des commandes** : tous les flags et filtres avant le motif, motif via `--regexp` (rg) ou `-e` (grep), racine en dernière position. Forme canonique GNU.

### Tests validés — Phase 2

- intégration Flask validée,
- exécution Docker validée,
- accès LAN validé,
- accès mobile validé,
- montage `versions/` en lecture seule validé,
- montage `ha_search.py` en lecture seule validé,
- regroupement UI version/fichier validé.

### Statut

Phase 1 et Phase 2 opérationnelles.

---

## Amendements

### v1.0 — 2026-05-08

Création initiale. Implémentation validée. Intégration Phase 2 sans rupture confirmée.
