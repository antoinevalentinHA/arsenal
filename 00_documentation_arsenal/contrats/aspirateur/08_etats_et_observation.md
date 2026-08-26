# CONTRAT ARSENAL — ASPIRATEUR
## 08 — États, mouvement et observation

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Fixer le vocabulaire d'état du domaine, l'autorité de chaque témoin,
et l'honnêteté d'observation opposable.

---

## 1. États canoniques du domaine

Le domaine distingue **huit** situations, qui ne se confondent jamais :

| État canonique | Ce qu'il signifie |
|---|---|
| **Mission ouverte** | Une session de nettoyage est **ouverte** — donc reprenable. **Ne dit rien** du mouvement du robot. |
| **Nettoyage réel** | Le robot **nettoie effectivement**. |
| **Pause** | La mission est ouverte et **suspendue**. |
| **Erreur** | Le robot **ou le dock** signale une condition d'erreur. |
| **Retour à la base** | Le robot **roule vers son dock**. C'est du **mouvement**. |
| **Amarrage** | Le robot **s'amarre**. |
| **Charge** | Le robot est **en charge**. |
| **Indisponibilité** | L'état n'est **pas connu** — `unknown`, `unavailable`, appareil hors ligne. |

> **`ASP-INV-44`** — Ces huit états sont **exposés distinctement**. Le domaine ne
> les agrège **jamais** en un booléen « occupé / libre », et ne présente jamais
> l'un pour l'autre. Une agrégation de confort est une perte d'information, pas
> une simplification.

> **`ASP-INV-45` — l'indisponibilité est un état, pas un trou.** Conformément à
> [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
> §6 et §8, `unknown` et `unavailable` **ne valent ni `false`, ni un état
> nominal, ni la dernière valeur connue**. Ils sont **restitués comme
> indisponibilité**, jamais masqués.

---

## 2. Autorité des témoins

| Question | Témoin faisant autorité | Statut |
|---|---|---|
| **Le robot bouge-t-il ?** | L'**état du `vacuum`** — `cleaning`, `returning` | **Autorité** ([`01`](01_finalite_et_perimetre.md) §7) |
| **Quelle activité précise ?** | `sensor.roborock_q7_max_etat` — énumération **non exhaustive** : `charger_disconnected`, `cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, `returning_home`, `docking`, `charging`, `error`, `device_offline`… | **Autorité** pour l'activité et la garde anti-double-lancement. Ses valeurs sont **partitionnées en quatre classes fermées** par [`07`](07_moteur_de_mission.md) §5.0 |
| **Une session est-elle inachevée ?** | `binary_sensor.roborock_q7_max_nettoyage` | Autorité **de sa seule sémantique** — voir §3 |
| **Quelle pièce ?** | `sensor.roborock_q7_max_piece_actuelle` | Observation ; sert aussi de **confirmation cartographique** ([`06`](06_integrite_mono_carte.md)) |
| **Pourquoi l'erreur ?** | `sensor.roborock_q7_max_erreur_de_l_aspirateur`, `sensor.roborock_q7_max_dock_erreur_de_dock` | Observation de diagnostic |
| **Progression** | Durée de nettoyage, surface de nettoyage | Observation — lecture bornée par [`04`](04_nombre_de_passages.md) §3 |
| **Batterie, charge, prérequis matériels** | Entités natives correspondantes | Observation, jamais gate — sauf la serpillière ([`03`](03_profils_metier.md) §4) |

> **`ASP-INV-46` — la garde anti-double-lancement s'appuie sur l'état machine.**
> Elle repose sur `sensor.roborock_q7_max_etat`, **jamais** sur le témoin de
> session inachevée.

---

## 3. `binary_sensor.…_nettoyage` — ce qu'il dit, et ce qu'il ne dit pas

**Fait établi.** Ce témoin reflète un champ de statut dont l'énumération est :
*terminé* · *nettoyage global inachevé* · *nettoyage zoné inachevé* · *nettoyage
par segments inachevé*. Sa sémantique réelle est donc **« une session n'est pas
terminée »** — c'est-à-dire **reprenable**.

**Il est désaligné du mouvement dans les deux sens, et c'est prouvé :**

| Situation observée | Témoin | Réalité |
|---|---|---|
| Session par segments ouverte, robot **immobile hors dock** | `on` | Le robot **ne nettoie pas** — témoin **sur-inclusif** |
| Robot **roulant vers son dock** en `returning_home` | `off` | Le robot **se déplace** — témoin **sous-inclusif** (53 s puis 25 s de déplacement à `off`, deux fois) |

> **`ASP-INV-47` — jamais une preuve de mouvement, dans ce domaine.**
> `binary_sensor.…_nettoyage` n'est **jamais** utilisé par le domaine
> `aspirateur` comme preuve de mouvement du robot. Il **signifie « session
> inachevée »**, et rien d'autre.
>
> **Portée : ce domaine.** Cet invariant ne gouverne **que** les usages du
> domaine `aspirateur`. La règle applicable aux consommateurs d'autres domaines
> appartient à leur contrat propre — pour l'inhibition d'intrusion, c'est
> **`ALM-ROBO-1`** ([`01`](01_finalite_et_perimetre.md) §7, `ASP-INV-4`). Un
> contrat **utilise** la doctrine transverse, il ne la **redéfinit** pas, et il ne
> légifère pas pour un domaine dont il n'a pas l'autorité.

**Usage légitime.** Ce témoin **est** l'observation de la « session inachevée » —
état canonique du §1 — et fonde le refus `SESSION_INACHEVEE`
([`07`](07_moteur_de_mission.md) §5.4). C'est son **seul** usage contractuel.

### 3.1 `MISSION_DEJA_OUVERTE` et `SESSION_INACHEVEE` — disjonction déterministe

Les deux refus reposent sur **deux témoins différents** et sur des **conditions
mutuellement exclusives**. Ils ne se recouvrent jamais.

| | `MISSION_DEJA_OUVERTE` | `SESSION_INACHEVEE` |
|---|---|---|
| **Témoin décisif** | L'**état machine** (`sensor.…_etat`) | Le **témoin de session** (`binary_sensor.…_nettoyage`) |
| **Condition** | L'état machine est en **classe A** — activité ou mission reconnue ([`07`](07_moteur_de_mission.md) §5.0) | L'état machine est en **classe R** (repos admissible) **et** le témoin de session vaut `on` |
| **Ce que cela signifie** | Le robot **fait** quelque chose de reconnu | Le robot **ne fait rien de reconnu**, mais une session reste **ouverte** |
| **Geste opérateur attendu** | Attendre la fin, ou arrêter la mission en cours | Arrêter la session ouverte, ou demander le retour à la base |

> **`ASP-INV-64` — arbitrage déterministe des deux refus.** L'état machine est
> évalué **en premier** et tranche seul : s'il est en classe A, le refus est
> `MISSION_DEJA_OUVERTE`, **quel que soit** l'état du témoin de session. **Pour
> l'arbitrage entre `MISSION_DEJA_OUVERTE` et `SESSION_INACHEVEE`**, le témoin de
> session n'est consulté **que** lorsque l'état machine appartient à la classe R.
>
> **Portée : cet arbitrage.** Cette règle de priorité ne borne **que** le choix
> entre ces deux motifs de refus. Elle **ne restreint pas** les autres usages
> contractuels du témoin de session — en particulier sa lecture comme **garde de
> reprise** depuis `paused`, où il atteste qu'une session est réellement ouverte
> ([`07`](07_moteur_de_mission.md) §7.1, `ASP-INV-62`).
>
> **La couverture est totale et sans recouvrement** : classes A, E et N refusent
> sur l'état machine seul ; la classe R refuse sur le témoin de session s'il est
> `on`, et autorise s'il est `off`. Aucun couple d'états ne produit deux motifs,
> et aucun n'en produit zéro.
>
> **Pourquoi cet ordre.** L'état machine est le témoin d'autorité de l'activité,
> et le témoin de session est **faux dans les deux sens** (§3). Le faire trancher
> en premier reviendrait à fonder un refus sur le témoin le moins fiable.

---

## 4. Sens physique d'un geste de conduite

> **`ASP-INV-48`** — Un geste de conduite n'est proposé que lorsqu'il a un **sens
> physique** dans l'état courant :
>
> - **pause** n'a de sens que sur une activité en cours ;
> - **reprise** n'a de sens que depuis une pause, session ouverte — c'est la garde de `ASP-INV-62` ([`07`](07_moteur_de_mission.md) §7.1) ;
> - **arrêt** n'a de sens que sur une mission ouverte ;
> - **retour à la base** n'a de sens que si le robot n'y est pas déjà, et n'y va
>   pas déjà.
>
> Hors de ces conditions, le geste n'est **pas présenté comme disponible**
> ([`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md) §6.1)
> — il n'est pas non plus « proposé puis ignoré ».

**Capacités réellement exposées.** Les gestes de conduite retenus sont ceux que
l'appareil déclare supporter et que l'audit a relevés comme tels. Le domaine
**n'invente aucun geste** et n'en suppose aucun.

---

## 5. Ce que le domaine expose pendant et après une mission

| Moment | Ce qui est exposé |
|---|---|
| **À la demande** | L'intention retenue — carte, pièces, profil, passages ([`05`](05_intention_de_mission.md)) |
| **À l'émission** | L'issue qualifiée — canal indisponible / rejetée / acceptée ([`07`](07_moteur_de_mission.md) §4) |
| **Après l'émission** | La **transition observée**, ou son absence qualifiée |
| **Pendant** | État canonique courant, pièce courante, progression, erreurs éventuelles |
| **En fin** | Fin nominale, retour, amarrage, charge — ou échec qualifié |
| **Après** | La **dernière intention lancée**, à titre de trace — **jamais** relue depuis l'appareil comme preuve du profil utilisé ([`03`](03_profils_metier.md) §5) |

> **`ASP-INV-49` — aucun silence.** Toute mission produit une issue **explicite**.
> Une mission qui ne démarre pas, une commande qui n'aboutit pas, un réglage qui
> ne se confirme pas **se disent**. L'absence de nouvelle n'est jamais une bonne
> nouvelle dans ce domaine — c'est le mode d'échec natif de l'appareil.

---

## 6. Ce que le domaine n'observe pas — V1

- **Aucune historisation.** Aucune entité du domaine n'est inscrite au `recorder`
  par ce contrat ; aucune reconstitution a posteriori n'est promise. Extension
  optionnelle, hors chemin critique
  ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)).
- **Aucune mesure de rendement** (surface nettoyée cumulée, statistiques d'usage,
  durée de vie des consommables).
- **Aucune position cartographique fine** du robot.

---

## Renvois

- Moteur, issues et gestes de conduite : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Refus et diagnostics : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Frontière UI : [`11_frontiere_ui.md`](11_frontiere_ui.md)
- Modèle d'états et vocabulaire (modèle alarme) : [`../alarme/10_modele_etats_et_vocabulaire.md`](../alarme/10_modele_etats_et_vocabulaire.md)
- Index du domaine : [`README.md`](README.md)
