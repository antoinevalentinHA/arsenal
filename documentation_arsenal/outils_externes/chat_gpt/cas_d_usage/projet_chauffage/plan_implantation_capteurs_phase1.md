# ==========================================================
# 🧠 PROJET ARSENAL — PLAN D’IMPLANTATION
# Observabilité Thermique — Phase fondatrice (Présence + Absence)
# ==========================================================

---

## 🎯 Objet

Ce document définit le **plan normatif d’implantation des capteurs de diagnostic thermique**
introduits dans Arsenal pour l’observabilité fine du chauffage en régimes :

- **Présence**
- **Absence**

Il constitue :

* le **pont officiel entre l’architecture et le YAML**
* la référence opposable pour toute création de capteur diagnostic thermique
* la base de traçabilité du domaine analytique Chauffage

Ce document est :

* **NORMATIF**
* structurant pour le domaine Chauffage
* préalable obligatoire à toute création de capteur associé

---

## 🧠 Principe directeur

Chaque capteur de ce domaine doit :

* appartenir à une famille thermique identifiée
* être rattaché à une transition décisionnelle officielle
* mesurer un phénomène physique réel
* être indépendant de toute logique décisionnelle
* être **reload-safe**

Aucun capteur ne peut :

* lire un offset
* lire un seuil
* lire une consigne
* produire une recommandation
* déclencher une action
* influencer la décision centrale

---

## 🧱 Organisation des fichiers

### Dossier cible principal

/homeassistant/11_template_sensors/chauffage/diagnostic_thermique/

### Sous-structure validée

diagnostic_thermique/
│
├── inertie_reprise/
├── inertie_arret/
├── absence/
└── cycles/

Règles :

* un fichier = une métrique principale
* un en-tête Arsenal obligatoire par fichier
* aucun regroupement fonctionnel hétérogène

---

## 🌡️ Sources de données autorisées

### Capteur thermique de référence unique

| Entité                            | Rôle                           |
| --------------------------------- | ------------------------------ |
| `sensor.temperature_min_chambres` | référence thermique officielle |

### Source décisionnelle

| Entité                                       | Rôle                          |
| -------------------------------------------- | ----------------------------- |
| `input_select.chauffage_dernier_mode_decide` | transitions reduced ↔ comfort |

### Repères temporels

| Source  | Usage             |
| ------- | ----------------- |
| `now()` | mesures de durées |

---

## 🧩 FAMILLE A — Inertie post-reprise (offset ON présence)

Dossier : `inertie_reprise/`

### A1 — Température de reprise Présence Chambres

* Rôle : figer la température au moment exact de la reprise  
* Fonction : point de départ thermique officiel du cycle  
* Nature : capteur repère interne (non enregistré au Recorder)  

---

### A2 — Amplitude chute post-reprise

* Entité : `sensor.amplitude_chute_reprise_presence_chambres`  
* Rôle : mesurer la sous-chauffe inertielle maximale  
* Phénomène : inertie bâtiment + hydraulique  
* Recorder : **OUI**  

---

### A3 — Durée chute post-reprise

* Entité : `sensor.duree_chute_reprise_presence_chambres`  
* Rôle : mesurer la latence avant inversion thermique  
* Phénomène : inertie temporelle réelle  
* Recorder : **OUI**  

---

## 🧩 FAMILLE B — Inertie post-arrêt (offset OFF présence)

Dossier : `inertie_arret/`

### B0 — Température d’arrêt Présence Chambres

* Rôle : figer la température au moment exact de la coupure  
* Fonction : point de départ overshoot officiel  
* Nature : capteur repère interne (non enregistré au Recorder)  

---

### B1 — Amplitude overshoot post-arrêt

* Entité : `sensor.amplitude_overshoot_arret_presence_chambres`  
* Rôle : mesurer la surchauffe inertielle maximale  
* Phénomène : inertie hydraulique / chaudière  
* Recorder : **OUI**  

---

### B2 — Durée overshoot post-arrêt

* Entité : `sensor.duree_overshoot_arret_presence_chambres`  
* Rôle : mesurer la latence thermique après coupure  
* Phénomène : diffusion résiduelle réelle  
* Recorder : **OUI**  

---

## 🧩 FAMILLE C — Dynamiques thermiques réelles

Famille transversale montée / perte thermique  
Regroupant dynamiques **Présence** et **Absence**

---

### C1 — Vitesse réelle de reprise (Présence)

* Entité : `sensor.vitesse_reprise_presence_chambres`  
* Rôle : mesurer la dynamique de montée (°C/h)  
* Phénomène : efficacité courbe de chauffe + émetteurs  
* Usage stratégique : dissociation offsets / courbe  
* Recorder : **OUI**  

---

### C2 — Vitesse réelle de refroidissement (Présence)

* Entité : `sensor.vitesse_refroidissement_presence_chambres`  
* Rôle : mesurer la perte thermique passive (°C/h)  
* Phénomène : inertie bâtiment + isolation  
* Usage stratégique : calibration offsets absence future  
* Recorder : **OUI**  

---

### C1A — Température plancher atteinte en Absence

Dossier : `absence/`

* Entité : `sensor.temperature_plancher_absence_chambres`  
* Rôle : mesurer la température minimale réellement atteinte pendant un cycle d’absence  
* Phénomène : profondeur thermique réelle du bâtiment  
* Usage stratégique :  
  - qualification inertie froide  
  - validation offsets absence  
* Nature : capteur intra-cycle figé naturellement  
* Recorder : **OUI**  

---

### C3 — Durée de stabilisation thermique en Absence

Dossier : `absence/`

* Entité : `sensor.duree_stabilisation_absence_chambres`  
* Rôle : mesurer le temps nécessaire pour atteindre un régime quasi-stationnaire  
* Phénomène : inertie froide + pertes structurelles  
* Usage stratégique :  
  - caractérisation inertielle bâtiment  
  - garde-fou auto-ajustement offsets  
* Nature : capteur intra-cycle figé dès stabilisation  
* Recorder : **OUI**  

---

## 🧩 FAMILLE D — Stabilité globale des cycles

Dossier : `cycles/`

Famille dédiée à la **stabilité structurelle** du pilotage thermique.
Elle ne mesure pas une dynamique locale (montée / chute), mais le système comme **oscillateur thermique global**.

La famille D Phase 1 couvre exclusivement les cycles du régime Présence,
considérés comme régime de référence du pilotage thermique.

L’analyse des cycles en régime Absence relève d’une extension ultérieure
hors périmètre Phase 1.

Capteurs constitutifs :

- **D1** : amplitude (déjà implémenté)
- **D2** : fréquence journalière des cycles
- **D3** : période moyenne des cycles

Ces trois métriques forment le triplet canonique :

- amplitude
- fréquence
- période

---

### D2 — Nombre cycles jour Présence Chambres

* Entité : `sensor.nombre_cycles_jour_presence_chambres`
* Rôle : mesurer la **nervosité structurelle** du système (stress chaudière / instabilité)
* Phénomène : fréquence effective des cycles thermiques complets sur une journée civile
* Ancrage : basé sur les reprises validées (repère A1) et la périodicité des redémarrages
* Nature : capteur **journalier**, inter-cycle, figé en fin de journée
* Contraintes :
  - aucun accès offsets / seuils / consignes
  - aucune dépendance température
  - calculs temporels uniquement en `now().timestamp()`
* Recorder : **OUI (prioritaire)**

---

### D3 — Durée cycle moyenne Présence Chambres

* Entité : `sensor.duree_cycle_moyenne_presence_chambres`
* Rôle : mesurer l’**inertie temporelle globale** (période propre du système thermique)
* Phénomène : durée moyenne entre deux reprises chauffage successives (cycle complet)
* Ancrage : basé sur les timestamps de reprises validées (repère A1)
* Nature : capteur **journalier**, inter-cycle, figé en fin de journée
* Contraintes :
  - aucun accès offsets / seuils / consignes
  - aucune dépendance température
  - calculs temporels uniquement en `now().timestamp()`
* Cohérence interne attendue :
  - relation d’ordre de grandeur : `D2 ≈ 24h / D3`
* Recorder : **OUI (prioritaire)**

---

## 🛡️ Politique Recorder associée

Capteurs intégrés explicitement dans `/homeassistant/recorder.yaml` :

* `sensor.amplitude_chute_reprise_presence_chambres`  
* `sensor.duree_chute_reprise_presence_chambres`  
* `sensor.amplitude_overshoot_arret_presence_chambres`  
* `sensor.duree_overshoot_arret_presence_chambres`  
* `sensor.vitesse_reprise_presence_chambres`  
* `sensor.vitesse_refroidissement_presence_chambres`  
* `sensor.amplitude_oscillation_cycle_presence_chambres`  
* `sensor.temperature_plancher_absence_chambres`  
* `sensor.duree_stabilisation_absence_chambres`  
* `sensor.nombre_cycles_jour_presence_chambres`  
* `sensor.duree_cycle_moyenne_presence_chambres`  

Capteurs exclus volontairement :

* `sensor.temperature_reprise_presence_chambres`  
* `sensor.temperature_arret_presence_chambres`  

Principe :

* uniquement métriques synthèse par cycle  
* exclusion des repères techniques instantanés  
* conformité stricte au contrat Recorder Arsenal  

---

## 🔒 Contraintes reload YAML

Tous les capteurs doivent :

* utiliser exclusivement `states()`  
* tolérer `unknown` / `unavailable`  
* ne dépendre d’aucun ordre de chargement  
* ne contenir aucune `condition: state`  
* utiliser exclusivement des timestamps bruts `now().timestamp()`  

---

## 🧠 Séquence d’implémentation validée

1. Infrastructure transitions (A1, B0)  
2. Inerties reprise (A2, A3)  
3. Inerties arrêt (B1, B2)  
4. Dynamiques présence (C1, C2)  
5. Dynamiques absence (C1A, C3)  
6. Synthèse stabilité (D1)  
7. Intégration Recorder  

---

## 📌 Finalité

Ce plan garantit :

* une observabilité thermique scientifique  
* une séparation stricte diagnostic / décision  
* une base historique exploitable long terme  
* un socle solide pour futur auto-ajustement offsets  

Il constitue le **référentiel d’implantation officiel du domaine Diagnostic Thermique Chauffage**.

---

## 🏷️ Statut

* Document projet Chauffage Arsenal  
* Normatif et structurant  
* Domaine : Observabilité thermique Présence & Absence  
* Toute modification doit être :  
  • explicitement décidée  
  • documentée  
  • consolidée au changelog
