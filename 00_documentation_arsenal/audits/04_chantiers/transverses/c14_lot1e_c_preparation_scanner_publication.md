# C14 — Lot 1E-c : préparation du scanner sécurité publication

<!-- audit:scope=doc — rapport discutant des motifs `token`/`secret`/`API_TOKEN = "…"` ; aucun secret réel (C14 Lot 1E-c) -->

- **Type :** lot d'**implémentation** du chantier [C14](chantier_couverture_ci_contrats_arsenal.md), suite de l'audit [Lot 1E](c14_lot1e_frontiere_git_securite_publication.md)
- **Statut :** exécuté — en attente de revue
- **Base :** `main` @ `076090b` (post-#269)
- **Périmètre modifié :** `scripts/security/audit_publication_git.py` (v1.2.0 → **v1.3.0**), contrat `securite_publication_git.md` (v1.1.0 → **v1.2.0**, contrat de l'outil), 3 annotations `audit:scope=doc` sur des documents, + ce rapport + index + registre
- **Non fait ici :** scanner **non branché en CI**, log suivi **non désindexé**, `.gitignore` **non modifié**, historique git **non assaini** (cf. §8)

---

## 1. Objet

Préparer le scanner `audit_publication_git.py` pour un branchement CI **honnête** : réduire les faux positifs (sans affaiblir la détection de vrais secrets), lever l'angle mort `zigbee2mqtt/`, qualifier les findings documentaires. **Le branchement CI est un lot séparé (1E-b).**

Principe respecté : *ne jamais dégrader la doctrine pour faire taire un vrai signal ; ne jamais brancher un scanner bruyant.*

## 2. Verdict initial

Mesuré sur `origin/main` (scanner d'origine, arbre d'origine — `Path.cwd()`) : **35 CRITICAL / 611 WARNING**. Décomposition exacte des 35 :

| Catégorie de finding | Nombre | Contrôle | Statut |
|---|---:|---|---|
| Faux positifs de **code** (mot-clé capté comme identifiant/type/appel dans un `.py`) | **25** | S1 | à éliminer (garde S1 littéral-en-code) |
| Findings **documentaires** (dans 3 `.md`) : `token` ×2, IP privée LAN ×2, port `localhost` ×1 | **5** | S1 + S2 | à qualifier `audit:scope=doc` → `WARNING` |
| Faux positifs de **motif** : `README` (URL `home-assistant.io` lue « domaine local ») ×2, nom de fichier `synology.yaml` ×2 | **4** | S2 + S3 | à corriger **dans le scanner** (bénéfice général) |
| **Vrai signal** : IP privée réelle dans un **contrat métier** (`arrosage/08_inventaire_pont_runtime.md:42`) | **1** | S2 | à conserver `CRITICAL` |
| **Total CRITICAL initial** | **35** | | |
| WARNING total | **611** | | bruit documentaire attendu |

**Note importante :** le `.log` suivi `zigbee2mqtt/migration-4-to-5.log` **n'est pas** dans ces 35 — l'angle mort S5a (walker filtré par `EXCLUDED_DIRS`) le **masquait**. La correction S5a (git-tracked) le **révèle** : c'est un **2ᵉ vrai signal, jusqu'ici caché**, pas un nouveau problème.

*Aucune valeur sensible n'est reproduite ici : seuls fichier + contrôle + label sont cités.*

## 3. Corrections du scanner

| Règle | Problème | Correction | Risque de régression | Test associé |
|---|---|---|---|---|
| **S1** | Le mot-clé `token`/`secret`/`password` capté comme **identifiant / type / appel** de code (`token: str`, `_G_TOKEN = re.compile(...)`, `RE_LAT_SECRET = …`, `token=line.strip()`) | En fichier de **code** (`.py`, `.sh`, `.js`, …), S1 ne se déclenche que si la valeur est un **littéral chaîne quoté**. Non-code (YAML/.md) inchangé | **Faible** — un secret codé en dur `API_TOKEN = "…"` reste quoté donc `CRITICAL` ; les YAML runtime (secrets `!secret` = placeholder) inchangés | selftest : 8 négatifs code + 5 positifs |
| **S5a** | Angle mort : `zigbee2mqtt/` exclu du walker → un `.log` **suivi** y échappait | Détection des fichiers interdits sur les fichiers **versionnés** (`git ls-files`) de **tout l'arbre**, indépendamment de `EXCLUDED_DIRS` | **Faible** — un artefact runtime **non suivi** (gitignoré) n'est plus signalé (correct : ne sera pas publié) | selftest : extensions `.log`/`.db`/`.key` reconnues |
| **S2** | `community.home-assistant.io` lu comme « domaine local » (le `.home` de `home-assistant`) | Lookahead `(?![\w-])` : le suffixe local doit être le **label terminal** | Faible — `foo.local` / `foo.home` (fin) toujours détectés | verdict : README ×2 disparus |
| **S3** | `synology.yaml` (**nom de fichier**) lu comme « accès distant » | Lookahead excluant les extensions de fichier après `synology.` | Faible — `synology.local`/`synology.com` (hostnames) toujours détectés | verdict : changelog + registre disparus |

Version : script **v1.3.0**, contrat de l'outil **v1.2.0** (§ 3.4, § 5.S1, § 5a alignés + journal). Le scanner **ne modifie jamais** le dépôt (invariant conservé).

## 4. Cas `zigbee2mqtt/`

- **État initial :** `zigbee2mqtt/` est dans `EXCLUDED_DIRS` (contrat § 3.4 — « tiers, hors périmètre »). Cette exclusion, pensée pour le scan de **contenu**, s'appliquait aussi par ricochet au contrôle des **fichiers interdits (S5a)**, qui reposait sur la liste du walker.
- **Cause de l'angle mort :** `scan_forbidden_files` itérait sur `iter_repo_files()` (filtré par `EXCLUDED_DIRS`). Le fichier **suivi** `zigbee2mqtt/migration-4-to-5.log` n'était donc jamais vu → S5a contourné.
- **Correction :** `scan_forbidden_files` porte désormais sur `git ls-files` (fichiers versionnés, tout l'arbre). Le contrat § 3.4 et § 5a sont amendés pour dire que l'exclusion ne vaut que pour le **contenu**, pas pour S5a.
- **Statut du `.log` suivi :** il **remonte désormais comme `CRITICAL` S5** — c'est un **vrai signal** (un `.log` versionné viole la frontière et le contrat S5a). Il **ne peut pas** être ramené à zéro sans **désindexation**, qui relève du **Lot 1E-d** (arbitrage propriétaire). **Non désindexé dans ce lot.**

## 5. Findings documentaires

| Fichier | Nature | Statut retenu | Justification |
|---|---|---|---|
| `outils_externes/nas_arsenal/investigations/enquete_clim_historique.md` | investigation (token + IP LAN) | `audit:scope=doc` → `WARNING` | document d'investigation ; IP LAN privées documentaires, aucun secret opérationnel |
| `architecture/ecosysteme_depots_satellites.md` | architecture (`localhost:<port>`) | `audit:scope=doc` → `WARNING` | port `localhost` documentaire |
| `audits/.../c14_lot1e_frontiere_git_securite_publication.md` | rapport d'audit (mots `token`/`secret`) | `audit:scope=doc` → `WARNING` | méta-documentation, aucun secret réel |
| `README.md` (×2) | URL `home-assistant.io` publiques | **corrigé au motif S2** (plus de finding) | FP : `.home-assistant.io` n'est pas un domaine local |
| `changelog/.../v16_0_5.md` | nom de fichier `synology.yaml` | **corrigé au motif S3** (plus de finding) | FP + fichier **frozen** (non annotable) — la correction du motif évite d'y toucher |
| `scripts/arsenal_contracts/resilience_integrations_registre.yaml` | nom de fichier `synology.yaml` | **corrigé au motif S3** (plus de finding) | FP : nom d'automatisation, pas un accès distant |
| `contrats/arrosage/08_inventaire_pont_runtime.md` | **vraie IP privée** (réservation DHCP) dans un **contrat métier** | **conservé `CRITICAL`** | vrai signal ; **contrat métier non modifié** dans ce lot — décision propriétaire (anonymiser ou `scope=doc`) |

Choix de méthode : les FP de **motif** (README, synology) sont corrigés **dans le scanner** (bénéfice général), pas par annotation ; les findings **réellement documentaires** sont annotés `scope=doc` (visibles en `WARNING`, non silencieux) ; le **contrat métier** arrosage n'est **pas** touché (résiduel assumé).

## 6. Baseline finale

| Niveau | Avant | Après | Commentaire |
|---|---:|---:|---|
| CRITICAL | **35** | **2** | 2 vrais signaux résiduels (§ ci-dessous) |
| WARNING | 611 | 620 | +9 net : +5 CRITICAL documentaires dégradés en `WARNING` (`scope=doc`) + auto-références `scope=doc` de **ce rapport** (mots `token`/`password`/… cités) − 4 FP de motif supprimés (plus aucun finding) |
| Faux positifs **code** (S1) | 25 | **0** | garde S1 littéral-en-code |
| Faux positifs **motif** (S2/S3) | 4 | **0** | lookaheads README + synology |
| Findings **documentaires** | 5 | 0 CRITICAL | 3 fichiers annotés `scope=doc` → `WARNING` |
| **Vrais signaux CRITICAL** | 1 *(arrosage)* | **2** | arrosage (conservé) **+ zigbee log révélé par S5a** |

**Les 2 `CRITICAL` résiduels sont de vrais signaux, pas des faux positifs :**

1. `contrats/arrosage/08_inventaire_pont_runtime.md:42` — **IP privée réelle** (réservation DHCP d'une carte) dans un **contrat métier**. Décision **propriétaire** : anonymiser l'IP, ou poser `audit:scope=doc` sur ce contrat. **Non traité ici** (contrat métier hors périmètre du lot).
2. `zigbee2mqtt/migration-4-to-5.log` — **`.log` suivi** (violation frontière + S5a). Traitement : **Lot 1E-d** (`.gitignore *.log` + désindexation, arbitrage).

**CRITICAL=0 n'est donc PAS atteint — et c'est honnête** : l'obtenir exigerait soit de masquer ces deux vrais signaux, soit d'agir hors périmètre (désindexation, modification d'un contrat métier). Conformément au principe du lot, ces deux signaux **restent visibles**.

## 7. Tests

- **`--selftest`** (juge testé) : 8 négatifs de code (`token: str`, `_G_TOKEN = re.compile(...)`, `token=line.strip()`, `RE_LAT_SECRET = …`, `password = get_password()`, …) → **non `CRITICAL`** ; 5 positifs (`API_TOKEN = "sk-…"`, `token = '…'`, `password: hunter2…` YAML, `api_key = "…"`, `Bearer …`) → **restent `CRITICAL`** ; extensions interdites `.log`/`.db`/`.key` reconnues, `.yaml`/`.py` non → **OK**.
- **Test `zigbee2mqtt/`** : le `.log` suivi remonte bien en `CRITICAL` S5 (vérifié sur corpus réel).
- **Scanner sur corpus réel** : `CRITICAL 35 → 2`, `WARNING 611 → 620` ; verdict global `CRITICAL` (attendu tant que les 2 résiduels ne sont pas traités). Mesure « avant » faite sur `origin/main` **depuis** un worktree détaché (le scanner scanne `Path.cwd()`).
- **`py_compile`** du scanner → OK.
- **Portes documentaires** (`docs_lint` + gates) → vertes (annotations `scope=doc` posées **après** le H1, R-DOC-H1-1 respecté).
- **`check_registre_chantiers`** + **`check_ci_coverage_registry`** → verts (aucun `check_*.py` ni workflow ajouté ; compteurs inchangés).

## 8. Non-actions

- **Scanner non branché en CI** (aucun workflow modifié) → Lot **1E-b**.
- **Log suivi non désindexé** ; `.gitignore` **non modifié** → Lot **1E-d** (arbitrage).
- **Historique git non assaini** (fuite GPS passée) → lot terrain dédié.
- **Contrat métier arrosage non modifié** → décision propriétaire.
- Aucun runtime YAML, aucun ID, aucun `check_config`, ni chauffage, ni AID/APD touchés.
- Aucun secret réel reproduit dans ce rapport.

## 9. Recommandation finale

Le scanner est **prêt** : faux positifs de code éliminés, angle mort levé, findings documentaires qualifiés, **vrais signaux conservés**. La baseline honnête est **`CRITICAL=2`**, pas 0.

**Avant de brancher le scanner en CI (Lot 1E-b), traiter les 2 vrais signaux :**

1. **Lot 1E-d** — `.gitignore *.log` + **désindexer** `zigbee2mqtt/migration-4-to-5.log` (arbitrage propriétaire).
2. **Décision propriétaire** sur `contrats/arrosage/08_inventaire_pont_runtime.md` — anonymiser l'IP ou poser `audit:scope=doc`.

**Puis Lot 1E-b** — brancher le scanner : d'abord **informatif** (`continue-on-error`) pour verrouiller la non-régression, puis **bloquant** (`--fail-on critical`) une fois `CRITICAL=0` réellement atteint. Le branchement bloquant **suppose** les deux actions ci-dessus faites — sinon la CI serait rouge sur des vrais signaux non résolus, ce qui est correct mais bloquerait tout push.

Le **Lot 1E-c est clos** sous réserve de confirmation par la CI GitHub (portes docs). Il n'affaiblit aucune détection et ne masque aucun vrai signal.
