# CONTRAT ARSENAL — CLIMATISATION
## 16 — Autorité de domaine — régimes automatique et manuel

**Version contrat :** v1.0

| Champ | Valeur |
|---|---|
| **Statut** | **Cible contractuelle — spécification opposable, runtime + UI livrés.** Échafaudage + **bascule** + **UI** livrés (§16.8) : l'application, la conformité, le Watchdog et le Guard consomment la **décision exécutoire** ; **le mode manuel est exécutoire** et **accessible** (section « Autorité & reprise en main »). Reste la **validation terrain** puis la clôture fonctionnelle. |
| **Domaine** | Climatisation (unité unique `climate.clim` / `switch.clim_power`). |
| **Instancie** | Doctrine transverse [`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). |
| **Patron** | Pilote VMC [`vmc.md`](../vmc.md) §16. |
| **Origine** | Chantier **C37** ; cadrage [`cadrage_autorite_de_domaine_mode_manuel_climatisation.md`](../../audits/02_conception/climatisation/cadrage_autorite_de_domaine_mode_manuel_climatisation.md) (décisions D1–D8). |

> **Portée.** Cette section instancie pour la climatisation la doctrine transverse d'autorité de
> domaine. Elle définit des **vérités, responsabilités et comportements attendus** ; elle **ne conçoit
> aucun** helper, automation, UI ni détail d'implémentation, et **ne fige aucun type ni identifiant**.
> En cas de divergence sur la titularité, la doctrine fait foi. Cette évolution est **orthogonale** à
> la qualité de la décision automatique : elle porte sur la **titularité de l'autorité**, non sur le
> calcul de `sensor.clim_target_mode`.

---

## 16.1 Principe et titulaires

À un instant donné, l'autorité décisionnelle de la climatisation est détenue par **un seul
titulaire** :

- **Régime automatique** — le titulaire est **Arsenal** ;
- **Régime manuel** — le titulaire est l'**utilisateur**.

Formule directrice : **unicité de l'autorité, révocabilité de sa délégation**. L'unicité porte sur le
fait qu'**un seul titulaire décide** à chaque instant, jamais sur son identité. Il n'existe **jamais**
deux décideurs concurrents, ni de priorité floue entre une décision Arsenal et une décision
utilisateur.

---

## 16.2 Décision exécutoire, écrivain unique, chemin canonique

- Il existe, à chaque instant, **une seule décision exécutoire**.
- L'**écrivain unique** vers l'équipement est la **couche d'exécution existante**
  (`script.clim_execution`, cf. [`08_execution.md`](08_execution.md)), **dans les deux régimes**.
  Aucune commande **directe** de `switch.clim_power` ou `climate.clim` en parallèle de ce chemin
  canonique n'est admise.
- `sensor.clim_target_mode` (décision canonique automatique, [`03_decision_canonique.md`](03_decision_canonique.md))
  demeure **calculé en permanence dans les deux régimes**. En **régime manuel** il est **non
  exécutoire** : il vaut **information** (décision théorique d'Arsenal) et **n'est pas consommé** par
  l'exécution.

**Disponibilité stricte de la décision exécutoire — aucun fallback métier.** La décision exécutoire
n'est **valide** que si le **titulaire** porte une valeur valide (`automatique` ou `manuel`) **et** que
la source qu'il désigne est valide (en automatique, la décision canonique ; en manuel, la consigne).
À défaut, la décision exécutoire est **indisponible**. Un état `unknown`/`unavailable` **ne vaut** ni
`automatique`, ni un mode, ni absence de besoin — aucune valeur n'est substituée.

- Lorsque la décision exécutoire est **indisponible**, l'exécution **s'abstient** (aucune commande) ;
  le physique **conserve son dernier état valide**. Aucun repli métier (ni vers `off`, ni vers un
  mode) n'est produit.
- La **cause d'indisponibilité** (titulaire, consigne ou décision théorique) est **exposée** au
  diagnostic — **aucune cause muette**.

---

## 16.3 Surface de commande manuelle

- La surface de commande manuelle est **le mode** `∈ {off, cool, dry, heat}` — les valeurs mêmes de
  `sensor.clim_target_mode` ([`03_decision_canonique.md`](03_decision_canonique.md)). Le titulaire
  manuel **écrit le mode cible**, qui **devient** la décision exécutoire.
- **Hors périmètre de cette passe** : la **consigne de température** et la **vitesse de ventilation**
  ne sont **pas** exposées à la commande manuelle (Arsenal ne pilote pas la consigne de température
  aujourd'hui ; les exposer serait un second axe de commande, à contractualiser séparément).

---

## 16.4 Transitions, restitution, redémarrage

**Principes.** Le **changement de titulaire** est **explicite, observable et déterministe**. **Aucune
reprise silencieuse** par Arsenal. Une **expiration** volontaire de la délégation (terme ou durée
choisie à l'entrée, INV-AUT-7) est **admise et offerte en option** ; elle n'est pas imposée et reste
une restitution prévue, observable et déterministe.

**Durée.** Le régime manuel est **indéfini jusqu'à restitution explicite** (ou expiration volontaire
si l'utilisateur en a fixé une à l'entrée).

**Entrée en manuel — atomique et supervisée.** L'entrée en régime manuel est portée par une
**primitive backend supervisée**, jamais par une écriture indépendante des vérités depuis l'UI. Elle
procède **dans cet ordre** :

1. **valider** le mode demandé (`off`/`cool`/`dry`/`heat`) — à défaut : abstention et cause exposée,
   aucune écriture ;
2. **écrire la consigne** (le mode) ;
3. **transférer l'autorité** à l'utilisateur (titulaire → manuel) ;
4. **convergence** par la décision exécutoire unique (§16.2).

L'écriture de la consigne **précède** le transfert d'autorité : à l'instant où le titulaire devient
manuel, la consigne porte **déjà** la valeur voulue — **aucune consigne antérieure restaurée n'est
exécutée transitoirement**. La primitive **n'écrit aucun relais** (écrivain unique préservé, §16.2).

**Retour en automatique — explicite et tracé.** Le retour est porté par une **primitive backend
explicite et traçable** (titulaire → automatique) ; la consigne est **laissée telle quelle** et
**ignorée** tant que le régime est automatique. La restitution est un **geste**, jamais un effet de
bord.

**L'UI appelle ces primitives ; elle n'orchestre pas la transition.**

**Redémarrage / rechargement.** Le comportement est **déterministe** et **conforme au titulaire
précédemment établi**, **sans reprise silencieuse** :

- **avant** la restauration des vérités **et** le franchissement du gate de stabilité, **aucune
  application** n'a lieu — l'application **attend** ;
- **aucune reprise implicite vers l'automatique** n'est admise ;
- **après** restauration et stabilité, l'application applique la décision exécutoire **du titulaire
  restauré**, **une seule fois**.

**Bootstrap ≠ fallback.** La valeur de **première création** d'un porteur d'autorité ou de consigne
est un **bootstrap** ; ce **n'est pas** un substitut d'un état `unknown`/`unavailable`, lequel rend la
décision exécutoire **indisponible** (§16.2). Un porteur d'intention/override **n'utilise pas**
`initial:` (doctrine [`restauration_etat_helpers.md`](../../architecture/03_doctrines/restauration_etat_helpers.md)).

---

## 16.5 Protections impératives et distinction en niveaux

| Niveau | Nature | Rapport à l'autorité |
|---|---|---|
| **(a) Cohérence système & impossibilité physique** | Impérative : Guard de cohérence `(clim_target_mode/exécutoire, climate.clim, switch.clim_power)` ([`09_securite.md`](09_securite.md), INV-1/INV-2) ; chemin de commande rompu (catégorie A commandabilité) | Prime dans les **deux régimes** ; borne les commandes, **n'est pas** une reprise d'autorité |
| **(b) — sans objet pour la climatisation** | Contrairement à la VMC (ventilation permanente), la climatisation a un **`off` légitime** ; **aucun invariant fonctionnel** n'impose un fonctionnement permanent | *néant* — l'absence de ce niveau n'est pas une non-conformité (doctrine §6, non sur-spécification) |
| **(c) Sélection du mode & politiques contextuelles** | Politique décisionnelle **négociable** (mode + vetos contextuels, §16.6) | Couche **où s'exerce** l'autorité, automatique ou manuelle |

- **Guard — comparé à la décision exécutoire.** Le Guard de cohérence système reste **impératif dans
  les deux régimes** ; il se compare désormais à la **décision exécutoire** (§16.2), mode manuel
  inclus. Il ne s'oppose donc **pas** à une commande manuelle *cohérente* — il n'interdit que
  l'**incohérence** `(décision, physique)` (ex. `switch.clim_power` actif alors que la décision
  exécutoire vaut `off`). En régime automatique, la décision exécutoire **est** `clim_target_mode` :
  le comportement du Guard y est **inchangé**.
- **Watchdog — ré-assertion de la décision exécutoire.** Le Watchdog ré-applique la **décision
  exécutoire** (auto **ou** consigne), et non la seule décision canonique machine. En automatique,
  cela **coïncide** avec la ré-assertion de `clim_target_mode` (comportement actuel préservé) ; en
  manuel, il ré-applique la **consigne** du titulaire. Le Watchdog **ne modifie jamais** ni
  `clim_target_mode` ni la consigne — il n'en demande que la ré-application sur divergence **réelle**
  avec l'état physique.
- **Conformité comparée à la décision exécutoire.** La conformité est évaluée entre l'état physique
  et la **décision exécutoire**, **jamais** contre la seule décision automatique. Sous autorité
  manuelle, l'écart entre la décision automatique (théorique) et l'état physique est **légitime** : il
  est **exposé** comme information, **sans** constituer une non-conformité ni déclencher d'alerte.
- **Anti-court-cycle — bornage décisionnel.** La protection contre les commutations rapprochées est
  une **durée minimale**, **règle exécutive commune aux deux régimes**. Couplée à une surface au
  niveau **mode** (§16.3), elle rend le battement impossible par construction. Elle **n'est pas** une
  protection impérative de sûreté matérielle.

> **Lacune de sûreté préexistante — hors périmètre, non bloquante.** Il n'existe **aujourd'hui aucune
> protection compresseur matérielle** (anti-court-cycle/défaut/surchauffe) — cf.
> [`06_doctrine_blocages.md`](06_doctrine_blocages.md) §2 (« état 1 vide »). Cette lacune affecte
> **déjà le régime automatique** ; elle n'est **pas** créée par le mode manuel. Une telle protection,
> si elle était posée et **passait le test d'universalité** de [`09_securite.md`](09_securite.md),
> relèverait du niveau **(a)** (impérative, commune aux deux régimes). Elle est suivie comme **item de
> sûreté séparé** (cadrage §3).

---

## 16.6 Vetos contextuels — catégorie A / catégorie B

Règle doctrinale (doctrine §7) : une inhibition ne prime sur la commande manuelle **que si** elle est
une **impossibilité physique** (catégorie A) **ou** une **protection de sûreté passant le test
d'universalité** ([`09_securite.md`](09_securite.md)). **Une préférence de confort ou de sobriété
n'est jamais impérative** (garde anti-abus).

| Inhibition | Nature | Catégorie | Opposable au titulaire manuel ? |
|---|---|---|---|
| Guard cohérence système (INV-1/INV-2) ; impossibilité physique | Cohérence / catégorie A | **A — impérative** | **Non** — mais le Guard se compare à l'exécutoire, il ne bloque que l'incohérence (§16.5). |
| Fenêtres ouvertes (COOL/HEAT/DRY) | Politique énergie/confort | **B — négociable** | **Oui** — outrepassable. |
| Absence prolongée (COOL) | Politique sobriété | **B** | **Oui.** |
| Vacances actives (COOL, [`15_absence_vacances_veto_cool.md`](15_absence_vacances_veto_cool.md)) | Politique sobriété | **B** | **Oui.** |
| Horaire | Politique confort | **B** | **Oui.** |
| Aération étage (COOL/DRY) | Politique coordination | **B** | **Oui.** |
| Poêle actif · aération post-chauffage (HEAT) | Politique coordination | **B** | **Oui.** |

**Conséquence opposable.** En régime **manuel**, le titulaire peut **légitimement** refroidir fenêtre
ouverte, en absence, en Vacances ou hors plage horaire : ce sont des **politiques d'automatisme**
(catégorie B), pas des protections de sûreté. Ces politiques restent **pleinement actives en régime
automatique** ; elles ne sont **pas supprimées**, seulement **non opposables** au titulaire manuel.
Elles demeurent **exposées** comme information (« Arsenal aurait bloqué : fenêtre ouverte »).

> **Articulation avec les flags opérateur existants.** La couche de blocages
> ([`06_doctrine_blocages.md`](06_doctrine_blocages.md)) reconnaît déjà des **flags manuels** (ex.
> `blocage_clim_poele`) : ce sont des décisions opérateur **ponctuelles** au sein du régime
> automatique. Le présent régime manuel est la forme **titularisée et révocable** de l'autorité
> utilisateur (délégation durable), **cohérente** avec ces flags — il ne les supprime pas.

---

## 16.7 Articulation avec les contrats voisins

- [`03_decision_canonique.md`](03_decision_canonique.md) — l'invariant « `clim_target_mode` non
  modifiable manuellement » vaut pour la **décision automatique** ; en manuel, l'exécutoire dérive du
  titulaire + consigne (§16.2), `clim_target_mode` restant la décision **théorique**.
- [`07_arbitrage_politique.md`](07_arbitrage_politique.md) — « un seul résultat de décision » reste
  vrai (une seule décision **exécutoire**) ; c'est le **titulaire** qui est révocable.
- [`09_securite.md`](09_securite.md) — Guard/Watchdog comparés à la décision **exécutoire** (§16.5) ;
  le *runtime* de ce rebranchement est **coordonné avec C30**.
- [`06_doctrine_blocages.md`](06_doctrine_blocages.md) — vetos contextuels = catégorie B, non
  opposables au titulaire manuel (§16.6) ; cohérence avec les flags opérateur existants.
- [`15_absence_vacances_veto_cool.md`](15_absence_vacances_veto_cool.md) — le veto COOL
  absence/Vacances est catégorie B : il reste l'autorité unique d'autorisation COOL en **automatique**,
  non opposable au titulaire **manuel**.

---

## 16.8 État de l'implémentation

**Échafaudage + bascule livrés ; UI à venir.**

- **Livré (échafaudage).** Porteurs `input_select.clim_titulaire_autorite` et
  `input_select.clim_consigne_manuelle` (sans `initial:`) ; décision exécutoire dérivée
  `sensor.clim_mode_commande` (anti-fallback strict, §16.2) ; primitives supervisées
  `script.clim_entrer_mode_manuel` (atomique) et `script.clim_revenir_mode_automatique`.
- **Livré (bascule).** L'**application** (`clim_execution` + son déclencheur), la **conformité**
  (`clim_incoherence_decision_reel`), le **Watchdog** et le **Guard** consomment désormais la
  **décision exécutoire** `sensor.clim_mode_commande` (auto **ou** consigne manuelle), et non plus la
  seule décision automatique. **Le mode manuel est exécutoire.** En régime automatique,
  `clim_mode_commande == clim_target_mode` : le comportement y est **inchangé** (iso-comportement,
  validé par l'oracle). Le Guard s'abstient si la décision exécutoire est indisponible (fail-safe
  §16.2). `sensor.clim_target_mode` reste calculé et exposé comme **décision théorique** (§16.2).
- **Réserve héritée, non régressive.** Le mode manuel hérite du *fail-open* suivi par **C30** (P1) :
  si l'état rapporté par l'intégration est dégradé, une commande peut ne pas s'exécuter silencieusement
  — comme en régime automatique aujourd'hui. Ce n'est **pas une régression** ; C30 traite ce défaut
  pour les deux régimes.
- **Livré (UI).** Section « 🎛️ Autorité & reprise en main » du dashboard climatisation
  (`18_lovelace/dashboards/climatisation/principal.yaml`) + cartes
  `19_button_card_templates/40_dashboards/climatisation/15_autorite/` : titulaire (lecture seule), un
  **sélecteur de mode unique** (rangée `{off, cool, dry, heat}`, mode actif surligné, appelle
  `clim_entrer_mode_manuel` avec la consigne, confirmation modale), restitution
  (`clim_revenir_mode_automatique`), **décision exécutoire** `sensor.clim_mode_commande` en lecture
  seule (anti-fallback « Indéterminée »), et en manuel la **décision théorique** `sensor.clim_target_mode`
  (information). L'UI **appelle** les primitives, n'écrit aucun helper, ne commande aucun
  relais/climate (§16.4). Aucun contrôle direct de mode/alimentation n'existait à neutraliser.
  **Doctrine couleurs (`ui/couleurs`) — usage binaire** : 🟢 vert canon = le mode **actif en régime
  manuel** (action autorisée / actif), ⚪ gris neutre canon = tout le reste (les 3 autres modes, et
  tous les modes en régime **automatique**), ⚪ gris indispo = indéterminée. **Le vert n'apparaît qu'en
  manuel** (l'utilisateur décide) ; le mode est porté par l'icône + le libellé.
- **À venir.** Validation terrain (le mode manuel étant exécutoire et accessible), puis clôture
  fonctionnelle.

---

*Contrat d'autorité de domaine — climatisation. Instancie
[`autorite_de_domaine.md`](../../architecture/03_doctrines/autorite_de_domaine.md). En cas de
divergence sur la titularité de l'autorité, la doctrine fait foi.*
