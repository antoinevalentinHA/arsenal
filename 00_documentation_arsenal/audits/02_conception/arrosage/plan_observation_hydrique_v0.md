# Plan d'observation hydrique v0 — questions mesurables & critères de sortie

| Champ | Valeur |
|---|---|
| **Type** | Plan d'observation (conception, **non normatif**) |
| **Domaine** | Arrosage — observabilité hydrique jardin (v0) |
| **Statut** | **Ouvert — guide d'observation, non opposable.** Aucune décision, aucun seuil, aucun runtime. |
| **Version** | 0.1 |
| **Date** | 2026-06-26 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `a4a80bc` |
| **Cadre** | Aucun YAML, aucun runtime. Les valeurs citées sont exploratoires ; les critères de sortie sont **indicatifs, non normatifs**. |

> **Objet.** Donner un **but** à l'observation v0 pour **éviter le logging
> éternel** : définir **ce que l'observation doit permettre d'apprendre** avant
> d'envisager une recommandation **v0.5**. Orienté **questions mesurables**, pas
> calendrier.

> **Garde-fou.** **Aucune date future** n'est posée ; **aucun « après X
> semaines »**. Les critères sont formulés en **conditions d'observation
> atteintes**, pas en échéance. Contrats normatifs associés :
> [`13_observation_hydrique_jardin.md`](../../../contrats/arrosage/13_observation_hydrique_jardin.md),
> [`14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md).

---

## 1. Pourquoi un plan (et pas seulement du logging)

L'observation v0 n'est utile que si elle **répond à des questions précises**. Sans
cible d'apprentissage, l'historisation s'éternise sans rien trancher. Ce plan
**liste les questions** et **les conditions** sous lesquelles on jugera en savoir
assez pour passer à une **recommandation diagnostique non actionnable** (v0.5).

Rappels : **une zone Rain Bird, trois points de mesure** ; **capteurs non
calibrés** ; **aucun seuil** ; **aucune action**.

---

## 2. Questions mesurables

### 2.1 Cinétique du réservoir sol
- Combien de temps les capteurs restent-ils **au-dessus de leur niveau haut**
  après un arrosage ?
- À quelle **vitesse redescendent-ils** par temps **doux / chaud / très chaud** ?
- Comment évoluent-ils après **24 h / 48 h / plusieurs jours sans pluie** ?

### 2.2 Comportement du Point 2
- Le **Point 2** est-il **réellement moins réactif**, ou seulement **placé dans une
  zone différente** (sol plus drainant, ombre, racines) ?
  (Observation, **pas** correction — [`14`](../../../contrats/arrosage/14_qualite_donnees_sol.md) §6.)

### 2.3 Pluie efficace
- **Quelle pluie fait réellement bouger** les capteurs ?
- Une pluie de **2–5 mm** est-elle **interceptée par le couvert végétal** (jardin
  dense, esprit sous-bois) ?
- **Quelle pluie devient « efficace »** dans ce jardin (croisement cumul ↔ réponse
  sol) ?

### 2.4 Plantes vs capteurs (stress précoce)
- L'**helxine** souffre-t-elle alors que la **médiane sol reste correcte** ?
- Les **fougères / érable japonais / tomates** montrent-ils un **stress avant les
  capteurs** ?
- Un **seul point sec** correspond-il à une **vraie zone sensible** ou à un
  **artefact** ? (jamais déclencheur de zone — [`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §4)

### 2.5 Demande climatique
- La **canicule accélère-t-elle le tarissement** visible sur les capteurs ?
- Les **nuits chaudes** empêchent-elles la **récupération** ?
- Comment se comporte le système **après pluie puis chaleur** ?

### 2.6 Rythme d'arrosage (observation, pas règle)
- Quel **délai minimal** entre deux arrosages semble **raisonnable** (observé) ?
- Combien de temps **après un arrosage Rain Bird** la **remontée** est-elle visible
  sur les capteurs ?

---

## 3. Ce que l'observation doit produire (sorties attendues)

- des **courbes de tarissement** par point et par régime météo (doux/chaud/canicule) ;
- une **première idée des fenêtres de fraîcheur** réelles des capteurs (alimente la
  durée frais/stale de [`14`](../../../contrats/arrosage/14_qualite_donnees_sol.md), **non figée**) ;
- une **caractérisation du Point 2** (zone vs défaut) ;
- une **corrélation pluie ↔ réaction sol** (pluie efficace) ;
- des **cas de désaccord entre points** documentés (hétérogénéité réelle).

---

## 3 bis. Observations acquises

> Constats datés, **purement descriptifs** — aucune règle, aucun seuil, aucune
> recommandation n'en découle en v0 (frontière §5 tenue).

### 2026-07-05 (soirée) — réponse sol à un arrosage réel de 35 min (T04)

Premier arrosage réel **instrumenté de bout en bout** (session supervisée
manuelle station 1, 18:58 → 19:33 locale, 35 min, orchestration Lot D,
verdict `close_nominale`). Relevé Recorder de
`sensor.jardin_humidite_sol_mediane`, 19:00 → 20:53 locale :

- **Amplitude** : médiane 26,1 % → 30,6 % (**+4,5 pts**, ~+17 % relatif),
  **encore en hausse** à la fin du relevé (pic réel non capturé, attendu
  plus tard dans la soirée) ;
- **Lag d'infiltration ≈ 25 min** : quasi-plateau de l'ouverture de l'eau
  (18:58) jusqu'à ~19:23, puis montée régulière ;
- **Percolation post-arrosage dominante** : l'essentiel de la hausse
  (27 → 30,6) s'est produit **après** l'arrêt de l'eau (19:33) — la réponse
  utile s'étale sur 1 à 2 h au moins après le stop ;
- **Franchissement du seuil de déclenchement** (30 %) à ~20:38, soit
  ~1 h 05 après la fin de l'arrosage ;
- **Contexte climatique** : journée à forte demande (ET₀ ≈ 6 mm/j) — une
  part de l'apport de surface s'évapore avant d'atteindre les sondes ;
- **Limite du relevé** : médiane seule — la lecture **par point** (dont le
  Point 2, §2.2) et l'hétérogénéité restent à extraire pour ce cycle ; la
  médiane peut sous-estimer la réponse si un point traîne ;
- **Effets décisionnels constatés (conformes)** : cooldown ré-armé à 18:58
  (`dernier_effectif`) ; `besoin_sol` maintenu `on` par hystérésis à 30,6 %
  (< seuil + hystérésis) — le cooldown porte seul l'anti-sur-arrosage.

Lecture prudente : **une seule occurrence**, par temps chaud, en arrosage
manuel de 35 min. Ni la cinétique ni le lag ne sont généralisables avant
d'autres cycles (doux / pluie / durées différentes).

### 2026-07-19 — dose-réponse « 35 min » (4 cycles auto) & non-fiabilité du signal sol médian (T05)

Analyse Recorder (base courante, **lecture seule**) des **4 cycles automatiques**
(déclenchement 05:30 local, durée **35 min** confirmée par
`arrosage_session_duree_minutes`), fenêtre d'infiltration **12 h**, juillet 2026 —
médiane `sensor.jardin_humidite_sol_mediane`, seuil de déclenchement 30 % :

| Cycle | avant | pic 12 h | montée | lag infiltration |
|---|---|---|---|---|
| 07-08 | 30,3 | 36,2 | +5,9 | ~5 h 40 |
| 07-09 | 21,4 | 48,0 | +26,6 | ~4 h 20 |
| 07-10 | 31,4 | 37,1 | +5,7 | ~2 h 40 |
| 07-18 | 33,2 | 51,3 | +18,1 | ~36 min |

- **Sur-arrosage constaté** : le pic post-arrosage atteint **36–51 %**,
  **systématiquement au-dessus du seuil de 30 %** (dépassement +6 à +21 pts) ;
  montée médiane ~12 pts (moyenne ~14). Même le plus petit effet (+5,7) franchit
  le seuil ⇒ en régime doux / faible demande, 35 min **remplit au-delà du
  besoin** (réserve de plusieurs jours ; intervalles observés 24–64 h).
- **Signal sol non fiable pour une dose-réponse** : pour la **même dose (35 min)**,
  la montée va de **+5,7 à +26,6** (×4,7) et le lag d'infiltration de **36 min à
  ~5 h 40**. Une part s'explique (le cycle parti le plus sec, 21,4 %, monte le
  plus — courbe de mouillage plausible), **mais pas tout** (07-18 part plus humide
  que 07-08 et monte 3×). Dispersion + lags erratiques ⇒ `…_mediane` n'est **pas
  encore une dose-réponse reproductible**.
- **Conséquence C11 (modulation de durée)** : confirme que le prérequis **P2**
  (capteurs sol à fiabiliser / calibrer — [`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §9,
  [`14`](../../../contrats/arrosage/14_qualite_donnees_sol.md) §6) **n'est pas
  réuni** : caler des bornes de modulation sur ce signal serait **cosmétique**
  (cf. [`cadrage_modulation_duree_arrosage.md`](cadrage_modulation_duree_arrosage.md) §5).
- **Note annexe (décision)** : trois des quatre cycles se déclenchent à médiane
  ~30–33 (**au seuil ou au-dessus**) ⇒ la décision ne se réduit pas à
  « médiane < 30 » — un autre gate joue (point sec / points frais). Observation,
  pas correction ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §4).
- **Contexte parc capteurs (info opérateur, 2026-07-19)** : le parc sol est passé
  de **3 à 6 capteurs**. Les constats ci-dessus datent du **parc en cours de
  fiabilisation** ; la dose-réponse et les fenêtres de fraîcheur (§2.1, §3)
  devront être **ré-observées sur le parc à 6 capteurs**. *(Les mentions « trois
  points de mesure » des contrats 12/13/14 et du §1 de ce plan sont désormais en
  retard sur le runtime — mise à jour documentaire à arbitrer, hors de cette
  entrée d'observation.)*

Lecture prudente : **petit échantillon** (4 cycles auto), **juillet chaud seul**,
**médiane seule** (lecture par point non extraite), fenêtre 12 h susceptible de
capter du bruit diurne. Aucune règle, aucun seuil, aucun runtime ; **durée de
base inchangée** (réglage opérateur, non touché).

---

## 4. Critères de sortie vers v0.5 (indicatifs, **non normatifs**)

On jugera l'observation v0 **suffisante** pour envisager une **recommandation
diagnostique non actionnable (v0.5)** lorsque **ces conditions sont atteintes**
(formulées en **observations acquises**, pas en délai) :

- [ ] **plusieurs cycles de tarissement** observés (différents régimes météo) ;
- [ ] **au moins un épisode chaud** observé ;
- [ ] **au moins une pluie significative** observée (et sa réponse sol) ;
- [ ] **comportement du Point 2 mieux compris** (zone vs défaut) ;
- [ ] **premières fenêtres de fraîcheur** des capteurs **confirmées** ;
- [ ] **corrélation minimale pluie ↔ réaction sol** établie ;
- [ ] **absence de recommandation runtime en v0 confirmée** (frontière tenue).

> Ces critères sont des **conditions d'apprentissage**, **non** des seuils
> opposables et **non** un calendrier. La décision de passer à v0.5 reste un
> **arbitrage opérateur**.

---

## 5. Hors périmètre (rappel)

- ❌ aucun seuil, aucune calibration, aucune correction du Point 2 ;
- ❌ aucune recommandation émise, aucun automatisme, aucune action Rain Bird ;
- ❌ aucun runtime / UI / helper / automation / script / template ;
- ❌ la canicule n'est pas un déclencheur ; un seul point sec n'est pas un
  déclencheur de zone.

---

## Liens

- Chapeau observation hydrique (v0) : [`contrats/arrosage/13_observation_hydrique_jardin.md`](../../../contrats/arrosage/13_observation_hydrique_jardin.md)
- Qualité des données sol : [`contrats/arrosage/14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md)
- Cadrage du chantier (#99) : [`cadrage_besoin_hydrique_decision_arrosage.md`](cadrage_besoin_hydrique_decision_arrosage.md)
- Confrontation des avis (#100) : [`confrontation_avis_besoin_hydrique.md`](confrontation_avis_besoin_hydrique.md)
- Capteurs humidité sol : [`contrats/arrosage/12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md)
- Index audits : [`audits/index.md`](../../index.md)

> **Portée.** Plan d'observation orienté apprentissage : transforme le logging en
> questions mesurables et critères de sortie. Aucun seuil, aucun runtime, aucune
> action, aucune date future. Observation avant recommandation.
