# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Alarme — Diagnostics, cohérence, divergence
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Sécurité / Alarme / Observabilité**
- Chemin : `homeassistant/documentation_arsenal/contrats/alarme/95_diagnostics_et_coherence.md`

---

## 🎯 Objet

Définir :

- les capteurs de cohérence,
- la détection d’échec d’application (réel vs cible),
- la conduite à tenir (diagnostic, pas d’auto-correction).

---

## ✅ Capteurs & signaux d’observabilité

### Cohérence alarme

- `binary_sensor.alarme_systeme_coherent`
  - attribut : `raison`

### Armement auto récent

- `binary_sensor.alarme_armee_auto_recentement`
  - fenêtre : 120 s
  - basé sur `automation.alarme_armement_automatique_en_cas_d_absence` (last_triggered)

### Divergence réel / cible (alerte)

- automation :
  - ID `10020000000030`
  - déclenche une alerte si divergence persiste 5 min

---

## 🧠 Principes

- Le diagnostic est **constatif**.
- Une divergence indique :
  - échec d’application,
  - ou blocage technique,
  - ou intégration défaillante,
  - mais ne doit pas déclencher une auto-correction implicite.

---

## 🛑 Interdictions

- tenter de “forcer” une correction en boucle,
- armer/désarmer automatiquement “par insistance”,
- masquer la divergence par un recalcul opportuniste.

---

## ✅ Conduite à tenir (canon Arsenal)

En cas de divergence persistante :

1) lire :
   - `input_text.alarme_etat_cible`
   - `alarm_control_panel.alarme_maison`
   - `input_text.alarme_raison`
2) vérifier les logs d’intégration / erreurs système
3) vérifier la disponibilité des entités consommées (unknown/unavailable)
