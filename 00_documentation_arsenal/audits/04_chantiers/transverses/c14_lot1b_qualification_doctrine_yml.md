# C14 — Lot 1B : qualification normative de `doctrine.yml`

- **Type :** lot d'**arbitrage** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md) — qualification, pas implémentation lourde
- **Statut :** rapport livré ; ancrage documentaire (commentaires) appliqué ; durcissements **proposés, non appliqués** (en attente d'arbitrage)
- **Base :** `main` @ `84108c3` (post-#263, Lot 1A)
- **Périmètre modifié :** `.github/workflows/doctrine.yml` (**commentaires uniquement**, logique inchangée) + ce rapport + index + registre

---

## 1. Objet du lot

`doctrine.yml` était, à l'issue du Lot 1A, le **seul** cas de règle CI sans clause normative écrite clairement identifiée. Ce lot qualifie le **statut normatif réel** de ses contrôles — sans présumer qu'une règle est normative parce qu'un contrôle existe.

**Principe C14 appliqué :** *la norme précède le contrôle, pas l'inverse.* Le but n'est pas de fabriquer une doctrine pour sauver un contrôle, mais de décider, pour chaque règle, si elle doit **suivre une norme, être corrigée, être affaiblie, ou être supprimée**. Chaque source a été **ouverte et lue** (principe méthodologique C14), pas devinée à partir d'un nom.

## 2. État actuel du workflow

`doctrine.yml` porte **deux contrôles actifs** et **un placeholder désactivé** (aucun script externe ; tout est inline). Déclencheurs : `push` + `pull_request`, sans filtre `paths`.

| Contrôle | Périmètre | Méthode actuelle | Bloquant ? | Source normative trouvée ? | Défaut connu |
|---|---|---|---|---|---|
| `platform: template` interdit | `11_template_sensors/` (inexistant) + `12_template_sensors/`, `*.yaml` | `grep -R "platform: template"` → `exit 1` si trouvé | **Oui** | **Oui** — `00_structure_includes/12_template_sensors.md` §Invariants | scope vise un dossier inexistant (`11_template_sensors/`) — bruit, sans impact fonctionnel |
| `mode:` requis sur automations | `11_automations/**/*.yaml` | Python inline : si `- id:` présent **et** `mode:` absent **dans le fichier** → `exit 1` | **Oui** | **Oui** — `00_structure_includes/11_automations.md` §Modes | contrôle au niveau **fichier**, pas automation : faux négatif possible sur fichier multi-automations |
| `default_entity_id` | (aucun) | **aucun code** — 2 lignes de commentaire « désactivé temporairement » | Non | **Non** | placeholder mort ; migration inachevée ; usages contractuels subsistants |

## 3. Analyse normative — `platform: template`

- **Norme écrite trouvée : OUI.** [`00_documentation_arsenal/architecture/00_structure_includes/12_template_sensors.md`](../../../architecture/00_structure_includes/12_template_sensors.md), §Invariants : « **Moteur unique : `template:`** » et « **Interdiction de `platform: template`** ». Document de structure déclaré normatif.
- **Pertinence actuelle :** élevée. Home Assistant accepte encore la forme legacy `platform: template` (sous `sensor:`) ; Arsenal impose la syntaxe moderne `template:`. La règle empêche une régression de syntaxe réelle et possible.
- **Risque couvert :** introduction d'un capteur template en syntaxe legacy — non conforme à l'invariant structurel, et divergent du gabarit canonique du domaine.
- **Recommandation : CONSERVER, bloquant, + ANCRER.** La règle est un vrai invariant Arsenal. Ancrage documentaire ajouté en commentaire du workflow (fait). Nettoyage optionnel du chemin inexistant `11_template_sensors/` : **proposé** (§7), non appliqué (modification de logique de workflow → arbitrage).

## 4. Analyse normative — `mode:`

- **Norme écrite trouvée : OUI.** [`00_documentation_arsenal/architecture/00_structure_includes/11_automations.md`](../../../architecture/00_structure_includes/11_automations.md) : §Structure attendue liste `mode:` comme clé attendue ; §« Modes Arsenal — Doctrine générale » énonce « **Le choix du `mode` fait partie du contrat comportemental de l'automatisation** » et fixe les modes autorisés (`single | restart | queued | parallel`) ; le §Modèle d'en-tête impose la rubrique « ⚙️ MODE … Justification ». L'exigence d'un `mode:` **explicite** découle directement du principe Arsenal « explicite plutôt qu'implicite » (le mode HA par défaut `single` serait un choix de contrat non déclaré).
- **Pertinence actuelle :** élevée. Le mode conditionne la concurrence/idempotence, elles-mêmes exigées par les invariants du même document.
- **Risque couvert :** automation livrée sans stratégie de concurrence déclarée (contrat comportemental implicite).
- **Défaut du contrôle actuel :** il teste la présence de la sous-chaîne `mode:` **au niveau du fichier**. Un fichier multi-automations où **une seule** automation porte `mode:` passerait, même si d'autres n'en ont pas ; et une occurrence de `mode:` dans des données de service pourrait masquer une absence réelle. **Mesure sur le corpus actuel :** 258 fichiers, **257 automations, 0 fichier multi-automations** (convention de fait « une automation par fichier »). Le contrôle fichier est donc **aujourd'hui équivalent** au contrôle par-automation — **0 faux négatif constaté** — mais la garantie repose sur la convention, pas sur le contrôle.
- **Recommandation : CONSERVER, bloquant, + ANCRER** (fait). **Durcissement par-automation : PROPOSÉ, non appliqué** (§7) — robustesse contre un futur fichier multi-automations ; priorité P2 (pas de faux négatif actuel). Ne pas durcir sans arbitrage explicite (consigne du lot).

## 5. Analyse du check `default_entity_id`

- **État actuel :** **placeholder mort**. Deux lignes de commentaire (« Désactivé temporairement / Migration legacy default_entity_id non terminée »), **aucun code**. Rien n'est vérifié.
- **Norme source éventuelle : AUCUNE.** Nulle doctrine ni contrat n'interdit `default_entity_id`. Au contraire, il subsiste des usages **contractuels assumés** (ex. `contrats/parametres_invalides.md` : `default_entity_id: binary_sensor.parametres_invalides_<domaine>`, « cohérence avec `unique_id` »).
- **Raison probable de désactivation :** une **migration** visant à retirer le `default_entity_id` legacy des **gabarits de template sensors** a été engagée (tracée en changelog `v11.1` — « suppression de `default_entity_id` du gabarit canonique sensor continu » — et `v12.1.1`), puis laissée inachevée. Le check n'a jamais été écrit ; seul le commentaire subsiste.
- **Recommandation : NE PAS réactiver dans `doctrine.yml`.** Ce n'est pas une règle de doctrine mais l'état résiduel d'une migration. **Deux options** (§7) : (a) supprimer le placeholder mort de `doctrine.yml` (nettoyage documentaire) ; (b) traiter la migration `default_entity_id` — si elle doit être menée à terme — dans un **lot séparé** dédié, sur la base d'une décision explicite. Le commentaire du workflow a été **clarifié** (fait) pour ne plus laisser croire à un contrôle en attente.

## 6. Arbitrage recommandé

| Règle | Norme écrite ? | Arbitrage |
|---|---|---|
| `platform: template` | Oui (`12_template_sensors.md`) | **Écrire/rattacher : rattachée** (ancrage fait) · **conserver le contrôle** bloquant · nettoyage de chemin *proposé* |
| `mode:` | Oui (`11_automations.md`) | **Rattachée** (ancrage fait) · **conserver** bloquant · **durcir** (par-automation) *proposé*, reporté à une PR d'implémentation |
| `default_entity_id` | Non | **Supprimer le placeholder** (nettoyage) · migration éventuelle *reportée* à un lot séparé · **ne pas** en faire une règle doctrine.yml |

Aucune règle ne relève de « écrire une clause uniquement pour sauver le checker » : les deux règles actives avaient **déjà** leur clause écrite ; elle n'était simplement pas citée. Aucune règle ne relève de « affaiblir en WARN » : les deux invariants justifient le blocage.

## 7. Proposition de traitement

### Règles à rattacher/conserver (fait dans ce lot — commentaires seuls)
- `platform: template` → commentaire d'ancrage vers `12_template_sensors.md` §Invariants ajouté.
- `mode:` → commentaire d'ancrage vers `11_automations.md` §Modes ajouté, avec mention explicite de la limite « niveau fichier ».

### Durcissements proposés (NON appliqués — nécessitent GO, PR d'implémentation séparée)
1. **`mode:` par-automation.** Remplacer le test fichier par un test par bloc (une garde par `- id:`), refusant toute automation sans clé `mode:` de niveau automation, et — option — validant que le mode ∈ {single, restart, queued, parallel}.
   - *Document normatif :* aucun à créer (clause déjà écrite) ; éventuellement préciser dans `11_automations.md` §Invariants que « tout `mode:` est explicite et ∈ {…} ».
   - *Checker :* transformer le contrôle inline en un `check_automation_mode_contracts.py` ancré (cohérent avec la famille `scripts/arsenal_contracts/`), ou durcir l'inline.
   - *Niveau de blocage :* ERROR (bloquant), comme aujourd'hui.
   - *Tests négatifs à ajouter :* automation sans `mode:` → ERROR ; fichier multi-automations dont une seule porte `mode:` → ERROR ; `mode:` de valeur hors énumération → ERROR ; `mode:` présent uniquement en donnée de service → ERROR.
2. **Nettoyage du scope `platform: template`.** Retirer le dossier inexistant `11_template_sensors/` du `grep` (le seul dossier réel est `12_template_sensors/`). Cosmétique, non bloquant.

### Règle à retirer / reclasser
3. **`default_entity_id`.** Supprimer le placeholder mort de `doctrine.yml` (nettoyage). Si la migration doit aboutir, l'ouvrir en **lot séparé** avec sa propre décision — elle touche des gabarits et des contrats, hors périmètre de `doctrine.yml`.

## 8. Conclusion

Les deux contrôles actifs de `doctrine.yml` sont **de vrais invariants Arsenal**, chacun adossé à une clause écrite existante de `00_structure_includes/` — ils n'étaient pas des « normes fantômes », seulement des règles **non citées**. Le troisième (`default_entity_id`) n'est **pas** une règle normative : c'est un vestige de migration.

Le Lot 1B est **clos par le rapport** pour sa partie *qualification* et *ancrage* (commentaires appliqués, logique inchangée). Il **appelle une PR d'implémentation séparée** — sur GO explicite — pour les deux durcissements proposés (`mode:` par-automation ; nettoyage `default_entity_id` et scope `platform: template`), qui modifient la logique du workflow et sortent donc de cette étape d'arbitrage.
