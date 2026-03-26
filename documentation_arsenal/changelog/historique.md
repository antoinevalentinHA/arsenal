# ARSENAL — Historique architectural (2025 → 2026)

> Lecture "signal" : ce document raconte **comment le système a changé de nature**, 
pas seulement ce qui a été ajouté. Chaque phase correspond à une inflexion de pensée, 
pas à une liste de commits.

---

## Avant-propos : ce que ce document n'est pas

Ce n'est pas un changelog. C'est une relecture rétrospective de l'évolution d'une doctrine. 
Les versions mineures qui ne font que consolider sans changer de paradigme sont volontairement effacées du récit. 
L'objectif est de pouvoir répondre, pour chaque période, à la question : **qu'est-ce que je savais faire que je ne savais pas faire avant ?**

---

## Vue synthétique — Inflexions majeures

| Période | Phase | Ce qui a changé en profondeur |
|---|---|---|
| août → oct. 2025 | Pré-Arsenal | Passage de "ça marche" à "c'est structuré" |
| déc. 2025 | Arsenal v1–v5 | Naissance des primitives (timers, scripts souverains, verrous) |
| jan. 2026 (début) | v6–v7 | Doctrine opposable : le système devient lisible et gouvernable |
| jan. 2026 (fin) | v8 | Souveraineté et silence : HA maître, bruit réduit, résilience outillée |
| fév. 2026 | v9 | Séparation structurelle : pipelines métier, contrats de domaine, abstraction logique |
| fév.–début mars 2026 | v10 | Maturité physique : capteurs redondés, états réconciliés, temporalité explicite |
| mars 2026 | v10 finale | Maturité contractuelle : documentation prescriptive, système déterministe et boot-safe |
| mars 2026 | v11+ | Système vérifié : exécution transactionnelle, souveraineté locale, contexte système |

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
Naissance des scripts "souverains" : l'alarme, l'ECS, le chauffage cessent d'être des séquences d'automations 
et deviennent des scripts qui portent leur propre responsabilité.

### Leçon retenue
> **Avant de construire, il faut que les fondations soient stables.** 
La discipline des chemins canoniques et des scripts souverains est la condition de tout le reste. 
Sans cette phase, Arsenal n'aurait pas de sol où pousser.

---

## Phase B — Arsenal v1 → v5 (décembre 2025)

Les jalons existent, le contenu détaillé n'a pas été archivé ici. 
Ce qui est certain : c'est pendant cette période que les premières primitives Arsenal 
apparaissent — timers, scripts souverains, helpers mémoire et premiers verrous d'état. 
La nomenclature et la séparation décision / exécution / UI prennent leur forme initiale.

### Leçon retenue
> Cette phase est le "big bang" doctrinal. 

---

## Phase C — Série v6 (janvier 2026, début)
### Ce qui s'est passé

**v6.4 — Normalisation totale des en-têtes :** 
chaque helper reçoit un rôle explicite (paramètre / mémoire / planification / décision / action). 
La séparation n'est plus implicite dans le nom — elle est déclarée. 
Les scripts clarifient leur périmètre (unitaire vs orchestration vs décision). 
Un seul script physique par ressource critique (`script.cycle_alimentation_box`).

**v6.5 — Premiers patterns métier durables :** 
l'état "Vacances" et l'état "Visiteur" deviennent des `binary_sensor` métier consommés 
par les autres domaines, pas des conditions éparpillées. 
La présence est reléguée au rang d'autorisation, pas de raccourci décisionnel.

### Leçon retenue
> **Verrouiller les couches avant d'ajouter.** 
Aucune feature significative dans ces versions — uniquement de la cohérence. 
C'est le moment où la doctrine devient opposable : si quelque chose casse, on sait *où* chercher.

---

## Phase D — Série v7 (11 janvier → mi-janvier 2026)
### Ce qui s'est passé

**v7.0 — Pivot documentaire :** 
naissance de `documentation_arsenal/` comme référentiel de doctrine. 
L'UI reçoit une règle constitutionnelle : **elle ne décide jamais**. 
Les timers deviennent des objets gouvernés.

**v7.2 — L'intention Neutre :** 
introduction d'un état de chauffage `Neutre` signifiant 
"autorisé sans action" — l'abstention volontaire. 
Fin des décisions implicites de présence. 
Ce détail conceptuel est structurant : 
le système peut désormais *ne pas agir* de manière intentionnelle et traçable.

**v7.3 — Signaux explicites :** 
la fin d'un cycle ECS cesse d'être inférée — elle émet un signal (`ecs_fin_cycle_signal`) qui doit être acquitté. 
La présence devient une *autorisation*, pas un raccourci. 
L'alarme reçoit des garde-fous sur les paramètres invalides.

### Leçon retenue
> **Passage d'un système qui marche à un système gouverné, lisible, opposable.** 
Chaque domaine peut maintenant être audité indépendamment. 
La documentation n'est plus un épiphénomène — elle est contraignante.

---

## Phase E — Série v8 (19 janvier → 4 février 2026)
### Ce qui s'est passé

**v8.0 — Réforme des notifications :** 
les notifications persistantes ne signalent plus des succès — elles projettent 
uniquement des états "en cours" ou "dégradés". Fin du bruit informationnel.

**v8.1 — Décision centrale 100% événementielle :** 
fin définitive du modèle polling — plus d'évaluation périodique, 
le chauffage répond uniquement à des événements. 
Introduction de l'anti-yo-yo (`chauffage_application_en_cours`) et d'une mémoire de confirmation cloud. 
L'observabilité est structurée en familles A/B/C/D.

**v8.2 — "Silence utile" :** Overkiz passe en mode silencieux. 
Le canal Zigbee migre (11→25), le maillage est reconstruit. 
La LQI reçoit une source unique. 
La présence voit ses temporisations réduites drastiquement — tout en perdant le droit d'écriture directe.

**v8.3 — Souveraineté HA :** 
HA devient maître absolu des consignes chauffage, ViCare devient esclave passif (flux monodirectionnel HA→ViCare). 
La Clim reçoit un pipeline canonique (autorité → exécution → watchdog). 
Les templates sont factorisés par ancres YAML.

### Leçon retenue
> **Le système devient sobre.** 
Moins de bruit, moins de polling, moins de couplage. 
Les sources sont uniques, la résilience est outillée (backoff réel, notifications persistantes recentrées). 
C'est la phase où "ça marche bien" devient "on sait pourquoi ça marche".

---

## Phase F — Série v9 (8 février → fin février 2026)
### Ce qui s'est passé

**v9.0 — Extinction du legacy :** 
tous les templates `platform: template` sont migrés vers le moteur moderne `template:`. 
L'arborescence capteurs est assainie. 
L'UI Chauffage est reconstruite avec des notifications découplées des scripts via une automation idempotente dédiée.

**v9.1 — UI stratifiée :** 
création de `button_card_templates/socle/` comme couche canonique. 
L'UI reçoit une architecture à trois niveaux : socle → génériques → métier. 
La logique *visite* quitte l'alarme pour devenir un domaine présence autonome. 
**Naissance des premiers contrats de domaine** (`contrats/alarme`, `contrats/ecs`).

**v9.4 → v9.6 — Domaine Aération refondé :** 
remplacement de l'automation monolithique par un pipeline modulaire M0–M6. 
Introduction d'un moteur de résilience générique (backoff réel, timers par intégration). 
Les ouvertures sont normalisées en couche abstraite `contact_*` (N1/N2) : 
les domaines critiques (chauffage, alarme, aération) consomment une vérité logique agrégée, 
et non plus des capteurs physiques individuels.

### Leçon retenue
> **La séparation des préoccupations devient structurelle, pas seulement conventionnelle.** 
Chaque domaine a un contrat. 
L'UI ne sait pas ce que fait le moteur. 
L'aération est un pipeline observable. 
Les capteurs physiques disparaissent derrière des couches d'abstraction.

---

## Phase G — v10 → v10.9.1 (fin février → mars 2026)
### Ce qui s'est passé

**v10 — Qualifications explicites :** 
fin de toute interprétation implicite des timers (`idle`, `cancel`). 
Introduction de marqueurs métier (`*_grace_echue`, `ouverture_qualifiee_maison`). 
La temporalité thermique devient monotone et garantie (calculs en secondes, hiérarchie stricte `analyse < blocage`).

**v10.3 — Simplification d'infrastructure :** 
suppression de `pyscript`, migration vers des scripts natifs HA. 
Réduction de la surface de maintenance. 
Préconfort vacances autonome.

**v10.7 — Redondance Zigbee généralisée :** 
chaque point critique est couvert par deux capteurs physiques fusionnés. 
Introduction de la couche N2 (`mouvement_<zone>`, `contact_*`) 
comme interface unique pour les automations — les capteurs physiques individuels disparaissent du code décisionnel.

**v10.8 — Nouveau moteur de réconciliation (contrat v2.2) :** 
abandon du modèle *last-valid-state* au profit d'un moteur centralisé avec 
fenêtre de corroboration, quarantaine et inhibition système. 
Introduction de trois couches d'état séparées : `observed_event` / `business_state` / `reconciliation_status`. 
Les templates sont auto-paramétrés via `this.entity_id` — ajouter un capteur devient déclaratif.

**v10.9 — Orchestration pure :** 
le moteur de réconciliation est extrait vers 5 scripts spécialisés à responsabilité unique. 
L'automation est réduite à un simple routage d'événements — toute logique métier réside dans les scripts.

**v10 finale — Maturité contractuelle :** 
transformation du système en architecture contractuelle, déterministe et boot-safe. 
Les monolithes documentaires sont éclatés en sous-domaines structurés. 
Le corpus ADR Viessmann est promu en architecture cible active. 
Généralisation des triggers `homeassistant.start` + garde `systeme_stable` → reconvergence automatique post-boot. 
La documentation cesse d'être descriptive — elle devient prescriptive.

### Leçon retenue
> **Le système atteint sa maturité physique et contractuelle.** 
La couche matérielle (Zigbee, capteurs) est abstraite, redondée et réconciliée. 
Le code décisionnel ne voit plus les capteurs physiques — il consomme uniquement des vérités métier réconciliées. 
La v10 finale marque le moment où la documentation devient une contrainte de conception, et non plus un reflet du code.

---

## Phase H — v11 → v11.1 (mars 2026)
### Ce qui s'est passé

**v11 — Souveraineté locale et exécution transactionnelle :** 
suppression complète de ViCare — Arsenal n'a plus aucune dépendance cloud sur la chaudière. 
Toutes les interactions boiler passent par un bridge MQTT local. 
L'exécution devient transactionnelle : chaque commande porte un `request_id`, 
chaque résultat exige un ACK explicite (`applied`) — le succès implicite est supprimé. 
L'ECS est refondu en pipeline modulaire sur température réelle post-inertie, 
avec autocorrection physique des offsets via la température maximale de cycle. 
La climatisation reçoit un moteur résilient avec post-condition vérifiée et retry contrôlé.

**v11.1 — Contexte système explicite :** 
introduction d'un contexte système global (panne secteur, campagne réseau, stabilité) 
qui conditionne l'ensemble des comportements nominaux. 
Les remédiations réseau sont désormais orchestrées par ce contexte → fin des automations autonomes concurrentes. 
L'ECS est inhibé explicitement en régime dérogatoire. 
L'UI `button_card_templates/` est refondue en architecture déclarative structurée (`socles` / `génériques` / `dashboards`).

### Leçon retenue
> **Le système devient vérifié et non-contradictoire.** 
Aucune action physique ne peut être présumée réussie sans validation explicite. 
Aucune logique nominale ne peut s'exécuter hors contexte système valide.

La suppression de ViCare n'est pas une simplification — c'est une conséquence : 
la souveraineté HA devient complète, de la décision jusqu'à la confirmation physique.

v10 garantissait la cohérence logique. 
v11 garantit la **validité physique et contextuelle**.

---

## Primitives architecturales Arsenal

Au fil de son évolution, Arsenal a convergé vers un petit nombre de primitives structurantes utilisées dans tous les domaines.

**Scripts souverains** — Une ressource physique critique possède toujours un script maître responsable de son exécution.

**Timers gouvernés** — Le temps n'est jamais implicite : il est représenté par des objets timer observables.

**Helpers mémoire** — Les états historiques ou les contextes persistants sont explicitement stockés dans des helpers.

**Capteurs métier** — Les automatisations consomment des vérités logiques (`contact_*`, `mouvement_<zone>`) plutôt que des capteurs physiques.

**Pipelines métier** — Les logiques complexes sont exprimées sous forme de pipelines modulaires (ex : M0 → M6 pour l'aération).

**Moteurs de réconciliation** — Les événements physiques instables sont consolidés par des moteurs dédiés avant d'être exposés au moteur métier.

**Transactions vérifiées** — Toute action sur un système physique critique est corrélée à un ACK explicite ; un succès non confirmé est considéré comme invalide.

**Contexte système** — Les comportements nominaux sont conditionnés par un état global explicite (stabilité, panne, réseau) garantissant la cohérence du système en régime dégradé.

---

## Patterns récurrents — ce que l'histoire révèle

**1. Structurer avant d'ajouter.** 
Chaque phase de feature est précédée ou suivie d'une phase de consolidation. 
Les versions qui "ne font rien" sont souvent les plus importantes à long terme.

**2. Les sources uniques comme invariant.** 
À chaque échelle — 
physique (un seul script par ressource), 
logique (un seul capteur de vérité par domaine), 
décisionnelle (un seul maître par flux) — 
Arsenal converge vers des sources uniques.

**3. L'abstraction comme protection.** 
La couche `contact_*`, la couche `mouvement_<zone>`, les contrats de domaine : à chaque fois, introduire une abstraction 
protège le code décisionnel contre la volatilité physique. 
Les capteurs changent, cassent, se multiplient — le moteur ne le voit pas.

**4. Rendre les intentions et les validations explicites.** 
`Neutre` plutôt qu'une absence de décision. 
`ecs_fin_cycle_signal` plutôt qu'une inférence d'état. 
`*_grace_echue` plutôt qu'un timer en `idle`. 
Arsenal a systématiquement remplacé l'implicite par de l'explicite gouverné — au prix d'un peu plus de code, 
mais d'une lisibilité et d'une auditabilité infiniment supérieures.

**5. L'UI ne décide jamais.** 
Ce principe, posé en v7.0, n'a jamais été violé. 
Il a rendu possibles toutes les refontes UI ultérieures sans régression fonctionnelle.

**6. Rien n'est vrai sans validation.** 
Un état n'est accepté que s'il est confirmé (ACK, corroboration, mesure stabilisée). 
C'est le passage d'un système cohérent à un système fiable.

---

*Document vivant — à enrichir à chaque inflexion majeure, pas à chaque release.*

*Ce document ne cherche pas à être exhaustif. 
Il cherche à préserver la mémoire des décisions qui ont changé la nature du système.*
