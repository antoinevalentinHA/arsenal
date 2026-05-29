# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Modèle d’états & vocabulaire
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/10_modele_etats_et_vocabulaire.md`

---

## 🎯 Objet

Définir le vocabulaire canonique de l’alarme :

- états réels (panneau),
- états logiques (cible),
- codes décisionnels internes,
- sémantique NOOP.

---

## 🧱 États réels (source : `alarm_control_panel.alarme_maison`)

États consommés comme “réels” :

- `disarmed`
- `armed_away`
- `pending`
- `triggered`

Tout autre état est accepté comme “brut”, mais ne doit pas être inventé
par Arsenal.

---

## 🧠 États logiques cibles (source : `input_text.alarme_etat_cible`)

Valeurs autorisées :

- `DISARMED`
- `ARMED_AWAY`
- `NOOP`

Règles :

- `NOOP` signifie : **aucune action** ne doit être tentée.
- L’état cible n’est pas un état réel : c’est une **intention publiée**.

---

## 🧾 Codes décisionnels (source : `input_text.alarme_decision`)

Ces codes sont des identifiants “machine” (diagnostic + audit) :

- `VISITEUR_PRESENT`
- `PRESENCE`
- `MODE_NON_AUTOMATIQUE`
- `ABSENCE_NON_STABLE`
- `BLOCAGE_AUTO`
- `DELAI_ENTREE`
- `ARMEMENT_AUTORISE`

Règle :

- Toute extension d’un code décisionnel implique :
  - mise à jour du cerveau,
  - mise à jour des diagnostics,
  - entrée de changelog.

---

## 🧠 Raison (source : `input_text.alarme_raison`)

`input_text.alarme_raison` contient une justification humaine, lisible,
alignée sur le code décisionnel.

Elle est :

- informative,
- non exécutoire,
- jamais utilisée comme trigger canonique.

---

## 🧪 Sémantique NOOP

NOOP est un état **intentionnel** :

- il évite les actions inutiles,
- il stabilise les retriggers,
- il permet une UI / diag explicite.

NOOP ne signifie pas “on ne sait pas” :
- “on ne sait pas” = `unknown/unavailable`.
