# 🧠 ARSENAL — TABLE OFFICIELLE DES CAPTEURS THERMIQUES · Index canonique des frontières d’autorité — Chauffage
# Domaine : Chauffage / Capteurs structurants
# Statut  : DOCUMENT NORMATIF — RÉFÉRENCE D’ARCHITECTURE
# Portée  : Frontières d’autorité du moteur thermique Arsenal
# ==========================================================

## 🎯 OBJET DU DOCUMENT

Ce document constitue :

- la **TABLE DES MATIÈRES OFFICIELLE DES CAPTEURS THERMIQUES ARSENAL**,  
- le **ROUTEUR D’ORIENTATION DOCUMENTAIRE OPPOSABLE**,  
- la **CARTOGRAPHIE STABLE DES FRONTIÈRES D’AUTORITÉ THERMIQUES**.

Il définit formellement :

- la hiérarchie des familles de capteurs,  
- leur rôle architectural exact,  
- leur position dans la chaîne décisionnelle,  
- leurs frontières d’autorité non franchissables.

👉 Tout capteur structurant du domaine Chauffage doit apparaître **dans ce répertoire et dans cet index**.  
👉 Toute consommation, évolution ou création hors de ces frontières constitue une **violation de gouvernance thermique**.

---

## 🧠 PHILOSOPHIE DE DÉCOUPAGE

Le répertoire `15_capteurs/` est organisé selon une **séparation architecturale stricte des responsabilités** :

### Axes fondamentaux

1. **Cœur décisionnel**  
2. **Autorisation d’exécution**  
3. **Blocages absolus (NIVEAU 1)**  
4. **Contexte humain / absence**  
5. **Paramétrage canonique**  
6. **Auto-ajustement & apprentissage supervisé**  
7. **Observabilité et diagnostics de gouvernance**  
8. **Inertie passive (absence)**  
9. **Cinématique des cycles en présence**  
10. **Physique post-arrêt**  
11. **Physique de reprise**

Chaque fichier représente **UNE FRONTIÈRE D’AUTORITÉ UNIQUE**.  
Aucune frontière ne doit mélanger :

- décision  
- autorisation  
- blocage  
- contexte  
- diagnostic  
- calibration  
- exécution  

---

## 🧱 HIÉRARCHIE GLOBALE DES CAPTEURS THERMIQUES

  Blocages NIVEAU 1
         ↓
  Contexte humain / absence
         ↓
  Capteurs structurants cœur
         ↓
  Paramétrage canonique
         ↓
  Décision centrale
         ↓
  Autorisation thermostat
         ↓
  Exécution matérielle
         ↓
  Diagnostics structurants
         ↓
  Inerties & cinématique thermique
         ↓
  Auto-ajustement supervisé

---

## 📑 TABLE D’ORIENTATION OFFICIELLE

| N° | Fichier | Domaine couvert | Type d’autorité | Rôle principal | Frontière protégée |
|----|---------|----------------|----------------|----------------|-------------------|
| 01 | 01_capteurs_decision.md | Décision centrale | DÉCISION STRUCTURANTE | Capteurs cœur de décision thermique | Décision centrale Chauffage |
| 02 | 02_capteurs_autorisation_thermostat.md | Autorisation thermostat | AUTORISATION D’EXÉCUTION | Verrous et synchronisation API | Frontière d’exécution chauffage |
| 03 | 03_capteurs_blocages_niveau1.md | Blocages NIVEAU 1 | INTERDICTIONS ABSOLUES | Apports externes & enveloppe ouverte | Intégrité thermique bâtiment |
| 04 | 04_capteurs_absence_geofencing.md | Absence / Géofencing | CONTEXTE HUMAIN STRATÉGIQUE | Présence / Absence maison | Contexte humain du moteur |
| 05 | 05_capteurs_parametrage_canonique.md | Paramétrage durable | PARAMÉTRAGE CANONIQUE | Consignes confort / reduced | Références thermiques métier |
| 06 | 06_capteurs_auto_ajustement_calibration.md | Auto-ajustement | APPRENTISSAGE SUPERVISÉ | Propositions & diagnostics calibration | Apprentissage thermique gouverné |
| 07 | 07_capteurs_diagnostics_structurants.md | Diagnostics structurants | OBSERVABILITÉ SOUVERAINE | Audit décisionnel & performance | Observabilité du moteur |
| 08 | 08_capteurs_inertie_absence.md | Inertie absence | OBSERVABILITÉ PASSIVE | Stabilisation & plancher thermique | Inertie passive bâtiment |
| 09 | 09_capteurs_cycles_presence.md | Cycles présence | OBSERVABILITÉ CINÉMATIQUE | Oscillation, période, fréquence | Cinématique moteur en présence |
| 10 | 10_capteurs_inertie_arret.md | Inertie arrêt | OBSERVABILITÉ POST-COUPURE | Overshoot, latence, refroidissement | Physique post-arrêt |
| 11 | 11_capteurs_inertie_reprise.md | Inertie reprise | OBSERVABILITÉ DE REDÉMARRAGE | Erreur, latence, récupération | Physique de reprise |

---

## 🧭 ROUTAGE DOCUMENTAIRE OFFICIEL

### Pour toute question de…

#### 🔥 Décision thermique
→ `01_capteurs_decision.md`  
→ `30_decision_centrale.md`  
→ `80_table_decision_canonique.md`  

#### 🔓 Autorisation / exécution
→ `02_capteurs_autorisation_thermostat.md`  
→ `70_autorisation_thermostat.md`  

#### ⛔ Blocages absolus
→ `03_capteurs_blocages_niveau1.md`  
→ `40_blocages.md`  

#### 🧍 Présence / absence
→ `04_capteurs_absence_geofencing.md`  
→ `60_absence_inhibition_geofencing.md`  

#### ⚙️ Paramétrage thermique
→ `05_capteurs_parametrage_canonique.md`  
→ `75_auto_ajustement_courbe.md`  

#### 🧪 Auto-ajustement / calibration
→ `06_capteurs_auto_ajustement_calibration.md`  

#### 🧠 Audit & gouvernance
→ `07_capteurs_diagnostics_structurants.md`  
→ `90_semantique_thermique.md`  

#### 🏠 Inertie bâtiment (absence)
→ `08_capteurs_inertie_absence.md`  

#### 🔁 Cycles et stabilité
→ `09_capteurs_cycles_presence.md`  

#### ⏹️ Coupure chauffage
→ `10_capteurs_inertie_arret.md`  

#### ▶️ Reprise chauffage
→ `11_capteurs_inertie_reprise.md`  

---

## 🔒 RÈGLES DE GOUVERNANCE FINALES

### Invariants non négociables

- Chaque fichier = **UNE FRONTIÈRE D’AUTORITÉ UNIQUE**  
- Aucun capteur structurant hors de ce répertoire  
- Aucun mélange :
  - décision / diagnostic  
  - autorisation / calibration  
  - blocage / observabilité  
  - apprentissage / exécution  

### Interdictions absolues

- ❌ Aucun capteur de diagnostic utilisé comme décision  
- ❌ Aucun capteur d’apprentissage autorisé à écrire  
- ❌ Aucun capteur inertiel utilisé comme seuil  
- ❌ Aucun court-circuit de frontière dans les automatisations  

---

## 🧠 CONCLUSION ARCHITECTURALE

Le répertoire `15_capteurs/` constitue désormais :

- la **COLONNE VERTÉBRALE DU MOTEUR THERMIQUE ARSENAL**,  
- une **cartographie industrielle des frontières thermiques**,  
- une base sûre pour :
  - auto-ajustement futur  
  - maintenance long terme  
  - audit humain fiable  
  - évolution maîtrisée du système  

👉 Toute évolution future du moteur Chauffage doit commencer par ce document.

==========================================================
