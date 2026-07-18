# Audit — Cartes « Température minimale / maximale des chambres » du dashboard Arsenal

## 1. Statut documentaire et non normatif

- **Type** : rapport d'audit transversal — **descriptif, lecture seule, non normatif**.
- Ce rapport **ne crée aucun contrat**, **ne modifie aucun runtime, agrégat, dashboard, template ou contrat**, **ne propose aucune correction, aucun capteur cible, aucune architecture, aucune mutualisation, aucun patch**.
- Les identifiants `OBJ-1…OBJ-8` (règles UI opposables) et `INT-1…INT-4` (contraintes d'interprétation) **structurent l'audit uniquement**. Ils **ne constituent pas de nouveaux contrats** et ne sont pas rendus opposables par le présent document ; ils renvoient à la doctrine existante (charte couleurs, architecture UI transverse).
- Ce rapport **n'importe pas** et **ne réutilise pas** les verdicts des audits d'exposition diagnostique Chauffage (`CH-DIAG-*`) ou Climatisation (`CLIM-DIAG-*`), et **ne modifie pas** ces rapports.

---

## 2. Objet, périmètre et limites

**Objet.** Les **deux cartes** du dashboard Arsenal affichant la **température minimale** et la **température maximale des chambres**, présentées comme une lecture thermique croisée Chauffage ↔ Climatisation.

**Périmètre.**
- Les deux templates de cartes et leur chaîne d'héritage UI.
- Les agrégats `sensor.temperature_min_chambres` / `sensor.temperature_max_chambres` et leur production.
- Les vérités contextuelles Chauffage / Climatisation / Météo mobilisables pour interpréter ces cartes.
- La confrontation aux règles UI opposables et aux contraintes d'interprétation.

**Limites.**
- Cet audit **n'audite pas** le fonctionnement général des domaines Chauffage ou Climatisation.
- Il **ne tranche pas** la sémantique que MIN/MAX devraient représenter (aucune autorité ne la définit — cf. §7).
- Il **ne produit aucun verdict global de conformité métier** sur les cartes, faute de contrat direct.

---

## 3. Base auditée

- **Dépôt** : `antoinevalentinHA/arsenal`.
- **Branche** : `claude/arsenal-temp-cards-audit-8cumpn`.
- **HEAD** : `34bf7cc6ad2139b3b102bf5e4822708132268c9e`.
- **Synchronisation** : à égalité stricte avec `origin/main` (ahead 0 / behind 0).
- **Arbre de travail** : propre.
- Le **runtime chargé fait foi** pour les constats de production et de logique ; les audits antérieurs ne servent que de repères.

---

## 4. Méthode par portes

1. **Porte 1** — constitution du corpus d'autorité et identification exacte de l'objet.
2. **Porte 2** — production réelle des vérités thermiques et diagnostiques (par zone, agrégats, vérités contextuelles).
3. **Porte 3** — logique réelle des deux cartes et de leur héritage UI.
4. **Porte 4** — comparaison finale et qualification par familles.
5. **Porte 5** — présente consignation documentaire.

Chaque porte a été validée explicitement avant la suivante, en lecture seule.

---

## 5. Identification exacte des deux cartes et de leur héritage

**Dashboard :** Arsenal (`arsenal-dashboard`), section `section_header` **« 🌡️ Températures »**.
**Fichier dashboard :** `18_lovelace/dashboards/arsenal.yaml` (instanciation des deux cartes dans la section Températures).

| Carte | Template | Fichier | Entité affichée | Intitulé (`name`) |
|---|---|---|---|---|
| MIN | `carte_temperature_min_chambres` | `19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_min_chambres.yaml` | `sensor.temperature_min_chambres` | « Température minimale » |
| MAX | `carte_temperature_max_chambres` | `19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_max_chambres.yaml` | `sensor.temperature_max_chambres` | « Température maximale » |

**Chaîne d'héritage (identique pour les deux), chemins complets :**

```
19_button_card_templates/40_dashboards/arsenal/30_diagnostic/carte_temperature_min_chambres.yaml
  └─ 19_button_card_templates/10_generiques/carte_temperature_confort.yaml      (show_icon: false)
       └─ 19_button_card_templates/00_socles/kpi/socle_kpi_label.yaml
            └─ 19_button_card_templates/00_socles/kpi/socle_kpi.yaml            (background-color : couleur externalisée)
                 └─ 19_button_card_templates/00_socles/carte_base_v2.yaml       (72px, tap=more-info, typo #111)
```

(La carte `carte_temperature_max_chambres.yaml` suit la même chaîne.)

**Responsabilités effectives (runtime) :**
- **Valeur (state)** : entité d'instance via `socle_kpi` (18px/700, °C).
- **Nom** : dashboard (« Température minimale » / « Température maximale »).
- **Icône** : masquée (`show_icon: false` dans `19_button_card_templates/10_generiques/carte_temperature_confort.yaml`).
- **Label** : bloc JS local de la carte (attribut de chambre).
- **Couleur de fond** : bloc JS **local de la carte** (voir §11–§12).
- **Action** : `tap: more-info` (hérité de `19_button_card_templates/00_socles/carte_base_v2.yaml`).

**Réutilisation.** Les deux **templates** ne sont instanciés que dans `18_lovelace/dashboards/arsenal.yaml`. Les deux **entités** agrégats sont, elles, largement consommées ailleurs (Chauffage, Climatisation, Aération, point de rosée, cartes clim `50_eligibilite`), mais ces consommateurs **n'imposent pas** la sémantique UI des deux cartes.

**Mention explicite :** **les deux cartes ne relèvent d'aucune autorité normative directe** (cf. §6.A et §7).

---

## 6. Corpus d'autorité

### 6.A — Autorités directes de l'objet : absentes

Aucune autorité ne définit **directement** la **sémantique métier** des cartes ni un **mapping couleur propre** à `temperature_min_chambres` / `temperature_max_chambres` : aucun contrat ne dit *ce que ces cartes doivent raconter* ni *quelle vérité leur couleur doit traduire*.

Ce constat **ne contredit pas** §6.C : la **doctrine UI transversale** (charte couleurs, architecture UI) **reste pleinement applicable** à ces cartes en tant que règles générales de restitution opposables à toute carte Arsenal. La distinction est donc :
- **absente** : autorité **directe** définissant la sémantique/mapping propre à MIN/MAX ;
- **présente et applicable** : règles UI **transversales** gouvernant toute restitution (§6.C).

La seule pièce du dépôt qui **nomme** les templates de cartes est un **plan d'action non normatif** (cf. §7).

### 6.B — Autorités contextuelles Chauffage / Climatisation / Météo (normatives, mais ne gouvernent pas les cartes)

**Météo (production par zone) :**
- `00_documentation_arsenal/contrats/meteo/temperature_interieure/consolidation.md` (v1.4)
- `00_documentation_arsenal/contrats/meteo/temperature_interieure/stabilisation.md` (v1.1)
- `00_documentation_arsenal/contrats/meteo/tendance_temperature.md`
- `00_documentation_arsenal/contrats/meteo/axe_temperature.md` (plausibilité 8–40, cf. §18 D3)

**Climatisation :**
- `00_documentation_arsenal/contrats/climatisation/03_decision_canonique.md`
- `00_documentation_arsenal/contrats/climatisation/04_entrees_metier.md`
- `00_documentation_arsenal/contrats/climatisation/05_decision_candidats.md`
- `00_documentation_arsenal/contrats/climatisation/10_observabilite.md`
- `00_documentation_arsenal/contrats/climatisation/13_intensite_besoin_froid.md`
- `00_documentation_arsenal/contrats/climatisation/14_recommandation_ventilation.md`
- `00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/00_overview.md`
- `00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/20_binary_sensors_franchissement.md`
- `00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md`
- `00_documentation_arsenal/contrats/climatisation/capteurs/besoins/10_besoins.md`

**Chauffage :**
- `00_documentation_arsenal/contrats/chauffage/50_standby_hysteresis.md`
- `00_documentation_arsenal/contrats/chauffage/70_autorisation_thermostat.md`
- `00_documentation_arsenal/contrats/chauffage/72_offsets_thermiques_lecture_physique.md`
- `00_documentation_arsenal/contrats/chauffage/90_semantique_thermique.md`
- `00_documentation_arsenal/contrats/chauffage/15_capteurs/01_capteurs_decision.md`
- `00_documentation_arsenal/contrats/chauffage/dependances_inter_domaines.md` (**descriptif, non doctrinal**)

### 6.C — Doctrine UI (transversale, opposable à toute carte Arsenal)
- `00_documentation_arsenal/ui/couleurs/README.md`
- `00_documentation_arsenal/ui/couleurs/01_principes.md`
- `00_documentation_arsenal/ui/couleurs/02_palette.md`
- `00_documentation_arsenal/ui/couleurs/02_1_palette_etiquettes.md`
- `00_documentation_arsenal/ui/couleurs/03_exceptions.md`
- `00_documentation_arsenal/ui/couleurs/04_typographie.md`
- `00_documentation_arsenal/ui/couleurs/05_regles.md`
- `00_documentation_arsenal/ui/architecture_transverse.md` (transformations UI autorisées/interdites)
- `00_documentation_arsenal/ui/architecture.md` (deux stratégies de couleur coexistantes)
- `00_documentation_arsenal/ui/socle_ui/06_kpi.md`

### 6.D — Documentation descriptive
- `00_documentation_arsenal/README.md`
- `19_button_card_templates/40_dashboards/arsenal/README.md`
- En-têtes des fichiers de cartes et du parent générique.
- Trilogie d'audit `temperature_interieure` (rapport / arbitrage / plan) et chantiers clim « stratégie COOL » — **descriptifs, non normatifs**.

---

## 7. Constat d'absence de contrat direct

- Le contrat par zone (`00_documentation_arsenal/contrats/meteo/temperature_interieure/consolidation.md` et `00_documentation_arsenal/contrats/meteo/temperature_interieure/stabilisation.md`) gouverne `sensor.temperature_<zone>` (consolidation → stabilisation → façade), **pas** les agrégats chambres.
- **Aucun contrat ne régit** `temperature_min_chambres` / `temperature_max_chambres` : ils sont **déclarés en entrée** par des contrats consommateurs, jamais gouvernés quant à leur mémoire, leur périmètre ou leur fraîcheur.
- Le **rapport d'audit** `00_documentation_arsenal/audits/01_rapports/temperature_interieure/audit_temperature_interieure_rapport_final.md` qualifie ces agrégats de **« références thermiques de décision de facto … ni souveraines ni contractualisées »**.
- Le **plan d'action** `00_documentation_arsenal/audits/03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md` (non normatif) propose de « créer le contrat aujourd'hui absent » (Lot 1) et est le **seul document** nommant les templates de cartes (Lot 4, à l'état de proposition).
- La **note d'arbitrage** `00_documentation_arsenal/audits/02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md` (non normative) recense des options non tranchées.
- Le **registre des chantiers** ne référence **aucun chantier** ouvert pour ces agrégats.

→ **Les deux cartes et leurs agrégats n'ont aucune autorité normative directe** définissant leur sémantique ou leur mapping couleur.

---

## 8. Production des températures par zone

Chaîne souveraine, une instance par zone : `_1` (HomeKit) + `_2` (Zigbee) → consolidée → stabilisée → façade.

**Fichiers producteurs (chemins complets) :**
- `12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/consolidation.yaml` → `sensor.temperature_brute_consolidee_<zone>`
- `12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/stabilisation.yaml` → `sensor.temperature_stabilisee_<zone>`
- `12_template_sensors/meteo/mesures/temperature/interieur_multi_capteurs/facade.yaml` → `sensor.temperature_<zone>`

*(`<zone>` désigne volontairement une famille de zones : `chambre_arnaud`, `chambre_matthieu`, `chambre_parents`, `sejour`, `entree`, `petite_maison`.)*

| Étape | Validation | Fraîcheur | Comportement dégradé |
|---|---|---|---|
| Consolidation | numérique + `5 ≤ v ≤ 45` | **TTL 1800 s** (`last_changed`) + `time_pattern /5` | abstention **`unknown`** si aucune source valide et mémoire expirée |
| Stabilisation | garde `5..45` ; EWMA α=0,35, δ_max=0,3 | **TTL 1800 s** + `time_pattern /5` | **`unknown`** si brute indisponible + mémoire expirée |
| Façade | `availability` (stabilisée ∉ unknown/unavailable/none) | — | façade **`unavailable`** |

→ **La chaîne par zone est gouvernée, bornée et sait s'abstenir** (conforme au contrat).

---

## 9. Production des agrégats MIN / MAX

**Fichiers producteurs exacts :**
- `12_template_sensors/meteo/mesures/temperature/chambres/min/valeur.yaml` → `sensor.temperature_min_chambres`
- `12_template_sensors/meteo/mesures/temperature/chambres/min/nom.yaml` (projection de nom associée)
- `12_template_sensors/meteo/mesures/temperature/chambres/max/global/valeur.yaml` → `sensor.temperature_max_chambres`
- `12_template_sensors/meteo/mesures/temperature/chambres/max/global/nom.yaml` (projection de nom associée)
- Entité **séparée, hors périmètre chambres** : `12_template_sensors/meteo/mesures/temperature/chambres/max/rdc/valeur.yaml` → `sensor.temperature_max_rdc`

| Propriété | Constat runtime |
|---|---|
| **Opérandes réels** | 3 **façades** chambres : `sensor.temperature_chambre_arnaud`, `sensor.temperature_chambre_matthieu`, `sensor.temperature_chambre_parents` |
| **Périmètre effectif** | **3 chambres uniquement** ; `sejour`/`entree` → agrégat RDC séparé ; `petite_maison` exclue |
| **Méthode** | dict → `selectattr('1','is_number')` → `sort(attribute=1)` → `[0]` (min) / `[-1]` (max) → `round(1)` |
| **Opérandes partiellement indisponibles** | min/max sur les façades restantes numériques (redondance) |
| **Aucun opérande exploitable** | branche `{% else %}` → **`{{ last }}`** avec `last = this.state` (valeur **figée**) |
| **Mémoire / fallback** | `this.state` republié ; attribut `chambre_la_plus_froide` / `chambre_la_plus_chaude` avec repli `'Mémoire'` |
| **Bornage de la mémoire** | **AUCUN** : ni `last_changed`, ni TTL, ni `time_pattern` |
| **Mise à jour** | triggers = `state` des 3 façades + `homeassistant start` (aucun `time_pattern`) |
| **Attributs** | `chambre_la_plus_froide` / `chambre_la_plus_chaude` (repli `'Mémoire'`), liste des sources |
| **Consommateurs principaux** | Chauffage (`autorisation_cible`, `ecart_consigne/*`, `diagnostic_thermique/*`), Climatisation (franchissements, `intensite_besoin_froid`), Aération, point de rosée, UI |

**État non numérique / `unknown`.** Un état non numérique peut apparaître **avant la première valeur exploitable** au démarrage, ou lors d'une **phase transitoire de rechargement**. En revanche, **une fois une valeur numérique mémorisée**, l'agrégat **tend à la republier sans borne temporelle** (pas de TTL, pas de `time_pattern`) : en régime établi, il ne repasse pas de lui-même à `unknown`. *(Le comportement exact à l'initialisation dépend du moteur de template Home Assistant et du type de rechargement ; aucune impossibilité absolue n'est affirmée pour tous les cas de reload.)*

→ **Constat de production :** les agrégats **filtrent** les opérandes indisponibles puis **republient `this.state`** sans borne temporelle ; en régime établi, **l'indisponibilité totale peut rester masquée** par une ancienne valeur numérique. **Aucun contrat ne les gouverne.**

---

## 10. Vérités contextuelles Chauffage et Climatisation

**Distinction stricte des couches (à ne jamais confondre) :**
**franchissement** (observation) ≠ **besoin** (métier) ≠ **admissibilité** (verrou décisionnel) ≠ **décision** (`clim_target_mode`) ≠ **action** (état HVAC réel).

### 10.1 Chauffage (interprétation possible de la borne froide)
- `input_number.chauffage_consigne_confort` (défaut 19), `input_number.chauffage_offset_on` (0.5), `input_number.chauffage_offset_off` (0.5).
- `sensor.chauffage_autorisation_cible` — producteur : `12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml`. Cette entité est une **autorisation / intention** ternaire `comfort/neutre/reduced` (**pas la décision souveraine Chauffage**). Le seuil de besoin y est calculé **inline** : `seuil_on = consigne − offset_on` ; **son calcul intègre en outre** le blocage poêle, la température extérieure, la présence et l'anticipation/météo. **Aucun capteur backend n'expose ce seuil principal comme vérité consommable.**
- Blocages : `input_boolean.chauffage_blocage_aeration`, `input_boolean.blocage_chauffage_poele`, fenêtre. Application/exécution : `input_boolean.chauffage_standby_force`, consigne chaudière (bridge).

### 10.2 Climatisation (interprétation possible de MAX / MIN)
- **Seuils COOL** (présence-dépendants) : `sensor.seuil_allumage_clim_applique` (`12_template_sensors/climatisation/seuils_on_off/cool/on.yaml`), `sensor.seuil_extinction_clim_applique` (`12_template_sensors/climatisation/seuils_on_off/cool/off.yaml`).
- **Seuil HEAT d'appoint** : `sensor.seuil_allumage_chauffage_clim` = `temperature_consigne_appliquee_locale − clim_offset_on` (`12_template_sensors/climatisation/seuils_on_off/heat/on.yaml`) — **base et offset distincts du chauffage principal**.
- **Franchissement COOL ON** : `binary_sensor.clim_seuil_allumage_cool_atteint` (`12_template_sensors/climatisation/seuils_on_off/cool/seuil_allumage_cool_atteint.yaml`) = **`temperature_max_chambres ≥ seuil_allumage_clim_applique`** ; garde indisponibilité → `false`. **Couche observation.**
- **Franchissement COOL OFF** : `binary_sensor.clim_seuil_extinction_cool_atteint` (`12_template_sensors/climatisation/seuils_on_off/cool/seuil_extinction_cool_atteint.yaml`) = `temperature_min_chambres ≤ seuil_extinction_clim_applique`.
- **Besoin brut** : `binary_sensor.besoin_clim_cool` (`12_template_sensors/climatisation/besoin/cool.yaml`) — hystérésis sur les deux franchissements COOL.
- **Admissibilité** : `binary_sensor.besoin_clim_cool_admissible` (`12_template_sensors/climatisation/besoin/cool_admissible.yaml`), enveloppe canonique reflétant `input_boolean.besoin_clim_cool_admissible`, piloté par `11_automations/climatisation/cool/admissibilite.yaml` (id `10030000000114`, verrou à deux portes gardé par l'autorisation : fenêtres / aération / horaire / absence / extérieur).
- **Décision** : `sensor.clim_target_mode` (`12_template_sensors/climatisation/decision/mode_target.yaml`) — consomme **exclusivement** les admissibles (`cool > dry > heat > off`).
- **Raison / action** : `sensor.clim_raison_decision` (`12_template_sensors/climatisation/decision/raison.yaml`) ; `sensor.clim_action_en_cours` (`12_template_sensors/climatisation/decision/action_en_cours.yaml`, état HVAC réel).
- **Intensité** : `sensor.clim_intensite_besoin_froid` (`12_template_sensors/climatisation/ventilation/intensite_besoin_froid.yaml`) = `max(0, temperature_max_chambres − seuil_extinction_clim_applique)` — **avec garde anti-gel réelle** (disponibilité conditionnée à la fraîcheur d'au moins une façade), contrairement à l'agrégat et au franchissement.

---

## 11. Logique réelle des cartes

**Entités réellement lues par chaque carte** (aucun include, aucune variable transmise par le dashboard) :
`sensor.temperature_min_chambres` **ou** `sensor.temperature_max_chambres` ; `input_number.chauffage_consigne_confort` ; `input_number.chauffage_offset_on` ; `binary_sensor.clim_seuil_allumage_cool_atteint`.

**Non lues** : `input_number.chauffage_offset_off`, `sensor.chauffage_autorisation_cible`, `sensor.seuil_allumage_clim_applique`, `sensor.seuil_extinction_clim_applique`, franchissements HEAT, `binary_sensor.besoin_clim_cool`, `binary_sensor.besoin_clim_cool_admissible`, `sensor.clim_target_mode`, `sensor.clim_raison_decision`, `sensor.clim_action_en_cours`, blocages, température extérieure, présence.

**Rendu (les deux cartes) :** valeur = état de l'agrégat (18/700, °C) ; nom = dashboard ; **pas d'icône** ; label = attribut de chambre (repli `'Inconnue'`) ; `tap` = more-info.

**Fait d'héritage.** Le bloc `background-color` de `19_button_card_templates/00_socles/kpi/socle_kpi.yaml` (couleur externalisée `sensor.couleur_*`) **et** le bloc local de la carte coexistent dans la liste `styles.card` ; le bloc local, **appliqué en dernier, l'emporte**. De plus, `sensor.couleur_temperature_min_chambres` / `sensor.couleur_temperature_max_chambres` **n'existent pas** : le mécanisme hérité est **ombré / mort**. **La couleur effective est intégralement celle du bloc JS local de la carte.**

---

## 12. Arbres couleur MIN et MAX

**Couleurs exactes employées par les cartes :**
- RED = `rgba(244, 67, 54, 0.2)`
- GREEN = `rgba(76, 175, 80, 0.2)`
- BLUE = `rgba(33, 150, 243, 0.2)` — **bleu sémantique « information / technique »** (`00_documentation_arsenal/ui/couleurs/02_palette.md`)
- GREY = `rgba(158, 158, 158, 0.2)` — **gris neutre** (« inactif / aucune demande »)

**Couleurs de référence de la charte, pour comparaison :**
- Gris **indisponibilité** : `rgba(158, 158, 158, 0.1)` — **jamais émis par ces cartes**.
- Bleu **thermique** (Exception 2, « froid / température basse ») : `rgba(144, 202, 249, 0.25)` — **non employé par ces cartes**.

**Arbre de décision (identique MIN/MAX, seule l'entité `temp` diffère) :**
```
temp        = valeur numérique de l'agrégat de la carte (min ou max) sinon null
cons_chauff = input_number.chauffage_consigne_confort sinon null
off_chauff  = input_number.chauffage_offset_on sinon null
cool_on     = binary_sensor.clim_seuil_allumage_cool_atteint (state)

1. si (temp===null OU cons_chauff===null OU off_chauff===null OU cool_on ∉ {'on','off'})
                                             → GREY  rgba(158,158,158,0.2)
2. seuil_chauff_on = cons_chauff − off_chauff
3. si cool_on === 'on'                       → RED   rgba(244,67,54,0.2)
4. si temp < seuil_chauff_on                 → BLUE  rgba(33,150,243,0.2)
5. sinon                                     → GREEN rgba(76,175,80,0.2)
```

**Description factuelle par branche (chaque branche est descriptible) :**
- **RED** = franchissement COOL ON, basé sur `temperature_max_chambres` (couche **observation**) — **identique sur les deux cartes**, y compris MIN.
- **BLUE** = température de la carte `< (consigne_confort − offset_on)` (seuil chauffage principal **recalculé localement**, sans hystérésis, sans le contexte décisionnel).
- **GREEN** = **résiduel** (ni COOL franchi, ni sous le seuil chauffage).
- **GREY** = un opérande non numérique ou franchissement hors `{on,off}` — en **gris neutre `0.2`**, non en gris indisponibilité `0.1`.

**Couche réellement représentée :** combinaison locale de plusieurs couches et périmètres (observation clim sur MAX + seuil chauffage recomputé sur l'entité de la carte + résiduel). **L'arbre n'a pas de sémantique unifiée, claire et documentée**, bien que ses branches soient individuellement descriptibles.

---

## 13. Confrontation `OBJ-1 … OBJ-8`

> Rappel : `OBJ-*` **structurent l'audit**, ils ne sont pas transformés en contrats.

| Règle | Verdict (MIN=MAX sauf mention) | Justification |
|---|---|---|
| **OBJ-1** — backend décide / UI observe | **PARTIEL** | RED observe un franchissement backend ; BLUE/GREEN relèvent d'une **classification locale autorisée** ; aucune décision backend fabriquée ni persistée ; enjeu résiduel purement sémantique. |
| **OBJ-2** — pas de recalcul métier / reproduction / état implicite | **INDÉTERMINABLE faute de sémantique gouvernante** | La comparaison locale et la classification **non persistée** relèvent de catégories **explicitement autorisées** (`00_documentation_arsenal/ui/architecture.md` « seuils locaux » ; `00_documentation_arsenal/ui/architecture_transverse.md` « classification locale non réutilisée »). **Aucun capteur backend n'expose** le seuil `consigne − offset_on` comme vérité consommable ; la carte **ne reproduit pas** toute l'autorisation Chauffage ; elle **ne persiste ni ne réexporte** son résultat. La qualification en non-conformité dépendrait de la sémantique cible, absente. **Non qualifié `NON CONFORME`.** |
| **OBJ-3** — réalité unique par couleur | **NON CONFORME** | Critère `00_documentation_arsenal/ui/couleurs/05_regles.md` non satisfait : **pas de réalité unique/claire/documentée** ; la couche change selon les branches ; combinaison **cross-entity non explicitée** sur MIN. Les branches restent descriptibles ; le défaut est l'absence de sémantique **unifiée et documentée**. |
| **OBJ-4** — indispo `0.1` prioritaire | **NON CONFORME** | La branche fallback émet `rgba(158,158,158,0.2)` ; le gris indisponibilité `rgba(158,158,158,0.1)` n'est **jamais émis**. Écart de logique UI, **distinct** du masquage par la production (§9). |
| **OBJ-5** — neutre `0.2` distinct d'indispo `0.1` | **NON CONFORME** | Un **gris unique `0.2`** couvre « aucune donnée exploitable » **et** « repos » : indistinction. Même cause racine qu'OBJ-4. |
| **OBJ-6** — palette sémantique, sens stable | **NON CONFORME** | Le bleu `rgba(33,150,243,0.2)` (« information/technique ») est employé pour « froid ». Ce n'est pas non plus la valeur thermique de l'Exception 2 (`rgba(144,202,249,0.25)`). Usage **hors réalité documentée, quel que soit le régime**. |
| **OBJ-7** — Exception thermique (si employée) | **INDÉTERMINABLE** | L'Exception 2 n'est **pas** mise en œuvre (valeurs sémantiques employées, pas d'orange chauffe) ; savoir si elle **devrait** gouverner ces cartes relève d'une ambiguïté sémantique (§18-B). |
| **OBJ-8** — `#111` typographique | **CONFORME** | Couleur portée par le fond (`color_type: card`) ; `name/state/label` restent `#111` ; aucun état encodé par le noir. |

---

## 14. Confrontation `INT-1 … INT-4`

> Rappel : `INT-*` sont des **contraintes d'interprétation** contextuelles, non des contrats des cartes.

| Contrainte | Verdict | Constat |
|---|---|---|
| **INT-1** — ne pas confondre les couches | **CONFONDU (présentation)** ; couche cible **INDÉTERMINABLE** | RED présenté comme « surchauffe clim COOL » (= franchissement) ; BLUE comme « froid/besoin chauffage » (= seuil recomputé). |
| **INT-2** — franchissement ≠ besoin ≠ admissibilité ≠ décision | **CONFONDU** | `binary_sensor.clim_seuil_allumage_cool_atteint` (franchissement d'observation) traité comme « la vérité clim COOL ». |
| **INT-3** — un offset ne crée pas un besoin | **PARTIEL** | L'offset est utilisé dans un **seuil** (usage légitime) ; la carte matérialise néanmoins une classification besoin-like locale. |
| **INT-4** — neutre = état normal | **RESPECTÉ** (pas d'alarme) ; sémantique de GREEN **INDÉTERMINABLE** | L'absence de franchissement/seuil retombe en GREEN, sans alerte ; mais GREEN agrège plusieurs réalités backend et n'a pas de sémantique définie. |

---

## 15. Scénarios diagnostiquement trompeurs

> La colonne « Réellement visible » ne liste que ce que la carte rend littéralement (valeur numérique, chambre en label, couleur de fond). Les libellés interprétatifs figurent en colonne « Interprétation raisonnable » : **ce sont des déductions possibles de l'utilisateur, pas des textes affichés par la carte**.

| Scénario | Réellement visible | Vérité réellement lue | Interprétation raisonnable | Conséquence | Atteignabilité |
|---|---|---|---|---|---|
| **MIN rouge car MAX a franchi COOL** | valeur (chambre la plus froide) + label chambre + **fond rouge** | franchissement COOL sur `temperature_max_chambres` | fond rouge pouvant être interprété comme une demande/action COOL attribuée à la valeur affichée | diagnostique | **réelle** |
| **MIN/MAX bleue, chauffage non autorisé** | valeur + label + **fond bleu** | `temp < consigne − offset_on`, sans poêle/ext/présence/blocages | fond bleu pouvant être interprété comme une demande de chauffe | diagnostique | **réelle** |
| **Rouge alors que besoin COOL non admissible** | valeur + label + **fond rouge** | franchissement seul ; admissibilité/décision non lues | fond rouge pouvant être interprété comme une demande/action COOL effective | diagnostique | **réelle** |
| **Non-rouge alors que décision/action COOL active** | valeur + label + **fond bleu ou vert** | franchissement `off` par hystérésis alors que `clim_target_mode`/action encore COOL | fond non rouge pouvant être interprété comme une absence de demande COOL | diagnostique | **réelle** |
| **Agrégat gelé, couleur maintenue** | valeur + **label `'Mémoire'`** + fond coloré | valeur périmée (`{{ last }}`) | valeur et couleur pouvant être interprétées comme vivantes | diagnostique | **réelle** (panne totale des 3 chambres) |
| **Indisponibilité réelle rendue neutre** | **fond gris `0.2`** | opérande non numérique | fond gris pouvant être interprété comme un repos / aucune demande | diagnostique | **quasi inatteignable** (agrégat gelé) ; réelle surtout au démarrage/rechargement |
| **GREEN regroupant des situations différentes** | valeur + label + **fond vert** | ni COOL franchi, ni sous le seuil chauffage | fond vert pouvant être interprété comme un état nominal | visuelle/diagnostique | **réelle** (cas dominant) |

---

## 16. Synthèse propre à la carte MIN

- **Rendu de la valeur** : la carte **projette fidèlement** l'état numérique de l'agrégat ; le calcul du minimum est **correct dès qu'au moins une façade est vivante**. **Réserve : la fiabilité temporelle de cette valeur n'est pas garantie** — en indisponibilité totale, une ancienne valeur peut être **maintenue indéfiniment** ; le label `'Mémoire'` est un indice, **sans âge ni statut de fraîcheur exposé**. *(Rendu fidèle à la source ≠ fiabilité de la source.)*
- **Label chambre** : fidèle à l'attribut (chambre / `'Mémoire'` / `'Inconnue'`).
- **Couleur BLUE** : classification locale **autorisée** dans sa forme ; **couche prétendue non documentée** (OBJ-3 / ambiguïté sémantique) ; bleu employé hors réalité documentée (**OBJ-6 NON CONFORME**).
- **Couleur RED (pilotée par MAX)** : **ambiguïté sémantique forte avec conséquence diagnostique** — la couleur décrit la chambre **la plus chaude** alors que la carte affiche la **plus froide**. **Non qualifiée de non-conformité métier** (aucune règle n'impose que la couleur décrive l'entité affichée) ; **aggrave OBJ-3**.
- **GREEN résiduel** : **indéterminable** (agrège plusieurs réalités backend).
- **Indisponibilité** : écart UI démontré (gris `0.2`, jamais `0.1`) **et** masquée par la production (deux causes distinctes).
- **État mémoire** : non signalé en couleur ; seul le label peut passer à `'Mémoire'`.

---

## 17. Synthèse propre à la carte MAX

- **Rendu de la valeur** : idem MIN — projection fidèle, calcul du maximum correct si ≥ 1 façade vivante, **même réserve de fiabilité temporelle** (mémoire non bornée, pas de statut de fraîcheur).
- **Label chambre** : chambre / `'Mémoire'` / `'Inconnue'`.
- **Couleur BLUE** : idem MIN (OBJ-6 NON CONFORME ; couche prétendue → ambiguïté sémantique).
- **Couleur RED (cohérente avec le franchissement)** : **cohérente avec l'entité affichée** (`temperature_max_chambres ≥ seuil COOL ON`) ; reste un **franchissement**, pas une décision (INT-2).
- **GREEN résiduel** : indéterminable (idem).
- **Indisponibilité** : écart UI + masquage production (idem).
- **État mémoire** : non signalé en couleur (idem).

> **Verdicts globaux distincts** : sur MAX, le RED est cohérent avec la valeur affichée ; sur MIN, il décrit une autre grandeur — **ambiguïté de restitution plus sévère** (ambiguïté sémantique forte, conséquence diagnostique), **sans non-conformité métier démontrée**.

---

## 18. Classement A / B / C / D des causes racines

> Familles **strictement séparées** : écarts UI ≠ ambiguïtés sémantiques ≠ défauts de production ≠ dettes documentaires.

### A — Écarts UI démontrés (règle opposable, indépendants de la sémantique) — **2**
- **A1** — indisponibilité et neutralité confondues par un **gris unique `rgba(158,158,158,0.2)`** ; le gris indisponibilité `rgba(158,158,158,0.1)` n'est jamais émis (OBJ-4 + OBJ-5).
- **A2** — **bleu sémantique `rgba(33,150,243,0.2)` employé pour « froid »** (OBJ-6).

*(OBJ-3 est NON CONFORME, mais sa cause racine est distribuée en B et D ; il n'est pas recompté comme cause A indépendante.)*

### B — Ambiguïtés sémantiques (absence d'autorité) — **6**
- **B1** — couche gouvernante de la couleur non définie (physique / franchissement / besoin / autorisation / décision).
- **B2** — régime de palette non tranché (palette sémantique vs Exception 2 thermique).
- **B3** — sens de GREEN (résiduel) non défini.
- **B4** — légitimité/rôle de **RED-sur-MIN** (modèle cross-entity) non contractualisé.
- **B5** — place du HEAT d'appoint clim (silence volontaire ou lacune ?).
- **B6** — régime de la classification locale / couche que BLUE prétend représenter (seuil chauffage recomputé).

### C — Défauts / limites de production des agrégats — **3**
- **C1** — mémoire `{{ last }}` **non bornée** ; agrégats ne devenant pas `unknown` en régime établi → **indisponibilité masquée**.
- **C2** — **périmètre non contractualisé** (3 chambres ; RDC séparé ; petite maison exclue).
- **C3** — **fraîcheur non exposée** (aucun statut / âge sur les agrégats).

### D — Dettes documentaires — **5**
- **D1** — en-têtes des cartes inexacts (« aucune décision » ; « vérité contractuelle clim COOL » = franchissement ; « froid basé sur chauffage principal » = seuil recomputé).
- **D2** — `19_button_card_templates/10_generiques/carte_temperature_confort.yaml` déclaré « pure / aucune transformation locale » alors que les enfants transforment.
- **D3** — plausibilité **8–40 °C** (`00_documentation_arsenal/contrats/meteo/axe_temperature.md` §3) vs **5–45 °C** (runtime / `00_documentation_arsenal/contrats/meteo/temperature_interieure/consolidation.md`).
- **D4** — asymétrie **max-ON / min-OFF** COOL documentée dans un fichier **non normatif** (`00_documentation_arsenal/contrats/climatisation/capteurs/seuils_et_franchissements/90_observations.md`), alors que le runtime en dépend.
- **D5** — **absence de contrat d'agrégation** gouvernant `sensor.temperature_min_chambres` / `sensor.temperature_max_chambres` (mémoire, périmètre, fraîcheur non normés).

> **Note de recomposition (vérification dépôt, lecture seule).** Une dette précédemment envisagée — « fichier de fallback météo inexistant » — **n'est plus valide** : `00_documentation_arsenal/contrats/meteo/fallback.md` **existe** et est correctement référencé par `00_documentation_arsenal/contrats/meteo/axe_temperature.md`. Elle a donc été retirée. La famille D reste à **5 dettes indépendantes** après avoir **scindé** l'ancien regroupement (asymétrie non normative **et** absence de contrat d'agrégation sont désormais deux constats distincts, D4 et D5).

---

## 19. Bilans chiffrés séparés

**19.1 — Règles UI `OBJ-*`** (par carte ; identiques MIN/MAX) :
- CONFORME : **1** (OBJ-8)
- PARTIEL : **1** (OBJ-1)
- NON CONFORME : **4** (OBJ-3, OBJ-4, OBJ-5, OBJ-6)
- INDÉTERMINABLE : **2** (OBJ-2, OBJ-7)

**19.2 — Contraintes `INT-*`** :
- RESPECTÉE : **1** (INT-4, volet « pas d'alerte » ; sémantique GREEN indéterminable)
- PARTIELLE : **1** (INT-3)
- CONFONDUE : **2** (INT-1, INT-2)

**19.3 — Constats par famille (causes racines dédupliquées)** :
- Écarts UI démontrés (A) : **2**
- Ambiguïtés sémantiques (B) : **6**
- Défauts de production (C) : **3**
- Dettes documentaires (D) : **5**

*(A1 et C1 concernent le même symptôme visible — indisponibilité invisible — mais restent deux causes distinctes. OBJ-4 et OBJ-5 partagent la cause A1.)*

---

## 20. Complexité constatée

| Type | Constat | Origine |
|---|---|---|
| **Accidentelle** | arbre couleur combinant 3 couches/périmètres (observation clim + seuil chauffage recomputé + résiduel) | absence de doctrine |
| **Duplication** | deux templates quasi identiques ; recompute d'un **fragment** de seuil chauffage (pas de toute l'autorisation) | reconstruction locale |
| **Logique morte** | bloc couleur externalisée hérité de `19_button_card_templates/00_socles/kpi/socle_kpi.yaml` **ombré** ; `sensor.couleur_temperature_min_chambres` / `sensor.couleur_temperature_max_chambres` inexistants | héritage technique |
| **Dépendances croisées** | RED des deux cartes piloté par le **même** franchissement basé sur MAX (cross-entity sur MIN) | reconstruction locale |
| **Responsabilités mélangées** | cartes déclarées « pures / sans décision » portant classification locale + recompute | absence de doctrine |

*(La branche GREY (indisponibilité) est de surcroît quasi inatteignable, en raison du gel des agrégats — défaut de production, §9.)*

**Aucune des complexités du modèle de couleur recensées ici n'est rattachée à une exigence métier directe démontrée.** Leur origine dominante est l'absence de doctrine, la reconstruction locale et l'héritage technique. *(Ce constat vise le seul modèle de couleur de ces deux cartes, non l'ensemble des cartes ni la chaîne thermique.)*

---

## 21. Ce qui est gouvernable aujourd'hui

| Élément | Statut |
|---|---|
| Rendu de la valeur à sa source (socle, °C, more-info) | **Conforme (rendu)** — la fiabilité de la **source** relève de C |
| `#111` typographique (OBJ-8) | **Conforme** |
| Gris indisponibilité `0.1` / distinction neutre-indispo (A1) | **Écart dont la règle cible est déjà opposable** ; **déterminable sans arbitrage métier supplémentaire** |
| Bleu employé pour « froid » (A2) | **Écart dont la règle cible est déjà opposable** ; **déterminable sans arbitrage métier supplémentaire** |
| Couleur sans réalité unique/documentée (OBJ-3) | **Constat déterminable** contre `00_documentation_arsenal/ui/couleurs/05_regles.md` ; **correction complète non déterminable sans contrat** |
| Classification locale / couche prétendue par BLUE (OBJ-2, B6) | **Indéterminable sans sémantique gouvernante** |
| RED-sur-MIN (B4), régime de palette (B2), sens de GREEN (B3), HEAT (B5), couche gouvernante (B1) | **Non gouvernés ; correction non déterminable sans contrat** |
| Visibilité réelle de l'indisponibilité | **Bloquée par un défaut de production** (C1) |
| Périmètre / fraîcheur des agrégats (C2/C3) | **Défaut de production** (hors UI) |
| En-têtes, README, plausibilité, asymétrie non normative, absence de contrat d'agrégation (D) | **Dette documentaire** |

**Constat de gouvernabilité :** une **correction complète et déterministe** de la couleur **n'est pas atteignable à partir des seuls contrats existants**. Deux écarts ont une **règle cible déjà opposable** (gris `0.1` ; bleu hors réalité) et sont déterminables sans arbitrage métier supplémentaire ; en revanche, la sémantique gouvernante de la couleur (OBJ-3, points B) n'est pas déterminable sans contrat, et la visibilité de l'indisponibilité reste bloquée par un défaut de production (C1). **Aucun séquencement de correction n'est formulé ici.**

---

## 22. Conclusion (cinq questions)

1. **Les deux cartes affichent-elles correctement les valeurs MIN/MAX ?**
   Le **rendu est fidèle à la source** et le calcul est correct dès qu'au moins une façade est vivante. **Mais la fraîcheur de la source n'est pas garantie** : en indisponibilité totale, une ancienne valeur peut être maintenue indéfiniment ; le label `'Mémoire'` est un indice, sans âge ni statut. (Rendu fidèle ≠ fiabilité temporelle de la source.)

2. **Leur couleur est-elle fiable et interprétable sans ambiguïté ?**
   **Non.** La couleur n'a pas de sémantique unifiée, claire et documentée (OBJ-3), ne distingue pas indisponibilité et neutralité (OBJ-4/5), et emploie le bleu hors sa réalité documentée (OBJ-6). La carte **MIN** présente le cas cross-entity le plus trompeur (RED piloté par MAX) ; la carte **MAX** est moins trompeuse.

3. **Quels défauts sont déjà démontrables contre la doctrine UI actuelle ?**
   `OBJ-3`, `OBJ-4`, `OBJ-5`, `OBJ-6`, et les confusions de couche `INT-1` / `INT-2`. **`OBJ-2` n'en fait pas partie** (classification locale autorisée ; verdict indéterminable sans sémantique gouvernante).

4. **Quels choix ne peuvent pas être tranchés sans contrat transversal dédié ?**
   La couche gouvernante de la couleur, le régime de palette, le sens de GREEN, la légitimité de RED-sur-MIN, la place du HEAT, et le régime de classification locale / la couche prétendue par BLUE (B1–B6), ainsi que la remédiation d'OBJ-3.

5. **L'état actuel justifie-t-il une phase d'arbitrage puis de contractualisation avant correction complète ?**
   **Oui, factuellement.** Deux écarts sont déterminables sur une règle déjà opposable ; mais la correction de fond de la couleur suppose de définir ce que MIN/MAX doivent représenter (absent), la remédiation d'OBJ-3 en dépend, OBJ-2 reste indéterminable sans cette sémantique, et la visibilité de l'indisponibilité est bloquée par un défaut de production. **Ce rapport constate ce préalable ; il ne rédige aucun contrat et ne recommande aucun modèle cible.**

---

## 23. Limites et objets hors périmètre

- Cet audit **ne définit pas** la sémantique cible des cartes ni ne rédige de contrat.
- Il **ne recommande** aucun capteur, aucune architecture, aucune mutualisation, aucun patch, aucun chantier.
- Il **n'audite pas** le fonctionnement métier général du Chauffage ou de la Climatisation ni **n'importe** les verdicts `CH-DIAG-*` / `CLIM-DIAG-*`.
- `sensor.temperature_max_rdc`, les zones hors chambres, la chaîne extérieure/jardin, et la logique interne des consommateurs (au-delà de leur relation aux agrégats) sont **hors périmètre**.
- La réconciliation de la plausibilité 8–40 / 5–45 est **signalée comme dette documentaire** (§18 D3), non traitée ici.
- Les branches marquées « quasi inatteignables » décrivent des états que le code ne rencontre pas en régime établi ; elles sont signalées comme telles.
