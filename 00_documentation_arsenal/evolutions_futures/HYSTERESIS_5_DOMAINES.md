# VÉRIFICATION DES BOUCLES D'HYSTÉRÉSIS — 5 DOMAINES

> Confrontation runtime du dépôt cloné. Le runtime fait foi.
> Climatisation : analysée **après** le correctif D8 (`temp_min <= seuil_off`).

## Constat central (à lire en premier)

La consigne suppose que les 5 domaines partagent une même structure : seuil ON,
seuil OFF, capteur ON, capteur OFF, capteur de besoin. **Le runtime ne valide cette
hypothèse que pour 2 domaines sur 5.**

| Domaine | Vraie hystérésis à 2 seuils ? | Structure réelle |
|---|---|---|
| Chauffage | **Non** | Système **modulant** (consigne + courbe de chauffe + plateaux). Le bang-bang est délégué aux vannes thermostatiques (matériel) et à la chaudière. Aucune boucle ON/OFF au niveau Arsenal. |
| Climatisation (cool) | **Oui** | Hystérésis à 2 seuils + maintien en bande morte. Correcte après le fix. |
| Déshumidification | **Oui** | Hystérésis à 2 seuils par critère (RH + HA), avec mémoire d'état. Correcte si bien configurée. |
| Aération | **Non** | Comparateur **sans mémoire**, **seuil unique** par critère. Les helpers `aeration_hysteresis_*` sont déclaratifs et **non câblés**. |
| VMC | **Non** | Front ON instantané (seuil ON seul) + **verrou temporel** (≥15 min) dans l'automation. `vmc_seuil_off` est **un paramètre mort**. |

La consigne s'applique donc pleinement à 2 domaines, partiellement aux 3 autres —
et cette inadéquation **est elle-même un résultat d'audit**.

---

# 1. CHAUFFAGE

## Identification
- **Seuil ON / OFF** : aucun seuil binaire Arsenal. Le domaine produit une *consigne*
  (`sensor.temperature_consigne_appliquee_locale`) modulée par la courbe de chauffe et
  les plateaux thermostatiques.
- **Capteur ON / OFF** : inexistants. Le seul binaire du domaine est
  `binary_sensor.chauffage_inhibition_geofencing_requise` (une **inhibition**, pas une
  demande de chauffe).
- **Capteur de besoin** : inexistant au niveau Arsenal.

## Verdict
La grille ON/OFF **ne s'applique pas**. L'hystérésis réelle vit **dans les vannes
thermostatiques** (chaque TRV régule sa pièce) et dans la chaudière — hors du périmètre
logiciel Arsenal. Arsenal pilote une *cible* continue, pas un état binaire.

- Chemin vers ON / OFF : porté par le matériel (TRV/chaudière), non observable ici.
- Blocage / maintien éternel / oscillation / contradiction : **non évaluables au niveau
  Arsenal** ; relèvent de la régulation matérielle.

> Recommandation d'audit : ne pas chercher à plaquer une hystérésis binaire sur le
> chauffage. Si une supervision de l'oscillation est souhaitée, elle existe déjà sous
> forme **diagnostique** (`diagnostic_thermique/cycles/nombre_cycles_par_jour`,
> `amplitude_oscillation_cycle`) — ce sont des observateurs, pas des décideurs.

---

# 2. CLIMATISATION (mode COOL — boucle canonique)

> Les modes DRY et HEAT sont des boucles sœurs du même domaine (voir §2 bis).

## Identification
- **Seuil ON** : `sensor.seuil_allumage_clim_applique` (« déclenchement »).
- **Seuil OFF** : `sensor.seuil_extinction_clim_applique` (« extinction »).
- **Invariant** : `seuil_ON > seuil_OFF` (garanti par `parametres_invalides_climatisation`).
- **Capteur ON** : `binary_sensor.clim_seuil_allumage_cool_atteint` = `temp_max >= seuil_ON`.
- **Capteur OFF** : `binary_sensor.clim_seuil_extinction_cool_atteint` = `temp_min <= seuil_OFF` *(post-fix)*.
- **Capteur de besoin** : `binary_sensor.besoin_clim_cool` = `si ON→true ; sinon si OFF→false ; sinon maintien`.
- **Décision** : `sensor.clim_target_mode` → `cool` si admissible.

Particularité : le front ON lit `temp_max` (pièce la plus chaude), le front OFF lit
`temp_min` (pièce la plus froide).

## Table de vérité (maison homogène, T = temp_max = temp_min)

| Scénario | Capteur ON | Capteur OFF | Besoin | Décision |
|---|---|---|---|---|
| A. T > seuil_ON | on | off | **on** | cool |
| B. seuil_OFF < T < seuil_ON | off | off | **maintien** (état précédent) | inchangée |
| C. T = seuil_ON | on (≥ inclusif) | off | **on** | cool |
| D. T = seuil_OFF | off | on (≤ inclusif) | **off** | off |
| E. T < seuil_OFF | off | on | **off** | off |

## Vérifications
- **Chemin vers ON** : A, C (toujours atteignable dès que la pièce chaude ≥ seuil_ON). ✅
- **Chemin vers OFF** : D, E (atteignable dès que la pièce froide ≤ seuil_OFF). ✅
- **Bande morte** : B → maintien propre, pas de battement. ✅
- **Égalités** : bornes ON (`>=`) et OFF (`<=`) inclusives ; comme `seuil_ON > seuil_OFF`,
  elles sont **mutuellement exclusives** pour T homogène → pas de double-vrai.
- **Spread (max ≠ min)** : ON et OFF peuvent être vrais simultanément si l'écart entre
  pièces ≥ (seuil_ON − seuil_OFF) ; le besoin donne **priorité à ON** → comportement
  protecteur, **pas de contradiction**.
- Maintien éternel / oscillation / blocage : **aucun** (post-fix). *(Avant le fix : OFF
  jamais atteignable → maintien éternel = bug D8, désormais corrigé.)*

**Verdict : boucle cohérente et complète.** ✅

## 2 bis. Boucles sœurs du même domaine
- **HEAT** : ON `temp_min < seuil_ON` ; OFF `temp_min >= seuil_OFF` ; `seuil_OFF > seuil_ON`
  (consigne ± offsets). Même capteur (`temp_min`) aux deux fronts → bande morte propre. ✅
- **DRY** : ON `humidex > seuil` ; OFF `humidex < (seuil − 1)`. **Bande morte de 1 unité
  codée en dur** (un seul seuil + offset fixe). Fonctionne, mais le deadband n'est pas
  paramétrable et n'a pas de seuil OFF dédié — dette mineure de lisibilité.

---

# 3. DÉSHUMIDIFICATION (déshumidificateur cave)

## Identification
Deux critères à hystérésis, agrégés par OU.

- **Critère RH** (`binary_sensor.critere_deshumidification_cave`) :
  - Seuil ON : `input_number.cave_rh_cible_on` · Seuil OFF : `input_number.cave_rh_cible_off`.
  - Logique : `si état=on → reste on tant que rh > seuil_OFF` ; `si état=off → passe on si rh >= seuil_ON`.
- **Critère HA** (`binary_sensor.critere_deshumidification_ha_cave`) : structure identique
  sur `sensor.humidite_absolue_cave` et seuils `…_cible_on/off_cave` (dérivés).
- **Capteur ON/OFF** : **portés par chaque critère** (mémoire d'état interne `this.state`).
- **Capteur de besoin** : `binary_sensor.deshumidificateur_cave_demarrage_recommande`
  = `critère_RH on OU critère_HA on` (agrégation pure, maintien si entrée invalide).
- **Invariant requis** : `seuil_ON > seuil_OFF`. Vérifié par
  `integrite_reglages/deshumidificateur.yaml` (diagnostic).

## Table de vérité — critère RH (config valide, ex. ON=75, OFF=70)

| Scénario | Si état=off | Si état=on | Besoin résultant |
|---|---|---|---|
| A. rh > ON (80) | on (80≥75) | on (80>70) | **on** |
| B. OFF < rh < ON (72) | off (72<75) | on (72>70) | **maintien** |
| C. rh = ON (75) | on (75≥75) | on | **on** |
| D. rh = OFF (70) | off | off (70>70 faux) | **off** |
| E. rh < OFF (65) | off | off | **off** |

## Vérifications
- Chemin vers ON (A, C) et vers OFF (D, E) : présents. ✅
- Bande morte B : maintien via `this.state`. ✅
- Égalités : ON inclusif (`>=`), OFF exclusif (`>`) → bornes nettes, pas de double-vrai. ✅

## ⚠️ Risque théorique : défauts de seuils inversés

- `cave_rh_cible_on` ∈ [60–85] sans `initial`.
- `cave_rh_cible_off` ∈ [65–80] sans `initial`.
- Les plages se chevauchent et n'empêchent donc pas une configuration incohérente (`OFF ≥ ON`).

Selon le mode de création ou de restauration des helpers, les valeurs minimales
pourraient être utilisées :

- ON = 60
- OFF = 65

ce qui inverserait l'hystérésis et pourrait provoquer une oscillation logique du critère.

Cependant, la confrontation runtime du système réel montre :

- `cave_rh_cible_on = 78`
- `cave_rh_cible_off = 73`
- `binary_sensor.parametres_invalides_deshumidificateur = off`

Le risque n'est donc pas actif sur l'installation auditée.

L'intégrité des paramètres détecte déjà toute configuration incohérente (`ON ≤ OFF`).

**Verdict :**
Aucun problème fonctionnel observé. Dette de robustesse potentielle lors d'une création ou réinitialisation des helpers, mais pas incident runtime.

---

# 4. AÉRATION

## Identification
- **Seuil ON** : `ha_min` ET `dt_min` (saisonniers, modulés nuit/pluie/grand-froid),
  via les `input_number.aeration_delta_ha_min_*` / `delta_t_min_*`.
- **Seuil OFF** : **inexistant.** Aucun second seuil. Les helpers
  `aeration_hysteresis_ha` / `aeration_hysteresis_t` existent mais leur propre contrat
  les déclare « **non utilisés par le moteur** » et interdit de « supposer une hystérésis
  active ».
- **Capteur ON / OFF** : un **seul** comparateur `binary_sensor.aeration_preferable_etage`
  (et `…_rdc`), **sans mémoire d'état** (`this.state` absent de l'expression).
- **Capteur de besoin** : `binary_sensor.aeration_conseillee` = `rdc on OU etage on`.
- Logique (hors overrides) : ON ⇔ `(int_abs − ext_abs) ≥ ha_min` **ET** `(t_in − t_out) ≥ dt_min`
  **ET** pas de pluie. Overrides : `co2 ≥ co2_fort` force ON ; canicule force OFF si CO₂ bas.

## Table de vérité (axe ΔHA, dt satisfait, sans pluie/CO₂/canicule)

| Scénario | État ON | État OFF | Besoin | Remarque |
|---|---|---|---|---|
| A. ΔHA > ha_min | on | — | **on** | |
| B. « entre ON et OFF » | **n/a** | **n/a** | — | **pas de bande morte : OFF = ¬ON** |
| C. ΔHA = ha_min | on (`>=`) | — | **on** | borne inclusive |
| D. « = seuil OFF » | **n/a** | — | — | aucun seuil OFF |
| E. ΔHA < ha_min | off | on | **off** | |

## Vérifications
- Chemin vers ON (A, C) et vers OFF (E) : présents. ✅
- **Bande morte : absente.** Frontière unique à `ha_min` (resp. `dt_min`).
- **Oscillation : OUI possible.** Avec du bruit de capteur autour de `ha_min`/`dt_min`,
  la recommandation **bascule on/off sans amortissement**. C'est le mode de défaillance
  que la consigne demandait de traquer — il est **réel** ici.
- Maintien éternel : non (capteur sans mémoire → pas de verrou d'état). ✅
- Contradiction : les overrides sont hiérarchisés (CO₂ fort > canicule > seuils) → pas de
  contradiction *logique*, mais le **seuil unique** reste le défaut structurel.

**Verdict : ce n'est pas une boucle d'hystérésis. Comparateur instantané à seuil unique →
risque d'oscillation. Les helpers d'hystérésis affichés sont morts (faux signal de
gouvernance).** ⚠️ *(L'oscillation peut être partiellement masquée en aval par le
mécanisme `tentative_en_grace` / l'automation d'application — à vérifier séparément si
ce domaine est mis au chantier, hors périmètre ici.)*

---

# 5. VMC

## Identification
- **Seuil ON** : `input_number.vmc_seuil_on` (HR, défaut 70 %) et
  `input_number.vmc_co2_seuil_on` (CO₂, défaut 1000 ppm).
- **Seuil OFF** : `input_number.vmc_seuil_off` / `vmc_co2_seuil_off` — **paramètres morts.**
  Lus uniquement par `integrite_reglages/vmc.yaml` (qui valide `ON > OFF`) et par les
  cartes UI. **Jamais consommés** par le capteur de décision ni par l'automation.
- **Capteur ON** : `binary_sensor.vmc_haute_vitesse_requise` — **instantané, sans mémoire** :
  ON ⇔ `(HR_pièce ≥ seuil_ON ET aération favorable) OU (CO₂ ≥ co2_ON)`.
- **Capteur OFF** : pas d'entité dédiée ; OFF = négation du capteur ON (mêmes seuils).
- **Capteur de besoin** : le même `vmc_haute_vitesse_requise`.
- **Maintien / libération** : `automation.vmc_gestion_auto` — applique la haute vitesse à
  ON, et à OFF **attend `vmc_duree_min_haute` (défaut 15 min)** avant de repasser en basse
  vitesse (mode `restart` : un nouveau ON annule la libération).

## Table de vérité (axe HR, aération favorable)

| Scénario | Capteur requis | Action automation |
|---|---|---|
| A. HR > seuil_ON | on | haute vitesse immédiate |
| B. « entre ON et OFF » | **n/a** | **pas de seuil OFF** → pas de bande morte de seuil |
| C. HR = seuil_ON | on (`>=`) | haute vitesse |
| D. « = seuil OFF » | **n/a** | seuil OFF ignoré par le moteur |
| E. HR < seuil_ON | off | basse vitesse **après 15 min** (si toujours off) |

## Vérifications
- Chemin vers ON (A, C) : immédiat. ✅
- Chemin vers OFF (E) : présent mais **temporisé** (≥15 min) — borné, pas éternel. ✅
- **Bande morte de seuil : absente** (un seul seuil). L'**anti-oscillation est temporelle** :
  le verrou de 15 min + `mode: restart` empêchent le ventilateur de battre physiquement.
  En revanche, le **capteur** `vmc_haute_vitesse_requise` peut, lui, scintiller au seuil
  (jitter UI), sans effet matériel grâce au verrou.
- Maintien éternel : non (libération bornée à 15 min après disparition de la demande). ✅
- **Contradiction de gouvernance : OUI.** `vmc_seuil_off` / `vmc_co2_seuil_off` sont
  réglables en UI, **validés** par l'`integrite` (`ON > OFF`), mais **n'ont aucun effet** :
  baisser le seuil OFF en espérant une libération plus tardive ne change rien.
  **Paramètre mort doté d'une validation active = faux sens de contrôle.**
- **Couplage** : la voie HR exige `aeration_preferable_etage` (favorable). Le jitter
  d'aération (§4) se propage donc à la voie humidité de la VMC. La voie CO₂ est indépendante.

**Verdict : pas d'hystérésis de seuil. Front ON instantané + verrou temporel de 15 min.
Anti-oscillation correcte au niveau matériel, mais seuils OFF morts (validés pourtant) et
couplage à l'aération.** ⚠️

---

# SYNTHÈSE TRANSVERSE

| Domaine | Hystérésis 2 seuils | Chemin ON | Chemin OFF | Blocage | Maintien éternel | Oscillation | Contradiction |
|---|---|---|---|---|---|---|---|
| **Chauffage** | non (modulant) | n/a Arsenal | n/a Arsenal | — | non | déléguée TRV | n/a |
| **Climatisation (cool)** | **oui** | ✅ | ✅ | non | non *(oui avant fix)* | non | non |
| **Déshumidification** | **oui** | ✅ | ✅ | non | non | **oui si mal configuré** | **oui au boot (défauts inversés)** |
| **Aération** | non (seuil unique) | ✅ | ✅ | non | non | **oui (pas de deadband)** | non |
| **VMC** | non (ON seul + verrou 15 min) | ✅ | ✅ (temporisé) | non | non | amortie *temporellement* ; capteur jitter | **oui (seuil OFF mort mais validé)** |

## Hiérarchie des risques
1. **Déshumidification — défauts de seuils inversés** (oscillation/contradiction dès le
   premier démarrage tant que `ON > OFF` n'est pas réglé). *Le plus concret.*
2. **VMC — seuils OFF morts mais validés** (faux contrôle ; gouvernance trompeuse).
3. **Aération — seuil unique sans deadband** (oscillation au seuil) + helpers d'hystérésis
   déclaratifs non câblés (dette de lisibilité).
4. **Climatisation** : sain après le fix D8.
5. **Chauffage** : hors grille (modulant) — ne pas forcer une hystérésis binaire.

> Aucune correction n'est proposée ici. Si tu veux ouvrir un chantier, l'ordre logique
> suit la hiérarchie ci-dessus ; chacun mérite d'abord sa propre confirmation runtime
> (notamment : grace timer d'aération en aval, et lecture effective de
> `vmc_duree_min_haute` vs `vmc_duree_haute_vitesse`).
