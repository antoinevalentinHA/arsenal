# 🎛️ ARSENAL — Couleurs UI : Exceptions contrôlées

## Objet

Ce document documente les **exceptions contrôlées et opposables**
à la palette sémantique principale Arsenal, sans s'y substituer. 

Ces exceptions ne remplacent pas la palette — elles s'y superposent
dans un contexte strict, catégoriel et documenté.

Toute exception non documentée ici est **invalide**.

---

## Règle générale des exceptions

Une exception contrôlée est autorisée si et seulement si :
- elle est **catégorielle** (liée à un domaine métier précis)
- elle est **non décisionnelle** (ne porte pas de jugement OK/KO)
- elle est **documentée ici** avec son périmètre strict
- elle ne **masque jamais** un état d'indisponibilité
- elle ne **modifie pas** la hiérarchie sémantique globale

---

## Exception 1 — Modes HVAC

### Objet

Dans les cartes de pilotage et d'état HVAC (chauffage, climatisation),
les couleurs identifient visuellement un **mode de fonctionnement**.
Elles ne portent aucun jugement métier (OK / KO / WARN).

Cette exception est **catégorielle**, non décisionnelle.

### Mapping autorisé (uniquement)

| Couleur | Valeur | Mode |
|---------|--------|------|
| 🔵 Bleu | `rgba(33, 150, 243, 0.2)` | `cool` |
| 🟢 Vert | `rgba(76, 175, 80, 0.2)` | `dry` |
| 🔴 Rouge | `rgba(244, 67, 54, 0.2)` | `heat` |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | `off` / veille / absence de mode |

### Priorité

En cas d'état indisponible (`unknown` / `unavailable`) :
le gris indisponibilité `rgba(158, 158, 158, 0.1)` prime
sur toute couleur de mode.

### 🚫 Interdits

- Utiliser ce mapping pour exprimer un statut (OK / KO / WARN / indispo)
- Étendre ce mapping à d'autres domaines que HVAC
- Introduire d'autres nuances ou d'autres opacités
- Masquer un état d'indisponibilité par une couleur de mode

---

## Exception 2 — Palette thermique (ECS / Température)

### Objet

Autoriser un codage visuel basé sur une logique **physique thermique**
(froid / valeur dans la plage attendue / chauffe en cours / chaud),
distinct de la sémantique métier OK / KO / WARN / INFO.

Cette exception est strictement limitée aux cartes :
- ECS
- Température technique
- Indicateurs thermiques physiques

Elle ne constitue pas un jugement métier.

### Mapping autorisé (uniquement)

| Couleur | Valeur | État thermique |
|---------|--------|---------------|
| 🔵 Bleu froid | `rgba(144, 202, 249, 0.25)` | Froid / température basse |
| 🟢 Vert dans la plage | `rgba(76, 175, 80, 0.2)` | Valeur dans la plage attendue — aucun franchissement du seuil physique défavorable (catégorie `dans_plage`) |
| 🟠 Orange | `rgba(255, 152, 0, 0.2)` | Chauffe en cours |
| 🔴 Rouge | `rgba(244, 67, 54, 0.2)` | Température haute / cible atteinte |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | Cas thermique neutre ou catégorie thermique non déterminée, uniquement lorsqu'un contrat le prévoit explicitement |
| ⚪ Gris indispo | `rgba(158, 158, 158, 0.1)` | `unknown` / `unavailable` |

### Catégorie physique `dans_plage` (vert thermique)

Le vert thermique `rgba(76, 175, 80, 0.2)` code une **catégorie physique
`dans_plage`, strictement bornée** (à perception positive, sans jugement `OK`
autonome) : la valeur de l'indicateur **ne franchit pas** son seuil physique
défavorable. La réalité gouvernante est la **comparaison physique**, pas le
caractère « positif » de la couleur ; `dans_plage` n'est pas une quatrième
famille sémantique générale.

- **Sens unique et opposable** : « valeur dans la plage attendue pour
  l'indicateur concerné, sans franchissement du seuil physique défavorable ».
- **Égalité exacte traitée positivement** : une couleur défavorable
  (bleu froid ou rouge chaud) n'apparaît qu'au **franchissement strict et
  démontré** du seuil physique défavorable ; à l'égalité exacte avec la
  référence, l'état reste `dans_plage`.
- **Ce vert ne signifie jamais** : confort global, conformité à une consigne,
  absence de besoin HVAC, autorisation, décision, action, nominalité système,
  ni absence de toute anomalie système. Il ne qualifie que **la seule grandeur
  physique de l'indicateur**.
- **Activation par contrat uniquement** : ce vert n'est disponible que
  **lorsqu'un contrat définit explicitement**, pour l'indicateur concerné, la
  catégorie physique `dans_plage`. Il **n'est pas** généralisé automatiquement
  à tous les indicateurs thermiques : les indicateurs thermiques existants sans
  cette catégorie restent **inchangés**, et aucun indicateur (bornes de service
  ECS ou autre) sans vert n'est **automatiquement migré**.
- **Aucun mélange de palettes** : le vert appartient désormais à l'Exception 2
  elle-même. Un indicateur thermique qui l'emploie reste **intégralement**
  dans la palette thermique (bleu froid / vert `dans_plage` / orange / rouge /
  gris) et **n'emprunte pas** le vert de la palette sémantique générale. La
  valeur RGBA est identique au vert canon Arsenal, mais son **régime** ici est
  **thermique et catégoriel**, non sémantique métier.

### Priorité

L'indisponibilité prime toujours (`rgba(158, 158, 158, 0.1)`).

Le **gris neutre `0.2`** (cas thermique neutre ou catégorie thermique non
déterminée, prévu par le contrat concerné) et le **gris indisponibilité `0.1`**
(`unknown` / `unavailable`) restent **deux réalités distinctes** : le second
prime et ne doit jamais être masqué par le premier. Un contrat peut ne prévoir
**aucun état gris neutre `0.2`**. En revanche, lorsqu'un indicateur est
`unknown` ou `unavailable`, le **gris indisponibilité `0.1` reste obligatoire et
prioritaire**.

### 🚫 Interdits

- Utiliser cette palette hors contexte thermique
- Introduire d'autres nuances de bleu froid
- Toute variation d'opacité non documentée ci-dessus
- Mélanger palette thermique et palette d'alerte métier
  dans une même logique décisionnelle
- Utiliser le bleu thermique `rgba(144, 202, 249, 0.25)`
  pour encoder un statut métier
- Décrire le vert `dans_plage` comme un confort global, une conformité à une
  consigne, une autorisation / décision / action HVAC, ou une nominalité
  système
- Généraliser le vert `dans_plage` à un indicateur thermique dont le contrat
  ne définit pas explicitement la catégorie physique `dans_plage`
- Faire apparaître une couleur défavorable (bleu froid ou rouge chaud) sans
  franchissement **strict** du seuil physique défavorable

---

## Exception 3 — Couleurs dynamiques d'icône en contexte NAV/HUB

### Objet

Dans le cadre strict des tuiles de navigation (NAV/HUB),
l'icône peut refléter dynamiquement un état global
via une couleur **pleine (opaque)** dérivée de la palette Arsenal.

Cette exception concerne **uniquement l'icône**,
dans un contexte de navigation structurelle exclusivement.

### Couleurs autorisées (versions opaques uniquement)

| Couleur | Valeur | Signification |
|---------|--------|--------------|
| 🔴 Rouge | `rgb(244, 67, 54)` | État d'alerte |
| 🟢 Vert | `rgb(76, 175, 80)` | État favorable |
| 🔵 Bleu | `rgb(33, 150, 243)` | État normal / informatif |
| ⚪ Gris | `rgb(158, 158, 158)` | Neutre / standby / off |

### Priorité sémantique

La hiérarchie sémantique globale reste inchangée :

🔴 > 🟠 > 🟢 > 🔵 > ⚪

### 🚫 Interdits

- Toute autre nuance de bleu
  (ex : `rgb(25, 118, 210)`, `rgb(144, 202, 249)`)
- Toute autre nuance de rouge ou de vert
- Utilisation de ces couleurs opaques hors contexte NAV/HUB
- Application de ces couleurs opaques au fond des cartes NAV
- Utilisation de ces couleurs opaques sur des cartes métier

---

## Exception 4 — Couleur structurelle NAV/HUB

### Objet

Couleur de fond réservée aux tuiles de navigation et aux hubs.
Structure UI pure, non sémantique.

Cette exception ne porte :
- aucun état métier,
- aucune sévérité,
- aucune décision.

Elle constitue uniquement une primitive structurelle UI.

### Couleur officielle

| Usage | Valeur |
|-------|--------|
| Fond NAV/HUB | `rgba(90, 110, 130, 0.08)` |

### Règles d'usage

- Réservé aux tuiles de navigation (menu / hub)
- Ne doit jamais encoder un état (OK / KO / WARN / OFF / unknown)
- Compatible avec icônes colorées dynamiques
- Stable et non dynamique

### 🚫 Interdits

- Utiliser cette couleur hors contexte NAV/HUB
- Utiliser cette couleur pour signaler un statut métier
- Faire varier son opacité
- Utiliser cette couleur comme fond de carte métier

---

## Exception 5 — Visualisations quantitatives

### Objet

Autoriser des variations d'opacité renforcées dans les composants
de visualisation quantitative :
- `bar-card`
- `mini-graph-card`
- `apexcharts-card`
- séries graphiques
- graphes temporels
- répartitions quantitatives

Cette exception concerne exclusivement :
- la lisibilité graphique,
- la distinction visuelle des séries,
- l'intensité de représentation quantitative.

Elle ne constitue pas une sémantique métier autonome.

### Principes

Les couleurs utilisées restent dérivées de la palette Arsenal,
mais peuvent utiliser des opacités renforcées pour améliorer :
- contraste,
- lisibilité,
- hiérarchie visuelle des séries,
- perception quantitative.

### Variations autorisées

Exemples autorisés :

| Couleur dérivée | Usage |
|----------------|------|
| `rgba(..., 0.6)` | Série secondaire |
| `rgba(..., 0.8)` | Série principale |
| `rgba(..., 0.85)` | Répartition dominante |
| `rgba(..., 0.9)` | Mise en évidence quantitative |

### Scope strict

Cette exception est limitée :
- aux composants graphiques,
- aux graphes,
- aux séries quantitatives,
- aux répartitions visuelles.

Elle ne s'applique jamais :
- aux cartes décisionnelles,
- aux cartes de synthèse métier,
- aux fonds de cartes métier,
- aux badges de statut,
- aux indicateurs d'alerte.

### Priorité

Les règles suivantes restent absolues :
- le gris indisponibilité prime toujours,
- les couleurs ne décident jamais,
- la hiérarchie sémantique globale reste inchangée.

### 🚫 Interdits

- Introduire des couleurs hors palette Arsenal
- Utiliser ces opacités renforcées sur des cartes métier classiques
- Utiliser ces opacités pour encoder une sévérité autonome
- Utiliser des couleurs opaques pleines hors contexte documenté
- Utiliser cette exception comme justification d'une dérive UI générale

---

## Exception 6 — Accentuation visuelle des états intermédiaires

### Objet

Autoriser une accentuation perceptive modérée des états
intermédiaires dans certaines cartes :
- interprétatives,
- KPI,
- supervision,
- seuils progressifs,
- transitions non critiques.

Cette exception permet d'améliorer :
- lisibilité,
- hiérarchie perceptive,
- distinction visuelle des niveaux intermédiaires.

Elle ne modifie pas la sémantique métier de la palette Arsenal.

### Scope autorisé

Cette exception est limitée :
- aux cartes KPI,
- aux cartes interprétatives,
- aux seuils progressifs,
- aux états transitoires,
- aux niveaux de vigilance non critiques.

Exemples typiques :
- bruit / acoustique,
- pluie récente,
- supervision UPS,
- états `transition`,
- états `stale`,
- seuils batterie/autonomie.

### Variantes autorisées

| Couleur | Valeur | Usage |
|---------|--------|------|
| 🟡 Jaune renforcé | `rgba(255, 193, 7, 0.25)` | Vigilance intermédiaire |
| 🟠 Orange renforcé | `rgba(255, 152, 0, 0.25)` | Warning modéré |
| 🟠 Orange transition | `rgba(255, 152, 0, 0.20)` | Transition faible |
| 🟠 Orange accentué | `rgba(255, 152, 0, 0.30)` | Transition forte |

### Principes

Ces variantes :
- restent dérivées de la palette Arsenal,
- ne constituent pas de nouvelles couleurs sémantiques,
- ne modifient pas la hiérarchie globale,
- ne remplacent jamais le rouge critique,
- ne remplacent jamais le gris indisponibilité.

### 🚫 Interdits

- Étendre ces opacités à toute l'UI Arsenal
- Utiliser ces variantes dans des cartes décisionnelles
- Introduire d'autres opacités intermédiaires non documentées
- Utiliser ces variantes pour encoder une nouvelle sévérité
- Transformer cette exception locale en palette parallèle

---

## Exception 7 — Palette hydrique / précipitations

### Objet

Autoriser une palette bleue dédiée à la représentation
des phénomènes hydriques :
- pluie,
- précipitations,
- intensité hydrique,
- cumul d'eau,
- phénomènes météorologiques liés à l'eau.

Cette exception est :
- catégorielle,
- quantitative,
- non décisionnelle.

Elle ne constitue pas une sémantique métier Arsenal.

### Scope autorisé

Cette exception est strictement limitée :
- aux cartes de précipitations,
- aux intensités de pluie,
- aux cumuls hydriques,
- aux graphes hydriques,
- aux indicateurs météo liés à l'eau.

Elle ne s'applique pas :
- aux cartes métier générales,
- aux statuts système,
- aux dashboards de supervision,
- aux KPI non hydriques,
- aux états décisionnels Arsenal.

### Palette autorisée

| Niveau | Valeur | Signification |
|--------|--------|---------------|
| 🔵 Bleu clair | `rgba(187, 222, 251, 0.3)` | Pluie faible |
| 🔵 Bleu moyen | `rgba(100, 181, 246, 0.3)` | Pluie modérée |
| 🔵 Bleu soutenu | `rgba(30, 136, 229, 0.35)` | Forte pluie |

### Principes

Cette palette :
- représente une intensité hydrique,
- ne représente jamais un statut métier,
- ne remplace jamais la palette Arsenal,
- reste limitée au domaine météorologique hydrique.

### Priorité

Les règles suivantes restent absolues :
- le gris indisponibilité prime toujours,
- la hiérarchie sémantique Arsenal reste inchangée,
- cette palette ne peut jamais encoder :
  - OK,
  - WARN,
  - CRITIQUE,
  - OFF,
  - indisponibilité.

### 🚫 Interdits

- Étendre cette palette à toute la météo Arsenal
- Utiliser ces bleus hors contexte hydrique
- Utiliser cette palette dans des cartes métier
- Utiliser cette palette pour représenter une sévérité système
- Introduire d'autres nuances hydriques non documentées
---

## Exception 8 — Échelle absolue Humidex (risque chaud/humide)

### Objet

Autoriser un codage visuel de l'**humidex** fondé sur son **échelle
d'interprétation absolue** (paliers fixes Environnement Canada), en
lieu et place de la qualification relative du mécanisme A.

L'humidex est un indice de stress chaud/humide doté d'une échelle
absolue largement admise : une même valeur a la même signification
quelle que soit la normale locale récente. La couleur exprime donc un
**niveau absolu**, pas un écart à une enveloppe glissante.

Cette exception est **catégorielle** (strictement humidex) et
**perceptive UI** : elle ne pilote aucune décision runtime.

### Scope autorisé

Strictement limité aux capteurs `couleur_humidex_*`
(`12_template_sensors/couleurs/meteo/humidex.yaml`) et à leur
projection dans le socle KPI.

Ne s'applique pas :
- aux autres grandeurs du mécanisme A (température, humidité relative,
  humidité absolue), qui restent en qualification relative,
- aux seuils opérationnels climatisation / DRY,
- à toute autre carte métier.

### Apex de l'axe rouge — `dark_red`

Cette exception **n'ajoute pas une couleur canon générale**. Elle
introduit un **apex de l'axe rouge**, réservé au palier humidex le
plus sévère (« coup de chaleur imminent »), strictement au-dessus du
rouge standard.

| Palier humidex | Clé | Valeur | Interprétation (Env. Canada) |
|----------------|-----|--------|------------------------------|
| `< 30` | `green` | `rgba(76, 175, 80, 0.2)` | aucun inconfort |
| `30 – 39` | `yellow` | `rgba(255, 235, 59, 0.2)` | un certain inconfort |
| `40 – 44` | `orange` | `rgba(255, 152, 0, 0.2)` | beaucoup d'inconfort |
| `45 – 54` | `red` | `rgba(244, 67, 54, 0.2)` | danger (coup de chaleur probable) |
| `>= 55` | `dark_red` | `rgba(183, 28, 28, 0.2)` | coup de chaleur imminent |
| invalide / non numérique | `grey` | `rgba(158, 158, 158, 0.2)` | donnée indisponible |

Seul `dark_red` (`rgba(183, 28, 28, 0.2)`, Material Red 900, opacité
canon 0.2) est nouveau ; les autres clés sont du canon Arsenal existant.

### Priorité

- Le gris indisponibilité prime toujours.
- `dark_red` est un **renforcement** de la criticité rouge, jamais un
  axe sémantique concurrent : la règle « le rouge prime toujours »
  reste valable (`dark_red` est un rouge maximal).

### 🚫 Interdits

- Propager `dark_red` comme couleur canon générale hors humidex.
- Réutiliser `dark_red` pour un autre domaine ou une autre sévérité.
- Réintroduire une qualification relative (enveloppe glissante) pour
  l'humidex.
- Encoder l'humidex avec une couleur « froid » : l'échelle absolue
  n'a pas de sémantique de froid (`< 30` → `green`).

---

## Exception 9 — Sens de commande des volets (montée / arrêt / descente)

### Objet

Dans les tuiles d'**action** du domaine Volets, la couleur identifie
visuellement le **sens de la commande** émise (montée, arrêt, descente).
Elle ne porte **aucun jugement métier** (OK / KO / WARN / INFO) et ne
reflète **aucun état** du volet.

Cette distinction est nécessaire car les volets Budendorf n'exposent
**aucun retour d'état** : la tuile ne peut donc traduire qu'une
**intention de commande**, jamais une position réelle. En l'absence
d'état, distinguer les trois commandes par la couleur améliore la
lisibilité et réduit le risque d'erreur de manipulation.

Cette exception est **catégorielle** (strictement Volets / action) et
**non décisionnelle**, sur le modèle exact de l'**Exception 1 — Modes
HVAC** : elle réemploie des valeurs RGBA canon pour un usage catégoriel,
sans introduire ni nuance ni opacité nouvelle.

### Périmètre strict

Réservée aux tuiles d'action volets (spécialisations `shutter_open`,
`shutter_stop`, `shutter_close` de `shutter_action_base`,
couche `10_action/` du domaine `40_dashboards/volets/`).

Ne s'applique pas :
- aux cartes de décision / exposition / KPI pluie (palette sémantique),
- à toute autre tuile d'action d'un autre domaine,
- à aucune carte portant un état ou une sévérité.

### Mapping autorisé (uniquement)

| Couleur | Valeur | Sens de commande |
|---------|--------|------------------|
| 🟢 Vert | `rgba(76, 175, 80, 0.2)` | `montée` — ouverture |
| 🟠 Orange | `rgba(255, 152, 0, 0.2)` | `arrêt` — interruption du mouvement |
| 🔵 Bleu | `rgba(33, 150, 243, 0.2)` | `descente` — fermeture |
| ⚪ Gris neutre | `rgba(158, 158, 158, 0.2)` | commande volet sans sens directionnel typé |

Le vert ne signifie **jamais** ici « OK / autorisé », l'orange **jamais**
« avertissement », le bleu **jamais** « information ». Ces couleurs
encodent exclusivement un **sens de commande**, à l'image des modes HVAC.

### Priorité

La hiérarchie sémantique globale reste inchangée (`05_regles.md`).
Ces tuiles ne lisant aucun état, elles ne peuvent jamais entrer en
concurrence avec une couleur sémantique : elles n'expriment qu'une
intention de commande. Si une tuile d'action venait à lire un état
(retour de position à l'avenir), l'indisponibilité
`rgba(158, 158, 158, 0.1)` primerait comme partout.

### 🚫 Interdits

- Utiliser ce mapping pour exprimer un statut (OK / KO / WARN / indispo)
- Étendre ce mapping hors des tuiles d'action du domaine Volets
- Introduire d'autres nuances ou d'autres opacités
- Colorer une tuile d'action volet sans qu'elle corresponde à l'un des
  trois sens documentés (montée / arrêt / descente)
- Décrire ces couleurs comme décoratives : elles encodent un sens de
  commande catégoriel, seule justification recevable
