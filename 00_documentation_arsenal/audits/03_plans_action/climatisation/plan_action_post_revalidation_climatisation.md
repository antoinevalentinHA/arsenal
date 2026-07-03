# PLAN D'ACTION — CLIMATISATION POST-REVALIDATION (2026-07)

> **Document de cadrage — aucune correction implémentée ici.**
> Traduit en lots actionnables les recommandations R1–R4 de
> [`audit_revalidation_domaine_climatisation_2026_07.md`](../../01_rapports/climatisation/audit_revalidation_domaine_climatisation_2026_07.md),
> à la lumière de l'audit initial
> ([`audit_climatisation_arsenal.md`](../../01_rapports/climatisation/audit_climatisation_arsenal.md))
> et du backlog
> ([`backlog_climatisation_hysteresis.md`](../../04_chantiers/climatisation/backlog_climatisation_hysteresis.md)).
> **Aucun runtime, YAML, checker ou workflow n'est modifié par ce plan.**

## Arbitrages propriétaire intégrés (2026-07-03)

| # | Arbitrage | Traduction dans ce plan |
|---|---|---|
| 1 | **D5** repromu en chantier **P1** | Lot A (chantier **C13** au registre) |
| 2 | **D-tuile** : clôturer/requalifier comme résorbée, sauf preuve contraire | Clôture confirmée — aucune preuve contraire trouvée (§5.1) ; réalignement backlog au Lot C |
| 3 | **Statut contrat v15.x** : correction opportuniste au prochain lot documentaire | Lot C |
| 4 | **Carte blocages synthèse** : requalifiée **dette d'explicabilité contextualisée** (métier/UX), pas cosmétique | Lot B, précédé de la recommandation d'architecture (§4) |

Ces arbitrages ne sont pas rediscutés ici. Aucune contradiction factuelle majeure
n'a été découverte lors de la relecture du dépôt ; au contraire, la doctrine des
blocages appuie l'arbitrage 4 (voir §4.1).

---

## 1. Classification des dettes issues de la revalidation

| Dette | Nature | Devenir |
|---|---|---|
| D5 — échec d'exécution silencieux (occurrence réelle 2026-07-03, [`diagnostic_clim_execution_echec.md`](../../01_rapports/climatisation/diagnostic_clim_execution_echec.md)) | **Opérationnelle** | **Lot A — chantier P1 (C13)** |
| N5 requalifiée — blocages affichés hors contexte de mode (carte synthèse + voyant) | **Explicabilité contextualisée** (observabilité + UX/Lovelace) | **Lot B — P2**, architecture d'abord (§4) |
| N4 — statut contrat « aligné runtime v15.x » périmé | **Documentaire** | **Lot C — opportuniste** |
| Contrat 05 « aucun deadlock thermique » — réalignement trivial | **Documentaire** | **Lot C** |
| Backlog — traces à réaligner (D-tuile clos, D5 promu, D13 déjà ✅) | **Documentaire** (hygiène de backlog) | **Lot C** |
| D-tuile — entrée périmée (objet disparu) | **À clôturer** | §5.1 (constat), écriture au Lot C |
| D10 — duplication humidex DRY | **Maintenabilité** | **Reporté** (§5.2) |
| D11 — sémantique `chauffage_clim_active_en_hiver` | **Maintenabilité** | **Reporté** |
| D12 — IDs hétérogènes, `clim_offset_off` min −3, doc fantôme `clim_etat_reel` | **Maintenabilité** | **Reporté** (doc fantôme absorbable par Lot B, cf. §5.2) |
| DRY — bande morte −1 codée en dur | **Maintenabilité** | **Reporté** |
| H2, H3a, H3b — VMC / aération | **Transverse hors domaine clim** | **Reporté** (backlog commun, inchangé) |

---

## 2. Lot A — Chantier C13 : notification d'échec d'exécution persistant (D5)

- **Objectif.** Matérialiser la promesse du contrat
  [`08_execution.md`](../../../contrats/climatisation/08_execution.md) (« échec
  persistant ⇒ notification persistante ») : lorsqu'un échec d'exécution latche
  `input_boolean.clim_execution_echec`, émettre une notification persistante ;
  la retirer au réarmement. L'échec du 2026-07-03 est resté invisible — c'est la
  seule dette du domaine à conséquence opérationnelle démontrée.
- **Dette.** Opérationnelle.
- **Priorité proposée.** **P1** (arbitrage propriétaire 1).
- **Fichiers probablement concernés.**
  - `10_scripts/climatisation/execution_mode_cible.yaml` (branche d'échec final —
    latch du booléen, point d'émission naturel) *ou* automation dédiée nouvelle
    dans `11_automations/climatisation/` déclenchée sur `clim_execution_echec`
    (préférable : garde le script d'exécution pur, pattern « projection UI
    observable » de `notifications.yaml`) ;
  - `11_automations/climatisation/rearmement_apres_recuperation.yaml` (point de
    dismiss naturel, ou couvert par la même automation dédiée) ;
  - `00_documentation_arsenal/contrats/climatisation/08_execution.md`
    (réalignement du § Résilience sur le mécanisme retenu) ;
  - `scripts/arsenal_contracts/check_climatisation_admissibilite_contracts.py`
    (nouvelle garde de non-régression, voir Validations).
- **Dépendances.** Aucune (indépendant des Lots B/C). Décision de conception
  unique : émission dans le script vs automation dédiée sur le booléen —
  l'automation dédiée est recommandée (booléen = source de vérité unique,
  notification reconstructible depuis l'état courant, symétrie création/dismiss,
  conforme au pattern existant de `notifications.yaml`).
- **Bénéfice attendu.** Visibilité immédiate des pannes d'exécution ; supprime la
  classe d'incident « clim ne démarre pas depuis N jours sans que personne ne le
  sache » ; solde la dernière divergence clim vs pattern maison
  (`retry_transactionnel` ECS/chauffage).
- **Risque de régression.** Faible : couche notification pure, aucune décision,
  aucune action matérielle. Seul point d'attention : ne pas doublonner avec la
  notification de mode (`notification_id` distinct de `clim_mode_actif`).
- **Effort.** Faible (une automation + un § de contrat + une garde CI).
- **Critères de fin.**
  1. `clim_execution_echec` → `on` produit une notification persistante ;
  2. réarmement (`rearmement_apres_recuperation.yaml`) → dismiss ;
  3. contrat 08 aligné sur le mécanisme réel (plus de sur-promesse) ;
  4. garde CI verte + détection prouvée par mutation-testing (méthode F2/F3) ;
  5. backlog mis à jour (D5 retiré des dettes ouvertes) et registre C13 clos —
     co-commit (règle 1 du registre).
- **Validations / checkers.** Extension de
  `check_climatisation_admissibilite_contracts.py` (présence de l'automation,
  trigger sur `clim_execution_echec`, `persistent_notification.create`/`dismiss`,
  `notification_id` dédié) via le workflow existant
  `.github/workflows/contracts_climatisation_admissibilite.yml` ; `docs_lint`.

---

## 3. Lot B — Explicabilité contextualisée des blocages (N5 requalifiée)

- **Objectif.** Que la couche d'observabilité des blocages ne présente jamais
  comme « bloquant » un verrou qui ne s'applique pas au contexte de mode
  courant (ex. : post-aération HEAT affichée en rouge pendant un COOL autorisé
  et actif), tout en préservant la visibilité complète des verrous actifs.
- **Dette.** Explicabilité contextualisée (observabilité backend + UX/Lovelace).
- **Priorité proposée.** **P2** — première dette d'explicabilité du domaine
  depuis la levée de D1–D3 ; non promue en chantier actif (décision d'agir non
  prise, contrairement à D5).
- **Fichiers probablement concernés.**
  - `12_template_sensors/climatisation/blocages/diagnotic.yaml`
    (`binary_sensor.clim_bloquee`) et/ou **nouveau** capteur de pertinence dans
    `12_template_sensors/climatisation/blocages/` ;
  - `19_button_card_templates/40_dashboards/climatisation/40_contraintes/clim_blocages_synthese_xl.yaml` ;
  - `19_button_card_templates/40_dashboards/climatisation/30_diagnostic/carte_clim_decision.yaml`
    (consommateur UI unique de `clim_bloquee` — nuance orange l. 104–108) ;
  - `00_documentation_arsenal/contrats/climatisation/06_doctrine_blocages.md`
    (§4, §5, §8) et `10_observabilite.md` ;
  - `scripts/arsenal_contracts/check_climatisation_admissibilite_contracts.py`
    (**F2 à faire évoluer en co-commit** — la composition de `clim_bloquee` est
    gelée en CI depuis le 2026-07-03).
- **Dépendances.** Arbitrage d'architecture préalable (§4) ; à séquencer
  **après** le Lot A (indépendants fonctionnellement, mais le même checker est
  touché — éviter deux évolutions CI concurrentes) ; le Lot C peut consigner la
  décision d'architecture au contrat dans la même vague documentaire.
- **Bénéfice attendu.** Répond à la question contractuelle « pourquoi la clim
  agit / n'agit pas » **dans le bon contexte** ; supprime le dernier cas où l'UI
  contredit la décision ; résorbe au passage N5 (couverture 3/5) et le résidu
  documenté de la dette #1 du contrat 06 §8 (absence prolongée non agrégée au
  voyant).
- **Risque de régression.** Moyen : triple co-évolution capteur + carte +
  checker (F2) + contrat dans le même commit ; purement observabilité (aucune
  décision touchée), mais un gel CI existant doit être révisé sans perdre sa
  valeur de non-régression.
- **Effort.** Moyen.
- **Critères de fin.**
  1. Aucun artefact d'observabilité n'affiche un blocage non applicable au
     contexte courant comme empêchant l'action ;
  2. les verrous actifs non pertinents restent **visibles** (section
     informative), jamais silencieux ;
  3. la narration blocages est cohérente avec `sensor.clim_raison_decision`
     (mêmes signaux, même contextualisation) ;
  4. invariant §5 du contrat 06 précisé et vérifié ;
  5. gels CI mis à jour + mutation-testing ; 6. backlog/registre réalignés.
- **Validations / checkers.** Évolution F2 + nouvelle garde « pertinence »
  (composition du capteur contextualisé + consommation par la carte, pattern
  F5/F6) dans `check_climatisation_admissibilite_contracts.py` ; `docs_lint`.

---

## 4. Recommandation d'architecture — blocages contextualisés (préalable au Lot B)

### 4.1 Fondement : la matrice d'applicabilité existe déjà et la doctrine est en tension avec le runtime

La colonne « Modes impactés » du contrat
[`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) §4,
confirmée par la lecture des trois autorisations
(`12_template_sensors/climatisation/autorisation/{cool,dry,heat}.yaml`) :

| Verrou (vérité consommée) | COOL | DRY | HEAT | Portée |
|---|---|---|---|---|
| `binary_sensor.clim_blocage_horaire_reel` | ✕ | ✕ | ✕ | **Globale** (neutralisée à la source par le mode nuit, §9) |
| `binary_sensor.fenetre_ouverte_maison_avec_delai` | ✕ | ✕ | ✕ | **Globale** |
| `binary_sensor.clim_blocage_aeration_etage_reel` | ✕ | ✕ | — | Contextuelle COOL·DRY |
| `binary_sensor.clim_extinction_absence_prolongee_autorisee` | ✕ | — | — | Contextuelle COOL |
| `input_boolean.blocage_clim_poele` | — | — | ✕ | Contextuelle HEAT |
| `input_boolean.chauffage_blocage_aeration` (post-aération) | — | — | ✕ | Contextuelle HEAT |

Or les deux artefacts d'inventaire agrègent **sans contexte** :
`binary_sensor.clim_bloquee` (`blocages/diagnotic.yaml`) passe à `on` sur poêle ou
post-aération pendant un COOL autorisé ; la carte
`clim_blocages_synthese_xl` affiche « Blocage(s) actif(s) » en rouge dans le même
cas. L'invariant §5 du contrat 06 — « `clim_bloquee == on` ⟺ au moins un blocage
**réellement effectif sur la chaîne de décision** » — n'est donc pas honoré à la
lettre : un verrou HEAT actif pendant que la décision sert COOL n'est pas
« effectif sur la chaîne de décision » courante. L'arbitrage propriétaire 4
(dette métier, pas libellé) est ainsi corroboré par la doctrine elle-même.

Le pattern de contextualisation existe déjà au runtime, éprouvé et gelé en CI :
`heat_contexte` de `12_template_sensors/climatisation/decision/raison.yaml`
(l. 66 : `target == 'heat' or (not cool_adm and not dry_adm)`), vérifié par
`test_raison_decision_blocages_contextualises_heat` du checker admissibilité.
**La cible est d'étendre cette contextualisation, pas d'en inventer une.**

### 4.2 Modèle cible : deux vérités distinctes, toutes deux exposées

1. **Inventaire** — « quels verrous sont actifs ? » : liste factuelle,
   non contextualisée, exhaustive (les 6 lignes de la matrice). C'est ce que
   `clim_bloquee` fait aujourd'hui (5/6 — l'absence prolongée manque, résidu
   documenté de la dette #1 du contrat 06 §8).
2. **Pertinence** — « un verrou actif empêche-t-il quelque chose que le système
   chercherait à faire dans le contexte courant ? » : inventaire **croisé** à la
   matrice d'applicabilité et au contexte (`sensor.clim_target_mode`, besoins et
   admissibles), même famille de règles que `heat_contexte`.

Un blocage actif **non pertinent** n'est jamais masqué : il change de registre
d'affichage (information neutre), pas de visibilité.

### 4.3 Déclinaison recommandée

- **Backend d'abord** (doctrine « aucune logique métier dans l'UI », déjà
  restaurée par D6) : créer un capteur de pertinence
  (ex. `binary_sensor.clim_blocage_pertinent_actif`, avec attributs listant
  séparément les verrous actifs pertinents et les verrous actifs hors contexte)
  dans `12_template_sensors/climatisation/blocages/`. Aucune décision ne le
  consomme (étage 3, contrat 06 §2).
- **Carte `clim_blocages_synthese_xl` en consommatrice pure**, restructurée en
  deux sections :
  - **« Blocages actifs pertinents »** — seuls déclencheurs du fond rouge ;
    libellé nominal borné (plus de « pleinement autorisé à agir ») ;
  - **« Autres contraintes observées »** — verrous actifs hors contexte de mode
    (ex. « poêle actif — n'affecte que le soutien HEAT »), fond neutre.
  La carte passe au passage de 3 à 6 verrous couverts (résorbe N5).
- **`clim_bloquee` conservé tel quel** (option additive, recommandée) : il reste
  l'inventaire de survol, sa composition gelée F2 est **intacte** ; la variante
  qui requalifierait `clim_bloquee` lui-même en pertinence est écartée en
  première intention (elle casse F2, le vocabulaire du contrat 06 §5 et la
  nuance orange de `carte_clim_decision` pour un bénéfice égal). Deux retouches
  périphériques restent à arbitrer au moment du chantier :
  - préciser l'invariant §5 du contrat 06 (« effectif » = inventaire ;
    « pertinent » = nouvelle vérité contextuelle) et lever le résidu absence
    prolongée (dette #1 §8) en l'ajoutant à l'inventaire — **cette** extension
    de composition, elle, exige l'évolution F2 en co-commit ;
  - décider si la nuance orange de `carte_clim_decision` (l. 104–108) bascule
    sur la pertinence — son garde-fou actuel (`action == 'bloquee' | 'arret'`)
    limite déjà le faux contexte pendant un mode actif, la bascule est donc un
    raffinement, pas un correctif.
- **Cohérences imposées** (critères de fin du Lot B) : mêmes vérités que les
  autorisations (`_reel`, `_avec_delai`, flags manuels — jamais de condition
  brute, contrat 06 §5) ; même contextualisation que `raison.yaml` (la carte ne
  doit jamais raconter autre chose que la raison) ; aucun cas particulier mode
  nuit (déjà neutralisé à la source dans `clim_blocage_horaire_reel`, contrat 06
  §9) ; `clim_action_en_cours` (F3) inchangé.

### 4.4 Ce que cette architecture évite

- **Masquer** un verrou actif (perte d'observabilité) — écarté par la section 2.
- **Recalculer** la pertinence en JS dans la carte (retour de D6) — écarté par
  le capteur backend.
- **Casser le gel F2** sans nécessité (régression de gouvernance) — écarté par
  l'option additive.
- **Un correctif de libellé seul** — écarté par l'arbitrage 4 : sans vérité de
  pertinence backend, tout libellé reste faux dans un contexte ou l'autre.

---

## 5. Items à clôturer et items reportés

### 5.1 À clôturer — D-tuile (arbitrage 2)

Vérification « preuve contraire » refaite sur le dépôt courant : l'entité
`clim_maintien_cool` n'apparaît **nulle part** (recherche globale négative) ;
`19_button_card_templates/40_dashboards/climatisation/20_statut_metier/clim_synthese_status_72.yaml`
est une lecture pure des capteurs de seuil réels passés en variables par
`18_lovelace/dashboards/climatisation/diagnostic.yaml` (l. 43–66), à palette
sémantique neutre. **Aucune preuve contraire → clôture confirmée** comme dette
résorbée. L'écriture (retrait de l'entrée au backlog, trace « clos ») relève du
Lot C. Seule trace résiduelle admise : la dette technique de factorisation JS
notée dans l'en-tête du template lui-même (l. 49–50) — hors périmètre, non
bloquante.

### 5.2 Reportés (aucun lot ouvert — disposition backlog inchangée)

- **D10** (duplication humidex DRY, capteur quasi-orphelin consommé par la seule
  tuile Dry de `diagnostic.yaml` l. 66), **D11** (nommage
  `chauffage_clim_active_en_hiver`), **D12** (IDs, `clim_offset_off` min −3.0,
  doc fantôme `clim_etat_reel` — cette dernière dans
  `carte_clim_decision.yaml` l. 51, fichier touché par le Lot B : correction
  opportuniste possible à ce moment-là), **DRY bande morte −1** : P2/P3
  maintenabilité, « laisser tel quel / opportuniste » reste la bonne disposition.
- **H2, H3a, H3b** : items VMC/aération du backlog commun, hors domaine
  climatisation strict — non traités par ce plan, pré-vérifications du backlog
  (`tentative_en_grace`, `vmc_duree_min_haute`) toujours valables.

---

## 6. Séquencement et gouvernance

1. **Lot A (C13, P1)** — immédiat, indépendant, risque faible.
2. **Lot C (P3, opportuniste)** — à la prochaine vague documentaire ; peut
   embarquer la consignation de l'architecture §4 au contrat 06 si le Lot B est
   validé entre-temps.
3. **Lot B (P2)** — après Lot A (même checker touché) et après validation de la
   recommandation §4 par le propriétaire.

Chaque lot suit la règle de co-commit du registre
([`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md), règle 1) : état du
registre, backlog et changelog mis à jour dans le commit qui livre.

### Lot C — Réalignement documentaire opportuniste (détail)

- **Objectif.** Solder les écarts documentaires N4 + contrat 05 + hygiène backlog.
- **Dette.** Documentaire. **Priorité.** P3, opportuniste (arbitrage 3).
- **Fichiers concernés.**
  `00_documentation_arsenal/contrats/climatisation/README.md` (statut
  « v15.x » → réalité v16.x) ; écho hub
  `00_documentation_arsenal/navigation/domaines/climatisation.md` (Orientation) ;
  `00_documentation_arsenal/contrats/climatisation/05_decision_candidats.md`
  (§ Garanties, réalignement trivial noté au backlog) ;
  `00_documentation_arsenal/audits/04_chantiers/climatisation/backlog_climatisation_hysteresis.md`
  (clôture D-tuile, promotion D5→C13, retrait de la ligne D13 déjà ✅).
- **Dépendances.** Aucune. **Bénéfice.** Statuts fiables pour le prochain
  auditeur. **Risque.** Nul (documentation pure). **Effort.** Trivial→faible.
- **Critères de fin.** Plus aucun statut revendiqué contredit par le dépôt ;
  `docs_lint` vert ; hub/registre/backlog racontent la même histoire.
- **Validations.** `scripts/docs_lint/docs_lint.py`,
  `scripts/arsenal_contracts/check_registre_chantiers.py`.

---

*Fin du plan. Lecture seule sur le runtime : aucun YAML Home Assistant, checker
ou workflow modifié. Écritures associées à ce plan : le présent document, son
indexation (`audits/index.md`, hub de domaine) et l'enregistrement de C13 au
registre des chantiers (promotion arbitrée de D5).*
