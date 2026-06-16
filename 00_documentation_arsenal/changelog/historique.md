# ARSENAL — Historique architectural (2025 → 2026)

> Lecture « signal » : ce document raconte **comment le système a changé de nature**,
pas seulement ce qui a été ajouté. Chaque phase correspond à une inflexion de pensée,
pas à une liste de commits. Le détail version par version vit dans
[`changelog/index.md`](index.md) et les changelogs gelés sous [`changelog/changelogs/`](changelogs/) ;
ce récit s'appuie exclusivement sur eux.

---

## Avant-propos : ce que ce document n'est pas

Ce n'est pas un changelog. C'est une relecture rétrospective de l'évolution d'une doctrine.
Les versions mineures qui ne font que consolider sans changer de paradigme sont volontairement effacées du récit.
L'objectif est de pouvoir répondre, pour chaque période, à la question : **qu'est-ce que je savais faire que je ne savais pas faire avant ?**

**Convention de lecture.** Dans chaque phase, la rubrique *« Ce qui s'est passé »* énonce des **faits** traçables aux changelogs (versions, entités, fichiers). La rubrique *« Leçon retenue »* est une **interprétation** rétrospective. Les deux ne doivent pas être confondues.

---

## La thèse en une page

Arsenal n'a pas été conçu structuré ; il l'est **devenu**, par couches successives. Deux fils s'entrelacent dans cette histoire :

- **Fil A — le runtime gagne en rigueur.** D'une installation Home Assistant organisée par fonctionnalité, le système passe à des scripts souverains (oct. 2025), une décision centrale événementielle (v8), des pipelines métier contractualisés (v9–v10), une exécution transactionnelle vérifiée (v11), des verrous d'admissibilité (v12), puis une vérité par snapshot (v13).
- **Fil B — la documentation cesse d'être un commentaire et devient une autorité.** Premiers contrats de domaine (v9), documentation prescriptive (v10 finale), puis le **corpus de contrats devient le point d'entrée unique de la gouvernance** (v14), avec une nomenclature qui place la documentation *avant* le code. À partir de là, le fil B s'outille : doctrines (v15.5.1), auto-audit (v15), **lint et CI documentaire** (v15.9.2), **checkers contractuels** (navigation Lovelace, sommeil, registres chauffage), enfin **navigation documentaire** gouvernée par des gates (v15.9.1 → v16).

Le point que ce document veut rendre lisible : **comment une installation HA est devenue un système gouverné par contrats, audits et CI documentaire.** C'est le fil B, longtemps discret, qui devient structurant à partir de v14 et porteur de l'identité d'Arsenal à partir de v15.9.

---

## Vue synthétique — Inflexions majeures

| Période | Phase | Ce qui a changé en profondeur |
|---|---|---|
| août → oct. 2025 | Pré-Arsenal | Passage de « ça marche » à « c'est structuré » |
| déc. 2025 | v1–v5 | Naissance des primitives (timers, scripts souverains, verrous) |
| jan. 2026 (début) | v6–v7 | Doctrine opposable : le système devient lisible et gouvernable ; **pivot documentaire** (`00_documentation_arsenal/`) |
| jan. 2026 (fin) | v8 | Souveraineté et silence : HA maître, bruit réduit, résilience outillée |
| février 2026 | v9 | Séparation structurelle : pipelines métier, **premiers contrats de domaine** |
| fév. → mars 2026 | v10 | Maturité physique puis **contractuelle** : réconciliation, déterminisme, documentation prescriptive |
| mars 2026 | v11 → v11.1.x | Système vérifié : exécution transactionnelle, souveraineté locale, capacité d'exécution comme condition de vérité |
| avril 2026 | v12 | Durcissement architectural : **verrou d'admissibilité**, transactions multi-domaines, contexte = transformation réversible |
| avril → mai 2026 | v13 | Vérité par **snapshot** et interprétée : sommeil, cardio, autonomie ; domaines externes (Bluetti, imprimerie) |
| mai 2026 | v14 | **Le pivot de gouvernance** : nomenclature canonique, `contrats/` = point d'entrée unique, doc avant code |
| mai → juin 2026 | v15 | L'ère de l'outillage : deadlines persistantes, doctrines, auto-audit, **lint et CI documentaire**, checkers |
| juin 2026 | v16 | **Navigation documentaire gouvernée** : hubs, gates de pages-feuilles, README de domaine |

---

## Phase A — Pré-Arsenal (août → octobre 2025)
### Ce qui s'est passé

Le système existait, mais n'était pas *gouvernable*.
Les automatisations étaient organisées par fonctionnalité plutôt que par domaine,
les chemins d'include n'étaient pas stables, et la logique de chaque domaine (alarme, ECS, chauffage)
était dispersée entre des automations, des scripts et des helpers sans hiérarchie claire.

Deux jalons marquent cette période :

**Septembre 2025 — Consolidation structurante :** premier grand ménage.
Migration vers des répertoires canoniques (`automations/`, `template_sensors/`…),
refonte de la navigation UI, industrialisation des `utility_meter`.
Le geste central n'est pas une feature — c'est la mise en cohérence de ce qui existait déjà.

**Octobre 2025 — Industrialisation :** introduction des `timer:`
comme primitive de contrôle (watchdogs, anti-rebond), remplacement progressif des `delay`.
Naissance des scripts « souverains » : l'alarme, l'ECS, le chauffage cessent d'être des séquences d'automations
et deviennent des scripts qui portent leur propre responsabilité.

### Leçon retenue
> **Avant de construire, il faut que les fondations soient stables.**
La discipline des chemins canoniques et des scripts souverains est la condition de tout le reste.
Sans cette phase, Arsenal n'aurait pas de sol où pousser.

---

## Phase B — v1 → v5 (décembre 2025)

Les jalons existent, le contenu détaillé n'a pas été archivé en récit ici.
Ce qui est certain : c'est pendant cette période que les premières primitives Arsenal
apparaissent — timers, scripts souverains, helpers mémoire et premiers verrous d'état.
La nomenclature et la séparation décision / exécution / UI prennent leur forme initiale.

### Leçon retenue
> Cette phase est le « big bang » doctrinal.

---

## Phase C — Série v6 (janvier 2026, début)
### Ce qui s'est passé

**v6.4 — Normalisation totale des en-têtes :**
chaque helper reçoit un rôle explicite (paramètre / mémoire / planification / décision / action).
La séparation n'est plus implicite dans le nom — elle est déclarée.
Les scripts clarifient leur périmètre (unitaire vs orchestration vs décision).
Un seul script physique par ressource critique.

**v6.5 — Premiers patterns métier durables :**
l'état « Vacances » et l'état « Visiteur » deviennent des `binary_sensor` métier consommés
par les autres domaines, pas des conditions éparpillées.
La présence est reléguée au rang d'autorisation, pas de raccourci décisionnel.

### Leçon retenue
> **Verrouiller les couches avant d'ajouter.**
C'est le moment où la doctrine devient opposable : si quelque chose casse, on sait *où* chercher.

---

## Phase D — Série v7 (mi-janvier 2026)
### Ce qui s'est passé

**v7.0 — Pivot documentaire :**
naissance de `00_documentation_arsenal/` comme référentiel de doctrine.
L'UI reçoit une règle constitutionnelle : **elle ne décide jamais**.
Les timers deviennent des objets gouvernés.

**v7.2 — L'intention Neutre :**
introduction d'un état de chauffage `Neutre` signifiant « autorisé sans action » — l'abstention volontaire.
Le système peut désormais *ne pas agir* de manière intentionnelle et traçable.

**v7.3 — Signaux explicites :**
la fin d'un cycle ECS cesse d'être inférée — elle émet un signal qui doit être acquitté.
La présence devient une *autorisation*. L'alarme reçoit des garde-fous sur les paramètres invalides.

### Leçon retenue
> **Passage d'un système qui marche à un système gouverné, lisible, opposable.**
La documentation n'est plus un épiphénomène — elle commence à être contraignante. *(C'est ici que le fil B s'amorce.)*

---

## Phase E — Série v8 (fin janvier → début février 2026)
### Ce qui s'est passé

**v8.0 — Réforme des notifications :** les notifications persistantes ne signalent plus des succès — elles projettent uniquement des états « en cours » ou « dégradés ». Fin du bruit informationnel.

**v8.1 — Décision centrale 100 % événementielle :** fin définitive du modèle polling pour le chauffage. Introduction de l'anti-yo-yo et d'une mémoire de confirmation cloud. L'observabilité est structurée en familles A/B/C/D.

**v8.2 — « Silence utile » :** canal Zigbee migré (11 → 25), maillage reconstruit, LQI à source unique. La présence voit ses temporisations réduites — tout en perdant le droit d'écriture directe.

**v8.3 — Souveraineté HA :** HA devient maître des consignes chauffage, ViCare esclave passif (flux HA → ViCare). La clim reçoit un pipeline canonique (autorité → exécution → watchdog). Templates factorisés par ancres YAML.

### Leçon retenue
> **Le système devient sobre.** Moins de bruit, moins de polling, moins de couplage. Les sources sont uniques, la résilience est outillée. « Ça marche bien » devient « on sait pourquoi ça marche ».

---

## Phase F — Série v9 (février 2026)
### Ce qui s'est passé

**v9.0 — Extinction du legacy :** tous les templates `platform: template` sont migrés vers le moteur moderne `template:`. L'arborescence capteurs est assainie.

**v9.1 — UI stratifiée et premiers contrats :** architecture UI à trois niveaux (socle → génériques → métier). La logique *visite* quitte l'alarme pour devenir un domaine présence autonome. **Naissance des premiers contrats de domaine** (`contrats/alarme`, `contrats/ecs`) — première brique tangible du fil B.

**v9.4 → v9.6 — Domaine Aération refondé :** remplacement de l'automation monolithique par un pipeline modulaire M0–M6. Moteur de résilience générique (backoff réel, timers par intégration). Les ouvertures sont normalisées en couche abstraite `contact_*` (N1/N2) : les domaines critiques consomment une vérité logique agrégée, pas des capteurs physiques.

### Leçon retenue
> **La séparation des préoccupations devient structurelle, pas seulement conventionnelle.** Chaque domaine commence à avoir un contrat. Les capteurs physiques disparaissent derrière des couches d'abstraction.

---

## Phase G — v10 → v10 finale (fin février → mars 2026)
### Ce qui s'est passé

**v10 — Qualifications explicites :** fin de toute interprétation implicite des timers. Marqueurs métier (`*_grace_echue`, `ouverture_qualifiee_maison`). Temporalité thermique monotone et garantie.

**v10.3 — Simplification d'infrastructure :** suppression de `pyscript`, migration vers des scripts natifs HA.

**v10.7 — Redondance Zigbee généralisée :** chaque point critique couvert par deux capteurs fusionnés. Couche N2 (`mouvement_<zone>`, `contact_*`) comme interface unique des automations.

**v10.8 — Moteur de réconciliation (contrat v2.2) :** abandon du *last-valid-state* au profit d'un moteur centralisé (fenêtre de corroboration, quarantaine, inhibition). Trois couches d'état séparées : `observed_event` / `business_state` / `reconciliation_status`. Templates auto-paramétrés via `this.entity_id`.

**v10.9 — Orchestration pure :** le moteur de réconciliation est extrait vers 5 scripts à responsabilité unique ; l'automation est réduite au routage.

**v10 finale — Maturité contractuelle :** transformation en architecture contractuelle, déterministe et boot-safe. Éclatement des monolithes documentaires en sous-domaines. Généralisation des triggers `homeassistant.start` + garde `systeme_stable`. **La documentation cesse d'être descriptive — elle devient prescriptive.**

### Leçon retenue
> **Maturité physique *et* contractuelle.** Le code décisionnel ne voit plus les capteurs physiques ; il consomme des vérités métier réconciliées. La v10 finale est le moment où la documentation devient une contrainte de conception, et non plus un reflet du code.

---

## Phase H — v11 → v11.1.x (mars 2026)
### Ce qui s'est passé

**v11 — Souveraineté locale et exécution transactionnelle :** suppression complète de ViCare (plus aucune dépendance cloud chaudière) ; toutes les interactions boiler passent par un **bridge MQTT local**. L'exécution devient transactionnelle : chaque commande porte un `request_id`, chaque résultat exige un **ACK explicite** (`applied`) — le succès implicite est supprimé. ECS refondu sur la température réelle post-inertie ; clim dotée d'un moteur résilient (post-condition + retry).

**v11.1 — Contexte système explicite :** un contexte global (panne secteur, campagne réseau, stabilité) conditionne les comportements nominaux. Remédiations réseau orchestrées (fin des automations concurrentes). UI déclarative (`socles` / `génériques` / `dashboards`).

**v11.1.1 → v11.1.3 — Vérité lue, puis capacité d'exécution :** le chauffage abandonne toute reconstruction interne (`programme_chauffage` interprète le `boiler_heating_setpoint` ; l'état `Inconnu` devient un signal utile). Puis le bridge boiler devient la **frontière contractuelle entre logique Arsenal et réalité physique** : `binary_sensor.boiler_bridge_online` devient une condition canonique — aucune action n'est décidée si elle ne peut être physiquement exécutée.

### Leçon retenue
> **Le système devient vérifié, contextuel et ancré dans le réel.** v10 garantissait la cohérence logique ; v11 garantit la validité physique ; v11.1 la validité contextuelle ; v11.1.1 la vérité lue ; v11.1.3 la capacité d'exécution comme condition de vérité. La suppression de ViCare n'est pas une simplification — c'est la conséquence d'une souveraineté HA complète, de la décision jusqu'à la confirmation physique.

---

## Phase I — Série v12 (avril 2026)
### Ce qui s'est passé

**v12.0 — Durcissement architectural, le verrou d'admissibilité :** un patron nouveau se généralise sur la climatisation (COOL/HEAT/DRY) — l'exécution directe sans admissibilité devient **contractuellement interdite**, séparant strictement *besoin admissible* et *exécution*. La météo jardin passe de monolithes à des pipelines contractualisées (sources validées → cible robuste → diagnostic → façade). Le mode Vacances passe d'un booléen plat à un **socle à quatre composantes** (calendrier, demande, effectivité, intégrité). La VMC reconstruit sa vérité depuis les relais physiques. Les capteurs d'**intégrité des réglages** posent un principe : un état n'est exploitable que s'il est explicitement valide.

**v12.2 → v12.2.2 — Transactions multi-domaines et contexte réversible :** le modèle transactionnel `request → execution → guard → verdict → trace` est généralisé à tous les actionneurs physiques (socle `transactions_bots/`). Apparaît le pattern **« contexte = transformation réversible d'un paramètre »** (réversibilité avec sauvegarde + sentinelle, idempotence, encapsulation). Introduction du **système d'étiquettes Arsenal** (automatisations, capteurs, helpers, scripts, palette UI) — base normative pour l'audit et le tooling.

**v12.3 — Élargissement contrôlé, la supervision d'outils externes :** un nouveau *type* de domaine apparaît, avec un patron stratifié réutilisable (mesures → état → santé par axe → synthèse → alerte), d'abord sur le NAS Imprimerie. La boucle UPS est fermée (politique d'arrêt HA déclarée). Le contrat de journalisation bifurque en deux volets mutuellement exclusifs — un journal **fonctionnel** (destiné à l'humain) et un journal **technique** (destiné à l'opérateur). Le recueil `principes_generaux` est promu **recueil normatif des invariants universels**.

### Leçon retenue
> **L'admissibilité avant l'action, la réversibilité comme discipline.** Le système ne se contente plus d'exécuter correctement : il vérifie d'abord qu'il a le *droit* d'exécuter, et sait défaire ce qu'il pose. Le fil B s'élargit : la supervision d'outils hors-HA et la journalisation deviennent elles-mêmes contractualisées.

---

## Phase J — Série v13 (avril → mai 2026)
### Ce qui s'est passé

**v13 — Découplages et domaines externes :** le bouclage ECS change de paradigme (modèle thermique opportuniste + présence, contrat v2.1.2). Nouveau domaine **Bluetti** (7 capteurs stratifiés + alerte panne secteur) appliquant le patron outils externes de v12.3. Migration des barres de navigation vers `custom:layout-card`. Domaine **imprimerie** enrichi (humidex par zone, NAS factorisé).

**v13.1 — Garde locale et sous-domaines autonomes :** le référentiel BSSID passe d'une garde globale à une **garde locale par source** (couplage strict source ↔ personne). L'ECS Petite Maison est extrait en sous-domaine autonome (dashboards et contrat dédiés).

**v13.2 → v13.3 — La vérité par snapshot :** le sommeil est refondu autour d'un **snapshot consolidé Arsenal**, rompant la dépendance directe aux capteurs Withings. Le cardio nuit applique le même patron (snapshot → interprétation → anomalie → confirmation de persistance) et bascule vers une **référence personnelle** (delta vs moyenne glissante, plutôt que seuils absolus). L'intégrité des paramètres reçoit une **taxonomie unifiée** (indisponibilité stricte : pas d'optimisme silencieux). La VMC durcit sa chaîne exécutive (séquence atomique non interruptible).

### Leçon retenue
> **De l'état brut à l'état interprété.** Arsenal cesse de lire des capteurs et commence à figer des **snapshots cohérents** qu'il interprète contre une référence (souvent personnelle). La donnée volatile externe (Withings, Netatmo) est mise à distance derrière une vérité Arsenal stable.

---

## Phase K — Série v14 (mai 2026) — *le pivot de gouvernance*
### Ce qui s'est passé

**v14 — Structurelle majeure.** Deux gestes liés transforment la nature documentaire du système.

- **Nomenclature canonique des includes :** préfixe numérique strict `00_` → `19_` sur tous les dossiers consommés par `configuration.yaml` (1 263 fichiers déplacés/renommés). Le numéro fixe l'**ordre canonique de lecture** ; surtout, `00_documentation_arsenal/` précède strictement le code — rendant visible, dans l'arborescence elle-même, la **primauté du contrat sur l'implémentation**.
- **Corpus de contrats normatifs :** `00_documentation_arsenal/contrats/` devient le **point d'entrée unique de la gouvernance Arsenal**, avec des contrats publiés, opposables et versionnés (Alarme en 13 fichiers numérotés, Chauffage avec sous-arborescence `15_capteurs/`, ECS, Boiler, Bouclage, Babysitting, Cumulus petite maison, Aération). Principe posé : **aucun YAML d'un domaine couvert ne doit plus exister sans contrat amont ; toute évolution passe d'abord par le contrat.**

En parallèle, le domaine Voiture passe à un **snapshot atomique** (trio de helpers écrits dans la même transaction logique).

### Leçon retenue
> **C'est ici que « gouverné par contrats » cesse d'être une intention pour devenir une structure.** Avant v14, des contrats existaient (depuis v9) ; après v14, ils sont *le point d'entrée*, et l'arborescence elle-même place la documentation avant l'implémentation. Le fil B devient le squelette du dépôt.

---

## Phase L — Série v15 (mai → juin 2026) — *l'ère de l'outillage*
### Ce qui s'est passé

La v15 est longue (de v15 à v15.9.3) ; trois sous-arcs en résument la nature.

**Runtime — généralisation des patterns durcis.** Les **deadlines persistantes** (helpers `input_datetime` rejouables après restart) remplacent les temporisations `for:` volatiles, d'abord sur l'éclairage jardin (v15.5) puis généralisées (v15.5.1). La climatisation reçoit une chaîne d'admissibilité complète avec **réconciliation post-boot** (v15.7.3), et un correctif critique de deadlock d'extinction COOL **figé par une CI dédiée** (v15.8.4). L'inhibition géofencing chauffage passe à une architecture deux couches gouvernée par hystérésis (v15.8).

**Doctrine — le corpus se formalise.** Création du sous-domaine `architecture/03_doctrines/` et migration des documents fondateurs (`principes_generaux`, `gestion_du_temps`, `separation_decision_action`, `git`, `nommage_entites`, `causalite_metier`, `entetes_fichiers`) (v15.5.1). Le chauffage se dote d'une **doctrine des registres** et d'un fichier CI `registres_entites.yaml` (v15.8).

**Auto-observation et — surtout — CI documentaire.** Arsenal expose son propre **audit patrimonial** (Arsenal Self Audit : capteurs MQTT + dérivés + contrat cadre `arsenal_self.md`, v15) et contractualise la suite d'outils NAS. Puis, fin mai → début juin, le fil B s'**outille de gardes automatiques** :
- **lint documentaire** et **contrôles CI docs** + contrôle des liens (v15.9.2) ;
- **navigation documentaire** : `navigation/README.md`, `carte_domaines.md`, pivots et premiers hubs de domaine (v15.9.1) ;
- **checker contractuel + CI Sommeil** (`check_sommeil_contracts.py`, `contracts_sommeil.yml`) et suivi transverse de **couverture normative** (v15.9.3).

C'est aussi en v15.6.1 qu'est créé `prompt_changelog.md`, fixant les règles rédactionnelles des changelogs eux-mêmes — la production documentaire devient à son tour normée.

### Leçon retenue
> **La gouvernance documentaire passe de l'intention à l'exécutable.** Un contrat sans garde est une bonne intention ; en v15.9, les contrats et la documentation acquièrent leurs **checkers et leurs gates CI** (lint, liens, orphelins, couverture, sommeil, registres). La documentation devient un artefact *testé*, au même titre que le runtime.

---

## Phase M — Série v16 (juin 2026) — *navigation documentaire gouvernée*
### Ce qui s'est passé

**v16.0.0 — Documentation navigable et vérifiée :** ajout de README dans les dossiers-feuilles et de liens internes dans les index (Architecture, Contrats, UI, outils externes) ; README de domaine pour la quasi-totalité des familles de contrats (alarme, ECS, météo, pannes, santé, publication, ouvertures, éclairage, imprimerie, déshumidificateur). Surtout, ajout du contrôle **`DOC-CI-6`** sur les pages-feuilles de navigation, intégré au workflow `docs.yml` : la navigabilité documentaire devient une **propriété vérifiée en CI**, pas une bonne volonté.

**v16.0.1 — Continuité runtime sous gouvernance documentaire :** réécriture du signal de panne secteur (`binary_sensor.panne_secteur_en_cours`, dérivation par OR UPS/Bluetti), présence thermique stabilisée, extension de la cascade de raison clim et verdicts par mode — chaque évolution accompagnée de ses rapports d'audit et de la mise à jour des contrats et hubs. Le runtime continue d'évoluer, mais **désormais toujours adossé à son corpus documentaire gouverné**.

### Leçon retenue
> **La boucle est bouclée : la documentation est navigable, référencée et testée.** Un document orphelin, un lien mort ou une page-feuille sans point d'entrée échouent la CI. Arsenal n'est plus seulement *documenté* : sa documentation est un système gouverné, avec ses invariants et ses gardes — exactement comme le runtime l'est depuis v8–v11.

---

## L'émergence de la gouvernance documentaire (fil B, vue d'ensemble)

Cette section retrace explicitement le fil le plus important pour comprendre ce qu'est devenu Arsenal. Faits, traçables aux versions citées.

1. **Amorce (v7.0).** Naissance de `00_documentation_arsenal/` : la doctrine a un lieu. L'UI reçoit sa règle constitutionnelle (« ne décide jamais »).
2. **Premiers contrats (v9.1).** `contrats/alarme`, `contrats/ecs` : un domaine = un contrat. La documentation commence à être opposable.
3. **Documentation prescriptive (v10 finale).** Les monolithes sont éclatés en sous-domaines ; la documentation devient une contrainte de conception.
4. **Le pivot (v14).** `contrats/` devient le **point d'entrée unique** ; la nomenclature `00_…19_` place la doc avant le code. « Aucun YAML sans contrat amont. »
5. **Les doctrines (v15.5.1).** `architecture/03_doctrines/` réunit les invariants universels (temps, séparation décision/action, nommage, causalité métier, en-têtes).
6. **L'auto-observation (v15).** Arsenal Self Audit : le système audite son propre patrimoine et l'expose.
7. **La CI documentaire (v15.9.2 → v15.9.3).** Lint documentaire, contrôle des liens, contrôles CI docs, checker + CI Sommeil, suivi de couverture normative. La documentation devient *testée*.
8. **La navigation gouvernée (v15.9.1 → v16).** Hubs de domaine, `carte_domaines.md`, README de dossiers-feuilles, et gate **`DOC-CI-6`** intégré à `docs.yml`. La navigabilité est un invariant vérifié.

**Les checkers contractuels** apparus dans la même période illustrent que cette gouvernance vaut aussi pour le runtime décrit par les contrats : CI includes Lovelace (`R-LL-INC-1`), navigation Lovelace (`R-LL-NAV-1`), registres chauffage, comparateur d'extinction COOL, région de décision chauffage (`R-COV-1`), contrats Sommeil. Le détail de chacun vit dans les changelogs et audits correspondants.

> **Interprétation.** Le fil B est ce qui distingue Arsenal d'une grosse configuration Home Assistant. Le runtime de beaucoup d'installations est sophistiqué ; rares sont celles où la *documentation elle-même* est contractuelle, navigable et gardée par CI. C'est cette bascule — discrète jusqu'en v14, structurante ensuite — qui fait d'Arsenal un système gouverné, et non seulement automatisé.

---

## Primitives architecturales Arsenal

Au fil de son évolution, Arsenal a convergé vers un petit nombre de primitives structurantes utilisées dans tous les domaines.

**Scripts souverains** — Une ressource physique critique possède toujours un script maître responsable de son exécution.

**Timers gouvernés** — Le temps n'est jamais implicite : il est représenté par des objets timer observables.

**Deadlines persistantes** — Les échéances déterminantes sont stockées dans des helpers `input_datetime`, rejouables après redémarrage, plutôt que portées par des temporisations volatiles.

**Helpers mémoire** — Les états historiques ou contextes persistants sont explicitement stockés.

**Capteurs métier (data-driven)** — Les automatisations consomment des vérités logiques (`contact_*`, `mouvement_<zone>`) plutôt que des capteurs physiques ; les scripts deviennent de purs exécutants.

**Pipelines métier** — Les logiques complexes sont exprimées en pipelines modulaires (ex. M0 → M6 pour l'aération).

**Moteurs de réconciliation** — Les événements physiques instables sont consolidés avant d'être exposés au moteur métier.

**Transactions vérifiées** — Toute action sur un système physique critique est corrélée à un ACK explicite ; un succès non confirmé est invalide. Généralisé en socle multi-domaines (`transactions_bots/`).

**Verrou d'admissibilité** — Avant d'exécuter, le système vérifie qu'il en a le droit : séparation stricte *besoin admissible* / *exécution*.

**Snapshot atomique** — Des grandeurs liées sont figées dans la même transaction logique pour former un tuple cohérent (autonomie/température, sommeil, cardio).

**Contexte système** — Les comportements nominaux sont conditionnés par un état global explicite (stabilité, panne, réseau).

**Contexte réversible** — Une transformation contextuelle d'un paramètre est réversible (sauvegarde + sentinelle), idempotente et encapsulée dans un script dédié.

---

## Instruments de gouvernance

Distincts des primitives *runtime*, ces instruments encadrent la production et la vérification de la documentation et des contrats.

**Contrats de domaine** — `contrats/` : référentiel opposable et versionné, **point d'entrée unique** de la gouvernance (v14). Aucun YAML d'un domaine couvert sans contrat amont.

**Doctrines** — `architecture/03_doctrines/` : invariants universels (temps, séparation décision/action, nommage, causalité métier, en-têtes).

**Audits** — `audits/` : rapports en lecture seule, plans d'action, chantiers, contre-expertises ; trace les constats avant correction.

**Checkers contractuels** — Scripts de vérification runtime opposables (navigation et includes Lovelace, registres chauffage, décision chauffage, contrats Sommeil…), chacun activé par un workflow CI nommé.

**CI documentaire** — Lint (`docs_lint`, ex. `R-DOC-H1-1`), contrôle des liens, contrôles `DOC-CI-*` (index changelog, orphelins, nommage, pages-feuilles), intégrés à `docs.yml`. La documentation est un artefact *testé*.

**Navigation documentaire** — `navigation/` : hubs de domaine non normatifs, `carte_domaines.md`, pivots ; gouvernée par les gates de navigabilité.

**Procédures d'autoring** — Règles de production normées (ex. `prompt_changelog.md` pour les changelogs).

---

## Patterns récurrents — ce que l'histoire révèle

**1. Structurer avant d'ajouter.** Chaque phase de feature est précédée ou suivie d'une phase de consolidation. Les versions qui « ne font rien » sont souvent les plus importantes à long terme.

**2. Les sources uniques comme invariant.** À chaque échelle — physique (un script par ressource), logique (un capteur de vérité par domaine), décisionnelle (un maître par flux), documentaire (un contrat par domaine) — Arsenal converge vers des sources uniques.

**3. L'abstraction comme protection.** Couches `contact_*` / `mouvement_<zone>`, contrats de domaine, snapshots : introduire une abstraction protège le code décisionnel contre la volatilité physique. Les capteurs changent ; le moteur ne le voit pas.

**4. Rendre les intentions et les validations explicites.** `Neutre` plutôt qu'une absence de décision ; un signal acquitté plutôt qu'une inférence ; `*_grace_echue` plutôt qu'un timer en `idle`. L'implicite est systématiquement remplacé par de l'explicite gouverné.

**5. L'UI ne décide jamais.** Posé en v7.0, jamais violé. Il a rendu possibles toutes les refontes UI ultérieures sans régression fonctionnelle.

**6. Rien n'est vrai sans validation.** Un état n'est accepté que s'il est confirmé (ACK, corroboration, mesure stabilisée). C'est le passage d'un système cohérent à un système fiable.

**7. L'admissibilité avant l'action.** À partir de v12, le système vérifie qu'il a le *droit* d'agir avant d'agir, et sait défaire ce qu'il a posé (contexte réversible).

**8. La documentation est gouvernée comme du code.** À partir de v14–v16, contrats, doctrines et navigation deviennent opposables, référencés et **gardés par CI**. Un document orphelin ou un lien mort est un échec de build, pas un détail.

---

*Document vivant — à enrichir à chaque inflexion majeure, pas à chaque release.*

*Ce document ne cherche pas à être exhaustif. Il cherche à préserver la mémoire des décisions qui ont changé la nature du système. Le détail factuel, version par version, reste dans [`changelog/index.md`](index.md) et les changelogs gelés.*
