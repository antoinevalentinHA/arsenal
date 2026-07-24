# C34 — Vague 4 : audit du domaine alarme

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 4 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaine** | Alarme (traité seul, cf. cadrage §7). |
| **Date** | 2026-07-24 |
| **Nature** | Audit statique. **Aucun reboot, reload, appel de service ni changement d'état n'a été provoqué.** Réutilise la preuve runtime L4 déjà acquise (§5.6 du cadrage), sans en produire de nouvelle. |
| **Couverture** | **30 / 30 fichiers runtime lus** (14 automatisations, 9 scripts, 7 templates), plus le panneau `16_template_alarm_panels/alarme_maison.yaml`, l'automatisation de stabilisation `system/stabilisation_post_demarrage.yaml`, la reconstruction visiteur `presence/visite/securite_reboot.yaml`, le watchdog `system/reload_integrations/zigbee.yaml`, et les contrats `50_intrusion_detection.md` / `70_sirene_actions_terminales.md`. |

> **Sémantique inversée (rappel du cadrage §7).** L'alarme est le seul domaine où **ne pas
> restaurer** un état antérieur peut être le comportement **correct** (révocation de sécurité).
> La grille de lecture y est donc inversée : un armement, un désarmement ou une mise sous sirène
> déclenchés **par la seule opération technique** sont suspects, mais le maintien aveugle de
> l'état antérieur ne vaut pas davantage garantie.

> **Règle appliquée (identique à la vague 1).** Une affirmation sur l'action physique n'est
> marquée *démontrée statiquement* que si la chaîne a été suivie **jusqu'au service appelé**
> et que triggers et conditions applicables ont été lus. Tout point dont la causalité exige un
> reboot, un reload ou un appel de service **provoqué** est classé **indéterminable**, jamais
> « plausible » (discipline du contre-audit de la vague 1, §8.6).

---

## 1. Frontière entre les événements

Quatre événements sont distingués — les trois du cadrage, plus un quatrième **propre au
domaine** : le redémarrage du bridge Zigbee2MQTT, qui rend `unavailable` les capteurs de
sécurité (contacts, mouvement) sans redémarrer Home Assistant.

| Événement | Signal technique dans les sources lues |
|---|---|
| **Redémarrage HA** | Aucune automatisation d'alarme ne porte de trigger `homeassistant start` direct. Le seul vecteur post-boot est `input_boolean.systeme_stable → on`, posé **à +45 s** par `system/stabilisation_post_demarrage.yaml` (§2). |
| **Reload YAML** | **Aucun trigger dédié.** Un reload YAML du package alarme recrée ses templates et helpers ; il ne recharge **pas** l'intégration Zigbee, donc ne rend pas les contacts `unavailable`. |
| **Reload d'intégration Zigbee** | **Aucun trigger dédié**, mais effet propre : contacts et détecteurs passent `unavailable` puis se recomposent. `systeme_stable` **reste `on`** (il ne retombe qu'au reboot HA — §2). |
| **Indisponibilité d'observation** | Traitée inégalement selon les automatisations (I5, gardes `from`, `to_state`) — c'est l'objet des §5-§6. |

**Conséquence méthodologique.** Comme en vague 1, les conclusions positives portent d'abord
sur le **redémarrage HA**. Mais l'alarme ajoute un vecteur que la vague 1 n'avait pas : le
**redémarrage d'intégration Zigbee**, non couvert par la garde `systeme_stable`. Il est traité
au §6.

---

## 2. Le repère temporel : `systeme_stable` à +45 s

`system/stabilisation_post_demarrage.yaml` (ID `10120000000018`) est le **seul** producteur de
`input_boolean.systeme_stable` : sur `homeassistant start`, il pose `off`, attend **45 s** fixes,
puis pose `on`. **Recherche confirmée** : aucune autre automatisation ne remet `systeme_stable`
à `off`. Il ne retombe donc **jamais** hors d'un redémarrage complet de HA — ni au reload YAML,
ni au redémarrage d'une intégration.

Ce délai de 45 s est le pivot de tout le comportement au reboot de l'alarme. Il est
**strictement inférieur** au `delay_on: 5 min` de la projection d'absence (§4) et **supérieur**
au `delay_on: 15 s` de la projection de présence (§4). Cette double inégalité — 15 s < 45 s <
5 min — détermine ce que l'alarme peut et ne peut pas faire à l'instant où elle « se réveille ».

---

## 3. Chaîne décision → action reconstituée

| Rôle | Composant | Démonstration |
|---|---|---|
| Observation présence | `binary_sensor.presence_famille_securite` (brut, partagé — hors périmètre alarme, cf. D-PRES) | lu indirectement |
| Projection désarmement | `binary_sensor.presence_famille_securite_confirmee_alarme` (`delay_on 15 s`) | lu |
| Projection armement | `binary_sensor.presence_famille_securite_absence_confirmee_alarme` (`delay_on 5 min`) | lu |
| Décision (pure) | `script.alarme_decision_centrale` → `input_text.alarme_decision` / `alarme_etat_cible` / `alarme_raison` | lu |
| Application | `automation 10020000000027` (trigger `systeme_stable → on` + états métier ; **condition `systeme_stable == on`**) | lu |
| Action physique (nominale) | `script.alarme_armer` / `script.alarme_desarmer` → `alarm_arm_away` / `alarm_disarm` | lu jusqu'au service |
| Action physique (intrusion) | `alarm_control_panel.alarm_trigger` **appelé directement** par `…009`, `…007`, `…032` (dette §9 du contrat 50, assumée) | lu jusqu'au service |
| Sirène | `alarm_control_panel → triggered` → `automation 10020000000011` → `script.sirene_brutale` (MQTT `warning/burglar`) | lu jusqu'au service |
| Équipement | `alarm_control_panel.alarme_maison` (**`platform: manual`**, `trigger_time: 180`) | lu |

La décision centrale est un **cerveau pur** (n'agit jamais sur le panneau) ; l'application est
le **seul écrivain automatique nominal** du panneau, doublé par trois appels directs
d'`alarm_trigger` sur le chemin intrusion (dette architecturale contractualisée, contrat 50 §9).
Aucun écrivain du panneau hors du domaine : `presence/high_accuracy_{on,off}.yaml` **lisent**
seulement l'état `armed_away` en condition.

---

## 4. Comportement au redémarrage HA — chemin nominal

### 4.1 Auto-armement impossible au point de bascule — **démontré statiquement**

À `systeme_stable → on` (+45 s), l'application recalcule la décision. Pour atteindre
`ARMED_AWAY`, la décision exige `absence_stable == on`, soit
`binary_sensor.presence_famille_securite_absence_confirmee_alarme` à `on`. Or ce capteur porte
`delay_on: 5 min` et est **recréé au reboot** : 45 s après le démarrage, son `on` ne peut pas
encore être confirmé. La décision retombe donc sur `ABSENCE_NON_STABLE → NOOP`, et le garde-fou
de l'application (`cible_calculee in ['DISARMED','ARMED_AWAY']`) bloque toute action sur `NOOP`.

**Aucun armement n'est émis au réveil du système.** Qualification §2 : **abstention temporaire**,
obtenue **par construction du délai d'absence**, non par une garde ajoutée.

Un armement **ultérieur** reste possible : si l'absence réelle persiste, le capteur d'absence
bascule `on` à +5 min, ce qui re-déclenche l'application (il figure dans ses triggers d'état) et
produit `ARMED_AWAY`. C'est un **recalcul fonctionnel sur donnée fraîche** (l'absence est
réellement confirmée 5 min), **non un rejeu** de l'état antérieur.

### 4.2 Auto-désarmement conditionné à une présence réelle — **démontré statiquement**

Le désarmement automatique exige `presence_securite == on`
(`presence_famille_securite_confirmee_alarme`, `delay_on 15 s`) ou `presence_visiteur == on`.
Deux propriétés protègent le reboot :

- le capteur calcule `is_state(brut, 'on')`, qui vaut **False** si le brut est `unknown` /
  `unavailable` : un capteur non encore recomposé **ne désarme jamais** ;
- `delay_on 15 s` impose une présence **soutenue** 15 s avant de confirmer, filtrant les blips
  (jitter GPS / BSSID, cf. D-PRES).

À +45 s, si la famille est réellement présente depuis ≥ 15 s, la décision vaut `PRESENCE →
DISARMED` et l'alarme se désarme si le panneau a été restauré à `armed_away`. Qualification §2 :
**recalcul fonctionnel** (désarmer une alarme alors que la famille est réellement là est
correct) ; en l'absence de présence réelle, **continuité légitime** de l'état restauré.

### 4.3 Reconstruction du contexte visiteur — **démontré statiquement**

`presence/visite/securite_reboot.yaml` (`10210000000005`), déclenché lui aussi par
`systeme_stable → on`, réaligne `input_boolean.presence_visiteur` / `visite_en_cours` sur
`binary_sensor.creneau_visiteur_actif`. Ces booléens **nourrissent** la décision centrale
(`VISITEUR_PRESENT → DISARMED`). Qualification §2 : **restauration** délibérée d'un contexte
métier. La course potentielle avec l'application (même trigger `systeme_stable → on`) est
**résolue par re-déclenchement** : l'application liste `input_boolean.visite_en_cours` dans ses
triggers d'état, donc tout réalignement postérieur la relance. Cohérence à terme établie.

### 4.4 Intrusion neutralisée pendant la fenêtre de 45 s — **démontré statiquement**

Les **trois** automatisations d'intrusion (`…009` mouvement, `…007` ouverture, `…032` fin de
délai) portent la condition `input_boolean.systeme_stable == on`, explicitement libellée
« anti-recomposition post-reboot ». Pendant les 45 s de stabilisation, `systeme_stable` est `off`
⇒ **aucune détection ne peut déclencher le panneau**. Qualification §2 : **abstention
temporaire**, par garde explicite. C'est le pendant, côté détection, du délai d'absence côté
armement.

### 4.5 Panneau `manual` restauré — **restauration (probable, HA-interne)**

`alarme_maison` est un `alarm_control_panel: platform: manual`. HA restaure l'état antérieur du
panneau au démarrage (RestoreEntity). Le comportement exact — notamment la restauration d'un
état transitoire (`arming`, `pending`, `triggered`) et la reprise du décompte `trigger_time` —
est **interne à HA et non démontrable par les sources du dépôt**. Qualification §8 : **probable
mais non prouvé** pour le mécanisme ; §2 : lorsque la décision recalcule `NOOP`, l'état restauré
est **maintenu** — **continuité légitime**.

---

## 5. Finding A — la mise sous sirène n'est pas gardée `systeme_stable`

**Démontré statiquement (absence de garde) ; effet runtime indéterminable.**

`automation 10020000000011` (sirène forte) déclenche sur
`alarm_control_panel.alarme_maison → triggered` (aucun `from:`) et ne porte **qu'une** garde :
`input_boolean.mode_test_alarme == off`. Elle **n'a pas** la garde `systeme_stable == on` que
portent les trois automatisations d'intrusion (§4.4). Son action est
`script.turn_on: script.sirene_brutale`, soit une publication MQTT `warning/burglar` à volume
maximal.

**Asymétrie démontrée** : trois automatisations sœurs du même domaine gardent la
recomposition post-reboot ; l'automatisation terminale qui **produit le son** ne la garde pas.
C'est structurellement le même type de constat que l'asymétrie VMC de la vague 1 (deux capteurs
voisins, traitements opposés de l'indisponibilité).

**Vecteur candidat** : si le panneau `manual` restaure l'état `triggered` au reboot, et si cette
restauration émet un changement d'état satisfaisant `to: triggered`, la sirène est **rejouée**
(nouvelle commande `burglar` pleine durée), hors de tout chemin d'intrusion gardé.

**Pourquoi indéterminable** : deux maillons dépendent du comportement interne de HA — (a) le
panneau `manual` restaure-t-il `triggered` (plutôt que l'état armé de repli) ? (b) une
restauration d'état émet-elle un événement satisfaisant un trigger `to:` sans `from:` ? Aucun
des deux n'est démontrable par les sources du dépôt, et le cadre C34 interdit de provoquer un
reboot pour l'observer.

**Confrontation contractuelle** (`70_sirene_actions_terminales.md`) : le contrat garantit la
**reboot-safety de l'extinction** (le décompte vit dans le device, `number.sirene_max_duration`),
mais **ne traite pas la ré-ignition** au reboot. I6 du contrat 50 (« sirène forte uniquement sur
intrusion confirmée / mouvement réel armé ») est énoncé pour les **appelants d'intrusion** ; la
sirène pilotée par la **transition d'état `triggered`** en est un chemin distinct, non couvert
par I6. Il ne s'agit donc **pas** d'un écart contractuel démontré, mais d'une **lacune de
couverture** (aucune clause n'assure que le passage à `triggered` par restauration ne rejoue pas
la sirène). Même forme de conclusion qu'en vague 1 (lacune, non écart).

---

## 6. Finding B — l'intrusion « ouverture » n'est restauration-safe qu'au reboot HA

**Démontré statiquement (asymétrie + périmètre de la garde) ; effet runtime indéterminable.**

`automation 10020000000007` (intrusion ouverture) déclenche sur une liste de
`binary_sensor.contact_*` avec **`to: 'on'` sans `from:`**. Ses gardes : `systeme_stable == on`,
`trigger.to_state.state not in ['unknown','unavailable']`, `armed_away`, `delai_desarmement == off`.

Deux propriétés se combinent en angle mort :

1. **`to: 'on'` sans `from:`** — une transition `unavailable → on` **satisfait** le trigger. La
   garde I5 (`to_state not in unknown/unavailable`) contrôle l'état **d'arrivée** (`on`, valide),
   **pas** l'état de départ. À l'inverse, l'automatisation **mouvement** (`…009`) porte
   `from: 'off'` explicite et **ne matche pas** `unavailable → on`. Le contrat 50 codifie
   d'ailleurs cette asymétrie (« front off → on » pour le mouvement, « transition vers on » pour
   l'ouverture).
2. **`systeme_stable` ne retombe qu'au reboot HA** (§2). Lors d'un **redémarrage du bridge
   Zigbee2MQTT** — déclenché automatiquement par le watchdog `system/reload_integrations/zigbee.yaml`
   (`10120000000010`, `hassio.addon_restart`) ou manuellement — les contacts passent
   `unavailable` puis se recomposent, **pendant que `systeme_stable` reste `on`**. La garde
   « anti-recomposition post-reboot » est alors **inopérante**, car ce n'est pas un reboot.

**Vecteur candidat** : alarme `armed_away`, redémarrage du bridge Zigbee, un contact se recompose
`unavailable → on` ⇒ `…007` déclenche `alarm_trigger` (puis sirène via §5). Les contacts nourrissant
le **délai d'entrée** échappent à ce risque (chaîne `ouvrants_entree` trigger-based → front
`off → on` sur `delai_entree_start`, dont l'en-tête grave « un état restauré à on au redémarrage
ne vaut pas nouvelle ouverture ») ; mais les contacts **fenêtres / pièces** de `…007` empruntent
le chemin **instantané**, qui ne bénéficie pas de cette protection.

**Pourquoi indéterminable** : établir l'effet exigerait de savoir si Zigbee2MQTT republie un
contact **réellement ouvert** comme `unavailable → on` (plutôt que de restituer son état retenu),
et si ce cas se présente **alors que l'alarme est armée**. Ces points dépendent du comportement de
l'intégration à la recomposition — non démontrable par les sources, et le cadre C34 interdit de
provoquer le redémarrage.

**Confrontation contractuelle** (`50_intrusion_detection.md`) : I5 impose d'ignorer `unknown` /
`unavailable`, ce que `…007` fait **sur l'état d'arrivée**. Aucune clause n'impose que la
**transition source** soit `off` (restauration-safety). C'est une **lacune** — non un écart :
le contrat lui-même décrit `…007` comme « transition vers on » sans front. La garde
`systeme_stable`, présentée comme « anti-recomposition », est **implicitement bornée au reboot HA**
sans que le contrat n'expose cette limite.

---

## 7. Reload YAML — appuyé sur la preuve runtime L4

**Démontré par preuve runtime existante (panneau) + démontré statiquement (contacts).**

La preuve L4 déjà acquise (cadrage §5.6) établit qu'au **reload**,
`alarm_control_panel.alarme_maison` **ne change pas d'état** (signal propre, aucun effet). Le
panneau ne passe donc pas par `triggered` ⇒ le Finding A n'est **pas** activé par un reload YAML.

Statiquement : un reload YAML du package alarme recrée ses templates et helpers, mais **ne
recharge pas l'intégration Zigbee** ⇒ les contacts restent `available`, sans transition
`unavailable → on` ⇒ le Finding B n'est **pas** activé par un reload YAML. Les projections de
présence/absence sont recréées ; leurs `delay_on` (15 s / 5 min) rejouent le même filtrage qu'au
reboot, sans `systeme_stable` pour garder l'application — mais l'application **conserve** sa
condition `systeme_stable == on`, qui reste vraie (pas de reboot), si bien qu'un recalcul peut
survenir sur les valeurs de repli des projections recréées. **L'ampleur exacte de cette fenêtre
de recréation des templates au reload YAML n'est pas mesurable sans provoquer le reload** →
qualifiée **indéterminable**, cohérente avec la même réserve en vague 1 (§4 quinquies).

---

## 8. Reload d'intégration — c'est le Finding B

Le reload de l'intégration Zigbee **est** le vecteur du §6 : recomposition des contacts,
`systeme_stable` inchangé, garde anti-recomposition inopérante. Verdict : **indéterminable**
(effet), **démontré statiquement** (mécanisme de l'angle mort). Le reload d'une intégration
**sans capteur de sécurité** (Netatmo, Overkiz, Synology, HomeKit, Fujitsu, SwitchBot) n'a
aucun chemin vers le panneau d'alarme dans les sources lues.

---

## 9. Diagnostics et UI — sans effet physique

- **`10020000000021` (notification persistante)** : re-projette la notification d'état à
  `systeme_stable → on` (« HA ne restaure pas les persistantes »), crée/supprime selon
  `armed_away` / `disarmed`. **Aucun effet physique.** §2 : anomalie d'UI au pire.
- **`10020000000033` (timer_cancel)** : purge `timer.delai_entree` au désarmement (hygiène
  « UI / restore / reboot »). Aucun effet physique.
- **`10020000000030` (alerte incohérence)** : notifie si `alarme_etat_cible` diverge du réel
  > 5 min ; exclut `NOOP` / `unknown` / `unavailable`. Les helpers `alarme_etat_cible` /
  `alarme_decision` / `alarme_raison` **n'ont pas de `initial:`** (restaurés), mais l'application
  les réécrit à +45 s et `NOOP` est exclu du déclencheur ⇒ pas de fausse alerte durable. §2 :
  **anomalie de diagnostic** au pire, jamais action physique.
- **`10020000000034` (watchdog blocage)** : corrige l'incohérence `blocage / timer`
  (`blocage_orphelin` → `turn_off` ; `timer_orphelin` → `cancel`), sur anomalie **stabilisée
  500 ms**. N'agit **pas** sur le panneau. §2 : révocation d'un état de blocage incohérent —
  correcte.
- **Scripts sirène** (`bip`, `bip_bip`, `brutale`, `stop`, `test`), **`clavier`**,
  **armement/désarmement manuels**, **badge** : chemins **call-only** ou à intention
  utilisateur explicite. Un script ne s'auto-exécute jamais au boot. Aucun vecteur technique.

---

## 10. Synthèse par événement et qualification

| Conclusion | Événement | Qualification §8 | Grille §2 |
|---|---|---|---|
| Pas d'auto-armement au réveil (45 s < 5 min) | Reboot HA | Démontré statiquement | Abstention temporaire |
| Armement ultérieur si absence réelle ≥ 5 min | Reboot HA | Démontré statiquement | Recalcul fonctionnel |
| Pas de désarmement sur `unknown` ni blip < 15 s | Reboot HA | Démontré statiquement | Continuité / recalcul fonctionnel |
| Intrusion neutralisée pendant 45 s | Reboot HA | Démontré statiquement | Abstention temporaire |
| Reconstruction contexte visiteur | Reboot HA | Démontré statiquement | Restauration |
| Panneau `manual` restauré + décision NOOP | Reboot HA | Probable (HA-interne) | Continuité légitime |
| **Finding A** — sirène rejouée sur restauration `triggered` | Reboot HA | **Indéterminable** (effet) ; guard-gap démontré statiquement | Action physique indésirable — **candidate, non établie** |
| **Finding B** — intrusion sur contact recomposé `unavailable → on` | Reload intégration Zigbee | **Indéterminable** (effet) ; guard-gap démontré statiquement | Action physique indésirable — **candidate, non établie** |
| Panneau inchangé au reload | Reload YAML | Démontré par preuve runtime L4 | Continuité légitime |
| Contacts non rechargés par un reload YAML alarme | Reload YAML | Démontré statiquement | — |

**Deux angles morts, une même signature.** Findings A et B sont tous deux des **absences de
garde** contre un artefact de restauration/recomposition, tous deux **démontrés statiquement**
quant au mécanisme, tous deux **indéterminables** quant à l'effet réel, tous deux qualifiés
**lacune** et non **écart** après confrontation aux contrats 50 et 70. Ils ne réclament aucune
correction dans ce rapport : ils alimentent le **portefeuille** (livrable 3 de C34).

---

## 11. Limites probatoires de la vague

- **Aucune preuve runtime nouvelle** n'a été produite ; la seule mobilisée est la preuve L4
  d'origine (panneau inchangé au reload).
- Les deux findings reposent sur le **comportement interne de HA** (restauration d'un panneau
  `manual` à `triggered` ; émission d'événement de restauration ; republication Zigbee2MQTT d'un
  contact ouvert) — **non démontrable par les sources** et **non observable** sans provoquer
  reboot/reload, ce que le cadre interdit.
- **`sensor.clavier_alarme_*` et les contacts de sécurité ne sont pas dans l'allowlist Recorder**
  au titre relevé (à confirmer en portefeuille) : même une preuve L4 ne pourrait lever le Finding
  B, faute d'historique de la transition `unavailable → on` sur les contacts (conséquence directe
  du §8 du cadrage : hors allowlist ⇒ indéterminable, non contournable).
- Le signal brut `presence_famille_securite` relève de **D-PRES / C33** et n'est pas ré-audité
  ici : la vague ne juge que les **projections** consommées par l'alarme (15 s / 5 min).

---

## 12. Suite

Cette vague **n'ouvre aucun sous-chantier correctif** (stop point du cadrage §10). Findings A et
B sont versés au **portefeuille C34** (livrable 3) comme risques **candidats**, avec, pour chacun,
la preuve manquante qualifiée (observation d'un reboot / reload provoqué, ou instrumentation
Recorder des contacts et du panneau — chantier d'instrumentation distinct). Le contre-audit de la
vague 4 (attaquer ces deux findings, chercher les contre-exemples, vérifier la restauration du
panneau `manual`) reste à conduire avant toute orientation.
