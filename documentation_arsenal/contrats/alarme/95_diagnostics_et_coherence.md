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
- la détection d'échec d'application (réel vs cible),
- la conduite à tenir (diagnostic, pas d'auto-correction).

---

## ✅ Capteurs & signaux d'observabilité

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
  - échec d'application,
  - ou blocage technique,
  - ou intégration défaillante,
  - mais ne doit pas déclencher une auto-correction implicite.

---

## 🛑 Interdictions

- tenter de "forcer" une correction en boucle,
- armer/désarmer automatiquement "par insistance",
- masquer la divergence par un recalcul opportuniste.

---

## ✅ Conduite à tenir (canon Arsenal)

En cas de divergence persistante :

1. lire :
   - `input_text.alarme_etat_cible`
   - `alarm_control_panel.alarme_maison`
   - `input_text.alarme_raison`
2. vérifier les logs d'intégration / erreurs système
3. vérifier la disponibilité des entités consommées (unknown/unavailable)

---

## 🛠️ Exception — Cohérence structurelle corrective

### Périmètre

Certaines incohérences relèvent d'un **problème structurel du système**
et non d'une divergence métier réel vs cible.

Ces incohérences peuvent être corrigées automatiquement par un mécanisme dédié.

Un problème structurel est une incohérence interne entre entités
censées représenter un même état logique via des mécanismes distincts
(ex : état + temporalité).

### Cas autorisés

- incohérence entre un état dérivé et son mécanisme de temporalité
- violation d'un invariant interne clairement défini

Exemple contracté :

- `input_boolean.blocage_armement_auto` ↔ `timer.blocage_armement_auto`

### Principe

```
La correction est autorisée uniquement si :
- elle ne modifie pas une décision métier
- ne doit en aucun cas rendre cohérent un système
  dont la divergence réel / cible persiste
- elle restaure un invariant structurel
```

### Mécanisme

Ces corrections sont assurées par des **watchdogs dédiés** :

- strictement événementiels
- à correction minimale
- sans logique métier
- sans boucle ni retry

### Séparation stricte

| Type | Comportement |
|------|--------------|
| Diagnostic (ce contrat) | Alerte uniquement |
| Watchdog structurel | Correction autorisée |

### Interdictions du watchdog structurel

Un watchdog ne doit jamais :

- armer ou désarmer l'alarme
- modifier `input_text.alarme_etat_cible`
- relancer une application échouée
- masquer une divergence réel / cible

### Référence

- Watchdog blocage armement :
  - automation `10020000000034`
  - contrat associé : `60_delais_et_blocages.md`
  - contrat associé : `95_diagnostics_et_coherence.md` (présent document)
