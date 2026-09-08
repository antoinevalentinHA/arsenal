# Contrat — Socle transactionnel des commandes NAS Arsenal

**Version** : v1.0.0
**Statut** : proposé / non implémenté
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
- l'opération demandée, prise dans le vocabulaire fermé du §5 ;
- un horodatage d'émission ;
- une source (utilisateur ou automatisation), à des fins diagnostiques.

Le `request_id` est la seule identité que le backend Arsenal contrôle. Il ne
préjuge d'aucune identité d'exécution.

---

## 7. Admission

L'admission est un acte NAS. Une commande y est reçue et évaluée selon un
ordre normatif strict, à la manière de la Phase 0 du socle
[`switchbot_transactionnel.md`](./switchbot_transactionnel.md) §9 :

1. Opération dans le vocabulaire fermé du §5 → sinon rejet.
2. Payload bien formé (`request_id` présent, forme valide) → sinon rejet.
3. Fraîcheur de la commande dans une fenêtre de validité définie à
   l'implémentation → sinon rejet.
4. `request_id` déjà connu et déjà terminal (§9) → réponse par relecture du
   résultat déjà produit, jamais par une nouvelle exécution.
5. Opération demandée déjà en cours (§11) → rejet `BUSY`.

**Invariant.** Un rejet d'admission (points 1 à 3, et le rejet `BUSY` du
point 5) n'ouvre **jamais** de transaction : aucun verrou n'est posé, aucun
`run_id` n'est attribué, aucune trace transactionnelle n'est créée au-delà
du rejet lui-même.

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

---

## 10. Terminaison transactionnelle

Deux familles de terminaison, strictement disjointes, sur le modèle de la
grammaire de verdict du socle SwitchBot :

### 10.1 Famille rejet (hors transaction)

Produite par le §7. Aucun `run_id`, aucun verrou.

| Verdict | Signification |
|---|---|
| `rejected_precondition` | Opération inconnue, payload malformé, ou hors vocabulaire fermé |
| `rejected_stale` | Commande hors fenêtre de fraîcheur |
| `rejected_busy` | Opération déjà en cours |

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

*Fin du contrat — Socle transactionnel des commandes NAS Arsenal v1.0.0.*
