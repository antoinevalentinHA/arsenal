# Arsenal — Contrat normatif
## Logbook Home Assistant

| Champ | Valeur |
|---|---|
| **Version** | 2.1 |
| **Statut** | Normatif opposable |
| **Remplace** | v2.0 |
| **Contrat jumeau** | `contrat_system_log.md` v1.1 |

---

## Principe fondamental

> Le Logbook raconte l'histoire fonctionnelle du système, pas son implémentation.

Journal narratif destiné à l'humain. Expose des événements interprétables, jamais des états internes.

---

## Règle d'admission (ABC)

Une entrée est autorisée **si et seulement si** elle satisfait les trois conditions :

**A. Nature événementielle** — changement d'état stable ou action effective. Pas d'état transitoire, pas de précondition, pas de variable interne.

**B. Impact fonctionnel observable** — modifie au moins une dimension : confort, sécurité, énergie, comportement global.

**C. Unicité explicative** — information nouvelle, non redondante avec un état persistant existant.

---

## Typologie autorisée (fermée)

Quatre catégories. Toute autre catégorie est interdite.

1. **Décision système** — changement de mode, arbitrage, sélection de programme.
2. **Transition d'état stable** — début / fin d'épisode (ECS, aération, vacances…).
3. **Sécurité ou anomalie à impact fonctionnel** — alarme, perte/retour réseau perçue par l'utilisateur, recovery visible.
   **Seules les anomalies à impact fonctionnel observable sont admissibles dans le Logbook. Les anomalies techniques internes (timeout, retry, incohérence interne, écart de bridge…) relèvent exclusivement de `system_log`.**
4. **Action système explicite** — script critique, action corrective, redémarrage ciblé.
   **Une action système n'est admissible que si son effet est perceptible au niveau fonctionnel. Les actions techniques sans effet observable (redémarrage de bridge, restart de watchdog, réconciliation interne…) relèvent de `system_log`.**

---

## Principe de substitution

> Quand un besoin de traçabilité existe, l'état persistant prime.

Ordre strict de préférence :

1. `sensor` / `binary_sensor` / `input_*`
2. attribut diagnostique
3. `system_log.write`
4. `logbook.log` *(dernier recours absolu)*

`logbook.log` n'est légitime que si **aucun** des trois canaux supérieurs ne porte l'information.

---

## Responsabilité d'émission

> Un événement = un point d'émission désigné.
> L'émetteur est celui qui possède la vérité de l'événement.

| Événement | Émetteur désigné |
|---|---|
| Décision prise | Couche décisionnelle |
| Exécution confirmée | Script exécutant |
| Anomalie détectée | Watchdog concerné |

Désignation faite par domaine, à l'implémentation.

**Interdit :** émissions concurrentes sur un même événement, écriture depuis observers/sensors/helpers techniques, multiplication non désignée des points d'émission.

---

## Règle de fréquence

> La fréquence anormale d'un événement est un signal système, pas un motif de log.

Un événement répété au-delà du seuil de référence du domaine doit être traité comme anomalie ou défaut de conception.

**Exception :** catégorie Sécurité / anomalie à impact fonctionnel — la répétition est elle-même un signal à conserver.

---

## Qualité du message

Chaque entrée porte implicitement :

- **Quoi** — l'événement
- **Pourquoi** — la cause ou l'intention, **formulée en langage métier**
- **Contexte** — obligatoire si l'événement n'est pas auto-explicite

> Le « Pourquoi » doit rester métier. Il ne doit jamais exposer une entité, un capteur, un helper ou une mécanique interne.

**Interdit :** noms d'entités bruts, identifiants internes, jargon technique, dump d'états, citation d'un capteur ou d'un helper comme cause.

**Exigé :** langage métier, lisible sans connaissance du système, orienté action ou résultat.

| ❌ Interdit | ✓ Conforme |
|---|---|
| `input_boolean.chauffage_mode_eco turned on` | Mode Confort activé |
| `script.aeration_declenchement called` | Aération déclenchée |
| `Mode réduit activé suite à presence_famille_unifiee = off` | Mode Réduit activé — absence détectée |
| `ROUTAGE : aucune branche ne matche` | *(à exclure entièrement)* |

---

## Test Arsenal

Quatre tests indépendants. **Un seul échec → exclusion.**

1. **Nature** — événement réel, pas état interne ?
2. **Impact** — modifie un comportement observable ?
3. **Densité** — information non redondante ?
4. **Formulation** — langage métier, sans jargon ni entité brute ?

---

## Canal adapté

| Nature | Canal |
|---|---|
| État métier | `sensor` / `helper` |
| Debug technique | `system_log` / Logger |
| Anomalie technique interne | `system_log` |
| Anomalie à impact fonctionnel | Logbook |
| Donnée continue | Recorder |
| Alerte éphémère | Notification |
| Narration fonctionnelle | Logbook |

---

## Dérives interdites

- Logbook utilisé comme console de debug
- Log « au cas où »
- Log de boot, recover, réconciliation, purge
- Log dans une branche `default`
- Log d'incohérence interne
- Log d'anomalie technique sans impact fonctionnel observable
- Log d'action technique sans effet perceptible
- Multiplication des émetteurs sans désignation
- Exposition de la mécanique interne (entités, helpers, identifiants)
- Tolérance du bruit par inertie

---

## Décision rapide (annexe opérationnelle)

```
1. L'information existe-t-elle déjà comme état persistant lisible ?
   → OUI → INTERDIT (redondance)                          ✗ STOP
2. L'événement entre-t-il dans la typologie fermée (1-4) ?
   → NON → INTERDIT                                       ✗ STOP
3. L'effet est-il fonctionnellement observable ?
   → NON → INTERDIT (relève de system_log)                ✗ STOP
4. L'émetteur est-il le détenteur désigné de la vérité ?
   → NON → INTERDIT (mauvais point d'émission)            ✗ STOP
5. Accepterais-je de le voir chaque jour dans l'activité ?
   → NON → INTERDIT (fréquence anormale = anomalie)       ✗ STOP
                              AUTORISÉ                    ✓
```

---

## Principe final

> Le Logbook raconte.
> Le debug trace.
> L'état prouve.
