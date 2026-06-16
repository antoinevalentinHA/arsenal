# DOCTRINE ARSENAL — Commandabilité

**Référence :** `DOCTRINE_COMMANDABILITE.md`
**Version :** 1.0.0
**Introduced :** Arsenal v16
**Statut :** Normatif

---

## 1. Principe fondateur

> **Une action ne doit être présentée comme exécutable que si le système peut réellement l'exécuter — quel que soit l'acteur, automatique ou manuel.**

La **commandabilité** est la capacité réelle du système à exécuter une action
demandée à l'instant présent. Elle est une **pré-condition d'action** : un *gate*,
pas une observation.

Arsenal pratique déjà ce raisonnement côté automatisations (cf. § 7). Cette
doctrine ne crée aucun besoin runtime nouveau : elle **nomme** un concept déjà
présent, en fixe les frontières, et énonce la seule règle qui manquait — la
symétrie entre le chemin automatique et le chemin manuel.

---

## 2. Définition

> **Commandabilité** : propriété, calculée à partir de vérités existantes et
> opposable, attestant que les **pré-conditions physiques d'exécution** d'une
> action sont réunies à l'instant présent — chemin de commande intègre, cible
> atteignable, et entrées d'exécution nécessaires disponibles (alimentation,
> pont, intégration).

La commandabilité répond à une question unique :

> *Puis-je exécuter cette action **maintenant** ?*

Son consommateur naturel n'est pas l'affichage mais la **couche d'action**.
Lorsqu'elle est fausse, aucune couche — décision, action, UI — ne doit présenter
l'action comme faisable.

---

## 3. Ce que la commandabilité n'est PAS

La commandabilité est distincte de plusieurs notions voisines avec lesquelles
elle ne doit jamais être confondue. Le critère discriminant est catégoriel :
les notions ci-dessous **décrivent un état** ; la commandabilité **autorise un
geste**.

| Notion | Question posée | Rôle | Commandabilité ? |
|---|---|---|---|
| État affiché | « quel est le dernier état connu ? » | mémoire, potentiellement périmée | Non |
| Disponibilité HA | « la feuille est-elle joignable (telle que détectée) ? » | observation, retardée | Non — entrée partielle |
| Connectivité / qualité de signal | « le lien est-il bon ? » (LQI, RF score) | mesure graduée | Non — entrée partielle |
| Santé | « le composant est-il sain ? » | diagnostic d'état | Non — entrée |
| Supervision / télémétrie | « que se passe-t-il ? » | observe, ne *gate* pas | Non |
| **Commandabilité** | **« puis-je exécuter maintenant ? »** | **pré-condition d'action (gate)** | **Oui** |

Une disponibilité Home Assistant n'est pas une preuve de commandabilité : elle
reflète, au mieux, la joignabilité d'une feuille telle que détectée en dernier,
sujette à retard et aveugle au chemin de commande comme à l'alimentation. La
commandabilité **compose** ces vérités ; elle ne s'y réduit pas.

---

## 4. Place dans l'architecture Arsenal

Arsenal repose sur **trois couches universelles**, posées par
`separation_decision_action.md` : observation, décision, action. Toute chaîne
les traverse.

| Couche (universelle) | Question | Forme typique |
|---|---|---|
| Observation (perception) | *Quel est l'état ?* | capteurs, dérivés, synthèses |
| Décision (métier) | *Que dit la logique ? (autorisation / interdiction)* | `binary_sensor.*`, templates purs |
| Action (exécution) | *Que faire quand la décision est vraie ?* | `automation.*`, `script.*` |

La **commandabilité n'est pas une quatrième couche.** C'est un **gate
conditionnel** qui peut s'insérer entre la décision et l'action **uniquement
lorsqu'une pré-condition physique d'exécution connue et pertinente existe**.

```
Chaîne courante (majorité des domaines) :
    [ OBSERVATION ] → [ DÉCISION ] → [ ACTION ]

Chaîne avec pré-condition physique connue (ex. boiler, dépendance secteur) :
    [ OBSERVATION ] → [ DÉCISION ] → ( COMMANDABILITÉ ) → [ ACTION ]
                                       └─ gate conditionnel, présent seulement
                                          si une impossibilité connue peut survenir
```

La majorité des chaînes Arsenal — présence, éclairage simple, notifications,
automatismes courants — restent `OBSERVATION → DÉCISION → ACTION` et
fonctionnent **sans aucun mécanisme de commandabilité**. Une nouvelle
fonctionnalité ne requiert **pas** de signal de commandabilité dédié : le gate
n'existe que là où une pré-condition physique connue le justifie (cf. § 7,
réutilisation des gates existants ; § 8, parcimonie).

Lorsqu'il est présent, le gate ne recalcule pas la décision métier (doctrine
`separation_decision_action`) et ne porte pas de logique de domaine : il
constitue un **filtre d'exécutabilité** — même lorsque la décision dit « agir »,
l'action ne doit ni se déclencher ni être offerte si l'exécution est connue
comme impossible.

Ce filtre prolonge deux invariants de `principes_generaux.md` : le § 8
(« disponibilité explicite plutôt qu'état factice ») et le § 6 (régimes d'un
état externe), mais **côté consommateur d'action** : ne pas offrir ce qui ne
peut pas aboutir.

---

## 5. Distinction centrale — Impossible (A) vs Interdit (B)

Deux situations empêchent une action ; elles relèvent de **couches
différentes** et appellent des règles différentes.

### A — Impossible physiquement → relève de la commandabilité

L'exécution ne peut pas aboutir, quel que soit l'acteur.

- panne secteur sur un équipement dépendant du secteur ;
- pont (bridge) hors ligne ;
- chemin de commande rompu (broker, passerelle, coordinateur).

> Catégorie A : la physique ne se contourne pas. Aucun acteur ne peut faire
> aboutir l'action.

### B — Interdit par politique → relève de la décision métier

L'action est *possible*, mais l'automatisme s'en abstient par règle.

- mode vacances ;
- anti-yo-yo ;
- admissibilité ;
- verrou métier (`*_autorisee`).

> Catégorie B : une politique de comportement automatique. L'action reste
> physiquement exécutable.

La frontière est nette : **A décrit ce que le système ne *peut* pas faire ;
B décrit ce que le système a *choisi* de ne pas faire automatiquement.**
Confondre les deux est l'erreur à proscrire.

---

## 6. Règle de symétrie automatique ↔ manuelle

### 6.1 Règle (catégorie A)

> **Si Arsenal sait qu'une action est physiquement impossible (catégorie A),
> aucun chemin — automatique ou manuel — ne doit la présenter comme
> exécutable.**

La commandabilité est une vérité **partagée** par tous les chemins. Si le chemin
automatique consomme une vérité d'exécution pour s'inhiber, le chemin manuel
doit consommer la **même** vérité. À défaut, l'interface ment sur la capacité
réelle d'action : elle propose un geste que le système sait voué à l'échec.

### 6.2 Pourquoi la règle ne s'applique pas à la catégorie B

Pour une interdiction de **politique** (catégorie B), la symétrie n'est **pas**
automatique. L'inhibition exprime une règle de comportement *automatique*, pas
une impossibilité. Un humain peut donc **légitimement** outrepasser une politique
depuis le chemin manuel : l'override manuel est alors une **fonctionnalité**, pas
un défaut.

> **Règle opposable :** un override manuel est légitime face à une interdiction
> de politique (B) ; il est un mensonge face à une impossibilité de
> commandabilité (A).

Sur-appliquer la symétrie à la catégorie B supprimerait l'agentivité humaine
légitime. La sous-appliquer à la catégorie A reproduirait le défaut d'origine
(une action impossible présentée comme faisable). La doctrine impose donc de
**qualifier chaque inhibition en A ou B** avant d'en déduire son traitement sur
le chemin manuel.

---

## 7. Réalisations existantes — réutilisation avant création

La commandabilité n'est pas un concept à bâtir : Arsenal en consomme déjà des
instances comme *gates* d'action. Ces signaux sont les **réalisations actuelles**
du principe.

| Signal existant | Dimension de commandabilité | Usage observé |
|---|---|---|
| `binary_sensor.boiler_bridge_online` / `sensor.boiler_bridge_sante` | capacité d'exécution du pont chaudière | gate de décision (`!= on → STOP`) |
| `binary_sensor.panne_secteur_en_cours` | dépendance secteur | inhibe des remédiations automatiques |
| `binary_sensor.systeme_stable` | stabilité / amorçage système | pré-condition transversale d'action |

À l'inverse, un signal de **supervision** (ex. la synthèse Ping LAN) qui se
déclare lui-même « couche de diagnostic » et « ne *gate* pas » **n'est pas** une
réalisation de commandabilité : il observe, il n'autorise aucun geste.

Toute application future du principe **réutilise** d'abord ces vérités existantes.
La création d'un signal n'est envisageable qu'après démonstration qu'une
disponibilité ne suffit pas **et** qu'aucun signal existant ne couvre le cas.

---

## 8. Garde-fous — philosophie Arsenal

Cette doctrine est un **principe**, pas une couche d'entités. Elle est soumise
aux invariants généraux d'Arsenal et les rappelle explicitement.

- **Une réalité unique par signal.** Chaque gate exprime une réalité d'exécution
  unique et stable. Il est **interdit** de fondre stabilité, dépendance secteur,
  santé de pont et verrous de politique dans un signal agrégateur unique.
- **Réutilisation avant création.** Le principe s'applique d'abord là où
  l'impossibilité est **déjà calculée** ; il compose des vérités existantes au
  point de consommation.
- **Aucun capteur dédié sans besoin démontré.** Un signal de commandabilité
  nouveau n'est légitime que si un cas précis prouve que disponibilité ≠
  commandabilité **et** qu'aucun signal existant ne le couvre.
- **Pas de « méga-capteur de commandabilité ».** Un verdict de commandabilité
  par action ou par équipement, agrégeant joignabilité ∧ chemin ∧ alimentation ∧
  pont, est explicitement proscrit comme dérive : il provoquerait une explosion
  combinatoire et une prolifération de capteurs contraire à la sobriété Arsenal.

> Le boiler justifie un signal de capacité explicite parce qu'il est une
> frontière d'exécution unique, critique et sous contrat transactionnel. Ce
> caractère exceptionnel n'est pas un gabarit à généraliser.

---

## 9. Statut architectural

Cette doctrine est :

- **transversale** — elle relie observation, décision, action et UI sans
  appartenir à une seule ;
- **structurante** — elle qualifie la frontière entre « ce que le système peut »
  et « ce que le système présente » ;
- **non optionnelle** — toute conception d'action ou d'affordance doit qualifier
  ses inhibitions en catégorie A (commandabilité) ou B (politique) et en déduire
  le traitement des chemins automatique et manuel. Cette qualification n'impose
  aucun gate là où aucune pré-condition physique connue n'existe.

Toute dérogation doit être explicitement justifiée dans le contrat du domaine
concerné.

---

## 10. Périmètre

La présente doctrine **formalise le concept**. Elle ne propose **aucune**
implémentation : ni capteur, ni entité, ni template, ni modification d'UI, ni
checker. L'application pratique (prises pendant une panne secteur, exposition au
chemin manuel, conséquences de rendu UI) relève des **contrats de domaine** et
de passes ultérieures délibérées, hors périmètre de ce document.

---

## 📎 Documents liés

- [`principes_generaux.md`](./principes_generaux.md) — invariants universels
  (notamment § 6 régimes d'un état externe, § 8 disponibilité explicite).
- [`separation_decision_action.md`](./separation_decision_action.md) — couches
  observation / décision / action que cette doctrine raffine.
- [`causalite_metier.md`](./causalite_metier.md) — temporalité persistante et
  autorité métier.

---

*Document normatif Arsenal. Toute dérogation doit être explicitement justifiée
dans le contrat du domaine concerné.*
