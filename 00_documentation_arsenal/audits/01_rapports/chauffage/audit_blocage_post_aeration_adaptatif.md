# 🧠 ARSENAL — RAPPORT D'AUDIT
## Chauffage — Blocage post-aération adaptatif

| Champ | Valeur |
|---|---|
| **Type** | Rapport d'audit (second niveau, ciblé) |
| **Domaine** | Chauffage / Aération / Blocage post-aération |
| **Statut** | ✅ CLÔTURÉ |
| **Version** | 1.0 |
| **Date** | 2026-06-03 |
| **Méthode** | Audit d'architecte sur état réel du dépôt (lecture des contrats `aeration_blocage_chauffage` M0→M6, du contrat `46_aeration_observation_thermique`, des scripts M3/M4, du `recorder.yaml`, traçage des `entity_id`) |
| **Autorité de référence** | Le dépôt. Le runtime fait foi sur le comportement. |
| **Question d'audit** | La couche d'observabilité actuelle constitue-t-elle une base exploitable pour un auto-ajustement fiable du blocage chauffage post-aération ? |

---

## 1. Contexte et objet

Après fermeture des fenêtres, le moteur Chauffage maintient un **blocage temporaire** afin de ne pas relancer la chauffe dans un transitoire d'air froid résiduel. L'objectif décisionnel poursuivi est double et antagoniste : ne pas lever trop tôt (gaspillage / lutte contre un transitoire), ne pas bloquer trop longtemps (sous-chauffe ressentie).

Cet audit détermine si les observations déjà produites par Arsenal suffisent à fonder une **boucle d'auto-ajustement** de la durée de blocage. Il porte **exclusivement** sur ce cas d'usage. Le préchauffage de retour de vacances est hors périmètre.

Le présent rapport ne propose aucun patch, aucun YAML, aucune automatisation. Il statue sur la suffisance des fondations d'observabilité.

## 2. Périmètre

**Inclus :** le pipeline réel de blocage post-aération (`00_documentation_arsenal/contrats/aeration_blocage_chauffage/`, modules M0→M6) ; le contrat d'observation thermique d'aération (`46_aeration_observation_thermique.md`) ; la couche ΔT par zone ; les paramètres gouvernés du barème M3 ; la couverture `recorder.yaml` des signaux d'épisode ; l'utilité éventuelle des 13 capteurs diagnostiques thermiques (`15_capteurs/08–11`) pour ce cas d'usage.

**Exclus :** préchauffage vacances ; audit général du moteur Chauffage ; gouvernance, CI et conformité documentaire en tant que telles ; sûreté de la couche d'exécution (boiler bridge), non rouverte ici.

## 3. Constats — architecture réelle du blocage (état du dépôt)

> **Constat fondateur (C-1) — Le blocage post-aération n'est pas statique.** Seule la durée *initiale* est fixe. Le pipeline réalise déjà une **adaptation feed-forward** au déficit thermique observé, via les modules M1→M6.

Chaîne réelle, par module :

- **M1 — Début d'épisode.** Fige les snapshots de référence thermique `T_REF` par zone à l'ouverture, et horodate l'épisode.
- **Couche ΔT (observation).** Capteurs `sensor.deltat_entree`, `deltat_sejour`, `deltat_chambre_arnaud`, `deltat_chambre_matthieu`, `deltat_chambre_parents`, `deltat_palier`, définis comme `max(T_REF_M1 − T_courante, 0)` : numériques, jamais négatifs, **monotones croissants**, robustes aux silences capteurs. Implémentés dans `12_template_sensors/aeration/delta_t_piece.yaml`.
- **Contrat 46 — Observation thermique.** Couche de vérité physique : valide qu'un épisode réel produit une chute `≥ ΔT_min_physique = 0.2 °C` dans la fenêtre `[10 min ; 30 min]` après fermeture ; neutralise les **épisodes zombies** (ouverture fantôme, capteur figé). En cas d'incohérence, l'épisode est invalidé et le blocage neutralisé. Ce contrat **ne décide rien**.
- **M2 — Programmation des délais.** Définit le blocage initial = `input_number.delai_stabilisation_capteurs + 1 min`, et programme deux échéances (`timer.aeration_analyse_delta_t`, `timer.aeration_blocage`) avec **monotonicité stricte** : un timer actif n'est jamais raccourci, les cibles `input_datetime` ne reculent jamais. Post-reboot safe.
- **M3 — Analyse ΔT (cœur adaptatif).** Déclenché **une seule fois** sur `timer.finished` (analyse), fenêtres fermées. Calcule `delta_max = max` des 6 capteurs ΔT (maximum simple, aucun lissage, aucune moyenne). Applique une **table de décision par paliers** sur paramètres gouvernés : `< seuil_tiny → 0` ; `< seuil_medium → prolongation_tiny` ; `< seuil_high → prolongation_medium` ; `sinon → prolongation_high`. Fallbacks contractuels : `0.4 / 0.8 / 1.2 °C → 60 / 120 / 180 min`. Publie le diagnostic `input_number.delta_t_max_decisionnel_aeration`. Route vers prolongation (extension **monotone**, jamais de réduction) ou maintien. M3 ne lève jamais le blocage.
- **M4 — Fin de blocage.** Déclenché sur `timer.finished` (blocage). Levée **purement horaire** : à l'expiration du timer (éventuellement prolongé), lève le blocage, annule les timers, neutralise les traces datetime, désarme le pipeline. **Unique mécanisme de levée.**
- **M5 / M6 — Réouverture / refermeture.** Une réouverture pendant blocage gèle les timers et neutralise M3 sans altérer les cibles monotones ; la refermeture stable réarme l'exécution.
- **M0 — Remédiation.** Traite le blocage orphelin / incohérent.

> **Constat (C-2) — La levée est en boucle ouverte temporelle.** Le blocage tombe à l'échéance d'un timer, **non** en fonction d'une récupération thermique réellement constatée. La seule rétroaction physique du pipeline est l'**extension** feed-forward de M3, calculée une fois.

> **Constat (C-3) — Le barème M3 est figé et météo-aveugle.** La transformation `déficit → durée` est une fonction en escalier à trois paliers, à paramètres réglés à la main. Aucune dépendance à la température extérieure ni à la dynamique de récupération.

> **Constat (C-4) — Écart de périmètre zones.** Le contrat 46 autorise 5 zones thermiques ; M3 agrège 6 capteurs ΔT (ajout de `deltat_palier`). Écart factuel mineur, sans effet de sûreté, mais à tracer.

## 4. Constats — substrat d'observation réellement disponible

> **Constat (C-5) — Les 13 capteurs diagnostiques thermiques n'observent pas l'aération.** Par contrat (`15_capteurs/08–11`), ils sont **invalidés pendant l'épisode** (`aeration_pipeline_arme = on` les neutralise) et sont **mono-zone** (`sensor.temperature_min_chambres`). Ils décrivent la dynamique *intrinsèque* du bâtiment en cycles présence **propres**, pas le transitoire d'aération.

> **Constat (C-6) — Le substrat pertinent est la couche ΔT d'aération**, distincte des 13 : multi-zone, monotone, spécifiquement ancrée sur le déficit causé par l'aération. C'est elle, et le diagnostic `delta_t_max_decisionnel_aeration`, qui portent l'information utile au blocage.

> **Constat (C-7) — Aucune historisation des signaux d'épisode.** Vérifié sur `recorder.yaml` (liste blanche explicite) : sont **absents du recorder** : les 6 `sensor.deltat_*`, `input_number.delta_t_max_decisionnel_aeration`, `input_datetime.chauffage_fin_blocage_aeration`, `input_number.delai_stabilisation_capteurs`. Sont également absents (cf. audit de niveau 1) : `sensor.vitesse_reprise_presence_chambres`, `sensor.vitesse_refroidissement_presence_chambres`, `sensor.temperature_reprise_presence_chambres`.

> **Constat (C-8) — Aucune métrique d'issue.** Aucun capteur ne mesure, après la levée, si la pièce a récupéré le confort en temps acceptable et sans surchauffe. Il n'existe donc aucune définition *mesurée* d'un « bon » blocage. Aucune métrique d'énergie ni de duty-cycle n'existe par ailleurs.

## 5. Analyse — trois régimes à distinguer

| Régime | Définition | État dans Arsenal |
|---|---|---|
| **Blocage statique** | Durée fixe, indépendante du comportement thermique observé | **Non.** Seul le *seed* initial (`delai_stabilisation + 1 min`) est fixe. |
| **Blocage adaptatif actuel** | Feed-forward : déficit observé `ΔT_max` → table de paliers → extension monotone ; levée horaire | **Oui, en production** (M1→M6). Boucle ouverte, décision unique par épisode, extension seulement. |
| **Auto-ajustement apprenant (futur)** | Boucle fermée : le système ajuste lui-même son barème à partir des *issues* observées sur de nombreux épisodes | **Non réalisable aujourd'hui.** Manque le signal d'issue (C-8) et l'historique d'épisodes (C-7). |

**Analyse.** Le saut conceptuel demandé ne porte pas du « statique » vers l'« adaptatif » — ce saut est déjà fait. Il porte de l'**adaptatif feed-forward à paramètres figés** vers l'**auto-ajustement apprenant**. Or un mécanisme ne peut régler automatiquement une décision dont il ne mesure jamais le résultat. L'obstacle n'est ni algorithmique ni théorique : il est **observationnel**.

## 6. Analyse — utilité des 13 capteurs diagnostiques pour ce cas d'usage

| Capteur | Pertinence | Justification factuelle |
|---|---|---|
| `vitesse_reprise_presence_chambres` | Indirecte (prior) | Vitesse de remontée à la reprise → dimensionner le blocage pour que la récupération post-levée arrive à l'heure utile. Mesuré hors aération, **non recordé**. |
| `vitesse_refroidissement_presence_chambres` | Indirecte faible | Perte *passive* (conduction). L'aération est une perte *convective* forcée → régime physique différent. Mono-zone, non recordé. |
| `duree_chute_reprise` / `amplitude_chute_reprise` | Indirecte faible | Latence / erreur initiale de reprise ; apport marginal au dimensionnement. |
| `temperature_plancher_absence` | Très indirecte | Plancher passif ; tangent au transitoire d'aération. |
| `amplitude_oscillation_cycle`, `duree_cycle_moyenne`, `nombre_cycles_jour` | Nulle | Cinématique d'hystérésis en régime établi, sans rapport avec un transitoire. |
| `temperature_arret`, `amplitude_overshoot_arret`, `duree_overshoot_arret` | Nulle | Physique post-arrêt d'un cycle normal, pas un événement d'aération. |

**Analyse.** Au mieux deux à quatre des treize capteurs ont une valeur de *prior* faible ; aucun n'observe directement l'épisode. La valeur décisionnelle de ce cas d'usage **ne réside pas dans les 13 capteurs diagnostiques** mais dans la couche ΔT d'aération.

## 7. Analyse — stratégies envisageables et confiance atteignable

| Stratégie | Avantages | Limites | Confiance |
|---|---|---|---|
| **(a) Feed-forward ΔT (l'existant, M3)** | Déterministe, robuste, déjà en place ; biais sécuritaire (extension seulement) | Barème figé, décision unique, aucune rétroaction, météo-aveugle | **Moyenne** |
| **(b) Levée sur décroissance du ΔT** | Ferme la boucle sur le transitoire réel ; les `deltat_*` restent vivants pendant le blocage (fenêtres fermées) | Distinguer « déficit qui retombe » de « toujours froid » ; dépendance météo ; non prouvé sans historique | **Moyenne** (meilleure base fermée disponible) |
| **(c) Prior vitesse de refroidissement** | Réutilise un capteur existant | Mauvais régime physique, mono-zone, non recordé | **Faible** |
| **(d) Dimensionnement par vitesse de reprise** | Adresse directement la sous-chauffe ressentie | Capteur invalidé pendant l'aération, non recordé, hors régime | **Faible** |
| **(e) Énergie thermique perdue (∫ΔT·dt)** | Invariant physique le plus propre | **Aucune métrique d'énergie ni de duty-cycle dans le dépôt** | **Non atteignable** |
| **(f) Apprentissage supervisé hors-ligne du barème** | Potentiel élevé, gouvernable | Nécessite d'abord de **constituer le jeu d'épisodes** (inexistant) | **Faible aujourd'hui / élevée une fois instrumenté** |

**Analyse.** Le plafond de confiance commun à toutes les stratégies tient à trois causes observationnelles : absence de signal d'issue, absence d'historique, absence de normalisation météo.

## 8. Limitations d'observabilité

1. **Cécité de l'issue.** Le pipeline ne mesure jamais l'effet de sa propre décision : aucun observable ne relie « durée appliquée » à « qualité de récupération après levée » (C-8).
2. **Levée non observée.** M4 lève sur horloge ; la trajectoire du ΔT pendant le blocage (signal pourtant vivant) n'est pas exploitée comme critère de levée (C-2).
3. **Non-persistance.** Les signaux d'épisode ne sont pas historisés (C-7) : aucune trace longitudinale ne survit à l'épisode, donc aucune corrélation rétrospective possible.
4. **Réduction scalaire.** La richesse multi-zone de la couche ΔT est réduite à un `max` unique en M3 : le ciblage par zone est perdu au moment de la décision.
5. **Absence de normalisation.** Le ΔT auto-normalise la *référence* de départ, mais la *récupération* reste confondue avec la météo extérieure, faute de grandeur de normalisation.
6. **Non-pertinence des diagnostiques présence.** Les capteurs censés décrire la thermique du bâtiment sont, par construction, aveugles pendant l'aération (C-5).

## 9. Informations manquantes

**Bloquant** (interdit toute boucle apprenante) :
- Historisation des signaux d'épisode : `delta_t_max_decisionnel_aeration`, `chauffage_fin_blocage_aeration`, les 6 `sensor.deltat_*`. Sans dataset d'épisodes, aucun apprentissage.
- Métrique d'issue de récupération liée à l'épisode. Sans définition mesurée du « bon blocage », rien à optimiser.

**Important** (plafonne la confiance) :
- Historisation de `vitesse_reprise` et `vitesse_refroidissement` (priors indisponibles).
- Normalisation ΔT intérieur/extérieur (temps de récupération confondu avec la météo).
- Observation de récupération propre à l'aération (les capteurs de reprise sont invalidés pendant l'épisode).

**Confort** (qualité décisionnelle) :
- Conservation de la dimension par zone au-delà du `max` M3.
- Exposition de la corrélation « déficit ↔ durée appliquée ↔ issue » pour analyse humaine.

**Corrélations aujourd'hui impossibles :** « déficit observé → durée de blocage → récupération obtenue » ; « durée de blocage → surchauffe/sous-chauffe constatée » ; « comportement par zone → décision par zone ». Toutes requièrent l'historique et la métrique d'issue ci-dessus.

## 10. Verdict

- La couche d'observabilité actuelle **est déjà une base exploitable pour un blocage adaptatif feed-forward** — elle l'est en production, via M1→M6, avec un biais sécuritaire (extension monotone, jamais de raccourcissement).
- La couche d'observabilité actuelle **n'est pas une base suffisante pour un auto-ajustement fiable et auto-apprenant.**
- Le manque déterminant n'est **ni un modèle, ni un algorithme** : ce sont deux observations à instaurer en amont — **l'historisation des épisodes** et **une métrique d'issue de récupération**. Tant qu'elles n'existent pas, toute boucle apprenante apprendrait dans le vide.
- Risque de l'existant : **faible** (l'extension seulement ne peut sur-lever ; son biais est le sur-blocage, pas la surchauffe). Toute boucle qui se mettrait à **raccourcir** introduirait un risque de sous-blocage et devrait être bordée.
- Précision actuelle : **grossière** (barème à trois paliers, décision unique, météo-aveugle) — suffisante pour « ne pas chauffer dans un transitoire d'air froid », insuffisante pour une optimisation fine.

## 11. Suites possibles

Orientations d'observabilité, classées par valeur / coût. Aucune ne constitue une prescription d'implémentation ; toutes restent subordonnées à validation humaine et mise à jour contractuelle.

1. **Instaurer l'historisation des épisodes** (ΔT décisionnel, durées de blocage, ΔT par zone). Prérequis absolu de toute suite ; coût faible (couverture recorder). *Sans cela, les points suivants sont inatteignables.*
2. **Définir une métrique d'issue de récupération** rattachée à l'épisode (qualité de retour au confort après levée, sans surchauffe). Fonde la notion de « blocage correct ».
3. **Évaluer une levée sur décroissance du ΔT** (stratégie b) comme évolution de M4, en complément du garde-fou horaire : seule voie, avec l'existant, pour réduire le sur-blocage sans nouvelle instrumentation — sous réserve d'un garde-fou anti-sous-blocage.
4. **Historiser les priors** `vitesse_reprise` / `vitesse_refroidissement` si une approche modèle est envisagée.
5. **Introduire une normalisation météo** pour rendre les récupérations comparables d'un épisode à l'autre.
6. **Constituer, une fois 1 et 2 en place, un jeu d'épisodes** permettant un réglage supervisé hors-ligne du barème M3 (stratégie f) — étape où l'« auto-ajustement apprenant » devient réellement envisageable.
7. **Aligner le périmètre zones** entre le contrat 46 (5 zones) et l'agrégat M3 (6 zones) — correction documentaire mineure (C-4).

---

*Fin du rapport.*
