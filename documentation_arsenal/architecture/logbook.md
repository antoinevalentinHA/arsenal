# Arsenal — Contrat Logbook Home Assistant

**Nature :** contrat architectural opposable
**Portée :** globale
**Auditabilité :** binaire (conforme / non conforme)
**Évolution :** contrôlée, justifiée, documentée

---

## Principe fondamental

> Le Logbook raconte l'histoire du système, pas son implémentation.

Le Logbook est un journal narratif fonctionnel, destiné à l'humain.
Il expose des événements interprétables — jamais des états internes.

---

## Règle de base (opposable)

Une entrée Logbook est autorisée si et seulement si elle respecte les trois conditions suivantes.

### A. Nature événementielle

L'entrée correspond à un changement d'état stable ou à une action effective.

Sont exclus : états transitoires, préconditions, variables internes.

### B. Impact fonctionnel observable

L'événement modifie au moins une de ces dimensions :

- confort (température, humidité, éclairage…)
- sécurité
- consommation énergétique
- comportement global du système

Un événement sans effet observable sur au moins une de ces dimensions est interdit, même s'il correspond à une action interne réelle.

### C. Unicité explicative

L'événement apporte une information nouvelle, non redondante.

Sont exclus : doublons, confirmations implicites, répétitions sans changement de contexte.

---

## Typologie autorisée (fermée)

Seules les catégories suivantes sont autorisées. Toute autre catégorie est interdite.

### 1. Décision système
Changement de programme, sélection de mode, arbitrage central.

### 2. Transition d'état stable
Début / fin d'un épisode (aération, ECS…), changement de régime durable.

### 3. Événement de sécurité ou anomalie
Alarme, perte / retour réseau, watchdog, recovery.

### 4. Action système explicite
Script critique, action corrective, redémarrage ciblé.

---

## Règle de fréquence

> La fréquence anormale d'un événement est un signal système, pas un motif de log.

Un même type d'événement répété au-delà d'un seuil de référence doit être traité comme une anomalie ou un défaut de conception — et non comme un comportement à enregistrer.

Des valeurs de référence peuvent être définies par domaine lors de l'implémentation.

**Exception :** les événements de catégorie Sécurité / Anomalie sont exclus de cette contrainte. Leur répétition est elle-même un signal à conserver.

---

## Responsabilité d'émission

> Un événement = un point d'émission désigné.

> L'émetteur est celui qui possède la vérité de l'événement.

Exemples de désignation :

| Événement | Émetteur désigné |
|---|---|
| Décision prise | Couche décisionnelle |
| Exécution confirmée | Script exécutant |
| Anomalie détectée | Watchdog concerné |

La désignation est faite au moment de l'implémentation, par domaine.

**Interdictions :**

- émissions concurrentes sur un même événement
- écriture depuis des observers, sensors ou helpers techniques
- multiplication des points d'émission sans désignation explicite

---

## Structure d'une entrée (norme forte)

Chaque entrée doit contenir implicitement :

- **Quoi** — l'événement
- **Pourquoi** — la cause ou l'intention
- **Contexte** — obligatoire dès lors que l'événement n'est pas auto-explicite

---

## Règle de formulation

Interdictions strictes :

- noms d'entités bruts (`input_boolean.xxx`, `sensor.xxx`, etc.)
- jargon technique
- identifiants internes

Exigences :

- langage métier
- lisible immédiatement sans connaissance du système
- orienté action ou résultat

| ❌ Interdit | ✔ Conforme |
|---|---|
| `input_boolean.chauffage_mode_eco turned on` | Mode éco activé |
| `script.aeration_declenchement called` | Aération déclenchée |

---

## Test Arsenal (complet — 4 tests)

Toute entrée candidate doit passer les quatre tests suivants.

**Test 1 — Nature**
> Est-ce un événement réel, et non un état interne ou transitoire ?

**Test 2 — Impact**
> Modifie-t-il un comportement fonctionnellement observable ?

**Test 3 — Densité**
> Apporte-t-il une information non redondante ?

**Test 4 — Formulation**
> Le message est-il rédigé en langage fonctionnel, sans jargon ni nom d'entité brut ?

**Si un seul test échoue → EXCLUSION.**

---

## Règle de densité

> Une timeline dense est un défaut système.

Objectif : lecture rapide, compréhension immédiate, absence de bruit.

**1 événement = 1 information utile.**

---

## Relations système

| | Logbook | Logger |
|---|---|---|
| Mode | Narratif | Technique |
| Volume | Rare | Verbeux |
| Destinataire | Humain | Machine |

| | Logbook | Recorder |
|---|---|---|
| Granularité | Discret | Continu |
| Unité | Événement | Donnée |
| Finalité | Explication | Observation |

| | Logbook | Notification |
|---|---|---|
| Nature | Mémoire | Alerte |
| Durée | Persistant | Éphémère |

---

## Dérives interdites

- Logger "au cas où"
- Logger pour debug
- Multiplier les points d'émission sans désignation
- Exposer la mécanique interne
- Tolérer le bruit par inertie

> Arsenal fait l'inverse : on sélectionne avant d'émettre.

---

## Règle d'or

> Si une entrée n'explique rien, elle est interdite.
