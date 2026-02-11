# 🧠 ARSENAL — ECS  
# Bouclage ECS — Sous-système non thermique

Chemin : `/homeassistant/documentation_arsenal/ecs/04_bouclage_ecs_sous_systeme.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Recirculation ECS

---

## 1. Objet

Ce document définit le sous-système de bouclage ECS.

Le bouclage est un mécanisme de confort,
totalement indépendant de la régulation thermique.

Il ne constitue jamais une décision de chauffe.

---

## 2. Doctrine générale

Le bouclage ECS est gouverné par les principes suivants :

- séparation stricte du thermique
- priorité absolue : AUTOMATIQUE > MANUEL
- temps encapsulé
- autorité explicite
- idempotence multi-contexte

Toute implémentation doit respecter ces règles.

---

## 3. Formes de bouclage

Deux formes strictement distinctes sont autorisées.

---

### 3.1 Bouclage ponctuel manuel temporisé

#### Nature

- déclenché explicitement
- borné par un timer dédié
- hors planification
- indépendant des cycles ECS

---

#### Règles

- ❌ ne déclenche jamais de chauffe
- ❌ ne modifie aucune consigne
- ❌ ne dépend d’aucune présence
- ❌ n’interrompt aucun bouclage automatique

- ✅ borné temporellement
- ✅ subordonné à l’autorité automatique
- ✅ idempotent

---

#### Gouvernance d’arrêt

L’arrêt par timer est autorisé uniquement si :

 input_boolean.bouclage_plage_active == off

Si une plage automatique est active :

- l’événement `timer.finished` est ignoré
- aucune action d’arrêt n’est exécutée

---

#### Invariants

- priorité : AUTOMATIQUE > MANUEL
- aucun contournement possible
- aucune révocation d’autorité

---

### 3.2 Bouclage automatique programmé

#### Nature

Sous-système de recirculation conditionnée,
conforme aux doctrines temporelles et contextuelles.

---

#### Autorité logique

Portée par :

 binary_sensor.bouclage_autorise

Ce capteur constitue l’unique vérité d’autorisation.

---

#### Conditions cumulatives

- jour ∈ lundi → vendredi
- heure ∈ [début ; fin]
- binary_sensor.presence_famille_unifiee == on
- invariant : début < fin

---

#### Objets structurants

- input_boolean.bouclage_plage_active  
- input_datetime.heure_debut_bouclage_ecs  
- input_datetime.heure_fin_bouclage_ecs  
- binary_sensor.bouclage_autorise  

---

#### Automation d’application

- ID : 10260000000001  
- Nom : Bouclage automatique programmé  
- Pilotage exclusif : switch.prise_bouclage  

Déclencheurs autorisés :

- changement de binary_sensor.bouclage_autorise
- changement de input_boolean.bouclage_plage_active
- systeme_stable → on

---

#### Garde-fous

- ❌ aucun polling temporel
- ❌ aucune consommation directe de now()
- ❌ aucune décision métier
- ❌ aucune écriture dans présence

- ✅ blocage si entités unknown / unavailable
- ✅ mode: restart
- ✅ resynchronisation post-boot

---

#### Notifications

- notification persistante d’état uniquement
- création à l’activation réelle
- suppression à l’arrêt
- aucun événementiel

---

## 4. Invariants globaux du bouclage

Quel que soit le mode :

- ❌ ne déclenche jamais de cycle ECS
- ❌ ne modifie aucune consigne
- ❌ n’interagit avec aucun verrou
- ❌ ne perturbe aucune autorité

- ✅ reste non thermique
- ✅ respecte AUTOMATIQUE > MANUEL
- ✅ garantit l’idempotence

---