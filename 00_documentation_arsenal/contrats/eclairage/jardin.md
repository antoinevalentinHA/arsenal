# 🧠 ARSENAL — CONTRAT FONCTIONNEL
## Éclairage du jardin (matin / soir)

---

## 🎯 OBJET

Ce document définit le **contrat fonctionnel** du système
d’éclairage automatique du jardin.

Il décrit **l’intention utilisateur**, les **règles métier**
et les **invariants fonctionnels**, indépendamment de toute
implémentation Home Assistant.

Ce document fait foi tant que l’intention utilisateur ne change pas.

---

## 🟦 1. INTENTIONS UTILISATEUR

### 🔘 Délégation de contrôle

L’utilisateur peut activer ou désactiver séparément :
- l’éclairage automatique du **matin**
- l’éclairage automatique du **soir**

Ces actions :
- ne déclenchent aucune action immédiate
- modifient uniquement le cadre de décision futur
- n’altèrent jamais l’état matériel instantané

---

### 🌅 Intention — MATIN

> Le matin, l’éclairage du jardin est un **agrément visuel**,
> comparable à celui du soir,
> mais **uniquement tant que la lumière naturelle est insuffisante**.

Principes fonctionnels :
- si la lumière naturelle est déjà suffisante, l’éclairage ne s’allume pas
- l’éclairage devient inutile dès que le jour est établi
- il n’apporte aucune valeur une fois la luminosité naturelle suffisante
- l’éclairage du matin ne doit jamais se prolonger tardivement

Le soleil est utilisé comme **indicateur de pertinence lumineuse**,
jamais comme une autorité décisionnelle directe.

---

### 🌆 Intention — SOIR

> Le soir, l’éclairage du jardin est un **agrément d’accompagnement**
> de la vie intérieure, **conditionné par la présence dans la maison**.

Principes fonctionnels :
- le coucher du soleil définit une **fenêtre de possibilité**
- tant que personne n’est présent à la maison, l’éclairage reste éteint
- l’éclairage s’active lorsque la présence est détectée
  après l’ouverture de cette fenêtre
- une fois allumé, il dure un certain temps, mais pas toute la nuit
- tant que le séjour est occupé, l’éclairage ne doit pas s’éteindre brutalement
- l’éclairage du soir ne doit jamais empiéter sur le matin

La présence :
- conditionne **l’activation effective**
- conditionne **la douceur de l’extinction**
- ne définit pas à elle seule l’existence temporelle du soir

---

## 🟩 2. PLANIFICATION JOURNALIÈRE
*(Temps civil, borné au jour)*

### 🌅 Cadre MATIN

Chaque jour, le système définit :

- une **heure de début** (référence utilisateur)
- une **heure de fin logique** (lever du soleil + délai)
- une **heure de fin absolue** (borne fixe de sécurité)

Ces bornes définissent une **fenêtre de pertinence lumineuse matinale**.

En dehors de cette fenêtre :
- l’éclairage du matin n’a plus de sens
- aucune activation ne doit avoir lieu

La fenêtre appartient strictement au **jour civil courant**
et ne se prolonge jamais au lendemain.

---

### 🌆 Cadre SOIR

Chaque jour, le système définit :

- une **heure d’ouverture de la possibilité du soir**
  (coucher du soleil avec décalage)
- une **durée maximale logique**
- une **borne de fin absolue système**
  garantissant la libération du matin

Le soir est modélisé comme un **cycle temporel continu**
dont l’activation effective dépend de la présence.

---

## 🟨 3. DÉCISIONS MÉTIER OBSERVABLES

Les décisions métier sont :
- déterministes
- dérivables d’états persistants explicites
- observables
- recalculables à tout instant

---

### 🌅 Décision — Fenêtre MATIN valide

> Sommes-nous actuellement dans la fenêtre
> de pertinence lumineuse du matin aujourd’hui ?

Cette décision dépend uniquement :
- du temps civil courant
- des bornes journalières calculées
- de l’autorisation utilisateur

Elle ne dépend pas :
- de la présence
- du soir
- de l’état matériel de l’éclairage

---

### 🌆 Décision — Cycle SOIR actif

> Le cycle d’éclairage du soir est-il en cours ?

Cette décision dépend :
- de l’ouverture temporelle du soir
- de la présence détectée après cette ouverture
- de la durée maximale
- de la borne de fin absolue
- de l’autorisation utilisateur

Elle ne dépend pas :
- du matin
- de l’état matériel de l’éclairage

---

### 🌆 Décision — Extinction SOIR autorisée

> Peut-on éteindre l’éclairage du jardin
> sans rupture brutale de confort ?

Cette décision dépend explicitement :
- de la durée minimale du cycle soir atteinte depuis la commande d’allumage
- de l’inactivité séjour consolidée

Elle représente une **règle de confort humain**.

La deadline soir ouvre la possibilité d’extinction.
La deadline d’inactivité séjour autorise humainement son exécution.
L’extinction n’est causée que par la conjonction des deux.

Un mouvement séjour ultérieur repousse la condition de confort
et peut différer l’extinction tant que l’occupation persiste.

Cette décision est matérialisée par deux deadlines persistantes :
- `input_datetime.jardin_soir_extinction_deadline`
- `input_datetime.jardin_sejour_inactivite_deadline`

Le capteur `binary_sensor.lumiere_jardin_soir_extinction_autorisee`
en est la **projection d’observabilité** — il reflète l’état de ces
deux deadlines à des fins d’UI et de diagnostic.
Il n’a aucun rôle causal dans la chaîne d’extinction.

---

## 🟥 4. RÈGLE D’ARBITRAGE UNIQUE

À un instant donné,
l’éclairage du jardin ne peut être gouverné
que par **une seule politique active**.

Ordre de priorité :

1. **SOIR**, si le cycle soir est actif
2. **MATIN**, si la fenêtre matin est valide
3. **AUCUNE**, sinon

Cette règle est :
- globale
- unique
- explicite
- indépendante de la présence

---

## 🟥 5. ACTION MATÉRIELLE

Les actions matérielles sont purement réactives :

- si une politique est active → éclairage ON
- si aucune politique n’est active → éclairage OFF
- si politique SOIR active et les deux deadlines d’extinction dépassées
  (deadline soir ET deadline inactivité séjour) → éclairage OFF

L’extinction est déclenchée de façon événementielle
par des triggers temporels explicites sur deadlines persistantes.
Elle n’est pas une règle instantanée.

Les scripts pilotent le matériel.
Les automatisations réagissent aux décisions métier.
Aucune logique fonctionnelle ne doit exister à ce niveau.

---

## 🚫 CE QUE CE CONTRAT INTERDIT

- un cycle dépendant d’un autre cycle
- une priorité implicite ou distribuée
- l’utilisation du soleil à la fois en calcul et en décision
- une fenêtre ou un cycle projeté au lendemain
- l’usage de la présence comme condition unique d’existence temporelle

---

## 🧠 PHRASE DE SYNTHÈSE

> La lumière naturelle détermine la pertinence.
> La présence déclenche et adoucit.
> Le temps borne et protège.
> L’arbitrage tranche.

---

## 🟫 5bis. NOTIFICATIONS UTILISATEUR (règle contractuelle)

Les notifications associées à l’éclairage du jardin
obéissent aux règles suivantes :

- Une **notification persistante** ne peut représenter
  **qu’un état matériel réellement vécu**.
- Pour le domaine Éclairage jardin, cela signifie :
  - *éclairage actuellement allumé*.

Sont **explicitement exclues** des notifications persistantes :
- les fenêtres de pertinence (matin ou soir),
- les décisions métier abstraites,
- les fins de cycle,
- les événements passés (extinction, clôture, dépassement de durée).

Conséquences contractuelles :
- l’extinction matérielle suffit comme signal utilisateur,
- aucune notification persistante ne peut subsister
  après extinction de l’éclairage,
- toute autre information relève au maximum
  d’une notification **non persistante** ou d’aucune notification.

Cette règle vise à garantir :
- une lecture utilisateur fidèle à la réalité vécue,
- l’absence de mémoire UI artificielle,
- une robustesse totale aux redémarrages.

---

## 🟪 6. ASYMÉTRIE FONCTIONNELLE MATIN / SOIR

Le comportement de l’éclairage du jardin n’est volontairement
**pas symétrique** entre le matin et le soir.

Cette asymétrie est une conséquence directe
de l’évolution naturelle de la lumière du jour.

---

### 🌅 MATIN — Allumage fragile

Le matin :
- la lumière naturelle **augmente**
- la fenêtre de pertinence lumineuse est **courte**
- un allumage peut ne **jamais** avoir lieu
  malgré l’existence théorique de la fenêtre

Conséquence fonctionnelle :

> Un cycle matinal peut se terminer
> sans avoir jamais été effectivement engagé.

Le système doit donc être capable de distinguer :
- la fin d’un cycle réellement vécu
- la disparition d’une opportunité non utilisée

Cette distinction est nécessaire pour :
- éviter toute notification abusive
- préserver la résilience aux redémarrages
- maintenir une lecture utilisateur fidèle à la réalité

---

### 🌆 SOIR — Extinction critique

Le soir :
- la lumière naturelle **diminue**
- la fenêtre temporelle s’ouvre naturellement
- l’activation effective dépend de la présence
- l’extinction constitue l’événement critique

Conséquence fonctionnelle :

> Toute extinction du soir doit être
> explicitement autorisée par une décision métier
> de confort humain.

Cette autorisation :
- n’est acquise que lorsque les deux conditions sont simultanément vraies :
  durée minimale du cycle soir atteinte ET inactivité séjour consolidée
- garantit l’absence de coupure brutale
- peut être différée par un mouvement séjour ultérieur,
  qui repousse la deadline d’inactivité tant que l’occupation persiste

---

### 🧠 Règle générale

> Lorsque la lumière naturelle augmente,
> le système protège l’allumage.
>
> Lorsque la lumière naturelle diminue,
> le système protège l’extinction.

Cette règle est structurante
et s’applique à tout domaine éclairage
reposant sur le cycle jour / nuit.

---

## 📌 STATUT

- Version : **Arsenal v14.x** *(contrat amendé — architecture deadlines persistantes)*
- Nature : **Contrat fonctionnel**
- Domaine : **Éclairage jardin**
- Rôle : **Document de référence**
- Modification : uniquement lors d’un changement d’intention utilisateur