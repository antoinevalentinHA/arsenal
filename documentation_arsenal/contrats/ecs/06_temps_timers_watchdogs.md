# 🧠 ARSENAL — ECS  
# Temps, timers et watchdogs

Chemin : `/homeassistant/documentation_arsenal/ecs/06_temps_timers_watchdogs.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Gestion du temps ECS

---

## 1. Objet

Ce document encadre l’utilisation du temps,
des timers et des watchdogs dans l’ECS.

Il empêche toute dérive temporelle
et tout cycle non borné.

---

## 2. Doctrine temporelle

Le temps dans l’ECS est :

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
- garantit l’auto-arrêt post-reboot
- neutralise toute dérive manuelle

---

### 5.2 Garanties

- pas de dépassement possible
- pas de contournement
- pas de désactivation implicite

---

## 6. Hiérarchie temporelle

En cas de conflit :

 Watchdog > Timer bouclage > Timer stabilisation

La hiérarchie est absolue.

---

## 7. Anti-patterns

Sont interdits :

- temporisation infinie
- polling temporel
- dépendance directe à now()
- délais arbitraires
- horodatage implicite

Toute dérive est critique.

---