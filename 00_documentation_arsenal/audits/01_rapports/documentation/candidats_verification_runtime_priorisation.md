# Candidats à vérification runtime — priorisation

> **Cadre.** Lecture seule. Pas d'audit du dépôt, pas de correction, pas de patch. Objectif : identifier les **prochains documents** normatifs/structurants susceptibles d'avoir divergé du runtime, sur le modèle de Bouclage, et les **prioriser**.
>
> **Méthode (triage mécanique, généralisation de la méthode Bouclage).** Pour chaque document de `contrats/` et `architecture/` (≥ 3 entités citées), extraction des entités Home Assistant référencées, puis test de présence de chaque `object_id` dans le **runtime réel** (1 553 YAML hors documentation). Un fort taux d'entités absentes = présomption de dérive. Vérification rapide « rename vs absent vs placeholder » sur les têtes de liste. **Ce sont des présomptions à confirmer**, pas des verdicts : le scan est par sous-chaîne (faux positifs possibles : placeholders, systèmes externes, gabarits `<zone>`).

---

## Exclusions (écartées d'emblée)

- `contrats/bouclage.md` et `contrats/ecs/04_bouclage_ecs_sous_systeme.md` — **déjà arbitrés et patchés** (tour précédent).
- `contrats/parametres_invalides.md` — entités manquantes = `input_datetime.yyy`, `…zzz`, `input_number.yyy` : **placeholders volontaires** (contrat *sur* les paramètres invalides). **Faux positif, pas une dérive.**

---

## Liste priorisée

| Pri. | Chemin | Manq./Tot. | Raison du soupçon (vérif. rapide) | Confiance | Nature probable |
|:--:|---|:--:|---|:--:|---|
| **P1** | `contrats/bluetti.md` | 21/37 | Intégration Bluetti **présente** au runtime, mais **21 entités citées sur 37 absentes** : le contrat décrit un parc d'entités qui ne correspond plus à ce qui existe. | **Élevée** | **Structurel** |
| **P1** | `contrats/sante/sommeil.md` | 10/23 | Intégrations `sommeil`/`withings` présentes, mais les entités citées (`*_statistique`, `withings_sleep_*_phase_local`) sont **absentes** ; le runtime expose une autre couche (`sommeil_consolidation_nuit_evenementielle`, …). Refonte non répercutée. | **Élevée** | **Structurel** |
| **P2** | `contrats/meteo/axe_humidite_relative_jardin.md` | 3/3 | **100 % des sources citées absentes** : `sensor.humidite_jardin_1/2/3` introuvables ; le runtime n'a que des sensors dérivés (`humidite_absolue_*_jardin`). Sources brutes renommées/supprimées. *(Doc sœur `axe_temperature_jardin.md` se déclare elle-même en dette d'amont.)* | **Moy.-élevée** | **Structurel / documentaire** |
| **P2** | `contrats/chauffage/15_capteurs/03_capteurs_blocages_niveau1/fenetre_ouverte_maison.md` | 5/12 | Capteurs d'ouverture de chambres cités en `binary_sensor.capteur_chambre_<nom>` **absents** ; les pièces existent au runtime sous un **autre préfixe** (`chambre_arnaud` ≠ `capteur_chambre_arnaud`). Renommage non suivi. | **Moy.-élevée** | **Documentaire (renommage)** |
| **P2** | `contrats/climatisation/06_doctrine_blocages.md` | 4/15 | `clim_blocage_*_reel` / `clim_blocage_*_actif` absents ; domaine **récemment retravaillé** (chantier observabilité COOL livré v15.8.4) → entités probablement renommées par ce chantier. | **Moyenne** | **Structurel (probable)** |
| **P2** | `contrats/climatisation/08_execution.md` | 2/12 | `automation.clim_application_consigne_heat` et `automation.clim_reprise_apres_erreur` **introuvables** (aucun slug proche). Automatisations supprimées/renommées ou jamais créées sous ce nom. | **Moyenne** | **Inconnue (slug ou structurel)** |
| **P3** | `contrats/volets_pluie.md` | 2/18 | Les automatisations **existent** mais avec un **slug réordonné** : doc `meteo_pluie_fermeture_volets_*` vs runtime `fermeture_volets_pluie_*`. Décalage de nommage, logique présente. | **Élevée (c'est cosmétique)** | **Cosmétique** |
| **P3** | `contrats/alarme/70_sirene_actions_terminales.md` | 1/7 | `switch.sirene_alarm` absent, mais le périphérique sirène **existe** (`sirene_bip`, `sirene_brutale`, …). Très probable renommage de l'actionneur. | **Moyenne** | **Cosmétique / documentaire** |
| **P3** | `contrats/arsenal_nas.md` | 2/6 | `automation.arsenal_nas_release_diff_notification` et `binary_sensor.arsenal_nas_any_job_stale` absents ; mais `arsenal_nas` décrit un **système externe** (NAS) dont une partie vit hors de ce dépôt. Frontière à qualifier avant conclusion. | **Faible** | **Inconnue (système externe)** |

*Mentions résiduelles, non prioritaires* : `architecture/bouclage.md` (1/8) appartient au **cluster Bouclage déjà traité** ; `architecture/integrite_parametres.md` (1/8) et quelques contrats à 1 entité manquante relèvent du **cosmétique isolé** — bruit de fond, à ignorer pour l'instant.

---

## Lecture rapide

- **Deux candidats P1 nets** (`bluetti`, `sommeil`) : intégration bien présente mais **gros écart d'entités** → ce sont les meilleurs équivalents de Bouclage pour une vérification runtime ciblée, probablement **structurels** (parc d'entités refondu).
- **Bloc P2 climatisation/chauffage/météo** : dérives liées à des **renommages** ou à des **chantiers récents** non répercutés dans la doc — confirmation runtime rapide recommandée, nature mixte (documentaire à structurel).
- **Bloc P3** : surtout du **cosmétique** (slugs d'automatisations, nom d'actionneur) ou de la **frontière externe** (`arsenal_nas`) — faible enjeu, à traiter au fil de l'eau.

**Prochaine vérification runtime ciblée suggérée** (même protocole que Bouclage, à ta main) : commencer par **`bluetti.md`** puis **`sommeil.md`** (P1), où le décalage est le plus massif et le plus susceptible d'être structurel.

---

*Fin de la priorisation. Aucun fichier modifié. Aucune correction ni patch proposé : uniquement une liste de candidats à confirmer.*
