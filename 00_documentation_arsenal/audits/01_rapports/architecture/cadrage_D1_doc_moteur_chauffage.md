# Rapport préparatoire — chantier D1 (clarification doc moteur chauffage)

**Périmètre** : cadrage du chantier documentaire D1. **Base** : HEAD `899c172` (2026-06-04).
**Nature** : rapport préparatoire en lecture seule. **Aucun patch, aucun fichier modifié.** Objet : produire un cadrage exact et opposable avant toute écriture.
**Sources relues intégralement** :
- `tools/arsenal_ci/README.md`
- `.github/workflows/arsenal-ci-chauffage.yml`
- `00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml` (en-tête + champs + registres)
- `tools/arsenal_ci/rules/meta_2.py` (règle META-2)
- `tools/arsenal_ci/cli.py`, `…/decision/cli_decision.py`, `…/execution/cli_execution.py` (points d'entrée des trois analyseurs)
- les éléments ayant conduit au retrait de A1 (contre-expertise A1/B1).

---

## 1. Rôles exacts (état vérifié)

### 1.1 Le lint sur `autorisation.yaml` (étage 1)
- C'est **un** des analyseurs, déclenché par le job `lint` du workflow. Il prend un fichier via `--config`, en construit un **graphe d'entités**, et applique les règles structurelles.
- Sa cible est la **liste `CONFIGS`** du workflow, aujourd'hui réduite à `12_template_sensors/chauffage/autorisation.yaml` (autorité Niveau 1, sécurité système).
- **Fait clé** : `CONFIGS` ne pilote **que** le périmètre du lint étage-1. Il ne pilote ni l'étage-2 (décision) ni l'étage-3 (exécution).

### 1.2 Le registre `registres_entites.yaml`
- **Artefact souverain** (contrat exécutable) : il **classe** chaque entité décisionnelle par `registre` / `couche` / `niveau` / `statut`, en citant un contrat markdown opposable. Il **ne crée aucune doctrine** (règle D-REG-7 : le markdown prime).
- Il déclare son propre périmètre : `perimetre_statut: "complet"`, `meta2_mode: "bloquant"`, `version: "1.0-complet"`.
- C'est **lui**, et non la liste `CONFIGS`, qui porte la **couverture de classification** des entités décisionnelles.

### 1.3 Les étages décision (2) et exécution (3)
- **Étage 2 — `decision` (`cli_decision`)** : analyse la **cascade de décision** (R-COV-1 runtime + R-MIRROR-1 runtime). Il **ne prend pas de `--config`** : il lit le cerveau de décision directement (déclencheurs `paths` du workflow : `10_scripts/chauffage/decision_centrale.yaml`, …).
- **Étage 3 — `execution` (`cli_execution`)** : analyse la **topologie d'appel** de la couche d'application (R-CALL-1 : appelants de `chauffage_appliquer_consigne`, CH-4). Lui aussi **sans `--config`**.
- Les deux sont des **analyseurs parallèles** au lint, **indépendants de `CONFIGS`**.

### 1.4 META-2
- Règle vérifiant que **tout nœud présent dans un graphe parsé** existe dans le registre ; sinon, violation de classe « bloquante » (périmètre incomplet).
- **Portée exacte** (lot 1.2, cf. docstring `meta_2.py`) : les **nœuds qu'Arsenal déclare et gouverne** dans le graphe analysé — pas toutes les cibles externes référencées.
- Donc META-2 **ne parse pas tous les fichiers chauffage** : sa portée effective = l'union de ce que les trois étages construisent comme graphes.

---

## 2. Ce qui est réellement couvert / non couvert

**Réellement couvert (faits) :**
- La **classification** de toutes les entités décisionnelles : portée par le registre, déclaré `complet`.
- La **cascade de décision** : étage 2, indépendamment de `CONFIGS`.
- La **topologie d'appel** d'exécution (frontière R-CALL-1) : étage 3, indépendamment de `CONFIGS`.
- Le **lint structurel** de l'autorité Niveau 1 : étage 1, sur `autorisation.yaml`.
- La **santé de l'outil** : self-test (136 tests sur fixtures synthétiques).

**Non couvert / borné (faits) :**
- Le **lint structurel étage-1 des autres fichiers** chauffage (au-delà d'`autorisation.yaml`) : non, par cadrage explicite (« étendre fichier par fichier »).
- Le **gating effectif** : `ARSENAL_CI_ENFORCE: "false"` → l'ensemble tourne en **warn-only**. Une violation doctrinale (exit 1), y compris META-2, **n'échoue pas** le job ; seules les erreurs d'exécution (exit 2) bloquent.
- La **conformité runtime** (comportement réel) : hors de portée d'analyseurs statiques.

**Conséquence de cadrage :** « `CONFIGS` = 1 fichier » **n'a jamais signifié** « 1 seul fichier validé ». Cela signifie « le lint structurel s'ancre sur 1 fichier, pendant que la classification (registre) et les analyses décision/exécution couvrent leur objet indépendamment de `CONFIGS` ».

---

## 3. Pourquoi l'audit initial a conclu à tort à une couverture limitée

Cause racine : **le `README` de l'outil ne décrit que l'étage 1.** Un lecteur du `README` voit « lint de `autorisation.yaml` » + « extension de `CONFIGS` fichier par fichier », et **rien** sur :
- les étages 2 (décision) et 3 (exécution / R-CALL-1) ;
- le rôle du registre comme **artefact de couverture** ;
- META-2.

D'où l'équation erronée **« `CONFIGS` court ⇒ couverture limitée »**, alors que `CONFIGS` ne borne que le lint étage-1.

Facteur aggravant : **trois notions de « bloquant » distinctes**, non disjointes dans la doc, faciles à confondre :
1. `meta2_mode: "bloquant"` (registre) = META-2 émet une **sévérité** violation plutôt qu'avertissement ;
2. `policy.meta2_active` = META-2 **s'exécute** ou non ;
3. `ARSENAL_CI_ENFORCE: "false"` (workflow) = une violation (exit 1) **fait échouer la CI** ou non — actuellement **non** (warn-only).
La contre-expertise a elle-même raccourci en « META-2 bloquant », sans distinguer (1) de (3).

---

## 4. Inexactitudes, ambiguïtés, manques (par fichier)

### 4.1 `tools/arsenal_ci/README.md`
- **Inexact** — Titre « Arsenal CI — Chauffage (**étage 1**) » : l'outil comporte **trois** analyseurs (lint, décision, exécution). Le titre sous-décrit la portée.
- **Inexact** — Exemple « Commande locale officielle » : `--config packages/chauffage/autorisation.yaml`. Le dossier `packages/` **n'existe pas** ; le chemin réel est `12_template_sensors/chauffage/autorisation.yaml` (cf. `CONFIGS` du workflow).
- **Manque** — Aucune mention des **étages 2/3** (`cli_decision`, `cli_execution`, R-COV-1/R-MIRROR-1/R-CALL-1).
- **Manque** — Aucune mention du **registre comme artefact de couverture** ni de **META-2**.
- **Ambigu** — Section « Extension de la cible » : laisse croire que la couverture **dépend** de `CONFIGS`, sans préciser que `CONFIGS` ne borne que l'étage-1.

### 4.2 `.github/workflows/arsenal-ci-chauffage.yml`
- **Inexact** — `name: "Arsenal CI — Chauffage (etages 1 & 2)"` : le workflow contient un **job `execution`** explicitement décrit en commentaire comme « **Troisième analyseur** ». Le nom omet l'étage 3.
- **Ambigu (mais correct)** — Commentaire `# Config chauffage validee (a ajuster a l'arborescence reelle)` : laisse penser que le chemin pourrait être faux ; il est en réalité correct (`12_template_sensors/chauffage/**.yaml`). À clarifier ou retirer.

### 4.3 `…/contrats/chauffage/ci/registres_entites.yaml`
- **Contradiction interne** — L'**en-tête en prose** dit : « VERSION : PARTIELLE — CERCLE 1 … Tant que la couverture n'est pas complète, META-2 doit être exécuté en mode **WARNING, non bloquant** ». Les **champs machine** disent : `perimetre_statut: "complet"`, `meta2_mode: "bloquant"`, `version: "1.0-complet"`. **Prose et données se contredisent** : l'une décrit un état partiel/warning, l'autre un état complet/bloquant.
- **Conséquence** : un lecteur ne sait pas quel état fait foi. (Artefact souverain → sensibilité accrue, cf. §5.)

---

## 5. Périmètre exact proposé du correctif D1

D1 est **documentaire**. Il **clarifie** ; il **n'ajoute aucun contrôle** et **ne touche aucune logique** (ni `CONFIGS`, ni règles, ni `env`).

### Fichiers à modifier et justification

| Fichier | Modification (intention, sans patch) | Pourquoi nécessaire |
|---|---|---|
| `tools/arsenal_ci/README.md` | Corriger le chemin d'exemple (`packages/…` → `12_template_sensors/chauffage/autorisation.yaml`) ; ajuster le titre pour ne plus le réduire à « étage 1 » ; **ajouter** une section décrivant les **trois analyseurs**, le **rôle du registre comme artefact de couverture**, **META-2**, et le fait que **`CONFIGS` ne borne que le lint étage-1** | Cause racine de la mauvaise interprétation : c'est le document que lit un observateur externe. Le corriger dissout la confusion « `CONFIGS` court ⇒ couverture limitée ». |
| `.github/workflows/arsenal-ci-chauffage.yml` | Corriger le `name:` pour refléter les **trois** analyseurs ; clarifier ou retirer le commentaire « a ajuster a l'arborescence reelle » devenu trompeur | Le nom est une étiquette publique du pipeline ; il sous-décrit la portée réelle. Modification de **commentaire/label uniquement**, pas de logique. |

### Décision à instruire séparément (hors écriture immédiate)
| Fichier | Point | Pourquoi ce n'est pas un simple correctif |
|---|---|---|
| `…/ci/registres_entites.yaml` | Lever la **contradiction prose vs champs** (PARTIELLE/WARNING vs complet/bloquant) | Artefact **souverain**. Aligner la prose sur les champs (ou l'inverse) **change le sens d'un contrat exécutable** : c'est une **décision** (quel état fait foi ?), pas une coquille. À trancher par l'auteur avant toute édition. D1 **identifie** la contradiction ; il ne la résout pas unilatéralement. |

### Hors périmètre D1 (rappel)
- Ne pas modifier `CONFIGS`, les règles, `ARSENAL_CI_ENFORCE`, ni aucune logique de validation.
- Ne pas « compléter » la couverture : D1 documente l'existant, il ne l'étend pas.

---

## 6. Opposabilité et limites

- **Opposabilité** : chaque inexactitude du §4 est ancrée sur le contenu réel des fichiers au HEAD `899c172` (chemin `packages/` absent ; job `execution` présent ; champs registre vs prose). Vérifiable par relecture directe.
- **Limite 1** : le titre « étage 1 » du `README` et « VERSION PARTIELLE » du registre peuvent être des **vestiges** d'un état antérieur ; je constate la contradiction au HEAD courant sans présumer la date de dérive.
- **Limite 2** : la résolution de la contradiction du registre dépend d'une intention (quel état est vrai aujourd'hui ?) que seul l'auteur détient. D1 ne doit pas la trancher.
- **Limite 3** : ce cadrage suppose que les étages 2/3 fonctionnent comme leurs commentaires et points d'entrée l'indiquent ; je n'ai pas exécuté `cli_decision`/`cli_execution` (seul le self-test, 136 tests, a été lancé).
- **Aucune écriture effectuée.** Ce document prépare le chantier ; il ne le réalise pas.

---

*Fin du rapport préparatoire. Lecture seule, sans patch.*
