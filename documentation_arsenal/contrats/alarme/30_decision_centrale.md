# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Interfaces contexte & helpers
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/documentation_arsenal/contrats/alarme/20_interfaces_contexte_et_helpers.md`

---

## 🎯 Objet

Définir les **entrées contextuelles** consommées par l’alarme et les **sorties**
publiées par le cerveau alarme via helpers.

---

## 🔌 Entrées contractuelles (lecture)

### Stratégie alarme

- `input_select.mode_alarme`
  - Valeurs attendues :
    - `Manuel`
    - `Automatique`
    - `Désactivé`

### Présence sécurité (autorité contractuelle : présence)

- `binary_sensor.presence_famille_securite`

### Absence stabilisée (projection temporelle)

- `binary_sensor.presence_famille_securite_absent_depuis_5_min`
  - Doit être un état “prêt à consommer” par l’alarme.
  - Son mode de calcul est hors périmètre alarme (mais opposable).

### Blocage armement auto (verrou logique)

- `input_boolean.blocage_armement_auto`

### Délai d’entrée (projection temporelle)

- `binary_sensor.delai_desarmement_en_cours`
  - Contractuellement : ON si `timer.delai_entree` est `active`.

### Contexte visite (signal externe au noyau alarme)

- `input_boolean.presence_visiteur`
- `input_boolean.visite_en_cours`
- `binary_sensor.creneau_visiteur_actif`
- `input_boolean.mode_visiteur`
- `input_select.jour_visiteur`
- `input_datetime.visiteur_start`
- `input_datetime.visiteur_end`

Remarque :
- La visite est un **contexte humain explicite**, pas une présence.
- Le noyau alarme peut la consommer comme **inhibition / neutralisation**.

---

## 📤 Sorties contractuelles (écriture)

Les helpers suivants sont **exclusivement écrits** par :

- `script.alarme_decision_centrale`

### Décision

- `input_text.alarme_decision`

### État cible

- `input_text.alarme_etat_cible`

### Raison humaine

- `input_text.alarme_raison`

---

## 🔒 Interdictions formelles

Il est interdit :

- d’écrire `input_text.alarme_*` depuis une automation, un capteur, ou l’UI,
- de recalculer une “décision alarme” ailleurs que dans le cerveau,
- de remplacer présence sécurité par une autre présence.
