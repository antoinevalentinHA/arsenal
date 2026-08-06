# 🧠 ARSENAL — ECS  
# États, mémoire et planification

Chemin : `/homeassistant/00_documentation_arsenal/contrats/ecs/05_etats_memoire_planification.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : États et mémoire ECS

---

## 1. Objet

Ce document définit les états runtime,
les mécanismes de mémoire persistante
et les règles de planification ECS.

Il garantit la stabilité décisionnelle
et l’intégrité historique.

---

## 2. États runtime

### 2.1 Verrou de cycle

 input_boolean.ecs_cycle_en_cours

Rôle :
Verrou logique exclusif de cycle ECS.

Invariants :

- un seul cycle simultané
- aucune libération anticipée
- aucun forçage manuel

---

### 2.2 État bouclage ponctuel

 input_boolean.bouclage_ecs_5_minutes_en_cours

Indique l’activation effective
du bouclage manuel temporisé.

---

## 3. Autorisations et blocages

Les états suivants autorisent ou interdisent,
sans jamais déclencher :

- ecs_blocage_planifiee
- ecs_desinfection_active
- bouclage_visiteur
- ecs_autocorrect_active

Ils ne constituent pas des ordres.

### 3.1 Cycle de vie de `ecs_blocage_planifiee` (double nature)

`input_boolean.ecs_blocage_planifiee` a une double nature :

- blocage manuel temporaire de l’utilisateur (toggle UI)
- blocage posé par le contexte Vacances

Sémantique : `on` = chauffe planifiée bloquée, `off` = normale.
Seul lecteur-condition : l’automation `veille_chauffe_ponctuelle`
(exige `off` pour autoriser la chauffe ponctuelle).

Cycle de vie côté contexte Vacances (couche effectivité) :

- pose : `binary_sensor.vacances_actives` → `on` (application Vacances)
- levée : transition réelle `binary_sensor.vacances_actives` → `off`
  (fin d’application Vacances), hors redémarrage

Préservation du blocage manuel :

- au redémarrage (`homeassistant: start`), le blocage n’est jamais forcé à
  `off` : un blocage manuel posé hors vacances survit au reboot
- la réconciliation d’un blocage-vacances résiduel (cycle terminé pendant
  un arrêt de Home Assistant) est assurée par la sortie de contexte
  `input_select.mode_maison` → `Normal`, qui lève alors le blocage

Invariants :

- la levée nominale est portée par l’effectivité (`vacances_actives`)
- la levée sur `mode_maison` → `Normal` est conservée comme filet de
  réconciliation de sortie/boot, jamais déclenchée par un toggle manuel
- aucune écriture ne force le blocage à `off` sur `homeassistant: start`

---

### 3.2 Cycle de vie de `ecs_desinfection_retour_due`

`input_boolean.ecs_desinfection_retour_due` est un état souverain de
planification mémorisant qu'une désinfection ECS au retour de vacances est due.

Sémantique : `on` = une désinfection-retour est due (légitimité établie par une
absence longue menée à terme) ; `off` = aucune désinfection-retour due.

Persistance : l'état est persistant. Il ne définit pas de valeur `initial`,
afin de survivre au redémarrage de Home Assistant. Côté registre HA, il porte
une catégorie mémoire (label `helper:memory` ou équivalent).

Écrivain souverain (unique) :

- pose (`→ on`) : exclusivement l'automation déclenchée par l'événement
  `timer.finished` de `timer.vacances_longues_ecs` (complétion naturelle).
  L'identifiant de cette automation sera attribué lors du patch runtime.
- réinitialisation (`→ off`) : exclusivement par l'**autorité de séquence de
  retour**, et **uniquement après un verdict final positif** (`reussite`, cf.
  §3.3). L'entité et l'identifiant de cette autorité seront attribués lors du
  patch runtime (objet proposé — cf.
  `04_chantiers/ecs/chantier_desinfection_hebdo_et_retour.md`).
- interdictions : `timer.cancel` (retour anticipé) ne pose jamais cet état ;
  aucune écriture manuelle ; aucun autre écrivain ; **aucune consommation avant
  verdict positif**.

Consommation (cible) : la dette n'est remise à `off` qu'après le verdict
`reussite` de la séquence (§3.3). Un appel de script accepté, un verrou pris,
une consigne envoyée, une température momentanément atteinte ou une fin d'appel
de script **ne valent pas** verdict. Sur échec, timeout, interruption ou preuve
indisponible, la dette **reste due**.

Idempotence : la désinfection de retour s'exécute au plus une fois par légitimité
établie. Un état `on` présent au démarrage est **réconcilié** (cf. §3.3 et
`10` §4.1), jamais relancé aveuglément ni consommé sans verdict positif.

> **Réconciliation (cible — écart runtime tracé, `origin/main` = `6068926`).** Le runtime
> réinitialise aujourd'hui la dette **immédiatement après l'appel** du script
> (`11_automations/ecs/desinfection_retour_vacances.yaml`), **avant** `ecs_fin_cycle_signal`,
> et **sans** trigger de réconciliation au démarrage (constats `ECS-DESINF-VAC`, chantier Lot 2).
> Le présent texte est la **cible** ; il est souverain pour le mécanisme de consommation.

Projection d'observabilité : `binary_sensor.ecs_desinfection_retour_vacances_autorisee`
est conservé comme projection 1:1 de `input_boolean.ecs_desinfection_retour_due`.
Il n'a plus de rôle décisionnel et ne lit plus `timer.vacances_longues_ecs` ni
son attribut `remaining`.

---

### 3.3 Verdict de séquence de désinfection-retour et consommation de la dette

La consommation de la dette (§3.2) est subordonnée à un **verdict de séquence**. Ce document est
**souverain** pour ce modèle ; `09` §2 en énonce les invariants, `10` §4.1 en porte la réconciliation
au reboot. **Aucune entité n'est créée par le présent texte** : l'entité porteuse du verdict et
l'autorité de séquence sont des **objets proposés** dont le nom/identifiant seront attribués au patch
runtime (cf. `04_chantiers/ecs/chantier_desinfection_hebdo_et_retour.md`).

États de verdict (vocabulaire canonique candidat) :

- `en_attente` — dette due, séquence non démarrée
- `en_cours` — cycle demandé / en cours, verdict non tranché
- `reussite` — ballon désinfecté **prouvé** : cible atteinte en mesure fraîche **et** complétion
  canonique `ecs_fin_cycle_signal`
- `echec` — cible non atteinte, cycle invalidé, ou refus initial
- `timeout` — attente bornée expirée sans preuve d'atteinte
- `preuve_indisponible` — mesure requise non fraîche (`provenance != 'mesure'`) au moment requis

Autorité et écriture :

- **autorité du verdict** : l'autorité de séquence de retour (objet proposé), **écrivain unique** du
  verdict et **seul** écrivain OFF de la dette
- **preuve exigée pour `reussite`** : atteinte `≥ cible − epsilon` en mesure fraîche **ET**
  `ecs_fin_cycle_signal` (fin exploitable, cf. `10` §8) — jamais une fin d'appel de script ni un pic instantané
- **consommation de la dette** : autorisée **si et seulement si** verdict `reussite`
- **cas interdisant la consommation** : `echec`, `timeout`, `preuve_indisponible`, `en_attente`,
  `en_cours` ⇒ dette **conservée**

Fail-safe : tout état `unknown`/`unavailable` ou toute mesure non fraîche **n'est jamais** interprété
comme `reussite`. Un cycle interrompu (absence de `ecs_fin_cycle_signal`) ne produit jamais `reussite`.

Reprise gardée (réconciliation, cf. `10` §4.1) : au démarrage, une dette `on` est réconciliée **sans
relance aveugle**. La reprise **ne lance pas** de cycle si l'une des gardes est fausse :

- la dette est `off` ;
- un cycle ECS est déjà en cours (`input_boolean.ecs_cycle_en_cours == on`) ;
- les observations thermiques nécessaires sont indisponibles ;
- un verdict positif antérieur solde déjà la dette.

La reprise est **idempotente** : au plus une exécution par légitimité établie.

**Circulation post-réussite (minimale, primitive existante).** Sur le verdict `reussite` — et
uniquement là — la séquence de retour appelle **une fois** `script.bouclage_ecs_5_minutes` (primitive
de bouclage **existante**, cf. `contrats/bouclage.md`) : décision ECS de circuler après réussite,
exécution et bornage (timer 5 min) assurés par le domaine Bouclage. Le lancement unique par réussite
découle des gardes **existantes** (verdict `en_cours` + dette `on`, retombées après consommation) ;
**aucun nouvel objet, aucun verrou, aucune durée** ne sont créés. ECS ne pilote **jamais**
`switch.prise_bouclage` directement et **n'introduit aucune vérité de bouclage** propre.

> **Limite de preuve.** Le résultat prouvé se limite à : **ballon désinfecté** (verdict `reussite`) +
> **circulation 5 min demandée** selon la primitive existante. La température du **retour de boucle**
> n'est **pas** prouvée (aucune sonde) ; la boucle n'est **jamais** déclarée « désinfectée » ; les
> tronçons terminaux non bouclés restent **hors garantie**. Aucun verdict « boucle » n'est créé.

---

### 3.4 Autorité effective de la désinfection hebdomadaire (`ecs_desinfection_active`)

`input_boolean.ecs_desinfection_active` est l'**autorité d'autorisation** de la désinfection ECS
**hebdomadaire** (récurrente, sur créneau *jour + heure*). Ce document est **souverain** pour son cycle
de vie ; `09` §2 en énonce l'invariant.

Sémantique : `on` = désinfection hebdomadaire autorisée ; `off` = interdite. Le helper **autorise ou
interdit**, il **ne déclenche jamais**.

Lecteur-condition (cible) : **unique** = la veille hebdomadaire `10250000000002`, qui exige
`ecs_desinfection_active == on` pour lancer un cycle. Le capteur de créneau
`binary_sensor.ecs_creneau_desinfection_en_cours` reste un **calcul pur** *jour+heure* et **ne lit
jamais** cette autorisation. `input_boolean.ecs_blocage_planifiee` reste **hors** de cette chaîne
(§3.1).

Cycle de vie (existant, inchangé) :

- extinction : à l'entrée effective en Vacances (`binary_sensor.vacances_actives → on`,
  `11_automations/modes/vacances/application_debut.yaml`) ⇒ inhibition de la désinfection hebdomadaire
  pendant l'absence
- réarmement : au retour (`input_select.mode_maison → Normal`, `11_automations/modes/normal.yaml`)

Conséquence : rendre le lecteur effectif rend **opérant** le toggle manuel **et** inhibe la désinfection
hebdomadaire en vacances via le cycle de vie **déjà en place** — sans nouvel écrivain.

> **Réconciliation (cible — écart runtime tracé, `origin/main` = `6068926`).** Aucun lecteur-condition
> ne consomme aujourd'hui `ecs_desinfection_active` (constat `ECS-DESINF-VAC-2`) : l'interrupteur est
> **inerte** et la désinfection hebdomadaire n'est pas inhibée en vacances (`ECS-DESINF-VAC-1`).
> Correction : chantier Lot 1.

---

## 4. Modes utilisateur

Modes disponibles :

- mode_vaisselle
- mode_enfants

Les modes :

- modifient un contexte
- reconfigurent un planning
- ne déclenchent jamais directement

### 4.1 Cycle de vie de la sauvegarde de `mode_vaisselle` (contexte Vacances)

`input_boolean.mode_vaisselle` est une préférence utilisateur persistante.
Son écriture nominale relève de l’utilisateur (UI) et du wrapper transitoire
`script.ecs_vaisselle_lancer_via_bouton`, qui restaure toujours l’état initial.

Le contexte Vacances éteint cette préférence à l’entrée effective et doit donc
en mémoriser l’état antérieur pour le restaurer à la sortie effective.

Mémoire dédiée :

 input_text.ecs_mode_vaisselle_sauvegarde

- nature : `helper:memory` (dernier état connu, non décisionnel)
- valeurs : `on`, `off`, ou `""` (sentinelle : aucune sauvegarde en cours)

Persistance :

- ce helper ne définit **pas** de clé `initial`
- Home Assistant restaure donc sa dernière valeur au redémarrage
- une sauvegarde valide (`on`/`off`) survit ainsi à un redémarrage survenant
  pendant des vacances longues
- la sentinelle vide n’est établie qu’à l’initialisation manuelle et après
  une restauration réussie

Entrée effective (`binary_sensor.vacances_actives` → `on`) :

- si la sauvegarde est vide : sauvegarder l’état courant (`on`/`off`) de
  `input_boolean.mode_vaisselle`
- éteindre `input_boolean.mode_vaisselle`

Sortie effective (`binary_sensor.vacances_actives` → `off`) :

- si la sauvegarde vaut `on` ou `off` : restaurer `input_boolean.mode_vaisselle`
  à cette valeur, puis remettre la sauvegarde à la sentinelle vide
- si la sauvegarde est vide ou invalide : abstention de restauration

Invariants :

- toute extinction Vacances dispose d’un chemin de restauration explicite
- aucune re-sauvegarde par-dessus une sauvegarde déjà valide (idempotence,
  y compris au redémarrage : la valeur restaurée n’est pas écrasée)
- aucune restauration n’invente une valeur
- la couche est l’effectivité (`vacances_actives`), comme les autres
  conséquences d’absence effective

---

## 5. Planification

La planification ECS définit uniquement
les fenêtres d’autorisation.

Elle inclut :

- jours actifs matin / soir
- heures hebdomadaires
- jour et heure de désinfection

Règle absolue :

> La planification n’est jamais un ordre de chauffe.

---

## 6. Mémoire temporelle

### 6.1 Horodatages persistants

 input_datetime.ecs_dernier_cycle 
 input_datetime.ecs_pic_thermique

Ces valeurs :

- sont écrites automatiquement
- ne sont jamais modifiables manuellement
- constituent des faits opposables

---

## 7. Diagnostics figés

Les diagnostics incluent :

- durée réelle
- température maximale
- résumés textuels
- sauvegardes JSON

Ils sont :

- figés post-cycle
- immuables
- utilisés pour analyse uniquement

Aucune donnée dynamique
ne peut servir de vérité finale.

---

## 8. Anti-patterns

Sont interdits :

- écriture manuelle de mémoire
- recalcul rétroactif
- diagnostic temps réel
- historisation implicite

Toute violation est critique.

---