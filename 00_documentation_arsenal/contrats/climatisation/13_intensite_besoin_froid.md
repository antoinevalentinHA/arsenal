# CONTRAT ARSENAL — CLIMATISATION
## 13 — Intensité du besoin de froid (couche perception)

**Version contrat :** v1.1
**Statut :** Normatif — couche perception observationnelle, antérieure à toute
résolution ventilation

> **v1.1 (C32 / A2 étendu COOL — déménagement) :** la garde anti-gel ne lit plus que **deux façades
> chambres** (Chambre Enfants + Chambre Parents). La **Salle de Jeux** en est
> **exclue** — cohérent avec la réduction 3→2 de `temperature_max_chambres` (C32/L2) : une pièce sans
> usage sommeil ne participe ni au besoin de chauffe **ni à la perception du besoin de froid**.
> Façades désormais `…_chambre_enfants` ; **alignement
> runtime** (retrait de la façade Salle de Jeux de la garde) reste porté par **C32/L4**. Chantier :
> [`chantier_restructuration_chambres_enfants.md`](../../audits/04_chantiers/transverses/chantier_restructuration_chambres_enfants.md).

---

## Objet

Ce contrat fixe la **couche de perception** qui quantifie **l'intensité du
besoin de froid** dans les chambres, en vue d'un futur pilotage intelligent de
la **vitesse de ventilation** de la climatisation.

Il définit **deux capteurs** :

1. un capteur **numérique** d'intensité brute (écart en °C) ;
2. un capteur **ordinal** d'intensité (`satisfait` / `faible` / `moyen` /
   `eleve` / `extreme`).

Ces capteurs sont de **pure perception** : ils n'émettent aucune commande, ne
pilotent aucun matériel, et n'écrivent aucun helper. Ils sont **observationnels**
et destinés à être **calés empiriquement** (historisation) avant tout câblage.

> Ce document est une **passe documentaire normative**. Il fixe la cible
> opposable **avant** toute implémentation runtime. Aucun runtime n'est créé ni
> modifié par ce lot (voir § Hors périmètre). La **résolution ventilation**
> (transformation de l'intensité en vitesse, clamps, garde-fous, gouvernance
> auto/override) est **hors périmètre** et relève d'un contrat ultérieur.

La ventilation est un **axe orthogonal** au mode thermique (cf.
[`12_ventilation_intention.md`](12_ventilation_intention.md)). Le présent contrat
ne décrit **que** la perception d'un besoin gradué ; il ne décide jamais
d'allumer, d'éteindre ou de changer le mode de la climatisation.

---

## Rôle des entités

| Entité | Rôle contractuel | Nature |
|---|---|---|
| `sensor.temperature_max_chambres` | **Opérande de déficit** : porte la température de la chambre la plus chaude. | Perception (agrégat) |
| `sensor.seuil_extinction_clim_applique` | **Référence opérationnelle** de satisfaction froid (voir §1). | Décision d'arrêt / référence |
| `sensor.temperature_chambre_enfants` · `_parents` | **Garde anti-gel** : fraîcheur des sources (disponibilité uniquement). Salle de Jeux **exclue** (C32/A2 COOL). | Perception (façades) |
| `sensor.clim_intensite_besoin_froid` | **Intensité brute** en °C, plancher 0. | Perception pure |
| `sensor.clim_intensite_besoin_froid_niveau` | **Niveau** de besoin (5 états). | Perception pure |

> **Noms d'entités — ratifiés.** Les deux capteurs existent désormais au runtime
> avec les `unique_id` `clim_intensite_besoin_froid` (numérique) et
> `clim_intensite_besoin_froid_niveau` (ordinal), sans le radical `consigne`
> (réservé, côté clim, à la consigne machine). Voir § État d'implémentation.

---

## 1. Référence opérationnelle retenue

La référence contre laquelle se mesure l'intensité est
**`sensor.seuil_extinction_clim_applique`** — le niveau à partir duquel Arsenal
considère que le refroidissement a **suffisamment produit d'effet** dans les
chambres atteignables.

Ce choix est **opérationnel** (et non théorique) : il réutilise le **plancher de
satisfaction** déjà défini par la régulation, plutôt que d'introduire un nouvel
objectif de confort.

### 1.1 Exclusion de la consigne machine

`sensor.consigne_clim_appliquee` est **exclu** du calcul du besoin. C'est une
**consigne machine / actionneur** envoyée au climatiseur Fujitsu/Airstage en
configuration mono-zone (mesure côté unité intérieure / palier), volontairement
basse. Elle appartient à la couche **actionneur**, **pas** à la couche besoin.

### 1.2 Distinction d'avec les seuils ON/OFF

- `sensor.seuil_allumage_clim_applique` reste le **seuil de déclenchement**
  (« faut-il refroidir ? », indexé sur `max`). Il **n'est pas** utilisé ici.
- `sensor.seuil_extinction_clim_applique` reste le **seuil d'arrêt** (indexé sur
  `min`), **mais il est aussi accepté comme référence opérationnelle** de
  satisfaction froid pour l'intensité.

Cette stratégie respecte la doctrine **max-ON / min-OFF** (cf.
[`audit_strategie_max_on_min_off_cool.md`](../../audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md))
sans la modifier : la couche perception **lit** ces références, elle ne les
**recalcule** ni ne les **refond**.

---

## 2. Couplage assumé au seuil OFF (C1)

Le seuil OFF porte désormais **deux rôles** :

1. décision d'arrêt COOL (comparée à `temperature_min_chambres`) ;
2. référence d'intensité (comparée à `temperature_max_chambres`).

> **C1 — Couplage assumé.** Toute modification future de
> `sensor.seuil_extinction_clim_applique` (ou de ses helpers
> `clim_seuil_extinction_presence` / `_absence`) **modifie aussi l'intensité de
> ventilation**. Ce couplage est **volontaire** et doit rester documenté. Il
> n'existe **pas** d'objectif de confort distinct à ce stade.

---

## 3. Contextualisation présence / nuit / absence assumée (C2)

`sensor.seuil_extinction_clim_applique` est **contextualisé** : il sélectionne
`clim_seuil_extinction_presence` ou `clim_seuil_extinction_absence` selon la
présence et le mode nuit (`binary_sensor.clim_mode_nuit_effectif`).

> **C2 — Contextualisation assumée.** La référence d'intensité **suit** ce
> contexte. La nuit (seuil OFF plus haut) ⇒ écart plus petit ⇒ **intensité
> mécaniquement plus basse**. Cette **baisse nocturne est voulue**, sous réserve
> que la future résolution ne cumule pas un clamp silencieux **excessif** (point
> à réconcilier hors de cette couche).

La contextualisation présence/nuit reste donc portée par le **seuil appliqué** —
jamais réintroduite ailleurs dans la couche perception (pas de double
contextualisation).

---

## 4. Capteur numérique d'intensité brute

### 4.1 Formule

```
intensité_brute = max(0, temperature_max_chambres − seuil_extinction_clim_applique)
```

L'état publié est **planché à 0**. L'écart signé réel reste exposé en attribut
de debug.

### 4.2 Plancher à 0 et sémantique des états

- **0** = **déficit nul** : la chambre la plus chaude est déjà au plancher de
  satisfaction (état **valide**, pas une abstention).
- **`unavailable`** = **calcul impossible** ou données non fiables.

La distinction **0 ≠ `unavailable`** est **normative** : un déficit nul est une
information ; une indisponibilité est une absence d'information.

### 4.3 Disponibilité (garde anti-gel)

Le capteur est **disponible si, et seulement si** :

1. `sensor.seuil_extinction_clim_applique` est **numérique** ; **ET**
2. **au moins une** façade chambre (`sensor.temperature_chambre_enfants` /
   `_parents` — Salle de Jeux exclue, C32/A2 COOL) est **numérique** ; **ET**
3. `sensor.temperature_max_chambres` est **numérique**.

Sinon → **abstention** (`unavailable`). Jamais de repli numérique, jamais de
`hold`.

> **Garde anti-gel — normative.** La disponibilité **ne doit jamais** être
> dérivée **seulement** de `sensor.temperature_max_chambres` : cet agrégat
> **gèle** sa dernière valeur **numérique** si toutes les façades tombent (voir
> §6). Une garde `is_number(max)` seule **passerait** sur une donnée gelée. La
> garde est donc fondée sur la **fraîcheur des façades** (condition 2), qui
> détecte exactement le gel. Cette couche est **volontairement plus stricte**
> que la chaîne de décision COOL existante.

### 4.4 Type

- `unit_of_measurement: "°C"` ;
- `state_class: measurement` ;
- **pas** de `device_class: temperature` (il s'agit d'un **écart** de
  température, pas d'une température absolue).

### 4.5 Attributs de debug

- `ecart_signe` — `max − seuil_off` non planché (peut être < 0) ;
- `max_chambres_utilise`, `seuil_off_utilise` ;
- `chambre_la_plus_chaude` — propagé de l'agrégat `max` ;
- `contexte_seuil` — `mode_actif` du seuil OFF (Présence / Absence / Absence
  (mode nuit)), rendant visible l'effet C2 ;
- `facades_numeriques` — nombre de façades fraîches (0–3) ;
- `cause` — `none` / `seuil_indisponible` / `gel_max_facades_indisponibles` /
  `max_transitoire` ;
- `min_chambres_observe` — lecture **passive** (debug et future résolution),
  **hors** calcul (pureté mono-axe).

---

## 5. Capteur ordinal d'intensité

### 5.1 États

`satisfait` · `faible` · `moyen` · `eleve` · `extreme` — plus `unavailable` /
`unknown` **hérités** de la disponibilité du capteur numérique.

- `satisfait` = **déficit nul** (état numérique 0) ;
- `faible` = besoin **léger** (premier palier strictement positif) ;
- `satisfait` est **distinct** de `faible`.

### 5.2 Lecture et pureté

L'ordinal ne lit **que** le capteur numérique (§4) — **mono-axe strict**. Il ne
lit ni `min`, ni l'écart inter-chambres, ni le CO₂, ni la présence : la
contextualisation est **déjà** incluse via le seuil OFF (C2) et ne doit pas être
réappliquée.

### 5.3 Stabilité de bande

Les **bandes** et leurs **marges d'hystérésis** ne sont **pas** calibrées par ce
contrat : elles seront déterminées **empiriquement**, après observation
historique réelle (§7).

> **Anti-pompage — normatif.** Un ordinal **décisionnel** exige une **stabilité
> de bande** (seuils montants ≠ descendants, ou maintien du niveau courant dans
> une bande morte), y compris autour de la frontière `satisfait` ↔ `faible`. Le
> capteur lit donc son propre état précédent. Les **valeurs** des marges sont
> hors périmètre de ce contrat.

### 5.4 Non-mapping vers les vitesses

Les quatre niveaux actifs (`faible` / `moyen` / `eleve` / `extreme`) **ne
constituent pas** un mapping direct obligatoire vers les quatre vitesses de
ventilation (`Silencieux` / `Faible` / `Moyen` / `Fort`). La **résolution** est
une couche **séparée**, hors périmètre (voir § Hors périmètre).

---

## 6. Dette des agrégats max/min (chantier séparé)

`sensor.temperature_max_chambres` et `sensor.temperature_min_chambres`
**conservent leur dernière valeur numérique sans TTL** si toutes les façades
chambres deviennent indisponibles. Cette **dette de gel** est **réelle** et
concerne tout le domaine (besoin COOL, aération, chauffage).

La couche perception du présent contrat **s'en protège** par la garde anti-gel
fondée sur les façades (§4.3) et **n'attend pas** sa correction pour exister.

**Prise en charge (C28 / C27).** Cette dette de gel a **deux volets**, désormais
gouvernés séparément : **(a)** la **réaction de la machine Climatisation** à une
observation non vivante — le besoin COOL/HEAT ne doit ni maintenir `on` ni réarmer en
aveugle — est **gouvernée par C28** (amendements aux couches seuils/franchissements/
besoins/admissibilité :
[`capteurs/besoins/10_besoins.md`](capteurs/besoins/10_besoins.md),
[`capteurs/seuils_et_franchissements/20_binary_sensors_franchissement.md`](capteurs/seuils_et_franchissements/20_binary_sensors_franchissement.md),
[`capteurs/admissibilite/00_admissibilite.md`](capteurs/admissibilite/00_admissibilite.md)) ;
**(b)** la **correction de l'agrégat** lui-même (abstention honnête à zéro façade, sans
gel) reste **gouvernée par C27** (contrat de production). La garde anti-gel locale du
présent contrat (§4.3) **demeure** valable comme protection propre à la couche
perception. La dette domaine-wide n'est donc **plus un simple constat** : elle est
**prise en charge** par C28 (machine) et C27 (agrégat).

---

## 7. Historisation

Les **deux** capteurs (numérique et ordinal) **doivent être historisés**
(`recorder.yaml`). Objectif : observer les valeurs réelles, **caler les bandes**
et vérifier l'**effet nuit / seuil OFF contextualisé** (C2) **avant** tout
câblage vers la ventilation réelle.

---

## 8. Hors périmètre du lot documentaire d'origine

> Cette section décrit le périmètre du **lot documentaire initial** (rédaction du
> contrat). Le **runtime a depuis été implémenté** dans un lot séparé — voir
> § 9 État d'implémentation. Les exclusions ci-dessous sont la **trace** de ce
> que ce lot documentaire ne faisait pas ; elles ne décrivent **pas** l'état
> actuel du système (les capteurs existent et `recorder.yaml` les historise).

Le lot documentaire d'origine était **strictement documentaire**. Étaient **hors
de son périmètre** :

- **aucun pilotage matériel** dans cette phase ;
- **aucune résolution ventilation** (mapping intensité → vitesse, garde-fou par
  `temperature_min_chambres`, clamp silencieux, gouvernance auto/override) ;
- **aucune création** des capteurs template (perception) à ce stade ;
- **aucune modification** de `recorder.yaml`, de
  `11_automations/climatisation/ventilation/application_mode.yaml`, de
  `script.clim_set_fan_mode` ;
- **aucun nouvel `input_number`** ;
- **aucune modification** des seuils ON/OFF (`clim_seuil_declenchement_*`,
  `clim_seuil_extinction_*`) ;
- **aucune modification** de la consigne machine (`clim_consigne_presence` /
  `_absence`, `sensor.consigne_clim_appliquee`).

---

## 9. État d'implémentation

> Sur le modèle du contrat 12 (§13). Le runtime de cette couche perception a été
> implémenté dans un lot séparé, postérieur à la présente passe documentaire.

- **Entités créées** (template sensors, sous
  `12_template_sensors/climatisation/ventilation/`) :
  - `sensor.clim_intensite_besoin_froid` — numérique, °C, `state_class:
    measurement`, **sans** `device_class` (écart, non température absolue) ;
  - `sensor.clim_intensite_besoin_froid_niveau` — ordinal
    (`satisfait` / `faible` / `moyen` / `eleve` / `extreme`).
- **Historisation** : les deux capteurs sont enregistrés dans `recorder.yaml`
  (section CLIMATISATION) pour l'observation et le calage empirique des bandes.
- **Caractère observationnel** : perception pure — aucune action, aucune
  écriture, aucun service.
- **Absence de pilotage** : ne commandent ni `climate.clim` ni aucun actionneur ;
  n'écrivent pas l'intention.
- **Modèle B intact** : le single-writer de l'intention reste préservé ; aucun
  chemin de pilotage n'est introduit.

---

## Renvois

- Ventilation (`fan_mode`) — intention persistante :
  [`12_ventilation_intention.md`](12_ventilation_intention.md)
- Recommandation de ventilation (consommateur diagnostique aval) :
  [`14_recommandation_ventilation.md`](14_recommandation_ventilation.md)
- Décision canonique du mode thermique :
  [`03_decision_canonique.md`](03_decision_canonique.md)
- Entrées métier (températures, seuils) :
  [`04_entrees_metier.md`](04_entrees_metier.md)
- Stratégie COOL max-ON / min-OFF (topologie mono-zone, non normatif) :
  [`audit_strategie_max_on_min_off_cool.md`](../../audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)
- Efficacité clim par chambre (couplage / découplage, non normatif) :
  [`chantier_efficacite_clim_par_chambre.md`](../../audits/04_chantiers/climatisation/chantier_efficacite_clim_par_chambre.md)
- Index du domaine : [`README.md`](README.md)
