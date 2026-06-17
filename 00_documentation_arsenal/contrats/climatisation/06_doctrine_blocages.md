# Arsenal — Climatisation · Couche Blocage
## Doctrine opérateur des blocages

> **Document normatif.**
> Il définit la classification des blocages du domaine climatisation, le patron d'implémentation
> d'un blocage activable, et les invariants de cohérence avec la couche autorisation et l'observabilité.
> Il précède et gouverne les spécifications d'entités de [`10_blocages.md`](capteurs/blocages/10_blocages.md).

---

## 1. Principe directeur

La climatisation **conseille, arbitre et protège**. Elle ne décide pas que le logement vit dans un environnement idéal.

Un blocage de confort ou de sobriété est un **paramètre de doctrine opérateur**, pas une règle gravée. Il doit donc être activable et désactivable explicitement. Un blocage de sécurité matériel est impératif. Un blocage informatif n'est jamais décisionnel.

---

## 2. Les trois étages de blocage

| Étage | Nature | Désactivation | Position |
|---|---|---|---|
| **1 — Critique sécurité / matériel** | Protège le matériel ou les personnes | Non désactivable, ou désactivable en maintenance uniquement | Entrée autorisation, impérative |
| **2 — Confort / sobriété / bon sens** | Optimise l'usage, évite le gaspillage | Activable / désactivable par interrupteur opérateur | Entrée autorisation, conditionnée |
| **3 — Informatif / diagnostic** | Rend l'état lisible | Sans objet (jamais consommé en décision) | Observabilité, hors chaîne |

> **État 1 actuellement vide pour la climatisation.** Aucun blocage matériel réel (défaut compresseur, surchauffe, court-cycle) n'existe à ce jour. C'est le seul vrai manque structurel si l'étage 1 doit être autre chose qu'une case réservée.

---

## 3. Patron d'implémentation d'un blocage activable (étage 2)

Le patron canonique existe déjà : `binary_sensor.clim_blocage_horaire_reel`. Il combine en interne un interrupteur d'activation et une condition métier, et expose une **vérité de blocage à l'instant T** consommée par les autorisations.

Tout blocage d'étage 2 fondé sur une **condition calculée** suit ce patron :

```text
BLOCAGE_X_REEL =  input_boolean.clim_blocage_X_actif == on
              ET  <condition calculée X> == on
```

Conséquences normatives :

- L'interrupteur ne suffit pas à bloquer ; la condition seule ne suffit pas non plus. Le blocage n'est effectif que par leur conjonction.
- Les autorisations consomment le `_reel`, **jamais la condition brute**. Elles restent des lecteurs combinatoires purs.
- Repli implicite : `is_state(...) → false` si une dépendance est indisponible. Aucun fallback mémoire.
- Un **flag opérateur manuel** (ex. `blocage_clim_poele`) est déjà sa propre garde : il *est* la décision opérateur. Il ne reçoit donc **pas** de second interrupteur d'activation. Ajouter `clim_blocage_poele_actif` serait un interrupteur pour activer un interrupteur — interdit.

---

## 4. Classification des blocages climatisation

| Blocage | Étage | Garde opérateur | Condition source | Vérité consommée | Modes impactés |
|---|---|---|---|---|---|
| Horaire | 2 | `input_boolean.clim_blocage_horaire_actif` *(existant)* | plage horaire + `now()` | `binary_sensor.clim_blocage_horaire_reel` | COOL · HEAT · DRY |
| Aération étage | 2 | `input_boolean.clim_blocage_aeration_etage_actif` *(nouveau)* | `binary_sensor.aeration_preferable_etage` | `binary_sensor.clim_blocage_aeration_etage_reel` | COOL · DRY |
| Fenêtres | 2 | `input_boolean.clim_blocage_fenetres_actif` *(nouveau)* | `binary_sensor.fenetre_ouverte_maison_avec_delai` | `binary_sensor.clim_blocage_fenetres_reel` | COOL · HEAT · DRY |
| Absence prolongée | 2 | `input_boolean.clim_blocage_absence_prolongee_actif` *(nouveau)* | `binary_sensor.clim_extinction_absence_prolongee_autorisee` | `binary_sensor.clim_blocage_absence_prolongee_reel` | COOL |
| Poêle | 2 | `input_boolean.blocage_clim_poele` *(existant, flag manuel direct)* | — | l'`input_boolean` lui-même | HEAT |
| Aération post-chauffage | 2 | `input_boolean.chauffage_blocage_aeration` *(existant, flag manuel direct)* | — | l'`input_boolean` lui-même | HEAT |
| Survol (voyant) | 3 | — | agrégation des blocages effectifs | `binary_sensor.clim_bloquee` | aucun (observabilité) |

Note de classification : le blocage **fenêtres** est le seul candidat « bon sens / quasi-matériel ». Faire tourner le groupe fenêtres ouvertes gaspille mais n'endommage pas. Il reste donc en étage 2 (désactivable librement), pas en étage 1.

---

## 5. Invariant de cohérence du voyant

`clim_bloquee` (étage 3) doit agréger les **vérités effectives** (`_reel` et flags manuels), jamais les conditions brutes.

Sinon le voyant ment : il afficherait `mdi:lock` alors que la climatisation tourne, parce que l'opérateur a désactivé le blocage correspondant. Le voyant doit satisfaire :

```text
clim_bloquee == on  ⟺  au moins un blocage est réellement effectif sur la chaîne de décision
```

Cela corrige aussi l'asymétrie documentée en [`90_observations.md`](capteurs/blocages/90_observations.md) §4 : le voyant lisait `fenetre_ouverte_maison` + `fenetre_ouverte_etage` (brutes, non temporisées), alors que les autorisations lisent `fenetre_ouverte_maison_avec_delai`. **Au runtime, le voyant lit désormais `fenetre_ouverte_maison_avec_delai` — donc la même vérité temporisée que la décision.** La cible `clim_blocage_fenetres_reel` ne changera pas cette vérité : elle ne fera que la **normaliser sous le patron `_reel`** (renommage différé, cf. §8).

---

## 6. État au redémarrage et règle de migration

| Règle | Spécification |
|---|---|
| Restauration | Les `input_boolean` de garde **ne définissent pas `initial:`**. L'état opérateur est restauré nativement au redémarrage. |
| Réactivation silencieuse | Interdite. Un reboot ne réarme jamais un blocage levé par l'opérateur. |
| Défaut à la création | Un `input_boolean` neuf vaut `off` = blocage **désactivé**. |
| **Migration** | Le passage d'un blocage « câblé en dur » à un blocage gardé **lève le blocage** tant que l'interrupteur n'est pas armé. Le déploiement doit donc **mettre `on`** les trois nouveaux interrupteurs une fois, pour préserver le comportement antérieur, avant toute désactivation volontaire. |

---

## 7. Invariants généraux

1. Une autorisation ne lit jamais une condition de blocage brute : uniquement le `_reel` correspondant ou un flag manuel.
2. Un blocage d'étage 3 (diagnostic) n'est jamais consommé par une autorisation ni par une automatisation décisionnelle.
3. Un blocage d'étage 2 fondé sur une condition calculée porte exactement une garde (`*_actif`) et expose exactement une vérité (`*_reel`).
4. Un flag manuel ne reçoit pas de garde supplémentaire.
5. Toute la sémantique de blocage s'exprime en « blocage effectif `on` → interdiction », sans double négation à la lecture aval.

---

## 8. État d'application et dette volontaire

La doctrine et la classification (§2–§7) sont **validées dans leur intégralité** et font foi comme cible. L'implémentation est **échelonnée** par décision opérateur.

| Blocage | État | Justification |
|---|---|---|
| Aération étage | **Appliqué** | Priorité réelle |
| Horaire | Appliqué *(préexistant)* | — |
| Fenêtres | **Dette volontaire** | Spec validée, implémentation différée |
| Absence prolongée | **Dette volontaire** | Spec validée, implémentation différée |
| Poêle · aération post-chauffage | Conservés en flags manuels | Conformes ; pas de garde supplémentaire |

Dettes assumées et tracées :

1. `clim_blocage_fenetres_reel` et `clim_blocage_absence_prolongee_reel` ne sont pas créés. Les autorisations continuent de lire `fenetre_ouverte_maison_avec_delai` et `clim_extinction_absence_prolongee_autorisee` en brut. La double négation aval sur l'absence (§7.5) subsiste jusqu'à la levée de cette dette.
2. La **cohérence de vérité** du voyant `clim_bloquee` (§5) est **déjà acquise au runtime** : le voyant agrège l'aération étage via `binary_sensor.clim_blocage_aeration_etage_reel` et lit `binary_sensor.fenetre_ouverte_maison_avec_delai` — la **vérité temporisée**, identique à celle consommée par les autorisations. Ce qui reste **différé** n'est donc **pas** la cohérence du voyant pour les fenêtres, mais la seule **normalisation de nommage** vers `clim_blocage_fenetres_reel` / `clim_blocage_absence_prolongee_reel` (cf. dette #1). **Résidu connu :** l'absence prolongée n'est pas encore agrégée au voyant (même famille différée), donc l'invariant §5 reste **partiel pour cette seule cause** jusqu'à la levée de la dette #1.
3. Nommage `blocage_clim_poele` / `chauffage_blocage_aeration` conservé hors convention `clim_blocage_*_actif`. **Aucun renommage** : pas de cosmétique au milieu d'un chantier décisionnel.
