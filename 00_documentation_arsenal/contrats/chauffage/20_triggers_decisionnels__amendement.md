# ==========================================================
# 🧠 ARSENAL — AMENDEMENT NORMATIF
#     CHAUFFAGE — TRIGGERS DÉCISIONNELS (V3 PRO)
#     Amendement : registres des triggers & purge des lignes fantômes
# ==========================================================
#
# 📌 STATUT :
#   AMENDEMENT au contrat de gouvernance `20_triggers_decisionnels.md`
#
# 🎯 OBJET :
#   Mettre `20` en conformité avec la doctrine des registres (`01`)
#   et la phase 3 (purification de `autorise_systeme`) :
#     1. scinder la rubrique « PRIORITÉ ZÉRO — OVERRIDES » en deux
#        registres distincts : SÉCURITÉ SYSTÈME et OVERRIDE OPÉRATEUR ;
#     2. purger les lignes de trigger FANTÔMES (sans entité-source
#        runtime réelle) ;
#     3. réaligner le vocabulaire géofencing sur `60` (stabilisation,
#        non « protection ») ;
#     4. acter qu'aucun trigger météo dédié n'existe ni n'est requis.
#
# 🧱 PRINCIPE DIRECTEUR :
#   « Une table plus petite mais strictement vraie » plutôt qu'une
#   pseudo-exhaustivité contenant des formulations sans réalité
#   runtime. Les lignes purgées sont attestées comme fantômes par
#   vérification runtime (voir §5, faits opposables).
#
# 🔒 SUBORDINATION :
#   • 00_gouvernance_chauffage.md (+ amendement)
#   • 01_doctrine_registres.md
#   Cohérent avec : 30 (+ amendement), 60 (réécriture), 70/90
#   (+ amendements), 80 (réécriture partielle)
#
# ==========================================================

---

## 1. Objet et nature

`20` n'est pas réécrit. Sa philosophie (« définir QUAND le cerveau doit
réfléchir à nouveau ») et l'essentiel de sa table sont confirmés. Cet
amendement corrige : le classement par registre de la tête de table, et la
présence de lignes sans support runtime.

> **Confirmation préalable (phase 3).** `input_boolean.chauffage_standby_force`
> n'est, et n'a jamais été, une source de trigger décisionnel. Le standby est
> post-décision (couche application) ; il n'a aucune raison de rappeler la
> Décision Centrale. La phase 3 n'a donc rien laissé d'implicite dans `20` :
> l'ancien couplage vivait dans la composition de `autorise_systeme`, jamais
> dans les triggers. Aucune correction de couplage standby n'est requise ici.

---

## 2. Scission de la tête de table par registre

La rubrique antérieure « PRIORITÉ ZÉRO — OVERRIDES UTILISATEUR / SYSTÈME »
amalgamait deux objets de registres irréductibles (`01` D0). Elle est scindée.

### 2.1 SÉCURITÉ SYSTÈME (registre sécurité)

> `binary_sensor.chauffage_autorise_systeme` est une **autorité de sécurité
> système pure** (cf. `30__amendement` R-30.1). Son trigger réveille la
> Décision Centrale sur toute transition de sécurité (OFF↔ON). Depuis la
> phase 3, ce capteur ne reflète plus que des causes de sécurité (blocage
> post-aération, indisponibilités) ; son trigger en hérite le sens purifié.

| Cause (sécurité système)   | Transition | Trigger | Criticité | Commentaire |
|----------------------------|------------|---------|-----------|-------------|
| chauffage_autorise_systeme | OFF → ON   | OUI     | CRITIQUE  | Levée d'interdiction de sécurité — revalidation complète |
| chauffage_autorise_systeme | ON → OFF   | OUI     | CRITIQUE  | Interdiction de sécurité immédiate |

> Ce trigger n'est PAS un override. Une sécurité s'impose par nature ; elle ne
> « contourne » rien par volonté. Le classer parmi les overrides entretiendrait
> une confusion de registre (violation D0).

### 2.2 OVERRIDE OPÉRATEUR (volonté humaine de contournement)

| Cause                   | Transition | Trigger | Criticité | Commentaire |
|-------------------------|------------|---------|-----------|-------------|
| mode_confort_chauffage  | OFF → ON   | OUI     | CRITIQUE  | Override prioritaire, contourne l'anti-rebond |
| mode_confort_chauffage  | ON → OFF   | OUI     | MAJEUR    | Retour régime normal |

Règles cardinales (inchangées, propres à l'override) :
- l'override opérateur contourne l'anti-rebond géoloc ;
- aucun délai de stabilisation n'est opposable à `mode_confort_chauffage` ;
- cette priorité ne contourne jamais les sécurités matérielles hors périmètre
  Arsenal.

> Distinction de registre : la sécurité (§2.1) **s'impose** ; l'override (§2.2)
> **contourne par volonté**. Les deux déclenchent un rappel, mais pour des
> raisons de natures différentes — ce que `20`, contrat des raisons de rappel,
> doit nommer distinctement.

---

## 3. Purge des lignes de trigger fantômes

Les lignes suivantes sont **abrogées** : elles ne correspondent à aucune
entité-source runtime (vérification §5). Leur abrogation ne crée aucun trou de
réveil, car les contextes concernés sont déjà couverts par des triggers réels
listés par ailleurs.

### 3.1 Rubrique géofencing — lignes « protection annulée par X » — ABROGÉES

- « protection annulée par présence » — ABROGÉE. Couverte par le trigger réel
  `presence_famille_unifiee`.
- « protection annulée par blocage » — ABROGÉE. Couverte par les triggers réels
  `chauffage_blocage_aeration` / `blocage_chauffage_poele` / fenêtre.
- « protection annulée par mode_maison » — ABROGÉE. Couverte par le trigger
  réel `mode_maison`.

La seule ligne géofencing conservée est la ligne réelle :

| Cause                            | Transition | Trigger | Criticité | Commentaire |
|----------------------------------|------------|---------|-----------|-------------|
| chauffage_inhibition_geofencing  | OFF → ON   | OUI     | CRITIQUE  | Entrée inhibition géofencing (stabilisation absence) |
| chauffage_inhibition_geofencing  | ON → OFF   | OUI     | CRITIQUE  | Sortie inhibition géofencing |

### 3.2 Rubrique « ATTENTE THERMIQUE » — ABROGÉE intégralement

Les quatre lignes (« entrée/sortie attente confort », « entrée/sortie attente
protection ») n'ont aucune entité-source runtime (`attente_*` inexistant). La
rubrique est abrogée. Le besoin thermique réel est porté par les transitions
de `sensor.chauffage_autorisation_cible` (§4.4 de `20`), déjà déclenchantes.

### 3.3 Rubrique « RAISON DOMINANTE » comme trigger — ABROGÉE

`sensor.chauffage_raison_calculee` (ou équivalent) n'est PAS un trigger et ne
doit jamais l'être : la raison est une **sortie** de la décision, non une
cause de rappel. La faire trigger créerait une remontée conséquence → cause
(violation D3) et un risque de boucle. La raison demeure un artefact de
diagnostic, hors surface de trigger.

---

## 4. Réalignement du vocabulaire géofencing sur `60`

Le vocabulaire « PROTECTION THERMIQUE », « protection », « confort différé »,
« Chauffe protection » est un résidu de l'ancienne doctrine géofencing. Il est
réaligné sur `60` (réécriture) :

- intitulé de rubrique : « ABSENCE — INHIBITION GÉOFENCING (STABILISATION
  THERMIQUE) » au lieu de « … / PROTECTION THERMIQUE » ;
- l'inhibition géofencing est un mécanisme de **stabilisation thermique
  d'absence** (registre stabilisation), jamais une « protection » (sécurité /
  bâti). Toute occurrence du terme « protection » dans la section géofencing de
  `20` est supprimée ou remplacée par « inhibition géofencing ».

---

## 5. Trigger météo — aucun, et c'est correct

> La modulation `suspension_relance_meteo` (cf. `70`/`90` amendements) agit sur
> `sensor.chauffage_autorisation_cible`. Or `20` déclenche déjà sur **tout
> changement** de `autorisation_cible`. La transition `comfort → neutre`
> produite par la météo est donc **nativement couverte**, sans trigger dédié.
>
> Aucun trigger météo ne doit être introduit. Introduire un trigger sur
> `meteo_favorable_chauffage` ou `chauffage_anticipation_meteo` serait une
> redondance inutile : la modulation se manifeste comme un changement de
> `autorisation_cible`, déjà déclenchant. Doctrinalement, la météo module
> l'intention, et le trigger sur l'intention suffit.

---

## 6. Faits opposables (vérification runtime)

Source : `11_automations/chauffage/decision_centrale_trigger.yaml`.

**Triggers réels (15 entités) :** `chauffage_autorise_systeme`,
`mode_confort_chauffage`, `pre_confort_actif_calcule`, `mode_maison`,
`aeration_episode_en_cours`, `aeration_confirmee`, `chauffage_blocage_aeration`,
`fenetre_ouverte_maison_avec_delai`, `blocage_chauffage_poele`,
`presence_famille_unifiee`, `chauffage_inhibition_geofencing`,
`chauffage_autorisation_cible`, `boiler_bridge_online`,
`chauffage_application_en_cours`, `systeme_stable` (+ timer anti-rebond géoloc,
+ reload script).

**Absences confirmées (lignes fantômes) :**
- aucune entité `protection_*` → lignes « protection annulée par X » fantômes ;
- aucune entité `attente_*` → rubrique « attente thermique » fantôme ;
- `raison_calculee` absent de la surface de trigger → ligne « raison
  dominante » fantôme.

**Absence confirmée de couplage standby :** `standby_force` absent de la
surface de trigger.

---

## 7. Invariants exposés (CI)

- **INV-TRIG-1** — `standby_force` n'est jamais une source de trigger
  décisionnel.
- **INV-TRIG-2** — `autorise_systeme` est classé trigger de **sécurité
  système**, distinct des overrides opérateur.
- **INV-TRIG-3** — Tout changement de `sensor.chauffage_autorisation_cible`
  rappelle la décision (couvre nativement `suspension_relance_meteo` ; aucun
  trigger météo dédié).
- **INV-TRIG-4** — Le vocabulaire de la section géofencing est aligné sur `60`
  (stabilisation, jamais « protection »).
- **INV-TRIG-5** — Toute ligne de la table des triggers correspond à une
  entité-source runtime réelle ; aucune ligne fantôme (pas d'entité
  `protection_*` / `attente_*`, raison non déclenchante).
- **INV-TRIG-6** — `raison_calculee` n'est jamais un trigger (interdiction de
  remontée conséquence → cause, D3).

---

## 8. Dépendances et portée

**Subordonné à :** `00_gouvernance_chauffage.md` (+ amendement) ·
`01_doctrine_registres.md`

**Complémentaire de :** `30_decision_centrale.md` (+ amendement) ·
`80_table_decision_canonique` (+ réécriture partielle)

**Cohérent avec :** `60` (réécriture) · `70`/`90` (amendements)

Cet amendement précise et purge `20` sans en réécrire la philosophie. Aucun
patch runtime n'est ouvert (l'automation de trigger réelle est déjà conforme à
la table purgée — c'est le contrat qui rattrape le runtime, pas l'inverse).

---

## 9. Note de cohérence runtime

Fait notable : la purge réalignе `20` sur un runtime **déjà conforme**.
L'automation `decision_centrale_trigger.yaml` n'a jamais implémenté les lignes
fantômes (elles n'existaient que dans le contrat). Cet amendement ne demande
donc aucun changement YAML : il supprime une dette documentaire (contrat
sur-spécifié par rapport au runtime), à l'inverse des divergences habituelles
où le runtime dérivait du contrat.

# ==========================================================
