# 🧠 ARSENAL — ECS  
# Temps, timers et watchdogs

Chemin : `/homeassistant/documentation_arsenal/ecs/06_temps_timers_watchdogs.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Gestion du temps ECS

---

## 1. Objet

Ce document encadre l'utilisation du temps,
des timers et des watchdogs dans l'ECS.

Il empêche toute dérive temporelle
et tout cycle non borné.

---

## 2. Doctrine temporelle

Le temps dans l'ECS est :

- encapsulé
- borné
- vérifié
- jamais consommé directement

Aucune automation ne dépend
directement de `now()`.

---

## 3. Timers de stabilisation

### 3.1 Nature

Timers `restore: false`

Usages :

- post-prélèvement
- attente post-action
- suspension temporaire du diagnostic

---

### 3.2 Règles

- aucun diagnostic pendant stabilisation
- aucune décision prématurée
- expiration non critique

---

## 4. Watchdog de cycle

### 4.1 Nature

Timers `restore: true`

Ils définissent :

- une durée maximale absolue
- une limite infranchissable

---

### 4.2 Invariants

- aucun cycle ne survit à son watchdog
- expiration = événement critique
- déclenchement de procédures de sûreté

---

## 5. Timer de bouclage ECS

### 5.1 Rôle

- borne strictement la durée
- garantit l'auto-arrêt post-reboot
- neutralise toute dérive manuelle

---

### 5.2 Garanties

- pas de dépassement possible
- pas de contournement
- pas de désactivation implicite

---

## 6. Timer d'inertie post-cycle ECS

### 6.1 Nature

Timer `restore: true`

`timer.fenetre_inertie_chauffe_ecs`

Durée : 15 minutes

---

### 6.2 Rôle

- représente la fenêtre de stabilisation thermique
  post-cycle ECS
- décale le gel des données diagnostiques
  jusqu'à expiration
- définit l'instant d'émission du signal canonique `ecs_fin_cycle_signal`
- permet la capture de l'inertie thermique réelle
  du ballon après arrêt du brûleur

---

### 6.3 Règles

- armé à la fin du cycle (`ecs_cycle_en_cours: on → off`)
- annulé si un nouveau cycle démarre avant échéance
- le gel final n'intervient qu'à l'échéance
- aucune décision thermique pendant la fenêtre
- aucune émission du signal `ecs_fin_cycle_signal` avant expiration du timer

---

### 6.4 Garanties

- persistant au redémarrage HA (`restore: true`)
- non critique : l'annulation ne compromet pas la sûreté
- subordonné au watchdog de cycle en cas de conflit

---

### 6.5 Rôle événementiel (canonique)

Le timer d'inertie post-cycle ECS ne se limite pas
à une fonction de stabilisation thermique.

Il définit l'instant canonique de fin de cycle exploitable.

À son échéance :

- les données diagnostiques sont considérées comme stabilisées
- le gel final est exécuté (automation 10250000000026)
- le signal canonique `ecs_fin_cycle_signal` est émis

Ce signal représente :

> la fin exploitable d'un cycle ECS

La fin de cycle ECS ne doit jamais être considérée
avant l'expiration de ce timer.

Il constitue l'unique événement canonique
de fin de cycle ECS.

---

### 6.6 Dépendances

Le timer d'inertie est utilisé par :

- automation `10250000000027` — armement / annulation
- automation `10250000000026` — gel final + émission du signal

Il constitue la référence temporelle unique
pour la fin exploitable d'un cycle ECS.

---

## 7. Hiérarchie temporelle

En cas de conflit :

```
Watchdog > Timer bouclage > Timer inertie post-cycle > Timer stabilisation
```

La hiérarchie est absolue.

---

## 8. Anti-patterns

Sont interdits :

- temporisation infinie
- polling temporel
- dépendance directe à `now()`
- délais arbitraires
- horodatage implicite

Toute dérive est critique.
