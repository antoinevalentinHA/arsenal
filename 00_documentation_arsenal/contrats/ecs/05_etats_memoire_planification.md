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
- réinitialisation (`→ off`) : exclusivement après consommation, dans
  l'automation « ECS - Désinfection fin vacances »
  (`11_automations/ecs/desinfection_retour_vacances.yaml`).
- interdictions : `timer.cancel` (retour anticipé) ne pose jamais cet état ;
  aucune écriture manuelle ; aucun autre écrivain.

Idempotence : la consommation exécute la désinfection au plus une fois puis
repositionne l'état à `off`. Un état `on` présent au démarrage est consommé une
seule fois (pas de double exécution).

Projection d'observabilité : `binary_sensor.ecs_desinfection_retour_vacances_autorisee`
est conservé comme projection 1:1 de `input_boolean.ecs_desinfection_retour_due`.
Il n'a plus de rôle décisionnel et ne lit plus `timer.vacances_longues_ecs` ni
son attribut `remaining`.

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