# 🧭 ARSENAL — DOCTRINE SYSTÈME · Restauration d'état des helpers et usage de la clé `initial`

---

## 📌 Statut

- Doctrine système transverse Arsenal.
- **NORMATIF et OPPOSABLE** dès sa création.
- Applicabilité globale (tous domaines, toutes versions).
- Version : **v1.0** — création 2026-07-01.

Ce contrat est opposable **tout en mentionnant des écarts connus** (cf. §Écarts
connus) à corriger dans un lot séparé. La présence d'écarts n'affaiblit pas
l'opposabilité de la doctrine ; elle la trace.

---

## 🎯 Portée

Tous les helpers YAML Arsenal exposant une clé `initial` :

- `input_number`
- `input_text`
- `input_datetime`
- `input_select`
- `input_boolean`
- `counter`

Les `counter` sont **inclus dans le périmètre** mais soumis à un **régime
distinct** (cf. §Règles spécifiques par type de helper).

---

## 🔗 Référence audit source

Ce contrat est adossé au rapport d'audit préparatoire **non opposable** :

- [`audits/01_rapports/transverses/audit_initial_helpers.md`](../../audits/01_rapports/transverses/audit_initial_helpers.md) (PR #198)

L'audit recense 19 occurrences de `initial`, établit le mécanisme du piège, et
documente la chronologie des correctifs. Le présent document en fait une norme.

---

## 🎯 Objectif

Empêcher que la clé `initial` **désactive silencieusement la restauration d'état
de Home Assistant** et **reforce** une valeur à chaque redémarrage, écrasant un
réglage opérateur, une intention persistante, un override ou un verrou.

---

## 🧠 Principe fondamental — Invariant principal

> **INV-INIT — Primauté de la restauration.**
> Sur les helpers `input_*`, l'état restauré par Home Assistant au redémarrage
> est la **VÉRITÉ PAR DÉFAUT**. La clé `initial` désactive cette restauration et
> reforce la valeur à chaque démarrage. Elle est **INTERDITE** sur tout helper
> portant un réglage opérateur, une intention persistante, un override ou un
> verrou, et n'est **AUTORISÉE** que pour un démarrage à valeur figée
> explicitement voulu, **déclaré et justifié in-file**.

**Asymétrie fondatrice** : sur les helpers `input_*`, `initial` **ressemble** à
une « valeur par défaut » mais **agit** comme un écrasement au reboot. Sur
`counter`, la mécanique est différente : `initial` est la valeur de reset et la
persistance est gouvernée par `restore`.

---

## 📖 Définitions

- **Paramètre réglable** — helper dont la valeur est ajustée par l'opérateur
  (seuil, durée, borne, coefficient).
- **Intention persistante / override / verrou** — helper (souvent `input_boolean`
  ou `input_select`) portant un choix devant **survivre au reboot**.
- **Sentinelle cold-start** — valeur neutre **voulue** au démarrage d'un pipeline
  (mémoire de filtre, état S(t-1)).
- **État transactionnel** — marqueur éphémère devant **repartir au neutre** à
  chaque cycle ou reboot.
- **Sentinelle « jamais »** — valeur-repère d'absence d'événement (ex.
  `1970-01-01`).
- **Booléen technique réinitialisé au boot** — `input_boolean` interne dont le
  démarrage figé (généralement `off`) est un besoin technique explicite, et qui
  **ne porte aucune intention/override/verrou**.
- **config-seed** — amorçage d'une valeur de configuration, éventuellement issue
  de `!secret`.

---

## ✅ Règles normatives obligatoires

> **Lecture des règles.** Chaque règle énonce d'abord la **conformité
> contractuelle** (obligation opposable), puis la **sévérité CI transitoire**
> (comportement du futur checker pendant la migration). Les deux niveaux sont
> **distincts** : une règle peut être obligatoire contractuellement alors que la
> première CI la signale seulement en WARN le temps de la migration. La sévérité
> CI transitoire **n'affaiblit pas** l'obligation contractuelle.

### R01 — `initial` interdit sur `input_*` *paramètre réglable*

`initial` est **interdit** sur `input_number`, `input_text`, `input_datetime`,
`input_select` de nature *paramètre réglable*.

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI transitoire :** cette règle est obligatoire contractuellement.
  La CI peut toutefois la signaler en **WARN** pendant la phase de migration,
  puis basculer en **ERROR** une fois les `initial` légitimes tagués (R03) et
  les écarts connus traités.

### R02 — `initial` interdit sur `input_boolean` d'intention/override/verrou

`initial` est **interdit** sur tout `input_boolean` représentant une intention
persistante, un override ou un verrou — **sans exception**. Sur les autres
`input_boolean`, `initial` est interdit par défaut et **toléré uniquement** sous
l'exception « booléen technique réinitialisé au boot » (cf. §Exceptions), avec
marqueur `initial VOULU`.

- **Conformité contractuelle :** obligatoire ; interdiction **dure** (sans
  exception) sur intention/override/verrou.
- **Sévérité CI transitoire :** cette règle est obligatoire contractuellement.
  Aucune occurrence n'existe aujourd'hui (coût de migration nul) : la CI peut la
  signaler en **ERROR dès la première version**. Un palier **WARN** initial reste
  acceptable si l'on souhaite un déploiement homogène avec les autres règles.

### R03 — Marqueur obligatoire pour tout `initial` conservé

Tout `initial` conservé (autorisé par exception ou régime counter) **doit** porter
le marqueur `# initial VOULU — <catégorie>` (cf. §Format de justification).

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI transitoire :** cette règle est obligatoire contractuellement.
  La CI la signale en **WARN documentaire** (elle vise la traçabilité, pas le
  blocage).

### R04 — Repli de lecture après retrait d'un `initial`

Le retrait d'un `initial` sur un paramètre réglable **doit** s'accompagner d'un
**repli de lecture** côté consommateur (ex. `float(<défaut>)`, `| default(...)`),
afin qu'aucune logique ne dépende d'un état `unknown` au premier démarrage.

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI transitoire :** cette règle est obligatoire contractuellement.
  Sa vérification statique est **partielle** (elle porte sur les consommateurs,
  hors du helper) : la CI la signale en **WARN** au mieux, la revue humaine reste
  nécessaire.

### R05 — `counter` : `initial` autorisé, `restore` explicite

Sur `counter`, `initial` est **autorisé** en tant que valeur de reset. La clé
`restore:` **doit être explicite** (le danger éventuel est porté par `restore`,
pas par `initial`).

- **Conformité contractuelle :** obligatoire (explicitation de `restore`).
- **Sévérité CI transitoire :** cette règle est obligatoire contractuellement.
  La CI la signale en **INFO** (régime distinct, danger moindre).

---

## 🔓 Exceptions autorisées

`initial` est autorisé **uniquement** dans les catégories suivantes, et
**seulement** sous couvert du marqueur `initial VOULU` (R03) :

- **sentinelle-cold-start** — ex. `temperature_jardin_etat_publie` (`initial: -20`).
- **transactionnel** — ex. `ecs_cycle_last_action_status` (`initial: ""`),
  `…request_id…` (`initial: ""`), `transactions_bots` (`initial: none`).
- **sentinelle-jamais** — ex. `palmares_pluie_journalier`
  (`initial: "1970-01-01 00:00:00"`).
- **compteur** — `counter` (R05).
- **booleen-technique-reset** — `input_boolean` interne réinitialisé au boot,
  sans intention/override/verrou (R02).
- **config-seed** — **catégorie non tranchée** (cf. §Décisions ouvertes) : ne pas
  déclarer conforme, ne pas déclarer interdit.

---

## ⛔ Cas interdits

- `initial` comme pseudo-« valeur par défaut » d'un paramètre réglable (écrase la
  calibration opérateur au reboot).
- `initial` sur une intention persistante, un override ou un verrou.
- `initial` conservé **sans** marqueur `initial VOULU`.
- Sur `counter` : `restore:` implicite (non déclaré).

---

## 🏷️ Format de justification `initial VOULU`

Tout `initial` conservé porte, dans le bloc de commentaire du helper, le marqueur
suivant. La **première ligne est machine-lisible** ; `<catégorie>` appartient au
vocabulaire clos ci-dessous.

```yaml
# initial VOULU — <catégorie>
# Raison : <pourquoi un démarrage à valeur figée est nécessaire>
# Restauration HA volontairement désactivée : oui
```

**Vocabulaire clos des catégories :**
`sentinelle-cold-start` | `transactionnel` | `sentinelle-jamais` | `compteur` |
`booleen-technique-reset` | `config-seed` *(à arbitrer)*.

La catégorie `parametre-reglable` **n'existe pas** comme justification : ce cas
est interdit (R01), pas justifiable.

---

## 🧩 Règles spécifiques par type de helper

| Type | Régime | Règles applicables |
|---|---|---|
| `input_number` | `initial` = exception justifiée | R01, R03, R04 |
| `input_text` | `initial` = exception justifiée | R01, R03, R04 |
| `input_datetime` | `initial` = exception justifiée | R01, R03, R04 |
| `input_select` | `initial` = exception justifiée | R01, R03, R04 |
| `input_boolean` | interdit sur intention/override/verrou (dur) ; exception technique-reset | R02, R03 |
| `counter` | `initial` autorisé (reset) ; `restore` explicite | R05, R03 |

---

## 🧾 Écarts connus à la date de création (2026-07-01)

Ces occurrences sont **présumées non conformes** et **inscrites comme écarts
connus, à traiter dans un lot séparé**. Elles ne sont **pas corrigées** par le
présent lot. Leur existence ne remet pas en cause l'opposabilité du contrat.

| Entité | Fichier | Écart présumé |
|---|---|---|
| `arrosage_fenetre_debut` | `07_input_datetimes/arrosage/fenetre.yaml` | `initial` sur borne « réglable par l'opérateur » (R01) |
| `arrosage_fenetre_fin` | `07_input_datetimes/arrosage/fenetre.yaml` | `initial` sur borne « réglable par l'opérateur » (R01) |
| `arsenal_self_audit_stale_threshold_hours` | `03_input_numbers/system/audit_stale_threshold_hours.yaml` | `initial` sur « paramètre humain modifiable depuis l'UI » (R01) |

---

## ❓ Décisions ouvertes

- **config-seed — badges / code alarme.** Les helpers
  `04_input_texts/alarme/badges.yaml` et `04_input_texts/alarme/code.yaml`
  (seed via valeur littérale et via `!secret`) restent en catégorie **`config-seed`
  à arbitrer** : ils **ne sont pas déclarés conformes**, **ni interdits**. La
  décision dépend d'un fait à établir : **ces helpers sont-ils édités via l'UI ?**
  Si oui, `initial` réécrase l'édition au reboot (interdit R01) ; si non (pur
  seed de configuration), tolérable sous justification. → **décision ouverte**,
  hors périmètre de ce lot.

---

## 🔗 Articulation avec la future CI

- La CI n'existe **pas encore** ; ce contrat ne la crée pas.
- Checker envisagé : `scripts/arsenal_contracts/check_initial_key_contracts.py` ;
  workflow dédié `contracts_initial_key.yml` (sur `push` + `pull_request`).
- **La CI lit le marqueur `initial VOULU` comme source de vérité, PAS la prose
  `NATURE`** des en-têtes. Test central : `initial` présent ⇒ marqueur valide
  requis ⇒ sinon signalé.
- Migration : Phase 1 CI en **WARN** (inventaire) → Phase 2 tag des `initial`
  légitimes (R03) → Phase 3 traitement des écarts connus → Phase 4 bascule
  **ERROR** (R02 dès v1 possible ; R01 après Phases 2–3).
- La ligne de routage dans `00_documentation_arsenal/README.md` sera ajoutée en
  Phase 1, **avec** le gate CI correspondant (la table de routage exige une
  colonne « Gate » remplie).

---

## 🔍 Limites de la vérification statique

- La CI vérifie une **déclaration**, pas une **intention** : elle ne peut établir
  ni la vraie nature d'un helper, ni le chemin d'édition UI, ni la véracité de la
  catégorie déclarée dans le marqueur.
- Un `initial` **mal catégorisé** (ex. un réglable tagué `sentinelle-cold-start`)
  **passe la CI** : c'est un faux négatif structurel, relevant de la **revue
  humaine**, irremplaçable.
- Faux positifs transitoires attendus : `initial` légitimes non encore tagués
  (résorbés par R03 en Phase 2).

---

## 🕰️ Historique / justification

Ce contrat est adossé à des faits opposables établis par l'audit #198 :

- **Mécanisme** : sur `input_*`, `initial` désactive la restauration HA et reforce
  la valeur au reboot.
- **Épisodes correctifs** (retrait de `initial` sur paramètres réglables) :
  - `89a0087` (2026-06-17) — fix(deshumidificateur): preserve user RH thresholds.
  - `2985696` (2026-06-30) — fix(arrosage): durée station 1, retrait du `initial`.
  - `6027097` (2026-06-30) — fix(arrosage): retrait des `initial` sur décision V1 et seuils pluie.
  - `f011851` (2026-06-30) — fix(meteo): retrait des `initial` sur paramètres réglables.
- **Rationale déjà standardisée** dans le dépôt :
  > ⚠️ PAS de clé `initial` : elle désactive la restauration HA et reforcerait le
  > réglage opérateur. Sans `initial`, HA restaure la dernière valeur réglée.

---

## 📌 Statut d'opposabilité

- Document d'architecture Arsenal, **normatif et opposable**, applicabilité
  globale (tous domaines).
- Positionné dans la couche doctrinale (`architecture/03_doctrines/`), entre les
  contrats fonctionnels et les documents d'architecture domaine.
- Opposable **malgré** les écarts connus listés, qui sont tracés et renvoyés à un
  lot correctif ultérieur.
- Stable, modifié uniquement lors d'évolutions doctrinales, versionné
  explicitement.

# ==========================================================
