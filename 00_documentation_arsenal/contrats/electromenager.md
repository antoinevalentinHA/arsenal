# 🧠 ARSENAL — CONTRAT NORMATIF
## Électroménager — Détection de cycle et notification (lave-vaisselle, buanderie)

## 📌 Statut

**v1.1 — NORMATIF.** Ce contrat documente le runtime réel. En cas de divergence,
le comportement réel des automations prévaut ; les libellés et descriptions ne
font pas autorité. Aucune entité, aucun seuil et aucune règle ne sont inventés.

**Portée volontairement restreinte.** Ce contrat **n'est pas** un contrat
« électroménager » général. Il couvre **exclusivement** la détection de cycle et
la notification des **deux appareils réellement implémentés** : le lave-vaisselle
et la buanderie (lave-linge). Toute autre prise ou tout autre appareil est hors
périmètre tant qu'il n'est pas implémenté et documenté.

## 🎯 Rôle

Signaler, par appareil, qu'un **cycle est en cours**, à partir de la **puissance
mesurée par sa prise connectée**, et **notifier** l'utilisateur au début et à la
fin du cycle. C'est de l'**observabilité + notification pure** : aucun pilotage
d'appareil, aucune décision énergétique.

## 🧱 Sources de vérité (entités réelles)

| Appareil | Source de puissance | Flag de cycle | Décision de fin | Début persistant |
|---|---|---|---|---|
| Lave-vaisselle | `sensor.prise_lave_vaisselle_power` | `input_boolean.lave_vaisselle_cycle` | `binary_sensor.lave_vaisselle_fin_cycle_etablie` | `input_datetime.lave_vaisselle_debut_cycle` |
| Buanderie (lave-linge) | `sensor.prise_buanderie_power` | `input_boolean.buanderie_cycle` | `binary_sensor.buanderie_fin_cycle_etablie` | — (aucune durée minimale) |

Automations (préfixe d'identifiant `1008` — registre `prefix_id.yaml`) :

| Appareil | Début | Fin | Projection persistante |
|---|---|---|---|
| Lave-vaisselle | `10080000000001` | `10080000000002` | `10080000000006` |
| Buanderie | `10080000000003` | `10080000000004` | `10080000000007` |

Canal de notification mobile : `script.notification_envoyer` vers
`input_text.telephone_parent_1_notify`.

## 1. Détection de début

`mode: single`. Déclencheur : la puissance de la prise dépasse un seuil pendant
3 minutes. Condition : le flag de cycle est `off`. Action : `turn_on` du flag.

**Lave-vaisselle** : l'automation de début écrit l'horodatage persistant
`input_datetime.lave_vaisselle_debut_cycle` **avant** d'allumer le flag. Tout flag
allumé par le début a donc un début daté.

| Appareil | Seuil de début | Durée |
|---|---|---|
| Lave-vaisselle | puissance > **30 W** | `00:03:00` |
| Buanderie | puissance > **50 W** | `00:03:00` |

Les seuils sont **propres à chaque prise** (asymétrie assumée, cf. §7).

## 2. Décision de fin établie (sur état)

La fin d'un cycle est une **décision sur état**, portée par un
`binary_sensor` de template par appareil — **autorité unique** de la fin, lue
par l'automation de fin comme déclencheur **et** comme condition. Elle est
recalculable à tout moment : elle ne dépend d'aucun front ni d'aucune exécution
passée.

La décision est vraie quand, **de façon continue** pendant la durée basse
(`delay_on`) :

- le flag de cycle est `on` ;
- la puissance est une valeur **mesurée** (numérique) **strictement inférieure**
  au seuil bas ;
- **lave-vaisselle uniquement** : le cycle dure depuis **plus de 45 min**
  (garde-fou anti-pause), durée lue sur `input_datetime.lave_vaisselle_debut_cycle`.

| Appareil | Seuil bas | Durée basse (`delay_on`) | Durée minimale de cycle |
|---|---|---|---|
| Lave-vaisselle | < **2 W** | `00:10:00` | > **45 min** (2 700 s) |
| Buanderie | < **2 W** | `00:15:00` | aucune |

**Mesure absente.** Une puissance `unknown`, `unavailable` ou non numérique
**n'est pas** une puissance basse : elle rend la décision fausse et réarme la
durée basse. Aucune fin n'est établie sur absence de mesure.

**Durée minimale et redémarrage (lave-vaisselle).** La durée **ne se lit jamais**
sur `last_changed` du flag, que tout redémarrage de Home Assistant remet à l'heure
du démarrage. Seul **repli** admis : si l'horodatage persistant est inconnu
(helper jamais écrit), la décision lit `last_changed` du flag, qui **minore** la
durée réelle — la fin peut être retardée, jamais anticipée.

**Effet de la combinaison.** Le `delay_on` porte sur la conjonction : si la
puissance tombe sous le seuil avant la durée minimale, la fin est établie au plus
tôt 10 min après que la durée minimale est atteinte (au plus tôt 55 min après le
début).

## 3. Clôture de fin (avec fenêtre de confirmation)

`mode: restart`. Déclencheurs :

- passage de la décision de fin à `on` (cas nominal) ;
- **réconciliation** : `input_boolean.systeme_stable → on` (redémarrage de HA) ;
- **réconciliation** : événement `automation_reloaded` (rechargement des
  automations).

Condition unique : la décision de fin est `on`.

L'arrêt n'est **pas** confirmé immédiatement : l'automation attend
(`wait_for_trigger` + `timeout`, `continue_on_timeout: true`) une éventuelle
**reprise** de puissance. La fin n'est confirmée que si **aucune reprise** n'est
survenue (`wait.trigger is none`) **et** que la décision est **toujours** `on` au
terme de la fenêtre. Sinon rien n'est écrit : la décision, recalculée, réarme la
suite.

| Appareil | Seuil de reprise | Délai de confirmation |
|---|---|---|
| Lave-vaisselle | > **5 W** | `00:05:00` |
| Buanderie | > **30 W** | `00:05:00` |

Fin confirmée : `turn_off` du flag, **puis** notification mobile de fin.

## 4. Invariants de fiabilité (C57)

- **INV-EM-1 — Aucune fin sur front unique.** La fin est une décision sur état ;
  aucun déclencheur `numeric_state` de puissance ne porte la fin. Une fin rejetée
  trop tôt ou un front manqué n'est jamais définitif.
- **INV-EM-2 — Réconciliation.** L'automation de fin se réévalue au retour de
  `systeme_stable` et après tout rechargement des automations : une exécution
  tuée (redémarrage, rechargement) pendant la fenêtre de confirmation est
  reprise.
- **INV-EM-3 — Aucune fin sans mesure.** Une puissance absente ou non numérique
  ne contribue jamais à établir une fin, ni pendant la durée basse, ni au terme
  de la confirmation.
- **INV-EM-4 — Durée persistante.** La durée minimale de cycle (lave-vaisselle)
  ne dépend d'aucun `last_changed`, hors repli prudent §2.
- **INV-EM-5 — Une clôture, une notification.** Le flag est éteint **avant** la
  notification de fin : la décision retombe aussitôt et toute réexécution échoue
  sur la condition. Une clôture logique et une notification de fin au plus par
  cycle.
- **INV-EM-6 — Aucune remise à `off` sans fin établie.** Aucun délai maximal,
  aucun chien de garde n'éteint un flag : un cycle dont la fin n'est pas établie
  (prise muette) reste visible comme en cours.

**Critère opposable.** Aucun redémarrage, rechargement ou passage prématuré sous
le seuil bas ne peut laisser indéfiniment un flag de cycle à `on` après une fin
effectivement établie par la mesure.

## 5. Notifications

- **Cycle en cours** : notification **persistante** d'état, **projetée** par
  l'automation de projection de l'appareil (`10080000000006` / `10080000000007`)
  depuis le flag : `create` tant que le flag est `on` (y compris au retour de
  `systeme_stable`), `dismiss` à son extinction (`notification_id` = nom du flag,
  idiome NOTIF-03, cf. [`notifications.md`](notifications.md)). Les automations
  de début et de fin n'écrivent aucune notification persistante.
- **Fin confirmée** : notification **mobile** (`script.notification_envoyer`,
  cible `input_text.telephone_parent_1_notify`), émise par l'automation de fin.

La notification n'est qu'un effet ; elle ne porte aucune décision.

## 6. Écrivain souverain

Chaque `input_boolean.*_cycle` possède **un et un seul** ensemble d'écrivains :
ses automations de début (`turn_on`) et de fin (`turn_off`) du **même appareil**.
`input_datetime.lave_vaisselle_debut_cycle` n'est écrit que par l'automation de
début du lave-vaisselle. Aucune autre autorité n'écrit ces helpers. Les flags sont
lus par la décision de fin, la garde de début et la projection persistante de
leur appareil ; aucun dashboard ni aucune décision hors domaine ne les lit.

Le CI vérifie ces règles : [`check_electromenager_contracts.py`](../../scripts/arsenal_contracts/check_electromenager_contracts.py)
(EM-1 à EM-8, avec rendu des gabarits de décision).

## 7. Hors périmètre

- **Aucun pilotage d'appareil** (pas de coupure/relance de prise, pas de
  commande machine).
- **Aucun automatisme énergétique** (pas d'effacement, pas de pilotage tarifaire).
- **Aucun dashboard** consommateur des flags.
- **Pas de généralisation** à d'autres prises ou appareils : seuls le
  lave-vaisselle et la buanderie sont couverts.
- **Pas d'usage des mesures `energy` / `linkquality`** (`sensor.prise_*_energy`,
  `sensor.prise_*_linkquality`) comme source de détection de cycle — seule la
  **puissance instantanée** (`*_power`) est utilisée.
- **Aucune historisation dédiée** (recorder) des entités de cycle : les traces
  natives des automations suffisent (arbitrage opérateur C57).

## 8. Dettes / observations

- **DETTE-EM-1 — Seuils asymétriques.** Les seuils de début, de bas et de reprise
  diffèrent entre appareils (lave-vaisselle 30 / 5 W, buanderie 50 / 30 W) ; ils
  sont calibrés par prise et non factorisés. Observation, pas anomalie.
- **OBS-EM-1 — Flags sans consommateur aval.** Les `*_cycle` ne servent
  aujourd'hui qu'à la notification ; aucun dashboard ni décision hors domaine ne
  les lit.
- **OBS-EM-2 — Pause longue en cours de cycle.** Une pause à puissance nulle plus
  longue que durée basse + confirmation (lave-vaisselle : après 45 min) est lue
  comme une fin ; la reprise ouvre un nouveau cycle (deux notifications). Limite
  des seuils calibrés, inchangée par C57.
- **OBS-EM-3 — Début manqué.** Un redémarrage pendant les 3 minutes de montée en
  puissance peut faire manquer le début (aucun flag, aucune notification) :
  défaut sans blocage, hors périmètre C57.
- **OBS-EM-4 — Prise muette.** Une prise indisponible durablement en fin de cycle
  laisse le flag à `on` (INV-EM-6) ; l'anomalie reste visible par la notification
  persistante. Le prochain cycle mesuré dont la fin est établie clôt le flag.

## 🔗 Renvois

- Notifications : [`notifications.md`](notifications.md)
  (`script.notification_envoyer`, idiome de projection NOTIF-03).
- Chantier : [`C57`](../audits/04_chantiers/electromenager/c57_fin_cycle_robuste.md).

## 🔒 Statut d'autorité

Contrat normatif opposable pour le périmètre déclaré (lave-vaisselle + buanderie).
Le runtime fait foi ; tout écart d'implémentation est une non-conformité, pas une
interprétation. L'ajout d'un nouvel appareil exige une extension explicite de ce
contrat (entités réelles, seuils réels), jamais une généralisation implicite.

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.1 | 2026-10-12 | **C57 — fin de cycle robuste.** La fin devient une **décision sur état** (`binary_sensor.*_fin_cycle_etablie`, §2) avec **réconciliation** au redémarrage et au rechargement (§3) ; durée minimale du lave-vaisselle lue sur l'horodatage **persistant** `input_datetime.lave_vaisselle_debut_cycle`, plus jamais sur `last_changed` ; mesure absente jamais lue comme puissance basse ; confirmation re-vérifiant la décision ; extinction avant notification ; invariants INV-EM-1 à 6 (§4). Alignement sur le runtime antérieur : le garde-fou de 45 min (non documenté en v1.0) et la projection persistante `10080000000006` / `10080000000007` (#324, C15) remplacent les `create` / `dismiss` attribués à tort au début et à la fin. Seuils inchangés. |
| 1.0 | 2026-06-07 | Création depuis le runtime réel. Documentation de la détection de cycle par puissance (début > seuil / 3 min ; fin < seuil bas / durée + fenêtre de confirmation anti-reprise), des flags `input_boolean.*_cycle`, des notifications persistante (début) et mobile (fin), et de l'écrivain souverain par flag, pour les deux appareils implémentés (lave-vaisselle `1008000000001/2`, buanderie `1008000000003/4`). Portée restreinte aux appareils réels ; aucun pilotage, aucun usage `energy`/`linkquality`. |
