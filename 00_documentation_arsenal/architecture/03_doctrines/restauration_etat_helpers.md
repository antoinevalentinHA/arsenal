# 🧭 ARSENAL — DOCTRINE SYSTÈME · Restauration d'état des helpers et usage de la clé `initial`

---

## 📌 Statut

- Doctrine système transverse Arsenal.
- **NORMATIF et OPPOSABLE**.
- Applicabilité globale (tous domaines, toutes versions).
- Version : **v1.1** — 2026-07-01 (v1.0 : création ; v1.1 : mise en cohérence
  post-chantier — CI active et bloquante, écarts résorbés, config-seeds arbitrés).

Le chantier de résorption est **clos** : l'inventaire `initial` est propre
(0 écart) et la CI est **active et bloquante** (cf. §CI active et opposable).

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
> contractuelle** (obligation opposable), puis la **sévérité CI** appliquée par
> le checker actif (`check_initial_key_contracts.py`). La CI est **bloquante** :
> toute violation d'une obligation dure sort en ERROR (exit 1).

### R01 — `initial` interdit sur `input_*` *paramètre réglable*

`initial` est **interdit** sur `input_number`, `input_text`, `input_datetime`,
`input_select` de nature *paramètre réglable*.

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI :** **ERROR** (HINIT-001) — un `initial` sur `input_*` sans
  marqueur valide bloque la CI.

### R02 — `initial` interdit sur `input_boolean` d'intention/override/verrou

`initial` est **interdit** sur tout `input_boolean` représentant une intention
persistante, un override ou un verrou — **sans exception**. Sur les autres
`input_boolean`, `initial` est interdit par défaut et **toléré uniquement** sous
l'exception « booléen technique réinitialisé au boot » (cf. §Exceptions), avec
marqueur `initial VOULU`.

- **Conformité contractuelle :** obligatoire ; interdiction **dure** (sans
  exception) sur intention/override/verrou.
- **Sévérité CI :** **ERROR** (HINIT-002) — tout `initial` sur `input_boolean`
  bloque la CI.

### R03 — Marqueur obligatoire pour tout `initial` conservé

Tout `initial` conservé (autorisé par exception ou régime counter) **doit** porter
le marqueur `# initial VOULU — <catégorie>` (cf. §Format de justification).

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI :** **ERROR** — un `initial` conservé sans marqueur (HINIT-001)
  ou avec un marqueur de catégorie invalide (HINIT-003) bloque la CI.

### R04 — Repli de lecture après retrait d'un `initial`

Le retrait d'un `initial` sur un paramètre réglable **doit** s'accompagner d'un
**repli de lecture** côté consommateur (ex. `float(<défaut>)`, `| default(...)`),
afin qu'aucune logique ne dépende d'un état `unknown` au premier démarrage.

- **Conformité contractuelle :** obligatoire.
- **Sévérité CI :** **non instrumentée** — le repli de lecture porte sur les
  consommateurs, hors du périmètre statique du checker ; la revue humaine reste
  nécessaire.

### R05 — `counter` : `initial` autorisé, `restore` explicite

Sur `counter`, `initial` est **autorisé** en tant que valeur de reset. La clé
`restore:` **doit être explicite** (le danger éventuel est porté par `restore`,
pas par `initial`).

- **Conformité contractuelle :** obligatoire (explicitation de `restore`).
- **Sévérité CI :** **INFO** si `restore` explicite ; **WARN** (non bloquant) si
  `restore` implicite (HINIT-004 — régime distinct, danger moindre).

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
- **config-seed** — amorçage de configuration **non éditable via UI** et **non
  écrit par automation** (ex. badges/code alarme). Exception **reconnue** sous
  marqueur `config-seed` (arbitrée, cf. §Décisions tranchées).

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
`booleen-technique-reset` | `config-seed`.

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

## 🧾 Écarts connus — résorbés

Les 3 écarts identifiés à la création (v1.0) sont **corrigés** : retrait de
`initial` (la restauration HA préserve désormais la valeur réglée).

| Entité | Fichier | Résorption |
|---|---|---|
| `arrosage_fenetre_debut` | `07_input_datetimes/arrosage/fenetre.yaml` | `initial` retiré (PR #205) |
| `arrosage_fenetre_fin` | `07_input_datetimes/arrosage/fenetre.yaml` | `initial` retiré (PR #205) |
| `arsenal_self_audit_stale_threshold_hours` | `03_input_numbers/system/audit_stale_threshold_hours.yaml` | `initial` retiré (PR #205) |

Le M6 `palmares_pluie_journalier_derniere_evaluation` (sentinelle de fraîcheur
reforcée au reboot, aveuglant le watchdog `evaluation_obsolete`) a également été
corrigé — retrait de `initial` (PR #204).

---

## ✅ Décisions tranchées

- **config-seed — badges / code alarme** (PR #206). Établi : `badges_autorises`
  et `alarm_code` **ne sont pas édités via l'UI** ni écrits par automation
  (lecture seule ; source de vérité = configuration déclarative / `secrets.yaml`).
  Ce sont donc des **config-seeds légitimes** : `initial` conservé, marqué
  `initial VOULU — config-seed`. Le retrait est écarté (il casserait le
  rechargement du code/secret et de la liste de badges au démarrage).

---

## 🔗 CI active et opposable

- **Checker** : `scripts/arsenal_contracts/check_initial_key_contracts.py`.
- **Workflow** : `.github/workflows/contracts_initial_key.yml` (sur `push` +
  `pull_request`), **bloquant** (le job échoue sur sortie non nulle).
- **Routage** : ligne dédiée dans `00_documentation_arsenal/README.md`
  (gate `check_initial_key_contracts`).
- **Source de vérité** : le marqueur in-file `initial VOULU — <catégorie>`, **PAS**
  la prose `NATURE`. Test central : `initial` présent ⇒ marqueur valide requis.
- **Sévérités CI (garde-fou actif)** :

  | Règle CI | Cas | Sévérité |
  |---|---|---|
  | HINIT-001 | `input_*` avec `initial` sans marqueur | **ERROR** |
  | HINIT-002 | `input_boolean` avec `initial` | **ERROR** |
  | HINIT-003 | marqueur présent mais catégorie invalide / `parametre-reglable` | **ERROR** |
  | HINIT-004 | `counter` : `restore` explicite → INFO ; implicite → WARN | INFO / WARN |
  | HINIT-006 | config-seed : marqueur `config-seed` valide → INFO ; sinon → ERROR | INFO / **ERROR** |

- **État de l'inventaire** (post-#207) : **15 occurrences — 0 ERROR / 0 WARN /
  15 INFO**, `✅ CONTRAT INITIAL CONFORME`.

---

## 🔍 Limites de la vérification statique

- La CI vérifie une **déclaration**, pas une **intention** : elle ne peut établir
  ni la vraie nature d'un helper, ni le chemin d'édition UI, ni la véracité de la
  catégorie déclarée dans le marqueur.
- Un `initial` **mal catégorisé** (ex. un réglable tagué `sentinelle-cold-start`)
  **passe la CI** : c'est un faux négatif structurel, relevant de la **revue
  humaine**, irremplaçable.
- L'inventaire actuel est intégralement marqué ou résorbé : aucun faux positif
  résiduel. Un `initial` légitime **nouvellement** ajouté sans marqueur sera
  bloqué (ERROR) jusqu'à ce qu'il porte son marqueur `initial VOULU`.

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
- Inventaire `initial` **propre** (0 écart) et **garde-fou CI actif** contre toute
  régression (cf. §CI active et opposable).
- Stable, modifié uniquement lors d'évolutions doctrinales, versionné
  explicitement.

# ==========================================================
