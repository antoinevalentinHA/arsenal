# ARSENAL — Audit · Chaîne transactionnelle MQTT Boiler (cas ECS)

**Composant :** `arsenal-ha` · `arsenal-boiler-bridge`
**Scope :** Pattern transactionnel boiler — cas de référence ECS setpoint — 6 couches
**Statut :** Dette technique identifiée, non critique
**Références :** contrat bridge v0.4.3 · contrat ACK HA v1.2 · contrat script exécutif v1.1
**Date :** 2026-03-26

---

## 1. Nature du système et périmètre

L'ECS est utilisé comme cas de référence, mais l'analyse porte sur un pattern générique applicable à l'ensemble des commandes boiler : chauffage (setpoint), pente (slope), parallèle (shift). Ces commandes reposent toutes sur le même mécanisme : `command → request_id → ACK → corrélation → statut`. Les constats et limites identifiés ici ne sont donc pas spécifiques à l'ECS — ils concernent l'ensemble des interactions transactionnelles avec la chaudière.

La chaîne auditée est transactionnelle (request_id + ACK corrélé), stratifiée proprement (6 couches distinctes), non heuristique (pas de déduction via télémétrie), et opérationnellement stable.

Elle implémente correctement : corrélation explicite ACK ↔ commande, séparation stricte observation / diagnostic / exécution, distinction claire succès (`applied`) vs non-succès (`accepted` exclu).

**Conclusion : base architecturelle saine.**

---

## 2. Point clé — correction de l'analyse intermédiaire

Contrairement à l'analyse intermédiaire, il existe bien une mémoire locale du résultat, portée par `script.ecs_appliquer_consigne_confirmee` et matérialisée dans `input_text.ecs_cycle_last_action_status`, avec normalisation stricte : `applied` | `rejected` | `timeout`.

**Requalification :** le système n'est pas dépourvu de vérité locale.

> Le point réel est : le résultat local existe, mais il est dérivé de sensors ACK globaux, et non retourné directement par le script bridge.

---

## 3. Architecture réelle (stratification)

**Périmètre :**

| Composant | Fichier |
|-----------|---------|
| Script exécutif bas niveau | `script.ecs_appliquer_consigne_bridge` |
| Script enveloppe (normalisation résultat) | `script.ecs_appliquer_consigne_confirmee` |
| Capteurs MQTT bruts bridge | `mqtt_sensors/boiler/boiler_bridge.yaml` · `mqtt_binary_sensors/boiler/boiler_bridge.yaml` |
| Capteurs MQTT bruts télémétrie | `mqtt_sensors/boiler/boiler_telemetry.yaml` · `mqtt_binary_sensors/boiler/boiler_telemetry.yaml` |
| Capteurs MQTT bruts ACK / erreur | `mqtt_sensors/boiler/boiler_command_feedback.yaml` |
| Capteurs template diagnostiques | `boiler_command_feedback.yaml` |
| Capteurs template transactionnels | `boiler_ack_dhw_set_setpoint_transaction.yaml` |

### Couches A–C — Observation

Bridge (online, heartbeat…), télémétrie chaudière, ACK brut JSON. Parfaitement découplé, sans logique parasite. ✔

### Couche D — Diagnostic

Extraction `status`, `reason`, etc. Aucun arbitrage métier. Propre, lisible. ✔

### Couche E — Corrélation transactionnelle

Comparaison `request_id` ACK vs helper. Production état synthétique.

⚠️ Dynamique (non figé) — dépend du helper courant.

### Couche F — Exécution (deux niveaux)

**Script bridge (bas niveau) :** publish → wait_template → nettoyage. Ne fige pas de résultat local.

**Script confirmé (enveloppe) :** lit les sensors ACK, normalise, écrit dans le helper résultat. Porte la vérité locale. ✔

---

## 4. Ce qui est structurellement solide

- Corrélation transactionnelle réelle (non simulée)
- Ordre critique respecté : helper → publish (supprime la race condition ACK ultra-rapide)
- Aucune confusion télémétrie / preuve d'exécution
- Séparation des couches rigoureuse
- Optimisation no-op maîtrisée (optimisation locale d'évitement, non validation transactionnelle)

**Architecture sérieuse, auditable, non bricolée.**

---

## 5. Limite principale (requalifiée)

Le résultat local n'est pas natif, mais reconstruit via lecture globale.

Concrètement : le script enveloppe lit `sensor.boiler_ack_*_status` au lieu de recevoir un résultat encapsulé du script bridge.

**Conséquence :** dépendance à l'état global au moment de la lecture, pas de capture transactionnelle pure. Robustesse correcte en nominal, non parfaite aux cas limites temporels.

**Dette technique réelle mais contenue.**

---

## 6. Écart contractuel principal

`bridge_online` est présent en couche observation (✔) mais absent de la logique transactionnelle (✗).

Le système observe la session bridge, mais ne la consomme pas dans la transaction ECS.

**Impact :** absence de garantie explicite que l'ACK exploité provienne d'une session bridge valide au moment de la transaction — non-alignement avec le contrat cible.

**Seul écart réellement structurant.**

---

## 7. Autres limites (secondaires)

- `pending` trop large : agrège `accepted`, mismatch, anciens ACK, états transitoires — perte de granularité diagnostique.
- Corrélation non persistante : dépend du helper, perd sa valeur après nettoyage.
- Aucune gestion de concurrence (acceptable si usage réellement séquentiel).
- Rupture de session bridge non traitée explicitement dans le script.

Défauts d'observabilité ou de robustesse future — non critiques aujourd'hui.

---

## 8. Évaluation du risque

**Risque observé : faible.** Aucun signe de faux succès, perte d'ACK ou instabilité.

**Risques théoriques :** incohérence temporelle possible, dépendance aux sensors globaux, absence de garde session. Risques latents uniquement.

---

## 9. Position recommandée

**Ne rien modifier.**

Système stable, comportement nominal correct, bénéfice d'une modification inférieur au risque de régression.

**Statut : dette technique identifiée — non critique.**

---

## 10. Axes d'amélioration (non urgents)

| Priorité | Axe |
|----------|-----|
| 1 | Intégrer `bridge_online` dans la logique transactionnelle |
| 2 | Retourner un résultat transactionnel natif (script bridge → script enveloppe) |
| 3 | Affiner l'état `pending` (discrimination mismatch / transitoire) |
| 4 | Gérer la concurrence si le pattern est réutilisé à plus grande échelle |
| 5 | Harmoniser les conventions `reason` (`none` / `unknown`) |

Améliorations de durcissement — aucune correction urgente.

---

## 11. Conclusion

Le système est proprement conçu, transactionnel réel, stable en production, et possède déjà une mémoire locale de résultat.

Points faibles résiduels : résultat local indirect (via sensors globaux) plutôt que nativement encapsulé, et absence d'intégration de `bridge_online` dans la logique transactionnelle.

Ces constats ne sont pas spécifiques à l'ECS. Ils s'appliquent à l'ensemble des commandes boiler qui reposent sur le même pattern. Le corriger ou le durcir sur ECS revient à corriger le standard boiler.

> Système transactionnel sain et stratifié. Résultat local existant mais dérivé de sensors globaux. Seul écart structurant : absence d'intégration de `bridge_online`. Dette technique non critique — aucune modification recommandée.

---

## Addendum — Hétérogénéité de complétude du standard boiler

L'examen des scripts `chauffage_appliquer_pente`, `chauffage_appliquer_parallele` et `chauffage_appliquer_consigne` confirme deux choses : le socle transactionnel boiler est bien transversal, et son niveau de complétude varie selon les commandes.

### Niveaux de complétude observés

**Niveau 1 — Socle transactionnel pur**
`chauffage_appliquer_pente`, `chauffage_appliquer_parallele` : publish → wait_template → nettoyage. La conclusion repose directement sur le sensor transactionnel live. Aucune écriture métier locale conditionnée par le succès.

**Niveau 2 — Socle transactionnel + écriture métier locale après succès corrélé**
`chauffage_appliquer_consigne` : même socle, mais avec une étape de conclusion locale — écriture de `input_select.chauffage_dernier_mode_decide` conditionnée à `status == applied AND request_id corrélé`. Présence d'un verrou applicatif local (`input_boolean.chauffage_application_en_cours`). Mémoire souveraine écrite uniquement sur succès réel.

**Niveau 3 — Socle transactionnel + enveloppe explicite de normalisation**
`ecs_appliquer_consigne_confirmee` : couche enveloppe dédiée qui normalise le résultat en `applied | rejected | timeout` dans `input_text.ecs_cycle_last_action_status`.

### Ce que cette graduation confirme

Les écarts identifiés dans l'audit (`bridge_online` non intégré, résultat dérivé de sensors globaux, concurrence non protégée) sont bien **boiler-wide** — ils ne varient pas selon le niveau de complétude. `chauffage_appliquer_consigne` confirme notamment que même à un niveau de maturité supérieur, `bridge_online` reste absent de la logique transactionnelle.

### Formulation requalifiée

Le standard boiler ne se réduit pas à "ECS plus abouti que le reste". La lecture correcte est :

> Le boiler repose sur un socle transactionnel commun, sur lequel certaines commandes ajoutent une couche locale de restitution ou d'écriture métier, tandis que d'autres restent au niveau du sensor transactionnel live. Le socle existe de fait — il est finalisé de manière hétérogène selon les interactions.

**Cette hétérogénéité ne remet pas en cause la recommandation : aucune modification immédiate.**

---

## Addendum 2 — Cartographie des points d'entrée et conséquence sur `bridge_online`

### Patterns d'appel observés

L'examen des appelants révèle trois patterns distincts, indépendants du niveau de complétude transactionnel.

**Pattern A — Point d'entrée unique (propre)**
`decision_centrale.yaml → script.chauffage_appliquer_consigne`
Séparation parfaite, gouvernance claire. C'est ici que `bridge_online` peut être branché une seule fois, proprement.

**Pattern B — Enveloppe orchestrée (semi-propre)**
Scripts ECS → `script.ecs_appliquer_consigne_confirmee` → `script.ecs_appliquer_consigne_bridge`
Bon design, mais partiellement contourné : des appels directs au script bas niveau existent en parallèle de l'enveloppe.

**Pattern C — Appel direct (brut)**
Automations courbe de chauffe → `script.chauffage_appliquer_pente` / `script.chauffage_appliquer_parallele`
Fonctionne, mais sans point d'entrée centralisé. Aucun endroit propre pour brancher `bridge_online`.

### Requalification du problème `bridge_online`

La garde `bridge_online` ne peut pas être intégrée proprement en l'absence d'un point d'entrée canonique par domaine. Toute tentative d'intégration au niveau des scripts exécutifs constituerait une violation de la séparation des couches.

| Domaine | Point d'entrée | `bridge_online` branchable ? |
|---------|---------------|------------------------------|
| Chauffage consigne | `decision_centrale.yaml` | ✔ oui — une seule fois |
| ECS | `ecs_appliquer_consigne_confirmee` | ✔ oui — après suppression des appels directs |
| Courbe de chauffe (pente / parallèle) | aucun | ✗ pas encore |

### Conséquence

La garde `bridge_online` ne peut pas être intégrée proprement tant qu'un point d'entrée unifié n'existe pas pour chaque domaine. L'introduire dans les scripts exécutifs bas niveau serait contraire à leur rôle.

**Prochaine évolution logique (non urgente) :** définir un point d'entrée canonique `chauffage_appliquer_courbe` qui orchestre pente et parallèle, et devient le seul endroit où `bridge_online` est évalué pour ce domaine.
