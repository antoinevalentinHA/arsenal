# Rapport d’avancement — Chantier « Navigation documentaire » (`contrats`)

- **Périmètre :** `00_documentation_arsenal/contrats`
- **Outil :** `scripts/docs_navigation/audit_doc_links.py`
- **Statut :** point d’étape consolidé — phase de réduction des `dead` terminée au bon niveau
- **Méthode :** audit en lecture seule → décision éditoriale → corrections ciblées (rechercher/remplacer VS Code) pour les lots sûrs ; garde-fous outil ajoutés par patches validés. Aucun `--fix-auto --apply` global.

---

## 1. Périmètre

Audit et fiabilisation des références documentaires internes du dossier `contrats/` : classification des renvois en `auto` / `ambiguous` / `dead` / `multi_target` / `ignored`, correction des liens cassés réels, linkification des renvois sûrs, et durcissement de l'outil contre les faux positifs. Les corrections documentaires ont été appliquées par l'auteur via rechercher/remplacer ; l'assistant a fourni diagnostics, lots exacts et validations (simulation + revert), sans modifier le dépôt.

## 2. État initial / état final

Au démarrage de la phase mesurée (nettoyage des `dead`), l'audit global `contrats` présentait un corpus largement non lié, avec un nommage hérité résiduel (`CONTRAT_*` / `DOCTRINE_*` majuscules) générant de nombreux liens morts.

| Indicateur | Initial | Final |
|---|---:|---:|
| Fichiers scannés | 248 | 248 |
| Fichiers concernés | 38 | 32 |
| Candidats | 611 | 591 |
| `auto` | 116 | **103** |
| `ambiguous` | 2 | **2** |
| `dead` | 17 | **5** |
| `multi_target` | 0 | **0** |
| `ignored` | 476 | 481 |

`dead` réels : **17 → 5** (les 5 restants sont assumés, cf. §5). Linkification des lots sûrs et désambiguïsations menées par domaine (chauffage, boiler, climatisation, météo, aération).

## 3. Corrections réalisées, par familles

- **Références mortes héritées (`CONTRAT_*` / `DOCTRINE_*`).** Réconciliation du nommage : `DOCTRINE_CAUSALITE.md` → `architecture/03_doctrines/causalite_metier.md` ; `CONTRAT_ECLAIRAGE_SEJOUR.md` → `sejour.md` ; reformulation des **auto-identifiants d'en-tête** (`entree.md`, `sejour.md`, `cardio_nuit.md`, `sommeil.md`, `volets_pluie.md`) vers le nom de fichier courant (reclassés `self_reference`). Effet : `dead` 17 → 7.
- **Renvoi de domaine `aeration.md`.** Repointé vers l'entrée canonique `aeration_blocage_chauffage/README.md` (2 occurrences). Effet : `dead` 7 → 5.
- **Index de modules.** `aeration_blocage_chauffage/README.md` : 13 renvois `socle_transversal/NN_*.md` linkifiés (index « Socle transversal »). Effet : `auto` −13.
- **Désambiguïsations.** `boiler/README.md` `mqtt.md` → `outils_externes/boiler_pi/mqtt.md` ; `boiler/script_executif.md` `CONTRAT_MQTT.md` → `outils_externes/boiler_pi/mqtt.md` avec réconciliation d'ancre (`§11` → `§5.3/§5.4`) et de version ; `climatisation/06_doctrine_blocages.md` `90_observations.md §4` → `capteurs/blocages/90_observations.md`.
- **Linkification des renvois sûrs par domaine.** Météo (lots backtick « Références / flèches ») ; climatisation (renvois backtick intra-domaine) ; chauffage (en-têtes relationnels et tokens backtick).

## 4. Garde-fous ajoutés à l'outil

Tous validés (compilation, audit avant/après, round-trip) ; aucun n'altère le périmètre `scope` ni la documentation.

- **Application par positions `start/end`** : remplacement de `line[start:end]` exact, droite→gauche, anti-chevauchement ; **jamais** `line.replace()`. Plan **dry-run ≡ apply** garanti par fonction partagée.
- **`--fix-auto --dry-run` / `--apply`** : `--apply` réactivé après validation ; exclusivité `--dry-run` XOR `--apply` ; refus si aucun des deux.
- **`--output` (rapport Markdown)** : sortie archivable, respecte `--status`, échappe les `|`.
- **`navigation_layer`** : une référence dont les cibles sont uniquement sous `navigation/` est classée `ignored` (couche détachable, non ciblée automatiquement).
- **`cross_domain_extensionless`** : un `extensionless` dont la cible unique est dans un autre domaine `contrats/<X>` que la source est classé `ignored` (identifiant technique probable).
- **`version_token`** : un `extensionless` de la forme `v\d+` résolu sous `changelog/` est classé `ignored` (variable/version textuelle).
- **Robustesse audit** : auto-références classées `self_reference/ignored` ; `--status ignored` détaille bien les ignorés.

## 5. Décisions de non-correction assumées

**`dead` conservés (5)** — ne pas linkifier ni repointer artificiellement :

| Référence | Nature |
|---|---|
| `observabilite_nas.md` | Contrat futur / keystone NAS (à créer si confirmé) |
| `latest.md` | Rapport NAS généré, hors dépôt |
| `ventilation.md` | Méta-citation historique (anomalie documentée, README obsolète non modifié) |
| `security_audit_report.md` | Artefact généré (sortie d'audit à la racine) |
| `CONTRAT_ALERTE_SANTE.md` | Document futur explicitement « à créer » |

**`ambiguous` conservés (2)** :

| Référence | Raison |
|---|---|
| `climatisation/capteurs/README.md` `00_overview.md` | Convention générique multi-catégorie (ambiguïté intentionnelle) |
| `climatisation/capteurs/decision/90_observations.md` `presence` | Nom d'attribut technique, pas un renvoi documentaire |

**`auto` laissés bruts (volontaire)** : météo (`raw_md` en en-têtes `# Dépend de :` et mid-prose, `utility_meter`) ; ECS (identifiants runtime intra-domaine : `ecs_fin_cycle_signal`, `ecs_cycle_session_*`, …) ; bandeau de hiérarchie cross-domaine d'`aeration_blocage_chauffage` ; reliquats racine/divers à traiter au cas par cas. `multi_target` : 0.

## 6. Règles pour la suite

1. **Ne jamais appliquer globalement les `extensionless`** : forte densité de faux positifs (identifiants runtime, noms techniques HA, versions). Traitement ciblé uniquement.
2. **Traiter `dead` avant `auto`** : un lien cassé dégrade la navigation plus qu'un renvoi non lié.
3. **Ne pas viser `auto: 0`** : nombre de renvois `auto` sont des valeurs/identifiants techniques légitimement non liés.
4. **Documenter les `dead` assumés** : artefact généré, document futur, ou méta-citation historique doivent être qualifiés explicitement, jamais « corrigés » pour faire baisser le compteur.
5. **Toujours `--dry-run` avant `--apply`** ; vérifier le plan, l'unicité des cibles et l'absence de lien cassé.
6. **Compléments doctrinaux** : ne jamais lier vers `navigation/` ; linkifier les vrais renvois (listes « Références », flèches, déclarations de dépendance), pas les identifiants runtime, valeurs, artefacts ou méta-citations ; privilégier le rechercher/remplacer ciblé (avec `files-to-include`) pour les corrections éditoriales simples.

---

*Point d’étape consolidé. État courant : `auto 103 · ambiguous 2 · dead 5 · multi_target 0 · ignored 481` sur 591 candidats / 248 fichiers. La phase de réduction des `dead` réels est stabilisée ; les compteurs résiduels correspondent à des décisions assumées, des références futures/externes, ou des lots à traiter ultérieurement au cas par cas.*
