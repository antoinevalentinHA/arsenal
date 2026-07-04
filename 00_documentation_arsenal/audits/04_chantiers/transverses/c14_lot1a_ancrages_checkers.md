# C14 — Lot 1A : réparation mécanique des ancrages des checkers

- **Type :** lot opérationnel du chantier [C14](chantier_couverture_ci_contrats_arsenal.md) — correction mécanique, **sans changement de comportement CI**
- **Statut :** exécuté — en attente de revue ; **clos sous réserve du GO propriétaire** (cf. §7)
- **Base :** `main` @ `2eaf41d` (post-#262)
- **Périmètre modifié :** `scripts/arsenal_contracts/*.py` (docstrings/commentaires uniquement) + ce rapport + index + registre
- **Hors périmètre (verrouillé) :** aucun YAML runtime, aucun ID, aucune règle métier, aucune regex, aucune constante, aucune nouvelle CI, aucun workflow, aucun contrat fonctionnel, aucun déplacement de document

---

## 1. Objectif du lot

Réparer mécaniquement l'ancrage **checker → document normatif** : faire pointer chaque checker vers sa source normative réelle par un **chemin repo stable**, sans toucher aux règles contrôlées. Le lot ne corrige pas les règles ; il corrige la **traçabilité** de la règle vers sa norme.

## 2. Rappel du principe C14

> **Tout constat d'absence doit être établi en ouvrant la cible, pas en s'arrêtant à un nom de fichier.**

> **Une norme mal ancrée n'est pas une norme absente.**

Conformément à ce principe, chaque document cible a été **ouvert et confirmé existant** avant correction (répertoires ECS, aération M0–M6, déshumidificateur, structure includes, contrats de domaine ; titres H1 des documents recorder et Netatmo). Aucun ancrage n'a été inventé.

## 3. Inventaire initial

76 checkers inspectés. Répartition par qualité d'ancrage constatée **avant** le lot :

| Catégorie d'ancrage | Nombre | Exemples | Action prévue |
|---|---:|---|---|
| 1. Chemin exact / auto-ancré par constante de code | **14** | `automation_ids`, `automation_prefix_domain`, `climatisation_*` (×4), `lovelace_*` (×3), `palmares_min_haute`, `presence`, `sommeil` ; auto-ancrés : `registre_chantiers`, `ui_couleurs`, `ui_runtime_colors` | aucune (déjà conforme) |
| 2. Nom / chapitre / version — document existant | **37** | ECS (×5), `alarme`, `boiler`, 13 domaines mono-fichier, météo (×6), aération recommandation/M0/M5, `chauffage_courbe_etancheite`, `initial_key`, structure (×4), **recorder**, **netatmo** | ajouter le chemin exact |
| 3. Nom littéral périmé — document réel ailleurs | **10** | éclairage (×3), `garage_toggle`, palmarès chaud/froid, `zones`, `volets_pluie`, `parametres_invalides`, aération M2 | remplacer par le chemin exact |
| 4. Citation absente — domaine contractualisé | **15** | `counters`, `timers`, inputs (×3), deshum (×3), aération M1/M3/M4/M6, `vacances`, `visite`, `vmc` | insérer un ancrage (docstring ou commentaire) |
| 5. Résiduel `doctrine.yml` | **0 checker** | règles `platform: template` et `mode:` (workflow, pas checker) | documenté §5, reporté en Lot 1B |
| **Total inspecté** | **76** | | **62 à corriger** |

## 4. Corrections réalisées

**62 checkers** ont reçu un ancrage par chemin exact. Le tableau ci-dessous regroupe par type (le détail ligne à ligne est le `git diff`). **La colonne « Comportement CI modifié ? » est `Non` sur toutes les lignes** — prouvé mécaniquement (cf. encadré).

| Checker (groupe) | Ancien ancrage | Nouvel ancrage | Type de correction | Comportement CI modifié ? |
|---|---|---|---|---|
| éclairage entrée/jardin/séjour, garage | `CONTRAT_ECLAIRAGE_*.md`, `CONTRAT_IMPLEMENTATION_GARAGE_TOGGLE.md` | `contrats/eclairage/{entree,jardin,sejour,garage}.md` | nom littéral périmé → chemin | Non |
| palmarès chaud / froid | `CONTRAT_PALMARES_*.md` | `contrats/meteo/palmares_{chaleur,froid}.md` | nom littéral périmé → chemin | Non |
| zones, volets, paramètres invalides | `CONTRAT_ZONES`, `CONTRAT_PLUIE_VOLETS`, `CONTRAT — PARAMÈTRES INVALIDES` | `contrats/{zones,volets_pluie,parametres_invalides}.md` | nom littéral périmé → chemin | Non |
| aération M2 | `contrats/aeration/M2/` (dossier inexistant) | `contrats/aeration_blocage_chauffage/m2_fin_episode/` | chemin périmé → chemin réel | Non |
| 13 domaines mono-fichier (arsenal_self, babysitting, batteries, bouclage, bssid, mobile, notifications, redondance, simulation, switchbot, ups, voiture, résilience) | nom/version sans chemin | `contrats/<domaine>.md` (chemin exact) | nom/version → chemin | Non |
| ECS (fondations, cycle, sécurité, désinfection, offsets) | chapitres sans chemin | `contrats/ecs/…` (dossier + chapitres) | nom → chemin | Non |
| alarme, boiler | chapitres sans chemin | `contrats/{alarme,boiler}/` | nom → chemin | Non |
| météo (consolidation, stabilisation, HR ×2, jardins ×2) | cité par `sensor.*` / `contrat_axe_*` | `contrats/meteo/…` (chemin exact) | nom → chemin | Non |
| chauffage courbe étanchéité, initial_key | filename / chemin relatif | chemin complet `00_documentation_arsenal/…` | complétion de chemin | Non |
| structure 01/02/03/19 | `Structure — NN (normatif)` | `architecture/00_structure_includes/*.md` | nom → chemin | Non |
| aération recommandation / M0 / M5 | filename / chapitres | `contrats/aeration…/…` | nom → chemin | Non |
| **catégorie 4** (counters, timers, inputs ×3, deshum ×3, aération M1/M3/M4/M6, vacances, visite, vmc) | aucune citation | docstring/commentaire d'ancrage ajouté vers le chemin exact | ajout d'ancrage | Non |
| **recorder** | titres (« Arsenal Recorder Contract, Fiche de Décision ») | `architecture/01_recorder/contrat.md` + `fiche_decision.md` (+ note de placement) | titre → chemin | Non |
| **netatmo** | « v1.1 » | `contrats/homekit_diagnostic.md` (+ note v1.1↔v1.2) | version → chemin | Non |

> **Preuve de non-régression (comportement CI inchangé).** Pour chacun des 62 checkers, le flux de **tokens de code** (hors commentaires et chaînes) a été comparé entre `origin/main` et l'arbre de travail via `tokenize` : **identique partout**. Seuls docstrings et commentaires ont changé. En complément : `py_compile` OK sur les 62 ; exécution d'un échantillon représentatif (`counters`, `vmc`, `recorder`, `diagnostic_netatmo`, `aeration_m0_recover`, `ecs_fondations`, `zones`, `resilience_integrations`) → **exit 0** partout, inchangé.

Convention d'ancrage retenue (uniforme) : une ligne `Contrat (source normative) : <chemin repo>` (ou `Référence` / `Source normative` selon l'en-tête existant), le chemin étant relatif à la racine du dépôt. Pour les checkers sans docstring, un docstring minimal a été inséré juste après le shebang (neutre à l'exécution). Pour les checkers à bannière `#`, une ligne de commentaire a été ajoutée dans la bannière.

## 5. Cas spécifiques

### 5.1 Recorder

Le contrat **existe déjà** ; aucun nouveau contrat n'a été écrit. L'ancrage du checker a été corrigé vers les deux documents existants :

- `00_documentation_arsenal/architecture/01_recorder/contrat.md` (« Arsenal — Contrat Recorder Home Assistant ») ;
- `00_documentation_arsenal/architecture/01_recorder/fiche_decision.md`.

**Question de statut signalée séparément (non traitée dans ce lot) :** ces documents vivent sous `architecture/01_recorder/`, dossier dont le `README.md` déclare « documents d'**architecture**… n'introduit aucune règle métier », alors que `contrat.md` est rédigé normativement et confronté par CI. Le docstring du checker porte désormais une note explicite renvoyant à cet arbitrage. **Le contrat n'a pas été déplacé** (le déplacement n'est pas démontré indispensable ici ; il relève d'un arbitrage documentaire — cf. §6).

### 5.2 Netatmo

Le contrat **existe déjà** : `00_documentation_arsenal/contrats/homekit_diagnostic.md` (« Contrat — Diagnostic station météo Netatmo », couche observation). Aucun contrat Netatmo séparé n'a été créé. L'ancrage du checker pointe désormais vers ce chemin. La **dérive de version** (checker cité « v1.1 » ↔ document en **v1.2**) est **signalée dans le docstring** : les invariants vérifiés restent le socle v1.1 ; l'alignement effectif de version (vérifier que le checker couvre bien v1.2, ou acter que v1.2 n'ajoute pas d'invariant testable) est laissé en résiduel — il demande une lecture du delta v1.1→v1.2, qui dépasse la réparation mécanique.

### 5.3 `doctrine.yml`

Cas **à part, non traité dans ce lot** (conforme à la consigne). Le workflow `doctrine.yml` porte deux règles inline :

- interdiction de `platform: template` (legacy) dans les répertoires de template sensors ;
- obligation d'un `mode:` sur les automations.

Ces deux règles **ne citent aucune clause écrite** d'un contrat ou d'une doctrine du dépôt — c'est le **seul vrai cas** de règle CI sans source normative écrite (les 76 checkers, eux, sont tous ancrés). Ce n'est pas un ancrage à réparer mais une **clause à créer ou à rattacher**, plus une correction de règle (`mode:` testé par fichier et non par automation ; check `default_entity_id` désactivé). Cela dépasse la réparation mécanique et **est reporté en micro-lot séparé C14 — Lot 1B** (rattachement/écriture de la clause + durcissement), à ouvrir après arbitrage.

## 6. Résiduel après Lot 1A

Volontairement laissé ouvert :

1. **Statut / placement du contrat recorder** — arbitrage documentaire : déplacer/promouvoir en `contrats/`, ou amender le README de `architecture/01_recorder/`. (Item P3 du backlog C14.)
2. **Alignement de version Netatmo** (v1.1 ↔ v1.2) — demande une lecture du delta, non mécanique.
3. **`doctrine.yml`** — clause à écrire/rattacher + durcissement → **Lot 1B**.
4. **Hygiène des workflows** (renommage `clim_ventilation_contracts.yml`, chemins morts de path filters, auto-référence de `contracts_19_button_card_templates.yml`) — hors ancrage checker, reste au backlog C14 (P3).
5. **Autres lots C14 non ouverts** : chargement HA (P0), durcissement `doctrine.yml` (Lot 1B), frontière git / sécurité publication (P1), et les lots 2–3 (enforcement chauffage, anti-dérive du registre de couverture, doctrines transverses, domaines nus).

Aucune citation n'a nécessité d'arbitrage bloquant : toutes les cibles étaient identifiables et confirmées.

## 7. Conclusion

Le Lot 1A est **exécuté et prouvé non régressif** : 62 checkers ré-ancrés par chemin exact, les 14 restants déjà conformes, **zéro changement de comportement CI** (preuve par comparaison de tokens de code + exécution d'échantillon). L'objectif — que chaque checker pointe clairement vers sa source normative réelle — est atteint pour l'intégralité des 76 checkers.

Le lot est **prêt à clore** sous réserve du GO propriétaire. Les seuls points normatifs restants (placement recorder, version Netatmo, `doctrine.yml`) sont explicitement reportés (§6) et ne relèvent pas de la réparation mécanique.
