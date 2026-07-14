# Gestion de l'absence et des vacances — chauffage hivernal et climatisation « COOL »

- **Type :** rapport d'audit comparatif **statique, lecture seule** — aucun runtime, contrat normatif, helper, test, checker, workflow CI ni changelog modifié.
- **Statut :** trace documentaire. **Aucune architecture cible décidée, aucun chantier ouvert, aucune piste exploratoire promue en décision.**
- **Nature :** consolidation de deux audits antérieurs (chauffage / climatisation COOL) sur la gestion de l'absence et des vacances.
- **Portée normative :** nulle. Les seules formulations normatives reprises ici renvoient à des contrats **déjà** opposables (chauffage 60/65/66, vacances 1.4) et sont signalées comme telles.
- **Convention de sourçage :** chaque fait structurant est relié à un fichier runtime ou contractuel, avec numéros de ligne lorsque la stabilité du fichier le permet. Aucun nom d'entité ni chemin n'est cité sans vérification dans le dépôt.

> **Distinction de lecture imposée à tout le rapport.** On sépare strictement : **FAIT** (vérifié sur pièce) · **INTERPRÉTATION** (lecture fonctionnelle proposée, non tranchée) · **QUESTION OUVERTE** (arbitrage requis avant toute conception). Aucun diagnostic n'est converti en décision.

---

## 1. Objet et périmètre

Ce rapport conserve la trace de l'audit comparatif entre :

1. la gestion **estivale** de l'absence par la climatisation en mode `COOL` ;
2. la gestion **hivernale** de l'absence et des vacances par le chauffage, dont son mécanisme d'anticipation du retour de vacances (« pré-confort »).

Il documente les faits établis, la comparaison factuelle des deux domaines, les limites des analogies envisagées, et les questions restant à trancher **avant** toute conception. Il ne propose aucune architecture, aucun YAML, aucune correction.

**Élément déclencheur (contexte, non-fait technique) :** un retour de plus de 8 h d'absence en période de forte chaleur, chambres jugées trop chaudes à l'arrivée. Cet incident sert de cadrage ; il n'est **pas** assimilé à un cas Vacances (voir §5, le mode Vacances n'était pas nécessairement actif).

---

## 2. Sources auditées

**Runtime — Climatisation COOL**
- `12_template_sensors/climatisation/autorisation/cool.yaml`
- `12_template_sensors/climatisation/autorisation/dry.yaml`
- `12_template_sensors/climatisation/blocages/absence_longue.yaml`
- `12_template_sensors/climatisation/decision/consigne.yaml`
- `12_template_sensors/climatisation/seuils_on_off/cool/on.yaml`
- `08_timers/climatisation/timer_absence_longue.yaml`
- `11_automations/climatisation/cool/start_timer_absence.yaml`
- `11_automations/climatisation/modes.yaml`
- `12_template_sensors/presence/confort_thermique_stabilisee.yaml`
- `12_template_sensors/presence/global.yaml`

**Runtime — Chauffage & pré-confort**
- `10_scripts/chauffage/decision_centrale.yaml`
- `11_automations/chauffage/pre_confort_vacances/orchestrateur.yaml`
- `11_automations/chauffage/pre_confort_vacances/cycle.yaml`
- `11_automations/chauffage/pre_confort_vacances/notification.yaml`
- `12_template_sensors/chauffage/pre_confort/pre_confort_debut_ts.yaml`
- `12_template_sensors/chauffage/pre_confort/pre_confort_fenetre_valide.yaml`
- `12_template_sensors/chauffage/pre_confort/preconfort_raison.yaml`
- `05_input_booleans/chauffage/preconfort.yaml`, `05_input_booleans/chauffage/preconfort_cycle.yaml`
- `07_input_datetimes/chauffage/fenetre_preconfort.yaml`, `07_input_datetimes/vacances/vacances.yaml`
- `03_input_numbers/chauffage/duree_prechauffage_vacances.yaml`
- `08_timers/chauffage/preconfort.yaml`

**Runtime — Vacances / autres consommateurs de retour**
- `12_template_sensors/modes/vacances_actives.yaml`
- `11_automations/ecs/desinfection_retour_vacances.yaml`

**Contrats (opposables)**
- `00_documentation_arsenal/contrats/chauffage/60_absence_inhibition_geofencing.md`
- `00_documentation_arsenal/contrats/chauffage/65_pre_confort_retour_vacances.md`
- `00_documentation_arsenal/contrats/chauffage/66_adaptation_consigne_vacances.md`
- `00_documentation_arsenal/contrats/vacances.md`

---

## 3. Cartographie du chauffage en absence et vacances (FAITS)

Autorité décisionnelle unique : `10_scripts/chauffage/decision_centrale.yaml` (hiérarchie explicitée en en-tête, `:23-55`). Source de présence : `binary_sensor.presence_famille_unifiee` (`12_template_sensors/presence/global.yaml:47`, `delay_on 3s` / `delay_off 30s`, `:51-52`).

| Régime | Entités clés | Décision produite | Référence |
|---|---|---|---|
| **Absence ordinaire** (hors Vacances) | `binary_sensor.chauffage_inhibition_geofencing_requise` (qualification hystérésis) + `input_boolean.chauffage_inhibition_geofencing` (état mémorisé) | Niveau 3b → `comfort` si zone froide sous seuil, sinon `reduced` | `decision_centrale.yaml:229-231` ; contrat `60` §4, §6 |
| **Vacances déclarées** | `binary_sensor.vacances_actives` | Niveau 2 → `reduced` par défaut ; consigne réduite **adaptée** à `input_number.chauffage_consigne_vacances` | `decision_centrale.yaml:211,214-216` ; `vacances_actives.yaml:45-50` ; contrat `66` |
| **Avant retour de vacances** | `input_boolean.pre_confort_actif_calcule` | Niveau 2, branche Vacances → `comfort` si pré-confort actif | `decision_centrale.yaml:212-213` |
| **Retour effectif** | présence réelle ⇒ `vacances_actives → off` | sortie branche Vacances → branche présence | `decision_centrale.yaml:221-227` |

**Faits structurants confirmés :**

- **F-CH-1.** Le chauffage ne se **coupe** jamais en absence ; il **réduit** (`reduced`) ou maintient un confort d'appoint. Aucun veto d'extinction total n'existe dans la décision centrale (`decision_centrale.yaml:197-234`).
- **F-CH-2.** L'inhibition géofencing est un **plancher thermique réactivable par hystérésis**, sans borne temporelle : la sortie dépend du franchissement du seuil thermique, pas d'un compteur (contrat `60` §6, §7, INV-GEO-8). Le contrat exclut explicitement toute sémantique de sécurité/hors-gel (`60` §2).
- **F-CH-3.** Le pré-confort agit **à l'intérieur** de la branche Vacances (conversion `reduced → comfort`) et **ne lève jamais** le régime Vacances (`decision_centrale.yaml:211-216` ; contrat `65` §3, §9).
- **F-CH-4.** Les deux mécanismes de confort d'absence sont **mutuellement exclusifs au runtime** : la branche Vacances (`:211`) précède et court-circuite la branche géofencing (`:229`), cohérent avec l'interdiction contractuelle de « double confort d'absence » (`60` §7 ; `65` orthogonalité §… « indépendance & neutralité »).

---

## 4. Cartographie du « COOL » en absence (FAITS)

Autorité d'autorisation : `binary_sensor.autorisation_clim_cool` (`12_template_sensors/climatisation/autorisation/cool.yaml:28-36`).

| Régime | Entités clés | Effet | Référence |
|---|---|---|---|
| **Micro-absence** | `binary_sensor.presence_confort_thermique_stabilisee` (`delay_off 120s`) | aucune bascule de stratégie | `confort_thermique_stabilisee.yaml:29` |
| **Absence normale** (< ~8 h) | `sensor.consigne_clim_appliquee`, `sensor.seuil_allumage_clim_applique` | **continue de climatiser** sur consigne/seuils **absence** | `decision/consigne.yaml:33-45` ; `seuils_on_off/cool/on.yaml:39-46` |
| **Absence prolongée** (≥ ~8 h) | `binary_sensor.clim_extinction_absence_prolongee_autorisee` | **veto total du `COOL`**, sans plafond thermique | `blocages/absence_longue.yaml:22-26` ; `autorisation/cool.yaml:35` |
| **DRY en absence** | `autorisation/clim_dry` | DRY exige `présence OU babysitting` → bloqué dès l'absence | `autorisation/dry.yaml:33-39` |
| **Retour détecté** | présence ⇒ annulation du timer, présence stabilisée `on` | `COOL` ré-autorisé, consigne **présence** — **réactif** | `start_timer_absence.yaml:56-63` |

**Faits structurants confirmés :**

- **F-COOL-1.** Le veto total après absence prolongée repose sur `binary_sensor.clim_extinction_absence_prolongee_autorisee` = (`presence_confort_thermique_stabilisee` off) ET (`timer.absence_longue_clim` idle) (`absence_longue.yaml:22-26`). Le timer est de 8 h (`timer_absence_longue.yaml`).
- **F-COOL-2.** L'extinction est un **veto binaire sans plafond** : aucune consigne de repli n'est appliquée au-delà du seuil ; la seule condition d'extinction est portée par `autorisation/cool.yaml:35`.
- **F-COOL-3.** Le domaine Vacances **n'intervient pas** dans la décision estivale : `autorisation/cool.yaml` ne lit ni `binary_sensor.vacances_actives`, ni `input_select.mode_maison`, ni `input_datetime.fin_vacances`. Recherche sur `12_template_sensors/climatisation` et `11_automations/climatisation` : **aucune** occurrence de `fin_vacances` / `pre_confort` / anticipation. Le seul point de lecture de `mode_maison` en climatisation (`11_automations/climatisation/modes.yaml`) gouverne le **chauffage-par-clim d'hiver**, jamais le `COOL` d'été.
- **F-COOL-4.** Il n'existe **aucun** pré-refroidissement ni mécanisme d'anticipation du retour. La remise en route est **purement réactive** au retour de présence (`start_timer_absence.yaml:56-63`).
- **F-COOL-5.** Ce comportement est **conforme au runtime actuel** ; l'audit n'a démontré **aucune non-conformité d'exécution** (pas de bug).

---

## 5. Comparaison factuelle

| Axe | CHAUFFAGE (hiver) | CLIMATISATION `COOL` (été) |
|---|---|---|
| Source de vérité de l'absence | `presence_famille_unifiee` (brut, 3s/30s) ; Vacances = `vacances_actives` | `presence_confort_thermique_stabilisee` (120s) pour consigne/seuils/DRY ; `presence_famille_unifiee` pour le timer 8 h |
| Prise en compte du mode Vacances | **Oui**, priorité Niveau 2 + consigne dédiée (`66`) | **Non** — jamais lu (F-COOL-3) |
| Distinction quotidien / vacances | **Oui** : absence ordinaire → géofencing ; Vacances → régime dédié + pré-confort | **Non** : seuil 8 h unique, indifférent au motif |
| Consigne en absence | Vacances : `chauffage_consigne_vacances` ; ordinaire : consigne réduite | `input_number.clim_consigne_absence` tant que < 8 h |
| Veto total | **Non** (réduit, ne coupe pas) | **Oui**, dur, après 8 h (`autorisation/cool.yaml:35`) |
| Plafond / plancher | **Plancher** thermique par hystérésis (`60`) | **Aucun** plafond |
| Anticipation du retour | **Oui** (pré-confort, `65`) | **Aucune** |
| Source de la date de retour | `input_datetime.fin_vacances` | inexistante côté `COOL` |
| Logique de reprise | présence ⇒ `vacances_actives off` ⇒ branche présence | présence ⇒ annule timer + stabilisée on ⇒ `COOL` ré-autorisé (réactif) |
| Modélisation d'inertie | capteurs d'inertie de reprise (diagnostic seul) | **aucune** pour le `COOL` |
| Comportement au redémarrage | recalcul idempotent boot-proof (`65` §5ter) | timer ré-armé (voir §10 — question ouverte) |
| Observabilité / diagnostic | `sensor.pre_confort_raison`, `sensor.vacances_raison`, notification persistante | `sensor.clim_verdict_cool`, `sensor.clim_raison_decision` (aucune raison « pré-refroid », inexistante) |
| Action manuelle | override `mode_confort_chauffage` (souverain) ; `pre_confort_enable` | consignes/seuils absence réglables ; aucun interrupteur d'anticipation |
| Dépendance à l'UI | UI non décisionnaire (notification = projection) | UI non décisionnaire |

---

## 6. Fonctionnement du pré-confort retour Vacances (FAITS)

### 6.1 Entités

| Rôle | Entité | Fichier |
|---|---|---|
| Date de retour (source) | `input_datetime.fin_vacances` | `07_input_datetimes/vacances/vacances.yaml:65` |
| Durée d'anticipation (fixe, transitoire) | `input_number.duree_prechauffage_retour_vacances` (min 3 / max 24 h) | `03_input_numbers/chauffage/duree_prechauffage_vacances.yaml:34-39` |
| Régime Vacances effectif | `binary_sensor.vacances_actives` | `12_template_sensors/modes/vacances_actives.yaml` |
| Disjoncteur opérateur | `input_boolean.pre_confort_enable` | `05_input_booleans/chauffage/preconfort.yaml:18` |
| Début / fin de fenêtre (ts) | `sensor.pre_confort_debut_ts` = `fin_ts − durée×3600` ; `sensor.pre_confort_fin_ts` = `as_timestamp(fin_vacances)` | `pre_confort_debut_ts.yaml:41`, `:62` |
| Validité de fenêtre | `binary_sensor.pre_confort_fenetre_valide` (`debut < fin`) | `pre_confort_fenetre_valide.yaml:39` |
| Fenêtre matérialisée | `input_datetime.pre_confort_debut_calcule` / `..._fin_calcule` | `07_input_datetimes/chauffage/fenetre_preconfort.yaml` |
| **Vérité opérationnelle unique** | `input_boolean.pre_confort_actif_calcule` | `05_input_booleans/chauffage/preconfort.yaml:22` |
| Mémoire de cycle | `input_boolean.pre_confort_cycle_consomme` / `..._cycle_override` | `05_input_booleans/chauffage/preconfort_cycle.yaml` |
| Timers instrumentaux | `timer.pre_confort_jusqua_debut` / `..._jusqua_fin` (`restore: false`) | `08_timers/chauffage/preconfort.yaml` |
| Diagnostic | `sensor.pre_confort_raison` | `12_template_sensors/chauffage/pre_confort/preconfort_raison.yaml` |

### 6.2 Chaîne (FAITS)

- **Fenêtre** = `[fin_vacances − durée ; fin_vacances]`. La borne de fin est la **date de retour** elle-même ; le début recule d'une durée fixe utilisateur (`pre_confort_debut_ts.yaml:41`, `:62`). Ce n'est **pas** un seuil thermique (contrat `65` §5).
- **Orchestration strictement événementielle**, sans polling : triggers = `homeassistant start`, `systeme_stable→on`, changement d'entrées de fenêtre/Vacances/enable, fin des timers instrumentaux (`orchestrateur.yaml:42-72`).
- **Éligibilité** (`orchestrateur.yaml:88-96`) : `pre_confort_enable` on ET `systeme_stable` on ET `vacances_actives` on ET `fenetre_valide` ET ts>0 ET **pas** `cycle_consomme` ET **pas** `cycle_override`.
- **Matérialisation** : avant fenêtre → off + armement des timers (`:139-155`) ; dans fenêtre → `pre_confort_actif_calcule` on (`:160-174`) ; sinon/non-éligible → off + cancel (`:124-135`, `default:176-188`).
- **Injection en décision** : lecture **directe** du booléen en branche Vacances (`decision_centrale.yaml:212`) → `comfort` (raison `pre_confort_vacances`).
- **Garde-fous** : anti-tôt (`now ≥ debut_ts`, `:160`) ; sortie stricte (`timer_jusqua_fin` + `default`) ; **une seule activation par cycle** — première montée → `cycle_consomme` on (`cycle.yaml:43-46,72-78`), l'éligibilité l'exclut ensuite (`orchestrateur.yaml:95`) ; override opérateur pendant la fenêtre → `cycle_override` on + `actif_calcule` off, invalidation définitive du cycle (`cycle.yaml:83-103` ; contrat `65` §3bis, §7) ; réinitialisation exclusivement sur `vacances_actives → off` (`cycle.yaml:108-116`).
- **Boot-proof** : recalcul complet sur `homeassistant start` / `systeme_stable→on` ; timers `restore: false` reconstruits par recalcul idempotent (contrat `65` §5ter).

### 6.3 Contrat vs runtime — écart de couche (FAIT + INTERPRÉTATION)

- **FAIT.** Le contrat `65` (§3, §4, §5ter) décrit une « autorisation simulée `comfort` **injectée dans la couche `70_autorisation_thermostat`** ». La recherche des consommateurs de `input_boolean.pre_confort_actif_calcule` ne révèle **aucun** capteur intermédiaire de couche « 70 » ; la décision centrale lit le booléen **directement** (`decision_centrale.yaml:212`).
- **INTERPRÉTATION (non tranchée).** Le comportement observé est conforme à l'**intention** du contrat (confort conditionnel, souveraineté de la décision préservée), mais la matérialisation par une couche « 70 » distincte n'est pas présente : il s'agit d'un **écart de couche/vocabulaire documentaire**, non d'un défaut fonctionnel. À confirmer par lecture exhaustive du contrat `70` et de son amendement (hors périmètre de cette trace).

---

## 7. Différences physiques et fonctionnelles entre chauffage et refroidissement

Le rapport **refuse explicitement** de présenter chauffage et refroidissement comme deux mécanismes simplement inverses.

**Constats fonctionnels (INTERPRÉTATION à soumettre, non érigée en règle) :**

- Une maison **excessivement froide** en absence hivernale peut constituer en soi un état indésirable (dérive du bâti, reprise violente) — ce que le plancher géofencing (`60`) vise précisément à éviter.
- Une maison à ~28 °C en absence estivale **n'est pas nécessairement un échec fonctionnel** : personne n'est présent, et la sobriété est légitime.
- Pour le refroidissement, le problème principal peut apparaître **non pendant l'absence, mais au retour** : le besoin est alors de **restaurer le confort avant une échéance utile**, pas nécessairement de maintenir un plafond pendant toute l'absence.
- Les dynamiques physiques diffèrent (apport thermique vs évacuation ; vitesse de chauffe ≠ vitesse de refroidissement), ce qui interdit de transposer tel quel un modèle calibré pour l'un vers l'autre.

Ces constats restent des **lectures fonctionnelles à soumettre à décision** (voir §11), et ne sont pas transformés en règle normative.

---

## 8. Limites des analogies étudiées

### 8.1 Analogie « plancher chauffage ↔ plafond COOL » — limitée, non démontrée

- **FAIT.** L'inhibition géofencing chauffage cherche à éviter une dérive **froide** excessive en absence (`60` §2).
- **INTERPRÉTATION.** Le `COOL` peut **légitimement** autoriser une dérive chaude quand personne n'est présent ; un **plafond estival permanent ne répond pas nécessairement au besoin réel**. L'analogie « inhibition géofencing → plafond COOL » est donc **limitée**.
- **Réserve explicite.** Le pré-confort retour Vacances constitue **potentiellement** une analogie plus pertinente que l'inhibition géofencing, **sans que cela conclue** que le plafond serait inutile ni que le pré-refroidissement serait la solution retenue.

### 8.2 Analogie « pré-confort Vacances ↔ pré-refroidissement » — pertinente mais partielle

- **FAIT.** Le pré-confort repose sur une **date de retour connue** (`fin_vacances`) et sur le **régime Vacances déclaré** (`vacances_actives`, `orchestrateur.yaml:91`).
- **INTERPRÉTATION.** Ce patron ne couvre pas directement : une absence **quotidienne** de plus de 8 h ; une absence **non déclarée** comme Vacances ; un retour dont **l'heure est inconnue**. L'incident déclencheur relève typiquement de ces cas non couverts.

**Distinction à préserver (FAIT terminologique) — quatre situations à ne jamais confondre :**
1. absence quotidienne normale ;
2. absence quotidienne prolongée (> 8 h) ;
3. vacances déclarées (`vacances_actives = on`) ;
4. préparation anticipée du retour de vacances (pré-confort).

> L'incident initial **ne doit pas** être assimilé à un cas Vacances si le mode Vacances n'était pas actif.

---

## 9. Points de robustesse et fragilités constatées

### 9.1 Robustesse (FAITS)

- Pré-confort **boot-proof** par recalcul idempotent (contrat `65` §5ter ; `orchestrateur.yaml:42-49`).
- Dégradation propre du pré-confort sur données invalides : `pre_confort_debut_ts` / `_fin_ts` → `unknown` si `fin_vacances`/durée invalides ; `fenetre_valide` off ; diagnostic `sensor.pre_confort_raison` (états `fin_vacances_invalide`, `duree_invalide`, `hors_fenetre_apres`, `cycle_consomme`, `cycle_override`…) (`preconfort_raison.yaml`).
- Exclusion mutuelle géofencing / pré-confort garantie par l'ordre des branches (`decision_centrale.yaml:211` avant `:229`).

### 9.2 Fragilités du modèle chauffage — à ne pas masquer (FAITS + INTERPRÉTATIONS)

- **FAIT.** Durée d'anticipation **fixe et pilotée par helper** (`input_number.duree_prechauffage_retour_vacances`), au **statut transitoire assumé par le contrat** (`65` §5ter : « source temporelle transitoire — mécanisme normatif conservé »), en attendant une estimation fondée sur la physique observée (`65` §5bis).
- **FAIT.** La mémoire de cycle est réinitialisée **exclusivement** sur `vacances_actives → off` (`cycle.yaml:108-116`).
- **INTERPRÉTATION.** Comme `vacances_actives` dépend de `presence_famille_unifiee` (`vacances_actives.yaml:45-50`) dont le débruitage est limité (3s/30s, `presence/global.yaml:51-52`), une **bascule brève de présence** pendant les vacances peut faire chuter `vacances_actives`, donc **réinitialiser la mémoire de cycle** (et rouvrir un droit d'anticipation, redéclencher la notification). Sensibilité réelle à documenter, non quantifiée ici.
- **FAIT + INTERPRÉTATION.** Écart de couche annoncé/réel du §6.3.
- **INTERPRÉTATION.** Le modèle chauffage **n'est donc pas un modèle parfait à recopier** ; toute transposition devrait traiter ces réserves.

### 9.3 Fragilité fonctionnelle côté COOL (FAIT + INTERPRÉTATION)

- **FAIT.** Le timer d'absence longue utilise `presence_famille_unifiee` brut (`start_timer_absence.yaml:36-40`), tandis que consigne/seuils/DRY utilisent la présence stabilisée 120 s. Asymétrie de robustesse **interne** au domaine COOL.

---

## 10. Sémantique du timer d'absence longue au redémarrage (QUESTION OUVERTE)

**FAITS (runtime exact) :**
- Le timer `timer.absence_longue_clim` est déclaré **avec restauration** : `restore: true`, durée `08:00:00` (`08_timers/climatisation/timer_absence_longue.yaml`).
- L'automation `11_automations/climatisation/cool/start_timer_absence.yaml` se déclenche notamment sur `homeassistant start` (`:36-40`), puis, après un `delay` de 5 s, si `presence_famille_unifiee` est `off`, appelle `timer.start` sur ce timer (`:44-54`). `timer.start` sans durée réarme la **durée configurée complète**.
- Conséquence : **un redémarrage de Home Assistant alors que la maison est absente réarme le compte à rebours pour 8 h pleines**, ce qui neutralise en pratique la restauration du temps écoulé.

**Deux sémantiques restent possibles (INTERPRÉTATIONS non tranchées) :**
1. mesurer **8 h physiques continues** d'absence (le réarmement serait alors un écart) ;
2. exiger **8 h d'absence observée de manière fiable depuis la dernière initialisation** du système (le réarmement au démarrage serait alors **intentionnel et prudent** — on ne fait pas confiance à une continuité non observée).

**Statut.** Aucun contrat opposable établissant l'intention n'a été trouvé pour ce point. Le comportement est **décrit exactement** ici mais **n'est pas qualifié de bug** : il reste **question ouverte** tant que l'intention opposable n'est pas fixée (voir §11 Q1).

---

## 11. Questions ouvertes (aucune réponse normative dans ce lot)

1. Quelle est la **sémantique exacte** des 8 h d'absence du `COOL` après un redémarrage (8 h physiques continues vs 8 h observées depuis la dernière initialisation) ?
2. Le comportement actuel de l'**absence quotidienne prolongée** (veto total) doit-il être **conservé** comme compromis énergétique ?
3. Les **vacances** doivent-elles constituer un régime `COOL` **distinct** de l'absence ordinaire ?
4. Pendant les vacances, le `COOL` doit-il être **totalement arrêté** ou seulement **très fortement réduit** ?
5. Arsenal doit-il viser une **température cible à l'heure de `fin_vacances`** ?
6. Le pré-refroidissement, s'il était étudié, devrait-il utiliser une **durée fixe initiale** ou une **estimation fondée sur la physique observée** ?
7. Quel comportement si le **retour réel** est **anticipé, retardé ou annulé** ?
8. Un éventuel pré-refroidissement devrait-il **lever un veto**, **sélectionner une consigne dédiée**, ou **injecter une nouvelle décision** ?
9. Une **architecture partagée** chauffage/refroidissement est-elle justifiée, ou créerait-elle un **couplage artificiel** au regard des différences physiques et contractuelles (§7) ?
10. Comment **distinguer proprement** une longue absence quotidienne (> 8 h) d'une période de vacances déclarée ?

*Note transverse (FAIT).* Un troisième consommateur de « retour de vacances » existe déjà — `11_automations/ecs/desinfection_retour_vacances.yaml` — mais il agit **sur front** `input_select.mode_maison` Vacances→Normal (`:37-41`), en **réaction** au retour, non en **anticipation**. Il n'est donc pas un précédent d'anticipation ; il est cité pour complétude de l'axe « préparation du retour ».

---

## 12. Conclusion d'audit

- Les deux domaines gèrent l'absence selon des **modèles asymétriques et non inversables** : le chauffage distingue absence ordinaire / vacances / anticipation du retour et ne coupe jamais ; le `COOL` distingue seulement absence normale / absence prolongée, sans mode Vacances, sans anticipation, avec un **veto total** après 8 h.
- Le pré-confort retour Vacances est un patron **réel, contractualisé et boot-proof**, mais **partiel** (dépend d'une date et d'un régime Vacances déclarés) et **non exempt de réserves** (durée fixe transitoire, réinitialisation de cycle sensible à la présence, écart de couche annoncé/réel).
- Les analogies « plafond estival » et « pré-refroidissement » sont **documentées comme limitées et non démontrées** ; aucune n'est privilégiée.
- **Le runtime n'a pas été modifié.** **Aucun contrat normatif n'a été modifié.** **Aucune architecture cible n'a été décidée.**
- **Un second travail de réflexion (conception) sera nécessaire avant tout chantier**, à partir des questions ouvertes du §11 et des différences physiques du §7.

---

*Rapport d'audit comparatif — trace documentaire, non normative, non prescriptive. Statique, lecture seule.*
