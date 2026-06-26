# CONTRAT ARSENAL — ARROSAGE
## 13 — Observation hydrique jardin (contrat chapeau, v0 observation/diagnostic)

**Version contrat :** v0.1
**Statut :** **Normatif — chapeau de l'observabilité hydrique.** Fixe la doctrine
opposable du futur runtime d'**observation + diagnostic** hydrique du jardin
(**v0**), **en deçà** de toute recommandation et de toute action. Aucune entité
runtime n'est créée par ce lot.

> **Arbitrage retenu (post-conception, audits #99/#100).** **v0 = observation +
> diagnostic uniquement.** La v0 **n'émet aucune recommandation d'arrosage**, **ne
> crée aucun runtime / UI / action**. Elle **prépare** proprement les futurs
> contrats et runtime d'observabilité. **Option A renforcée** retenue ; **Option B
> refusée en runtime** à ce stade ; **Option C refusée**.

> **Garde-fou de lecture.** Ce contrat **ne fixe aucun seuil hydrique final**, **ne
> décide aucune calibration**, **ne relie pas** l'humidité sol à Rain Bird. Une
> zone Rain Bird, **trois points de mesure**.

---

## Objet

Définir le **socle d'observabilité hydrique du jardin** : ce qu'Arsenal **observe**
et **diagnostique** (qualité/confiance) à partir des trois points d'humidité sol et
de la demande climatique, **sans** produire de **recommandation** ni d'**action**.
Ce contrat est le **chapeau** : il pose le vocabulaire, les invariants et
l'architecture par **canaux** ; les couches sous-jacentes (qualité des données,
agrégats, futurs canaux) sont portées par des contrats dédiés et des documents de
conception.

Amont de conception (non normatif) :
- cadrage du chantier : [`cadrage`](../../audits/02_conception/arrosage/cadrage_besoin_hydrique_decision_arrosage.md) (PR #99) ;
- confrontation des avis externes : [`confrontation`](../../audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md) (PR #100) ;
- plan d'observation v0 : [`plan_observation_hydrique_v0`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md).

---

## 1. Invariants structurants

1. **Une seule zone Rain Bird** / une seule station d'arrosage.
2. **Trois points de mesure** d'humidité, **pas trois zones d'arrosage**
   ([`12`](12_capteurs_humidite_sol.md) §2).
3. **Arrosage par aspersion** (couvert végétal interceptant ; timing important).
4. **Observation avant recommandation** ; **recommandation avant action**.
5. **Aucun automatisme** d'arrosage à ce stade.
6. **Pas de score unique** en v0 : aucune fusion destructrice d'information.
7. **Pas de seuil hydrique final** ; **pas de calibration déduite**.
8. **Capteurs sol ≠ déclencheurs** d'arrosage : ils **informent**, ne **commandent**
   rien.

---

## 2. Séparation des couches

| Couche | Rôle | Statut v0 |
|---|---|---|
| **Observation** | Mesures brutes et **dérivés factuels** (médiane, minimum, hétérogénéité, fraîcheur…) | **cible v0** |
| **Diagnostic** | **Qualité / confiance / fraîcheur / cohérence** des données ([`14`](14_qualite_donnees_sol.md)) | **cible v0** |
| **Recommandation** | Classes de besoin (§5) — **vocabulaire futur, NON émis en v0** | **hors v0** |
| **Action** | Rain Bird / scripts supervisés ([`11`](11_mode_manuel_supervise.md)) | **hors périmètre immédiat** |

> **Frontière dure v0.** Le futur runtime v0 **s'arrête à la frontière
> diagnostic / recommandation**. Aucun **état de recommandation** n'est émis ;
> aucun **script d'arrosage** n'est piloté par ces capteurs ; aucun **bouton
> d'action** n'est ajouté.

---

## 3. Architecture par canaux

Le besoin hydrique sera **structuré en canaux séparés** (consensus de conception),
**jamais** un indicateur global unique. **En v0, seuls les éléments d'observation
factuelle du canal sol et la qualité des données sont des cibles runtime** ; le
reste est **vocabulaire de cadrage** (futur).

### 3.1 Canal réservoir sol (lent)
- **médiane** des points frais ;
- **minimum** (point le plus sec) ;
- **hétérogénéité** (`max − min`) ;
- **fraîcheur** (qualité, [`14`](14_qualite_donnees_sol.md)) ;
- **tendance** (futur) ; **tarissement** (futur).

### 3.2 Canal demande climatique (rapide) — *cadrage futur, non v0-runtime*
- saison ; température extérieure ; **Tmax prévue** ;
- **chaleur consécutive** ; **nuits chaudes** ; **canicule** ;
- humidex / proxy **ET** éventuel.

> La **demande climatique ne déclenche aucune action autonome** ; la **canicule
> n'est pas un déclencheur**. Température = **proxy de demande**, jamais indicateur
> d'eau.

### 3.3 Modulateurs — *cadrage futur, non v0-runtime*
- **pluie récente effective** ; **pluie prévue crédible** ;
- **dernier arrosage** ; **disponibilité Rain Bird** ;
- **qualité des données** ([`14`](14_qualite_donnees_sol.md)) ;
- **vérification humaine** si doute (drapeau de diagnostic, pas une action).

---

## 4. Frontière v0 (rappel opposable)

- la **v0 documentaire** peut définir le **vocabulaire futur** (classes §5) ;
- le **runtime v0** futur ne devra émettre que **observation + diagnostic** ;
- **aucun état de recommandation** ne doit être émis en v0 ;
- **aucun script d'arrosage** ne doit être piloté par ces futurs capteurs ;
- **aucun bouton d'action** ne doit être ajouté dans ce chantier ;
- **un seul point sec ne suffit jamais** à déclarer la zone sèche
  ([`14`](14_qualite_donnees_sol.md)).

---

## 5. Classes candidates futures (vocabulaire, **NON émis en v0**)

Vocabulaire de la **future** couche recommandation, documenté pour cohérence
amont — **aucune** n'est un état runtime v0 :

`DONNEES_INSUFFISANTES` · `HUMIDE` · `CONFORT` · `A_SURVEILLER` ·
`BESOIN_MODERE` · `BESOIN_MARQUE` · `DIFFERE_PLUIE_PREVUE` ·
`ARROSAGE_DECONSEILLE` · `VERIFICATION_HUMAINE`.

> **Explicitement :**
> - ces classes **ne sont pas des états runtime v0** ;
> - ces classes **ne sont pas des seuils** ;
> - ces classes **ne déclenchent rien** ;
> - elles **préparent seulement** la future couche recommandation.

---

## 6. Ordre de livraison (trajectoire)

1. **v0 — observation + diagnostic** (ce chapeau + [`14`](14_qualite_donnees_sol.md)) :
   mesures, dérivés factuels du canal sol, qualité/confiance des données. **Aucune
   recommandation, aucune action.**
2. **Phase d'observation** instrumentée (plan non normatif, critères de sortie
   vers v0.5) — [`plan_observation_hydrique_v0`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md).
3. **v0.5 — recommandation diagnostique non actionnable** (perception pure, ne
   pilote rien) — *contrat futur, hors de ce lot*.
4. **Exécution** : reste **manuelle supervisée** ([`11`](11_mode_manuel_supervise.md)) ;
   tout **automatisme** demeure **très ultérieur et hors périmètre**, subordonné à
   la Phase 0 ([`07`](07_phase_0_terrain.md)).

---

## 7. Non-objectifs (hors périmètre de ce chantier)

- ❌ créer un capteur `besoin_hydrique` ou `recommandation_arrosage` ;
- ❌ créer un booléen `arrosage_recommande` ;
- ❌ décider des seuils ; corriger / calibrer le Point 2 ;
- ❌ faire de la **canicule** un déclencheur autonome ;
- ❌ faire d'un **seul point sec** un déclencheur de zone ;
- ❌ relier directement l'humidité sol à Rain Bird ;
- ❌ tout runtime / UI / helper / automation / script / template.

---

## Renvois

- Qualité des données sol (socle transverse) : [`14_qualite_donnees_sol.md`](14_qualite_donnees_sol.md)
- Capteurs humidité sol (3 points / 1 zone) : [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md)
- Besoin hydrique (perception, référence) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Observation & preuves : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Pré-requis runtime / Phase 0 : [`10_prerequis_runtime.md`](10_prerequis_runtime.md) · [`07_phase_0_terrain.md`](07_phase_0_terrain.md)
- Mode manuel supervisé : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Cadrage (conception, #99) : [`cadrage_besoin_hydrique_decision_arrosage.md`](../../audits/02_conception/arrosage/cadrage_besoin_hydrique_decision_arrosage.md)
- Confrontation des avis (conception, #100) : [`confrontation_avis_besoin_hydrique.md`](../../audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md)
- Plan d'observation v0 (non normatif) : [`plan_observation_hydrique_v0.md`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)
- Index du domaine : [`README.md`](README.md)
