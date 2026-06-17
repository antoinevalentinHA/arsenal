# 🏗️ ARSENAL — CHANTIER
## Chauffage — Observabilité de l'auto-ajustement de la courbe

| Champ | Valeur |
|---|---|
| **Type** | Chantier |
| **Domaine** | Chauffage / Auto-ajustement courbe |
| **Statut** | Ouvert — non ordonnancé |
| **Origine** | Audit `01_rapports/chauffage/audit_auto_ajustement_courbe.md` (clôturé 2026-06-03) |
| **Priorité** | 1 (unique chantier issu de l'audit) |
| **Nature** | Observabilité — **aucun changement de comportement** |

---

> **Avancement (2026-06-17).** Capture (P1/P2) acquise ; **persistance P3 réalisée** pour les
> termes de décision (historisation Recorder minimale : entrées de garde + résultat appliqué),
> cf. [`plan d'action`](../../03_plans_action/chauffage/plan_action_observabilite_auto_ajustement_courbe.md)
> et [`spec`](../../03_plans_action/chauffage/spec_persistance_termes_decision_courbe.md). Le **« quoi/quand »**
> (valeurs appliquées + horodatage) est désormais requêtable dans l'historique HA sans SQLite.
> Le **« pourquoi »** d'une **abstention** reste porté par les événements (verdict event-only,
> cf. spec §3.4). **Chantier toujours ouvert** : P4–P9 (complétude, dérivation, effet, supervision)
> non démarrées.

## 1. Objectif

Rendre l'auto-ajustement de la courbe de chauffe **observable de lui-même** : permettre à un humain de répondre, à partir de traces durables, à quatre questions sur tout ajustement (réel ou simulé) :

1. **Quoi** a été appliqué — valeurs de pente et de parallèle avant/après.
2. **Quand** — horodatage exploitable.
3. **Pourquoi** — décision retenue, ou **raison du refus** lorsqu'un ajustement suggéré n'a pas été appliqué.
4. **Avec quel effet** — évolution ultérieure de la qualité de régulation après l'ajustement.

## 2. Justification

L'audit a établi que le système se comporte correctement mais reste **aveugle sur ses propres décisions** : les valeurs de courbe réellement appliquées, les valeurs suggérées et le motif des refus ne sont pas historisés ni lisibles, tandis que seuls quelques indicateurs de régulation (oscillation, overshoot, cycles) le sont.

Cette cécité a deux conséquences directes :

- elle rend **indécidable** la question centrale de l'audit — y a-t-il une dérive réelle de la courbe ? — faute de pouvoir reconstituer la chronologie des valeurs appliquées et la mettre en regard de la qualité de régulation ;
- elle prive de substance la **supervision humaine** que le mécanisme revendique : une « calibration supervisée » suppose un superviseur capable de voir ce qui est calibré.

L'observabilité est donc le **préalable** qui transforme tous les autres jugements de l'audit (dérive ? proxy utile ? protection suffisante ?) de spéculations en faits, et qui conditionne toute évolution future légitime de l'apprentissage.

## 3. Périmètre

- Les **grandeurs propres du domaine** auto-ajustement : pente et parallèle réellement appliqués, valeurs suggérées, et motif de décision/refus de chaque cycle.
- La **mise en regard** de ces décisions avec les indicateurs de régulation déjà mesurés (oscillation, overshoot, nombre/durée de cycles), afin de permettre une appréciation *a posteriori* de l'effet.
- La **lisibilité** de cette information pour un humain (consultation, rétrospective).

## 4. Hors périmètre

- Toute **modification du comportement** de l'auto-ajustement.
- Le **câblage de la représentativité** thermique (le signal, faible *comme proxy physique*, est **retenu comme critère métier d'éligibilité** et désormais **câblé en verrou §7/§8** ; voir contre-expertise audit §5.6 et backlog R-1).
- Toute évolution des **garde-fous** poêle / fenêtre / aération.
- Tout changement des **bornes, du pas, de la cadence ou de la bande morte**.
- La **couche d'exécution transactionnelle** (déjà saine, non rouverte).
- Toute **solution technique** : ce document définit le chantier, pas son implémentation.

## 5. Valeur métier attendue

- Passer d'un système qui se comporte bien **à l'aveugle** à un système **supervisable**.
- Rendre **vérifiable** (et non plus supposée) l'existence ou l'absence de dérive de la courbe dans le temps.
- Donner au propriétaire du système les moyens de **démontrer** — ou d'infirmer — l'efficacité de l'auto-ajustement, ce qui n'est aujourd'hui pas possible.
- Constituer le **prérequis** de toute évolution future de l'apprentissage (y compris l'éventuelle reprise de la question de représentativité sur un meilleur signal).

## 6. Risques traités

| Risque (issu de l'audit) | Effet de l'observabilité |
|---|---|
| Auto-ajustement aveugle sur ses propres variables (**Important**) | Traité directement : les décisions deviennent reconstituables. |
| Dérive de courbe indécidable faute de preuves | Rendue mesurable : la chronologie applicable est conservée. |
| Supervision revendiquée mais non instrumentée | Rendue effective : le superviseur dispose enfin du nécessaire. |

## 7. Critères de succès

Le chantier est réussi si, **sans avoir modifié le comportement** du système, un humain peut :

1. reconstituer la **chronologie des valeurs de courbe appliquées** sur une période donnée ;
2. retrouver, pour chaque ajustement, la **valeur suggérée** et la **raison** de son application ou de son refus ;
3. mettre cette chronologie **en regard de la qualité de régulation** observée ensuite ;
4. répondre, sur données et non par hypothèse, à la question : *« la courbe a-t-elle dérivé, et un ajustement donné a-t-il amélioré la régulation ? »*

## 8. Dépendances éventuelles

- S'appuie sur les indicateurs de régulation **déjà existants** (oscillation, overshoot, cycles) ; n'en crée pas de nouveaux dans son périmètre.
- Indépendant de la couche d'exécution et de la décision centrale : aucune de leurs logiques n'est touchée.
- **Aucune dépendance** envers la représentativité ni envers les garde-fous contextuels (volontairement hors périmètre).

---
*Chantier défini à partir des conclusions de l'audit clôturé du 2026-06-03. Définition uniquement — aucune solution technique.*
