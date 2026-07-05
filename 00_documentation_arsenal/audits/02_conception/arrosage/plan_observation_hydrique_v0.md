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
