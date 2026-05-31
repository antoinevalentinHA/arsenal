# Plan d'action Arsenal — Durcissement des agrégats `temperature_min/max_chambres`

> Statut : plan d'action — non normatif tant que non promu en contrat
> Portée : couche d'agrégation thermique intérieure (`sensor.temperature_min_chambres`,
>          `sensor.temperature_max_chambres`)
> Origine : audit officiel « Températures intérieures / façades thermiques internes »
>           + note de validation du risque réel
> Hypothèses admises : façades par zone saines, consommateurs sains, problème
>           circonscrit à la couche d'agrégation
> Principe directeur : « le runtime est la référence, le contrat documente le runtime »

---

## Préambule — correction de cohérence (nommage du contrat de fallback)

- Le contrat commun de fallback cible s'appellera **`fallback.md`**.
- Le nom de fichier `contrat_fallback.md` **n'est pas** retenu comme nom de fichier cible.
- Tous les renvois documentaires futurs devront pointer vers **`fallback.md`**.

---

## 1. Décision architecturale cible

**Séparer deux canaux sur l'agrégat : la valeur (inchangée) et la confiance (nouvelle).**

- **Canal valeur** — continuité bornée : `sensor.temperature_min_chambres` /
  `sensor.temperature_max_chambres` continuent de republier la dernière valeur
  connue. Tant que l'on reste dans le TTL, **le comportement métier de chauffage /
  climatisation / aération est strictement identique à aujourd'hui** — c'est
  l'exigence centrale.
- **Canal confiance** — bornage par TTL : un statut + un âge mémoire signalent quand
  la valeur publiée est « fraîche », « mémoire » ou « périmée ». Ce canal **ne touche
  pas la valeur** ; il la qualifie.

Ce schéma reprend exactement la doctrine déjà en place pour l'extérieur
(`sensor.temperature_jardin` + `sensor.temperature_jardin_statut`) : valeur et statut
sont deux entités/canaux distincts. **L'abstention brutale n'est pas la cible**
(réponse Q1) : faire passer l'agrégat à `unknown` propagerait `cible = neutre` au
chauffage (arrêt d'ajustement), ce que la note de risque a écarté. La bascule
éventuelle vers une abstention au-delà du TTL est **différée en arbitrage** (§4), car
elle, et elle seule, modifierait le métier.

---

## 2. Lots proposés

**Lot 1 — Contrat d'agrégation (gouvernance, risque runtime nul).**
Créer le contrat aujourd'hui absent qui régit `temperature_min_chambres` /
`temperature_max_chambres` : rôle de **référence de décision**, politique de
**continuité bornée** (et non d'abstention), TTL, statut, alerte. Le contrat doit
**acter explicitement la divergence assumée** avec
`temperature_interieure/consolidation.md §6` (qui, lui, impose l'abstention) : la
couche d'agrégation est un rôle différent (référence métier) justifiant une
continuité, là où la couche consolidation impose l'abstention. Référencer le contrat
commun de fallback `fallback.md` (à créer, voir préambule) comme cadre commun.

**Lot 2 — TTL & fraîcheur (runtime additif, comportement métier inchangé).**
Doter l'agrégat d'un **TTL spécifique, plus court que le TTL des façades**
(réponse Q2). Justification : la péremption par zone (1800 s dans
`consolidation.yaml`) est **déjà absorbée en amont** ; recompter 1800 s au niveau
agrégat cumulerait jusqu'à ~60 min de gel avant tout signal. Le TTL agrégat doit
mesurer **la durée depuis que les trois façades sont simultanément indisponibles**,
en réutilisant le **pattern de fraîcheur déjà déployé pour l'humidité**
(`input_datetime.humidite_relative_last_valid_ts_<zone>`, changelog v12.1.1). Valeur
numérique exacte → arbitrage §4.

**Lot 3 — Observabilité du gel (diagnostic, additif).**
Rendre le gel visible (réponse Q3), par ordre de footprint croissant :
- **Minimal** : exposer `âge mémoire` + `mode` (sur le modèle
  `mode_resolution`/`source_active` de la consolidation) **en attributs des entités
  existantes** — aucune nouvelle entité.
- **Si un signal consommable est requis** pour l'alerte/la carte : un compagnon
  statut, justifié par **symétrie avec `sensor.temperature_jardin_statut`** (entité
  nouvelle mais motivée). À trancher (§4).
- **Notification** : une automatisation d'alerte quand les trois façades sont
  indisponibles au-delà du TTL, branchée sur le système existant
  (`contrats/notifications.md`). Nouvelle automatisation justifiée : l'observabilité
  est l'objet même du durcissement.

**Lot 4 — UI (diagnostic, faible risque).**
Étendre les cartes **existantes** `carte_temperature_min_chambres` /
`carte_temperature_max_chambres`
(`19_button_card_templates/40_dashboards/arsenal/30_diagnostic/`) pour restituer
l'état `mémoire`/`périmé` — sans nouvelle entité ni nouvelle carte.

**Lot 5 — Tests de validation (préalable à toute implémentation).**
Voir Q5 / §5 (critères de clôture).

---

## 3. Risques

- **Risque principal — régression silencieuse du métier.** Toute écriture sur
  `chambres/min/valeur.yaml` / `chambres/max/global/valeur.yaml` (et la variante
  `chambres/max/rdc/valeur.yaml`) touche la référence de décision. Mitigation : Lots
  2-3 ne changent **que** le canal confiance ; la valeur reste identique dans le TTL.
  Tout changement du canal valeur (abstention) est exclu de ce plan.
- **Risque de double comptage de TTL** si l'on réutilise naïvement 1800 s → traité
  par le choix d'un TTL agrégat court fondé sur « durée d'indisponibilité
  simultanée ».
- **Risque de bruit d'alerte** (notification trop sensible) → délai de grâce à
  calibrer (§4).
- **Risque de prolifération d'entités** → priorité aux attributs sur entités
  existantes ; compagnon statut seulement si justifié.

---

## 4. Arbitrages humains

1. **Bascule au-delà du TTL** : la valeur reste-t-elle en continuité indéfinie (canal
   confiance seul), ou bascule-t-elle en abstention après un second seuil ? (Seule
   option modifiant le métier → décision explicite requise, par domaine.)
2. **Valeur du TTL agrégat** : seuil court fondé sur l'indisponibilité simultanée —
   quelle durée ?
3. **Statut : attribut ou entité compagnon ?** Minimal (attributs) vs symétrie avec
   `temperature_jardin_statut` (entité dédiée).
4. **Délai de grâce de la notification** avant alerte.
5. **Plausibilité intérieure** : réconcilier `axe_temperature.md §3` (8-40) avec le
   runtime / `consolidation.md` (5-45) — adjacent mais à traiter dans le même
   contrat.

---

## 5. Critères de clôture

- **Contrat d'agrégation** rédigé, actant la continuité bornée et sa divergence
  assumée avec `consolidation.md §6` ; renvois cohérents vers `fallback.md`.
- **Preuve de non-régression métier** (réponse Q5), en DevTools / tests de contrat,
  avant implémentation :
  - une source par zone coupée → façade `source_unique`, agrégat inchangé
    (redondance prouvée) ;
  - une zone entièrement coupée → agrégat calculé sur les deux restantes ;
  - **trois zones coupées < TTL** → valeur publiée identique **et** sorties
    identiques de `sensor.chauffage_autorisation_cible`, des `seuil_*_atteint` clim
    et de `aeration/conseillee/etage` (preuve « zéro changement métier ») ;
  - **trois zones coupées > TTL** → statut `périmé` + alerte déclenchés **sans**
    modification de la valeur d'état (Phase 1) ;
  - redémarrage HA → état sûr au démarrage, initialisation correcte de la fraîcheur.
- **Observabilité vérifiée** : le gel est désormais détectable (statut + alerte), là
  où il était invisible.
- **Aucune entité existante renommée** ; toute entité nouvelle justifiée (fraîcheur,
  statut compagnon, automatisation d'alerte).
