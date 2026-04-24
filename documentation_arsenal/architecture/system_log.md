# Arsenal — Contrat normatif
## `system_log` — Canal diagnostique

| Champ | Valeur |
|---|---|
| **Version** | 1.1 |
| **Statut** | Normatif opposable |
| **Remplace** | v1.0 |
| **Contrat jumeau** | `contrat_logbook.md` v2.1 |

---

## Principe fondamental

> Un log = un écart. Pas un commentaire de fonctionnement.

`system_log` est le canal diagnostique du système. Il signale les pertes de garantie, jamais le fonctionnement nominal.

> Une anomalie technique interne relève exclusivement de `system_log`. Les anomalies à impact fonctionnel observable relèvent du Logbook.

---

## Règle d'admission

Une écriture `system_log.write` est légitime **si et seulement si** l'événement traduit une **perte de garantie** :

- rejet d'une commande (`rejected`)
- expiration (`timeout`)
- épuisement d'un mécanisme de résilience (`retry épuisé`)
- valeur hors bornes ou incohérence détectée
- état inattendu d'une dépendance
- fallback ou comportement défensif activé

Toute écriture qui décrit le **fonctionnement nominal** est interdite.

---

## Niveaux autorisés

| Niveau | Usage | Statut |
|---|---|---|
| `error` | Garantie rompue, action requise ou impossible | Autorisé |
| `warning` | Garantie dégradée, comportement défensif activé | Autorisé |
| `info` | Information sans écart | **Interdit par défaut** |
| `debug` | Hors périmètre normatif (usage local seulement) | Hors scope |

L'usage de `info` exige une justification explicite documentée par domaine.
**`info` ne doit jamais servir à compenser un manque d'état persistant.**

---

## Test d'admission

Trois tests indépendants. **Un seul échec → exclusion.**

1. **Écart** — l'événement traduit-il une perte de garantie ?
2. **Diagnostic** — la lecture du log fournit-elle une piste actionnable au diagnostic ?
3. **Rareté** — l'occurrence est-elle exceptionnelle dans le fonctionnement nominal ?

---

## Qualité du message

Chaque entrée doit porter :

- **Quoi** — la nature de l'écart
- **Où** — domaine ou composant émetteur
- **Pourquoi** — cause identifiée ou symptôme observé
- **Contexte exploitable** — valeur(s), seuil(s), identifiant(s) utiles au diagnostic

Contrairement au Logbook, **les noms d'entités, identifiants techniques et valeurs brutes sont autorisés** — ils sont l'intérêt du canal.

---

## Responsabilité d'émission

> Un écart = un point d'émission désigné.

L'émetteur est le composant qui **détient la vérité diagnostique** de l'écart.

| Écart | Émetteur désigné |
|---|---|
| Commande rejetée par le bridge | Wrapper transactionnel |
| Timeout d'acknowledgment | Script appelant |
| Valeur hors bornes | Pipeline de perception (couche stabilisation) |
| Retry épuisé | Couche de résilience |

**Interdit :** double émission d'un même écart par plusieurs couches.

---

## Dérives interdites

- log narratif de retry (« tentative 1/3 », « tentative 2/3 ») — seul l'épuisement se logue
- log de progression (« début », « en cours », « fin »)
- log `info` « au cas où »
- log `info` servant à compenser un manque d'état persistant
- log de réussite d'une opération nominale
- log purement redondant avec un état persistant déjà exposé, sans apport diagnostique supplémentaire
- log servant de béquille à une logique manquante
- log servant de trace métier (→ relève du Logbook)

---

## Granularité diagnostique vs redondance

> Un log n'est pas redondant s'il apporte une granularité diagnostique que l'état persistant ne porte pas.

Exemple admissible :

- un helper `bridge_etat` expose « en défaut » → état persistant, suffisant pour la lecture humaine
- un log `system_log` porte simultanément `request_id=42`, `composant=ecs`, `motif=timeout_ack`, `delai=8.2s` → granularité diagnostique non portée par l'état

Cette double émission est légitime tant que le log apporte une information **exploitable au diagnostic** que l'état persistant ne contient pas.

---

## Propriété cible

> Un système silencieux par construction, pas par absence de bugs.

La densité du `system_log` est un **indicateur inverse de santé** :

- système sain → `system_log` quasi vide
- pic de logs → signal d'incident à investiguer
- log fréquent stable → défaut de conception à corriger (pas un comportement à tolérer)

---

## Frontière avec le Logbook

| Question | Canal |
|---|---|
| « Que s'est-il passé fonctionnellement ? » | Logbook |
| « Qu'est-ce qui a dérapé techniquement ? » | `system_log` |
| « Quelle est la valeur actuelle ? » | `sensor` / `helper` |
| « Pourquoi le confort a-t-il changé ? » | Logbook |
| « Pourquoi la commande n'a pas pris ? » | `system_log` |

---

## Principe final

> Le Logbook raconte ce qui s'est passé.
> `system_log` signale ce qui n'aurait pas dû.
> L'état prouve ce qui est.
