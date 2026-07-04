# C14 — Lot 1E : frontière git / sécurité publication (audit)

- **Type :** lot d'**audit / cadrage** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md) — **pas** d'implémentation, pas de suppression, pas de désindexation
- **Statut :** rapport livré ; aucun fichier runtime, `.gitignore`, workflow ni checker modifié
- **Base :** `main` @ `6373b78` (post-#268)
- **Périmètre modifié :** ce rapport + `index.md` + registre des chantiers uniquement
- **Principe :** ne rien effacer, déplacer ou ignorer sans comprendre son rôle ; ne rien classer sensible sans inspection ; ne pas classer publiable par défaut parce qu'un fichier est déjà suivi.

---

## 1. Objet

Établir précisément ce qui peut entrer dans Git, ce qui doit rester local, ce qui doit être ignoré et ce qui doit être **bloqué automatiquement** avant publication. Le livrable est ce cadrage ; l'implémentation relève de lots suivants.

## 2. Risque traité

> **Un dépôt Git peut publier accidentellement des secrets, fichiers runtime, backups, traces personnelles ou artefacts locaux** — visibles après `git clone`, y compris via l'historique même si corrigés dans l'état courant.

## 3. État actuel du dépôt

**Constat majeur : l'infrastructure de sécurité publication existe déjà, mais n'est pas branchée en CI.**

| Catégorie | Présent dans Git ? | Sensibilité | Règle actuelle | Risque | Action recommandée |
|---|---|---|---|---|---|
| Secrets réels (`secrets.yaml`, `.env`, `.pem`, `.key`, `.crt`) | **Non** (0 suivi) | critique | `.gitignore` + contrat S5a | faible (bien couvert) | maintenir |
| Exemples de secrets (`secrets.yaml.example`) | Non (absent) | faible | — | — | (optionnel : fournir un exemple anonymisé) |
| Runtime HA (`.storage/`, `*.db`, `home-assistant.log*`, `.uuid`, `.HA_VERSION`) | **Non** (0 suivi) | critique | `.gitignore` complet | faible | maintenir |
| **Logs suivis** | **`zigbee2mqtt/migration-4-to-5.log`** (1 fichier) | faible (contenu : 4 lignes, 0 IP/MAC/token) | **trou `.gitignore`** (voir §4) | **modéré** (viole doctrine + contrat S5a) | gitignore `*.log` + **désindexer** (arbitrage, Lot 1E-d) |
| Backups / archives (`backups/`, `*.tar`, `*.zip`) | Non (0 suivi) | critique | `.gitignore` | faible | maintenir |
| Custom components (`custom_components/`) | **Oui** (2321 fichiers) | modérée | `.gitattributes` `linguist-vendored` | assumé (vendored HACS/intégrations) | maintenir — versionnable sous conditions |
| Frontend (`www/`) | **Oui** (25 fichiers) | faible | `.gitattributes` vendored (partiel) | faible | maintenir |
| Données personnelles (IP, GPS, noms) | **Oui, dans des docs** | modérée | contrat S2/S4/S8 (scanner) | **à qualifier** (voir §5) | annoter `audit:scope=doc` ou remédier |
| Exports personnels | Non | — | `.gitignore` (`*_sanitized.*`, `*_redacted.*`) | faible | maintenir |
| Caches (`__pycache__/`, `.cache/`, `tts/`, `deps/`) | Non | faible | `.gitignore` | faible | maintenir |
| Fichiers CI / docs / contrats / checkers | **Oui** (patrimoine) | publiable | — | — | publiable assumé |

## 4. Audit `.gitignore`

**Protections existantes (solides) :** secrets (`secrets.yaml`, `*.pem/.key/.crt/.p12`), runtime HA (`.storage/`, `.cloud/`, `*.db*`, `home-assistant.log*`, `.uuid`, `.HA_VERSION`), réseau (`ip_bans.yaml`, `known_devices.yaml`), état éphémère (`state.json`, `.state`, `tts/`, `deps/`), caches (`.cache/`, `__pycache__/`, `*.py[cod]`), Zigbee2MQTT runtime (`zigbee2mqtt/log/`, `coordinator_backup.json`, `state.json`, `database.db*`), backups/archives (`backups/`, `*.tar`, `*.tar.gz`, `*.zip`), OS/éditeurs, tokens/auth (`access_tokens.*`, `auth`, `html5_push_registrations.conf`), pipeline de publication (`*_sanitized.*`, `*_redacted.*`, `security_audit_report.md`).

**Trou identifié :** pas de règle générique **`*.log`**. Le `.gitignore` couvre `home-assistant.log*`, `*.log.*` et le **dossier** `zigbee2mqtt/log/`, mais **pas** un `.log` de premier niveau comme `zigbee2mqtt/migration-4-to-5.log` — qui est **effectivement suivi** (preuve du trou). Un `*.log` global fermerait ce trou.

**Règles à surveiller (non dangereuses mais larges) :** `*.db`, `*.tar`, `*.zip`, `*.bak`, `auth` (sans slash — ignore tout fichier/dossier nommé `auth`), `*.local.yaml`. Aucune ne masque aujourd'hui un fichier nécessaire (vérifié : les fichiers patrimoine n'utilisent pas ces extensions).

## 5. Audit des fichiers suivis

**Méthode :** `git ls-files` filtré par extensions/noms sensibles + exécution du scanner du dépôt (`scripts/security/audit_publication_git.py`, read-only). **Aucune valeur sensible n'est reproduite ici** — seuls fichier, contrôle et nature du risque sont cités (le scanner redacte déjà : il rapporte `fichier:ligne — label`, pas la valeur).

**Résultat headline :** **aucun secret vivant** (token/password/clé) dans une **config runtime** n'est suivi. Aucun `secrets.yaml`, `.env`, `.pem`, `.key` suivi.

**Verdict brut du scanner (état courant) : 34 `CRITICAL` + 609 `WARNING`** — mais **dominés par des faux positifs et des références documentaires** :

- **26/34 CRITICAL = faux positifs de code** : le motif S1 `token`/`secret` capture le **mot** « token »/« secret » comme **identifiant Python ou motif de regex** dans l'**outillage du dépôt** — p. ex. `scripts/docs_navigation/audit_doc_links.py` (`token: str`, un lexer de liens Markdown), `scripts/docs_lint/*.py`, `tools/arsenal_ci/decision/normaliseur.py`, et `scripts/arsenal_contracts/check_zones_contracts.py:55-56` (où `!secret` est **dans la regex qui protège** les coordonnées GPS). Ce ne sont **pas** des secrets.
- **8/34 CRITICAL = findings documentaires à qualifier** : IP privées / domaines locaux / mention « synology » dans des **documents** — `outils_externes/nas_arsenal/investigations/enquete_clim_historique.md` (S1 token + 2× IP privée S2), `architecture/ecosysteme_depots_satellites.md` (port), `contrats/arrosage/08_inventaire_pont_runtime.md` (IP), `README.md` (URL domaine local ×2), `changelog/.../v16_0_5.md` + `resilience_integrations_registre.yaml` (mention synology). Le contrat prévoit exactement ce cas : annotation **`audit:scope=doc`** (dégrade CRITICAL→WARNING) ou **`audit:ignore`** par ligne, sinon remédiation. Ces annotations **ne sont pas encore posées**.

**Point d'attention — angle mort du scanner :** le scanner **exclut `zigbee2mqtt/` de son walker** (§3.4 du contrat, exclusions de performance). Il **n'a donc pas vu** le `.log` suivi de §3. Le contrôle S5a (`*.log` interdit) est ainsi contourné pour cet arbre — à corriger lors du branchement.

**Historique Git :** le changelog du scanner (v1.2.0) documente une **fuite passée de coordonnées GPS** du domicile dans `17_zones/*_securite.yaml` (désormais externalisées en `!secret`). En l'état courant c'est corrigé, mais un scan `--history` (`git rev-list --all`) rapporterait la fuite historique comme `CRITICAL` — **un `git clone` expose l'historique**. À évaluer dans un lot dédié (remédiation via `git filter-repo`, décision propriétaire).

## 6. Protections CI existantes

| Protection | Existe ? | État |
|---|---|---|
| Doctrine frontière patrimoine/runtime | **Oui** | [`architecture/03_doctrines/git.md`](../../../architecture/03_doctrines/git.md) — versionné vs jamais-versionné |
| Contrat de sécurité publication | **Oui** | [`contrats/publication/securite_publication_git.md`](../../../contrats/publication/securite_publication_git.md) v1.1.0, normatif |
| Scanner de secrets/exposition | **Oui** | `scripts/security/audit_publication_git.py` v1.2.0 — contrôles **S1–S8** (secrets, IP/réseau, MQTT/NAS/SSH, sécurité domestique, fichiers/dossiers interdits, historique git, GPS), placeholders, annotations, `PASS/WARNING/CRITICAL`, `--fail-on`, `--history` |
| **Branchement du scanner en CI** | **NON** | **aucun workflow ne l'appelle** — c'est le **trou principal** : un scanner normatif, implémenté et bloquant-capable qui **ne tourne jamais en CI** |
| `.gitignore` / `.gitattributes` | **Oui** | complets (voir §4) ; `.gitattributes` : `custom_components/**` et `www/…` en `linguist-vendored` |
| Docs lint lié à la publication | Non | hors périmètre (docs_lint traite la structure documentaire) |

**Ce qui manque / est automatisable :** (a) **brancher le scanner en CI** ; (b) mais pas en l'état — il faut d'abord **résoudre les 26 faux positifs S1** (raffiner le motif pour ne pas matcher les identifiants de code, ou exclure l'outillage — le contrat §2 prescrit qu'un faux positif conduit à une **évolution du contrat**, pas à une dégradation) et **annoter les 8 findings docs** (`audit:scope=doc`) ; (c) **fermer le trou `.gitignore` `*.log`** et **désindexer** le log suivi ; (d) lever l'**angle mort `zigbee2mqtt/`** du scanner pour S5a.

## 7. Doctrine cible proposée

La doctrine existe déjà (`git.md` + `securite_publication_git.md`) et est **globalement suffisante**. Formalisation des quatre catégories (confirmation, pas création) :

- **Publiable** : YAML déclaratif sans secret (includes structurés `01_`→`19_`, `configuration.yaml`, `recorder/logbook/logger.yaml`), contrats, checkers, workflows, documentation, `.vscode/settings.json`/`extensions.json`.
- **Local non versionné** : `secrets.yaml`, `.storage/`, `.cloud/`, logs (`*.log`), bases SQLite (`*.db*`), backups/archives, tokens/`auth`, caches (`tts/`, `deps/`, `.cache/`, `__pycache__/`), état éphémère (`state.json`).
- **Versionnable sous conditions** : `custom_components/` (vendored HACS/intégrations, assumé), `www/` (cartes frontend vendored), `zigbee2mqtt/configuration.yaml` (déclaratif maintenu à la main), exemples anonymisés / templates.
- **À bloquer automatiquement** (par le scanner, une fois branché) : secrets réels (S1), IP/domaines/ports privés non annotés (S2), MQTT/NAS/SSH (S3), codes/MAC/GPS de sécurité domestique (S4/S8), fichiers/dossiers interdits `*.db/*.log/*.key/*.pem/secrets.yaml/.storage/backups` (S5), fuites d'historique (S6).

## 8. Backlog d'implémentation

| Priorité | Lot | Objet | Garantie | Risque | Commentaire |
|---|---|---|---|---|---|
| **P1** | 1E-c | Raffiner le scanner S1 (ne pas matcher les identifiants de code) + lever l'angle mort `zigbee2mqtt/` pour S5a ; annoter `audit:scope=doc` les 8 findings docs | ramène le verdict à un **baseline `CRITICAL=0` réel** | faible (évolution de contrat + annotations) | **prérequis au branchement** |
| **P1** | 1E-b | **Brancher le scanner en CI** (`--fail-on critical`), d'abord **informatif** (`continue-on-error`) puis bloquant une fois le baseline propre | secrets/expositions **confrontés à chaque push** | moyen (faux rouge si branché avant 1E-c) | cœur du lot — après 1E-c |
| **P2** | 1E-d | Fermer le trou `.gitignore` `*.log` + **désindexer** `zigbee2mqtt/migration-4-to-5.log` | plus de log runtime suivi | faible | **désindexation = arbitrage propriétaire** |
| **P2** | 1E-a | Amender `git.md` / `securite_publication_git.md` si besoin (ex. `*.log` explicite, exclusion `zigbee2mqtt/` requalifiée) | doctrine alignée | faible | la doctrine existe déjà ; retouches mineures |
| **P3** | 1E-terrain | Assainissement de l'**historique git** (fuite GPS passée) via `git filter-repo` | historique propre | **élevé** (réécriture d'historique) | décision propriétaire ; hors CI |
| **P3** | 1E-terrain | Procédure opérateur « scanner avant push » (hook `pre-commit` local, S9 du contrat) | garde locale | faible | complément au CI |

## 9. Recommandation finale

**Première PR : Lot 1E-c** — préparer le scanner à être branché : (1) raffiner le motif S1 pour qu'il ne matche plus les **identifiants de code** (les 26 faux positifs de l'outillage), (2) lever l'angle mort `zigbee2mqtt/` pour que S5a voie le `.log` suivi, (3) annoter `audit:scope=doc` (ou requalifier) les **8 findings documentaires**. Objectif : atteindre un **baseline `CRITICAL=0` honnête**, sans dégrader la doctrine.

**Puis Lot 1E-b** : brancher le scanner en CI — d'abord **informatif** (`continue-on-error`, visibilité sans faux rouge), puis **bloquant** (`--fail-on critical`) une fois le baseline propre. C'est le vrai gain : la frontière git passe d'une **discipline manuelle** à une **garde confrontée**.

**En parallèle (quick win) : Lot 1E-d** — `.gitignore *.log` + désindexation du log suivi (sur GO propriétaire, car désindexation).

Cet ordre respecte le principe du lot : **ne pas brancher un scanner qui vire au rouge sur des faux positifs**, et **ne pas dégrader la doctrine pour faire taire un vrai signal**.

## 10. Non-actions de ce lot

Ce lot est un **audit**. Il n'a **pas** :

- supprimé de fichier ;
- désindexé de fichier (le `.log` suivi reste suivi) ;
- modifié de runtime YAML, d'ID, de contrat métier ;
- révélé de secret réel (seuls fichier + contrôle + label sont cités) ;
- créé de checker ;
- modifié `.gitignore`, `.gitattributes` ni aucun workflow ;
- traité le chargement HA, le chauffage, ni touché AID/APD ;
- fait de nettoyage opportuniste.

Le rapport `security_audit_report.md` généré par l'exécution du scanner **n'est pas versionné** (déjà couvert par `.gitignore`).
