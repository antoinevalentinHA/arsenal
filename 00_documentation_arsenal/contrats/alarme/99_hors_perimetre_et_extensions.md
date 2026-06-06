# 🧠 ARSENAL — CONTRAT MÉTIER · Alarme — Hors périmètre & extensions

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme**
- Chemin : `homeassistant/00_documentation_arsenal/contrats/alarme/99_hors_perimetre_et_extensions.md`

---

## 🎯 Objet

Définir ce qui est hors périmètre du domaine alarme, et comment intégrer
des extensions sans contaminer le noyau.

---

## 🧱 Hors périmètre (strict)

- La détection technique de présence (GPS, Wi-Fi, etc.)
- L’architecture interne Zigbee2MQTT
- La “visite” en tant que domaine autonome de planification humaine
- Les arbitrages de confort (chauffage / ECS)

---

## 🧩 Visite : position contractuelle

La visite est un **contexte humain explicite**.

- Elle peut être consommée par l’alarme comme :
  - neutralisation / inhibition / adaptation

Mais la logique de planification visite (jours / créneaux) n’appartient pas
au noyau alarme.

Recommandation d’architecture :

- isoler la visite dans un dossier contractuel dédié (ex : [`visite.md`](../visite.md))
- l’alarme ne consomme qu’un signal stable :
  - `input_boolean.presence_visiteur`
  - `input_boolean.visite_en_cours`
  - ou un unique binaire métier “visite active”.

---

## ✅ Extensions autorisées

Une extension est admissible si :

- elle n’introduit aucune logique décisionnelle hors cerveau,
- elle expose un état simple, stable, consommable,
- elle respecte les invariants alarme (séparation, idempotence, unicité).

Exemples :

- nouveaux capteurs intrusion
- nouveaux canaux de notification
- nouveaux inhibiteurs explicites (mode babysitting, etc.)

---

## 🛑 Interdictions

- créer une “nouvelle alarme” locale
- multiplier les cerveaux
- coupler une extension à des actions directes sur `alarm_control_panel`
