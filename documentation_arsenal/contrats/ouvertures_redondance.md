# ARSENAL — Contrat Normatif v2.2
## Réconciliation des capteurs de contact — Capteurs critiques

**Statut :** Normatif  
**Date :** 2026-03-11  
**Périmètre :** Capteurs de classe `capteur_critique`

---

## 1 — Classification des capteurs

### 1.1 Classe `standard`

Capteurs dont un état incorrect transitoire n'entraîne pas de risque métier significatif.

Règle applicable : réconciliation par dernier événement valide reçu.

### 1.2 Classe `capteur_critique`

Capteurs dont un état incorrect peut bloquer ou déclencher à tort une automatisation à effet réel.

Le critère de classification est le **couplage fonctionnel** du capteur dans l'architecture d'automatisation, pas son type physique. 
Un capteur de fenêtre qui gouverne le chauffage est critique. Un capteur de porte qui ne déclenche qu'une notification ne l'est pas nécessairement.

Exemples : fenêtre pilotant une zone de chauffage, contact conditionnant une alarme, ouvrant bloquant un système de ventilation.

Règle applicable : contrat décrit ci-après.

La classe est déclarée explicitement par instance dans la configuration. Absence de déclaration = classe `standard` par défaut.

---

## 2 — Séparation des couches d'état

Pour tout capteur de classe `capteur_critique`, le système maintient trois couches distinctes :

| Couche | Identifiant | Définition |
|--------|-------------|------------|
| État observé | `observed_event` | Dernier événement reçu syntaxiquement valide, quelle que soit sa validité sémantique |
| Vérité métier retenue | `business_state` | État appliqué aux automatisations et à l'interface utilisateur |
| État d'observabilité | `reconciliation_status` | Diagnostic courant du système de réconciliation |

Ces couches ne sont pas interchangeables. Toute automatisation doit consommer `business_state`, jamais directement les états bruts des sources.

---

## 3 — Règle de réconciliation asymétrique

### 3.1 Traitement d'un événement `off`

Un événement `off` reçu de l'une quelconque des sources est accepté immédiatement comme vérité métier, 
y compris pendant une quarantaine active ou une phase d'inhibition.

Justification : sur un capteur critique, la fermeture est le cas sûr. 
Les événements `off` sont acceptés comme vérité métier par défaut, sauf contradiction future. 
Cette présomption est un choix de politique fail-safe, pas une vérité physique.

**Action :**
- `business_state` → `off`
- `reconciliation_status` → `stable`
- Toute quarantaine `on` en cours est annulée

### 3.2 Traitement d'un événement `on`

Un événement `on` n'est pas accepté immédiatement comme vérité métier. 
Il déclenche l'ouverture d'une fenêtre de corroboration, sous réserve que le système soit en état stable (§5).

---

## 4 — Fenêtre de corroboration

### 4.1 Définition

À la réception d'un événement `on` d'une source, le système ouvre une fenêtre de durée `T_corroboration` 
pendant laquelle il attend une transition corroborante de l'autre source.

### 4.2 Valeur normative

| Paramètre | Valeur par défaut | Plage admissible | Configurabilité |
|-----------|------------------|------------------|-----------------|
| `T_corroboration` | **5 s** | 2 s – 10 s | Par instance |

La valeur plancher de 2 s correspond au délai physique nominal entre deux capteurs lors d'une ouverture réelle. 
La valeur plafond de 10 s est une borne dure : au-delà, le système masque l'incertitude au lieu de la gérer.

### 4.3 Condition de corroboration valide

La corroboration est valide si et seulement si l'autre source effectue une **transition `off` → `on`** 
dans la fenêtre `T_corroboration` suivant l'événement déclencheur.

Une simple coïncidence d'états (`on` simultané sans transition détectable) n'est pas une corroboration valide. 
Cette règle protège contre les états restaurés au redémarrage HA et les replays Zigbee post-retour de mesh, 
qui font remonter les deux sources en `on` sans séquence physique réelle.

### 4.4 Corroboration réussie

- `business_state` → `on`
- `reconciliation_status` → `stable`

### 4.5 Corroboration échouée — entrée en quarantaine

Si aucune corroboration n'est reçue dans `T_corroboration` :

- L'événement `on` passe en quarantaine
- `business_state` reste inchangé
- `reconciliation_status` → `quarantine`
- Durée de quarantaine : `T_quarantaine = T_corroboration`

---

## 5 — Inhibition post-startup / reconnexion

### 5.1 Signal de stabilité système

Arsenal expose un signal de stabilité système normalisé :

| Entité | État | Signification |
|--------|------|---------------|
| `binary_sensor.systeme_stable` | `on` | Système stabilisé — réconciliation autorisée |
| `binary_sensor.systeme_stable` | `off` | Phase de démarrage, instabilité ou retour incomplet — réconciliation inhibée |

Ce signal est la référence normative pour l'inhibition. Il n'est pas défini par un délai absolu 
mais par une condition de stabilité gouvernée par l'architecture Arsenal. 
Toute substitution par un timer fixe est une déviation contractuelle.

### 5.2 Condition d'inhibition

Tant que `binary_sensor.systeme_stable = off` :

- Toute promotion vers `business_state = on` est interdite, même si une séquence de corroboration est observée
- Les événements reçus sont enregistrés dans `observed_event`
- Les attributs d'observabilité restent alimentés normalement
- `reconciliation_status` → `inhibited`, quel que soit l'état précédent du processus de réconciliation

### 5.3 Levée de l'inhibition

L'inhibition est levée dès que `binary_sensor.systeme_stable` passe à `on`.

À la levée :
- Les événements `on` reçus pendant l'inhibition sont abandonnés — ils ne sont pas rejoués ni réévalués
- `reconciliation_status` → `stable` (si aucune divergence active)

Justification du non-replay : un événement `on` reçu pendant la phase d'instabilité a une fraîcheur sémantique non vérifiable. 
Le rejouer après stabilisation reviendrait à accorder une confiance rétroactive à un événement dont l'origine réelle ne peut être établie.

### 5.4 Limite assumée

Si un capteur critique est en état `on` physiquement réel pendant la phase où `systeme_stable = off`, 
la vérité métier peut rester temporairement à `off` jusqu'à la levée de l'inhibition suivie d'un événement physique réel. 
Cette asymétrie est volontaire et conforme à la politique fail-safe du contrat.

---

## 6 — Quarantaine et escalade

### 6.1 Valeur normative

| Paramètre | Valeur par défaut | Relation |
|-----------|------------------|----------|
| `T_quarantaine` | **5 s** | `T_quarantaine = T_corroboration` |

Les deux durées sont intentionnellement alignées. Une dissociation sans justification fonctionnelle explicite est proscrite.

### 6.2 Résolution de quarantaine

À l'expiration de `T_quarantaine` sans corroboration reçue, l'événement `on` est rejeté comme vérité métier :

- `business_state` reste inchangé
- `reconciliation_status` → `divergent`
- `suspect_event` → `on_non_corroborated`

Il n'y a pas d'expiration silencieuse. L'échec de corroboration est un signal d'observabilité à part entière.

### 6.3 Annulation de quarantaine par `off`

Si un événement `off` est reçu pendant la quarantaine :

- La quarantaine est immédiatement clôturée
- `business_state` → `off`
- `reconciliation_status` → `stable`

---

## 7 — Attributs d'observabilité

| Attribut | Type | Valeurs possibles | Description |
|----------|------|-------------------|-------------|
| `observed_event` | string \| null | `on` / `off` / `null` | Dernier événement syntaxiquement valide reçu, quelle que soit sa validité sémantique |
| `business_state` | string | `on` / `off` | Vérité métier retenue |
| `reconciliation_status` | string | `stable` / `quarantine` / `divergent` / `inhibited` | État courant du processus de réconciliation |
| `suspect_event` | string \| null | `on_non_corroborated` / `null` | Nature de l'événement suspect ayant déclenché l'escalade |
| `last_corroborated_at` | datetime \| null | timestamp ISO 8601 | Horodatage de la dernière corroboration réussie |
| `last_divergence_at` | datetime \| null | timestamp ISO 8601 | Horodatage de la dernière escalade `divergent` |
| `divergence_source` | string \| null | identifiant de source | Source ayant émis l'événement non corroboré |

`reconciliation_status = divergent` est le signal primaire pour les alertes de maintenance.  
`reconciliation_status = inhibited` est informatif — il ne déclenche pas d'alerte.

---

## 8 — Diagramme de décision

```
Événement reçu
      │
      ├─ off ──────────────────────────────────────────► business_state = off
      │                                                   reconciliation_status = stable
      │                                                   (annule quarantaine si active)
      │
      └─ on
            │
            ▼
     systeme_stable = off ?
            │
            ├─ oui ─────────────────────────────────────► observed_event enregistré
            │                                              reconciliation_status = inhibited
            │                                              (abandonné à la levée)
            │
            └─ non
                  │
                  ▼
         Ouvrir fenêtre T_corroboration (5 s par défaut)
                  │
                  ├─ Transition off→on reçue de l'autre source dans T_corroboration
                  │         │
                  │         ▼
                  │   business_state = on
                  │   reconciliation_status = stable
                  │
                  └─ Pas de transition dans T_corroboration
                            │
                            ▼
                     Quarantaine (T_quarantaine = 5 s)
                            │
                            ├─ off reçu pendant quarantaine
                            │         │
                            │         ▼
                            │   business_state = off
                            │   reconciliation_status = stable
                            │
                            └─ T_quarantaine écoulé sans corroboration
                                      │
                                      ▼
                               business_state = inchangé
                               reconciliation_status = divergent
                               suspect_event = on_non_corroborated
```

---

## 9 — Hypothèses normatives

**H1 — Politique fail-safe sur `off`**  
Les événements `off` sont acceptés comme vérité métier par défaut. Il s'agit d'un choix de politique, pas d'une vérité physique. 
Un `off` parasite produira un état incorrect mais temporaire, résolu par la prochaine ouverture physique réelle.

**H2 — Disponibilité de deux sources**  
Le mécanisme de corroboration requiert au minimum deux sources actives. 
Un capteur en classe `capteur_critique` avec une seule source active doit basculer en mode dégradé documenté séparément.

**H3 — Horodatage fiable**  
La fenêtre de corroboration repose sur les timestamps HA. 
Des décalages d'horloge entre coordinateur Zigbee et HA peuvent affecter la précision de la fenêtre. 
Ce risque est mitigé par le choix de `T_corroboration = 5 s`.

**H4 — Indépendance des sources**  
Les deux sources d'un même ouvrant doivent être physiquement et électriquement indépendantes pour que la corroboration ait une valeur discriminante.

**H5 — Fiabilité de `binary_sensor.systeme_stable`**  
L'inhibition repose sur la disponibilité et la fiabilité de ce signal. 
Un signal bloqué à `off` indéfiniment maintient le système en inhibition permanente. 
Ce cas est géré au niveau du signal de stabilité Arsenal, hors périmètre du présent contrat.