# CONTRAT ARSENAL — ARROSAGE
## 20 — Arbitrage pluie ↔ besoin hydrique (couche réaction / décision pluie)

**Version contrat :** v0.1
**Statut :** **Normatif — spécification ; runtime de l'arbitrage NON livré.** Aujourd'hui,
seule une **projection booléenne** existe au runtime (`binary_sensor.arrosage_suspension_pluie`),
calculée directement sur des cumuls et une prévision en millimètres ; ce contrat la
**re-qualifie** comme **projection dérivée** d'un **verdict d'arbitrage riche** qui,
lui, **reste à implémenter**. Ce document **ne crée aucun** YAML, helper, entité,
automation, script, template, checker ni `entity_id`.

> **Positionnement (frontières).** Ce contrat définit **comment la pluie doit
> peser sur la décision d'arroser** : une **couche de réaction / décision**, en
> aval de la **production** des signaux de précipitation
> ([`meteo/pluie_production.md`](../meteo/pluie_production.md), autorité de
> production — INV-PROD-1 « production ≠ réaction ») et de l'**honnêteté du cumul
> observé** ([`06_observation_et_preuves.md`](06_observation_et_preuves.md) §7),
> et en amont de la **décision « quand arroser »**
> ([`17_decision_v1.md`](17_decision_v1.md), inchangée dans ce lot). Il **ne
> produit aucun signal pluie** et **n'exécute rien** : il **consomme** des signaux
> produits ailleurs et **expose un verdict** dont dérive l'entrée pluie de `17`.

> **Garde-fou de lecture.** La pluie ne peut ici que **freiner** (différer) ou
> **relâcher le frein** : elle **n'augmente jamais** l'arrosage et **n'émet jamais
> d'ordre d'arroser**. La décision finale reste soumise à `17` et à **toutes** ses
> autres gardes. **Aucune valeur numérique** (seuil, horizon, durée de report,
> seuil de crédibilité ou de quantité utile) n'est fixée ici : elles relèvent du
> cadrage
> ([`cadrage_arbitrage_pluie_besoin.md`](../../audits/02_conception/arrosage/cadrage_arbitrage_pluie_besoin.md))
> puis d'une **preuve runtime**.

---

## 1. Finalité

Décider si, **à l'instant considéré**, la pluie — **observée** (passée) ou
**raisonnablement prévisible** (future) — justifie de **différer** un arrosage,
**sans** priver le jardin sur un doute, **sans** laisser une pluie passée conserver
indéfiniment autorité contre un besoin renouvelé, et **sans** sacrifier un besoin
hydrique établi à une prévision faible, lointaine ou incertaine. Sert la finalité
**F1/optimisation de l'eau** ([`01_metier.md`](01_metier.md)) : différer un arrosage
**inutile**, mais **ne jamais** transformer une incertitude météo en privation.

## 2. Périmètre

| Inclus | Exclu |
|---|---|
| Arbitrage pluie observée / pluie future / besoin hydrique établi → **verdict riche** | **Production** des signaux pluie (→ [`meteo/pluie_production.md`](../meteo/pluie_production.md)) |
| **Projection booléenne** dérivée, consommée par la décision (`17`) | **Sémantique du cumul** observé (0.0 vs `unknown`) (→ [`06`](06_observation_et_preuves.md) §7) |
| Attente d'infiltration **bornée** après pluie observée | **Décision « quand »**, fenêtre, cooldown, plafond (→ [`17`](17_decision_v1.md)) |
| Qualité / fraîcheur **exigées pour la décision** | **Exécution** Rain Bird, `rain_delay`, coexistence (→ [`03`](03_coexistence_rainbird.md), [`11`](11_mode_manuel_supervise.md)) |
| Diagnostic de l'arbitrage (verdict, facteurs, données manquantes) | Réaction des **ouvrants** à la pluie (→ [`../volets_pluie.md`](../volets_pluie.md)) |

## 3. Vocabulaire normatif

- **Pluie observée** : précipitation réellement mesurée (cumuls glissants), au sens
  de [`06`](06_observation_et_preuves.md) §7 et [`pluie_production.md`](../meteo/pluie_production.md).
- **Attente d'infiltration** : délai **borné** après une pluie observée pendant
  lequel Arsenal **diffère** pour laisser l'eau s'infiltrer et son effet devenir
  observable. **Distincte** d'une suspension durable.
- **Pluie future** : précipitation **annoncée** par prévision — une **présomption,
  jamais un fait** ([`pluie_production.md`](../meteo/pluie_production.md) INV-PROD-7).
- **Crédibilité** (de l'événement futur) : degré de confiance dans la survenue de la
  pluie annoncée. Elle **peut** s'appuyer sur la **probabilité** annoncée et sur la
  **concordance de sources**, **sans** s'y réduire.
- **Quantité potentiellement utile** : ampleur de la pluie (observée ou future)
  susceptible de **répondre au besoin**. Une quantité mesurée/annoncée **n'est pas
  automatiquement** utile.
- **Délai avant l'événement** : temps estimé avant le début d'une pluie future.
- **Besoin hydrique établi** : besoin du sol **déjà qualifié** par la chaîne besoin
  existante ([`04`](04_besoin_hydrique.md), [`15`](15_canal_reservoir_sol.md),
  `binary_sensor.arrosage_besoin_sol`). *(Le **niveau** de ce besoin — au-delà du
  seuil binaire actuel — reste **à qualifier** ultérieurement ; ce contrat
  **n'introduit pas** de notion normative d'« urgence » non encore existante.)*
- **Report** : décision de différer l'arrosage pour raison de pluie, **bornée dans
  le temps** et **explicable**.
- **Verdict d'arbitrage pluie** `‹verdict_arbitrage_pluie›` : la **vérité métier**
  du domaine (§7).
- **Projection booléenne** `‹suspension_pluie_derivee›` : dérivée du verdict pour
  compatibilité avec `17` (§8).

## 4. Entrées factuelles (par renvoi — aucune source redéfinie)

Ce contrat **ne redéfinit ni ne produit** aucune source ; il consomme, **par
renvoi**, des signaux dont l'autorité de production est ailleurs. Les natures
ci-dessous sont **distinctes par construction** ([`pluie_production.md`](../meteo/pluie_production.md)
INV-PROD-2, qualifications non fusionnables) et **ne doivent pas** être fondues :

| Nature factuelle | Ce qu'elle établit | Autorité de production |
|---|---|---|
| **Pluviomètre quantitatif** (cumuls observés) | quantité réellement tombée, par fenêtres | [`pluie_production.md`](../meteo/pluie_production.md) §5 ; sémantique honnête [`06`](06_observation_et_preuves.md) §7 |
| **Prévision — quantité** | quantité **annoncée** sur un horizon (présomption) | [`pluie_production.md`](../meteo/pluie_production.md) (`pluie_prevue`, INV-PROD-7) |
| **Prévision — probabilité** | crédibilité **annoncée** de l'événement | produite par la prévision, **aujourd'hui exposée mais non consommée** (§13) |
| **Contact / surface mouillée** (détecteur binaire) | « il pleut / c'est mouillé maintenant » | [`pluie_production.md`](../meteo/pluie_production.md) (évidence any-rain, épisode) |
| **Capteur / inhibition Rain Bird** | inhibition **matérielle** côté contrôleur | matériel Rain Bird — **hors observation Arsenal** ([`03`](03_coexistence_rainbird.md)) |

> **Distinction fonctionnelle à préserver.** Ces natures **n'ont pas la même valeur
> métier** : une **détection binaire** ne quantifie pas (elle ne qualifie jamais une
> pluie « utile ») ; une **prévision** n'est pas une mesure ; une **inhibition
> matérielle** Rain Bird relève du **secours**, pas d'une observation Arsenal. Le
> contrat **ne suppose aucune équivalence** entre elles. *(État constaté :
> l'arbitrage actuel ne consomme que le pluviomètre quantitatif et la prévision de
> quantité ; le contact binaire et l'inhibition Rain Bird **ne participent pas** —
> voir §13 et le cadrage pour l'étude de leur éventuelle valeur de **confirmation
> indépendante** ou de **diagnostic**.)*

## 5. Qualité et fraîcheur exigées

- L'arbitrage **exige** que chaque entrée consommée soit **disponible, fraîche et
  plausible** pour peser sur le verdict ; à défaut, l'entrée **ne participe pas**
  (elle n'est **ni** lue comme 0, **ni** comme « pas de pluie », **ni** comme « pas
  de besoin »).
- La **fraîcheur** de la donnée pluie est régie en amont par
  [`pluie_production.md`](../meteo/pluie_production.md) (INV-PROD-6, disponibilité
  honnête) et [`06`](06_observation_et_preuves.md) §7 (cumul honnête : `0.0`
  **confirmé** vs `unavailable` **inconnu**). Ce contrat **n'en crée pas** de
  seconde définition ; il **exige** en revanche que l'arbitrage **tienne compte**
  de l'état de disponibilité (une donnée absente/périmée est traitée comme
  **non qualifiante**, pas comme une valeur).
- La qualité du **besoin hydrique** (sol) relève de [`14`](14_qualite_donnees_sol.md)
  et [`15`](15_canal_reservoir_sol.md).

## 6. Pluie observée (passée)

- Une pluie observée est un **événement mesuré, borné dans le temps**, **pas** une
  preuve durable que le sol **reste** suffisamment humide.
- Elle peut légitimement motiver une **attente d'infiltration** bornée (§7) et,
  au-delà, informer l'arbitrage — mais elle **ne conserve pas** autorité **au-delà
  d'un horizon borné**, ni **contre** un besoin hydrique **renouvelé** établi par
  des mesures de sol **fraîches**.
- Les **fenêtres** distinctes (courtes / longues) restent des **canaux séparés**
  (jamais fondus en une autorité unique opaque). Leur portée temporelle et les
  quantités qualifiant une pluie « utile » sont des **valeurs différées** (cadrage).

## 7. Attente d'infiltration (bornée)

- Après une pluie observée jugée pertinente, l'arbitrage peut conclure à une
  **attente d'infiltration** : différer **pour une durée bornée**, le temps que
  l'eau s'infiltre et que son effet devienne **observable** sur le sol.
- Cette attente est **distincte** d'une suspension durable : elle est **explicitement
  bornée**, **stable** (pas de recalcul oscillant), et **explicable**.
- Sa **durée** est une **valeur différée** (cadrage puis preuve runtime).

## 8. Pluie future (annoncée)

L'arbitrage d'une pluie future **distingue explicitement**, sans les fondre :
1. la **crédibilité** de l'événement (dont **probabilité** annoncée et **concordance
   de sources**) ;
2. la **quantité potentiellement utile** annoncée ;
3. le **délai** avant l'événement ;
4. le **besoin hydrique établi** à l'instant.

- **Ni** la quantité seule, **ni** la probabilité seule, **ni** leur **produit
  simpliste** `probabilité × quantité` ne suffisent à justifier un report.
- Un report pour pluie future n'est légitime que si l'événement est **suffisamment
  crédible**, **suffisamment proche** et **potentiellement utile** — les seuils de
  ces qualificatifs étant **différés** (cadrage).
- Une prévision **absente / vide / non qualifiable** ⇒ verdict d'**indécidabilité**
  pluie (§9 / §11), **jamais** « pas de pluie prévue », **jamais** 0.

## 9. Arbitrage pluie ↔ besoin — verdict riche (vérité métier)

Le domaine expose une **vérité métier unique** : le **verdict d'arbitrage pluie**
`‹verdict_arbitrage_pluie›`, aux valeurs **exclusives** et **explicables** :

| Verdict | Sens |
|---|---|
| `aucune_suspension` | Aucune raison liée à la pluie de différer. |
| `attente_infiltration` | Pluie observée récente ⇒ attente **bornée** d'infiltration/effet. |
| `report_pluie_credible` | Pluie future **crédible, suffisamment proche et potentiellement utile** ⇒ report justifié. |
| `pluie_future_insuffisante` | Pluie future **insuffisante / trop incertaine / trop lointaine** pour justifier un report. |
| `besoin_etabli_prioritaire` | **Besoin hydrique établi** rendant le report **injustifié** (le besoin l'emporte sur une pluie insuffisante/incertaine). |
| `pluie_indecidable` | **Données pluie insuffisantes / non qualifiables** pour statuer sur un report. |

- Le verdict est une **fonction déterministe et explicable** de ses entrées ; il
  **expose** les facteurs ayant pesé (§12).
- Le verdict est la **seule autorité sémantique** du domaine « pluie dans la
  décision ». La projection booléenne (§10) **n'est pas** cette autorité.

## 10. Projection booléenne dérivée (compatibilité `17`)

La décision `17` consomme aujourd'hui une **entrée booléenne** de suspension pluie.
Cette entrée est **une projection dérivée** du verdict riche, **jamais** l'inverse :

```
‹verdict_arbitrage_pluie›  (vérité métier, §9)
   → ‹suspension_pluie_derivee›  (projection booléenne de compatibilité)
   → consommation par la décision 17 (gate « hors suspension pluie »)
```

- La projection vaut **« différer »** (frein **serré**) **uniquement** pour les
  verdicts qui justifient un report : `attente_infiltration` et
  `report_pluie_credible`.
- Elle vaut **« ne pas différer »** (frein **relâché**) pour **tous** les autres
  verdicts — y compris `pluie_future_insuffisante`, `besoin_etabli_prioritaire`
  **et `pluie_indecidable`**.
- La projection est un **frein additif** ([`06`](06_observation_et_preuves.md) §7.3) :
  frein relâché ⇒ **elle n'actionne aucun accélérateur** et **n'émet aucun ordre
  d'arroser** ; la décision reste soumise à **toutes** les autres gardes de `17`
  (besoin sol, fenêtre, cooldown, préconditions/disponibilité pont, état réservoir).

## 11. Indisponibilités et abstentions — direction de défaillance

> **Une incapacité à qualifier les données pluie ne vaut ni absence de pluie, ni
> absence de besoin.**

- Des données pluie insuffisantes / non qualifiables produisent le verdict
  **explicite** `pluie_indecidable` (ou une qualité de données exposée comme
  insuffisante) — **jamais** une suspension fabriquée.
- En conséquence, la **projection booléenne reste relâchée** sur `pluie_indecidable`
  (le frein pluie ne se serre pas sur un doute pluie).
- Cela **ne constitue jamais** un ordre d'arroser : la décision demeure **entièrement
  soumise** à `17` et à ses autres gardes (dont l'**anti-faux-négatif sol** de
  [`04`](04_besoin_hydrique.md) §4 / [`17`](17_decision_v1.md) §4, et l'abstention
  prudente sur canal sol indisponible).
- **Ce contrat ne possède que le frein pluie.** Il **n'émet aucune abstention
  générale** : prononcer une abstention d'arrosage sur un doute **pluie** créerait
  une **autorité concurrente** susceptible de priver le jardin — **interdit**. La
  seule autorité d'abstention globale reste `17`.

## 12. Autorité, writer et diagnostic

- **Autorité métier unique** : le verdict d'arbitrage pluie (§9) est la seule vérité
  du domaine « pluie dans la décision » ; **un seul writer** le produit (runtime
  futur). La projection booléenne (§10) en dérive et n'a **pas** d'autorité propre.
- **Séparation stricte** : ce contrat **ne décide pas « quand »** (17), **ne produit
  pas** les signaux pluie (production), **n'exécute rien** (Rain Bird).
- **Diagnostic attendu** (le backend décide, l'UI restitue) : le domaine doit
  **exposer**, sans reconstruction, au minimum — le **verdict**, les **facteurs
  ayant participé** (crédibilité, quantité utile, délai, besoin, fenêtres
  observées), l'**état de qualité/fraîcheur** des entrées, et les **données
  manquantes** (rendues **visibles**, jamais maquillées en 0 ou en « pas de pluie »).

## 13. Constats d'état (non normatifs — renvoi cadrage)

*(Cette section **décrit l'existant** pour situer la cible ; elle **n'énonce aucune
norme** et **ne fige aucune valeur**.)*
- La probabilité de prévision est **aujourd'hui exposée** (attribut de
  `sensor.pluie_prevue`) **mais consommée nulle part** ; le délai avant pluie
  **n'est pas** calculé. Leur exploitation relève du cadrage.
- Le contact binaire de pluie et l'inhibition matérielle Rain Bird **ne participent
  pas** à l'arbitrage actuel ; l'étude de leur éventuelle valeur (confirmation
  indépendante / diagnostic) relève du cadrage.

## 14. Invariants (opposables)

1. **La pluie ne peut qu'ajouter ou relâcher un frein ; elle n'augmente jamais
   l'arrosage** et **n'émet jamais d'ordre d'arroser**.
2. **Une prévision n'est jamais un fait** (présomption ; `unknown`/`unavailable` ≠ 0
   ≠ « pas de pluie » ≠ « pas de besoin »).
3. **Pluie passée et pluie future sont des canaux distincts**, jamais fondus en un
   score opaque.
4. **Ni quantité seule, ni probabilité seule, ni leur produit simpliste** ne
   qualifie un report : crédibilité, quantité utile, délai et besoin établi restent
   **explicitement distingués**.
5. **Une pluie passée ne conserve pas durablement autorité** contre un besoin
   renouvelé établi par des mesures de sol **fraîches** ; son autorité est **bornée**.
6. **Une pluie observée peut imposer une attente d'infiltration bornée**, distincte
   d'une suspension durable.
7. **Tout report est borné, stable et explicable** ; une prévision changeante **ne
   doit pas** produire d'oscillation incontrôlée du verdict.
8. **Une donnée pluie non qualifiable ⇒ verdict d'indécidabilité explicite**, jamais
   une suspension fabriquée ; la **projection reste relâchée** ; **jamais** d'ordre
   d'arroser ; **jamais** d'abstention générale émise par ce contrat.
9. **Vérité métier = verdict riche** ; la projection booléenne en **dérive**
   (compatibilité `17`) et n'est **pas** l'autorité du domaine.
10. **Une seule autorité métier, un seul writer** ; **exécution Rain Bird hors
    périmètre**.
11. **Diagnostic honnête** : verdict, facteurs participants, qualité et **données
    manquantes visibles**.

## 15. Exclusions (hors périmètre)

- ❌ **Inventer** un seuil, un horizon, une durée de report, un seuil de crédibilité
  ou de quantité utile (valeurs **différées**, cadrage puis preuve) ;
- ❌ une **formule `probabilité × quantité`** ou tout **score composite opaque** ;
- ❌ **fondre** pluie passée et pluie future ;
- ❌ faire de la pluie un **accélérateur** d'arrosage ;
- ❌ **anticipation chaleur** / besoin futur climatique (chantier séparé) ;
- ❌ modifier la **modulation de durée** ([`19`](19_modulation_duree.md)) ;
- ❌ créer une **vérification post-arrosage** ou une cartographie des sondes ;
- ❌ modifier le **secours Rain Bird** / `rain_delay` / la coexistence ;
- ❌ réécrire la **logique de `17`** (renvoi minimal seulement) ;
- ❌ tout **runtime / UI / helper / automation / script / template / checker /
  `entity_id`** dans ce lot documentaire.

## 16. Critères de validation

La cible est un **arbitrage réellement branché** (pas d'observation à blanc
prolongée), validé **en runtime** après mise en service. La validation devra couvrir
au minimum :
- les **six verdicts** atteignables sur des situations réelles ou reconstituées,
  chacun **explicable** par ses facteurs ;
- la **projection booléenne** conforme (§10 : serrée uniquement sur
  `attente_infiltration` / `report_pluie_credible` ; relâchée sinon, y compris
  `pluie_indecidable`) ;
- la **direction de défaillance** (§11) : donnée pluie manquante ⇒ `pluie_indecidable`,
  projection relâchée, aucun ordre d'arroser, aucune abstention générale ;
- le **caractère borné et stable** du report (pas d'oscillation sur prévision
  changeante) ;
- l'**absence de régression** de `17` (aucune autre garde modifiée) ;
- le **diagnostic** (§12) exposant verdict + facteurs + qualité + données manquantes.

## 17. Limites & preuves manquantes

- **Aucune valeur n'est fixée** : seuils de crédibilité / quantité utile, fenêtres
  de pluie passée, durée d'attente d'infiltration, durée maximale de report,
  amortissement anti-oscillation — **tous différés** au cadrage puis à la **preuve
  runtime/terrain**.
- La **qualification d'un niveau** de besoin (au-delà du seuil binaire actuel) et
  l'exploitation de la **probabilité** / du **délai avant pluie** sont **à établir**
  (cadrage).
- Ce contrat **spécifie** l'état cible ; il **ne préjuge pas** de la forme runtime
  exacte (template, attributs, helper) ni des `entity_id`, décidés à l'implémentation
  (convention de nommage conceptuel du domaine, [`README.md`](README.md)).

---

## Renvois

- Décision « quand » (consomme la projection booléenne) : [`17_decision_v1.md`](17_decision_v1.md)
- Besoin hydrique (perception ; pluie récente/prévue diminuent le besoin) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Honnêteté du cumul observé (0.0 vs `unknown` ; frein additif) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md) §7
- Qualité des données sol : [`14_qualite_donnees_sol.md`](14_qualite_donnees_sol.md)
- Canal réservoir sol (médiane, minimum, hétérogénéité) : [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)
- Production des signaux de précipitation (autorité amont) : [`../meteo/pluie_production.md`](../meteo/pluie_production.md)
- Coexistence / secours Rain Bird (hors périmètre) : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Cadrage de conception (valeurs différées, exploration) : [`cadrage_arbitrage_pluie_besoin.md`](../../audits/02_conception/arrosage/cadrage_arbitrage_pluie_besoin.md)
- Registre du chantier (C41) : [`REGISTRE_CHANTIERS.md`](../../audits/REGISTRE_CHANTIERS.md)
- Index du domaine : [`README.md`](README.md)
