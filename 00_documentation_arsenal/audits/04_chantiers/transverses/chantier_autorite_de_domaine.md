# Chantier TRANSVERSE (C36) — Autorité de domaine — unicité de l'autorité, révocabilité de sa délégation

| Champ | Valeur |
|---|---|
| **Chantier** | Poser une doctrine transverse d'**autorité de domaine** : lever l'assimilation actuelle entre *autorité unique* et *souveraineté permanente d'Arsenal*, et définir les régimes **automatique** / **manuel** sous la formule **« unicité de l'autorité, révocabilité de sa délégation »**. |
| **Domaine** | Transverse — doctrine d'autorité décisionnelle. Sans propriétaire documentaire préexistant. |
| **Statut** | **Ouvert — doctrine (PR #571) et amendement VMC v2.5 (PR #572) livrés ; conception runtime VMC validée ; PR A (contrat v2.6 — comportements) en cours.** PR A strictement documentaire ; runtime en PR B/C ultérieures. |
| **Priorité** | **P2** — enjeu structurant, sans risque technique immédiat. Fait suite à l'observation **A2** de C34 (asymétrie doctrinale commande-directe / consigne-déléguée) et à l'audit transverse d'autorité (2026-07-24). |
| **Ouvert le** | 2026-07-24. |
| **Prochain jalon** | Doctrine (PR #571) et amendement VMC v2.5 (PR #572) **livrés** ; **conception runtime validée**. **PR A** : contrat [`contrats/vmc.md`](../../../contrats/vmc.md) **v2.6** — spécification des comportements de l'autorité de domaine (anti-fallback, transitions atomiques, récupération minimale, conformité vs décision exécutoire), sans runtime. **PR B** (échafaudage inerte + `availability` cohérence) puis **PR C** (bascule L4+L6) à suivre, sur pré-attribution des identifiants. |
| **Registre** | Chantier **C36** — ① Actifs, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |

> **Portée.** Chantier **doctrinal resserré.** Aucun helper, aucune UI, aucun runtime, aucune
> modification de contrat de domaine à ce stade. Les contrats affirmant une souveraineté permanente
> d'Arsenal sont **recensés comme « à réconcilier ultérieurement »** (Lot 4), non modifiés ici.
> L'ouverture doctrinale n'a valu ni conception par domaine, ni choix de pilote ; le
> pilote **VMC** a depuis été retenu (2026-07-24) et traité **au seul niveau
> documentaire** (§6).

---

## 1. La contradiction démontrée

Un audit transverse en lecture seule (2026-07-24) a confronté la doctrine, les contrats et
l'implémentation sur la question de l'autorité décisionnelle. Trois constats.

**A. Arsenal détient de fait l'autorité par défaut dans les domaines thermiques/air.** Les contrats
l'écrivent littéralement : [`chauffage/10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md)
§2 (« *le moteur Chauffage Arsenal est l'autorité souveraine de référence…* » ; « *toute commande
manuelle est réinterprétée par la Décision Centrale* ») ; [`climatisation/03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md)
(invariant *« non modifiable manuellement »*). Dans ces domaines, l'ordre humain **n'est pas une
entrée de premier rang**, et la machinerie de réconciliation (Guard + Watchdog) **ré-asserte** la
décision automatique — une action manuelle directe est annulée sans acte explicite.

**B. La doctrine tranche déjà, à moitié, dans l'autre sens.** [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
§6.2 pose qu'un override manuel est **légitime** face à une interdiction de politique (catégorie B).
Deux domaines l'implémentent déjà : arrosage ([`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md),
mode manuel supervisé, opérateur décideur) et voiture ([`voiture.md`](../../../contrats/voiture.md),
amendement A1, commande manuelle bornée, décideur humain). Il existe donc une **contradiction non
arbitrée** entre les contrats thermiques (souveraineté machine) et la doctrine de commandabilité
(délégation révocable).

**C. Le problème n'est pas le principe d'autorité unique.** Le problème est l'**assimilation** entre
*autorité unique* et *souveraineté permanente d'Arsenal*. Le principe [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md)
§2 garantit qu'il n'existe jamais deux décideurs ; il ne dit **rien** sur l'identité du décideur.
C'est l'ajout implicite « le décideur est toujours Arsenal » qui est fautif.

---

## 2. Objectif normatif — porté par la doctrine

L'énoncé normatif du chantier — formulation directrice « unicité de l'autorité, révocabilité de sa
délégation », régimes automatique / manuel, invariants, cadre commun (portée, durée, expiration,
restitution) et protections impératives — est porté **exclusivement** par
[`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md). La présente
fiche **ne le recopie pas** : elle en pilote la production et la gouvernance.

---

## 3. Périmètre / hors-périmètre

**Périmètre (doctrinal) :**

- la contradiction souveraineté permanente ↔ délégation révocable ;
- la définition de l'**autorité de domaine** (unicité de la décision exécutoire et de l'écrivain) ;
- les régimes **automatique** et **manuel**, et le statut **non exécutoire** de la décision théorique
  d'Arsenal en manuel ;
- les règles de **transition, portée, durée, persistance et restitution**, posées comme **cadre
  commun** que les contrats de domaine renseignent — **sans** rendre obligatoire chaque variante ;
- la **définition stricte des protections impératives** ;
- la **méthode de sélection ultérieure d'un domaine pilote** (critères, pas de choix).

**Hors-périmètre (explicite) :**

- toute conception de helpers, d'UI, de runtime, et toute implémentation par domaine ;
- toute modification des contrats de domaine — notamment chauffage et climatisation (Lot 4 :
  **recensement** seulement) ;
- le régime de sûreté **alarme** (conservé tel quel) et le domaine **ouvertures** (observation pure) ;
- les arbitrages **par domaine** (portée globale vs zone, modèle de durée, « action physique directe
  = reprise ? ») : la doctrine pose le **cadre** qui les rend décidables, elle ne les tranche pas ;
- le **choix** du domaine pilote lui-même.

---

## 4. Documents à créer ou modifier

**Propriétaire documentaire naturel.** La vérité *« autorité unique par domaine »* appartient à
[`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) §2 ; la
contradiction y est localisée. [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
détient l'axe **orthogonal** (capacité d'exécution, non titularité) et s'interdit lui-même (§8) de
fusionner des réalités distinctes — il reste une **dépendance**, pas le propriétaire.

- **MODIFIER** — [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md)
  (§2) : clarifier *unicité de l'autorité ≠ souveraineté permanente ; titulaire variable ; délégation
  révocable* + renvoi.
- **CRÉER** — [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md) :
  doctrine instanciant §2 (régimes, écrivain unique, transition/portée/durée/persistance/restitution,
  protections impératives).
- **Renvois strictement nécessaires** — index [`03_doctrines/README.md`](../../../architecture/03_doctrines/README.md)
  et compteur/énumération de [`architecture/index.md`](../../../architecture/index.md).
- **Gouvernance** — la présente fiche + la ligne au cockpit [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
  (co-commit).
- **Recensement (sans modification)** — contrats à réconcilier :
  [`chauffage/10_souverainete_execution.md`](../../../contrats/chauffage/10_souverainete_execution.md) §2,
  [`climatisation/03_decision_canonique.md`](../../../contrats/climatisation/03_decision_canonique.md) ;
  précédents réutilisables : [`arrosage/11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md),
  [`voiture.md`](../../../contrats/voiture.md) (A1).

---

## 5. Lots documentaires minimaux

- **L1 — Trancher la contradiction** : clarifier `principes_generaux.md` §2 (formulation directrice).
- **L2 — Doctrine « autorité de domaine »** : régimes, écrivain unique, décision théorique non
  exécutoire, transition/portée/durée/persistance/restitution comme **cadre commun**.
- **L3 — Protections impératives** : critère opposable (commandabilité catégorie A + test
  d'universalité) + garde anti-abus « confort/sobriété ≠ sécurité ».
- **L4 — Méthode de sélection du domaine pilote** + recensement des contrats à réconcilier
  ultérieurement + renvois/registre (co-commit).

> **Réalisation à l'ouverture.** L1, L2 et une première rédaction de L3 sont portés par la doctrine
> créée à l'ouverture ; L4 (méthode + recensement) est intégré à la doctrine (§7, §9) et à la présente
> fiche (§4, §6). Le séquencement ultérieur relève des passes par domaine.

---

## 6. Méthode de sélection ultérieure d'un domaine pilote

Le domaine pilote **n'est pas choisi ici**. Critères de sélection proposés, à trancher au moment de la
première passe par domaine :

- **Révélateur du problème** — le domaine où l'absence de reprise en main est la plus démontrée
  (climatisation : décision non modifiable manuellement + ré-assertion Watchdog).
- **Écrivain déjà unique et identifié** — pour ne pas créer d'ambiguïté d'écriture à l'occasion.
- **Décision déjà pure et permanente** — pour exposer sans coût la décision théorique non exécutoire.
- **Protections impératives déjà qualifiées** — pour distinguer nettement sûreté et confort (le test
  d'universalité de `09_securite.md` est un acquis côté climatisation).
- **Coût de réconciliation contractuelle borné** — impact documentaire maîtrisable sur le contrat du
  domaine.

> **Pilote retenu (2026-07-24) : VMC.** Décision propriétaire après l'audit ciblé VMC. Motifs :
> surface de commande binaire `{basse, haute}` coïncidant avec le mode manuel ; **écrivain déjà
> unique** (`script.vmc_haute_vitesse` / `script.vmc_basse_vitesse`) ; **aucune ré-assertion
> silencieuse continue** à démanteler (le §12.1 du contrat VMC l'exclut) ; décision pure disponible
> comme décision théorique non exécutoire ; **protection physique XOR** nettement séparable. La
> traduction contractuelle est portée par [`../../../contrats/vmc.md`](../../../contrats/vmc.md) §16
> (v2.5 → **v2.6** : comportements spécifiés). Déploiement **en trois PR** — A (contrat, documentaire),
> B (échafaudage inerte + `availability` cohérence, sans activation du manuel), C (bascule L4+L6 +
> tests terrain). Les travaux C36-VMC avancent **en parallèle** des réserves C35 (calibration /
> historisation), orthogonales à la titularité de l'autorité.

---

## 7. Arbitrages restant ouverts (hors ouverture)

Ces arbitrages relèvent des **passes par domaine**, pas de l'ouverture doctrinale :

- une **action physique directe** sur un équipement vaut-elle prise en main ? (à trancher par domaine) ;
- **portée** du mode manuel : domaine entier, zone, ou les deux, selon le domaine ;
- **modèle de durée** offert (ponctuel / temporisé / conditionnel / indéfini) par domaine ;
- **domaines dans le périmètre** (VMC, déshumidificateur — aujourd'hui auto purs à contraintes de
  sûreté fortes — reçoivent-ils un mode manuel ?) ;
- réconciliation effective des contrats de souveraineté chauffage/climatisation (Lot 4 recense ; la
  mise en cohérence est une passe distincte).

---

## 8. Ce que ce chantier ne décide PAS

- aucun **helper**, **UI**, **runtime**, **checker**, **workflow**, **changelog** ;
- aucune **modification de contrat de domaine** (chauffage, climatisation ou autre) ;
- aucun **choix** de domaine pilote ni aucune **variante locale** de portée/durée imposée ;
- aucune **modification** du régime de sûreté alarme ni du domaine ouvertures.

---

## 9. Critères de non-clôture

C36 **n'est pas clôturable** tant que :

- la contradiction n'est pas explicitement nommée et tranchée au propriétaire du principe
  (`principes_generaux.md` §2) ;
- la doctrine `autorite_de_domaine.md` n'est pas rédigée, mergée et propriétaire unique de la
  titularité de l'autorité ;
- le cadre commun (portée/durée/expiration/restitution) et les protections impératives (critère
  opposable + garde anti-abus) ne sont pas posés **comme invariants sans sur-spécification** ;
- la méthode de sélection d'un domaine pilote et le recensement des contrats à réconcilier ne sont pas
  fournis.

> **Cohérence interne.** Ces critères sont **documentaires, donc solvables sans preuve terrain**
> (doctrine [`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md)).

---

## 10. Renvois

- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Doctrine créée : [`autorite_de_domaine.md`](../../../architecture/03_doctrines/autorite_de_domaine.md)
- Principe propriétaire : [`principes_generaux.md`](../../../architecture/03_doctrines/principes_generaux.md) §2
- Dépendance (axe orthogonal) : [`commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
- Séparation décision / action : [`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md)
- Observation d'origine (asymétrie doctrinale) : [`c34_portefeuille_chantiers.md`](c34_portefeuille_chantiers.md) (A2)
- Précédents de mode manuel : [`arrosage/11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md) · [`voiture.md`](../../../contrats/voiture.md) (A1)
