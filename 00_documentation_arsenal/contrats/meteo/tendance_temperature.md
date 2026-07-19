# Arsenal — Contrat métier et architectural
# Famille — Tendance thermique des agrégats intérieurs (lecture glanceable)
# Version : 1.1
# Statut : normatif — doctrine de décision amendée ; runtime en écart temporaire (voir §0 et §18)
# Chemin : 00_documentation_arsenal/contrats/meteo/tendance_temperature.md
# Dépend de : meteo.md, affichage.md, validation.md, fallback.md
# Renvoi : extrema_jour_courant.md §9.3 (usage « tendance » de la plateforme statistics)
#          audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md (constat fondant l'amendement v1.1)

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

**État d'implémentation au moment de l'amendement.** Le runtime
(`13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`,
`12_template_sensors/meteo/tendance/temperature.yaml`) implémente **encore la
grandeur dépréciée v1.0**. Il existe donc un **écart temporaire assumé** entre ce
contrat (v1.1, doctrine cible) et le runtime (v1.0). Cet écart est **explicitement
tracé en §18** et sera résorbé dans une **passe runtime ultérieure** ; il n'est ni
une non-conformité cachée, ni une dérive tolérée indéfiniment.

Toute implémentation ultérieure doit être conforme aux invariants `INV-TEND-*`
ci-dessous, dans leur version v1.1. Tout écart d'implémentation **non tracé en
§18** est une non-conformité, pas une interprétation.

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

La famille crée, par axe, **trois couches** (doctrine cible v1.1) :

- une **couche statistique « moyenne courte »** (moyenne glissante de la source
  sur fenêtre courte `W_court`) ;
- une **couche statistique « moyenne longue »** (moyenne glissante de la source
  sur fenêtre longue `W_long`) ;
- une **couche d'interprétation** exposant l'état de tendance et son icône, à
  partir de l'**écart entre les deux moyennes**.

Soit **3 axes**, chacun produisant un capteur de tendance consommable.

> **Note d'écart (v1.0 → v1.1).** La v1.0 ne créait qu'**une** couche statistique
> (moyenne longue 60 min) et comparait la **valeur instantanée** à cette moyenne.
> La couche « moyenne courte » est **nouvelle** et reste **à créer** en passe
> runtime (cf. §18). Aucun identifiant n'est figé ici (§11).

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

> **Note d'écart.** Le runtime applique encore la grandeur v1.0 dépréciée ; voir
> §18 (écart temporaire contrat ↔ runtime).

### 3.3 Donnée exploitable

La couche d'interprétation considère la source comme **exploitable** si et
seulement si sa valeur instantanée est **numérique** (ni `unknown`, ni
`unavailable`, ni `none`, ni chaîne vide).

La famille **ne réapplique aucune plage de plausibilité** sur les sources : la
qualification physique est de la responsabilité de l'amont (les agrégats, et en
deçà les contrats d'axe `meteo.md` / `validation.md` / `fallback.md`). Réappliquer
ici une borne reviendrait à dupliquer une autorité de validation, ce que le
domaine météo interdit (source unique de vérité par couche).

### 3.4 Absence de tendance

Tant que **l'une des deux** fenêtres statistiques (courte ou longue) ne contient
pas assez d'échantillons pour produire sa moyenne, ou tant que la source n'est pas
exploitable, **la tendance n'existe pas** : l'état exposé est `indisponible`.
L'absence n'est jamais comblée par extrapolation ni masquée (cf. INV-TEND-5).

---

## 4. Architecture canonique de la famille

Quatre couches, par axe, sans pilotage et sans historique (doctrine cible v1.1) :

```text
source agrégée (existante, inchangée)
   sensor.temperature_{min_chambres | moyenne_maison | max_chambres}
        │  lecture seule
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

### 8.2 Cibles candidates v1.1 — à valider sur le bruit réel (NON figées)

> **Statut de ces valeurs.** Ce sont des **cibles candidates / valeurs initiales**,
> **pas** des valeurs définitives. Le **plancher de bruit réel** des trois
> agrégats n'a pas encore été mesuré (cf. audit sensibilité §9, tests 1–3). Elles
> doivent être **validées sur données runtime avant figement**. Tant que cette
> validation n'a pas eu lieu, aucune de ces valeurs ne devient un défaut
> contractuel opposable.

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

## 11. Convention de nommage (gabarit cible — non figé)

Le présent contrat **n'invente aucun identifiant d'entité ni `unique_id`**
(interdiction `contrats/README.md`). Il fixe seulement une **grammaire cible**,
à arrêter à l'implémentation :

```text
couche statistique courte :  moyenne glissante de la source, fenêtre W_court
couche statistique longue :  moyenne glissante de la source, fenêtre W_long
couche d'interprétation   :  tendance_<axe>     (axe ∈ {min_chambres, moyenne_maison, max_chambres})
```

> **Note d'écart.** Le runtime v1.0 ne porte qu'une couche statistique longue
> (`sensor.temperature_<axe>_moyenne_60_min`, identifiant existant **non renommé**).
> La couche courte est à créer ; son identifiant définitif relève de la passe
> runtime et sera tracé au changelog (le présent contrat n'en fige aucun).

La grammaire doit être **homogène sur les trois axes** : aucun axe n'est un cas
particulier de nommage. Les identifiants définitifs relèvent de l'implémentation
et seront tracés au changelog.

---

## 12. Dépendances

| Dépendance | Rôle | Caractère |
|---|---|---|
| `sensor.temperature_min_chambres` | source agrégée — lue | bloquant (lecture) |
| `sensor.temperature_moyenne_maison` | source agrégée — lue | bloquant (lecture) |
| `sensor.temperature_max_chambres` | source agrégée — lue | bloquant (lecture) |
| Couche statistique courte (moyenne glissante `W_court`, ×3) | référence récente | bloquant (à créer, cf. §18) |
| Couche statistique longue (moyenne glissante `W_long`, ×3) | référence de fond | bloquant |
| Couche d'interprétation (tendance, ×3) | interface consommable | bloquant |

Consommateur aval **nommé** : la catégorie *Favoris* de l'interface de conduite
Home Assistant (Android Auto), configurée dans l'application compagnon, hors
dépôt.

---

## 13. Recorder

| Population | Doctrine |
|---|---|
| Couches statistiques (moyennes glissantes courte et longue) | inclusion `recorder` **uniquement** si un graphe historique les consomme ; aucun à ce jour ⇒ ne rien ajouter |
| Couche d'interprétation (tendance) | état catégoriel ; inclusion `recorder` **uniquement** si un historique d'état est explicitement souhaité ; sinon, ne rien ajouter |

Le `recorder` Arsenal fonctionne en liste blanche : aucune entité de cette
famille n'y est ajoutée tant qu'un consommateur historique réel n'est pas nommé
(cf. clause anti-couche-orpheline, INV-TEND-10).

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
  architecturale : rattachement météo justifié, nouveau domaine non justifié).

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
| INV-TEND-14 | Tout écart entre ce contrat et le runtime doit être **explicitement tracé en §18** ; un écart non tracé reste une non-conformité. |

---

## 17. Extensions futures envisagées

- amplitude récente (`max − min` sur fenêtre) en attribut d'observabilité ;
- couche couleur dédiée si un dashboard (hors Android Auto) en exprime le besoin,
  sous contrat séparé et avec consommateur nommé ;
- tendance d'autres grandeurs déjà affichées en conduite (ECS, humidité),
  par réplication du même gabarit, sous décision explicite.

Aucune de ces extensions n'a de valeur normative à ce stade.

---

## 18. Écart temporaire contrat ↔ runtime (v1.1)

Cette section **trace** l'écart, **assumé et borné**, entre la doctrine cible
v1.1 (ci-dessus) et le runtime actuel, qui implémente encore la grandeur v1.0
dépréciée. Elle satisfait `INV-TEND-13` et `INV-TEND-14`.

### 18.1 Nature de l'écart

| Aspect | Contrat v1.1 (cible) | Runtime actuel (v1.0) |
|---|---|---|
| Grandeur de décision | `moyenne_courte − moyenne_longue` | `valeur_instantanée − moyenne_60_min` |
| Couches statistiques | 2 (courte + longue) | 1 (longue, `..._moyenne_60_min`) |
| Seuils | cibles candidates `S_in≈0,15` / `S_out≈0,08` (à valider) | `S_in=0,4` / `S_out=0,2` |
| Symptôme | — | faux `stable` sur rampes lentes (audit §4) |

### 18.2 Statut

- L'écart est **connu, documenté et volontaire** : le contrat est amené **en
  avance** sur le runtime pour fixer le besoin avant la correction.
- Le runtime n'est **pas** modifié dans la passe documentaire qui produit cette
  v1.1 : aucun YAML, aucun capteur, aucun helper, aucune automatisation touchés.
- L'écart **n'est pas indéfini** : il est résorbé par la passe runtime décrite en
  §18.3.

### 18.3 Passe runtime à venir (préparation, non exécutée ici)

Fichiers à aligner sur la doctrine v1.1, en respectant lecture seule des sources,
aucun renommage d'entité existante, aucun alias modifié :

1. `13_sensor_platforms/statistics/meteo/tendance_temperature.yaml`
   — ajouter, par axe, la **moyenne courte** (`statistics`/`mean`, `max_age`
   ≈ `W_court`) ; conserver la moyenne longue existante **sans la renommer**.
2. `12_template_sensors/meteo/tendance/temperature.yaml`
   — remplacer la grandeur de décision par `moyenne_courte − moyenne_longue` ;
   appliquer les seuils validés (après mesure du bruit, audit §9) ; écouter la
   moyenne courte en trigger ; mettre à jour les attributs d'observabilité (§10).

Préalable bloquant : **mesure du plancher de bruit réel** (audit
[`audit_tendance_temperature_sensibilite.md`](../../audits/01_rapports/meteo/audit_tendance_temperature_sensibilite.md)
§9, tests 1–3) avant figement des seuils. Tant que cette passe runtime n'est pas
faite, le symptôme « faux `stable` » **persiste en production** : c'est le coût
assumé de l'écart, préféré à une correction runtime non validée.

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.1 | 2026-06-17 | **Amendement doctrinal de la grandeur de décision.** Dépréciation de `valeur_instantanée − moyenne_60_min` (saturation `r × W/2` sur rampes lentes ⇒ faux `stable`, cf. audit `audit_tendance_temperature_sensibilite.md`). Adoption de la grandeur lissée `moyenne_courte − moyenne_longue` (§3.2, §5) ; passage à 2 couches statistiques (§2.2, §4, §12) ; cibles candidates **non figées** `W_long=60`, `W_court≈15`, `S_in≈0,15`, `S_out≈0,08` à valider sur le bruit réel (§8). Invariants : INV-TEND-6 reformulé (écart entre deux statistiques lissées), ajout INV-TEND-13 (grandeur v1.0 dépréciée) et INV-TEND-14 (traçage des écarts). Section §18 « écart temporaire contrat ↔ runtime » ajoutée. **Aucune modification runtime** dans cette passe : le runtime applique encore la v1.0 ; correction reportée à une passe ultérieure (§18.3). Invariants structurants conservés : backend interprète / UI restitue, états fermés, indisponibilité honnête, hystérésis obligatoire, lecture seule des sources, aucune autorité décisionnelle. |
| 1.0 | 2026-06-09 | Promotion en contrat normatif : la famille « tendance thermique des agrégats intérieurs » est implémentée au runtime (couche perception `sensor.temperature_<axe>_moyenne_60_min` — `statistics`/`mean`, fenêtre 60 min ; couche interprétation `sensor.tendance_temperature_<axe>` — trigger template sensors, hystérésis `S_in`=0.4 / `S_out`=0.2, écart arrondi au centième, `time_pattern` 5 min ; ni automatisation ni helper) et conforme aux invariants `INV-TEND-*`. Grammaire de nommage (§11) désormais figée aux valeurs ci-dessus. Cadrage « pré-contrat / avant implémentation » retiré. |
| 0.1.0 | 2026-06-09 | Brouillon pré-normatif initial — formalisation de la famille « tendance thermique des agrégats intérieurs » destinée aux Favoris Android Auto : nature métier (écart instantané vs moyenne glissante), méthode retenue (`statistics`/`mean` + interprétation à bande morte et hystérésis), états fermés, icônes dynamiques, gestion d'indisponibilité, observabilité, exclusions et invariants `INV-TEND-*`. Avant implémentation : aucun identifiant figé, aucune entité existante modifiée. |
