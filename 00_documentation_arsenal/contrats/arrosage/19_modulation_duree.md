# CONTRAT ARSENAL — ARROSAGE
## 19 — Modulation bornée de la durée d'arrosage (P4)

**Version contrat :** v0.1
**Statut :** **Normatif — spécification P4 ; runtime NON livré.** Définit la
**fonction de modulation** de la **durée** d'un arrosage de la station 1 par des
**critères physiques** (réservoir sol, demande climatique), sa **composition**,
ses **invariants de sûreté** et ses **critères de validation**. **Contrat avant
runtime** : ce document **ne crée aucun** YAML, helper, entité, automation, script,
template ni checker. La **cible** de P4 est le **branchement effectif** de la durée
modulée au point unique du Run — **pas** une nouvelle phase d'observation à blanc
(la phase probatoire des canaux sol/climat est déjà acquise, cf. réveil de C11,
[`REGISTRE_CHANTIERS.md`](../../audits/REGISTRE_CHANTIERS.md) ; amendement du
cadrage §4.5, [`cadrage_modulation_duree_arrosage.md`](../../audits/02_conception/arrosage/cadrage_modulation_duree_arrosage.md) §4.5).

> **Positionnement.** Ce contrat **matérialise** la cible doctrinale du cadrage C11
> ([`cadrage_modulation_duree_arrosage.md`](../../audits/02_conception/arrosage/cadrage_modulation_duree_arrosage.md)).
> Il traite **« combien de temps arroser »** — **jamais** « quand arroser », qui
> reste **intégralement** porté par la décision V1 ([`17`](17_decision_v1.md),
> inchangé). La modulation **n'ajoute aucune autorité de décision** et **ne peut
> pas** transformer un besoin d'arrosage positif en absence d'exécution.

> **Garde-fou de lecture.** Une zone Rain Bird, une station. La modulation **part
> de** la durée de base opérateur, **ne la remplace jamais**, et reste **bornée,
> traçable, neutralisable et désactivable**. **Aucune valeur de borne de modulation
> n'est inventée** dans ce contrat : les bornes numériques sont établies par
> **exploitation des données disponibles** puis **preuve runtime** (§6, §12).

---

## 1. Objet

Décrire la **fonction** qui transforme la **durée nominale** (réglage opérateur)
en **durée applicable** par une **modulation bornée** issue de deux canaux
physiques déjà livrés et observés, puis la façon dont le **Run** la **fige** et
l'applique. La modulation sert la finalité **F1/optimisation de l'eau**
([`01_metier.md`](01_metier.md)) : arroser **juste assez**, sans jamais priver le
jardin d'eau sur un doute.

---

## 2. Place dans les couches (séparation stricte)

| Couche | Contenu | Statut |
|---|---|---|
| **Observation** (factuel) | médiane / minimum / hétérogénéité / points frais / état réservoir sol ([`15`](15_canal_reservoir_sol.md)) ; ET₀ / VPD / état demande climatique ([`16`](16_canal_demande_climatique.md)) ; `sensor.arrosage_dernier_effectif` | **livré** — la modulation **n'en fait pas partie** |
| **Recommandation** (par canal) | qualification, **motif** et **facteur recommandé** de chaque canal, ou son **abstention explicite** | **P4** |
| **Décision** (composition) | règle d'arbitrage produisant la **durée applicable** unique + **motif dominant / synthèse** | **P4** |
| **Exécution** | le **Run** ([`11`](11_mode_manuel_supervise.md)) **fige (snapshot)** la durée applicable au démarrage et l'applique au **point unique** ; autorité de fin = `input_datetime.arrosage_session_fin_prevue` | Run existant |

> **Élaborer un facteur ou une durée recommandée est une opération métier /
> décisionnelle, pas une observation.** Aucun artefact runtime de P4 ne doit être
> qualifié de « couche observation ». Le contrat fixe ces **rôles** sans préjuger
> de la **nature exacte** des futures entités (template, attributs, helper) —
> décidée à l'implémentation, noms conceptuels `‹…›` jusque-là
> ([`README.md`](README.md) « noms conceptuels non figés »).

---

## 3. Grandeur modulée, unité, point d'insertion

- **Grandeur modulée** : la **durée d'arrosage de la station 1**, en **minutes
  entières**.
- **Point d'insertion UNIQUE** : la durée consommée par le Run
  (`script.arrosage_rain_bird_station_1_courte_supervisee`, variable `duree_minutes`).
  La durée modulée s'y substitue et **propage sans divergence** vers l'état de
  session, l'échéance `arrosage_session_fin_prevue` et la durée native. **Aucune
  écriture ailleurs**, **aucun second point** de réglage.
- **Autorité de fin** : **inchangée** — `input_datetime.arrosage_session_fin_prevue`
  (posée au démarrage, appliquée par l'automation de fin `10270000000006`,
  [`11`](11_mode_manuel_supervise.md)). La durée native reste un **dead-man
  présumé**, jamais l'autorité de fin.

---

## 4. Durée nominale de référence

- **Base** : `input_number.arrosage_rainbird_station_1_duree_minutes` (réglage
  **opérateur**, borné `[1,60]`, [`17`](17_decision_v1.md) §5).
- La modulation **part de** cette base et **ne l'écrit jamais** : le helper reste
  **à écrivain unique opérateur** (aucun double-writer). La base demeure la
  **référence** ; la modulation est une **surcouche** désactivable.

---

## 5. Modèle de composition (M4 — précédence d'abstention + composition ordonnée multiplicative)

### 5.1 Qualification et abstention, par canal

Chaque canal expose **séparément** : (a) son **statut de qualification** ;
(b) son **motif** ; (c) son **facteur recommandé** lorsqu'il est **qualifié** ;
(d) son **abstention explicite** lorsqu'il ne l'est pas.

Un canal **s'abstient** dès qu'une donnée dont il dépend est **absente**,
**indisponible**, **insuffisamment fraîche**, **dégradée** ou **non qualifiée**
(réservoir sol `insuffisant`/`indisponible`, ou climat sans ET₀/VPD frais —
[`15`](15_canal_reservoir_sol.md) §5, [`16`](16_canal_demande_climatique.md) §6).

> **Abstention ≠ observation remplacée par 1,0.** Le contrat distingue deux plans :
> - **résultat métier** : `abstention` (le canal **ne recommande rien**, motif et
>   disponibilité exposés) ;
> - **conséquence dans la composition** : **aucune modification de la durée
>   entrante**, soit l'**élément multiplicatif neutre** (facteur `1,0`) **par
>   construction**.
>
> Le `1,0` n'est **jamais** une valeur factuelle inventée ni une donnée hydrique /
> climatique fabriquée : c'est la **traduction formelle** d'une abstention. **Aucune
> réduction ne peut provenir d'un canal abstenu, dégradé ou non qualifié.**

### 5.2 Ordre de composition

```
durée nominale (base opérateur)
   × facteur_sol      (canal réservoir sol — PRIMAIRE)
   × facteur_climat   (canal demande climatique — SECONDAIRE)
   → arrondi final (§7)
   → clamp absolu [1,60] (§6)
   = durée applicable
```

L'ordre est **fixe** : sol **puis** climat. Chaque facteur est **borné, exposé et
neutralisable indépendamment**. Le produit est une **composition ordonnée à
contributions séparées**, **non** un score composite opaque (§9, [`13`](13_observation_hydrique_jardin.md) §1.6).

### 5.3 Rôle du canal sol (primaire)

Sur un signal **fiable et explicitement qualifié**, `facteur_sol` peut :
- **réduire** la durée (`facteur_sol < 1`) lorsque le réservoir sol est
  **amplement satisfait** (recommandation fiable et qualifiée) ;
- rester **neutre** (`facteur_sol = 1`) — y compris par **abstention** (§5.1) ;
- **allonger** la durée (`facteur_sol > 1`) lorsqu'un **déficit fiable** le justifie.

### 5.4 Rôle du canal climatique (secondaire)

`facteur_climat` exprime une **demande supplémentaire** et peut :
- rester **neutre** (`facteur_climat = 1`) — y compris par **abstention** ;
- **allonger réellement** la durée (`facteur_climat > 1`) sous **forte demande
  évaporative qualifiée** (ET₀/VPD) — **facteur initial `1,05`** (§6) ;
- **jamais réduire** la durée à lui seul (`facteur_climat ≥ 1`, invariant §6).

Un canal climatique **non pleinement qualifié** (`degrade`, `indisponible`,
indéterminé, ou ET₀/VPD non exploitables) **n'allonge pas** et **interdit toute
réduction** : la durée reste la **durée nominale** (protection). Une lecture
climatique **absente ou dégradée n'est jamais** interprétée comme favorable à une
réduction.

### 5.5 Composition et plancher nominal (couche décision)

La composition est `nominale × facteur_sol × facteur_climat`, avec un **plancher
à la durée nominale sous forte demande** :
- **forte demande qualifiée** (`facteur_climat = 1,05`) :
  `produit = base × facteur_sol × 1,05` ; **`durée_avant_arrondi = max(base,
  produit)`** — une réduction sol combinée à l'allongement climatique **ne
  descend jamais sous la base** ;
- **demande faible/normale qualifiée** (`facteur_climat = 1`) :
  `durée_avant_arrondi = base × facteur_sol` (la réduction sol s'applique) ;
- **climat non qualifié** : `durée_avant_arrondi = base` (protection, sans
  réduction).

Puis **arrondi** (§7) et **clamp `[1,60]`** (§6). `facteur_theorique` (produit des
recommandations, p. ex. `0,95 × 1,05 = 0,9975`) et `facteur_applique` (après
plancher, p. ex. `1,0`) sont **exposés distinctement** (§10). Le **motif global**
distingue au minimum :
- **`reduction_sol`** — réduction sol appliquée (climat normal) ;
- **`allongement_climatique`** — allongement réel (climat fort, sol non réducteur) ;
- **`compensation_sol_climat`** — réduction sol et allongement climatique se
  compensent, durée ramenée au **plancher nominal** ;
- **`climat_non_qualifie_plancher_nominal`** — climat non qualifié, durée nominale
  par protection.

---

## 6. Bornes (invariants de sûreté vs calibration)

**Contractuel (non réglable depuis l'UI) :**
1. **Clamp absolu** de la durée applicable à **`[1, 60]`** minutes. Cette borne
   n'est **pas** une vérité agronomique ou métier intemporelle : c'est l'**enveloppe
   absolue actuellement autorisée** par le **helper de durée**
   (`input_number.arrosage_rainbird_station_1_duree_minutes`, `[1,60]`) et le
   **wrapper d'exécution** ([`11`](11_mode_manuel_supervise.md),
   [`17`](17_decision_v1.md) §5). P4 la **conserve** et la rend **opposable à
   l'implémentation actuelle** ; elle **n'évolue que par modification contractuelle
   coordonnée** avec l'enveloppe d'exécution (helper + wrapper), jamais
   unilatéralement. Le **plancher `1`** garantit **actuellement** qu'une modulation
   de durée **ne supprime pas** une exécution déjà autorisée (§5.3 ne peut produire
   `0`).
2. **`facteur_climat ≥ 1`** : le canal climatique ne réduit **jamais** seul.
3. **Aucune réduction** (`facteur < 1`) depuis un canal **abstenu, dégradé, non
   frais ou non qualifié** — la réduction est réservée à un signal **sol fiable et
   qualifié** (§5.1, §5.3).
3bis. **Plancher nominal sous forte demande & protection (opposable).** Sous
   **forte demande climatique qualifiée**, la durée finale **ne descend jamais
   sous la base** : `durée_avant_arrondi = max(base, base × facteur_sol × 1,05)`.
   Un canal climatique **`degrade`, `indisponible`, indéterminé, ou ET₀/VPD
   `unknown`/`unavailable`** ⇒ **durée = base** (aucune réduction, aucun
   allongement). Un canal climatique **incomplet** n'est **jamais** lu comme
   favorable à la réduction (§5.4, §5.5).
4. **Domaine admissible borné** : `facteur_sol ∈ [f_sol_min, f_sol_max]` avec
   `f_sol_min > 0` (plancher de réduction **strictement positif**) et
   `facteur_climat ∈ [1, f_climat_max]`. L'existence de ces bornes est
   **contractuelle** ; **leurs valeurs ne le sont pas** (ci-dessous).

**Calibration (valeurs — établies par preuve, jamais inventées ici) :**
- Les **amplitudes** (`f_sol_min`, `f_sol_max`, `f_climat_max`) et les **seuils
  internes** de qualification (p. ex. le seuil « sol amplement satisfait » ouvrant
  la réduction) sont établis par **exploitation documentée des données
  disponibles** (historique sol/climat ~1 mois : distribution de la médiane au
  déclenchement, dose-réponse 35 min montrant un **sur-arrosage récurrent** —
  pic 36–51 % ≫ seuil 30 %, séchage ≈ −3,3 pt/j VPD-dépendant), **puis confirmés
  par preuve runtime** sur la modulation branchée (§12).
- **Forte demande climatique — facteur d'allongement et seuils (§5.4/§5.5)** —
  **calibration initiale réversible**, **non** des vérités agronomiques
  définitives : **facteur `1,05`** (allongement **réel**) déclenché à
  **ET₀ ≥ 6,0 mm·j⁻¹** **OU** **VPD ≥ 2,3 kPa** (≈ **quartile supérieur** des
  distributions réellement observées, ~1 mois). Sous forte demande, le **plancher
  nominal** (§5.5) garantit que la durée ne descend jamais sous la base.
  **Recalibrables** après validation runtime. Implémentés en **constantes nommées
  et commentées** dans le runtime — **pas de helper**, pas de réglage UI.
- S'ils sont exposés en helpers, ce n'est **qu'à l'intérieur** du domaine
  admissible borné (1), et **seulement si** leur utilité et leur autorité sont
  établies (arbitrage propriétaire). **Aucune valeur numérique n'est fixée par ce
  contrat.**

---

## 7. Arrondi

- La composition (§5) est calculée en **réel** ; l'**arrondi est final**, appliqué
  **après** toutes les règles métier (facteurs sol puis climat), **avant** le clamp
  absolu (§6.1).
- **Au plus proche.** L'égalité exacte à `0,5` est tranchée **à l'entier pair**
  (arrondi « bancaire », **biais statistiquement nul**). Un arrondi systématique
  **vers le haut** est **proscrit** : il introduirait un **biais permanent de
  sur-arrosage** contraire à la finalité d'optimisation.

> **Vérification obligatoire à l'implémentation.** Cette convention (au plus proche,
> égalité `0,5` → **entier pair**, **clamp après arrondi**) doit faire l'objet de
> **cas de test explicites**, en particulier sur les valeurs `x,5` (p. ex. `2,5 → 2`,
> `3,5 → 4`). Elle **ne doit pas** être supposée implicitement à partir du
> comportement d'un filtre (p. ex. `round` de Jinja, dont la règle d'égalité peut
> différer) : le comportement attendu est **spécifié ici** et **prouvé par test**.

---

## 8. Idempotence, stabilité, snapshot

- La durée applicable est une **fonction pure et déterministe** des entrées à
  l'instant du calcul.
- **Snapshot unique** : la durée est **figée une seule fois au démarrage du Run**
  (là où `duree_minutes` est aujourd'hui lue). Les changements d'observation
  **pendant** le cycle **ne modifient ni `arrosage_session_fin_prevue` ni la durée
  native** du Run en cours.
- Deux évaluations sur les mêmes entrées donnent la **même** durée (stabilité,
  aucun battement intra-cycle).

---

## 9. Séparation calcul / autorisation / exécution — invariants opposables

1. La modulation agit **uniquement** sur **« combien de temps »** ; elle **ne
   touche jamais** la décision **« quand »** ([`17`](17_decision_v1.md) inchangé) et
   **n'ajoute aucune autorité** de déclenchement.
2. **Point d'insertion unique** (§3) ; **aucun double-writer** ; la base opérateur
   (§4) n'est jamais écrite par la modulation.
3. **Aucune fusion opaque** : le **facteur composé** peut être calculé **à titre
   explicatif**, mais il **ne doit pas** être l'**unique** sortie observable ni
   **masquer** les contributions intermédiaires (§10, [`13`](13_observation_hydrique_jardin.md) §1.6).
4. **Désactivable** : un interrupteur ramène **exactement** à la durée de base
   (§4) ; **indisponibilité de la modulation ⇒ durée de base** (retour déterministe).
5. La modulation **ne réduit jamais** l'exécution à néant (plancher `1`, §6.1).

---

## 10. Observabilité (anti-fusion — minimum traçable)

La restitution doit permettre de **retrouver au minimum**, sans reconstruction :

1. la **durée nominale** (base) ;
2. le **statut** et le **facteur** du canal **sol** ;
3. la **durée après contribution sol** ;
4. le **statut** et le **facteur** du canal **climatique** ;
5. la **durée avant arrondi** ;
6. la **durée applicable finale** ;
7. le **motif dominant** ou la **synthèse explicative** ;
8. la **durée effectivement figée** par le Run (snapshot §8) ;
9. le **statut de demande climatique** (forte / faible ou normale / non
   qualifiée) et son motif ; `facteur_theorique` (produit des recommandations) vs
   `facteur_applique` (après plancher §5.5), rendant visibles l'**allongement
   climatique** et la **compensation** au plancher nominal.

Chaque canal expose en outre sa **disponibilité** et son **abstention** explicite
(§5.1). Le facteur composé (§9.3) est **optionnel et explicatif**, jamais
substitut des points 2–6.

---

## 11. Données `unknown` / `unavailable` — aucun fallback silencieux

- **Aucune donnée factuelle inventée** ; **aucune interprétation de l'absence**
  comme un état hydrique ou climatique réel.
- Une entrée absente / périmée / non qualifiée ⇒ **abstention explicite** du canal
  concerné (motif + disponibilité exposés, §5.1), **jamais** une valeur estimée.
- Conséquence de composition : **facteur neutre `1,0`** du canal abstenu (élément
  neutre, §5.1) — **jamais** une réduction.
- Si **tous** les canaux s'abstiennent : **durée applicable = durée de base**
  (aucune modulation), l'arrosage a lieu **à la durée nominale**.

---

## 12. Mise en service & validation runtime (pas d'observation à blanc)

> **Amendement doctrinal (2026-07-29).** L'exigence d'une **observation à blanc
> préalable** ([`cadrage_modulation_duree_arrosage.md`](../../audits/02_conception/arrosage/cadrage_modulation_duree_arrosage.md)
> §4.5, version antérieure) est **remplacée** : la phase probatoire des canaux
> sol/climat est **déjà acquise** (P2 réuni, réveil de C11). L'observabilité est
> **immédiate au branchement** (§10) et la validation se fait **en runtime après
> mise en service**. Aucune période indéterminée de calcul non appliqué.

**Séquence (hors de ce lot documentaire) :**
1. **Définir** la modulation (ce contrat) ;
2. **Implémenter** le calcul et son **observabilité** (§10) ;
3. **Brancher** réellement la durée calculée au **point unique** du Run (§3) ;
4. **Valider en runtime** ;
5. **Corriger / recalibrer** si les preuves runtime l'exigent (§6).

**La validation runtime (§4 de la séquence) doit couvrir :**
- un **Run réellement exécuté** avec une durée **différente** de la base ;
- la **cohérence** entre durée calculée, **snapshot** du Run,
  `arrosage_session_fin_prevue` et durée native ;
- le **retour exact à la durée nominale** lorsque la modulation **s'abstient** ou
  est **désactivée** ;
- l'**absence de modification** de la durée **pendant** un Run en cours (§8) ;
- le **respect des bornes** (§6) et de l'**autorité unique de fin** (§3).

Les **historiques existants** servent à **concevoir et tester** le modèle et à
établir un **domaine admissible conservateur** (§6) ; les **preuves manquantes**
(dose-réponse fiable, bornes définitives) sont obtenues **ensuite sur la modulation
réellement branchée**.

---

## 13. Critères de clôture P4

P4 est **clôturable** lorsque :
1. le présent contrat est **figé** et référencé (registre / index) ;
2. le calcul et l'observabilité (§10) sont **implémentés** ;
3. la durée modulée est **branchée** au point unique (§3) ;
4. la **validation runtime** (§12) est **acquise** sur les cinq points listés ;
5. le **domaine admissible** (§6) est **justifié** par les données puis **confirmé**
   en runtime, sans valeur inventée ;
6. la **désactivation** et l'**abstention** ramènent **exactement** à la base
   (preuve runtime).

---

## 14. Hors périmètre

- ❌ toucher la décision **« quand »** ([`17`](17_decision_v1.md)) ou ajouter une
  autorité de déclenchement ;
- ❌ **coefficient cultural (Kc)**, **ETc**, **dose** en millimètres → minutes
  ([`16`](16_canal_demande_climatique.md) §4/§8) ;
- ❌ **score composite opaque** / fusion destructrice des canaux ;
- ❌ **multi-zone**, **station 2** ;
- ❌ **fixer des valeurs de borne** de modulation dans ce contrat ;
- ❌ tout **runtime / UI / helper / automation / script / template / checker** dans
  ce lot documentaire.

---

## Renvois

- Cadrage du chantier C11 (cible doctrinale, prérequis) : [`cadrage_modulation_duree_arrosage.md`](../../audits/02_conception/arrosage/cadrage_modulation_duree_arrosage.md)
- Plan d'observation hydrique v0 (T04–T07, P2) : [`plan_observation_hydrique_v0.md`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)
- Décision V1 (« quand », base durée réutilisée) : [`17_decision_v1.md`](17_decision_v1.md)
- Mode manuel supervisé (Run, point d'insertion, autorité de fin) : [`11_mode_manuel_supervise.md`](11_mode_manuel_supervise.md)
- Besoin hydrique (garde anti-faux-négatif) : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Canal réservoir sol (primaire) : [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)
- Canal demande climatique (secondaire, ET₀/VPD) : [`16_canal_demande_climatique.md`](16_canal_demande_climatique.md)
- Chapeau observation hydrique (canaux non fondus) : [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md)
- Recommandation / motif dominant (précédent) : [`../aeration_recommandation.md`](../aeration_recommandation.md)
- Finalité métier (optimiser l'eau, F1) : [`01_metier.md`](01_metier.md)
- Index du domaine : [`README.md`](README.md)
