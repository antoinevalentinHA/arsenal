# CONTRAT ARSENAL — CLIMATISATION
## 14 — Recommandation de ventilation (diagnostic)

**Version contrat :** v2.0
**Statut :** Normatif — aligné runtime (Lots 1/3/2 mergés). La recommandation
est désormais **câblée** à la résolution (`10030000000120`, contrat 12) ; elle
reste une **perception thermique pure** (ne pilote rien elle-même).

> **v2.0 — réalignement runtime.** Référentiel unique `x` (§3/§5), grille à
> hystérésis (§5), frein = **cap Faible** (§6), `Silencieux` réservé au domaine
> silence (§7). La résolution automatique (et l'arbitrage **absence → Fort**)
> vit dans `application_mode.yaml` (contrat 12), pas dans cette recommandation.

---

## Objet

Ce contrat définit `sensor.clim_fan_mode_recommande` : une **recommandation
diagnostique** de vitesse de ventilation, dérivée de l'intensité du besoin de
froid (contrat [`13_intensite_besoin_froid.md`](13_intensite_besoin_froid.md)),
bornée par un garde-fou de contrôlabilité et plafonnée par le silencieux.

> Ce capteur **n'écrit rien, ne pilote rien**. Il sert à **observer l'écart**
> entre le besoin thermique et l'intention persistante de l'utilisateur, sans
> modifier le Modèle B de ventilation (contrat
> [`12_ventilation_intention.md`](12_ventilation_intention.md)).

> **v2.0 — la résolution est désormais câblée.** La recommandation est
> consommée par l'autorité de résolution (`10030000000120`,
> `application_mode.yaml`) qui la transforme en commande matérielle **en mode
> « Auto Arsenal » uniquement** (contrat 12). Ce contrat reste néanmoins une
> **perception thermique pure** : il décrit *ce qui serait recommandé*, jamais
> *ce qui est commandé* — la décision de pilotage appartient à la résolution.

---

## Rôle des entités

| Entité | Rôle contractuel | Nature |
|---|---|---|
| `sensor.clim_fan_mode_recommande` | **Recommandation** de vitesse (FR), observationnelle. | Diagnostic / perception |
| `sensor.clim_intensite_besoin_froid_niveau` | **Moteur** : niveau ordinal de besoin. | Perception (contrat 13) |
| `binary_sensor.clim_seuil_extinction_cool_atteint` | **Frein min** : pièces atteignables satisfaites. | Franchissement |
| `binary_sensor.clim_silencieux_autorise` | **Plafond** silencieux. | Décision métier |
| `sensor.clim_intensite_besoin_froid` | Source numérique amont (x) — contexte observable. | Perception (contrat 13) |
| `input_select.clim_fan_mode_cible` | **Intention** utilisateur — diagnostic d'écart **uniquement**. | Intention (Modèle B) |
| `sensor.clim_mode_de_ventilation_local` | **Réel** Fujitsu — diagnostic d'écart **uniquement**. | Perception |

> **Nom d'entité — ratifié.** La recommandation existe désormais au runtime avec
> l'`unique_id` `clim_fan_mode_recommande`. L'**entity_id canonique** est forcé
> explicitement par `default_entity_id: sensor.clim_fan_mode_recommande` (idiome
> Arsenal), afin que l'entité réelle corresponde au nom contractuel et ne dépende
> pas de la slugification du `name`. Voir § État d'implémentation.

---

## 1. Trois objets strictement distincts

| Objet | Entité | Signification |
|---|---|---|
| **Recommandation** | `sensor.clim_fan_mode_recommande` | Ce que le besoin thermique **suggérerait** |
| **Intention** | `input_select.clim_fan_mode_cible` | Ce que l'utilisateur **veut** (persistant, Modèle B) |
| **Réel** | `sensor.clim_mode_de_ventilation_local` | Ce que la clim **fait** (`fan_mode` Fujitsu) |

Ces trois objets **NE DOIVENT JAMAIS être confondus**. La recommandation **ne
remplace pas** l'intention et **ne décrit pas** le réel : elle est une **opinion
métier observable**, indépendante.

---

## 2. Non-pilotage — interdits cardinaux

- **INTERDIT** — La recommandation NE DOIT JAMAIS écrire
  `input_select.clim_fan_mode_cible` (single-writer utilisateur préservé, §1 du
  contrat 12).
- **INTERDIT** — La recommandation NE DOIT JAMAIS commander `climate.clim`
  (`climate.set_fan_mode`) ni `switch.clim_quiet_fan`.
- **INTERDIT** — La recommandation NE DOIT déclencher aucune automatisation,
  aucun script, aucun actionneur.
- **INVARIANT** — Le Modèle B reste **intact** : le chemin unique
  intention → résolution → matériel (automation `10030000000120` →
  `script.clim_set_fan_mode`) n'est **ni modifié, ni doublé** par ce capteur.

La recommandation est une **lecture pure**. Sa seule sortie est son propre état
et ses attributs.

---

## 3. Entrées

**Pour le calcul (`state`)** — mono-axe besoin, plus garde-fous :
- `sensor.clim_intensite_besoin_froid_niveau` (moteur) ;
- `binary_sensor.clim_seuil_extinction_cool_atteint` (frein min) ;
- `binary_sensor.clim_silencieux_autorise` (plafond).

**Pour le contexte observable (hors calcul du `state`)** :
- `sensor.clim_intensite_besoin_froid` — source numérique amont (x) dont
  `sensor.clim_intensite_besoin_froid_niveau` est la projection ordinale
  effectivement consommée par la recommandation.

**Pour le diagnostic d'écart (attributs uniquement, JAMAIS dans le calcul)** :
- `input_select.clim_fan_mode_cible` ;
- `sensor.clim_mode_de_ventilation_local`.

> Les deux dernières entités **NE DOIVENT PAS** influencer `state`. Les utiliser
> dans le calcul transformerait un diagnostic en boucle de contrôle.

---

## 4. Disponibilité

| Situation | Comportement | Cause |
|---|---|---|
| Niveau de besoin `unknown`/`unavailable` | → **`unavailable`** (abstention) | Le moteur manque : aucune recommandation possible. |
| Frein min `unknown`/`unavailable` | calcul **sans frein**, recommandation publiée | `cause_plafonnement = frein_min_indisponible` |
| Silencieux `unknown`/`unavailable` | calcul **sans plafond**, recommandation publiée | `cause_plafonnement = silencieux_indisponible` |

La recommandation **NE DOIT JAMAIS** retomber sur une vitesse par défaut quand le
besoin est indisponible : elle s'**abstient** (`unavailable`). Pour les
garde-fous indéterminés, elle **dégrade en restant transparente** (calcul sans le
garde-fou concerné, cause flaggée) — un diagnostic doit rester informatif.

---

## 5. Grille de vitesse — référentiel unique `x` (v2.0)

La recommandation est pilotée par un **référentiel UNIQUE** :

```
x = sensor.clim_intensite_besoin_froid
  = max(0, temperature_max_chambres − seuil_extinction_clim_applique)
```

> Le **double référentiel ON/OFF est abandonné** : plus aucun plancher fondé sur
> `seuil_allumage_clim_applique`. Tout dépend de `x` (écart de la chambre la plus
> chaude au seuil d'arrêt). `x` est la grandeur la plus stable et lisible.

Index ordinal de vitesse : `Silencieux = 0`, `Faible = 1`, `Moyen = 2`, `Fort = 3`.

**Grille à deux latches d'hystérésis** (présence-agnostique, plancher `Faible`) :

| Seuil | Montée | Descente | Dead-band |
|---|---|---|---|
| **Moyen** (idx ≥ 2) | `x ≥ 1.0` | `x < 0.6` | 0.4 °C |
| **Fort** (idx ≥ 3) | `x ≥ 2.0` | `x < 1.5` | 0.5 °C |

- `idx = 3` si latch Fort · `2` si latch Moyen · sinon **`1` (Faible)**.
- **`Silencieux` (0) n'est JAMAIS émis** par la recommandation : le `quiet` est
  propriété **exclusive** du domaine silence (§7). Le plancher hors silence est
  **Faible**.
- Seuils `1.0 / 0.6 / 2.0 / 1.5` **codés en dur**, latches persistés en attributs
  (`latch_moyen` / `latch_fort`), hold de l'état précédent si `x` manquant.
- `Auto` (Fujitsu) est **exclu** des cibles ; `mode_technique` ∈ `low/medium/high`.

> **Valeurs à observer (recorder)** — calibrage initial, non définitif.

---

## 6. Frein chambre froide (anti-acharnement ventilatoire) — cap `Faible`

```
recommandation_apres_frein =
    SI binary_sensor.clim_seuil_extinction_cool_atteint == on  → cap Faible (idx = 1)
    SINON                                                       → grille (§5)
```

**Justification.** `binary_sensor.clim_seuil_extinction_cool_atteint` exprime
`temperature_min_chambres ≤ seuil_extinction_clim_applique` : les pièces
**atteignables / contrôlables** sont déjà au seuil d'arrêt. Pousser davantage
surrefroidirait une pièce contrôlée pour une chambre potentiellement
**découplée** (topologie mono-zone, clim au palier, portes fermables).

> **v2.0 — le frein plafonne à `Faible`, pas à `Silencieux`** : `Silencieux`
> étant réservé au domaine silence (§7), le plancher pratique hors silence est
> `Faible`. Le frein est **présence-agnostique** ; son **ignorance en ABSENCE**
> (→ `Fort`) est un arbitrage **effectif** porté par la résolution
> (`application_mode.yaml`, contrat 12), **hors** de cette recommandation.

> Ce frein appartient à la **recommandation**, jamais au besoin : `min` n'entre
> **pas** dans `sensor.clim_intensite_besoin_froid` (qui reste mono-axe). Il est
> lu ici via le binaire de franchissement **existant**, sans recalcul.

---

## 7. Plafond silencieux + `Silencieux` réservé au domaine silence

```
ordre des caps (sur la grille §5) :
    1. plafond silencieux : SI clim_silencieux_autorise == on ET idx > 2 → idx = 2 (Moyen)
    2. frein chambre froide (§6, prime) : SI extinction_cool_atteint == on → idx = 1 (Faible)
```

**Plafond, pas décrément.** Le silencieux **borne le haut** (jamais `Fort`), il
**ne soustrait pas**. Le frein (§6) **prime** sur le plafond (cap plus bas).

**`Silencieux` / `quiet` = propriété EXCLUSIVE du domaine silence.** La
recommandation **n'émet jamais `Silencieux`** : elle plafonne à `Moyen` en plage
silencieuse, mais le **vrai `quiet`** est appliqué exclusivement par l'automation
silence (`switch.clim_quiet_fan`, `1003000000020`), jamais par cette voie ni par
la résolution. Le **silence est prioritaire** : pendant la plage, la résolution
(`application_mode.yaml`) s'abstient (`not override_actif`).

---

## 8. Vocabulaire de sortie

- **`state` = libellé français** : `Silencieux` / `Faible` / `Moyen` / `Fort`.
  Directement comparable à `input_select.clim_fan_mode_cible` (FR).
- **attribut `mode_technique` = valeur technique Fujitsu** : `quiet` / `low` /
  `medium` / `high`. Directement comparable à
  `sensor.clim_mode_de_ventilation_local` (technique).

Cette double exposition est **normative** : sans elle, les écarts (§9) seraient
faussés par la différence de vocabulaire FR ↔ technique.

---

## 9. Attributs attendus

| Attribut | Contenu |
|---|---|
| `niveau_besoin_lu` | état de `clim_intensite_besoin_froid_niveau` (contexte) |
| `intensite_num` | état de `clim_intensite_besoin_froid` (= `x`) |
| `latch_moyen` / `latch_fort` | latches d'hystérésis persistés (§5) |
| `vitesse_grille` | vitesse issue de la grille `x`, **avant** caps |
| `cap_actif` | cap appliqué : `frein` / `silence` / `none` |
| `reco_finale` | = `state` (après caps, §6/§7) |
| `mode_technique` | recommandation finale en technique (`low`/`medium`/`high`) |
| `cause_plafonnement` | `none` / `frein_min_actif` / `plafond_silencieux` / `frein_min_indisponible` / `silencieux_indisponible` |
| `intention_actuelle` | `input_select.clim_fan_mode_cible` (diagnostic) |
| `ventilation_reelle` | `sensor.clim_mode_de_ventilation_local` (diagnostic) |
| `ecart_reco_intention` | comparaison `reco_finale` (FR) ↔ intention (FR) |
| `ecart_reco_reel` | comparaison `mode_technique` ↔ réel (technique) |

La cascade `vitesse_grille → cap_actif → reco_finale` DOIT rester observable,
afin que **chaque étage** (grille, plafond silence, frein) soit explicable.

---

## 10. Capteur d'écart — différé

Aucun capteur séparé `sensor.clim_fan_mode_ecart` n'est créé dans ce lot. Les
écarts (`ecart_reco_intention`, `ecart_reco_reel`) vivent **en attributs** de
`sensor.clim_fan_mode_recommande`.

> Promotion possible **plus tard** vers un capteur dédié si l'historisation
> d'attributs se révèle insuffisante pour l'analyse de tendance. Différé, non
> supprimé.

---

## 11. Hors périmètre (explicite)

Périmètre **de ce capteur** (la perception). La résolution est câblée (§12) mais
relève d'un **autre** contrat (12) et d'un **autre** fichier — ce capteur :

- **ne pilote aucun matériel** : n'écrit pas `input_select.clim_fan_mode_cible`,
  ne commande ni `climate.clim`, ni `switch.clim_quiet_fan`,
  ni `script.clim_set_fan_mode` ;
- **ne double pas** la résolution : le câblage recommandation → matériel est
  porté **exclusivement** par `application_mode.yaml` (`10030000000120`,
  contrat 12) ; ce capteur ne fait que **publier** la recommandation que la
  résolution *lit* ;
- **ne porte pas** l'arbitrage **absence → Fort** : il est **présence-agnostique**
  (§6) ; ce forçage vit dans la résolution (`application_mode.yaml`, contrat 12) ;
- **ne déclenche aucune** automatisation, **aucun** `input_number` ;
- **ne change pas** les seuils ON/OFF (`clim_seuil_declenchement_*`,
  `clim_seuil_extinction_*`) ;
- **ne modifie pas** la consigne machine
  (`clim_consigne_presence`/`_absence`, `sensor.consigne_clim_appliquee`).

---

## 12. Runtime minimal — réalisé

| Fichier | Action (réalisée) |
|---|---|
| `12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml` | capteur diagnostic **créé** (grille `x`, latches, caps) |
| `recorder.yaml` | `sensor.clim_fan_mode_recommande` **historisé** |
| `11_automations/climatisation/ventilation/application_mode.yaml` | résolution **câblée** : lit `mode_technique` en « Auto Arsenal » (contrat 12) |

La résolution automatique (câblage de la recommandation au matériel via
l'autorité `10030000000120`) est **désormais réalisée** et décrite par le
contrat 12. En « Auto Arsenal », elle suit `mode_technique` ; l'arbitrage
**absence → Fort** y est porté (pas ici). Ce capteur reste **perception pure**.

---

## 13. État d'implémentation

> Sur le modèle du contrat 12 (§13). Le runtime de cette couche de recommandation
> a été implémenté, puis **réaligné** par les lots de recalibrage « Auto Arsenal »
> (grille `x`, frein = cap Faible, `Silencieux` réservé au silence), désormais
> mergés.

- **Entité créée** : `sensor.clim_fan_mode_recommande`
  (`12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml`),
  `state` FR (`Faible` / `Moyen` / `Fort`) + attribut
  `mode_technique` (`low` / `medium` / `high`).
- **Grille `x` à hystérésis** : référentiel unique
  `x = sensor.clim_intensite_besoin_froid` ; latches `latch_moyen` (1.0/0.6) et
  `latch_fort` (2.0/1.5) persistés en attributs ; plancher `Faible` ;
  `Silencieux` **jamais** émis (§5/§7).
- **Caps câblés** : frein chambre froide → cap `Faible` (§6) ; plafond silencieux
  → cap `Moyen` (§7) ; frein prime. Cascade observable via
  `vitesse_grille → cap_actif → reco_finale` (§9).
- **Entity_id canonique** forcé via
  `default_entity_id: sensor.clim_fan_mode_recommande` (le `name` se serait sinon
  slugifié autrement).
- **Historisation** : enregistré dans `recorder.yaml` (section CLIMATISATION).
- **Résolution câblée** (contrat 12) : en « Auto Arsenal », l'autorité
  `10030000000120` (`application_mode.yaml`) **lit** `mode_technique` et le résout
  vers le matériel ; l'arbitrage **absence → Fort** y est porté, **hors** de ce
  capteur (présence-agnostique, §6/§11).
- **Absence de pilotage propre** : ce capteur n'écrit pas
  `input_select.clim_fan_mode_cible`, ne commande ni `climate.clim`, ni
  `script.clim_set_fan_mode`, ni `switch.clim_quiet_fan` ; `input_select` et
  `sensor.clim_mode_de_ventilation_local` ne servent qu'au diagnostic d'écart.
- **Modèle B intact** : single-writer de l'intention préservé ; chemin unique de
  résolution (`10030000000120`) non doublé — ce capteur **publie**, la résolution
  **lit**.

---

## Renvois

- Intention persistante (Modèle B) :
  [`12_ventilation_intention.md`](12_ventilation_intention.md)
- Intensité du besoin de froid (moteur amont) :
  [`13_intensite_besoin_froid.md`](13_intensite_besoin_froid.md)
- Stratégie COOL max-ON / min-OFF (frein min, topologie mono-zone) :
  [`audit_strategie_max_on_min_off_cool.md`](../../audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)
- Index du domaine : [`README.md`](README.md)
