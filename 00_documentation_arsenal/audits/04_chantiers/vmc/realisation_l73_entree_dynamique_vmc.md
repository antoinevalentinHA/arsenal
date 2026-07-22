# Réalisation L7.3 — critère d'entrée dynamique et observabilité (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L7.3 — critère d'entrée dynamique et observabilité** |
| **Statut** | **Préparé sur branche** |
| **Preuve opérationnelle** | `arsenal-runtime`, commit **`16326b1`**, dossier `analyses/c35_l73_instrumentation_20260722/` |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §2.2, §2.2 bis, §4.4 bis, §9.1 bis, §10.2 exigences 11 à 19. **Non modifié par ce lot** |

> **La voie d'évolution est instrumentée et intégralement exposée. Elle n'est
> pas rendue décisionnelle — et ce n'est pas un choix de prudence, c'est une
> impossibilité démontrée.**

---

## 1. Ce qui est créé

[`13_sensor_platforms/statistics/vmc/minimum_glissant.yaml`](../../../../13_sensor_platforms/statistics/vmc/minimum_glissant.yaml)
— deux capteurs `platform: statistics` fournissant la **valeur de référence** de
l'observation glissante bornée du §2.2 bis :

| Capteur | Source | Fenêtre nominale |
|---|---|---|
| `sensor.vmc_minimum_glissant_sdb_parents` | `sensor.humidite_relative_sdb_parents` | **20 min** |
| `sensor.vmc_minimum_glissant_sdb_enfants` | `sensor.humidite_relative_sdb_enfants` | **30 min** |

`state_characteristic: value_min` — l'évolution locale s'en déduit par
différence avec la mesure courante.

**Les fenêtres sont celles de la passe 1.** Celle de 30 minutes est fondée sur
la **profondeur disponible pendant les montées réelles**, et non sur
l'intervalle médian global entre états — distinction établie par le contre-audit
`132072bf`.

**Aucun élargissement Recorder n'est requis** : les deux sources sont déjà dans
l'allowlist.

---

## 2. Ce n'est pas une mémoire

Le **§2.2** interdit nommément mémoire d'épisode, instant de début, durée
écoulée, **valeur de pic**, historique de mesures, compteur et timer.

> Ces capteurs ne portent **rien de tout cela**. Ils exposent une **statistique
> bornée** de la mesure courante, que le **§2.2 bis** autorise explicitement, et
> **en condition d'entrée seulement**.

---

## 3. Le point ouvert par L6 est clos — par constat

L6 avait désigné les attributs de couverture temporelle de la plateforme
`statistics` comme **« à constater sur l'instance, non affirmés »** : les
exigences 12, 17 et 19 du §10.2 en dépendent.

**Constat fait sur les 38 bases** (`16326b1`), sur deux témoins déjà en service
et munis de `max_age` :

| Témoin | Bases | Attributs |
|---|---:|---|
| `sensor.temperature_sejour_mean_10min` | **38/38** | `age_coverage_ratio`, `buffer_usage_ratio`, `source_value_valid` |
| `sensor.temperature_sejour_mean_30min` | **38/38** | idem |

> **Les trois attributs attendus sont présents partout.** Les exigences 12, 17
> et 19 sont servables **sans créer aucun capteur supplémentaire**.

---

## 4. Exposition — les neuf exigences du §10.2

Chaque besoin expose désormais, en attributs :

| # | Exigence | Attribut |
|---|---|---|
| 11 | durée nominale de la fenêtre | `evolution_fenetre_nominale` |
| 12 | profondeur temporelle réellement disponible | `evolution_profondeur_disponible` |
| 13 | valeur courante | `evolution_valeur_courante` |
| 14 | valeur de référence utilisée | `evolution_valeur_reference` |
| 15 | évolution calculée, si calculable | `evolution_calculee` |
| 16 | frontière d'évolution configurée | `evolution_frontiere` |
| 17 | statut calculable / non calculable | `evolution_calculable` |
| 18 | condition dynamique satisfaite / non satisfaite | `evolution_satisfaite` |
| 19 | raison de non-calculabilité | `evolution_cause_non_calculable` |

**Aucun repli silencieux** : chaque grandeur est convertie avec `float(none)`,
et l'absence est **nommée** plutôt que remplacée.

Un attribut supplémentaire, `evolution_role`, énonce **en clair** que la voie
est exposée mais non décisionnelle : l'explicabilité ne doit pas laisser croire
qu'un critère affiché est un critère appliqué.

---

## 5. Pourquoi la voie n'est pas rendue décisionnelle

**Machine simulée** — la seule possible à ce stade :

```
entrée      : niveau ≥ S   OU   (montée ≥ D sur W)
libération  : niveau < S            ← seule frontière disponible avant L7.4
```

| Pièce | Ouverts par le **niveau** | Ouverts par l'**évolution** | Vie médiane | < 60 s | < 5 min |
|---|---:|---:|---:|---:|---:|
| **Parents** | 281 | **784** | **25 s** | **70 %** | **91 %** |
| **Enfants** | **0** | **98** | 328 s | 7 % | 43 % |

> **La voie d'évolution existe précisément pour reconnaître un épisode qui
> n'atteint jamais la frontière de niveau.** Or, tant que la seule frontière de
> libération disponible **est cette même frontière de niveau**, un besoin ouvert
> par l'évolution **naît déjà sous elle** : il est libéré à l'évaluation
> suivante.

**Ce n'est pas un défaut de calibration : c'est une contradiction interne de la
machine à ce stade. Aucune valeur de `W` ou de `D` ne la lèverait.**

**Coût chiffré d'une décisionnalisation prématurée** : 784 besoins
supplémentaires chez les parents, dont **91 % libérés en moins de cinq
minutes** — un battement sans aucun bénéfice de couverture.

### 5.1 Une nuance de lecture, à ne pas confondre avec un maintien

La « durée de vie » observée **n'est pas une durée de besoin** : c'est le
**délai jusqu'à la mesure suivante**.

La salle de douche enfants publiant plus rarement, sa médiane paraît plus longue
— 328 s contre 25 s — **sans que le besoin y soit mieux tenu**. Aucun de ses
épisodes n'atteint `S` : chaque besoin y meurt dès la première mesure suivante.
Le chiffre mesure la cadence du capteur, pas la machine.

---

## 6. Tension avec le §9.1 bis — qualifiée, non résolue

Le contrat pose que l'observation glissante « **n'est pas restaurée : elle
repart vide** » (§9.1 bis). La plateforme `statistics` **recharge** en revanche
sa fenêtre depuis l'historique du Recorder — contrainte que `recorder.yaml`
documente pour toute source de cette plateforme.

**Qualification :**

| Invariant du §9.1 bis | Respecté ? |
|---|---|
| le remplissage ne fait perdre aucun besoin restauré | **oui** — une fenêtre pleine ne révoque rien |
| il ne crée aucun faux besoin | **oui** — la voie n'est pas décisionnelle, et le sera sous plancher en L7.4 |
| aucune valeur de remplissage n'est fabriquée | **oui** — les valeurs viennent de mesures réelles |

> **L'écart porte sur la lettre, non sur les invariants.** Le contrat décrit une
> fenêtre vide au redémarrage ; l'implémentation en fournit une **pleine de
> mesures réelles**. **Aucun invariant n'est franchi**, et l'écart va dans le
> sens conservateur.
>
> **Le point est consigné, non tranché.** Il n'appelle pas de co-changement
> tant que la voie n'est pas décisionnelle ; **L7.4 devra le reprendre**, car
> c'est là qu'une fenêtre pleine dès le démarrage aura un effet réel.

---

## 7. Garde CI — les deux faces

Un **test 6** est ajouté à `check_vmc_contracts.py`. Il garde **les deux
faces** :

- **l'exposition existe** — les neuf attributs des exigences 11 à 19 sont
  présents dans chaque besoin ;
- **la référence glissante n'entre pas dans `state`** — la voie reste non
  décisionnelle tant que la libération se confond avec l'entrée.

**Deux preuves négatives établies** : faire entrer la référence glissante dans
l'état fait échouer le checker ; retirer un seul attribut d'exposition aussi.

> **Le second contrôle est explicitement daté.** Il devra être **retiré par
> L7.4**, qui rend la voie décisionnelle : son échec sera alors le **signal
> attendu**, non une régression. Le message d'erreur le dit — « ce contrôle
> doit être retiré par L7.4, pas contourné ».

---

## 8. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés**, tous passent. Les trois fichiers
runtime sont **valides au parseur YAML**. Les **gates documentaires** passent.

> **Deux échecs demeurent, ANTÉRIEURS à ce lot** : `lovelace_no_inline_templating`
> et `vacances`. Ni causés, ni aggravés.

---

## 9. Ce que ce lot ne fait pas

- il **ne modifie pas `/config`** ;
- il **ne change aucun comportement** : la décision est identique à celle de
  L7.2 ;
- il **ne rend pas la voie d'évolution décisionnelle** ;
- il **ne rétablit pas** la couverture de la salle de douche enfants, toujours à
  0/27 — cela relève de L7.4 ;
- il **n'introduit ni hystérésis, ni frontière modulée** ;
- il **n'applique pas le §4.4** ;
- il **n'expose rien en UI** ;
- il **ne tranche pas** la tension avec le §9.1 bis ;
- il **ne clôt pas C35**.

---

## 10. État des écarts contractuels

| # | Écart | État |
|---|---|---|
| 1 | verdict d'aération décisionnel | ✅ résorbé (L7.2) |
| 2 | frontières de libération non consommées | partiel |
| 3 | aucun besoin hystérétique | demeure — **L7.4** |
| 4 | aucun état humidité par pièce | partiel |
| 5 | restauration et indisponibilité | demeure — **L7.5** |
| 6 | intention divergente | ✅ résorbé (L7.1) |

> **Prochain jalon : L7.4 — machine hystérétique et libération modulée.** C'est
> le lot pivot du chantier : il rend la voie d'évolution décisionnelle, débloque
> l'été, et rend la salle de douche enfants opérante. Tout ce qui précède le
> prépare.
