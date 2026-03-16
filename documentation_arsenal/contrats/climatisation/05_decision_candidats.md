# CONTRAT ARSENAL — CLIMATISATION
## 05 — Décision — Production des candidats

**Version contrat :** v1.2

---

## Principe

Cette section définit, pour chaque mode climatique, les conditions de **besoin (requis)** et d'**applicabilité (applicable)**.

- `requis` exprime un besoin thermique ou hygrométrique constaté.
- `applicable` exprime uniquement la possibilité locale d'exécuter un mode. Il ne constitue jamais une priorité ni une sélection.

Elle ne contient :
- aucune priorité inter-mode,
- aucun choix final,
- aucune notion de sélection.

Chaque mode est évalué de manière indépendante.  
La couche Décision peut produire plusieurs candidats requis et applicables simultanément.  
La sélection du mode cible relève exclusivement de la couche d'Arbitrage (`06_arbitrage_politique.md`).

---

## COOL

**Requis si :**
- la température intérieure (chambre la plus chaude) est supérieure ou égale au seuil d'allumage COOL.

**Applicable si :**
- la température extérieure est compatible avec le refroidissement,
- les fenêtres sont fermées,
- l'aération n'est pas favorable,
- aucun blocage horaire n'est actif,
- COOL n'est pas inhibé par une absence prolongée.

---

## DRY

**Requis si :**
- l'humidex intérieur dépasse le seuil de déclenchement DRY.

**Applicable si :**
- une présence est détectée ou le mode babysitting est actif,
- les fenêtres sont fermées,
- l'aération n'est pas favorable,
- aucun blocage horaire n'est actif.

---

## HEAT — Chauffage d'appoint

**Requis si :**
- la température intérieure est inférieure au seuil d'allumage HEAT.

**Applicable si :**
- une présence réelle est détectée,
- le chauffage par climatisation est explicitement autorisé,
- la température extérieure est suffisante,
- le poêle n'est pas actif,
- les fenêtres sont fermées,
- aucun blocage horaire n'est actif.

**Note :** Le mode HEAT est strictement un chauffage d'appoint. Il ne constitue jamais une source de chauffage principale.

---

## OFF — État neutre (hors production des candidats)

Le mode OFF n'est ni requis ni applicable.  
Il n'est jamais produit comme candidat par la couche de Décision.

OFF n'est pas évalué dans cette section.

La sélection de OFF relève exclusivement de la politique d'arbitrage, lorsqu'aucun mode requis et applicable n'est sélectionnable.
