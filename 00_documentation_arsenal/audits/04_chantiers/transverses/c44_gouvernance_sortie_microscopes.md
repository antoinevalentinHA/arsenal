# Chantier TRANSVERSE (C44) — Gouvernance de sortie des microscopes Recorder

| Champ | Valeur |
|---|---|
| **Chantier** | Empêcher qu'une observation déclarée temporaire devienne permanente par inertie. Poser une **norme opposable** de sortie des microscopes Recorder, régulariser les 14 blocs existants, et requalifier en observabilité permanente les entités devenues nécessaires à la relecture d'une décision active. |
| **Domaine** | Transverse — gouvernance de l'observabilité. Touche arrosage, climatisation, chauffage, éclairage. |
| **Statut** | **Ouvert (2026-08-31) — lot documentaire D1/D2 livré.** Aucun retrait effectué ; aucune entité ajoutée ni retirée du Recorder. |
| **Priorité** | **P2** — aucun risque fonctionnel ; enjeu de gouvernance et de tenue du contrat Recorder. |
| **Ouvert le** | 2026-08-31. |
| **Prochain jalon** | **2026-10-31** — première échéance opposable (arrosage exploratoire). |
| **Registre** | Chantier **C44** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Mesure amont** | `arsenal-runtime/analyses/recorder_churn_attributs_20260831/` (hors dépôt gouverné) — base `recorder_20260831.db`. |

> **⚠️ Portée du lot livré.** **Documentaire strictement.** Aucune entité ajoutée ou retirée
> de `recorder.yaml` — preuve structurelle au §7. Aucun seuil, aucun trigger, aucun template,
> aucune automatisation. Aucune hystérésis. Aucun checker CI. Aucun changelog (doctrine
> [`redaction_changelog.md`](../../../architecture/03_doctrines/redaction_changelog.md) §1).

---

## 1. Le problème démontré

Au 2026-08-31, `recorder.yaml` portait **14 blocs** de microscope, **50 entités**, pour une ancienneté de **57 à 65 jours**. Aucun n'avait été réexaminé.

**Onze blocs sur quatorze** portaient `Réévaluer : à la clôture du chantier` — sans date, sans seuil de sortie, sans propriétaire. C'est très exactement ce que la doctrine interdit :

> **R-QUALIF-3** ([`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)) — *« Une réserve sans critère de levée (ni date, ni seuil de sortie, ni propriétaire) est **interdite** : elle est perpétuelle par construction. »*

L'échéance était de surcroît **circulaire** : conditionner la sortie d'un microscope à la clôture du chantier que ce microscope alimente garantit qu'elle n'arrive jamais.

### 1.1 Révision assumée du choix de juin 2026

Le gabarit fautif n'était pas une négligence. Il vient de l'Annexe A de [`audit_recorder_instrumentation_temporaire.md`](../../01_rapports/architecture/audit_recorder_instrumentation_temporaire.md), dont le §8-S1 demandait explicitement *« une condition de réévaluation — **pas de date de retrait couperet** »*. Ce choix protégeait une observation utile d'un retrait au milieu d'un chantier actif ; il était défendable.

**L'expérience l'a réfuté** : il n'a pas produit de la souplesse, il a produit une **reconduction tacite**. C44 le révise. L'échéance opposable devient obligatoire, mais elle reste satisfaite par un **événement datable** — ce qui préserve l'intention d'origine sans en conserver l'effet de dérive.

Ce rapport de juin 2026 est un **snapshot daté** (« établi à HEAD `12deca6` ; périssable ») : il n'est pas réécrit. La révision est portée par le contrat Recorder et par le présent document.

### 1.2 Ce que la mesure a corrigé

Le même audit prévoyait en §8-S5 d'« attribuer le poids base, seul moyen de passer de la présomption au verdict sur qui pèse ». C'est fait — et cela renverse une de ses conclusions : `sensor.arrosage_demande_climatique_vpd`, qu'il désignait **« candidat n°1 au retrait post-chantier »**, est devenu une **entrée de décision** de la modulation C11.

---

## 2. La norme — six champs obligatoires

Portée par [`architecture/01_recorder/contrat.md`](../../../architecture/01_recorder/contrat.md) §Instrumentation temporaire de chantier : **Ajouté · Autorité · Preuve attendue · Échéance opposable · Action de sortie · Si échéance dépassée**.

Quatre règles d'application : aucune reconduction tacite · échéance non circulaire · **le coût n'est pas un critère** · **sortir du régime microscope ≠ sortir du Recorder**.

---

## 3. Régularisation des 14 blocs

### 3.1 Dates reconstituées par archéologie Git

Les sept `Ajouté : à confirmer` sont résolus.

| Bloc | Commit | Date | PR |
|---|---|---|---|
| B01 réservoir sol | `737c60a0` | 2026-06-27 | #103 |
| B02 demande climatique | `9fecb78f` | 2026-07-01 | #215 — **les trois entités dans le même commit**, la mention antérieure ne datait que le VPD |
| B03 chaîne décisionnelle V1 | `f54a4b47` | 2026-06-28 | #134 |
| B05 session Lot B | — | 2026-07-05 | #277 |
| B08 intensité besoin froid | `a05c3d22` | 2026-06-23 | — |
| B09 fan_mode recommandé | `c2a18748` | 2026-06-23 | — |
| B11 chauffage P3 | `c86b92f8` | 2026-06-17 | — concorde avec l'incident D-CRIT-1 du 16/06 |

`input_number.arrosage_seuil_humidite_declenchement` fait exception : ajouté le **2026-06-28** par un commit distinct (« graphe humidité du sol au dashboard »), soit un jour après son bloc et **pour un motif UI**, alors que son rôle réel est celui d'un seuil de décision.

### 3.2 Rattachements corrigés

| Mention fautive | Correction |
|---|---|
| **`(C2)`** (B08) | **N'existe pas** au registre. Autorités réelles : contrats climatisation **13** (perception) et **14** §42/§92 (résolution câblée). Mention supprimée, aucun chantier créé. |
| **`Lots C-G`** (B05) | Plan interne à l'audit exécutions longues **§8**, jamais promu : ni ligne de registre, ni chantier. Conditionner une sortie à un travail non ordonnancé est une réserve perpétuelle. **Découplé** : le Lot B est soldé et se suffit. |
| **`contrat 76`** (B11-B14) | Chantier réel = **C5**, [`ch_observabilite_auto_ajustement_courbe.md`](../chauffage/ch_observabilite_auto_ajustement_courbe.md). Pointeur ajouté. |

### 3.3 Justifications factuellement fausses corrigées

- **B09** — « observer ce que ferait une **logique automatique future** […] **aucun pilotage** ». Le contrat 14 v2.0 acte que *« la résolution est désormais câblée »* ; `11_automations/climatisation/ventilation/application_mode.yaml` **se déclenche** sur `sensor.clim_fan_mode_recommande` et **lit** son attribut `mode_technique` pour commander la ventilation. **L'entité pilote.**
- **B08** — « calage des bandes **avant tout câblage** ». Le câblage a eu lieu : contrat 14 §42/§92 fait de `clim_intensite_besoin_froid_niveau` le **moteur** de la recommandation.

### 3.4 Classement après régularisation

| Statut | Blocs / parts | Entités |
|---|---|---|
| **Observabilité permanente** | B02, B03, B04, B08, B09, parts permanentes de B01 · B05 · B06 · B07 | **41** |
| **Microscope borné** | parts temporaires de B01 (3) · B05 (1) · B07 (1), B10, B11-B14 | **9** |

Échéances opposables : **2026-10-31** · **2026-11-16** · **2027-02-07** · **2027-04-30**.

### 3.5 Couplage C43 ↔ `jardin_humidite_sol_mediane`

La justification **A6** de [C43](c43_reduction_churn_recorder.md) — retrait de l'attribut `mediane` de `binary_sensor.arrosage_besoin_sol` — repose explicitement sur le fait que `sensor.jardin_humidite_sol_mediane` **est lui-même historisé**. Retirer cette entité invaliderait rétroactivement ce retrait. Le couplage, absent des deux documents, est désormais inscrit dans `recorder.yaml` et ici.

---

## 4. Plan d'observation hydrique v0 — issue retenue

Confrontation de la checklist §4 au journal T04→T08 :

| Condition §4 | État |
|---|---|
| 1 — plusieurs cycles de tarissement, régimes variés | **acquise** (T08 : 10 phases ≥ 36 h, VPD 1,0→4,0 kPa, r = −0,74) |
| 2 — au moins un épisode chaud | **acquise** (T04 : ET₀ ≈ 6 mm/j) |
| 3 — pluie significative + réponse sol | **non acquise** — la pluie est exclue par construction de toutes les analyses |
| 4 — comportement du Point 2 | **non acquise et non acquérable** — les sondes individuelles sont hors Recorder |
| 5 — fenêtres de fraîcheur | **partielle** — disponibilité du parc établie, durée frais/stale non |
| 6 — corrélation pluie ↔ réaction sol | **non acquise** — même cause que 3 |
| 7 — absence de recommandation runtime en v0 | **acquise**, frontière tenue |

**Issue retenue : le plan v0 est dépassé par C11 P4.** Il visait à décider s'il fallait passer à une recommandation ; la recommandation est livrée et validée §12. Les conditions **3, 4 et 6** sont requalifiées **non bloquantes / sans objet** au titre de `R-VERROU-1`. **Décision explicite : ne pas historiser les six sondes ni ajouter une entrée pluie** dans le seul but de solder une checklist devenue sans objet — ce serait la seule option qui *augmente* le Recorder.

---

## 5. C11 P4 — proposition de clôture avec réserve structurelle

Trois des quatre preuves du contrat 19 §12 sont acquises (réduction réelle, retour à la base, cohérence décision ↔ durée figée).

**La quatrième — motif d'allongement CONSOMMÉ par un Run réel — n'est pas solvable.** Mesure sur `recorder_20260831.db` : `climat_statut = demande_forte` n'apparaît **jamais avant 12 h** (158 occurrences, **0 sur 69 points de décision à 05 h**), tandis que les **16 arrosages réels** se déclenchent tous entre 05:30 et 05:56. Les deux fenêtres ne se recouvrent pas par construction physique — la demande évaporative est diurne, le déclenchement est à l'aube.

**Qualification proposée : NON BLOQUANTE** au titre de `R-VERROU-1` (preuve non productible en observation naturelle, non provoquée). **Clôture de P4 proposée sur cette base.**

> Cette proposition n'est **pas** appliquée : ni la ligne C11 du registre, ni le contrat 19 §12 ne sont modifiés par ce lot. La clôture effective est un acte distinct.

---

## 6. C22 — note factuelle

**Aucune solution runtime n'est proposée ici. C22 relève d'un chantier fonctionnel séparé.**

Faits mesurés sur `recorder_20260831.db`, autorité reconstruite à 50 lx :

- **949 fronts montants** sur 31 jours ; **médiane 29/jour** ;
- **50 %** des fronts montants surviennent à **moins d'une minute** du front descendant précédent, **76 %** à moins de cinq minutes ;
- **109 fronts montants** tombent dans une heure où la lampe consommait — **majorant d'opportunités, en aucun cas des extinctions prouvées** (la résolution énergétique disponible est horaire) ;
- `binary_sensor.sejour_extinction_luminosite_autorisee` est utilisé comme **déclencheur** `trigger: state … to: "on"` dans `11_automations/eclairage/sejour/off_luminosite.yaml`, et non seulement lu en condition ;
- la clause de réexamen du **§2bis** du chantier C22 — *« à ré-examiner seulement si un battement réel est observé au seuil »* — est donc **factuellement déclenchée**.

**À instruire séparément** : hystérésis sur l'autorité, temporisation du trigger, ou combinaison des deux.

**Découplage probatoire, à ne pas confondre.** Le battement de l'autorité et la collecte lux sont couplés **fonctionnellement**, pas **probatoirement** : une hystérésis sur l'autorité ne modifie ni le capteur lux brut ni ses LTS, et ne compromet donc pas l'analyse hivernale hors ligne. Il ne doit **pas** être écrit que le battement « fausse la calibration » — cela demanderait une démonstration qui n'a pas été faite.

---

## 7. Preuve — la liste Recorder est inchangée

Comparaison structurelle avant / après le lot, par chargement YAML de `recorder.yaml` :

```
                        avant                             après
nb_entites              361                               361
nb_uniques              361                               361
sha256 (liste ordonnée) 469eeb7b619905b5…5442ea98eb7      469eeb7b619905b5…5442ea98eb7
auto_purge / purge_keep_days / commit_interval            identiques
```

Le diff de `recorder.yaml` ne contient **aucune ligne non-commentaire** modifiée (vérifié par filtrage du diff unifié).

---

## 8. Ce que ce lot ne fait pas

Aucun retrait R2. Aucun checker CI. Aucune hystérésis. Aucun seuil, trigger, template ou automatisation d'éclairage. Aucune clôture de chantier — ni C11, ni C22, ni C5. Aucun ID attribué hors C44.

## 9. Critères de clôture

1. Les quatre échéances opposables sont tenues ou explicitement réévaluées, sans reconduction tacite.
2. Les lots R2 sont exécutés ou abandonnés par décision motivée.
3. Le checker anti-inertie (lot CI distinct) rend la norme §2 opposable en CI.
4. Aucun bloc de `recorder.yaml` ne porte plus d'échéance non vérifiable.

---

*Chantier ouvert le 2026-08-31. Source faisant foi pour la ligne C44 du registre.*
