# Dossier de conception — Lot L7
## Observabilité auto-ajustement courbe — Supervision (vue dédiée)

| Champ | Valeur |
|---|---|
| **Type** | Dossier de conception de lot (détaillé) |
| **Lot** | **L7** (phase **P7** du plan d'action) — *uniquement* |
| **Domaine** | Chauffage / Observabilité de l'auto-ajustement courbe |
| **Statut** | Conception de lot — aucune implémentation |
| **Version** | 1.0 |
| **Date** | 2026-07-02 |
| **Amont figé** | `76_…md` (§3 Q1–Q8, §11) ; `plan_action_…md` (P7) ; `dossier_conception_observabilite.md` (§7 critères, §8) ; **audit d'implantation UI** (verdict **B**) ; lots **L1–L6** livrés |
| **Cadre** | Lecture seule. Aucun YAML Lovelace, aucune carte, aucun patch. Décisions de conception uniquement. |

> **Objet :** décider **comment assembler les 8 réponses opposables** (Q1–Q8) en **une vue de supervision lisible**, **où** la poser (verdict d'audit : scénario **B**), et **quelles règles** garantissent lisibilité, non-multiplication d'indicateurs et **supervision ≠ pilotage**. C'est le maillon **présentation** du pipeline (capture → conservation → dérivation → **présentation**) : il ne présente **que** ce qui est déjà dérivé (L1–L6).

---

## 1. Périmètre exact du lot L7

**Inclus (L7) :**
- **Emplacement & navigation** (scénario **B** validé) : un **sous-dashboard dédié** rattaché au hub Diagnostics Chauffage, miroir de vannes/thermiques.
- **Vue de supervision** assemblant les **8 réponses** (Q1–Q8), avec **bandeau complétude**, **lisibilité nominal/anomal**, et **effet borné** (INV-4).
- **Réduction de l'amorce** actuelle du hub (« Auto-ajustement courbe » / « Dernier ajustement ») à un **teaser compact** (statut + complétude + accès).
- **Extension `logbook.yaml`** aux événements courbe (trace lisible d'épisodes / décisions), le cas échéant.

**Explicitement hors L7 (différé) :**
- **Validation de conformité globale `76` §11 + calibration** des paramètres (délai de stabilisation, seuils) → **L8**. Clôture → **L9**.
- Toute **nouvelle grandeur d'observabilité** (L7 **ne dérive rien** : il présente L1–L6). Aucun indicateur hors des 8 questions (INV-7).
- Toute **action / écriture / contrôle** sur la page (INV-1 ; supervision uniquement).

---

## 2. Emplacement & navigation (scénario B — verdict d'audit)

### 2.1 Décision
- **Nouveau sous-dashboard** de clé pressentie **`diagnostics-courbe-dashboard`** (aligné sur `diagnostics-vannes-dashboard` / `diagnostics-thermiques-dashboard`), déclaré dans `dashboards.yaml`.
- **Badge d'accès** ajouté sur le hub `diagnostics-chauffage-dashboard` (3ᵉ badge sous-diagnostic, miroir vannes/thermiques).
- **Badge retour** vers le hub dans le nouveau sous-dashboard.
- **Conformité `R-LL-NAV-1`** : `navigation_path` canonique `/<dashboard-key>` ; **pas de cul-de-sac** ; **retour cohérent** avec le prédécesseur (le hub).

### 2.2 Réduction de l'amorce du hub
- La section « 🔁 Auto-ajustement courbe de chauffe » du hub (aujourd'hui une carte `chauffage_auto_courbe_status_72` « Dernier ajustement ») est **réduite à un teaser compact** : **statut apprenant/gel + complétude + bouton d'accès** au sous-dashboard. Objectif : coup d'œil au hub, **supervision complète sur la page dédiée** ; évite la **double maintenance** et le doublon d'affichage.

### 2.3 Frontière de rôle (opposable en revue)
- La page dédiée est **supervision** : **lecture seule**, aucun toggle/slider/service. Le **pilotage** reste dans `reglages-chauffage-dashboard` ; la **synthèse d'état** reste au hub. Aucun recouvrement fonctionnel.

---

## 3. Assemblage des 8 réponses (Q1–Q8 → grandeurs L1–L6)

Chaque question opposable est **déjà** couverte par une grandeur livrée ; L7 les **présente**, sans en créer.

| Q (76 §3) | Réponse portée par | Origine |
|---|---|---|
| **Q1** Valeurs proposées + erreur source | `sensor.chauffage_pente_suggeree` / `…parallele_suggeree` ; `ecart_consigne_*` ; event `chauffage_courbe_cycle_evalue` (suggérés) | L1 |
| **Q2** Décision par paramètre/sens (appliqué/refusé/abstenu) | event `…cycle_evalue` (`pente_issue`, `parallele_issue`) ; `input_text.chauffage_last_adjustment` ; réversions | L1/L4/L5 |
| **Q3** Pourquoi (raison typée nominal/anomal + contexte) | `cycle_reason` (+ `…_type`) ; `input_text.chauffage_courbe_gel_cause` ; contexte du cycle (représentativité, poêle, mode, auto) | L1/L4 |
| **Q4** Valeur confirmée appliquée + acquittement | `input_number.chauffage_{pente,parallele}_consigne` (intentionnel-confirmé, CR-2) ; `chauffage_last_adjustment` (avant→après, mode) | L1/P3 |
| **Q5** Effet **au niveau fenêtre régime** (tendance, borné) | `sensor.chauffage_courbe_effet_{pente,parallele}` + attributs `niveau/nature/confiance` | L6 |
| **Q6** Dérive / trajectoire | `sensor.chauffage_courbe_derive_{pente,parallele}` ; `counter.chauffage_courbe_reversions` ; historique consignes | L5/P3 |
| **Q7** Complétude + cycles gelés / non apprenants | `sensor.chauffage_courbe_completude` ; `…apprentissage_statut` ; `…gel_cause` ; `…taux_jours_apprenants` ; events `…gel_episode` | L4 |
| **Q8** État nominal installé durablement | `sensor.chauffage_courbe_persistance` `{ras, gel_persistant, refus_recurrent}` ; `counter.chauffage_courbe_refus_consecutifs` | L5 |

> **Liste fermée (INV-7).** Aucun composant de la vue ne se justifie hors de ces 8 questions. Tout indicateur candidat qui ne s'y rattache pas est **rejeté** (anti-multiplication).

---

## 4. Structure de la vue (lisibilité, non-multiplication)

### 4.1 Décision : un **bandeau** + des **sections par question**, du plus « santé » au plus « analyse »
Ordre retenu (haut → bas), pensé **coup d'œil d'abord** :

1. **Bandeau complétude & état (Q7)** — en tête, toujours visible : `completude` (à_jour / **trou_detecte** / inconnu), `statut apprenant/gel` (+ cause si gel), `taux jours apprenants`. C'est le **contrat de confiance** de tout le reste (une trace incomplète relativise les autres réponses).
2. **Proposé & décidé (Q1–Q2–Q3)** — suggéré vs courant + erreur source ; issue par paramètre (appliqué/refusé/abstenu) ; **raison typée nominal/anomal** + contexte d'entrée.
3. **Appliqué & confirmé (Q4)** — consignes confirmées (avant→après, mode) ; statut d'acquittement ; libellé « intentionnel-confirmé » (limite CR-2 consignée).
4. **Trajectoire & oscillation (Q6)** — dérive nette pente/parallèle ; réversions (converge vs oscille).
5. **À surveiller — persistance (Q8)** — drapeau `{ras, gel_persistant, refus_recurrent}`, affiché en **« à surveiller »**, jamais « anomalie » (réserve L5/L6).
6. **Effet borné (Q5)** — effet par régime, **en dernier** (le moins confiant) : état `{amelioration, degradation, indetermine}` **avec ses limites affichées** (`niveau=fenetre_regime`, `nature=correlation`, `confiance`).

### 4.2 Règles de lisibilité
- **Lisibilité nominal/anomal** : distinction visuelle claire (respect des contrats de couleurs UI — `check_ui_couleurs` / `ui_runtime_colors`) ; `anomal` saillant, `nominal` neutre ; **le drapeau de persistance n'est pas rendu comme `anomal`** (« à surveiller »).
- **Effet borné, jamais causal** : l'effet **affiche ses réserves** (fenêtre régime, corrélation, confiance) ; aucune formulation causale « l'ajustement X a amélioré ».
- **Trou ≠ silence** : le bandeau distingue explicitement `trou_detecte` (cycle non évalué) d'un cycle évalué non actionnable.
- **PC/mobile** : sections empilables (vertical-stack / grid 2 colonnes qui retombe à 1 sur mobile), en miroir de `diagnostic_thermique` ; pas de tableau large non responsive.
- **Anti-multiplication (INV-7)** : un composant = une réponse opposable ; pas d'indicateur décoratif.

### 4.3 Patron de réutilisation
- **Miroir ECS** : `includes/cartes/ecs_apprentissage_offsets.yaml` (synthèse lecture seule) et `dashboards/diagnostics/ecs.yaml` (section « Apprentissage des offsets ») servent de **patron de style** — même grammaire visuelle, cohérence transverse.

---

## 5. Logbook (trace lisible d'événements)

- **Décision.** Étendre `logbook.yaml` aux événements **`chauffage_courbe_gel_episode`** (début/fin de gel, corrélés) et, optionnellement, **`chauffage_adjustment`** (applications), pour offrir un **journal humain** des transitions — support de Q2/Q7 hors dashboard.
- **Cadrage.** Trace **event-only**, lecture seule ; aucune duplication d'entité ; aligné sur la façon dont `logbook.yaml` inclut déjà des événements de domaine.

---

## 6. Contraintes d'implémentation (pour le YAML L7, non ouvert ici)

- `R-LL-NAV-1` (navigation), `check_lovelace_includes_contracts` (cibles `!include` existantes), `check_lovelace_section_headers_contracts` (en-têtes de section), `check_ui_couleurs` / `check_ui_runtime_colors` (contrats de couleurs), `check_19_button_card_templates` (si templates button-card réutilisés).
- **Déclaration** obligatoire du nouveau dashboard dans `dashboards.yaml` + **badge retour** (sinon `R-LL-NAV-1` R3 cul-de-sac).
- **Aucune entité nouvelle** : la vue lit L1–L6 ; si un besoin d'affichage exigeait une grandeur absente, ce serait un signal de **retour en conception** (L5/L6), pas un ajout en L7.

---

## 7. Critères de validation du lot L7

| # | Critère | Preuve attendue |
|---|---|---|
| V1 | **Les 8 réponses sont lisibles** | Un humain retrouve Q1–Q8 sur la page, sans hypothèse (test de lecture) |
| V2 | **Bandeau complétude en tête** | `trou_detecte` vs silence légitime **distingué** ; taux apprenants visible |
| V3 | **Effet borné** | Effet affiché en tendance de fenêtre régime, **avec limites** ; aucune formulation causale (INV-4) |
| V4 | **Nominal/anomal lisible** | Distinction visuelle conforme aux contrats couleurs ; persistance rendue « à surveiller », pas « anomal » |
| V5 | **Supervision ≠ pilotage** | **Aucune** action/écriture/toggle sur la page ; pilotage resté dans `reglages-chauffage` (INV-1) |
| V6 | **Navigation conforme** | Dashboard déclaré ; badge d'accès depuis le hub ; badge retour ; `R-LL-NAV-1` vert |
| V7 | **Amorce réduite** | Section hub ramenée à un teaser (statut + complétude + accès) ; pas de double maintenance |
| V8 | **Non-multiplication (INV-7)** | Tout composant se rattache à une des 8 questions ; aucun indicateur orphelin |

La validation **de conformité `76` §11** (les 6 démonstrations) reste **L8** ; L7 fournit la **lisibilité** requise pour la conduire.

---

## 8. Risques de régression

| ID | Risque | Prob. | Impact | Maîtrise |
|---|---|---|---|---|
| RR-1 | Page **illisible** (surcharge d'indicateurs) | Moyenne | Élevé | Liste fermée aux 8 questions (INV-7, V8) ; bandeau + sections ordonnées |
| RR-2 | **Effet sur-interprété** comme causal | Moyenne | Élevé | Limites affichées, formulation corrélation (V3) |
| RR-3 | Persistance rendue comme **anomalie** | Moyenne | Moyen | Rendu « à surveiller » (V4), aligné réserve L5/L6 |
| RR-4 | **Contrôle** glissé sur la page de supervision | Faible | Élevé | Interdiction stricte (V5) ; toggles restés en réglages |
| RR-5 | **Cul-de-sac** de navigation (R-LL-NAV R3) | Faible | Moyen | Badge retour obligatoire (V6) |
| RR-6 | **Double maintenance** hub/page | Moyenne | Faible | Amorce réduite à un teaser (V7) |
| RR-7 | Contrats **couleurs / section headers** non respectés | Moyenne | Faible | Patron ECS + contrats CI (V4, §6) |

---

## 9. Démonstration INV-1, INV-2, INV-4 (au niveau présentation)

- **INV-1 — Read-only.** La vue **n'écrit rien** ; aucun service, toggle ou action. Elle **lit** des grandeurs d'observabilité déjà produites. Le comportement de décision est inchangé.
- **INV-2 — Étanchéité.** La présentation est le **dernier maillon** unidirectionnel ; elle ne réinjecte rien dans la décision. (La garde d'étanchéité — L5, étendue L6 — reste opposable ; la vue ne fait que lire.)
- **INV-4 — Effet au niveau régime.** L'effet est présenté **exclusivement** en tendance de fenêtre régime, **avec limites**, jamais par ajustement isolé.

---

## Rattachement

- **Réalise :** le lot **L7** (phase P7) du plan d'action, au service du contrat `76` (§3 Q1–Q8, §7 lisibilité) — écart **É-10** (dashboard diagnostic) + extension logbook.
- **Diffère explicitement :** L8 (validation `76` §11 + calibration), L9 (clôture).
- **Ne rouvre :** aucun document figé ; ne crée **aucune** grandeur (présente L1–L6) ; place validée par l'audit d'implantation (scénario B).
- **Lecture seule :** aucune entité créée, aucun fichier modifié par ce dossier ; architecture Lovelace vérifiée sur HEAD courant.

*Dossier de conception L7 — 2026-07-02. Supervision (vue dédiée) uniquement. Aucun YAML Lovelace, aucune carte, aucun patch. La conformité `76` §11 et la calibration relèvent de L8.*
