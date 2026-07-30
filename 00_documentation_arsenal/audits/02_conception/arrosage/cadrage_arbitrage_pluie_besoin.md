# Cadrage de conception — Arbitrage pluie ↔ besoin hydrique (C41)

**Nature :** document de **conception / cadrage** — **NON normatif**.
**Autorité :** aucune. La seule source normative du domaine est le contrat
[`20_arbitrage_pluie_besoin.md`](../../../contrats/arrosage/20_arbitrage_pluie_besoin.md).
Ce cadrage **explore** ; il **ne fixe aucune règle opposable** et **ne doit pas**
devenir une seconde source de vérité. Toute valeur qui y serait déterminée devra
être **portée par preuve** puis, si elle devient opposable, **remontée dans le
contrat** (ou dans un helper documenté), jamais laissée ici comme norme.

**Chantier :** C41 — voir [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md).
**Frontière :** distinct de **C17** (production / acquisition sécurisée des signaux
pluie, domaine météo). C41 = **réaction / arbitrage** côté arrosage.

---

## 1. Constats issus de l'audit

Chaîne pluie → arrosage établie par lecture statique (deux branches disjointes) :
`pluie_total_local → pluie_cumul_24/48/72h (+ pluie_prevue) → binary_sensor.arrosage_suspension_pluie → binary_sensor.arrosage_intention`.
La branche « épisode » (contact Zigbee SNZB-05, `pluie_evidence_active`,
`pluie_en_cours`, `pluie_recente`) alimente aération/volets, **pas** l'arrosage.

- La suspension pluie côté arrosage est **orpheline de contrat** : sa règle et ses
  seuils ne vivent que dans le commentaire d'en-tête du runtime.
- Le signal consommé est **exclusivement millimétrique** (cumul observé + cumul
  prévu vs helpers de seuil).
- `sensor.pluie_prevue` **calcule et expose** une probabilité (`probabilite_max_pct`)
  **non consommée** ; le **délai avant pluie** n'est pas calculé.
- L'arbitrage est **binaire** : `suspension = obs OR prev` ; toute source `unknown`
  est exclue du OU (doute ⇒ OFF, direction sûre).
- La suspension **inhibe** l'intention **sans** possibilité pour un besoin sol frais
  et bas de l'emporter.

## 2. Défauts du runtime actuel (rappel, référencés dans l'audit)

- **DA-1** suspension binaire mm-seule (probabilité et délai ignorés).
- **DA-2** aucun arbitrage par le besoin (pas d'emportement du besoin établi).
- **DA-3** autorité durable de la pluie passée jusqu'à 72 h contre des sondes fraîches.
- **DA-4** pas de délai d'infiltration distinct d'une suspension durable.
- **DA-5** orpheline de contrat (comblée par le contrat 20).
- **DA-6** probabilité exposée mais dormante.
- **RP-1/2/3** report non borné explicitement, oscillation possible, valeur portée au boot.

## 3. Scénarios à étudier

1. Sol sec établi + pluie prévue faible/incertaine/lointaine → le besoin doit
   pouvoir l'emporter (`besoin_etabli_prioritaire`).
2. Pluie observée significative récente → attente d'infiltration bornée, puis
   réévaluation sur sondes fraîches.
3. Pluie passée ancienne (bord de fenêtre 72 h) + sondes fraîches basses → la pluie
   passée **ne doit plus** suspendre (`aucune_suspension` / besoin prioritaire).
4. Pluie future crédible, proche, quantité utile, sol non urgent → `report_pluie_credible`.
5. Prévision oscillant autour d'un seuil → stabilité attendue (anti-oscillation).
6. Prévision absente / cumul indisponible / seuils helpers indisponibles →
   `pluie_indecidable`, projection relâchée, aucun ordre d'arroser.

## 4. Variables candidates (à qualifier — AUCUNE valeur fixée)

- **Pluie passée** : fenêtres retenues (courtes vs longues), quantité qualifiant une
  pluie « utile », décroissance de l'autorité dans le temps.
- **Infiltration** : durée d'attente bornée ; critère de « effet observable ».
- **Pluie future** : seuil de **crédibilité** (dont usage de la probabilité annoncée
  et concordance de sources), seuil de **quantité utile**, **horizon** pertinent,
  **délai** maximal justifiant un report.
- **Besoin** : niveau de besoin établi au-delà du seuil binaire actuel (à qualifier).
- **Report** : durée maximale, hystérésis / amortissement anti-oscillation.

## 5. Valeurs à déterminer (questions chiffrées différées)

Aucune n'est tranchée ici. Elles ne deviendront opposables qu'après preuve :
- combien de mm et sur quelles fenêtres qualifient une pluie passée « utile » ?
- quelle durée d'attente d'infiltration ?
- quel couple (crédibilité, quantité, délai) qualifie une pluie future « reportable » ?
- quelle durée maximale de report ? quel amortissement contre l'oscillation ?
- quel niveau de besoin établi l'emporte sur une pluie future insuffisante ?

## 6. Données nécessaires

- Historique des cumuls `pluie_cumul_*` et de `pluie_prevue` (quantité **et**
  `probabilite_max_pct`), horodatés, sur une période représentative.
- Historique de la médiane sol (`sensor.jardin_humidite_sol_mediane`) et de l'état
  réservoir, pour corréler pluie ↔ réponse du sol.
- Journal des sessions d'arrosage réelles (`sensor.arrosage_dernier_effectif`,
  verdicts de session) pour mesurer les reports effectifs.
- Traces de prévision (échéances Met.no) pour évaluer crédibilité et délai.

## 7. Méthodes d'analyse

- Corrélation pluie observée → variation de médiane (délai et amplitude d'infiltration).
- Distribution jointe (quantité prévue, probabilité, délai) vs pluie réellement
  survenue (calibration de la crédibilité, **sans** produit simpliste).
- Analyse de stabilité : sensibilité du verdict aux variations horaires de prévision.
- Analyse des faux reports (report alors que la pluie n'est pas venue) et des reports
  manqués (arrosage juste avant une pluie utile).

## 8. Scénarios de mutation (tests à concevoir)

- Frontières de chaque verdict (juste au-dessus / en dessous des seuils candidats).
- Bascule `report_pluie_credible` ↔ `pluie_future_insuffisante` sur variation de
  crédibilité / quantité / délai.
- `besoin_etabli_prioritaire` l'emporte sur une pluie future insuffisante.
- `pluie_indecidable` sur chaque source manquante ⇒ projection **relâchée** (jamais
  suspension fabriquée, jamais ordre d'arroser).
- Non-régression : projection booléenne conforme (serrée uniquement sur
  `attente_infiltration` / `report_pluie_credible`).

## 9. Critères de preuve (runtime et terrain)

- **Runtime** : les six verdicts atteignables et **explicables** ; projection
  conforme ; direction de défaillance vérifiée ; report borné et stable observé sur
  cycles réels.
- **Terrain** : au moins un report justifié suivi d'une pluie réellement utile ; au
  moins un cas où un besoin établi l'emporte sur une pluie insuffisante ; absence
  d'oscillation sur une prévision changeante réelle.
- Les preuves de C11 (approche « pas d'observation à blanc », validation runtime
  après branchement) servent de modèle méthodologique.

## 10. Trajectoire (contrat → runtime)

1. Contrat [`20`](../../../contrats/arrosage/20_arbitrage_pluie_besoin.md) figé
   (catégories + invariants, sans valeur) — **présent lot documentaire**.
2. Exploitation des données (§6/§7) → **valeurs candidates** documentées ici.
3. Implémentation runtime du **verdict riche** + **projection booléenne** (writer
   unique), avec observabilité de diagnostic.
4. Branchement de la projection à l'entrée pluie de `17` (renvoi déjà posé).
5. Validation runtime + terrain (§9), recalibration si nécessaire.
6. Remontée des valeurs stabilisées dans le contrat / helpers documentés ; clôture C41.

## 11. Hors périmètre

Anticipation chaleur (chantier séparé), modulation de durée C11, vérification
post-arrosage, cartographie des six sondes, secours Rain Bird, production/acquisition
des signaux pluie (C17). Aucune de ces questions n'est traitée ici.

---

## Renvois

- Contrat normatif : [`20_arbitrage_pluie_besoin.md`](../../../contrats/arrosage/20_arbitrage_pluie_besoin.md)
- Décision « quand » : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Production pluie (C17, distinct) : [`meteo/pluie_production.md`](../../../contrats/meteo/pluie_production.md)
- Honnêteté cumul : [`06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md) §7
- Cadrage besoin/décision antérieur (trajectoire anticipée §10-11) : [`cadrage_besoin_hydrique_decision_arrosage.md`](cadrage_besoin_hydrique_decision_arrosage.md)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
