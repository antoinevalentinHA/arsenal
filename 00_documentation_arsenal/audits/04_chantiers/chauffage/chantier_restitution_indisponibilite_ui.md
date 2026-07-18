# 🧯 Chantier C26 — Restitution UI de l'indisponibilité (Chauffage)

> **Document de cadrage — ouverture de chantier.** Périmètre **strictement UI**.
> **Aucun** changement fonctionnel, runtime, contrat, CI, entité, socle ou logique métier.
> **Autorité opposable :** exclusivement les documents sous [`00_documentation_arsenal/ui`](../../../ui). Le présent document en dérive et ne s'y substitue pas.

| Champ | Valeur |
|---|---|
| **Domaine** | Chauffage — exposition diagnostique (UI) |
| **Priorité** | P2 |
| **Statut** | Correction UI implémentée sur branche — PR en cours ; validation et clôture non engagées |
| **Base** | `origin/main` @ `29dd98c` |
| **Source faisant foi** | [`audit_exposition_diagnostics_chauffage.md`](../../01_rapports/chauffage/audit_exposition_diagnostics_chauffage.md) — écart **CH-DIAG-08 / F1** |
| **Précédent d'implémentation validé** | **C23** (alarme — restitution `triggered` + priorité d'indisponibilité, patch UI mergé #392). *Précédent utile de mise en œuvre et de validation, **non** autorité normative.* |
| **Référence UI exemplaire** | `19_button_card_templates/40_dashboards/chauffage/30_diagnostic/chauffage_diagnostic_global_compact.yaml` |

---

## 1. Origine de l'écart

L'audit d'exposition diagnostique Chauffage a établi un **unique écart de verdict** (`CH-DIAG-08 / F1`), **strictement UI et sans conséquence fonctionnelle** : sur la **surface principale**, trois cartes décisionnelles restituent l'indisponibilité d'une source **déjà consommée** comme un **état métier valide** :

- `carte_chauffage_intention` — `unavailable` → libellé **brut**, aucun gris d'indisponibilité ;
- `carte_chauffage_synthese` — `unavailable` → **gris neutre `0.2`** (indisponibilité confondue avec le repos nominal) ;
- `carte_chauffage_decision` — `mode_calcule` `unavailable` → fond **rouge** (indisponibilité présentée comme une incohérence décisionnelle).

La **surface diagnostic** (`chauffage_diagnostic_global_compact`) restitue déjà l'indisponibilité correctement (gris indispo prioritaire). L'écart est une **asymétrie de restitution principale ↔ diagnostic**. Conformément au rapport d'audit, **les diagnostics nécessaires aux trois cartes sont déjà produits ; aucune modification de leur production n'est requise dans ce chantier** (ce chantier ne certifie pas le runtime Chauffage dans son ensemble).

## 2. Objectif

Rendre correctement l'**indisponibilité des sources déjà consommées** par les trois cartes, conformément à la charte couleur Arsenal, en **alignant** leur restitution sur la carte exemplaire et le précédent d'implémentation C23. **Les états disponibles restent strictement inchangés.**

## 3. Périmètre exact — trois cartes (les seules)

| Carte | Fichier | Socle |
|---|---|---|
| `carte_chauffage_intention` | `19_button_card_templates/40_dashboards/chauffage/20_statut_metier/carte_chauffage_intention.yaml` | `socle_decision_72` |
| `carte_chauffage_synthese` | `19_button_card_templates/40_dashboards/chauffage/20_statut_metier/carte_chauffage_synthese.yaml` | `socle_status_label_xl` |
| `carte_chauffage_decision` | `19_button_card_templates/40_dashboards/chauffage/30_diagnostic/carte_chauffage_decision.yaml` | `socle_decision_72` + `chauffage_registres_raison` |

Aucun autre fichier UI. Aucun dashboard Lovelace, aucun socle, aucun template sensor.

## 4. Invariants d'innocuité fonctionnelle (absolue)

Le futur patch UI :

- **ne modifie que les trois fichiers de cartes validés** (§3) ;
- **ne modifie aucun** dashboard parent, socle, producteur (template sensor / automation) ni entité ;
- **mêmes entités et mêmes valeurs consommées** ; aucune entité ni source ajoutée ou renommée ;
- **aucune** écriture, aucun `service`/`action`, aucune interactivité ajoutée ; aucun nouveau capteur, helper, seuil ni logique métier — l'UI ne décide rien ([`ui/couleurs/01_principes.md`](../../../ui/couleurs/01_principes.md)) ;
- **ne change aucun rendu lorsque toutes les sources sont disponibles** (aucune re-sémantisation des états valides) ;
- **ne traite aucun autre constat** du rapport ;
- **ne peut avoir aucun effet sur les décisions ou commandes Chauffage** (restitution visuelle seule).

## 5. Doctrine UI applicable (renvois aux documents d'autorité — seule source opposable)

- [`ui/couleurs/05_regles.md`](../../../ui/couleurs/05_regles.md) — **R6** (le gris indisponibilité prime sur toute couleur sémantique) ; table *Traitement des données indisponibles* (`unknown`/`unavailable`/entité absente/valeur non exploitable → `rgba(158,158,158,0.1)`) ; interdit absolu de masquer `unknown`/`unavailable` par une couleur sémantique.
- [`ui/couleurs/02_palette.md`](../../../ui/couleurs/02_palette.md) — gris indispo `0.1` ≠ gris neutre `0.2` (« ne doit jamais être confondu avec un état neutre valide » ; « prime sur toute autre couleur »).
- [`ui/couleurs/03_exceptions.md`](../../../ui/couleurs/03_exceptions.md) — Exception 1 (Modes HVAC) : « le gris indisponibilité prime sur toute couleur de mode ».
- [`ui/couleurs/01_principes.md`](../../../ui/couleurs/01_principes.md) — « le backend décide, l'UI observe ».
- [`ui/socle_ui/03_decision.md`](../../../ui/socle_ui/03_decision.md) / [`07_status.md`](../../../ui/socle_ui/07_status.md) / [`09_diagnostic.md`](../../../ui/socle_ui/09_diagnostic.md) — mapping délégué à la carte métier ; fond dynamique admis en synthèse XL.

**Arbitrage doctrinal (validé) :** la règle d'indisponibilité ([`05_regles`](../../../ui/couleurs/05_regles.md)) prime ici sur la note générique « aucun `background-color` dynamique » des socles `decision`/`etat` — **sans modifier le socle**. Le rendu attendu est **dérivé de la doctrine UI** ; C23 en est un **précédent d'implémentation validé** (mergé, checkers UI verts), non une autorité.

## 6. États à restituer (exigence de résultat)

Pour chaque carte :

- **l'indisponibilité doit être évaluée avant toute restitution sémantique (couleur métier, couleur de mode, calcul de cohérence) susceptible de la masquer** ;
- si une source réellement consommée est `unknown` / `unavailable` / absente / non exploitable (ensemble d'indisponibilité aligné sur la carte exemplaire) → la carte restitue **un état d'indisponibilité** :
  - **fond** : gris indispo `rgba(158,158,158,0.1)` (prioritaire, R6) ;
  - **libellé neutre non métier** et **icône neutre d'indisponibilité** — jamais le jeton brut, jamais un faux état métier. Le **choix exact** du libellé et de l'icône sera **dérivé** de la documentation UI, de la carte exemplaire et de la **cohérence entre les trois cartes**, puis **présenté dans le plan UI avant modification** (le cadrage impose le **résultat sémantique**, pas un texte précis) ;
- sinon → rendu **inchangé** des états disponibles.

Les branches sont **mutuellement exclusives**, l'indisponibilité étant prioritaire (R6).

**Sources déjà consommées, gardées par carte** (identifiées, sans élargissement) :

| Carte | Sources déterminant la restitution |
|---|---|
| `carte_chauffage_intention` | `sensor.chauffage_mode_calcule` |
| `carte_chauffage_synthese` | `sensor.programme_chauffage`, `sensor.chauffage_raison_calculee` |
| `carte_chauffage_decision` | `sensor.programme_chauffage`, `sensor.chauffage_mode_calcule` |

*(La structure de code exacte n'est pas figée ici : elle sera arbitrée à l'audit du diff UI, sous réserve du seul résultat ci-dessus.)*

## 7. Exclusions (garde-fous)

Sont **hors périmètre** et **non touchés** :

- **F2** — branche périmée `chauffage_non_autorise` dans `carte_chauffage_synthese` (laissée **intacte**) ;
- **F3** — reconstruction UI d'un verdict de divergence / réordonnancement de priorité / duplication de seuils ;
- **O-1** — surcouche rouge d'incohérence non exposée ;
- **F4** — cartes secondaires sans garde d'indisponibilité ;
- en-tête `chauffage_etat_reel` (documenté, non défini) de `carte_chauffage_decision` ;
- **tout autre constat** du rapport ;
- aucun nettoyage opportuniste, aucune refonte de dashboard.

## 8. Séquence — validation → consignation → correction → traçabilité

1. **Ouverture documentaire** (le présent chantier + inscription au registre + index) → **PR documentaire draft**, arrêt avant merge.
2. **Correction UI** (seulement après merge de l'ouverture) : traitement de l'indisponibilité sur les **3 cartes**, diff minimal et local, aucun autre changement → **PR UI dédiée**, arrêt avant merge.
3. **Traçabilité** : mise à jour du chantier + registre (co-commit) ; contrôles Lovelace + documentaires ; **pas de changelog** sauf obligation explicite démontrée (précédent C23 ; `redaction_changelog.md` §1).
4. **Validation finale** : revue de clôturabilité en lecture seule, **sans forçage d'aucun état Home Assistant**.

**Chemin documentaire prévisible** (sous réserve de contrôle des conventions du dépôt **juste avant** consignation, non figé ici) :
- dossier de chantier : `00_documentation_arsenal/audits/04_chantiers/chauffage/chantier_restitution_indisponibilite_ui.md` ;
- inscription : `00_documentation_arsenal/audits/REGISTRE_CHANTIERS.md` (① Actifs) ;
- navigation : `00_documentation_arsenal/audits/index.md` (Chantiers › Chauffage).

## 9. Critères de validation et de clôture

**Aucun état Home Assistant n'est forcé** à aucune étape.

- **Preuve statique — obligatoire.** Sur les 3 cartes : sous source indisponible, rendu gris indispo `0.1` + libellé/icône neutres, **jamais** couleur sémantique / rouge / gris neutre ; branches mutuellement exclusives (indisponibilité prioritaire, R6) ; **états disponibles inchangés** (diff limité au traitement de l'indisponibilité) ; checkers UI verts (`contracts_19_button_card_templates`, `contracts_ui_couleurs`, `contracts_ui_runtime_colors`, `contracts_ui_semantic_colors*`).
- **Preuve visuelle — souhaitée si réalisable sans toucher au runtime.** Rendu d'indisponibilité constaté sur **rendu contrôlé ou capture** (gris `0.1` distinct du gris neutre `0.2`), sans provoquer d'indisponibilité réelle.
- **Observation terrain naturelle — différable et non provoquée.** Consignée explicitement comme différée si elle ne survient pas, à l'image de C23.

**Clôturabilité.** La **clôture documentaire** peut être évaluée à partir des **preuves statiques et visuelles disponibles**, l'observation terrain restant **différable** et explicitement consignée. La distinction preuve statique / visuelle / terrain est explicite. *(Le chantier ne subordonne pas sa clôturabilité documentaire à la survenue d'une indisponibilité réelle.)*

### Trace — correction UI implémentée (preuve statique)

Correction UI **implémentée sur branche** (PR en cours ; **validation et clôture non engagées**). Choix retenus, dérivés de la doctrine UI et de la carte exemplaire `chauffage_diagnostic_global_compact` (patron d'implémentation validé C23) :

- **Ensemble d'indisponibilité** (aligné exemplaire) : `['unknown', 'unavailable', undefined, null, 'none', '']` ;
- **Fond** : gris indispo `rgba(158, 158, 158, 0.1)`, **prioritaire (R6)** — jamais rouge, jamais gris neutre `0.2` ;
- **Libellé principal** : `Indisponible` ; **label complémentaire** (quand porté par la carte) : `Données indisponibles` ; **icône** (quand affichée) : `mdi:shield-off`.

Application par carte (garde évaluée **avant** toute restitution sémantique) :

| Carte | Sources gardées | Champs traités |
|---|---|---|
| `carte_chauffage_intention` | `sensor.chauffage_mode_calcule` | `icon` (→ `mdi:shield-off`), `state_display` (→ `Indisponible`), règle couleur `state` en tête (→ gris `0.1`) |
| `carte_chauffage_synthese` | `sensor.programme_chauffage`, `sensor.chauffage_raison_calculee` | `icon`, `state_display`, `label` (→ `Données indisponibles`), règle couleur `state` en tête |
| `carte_chauffage_decision` | `sensor.programme_chauffage`, `sensor.chauffage_mode_calcule` | `variables.diag.indisponible` (avant cohérence → plus de faux rouge), `state_display`, `label`, fond gris `0.1` |

**États disponibles inchangés** (ajout de branches prioritaires uniquement) ; **F2/F3/F4/O-1 intacts** ; le littéral `Inconnu` de `carte_chauffage_decision` (état disponible) reste hors périmètre. Aucun socle, dashboard parent, entité, runtime, contrat, checker, workflow ou changelog touché.

## 10. Identifiant proposé — vérifié

**Identifiant : `C26`.**

Preuve de disponibilité (base `origin/main` @ `29dd98c`, le 2026-07-18) :
- IDs présents dans `REGISTRE_CHANTIERS.md` : **`C1` … `C25`** (contigus, maximum = `C25`) ;
- recherche `\bC26\b` dans **tout** `00_documentation_arsenal/` : **aucune occurrence** ;
- recensement de tous les `C<n>` de l'arborescence `audits/` : **`C1` … `C25`** exclusivement.

⇒ `C26` est le **prochain identifiant réellement libre** (max + 1, sans trou ni réservation antérieure). L'ID n'est pas figé par analogie : il est **attribué après vérification du registre**, et sera **re-confirmé** au moment du co-commit d'ouverture (règle de co-commit `REGISTRE_CHANTIERS.md` §1).

---

*Ouverture documentaire de chantier — cadrage uniquement. Aucun fichier UI, runtime, dashboard, socle, contrat, checker, workflow, registre d'entités ou changelog modifié. Aucune correction UI préparée dans cette PR.*
