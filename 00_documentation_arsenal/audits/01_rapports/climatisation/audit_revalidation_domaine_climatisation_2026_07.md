# AUDIT DE REVALIDATION — DOMAINE CLIMATISATION (2026-07)

> Audit **statique, lecture seule** — aucun runtime modifié.
> Mandat : ré-vérifier sur pièces l'état réel du domaine climatisation après la
> vague de corrections v15.8.x → v16.x, en confrontant chaque statut **revendiqué**
> (backlog, registre, contrats, hub) au **code réel du dépôt**.
> Référentiel amont : [`audit_climatisation_arsenal.md`](audit_climatisation_arsenal.md)
> (audit initial, dettes D1–D13) et
> [`../../04_chantiers/climatisation/backlog_climatisation_hysteresis.md`](../../04_chantiers/climatisation/backlog_climatisation_hysteresis.md)
> (état revendiqué au 2026-07-03).
> Le runtime fait foi ; chaque verdict est adossé à des chemins de fichiers précis.

## Note de périmètre et de méthode

Ré-audit **de conformité d'état**, pas un ré-audit architectural complet : la
cartographie du domaine (perception → besoins → admissibilité → décision →
exécution → sécurité → observabilité) reste celle de l'audit initial, non
contredite par la présente lecture. Ont été relus et confrontés :

- les artefacts runtime porteurs des dettes D1–D13 (`12_template_sensors/climatisation/`,
  `11_automations/climatisation/`, `10_scripts/climatisation/`,
  `19_button_card_templates/40_dashboards/climatisation/`,
  `18_lovelace/dashboards/climatisation/`, `03_input_numbers/climatisation/`) ;
- les trois checkers CI du domaine (`scripts/arsenal_contracts/check_climatisation_*.py`),
  **exécutés localement** lors de cet audit ;
- la chaîne documentaire : contrat (`contrats/climatisation/`), backlog, registre
  des chantiers, hub de domaine, index des audits.

Non ré-audités : les pipelines amont transverses (présence, aération, chauffage,
fenêtres), le sous-domaine déshumidificateur (H1 — domaine distinct, clos au
registre), et les items transverses H2/H3a/H3b (VMC/aération — hors périmètre
climatisation strict, portés par le backlog commun).

---

# 1. VERDICTS — DETTES DÉCLARÉES RÉSOLUES

Chaque dette retirée du backlog a été re-vérifiée dans le runtime actuel.

| Dette | Verdict | Preuve runtime |
|---|---|---|
| D1 — raison masquant des causes réelles | **RÉSOLU — CONFIRMÉ** | `12_template_sensors/climatisation/decision/raison.yaml` : la cascade lit désormais `binary_sensor.clim_blocage_aeration_etage_reel` (l. 75), `binary_sensor.clim_extinction_absence_prolongee_autorisee` (l. 85) et ajoute `exterieur_trop_froid` (l. 87) ; blocages HEAT-only gardés par `heat_contexte` (l. 66–71) |
| D2 — fenêtres brutes vs temporisées | **RÉSOLU — CONFIRMÉ** | même fichier, l. 77 : la raison lit `fenetre_ouverte_maison_avec_delai`, alignée sur `autorisation/*.yaml` |
| D3 — voyant `clim_bloquee` mensonger | **RÉSOLU — CONFIRMÉ** | `12_template_sensors/climatisation/blocages/diagnotic.yaml` : composition figée sur 5 sources structurelles (poêle, post-aération, horaire `_reel`, aération étage `_reel`, fenêtres `_avec_delai`) ; le faux positif `fenetre_ouverte_etage` a disparu |
| D4 — `correction.yaml` en course avec le Guard | **RÉSOLU — CONFIRMÉ** | `11_automations/climatisation/cool/maj_consignes/` ne contient plus que `absence.yaml` et `presence.yaml` ; l'automation hors chaîne a été supprimée |
| D6 — logique métier dans l'UI | **RÉSOLU — CONFIRMÉ** | `19_button_card_templates/40_dashboards/climatisation/40_contraintes/clim_blocages_synthese_xl.yaml` : l'état actif est lu depuis les capteurs backend `_reel` (l. 71–73), `new Date()` ne sert plus qu'au formatage informatif ; `carte_clim_decision` délègue la cohérence à `clim_incoherence_decision_reel` (vérifié par le test CI `test_ui_carte_clim_decision_delegue_coherence`) |
| D7 — `clim_action_en_cours` « bloquée » à tort | **RÉSOLU — CONFIRMÉ** | `12_template_sensors/climatisation/decision/action_en_cours.yaml` : priorité à l'état HVAC réel (`climate.clim`), `bloquee` seulement si le poêle bloque clim à l'arrêt |
| D8 — extinction COOL au mauvais sens | **RÉSOLU — CONFIRMÉ** | `12_template_sensors/climatisation/seuils_on_off/cool/seuil_extinction_cool_atteint.yaml` : `temp_min <= seuil_off` (l. 37) ; sens gelé par `scripts/arsenal_contracts/check_climatisation_seuils_cool_contracts.py` |
| D9 — consigne COOL non appliquée à l'entrée | **RÉSOLU — CONFIRMÉ** | `11_automations/climatisation/cool/application_consigne.yaml` (automation `10030000000119`) : application à l'entrée en COOL, au changement de consigne attendue et au boot — symétrique de `heat/application_consigne.yaml` |
| D13 — CI partielle (reliquat F2/F3) | **RÉSOLU — CONFIRMÉ** | `scripts/arsenal_contracts/check_climatisation_admissibilite_contracts.py` : tests `test_clim_bloquee_survol_fige` (F2) et `test_clim_action_en_cours_survol_fige` (F3) présents ; les 3 checkers du domaine (`admissibilite`, `seuils_cool`, `ventilation`) **passent localement** (exécutés pendant cet audit, exit 0) ; workflows `.github/workflows/contracts_climatisation_admissibilite.yml`, `contracts_climatisation_seuils.yml`, `clim_ventilation_contracts.yml` |

**Aucune résolution revendiquée n'est infirmée.** Le domaine est passé de 1 à 3
workflows CI contractuels depuis l'audit initial.

---

# 2. VERDICTS — DETTES DÉCLARÉES OUVERTES

| Dette | Verdict | Preuve runtime |
|---|---|---|
| D5 — pas de notification d'échec persistant | **OUVERT — CONFIRMÉ, aggravé d'une occurrence réelle** | `11_automations/climatisation/notifications.yaml` ne notifie que le mode actif ; `10_scripts/climatisation/execution_mode_cible.yaml` latche `input_boolean.clim_execution_echec` + incrémente `counter.clim_execution_retry_count` **sans aucune notification** ; aucun consommateur de `clim_execution_echec` n'émet de notification (`rearmement_apres_recuperation.yaml`, `reprise_apres_echec.yaml`). L'occurrence réelle du 2026-07-03 ([`diagnostic_clim_execution_echec.md`](diagnostic_clim_execution_echec.md) : booléen latché non remarqué) matérialise exactement le risque décrit — voir recommandation R1 |
| D10 — duplication humidex DRY | **OUVERT — CONFIRMÉ** | `12_template_sensors/climatisation/seuils_on_off/dry/on.yaml` produit toujours `binary_sensor.clim_humidex_sup_cible_dry`, consommé uniquement par la tuile Dry de `18_lovelace/dashboards/climatisation/diagnostic.yaml` (l. 66) ; le seuil réel de la décision reste `seuil_allumage_dry_atteint.yaml` ; toujours pas de `dry/off.yaml` |
| D11 — sémantique `chauffage_clim_active_en_hiver` | **OUVERT — CONFIRMÉ** (P3, laisser tel quel) | `11_automations/climatisation/modes.yaml` : calcul toujours fondé sur le seul `input_select.mode_maison`, aucune logique saisonnière |
| D12 — divers maintenabilité | **OUVERT — CONFIRMÉ** | doc fantôme `sensor.clim_etat_reel` toujours présente (`19_button_card_templates/40_dashboards/climatisation/30_diagnostic/carte_clim_decision.yaml`, l. 51) ; `clim_offset_off` toujours `min: -3.0` (`03_input_numbers/climatisation/modes/heat/seuils/offsets.yaml`, l. 47) ; IDs d'automation toujours hétérogènes (13/14 chiffres) |
| Contrat 05 — « aucun deadlock thermique » | **OUVERT — CONFIRMÉ** (P3 doc) | `contrats/climatisation/05_decision_candidats.md`, § Garanties : l'énoncé est présent ; le réalignement trivial noté au backlog reste à faire |
| D-tuile — polarité `clim_synthese_status_72` | **PÉRIMÉ AU BACKLOG — probablement résorbé** | voir constat N1 |

---

# 3. CONSTATS NOUVEAUX (chaîne documentaire)

### N1 — L'entrée backlog « D-tuile » est périmée : la tuile a été refondue

**Gravité : Faible (hygiène de backlog)**

**Constat.** Le backlog décrit D-tuile comme « défaut de modèle du template
partagé […] `clim_maintien_cool` est une entité fantôme », en attente d'observation.
Or `clim_maintien_cool` n'apparaît **plus nulle part** dans le dépôt (recherche
globale négative), et
`19_button_card_templates/40_dashboards/climatisation/20_statut_metier/clim_synthese_status_72.yaml`
a été refondu : lecture pure des capteurs de seuil réels
(`clim_seuil_allumage_*`/`clim_seuil_extinction_*`, passés en variables par
`18_lovelace/dashboards/climatisation/diagnostic.yaml`, l. 43–66), palette
sémantique neutre (seuil franchi = information bleue, pas un état favorable),
sans vocabulaire d'action réelle. Le défaut de polarité décrit ne correspond plus
au code.

**Impact.** Le backlog — document de travail « ne liste que les dettes encore
ouvertes » — porte un item dont l'objet a disparu.

**Recommandation.** Requalifier ou clôturer D-tuile au backlog après confirmation
par le propriétaire (l'observation runtime post-déploiement que le backlog
attendait semble avoir été dépassée par la refonte).

### N2 — Le registre des chantiers liste encore D13 comme ouvert

**Gravité : Faible (cohérence d'index)**

**Constat.** `audits/REGISTRE_CHANTIERS.md` § ④ (ligne « Climatisation /
hystérésis ») énumère « H2, H3a/H3b, D5, D13, D-tuile, D10 » alors que le backlog
source marque D13 **traité le 2026-07-03** (gardes F2/F3, vérifiées en § 1).
Le registre prime comme cockpit ; sa ligne est en retard d'un événement sur sa
propre source faisant foi.

**Traitement.** Corrigé dans le cadre du présent audit (mise à jour d'index,
aucun contenu normatif touché).

### N3 — Deux rapports d'audit absents du hub de domaine

**Gravité : Faible (navigation, anti-orphelin)**

**Constat.** [`diagnostic_clim_execution_echec.md`](diagnostic_clim_execution_echec.md)
et [`investigation_temporisation_allumage_hvac.md`](investigation_temporisation_allumage_hvac.md)
(tous deux du 2026-07-03) sont indexés dans `audits/index.md` mais **absents** de
la section « Audits & état » du hub
`navigation/domaines/climatisation.md`, qui se veut le point d'entrée du domaine.

**Traitement.** Corrigé dans le cadre du présent audit (hub complété).

### N4 — Statut de contrat périmé : « aligné runtime Arsenal v15.x »

**Gravité : Moyenne (gouvernance documentaire)**

**Constat.** `contrats/climatisation/README.md` affiche « Version contrat : v1.4 —
Statut : Stable — aligné runtime Arsenal v15.x », repris par le hub. Or :

- le runtime du dépôt est en **v16.3.2** (`changelog/changelogs/v16/`) ;
- le chantier **C8 mode nuit** est livré en **v16.1.0** et intégré au contrat
  (`06_doctrine_blocages.md` §9, statut « implémenté au runtime en v16.1.0,
  validation terrain 2026-06-29 ») avec de nouvelles entités
  (`input_boolean.clim_mode_nuit_actif`, `binary_sensor.clim_mode_nuit_effectif` —
  `05_input_booleans/climatisation/modes/mode_nuit.yaml`,
  `12_template_sensors/climatisation/blocages/mode_nuit_effectif.yaml`) ;
- la famille s'est étendue de trois contrats ventilation (`12_ventilation_intention.md`,
  `13_intensite_besoin_froid.md`, `14_recommandation_ventilation.md`) désormais
  gelés par `clim_ventilation_contracts.yml`.

Le contenu du contrat est à jour ; c'est la **ligne de statut** (et son écho dans
le hub) qui ne l'est plus.

**Recommandation.** Arbitrage propriétaire : bumper la ligne de statut du README
contrat (par ex. « aligné runtime v16.x ») et répercuter au hub. Non appliqué ici —
toucher la version d'un contrat excède une mise à jour d'index.

### N5 — La carte « blocages synthèse » sur-affirme encore en cas nominal

**Gravité : Faible (explicabilité résiduelle)**

**Constat.** `clim_blocages_synthese_xl.yaml` couvre désormais fidèlement ses
**trois** blocages annoncés (horaire, aération étage, post-aération), mais son
libellé nominal reste absolu : « Aucun blocage en cours — Le système est
pleinement autorisé à agir » (l. 101–103). Or `binary_sensor.clim_bloquee`
(`blocages/diagnotic.yaml`) compose **cinq** sources : la carte peut afficher ce
message pendant qu'un blocage fenêtres (`fenetre_ouverte_maison_avec_delai`) ou
poêle est actif. L'en-tête du template documente honnêtement le périmètre réduit ;
c'est le libellé qui généralise.

**Recommandation.** Reformuler le libellé nominal en périmètre borné (par ex.
« Aucun blocage horaire / aération en cours ») **ou** aligner la carte sur les 5
sources de `clim_bloquee`. Candidat P3 au backlog — aucune correction appliquée ici.

---

# 4. ÉVALUATION GLOBALE

**Le domaine est-il conforme à ses propres revendications ?** *Oui, à une entrée
de backlog et deux lignes d'index près.* Les 9 résolutions revendiquées (D1, D2,
D3, D4, D6, D7, D8, D9, D13) sont toutes **confirmées dans le runtime**, et les
plus fragiles sont gelées en CI (F2/F3, sens d'extinction COOL, délégation de
cohérence UI). Les dettes déclarées ouvertes le sont réellement. Aucun écart
inverse (résolution revendiquée non effective) n'a été trouvé.

**Le domaine est-il explicable ?** *Oui, désormais.* La conclusion la plus sévère
de l'audit initial (« non explicable via les dashboards ») est **levée** : raison,
voyant et survol dérivent des mêmes signaux que les autorisations. Reliquat unique
et mineur : le libellé nominal de la carte blocages synthèse (N5).

**Le domaine est-il gouverné ?** *Oui, avec un retard d'écriture.* 3 workflows CI
contractuels (contre 1 à l'audit initial), contrats étendus (ventilation, mode
nuit) et validés terrain (C4, C8). Les frictions restantes sont exclusivement
documentaires : backlog D-tuile périmé (N1), registre en retard sur D13 (N2), hub
incomplet (N3), statut de contrat daté (N4).

**Risque opérationnel dominant.** **D5** reste la seule dette à conséquence
opérationnelle démontrée : l'échec d'exécution du 2026-07-03 est resté silencieux,
exactement comme l'audit initial le prédisait. Sa probabilité n'est plus
théorique.

---

# 5. RECOMMANDATIONS & ARBITRAGES OUVERTS (sans correction runtime)

- **R1 — Reprioriser D5** (propriétaire) : l'occurrence réelle du 2026-07-03
  justifie de promouvoir D5 du statut « P2 dormant au backlog » vers un chantier
  ordonnancé (notification persistante sur `input_boolean.clim_execution_echec`,
  pattern `retry_transactionnel` ECS/chauffage) — ou d'acter par écrit que le
  silence est assumé et de corriger le contrat `08_execution.md` en conséquence.
- **R2 — Requalifier D-tuile au backlog** (N1) : constat d'objet disparu ;
  clôture ou requalification à confirmer par le propriétaire.
- **R3 — Bumper le statut du contrat** (N4) : ligne « aligné runtime v15.x » à
  actualiser (README contrat + écho hub). Arbitrage propriétaire.
- **R4 — Libellé de la carte blocages synthèse** (N5) : périmètre borné ou
  alignement 5 sources ; candidat P3.
- Reliquats P3 inchangés (D10, D11, D12, contrat 05, DRY deadband) : la
  disposition « laisser tel quel / opportuniste » du backlog reste pertinente.

---

*Fin de l'audit. Lecture seule : aucun runtime, aucun contrat, aucun checker
modifié. Seules mises à jour associées (navigation/index) : hub de domaine
complété (N3), registre des chantiers réconcilié avec le backlog (N2), indexation
du présent rapport.*
