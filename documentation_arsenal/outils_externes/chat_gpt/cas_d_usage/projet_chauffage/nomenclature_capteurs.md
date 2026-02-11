# ==========================================================
# 🧠 PROJET ARSENAL — NOMENCLATURE OFFICIELLE
# Capteurs Observabilité Thermique — Phase 1
# ==========================================================

---

## 🎯 Objet

Ce document définit la **nomenclature normative et définitive**
des capteurs d’observabilité thermique Phase 1 du projet Chauffage Arsenal.

Il formalise :

* les **noms canoniques des capteurs**
* leur **ordre lexical obligatoire**
* leur **vocabulaire autorisé**
* leur **cohérence UX** avec `nommage_entites.md`

Ce document est :

* **NORMATIF**
* opposable à toute implémentation YAML
* garant de stabilité long terme des entités

---

## 🧠 Principe fondamental

> Le nom d’un capteur décrit **un phénomène thermique réel**,
> pas une méthode de calcul, pas un algorithme, pas une intention.

Conséquences :

* aucun terme technique (`stats`, `derivative`, `triggered`, etc.)
* aucun terme d’implémentation (`local`, `proxy`, `calc`, etc.)
* aucun terme décisionnel (`seuil`, `autorisation`, `intention`)

Le nom est :

* lisible humainement
* stable dans le temps
* exploitable en recherche

---

## 🧱 Structure canonique des noms

Ordre strict des éléments :

<Grandeur> <Qualificatif thermique> <Contexte> <Zone>
Où :

* **Grandeur** : toujours en premier
* **Zone** : toujours en dernier
* tous les termes intermédiaires décrivent un **phénomène physique**

---

## 🌡️ Grandeurs autorisées

| Grandeur    | Usage                |
| ----------- | -------------------- |
| Température | valeurs absolues     |
| Durée       | phénomènes temporels |
| Vitesse     | pentes thermiques    |
| Amplitude   | oscillations         |
| Nombre      | comptages            |

Interdits :

* Δ
* delta
* T_
* notations mathématiques

La physique est exprimée **en français lisible**.

---

## 🔁 Vocabulaires thermiques autorisés

### Inertie & dynamique

| Terme         | Sens                  |
| ------------- | --------------------- |
| inertie       | latence thermique     |
| chute         | poursuite de baisse   |
| montée        | poursuite de hausse   |
| reprise       | redémarrage chauffage |
| arrêt         | arrêt chauffage       |
| stabilisation | fin dynamique         |

---

### Oscillation & cycles

| Terme       | Sens                 |
| ----------- | -------------------- |
| oscillation | variation cyclique   |
| cycle       | période complète     |
| overshoot   | dépassement inertiel |
| plancher    | minimum atteint      |

---

### Régimes

| Terme    | Usage           |
| -------- | --------------- |
| Présence | régimes confort |
| Absence  | régimes réduits |

---

## 🧩 FAMILLE A — Inertie post-reprise (Présence)

Zone de référence : **Chambres**

### Capteurs canoniques

| Rôle                         | Nom officiel                                |
| ---------------------------- | ------------------------------------------- |
| Température initiale reprise | Température reprise Présence Chambres       |
| Amplitude chute résiduelle   | Amplitude chute reprise Présence Chambres   |
| Durée chute post-reprise     | Durée chute reprise Présence Chambres       |
| Vitesse de remontée          | Vitesse reprise Présence Chambres           |

---

## 🧩 FAMILLE B — Inertie post-arrêt (Présence)

Zone de référence : **Chambres**

### Capteurs canoniques

| Rôle                        | Nom officiel                                  |
| --------------------------- | --------------------------------------------- |
| Température arrêt chauffage | Température arrêt Présence Chambres           |
| Overshoot inertiel          | Amplitude overshoot arrêt Présence Chambres   |
| Durée overshoot             | Durée overshoot arrêt Présence Chambres       |

---

## 🧩 FAMILLE C — Inertie en absence

Zone de référence : **Chambres**

### Capteurs canoniques

| Rôle                          | Nom officiel                            |
| ----------------------------- | --------------------------------------- |
| Température plancher atteinte | Température plancher Absence Chambres   |
| Vitesse perte thermique       | Vitesse perte Absence Chambres          |
| Durée stabilisation           | Durée stabilisation Absence Chambres    |

---

## 🔄 FAMILLE D — Dynamique globale des cycles (Phase 1)

Zone de référence : **Chambres**

### Capteurs canoniques

| Rôle                              | Nom officiel                               |
| --------------------------------- | ------------------------------------------ |
| Amplitude oscillation cycle       | Amplitude oscillation cycle Présence Chambres |
| Fréquence journalière des cycles  | Nombre cycles jour Présence Chambres       |
| Période moyenne des cycles        | Durée cycle moyenne Présence Chambres      |

---

## 🔗 Correspondance entités YAML ↔ Noms officiels

### Présence

| Entité YAML                                             | Nom officiel                                    |
| ------------------------------------------------------- | ----------------------------------------------- |
| sensor.amplitude_chute_reprise_presence_chambres       | Amplitude chute reprise Présence Chambres       |
| sensor.duree_chute_reprise_presence_chambres           | Durée chute reprise Présence Chambres           |
| sensor.amplitude_overshoot_arret_presence_chambres     | Amplitude overshoot arrêt Présence Chambres     |
| sensor.duree_overshoot_arret_presence_chambres         | Durée overshoot arrêt Présence Chambres         |
| sensor.vitesse_reprise_presence_chambres               | Vitesse reprise Présence Chambres               |
| sensor.vitesse_refroidissement_presence_chambres       | Vitesse refroidissement Présence Chambres       |
| sensor.amplitude_oscillation_cycle_presence_chambres   | Amplitude oscillation cycle Présence Chambres   |

---

### Absence

| Entité YAML                                      | Nom officiel                          |
| ----------------------------------------------- | ------------------------------------- |
| sensor.temperature_plancher_absence_chambres    | Température plancher Absence Chambres |
| sensor.duree_stabilisation_absence_chambres     | Durée stabilisation Absence Chambres  |

---

### Cycles / stabilité

| Entité YAML                                   | Nom officiel                                |
| -------------------------------------------- | ------------------------------------------- |
| sensor.amplitude_oscillation_cycle_presence_chambres | Amplitude oscillation cycle Présence Chambres |
| sensor.nombre_cycles_jour_presence_chambres  | Nombre cycles jour Présence Chambres        |
| sensor.duree_cycle_moyenne_presence_chambres | Durée cycle moyenne Présence Chambres       |

---

## 🧠 Règles UX de recherche

Recherche typique utilisateur :

* "température reprise" → toutes reprises
* "durée stabilisation" → toutes stabilisations
* "oscillation" → toutes oscillations

Garanties :

* aucun bruit technique
* aucune collision sémantique
* regroupement naturel par phénomène

---

## 🔒 Invariants absolus

Il est strictement interdit :

* d’introduire un terme d’implémentation
* d’introduire un terme décisionnel
* d’utiliser une notation mathématique
* d’abréger un phénomène
* de déplacer la zone hors dernière position

Tout capteur non conforme :

* est renommé avant intégration
* n’est jamais exposé en UI

---

## 🧠 Statut architectural

* Domaine : Chauffage / Observabilité
* Phase : 1
* Autorité : Diagnostic pur
* Impact système : nul
* Pérennité : long terme

---

## 📌 Finalité

Cette nomenclature garantit :

* cohérence UI parfaite
* recherche instantanée
* stabilité inter-versions
* lisibilité scientifique

Elle constitue le **référentiel unique de nommage Phase 1**.

---

## 🏷️ Statut

* Document projet Chauffage Arsenal
* Normatif et fondateur
* Applicabilité Phase 1 uniquement
* Toute création future doit s’y conformer
