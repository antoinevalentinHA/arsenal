# Chantier CHAUFFAGE (C48) — Convergence documentaire et gouvernance de la migration Boiler Bridge → Boilerack

| Champ | Valeur |
|---|---|
| **Chantier** | Gouverner et clore documentairement la migration Boiler Bridge → Boilerack, techniquement terminée et validée terrain. Aligner la documentation Arsenal sur l'état réel de production, référencer (sans les exécuter) les correctifs documentaires dus côté dépôt public Boilerack, et parquer explicitement les dettes guard hors périmètre. |
| **Domaine** | Chauffage / boiler — déborde vers ECS (rôle `dhw_setpoint`) et vers la couche transverse « écosystème des dépôts satellites ». Rangé sous `chauffage/`, comme la migration elle-même (`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`). |
| **Statut** | **Ouvert (2026-09-06) — Axe A complet (13/13 : A1–A13). Bloqué sur Axe B (dépôt externe Boilerack, hors gouvernance Arsenal). Voir §9.** |
| **Priorité** | P2 — aucun risque fonctionnel ; le runtime est stabilisé et validé terrain. Enjeu de gouvernance et de cohérence documentaire uniquement. |
| **Ouvert le** | 2026-09-06. |
| **Registre** | Chantier **C48** — ① Actifs, cf. [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Source normative amont** | [`../../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md) v8 — §16 prononce la **clôture fonctionnelle** du recâblage runtime. C48 ne rouvre pas ce jugement : il gouverne ce que cette clôture laisse en dette **documentaire**. |

> **⚠️ Portée de cette ouverture.** Strictement documentaire et de gouvernance.
> Aucune entité, script, garde, automatisation, checker ou dashboard n'est créé,
> modifié ou retiré par ce document. Aucun accès au Raspberry Pi. Aucun
> déploiement. Aucune modification du dépôt Boilerack (dépôt externe, hors
> gouvernance directe de cette session). **Aucun changelog créé** — voir §7.

---

## 1. Contexte acquis — état terrain au 2026-09-06

La migration Boiler Bridge → Boilerack est **techniquement terminée et validée
terrain** :

- **Boilerack** est l'écrivain souverain actif en production.
- `boilerack.service` est `enabled` et `active`.
- `boiler_bridge.service` historique est `disabled` et `inactive`.
- Le guard historique est en **v1.3** et cible par défaut `boilerack.service`.
- Le **Lot 1 guard/systemd** a été audité indépendamment, mergé, déployé et
  validé terrain.
- Boilerack est resté actif **sans redémarrage** pendant le déploiement du
  guard.
- Le chauffage est resté fonctionnel de bout en bout.
- **Aucun runtime Arsenal versionné** ne peut réactiver ou commander l'ancien
  bridge.
- La **garde fonctionnelle HA par rôle** (garde composée du §7 du contrat
  central chauffage, cf. `30_decision_centrale__amendement_garde_execution.md`)
  est déjà **en production**.

Ce constat recoupe la **clôture fonctionnelle** prononcée au §16 de
`migration_boiler_bridge_vers_boilerack.md` : les quatre rôles d'écriture
(`dhw_setpoint`, `heating_setpoint`, `heating_curve_shift`,
`heating_curve_slope`) y sont éprouvés en production (épreuves A-5 à A-8).

### 1.1 Micro-audit terrain complémentaire — le `Conflicts=` du drop-in

Un micro-audit terrain, postérieur à la clôture fonctionnelle du §16, a établi
les faits suivants :

- `Conflicts=boiler_bridge.service` est chargé depuis un **drop-in**
  `/etc/systemd/system/boilerack.service.d/10-exclusion.conf`, et **non** du
  fragment principal `boilerack.service`.
- Ce drop-in est **persistant** sur l'instance déployée.
- `install.py` de Boilerack **ne touche jamais** au répertoire `.service.d`.
- Une réinstallation normale de Boilerack **conserve donc** ce `Conflicts=`.
- **Aucune correction runtime n'est nécessaire** sur ce point.

**Verdict terrain final : PERSISTANT — chantier documentaire uniquement.**
Ce fait est réel, terrain, et non versionné dans le fragment principal du
service — il doit être **documenté en tant que tel**, sans jamais prétendre
qu'il est porté par le gabarit `systemd/boilerack.service` du dépôt public
(Axe B, lot B7).

---

## 2. Audits de référence

Deux audits cloud de convergence, conduits en amont de l'ouverture de ce
chantier, en forment la base probatoire. Ils ne sont pas des fichiers du
dépôt Arsenal (analyses de session, non versionnées) ; leurs conclusions
opposables sont reprises ici et dans la roadmap §4.

### 2.1 Audit Boilerack (dépôt public)

Verdict : **prêt techniquement, pas prêt documentairement.**

Constats retenus : README et index design encore en posture « en
construction » ; en-tête de `systemd/boilerack.service` présentant l'unité
comme jamais chargée sur un vrai systemd ; `Development Status :: 1 -
Planning` ; absence de documentation publique de migration, exploitation,
vérification, diagnostic, rollback, topics MQTT ; absence de première
version/tag correspondant à l'état homologué ; `Conflicts=` réel non
documenté ni dans le corpus interne (« C12 » du dépôt Boilerack) ni dans le
gabarit systemd, alors que sa persistance face à `install.py` est désormais
démontrée (§1.1) ; aucune dette technique du guard jugée bloquante au point
d'arrêt actuel.

### 2.2 Audit Arsenal (ce dépôt)

Verdict : **cohérent après documentation.**

Constats retenus : runtime HA déjà cohérent avec Boilerack souverain, aucun
chantier runtime Arsenal nécessaire ; documentation à deux vitesses ;
plusieurs documents présentent encore `boiler_bridge` comme runtime de
production ; `outils_externes/boiler_pi/*` est la zone la plus obsolète ;
`contrats/chauffage/30_decision_centrale__amendement_garde_execution.md`
affirme encore que la garde composée n'est pas en service alors qu'elle
l'est (vérifié en §6.3 du document — voir Axe A, lot A1) ;
`architecture/ecosysteme_depots_satellites.md` ignore Boilerack (vérifié —
voir Axe A, lot A3) ; aucune gouvernance Arsenal formelle ne portait la
migration avant C48 (pas de chantier, pas d'entrée registre, pas de
changelog — migration techniquement close mais non gouvernée) ; les dettes
guard (`RC_PROBE`, axe MQTT 3b, panne Boilerack non détectée directement)
peuvent être parquées (Axe C).

---

## 3. Doctrine de la présente ouverture

Le but de C48 n'est **pas** de corriger immédiatement tous les fichiers
identifiés. Cette ouverture pose le périmètre, la roadmap et les critères de
clôture ; l'exécution des lots (Axe A, A1 à A13) est **hors périmètre de la
présente ouverture** et fera l'objet de travaux ultérieurs, chantier par
chantier ou lot par lot, sous ce même C48.

---

## 4. Périmètre — trois axes

### Axe A — Arsenal (ce dépôt)

Aligner la documentation Arsenal sur l'état réel de production. Roadmap
finie, lot par lot :

| Lot | Fichier(s) | Contradiction / manque | Correction minimale attendue | Dépendances | Critère de clôture du lot |
|---|---|---|---|---|---|
| **A1** | `contrats/chauffage/30_decision_centrale__amendement_garde_execution.md` §6.3 | Affirme que la garde composée « n'a pas encore d'implémentation […] elle n'est pas en service » — faux au terrain | Réviser §6.3 pour constater le passage en service ; ne pas réécrire les seuils/décisions normatives des §2/§3 | — | §6.3 reflète l'état terrain, reste du document inchangé — **LIVRÉ (#783, 2026-09-06)** |
| **A2** | `contrats/chauffage/30_decision_centrale.md` §7 | Référence un signal unique `binary_sensor.boiler_bridge_online`, non absorbé par l'amendement | Aligner la référence de signal sur la garde composée par rôle, sans dupliquer le contenu normatif de l'amendement | A1 | §7 ne contredit plus son propre amendement — **LIVRÉ (#783, 2026-09-06)** |
| **A3** | `architecture/ecosysteme_depots_satellites.md` (tableau §1, fiche §4.6, tableau de synthèse §3) | Ignore Boilerack ; décrit `boiler-bridge` comme seul satellite actif du domaine boiler | Ajouter Boilerack comme satellite gouverné actif ; requalifier `boiler-bridge` comme satellite historique désactivé (sans supprimer sa fiche) | — | Le document nomme Boilerack comme écrivain souverain actif ; `boiler-bridge` reste tracé comme historique — **LIVRÉ (#782, 2026-09-06)** |
| **A4** | `outils_externes/boiler_pi/{README,architecture,guard,mqtt,workflow}.md` | Zone la plus obsolète (audit 2.2) : décrit `arsenal-boiler-bridge`/vcontrold comme service actif | Basculer la posture en « historique, désactivé » ; pointer vers Boilerack et son dépôt ; documenter le guard v1.3 et sa cible par défaut | A3 | Aucun de ces documents ne décrit `boiler-bridge` comme actif — **LIVRÉ (#782, 2026-09-06)** |
| **A5** | `navigation/domaines/boiler.md`, `navigation/domaines/chauffage.md` | Le hub boiler pointe le bus MQTT chaudière vers `boiler-bridge` comme producteur vivant | Réorienter le renvoi producteur vers Boilerack ; conserver `interface_ha_boiler_bridge.md` comme contrat d'adaptation HA existant | A3, A4 | Les hubs orientent vers Boilerack comme source de vérité — **LIVRÉ (#782, 2026-09-06)** |
| **A6** | `contrats/boiler/{README,socle_transactionnel,mqtt_ack_ha,script_executif,retry_transactionnel,guard_exposition_ha,consommation_ack}.md` | Corpus HA-side rédigé à l'époque du pont historique | Revue de cohérence : nommer Boilerack comme écrivain amont là où le texte présume `boiler_bridge` actif ; invariants transactionnels déjà éprouvés (ACK, `request_id`) non retouchés | A3 | Le corpus `contrats/boiler/` ne présume plus `boiler_bridge` actif — **LIVRÉ (#783, 2026-09-06)** |
| **A7** | `schemas_ascii/regulation_thermique.md` | Schéma ASCII de pipeline probablement daté au pont historique | Mettre à jour le pipeline visuel (bridge → Boilerack), sans changer la sémantique du schéma | A3 | Le schéma reflète le pipeline réel — **LIVRÉ (ce commit, 2026-09-06)** |
| **A8** | `architecture/03_doctrines/commandabilite.md`, `architecture/volets.md`, `contrats/chauffage/20_triggers_decisionnels.md`, `contrats/chauffage/20_triggers_decisionnels__amendement.md`, `contrats/ecs/application_consigne.md` | Mentions résiduelles de `boiler_bridge` non vérifiées une par une | Vérification ligne à ligne ; correction uniquement si le texte affirme `boiler_bridge` actif | A3 | Chaque fichier vérifié ; correction ou constat « sans objet » consigné — **LIVRÉ (ce commit, 2026-09-06)** |
| **A9** | `contrats/ping_lan_synthese.md` | Référence probable à `binary_sensor.boiler_bridge` (ping ICMP) | **Vérification seule** — cette entité est explicitement conservée par le cadrage de migration (§8) ; a priori aucune correction | — | Constat explicite « entité conservée, aucune correction » — **LIVRÉ (ce commit, 2026-09-06)** |
| **A10** | `README.md` / `README.fr.md` (légende de la capture `systeme-boiler-bridge.png`) | À vérifier : la légende nomme une carte UI, pas nécessairement l'autorité runtime | Corriger seulement si le texte affirme une autorité runtime erronée | — | Constat explicite, correction si nécessaire seulement — **LIVRÉ (ce commit, 2026-09-06)** |
| **A11** | `audits/index.md`, `audits/01_rapports/documentation/{rapport_ecosysteme_depots_satellites,cartographie_chaines_documentaires_arsenal,audit_navigation_documentation_arsenal,audit_documentaire_global_2026_06_06}.md` | Anciens constats P3 sur le domaine boiler non rattachés à la migration | **Rattachement seul** (pointeur daté vers C48), jamais réécriture de rapports figés | A3–A9 | Chaque constat P3 pertinent porte un pointeur vers C48, ou est explicitement parqué — **LIVRÉ (ce commit, 2026-09-06)** |
| **A12** | `REGISTRE_CHANTIERS.md` | Migration technique close mais non gouvernée | Ligne C48 ajoutée en ① Actifs | — | **Fait à l'ouverture — cf. §5** |
| **A13** | Changelog | Doctrine interdit la fabrication d'un changelog hors dépôt de diffs par l'opérateur | **Aucune action changelog dans ce chantier** — cf. §7 | — | Constat explicite consigné : traçabilité par commit/PR + ligne registre |

**Ordre d'exécution initialement proposé** (hors périmètre de l'ouverture) :
A3 → A4 / A5 (dépendent de la requalification du satellite) → A1 / A2
(contrat) → A6 / A7 / A8 / A9 / A10 (vérifications ciblées) → A11
(rattachement). **Suivi (§9)** : les treize lots (A1–A13) sont livrés dans cet
ordre, A7 → A11 au même commit que le présent rattrapage. **Axe A est
complet.**

### Axe B — Boilerack (dépôt externe public)

**Non modifié depuis cette session.** Le tableau suivant documente et
référence les lots dus côté Boilerack ; leur exécution relève d'une session
ultérieure ouverte sur ce dépôt, pas de C48.

| Lot | Manque constaté (audit 2.1) | Correction attendue côté Boilerack | Ordre |
|---|---|---|---|
| **B1** | README en posture « en construction » | Refléter la posture réelle : écrivain souverain actif en production | 1 |
| **B2** | Index design idem | Idem | 1 |
| **B3** | En-tête `systemd/boilerack.service` dit « jamais chargé sur un vrai systemd » | Corriger : `enabled`/`active` en production | 2 |
| **B4** | `Development Status :: 1 - Planning` | Requalifier le classifieur de maturité | 2 |
| **B5** | Absence de doc migration / exploitation / vérification / diagnostic / rollback / topics MQTT | Produire ces documents | 3 |
| **B6** | Absence de tag correspondant à l'état homologué | Émettre une première version | 4 (après B1–B5) |
| **B7** | `Conflicts=boiler_bridge.service` non documenté dans le gabarit ni dans le corpus interne, persistance face à `install.py` démontrée (§1.1) mais non écrite | Documenter factuellement le drop-in `10-exclusion.conf` et sa persistance, **sans** prétendre qu'il est porté par le fragment principal `boilerack.service` | 3 |

### Axe C — dettes explicitement parquées

Consignées ici sans être ouvertes ; elles ne deviennent pas des
sous-chantiers par effet de bord :

- panne Boilerack non détectée **directement** par le guard ;
- `RC_PROBE` ;
- sous-axe MQTT 3b ;
- escalade / reboot du guard ;
- renommage cosmétique `boiler_bridge_*` ;
- durcissement systemd optionnel.

**Réveil** : sur demande explicite de l'opérateur, ou sur incident réel les
concernant. Aucune échéance opposable n'est fixée — ce ne sont pas des
microscopes probatoires (cf. doctrine C44), mais des dettes de confort
hors périmètre.

---

## 5. Ce que cette ouverture fait, précisément

- Crée le présent document.
- Ajoute la ligne **C48** à `REGISTRE_CHANTIERS.md`, section ① Actifs.
- Ne modifie **aucun** autre document métier (Axe A, lots A1–A11 : hors
  périmètre de cette ouverture).
- Ne modifie pas Boilerack (Axe B : référencé, non exécuté).
- N'ouvre aucun sous-chantier sur l'Axe C.

---

## 6. Interdictions (rappel, opposables à tout lot futur de C48)

Aucun changement runtime · aucun accès au Raspberry Pi · aucun redémarrage ·
aucun déploiement · aucune modification de Boilerack depuis une session
Arsenal · aucun nouveau contrat technique inventé · aucun ID de chantier
inventé · aucun élargissement vers Guard Lot 2 · aucun nettoyage cosmétique
opportuniste.

---

## 7. Changelog — non créé, par doctrine

Conformément à
[`architecture/03_doctrines/redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md)
§1 : *« Ne jamais fabriquer ni numéroter un changelog de sa propre
initiative pour acter un changement […]. Hors du déclenchement [dépôt de
diffs de release par l'opérateur], un changement livré se trace via le
commit de merge / la PR dans les contrats et la ligne de clôture du
registre, jamais via un changelog inventé. »*

**Aucun changelog n'est créé par C48, à aucun de ses lots**, sauf si
l'opérateur déclenche explicitement la procédure standard (dépôt de diffs
dans `changelog/diffs_temporaires/` + demande de rédaction) à l'occasion
d'une release portant tout ou partie des lots A1–A13. La traçabilité de C48
repose sur : cette ligne de registre, les commits/PR de chaque lot, et la
mise à jour de statut de ce document au même commit que chaque lot livré
(règle de gouvernance n°1 du registre).

---

## 8. Critères de clôture de C48

Le chantier est déclarable clos quand :

1. Arsenal ne décrit plus `boiler_bridge` comme écrivain actif (Axe A,
   lots A3–A10) ;
2. Boilerack se décrit correctement comme runtime de production (Axe B,
   lots B1–B4 — hors dépôt Arsenal, vérifié par renvoi) ;
3. le rôle respectif Arsenal / Boilerack / guard / bridge historique est
   explicite dans la documentation Arsenal (Axe A, lots A3–A5) ;
4. la garde composée HA est documentée comme réellement en service
   (Axe A, lots A1–A2) ;
5. le `Conflicts=` terrain est documenté sans prétendre qu'il est versionné
   dans le fragment principal (Axe B, lot B7 ; §1.1 du présent document) ;
6. la persistance du drop-in face à `install.py` est explicitée (Axe B,
   lot B7 ; §1.1) ;
7. la migration est présente dans le registre Arsenal (fait à l'ouverture,
   §5) ;
8. la traçabilité de C48 repose sur le registre et les commits/PR, **sans
   changelog fabriqué** (§7) ;
9. les anciens constats P3 sont rattachés ou explicitement parqués
   (Axe A, lot A11) ;
10. les dettes guard hors périmètre sont documentées comme parquées
    (Axe C, §4) ;
11. aucun nouveau développement runtime n'a été introduit par C48, à aucun
    de ses lots.

---

## 9. Journal des lots livrés

> **Note de rattrapage.** La règle de gouvernance n°1 (§7) impose la mise à
> jour de statut de ce document au même commit que chaque lot livré. Les PR
> #782 et #783 ne l'ont pas fait. Le présent §9 et les mises à jour de
> statut/tableau ci-dessus corrigent cet oubli, à la ligne du registre
> mise à jour au même commit — sans réécrire l'historique des PR déjà
> mergées.

### Lots A3 / A4 / A5 — livrés (#782, 2026-09-06)

- **A3** — `architecture/ecosysteme_depots_satellites.md` : Boilerack ajouté
  comme satellite gouverné actif (fiche §4.6, « écrivain souverain actif »),
  `boiler-bridge` requalifié historique (fiche renumérotée §4.7, service
  `disabled`/`inactive`) ; le **guard de supervision externe reste hébergé
  par le dépôt `boiler-bridge`, préservé comme composant actif (v1.3)** —
  la requalification ne porte que sur le rôle d'écrivain, pas sur le guard.
- **A4** — les 5 documents `outils_externes/boiler_pi/{README,architecture,
  guard,mqtt,workflow}.md` basculent en posture historique pour le service
  de pont. `guard.md` documente désormais explicitement la **version
  normative v1.1 du document** distincte de la **version terrain déployée
  v1.3**, et la **cible par défaut `boilerack.service`** (historiquement
  `boiler_bridge.service`). `workflow.md` ajoute une mise en garde : le
  rollback est une opération explicite, pas un chemin de déploiement normal.
- **A5** — `navigation/domaines/boiler.md` nomme Boilerack écrivain souverain
  actif et `boiler-bridge` historique. `navigation/domaines/chauffage.md`
  audité, aucune contradiction trouvée, non modifié.

Aucun ID/entité renommé, aucun contrat technique touché, aucun runtime,
aucun changelog.

### Lots A1 / A2 / A6 — livrés (#783, 2026-09-06)

- **A1** — `30_decision_centrale__amendement_garde_execution.md` §6.3 : la
  réserve « garde composée pas en service » est barrée et levée, avec preuve
  terrain (`12_template_sensors/boiler/telemetry_status.yaml` dérive les
  quatre `binary_sensor.boiler_commandable_<rôle>` sur les quatre conditions
  exactes du §2 ; les 4 scripts exécutifs concernés préconditionnent
  l'émission sur ce composé). §§2/3 (seuils, décisions normatives) non
  réécrits.
- **A2** — `30_decision_centrale.md` (§6, §7, §8 diagramme, §9 table) :
  les 4 occurrences internes réconciliées avec l'amendement, sans dupliquer
  sa définition normative.
- **A6** — `contrats/boiler/{README,socle_transactionnel,script_executif}.md`
  alignés sur Boilerack écrivain souverain et sur la garde composée
  réellement consommée par les scripts exécutifs (précondition de
  commandabilité, pas seulement `bridge_online`). `mqtt_ack_ha.md`,
  `retry_transactionnel.md`, `guard_exposition_ha.md` et
  `consommation_ack.md` étaient déjà amendés (C48 ouverture) — zéro diff.

Vérifié contre le runtime réel (template sensors, scripts exécutifs,
`decision_centrale.yaml`) avant correction. Aucun ID/entité renommé, aucun
seuil normatif réécrit, aucun invariant transactionnel touché, aucun
runtime modifié.

### Lots A7 à A11 — livrés (ce commit, 2026-09-06)

- **A7** — `schemas_ascii/regulation_thermique.md` (schéma non normatif) :
  « `script.chauffage_appliquer_consigne -> protocole local (boiler bridge)` »
  devient « `-> écrivain souverain (Boilerack)` » ; « `G2 bridge offline
  (binary_sensor.boiler_bridge_online=off)?` » devient « `G2 garde
  d'exécution composée KO (binary_sensor.boiler_bridge_online nécessaire,
  non suffisant seul)` », alignée sur le libellé réel de
  `30_decision_centrale.md` §8 (déjà corrigé au lot A2) ; la mention « G2
  bridge » du §[N0] override devient « G2 exécution ». Note historique
  ajoutée en pied de fichier. Sémantique du schéma inchangée.
- **A8** — vérification ligne à ligne des 5 fichiers :
  - `architecture/03_doctrines/commandabilite.md` §7 : la table des
    réalisations décrivait `binary_sensor.boiler_bridge_online` comme
    « capacité d'exécution du pont chaudière » avec usage « gate de décision
    (`!= on → STOP`) » — silencieux sur le caractère composé de la garde
    (A1/A2). Corrigé pour nommer l'écrivain souverain (Boilerack),
    l'`entity_id` hérité conservé par doctrine, et le statut nécessaire-non-
    suffisant de la garde.
  - `contrats/chauffage/20_triggers_decisionnels.md` : en-tête de section
    « CAPACITÉ D'EXÉCUTION — INFRASTRUCTURE BOILER BRIDGE » renommé
    « GARDE D'EXÉCUTION (ÉCRIVAIN SOUVERAIN) », avec note sur la nature de
    `boiler_bridge_online` (entity_id hérité, composante nécessaire non
    suffisante). Table des triggers (transitions `boiler_bridge_online`)
    inchangée — les triggers eux-mêmes restent valides.
  - `contrats/ecs/application_consigne.md` : §Rôle, étape 2, « générer une
    transaction boiler bridge » devient « générer une transaction vers
    l'écrivain souverain ». Les deux bandeaux AMENDÉ déjà en tête (migration,
    puis V1.2 ACK) ne couvraient pas cette ligne, laissée résiduelle.
  - `architecture/volets.md` : aucune occurrence de `boiler_bridge` —
    **sans objet**.
  - `contrats/chauffage/20_triggers_decisionnels__amendement.md` : la seule
    occurrence est `boiler_bridge_online` dans une liste factuelle des
    16 entités déclenchant `decision_centrale_trigger.yaml` (vérification
    runtime), sans affirmation sur l'activité du pont historique —
    **sans objet**.
- **A9** — `contrats/ping_lan_synthese.md` : `binary_sensor.boiler_bridge`
  (entité de l'intégration `ping`, cible ICMP de la machine hôte) vérifié
  contre `migration_boiler_bridge_vers_boilerack.md` §8, qui la déclare
  explicitement **conservée** — mesure la joignabilité de cette machine
  (qui héberge toujours Boilerack), indépendante du transport MQTT, « ni
  renommée, ni déplacée, ni retirée ». **Aucune correction.**
- **A10** — `README.md` : légende de `systeme-boiler-bridge.png`, « Boiler
  bridge: every physical command is transactional… » devient « Boilerack,
  the sovereign writer to the boiler: every physical command is
  transactional… » (le titre alt-text de l'image, qui décrit la carte UI
  telle qu'elle apparaît à l'écran, n'est pas modifié). `README.fr.md` :
  même correction sur la légende homologue, et la phrase d'ouverture « la
  chaudière est pilotée via un pont Raspberry Pi (`boiler_pi`) » devient
  « la chaudière est pilotée par un écrivain souverain (Boilerack), hébergé
  sur le Raspberry Pi qui documentait historiquement le pont `boiler_pi` ».
  Le nom littéral de la carte UI (`sensor.boiler_bridge_sante`, « Boiler
  Bridge ») n'est pas renommé — hors périmètre A10, déjà tranché comme
  nommage hérité assumé.
- **A11** — `audits/index.md` : C48 déjà référencé à l'ouverture (#781) —
  rien à ajouter. Pointeur daté ajouté en tête de
  `rapport_ecosysteme_depots_satellites.md` (seul des quatre rapports
  portant un constat P3 réellement lié à l'écrivain — `boiler-bridge` y est
  décrit comme seul satellite actif du domaine, désormais requalifié
  historique par le lot A3), sans réécrire son corps ni son constat n°5
  (dépôt privé, sans licence — inchangé, hors sujet migration).
  `cartographie_chaines_documentaires_arsenal.md`,
  `audit_navigation_documentation_arsenal.md` et
  `audit_documentaire_global_2026_06_06.md` vérifiés : mentions de `boiler`
  limitées à des inventaires de liens et de structure documentaire, aucune
  assertion sur l'écrivain actif — **sans objet**, non modifiés.

**Vérification (ce commit)** : `check_registre_chantiers.py` (REG-1 : 159
cibles, REG-2 : tout identifiant attribué) ; `docs_ci_orphan_report.py`
(DOC-CI-3, 192/192 référencés) ; `docs_ci_contract_counts.py` (DOC-CI-2, 16
compteurs, 0 écart) ; `docs_ci_naming.py` (DOC-CI-5) ;
`docs_ci_navigation_leaf_pages.py` (DOC-CI-6) ; `check_ci_coverage_registry.py`
— tous verts. `check_boiler_transactionnel_contracts.py` : 16/16 tests verts
(T01–T16), sans régression — ces cinq lots sont strictement documentaires,
aucun YAML/script/entité modifié.

**Axe A est complet (13/13).** Axe B (dépôt public Boilerack) et Axe C
(dettes guard parquées) restent inchangés — hors gouvernance directe
d'Arsenal. **C48 reste OUVERT** : les critères 2, 5 et 6 du §8 dépendent du
contenu du dépôt Boilerack lui-même, qu'une session Arsenal ne peut pas
modifier.

---

## 10. Renvois

- Migration (normatif amont) :
  [`architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`](../../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)
- Amendement garde d'exécution :
  [`contrats/chauffage/30_decision_centrale__amendement_garde_execution.md`](../../../contrats/chauffage/30_decision_centrale__amendement_garde_execution.md)
- Contrat central chauffage :
  [`contrats/chauffage/30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md)
- Écosystème des dépôts satellites :
  [`architecture/ecosysteme_depots_satellites.md`](../../../architecture/ecosysteme_depots_satellites.md)
- Doctrine changelog :
  [`architecture/03_doctrines/redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md)
- Doctrine solvabilité probatoire (réserves non circulaires, échéances
  opposables) :
  [`architecture/03_doctrines/solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)
- Registre des chantiers :
  [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
