# 🧠 ARSENAL — ECS  
# Orchestration et wrappers non thermiques

Chemin : `/homeassistant/documentation_arsenal/ecs/03_orchestration_et_wrappers.md`  
Statut : **STRUCTURANT — OPPOSABLE**  
Périmètre : Orchestration ECS

---

## 1. Objet

Ce document encadre les scripts d’orchestration ECS
et les wrappers d’interface utilisateur.

Il garantit que ces scripts restent
strictement non thermiques.

---

## 2. Nature des scripts d’orchestration

Les scripts d’orchestration :

- séquencent des briques existantes
- attendent des événements réels
- coordonnent des interactions utilisateur
- encapsulent des parcours complexes

Ils ne disposent d’aucune autorité thermique.

---

## 3. Cas d’usage typiques

Exemples :

- vaisselle + bouclage
- boutons utilisateur
- scénarios composites
- enchaînements conditionnels

Ces cas restent soumis à la chaîne autorisée.

---

## 4. Contraintes fondamentales

Les scripts d’orchestration :

- ❌ ne calculent aucune consigne
- ❌ ne déclenchent pas directement la couche matérielle
- ❌ ne décident pas d’un cycle
- ❌ ne modifient aucun verrou

Ils doivent systématiquement déléguer.

---

## 5. Synchronisation événementielle

Les scripts d’orchestration :

- attendent des changements d’état réels
- consomment des événements
- utilisent des délais bornés

Ils n’utilisent jamais :

- de polling
- de boucles infinies
- de temporisations arbitraires

---

## 6. Observabilité

Tout script d’orchestration doit :

- exposer ses étapes
- journaliser ses transitions
- signaler ses échecs

Aucun parcours implicite n’est admis.

---

## 7. Anti-patterns

Sont interdits :

- orchestration décidant d’une chauffe
- wrapper écrivant une consigne
- scénario masquant un refus
- enchaînement non traçable

Toute dérive doit être éliminée.

---