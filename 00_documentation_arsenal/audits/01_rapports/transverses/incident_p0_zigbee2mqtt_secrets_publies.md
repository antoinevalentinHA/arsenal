# Incident P0 — Secrets Zigbee2MQTT publiés dans le dépôt
<!-- audit:scope=doc -->


**Date du rapport :** 2026-07-05
**Gravité :** P0 — publication de credentials et de matière de clé réseau
**Fichiers concernés :** `zigbee2mqtt/configuration.yaml`, `zigbee2mqtt/configuration_backup_v4.yaml`
**Contrat de référence :** `00_documentation_arsenal/contrats/publication/securite_publication_git.md` (v1.3.0)
**Règle absolue de ce rapport :** aucune valeur secrète n'est recopiée ici — ni dans les diffs, ni dans les messages de commit, ni dans la PR.

---

## 1. Ce qui a été exposé

Les deux fichiers Zigbee2MQTT versionnés contenaient, en clair (catégories
uniquement — les valeurs ne sont pas reproduites) :

| Élément | Contrôle censé le couvrir | Impact |
|---|---|---|
| Mot de passe du broker MQTT (compte `addons`) | S1 (`password`) / S3 | Accès au bus MQTT : lecture/écriture de tous les topics (alarme, sirène, contacts, prises) pour quiconque atteint le broker |
| Clé de chiffrement du réseau Zigbee (bloc d'octets) | aucun (lacune) | Déchiffrement et injection du trafic Zigbee à portée radio : contacts, claviers d'alarme, sirène |
| Identifiants du réseau Zigbee (PAN ID, PAN ID étendu) | aucun (lacune) | Ciblage précis du réseau (avec le canal, également en clair) |
| Numéro de série du dongle USB coordinateur | aucun (mineur) | Empreinte matérielle du coordinateur |

L'exposition vaut pour l'**état courant** et pour **tout l'historique Git** du
dépôt distant (un clone suffit à récupérer les valeurs).

---

## 2. Pourquoi le scanner n'a pas bloqué — analyse de l'écart de couverture

La défense comptait deux étages. **Les deux ont cédé, indépendamment.**

### 2.1 Étage 1 — le scanner rendait `PASS` (cause déterminante)

`zigbee2mqtt/` figurait dans `EXCLUDED_DIRS` du scanner (contrat § 3.4,
« exclusions de performance »), au même titre que `www/` et
`custom_components/`, avec la justification « tiers, hors périmètre Arsenal ».

C'est une **erreur de classification** : `www/` et `custom_components/`
contiennent du *code tiers* (bruit de faux positifs, jamais de secrets
Arsenal) ; `zigbee2mqtt/` contient de la **configuration** — précisément la
catégorie de fichiers qui porte des credentials. Résultat : les contrôles de
contenu S1–S8 n'ont **jamais** parcouru `zigbee2mqtt/configuration.yaml`, et
le verdict global du dépôt était `PASS` (vérifié : exit 0, zéro `CRITICAL`)
alors qu'un mot de passe littéral y était versionné.

L'angle mort était même **partiellement documenté** : la v1.3.0 du script
(C14 Lot 1E-c) avait constaté qu'un `.log` suivi sous `zigbee2mqtt/` échappait
au contrôle S5a et avait corrigé ce point — mais uniquement pour les noms de
fichiers interdits, pas pour le **contenu**. `configuration.yaml` n'étant pas
un nom interdit, il est resté invisible.

### 2.2 Étage 2 — le CI était informatif, pas bloquant

Le workflow `security_publication_audit.yml` (C14 Lot 1E-b) exécutait le
scanner avec `continue-on-error: true` : « ce job ne bloque JAMAIS une PR à ce
stade ». Le passage en bloquant était planifié comme « lot ultérieur ». Même
si le scanner avait détecté le secret, **rien n'aurait empêché le merge**.

### 2.3 Lacune de patterns — la clé réseau Zigbee était indétectable

Simulation faite en levant seulement l'exclusion de répertoire : les patterns
v1.3.0 n'attrapaient que le mot de passe MQTT (S1). La clé réseau Zigbee, en
**bloc YAML d'octets**, ne contient aucun mot-clé S1 (ni `token`, ni
`password`…) : elle serait passée inaperçue même sans l'exclusion. Idem pour
le PAN ID étendu. Aucun contrôle ne couvrait la matière de clé réseau.

### 2.4 Défauts aggravants relevés au passage

- **S2 « port exposé »** : la liste blanche de ports (1883, 8123…) était
  testée par lookahead *après* le match — elle ne s'appliquait donc jamais au
  port matché lui-même. Lever l'exclusion aurait produit un faux positif
  `CRITICAL` sur l'URL standard du broker (`:1883`), le genre de bruit qui
  pousse à ré-exclure un répertoire au lieu de corriger le motif.
- **Historique** : le scan `--history` n'est pas exécuté en CI, et il
  respectait lui aussi `EXCLUDED_DIRS` — aucune chance de rattrapage.
- **Combinaison user/password (S3)** : le motif exige le mot-clé `username`,
  or Zigbee2MQTT écrit `user:` — le contrôle de couple identifiant/mot de
  passe ne se serait pas déclenché non plus.

### 2.5 Synthèse

> Un répertoire de configuration exclu « pour la performance », un gate CI
> volontairement non bloquant, et une catégorie de secret sans pattern :
> chaque couche a échoué pour une raison distincte, et aucune ne compensait
> les autres. Le correctif traite les trois couches, plus un verrou de
> non-régression testé.

---

## 3. Correctifs appliqués (cette PR)

| # | Correctif | Fichier |
|---|---|---|
| 1 | `zigbee2mqtt/` retiré de `EXCLUDED_DIRS` — le contenu est scanné | `scripts/security/audit_publication_git.py` (v1.4.0) |
| 2 | Nouveau contrôle **S9 — Clés réseau Zigbee** : clé réseau / PAN ID étendu littéraux (bloc ou inline) → `CRITICAL` ; PAN ID littéral → `WARNING` ; `GENERATE` et `'!secret x'` admis | idem |
| 3 | Placeholders : `GENERATE` et forme quotée `'!secret x'` (syntaxe Zigbee2MQTT) | idem |
| 4 | Motif S2 « port exposé » : liste blanche appliquée au port matché | idem |
| 5 | Configuration réelle remplacée par un **exemple neutralisé** — bloc `devices`/`groups` conservé à l'identique (les `friendly_name`, source des IDs Home Assistant, sont inchangés) ; secrets externalisés (`'!secret …'`) ; clés réseau en `GENERATE` ; fichier de backup supprimé | `zigbee2mqtt/configuration.example.yaml` |
| 6 | Exclusions Git : la configuration réelle, ses backups et `secret.yaml` ne sont plus versionnables | `.gitignore` |
| 7 | Workflow CI **bloquant** : `--fail-on critical`, suppression de `continue-on-error`, `--selftest` + contrats en préambule | `.github/workflows/security_publication_audit.yml` |
| 8 | Tests positifs/négatifs (verrou de non-régression, fixtures factices) : l'exemple neutralisé passe ; un mot de passe MQTT littéral échoue (S1) ; une clé réseau littérale échoue (S9) ; périmètre, hygiène Git et gate CI vérifiés (Z1–Z7) | `scripts/security/check_publication_zigbee2mqtt_contracts.py` |

État vérifié après correctifs : `--selftest` OK, contrats Z1–Z7 OK (11/11),
scan complet du dépôt = **0 `CRITICAL`**, exit 0.

---

## 4. Actions restantes hors dépôt (opérateur)

La purge du dépôt **ne révoque rien** : les valeurs restent valides côté
runtime et lisibles dans l'historique Git distant.

**Statut (2026-07-07) — risque accepté par décision opérateur, non réalisées :**
rotation MQTT, rotation clé réseau Zigbee et purge d'historique **ne sont
pas exécutées**. Justification opérateur : l'exposition est jugée limitée au
réseau local — atteindre le broker MQTT ou le trafic radio Zigbee suppose
déjà une intrusion sur le réseau local, un niveau d'accès qui rendrait la
plupart des autres protections secondaires. **Déclencheur de réouverture** :
tout changement de surface d'exposition (accès distant au broker, réseau
invité/IoT non cloisonné, clone du dépôt distant sorti du contrôle de
l'opérateur, ou publication future d'un secret exploitable à distance).

1. **Rotation du mot de passe MQTT** du compte `addons`
   (broker Mosquitto), puis report de la nouvelle valeur dans
   `zigbee2mqtt/secret.yaml` **local** (non versionné, désormais gitignoré).
   — **non faite, risque accepté** (cf. ci-dessus).
2. **Rotation de la clé réseau Zigbee** : décision d'opérateur — changer la
   clé impose de ré-appairer l'ensemble des 66 périphériques. Tant que la
   rotation n'est pas faite, le trafic Zigbee reste déchiffrable par
   quiconque a lu le dépôt et se trouve à portée radio.
   — **non faite, risque accepté** (cf. ci-dessus).
3. **Purge de l'historique Git** (`git filter-repo` ou BFG sur les deux
   fichiers, puis force-push et invalidation des clones/forks) : décision
   séparée — sans elle, l'invariant du contrat (« un CRITICAL en historique
   bloque ») s'appliquera au premier scan `--history`.
   — **non faite, risque accepté** (cf. ci-dessus).
4. **Runtime local** : ce dépôt supprime `zigbee2mqtt/configuration.yaml` du
   suivi Git. Si le runtime synchronise le dépôt par `git pull`, **préserver
   ou restaurer le fichier local réel** après synchronisation (il est
   désormais gitignoré : Git ne le touchera plus ensuite). Aucune nouvelle
   configuration opérationnelle n'est inventée ici : l'exemple versionné est
   volontairement non fonctionnel tel quel.

---

## 5. Invariants réaffirmés

- Les IDs Home Assistant (`friendly_name` du parc Zigbee) sont inchangés.
- Aucune valeur secrète ne figure dans ce rapport, les diffs ou les messages.
- Le juge est testé avant d'être appliqué (`--selftest` + Z1–Z7 en CI, avant
  le scan bloquant).
- Toute nouvelle exclusion de répertoire du scan de contenu doit désormais
  répondre à la question : « ce répertoire peut-il contenir de la
  configuration ? » — si oui, elle est interdite (contrat § 3.4, v1.3.0).
