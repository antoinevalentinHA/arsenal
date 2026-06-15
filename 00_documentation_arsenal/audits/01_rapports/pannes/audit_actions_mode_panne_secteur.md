# ⚡ ARSENAL — AUDIT MÉTIER — Mode panne secteur : pertinence des actions déclenchées

> **Trace d'audit documentaire.** Aucune correction runtime dans cette passe : ni automation, ni template, ni script, ni Lovelace modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse · **[RECO]** recommandation.
> Audit frère (détection) : [`audit_panne_detection_coupure_secteur.md`](audit_panne_detection_coupure_secteur.md).

---

## Verdict

La **détection** est désormais correcte (correction P0 du témoin canonique appliquée). Le sujet de cette passe est la **pertinence métier** des actions déclenchées ensuite.

Le constat n'est **pas** « le mode panne gaspille la batterie ». C'est plus fin : la réponse est **non contextualisée**, et la documentation raisonne en **« sobriété batterie » globale** alors que l'architecture comporte **deux réservoirs distincts** aux finalités opposées. Lus correctement, les effets se classent en **trois catégories** qu'il faut distinguer (cf. § Taxonomie) :

- **Sobriété critique** (rail UPS) — préserver HA / box / réseau / données : intangible.
- **Stockage thermique utile** (rail Bluetti) — ECS haute / désinfection : conversion **volontaire** d'énergie batterie en eau chaude stockée, exploitable par la famille même après la batterie. **Pas une anomalie.**
- **Confort inutile** (rail Bluetti) — chauffage confort d'ambiance non requis (été, absence, maison déjà tempérée) : le seul volet réellement discutable.

**Gravité de fond : P0 (conception/doctrine)** — formaliser la doctrine des deux réservoirs et la taxonomie d'usage, puis conditionner les actions (budget SOC Bluetti + veto confort), avant tout correctif runtime.

---

## Topologie des deux réservoirs (doctrine réelle)

**[FAIT]** L'architecture segmente deux alimentations de secours **indépendantes**, qui ne servent pas le même besoin (`00_documentation_arsenal/architecture/infrastructure_puissance.md:6-14`, `contrats/bluetti.md:5-11`) :

| Réservoir | Alimente | Finalité | Logique d'économie |
|---|---|---|---|
| **UPS (onduleur)** | NAS, serveur HA, box / switch, réseau | Intégrité données + LAN + arrêt propre | **Sobriété critique** : ne rien gaspiller, *graceful shutdown* sous seuil (`infrastructure_puissance.md:24-32`) |
| **Bluetti AC180** | Chaudière, Boiler Pi (boiler bridge), Vitoconnect, ESP32, Deco cave | Chaîne thermique autonome | **Réserve thermique** : à dépenser utilement (eau chaude stockée), bornée par le SOC |

Conséquence directe : **le chauffage et l'ECS ne tirent PAS sur le rail UPS** ; ils consomment le Bluetti, réservoir **dédié** au thermique. La crainte « les actions vident les batteries qui protègent les données » est donc **infondée** : les deux rails sont séparés. La vraie question n'est pas « consommer ou non » mais « **comment dépenser le réservoir Bluetti** : stockage utile vs confort inutile, et avec quel budget SOC ».

---

## Taxonomie d'usage en coupure (à substituer à la « sobriété batterie » globale)

1. **Sobriété critique — rail UPS.** Aucune charge thermique ne doit le toucher (c'est le cas). Préservation pour compute/réseau/données ; arrêt propre sous seuil. Non négociable.
2. **Stockage thermique utile — rail Bluetti.** L'**ECS haute / désinfection** convertit l'énergie batterie en **eau chaude stockée** : utile aux usages familiaux pendant et après la coupure, et justifié sanitairement. Le contrat l'assume déjà comme **exception volontaire** (`contrats/pannes/secteur/20_chauffage_et_ecs.md:72-94` : disponibilité ECS + hygiène). À **borner par le SOC Bluetti**, pas à proscrire.
3. **Confort inutile — rail Bluetti.** Le **chauffage confort d'ambiance** ne stocke rien (la maison perd sa chaleur) et n'a pas toujours de valeur (été, absence). C'est le volet à **conditionner ou suspendre**.

---

## Faits observés — chaîne d'actions

**[FAIT] Réflexe fixe à l'entrée.** `11_automations/panne/secteur/activation_mode_panne.yaml:131-141` : `turn_on` `panne_secteur_active`, `turn_on` `mode_confort_chauffage`, puis appel `script.mode_panne_coupure_secteur`. Le script `10_scripts/system/coupure_secteur.yaml:82-85` applique **ECS `target_temp: 45` / `consigne_haute`**. Aucune lecture de contexte (saison, T°, SOC, présence, durée) n'encadre ces actions.

**[FAIT] ECS haute = stratégie défendable, pas anomalie.** Le contrat la pose comme **exception assumée** (`20…:72-94`), motivée par la disponibilité en eau chaude et l'hygiène. Au regard de la topologie, c'est un **stockage thermique** sur le réservoir dédié. Réserve unique : elle n'est **pas bornée par le SOC** (voir délestage).

**[FAIT] L'override confort court-circuite la hiérarchie métier.** `10_scripts/chauffage/decision_centrale.yaml` : `mode_confort_chauffage == on` est la **première branche** de `desired_mode` (`:195-198`, raison `confort_force`), devant aération, fenêtre, vacances, présence ; garde-fous désactivés sous override (`:170-172`, `:285-292`). Or `20…:45-68` veut que ce soit *« une intention, et non une action thermique »*, la décision centrale restant souveraine. C'est le **confort** (catégorie 3) qui mériterait un veto contextuel — pas l'ECS.

**[FAIT] Aucune garde saisonnière (volet confort).** Aucune gestion `saison/été/hiver` dans `decision_centrale`, `autorisation`, templates chauffage/boiler. En été, la consigne confort (`chauffage_consigne_confort`, plage **17–25 °C**) est sous l'ambiance → **probablement inerte**, mais le signal reste publié sans condition.

**[FAIT] Délestage SOC-conscient absent (les deux rails).** Le SOC Bluetti n'apparaît dans le flux panne que dans une **notification** (`11_automations/panne/secteur/alerte_bluetti.yaml:53`, invariant `:12-14`). Rien ne **borne** le stockage ECS ni ne **suspend** le confort quand le Bluetti baisse. Côté UPS, l'arrêt propre existe (`11_automations/system/ha_shutdown_ups.yaml`) — la sobriété critique y est donc gérée ; c'est le **budget du rail Bluetti** qui manque.

**[FAIT] Divergence contrat ↔ implémentation sur l'ECS.** Le contrat exige `script.chauffage_ecs_cycle` (`20…:88-104` — *« cycle »*, type `desinfection` possible, idempotent). L'implémentation appelle `script.ecs_appliquer_consigne_confirmee` (consigne 45 °C). Soit le contrat est périmé, soit l'implémentation est non canonique (`20…:142`). À réconcilier — d'autant que le contrat évoque justement la **désinfection**, cohérente avec le stockage thermique.

---

## Cas explicite — réponse en été

**Chauffage confort — [HYP, confiance élevée] probablement inerte, mais non contextualisé.** Consigne sous l'ambiance estivale → aucune demande de chaleur. Le grief n'est pas un drain : c'est un **signal confort publié hors contexte** (catégorie *confort inutile*).

**ECS 45 °C — [FAIT] consommation réelle, mais potentiellement voulue.** L'ECS chauffe en toute saison (`coupure_secteur.yaml:82-85`) et puise le Bluetti. Ce n'est **pas** une anomalie par défaut : c'est du **stockage thermique** (eau chaude familiale + hygiène). La question n'est pas « faut-il l'interdire » mais « **jusqu'à quel SOC Bluetti l'autoriser** ». En été comme en hiver, l'arbitrage est un **budget**, pas une proscription.

---

## Hypothèses (à vérifier en runtime)

**[HYP] Sortie ECS.** Le contrat (`20…:106-112`) impose un reset ECS à la valeur de sécurité **10 °C** au retour secteur. `11_automations/panne/secteur/desactivation_mode_panne.yaml:114-141` ne réalise **aucun reset ECS** ; le rabaissement dépend du gardien `11_automations/ecs/consigne_10/gardien_consigne_reduite.yaml` — à confirmer.

**[HYP] Chauffe estivale physique.** Dépend de la coupure été interne chaudière, non observée. Confiance moyenne : inerte si coupure été active.

---

## Nuance d'équité

L'ECS haute et même le confort hivernal ont une **logique défendable** (eau chaude disponible, maison maintenue tant que le Bluetti tient). Le défaut n'est **ni le confort ni l'ECS en soi**, mais (a) l'**absence de budget SOC** sur le rail Bluetti et (b) l'**absence de veto contextuel** sur le seul confort. La « sobriété batterie » globale est une **simplification** : elle ignore que les deux rails ont des finalités opposées et que dépenser le Bluetti en eau chaude est un **usage**, pas un gaspillage.

---

## Classement des suites

| Prio | Sujet | Preuve | Nature |
|---|---|---|---|
| **P0** | **Formaliser la doctrine des deux réservoirs + la taxonomie d'usage** (sobriété critique UPS / stockage thermique utile Bluetti / confort inutile), puis conditionner les actions : **budget SOC Bluetti** + **veto confort contextuel**. Remplacer le raisonnement « sobriété batterie » global. | `infrastructure_puissance.md:6-14` + `bluetti.md:5-11` vs `activation_mode_panne.yaml:131-141` + `coupure_secteur.yaml:82-85` | Conception/doctrine |
| **P1** | **Budget SOC Bluetti absent** : ni le stockage ECS ni le confort ne sont bornés par le SOC du réservoir thermique. | `alerte_bluetti.yaml:12-14,53` ; arrêt propre seulement côté UPS (`ha_shutdown_ups.yaml`) | Résilience |
| **P1** | **Confort non gardé** : l'override `mode_confort` force la première branche sans veto saison/T°/présence ; c'est le volet *confort inutile* à conditionner (pas l'ECS). | `decision_centrale.yaml:195-198,170-172,285-292` vs `20…:45-68` | Cohérence contrat/runtime |
| **P2** | **Sortie ECS** : vérifier le reset à 10 °C au retour secteur. | `20…:106-112` vs `desactivation_mode_panne.yaml:114-141` | Conformité (à confirmer) |
| **P2** | **Divergence script ECS** : `chauffage_ecs_cycle` (contrat, désinfection) vs `ecs_appliquer_consigne_confirmee` (impl). Réconcilier, dans l'esprit « stockage thermique ». | `20…:88-104,142` vs `coupure_secteur.yaml:82-85` | Contrat/runtime |
| **P3** | **Doc « sobriété batterie » trop simple** : `infrastructure_puissance.md:16-20` parle d'« économiser les batteries » sans distinguer rails ni usages. **Corrigé dans cette passe** (nuance topologie + taxonomie). | `infrastructure_puissance.md:16-20` | Documentation |

---

## Recommandations (sans patch)

Doctrine cible, par réservoir plutôt qu'en « sobriété » globale :
- **Rail UPS** — sobriété critique intangible : compute/réseau/données, arrêt propre sous seuil. Aucune charge thermique (déjà le cas).
- **Rail Bluetti** — réserve thermique à **dépenser utilement** : autoriser le **stockage ECS** (eau chaude + hygiène) **borné par un seuil de SOC Bluetti** ; **suspendre/abaisser le confort d'ambiance** dès qu'il n'apporte pas de valeur (été, absence, SOC bas) — c'est lui le poste sacrifiable, pas l'ECS.

Aucune action runtime n'est engagée par cette trace.

---

## Références

- Audit détection (frère) : [`audit_panne_detection_coupure_secteur.md`](audit_panne_detection_coupure_secteur.md)
- Contrat effets chauffage/ECS : [`contrats/pannes/secteur/20_chauffage_et_ecs.md`](../../../contrats/pannes/secteur/20_chauffage_et_ecs.md) · socle : [`10_socle.md`](../../../contrats/pannes/secteur/10_socle.md)
- Architecture énergie (deux réservoirs) : [`architecture/infrastructure_puissance.md`](../../../architecture/infrastructure_puissance.md) · Bluetti / chaîne thermique : [`contrats/bluetti.md`](../../../contrats/bluetti.md)
- Runtime (non modifié) : `11_automations/panne/secteur/activation_mode_panne.yaml` · `10_scripts/system/coupure_secteur.yaml` · `10_scripts/chauffage/decision_centrale.yaml`
- Hub domaine : [`navigation/domaines/pannes.md`](../../../navigation/domaines/pannes.md) · Index : [`audits/index.md`](../../index.md)
