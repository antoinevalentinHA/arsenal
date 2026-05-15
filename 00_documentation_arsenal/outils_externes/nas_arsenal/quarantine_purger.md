# Contrat opérationnel — `quarantine_purger` NAS Arsenal

## Identification

| Champ | Valeur |
|---|---|
| **Brique** | `quarantine_purger` |
| **Version contrat** | 1.0 |
| **Version script** | 1.0 |
| **Statut** | proposition initiale |
| **Mode défaut** | dry-run strict |
| **Brique amont** | `retention_manager` v2.1+ |
| **Périmètre** | purge différée de la quarantine NAS Arsenal |

---

## 1. Objet

`quarantine_purger` analyse la zone de quarantine produite par `retention_manager`
et produit un rapport de purge différée.

Sous flag explicite `--apply`, il supprime définitivement les dossiers de
quarantine datés dont l'âge dépasse le délai configuré.

Cette brique :

- ne classe aucun artefact ;
- ne décide jamais qu'un fichier doit entrer en quarantine ;
- ne travaille que sur des dossiers déjà isolés par `retention_manager` ;
- ne connaît pas le contenu des archives qu'elle purge.

---

## 2. Position dans la chaîne

```text
versions/
    │
    ▼
┌──────────────────────┐
│  retention_manager   │   classification + déplacement vers quarantine
└──────────────────────┘
    │
    ▼
_quarantine/YYYY-MM-DD/
    │
    ▼
┌──────────────────────┐
│  quarantine_purger   │   purge différée des dossiers expirés
└──────────────────────┘
    │
    ▼
destruction réelle
```

Séparation stricte des responsabilités :

```text
retention_manager  =  classification + isolement
quarantine_purger  =  purge différée des dossiers isolés
```

---

## 3. Invariant dur

> `quarantine_purger` ne scanne jamais le dossier de production `versions/`.

Il ne reçoit en entrée que le dossier `_quarantine/`.

Aucune option CLI, aucune clé YAML, aucune évolution mineure future
ne peut permettre à cette brique d'agir sur le dossier patrimonial de production.

Ce verrou est inconditionnel et non paramétrable.

---

## 4. Unité de purge

L'unité atomique de purge est le **dossier de quarantine daté**.

```text
_quarantine/2026-05-10/     ← unité de purge
    Automatic_backup_...
    Automatic_backup_...
```

Un dossier daté est purgé en totalité ou pas du tout.
Il n'existe pas de purge partielle d'un dossier de quarantine.

Ce choix garantit :

- atomicité maximale des opérations ;
- traçabilité batch claire ;
- zéro ambiguïté sur les dossiers partiellement traités ;
- suppression d'un seul objet FS par décision.

---

## 5. Calcul de l'âge

L'âge d'un dossier de quarantine est calculé **exclusivement** à partir
de son nom.

```text
_quarantine/2026-05-10/
             ↑
             date d'entrée en quarantine — vérité métier
```

Pattern accepté : `YYYY-MM-DD` strict.

Le `mtime` du dossier n'est **jamais** utilisé comme source de date,
ni comme fallback. Un `rsync`, un `touch`, une restauration NAS peuvent
modifier le `mtime` sans que la date d'entrée en quarantine ait changé.

Conséquence doctrinale :

```text
dossier non conforme au pattern YYYY-MM-DD
    → décision KEEP_QUARANTINE_UNDATED
    → jamais purgé automatiquement
```

Si la structure n'est pas conforme, la brique refuse l'action destructive.
Il n'existe pas de heuristique de fallback.

---

## 6. Décisions produites

| Décision | Sens métier | Action V1.0 |
|---|---|---|
| `KEEP_QUARANTINE_RECENT` | dossier daté, âge < délai configuré | aucune |
| `PURGE_QUARANTINE_EXPIRED` | dossier daté, âge ≥ délai configuré | suppression (sous `--apply`) |
| `KEEP_QUARANTINE_UNDATED` | nom non conforme à `YYYY-MM-DD` | aucune |
| `KEEP_QUARANTINE_INVALID` | structure douteuse (fichier isolé, etc.) | aucune |
| `PURGE_ERROR` | erreur lors de la suppression effective | erreur tracée |

Seul `PURGE_QUARANTINE_EXPIRED` déclenche une action effective.
Toutes les autres décisions sont **purement informatives** en V1.0.

---

## 7. Périmètre V1.0

### 7.1 Inclus

- scan plat du premier niveau de `_quarantine/`
- détection des dossiers nommés `YYYY-MM-DD`
- calcul de l'âge par nom de dossier
- décision par dossier selon le délai configuré
- rapport Markdown
- suppression récursive du dossier entier sous `--apply`

### 7.2 Exclus

- analyse du contenu des archives
- validation Home Assistant
- inspection de hash ou d'intégrité
- compression
- restauration
- notification
- décision intelligente ou scoring
- action sur `versions/`
- traversée multi-niveaux de la quarantine

---

## 8. Garde-fous bloquants

La suppression effective n'est autorisée que si **toutes** les conditions
suivantes sont réunies simultanément :

```text
1. flag --apply présent
2. allow_purge == true  (YAML)
3. décision == PURGE_QUARANTINE_EXPIRED
4. âge du dossier >= quarantine_min_age_days
5. chemin cible situé strictement sous --quarantine
```

Si une seule condition manque → aucune suppression.

Le garde-fou `allow_purge` est bloquant de la même manière que
`quarantine_only_automatic_backups` dans `retention_manager` :
toute valeur autre que `true` strict (ex : `false`, `"true"`, `null`,
clé absente) bloque tout apply avec erreur tracée :

```text
allow_purge_must_be_true_in_quarantine_purger_v1
```

L'élargissement du périmètre de purge devra faire l'objet d'une révision
contractuelle (V2) — pas d'un changement de YAML.

---

## 9. Configuration YAML (`quarantine_purger_policy.yaml`)

Ce fichier est **propre à `quarantine_purger`** et distinct de
`retention_policy.yaml`. Aucune clé n'est partagée entre les deux briques.

### 9.1 Clés actives V1.0

| Clé | Type | Rôle |
|---|---|---|
| `quarantine_min_age_days` | `int` | âge minimal (en jours) avant purge |
| `allow_purge` | `bool` | garde-fou bloquant — doit valoir `true` |

### 9.2 Exemple minimal

```yaml
quarantine_min_age_days: 30
allow_purge: true
```

---

## 10. Modes d'exécution

### 10.1 Mode dry-run (défaut)

```bash
python3 quarantine_purger.py \
  --quarantine <dir> \
  --policy <yaml> \
  --report <md>
```

- Aucune modification du système de fichiers.
- Le rapport contient les `purge_planned` mais aucun `purge_done`.
- Convient à toute exécution exploratoire, audit, vérification.

### 10.2 Mode apply

```bash
python3 quarantine_purger.py \
  --quarantine <dir> \
  --policy <yaml> \
  --report <md> \
  --apply
```

- Les dossiers expirés sont supprimés récursivement.
- Le flag `--apply` est **obligatoire** pour toute suppression.
- Sans ce flag, la brique est strictement non destructive.

Convention d'exploitation : le `--apply` ne doit être ajouté qu'**après**
lecture du rapport dry-run du même run.

---

## 11. Rapport produit

Format Markdown. Contient :

- date et heure d'exécution
- version de la brique
- mode (dry-run / apply)
- dossier quarantine analysé
- délai minimal configuré (`quarantine_min_age_days`)
- état du garde-fou `allow_purge`
- synthèse par décision (compteurs)
- nombre de suppressions planifiées
- nombre de suppressions effectuées
- nombre d'erreurs
- détail tabulaire : dossier, âge (jours), décision, purge planifiée, purge effectuée

Le rapport est l'unique sortie observable de la brique.

---

## 12. Invariants de validation

Une exécution est **conforme** si et seulement si :

1. Aucun chemin hors `_quarantine/` n'est scanné ni modifié ;
2. Aucun dossier non conforme à `YYYY-MM-DD` n'est purgé ;
3. Aucun dossier dont l'âge est inférieur à `quarantine_min_age_days` n'est purgé ;
4. En dry-run, aucune suppression effective n'a lieu ;
5. En apply, chaque `purge_planned == True` est suivi d'un `purge_done` ou `purge_error` ;
6. Si `allow_purge != true`, aucune suppression n'a lieu même avec `--apply` ;
7. Toute erreur de suppression est visible et tracée dans le rapport ;
8. Tous les `KEEP_QUARANTINE_*` ont `purge_planned == False`.

Ces invariants sont vérifiables par lecture du rapport seul.

---

## 13. Limitations volontaires V1.0

`quarantine_purger` V1.0 **ne fait pas** :

- aucune suppression sans `--apply` ;
- aucune suppression si `allow_purge != true` ;
- aucune analyse du contenu des archives supprimées ;
- aucune restauration d'artefact ;
- aucune compression ;
- aucune action sur un dossier non daté ;
- aucune action sur `versions/` ;
- aucune traversée récursive de la quarantine ;
- aucune notification, aucun side effect réseau.

Ces limitations sont des **choix doctrinaux**, pas des dettes techniques.

---

## 14. Évolutions hors périmètre V1.0

- purge par artefact individuel → hors doctrine V1, révision contractuelle majeure uniquement
- traversée multi-niveaux de la quarantine → V2
- rapport d'inventaire du contenu des dossiers expirés → V2
- compression avant purge → hors périmètre

---

## 15. Formule doctrinale

> Ce qui n'a pas été isolé par une brique amont
> ne peut pas être détruit par `quarantine_purger`.
