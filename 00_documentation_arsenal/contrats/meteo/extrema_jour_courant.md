# Arsenal — Pré-contrat métier et architectural
# Famille — Extrema du jour civil en cours (températures par zone)
# Version : 0.1.0
# Statut : pré-normatif — à figer avant toute phase d'implémentation
# Chemin : 00_documentation_arsenal/contrats/meteo/extrema_jour_courant.md

---

## 0. Statut et portée de ce document

Ce document est un **pré-contrat**. Il fixe la doctrine d'une nouvelle famille
Arsenal avant écriture de toute entité. Il ne contient aucun YAML, aucune
automatisation, aucun helper, aucune implémentation. Il a vocation à devenir
contrat normatif (`v1.0`) une fois validé, et à servir de référence opposable
lors de la phase patch.

Toute implémentation ultérieure doit être conforme aux invariants `INV-JC-*`
ci-dessous. Tout écart d'implémentation est une non-conformité, pas une
interprétation.

---

## 1. Objet

Définir la famille métier dédiée à l'affichage, pour chaque zone suivie, de :

```text
minimum observé aujourd'hui
maximum observé aujourd'hui
```

sur la fenêtre **du jour civil en cours** :

```text
00:00:00 (heure locale) → maintenant
```

avec **remise à zéro à minuit** et **aucune conservation de la veille**.

La famille remplace, pour le dashboard « Températures Min · Max », la branche
glissante 24 h (`platform: statistics`, `max_age: 24h`) jugée non conforme à la
notion métier « jour en cours » (cf. §9).

---

## 2. Périmètre

### 2.1 Zones concernées

```text
entree
sejour
palier
chambre_arnaud
chambre_matthieu
chambre_parents
petite_maison
sdb_parents
sdb_enfants
garage
cave
jardin
```

Soit **12 zones**, **2 axes** (min, max).

### 2.2 Statut particulier du Jardin

Le Jardin participe à cette famille **uniquement en lecture** (cf. §7).
Il dispose déjà d'une mémoire courante pilotée par le pipeline palmarès :

```text
input_number.temperature_min_jour_courant_jardin
input_number.temperature_max_jour_courant_jardin
```

La famille **réutilise** ces mémoires existantes pour l'exposition. Elle n'en
crée pas de nouvelles pour le Jardin, et n'y écrit jamais.

### 2.3 Ce que la famille n'est pas

La famille ne couvre **pas** :

- la journée civile clôturée (`*_journaliere_*`) ;
- la clôture quotidienne à 00:00:05 ;
- l'historique quotidien ;
- les palmarès par pièce ;
- la conservation de la valeur de la veille ;
- les records hebdomadaires / mensuels / saisonniers ;
- la branche glissante 24 h (qui est explicitement abandonnée, cf. §9).

---

## 3. Nature métier

### 3.1 Définitions exactes

**Minimum du jour en cours d'une zone** :

```text
la plus basse valeur métier valide observée sur la source thermique
de la zone, depuis 00:00:00 (heure locale) du jour civil courant
jusqu'à l'instant présent.
```

**Maximum du jour en cours d'une zone** :

```text
la plus haute valeur métier valide observée sur la source thermique
de la zone, depuis 00:00:00 (heure locale) du jour civil courant
jusqu'à l'instant présent.
```

### 3.2 Valeur métier valide

Une mesure est « métier valide » si elle est :

- numérique (ni `unknown`, ni `unavailable`, ni `none`, ni chaîne vide) ;
- distincte de toute sentinelle (cf. §6) ;
- comprise dans la `plage_metier_source` de la zone.

| Classe de zone | `plage_metier_source` |
|---|---|
| Zones intérieures (11 pièces) | `[5, 45]°C` |
| Jardin (extérieur) | héritée du pipeline palmarès — non redéfinie ici |

Toute mesure hors plage métier est ignorée (abstention), jamais écrite.

### 3.3 Absence métier

Tant qu'aucune mesure valide n'a été observée **depuis le dernier reset**, le
minimum et le maximum du jour n'existent pas en tant que valeurs métier. Cet
état d'absence est porté par une sentinelle interne (§6) et **n'est jamais
exposé comme une valeur** : l'exposition est alors `unavailable` (cf. INV-JC-7).

---

## 4. Architecture canonique de la famille

Trois couches, sans clôture, sans historique :

```text
source température (existante, inchangée)
   sensor.temperature_<zone>
        │  sur changement d'état
        ▼
mémoire jour courant            ← registre de pipeline (input_number)
   input_number.temperature_min_jour_courant_<zone>
   input_number.temperature_max_jour_courant_<zone>
        │  lecture seule
        ▼
exposition dashboard            ← interface consommable (template sensor)
   sensor.temperature_min_jour_courant_<zone>
   sensor.temperature_max_jour_courant_<zone>
```

La couche exposée s'arrête là : elle a un consommateur direct (la restitution
UI et la couche couleur du dashboard, cf. §12). Aucune couche supplémentaire
n'est créée tant qu'elle n'a pas de consommateur (cf. §14.5).

---

## 5. Monotonicité

Entre deux remises à zéro consécutives, pour une zone donnée :

- le **minimum** ne peut que **baisser ou rester identique** ;
- le **maximum** ne peut que **monter ou rester identique**.

L'écriture de la mémoire courante n'a lieu que si la mesure entrante **étend
strictement** l'extrême :

```text
update min  ⇔  mesure < min_courant   (et mesure dans la plage métier)
update max  ⇔  mesure > max_courant   (et mesure dans la plage métier)
```

Toute mesure qui n'étend pas l'extrême est ignorée (abstention silencieuse,
légitime). La **seule** opération autorisée à faire remonter un minimum ou
redescendre un maximum est la **remise à zéro** (§6).

---

## 6. Remise à zéro

### 6.1 Doctrine de minuit

À minuit civil local (`00:00:00`), chaque mémoire courante d'une **zone
intérieure** est réinitialisée à sa sentinelle. La nouvelle journée démarre
sans pollution de la veille.

La remise à zéro de la famille **ne dépend d'aucune clôture** : il n'existe pas
d'étape `00:00:05` à attendre. Le reset s'effectue donc à minuit strict, et non
à `00:00:10` comme pour le Jardin (dont le décalage existe uniquement pour
laisser passer la clôture du palmarès — étape absente ici).

Le Jardin **n'est pas** réinitialisé par la famille (cf. §7) : sa mémoire
courante reste remise à zéro par le pipeline palmarès.

### 6.2 Sentinelles

| Axe | Sentinelle | Signification | Justification |
|---|---|---|---|
| min | `999` | absence métier | strictement supérieure à toute valeur métier plausible : ne peut jamais piéger une comparaison `mesure < min_courant` |
| max | `-999` | absence métier | strictement inférieure à toute valeur métier plausible : ne peut jamais piéger une comparaison `mesure > max_courant` |

Grammaire alignée sur celle du pipeline Jardin (sentinelle froide `999`,
sentinelle chaude `-999`), afin que toute la météo partage une seule grammaire
d'absence métier.

Distinction métier / technique (même logique que les contrats palmarès) :

| Plage | Rôle |
|---|---|
| `plage_metier_source` | valeurs réelles attendues (`[5, 45]°C` en intérieur) |
| `plage_helpers_technique` | bornes effectives des `input_number`, étendues pour autoriser le stockage de la sentinelle hors plage métier |

La sentinelle est **stockable techniquement** mais **jamais métier**
(cf. INV-JC-6).

### 6.3 Première mesure du jour

La première mesure métier valide observée après un reset écrase
nécessairement la sentinelle :

```text
première mesure < 999   → initialise le minimum du jour
première mesure > -999  → initialise le maximum du jour
```

La première mesure valide du jour initialise donc simultanément les deux
extrêmes. Avant cette première mesure, l'exposition reste `unavailable`.

---

## 7. Écrivain souverain

### 7.1 Principe

**Chaque entité de mémoire courante possède un et un seul écrivain souverain.**
Aucune entité de la famille n'est écrite par plus d'une autorité.

| Entité | Écrivain souverain |
|---|---|
| `input_number.temperature_*_jour_courant_<piece>` (11 pièces) | la couche d'alimentation de la **présente famille** (update + reset) |
| `input_number.temperature_*_jour_courant_jardin` | le **pipeline palmarès Jardin** — exclusivement |

### 7.2 Implication impérative pour le Jardin

Le Jardin possède déjà :

```text
input_number.temperature_min_jour_courant_jardin
input_number.temperature_max_jour_courant_jardin
```

pilotés par le pipeline palmarès (automatisations `update` / `reset` /
`cloture`).

La présente famille **ne doit jamais devenir écrivain de ces entités**. Elle
est, pour le Jardin, **strictement consommatrice** :

- elle **ne les met jamais à jour** ;
- elle **ne les réinitialise jamais** ;
- elle **n'émet aucun `set_value`** vers elles ;
- sa couche d'alimentation factorisée **exclut le Jardin** de toute liste de
  cibles d'écriture.

La seule interaction autorisée de la famille avec les mémoires Jardin est la
**lecture** par la couche d'exposition.

### 7.3 Justification

Un double écrivain sur la mémoire courante Jardin introduirait des courses
d'écriture, corromprait la source du palmarès, et violerait à la fois le
présent contrat et les contrats palmarès chaud/froid. L'exclusion du Jardin de
la couche d'écriture est donc **bloquante**, pas indicative.

---

## 8. Relation avec le palmarès

### 8.1 Le jour courant comme amont possible

La couche « jour courant » est l'amont à partir duquel un système historique
**peut** dériver une valeur clôturée (c'est exactement ce que fait le Jardin :
sa mémoire courante est clôturée à `00:00:05` vers `*_journaliere_*`, puis
consommée par le palmarès).

### 8.2 Historique ≠ obligation

**La présence d'une couche « jour courant » n'impose aucune couche
historique.** Une zone peut disposer d'extrema du jour en cours **sans**
journée clôturée, **sans** palmarès, **sans** conservation de la veille. C'est
le cas normal et attendu des 11 zones intérieures.

### 8.3 Clause anti-dérive

L'existence de cette famille **ne doit jamais servir de justification** pour
imposer à une zone :

```text
*_journaliere_*
palmarès
historique quotidien
```

L'ajout d'une couche de clôture ou de palmarès à une zone est un acte
**séparé**, qui exige :

1. un besoin métier explicite et démontré pour cette zone ;
2. son propre contrat ;
3. un consommateur réel et nommé de la couche historique.

Il n'existe **aucune propagation automatique** du modèle Jardin aux autres
zones. Le Jardin est aujourd'hui la **seule** zone à porter les deux couches,
par exception justifiée (besoin records météo formalisé dans les contrats
palmarès) — et non comme gabarit à généraliser.

---

## 9. Interdiction explicite — fenêtre glissante 24 h

### 9.1 Incompatibilité doctrinale

Une fenêtre glissante du type :

```text
platform: statistics
state_characteristic: value_min / value_max
max_age:
  hours: 24
```

est **incompatible** avec la notion métier « jour en cours » et **interdite**
comme source de la présente famille.

### 9.2 Pourquoi

1. **Pas de frontière de minuit.** Une fenêtre 24 h ne se réinitialise jamais à
   `00:00`. À 15:00, elle couvre « hier 15:00 → maintenant », pas
   « aujourd'hui 00:00 → maintenant ». Elle répond à une autre question.
2. **Violation de la monotonicité (§5).** Lorsqu'une valeur extrême sort de la
   fenêtre, le minimum peut **remonter** et le maximum **redescendre** à
   l'intérieur d'une même « journée » — ce que la famille interdit
   structurellement.
3. **Plausible mais faux.** L'extrême affiché peut appartenir à la veille,
   produisant un affichage crédible mais incorrect — précisément le défaut que
   la doctrine Arsenal combat.
4. **Cohérence inter-contrats.** C'est le construit déjà interdit comme source
   métier par `§3.4` des contrats palmarès chaud/froid. La famille étend cette
   interdiction au dashboard des pièces.

### 9.3 Portée précise de l'interdiction

L'interdiction porte sur l'usage de la fenêtre glissante **comme source des
extrema du jour en cours**. Elle ne proscrit pas la plateforme `statistics` en
soi pour d'autres usages explicitement qualifiés « tendance ». La famille
existe pour **remplacer** la fenêtre glissante, jamais pour l'encapsuler.

---

## 10. Convention de nommage

### 10.1 Mémoire courante

```text
input_number.temperature_min_jour_courant_<zone>
input_number.temperature_max_jour_courant_<zone>
```

(grammaire identique à l'existant `temperature_min_jour_courant_jardin`).

### 10.2 Exposition

```text
sensor.temperature_min_jour_courant_<zone>
sensor.temperature_max_jour_courant_<zone>
```

### 10.3 Disparition du nom ambigu

Le segment `_jour_` employé seul (sans `courant`) par la branche glissante
(`sensor.temperature_min_jour_<zone>`) **disparaît** du périmètre métier au
terme de la migration. Grammaire finale, sans ambiguïté :

```text
_jour_courant_   → jour civil en cours      (présente famille)
_journaliere_    → jour civil clôturé        (Jardin / palmarès uniquement)
```

---

## 11. Invariants métier

| ID | Invariant |
|---|---|
| INV-JC-1 | La fenêtre métier est le jour civil en cours, `00:00:00 → maintenant`, heure locale. |
| INV-JC-2 | Une fenêtre glissante 24 h est interdite comme source (cf. §9). |
| INV-JC-3 | Entre deux resets, le minimum est non croissant ; le maximum est non décroissant. |
| INV-JC-4 | La mémoire n'est écrite que si la mesure étend strictement l'extrême et appartient à la plage métier. |
| INV-JC-5 | La remise à zéro à minuit est la seule opération pouvant faire remonter un min ou redescendre un max. |
| INV-JC-6 | Les sentinelles `999` (min) et `-999` (max) sont techniques, jamais métier. |
| INV-JC-7 | Aucune exposition n'affiche jamais une sentinelle : mémoire à la sentinelle ⇒ exposition `unavailable`. |
| INV-JC-8 | Chaque mémoire courante a un et un seul écrivain souverain (§7). |
| INV-JC-9 | La famille n'écrit jamais les mémoires courantes du Jardin ; elle les lit exclusivement. |
| INV-JC-10 | La famille ne crée aucune couche clôturée, historique ou palmarès (§2.3, §8). |
| INV-JC-11 | L'ajout d'une couche historique à une zone exige un contrat dédié et un consommateur nommé — aucune propagation automatique. |
| INV-JC-12 | Toute couche exposée a un consommateur réel ; aucune couche orpheline (§14.5). |
| INV-JC-13 | Le reset des zones intérieures s'effectue à minuit strict, sans dépendance à une étape de clôture. |

---

## 12. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `sensor.temperature_<zone>` (×12) | source thermique instantanée | bloquant |
| `input_number.temperature_*_jour_courant_<piece>` (11 pièces) | mémoire courante — écrite par la famille | bloquant |
| `input_number.temperature_*_jour_courant_jardin` | mémoire courante Jardin — **lue** par la famille, écrite par le palmarès | bloquant (lecture) |
| `sensor.temperature_*_jour_courant_<zone>` (exposition) | interface consommable | bloquant |

Consommateurs aval (hors surface du présent contrat, mais à repointer en phase
patch) :

- `sensor.temperature_minmax_jour_<zone>` (restitution UI) ;
- famille couleur `sensor.couleur_temperature_min/max_jour_<zone>`.

---

## 13. Recorder

| Population | Entités | Doctrine |
|---|---|---|
| A | `input_number.temperature_*_jour_courant_<piece>` | `restore_state` natif suffit à la survie inter-redémarrage du jour en cours ; aucune inclusion recorder **requise** pour la correction métier. |
| B | `sensor.temperature_*_jour_courant_<zone>` (exposition) | À **n'inclure que si** un graphe historique les consomme. Aucun consommateur de ce type n'existe à ce jour ⇒ ne rien ajouter (cf. INV-JC-12). |

Le recorder fonctionne en liste blanche. Le retrait de la branche glissante ne
retire rien du recorder (les `statistics` n'y figurent pas). Les entrées
recorder du Jardin (`*_journaliere_*`, palmarès) sont **inchangées**.

---

## 14. Facteur Arsenal

### 14.1 Famille homogène

Une grammaire unique `temperature_<axe>_jour_courant_<zone>` pour la mémoire et
l'exposition, identique sur les 12 zones, 2 axes. Aucune zone n'est un cas
particulier de nommage.

### 14.2 Ancres YAML

La logique d'exposition est définie **une fois** via ancre ; chaque instance de
zone n'est qu'un stub (réutilisation directe du motif déjà employé par la
famille couleur et par `temperature_minmax_jour`).

### 14.3 `this.entity_id`

L'exposition dérive l'axe et la zone depuis `this.entity_id`
(`replace` du préfixe), et lit la mémoire correspondante sans une seule ligne
de logique par zone — motif déjà présent et éprouvé dans le dépôt.

### 14.4 Factorisation de la couche d'écriture

L'alimentation est factorisée par liste de triggers + dérivation de la cible
depuis l'entité déclencheuse, plutôt que par automatisation dédiée par zone.
La couche d'écriture **exclut le Jardin** (§7.2). C'est l'écart majeur, et
assumé, avec le pipeline Jardin historique (écrit à la main, mono-source).

### 14.5 Doctrine des couches sans consommateur

La famille s'arrête à la couche exposée parce que c'est la dernière couche
réellement consommée (dashboard). Aucune couche `*_journaliere_*`, historique
ou palmarès n'est créée en l'absence de consommateur. Cette clause est le
garde-fou structurel contre toute dérive vers une généralisation du pipeline
Jardin complet (INV-JC-10, INV-JC-12).

---

## 15. Hors périmètre

- journée civile clôturée par pièce ;
- clôture quotidienne par pièce ;
- palmarès par pièce ;
- records hebdomadaires / mensuels / saisonniers ;
- conservation de la veille ;
- fenêtres glissantes (24 h ou autres) comme source métier ;
- modification du pipeline palmarès Jardin.

---

## 16. Extensions futures envisagées

- amplitude thermique du jour (`max - min`) en exposition dérivée ;
- badge « extrême atteint aujourd'hui » ;
- une couche clôturée **par zone**, mais uniquement si un besoin métier
  explicite et un consommateur nommé apparaissent, et sous contrat dédié
  (INV-JC-11).

Aucune de ces extensions n'a de valeur normative en v0.1.

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 0.1.0 | 2026-06-03 | Brouillon pré-normatif initial — formalisation de la famille « extrema du jour civil en cours » : nature métier, monotonicité, remise à zéro, écrivain souverain (Jardin en lecture seule), relation non obligatoire au palmarès, interdiction de la fenêtre glissante 24 h comme source, et garde-fous Arsenal (familles homogènes, ancres, `this.entity_id`, pas de couche sans consommateur). |
