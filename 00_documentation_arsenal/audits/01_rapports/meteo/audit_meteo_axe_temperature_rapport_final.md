# Audit Arsenal — Domaine météo / axe température

> Type : rapport d'audit architectural
> Portée : sources météo / température extérieure, capteurs façade, contrats,
>          dépendances runtime, consommateurs, robustesse, fallbacks
> Mode : lecture seule — aucun code, contrat, runtime ou UI modifié
> Principe directeur : « le runtime est la référence, le contrat documente le runtime »

---

## 1. Résumé exécutif

**Signal net.** L'axe *température extérieure du domicile* repose sur une **façade
souveraine mature et conforme** : `sensor.temperature_jardin`, alimentée par un
pipeline contractualisé (validation → détection divergence chaude → fusion robuste
→ stabilisation EWMA/δ_max → continuité TTL 3 niveaux). Toutes les
décisions/actions extérieures (`chauffage`, `climatisation`, `aération`, `voiture`)
lisent cette façade et **non les capteurs bruts**. La séparation décision / action
/ diagnostic / UI est respectée.

**Risque principal.** Il n'est pas dans la façade elle-même, mais dans
**l'hétérogénéité des conventions d'abstention côté consommateurs** et dans une
**dette contractuelle centrale** : `contrat_fallback.md`, référencé par cinq
contrats, **n'existe pas comme fichier**. Le mécanisme de fallback est implémenté,
mais sa norme de référence est manquante.

**Criticité globale : MODÉRÉE.** Aucune dépendance directe d'une décision sur un
capteur faillible n'a été trouvée pour l'extérieur domicile. Les modes dégradés
observés sont aujourd'hui *fail-safe par chance de configuration*, pas *fail-safe
par conception partagée*.

**Conclusion architecturale.** L'architecture cible (façade météo souveraine) est
**déjà atteinte pour l'axe jardin**. Le chantier n'est pas de la construire mais de
(a) **généraliser la convention d'abstention**, (b) **solder la dette contractuelle
fallback/validation**, (c) **statuer sur l'extérieur imprimerie**, source non
souveraine et non contractualisée.

---

## 2. Périmètre analysé

**Fichiers inspectés (extraits clés) :**

- Architecture : `00_documentation_arsenal/architecture/capteurs_meteo.md`,
  `meteo_affichage.md`
- Contrats : `contrats/meteo/{meteo,gouvernance,validation,axe_temperature,axe_temperature_jardin,affichage}.md`
- Implémentation façade extérieure :
  `12_template_sensors/meteo/mesures/temperature/jardin/*`
  (facade, validation_sources, suspect_chaud, nb_sources_retenues,
  incoherence_retenue, diagnostic_fusion_sensors)
- Implémentation extérieure imprimerie :
  `12_template_sensors/meteo/mesures/temperature/exterieur.yaml`
- Prévision : `12_template_sensors/meteo/{temperature_prevue,meteo_favorable}.yaml`
- Consommateurs décision :
  `chauffage/autorisation_cible_selon_temperature.yaml`,
  `climatisation/autorisation/{cool,heat}.yaml`,
  `climatisation/decision/raison.yaml`,
  `aeration/conseillee/{rdc,etage}.yaml`,
  `11_automations/voiture/autonomie.yaml`
- Helpers + stabilisation : `03/05/07_*/meteo/temperature_jardin_*`,
  `11_automations/meteo/temperature_jardin_stabilisation.yaml`

**Domaines concernés :** chauffage, climatisation, aération, voiture (autonomie VE),
dérivés météo (humidex / humidité absolue / point de rosée), statistiques,
palmarès, UI/dashboards.

**Exclusions :** axe *humidité* traité seulement là où il croise la température
(aération) ; axe *température intérieure* mentionné pour mémoire (lui aussi façadé,
conforme `axe_temperature.md`) mais hors cœur du sujet « extérieur/météo ».

---

## 3. Cartographie des sources météo / température

| Entité | Type | Niveau | Rôle | Disponibilité attendue | Comportement dégradé |
|---|---|---|---|---|---|
| `sensor.temperature_jardin_1` | brute (Netatmo/HomeKit NO) | source | Mesure extérieure domicile | Faillible (cloud/HK) | Exclue par validation si `unknown`/`unavailable`/hors `[-10;50]`/âge>900 s |
| `sensor.temperature_jardin_2` | brute (Netatmo/HomeKit SE) | source | Mesure extérieure domicile | Faillible | idem |
| `sensor.temperature_jardin_3` | brute (SwitchBot/BT) | source | Mesure extérieure domicile (non caractérisée) | Faillible | idem ; ne peut influencer la cible si divergence haute |
| `sensor.temperature_jardin_X_validee` | validation | couche 1 | Recevabilité par source | Dérivée | `unavailable` si source invalide |
| `sensor.temperature_jardin_cible_robuste` | fusion | couche 3 | Cible instantanée robuste | Dérivée | absente → bascule mémoire/TTL |
| `input_number.temperature_jardin_etat_publie` (+ `_ts`) | mémoire | couche 4 | État stabilisé persistant | Persistant | sentinelle hors plage → `mem_ok` faux |
| **`sensor.temperature_jardin`** | **façade souveraine** | **couche 5** | **Température extérieure de référence domicile** | **Façade** | publie `unknown` si cible absente ET (mémoire non plausible OU âge>TTL 1800 s) |
| `sensor.temperature_jardin_statut` | diagnostic | couche 5 | Confiance : `nominal/suspect_chaud/incoherence_retenue/degrade/memoire/inconnu` | Façade | `inconnu` = interdiction métier |
| `sensor.temperature_exterieur_1` / `_2` | brute (Komori NO / Bobst SO) | source | Mesure extérieure **imprimerie** | Faillible | aucune validation amont |
| `sensor.temperature_exterieur` | « façade » non souveraine | — | Extérieur imprimerie (min des deux) | Faillible | renvoie `None` si les deux invalides (≠ commentaire qui annonce une mémoire) |
| `weather.forecast_maison` | brute (met.no) | source | Prévision horaire | Faillible (cloud) | chaîne avale fail-safe |
| `sensor.temperature_prevue` | dérivée forecast | — | T° extérieure prévue +Xh | Dérivée | indispo → consommateur off |
| `binary_sensor.meteo_favorable_chauffage` | dérivée forecast | — | Anticipation confort différé | Dérivée | `availability` gardée ; `false` si sources absentes |

---

## 4. Chaînes de dépendance

**Chaîne A — Extérieur domicile (souveraine, conforme) :**
`jardin_1/2/3 (brut)` → `*_validee (validation §3/§4 + péremption 900 s)` →
`cible_robuste (médiane, exclusion suspect_chaud, fusion §7)` →
`stabilisation EWMA + δ_max + reseed (automation + helpers)` →
**`sensor.temperature_jardin` / `_statut`** →
`chauffage / climatisation / aération / voiture / dérivés / stats / UI`.

**Chaîne B — Extérieur imprimerie (non souveraine) :**
`temperature_exterieur_1/_2 (brut)` →
`sensor.temperature_exterieur (min naïve, sans validation/TTL/statut)` →
`dérivés imprimerie (humidex/HA/rosée) + UI + statistics + recorder`.
**N'alimente aucune décision/action.**

**Chaîne C — Prévision (gardée, fail-safe) :**
`weather.forecast_maison` → `sensor.temperature_prevue` →
`binary_sensor.meteo_favorable_chauffage (availability gardée)` →
anticipation `sensor.chauffage_autorisation_cible`.

---

## 5. Consommateurs identifiés

**Chauffage** — `sensor.chauffage_autorisation_cible` lit
`sensor.temperature_jardin` ; `ecart_consigne/ecart_doux.yaml`,
`ecart_froid.yaml` ; contexte UI `meteo_chauffage_actuelle_72.yaml`. Anticipation
via chaîne C.

**Climatisation** — `binary_sensor.autorisation_clim_cool` (`cool.yaml`),
autorisation `heat.yaml`, `decision/raison.yaml`, cartes diagnostic
`carte_clim_diagnostic_temperature_exterieure(_hiver).yaml`.

**Aération** — `binary_sensor.aeration_preferable_rdc` / `_etage`
(`conseillee/rdc.yaml`, `etage.yaml`) : consomment `temperature_jardin`,
`humidite_absolue_jardin`, `humidite_relative_jardin`.

**ECS** — non concerné : aucune lecture de température extérieure trouvée dans le
domaine ECS.

**Voiture** — `11_automations/voiture/autonomie.yaml` (estimation autonomie VE
selon T° extérieure).

**Dérivés météo** — `humidex/base.yaml`, `humidite_absolue/base.yaml`,
`point_de_rosee/base.yaml` : variantes jardin (façade) et imprimerie
(`temperature_exterieur`).

**Statistiques / diagnostic / UI** — `statistiques/filtres/temperature.yaml`,
`13_sensor_platforms/statistics/meteo/*`, palmarès chaud/froid,
`update/cloture_temperature_max|min`, `couleurs/meteo/temperature.yaml`,
KPI/dashboards.

---

## 6. Analyse de robustesse

| Consommateur | Comportement nominal | Si façade `unknown`/`unavailable` | Risque | Criticité | Recommandation |
|---|---|---|---|---|---|
| `chauffage_autorisation_cible` | logique ternaire | `ext = float(99)` → test `==99` → cible **`unknown`** (abstention) | Sentinelle correcte (99 hors `[-10;50]`) mais implicite | Faible | Documenter la sentinelle ; idéalement test d'indispo explicite |
| `autorisation_clim_cool` | `T ≥ seuil_min` | `T = float(0)` → `0 ≥ 99(défaut)` → **false** | **0 °C est une valeur plausible, pas une sentinelle** ; fail-safe seulement par sens de comparaison + seuil par défaut | **Modérée** | Remplacer `float(0)` par test d'indisponibilité explicite → abstention |
| `autorisation_clim` heat | `T > seuil_hiver` | `T = float(0)` → bloque | idem | Modérée | idem |
| `clim decision/raison` | diagnostic | `float(0)` → raison potentiellement trompeuse | UI/diag seulement | Faible | aligner sur convention |
| `aeration_preferable_*` | calcul Δ thermique/HA | garde `reject in [unknown,unavailable,None]` → **abstention propre** | Aucun (bonne pratique) | — | **Modèle à généraliser** |
| `voiture/autonomie` | estimation | garde `is_number` → abstention | Aucun | — | conforme |
| `meteo_favorable_chauffage` | seuil prévision | `availability` gardée → `false` → anticipation off | Aucun | — | conforme |
| `sensor.temperature_exterieur` (imprimerie) | min des deux | renvoie **`None`** (le commentaire annonce à tort une mémoire) | Incohérence code/doc ; pas de continuité | Faible (aucune décision) | Clarifier : observation-only ou axe souverain |

---

## 7. Fallbacks existants

- **Explicite et souverain (chaîne A) :** niveaux 1/2/3 du contrat
  `axe_temperature_jardin` — fusion → `memoire` (âge ≤ TTL 1800 s, plausibilité §4,
  garde `systeme_stable`) → `unknown`. Report résiduel δ_max maintenu dans l'état
  interne (§8.3). **Bien implémenté.**
- **Implicite / acceptable :** chauffage `float(99)` (sentinelle hors plage,
  fail-safe).
- **Implicite / fragile :** climatisation `float(0)` — fabrique une mesure
  plausible au lieu d'abstenir. Fail-safe conjoncturel, non garanti par conception.
- **Fallback dangereux / trompeur :** `exterieur.yaml` (imprimerie) — l'en-tête
  promet « conserve sa dernière valeur » alors que le `state` renvoie `None` ;
  l'attribut `capteur_utilise` tente une mémoire incohérente avec le state.
  **Mensonge documentaire.**
- **Absent :** extérieur imprimerie — pas de TTL, pas de plausibilité, pas de
  statut, pas de garde de péremption.

---

## 8. Écarts et dettes

**Dette contractuelle.**

1. `contrat_fallback.md` référencé par `meteo.md`, `gouvernance.md`,
   `validation.md`, `axe_temperature.md`, `axe_temperature_jardin.md` — **fichier
   inexistant**. La norme du mécanisme le plus critique n'est pas écrite.
2. `validation.md` est l'implémentation de `contrat_validation.md` mais **le nom de
   fichier ne correspond pas** aux renvois contractuels.
3. Extérieur imprimerie (`sensor.temperature_exterieur`) : **aucun contrat d'axe**,
   alors que `axe_temperature_jardin.md §1` annonce qu'« chaque zone fait l'objet
   d'un contrat d'axe distinct ».

**Dette runtime.**

4. **Conventions d'abstention divergentes** : `float(99)` (chauffage) vs `float(0)`
   (clim) vs gardes explicites (aération/voiture). Pas de convention partagée.
5. `float(0)` clim = valeur plausible injectée dans le calcul, pas une sentinelle →
   risque latent si un seuil bascule de sens.

**Dette diagnostic.**

6. `sensor.temperature_jardin_statut` (et `degrade`/`suspect_chaud`/
   `incoherence_retenue`) **n'est consommé par aucune décision, aucune
   notification, aucun watchdog**. Le diagnostic riche reste « mort » côté
   supervision active.
7. La validation runtime ajoute une **garde de péremption (âge ≤ 900 s)** sur les
   sources brutes, **absente de `validation.md`** (runtime plus strict que le
   contrat).

**Dette UI.**

8. À vérifier au cas par cas : les dashboards doivent restituer honnêtement
   `memoire`/`inconnu` (la façade expose `mode_publication`, `cause`,
   `age_memoire_s`) — conforme à `affichage.md` qui exige une UI strictement
   passive.

**Dette documentaire.**

9. En-tête de `exterieur.yaml` faux (mémoire annoncée, non implémentée).
10. `axe_temperature_jardin.md` note lui-même que les contrats amont « ne sont pas
    versionnés — dette documentaire à solder ».

---

## 9. Recommandations architecturales (sans code)

L'architecture cible « façade météo souveraine » **existe déjà pour le jardin** ;
il s'agit de la **généraliser et de la documenter**, autour de six attributs
canoniques par axe extérieur :

- **Température extérieure de référence** — une façade par zone
  (`temperature_jardin` ✅ ; pour l'imprimerie : décider souveraineté ou
  observation explicite).
- **État de confiance** — le `statut` existant ; à promouvoir au rang de signal
  consommable.
- **Mode de source** — `fusion / memoire / abstention` (déjà exposé en attribut).
- **Raison de dégradation** — `cause` (déjà exposé).
- **Signal de disponibilité météo** — convention unique : un consommateur ne doit
  jamais *fabriquer* une valeur plausible ; il abstient explicitement sur
  indisponibilité.
- **Règles de consommation par domaine** — formaliser : *bloquer la décision*
  (chauffage/clim), *dégrader l'UI seulement* (dashboards), *déclencher un
  diagnostic* (notification sur `inconnu`/`degrade` persistant), *fallback
  explicite* (réservé à la façade, jamais au consommateur).

Principe directeur proposé, cohérent avec la doctrine « REJECT-not-clamp » et
« writer souverain unique » : **la façade abstient (publie `unknown`), le
consommateur teste l'indisponibilité et s'abstient — il ne devine jamais.**

---

## 10. Plan d'action proposé

- **Lot 1 — Observation / cartographie.** Figer le présent audit ; recenser chaque
  seuil par défaut (`float(99)`, `float(0)`) et vérifier son sens de fail-safe réel
  face aux valeurs d'`input_number` en runtime.
- **Lot 2 — Façade météo souveraine.** Écrire le contrat de fallback (formalisant
  les niveaux 1/2/3 déjà implémentés) ; aligner le nommage `validation.md` ↔
  renvois ; intégrer la garde de péremption 900 s au contrat de validation.
- **Lot 3 — Migration des consommateurs.** Définir une convention d'abstention
  unique ; migrer la climatisation (`float(0)` → test d'indisponibilité explicite) ;
  harmoniser le chauffage ; aération/voiture déjà conformes (référence).
- **Lot 4 — Diagnostics / UI.** Câbler une supervision sur
  `temperature_jardin_statut` (notification persistante si `inconnu`/`degrade`
  prolongé) ; auditer les dashboards pour restitution honnête mémoire/abstention.
- **Lot 5 — Contrats / doc / tests.** Statuer sur l'imprimerie (contrat d'axe vs
  observation-only) ; corriger l'en-tête de `exterieur.yaml` ; ajouter des tests de
  contrat (style pipeline CI existant) sur les modes dégradés de la façade.

> Note : le plan d'action détaillé et ordonné par risque fait l'objet d'un document
> dédié — `03_plans_action/meteo/plan_action_meteo_axe_temperature.md`.

---

## 11. Questions ouvertes (arbitrages humains)

1. **Imprimerie :** promouvoir `sensor.temperature_exterieur` en axe souverain
   (contrat + pipeline) **ou** le déclarer explicitement *observation-only* et
   retirer le commentaire de mémoire trompeur ?
2. **Statut consommable :** une décision doit-elle réagir au `statut` (ex. clim
   refusant d'agir en `degrade`/`incoherence_retenue`) **ou** la lecture
   valeur-seule (façade=`unknown` ⇒ abstention) suffit-elle, le statut restant
   purement observationnel ?
3. **Convention d'abstention :** sentinelle hors-plage unique (façon `float(99)`)
   **ou** test d'indisponibilité explicite généralisé (façon aération) — lequel
   devient la norme Arsenal ?
4. **Péremption :** la garde 900 s sur les sources brutes monte-t-elle dans le
   contrat de validation, ou reste-t-elle une décision d'implémentation locale ?
5. **Supervision active :** faut-il une notification/watchdog sur indisponibilité
   météo prolongée, et avec quel délai de grâce ?
