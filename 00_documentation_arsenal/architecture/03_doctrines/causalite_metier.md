# DOCTRINE ARSENAL — Causalité métier et temporalité persistante

**Référence :** `DOCTRINE_CAUSALITE.md`
**Version :** 1.0.2
**Introduced :** Arsenal v15.5
**Statut :** Normatif

---

## 1. Principe fondateur

> **Arsenal détient le temps. Home Assistant l'exécute.**

Toute décision métier à effet différé doit être matérialisée dans un état persistant Arsenal
avant que Home Assistant ne l'exécute.

Home Assistant est le runtime, l'orchestrateur, le bus d'états.
Il n'est plus l'autorité temporelle métier.

---

## 2. Le `for:` comme anti-pattern Arsenal

### 2.1 Définition

Le paramètre `for:` de Home Assistant déclenche une automation après qu'un état
a été maintenu pendant une durée donnée. La minuterie est portée implicitement
par le moteur HA et n'est jamais persistée.

### 2.2 Usages autorisés

| Usage | Statut | Justification |
|---|---|---|
| Filtre anti-rebond sur signal physique | ✅ Autorisé | Durée courte, perte sans conséquence métier |
| Debounce de capteur (mouvement, contact) | ✅ Autorisé | Signal, pas décision |
| Porteur de causalité métier durable | ❌ Anti-pattern | Voir §2.3 |

### 2.3 Pourquoi le `for:` causal est un anti-pattern

**Fragilité au redémarrage.** La minuterie `for:` est perdue à chaque redémarrage HA.
Si l'entité déclencheuse est déjà dans l'état cible au boot, aucun front n'est émis,
aucune minuterie ne repart. La décision est silencieusement perdue.

**Inauditabilité.** Il est impossible de répondre à la question
*"depuis quand cette extinction est-elle prévue ?"* sans reconstituer
l'historique des fronts. Aucun état observable ne porte l'intention.

**Causalité embarquée dans le moteur.** La décision n'appartient pas à Arsenal —
elle appartient au scheduler interne de HA. Elle ne peut être ni inspectée,
ni corrigée, ni rejouée.

**Non reconstructibilité.** Un redémarrage pendant le `for:` en cours
détruit l'information causale sans trace. Il n'existe aucun mécanisme de reprise.

---

## 3. Autres sources de causalité volatile

Le `for:` n'est pas le seul vecteur. Sont également considérés comme porteurs
de causalité volatile, et donc soumis à la même doctrine :

| Source | Problème |
|---|---|
| `last_changed` comme autorité causale | Réinitialisé au boot, non persistant |
| `sun.sun` comme déclencheur implicite | États `unavailable` → `below_horizon` au boot piégeux |
| `unavailable → off` comme front métier | Transition parasite, non intentionnelle |
| `timer.*` sans `restore: true` comme mémoire métier unique | Perdu au redémarrage ; un `timer` avec `restore: true` peut être acceptable comme mécanisme d'exécution, mais ne constitue pas à lui seul une mémoire métier suffisante |
| Fronts `state` perdus au reboot | Tout trigger `platform: state` sans stratégie de reprise |

---

## 4. Pattern de remplacement — Deadline persistante

### 4.1 Principe

Toute temporisation à effet métier durable est remplacée par une **deadline persistante**,
stockée dans un `input_datetime` Arsenal.

La deadline est :
- écrite par une automation dédiée au moment où la décision est prise,
- lue par une automation d'exécution déclenchée par l'`input_datetime`, `homeassistant.start` et `automation_reloaded`,
- reconstructible à tout moment par lecture directe de l'état.

### 4.2 Structure type

**Entité deadline :**
```yaml
input_datetime.{zone}_extinction_deadline
```

**Automation 1 — Écriture de la deadline (décision) :**
```yaml
trigger:
  - platform: state
    entity_id: binary_sensor.mouvement_{zone}
    to: "off"

action:
  - action: input_datetime.set_datetime
    target:
      entity_id: input_datetime.{zone}_extinction_deadline
    data:
      datetime: >
        {{ (now() + timedelta(minutes=states('input_number.duree_absence_{zone}') | int(20)))
           .strftime('%Y-%m-%d %H:%M:%S') }}
```

**Automation 2 — Exécution (extinction) :**
```yaml
trigger:
  - platform: time
    id: deadline_atteinte
    at: input_datetime.{zone}_extinction_deadline

  - platform: homeassistant
    id: redemarrage_ha
    event: start

  - platform: event
    id: automation_rechargee
    event_type: automation_reloaded

action:
  - choose:
      - conditions:
          - condition: trigger
            id: deadline_atteinte
        sequence:
          - [conditions métier spécifiques]
          - [action d'extinction]

      - conditions:
          - condition: trigger
            id: redemarrage_ha
        sequence:
          - delay: "00:01:30"
          - condition: state
            entity_id: binary_sensor.mouvement_{zone}
            state: "off"
          - condition: template
            value_template: >
              {% set dl = states('input_datetime.{zone}_extinction_deadline') %}
              {{ dl not in ('unknown', 'unavailable', 'none', '')
                 and now() >= dl | as_datetime }}
          - [conditions métier spécifiques]
          - [action d'extinction]

      - conditions:
          - condition: trigger
            id: automation_rechargee
        sequence:
          - delay: "00:00:10"
          - condition: template
            value_template: >
              {% set dl = states('input_datetime.{zone}_extinction_deadline') %}
              {{ dl not in ('unknown', 'unavailable', 'none', '')
                 and now() >= dl | as_datetime }}
          - [conditions métier spécifiques]
          - [action d'extinction]
```

### 4.3 Règle d'annulation et d'invalidation de deadline

La deadline n'est pas effacée à chaque retour de mouvement. Le comportement normalisé est :

**Retour de mouvement (`on`) :** la deadline est laissée en place.
Les conditions métier de l'automation d'exécution (état lumière, état mouvement)
empêchent l'extinction si le mouvement est actif.
La deadline sera écrasée par la prochaine transition `off`.

**Raison :** effacer la deadline au retour de mouvement introduit un risque symétrique —
si le retour de mouvement est une transition parasite (`unavailable → on`),
la deadline est détruite sans raison métier légitime.

**Nouvelle transition `off` :** la deadline est remplacée par la valeur recalculée.
L'automation d'écriture est idempotente ; chaque `off` repart d'un délai frais.

**Règle résumée :**

| Événement | Action sur la deadline |
|---|---|
| Mouvement → `off` | Deadline écrite / remplacée |
| Mouvement → `on` | Deadline conservée, exécution bloquée par condition |
| Deadline atteinte, mouvement encore `off` | Extinction exécutée |
| Deadline atteinte, mouvement repassé `on` | Condition échoue, rien ne se passe |

Tout domaine nécessitant un effacement explicite de la deadline
(ex. : annulation manuelle, mode vacation) doit le formaliser dans son propre contrat.

### 4.4 Propriétés garanties par ce pattern

| Propriété | `for:` causal | Deadline persistante |
|---|---|---|
| Survie au redémarrage | ❌ | ✅ |
| Auditabilité | ❌ | ✅ |
| Reconstructibilité | ❌ | ✅ |
| Observable dans l'UI | ❌ | ✅ |
| Indépendant du moteur HA | ❌ | ✅ |

---

## 5. Stratégie de migration

### 5.1 Critères de priorisation

Les `for:` causaux existants sont audités et classés selon la **criticité de perte au reboot** :

| Niveau | Critère | Exemples |
|---|---|---|
| 🔴 Critique | Risque matériel, sécurité, ressource physique | Arrosage, chauffage, alarmes |
| 🟠 Significatif | Consommation inutile prolongée, inconfort | Éclairages automatiques |
| 🟡 Tolérable | Effet cosmétique, récupération rapide | Notifications, logs |

### 5.2 Séquence de migration confirmée

1. **Éclairage garage** — premier candidat : `garage_light_state` existant,
   infrastructure logique partiellement en place.
2. **Éclairage séjour** — introduction préalable d'un état logique souverain requise.
3. **Audit global** — tous les `platform: state` + `for:` Arsenal sans stratégie de reprise boot.

### 5.3 Règle pour les nouveaux domaines

Tout nouveau domaine Arsenal intégrant une temporisation à effet métier durable
doit naître directement avec le pattern deadline persistante.
Le `for:` causal n'est pas une étape intermédiaire acceptable.

---

## 6. Résumé de la bascule architecturale

| Ancien modèle | Nouveau modèle |
|---|---|
| HA détient le temps | Arsenal détient le temps |
| Minuterie implicite moteur | Décision persistée |
| Causalité volatile | Causalité observable |
| État non reconstructible | État reconstructible |
| Comportement | Intention matérialisée |
| Moteur événementiel | Système décisionnel |

---

*Document normatif Arsenal. Toute dérogation doit être explicitement justifiée dans le contrat du domaine concerné.*
