# ⚡ ARSENAL — AUDIT MÉTIER — Mode panne secteur : pertinence des actions déclenchées

> **Trace d'audit documentaire.** Aucune correction runtime dans cette passe : ni automation, ni template, ni script, ni Lovelace modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse · **[RECO]** recommandation.
> Audit frère (détection) : [`audit_panne_detection_coupure_secteur.md`](audit_panne_detection_coupure_secteur.md).

---

## Verdict

La **détection** est désormais correcte (correction P0 du témoin canonique appliquée — `binary_sensor.coupure_secteur` requalifié sur UPS/Bluetti). Mais les **actions déclenchées en aval restent non contextualisées** : l'entrée en mode panne force `input_boolean.mode_confort_chauffage = on` **et** une consigne **ECS 45 °C**, de façon **inconditionnelle**, sans lire la **saison**, la **température**, le **SOC batterie**, la **présence/vacances** ni la **durée**.

**Contradiction doctrine ↔ runtime (cœur du constat) :** l'architecture assigne au mode dégradé un objectif de **sobriété** pour économiser les batteries (`infrastructure_puissance.md:16-20`). Or la réponse n'est pas gardée par le contexte. Il faut distinguer les deux volets, qui n'ont pas le même poids énergétique :

- **ECS 45 °C** — **consommation réelle sur batterie**, en toute saison, sans veto SOC ni durée. C'est le point qui contredit concrètement la sobriété.
- **Chauffage confort** — **signal forcé non gardé**. La consigne confort est basse (input_number `chauffage_consigne_confort`, plage **17–25 °C**, ~19 °C typique) : en hiver c'est une consommation réelle mais défendable ; en été l'ambiance dépasse la consigne, donc **probablement inerte** (aucune demande de chaleur). Le défaut est l'**absence de contextualisation**, pas un drain estival.

**Gravité de fond : P0 (conception métier)** — la doctrine doit être tranchée avant tout correctif runtime.

---

## Contexte

Cette passe est la suite de l'audit détection. La correction P0 de la détection a été appliquée (runtime, commit `f963128`) ; le présent audit ne porte **pas** sur la détection mais sur la **pertinence métier** de ce qui se déclenche une fois la coupure qualifiée.

---

## Faits observés — chaîne d'actions

**[FAIT] Réflexe fixe à l'entrée.** `11_automations/panne/secteur/activation_mode_panne.yaml:131-141` : `turn_on` `panne_secteur_active`, `turn_on` `mode_confort_chauffage`, puis appel `script.mode_panne_coupure_secteur`. Le script `10_scripts/system/coupure_secteur.yaml:82-85` applique **ECS `target_temp: 45` / `consigne_haute`**. Aucune lecture de contexte n'encadre ces actions.

**[FAIT] Contradiction avec l'intention d'architecture.** `00_documentation_arsenal/architecture/infrastructure_puissance.md:16-20` : en mode dégradé, objectif = *« passer le chauffage en mode "Sécurité" ou "Sobriété" afin d'économiser les batteries »* ; `:31-32` : coupure > 4 h → priorité à l'extinction, pas au maintien de température. La réponse implémentée n'est pas gardée : l'**ECS 45 °C** consomme réellement (à rebours direct de la sobriété), et le **signal confort** est publié sans condition (consommation réelle en hiver ; probablement inerte en été — voir analyse séparée).

**[FAIT] L'override court-circuite la hiérarchie métier.** `10_scripts/chauffage/decision_centrale.yaml` : `mode_confort_chauffage == on` est la **première branche** de `desired_mode` (`:195-198`, raison `confort_force`), devant aération, fenêtre, vacances, présence. Les garde-fous sont explicitement désactivés sous override (`:170-172` anti-rebond, `:285-292` programme inconnu). Or le contrat `00_documentation_arsenal/contrats/pannes/secteur/20_chauffage_et_ecs.md:45-68` veut que `mode_confort_chauffage` soit *« une intention, et non une action thermique »*, la décision centrale restant souveraine — interdiction explicite de *« court-circuiter la décision centrale »*. Esprit du contrat (intention pondérée) vs code (forçage en tête) : divergence.

**[FAIT] Aucune garde saisonnière dans Arsenal.** Recherche exhaustive : aucune gestion `saison/été/hiver/coupure été` dans `decision_centrale`, `autorisation`, les templates chauffage ou boiler. Le seul rempart contre une chauffe estivale est la coupure été **interne à la chaudière Viessmann**, hors contrôle observable d'Arsenal. L'ECS n'a, elle, pas de coupure été.

**[FAIT] Divergence contrat ↔ implémentation sur l'ECS.** Le contrat exige le passage par `script.chauffage_ecs_cycle` (`20…:88-104` — *« cycle »*, type `desinfection` possible, idempotent). L'implémentation appelle un **script différent**, `script.ecs_appliquer_consigne_confirmee` (consigne 45 °C). Soit le contrat est périmé, soit l'implémentation est non canonique au sens de `20…:142`.

**[FAIT] Aucun délestage batterie-conscient.** Le SOC n'apparaît dans tout le flux panne que dans une **notification** (`11_automations/panne/secteur/alerte_bluetti.yaml:53`, invariant `:12-14` : *« ne pilote ni chauffage, ni ECS, ni mode panne »*). Rien ne réduit la réponse quand la batterie baisse ; seul `11_automations/system/ha_shutdown_ups.yaml` agit (extinction HA/NAS).

---

## Analyse séparée — chauffage vs ECS (cas de l'été)

Les deux volets de la réponse doivent être jugés séparément ; les amalgamer surestime l'impact.

**Chauffage confort en été — [HYP, confiance élevée] probablement inerte, mais non contextualisé.** La consigne confort (~17–25 °C, ~19 °C typique) est inférieure à l'ambiance estivale : la régulation n'a alors **aucune demande de chaleur**, indépendamment même de la coupure été de la chaudière. L'override force donc un **signal** confort sans effet thermique probable. Le grief n'est **pas** un drain batterie estival — c'est l'**absence de contextualisation** (le signal est publié quelle que soit la saison/présence).

**ECS 45 °C en été — [FAIT] consommation réelle sur batterie.** L'ECS n'a pas de coupure été : `10_scripts/system/coupure_secteur.yaml:82-85` applique 45 °C en toute saison. Sur la chaîne thermique alimentée par Bluetti, cela **consomme réellement**, sans veto SOC ni durée, et sans bénéfice de résilience l'été. C'est ici qu'est le coût concret.

**Synthèse :** en été, le mode panne est *probablement inerte côté chauffage* et *réellement consommateur côté ECS*. Le défaut commun reste le **réflexe fixe non gardé** ; l'enjeu énergétique se concentre sur l'**ECS**, pas sur le chauffage.

---

## Hypothèses (à vérifier en runtime)

**[HYP]** **Sortie ECS possiblement non conforme.** Le contrat (`20…:106-112`) impose un reset ECS à la valeur de sécurité **10 °C** au retour secteur. `11_automations/panne/secteur/desactivation_mode_panne.yaml:114-141` ne réalise **aucun reset ECS**. Le rabaissement dépend du gardien `11_automations/ecs/consigne_10/gardien_consigne_reduite.yaml` — à confirmer : l'ECS revient-elle à 10 °C, ou reste-t-elle à 45 °C après l'épisode ?

**[HYP]** **Chauffe estivale physique.** Que `desired_mode = comfort` provoque une chauffe réelle en été dépend de la coupure été de la chaudière, non observée dans le dépôt. Confiance moyenne : inerte si coupure été active, chauffe sinon.

---

## Nuance d'équité

Le réflexe « confort-sécurisation » a une **logique défendable en hiver, coupure courte, batterie saine** : maintenir la chaleur pendant que la chaudière tourne sur batterie évite de réchauffer une maison froide plus tard. Le défaut n'est pas le confort *en soi*, mais son application **universelle et non gardée**.

---

## Classement des suites

| Prio | Sujet | Preuve | Nature |
|---|---|---|---|
| **P0** | Réponse panne **non contextualisée** (signal confort + ECS 45 °C sans veto saison/T°/SOC/durée). Impact à distinguer : **ECS 45 °C = consommation réelle** sur batterie, toute saison ; **confort = signal non gardé**, probablement inerte en été. **Trancher d'abord la doctrine** : sobriété (archi) vs sécurisation-confort (contrat), puis conditionner la réponse — l'ECS étant la priorité énergétique. | `infrastructure_puissance.md:16-20,31-32` vs `activation_mode_panne.yaml:131-141` + `coupure_secteur.yaml:82-85` ; absence de garde saison | Conception métier |
| **P1** | Override `mode_confort` **court-circuite la hiérarchie** alors que le contrat le veut « intention » non forçante ; ajouter un veto contextuel (au minimum saison/T° extérieure). | `decision_centrale.yaml:195-198,170-172,285-292` vs `20…:45-68` | Cohérence contrat/runtime |
| **P1** | **Délestage batterie-conscient absent** : rien ne réduit chauffage/ECS quand le SOC chute. | `alerte_bluetti.yaml:12-14,53` ; seul `ha_shutdown_ups.yaml` agit | Résilience |
| **P2** | **Sortie ECS** : vérifier le reset à 10 °C au retour secteur (non fait dans la désactivation). | `20…:106-112` vs `desactivation_mode_panne.yaml:114-141` | Conformité (à confirmer) |
| **P2** | **Divergence script ECS** : contrat exige `chauffage_ecs_cycle`, impl utilise `ecs_appliquer_consigne_confirmee`. Réconcilier. | `20…:88-104,142` vs `coupure_secteur.yaml:82-85` | Contrat/runtime |
| **P3** | **Contradiction doctrinale documentaire** : `infrastructure_puissance.md` (sobriété) vs `20_chauffage_et_ecs.md` (confort-sécurisation). Documenter la décision retenue. | les deux fichiers | Documentation |

---

## Recommandations (sans patch)

La pièce maîtresse est **P0 — décider ce que le mode panne *doit* faire** avant de toucher au code. Piste cohérente avec l'architecture : **sobriété par défaut**, le volet confort n'étant autorisé que sous conditions (hiver + T° intérieure basse + SOC suffisant + coupure courte), l'ECS de secours restant justifié par l'hygiène mais **gardé par un seuil de batterie**. Aucune action runtime n'est engagée par cette trace.

---

## Références

- Audit détection (frère) : [`audit_panne_detection_coupure_secteur.md`](audit_panne_detection_coupure_secteur.md)
- Contrat effets chauffage/ECS : [`contrats/pannes/secteur/20_chauffage_et_ecs.md`](../../../contrats/pannes/secteur/20_chauffage_et_ecs.md) · socle : [`10_socle.md`](../../../contrats/pannes/secteur/10_socle.md)
- Architecture énergie : [`architecture/infrastructure_puissance.md`](../../../architecture/infrastructure_puissance.md)
- Runtime (non modifié) : `11_automations/panne/secteur/activation_mode_panne.yaml` · `10_scripts/system/coupure_secteur.yaml` · `10_scripts/chauffage/decision_centrale.yaml`
- Hub domaine : [`navigation/domaines/pannes.md`](../../../navigation/domaines/pannes.md) · Index : [`audits/index.md`](../../index.md)
