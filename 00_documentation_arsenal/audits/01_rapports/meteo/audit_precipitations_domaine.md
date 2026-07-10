# Audit Arsenal — Domaine fonctionnel « Précipitations »

> Type : rapport d'audit de domaine, architectural et statique (lecture seule).
> Portée : **l'ensemble du domaine « Précipitations »** — acquisition, normalisation,
>          consolidation, décision, action, mesure, cumuls, records, prévision,
>          observabilité, recorder, CI — et **toutes ses interactions inter-domaines**
>          (volets, aération, arrosage, climatisation, chauffage, présence, météo).
> Mode : lecture seule — aucun runtime, template, helper, script, automation, dashboard,
>          configuration, contrat, CI ou documentation normative existante modifié.
>          Seule écriture : le présent rapport d'audit.
> Méthode : voir §3.
> Filiation : ce rapport **élargit** l'audit spécialisé
>          [`audit_precipitations_chaine_decisionnelle.md`](audit_precipitations_chaine_decisionnelle.md)
>          (chaîne de protection des ouvrants, déjà consigné). Il en reprend les
>          constats structurants et les replace dans le domaine complet.
> Neutralité : ce document décrit et cartographie. Les « opportunités » (§13) et
>          « recommandations » (§14) sont des pistes, **pas** des décisions
>          d'implémentation. Aucun correctif, aucun patch.

---

## 1. Synthèse exécutive

Le domaine « Précipitations » d'Arsenal est **étendu, stratifié et fonctionnellement
mûr** : deux sources physiques (pluviomètre Netatmo, détecteur Zigbee SONOFF SNZB-05)
plus une source de prévision (Met.no) alimentent une mesure sécurisée localement, des
cumuls glissants honnêtes, un palmarès journalier contractualisé, et quatre familles de
consommateurs (volets, aération, arrosage, affichage/records).

Trois traits structurants ressortent de l'audit :

1. **La notion de « pluie » n'est pas unique mais éclatée.** Le domaine expose **au moins
   quatre représentations parallèles de « il pleut »** — `input_boolean.pluie_en_cours`,
   `binary_sensor.intention_pluie_forte`, `binary_sensor.pluie_recente`, et la présomption
   `sensor.pluie_prevue` — chacune câblée sur une source différente et consommée par des
   domaines différents, **sans autorité unique de domaine** qui les consolide.

2. **La couche mesure est sécurisée, la couche décision ne l'est pas.** Les cumuls et le
   total local passent par une façade locale robuste (`pluie_total_local`, `pluie_cumul_*`)
   fidèle à la doctrine `securisation_capteurs_externes.md`. Mais les **décisions**
   (`pluie_en_cours`, `intention_pluie_forte`, gate aération) lisent **directement des
   sources brutes externes** (Netatmo cloud, Zigbee brut). La doctrine est appliquée à la
   statistique, pas à la décision.

3. **La couverture contractuelle et CI est asymétrique.** La *réaction volets* est
   contractualisée + vérifiée en CI ; le *palmarès pluie* dispose d'un contrat STRICT
   (`pluie_palmares.md` v1.1) **mais d'aucun checker** (le palmarès *température*, lui, en a
   trois) ; la *production* de la pluie métier (détection, consolidation d'épisode, cumuls,
   suspension arrosage) n'a **ni contrat ni CI**.

Le domaine fonctionne. Ses faiblesses sont d'ordre **architectural et de gouvernance**
(fragmentation sémantique, sécurisation partielle, asymétrie start/stop d'épisode, angles
morts contractuels), non de panne fonctionnelle courante.

---

## 2. Périmètre

**Inclus.** Toute la chaîne pluie : capteurs physiques et virtuels, intégration météo de
prévision, normalisation Zigbee, consolidation d'épisode, intentions, mesure et cumuls,
palmarès, prévision, notifications, recorder, statistiques, dashboards, diagnostics,
contrats et CI relatifs à la pluie, ainsi que **les interactions** avec volets, aération,
arrosage, climatisation, chauffage, présence, météo.

**Exclu.** Le détail interne de la mécanique de fermeture des volets (couvert par l'audit
spécialisé compagnon) ; les axes météo hors pluie (température, humidité, pression — cités
seulement là où ils croisent la pluie) ; les intégrations tierces elles-mêmes (code Netatmo,
Zigbee2MQTT, Met.no) ; `custom_components/`.

---

## 3. Méthode

- Lecture directe du code (helpers, templates, automations, scripts, dashboards, recorder,
  utility_meter, contrats, workflows CI).
- Cartographie des flux par recherche des producteurs et consommateurs de chaque entité
  pluie (traçage amont/aval).
- Confrontation aux doctrines normatives Arsenal (`03_doctrines/`, `architecture/`).
- Aucune exécution runtime, aucune inspection d'historique live : audit **statique**. Là où
  la sémantique runtime d'une entité d'intégration n'est pas déclarée dans le dépôt (ex.
  `weather.forecast_maison`, `sensor.pluviometre_precipitation`), le fait est signalé plutôt
  qu'inféré.

---

## 4. Cartographie du domaine

### 4.1 Sources

| Source | Entité(s) | Nature | Sémantique |
|---|---|---|---|
| Pluviomètre Netatmo (cloud) | `sensor.pluviometre_precipitation` (intensité) · `…_last_hour` · `…_aujourd_hui` | Mesure quantitative | Pluie **mesurée** |
| SONOFF SNZB-05 (Zigbee `zigbee_pluie` `0xa4c1380550bda762`) | `binary_sensor.zigbee_pluie_water_leak` (+ battery, lqi) | Détecteur de présence d'eau | Premières **gouttes** |
| Prévision Met.no | `weather.forecast_maison` → `sensor.pluie_prevue` | Présomption | Pluie **prévue** |
| Injection manuelle | `input_boolean.pluie_zigbee_virtuel` | Source de test / secours | Substitut du Zigbee |

> `weather.forecast_maison`, `sensor.pluviometre_precipitation*` et
> `binary_sensor.zigbee_pluie_water_leak` sont des **entités d'intégration**, non déclarées
> en YAML dans le dépôt : uniquement consommées.

### 4.2 Transformations (normalisation / mesure / cumuls / records)

| Couche | Entité / fichier | Rôle |
|---|---|---|
| Normalisation Zigbee | `impulsion/debut.yaml`, `impulsion/fin.yaml`, `timer.pluie_zigbee_rearm`, `input_boolean.pluie_zigbee_virtuel` | Anti-rebond 1 s, impulsion 2 min, coupe-circuit 10 min |
| Mesure locale | `capteurs_locaux.yaml` → `sensor.pluie_aujourdhui_local`, `sensor.pluie_total_local` (+ stores `pluie_total_local_store`, `pluie_today_last`) | Façade locale robuste + total persistant |
| Total monotone | `totaliseur_cumulatif.yaml` (`10160000000009`) | Accumulateur monotone (n'enlève jamais) |
| Cumuls bruts | `13_sensor_platforms/statistics/meteo/pluie/cumul_{24,48,72}h.yaml` → `…_brut` | Moteurs `statistics` (`change`, max_age h) |
| Cumuls métier | `cumul_glissant.yaml` → `sensor.pluie_cumul_{24,48,72}h` | Distinction « fenêtre vide = 0 » vs « source morte = unavailable », clamp anti-négatif |
| Compteurs de cycle | `utility_meter.yaml` : `pluie_journaliere` (daily), `pluie_semaine`/`sensor.pluie_hebdomadaire` (weekly) | Cumuls par cycle, source `pluie_total_local` |
| Records | `palmares_journalier_synthese.yaml`, `…_anomalie.yaml`, `…_snapshot.yaml`, `…_evaluation.yaml`, helpers `palmares_pluie_journalier_*` | Top-10 journalier persistant + anomalie structurelle |
| Prévision | `prevue.yaml` → `sensor.pluie_prevue` | Cumul prévu sur horizon glissant |

### 4.3 Décisions (couche métier « il pleut »)

| Entité | Source | Paradigme | Consommé par |
|---|---|---|---|
| `input_boolean.pluie_en_cours` | SNZB prioritaire + Netatmo secours (entrée) ; **Netatmo seul** (sortie) | Impératif (automations `maj_sensor/on|off`) | Volets chambres, aération |
| `binary_sensor.intention_pluie_forte` | Netatmo ≥ `seuil_pluie_fermeture_volets` (2,5 mm) | Déclaratif (template) | Volets séjour |
| `binary_sensor.pluie_recente` | Netatmo `last_hour` > 0 | Déclaratif (template) | Aération (affichage), dashboards volets |
| `binary_sensor.arrosage_suspension_pluie` | cumuls 24/48/72 h + `pluie_prevue` vs seuils | Déclaratif (template) | Arrosage (intention) |

### 4.4 Actions

| Entité | Déclencheur pluie | Effet |
|---|---|---|
| `automation.pluie_volets_chambres` (`…011`) | `pluie_en_cours → on` | Notification (présence) / fermeture volets chambres (absence) |
| `automation.pluie_volets_sejour` (`…010`) | `intention_pluie_forte → on` | Fermeture volets séjour |
| `script.volets_fermeture_execute` | (délégué) | Fermeture idempotente `queued` |
| `automation.arrosage_declenchement` (`…002`) | via `arrosage_intention` (gate `not suspension_pluie`) | Lance / inhibe l'arrosage |

### 4.5 Affichage & diagnostics

Dashboards `meteo/meteo_precipitations`, `meteo/meteo_palmares`, `arrosage/diagnostic`,
`arrosage/reglages`, `volets/diagnostic`, `volets/reglages`, `aeration/principal` ; cartes
`19_button_card_templates/**` (décision pluie, exposition, KPI cibles, seuils, raison
arrosage). `sensor.resume_fenetres_concernees_ouvertes_pluie` (texte UI).

### 4.6 Dépendances (graphe résumé)

```
SNZB-05 ─impulsion─▶ pluie_zigbee_virtuel ─┐
                                           ├─▶ pluie_en_cours ─▶ volets chambres
Netatmo (precip) ──────────────────────────┘        │            aération (veto)
        │                                            └─(sortie)─ Netatmo seul
        ├─▶ intention_pluie_forte ─▶ volets séjour
        ├─▶ pluie_recente ─▶ aération (affichage) / volets diag
        ├─▶ pluie_aujourdhui_local ─▶ totaliseur ─▶ pluie_total_local ─┬─▶ utility_meter (jour/semaine) ─▶ palmarès
        │                                                              └─▶ statistics brut ─▶ cumul_glissant ─▶ suspension_pluie ─▶ arrosage
Met.no ─▶ pluie_prevue ───────────────────────────────────────────────────────────────────▶ suspension_pluie ─▶ arrosage
                                                                          aération_preferable_etage ─▶ clim_blocage_aeration_etage (2nd ordre)
```

---

## 5. Architecture actuelle : chaîne par couche et responsabilités

| Couche | Réalisation | Responsabilité | Observation |
|---|---|---|---|
| **Acquisition** | Netatmo (cloud), SNZB-05 (Zigbee), Met.no | Capter le réel | Deux capteurs de natures différentes (mesure vs contact d'eau) traités comme équivalents pour l'épisode |
| **Normalisation** | `impulsion/*`, timer réarmement | Transformer un signal brut instable en impulsion propre | Excellente pour le Zigbee ; **inexistante** pour le Netatmo (lu brut) |
| **Sécurisation** | `capteurs_locaux.yaml`, `cumul_glissant.yaml` | Façade locale, honnêteté d'état | Appliquée à la **mesure/cumuls**, **pas** à la décision |
| **Consolidation** | `maj_sensor/on|off` → `pluie_en_cours` ; `totaliseur_cumulatif` → total | Produire une vérité stable | Épisode : consolidation **impérative** et **asymétrique** ; total : monotone et propre |
| **Décision** | `intention_pluie_forte`, `pluie_recente`, `suspension_pluie`, gate aération | Exprimer une intention métier | Éclatée en signaux parallèles, paradigmes mixtes (impératif vs déclaratif) |
| **Action** | automations volets, arrosage ; `volets_fermeture_execute` | Appliquer | Exécution pure et idempotente — exemplaire |
| **Observabilité** | dashboards, attributs, recorder, palmarès, `system_log` | Rendre l'état lisible | Riche en affichage ; **pauvre en traçabilité décisionnelle** (source d'un épisode non exposée) |

---

## 6. Concepts métier : présents, absents, confondus

| Concept | État | Porté par | Remarque |
|---|---|---|---|
| Premières gouttes | ◐ implicite | `zigbee_pluie_water_leak` (brut) | Non exposé comme concept nommé ; absorbé dans `pluie_en_cours` |
| Pluie détectée | oui | `pluie_en_cours` | Mais mêlée à « épisode en cours » |
| Pluie en cours | oui | `pluie_en_cours` | Binaire, sans durée ni intensité |
| Pluie mesurée | oui | `sensor.pluviometre_precipitation`, `pluie_total_local` | — |
| Pluie récente (≤ 1 h) | oui | `binary_sensor.pluie_recente` | — |
| Pluie persistante | **non** | — | Aucune notion de durée d'épisode / intensité intégrée |
| Pluie forte | oui | `binary_sensor.intention_pluie_forte` | Seuil instantané, **sans hystérésis** |
| Pluie terminée | ◐ implicite | `pluie_en_cours = off` (Netatmo seul) | Pas de concept explicite de fin |
| Pluie prévue | oui (bien isolée) | `sensor.pluie_prevue` | « présomption », jamais 0 par défaut |
| Cumuls 24/48/72 h | oui | `sensor.pluie_cumul_*` | Honnêteté d'état soignée |
| Cumul jour / semaine | oui | `pluie_journaliere`, `pluie_hebdomadaire` | — |
| **Humidité résiduelle** (sol/surfaces mouillées après pluie) | **non** | — | Concept absent — recherché, aucun capteur/template ne le modélise |

**Confusions notables :**
- **Quatre notions de « il pleut »** coexistent sans consolidation (§1).
- Le label de décision **`pluie_recente`** de l'aération est en réalité alimenté par
  `input_boolean.pluie_en_cours`, tandis que les dashboards volets lient le même libellé
  `pluie_recente` à la **vraie** entité `binary_sensor.pluie_recente` : **un même mot pour
  deux entités différentes** selon le domaine.
- Le **SNZB-05 est un détecteur de fuite d'eau** (`water_leak`) promu au rang de source
  d'épisode de pluie — usage détourné (d'où le coupe-circuit anti-blocage 10 min).

---

## 7. Consommateurs du domaine

| Domaine consommateur | Entité(s) pluie consommée(s) | Type de couplage |
|---|---|---|
| **Volets — chambres** | `pluie_en_cours` (+ présence, verrou) | Décision / action |
| **Volets — séjour** | `intention_pluie_forte` (+ autorisation) | Décision / action |
| **Aération** (RDC/étage/global) | `pluie_en_cours` (**veto**, surclassé par CO₂ fort) ; `pluviometre_precipitation_last_hour` (affichage) ; RH extérieure ≥ seuil → modulateur `aeration_mod_pluie_delta_ha` | Décision (gate) |
| **Arrosage** | `pluie_cumul_24/48/72h` + `pluie_prevue` → `suspension_pluie` → `arrosage_intention` (gate `not susp`) | Décision (suspension) |
| **Climatisation** | `aeration_preferable_etage` (elle-même vetoée par la pluie) → `clim_blocage_aeration_etage_reel` | **2nd ordre** (indirect) |
| **Chauffage** | — | **Aucun** (réagit aux épisodes d'aération *physiques*, pas à la pluie) |
| **Présence / sécurité** | `presence_famille_securite` gate la fermeture volets ; **pas** de couplage alarme | Contexte |
| **Records / statistiques** | `pluie_journaliere` → palmarès ; cumuls, recorder | Statistique |
| **Affichage** | multiples dashboards + cartes | Présentation |
| **Notifications** | 3 notifications, **toutes** issues des 2 automations volets | Sortie utilisateur |

**Entités sans consommateur fonctionnel transverse** : `binary_sensor.zigbee_pluie_water_leak`
(uniquement dashboard + entrée de `pluie_en_cours`) et `sensor.pluie_journaliere` (uniquement
palmarès + dashboard).

---

## 8. Robustesse : situations limites

| # | Situation | Comportement actuel | Appréciation |
|---|---|---|---|
| 1 | Premières gouttes, Netatmo à 0 | Chambres/aération réagissent (SNZB prioritaire, si maillon sain) ; **séjour non** (2,5 mm requis) | Angle mort séjour **par conception** |
| 2 | Pluie faible / bruine sous 0,1 mm | Épisode ouvert par SNZB puis **refermé par Netatmo** (< 0,1 mm/5 min) malgré bruine | Fermeture prématurée d'épisode |
| 3 | Pluie discontinue / averses | Impulsion SNZB réarmée toutes les 2 min ; `pluie_en_cours` peut rebondir | Pas d'« épisode englobant » |
| 4 | Pluie forte / orage oscillant autour de 2,5 mm | `intention_pluie_forte` sans hystérésis → bascules et re-notifications | Chatter |
| 5 | Incohérence SNZB (eau) vs Netatmo (0 mm) | Priorité codée dans `maj_sensor/on`, **sans réconciliation ni trace** de la source | Non observable |
| 6 | Perte du SNZB | Repli sur Netatmo (lent), **sans alerte** de perte du chemin rapide | Dégradation silencieuse |
| 7 | Indisponibilité cloud Netatmo | **Épisode `pluie_en_cours` ne peut plus être refermé** (sortie exige Netatmo valide) | **Risque d'état collant** |
| 8 | Faux positif SNZB (condensation, nettoyage) | Ouvre un épisode ; coupe-circuit 10 min limite le blocage | Mitigé mais possible |
| 9 | Faux négatif (mouillage lent du SNZB) | Retard de détection des premières gouttes | Latence matérielle |
| 10 | Redémarrage Home Assistant | `systeme_stable` (reprise), watchdog 1 min, `timer restore`, stores persistants, palmarès sans `initial` | **Bien couvert** |
| 11 | Cumuls : fenêtre vide vs source morte | `cumul_glissant` distingue 0.0 vs unavailable | **Exemplaire** |
| 12 | Reset du store de total | Totaliseur monotone n'enlève jamais ; clamp anti-négatif au niveau métier | Bien géré |

---

## 9. Observabilité

- **Points forts** : attributs décisionnels riches (`source`, `seuil`, `valeur`, `mode`,
  `presence`, `fiabilite`, `motif`) ; dashboards de trace décisionnelle (volets/diagnostic,
  arrosage/diagnostic) ; palmarès avec `binary_sensor` d'anomalie structurelle et `detail`
  humain ; recorder cohérent (bloc « PLUIE / PRESSION » Population A justifié).
- **Limites** :
  - **Aucune trace de la source** ayant ouvert un épisode (`pluie_en_cours` ne dit pas si
    c'est le SNZB ou le Netatmo qui a déclenché).
  - **Pas de notification** ni de diagnostic de **perte du chemin rapide** (SNZB indisponible)
    ou d'**épisode collant** (Netatmo indisponible pendant un épisode).
  - Le palmarès pluie écrit uniquement un `system_log` en cas de snapshot invalide ; aucune
    remontée utilisateur.
  - Suspension arrosage : diagnostic présent (`fiabilite`/`motif`) mais **muet** (ne notifie
    pas quand il inhibe l'arrosage).

---

## 10. Gouvernance : conformité aux principes Arsenal

| Principe | Source doctrinale | Verdict | Détail |
|---|---|:--:|---|
| Séparation décision / action | `separation_decision_action.md` | Conforme | Réaction volets et arrosage : décision (templates) vs action (scripts/automations) nette |
| Séparation acquisition / décision | idem + `capteurs_meteo.md` | Partiel | Mesure séparée proprement ; décision lit encore des sources brutes |
| Sécurisation des capteurs externes | `securisation_capteurs_externes.md` | **Écart** | Décisions sur Netatmo cloud + Zigbee **bruts** ; sécurisation appliquée aux cumuls seulement |
| Autorité unique par domaine | `principes_generaux.md` §2 | **Écart** | 4 notions « il pleut » concurrentes, pas d'autorité unique |
| Robustesse | `principes_generaux.md` §5/§6 | Partiel | Reprise redémarrage et honnêteté d'état solides ; risque d'état collant (sortie Netatmo-only) |
| Idempotence | `principes_generaux.md` §4 | Conforme / partiel | Exécution `queued` idempotente ; `intention_pluie_forte` sans hystérésis |
| Observabilité | §9 | Partiel | Riche à l'affichage, pauvre en traçabilité de décision |
| Nommage par représentation | `nommage_entites.md` §7 | Écart | `zigbee_pluie_water_leak` nomme le matériel ; label `pluie_recente` réutilisé pour 2 entités |
| Documentation / contrats | — | **Écart** | Production pluie non contractualisée ; précipitation absente des axes du contrat météo |
| Maintenabilité (CI) | — | **Écart** | Palmarès pluie STRICT **sans checker** (température en a 3) ; détection/cumuls/suspension sans CI |

**Écarts de cohérence documentaire** (rappel/complément de l'audit compagnon) :
`intention_pluie_detectee.yaml` définit `intention_pluie_forte` ; `volets_auto_pluie.yaml`
définit `fermeture_volets_pluie` ; `utility_meter` clé `pluie_semaine` → entité
`sensor.pluie_hebdomadaire` (clé ≠ nom d'entité) ; label `pluie_recente` ambigu entre domaines.

---

## 11. Évolutivité

| Ajout envisagé | Facilité actuelle | Frein |
|---|---|---|
| Nouveau capteur de pluie (2e détecteur, station tierce) | **Moyenne** | Faudrait l'insérer dans `maj_sensor/on` (impératif) et dans `intention_pluie_forte` (Netatmo en dur) séparément ; pas de point de fusion unique |
| Nouvelle source météo de prévision | **Bonne** | `pluie_prevue` isole déjà la prévision derrière une entité ; changer `weather.forecast_maison` reste local |
| Nouveau détecteur (premières gouttes ailleurs) | **Moyenne** | Même limite : pas de couche d'intention abstraite partagée à alimenter |
| Nouvelle stratégie décisionnelle (ex. séjour réagit aux gouttes) | **Faible** | Le séjour est lié en dur au seuil Netatmo ; changer la stratégie touche plusieurs entités hétérogènes |
| Nouveau consommateur (ex. store de terrasse) | **Bonne** si branché sur `pluie_en_cours` ; **faible** s'il lui faut une sémantique fine (intensité, persistance) inexistante |

Le point de friction récurrent : **l'absence d'une autorité d'intention abstraite** oblige
chaque évolution à câbler la source directement chez plusieurs consommateurs.

---

## 12. Points forts

- Couche d'**exécution pure et idempotente** (`volets_fermeture_execute`, `queued`).
- **Normalisation Zigbee** robuste (anti-rebond, impulsion, coupe-circuit) — reconnaît
  l'imperfection du capteur matériel.
- **Honnêteté d'état** des cumuls (0.0 vs unavailable) et de la **prévision** (présomption).
- **Total monotone** propre (jamais de soustraction sur reset).
- **Palmarès contractualisé** (invariants stricts, anomalie structurelle observable,
  REJECT-not-clamp, FIFO ex-æquo).
- **Recorder gouverné** (bloc Population A justifié, sources statistiques préservées).
- **Reprise après redémarrage** pensée de bout en bout.
- **Réaction volets contractualisée + testée en CI**.

---

## 13. Limites & risques (synthèse)

**Limites structurelles**
- Fragmentation sémantique (4 notions de « il pleut », pas d'autorité unique).
- Sécurisation externe appliquée à la mesure, pas à la décision.
- Asymétrie entrée/sortie d'épisode (multi-source à l'entrée, Netatmo seul à la sortie).
- Concepts absents : pluie persistante, intensité intégrée, humidité résiduelle.
- Paradigmes de consolidation mixtes (impératif `pluie_en_cours` vs déclaratif reste).

**Risques**

| Risque | Déclencheur | Effet | Gravité |
|---|---|---|:--:|
| Épisode collant | Netatmo indisponible pendant un épisode | `pluie_en_cours` bloqué `on` | Élevée |
| Fermeture prématurée d'épisode | Bruine SNZB, Netatmo ~0 | Épisode éteint malgré pluie | Moyenne |
| Séjour non protégé | Pluie < 2,5 mm | Volets séjour ouverts | Moyenne |
| Chatter « pluie forte » | Oscillation autour du seuil | Re-notifications / bascules | Faible-Moyenne |
| Chemin rapide muet | Perte SNZB | Détection lente sans alerte | Moyenne |
| Dérive non gardée | Absence de CI sur détection/cumuls/palmarès pluie | Régressions silencieuses | Moyenne |

---

## 14. Opportunités d'amélioration (constats → pistes, sans correctif)

### Robustesse
- **Sécuriser localement les sources de décision** (façade locale conforme à
  `securisation_capteurs_externes.md`), comme déjà fait pour les cumuls.
- **Symétriser entrée/sortie d'épisode** (faire participer le SNZB — ou une fenêtre de grâce
  — à la fin) et **supprimer le risque d'état collant** si Netatmo tombe.
- **Hystérésis** sur « pluie forte » ; **réconciliation multi-source** explicite et tracée.

### Cohérence métier
- Une **autorité d'intention pluie unique** (couche abstraite), graduée (gouttes / pluie /
  forte / terminée), consommée par tous les régimes — le séjour pourrait alors réagir aux
  premières gouttes.
- **Nommer explicitement** « premières gouttes » et lever l'ambiguïté du label `pluie_recente`.
- Étudier les concepts manquants utiles (pluie persistante, **humidité résiduelle** pour
  affiner arrosage/aération après pluie).

### Maintenabilité
- **Checker CI + contrat** pour la production pluie (détection, consolidation, cumuls) et pour
  le **palmarès pluie** (aligner sur le palmarès température, déjà gardé par 3 workflows).
- **Reconnaître (ou documenter l'exclusion de) la précipitation** comme axe du contrat météo.
- Aligner **noms de fichiers/clés ↔ entités**.

### Simplicité
- **Unifier le paradigme** de consolidation (déclaratif recalculable) plutôt qu'un mélange
  impératif/déclaratif.
- **Référentiel unique** des ouvrants exposés à la pluie.

### Valeur fonctionnelle
- **Observabilité de la décision** : exposer la source d'un épisode, notifier la perte du
  chemin rapide et l'inhibition d'arrosage.
- Protéger le **séjour** dès les premières gouttes (dépend de l'autorité d'intention unique).

---

## 15. Recommandations d'architecture (neutres)

1. **Autorité de domaine unique pour la pluie** : une couche d'intention déclarative,
   multi-source, à disponibilité explicite et hystérésis, produisant des états gradués et
   observables — sur le modèle éprouvé du **domaine chauffage** (décision souveraine →
   exécutants bornés).
2. **Découplage décision / matériel** : les consommateurs (volets, aération, arrosage,
   futurs) consomment cette autorité abstraite plutôt qu'un capteur nommé, les sources
   restant interchangeables derrière une façade sécurisée.
3. **Alignement de gouvernance** : contractualiser la production pluie et garder le palmarès
   pluie en CI, pour lever l'asymétrie avec les domaines déjà normés.

Ces directions **prolongent** des principes déjà présents dans Arsenal (sécurisation des
capteurs externes, autorité unique, séparation décision/action, capteurs d'intention).

---

## 16. Conclusion

Le domaine « Précipitations » est **fonctionnellement opérationnel et localement bien
conçu** (exécution idempotente, normalisation Zigbee, honnêteté des cumuls, palmarès
contractualisé, reprise redémarrage). Ses faiblesses sont **architecturales et de
gouvernance**, non fonctionnelles au quotidien : une notion de pluie **fragmentée** sans
autorité unique, une **sécurisation** appliquée à la mesure mais pas à la décision, une
**asymétrie** d'épisode porteuse d'un risque d'état collant, des **concepts absents** (pluie
persistante, humidité résiduelle) et une **couverture contractuelle/CI incomplète** (palmarès
pluie sans checker, production non normée).

La trajectoire d'évolution la plus cohérente avec la doctrine Arsenal serait l'introduction
d'une **autorité d'intention pluie unique et abstraite**, sécurisée et observable, dont
tous les domaines consommateurs dépendraient — sans remettre en cause les couches
d'exécution et de records, déjà saines. Ces éléments sont livrés comme **constats et pistes**,
sans aucun correctif.

---

*Fin de l'audit — lecture seule. Aucun fichier fonctionnel du dépôt n'a été modifié ;
seul le présent rapport documentaire a été créé.*
