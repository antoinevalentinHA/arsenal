# Audit — Désinfection ECS hebdomadaire pendant les vacances

> **Statut :** rapport d'audit **statique, lecture seule** — constat **confirmé**
> **Constat :** `ECS-DESINF-VAC-1` (🟠) — la désinfection ECS **hebdomadaire** n'est **pas inhibée** pendant le mode Vacances : elle se déclenchera au créneau programmé (jour + heure) alors que l'utilisateur attend qu'aucune désinfection n'ait lieu en son absence.
> **Constat corollaire :** `ECS-DESINF-VAC-2` (🟠) — l'interrupteur d'activation `input_boolean.ecs_desinfection_active` est **inerte** (aucun consommateur ne le lit) : « Activation : Désactivé » n'empêche pas le cycle.
> **Domaine :** `ecs` / `vacances`
> **Saisine :** observation propriétaire (capture UI ECS, mode Vacances actif, désinfection programmée « Jeudi 6:25 »).
> **Chemin d'archivage :** `00_documentation_arsenal/audits/01_rapports/ecs/audit_desinfection_hebdomadaire_pendant_vacances.md`
> **État du dépôt à la rédaction :** `origin/main` = `e2af0c6`
> **Nature :** observation et analyse par lecture du dépôt (contrats **et** runtime). **Aucune correction n'est appliquée** ; les options du §10 sont des hypothèses, à contractualiser avant tout patch (doctrine Arsenal : *contrat avant runtime*).

---

## 1. Saisine

Constat propriétaire, capture UI à l'appui :

- le **mode Vacances est actif** ;
- la **désinfection** est programmée **le jeudi à 6 h 25** (bloc « Désinfection » : *Jour = Jeudi*, *Heure = 6:25*, *Consigne = 59 °C*), tandis que le sous-bloc *Activation* affiche **« Désactivé »** ;
- attente métier énoncée : **pendant les vacances, la désinfection ne doit pas se faire** ; elle est prévue **au retour** de vacances.

Question posée : *ce point est-il correct — la désinfection hebdomadaire est-elle bien inhibée pendant l'absence ?*

**Réponse : non.** En l'état du dépôt, la désinfection hebdomadaire **se déclenchera** au créneau « Jeudi 6:25 » même en mode Vacances. Le détail de la chaîne et des gardes manquantes suit.

---

## 2. Deux mécanismes de désinfection distincts (à ne pas confondre)

Le domaine ECS porte **deux** chaînes de désinfection **indépendantes** :

1. **Désinfection hebdomadaire** — récurrente, sur créneau *jour + heure* (ici *Jeudi 6:25*).
   Chaîne : `binary_sensor.ecs_creneau_desinfection_en_cours` → `ECS - Veille désinfection` (`10250000000002`) → `script.chauffage_ecs_cycle` (`mode: desinfection`).

2. **Désinfection au retour de vacances** — ponctuelle, à la sortie d'une absence *longue* (timer 6 j).
   Chaîne : `timer.vacances_longues_ecs` → `timer.finished` → `input_boolean.ecs_desinfection_retour_due` → `ECS - Désinfection fin vacances` (`10250000000021`).

Le chantier `VAC-IMP-5` (cf. `04_chantiers/vacances/`, `05_clotures/vacances/`) a **entièrement** porté sur la chaîne **(2)** — sa légitimité, sa détection de complétion, son idempotence. **La présente saisine porte sur la chaîne (1)**, qui n'a pas été instruite sous cet angle. Les deux ne doivent pas être amalgamées : corriger (2) ne corrige **pas** (1).

---

## 3. Chaîne runtime de la désinfection hebdomadaire (preuve)

### 3.1 Le capteur de créneau — calcul pur *jour + heure*, sans aucune garde

`12_template_sensors/ecs/fenetres_chauffe/desinfection.yaml` (`binary_sensor.ecs_creneau_desinfection_en_cours`) :

- lit **uniquement** `input_datetime.ecs_desinfection_heure` (l. 28) et `input_select.ecs_desinfection_jour` (l. 29) ;
- passe à `on` sur la micro-fenêtre `[HH:MM ; HH:MM+5 min)` du jour cible (l. 41-48) ;
- **ne lit ni le mode Vacances, ni `ecs_desinfection_active`, ni aucun blocage.** C'est un calcul stateless assumé (« Aucune action / aucun déclenchement », l. 13-16).

Conséquence : en mode Vacances, le jeudi à 6 h 25, ce capteur bascule `off → on` exactement comme un jeudi ordinaire.

### 3.2 La veille — déclenche le cycle sans garde d'inhibition

`11_automations/ecs/veilles/veille_desinfection.yaml` (`10250000000002`) :

- **déclencheur** : `binary_sensor.ecs_creneau_desinfection_en_cours` `off → on` (l. 30-34), plus rattrapage au retour de `systeme_stable` (l. 36-38) ;
- **conditions** (l. 40-51) : `systeme_stable == on`, `creneau == on`, `ecs_cycle_en_cours == off` ;
- **action** (l. 53-56) : `script.chauffage_ecs_cycle` avec `mode: "desinfection"`.

**Aucune** des trois conditions ne teste le contexte Vacances **ni** l'interrupteur `ecs_desinfection_active`. Ces gardes sont, en mode Vacances, toutes satisfiables : `systeme_stable` n'a pas de lien avec l'absence, et `ecs_cycle_en_cours` est `off` au repos. Le cycle **part**.

### 3.3 Le script de cycle — exécute sans arbitrage de contexte

`10_scripts/ecs/cycle.yaml` (`script.chauffage_ecs_cycle`) : orchestrateur d'exécution pur. Son en-tête l'affirme explicitement — « Aucun déclenchement horaire », « Aucun arbitrage planning / présence », « Aucune décision métier ECS globale » (l. 60-65). Il **ne défend pas** contre un lancement en vacances : ce n'est pas son rôle. La cible `desinfection` porte la consigne haute `input_number.ecs_temperature_desinfection` (59 °C ici) (l. 163-165).

**Verdict de la chaîne (1) :** rien, du capteur au script, ne s'oppose à une désinfection hebdomadaire pendant l'absence.

---

## 4. Le contraste probant : la chauffe ponctuelle, elle, est bien inhibée

La chaîne **ponctuelle** (chauffe hebdo matin/soir) suit exactement le même patron *créneau → veille → cycle*, **mais** sa veille porte la garde manquante côté désinfection :

`11_automations/ecs/veilles/veille_chauffe_ponctuelle.yaml` (`10250000000001`), condition l. 48-51 :

```yaml
# 🔒 BLOCAGE PLANIFICATION
- condition: state
  entity_id: input_boolean.ecs_blocage_planifiee
  state: "off"
```

Or `input_boolean.ecs_blocage_planifiee` est posé **`on`** à l'entrée effective en Vacances (`11_automations/modes/vacances/application_debut.yaml`, l. 89-93). La chauffe ponctuelle est donc **effectivement bloquée** en vacances — **la désinfection hebdomadaire ne l'est pas**. Deux chaînes jumelles, une seule gardée : c'est l'asymétrie au cœur du constat.

> ⚠️ **Nuance contractuelle importante — ne pas « corriger » en ajoutant `ecs_blocage_planifiee` à la veille désinfection.** Le contrat `contrats/ecs/05_etats_memoire_planification.md` §3.1 (l. 66-67) verrouille : *« Seul lecteur-condition [de `ecs_blocage_planifiee`] : l'automation `veille_chauffe_ponctuelle` »*. Étendre ce blocage à la désinfection **violerait** ce contrat d'écrivain/lecteur unique. La garde propre à la désinfection est un **autre** état : `ecs_desinfection_active` (cf. §5).

---

## 5. Cause racine : `ecs_desinfection_active` est un interrupteur mort

L'architecture **prévoyait** une garde dédiée à la désinfection, mais elle n'est **jamais consommée**.

**Intention documentée et écrite au runtime :**

- `05_input_booleans/ecs/desinfection.yaml` définit `input_boolean.ecs_desinfection_active` avec pour rôle explicite : *« ON → le cycle de désinfection ECS hebdomadaire peut être déclenché automatiquement ; OFF → …désactivé »* (l. 10-13) ;
- le contrat `contrats/ecs/05_etats_memoire_planification.md` §3 (l. 47-57) le range parmi les états qui **« autorisent ou interdisent, sans jamais déclencher »** ;
- le cycle de vie l'actionne comme une garde de contexte : **éteint** à l'entrée Vacances (`application_debut.yaml`, l. 111-115, aux côtés de `mode_vaisselle`) et **rallumé** au retour (`11_automations/modes/normal.yaml`, l. 100-103). C'est exactement le geste attendu pour « suspendre la désinfection pendant l'absence ».

**Défaut :** **aucun** consommateur ne lit cet état. Recherche exhaustive du dépôt sur `ecs_desinfection_active` — occurrences uniquement dans : la **définition** du helper, les **deux écrivains** de cycle de vie (`application_debut.yaml`, `normal.yaml`), la **carte UI** (`18_lovelace/dashboards/ecs/reglages.yaml`, l. 130), les **contrats** et l'historique. **Ni le capteur de créneau (§3.1), ni la veille (§3.2)** ne le testent en condition.

L'interrupteur est donc **inerte** : le poser à `off` — que ce soit **manuellement** (l'UI « Activation : Désactivé » de la capture) ou **automatiquement** par l'entrée en Vacances — **ne change rien** au déclenchement. C'est la cause commune des deux constats :

- **`ECS-DESINF-VAC-1`** (le point de la saisine) : l'extinction *automatique* en Vacances est sans effet → désinfection en absence.
- **`ECS-DESINF-VAC-2`** : l'extinction *manuelle* est également sans effet → l'interrupteur d'activation ne protège personne, y compris hors vacances.

Un mécanisme présent, affiché comme actionnable, et **jamais effectif** : c'est une **dette de fiabilité** (fausse impression de couverture) — le même motif de gouvernance que celui relevé pour la chaîne (2) dans `rapport_observation_vac_imp_5.md` §5.

---

## 6. Ce que l'utilisateur voit vs. ce qui se passe

| Élément UI (capture) | Interprétation naturelle | Réalité runtime |
|---|---|---|
| Mode Vacances actif | « la maison sait que je suis absent » | vrai pour la chauffe ponctuelle (bloquée) ; **faux pour la désinfection** |
| Désinfection · Activation : **Désactivé** | « la désinfection est coupée » | **inerte** — l'état n'est lu par aucun déclencheur |
| Désinfection · Jour = Jeudi · Heure = 6:25 | « prochaine désinfection prévue jeudi » | **exact — et elle partira**, vacances ou non |

La capture est donc **cohérente avec le déclenchement** : le créneau « Jeudi 6:25 » est bien la fenêtre où, en l'état, le cycle de désinfection à 59 °C se lancera pendant l'absence.

---

## 7. Reconnexion à VAC-IMP-5 (item de vérification laissé ouvert)

Ce constat **tranche** une question explicitement laissée en suspens par l'instruction de `VAC-IMP-5` :

- `rapport_observation_vac_imp_5.md` §5 (l. 77) : *« Atténuation probable (**à vérifier**) : une désinfection ECS … indépendante existe — `ecs_veille_desinfection` … sans lien avec le timer de vacances. Si ce créneau régulier couvre l'hygiène ECS… **Cette substitution doit être vérifiée**. »*
- même rapport §8, recommandation 2 (l. 112) : *« vérification de la substitution par `ecs_veille_desinfection` … pour figer la criticité métier ».*

**Vérification faite ici :** la chaîne (1) est bien indépendante du timer de vacances — **et n'a aucune garde d'absence**. Deux corrections de lecture au passage :

1. cette désinfection est **hebdomadaire** (créneau conditionné à `today == jour_cible`, un seul jour de la semaine — cf. §3.1), et **non « quotidienne »** comme l'indiquait par approximation le §5 du rapport VAC-IMP-5 ;
2. loin d'être une simple « atténuation » de l'absence de la chaîne (2), son fonctionnement **pendant** l'absence est précisément le comportement **non désiré** signalé par la saisine.

---

## 8. Impact métier

- **Effet non désiré confirmé :** montée en température ECS haute (désinfection, ~59 °C) **pendant l'absence**, à chaque jeudi 6:25 traversé par les vacances — consommation d'énergie et sollicitation thermique à contre-emploi de l'intention « maison en veille ».
- **Interrupteur de sûreté non fonctionnel :** l'utilisateur ne peut pas suspendre la désinfection via « Activation : Désactivé » — ni manuellement, ni via le contexte Vacances. Toute confiance placée dans ce toggle est trompée (`ECS-DESINF-VAC-2`).
- **Criticité sanitaire :** *faible* — il s'agit d'un excès de désinfection (côté sûr de l'hygiène), non d'un manque. Le risque est **énergétique, fonctionnel et de gouvernance** (mécanisme affiché ≠ mécanisme effectif), non un risque sanitaire.
- **Gravité proposée : 🟠 (importance).** Comportement contraire à l'attente explicite, garde documentée inopérante, sur un domaine (ECS) à invariants stricts.

---

## 9. Confrontation contractuelle

| Source contractuelle | Ce qu'elle pose | Écart constaté |
|---|---|---|
| `contrats/ecs/05` §3 (l. 47-57) | `ecs_desinfection_active` **autorise ou interdit** la désinfection | L'état n'est lu par **aucun** consommateur → l'autorisation/interdiction est **ineffective** |
| `contrats/ecs/05` §3.1 (l. 66-67) | `ecs_blocage_planifiee` a **un seul** lecteur-condition : `veille_chauffe_ponctuelle` | Interdit d'étendre ce blocage à la désinfection → la garde désinfection **doit** passer par `ecs_desinfection_active` |
| `contrats/vacances.md` §10 (l. 394-399) | La logique d'**absence effective** (dont ECS) se lit sur `binary_sensor.vacances_actives` **uniquement** | Si une garde d'absence est ajoutée à la désinfection, sa **couche** doit être `vacances_actives` (comme le blocage ponctuel via `application_debut`/`application_fin`), pas la projection `mode_maison` |
| `contrats/ecs/09` (invariants) | Traçabilité de toute action ECS ; correction ou signalement de toute dérive | Dérive présente non signalée ; à instruire |

Aucun contrat n'**exige** aujourd'hui que la désinfection hebdomadaire soit inhibée en Vacances — c'est précisément le **trou contractuel** : l'intention existe (helper + cycle de vie) mais n'est **ni contractualisée comme invariant, ni instrumentée**. La correction devra donc **d'abord** poser le contrat (garde de désinfection = `ecs_desinfection_active`, couche d'absence = `vacances_actives`), **puis** le runtime, **puis** la CI.

---

## 10. Options de correction — hypothèses (aucune retenue)

> À arbitrer après réconciliation contractuelle. Toutes doivent respecter les invariants Arsenal (lecteur/écrivain unique, couche d'effectivité `vacances_actives`, *contrat avant YAML*).

1. **Rendre l'interrupteur effectif (recommandée, minimale, résout les deux constats).**
   Ajouter à `veille_desinfection.yaml` la condition `input_boolean.ecs_desinfection_active == on`, en miroir exact de la garde `ecs_blocage_planifiee` de `veille_chauffe_ponctuelle`. Comme cet interrupteur est déjà éteint à l'entrée Vacances et rallumé au retour, l'inhibition en absence en découle **gratuitement**, et le toggle manuel « Activation » redevient opérant. Ne touche **pas** à `ecs_blocage_planifiee` (respecte §3.1).

2. **Garde d'absence explicite.**
   Ajouter à la veille une condition `binary_sensor.vacances_actives == off`. Plus littéral vis-à-vis de la saisine, mais **ne répare pas** l'interrupteur mort (`ECS-DESINF-VAC-2` resterait ouvert) et introduit une seconde source de vérité là où l'option 1 en réutilise une existante. **Combinable** avec 1 si l'on veut séparer « désactivation manuelle » et « inhibition d'absence ».

3. **Report/rattrapage au retour.**
   Si un créneau de désinfection est *manqué* pendant l'absence, poser une désinfection due au retour (réutiliser le mécanisme souverain `ecs_desinfection_retour_due` de la chaîne (2)). Extension de confort, à considérer **après** 1, non nécessaire pour clore la saisine.

4. **Garde dans le capteur plutôt que la veille.**
   Écartée par symétrie avec le patron ponctuel (la garde vit dans la **veille**, le capteur reste un calcul pur *jour+heure*) et pour préserver la nature stateless documentée du capteur (§3.1).

**Instrumentation CI attendue (toute option) :** un contrôleur analogue à `check_ecs_desinfection_retour_contracts.py` asseyant que la veille de désinfection **porte** la garde retenue (interdit la régression du « toggle mort »).

---

## 11. Statut et verdict

- **Constat `ECS-DESINF-VAC-1` (🟠) : CONFIRMÉ** — la désinfection ECS hebdomadaire n'est pas inhibée en Vacances ; elle se déclenchera au créneau « Jeudi 6:25 » pendant l'absence. La saisine est **fondée**.
- **Constat `ECS-DESINF-VAC-2` (🟠) : CONFIRMÉ** — `input_boolean.ecs_desinfection_active` est un interrupteur **inerte** (aucun lecteur-condition) ; « Activation : Désactivé » ne protège pas, en vacances comme hors vacances. **Cause racine commune.**
- **Chaîne (2) (désinfection au retour) :** hors périmètre de cette saisine ; son état reste celui décrit par `VAC-IMP-5` (traité runtime, validation partielle).
- **Verdict :** **PRÊT À CONTRACTUALISER PUIS CORRIGER.** Le défaut est reproductible par lecture, sa cause est cernée, et une correction minimale (option 1) existe. Conformément à la doctrine Arsenal, l'étape suivante est **contrat → runtime → CI**, non un patch direct.
- **Suite recommandée :** ouvrir un chantier `04_chantiers/ecs/` (candidat `ECS-DESINF-VAC`), poser l'invariant « la désinfection hebdomadaire respecte `ecs_desinfection_active` ; l'absence effective l'éteint via `vacances_actives` », puis livrer le lot runtime + CI.

---

*Rapport d'audit `ECS-DESINF-VAC-1` / `ECS-DESINF-VAC-2`. Établi en lecture seule du dépôt (contrats et runtime), sans patch, sans modification YAML ni runtime. Distingue faits observés, cause racine et hypothèses de correction ; aucune correction n'est proposée comme définitive.*
