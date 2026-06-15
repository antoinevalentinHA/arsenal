# 🔁🔔 Contrat Arsenal — Panne secteur (Cycle de vie & signalisation)

**Version :** 1.1
**Compatible :** Arsenal v6+
**Statut :** Contrat actif

**Historique :**
- v1.0 : création — cycle de vie, idempotence, signalisation persistante, persistance inter-redémarrage
- v1.1 : réalignement runtime — confort conditionné (veto), ECS de secours `desinfection` bornée SOC, réconciliation de sortie, signal canonique `binary_sensor.panne_secteur_en_cours` pour l'inhibition des remédiations

---

## 🔗 Dépendance normative

Ce contrat est un contrat **dérivé**. Il dépend du contrat socle :

[10_socle.md](10_socle.md)

Les notions de **"coupure secteur confirmée"** et de **"panne secteur qualifiée"** sont définies exclusivement par ce contrat socle.

Les effets métier chauffage et ECS déclenchés à l'entrée en mode panne sont régis par :

[20_chauffage_et_ecs.md](20_chauffage_et_ecs.md)

Le présent contrat ne redéfinit pas ces effets. Il les référence comme actions autorisées dans le cycle de vie.

---

## 🎯 Objet

Ce contrat définit :

- les conditions d'entrée en mode panne
- les règles de cycle de vie
- la signalisation utilisateur associée

---

## 🔁 Entrée en mode panne

### Déclencheurs autorisés

- coupure secteur confirmée (transition `off → on` du signal canonique)
- redémarrage Home Assistant alors que `binary_sensor.coupure_secteur == on` et que l'état de panne persistant est actif

> ⚠️ Le second déclencheur repose sur la **persistance explicite de l'état système** entre redémarrages. L'implémentation doit garantir cette persistance via un mécanisme indépendant du cycle de vie du processus Home Assistant. Sans ce mécanisme, ce déclencheur n'est pas garanti.

---

### 🧭 Nature de l'état

L'entrée en mode panne constitue un **état système persistant**.

Cet état :

- est dérivé de la panne secteur qualifiée
- doit survivre à un redémarrage Home Assistant
- ne constitue pas un événement ponctuel

---

### Actions autorisées

- activation **conditionnelle** de `input_boolean.mode_confort_chauffage` (**veto confort** : besoin thermique réel + présence + budget SOC Bluetti ; sinon neutralisé)
- déclenchement du mécanisme ECS de secours canonique (cycle `desinfection`, **borné par le budget SOC Bluetti**)
- notification persistante (état système)
- notification mobile (optionnelle, événementielle)

Les deux premières actions sont régies par le contrat de résilience thermique [`20_chauffage_et_ecs.md`](20_chauffage_et_ecs.md). En cas de conflit d'interprétation, ce contrat est subordonné au contrat thermique sur ces points.

---

### 🔒 Invariant — Idempotence

L'entrée en mode panne est **strictement idempotente** :

- toute réévaluation de la condition panne doit être **sans effet supplémentaire** si l'état est déjà actif
- aucun cycle ECS ne doit être relancé
- aucune notification ne doit être dupliquée
- aucune action ne doit être rejouée lors d'un redémarrage Home Assistant

---

## 🔔 Signalisation utilisateur — État panne

### Principe canonique

Une panne secteur active est matérialisée par une **notification persistante d'état système**.

---

### Propriétés

Cette notification :

- est créée **uniquement** lors de l'entrée en mode panne
- représente exclusivement l'état : *Panne secteur en cours — mode secours actif*
- est visible **tant que la panne est active**
- est supprimée **explicitement** lors de la sortie de panne

---

### 🔒 Invariant — Unicité

Une seule notification persistante est autorisée pour représenter l'état de panne secteur.

Son identifiant est **stable, unique et normatif** :

```
mode_panne_secteur
```

Toute implémentation doit utiliser cet identifiant. L'utilisation d'un identifiant instable ou généré dynamiquement est interdite.

---

### Invariants

La notification persistante est :

- un **état courant**
- non un événement
- non une trace
- non un journal

Il est strictement interdit de :

- créer une notification de "retour à la normale"
- laisser persister une notification après la panne
- utiliser un identifiant autre que `mode_panne_secteur`

---

### Gouvernance

- **Création** :
  - automation d'entrée en mode panne
  - via un script dédié

- **Suppression** :
  - automation de sortie de panne
  - via `persistent_notification.dismiss`
  - avec `notification_id: mode_panne_secteur`

---

### Principe Arsenal

> On persiste **l'état critique en cours**.
> On ne persiste **jamais** sa résolution.

---

## 🔁 Sortie de panne & réconciliation

La sortie de panne (retour secteur confirmé) :

- clôt l'épisode (`input_boolean.panne_secteur_active → off`)
- lève le signal confort (`input_boolean.mode_confort_chauffage → off`)
- réinitialise l'ECS à sa valeur de sécurité (cf. [`20_chauffage_et_ecs.md`](20_chauffage_et_ecs.md), sortie ECS)
- supprime la notification persistante

Un **mécanisme de réconciliation** garantit qu'un épisode resté actif alors que le secteur est revenu (par exemple transition manquée pendant un redémarrage HA) est clôturé : à la stabilisation système, si `binary_sensor.coupure_secteur == off` et que l'épisode est encore actif, la sortie est rejouée.

---

## 🛡️ Signal canonique d'inhibition des remédiations

L'état de panne (en cours **ou** encore latché) est exposé par un **signal canonique unique** :

```
binary_sensor.panne_secteur_en_cours
```

- `state` : `on` si coupure live (`coupure_secteur == on`) **ou** épisode latché (`panne_secteur_active == on`)
- `availability` : indéterminé (détection `unavailable`/`unknown` **et** pas d'épisode latché) → le capteur devient lui-même `unavailable`, ce qui inhibe **par prudence** côté consommateurs

**Doctrine.** Pendant une panne secteur, les indisponibilités des périphériques **non secourus** (intégrations cloud, stations météo, climatisation, accès externe) sont des **KO attendus**, pas des dysfonctionnements. Les remédiations automatiques (reloads d'intégration, reboot box, watchdog climatisation, reboot des stations Netatmo) sont donc **inhibées** tant que `binary_sensor.panne_secteur_en_cours != off`, et reprennent naturellement au retour du secteur. Tout nouveau système de remédiation référence ce signal unique plutôt que de dupliquer les conditions d'état.

---

## 🚫 Comportements strictement interdits

- Rejouer une action déjà exécutée dans l'épisode en cours
- Déclencher un second cycle ECS sur redémarrage HA
- Créer plus d'une notification persistante pour l'état de panne
- Utiliser un `notification_id` instable ou dynamique
- Laisser persister la notification après retour à la normale
- Émettre une notification de "retour à la normale"
- Traiter la panne comme un événement ponctuel

---

## 🔗 Traçabilité des garanties

| Garantie | Fondement contractuel |
|---|---|
| Stabilité au redémarrage HA | Persistance explicite requise — déclencheur redémarrage |
| Idempotence complète | Invariant idempotence — entrée en mode panne |
| Unicité de la notification | Invariant unicité + `notification_id` normatif |
| Absence de notification résiduelle | Interdiction explicite + suppression à la sortie |
| Cohérence avec le socle | Dépendance normative déclarée |
| Non-redéfinition des effets métier | Subordination au contrat thermique déclarée |
| Clôture d'un épisode resté actif | Mécanisme de réconciliation à la stabilisation système |
| Inhibition des remédiations en panne | Signal canonique `binary_sensor.panne_secteur_en_cours` |
