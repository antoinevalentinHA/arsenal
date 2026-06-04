# Arsenal CI — Chauffage (lint étage 1 + analyses décision/exécution) — Intégration repo

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
  --config 12_template_sensors/chauffage/autorisation.yaml \
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

## Les trois analyseurs (rôles non interchangeables)

Le moteur n'est pas un lint unique. Le workflow exécute **trois analyseurs**
parallèles, en plus du self-test :

- **Étage 1 — lint structurel** (`arsenal_ci.cli`) : construit un graphe à partir
  d'un fichier passé via `--config` et applique les règles structurelles.
- **Étage 2 — décision** (`arsenal_ci.decision.cli_decision`) : analyse la cascade
  de décision (R-COV-1 / R-MIRROR-1 runtime). **N'utilise pas `--config`.**
- **Étage 3 — exécution** (`arsenal_ci.execution.cli_execution`) : analyse la
  topologie d'appel de la couche d'application (R-CALL-1, CH-4 : appelants de
  `chauffage_appliquer_consigne`). **N'utilise pas `--config`.**

Invocations (identiques en local et en CI) :

```bash
python -m arsenal_ci.decision.cli_decision   --json ci_reports/decision.json
python -m arsenal_ci.execution.cli_execution --json ci_reports/execution.json
```

## Portée de `CONFIGS` (étage 1 uniquement)

La liste des fichiers validés est explicite dans le workflow (tableau `CONFIGS`).
On l'étend fichier par fichier, jamais par glob implicite.

**`CONFIGS` ne borne que l'étage 1 (lint).** Les étages 2 (décision) et 3
(exécution) ne lisent pas `CONFIGS` : ils couvrent la cascade de décision et la
topologie d'appel **indépendamment** de cette liste. Une liste `CONFIGS` courte
ne signifie donc **pas** que « un seul fichier est validé » : elle signifie que
le lint structurel s'ancre sur ce(s) fichier(s), pendant que les étages 2/3
opèrent sur leur propre objet.

## Registre et META-2 — ce qui porte la couverture de classification

La **couverture de classification** des entités décisionnelles n'est pas portée
par `CONFIGS` mais par le registre souverain
`00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml`, qui
classe chaque entité (registre / couche / niveau) en citant un contrat opposable.

La règle **META-2** vérifie que **tout nœud présent dans un graphe parsé** existe
dans le registre (sinon : périmètre incomplet). Sa portée est donc l'union des
graphes effectivement construits par les analyseurs — **pas l'ensemble des
fichiers chauffage du dépôt**. META-2 ne parcourt pas tous les fichiers : il
contrôle les nœuds des graphes qu'on lui donne à juger.

## Gating CI : warn-only (état courant)

L'état courant du workflow est `ARSENAL_CI_ENFORCE: "false"`, soit **phase A
(warn-only)** : une violation doctrinale (exit 1), y compris une violation
META-2, **ne fait pas échouer la CI** ; seule une erreur d'exécution (exit 2)
bloque. La bascule vers la phase bloquante est décrite ci-dessus (section
« Stratégie de transition »). « Bloquant » au sens de `meta2_mode` (sévérité de
la règle) est donc distinct de « bloquant » au sens du gating CI
(`ARSENAL_CI_ENFORCE`).
