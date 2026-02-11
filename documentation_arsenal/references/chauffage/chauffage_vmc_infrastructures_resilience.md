# ==========================================================
# 🧠 ARSENAL — DOCUMENT D’ARCHITECTURE & DE RÉFÉRENCE
#     Chauffage / VMC / Infrastructure — V3 PRO
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT DE RÉFÉRENCE TECHNIQUE — NON NORMATIF
#
# 🔒 AUTORITÉ :
#   Ce document ne constitue PAS un contrat métier opposable.
#   Il ne possède AUCUNE autorité décisionnelle.
#
#   En cas de divergence, seules font foi les références normatives :
#     - /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#     - /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     - /documentation_arsenal/contrats/chauffage/60_table_decision_canonique.md
#
# 🎯 RÔLE :
#   Centraliser une vue transversale du système Arsenal V3 PRO :
#     - synthèse doctrinale Chauffage,
#     - architecture technique Chauffage,
#     - paramètres thermiques opérationnels,
#     - architecture VMC,
#     - infrastructure & résilience capteurs.
#
#   Ce document joue un rôle :
#     • de cartographie d’architecture,
#     • de fiche de paramétrage consolidée,
#     • de support de compréhension globale du système.
#
# ----------------------------------------------------------
# ⚠️ ANALYSE & POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------
#
# Ce document regroupe plusieurs natures distinctes :
#
#   1) Doctrine synthétique Chauffage
#      → version simplifiée et historiquement intermédiaire
#        du modèle décisionnel actuel.
#
#   2) Architecture technique détaillée
#      → description fidèle des patterns réels (souveraineté,
#        atomicité, guard, mirroring, apprentissage statistique).
#
#   3) Paramétrage opérationnel
#      → photographie des consignes, seuils et délais en vigueur
#        à un instant donné.
#
#   4) Sous-systèmes connexes (VMC, résilience)
#      → documentation d’architecture multi-domaines.
#
# En conséquence :
#
# - La section « Contrat Métier : Chauffage » contenue ici :
#     ❌ ne reflète PLUS la hiérarchie normative réelle,
#     ❌ introduit une hiérarchie décisionnelle fictive (5 niveaux),
#     ❌ assimile à tort :
#         • standby comme cause métier,
#         • protection thermique comme niveau décisionnel,
#         • confort d’opportunité comme décision automatique.
#
# - Cette section est conservée :
#     • comme mémoire conceptuelle,
#     • comme vue pédagogique ancienne,
#     • comme trace d’évolution du modèle mental.
#
# Elle ne doit JAMAIS être utilisée comme base de conception.
#
# ----------------------------------------------------------
# 🧠 RÈGLE DE GOUVERNANCE DOCUMENTAIRE
# ----------------------------------------------------------
#
# - Ce document :
#     ❌ n’est PAS normatif,
#     ❌ n’est PAS opposable au YAML,
#     ❌ ne doit PAS servir d’arbitrage métier,
#     ❌ ne doit PAS être cité comme source de règle.
#
# - Il est autorisé uniquement pour :
#     ✅ compréhension globale,
#     ✅ audit d’architecture,
#     ✅ communication interne,
#     ✅ photographie d’état système.
#
# ----------------------------------------------------------
# 📌 HISTORIQUE & VALEUR
# ----------------------------------------------------------
#
# - Nature :
#     Dossier d’architecture consolidé Arsenal V3 PRO.
#
# - Valeur principale :
#     Très forte valeur d’architecture technique
#     (patterns de souveraineté, locking, apprentissage, guard).
#
# - Limite principale :
#     Doctrine Chauffage partiellement obsolète
#     par rapport aux contrats normatifs actuels.
#
# ==========================================================


# 📂 DOCUMENTATION COMPLÈTE — ARSENAL V3 PRO

## 📑 1. CONTRAT MÉTIER : CHAUFFAGE

### 🎯 Objet
Garantir le confort thermique en présence et la sobriété en absence, tout en protégeant l'infrastructure matérielle contre les instabilités logicielles (Cloud/API).

### ⚖️ Hiérarchie des Causes (Strict)
La décision finale est dictée par une hiérarchie de priorités descendantes. Une cause de niveau supérieur écrase systématiquement les ordres des niveaux inférieurs.
1. **Niveau 1 — Blocages Absolus** : Fenêtre ouverte, Poêle actif, Mode Vacances, Aération.
   - *Action* : Mode **ECO** forcé.
2. **Niveau 2 — Autorisation Système** : Hystérésis de protection post-blocage.
   - *Action* : **ATTENTE** (Maintien de l'état précédent).
3. **Niveau 3 — Standby (Hystérésis Thermique)** : Seuil de température non atteint.
   - *Action* : **ATTENTE** (Repos nominal).
4. **Niveau 4 — Confort d’Opportunité** : Présence détectée ou Forçage manuel.
   - *Action* : Mode **CONFORT** requis.
5. **Niveau 5 — Protection Thermique** : Absence prolongée avec dérive excessive.
   - *Action* : Mode **CONFORT** ponctuel (Inhibition).

### 🚫 Règles d'Or
- **Indépendance de la Présence** : La présence est une autorisation de chauffe, jamais une autorité thermique. C'est l'écart de température qui déclenche l'action.
- **Souveraineté Locale** : En cas de déconnexion Cloud, le système utilise sa dernière mémoire d'intention pour maintenir le service.
- **Transparence** : Chaque état doit être justifié par une `raison_calculee` explicite.

---

## 🏗️ 2. ARCHITECTURE TECHNIQUE : CHAUFFAGE

### 🏛️ Modèle "Trigger - Decision - Action - Guard"
L'architecture repose sur un cycle asynchrone sécurisé pour traiter avec des API Cloud lentes ou instables.

#### 🧩 Couches Fonctionnelles
1. **Le Diapason (Mesure & Mirroring)** : `sensor.ecart_consigne_confort` & `sensor.temperature_consigne_appliquee_locale`.
   - *Rôle* : Mesure de la tension thermique. Utilise des miroirs locaux (`sensor..._local`) pour calculer l'écart en temps réel sans dépendance au cloud.
2. **La Partition (Cible)** : `sensor.chauffage_autorisation_cible`.
   - *Rôle* : Traduction des faits physiques en intention ternaire (`comfort`, `reduced`, `neutre`) via une double hystérésis.
3. **L'Expertise Statistique (Intelligence)** : `sensor.chauffage_pente_suggeree` & `parallele_suggeree`.
   - *Rôle* : Analyse statistique des dérives (moyennes 24h et périodes froides) pour proposer des ajustements de la loi d'eau.
4. **L'Étincelle (Trigger)** : `automation.chauffage_trigger_decision_centrale`.
   - *Rôle* : Observateur de contexte (fenêtre, poêle, présence) ou watchdog.
5. **Le Cerveau (Décision)** : `script.chauffage_decision_centrale`.
   - *Rôle* : Arbitre souverain appliquant la table de décision.
6. **L'Optimiseur (Loi d'eau)** : `automation.chauffage_decision_auto_ajustement_courbe`.
   - *Rôle* : Instance décisionnelle quotidienne (10h00) appliquant les suggestions de l'Expertise Statistique.
7. **Les Bras (Exécution)** : Scripts `chauffage_appliquer_...`.
   - *Rôle* : Gestionnaires de transactions Cloud avec gestion du verrouillage système.
8. **La Police (Garde)** : `automation.realignement_vicare_ha`.
   - *Rôle* : Surveillant de souveraineté. Corrige toute dérive passive du matériel par rapport à la mémoire locale.

#### 🔒 Invariants Architecturaux
- **Pattern de Souveraineté** : Les `input_number` et `input_select` locaux sont la seule source de vérité.
- **Pattern d'Atomicité (Locking)** : Le verrou `input_boolean.chauffage_application_en_cours` suspend la Garde pendant toute écriture vers le Cloud.
- **Pattern d'Apprentissage** : Segmentation thermique entre Dérive Temps Doux ($T_{ext} \ge 10^\circ\text{C}$ pour Parallèle) et Dérive Temps Froid ($T_{ext} \le 5^\circ\text{C}$ pour Pente).

---

## 🛠️ 3. FICHE DE PARAMÉTRAGE : CHAUFFAGE

### 🌡️ Consignes et Seuils Thermiques
| Paramètre | Valeur | Source |
| :--- | :--- | :--- |
| Consigne Confort | **19,0 °C** | |
| Consigne Réduite | **15,0 °C** | |
| Seuil Chauffage (Ext) ON | **15,0 °C** | |
| Seuil Chauffage (Ext) OFF | **18,0 °C** | |
| Offset ON (Hystérésis) | **0,2 °C** | |
| Offset OFF (Hystérésis) | **0,5 °C** | |
| Protection Absence (ON) | **0,6 °C** | |
| Protection Absence (OFF) | **0,0 °C** | |

### 📐 Loi d'Eau (Courbe de Chauffe)
| Paramètre | Valeur | Source |
| :--- | :--- | :--- |
| Pente actuelle | **1,8** | |
| Parallèle actuel | **1,0 °C** | |
| Ajustement Auto | **ACTIF** | |
| Mode Simulation | **DÉSACTIVÉ** | |

### 🛡️ Délais de Sécurité et Blocages
| Paramètre | Valeur | Source |
| :--- | :--- | :--- |
| Système de blocage aération | **ACTIF** | |
| Délai stabilisation aération | **15 min** | |
| Durée blocage après poêle | **45 min** | |

---

## 🏗️ 4. ARCHITECTURE & LOGIQUE : VMC

### 🏛️ Modèle Décisionnel
La VMC repose sur le découplage entre l'Analyse (Requête), l'Intention (Sémantique) et l'Exécution (Protection).

#### 🧩 Couches Fonctionnelles
1. **L'Arbitre (Décision)** : `binary_sensor.vmc_haute_vitesse_requise`.
   - *Rôle* : Évalue la pollution Chimique (CO₂) et Hydrique (HR) en fonction du facteur d'opportunité ($\Delta$HA).
2. **L'Intention (Sémantique)** : `sensor.vmc_intention`.
   - *Rôle* : Traduit la décision en langage humain et identifie la cause racine (ex: "Humidité excessive – SDB Enfants").
3. **Le Chef d'Orchestre (Exécution)** : `automation.vmc_gestion_automatique_humidite`.
   - *Rôle* : Pilote le moteur en `mode: restart` avec une durée minimale de fonctionnement.

### 🧠 Logique de l'Air Utile ($\Delta$HA)
- **Priorité CO₂** : Si $CO_2 \ge 1000$ ppm, la haute vitesse est forcée quelle que soit l'humidité.
- **Opportunité Hydrique** : Si l'humidité est haute mais l'air extérieur est plus humide ($\Delta$HA < 0), la haute vitesse est inhibée pour éviter de charger le bâti en eau.

### ⚙️ Paramètres VMC
| Paramètre | Valeur | Rôle |
| :--- | :--- | :--- |
| Seuil HR ON | **70 %** | Déclenchement haute vitesse. |
| Seuil HR OFF | **65 %** | Fin de besoin humidité. |
| Seuil CO₂ ON | **1000 ppm** | Déclenchement haute vitesse. |
| Seuil CO₂ OFF | **800 ppm** | Fin de besoin CO₂. |
| Durée min Haute Vitesse | **Réglable (ex: 15 min)** | Protection moteur et assèchement conduits. |

---

## ⚡ 5. INFRASTRUCTURE & RÉSILIENCE CAPTEURS

### 🔋 Résilience Électrique
- **Cœur Système** (NAS, HA, Box) : Onduleur (UPS).
- **Terminaux** (Chaudière, Vitoconnect) : Batteries de secours dédiées.
- *Rôle* : Assurer la continuité de la gouvernance thermique et la protection des bases de données.

### 📡 Résilience des Capteurs
- **Redondance Physique** : Les points de mesure critiques sont doublés physiquement.
- **Sensor Fusion** : Les templates de sécurisation sélectionnent la meilleure valeur disponible ou conservent la dernière valeur connue (Persistence).
- **Météo** : Fusion entre station locale (priorité réactivité) et API Cloud (fallback).
