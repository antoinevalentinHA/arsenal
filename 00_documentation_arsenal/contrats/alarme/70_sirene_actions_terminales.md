# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Sirène (actions terminales)
# ==========================================================

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

- `script.arret_sirene` doit être exécutable **à tout moment**, sans condition.
- Les scripts sirène ne décident jamais :
  - ni “quand biper”,
  - ni “quand hurler”,
  - ni “quand s’arrêter”.
- Toute logique de contexte (mode test, intrusion confirmée, etc.) est ailleurs.

---

## ⏱️ Chemin d'arrêt (extinction) — canonique

L'arrêt de la sirène repose sur **deux mécanismes complémentaires**, et **aucun autre** :

- **Coupe immédiate** — `script.arret_sirene` publie `warning/stop` (MQTT). Il est appelé **inconditionnellement**, en première étape de `script.alarme_desarmer` (priorité absolue, cf. invariants). C'est la seule coupe **avant** échéance.
- **Auto-extinction (canonique)** — portée par le **device** : `script.sirene_brutale` publie `warning/burglar` avec `"duration": number.sirene_max_duration` ; la sirène **s'éteint seule** à l'échéance. Le décompte vit dans le device, indépendamment de Home Assistant → comportement **reboot-safe**. C'est le **mécanisme canonique d'auto-extinction**.

Aucune automatisation Home Assistant ne porte l'auto-extinction. L'ancienne automatisation `11_automations/alarme/sirene/stop.yaml` (déclencheur/cible `switch.sirene_alarm`, `delay`) était **morte** (entité inexistante) et a été **supprimée** (CH-4-B) ; elle ne fait **plus** partie du chemin vivant et **ne doit pas être recréée**. L'entité `switch.sirene_alarm` **n'existe pas**.

---

## 🛑 Interdictions

- utiliser la sirène forte comme feedback UX (armement/désarmement)
- conditionner `arret_sirene` à un état alarme
- déclencher la sirène depuis le cerveau décisionnel
- reconstituer un coupe-circuit d'extinction côté Home Assistant (`delay`/`switch`) : l'auto-extinction est **canoniquement** portée par la durée device (`number.sirene_max_duration`) ; l'entité `switch.sirene_alarm` n'existe pas
