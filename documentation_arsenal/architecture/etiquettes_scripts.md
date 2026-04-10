# Arsenal — Contrat de catégorisation des scripts HA
**Version** : 1.0.1  
**Statut** : Validé — production  
**Périmètre** : Tous les scripts Home Assistant du système Arsenal  
**Relation** : Taxonomie sœur du contrat de catégorisation des automatisations (v1.1.1) — même esprit architectural, objet distinct

---

## 1. Principe fondateur

### 1.1 Nature d'un script vs nature d'une automatisation

Une automatisation porte un **rôle système visible** : elle se déclenche, réagit, orchestre, met en visibilité. Sa catégorisation reflète son rôle dans le flux observable d'Arsenal.

Un script porte un **rôle d'implémentation** : il est appelé, encapsule, séquence, délègue. Sa catégorisation reflète sa **finalité architecturale intrinsèque**, indépendamment de qui l'appelle ou du contexte dans lequel il est invoqué.

> **Règle fondamentale** : La catégorisation d'un script suit sa finalité intrinsèque — non le type du composant appelant, non le contexte d'invocation, non la simple présence d'actions dans son corps.

### 1.2 Principe directeur

> **Taguer selon la finalité, jamais selon l'implémentation.** Un script qui "exécute des actions" n'est pas automatiquement `script:execution`. La question est : *pourquoi ce script existe-t-il ?*

---

## 2. Modèle de catégories

Le modèle repose sur **4 catégories fonctionnelles**, mutuellement exclusives.

---

### Catégorie A — `script:decision`

**Définition** : Script dont la finalité est de **produire ou consolider une vérité de gouvernance** — un état canonique, une décision métier, un signal d'autorité.

**Caractéristiques** :
- Modifie un `input_boolean`, `input_select`, `input_number`, ou un état de gouvernance de domaine
- Peut encapsuler une logique conditionnelle complexe aboutissant à une décision
- Peut être appelé par plusieurs automatisations sans changer de nature

> **Piège à éviter — helpers** : L'écriture d'un `input_boolean`, `input_number` ou autre helper n'implique pas automatiquement un classement en `script:decision`. Le critère déterminant est la nature de ce que représente le helper, non l'acte d'écriture :
> - Helper représentant une **vérité de gouvernance** (décision domaine, mode actif, autorisation) → `script:decision`
> - Helper utilisé comme **état technique, mémoire ou compteur** → `script:support`
> - Helper servant de **levier d'application** (setpoint, consigne transmise à un actionneur) → `script:execution`
>
> Sinon, tout script qui touche un `input_*` devient artificiellement `script:decision`.

**Exemples Arsenal** :
- Script de consolidation d'état de présence canonique
- Script de calcul et écriture d'un mode domaine
- Script d'arbitrage entre plusieurs signaux de demande

---

### Catégorie B — `script:execution`

**Définition** : Script dont la finalité est d'**appliquer nominalement une action ou une séquence d'actions** sur un équipement, un bus, ou un système externe — dans le cadre du flux normal attendu.

**Caractéristiques** :
- Produit un effet physique ou externe : `mqtt.publish`, `climate.set_*`, `switch.turn_*`, appel API
- Sa raison d'être est d'**exécuter le nominal prévu** — piloter, activer, séquencer, orchestrer une chaîne d'actions métier
- Ne contient pas de logique de détection d'écart ou de remédiation — ces responsabilités appartiennent à `script:guard`

**Distinction critique avec `script:guard`** : la présence d'actions dans le corps d'un script ne suffit pas à le classer `script:execution`. Ce qui compte est la **finalité** : le script est-il là pour exécuter le nominal, ou pour corriger un écart ?

**Exemples Arsenal** :
- Script d'envoi de commande chaudière (séquence nominale)
- Script d'activation VMC avec séquençage L1/L2
- Script de pilotage climatisation Fujitsu Airstage
- Script de fermeture volets en séquence

---

### Catégorie C — `script:guard`

**Définition** : Script dont la finalité est de **corriger un écart, rétablir une cohérence, ou protéger le système** — retry, remédiation, réconciliation, restauration d'invariant.

**Caractéristiques** :
- Sa raison d'être est une **anomalie possible ou avérée** : échec de commande, timeout, incohérence d'état, violation d'invariant
- Peut contenir des actions concrètes (retry d'une commande, forçage d'état) — cela ne le reclasse pas en `script:execution`
- Finalité défensive : il existe parce que le nominal peut échouer, pas pour exécuter le nominal

> Un script de retry est `script:guard` même s'il finit par envoyer une commande physique. Sa raison d'être est la remédiation, pas l'exécution nominale.

**Exemples Arsenal** :
- Script de retry commande chaudière après timeout
- Script de réconciliation état VMC (restauration XOR invariant)
- Script de watchdog climatisation
- Script de remédiation connectivité Netatmo

---

### Catégorie D — `script:support`

**Définition** : Script sans autorité architecturale propre de décision, d'exécution métier ou de remédiation, servant de **brique transverse de support technique**.

**Définition positive** (non résiduelle) : `script:support` désigne explicitement les scripts dont la finalité est :
- **Factorisation** : éviter la duplication de logique entre appelants
- **Wrapper** : encapsuler un appel de service avec normalisation des paramètres
- **Formatage** : transformer, préparer, normaliser des données
- **Journalisation** : persister un état, un événement, une trace
- **Transformation utilitaire** : conversion, calcul sans autorité de gouvernance
- **Service transversal** : brique réutilisable sans finalité autonome

**Critère décisif** : isolé de ses appelants, ce script **ne porte pas à lui seul une intention architecturale** de décision, d'exécution métier ou de défense. Il sert — il ne dirige pas, n'applique pas au sens métier, ne remédie pas.

> `script:support` est une catégorie positive et définie. Ce n'est pas la catégorie des scripts qu'on n'a pas su classer.

**Exemples Arsenal** :
- Script de notification générique (formatage + envoi, sans logique d'alerte propre)
- Script de persistance / mémorisation d'état
- Script de rotation de valeur min/max
- Wrapper de service MQTT avec normalisation
- Script utilitaire de nettoyage d'état nominal

---

## 3. Labels recommandés

### Labels à créer dans Home Assistant

```
script:decision
script:execution
script:guard
script:support
```

### Conventions de nommage

- Préfixe `script:` — namespace dédié, distinct du préfixe `signal:` des automatisations
- Minuscules, pas d'espaces, pas d'accents
- Quatre labels — liste **fermée**
- Aucun script ne reste sans label (contrairement aux automatisations où l'absence de label est valide)

### Règle d'unicité

> **Un script = un seul label.** La finalité d'un script est unique par construction. Si l'attribution est ambiguë, c'est un signal que le script mélange des responsabilités — le découper, pas multiplier les labels.

### Différence avec les automatisations

Pour les automatisations, l'absence de label est le marqueur du bruit système — c'est intentionnel et suffisant.

Pour les scripts, **tous les scripts sont taguès**. Un script sans label est un oubli de classification, pas une déclaration d'appartenance au bruit.

---

## 4. Règles de classification (contrat)

### 4.1 Arbre de décision

```
Le script produit-il ou consolide-t-il une vérité
de gouvernance ou un état canonique de domaine ?
    └── OUI → script:decision

Le script applique-t-il nominalement une action
ou une séquence sur un équipement ou bus externe,
dans le cadre du flux prévu ?
    └── OUI → script:execution

Le script existe-t-il pour corriger un écart,
rétablir une cohérence, ou remettre en état
après anomalie, échec ou violation d'invariant ?
    └── OUI → script:guard

Le script est-il une brique de support technique
sans autorité architecturale propre
(wrapper, factorisation, formatage, journalisation) ?
    └── OUI → script:support
```

### Règle de priorité en cas de conflit

Lorsqu'un script semble satisfaire plusieurs critères simultanément, appliquer la catégorie la plus haute dans l'ordre suivant :

```
1. script:guard      — la remédiation prime sur tout
2. script:decision   — la gouvernance prime sur l'application
3. script:execution  — l'application prime sur le support
4. script:support    — catégorie de base si aucune autorité propre
```

Cette règle n'est pas une invitation à rationaliser un script mal découpé. Si deux catégories semblent également valides, c'est presque toujours le signe que le script mélange deux responsabilités distinctes et doit être scindé. La règle de priorité tranche les cas véritablement ambigus — elle ne dispense pas du découpage.

### 4.2 Cas limites et résolutions

| Situation | Résolution |
|---|---|
| Script de retry qui envoie une commande physique | `script:guard` — sa finalité est la remédiation. La commande est un moyen, pas la raison d'être. |
| Script de notification d'alerte | `script:guard` si la logique d'alerte lui est propre ; `script:support` s'il est un wrapper générique d'envoi appelé par le composant qui détecte l'anomalie |
| Script de notification nominale (confirmation d'action réussie) | `script:support` — brique de formatage/envoi sans autorité de détection |
| Script appelé à la fois par un `signal:decision` et un `signal:guard` | Le label suit la finalité intrinsèque du script, pas celle de ses appelants. Si les deux usages sont légitimes, le script est mal découpé. |
| Script qui consolide un état ET envoie une commande | Découper. Si impossible, `script:execution` — l'effet externe prime pour la traçabilité, mais noter la dette. |
| Script de séquençage pur (A puis B puis C) sans logique propre | `script:execution` si la séquence est nominale ; `script:guard` si la séquence est une procédure de récupération. |
| Script utilitaire de calcul sans écriture d'état de gouvernance | `script:support` — transformation sans autorité. |

### 4.3 Interdictions formelles

- ❌ Ne pas classer `script:execution` un script dont la raison d'être est la remédiation ou le retry — même s'il contient des appels de service physiques
- ❌ Ne pas classer `script:support` un script qui prend des décisions de gouvernance ou remédie à des anomalies — même s'il est "petit" ou "simple"
- ❌ Ne pas utiliser `script:support` comme catégorie résiduelle pour les scripts non identifiés
- ❌ Ne pas laisser un script sans label
- ❌ Ne pas assigner deux labels à un même script — l'ambiguïté est un signal de couplage à corriger
- ❌ Ne pas faire varier le label d'un script selon son appelant

### 4.4 Invariants du modèle

> **Invariant execution** : Tout effet physique ou externe nominal produit via script doit être traçable dans la vue `script:execution`. Si ce n'est pas le cas, c'est un défaut de classification ou un script non tagué.

> **Invariant guard** : Tout mécanisme de retry, de réconciliation ou de restauration d'invariant implémenté en script doit être traçable dans la vue `script:guard`, indépendamment du contexte d'appel.

> **Invariant support** : Tout script classé `script:support` doit pouvoir être décrit comme "brique de service technique sans finalité autonome". Si la description requiert les mots *décide*, *commande*, *corrige*, ou *remédie*, le classement est faux.

> **Invariant de découpage** : Tout script dont la finalité architecturale ne peut pas être énoncée en une seule phrase courte est considéré comme mal découpé. Un script = une intention. Si deux intentions coexistent dans le corps du script, il doit être scindé en deux scripts distincts, chacun avec son propre label. Cette règle s'applique indépendamment de la taille ou de la complexité apparente du script.

---

## 5. Recommandations pratiques

### 5.1 Stratégie de déploiement

Aligner sur les phases du contrat des automatisations :

1. **Phase 1** : Tagger `script:execution` en priorité — scripts d'envoi de commandes physiques nominales. Valider l'invariant execution.
2. **Phase 2** : Tagger `script:guard` — scripts de retry, watchdog, réconciliation.
3. **Phase 3** : Tagger `script:decision` — scripts de consolidation d'état de gouvernance.
4. **Phase 4** : Tagger `script:support` — wrappers, utilitaires, journalisation. Vérifier que l'invariant support tient pour chacun.
5. **Phase 5** : Vérifier qu'aucun script n'est sans label.

### 5.2 Relation avec les automatisations

Les deux taxonomies sont indépendantes et complémentaires :

| Couche | Objet | Taxonomie |
|---|---|---|
| Déclenchement / orchestration | Automatisation | `signal:*` |
| Implémentation / séquence | Script | `script:*` |

Un filtre UI sur `signal:execution` montre les automatisations qui commandent des équipements. Un filtre sur `script:execution` montre les scripts qui implémentent ces commandes. Ce sont deux lectures orthogonales, pas redondantes.

### 5.3 Erreurs à éviter

- **Ne pas confondre présence d'actions et finalité d'exécution.** Presque tout script "fait des actions". La question est toujours : *pourquoi ce script existe-t-il ?*
- **Ne pas laisser `script:support` croître sans contrôle.** Si cette catégorie devient majoritaire, c'est souvent le signe que des scripts portent des responsabilités non nommées.
- **Ne pas tagger à la création** — attendre que le rôle du script soit stabilisé et que ses appelants soient connus.

---

## Annexe — Gabarit de classification rapide

```
entity_id     : script.xxx
name          : [nom lisible]
appelants     : [automations / scripts appelants connus]
finalité      : [gouvernance / exécution nominale / remédiation / support technique]
label assigné : [script:decision | script:execution | script:guard | script:support]
justification : [1 phrase — commencer par "Ce script existe pour..."]
```

---

*Arsenal — Contrat de catégorisation des scripts v1.0.1*
