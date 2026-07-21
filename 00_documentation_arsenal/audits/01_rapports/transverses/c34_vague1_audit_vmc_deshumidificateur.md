# C34 — Vague 1 : audit VMC et déshumidificateur

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 1 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaines** | VMC · déshumidificateur |
| **Date** | 2026-07-21 |
| **Nature** | Audit statique. **Aucun reboot, reload, appel de service ou changement d'état n'a été provoqué.** |
| **Couverture** | **20 fichiers lus sur 26** + `vmc.md` + `resilience_integrations.md` + `ups_arret_ha.md`. Les 3 contrats du déshumidificateur restent non lus. Couverture **assumée et bornée** (§6). |

> **Règle appliquée.** Une affirmation sur l'action physique n'est marquée *démontrée
> statiquement* que si la chaîne a été suivie **jusqu'au service appelé** et que les triggers
> et conditions applicables ont été lus. Les autres conclusions portent une qualification
> inférieure.

---

## 1. Correction préalable du cadrage C34

Le cadrage annonçait **21 fichiers runtime** pour la vague 1. Le décompte nominatif donne
**26** : VMC 4+2+5 = 11, déshumidificateur 8+2+5 = 15. **Le chiffre du cadrage est erroné**
et doit être corrigé.

---

## 2. Frontière entre les événements

Distinction établie par lecture, **non transposable** d'un événement à l'autre :

| Événement | Effet observé dans les sources lues |
|---|---|
| **Redémarrage HA** | Seul événement portant un trigger dédié : `platform: homeassistant, event: start`. Présent dans 4 des automatisations lues. |
| **Reload YAML** | **Aucun trigger dédié trouvé** dans les fichiers lus. Un reload recharge les définitions ; il ne produit pas d'événement `homeassistant start`. |
| **Reload d'intégration** | **Aucun trigger dédié trouvé.** Il rend les entités de l'intégration momentanément `unavailable`, ce qui est un cas d'**indisponibilité d'observation**, pas de redémarrage. |
| **Indisponibilité d'observation** | Traitée par des gardes explicites dans les scripts (§3.2, §4.3). |
| **Perte / restauration de helper** | `timer.deshumidificateur_blocage_redemarrage` n'est pas restauré au reboot — **limite assumée et documentée** dans l'en-tête de `reconciliation_demarrage.yaml`. |

**Conséquence méthodologique** : les conclusions ci-dessous portent sur le **redémarrage HA**.
Le comportement au **reload YAML** et au **reload d'intégration** est **indéterminable** à
partir des seules sources lues, faute de trigger dédié — leur effet transite par
l'indisponibilité des entités, dont les gardes sont analysées séparément.

---

## 3. VMC

### 3.1 Chaîne reconstituée

| Rôle | Composant |
|---|---|
| Observation | `switch.vmc_l1`, `switch.vmc_l2` (relais) ; capteurs d'humidité et CO₂ |
| Décision | `binary_sensor.vmc_haute_vitesse_requise` *(non lu — §6)* |
| Cohérence physique | `binary_sensor.vmc_coherence_physique` (`coherence.yaml`) |
| Application | `automation 10190000000001` (`gestion_auto.yaml`), `automation 10190000000003` (`watchdog.yaml`) |
| Action physique | `script.vmc_basse_vitesse`, `script.vmc_haute_vitesse` |
| Équipement | `switch.vmc_l1` / `switch.vmc_l2` (XOR strict, « Bloc 10 ») |
| Reflet UI | `input_boolean.vmc_haute_vitesse` via `automation 10190000000004` |

### 3.2 Fausse incohérence au démarrage — neutralisée en bout de chaîne

**Démontré statiquement.**

`coherence.yaml` calcule :

```
{% set l1 = is_state('switch.vmc_l1', 'on') %}
{% set l2 = is_state('switch.vmc_l2', 'on') %}
{{ (l1 and not l2) or (l2 and not l1) }}
```

`is_state(..., 'on')` renvoie **False** lorsque l'entité est `unavailable` ou `unknown`. Au
démarrage, les deux relais indisponibles donnent donc `l1 = l2 = False`, d'où un état
**`off`** — soit « incohérence physique » — alors qu'aucune incohérence réelle n'est établie.
Le `delay_off: 2s` ne fait que retarder de deux secondes cette bascule, largement dépassées
par une indisponibilité de démarrage.

`watchdog.yaml` s'arme alors : trigger `homeassistant start`, condition
`is_state('binary_sensor.vmc_coherence_physique','off')` — **vraie** — puis appelle
`script.vmc_basse_vitesse`. **Aucun délai, aucune garde `systeme_stable`.**

Mais `basse_vitesse.yaml` ouvre son `choose` par :

```
- conditions: relais in ['unavailable','unknown']
  sequence: []
```

**Aucune action physique n'est émise.** Le risque est réel dans la chaîne décisionnelle et
**neutralisé par la garde de disponibilité du script exécutif**, non par le watchdog.

**Qualification : abstention temporaire.** Correcte, mais obtenue en bout de chaîne.

### 3.3 Incohérence réelle au démarrage

**Démontré statiquement.** Si les relais **sont disponibles** et dans un état invalide
(double ON ou double OFF), la même chaîne aboutit à la branche `default` du script :
`switch.turn_off` sur `vmc_l1`, délai 200 ms, `switch.turn_on` sur `vmc_l2`.

**Qualification : révocation de sécurité justifiée** — convergence fail-safe vers la basse
vitesse, conforme à la finalité déclarée du watchdog.

### 3.4 `systeme_stable` : garde réelle mais contournée au démarrage

**Démontré statiquement.** `gestion_auto.yaml` porte :

```
condition:
  - condition: or
    conditions:
      - condition: template
        value_template: "{{ trigger.platform == 'homeassistant' }}"
      - condition: state
        entity_id: input_boolean.systeme_stable
        state: "on"
```

`input_boolean.systeme_stable` **existe et est utilisé** — mais le trigger de démarrage
**contourne délibérément la garde** par le premier terme du `or`.

**Correction du premier passage — lecture de `haute_vitesse_requise.yaml`.** Une version
antérieure de ce rapport affirmait que la branche `default` du `choose` était atteinte au
démarrage, le capteur décisionnel étant `unknown`. **C'est faux.**
`binary_sensor.vmc_haute_vitesse_requise` **ne porte aucun bloc `availability`** et calcule
son état avec `| float(0)` et `is_state()` : sources indisponibles ⇒ humidités à `0`,
`aeration_favorable` à `False`, `co2_valide` à `False` ⇒ l'état vaut **`off`**, jamais
`unknown`. La branche `default` n'est donc **pas** atteinte.

**Comportement réel au démarrage** : la branche « basse vitesse » s'exécute, sur une décision
`off` **calculée à partir de valeurs de repli** — comportement documenté dans l'en-tête du
capteur (« Capteurs HR indisponibles : interprétés comme non déclenchants »). Le trigger
étant `homeassistant`, le `delay` d'hystérésis est sauté et `script.vmc_basse_vitesse` est
appelé, lequel s'abstient si les relais sont indisponibles (§3.2).

**Qualification révisée : recalcul fonctionnel sur valeurs de repli**, et non action sur
décision non établie. La nuance est importante : le système ne « manque » pas de décision,
il en produit une avec des défauts documentés.

**Asymétrie relevée entre les deux capteurs de diagnostic VMC** :
`binary_sensor.vmc_conformite_decision` **porte une `availability`** exigeant
`decision`, `l1` et `l2` dans `['on','off']` — il devient donc `unavailable` au démarrage,
ce qui est correct. `binary_sensor.vmc_coherence_physique` **n'en porte aucune** et produit
un `off` trompeur (§3.2). Deux capteurs voisins, deux traitements opposés de
l'indisponibilité.

**Qualification : révocation de sécurité justifiée**, avec une **réserve** — le déclencheur
est l'absence de donnée (`unknown`), non une incohérence constatée. L'en-tête du fichier
affirme « ✅ BOOT-SAFE » ; cette affirmation est **exacte quant à l'absence de dommage**, mais
**ne couvre pas** le cas d'une action émise avant calcul du décisionnel.

### 3.5 Reflet UI

**Démontré statiquement.** `synchro_booleen.yaml` (mode `queued`, trigger `homeassistant
start`) met à jour `input_boolean.vmc_haute_vitesse`. Si l'état physique est invalide, **aucune
branche du `choose` ne correspond** et le booléen n'est pas modifié.

Le fichier documente que ce booléen est une « façade de compatibilité UI », « ni source de
vérité métier, ni source de vérité physique ».

**Qualification : restauration correcte d'un reflet, sans effet physique.**

### 3.6 Question du cadrage : lacune documentaire ?

**Tranché : ce n'est pas une lacune.** `contrats/vmc.md` existe en **v1.3, statut « Stable —
conforme Arsenal »**, se déclare définir « EXHAUSTIVEMENT le comportement attendu », et pose
trois niveaux non fusionnables — décision pure, application, actionneurs. L'absence de
répertoire `contrats/vmc/` reflète un **contrat unique suffisant**, non un manque.

---

## 4. Déshumidificateur

### 4.1 Chaîne reconstituée

| Rôle | Composant |
|---|---|
| Observation | `sensor.prise_deshumidificateur_power` (puissance) |
| État réel | `binary_sensor.deshumidificateur_actif` (`etat.yaml`, seuil 100 W) |
| Décision | `binary_sensor.deshumidificateur_cave_demarrage_recommande` *(non lu — §6)* |
| Contrainte temporelle | `timer.deshumidificateur_blocage_redemarrage`, `input_number.deshumidificateur_delai_min_redemarrage` |
| Application | automatisations `…006` (activation), `…008` (blocage), `…010` (réconciliation) |
| **Autorité d'exécution unique** | `script.set_deshumidificateur_state` |
| Qualification | `script.guard_deshumidificateur` → 7 `input_text` de diagnostic |
| Équipement | `switch.deshumidificateur` |

### 4.2 Défaut démontré : garde d'indisponibilité structurellement inopérante

**Démontré statiquement — chaîne suivie jusqu'au service `switch.turn_on`.**

`etat.yaml` produit `binary_sensor.deshumidificateur_actif` ainsi :

```
{% if p_raw in ['unknown','unavailable','none',''] %}
  false
{% else %}
  {{ (p_raw | float) > 100 }}
{% endif %}
```

Le capteur renvoie donc **`off`**, jamais `unknown`, lorsque la source est indisponible. Le
commentaire l'assume : « En cas d'indisponibilité → OFF (pas de fausse détection ON) ».

Or `set_deshumidificateur_state` se protège par :

```
- conditions: {{ current_real_state in ['unknown', 'unavailable'] }}
  sequence: - stop: "Source de verite indisponible"
```

où `current_real_state` est précisément `binary_sensor.deshumidificateur_actif`.

**Cette garde ne peut jamais être vraie.** Le script déclare vérifier « la disponibilité de la
source de vérité » ; **structurellement, il ne la vérifie pas**. Seule la garde suivante, sur
`switch.deshumidificateur`, reste opérante.

**Conséquence** : lorsque la prise est indisponible, le système **affirme** que l'appareil est
à l'arrêt au lieu de reconnaître qu'il l'ignore. Si la recommandation est active et le timer
échu, la branche `default` émet `switch.turn_on`.

**Qualification : action physique sur observation fausse.** L'effet matériel est probablement
**nul si l'appareil tourne déjà** (commande idempotente), mais la chaîne agit sur une donnée
qu'elle croit fiable et qui ne l'est pas — et le guard qualifiera ensuite `not_confirmed`
après 120 s, produisant un **diagnostic faux** plutôt qu'un signal d'indisponibilité.

**C'est le défaut principal de la vague 1.**

### 4.3 Réconciliation au redémarrage

**Démontré statiquement.** `reconciliation_demarrage.yaml` (ID `10060000000010`) : trigger
`homeassistant start`, `delay: 00:01:30`, puis conditions. **Aucune dépendance à
`systeme_stable`** — l'attente est un délai fixe de 90 secondes.

L'en-tête est explicite : « ne rejoue aucune commande passée », « décision fraîche fondée
uniquement sur les états courants ». **La lecture du code le confirme** : aucune relecture
d'historique, aucun `last_changed`.

**Qualification : recalcul fonctionnel**, non un rejeu.

**Limite assumée, documentée dans le fichier** : le timer de blocage n'étant pas restauré
après reboot, il revient à `idle`, la condition passe, et « Arsenal privilégie la reprise de
service à l'absence prolongée de cycle ». Une **activation physique au redémarrage est donc
possible et voulue** — ce n'est pas un défaut au sens de l'invariant C34, mais un arbitrage
explicite.

**Réserve** : cette réconciliation hérite du défaut §4.2, puisque sa condition
`binary_sensor.deshumidificateur_actif == 'off'` peut être satisfaite par une observation
fausse, et que sa garde `not in ['unknown','unavailable']` est inopérante sur ce capteur.

### 4.4 Blocage de redémarrage

**Probable mais non prouvé.** `blocage_redemarrage.yaml` déclenche sur une transition
`from: 'on'` → `to: 'off'` de `binary_sensor.deshumidificateur_actif`. Au redémarrage,
l'état antérieur n'est pas `on` mais absent : le trigger ne devrait donc pas se déclencher.
**Non démontré** — le comportement exact d'un trigger `from:` explicite après redémarrage
n'a pas été établi par une source du dépôt.

### 4.5 Auteurs de commande

**Démontré statiquement.** Trois automatisations lues (`…006`, `…010`) et le script
`forcer_etat` convergent **toutes** vers `script.set_deshumidificateur_state`, déclaré
« autorité d'exécution unique du domaine ». Aucun `switch.turn_on/off` direct sur
`switch.deshumidificateur` n'a été trouvé hors de ce script **dans les fichiers lus**.

**Réserve** : 5 automatisations du domaine n'ont pas été lues (§6) — l'unicité de l'auteur
n'est donc **pas établie sur l'ensemble du domaine**.

---

## 4 bis. Writers, rejeu et timers — lecture complète des 8 automatisations

### Auteur unique d'action physique — **démontré**

Les **8 automatisations** et les **2 scripts** du domaine ont été lus. `switch.deshumidificateur`
n'est écrit que par `script.set_deshumidificateur_state`. Cinq appelants : `…006` activation,
`…007` désactivation, `…010` réconciliation, `…005` retry ON, `…009` retry OFF. Les trois
autres (`…003` ouverture cycle, `…004` fermeture cycle, `…008` blocage) n'agissent que sur des
timers, **sans aucune action matérielle**.

**L'unicité de l'auteur, réservée au premier passage, est désormais établie sur l'ensemble du
domaine.**

### Rejeu — anti-boucle présent, risque résiduel au reboot

Les deux `retry` déclenchent sur `input_text.deshum_guard_last_verdict` passant à
`not_confirmed`, sous quatre conditions dont
`{{ states('input_text.deshum_guard_last_request_source') != 'automation.deshumidificateur_retry_on' }}`.
**Un retry ne peut donc pas se relancer sur son propre échec** : une seule réémission.

**Risque résiduel — plausible, non prouvé.** Ces `input_text` sont **restaurés au
redémarrage**. Si le dernier verdict enregistré était `not_confirmed`, avec
`expected_state` cohérent et `reason = timeout_reached`, la restauration produit un
changement d'état susceptible d'armer le trigger `to: "not_confirmed"` au démarrage, donc
**une réémission de commande physique**. Établir ce point exigerait de connaître le
comportement exact de HA lors de la restauration d'un `input_text` — **non démontrable par
les sources du dépôt**.

### Désactivation — absence de rejeu, intentionnelle et documentée

`desactivation.yaml` (`…007`) ne porte **aucun trigger `homeassistant start`**, et son
en-tête l'assume : « En cas de redémarrage de Home Assistant alors que la recommandation est
déjà OFF, aucune extinction n'est rejouée automatiquement. Ce comportement est intentionnel. »

**Qualification : continuité légitime.** Aucune coupure au redémarrage.

### Timers au redémarrage — vecteur de déclenchement

`activation` et `desactivation` portent chacune un trigger sur un timer passant à `idle`
(`blocage_redemarrage` pour l'une, `cycle` pour l'autre). Les timers n'étant pas restaurés,
ils reviennent à `idle` au démarrage — **ce qui constitue un vecteur de déclenchement des deux
automatisations**. Leurs conditions `for: "00:05:00"` sur la recommandation devraient
s'y opposer, la durée d'état étant réinitialisée au redémarrage.

**Qualification : abstention temporaire — probable, non prouvée.** La protection repose sur le
comportement de `for:` après redémarrage, non établi par les sources du dépôt.

### Recommandation métier — auto-référence

`demarrage_recommande.yaml` conserve son propre état lorsqu'un critère est invalide :

```
{% if critere_rh in invalides or critere_ha in invalides %}
  {{ is_state(this.entity_id, 'on') }}
{% else %}
  {{ critere_rh == 'on' or critere_ha == 'on' }}
{% endif %}
```

C'est le **même mécanisme d'auto-référence que celui documenté en C32 / L6c** : une entité
neuve — après redémarrage ou après renommage d'`unique_id` — se relit sans rien lire et
retombe à `off`. **La recommandation ne peut donc pas être `on` tant que les critères ne sont
pas calculés**, ce qui rend la réconciliation `…010` inopérante dans cette fenêtre.

**Qualification : abstention temporaire — démontrée statiquement.** Effet protecteur ici, mais
par un mécanisme dont C32 a établi qu'il crée une **fenêtre aveugle** de durée non bornée.

---

## 5. Portée réelle des doctrines transverses

### `resilience_integrations.md` — v1.1, **mode report-only**

**Champ d'application** : détection et relance des **intégrations défaillantes**, selon deux
axes déclarés orthogonaux — **fraîcheur** (âge des données) et **disponibilité** (présence de
membres exploitables).

**Ce qu'il impose** : la non-substitution des deux axes ; une chaîne complète comprenant
diagnostic, décision, action et UI ; pour les automatisations de décision, la garde
`input_boolean.systeme_stable = on`, le `mode: single` et l'absence de `time_pattern` ;
la délégation de l'action à `script.resilience_integration_recover`.

**Ce qu'il ne permet pas de conclure pour VMC et déshumidificateur** : il traite d'une
**panne d'intégration**, non d'une **opération technique volontaire**. Il ne décrit ni le
redémarrage, ni le reload YAML, ni le reload d'intégration, et ne s'applique à aucun des deux
domaines de cette vague. **Il n'est donc pas invoqué comme preuve.**

**Une résonance, explicitement non probante** : son principe « un âge figé bas ne vaut jamais
preuve de santé » décrit une structure identique au défaut du §4.2 — un `off` figé ne vaut pas
preuve d'arrêt. C'est une **analogie conceptuelle**, non une règle opposable au déshumidificateur.

### `ups_arret_ha.md` — v1.0, **statut « Projet »**

**Portée exacte** : déclencher un **arrêt propre** de Home Assistant (`hassio.host_shutdown`)
lorsque l'UPS est sur batterie et l'autonomie insuffisante. Le contrat n'autorise aucune
action sur les autres équipements.

**Différences déterminantes** : l'arrêt UPS est **subi et anticipé**, avec préavis (critère de
coupure durable ≥ 60 s), et suivi d'un **démarrage à froid**. Le **redémarrage volontaire**, le
**reload YAML** et le **reload d'intégration** n'y figurent pas.

**Transpositions interdites** : aucune conclusion de ce contrat ne vaut pour les trois
événements de C34, et aucune conclusion de C34 ne vaut pour l'arrêt UPS. Son statut « Projet »
interdit en outre de le traiter comme une norme stabilisée.

---

## 6. Limites probatoires de cette vague

**Fichiers lus (11 / 26)** : VMC — `watchdog`, `synchro_booleen`, `gestion_auto`,
`coherence`, `intention`, `basse_vitesse`. Déshumidificateur — `reconciliation_demarrage`,
`blocage_redemarrage`, `activation`, `etat`, `guard_deshumidificateur`, `forcer_etat`.

**Non lus (6 fichiers runtime + 3 contrats)** : VMC — `alerte_nc_decision`,
`haute_vitesse` (script), `delta_humidite_absolue_favorable`. Déshumidificateur —
`conformite_execution`, `criteres/humidite_absolue`, `criteres/humidite_relative`, et les
**3 contrats du domaine** (`deshumidificateur.md`, `guard.md`, `README.md`).

**Domaine déshumidificateur : les 8 automatisations et les 2 scripts sont lus**, ce qui rend
la cartographie des writers complète (§4 bis). Le décisionnel `demarrage_recommande` est lu ;
ses deux critères amont ne le sont pas.

**Conséquences directes** :

- les deux **critères amont** du déshumidificateur n'étant pas lus, la manière dont ils
  produisent `unknown` — et donc déclenchent l'auto-référence du §4 bis — **n'est pas établie** ;
- les **3 contrats du domaine** n'étant pas lus, le défaut du §4.2 **n'est pas confronté à sa
  norme** : il est décrit, non qualifié en écart contractuel ;
- **aucune preuve runtime** n'a été mobilisée : toutes les conclusions sont statiques ;
- deux points reposent sur le comportement interne de Home Assistant — restauration d'un
  `input_text` et évaluation de `for:` après redémarrage — **non démontrables par les sources
  du dépôt** et donc laissés *probables*.

---

## 7. Suite

Compléter la lecture des 15 fichiers restants et des contrats du déshumidificateur, puis
conduire le **contre-audit** prévu par C34. Le défaut du §4.2 devra être confronté aux
contrats `contrats/deshumidificateur/` avant toute orientation corrective.

---
