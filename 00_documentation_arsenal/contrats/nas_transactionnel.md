# Contrat — Socle transactionnel des commandes NAS Arsenal

**Version** : v1.1.1
**Statut** : proposé / non implémenté

> **v1.1.0 — clarification pré-Lot A (2026-09-09).** Fermeture des ambiguïtés
> identifiées avant le Lot A d'admission (chantier C51) : ajout du champ
> `expires_at` au schéma de commande (§6), traitement explicite d'un
> `request_id` connu non terminal (§7, §9.4) et d'un `request_id` réutilisé
> avec un payload incompatible (§7, nouveau verdict `rejected_conflict`,
> §10.1), fail-closed sur ledger illisible (nouveau verdict
> `admission_unavailable`, §7, §10.1), verrouillage de l'invariant de
> crash-consistency (§9.5), et convergence explicite du `run_id` unique
> (§9.2). Aucun mécanisme d'implémentation n'est fixé par cette révision
> (probe-then-release, recovery de ledger, réconciliation concrète restent
> ouverts au design). Purement additif — aucun retrait, aucune
> renumérotation de section.

> **v1.1.1 — correction d'une contradiction interne §7/§8 (2026-09-09).**
> L'ordre normatif d'admission (§7 v1.1.0) évaluait la fraîcheur
> (`expires_at`, alors point 3) **avant** la consultation du `request_id`
> connu (alors point 4) : une redelivery QoS 1 d'un `request_id` déjà
> **terminal**, survenant après `expires_at`, était rejetée
> `rejected_stale` avant toute relecture du ledger — en contradiction
> directe avec l'idempotence de commande fixée par le §8 (« une redelivery
> ne crée jamais une seconde exécution ») et avec l'invariant de
> crash-consistency du §9.5 (« `expires_at` ne requalifie jamais une
> demande déjà admise »). Correction : dans l'ordre normatif du §7, la
> consultation du `request_id` connu (désormais point 3) précède
> désormais la fraîcheur (désormais point 4), qui ne gouverne plus que
> l'admissibilité d'un `request_id` **inconnu**. Un `request_id` déjà
> connu — terminal ou `admitted` — n'est plus jamais rejeté
> `rejected_stale`. Renumérotation des seuls points internes du §7 (les
> renvois §6, §9.4, §11 sont mis à jour en conséquence) ; aucun verdict,
> aucune section, aucune autre sémantique C51 n'est ajouté, retiré ou
> modifié par cette révision.

**Périmètre** : direction **Home Assistant → NAS** — admission et corrélation
des commandes `AUDIT` et `RELEASE_DIFF`. Ne couvre ni la logique des moteurs,
ni la projection MQTT existante NAS→HA.
**Chantier** : [`audits/04_chantiers/transverses/c51_commandabilite_nas.md`](../audits/04_chantiers/transverses/c51_commandabilite_nas.md)
**Contrats liés** :
- [`switchbot_transactionnel.md`](./switchbot_transactionnel.md) — précédent transactionnel réutilisé (grammaire de verdict, phases, `request_id`)
- [`arsenal_nas.md`](./arsenal_nas.md) — consommation HA du résultat RELEASE_DIFF (non modifié par ce contrat)
- [`arsenal_self.md`](./arsenal_self.md) — consommation HA du résultat AUDIT (non modifié par ce contrat)
- [`outils_externes/nas_arsenal/diff/diff_release.md`](../outils_externes/nas_arsenal/diff/diff_release.md) — moteur RELEASE_DIFF (souverain sur sa spécialisation)
- [`outils_externes/nas_arsenal/diff/release_diff_mqtt.md`](../outils_externes/nas_arsenal/diff/release_diff_mqtt.md) — projection MQTT RELEASE_DIFF existante
- [`outils_externes/nas_arsenal/audit/audit.md`](../outils_externes/nas_arsenal/audit/audit.md) — moteur AUDIT (souverain sur sa spécialisation)
- [`outils_externes/nas_arsenal/audit/mqtt.md`](../outils_externes/nas_arsenal/audit/mqtt.md) — projection MQTT AUDIT existante

---

## 1. Objet

Le présent contrat définit le **socle transactionnel commun** permettant à
Home Assistant/Arsenal de demander au NAS l'exécution d'une opération métier
existante, et de corréler de façon fiable cette demande à son exécution et à
sa terminaison.

Il couvre exclusivement la **direction de commande** (HA → NAS). La direction
inverse — état et événements du résultat métier (NAS → HA) — est déjà
contractualisée par `arsenal_nas.md`/`release_diff_mqtt.md` et
`arsenal_self.md`/`audit/mqtt.md`, et n'est pas modifiée ici.

---

## 2. Phrase centrale

> Ce contrat fixe **comment une demande devient une exécution corrélable**.
> Il ne dit jamais **ce que produit** cette exécution — c'est la propriété
> exclusive des contrats moteur et de leurs projections MQTT existantes.

---

## 3. Périmètre

### 3.1 Couvert par ce contrat

- Vocabulaire fermé des opérations demandables.
- Identité de la demande (`request_id`).
- Admission ou rejet d'une demande.
- Idempotence de la demande (déduplication, mémoire persistante bornée).
- Attribution du `run_id` et sa corrélation stable au `request_id`.
- Grammaire de terminaison **transactionnelle** (technique), distincte du
  résultat métier.
- Politique générique de concurrence (`BUSY`), déclinée par opération dans
  le chantier C51.
- Invariants de sécurité minimaux du canal de commande.

### 3.2 Hors contrat

- La sémantique de génération du diff (`diff_release.md`) ou du verdict
  d'audit (`audit.md`).
- Le format exact et le contenu des payloads d'état/événement NAS→HA
  (`release_diff_mqtt.md`, `audit/mqtt.md`) — inchangés par ce contrat.
- Le mécanisme de supervision technique du listener NAS (Docker, tâche DSM
  au démarrage, ou autre) — non normatif ici.
- L'identité MQTT concrète (compte, ACL) — déterminée après audit du
  broker, hors périmètre documentaire.
- La décision d'agir (UI, automatisation planifiée) — relève du backend
  Arsenal, pas de ce contrat.

---

## 4. Frontière d'autorité

| Couche | Autorité | Ne produit pas |
|---|---|---|
| Backend Arsenal | Demande (`request_id`, opération) | N'exécute rien, ne décide jamais du résultat |
| Admission NAS | Admission, déduplication, concurrence, attribution du `run_id` | Ne réinterprète jamais le vocabulaire reçu |
| Moteur (AUDIT ou RELEASE_DIFF) | Exécution et résultat métier, selon son propre contrat | Ne décide pas de l'admission ni de la concurrence globale |
| Domaines HA `arsenal_self`/`arsenal_nas` | Consommation et diagnostic du résultat déjà publié | Ne recalculent jamais le verdict ni le `run_id` |

Le NAS reste seul autorité d'admission, d'exécution, de concurrence et de
résultat. Home Assistant n'est jamais autorité de résultat — clause
préservée sans exception par ce contrat.

---

## 5. Vocabulaire fermé des opérations

| Opération | Chaîne métier existante (souveraine, non modifiée) |
|---|---|
| `AUDIT` | Extraction, contrôle de stabilité, audit patrimonial, publication — contrat [`audit/audit.md`](../outils_externes/nas_arsenal/audit/audit.md) |
| `RELEASE_DIFF` | Génération de diffs sémantiques inter-releases, mode batch consécutif uniquement — contrat [`diff/diff_release.md`](../outils_externes/nas_arsenal/diff/diff_release.md) |

Aucune autre valeur n'est admissible. Aucun paramètre métier libre
(`--couple`, chemin, argument shell) n'est transmis par la commande. Toute
extension de ce vocabulaire est une révision majeure du présent contrat,
jamais une tolérance d'implémentation.

---

## 6. Identité de commande

Une commande porte au minimum :

- `request_id` — identifiant unique attribué par le backend Arsenal, unique
  par demande (pas par opération) ;
- `operation` — l'opération demandée, prise dans le vocabulaire fermé du §5 ;
- `ts` — horodatage d'émission ;
- `expires_at` — horodatage de péremption de la commande, fourni par le
  backend Arsenal ;
- `source` — utilisateur ou automatisation, à des fins diagnostiques.

Le `request_id` est la seule identité que le backend Arsenal contrôle. Il ne
préjuge d'aucune identité d'exécution.

**Autorité sur `expires_at`.** `expires_at` est une valeur **fournie par
Arsenal, validée par le NAS** — jamais une identité d'exécution, jamais une
délégation d'autorité de décision. Le NAS reste seul autorité d'admission
(§4) : il ne fait pas confiance à `expires_at` tel quel, il le valide (forme,
cohérence avec `ts`, plage jugée raisonnable) avant de l'opposer à la
commande — voir §7 point 4. Le NAS ne substitue **jamais** silencieusement
`expires_at` par une fenêtre de fraîcheur globale (TTL NAS) qui ignorerait la
valeur transmise par Arsenal ; un garde-fou NAS supplémentaire, s'il existe,
est un contrôle additionnel explicite, pas un remplacement.

---

## 7. Admission

L'admission est un acte NAS. Une commande y est reçue et évaluée selon un
ordre normatif strict, à la manière de la Phase 0 du socle
[`switchbot_transactionnel.md`](./switchbot_transactionnel.md) §9 :

0. Mémoire d'idempotence (§8, le « ledger ») lisible et exploitable de façon
   fiable → sinon échec fermé de l'admission, **avant tout autre point de
   contrôle** : verdict `admission_unavailable` (§10.1). Un ledger illisible
   ou corrompu n'est **jamais** traité comme un ledger vide — l'admission
   n'a pas les moyens de savoir si un `request_id` a déjà été vu, elle ne
   peut donc décider pour aucune commande tant que la lecture n'est pas
   restaurée. Aucune nouvelle exécution, aucun `run_id`, aucun écrasement du
   ledger par un ledger vide ne sont jamais produits sous ce verdict. Le
   mécanisme de restauration (réparation, remplacement, intervention
   manuelle) est un choix d'implémentation, non fixé par ce contrat.
1. Opération dans le vocabulaire fermé du §5 → sinon rejet
   `rejected_precondition`.
2. Payload bien formé (`request_id` présent, forme valide) → sinon rejet
   `rejected_precondition`.
3. `request_id` déjà connu dans le ledger (§8) — ce point est évalué **avant**
   la fraîcheur (point 4) : un `request_id` déjà enregistré ne redevient
   **jamais** une nouvelle demande du seul fait de l'écoulement du temps ;
   la fraîcheur (point 4) ne décide que de l'admissibilité d'un `request_id`
   **inconnu**.
   a. présenté avec une `operation` ou des champs d'identité incompatibles
      avec la demande déjà enregistrée sous ce `request_id` → rejet
      `rejected_conflict` (§10.1). Incohérence de demande — aucune nouvelle
      exécution, aucun nouveau `run_id`, quel que soit par ailleurs l'état
      terminal ou non de l'enregistrement existant.
   b. sinon, déjà **terminal** (`completed`/`technical_failure`, §10.2) →
      réponse par relecture du résultat déjà produit, jamais par une
      nouvelle exécution — **y compris si `expires_at` est désormais
      dépassé** : la fraîcheur ne s'oppose jamais à un `request_id` déjà
      connu.
   c. sinon, **non terminal** (`admitted`, `run_id` déjà attribué, transaction
      non close) → **aucune réadmission, aucun nouveau `run_id`, aucun
      nouvel appel du wrapper métier, et jamais `rejected_stale`.**
      L'admission relit et retourne l'état `admitted` déjà connu, associé au
      `run_id` déjà attribué, sans jamais invoquer le moteur pour cette
      demande. Voir §9.4 (réconciliation) pour ce qui détermine, hors chaîne
      d'admission, la vivacité réelle de ce `run_id`.
4. `request_id` **inconnu** du ledger (point 3) : fraîcheur de la commande —
   `expires_at` (§6) non dépassé et contraintes temporelles NAS satisfaites
   (cohérence de forme, cohérence avec `ts`, plage jugée admissible) →
   sinon rejet `rejected_stale`. Une commande est stale dès que l'une de ces
   contraintes temporelles n'est pas satisfaite, pas seulement en cas de
   dépassement strict de `expires_at`. Un `request_id` déjà connu (point 3)
   n'atteint jamais ce point et ne peut donc jamais être rejeté
   `rejected_stale`.
5. `request_id` inconnu, opération demandée déjà en cours (§11) → rejet
   `rejected_busy`. Aucun `run_id` n'est attribué et aucun wrapper métier
   n'est invoqué pour cette demande.

**Invariant.** Un rejet d'admission (points 0 à 2, 3a, 4 et 5) n'ouvre
**jamais** de transaction : aucun verrou n'est posé, aucun `run_id` n'est
attribué, aucun wrapper métier n'est invoqué, aucune trace transactionnelle
n'est créée au-delà du rejet lui-même. Le point 3c (non terminal) n'ouvre pas
non plus de nouvelle transaction : il relit un état déjà ouvert, sans jamais
en créer un second.

---

## 8. Idempotence de commande

Le NAS tient une **mémoire persistante et bornée** des `request_id` traités,
distincte des mémoires d'idempotence métier existantes
(`state/processed_backups.json`, `state/processed_releases.json`, qui
portent l'idempotence du **traitement**, pas celle de la **commande**).

- Une redelivery MQTT QoS 1 du même `request_id` ne crée jamais une seconde
  exécution : le résultat déjà produit est relu et retourné.
- La mémoire survit au redémarrage du listener (persistée sur disque, pas
  seulement en mémoire volatile) — une redelivery après restart doit
  toujours être reconnue.
- La forme concrète de cette mémoire (fichier, taille, TTL) est un choix
  d'implémentation, non tranché par ce contrat.

Ne pas confondre : l'idempotence d'un backup déjà traité (SHA identique,
statut `ok`) et l'idempotence d'une commande MQTT (`request_id` déjà connu)
sont deux mécanismes distincts, à deux niveaux distincts.

---

## 9. Corrélation `request_id` ↔ `run_id`

### 9.1 Définitions

- **`request_id`** — identité de la **demande** Arsenal. Attribué par le
  backend, avant toute admission.
- **`run_id`** — identité de l'**exécution NAS effectivement admise**.
  Attribué par l'admission NAS, **après** admission réussie et **avant**
  l'entrée dans le moteur métier.

### 9.2 Règles

- Un rejet d'admission (§7) ne crée jamais de `run_id`.
- Une même redelivery du même `request_id` ne crée jamais un nouveau
  `run_id` : elle relit le `run_id` déjà associé et son résultat.
- Un `request_id` admis est associé de façon **stable et durable** à son
  `run_id` — l'association ne change jamais après attribution.
- Le `run_id` est le pivot qui relie la **terminaison transactionnelle**
  (§10) au **résultat métier** publié par ailleurs (§11).
- **Convergence stricte.** Le `run_id` attribué par l'admission est, sans
  exception, le même `run_id` transmis au moteur/wrapper métier et publié
  dans le résultat (AUDIT/RELEASE_DIFF, via `arsenal_self`/`arsenal_nas`).
  Aucune seconde identité d'exécution n'est générée en aval de l'admission,
  à quelque étape que ce soit — ni par le wrapper, ni par le moteur, ni par
  la publication du résultat.

### 9.3 Ce que ce contrat ne fixe pas

Le format concret du `run_id` et de l'`event_id`, tel que spécifié par
[`diff/release_diff_mqtt.md`](../outils_externes/nas_arsenal/diff/release_diff_mqtt.md)
pour RELEASE_DIFF, reste une spécialisation moteur, non fixée ici. Le
mécanisme actuel — où `run_id` est généré à l'intérieur du moteur
`release_diff.py`, décrit par
[`diff/diff_release.md`](../outils_externes/nas_arsenal/diff/diff_release.md)
et producteur du fichier support `release_diff_last_run.json` — devra
évoluer pour devenir compatible avec le présent contrat, par révision de
`diff/release_diff_mqtt.md`. Un futur contrat équivalent reste à définir
pour AUDIT (inexistant aujourd'hui). La relecture opportuniste d'un unique fichier
« dernier run » n'est **jamais** considérée comme une preuve
transactionnelle suffisante en présence de concurrence — c'est précisément
la limite que le présent contrat corrige en déplaçant l'attribution du
`run_id` en amont du moteur.

### 9.4 Réconciliation d'un `request_id` non terminal

Un `request_id` déjà connu, associé à un `run_id`, mais dont la transaction
n'est pas close (verdict `admitted` persistant, §10.2) ne peut jamais, par
simple redelivery, être réadmis (§7 point 3c) : l'admission relit cet état,
elle ne le retranche ni ne le prolonge.

Déterminer si l'exécution sous-jacente est toujours réellement active, ou si
l'enregistrement `admitted` est orphelin (processus producteur disparu, par
exemple après un crash), n'est **pas** une décision de l'admission — c'est
une logique de réconciliation/diagnostic distincte de la chaîne normale
d'admission du §7. Son issue possible (laisser courir, marquer
`technical_failure`, ou bloquer en sécurité dans l'attente d'une
intervention) et son déclenchement concret (détection de processus vivant,
délai d'observation, intervention manuelle) sont des choix d'implémentation,
non fixés par ce contrat. Le présent contrat fixe uniquement l'invariant
qui les encadre : voir §9.5.

### 9.5 Invariant de crash-consistency

Dès qu'une association `request_id` → `run_id` a été persistée dans le
ledger (§8), **aucune** redelivery ultérieure de ce `request_id` — MQTT
QoS 1, retry applicatif, ou tout autre chemin — ne peut jamais produire un
second `run_id`. Cette propriété est absolue, y compris si le processus
d'admission ou le moteur métier crashe entre la persistance de l'association
et la clôture de la transaction.

Une entrée `admitted` orpheline doit être réconciliée (§9.4) ou rester
bloquée en sécurité. Elle ne peut **jamais** être transformée en nouvelle
admission par expiration de `expires_at` ou par toute autre logique de TTL :
`expires_at` (§6) gouverne l'admission d'une **nouvelle** demande (§7), il
ne requalifie jamais une demande déjà admise.

---

## 10. Terminaison transactionnelle

Deux familles de terminaison, strictement disjointes, sur le modèle de la
grammaire de verdict du socle SwitchBot :

### 10.1 Famille rejet (hors transaction)

Produite par le §7. Aucun `run_id`, aucun verrou.

| Verdict | Signification |
|---|---|
| `rejected_precondition` | Opération inconnue, payload malformé, ou hors vocabulaire fermé |
| `rejected_stale` | Commande hors fenêtre de fraîcheur (`expires_at` dépassé ou contrainte temporelle NAS non satisfaite) — uniquement pour un `request_id` **inconnu** du ledger (§7 point 4) ; un `request_id` déjà connu n'est jamais rejeté sous ce verdict (§7 point 3) |
| `rejected_busy` | Opération déjà en cours (`request_id` inconnu du ledger) |
| `rejected_conflict` | `request_id` déjà connu, présenté avec une `operation` ou des champs d'identité incompatibles avec la demande déjà enregistrée sous ce `request_id` |
| `admission_unavailable` | Ledger d'idempotence (§8) illisible ou corrompu — l'admission ne peut évaluer aucune demande tant que la lecture n'est pas restaurée |

**Nature distincte d'`admission_unavailable`.** Les quatre autres verdicts de
cette famille sont produits après évaluation complète de la demande
présentée : ils la refusent. `admission_unavailable` n'évalue rien — il
signale que l'admission elle-même est hors d'état de décider, pour
**toute** demande, indépendamment de son contenu. Il partage néanmoins la
propriété structurelle de la famille (§7, invariant) : aucune transaction
n'est ouverte, aucun `run_id` n'est attribué.

### 10.2 Famille résultat de transaction (dans transaction)

Produite uniquement après admission réussie et attribution du `run_id`.

| Verdict | Signification |
|---|---|
| `admitted` | Commande admise, `run_id` attribué, exécution non encore terminale |
| `completed` | Le moteur a produit un résultat exploitable, quel que soit le verdict métier (succès, alerte, partiel) |
| `technical_failure` | Le moteur a échoué techniquement — aucun résultat métier exploitable |

**Invariant central (§12)** : `completed` ne dit **rien** du résultat
métier. Une transaction `completed` peut corréler un résultat métier `ok`,
`alert`, `partial` ou `error` — ces valeurs restent exclusivement définies
par `arsenal_self.md`/`arsenal_nas.md` et leurs contrats MQTT.

---

## 11. Concurrence

Politique générique, déclinée précisément par opération dans le chantier
C51 :

- Une commande reçue pour une opération déjà en cours d'exécution est
  rejetée `rejected_busy` (§10.1) — jamais mise en file, jamais coalescée.
- L'admission d'une opération n'est jamais bloquée par l'exécution en
  cours de l'**autre** opération, sauf invariant partagé démontré (aucun
  identifié à ce jour — voir chantier C51 §8).
- Le verrou garantissant l'exclusion mutuelle intra-opération est une
  responsabilité NAS, réutilisant/durcissant les mécanismes déjà en place
  plutôt que d'en créer un second et incompatible.

**Ce que ce contrat fixe, et ce qu'il ne fixe pas encore.** Le contrat fixe
le **résultat** : une opération déjà en cours produit `rejected_busy`, sans
`run_id` attribué et sans qu'aucun wrapper métier soit invoqué pour cette
demande (§7 point 5). Il ne fige **pas** encore le mécanisme concret de
coordination avec le verrou déjà en place (par ex. `flock`) — notamment un
éventuel schéma probe-then-release — qui reste à démontrer au design
d'implémentation. Cette coordination ne doit en aucun cas créer une seconde
autorité de verrouillage concurrente de celle déjà en place : elle la
réutilise ou la durcit, jamais ne la double.

---

## 12. Séparation stricte transaction / résultat métier

Cette séparation est l'invariant le plus important du présent contrat.

- Le vocabulaire de terminaison transactionnelle (§10) et le vocabulaire de
  résultat métier (`ok`/`alert`/`error` pour AUDIT,
  `ok`/`partial`/`error` pour RELEASE_DIFF) ne partagent **aucun** champ,
  **aucune** valeur, **aucun** nom.
- Une transaction `completed` n'implique jamais un résultat métier
  favorable.
- Une future implémentation physique des topics MQTT (fusion ou séparation
  des plans transaction et état) est un choix d'optimisation de transport,
  laissé ouvert par ce contrat — mais la séparation **sémantique** reste
  non négociable, quelle que soit l'implémentation physique retenue.

---

## 13. Sécurité minimale

- Vocabulaire fermé (§5) : rien d'autre n'est interprété par l'admission.
- Aucun argument shell arbitraire transmis par Arsenal.
- Le canal de commande est **non retenu** (`retain=false`) — un
  redémarrage du broker ne doit jamais rejouer une commande périmée.
  Contraste assumé avec les topics état existants, retenus par conception
  (`release_diff_mqtt.md` §6.2, `audit/mqtt.md` §6).
- Extension proposée, cohérente avec le namespace déjà déclaré extensible
  par `release_diff_mqtt.md` §6.1 (`arsenal/nas/<job>/state`,
  `arsenal/nas/<job>/event`) : un troisième plan `arsenal/nas/<job>/command`
  — proposition à valider à l'implémentation, pas un engagement définitif
  de ce contrat.
- Déduplication applicative (§8), en sus du QoS MQTT.
- Identité MQTT dédiée au canal de commande recommandée par moindre
  privilège (distincte des identités de publication d'état) — le compte
  concret n'est pas choisi ici.
- ACL du broker vérifiées avant toute activation terrain — prérequis
  d'implémentation, non bloquant pour ce contrat.

---

## 14. Diagnostic minimal

L'admission NAS doit exposer en permanence :

| Champ | Écrit à | Description |
|---|---|---|
| `last_request_id` | Admission | Dernier `request_id` ayant franchi l'admission |
| `last_operation` | Admission | Dernière opération admise |
| `last_run_id` | Attribution du `run_id` | Dernier `run_id` attribué |
| `last_transaction_verdict` | Terminaison ou rejet | Dernier verdict produit, toute famille confondue |
| `last_ts` | Terminaison ou rejet | Horodatage de clôture ou de rejet |

Ce diagnostic est distinct des entités de résultat métier existantes
(`arsenal_self`, `arsenal_nas`) et ne les remplace pas.

---

## 15. Frontières exclues

Le présent contrat ne fait pas :

- la génération de diffs ou de verdicts d'audit ;
- la définition ou la modification des états métier existants ;
- la définition du format physique final des topics de commande ;
- le choix du mécanisme de supervision du listener NAS ;
- l'attribution d'une identité MQTT concrète ;
- la décision d'agir (UI, automatisation) — c'est le backend Arsenal, hors
  périmètre de ce contrat.

---

## 16. Extensibilité

L'ajout d'une future opération au-delà de `AUDIT`/`RELEASE_DIFF` est une
révision majeure de ce contrat (§5), jamais une tolérance d'implémentation.
Le mécanisme d'admission, de corrélation et de terminaison défini ici est
conçu pour rester valide sans modification lors d'un tel ajout ; seul le
vocabulaire fermé du §5 est révisé.

---

## 17. Gouvernance

Toute modification du vocabulaire fermé, de la grammaire de terminaison
transactionnelle, ou de la règle de corrélation `request_id`↔`run_id`
nécessite une évolution versionnée du présent contrat.

Toute modification du résultat métier ou de sa projection MQTT relève
exclusivement de `arsenal_self.md`/`audit/mqtt.md` (AUDIT) ou
`arsenal_nas.md`/`release_diff_mqtt.md` (RELEASE_DIFF) — jamais du présent
contrat.

---

*Fin du contrat — Socle transactionnel des commandes NAS Arsenal v1.1.1.*
