# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Décision centrale (pure)

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : [`30_decision_centrale.md`](30_decision_centrale.md)

---

## 🎯 Objet

Définir le contrat d’exécution du cerveau :

- `script.alarme_decision_centrale`

---

## 🧠 Rôle

Le cerveau :

- lit des **entrées contractuelles**,
- calcule une décision **déterministe**,
- publie la décision via helpers,
- n’exécute aucune action.

---

## 🔒 Propriétés obligatoires

- **Déterministe** : mêmes entrées → mêmes sorties.
- **Idempotent** : exécutable sans effet de bord.
- **Sans action** :
  - aucun appel à `alarm_control_panel.*`,
  - aucun `timer.*`,
  - aucune notification,
  - aucune sirène.

---

## 📤 Sorties obligatoires

Le cerveau publie :

- `input_text.alarme_decision`
- `input_text.alarme_etat_cible`
- `input_text.alarme_raison`

---

## 🧩 Canon décisionnel (niveau contrat)

La décision doit tenir compte, au minimum, de :

1) contexte visiteur (si présent)
2) présence sécurité
3) mode alarme (automatique vs non)
4) absence stabilisée
5) blocage armement auto
6) délai d’entrée en cours
7) sinon : armement autorisé

---

## 🧭 Source de la présence sécurité (déterminants armement / désarmement)

Le canon décisionnel distingue deux entrées de présence aux exigences de stabilité différentes :

- **Désarmement automatique** (canon §2 « présence sécurité ») : le cerveau lit la **projection confirmée** `binary_sensor.presence_famille_securite_confirmee_alarme` — image stabilisée du signal brut avec `delay_on: 15 s`. Une présence sécurité doit donc être **confirmée pendant au moins 15 s** avant de produire un désarmement automatique. Cette projection filtre les `on` fugitifs (jitter GPS, franchissement de frontière de zone, BSSID Wi-Fi) à proximité du domicile.
- **Armement automatique** (canon §4 « absence stabilisée ») : le cerveau lit la **projection confirmée d'absence** `binary_sensor.presence_famille_securite_absence_confirmee_alarme` — image stabilisée du signal brut avec `delay_on: 5 min`. Une absence sécurité doit donc être **confirmée pendant au moins 5 min** avant de produire un armement automatique. La temporisation est portée par la projection elle-même (atomique) et non plus par un timer démarré dans une automatisation tierce.
- **Mécanisme historique supprimé (phase 2, commit `c4637ee` / #160)** : l'ancien trio `binary_sensor.presence_famille_securite_absent_depuis_5_min` + timer `timer.presence_famille_securite_absence` + automatisation `presence/absence_5_min.yaml` a été **retiré**. Le seul consommateur résiduel (diagnostic `binary_sensor.alarme_systeme_coherent`, `12_template_sensors/alarme/coherence.yaml`) calcule désormais l'absence prolongée **inline** depuis l'âge du signal brut (seuil 480 s), sans réintroduire de timer ni consommer la projection d'armement.

### Invariants de séparation

- Le **signal brut partagé** `binary_sensor.presence_famille_securite` **n'est pas modifié** : il reste la vérité de présence sécurité commune, consommée telle quelle par les autres domaines.
- La projection `presence_famille_securite_confirmee_alarme` est **réservée au désarmement automatique de l'alarme** ; elle ne doit pas être consommée hors de ce périmètre.
- La projection `presence_famille_securite_absence_confirmee_alarme` est **réservée à l'armement automatique de l'alarme** ; elle ne doit pas être consommée hors de ce périmètre.
- Les consommateurs **ECS / bouclage**, volets, éclairage jardin et confort thermique **ne sont pas affectés** : ils continuent de lire le signal brut.

### Invariant d'atomicité

- Tout déterminant temporel de la décision (présence confirmée, absence confirmée) doit être **reconstructible à tout instant à partir d'un seul état persistant** : la temporisation est portée par la projection (`delay_on`), jamais par un timer démarré dans une automatisation distincte du capteur consommé.
- Cet invariant interdit la dépendance non atomique « front brut + timer démarré ailleurs », à l'origine de l'armement immédiat parasite au front OFF.

---

## 🛑 Interdictions

- Introduire une logique d’application (arm/disarm) dans le cerveau.
- Introduire un `delay` ou un `wait`.
- Déclencher une sirène ou une notification.
