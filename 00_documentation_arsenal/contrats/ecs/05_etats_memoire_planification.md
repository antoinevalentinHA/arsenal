# 🧠 ARSENAL — ECS  
# États, mémoire et planification

Chemin : `/homeassistant/00_documentation_arsenal/ecs/05_etats_memoire_planification.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : États et mémoire ECS

---

## 1. Objet

Ce document définit les états runtime,
les mécanismes de mémoire persistante
et les règles de planification ECS.

Il garantit la stabilité décisionnelle
et l’intégrité historique.

---

## 2. États runtime

### 2.1 Verrou de cycle

 input_boolean.ecs_cycle_en_cours

Rôle :
Verrou logique exclusif de cycle ECS.

Invariants :

- un seul cycle simultané
- aucune libération anticipée
- aucun forçage manuel

---

### 2.2 État bouclage ponctuel

 input_boolean.bouclage_ecs_5_minutes_en_cours

Indique l’activation effective
du bouclage manuel temporisé.

---

## 3. Autorisations et blocages

Les états suivants autorisent ou interdisent,
sans jamais déclencher :

- ecs_blocage_planifiee
- ecs_desinfection_active
- bouclage_visiteur
- ecs_autocorrect_active

Ils ne constituent pas des ordres.

---

## 4. Modes utilisateur

Modes disponibles :

- mode_vaisselle
- mode_enfants

Les modes :

- modifient un contexte
- reconfigurent un planning
- ne déclenchent jamais directement

---

## 5. Planification

La planification ECS définit uniquement
les fenêtres d’autorisation.

Elle inclut :

- jours actifs matin / soir
- heures hebdomadaires
- jour et heure de désinfection

Règle absolue :

> La planification n’est jamais un ordre de chauffe.

---

## 6. Mémoire temporelle

### 6.1 Horodatages persistants

 input_datetime.ecs_dernier_cycle 
 input_datetime.ecs_pic_thermique

Ces valeurs :

- sont écrites automatiquement
- ne sont jamais modifiables manuellement
- constituent des faits opposables

---

## 7. Diagnostics figés

Les diagnostics incluent :

- durée réelle
- température maximale
- résumés textuels
- sauvegardes JSON

Ils sont :

- figés post-cycle
- immuables
- utilisés pour analyse uniquement

Aucune donnée dynamique
ne peut servir de vérité finale.

---

## 8. Anti-patterns

Sont interdits :

- écriture manuelle de mémoire
- recalcul rétroactif
- diagnostic temps réel
- historisation implicite

Toute violation est critique.

---