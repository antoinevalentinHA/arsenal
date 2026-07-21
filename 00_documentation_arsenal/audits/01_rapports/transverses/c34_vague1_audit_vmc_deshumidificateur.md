# C34 — Vague 1 : audit VMC et déshumidificateur

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 1 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaines** | VMC · déshumidificateur |
| **Date** | 2026-07-21 |
| **Nature** | Audit statique. **Aucun reboot, reload, appel de service ou changement d'état n'a été provoqué.** |
| **Couverture** | **26 / 26 fichiers runtime lus**, plus `vmc.md`, les **3 contrats du déshumidificateur**, `resilience_integrations.md` et `ups_arret_ha.md`. **Corpus complet.** |

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

## 4 ter. Qualification contractuelle — lecture des 3 contrats

### Écart contractuel **démontré** — invariant G7 inapplicable

`guard.md` **v1.0.2, statut « Stable — approuvé pour implémentation »**, pose :

> **G7** — « Si la source de vérité est **indisponible** à l'ouverture ou devient indisponible
> pendant l'attente, le guard interrompt immédiatement toute attente en cours et produit
> `command_error`. »

Le §6 définit `command_error` comme « la source de vérité est **indisponible** au moment de
l'observation », et le §9 déclare `last_observed_state` avec « valeurs possibles : `on`, `off`,
**`unknown`, `unavailable`** ».

Le §4 désigne `binary_sensor.deshumidificateur_actif` comme **seule** source de vérité. Or ce
capteur **ne peut jamais valoir `unknown` ni `unavailable`** (§4.2).

**Conséquences, toutes démontrées statiquement :**

| Élément contractuel | État réel |
|---|---|
| **G7** (invariant) | **structurellement inapplicable** — sa condition ne peut jamais être vraie |
| Verdict `command_error` (§6) | **inatteignable** |
| `last_observed_state` ∈ {`unknown`,`unavailable`} (§9) | **impossible** |
| Garde de `set_deshumidificateur_state` | morte (§4.2) |

**Qualification : écart contractuel démontré.** L'exigence violée est **G7**, ainsi que la
grammaire de verdict du §6. La cause racine est unique : `etat.yaml` **absorbe**
l'indisponibilité en `false` au lieu de la propager.

**Ce n'est pas une action physique démontrée.** L'effet matériel d'un `switch.turn_on` sur un
appareil déjà en marche est vraisemblablement nul. Le défaut est **de représentation et de
garde**, et il se propage au diagnostic (ci-dessous).

### Propagation au diagnostic — branche morte

`conformite_execution.yaml` prévoit explicitement :

```
{% elif verdict == 'command_error' %}
  unknown            (niveau)
  source_indisponible  (cause)
```

Cette branche est **morte** : le verdict qu'elle traite est inatteignable. Le capteur est
**conçu pour révéler** l'indisponibilité de la source et **ne le pourra jamais**.

**Trois niveaux affectés par une cause unique** : contrat (G7), exécution (garde), diagnostic
(branche morte).

### Ce qui n'est **pas** un écart — correction d'une lecture antérieure

`deshumidificateur.md` prescrit, pour les critères : **« en cas d'indisponibilité d'un
critère : conservation de l'état courant »**.

L'auto-référence `{{ is_state(this.entity_id, 'on') }}` de `demarrage_recommande`, de
`critere_deshumidification_cave` et de `critere_deshumidification_ha_cave` est donc
**contractuellement conforme**. Le §4 bis la rapprochait du mécanisme de C32 / L6c : le
rapprochement **technique** reste exact, mais **il ne s'agit pas d'un défaut ici** — c'est le
comportement exigé. Seule subsiste la remarque de C32 sur la fenêtre aveugle d'une entité
neuve, qui relève du mécanisme, non d'une non-conformité.

### VMC — les fichiers restants ne modifient pas la conclusion

`haute_vitesse.yaml` porte **la même garde de disponibilité** que `basse_vitesse.yaml`
(première branche `choose`, `sequence: []` sur `unavailable`/`unknown`). **Aucun writer, aucune
autorisation ni action physique supplémentaire.** Les deux scripts sont les seuls writers de
`switch.vmc_l1` / `switch.vmc_l2` : **auteur unique VMC confirmé**.

`delta_humidite_absolue_favorable.yaml` est un capteur dérivé (`| float(0)`), **sans effet de
bord**.

`alerte_nc_decision.yaml` (`10190000000005`) ne pilote aucun relais : il crée et retire une
notification persistante. Il apporte cependant un élément sur `systeme_stable` — il l'utilise
comme **trigger de re-projection post-démarrage** (« HA ne restaure pas les persistantes »), et
traite explicitement `unknown` / `unavailable` pour éteindre la notification. **Usage correct,
sans action physique.**

**Conclusion VMC inchangée par cette passe** — actée sans extrapolation.

---

## 4 quater. Corrections successives de l'audit

| Passe | Conclusion initiale | Correction |
|---|---|---|
| 1 → 2 | « branche `default` atteinte au démarrage, décisionnel `unknown` » | **Faux.** `vmc_haute_vitesse_requise` n'a pas d'`availability` : il vaut `off`. Branche « basse vitesse », décision sur valeurs de repli |
| 2 → 3 | « unicité de l'auteur non établie » | **Établie** après lecture des 8 automatisations et 2 scripts |
| 3 → 4 | « auto-référence = mécanisme de C32/L6c, fenêtre aveugle » | **Contractuellement conforme** — le contrat impose la conservation de l'état courant |
| 3 → 4 | « garde inopérante = défaut d'implémentation » | **Écart contractuel démontré** — G7 de `guard.md` rendu inapplicable |

---

## 4 quinquies. Distinction des trois événements — état final

| Événement | VMC | Déshumidificateur |
|---|---|---|
| **Reboot HA** | Chaîne watchdog armée sur fausse incohérence, **abstention** en bout de chaîne. Décision sur valeurs de repli. *Démontré statiquement.* | Réconciliation à +90 s, **recalcul fonctionnel**. Timers non restaurés → vecteurs de déclenchement. *Démontré / plausible.* |
| **Reload YAML** | **Aucun trigger dédié** dans les 11 fichiers. | **Aucun trigger dédié** dans les 15 fichiers. |
| **Reload d'intégration** | **Aucun trigger dédié.** | **Aucun trigger dédié.** |

> **L'absence de trigger dédié n'est pas une preuve d'absence d'effet.** Un reload rend les
> entités momentanément indisponibles ; les templates sans `availability` (`vmc_coherence_physique`,
> `vmc_haute_vitesse_requise`, `deshumidificateur_actif`) produiront alors les **mêmes valeurs de
> repli qu'au démarrage**, et les automatisations déclenchant sur *changement d'état* peuvent
> s'armer. **Ces effets restent indéterminables** : ils exigeraient un reload provoqué, interdit
> par le cadre du chantier.

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

## 8. Contre-audit de la vague 1

### 8.1 Perimetre et methode

Ce contre-audit porte sur les conclusions des sections 1 a 7 du present rapport,
telles que mergees en PR1. Il ne rejoue pas la cartographie : il attaque les
conclusions sensibles, cherche les contre-exemples, et produit la version
consolidee.

Methode : recherche exhaustive des ecrivains de `switch.deshumidificateur`,
`switch.vmc_l1` et `switch.vmc_l2` sur la totalite de l'arborescence de
configuration (YAML et `.storage`), et non plus sur le seul corpus metier ;
lecture integrale des fichiers decisifs ; confrontation des invariants
contractuels a la chaine reellement composee.

Limite constitutive : aucun redemarrage, aucun rechargement et aucun appel de
service n'a ete provoque. Tout point dont la causalite exige une de ces actions
est classe indeterminable, et non plausible.

### 8.2 Conclusions confirmees

- `12_template_sensors/vmc/coherence.yaml` ne declare pas d'`availability` : les
  deux relais indisponibles produisent `false and false`, soit un etat `off`
  interprete comme coherence satisfaite alors qu'aucune mesure n'a eu lieu.
- L'asymetrie avec `12_template_sensors/vmc/conformite_decision.yaml` est reelle :
  ce dernier declare une `availability` qui exige `l1` et `l2` dans `['on','off']`.
  Deux capteurs du meme domaine traitent donc l'indisponibilite de facon opposee.
- `10_scripts/vmc/basse_vitesse.yaml` et `10_scripts/vmc/haute_vitesse.yaml`
  s'abstiennent explicitement (`sequence: []`) lorsque l'un des relais est
  `unavailable` ou `unknown`.
- `12_template_sensors/deshumidificateur/etat.yaml` convertit l'indisponibilite de
  la prise en `false`.

### 8.3 Conclusions refutees

Deux affirmations de la PR1 sont refutees ou reduites par le present contre-audit.
Elles sont conservees ici en tant qu'historique, et non effacees.

#### Refutation 1 : l'auteur unique

La PR1 affirmait que chaque domaine possedait un auteur unique de la commande
physique. Cette affirmation reposait sur une recherche limitee au corpus metier.
Elargie a l'ensemble de l'arborescence, elle est fausse.

Deux ecrivains supplementaires existent :

- `10_scripts/system/transactions_bots.yaml` construit `entity: switch.deshumidificateur`
  lorsque `target_bot == 'deshumidificateur'`, puis emet en phase 2 un
  `switch.turn_on` ou un `switch.turn_off` sur cette entite.
- `18_lovelace/dashboards/vmc/diagnostic.yaml` expose deux `custom:button-card`
  heritant de `socle_toggle_confirme_indispo`, lies a `switch.vmc_l1` et
  `switch.vmc_l2`, dont le `tap_action` est un `toggle` reel.

La formulation correcte n'est donc pas auteur unique, mais auteur automatique
unique par domaine dans les scenarios etudies. Voir la taxinomie en 8.5.

#### Refutation 2 : l'ecart contractuel G7

La PR1 qualifiait la situation du deshumidificateur d'ecart contractuel demontre
sur l'invariant G7. Cette qualification est trop forte et est reduite en 8.4.

### 8.4 Conclusions requalifiees : G7 et command_error

La requalification procede en trois temps distincts, a ne pas confondre.

#### Conformite locale du guard

`10_scripts/deshumidificateur/guard_deshumidificateur.yaml` declare en en-tete
lire exclusivement `binary_sensor.deshumidificateur_actif` et ne jamais lire
`switch.deshumidificateur` comme preuve. Sur cette entree contractuelle, il
implemente G7 fidelement : verdict `command_error` avec raison
`unavailable_at_open` si l'etat observe a l'ouverture vaut `unknown` ou
`unavailable`, et `unavailable_during_wait` si l'indisponibilite survient pendant
l'attente, le `wait_template` rompant explicitement sur ces deux valeurs.

Le guard est donc localement conforme a `guard.md`. Aucune violation ne lui est
imputable.

#### Neutralisation de G7 en composition

`12_template_sensors/deshumidificateur/etat.yaml` transforme en amont
l'indisponibilite physique de la prise en `false`. En regime etabli, la situation
prevue par G7 n'atteint donc jamais le guard : l'invariant est structurellement
neutralise par la composition de la chaine, sans qu'aucun de ses deux maillons ne
soit individuellement en faute.

#### Lacune contractuelle demontree

La recherche d'un contrat imposant la conservation de `unknown` / `unavailable`
en amont du guard n'a produit aucune clause applicable. La seule clause voisine,
`contrats/deshumidificateur/deshumidificateur.md` ligne 136, prescrit la
conservation de l'etat courant en cas d'indisponibilite d'un critere : elle porte
sur les criteres de decision, non sur la source de verite.

Verdict : lacune contractuelle demontree. Aucun contrat n'assigne a `etat.yaml`
la responsabilite de propager l'indisponibilite. Il ne s'agit donc pas d'un ecart
a `guard.md`, contrairement a ce qu'affirmait la PR1.

#### Couverture partielle de command_error

`command_error` n'est pas inatteignable. Un capteur template sans valeur calculee
expose `unknown` avant sa premiere evaluation. La branche `unavailable_at_open`
reste donc atteignable dans cette fenetre, notamment au demarrage et lors d'un
rechargement des templates.

Verdict : couverture partielle de G7, et non inatteignabilite absolue.
Atteignable en fenetre transitoire ; inatteignable en regime etabli pour le
scenario que G7 vise reellement, a savoir l'indisponibilite physique de la prise.
L'etendue exacte de cette fenetre n'a pas ete mesuree, faute de pouvoir provoquer
un demarrage.

### 8.5 Taxinomie des writers

La notion d'auteur unique employee en PR1 confondait trois natures d'ecrivains.
Elles sont ici separees.

#### Writers automatiques

Ecrivains susceptibles d'emettre une commande sans intention utilisateur, sur
declencheur. Pour les deux domaines, ce sont les automatisations et scripts
metier deja cartographies en sections 4 et 7.

Conclusion confirmee : aucun d'eux ne produit d'action physique automatique au
demarrage. Les scripts VMC s'abstiennent explicitement sur relais indisponibles,
et la chaine deshumidificateur ne comporte pas d'emission declenchee par le seul
demarrage.

#### Writers manuels

Ecrivains exigeant une intention utilisateur explicite.

`18_lovelace/dashboards/vmc/diagnostic.yaml` expose deux boutons lies a
`switch.vmc_l1` et `switch.vmc_l2`. Le socle `socle_toggle_confirme_indispo`
porte un `tap_action` de type `toggle` : la commande est reelle, et elle
contourne les scripts VMC et leurs gardes d'abstention.

Deux limitations sont toutefois etablies par lecture du socle :

- une confirmation modale est obligatoire avant bascule ;
- le bloc `state` applique `pointer-events: none` des que l'entite vaut
  `unknown`, `unavailable` ou `none`.

Verdict final sur les commandes manuelles VMC : chemin de commande manuel
demontre, mais fonctionnellement neutralise pendant la fenetre transitoire
d'indisponibilite. Ce writer ne peut donc pas agir dans la phase que la vague 1
etudie. Il ne constitue en aucun cas un writer automatique au demarrage.

#### Writers transactionnels

`10_scripts/system/transactions_bots.yaml` constitue une categorie propre.

Chaine etablie par lecture integrale du fichier :

- phase 0 : `entity` resolue en `switch.deshumidificateur` lorsque
  `target_bot == 'deshumidificateur'`, avec `proof_level: B` ;
- garde d'autorisation fonctionnelle : `action not in ['turn_on', 'turn_off']`
  pour le niveau B produit `rejected_precondition` / `invalid_action` ;
- phase 2 : emission d'un `switch.turn_on` ou `switch.turn_off` sur `{{ entity }}`.
  Aucune branche `switch.toggle` n'existe.

Le lock et le cooldown produisent `rejected_busy` et `rejected_cooldown` : ils
limitent l'execution, ils ne constituent pas l'autorisation fonctionnelle, qui
releve de la matrice `proof_level` / `action`.

Recherche des appelants sur l'ensemble de l'arborescence, YAML et `.storage` :
aucune invocation. Les seules autres occurrences sont la definition elle-meme et
deux commentaires d'en-tete dans les helpers de verrou. Le script est par ailleurs
depourvu de declencheur, comme tout script.

Verdict final sur `transactions_bots.yaml` : writer supplementaire demontre, la
chaine etant suivie jusqu'a un service de commutation visant effectivement
`switch.deshumidificateur` ; mais non instrumente, faute d'appelant. Il ne peut
etre emprunte que par instruction externe explicite. Il ne peut pas s'activer
seul au demarrage ni lors d'un rechargement.

### 8.6 Points indeterminables

Les points suivants etaient qualifies de plausibles en PR1. Aucun ne peut etre
etabli sans provoquer un redemarrage ou un rechargement, ce que le cadre de la
vague 1 interdit. Ils sont donc requalifies en indeterminables, et non conserves
comme risques par prudence rhetorique.

- Rejeu de commande a partir d'un `input_text` restaure. Le comportement de
  restauration effectif n'a pas ete observe.
- Timers observes a l'etat `idle`. L'etat constate ne renseigne pas sur la
  trajectoire suivie lors d'un demarrage.
- Fenetre aveugle de l'auto-reference du deshumidificateur. Son existence decoule
  de la lecture du code, sa duree et ses effets non.
- Contournement de `input_boolean.systeme_stable` par la branche
  `trigger.platform == 'homeassistant'` de `11_automations/vmc/gestion_auto.yaml`.
  Le contournement est ecrit et lisible ; ses consequences runtime ne le sont pas.

Ces quatre points restent des objets de chantier valides. Ils ne sont pas des
constats.

### 8.7 Separation reboot, reload YAML, reload d'integration

La PR1 traitait ces trois scenarios de facon insuffisamment separee. Le
contre-audit impose la distinction suivante.

- Redemarrage complet. Recreation de toutes les entites, phase transitoire
  d'indisponibilite, puis recalcul. C'est le seul scenario pour lequel la vague 1
  produit des conclusions positives, et uniquement par lecture statique.
- Rechargement YAML. Recreation des seules entites du domaine recharge. Les
  entites d'integration ne sont pas recreees. L'absence de declencheur dedie ne
  vaut pas preuve d'absence d'effet : ce point n'a pas ete instruit.
- Rechargement d'integration. Recreation des entites portees par l'integration,
  sans recreation des entites template qui les consomment. La combinaison des deux
  n'a pas ete cartographiee.

Aucune conclusion de la vague 1 ne doit etre transposee d'un scenario a l'autre.

### 8.8 Consequences sur l'orientation des chantiers

- L'absence d'`availability` sur `12_template_sensors/vmc/coherence.yaml` reste le
  constat le plus solide de la vague 1, et le seul directement actionnable.
- La lacune contractuelle etablie en 8.4 releve d'une decision de doctrine sur la
  responsabilite de propagation de l'indisponibilite dans une chaine composee.
  Elle ne se corrige pas par un correctif local.
- La taxinomie des writers etablie en 8.5 doit etre etendue aux cinq domaines
  restants avant toute conclusion transverse sur la commandabilite.
- Les vagues suivantes doivent traiter separement les trois scenarios de 8.7.

### 8.9 Incoherences internes levees et lignes remplacees

#### Contradiction entre le paragraphe 4 quater et le paragraphe 6

Le rapport se contredisait. Le paragraphe 4 quater qualifiait la garde inoperante
d'ecart contractuel demontre. Le paragraphe 6 constatait au contraire que les
trois contrats du domaine n'avaient pas ete lus, et que le defaut du paragraphe
4.2 etait donc decrit, non qualifie en ecart contractuel.

Les contrats ayant desormais ete lus, la contradiction est levee en faveur de la
prudence du paragraphe 6, et non de l'affirmation du paragraphe 4 quater. La
qualification retenue est celle du paragraphe 8.4 : conformite locale du guard,
neutralisation de G7 en composition, lacune contractuelle demontree.

#### Lignes du paragraphe 4 quater remplacees

Le tableau des corrections successives du paragraphe 4 quater est conserve tel
quel a titre d'historique. Deux de ses lignes sont remplacees par le present
contre-audit et ne doivent plus etre citees comme conclusions :

| Ligne du 4 quater | Statut apres contre-audit | Renvoi |
|---|---|---|
| Passe 2 vers 3 : unicite de l'auteur etablie | Refutee. Deux ecrivains supplementaires demontres | 8.3 et 8.5 |
| Passe 3 vers 4 : ecart contractuel demontre sur G7 | Reduite. Lacune contractuelle, sans ecart a `guard.md` | 8.4 |

#### Articulation avec le paragraphe 4 quinquies

Le paragraphe 8.7 ne remplace pas le paragraphe 4 quinquies, qui distinguait deja
les trois evenements et posait correctement que l'absence de declencheur dedie ne
vaut pas preuve d'absence d'effet. Il y ajoute une seule regle : aucune conclusion
etablie pour un evenement ne peut etre transposee a un autre, meme lorsque le
mecanisme sous-jacent parait identique.
