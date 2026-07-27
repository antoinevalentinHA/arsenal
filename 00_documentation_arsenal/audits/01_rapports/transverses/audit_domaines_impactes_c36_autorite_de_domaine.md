# Audit — Domaines impactés par C36 (autorité de domaine)

| Champ | Valeur |
|---|---|
| **Rapport** | Audit du périmètre du chantier [C36](../../04_chantiers/transverses/chantier_autorite_de_domaine.md) — *« Unicité de l'autorité, révocabilité de sa délégation »*. Recense les domaines touchés et évalue la conformité du pilote VMC à la doctrine créée. |
| **Domaines** | VMC (pilote) · socle doctrinal transverse · chauffage / climatisation (recensés, non modifiés) |
| **Date** | 2026-07-27 |
| **Nature** | **Audit statique, lecture seule.** Aucun reboot, reload, appel de service ou changement d'état n'a été provoqué. **Aucun runtime / contrat / checker / UI / registre n'est modifié par ce rapport.** |
| **Base** | HEAD `232be34`. Plage C36 auditée : `e732861~1..200deda` (#571→#579), plus la complétion UI post-clôture #593 (`18b454d`) rattachée à la même ligne d'autorité. |
| **Couverture** | Doctrine `autorite_de_domaine.md` (226 l.) · contrat `vmc.md` §16 (v2.6, 1429 l.) · 4 helpers + 4 scripts + 4 automations + 3 template sensors VMC · `check_vmc_contracts.py` (781 l.) · diff Git intégral de la plage. |

> **Règle appliquée.** Une affirmation sur le comportement runtime n'est marquée *démontrée
> statiquement* que si la chaîne a été suivie jusqu'au service appelé (ou jusqu'à la clause
> d'`availability`/`state` produisant la valeur), triggers et conditions lus. Les verdicts de
> conformité portent sur le **code déployé**, pas sur la seule prose du contrat.

---

## 1. Périmètre réel — quels domaines C36 a-t-il impactés ?

C36 est un chantier **doctrinal** dont la démonstration passe par **un seul domaine pilote**. Le
diff délimite quatre cercles d'impact, de décroissant :

### 1.1 Impact direct — modifié par C36

| Cercle | Artefacts | Nature de l'impact |
|---|---|---|
| **Socle doctrinal (transverse)** | `architecture/03_doctrines/autorite_de_domaine.md` (**créé**, normatif) · `principes_generaux.md` §2 (**amendé** : unicité ≠ permanence) | **Normatif, opposable à tout domaine** offrant une reprise en main. Ne crée aucun runtime (§9 de la doctrine). |
| **VMC — pilote** | contrat `vmc.md` **§16** (v2.6) · helpers `vmc_titulaire_autorite`, `vmc_consigne_manuelle` · scripts `vmc_entrer_mode_manuel`, `vmc_revenir_mode_automatique` · décision exécutoire `binary_sensor.vmc_haute_vitesse_commandee` · `conformite_decision.yaml` (refonte) · `coherence.yaml` · `gestion_auto.yaml` (bascule vers l'exécutoire) · cartes UI `15_autorite/` · `check_vmc_contracts.py` (TEST 9) | **Seul domaine dont le runtime change.** Reçoit la doctrine de bout en bout : contrat → échafaudage → bascule → UI. |

### 1.2 Complété juste après la clôture — même ligne d'autorité

La couche **intention UI** décrite au contrat §16.4 (`input_select.vmc_autorite_intention` +
automations `autorite_intention_execution.yaml` / `autorite_intention_synchro.yaml`) est arrivée
en **#593 (`18b454d`), postérieure au commit de clôture #579**. Elle finalise le pilote VMC mais
ne fait **pas** partie du diff C36 strict. Elle est auditée ici car elle constitue l'état déployé
du mécanisme d'autorité VMC.

### 1.3 Recensés mais **non modifiés** par C36 — dette essaimée `D-C36-L4`

Le Lot 4 a **recensé** (sans les toucher) les deux contrats affirmant une souveraineté
**permanente** d'Arsenal, en contradiction latente avec la doctrine :

- chauffage — [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md)
- climatisation — [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) (invariant *« non modifiable manuellement »*)

Leur mise en cohérence est une **passe distincte, non ordonnancée**, portée au registre en
**③ À arbitrer / dormants**. C36 ne l'a pas exécutée (§8 du chantier, §9 de la doctrine :
recensement seulement).

### 1.4 Hors périmètre C36 — domaines ayant **adopté** la doctrine ensuite

La généralisation transverse est explicitement **essaimée hors C36** (chantiers propres) :
**C37** climatisation · **C39** chauffage · **C40** déshumidificateur. Ils instancient la doctrine
mais ne sont **pas** un impact de C36 ; ils n'entrent pas dans le présent audit.

> **Réponse directe.** « Les domaines impactés par C36 » = **VMC** (runtime + contrat, en
> profondeur) et le **socle doctrinal transverse**. Chauffage et climatisation ne sont
> qu'**inventoriés** pour réconciliation future ; ils ne sont pas modifiés.

---

## 2. VMC — conformité du runtime aux invariants INV-AUT-1..7

Verdict par invariant, contre le **code déployé** (helpers, scripts, template sensors,
automations lus intégralement).

| Invariant | Verdict | Preuve statique |
|---|---|---|
| **INV-AUT-1** — Unicité de l'autorité | **CONFORME** | Titularité portée par un helper unique `input_select.vmc_titulaire_autorite` (options `{automatique, manuel}`). La décision exécutoire `vmc_haute_vitesse_commandee` résout un seul régime à la fois (`state` : manuel → consigne ; sinon → décision auto). Aucun second décideur. |
| **INV-AUT-2** — Écrivain unique | **CONFORME** | Balayage du dépôt : seuls `script.vmc_haute_vitesse` et `script.vmc_basse_vitesse` écrivent `switch.vmc_l1/l2`. Les primitives d'autorité et `gestion_auto` **n'écrivent aucun relais** (helpers / délégation seulement). `synchro_booleen.yaml` ne lit les relais que comme **triggers** (écrit un `input_boolean` façade UI), pas un second chemin d'écriture. |
| **INV-AUT-3** — Pas de décideurs concurrents | **CONFORME** | `gestion_auto.yaml` ne consomme QUE `binary_sensor.vmc_haute_vitesse_commandee` — aucune reconstruction, aucun arbitrage local (TEST 9 le garde partiellement, cf. §3). Le régime tranche sans priorité floue. |
| **INV-AUT-4** — Décision théorique non exécutoire | **CONFORME** | En manuel, `vmc_haute_vitesse_requise` (décision auto) n'est **pas** consommée par l'application ; elle est exposée en attribut informatif (`decision_theorique`, `ecart_theorique`) de `conformite_decision`, sans constituer de non-conformité. |
| **INV-AUT-5** — Transition explicite / observable / déterministe | **CONFORME** | Chaîne UI → `input_select.vmc_autorite_intention` → automation de traduction (gardée « n'agir que si intention ≠ titulaire ») → primitive supervisée → helper de titularité. Entrée manuel **atomique** : consigne écrite **avant** transfert d'autorité (`entrer_mode_manuel.yaml`, séquence imposée). |
| **INV-AUT-6** — Pas de reprise silencieuse | **CONFORME** | Aucun helper d'autorité ne porte `initial:` (restauration HA = vérité). `gestion_auto` ne s'applique qu'après `input_boolean.systeme_stable → on`, sous condition — **aucune reprise implicite vers l'automatique** au boot. La 1ʳᵉ option n'est qu'un bootstrap de création, jamais un fallback (un `unknown` rend l'exécutoire *indisponible*, ne vaut pas « automatique »). |
| **INV-AUT-7** — Expiration volontaire admise | **NON OFFERT — conforme** | Aucune expiration/temporisation de la délégation n'est proposée (délégation indéfinie jusqu'à restitution explicite). Légitime au titre de la **non-sur-spécification** (§6 de la doctrine : un domaine n'est pas tenu d'offrir chaque variante). |

**Anti-fallback (§16.2), démontré statiquement.** `haute_vitesse_commandee.yaml` porte une
`availability` stricte : l'exécutoire est **indisponible** si le titulaire est invalide OU si la
source qu'il désigne l'est (auto → `requise ∉ {on,off}` ; manuel → `consigne ∉ {basse,haute}`).
`gestion_auto` **sans `default`** ⇒ sur exécutoire indisponible, **abstention** (le physique
conserve son dernier régime). `conformite_decision` reste disponible tant que les relais sont
lisibles et **expose la cause** (`cause_indetermination`) — aucune cause muette.

**Bilan §2 : 7/7 invariants tenus par le runtime déployé.** Le pilote VMC est une instanciation
fidèle de la doctrine. Le point faible n'est **pas** le comportement — c'est sa **protection**
contre la régression (§3).

---

## 3. Constat central — la conformité est **portée par le code, pas verrouillée par la CI**

`check_vmc_contracts.py` compte 10 tests. **Un seul** — **TEST 9** — porte authentiquement sur
l'autorité C36. Il vérifie que `gestion_auto.yaml` :

- ne lit **aucun ingrédient** ayant formé la décision (anti-reconstruction, §8.2) ;
- lit **bien** la décision exécutoire `vmc_haute_vitesse_commandee` (§16.2) ;
- que cet exécutoire **contient** la sous-chaîne `vmc_haute_vitesse_requise` (verdict agrégé) ;
- ne lit **pas** le reflet d'exécution `input_boolean.vmc_haute_vitesse` (§8.4).

C'est réel et utile, mais cela ne garde **qu'un maillon**. Ne sont **pas** vérifiés en CI :

| # | Exigence §16 non gardée | Risque de régression silencieuse |
|---|---|---|
| A1 | **Écrivain unique / numerus clausus des relais** (§16.2, §13.1) — aucune garde n'interdit une écriture directe de `switch.vmc_l1/l2` hors des 2 scripts canoniques. | Un nouvel automatisme écrivant un relais passerait la CI. §16.6 se déclare « conforme » **sans filet**. |
| A2 | **Anti-fallback sémantique** de l'exécutoire (§16.2) — rien ne vérifie que `haute_vitesse_commandee` traite `unknown`/`unavailable` sans substituer `automatique`/`basse`. | Un `\| default('basse')` ou un test avalant `unknown` passerait ; c'est le cœur de l'anti-repli. |
| A3 | **Résolution effective de la titularité** — TEST 9 exige la *présence* de `requise` dans l'exécutoire, **pas** qu'il lise le titulaire/la consigne. | Un exécutoire qui recopierait `requise` en ignorant le régime manuel **passerait TEST 9** — alors que c'est l'objet même de C36. |
| A4 | **Atomicité consigne-avant-autorité** (§16.4) — l'ordre de la primitive d'entrée manuel n'est pas inspecté. | Inversion de l'ordre (autorité avant consigne) non détectée. |
| A5 | **Boot / pas de reprise silencieuse** (§16.4, §9.4) — rien n'impose à `gestion_auto` d'attendre `systeme_stable` ni d'appliquer « une seule fois ». | Le retrait de la garde de stabilité serait invisible en CI. |
| A6 | **Intégralité du §16.5** — watchdog XOR sur incohérence *réelle*, conformité comparée à l'*exécutoire*, récupération minimale (garde anti-matraquage). | Aucun test ; comportements les plus subtils, les plus exposés à une refonte maladroite. |
| A7 | **Porteur d'intention sans `initial:` / UI n'écrit jamais le titulaire** (§16.4). | Ajout d'un `initial:` ou d'un `tap_action` écrivant le titulaire non détecté. |

**Divergence contrat↔CI notable (A3).** TEST 9 valide `commande → exécutoire → verdict` par
simple **présence de sous-chaîne**. La surface opposable du §16 est donc **en avance** sur ce que
la CI sait constater : la garantie centrale de C36 (l'exécutoire *dépend du titulaire*) n'est pas
testée. À prioriser si le constat est promu.

---

## 4. Socle doctrinal transverse — intégrité

`autorite_de_domaine.md` (v1.0.0, normatif) :

- **instancie** le principe §2 de `principes_generaux.md` sans en créer un second (propriété claire :
  §2 fait foi pour l'unicité, la doctrine pour la titularité) ;
- pose 7 invariants opposables + un **cadre commun** (portée/durée/expiration/restitution/persistance)
  explicitement **sans sur-spécification** ;
- borne les **protections impératives** (§7) par renvoi à `commandabilite.md` (cat. A/B) et un
  **test d'universalité** emprunté à `climatisation/09_securite.md`, avec **garde anti-abus**
  (confort/sobriété ≠ protection impérative) ;
- se déclare ne créer **aucun** helper/UI/runtime et ne modifier **aucun** contrat (§9).

**Cohérence vérifiée** : la doctrine ne fige aucun domaine pilote et renvoie explicitement la
réconciliation chauffage/clim hors de son périmètre. Aucune incohérence interne relevée. Le
contrat VMC §16 s'y subordonne correctement (« la doctrine fait foi en cas de divergence »).

---

## 5. Dette latente non réconciliée (`D-C36-L4`)

C'est le seul **impact ouvert** de C36 sur d'autres domaines. Les contrats chauffage
`10_souverainete_execution.md` et climatisation `03_decision_canonique.md` affirment encore une
souveraineté **permanente** d'Arsenal — lecture que la doctrine qualifie précisément d'« ajout non
fondé ». Tant que la passe de réconciliation n'est pas ordonnancée :

- **contradiction documentaire latente** (un contrat de domaine dit « non modifiable manuellement »,
  la doctrine transverse dit « toute autorité est révocable ») — **sans incident runtime**, ces
  domaines n'offrant pas (encore, hors C37/C39) de reprise manuelle contradictoire ;
- statut correct au registre (**dormant**, réveil sur go opérateur). **Aucune action forcée
  recommandée** : l'arbitrage est propriétaire.

> Nuance importante : C37 (clim) et C39 (chauffage) ont depuis **appliqué** la doctrine à ces
> domaines. La réconciliation des **contrats** `10`/`03` reste néanmoins à acter formellement — à
> vérifier lors du réveil de `D-C36-L4` pour éviter un contrat en retard sur son propre runtime.

---

## 6. Réserves documentées reprises telles quelles (non ré-ouvertes ici)

- **Réserve terrain J (VMC)** — scénarios invasifs (rafale, flapping provoqué, défaut persistant)
  non exercés. **Non bloquants**, réexaminés **uniquement sur occurrence naturelle**. Ancrage
  durable = garde contractuelle `vmc.md` §16.5 (aucun compteur/retry sans preuve de matraquage).
  L'audit **confirme** que le runtime ne porte aucun compteur/retry (cohérent avec la réserve).
- **Points non tranchés du contrat** (réserves, pas des défauts) : admissibilité de l'**arrêt** en
  manuel (§16.3), **expiration** de délégation (§16.4). Conformes à la non-sur-spécification.

---

## 7. Opportunités classées — **non imposées, aucune n'est prescrite**

Si le propriétaire décide de **verrouiller C36 contre la régression** (le seul écart réel de cet
audit), par ordre de rendement :

1. **Garde écrivain unique (A1)** — scanner interdisant toute écriture de `switch.vmc_l1/l2` hors
   `haute_vitesse.yaml`/`basse_vitesse.yaml`. Rendement élevé, coût faible (motif syntaxique).
2. **Garde titularité effective (A3)** — exiger que `haute_vitesse_commandee.yaml` lise
   `vmc_titulaire_autorite` **et** `vmc_consigne_manuelle`. Ferme l'angle mort central.
3. **Garde anti-fallback (A2)** — interdire `default(...)`/coercition avalant `unknown` dans
   l'`availability`/`state` de l'exécutoire.
4. **Garde boot (A5)** — exiger la condition `systeme_stable` sur `gestion_auto`.
5. **Gardes A4/A6/A7** — plus coûteuses (analyse d'ordre, sémantique §16.5) ; à peser.

Toute suite relèverait d'un **chantier CI** distinct (cf. C14, couverture contractuelle) et d'un
arbitrage propriétaire. Le présent rapport **ne l'engage pas**.

---

## 8. Synthèse

- **Domaines impactés par C36** : **VMC** (pilote, runtime + contrat) et le **socle doctrinal
  transverse**. Chauffage / climatisation sont **recensés, non modifiés** (`D-C36-L4`, dormant).
  C37/C39/C40 sont **hors C36**.
- **Pilote VMC** : **7/7 invariants d'autorité tenus** par le code déployé. Instanciation fidèle,
  anti-fallback réel, écrivain unique préservé, aucune reprise silencieuse. Comportement **sain**.
- **Seul écart réel** : la conformité repose sur le **code et une conformité auto-déclarée
  (§16.6)**, la **CI ne verrouillant qu'un maillon** (TEST 9). Angles morts A1–A7, dont l'A3
  (titularité effective non testée) est le plus structurant.
- **Dette ouverte** : réconciliation des contrats de souveraineté chauffage/clim (`D-C36-L4`),
  correctement dormante — arbitrage propriétaire.
- **Aucun P1.** Écart classé **P2 (durcissement CI)** ; contradiction contractuelle **P2/P3
  (documentaire, sans incident runtime)**.

**Aucun runtime / contrat / checker / UI / dashboard / registre / changelog n'est modifié par ce
rapport.** Les opportunités du §7 sont classées, non prescrites.

---

## 📎 Renvois

- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Chantier d'origine : [`chantier_autorite_de_domaine.md`](../../04_chantiers/transverses/chantier_autorite_de_domaine.md)
- Contrat pilote : [`vmc.md`](../../../contrats/vmc.md) §16
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (trace ⑤ C36 · dette `D-C36-L4`)
- Contrats à réconcilier : chauffage [`10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) · climatisation [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md)
