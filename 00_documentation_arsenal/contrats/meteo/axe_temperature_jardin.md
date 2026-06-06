# axe_temperature_jardin.md
# Arsenal — Contrat d'axe : Température jardin
# Version : 1.2
# Statut : normatif
# Dépend de : meteo.md (non versionné), validation.md (non versionné), fallback.md (non versionné)
# Note : les contrats amont ne sont pas versionnés — dette documentaire à solder en v1.2
#
# Delta v1.0 → v1.1
# - §9.1  : reformulation mécanisme TTL (non figé sur time_pattern)
# - §9.2  : ajout garde systeme_stable (publication et seed bloqués si off)
# - §10   : reformulation indicateurs secondaires (sans "obligatoirement")
# - §11.1 : ajout input_boolean.systeme_stable comme dépendance bloquante publication
# - §9.2  : condition mémoire renforcée (plausibilité §4 exigée)
#
# Delta v1.1 → v1.2
# - §8.1  : ajout précondition de qualification de S(t-1) avant tout calcul EWMA
# - §8.5  : ajout nouveau paragraphe — principe de non-assimilation mémoire/qualification
# - §9.2  : écho normatif du principe §8.5 dans le contexte de la continuité

---

## 1. Objet

Définir les règles locales applicables à l'axe température jardin
dans Arsenal.

Cet axe couvre la température extérieure du domicile, zone jardin.
Il ne couvre pas la température extérieure d'autres zones
(ex : imprimerie). Chaque zone fait l'objet d'un contrat d'axe distinct.

Ce contrat ne redéfinit ni la validation des sources ni le mécanisme
général de fallback. Il précise :

- les sources prises en compte sur cet axe
- la règle locale de détection de divergence haute
- la règle locale de construction de la cible robuste
- la règle locale de stabilisation de la valeur publiée
- les statuts diagnostiques associés

Cet axe vise une publication :

- stable dans le temps
- robuste aux biais chauds liés à l'exposition
- exploitable par des logiques métier
- sans saut artificiel dû à un changement de capteur

---

## 2. Sources déclarées

| Rôle   | Entité                       | Technologie     | Exposition       | Statut qualification     |
|--------|------------------------------|-----------------|------------------|--------------------------|
| Source | sensor.temperature_jardin_1  | Netatmo/HomeKit | Nord-Ouest       | qualifiée                |
| Source | sensor.temperature_jardin_2  | Netatmo/HomeKit | Sud-Est          | qualifiée                |
| Source | sensor.temperature_jardin_3  | SwitchBot/BT    | Non caractérisée | intégrée sous contrainte |

Aucune source n'est déclarée primaire ou secours.
Les trois sources sont admissibles à la fusion sur cet axe,
sous réserve de validation et des règles locales définies
dans le présent contrat.

Une source est considérée comme valide exclusivement selon
les règles définies dans validation.md.
Aucune logique de validation n'est redéfinie ici.

### 2.1 Note sur la source 3

L'exposition de sensor.temperature_jardin_3 n'est pas caractérisée
de manière formelle.

Son inclusion est autorisée car les mécanismes de détection de
divergence haute garantissent qu'elle ne peut pas influencer
la cible robuste en cas de comportement aberrant.

La caractérisation formelle de son exposition sera nécessaire
avant toute évolution future vers un modèle hiérarchisé
ou une source canonique unique.

---

## 3. Risque principal couvert

Le risque principal couvert par ce contrat est la publication
d'une température artificiellement trop élevée du fait d'un
biais d'exposition locale ou de rayonnement.

En conséquence, la fusion sur cet axe n'est pas symétrique :
une divergence vers le haut est traitée comme un risque
spécifique et conduit à l'exclusion de la source concernée
de la cible publiée pour le cycle courant.

Cette asymétrie ne constitue pas une préférence générale
pour les valeurs basses. Elle constitue une protection
défensive contre un biais chaud manifestement divergent,
justifiée par la nature physique du risque d'exposition.

---

## 4. Plage de plausibilité

| Borne   | Valeur |
|---------|--------|
| Minimum | -10 °C |
| Maximum | +50 °C |

Toute valeur hors de cette plage est invalide au sens
de validation.md, même si elle est techniquement lisible.

La vérification de plausibilité est déléguée à validation.md
et n'est pas réimplémentée dans le présent contrat.

---

## 5. Paramètres locaux

| Paramètre    | Valeur de référence | Plage admissible | Gouvernance       |
|--------------|---------------------|------------------|-------------------|
| δ_suspect    | 1.5 °C              | [1.0 – 2.5] °C   | révision annuelle |
| δ_coherence  | 1.2 °C              | [0.8 – 2.0] °C   | révision annuelle |
| α_EWMA       | 0.3                 | [0.2 – 0.5]      | révision annuelle |
| δ_max        | 0.5 °C / cycle      | [0.3 – 1.0] °C   | révision annuelle |
| TTL_effectif | 30 minutes          | non modifiable   | contractuel fixe  |

### 5.1 Justification des valeurs de référence

- **δ_suspect = 1.5 °C** : en dessous de ce seuil, la divergence n'est
  pas considérée comme suffisamment probante pour justifier une exclusion
  structurelle pour biais chaud. Ce seuil définit une frontière
  décisionnelle, pas une attribution de cause.

- **δ_coherence = 1.2 °C** : en dessous de ce seuil, deux capteurs sont
  considérés comme mesurant le même phénomène. Au-dessus, leur moyenne
  serait ininterprétable.

- **α_EWMA = 0.3** : réactivité modérée. Un événement thermique réel
  (front froid, nuit tombante) atteint 95 % de son impact en environ
  8–9 cycles. Une valeur plus basse (0.2) lisse davantage mais retarde
  les décisions d'automatisme. Une valeur plus haute (0.5) réduit la
  stabilisation.

- **δ_max = 0.5 °C / cycle** : interdit tout saut brusque visible en
  publication quelle qu'en soit la cause, y compris un changement brutal
  du nombre de sources disponibles.

### 5.2 Règles de gouvernance des paramètres

- Toute modification d'un paramètre déclenche une montée de version mineure.
- Aucune adaptation automatique des paramètres n'est autorisée.
- Les valeurs effectives utilisées en implémentation doivent être
  documentées et rester dans les plages admissibles déclarées ci-dessus.
- α_EWMA et δ_max peuvent être renseignés comme helpers dédiés
  en implémentation Home Assistant.
- `input_boolean.systeme_stable` est un composant Arsenal transverse.
  Sa valeur n'est pas un paramètre de cet axe et ne peut pas être
  surchargée localement.

---

## 6. Détection de divergence haute

### 6.1 Périmètre d'application

La détection s'applique exclusivement aux sources valides
au sens de validation.md pour le cycle courant.
Une source invalide est déjà exclue avant cette étape.

### 6.2 Référence de divergence

La référence de divergence est la médiane des valeurs
des sources valides pour le cycle courant.

En cas de nombre pair de sources valides, la médiane
est la moyenne des deux valeurs centrales.

### 6.3 Règle de suspicion chaude

Toute source valide dont la valeur est strictement supérieure à :

```
médiane_sources_valides + δ_suspect
```

est déclarée `suspect_chaud` pour le cycle courant.

Une source `suspect_chaud` est exclue de la construction
de la cible robuste. Elle n'est pas pondérée ni atténuée :
elle est retirée du calcul pour le cycle courant.

### 6.4 Portée et non-persistance

Le statut `suspect_chaud` :

- est purement local au cycle courant
- n'invalide pas la source au sens de validation.md
- n'interdit pas son retour automatique dans un cycle ultérieur
  si la condition de divergence n'est plus présente
- ne déclenche aucune alarme ni blocage

---

## 7. Construction de la cible robuste

La cible robuste est construite à partir des sources :

- valides au sens de validation.md
- non déclarées `suspect_chaud` à l'étape §6

### 7.1 Cas nominal — au moins 2 sources retenues

Les sources retenues sont triées par ordre croissant.

Soient `v1` ≤ `v2` ≤ ... les valeurs retenues.

Seules `v1` et `v2` sont utilisées dans les règles suivantes.

#### 7.1.1 Cas cohérent

Si :

```
|v2 - v1| <= δ_coherence
```

alors :

```
cible_robuste = (v1 + v2) / 2
```

#### 7.1.2 Cas incohérence retenue

Si :

```
|v2 - v1| > δ_coherence
```

alors `v1` et `v2` sont considérées incohérentes entre elles.
Ne pas les moyenner.

La cible robuste vaut alors la médiane de l'ensemble
des sources retenues (toutes, pas seulement v1 et v2).

**Cas particulier N=2** : si le nombre de sources retenues est
exactement 2, la médiane d'un ensemble de 2 valeurs est leur
moyenne — ce §7.1.2 produit donc le même résultat numérique
que §7.1.1. Cela est intentionnel : avec exactement 2 sources
retenues et incohérentes entre elles, aucune règle interne au
présent contrat ne permet d'identifier la source correcte.
La moyenne est retenue comme estimateur par défaut en absence
d'information discriminante. La publication est maintenue par
continuité de service, avec un statut explicitement dégradé
sur le plan de la fiabilité.
Le statut `incoherence_retenue` est néanmoins publié pour signaler
l'anomalie à l'observabilité.

Ce cas porte le statut diagnostique `incoherence_retenue`.

### 7.2 Cas dégradé — une seule source retenue

Si une seule source est retenue après exclusion des
sources invalides et `suspect_chaud`, la cible robuste
vaut la valeur de cette source unique.

Ce cas porte le statut diagnostique `degrade`.

### 7.3 Absence de cible robuste

Si aucune source n'est retenue, aucune cible robuste
instantanée n'est produite.

L'axe bascule vers le mécanisme de continuité défini au §9.

---

## 8. Stabilisation de la publication

La cible robuste ne doit jamais être publiée directement.
Une stabilisation temporelle est obligatoire à chaque cycle.

### 8.1 Filtrage EWMA

La valeur publiée résulte d'un filtrage exponentiel :

```
S(t) = S(t-1) + α_EWMA × (cible(t) - S(t-1))
```

`S(t-1)` est l'état interne du filtre au cycle précédent,
maintenu en mémoire persistante entre cycles.

**Précondition obligatoire :** avant tout calcul EWMA, l'état
interne `S(t-1)` doit être explicitement qualifié : valeur
numérique présente, dans la plage de plausibilité §4.

Si cette précondition n'est pas satisfaite, aucun calcul EWMA
n'est effectué pour le cycle courant. L'axe bascule vers le
mécanisme de continuité défini au §9.

### 8.2 Priorité de δ_max sur EWMA

La variation effectivement publiée entre deux cycles successifs
est bornée par δ_max :

```
|S_publie(t) - S_publie(t-1)| <= δ_max
```

δ_max est prioritaire sur EWMA.
EWMA propose une cible interne.
δ_max borne la variation publiée.

### 8.3 Report résiduel — règle critique

En cas de limitation par δ_max, la différence résiduelle
entre la cible EWMA théorique et la valeur effectivement publiée
n'est pas abandonnée.

Elle est reportée au cycle suivant via l'état interne S(t-1),
qui doit refléter la valeur réellement publiée, pas la cible EWMA.

Formellement :

```
S_interne(t) = S_publie(t)    [et non S_interne(t) = S_ewma_theorique(t)]
```

Toute implémentation qui écrête sans maintenir cette continuité
d'état introduit une dette silencieuse susceptible de produire
un saut différé. Une telle implémentation est non conforme
au présent contrat.

### 8.4 Reprise après période de mémoire

En cas de reprise après une période sans cible robuste,
l'écart entre la valeur publiée (issue de la mémoire de
continuité) et la nouvelle cible robuste peut être important.

Le mécanisme EWMA reste applicable sans reset, afin de
préserver la continuité de série. Le rattrapage s'effectue
progressivement sur les cycles suivants, borné par δ_max.

Aucun reset de l'état interne n'est autorisé, même après
une longue période de mémoire.

### 8.5 Non-assimilation mémoire restaurée / état qualifié

La restauration d'un état persistant (par exemple via le
mécanisme restore_state de Home Assistant) ne constitue pas
en elle-même une qualification métier de cet état.

Un état restauré doit satisfaire la précondition §8.1 —
valeur numérique présente, dans la plage de plausibilité §4 —
avant d'être utilisé comme base de calcul EWMA.

Cette règle s'applique indépendamment de l'état du flag
`pipeline_initialise` : l'initialisation historique du pipeline
ne certifie pas la validité de l'état interne pour le cycle courant.

---

## 9. Continuité et abstention

La mémoire de continuité est autorisée pour cet axe.

| Niveau | Condition                                            | Valeur publiée             | Statut    |
|--------|------------------------------------------------------|----------------------------|-----------|
| 1      | Cible robuste disponible                             | Valeur stabilisée §8       | cf. §10   |
| 2      | Aucune cible robuste, âge mémoire ≤ TTL_effectif     | Dernière valeur stabilisée | `memoire` |
| 3      | Aucune cible robuste, âge mémoire > TTL_effectif     | `unknown`                  | `inconnu` |

### 9.1 Contrainte d'implémentation

Toute implémentation de cet axe doit embarquer un mécanisme
de réévaluation temporelle permettant l'expiration effective
du TTL, indépendamment des changements d'état des sources.

En Home Assistant, ce mécanisme peut prendre la forme d'un
trigger `time_pattern`, d'un timer dédié, ou de tout autre
dispositif garantissant une réévaluation périodique de période
inférieure ou égale à TTL_effectif / 2.

L'absence de mécanisme temporel conforme rend l'implémentation
non conforme au présent contrat, indépendamment de la correction
des autres règles.

### 9.2 Garde de stabilité système

L'axe ne peut ni initialiser un nouvel état ni publier une valeur
calculée tant que `input_boolean.systeme_stable` n'est pas `on`.

Tant que cette condition n'est pas satisfaite, seules les règles
de continuité s'appliquent :

- si un état persistant existe, est numérique, respecte la plage de
  plausibilité §4, et que son âge est inférieur ou égal à TTL_effectif :
  publication de la mémoire de continuité
- sinon : abstention (`unknown`)

La restauration d'un état persistant ne constitue pas en elle-même
une qualification de cet état au sens du présent paragraphe.
Les conditions ci-dessus — numérique, plausible §4, âge ≤ TTL —
doivent être vérifiées explicitement avant toute publication
en mode continuité.

Cette garde est transverse à l'axe. Elle ne modifie ni la fusion
ni la détection : les couches 1 à 3 continuent de calculer
normalement. Elle bloque uniquement la publication (couche 5)
et le seed initial (couche 4).

Justification : au redémarrage de Home Assistant, les intégrations
sources (HomeKit, Bluetooth) peuvent ne pas être encore stables
au moment où le pipeline calcule sa première cible robuste.
Un seed sur une cible partiellement valide produirait un état
initial incorrect difficile à détecter.

---

## 10. Statuts diagnostiques

L'axe expose un statut global unique à chaque cycle,
complété par des indicateurs secondaires destinés à
l'observabilité fine.

Le statut global ne constitue pas à lui seul une vue exhaustive
des anomalies locales. Lorsqu'ils sont exposés, les indicateurs
secondaires complètent l'analyse diagnostique.

### 10.1 Table des statuts globaux

| Statut                | Signification                                                       |
|-----------------------|---------------------------------------------------------------------|
| `nominal`             | Fusion normale, aucune anomalie locale détectée                     |
| `suspect_chaud`       | Au moins une source exclue pour divergence haute — fusion active    |
| `incoherence_retenue` | Sources retenues incohérentes entre elles — fusion active           |
| `degrade`             | Une seule source disponible après exclusions                        |
| `memoire`             | Publication issue de la mémoire de continuité                       |
| `inconnu`             | Aucune publication disponible — mémoire expirée ou absente          |

### 10.2 Priorité des statuts

En cas de coexistence de plusieurs conditions au même cycle,
le statut publié est celui de plus haute priorité :

| Priorité | Statut                |
|----------|-----------------------|
| 1 (max)  | `inconnu`             |
| 2        | `memoire`             |
| 3        | `degrade`             |
| 4        | `incoherence_retenue` |
| 5        | `suspect_chaud`       |
| 6 (min)  | `nominal`             |

### 10.3 Indicateurs diagnostiques secondaires

Le statut global unique peut masquer des anomalies actives
de moindre priorité. Par exemple, une source `suspect_chaud`
active lors d'un cycle `degrade` n'est pas visible dans le
statut global.

Des indicateurs diagnostiques secondaires peuvent être exposés
en complément :

- nombre de sources valides au cycle courant
- nombre de sources exclues pour `suspect_chaud` au cycle courant
- présence d'une `incoherence_retenue` active

Ces indicateurs n'ont pas de rôle décisionnel. Ils sont destinés
exclusivement à l'observabilité et au diagnostic.
Leur implémentation est recommandée mais non obligatoire en v1.0.

### 10.4 Interprétation des statuts

- `suspect_chaud` (priorité 5) n'est pas un état bénin.
  Il signale une anomalie active sur une source. Sa position
  basse dans la priorité signifie uniquement que les états de
  dégradation plus graves le masquent — pas qu'il soit négligeable.
  Il doit être surveillé via les indicateurs secondaires §10.3.

- `incoherence_retenue` (priorité 4) signale que les sources
  retenues sont incohérentes entre elles. La publication continue
  mais la cible robuste est considérée comme faiblement fiable.

- `degrade` (priorité 3) signale qu'une seule source porte l'axe.
  Il recouvre deux cas distincts non discriminés par le statut global :
  sources absentes pour cause d'invalidité, ou sources exclues pour
  `suspect_chaud`. Les indicateurs secondaires §10.3 permettent
  de discriminer ces cas si exposés.
  La rupture de la source unique provoquerait un basculement direct
  en `memoire`.

- `memoire` (priorité 2) signale que la valeur publiée n'est plus
  issue d'une mesure instantanée.

- `inconnu` (priorité 1) est le seul statut qui interdit toute
  logique métier dépendante de cet axe.

---

## 11. Dépendances

### 11.1 Dépendances fonctionnelles

| Contrat / Composant                  | Rôle                                           | Caractère              |
|--------------------------------------|------------------------------------------------|------------------------|
| validation.md                | Validation des sources amont                   | **bloquant**           |
| fallback.md                  | Mécanisme TTL et mémoire de continuité         | fonctionnel            |
| meteo.md                     | Cadre du domaine météo/climat                  | cadre                  |
| input_boolean.systeme_stable         | Garde de stabilité système pour la publication | **bloquant publication** |

### 11.2 Note sur le caractère bloquant de validation.md

Si validation.md est absent, mal implémenté ou incohérent,
le présent contrat est sans fondation : la distinction
valide / invalide est indéfinie et toutes les règles de fusion
perdent leur sens.

L'implémentation de cet axe est conditionnée à l'existence
et à la conformité de validation.md.

### 11.3 Avertissement d'implémentation — séparation des couches

Les quatre couches du pipeline (validation, détection, fusion,
stabilisation) doivent rester strictement séparées en implémentation.

En Home Assistant, toute dépendance circulaire entre templates
issues d'un mélange de ces couches invalide les garanties
du présent contrat. La validation relève exclusivement de
validation.md et ne doit pas être réimplémentée
dans les composants de fusion ou de stabilisation.

---

## 12. Unité et arrondi

| Paramètre | Valeur |
|-----------|--------|
| Unité     | °C     |
| Arrondi   | 0.1 °C |

L'arrondi s'applique à la valeur publiée finale uniquement.
Tous les calculs intermédiaires (médiane, EWMA, cible robuste)
sont effectués en précision native.

---

## 13. Renvois contractuels

- Cadre du domaine    → `meteo.md`
- Validation sources  → `contrat_v