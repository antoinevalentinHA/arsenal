# 🔌 Contrat Arsenal — Panne secteur (Socle)

**Version :** 1.0  
**Compatible :** Arsenal v6+  
**Statut :** Contrat actif  

**Historique :**
- v1.0 : création — qualification panne secteur, invariants d'architecture, monotonicité, unicité du signal, indisponibilité du capteur

---

## 🎯 Objet

Ce contrat définit la **qualification d'une panne secteur** et les **invariants système** associés.

Il constitue le **socle normatif commun** à tous les comportements Arsenal liés à la résilience électrique.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la définition d'une panne secteur
- les règles de qualification et de stabilité
- les invariants d'architecture associés

Il ne couvre pas :

- les effets métier (chauffage, ECS, etc.)
- les actions système
- la signalisation utilisateur
- les choix d'implémentation technique propres à Home Assistant

---

## 🚨 Définition d'une panne secteur

Une **panne secteur** est considérée active lorsque :

- `binary_sensor.coupure_secteur == on`
- et que cet état est confirmé temporellement

Cette confirmation temporelle doit :

- exclure les micro-coupures et sauts de tension
- reposer sur une durée minimale de confirmation
- être définie explicitement dans le document normatif de temporalité :  
  `/documentation_arsenal/architecture/resilience_electrique/10_temporalite.md`

Ce document est **NORMATIF** pour toute implémentation. Toute durée de confirmation non issue de ce document est invalide.

Une panne secteur ne peut donc pas être qualifiée active sur la seule base d'un changement d'état bref ou transitoire.

La panne est considérée terminée lorsque :

- `binary_sensor.coupure_secteur == off`
- de manière stable
- et à l'issue d'une observation réelle du retour à l'état normal

La fin de panne ne peut jamais être déduite d'une simple restauration d'état logiciel, ni de la disparition du signal d'entrée sans confirmation positive de retour à la normale.

---

## 📎 Note d'implémentation Arsenal

Le signal canonique de coupure secteur est exposé via :

```
binary_sensor.coupure_secteur
```

Ce nom est **normatif** dans l'implémentation Home Assistant Arsenal. Aucun consommateur ne doit référencer un autre signal pour qualifier l'état de panne secteur.

---

## 🧠 Principe fondamental Arsenal

> **Un événement critique ne déclenche jamais directement une action métier.  
> Il publie un état ou une intention explicite.**

---

## 🧭 Invariants d'architecture

### Source de vérité observable

Tout dispositif participant à la qualification d'une panne secteur doit demeurer **observable pendant l'événement qu'il qualifie**, selon l'architecture de résilience en vigueur.

Un dispositif incapable de rester observable pendant la panne ne peut pas constituer à lui seul une source de vérité suffisante.

### Qualification fondée sur le réel

La qualification d'entrée en panne et de sortie de panne doit reposer sur une observation stable du réel, et non sur une simple réhydratation logicielle d'état.

### Unicité du signal canonique

La qualification de panne secteur produit un **signal canonique unique** : `binary_sensor.coupure_secteur`.

Aucun consommateur ne doit interpréter directement des sources physiques multiples non consolidées. La consolidation éventuelle de plusieurs sources est une responsabilité de la couche de détection, transparente pour les couches supérieures.

### Monotonicité de l'état

Une panne secteur qualifiée active **ne peut être annulée qu'après confirmation positive et stable du retour à la normale**.

La disparition du signal d'entrée ne constitue pas à elle seule une confirmation de fin de panne. L'état "panne active" est persistant jusqu'à levée explicite fondée sur le réel.

### Indisponibilité du signal canonique

Si `binary_sensor.coupure_secteur` est en état `unavailable` ou `unknown` — notamment au démarrage de Home Assistant — le système ne peut pas qualifier l'état de panne secteur.

Dans ce cas :

- l'état de panne ne peut être ni confirmé ni infirmé
- aucune action métier ne peut s'appuyer sur cet état non qualifié
- l'architecture de résilience doit prévoir un **mécanisme de fallback** permettant de restaurer la disponibilité du signal

Le système garantit la **disponibilité du signal canonique**, pas la disponibilité d'un capteur individuel.

Le mécanisme de fallback est défini dans :  
`/documentation_arsenal/architecture/resilience_electrique/20_fallback.md`

Ce mécanisme relève **exclusivement de la couche de détection**. Il peut reposer sur :

- la supervision de la disponibilité des réseaux (ex : Zigbee)
- la redondance de capteurs physiques
- des stratégies de sélection de source

Dans tous les cas :

- le fallback ne doit jamais exposer plusieurs sources aux consommateurs
- le signal canonique `binary_sensor.coupure_secteur` reste l'unique interface
- la logique de fallback est transparente pour les couches supérieures

> ⚠️ Toute source physique participant au fallback doit demeurer observable pendant une panne secteur. Une source dépendante du secteur ne peut pas constituer une source primaire valide.

### Neutralité métier du socle

Le présent contrat ne confère aucune autorité métier sur le chauffage, l'ECS ou tout autre sous-système. Il ne définit que la qualification de l'événement, les conditions minimales de fiabilité, et les invariants de séparation des responsabilités.

---

## 🚫 Comportements strictement interdits

- Déclencher directement une action métier à partir d'un événement système
- Interpréter directement des sources physiques non consolidées
- Mélanger détection, intention, décision et action
- Introduire un état implicite non observable
- Qualifier une panne réelle sur la base d'un état transitoire non confirmé
- Qualifier une fin de panne sur la base d'une simple restauration logicielle ou de la disparition du signal d'entrée
- Utiliser un signal autre que `binary_sensor.coupure_secteur` comme source de qualification

---

## 🔗 Traçabilité des garanties

| Garantie | Fondement contractuel |
|---|---|
| Exclusion des micro-coupures | Confirmation temporelle obligatoire → `10_temporalite.md` |
| Stabilité au redémarrage HA | Qualification fondée sur le réel — exclusion de la réhydratation logicielle |
| Séparation des responsabilités | Principe fondamental Arsenal + Neutralité métier du socle |
| Absence de rebond d'état | Monotonicité de l'état |
| Cohérence inter-systèmes | Unicité du signal canonique |
| Résilience en cas de perte du capteur | Invariant indisponibilité + mécanisme de fallback |

---

## 🛡️ Garanties apportées par ce contrat

- Qualification robuste des pannes secteur
- Exclusion contractuelle des micro-coupures non significatives
- Comportement stable en cas de redémarrage Home Assistant
- Absence de rebond entre états "panne" et "normal"
- Cohérence garantie entre tous les consommateurs du signal
- Séparation stricte des responsabilités
- Comportement défini en cas d'indisponibilité du capteur
- Base opposable pour tous les contrats dérivés
