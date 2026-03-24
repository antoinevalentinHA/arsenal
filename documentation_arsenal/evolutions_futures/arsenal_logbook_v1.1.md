# 🧠 Arsenal — Contrat normatif
## Logbook Home Assistant

| Champ | Valeur |
|---|---|
| **Version** | 1.1 |
| **Statut** | Normatif opposable |

---

## 🎯 Finalité

Ce contrat définit ce qui peut, ou non, apparaître dans le Logbook Home Assistant.

Il garantit :

- une activité lisible par l'humain
- l'absence de bruit technique
- la séparation stricte entre narration métier et debug interne
- la cohérence avec le principe Arsenal : l'état fait foi, le log ne remplace pas la vérité

---

## 🧱 Principe fondamental

> Le Logbook raconte l'histoire fonctionnelle du système, pas son implémentation.

---

## ⚡ Décision rapide (10 secondes)

```
1. L'information existe-t-elle déjà comme état persistant lisible ?
   → OUI → INTERDIT (redondance)                              ✗ STOP

2. L'événement a-t-il un sens pour un humain non technique ?
   → NON → INTERDIT                                           ✗ STOP

3. Modifie-t-il réellement l'état fonctionnel du système ?
   → NON → INTERDIT                                           ✗ STOP

4. Accepterais-je de le voir chaque jour dans l'activité ?
   → NON → INTERDIT                                           ✗ STOP

                              AUTORISÉ                        ✓
```

---

## ✅ Entrées autorisées

### 1. Événements métier stables

- passage en mode Confort / Réduit
- cycle ECS lancé
- alarme armée / désarmée
- début ou fin d'un blocage métier

### 2. Actions effectives observables

- chauffage réellement rétabli
- blocage chauffage activé
- désinfection ECS déclenchée

### 3. Échecs réels à impact fonctionnel

- consigne ECS rejetée
- timeout de confirmation bridge
- commande non appliquée

---

## ❌ Entrées interdites

### Debug interne
- branche default, incohérence, validation, guard

### Mécanique de pipeline
- pipeline armé / désarmé, recover, purge zombie, réconciliation

### Boot technique
- réapplication au démarrage, resynchronisation locale, restauration technique

### Redondance
- toute information déjà visible dans un `sensor` / `helper`

---

## 🔁 Principe de substitution

> Quand un besoin de traçabilité existe, la priorité est donnée à un état persistant.

Ordre strict :

1. `sensor` / `binary_sensor` / `input_*`
2. attribut diagnostique
3. `system_log.write`
4. `logbook.log` *(dernier recours)*

---

## 🎯 Cas légitimes de `logbook.log`

> Voir Principe de substitution (section précédente).

`logbook.log` est autorisé uniquement si les trois conditions suivantes sont réunies :

- aucun état persistant ne porte l'information
- l'événement est métier et lisible
- l'événement est rare et utile à relire

---

## 🚫 Anti-patterns

- Logbook utilisé comme console de debug
- Log dans une branche `default`
- Log de boot
- Log de `recover`
- Log d'incohérence interne
- Log pour "se rassurer"

---

## 🧠 Règle de rareté

> Une entrée fréquente est présumée illégitime.

Toute entrée susceptible d'apparaître plusieurs fois par jour doit être justifiée explicitement.

---

## 🏷️ Qualité des messages

| | Exemple |
|---|---|
| ✅ Autorisé | `Passage en mode Confort` |
| ✅ Autorisé | `Cycle ECS lancé` |
| ✅ Autorisé | `Consigne ECS rejetée` |
| ❌ Interdit | `ROUTAGE : aucune branche ne matche` |
| ❌ Interdit | `trigger_id=...` |
| ❌ Interdit | dump d'états bruts |

---

## 🔄 Canal adapté

| Nature | Canal |
|---|---|
| État métier | `sensor` / `helper` |
| Debug | `system_log` |
| Anomalie | `system_log` / compteur |
| Narration fonctionnelle | Logbook |

---

## 🔥 Règle radicale

> Si un message révèle le code, il est interdit.

---

## 🧠 Principe final

> Le Logbook raconte.  
> Le debug trace.  
> L'état prouve.
