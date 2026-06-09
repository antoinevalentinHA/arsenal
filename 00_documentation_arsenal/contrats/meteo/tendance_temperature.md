# Arsenal — Contrat métier et architectural
# Famille — Tendance thermique des agrégats intérieurs (lecture glanceable)
# Version : 1.0
# Statut : normatif — famille implémentée
# Chemin : 00_documentation_arsenal/contrats/meteo/tendance_temperature.md
# Dépend de : meteo.md, affichage.md, validation.md, fallback.md
# Renvoi : extrema_jour_courant.md §9.3 (usage « tendance » de la plateforme statistics)

---

## 0. Statut et portée de ce document

Ce document est un **contrat normatif**. Il fixe la doctrine de la famille
Arsenal « tendance thermique des agrégats intérieurs », **désormais
implémentée** au runtime (couche perception `sensor.temperature_<axe>_moyenne_60_min`
— `statistics` / `mean`, fenêtre 60 min ; couche interprétation
`sensor.tendance_temperature_<axe>` — trigger template sensors ; `<axe>` ∈
{`min_chambres`, `moyenne_maison`, `max_chambres`} ; ni automatisation, ni
helper). Il sert de **référence opposable** : le comportement réel du runtime
fait foi, et ce contrat le documente.

Toute implémentation ultérieure doit être conforme aux invariants `INV-TEND-*`
ci-dessous. Tout écart d'implémentation est une non-conformité, pas une
interprétation.

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
| Minimum chambres | `sensor.temperature_min_chambres` | agrégat trigger template (min des 3 chambres) |
| Moyenne maison | `sensor.temperature_moyenne_maison` | agrégat template (moyenne 8 pièces) |
| Maximum chambres | `sensor.temperature_max_chambres` | agrégat trigger template (max des 3 chambres) |

Ces trois entités sont des **agrégats déjà qualifiés**. La présente famille les
consomme **en lecture seule stricte**. Elle ne les modifie pas, ne les renomme
pas, ne les réagrège pas et ne relit pas les capteurs de pièce sous-jacents.

### 2.2 Capteurs dérivés (à créer)

La famille crée, par axe, **deux couches** :

- une **couche statistique** (moyenne glissante de la source sur fenêtre courte) ;
- une **couche d'interprétation** exposant l'état de tendance et son icône.

Soit **3 axes**, chacun produisant un capteur de tendance consommable.

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

La décision s'appuie sur l'**écart entre la valeur instantanée de la source et
sa moyenne glissante** sur la fenêtre retenue :

```text
ecart_axe = valeur_instantanee_source − moyenne_glissante_source(fenetre)
```

- `ecart_axe > 0` significatif  → la grandeur est au-dessus de sa moyenne récente → **hausse**
- `ecart_axe < 0` significatif  → la grandeur est en dessous de sa moyenne récente → **baisse**
- `|ecart_axe|` non significatif → **stable**

Le caractère « significatif » est tranché par une **bande morte avec hystérésis**
(cf. §8).

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

Tant que la fenêtre statistique ne contient pas assez d'échantillons pour
produire une moyenne, ou tant que la source instantanée n'est pas exploitable,
**la tendance n'existe pas** : l'état exposé est `indisponible`. L'absence n'est
jamais comblée par extrapolation ni masquée (cf. INV-TEND-5).

---

## 4. Architecture canonique de la famille

Trois couches, par axe, sans pilotage et sans historique :

```text
source agrégée (existante, inchangée)
   sensor.temperature_{min_chambres | moyenne_maison | max_chambres}
        │  lecture seule
        ▼
couche statistique               ← moyenne glissante sur fenêtre courte
   (platform: statistics, state_characteristic: mean)
        │  lecture
        ▼
couche d'interprétation          ← état de tendance + icône dynamique
   {hausse | baisse | stable | indisponible}
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

**Moyenne glissante (`statistics`, `state_characteristic: mean`) sur fenêtre
courte, puis interprétation par écart instantané vs moyenne, avec bande morte et
hystérésis.**

### 5.2 Méthodes étudiées et arbitrage

| Méthode | Robustesse | Stabilité | Lisibilité | Pertinence Android Auto | Verdict |
|---|---|---|---|---|---|
| Comparaison instantanée (valeur vs valeur N min avant, en template) | Faible (échantillon unique, sensible au bruit) | Faible (scintille) | Bonne | Faible | **Écartée** |
| Fenêtre glissante `statistics` `mean` + écart instantané | Élevée (lissage) | Élevée | Élevée (écart simple) | Élevée | **Retenue** |
| Fenêtre glissante `statistics` `change` (dernier − premier) | Bonne | Bonne | Bonne | Bonne | Acceptable, mais sensible à l'échantillon de bord ; écartée au profit de `mean` |
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
3. **Robustesse et stabilité avant réactivité.** Le lissage sur fenêtre absorbe
   le bruit capteur et les micro-variations ; l'écart instantané vs moyenne est
   peu sensible à un échantillon de bord (contrairement à `change`). La bande
   morte + hystérésis (§8) supprime le scintillement — condition impérative d'un
   affichage consulté en conduite.
4. **Lisibilité.** Un écart à la moyenne récente se réduit trivialement à trois
   états ; la sémantique « la maison se réchauffe / se refroidit / est stable »
   est immédiate.
5. **Sans état, sans écrivain souverain.** La couche statistique est dérivée et
   sans persistance métier à gouverner ; aucun helper, aucune automatisation, donc
   moindre surface de maintenance et de panne.
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
tendance lui-même (jamais par une carte). Vocabulaire aligné sur celui déjà
employé dans le dépôt pour le sens thermique :

| État | Icône | Justification |
|---|---|---|
| hausse | `mdi:thermometer-chevron-up` | déjà l'icône canonique de montée thermique dans le dépôt (≈47 usages) |
| baisse | `mdi:thermometer-chevron-down` | déjà l'icône canonique de descente thermique (≈24 usages) |
| stable | `mdi:thermometer` | neutre, vocabulaire thermique de base du dépôt |
| indisponible | `mdi:thermometer-off` | déjà employé dans le dépôt pour l'absence de mesure |

L'icône est **descriptive**, jamais prescriptive : elle ne suggère aucune action
ni aucun confort souhaitable (cf. `affichage.md`, Invariant 5).

---

## 8. Seuils et hystérésis

### 8.1 Bande morte (dead-band)

La transition vers `hausse` ou `baisse` n'est déclarée que si l'écart franchit
un **seuil d'entrée** ; le retour à `stable` n'a lieu qu'en deçà d'un **seuil de
sortie** strictement inférieur. Cette **asymétrie est l'hystérésis** ; elle
empêche tout scintillement autour du seuil.

| Paramètre | Valeur recommandée | Caractère |
|---|---|---|
| Fenêtre de lissage `W` | 60 min | recommandé, surchargeable |
| Seuil d'entrée `S_in` | 0,4 °C | recommandé, surchargeable |
| Seuil de sortie `S_out` | 0,2 °C | recommandé, surchargeable (`S_out < S_in` impératif) |

### 8.2 Justification des valeurs

- **`W = 60 min`** : fenêtre suffisamment longue pour un lissage fort et une
  sémantique intuitive (« évolution sur la dernière heure »), conforme à la
  priorité *stabilité > réactivité*.
- **`S_in = 0,4 °C`** : au-delà de la résolution d'affichage (arrondi 0,1 °C) et
  du bruit typique, en deçà d'une dérive intérieure réellement perceptible sur
  une heure.
- **`S_out = 0,2 °C`** : moitié du seuil d'entrée — marge anti-rebond classique.

Ces valeurs sont des **paramètres contractuels par défaut**, ajustables sans
réécriture du contrat tant que l'invariant `S_out < S_in` est respecté. Toute
modification doit être tracée au changelog Arsenal.

---

## 9. Gestion des cas indisponibles

- Source instantanée `unknown` / `unavailable` / non numérique → tendance
  `indisponible`, icône `mdi:thermometer-off`.
- Fenêtre statistique insuffisamment alimentée (moyenne non encore disponible) →
  tendance `indisponible`.
- Aucune valeur de tendance n'est jamais figée en mémoire ni extrapolée : l'état
  d'indisponibilité est **visible et honnête** (cf. `affichage.md`, Invariant 4).
- La famille **ne déclenche aucun fallback** : elle consomme une donnée déjà
  qualifiée et s'abstient si celle-ci est absente.

---

## 10. Observabilité

Chaque capteur de tendance expose, en attributs, de quoi auditer sa décision
**sans recalcul externe** :

- l'écart courant `ecart_axe` ayant servi à la décision ;
- la moyenne glissante de référence et la fenêtre `W` appliquée ;
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
couche statistique     :  moyenne glissante de la source, fenêtre W
couche d'interprétation:  tendance_<axe>     (axe ∈ {min_chambres, moyenne_maison, max_chambres})
```

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
| Couche statistique (moyenne glissante, ×3) | référence de lissage | bloquant |
| Couche d'interprétation (tendance, ×3) | interface consommable | bloquant |

Consommateur aval **nommé** : la catégorie *Favoris* de l'interface de conduite
Home Assistant (Android Auto), configurée dans l'application compagnon, hors
dépôt.

---

## 13. Recorder

| Population | Doctrine |
|---|---|
| Couche statistique (moyenne glissante) | inclusion `recorder` **uniquement** si un graphe historique la consomme ; aucun à ce jour ⇒ ne rien ajouter |
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
  automatisation dédiée — la couche statistique porte le lissage.
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
| INV-TEND-6 | La décision repose sur une statistique lissée sur fenêtre, jamais sur une comparaison d'échantillon instantané. |
| INV-TEND-7 | Hystérésis obligatoire : seuils d'entrée et de sortie asymétriques (`S_out < S_in`) pour interdire tout scintillement. |
| INV-TEND-8 | À chaque état correspond une et une seule icône, portée par le capteur lui-même, descriptive et non prescriptive. |
| INV-TEND-9 | La famille est homogène sur les trois axes ; aucun axe n'est un cas particulier. |
| INV-TEND-10 | Toute couche exposée a un consommateur réel et nommé ; aucune couche orpheline. |
| INV-TEND-11 | La fenêtre glissante sert exclusivement à qualifier une tendance ; elle n'est jamais source d'un extrême du jour (renvoi `extrema_jour_courant.md` §9 ; usage légitimé §9.3). |
| INV-TEND-12 | La tendance n'a aucune autorité décisionnelle : aucun pilotage d'équipement, aucun déclenchement d'automatisation métier. |

---

## 17. Extensions futures envisagées

- amplitude récente (`max − min` sur fenêtre) en attribut d'observabilité ;
- couche couleur dédiée si un dashboard (hors Android Auto) en exprime le besoin,
  sous contrat séparé et avec consommateur nommé ;
- tendance d'autres grandeurs déjà affichées en conduite (ECS, humidité),
  par réplication du même gabarit, sous décision explicite.

Aucune de ces extensions n'a de valeur normative à ce stade.

---

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-06-09 | Promotion en contrat normatif : la famille « tendance thermique des agrégats intérieurs » est implémentée au runtime (couche perception `sensor.temperature_<axe>_moyenne_60_min` — `statistics`/`mean`, fenêtre 60 min ; couche interprétation `sensor.tendance_temperature_<axe>` — trigger template sensors, hystérésis `S_in`=0.4 / `S_out`=0.2, écart arrondi au centième, `time_pattern` 5 min ; ni automatisation ni helper) et conforme aux invariants `INV-TEND-*`. Grammaire de nommage (§11) désormais figée aux valeurs ci-dessus. Cadrage « pré-contrat / avant implémentation » retiré. |
| 0.1.0 | 2026-06-09 | Brouillon pré-normatif initial — formalisation de la famille « tendance thermique des agrégats intérieurs » destinée aux Favoris Android Auto : nature métier (écart instantané vs moyenne glissante), méthode retenue (`statistics`/`mean` + interprétation à bande morte et hystérésis), états fermés, icônes dynamiques, gestion d'indisponibilité, observabilité, exclusions et invariants `INV-TEND-*`. Avant implémentation : aucun identifiant figé, aucune entité existante modifiée. |
