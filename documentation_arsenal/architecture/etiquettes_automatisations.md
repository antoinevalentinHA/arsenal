# Arsenal — Contrat de catégorisation des automatisations HA
**Version** : 1.1.1  
**Statut** : Proposition — prête à validation  
**Périmètre** : Toutes les automatisations Home Assistant du système Arsenal

---

## 1. Audit synthétique

### 1.1 Contexte du problème

Arsenal a migré d'un modèle purement événementiel vers un modèle hybride. Cette évolution est architecturalement justifiée (pipelines de fusion thermique, stabilisation EWMA, diagnostics continus), mais elle a effacé la distinction visuelle entre :

- les automatisations qui **prennent des décisions ou exécutent des actions** (signal métier)
- les automatisations qui **alimentent le modèle interne en continu** (bruit système)

Résultat : dans la vue "dernières exécutions" de l'UI HA, les pipelines météo et de stabilisation écrasent les événements opérationnels. L'observabilité métier est dégradée.

### 1.2 Groupes naturels identifiés (sans liste exhaustive)

| Groupe observé | Exemples Arsenal typiques |
|---|---|
| Pipelines de fusion / calcul continu | température jardin, fusion EWMA, timestamps météo |
| Décisions domaine | chauffage ON/OFF, ECS demande, clim admissibilité |
| Exécution physique | envoi commande chaudière, activation clim, VMC relay |
| Surveillance défensive / remédiation | watchdog clim, diagnostic connectivité, retry, détection invariant |
| Présence / sécurité | armement alarme, arrivée/départ, GPS haute précision |

### 1.3 Incohérences attendues

- Absence de labels sur la majorité des automatisations (catégorisation implicite par nom)
- Mélange décision + exécution dans une même automatisation dans les domaines anciens
- Pipelines continus non distingués des automatisations événementielles dans l'UI
- Aucun mécanisme actuel permettant de filtrer le signal du bruit

---

## 2. Modèle de catégories

### Principe directeur

> **Taguer le signal, jamais le bruit.** L'absence de label est la marque du bruit système.

Le modèle repose sur **3 catégories fonctionnelles**, mutuellement exclusives, alignées sur les couches Arsenal.

---

### Catégorie A — `signal:decision`

**Définition** : L'automatisation évalue une condition métier et **produit une décision** (booléen, état, mode) qui gouverne d'autres composants.

**Caractéristiques** :
- Modifie un `input_boolean`, `input_select`, `input_number`, ou un état de gouvernance de domaine
- Représente l'**autorité centrale** d'un domaine
- Ne commande rien de physique — elle statue, d'autres exécutent

**Exemples Arsenal** :
- Décision de demande de chauffage
- Calcul d'admissibilité climatisation (verrou HEAT/COOL/DRY)
- Décision d'armement alarme
- Activation mode Vacances

---

### Catégorie B — `signal:execution`

**Définition** : L'automatisation **traduit une décision en commande physique ou externe** — équipement, bus MQTT, relay, API.

**Caractéristiques** :
- Appelle un service HA produisant un effet matériel ou externe (`climate.set_*`, `mqtt.publish`, `switch.turn_*`, script souverain)
- Ne prend aucune décision — elle **applique** une décision déjà prise et tracée en amont
- Périmètre strict : **équipements et bus uniquement**. Les notifications n'appartiennent pas à cette catégorie (voir `signal:guard`)

**Exemples Arsenal** :
- Envoi commande chaudière via MQTT (boiler bridge)
- Activation/désactivation VMC relay L1/L2
- Commande climatisation Fujitsu Airstage
- Activation volets roulants

---

### Catégorie C — `signal:guard`

**Définition** : L'automatisation se déclenche sur une **condition anormale** — exception, violation d'invariant, timeout, perte de disponibilité, incohérence d'état — et produit une remédiation défensive ou une alerte opérateur.

> `signal:guard` ne désigne pas une automatisation "prudente" ou "protectrice" au sens large. Il désigne exclusivement une automatisation déclenchée par un écart avéré par rapport au comportement nominal attendu. Une automatisation préventive qui s'exécute sur flux normal n'est pas `signal:guard`.

**Caractéristiques** :
- Se déclenche sur **condition anormale** : timeout, état `unavailable`, valeur hors seuil critique, violation d'invariant, perte de cohérence
- Produit : retry, reset, forçage d'état, notification d'alerte
- Ne se substitue pas à une décision de gouvernance — elle réagit à un écart, elle ne gouverne pas

**Exemples Arsenal** :
- Watchdog climatisation (retry après échec de commande)
- Diagnostic connectivité Netatmo
- Détection panne Internet + remédiation timer
- Détection incohérence VMC (violation XOR invariant)
- Notification de timeout boiler bridge
- Alerte température hors plage

---

### Doctrine notifications (règle normative)

> Une automatisation dont le **rôle principal** est d'émettre une notification d'alerte, d'anomalie, d'échec, d'incohérence, de timeout ou de remédiation est classée `signal:guard`.
>
> Une notification purement informative ou nominale (confirmation d'action réussie, fin de cycle normal, changement de mode nominal) ne qualifie pas à elle seule une automatisation pour `signal:guard`. Dans ce cas, le label suit le rôle principal de l'automatisation (`signal:exec` ou `signal:decision`) et la notification est un effet secondaire non déterminant pour la classification.

---

### Ce qui n'est PAS tagué (bruit système)

Les automatisations suivantes **ne reçoivent aucun label** — leur absence dans les vues filtrées est le comportement attendu :

- Pipelines de fusion thermique (température jardin, EWMA, etc.)
- Calculs météo continus (humidité, timestamps, pressions)
- Stabilisation et lissage de capteurs
- Synchronisation d'états intermédiaires
- Projections de présence (sauf si elles prennent une décision)
- **Mémoire, cumul, archivage, reset périodique** : réinitialisations quotidiennes/hebdomadaires, gels de données min/max, compteurs, journalisation nominale, entretien d'état interne — non taguées sauf si elles portent directement une décision de gouvernance, une commande physique, ou une remédiation sur écart avéré

> **Critère d'exclusion** : si l'automatisation ne produit ni décision de gouvernance, ni commande physique sur équipement ou bus, ni réponse à une condition anormale avérée, elle n'est pas taguée. La nature de la production est le seul critère.

---

## 3. Labels recommandés

### Labels à créer dans Home Assistant

```
signal:decision
signal:execution
signal:guard
```

### Conventions de nommage

- Préfixe `signal:` — namespace explicite, évite les collisions avec des labels futurs
- Minuscules, pas d'espaces, pas d'accents
- Trois labels seulement — la liste est **fermée**

### Règle d'unicité

> **Une automatisation = un seul label.** Les rôles multiples indiquent un problème de découpage à corriger, pas une raison d'assigner deux labels.

---

## 4. Règles de classification (contrat)

### 4.1 Arbre de décision

```
L'automatisation produit-elle une décision métier
(modifie un état de gouvernance, statue sur un domaine) ?
    └── OUI → signal:decision

L'automatisation traduit-elle une décision en commande
physique ou sur un bus externe (équipement, MQTT, relay) ?
    └── OUI → signal:execution

L'automatisation se déclenche-t-elle sur une exception,
une anomalie, un timeout ou une violation d'invariant ?
    └── OUI → signal:guard
    (inclut : remédiation, retry, notification d'alerte)

Aucune des conditions ci-dessus ?
    └── Pas de label (bruit système)
```

### 4.2 Cas limites et résolutions

| Situation | Résolution |
|---|---|
| L'automatisation décide ET exécute en un seul bloc | Découper en deux automatisations. Si impossible, classer `signal:execution` — l'effet physique prime pour la traçabilité. |
| L'automatisation projette un état de présence | `signal:decision` si elle modifie un état de gouvernance ; pas de label si elle alimente seulement un sensor intermédiaire |
| Pipeline continu qui, parfois, déclenche une commande physique | Séparer le pipeline (sans label) de la condition de déclenchement d'exécution (`signal:execution`) |
| Notification d'alerte, d'anomalie, d'échec ou de remédiation | `signal:guard` — c'est le rôle principal de l'automatisation |
| Notification informative accompagnant une action nominale | Le label suit le rôle principal (`signal:execution` ou `signal:decision`) ; la notification est un effet secondaire |
| Retry automatique | `signal:guard` — le retry est une réponse à une anomalie, pas une exécution nominale |
| Forçage d'état suite à incohérence détectée | `signal:guard` — la détection d'incohérence qualifie, même si l'action corrective est physique |
| Reset périodique nominal (quotidien, hebdomadaire) | Pas de label — entretien d'état interne, pas de production de signal |

### 4.3 Interdictions formelles

- ❌ Ne pas assigner `signal:decision` à une automatisation qui ne modifie aucun état de gouvernance
- ❌ Ne pas assigner `signal:execution` à une automatisation qui calcule, projette, ou notifie sans commander un équipement ou un bus
- ❌ Ne pas assigner `signal:execution` à une notification d'alerte ou d'anomalie — celles-ci sont `signal:guard`
- ❌ Ne pas assigner `signal:guard` à une automatisation préventive ou périodique qui s'exécute sur flux nominal sans condition anormale avérée
- ❌ Ne pas créer de label par domaine métier (`chauffage`, `clim`, `meteo`) — cela contredit l'objectif
- ❌ Ne pas assigner deux labels à une même automatisation
- ❌ Ne pas tagger les pipelines continus sous prétexte qu'ils "contribuent" à une décision

### 4.4 Invariants du modèle

> **Invariant execution** : Toute commande physique ou sur bus externe envoyée par Arsenal doit être traçable via `signal:execution`. Si une telle commande ne peut pas être retrouvée dans cette vue, c'est un défaut de classification.

> **Invariant guard** : Toute notification d'alerte, d'anomalie, d'échec ou de remédiation émise par Arsenal doit être traçable via `signal:guard`, sauf si elle est un effet secondaire d'une automatisation dont le rôle principal est `signal:execution` ou `signal:decision`.

---

## 5. Recommandations pratiques

### 5.1 Stratégie de déploiement

**Approche recommandée : progressive par criticité**

1. **Phase 1 — Exécution physique** : Tagger en priorité toutes les automatisations `signal:execution` (chaudière, VMC, clim, volets). Ce sont les plus critiques et les moins nombreuses. Valider l'invariant execution immédiatement.

2. **Phase 2 — Décisions domaine** : Tagger les `signal:decision` par domaine, en commençant par les domaines les plus actifs (chauffage, vacances, présence).

3. **Phase 3 — Surveillance défensive** : Identifier et tagger les `signal:guard` — watchdogs, remédiations, notifications d'alerte. C'est souvent la catégorie la plus dispersée dans le corpus.

4. **Phase 4 — Validation** : Parcourir toutes les automatisations sans label et confirmer explicitement que leur absence est intentionnelle.

### 5.2 Vue opérationnelle cible

Créer dans HA une vue dédiée avec filtre sur `signal:decision` + `signal:execution`. C'est la vue de supervision quotidienne — elle montre ce qu'Arsenal a décidé et ce qu'il a commandé. La vue `signal:guard` est la vue de diagnostic — elle montre ce qui a dysfonctionné ou nécessité une intervention défensive.

### 5.3 Erreurs à éviter

- **Ne pas tagger pendant l'implémentation d'une nouvelle automatisation** — attendre que le rôle soit stabilisé
- **Ne pas utiliser les labels comme documentation** — ils ne décrivent pas ce que fait l'automatisation, seulement son rôle architectural
- **Ne pas créer de label `signal:pipeline`** — l'absence de label est suffisante et plus robuste (pas de drift si un pipeline est oublié)

### 5.4 Pièges UI Home Assistant

- La vue "dernières automatisations" ne peut pas exclure — c'est le problème de départ, les labels ne le résolvent pas directement. La solution est de créer une **vue dédiée avec filtre d'inclusion** sur les labels signal.
- Les labels HA sont case-sensitive dans certaines versions — utiliser exclusivement des minuscules.
- Un label supprimé d'une automatisation n'est pas supprimé du registre HA tant qu'il est référencé ailleurs — ne pas s'en inquiéter.
- Les filtres de tableau de bord HA par label sont disponibles dans la vue liste des automatisations (Settings → Automations) — pas besoin de Lovelace custom pour l'usage opérationnel de base.

---

## Annexe — Gabarit de classification rapide

Pour chaque automatisation à classer :

```
entity_id     : automation.xxx
name          : [nom lisible]
déclencheur   : [event / state / time / mqtt / …]
produit       : [état de gouvernance / commande physique / réponse anomalie / calcul]
label assigné : [signal:decision | signal:execution | signal:guard | aucun]
justification : [1 phrase]
```

---

*Arsenal — Contrat de catégorisation v1.1.1*
