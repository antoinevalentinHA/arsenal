# Plan d'action vivant — Chantier arrosage

> **NON NORMATIF — boussole de livraison.** Ce document **oriente le chantier** arrosage jusqu'à sa **complétude** (le domaine est déjà publié incrémentalement, v16.2 / v16.3 ; reste à le rendre complet) ; il ne définit aucune règle. En cas de divergence, **les contrats du domaine font foi** ([`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md)).
>
> **Ce n'est pas** : un changelog, une release note, un contrat normatif, un journal de PR, un backlog fourre-tout, ni une liste d'idées. Le **cockpit d'état** reste le registre, ligne **C10** ([`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)) ; ce plan ne le duplique pas.
>
> **Vivant** : à **relire avant chaque lot** et **mettre à jour après chaque lot** ; à **clôturer ou remplacer** quand le domaine est livré.

## Vocabulaire (à ne pas confondre)

| Terme | Sens dans ce plan |
|---|---|
| **mergé** | code intégré à `main`, CI verte — n'implique ni publication ni validation terrain |
| **durci** | comportement renforcé (fail-safe, fraîcheur, explicabilité) sur un acquis déjà mergé |
| **publié** | inscrit dans un **changelog de release** Arsenal — **fait** : releases **v16.2** (observation v0) et **v16.3** (V1 + durcissements) |
| **livré** | le domaine est **complet** — manques (§5) résorbés et validations terrain faites — au point d'être exploitable sans ambiguïté (cf. §3) — **pas encore atteint** |

---

## 1. Cadre et statut

- Document **non normatif** : il aide à **décider**, il ne prescrit pas. Tout lot futur sera **audité avant tout YAML** (contrats avant runtime).
- Les **contrats priment** : ce plan **pointe** vers eux sans les réécrire.
- Le **registre C10** reste le cockpit **synthétique** d'état ; ce plan en est le détail de pilotage, séparé.
- **Ce n'est pas un changelog** : aucun commit n'est journalisé ici ; aucune release n'est préparée par ce document.

## 2. État actuel réel

- **V1 runtime mergée** (décision besoin sol → intention → exécution déléguée au script Run supervisé).
- **Durcissements post-V1 mergés**, portant sur UI/réglages, observabilité décisionnelle, fraîcheur, coexistence fail-safe et explicabilité de l'intention.
- **Publié incrémentalement** : releases **v16.2** (observation v0 + pré-runtime) et **v16.3** (V1 automatique + durcissements).
- **Domaine non encore complet** : publié **≠** complet. Les manques (§5) restent à résorber ; c'est précisément ce plan qui trace le chemin restant.

## 3. Objectif de livraison

« **Livrer** » le domaine arrosage = pouvoir l'inclure dans une **release Arsenal sans ambiguïté**, c'est-à-dire :

- runtime **cohérent** ;
- UI **exploitable** par l'opérateur ;
- diagnostic **compréhensible** (dont la santé du pont) ;
- **notifications utiles arbitrées** (signal vs bruit tranché) ;
- **validations terrain minimales** effectuées ;
- **aucune dette bloquante** connue.

> Le domaine est déjà **publié** incrémentalement (v16.2 / v16.3) ; chaque incrément l'est **dans le changelog de sa release** (co-commit). « Livrer » ne désigne donc pas la première publication mais la **complétude** : l'atteinte des critères ci-dessus, **conditionnée** à leur réalisation, pas à une date.

## 4. Acquis (haut niveau, sans détail PR par PR)

- **Décision / action V1** : socle besoin → intention → exécution supervisée ([`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)).
- **Coexistence Rain Bird** gouvernée, direction de défaillance vers le secours ([`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md)).
- **Fraîcheur du pont** corrigée et fondée sur `bridge_uptime.last_reported` (référence temporelle de liveness alignée sur la doctrine repo-wide).
- **Intention explicable** par `motif` + `categorie` (attributs lecture seule, sans changer l'état).
- **Observabilité / historisation de base** de la chaîne de décision (Recorder).
- **UI et découvrabilité déjà amorcées** : réglages, cartes, hub de domaine et `carte_domaines` réconciliés.

## 5. Manques avant livraison

- **UI opérateur à finaliser** : l'exploitation quotidienne doit être lisible et complète.
- **Diagnostic explicable à compléter**, notamment la **santé du pont** (pourquoi disponible/frais ou non).
- **Notifications utiles à arbitrer** : quoi notifier, quand, et ce qui serait du bruit.
- **Validations terrain à effectuer** : arrosage réellement déclenché, comportement sur la durée.
- **Lisibilité du verdict d'arrosage / historique opérateur** : pouvoir relire *pourquoi* le système a arrosé ou s'est abstenu.
- **Clarté sur les conditions de livraison** : savoir, à un instant donné, ce qui reste réellement bloquant.

## 6. Lots candidats priorisés (non prescriptif)

Quelques **axes ordonnés**, pas un backlog. Chaque lot sera **audité avant YAML** ; l'ordre est indicatif.

1. **UI d'exploitation / lisibilité de l'intention** — rendre l'état et le `motif`/`categorie` exploitables par l'opérateur.
2. **Diagnostic pont explicable** — surface lisible de la santé/fraîcheur du pont.
3. **Notifications** — un jeu **minimal et utile**, une fois l'arbitrage signal/bruit tranché (§7).
4. **Validations terrain** — exécuter le minimum nécessaire (§8) et en consigner le verdict.
5. **Complétude / clôture du chantier** — quand les critères du §3 sont réunis ; chaque lot d'ici là est **publié dans le changelog de sa release** (co-commit), pas accumulé pour un changelog final.

## 7. Questions ouvertes (à trancher avant livraison)

- Quelles **notifications** sont réellement utiles, lesquelles seraient du **bruit** ?
- Quel **niveau d'explicabilité UI** est **suffisant** pour livrer (sans sur-ingénierie) ?
- Quelles **validations terrain** sont **nécessaires** (vs souhaitables mais non bloquantes) ?
- Quels **signaux** permettent d'affirmer que le domaine est **publiable** ?

## 8. Validations terrain nécessaires

**Acquis terrain (prudents)** — observés après correction de fraîcheur du pont :

- pont Rain Bird **exploitable** après correction de fraîcheur ;
- `pont_donnees_disponibles = on` ;
- `pont_donnees_fraiches = on` ;
- source d'horloge = `bridge_uptime.last_reported` ;
- âge d'uptime **cohérent** après reload HA.

> **Ces acquis ne valent pas validation complète du domaine.** Restent à valider : l'**arrosage effectif**, le **comportement sur la durée**, l'**UI opérateur** et les **notifications**. Cadre des validations : Phase 0 terrain et pré-requis runtime ([`07_phase_0_terrain.md`](../../../contrats/arrosage/07_phase_0_terrain.md), [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)).

## 9. Éléments explicitement différés

Hors périmètre de la **première** livraison (différés, **non bloquants**) :

- calibration avancée ;
- auto-tuning ;
- modulation climatique sophistiquée ;
- multi-zone ;
- dead-man switch complet ;
- évolutions agronomiques lourdes.

> Ces sujets restent légitimes **plus tard** ; ils ne conditionnent pas la première release du domaine.

## 10. Règles de mise à jour

- **Relire** ce plan **avant chaque lot**.
- **Mettre à jour** ce plan **après chaque lot** (état, manques, questions tranchées).
- **Ne pas** y inscrire tous les commits ; **ne pas** en faire un changelog.
- Maintenir le **registre C10 synthétique** (ce plan porte le détail, pas le cockpit).
- **Clôturer ou remplacer** ce plan **quand le domaine est livré**.

---

*Plan d'action vivant — non normatif. Couvre le chemin jusqu'à la complétude du domaine arrosage (déjà publié incrémentalement, v16.2 / v16.3), pas sa trajectoire long terme. Cockpit d'état : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C10). Doctrine du domaine : [`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md).*
