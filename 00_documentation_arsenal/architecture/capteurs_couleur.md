# 🎨 ARSENAL — Architecture · Capteurs de couleur

> **Carte de l'existant.** Ce document *recense* et *décrit* les capteurs de couleur d'Arsenal et leurs mécanismes. Il ne propose ni contrat, ni architecture transverse, ni évolution. Il sert de point d'entrée pour comprendre « qui produit une couleur, comment, et pour qui ».

## 📌 Statut du document

- **Type** : Cartographie / README de référence.
- **Caractère** : **Descriptif** — décrit le mécanisme observé ; n'impose rien.
- **Autorité** : **aucune**. En cas de divergence, le runtime fait foi ; la charte `ui/couleurs/` prime pour la restitution rgba.
- **Périmètre** : entités `sensor.couleur_*` (couche *amont*, production de la clé sémantique). La charte des couleurs rgba (couche *aval*) est référencée mais hors périmètre de description.

**Convention épistémique** (alignée sur `architecture/meteo_interpretation_contextuelle.md`) :
- **[F] Fait observé** — vérifiable dans le dépôt.
- **[I] Interprétation** — lecture de sens proposée, non imposée.
- **[H] Hypothèse** — inférence non entièrement vérifiable en lecture seule.

---

## 🔗 Dépendances (lecture)

- [`meteo_interpretation_contextuelle.md`](meteo_interpretation_contextuelle.md) — **référence du mécanisme A** (météo). Ce document ne re-décrit pas A : il y délègue.
- [`capteurs_meteo.md`](capteurs_meteo.md) — mesures, périodes et seuils source de la famille A.
- [`../ui/couleurs/00_index.md`](../ui/couleurs/00_index.md) — charte *aval* : palette rgba et sémantique des clés.
- [`../ui/socle_ui/06_kpi.md`](../ui/socle_ui/06_kpi.md) — `socle_kpi`, consommateur canonique (mapping clé → rgba).

---

## 1. Vue d'ensemble

**[F]** Le dépôt définit **158 entités** `sensor.couleur_*` (`unique_id: couleur_*`), majoritairement sous `12_template_sensors/couleurs/` et ses sous-dossiers `meteo/` et `sante/`.

**[F]** Chaque capteur émet une **clé textuelle** (`green`, `red`, `orange`, `yellow`, `blue`, `light_blue`, `grey`, `unavailable`) — jamais une valeur rgba. La conversion clé → couleur rgba a lieu **en aval**, dans le socle UI `socle_kpi`.

**[I]** Les capteurs partagent trois choses : un **préfixe de nommage** (`couleur_`), un **point de consommation** unique (`socle_kpi`), et — partiellement — une **palette de clés**. Ils ne partagent **pas** un mécanisme de qualification commun (cf. §2).

---

## 2. Les familles de mécanismes (A → G)

**[F]** Il n'existe pas un modèle unique. On observe **sept familles structurellement distinctes**, qui diffèrent par leur *entrée*, leur *référence* et leur *palette de sortie*.

### A · Interprétation contextuelle (enveloppe de confort)
- **Principe** : la valeur est lue par rapport à un *centre* `(seuil_bas + seuil_haut) / 2` et une demi-largeur de zone verte globale (`input_number.temperature_couleur_zone_verte`).
- **Sortie** : `blue / light_blue / green / yellow / red / grey`, symétrique autour du centre.
- **Entités** : `couleur_temperature_<zone>`, `couleur_humidite_relative_*`, `couleur_humidite_absolue_*`, `couleur_humidex_*`, `couleur_temperature_{min,max,minmax}_jour_*`.

### B · Seuils fixes absolus (progression monotone)
- **Principe** : cascade de bornes fixes en dur, sans centre ni référence dynamique.
- **Sens** : « plus = mieux » (santé) ou « plus = pire » (CO₂).
- **Entités** : `couleur_co2_*` (warn 500 / crit 800), `couleur_sante_pas_*`, `couleur_sante_distance_*`, `couleur_sante_calories_*`, `couleur_sante_duree_sommeil`, `couleur_sante_score_sommeil`, `couleur_bruit_*`.

### C · Remapping d'états métier qualitatifs
- **Principe** : une couleur est associée à un *état nommé* (pas à un seuil numérique).
- **Entités** : `couleur_cardio_nuit_etat` (`optimal / normal / eleve / anormal` + confirmation), `couleur_diagnostic_redondance_<contact>` (`nominal / divergent / degrade / critique / quarantine / inhibited`).

### D · Écart à une référence historique (baseline)
- **Principe** : `delta = valeur_courante − référence`, seuils appliqués sur le delta.
- **Entités** : `couleur_cpu_moyenne_10_min_*` et `couleur_memoire_moyenne_10_min_*` (vs médiane 7 j), `couleur_sante_frequence_respiratoire` (vs moyenne 14 j), `couleur_cardio_nuit_delta_baseline`.

### E · État binaire / on-off
- **Principe** : seuil unique on/off, pas de gradation.
- **Entités** : `couleur_boiler_burner_modulation` (`0 → grey`, `>0 → blue`).

### F · Fraîcheur de donnée
- **Principe** : âge de la donnée comparé à un *centre* et un *seuil* propres à chaque intégration (`centre_map`, `seuil_map`).
- **Entités** : `couleur_age_<integration>` (homekit, netatmo, switchbot, fujitsu, cumulus, synology, audi).

### G · Bornes de service (hybride)
- **Principe** : bornes issues de consignes de service plutôt que de seuils de confort.
- **Entités** : `couleur_temperature_ecs*` (`seuil_on` / `seuil_off` du bouclage ECS, **sans vert**), `couleur_temperature_moyenne_maison` (bornes dérivées des consignes chauffage/clim).

**[F]** Remarque transversale : **un même domaine peut relever de plusieurs familles**. La Santé combine B (pas, distance, calories, sommeil), C (cardio état) et D (fréquence respiratoire, cardio delta).

---

## 3. Domaines propriétaires

| Domaine | Familles | Référence des couleurs | Emplacement |
|---|---|---|---|
| Météo | A, B (CO₂, bruit), G (moyenne maison) | Confort contextuel / seuils air / consignes | `couleurs/meteo/` |
| Imprimerie | A (réutilise le mécanisme météo) | Confort thermique des zones pro | `couleurs/meteo/temperature.yaml` |
| Santé | B, C, D | Seuils fixes + états + baseline | `couleurs/sante/` |
| Système | D | Écart à la médiane 7 j | `couleurs/systeme.yaml`, `uptime.yaml` |
| Intégrations / Diagnostic | F | Fraîcheur par intégration | `couleurs/integrations.yaml` |
| Diagnostic / Redondance | C | États de cohérence | `couleurs/diagnostic_redondance_contacts.yaml` |
| Boiler | E | État de fonctionnement | `couleurs/boiler_modulation.yaml` |
| ECS | G | Bornes `seuil_on` / `seuil_off` | `couleurs/temperature_ecs*.yaml` |

---

## 4. Consommateurs

**[F]** Les capteurs de couleur sont consommés **exclusivement par la couche UI** ; aucune automatisation ni logique de décision ne les lit.

| Couche | Nombre de fichiers référençant une couleur | Rôle |
|---|---|---|
| `19_button_card_templates/` | 66 | Affichage des cartes |
| `18_lovelace/` | 12 | Tableaux de bord |
| `11_automations/` | 0 | — (aucun usage runtime) |

**[F]** Point de consommation canonique : le socle **`socle_kpi`** (`ui/socle_ui/06_kpi.md`).
- Résout l'entité couleur par convention `sensor.couleur_<suffixe_entité>`, ou via `variables.couleur` explicite.
- Mappe la clé sémantique → rgba.
- Déclare **deux profils de palette** : `arsenal` (green / red / orange / blue / grey / yellow) et `ecs` (blue / orange / red).
- Clé inconnue → repli `grey` ; indisponibilité → `rgba(158, 158, 158, 0.1)`.

**[I]** La couleur est une **projection terminale d'affichage** : aucun comportement du système n'en dépend.

---

## 5. Documentation existante

| Famille / domaine | Documentation présente | Niveau |
|---|---|---|
| A (Météo) | `architecture/meteo_interpretation_contextuelle.md` + `contrats/meteo/affichage.md` + `audits/01_rapports/meteo/audit_affichage_meteo.md` | **Élevé** (descriptif + contrat d'affichage) |
| Charte aval (rgba) | `ui/couleurs/` (7 fichiers : index, principes, palette, palette étiquettes, exceptions, typographie, règles) | **Élevé** (charte normative) |
| Socle consommateur | `ui/socle_ui/06_kpi.md` | Moyen (décrit la résolution et le mapping) |
| B, C, D, E, F, G (hors météo) | En-tête de fichier YAML uniquement | **Faible** |

**[F]** Le document météo précise lui-même « Autorité : aucune », se limite à la météo, et **liste explicitement les autres mécanismes (CO₂ à seuils fixes, cohérence…) comme hors périmètre**.

---

## 6. Gouvernance existante

**[F]** La gouvernance est **asymétrique** : elle couvre l'aval (couleurs rgba), pas l'amont (capteurs producteurs).

**Aval — gouverné :**
- 2 scripts de contrat : `check_ui_couleurs_contracts.py` (présence/cohérence de la charte), `check_ui_runtime_colors_contracts.py` (les rgba employés dans `18_lovelace`/`19_button_card_templates` appartiennent à la palette canonique + exceptions documentées).
- 2 workflows CI : `contracts_ui_couleurs.yml`, `contracts_ui_runtime_colors.yml`.

**Amont — non gouverné :**
- **Aucun** dossier `contrats/couleurs/` ni `contrats/ui/`.
- **Aucun** contrat normatif des capteurs `sensor.couleur_*`.
- **Aucun** audit transverse des capteurs de couleur.
- Seule exception : la famille A (météo) dispose d'une documentation d'architecture **descriptive et sans autorité**.

---

## 7. Constat de divergence sémantique

**[F]** La charte (`ui/couleurs/02_palette.md`) affirme que chaque couleur porte une « sémantique **unique, stable et opposable** ». En amont, cette unicité n'est **pas** respectée : la même clé reçoit des sens différents selon le domaine.

| Clé | Sémantique de charte (aval) | Sens réels observés en amont |
|---|---|---|
| `blue` | Information / technique / confort informatif | Trop froid (météo, ECS) · Excellent (pas, distance, calories, sommeil) · Optimal (cardio) · En marche (boiler) · Quarantaine (redondance) |
| `green` | OK / favorable / nominal | Présent partout **sauf** ECS et boiler |
| `light_blue` | *(absent de la charte)* | Émis par la famille A ; n'existe que comme « Exception 2 — palette thermique » du contrat runtime |
| `grey` vs `unavailable` | Deux gris distincts (neutre / indisponibilité) | Choix de clé non uniforme : `grey` pour seuils invalides (météo), `unavailable` pour donnée absente (santé) — selon les fichiers |

**[I]** Il existe un **ancrage sémantique central**, mais il vit **en aval** (charte + socle). En amont, chaque domaine a choisi son association couleur → sens, sans lien contractuel à la charte. La convention `sensor.couleur_*` garantit un *nommage* et un *point de branchement* communs, **pas une sémantique commune**.

**[H]** Le cas le plus saillant est le `blue` : au moins cinq significations incompatibles, dont l'usage « meilleur état » (santé, cardio) entre en concurrence avec le `green` « favorable » de la charte. Ce constat est posé ici **comme observation** ; sa résolution éventuelle relèverait d'une décision, non de cette cartographie.

---

## 8. Index rapide des fichiers

| Fichier | Famille(s) |
|---|---|
| `couleurs/meteo/temperature.yaml` (maison + imprimerie) | A |
| `couleurs/meteo/humidite_relative.yaml`, `humidite_absolue.yaml`, `humidex.yaml` | A |
| `couleurs/meteo/temperature_min_max/{min,max,minmax}_jour.yaml` | A |
| `couleurs/meteo/co2.yaml`, `bruit_chambres.yaml` | B |
| `couleurs/meteo/temperature_moyenne_maison.yaml` | G |
| `couleurs/sante/{pas,distance,calories,duree_sommeil,score_sommeil}.yaml` | B |
| `couleurs/sante/frequence_cardiaque.yaml` (cardio état / delta / anomalie) | C, D |
| `couleurs/sante/frequence_respiratoire.yaml` | D |
| `couleurs/systeme.yaml`, `uptime.yaml` | D |
| `couleurs/integrations.yaml` | F |
| `couleurs/diagnostic_redondance_contacts.yaml` | C |
| `couleurs/boiler_modulation.yaml` | E |
| `couleurs/temperature_ecs.yaml`, `temperature_ecs_petite_maison.yaml` | G |
