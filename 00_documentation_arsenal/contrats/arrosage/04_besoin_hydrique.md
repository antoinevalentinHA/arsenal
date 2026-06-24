# CONTRAT ARSENAL — ARROSAGE
## 04 — Besoin hydrique (perception)

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir le **besoin hydrique** par zone/station comme couche de
**perception pure**, ses entrées conceptuelles et ses garde-fous, **sans figer
d'`entity_id`**.

---

## 1. Définition

Le **besoin hydrique** d'une zone répond à une seule question :

> *Cette zone du jardin mérite-t-elle de l'eau, indépendamment de toute
> autorisation, fenêtre ou régime ?*

C'est une **perception**, au sens de la doctrine Arsenal : un **fait estimé**,
pur et déterministe, **présence-agnostique** et **régime-agnostique**. Il ne
décide rien, ne pilote rien (cf. couche « Besoin » de
[`climatisation/README.md`](../climatisation/README.md) ; la transformation en
action relève de l'intention, [`05_intention.md`](05_intention.md)).

> **Granularité.** Le besoin est **par zone / station Rain Bird**, jamais global.
> Une zone ombragée et une zone plein soleil n'ont pas le même besoin.

---

## 2. Entrées conceptuelles

Toutes les entrées ci-dessous sont **conceptuelles** (`‹…›`) : aucun capteur réel
n'est encore appairé, aucun `entity_id` n'est figé.

| Entrée conceptuelle | Sens | Source pressentie |
|---|---|---|
| `‹humidite_sol_zone›` | Humidité réelle du sol de la zone | Capteur d'humidité sol **Zigbee** (commandé, non appairé) |
| `‹dernier_arrosage_zone›` | Temps écoulé depuis le dernier arrosage **connu** | Observation Arsenal + Rain Bird (cf. [`06_observation_et_preuves.md`](06_observation_et_preuves.md)) |
| `‹pluie_recente›` | Pluie tombée récemment | Signaux pluie ([`volets_pluie.md`](../volets_pluie.md), [`meteo/README.md`](../meteo/README.md)) |
| `‹pluie_prevue›` | Pluie prévue à court terme | Prévision météo |
| `‹chaleur_prevue›` | Chaleur / évapotranspiration prévue | Prévision météo |
| `‹saison_periode›` | Saison / période de l'année | Calendrier / météo |
| `‹restriction_eau›` | Restriction d'arrosage éventuelle (réglementaire/opérateur) | Réglage opérateur |

> **`‹dernier_arrosage_zone›` est délicat.** Il dépend de l'observation, qui peut
> être **présumée** (ACK BLE) plutôt que **confirmée** (eau qui coule). Le besoin
> doit donc consommer un *dernier arrosage **connu***, en distinguant confirmé /
> présumé / inconnu — voir [`06_observation_et_preuves.md`](06_observation_et_preuves.md).

---

## 3. Combinaison (conceptuelle, non figée)

Le besoin combine les entrées dans un sens **qualitatif** (les seuils, poids et
formules sont **non figés**, à calibrer en Phase 0) :

- l'**humidité sol basse** **augmente** le besoin ;
- un **arrosage récent** ou une **pluie récente** **diminue** le besoin ;
- une **pluie prévue** proche **diminue** le besoin (éviter le sur-arrosage,
  F2 de [`01_metier.md`](01_metier.md)) ;
- une **chaleur prévue** forte **augmente** le besoin ;
- la **saison** module l'amplitude globale ;
- une **restriction** active **plafonne ou annule** le besoin exécutable.

> **Forme conceptuelle.** Le besoin pourra s'exprimer comme un **niveau ordinal**
> par zone (p. ex. `‹besoin_zone›` ∈ {satisfait, faible, moyen, élevé}) doublé
> éventuellement d'un **support numérique**, sur le modèle de l'intensité de
> besoin en climatisation
> ([`climatisation/README.md`](../climatisation/README.md)). **Aucune échelle,
> aucun seuil n'est arrêté ici.**

---

## 4. Disponibilité & dégradation

| Situation | Comportement attendu (perception) |
|---|---|
| `‹humidite_sol_zone›` indisponible | Le besoin **ne se fabrique pas** une valeur faussement rassurante : il s'abstient ou se replie sur un défaut **prudent** (ne pas conclure « sol humide » par défaut). |
| Signaux pluie/météo indisponibles | Besoin calculé **sans** le garde-fou concerné, **transparence** de la cause. |
| Toutes entrées indisponibles | Besoin **inconnu** — l'intention en tiendra compte comme **inconnue critique** ([`05_intention.md`](05_intention.md)). |

> **Garde anti-faux-négatif.** Un capteur sol muet **ne doit jamais** être lu
> comme « sol humide donc pas besoin d'eau ». La direction de défaillance
> ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) §5) impose que le
> doute n'aboutisse pas à priver le jardin d'eau.

---

## 5. Invariants du besoin

1. Le besoin est **perception pure** : aucun pilotage, aucune écriture, aucune
   prise en compte du régime ni des fenêtres.
2. Le besoin est **par zone / station**.
3. Le besoin consomme un **dernier arrosage connu** qualifié (confirmé /
   présumé / inconnu), pas une présomption traitée comme un fait.
4. Une **entrée indisponible** ne produit jamais un besoin faussement bas.
5. **Aucun `entity_id`, seuil, poids ou formule n'est figé** : tout est
   conceptuel jusqu'à la Phase 0.
6. Le **mapping capteur sol ↔ zone Rain Bird** est une **inconnue à établir** en
   Phase 0 ([`07_phase_0_terrain.md`](07_phase_0_terrain.md)) — le besoin par
   zone n'est exploitable qu'une fois ce mapping confirmé.

---

## Renvois

- Intention (consomme le besoin) : [`05_intention.md`](05_intention.md)
- Observation du dernier arrosage : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Signaux pluie / météo : [`volets_pluie.md`](../volets_pluie.md), [`meteo/README.md`](../meteo/README.md)
- Modèle besoin/perception : [`climatisation/README.md`](../climatisation/README.md)
- Index du domaine : [`README.md`](README.md)
