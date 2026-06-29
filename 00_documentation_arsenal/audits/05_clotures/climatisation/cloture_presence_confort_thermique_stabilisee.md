# ✅ ARSENAL — CLÔTURE DE CHANTIER

## Climatisation / Présence — Validation terrain de la présence confort thermique stabilisée (V1 + V2)

| Champ | Valeur |
|---|---|
| **Type** | Clôture de chantier — validation terrain |
| **Domaine** | Climatisation / Présence — interface de stabilisation COOL/DRY |
| **Statut** | ✅ CLÔTURÉ sur le périmètre **COOL/DRY** — `T = 120 s` ratifié (réserve de surveillance) |
| **Version** | 1.0 |
| **Date** | 2026-06-19 |
| **Chantier** | C4 (registre) — [`suivi_post_deploiement_presence_confort_thermique_stabilisee.md`](../../04_chantiers/climatisation/suivi_post_deploiement_presence_confort_thermique_stabilisee.md) |
| **Critères** | §5 du suivi (C1, C2, C3, C4) |
| **Cadrage contrat** | [`cadrage_contrat_presence_confort_thermique_stabilisee.md`](../../02_conception/climatisation/cadrage_contrat_presence_confort_thermique_stabilisee.md) |

---

## 1. Objet

Clore le chantier C4 sur le **périmètre validé** : le signal
`binary_sensor.presence_confort_thermique_stabilisee` (`delay_off = 120 s`, pas
de `delay_on`), branché sur les portes de présence **COOL/DRY** (V1 + V2), absorbe
les faux-absents courts sans couper la climatisation, sans anticiper les vraies
absences.

Ce document **ne ratifie pas** une extension de la stabilisée hors COOL/DRY
(volet B), explicitement hors périmètre (cf. §5).

## 2. Données de validation

- **Méthode** : analyse lecture seule de l'historique Recorder via
  `tools/investigations/valider_presence_stabilisee_c4.py` (API History HA, aucun
  état écrit, aucune entité créée).
- **Fenêtre** : 2026-06-17 → 2026-06-19 (post-V2 ; V2 = v16.0.3, 17/06).
- **Couverture** (points historisés) : `presence_famille_unifiee` 55,
  `presence_confort_thermique_stabilisee` 47, `autorisation_clim_cool` 56,
  `autorisation_clim_dry` 74, `clim_target_mode` 72, `clim_blocage_horaire_reel` 30.
- **Creux de présence brute** : 24 (24 complets) — 20 ≥ 120 s (absences réelles,
  attendues), 4 < 120 s (faux-absents, censés être absorbés).

## 3. Verdict par critère (§5)

**Creux courts (< 120 s) observés :**

| Début | Durée | `clim_target_mode` | Stabilisée relâchée | Coupure autorisation |
|---|---|---|---|---|
| 2026-06-18 09:44:56 | 30,7 s | cool | non | aucune |
| 2026-06-18 09:46:57 | **107,1 s** | cool | non | aucune |
| 2026-06-18 17:09:33 | 36,4 s | off | non | aucune |
| 2026-06-18 17:52:32 | 34,9 s | cool | non | aucune |

- **C1 — aucune coupure < 120 s : PASS (exercé).** Trois des quatre creux courts
  surviennent sous `clim_target_mode = cool` (climatisation active, autorisation à
  risque), aucune autorisation COOL/DRY n'est tombée pendant la fenêtre
  d'absorption. Le creux de **107,1 s sous COOL actif absorbé sans coupure** est la
  preuve directe de la classe de faux-absent que V2 devait traiter. Le 4ᵉ creux
  (`off`) est neutre (rien à couper) et n'altère pas le verdict.
- **C2 — réveil sans latence : PASS.** Latence de restauration des autorisations
  au retour de présence : médiane 0 s, max 0 s. Absence de `delay_on` confirmée.
- **C3 — vraies absences préservées : PASS.** Aucune relâche anticipée de la
  stabilisée (< 120 s) ; les 20 absences ≥ 120 s coupent par conception, sans
  anticipation.
- **C4 — calibration `T` : couverte.** Les 4 faux-absents observés sont < 120 s
  (max **107,1 s**). `T = 120 s` couvre la distribution observée.

## 4. Ratification `T = 120 s`

`T = 120 s` est **ratifié** comme seuil opérationnel : il couvre la classe de
faux-absent observée, dont le cas à 107,1 s sous COOL actif.

> **Réserve de surveillance.** Le maximum empirique (107,1 s) laisse une marge de
> ~13 s (~11 %) sous le seuil. Un faux-absent > 120 s serait traité comme une
> absence réelle et couperait COOL/DRY. La marge est **assumée et surveillée** :
> rouvrir l'examen de `T` si un faux-absent approche ou dépasse 120 s.

## 5. Périmètre clos vs hors périmètre

- **Clos (volet A)** : comportement de la présence stabilisée appliquée aux
  décisions **COOL/DRY** (V1 + V2), validé terrain ci-dessus.
- **Hors périmètre (volet B)** : l'arbitrage *étendre la stabilisée aux
  consommateurs de présence brute (chauffage/HEAT, éclairage, vacances…) vs la
  confiner à COOL/DRY* **n'est pas tranché ici**. Il est porté par le dossier
  d'arbitrage dormant **D-PRES** (§9 question 5 et piste P-F de
  [`cadrage_dette_modelisation_presence.md`](../../02_constats/transverses/cadrage_dette_modelisation_presence.md)).
  Sa non-résolution n'empêche pas la clôture du volet A.
- **Hors périmètre (doctrine)** : la ratification du **contrat** comme *opposable*
  (cf. cadrage contrat) est un acte distinct, non emporté par cette validation
  terrain.

## 6. Statut

✅ **CLÔTURÉ** sur le périmètre COOL/DRY. C4 descend de ① Actifs vers ⑤ Clos
récents au registre. Volet B routé vers D-PRES. `T = 120 s` ratifié avec réserve
de surveillance.

## 7. Surveillance post-clôture — fenêtre 2 (2026-06-22 → 2026-06-29)

| Champ | Valeur |
|---|---|
| **Nature** | Datapoint de surveillance (réserve §4) — **ne re-valide ni ne rouvre** la clôture |
| **Outil** | `enquete_presence_meteo.py` (lecture seule ; lentille **météo-conditionnelle**, distincte de l'outil C4) |
| **Commande** | `COOL_REF=24.5 DAYS=7 python3 enquete_presence_meteo.py` |
| **Exposition** | 7 épisodes sains ON→OFF→ON ; 7 en régime `target=cool` ; 7 j `tmax ≥ 24,5 °C` ; 3 reload exclus |

**Résultat.** 3 impacts clim sur la fenêtre, **tous longs** : min ~4202 s (~70 min),
médiane ~5732 s (~1 h 35), max ~8079 s (~2 h 15). **Aucun impact < 120 s.**
Ventilation : 23/06 (4 ép. cool, 0 impact) · 25/06 · 27/06 · 28/06 (1 ép. cool →
1 impact long chacun).

**Lecture.**
- **Non-régression confirmée.** Aucune coupure courte (< 120 s) d'origine
  faux-absent n'est réapparue : la classe corrigée par V1+V2 reste éteinte sur une
  2ᵉ fenêtre caniculaire. C'est une corroboration **par absence de régression** — la
  fenêtre **n'a pas exercé positivement** l'absorption (aucun faux-absent < 120 s
  sous COOL à absorber n'y est observé), à la différence de la preuve C1 (107,1 s
  absorbé). Elle ne constitue donc **pas** une seconde validation autonome, et n'en
  a pas besoin : le volet A est déjà clos.
- **Réserve de surveillance (§4) non déclenchée.** Aucun faux-absent n'a approché
  ou dépassé 120 s ; `T = 120 s` n'est pas remis en cause. La réserve **reste
  ouverte** (surveillance continue) — ce datapoint ne la solde pas.
- **Impacts longs = comportement attendu, hors périmètre.** Les 3 coupures
  (~70 min à ~2 h 15) relèvent de la **frontière de calibration assumée** (§3 du
  suivi) : une absence > 120 s est traitée comme réelle et coupe par conception
  (extinction durable pilotée par le timer 8 h). Elles ne sont **pas** un
  faux-absent court, **pas** un sujet à qualifier, **pas** une validation
  insuffisante.

**Bornes explicites (ce que ce datapoint n'ouvre pas).**
- Si une coupure « longue » se révélait un jour une **perte de présence brute
  durable et fausse** (capteur), cela relèverait de **D-PRES** (modélisation de la
  présence brute), pas de la stabilisée COOL/DRY ni de la calibration `T`. Aucune
  trace de ce cas ici.
- Aucune trace de **court-cycle compresseur** (cycles ON/OFF rapprochés) : les
  impacts sont des coupures **longues uniques**, l'opposé d'un court-cycle.
  **Aucun chantier anti-court-cycle compresseur n'est ouvert** (aucune preuve).

**Statut inchangé.** Clôture volet A maintenue ; verdict §3 et ratification §4
intacts.

*Aucun runtime, contrat ou YAML modifié par ce document (validation lecture seule).*
