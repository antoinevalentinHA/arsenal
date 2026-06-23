# CONTRAT ARSENAL — CLIMATISATION
## 12 — Ventilation (fan_mode) — Intention persistante (Modèle B)

**Version contrat :** v1.0
**Statut :** Normatif — cible de conception, antérieure à l'implémentation runtime

---

## Objet

Ce contrat fixe le **modèle fonctionnel de la ventilation** de la
climatisation (le `fan_mode` : vitesse de soufflage), distinct du mode
thermique (`cool` / `dry` / `heat` / `off`) traité par les sections 01→11.

La ventilation est un **axe orthogonal** au mode thermique : elle ne
décide jamais d'allumer, d'éteindre ou de changer le mode de la
climatisation. Elle exprime **quelle vitesse de soufflage** appliquer
lorsque la climatisation fonctionne.

Le modèle retenu est le **Modèle B** : l'intention utilisateur est
**persistante** et le silencieux automatique est un **override temporaire
et non destructif** de cette intention.

> Ce document est une **passe documentaire**. Il fixe la cible opposable
> avant toute implémentation. Aucun runtime n'est modifié par ce lot
> (voir §13).

> **Voir aussi.** L'**intensité graduée** du besoin de froid qui pilotera une
> future résolution automatique de la vitesse de ventilation est spécifiée par
> le contrat voisin
> [`13_intensite_besoin_froid.md`](13_intensite_besoin_froid.md) (couche
> perception, sans pilotage matériel). La présente section reste limitée au
> `fan_mode` et à l'intention utilisateur.

---

## Rôle des entités

| Entité | Rôle contractuel | Nature |
|---|---|---|
| `input_select.clim_fan_mode_cible` | **Intention utilisateur persistante** : le mode de ventilation souhaité par défaut. Ne reflète JAMAIS le réel. | Intention |
| `sensor.clim_mode_de_ventilation_local` | **Perception** du mode de ventilation réellement appliqué (`fan_mode` lu sur `climate.clim`). Lecture pure. | Perception |
| `binary_sensor.clim_silencieux_autorise` | **Décision métier** autorisant l'override silencieux (plage horaire + présence + activation). | Décision |
| `switch.clim_quiet_fan` | **Actionneur** silencieux. | Exécution |
| `sensor.clim_mode_silencieux_local` | **Perception** de l'état silencieux réel. Lecture pure. | Perception |

Ces cinq entités existent déjà. Ce contrat **ne les renomme pas, ne les
recrée pas et n'en crée aucune autre**.

### Mapping intention → fan_mode technique

| `input_select.clim_fan_mode_cible` (FR) | `fan_mode` technique |
|---|---|
| Silencieux | `quiet` |
| Faible | `low` |
| Moyen | `medium` |
| Fort | `high` |
| Auto | `auto` |

Ce mapping est l'unique table de correspondance autorisée entre
l'intention et la commande matérielle.

---

## 1. Single-writer de l'intention

L'intention utilisateur a un **écrivain unique** : l'utilisateur.

- **AUTORISÉ** — Seul l'utilisateur (via l'UI) DOIT pouvoir écrire
  `input_select.clim_fan_mode_cible`.
- **INTERDIT** — Aucune couche de **perception** NE DOIT écrire cette entité.
- **INTERDIT** — Aucune couche de **décision** NE DOIT écrire cette entité.
- **INTERDIT** — Aucune couche d'**exécution** NE DOIT écrire cette entité.
- **INTERDIT** — Aucune **restauration** NE DOIT écrire cette entité.
- **INTERDIT** — Aucune **réconciliation** NE DOIT écrire cette entité.

> **Clause centrale.** La restauration de l'intention agit **uniquement
> sur le mode effectif appliqué** à la climatisation (`fan_mode` matériel).
> Elle NE DOIT JAMAIS modifier `input_select.clim_fan_mode_cible`.

L'intention est une **vérité d'origine utilisateur**. La perception et
l'exécution la **lisent** ; elles ne la **réécrivent jamais**. Toute
réécriture de l'intention par une couche non-utilisateur est, par
construction, un défaut du modèle.

---

## 2. Autorité de résolution ventilation

Le modèle introduit une **autorité fonctionnelle de résolution** dont le
seul rôle est de calculer le **mode effectif** à appliquer.

```
mode_effectif =
    si binary_sensor.clim_silencieux_autorise == on   → quiet
    sinon                                              → mapping(input_select.clim_fan_mode_cible)
```

Propriétés de l'autorité de résolution :

- elle **lit** l'intention et l'autorisation silencieux ;
- elle **ne décide jamais** d'allumer/éteindre/changer le mode thermique ;
- elle **n'écrit jamais** dans l'intention (§1) ;
- elle est le **seul chemin conceptuel** vers l'écriture matérielle du
  `fan_mode` (§3).

La résolution sépare strictement quatre rôles, qui NE DOIVENT JAMAIS être
confondus :

| Rôle | Porté par | Écrit |
|---|---|---|
| **Intention** | `input_select.clim_fan_mode_cible` | utilisateur seul |
| **Résolution** | autorité de résolution | mode effectif (calcul) |
| **Exécution** | commande `fan_mode` matériel | climate.clim |
| **Perception** | `sensor.clim_mode_de_ventilation_local` | lecture pure |

---

## 3. Chemin unique vers le matériel

- Il NE DOIT exister qu'**un seul chemin logique d'écriture** vers le
  `fan_mode` matériel : la **résolution** (§2).
- Une seule autorité DOIT commander le `fan_mode` (`climate.set_fan_mode`).
- L'automatisation d'application UI actuelle NE DOIT PAS constituer un
  **second chemin concurrent** d'écriture matérielle : l'application d'une
  intention DOIT passer par la résolution.
- Aucun autre composant NE DOIT écrire directement le `fan_mode` matériel.

**Objectif :** éliminer les doubles commandes, les courses, les boucles et
les comportements fantômes.

**Implémentation :** l'autorité de résolution est l'automation
`10030000000120`. Le `quiet` de l'override reste réalisé par
`switch.clim_quiet_fan` (automation silence `1003000000020`) — actionneur
distinct de `climate.set_fan_mode`, conformément à la liste des deux
actionneurs (§ Rôle des entités).

---

## 4. Origine de pilotage ventilation

Le modèle introduit une **origine de pilotage ventilation** : une
perception expliquant **pourquoi** le mode appliqué est celui observé.

Elle DOIT être :

- **déterministe** (une seule valeur à un instant donné) ;
- **mutuellement exclusive** (les états ne se chevauchent pas) ;
- **à valeurs finies** ;
- **utilisable par l'UI**.

### Valeurs

| Valeur | Signification |
|---|---|
| `indisponible` | Donnée ou API non exploitable : le pilotage ne peut être ni établi ni expliqué. |
| `silencieux_auto` | Override silencieux actif : mode effectif forcé à `quiet`. |
| `incompatible` | Le `fan_mode` cible résolu n'est pas applicable (absent de `fan_modes`) : abstention observable. |
| `intention` | Nominal : le mode appliqué découle du mapping de l'intention utilisateur. |

### Hiérarchie de priorité (ordre normatif)

```
1. indisponible      ← prime sur tout
2. silencieux_auto
3. incompatible
4. intention         ← cas nominal
```

**Justification de l'ordre (doctrine Arsenal).**

- `indisponible` prime, par cohérence directe avec la règle couleur **R6**
  (« le gris indisponibilité prime sur toute couleur ») : une donnée non
  exploitable interdit toute affirmation sur le pilotage.
- `silencieux_auto` vient ensuite : tant qu'il est actif, l'override est
  l'**autorité gouvernante** du mode effectif (§2) et masque l'intention.
- `incompatible` précède `intention` : une cible non applicable est un fait
  observable d'abstention, prioritaire sur l'affichage du cas nominal.
- `intention` est le cas par défaut, lorsqu'aucune des conditions
  supérieures n'est vraie.

Cet ordre est **conservé** par rapport à la recommandation initiale : il
est cohérent avec R6 et avec le principe « override = autorité temporaire ».
Aucune réorganisation n'est justifiée.

**Entité d'implémentation :** `sensor.clim_origine_ventilation`
(`12_template_sensors/climatisation/ventilation/origine.yaml`) — capteur
template, perception pure, valeurs `indisponible` / `silencieux_auto` /
`incompatible` / `intention`.

---

## 5. Comportement nominal

### Hors plage silencieuse

- l'intention est **conservée** ;
- `mode_effectif = mapping(intention)` ;
- le silencieux est désactivé sauf autre cause documentée.

### Entrée en plage silencieuse

- l'intention est **conservée** (jamais réécrite) ;
- `mode_effectif` devient `quiet` ;
- l'override **NE réécrit PAS** l'intention.

### Pendant la plage silencieuse

- l'utilisateur PEUT modifier son intention ;
- cette nouvelle intention est **enregistrée immédiatement** dans
  `input_select.clim_fan_mode_cible` (écriture utilisateur, §1) ;
- elle **ne casse pas** l'override (`mode_effectif` reste `quiet`) ;
- elle sera **appliquée à la sortie** de plage.

### Sortie de plage silencieuse

- `mode_effectif` redevient `mapping(intention courante)` ;
- si l'utilisateur a changé l'intention pendant la plage, c'est cette
  **nouvelle intention** qui est appliquée.

---

## 6. Réconciliation / convergence

**Trou corrigé.** La restauration NE DOIT PAS dépendre uniquement d'une
transition `ON → OFF` de l'override silencieux. Une telle dépendance
laisse le système désaligné après tout événement qui n'est pas cette
transition précise (redémarrage, retour de disponibilité, etc.).

Il DOIT exister une **logique de convergence sur événements**, déclenchée
notamment par :

- redémarrage de Home Assistant ;
- passage de `binary_sensor.systeme_stable` à `on` (si cette entité est
  utilisée dans le domaine) ;
- retour de disponibilité de `climate.clim` ou de l'API Airstage ;
- changement d'état de `climate.clim` vers un état actif ;
- changement de l'intention utilisateur ;
- changement de l'autorisation silencieux
  (`binary_sensor.clim_silencieux_autorise`) ;
- détection d'un écart entre mode appliqué et mode effectif attendu.

### Règle de convergence

> **Si** l'override silencieux est **OFF**
> **et** `mode appliqué ≠ mapping(intention)`,
> **alors** réappliquer l'intention (via la résolution, §3),
> **sous réserve** de compatibilité (§8) et de disponibilité (§9).

La convergence agit sur le **mode effectif**, jamais sur l'intention (§1).
À contexte identique, l'état final est identique (déterminisme,
cohérent avec la section 10 du contrat climatisation).

---

## 7. Clim éteinte

- L'intention de ventilation NE DOIT JAMAIS rallumer la climatisation.
- Si `climate.clim` est éteint ou au repos, l'intention est **conservée**.
- Elle sera appliquée à la **prochaine reprise d'activité compatible**.

La ventilation est subordonnée à l'activité thermique : elle ne crée
jamais d'activité, elle qualifie une activité existante.

---

## 8. Compatibilité des fan_modes

- Le mapping intention → `fan_mode` technique DOIT rester documenté (table
  ci-dessus).
- Avant toute commande, le `fan_mode` cible DOIT être présent dans
  `climate.clim.attributes.fan_modes`.
- Si le mode cible n'est pas disponible :
  - **abstention** (aucune commande) ;
  - l'intention **n'est pas modifiée** ;
  - l'incompatibilité DOIT être rendue **observable** (origine
    `incompatible`, §4).

---

## 9. API / entités indisponibles

- Si l'API Airstage ou les entités nécessaires sont indisponibles :
  - **abstention** ;
  - **pas** de multiplication de retries ;
  - l'intention **n'est pas modifiée** ;
  - réconciliation au **retour de disponibilité** (§6).

Ce traitement est cohérent avec la résilience d'exécution du contrat
climatisation (section 08) : indisponibilité ⇒ abstention bornée, jamais
corruption de l'intention.

---

## 10. UI attendue

Cible UI **fixée** par ce contrat, **sans modification des dashboards dans
ce lot** (§13).

### Dashboard principal (supervision)

- affiche le **mode réellement appliqué** ;
- affiche l'**origine** seulement quand elle informe ;
- NE DOIT PAS afficher « Souhaité : X » quand `appliqué == intention` hors
  override ;
- en override silencieux, formulation du type :
  « **Silencieux auto · retour Moyen** » ;
- en nominal, afficher simplement le mode appliqué, p. ex. « **Moyen** » ;
- en incompatibilité, afficher une **explication courte**.

### Dashboard Réglages

- le sélecteur DOIT être intitulé « **Mode souhaité** » ;
- ce libellé n'est correct **que parce que** le Modèle B rend l'intention
  persistante.

---

## 11. Couleurs UI

Rappel de la charte (`ui/couleurs/`), opposable à toute future carte
ventilation :

- 🔵 **bleu** `rgba(33,158,243,0.2)` = information **technique exploitable** /
  supervision (un mode de ventilation réel et disponible) ;
- ⚪ **gris indisponibilité** `rgba(158,158,158,0.1)` = `unknown` /
  `unavailable` / donnée non exploitable ;
- le **gris indisponibilité prime toujours** (R6) ;
- une carte NE DOIT JAMAIS afficher une donnée indisponible en bleu ;
- INTERDIT de créer une **couleur de divergence** souhaité/appliqué dans
  Lovelace.

> Note : la valeur bleu canonique exacte est `rgba(33,150,243,0.2)`
> (cf. `ui/couleurs/02_palette.md`). C'est la seule teinte bleue autorisée
> pour la ventilation exploitable.

---

## 12. Observabilité minimale

- L'utilisateur DOIT pouvoir comprendre **pourquoi** le réel diffère de
  l'intention.
- L'**origine de pilotage ventilation** (§4) est la perception minimale
  nécessaire à cette compréhension.
- Il **n'est pas nécessaire** de créer un capteur de divergence dédié à ce
  stade.
- La divergence est **déductible** de trois éléments :
  intention (`input_select.clim_fan_mode_cible`),
  réel (`sensor.clim_mode_de_ventilation_local`) et
  origine de pilotage.

---

## 13. État d'implémentation (Modèle B)

### Synchronisation réel → intention — supprimée

L'automatisation de synchronisation du **réel → intention**
(`sensor.clim_mode_de_ventilation_local` → `input_select.clim_fan_mode_cible`)
violait le single-writer (§1). Elle est **supprimée**
(`11_automations/climatisation/ventilation/synchronisation_etat.yaml`,
ex-ID `10030000000121`, retiré) : plus aucune perception n'écrit l'intention.

### Implémenté par le chantier Modèle B

- résolution + restauration : automation `10030000000120`
  (`application_mode.yaml`), réaffectée en autorité unique vers
  `script.clim_set_fan_mode` (§2, §3, §5, §6) ;
- origine de pilotage : `sensor.clim_origine_ventilation`
  (`origine.yaml`, §4) ;
- UI : `carte_clim_ventilation` consomme l'origine et n'affiche plus le
  « Souhaité : X » tautologique (§10).

### Encore hors périmètre

- suppression du template orphelin `carte_clim_fan_mode` (carte action V3,
  non consommée par le dashboard principal) ;
- tout redesign Lovelace supplémentaire.
