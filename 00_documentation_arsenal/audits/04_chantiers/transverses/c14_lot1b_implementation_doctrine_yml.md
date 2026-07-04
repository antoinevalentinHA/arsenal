# C14 — Lot 1B-implémentation : durcissement de `doctrine.yml`

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md), suite de l'arbitrage [Lot 1B](c14_lot1b_qualification_doctrine_yml.md)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `14b85ae` (post-#264, Lot 1B qualification)
- **Périmètre modifié :** `.github/workflows/doctrine.yml` **uniquement** (+ ce rapport + index + registre)
- **Nature :** aligne le contrôle sur les invariants **déjà confirmés** au Lot 1B ; ne crée ni ne modifie aucune doctrine métier

---

## 1. Objet

Appliquer les trois corrections d'implémentation cadrées par l'arbitrage Lot 1B, sur le seul workflow `doctrine.yml` :

1. durcir le contrôle `mode:` pour qu'il porte au niveau **automation** (et non fichier) ;
2. supprimer le **placeholder mort** `default_entity_id` ;
3. nettoyer le **scope mort** `11_template_sensors/` du contrôle `platform: template`.

Ce lot **modifie la logique CI** — mais seulement pour aligner le contrôle sur des invariants écrits déjà validés, sans introduire de règle nouvelle ni imposer de valeur de mode.

## 2. Corrections appliquées

| Correction | Source normative | Fichier modifié | Comportement CI modifié ? | Commentaire |
|---|---|---|---|---|
| `mode:` par automation | `00_structure_includes/11_automations.md` §Modes | `.github/workflows/doctrine.yml` | **Oui — durcissement volontaire** (faux négatif supprimé) | parse YAML ; une garde par automation |
| Suppression placeholder `default_entity_id` | *aucune (non normatif)* | `.github/workflows/doctrine.yml` | Non (bloc déjà sans code) | retrait d'un commentaire mort, pas de contrôle retiré |
| Nettoyage scope `platform: template` | `00_structure_includes/12_template_sensors.md` §Invariants | `.github/workflows/doctrine.yml` | Non (règle inchangée, scope réduit au dossier vivant) | `11_template_sensors/` (inexistant) retiré |

> Une étape `Install PyYAML` (patron identique à `contracts_automation_ids.yml`) est ajoutée : le contrôle `mode:` durci parse désormais le YAML.

## 3. Contrôle `mode:` par automation

- **Ancienne logique (niveau fichier) :** pour chaque `*.yaml`, si la sous-chaîne `- id:` est présente **et** que la sous-chaîne `mode:` est absente du **fichier entier** → échec. Faux négatif : un fichier multi-automations où **une seule** automation porte `mode:` passe, même si d'autres n'en ont pas ; une occurrence de `mode:` en donnée de service peut masquer une absence réelle.
- **Nouvelle logique (niveau automation) :** chargement YAML tolérant (tags HA `!…` neutralisés) ; chaque fichier est normalisé en **liste d'items** ; pour **chaque** item portant une clé `id`, la clé `mode` doit être présente. Message d'erreur exploitable : `<fichier> : automation id=<id> sans cle 'mode:'`. La **valeur** du mode n'est pas contrôlée (aucun mode imposé dans ce lot). Contrôle **bloquant** (exit 1).
- **Faux négatif supprimé :** démontré — un fichier multi-automations `[conforme + sans mode]` **passait** l'ancien contrôle et **échoue** désormais, en pointant l'automation fautive.
- **Résultat sur corpus réel :** `11_automations/` = 258 fichiers, 257 automations. Le contrôle durci s'exécute → **exit 0** (aucune régression). Le corpus étant à 1 automation/fichier, la garantie est désormais portée par le contrôle lui-même et non plus par la convention.

## 4. Placeholder `default_entity_id`

- **Statut :** non normatif (aucune clause écrite ; vestige d'une migration inachevée ; usages contractuels subsistants — cf. rapport de qualification Lot 1B).
- **Action :** le bloc de commentaire mort est **supprimé** de `doctrine.yml`.
- **Absence de remplacement :** aucun contrôle n'est introduit à sa place. Une éventuelle migration `default_entity_id` reste un **sujet séparé** (hors périmètre), non promis par ce workflow.

## 5. Scope `platform: template`

- **Suppression du chemin mort :** `11_template_sensors/` (répertoire inexistant) est retiré du `grep`.
- **Maintien du contrôle vivant :** le contrôle reste **bloquant** sur `12_template_sensors/` (le dossier réel, adossé à l'invariant `12_template_sensors.md`). La règle elle-même est inchangée.
- **Résultat sur corpus réel :** aucun `platform: template` présent dans `12_template_sensors/` → **exit 0**.

## 6. Tests / validations

- **Syntaxe YAML du workflow :** `yaml.safe_load` OK ; 4 étapes reconnues (`Checkout`, `Install PyYAML`, `Check forbidden legacy template platform`, `Check automations without mode`).
- **Tests négatifs du nouveau contrôle `mode:`** (script embarqué **extrait du workflow** et exécuté tel quel) :
  - automation `id` + `mode` → **exit 0** ;
  - automation `id` sans `mode` → **exit 1** (fichier + id) ;
  - fichier sans automation (pas d'`id`) → **exit 0** ;
  - fichier multi-automations (1 conforme + 1 sans `mode`) → **exit 1**, ciblage de l'automation fautive.
- **Exécution sur corpus réel :** contrôle `mode:` durci → exit 0 ; contrôle `platform: template` (scope nettoyé) → exit 0.
- **Docs lint** (`docs_lint.py` + gates DOC-CI-1/2/3/5/6) : verts.
- **Checker registre chantiers** (`check_registre_chantiers.py`) : vert.

## 7. Résiduel (hors périmètre de ce lot)

- **Chargement HA** (P0) — non traité.
- **Frontière git / sécurité publication** (P1) — non traité.
- **Normalisation future des modes autorisés** : ce lot n'impose aucune valeur de mode ; un durcissement ultérieur pourrait valider `mode ∈ {single, restart, queued, parallel}` — décision séparée, non engagée ici.
- **Migration `default_entity_id`** : à ouvrir en lot dédié si jugée nécessaire.
- **Autres lots C14** : enforcement moteur chauffage, CI anti-dérive du registre de couverture, doctrines transverses (causalité métier, gestion du temps), domaines nus (arrosage).

## 8. Conclusion

Les trois corrections cadrées sont appliquées sur le seul `doctrine.yml`, sans toucher au runtime, aux contrats, aux ID ni à la doctrine métier. Le contrôle `mode:` est désormais **robuste au niveau automation** (faux négatif supprimé, prouvé), le placeholder mort est retiré, et le scope `platform: template` est réduit au dossier vivant. Le corpus réel reste vert.

Le **Lot 1B-implémentation est clos** sous réserve de confirmation par la CI GitHub. Il n'ouvre aucune dette nouvelle ; les suites listées au §7 sont des lots distincts.
