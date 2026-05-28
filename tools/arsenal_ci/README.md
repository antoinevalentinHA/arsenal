# Arsenal CI — Chauffage (étage 1) — Intégration repo

## Emplacement dans le dépôt

```
<repo>/
├── 00_documentation_arsenal/contrats/chauffage/ci/
│   └── registres_entites.yaml          # artefact souverain — NE migre PAS sous tools/
├── tools/arsenal_ci/                    # le moteur (package Python)
│   ├── parsing/ graph/ registers/ rules/ report/
│   ├── cli.py
│   └── tests/                           # fixtures synthétiques, autonomes
├── .github/workflows/
│   └── arsenal-ci-chauffage.yml
```

Le registre reste à son emplacement souverain ; l'outil le lit par chemin.
Les fixtures de test restent synthétiques et ne pointent jamais vers la vraie config.

## Commande locale officielle

Identique en local et en CI (la CI ne fait rien d'irreproductible à la main) :

```bash
python -m tools.arsenal_ci.cli \
  --registry 00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml \
  --config packages/chauffage/autorisation.yaml \
  --json arsenal_ci_report.json
```

Exit codes : `0` conforme · `1` violation doctrinale · `2` erreur d'exécution (outil/registre cassé).
Option `--strict` : un warning provoque alors un exit `1`.

## Self-test

```bash
python -m pytest tools/arsenal_ci/tests/ -q
```

## Stratégie de transition warn-only → bloquant

La bascule est une variable unique en tête de workflow :

```yaml
env:
  ARSENAL_CI_ENFORCE: "false"   # phase A : warn-only
                                # "true"  : phase B : bloquant
```

| Phase | exit 1 (violation) | exit 2 (erreur exécution) |
|-------|--------------------|---------------------------|
| A — warn-only (`false`) | n'échoue pas (warning + artifact) | **échoue** |
| B — bloquant (`true`)   | **échoue** | **échoue** |

L'erreur d'exécution est bloquante dès la phase A : un juge défectueux doit être vu
immédiatement, indépendamment de la tolérance doctrinale. La bascule A→B est un
diff unique, traçable en PR (décision doctrinale explicite).

## Extension de la cible

La liste des fichiers validés est explicite dans le workflow (tableau `CONFIGS`).
On l'étend fichier par fichier, jamais par glob implicite.
