# AUDIT — STRATÉGIE DE PILOTAGE COOL : « MAX POUR ON / MIN POUR OFF »
## Reconstruction factuelle de la chaîne de décision climatique estivale

> **Statut :** document d'audit **non normatif**.
> Il ne modifie aucun runtime, aucun contrat, aucune automatisation. Aucune
> correction n'est appliquée. Il décrit le système réel, le prouve, l'analyse,
> et conclut. Toute proposition d'évolution éventuelle est portée par un patch
> documentaire **séparé**.
>
> **Domaine :** `climatisation` · mode **COOL** (refroidissement estival)
> **Dépôt audité :** `antoinevalentinHA/arsenal` · commit **`ce24fb28`** · 2026-06-14
> **Méthode :** clone intégral, lecture du runtime YAML, des contrats, des
> capteurs, des automatisations réellement chargées, puis confrontation
> systématique contrat ↔ runtime. Aucune affirmation n'est posée sans preuve
> citée (chemin de fichier + extrait).

> ## ⚠️ STATUT DE RÉVISION — v2 (révise la conclusion de v1)
>
> Ce document a deux couches, **toutes deux conservées** :
>
> - **v1 (Phases 0 à 5)** — analyse à partir des **propriétés mathématiques de
>   l'hystérésis**. Factuellement exacte sur la chaîne de décision, mais reposant
>   sur une **hypothèse implicite non vérifiée** : que les trois chambres sont
>   **également contrôlables** par le climatiseur. Sous cette hypothèse, v1
>   désignait le critère `min`-pour-OFF comme « la moitié fragile » de la règle.
> - **v2 (Phase 6)** — **contre-analyse topologique** intégrant la réalité
>   physique : **un seul climatiseur sur le palier**, chambres ouvrables/fermables,
>   **aucun capteur de porte**, **mono-zone par contrat**. Cette couche **révise la
>   conclusion centrale de v1**.
>
> **Conclusion qui change :** la stratégie `max`-ON / `min`-OFF n'est **pas** une
> fragilité à corriger. C'est un **mécanisme de robustesse mono-zone** qui garantit
> l'**atteignabilité de l'état OFF** face à une chambre thermiquement découplée. Le
> critère `min`-OFF n'est donc **pas** à remplacer par `max`-OFF : ce dernier
> introduirait un mode de défaillance **pire** (acharnement climatique). Ce qui
> était présenté en v1 comme « fragilité du `min`-OFF » est reclassé en v2 comme
> **compromis assumé** (cf. Phase 6).
>
> **v1 n'est pas effacée** : elle est conservée comme *analyse partielle, avant
> prise en compte de la topologie*. Les sections v1 ci-dessous portent un rappel
> `[v1 — partiel]` là où la révision s'applique.

---

## 0. Réponse directe à la question posée  *(v1 — partiel ; voir Phase 6 pour la révision)*

L'observation du tableau de bord (« la chambre la plus chaude déclenche le
refroidissement, la chambre la plus froide autorise l'arrêt ») est **exacte**.
Elle est **prouvée par le runtime**, **documentée comme volontaire** dans les
contrats, et **garantie cohérente** (hystérésis `ON > OFF`) par le capteur
d'intégrité. Ce n'est donc pas un bug.

Mais l'audit met en évidence trois choses que le tableau de bord ne dit pas :

1. La justification écrite de cette asymétrie (« l'extinction attend que
   *l'ensemble* des zones redescendent sous le seuil ») **décrit l'inverse** de
   ce que `min` pour OFF produit réellement.
2. Le bénéfice anti-oscillation revendiqué **n'est vrai que pour une maison
   homogène**. Dès que l'écart inter-chambres dépasse l'hystérésis (≈ **1 °C**),
   la stratégie **dégénère** : court-cycle sur la chambre chaude **et**
   sur-refroidissement de la chambre froide.
3. Le système dispose déjà de toute l'instrumentation pour **mesurer** cet écart
   et trancher empiriquement (recorder + protocole d'observation existant).

Le détail, les preuves et les scénarios suivent.

> **Reformulation v2.** Les points 1 et 2 ci-dessus restent vrais *en régime
> entièrement couplé* (portes ouvertes). Mais la **Phase 6** montre que, sous la
> topologie réelle (clim unique sur le palier, portes fermables), l'asymétrie
> `max`/`min` est d'abord un **mécanisme de robustesse** : `min`-OFF garantit que
> l'arrêt reste **atteignable** via une pièce réellement contrôlée. Le « bénéfice
> anti-oscillation » est secondaire ; le bénéfice primaire est la **vivacité**
> (le système peut toujours revenir à OFF). Le point 3 (mesurer `Δ`) reste valide.

---

# PHASE 1 — ÉTAT EXACT DU SYSTÈME

## 1.1 Chaîne de décision COOL reconstruite (de bas en haut)

```
 [Perception]   sensor.temperature_chambre_arnaud
                sensor.temperature_chambre_matthieu      sensor.temperature_jardin
                sensor.temperature_chambre_parents
                        │                                        │
        ┌───────────────┴───────────────┐                        │
        ▼                               ▼                         │
 sensor.temperature_max_chambres   sensor.temperature_min_chambres│
   (la plus CHAUDE)                  (la plus FROIDE)             │
        │                               │                         │
        ▼ ≥                             ▼ ≤                        │
 sensor.seuil_allumage_clim_applique  sensor.seuil_extinction_clim_applique
   (présence ? presence : absence)     (présence ? presence : absence)
        │                               │                         │
        ▼                               ▼                         │
 binary_sensor.clim_seuil_          binary_sensor.clim_seuil_     │
   allumage_cool_atteint              extinction_cool_atteint     │
        │   (franchissement ON)        │   (franchissement OFF)   │
        └───────────────┬──────────────┘                         │
                        ▼                                         │
            binary_sensor.besoin_clim_cool                        │
              (hystérésis métier : ON prioritaire)                │
                        │                                         │
                        │        binary_sensor.autorisation_clim_cool ◄──┘
                        │          (ext° + aération + fenêtres +
                        │           horaire + absence prolongée)
                        ▼                  │
        input_boolean.besoin_clim_cool_admissible
          (automation « Admissibilité » : 2 portes causales)
                        │
                        ▼
              sensor.clim_target_mode   ──►  cool / dry / heat / off
                        │
                        ▼
        automation « Application automatique » (trigger_execution)
                        │
                        ▼
               script.clim_execution  ──►  climate.clim + switch.clim_power
                        ▲
              ┌─────────┴─────────┐
        Guard (INV-1/2/3)    Watchdog (incohérence ≥ persistante)
        Reprise après échec (timer.clim_retry, ≤ 2 tentatives)
```

## 1.2 Cartographie — pour chaque décision : capteur · fichier · logique · preuve

### Décision 1 — ALLUMAGE (ON) : indexé sur la chambre la plus CHAUDE

| Élément | Valeur |
|---|---|
| Capteur de franchissement | `binary_sensor.clim_seuil_allumage_cool_atteint` |
| Fichier | `12_template_sensors/climatisation/seuils_on_off/cool/seuil_allumage_cool_atteint.yaml` |
| Logique exacte | `temperature_max_chambres | float >= seuil_allumage_clim_applique | float` |
| Capteur source | `sensor.temperature_max_chambres` |
| Définition source | `12_template_sensors/meteo/mesures/temperature/chambres/max/global/valeur.yaml` |
| Agrégat | `max` des 3 chambres (Arnaud, Matthieu, Parents) — voir extrait ci-dessous |

> Preuve (max/global/valeur.yaml) :
> `{{ (valides | sort(attribute=1))[-1][1] }}` → dernier élément du tri croissant
> = **valeur la plus élevée**. Attribut `chambre_la_plus_chaude` confirmé.

### Décision 2 — EXTINCTION (OFF) : indexée sur la chambre la plus FROIDE

| Élément | Valeur |
|---|---|
| Capteur de franchissement | `binary_sensor.clim_seuil_extinction_cool_atteint` |
| Fichier | `12_template_sensors/climatisation/seuils_on_off/cool/seuil_extinction_cool_atteint.yaml` |
| Logique exacte | `temperature_min_chambres | float <= seuil_extinction_clim_applique | float` |
| Capteur source | `sensor.temperature_min_chambres` |
| Définition source | `12_template_sensors/meteo/mesures/temperature/chambres/min/valeur.yaml` |
| Agrégat | `min` des 3 chambres — `{{ (valides | sort(attribute=1))[0][1] }}` (premier du tri croissant) |

**→ L'observation est confirmée et prouvée : `max` pour ON, `min` pour OFF.**

### Décision 3 — SEUILS appliqués (contextuels présence/absence)

| Sortie | Fichier | Logique |
|---|---|---|
| `sensor.seuil_allumage_clim_applique` | `seuils_on_off/cool/on.yaml` | présence → `clim_seuil_declenchement_presence` ; sinon `…_absence` |
| `sensor.seuil_extinction_clim_applique` | `seuils_on_off/cool/off.yaml` | présence → `clim_seuil_extinction_presence` ; sinon `…_absence` |

**Valeurs runtime documentées** (acte opérateur tracé dans
`protocole_observation_seuils_cool.md`, même chantier) :
ON ≈ **24,5 °C** / OFF ≈ **23,5 °C** présence → **hystérésis de seuil = 1,0 °C**.

> ⚠️ Ces valeurs sont du *runtime state* (helpers `input_number`, stockés hors
> dépôt dans `.storage`). La valeur **figée dans le dépôt** est la plage
> autorisée (`presence ON ∈ [22,28]`, `OFF ∈ [20,26]`,
> `03_input_numbers/…`). Le 24,5 / 23,5 provient du protocole d'observation,
> source la plus autoritative présente au dépôt, mais reste modifiable en direct.

### Décision 4 — BESOIN (hystérésis métier)

| Élément | Valeur |
|---|---|
| Capteur | `binary_sensor.besoin_clim_cool` |
| Fichier | `12_template_sensors/climatisation/besoin/cool.yaml` |
| Logique | `si ON → true ; sinon si OFF → false ; sinon état courant (hold)` |
| Priorité | **ON l'emporte** si ON et OFF simultanément vrais (ordre `if/elif`) |
| Contrat | `contrats/climatisation/capteurs/besoins/10_besoins.md` (formule identique) |

### Décision 5 — MODE (cool / dry / heat / off)

| Élément | Valeur |
|---|---|
| Capteur | `sensor.clim_target_mode` |
| Fichier | `12_template_sensors/climatisation/decision/mode_target.yaml` |
| Logique | `cool` si `besoin_clim_cool_admissible` ; sinon `dry` ; sinon `heat` ; sinon `off` |
| Arbitrage | priorité fixe COOL > DRY > HEAT > OFF (ThermalPriorityPolicy v1) |

### Décision 6 — AUTORISATION (blocages transversaux)

| Élément | Valeur |
|---|---|
| Capteur | `binary_sensor.autorisation_clim_cool` |
| Fichier | `12_template_sensors/climatisation/autorisation/cool.yaml` |
| Conditions (toutes requises) | `temperature_jardin ≥ clim_seuil_temperature_exterieure_minimum` **ET** `clim_blocage_aeration_etage_reel == off` **ET** `fenetre_ouverte_maison_avec_delai == off` **ET** `clim_blocage_horaire_reel == off` **ET** `clim_extinction_absence_prolongee_autorisee == off` |

### Décision 7 — ADMISSIBILITÉ (2 portes causales)

| Élément | Valeur |
|---|---|
| Sortie | `input_boolean.besoin_clim_cool_admissible` |
| Fichier | `11_automations/climatisation/cool/admissibilite.yaml` (id `10030000000114`) |
| Porte 1 | front montant du **besoin** sous autorisation active |
| Porte 2 | requalification sur **autorisation stable 5 min** sous besoin actif |
| Extinctions | retombée du besoin **ou** révocation de l'autorisation (immédiates) |
| Contrat | `05_decision_candidats.md` (v1.4) |

### Décision 8 — PROTECTIONS ANTI-OSCILLATION (deux couches indépendantes)

| Couche | Mécanisme | Preuve |
|---|---|---|
| **Hystérésis de seuil** | `S_on > S_off` **imposé** | `12_template_sensors/system/integrite_reglages/climatisation.yaml` inv1/inv2 : `clim_seuil_declenchement_* > clim_seuil_extinction_*` |
| **Hystérésis d'état** | `hold` quand aucun franchissement actif | `besoin/cool.yaml` branche `{{ is_state(this.entity_id,'on') }}` |
| Stabilisation porte 2 | autorisation requalifiée seulement après **5 min** stables | `cool/admissibilite.yaml` `for: minutes: 5` |

### Décision 9 — REPRISES & SÉCURITÉS

| Rôle | Automatisation | Fichier | Action |
|---|---|---|---|
| Cohérence immédiate décision↔exécution | Guard `10030000000101` | `climatisation/guard.yaml` | INV-1/2/3 → `script.clim_exec_apply_off` |
| Incohérence persistante | Watchdog `10030000000106` | `climatisation/watchdog.yaml` | sur `clim_incoherence_decision_reel` → ré-exécution |
| Reprise après échec | `10030000000108` | `climatisation/reprise_apres_echec.yaml` | timer `clim_retry`, borne **≤ 2** tentatives |
| Transit décision→exécution | `10030000000105` | `climatisation/trigger_execution.yaml` | relais `clim_target_mode` → `script.clim_execution`, garde `systeme_stable` |

---

# PHASE 2 — COHÉRENCE ARCHITECTURALE

| Critère | Verdict | Justification (preuve dépôt) |
|---|---|---|
| Séparation Perception → Décision → Exécution | **Respectée** | Le besoin n'intègre aucune contrainte physique (`besoins/90_observations.md §5`) ; l'autorisation absorbe le monde ; le Guard ne lit aucune grandeur du monde. |
| Décision pure sans effet de bord | **Respectée** | `mode_target.yaml` / `raison.yaml` sont des capteurs templates sans action. |
| Idempotence d'exécution | **Respectée** | `trigger_execution` relaie vers un script idempotent ; Guard `mode: restart`. |
| Absence de deadlock thermique | **Respectée aujourd'hui** | Le backlog note que le contrat 05 « aucun deadlock » est redevenu vrai depuis le fix D8. |
| Documentation = runtime (formule) | **Respectée** | `20_binary_sensors_franchissement.md` cite littéralement `temp_max ≥ seuil` / `temp_min ≤ seuil`. |
| Documentation = runtime (**intention**) | **PARTIELLEMENT FAUSSE** | Voir Phase 3 §3.2 et Annexe A : la *justification* de l'asymétrie contredit le comportement réel de `min`-pour-OFF. |
| Absence d'oscillation | **Conditionnelle** | Garantie pour maison homogène ; non garantie en hétérogène (Phase 3). |
| Confort hygrométrique (DRY) | **Cohérent mais asymétrique vs COOL** | DRY = `max`/`max−1` (symétrique sur le même capteur) ; COOL = `max`/`min` (asymétrique). Deux philosophies d'agrégation coexistent. |

**Lecture critique.** L'architecture *de structure* est solide et exemplaire
(couches étanches, invariants CI, filets Guard/Watchdog/Reprise). Le point de
fragilité n'est **pas** structurel : il est dans la **sémantique de la règle
d'extinction COOL** et dans **l'écart entre son intention écrite et son effet
réel**. C'est un défaut d'explicabilité/conception, pas un défaut de plomberie.

> **[v1 — partiel]** Les deux lignes du tableau ci-dessus marquées « PARTIELLEMENT
> FAUSSE » et « Conditionnelle » reflètent le cadrage v1. La **Phase 6** les
> requalifie : l'« écart intention ↔ effet » est réel mais l'intention correcte
> n'est pas « attendre toutes les zones » — c'est l'**atteignabilité de OFF** sous
> topologie mono-zone ; et le caractère « conditionnel » de l'anti-oscillation
> devient un **compromis assumé**, non un défaut.

---

# PHASE 3 — ANALYSE DU CHOIX « MAX POUR ON / MIN POUR OFF »

## 3.1 Machine à états réelle (dérivation rigoureuse)

Soit `M = temperature_max_chambres`, `m = temperature_min_chambres`,
`S_on` (≈ 24,5), `S_off` (≈ 23,5), avec **`S_on > S_off`** garanti.
La machine `besoin_clim_cool` est :

```
→ ON   quand  M ≥ S_on
→ OFF  quand  (M < S_on)  ET  (m ≤ S_off)      ← le ON prioritaire masque le OFF
       sinon : hold
```

Le point clé est que `m ≤ S_off` **ne suffit pas** à éteindre : il faut **d'abord**
que la chambre la plus chaude soit redescendue sous `S_on`. L'extinction est donc
gouvernée par **deux conditions conjointes**, pas par la seule chambre froide.

Posons **Δ = M − m** (écart inter-chambres instantané, ≥ 0).
À l'instant de l'allumage : `M = S_on`, donc `m = S_on − Δ`.

- **Si Δ ≥ (S_on − S_off)** : alors `m = S_on − Δ ≤ S_off` **dès l'allumage**. La
  condition OFF est *déjà satisfaite* (masquée par la priorité ON). Conséquence :
  à la seconde où `M` repasse sous `S_on`, l'extinction se déclenche
  **immédiatement**. La bande morte effective sur la chambre chaude s'effondre à
  ≈ 0 → **court-cycle**.
- **Si Δ < (S_on − S_off)** : `m = S_on − Δ > S_off`. L'extinction exige que `m`
  descende jusqu'à `S_off`, donc un refroidissement *supplémentaire*. La bande
  morte est préservée → comportement stable.

**Or `S_on − S_off ≈ 1,0 °C`** (valeur documentée). Le seuil de bascule entre
les deux régimes est donc **un écart inter-chambres de 1 °C seulement**. En été,
portes fermées, orientations différentes, un écart ≥ 1 °C entre deux chambres est
**banal**. Le régime dégénéré n'est donc pas un cas d'école : c'est probablement
le **cas nominal estival**.

## 3.2 Les deux effets de bord (même cause : l'écart Δ)

**Effet A — sur-refroidissement de la chambre froide.**
Tant que `M ≥ S_on`, le besoin reste ON *quel que soit* `m`. La chambre la plus
froide est tirée vers `≈ M − Δ` ≈ `S_on − Δ` pendant toute la phase ON. Plus Δ
est grand, plus cette chambre est sur-refroidie (ex. chambre enfant à 21 °C
pendant que la chambre parents peine à 24,5 °C). Coût : confort + énergie.

**Effet B — court-cycle sur la chambre chaude** (régime Δ ≥ hystérésis, §3.1).
La chambre chaude oscille autour de `S_on` sans bande morte → marche/arrêt
rapprochés. Coût : usure compresseur, bruit, énergie. **C'est l'exact opposé du
bénéfice anti-oscillation revendiqué** par `90_observations.md`.

Les deux effets croissent avec Δ. **L'hétérogénéité est le seul facteur de
risque**, et l'hystérésis de 1 °C la rend très facilement franchissable.

## 3.3 Scénarios demandés

| Scénario | Comportement réel | Verdict |
|---|---|---|
| **Maison homogène** (Δ ≈ 0) | `m ≈ M` : bande morte propre [23,5 ; 24,5]. Anti-oscillation **vraie**. | ✅ Optimal — c'est le cas pour lequel la règle a été pensée. |
| **Maison hétérogène** (Δ ≥ 1 °C) | Régime dégénéré : Effet A **et** Effet B simultanés. | ⚠️ Court-cycle + sur-refroidissement. |
| **Chambre exceptionnellement chaude** (1 pièce stub, ex. plein sud) | `M` reste haut longtemps → unité tourne longtemps → les 2 autres chambres tirées sous `S_off`. | ⚠️ Sur-refroidissement marqué des pièces saines. |
| **Chambre exceptionnellement froide** (1 pièce nord/ombre) | `m` est en permanence ≤ `S_off` → la condition OFF dépend *entièrement* de `M < S_on`. La chambre froide ne protège plus l'arrêt : elle le **vide de sens**. | ⚠️ OFF piloté de fait par `M` seul → revient à du « max/quasi-max » sans bande morte. |
| **Nuit d'été, portes fermées** | Δ maximal (pièces isolées) → régime dégénéré garanti. | ⚠️ Le pire cas structurel ; cf. protocole d'observation existant. |
| **Forte canicule** (ext ≥ 33 °C) | `M` saturé haut → ON quasi permanent → Effets A/B masqués par le fonctionnement continu (peu de cycles). | ➖ Peu d'oscillation, mais sur-refroidissement de la pièce froide accentué. |
| **Forte inertie** (bâti lourd) | Transitions lentes → `M` franchit `S_on` lentement → court-cycle atténué (les bascules sont espacées). | ➖ Atténue l'Effet B, pas l'Effet A. |
| **Faible inertie** (bâti léger) | `M` franchit `S_on` vite et souvent → Effet B (court-cycle) amplifié. | ⚠️ Régime dégénéré le plus visible. |
| **Chambres fermées** | Découplage thermique → Δ grand → régime dégénéré. | ⚠️ |
| **Chambres ouvertes** | Brassage → Δ petit → proche de l'homogène. | ✅ |

## 3.4 Bénéfices / risques / effets de bord / hypothèses implicites

- **Bénéfices réels** : réactivité ON maximale (aucune pièce ne reste en
  surchauffe sans déclencher) ; anti-oscillation **si** maison homogène ;
  robustesse de structure (fallback, intégrité, filets).
- **Risques** : court-cycle (Δ ≥ hystérésis) ; sur-refroidissement de la pièce
  froide ; perte de sens du critère OFF quand une pièce est durablement froide.
- **Effet de bord majeur** : avec une seule entité `climate.clim` (décision
  globale, un seul actionneur), `max` pour ON + `min` pour OFF revient, en
  hétérogène, à **piloter sur la chambre chaude pour ON et à ne presque jamais
  laisser la chambre froide gouverner l'OFF** — c'est-à-dire un comportement
  proche de « max/max sans bande morte », le contraire de l'intention.
- **Hypothèses implicites** (non vérifiées dans le dépôt) :
  (1) la maison est thermiquement **homogène** ; (2) l'écart inter-chambres
  reste **< hystérésis** ; (3) un seul actionneur peut satisfaire 3 pièces
  hétérogènes. Aucune de ces hypothèses n'est garantie en été.

---

# PHASE 4 — COMPARAISON AVEC D'AUTRES STRATÉGIES

Comparaison **objective**, à hystérésis et seuils égaux. `X` = grandeur de
pilotage. Aucune n'est recommandée ici (audit non normatif).

| Stratégie ON / OFF | Réactivité surchauffe | Bande morte effective | Sur-refroidissement pièce froide | Court-cycle (Δ grand) | Garantit « aucune pièce chaude » | Remarque |
|---|---|---|---|---|---|---|
| **max / min** *(actuelle)* | ★★★ | s'effondre si Δ ≥ hyst. | Élevé | **Oui** si Δ ≥ hyst. | Non (OFF lâche tôt sur M) | Optimale **seulement** en homogène |
| max / max | ★★★ | **propre et constante** sur M | Élevé (tourne jusqu'à M≤S_off) | Non | **Oui** | « confort de la pire pièce » ; énergivore |
| min / min | ★ | propre sur m | Nul | Non | Non (laisse pièces chaudes) | Trop laxiste : sous-refroidit |
| moyenne maison | ★★ | propre sur la moyenne | Moyen | Non | Non | Équilibré, ignore les extrêmes |
| moyenne chambres | ★★ | propre | Moyen | Non | Non | Variante de la moyenne, périmètre réduit |
| médiane | ★★ | propre | Faible | Non | Non | **Robuste** à 1 pièce/capteur aberrant |
| percentile (P75/P90) | ★★–★★★ | propre | Réglable | Non | Quasi | Curseur entre moyenne et max |
| humidex (felt) | n/a temp | propre | dépend | Non | n/a | Pilote le **ressenti**, pas le sec ; pertinent climat humide (Bordeaux) ; unifierait COOL/DRY |
| T° + humidité combinée | ★★ | propre | dépend | Non | partiel | Confort plus fidèle, +dépendance HR (bruit) |
| **hybride** : ON sur `max`, OFF sur `moyenne` ou `max` | ★★★ | **propre** | Moyen | **Non** | Quasi/Oui | Conserve la réactivité ON (l'atout réel) en retirant le `min` d'OFF |

**Observation centrale, fondée sur §3 :** la moitié **ON (`max`) de la règle est
saine** — c'est l'atout réel (réactivité). C'est la moitié **OFF (`min`) qui porte
toute la fragilité** (effondrement de bande morte + sur-refroidissement + perte de
sens). Toute évolution éventuelle se concentrerait donc sur le **critère OFF**,
pas sur le critère ON.

> **[v1 — RENVERSÉ EN PHASE 6]** Cette « observation centrale » est **fausse** une
> fois la topologie prise en compte. Le `min`-OFF n'est pas la moitié fragile :
> c'est une **garantie de vivacité** (atteignabilité de OFF) propre au mono-zone.
> L'« effondrement de bande morte » et le « sur-refroidissement » sont réels mais
> **uniquement en régime couplé**, et constituent le **compromis soft assumé** du
> choix — pas un motif de bascule vers `max`-OFF, qui dégraderait la robustesse.
> Voir Phase 6 §6.5-6.6.

**Ce qui ne peut être tranché depuis le seul dépôt :** la valeur empirique de Δ.
Tout le diagnostic bascule sur « Δ ≥ 1 °C ? ». Or `temperature_max_chambres`,
`temperature_min_chambres` et `clim_target_mode` sont **historisés**
(`recorder.yaml` l.13-14 et l.258). La distribution réelle de `Δ` aux instants de
transition est donc **directement mesurable**, et le chantier dispose déjà d'un
cadre de mesure (`protocole_observation_seuils_cool.md`,
`investigation_historique_clim_30j.md`). **La preuve manquante est mesurable, pas
hypothétique.**

---

# PHASE 5 — CONCLUSION INITIALE  *(v1 — partielle ; révisée en Phase 6)*

> **Avertissement de reclassement.** La conclusion ci-dessous est celle de **v1**,
> obtenue **avant** prise en compte de la topologie mono-zone. Elle est
> **conservée pour l'historique intellectuel** mais **partiellement révisée** : la
> ligne « Mérite-t-elle une remise en question ? → ciblée sur le critère OFF » est
> **renversée** par la Phase 6. Lire la Phase 5 **puis** la Phase 6 pour la
> conclusion qui fait foi.

| Question | Réponse | Fondement |
|---|---|---|
| **Intentionnelle ?** | **Oui.** | `seuils_et_franchissements/90_observations.md` (« Cette asymétrie est volontaire ») + invariants `integrite_reglages`. |
| **Correctement documentée ?** | **Formule : oui. Intention : non.** | La formule (`max ≥`, `min ≤`) est exacte dans le contrat. La *justification* (« l'extinction attend que l'ensemble des zones redescendent ») décrit l'inverse du comportement de `min`-pour-OFF (cf. §3.1 ; Annexe A). Le rapport `audit_climatisation_arsenal.md` (D8) décrit en plus l'**ancienne** logique `≥` (pré-fix), désormais périmée. |
| **Cohérente ?** | **En code : oui. En intention : non robuste.** | Pas de deadlock, intégrité validée, filets présents — mais le confort revendiqué ne tient qu'en maison homogène. |
| **Optimale pour les objectifs Arsenal ?** | **Non démontré.** Optimale **sous l'hypothèse implicite d'homogénéité** uniquement. | §3.3 : en hétérogène (cas estival probable, hystérésis 1 °C), elle dégrade confort, stabilité et énergie. |
| **Mérite-t-elle une remise en question ?** | **Oui — ciblée sur le critère OFF**, et **après mesure** de Δ. | §4. Le critère ON (`max`) est sain ; seul OFF (`min`) est discutable. La donnée pour trancher est déjà historisée. |

**Synthèse non normative.** Le système est bien construit et l'asymétrie est un
choix assumé, pas un accident. Le problème n'est ni un bug ni la plomberie : c'est
(a) un **écart entre l'intention écrite et l'effet réel** de `min`-pour-OFF, et
(b) une **optimalité conditionnée à une homogénéité non garantie**. Avant toute
évolution, la bonne action est **empirique** : mesurer la distribution de
`Δ = temperature_max_chambres − temperature_min_chambres` aux transitions
`clim_target_mode`, sur données déjà historisées. Si `Δ < hystérésis` domine, la
règle actuelle est bonne et seule sa *documentation d'intention* doit être
corrigée. Si `Δ ≥ hystérésis` est fréquent, le critère **OFF** mérite un chantier
dédié (hors périmètre de ce document).

> **Supersession v2.** La dernière ligne (« remise en question ciblée sur OFF »)
> est **renversée** par la Phase 6 : sous topologie réelle, `min`-OFF **ne doit pas**
> être remplacé par `max`-OFF. Le reste de la synthèse (mesurer `Δ`, corriger la
> doc d'intention) reste valide, mais l'intention corrigée n'est plus « fragilité »
> mais « robustesse mono-zone » (Phase 6 §6.6, Annexe A).

---

# PHASE 6 — RÉVISION : CONTRE-ANALYSE TOPOLOGIQUE (v2)

> Cette phase **révise explicitement** la conclusion de la Phase 5. Elle ne
> raisonne plus sur les seules propriétés de l'hystérésis, mais sur la **réalité
> physique du logement** et la **contrôlabilité asymétrique** des pièces.

## 6.1 L'hypothèse implicite de v1, et pourquoi elle était fausse

Les Phases 1-4 restent **factuellement exactes** (la chaîne de décision est bien
celle décrite). Mais la **conclusion** de v1 reposait sur une hypothèse jamais
vérifiée dans le dépôt :

> *« Les trois chambres sont également contrôlables par le climatiseur. »*

Sous cette hypothèse, l'écart inter-chambres `Δ` n'est qu'un défaut d'homogénéité,
et `min`-OFF apparaît comme un arrêt « trop précoce ». **C'est faux dès qu'on
modélise la topologie.**

## 6.2 Topologie réelle (faits, avec preuves dépôt)

| Fait physique | Preuve dans le dépôt |
|---|---|
| **Un seul** climatiseur (`climate.clim` + `switch.clim_power`) | `climatisation/guard.yaml`, `trigger_execution.yaml` (entités au singulier) |
| **Mono-zone par conception** (pas de pilotage par pièce) | `contrats/climatisation/11_perimetre_exclu.md` : « pilotage multi-zones » **explicitement exclu** |
| Le refroidissement est **borné par une consigne** (pas « sans fin ») | `decision/consigne.yaml` → `clim_consigne_presence/absence` appliquée à `climate.clim` |
| **OFF est un état normal et volontaire, jamais une erreur** | `contrats/climatisation/01_finalite.md` |
| « éviter toute action par principe » | `01_finalite.md`, principes directeurs |
| **Aucun capteur de porte** dans la décision climatique | aucune entité `binary_sensor.*porte*` consommée par la chaîne COOL (autorisation, besoin, admissibilité) |

**Conséquence physique centrale.** Le climatiseur est **sur le palier**. Une
chambre n'est refroidie **que si sa porte est ouverte** (couplage par échange
d'air). Une chambre **fermée est thermiquement découplée** : l'appareil **ne peut
pas l'atteindre**. Donc, en régime de refroidissement :

- les pièces **couplées** (ouvertes) tendent vers le froid (la consigne) → ce sont
  elles qui deviennent le **`min`** ;
- une pièce **découplée chaude** (fermée) reste chaude → c'est souvent elle le
  **`max`**.

→ **Le `min` est presque toujours une pièce que le climatiseur contrôle
réellement. Le `max` peut être une pièce qu'il ne contrôle pas.** C'est l'asymétrie
de contrôlabilité que v1 ignorait.

## 6.3 Reformulation : `min`-OFF est une garantie de vivacité (atteignabilité de OFF)

La machine d'état réelle (Phase 3 §3.1) éteint quand `(max < S_on) ET (off franchi)`.

- **`min`-OFF** indexe l'arrêt sur une pièce **contrôlable** → l'état OFF est
  **toujours atteignable** : le climatiseur peut toujours amener une pièce couplée
  jusqu'à `S_off`.
- **`max`-OFF** indexerait l'arrêt sur la pièce la plus chaude, qui peut être
  **incontrôlable** (découplée) → l'état OFF devient **inatteignable** tant que la
  porte reste fermée → **acharnement**.

**C'est exactement le mécanisme que la question centrale supposait.** `min`-OFF
n'est pas la « moitié fragile » de la règle : c'est la **soupape de sûreté** qui
empêche une chambre isolée de retenir le système en marche.

> **Précision rigoureuse — limite de la garantie.**
> `min`-OFF ne protège l'atteignabilité de OFF **que lorsque le `max` est repassé
> sous le seuil d'allumage `S_on`** (car le franchissement ON est prioritaire dans
> `besoin_clim_cool` : tant que `max ≥ S_on`, l'état reste ON quel que soit le
> `min`). La protection de `min`-OFF opère donc dans la **bande `[S_off, S_on]`**.
> **Au-dessus de `S_on`**, c'est le critère d'**allumage sur le `max`** qui
> gouverne le maintien en marche — indépendamment de l'extinction (ni `min`-OFF ni
> `max`-OFF n'y changent quoi que ce soit).

## 6.4 Les trois régimes de couplage

### Régime 1 — entièrement couplé (toutes portes ouvertes)

Brassage d'air → `max ≈ min ≈` consigne. `Δ → 0`.
- `min`-OFF : bande morte propre `[S_off, S_on]`, anti-oscillation réelle.
- **C'est le seul régime où l'analyse v1 s'applique telle quelle**, et où `max`-OFF
  serait marginalement « plus propre » sur le confort de la pièce chaude.
- Revers de `min`-OFF ici : arrêt possiblement précoce de la pièce chaude
  accessible si `Δ` reste ≥ hystérésis (pièces inégalement exposées malgré portes
  ouvertes). **Défaut soft, auto-correctif.**

### Régime 2 — partiellement découplé (≥ 1 porte fermée, ≥ 1 ouverte) — *cas estival nominal*

Ex. **Parents fermée** (~26 °C, découplée) ; Arnaud/Matthieu ouverts, refroidis.

| | **`max`-ON / `min`-OFF** (actuel) | **`max`-ON / `max`-OFF** |
|---|---|---|
| Parents **> S_on** (26) | ON verrouillé par le `max` (acharnement causé par le critère **ON**, pas OFF) | **Identique** (même verrou ON) |
| Parents **dans `[S_off, S_on]`** (24) | `max<S_on` → `min`=Arnaud≈23 ≤ S_off → **OFF → retour à OFF** ✅ | OFF exige `max≤S_off` → Parents ≤ 23,5 **impossible** (découplée) → **reste ON, s'acharne**, fige Arnaud/Matthieu à la consigne, **n'atteint jamais OFF** ✗ |
| Fenêtre d'acharnement | étroite (uniquement `max>S_on`, hors de portée du critère OFF) | **large** (tout `max>S_off`) |
| Échappatoire | automatique (dès que le `max` découplé repasse sous `S_on`) | **manuelle** (réouverture de la porte) |

**C'est le régime décisif.** `min`-OFF y est **strictement plus robuste** :
l'arrêt s'appuie sur une pièce contrôlée ; `max`-OFF y crée un acharnement sans
échappatoire automatique.

### Régime 3 — totalement découplé (toutes portes fermées)

Aucune des 3 chambres n'est couplée ; le climatiseur ne refroidit que le palier
(non mesuré dans la décision). Les 3 capteurs dérivent vers le chaud.
- Si une chambre est `≥ S_on` : ON verrouillé par le `max` → acharnement (cause =
  critère ON). `min`-OFF et `max`-OFF **identiques** ici.
- Si toutes sont dans `[S_off, S_on]` : l'arrêt dépend de la lente fuite thermique
  sous les portes ; **`min`-OFF relâche le premier** (le `min` atteint `S_off`
  avant le `max`). `min`-OFF reste **≥** `max`-OFF, jamais pire.
- **Limite honnête** : dans ce régime, la protection de `min`-OFF s'**affaiblit**
  (plus aucune pièce franchement contrôlable). C'est un coin étroit, à distinguer
  du régime 2 où `min`-OFF protège clairement. La parade réelle de ce coin relève
  d'autres couches (présence, horaire, consigne), pas du choix `min`/`max`.

## 6.5 Le compromis, explicité

`min`-OFF et `max`-OFF échangent un défaut contre un autre. Le système **ne peut
pas distinguer** couplé de découplé (aucun capteur de porte) : il doit choisir
**une** règle robuste sous incertitude.

| | **Compromis ACCEPTÉ** (par `min`-OFF) | **Compromis REFUSÉ** (qu'aurait imposé `max`-OFF) |
|---|---|---|
| Nature | **Arrêt potentiellement précoce** de la pièce la plus chaude **accessible**, en régime couplé | **Acharnement climatique** sur une chambre **fermée** (OFF inatteignable) |
| Gravité | **Soft** : borné, **auto-correctif** (la pièce se réchauffe et redéclenche ; ou l'utilisateur ouvre la porte) | **Dur** : énergie continue, pièces accessibles figées à la consigne, **viole « OFF est normal »**, **aucune** échappatoire automatique |
| Réversibilité | immédiate, sans action humaine | nécessite une **action humaine** (ouvrir la porte) |
| Alignement philosophie Arsenal | **Cohérent** (OFF atteignable, dégradation acceptable, pas d'action « par principe ») | **En conflit** (action par principe, OFF nié) |

**Propriété de domination.** Sur l'axe **vivacité** (atteignabilité de OFF),
`min`-OFF **n'est jamais pire** que `max`-OFF, et **strictement meilleur** dès
qu'une pièce découplée stationne dans `[S_off, S_on]`. Le prix est un défaut de
confort **soft** en régime couplé. Un contrôleur robuste préfère la règle dont le
**pire cas est borné** : c'est `min`-OFF.

## 6.6 Conclusion révisée (fait foi)

| Question | Réponse v2 | Fondement |
|---|---|---|
| **Intentionnelle ?** | **Oui** — et l'intention est plus profonde que documentée : robustesse mono-zone. | `90_observations.md` + `11_perimetre_exclu.md` + `01_finalite.md` |
| **Correctement documentée ?** | **Formule : oui. Intention : non — mais pas pour la raison donnée en v1.** La bonne intention est le **découplage / atteignabilité de OFF**, pas « attendre toutes les zones ». | Annexe A (réécrite) |
| **Cohérente ?** | **Oui**, y compris en intention, une fois la topologie prise en compte. | §6.3-6.5 |
| **Optimale pour les objectifs Arsenal ?** | **Oui sous incertitude de couplage** : c'est la règle au pire cas borné, alignée sur « OFF est normal » et « comportement dégradé acceptable ». | §6.5 |
| **Mérite-t-elle une remise en question ?** | **Non sur le critère OFF.** Le `min`-OFF est à **conserver**. La seule action utile est **documentaire** (clarifier l'intention) et, optionnellement, **empirique** (mesurer la fréquence des régimes). | §6.5-6.6 |

**Renversement explicite vs v1.** Là où v1 concluait « remise en question ciblée
sur OFF (vers `max`/moyenne) », **v2 conclut l'inverse** : `min`-OFF est un choix
de conception correct ; `max`-OFF serait une **régression** de robustesse. Le
critère ON (`max`) **et** le critère OFF (`min`) sont tous deux justifiés —
respectivement par la **réactivité** et par la **vivacité**.

**Intention fidèle retenue** (portée par le patch documentaire séparé) :

> « L'allumage est indexé sur la chambre la plus **chaude** : réactivité à la
> surchauffe locale. L'extinction est indexée sur la chambre la plus **froide** —
> donc sur une pièce que le climatiseur de palier **contrôle effectivement** — afin
> que l'état OFF reste **atteignable** : une chambre thermiquement découplée (porte
> fermée), une fois repassée sous le seuil d'allumage, ne peut pas à elle seule
> maintenir la climatisation active. *Au-dessus du seuil d'allumage, c'est le
> critère d'allumage sur le `max` qui gouverne.* En régime entièrement couplé, le
> revers est un arrêt possiblement précoce de la pièce la plus chaude accessible —
> dégradation acceptable, auto-corrigée par la réouverture d'une porte. »

---

## ANNEXE A — Écarts documentation ↔ runtime relevés (sans correction appliquée)

| # | Écart | Localisation | Nature | Gravité |
|---|---|---|---|---|
| A1 | Justification de l'asymétrie : « l'extinction attend que **l'ensemble** des zones redescendent sous le seuil ». Cette phrase est **doublement imprécise** : (a) elle décrit `max`-OFF, pas le `min`-OFF réel ; (b) surtout, elle **manque l'intention véritable** mise en évidence en Phase 6 — l'extinction est indexée sur la pièce **contrôlable** (la plus froide) pour garantir l'**atteignabilité de OFF** face à une chambre **thermiquement découplée**. | `contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md` § *Asymétrie max / min — COOL* | Doc d'intention incomplète (formule exacte par ailleurs) | Explicabilité — **non bloquant** |
| A2 | Constat D8 décrit l'extinction comme `temperature_min ≥ seuil_extinction` (`≥`) ; le runtime actuel est `<=`. Vestige **pré-fix**, déjà soldé au backlog. | `audits/01_rapports/climatisation/audit_climatisation_arsenal.md` D8 | Rapport historique périmé | Hygiène doc — **non bloquant** |

> **A1 fait l'objet d'un patch documentaire séparé** (purement éditorial, aucun
> runtime ni contrat modifié) — `patch_doc_intention_asymetrie_cool.md`, **mis à
> jour en v2** : la correction d'intention retenue est la **formulation
> « découplage / atteignabilité de OFF »** (Phase 6 §6.6), et **non** le cadrage
> « fragilité » de v1. A2 est laissé en l'état (rapport historique, déjà résolu).

---

## ANNEXE B — Inventaire des preuves (fichiers lus)

**Runtime (template sensors)** : `seuils_on_off/cool/{on,off,seuil_allumage_cool_atteint,seuil_extinction_cool_atteint}.yaml` · `besoin/cool.yaml` · `autorisation/cool.yaml` · `decision/{mode_target,raison}.yaml` · `meteo/mesures/temperature/chambres/{max/global,min}/valeur.yaml` · `seuils_on_off/dry/{seuil_allumage,seuil_extinction}_dry_atteint.yaml` · `system/integrite_reglages/climatisation.yaml`.
**Automatisations** : `climatisation/{guard,watchdog,reprise_apres_echec,trigger_execution,modes}.yaml` · `cool/admissibilite.yaml`.
**Contrats** : `seuils_et_franchissements/{20_binary_sensors_franchissement,90_observations}.md` · `besoins/{10_besoins,90_observations}.md`.
**Historisation** : `recorder.yaml` (l.13-14 temp max/min chambres ; l.258 `clim_target_mode`).
**Chantier existant** : `04_chantiers/climatisation/{backlog_climatisation_hysteresis,protocole_observation_seuils_cool,chantier_observabilite_cool}.md`.
**Helpers (plages)** : `03_input_numbers/…` (`clim_seuil_declenchement/extinction_{presence,absence}`).

*Commit audité : `ce24fb28`. Aucune modification n'a été apportée au dépôt par cet audit.*
