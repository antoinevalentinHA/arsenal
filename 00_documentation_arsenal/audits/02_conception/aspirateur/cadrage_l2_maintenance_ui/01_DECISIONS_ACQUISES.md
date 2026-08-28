# Registre des décisions opérateur acquises — **V3**

> **Contenu inchangé depuis la V1.** Aucune décision n'a été ajoutée, retirée
> ni modifiée par les corrections d'audit. Décompte de référence au §G.

Ces décisions sont **prises**. Elles ne sont pas rouvertes par le présent
cadrage et ne figurent pas parmi les arbitrages ouverts.
Elles n'ont **aucune traduction dans le dépôt** à ce jour : aucune n'est
implémentée.

---

## A. Conduite et supervision (lot L2)

| Réf. | Décision |
|---|---|
| **D-01** | Le geste de conduite passe par un script dédié, rôle `script.aspirateur_conduire_mission`. |
| **D-02** | Quatre gestes, et quatre seulement : **pause, reprise, arrêt, retour à la base**. |
| **D-03** | Une automation de supervision, intitulée `Aspirateur - Supervision de mission`. |
| **D-04** | Son identifiant est `10280000000001`. |
| **D-05** | **Aucun identifiant supplémentaire n'est inventé.** Tout identifiant nouveau est attribué par l'opérateur. |
| **D-06** | **Aucune mission externe n'est adoptée.** Une activité du robot non ouverte par Arsenal n'est jamais supervisée ni reprise. |
| **D-07** | La **reprise** n'est autorisée que pour une **mission Arsenal ouverte**. |
| **D-08** | Le **verdict persistant** sert de **mémoire de supervision**. |
| **D-09** | **Trois writers** du verdict, à **ensembles de valeurs exactes disjoints**. La disjonction porte sur les valeurs, **pas** sur les préfixes : aucun writer n'est tenu de posséder un préfixe exclusif. |
| **D-10** | `CLOTURE/APRES_ARRET_NON_CONFIRME` et `CLOTURE/APRES_RETOUR_NON_CONFIRME` sont **distincts** et **terminaux**. |
| **D-11** | Les codes du catalogue sont **conservés tels quels**. Il est interdit de leur substituer des préfixes plus commodes pour la CI. Sont notamment conservés : `ECHEC/MISSION_INTERROMPUE`, `ECHEC/ERREUR_EN_MISSION`, `CLOTURE/APRES_ARRET_NON_CONFIRME`, `CLOTURE/APRES_RETOUR_NON_CONFIRME`. |

### Règles de redémarrage — acquises

| Réf. | Règle |
|---|---|
| **D-R1** | Ne **jamais inventer** une transition non observée. |
| **D-R2** | **Poursuivre** une chaîne de retour déjà qualifiée dans le verdict. |
| **D-R3** | **Clôturer honnêtement** une chaîne devenue opaque. |
| **D-R4** | Ne **jamais adopter** une mission externe. |
| **D-R5** | Ne **jamais réarmer** depuis un verdict terminal périmé. |

---

## B. Vidage du bac

| Réf. | Décision |
|---|---|
| **D-12** | **Le dock vide physiquement et automatiquement le bac**, en dehors des heures interdites configurées. Les 608 cycles relevés sont cohérents avec ce fonctionnement réel. *Déclaration opérateur — même régime de preuve que `ARB-3` et `ARB-5` du contrat.* |
| **D-13** | Le vidage **n'est pas un geste physique** de l'opérateur. C'est une **fonction native autonome** du couple robot/dock. |
| **D-14** | Le vidage est **retiré de la V1 Maintenance** et déclaré **non bloquant**. |
| **D-15** | **Aucun** bouton, script, commande brute ou lot Arsenal de vidage n'est créé. |
| **D-16** | Arsenal pourra **seulement observer et notifier** une erreur de dock ou de vidage, **si** un signal fiable existe. |
| **D-17** | `dustCollectionWorkTimes` **ne doit pas** être utilisé comme compteur de durée de vie d'un sac. |
| **D-18** | L'absence de primitive Home Assistant confirmable **n'est plus un manque fonctionnel** pour la V1. |
| **D-19** | Aucune entité ni compteur maison ne sera créé pour le bac. |

---

## C. Périmètre Maintenance V1

| Réf. | Décision |
|---|---|
| **D-20** | Périmètre exact : **filtre**, **brosse principale**, **brosse latérale**, **nettoyage des capteurs**. |
| **D-21** | **Notification persistante agrégée** pour l'entretien. |
| **D-22** | **Déclaration explicite** de l'opérateur après entretien physique. |
| **D-23** | **Remise à zéro unique**, suivie d'une **confirmation par relecture**. |
| **D-24** | **Aucune remise à zéro automatique.** |
| **D-25** | **Aucune répétition automatique.** |

---

## D. Notifications

| Réf. | Décision |
|---|---|
| **D-26** | Mission en cours → notification **persistante temporaire**. |
| **D-27** | Entretien requis → notification **persistante durable agrégée**. |
| **D-28** | Erreur ou interruption urgente → **notification mobile opérateur**. |
| **D-29** | **Aucune notification mobile** pour une échéance normale d'entretien. |
| **D-30** | **Aucun helper d'acquittement ni de report** pour l'instant. |

---

## E. Interface

| Réf. | Décision |
|---|---|
| **D-31** | La carte NAS du dashboard Navigation est **remplacée** par la carte Aspirateur. |
| **D-32** | L'accès NAS est **déplacé** dans le dashboard Système, avec une carte récapitulative et un raccourci vers le dashboard NAS existant. |
| **D-33** | **Aucun dashboard Aspirateur dédié.** |
| **D-34** | **Aucun hub documentaire Aspirateur.** |
| **D-35** | **Aucune entrée Aspirateur Tier 1** dans la carte des domaines. |
| **D-36** | La carte Navigation doit permettre **à terme le lancement**, pas seulement la lecture et la conduite. |

---

## F. Discipline de session

| Réf. | Décision |
|---|---|
| **D-37** | Le cadrage est traité comme un **livrable opposable antérieur à toute implémentation**. |
| **D-38** | La préparation du lot combiné est **interrompue** tant que le cadrage n'est pas audité. |
| **D-39** | Aucune écriture de dépôt, aucune commande Home Assistant, aucune notification, aucune commande robot. |

---

## G. Décompte de référence

Ce décompte est la **source de vérité** des compteurs cités ailleurs dans
l'artefact. Il est vérifiable par simple lecture du présent fichier.

| Bloc | Références | Nombre |
|---|---|---|
| A — Conduite et supervision | `D-01` → `D-11` | 11 |
| A — Règles de redémarrage | `D-R1` → `D-R5` | **5** |
| B — Vidage du bac | `D-12` → `D-19` | 8 |
| C — Périmètre Maintenance V1 | `D-20` → `D-25` | 6 |
| D — Notifications | `D-26` → `D-30` | 5 |
| E — Interface | `D-31` → `D-36` | 6 |
| F — Discipline de session | `D-37` → `D-39` | 3 |

**Décisions `D-xx` : 39. Règles `D-Rx` : 5. Total : 44.**
**Vidage et Maintenance réunis (`D-12` → `D-25`) : 14.**

> **Correction V2.** Le manifeste de la V1 annonçait « 12 acquises pour le
> vidage et la maintenance, 36 au total ». Les deux compteurs étaient faux.

---

## Note de traçabilité

Les décisions **D-12 à D-19** corrigent une qualification erronée d'une version
antérieure du cadrage, qui présentait le vidage comme un geste physique opéré
par l'humain. Cette qualification est **retirée**.

**La V2 n'ajoute, ne retire et ne modifie aucune décision.** Les corrections
issues de l'audit portent exclusivement sur des **propositions**, des **faits**
et des **arbitrages** — jamais sur ce registre. En particulier, aucun des six
arbitrages ajoutés (`A-9` à `A-14`) n'a été transformé en décision.
