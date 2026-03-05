# ARSENAL — CONTRAT NORMATIF
## Ouvertures Zigbee — Capteurs réconciliés (redondance asymétrique)

---

**Statut :** ADOPTÉ  
**Version :** 1.1  
**Domaine :** Zigbee / Ouvertures / Aération / Chauffage / Sécurité thermique  
**Remplace :** v1.0 (contradictions R2/R3, gestion unknown révisée)  
**Changelog v1.1 :**
- Algorithme de réconciliation restructuré en forme normale (divergence précondition)
- Remplacement du principe "unknown → unknown" par disqualification de source
- Source canonique qualifiée N1
- Table de vérité complète mise à jour

---

## 1. Contexte et hypothèses terrain

### 1.1 Architecture matérielle

Pour chaque ouvrant critique, deux capteurs Zigbee sont déployés en redondance :

- **capteur_A** : Aqara (capteur historique)
- **capteur_B** : Sonoff (capteur redondant, déployé en complément)

États possibles de chaque capteur :

| État | Signification | Exploitable |
|------|---------------|-------------|
| `on` | Ouvrant détecté ouvert | ✅ oui |
| `off` | Ouvrant détecté fermé | ✅ oui |
| `unknown` | État indéterminé | ❌ non — source disqualifiée |
| `unavailable` | Capteur non joignable | ❌ non — source disqualifiée |

### 1.2 Hypothèses opérationnelles validées terrain

Ces hypothèses sont le fondement du contrat. Elles doivent être réévaluées si le contexte matériel change.

**H1 — Ouverture non ratée**
Les événements d'ouverture sont détectés de façon fiable par au moins un capteur. Aucun ouvrant réellement ouvert n'a été déclaré fermé en pratique.

**H2 — Fermeture parfois ratée (Aqara)**
Les Aqara peuvent manquer des événements de fermeture et rester bloqués à l'état `on` alors que l'ouvrant est physiquement fermé. Ce scénario "zombie ouverture" a été observé en production et constitue le **risque dominant**.

**H3 — Sonoff plus fiable**
Les Sonoff présentent une meilleure fiabilité globale, en particulier sur la détection de fermeture. Cette hypothèse est en cours de confirmation terrain.

**H4 — Scénario dominant de divergence**
En cas de divergence `capteur_A=on / capteur_B=off`, l'interprétation retenue est : **Aqara zombie, Sonoff fiable**. Le `off` l'emporte.

---

## 2. Objet du capteur réconcilié

Un **capteur réconcilié** est une entité binaire métier représentant :

> « L'état d'ouverture d'un ouvrant critique, consolidé à partir de deux sources physiques, selon une logique asymétrique adaptée au risque dominant identifié terrain. »

Il est la **source canonique N1** — seule source autorisée pour toute logique métier (chauffage, sécurité, alertes, métriques). Aucune logique ne consomme directement les sources brutes lorsqu'un capteur réconcilié existe.

---

## 3. Principe de disqualification

Un capteur dans un état non exploitable (`unknown` ou `unavailable`) est **disqualifié** : il est exclu du calcul de réconciliation.

La réconciliation s'opère sur l'ensemble des sources restantes exploitables.

```
Sources exploitables = {A, B} ∩ {on, off}
```

Ce principe évite tout raisonnement sur une absence de signal et garantit qu'un état `off` ne peut jamais résulter d'une source muette.

---

## 4. Algorithme de réconciliation (forme normale)

Les règles s'appliquent dans l'ordre strict suivant. La première règle satisfaite s'applique, les suivantes sont ignorées.

```
R1 — Aucune source exploitable
     si Sources exploitables = ∅
     → state = unknown, degrade = true

R2 — Une seule source exploitable (disqualification partielle)
     si Sources exploitables = {X} (une seule)
     → state = X, degrade = true

R3 — Deux sources, divergence
     si Sources exploitables = {A, B} et A ≠ B
     → state = off, divergence = true

R4 — Deux sources, consensus
     si Sources exploitables = {A, B} et A = B
     → state = A
```

**Note sur R3 :** La divergence est résolue en faveur de `off`. Justification H4 : le scénario dominant est un Aqara bloqué `on` après fermeture réelle. Un `off` isolé est plus fiable qu'un `on` isolé persistant.

**Note sur R1 :** C'est le seul cas produisant `unknown`. Il est inévitable : sans aucune source, aucune décision n'est possible.

---

## 5. Observabilité obligatoire

Le capteur réconcilié expose systématiquement :

| Attribut | Type | Description |
|----------|------|-------------|
| `state` | `on / off / unknown` | État réconcilié (source canonique N1) |
| `etat_A` | `on / off / unknown / unavailable` | État brut capteur A |
| `etat_B` | `on / off / unknown / unavailable` | État brut capteur B |
| `divergence` | `true / false` | A et B exploitables mais différents |
| `degrade` | `true / false` | Au moins une source disqualifiée |

La divergence et la dégradation doivent déclencher une **alerte observable** (log, notification, tableau de bord). Il ne suffit pas de les stocker silencieusement.

---

## 6. Table de vérité normative complète

### Cas nominaux — deux sources exploitables

| capteur_A | capteur_B | réconcilié | divergence | degrade | Règle |
|-----------|-----------|------------|------------|---------|-------|
| off | off | **off** | false | false | R4 |
| on | on | **on** | false | false | R4 |
| on | off | **off** | true | false | R3 |
| off | on | **off** | true | false | R3 |

### Cas dégradés — une source disqualifiée

| capteur_A | capteur_B | réconcilié | divergence | degrade | Règle |
|-----------|-----------|------------|------------|---------|-------|
| off | unknown/unavailable | **off** | false | true | R2 |
| on | unknown/unavailable | **on** | false | true | R2 |
| unknown/unavailable | off | **off** | false | true | R2 |
| unknown/unavailable | on | **on** | false | true | R2 |

### Cas dégradé total — deux sources disqualifiées

| capteur_A | capteur_B | réconcilié | divergence | degrade | Règle |
|-----------|-----------|------------|------------|---------|-------|
| unknown/unavailable | unknown/unavailable | **unknown** | false | true | R1 |

---

## 7. Interdictions absolues

**I1 — Interdiction de consommation directe des sources**
Toute logique métier critique est interdite de consommer directement `capteur_A` ou `capteur_B` lorsqu'un capteur réconcilié existe.

**I2 — Interdiction de fermeture sur source disqualifiée**
Il est interdit de déclarer `off` si la seule source disponible est `unknown` ou `unavailable`.

**I3 — Interdiction de masquer la divergence**
La divergence `true` doit être exposée et observable. Elle ne peut pas être ignorée ou écrasée silencieusement.

**I4 — Interdiction de fermeture par timeout**
Un timeout arbitraire ne peut pas produire un état `off`. Seul un signal `off` explicite d'une source exploitable peut clôturer.

---

## 8. Limites reconnues et risques acceptés

### 8.1 Risque : faux fermé sur divergence (Sonoff défaillant)

**Scénario :** capteur_B (Sonoff) se bloque `off` à tort alors que l'ouvrant est réellement ouvert et capteur_A (Aqara) dit `on`.

**Conséquence :** R3 déclare `off`, masquant une ouverture réelle.

**Mitigation actuelle :**
- `divergence=true` est exposée → investigation possible
- L'hypothèse H3 (Sonoff fiable) borne la probabilité de ce scénario
- Ce scénario est l'inverse du risque dominant (H2) et n'a pas été observé terrain

**Mitigation future envisagée :** debounce temporel sur R3 — ne clôturer en divergence que si le `off` persiste depuis N secondes. À activer si des faux fermés sont observés terrain, sans modifier les règles centrales.

### 8.2 Réévaluation des hypothèses

Ce contrat repose sur H1–H4. Déclencheurs de révision :

| Événement terrain | Hypothèse remise en cause | Action |
|-------------------|--------------------------|--------|
| Ouverture manquée par les deux capteurs | H1 | Révision R4 (consensus) |
| Sonoff rate des fermetures | H3, H4 | Révision R3 (divergence) |
| Double blocage ON observé | H2 | Architecture watchdog (HYPOTHÈSE B) |

---

## 9. Critères d'acceptation

Le contrat est respecté si et seulement si :

- Une ouverture est détectée dès qu'au moins une source exploitable passe `on`
- Une fermeture est déclarée dès qu'au moins une source exploitable passe `off`
- Aucune source disqualifiée ne peut produire un état `off`
- `unknown` n'est produit que si les deux sources sont simultanément disqualifiées
- La divergence est exposée et observable dès que A ≠ B (toutes deux exploitables)
- La dégradation est exposée et observable dès qu'une source est disqualifiée
- Aucune logique métier ne consomme directement les sources brutes

---

## 10. Évolutions futures prévues

| Évolution | Déclencheur | Impact contrat |
|-----------|-------------|----------------|
| Debounce sur R3 | Faux fermés observés terrain | Amendement R3 uniquement |
| Pondération par fiabilité capteur | Données terrain Sonoff accumulées | Nouveau contrat v2 |
| Watchdog physique (HYPOTHÈSE B) | Double blocage ON observé | Architecture complémentaire |

---

*Fin du contrat — ARSENAL v1.1*
