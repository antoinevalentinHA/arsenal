# CONTRAT — Sécurité publication Git

**Référence :** `documentation_arsenal/contrats/publication/securite_publication_git.md`
**Version :** v1.4.0
**Statut :** Normatif
**Scope :** Arsenal — audit pré-publication

---

## Journal des versions

| Version | Modifications |
|---|---|
| v1.0.0 | Version initiale |
| v1.0.1 | Corrections script uniquement (bugs) — contrat inchangé |
| v1.1.0 | Annotations `audit:ignore` / `audit:scope=doc` ; placeholders numériques ; S5 affiné ; exclusions de performance formalisées |
| v1.2.0 | **C14 Lot 1E-c — réduction des faux positifs, sans affaiblir la détection.** S1 : en fichier de **code**, un mot-clé secret n'est `CRITICAL` que si sa valeur est un **littéral chaîne quoté** (les identifiants/types/appels — `token: str`, `_G_TOKEN = re.compile(...)` — ne sont plus des secrets ; les valeurs codées en dur `API_TOKEN = "…"` restent `CRITICAL`). S5a : le contrôle des **fichiers interdits** porte désormais sur les fichiers **versionnés** (`git ls-files`) de tout l'arbre, **indépendamment de `EXCLUDED_DIRS`** — lève l'angle mort `zigbee2mqtt/` (un `.log` suivi y échappait) ; un artefact runtime **non suivi** (gitignoré) n'est pas signalé. S2/S3 : `.home-assistant.io` n'est plus lu comme domaine local ; `synology.<ext>` (nom de fichier) n'est plus lu comme accès distant. Ajout d'un `--selftest`. Script : v1.2.0 → **v1.3.0**. |
| v1.3.0 | **Incident P0 — secrets Zigbee2MQTT publiés.** Périmètre : `zigbee2mqtt/` **retiré des exclusions § 3.4** — répertoire de configuration porteuse de credentials, classé à tort « tiers » ; cette exclusion a produit un verdict `PASS` sur un mot de passe MQTT littéral et une clé réseau Zigbee versionnés. Nouveau contrôle **S9 — Clés réseau Zigbee** : `network_key` / `ext_pan_id` littéraux (bloc YAML ou inline) → `CRITICAL` ; `pan_id` littéral → `WARNING` ; formes admises : `GENERATE` et `'!secret x'`. Placeholders § 3.5 : ajout de `GENERATE` et de la forme **quotée** `'!secret x'` (syntaxe Zigbee2MQTT). S2 : liste blanche de ports appliquée au **port matché lui-même** (l'ancien lookahead ne neutralisait jamais `:1883`). CI : le workflow d'audit devient **bloquant** (`--fail-on critical`, plus de `continue-on-error`), précédé de `--selftest` et des contrats `check_publication_zigbee2mqtt_contracts.py`. Rapport : `audits/01_rapports/transverses/incident_p0_zigbee2mqtt_secrets_publies.md`. Script : v1.3.0 → **v1.4.0**. |
| v1.4.0 | **C32 — dé-identification des prénoms enfants.** Nouveau contrôle **S7 — Prénoms enfants** (`arnaud` / `matthieu`), l'un des « noms propres nominatifs » listés en § 9. Après le chantier C32 (Chambre Arnaud → Chambre Enfants, Chambre Matthieu → Salle de Jeux ; suivi enfants fusionné), aucun prénom d'enfant ne doit revenir dans le **runtime** : détection `\b(arnaud\|matthieu)\b` → `CRITICAL` en fichier de runtime (verrou anti-retour), `WARNING` en documentation active (`.md`/`.txt` — mentions historiques « ex- » des contrats), **hors périmètre** pour l'historique gelé (`00_documentation_arsenal/changelog/`, `…/audits/`). En historique Git (`--history`) : `WARNING` — les prénoms passés subsistent, leur purge relève d'un `git filter-repo` (cf. S6). Script : v1.4.0 → **v1.5.0**. |

---

## 1. Objet

Ce contrat définit les règles de détection des informations sensibles dans le dépôt Arsenal avant toute publication publique (GitHub, fork, archive partagée). Il gouverne le script `scripts/security/audit_publication_git.py` et ses évolutions.

---

## 2. Principe fondamental

> **L'audit est bloquant, pas décoratif.**

| Verdict global | Condition | Conséquence |
|---|---|---|
| `PASS` | Aucun signal détecté | Publication techniquement autorisée |
| `WARNING` | Au moins un signal ambigu ou contextuel | **Revue manuelle obligatoire** avant publication |
| `CRITICAL` | Au moins un secret ou exposition avérée | **Publication interdite** |

Un seul `CRITICAL` suffit à bloquer. Les `WARNING` ne se cumulent pas automatiquement en `CRITICAL` — la décision appartient au mainteneur.

> **Le contrat s'adapte au système réel, pas l'inverse.**
> Un faux positif identifié et justifié doit conduire à une évolution du contrat,
> pas à une dégradation de la documentation Arsenal.

---

## 3. Périmètre de scan

### 3.1 Fichiers scannés (état courant)

- Tous les fichiers texte du dépôt, récursivement depuis la racine
- Extensions auditées en **présence** uniquement (pas en contenu) : `.db`, `.log`, `.key`, `.pem`, `.crt`, `.env`
- Les fichiers binaires (détectés par présence d'octets nuls) sont ignorés
- Les fichiers de taille supérieure à 2 Mo sont ignorés

### 3.2 Historique Git (optionnel, flag `--history`)

- Scan via `git rev-list --all` + `git grep` par commit
- Un secret supprimé de l'état courant mais présent dans l'historique reste un `CRITICAL` — il sera visible après `git clone`
- Les hits historiques sont libellés `(historique Git)` dans le rapport
- Déduplication par `(fichier, ligne, pattern)` : un secret présent dans N commits génère un seul finding

### 3.3 Exclusions légitimes

Les fichiers suivants sont exclus du scan (contiennent les patterns par construction) :

```
security_audit_report.md
documentation_arsenal/contrats/publication/securite_publication_git.md
scripts/security/audit_publication_git.py
```

Ces exclusions sont codées en dur dans le script. Elles ne sont pas configurables.

### 3.4 Exclusions de performance

Les répertoires suivants sont ignorés par le walker (contenu non scanné).
Justification : tiers (code externe) ou générés, hors périmètre Arsenal.

```
.git/
__pycache__/
.venv/  venv/
node_modules/
.mypy_cache/  .pytest_cache/
www/
custom_components/
```

> Ces répertoires ne sont **pas** dans FORBIDDEN_DIRS : leur présence n'est pas interdite,
> leur contenu est simplement hors périmètre d'audit.

> **v1.2.0 :** cette exclusion ne vaut que pour le scan de **contenu** (S1–S8).
> La détection des **fichiers interdits (S5a)** porte désormais sur les fichiers
> **versionnés** de tout l'arbre, y compris ces répertoires — un `.log` suivi
> sous `zigbee2mqtt/` est donc bien signalé.

> **v1.3.0 — leçon de l'incident P0 :** `zigbee2mqtt/` est **retiré** de cette
> liste. Seul du **code tiers** peut être exclu du scan de contenu ; un
> répertoire de **configuration** (credentials, clés réseau) ne le peut jamais,
> quelle que soit sa provenance. L'exclusion de `zigbee2mqtt/` a produit un
> verdict `PASS` alors que `zigbee2mqtt/configuration.yaml` versionnait un mot
> de passe MQTT littéral et la clé du réseau Zigbee.

### 3.5 Placeholders reconnus

Les valeurs suivantes ne déclenchent pas de verdict sur les contrôles S1–S4.
Vérification effectuée **ligne par ligne** (un placeholder sur une ligne n'immunise pas les autres lignes du même fichier).

**Placeholders textuels :**
```
""  ''  null  ~  none
YOUR_*  CHANGEME  REDACTED  PLACEHOLDER
example  dummy  test  sample  demo
!secret <nom>          # référence HA secrets.yaml — valeur externalisée
'!secret <nom>'        # idem, forme QUOTÉE (syntaxe Zigbee2MQTT) — v1.3.0
GENERATE               # Zigbee2MQTT : clé/PAN générés au premier démarrage — v1.3.0
```

**Placeholders numériques** (codes d'exemple conventionnels) :
```
1234  0000  9999  12345  000000
```

Effet : `alarm_code: 1234` → `WARNING` au lieu de `CRITICAL`.
Rationale : le script détecte la **structure**, pas la valeur. Un code placeholder signale
une structure sensible sans certifier qu'il s'agit d'un vrai secret.

---

## 4. Annotations d'exception

Les annotations permettent au mainteneur de qualifier explicitement un signal
sans modifier le contenu fonctionnel. Elles sont **déclaratives et traçables** —
un signal annoté reste visible dans le rapport avec son annotation.

> Ces annotations ne sont pas des mécanismes de silence aveugle.
> Elles déplacent la responsabilité vers le mainteneur qui les pose.

### 4.1 `# audit:ignore` — exception par ligne

Syntaxe : annotation en fin de ligne active.

```yaml
ping_host: 192.168.1.1  # audit:ignore — IP exemple dans contrat ping_lan
```

Comportement : la ligne est sautée avant toute analyse. Aucun finding n'est généré.

Règles d'usage :
- Réservé aux faux positifs avérés et justifiés
- La justification doit figurer après `audit:ignore —`
- Un `audit:ignore` sans justification est invalide (le script émet un `WARNING` de forme)

### 4.2 `# audit:scope=doc` — exception par fichier

Syntaxe : annotation sur l'une des 5 premières lignes du fichier.

```markdown
<!-- audit:scope=doc -->
# Contrat ping LAN
```

ou en YAML :

```yaml
# audit:scope=doc
# Contrat : ping_lan_synthese.md
```

Comportement : tous les `CRITICAL` du fichier sont dégradés en `WARNING`.
Les `WARNING` existants sont conservés. Le rapport indique `[scope=doc]` pour chaque finding affecté.

Règles d'usage :
- Réservé aux fichiers **entièrement documentaires** : contrats, changelogs, architecture, guides
- Interdit sur les fichiers de configuration runtime (`.yaml` HA actifs, `configuration.yaml`, ESPHome)
- Le mainteneur assume que le fichier ne contient aucun secret opérationnel

Fichiers Arsenal légitimement éligibles :
```
00_documentation_arsenal/**/*.md
00_documentation_arsenal/**/*.txt
```

Fichiers explicitement non éligibles :
```
configuration.yaml
esphome/*.yaml
secrets.yaml
```

---

## 5. Contrôles

### S1 — Secrets évidents · `CRITICAL`

Patterns recherchés (insensibles à la casse, après suppression des commentaires de fin de ligne) :

| Pattern | Libellé |
|---|---|
| `token\s*[:=]\s*\S+` | token |
| `password\s*[:=]\s*\S+` | password |
| `api_key\s*[:=]\s*\S+` | api_key |
| `bearer\s+[a-zA-Z0-9\-._~+/]+=*` | bearer |
| `secret\s*[:=]\s*\S+` | secret |
| `client_secret\s*[:=]\s*\S+` | client_secret |
| `webhook\s*[:=]\s*https?://\S+` | webhook |
| `refresh_token\s*[:=]\s*\S+` | refresh_token |

**Seuil :** toute correspondance avec une valeur non-placeholder → `CRITICAL`

> **v1.2.0 — contexte de code.** Dans un fichier de **code**
> (`.py`, `.sh`, `.js`, `.ts`, …), un mot-clé S1 n'est retenu que si sa valeur
> est un **littéral chaîne quoté** (`API_TOKEN = "…"`). Un identifiant, un type
> ou un appel (`token: str`, `_G_TOKEN = re.compile(...)`, `token=line.strip()`)
> n'est **pas** un secret et n'est plus signalé. Les fichiers **non-code**
> (YAML, `.md`, `.txt`) conservent le seuil ci-dessus (une valeur non quotée
> peut être un vrai secret). Motivation : § 2 — un faux positif justifié fait
> évoluer la détection, pas la documentation.

---

### S2 — Réseau / Exposition · `CRITICAL` ou `WARNING`

| Pattern | Verdict |
|---|---|
| IP privée `192.168.x.x` | `CRITICAL` |
| IP privée `10.x.x.x` | `CRITICAL` |
| IP privée `172.16-31.x.x` | `CRITICAL` |
| URL vers domaine `.home` / `.local` / `.lan` / `.internal` / `.localdomain` | `CRITICAL` |
| Port explicite hors `80`, `443`, `8080`, `8123`, `1883`, `5353` | `CRITICAL` |
| URL `http://` ou `https://` vers domaine non-local (≥ 8 caractères, non déjà `CRITICAL`) | `WARNING` |

---

### S3 — MQTT / NAS / SSH · `CRITICAL` ou `WARNING`

| Condition | Verdict |
|---|---|
| `broker\s*[:=]` + valeur non-placeholder | `CRITICAL` |
| `username` **et** `password` présents dans le même fichier, valeurs non-placeholder (vérifié ligne par ligne) | `CRITICAL` |
| Accès distant : `rsync://`, `ssh://`, URL ou hostname Synology | `CRITICAL` |
| Topic MQTT contenant `alarm`, `code` ou `presence` (dans un bloc `platform: mqtt`) | `WARNING` |
| Mot `synology` ou `nas` dans une valeur non-placeholder | `WARNING` |

---

### S4 — Sécurité domestique · `CRITICAL` ou `WARNING`

| Pattern | Verdict |
|---|---|
| `alarm_code\s*[:=]\s*\d+` (valeur non-placeholder numérique) | `CRITICAL` |
| `bssid\s*[:=]` + adresse MAC | `CRITICAL` |
| `(arm\|disarm)` + `(code\|pin)` + valeur numérique sur la même ligne | `CRITICAL` |
| Termes `alarme`, `clavier`, `intrusion` dans une valeur | `WARNING` |
| Présence nominative dans un contexte de présence (`antoine` + `presence`) | `WARNING` |

---

### S5 — Fichiers et répertoires interdits · `CRITICAL`

#### 5a — Fichiers interdits (par nom / extension)

Présence dans le dépôt (même vide) :

```
secrets.yaml
*.key  *.pem  *.crt  *.env
*.db   *.log
```

> **v1.2.0 :** « présence dans le dépôt » = fichier **versionné** (`git ls-files`),
> évalué sur **tout l'arbre** indépendamment des exclusions de § 3.4. Un fichier
> interdit **local non suivi** (gitignoré) ne sera pas publié et n'est donc pas
> signalé.

#### 5b — Répertoires interdits (par nature, pas uniquement par nom)

Un répertoire est interdit S5 si son **nom ET son contexte** correspondent à un répertoire de sauvegarde système ou d'export runtime.

| Nom | Contexte interdit | Contexte autorisé |
|---|---|---|
| `.storage/` | Toute profondeur | — |
| `backups/` | Racine ou premier niveau ; ou contenant `.db`, `.log`, `.tar`, `.gz`, `.zip` | Sous-répertoire métier Arsenal ne contenant que du YAML fonctionnel |

> **Faux positif identifié (v1.0.0) :** `04_input_texts/ecs/backups/` est un répertoire
> métier Arsenal contenant des helpers YAML. Son nom est générique mais son contenu
> n'est pas sensible. La règle nominative pure de v1.0.0 était trop agressive.
> La règle v1.1 exige contexte + contenu pour qualifier l'interdiction.

Détection : `scan_forbidden_dirs()` parcourt ROOT indépendamment du walker,
pour ne pas dépendre de `EXCLUDED_DIRS`.

---

### S6 — Historique Git · héritage du contrôle parent

- Mode défaut : scan de l'état courant uniquement (S1–S5)
- Flag `--history` : relance S1–S4 sur tous les commits via `git rev-list --all`
- Chaque hit historique hérite du verdict du contrôle qui l'a détecté
- Libellé dans le rapport : `(historique Git)`
- Les annotations `audit:ignore` et `audit:scope=doc` de l'état courant **ne s'appliquent pas** à l'historique

> Un `CRITICAL` détecté dans l'historique bloque la publication **même si corrigé dans l'état courant**.
> La suppression du secret doit se faire via `git filter-repo` ou équivalent.

---

### S7 — Prénoms enfants (dé-identification) · `CRITICAL` ou `WARNING`

Implémenté en script v1.5.0 (chantier **C32** : dé-identification des prénoms enfants après le renommage
Chambre Arnaud → Chambre Enfants / Chambre Matthieu → Salle de Jeux et la fusion du suivi enfants).
Sous-ensemble **concret** des « noms propres nominatifs » de § 9. **Verrou anti-retour** : après C32, aucun
prénom d'enfant ne doit revenir dans le **runtime**.

| Contexte du fichier | Verdict |
|---|---|
| **Runtime** (YAML de config, code) | `CRITICAL` — une régression de dé-identification bloque la publication |
| **Documentation active** (`.md` / `.txt`) | `WARNING` — mentions historiques « ex- » des contrats, à accepter en revue |
| **Historique gelé** (`00_documentation_arsenal/changelog/`, `…/audits/`) | hors périmètre — le record conserve légitimement les prénoms |

Détection : `\b(arnaud\|matthieu)\b` (insensible à la casse). En historique Git (`--history`) : `WARNING`
— les prénoms passés subsistent dans l'historique ; leur purge relève d'un `git filter-repo` (cf. S6),
arbitrage distinct. Le scanner **s'auto-exclut** (§ 3.3) : sa liste de prénoms ne se signale pas.

---

### S8 — Coordonnées GPS · `CRITICAL` ou `WARNING`

Implémenté en script v1.2.0 (fuite des coordonnées du domicile dans `17_zones/`).

| Forme | Verdict |
|---|---|
| Clé `latitude` / `longitude` + valeur décimale (`:`/`=`/`\|`) | `CRITICAL` |
| Paire de décimales haute précision adjacentes (forme narrative/GeoJSON) | `CRITICAL` |
| Décimale isolée à signature GPS (≥ 6 décimales, filet heuristique) | `WARNING` |

L'externalisation `!secret` (placeholder § 3.5) est la parade fonctionnelle.

---

### S9 — Clés réseau Zigbee · `CRITICAL` ou `WARNING`

Implémenté en script v1.4.0 (incident P0 : `network_key` réelle versionnée dans
`zigbee2mqtt/configuration.yaml`). La clé réseau Zigbee chiffre tout le trafic
domotique (alarme, contacts, sirène) : sa publication permet de le déchiffrer
et d'y injecter des commandes. Elle ne matche **aucun** mot-clé S1, d'où un
contrôle dédié.

| Forme | Verdict |
|---|---|
| `network_key` / `ext_pan_id` **en bloc YAML** (clé seule en fin de ligne : la liste d'octets suit) | `CRITICAL` |
| `network_key` / `ext_pan_id` **inline** avec valeur littérale non-placeholder | `CRITICAL` |
| `pan_id` inline avec valeur littérale non-placeholder | `WARNING` |
| Valeur `GENERATE` ou `'!secret <nom>'` | aucun signal |

> Un en-tête de bloc est signalé **par construction** : les seules formes
> légitimement versionnables étant `GENERATE` et `'!secret x'` (inline),
> une valeur vide introduisant un bloc est nécessairement de la matière de clé.

---

## 6. Format de sortie

### 6.1 Console

```
❌ [CRITICAL ] S1 — config/integrations/mqtt.yaml:12 — password
⚠️  [WARNING  ] S3 — packages/network.yaml:4 — référence NAS en valeur  [scope=doc]
✅ [PASS]  S1-S6 — aucun signal détecté
```

**Codes de retour :**

| Code | Signification |
|---|---|
| `0` | PASS global, ou WARNING avec `--fail-on critical` |
| `1` | WARNING présent (avec `--fail-on warning`, défaut) |
| `2` | CRITICAL présent |

### 6.2 Rapport Markdown

Fichier : `security_audit_report.md` à la racine du dépôt.

Ce fichier **ne doit pas être versionné** (à ajouter dans `.gitignore`).

Le rapport est **toujours régénéré intégralement** — jamais appendé.

Structure :

```
# Rapport d'audit sécurité — Arsenal
Tableau : date, commit HEAD, historique activé, verdict global
## Résumé (comptages par sévérité)
## Détail par contrôle (S1–S6)
## Fichiers concernés
## Recommandations
_Pied de page : version du script_
```

---

## 7. Intégration CI

```yaml
# GitHub Actions — bloquant sur CRITICAL, tolérant sur WARNING
- name: Audit sécurité publication
  run: python scripts/security/audit_publication_git.py --fail-on critical

# GitHub Actions — bloquant sur WARNING aussi (mode strict)
- name: Audit sécurité publication (strict)
  run: python scripts/security/audit_publication_git.py --fail-on warning
```

Le code de retour `2` fait échouer le pipeline. Le code `1` peut être configuré selon la politique du moment via `--fail-on`.

---

## 8. Invariants

- Le script **ne modifie jamais** le dépôt
- Le rapport est toujours régénéré intégralement (pas d'append)
- Un `CRITICAL` en historique Git bloque même si corrigé dans l'état courant
- Les exclusions légitimes (§ 3.3) sont codées en dur dans le script, non configurables
- Les lignes vides et les commentaires purs (`# …`) sont ignorés par le scanner
- La partie commentaire de fin de ligne est retirée avant analyse, **sauf** détection d'annotation `audit:ignore`
- Un `audit:ignore` sans justification génère un `WARNING` de forme
- Les annotations de l'état courant ne s'appliquent pas à l'historique Git
- `scan_forbidden_dirs()` est indépendante du walker — elle n'est pas affectée par `EXCLUDED_DIRS`

---

## 9. Évolutions prévues

| Ref | Description | Statut |
|---|---|---|
| S7 | Prénoms enfants dé-identifiés (`arnaud` / `matthieu`) — verrou anti-retour ; sous-ensemble concret des « noms propres nominatifs » | **implémenté** (script v1.5.0, § 5/S7) |
| S8 | Coordonnées GPS (`latitude`, `longitude`, zone `home`) | **implémenté** (script v1.2.0, § 5/S8) |
| S9 | Clés réseau Zigbee (`network_key`, `ext_pan_id`, `pan_id`) | **implémenté** (script v1.4.0, § 5/S9) |
| S10 | Intégration `pre-commit` hook local (ex-S9 de v1.1) | prévu |
| S11 | Rapport JSON machine-readable pour intégration CI avancée | prévu |

---

## 10. Fichiers associés

| Fichier | Rôle |
|---|---|
| `scripts/security/audit_publication_git.py` | Implémentation v1.4.0 |
| `scripts/security/check_publication_zigbee2mqtt_contracts.py` | Contrats positifs/négatifs publication Zigbee2MQTT (verrou incident P0) |
| `.github/workflows/security_publication_audit.yml` | Branchement CI **bloquant** (`--fail-on critical`) |
| `zigbee2mqtt/configuration.example.yaml` | Exemple Zigbee2MQTT neutralisé — seul artefact z2m versionné |
| `security_audit_report.md` | Rapport généré (non versionné) |
| Ce fichier | Contrat normatif |

---

*Fin de contrat v1.1.0*
