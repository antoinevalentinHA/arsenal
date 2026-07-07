# CONTRAT ARSENAL — ARROSAGE
## 16 — Canal demande climatique (observation v0)

**Version contrat :** v0.1
**Statut :** **Normatif — définit les grandeurs d'observation** du **canal demande
climatique (rapide)**. **Observation / diagnostic uniquement**, en deçà de toute
recommandation et de toute action. **Runtime d'observation LIVRÉ (lot P3,
PR #178/#215)** : `12_template_sensors/arrosage/demande_climatique.yaml` expose
ET₀, VPD et l'état qualitatif du canal, strictement en diagnostic — **non
branché** à aucune décision, recommandation, dose ou pilotage (frontière §7
inchangée). Ce document **spécifie** les grandeurs et leurs formules ; toute
évolution du runtime au-delà de l'observation (fusion, décision, action) reste
hors périmètre et nécessite un contrat dédié (cf. cadrage « modulation de
durée », registre C11).

> **Position dans le socle v0.** Ce contrat **dérive** du chapeau
> [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md) (canal
> §3.2) et **complète** le canal réservoir sol
> ([`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)) : là où le réservoir
> sol observe **ce qu'il reste** d'eau dans le sol (lent), la demande climatique
> observe **ce que le climat retire** (rapide). Il **matérialise le vocabulaire** du
> canal demande climatique, **sans** créer le runtime, **sans** décider la
> recommandation, **sans** choisir de seuil hydrique.

> **Garde-fou de lecture.** **Température = proxy de demande, jamais indicateur
> d'eau** ([`13`](13_observation_hydrique_jardin.md) §3.2). L'ET₀ est une **demande
> évaporative de référence**, **PAS** un besoin d'arrosage ni une **dose** : elle
> **décrit** un climat, elle ne **commande** rien.

---

## Objet

Définir, comme **cible d'observation v0**, les **grandeurs de la demande
climatique** que le runtime expose (lot P3 livré) : l'**évapotranspiration de référence
ET₀** (journalière) et le **déficit de pression de vapeur VPD** (courant), assorties
d'un **état qualitatif du canal**. Ces grandeurs sont **factuelles** ; elles
**n'émettent aucune recommandation** et **ne pilotent rien**.

Le **modèle est contraint par les capteurs réellement disponibles** (§1) :
l'**ET₀ Penman-Monteith complet (FAO-56) est exclu** faute de **vent** et de
**rayonnement solaire** mesurés. Le repli retenu — **Hargreaves-Samani** — n'utilise
que des grandeurs disponibles et un terme de rayonnement **calculé**, sans constante
inventée ([`06_observation_et_preuves.md`](06_observation_et_preuves.md) :
honnêteté d'observation).

---

## 1. Périmètre, dépendances & capteurs requis

- **Amont** : chapeau [`13`](13_observation_hydrique_jardin.md) (canaux, frontière
  v0, §3.2).
- **Complément** : canal réservoir sol [`15`](15_canal_reservoir_sol.md) (autre
  canal, **jamais fondu** en un indicateur unique en v0).
- **Aval (hors v0)** : la future couche **recommandation** (non émise) et la
  combinaison **demande − réserve − modulateurs** → besoin (futur, autre contrat).

**Capteurs / entrées requis** (rôles ; les `entity_id` ne sont pas figés par ce
contrat — convention [`15`](15_canal_reservoir_sol.md) §5) :

| Rôle | Disponibilité constatée | Usage |
|---|---|---|
| Température extérieure **moyenne** journalière (Tmean) | ✅ `sensor.temperature_exterieure_moyenne_jour` | ET₀ |
| Température extérieure **min / max** journalières (Tmin / Tmax) | ◐ à **lier au runtime** (capteur extérieur + min/max du jour ; palmarès journaliers existants) | ET₀ (terme d'amplitude) |
| **Humidité relative** extérieure courante (HR) | ✅ `sensor.humidite_relative_jardin` | VPD |
| Température extérieure **courante** | ✅ `sensor.temperature_jardin` | VPD |
| **Latitude** | ✅ attribut `zone.home` | radiation extraterrestre Ra (calcul) |
| **Quantième** (jour de l'année) | ✅ déterministe (date) | Ra (calcul) |

> **Tmin / Tmax — exigence opposable.** Le contrat **ne fige aucun `entity_id`
> runtime** (convention [`15`](15_canal_reservoir_sol.md) §5), mais **impose** que
> `Tmin` et `Tmax` soient **dérivées de données journalières fiables** : extrêmes
> **réels du jour** mesurés sur le capteur de température extérieure, ou capteurs
> d'extrêmes journaliers **qualifiés**. **À défaut de `Tmin`/`Tmax` fiables, l'ET₀
> n'est pas calculée** (§2, §6) — **aucune** valeur de repli n'est inventée.

> **Non requis** (et volontairement non utilisés) : anémomètre et pyranomètre
> (**absents** du parc) ; pression atmosphérique (inutile aux formules retenues).
> Aucune valeur de vent ou de rayonnement n'est **inventée** ni **modélisée par
> prévision** pour combler ces absences.

---

## 2. Formule retenue — ET₀ Hargreaves-Samani (journalière)

Repli FAO-56 standard lorsque seule la **température** est fiable ; l'amplitude
thermique `Tmax − Tmin` sert de **proxy du rayonnement et de la nébulosité**.

```
ET₀ = 0.0023 · (Tmean + 17.8) · (Tmax − Tmin)^0.5 · Ra
```

- `ET₀` en **mm·jour⁻¹** ; `Tmean`, `Tmax`, `Tmin` en **°C** ;
- `Ra` = **radiation extraterrestre**, exprimée en **mm·jour⁻¹** (évaporation
  équivalente).

**Radiation extraterrestre `Ra`** (FAO-56, calcul déterministe — aucun capteur) :

```
Ra(MJ·m⁻²·j⁻¹) = (1440/π) · Gsc · dr · [ ωs·sin(φ)·sin(δ) + cos(φ)·cos(δ)·sin(ωs) ]
Ra(mm·j⁻¹)     = 0.408 · Ra(MJ·m⁻²·j⁻¹)

Gsc = 0.0820 MJ·m⁻²·min⁻¹           (constante solaire)
dr  = 1 + 0.033·cos(2π·J/365)        (distance Terre–Soleil inverse)
δ   = 0.409·sin(2π·J/365 − 1.39)     (déclinaison solaire, rad)
ωs  = arccos( −tan(φ)·tan(δ) )       (angle horaire au coucher, rad)
φ   = latitude (rad, depuis zone.home) ;  J = quantième (1–365/366)
```

> **Garde de calcul (opposable).** L'ET₀ n'est **émise que si** `Tmean`, `Tmin`
> **et** `Tmax` sont **disponibles, fraîches et issues de données journalières
> fiables**. Si l'une **manque**, est **périmée** ou n'est **pas** une donnée
> journalière fiable, l'ET₀ est **indisponible** (état `degrade` ou `indisponible`,
> §6) — **jamais** une valeur estimée « au doigt mouillé », ni un repli arbitraire
> (p.ex. amplitude `Tmax − Tmin` forcée). **Pas d'entrée fiable → pas d'ET₀.**

---

## 3. Formule retenue — VPD courant (déficit de pression de vapeur)

Moteur **physique direct** de la demande évaporative, **instantané**, à partir des
capteurs température + HR extérieurs déjà présents (FAO-56 eq. 11/19) :

```
e°(T) = 0.6108 · exp[ 17.27·T / (T + 237.3) ]   (kPa)   — pression de vapeur saturante
ea     = e°(T) · HR/100                           (kPa)   — pression de vapeur réelle
VPD    = e°(T) − ea = e°(T) · (1 − HR/100)        (kPa)
```

- `T` = température extérieure **courante** (°C) ; `HR` = humidité relative
  extérieure **courante** (%).

---

## 4. Limites (honnêteté d'observation)

- **Hargreaves ≠ Penman-Monteith.** Estimation à partir de la seule température ;
  écart typique **±15–30 %** vs PM en conditions **ventées ou très humides** ;
  calibrée pour un **gazon de référence**. → **indicateur relatif** de demande,
  **jamais une dose** d'arrosage.
- **Ra = rayonnement de sommet d'atmosphère**, déterministe (latitude + quantième) :
  il **ne capte pas** la nébulosité réelle autrement que **via l'amplitude
  thermique** (`Tmax − Tmin`) — hypothèse **assumée** du modèle, pas un défaut
  masqué.
- **VPD courant = instantané** : moteur de la demande, **pas** une demande
  journalière intégrée. Complément de l'ET₀, **non** substitut.
- **ET₀ ≠ ETc ≠ besoin.** Aucun **coefficient cultural (Kc)**, aucun **sol**, aucune
  **pluie soustraite** : ce canal produit l'**ET₀ de référence** uniquement. La
  traduction en besoin relève d'un **contrat futur**.
- **Dépendance à la fraîcheur** des entrées (température / humidité extérieures) :
  sans `Tmin`/`Tmax` **fiables**, l'ET₀ **n'est pas produite** (indisponible),
  jamais estimée par repli (§2 garde de calcul, §6).

---

## 5. Grandeurs produites (cibles v0)

`entity_id` **non figés** (le contrat fixe ce qui doit être visible, pas comment —
[`15`](15_canal_reservoir_sol.md) §5) :

| Grandeur | Unité | Source |
|---|---|---|
| **ET₀ journalière** | mm·jour⁻¹ | Hargreaves-Samani (§2) |
| **VPD courant** | kPa | déficit de pression de vapeur (§3) |
| **État qualitatif du canal** | — | `complet` / `degrade` / `indisponible` (§6) |
| *(diagnostic, optionnel)* `Ra` du jour, fraîcheur des entrées | mm·j⁻¹ / — | attributs de transparence |

> Les grandeurs sont **exposées séparément** : l'ET₀ (journalière, lente à varier)
> et le VPD (courant, rapide) ne sont **jamais fondus** en un score unique
> ([`13`](13_observation_hydrique_jardin.md) §1.6).

---

## 6. État qualitatif du canal demande climatique

Vocabulaire candidat v0, **strictement diagnostic / observation** :

| État | Sens (lecture du canal, **pas** une décision) |
|---|---|
| `complet` | `Tmin`, `Tmax`, `Tmean` **et** HR extérieures **fraîches** → ET₀ **et** VPD calculés |
| `degrade` | une entrée **manque ou est périmée**. Si `Tmin`/`Tmax`/`Tmean` sont indisponibles ou non fiables, l'**ET₀ n'est PAS produite** (elle passe à **indisponible**) — **seul le VPD** reste exposé tant que température + HR **courantes** sont fraîches. Le canal **n'émet jamais une ET₀ de repli** : `degrade` signale une lecture **partielle**, pas une ET₀ « complète » fabriquée |
| `indisponible` | température / humidité extérieures **absentes ou périmées** → **aucune** grandeur fiable (ni ET₀, ni VPD) |

> **Ces états ne sont PAS des recommandations d'arrosage.** Ils ne signifient ni
> « arroser », ni « ne pas arroser » : ils **qualifient seulement la lecture** du
> canal demande climatique.

---

## 7. Frontière stricte (observation / diagnostic — opposable)

- le canal demande climatique fournit des **observations** (ET₀, VPD) et un
  **diagnostic** de lecture (§6) ;
- il **n'émet aucune recommandation** ; il **ne produit pas** `besoin_hydrique`,
  `arrosage_recommande`, ni aucune classe de [`13`](13_observation_hydrique_jardin.md) §5 ;
- il **ne pilote pas** Rain Bird ; il **ne crée aucun bouton** ni script ;
- l'ET₀ et le VPD **ne déclenchent rien** : **chaleur / canicule ne sont pas des
  déclencheurs** ([`13`](13_observation_hydrique_jardin.md) §3.2) ;
- il **n'est pas combiné** en v0 avec le réservoir sol pour produire un besoin
  (fusion **future**, autre contrat).

---

## 8. Non-objectifs (hors périmètre)

- ❌ ET₀ **Penman-Monteith complet** (exclu : ni vent ni rayonnement mesurés) ;
- ❌ **inventer** une valeur de vent ou de rayonnement, ou la dériver d'une
  **prévision** (`weather.*`) au cœur du calcul ;
- ❌ produire un **coefficient cultural (Kc)**, une **ETc**, un **besoin hydrique**
  ou une **dose** d'arrosage ;
- ❌ **soustraire la pluie** ou fondre demande + réserve en un score unique ;
- ❌ faire de la **canicule** / d'une **ET₀ élevée** un **déclencheur** ;
- ❌ relier directement la demande climatique à Rain Bird ;
- ❌ tout runtime / UI / helper / automation / script / template **dans ce document**.

---

## Renvois

- Chapeau observation hydrique (frontière v0, canaux, §3.2) : [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md)
- Canal réservoir sol (canal complémentaire) : [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)
- Besoin hydrique (perception, référence) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Observation & preuves (honnêteté d'observation) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Plan d'observation v0 (seuils exploratoires, non normatif) : [`plan_observation_hydrique_v0.md`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)
- Index du domaine : [`README.md`](README.md)
