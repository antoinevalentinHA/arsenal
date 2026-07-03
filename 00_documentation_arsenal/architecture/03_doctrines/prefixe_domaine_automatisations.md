# 🧠 ARSENAL — Contrat : Préfixe d'ID & domaine fonctionnel propriétaire

> **Statut** : NORMATIF et OPPOSABLE — v1.0 (2026-07-03).
> **Complète** : [`id_automatisations.md`](./id_automatisations.md) — qui régit la **forme** des IDs (structure, attribution, invariants, unicité).
> **Le présent contrat régit leur SENS** : ce que le préfixe affirme, et ce que cette affirmation engage.

---

## 🎯 OBJET

Ce contrat définit le lien entre :

- le **préfixe** (4 premiers chiffres) d'un ID d'automatisation Arsenal ;
- le **domaine fonctionnel propriétaire** de cette automatisation.

Il formalise :

- la notion de **domaine fonctionnel propriétaire** ;
- la distinction entre **dossier physique** et **domaine d'identité** ;
- le rôle du préfixe comme **identité fonctionnelle opposable** ;
- la définition stricte du domaine **`transversal`** ;
- les interdictions associées ;
- les conséquences attendues pour l'audit du corpus et la CI future.

Il ne redéfinit pas :

- le format des IDs (14 chiffres, préfixe 4 + suffixe 10) ;
- la procédure d'attribution des IDs ;
- la procédure de création d'un préfixe
  (cf. [`id_automatisations.md`](./id_automatisations.md) § Création d'un nouveau domaine fonctionnel).

---

## 🧭 DÉFINITIONS

### Domaine fonctionnel propriétaire

Le **domaine fonctionnel propriétaire** d'une automatisation est le domaine
Arsenal qui porte la **responsabilité principale** de son comportement :

- c'est **son** intention métier que l'automatisation matérialise ;
- c'est **son** contrat fonctionnel qui la rend légitime ;
- c'est **lui** qui répond de ses effets.

Toute automatisation a **exactement un** domaine fonctionnel propriétaire
(principe Arsenal : un seul propriétaire par vérité, aucune vérité concurrente).
Ce propriétaire peut être un domaine métier, ou le domaine `transversal`
défini ci-dessous — jamais deux domaines simultanément, jamais aucun.

### Domaine d'identité

Le **domaine d'identité** d'une automatisation est le domaine déclaré par le
**préfixe** de son ID, tel que documenté dans la source de vérité unique :

    /homeassistant/06_input_selects/system/prefix_id.yaml
    (helper input_select.prefix_id_select)

### Dossier physique

Le **dossier physique** est l'emplacement du fichier YAML sous
`11_automations/`. C'est un choix de **rangement**, au service de la
navigation et de la maintenance.

---

## 🧠 PRINCIPE FONDAMENTAL

> **Le préfixe d'un ID d'automatisation déclare son domaine fonctionnel
> propriétaire. Cette déclaration est une identité fonctionnelle OPPOSABLE.**

Concrètement :

- le préfixe n'est **ni décoratif, ni un artefact de génération** :
  il affirme « ce domaine répond de cette automatisation » ;
- cette affirmation est **engageante** : elle doit être vraie au moment de
  l'attribution et le rester ;
- elle est **vérifiable** : tout lecteur, auditeur ou outil doit pouvoir
  confronter le préfixe au comportement réel de l'automatisation ;
- elle est **stable** : l'ID ne changeant jamais (invariant doctrinal),
  le choix du préfixe est un acte d'architecture, pas une commodité.

**Invariant :**

> domaine d'identité (préfixe) **=** domaine fonctionnel propriétaire.

Toute automatisation dont le préfixe ne correspond pas à son domaine
fonctionnel propriétaire est **NON CONFORME** au présent contrat —
sauf exception explicitement documentée et opposable (cf. § Exceptions).

---

## 🗂️ DOSSIER PHYSIQUE ≠ DOMAINE D'IDENTITÉ

Le dossier physique **n'est pas** la source de vérité du domaine :

- une automatisation peut être rangée dans un dossier **pratique**
  tout en relevant d'un autre domaine fonctionnel ;
- le rangement peut suivre des logiques de proximité technique,
  d'exploitation ou de lisibilité ;
- en cas de divergence entre dossier et préfixe,
  **c'est le préfixe qui porte l'identité** — à condition d'être lui-même
  conforme au présent contrat.

Règles :

1. **Par défaut**, dossier et domaine d'identité coïncident : c'est l'état
   normal du corpus, et toute divergence doit rester l'exception.
2. Une divergence dossier ↔ préfixe est **admissible** uniquement si :
   - le préfixe désigne bien le domaine fonctionnel propriétaire réel ;
   - la divergence est **documentée** (en-tête du fichier et/ou registre
     d'exceptions de la CI, cf. § Conséquences — CI).
3. Le chemin du fichier ne constitue **jamais une preuve** : il crée au mieux
   une **présomption simple, réfutable** — jamais une conclusion.
4. Aucun outil (audit, CI, générateur, IA) ne doit **déduire** un préfixe
   d'un dossier, ni « corriger » un préfixe pour le faire coïncider avec un
   dossier (cf. § Interdictions).

---

## 🏷️ DOMAINE `transversal`

### Définition stricte

> Le domaine **`transversal`** regroupe **uniquement** les automatisations
> dont la responsabilité principale est l'**orchestration**, la
> **synchronisation**, la **supervision** ou la **médiation** entre
> plusieurs domaines fonctionnels, **lorsqu'aucun domaine métier unique ne
> peut être désigné comme propriétaire principal**.

`transversal` est un **domaine fonctionnel à part entière** :
il a une responsabilité propre (la cohérence interdomaines),
un périmètre défini, et des critères d'entrée stricts.
Ce n'est **ni un bac à divers, ni une zone d'attente, ni un refuge**
pour les automatisations mal classées.

### Critères d'entrée (TOUS requis)

Une automatisation relève de `transversal` si et seulement si :

1. elle **coordonne plusieurs domaines fonctionnels** (lecture ET action,
   ou arbitrage, sur au moins deux domaines) ;
2. **aucun domaine métier unique** ne porte clairement la responsabilité
   principale de son comportement ;
3. son rôle est une **orchestration, une médiation, une supervision ou une
   cohérence globale** — pas une logique métier d'un domaine donné ;
4. son rattachement à un domaine métier unique serait **artificiel**
   (il faudrait choisir un propriétaire arbitraire parmi plusieurs candidats
   équivalents).

### Critères d'exclusion (UN SEUL suffit à disqualifier)

Ne relève **PAS** de `transversal` :

- une automatisation métier qui **lit simplement un capteur** d'un autre
  domaine (la lecture ne transfère pas la propriété) ;
- une automatisation métier qui **produit une notification**
  (notifier n'est pas orchestrer) ;
- une automatisation métier qui **déclenche une action secondaire** hors de
  son domaine (l'effet de bord ne déplace pas la responsabilité principale) ;
- une automatisation **mal rangée ou mal préfixée** qu'on voudrait éviter de
  corriger ;
- toute **exception de confort** — c'est-à-dire tout cas où `transversal`
  serait choisi parce que c'est plus simple, et non parce que c'est vrai.

### Exemple doctrinal

- Une automatisation **chauffage** qui lit l'état des **ouvertures** pour
  décider du chauffage reste **chauffage** : son propriétaire fonctionnel est
  le chauffage ; les ouvertures ne sont qu'une donnée d'entrée.
- Une automatisation qui **arbitre simultanément** chauffage, présence,
  ouvertures, énergie et mode maison, **sans domaine dominant**, peut relever
  de `transversal`.

### Justification individuelle obligatoire

Chaque automatisation rattachée à `transversal` doit porter une
**justification explicite** de ce rattachement :

- dans l'en-tête du fichier (rubriques RÔLE / PÉRIMÈTRE / AUTORITÉ,
  cf. [`11_automations.md`](../00_structure_includes/11_automations.md)) ;
- vérifiable au regard des critères d'entrée ci-dessus.

Une entrée en `transversal` **non justifiée** est non conforme,
même si l'automatisation est réellement interdomaines.

### Statut du domaine — non créé à ce jour

À la date du présent contrat, le domaine `transversal` **n'existe pas**
dans `input_select.prefix_id_select`, et **aucun préfixe ne lui est réservé
ici** (interdiction doctrinale d'inventer un préfixe hors procédure).

Sa création éventuelle :

- est conditionnée au **résultat de l'audit du corpus** (cf. § Conséquences — Audit) ;
- suit **exclusivement** la procédure de création de domaine de
  [`id_automatisations.md`](./id_automatisations.md)
  (ajout explicite dans `prefix_id.yaml`, préfixe numérique unique à 4 chiffres) ;
- exige une **validation explicite** du propriétaire du système.

---

## 🛑 INTERDICTIONS

Il est strictement interdit :

1. **Préfixe opportuniste** — de choisir un préfixe pour sa disponibilité,
   sa lisibilité, sa proximité numérique ou toute autre commodité étrangère
   à la propriété fonctionnelle réelle.
2. **`transversal` par confort** — de rattacher à `transversal` une
   automatisation qui a un propriétaire métier identifiable, pour éviter un
   choix, une correction ou un débat.
3. **Déduction automatique naïve dossier → préfixe** — de déduire, imposer ou
   « corriger » un préfixe à partir du chemin du fichier, par quelque outil
   que ce soit (audit, CI, générateur, IA). Le dossier est un indice,
   jamais une autorité.
4. **Modification d'ID hors procédure exceptionnelle** — de modifier un ID
   (préfixe inclus) pour mettre en cohérence identité et propriété.
   L'invariant « un ID ne change jamais après création » demeure ;
   toute reprise passe par une **exception explicitement décidée, documentée
   et localisée**, sur le modèle de la clause d'exception AID-006
   (cf. [`id_automatisations.md`](./id_automatisations.md) § Exception tracée) :
   décision du propriétaire, mapping vérifié sans collision, audit des
   références, procédure runtime Home Assistant explicite (unique_id,
   registre d'entités, risque `automation.*_2`), rollback prévu.
   L'exception AID-006 est un **précédent de méthode**, pas un précédent
   de droit.
5. **Préfixe hors source de vérité** — d'utiliser ou de déclarer en exception
   un préfixe absent de `input_select.prefix_id_select`.

---

## 🔍 CONSÉQUENCES — AUDIT DU CORPUS

Le présent contrat rend exigible un **audit en lecture seule** du corpus
réel, préalable à toute mise en conformité. Cet audit doit :

- inventorier chaque automatisation : fichier, alias, ID, préfixe, domaine
  déclaré du préfixe, dossier physique, **domaine fonctionnel apparent**
  (établi par lecture du comportement, jamais du seul chemin), justification ;
- classer chaque cas : **conforme** / **transversal légitime** /
  **exception à documenter** / **ambigu** / **probablement fautif** ;
- pour tout candidat à correction d'ID, auditer les **références exactes**
  (runtime YAML, scripts, templates, Lovelace, contrats CI, documentation,
  workflows) et les références par entité `automation.*` ;
- évaluer les impacts Home Assistant avant toute proposition
  (`id` = `unique_id` d'entité : orphelinage, slugs, `automation.*_2`,
  nécessité éventuelle d'une procédure transitoire type AID-006).

L'audit **constate** ; il ne corrige pas. Toute correction relève d'une
décision explicite postérieure à l'audit.

---

## 🤖 CONSÉQUENCES — CI FUTURE

Une CI de cohérence préfixe ↔ domaine est attendue **après** le contrat,
l'audit et les éventuels alignements. Elle devra :

- prendre pour source de vérité des préfixes :
  `06_input_selects/system/prefix_id.yaml` ;
- s'appuyer sur le **registre d'exceptions opposable** (divergences
  dossier ↔ préfixe documentées, rattachements `transversal`), dont
  l'emplacement normatif est :
  `scripts/arsenal_contracts/prefix_domain_exceptions.yaml` —
  ses propriétés sont contractuelles : explicite, justifié cas par cas,
  versionné, opposable ; toute entrée exige une décision propriétaire
  explicite et tracée ;
- ne PAS implémenter de règle naïve dossier → préfixe : le dossier n'y a
  valeur que de **présomption réfutable**, levée par le registre
  d'exceptions. Mécanique exacte de résolution : la présomption s'attache
  au **dossier racine** sous `11_automations/` uniquement (les sous-dossiers
  n'ont aucune autorité) ; seule une entrée valide du registre
  (id + fichier concordants) lève la présomption ;
- distinguer :
  - **ERROR** — préfixe incohérent non couvert par une exception déclarée ;
  - **ERROR** — exception déclarée vers un préfixe inexistant dans
    `prefix_id_select` ;
  - **ERROR** — automatisation sans domaine fonctionnel résolu ;
  - **INFO/WARN** — uniquement transitoire, pour des cas à documenter ;
    aucune tolérance permanente ;
- ne produire **aucun faux positif connu** sur le corpus aligné.

La CI vérifie la **conformité au présent contrat**, pas une approximation :
en cas d'écart entre la règle implémentée et le contrat, c'est
l'implémentation qui est fausse.

---

## 📌 STATUT

Document d'architecture Arsenal
**Normatif et opposable**

Toute dérogation doit être :

- explicitement décidée
- documentée
- localisée
