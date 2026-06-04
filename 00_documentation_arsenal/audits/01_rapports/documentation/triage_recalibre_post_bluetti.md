# Triage recalibré — candidats à vérification runtime (post-Bluetti)

> **Cadre.** Lecture seule. Aucune correction, aucun patch, aucune modification documentaire. Objectif : reclasser la liste de priorisation à la lumière de l'enseignement Bluetti, pour **optimiser l'effort** avant la prochaine vérification détaillée.
>
> **Discriminant corrigé.** On ne compte plus « combien d'entités citées sont absentes du YAML ». On demande : **le cœur de doctrine (entités dérivées/décisionnelles, invariants, logique métier) est-il présent et consommé au runtime ?** Les entités absentes ne comptent que si elles **portent la doctrine** ; les entités d'intégration (custom_component/HACS), les catalogues diagnostic, les entités différées et les abréviations de nommage de **sources** ne sont pas de la dérive.

---

## 1. Ce que Bluetti a invalidé dans le triage initial

Le scan initial gonflait le soupçon dans **trois cas** qui ne sont pas de la dérive :
1. **Entités d'intégration** créées hors YAML (custom_component) → absentes du YAML par construction.
2. **Catalogues diagnostic** et **entités explicitement différées** → absence attendue, voire confirmatrice.
3. **Abréviations / variantes de nommage de sources** dans le doc → l'entité existe sous un nom voisin.

Appliqué à la liste, ce filtre **dégonfle fortement** la priorisation : la plupart des candidats P1/P2 tombent en *faux positif* ou *documentaire*.

---

## 2. Tableau de priorisation mis à jour

| Rang | Chemin | Doctrine (dérivés/logique) présente & consommée ? | Verdict recalibré | Nature |
|:--:|---|---|---|---|
| ✅ clos | `contrats/bluetti.md` | **Oui** — 7 dérivés + logique au seuil près | **Faux positif (vérifié)** | conforme |
| ✅ clos | `contrats/meteo/axe_humidite_relative_jardin.md` | **Oui** — pipeline complet `…/meteo/mesures/humidite_relative/jardin/` + **CI dédiée** ; sources réelles `humidite_relative_jardin_1/2/3` (doc abrège en `humidite_jardin_N`) | **Faux positif** | conforme |
| ▽ bas | `contrats/sante/sommeil.md` | **Partielle** — couche « vérité métier » `sommeil_derniere_nuit_*` présente ; couches *statistiques* / *calcul* absentes. **MAIS doc auto-déclarée `v0.9 (draft, non validé)`** | **Draft hors périmètre normatif** | documentaire (draft) |
| ◦ moyen-bas | `contrats/climatisation/06_doctrine_blocages.md` | **Majoritairement** — architecture de blocage présente (aération, horaire, `clim_bloquee`…) ; 2 familles (`fenetres`, `absence_prolongee`) absentes **sous le nom `clim_blocage_*_reel/_actif`**, apparemment implémentées autrement (`fenetre_ouverte_maison_avec_delai`, `clim_extinction_absence_prolongee_autorisee` présents) | **À confirmer** — possible écart de **cohérence de patron** | documentaire / structurel-léger |
| ◦ bas | `contrats/climatisation/08_execution.md` | **Oui** — cœur d'exécution présent et très consommé (`script.clim_execution`, `clim_target_mode`, `clim_power`, `timer.clim_retry`, `consigne_clim_appliquee`) ; seules 2 **automatisations** citées absentes (probable refactor vers le script / slug) | **Documentaire** | cosmétique / documentaire |
| ◦ bas | `contrats/chauffage/15_capteurs/03_…/fenetre_ouverte_maison.md` | **Oui** — dérivé `binary_sensor.fenetre_ouverte_maison` présent et très consommé ; sources réelles `binary_sensor.contact_chambre_*` (doc dit `capteur_chambre_*`) | **Documentaire** (renommage de sources) | documentaire |
| ◦ bas | `contrats/volets_pluie.md` | **Oui** — automatisations présentes, slug réordonné (`fermeture_volets_pluie_*` vs doc `meteo_pluie_fermeture_volets_*`) | **Cosmétique** | cosmétique |
| ◦ bas | `contrats/alarme/70_sirene_actions_terminales.md` | **Oui** — périphérique sirène présent (`sirene_bip`, `sirene_brutale`…) ; `switch.sirene_alarm` renommé | **Cosmétique** | cosmétique |
| – hors | `contrats/arsenal_nas.md` | **Frontière externe** — 2 entités côté NAS (hors HA) | **Hors scope** (système externe) | inconnu / externe |

*(Rappel : `contrats/bouclage.md` + `ecs/04` déjà arbitrés/patchés ; `parametres_invalides.md` = placeholders, faux positif.)*

---

## 3. Justification du reclassement (par candidat)

- **bluetti.md → conforme.** Doctrine intégralement implémentée ; les absences = intégration `bluetti_bt` + différés. *(Vérifié en détail.)*
- **humidite_relative_jardin.md → conforme (faux positif).** Le doc cite 3 sources `humidite_jardin_N` ; le runtime les a sous `humidite_relative_jardin_N` (+ `_suspect`/`_valide`), et **toute la chaîne dérivée** (validation, rétention, mémoire, façade finale) existe dans `12_template_sensors/meteo/mesures/humidite_relative/jardin/`, avec une **CI dédiée** (`.github/workflows/contracts_humidite_relative_jardin.yml`). Doctrine présente, consommée et testée → pas de dérive.
- **sommeil.md → draft, priorité basse.** En-tête `v0.9 (draft, non validé)`. La couche « vérité métier » (`sommeil_derniere_nuit_*`) est présente et consommée ; les couches *statistiques* (`sommeil_*_statistique`) et *calcul* (`sommeil_total_calcule`) sont absentes — comportement **attendu d'un draft** (doctrine partiellement en avance sur le runtime), pas d'une dérive de contrat normatif. À ne pas traiter comme un cas Bouclage.
- **clim/06_doctrine_blocages.md → à confirmer (seul résidu doctrine-pertinent).** Document **normatif**. Le patron de blocage est en place pour la majorité des familles ; mais 2 familles documentées (`clim_blocage_fenetres_*`, `clim_blocage_absence_prolongee_*`) **n'existent pas sous le nom `_reel`/`_actif`** attendu par le patron. Des entités voisines existent, mais l'**équivalence doctrinale n'est pas démontrée** : il peut s'agir soit d'un simple renommage, soit d'une **incohérence de patron** (2 familles ne suivent pas la structure normative). Domaine **récemment retravaillé** (chantier observabilité COOL v15.8.4) → divergence plausible.
- **clim/08_execution.md → documentaire.** Le cœur d'exécution idempotente (`script.clim_execution` + `clim_target_mode` + `clim_retry` + `clim_power`) est présent et très consommé ; seules 2 automatisations citées manquent, vraisemblablement absorbées par le modèle script ou renommées. Doctrine présente.
- **fenetre_ouverte_maison.md → documentaire.** Dérivé présent et consommé partout (chauffage/aération/clim) ; les sources sont `contact_chambre_*` et non `capteur_chambre_*`. Renommage de **sources** non répercuté, doctrine intacte.
- **volets_pluie / alarme sirene → cosmétique.** Logique/périphérique présents, simple décalage de slug ou de nom d'actionneur.
- **arsenal_nas → hors scope.** Système externe (NAS) ; frontière à qualifier, pas un contrat HA-runtime au sens strict.

---

## 4. Candidat unique recommandé pour la prochaine vérification runtime

### ➡️ `contrats/climatisation/06_doctrine_blocages.md`

**Pourquoi celui-là, et lui seul :**
- C'est le **seul candidat restant** dont l'écart pourrait être **doctrinal** (cohérence du patron de blocage), pas un simple renommage de source, un catalogue diagnostic ou un draft.
- Il est **explicitement normatif** (« Document normatif. ») — donc un écart y a une portée réelle, contrairement à `sommeil.md` (draft).
- Le domaine a été **récemment refondu** (chantier COOL v15.8.4), ce qui rend une divergence doctrine↔runtime crédible.
- La question est **nette et bornée** : les blocages « fenêtres » et « absence prolongée » sont-ils réellement implémentés (sous d'autres noms) conformément au patron `_reel`/`_actif`, ou s'agit-il d'une incohérence de patron / d'une doctrine en avance sur le runtime ?

**Rendement attendu, honnêtement : modéré.** La recalibration montre que le **gros poisson structurel (Bouclage) était déjà pris**. Les autres candidats sont des faux positifs, un draft, ou du documentaire/cosmétique. `clim/06` est le meilleur usage de l'effort, mais une vérification approfondie y confirmera probablement « doctrine présente, 2 familles à réconcilier » plutôt qu'une refonte. Les cas `clim/08`, `fenetre_ouverte_maison`, `volets_pluie`, `alarme sirene` peuvent être traités plus tard comme de simples **réconciliations de nommage**, sans vérification lourde.

---

*Fin du triage recalibré. Aucun fichier modifié. Aucune correction ni patch : uniquement un reclassement et une recommandation d'effort.*
