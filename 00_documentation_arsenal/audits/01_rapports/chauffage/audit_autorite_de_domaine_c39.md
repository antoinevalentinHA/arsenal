# Audit — Autorité de domaine chauffage (C39)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit de conformité du domaine **chauffage** à la doctrine [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md), appliquée par le chantier C39 (patron VMC/C36). Complément de l'[audit C36](../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md), qui avait explicitement exclu ce domaine. |
| **Domaine** | chauffage |
| **Date** | 2026-07-27 |
| **Nature** | **Audit statique, lecture seule.** Aucun reboot, reload, appel de service ou changement d'état provoqué. **Aucun runtime / contrat / checker / UI / registre modifié par ce rapport.** |
| **Base** | HEAD `6169b4d`. |
| **Couverture** | Stack autorité chauffage (helpers, 2 primitives, décision exécutoire `sensor.chauffage_mode_commande`, 2 automations de médiation, application `10240000000028` → écrivain `chauffage_appliquer_consigne` → bridge MQTT chaudière) · contrats `85_autorite_de_domaine_chauffage.md`, `10_souverainete_execution.md` (+ `__amendement.md`), `30_decision_centrale.md` · checker CI R-CALL-1 (`r_call_1.py`) + workflow `arsenal-ci-chauffage.yml` + HINIT. |

> **Règle appliquée.** Verdict porté sur le **code déployé** (templates, conditions, `mqtt.publish`
> suivis jusqu'au topic), pas sur la seule prose contractuelle.

---

## 1. Chaîne d'autorité reconstituée

| Rôle | Composant réel |
|---|---|
| Observation / décision auto | `script.chauffage_decision_centrale` → écrit `chauffage_raison` + `chauffage_mode_session`, **émet un événement** `chauffage_execution_requise` (n'appelle **plus** l'écrivain) |
| Titulaire (vérité) | `input_select.chauffage_titulaire_autorite` ∈ `{automatique, manuel}`, écrit **uniquement** par les 2 primitives |
| Intention UI | `input_select.chauffage_autorite_intention` (surface) → médiation `10240000000029` ; re-synchro `10240000000030` |
| Consigne manuelle | `input_select.chauffage_consigne_manuelle` ∈ `{confort, reduite}`, écrite **avant** le transfert |
| Décision exécutoire | `sensor.chauffage_mode_commande` (dérivée pure ; auto → `mode_session`, manuel → `consigne_manuelle`) |
| Application | automation `10240000000028` (anti-fallback + idempotence + garde `systeme_stable`) |
| **Écrivain unique** | `script.chauffage_appliquer_consigne` → `mqtt.publish` `boiler/command/heating/set_temperature` (+ ACK corrélé `request_id`) |
| Chaudière | bridge Netatmo (exécution déléguée, aucun actionneur physique Arsenal) |

---

## 2. Conformité aux invariants INV-AUT-1..7

| Invariant | Verdict | Preuve statique |
|---|---|---|
| **INV-AUT-1** Unicité | **CONFORME** | Un seul porteur `chauffage_titulaire_autorite` (2 options exclusives), écrit exclusivement par les 2 primitives. Intention UI = porteur de surface distinct, « ne transfère jamais l'autorité ». |
| **INV-AUT-2** Écrivain unique | **CONFORME** (1 axe séparé) | `chauffage_appliquer_consigne` est le **seul** à publier sur `…/set_temperature` (grep exhaustif). **Numerus clausus des appelants fermé à 3**, gardé en CI par **R-CALL-1**. `decision_centrale` n'émet plus qu'un événement ; les scripts vacances déclarent ne jamais l'appeler. **Point d'attention** : la courbe de chauffe publie sur des topics **distincts** (`…/set_curve_slope`, `…/set_curve_shift`) — second axe non gouverné par l'exécutoire régime. **L'unicité de l'écrivain est vraie par axe, pas globale au bridge.** |
| **INV-AUT-3** Pas de concurrents | **CONFORME** | En manuel, l'application n'applique la décision auto que si `trigger.id != 'decision_auto' or titulaire == automatique` : l'événement décisionnel auto est **ignoré** en manuel. |
| **INV-AUT-4** Théorique non exécutoire | **CONFORME** | `mode_commande` en manuel = consigne, jamais `mode_session` (exposé seulement en attribut `regime_theorique`). La garde ci-dessus empêche l'événement auto d'atteindre l'écrivain. |
| **INV-AUT-5** Transition explicite | **CONFORME** | Primitives explicites ; médiation gardée « n'agir que si intention ≠ titulaire » ; synchro idempotente ; état lisible via titulaire + attribut. |
| **INV-AUT-6** Pas de reprise silencieuse | **CONFORME** (gardé partiellement CI) | Aucun `initial:` sur les 3 selects (gardé CI par **HINIT**). Application gardée `systeme_stable` ; convergence ordonnée (barrière de réconciliation du résidu `mode_confort_chauffage` → décision → application unique du titulaire restauré). Aucune reprise implicite vers l'auto. |
| **INV-AUT-7** Expiration volontaire | **NON OFFERT — conforme** (contrat sur-annonce) | Runtime = manuel indéfini (primitive sans champ durée). Légitime (non-sur-spécification). **Écart mineur** : le contrat 85 **annonce l'option**, le runtime ne l'implémente pas. |

**Anti-fallback (démontré, triple garde).** `mode_commande.availability` est vraie **uniquement** si
`(auto ET mode_session ∈ {confort,reduite}) OU (manuel ET consigne ∈ {confort,reduite})` — aucun
`unknown` substitué. L'application redouble la garde, l'écrivain la re-redouble (précheck
bridge/consigne/température). Aucun repli métier.

**Bilan §2 : 7/7 invariants tenus par le runtime déployé.** Écrivain unique et absence d'`initial:`
sont, ici, **effectivement gardés en CI** (R-CALL-1, HINIT) — meilleure couverture que la clim et la VMC.

---

## 3. Réconciliation du contrat de souveraineté `10_souverainete_execution.md` — **hétérogène (résidu ouvert)**

C'est le **point central** et l'écart le plus net entre chauffage et climatisation. Le texte de base du
contrat 10 **n'a pas été édité en place** ; la réconciliation est portée par des fichiers séparés
(contrat 85 + amendement CH-4), avec un niveau de fermeture **inégal selon le paragraphe** :

| Assertion du contrat 10 | Réconciliation | Verdict |
|---|---|---|
| **§2** souveraineté **permanente** d'Arsenal (l. 49-51) | Contrat 85 (l. 33-35) **cite le §2 nommément** : unicité conservée, **titularité précisée** — « délégable et révocable ». | **Neutralisée explicitement, tracée.** Dette close au niveau §2. |
| **§6 l. 248** forçage confort utilisateur | Contrat 85 §85.6 (D4) : rôle utilisateur **retiré** au profit du modèle titulaire (toggle supprimé), réconciliation boot purgeant le résidu. | **Migré explicitement.** |
| **§6 l. 244** « **toute commande manuelle est réinterprétée par la Décision Centrale** » | **Jamais citée ni neutralisée ligne à ligne.** Réconciliation seulement conceptuelle (85 §85.2 établit qu'en manuel l'exécutoire n'est pas la décision machine, **sans citer** l. 244 ; §85.7 renvoie au contrat **30**, pas au 10 §6) + **clause de préséance générale** (85 l. 17-19). | **RÉSIDU OUVERT** au niveau textuel. |
| **§8** « aucune UI souveraine », « une seule source de décision » | UI jamais souveraine (respecté de fait) ; « une seule source » couvert par le renvoi §2. | Respecté ; non cité en propre. |

**Vérifié sur pièces** : le contrat 85 ne référence le contrat 10 que via son **§6bis** (validation
transactionnelle, protection impérative) — jamais via le **§6 l. 244**. La contradiction la plus directe
avec le régime manuel subsiste donc **littéralement** dans le texte de base, réconciliée uniquement
**par priorité** (la doctrine et le contrat 85 font foi en cas de divergence de titularité), pas par une
note in-texte qui cite et qualifie l. 244 comme le §2 l'a été.

> **Conséquence.** Conforme en **priorité doctrinale** (aucun incident runtime : le runtime suit bien la
> titularité), mais la dette `D-C36-L4` n'est **pas close au niveau §6 l. 244**. Un renvoi explicite
> in-texte sur `10 §6 l.244` (et `§8`), symétrique de celui posé sur le §2, fermerait proprement le
> résidu. **Écart contrat↔contrat, P2/P3, sans conséquence fonctionnelle.**

---

## 4. Couverture CI

**Gardé par un filet mécanique :**

- **Écrivain unique / numerus clausus (INV-AUT-2)** — **R-CALL-1** (`r_call_1.py`), job `execution` du
  workflow `arsenal-ci-chauffage.yml`, miroir contrat↔constante gardé par méta-test. **La meilleure garde
  d'autorité des trois domaines audités.**
- **Pas de `initial:` (INV-AUT-6)** — **HINIT** (ERROR bloquant), couvre les 3 selects.

**Réserve majeure — les gardes chauffage sont en phase warn-only :**

- Le workflow porte **`ARSENAL_CI_ENFORCE: "false"`** : R-CALL-1 et le lint structurel/décision
  **signalent** les violations mais **n'échouent pas** la CI (bloquants seulement en phase `enforce`).
  **La garde existe mais ne verrouille pas encore.**

**Angles morts (conformité auto-déclarée) :**

| # | Non gardé | Risque |
|---|---|---|
| B1 | **Anti-fallback de l'availability de `chauffage_mode_commande`** | L'étage-1 CI ne lint **qu'un seul fichier** (`autorisation.yaml`) ; `mode_commande.yaml` **n'y est pas**. La correction de l'`availability` repose sur revue humaine. |
| B2 | **Garde de stabilité au boot + convergence ordonnée (INV-AUT-6 runtime)** | Non testées. |
| B3 | **Unicité du titulaire / garde `decision_auto` en manuel (INV-AUT-1/3/4)** | R-CALL-1 garde l'appelant de l'écrivain, pas les écrivains du **titulaire** ni la garde `trigger.id`. |
| B4 | **Topic MQTT vs appelants** | R-CALL-1 garde les **appelants du script**, pas le **topic** : un `mqtt.publish` direct vers `…/set_temperature` contournerait la garde (limite documentée). |

---

## 5. Écarts contrat↔runtime & points d'attention

1. **`decision_centrale.yaml` — en-tête périmé (doc drift).** Les commentaires « délègue toute exécution
   à `script.chauffage_appliquer_consigne` » contredisent le comportement post-C39 (il n'émet plus qu'un
   événement). Prose obsolète, sans effet runtime.
2. **INV-AUT-7 annoncé, non implémenté** (cf. §2) — le contrat sur-annonce le runtime. Bénin.
3. **`10 §6 l. 244` littéralement contradictoire** (cf. §3) — principal écart, contrat↔contrat.
4. **Double vocabulaire** : `chauffage_dernier_mode_decide` parle `comfort/reduced/neutre` tandis que la
   chaîne d'autorité parle `confort/reduite` — cohérent (mémoire post-ACK en `boiler_mode`) mais deux
   lexiques coexistent, point de lisibilité.
5. **Réserves assumées et tracées du contrat 85** : anti-court-cycle délégué au firmware chaudière (D8) ;
   protection batterie critique = chantier séparé. Cohérent avec la doctrine §7.

---

## 6. Synthèse

- **Conformité runtime : 7/7 invariants tenus** (INV-AUT-7 non offert, légitime). Patron VMC fidèlement
  répliqué. **Aucun P1** propre à l'autorité.
- **Couverture CI : la meilleure des trois domaines** (R-CALL-1 écrivain unique + HINIT) — **mais en
  phase warn-only** (`ARSENAL_CI_ENFORCE=false`) : les gardes ne verrouillent pas encore. Angles morts
  B1–B4 (anti-fallback, boot, titulaire, topic). **P2.**
- **Réconciliation de souveraineté : hétérogène.** §2 et §6 l.248 neutralisés/migrés explicitement ; **§6
  l. 244 laissé littéralement contradictoire**, couvert seulement par préséance ⇒ **résidu `D-C36-L4`
  ouvert au niveau textuel**. Sans incident runtime. **P2/P3.**
- **Dette documentaire** : en-tête `decision_centrale` périmé, double vocabulaire, contrat sur-annonçant
  INV-AUT-7. **P3.**

**Aucun runtime / contrat / checker / UI / registre / changelog modifié par ce rapport.** Les pistes
(fermer le résidu §6 l.244 par renvoi in-texte ; passer les gardes chauffage en `enforce` ; étendre le
lint étage-1 à `mode_commande.yaml`) sont **classées, non prescrites** — arbitrage propriétaire.

---

## 📎 Renvois

- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Contrats : [`85_autorite_de_domaine_chauffage.md`](../../../contrats/chauffage/85_autorite_de_domaine_chauffage.md) · [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) (+ [`__amendement.md`](../../../contrats/chauffage/10_souverainete_execution__amendement.md)) · [`30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md)
- Audit jumeau (climatisation) : [`../climatisation/audit_autorite_de_domaine_c37.md`](../climatisation/audit_autorite_de_domaine_c37.md)
- Audit d'origine (C36/VMC) : [`../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md`](../transverses/audit_domaines_impactes_c36_autorite_de_domaine.md)
