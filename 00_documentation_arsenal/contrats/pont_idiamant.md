# Contrat — Pont iDiamant (volets) : supervision et remédiation

**Arsenal** · Couche domaine · v1.2 — 2026-08-24

---

## Objet

Ce contrat définit la **politique de remédiation** du pont de volets iDiamant
(passerelle commerciale Netatmo / Legrand, accessoire HomeKit « Prise Control »).

Il répond à une question que ni la supervision réseau ni la résilience générique
des intégrations ne tranchent :

> *Quand le pont ne répond plus applicativement, quelle action Arsenal est-il
> autorisé à entreprendre, dans quel ordre, et jusqu'où ?*

Il **lève la réserve §14.1** de [`resilience_integrations.md`](resilience_integrations.md),
qui déclarait la remédiation physique hors de son propre ressort et en attente
d'un contrat de domaine.

---

## 1. Périmètre

| Élément | Valeur |
|---|---|
| **Équipement** | Pont iDiamant — passerelle commerciale, boîte noire (cf. [`architecture/volets.md`](../architecture/volets.md) §3) |
| **Entrée de configuration** | `homekit_controller`, libellé « Prise Control » |
| **Périmètre d'entités** | `group.homekit_prise_control` — les 4 `cover.*` du pont |
| **Alimentation** | `switch.prise_palier` — prise Zigbee commandée, **secteur direct, non secourue** (cf. [`architecture/infrastructure_puissance.md`](../architecture/infrastructure_puissance.md)) |
| **Sonde réseau** | `binary_sensor.idiamant` (Ping) |
| **Classe réseau** | `local_lan` |

### Hors périmètre

- Les règles métier des volets (fermeture pluie, autorisations) — propriété de
  [`volets_pluie.md`](volets_pluie.md).
- Les stations météo Netatmo, qui ont leur propre politique dans
  [`homekit_diagnostic.md`](homekit_diagnostic.md) §9.1.
- La détection elle-même — propriété de [`resilience_integrations.md`](resilience_integrations.md) :
  ce contrat **consomme** les axes, il n'en définit aucun.

---

## 2. Le mode de défaillance à traiter

Le pont présente un mode de panne **déjà documenté** avant ce contrat
([`architecture/volets.md`](../architecture/volets.md) §7) :

> « iDiamant répond au ping tout en étant planté applicativement. »

Observable :

- `binary_sensor.idiamant` reste `on` — la pile IP répond ;
- l'entrée de configuration reste en `setup_retry` — le service HAP ne complète
  plus l'établissement de session ;
- les `cover.*` deviennent et restent `unavailable` ;
- Home Assistant **réessaie nativement**, sans succès, indéfiniment.

> **R-PONT-1 (opposable).** Le ping ne prouve rien sur la santé applicative du
> pont. Il ne doit jamais servir ni à déclencher, ni à inhiber une remédiation
> de ce contrat.

---

## 3. Ce que le rechargement logiciel peut et ne peut pas

Un `reload_config_entry` **réinitialise le client** Home Assistant. Il ne touche
pas au pont.

> **R-PONT-2 (opposable, fondée sur preuve terrain — §7).** Lorsque le pont est
> figé applicativement, **aucune relance logicielle ne le réveille**. Le reload
> d'entrée est de la même classe d'action que le réessai natif de Home Assistant,
> qui a déjà échoué de façon répétée avant qu'Arsenal n'intervienne.

Le reload conserve néanmoins une valeur : il **résout d'autres classes de panne**
(état client corrompu, session désynchronisée) et il est peu coûteux. Il reste
donc le **premier échelon**, mais il doit être **borné bas** : au-delà de quelques
tentatives, son échec cesse d'être une information nouvelle.

---

## 4. Politique de remédiation — escalade bornée

L'escalade comporte **deux échelons et un seul palier de franchissement**.

| Échelon | Action | Déclenchement | Borne |
|---|---|---|---|
| **1 — logiciel** | `reload_config_entry` de l'entrée | Axes de `resilience_integrations.md` (fraîcheur, disponibilité, échec de configuration) | Backoff et plafond du script canon |
| **2 — physique** | Power-cycle de `switch.prise_palier` | **2 tentatives de reload infructueuses** | **Tir unique par épisode** |

> **R-PONT-3 (opposable).** L'échelon 2 est franchi lorsque le compteur de
> tentatives de reload atteint **2**. Ce seuil est un arbitrage explicite : il
> place l'action efficace à environ trente minutes du début de l'incident, au
> lieu des deux heures et demie qu'imposerait l'attente du plafond de 5.
> Les volets sont un équipement d'usage quotidien ; l'indisponibilité prolongée
> a un coût réel.

> **R-PONT-4 (opposable — anti-boucle).** Le power-cycle est **unique par
> épisode**. Le compteur de tentatives n'est **jamais** remis à zéro par
> l'escalade : le laisser courir garantit que le franchissement du palier ne
> peut pas se reproduire dans le même épisode.
> Un épisode se termine de deux façons, et de deux seulement :
> - par un **retour OK** constaté, qui remet naturellement le compteur à zéro ;
> - par le **blocage** au plafond du script canon, qui arrête toute relance.
>
> Aucune autre sortie n'est autorisée. En particulier, il est **interdit** de
> remettre le compteur à zéro après un power-cycle : cela rouvrirait le palier
> et créerait une boucle de coupures électriques.

> **R-PONT-5.** L'action physique est déléguée au script utilitaire existant
> `script.reboot_netatmo`, paramétré par la prise. Ce script est générique par
> conception (« un seul script, zéro duplication ») ; son nom est historique et
> ne restreint pas son périmètre. Aucun second script de power-cycle ne doit
> être créé.

---

## 5. Gardes

L'échelon 2 n'est exécuté que si **toutes** ces conditions sont réunies.

| Garde | Motif |
|---|---|
| `input_boolean.systeme_stable = on` | Un incident observé pendant l'instabilité post-démarrage est un artefact d'initialisation, pas une panne. |
| `binary_sensor.panne_secteur_en_cours = off` | `switch.prise_palier` est en **secteur direct, non secourue**. Pendant une coupure, l'indisponibilité du pont est un **KO attendu** et la prise n'est de toute façon pas commandable. Couper puis rallumer serait futile. |
| **Incident encore constaté** | Le palier peut être franchi alors que le pont vient de revenir. Couper l'alimentation d'un équipement sain est une régression. L'action exige donc que l'indisponibilité franche **ou** l'échec de configuration soit toujours actif au moment d'agir. |

### 5.1 Garde explicitement écartée — accès externe

> **R-PONT-6 (opposable).** La condition `binary_sensor.acces_externe = on`,
> présente dans la politique des stations Netatmo, **ne doit pas** être reprise ici.
>
> Les stations dépendent d'un support **cloud** ; le pont iDiamant est
> **`local_lan`** — son service HAP est local. Reprendre cette garde par
> mimétisme inhiberait la remédiation d'un équipement local sur un signal WAN,
> ce que [`resilience_integrations.md`](resilience_integrations.md) §6 interdit
> explicitement.
>
> Cette exclusion est **délibérée et opposable** : elle doit survivre à toute
> relecture qui chercherait à « aligner » les deux politiques.

---

## 6. Interdictions

- Déclencher un power-cycle sur la seule foi du ping (R-PONT-1).
- Déclencher plus d'un power-cycle par épisode (R-PONT-4).
- Remettre le compteur de tentatives à zéro depuis l'escalade (R-PONT-4).
- Inhiber ce contrat sur un signal WAN (R-PONT-6).
- Couper l'alimentation pendant une panne secteur (§5).
- Créer un second script de power-cycle (R-PONT-5).
- Définir un axe de détection dans ce contrat : la détection appartient à
  `resilience_integrations.md`, ce contrat n'en est que le consommateur.
- Réimplémenter quoi que ce soit du protocole du pont : c'est une boîte noire
  ([`architecture/volets.md`](../architecture/volets.md) §6).

---

## 7. Leçon terrain — 2026-08-23 / 2026-08-24

Épisode ayant fondé ce contrat.

| Horodatage (local) | Événement |
|---|---|
| 2026-08-23 14:57 | L'entrée passe en `setup_retry`. Les 4 `cover.*` deviennent `unavailable`. |
| 23/08 → 24/08 | Home Assistant réessaie nativement pendant **plus de 25 heures**. Aucun succès. Aucune alerte : rien dans Arsenal ne surveillait cette entrée. |
| 24/08 11:14:47 | Première remédiation Arsenal : `reload_config_entry`. **Échec** — attente de 3 minutes expirée, volets toujours `unavailable`. |
| 24/08 ~11:26 | **Coupure manuelle de la prise pendant quelques secondes, puis remise sous tension.** |
| 24/08 ~11:27 | Le pont revient. L'entrée se charge. Les 4 `cover.*` repassent à `closed`, âge des données à 0. |

### Conclusions verrouillées

```
1. plus de 25 h de réessais logiciels natifs n'ont pas récupéré le pont
2. un reload d'entrée supplémentaire n'a rien changé
3. une coupure d'alimentation de quelques secondes a suffi
4. la remédiation efficace agit sur l'ACCESSOIRE, pas sur le client
```

Ces conclusions ne sont pas une découverte : elles **confirment** ce que
[`homekit_diagnostic.md`](homekit_diagnostic.md) §11 avait déjà verrouillé pour
les stations, et ce que le commentaire de `11_automations/meteo/reboot_station/*`
énonçait déjà — *« aucune relance logicielle ne le réveille, seul un power-cycle
récupère »*. Le présent contrat étend au pont une politique dont la validité
était établie, et dont seule l'application au pont manquait.

### Réserve — efficacité du reload non départagée

L'épisode ne permet pas de dire si le reload aurait fini par réussir après 3, 4
ou 5 tentatives : la coupure manuelle est intervenue avant. **Réserve
opportuniste** au sens de [`solvabilite_probatoire.md`](../architecture/03_doctrines/solvabilite_probatoire.md) §3 —
**non bloquante**, la preuve dépendant d'une occurrence non provocable. Elle ne
change pas la politique : le seuil de 2 est un arbitrage de coût
d'indisponibilité (R-PONT-3), pas une affirmation sur le nombre exact de reloads
nécessaires.

---

## 8. Limites connues

### 8.1 Latence d'observation de l'axe 3

L'axe « échec de configuration » est observé par un capteur à réveil périodique
(5 minutes), parce que la source de la preuve n'émet aucun événement
([`resilience_integrations.md`](resilience_integrations.md) R-AXE3-4).

Conséquence, **dans les deux sens** :

- l'entrée d'incident est vue avec un retard pouvant aller jusqu'à un tick ;
- la **sortie** d'incident aussi : après un retour effectif du pont, l'état
  d'entrée peut rester affiché en échec jusqu'au tick suivant.

Cette latence a été **observée** le 2026-08-24 à 11:27:53 : les volets étaient
revenus (`closed`, âge 0, indisponibilité retombée) alors que l'état d'entrée
lisait encore `setup_retry`.

> **R-PONT-7.** Cette latence est **bornée et acceptée**. Elle ne peut retarder
> qu'un **nettoyage** (remise à zéro du compteur, annulation du backoff), jamais
> provoquer une action indue : les gardes du §5 exigent un incident **encore
> constaté**, et l'axe disponibilité, lui, est réactif.
>
> En conséquence, la garde « incident encore constaté » **ne doit pas** reposer
> sur le seul axe 3, dont la lecture peut être périmée.

### 8.2 Compteur de tentatives non remis à zéro — course avec le backoff

Le binaire de retour OK du script canon exige un **recovery en cours** (timer de
backoff actif) maintenu pendant une temporisation de 2 minutes. Si la reprise
survient **moins de 2 minutes avant l'expiration du backoff**, la temporisation
est interrompue par la retombée de `recovery_en_cours` : le retour OK n'est
jamais prononcé, et le **compteur de tentatives n'est pas remis à zéro**.

**Observé le 2026-08-24** : reprise vers 11:26:30, backoff expirant à 11:27:57 —
le débounce de 2 minutes a été coupé à environ 90 secondes. Le compteur est resté
à 1 alors que l'épisode était clos.

> **R-PONT-8.** Ce défaut appartient au **patron canon** de
> [`resilience_integrations.md`](resilience_integrations.md) (invariant 5, retour OK
> conditionné à un recovery en cours) et affecte **toutes** les chaînes, pas
> seulement celle-ci. Il n'est pas corrigé par le présent contrat.
>
> Conséquence pour l'escalade : un compteur resté à 1 fait franchir le palier
> après **un seul** reload de l'épisode suivant au lieu de deux. C'est une
> **dégradation de l'arbitrage R-PONT-3, pas une atteinte à la sécurité** : la
> garde « incident encore constaté » (§5) interdit toujours de couper
> l'alimentation d'un pont sain, et le tir reste unique (R-PONT-4).
>
> **Réserve différée solvable, non bloquante.** Propriétaire : le patron canon.
> Critère de levée : correction du retour OK au niveau du script canon, de façon
> à ce qu'une reprise survenue pendant le backoff soit constatée même si le timer
> expire pendant la temporisation.
>
> ✅ **LEVÉE le 2026-08-24** par
> [`resilience_integrations.md`](resilience_integrations.md) **v2.3** : le binaire
> « recovery en cours » décrit désormais un **épisode ouvert** (R-RECOV-1) et non
> l'état du backoff, ce qui supprime la course. La correction porte sur les sept
> chaînes, pas seulement celle-ci.

> **R-PONT-9 (opérationnel).** Tant que R-PONT-8 n'est pas levée, un compteur
> laissé à une valeur non nulle après un épisode clos **doit être remis à zéro**
> — c'est une opération de maintenance, explicitement prévue par le helper.
>
> ✅ **SANS OBJET depuis le 2026-08-24** (R-PONT-8 levée). Conservée comme trace :
> la remise à zéro manuelle du 2026-08-24 relevait de cette règle. Avec la
> définition par épisode, un compteur non nul sur un périmètre sain est
> désormais **résorbé automatiquement** — il maintient l'épisode ouvert, donc le
> retour OK se prononce et remet le compteur à zéro de lui-même.

### 8.3 Axe fraîcheur inapplicable à ce pont

Les `cover.*` de cette entrée sont en **push pur** : ils ne rapportent qu'au
changement d'état, sans écriture périodique du coordinateur.

**Mesuré le 2026-08-24 à 11:48**, pont pleinement sain :

```
salle_de_jeux=closed    last_reported=11:26:44
chambre_enfants=closed  last_reported=11:26:44
sejour_droit=closed     last_reported=11:26:44
sejour_gauche=closed    last_reported=11:26:44
age = 21 min, et croissant
```

> **R-PONT-10 (opposable).** L'axe fraîcheur est **inapplicable** à cette entrée
> et **ne doit pas être câblé**. L'âge d'un volet immobile croît sans borne :
> tout seuil finit par être franchi sur un périmètre sain. Le seuil de 45 min
> initialement retenu aurait produit un faux incident toutes les ~50 minutes —
> et, l'escalade consommant le compteur de tentatives, aurait fini par exposer
> le pont à des coupures d'alimentation injustifiées.
>
> Relever le seuil est **interdit** : ce n'est pas un défaut de réglage mais une
> absence de grandeur mesurable. Voir R-AXE1-1 de
> [`resilience_integrations.md`](resilience_integrations.md) §3.1.

L'âge reste **exposé en observabilité**, mais il n'entre **ni** dans la condition
d'incident **ni** dans la condition de succès : l'automation transmet
`axe_fraicheur: false` au script canon (R-AXE1-3), qui conclut au retour sur les
seuls axes disponibilité et échec de configuration. Il n'est **jamais** un
déclencheur.

Cette entrée est donc couverte par **deux axes** — disponibilité et échec de
configuration — qui sont exactement les deux qui ont détecté l'incident du
2026-08-23.

---

## 9. Frontières

| Sujet | Propriétaire |
|---|---|
| Détection (les trois axes), script canon de recovery, maille entrée | [`resilience_integrations.md`](resilience_integrations.md) |
| Politique de power-cycle des **stations** Netatmo | [`homekit_diagnostic.md`](homekit_diagnostic.md) §9.1 |
| Règles métier des volets | [`volets_pluie.md`](volets_pluie.md) |
| Architecture du pont, patron d'intégration, mode de panne | [`architecture/volets.md`](../architecture/volets.md) |
| Topologie d'alimentation et commandabilité | [`architecture/infrastructure_puissance.md`](../architecture/infrastructure_puissance.md) |
| Supervision réseau du pont | [`ping_lan_synthese.md`](ping_lan_synthese.md) |

---

## 10. Historique de version

- **v1.0** — 2026-08-24. Création. Politique d'escalade bornée à deux échelons
  (reload puis power-cycle unique au seuil de 2 tentatives), gardes explicites
  dont l'exclusion délibérée de la garde WAN (R-PONT-6), anti-boucle par
  non-réinitialisation du compteur (R-PONT-4), limite de latence de l'axe 3
  (R-PONT-7). Lève la réserve §14.1 de `resilience_integrations.md`.
  Consigne également R-PONT-8 (compteur non remis à zéro : course entre la
  temporisation du retour OK et l'expiration du backoff, défaut du patron canon
  observé le jour même) et R-PONT-9 (remise à zéro de maintenance).
- **v1.1** — 2026-08-24. Ajout de R-PONT-10 (§8.3) : l'axe fraîcheur est
  **inapplicable** à ce pont (entités en push pur, âge non borné), retiré du
  câblage et déclaré `non_applicable` au registre. Mesure terrain à l'appui.
  Aucune modification de la politique d'escalade.
- **v1.2** — 2026-08-24. **R-PONT-8 levée** par `resilience_integrations.md` v2.3
  (épisode de recovery, R-RECOV-1) ; R-PONT-9 devient sans objet. La sentinelle
  de seuil est remplacée par le paramètre explicite `axe_fraicheur: false`
  (R-AXE1-3). Aucune modification de la politique d'escalade.

---

*Arsenal — document contractuel · couche domaine · pont iDiamant · v1.2*
