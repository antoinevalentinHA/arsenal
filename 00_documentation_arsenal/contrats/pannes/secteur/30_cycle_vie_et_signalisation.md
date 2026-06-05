# 🔁🔔 Contrat Arsenal — Panne secteur (Cycle de vie & signalisation)

**Version :** 1.0  
**Compatible :** Arsenal v6+  
**Statut :** Contrat actif

**Historique :**
- v1.0 : création — cycle de vie, idempotence, signalisation persistante, persistance inter-redémarrage

---

## 🔗 Dépendance normative

Ce contrat est un contrat **dérivé**. Il dépend du contrat socle :

`/00_documentation_arsenal/contrats/pannes/secteur/10_socle.md`

Les notions de **"coupure secteur confirmée"** et de **"panne secteur qualifiée"** sont définies exclusivement par ce contrat socle.

Les effets métier chauffage et ECS déclenchés à l'entrée en mode panne sont régis par :

`/00_documentation_arsenal/contrats/pannes/secteur/20_chauffage_et_ecs.md`

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

- activation de `input_boolean.mode_confort_chauffage`
- déclenchement du mécanisme ECS de secours canonique
- notification persistante (état système)
- notification mobile (optionnelle, événementielle)

Les deux premières actions sont régies par le contrat de résilience thermique. En cas de conflit d'interprétation, ce contrat est subordonné au contrat thermique sur ces points.

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
