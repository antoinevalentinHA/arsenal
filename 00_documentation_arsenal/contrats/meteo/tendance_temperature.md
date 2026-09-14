# Arsenal — Contrat métier et architectural
# Famille — Tendance thermique des agrégats intérieurs (lecture glanceable)
# Version : 1.2 (révision)
# Statut : normatif — doctrine de décision v1.1 conforme au runtime (§0, §18) ; doctrine d'architecture v1.2 (couche de projection statistique ré-échantillonnée, §4.2) désormais conforme au runtime, déployée et validée terrain (PR #839, commit `9de7993`, §19). Validation terrain des seuils §8.2 : dette ouverte distincte, non résorbée, non traitée par cette clôture.
# Chemin : 00_documentation_arsenal/contrats/meteo/tendance_temperature.md
# Dépend de : meteo.md, affichage.md, validation.md, fallback.md
# Renvoi : extrema_jour_courant.md §9.3 (usage « tendance » de la plateforme statistics)
#          audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md (constat fondant l'amendement v1.1)
#          resilience_integrations.md — R-ANCRAGE-2, R-AXE1-1 (exclusion explicite de la couche de projection de tout axe résilience/fraîcheur, §4.2, §15)
#          architecture/01_recorder/contrat.md — Population A (statut Recorder de la couche de projection, §13)

---

## 0. Statut et portée de ce document

Ce document est un **contrat normatif** : il est l'**autorité** sur la famille
Arsenal « tendance thermique des agrégats intérieurs ». Il définit ce que le
système *doit* faire ; le runtime en est l'**implémentation**, qui lui doit
conformité — et non l'inverse. Un audit lit le runtime comme **référence
factuelle** (ce qui se passe réellement), mais cette lecture ne confère aucune
autorité normative au comportement observé : si le runtime s'écarte du besoin,
c'est le contrat qui tranche le besoin, puis le runtime qui s'aligne.

**Amendement v1.1.** L'audit
[`audit_tendance_temperature_sensibilite.md`](../../audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md)
a établi que la **grandeur de décision** posée par la v1.0 — *valeur instantanée
de la source moins sa propre moyenne glissante 60 min* — est **inadaptée au
besoin** : sur une rampe lente monotone, cet écart **sature** à `pente × W/2` et
**ne croît pas** avec l'ampleur de la tendance, classant à tort en `stable` des
hausses ou baisses pourtant perceptibles pour le confort. Ce n'était **pas un
défaut d'implémentation** (le runtime appliquait fidèlement la v1.0) mais une
**insuffisance normative du contrat lui-même**. La présente version **déprécie**
cette grandeur et lui substitue une grandeur de tendance lissée
**`moyenne_courte − moyenne_longue`** (§3.2, §5, §8).

**État d'implémentation — résorbé.** Le runtime
(`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`,
`12_template_sensors/meteo/tendance/temperature.yaml`) implémente **la grandeur
v1.1** (`moyenne_courte − moyenne_longue`, seuils `S_in=0.15` / `S_out=0.08`).
L'écart contrat ↔ runtime décrit par les versions précédentes de ce document est
**résorbé** ; il est conservé à titre historique en §18. Une **dette distincte**
subsiste sur la validation terrain des seuils (§8.2) : elle n'est **pas** couverte
par cette résorption et reste ouverte.

**Amendement v1.2 — défaut fonctionnel prouvé et cible architecturale.** Preuve
terrain : lorsque `sensor.temperature_moyenne_maison` reste numériquement
valide et inchangée pendant plus de 15 minutes sans nouvel événement utile, la
moyenne `statistics` courte (`W_court`) devient `unknown` alors que la moyenne
longue reste numérique et que la source, elle, demeure exploitable — la
tendance bascule alors à tort en `indisponible`. Le défaut : une valeur métier
stable et valide peut être interprétée comme absence de donnée statistique
simplement parce qu'elle ne génère pas assez de rapports dans la fenêtre
courte. Deux corrections ont été comparées : un TTL dans la couche
d'interprétation, écarté ; et un **ré-échantillonnage dédié** en amont des deux
couches `statistics`, retenu. La cible amendée insère une **couche de
projection statistique ré-échantillonnée** entre la source et les deux couches
`statistics` existantes (§2.2, §4.2). Cette couche ne modifie ni la grandeur de
décision (§3.2, inchangée depuis v1.1) ni les seuils `S_in`/`S_out` (§8.2, dette
de validation terrain inchangée et non rouverte par le présent amendement) :
elle règle exclusivement le **défaut d'alimentation en échantillons** des
couches `statistics`.

**Clôture v1.2 — runtime déployé et validé terrain.** La couche de projection
décrite ci-dessus a été implémentée (PR #839, commit `9de7993`) : trois
trigger-based template sensors de projection
(`sensor.temperature_min_chambres_projection`,
`sensor.temperature_moyenne_maison_projection`,
`sensor.temperature_max_chambres_projection`, §11), repointage des six
couches `statistics` existantes sur leur projection respective, inclusion
Recorder Population A des trois projections (§13). Le SHA candidat exact de
la PR a été déployé sur le `/config` réel et validé terrain avant merge :
YAML valide, `ha core check` vert, redémarrage HA propre, trois projections
numériques et strictement égales à leur source, six `statistics` numériques
dès le premier report valide, trois tendances disponibles et `stable` ; sur
les axes `min_chambres` et `max_chambres`, un plateau de plus de 15 minutes a
montré une valeur de projection et un `last_changed`/`last_updated` inchangés
tandis que `last_reported` avançait toutes les 5 minutes, les `statistics`
15/60 min restant numériques et sans aucune bascule `indisponible` ; sur
l'axe `moyenne_maison`, un changement naturel de la source s'est propagé
immédiatement à la projection avec un véritable `state_changed` et une mise à
jour des `statistics`. Aucun défaut bloquant n'a été observé. **Aucun test de
panne réelle n'a été provoqué ni exécuté** : ce point reste hors du périmètre
validé par ce lot. PR #839 mergée sur `main`. L'écart §19 est **résorbé** ; il
est conservé à titre historique. La dette de validation terrain des seuils
`S_in`/`S_out` (§8.2) reste **ouverte et distincte**, non traitée par cette
clôture.

Toute implémentation ultérieure doit être conforme aux invariants `INV-TEND-*`
ci-dessous, dans leur version la plus récente (v1.1 pour la grandeur de
décision, v1.2 pour la couche de projection). Tout écart d'implémentation non
tracé au changelog est une non-conformité, pas une interprétation.

---

## 1. Objet

Définir, pour chacun des trois agrégats thermiques intérieurs déjà affichés en
conduite, un **capteur de tendance dédié** indiquant si la grandeur observée est
en **hausse**, en **baisse** ou **stable**, accompagné d'une **icône dynamique**
adaptée.

Intention utilisateur réelle : rendre l'information thermique **lisible en
quelques secondes pendant la conduite**, sans lecture chiffrée fine. La priorité
déclarée est, dans l'ordre : **robustesse, lisibilité, stabilité** — la
réactivité absolue est explicitement secondaire.

---

## 2. Périmètre

### 2.1 Sources déclarées (existantes, inchangées)

| Rôle source | Entité (existante) | Nature |
|---|---|---|
| Minimum chambres | `sensor.temperature_min_chambres` | agrégat trigger template (min des 2 chambres de l'étage — Salle de Jeux exclue, C32/A2) |
| Moyenne maison | `sensor.temperature_moyenne_maison` | agrégat template (moyenne 8 pièces) |
| Maximum chambres | `sensor.temperature_max_chambres` | agrégat trigger template (max des 2 chambres de l'étage — Salle de Jeux exclue, C32/A2) |

Ces trois entités sont des **agrégats déjà qualifiés**. La présente famille les
consomme **en lecture seule stricte**. Elle ne les modifie pas, ne les renomme
pas, ne les réagrège pas et ne relit pas les capteurs de pièce sous-jacents.

### 2.2 Capteurs dérivés (à créer)

La famille crée, par axe, **quatre couches** (doctrine cible v1.2) :

- une **couche de projection statistique ré-échantillonnée**, recopie stricte
  de la source à cadence périodique explicite, dédiée à l'alimentation fiable
  des deux couches `statistics` ci-dessous (§4.2) — **amendement v1.2,
  implémentée et validée terrain, §19** ;
- une **couche statistique « moyenne courte »** (moyenne glissante de la
  projection sur fenêtre courte `W_court`) ;
- une **couche statistique « moyenne longue »** (moyenne glissante de la
  projection sur fenêtre longue `W_long`) ;
- une **couche d'interprétation** exposant l'état de tendance et son icône, à
  partir de l'**écart entre les deux moyennes**.

Soit **3 axes**, chacun produisant un capteur de tendance consommable.

> **Note historique (v1.0 → v1.1, résorbée).** La v1.0 ne créait qu'**une** couche
> statistique (moyenne longue 60 min) et comparait la **valeur instantanée** à
> cette moyenne. La couche « moyenne courte » a été ajoutée en runtime ; les deux
> couches sont **vivantes** (§11, §12). Cf. §18 pour la trace de cette résorption.
>
> **Note contractuelle (v1.2, résorbée).** Les deux couches `statistics`
> consommaient jusqu'ici directement la source agrégée. L'amendement v1.2
> intercale la couche de projection **entre** la source et les deux couches
> `statistics`, sans modifier ces dernières ni la source. Cette intercalation
> est **vivante** en runtime (§11, §13). Cf. §19 pour la trace de cette
> résorption.

### 2.3 Ce que la famille n'est pas

La famille ne couvre **pas** :

- la production ou la correction de la donnée thermique (amont, inchangé) ;
- la validation de plausibilité des sources (déléguée, cf. §3.3) ;
- les extrema du jour civil (couverts par `extrema_jour_courant.md`) ;
- la couche couleur de dashboard (`sensor.couleur_temperature_*`) ;
- la configuration des *Favoris Android Auto* elle-même, qui réside dans
  l'application compagnon et **hors du dépôt** ;
- toute décision, recommandation ou pilotage d'équipement.

---

## 3. Nature métier

### 3.1 Définition de la tendance

La tendance d'un axe est l'**orientation récente** de la grandeur source,
qualifiée sur une **fenêtre glissante courte**, et réduite à trois états
lisibles : la grandeur **monte**, **descend**, ou **n'évolue pas significativement**.

La tendance est une **interprétation**, pas une mesure. À ce titre elle relève
strictement de la couche backend : l'UI ne la calcule jamais (cf. `affichage.md`,
principe « l'UI observe, elle n'interprète jamais »).

### 3.2 Grandeur de décision

> **Doctrine cible (v1.1).** La décision s'appuie sur l'**écart entre une moyenne
> glissante courte et une moyenne glissante longue** de la même source :

```text
ecart_axe = moyenne_glissante_source(W_court) − moyenne_glissante_source(W_long)
```

- `ecart_axe > 0` significatif  → la moyenne récente dépasse la moyenne de fond → **hausse**
- `ecart_axe < 0` significatif  → la moyenne récente est sous la moyenne de fond → **baisse**
- `|ecart_axe|` non significatif → **stable**

Le caractère « significatif » est tranché par une **bande morte avec hystérésis**
(cf. §8).

**Pourquoi ce changement (grandeur v1.0 dépréciée).** La v1.0 décidait sur
`valeur_instantanee_source − moyenne_glissante_source(W_long)`. Cette grandeur est
**dépréciée** : pour une rampe linéaire de pente `r`, la valeur instantanée
n'excède sa propre moyenne glissante que d'un **décalage de retard** constant
`r × W_long/2`, qui **sature** et **ne grandit pas** avec la durée ou l'ampleur de
la tendance. Avec `W_long = 60 min`, l'écart plafonne à `r × 30 min` ; il faut
donc une pente **≥ 0,8 °C/h soutenue** pour franchir un seuil de 0,4 °C, alors
qu'une dérive de confort perceptible se situe à 0,2–0,6 °C/h. Résultat
documenté : `stable` permanent sur des hausses/baisses réelles
(cf. [`audit_tendance_temperature_sensibilite.md`](../../audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md) §4).

La grandeur cible `moyenne_courte − moyenne_longue` corrige ce défaut : pour une
rampe, elle vaut `r × (W_long − W_court)/2`, donc **croît avec l'écartement des
fenêtres** et reste **lissée des deux côtés** (robuste au bruit, contrairement à
une comparaison d'échantillon instantané). Elle reste **dans l'idiome maison**
`statistics`/`mean` (sans état, sans automatisation, sans helper — §5, §14).

> **Note historique.** Le runtime a appliqué la grandeur v1.0 dépréciée jusqu'à la
> passe runtime tracée en §18 ; il applique désormais la grandeur v1.1 ci-dessus.

### 3.3 Donnée exploitable

La couche d'interprétation considère la source comme **exploitable** si et
seulement si sa valeur instantanée est **numérique** (ni `unknown`, ni
`unavailable`, ni `none`, ni chaîne vide).

La famille **ne réapplique aucune plage de plausibilité** sur les sources : la
qualification physique est de la responsabilité de l'amont (les agrégats, et en
deçà les contrats d'axe `meteo.md` / `validation.md` / `fallback.md`). Réappliquer
ici une borne reviendrait à dupliquer une autorité de validation, ce que le
domaine météo interdit (source unique de vérité par couche).

**Réutilisation par la couche de projection (v1.2).** Ce même critère
d'exploitabilité gouverne strictement la disponibilité (`availability`) de la
couche de projection (§4.2) : la projection est disponible si et seulement si
la source l'est, au même instant, selon ce critère — et pour aucune autre
raison.

### 3.4 Absence de tendance

Tant que **l'une des deux** fenêtres statistiques (courte ou longue) ne contient
pas assez d'échantillons pour produire sa moyenne, ou tant que la source n'est pas
exploitable, **la tendance n'existe pas** : l'état exposé est `indisponible`.
L'absence n'est jamais comblée par extrapolation ni masquée (cf. INV-TEND-5).

---

## 4. Architecture canonique de la famille

### 4.1 Schéma canonique

Cinq couches, par axe, sans pilotage et sans historique métier propre
(doctrine cible v1.2) :

```text
source métier (existante, inchangée)
   sensor.temperature_{min_chambres | moyenne_maison | max_chambres}
        │  lecture seule
        ▼
couche de projection statistique ré-échantillonnée   ← §4.2 (amendement v1.2, §19)
   recopie stricte, cadence périodique explicite, aucune mémoire, aucun fallback
        │
        ├───────────────────────────────┐
        ▼                                ▼
couche statistique « courte »      couche statistique « longue »
   moyenne glissante W_court           moyenne glissante W_long
   (statistics / mean)                 (statistics / mean)
        │                                │
        └──────────────┬─────────────────┘
                       ▼
couche d'interprétation          ← écart = moyenne_courte − moyenne_longue
   {hausse | baisse | stable | indisponible}   + icône dynamique
        │  restitution directe
        ▼
Favoris Android Auto             ← rendu glanceable (hors dépôt)
```

La couche exposée s'arrête à l'interprétation : son consommateur direct et
nommé est la catégorie *Favoris* de l'interface de conduite. Aucune couche
supplémentaire (couleur, historique, palmarès) n'est créée sans consommateur
réel.

Précédent architectural : `sensor.clim_mode_local`
(`12_template_sensors/climatisation/decision/mode.yaml`) établit déjà le motif
d'un **capteur portant lui-même une icône dynamique « compatible Android Auto »**.
La présente famille étend ce motif éprouvé à la tendance thermique.

### 4.2 Couche de projection statistique ré-échantillonnée (amendement v1.2)

#### Rôle normatif

> La couche de projection est une **série temporelle synthétique dérivée**,
> exclusivement destinée à alimenter les deux couches `statistics` de la
> présente famille (§4.1, §12).

Elle :

- ne crée aucune vérité métier ;
- ne qualifie et ne valide aucune source (cf. §3.3 — l'autorité de
  qualification reste amont) ;
- ne choisit aucune source ;
- ne lisse, n'agrège et ne transforme rien (recopie stricte, INV-TEND-15) ;
- ne mémorise rien (INV-TEND-16) ;
- ne prolonge ni n'extrapole jamais une valeur devenue non exploitable ;
- ne déclenche et ne porte aucun fallback ni aucun seuil métier (INV-TEND-17) ;
- ne sert jamais à qualifier la résilience, la santé ou la fraîcheur de la
  source amont (INV-TEND-19, renvoi `resilience_integrations.md` R-ANCRAGE-2
  et R-AXE1-1) ;
- n'a qu'un seul type de consommateur autorisé : les couches `statistics`
  courte et longue de la présente famille (INV-TEND-20).

#### Mécanisme retenu

Trigger-based template sensor, par axe :

- déclencheurs : `state` sur la source ; `time_pattern` périodique (cadence
  ci-dessous) ; `homeassistant: start` ;
- `state` : recopie stricte de l'état de la source, sans aucune
  transformation ;
- `availability` : exploitabilité numérique instantanée de la source, au sens
  strict du §3.3 — ni mémoire, ni délai, ni tolérance ;
- aucune variable de mémoire, aucun `restore_state`, aucun TTL, aucun
  fallback.

**`force_update` est interdit** dans ce mécanisme, à quelque titre que ce soit
(INV-TEND-18). Qualification technique retenue : l'attribut n'existe pas dans
le schéma YAML d'un template sensor / trigger-based template sensor ; là où il
existe ailleurs dans Home Assistant, il transforme une valeur strictement
identique en véritable `state_changed`, rafraîchissant `last_changed`,
`last_updated` et `last_reported` — ce qui produirait un churn Recorder
artificiel et brouillerait la distinction entre échantillonnage synthétique et
changement réel de valeur amont. Aucune des deux distinctions que cette
famille doit préserver (§9, §13) ne peut tolérer ce brouillage.

#### Comportement sur tick périodique à valeur identique

Sur un tick `time_pattern` dont la valeur recopiée est identique à l'état
précédent, le comportement Home Assistant est le suivant, et doit être
respecté tel quel par l'implémentation :

- l'état est réécrit ;
- aucun `state_changed` n'est émis ;
- ni `last_changed` ni `last_updated` ne sont modifiés ;
- `last_reported` est rafraîchi ;
- un événement `state_reported` est émis.

La plateforme `platform: statistics` consomme nativement **les deux**
événements, `state_changed` et `state_reported`, comme échantillons valides.
Le tick périodique alimente donc les deux couches `statistics` en aval sans
qu'aucun changement métier n'ait eu lieu — c'est précisément la propriété qui
corrige le défaut décrit en §0, sans recourir à `force_update`.

#### Cadence

La cadence du déclencheur `time_pattern` est bornée par la fenêtre courte :

```text
T ≤ W_court / 3
```

garantissant plusieurs échantillons par fenêtre courte quelle que soit
l'activité de la source. La **valeur candidate actuelle** est `/5` (idiome
Arsenal déjà en usage pour les réveils périodiques), homogène sur les trois
axes (INV-TEND-18). Cette borne est l'invariant contractuel ; `/5` en est la
valeur actuellement retenue, ajustable tant que la borne reste respectée, sans
que cela constitue une modification de `W_court`, `W_long`, `S_in` ou `S_out`
(§8, inchangé).

#### Exclusion résilience explicite

Le `last_reported` de la couche de projection est **synthétique par
construction** (section précédente) : il ne doit **jamais** servir de preuve
de fraîcheur, de santé ou d'activité réelle de la source amont. La couche de
projection est une entité **dérivée** au sens de `resilience_integrations.md`
R-ANCRAGE-2 (template, valeur stabilisée) : elle est de ce fait
**irrecevable** dans tout périmètre de détection résilience/fraîcheur, sur
cette famille comme sur toute autre (INV-TEND-19). Aucune modification de
`resilience_integrations.md` n'est requise : la doctrine existante couvre déjà
ce cas.

#### Restart

Au redémarrage :

- la couche de projection est réévaluée depuis la source **live**
  (déclencheur `homeassistant: start`), sans mémoire métier propre à
  restaurer ;
- les couches `statistics` courte et longue reconstruisent leur fenêtre depuis
  l'historique Recorder de la projection selon la mécanique HA existante
  (cf. §13 — Population A) ;
- aucun état intermédiaire n'est à restaurer par la présente famille.

---

## 5. Méthode de calcul retenue et justification

### 5.1 Méthode retenue

**Deux moyennes glissantes (`statistics`, `state_characteristic: mean`) sur une
fenêtre courte `W_court` et une fenêtre longue `W_long`, puis interprétation par
écart `moyenne_courte − moyenne_longue`, avec bande morte et hystérésis.**

> **Méthode v1.0 dépréciée.** La v1.0 retenait *une seule* moyenne (longue) et
> comparait la **valeur instantanée** à cette moyenne. Cette grandeur sature sur
> les rampes lentes (§3.2) et est abandonnée. La justification §5.3 ci-dessous est
> mise à jour en conséquence.

### 5.2 Méthodes étudiées et arbitrage

| Méthode | Robustesse | Stabilité | Lisibilité | Pertinence Android Auto | Verdict |
|---|---|---|---|---|---|
| Comparaison instantanée (valeur vs valeur N min avant, en template) | Faible (échantillon unique, sensible au bruit) | Faible (scintille) | Bonne | Faible | **Écartée** |
| Valeur instantanée − moyenne glissante longue (`statistics`/`mean`) | Élevée (lissage) | Élevée | Bonne | Moyenne | **Dépréciée v1.1** : sature à `r × W/2` sur rampe lente ⇒ faux `stable` (audit sensibilité §4) |
| **Moyenne courte − moyenne longue (deux `statistics`/`mean`)** | **Élevée (double lissage)** | **Élevée** | **Élevée (écart simple)** | **Élevée** | **Retenue v1.1** : croît avec la tendance (`r × (W_long−W_court)/2`), lissée des deux côtés |
| Fenêtre glissante `statistics` `change` (dernier − premier) | Bonne | Bonne | Bonne | Bonne | Acceptable, mais sensible à l'échantillon de bord ; écartée au profit du double `mean` |
| `binary_sensor` `platform: trend` (pente, gradient) | Élevée | Élevée | Moyenne (binaire par sens) | Moyenne | Écartée : impose 2 binaires par axe (6 entités) + recombinaison pour produire 3 états ; « stable » seulement implicite |
| `sensor` `platform: derivative` (pente °C/temps) | Élevée | Élevée | Moyenne (unité de pente) | Moyenne | Écartée : exige de toute façon un seuillage et une fenêtre ; la pente est moins directement lisible qu'un écart |
| Helper intermédiaire + automatisation de snapshot | Élevée (contrôle total) | Élevée | Bonne | Bonne | Écartée : surdimensionnée — réintroduit un écrivain souverain et une automatisation là où une statistique sans état suffit |
| Lecture d'historique en template (`states.…` sur historique) | Faible (coûteux, fragile) | Faible | — | Faible | **Écartée** |

### 5.3 Justification du choix

1. **Cohérence avec l'existant.** La plateforme `statistics` avec
   `state_characteristic: mean` est **déjà** le motif établi du dépôt pour lisser
   la température (`13_sensor_platforms/statistics/meteo/temperature.yaml`,
   moyennes glissantes par zone). La famille réutilise ce motif éprouvé.
2. **Légitimité doctrinale explicite.** `extrema_jour_courant.md` §9 interdit la
   fenêtre glissante **comme source d'un extrême du jour**, mais §9.3 autorise
   explicitement la plateforme `statistics` **pour des usages explicitement
   qualifiés « tendance »**. Le présent usage est précisément celui-là.
3. **Robustesse et stabilité avant réactivité.** Le **double** lissage absorbe le
   bruit capteur des deux côtés de l'écart (les deux termes sont des moyennes, pas
   un échantillon instantané) ; il est donc plus robuste que la grandeur v1.0. La
   bande morte + hystérésis (§8) supprime le scintillement — condition impérative
   d'un affichage consulté en conduite.
4. **Lisibilité et non-saturation.** L'écart entre une moyenne récente et une
   moyenne de fond se réduit trivialement à trois états ; la sémantique « la maison
   se réchauffe / se refroidit / est stable » est immédiate. Surtout, contrairement
   à `valeur − moyenne`, cet écart **croît avec la tendance** (`r × (W_long−W_court)/2`)
   au lieu de saturer : c'est la propriété même qui corrige le faux `stable`.
5. **Sans état, sans écrivain souverain.** Les **deux** couches statistiques sont
   dérivées et sans persistance métier à gouverner ; aucun helper, aucune
   automatisation, donc moindre surface de maintenance et de panne.
6. **Séparation des responsabilités.** Statistique (perception) et interprétation
   sont deux couches distinctes ; l'UI ne fait que restituer. Conforme à la
   doctrine « le backend décide, l'UI restitue ».

---

## 6. États autorisés

L'état de tendance appartient à l'**ensemble fermé** :

```text
hausse | baisse | stable | indisponible
```

Aucune autre valeur n'est admise. `indisponible` est un état de **première
classe**, jamais une valeur masquée ni une chaîne vide.

---

## 7. Icônes dynamiques

À chaque état correspond **une et une seule** icône, portée par le capteur de
tendance lui-même (jamais par une carte).

Le vocabulaire iconographique est volontairement **directionnel et fortement
lisible**, car les capteurs de tendance sont destinés à être affichés sous les
valeurs de température correspondantes, notamment dans Android Auto. Le contexte
thermique est donc déjà porté par la tuile de température ; l'icône de tendance
ne doit restituer que le sens d'évolution.

| État | Icône | Justification |
|---|---|---|
| hausse | `mdi:arrow-up-bold` | flèche montante explicite, lisible en conduite |
| baisse | `mdi:arrow-down-bold` | flèche descendante explicite, lisible en conduite |
| stable | `mdi:minus-thick` | absence d'évolution significative, sans ambiguïté thermique |
| indisponible | `mdi:alert-circle-outline` | absence d'exploitation fiable, distincte d'une tendance stable |

L'icône est **descriptive**, jamais prescriptive : elle ne suggère aucune action
ni aucun confort souhaitable (cf. `affichage.md`, Invariant 5).

---

## 8. Seuils et fenêtres

### 8.1 Bande morte (dead-band) et hystérésis

La transition vers `hausse` ou `baisse` n'est déclarée que si l'écart
`moyenne_courte − moyenne_longue` franchit un **seuil d'entrée** ; le retour à
`stable` n'a lieu qu'en deçà d'un **seuil de sortie** strictement inférieur. Cette
**asymétrie est l'hystérésis** ; elle empêche tout scintillement autour du seuil.

### 8.2 Cibles candidates v1.1 — déployées en runtime, non validées (NON figées)

> **Statut de ces valeurs — dette ouverte distincte.** Ces valeurs sont
> **effectivement déployées en runtime** (`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`,
> `12_template_sensors/meteo/tendance/temperature.yaml`) depuis la passe tracée en
> §18. Leur déploiement **ne vaut pas validation** : elles restent des **cibles
> candidates**, **pas** des valeurs définitives. Le **plancher de bruit réel** des
> trois agrégats n'a **toujours pas été mesuré** (cf. audit sensibilité §9,
> tests 1–3) ; cette mesure était et reste un **préalable contractuel** à leur
> figement (§8.3), et son absence n'a **pas été comblée** par la mise en
> production. Tant que cette validation n'a pas eu lieu, ces valeurs restent
> **actives en runtime** mais **ne deviennent pas** un défaut contractuel
> opposable ; ne pas lire leur présence en production comme une validation de
> fait. Cette dette est **distincte** de la résorption de l'écart §0/§18 et n'est
> **pas** close par elle.

| Paramètre | Cible candidate | Caractère |
|---|---|---|
| Fenêtre longue `W_long` | 60 min | cadrage v1.1, à confirmer |
| Fenêtre courte `W_court` | ≈ 15 min | cible candidate, à valider |
| Seuil d'entrée `S_in` | ≈ 0,15 °C | cible candidate, à valider (`> plancher de bruit`) |
| Seuil de sortie `S_out` | ≈ 0,08 °C | cible candidate, à valider (`S_out < S_in` impératif) |

### 8.3 Justification des cibles candidates

- **`W_long = 60 min`** : moyenne de fond ; lissage fort, sémantique « dernière
  heure », conforme à *stabilité > réactivité*. Inchangée par rapport à la v1.0.
- **`W_court ≈ 15 min`** : moyenne récente ; assez courte pour réagir à une dérive
  de confort, assez longue pour rester lissée (≠ échantillon instantané). Pour une
  rampe, l'écart vaut `r × (W_long−W_court)/2 ≈ r × 22,5 min` : une dérive de
  0,4 °C/h produit ≈ 0,15 °C d'écart — d'où le `S_in` candidat ci-dessous.
- **`S_in ≈ 0,15 °C`** : calé pour détecter ≈ 0,4 °C/h, **sous réserve** que le
  plancher de bruit mesuré le permette ; sinon `S_in` devra être relevé (le bruit
  des agrégats, arrondis 0,1 °C, n'est pas encore caractérisé).
- **`S_out ≈ 0,08 °C`** : ≈ moitié du seuil d'entrée — marge anti-rebond classique.

Le **risque de faux positifs** est l'inverse du défaut v1.0 : un `S_in` trop bas
relativement au bruit ferait scintiller `hausse`/`baisse`. C'est précisément ce
que la **mesure préalable du bruit** (audit §9) doit borner. **Ne pas réduire la
correction à « on baisse le seuil »** : le gain vient d'abord de la **grandeur**
(double moyenne, §3.2), le recalage des seuils n'en est que le corollaire.

Après validation terrain, ces valeurs deviendront des **paramètres contractuels
par défaut**, ajustables tant que `S_out < S_in` est respecté ; toute modification
sera tracée au changelog Arsenal.

---

## 9. Gestion des cas indisponibles

- Source `unknown` / `unavailable` / non numérique → tendance `indisponible`,
  icône `mdi:thermometer-off`.
- **L'une ou l'autre** des deux fenêtres statistiques (courte ou longue)
  insuffisamment alimentée (moyenne non encore disponible) → tendance
  `indisponible`.
- Aucune valeur de tendance n'est jamais figée en mémoire ni extrapolée : l'état
  d'indisponibilité est **visible et honnête** (cf. `affichage.md`, Invariant 4).
- La famille **ne déclenche aucun fallback** : elle consomme une donnée déjà
  qualifiée et s'abstient si celle-ci est absente.

---

## 10. Observabilité

Chaque capteur de tendance expose, en attributs, de quoi auditer sa décision
**sans recalcul externe** :

- l'écart courant `ecart_axe = moyenne_courte − moyenne_longue` ayant servi à la
  décision ;
- les **deux** moyennes glissantes de référence et les fenêtres `W_court` /
  `W_long` appliquées ;
- les seuils `S_in` / `S_out` effectifs ;
- l'entité source consommée.

Objectif : qu'un audit puisse, à la seule lecture de l'entité, **rejouer
mentalement** la qualification de l'état (auditabilité Arsenal).

---

## 11. Convention de nommage (grammaire vivante — identifiants figés)

Le présent contrat **n'invente aucun identifiant d'entité ni `unique_id`**
(interdiction `contrats/README.md`). La grammaire ci-dessous est **implémentée et
vivante** en runtime (passe tracée au changelog et en §18) :

```text
couche statistique courte :  sensor.temperature_<axe>_moyenne_15_min
couche statistique longue :  sensor.temperature_<axe>_moyenne_60_min
couche d'interprétation   :  sensor.tendance_temperature_<axe>     (axe ∈ {min_chambres, moyenne_maison, max_chambres})
```

La grammaire est **homogène sur les trois axes** : aucun axe n'est un cas
particulier de nommage. Ces identifiants sont ceux du runtime déployé ; toute
modification ultérieure suit la règle générale (aucun renommage sans traçage
changelog).

**Gabarit figé (v1.2, implémenté et vivant).** La couche de projection
introduite en §4.2 est implémentée en runtime (PR #839, commit `9de7993`,
§19) sous la grammaire suivante, homogène avec celle ci-dessus :

```text
couche de projection :  sensor.temperature_<axe>_projection     (axe ∈ {min_chambres, moyenne_maison, max_chambres})
```

Soit, par axe, les trois entités et `unique_id` réellement retenus :

| Axe | Entité | `unique_id` |
|---|---|---|
| `min_chambres` | `sensor.temperature_min_chambres_projection` | `temperature_min_chambres_projection` |
| `moyenne_maison` | `sensor.temperature_moyenne_maison_projection` | `temperature_moyenne_maison_projection` |
| `max_chambres` | `sensor.temperature_max_chambres_projection` | `temperature_max_chambres_projection` |

Ces identifiants sont ceux du runtime déployé ; toute modification ultérieure
suit la règle générale (aucun renommage sans traçage changelog).

---

## 12. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `sensor.temperature_min_chambres` | source agrégée — lue | bloquant (lecture) |
| `sensor.temperature_moyenne_maison` | source agrégée — lue | bloquant (lecture) |
| `sensor.temperature_max_chambres` | source agrégée — lue | bloquant (lecture) |
| Couche de projection statistique ré-échantillonnée (×3, §4.2 — amendement v1.2, §19) | amont dédié des deux couches `statistics` | bloquant |
| Couche statistique courte (moyenne glissante `W_court`, ×3) | référence récente | bloquant |
| Couche statistique longue (moyenne glissante `W_long`, ×3) | référence de fond | bloquant |
| Couche d'interprétation (tendance, ×3) | interface consommable | bloquant |

Consommateur aval **nommé** : la catégorie *Favoris* de l'interface de conduite
Home Assistant (Android Auto), configurée dans l'application compagnon, hors
dépôt.

---

## 13. Recorder

| Population | Doctrine |
|---|---|
| Couche de projection statistique ré-échantillonnée (§4.2 — amendement v1.2, §19) | **Population A obligatoire** (`architecture/01_recorder/contrat.md`) : elle est la **source** de deux capteurs `platform: statistics` actifs (courte et longue) ; sans son historique enregistré, ces fenêtres glissantes ne peuvent pas être reconstruites de façon fiable après redémarrage ou purge. Inclusion recorder **requise**, taguée `# OBLIGATOIRE — contrainte HA`. |
| Couches statistiques (moyennes glissantes courte et longue) | inclusion `recorder` **uniquement** si un graphe historique les consomme ; aucun à ce jour ⇒ ne rien ajouter |
| Couche d'interprétation (tendance) | état catégoriel ; inclusion `recorder` **uniquement** si un historique d'état est explicitement souhaité ; sinon, ne rien ajouter |

Le `recorder` Arsenal fonctionne en liste blanche : aucune entité de cette
famille n'y est ajoutée tant qu'un consommateur historique réel n'est pas nommé
(cf. clause anti-couche-orpheline, INV-TEND-10), **à l'exception de la couche
de projection**, dont l'inclusion est obligatoire par contrainte HA (ligne
ci-dessus) et non discrétionnaire.

**Précision (tick identique sans `force_update`, §4.2).** L'enregistrement
Recorder de la projection suit la mécanique HA standard : seuls les
véritables changements de valeur produisent un `state_changed` et donc une
ligne Recorder ; un tick périodique à valeur identique ne produit qu'un
`state_reported` et **n'est jamais présenté ni traité comme un
`state_changed` artificiel**. La présente famille n'introduit aucun mécanisme
(`force_update` ou autre) visant à forcer l'écriture Recorder sur valeur
identique.

L'inclusion Recorder Population A des trois projections a été réalisée par
la passe runtime tracée en §19 (`recorder.yaml`, PR #839) : les trois
entités de projection y figurent, sans élargissement du périmètre
`recorder.yaml` au-delà de ces trois entités.

---

## 14. Facteur Arsenal

- **Famille homogène** : même logique, même grammaire, mêmes seuils sur les trois
  axes ; factorisable par ancre + dérivation depuis `this.entity_id` (motif déjà
  éprouvé dans le dépôt, cf. `extrema_jour_courant.md` §14).
- **Sans état** : aucune mémoire métier, aucun écrivain souverain, aucune
  automatisation dédiée — les couches statistiques portent le lissage.
- **Réutilisation de l'existant** : motif `statistics`/`mean` déjà présent, motif
  d'icône dynamique « Android Auto » déjà présent (`clim_mode_local`).
- **Aucune couche sans consommateur** : la chaîne s'arrête à l'état réellement
  affiché.

---

## 15. Hors périmètre — exclusions explicites

Il est **interdit**, au titre de ce contrat :

- de calculer la tendance dans la couche UI / carte / Android Auto
  (`affichage.md` : l'UI observe, n'interprète jamais) ;
- de modifier, renommer, réagréger ou réécrire les trois capteurs sources ;
- de relire les capteurs de pièce sous-jacents pour reconstruire un agrégat ;
- de réappliquer une plage de plausibilité sur les sources (autorité amont) ;
- d'utiliser la fenêtre glissante comme source d'un extrême du jour
  (renvoi `extrema_jour_courant.md` §9) ;
- de masquer, figer ou extrapoler une valeur en cas d'indisponibilité ;
- de confier à la tendance une quelconque autorité décisionnelle ou un pilotage
  d'équipement ;
- de créer une couche couleur, historique ou palmarès sans consommateur nommé ;
- de créer un domaine documentaire distinct pour ce besoin (cf. analyse
  architecturale : rattachement météo justifié, nouveau domaine non justifié) ;
- d'utiliser `force_update` dans la couche de projection ou ailleurs dans
  cette famille (§4.2) ;
- d'utiliser le `last_reported` de la couche de projection, ou tout autre
  signal qui en dérive, comme preuve de fraîcheur, de santé ou d'activité de
  la source amont (§4.2, renvoi `resilience_integrations.md` R-ANCRAGE-2 /
  R-AXE1-1) ;
- de brancher un consommateur autre que les deux couches `statistics` de la
  présente famille sur la couche de projection (§4.2, INV-TEND-20) ;
- de faire porter à la couche de projection une mémoire, un TTL, un fallback
  ou une décision métier quelconque (§4.2).

---

## 16. Invariants Arsenal

| ID | Invariant |
|---|---|
| INV-TEND-1 | La tendance est une interprétation backend ; l'UI (dont Android Auto) ne la calcule jamais, elle restitue l'état et l'icône déjà produits. |
| INV-TEND-2 | Le capteur de tendance consomme exclusivement l'agrégat source déjà qualifié ; il ne réagrège pas et ne relit pas les capteurs de pièce. |
| INV-TEND-3 | Les trois capteurs sources ne sont jamais modifiés, renommés ni réécrits par cette famille (lecture seule stricte). |
| INV-TEND-4 | L'état appartient à l'ensemble fermé `{hausse, baisse, stable, indisponible}`. Aucune autre valeur. |
| INV-TEND-5 | Indisponibilité honnête : source non exploitable ou fenêtre insuffisante ⇒ état `indisponible`, jamais masqué ni extrapolé. |
| INV-TEND-6 | La décision repose sur l'**écart entre deux statistiques lissées sur fenêtre** (`moyenne_courte − moyenne_longue`) ; **aucun des deux termes** n'est un échantillon instantané. |
| INV-TEND-7 | Hystérésis obligatoire : seuils d'entrée et de sortie asymétriques (`S_out < S_in`) pour interdire tout scintillement. |
| INV-TEND-8 | À chaque état correspond une et une seule icône, portée par le capteur lui-même, descriptive et non prescriptive. |
| INV-TEND-9 | La famille est homogène sur les trois axes ; aucun axe n'est un cas particulier. |
| INV-TEND-10 | Toute couche exposée a un consommateur réel et nommé ; aucune couche orpheline. |
| INV-TEND-11 | Les fenêtres glissantes servent exclusivement à qualifier une tendance ; elles ne sont jamais source d'un extrême du jour (renvoi `extrema_jour_courant.md` §9 ; usage légitimé §9.3). |
| INV-TEND-12 | La tendance n'a aucune autorité décisionnelle : aucun pilotage d'équipement, aucun déclenchement d'automatisation métier. |
| INV-TEND-13 | La grandeur `valeur_instantanee − moyenne_glissante` (v1.0) est **dépréciée** : elle sature sur les rampes lentes (§3.2). Toute nouvelle implémentation l'interdit ; sa persistance au runtime n'est tolérée que comme **écart temporaire tracé** (§18). |
| INV-TEND-14 | Tout écart entre ce contrat et le runtime doit être **explicitement tracé** (§18 pour l'historique v1.0→v1.1, §19 pour l'historique v1.1→v1.2, résorbé) ; un écart non tracé reste une non-conformité. |
| INV-TEND-15 | La couche de projection (§4.2) recopie **strictement** la valeur instantanée de la source ; elle n'applique aucune transformation, aucun lissage, aucune conversion supplémentaire. |
| INV-TEND-16 | La couche de projection ne porte **aucune mémoire propre** : elle ne conserve, ne restaure ni ne prolonge aucune valeur au-delà de la lecture instantanée de la source ; aucune valeur non numérique n'est jamais prolongée ou extrapolée. |
| INV-TEND-17 | La couche de projection ne déclenche et ne porte **aucun fallback, aucun seuil métier et aucune décision** ; sa disponibilité est strictement dérivée de l'exploitabilité instantanée de la source (§3.3). |
| INV-TEND-18 | La cadence de rafraîchissement périodique de la couche de projection est bornée par la fenêtre courte (`T ≤ W_court / 3` ; valeur candidate actuelle `/5`, §4.2). `force_update` est **interdit**, à quelque titre que ce soit, dans cette famille. |
| INV-TEND-19 | L'événement `state_reported` produit par un tick périodique à valeur identique de la couche de projection est un artefact synthétique d'échantillonnage ; il ne constitue **jamais** une preuve de fraîcheur, de santé ou d'activité de la source amont. La couche de projection est explicitement **hors de tout périmètre de résilience/fraîcheur** (renvoi `resilience_integrations.md` R-ANCRAGE-2, R-AXE1-1). |
| INV-TEND-20 | Le seul consommateur autorisé de la couche de projection est le couple de couches statistiques courte/longue de la présente famille ; aucun autre consommateur ne peut s'y brancher sans amendement contractuel explicite (cf. INV-TEND-10). |

---

## 17. Extensions futures envisagées

- amplitude récente (`max − min` sur fenêtre) en attribut d'observabilité ;
- couche couleur dédiée si un dashboard (hors Android Auto) en exprime le besoin,
  sous contrat séparé et avec consommateur nommé ;
- tendance d'autres grandeurs déjà affichées en conduite (ECS, humidité),
  par réplication du même gabarit, sous décision explicite.

Aucune de ces extensions n'a de valeur normative à ce stade.

---

## 18. Écart contrat ↔ runtime v1.0 → v1.1 — clôture historique

Cette section **trace historiquement** l'écart qui a existé entre la doctrine
v1.1 et le runtime, avant sa résorption. Elle satisfait `INV-TEND-13` et
`INV-TEND-14`. **Cet écart est clos** : le runtime implémente la grandeur v1.1.
§18.3 précise ce que cette clôture **ne couvre pas**.

### 18.1 Nature de l'écart (historique, au moment de l'amendement 2026-06-17)

| Aspect | Contrat v1.1 (cible) | Runtime d'alors (v1.0) |
|---|---|---|
| Grandeur de décision | `moyenne_courte − moyenne_longue` | `valeur_instantanée − moyenne_60_min` |
| Couches statistiques | 2 (courte + longue) | 1 (longue, `..._moyenne_60_min`) |
| Seuils | cibles candidates `S_in≈0,15` / `S_out≈0,08` (à valider) | `S_in=0,4` / `S_out=0,2` |
| Symptôme | — | faux `stable` sur rampes lentes (audit §4) |

### 18.2 Résorption

- L'écart était **connu, documenté et volontaire** : le contrat avait été amené
  **en avance** sur le runtime pour fixer le besoin avant la correction.
- La passe runtime alignant les deux fichiers sur la doctrine v1.1 a été
  exécutée et tracée au changelog (`v16_0_3`) : ajout, par axe, de la
  **moyenne courte** (`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`,
  `sensor.temperature_<axe>_moyenne_15_min`) ; remplacement de la grandeur de
  décision par `moyenne_courte − moyenne_longue` et passage des seuils à
  `S_in=0,15` / `S_out=0,08` (`12_template_sensors/meteo/tendance/temperature.yaml`).
  La moyenne longue existante n'a pas été renommée ; aucune entité source
  modifiée.
- Constat fait à l'occasion de la présente révision (« v1.1 (révision) ») :
  cette résorption runtime n'avait jamais été reportée dans le corps du présent
  contrat — §0, §2.2, §3.2, §11 et §12 continuaient de décrire un écart déjà
  refermé. C'est l'objet de la présente révision : mettre le texte en
  concordance avec un runtime qui, lui, était déjà à jour.

### 18.3 Ce que cette clôture ne couvre pas

La résorption de l'écart de **grandeur** (§18.1-18.2) est **indépendante** de la
validation du **calibrage** des seuils. Le préalable de §8.3 — mesure du
plancher de bruit réel des trois agrégats (audit
[`audit_tendance_temperature_sensibilite.md`](../../audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md)
§9, tests 1–3) — n'a **pas été exécuté**. Le passage en production de
`S_in=0,15` / `S_out=0,08` (changelog `v16_0_3`) a eu lieu **sans** cette
mesure. Cette dette est **distincte** de l'écart clos ci-dessus, reste
**ouverte**, et est tracée en §8.2 : elle n'est **pas** résorbée par la présente
section.

---

## 19. Écart contrat ↔ runtime v1.1 → v1.2 — clôture historique

Cette section **trace historiquement** l'écart qui a existé entre la doctrine
v1.2 et le runtime, avant sa résorption. Elle satisfait `INV-TEND-14`.
**Cet écart est clos** : le runtime implémente la couche de projection
statistique ré-échantillonnée décrite en §4.2. §19.3 précise ce que cette
clôture **ne couvre pas**.

### 19.1 Nature de l'écart (historique, au moment de l'amendement 2026-09-14)

| Aspect | Contrat v1.2 (cible) | Runtime d'alors (avant PR #839) |
|---|---|---|
| Couche de projection statistique ré-échantillonnée (§4.2) | requise, en amont des deux couches `statistics` | absente |
| Source des couches `statistics` courte/longue | la projection (§2.2, §4.1) | la source agrégée directement (`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`) |
| Défaut corrigé | absence de faux `indisponible` sur source stable peu bavarde (§0) | défaut présent : la fenêtre courte peut passer `unknown` alors que la source reste numériquement valide |
| Identifiants de la projection | gabarit non figé (§11) | — (inexistants) |
| Recorder de la projection | Population A obligatoire (§13) | sans objet (entité inexistante) |

### 19.2 Résorption

- L'écart était **connu, documenté et volontaire** : le contrat avait été
  amendé **en avance** sur le runtime (LOT DOC 2, 2026-09-14) pour fixer la
  cible architecturale avant l'implémentation.
- La passe runtime a été exécutée et tracée par la PR #839 (commit
  `9de7993`, LOT R1) : ajout, par axe, des trois trigger-based template
  sensors de projection (`12_template_sensors/meteo/tendance/projection.yaml`
  — `sensor.temperature_min_chambres_projection`,
  `sensor.temperature_moyenne_maison_projection`,
  `sensor.temperature_max_chambres_projection`, §11) ; repointage des six
  couches `statistics` 15/60 min existantes
  (`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`) sur leur
  projection respective (seul le champ `entity_id` modifié ; `unique_id`,
  `name`, `state_characteristic`, `max_age`, `sampling_size` inchangés) ;
  inclusion des trois projections au bloc Recorder Population A
  (`recorder.yaml`, §13). Cadence runtime homogène sur les trois axes :
  `time_pattern: /5` (§4.2). Aucune modification de la couche
  d'interprétation, des seuils `S_in`/`S_out`, des fenêtres
  `W_court`/`W_long`, ni des trois sources métier. `force_update` n'est pas
  utilisé dans ce mécanisme (INV-TEND-18).
- **Validation terrain acquise** sur le SHA candidat exact de la PR, déployé
  sur le `/config` réel avant merge : YAML valide, `ha core check` vert,
  redémarrage HA propre, trois projections numériques et strictement égales
  à leur source, six `statistics` numériques dès le premier report valide,
  trois tendances disponibles et `stable` ; sur les axes `min_chambres` et
  `max_chambres`, un plateau de plus de 15 minutes a montré une valeur de
  projection et un `last_changed`/`last_updated` inchangés tandis que
  `last_reported` avançait toutes les 5 minutes, les `statistics` 15/60 min
  restant numériques et sans aucune bascule `indisponible` ; sur l'axe
  `moyenne_maison`, un changement naturel de la source s'est propagé
  immédiatement à la projection avec un véritable `state_changed` et une
  mise à jour des `statistics`. Aucun défaut bloquant observé. **Aucun test
  de panne réelle n'a été provoqué ni exécuté.**
- Verdict terrain : GO MERGE. PR #839 mergée sur `main` (commit `9de7993`).

### 19.3 Ce que cette clôture ne couvre pas

Cette clôture est **indépendante** :

- de la grandeur de décision `moyenne_courte − moyenne_longue` (§3.2, v1.1,
  résorbée §18) — inchangée par cette clôture ;
- de la dette de validation terrain des seuils `S_in`/`S_out` (§8.2/§8.3) :
  le préalable de mesure du plancher de bruit réel des trois agrégats n'a
  **pas été exécuté** par cette clôture et reste **ouvert et distinct**,
  tracé en §8.2 ; les valeurs `S_in≈0,15`/`S_out≈0,08` ne sont **pas**
  validées par la présente section ;
- du test de panne réelle sur la couche de projection : ce test **n'a pas
  été provoqué ni exécuté** lors de la validation terrain ; seul un
  comportement nominal (plateau, changement naturel de source) a été
  observé. L'absence de ce test n'est ni comblée ni présumée par la présente
  clôture.

Ces dettes sont **distinctes** de l'écart clos ci-dessus et ne sont **pas**
résorbées par la présente section.

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.2 (révision) | 2026-09-14 | **Clôture de l'écart architectural v1.1 → v1.2 (LOT DOC 3).** Aucune doctrine fonctionnelle modifiée. Constat : la couche de projection statistique ré-échantillonnée spécifiée par l'amendement v1.2 (§4.2) a été implémentée en runtime (PR #839, commit `9de7993`, LOT R1) — trois trigger-based template sensors de projection (`sensor.temperature_min_chambres_projection`, `sensor.temperature_moyenne_maison_projection`, `sensor.temperature_max_chambres_projection`, §11, gabarit désormais figé), cadence `time_pattern: /5` (§4.2), sans `force_update` (INV-TEND-18), repointage des six couches `statistics` 15/60 min existantes sur leur projection respective, inclusion Recorder Population A des trois projections (§13). Validation terrain obtenue sur le SHA candidat exact déployé sur `/config` avant merge : YAML valide, `ha core check` vert, redémarrage propre, projections et `statistics` numériques, trois tendances `stable`, comportement de plateau conforme observé sur `min_chambres`/`max_chambres` (>15 min), propagation réelle observée sur `moyenne_maison`, aucun défaut bloquant. **Test de panne réelle non provoqué, non exécuté.** PR #839 mergée sur `main`. §19 transformé en clôture historique (19.1 nature de l'écart, 19.2 résorption, 19.3 ce que la clôture ne couvre pas). Dette de validation terrain des seuils `S_in`/`S_out` (§8.2) **non traitée, non rouverte, reste ouverte et distincte**. Aucun invariant ajouté, retiré ou renuméroté. |
| 1.2 (amendement) | 2026-09-14 | **Amendement architectural — couche de projection statistique ré-échantillonnée (LOT DOC 2).** Constat terrain : `sensor.temperature_moyenne_maison` peut rester numériquement valide plus de 15 min sans regénérer d'échantillon `statistics` courte, faisant passer la tendance à tort en `indisponible` alors que la source est exploitable. Arbitrage : TTL en couche d'interprétation écarté ; ré-échantillonnage dédié retenu. Ajout d'une couche de projection statistique ré-échantillonnée (§2.2, §4.1, §4.2) intercalée entre la source et les deux couches `statistics` existantes — mécanisme trigger-based template sensor (triggers `state`/`time_pattern`/`homeassistant: start`, recopie stricte, `availability` = exploitabilité instantanée de la source), `force_update` explicitement interdit (qualifié contre le schéma YAML HA). Cadence normée `T ≤ W_court / 3`, valeur candidate actuelle `/5` (§4.2) — `W_court`, `W_long`, `S_in`, `S_out` **inchangés** (§8). Exclusion explicite de la projection de tout axe résilience/fraîcheur (`resilience_integrations.md` R-ANCRAGE-2, R-AXE1-1) — **aucune modification de ce contrat de résilience**. Population Recorder A obligatoire précisée pour la projection (§13) — `recorder.yaml` **non modifié** dans ce lot. Gabarit de nomenclature **non figé** proposé pour la projection (§11) — aucun `entity_id` ni `unique_id` créé. Nouveaux invariants `INV-TEND-15` à `INV-TEND-20` (§16), aucun invariant existant renuméroté. Nouvelle section §19 (écart contrat ↔ runtime v1.1 → v1.2, **ouvert**) ; §17/§18 non renumérotés. **Aucune modification runtime dans cette passe.** Dette de validation terrain des seuils (§8.2) **non traitée, non rouverte, non mélangée** à cet amendement. |
| 1.1 (révision) | 2026-09-14 | **Clôture de la dette narrative v1.0 → v1.1 (LOT DOC 1).** Aucune doctrine fonctionnelle modifiée. Constat : la passe runtime alignant les deux fichiers (`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`, `12_template_sensors/meteo/tendance/temperature.yaml`) sur la grandeur `moyenne_courte − moyenne_longue` et les seuils `S_in=0,15`/`S_out=0,08` a déjà eu lieu (changelog `v16_0_3`), mais n'avait jamais été reportée dans le corps du contrat. Correction du statut (en-tête), §0, §2.2, §3.2, §11, §12 : passage du conditionnel/futur (« encore v1.0 », « à créer », « gabarit cible non figé ») au constat (« vivant », « figé »). §18 transformé en section de clôture historique (18.1 nature de l'écart, 18.2 résorption, 18.3 ce que la clôture ne couvre pas). §8.2 précisé : `S_in=0,15`/`S_out=0,08` sont **déployés en runtime** mais **non validés** — la mesure du plancher de bruit (§8.3, audit §9 tests 1–3) n'a pas été exécutée ; dette de validation terrain **conservée ouverte et distincte**, non close par la présente révision. Aucun invariant ajouté, retiré ou renuméroté. Aucune modification runtime dans cette passe. |
| 1.1 | 2026-06-17 | **Amendement doctrinal de la grandeur de décision.** Dépréciation de `valeur_instantanée − moyenne_60_min` (saturation `r × W/2` sur rampes lentes ⇒ faux `stable`, cf. audit `audit_tendance_temperature_sensibilite.md`). Adoption de la grandeur lissée `moyenne_courte − moyenne_longue` (§3.2, §5) ; passage à 2 couches statistiques (§2.2, §4, §12) ; cibles candidates **non figées** `W_long=60`, `W_court≈15`, `S_in≈0,15`, `S_out≈0,08` à valider sur le bruit réel (§8). Invariants : INV-TEND-6 reformulé (écart entre deux statistiques lissées), ajout INV-TEND-13 (grandeur v1.0 dépréciée) et INV-TEND-14 (traçage des écarts). Section §18 « écart temporaire contrat ↔ runtime » ajoutée. **Aucune modification runtime** dans cette passe : le runtime applique encore la v1.0 ; correction reportée à une passe ultérieure (§18.3). Invariants structurants conservés : backend interprète / UI restitue, états fermés, indisponibilité honnête, hystérésis obligatoire, lecture seule des sources, aucune autorité décisionnelle. |
| 1.0 | 2026-06-09 | Promotion en contrat normatif : la famille « tendance thermique des agrégats intérieurs » est implémentée au runtime (couche perception `sensor.temperature_<axe>_moyenne_60_min` — `statistics`/`mean`, fenêtre 60 min ; couche interprétation `sensor.tendance_temperature_<axe>` — trigger template sensors, hystérésis `S_in`=0.4 / `S_out`=0.2, écart arrondi au centième, `time_pattern` 5 min ; ni automatisation ni helper) et conforme aux invariants `INV-TEND-*`. Grammaire de nommage (§11) désormais figée aux valeurs ci-dessus. Cadrage « pré-contrat / avant implémentation » retiré. |
| 0.1.0 | 2026-06-09 | Brouillon pré-normatif initial — formalisation de la famille « tendance thermique des agrégats intérieurs » destinée aux Favoris Android Auto : nature métier (écart instantané vs moyenne glissante), méthode retenue (`statistics`/`mean` + interprétation à bande morte et hystérésis), états fermés, icônes dynamiques, gestion d'indisponibilité, observabilité, exclusions et invariants `INV-TEND-*`. Avant implémentation : aucun identifiant figé, aucune entité existante modifiée. |
