# contrat_axe_humidite_relative_jardin.md
# Arsenal — Contrat d'axe : Humidité relative jardin
# Version : 1.0
# Statut : normatif
# Dépend de : contrat_meteo.md (non versionné), contrat_validation.md (non versionné), contrat_fallback.md (non versionné)
# Note : les contrats amont ne sont pas versionnés en v1.0 — dette documentaire à solder en v1.1

---

## 1. Objet

Définir les règles locales applicables à l'axe humidité relative jardin
dans Arsenal.

Cet axe couvre l'humidité relative extérieure du domicile, zone jardin.
Il ne couvre pas l'humidité relative d'autres zones (ex : imprimerie).
Chaque zone fait l'objet d'un contrat d'axe distinct.

Ce contrat ne redéfinit ni la validation des sources ni le mécanisme
général de fallback. Il précise :

- les sources prises en compte sur cet axe
- la règle locale de détection d'outlier symétrique
- la règle locale de construction de la cible robuste
- la règle locale de stabilisation de la valeur publiée
- les statuts diagnostiques associés

Cet axe vise une publication :

- stable dans le temps
- robuste aux outliers bilatéraux (dérive haute et basse)
- exploitable par des logiques métier
- sans saut artificiel dû à un changement de capteur

---

## 2. Sources déclarées

| Rôle   | Entité                   | Technologie     | Exposition       | Statut qualification     |
|--------|--------------------------|-----------------|------------------|--------------------------|
| Source | sensor.humidite_jardin_1 | Netatmo/HomeKit | Nord-Ouest       | qualifiée                |
| Source | sensor.humidite_jardin_2 | Netatmo/HomeKit | Sud-Est          | qualifiée                |
| Source | sensor.humidite_jardin_3 | SwitchBot/BT    | Non caractérisée | intégrée sous contrainte |

Aucune source n'est déclarée primaire ou secours.
Les trois sources sont admissibles à la fusion sur cet axe,
sous réserve de validation et des règles locales définies
dans le présent contrat.

Une source est considérée comme valide exclusivement selon
les règles définies dans contrat_validation.md.
Aucune logique de validation n'est redéfinie ici.

### 2.1 Note sur la source 3

L'exposition de sensor.humidite_jardin_3 n'est pas caractérisée
de manière formelle.

Son inclusion est autorisée car les mécanismes de détection
d'outlier symétrique garantissent qu'elle ne peut pas influencer
la cible robuste en cas de comportement aberrant, dans quelque
direction que ce soit.

La caractérisation formelle de son exposition sera nécessaire
avant toute évolution future vers un modèle hiérarchisé
ou une source canonique unique.

---

## 3. Risque principal couvert

Le risque principal couvert par ce contrat est la publication
d'une humidité relative affectée par un capteur outlier,
déviant de manière significative par rapport aux autres sources,
dans un sens comme dans l'autre.

Contrairement à l'axe température jardin, il n'existe pas de
vecteur de biais dominant et stable pour l'humidité relative :

- un capteur échauffé localement peut produire une HR basse
- un capteur exposé à la condensation ou au brouillard local
  peut produire une HR haute

En conséquence, la fusion sur cet axe est symétrique :
toute source s'écartant de la médiane au-delà de δ_hr_suspect
est exclue de la cible publiée, quelle que soit la direction
de l'écart.

---

## 4. Plage de plausibilité

| Borne   | Valeur   |
|---------|----------|
| Minimum | -1 % HR  |
| Maximum | 101 % HR |

La borne inférieure à -1 et la borne supérieure à 101 permettent
d'absorber les légères dérives de mesure des capteurs tout en
éliminant les valeurs grossièrement aberrantes.

La valeur 100 % HR est physiquement valide (brouillard, rosée,
condensation matinale sur capteur extérieur) et doit être acceptée.

Toute valeur hors de cette plage est invalide au sens
de contrat_validation.md, même si elle est techniquement lisible.

La vérification de plausibilité est déléguée à contrat_validation.md
et n'est pas réimplémentée dans le présent contrat.

---

## 5. Paramètres locaux

| Paramètre      | Valeur de référence | Plage admissible | Gouvernance       |
|----------------|---------------------|------------------|-------------------|
| δ_hr_suspect   | 6 % HR              | [4 – 10] % HR    | révision annuelle |
| δ_hr_coherence | 5 % HR              | [3 – 8] % HR     | révision annuelle |
| α_EWMA         | 0.3                 | [0.2 – 0.5]      | révision annuelle |
| δ_max          | 1.0 % HR / cycle    | [0.5 – 3.0] % HR | révision annuelle |
| TTL_effectif   | 30 minutes          | non modifiable   | contractuel fixe  |

### 5.1 Justification des valeurs de référence

- **δ_hr_suspect = 6 % HR** : au-dessus du bruit normal des capteurs
  grand public (±3–5 % HR), en dessous des écarts caractéristiques
  d'un vrai outlier (8–10 % HR). Ce seuil définit une frontière
  décisionnelle, pas une attribution de cause. L'exclusion est
  symétrique : elle s'applique aussi bien à une source anormalement
  haute qu'à une source anormalement basse.

- **δ_hr_coherence = 5 % HR** : légèrement inférieur à δ_hr_suspect
  afin de ne pas être redondant. Deux sources ayant passé le filtre
  outlier peuvent encore présenter un écart naturel de 4–5 % sans
  incohérence. Au-delà, leur moyenne serait ininterprétable.

- **α_EWMA = 0.3** : identique à l'axe température. L'humidité relative
  évolue plus lentement que la température, ce qui rend un α légèrement
  plus bas envisageable. Valeur conservée identique en v1.0 pour
  cohérence système ; révisable sur observation terrain.

- **δ_max = 1.0 % HR / cycle** : variation publiée maximale par cycle.
  Plus souple que pour la température (0.5 °C) car l'humidité relative
  peut légitimement varier plus rapidement en conditions extérieures
  (pluie, brouillard, vent). Interdit néanmoins tout saut artificiel.

### 5.2 Règles de gouvernance des paramètres

- Toute modification d'un paramètre déclenche une montée de version mineure.
- Aucune adaptation automatique des paramètres n'est autorisée.
- Les valeurs effectives utilisées en implémentation doivent être
  documentées et rester dans les plages admissibles déclarées ci-dessus.
- α_EWMA et δ_max peuvent être renseignés comme helpers dédiés
  en implémentation Home Assistant.

---

## 6. Détection d'outlier symétrique

### 6.1 Périmètre d'application

La détection s'applique exclusivement aux sources valides
au sens de contrat_validation.md pour le cycle courant.
Une source invalide est déjà exclue avant cette étape.

### 6.2 Référence de détection

La référence est la médiane des valeurs des sources valides
pour le cycle courant.

En cas de nombre pair de sources valides, la médiane
est la moyenne des deux valeurs centrales.

### 6.3 Règle d'outlier symétrique

Toute source valide dont la valeur s'écarte de la médiane
de plus de δ_hr_suspect, dans un sens comme dans l'autre :

```
|source - médiane_sources_valides| > δ_hr_suspect
```

est déclarée `suspect_hr` pour le cycle courant.

Une source `suspect_hr` est exclue de la construction
de la cible robuste. Elle n'est pas pondérée ni atténuée :
elle est retirée du calcul pour le cycle courant.

**Différence fondamentale avec l'axe température** : l'exclusion
est bilatérale. Une source anormalement basse est exclue
au même titre qu'une source anormalement haute.

### 6.4 Portée et non-persistance

Le statut `suspect_hr` :

- est purement local au cycle courant
- n'invalide pas la source au sens de contrat_validation.md
- n'interdit pas son retour automatique dans un cycle ultérieur
  si la condition d'outlier n'est plus présente
- ne déclenche aucune alarme ni blocage

---

## 7. Construction de la cible robuste

La cible robuste est construite à partir des sources :

- valides au sens de contrat_validation.md
- non déclarées `suspect_hr` à l'étape §6

### 7.1 Cas nominal — au moins 2 sources retenues

Les sources retenues sont triées par ordre croissant.

Soient `v1` ≤ `v2` ≤ ... les valeurs retenues.

La règle de cohérence locale s'applique volontairement aux
deux plus petites valeurs retenues (`v1`, `v2`), et non
aux deux valeurs centrales. Ce choix privilégie la stabilité
et la simplicité contractuelle sur l'optimalité statistique.

Le test de cohérence est effectué sur `v1` et `v2` uniquement,
quelle que soit la taille de la liste retenue.

**Note de choix architectural** : restreindre le test à `v1` et `v2`
est un choix de robustesse sur précision. En cas de N=3 sources
retenues cohérentes (ex : 60/62/64), `v3` n'est pas intégrée dans
le calcul de la cible. Ce choix simplifie la règle de fusion,
la rend indépendante du nombre de sources retenues au-delà de 2,
et évite qu'une troisième source légèrement plus élevée n'introduise
un biais résiduel. La perte de précision est acceptée comme
contrepartie de la robustesse.

#### 7.1.1 Cas cohérent

Si :

```
|v2 - v1| <= δ_hr_coherence
```

alors :

```
cible_robuste = (v1 + v2) / 2
```

#### 7.1.2 Cas incohérence retenue

Si :

```
|v2 - v1| > δ_hr_coherence
```

alors `v1` et `v2` sont considérées incohérentes entre elles.
Ne pas les moyenner selon la règle nominale §7.1.1.

La cible robuste vaut alors la médiane de l'ensemble
des sources retenues.

Avec exactement 2 sources retenues, cette médiane est égale
à leur moyenne. La publication est maintenue par continuité
de service, mais porte obligatoirement le statut
`incoherence_retenue`, car aucune règle interne au présent
contrat ne permet d'identifier la source correcte.

Ce cas porte le statut diagnostique `incoherence_retenue`.

### 7.2 Cas dégradé — une seule source retenue

Si une seule source est retenue après exclusion des
sources invalides et `suspect_hr`, la cible robuste
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

---

## 9. Continuité et abstention

La mémoire de continuité est autorisée pour cet axe.

| Niveau | Condition                                        | Valeur publiée             | Statut    |
|--------|--------------------------------------------------|----------------------------|-----------|
| 1      | Cible robuste disponible                         | Valeur stabilisée §8       | cf. §10   |
| 2      | Aucune cible robuste, âge mémoire ≤ TTL_effectif | Dernière valeur stabilisée | `memoire` |
| 3      | Aucune cible robuste, âge mémoire > TTL_effectif | `unknown`                  | `inconnu` |

### 9.1 Contrainte d'implémentation

Toute implémentation de cet axe doit embarquer un mécanisme
de réévaluation temporelle permettant l'expiration effective
du TTL, indépendamment des changements d'état des sources.

En Home Assistant, ce mécanisme peut prendre la forme d'un
trigger `time_pattern`, d'un timer dédié, ou de tout autre
dispositif garantissant de manière démontrable une réévaluation
périodique de période inférieure ou égale à TTL_effectif / 2,
y compris en l'absence de tout changement d'état des sources.

L'absence de mécanisme temporel conforme rend l'implémentation
non conforme au présent contrat, indépendamment de la correction
des autres règles.

---

## 10. Statuts diagnostiques

L'axe expose un statut global unique à chaque cycle,
complété par des indicateurs secondaires destinés à
l'observabilité fine.

Le statut global ne constitue pas à lui seul une vue exhaustive
des anomalies locales. Lorsqu'ils sont exposés, les indicateurs
secondaires complètent l'analyse diagnostique.

### 10.1 Table des statuts globaux

| Statut                | Signification                                                      |
|-----------------------|--------------------------------------------------------------------|
| `nominal`             | Fusion normale, aucune anomalie locale détectée                    |
| `suspect_hr`          | Au moins une source exclue pour outlier symétrique — fusion active |
| `incoherence_retenue` | Sources retenues incohérentes entre elles — fusion active          |
| `degrade`             | Une seule source disponible après exclusions                       |
| `memoire`             | Publication issue de la mémoire de continuité                      |
| `inconnu`             | Aucune publication disponible — mémoire expirée ou absente         |

### 10.2 Priorité des statuts

En cas de coexistence de plusieurs conditions au même cycle,
le statut publié est celui de plus haute priorité :

| Priorité | Statut                |
|----------|-----------------------|
| 1 (max)  | `inconnu`             |
| 2        | `memoire`             |
| 3        | `degrade`             |
| 4        | `incoherence_retenue` |
| 5        | `suspect_hr`          |
| 6 (min)  | `nominal`             |

### 10.3 Indicateurs diagnostiques secondaires

Des indicateurs diagnostiques secondaires peuvent être exposés
en complément du statut global :

- nombre de sources valides au cycle courant
- nombre de sources exclues pour `suspect_hr` au cycle courant
- présence d'une `incoherence_retenue` active

Ces indicateurs n'ont pas de rôle décisionnel. Ils sont destinés
exclusivement à l'observabilité et au diagnostic.
Leur implémentation est recommandée mais non obligatoire en v1.0.

### 10.4 Interprétation des statuts

- `suspect_hr` (priorité 5) signale une anomalie active sur une
  source, dans un sens comme dans l'autre. Sa position basse dans
  la priorité signifie uniquement que les états de dégradation plus
  graves le masquent — pas qu'il soit négligeable. Il doit être
  surveillé via les indicateurs secondaires §10.3.

- Le statut global ne garantit pas la visibilité de toutes les
  anomalies locales. En particulier, une exclusion `suspect_hr`
  peut être masquée par un statut global `degrade`, `memoire`
  ou `inconnu`.

- `incoherence_retenue` (priorité 4) signale que les sources
  retenues sont incohérentes entre elles. La publication continue
  mais la cible robuste est considérée comme faiblement fiable.

- `degrade` (priorité 3) signale qu'une seule source porte l'axe.
  Il recouvre deux cas distincts non discriminés par le statut global :
  sources absentes pour cause d'invalidité, ou sources exclues pour
  `suspect_hr`. Les indicateurs secondaires §10.3 permettent de
  discriminer ces cas si exposés. La rupture de la source unique
  provoquerait un basculement direct en `memoire`.

- `memoire` (priorité 2) signale que la valeur publiée n'est plus
  issue d'une mesure instantanée.

- `inconnu` (priorité 1) est le seul statut qui interdit toute
  logique métier dépendante de cet axe.

---

## 11. Dépendances

### 11.1 Dépendances fonctionnelles

| Contrat               | Rôle                                   | Caractère    |
|-----------------------|----------------------------------------|--------------|
| contrat_validation.md | Validation des sources amont           | **bloquant** |
| contrat_fallback.md   | Mécanisme TTL et mémoire de continuité | fonctionnel  |
| contrat_meteo.md      | Cadre du domaine météo/climat          | cadre        |

### 11.2 Note sur le caractère bloquant de contrat_validation.md

Si contrat_validation.md est absent, mal implémenté ou incohérent,
le présent contrat est sans fondation : la distinction
valide / invalide est indéfinie et toutes les règles de fusion
perdent leur sens.

L'implémentation de cet axe est conditionnée à l'existence
et à la conformité de contrat_validation.md.

### 11.3 Avertissement d'implémentation — séparation des couches

Les quatre couches du pipeline (validation, détection, fusion,
stabilisation) doivent rester strictement séparées en implémentation.

En Home Assistant, toute dépendance circulaire entre templates
issues d'un mélange de ces couches invalide les garanties
du présent contrat. La validation relève exclusivement de
contrat_validation.md et ne doit pas être réimplémentée
dans les composants de fusion ou de stabilisation.

---

## 12. Unité et arrondi

| Paramètre | Valeur |
|-----------|--------|
| Unité     | % HR   |
| Arrondi   | 1 % HR |

L'arrondi s'applique à la valeur publiée finale uniquement.
Tous les calculs intermédiaires (médiane, EWMA, cible robuste)
sont effectués en précision native.

L'arrondi à 1 % HR est cohérent avec la précision réelle
des capteurs grand public utilisés sur cet axe. Un arrondi à
0.1 % serait une fausse précision.

---

## 13. Renvois contractuels

- Cadre du domaine    → `contrat_meteo.md`
- Validation sources  → `contrat_validation.md`
- Continuité/fallback → `contrat_fallback.md`
- Axe lié             → `contrat_axe_temperature_jardin.md`

---

## 14. Relation avec l'axe température jardin

Les deux axes partagent les mêmes capteurs physiques.
Leurs pipelines sont indépendants et ne se croisent pas.

La différence doctrinale fondamentale est la suivante :

| Axe                | Type de risque    | Logique de fusion     |
|--------------------|-------------------|-----------------------|
| Température jardin | Biais unilatéral  | Exclusion asymétrique |
| Humidité relative  | Outlier bilatéral | Exclusion symétrique  |

Cette différence est intentionnelle et justifiée par la physique
des grandeurs mesurées. Elle ne constitue pas une incohérence
architecturale.

---

## 15. Note d'évolution

La présente version introduit une fusion locale symétrique
anti-outlier, sans hiérarchie primaire/secours entre sources.

### 15.1 Évolutions autorisées en version mineure

- Révision documentée de `δ_hr_suspect` dans sa plage admissible
- Révision documentée de `δ_hr_coherence` dans sa plage admissible
- Révision documentée de `α_EWMA` et `δ_max` dans leurs plages admissibles
- Caractérisation formelle de l'exposition de sensor.humidite_jardin_3
- Versionnement des dépendances contractuelles amont
- Promotion des indicateurs secondaires §10.3 au rang obligatoire
- Extension du test de cohérence à N=3 sources retenues si observé nécessaire

### 15.2 Évolutions requérant une version majeure

- Modification du modèle de fusion (source canonique unique,
  hiérarchie primaire/secours, passage à une logique asymétrique, etc.)
- Modification du modèle de stabilisation

### 15.3 Anti-pattern verrouillé

Aucune évolution future ne pourra réintroduire une bascule
opportuniste non gouvernée entre capteurs.

Toute logique du type "si source A disponible, utiliser A ;
sinon basculer sur B" est explicitement interdite par le présent
contrat, sauf révision majeure documentée.
