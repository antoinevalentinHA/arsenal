# CONTRAT — `release_diff`

## Statut

- Brique normative
- Couche : NAS Arsenal / versioning sémantique
- Dépend de : `ha_backup_timeline_extract_v2.py`, `versions/`
- Indépendante de : `ha_backup_timeline_diff.py`, `_diff/timeline/`
- Révision : intègre `state/release_diff_last_run.json` (cf. `release_diff_mqtt.md`)

---

## Objet

`release_diff` produit des diffs **sémantiques de version** à partir des snapshots Arsenal historisés dans `versions/`.

Il introduit une couche de versioning au-dessus du pipeline forensic existant, sans modifier ce dernier.

Unité de diff :

```text
release(N) ↔ release(N+1)
```

et non :

```text
backup(N) ↔ backup(N+1)
```

Le répertoire `.storage/` est exclu du patrimoine gouverné et du diff forensic.
Exception contrôlée : `.storage/core.entity_registry` peut être extrait comme runtime minimal d’audit patrimonial.
Ce fichier est présent dans `versions/` mais n’appartient pas au périmètre métier des changelogs.

La brique répond au besoin de produire un changelog Arsenal exploitable (`v14 → v15`) sans agréger manuellement une chaîne de micro-diffs techniques intermédiaires.

---

## Séparation forensic / sémantique

La brique formalise une dissociation stricte de deux couches qui coexistaient implicitement dans `_diff/` :

| Couche | Unité | Producteur | Destination |
|--------|-------|------------|-------------|
| Forensic | `backup → backup` | `ha_backup_timeline_diff.py` | `_diff/timeline/` |
| Sémantique | `release → release` | `release_diff.py` | `_diff/releases/` |

Les deux couches sont indépendantes. La couche forensic ne lit pas la couche sémantique. La couche sémantique ne lit pas la couche forensic — elle lit directement `versions/`.

---

## Invariants

Contrats durs. Toute évolution doit les préserver.

- **Source unique sémantique** : `release_diff` lit exclusivement `versions/` et `state/releases.json`. Il ne lit jamais `_diff/timeline/*.md`.
- **Aucun replay** : un diff de release est produit par comparaison directe des deux snapshots ancres. Les backups intermédiaires entre deux ancres sont strictement ignorés.
- **Régénérabilité** : `_diff/releases/` est intégralement reconstructible à partir de `versions/` + `state/releases.json`. La suppression de `_diff/releases/` n'entraîne aucune perte de patrimoine.
- **Non-destructif** : la brique n'écrit jamais en dehors de `_diff/releases/`, `state/processed_releases.json` et `state/release_diff_last_run.json`. Elle ne supprime ni ne modifie aucun fichier de `versions/`, `ha_backup_maison/`, ou `_diff/timeline/`.
- **Idempotence** : un couple `(ancre_N, ancre_N+1)` déjà traité avec `status=ok` et `sha256` identiques des deux snapshots n'est jamais retraité.
- **REJECT-not-clamp** : toute ambiguïté de détection d'ancre (doublon de nom, suffixe non reconnu, ordre incohérent) provoque un rejet explicite du couple concerné. Aucune résolution silencieuse.
- **Strictement flat sur `versions/`** : le scan d'ancres lit uniquement les noms de répertoires de premier niveau de `versions/`. Aucune descente récursive pour cette détection.

---

## Modèle d'ancre

### Format reconnu

Une **ancre de release** est un répertoire de `versions/` dont le nom contient un tag de version Arsenal correspondant exactement à l'expression :

```text
Arsenal_v(\d+)(?:\.(\d+))?(?:\.(\d+))?(?=_|$)
```

Captures :

- groupe 1 : version majeure (entier, obligatoire),
- groupe 2 : version mineure (entier, optionnel),
- groupe 3 : version patch (entier, optionnel).

L'ancre lookahead `(?=_|$)` borne le match et garantit qu'aucun composant numérique additionnel n'est silencieusement avalé. Les formes à quatre composantes ou plus (`Arsenal_v15.5.1.2`) ne matchent jamais. Les formes contenant un tiret (`Arsenal_v15-test`) ne matchent jamais.

En revanche, tout suffixe commençant par un underscore est **absorbé comme suffixe libre**, indépendamment de sa nature. `Arsenal_v15_rc1_ef98ab23` parse vers le triplet `(15, 0, 0)` et produit l'ancre `v15`, exactement comme `Arsenal_v15_77358a2b`. La brique ne maintient aucune liste de suffixes interdits (`_rc`, `_beta`, `_alpha`, etc.) : la robustesse repose sur la chaîne `parse → normalisation → collision → rejet`. Si un répertoire `Arsenal_v15_rc1_...` coexiste avec un répertoire `Arsenal_v15_...` légitime, les deux parsent vers le même triplet et le mécanisme de doublon d'ancre les rejette tous deux. Ce comportement est conforme à REJECT-not-clamp et préserve l'auditabilité sans imposer de catalogue de suffixes à maintenir.

La conséquence pratique pour l'opérateur : un répertoire de version arsenalisée porte toujours un tag stable. Tout suffixe `_xxx` qui n'est pas le hash de capture est une source potentielle de collision et doit être évité dans `versions/`. Les répertoires expérimentaux ou de pré-release qui ne doivent pas être interprétés comme des ancres restent en dehors de `versions/`.

### Exemples

| Nom de répertoire | Détecté | Ancre |
|-------------------|---------|-------|
| `2026-05-06_17-40_Arsenal_v14_77358a2b` | oui | `v14` |
| `2026-05-08_09-12_Arsenal_v14.1_abc12345` | oui | `v14.1` |
| `2026-05-11_18-30_Arsenal_v15_d4464cb6` | oui | `v15` |
| `2026-05-12_10-15_Arsenal_v15.5.1_f1caab65` | oui | `v15.5.1` |
| `2026-05-10_22-00_Arsenal_v15_rc1_ef98ab23` | oui | `v15` (suffixe absorbé, source potentielle de collision) |
| `2026-05-10_22-00_Arsenal_v15-test_xyz` | non | — |
| `2026-05-10_22-00_Arsenal_v15.5.1.2_abc` | non | — |
| `2026-05-09_11-30_backup_auto_3f7c1a2b` | non | — |

### Ordre canonique

Les ancres sont triées par tuple `(majeur, mineur, patch)` avec `mineur = 0` et `patch = 0` si absents.

```text
v14 < v14.1 < v14.2 < v15 < v15.1 < v15.5 < v15.5.1 < v15.6 < v16
```

L'ancre lisible est rendue sous sa forme minimale : `v15` pour `(15, 0, 0)`, `v15.5` pour `(15, 5, 0)`, `v15.5.1` pour `(15, 5, 1)`. La forme lisible ne révèle jamais une composante absente ou nulle finale.

L'ordre du couple est strictement `(ancre_N, ancre_N+1)` selon cet ordre canonique. La date du backup source n'intervient pas dans le tri ; elle n'est qu'un horodatage de capture.

### Doublon d'ancre

Si deux répertoires de `versions/` parsent vers le **même triplet `(majeur, mineur, patch)`** — qu'ils portent ou non le même tag textuel — l'ancre est marquée **ambiguë** et tous les couples impliquant cette ancre sont rejetés.

Conséquence directe : `Arsenal_v15`, `Arsenal_v15.0` et `Arsenal_v15.0.0` produisent tous le triplet `(15, 0, 0)`. La présence simultanée d'au moins deux de ces formes dans `versions/` constitue un doublon d'ancre, indépendamment de la différence orthographique du tag.

La levée d'ambiguïté est une action humaine : renommer ou supprimer les répertoires en conflit. La brique ne tranche jamais d'elle-même.

### Cohérence temporelle observable

Le tri canonique repose strictement sur `(majeur, mineur, patch)`. La date de capture n'intervient pas dans le tri.

En revanche, la brique observe la cohérence temporelle du graphe et signale les ancres rétroactives.

Une ancre est dite **rétroactive** si sa date de capture est postérieure à celle d'une ancre d'ordre canonique supérieur déjà existante.

Exemple :

```text
v15    capturé le 11 mai
v14.3  capturé le 15 mai   → rétroactive
```

Ce cas est légitime (hotfix de maintenance sur une branche antérieure publiée après une release ultérieure). La brique ne le rejette pas.

Elle enregistre un `lineage_warning` dans `state/processed_releases.json` et produit normalement les diffs concernés. La rétroactivité reste consultable mais n'altère ni le tri canonique, ni la production des diffs.

La date de capture est lue depuis le **préfixe du nom de répertoire** (`YYYY-MM-DD_HH-MM`), jamais depuis le mtime filesystem.

Si une ancre n'a pas de préfixe daté reconnaissable, elle est traitée sans information temporelle : aucun `lineage_warning` n'est produit pour les couples l'impliquant.

---

## Modèle de données

### `state/processed_releases.json`

Fichier d'état distinct de `state/processed_backups.json`. Aucun couplage entre les deux.

Structure :

```json
{
  "schema_version": 1,
  "couples": [
    {
      "from": "v14.2",
      "to": "v15",
      "from_version_dir": "2026-05-10_09-12_Arsenal_v14.2_abc12345",
      "to_version_dir": "2026-05-11_18-30_Arsenal_v15_d4464cb6",
      "from_sha256": "...",
      "to_sha256": "...",
      "status": "ok",
      "produced_at": "2026-05-12T08:30:00+02:00",
      "is_consecutive": true,
      "diff_path": "_diff/releases/v14.2__to__v15.md",
      "digest_path": "_diff/releases/v14.2__to__v15__digest.md"
    }
  ],
  "lineage_warnings": [
    {
      "anchor": "v14.3",
      "captured_at": "2026-05-15T10-00",
      "later_than": ["v15"],
      "detected_at": "2026-05-16T08:30:00+02:00"
    }
  ],
  "rejected": [
    {
      "reason": "anchor_ambiguous",
      "anchor": "v15",
      "version_dirs": [
        "2026-05-11_18-30_Arsenal_v15_d4464cb6",
        "2026-05-11_22-15_Arsenal_v15_aa11bb22"
      ],
      "detected_at": "2026-05-12T08:30:00+02:00"
    }
  ]
}
```

### Hash de snapshot

Le `sha256` d'un snapshot ancre est calculé sur le contenu canonique du répertoire `versions/<ancre>/` :

- liste triée des chemins relatifs,
- hash du contenu de chaque fichier,
- concaténation puis hash global.

Algorithme exact à figer dans le module utilitaire `release_snapshot_hash.py` afin de garantir la reproductibilité.

Le mécanisme de calcul de hash peut être ultérieurement cacheable sans modifier la sémantique du contrat. Un cache éventuel (typiquement `state/release_snapshot_hash_cache.json`) ne doit jamais altérer la valeur produite par l'algorithme canonique ; il ne sert qu'à éviter de relire un snapshot inchangé. La présence ou l'absence d'un cache reste un détail d'implémentation, invisible des consommateurs du contrat.

### Champ `is_consecutive`

Chaque entrée de `couples` porte un booléen `is_consecutive` qui qualifie la nature du couple au regard du graphe canonique d'ancres **au moment de la dernière exécution de la brique**.

Un couple `(A, B)` est dit **consécutif** si et seulement si :

- A et B sont toutes deux présentes dans le graphe d'ancres courant,
- B est l'ancre immédiatement supérieure à A dans l'ordre canonique,
- aucune autre ancre du graphe n'est strictement comprise entre A et B.

Le champ est **recalculé à chaque exécution** de la brique sur l'ensemble des couples existants de `processed_releases.json`. La création d'une nouvelle ancre intermédiaire peut donc transformer rétroactivement un couple consécutif en couple non-consécutif. Cette transformation est purement métadonnée : elle ne modifie ni le diff produit, ni le digest, ni les chemins de fichiers, ni les hashes des snapshots.

Le mode d'exécution qui a produit le diff (batch ou `--couple`) n'est pas tracé. Seule la nature actuelle du couple compte.

Ce champ est strictement informatif : il n'intervient ni dans l'idempotence, ni dans la production des diffs, ni dans les politiques d'échec. Il sert uniquement à structurer l'index lisible par l'humain et à offrir un point d'accroche stable aux consumers futurs (Arsenal Search, release intelligence) sans imposer de classification physique des artefacts.

---

## Capacités du moteur

Le moteur expose deux modes de production, de rang égal :

| Mode | Couples produits | Déclenchement |
|------|------------------|---------------|
| Batch consécutif | Tous les couples `(ancre_N, ancre_N+1)` selon l'ordre canonique | Exécution sans `--couple` |
| Couple arbitraire | Un couple `(A, B)` explicitement demandé, voisins ou non | Exécution avec `--couple A B` |

Les deux modes utilisent strictement le même algorithme de production de diff (lecture directe des deux snapshots ancres, aucun replay, aucun parcours d'intermédiaires). La seule différence est la sélection des couples.

Les diffs produits par les deux modes coexistent dans `_diff/releases/` et sont indexés dans `state/processed_releases.json` sans distinction de provenance. Un couple `(v14, v16)` produit explicitement reste valide même si les couples consécutifs `(v14, v15)` et `(v15, v16)` existent par ailleurs.

L'idempotence est calculée par couple, indépendamment du mode qui l'a produit.

---

## Algorithme

### Phase commune : construction du graphe d'ancres

```text
1. Scanner versions/ (flat, premier niveau uniquement)
2. Pour chaque répertoire, tester la regex d'ancre
   - match → enregistrer (tag, dir, date_capture)
   - no match → ignorer
3. Détecter les doublons de tag
   - doublon → enregistrer dans rejected, sortir l'ancre du graphe
4. Trier les ancres restantes par ordre canonique
5. Détecter les ancres rétroactives → lineage_warnings
```

### Phase de production

**Mode batch consécutif** (par défaut) :

```text
6a. Construire les couples consécutifs (a_N, a_N+1)
```

**Mode couple arbitraire** (`--couple A B`) :

```text
6b. Résoudre A et B comme ancres du graphe
    - A ou B absente → erreur opérationnelle, exit 1
    - A et B identiques → erreur opérationnelle, exit 1
    - A canoniquement postérieure à B → erreur opérationnelle, exit 1
7b. Construire le couple unique (A, B)
```

### Phase finale : production des diffs

```text
8. Pour chaque couple sélectionné :
   a. Calculer from_sha256 et to_sha256
   b. Chercher dans processed_releases.json :
      - couple identique avec mêmes sha256 et status=ok → SKIP
      - sinon → produire
   c. Produire diff direct snapshot ↔ snapshot
   d. Produire digest
   e. Mettre à jour processed_releases.json
9. Recalculer is_consecutive pour TOUS les couples de processed_releases.json
   (y compris ceux non retraités à cette exécution)
10. Régénérer INDEX_RELEASES.md
```

Aucune lecture de `_diff/timeline/*.md`. Aucun replay. Aucun parcours des backups intermédiaires, y compris en mode couple arbitraire.

Les diffs sont stockés à plat dans `_diff/releases/`, sans sous-dossier de classification. La qualification consécutif / non-consécutif est portée par le champ `is_consecutive` de `processed_releases.json` et matérialisée visuellement dans `INDEX_RELEASES.md`.

---

## Sorties

### `_diff/releases/`

```text
_diff/releases/
├── INDEX_RELEASES.md
├── v14__to__v14.1.md
├── v14__to__v14.1__digest.md
├── v14.1__to__v14.2.md
├── v14.1__to__v14.2__digest.md
├── v14.2__to__v15.md
└── v14.2__to__v15__digest.md
```

### Format `<from>__to__<to>.md`

Diff détaillé. Sections imposées :

- entête : couple, snapshots source, sha256, date de production,
- fichiers ajoutés,
- fichiers supprimés,
- fichiers modifiés (avec diff unifié borné),
- bilan numérique.

En V1, les renommages et déplacements de fichiers ne sont pas interprétés sémantiquement. Ils apparaissent volontairement comme une suppression + un ajout. Aucune heuristique de détection de renommage n'est appliquée afin de préserver la reproductibilité, la simplicité du moteur et l'absence de faux positifs.

### Format `<from>__to__<to>__digest.md`

Résumé court orienté changelog. Sections imposées :

- couple,
- statistique : N fichiers ajoutés, M modifiés, K supprimés,
- top 10 fichiers les plus modifiés (par volume de lignes),
- domaines Arsenal touchés (déduits du préfixe `NN_*`),
- indicateurs métier (présence de modifications dans `00_documentation_arsenal/`, `configuration.yaml`, etc.).

Le digest est explicitement conçu pour servir de **squelette de pré-changelog**. Il n'est pas un changelog publiable en l'état.

### `INDEX_RELEASES.md`

Index linéaire des couples produits.

Structure en deux sections successives :

1. **Couples consécutifs** : tous les couples `(A, B)` avec `is_consecutive = true`, listés du plus récent au plus ancien selon l'ordre canonique de B. Cette section reflète le graphe canonique des releases tel qu'il existe au moment de la dernière exécution.
2. **Couples non-consécutifs** : tous les couples `(A, B)` avec `is_consecutive = false`, listés du plus récent au plus ancien selon l'ordre canonique de B. Cette section contient les diffs d'exploration, de backport, ou les anciens couples consécutifs qu'une ancre intermédiaire a rendus non-consécutifs rétroactivement.

Chaque entrée porte un lien vers le diff et vers le digest correspondant.

Ne contient jamais de couple rejeté ni d'ancre marquée par `lineage_warning` (ces informations restent dans `state/processed_releases.json`).

L'index est régénéré intégralement à chaque exécution, à partir de `processed_releases.json`.

### `state/release_diff_last_run.json`

Résumé du dernier run, destiné exclusivement à la projection MQTT (`publish_release_diff_mqtt.sh`).

- Écrit à la fin de chaque exécution que la brique peut mener à terme, y compris en échec contrôlé (schéma d'erreur).
- Schéma défini par le contrat `release_diff_mqtt.md` §5 (source unique) ; le présent contrat n'en duplique pas la structure.
- Artefact de projection **non patrimonial** : régénéré intégralement à chaque run, il ne participe ni à l'idempotence (portée par `state/processed_releases.json`), ni à la régénérabilité de `_diff/releases/`. Sa suppression n'entraîne aucune perte de patrimoine.
- Le champ `produced[]` ne liste que les couples nouvellement produits au cours du run ; il ne se substitue jamais à `processed_releases.json`.

---

## Interface CLI

```bash
python3 release_diff.py [OPTIONS]
```

Options :

| Option | Effet |
|--------|-------|
| (aucune) | Mode batch consécutif : produit tous les couples `(ancre_N, ancre_N+1)`. |
| `--couple <from> <to>` | Mode couple arbitraire : produit le seul couple `(from, to)`, voisins ou non dans l'ordre canonique. |
| `--dry-run` | Scanne, détecte les couples sélectionnés selon le mode, simule la production, n'écrit rien. |
| `--force` | Retraite les couples sélectionnés même si déjà marqués `ok`. |
| `--limit N` | En mode batch consécutif uniquement : borne le nombre de couples produits par exécution. Sans effet en mode couple arbitraire. |
| `--strict` | Échoue (exit code non-nul) dès qu'un rejet est détecté. Mode CI/audit. |

Sortie standard : journal structuré ligne par ligne, lisible par un humain et grep-able.

Exit codes :

| Code | Sens |
|------|------|
| 0 | Exécution nominale, zéro rejet ou rejets tolérés (hors `--strict`). |
| 1 | Erreur opérationnelle (I/O, permissions, snapshot illisible). |
| 2 | Mode `--strict` et au moins un rejet détecté. |

---

## Politiques d'échec

REJECT-not-clamp en toutes circonstances.

| Cas | Décision |
|-----|----------|
| Tag dupliqué dans `versions/` | Couple rejeté, ancre marquée ambiguë, écrit dans `rejected`. |
| Snapshot illisible (permissions, corruption) | Couple rejeté avec `reason=snapshot_unreadable`. |
| Aucun couple éligible (moins de deux ancres) | Sortie nominale, journal explicite, aucun écrit. |
| Ordre canonique incohérent (rare, ex : majeur descendant) | Couple rejeté avec `reason=order_inconsistent`. |
| `versions/` absent ou vide | Erreur opérationnelle, exit code 1. |
| `--couple A B` avec A ou B absente du graphe | Erreur opérationnelle, exit code 1. |
| `--couple A A` (identité) | Erreur opérationnelle, exit code 1. |
| `--couple A B` avec A canoniquement postérieure à B | Erreur opérationnelle, exit code 1. |
| Ancre rétroactive détectée | `lineage_warning` enregistré, diffs produits normalement. Aucun blocage. |

Aucune heuristique de récupération automatique. La résolution est manuelle, hors brique.

---

## Indépendance vis-à-vis de la timeline forensic

`release_diff` ne déclenche jamais l'extracteur. Il ne modifie ni `_diff/timeline/`, ni `state/processed_backups.json`, ni `versions/`, ni `ha_backup_maison/`.

Inversement, `ha_backup_timeline_extract_v2.py` et `ha_backup_timeline_diff.py` ne lisent ni n'écrivent dans `_diff/releases/` ni `state/processed_releases.json`.

Cette indépendance est un invariant architectural : les deux couches peuvent être désactivées, supprimées, ou reconstruites séparément.

---

## Ordonnancement

`release_diff` peut être exécuté :

- à la main (commande directe),
- via Scheduler Synology, en tâche distincte de l'extraction timeline,
- en mode CI/audit avec `--strict` lors d'une livraison de version.

Fréquence recommandée : déclenchement manuel ou quotidien. Le besoin est aligné sur le rythme des releases (jours/semaines), pas sur le rythme des backups (30 minutes).

Aucune dépendance temporelle entre `release_diff` et le scheduler d'extraction.

---

## Prérequis de mise en service

Migration mineure des artefacts forensic existants :

```text
_diff/*.md         →  _diff/timeline/*.md
_diff/INDEX.md     →  _diff/timeline/INDEX.md
```

Cette migration est nécessaire pour libérer l'espace `_diff/releases/` et formaliser la séparation des couches. Elle n'altère aucun contenu, uniquement les chemins.

Mise à jour conjointe du contrat `diff_auto.md` : la section *Structure NAS* doit refléter la nouvelle arborescence `_diff/timeline/` et `_diff/releases/`.

---

## Dépannage

### Aucun couple produit

Vérifier :

- présence d'au moins deux ancres détectées dans `versions/`,
- absence de doublons de tag (consulter `rejected` dans `processed_releases.json`),
- ordre canonique cohérent.

### Couple attendu manquant

Vérifier :

- les deux répertoires sources matchent bien la regex d'ancre,
- aucun suffixe parasite (`_rc1`, `_test`, tiret) ne casse le match,
- le couple n'est pas déjà rejeté pour ambiguïté.

### Diff incomplet ou suspect

Vérifier :

- intégrité des deux snapshots ancres (taille, nombre de fichiers),
- `from_sha256` et `to_sha256` distincts (sinon les deux snapshots sont identiques, le diff est légitimement vide),
- relancer avec `--force` après correction si besoin.

### Rejet pour ambiguïté

Action humaine obligatoire. Renommer ou supprimer le doublon dans `versions/`, puis relancer. La brique ne tranche jamais d'elle-même.

### `lineage_warning` signalé

Cas légitime dans les workflows de maintenance (hotfix d'une branche antérieure publié après une release ultérieure). Aucune action requise.

Si le warning révèle au contraire une erreur de tag humaine (typiquement un `v14.3` qui aurait dû être `v15.3`), la correction est manuelle : renommer le répertoire dans `versions/` et relancer avec `--force` sur les couples impactés.

---

## Hors périmètre

Explicitement non couvert par cette brique (à confier à des couches ultérieures) :

- génération automatique de changelog Arsenal publiable,
- classification sémantique des changements (feature / fix / refactor),
- détection de rupture de contrat (lecture des en-têtes normatifs),
- corrélation avec le journal de commits Arsenal,
- interface web de consultation des diffs de release (relève d'Arsenal Search).

Le digest produit est un squelette destiné à alimenter ces couches, pas à les remplacer.

---

## Bilan d'invariants

Renforcés par cette brique :

- séparation explicite forensic / sémantique,
- régénérabilité totale de `_diff/releases/` à partir de `versions/`,
- REJECT-not-clamp étendu au domaine release,
- idempotence par couple `(ancre_N, ancre_N+1)` ou par couple arbitraire, indépendamment du mode producteur,
- cohérence temporelle observable du graphe d'ancres, sans blocage des workflows de maintenance légitimes,
- non-interprétation des renommages en V1 (rename = delete + create), garantissant reproductibilité et déterminisme,
- namespace plat stable pour les artefacts de diff : la nature consécutive ou non d'un couple n'altère ni son chemin, ni son contenu, et reste une métadonnée recalculable.
- `state/release_diff_last_run.json` est un artefact de projection non patrimonial, régénéré à chaque run, hors idempotence ; son schéma est porté par `release_diff_mqtt.md`.

Déjà établis et préservés :

- source unique = `ha_backup_maison/*.tar`,
- `versions/` reste l'unique source régénérable des artefacts dérivés,
- aucun secret versionné,
- aucune exposition publique.

Non altérés :

- pipeline d'extraction (`ha_backup_timeline_extract_v2.py`),
- pipeline forensic (`ha_backup_timeline_diff.py`),
- contenu de `_diff/timeline/` une fois migré,
- `state/processed_backups.json`.
