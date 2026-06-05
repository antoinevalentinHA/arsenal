# Audit — Affichage météo dans le runtime Arsenal

> **Type** : audit architectural en lecture seule
> **Sujet** : fonctionnement de l'affichage météo, attention particulière aux mécanismes visuels (couleurs)
> **Mode** : lecture seule stricte — aucun patch, aucun commit, aucune modification de fichier
> **Principe directeur** : le runtime est la référence ; on distingue systématiquement *faits observés* et *interprétations*.

---

## 1. HEAD audité

- Dépôt : `antoinevalentinHA/arsenal`
- Branche : `main`
- HEAD : `6e24ed2117eee65ea19810a699e69b64b74247eb`
- Dernier commit : `Antoine — Fri Jun 5 12:59:47 2026 +0200 — docs(audits): close garage consolidation arbitration`
- Volume : 4 668 fichiers (hors `.git`)

L'audit porte sur l'état exact de ce HEAD, cloné localement et inspecté sans écriture.

---

## 2. Méthode d'investigation

Démarche descendante, sans hypothèse initiale sur l'implémentation :

1. **Cartographie lexicale** — recherche transverse des fichiers contenant `meteo`/`météo`/`weather` dans leur chemin, puis du terme `couleur` pour localiser le mécanisme visuel.
2. **Lecture documentaire d'abord** — architecture (`architecture/meteo_affichage.md`, `architecture/capteurs_meteo.md`), contrats (`contrats/meteo/…`), charte couleurs (`ui/couleurs/…`), hub de navigation, rapport et plan d'action d'audit existants.
3. **Confrontation au runtime** — capteurs couleur (`12_template_sensors/couleurs/meteo/`), seuils dynamiques (`12_template_sensors/statistiques/seuils_dynamiques/`), templates `button-card` (`19_button_card_templates/`), dashboards Lovelace (`18_lovelace/dashboards/meteo/`) et leur enregistrement (`18_lovelace/dashboards.yaml`).
4. **Suivi des dépendances** — du dashboard vers le socle UI, du socle vers le capteur couleur, du capteur couleur vers les seuils et le helper de zone verte, puis des seuils vers la période solaire et l'offset saisonnier.
5. **Vérification d'usage réel** — recensement des `template:` consommés par dashboard, contrôle de l'enregistrement des vues, repérage des templates définis mais non consommés.

Limite assumée : l'audit lit des fichiers statiques. Il **ne peut pas observer d'états runtime** (valeurs de capteurs, rendu effectif). Les conclusions sur le comportement reposent sur la lecture du code, pas sur une exécution.

---

## 3. Fichiers étudiés (principaux)

**Documentation**
- `00_documentation_arsenal/architecture/meteo_affichage.md`
- `00_documentation_arsenal/architecture/capteurs_meteo.md`
- `00_documentation_arsenal/contrats/meteo/meteo.md`, `…/affichage.md`, `…/gouvernance.md`, `…/validation.md`
- `00_documentation_arsenal/ui/couleurs/02_palette.md`, `…/02_1_palette_etiquettes.md`, `…/03_exceptions.md`
- `00_documentation_arsenal/navigation/domaines/meteo.md`
- `00_documentation_arsenal/audits/01_rapports/meteo/audit_meteo_axe_temperature_rapport_final.md`

**Runtime — capteurs**
- `12_template_sensors/couleurs/meteo/{temperature,humidite_relative,humidite_absolue,humidex,co2,temperature_moyenne_maison}.yaml`
- `12_template_sensors/couleurs/meteo/temperature_min_max/{min_jour,max_jour,minmax_jour}.yaml`
- `12_template_sensors/statistiques/seuils_dynamiques/bas/temperature.yaml`
- `12_template_sensors/meteo/temperature_prevue.yaml`
- `03_input_numbers/meteo/zones_vertes_dashboard/temperature.yaml`

**Runtime — UI**
- `19_button_card_templates/00_socles/kpi/socle_kpi.yaml`
- `19_button_card_templates/40_dashboards/meteo/README.md`
- `19_button_card_templates/40_dashboards/meteo/10_diagnostic_seuils/carte_precipitations_seuils_variables.yaml`
- `19_button_card_templates/40_dashboards/meteo/20_diagnostic_coherence/temperature.yaml`
- `19_button_card_templates/40_dashboards/arsenal/40_kpi_contexte/kpi_icone_meteo.yaml`
- `18_lovelace/dashboards/meteo/{meteo_temperature,meteo_co2,meteo_humidex,meteo_publique,meteo_backups,meteo_precipitations}.yaml`
- `18_lovelace/dashboards.yaml`

---

## 4. Architecture observée

### 4.1 Surface UI météo (faits)

`18_lovelace/dashboards.yaml` enregistre les vues météo suivantes, chacune adossée à un fichier de `18_lovelace/dashboards/meteo/` :
température, humidité relative, humidité absolue, humidex, bruit, CO₂, précipitations, pression, météo publique, min/max température, backups (redondance). Une seconde série d'écrans `imprimerie/meteo/` (température, humidité relative, humidité absolue, humidex) couvre les zones professionnelles de l'imprimerie. Un écran de réglages `reglages/meteo.yaml` complète l'ensemble.

### 4.2 Chaîne canonique de restitution (fait)

Le pattern dominant (≈ 61 cartes recensées via `template: socle_kpi` dans les dashboards météo) est une chaîne en trois temps :

```
sensor.<grandeur>_<zone>            (valeur physique, affichée comme texte)
        +
sensor.<grandeur>_seuil_bas/haut_<zone>   (seuils dynamiques)
input_number.<grandeur>_couleur_zone_verte (demi-largeur de zone verte)
        ↓
sensor.couleur_<grandeur>_<zone>    (capteur couleur → CLÉ textuelle : green/blue/…)
        ↓
template button-card "socle_kpi"    (mapping CLÉ → rgba via palette JS)
```

Concrètement, dans `meteo_temperature.yaml`, chaque tuile est :

```yaml
type: custom:button-card
template: socle_kpi
entity: sensor.temperature_<zone>
triggers_update:
  - sensor.couleur_temperature_<zone>
```

La carte affiche la **valeur** (`entity.state`) comme contenu dominant et porte la **qualification** dans la **couleur de fond**. Le `triggers_update` force le re-rendu quand le capteur couleur change (la carte ne référence pas ce capteur comme entité principale : elle le *dérive*).

Cette chaîne est **conforme** à ce que décrivent `architecture/meteo_affichage.md` (séparation capteur → capteur couleur → UI) et le contrat `contrats/meteo/affichage.md` (valeur et couleur portées par des capteurs distincts ; la carte consomme une clé, ne la calcule pas).

### 4.3 Où la couleur réelle est produite (fait)

Le mapping clé → couleur n'est **pas** dans le capteur couleur ; il est dans le socle `socle_kpi` (`styles.card.background-color`, JS `button-card`). Deux palettes (`arsenal`, `ecs`) y sont codées. Extrait de la palette `arsenal` :

```
green       rgba(76, 175, 80, 0.2)
red         rgba(244, 67, 54, 0.2)
orange      rgba(255, 152, 0, 0.2)
blue        rgba(33, 150, 243, 0.2)
yellow      rgba(255, 235, 59, 0.2)
grey        rgba(158, 158, 158, 0.2)
light_green rgba(76, 175, 80, 0.2)   ← identique à green
light_blue  rgba(33, 150, 243, 0.2)  ← identique à blue
unavailable rgba(158, 158, 158, 0.1)
```

L'entité couleur est résolue ainsi : priorité à `variables.couleur` si fournie, sinon dérivation `sensor.<x>` → `sensor.couleur_<x>` par regex. Robustesse : entité absente ou `unknown`/`unavailable` → `unavailable` ; clé inconnue → `grey`.

---

## 5. Mécanismes identifiés

L'affichage météo n'est pas mono-mécanisme. Cinq mécanismes coexistent.

### Mécanisme A — KPI à capteur couleur (qualification absolue, couleur en backend)

**Axes** : température, humidité relative, humidité absolue, humidex, CO₂.
**Fait** : la couleur est calculée dans un *capteur déclenché* (`couleur_*`), pas dans la carte. La carte (`socle_kpi`) ne fait que mapper la clé en rgba.

Point central pour l'objectif de l'audit — **les couleurs ne sont ni statiques, ni un simple escalier de seuils** :

- **Température** (`couleurs/meteo/temperature.yaml`) — modèle **centré sur le confort**, et non bas → haut. `centre = (seuil_bas + seuil_haut)/2`, `zone = input_number.temperature_couleur_zone_verte`. Bandes :
  `t < bas → blue` · `bas ≤ t < centre−zone → light_blue` · `centre−zone ≤ t ≤ centre+zone → green` · `centre+zone < t ≤ haut → yellow` · `t > haut → red` · invalide/incohérent → `grey`.
  Les 24 zones partagent la même logique via une ancre YAML (`&couleur_temperature_logic`) et la dérivation du suffixe depuis `this.entity_id`.
- **Humidité relative / absolue** — même logique centrée, avec une bande supplémentaire `light_green` (légèrement sous le centre) ; helpers propres (`humidite_relative_couleur_zone_verte`, `humidite_absolue_couleur_zone_verte`).
- **Humidex** — modèle **différent**, par marges autour des seuils : `marge = (haut − bas)/5` ; `blue/light_blue/light_green` en approche basse, `green` sur `[bas+marge ; haut[`, `yellow/red` au-dessus. Le vert couvre ici toute la bande de confort, encadré par des transitions.
- **CO₂** (`couleurs/meteo/co2.yaml`) — modèle **à seuils fixes codés en dur** (`warn = 500`, `crit = 800`) : `green/orange/red`, `grey` si invalide. Pas de seuils dynamiques, pas de helper de zone verte, et usage de `orange` (absent du modèle température).

**Fait complémentaire** : les seuils consommés (`sensor.<grandeur>_seuil_bas/haut_<zone>`) sont eux-mêmes **dynamiques**. `seuils_dynamiques/bas/temperature.yaml` calcule `seuil_bas = moyenne_filtrée_par_période − offset_saisonnier`, où la période vient de `sensor.periode_meteo` (position solaire) et l'offset varie par saison (hiver −1.3 °C, inter-saison −1.0 °C, été −3.0 °C). La bande verte se **déplace** donc avec les seuils et **s'élargit/se rétrécit** avec le helper.

**Interprétation** : pour les axes A hors CO₂, la couleur est une fonction de (valeur, seuils dynamiques, demi-largeur de zone verte) ; parler de « couleur pilotée par seuils » serait une simplification fausse — la couleur encode une *position relative à un centre de confort mobile*. Le CO₂ est l'exception : seuils statiques, modèle escalier.

**Fait sur le helper de zone verte** : `input_number.temperature_couleur_zone_verte` est un paramètre **UI persistant** ajustable par curseur (`min 0.2`, `max 1.5`, `step 0.1`, °C). Son en-tête interdit explicitement de le piloter dynamiquement selon la météo. La largeur du vert est donc un réglage manuel global, ni codé en dur ni dynamique.

### Mécanisme B — Carte à seuils, couleur calculée en carte (précipitations)

**Fait** : `carte_precipitations_seuils_variables.yaml` calcule la couleur **dans la carte** (JS), directement à partir de seuils passés en `variables` (`seuil_faible/modere/forte`), avec la **palette hydrique** bleue (`rgba(187,222,251,.3)` → `rgba(100,181,246,.3)` → `rgba(30,136,229,.35)`), `grey` sinon. Utilisée dans `meteo_precipitations.yaml`. Une variante `…_tap` duplique la carte pour l'action.
**Interprétation** : ici la couleur *est* pilotée directement par seuils, et *dans l'UI*. C'est cohérent avec l'« Exception 7 — palette hydrique » de la charte couleurs, mais en tension avec les principes généraux d'architecture (cf. §7).

### Mécanisme C — Diagnostic de cohérence, couleur par écart (Δ inter-capteurs)

**Fait** : `20_diagnostic_coherence/temperature.yaml` (et son symétrique `humidite.yaml`) calcule la couleur **dans la carte** par **comparaison de deux capteurs** : un maître de zone (suffixe `_1`, dérivé par regex `/_\d$/ → _1`) et un capteur secondaire. `|Δ| < 0.3 → green` · `< 0.8 → yellow` · `≥ 0.8 → red` · données manquantes → `grey`. Cas spéciaux Netatmo jardin (`_jardin_1/_2`) **codés en dur → toujours green**. Un label affiche `Δ ±x.x°C`.
**Faits associés** : ces cartes ne vivent que dans `meteo_backups.yaml` (≈ 15 cartes température + 15 humidité), dashboard **enregistré et actif** (`meteo-backups-dashboard`). Le « backups » désigne ici la **redondance de capteurs** par zone (Netatmo 1/2/3), pas des sauvegardes. La carte utilise un jaune renforcé `rgba(255,193,7,.25)` (variante « Exception 6 »), distinct du jaune sémantique officiel `rgba(255,235,59,.2)`.

### Mécanisme D — Carte météo native (prévisions publiques)

**Fait** : `meteo_publique.yaml` n'utilise **aucune** logique de couleur Arsenal : cartes natives Home Assistant `type: weather-forecast` (horaire 8 créneaux, journalier), entité `weather.forecast_maison`.

### Mécanisme E — Icône météo dynamique (contexte)

**Fait** : `kpi_icone_meteo.yaml` spécialise `socle_kpi` en remplaçant l'icône statique par une icône `mdi:weather-*` dérivée de l'état d'une entité `weather.*` (`weather.forecast_maison` par défaut), avec fallback `mdi:weather-cloudy`. Le **fond** reste géré par `socle_kpi` (donc par un capteur couleur). Ce template est utilisé sur le dashboard d'accueil (`18_lovelace/dashboards/arsenal.yaml`), pas dans les écrans météo.

### Source météo externe (fait)

`weather.forecast_maison` est l'**intégration Met.no** (commentaire explicite de `temperature_prevue.yaml`, qui appelle `weather.get_forecasts`). Cette entité n'est **pas définie en YAML** dans le dépôt : c'est une *config entry* configurée hors dépôt. Le sensor `temperature_prevue` en extrait la température prévue à un horizon paramétrable (`input_number.meteo_horizon_prevision_heures`).

---

## 6. Synthèse des dépendances

```
sun.sun ─► sensor.periode_meteo ─┐
                                 ├─► seuils dynamiques (bas/haut) ─┐
moyennes filtrées par période ───┘                                │
offset saisonnier (mois) ────────────────────────────────────────┤
input_number.<grandeur>_couleur_zone_verte ──────────────────────┤
sensor.<grandeur>_<zone> (valeur) ───────────────────────────────┤
                                                                  ▼
                                            sensor.couleur_<grandeur>_<zone>  (clé)
                                                                  ▼
                                            socle_kpi (palette JS) ─► rgba de fond
                                                                  ▲
                                            triggers_update (re-rendu)

Met.no (weather.forecast_maison) ─► weather-forecast natif (méca. D)
                                  └─► kpi_icone_meteo : icône (méca. E)
                                  └─► temperature_prevue (sensor dérivé)

précipitations : entity + variables.seuil_* ─► couleur calculée EN CARTE (méca. B)
cohérence      : maître _1 vs secondaire     ─► couleur par Δ EN CARTE (méca. C)
```

---

## 7. Incohérences et absences documentaires

> Présentées comme *faits* (texte vs texte, ou texte vs code) ; le caractère « problématique » relève de l'*interprétation* et est signalé comme tel.

1. **Granularité capteur > granularité visuelle (fait).** Les capteurs couleur émettent jusqu'à 7 clés (`blue, light_blue, light_green, green, yellow, red, grey`). La palette `socle_kpi` **replie** `light_blue` sur le rgba de `blue` et `light_green` sur celui de `green` (commentés « Compat éventuelle avec des clés météo existantes »). *Interprétation* : une distinction calculée par le capteur (p. ex. « sous le confort mais au-dessus du seuil bas ») devient **invisible** à l'écran, rendue identique à l'état adjacent. La charte sémantique (`02_palette.md`) ne déclare d'ailleurs ni `light_blue` ni `light_green` et interdit la « multiplication de nuances intermédiaires ».

2. **Contrat d'affichage vs cartes qui calculent la couleur (fait).** `contrats/meteo/affichage.md` est **normatif et opposable** et pose, entre autres : Invariant 2 « Aucune carte UI ne calcule une couleur à partir d'une valeur » ; Invariant 3 « aucune logique conditionnelle locale » ; interdictions absolues « introduire une logique de seuil dans l'UI », « recalculer une couleur côté carte », « comparer plusieurs capteurs dans l'UI ». Or :
   - le mécanisme **B (précipitations)** calcule la couleur en carte à partir de seuils ;
   - le mécanisme **C (cohérence)** calcule la couleur en carte en comparant deux capteurs.
   *Interprétation / nuance* : le périmètre déclaré du contrat se limite à *température, humidité relative, humidité absolue, humidex*. Les précipitations sont hors périmètre et explicitement couvertes par l'« Exception 7 » de la charte. Le cas C est plus délicat : il porte sur la température/humidité (dans le périmètre nominal), mais le hub de navigation rattache ces capteurs au domaine `temperature_interieure`/redondance, et le `README` des templates météo revendique « diagnostic de cohérence » comme *pattern Arsenal à part entière*. Il y a donc, au minimum, une **tension non tranchée** entre un contrat d'affichage strict et des patterns diagnostiques autorisés ailleurs.

3. **Architecture vs runtime — templates `carte_*` fantômes (fait).** `architecture/meteo_affichage.md` désigne comme canoniques des templates `carte_temperature`, `carte_humidite`, `carte_humidite_absolue`, `carte_humidex`. Ces noms **n'existent pas** dans `19_button_card_templates/`. Le runtime utilise un socle générique `socle_kpi` (+ dérivation du capteur couleur). *Interprétation* : la doc d'architecture décrit une cible (cartes spécialisées par grandeur) que l'implémentation a remplacée par un socle unique paramétré.

4. **Référence de chemin erronée (fait).** La même doc d'architecture cite en dépendance `/contrats/meteo_affichage.md`. Le contrat réel est `contrats/meteo/affichage.md` (chemin imbriqué). Le fichier existe, mais la référence pointe une cible inexistante.

5. **Template défini mais non consommé (fait).** `carte_co2_seuils_variables.yaml` n'est référencé dans aucun dashboard (uniquement son propre fichier et le `README`). Le CO₂ est affiché via le mécanisme A (`socle_kpi` + `couleur_co2`). *Interprétation* : template dormant / candidat à un nettoyage ou à un usage prévu mais non branché.

6. **Hétérogénéité des modèles de couleur (fait).** Trois modèles coexistent rien que pour les capteurs couleur backend : confort centré (température), confort centré + `light_green` (humidités), marges autour des seuils (humidex), escalier à seuils fixes (CO₂). Le `temperature_moyenne_maison` introduit encore un autre référentiel (consignes chauffage/clim, donc dépendance vers un autre domaine). *Interprétation* : cohérent fonctionnellement mais non unifié ; aucune doc ne récapitule ces variantes côté affichage.

7. **Absence d'audit du domaine affichage (fait).** Le seul audit météo existant (`audit_meteo_axe_temperature_rapport_final.md`) porte sur l'**axe température extérieure** (façade, fallback, consommateurs) et déclare le domaine **non clôturé**. Le hub de navigation confirme un « audit partiel ». **Aucun document d'audit ne couvre l'affichage / les couleurs.** Le présent rapport comble ce vide. (À noter, dette signalée par l'audit existant : `contrat_fallback.md`, référencé par cinq contrats, n'existe pas comme fichier.)

---

## 8. Éléments encore incertains

- **Rendu effectif non observé.** Tout repose sur la lecture statique : impossible de confirmer les valeurs réelles, les états `unknown`, ou le rendu visuel exact sans runtime.
- **Définition de `weather.forecast_maison`.** Entité Met.no configurée hors dépôt — non vérifiable ici (config entry).
- **Existence réelle de tous les capteurs `seuil_bas/haut` et `couleur_*` par zone.** Les capteurs couleur sont définis pour 24 zones ; la présence et la fraîcheur des seuils correspondants par zone n'ont pas été exhaustivement croisées.
- **Axes survolés.** `meteo_bruit` (capteur couleur `bruit_chambres` dédié) et `meteo_pression` (fichier très court) n'ont pas été disséqués au même niveau que température/humidité/humidex/CO₂/précipitations.
- **Dashboards `imprimerie/meteo/`.** Recensés et enregistrés ; supposés réutiliser le mécanisme A pour les zones pro (capteurs couleur de ces zones existent), mais leur contenu n'a pas été lu ligne à ligne.
- **Portée exacte du contrat d'affichage.** Le rattachement du diagnostic de cohérence au périmètre du contrat (point 7.2) est une question d'arbitrage documentaire, non tranchée dans les fichiers lus.

---

## 9. Pistes de travail futures (sans prescription)

Ces pistes décrivent des questions ouvertes, pas des corrections à appliquer.

1. **Clarifier le statut des mécanismes B et C** au regard de `contrats/meteo/affichage.md` : soit acter explicitement qu'ils sont hors périmètre (et le documenter dans le contrat), soit reconnaître la divergence.
2. **Documenter la perte de granularité** `light_blue`/`light_green` → `blue`/`green` : choix assumé d'unification visuelle, ou bandes à rendre distinctes.
3. **Réconcilier `architecture/meteo_affichage.md` avec le runtime** : noms de templates (`carte_*` vs `socle_kpi`) et chemin de dépendance du contrat.
4. **Recenser les modèles de couleur** dans un document unique côté affichage (confort centré / marges / escalier fixe / référentiel consignes).
5. **Statuer sur `carte_co2_seuils_variables`** (dormant) : à brancher, à supprimer, ou à conserver explicitement comme réserve.
6. **Étendre l'audit** aux axes bruit, pression, précipitations et aux écrans `imprimerie/meteo/`, puis clôturer le domaine côté navigation.
7. **Tracer la dépendance externe Met.no** dans la documentation du domaine (entité non versionnée mais structurante pour D et E).

---

## 10. Conclusion (faits dominants)

L'affichage météo Arsenal n'est ni statique ni piloté par un simple escalier de seuils. Le cœur du domaine (température, humidités, humidex) repose sur une **chaîne capteur → capteur couleur → socle UI** où la couleur encode une **position relative à une bande de confort mobile**, calculée en backend à partir de **seuils eux-mêmes dynamiques** (période solaire + saison) et d'une **demi-largeur de zone verte réglable**. La carte ne fait que traduire une clé textuelle en rgba via une palette. À côté de ce cœur conforme aux contrats, coexistent des mécanismes qui s'en écartent ou en débordent — précipitations (couleur calculée en carte, palette hydrique), diagnostic de cohérence (couleur par écart inter-capteurs), prévisions natives Met.no, icône météo dynamique. Les principaux écarts relevés sont documentaires (architecture vs runtime, granularité capteur vs palette, contrat d'affichage vs cartes diagnostiques) et l'affichage n'avait jusqu'ici fait l'objet d'aucun audit dédié.
