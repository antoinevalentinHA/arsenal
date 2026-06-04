# Audit du dossier `19_button_card_templates`

> **Périmètre :** dépôt `antoinevalentinHA/arsenal`, HEAD `50e8998` (2026-06-04), dossier `19_button_card_templates` analysé récursivement.
> **Nature :** audit **exclusivement documentaire**. Aucun patch, aucun diff, aucune modification, aucun renommage, aucune déduplication. Tout verdict de factorisation est argumenté et présenté comme *hypothèse à valider*, jamais comme action.
> **Méthode :** clone réel du dépôt, parsing YAML des 220 fichiers (loader tolérant aux tags Home Assistant pour ne pas ignorer silencieusement les consommateurs `18_lovelace`), reconstruction du graphe d'héritage, mesure de similarité par paires sur corps normalisés (hors commentaires), extraction et hachage des blocs JavaScript, recensement d'usage sur **l'ensemble du dépôt** (1 554 fichiers YAML).

---

## 1. Résumé exécutif

| Indicateur | Valeur |
|---|---|
| Fichiers analysés | **240** (220 YAML + 20 README.md) |
| Templates `button_card_templates` définis | **220** (1 par fichier sauf 2 exceptions) |
| — dont couche *bibliothèque* réutilisable (`00_socles` / `10_generiques` / `20_transverses`) | **61** |
| — dont couche *dashboards métier* (`40_dashboards`) | **159** |
| Documents analysés | **20 README.md** |
| Racines d'héritage | 4 (`carte_base_v2`, `socle_badge_42`, `socle_etat_lecture_principale`, `socle_header_base`) |
| Cycles d'héritage | **0** |
| Parents externes non résolus | **0** (bibliothèque auto-portante) |
| Doublons de fichier entier (exacts ou normalisés) | **0** |
| Templates sans aucune référence dans tout le dépôt | **4** |
| Blocs JavaScript répétés à l'identique (≥2) | 11 |
| Blocs `card_mod` / `custom_fields` | **0** (absents) |
| Couverture de l'en-tête normé `# ARSENAL` | **220 / 220 (100 %)** |

**Niveau global de qualité : ÉLEVÉ.** L'arborescence présente une hygiène structurelle remarquable : héritage strict et acyclique, aucune duplication de fichier entier, en-tête documentaire normé sur 100 % des fichiers, style entièrement porté par le mécanisme natif `styles:` de button-card (aucun `card_mod` sauvage, aucun `custom_fields` épars), nommage globalement systématique.

**Niveau global de dette technique : FAIBLE à MODÉRÉ.** La dette n'est pas dans des doublons, mais dans : (a) une **prolifération de jumeaux paramétriques** dans `00_socles` (familles KPI / status / etat différant de 1 à 2 lignes) ; (b) **4 templates complets mais jamais référencés** ; (c) une **dérive d'idiome** sur le test d'indisponibilité JS (deux écritures sémantiquement non équivalentes coexistent) ; (d) des **lacunes documentaires** ciblées (couche bibliothèque non documentée, 5 dashboards sans README, 2 README obsolètes).

**Niveau global de risque : FAIBLE.** Aucun élément ne menace le fonctionnement actuel. Les sujets identifiés sont des sujets de *maintenabilité* et de *lisibilité*, pas de correction. Plusieurs « opportunités » apparentes sont en réalité des **zones à ne pas toucher** (cf. §5), car la similarité textuelle y recouvre une distinction sémantique intentionnelle.

---

## 2. Cartographie de l'arborescence

### 2.1 Organisation observée

```
19_button_card_templates/
├── 00_socles/         33 fichiers — fondations UI (héritage de base)
│   ├── (racine)       carte_base_v2, socle_badge_42, socle_decision_72,
│   │                  socle_header_base, socle_info_72
│   ├── action/        5 socles d'action
│   ├── diagnostic/    3 socles de diagnostic
│   ├── etat/          3 socles d'état
│   ├── kpi/           6 socles KPI
│   ├── status/        9 socles de statut
│   └── toggle/        3 socles de bascule
├── 10_generiques/     20 fichiers — cartes génériques métier-agnostiques
│   ├── action/        3 cartes d'action
│   ├── badges/        1 badge
│   ├── headers/       2 en-têtes de section
│   ├── navigation/    2 boutons de navigation
│   └── (racine)       12 cartes (kpi, mode, seuils, conformité, température…)
├── 20_transverses/    8 fichiers — éléments transverses (navigation, alertes, timers)
│   └── navigation/badges/  5 badges de navigation nommés
└── 40_dashboards/     159 fichiers — templates spécifiques par domaine
    └── (25 sous-dossiers : aeration, alarme, arsenal, audi, boiler, chauffage,
        climatisation, deshumidificateur, eclairage, ecs, ecs_petite_maison,
        imprimerie, meteo, modes, mouvements, nas, nas_imprimerie, netatmo,
        ouvertures, prises, sante, system, ups, vmc, volets)
```

### 2.2 Logique de structuration (déduite, cohérente)

L'arborescence matérialise une **stratification par niveau d'abstraction**, conforme à la discipline Arsenal (séparation des couches) :

1. **`00_socles`** — fondations visuelles/comportementales pures, sans logique métier. `carte_base_v2` est la racine de fait (32 consommateurs).
2. **`10_generiques`** — cartes réutilisables, paramétrables, indépendantes d'un domaine (ex. `carte_kpi_bleu`, `carte_capteur_seuils`).
3. **`20_transverses`** — éléments présents sur plusieurs dashboards (navigation, alertes paramètres, timers).
4. **`40_dashboards`** — instances métier, une carte = une intention d'affichage domaine.

Point structurel essentiel : **tout le dossier est injecté via `!include_dir_merge_named /config/19_button_card_templates`** dans les vrais dashboards Lovelace situés dans `18_lovelace/`. Conséquence : *chaque fichier* (y compris ceux de `40_dashboards`) définit un `button_card_template` nommé enregistré globalement ; les **consommateurs réels** (vues Lovelace) sont **hors du présent dossier**. Toute analyse d'« orphelin » menée sans scanner `18_lovelace/` serait donc fausse — c'est ce qui motive le recensement d'usage sur l'ensemble du dépôt (cf. §1 et §7).

### 2.3 Familles de templates identifiées

| Famille | Membres (socles) | Trait commun | Axe de variation |
|---|---|---|---|
| **KPI** | `socle_kpi`, `socle_kpi_72`, `socle_kpi_72_sans_icone`, `socle_kpi_label`, `socle_kpi_label_72`, `socle_kpi_label_72_sans_icone` | valeur dominante (`state` 18px/700) | présence label, présence icône, hauteur |
| **Status** | `socle_status`, `socle_status_72`, `socle_status_compact`, `socle_status_label`, `socle_status_label_72`, `socle_status_label_sans_nom`, `socle_status_label_xl`, `socle_status_state_bottom_72` | lecture d'état (`state` 14px/400) | label, nom, taille, position |
| **Action** | `socle_action_simple`, `socle_action_simple_sans_couleur`, `socle_action_critical`, `socle_action_label_compact`, `socle_action_script_confirme` | interaction (tap actif) | couleur, criticité, confirmation |
| **Toggle** | `socle_toggle`, `socle_toggle_compact_68`, `socle_toggle_confirme` | `action: toggle` | confirmation, compacité |
| **Diagnostic** | `socle_diagnostic`, `socle_diagnostic_compact`, `socle_diagnostic_compact_readonly_72` | lecture diagnostique | compacité, lecture seule |
| **Navigation (badges)** | `bouton_accueil`, `bouton_retour`, `bouton_diagnostics`, `bouton_parametres`, `bouton_navigation` (`_badge_carre`) | héritent `bouton_navigation_base` | icône, nom, `navigation_path` |
| **Header** | `section_header`, `sub_section_header` | héritent `socle_header_base` | niveau hiérarchique |

---

## 3. Inventaire des doublons

**Aucun doublon de fichier entier** n'existe : ni à l'identique (corps hors commentaires), ni après normalisation agressive (espaces/indentation supprimés). Sur 220 fichiers, **220 empreintes de corps distinctes**. Les « doublons » de cet audit sont donc exclusivement **partiels** (jumeaux paramétriques et blocs JS répétés).

### 3.1 Jumeaux paramétriques de socles (similarité ≥ 0,90)

84 paires dépassent 0,70 de similarité ; le noyau dur (≥ 0,90) est concentré dans `00_socles`. Différences mesurées au diff exact :

| # | Fichiers concernés | Sim. | Éléments communs | Différence **exacte** | Verdict |
|---|---|---|---|---|---|
| D1 | `kpi/socle_kpi_72` ↔ `status/socle_status_72` | **0,987** | structure, héritage `carte_base_v2`, dimensions, désactivation interactions | `state`: **18px/700** (KPI) vs **14px/400** (status) | **Ne pas factoriser** — la typographie du `state` *est* la sémantique (valeur dominante vs lecture d'état). Cf. §5. |
| D2 | `kpi/socle_kpi_label_72` ↔ `kpi/socle_kpi_label_72_sans_icone` | **0,985** | tout le corps | `show_icon: true` vs `false` | Factorisation envisageable (Lot 3) — variante par 1 booléen. Réserve : sémantique de fusion des `styles` (cf. §4). |
| D3 | `kpi/socle_kpi_72` ↔ `kpi/socle_kpi_72_sans_icone` | **0,983** | tout le corps | `show_icon: true` vs `false` | Idem D2, **mais** `socle_kpi_72_sans_icone` est **sans usage** (cf. §7). À traiter d'abord côté usage, pas factorisation. |
| D4 | `toggle/socle_toggle_confirme` ↔ `action/socle_action_script_confirme` | **0,965** | échafaudage de confirmation, JS de confirmation | `action: toggle` vs `call-service` | **Ne pas factoriser** — type d'action structurellement différent. Le partage se limite au bloc JS de confirmation (cf. §3.2, J-confirm). |
| D5 | `status/socle_status_label` ↔ `status/socle_status_label_sans_nom` | **0,952** | tout le corps | présence/absence du `name` | Factorisation envisageable (Lot 3) ; faible gain, à valider visuellement. |
| D6 | `status/socle_status_label` ↔ `etat/socle_etat_reel` | **0,949** | structure de lecture | `socle_etat_reel` **sans usage** + nuances de style | **Vérifier d'abord l'intention** de `socle_etat_reel` (cf. §7) avant tout rapprochement. |

> Les paires 0,70–0,90 (78 autres) relèvent de la **ressemblance de famille** (mêmes fondations, même grille 72px) et **non** de duplication : elles partagent l'ADN `carte_base_v2` mais divergent sur des attributs porteurs de sens (taille, couleur, position, interactions). Elles sont listées dans l'annexe technique (fichier `sim.json` reproductible) mais ne constituent pas des cibles de factorisation.

### 3.2 Blocs JavaScript répétés (≥ 2 occurrences, corps normalisé identique)

| Réf. | Occ. | Extrait | Nature |
|---|---|---|---|
| J-unavail-A | **4** | `entity.state === "unknown" || entity.state === "unavailable"` | garde d'indisponibilité (idiome A) |
| J-none-B | **3** | `['unknown','unavailable','none'].includes(entity?.state)` | garde d'indisponibilité (idiome B) |
| J-confirm-txt | 2 | `variables?.confirmation || "Confirmer l'exécution de cette action ?"` | message de confirmation par défaut |
| J-confirm-act | 2 | `variables?.action_service ? "call-service" : "none"` | sélection d'action conditionnelle |
| J-mm | 2 | `parseFloat(entity.state) … toFixed(1)} mm` | formatage millimètres |
| J-bg-onoff-green | 2 | `entity.state === 'on' ? 'rgba(76,175,80,…)' : 'rgba(158,…)'` | fond on/off (vert/gris) |
| J-bg-onoff-red | 2 | `entity.state === "on" ? "rgba(244,67,54,…)" : "rgba(76,175,80,…)"` | fond on/off (rouge/vert) |
| J-seuils | 2×2 | gardes de seuils `s_crit` / `s_low` / `seuil_faible` | classification par seuils |

**Incohérence notable (J-unavail-A vs J-none-B) :** les deux idiomes **ne sont pas équivalents**. L'idiome B (`['unknown','unavailable','none'].includes(entity?.state)`) gère en plus (1) l'entité `null`/`undefined` via le chaînage optionnel `entity?.` et (2) l'état `'none'`. L'idiome A (14 fichiers) plante ou se comporte différemment si `entity` est absent ou si l'état vaut `'none'`. Au total, `unavailable` apparaît dans **97 fichiers / 411 occurrences** : la garde d'indisponibilité est omniprésente mais **non standardisée**. C'est le seul écart susceptible d'avoir un impact comportemental réel (cas limites). Ce n'est **pas** un doublon à fusionner mais une **dérive d'idiome à harmoniser** — à traiter avec prudence car chaque `[[[ … ]]]` button-card est isolé (pas de fonction partagée possible nativement).

---

## 4. Opportunités de factorisation

> ⚠️ **Avertissement transverse sur la sémantique button-card.** Dans custom:button-card, lorsqu'un template hérite d'un parent, les **listes `styles` sont concaténées** (et non remplacées) : le parent et l'enfant additionnent leurs entrées, la dernière l'emportant par cascade CSS. Convertir une variante « copie intégrale » (ex. `_sans_icone`) en variante « héritante + surcharge » **change la mécanique de fusion** et peut produire des différences de rendu subtiles. **Aucune des factorisations ci-dessous n'est sûre sans validation visuelle** sur dashboard réel. Elles sont présentées comme hypothèses argumentées, pas comme actions.

### F1 — Variantes `_sans_icone` héritant de leur jumelle « avec icône »

- **Principe :** `socle_kpi_label_72_sans_icone` hériterait de `socle_kpi_label_72` en surchargeant `show_icon: false` (idem `socle_kpi_72_sans_icone` ↔ `socle_kpi_72`).
- **Périmètre :** 2 paires (D2, D3).
- **Gain attendu :** suppression d'environ 40–55 lignes dupliquées par paire ; un seul point de vérité pour la typographie KPI.
- **Conditions nécessaires :** (1) vérifier que la concaténation de `styles` parent+enfant produit un rendu **strictement identique** à la copie actuelle ; (2) traiter d'abord le statut « sans usage » de `socle_kpi_72_sans_icone` (cf. §7) — inutile de factoriser un template à supprimer.
- **Niveau de risque :** **moyen** (sémantique de fusion `styles`).
- **Recommandation :** **Lot 3** (validation visuelle obligatoire). Ne traiter `socle_kpi_label_72_sans_icone` (11 usages, vivant) qu'après preuve d'équivalence de rendu.

### F2 — Harmonisation de la garde d'indisponibilité JS

- **Principe :** converger vers **un seul idiome** documenté (l'idiome B, plus robuste, est le candidat naturel : il couvre `null` et `'none'`).
- **Périmètre :** jusqu'à 97 fichiers contenant `unavailable`.
- **Gain attendu :** cohérence comportementale sur les cas limites, réduction du risque de divergence future.
- **Conditions nécessaires :** **démonstration au cas par cas** que basculer A→B ne change pas le rendu là où `entity` est toujours défini et où `'none'` n'apparaît jamais. **L'impact fonctionnel n'est PAS nul a priori** (B traite `'none'` différemment) — cette harmonisation **sort donc du périmètre « risque nul »** et relève d'un chantier comportemental à part entière, pas d'un nettoyage.
- **Niveau de risque :** **élevé** si appliqué mécaniquement.
- **Recommandation :** **ne pas inclure dans un lot de factorisation à risque nul.** En faire un sujet documenté (convention d'idiome) et trancher domaine par domaine. À ce stade : **documenter, ne pas modifier.**

### F3 — Famille des badges de navigation

- **Principe théorique :** les 5 `bouton_*_badge_carre` ne diffèrent que par `icon`, `name` et `tap_action.navigation_path` ; ils pourraient être un unique template paramétré par variables.
- **Périmètre :** 5 templates **mais 216 sites d'appel** (93 + 62 + 31 + 17 + 13).
- **Gain attendu :** −4 fichiers.
- **Conditions nécessaires :** réécrire chaque site d'appel pour passer `icon`/`name`/`navigation_path` en variables.
- **Niveau de risque :** **élevé** (churn massif sur 200+ appels, perte de la lisibilité « rôle nommé »).
- **Recommandation :** **NE PAS FAIRE.** Ce sont des **constantes de navigation nommées** (rôles sémantiques), pas une duplication accidentelle. Cf. §5. Le gain (−4 fichiers) ne compense ni le risque ni la perte d'expressivité.

### F4 — Bloc de confirmation partagé (D4, J-confirm)

- **Principe :** `socle_toggle_confirme` et `socle_action_script_confirme` partagent l'échafaudage de confirmation (message + logique). Un socle intermédiaire « confirmable » pourrait porter le commun.
- **Périmètre :** 2 socles.
- **Gain attendu :** factorisation du message/JS de confirmation.
- **Conditions nécessaires :** isoler le commun **sans** coupler les types d'action (`toggle` vs `call-service`), qui doivent rester distincts.
- **Niveau de risque :** **moyen-élevé** (l'héritage button-card ne permet pas de « trou » d'action proprement ; risque de sur-ingénierie pour 2 fichiers).
- **Recommandation :** **non prioritaire.** Gain faible, complexité conceptuelle réelle. À documenter comme convention plutôt qu'à coder.

---

## 5. Zones à ne pas toucher

Ces ensembles présentent une **forte similarité textuelle** mais une **distinction sémantique intentionnelle**. Les fusionner détruirait de l'information de conception sans gain fonctionnel.

1. **`socle_kpi_72` vs `socle_status_72` (0,987).** La seule différence — typographie du `state` (18px/700 vs 14px/400) — **encode la sémantique** : un KPI met une *valeur* en avant, un status *lit un état*. Deux intentions UI distinctes qui doivent rester nommées séparément. Fusionner reviendrait à confondre « combien » et « dans quel état ».

2. **Les 5 badges de navigation (`bouton_*_badge_carre`).** Rôles de navigation **nommés** (accueil, retour, diagnostics, paramètres, navigation) avec chacun son `navigation_path`. La similarité est attendue (ils héritent tous `bouton_navigation_base`) ; leur identité distincte est un **choix d'expressivité** qui rend les 216 sites d'appel lisibles. Cf. §4-F3.

3. **`socle_toggle_confirme` vs `socle_action_script_confirme` (0,965).** Types d'action fondamentalement différents (`toggle` vs `call-service`). La ressemblance porte sur la confirmation, pas sur la fonction.

4. **Toute la couche `00_socles` vis-à-vis de `10_generiques`.** Les génériques *satellisent* les socles (relation documentée « SATELLITE DE »). Leur proximité est structurelle et **voulue** ; ce n'est pas une redondance.

5. **Familles status/etat/diagnostic entre elles (0,79–0,95).** Elles partagent la grille 72px mais répondent à des intentions distinctes (statut interprété / état réel / diagnostic). À conserver tant que la taxonomie de la bibliothèque n'est pas explicitement repensée et documentée.

---

## 6. Audit documentaire

### 6.1 Vue d'ensemble

- **En-tête normé :** présent sur **220/220 fichiers YAML (100 %)** — bandeau `# ARSENAL` avec champs RÔLE, COMPORTEMENT, SOURCE, USAGE, et relations « SATELLITE DE / PIVOT ». Hygiène exemplaire et homogène.
- **README de domaine :** **20**, tous dans `40_dashboards/*`. Qualité globalement **élevée** : orientés principes (ex. chauffage : « UI ≠ décision », dualité intention/réel), structurés, pédagogiques.

### 6.2 Constats par document et par lacune

| Document / zone | Rôle | Qualité | Cohérence avec le code | Écart observé | Priorité |
|---|---|---|---|---|---|
| **Couche bibliothèque** `00_socles`, `10_generiques`, `20_transverses` | (devrait expliquer la taxonomie, le nommage, les règles d'héritage) | — | — | **AUCUN README.** Les 61 templates réutilisables — la fondation même — n'ont aucune documentation de niveau dossier (seuls les en-têtes par fichier existent). | **HAUTE** |
| **Racine** `19_button_card_templates/` | (devrait expliquer 00/10/20/40 et le mécanisme `!include_dir_merge_named`) | — | — | **AUCUN README racine.** La logique de stratification et le point d'injection Lovelace ne sont écrits nulle part. | **HAUTE** |
| `40_dashboards/modes/README.md` | doc domaine modes | bonne | **désynchronisée** | Utilise `carte_mode_maison_synthese` comme **exemple canonique** (4 occurrences, dont un titre de section) ; ce fichier **n'existe pas**. Le dossier contient en réalité `carte_mode_babysitting_synthese` + `carte_vacances_*`. | **MOYENNE** |
| `40_dashboards/sante/README.md` | doc domaine santé | bonne | **partiellement obsolète** | Liste `carte_frequence_cardiaque_qualitative` (l. 28 et arbre l. 82) ; **inexistant**. Restructuré depuis en `carte_cardio_nuit_synthese` / `cartes_cardio_nuit`. | **MOYENNE** |
| Dashboards `ecs_petite_maison`, `imprimerie`, `nas_imprimerie`, `netatmo`, `ups` | doc domaine | absente | — | **5 dashboards sur 25 sans README.** | **MOYENNE** |
| Les 4 templates sans usage (cf. §7) | — | — | — | **Aucun n'est mentionné dans aucun README** : intention (réserve ? abandon ?) non tracée. | **MOYENNE** |

### 6.3 Conventions documentées vs réellement appliquées

| Convention | Documentée ? | Appliquée ? | Remarque |
|---|---|---|---|
| En-tête `# ARSENAL` normé | implicite (par l'exemple) | **oui, 100 %** | Convention de fait, jamais écrite formellement. À formaliser. |
| 1 fichier = 1 template | implicite | **218/220** | 2 exceptions : `thermo_variance_12h_72.yaml` (2 clés) et `cartes_cardio_nuit.yaml` (3 clés — nommage pluriel `cartes_` qui signale au moins l'intention). |
| Relation « SATELLITE DE » dans l'en-tête | oui (champ présent) | partiellement | Présente sur certains génériques, absente sur d'autres. À uniformiser. |
| Style via `styles:` natif, jamais `card_mod` | non écrit | **oui, total** | `card_mod` = 0, `custom_fields` = 0. Convention forte mais **non documentée**. |
| Nommage par préfixe (`socle_`/`carte_`/`bouton_`) | non écrit | **majoritaire, non strict** | Voir §7.4. |

### 6.4 Propositions documentaires (corrections, compléments, restructurations)

- **Corrections factuelles** (priorité moyenne) : aligner `modes/README.md` et `sante/README.md` sur les fichiers réellement présents (remplacer les exemples fantômes par des fichiers existants).
- **Compléments** (priorité haute) : créer un **README de bibliothèque** documentant la taxonomie des familles (§2.3), les règles d'héritage, le nommage, la convention « pas de `card_mod` », et la sémantique de concaténation des `styles`. Créer un **README racine** expliquant 00/10/20/40 et l'injection `!include_dir_merge_named`.
- **Compléments** (priorité moyenne) : ajouter les 5 README de dashboards manquants ; tracer l'intention des 4 templates sans usage.
- **Clarifications** : formaliser par écrit la convention d'en-tête normé (qui n'existe aujourd'hui que par mimétisme).
- **Restructuration** : envisager une **convention d'idiome JS** (garde d'indisponibilité) documentée, en préalable à toute harmonisation de code (cf. §4-F2).

---

## 7. Dette technique observée

### 7.1 Templates sans aucune référence dans tout le dépôt (4)

Recensement effectué sur **1 554 fichiers YAML** (loader tolérant aux tags HA, pour inclure les consommateurs `18_lovelace`). Ces 4 templates sont **complets** (non des ébauches), correctement rattachés à un parent, mais **jamais référencés** et **jamais documentés** :

| Template | Fichier | Lignes | Parent | Observation |
|---|---|---|---|---|
| `socle_etat_reel` | `00_socles/etat/socle_etat_reel.yaml` | 57 | `carte_base_v2` | Très proche (0,90–0,95) de `socle_status_label` et `socle_diagnostic` (vivants) → **possiblement supplanté**. |
| `socle_kpi_72_sans_icone` | `00_socles/kpi/socle_kpi_72_sans_icone.yaml` | 62 | `carte_base_v2` | = `socle_kpi_72` + `show_icon:false`. Variante triviale inutilisée. |
| `carte_bruit_seuils_variables` | `10_generiques/carte_bruit_seuils_variables.yaml` | 88 | `socle_kpi` | Générique complet, jamais instancié. |
| `carte_mode_toggle` | `10_generiques/carte_mode_toggle.yaml` | 34 | `socle_toggle` | Générique complet, jamais instancié. |

> **Verdict prudent :** le dépôt cloné est *shallow* (pas d'historique) et il est *théoriquement* possible que ces templates soient appelés depuis un dashboard hors dépôt ou défini manuellement dans l'UI. **Ne rien supprimer sans avoir vérifié l'absence de tout consommateur hors-dépôt.** Statut recommandé : **« candidats réserve/obsolète à statuer »**, à documenter explicitement (réservé pour usage futur *ou* déprécié), pas à dédupliquer sur hypothèse.

### 7.2 Prolifération de jumeaux paramétriques

`00_socles` compte plusieurs familles dont les membres ne diffèrent que par 1–2 attributs (`show_icon`, présence de `name`, typographie). C'est lisible mais **multiplie les points de vérité** : une évolution de la grille 72px doit être répercutée sur ~15 socles. Risque futur : **dérive silencieuse** entre jumeaux si une modification n'est pas propagée partout.

### 7.3 Dérive d'idiome JavaScript

La garde d'indisponibilité (cf. §3.2, §4-F2) coexiste sous (au moins) deux formes non équivalentes. Point faible de **cohérence comportementale** sur les cas limites (`null`, `'none'`). Risque futur : comportements divergents entre cartes selon l'idiome hérité du copier-coller d'origine.

### 7.4 Nommage : incohérences mineures

- **Préfixes mixtes** dans `10_generiques` : majorité en `carte_`, mais `status_72_on_off`, `status_72_info_transitoire`, `kpi_no_action` n'ont pas le préfixe `carte_`.
- **Racine nommée `carte_base_v2`** dans `00_socles` (où la convention est `socle_`) ; de plus, **`_v2` sans `v1`** présent dans le dépôt → **artefact de versioning** figé.
- **Suffixes de taille hétérogènes** : numériques (`_72` ×19, `_42` ×5, `_68` ×1) **et** sémantiques (`_compact` ×6, `_xl` ×1). Cas limite : `socle_toggle_compact_68` cumule les deux logiques (`compact` + `68`).

> Ces points sont **documentaires/cosmétiques** et **hors périmètre de modification** (le renommage est explicitement interdit). Ils sont signalés pour la **convention de nommage à écrire**, pas pour action immédiate.

### 7.5 Fichiers multi-clés (2)

`thermo_variance_12h_72.yaml` (2 templates) et `cartes_cardio_nuit.yaml` (3 templates) rompent la convention « 1 fichier = 1 template » (respectée à 218/220). Impact : **négligeable** fonctionnellement (le merge nommé accepte plusieurs clés par fichier), mais légère entorse à la prévisibilité de l'arborescence. À documenter comme exception assumée ou à statuer.

---

## 8. Plan de chantier recommandé

> Aucun de ces lots n'est exécuté ici. Ils sont ordonnés par **rapport gain/risque croissant** ; seuls les lots 1 et 2 sont à risque réellement nul.

### Lot 1 — Inventaire et documentation *(risque nul, valeur immédiate)*
1. Rédiger un **README racine** (`19_button_card_templates/`) : stratification 00/10/20/40, mécanisme `!include_dir_merge_named`, conventions.
2. Rédiger un **README de bibliothèque** (couvrant 00/10/20) : taxonomie des familles (§2.3), règles d'héritage, sémantique de concaténation des `styles`, convention « pas de `card_mod` ».
3. Corriger les **2 README obsolètes** (`modes`, `sante`) : remplacer les exemples fantômes par des fichiers existants.
4. Ajouter les **5 README de dashboards manquants** (`ecs_petite_maison`, `imprimerie`, `nas_imprimerie`, `netatmo`, `ups`).
5. **Statuer et documenter** l'intention des 4 templates sans usage (réserve vs déprécié) — *après* vérification d'absence de consommateur hors-dépôt.
6. Formaliser par écrit la **convention d'en-tête normé** et la **convention de nommage** (constat, pas renommage).

### Lot 2 — Factorisations triviales à risque nul
> **Constat de l'audit : il n'existe aucune factorisation strictement à risque nul** dans ce dossier. Toutes les pistes (F1, F2, F4) supposent soit une validation visuelle (concaténation `styles`), soit un arbitrage comportemental (idiome JS). **Ce lot est donc vide** — ce qui est en soi un indicateur positif de l'état du dossier. Ne rien forcer ici.

### Lot 3 — Factorisations nécessitant validation visuelle
1. **F1** — variantes `_sans_icone` héritant de leur jumelle : prototyper sur `socle_kpi_label_72_sans_icone` (vivant, 11 usages), **comparer le rendu pixel** avant toute généralisation. Écarter `socle_kpi_72_sans_icone` (à statuer côté usage d'abord).
2. **D5** — `socle_status_label_sans_nom` héritant de `socle_status_label` : faible gain, à valider visuellement.

### Lot 4 — Nettoyage final éventuel
1. Décision sur les 4 templates sans usage (suppression *uniquement* si absence de consommateur prouvée hors-dépôt).
2. Décision sur l'**harmonisation d'idiome JS** (F2) — **chantier comportemental distinct**, domaine par domaine, hors « nettoyage ».
3. Décision sur les 2 fichiers multi-clés (laisser en exception documentée vs scinder).

---

## 9. Conclusion

Le dossier `19_button_card_templates` est, dans son état au HEAD `50e8998`, une **bibliothèque UI saine et bien gouvernée** : héritage strict et acyclique, **zéro doublon de fichier entier**, en-tête normé sur 100 % des fichiers, style entièrement canalisé par le mécanisme natif `styles:` (aucun `card_mod`/`custom_fields` épars), nommage globalement systématique. Cette discipline est cohérente avec l'approche contractuelle Arsenal.

La dette identifiée est **réelle mais circonscrite**, et surtout de nature **documentaire et de cohérence**, pas de correction :
- la **couche bibliothèque réutilisable n'est pas documentée** au niveau dossier (lacune la plus structurante) ;
- **4 templates complets ne sont référencés nulle part** (à statuer, pas à supprimer à l'aveugle) ;
- une **dérive d'idiome JS** sur la garde d'indisponibilité introduit des divergences possibles sur les cas limites ;
- quelques **README obsolètes** et **manquants**.

Le point méthodologique le plus important de cet audit : **la similarité textuelle élevée entre socles ne constitue pas, ici, une opportunité de factorisation évidente.** La plupart des paires « presque identiques » encodent une distinction sémantique voulue (KPI vs status, rôles de navigation nommés, types d'action). Et les rares pistes de factorisation **réelles** (variantes `_sans_icone`) **ne sont pas à risque nul** à cause de la concaténation des listes `styles` propre à button-card : elles exigent une validation visuelle. Conformément à la consigne, **aucune déduplication ne doit être engagée sur la base d'une hypothèse**.

**Recommandation d'ouverture de chantier :** ne lancer immédiatement que le **Lot 1 (documentation, risque nul, forte valeur)**. Les Lots 3 et 4 ne méritent d'être ouverts qu'avec validation visuelle et arbitrage explicite ; le Lot 2 est, à juste titre, **vide**.

---

*Rapport produit en lecture seule. Aucun fichier du dépôt n'a été modifié, renommé ou supprimé. Aucun patch ni diff n'est proposé. Les empreintes, graphes d'héritage et mesures de similarité sont reproductibles à partir du HEAD indiqué.*
