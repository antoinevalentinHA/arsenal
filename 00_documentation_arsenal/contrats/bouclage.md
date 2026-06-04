# 🧠 ARSENAL — CONTRAT NORMATIF · ECS — BOUCLAGE

**Version :** 2.3.0  
**Statut :** Actif  
**Rupture :** Abandon des plages horaires au profit d'un maintien conditionnel opportuniste (AUTO) + cycle manuel borné par timer (5 min)  
**Migration :** `binary_sensor.bouclage_autorise` conservé — migrations sémantiques contrôlées :
- v1 → v2 : plage horaire + présence → disponibilité thermique + présence unifiée
- v2 → v3 : composante présence migrée de `presence_famille_unifiee` (périmètre confort, inclut l'approche/quartier) vers `presence_famille_securite OR input_boolean.presence_visiteur` (occupation maison stricte, foyer ou visiteur), et contractualisation de l'interrupteur utilisateur du sous-système AUTO (`input_boolean.bouclage_auto_active`).

---

## 🎯 OBJET DU CONTRAT

Ce contrat définit le **cadre normatif global** de conception,
d'implémentation et d'interprétation du **sous-système Bouclage ECS** dans Arsenal.

Il établit :

- la **sémantique officielle** du bouclage ECS,
- la **distinction stricte** entre qualification thermique, autorisation, état effectif, action et orchestration,
- la **machine d'état normative**,
- l'**arbitrage AUTO / cycle manuel**,
- les **invariants énergétiques**,
- les **règles inter-domaines** (ECS / UI).

Ce contrat constitue une **référence structurante** destinée à figer
définitivement la gouvernance du bouclage ECS.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- l'**interrupteur utilisateur du sous-système AUTO** (kill-switch),
- le **bouclage automatique opportuniste** (modèle thermique + présence),
- le **cycle manuel de bouclage** (déclenchement explicite borné à 5 minutes),
- l'**arbitrage AUTO / cycle manuel**,
- l'orchestration post-cycle ECS,
- l'interaction avec les domaines :
  - UI directe.

Il ne couvre pas :

- le pilotage thermique ECS,
- la production d'eau chaude,
- les consignes ou offsets,
- l'optimisation énergétique future.

---

## 🧠 PRINCIPE FONDAMENTAL

Dans Arsenal :

> **Le bouclage ECS est un actionneur de confort opportuniste,
> actif uniquement lorsque l'utilisateur a activé le sous-système AUTO,
> que de l'eau chaude est réellement disponible
> et qu'un usage est probable.**

Il est :

- toujours **conditionné à l'activation utilisateur du sous-système AUTO**,
- toujours **conditionné à la disponibilité thermique réelle**,
- toujours **conditionné à une occupation maison stricte** (foyer ou visiteur),
- jamais basé sur une plage horaire,
- jamais auto-prolongé artificiellement,
- jamais soumis à une heuristique comportementale ou prédictive,
- jamais auto-corrigé inter-domaines.

En mode AUTO, l'actionneur est **maintenu actif tant que les conditions d'autorisation sont réunies**.
Il ne s'agit pas d'une impulsion déclenchée par un front — c'est un maintien conditionnel continu.
Ce maintien est passif : il résulte uniquement de la persistance des conditions d'autorisation, sans logique de maintien actif.

La thermique du ballon constitue la **borne naturelle** du bouclage :
lorsque le ballon se refroidit sous le seuil d'extinction, le bouclage s'arrête de lui-même.
Aucun timer n'est nécessaire en mode AUTO.

La température du ballon est interprétée comme un **signal de disponibilité d'usage ECS**,
et non comme un indicateur de stock thermique exploitable.

---

Occupation maison stricte :

La maison est considérée occupée si et seulement si :

- binary_sensor.presence_famille_securite == on
  (présence foyer au périmètre maison strict)

OU

- input_boolean.presence_visiteur == on
  (occupation explicite via mode Visite)

Aucune autre source ne peut qualifier une occupation maison stricte.

---

## 🧩 OBJETS STRUCTURANTS OFFICIELS

### 🔹 Interrupteur utilisateur du sous-système AUTO

- `input_boolean.bouclage_auto_active`

Rôle :
- Permettre à l'utilisateur d'**activer ou désactiver l'intégralité du sous-système AUTO** sans toucher aux autres conditions ni au cycle manuel.

Sémantique :
- `on` : le sous-système AUTO est armé. Le maintien conditionnel s'applique selon les autres composantes (thermique + occupation).
- `off` : le sous-système AUTO est désarmé. `binary_sensor.bouclage_autorise` est forcé à `off`, indépendamment de la thermique et de l'occupation.

Statut :
- **AUTORITÉ UTILISATEUR DU SOUS-SYSTÈME AUTO**
- composante de premier niveau de `binary_sensor.bouclage_autorise`
- ne pilote pas directement l'actionneur
- ne gouverne pas le cycle manuel — voir § Arbitrage AUTO / cycle manuel

Portée :
- **gouverne uniquement le mode AUTO**,
- **ne gouverne pas le cycle manuel** : un cycle manuel reste déclenchable et fonctionnel même lorsque `bouclage_auto_active == off`,
- **ne corrige jamais l'état physique** de `switch.prise_bouclage` directement : la transition à `off` agit via `bouclage_autorise` et l'automation 10260000000002 (front descendant), conformément à la doctrine de séparation autorité logique / actionneur.

---

### 🔹 Capteur de disponibilité thermique

- `binary_sensor.ecs_disponible`

Rôle :
- Indiquer si le ballon est dans une plage thermique exploitable pour le bouclage.

Règles :

| Condition | État |
|---|---|
| `sensor.ecs_temperature_ballon_securisee` >= 45 °C | `on` |
| `sensor.ecs_temperature_ballon_securisee` <= 40 °C | `off` |

Hystérésis : 5 °C (seuil_on = 45 °C, seuil_off = 40 °C)

Statut :
- **CAPTEUR DE QUALIFICATION THERMIQUE**
- non décisionnel
- non actionneur

---

### 🔹 Capteur d'autorisation de bouclage AUTO

- `binary_sensor.bouclage_autorise`

> ⚠️ Migrations sémantiques successives :
> - v1 → v2 : sémantique temporelle (plage horaire + présence) remplacée par disponibilité thermique + présence.
> - v2 → v3 : composante présence migrée de `presence_famille_unifiee` (présence Confort, périmètre trop large incluant l'approche/quartier) vers une union stricte foyer + visiteur ; contractualisation de l'interrupteur utilisateur `bouclage_auto_active` comme composante de premier niveau (rattrapage d'un objet existant non documenté).
>
> Le nom de l'entité est conservé pour éviter toute rupture UI ou référence externe.

Définition normative v3 :

```
bouclage_autorise =
  input_boolean.bouclage_auto_active == on
  AND
  binary_sensor.ecs_disponible == on
  AND
  (
    binary_sensor.presence_famille_securite == on
    OR
    input_boolean.presence_visiteur == on
  )
```

Rôle :
- Autoriser le bouclage automatique lorsque l'utilisateur a armé le sous-système AUTO, que l'eau est exploitable **et** qu'un usage est probable au sens d'une occupation maison stricte (foyer présent au périmètre Sécurité, ou visiteur planifié actif).

Justification des composantes :

- `input_boolean.bouclage_auto_active` est l'interrupteur utilisateur du sous-système AUTO. Sa position en première composante (court-circuit logique) garantit que désarmer AUTO suffit à forcer `bouclage_autorise` à `off`, indépendamment de l'état thermique ou de l'occupation.
- `binary_sensor.presence_famille_securite` est la projection canonique stricte du foyer (zone "Maison – Sécurité"), excluant l'approche périmétrique. C'est la seule projection appropriée pour qualifier un usage ECS effectif — un membre du foyer en approche du quartier ne consomme pas d'ECS.
- `input_boolean.presence_visiteur` est la vérité d'occupation explicite portée par le domaine Visite (cf. contrat Visite, I8). Sa lecture par ECS couvre les cas d'occupation hors-foyer (femme de ménage, hôte planifié) qui consomment l'ECS sans qu'aucun `person.*` du foyer ne soit présent.
- L'union `OR` entre les deux présences est sémantiquement correcte : la maison est occupée dès lors que l'une **ou** l'autre des deux populations y est présente.

Statut :
- **AUTORITÉ LOGIQUE DU SOUS-SYSTÈME AUTO**
- ne pilote pas directement l'actionneur
- ne constitue pas un état actif — c'est une condition d'autorisation

---

### 🔹 Actionneur physique partagé

- `switch.prise_bouclage`

Rôle :
- Actionneur unique de la pompe de recirculation ECS.

Statut :
- **ACTIONNEUR PARTAGÉ MULTI-DOMAINES**

Règles :

- ne constitue jamais une source de vérité,
- peut être piloté par plusieurs domaines,
- n'est jamais corrigé automatiquement par ECS,
- peut diverger volontairement de l'état logique.

---

### 🔹 Timer de cycle manuel

- `timer.bouclage_ecs_5_minutes`

Rôle :
- Borner strictement la durée d'un cycle manuel à 5 minutes.

Propriétés :
- durée fixe : 5 minutes,
- restore: true,
- reboot-safe.

Invariant :

> Aucun cycle manuel ne peut dépasser 5 minutes.

Statut :
- **BORNE OBLIGATOIRE DU CYCLE MANUEL**
- absent du mode AUTO — interdit en mode AUTO

---

### 🔹 Flag d'état cycle manuel

- `input_boolean.bouclage_ecs_5_minutes_en_cours`

Rôle :
- Représenter l'état logique d'un cycle manuel actif (durée bornée par timer).

Statut :
- observabilité pure,
- anti-rebond,
- inter-automations.

Interdits :
- ne pilote rien,
- ne décide rien,
- ne corrige rien.

Invariant de non-survie :

> `input_boolean.bouclage_ecs_5_minutes_en_cours` ne peut jamais survivre à un timer idle.

Garanties obligatoires d'implémentation :

- `timer.bouclage_ecs_5_minutes` → `finished` : flag → `off` **inconditionnel**,
- `homeassistant.start` + timer idle + flag `on` → flag → `off` (**purge d'état logique incohérent — ne touche pas `switch.prise_bouclage`**),
- [optionnel] watchdog : timer idle + flag `on` depuis > 10 min → flag → `off`.

Conséquence normative :

> Un flag `on` avec timer idle est un état interdit. Il constitue un défaut d'implémentation, non un état légitime.

---

## 🔗 ÉCRIVAINS OFFICIELS DE L'ACTIONNEUR

### Domaine ECS (légitimes)

- `automation 10260000000001` — Bouclage AUTO : démarrage → ON  
  Déclencheur : front montant de `binary_sensor.bouclage_autorise`  
  **Règle : ne teste jamais `input_boolean.bouclage_ecs_5_minutes_en_cours`. Le cycle manuel ne constitue pas un verrou d'entrée AUTO.**

- `automation 10260000000002` — Bouclage AUTO : extinction → OFF
  Déclencheur : front descendant de `binary_sensor.bouclage_autorise`

- `script.bouclage_ecs_5_minutes` → ON + flag
  **Règle : indépendant de `input_boolean.bouclage_auto_active`. Un cycle manuel reste déclenchable même lorsque le sous-système AUTO est désarmé.**

- `automation 10260000000003` — Extinction bouclage manuel → flag OFF inconditionnel + switch OFF si `bouclage_autorise == off`  
  Déclencheur : fin de `timer.bouclage_ecs_5_minutes`

---

### UI directe

- Toggle brut dans `prises.yaml`

Statut :
- **COMMANDE UTILISATEUR NON GOUVERNÉE**

Règle :
- ECS ne corrige jamais une action UI directe.

---

## 🔒 RÈGLE INTER-DOMAINES

Principe normatif :

- UI est souveraine sur l'actionneur,
- ECS **ne corrige jamais** un état imposé par UI.

Conséquences :

- aucune lutte d'autorité,
- aucune oscillation corrective,
- aucune reprise de main automatique.

---

### Lecture passive du domaine Visite

ECS consomme `input_boolean.presence_visiteur` **en lecture seule** comme contribution à `binary_sensor.bouclage_autorise`.

Cette lecture :

- ne constitue pas une dépendance de pilotage — Visite n'écrit ni ne déclenche rien dans ECS,
- est cohérente avec le contrat Visite (I8) qui autorise explicitement l'exposition passive de `presence_visiteur` comme vérité d'occupation opposable consommable par d'autres domaines,
- ne crée aucune coupling d'écriture : la maintenance des deux contrats reste indépendante.

ECS ne doit jamais être utilisé pour inférer, corriger ou rétroagir sur l'état du domaine Visite.

---

## 🔄 MACHINE D'ÉTAT OFFICIELLE

États reconnus :

- **IDLE**
  Aucun bouclage actif. Sous-système AUTO désarmé, ballon froid, ou maison non occupée.

- **BOUCLAGE_AUTO**
  `binary_sensor.bouclage_autorise == on` (sous-système armé, ballon disponible, maison occupée).

- **CYCLE_MANUEL_5_MIN**
  Cycle explicitement déclenché et automatiquement borné à 5 minutes. Flag manuel actif. Ne constitue pas un état de maintien. Indépendant de `bouclage_auto_active`.

- **SUPERPOSITION**
  Cycle manuel déclenché pendant BOUCLAGE_AUTO.

---

### Transitions autorisées

| # | De | Vers | Condition |
|---|---|---|---|
| 1 | IDLE | BOUCLAGE_AUTO | `bouclage_autorise` devient `on` |
| 2 | IDLE | CYCLE_MANUEL_5_MIN | déclenchement `script.bouclage_ecs_5_minutes` |
| 3 | BOUCLAGE_AUTO | IDLE | `bouclage_autorise` devient `off` (cause indifférente : désarmement AUTO, refroidissement ballon, ou départ occupation) |
| 4 | CYCLE_MANUEL_5_MIN | IDLE | fin timer ET `bouclage_autorise == off` |
| 5 | CYCLE_MANUEL_5_MIN | SUPERPOSITION | `bouclage_autorise` devient `on` pendant cycle |
| 6 | SUPERPOSITION | BOUCLAGE_AUTO | fin timer (AUTO continue) |
| 7 | BOUCLAGE_AUTO | SUPERPOSITION | déclenchement `script.bouclage_ecs_5_minutes` pendant AUTO |

Note sur la transition 3 :

> Le désarmement du sous-système AUTO (`bouclage_auto_active : on → off`) provoque un front descendant de `bouclage_autorise`. L'automation 10260000000002 réagit à ce front et coupe `switch.prise_bouclage`. Comportement attendu et symétrique : armer AUTO autorise le maintien, le désarmer le retire.

---

## 🔒 ARBITRAGE AUTO / CYCLE MANUEL

Règle fondamentale :

> **Le cycle manuel est une impulsion indépendante, bornée par timer. Il ne constitue pas un mode.**

Implémentation normative :

- Le cycle manuel :
  - est une impulsion de 5 minutes,
  - ne constitue pas un état de maintien,
  - ne prolonge jamais AUTO,
  - ne bloque jamais AUTO,
  - ne peut jamais interrompre AUTO,
  - **est indépendant de `input_boolean.bouclage_auto_active`** : il reste déclenchable et fonctionnel même lorsque le sous-système AUTO est désarmé.

- Fin de timer pendant SUPERPOSITION :
  - éteint le flag manuel,
  - laisse l'actionneur sous gouverne AUTO.

Justification de l'indépendance du cycle manuel :

> `bouclage_auto_active` gouverne le **mode AUTO** uniquement. Le cycle manuel est une commande utilisateur ponctuelle, déjà bornée par timer 5 min, sans risque énergétique. La soumettre au kill-switch reviendrait à désactiver l'ensemble du sous-système Bouclage, ce qui n'est pas l'intention de l'interrupteur.

---

## 🧠 ORCHESTRATION CLIENT

### Script client officiel

- `script.lancer_vaisselle_et_bouclage`

Statut :
- **ORCHESTRATEUR SÉQUENTIEL**

Rôle :
- lancer cycle ECS vaisselle,
- attendre fin moteur,
- déclencher un bouclage manuel standard.

Interdits :
- ne pilote aucun actionneur,
- ne modifie aucun état,
- ne décide aucune autorisation.

---

## 🔒 INVARIANTS STRUCTURANTS

- aucun bouclage AUTO si `bouclage_auto_active == off`,
- aucun bouclage AUTO si `ecs_disponible == off`,
- aucun bouclage AUTO si l'occupation maison stricte est `off`, c'est-à-dire si `presence_famille_securite == off` ET `input_boolean.presence_visiteur == off`,
- bouclage AUTO autorisé uniquement si l'occupation maison stricte est `on`, c'est-à-dire si `presence_famille_securite == on` OU `input_boolean.presence_visiteur == on`,
- `bouclage_auto_active == off` force `bouclage_autorise == off` indépendamment des autres composantes (court-circuit logique),
- le cycle manuel reste fonctionnel indépendamment de `bouclage_auto_active`,
- aucune prolongation artificielle du bouclage,
- aucune logique basée sur l'heure ou le jour,
- aucune heuristique comportementale ou prédictive,
- aucun helper ne pilote un actionneur,
- aucun script ne décide,
- aucun moteur ECS ne corrige un domaine externe,
- `input_boolean.bouclage_ecs_5_minutes_en_cours` ne peut jamais survivre à un timer idle,
- l'automation AUTO de démarrage ne teste jamais le flag de cycle manuel.

`binary_sensor.bouclage_autorise` ne pilote jamais directement l'actionneur.
Les écrivains habilités sur `switch.prise_bouclage` sont exclusivement :
- les automations du domaine bouclage (`11_automations/bouclage/`),
- `script.bouclage_ecs_5_minutes` (point d'entrée unique du cycle manuel).
Aucun autre script, helper ou binary_sensor ne peut écrire sur `switch.prise_bouclage`.

Le bouclage ECS ne doit jamais être utilisé pour influencer ou maintenir la température du ballon.
Toute interaction thermique est considérée comme un effet secondaire non exploité.

La température du ballon constitue la **borne naturelle et suffisante** du bouclage AUTO.
Aucun timer n'est requis ni autorisé en mode AUTO.

---

## 🚫 INTERDITS FORMELS

Sont strictement interdits :

- toute plage horaire comme condition de bouclage AUTO,
- tout timer comme borne du mode AUTO,
- utiliser l'état matériel `switch.prise_bouclage` comme vérité logique,
- corriger un état imposé par UI,
- créer une logique de prolongation automatique,
- utiliser le reboot pour corriger arbitrairement l'état physique de `switch.prise_bouclage`,
- tester `input_boolean.bouclage_ecs_5_minutes_en_cours` dans l'automation de démarrage AUTO,
- laisser subsister un flag `on` après expiration ou idle du timer,
- réintroduire `binary_sensor.presence_famille_unifiee` comme composante de `bouclage_autorise` — sa sémantique de périmètre Confort (incluant l'approche) est inappropriée pour qualifier un usage ECS,
- soumettre le cycle manuel à `input_boolean.bouclage_auto_active` — l'interrupteur ne gouverne que le mode AUTO,
- utiliser `input_boolean.bouclage_auto_active` pour piloter directement `switch.prise_bouclage` — sa propagation passe exclusivement par `bouclage_autorise` et l'automation 10260000000002,
- piloter `switch.prise_bouclage` depuis tout script autre que `script.bouclage_ecs_5_minutes`.

---

## ❌ SUPPRESSIONS STRUCTURELLES

### Rupture v1 → v2 (rappel)

Sont supprimés :

- `input_boolean.bouclage_plage_active` — clé d'activation plage horaire, devenue sans objet
- toute automation de bouclage AUTO basée sur plage horaire

### Rupture v2 → v3

Est retirée de la composition de `bouclage_autorise` :

- `binary_sensor.presence_famille_unifiee` — périmètre Confort (incluant l'approche/quartier) inadapté à la qualification d'usage ECS. L'entité reste valide pour ses domaines consommateurs légitimes (chauffage, climatisation), mais n'est plus consommée par ECS.

Est ajouté à la composition de `bouclage_autorise` :

- `input_boolean.bouclage_auto_active` — entité préexistante, non contractualisée jusqu'ici. Reconnue comme objet structurant officiel et placée en première composante (court-circuit logique).

### Conservés intacts

- `timer.bouclage_ecs_5_minutes` — borne obligatoire du cycle manuel
- `switch.prise_bouclage` — actionneur physique
- `input_boolean.bouclage_ecs_5_minutes_en_cours` — flag d'état cycle manuel

### Migrations sémantiques (nom conservé, logique remplacée)

- `binary_sensor.bouclage_autorise` :
  - v1 (plage horaire + présence) → v2 (disponibilité thermique + présence unifiée) → v3 (kill-switch utilisateur + disponibilité thermique + occupation maison stricte foyer ∪ visiteur)

---

## 📌 OBSERVABILITÉ & DIAGNOSTIC

Sources officielles :

| Entité | Rôle |
|---|---|
| `input_boolean.bouclage_auto_active` | Interrupteur utilisateur du sous-système AUTO |
| `sensor.ecs_temperature_ballon_securisee` | Température ballon (source physique) |
| `binary_sensor.ecs_disponible` | Qualification thermique |
| `binary_sensor.presence_famille_securite` | Présence foyer — projection stricte (zone Maison – Sécurité) |
| `input_boolean.presence_visiteur` | Occupation visiteur planifié (consommé en lecture, contrat Visite) |
| `binary_sensor.bouclage_autorise` | Autorisation AUTO effective |
| `timer.bouclage_ecs_5_minutes` | Borne temporelle du cycle manuel |
| `input_boolean.bouclage_ecs_5_minutes_en_cours` | État cycle manuel actif |
| `switch.prise_bouclage` | État physique actionneur |

Toute divergence entre état logique et état physique est :

- volontaire,
- inter-domaine,
- non corrigée.

---

## 📋 CHANGELOG

### v2.3.0
- **§ En-tête** : bump version, ligne `Migration` étendue avec la rupture v2 → v3 (présence + contractualisation du kill-switch).
- **§ Périmètre couvert** : ajout de l'interrupteur utilisateur du sous-système AUTO comme objet de premier niveau.
- **§ Principe fondamental** : la doctrine est triplement conditionnée — activation utilisateur AUTO + disponibilité thermique + occupation maison stricte (foyer ou visiteur).
- **§ Objets structurants officiels** : ajout de `input_boolean.bouclage_auto_active` comme objet structurant officiel de premier niveau (rattrapage d'un objet préexistant non documenté). Sémantique, statut et portée explicités. Indépendance vis-à-vis du cycle manuel formalisée.
- **§ Capteur d'autorisation de bouclage AUTO** : redéfinition normative de `binary_sensor.bouclage_autorise`. Ajout de `bouclage_auto_active` comme première composante (court-circuit logique). Composante présence migrée de `binary_sensor.presence_famille_unifiee` vers `binary_sensor.presence_famille_securite OR input_boolean.presence_visiteur`. Bloc de justification étendu aux trois composantes.
- **§ Écrivains officiels** : ajout d'une note explicite sur l'indépendance de `script.bouclage_ecs_manuel` vis-à-vis de `bouclage_auto_active`.
- **§ Règle inter-domaines** : ajout d'une sous-section *Lecture passive du domaine Visite*, formalisant que ECS consomme `presence_visiteur` en lecture seule, sans coupling d'écriture, en cohérence avec l'amendement I8 du contrat Visite (v1.1.0).
- **§ Machine d'état** : libellé IDLE étendu (sous-système AUTO désarmé inclus). État CYCLE_MANUEL_5_MIN explicité comme indépendant de `bouclage_auto_active`. Note ajoutée sur la transition 3 décrivant le désarmement AUTO comme cause légitime du retour à IDLE.
- **§ Arbitrage AUTO / cycle manuel** : ajout explicite de l'indépendance du cycle manuel vis-à-vis du kill-switch, avec justification.
- **§ Invariants structurants** : ajout de trois invariants — court-circuit logique du kill-switch, désarmement AUTO comme cause d'extinction, indépendance du cycle manuel. Invariant de présence reformulé pour refléter la nouvelle composition (ET sur les deux négations).
- **§ Interdits formels** : ajout de trois interdits — réintroduction de `presence_famille_unifiee` dans `bouclage_autorise`, soumission du cycle manuel au kill-switch, pilotage direct de `switch.prise_bouclage` par le kill-switch.
- **§ Suppressions structurelles** : section restructurée. `presence_famille_unifiee` retirée de la composition de `bouclage_autorise` (l'entité reste valide pour ses autres consommateurs). `input_boolean.bouclage_auto_active` ajouté comme nouvelle composante contractualisée.
- **§ Observabilité & Diagnostic** : table mise à jour — `bouclage_auto_active` ajouté en tête, `presence_famille_unifiee` retiré, `presence_famille_securite` et `presence_visiteur` ajoutés.
- **Motivation principale (présence)** : la présence Confort (`presence_famille_unifiee`) inclut la projection « Approche – Sécurité » (quartier proche), inadaptée à la qualification d'un usage ECS. Par ailleurs, elle ignore le mode Visiteur, ce qui empêchait le bouclage AUTO lorsqu'une femme de ménage ou un hôte planifié occupait seul la maison. La composition retenue (`presence_famille_securite OR presence_visiteur`) corrige les deux défauts simultanément, sans création d'entité intermédiaire.
- **Motivation secondaire (kill-switch)** : `input_boolean.bouclage_auto_active` existait déjà dans l'implémentation comme interrupteur utilisateur du sous-système AUTO, mais n'était documenté dans aucun contrat. Ce rattrapage normatif clôt la dette : l'entité est désormais reconnue comme objet structurant officiel, sa sémantique et sa portée sont fixées, et son indépendance vis-à-vis du cycle manuel est explicite.

### v2.2.1
- **§ Périmètre / Objet** : retrait de la référence Alarme / Visite.
- **§ Écrivains officiels** : suppression du bloc domaine ALARME / VISITE (`activation.yaml`, `securite_reboot.yaml`, `desactivation.yaml`) — domaine désormais hors périmètre.
- **§ Règle inter-domaines** : retrait de la souveraineté ALARME ; seule UI reste domaine externe reconnu.
- **§ Interdits formels** : remplacement de *"correction automatique post-reboot"* et *"corriger un état imposé par ALARME ou UI"* par formulations précises — le reset du flag au boot est **légitime** (purge d'état logique, sans toucher l'actionneur) ; seule la correction arbitraire de `switch.prise_bouclage` au reboot est interdite.
- **§ Flag — garanties** : clarification explicite que la purge reboot-safe ne concerne que le flag, jamais l'actionneur.

### v2.2.0
- **§ Flag d'état cycle manuel** : ajout invariant de non-survie + garanties obligatoires d'implémentation (timer.finished → flag off inconditionnel, reboot-safe reset, watchdog optionnel).
- **§ Écrivains officiels** : `automation 10260000000001` — ajout de la règle explicite interdisant tout test du flag dans AUTO démarrage.
- **§ Écrivains officiels** : `automation 10260000000003` — clarification : flag off **inconditionnel** à l'expiration, switch off conditionnel à `bouclage_autorise`.
- **§ Invariants structurants** : ajout des deux invariants manquants (non-survie du flag, absence de garde AUTO sur flag manuel).
- **§ Interdits formels** : ajout de deux interdits explicites (garde flag dans AUTO, flag orphelin post-timer).
- **Motivation** : bug production — flag `bouclage_ecs_5_minutes_en_cours` resté `on` après expiration timer → paralysie du mode AUTO.

### v2.1.2
- Version précédente (actif).

# ==========================================================
