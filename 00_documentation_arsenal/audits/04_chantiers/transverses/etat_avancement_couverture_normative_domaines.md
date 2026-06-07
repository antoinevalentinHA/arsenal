# Rapport d’avancement — Chantier « Couverture normative des domaines »

- **Périmètre :** suites de l’audit [`etat_couverture_normative_domaines.md`](etat_couverture_normative_domaines.md) (couverture normative des domaines fonctionnels).
- **Référence (photographie figée) :** l’audit initial, observé sur `main` @ `20d909df` (2026-06-07). Ce rapport d’audit **n’est pas réécrit** : il reste une photographie d’état opposable.
- **Statut :** point d’étape consolidé — **2 points P1 traités**, **5 P2 traités** (`sante/sommeil.md`, `meteo/fallback.md`, `meteo/extrema_jour_courant.md`, `electromenager`, `poele`), **1 P3 traité** (`sante/cardio_nuit.md`), **1 divergence fermée** ; **plus aucun P2 ouvert** — chantier **toujours ouvert** sur les **P3–P4** restants.
- **Méthode :** suites documentaires par patches atomiques validés CI (lint `docs_lint`). Aucun chantier métier nouveau ouvert ; aucune modification du runtime, des scripts ou des dashboards.

---

## 1. Périmètre et rattachement

L’audit `etat_couverture_normative_domaines.md` est une **photographie d’état** datée et épinglée à un commit. Pour préserver sa valeur d’opposabilité, il ne doit pas être édité au fil des corrections.

Ce document est le **point d’étape vivant** qui lui est rattaché, dans le même dossier `04_chantiers/transverses/`, suivant la convention déjà employée pour le chantier voisin [`etat_avancement_chantier_navigation_documentaire_contrats.md`](etat_avancement_chantier_navigation_documentaire_contrats.md). Il consigne : ce qui a été réalisé depuis l’audit, ce qui reste ouvert, et le prochain ordre de traitement. Il a vocation à être mis à jour, puis **clôturé** dans `05_clotures/` une fois le backlog résorbé.

## 2. Évolutions réalisées depuis l’audit

### 2.1 P1 — fichier vide trompeur `05_capteurs_parametrage_canonique.md` → contrat normatif

- **Constat audit (P1) :** `contrats/chauffage/15_capteurs/05_capteurs_parametrage_canonique.md` réduit à un titre (38 o, 1 ligne), donnant une fausse impression de couverture.
- **Réalisé :** réécriture en **contrat normatif complet** — frontière d’autorité « Paramétrage canonique » (références thermiques métier durables : consignes confort / réduite / vacances), entités et bornes ancrées sur `03_input_numbers/chauffage/consignes.yaml` et le registre, distinction explicite norme (contrat) / preuve d’exposition (dashboard `reglages/chauffage.yaml`).
- **Trace :** commit `bb50e76d` (`docs(chauffage): document canonical sensor parameterization`).
- **Statut :** **P1 clos.**

### 2.2 Divergence `input_number.chauffage_consigne_reduite_sauvegarde` — fermée

- **Constat audit / contrat 05 :** slot de sauvegarde réel présent dans `consignes.yaml`, absent de la section `parametres:` du registre et non exposé au dashboard ; laissé « à aligner ».
- **Réalisé :** entité **alignée** dans `contrats/chauffage/ci/registres_entites.yaml` (`role: parametre`, `exclus_invariants_registre`, contrat causal `66_adaptation_consigne_vacances.md`) ; **contrat 05 ajusté** pour acter l’alignement tout en maintenant le slot **hors** population canonique des références de régime (mémoire interne, non surface de réglage).
- **Traces :** commits `2a9bef67` (`align reduced setpoint backup registry`) et `1984ce09` (`mark reduced setpoint backup as registry-aligned`).
- **Statut :** **divergence close** côté registre **et** contrat.

> Note : l’indexation du rapport d’audit lui-même (gate orphelin DOC-CI-3) a été corrigée par le commit `879eb4a0`.

### 2.3 P1 — domaine `reveils` / `babyphone` non documenté → contrat normatif

- **Constat audit (P1) :** domaine runtime actif (`11_automations/reveils/` : compteurs, babyphone, reset, par enfant) sans aucune documentation normative dans `contrats/`.
- **Réalisé :** création du contrat plat racine `contrats/reveils.md` (référencé dans `contrats/index.md`), à partir du runtime observé, sans entité ni règle inventée. Distinction nette : compteurs nocturnes = **observabilité** (pas une preuve de réveil réel) ; reset = **cycle de vie** ; babyphone = **notification opt-in expérimentale et non garantie** (capteurs Netatmo insuffisamment réactifs ; **aucun invariant de surveillance fiable** ; jamais un service opposable). Destinataire documenté = celui observé (chemin canonique existant), sans destinataire configurable inventé.
- **Traces :** commits `9c58fd00` (`docs(reveils): add nocturnal wake-ups contract`) et `3d6b52a6` (`docs(contrats): index reveils contract`).
- **Statut :** **trou documentaire P1 clos.** Les **dettes runtime et arbitrages** consignés dans `reveils.md` §7 (`DETTE-REV-1` fallback `float(0)` du babyphone, `DETTE-REV-2` historique/compteur, `DETTE-REV-3` reset en fenêtre nocturne, `ARB-REV-1` Vacances/Babysitting, `ARB-REV-2` qualification du babyphone) **restent ouverts** — ce sont des dettes / arbitrages, pas un trou de couverture documentaire.

### 2.4 P2 — `sante/sommeil.md` draft v0.9 → contrat normatif v1.0 (aligné runtime)

- **Constat audit (P2) :** contrat existant en statut `v0.9 (draft, non validé)`, **périmé/divergent** : entités fictives (`*_phase_local`, `sommeil_total_calcule`, `*_statistique`, garde `sommeil_derniere_consolidation`), entités réelles non documentées (gate, total_local, snapshot helpers, moyennes, nuit manquante).
- **Réalisé :** **réécriture alignée sur le runtime réel** puis promotion en **v1.0 normatif**. Aucune entité inventée, aucune entité fictive conservée. Documentés : vrai pivot `sensor.withings_sommeil_total_local` + gate `binary_sensor.sommeil_donnees_exploitables` ; snapshot **helpers** `input_*.sommeil_derniere_nuit_*` ; `binary_sensor.sommeil_derniere_nuit_valide` ; consolidation `10200000000003` (09/10/11h, garde `date != today`, double validation) ; nuit manquante `10200000000004` ; moyennes glissantes `sommeil_{total,score}_moyenne_{7,14,30}j` (explicitement ≠ valeurs de nuit). Runtime non modifié.
- **Trace :** commit `d78dacd5` (`docs(sante): rewrite sleep contract from runtime`).
- **Statut :** **P2 traité — contrat figé v1.0.** Les **limites runtime connues** consignées dans le contrat (`DETTE-SOM-1` agrégat `float(0)`, `DETTE-SOM-2` fallback cache au démarrage, `DETTE-SOM-3` double représentation du texte, `DETTE-SOM-4` libellé interne « Couche 2 ») **restent ouvertes** comme limites/dettes runtime, pas comme trou de couverture documentaire.

### 2.5 P2 — `meteo/fallback.md` stub de continuité → contrat normatif v1.0 (consolidé runtime)

- **Constat audit (P2) :** `fallback.md` était un **stub de continuité** (« contenu normatif détaillé reste à consolider ») alors qu'il est le **centre porteur** du domaine météo — `gouvernance.md` lui délègue **exclusivement** la continuité (hiérarchie des sources, mémoire, TTL, abstention), `validation.md` §6 et `meteo.md` y renvoient. Centre structurellement creux.
- **Réalisé :** **consolidation depuis le runtime réel** (chaîne canonique `humidite_relative/jardin` + variantes température jardin / intérieur multi-capteurs) puis promotion en **v1.0 normatif**. Formalisés sans invention : hiérarchie des niveaux (sources validées → cible robuste → mémoire de continuité → abstention), TTL (`TTL_DEFAULT = 30 min`, `TTL_override` par axe, double TTL intérieur signalé), qualification du statut, interdictions, séparation validation/fallback/gouvernance/axes. Runtime non modifié ; **aucun contrat voisin repointé** (aucune incohérence de lien trouvée).
- **Trace :** commit `1d82dbb9` (`docs(meteo): consolidate fallback contract from runtime`).
- **Statut :** **P2 traité — contrat figé v1.0.** Les **limites runtime connues** (`DETTE-FB-1` nommage mémoire par axe non uniforme, `DETTE-FB-2` TTL exprimé en min vs s, `DETTE-FB-3` vocabulaire de statut par axe) **restent ouvertes** comme dettes runtime, pas comme trou de couverture documentaire.

### 2.6 P2 — `meteo/extrema_jour_courant.md` pré-normatif v0.1.0 → contrat normatif v1.0 (famille implémentée)

- **Constat audit (P2) :** pré-contrat **contract-first** (v0.1.0, « pré-normatif — à figer **avant toute phase d'implémentation** »). L'audit d'origine prévoyait « promouvoir en v1.0 **après/pendant l'implémentation** ».
- **Réalisé :** la famille « extrema du jour civil en cours » (12 zones × min/max) est **désormais implémentée** au runtime et **conforme aux invariants `INV-JC-*`** (reset minuit strict `10160000000034`, sentinelles `999`/`-999`, plage `[5,45]°C`, monotonicité stricte `10160000000032`/`33`, Jardin en lecture seule, exposition `unavailable` sur sentinelle). **Promotion en v1.0 normatif** avec retrait du cadrage « pré-contrat / avant implémentation ». Runtime, `statistics`, dashboards et CI non modifiés.
- **Trace :** commit `7b5b1e44` (`docs(meteo): promote current-day extrema contract to v1.0`).
- **Statut :** **P2 traité — contrat figé v1.0.** La **dette de migration `DETTE-JC-1`** (branche glissante 24 h `temperature_*_jour_<zone>` encore présente au runtime, **hors source canonique**, retrait effectif non réalisé) **reste ouverte** dans le contrat — **aucun chantier runtime ouvert**, aucun `statistics` supprimé.

### 2.7 P2 — `electromenager` domaine actif non documenté → contrat plat racine normatif

- **Constat audit (P2) :** domaine runtime actif (détection de cycle lave-vaisselle + buanderie via prises connectées, flags `input_boolean.*_cycle`, notifications) **sans aucune documentation**.
- **Réalisé :** **création** du contrat plat racine `contrats/electromenager.md` (v1.0 normatif, documenté depuis le runtime : détection début/fin par puissance, fenêtre de confirmation anti-reprise, notifications persistante + mobile, écrivain souverain par flag) **à portée volontairement restreinte** (deux appareils réellement implémentés, **pas** un contrat « électroménager » général ; aucun pilotage, aucun usage `energy`/`linkquality` comme source). **Indexation** dans `contrats/index.md` (rubrique « Énergie et équipements »). Runtime, dashboards et CI non modifiés.
- **Traces :** commits `b8d36717` (`docs(electromenager): add appliance-cycle contract from runtime`) et `a05242f7` (`docs(contrats): index electromenager contract`).
- **Statut :** **P2 traité — domaine documenté et indexé.** Observations consignées dans le contrat (`DETTE-EM-1` seuils asymétriques par appareil, `OBS-EM-1` flags sans consommateur aval) — observations, pas trou de couverture.

### 2.8 P2 — `poele` domaine actif sans contrat souverain → contrat souverain plat racine

- **Constat audit (P2) :** domaine actif et **transverse** (apport thermique exogène : détection, mémoire 24 h, blocage chauffage **et** climatisation HEAT), **couvert seulement indirectement** côté chauffage (2 contrats capteurs de détection), **sans contrat souverain**.
- **Réalisé :** **création** du contrat souverain plat racine `contrats/poele.md` (v1.0 normatif, documenté depuis le runtime : mémoire 24 h `poele_recent`/`timer.poele_24h`, blocage chauffage+clim synchrone, ajustement de durée, sécurité démarrage, effets transverses chauffage décision + courbe et climatisation HEAT, écrivain souverain par flag). **Détection laissée souveraine** aux contrats capteurs chauffage (`signature_thermique_poele.md`, `poele_en_fonction.md`) via **renvoi**, sans déplacement ni duplication. **Indexation** dans `contrats/index.md` (rubrique « Environnement physique et sécurité », libellé transverse). Runtime, contrats chauffage, climatisation, dashboards et CI non modifiés.
- **Traces :** commits `df0e0bf2` (`docs(poele): add sovereign stove domain contract from runtime`) et `3b92eb8a` (`docs(contrats): index poele contract`).
- **Statut :** **P2 traité — domaine souverain documenté et indexé.** Observations consignées dans le contrat (`OBS-POELE-1` fichier timer mal nommé, `OBS-POELE-2` blocage chauffage/clim synchrone) — observations, pas trou de couverture.

**➡️ Tous les P2 sont désormais traités. Aucun P2 ouvert ne subsiste.**

### 2.9 P3 — `sante/cardio_nuit.md` statut périmé + renvois morts → contrat promu normatif

- **Constat audit (P3) :** contrat complet mais **statut périmé** (`READY FOR IMPLEMENTATION`, v2.0.2) alors que le domaine **est implémenté et conforme** au runtime (consolidation, capteurs métier, snapshot, couleur) ; **deux renvois hérités morts** : `CONTRAT_SOMMEIL_NUIT.md` (fichier inexistant) et `CONTRAT_ALERTE_SANTE.md` (« à créer », jamais créé ; affirmation de couverture fausse).
- **Réalisé :** **promotion** du contrat en **v2.1 — NORMATIF (implémenté)** après vérification de conformité (toutes les entités citées existent au runtime) ; renvoi sommeil corrigé vers `sommeil.md` ; renvoi d'alerte santé retiré (alerte santé **hors périmètre et non contractualisée à ce jour** — aucun domaine ni contrat d'alerte créé). **Navigation santé alignée** (`navigation/domaines/sante.md` : 4 mentions cardio_nuit relabellisées). Aucune règle ni entité modifiée ; runtime, dashboards et CI non touchés.
- **Traces :** commits `3a2e71c9` (`docs(sante): clarify cardio_nuit status and fix dead references`) et `37a94cee` (`docs(nav): mark cardio contract normative in sante hub`).
- **Statut :** **P3 traité — statut figé v2.1 normatif, renvois assainis, nav cohérente.** L'alerte santé reste explicitement hors périmètre — pas de domaine ouvert, pas de surpromesse.

## 3. Reste ouvert — backlog de couverture normative

Les éléments ci-dessous restent ouverts ; ils renvoient aux listes compactes `DOMAINES_NON_DOCUMENTES`, `CONTRATS_DRAFT_OU_NON_NORMATIFS` et `FICHIERS_VIDES_OU_PLACEHOLDERS` de l’audit, qui demeurent la source détaillée.

| Priorité | Élément | Nature | État |
|---|---|---|---|
| P1 ✅ | `reveils` / `babyphone` | domaine désormais **documenté** (`contrats/reveils.md`, indexé) | **traité — trou documentaire P1 clos** ; dettes runtime/arbitrages suivies dans `reveils.md` §7 |
| P2 ✅ | `electromenager` | contrat plat racine créé + indexé (`b8d36717`, `a05242f7`) | **traité — documenté** (détection cycle + notification, périmètre restreint à 2 appareils) |
| P2 ✅ | `poele` | contrat souverain plat racine créé + indexé (`df0e0bf2`, `3b92eb8a`) | **traité — domaine souverain** (transverse chauffage + climatisation) ; détection déléguée aux capteurs chauffage |
| P2 ✅ | `sante/sommeil.md` | réécrit **v1.0 normatif** aligné runtime (`d78dacd5`) | **traité — figé v1.0** ; limites runtime (`DETTE-SOM-1..4`) suivies dans le contrat |
| P2 ✅ | `meteo/extrema_jour_courant.md` | promu **v1.0 normatif** (famille implémentée, `7b5b1e44`) | **traité — figé v1.0** ; `DETTE-JC-1` (glissante 24 h résiduelle) suivie dans le contrat, sans chantier runtime |
| P2 ✅ | `meteo/fallback.md` | consolidé **v1.0 normatif** depuis runtime (`1d82dbb9`) | **traité — figé v1.0** ; dettes runtime (`DETTE-FB-1..3`) suivies dans le contrat |
| P3 | `chauffage/15_capteurs/12_capteurs_observabilite_pure.md` | stub déclaré vide | ouvert |
| P3 | `deshumidificateur/guard.md` (§12) | helpers diagnostiques « à créer » | ouvert |
| P3 ✅ | `sante/cardio_nuit.md` | promu v2.1 normatif + renvois assainis + nav alignée (`3a2e71c9`, `37a94cee`) | **traité** |
| P3 | `couleurs`, `boutons`, `statistiques` | rattachement à clarifier (architecture/UI vs contrat) | ouvert |
| P4 | `modes/normal` | renvoi à acter depuis `vacances.md` | ouvert |

> Les dettes/arbitrages de `reveils.md` §7 ne figurent pas dans ce backlog de **couverture documentaire** : ce sont des dettes runtime / arbitrages métier, suivies dans le contrat lui-même. Le domaine `reveils` n’est plus un trou de couverture.

## 4. Prochain ordre de traitement

1. **P2 — contrats draft à figer : fait** — `sante/sommeil.md` (v1.0), `meteo/fallback.md` (v1.0), `meteo/extrema_jour_courant.md` (v1.0). Dette résiduelle `DETTE-JC-1` (glissante 24 h) suivie dans le contrat, **sans chantier runtime**.
2. **P2 — domaines à documenter : fait** — `electromenager` et `poele` documentés + indexés. **Plus aucun P2 ouvert.**
3. **P3 — consolidations :** `deshumidificateur/guard.md §12`, arbitrage `12_capteurs_observabilite_pure.md`, clarification `couleurs` / `boutons` / `statistiques`. *(`sante/cardio_nuit.md` — statut + renvois + nav — fait.)*
4. **P4 — `modes/normal` :** renvoi depuis `vacances.md`.

> Tous les P1 et **tous les P2** de l’audit sont traités : P1 (`05_capteurs_parametrage_canonique.md`, `reveils`/`babyphone`) ; P2 (`sante/sommeil.md`, `meteo/fallback.md`, `meteo/extrema_jour_courant.md` en v1.0 ; `electromenager` et `poele` en contrats racine). **Le backlog restant ne comporte plus que des P3 et un P4** ; le premier P3 (`sante/cardio_nuit.md`) est traité, le chantier global **reste ouvert**.

Chaque suite suit le même principe : patch documentaire / registre atomique, validé CI, sans toucher au runtime, et **sans rouvrir l’audit figé**.

## 5. Portée et invariants de ce suivi

- L’audit initial n’est **pas modifié** (photographie d’état épinglée).
- Ce document est le **point d’étape** rattaché ; il est vivant et sera clôturé dans `05_clotures/` lorsque le backlog P1–P4 sera résorbé.
- **Aucun chantier métier nouveau** n’est ouvert : les suites sont strictement documentaires et de registre.
- Source de détail des éléments ouverts : les listes compactes de l’audit, non recopiées ici pour éviter toute divergence.

## 6. Point de gouvernance CI (signalé — non corrigé)

Le traitement de `reveils` a fait apparaître une **faiblesse possible de la CI documentaire**, à confirmer : un **contrat plat racine** (ex. `contrats/reveils.md`) **semble pouvoir être ajouté sans être référencé** dans `contrats/index.md` sans déclencher de gate, car **DOC-CI-2** paraît ne contrôler que les **lignes de dossiers** de l’index (`[domaine/](…)`) et **DOC-CI-3** ne couvre que l’arborescence `audits/`. Ici, l’indexation a été faite volontairement (commit `3d6b52a6`), mais rien ne l’imposait.

- **Portée :** ce point relève de la **gouvernance documentaire / CI**, distincte du présent chantier de couverture normative ; il est donc à rattacher aux **suites de gouvernance documentaire** (famille du chantier `cloture_chantier_documentaire_2026_06_06.md`), pas à ce backlog.
- **Statut :** **signalé uniquement**, **non corrigé** ; aucune modification de la CI dans le patch courant. Formulation prudente : l’existence exacte et la portée du trou restent **à qualifier** avant toute décision.
- **Recommandation :** inscrire au backlog de gouvernance documentaire un item « qualifier puis, si confirmé, étendre un gate d’indexation aux contrats plats racine », sans préjuger de la solution.
