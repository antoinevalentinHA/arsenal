# ARSENAL — CONTRAT NORMATIF
## Ouvertures Zigbee — Capteurs réconciliés par dernier événement valide

---

**Statut :** ADOPTÉ  
**Version :** 2.0  
**Domaine :** Zigbee / Ouvertures / Aération / Chauffage / Sécurité thermique  
**Remplace :** v1.1 (réconciliation asymétrique Aqara/Sonoff par état brut)

**Changelog v2.0 :**
- Abandon de toute priorité de marque ou de capteur
- Abandon du vote sur états bruts instantanés
- Principe canonique : **dernier événement valide reçu, toutes sources confondues**
- Implémentation via template binary_sensor déclenché (`trigger-based`)
- `unknown` limité à l'absence totale d'historique valide

---

## 1. Contexte et hypothèses terrain

### 1.1 Architecture matérielle

Pour chaque ouvrant critique, deux capteurs Zigbee sont déployés en redondance :

- **capteur_A** — ex. Aqara
- **capteur_B** — ex. Sonoff

Le contrat **ne donne aucune priorité normative** à une marque ou un modèle.

### 1.2 États bruts possibles

| État          | Signification         | Exploitable comme événement |
|---------------|-----------------------|-----------------------------|
| `on`          | ouverture détectée    | ✅ oui                      | 
| `off`         | fermeture détectée    | ✅ oui                      |
| `unknown`     | état indéterminé      | ❌ non                      |
| `unavailable` | capteur non joignable | ❌ non                      |

### 1.3 Hypothèses opérationnelles

**H1 — Les événements constatés sont présumés valides**  
Un `on` ou `off` reçu de n'importe quelle source est présumé valide tant qu'aucune observation terrain ne démontre le contraire. Un capteur peut manquer un événement, mais il n'invente pas d'événement.

**H2 — Des événements peuvent être manqués**  
Un capteur peut rater un changement d'état et rester figé. C'est le risque dominant (état zombie).

**H3 — Aucune source n'est structurellement plus fiable qu'une autre**  
La fiabilité relative des capteurs peut varier terrain, mais ne constitue pas un critère normatif.

**H4 — Le risque dominant est le faux ouvert persistant**  
Un état zombie `on` peut bloquer le chauffage indéfiniment. C'est la conséquence la plus grave à éviter.

---

## 2. Objet du capteur réconcilié

Un **capteur réconcilié** est une entité métier représentant :

> « L'état logique d'un ouvrant, déterminé par le dernier événement valide reçu de l'une ou l'autre des sources redondantes, dans l'ordre d'arrivée observé par Home Assistant. »

Il constitue la **source canonique N1** pour toute logique métier (chauffage, aération, sécurité thermique, alertes, métriques). Aucune logique ne consomme directement les sources brutes lorsqu'un capteur réconcilié existe.

---

## 3. Principe fondamental

> **La vérité réconciliée est le dernier événement valide (`on` ou `off`) reçu de l'une ou l'autre des sources, dans l'ordre d'arrivée des `state_changed`.**

Corollaires directs :

- Un `off` reçu de n'importe quelle source clôture immédiatement l'état réconcilié, quelle que soit la valeur courante de l'autre capteur.
- Un `on` reçu de n'importe quelle source ouvre immédiatement l'état réconcilié.
- Les états bruts instantanés des capteurs ne sont pas la base de décision — ils sont purement observationnels.

Ce principe protège naturellement contre les zombies : dès qu'un capteur détecte la fermeture, l'état réconcilié passe `off`, même si l'autre reste bloqué `on`.

---

## 4. Algorithme de réconciliation

```
À chaque state_changed reçu d'une source :

  Si nouvel_état ∈ {on, off} :
    → state_réconcilié = nouvel_état

  Si nouvel_état ∈ {unknown, unavailable} :
    → ignorer pour la réconciliation
    → conserver l'état réconcilié précédent
    → recalculer degrade
```

**Initialisation :** si aucun événement valide n'a encore été reçu d'aucune source → `state = unknown`.

---

## 5. Implémentation Home Assistant

Le capteur réconcilié est implémenté comme un **template binary_sensor déclenché** (`trigger-based`).

Ce choix est fondé sur les propriétés suivantes de HA :
- un template trigger-based s'exécute à chaque `state_changed` des sources surveillées
- il voit bien l'événement dans l'ordre d'arrivée, pas un snapshot d'état
- son état est **restauré au redémarrage** pour les binary_sensors trigger-based
- `this.state` permet de conserver proprement l'état précédent sans helper externe

### Gabarit YAML normatif

```yaml
template:
  - trigger:
      - platform: state
        entity_id:
          - binary_sensor.capteur_a
          - binary_sensor.capteur_b
    binary_sensor:
      - name: "Contact reconcilie"
        unique_id: contact_reconcilie
        device_class: opening
        state: >
          {% set new_state = trigger.to_state.state %}
          {% if new_state in ['on', 'off'] %}
            {{ new_state }}
          {% else %}
            {{ this.state if this.state in ['on', 'off'] else 'unknown' }}
          {% endif %}
        attributes:
          etat_a: "{{ states('binary_sensor.capteur_a') }}"
          etat_b: "{{ states('binary_sensor.capteur_b') }}"
          degrade: >
            {{ states('binary_sensor.capteur_a') in ['unknown', 'unavailable']
               or states('binary_sensor.capteur_b') in ['unknown', 'unavailable'] }}
          divergence: >
            {{ states('binary_sensor.capteur_a') in ['on', 'off']
               and states('binary_sensor.capteur_b') in ['on', 'off']
               and states('binary_sensor.capteur_a') != states('binary_sensor.capteur_b') }}
```

**Note sur le fallback :** si `this.state` est non initialisé (première création, premier cycle), le fallback est `unknown` — jamais `off`. Déclarer `off` sans événement valide reçu serait une violation de I5.

---

## 6. Observabilité

| Attribut | Type | Description |
|---|---|---|
| `state` | `on / off / unknown` | État réconcilié canonique (N1) |
| `etat_a` | `on / off / unknown / unavailable` | État brut courant A |
| `etat_b` | `on / off / unknown / unavailable` | État brut courant B |
| `divergence` | booléen | A et B exploitables mais états bruts différents |
| `degrade` | booléen | Au moins une source actuellement disqualifiée |

La `divergence` brute **n'a aucun pouvoir d'arbitrage sur l'état réconcilié** — elle constitue uniquement un signal d'observabilité.

Le flag `degrade` décrit l'état **actuel des sources**, pas la validité de l'historique retenu. Un état réconcilié fondé sur un événement mémorisé reste pleinement valide même si `degrade = true`.

La `divergence` et la `degrade` sont des **signaux d'alerte observationnels**. Ils doivent être visibles en dashboard et loggés.

---

## 7. Table de vérité normative

### Cas nominaux

| Dernier événement reçu | État réconcilié | Note                |
|------------------------|-----------------|---------------------|
| `off` (A ou B)         | **off**         | Fermeture immédiate |
| `on` (A ou B)          | **on**          | Ouverture immédiate |

### Cas dégradés

| Situation                                               | État réconcilié | degrade |
|---------------------------------------------------------|-----------------|---------|
| Source disqualifiée, dernier event de l'autre = `off`   | **off**         | true    |
| Source disqualifiée, dernier event de l'autre = `on`    | **on**          | true    |
| Deux sources disqualifiées, dernier event connu = `off` | **off**         | true    |
| Deux sources disqualifiées, dernier event connu = `on`  | **on**          | true    |
| Aucun événement valide jamais reçu                      | **unknown**     | true    |

**Note :** même avec deux sources disqualifiées, l'historique valide déjà reçu est conservé via `this.state`. `unknown` n'est produit qu'en absence totale d'historique.

---

## 8. Interdictions absolues

**I1 — Interdiction de priorité matérielle**  
Aucune marque ou modèle ne peut être déclaré prioritaire.

**I2 — Interdiction de vote sur états bruts instantanés**  
L'état réconcilié ne peut pas résulter d'un simple vote ou comparaison d'états bruts.

**I3 — Interdiction de masquer la divergence**  
Toute divergence doit être exposée et observable.

**I4 — Interdiction de consommation directe des sources brutes**  
Toute logique métier critique consomme uniquement le capteur réconcilié N1.

**I5 — Interdiction de produire `off` sans fondement événementiel**  
Une fermeture ne peut être déclarée que sur la base d'un événement `off` valide reçu — jamais par timeout, inférence, absence de signal, ou état non initialisé.

**I6 — Interdiction de produire `unknown` si un historique valide existe**  
`unknown` n'est autorisé qu'en absence totale d'événement valide reçu (premier démarrage sans historique restauré).

---

## 9. Limites reconnues et risques acceptés

### 9.1 Risque : `on` intempestif d'une source défaillante

Un capteur défaillant émettant un `on` parasite ferait passer l'état réconcilié à `on`.

**Mitigation :** H1 postule que les événements constatés sont vrais. Si cette hypothèse est invalidée terrain, un debounce peut être ajouté en couche supérieure sans modifier ce contrat.

### 9.2 Risque : fenêtre `unknown` à la première création

Si aucun historique n'est disponible (première création d'entité), l'état est `unknown` jusqu'au premier événement valide reçu.

**Mitigation :** les template binary_sensors trigger-based restaurent leur état au redémarrage — ce cas ne concerne que la toute première initialisation.

---

## 10. Critères d'acceptation

Le contrat est respecté si et seulement si :

- L'état réconcilié suit immédiatement tout événement valide reçu de n'importe quelle source
- Un `off` reçu clôture l'état réconcilié même si l'autre source reste `on`
- Un `on` reçu ouvre l'état réconcilié même si l'autre source reste `off`
- `unknown` n'est produit qu'en absence totale d'événement valide (aucun historique disponible)
- Aucune marque n'est priorisée
- La divergence est exposée dès que les états bruts diffèrent
- La dégradation est exposée dès qu'une source est disqualifiée
- Aucune logique métier ne consomme directement les sources brutes

---

## 11. Évolutions futures prévues

| Évolution                     | Déclencheur                            | Impact contrat                            |
|-------------------------------|----------------------------------------|-------------------------------------------|
| Debounce sur événements `on`  | `on` parasite observé terrain          | Couche filtre supérieure, hors contrat N1 |
| Watchdog anti-zombie temporel | Besoin de détection de zombie résiduel | Couche supérieure, hors contrat N1        |
| Score de confiance par source | Statistiques terrain longues           | Nouveau contrat v3                        |

---

*Fin du contrat — ARSENAL v2.0*