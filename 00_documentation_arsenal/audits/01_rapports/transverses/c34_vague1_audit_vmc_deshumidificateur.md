# C34 — Vague 1 : audit VMC et déshumidificateur

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 1 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaines** | VMC · déshumidificateur |
| **Date** | 2026-07-21 |
| **Nature** | Audit statique. **Aucun reboot, reload, appel de service ou changement d'état n'a été provoqué.** |
| **Couverture** | **11 fichiers lus sur 26** + contrat VMC (§1-2) + `contrats/deshumidificateur/` non lu. Couverture partielle **assumée et bornée** (§6). |

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

De plus, la branche `default` du `choose` — atteinte lorsque
`binary_sensor.vmc_haute_vitesse_requise` n'est ni `on` ni `off`, donc `unknown` au
démarrage — appelle `script.vmc_basse_vitesse`.

**Conséquence** : au redémarrage, si les relais sont déjà disponibles alors que le capteur
décisionnel n'est pas encore calculé, une action physique peut être émise **sur la base d'un
état décisionnel non encore établi**, sans que `systeme_stable` ne s'y oppose.

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

## 5. Portée réelle des doctrines transverses

**Non établie.** `resilience_integrations.md` et `ups_arret_ha.md` **n'ont pas été lus** dans
cette vague. Conformément à la consigne, ils ne sont **pas** invoqués par proximité
sémantique. Leur portée reste à établir.

---

## 6. Limites probatoires de cette vague

**Fichiers lus (11 / 26)** : VMC — `watchdog`, `synchro_booleen`, `gestion_auto`,
`coherence`, `intention`, `basse_vitesse`. Déshumidificateur — `reconciliation_demarrage`,
`blocage_redemarrage`, `activation`, `etat`, `guard_deshumidificateur`, `forcer_etat`.

**Non lus** : VMC — `alerte_nc_decision`, `haute_vitesse` (script),
`conformite_decision`, `haute_vitesse_requise`, `delta_humidite_absolue_favorable`.
Déshumidificateur — `desactivation`, `ouverture_cycle`, `fermeture_cycle`, `retry_on`,
`retry_off`, `demarrage_recommande`, `conformite_execution`, les deux critères d'humidité,
et les 3 contrats du domaine.

**Conséquences directes** :

- les capteurs **décisionnels** des deux domaines n'ont pas été lus : aucune conclusion n'est
  émise sur leur comportement en `unknown` ;
- les automatisations `retry_on` / `retry_off` n'ont pas été lues : **le risque de rejeu n'est
  pas évalué** ;
- l'unicité de l'auteur de commande n'est pas établie sur l'ensemble du domaine ;
- **aucune preuve runtime** n'a été mobilisée : toutes les conclusions ci-dessus sont
  statiques.

---

## 7. Suite

Compléter la lecture des 15 fichiers restants et des contrats du déshumidificateur, puis
conduire le **contre-audit** prévu par C34. Le défaut du §4.2 devra être confronté aux
contrats `contrats/deshumidificateur/` avant toute orientation corrective.

---
