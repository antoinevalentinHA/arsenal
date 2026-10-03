# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Sirène (actions terminales)

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/70_sirene_actions_terminales.md`

---

## 🎯 Objet

Définir les scripts sirène comme **actions terminales** :

- aucun raisonnement,
- aucun état de sécurité calculé,
- exécution explicite et traçable.

---

## ✅ Scripts canoniques

- `script.sirene_bip`
  - bip court “sécurisé” (avec garde disponibilité indirecte)
- `script.sirene_bip_bip`
  - double bip de confirmation (désarmement)
- `script.sirene_brutale`
  - sirène forte (mode intrusion)
- `script.arret_sirene`
  - arrêt immédiat (priorité absolue)

---

## 🔒 Invariants

- `script.arret_sirene` doit être exécutable **à tout moment** : le script lui-même ne porte **aucune** condition (ni état alarme, ni mode test).
- Les scripts sirène ne décident jamais :
  - ni “quand biper”,
  - ni “quand hurler”,
  - ni “quand s’arrêter”.
- Toute logique de contexte (intrusion confirmée, origine, délai, etc.) est ailleurs.

### Verrou mode test — silence physique absolu (C54)

`input_boolean.mode_test_alarme == on` ⇒ **aucune émission sonore** de la chaîne alarme.

- Chaque script sirène **émetteur de son** — `script.sirene_bip`, `script.sirene_bip_bip`, `script.sirene_brutale`, `script.sirene_test` — porte, **en première étape**, le verrou :
  `{{ not is_state('input_boolean.mode_test_alarme', 'on') }}`.
- Ce verrou est un **veto physique**, pas une décision : il ne dit ni quand biper ni quand hurler, il interdit l'émission quel que soit l'appelant. Il garantit l'invariant même si un appelant (automation, script, UI, appel direct) omet sa propre garde. Les gardes des appelants sont **conservées** (défense en profondeur).
- **Fail-open** : seul `on` explicite bloque. Un état absent, `unknown` ou `unavailable` n'inhibe jamais la sirène réelle (même parti que `50_intrusion` §I7).
- Le mode test reste un mode de **test logique complet** : détection, décision, timers, transitions de panneau, notifications et traces sont inchangés ; seule l'émission physique est coupée.
- `script.arret_sirene` est **hors verrou** (voir § Chemin d'arrêt).

---

## ⏱️ Chemin d'arrêt (extinction) — canonique

L'arrêt de la sirène repose sur **deux mécanismes complémentaires**, et **aucun autre** :

- **Coupe immédiate** — `script.arret_sirene` publie `warning/stop` (MQTT). C'est la seule coupe **avant** échéance. Deux appelants :
  - `script.alarme_desarmer`, en première étape, **uniquement si** `alarm_control_panel.alarme_maison == triggered` — seul état dans lequel Arsenal lance la sirène forte (`10020000000011`). Cette condition est **indépendante du mode test** : une sirène réellement lancée doit pouvoir être coupée même si le mode test a été activé pendant le hurlement ;
  - le bouton UI « Arrêt sirène » (`carte_action_arret_sirene`), **inconditionnel**.

> **Constat terrain (2026-10-03, C54) — la commande d'arrêt est sonore.** Sur la Develco/Frient SIRZB-111, le payload `{"warning":{"mode":"stop"}}` **produit une séquence à deux tons** (~4 cycles) au lieu d'un silence. Prouvé par traces runtime + reproduction opérateur (désarmement dashboard 18:47:44, bouton UI 18:51:00). Conséquence : avant C54, **chaque désarmement** (automatique compris, mode test compris) faisait sonner la sirène. D'où la restriction de l'appel au seul état `triggered`.
>
> **Réserves ouvertes (C54, lot 2)** : (i) le bouton UI reste sonore ; (ii) l'**efficacité** de ce `stop` sur une sirène en plein hurlement n'est **pas** établie (V4 a prouvé l'auto-extinction par durée, pas la coupe par `stop`) ; (iii) la trame Zigbee réellement émise par Zigbee2MQTT n'a pas été observée. Correction du payload : **essai réel autorisé par l'opérateur uniquement**.

**Contrainte de cohérence** : l'auto-extinction device (`number.sirene_max_duration`, 60 s) doit rester **inférieure ou égale** à `trigger_time` du panneau (180 s, `16_template_alarm_panels/alarme_maison.yaml`). Sinon la sirène pourrait hurler après le retour du panneau hors `triggered`, et le désarmement ne la couperait plus.
- **Auto-extinction (canonique)** — portée par le **device** : `script.sirene_brutale` publie `warning/burglar` avec `"duration": number.sirene_max_duration` ; la sirène **s'éteint seule** à l'échéance. Le décompte vit dans le device, indépendamment de Home Assistant → comportement **reboot-safe**. C'est le **mécanisme canonique d'auto-extinction**.

Aucune automatisation Home Assistant ne porte l'auto-extinction. L'ancienne automatisation `11_automations/alarme/sirene/stop.yaml` (déclencheur/cible `switch.sirene_alarm`, `delay`) était **morte** (entité inexistante) et a été **supprimée** (CH-4-B) ; elle ne fait **plus** partie du chemin vivant et **ne doit pas être recréée**. L'entité `switch.sirene_alarm` **n'existe pas**.

---

## 🛑 Interdictions

- utiliser la sirène forte comme feedback UX (armement/désarmement)
- conditionner le **script** `arret_sirene` lui-même (état alarme, mode test) — seul l'**appel** depuis `script.alarme_desarmer` est restreint à `triggered`
- émettre `warning/stop` sur un désarmement hors `triggered` (commande sonore, C54)
- publier vers `zigbee2mqtt/sirene/set` ailleurs que dans les scripts sirène canoniques (`10_scripts/alarme/sirene/`)
- retirer ou rendre fail-closed le verrou mode test d'un script sirène émetteur
- déclencher la sirène depuis le cerveau décisionnel
- reconstituer un coupe-circuit d'extinction côté Home Assistant (`delay`/`switch`) : l'auto-extinction est **canoniquement** portée par la durée device (`number.sirene_max_duration`) ; l'entité `switch.sirene_alarm` n'existe pas
