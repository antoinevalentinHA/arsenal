# Contrat opérationnel — `retention_manager` NAS Arsenal

## Identification

- **Brique** : `retention_manager`
- **Version contrat** : 2.1
- **Version script** : 2.1
- **Statut** : runtime opérationnel
- **Mode défaut** : dry-run strict
- **Référence stratégique** : *Évolution future — Gestion de rétention patrimoniale NAS Arsenal*

---

## 1. Objet

Analyser les artefacts patrimoniaux d'un dossier NAS Arsenal et produire
un rapport de rétention. Sous flag explicite `--apply`, déplacer vers une
zone de quarantine les sauvegardes automatiques hors top N.

Cette brique **n'est pas** un moteur de suppression.

---

## 2. Doctrine asymétrique

Quatre catégories d'artefacts, traitées différemment :

| Catégorie | Origine | Politique |
|---|---|---|
| Patrimoine | `Arsenal v*` | `KEEP_MAJOR` — jamais touché |
| Critiques | nom contenant `changelog`, `contrat`, `migration`, `audit`, `rupture` | `KEEP_CRITICAL` — jamais touché |
| Runtime | `Automatic_backup*` | rotation par count (top N) |
| Reste | tout le reste | politique temporelle informative uniquement |

---

## 3. Invariant dur

> Toute sauvegarde dont le nom métier commence par `Arsenal v`
> est classée `KEEP_MAJOR` **avant toute autre règle**.
>
> Elle ne peut être déplacée, supprimée, compressée, ni reclassée.

Ce verrou est inconditionnel et non paramétrable.

---

## 4. Ordre doctrinal d'évaluation

```text
1. Invariants nominaux patrimoniaux  → KEEP_MAJOR
2. Artefacts critiques nominaux      → KEEP_CRITICAL
3. Sauvegardes automatiques          → KEEP_AUTOMATIC_RECENT
                                     → QUARANTINE_AUTOMATIC_OLD
4. Politique temporelle (résidu)     → KEEP_RECENT
                                     → KEEP_DAILY
                                     → KEEP_WEEKLY
                                     → CANDIDATE_DELETE
```

Une décision prise à un niveau supérieur n'est jamais rééxaminée par
un niveau inférieur.

---

## 5. Décisions produites

| Décision | Sens métier | Action V2.1 |
|---|---|---|
| `KEEP_MAJOR` | jalon patrimonial Arsenal | aucune |
| `KEEP_CRITICAL` | artefact critique nominal | aucune |
| `KEEP_AUTOMATIC_RECENT` | dans le top N des Automatic | aucune |
| `QUARANTINE_AUTOMATIC_OLD` | hors top N des Automatic | move (sous `--apply`) |
| `KEEP_RECENT` | fenêtre `keep_all_days` | aucune |
| `KEEP_DAILY` | slot quotidien occupé | aucune |
| `KEEP_WEEKLY` | slot hebdomadaire occupé | aucune |
| `CANDIDATE_DELETE` | hors politique temporelle | aucune |

Seul `QUARANTINE_AUTOMATIC_OLD` déclenche une action effective.
Toutes les autres décisions sont **purement informatives** en V2.1.

---

## 6. Périmètre effectif V2.1

### 6.1 Move effectif

```text
MOVE EFFECTIF :
  - décision == QUARANTINE_AUTOMATIC_OLD
  - flag --apply présent
  - quarantine_only_automatic_backups == true (YAML)
```

Les trois conditions doivent être réunies. Manque l'une → pas de move.

### 6.2 Move interdit

```text
MOVE INTERDIT (V2.1) :
  - Arsenal v*                 (KEEP_MAJOR)
  - artefacts critiques        (KEEP_CRITICAL)
  - tout artefact temporel     (KEEP_RECENT, KEEP_DAILY,
                                KEEP_WEEKLY, CANDIDATE_DELETE)
```

Ces catégories ne sont **jamais** déplacées par cette brique, quel que
soit le contenu du YAML, quel que soit l'argument CLI.

---

## 7. Quarantine ≠ suppression

> **La quarantine est un déplacement logique, pas une suppression.**

Aucune destruction de données n'est effectuée par `retention_manager`.

Un artefact en `QUARANTINE_AUTOMATIC_OLD` qui a été déplacé sous `--apply` :

- existe toujours sur le NAS ;
- est lisible ;
- est restaurable par simple `mv` ;
- conserve son nom et sa structure interne.

Il a simplement quitté le dossier de production.

La suppression réelle relève d'une brique séparée, hors périmètre :
`quarantine_purger` (à venir).

---

## 8. Schéma doctrinal du flux

```text
versions/
    │
    ▼
┌──────────────────────┐
│  retention_manager   │   ← analyse + classification
│        V2.1          │   ← move (sous --apply)
└──────────────────────┘
    │
    ▼
_quarantine/YYYY-MM-DD/
    │
    ▼
┌──────────────────────┐
│  quarantine_purger   │   ← brique future séparée
│       (futur)        │   ← purge différée
└──────────────────────┘
    │
    ▼
destruction réelle
```

Séparation des responsabilités stricte :

```text
retention_manager  ≠  quarantine_purger
classification     ≠  destruction
```

---

## 9. Modes d'exécution

### 9.1 Mode dry-run (défaut)

```bash
python3 retention_manager.py \
  --root <dir> \
  --policy <yaml> \
  --report <md>
```

- **Aucune modification du système de fichiers.**
- Le rapport contient les `move_planned` mais aucun `move_done`.
- Convient à toute exécution exploratoire, audit, vérification.

### 9.2 Mode apply

```bash
python3 retention_manager.py \
  --root <dir> \
  --policy <yaml> \
  --report <md> \
  --apply
```

- Les artefacts éligibles sont déplacés vers `_quarantine/YYYY-MM-DD/`.
- Le flag `--apply` est **obligatoire** pour tout move.
- Sans ce flag, la brique est strictement non destructive.

Convention d'exploitation : le `--apply` ne doit être ajouté qu'**après**
lecture du rapport dry-run du même run.

---

## 10. Configuration YAML (`retention_policy.yaml`)

### 10.1 Clés actives V2.1

| Clé | Type | Rôle |
|---|---|---|
| `protected_name_prefixes` | `list[str]` | Préfixes nominaux → `KEEP_MAJOR` |
| `critical_name_patterns` | `list[str]` | Sous-chaînes nominales → `KEEP_CRITICAL` |
| `automatic_backup_prefixes` | `list[str]` | Préfixes runtime → catégorie automatic |
| `automatic_backup_keep_count` | `int` | N pour le top N (défaut : 10) |
| `quarantine_dir` | `str` | Chemin quarantine (relatif à `--root` ou absolu) |
| `quarantine_only_automatic_backups` | `bool` | Garde-fou actif (doit valoir `true`) |
| `retention.keep_all_days` | `int` | Fenêtre `KEEP_RECENT` |
| `retention.keep_daily_days` | `int` | Fenêtre `KEEP_DAILY` |
| `retention.keep_weekly_days` | `int` | Fenêtre `KEEP_WEEKLY` |

### 10.2 Garde-fou bloquant

```yaml
quarantine_only_automatic_backups: true
```

Toute valeur autre que `true` strict (ex : `false`, `"false"`, `null`,
clé absente) **bloque tout move** avec erreur tracée :

```text
quarantine_only_automatic_backups_must_be_true_in_v2
```

C'est volontaire. L'élargissement du périmètre quarantine devra faire
l'objet d'une révision contractuelle (V3) — pas d'un changement de YAML.

---

## 11. Datation des artefacts

Pour chaque artefact, deux sources de date possibles :

1. **`name`** : date extraite du nom de fichier via regex
   - patterns acceptés : `YYYY-MM-DD`, `YYYYMMDD`
2. **`mtime`** : fallback sur la date de modification du fichier
   - utilisé si aucun pattern ne match
   - utilisé si le pattern match mais que la date est invalide

La source est tracée explicitement dans le rapport (colonne `Source date`).
Les classifications basées sur `mtime` sont fragiles (sensibles aux
restaurations, `touch`, `rsync`) et doivent être surveillées en audit.

---

## 12. Parsing du nom métier

Format attendu :

```text
<date>_<heure>_<nom_metier>_<hash>
```

Exemple :

```text
2026-05-06_17-40_Arsenal_v14_77358a2b
                  ↑ nom métier extrait : Arsenal_v14
```

Algorithme : `split("_")` puis `parts[2:-1]` joint par `_`.

Si le nom n'a pas la structure attendue (moins de 5 segments), le nom
complet est utilisé comme nom métier — fallback permissif.

Le nom métier est ensuite normalisé (`_` → ` `) pour les tests de
préfixe patrimonial.

---

## 13. Scan

- **Plat uniquement** : seuls les enfants directs de `--root` sont vus.
- Aucune récursivité.
- Le dossier `quarantine_dir` est **exclu** du scan (anti-récursion).
- Tri alphabétique stable.

---

## 14. Rapport produit

Format Markdown. Contient :

- en-tête (date, version, mode, quarantine, garde-fous)
- synthèse par décision (compteurs)
- synthèse quarantine (planifiés / effectués / en erreur)
- détail tabulaire (décision, date, source date, nom, raison, move)

Le rapport est l'unique sortie observable de la brique.

---

## 15. Limitations volontaires V2.1

`retention_manager` V2.1 **ne fait pas** :

- aucune suppression réelle (jamais) ;
- aucune compression d'aucune sorte ;
- aucune rotation temporelle destructive ;
- aucun move hors `QUARANTINE_AUTOMATIC_OLD` ;
- aucune action sans `--apply` ;
- aucune traversée récursive ;
- aucune action sur la quarantine elle-même ;
- aucune purge des fichiers déjà en quarantine ;
- aucune notification, aucun side effect réseau.

Ces limitations sont des **choix doctrinaux**, pas des dettes.

---

## 16. Évolutions hors périmètre

Évolutions **non couvertes** par ce contrat :

- purge différée des fichiers en quarantine → `quarantine_purger`
- compression d'archives anciennes
- rotation destructive des artefacts temporels
- traversée multi-dossiers
- politique de rétention patrimoniale long terme

Ces sujets relèvent du document stratégique référencé en en-tête.

---

## 17. Invariants de validation

Une exécution est **conforme** si et seulement si :

1. Tous les `Arsenal v*` sont en `KEEP_MAJOR` dans le rapport ;
2. Aucun `KEEP_MAJOR` n'a `move_planned == True` ;
3. Aucun `KEEP_CRITICAL` n'a `move_planned == True` ;
4. Aucun `KEEP_*` temporel n'a `move_planned == True` ;
5. Tous les `move_planned == True` sont des `QUARANTINE_AUTOMATIC_OLD` ;
6. En dry-run, aucun `move_done == True` n'apparaît ;
7. En apply, `move_done` ou `move_error` est positionné pour chaque
   `move_planned == True`.

Ces invariants sont vérifiables par lecture du rapport seul.
