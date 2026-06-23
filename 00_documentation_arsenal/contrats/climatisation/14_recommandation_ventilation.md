# CONTRAT ARSENAL — CLIMATISATION
## 14 — Recommandation de ventilation (diagnostic)

**Version contrat :** v1.0
**Statut :** Normatif — recommandation **diagnostique observationnelle**, sans
pilotage matériel, antérieure à toute résolution automatique

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

> Ce document est une **passe documentaire normative**. Il fixe la cible
> opposable **avant** toute implémentation runtime. La **résolution automatique**
> (transformation de la recommandation en commande matérielle) est **hors
> périmètre** et relèvera d'une décision de gouvernance ultérieure.

---

## Rôle des entités

| Entité | Rôle contractuel | Nature |
|---|---|---|
| `sensor.clim_fan_mode_recommande` *(à créer)* | **Recommandation** de vitesse (FR), observationnelle. | Diagnostic / perception |
| `sensor.clim_intensite_besoin_froid_niveau` | **Moteur** : niveau ordinal de besoin. | Perception (contrat 13) |
| `binary_sensor.clim_seuil_extinction_cool_atteint` | **Frein min** : pièces atteignables satisfaites. | Franchissement |
| `binary_sensor.clim_silencieux_autorise` | **Plafond** silencieux. | Décision métier |
| `sensor.clim_intensite_besoin_froid` | Contexte (debug). | Perception (contrat 13) |
| `input_select.clim_fan_mode_cible` | **Intention** utilisateur — diagnostic d'écart **uniquement**. | Intention (Modèle B) |
| `sensor.clim_mode_de_ventilation_local` | **Réel** Fujitsu — diagnostic d'écart **uniquement**. | Perception |

> **Nom d'entité à ratifier.** L'`unique_id` de la recommandation n'est pas figé
> par ce contrat (candidat : `clim_fan_mode_recommande`). Ratification à la
> création runtime.

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

**Pour le contexte (debug uniquement)** :
- `sensor.clim_intensite_besoin_froid`.

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

## 5. Mapping initial besoin → recommandation brute

| Niveau de besoin | Recommandation brute |
|---|---|
| `satisfait` | `Silencieux` |
| `faible` | `Silencieux` |
| `moyen` | `Faible` |
| `eleve` | `Moyen` |
| `extreme` | `Fort` |

> **Mapping INITIAL, observationnel, à caler empiriquement.** Ce n'est **pas** un
> calibrage définitif. Le repli `satisfait`+`faible` → `Silencieux` évite une
> bijection tautologique 1:1 et donne de la marge ; il sera revu après
> observation historique (recorder). `Auto` (Fujitsu) est **exclu** des cibles de
> recommandation.

Index ordinal de vitesse (pour les opérations de plafond) :
`Silencieux = 0`, `Faible = 1`, `Moyen = 2`, `Fort = 3`.

---

## 6. Frein min (anti-acharnement ventilatoire)

```
recommandation_apres_frein =
    SI binary_sensor.clim_seuil_extinction_cool_atteint == on  → Silencieux
    SINON                                                       → recommandation_brute
```

**Justification.** `binary_sensor.clim_seuil_extinction_cool_atteint` exprime
`temperature_min_chambres ≤ seuil_extinction_clim_applique` : les pièces
**atteignables / contrôlables** sont déjà au seuil d'arrêt. Pousser davantage
surrefroidirait une pièce contrôlée pour une chambre potentiellement
**découplée** (topologie mono-zone, clim au palier, portes fermables). Le frein
**plafonne à `Silencieux`**.

> Ce frein appartient à la **recommandation**, jamais au besoin : `min` n'entre
> **pas** dans `sensor.clim_intensite_besoin_froid` (qui reste mono-axe). Il est
> lu ici via le binaire de franchissement **existant**, sans recalcul.

---

## 7. Plafond silencieux (sans double-comptage)

```
recommandation_finale =
    SI binary_sensor.clim_silencieux_autorise == on  → min(recommandation_apres_frein, Moyen)
    SINON                                             → recommandation_apres_frein
```

**Plafond, pas décrément.** Le silencieux **borne le haut** (jamais `Fort`,
jamais `Auto`), il **ne soustrait pas**. L'effet **nuit** est déjà inclus en
amont, dans l'intensité (via `clim_mode_nuit_effectif` →
`seuil_extinction_clim_applique` en valeurs absence → besoin plus bas). Comme le
silencieux est un opérateur `min` sur l'index de vitesse :

- si l'intensité nocturne recommande déjà ≤ `Moyen`, le plafond est un **no-op**
  (aucune double pénalité) ;
- il ne mord que pour couper un `Fort` résiduel — comportement **voulu**.

Le plafond s'applique **en dernier** (sommet de la pile de résolution),
cohérent avec « silencieux > intention » du Modèle B.

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
| `niveau_besoin_lu` | état de `clim_intensite_besoin_froid_niveau` |
| `intensite_num` | état de `clim_intensite_besoin_froid` (contexte) |
| `reco_brute` | après mapping, avant garde-fous |
| `reco_apres_frein_min` | après frein min (§6) |
| `reco_finale` | = `state` (après plafond silencieux, §7) |
| `mode_technique` | recommandation finale en technique (`quiet`/`low`/`medium`/`high`) |
| `cause_plafonnement` | `none` / `frein_min_actif` / `plafond_silencieux` / `frein_min_indisponible` / `silencieux_indisponible` |
| `intention_actuelle` | `input_select.clim_fan_mode_cible` (diagnostic) |
| `ventilation_reelle` | `sensor.clim_mode_de_ventilation_local` (diagnostic) |
| `ecart_reco_intention` | comparaison `reco_finale` (FR) ↔ intention (FR) |
| `ecart_reco_reel` | comparaison `mode_technique` ↔ réel (technique) |

La cascade `reco_brute → reco_apres_frein_min → reco_finale` DOIT rester
observable, afin que **chaque étage de plafonnement** soit explicable.

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

- **aucun pilotage matériel** ; **aucune résolution automatique** ;
- **aucune** modification de
  `11_automations/climatisation/ventilation/application_mode.yaml` ;
- **aucune** modification de `script.clim_set_fan_mode` ;
- **aucune** écriture de `input_select.clim_fan_mode_cible` ;
- **aucune** automatisation, **aucun** `input_number` ;
- **aucun** changement des seuils ON/OFF (`clim_seuil_declenchement_*`,
  `clim_seuil_extinction_*`) ;
- **aucune** modification de la consigne machine
  (`clim_consigne_presence`/`_absence`, `sensor.consigne_clim_appliquee`).

---

## 12. Runtime futur minimal

| Fichier | Action future |
|---|---|
| `12_template_sensors/climatisation/ventilation/fan_mode_recommande.yaml` | créer le capteur diagnostic |
| `recorder.yaml` | historiser `sensor.clim_fan_mode_recommande` |

La résolution automatique (câblage de la recommandation au matériel via
l'autorité `10030000000120`) reste **hors périmètre**, subordonnée à une décision
de gouvernance auto/override ultérieure.

---

## Renvois

- Intention persistante (Modèle B) :
  [`12_ventilation_intention.md`](12_ventilation_intention.md)
- Intensité du besoin de froid (moteur amont) :
  [`13_intensite_besoin_froid.md`](13_intensite_besoin_froid.md)
- Stratégie COOL max-ON / min-OFF (frein min, topologie mono-zone) :
  [`audit_strategie_max_on_min_off_cool.md`](../../audits/04_chantiers/climatisation/audit_strategie_max_on_min_off_cool.md)
- Index du domaine : [`README.md`](README.md)
