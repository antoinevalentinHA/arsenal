# ⚡ ARSENAL — AUDIT — `automation.panne_detection_coupure_secteur` non déclenchée

> **Trace d'audit documentaire.** Aucune correction runtime dans cette passe : ni automation, ni template, ni Lovelace, ni script modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse · **[RECO]** recommandation.

---

## Verdict

L'automation a fonctionné **exactement comme codée**. Le non-déclenchement provient de son **témoin unique**, structurellement incapable de voir une coupure que l'onduleur compense. **Gravité : P0** (détection structurellement aveugle). Correction reportée à la passe suivante (cf. § Passe suivante).

- **Cause la plus plausible :** le seul signal d'entrée mesure un point **secouru par l'UPS**, resté sous tension pendant la coupure réelle.
- **Confiance :** élevée sur la chaîne logique (témoin → trigger) ; moyenne sur le détail physique exact (mesure de la sortie UPS *vs* passage en `unavailable`) — les deux mènent au même résultat.

---

## Événement réel

Coupure secteur réelle constatée (date non consignée dans cette trace). Infrastructure critique maintenue (Bluetti + UPS) : HA, box Internet, réseau, boiler bridge, chaudière, capteurs Zigbee. `automation.panne_detection_coupure_secteur` **ne s'est pas déclenchée** ; le mode panne n'a pas été armé.

---

## Automatisation auditée

| Élément | Valeur |
|---|---|
| Fichier | `11_automations/panne/secteur/activation_mode_panne.yaml` (L79–141) |
| `id` | `1004000000001` |
| `alias` → entité | `Panne - Détection coupure secteur` → `automation.panne_detection_coupure_secteur` |
| `mode` | `single` |
| Trigger `power_cut` | `binary_sensor.coupure_secteur` `off → on`, `for: 00:00:30` (L94–99) |
| Trigger `ha_start` | `input_boolean.systeme_stable` → `on` (L101–104) |
| Conditions | coupure `on` · `panne_secteur_active off` · `trigger.id ∈ {power_cut, ha_start}` (L109–123) |

---

## Chaîne de détection actuelle

`automation.panne_detection_coupure_secteur`
 → `binary_sensor.coupure_secteur`
  → `12_template_sensors/system/coupure_secteur.yaml` (L29–30) :
   `{{ states('sensor.prise_onduleur_voltage') | float(230) == 0 }}`
   → `sensor.prise_onduleur_voltage` = prise Zigbee `prise_onduleur`
   (`zigbee2mqtt/configuration.yaml:79-80`), documentée « Prise onduleur (NAS / réseau) »
   (`utility_meter.yaml:175`).

**[FAIT]** `infrastructure_puissance.md:6-9` place NAS / Serveur HA / Box sous protection **Onduleur (UPS)**. Le point mesuré appartient donc au cœur **secouru**.

---

## Cause du non-déclenchement

1. **[FAIT]** Le témoin mesure un circuit secouru. Pendant la coupure, ce point reste alimenté (UPS) → tension ≠ 0 V → `binary_sensor.coupure_secteur` reste `off` → trigger `power_cut` jamais armé.
2. **[FAIT]** Aggravant — défaut `float(230)` sans `availability:` : un témoin `unknown`/`unavailable` est lu **230 V**, soit « pas de coupure ». L'échec se fait du **mauvais côté**.
3. **[FAIT, écarté]** `ha_start` ne pouvait pas suppléer : HA n'a pas redémarré (secouru), et sa condition exige de toute façon `coupure_secteur == on`.
4. **[FAIT, écarté]** `for: 00:00:30` n'est pas en cause : valeur **normative** (`11_temporalite.md:30`), coupure réelle plus longue.

---

## Violation d'invariant normatif

Le contrat socle est explicite — `00_documentation_arsenal/contrats/pannes/secteur/10_socle.md` :

- **L88–90** : « Tout dispositif participant à la qualification d'une panne secteur doit demeurer **observable pendant l'événement qu'il qualifie**. […] ne peut pas constituer à lui seul une source de vérité suffisante. »
- **L135** : « **Une source dépendante du secteur ne peut pas constituer une source primaire valide.** »

**[FAIT]** L'implémentation actuelle viole cet invariant : la source primaire (`prise_onduleur_voltage`) est précisément un point dont l'observabilité « normale » dépend du secteur, mais qui — étant secouru — ne reflète pas l'événement. Le signal canonique ne peut donc pas qualifier la coupure.

---

## Témoins plus pertinents déjà présents (non câblés)

Deux signaux restent **observables pendant** une coupure et **chutent** à la perte du secteur, mais **n'alimentent pas** `binary_sensor.coupure_secteur` :

| Signal | Définition | Comportement en coupure | Statut actuel |
|---|---|---|---|
| `binary_sensor.critere_ups_sur_batterie` | `12_template_sensors/system/ups.yaml:43-51` — `'OB' in sensor.ups_code_d_etat` ; `unknown/unavailable → false` | passe `on` (UPS sur batterie) | non relié au signal canonique |
| `binary_sensor.bluetti_secteur_present` | `12_template_sensors/bluetti/secteur_present.yaml:17-20` — `sensor.bluetti_ac_input_voltage > 200`, avec `availability:` | passe `off` (secteur absent en entrée Bluetti) | invariant **délibéré** : « ne qualifie jamais `binary_sensor.coupure_secteur` » (`secteur_present.yaml:11`) |

**[FAIT]** La source Bluetti est volontairement confinée au domaine `energie_chaudiere`. Toute remédiation P0 devra trancher ce cloisonnement (révision d'invariant) plutôt que le contourner.

---

## Hypothèses (à départager en runtime)

- **[HYP, confiance élevée]** `prise_onduleur` mesure une tension **en aval de l'UPS** → ~230 V maintenus pendant la coupure → coupure invisible.
- **[HYP, alternative]** `prise_onduleur` est **en amont** → la prise Zigbee perd son alimentation → `unavailable` → `float(230)` ramène 230 V → même résultat.
- **Donnée runtime manquante :** historique de `sensor.prise_onduleur_voltage` pendant l'épisode (~230 V constant *ou* `unavailable`). C'est le seul point qui distingue les deux hypothèses ; il ne change pas le verdict P0.

---

## Recommandations

- **[RECO P0]** Requalifier `binary_sensor.coupure_secteur` sur une source **observable pendant l'événement et qui chute à la perte du secteur** — au moins `binary_sensor.critere_ups_sur_batterie`, éventuellement consolidée (OR) avec `binary_sensor.bluetti_secteur_present`. Consolidation dans la **couche de détection**, conformément à `10_socle.md:123-133` (l'unicité du signal canonique est préservée pour les consommateurs).
- **[RECO P1]** Supprimer le défaut dangereux `float(230)` : défaut neutre + `availability:`, sur le motif déjà employé par `bluetti/secteur_present.yaml:19-20`.
- **[RECO P3]** Corriger l'en-tête trompeur de `12_template_sensors/system/coupure_secteur.yaml:5` (« prise de la cave à vin » ≠ source réelle `prise_onduleur_voltage`).

---

## Passe suivante — correction P0 du témoin canonique

Cette trace **prépare** la passe correctrice, qui sera **runtime** et donc hors du présent périmètre documentaire. Périmètre prévu de la passe P0 :

- **Cible runtime :** `12_template_sensors/system/coupure_secteur.yaml` (requalification de la source) — et, si la voie Bluetti est retenue, **révision d'invariant** de `12_template_sensors/bluetti/secteur_present.yaml:11` et `sur_batterie.yaml:11`.
- **Contrat impacté :** `10_socle.md` (mécanisme de fallback / sélection de source, L108–135) — mise en cohérence du signal canonique avec son invariant d'observabilité.
- **Risques à arbitrer dans la passe P0 :**
  - *faux positif* — `OB`/micro-coupure : mitigé par le `for: 00:00:30` existant ;
  - *régression* — changement de sémantique du signal canonique : valider contre les consommateurs (chauffage, ECS) et le contrat avant bascule.
- **Pré-requis de vérification :** capturer en runtime l'état des trois témoins (`prise_onduleur_voltage`, `critere_ups_sur_batterie`, `bluetti_secteur_present`) lors d'une coupure contrôlée, pour confirmer la source de remplacement.

---

## Références

- Automation auditée (runtime) : `11_automations/panne/secteur/activation_mode_panne.yaml`
- Témoin canonique (runtime) : `12_template_sensors/system/coupure_secteur.yaml`
- Contrat socle (invariant violé) : [`contrats/pannes/secteur/10_socle.md`](../../../contrats/pannes/secteur/10_socle.md) · [temporalité](../../../contrats/pannes/secteur/11_temporalite.md)
- Hub domaine : [`navigation/domaines/pannes.md`](../../../navigation/domaines/pannes.md)
- Index des audits : [`audits/index.md`](../../index.md)
