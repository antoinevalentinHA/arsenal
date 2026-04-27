# 🧠 ARSENAL — CONTRAT NORMATIF
## Présence / Alarme — Mode Visiteur (Visite planifiée)

---

## 📌 Statut

CONTRAT NORMATIF — FAIT FOI

Ce document définit la doctrine officielle du mode Visiteur dans Arsenal.

En cas de divergence :
- le comportement réel des automatisations prévaut,
- les alias et descriptions ne font pas autorité.

---

## 🔒 Autorité

Ce contrat fixe :

- le modèle métier du mode visite,
- les sources de vérité,
- les invariants,
- les points d’écriture autorisés,
- les interdictions.

Aucune évolution ne doit violer ce cadre sans révision formelle.

---

## 🎯 Rôle

Le mode Visiteur matérialise un contexte humain explicite indiquant la présence de personnes extérieures au foyer sur un créneau planifié.

Il permet d’adapter les raisonnements :

- alarme,
- présence,
- énergie.

Il ne repose sur aucune déduction automatique.

---

## 🧭 Périmètre

Ce contrat couvre :

- la planification visite,
- le calcul du créneau actif,
- l’activation / désactivation,
- la reconstruction post-redémarrage,
- la projection UI.

Il ne couvre pas :

- la décision centrale alarme,
- les logiques thermiques internes,
- les règles de présence hors visite.

---

## 🧩 Entités canoniques

### Paramétrage

- input_select.jour_visiteur
- input_datetime.visiteur_start
- input_datetime.visiteur_end

### Autorisation

- input_boolean.mode_visiteur

### États métier

- input_boolean.visite_en_cours
- input_boolean.presence_visiteur

### Temporalité

- binary_sensor.creneau_visiteur_actif

### Système

- input_boolean.systeme_stable

### UI

- persistent_notification : visiteur_etat

---

## 🧱 Sources de vérité

| Domaine       | Entité                              |
|---------------|-------------------------------------|
| Temporalité   | binary_sensor.creneau_visiteur_actif |
| Contexte      | input_boolean.visite_en_cours        |
| Occupation    | input_boolean.presence_visiteur      |
| Projection UI | visiteur_etat                        |

---

## ✅ Invariants

### I1 — Calcul temporel unique

Le calcul jour/heure est exclusivement porté par :

binary_sensor.creneau_visiteur_actif

---

### I2 — Garde-fou de programmation

Si :

input_boolean.mode_visiteur = off

alors :

binary_sensor.creneau_visiteur_actif = off

obligatoirement.

---

### I3 — Écriture contrôlée

Seules les automations suivantes écrivent les états métier :

| ID | Rôle |
|----|------|
| 10210000000003 | Activation |
| 10210000000004 | Désactivation |
| 10210000000005 | Reconstruction |

---

### I4 — Couplage contexte / occupation

En régime stable :

visite_en_cours = on ⇔ presence_visiteur = on

---

### I5 — Nettoyage fort

À la sortie du mode visite :

- visite_en_cours = off
- presence_visiteur = off

Aucun effet sur les équipements énergétiques.

---

### I6 — Projection UI pure

La notification persistante :

- existe si visite_en_cours = on,
- est absente si visite_en_cours = off,
- est gérée uniquement par l’ID 10210000000006.

---

### I7 — Reconstruction déterministe

Après redémarrage :

systeme_stable = on ⇒ réalignement sur creneau_visiteur_actif

sans historique.

---

### I8 — Isolation énergétique

Le mode visite ne pilote aucun équipement énergétique.

En particulier :

- aucun accès à switch.prise_bouclage
- aucune influence sur le bouclage ECS

---

## 🧠 Capteur métier — Créneau visiteur actif

Fichier : 11_template_sensors/presence/visite.yaml

Doctrine :

Le créneau est actif si et seulement si :

- mode_visiteur = on
- jour courant = jour sélectionné
- heure courante ∈ [start, end]

Paramètres consommés :

- input_boolean.mode_visiteur
- input_select.jour_visiteur
- input_datetime.visiteur_start
- input_datetime.visiteur_end

---

### Limitation temporelle

L’implémentation actuelle impose :

visiteur_start ≤ visiteur_end

Les créneaux traversant minuit ne sont pas supportés.

---

## 🔄 Transitions canoniques

### Entrée en visite — Activation

ID : 10210000000003

Déclencheur :
- creneau_visiteur_actif : off → on

Condition :
- visite_en_cours = off

Effets :

- visite_en_cours → on
- presence_visiteur → on
- notification mobile

---

### Sortie de visite — Désactivation

ID : 10210000000004

Déclencheur :
- creneau_visiteur_actif : on → off

Condition :
- visite_en_cours = on

Effets :

- visite_en_cours → off
- presence_visiteur → off

---

### Reconstruction — Reboot

ID : 10210000000005

Déclencheur :
- systeme_stable : off → on

Effets :

Si creneau_visiteur_actif = on :

- visite_en_cours → on
- presence_visiteur → on

Sinon :

- visite_en_cours → off
- presence_visiteur → off

---

## 🧩 Notification persistante

ID : 10210000000006

Déclencheur :
- changement de visite_en_cours

Règle :

- ON  → création visiteur_etat
- OFF → suppression visiteur_etat

Exclusivité stricte.

---

## 🚫 Interdictions

### D1 — Calcul temporel parallèle

Aucune automation ne calcule jour ou heure.

---

### D2 — Double autorité

Aucun autre composant n’écrit :

- visite_en_cours
- presence_visiteur

---

### D3 — Concurrence UI

Aucun autre composant ne manipule visiteur_etat.

---

### D4 — Pilotage énergétique interdit

Le domaine VISITE ne doit jamais :

- piloter un switch énergétique
- influencer le bouclage ECS
- introduire de logique thermique

---

## 🧪 Tests de conformité

### T1 — Garde-fou

mode_visiteur off ⇒ creneau_visiteur_actif off

---

### T2 — Activation

creneau off → on ⇒ visite_en_cours on + presence_visiteur on

---

### T3 — Désactivation

creneau on → off ⇒ tous états off

---

### T4 — Reboot

systeme_stable on ⇒ état conforme au créneau

---

## 📎 Fichiers impliqués

### Helpers

- 05_input_booleans/presence/mode_visite_auto.yaml
- 05_input_booleans/presence/visite_en_cours.yaml
- 05_input_booleans/presence/visiteur.yaml
- 06_input_selects/presence/jour_visite.yaml
- 07_input_datetimes/presence/creneau_visite.yaml

### Capteur

- 11_template_sensors/presence/visite.yaml

### Automations

- activation.yaml (10210000000003)
- desactivation.yaml (10210000000004)
- securite_reboot.yaml (10210000000005)
- notification.yaml (10210000000006)

---

## ✅ Fin du contrat

Toute modification de ce sous-système doit préserver l’intégralité des invariants ci-dessus.