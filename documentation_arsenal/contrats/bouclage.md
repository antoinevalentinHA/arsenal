# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     ECS — BOUCLAGE
# ==========================================================

**Version :** 2.1.2  
**Statut :** Actif  
**Rupture :** Abandon des plages horaires au profit d'un maintien conditionnel opportuniste (AUTO) + cycle manuel borné par timer (5 min)  
**Migration :** `binary_sensor.bouclage_autorise` conservé — migration sémantique contrôlée (v1 : plage horaire + présence → v2 : disponibilité thermique + présence)

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
- les **règles inter-domaines** (ECS / Alarme / UI).

Ce contrat constitue une **référence structurante** destinée à figer
définitivement la gouvernance du bouclage ECS.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- le **bouclage automatique opportuniste** (modèle thermique + présence),
- le **cycle manuel de bouclage** (déclenchement explicite borné à 5 minutes),
- l'**arbitrage AUTO / cycle manuel**,
- l'orchestration post-cycle ECS,
- l'interaction avec les domaines :
  - Alarme / Visite,
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
> actif uniquement lorsque de l'eau chaude est réellement disponible
> et qu'un usage est probable.**

Il est :

- toujours **conditionné à la disponibilité thermique réelle**,
- toujours **conditionné à la présence famille**,
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

## 🧩 OBJETS STRUCTURANTS OFFICIELS

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

> ⚠️ Migration sémantique v1 → v2 : cette entité existait en v1 avec une sémantique temporelle (plage horaire + présence).
> Sa sémantique est remplacée intégralement. Le nom est conservé pour éviter toute rupture UI ou référence externe.

Définition normative v2 :

```
bouclage_autorise =
  binary_sensor.ecs_disponible == on
  AND
  binary_sensor.presence_famille_unifiee == on
```

Rôle :
- Autoriser le bouclage automatique lorsque les deux conditions sont simultanément réunies.

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

---

## 🔗 ÉCRIVAINS OFFICIELS DE L'ACTIONNEUR

### Domaine ECS (légitimes)

- `automation 10260000000001` — Bouclage AUTO : démarrage → ON
  Déclencheur : front montant de `binary_sensor.bouclage_autorise`

- `automation 10260000000002` — Bouclage AUTO : extinction → OFF
  Déclencheur : front descendant de `binary_sensor.bouclage_autorise`

- `script.bouclage_ecs_manuel` → ON + flag
- `automation 10260000000003` — Extinction bouclage manuel → OFF + flag
  Déclencheur : fin de `timer.bouclage_ecs_5_minutes`

---

### Domaine ALARME / VISITE

- `activation.yaml`
- `securite_reboot.yaml`
- `desactivation.yaml`

Statut :
- **DOMAINE EXTERNE SOUVERAIN**

Règle :
- ECS ne corrige jamais une action ALARME.

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

- ALARME est souverain sur l'actionneur,
- UI est souveraine sur l'actionneur,
- ECS **ne corrige jamais** un état imposé par un autre domaine.

Conséquences :

- aucune lutte d'autorité,
- aucune oscillation corrective,
- aucune reprise de main automatique.

---

## 🔄 MACHINE D'ÉTAT OFFICIELLE

États reconnus :

- **IDLE**
  Aucun bouclage actif. Ballon froid ou famille absente.

- **BOUCLAGE_AUTO**
  `binary_sensor.bouclage_autorise == on`.

- **CYCLE_MANUEL_5_MIN**
  Cycle explicitement déclenché et automatiquement borné à 5 minutes. Flag manuel actif. Ne constitue pas un état de maintien.

- **SUPERPOSITION**
  Cycle manuel déclenché pendant BOUCLAGE_AUTO.

---

### Transitions autorisées

| # | De | Vers | Condition |
|---|---|---|---|
| 1 | IDLE | BOUCLAGE_AUTO | `bouclage_autorise` devient `on` |
| 2 | IDLE | CYCLE_MANUEL_5_MIN | déclenchement `script.bouclage_ecs_manuel` |
| 3 | BOUCLAGE_AUTO | IDLE | `bouclage_autorise` devient `off` |
| 4 | CYCLE_MANUEL_5_MIN | IDLE | fin timer ET `bouclage_autorise == off` |
| 5 | CYCLE_MANUEL_5_MIN | SUPERPOSITION | `bouclage_autorise` devient `on` pendant cycle |
| 6 | SUPERPOSITION | BOUCLAGE_AUTO | fin timer (AUTO continue) |
| 7 | BOUCLAGE_AUTO | SUPERPOSITION | déclenchement `script.bouclage_ecs_manuel` pendant AUTO |

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
  - ne peut jamais interrompre AUTO.

- Fin de timer pendant SUPERPOSITION :
  - éteint le flag manuel,
  - laisse l'actionneur sous gouverne AUTO.

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

- aucun bouclage AUTO si `ecs_disponible == off`,
- aucun bouclage AUTO si `presence_famille_unifiee == off`,
- aucune prolongation artificielle du bouclage,
- aucune logique basée sur l'heure ou le jour,
- aucune heuristique comportementale ou prédictive,
- aucun helper ne pilote un actionneur,
- aucun script ne décide,
- aucun moteur ne corrige un domaine externe.

`binary_sensor.bouclage_autorise` ne pilote jamais directement l'actionneur.
Seules les automatisations sont habilitées à écrire dans `switch.prise_bouclage`.

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
- corriger un état imposé par ALARME ou UI,
- créer une logique de prolongation automatique,
- correction automatique post-reboot.

---

## ❌ SUPPRESSIONS STRUCTURELLES (rupture v1 → v2)

Sont supprimés :

- `input_boolean.bouclage_plage_active` — clé d'activation plage horaire, devenue sans objet
- toute automation de bouclage AUTO basée sur plage horaire

Sont migrés sémantiquement (nom conservé, logique remplacée) :

- `binary_sensor.bouclage_autorise` — sémantique v1 (plage horaire + présence) remplacée par sémantique v2 (disponibilité thermique + présence)

Sont conservés intacts :

- `timer.bouclage_ecs_5_minutes` — borne obligatoire du cycle manuel
- `switch.prise_bouclage` — actionneur physique
- `input_boolean.bouclage_ecs_5_minutes_en_cours` — flag d'état cycle manuel

---

## 📌 OBSERVABILITÉ & DIAGNOSTIC

Sources officielles :

| Entité | Rôle |
|---|---|
| `sensor.ecs_temperature_ballon_securisee` | Température ballon (source physique) |
| `binary_sensor.ecs_disponible` | Qualification thermique |
| `binary_sensor.presence_famille_unifiee` | Présence famille |
| `binary_sensor.bouclage_autorise` | Autorisation AUTO effective |
| `timer.bouclage_ecs_5_minutes` | Borne temporelle du cycle manuel |
| `input_boolean.bouclage_ecs_5_minutes_en_cours` | État cycle manuel actif |
| `switch.prise_bouclage` | État physique actionneur |

Toute divergence entre état logique et état physique est :

- volontaire,
- inter-domaine,
- non corrigée.

---

## 🧠 STATUT

- Contrat normatif : **ACTIF**
- Domaine : **ECS / Bouclage**
- Rôle : **STRUCTURANT**
- Évolutivité : **MAÎTRISÉE**

# ==========================================================
