# Cadrage — Mode manuel supervisé pour la climatisation (autorité de domaine)

**Type :** note de décision (conception). **Chantier :** C37 — Autorité de domaine appliquée à
la climatisation. **Doctrine :** [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md).
**Patron :** pilote VMC [`vmc.md`](../../../contrats/vmc.md) §16. **Statut :** décisions **actées
propriétaire (2026-07-25)**, sans implémentation. **Aucun contrat, aucun runtime modifié par ce
document.**

---

## 0. Objet

L'ouverture C37 ([`chantier_autorite_de_domaine_climatisation.md`](../../04_chantiers/climatisation/chantier_autorite_de_domaine_climatisation.md))
a posé la contradiction (souveraineté machine diffuse) et cadré les arbitrages §5. Le **pivot §5.1
est tranché : OUI**, la climatisation reçoit un **mode manuel supervisé** (délégation révocable). Ce
cadrage **acte les décisions D1–D8**, classe les vetos (D5) et **spécifie le contrat à écrire** (§2).
Il précède le contrat ; il ne l'écrit pas.

---

## 1. Décisions d'arbitrage — actées propriétaire

### D1 (§5.1) — La climatisation reçoit un mode manuel supervisé. **OUI.**

Régime manuel conforme aux invariants INV-AUT-1..7 : l'utilisateur devient **titulaire**, sa commande
devient la **décision exécutoire**, la décision machine (`clim_target_mode`) se rétrograde en
**décision théorique non exécutoire** (INV-AUT-4), sans casser l'unicité (INV-AUT-1) ni permettre de
reprise silencieuse (INV-AUT-6).

### D2 (§5.2) — Surface de commande = **mode `{off, cool, dry, heat}`**.

Le titulaire choisit le **mode cible**, qui **devient** la décision exécutoire — mapping **direct** sur
`sensor.clim_target_mode` (l'utilisateur écrit la même variable que la machine produit en automatique).
**Hors périmètre de la 1ʳᵉ passe** : consigne de température et vitesse de ventilation (Arsenal ne
pilote pas la consigne aujourd'hui — les ajouter introduirait un 2ᵉ axe de commande à contractualiser
séparément). Surface **bornée**, doctrinalement propre (patron VMC §16.3).

### D3 (§5.3) — Portée = **domaine entier (mono-unité)**.

L'installation est **mono-unité** (`climate.clim` / `switch.clim_power` uniques). La prise en main
porte sur l'unité entière ; aucun arbitrage zone/équipement (la doctrine §6 n'oblige pas à offrir une
granularité absente).

### D4 (§5.4) — Anti-court-cycle = **bornage décisionnel** (livrable) ; étage 1 réel = item séparé.

La protection retenue pour livrer le mode manuel est le **bornage décisionnel** : une **durée minimale
commune aux deux régimes** (patron VMC §8.2 — montée immédiate / descente différée, une nouvelle
demande annule un retour différé). Couplée à une surface **au niveau mode** (D2), elle rend le
battement **impossible par construction** (on ne peut commander plus vite que la durée minimale).

> **Lacune préexistante consignée (§3).** `06_doctrine_blocages.md` §2 : *« état 1 actuellement vide…
> aucun blocage matériel réel (court-cycle) n'existe à ce jour. C'est le seul vrai manque
> structurel. »* Cette absence de protection compresseur **matérielle** affecte **déjà le régime
> automatique** ; elle n'est **pas** créée par le mode manuel et **ne le bloque pas**. Elle est
> promue en **item de sûreté séparé** (§3).

### D5 (§5.5) — Vetos : classification catégorie A / B.

Règle doctrinale (§7) : une inhibition ne prime sur la commande manuelle **que si** elle relève de la
**catégorie A** (impossibilité physique) **ou** d'une **protection de sûreté passant le test
d'universalité** de [`09_securite.md`](../../../contrats/climatisation/09_securite.md). **Une
préférence de confort ou de sobriété n'est jamais impérative** (garde anti-abus).

| Inhibition (source) | Nature | Catégorie | Le titulaire manuel peut-il l'outrepasser ? |
|---|---|---|---|
| **Guard système** — `clim_power on` interdit si `target_mode = off` ; `climate.clim` actif interdit si `off` (INV-1/INV-2, `09_securite.md`) | Cohérence système `(décision, physique)` | **Impérative** (préservée par construction) | **Non** — mais le Guard se compare désormais à la **décision exécutoire** (mode manuel inclus), donc il ne s'oppose plus à une commande manuelle *cohérente* ; il n'interdit que l'incohérence. |
| **Impossibilité physique** — chemin de commande rompu, unité hors ligne | Catégorie A commandabilité | **Impérative** | **Non** (aucun titulaire ne peut la contourner). |
| **Fenêtres ouvertes** (COOL/HEAT/DRY, `06` §4) | Politique énergie/confort | **B** (négociable) | **Oui** — « refroidir fenêtre ouverte » est une politique, pas une sûreté. |
| **Absence prolongée** (COOL) | Politique sobriété | **B** | **Oui.** |
| **Vacances actives** (COOL, C20 / `15`) | Politique sobriété | **B** | **Oui.** |
| **Horaire** | Politique confort | **B** | **Oui.** |
| **Aération étage** (COOL/DRY) | Politique coordination | **B** | **Oui.** |
| **Poêle actif / aération post-chauffage** (HEAT) | Politique coordination | **B** | **Oui.** |

> **Conséquence à valider — importante.** En régime **manuel**, l'utilisateur peut **légitimement**
> refroidir fenêtre ouverte, en absence, en Vacances ou hors plage horaire : ce sont des **politiques
> d'automatisme** (catégorie B), pas des protections de sûreté. C'est **exactement l'intention** de la
> doctrine (« un titulaire manuel peut légitimement outrepasser une politique »). Ces politiques
> restent **pleinement actives en automatique** ; elles ne sont **pas supprimées**, seulement **non
> opposables** au titulaire manuel. Les vetos restent **exposés** comme information (« Arsenal aurait
> bloqué : fenêtre ouverte »). **Aucune protection de sûreté n'existe aujourd'hui qui serait
> outrepassée** — la seule qui le serait (compresseur) n'existe pas encore (D4/§3).

### D6 (§5.6) — Durée, expiration, persistance.

- **Durée** : régime manuel **indéfini jusqu'à restitution explicite** (patron VMC).
- **Expiration** : expiration volontaire (INV-AUT-7) **offerte en option** (terme/durée choisi à
  l'entrée), **non imposée** ; une expiration reste une restitution prévue, observable, déterministe.
- **Persistance** : au redémarrage, le **titulaire est restauré** fidèlement, **une seule**
  application de la décision exécutoire, physique préservé par inertie ; **aucune reprise
  silencieuse** (INV-AUT-6). Porteurs **sans `initial:`** (bootstrap ≠ fallback).

### D7 (§5.7) — Action physique directe ≠ prise en main (1ʳᵉ passe).

Une action sur la **télécommande IR** de l'unité (ou une appli constructeur) **ne vaut pas** prise en
main dans la 1ʳᵉ passe : elle n'est **pas observable de façon fiable** par Arsenal (comme la VMC ne
l'a pas traitée). La prise en main passe **exclusivement** par la primitive supervisée (§2).

### D8 (§6) — Séquencement avec C30.

Le **contrat spécifie** le rebranchement de la conformité et du Watchdog sur la **décision
exécutoire** (auto **ou** consigne) comme **comportement cible** (§2). Le **runtime** de ce
rebranchement est **coordonné avec C30** (P1), qui durcit la même couche : aucune écriture runtime de
la conformité avant stabilisation ou coordination explicite avec C30. Le reste (titulaire, consigne,
décision exécutoire dérivée, primitives, surface, durée) **n'est pas gated** par C30.

---

## 2. Forme du contrat à écrire (spécification — passe suivante)

Le contrat climatisation sera amendé sur le **patron VMC §16**, mappé au domaine. **Cette section
spécifie ce qui sera écrit ; elle n'est pas le contrat.**

- **Titulaire d'autorité** — porteur explicite (Arsenal / utilisateur), lisible, observable
  (analogue `input_select.vmc_titulaire_autorite`).
- **Consigne manuelle** — le **mode** choisi par le titulaire manuel `∈ {off, cool, dry, heat}`
  (analogue `input_select.vmc_consigne_manuelle`, ici à valeurs de mode).
- **Décision exécutoire dérivée, anti-fallback strict** — un capteur dérivé pur de (titulaire,
  consigne, décision auto). **Valide seulement si** titulaire valide **et** source désignée valide,
  sinon **indisponible → abstention** : le physique conserve son dernier régime valide, la cause
  d'indisponibilité est exposée (patron VMC §16.2 / `haute_vitesse_commandee.yaml`).
- **Décision théorique** — `clim_target_mode` (décision auto) **maintenue et exposée** en manuel comme
  **information non exécutoire** (l'invariant « non modifiable manuellement » de
  [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) est **conservé
  pour la décision *automatique***, et **complété** : en manuel, l'exécutoire n'est plus
  `clim_target_mode` mais la décision dérivée ci-dessus).
- **Écrivain unique** — la couche d'exécution existante (`script.clim_execution`), **inchangée** comme
  unique chemin ; **aucune** commande directe de `switch.clim_power` / `climate.clim` hors chemin
  canonique.
- **Primitives supervisées** — entrée (valider consigne → écrire consigne → transférer autorité →
  converger, **l'écriture précède le transfert**) et retour (explicite, tracé) ; l'UI **appelle** les
  primitives, ne décide ni n'orchestre.
- **Conformité et Watchdog** — rebranchés sur la **décision exécutoire** (D8) : l'écart entre décision
  **auto** et physique est **légitime** en manuel, exposé **sans** non-conformité ni alerte ; le
  Watchdog ne ré-assère que sur incohérence **réelle** vis-à-vis de l'exécutoire.
- **Protections impératives** — Guard cohérence (préservé, comparé à l'exécutoire) et impossibilité
  physique (cat A), communes aux deux régimes ; durée minimale de descente = règle exécutive commune
  (D4).

**Amendements attendus** : `03_decision_canonique.md` (invariant de sortie **précisé**, pas supprimé),
`07_arbitrage_politique.md`, `09_securite.md` (conformité/Watchdog vs exécutoire), `06_doctrine_blocages.md`
(vetos cat B non opposables au manuel), `15_absence_vacances_veto_cool.md` (veto COOL cat B). Ampleur
à confirmer à l'ouverture de la passe contrat.

---

## 3. Item de sûreté séparé — étage 1 compresseur (à suivre)

L'absence de protection compresseur **matérielle** (`06_doctrine_blocages.md` §2, « seul vrai manque
structurel ») est une **dette de sûreté préexistante**, indépendante du mode manuel. Elle mérite un
**suivi propre** : évaluer si une protection court-cycle/défaut passe le **test d'universalité** (§09)
— auquel cas elle serait **impérative, commune aux deux régimes**. **Non bloquante** pour C37 (D4).
**Ouvert (2026-07-25)** comme chantier **C38** — ouverture documentaire
[`chantier_protection_compresseur.md`](../../04_chantiers/climatisation/chantier_protection_compresseur.md)
(① Actifs, P3 ; caractériser la protection interne Airstage/Fujitsu puis arbitrer).

---

## 4. Séquencement & prochaines étapes

1. **Contrat** (passe suivante) — amender les contrats sur le patron §2, **hors** runtime de
   conformité. **STOP-avant-écriture** : valider ce cadrage (en particulier **D5**) d'abord.
2. **Runtime** — porteurs (titulaire, consigne), décision exécutoire dérivée anti-fallback, primitives
   supervisées ; **le rebranchement conformité/Watchdog est coordonné avec C30** (D8).
3. **UI** — surface de reprise en main (patron VMC : voir titulaire, entrer en manuel, choisir le
   mode, restituer) ; l'UI appelle les primitives.
4. **Validation terrain** — puis clôture fonctionnelle du pilote climatisation.

---

## 5. Ce que ce cadrage ne décide PAS

- Il n'**amende aucun** contrat, ne crée **aucun** helper / capteur / script / UI / checker.
- Il ne fixe **pas** les noms d'entités, types ni identifiants (à l'implémentation).
- Il ne tranche **pas** l'ouverture d'un item pour l'étage 1 compresseur (§3, décision propriétaire).
- Il ne préjuge **pas** du calendrier de C30 (D8) : il pose la règle de coordination, pas une date.

---

## 6. Renvois

- Ouverture : [`chantier_autorite_de_domaine_climatisation.md`](../../04_chantiers/climatisation/chantier_autorite_de_domaine_climatisation.md) (C37, §5 arbitrages)
- Doctrine : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) (INV-AUT-1..7, §6 cadre commun, §7 protections impératives)
- Patron pilote : [`vmc.md`](../../../contrats/vmc.md) §16
- Contrats à amender : [`03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) · [`07_arbitrage_politique.md`](../../../contrats/climatisation/07_arbitrage_politique.md) · [`09_securite.md`](../../../contrats/climatisation/09_securite.md) · [`06_doctrine_blocages.md`](../../../contrats/climatisation/06_doctrine_blocages.md) · [`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md)
- Séquencement : [`chantier_convergence_decision_execution_climatisation.md`](../../04_chantiers/climatisation/chantier_convergence_decision_execution_climatisation.md) (C30)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C37)
