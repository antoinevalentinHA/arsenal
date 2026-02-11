# ⚠️ DOCUMENT HISTORIQUE — ARCHIVE

Ce document n’est plus normatif.

Il a été remplacé par le corpus :

/documentation_arsenal/ecs/

Toute référence opérationnelle doit se faire
exclusivement sur les documents actifs.

# 🧠 ARSENAL — CONTRAT SYSTÈME : ECS
Chemin : `/homeassistant/documentation_arsenal/contrats/ecs.md`  
Statut : **FONDATEUR — GELÉ**  
Périmètre : Eau Chaude Sanitaire (ECS)

---

## 1. Objet du contrat

Ce document définit le **contrat architectural et fonctionnel** du sous-système **ECS** (Eau Chaude Sanitaire) dans ARSENAL.

Il établit de manière **opposable** :

- les **autorités habilitées** à agir sur l’ECS
- la séparation stricte entre **planification**, **autorisation**, **exécution** et **sécurité**
- les **invariants thermiques et temporels**
- les mécanismes de **garde**, de **journalisation** et de **rattrapage**
- le comportement attendu en cas d’erreur, de redémarrage ou de défaillance partielle

Tout script, automation, capteur ou helper ECS **doit respecter ce contrat**.

---

## 2. Périmètre

### 2.1 Inclus (IN)

- Exécution d’un cycle thermique ECS :
  - ponctuel
  - vaisselle
  - désinfection
- Pilotage ViCare ECS :
  - consigne effective
  - prélèvement unique
- Gestion complète du cycle :
  - verrouillage
  - surveillance thermique réelle
  - timeouts et watchdogs
  - rabaissement post-cycle
- Bouclage ECS ponctuel (recirculation)
- Gardiens ECS actifs (permanents et événementiels)
- Journalisation complète des cycles ECS
- Mémoire persistante (timestamps, diagnostics, sauvegardes)

### 2.2 Exclus (OUT)

- Chauffage (radiateurs, courbes de chauffe)
- Climatisation
- Décision métier globale “faut-il chauffer maintenant”
- Arbitrages présence / absence / confort
- Toute chauffe ECS déclenchée sans passer par la chaîne autorisée

---

## 3. Principes ARSENAL appliqués à l’ECS

### 3.1 Helpers

Les helpers (`input_*`, `timer`) sont **passifs** :

- ❌ ne déclenchent rien
- ❌ ne pilotent rien
- ❌ ne décident rien

Ils servent exclusivement à :
- exprimer une **intention**
- stocker un **paramètre**
- mémoriser un **état ou un fait**

---

### 3.2 Capteurs

Les capteurs :

- exposent une **vérité calculée ou mesurée**
- servent au diagnostic et à la décision
- ❌ ne commandent jamais directement l’ECS

---

### 3.3 Scripts

Les scripts :

- exécutent une **demande explicite**
- orchestrent des briques existantes
- sont **déterministes et observables**
- n’inventent jamais une logique métier globale

---

### 3.4 Automatisations

Les automatisations :

- observent
- planifient
- journalisent
- déclenchent **uniquement** via la chaîne autorisée

Elles ne contiennent **aucune décision thermique**.

---

## 4. Autorités et hiérarchie ECS

### 4.1 Autorité thermique UNIQUE

#### `script.chauffage_ecs_cycle`  
**Rôle : Orchestrateur unique du cycle ECS**

Responsabilités couvertes :
- verrouillage exclusif ECS
- calcul et application de la consigne effective
- déclenchement du prélèvement unique
- surveillance thermique réelle
- gestion des timeouts et watchdogs
- rabaissement post-chauffe
- libération contrôlée du verrou

Garanties :
- un seul cycle ECS à la fois
- aucun cycle infini
- aucun succès supposé
- décisions basées uniquement sur des mesures réelles

❌ Ce script ne planifie pas  
❌ Ce script ne décide pas “s’il faut chauffer”

---

### 4.2 Scripts de garde (autorisation préalable)

Exemple :  
`script.ecs_vaisselle_lancer_si_ok`

Rôle :
- autoriser ou refuser l’appel au moteur ECS
- contrôles locaux uniquement :
  - mode actif
  - absence de cycle en cours
  - délais minimaux respectés

❌ ne pilote pas ViCare  
❌ ne modifie aucune consigne

---

### 4.3 Scripts d’orchestration

Exemples :
- vaisselle + bouclage
- wrappers bouton utilisateur

Rôle :
- séquencer des briques existantes
- attendre des événements réels
- rester totalement non thermiques

---

### 4.4 Bouclage ECS

Le bouclage ECS est un **confort ponctuel ou programmé**, jamais une logique thermique.

Il existe désormais **deux formes strictement distinctes**, hiérarchisées et gouvernées :

---

#### 4.4.1 Bouclage ponctuel (manuel temporisé)

- déclenché explicitement par action utilisateur ou script  
- borné par un **timer dédié**  
- arrêté automatiquement **sous condition de souveraineté**  
- indépendant des cycles ECS  
- totalement hors planification hebdomadaire  

Règles :

- ❌ ne déclenche jamais de chauffe ECS  
- ❌ ne modifie aucune consigne  
- ❌ ne dépend d’aucune présence  
- ❌ n’interrompt jamais un bouclage automatique actif  
- ✅ toujours borné temporellement  
- ✅ auto-arrêté **uniquement si aucune plage automatique n’est active**  
- ✅ idempotent en superposition de contextes  

Gouvernance spécifique :

- l’arrêt par fin de timer est **autorisé uniquement si** :
  - `input_boolean.bouclage_plage_active == off`
- si une plage automatique est active :
  - l’événement `timer.finished` est **ignoré**
  - aucune action d’arrêt n’est exécutée  
  - aucune concurrence inter-contexte n’est possible  

Invariants :

- priorité absolue : **AUTOMATIQUE > MANUEL**  
- un cycle manuel :
  - ❌ ne peut jamais interrompre un cycle automatique  
  - ❌ ne peut jamais révoquer une autorité de plage  
  - ✅ reste un confort strictement subordonné  

---

#### 4.4.2 Bouclage automatique programmé

Un sous-système de **recirculation programmée conditionnée**, conforme aux doctrines :

- `gestion_du_temps.md`  
- `présence maison`  
- séparation décision / application ECS  

Caractéristiques architecturales :

- autorisation portée par un **binary_sensor logique durable** :
  - `binary_sensor.bouclage_autorise`
- le temps est **encapsulé**, jamais consommé directement par une automation  
- la présence est consommée comme **signal de contexte**, jamais comme décision  

Conditions d’autorisation cumulatives :

- jour ∈ lundi → vendredi  
- heure courante ∈ [début ; fin]  
- `binary_sensor.presence_famille_unifiee == on`  
- invariant : **début < fin** (plages chevauchant minuit interdites)  

Objets structurants :

- `input_boolean.bouclage_plage_active`  
  → autorisation utilisateur globale et **autorité AUTO souveraine**  
- `input_datetime.heure_debut_bouclage_ecs`  
- `input_datetime.heure_fin_bouclage_ecs`  
  → paramétrage horaire (heure seule)  
- `binary_sensor.bouclage_autorise`  
  → vérité logique unique d’autorisation  

Automation d’application associée :

- `10260000000001` — *Bouclage automatique programmé*  
- pilotage unique de `switch.prise_bouclage`  
- déclenchement uniquement par :
  - changement de `binary_sensor.bouclage_autorise`  
  - changement de `input_boolean.bouclage_plage_active`  
  - passage de `input_boolean.systeme_stable` à `on`  

Garde-fous structurels :

- ❌ aucun polling temporel  
- ❌ aucune consommation directe de `now()` dans l’automation  
- ❌ aucune décision métier thermique  
- ❌ aucune écriture dans un capteur de présence  
- ❌ aucune dépendance à un timer manuel  
- ✅ blocage si entités `unknown` / `unavailable`  
- ✅ `mode: restart` pour neutraliser les rafales au reload  
- ✅ re-synchronisation post-démarrage via `systeme_stable`  

Notifications :

- une **notification persistante d’état uniquement** :
  - créée lorsque le bouclage est effectivement actif  
  - supprimée automatiquement à l’arrêt  
  - aucune notification événementielle  
  - aucun historique métier associé  

Invariants globaux :

- le bouclage ECS, quelle que soit sa forme :
  - ❌ ne déclenche jamais de cycle ECS  
  - ❌ ne modifie aucune consigne  
  - ❌ n’interagit jamais avec les verrous ECS  
  - ❌ ne perturbe jamais une autorité supérieure  
  - ✅ reste un sous-système de confort strictement non thermique  
  - ✅ respecte la souveraineté : **AUTOMATIQUE > MANUEL**  
  - ✅ garantit l’idempotence en superposition de contextes

---

## 5. États, verrous et mémoire

### 5.1 États runtime

- `input_boolean.ecs_cycle_en_cours`  
  Verrou logique de cycle ECS
- `input_boolean.bouclage_ecs_5_minutes_en_cours`  
  État du bouclage ponctuel

---

### 5.2 Autorisations / blocages

- `ecs_blocage_planifiee`
- `ecs_desinfection_active`
- `bouclage_visiteur`
- `ecs_autocorrect_active`

Ces états **autorisent ou interdisent**, mais ne déclenchent jamais.

---

### 5.3 Modes utilisateur

- `mode_vaisselle`
- `mode_enfants`

Les modes :
- modifient un **contexte**
- reconfigurent un planning
- ❌ ne déclenchent jamais directement une chauffe

---

### 5.4 Planification

- jours actifs ECS (matin / soir)
- heures ECS hebdomadaires
- jour et heure de désinfection

La planification définit **quand c’est autorisé**, jamais quand ça chauffe.

---

### 5.5 Mémoire temporelle (vérités persistantes)

- `input_datetime.ecs_dernier_cycle`  
  Horodatage du dernier cycle effectif
- `input_datetime.ecs_pic_thermique`  
  Horodatage du pic thermique réel (Tmax)

Ces valeurs :
- sont écrites automatiquement
- ne doivent **jamais** être modifiées manuellement

---

### 5.6 Diagnostics figés

- durée réelle du cycle
- température maximale atteinte
- résumés textuels figés
- sauvegardes JSON (planning / réglages)

👉 Les dashboards et analyses **ne consomment que des données figées**.

---

## 6. Timers ECS

### 6.1 Timers de stabilisation (restore: false)

- post-prélèvement
- attente vérification post-action

Rôle :
- suspendre temporairement les diagnostics
- éviter toute conclusion prématurée

---

### 6.2 Watchdog de cycle (restore: true)

- durée maximale absolue
- un cycle ECS ne peut jamais survivre à son watchdog

Expiration = **événement de sécurité critique**.

---

### 6.3 Timer bouclage ECS

- borne strictement la durée du bouclage
- garantit l’auto-arrêt même après reboot

---

## 7. Gardiens ECS (sécurité active)

### 7.1 Gardien permanent hors cycle

- garantit la consigne ECS à **10 °C** hors cycle
- correction silencieuse et idempotente
- indépendant du cloud

---

### 7.2 Gardien post-prélèvement

- réapplication vérifiée de la consigne basse
- double tentative
- fallback matériel + alerte

---

### 7.3 Gardien post-cycle

- vérification différée du retour à 10 °C
- tolérant aux ratés ViCare
- jamais actif pendant un cycle

---

### 7.4 Watchdog terminal

- rabaissement forcé
- libération unilatérale du verrou
- dernier rempart de sûreté

---

## 8. Journalisation ECS

Un cycle ECS est documenté par :

1. journalisation du **début de cycle**
2. capture du **pic thermique réel**
3. consolidation **post-stabilisation** de fin de cycle

Règle :
> Un cycle ECS n’existe que s’il est traçable du début au gel final.

---

## 9. Invariants absolus (non négociables)

- ❌ Aucun cycle ECS hors script autoritaire
- ❌ Aucune consigne haute hors cycle
- ❌ Aucun cycle ECS infini
- ❌ Aucun état dangereux silencieux
- ❌ Aucun déclenchement direct depuis une automation
- ✅ Consigne 10 °C = état nominal hors cycle
- ✅ Toute action ECS est traçable
- ✅ Toute dérive est corrigée ou signalée

---

## 10. Défaillances tolérées

Le système ECS reste sûr en cas de :
- redémarrage Home Assistant
- latence ou indisponibilité ViCare
- désynchronisation cloud
- reboot en cours de cycle

La sécurité locale **prime toujours**.

---

## 11. Interdictions explicites

Il est interdit :

- de déclencher une chauffe ECS sans passer par la chaîne autorisée
- de laisser une consigne haute hors cycle
- de libérer un verrou ECS sans rabaissement
- d’utiliser une donnée dynamique comme vérité finale
- d’implémenter une logique thermique dans une automation

---

## 12. Statut du contrat

Ce contrat ECS est :

- **fondateur**
- **gelé**
- **opposable**
- référence unique pour toute évolution future

Toute modification doit :
- être justifiée
- être documentée
- faire l’objet d’une révision explicite de ce contrat.

---
