# Plan d'action Arsenal — Domaine météo / axe température

> Statut : plan d'action — non normatif tant que non promu en contrat
> Portée : axe température extérieure (jardin / domicile), extérieur imprimerie, prévision
> Origine : audit architectural météo / axe température
> Principe directeur : « le runtime est la référence, le contrat documente le runtime »

---

## Préambule

Plan ordonné du risque minimal vers le risque le plus engageant. Chaque lot porte
une **nature** (contrat / runtime / diagnostic / UI). Le plan ne modifie aucun
contrat, aucun runtime, aucune UI : il décrit des interventions à conduire.

### Correction de cohérence — nommage du contrat de fallback

- Le futur contrat cible s'appellera **`fallback.md`**.
- Tous les renvois documentaires futurs devront pointer vers **`fallback.md`**,
  et **non** vers `contrat_fallback.md`.
- Les renvois existants qui utilisent aujourd'hui le nom logique
  `contrat_fallback.md` devront être repointés vers le fichier réel `fallback.md`
  lors du Lot 1.

---

## Lot 1 — Solder la dette contractuelle fallback & validation

**Nature : contrat (risque runtime nul).**

**Objectif.** Écrire `fallback.md`, qui est référencé par cinq contrats mais
n'existe pas, en se contentant de **formaliser le mécanisme déjà implémenté**
(niveaux 1/2/3, TTL 1800 s, mémoire plausible, garde `systeme_stable`, report
résiduel δ_max). Réconcilier les noms logiques (`contrat_meteo.md`,
`contrat_validation.md`, `contrat_fallback.md`) avec les fichiers réels
(`meteo.md`, `validation.md`, et désormais `fallback.md`). Les renvois pointant
vers `contrat_fallback.md` sont repointés vers `fallback.md`.

**Fichiers probablement concernés.** Création : `00_documentation_arsenal/contrats/meteo/fallback.md`.
Mise à jour des renvois : `meteo/meteo.md`, `meteo/gouvernance.md`,
`meteo/validation.md`, `meteo/axe_temperature.md`, `meteo/axe_temperature_jardin.md`.
Changelog : `00_documentation_arsenal/changelog/`.

**Risques.** Aucun risque runtime. Risque documentaire : écrire un fallback qui
*diverge* du runtime. Mitigation : doctrine « le runtime est la référence, le
contrat documente le runtime » — le contrat décrit `jardin/facade.yaml` et
`temperature_jardin_stabilisation.yaml`, sans rien prescrire de nouveau.

**Validations Home Assistant DevTools.** Aucune (lot documentaire). Vérifier par
relecture croisée que chaque seuil cité (TTL 1800 s, péremption sources 900 s,
plage `[-10;50]`) correspond aux valeurs présentes dans `jardin/facade.yaml` et
`jardin/validation_sources.yaml`.

**Critères de clôture.** `fallback.md` existe ; tous les renvois contractuels
résolvent vers un fichier réel et pointent vers `fallback.md` (jamais
`contrat_fallback.md`) ; aucune entité inventée ; revue de cohérence
runtime ↔ contrat signée.

---

## Lot 2 — Doctrine d'abstention météo unique

**Nature : contrat (risque runtime nul).**

**Objectif.** Inscrire dans le corpus la règle : *la façade abstient (publie
`unknown`), le consommateur teste l'indisponibilité et s'abstient — il ne fabrique
jamais de valeur plausible*. C'est le **prérequis normatif** de la migration
runtime (Lot 5).

**Fichiers probablement concernés.** `meteo/gouvernance.md` (section consommation)
ou nouveau paragraphe transverse ; renvoi depuis les contrats métier
`chauffage/15_capteurs/*`, `climatisation/capteurs/autorisations/10_autorisations.md`,
`aeration_recommandation.md`.

**Risques.** Nul. Risque de sur-prescription : ne pas imposer une seule technique
(sentinelle hors-plage *vs* test explicite) mais une seule **propriété**
(abstention sûre, jamais de valeur plausible injectée). Laisser le choix technique
aux contrats d'axe.

**Validations Home Assistant DevTools.** Aucune.

**Critères de clôture.** Doctrine écrite et opposable ; chaque domaine consommateur
de température extérieure référence cette doctrine ; arbitrage #3 (ci-dessous)
tranché et consigné.

---

## Lot 3 — Clarifier `sensor.temperature_exterieur` (imprimerie)

**Nature : contrat + documentaire (risque runtime nul si on s'en tient à la doc).**

**Objectif.** Lever l'ambiguïté : l'en-tête de `exterieur.yaml` promet une mémoire
(« conserve sa dernière valeur ») que le `state` n'implémente pas (il renvoie
`None`). Décider du statut de cette zone : *observation-only* assumée, ou futur axe
souverain. Le lot **documentaire** corrige le mensonge d'en-tête ; la promotion en
axe souverain est un chantier runtime distinct (hors de ce lot, car plus risqué).

**Fichiers probablement concernés.** Documentaire/décision :
`00_documentation_arsenal/contrats/meteo/` (note de statut de zone). En-tête à
corriger : `12_template_sensors/meteo/mesures/temperature/exterieur.yaml`
(commentaire uniquement, pas la logique). Aucun consommateur de décision n'est
touché : `sensor.temperature_exterieur` n'alimente que dérivés/UI/stats/recorder.

**Risques.** Si la correction se limite au commentaire, risque nul. Toute
réécriture de la logique de fusion (`min` naïve → souveraine) est explicitement
**reportée** car elle changerait `sensor.temperature_exterieur` consommé par
`humidex/base.yaml`, `humidite_absolue/base.yaml`, `point_de_rosee/base.yaml`,
`statistics/meteo/temperature.yaml` et `recorder.yaml`.

**Validations Home Assistant DevTools.** États de `sensor.temperature_exterieur`,
`sensor.temperature_exterieur_1`, `sensor.temperature_exterieur_2` ; vérifier dans
Template que, sources rendues invalides, l'entité passe bien à l'état attendu
(aujourd'hui `None`) — pour documenter le comportement réel, pas le corriger.

**Critères de clôture.** En-tête de `exterieur.yaml` aligné sur le comportement
réel ; statut de zone (observation-only) écrit ou arbitrage #1 ouvert pour
promotion ; aucune entité renommée.

---

## Lot 4 — Exploiter `sensor.temperature_jardin_statut`

**Nature : diagnostic (runtime additif, faible risque).**

**Objectif.** Donner une consommation active au statut souverain aujourd'hui
« mort » côté supervision. Sans toucher aux décisions : ajouter une
**observabilité/notification** sur indisponibilité météo prolongée (`inconnu`), et
idéalement sur `degrade`/`incoherence_retenue` persistants.

**Fichiers probablement concernés.** Probablement une automatisation de
notification dans `11_automations/meteo/` (s'appuyant sur
`sensor.temperature_jardin_statut`, ses attributs `cause` et `age_memoire_s`) ;
éventuellement intégration au système de notifications existant
(`00_documentation_arsenal/contrats/notifications.md`). Aucune création d'entité
de mesure n'est nécessaire : le statut existe déjà.

**Risques.** Additif et non décisionnel → faible. Risque de bruit de notification :
prévoir un délai de grâce (arbitrage #5). Ne pas câbler le statut dans une décision
à ce stade (ce serait l'arbitrage #2, non tranché).

**Validations Home Assistant DevTools.** Forcer `inconnu` en rendant les trois
sources invalides (ou en laissant expirer le TTL) et observer la bascule de
`sensor.temperature_jardin_statut` et de `sensor.temperature_jardin` → `unknown` ;
vérifier `state_attr('sensor.temperature_jardin_statut','cause')` et
`age_memoire_s` ; confirmer le déclenchement de la notification après le délai
retenu.

**Critères de clôture.** Une indisponibilité météo prolongée produit une
trace/notification traçable ; aucun chemin décisionnel modifié ; délai de grâce
documenté.

---

## Lot 5 — Migrer le pattern climatisation `float(0)`

**Nature : runtime (risque modéré — applique la doctrine du Lot 2).**

**Objectif.** Remplacer l'injection d'une valeur plausible (`float(0)`, 0 °C ∈
`[-10;50]`) par une abstention explicite sur indisponibilité de
`sensor.temperature_jardin`. Aligner accessoirement le chauffage (sentinelle
`float(99)` correcte mais implicite) sur la même doctrine.

**Fichiers probablement concernés.** `12_template_sensors/climatisation/autorisation/cool.yaml`,
`12_template_sensors/climatisation/autorisation/heat.yaml`,
`12_template_sensors/climatisation/decision/raison.yaml` ; pour harmonisation :
`12_template_sensors/chauffage/autorisation_cible_selon_temperature.yaml`. Entités
de seuil concernées (inchangées) : `input_number.clim_seuil_temperature_exterieure_minimum`,
`input_number.clim_hiver_seuil_temperature_exterieure`.

**Risques.** **Le plus engageant du plan.** `binary_sensor.autorisation_clim_cool`
et l'autorisation heat pilotent l'éligibilité clim ; une erreur d'abstention
pourrait autoriser ou bloquer à tort. Mitigation : la cible d'abstention doit
rester *fail-safe* (indispo ⇒ autorisation `off`), comportement identique au
fonctionnement actuel mais rendu **explicite et indépendant du sens de
comparaison**. Procéder un fichier à la fois, clim avant harmonisation chauffage.

**Validations Home Assistant DevTools.** Dans Template, simuler
`sensor.temperature_jardin` à `unknown`/`unavailable` et vérifier que
`binary_sensor.autorisation_clim_cool` reste `off` ; idem autorisation heat ;
vérifier qu'avec une valeur réelle plausible (ex. 18 °C) les autorisations
retrouvent leur valeur nominale identique à l'avant-migration ; comparer le
comportement avant/après sur un jeu de valeurs aux bornes des seuils. Surveiller
l'absence de régression sur `decision/raison.yaml`.

**Critères de clôture.** Aucun consommateur extérieur n'utilise plus de valeur
fabriquée plausible ; indisponibilité ⇒ abstention `off` prouvée en DevTools ;
comportement nominal strictement inchangé hors indisponibilité ; doctrine du Lot 2
respectée.

---

## Lot 6 — UI honnête + tests de contrat

**Nature : UI + diagnostic (faible risque).**

**Objectif.** Garantir que les dashboards restituent fidèlement `memoire`/`inconnu`
(conforme à `affichage.md` — UI strictement passive) et ajouter des tests de
contrat sur les modes dégradés de la façade, dans la lignée du pipeline CI existant.

**Fichiers probablement concernés.** UI : `18_lovelace/dashboards/meteo/*`, cartes
diagnostic `19_button_card_templates/40_dashboards/meteo/20_diagnostic_coherence/temperature.yaml`,
`.../climatisation/50_eligibilite/carte_clim_diagnostic_temperature_exterieure*.yaml`.
Tests : `scripts/arsenal_contracts/`, `tools/arsenal_ci/`, registre
`00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml` (pattern de
référence).

**Risques.** UI : nul côté décision. Tests : risque de figer un comportement encore
en arbitrage → n'écrire les tests qu'après clôture des Lots 1, 2 et 5.

**Validations Home Assistant DevTools.** Vérifier qu'aucune carte n'affiche une
valeur quand la façade est `unknown` (elle doit montrer l'indisponibilité/`cause`) ;
exécuter la suite de tests de contrat météo en CI.

**Critères de clôture.** Restitution UI conforme à `affichage.md` ; tests de
contrat couvrant `nominal/memoire/inconnu/degrade` au vert ; documentation et
changelog à jour.

---

## Points nécessitant arbitrage humain

1. **Imprimerie (Lot 3).** `sensor.temperature_exterieur` reste-t-il
   *observation-only* (correction documentaire seule) ou devient-il un axe souverain
   (pipeline + contrat) ? La promotion impacterait `humidex/base.yaml`,
   `humidite_absolue/base.yaml`, `point_de_rosee/base.yaml`, `statistics` et
   `recorder.yaml`.
2. **Statut décisionnel (Lots 4/5).** Une décision doit-elle un jour réagir au
   `statut` (clim refusant d'agir en `degrade`/`incoherence_retenue`) ou la lecture
   valeur-seule reste-t-elle la norme, le statut demeurant purement observationnel ?
3. **Technique d'abstention (Lot 2).** Sentinelle hors-plage unique *ou* test
   d'indisponibilité explicite généralisé : laquelle devient la convention Arsenal ?
4. **Péremption (Lot 1).** La garde 900 s sur les sources brutes monte-t-elle dans
   le contrat de validation, ou reste-t-elle décision d'implémentation locale ?
5. **Délai de grâce notification (Lot 4).** Seuil de durée avant alerte sur
   indisponibilité météo prolongée.

---

## Ordre recommandé

**1 → 2 → 3 → 4 → 5 → 6.**

Les Lots 1–4 sont à risque runtime nul ou additif et peuvent avancer en parallèle
des arbitrages ; le Lot 5 (seul changement décisionnel) ne démarre qu'une fois la
doctrine du Lot 2 figée et l'arbitrage #3 tranché.
