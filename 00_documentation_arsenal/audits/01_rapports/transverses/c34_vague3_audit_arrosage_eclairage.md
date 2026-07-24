# C34 — Vague 3 : audit arrosage et éclairage

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 3 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaines** | Arrosage (Rain Bird / pont externe) · Éclairage |
| **Date** | 2026-07-24 |
| **Nature** | Audit statique. **Aucun reboot, reload, appel de service ni changement d'état n'a été provoqué.** |
| **Couverture** | **68 fichiers runtime** (arrosage 6+3+14 = 23 ; éclairage 27+6+12 = 45), plus les contrats confrontés (`arrosage/17_decision_v1.md`, `03_coexistence_rainbird.md`, `11_mode_manuel_supervise.md` ; `eclairage/sejour.md`, `entree.md`, `jardin.md`). Décisives lues intégralement ; inertes (diagnostics/notifications sans écrivain physique ni trigger de démarrage) échantillonnées. |

> **Règle appliquée (identique aux vagues 1 et 4).** Une affirmation sur l'action physique n'est
> marquée *démontrée statiquement* que si la chaîne a été suivie **jusqu'au service appelé** et que
> triggers et conditions applicables ont été lus. Tout point dont la causalité exige un reboot, un
> reload ou un appel de service **provoqué** est classé **indéterminable**, jamais « plausible ».

---

## 1. Frontière entre les événements

| Événement | Arrosage | Éclairage |
|---|---|---|
| **Redémarrage HA** | **3 automatisations** portent `platform: homeassistant, event: start` : `declenchement` (`…002`), `session_fin_watchdog` (`…006`), `coexistence_rain_delay` (`…003`). | Les **4 extinctions** (`sejour/off …015`, `jardin/soir/extinction …004`, `entree/extinction`, `garage/extinction_automatique`) portent `event: start`. La `jardin/soir/allumage …003` et les 3 `simulation_presence` réagissent à `systeme_stable → on`. |
| **Reload YAML** | **Aucun trigger dédié.** | **Trigger dédié `event_type: automation_reloaded`** sur les 4 extinctions — **premier domaine de l'audit à traiter explicitement le reload YAML** (les vagues 1 et 4 n'en avaient trouvé aucun). |
| **Reload d'intégration** | **Vecteur propre et fort** : le pont Rain Bird (ESP32 BLE/Wi-Fi) rend `unavailable` ses capteurs et son `switch.…_station_1` à la recomposition. | Les `switch.*` et `binary_sensor.mouvement_*` (Zigbee) recomposent `unavailable → …`. |

**Rappel du cadrage** : `systeme_stable` ne retombe qu'au **reboot HA** (établi en vague 4). Les
conclusions au **reload d'intégration** ne se transposent donc pas du reboot.

---

## 2. Arrosage — boot-safe par double garde de disponibilité

### 2.1 Chaîne décision → action

| Rôle | Composant |
|---|---|
| Décision (pure) | `binary_sensor.arrosage_intention` (7 gardes ET, contrat 17 §3) |
| Gardes de disponibilité du pont | `binary_sensor.rain_bird_pont_donnees_disponibles`, `…preconditions_runtime` (lisent heartbeat/uptime/version/active_station, BLE/Wi-Fi/batterie) |
| Cooldown | `sensor.arrosage_dernier_effectif` (**trigger-based, `device_class: timestamp`, restauré au reboot**) |
| Application (start) | `automation …002` → `script.arrosage_rain_bird_station_1_courte_supervisee` → `switch.turn_on` station 1 |
| Fin / reprise / watchdog | `automation …006` → `script.…stop_supervise` (`button.stop_all_irrigation`) — **n'arrose jamais** |
| Coexistence | `automation …003` → `script.…rain_delay_appliquer` (`number.set_value` rain_delay) |
| Équipement | `switch.rain_bird_bat_bt_2_e9a3_station_1` (preuve primaire) |

### 2.2 Pas de démarrage d'arrosage injustifié au reboot — **démontré statiquement**

`declenchement …002` déclenche sur `homeassistant start` **sous condition
`binary_sensor.arrosage_intention == on`**. Or l'intention n'est `on` que si (entre autres)
`pont_donnees_disponibles == on` **ET** `preconditions_runtime == on` — deux gardes qui lisent des
capteurs du **pont externe** (heartbeat, uptime, version, active_station, BLE/Wi-Fi RSSI, batterie).
Au démarrage, ce pont BLE/Wi-Fi est **indisponible** le temps de sa reconnexion : ses capteurs valent
`unavailable` ⇒ intention `off` ⇒ la condition de `…002` est fausse ⇒ **aucun `switch.turn_on`**.

**Double garde.** Même si l'intention était `on` à l'instant du trigger `start`, le **script exécutif**
re-vérifie ses propres gardes (`dispo_ok and precond_ok and station idle and switch off`) et **refuse**
(notification, `stop`) sinon — abstention en bout de chaîne, exactement comme le script VMC de la vague 1.
Décision **et** exécutant lisent la disponibilité du pont : convergence sûre.

**Qualification §2 : abstention temporaire** (par la disponibilité du pont), non par une garde ajoutée.
Un démarrage d'arrosage **postérieur** (pont revenu, intention `on` en fenêtre) serait la décision
nominale sur donnée fraîche — **recalcul fonctionnel**, non un artefact de reboot.

### 2.3 Le cooldown survit au reboot — **démontré statiquement**

`arrosage_intention` neutralise sa garde cooldown quand `arrosage_dernier_effectif ∈
{unknown, unavailable, none, ''}` (`cooldown_ok = true`). Le risque serait donc un **sur-arrosage**
si l'horodatage était perdu au reboot. Il ne l'est pas : `arrosage_dernier_effectif` est un capteur
**trigger-based** `device_class: timestamp`, dont l'en-tête grave « valeur restaurée au redémarrage »
— comportement conforme aux capteurs trigger-based de HA (RestoreEntity). Le cooldown **reste
opérant** après reboot. **La garde anti sur-arrosage n'est pas contournée.**

### 2.4 Fin / reprise / coexistence — **recalcul / continuité**

- `session_fin_watchdog …006` (`start`) **n'arrose jamais** : il **solde** une session orpheline
  dont l'échéance est passée (stop supervisé, verdict `close_reprise`), et **s'abstient** si l'échéance
  est encore future (le trigger `echeance` réarmé sur l'input_datetime tirera à l'heure dite).
  **Recalcul fonctionnel** ; le stop est idempotent et prouvé par le switch natif.
- `coexistence_rain_delay …003` (`start`) réaffirme le paramètre `rain_delay` **via un script gardé**
  (`dispo_ok and frais_ok`) : au reboot, pont indisponible ⇒ pas d'écriture. `rain_delay` n'est **pas**
  une commande d'irrigation ; il neutralise le programme de secours interne, et est **fail-safe** (si
  HA disparaît, il expire, le secours reprend). **Restauration** d'un paramètre de coexistence, gardée.

### 2.5 Reload d'intégration Rain Bird — absorbé par la couche décision

Le vecteur « recomposition `unavailable → on` » qui a produit le Finding B de l'alarme **n'existe pas
ici** : `declenchement …002` déclenche sur `arrosage_intention` (un **template décisionnel**
availability-aware qui vaut `off` dès qu'une source est indisponible), **non** sur le `switch.*` brut.
La couche décision ne « recompose » pas vers un `on` parasite. `session_fin_observee` et le watchdog
lisent le switch, mais **ne démarrent jamais** (stop/observe seulement). **Aucun vecteur de démarrage
au reload d'intégration.**

**Verdict arrosage : aucun défaut candidat.** Domaine **boot-safe démontré statiquement**, doublement
gardé (décision availability-aware + exécutant supervisé), cooldown restauré, chemins de fin sans start.

---

## 3. Éclairage — extinctions ré-assertées, une asymétrie de front

### 3.1 Extinctions : rattrapage d'un OFF calculé — **restauration / recalcul fonctionnel**

Les **4 extinctions** (`sejour/off …015`, `jardin/soir/extinction …004`, `entree/extinction`,
`garage/extinction_automatique`) déclenchent sur `deadline` (time) **+ `homeassistant start` + `automation_reloaded`**,
avec un délai (`90 s` au start, `10 s` au reload) et une **condition idempotente stricte** :

```
mouvement <zone> == off  ET  <auto/state> == on  ET  <switch/état> == on
ET  deadline ∉ {unknown, unavailable, none, ''}  ET  now() >= deadline
```

L'action `switch.turn_off` n'est émise **que si la deadline persistée (input_datetime restauré) est
réellement dépassée et la lampe encore allumée**. C'est un **rattrapage** d'une extinction **due** —
le système ne maintient pas aveuglément l'état antérieur, il **ré-applique la décision temporelle
déjà échue**. Une deadline **future** (lampe légitimement allumée dans sa fenêtre) ⇒ condition fausse
⇒ **aucune extinction**. Une deadline `unknown` au boot ⇒ condition fausse ⇒ pas d'extinction.

**Qualification §2 : restauration / recalcul fonctionnel.** L'extinction au boot/reload est **justifiée**
(l'heure d'éteindre est passée) ⇒ **pas** « action physique indésirable ». **Point positif notable** :
c'est le **seul domaine de l'audit** traitant explicitement le **reload YAML** (`automation_reloaded`),
là où l'alarme et le traitement de l'air laissaient ce cas *indéterminable*.

### 3.2 Allumage au boot : rattrapage gardé — **recalcul fonctionnel**

`jardin/soir/allumage …003` est le seul **allumage** réagissant à un signal de démarrage, et il le fait
sur `systeme_stable → on` (le signal **stabilisé à +45 s**, pas le `start` brut), sous conditions
`systeme_stable on` **ET** `cycle_soir on` **ET** `presence on` **ET** `switch off` (idempotent). Il
ré-établit l'état « soir + présence ⇒ jardin allumé ». Les `simulation_presence` (entrée / chambre /
garage) ré-appliquent de même leur **plage horaire** à `systeme_stable → on`, sous garde
`simulation_presence_autorisee` (mode absence). **Recalcul fonctionnel gardé** ; l'allumage au boot est
**plus** gardé que l'extinction (systeme_stable + présence/plage), choix de conception défendable :
allumer exige plus qu'éteindre.

### 3.3 Finding E1 (candidat) — allumages sur front `to: 'on'` sans `from:`

**Démontré statiquement (asymétrie) ; effet runtime indéterminable ; faible conséquence.**

`sejour/on …014` déclenche sur `binary_sensor.mouvement_sejour` **`to: "on"` sans `from:`**, et
`garage/allumage_automatique` de même (`mouvement_garage`/contact `to: "on"`). À l'inverse,
`entree/automatique …026` porte **`from: "off"`** explicite. Une transition `unavailable → on`
(recomposition Zigbee au **reload d'intégration**, ou au reboot pendant la fenêtre non gardée par
`systeme_stable` — ces allumages ne le consultent pas) **satisfait** un trigger `to: 'on'` sans `from`,
et — si `<auto> on`, lampe `off`, période sombre — **allume la lampe**.

C'est **structurellement le Finding B de l'alarme**, transposé à l'éclairage : deux automatisations
sœurs, l'une restauration-safe (`from: 'off'`), l'autre non. **Différence majeure : la conséquence est
un éclairage**, non un déclenchement de sirène ou d'alarme ⇒ **faible gravité**. **Effet indéterminable**
(dépend de la republication Zigbee `unavailable → on` d'un capteur de mouvement, non démontrable sans
provoquer le reload) ; **guard-gap démontré statiquement** ; qualification **lacune** probable (à
confronter précisément aux contrats `sejour.md` / `garage.md` en contre-audit), **non écart**.

### 3.4 Sans effet physique / hors boot

- `garage/recalage_nocturne_booleen …025` : recale un **booléen logique** (`garage_light_state`) à
  02/03/04 h, **jamais d'action physique** (« n'appelle jamais `button.garage` »). Hors boot.
- `simulation_presence/system …008` : orchestration horaire (sunrise −90 min), génère des horaires
  via script. Hors boot, pas de pilotage direct.
- Astronomie (`activation`/`desactivation`), sapin (`on`/`off`), `maj_heure_*`, `ecriture_deadline`,
  `mouvements_sejour` : chemins horaires / d'écriture de deadline / d'enregistrement, sans trigger de
  démarrage physique. `notification`/diagnostics : sans effet matériel.

---

## 4. Synthèse par événement et qualification

| Conclusion | Domaine · Événement | Qualification §8 | Grille §2 |
|---|---|---|---|
| Pas de démarrage d'arrosage au reboot (pont indisponible) | Arrosage · Reboot | Démontré statiquement | Abstention temporaire |
| Cooldown restauré (timestamp trigger-based) | Arrosage · Reboot | Démontré statiquement | Continuité légitime |
| Reprise/fin sans start ; coexistence gardée fail-safe | Arrosage · Reboot | Démontré statiquement | Recalcul / restauration |
| Reload d'intégration absorbé par la décision availability-aware | Arrosage · Reload intégr. | Démontré statiquement | Continuité légitime |
| Extinctions = rattrapage d'un OFF calculé, deadline-gaté | Éclairage · Reboot + **Reload YAML** | Démontré statiquement | Restauration / recalcul fonctionnel |
| Allumage jardin au boot gardé (systeme_stable + présence + cycle) | Éclairage · Reboot | Démontré statiquement | Recalcul fonctionnel |
| **Finding E1** — allumage sur `to:'on'` sans `from:` (séjour, garage) | Éclairage · Reload intégr. Zigbee | **Indéterminable** (effet) ; guard-gap démontré statiquement | Action physique indésirable — **candidate, faible gravité** |

---

## 5. Convergence transverse

- **Arrosage est le domaine le plus boot-safe de l'audit à ce jour** : double garde de disponibilité
  (décision *et* exécutant), couche décision availability-aware qui neutralise la recomposition, cooldown
  restauré. **Aucun candidat.**
- **Éclairage** apporte le **premier traitement explicite du reload YAML** (`automation_reloaded`) et un
  motif d'extinction **exemplaire** (rattrapage d'un OFF calculé, idempotent, deadline-gaté).
- **Finding E1 partage la signature du Finding B (alarme)** : trigger `to: 'on'` **sans `from:`** sur un
  capteur qui recompose `unavailable → on`, garde `systeme_stable` **implicitement bornée au reboot HA**
  et non érigée en invariant. **Même racine doctrinale** que celle consolidée en vague 4 (§13.6). E1 est
  hiérarchiquement **sous** les findings A/B de l'alarme : conséquence = éclairage, gravité faible.

---

## 6. Limites probatoires

- **Aucune preuve runtime nouvelle** ; la preuve L4 d'origine classait arrosage et éclairage
  *indéterminables* (vanne Rain Bird / lampes hors allowlist Recorder, aucune entité `light.`). Le
  présent audit établit **statiquement** ce que L4 ne pouvait trancher.
- E1 repose sur la republication Zigbee `unavailable → on` d'un capteur de mouvement — **non observable**
  sans provoquer un reload d'intégration, interdit par le cadre.
- Le signal de présence (`presence_famille_securite`) consommé par l'allumage jardin relève de **D-PRES /
  C33** et n'est pas ré-audité ici.
- **Asymétrie 27 automatisations / 7 contrats** (cadrage) : instruite partiellement — les extinctions et
  allumages de séjour/entrée/jardin/garage sont contractualisés ; simulation de présence, sapin,
  astronomie relèvent de contrats plus légers ou implicites. La **complétude contractuelle** de
  l'éclairage est une **dette documentaire** distincte de C34, à signaler au portefeuille.

---

## 7. Suite

Cette vague **n'ouvre aucun sous-chantier correctif** (stop point du cadrage §10). **Finding E1** est
versé au **portefeuille C34** (livrable 3) sous les findings A/B de l'alarme (même racine, gravité
moindre). Arrosage est consigné **sans finding** (résultat positif). Le **contre-audit de la vague 3**
(attaquer E1, chercher les contre-exemples, confronter au contrat `sejour.md`/`garage.md`, vérifier la
restauration effective de `arrosage_dernier_effectif` et des input_datetime de deadline) reste à conduire
avant toute orientation.
