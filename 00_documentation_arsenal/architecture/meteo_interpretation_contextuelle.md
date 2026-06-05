# 🧠 ARSENAL — ARCHITECTURE · Interprétation météo contextuelle

> **Modèle d'interprétation d'une grandeur météo : sa lecture relativement à une référence contextuelle et à une enveloppe de confort dynamique, dont la couleur n'est que la projection terminale.**

## 📌 Statut du document

- **Type** : Architecture / documentation de référence
- **Domaine** : Météo — interprétation & qualification (couche *amont* de l'affichage)
- **Caractère** : **Descriptif** — ce document *décrit* le mécanisme observé ; il n'impose rien.
- **Autorité** : aucune. En cas de divergence, **le runtime fait foi**, et le contrat `contrats/meteo/affichage.md` prime pour tout ce qui concerne la restitution.
- **Dépendances (lecture)** :
  - `architecture/capteurs_meteo.md` (mesures, période météo, seuils dynamiques)
  - `contrats/meteo/affichage.md` (contrat de restitution)
  - `ui/couleurs/` (charte des couleurs)
- **Périmètre** : le mécanisme principal du domaine, dit ici **mécanisme A** — interprétation des grandeurs disposant d'un capteur couleur dédié : **température, humidité relative, humidité absolue, humidex**. Les autres mécanismes (CO₂ à seuils fixes, précipitations, cohérence inter-capteurs, prévisions) **sont hors périmètre** (cf. §6).

---

## 🧪 Convention de statut épistémique

Ce document distingue explicitement quatre registres. Chaque affirmation porteuse est préfixée :

- **[F] Fait démontré** — vérifiable dans le runtime exécutable et/ou un document du dépôt (source indiquée).
- **[I] Intention documentée** — intention de conception *écrite* dans le dépôt (commentaire de fichier, changelog), mais **non normative**.
- **[N] Nomenclature introduite** — **appellation** apportée par *ce document* pour nommer un mécanisme **attesté** ; le mécanisme est un fait, seul le nom est introduit.
- **[H] Mise en récit** — reformulation **narrative** introduite par *ce document*, **sans référent dans le dépôt** ; éclairante mais non attestée.

> **Avertissement de lecture.**
> **[F]** Le runtime n'émet, par zone et par grandeur, qu'une **couleur** (clé textuelle) et un attribut de **validité** (`reason` ∈ `ok` / `unavailable` / `invalid_thresholds`).
> Il **ne publie aucune position nommée** (« sous », « dans », « au-dessus »).
> **[N]** Les termes « normale contextuelle » et « enveloppe de confort » employés ci-dessous **nomment des objets réels du runtime** ; ce sont des appellations introduites, pas des inventions de concept.
> **[H]** La filiation avec les **bulletins météo** et la lecture « positionnelle » (sous / dans / au-dessus des normales) sont une **mise en récit** : elles éclairent le *pourquoi*, mais ne décrivent aucun libellé produit par le système.

---

## 1. 🎯 Le concept

**[H]** Le domaine n'a pas été conçu comme un système de couleurs. La couleur est une **projection visuelle terminale**. Ce cadrage est cohérent avec le contrat `affichage.md`, qui qualifie la couleur de « descriptive, jamais prescriptive » et précise qu'elle « ne qualifie aucun confort souhaitable » — la couleur *décrit*, elle ne *prescrit* pas.

**[F]** Le cœur du mécanisme est l'**interprétation d'une grandeur mesurée par sa position relative à une référence contextuelle**, et non par sa valeur brute. C'est attesté à deux niveaux :
- dans le runtime, par la cascade conditionnelle des capteurs couleur, qui compare la valeur à un *centre* et à des *bornes* dérivés du contexte (cf. §2–§4) ;
- dans `architecture/capteurs_meteo.md`, qui pose que les seuils « définissent un **cadre d'interprétation**, jamais une décision ».

> **Encadré — contexte historique (hors dépôt).**
> **[H]** D'après le propriétaire du domaine, l'inspiration d'origine provient des **bulletins météo** : lire une grandeur « sous / dans / au-dessus des normales » plutôt que dans l'absolu. Cette filiation **n'est attestée par aucun document du dépôt** ; elle est fournie comme éclairage d'intention et **ne doit pas être lue comme un fait démontré**.

La suite descend du concept vers l'implémentation : **référence contextuelle → enveloppe de confort → qualification → projection visuelle**.

---

## 2. 📐 La référence contextuelle

**[F]** La référence n'est pas fixe : elle dépend du **moment de la journée**. Le runtime sélectionne une période via `sensor.periode_meteo`, dérivée de la position solaire (`sun.sun`), parmi : `aube`, `matin`, `jour`, `crepuscule`, `nuit`. Ceci est décrit dans `architecture/capteurs_meteo.md`.

**[F]** Pour chaque grandeur et chaque zone, la référence est la **moyenne filtrée de la période active** :
`sensor.<grandeur>_filtre_<periode>_moyenne_<zone>`. Le runtime construit les seuils à partir de cette moyenne (cf. §3), et `architecture/capteurs_meteo.md` documente explicitement que chaque seuil dépend « de la période météo active, de la **moyenne filtrée correspondante**, d'un offset saisonnier ».

**[I]** Le capteur filtre porte dans son en-tête l'intention de conserver des « **références thermiques comparables** sur une même journée » : l'objectif déclaré est de comparer une mesure à *sa propre référence du moment*, non à une valeur universelle.

**[N]** Nous désignons cette moyenne filtrée par période comme la **« normale contextuelle »** de la grandeur. Le mécanisme (moyenne filtrée ancrant les seuils) est un fait ; le terme « normale » est l'appellation fédératrice introduite ici pour le nommer — le dépôt ne l'emploie pas en ce sens.

**[F] — précision.** Deux objets à ne pas confondre :
- l'**ancre** de la référence = la moyenne filtrée par période ;
- le **centre de qualification** réellement utilisé pour la couleur = `(seuil_bas + seuil_haut) / 2`, qui n'est *pas* exactement la moyenne (cf. §3, asymétrie des offsets).

---

## 3. 🎚️ L'enveloppe de confort

**[F]** Autour de la référence, le runtime construit une enveloppe par un **offset saisonnier** :
```
seuil_bas  = moyenne_filtrée(période) − offset_bas(saison)
seuil_haut = moyenne_filtrée(période) + offset_haut(saison)
```
`architecture/capteurs_meteo.md` nomme cet ensemble un « **cadre de confort dynamique** », et le changelog `v04` documente le passage des capteurs couleur à un « **modèle recentré "zone de confort"** » avec « externalisation des seuils ».

**[F]** Les offsets sont **saisonniers et asymétriques** (valeurs observées sur l'axe température) :

| Côté | Hiver | Inter-saison | Été |
|------|-------|--------------|-----|
| bas (soustrait) | 1.3 °C | 1.0 °C | 3.0 °C |
| haut (ajouté)   | 0.9 °C | 1.1 °C | 1.4 °C |

**[F] — précision.** Le découpage mensuel des saisons **diffère légèrement** entre le calcul du bas et celui du haut (p. ex. mai et septembre ne tombent pas dans la même tranche des deux côtés). Fait du runtime, rapporté sans jugement.

**[F]** Conséquence de l'asymétrie : le **centre** de l'enveloppe se situe *légèrement sous la moyenne* —
`centre ≈ moyenne − 0.2 °C` en hiver, `≈ moyenne − 0.8 °C` au cœur de l'été. La tolérance est donc plus large du **côté froid**.

**[I]** L'en-tête du capteur de seuil bas justifie cette permissivité : l'offset d'été plus large vise à « **absorber les variations naturelles sans générer de fausse alerte** ». L'asymétrie n'est pas un artefact : c'est une **philosophie de confort** assumée dans le code.

**[N]** Nous appelons `[seuil_bas, seuil_haut]` l'**« enveloppe de confort »**. L'objet est attesté (« cadre de confort dynamique » dans `capteurs_meteo.md`) ; le mot « enveloppe » est l'appellation propre à ce document.

---

## 4. 🧭 La qualification

**[F]** Le capteur couleur de chaque zone compare la valeur courante à `{ centre, zone_verte, seuil_bas, seuil_haut }` et en déduit une **clé**. Deux variantes géométriques du même découpage coexistent :

- **Variante centrée** (température, humidité relative, humidité absolue) — qualification *autour du centre* :
  ```
  valeur < seuil_bas                          → blue
  seuil_bas ≤ valeur < centre − zone           → light_blue
  (humidités) centre − zone ≤ valeur < centre  → light_green
  centre − zone ≤ valeur ≤ centre + zone       → green
  centre + zone < valeur ≤ seuil_haut          → yellow
  valeur > seuil_haut                          → red
  ```
- **Variante par les bords** (humidex) — qualification *par rapport aux bornes de l'enveloppe*, avec une marge `= (seuil_haut − seuil_bas) / 5` ; le **vert** couvre l'intérieur de l'enveloppe, encadré de transitions.

**[F]** Dans tous les cas, une valeur absente, non numérique, ou des seuils incohérents (`bas ≥ haut`, `bas` ou `haut` à 0) produisent **`grey`**, et l'attribut `reason` distingue `unavailable` de `invalid_thresholds`. La validité **prime** sur toute couleur.

**[F]** La sortie est une **clé couleur**. Le système **ne nomme aucune position** ; il n'existe ni entité ni attribut « sous / dans / au-dessus ».

**[I]** Les en-têtes des capteurs couleur expriment néanmoins une intention positionnelle : « niveau » de la grandeur, « légèrement au-dessus du centre », et l'objectif explicite d'une « **lecture visuelle discriminante (fini le "tout vert")** ». L'ambition est de distinguer plusieurs degrés d'écart, pas seulement « conforme / non conforme ».

> **Encadré — lecture « bulletin » (mise en récit).**
> **[H]** On peut lire les clés comme une échelle de position : `green` = *dans la normale* ; `light_blue` / `light_green` / `yellow` = *en approche d'un bord* ; `blue` / `red` = *hors enveloppe* (sous / au-dessus). Cette correspondance est **fidèle au calcul** mais **n'est matérialisée nulle part dans le runtime** : elle reste une mise en récit.

---

## 5. 🎨 La projection visuelle

**[F]** La traduction de la clé en couleur réelle a lieu **dans la couche UI**, au sein du socle `socle_kpi` (button-card). Le socle :
- dérive l'entité couleur (`sensor.<x>` → `sensor.couleur_<x>`, ou `variables.couleur` explicite) ;
- mappe la clé vers un `rgba` via une palette de profil (`arsenal` / `ecs`) ;
- applique des fallbacks : entité absente ou `unknown` / `unavailable` → couleur d'indisponibilité ; clé inconnue → `grey`.

**[F]** La palette `arsenal` **replie** `light_blue` sur le `rgba` de `blue` et `light_green` sur celui de `green` (commentées « compat éventuelle »). Les degrés intermédiaires émis par le capteur sont donc **rendus identiques** à leur couleur de base : la granularité logique (clés) est plus fine que la granularité visuelle (couleurs) — fait à connaître pour comprendre le rendu.

**[F]** Le contrat `affichage.md` encadre cette couche : la couleur est « **descriptive, jamais prescriptive** », les états invalides restent visibles, et aucune logique de seuil n'est ré-introduite côté carte pour les grandeurs du mécanisme A.

**[H]** Conformément au cadrage du §1, la couleur est la **dernière étape** d'une chaîne d'interprétation, et non l'objet du domaine.

> **Renvoi.** Le détail du mapping clé → `rgba`, des profils et de la réconciliation des clés capteur avec la charte relève d'un document de référence UI dédié (« Doc β », à venir) et de `ui/couleurs/02_palette.md`. Le présent document s'arrête à la frontière de la projection.

---

## 6. 🚧 Frontières & hors-périmètre

**[F]** Ce document décrit le **mécanisme A** uniquement. Ne sont **pas** couverts ici, et relèvent d'autres décisions :

- **CO₂** — affiché par la même chaîne de rendu, mais qualifié par des **seuils codés en dur** (non dynamiques) et hors des grandeurs du contrat `affichage.md` ; son rattachement (météo vs qualité d'air) est un arbitrage ouvert.
- **Précipitations** — couleur calculée *dans la carte*, palette hydrique (charte, Exception 7).
- **Cohérence inter-capteurs (Δ)** — qualification *relative* entre capteurs redondants ; relève du concept de **consolidation** (cf. contrats `*/consolidation.md`), distinct de la présente interprétation.
- **Prévisions** — `weather.forecast_maison` (Met.no), carte native et icône dynamique : restitution, non interprétation au sens de ce document.

**[F]** Ce document **ne définit aucune règle normative**, **ne modifie aucun comportement runtime** et **ne réécrit pas** l'architecture des couches. Il *nomme et explique* un modèle déjà présent.

---

## 7. 🔁 Positionnement dans le corpus

**[F]** Ce document est **en aval** de `capteurs_meteo.md` (qui fournit période, moyenne filtrée et seuils dynamiques) et **en amont** de `affichage.md` (qui gouverne la restitution). Il documente la **couche d'interprétation** qui relie la mesure à l'affichage, jusqu'ici décrite seulement de façon dispersée (architecture des seuils, contrat de restitution, changelog `v04`, commentaires de capteurs).

**[N]** Sa contribution propre est de **nommer** cette couche (« normale contextuelle », « enveloppe de confort ») et de **consolider** une lecture éparse, **[H]** en explicitant le *pourquoi* (lecture relative à une référence contextuelle), tout en distinguant ce qui est démontré, documenté, nommé ou raconté.

---

## 8. 📜 Place dans l'histoire d'Arsenal *(contexte hors dépôt)*

> Cette section est **isolée du contenu technique** : elle ne porte aucune règle et n'engage pas la lecture des sections §1–§7.

**[F]** Indépendamment de toute histoire, ce domaine **illustre concrètement** plusieurs patterns aujourd'hui courants dans Arsenal : nommage industrialisé des entités (`couleur_<grandeur>_<zone>`, 24 zones dérivées d'une seule logique), **factorisation par ancres YAML** et par **`this.entity_id`**, et **séparation stricte donnée / interprétation / restitution**. Ces traits sont vérifiables dans les fichiers du mécanisme A.

**[H] — hors dépôt.** Selon le propriétaire du domaine, ce chantier a joué un rôle de **laboratoire** dans l'émergence ou la consolidation de ces principes avant qu'ils ne deviennent structurants ailleurs dans Arsenal. Cette filiation relève du **témoignage de conception** : elle **n'est pas attestée par le corpus** — les doctrines de nommage et d'étiquettes ne référencent pas ce domaine comme origine. Si une fresque historique devait être développée, elle aurait sa place dans le cluster méta / changelog, ce document n'en gardant qu'une note.

---

## 📎 Statut de preuve (synthèse)

| Élément | Registre | Source |
|---|---|---|
| Référence = moyenne filtrée par période | **[F]** | `capteurs_meteo.md` + runtime |
| Seuils = moyenne ± offset saisonnier | **[F]** | runtime + `capteurs_meteo.md` |
| « Cadre / zone de confort » dynamique | **[F]** | `capteurs_meteo.md` + changelog `v04` |
| Lecture descriptive, non décisionnelle | **[F]** | `affichage.md` |
| Sortie = clé couleur, sans position nommée | **[F]** | runtime (capteurs couleur, `reason`) |
| Asymétrie de l'enveloppe (motif) | **[I]** | en-tête seuil bas |
| « Références comparables », « fini le tout vert » | **[I]** | en-têtes de capteurs |
| Patterns (ancres, `this.entity_id`, séparation) présents | **[F]** | fichiers du mécanisme A |
| Termes « normale contextuelle », « enveloppe de confort » | **[N]** | introduits ici (mécanisme attesté) |
| Lecture « bulletin » (sous/dans/au-dessus) | **[H]** | intention propriétaire, hors dépôt |
| Rôle « laboratoire » dans l'histoire d'Arsenal | **[H]** | témoignage, hors dépôt |
