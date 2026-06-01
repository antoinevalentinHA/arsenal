# Étape A — Proposition de réécriture contractuelle (VAC-IMP-1)

> **Statut :** proposition de rédaction — **à relire avant génération des patchs documentaires**.
> **Nature :** texte contractuel cible, document par document. **Aucun patch, aucun diff, aucun YAML, aucun runtime, aucune CI.** Le dépôt n'est pas modifié ; ce document est produit hors du clone.
> **Fondement :** note de réconciliation Étape A validée (axe unique : le régime d'absence chauffage consomme `binary_sensor.vacances_actives`, jamais la projection `input_select.mode_maison` ; `sensor.chauffage_autorisation_cible` redevient purement thermique — option B ; `decision_centrale` devient l'unique arbitre Vacances).
> **Hors liste :** `vacances.md` n'est pas réécrit (référence, conforme en substance, §10 inchangé). `66_adaptation_consigne_vacances.md` reste la référence d'alignement, **inchangé**.

## Conventions de lecture

Chaque contrat est traité en cinq points : (1) sections à modifier ; (2) texte cible proposé ; (3) suppressions ; (4) ajouts ; (5) justification normative. Les blocs `« … »` citent le texte **actuel** ; les blocs encadrés `>` donnent le **texte cible proposé**. Aucun identifiant technique (token de raison, `unique_id`, slug) n'est renommé ; les identifiants normatifs nouveaux éventuels sont **explicitement signalés « à ratifier »** (numérotation non inventée d'autorité).

---

## A. `80_table_decision_canonique.md`

### A.1 Sections à modifier
§3.1 (axes), §3.4 (pré-confort), §4 (table — lignes 6 / 6\* et note d'exception), **§6 (note pré-confort — clause VAC-AME-3)**, §9 (libellés interdits).

### A.2 / A.3 / A.4 — Texte cible, suppressions, ajouts

**§3.1 — axe « contexte majeur ».**
- Actuel : « mode maison Vacances (contexte majeur à effet conditionnel — voir §4) ».
- **[REMPLACEMENT]** cible :
> - absence effective Vacances (`binary_sensor.vacances_actives = on`) — contexte majeur à effet conditionnel (voir §4)

**§3.4 — source d'autorisation amont « pré-confort ».**
- Actuel : « est une exception normative interne au contexte `mode_maison = Vacances` », « évaluée exclusivement dans ce contexte ».
- **[REMPLACEMENT]** cible :
> - est une exception normative interne au contexte d'**absence effective Vacances** (`binary_sensor.vacances_actives = on`),
> - elle est évaluée exclusivement dans ce contexte, pas comme autorisation amont générique,
> - elle reste soumise à l'absence de tout blocage pur actif et à la validation complète de la Décision Centrale.

**§4 — table, lignes 6 et 6\*.**
- Actuel : « Mode maison = Vacances, pré-confort inactif → `reduced` » et « Mode maison = Vacances, pré-confort actif → `comfort` ».
- **[REMPLACEMENT]** cible (cellules « Contexte actif ») :
> | 6  | Absence effective Vacances (`vacances_actives = on`), pré-confort inactif | `reduced` | Sobriété maximale imposée |
> | 6\* | Absence effective Vacances (`vacances_actives = on`), pré-confort actif *(exception)* | `comfort` | Exception normative explicite |

**§4 — note d'exception normative Vacances.**
- Actuel : « lorsque `input_boolean.pre_confort_actif_calcule` est actif en contexte Vacances … Cette exception est interne au contexte Vacances. »
- **[REMPLACEMENT]** cible :
> **Exception normative Vacances (ligne 6\*) :** lorsque `input_boolean.pre_confort_actif_calcule` est actif **en absence effective Vacances (`binary_sensor.vacances_actives = on`)**, et en l'absence de tout blocage pur actif (lignes 1 à 5), la Décision Centrale peut produire `comfort`. Cette exception est interne au contexte d'absence effective Vacances. Elle ne constitue pas un contournement de blocage.

**§6 — note pré-confort (suppression de la clause VAC-AME-3).**
- Actuel : « … traitée exclusivement dans le contexte `mode_maison = Vacances` (§4, ligne 6\*). Elle ne bénéficie d'aucun effet en dehors de ce contexte, **quelle que soit l'activité de `binary_sensor.vacances_actives`.** »
- **[SUPPRESSION]** de la proposition « quelle que soit l'activité de `binary_sensor.vacances_actives` ».
- **[REMPLACEMENT]** cible :
> **Note sur le pré-confort retour vacances :** cette source d'autorisation n'est pas évaluée en régime absence standard. Elle est traitée **exclusivement lorsque l'absence Vacances est effective (`binary_sensor.vacances_actives = on`)** (§4, ligne 6\*). Hors de ce contexte d'effectivité, elle ne produit aucun effet. La projection `input_select.mode_maison = Vacances` ne suffit pas à elle seule : c'est l'effectivité qui gouverne le régime, conformément à `vacances.md` §10.

**§9 — libellés interdits.**
- **[REMPLACEMENT]** de forme uniquement, pour cohérence sémantique (le sens des interdictions est inchangé) :
> | Confort en **absence effective Vacances** hors pré-confort autorisé | ❌ | Sobriété maximale |
> | Confort produit par pré-confort hors **absence effective Vacances** | ❌ | Exception bornée au contexte d'effectivité Vacances |

### A.5 Justification normative
Alignement direct sur `vacances.md` §10 (« chauffage → `vacances_actives` **uniquement** ») et §8.2 (le régime réduit est une « conséquence métier d'absence effective »). La suppression de la clause de §6 lève **VAC-AME-3** (la seule contradiction frontale du corpus). Les tables §5/§6/§7 (présence/absence/inhibition), l'override §3.4, et l'ensemble §8/§10/§11 demeurent **inchangés**.

---

## B. `80_table_decision_canonique__reecriture_partielle.md`

### B.1 Sections à modifier
§4.2 (contexte majeur Vacances — table de comportement) ; libellés « Vacances » de §3 et §9 (forme).

### B.2 / B.3 / B.4 — Texte cible

**§4.2 — table.**
- Actuel : « Mode maison = Vacances, pré-confort inactif → `reduced` » / « Mode maison = Vacances, pré-confort actif → `comfort` ».
- **[REMPLACEMENT]** cible :
> ### 4.2 Contexte majeur Vacances — effet conditionnel (registre sécurité/contexte)
>
> | Contexte | Décision finale | Justification |
> |----------|-----------------|---------------|
> | Absence effective Vacances (`vacances_actives = on`), pré-confort inactif | `reduced` | Sobriété maximale imposée |
> | Absence effective Vacances (`vacances_actives = on`), pré-confort actif | `comfort` *(exception normative)* | Exception bornée au contexte d'effectivité Vacances |
>
> L'exception pré-confort demeure interne à l'absence effective Vacances et soumise à la validation complète de la Décision Centrale (cf. `40 §6.1`). La projection `input_select.mode_maison` ne porte plus, à elle seule, l'effet de régime (cf. `vacances.md` §10).

**§3 et §9 — forme.** Remplacer les occurrences « (régime) Vacances » désignant l'effet de régime par « absence effective Vacances (`vacances_actives = on`) ». Le terme générique « contexte Vacances » est conservé là où il désigne la phase, non la garde.

### B.5 Justification normative
La réécriture partielle a déjà transformé l'axe blocages en **registres** (D1/D2). Le présent changement ne touche **que** la garde de l'effet conditionnel Vacances (§4.2). **À préserver strictement :** §4.1 (sécurités, dominance d'ordre), **§4.3 (règle POÊLE par corroboration, D-POELE-1)**, §9 ligne poêle, et **INV-TBL-1 / INV-TBL-2 / INV-TBL-3** (gardes `comfort`, ordre poêle/Vacances indifférent, corroboration). Aucune interaction avec l'effectivité ; aucune nouvelle contradiction introduite.

---

## C. `30_decision_centrale.md`

### C.1 Sections à modifier
§4 Niveau 2 (contextes majeurs) ; §10 (table des raisons — description du label `mode_maison_vacances`). §3a est **conservée** (voir justification).

### C.2 / C.3 / C.4 — Texte cible

**§4 — Niveau 2.**
- Actuel : « Aération … fenêtres ouvertes (avec délai), **mode maison = Vacances**, poêle actif. » et « **mode maison = Vacances → `reduced`**, sauf exception … pré-confort … → `comfort` ».
- **[REMPLACEMENT]** cible :
> ### Niveau 2 — Contextes majeurs
>
> Aération en cours confirmée, blocage aération, fenêtres ouvertes (avec délai), **absence effective Vacances (`binary_sensor.vacances_actives = on`)**, poêle actif.
>
> Effets :
> - aération confirmée / blocage aération / fenêtres ouvertes / poêle actif → `reduced`
> - **absence effective Vacances (`vacances_actives = on`)** → `reduced`, **sauf exception normative explicite** : pré-confort retour vacances actif (`input_boolean.pre_confort_actif_calcule`) → `comfort`
>
> La Décision Centrale est l'**unique arbitre** du contexte Vacances : elle consomme l'effectivité `binary_sensor.vacances_actives` et non la projection `input_select.mode_maison`. Aucune autre couche (capteur d'autorisation thermique, diagnostic) ne porte de logique Vacances.

**§10 — table des raisons (description, token inchangé).**
- Actuel : « Mode vacances + pré-confort actif → `pre_confort_vacances` » ; « Mode vacances (sans pré-confort) → `mode_maison_vacances` ».
- **[REMPLACEMENT]** des seules **descriptions** (les tokens `pre_confort_vacances` et `mode_maison_vacances` restent **inchangés** — ce sont des clés techniques de raison) :
> | Absence effective Vacances + pré-confort actif | `pre_confort_vacances` |
> | Absence effective Vacances (sans pré-confort) | `mode_maison_vacances` |
- **[AJOUT]** d'une note sous la table :
> Le token `mode_maison_vacances` est conservé tel quel comme **clé technique de raison** (stabilité runtime, miroir diagnostic, assertions CI). Sa **sémantique** est désormais « absence effective Vacances sans pré-confort ». Un renommage éventuel relève d'un sous-arbitrage distinct (plan v2 §6.3) à fort rayon de propagation (runtime `reason`, `diagnostic/raison.yaml`, CI) — **non retenu ici**.

### C.5 Justification normative
§4 est l'implémentation doctrinale de la table 80 ; il doit suivre le même réalignement. **§3a (délégation présence → `autorisation_cible`) est conservée à l'identique** : la structure de délégation ne change pas ; seule la logique interne de `autorisation_cible` maigrit (cf. §E). Le maintien du token `mode_maison_vacances` préserve **R-ISO-1** (isomorphisme `desired_mode` ↔ `reason`, qui ignore les émissions), **R-MIRROR-1** (miroir `raison.yaml`) et les assertions positionnelles de `test_lot_2_1` (qui n'inspectent pas le label). Aucune contradiction nouvelle.

---

## D. `30_decision_centrale__amendement.md`  *(C1)*

### D.1 Sections à modifier
§8 (impact attendu — bullet `desired_mode`), et **ajout** d'une section d'articulation. R-30.6, §6, INV-30-5 sont **conservés** (déjà bornés au refactor CH-2) ; seule leur **portée** est explicitée.

### D.2 / D.3 / D.4 — Texte cible

**Constat préalable (à rappeler dans l'amendement).** R-30.6 (« le refactor cible (désintrication de `standby_force`…) ne doit pas modifier l'effet thermique »), §6 (« de modifier l'effet thermique (`desired_mode`) à l'occasion du **refactor de causalité** ») et INV-30-5 (« le `desired_mode` est invariant **par le refactor de désintrication** ») sont **déjà bornés** à CH-2. **Aucune suppression** n'est requise. Seule la formulation §8 sur-porte.

**§8 — bullet `desired_mode`.**
- Actuel : « **`desired_mode`** : inchangé dans tous les contextes (R-30.6). »
- **[REMPLACEMENT]** cible (bornage explicite) :
> - **`desired_mode`** : inchangé dans tous les contextes **par le seul refactor de désintrication CH-2** (R-30.6). Cette invariance est relative à CH-2 ; elle n'interdit pas une évolution thermique ultérieure décidée par un chantier métier distinct et explicitement documenté (cf. §10).

**[AJOUT] — nouvelle section d'articulation (numéro `§10` proposé — *à ratifier*).**
> ## 10. Articulation avec le chantier « Vacances sur l'effectivité » (VAC-IMP-1)
>
> Le chantier VAC-IMP-1 fait consommer au régime d'absence chauffage l'effectivité `binary_sensor.vacances_actives` au lieu de la projection `input_select.mode_maison`. Il s'agit d'un **changement de `desired_mode` intentionnel, postérieur et distinct** du refactor de désintrication CH-2.
>
> - R-30.6 / §6 / INV-30-5 conservent toute leur valeur **pour le périmètre CH-2** : la désintrication n'a pas modifié `desired_mode`.
> - VAC-IMP-1 modifie délibérément `desired_mode` dans le seul contexte « projection Vacances ∧ présence réelle » (correction de S-CHAUFFAGE-PRESENCE), conformément à `vacances.md` §10. Ce changement est hors du champ d'invariance de CH-2 et n'en constitue pas une violation.
> - **Invariant structurel maintenu (permanent, indépendant de CH-2) :** l'isomorphisme des gardes de tête entre les axes `desired_mode` et `reason` de la Décision Centrale (R-ISO-1 / INV-30-5 au sens « équivalence de squelette ») reste **obligatoire** après VAC-IMP-1. Le changement de garde Vacances doit donc être appliqué **identiquement** aux deux axes.
> - **Garde de re-vérification (R-30.7) applicable :** avant tout patch runtime, le graphe de dépendances de `decision_centrale.yaml` est re-vérifié sur le runtime courant.

**[AJOUT optionnel — invariant exposé CI, identifiant *à ratifier*].** Si un invariant CI dédié est souhaité pour figer la distinction de périmètre :
> - **INV-30-7 *(proposé, à ratifier)*** — L'invariance de `desired_mode` portée par R-30.6 est **relative au refactor de désintrication CH-2** ; elle n'est pas opposable à un changement thermique d'un chantier métier documenté (ex. VAC-IMP-1). L'isomorphisme `desired_mode` ↔ `reason` (R-ISO-1) demeure, lui, inconditionnel.

### D.5 Justification normative
Lève le risque d'auto-contradiction du corpus **sans toucher aux garanties de CH-2**. La distinction « invariance relative à un refactor » vs « invariance structurelle permanente (isomorphisme) » est rendue explicite, ce qui **renforce** R-ISO-1 / R-MIRROR-1 au lieu de les affaiblir. R-30.1→R-30.5, R-30.7, INV-30-1/2/3/4/6 et §6 (interdictions non thermiques) demeurent **inchangés**.

---

## E. `15_capteurs/01_capteurs_decision.md`  *(option B)*

### E.1 Sections à modifier
Définition `sensor.chauffage_autorisation_cible` : 🎯 Rôle, 🔗 Dépendances → Contextes.

### E.2 / E.3 / E.4 — Texte cible

**🎯 Rôle.**
- Actuel : « Il répond exclusivement à : fait-il froid dehors, fait-il froid dedans, **et dans quel mode est la maison** — sans tenir compte des mécanismes de blocage ou d'exécution. »
- **[SUPPRESSION]** de « et dans quel mode est la maison ».
- **[REMPLACEMENT]** cible :
> Il répond exclusivement à : fait-il froid dehors, fait-il froid dedans — sans tenir compte du contexte Vacances, des mécanismes de blocage ou d'exécution. Le contexte Vacances est arbitré exclusivement en amont par la Décision Centrale (cf. `30` §4) ; ce capteur **ne le connaît pas**.

**🔗 Dépendances → Contextes.**
- Actuel : la liste « Contextes » comprend « `input_boolean.blocage_chauffage_poele` ⚠️ dette … » **et** « `input_select.mode_maison` ».
- **[SUPPRESSION]** de la ligne « `input_select.mode_maison` ».
- **[AJOUT]** d'une note doctrinale :
> Le retrait de `input_select.mode_maison` applique au contexte Vacances la même réduction de dette de couche que celle déjà documentée pour `input_boolean.blocage_chauffage_poele` (« dépendance à migrer vers la décision centrale ») : ce capteur ne porte que le thermique pur.

### E.5 Justification normative
Réalise l'**option B** : `autorisation_cible` redevient un capteur d'**intention thermique** pure. La cohérence est forte avec la doctrine **déjà inscrite** dans ce contrat (« Ne doit pas connaître les blocages N1 »). Les consommateurs contractuels (decision_centrale présence, `autorisation.yaml`, triggers, `50_standby_hysteresis`, diagnostics) restent listés à l'identique : le capteur est consommé comme avant, seule sa logique interne maigrit. Bornes de valeurs (`comfort`/`neutre`/`reduced`/`unknown`) et garanties **inchangées**.

---

## F. `15_capteurs/07_capteurs_diagnostics_structurants.md`

> Note de nommage : le fichier réel est `07_capteurs_diagnostics_structurants.md` (le plan/mission cite `07_capteurs_structurants.md`).

### F.1 Sections à modifier
Dépendances de `sensor.chauffage_mode_calcule` et de `sensor.chauffage_raison_calculee`.

### F.2 / F.3 / F.4 — Texte cible

**`mode_calcule` → 🔗 Dépendances → « Contexte utilisateur ».**
- Actuel : « - input_boolean.mode_confort_chauffage / - input_select.mode_maison ».
- **[REMPLACEMENT]** cible :
> Contexte utilisateur :
> - input_boolean.mode_confort_chauffage
>
> Contexte d'effectivité Vacances :
> - binary_sensor.vacances_actives

**`raison_calculee` → 🔗 Dépendances → « Blocages et contextes ».**
- Actuel : la liste comprend « - input_select.mode_maison ».
- **[REMPLACEMENT]** de cette ligne :
> - binary_sensor.vacances_actives

- **[AJOUT]** d'une note (les deux capteurs) :
> La garde Vacances de ces miroirs de diagnostic est alignée sur l'effectivité `binary_sensor.vacances_actives`, en stricte cohérence avec la Décision Centrale (`30` §4). `input_select.mode_maison` est retiré des dépendances **de la garde Vacances** ; il n'est pas réintroduit par une autre voie dans ces capteurs.

### F.5 Justification normative
Maintient la propriété de **miroir fidèle** : les diagnostics doivent dériver de la **même** hiérarchie que la décision (INV-30-6 ; R-MIRROR-1 pour `raison_calculee`). Recâbler la garde Vacances sur `vacances_actives` est la condition contractuelle de l'alignement runtime ultérieur. La nature « jamais consommé par une automation » et la dépendance à `sensor.chauffage_autorisation_cible` (délégation présence) sont **conservées**. *(La mention `binary_sensor.pre_confort_actif` de la liste actuelle de `raison_calculee` est un écart de nommage préexistant, hors périmètre VAC-IMP-1 — non traité ici.)*

---

## G. `20_triggers_decisionnels.md`

### G.1 Sections à modifier
Table « Niveau 1 — contextes contraignants / blocages majeurs » (lignes `mode_maison`) ; ajout d'une ligne `vacances_actives` ; note de redondance `mode_maison`.

### G.2 / G.3 / G.4 — Texte cible

**[AJOUT] d'une ligne de trigger d'effectivité** (table régime/contexte) :
> | binary_sensor.vacances_actives | OFF → ON | OUI | CRITIQUE | Entrée absence effective Vacances — (re)calcul du régime |
> | binary_sensor.vacances_actives | ON → OFF | OUI | CRITIQUE | Sortie absence effective Vacances — revalidation du régime |

**[REMPLACEMENT] des justifications des lignes `mode_maison`** (lignes « Entrée contexte majeur Vacances » / « Sortie contexte Vacances / revalidation régime ») :
> | mode_maison | autre → Vacances | OUI | CRITIQUE | Reconfiguration de l'espace d'autorisation (projection) — l'effet de **régime** est porté par `vacances_actives` |
> | mode_maison | Vacances → autre | OUI | MAJEUR | Reconfiguration de l'espace d'autorisation (projection) — l'effet de **régime** est porté par `vacances_actives` |

**[CONSERVATION + précision] de la note de redondance `mode_maison`** :
> - la présence de `mode_maison` dans cette table reste **volontaire** : il agit comme **signal de reconfiguration de l'espace d'autorisation** (projection), non comme garde de régime ;
> - depuis VAC-IMP-1, l'**effet de régime** d'absence Vacances est porté exclusivement par `binary_sensor.vacances_actives` ;
> - `mode_maison` est conservé comme déclencheur défensif ; son retrait éventuel relève d'un arbitrage distinct.

### G.5 Justification normative
Rend le recalcul du régime **déterministe** sur l'effectivité (transition `vacances_actives → off` chez des occupants présents). Le maintien de `mode_maison` comme trigger « reconfiguration d'autorisation » évite toute régression de réveil et reste justifié indépendamment du régime. **Couplage impératif :** voir §H (INV-TRIG-5) et la note runtime finale.

---

## H. `20_triggers_decisionnels__amendement.md`

### H.1 Sections à modifier
§6 (Faits opposables — liste des « Triggers réels »).

### H.2 / H.3 / H.4 — Texte cible

**§6 — liste opposable.**
- Actuel : « **Triggers réels (15 entités) :** … `presence_famille_unifiee`, `chauffage_inhibition_geofencing`, `chauffage_autorisation_cible`, `boiler_bridge_online`, `chauffage_application_en_cours`, `systeme_stable` (+ timer …, + reload …). »
- **[REMPLACEMENT]** cible (passage à 16 entités, **conditionné à l'ajout du trigger runtime en Étape C**) :
> **Triggers réels (16 entités) :** `chauffage_autorise_systeme`, `mode_confort_chauffage`, `pre_confort_actif_calcule`, `mode_maison`, **`vacances_actives`**, `aeration_episode_en_cours`, `aeration_confirmee`, `chauffage_blocage_aeration`, `fenetre_ouverte_maison_avec_delai`, `blocage_chauffage_poele`, `presence_famille_unifiee`, `chauffage_inhibition_geofencing`, `chauffage_autorisation_cible`, `boiler_bridge_online`, `chauffage_application_en_cours`, `systeme_stable` (+ timer anti-rebond géoloc, + reload script).

- **[AJOUT]** d'une note de couplage :
> L'inscription de `binary_sensor.vacances_actives` dans cette liste opposable **n'est valide qu'une fois le trigger runtime correspondant ajouté** à `11_automations/chauffage/decision_centrale_trigger.yaml` (Étape C). Tant que le runtime n'est pas patché, la ligne `vacances_actives` de `20` constituerait une **ligne fantôme** au regard d'**INV-TRIG-5** : la mise en cohérence contrat ↔ runtime doit être simultanée côté chantier.

### H.5 Justification normative
**INV-TRIG-5** impose que toute ligne de la table des triggers corresponde à une entité-source runtime réelle. L'amendement matérialise ce couplage. **À préserver :** INV-TRIG-1 (`standby_force` jamais trigger), INV-TRIG-2/3/4/6, et les absences confirmées (lignes fantômes `protection_*` / `attente_*` / `raison_calculee`) **inchangées**.

---

## I. `65_pre_confort_retour_vacances.md`

### I.1 Sections à modifier
**Aucune modification substantielle.** Clarification définitionnelle optionnelle uniquement.

### I.2 / I.3 / I.4 — Texte cible

Le contrat est **déjà conforme** : §5 conditionne l'activation « au sens strict : `binary_sensor.vacances_actives = on` », et §7 définit le « cycle Vacances » comme une occurrence continue de `binary_sensor.vacances_actives = on`. Les mentions « régime Vacances » (§ délais, § effets autorisés/interdits) désignent déjà ce contexte effectif.

**[AJOUT optionnel — note de cohérence en tête de §5]**, si l'on souhaite verrouiller le vocabulaire :
> Dans ce contrat, « régime Vacances » désigne **systématiquement** l'absence effective Vacances (`binary_sensor.vacances_actives = on`), conformément à `vacances.md` §10 et à la table 80 §4.2. La projection `input_select.mode_maison` n'y intervient jamais comme garde.

### I.5 Justification normative
Aucune contradiction à lever : le gardiennage strict sur `vacances_actives = on` y est **antérieur** au chantier. La note proposée est purement préventive (lisibilité) et n'altère ni les conditions d'activation, ni l'anti-rebond, ni la portée. **À préserver :** intégralité du mécanisme pré-confort (activation unique par cycle, fenêtre bornée, subordination à l'override).

---

## Récapitulatif — invariants explicitement préservés

| Invariant / clause | Statut |
|--------------------|--------|
| Tables présence / absence / inhibition (80 §5/§6/§7) | inchangées |
| Règle POÊLE par corroboration (80-réécriture §4.1/§4.3/§9 ; INV-TBL-1/2/3 ; D-POELE-1) | inchangée |
| Override opérateur `mode_confort_chauffage` (Niveau 0) | inchangé |
| Gardiennage pré-confort sur `vacances_actives = on` (65) | inchangé (déjà conforme) |
| R-30.1→R-30.5, R-30.7, INV-30-1/2/3/4/6 | inchangés |
| R-ISO-1 (isomorphisme `desired_mode` ↔ `reason`) | **renforcé** (rendu explicite, §D) |
| R-MIRROR-1 (miroir `raison.yaml`) | condition d'alignement diagnostic (§C/§F) |
| INV-TRIG-1/2/3/4/6 | inchangés |
| Token de raison `mode_maison_vacances` (clé technique) | **non renommé** |
| `66_adaptation_consigne_vacances.md` ; `vacances.md` §10 | inchangés (références) |
| Fixture gelée `d2` | hors périmètre contractuel, intouchée |

## Couplages à honorer lors de la phase runtime (rappel, non contractuel)
- **§H ↔ Étape C :** ligne trigger `vacances_actives` (contrat 20/amendement) ↔ trigger runtime réel (INV-TRIG-5).
- **§C/§D ↔ Étape C+D :** garde Vacances mutée **identiquement** dans `desired_mode` + `reason` de `decision_centrale` **et** dans `diagnostic/raison.yaml` (R-ISO-1 + R-MIRROR-1), patch **atomique**.
- **§D ↔ Étape C :** le scoping de R-30.6/§8 précède le changement de `desired_mode`.

## Décisions ouvertes signalées (à ratifier avant patch documentaire)
1. Numérotation de la section ajoutée à `30__amendement` (proposée `§10`) et de l'invariant éventuel (proposé `INV-30-7`) — **identifiants à ratifier**, non imposés.
2. Maintien (recommandé) ou retrait du trigger `input_select.mode_maison` (§G).
3. Renommage éventuel du token `mode_maison_vacances` — **non retenu** par défaut (rayon de propagation runtime/CI).
4. Notes optionnelles de §B (vacances.md), §I (65) — à inclure ou non.

---

*Proposition de rédaction en lecture seule — aucun fichier du dépôt modifié ni créé. Prête à relecture avant génération des patchs documentaires. Ne contient ni YAML, ni patch runtime, ni changement CI.*
