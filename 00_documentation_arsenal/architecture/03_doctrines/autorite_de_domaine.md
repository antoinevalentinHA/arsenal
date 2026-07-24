# DOCTRINE ARSENAL — Autorité de domaine

**Référence :** `autorite_de_domaine.md`
**Version :** 1.0.0
**Chantier d'origine :** C36 — Autorité de domaine (unicité de l'autorité, révocabilité de sa délégation)
**Statut :** Normatif

---

## 1. Principe fondateur

> **Pour un périmètre donné et à un instant donné, une seule autorité produit la
> décision exécutoire, et un seul écrivain la porte vers l'exécution. Le titulaire
> de cette autorité peut être Arsenal ou l'utilisateur.**

La formulation directrice de cette doctrine est :

> **Unicité de l'autorité, révocabilité de sa délégation.**

Cette doctrine **instancie**, sans le contredire, le principe *« Autorité unique par
domaine »* de [`principes_generaux.md`](./principes_generaux.md) (§2). Elle en lève une
lecture implicite dangereuse : l'assimilation de l'**unicité** de l'autorité à sa
**permanence** au profit d'Arsenal.

---

## 2. La distinction à établir — unicité ≠ permanence

L'invariant *« un seul décideur par domaine »* garantit qu'il n'existe **jamais** deux
décideurs concurrents, plusieurs écrivains, ni une priorité floue entre une décision
Arsenal et une décision utilisateur. Cet invariant est **conservé strictement**.

Il ne dit **rien**, en revanche, sur l'**identité** du décideur. Assimiler l'unicité à
une souveraineté permanente d'Arsenal est un ajout non fondé : c'est cette assimilation
— et non le principe d'unicité — qui est corrigée ici.

> **L'autorité reste unique à chaque instant ; seul son titulaire peut changer.**

Le changement de titulaire est une **délégation révocable**, pas une rupture de
l'unicité : à tout instant, exactement un titulaire décide.

---

## 3. Définitions

| Terme | Définition |
|---|---|
| **Autorité de domaine** | La faculté, pour un périmètre donné et à un instant donné, de produire la **décision exécutoire** de ce périmètre. Elle est **unique** à chaque instant. |
| **Titulaire** | L'entité qui détient l'autorité à l'instant considéré : **Arsenal** (régime automatique) **ou** l'**utilisateur** (régime manuel). Jamais les deux simultanément. |
| **Décision exécutoire** | La décision effectivement portée vers l'exécution matérielle du périmètre. Il n'en existe **qu'une** à l'instant t. |
| **Écrivain unique** | L'unique couche autorisée à porter la décision exécutoire vers l'exécution pour ce périmètre. L'unicité de l'écrivain est le corollaire d'exécution de l'unicité de l'autorité. |
| **Décision théorique** | Ce qu'Arsenal **aurait décidé**. En régime manuel, elle peut continuer d'être calculée et exposée, **mais uniquement comme information non exécutoire**. |

---

## 4. Les deux régimes

Un périmètre gouverné par cette doctrine est, à chaque instant, dans **exactement un**
des deux régimes.

| Régime | Titulaire de l'autorité | Décision exécutoire produite par | Décision théorique d'Arsenal |
|---|---|---|---|
| **Automatique** | **Arsenal** | Arsenal (chaîne observation → décision → exécution) | *est* la décision exécutoire |
| **Manuel** | **Utilisateur** | l'utilisateur (commande explicite) | calculée si utile, **non exécutoire** (information) |

En régime manuel, Arsenal **expose l'état réel**, **exécute les commandes explicites**,
**diagnostique les échecs**, **maintient les protections impératives documentées** (§7),
et **ne reprend pas silencieusement la main** (§5).

> Le passage en manuel ne signifie pas « arrêt ». Il signifie que **l'utilisateur décide
> de la commande** — marche, arrêt, consigne, vitesse, position, durée ou toute autre
> capacité propre au domaine. La nature exacte de la commande relève du **contrat de
> domaine**, pas de la présente doctrine (§6, §9).

---

## 5. Invariants opposables

- **INV-AUT-1 — Unicité de l'autorité.** À un instant donné et pour un périmètre donné,
  l'autorité décisionnelle est détenue par **un seul** titulaire.
- **INV-AUT-2 — Écrivain unique.** La décision exécutoire est portée vers l'exécution par
  **un seul** écrivain ; aucun second chemin d'écriture n'est admis en parallèle.
- **INV-AUT-3 — Pas de décideurs concurrents.** Aucune priorité floue, aucun arbitrage
  implicite entre une décision Arsenal et une décision utilisateur : le régime détermine
  sans ambiguïté qui décide.
- **INV-AUT-4 — Décision théorique non exécutoire.** En régime manuel, toute décision
  calculée par Arsenal est **information**, jamais commande ; elle n'atteint pas
  l'écrivain.
- **INV-AUT-5 — Transition explicite, observable, déterministe.** Le changement de
  titulaire résulte d'un acte explicite, est **observable** (l'état d'autorité est lisible)
  et **déterministe** (mêmes causes, même résultat).
- **INV-AUT-6 — Pas de reprise silencieuse.** Arsenal ne **reprend jamais** l'autorité
  d'un périmètre en régime manuel de façon silencieuse. Toute restitution à Arsenal est
  elle-même explicite, observable et déterministe (INV-AUT-5).
- **INV-AUT-7 — Expiration volontaire admise.** Une expiration **choisie dès l'origine par
  l'utilisateur** (terme, condition ou durée) est une modalité **légitime** de restitution
  ; elle ne contredit pas INV-AUT-6, la restitution restant prévue, observable et
  déterministe.

---

## 6. Cadre commun — portée, durée, expiration, restitution

Cette doctrine fixe un **cadre commun** que les contrats de domaine renseignent ; elle
**n'impose pas** que chaque domaine offre chaque variante possible. Le socle transverse
impose les **invariants** (§5), pas les **usages locaux**.

Chaque contrat de domaine qui adopte le régime manuel **doit** définir, dans les bornes
des invariants du §5 :

- **Portée** — le périmètre exact d'une prise en main (domaine entier, zone, équipement).
  Un même domaine peut n'exposer qu'une seule granularité ; il n'est **pas** tenu de les
  offrir toutes.
- **Durée** — le ou les modes de durée offerts (ponctuel, temporisé, conditionnel,
  indéfini). Un domaine peut n'en offrir qu'un.
- **Expiration** — si une expiration volontaire (INV-AUT-7) est proposée, et selon quel
  terme/condition.
- **Restitution** — comment l'autorité revient à Arsenal : l'acte de restitution est
  **explicite, observable et déterministe** (INV-AUT-5/6), sans effet de bord ni surprise.
- **Persistance** — le comportement du régime après redémarrage ou rechargement : le
  contrat de domaine statue explicitement (état restauré vs recalculé), en cohérence avec
  [`restauration_etat_helpers.md`](./restauration_etat_helpers.md). Aucune restauration ni
  aucun recalcul ne doit produire de reprise silencieuse (INV-AUT-6).

> **Non sur-spécification.** L'absence, dans un domaine, d'une variante de portée ou de
> durée n'est **pas** une non-conformité : seul le respect des invariants du §5 l'est.

---

## 7. Protections impératives

Certaines protections priment légitimement sur la commande humaine. Leur périmètre doit
être **strictement défini**, sous peine de vider le régime manuel de son sens.

Une inhibition ne prime sur une commande manuelle **que si** elle relève de l'une des deux
catégories suivantes, qualifiées par renvoi et **jamais élargies par commodité** :

1. **Impossibilité physique (catégorie A de [`commandabilite.md`](./commandabilite.md),
   §5).** L'exécution ne peut aboutir quel que soit l'acteur (chemin de commande rompu,
   pont hors ligne, dépendance secteur absente). Aucun titulaire ne peut la contourner.
2. **Protection de sûreté ou de matériel non négociable**, satisfaisant le **test
   d'universalité** déjà établi par [`../../contrats/climatisation/09_securite.md`](../../contrats/climatisation/09_securite.md)
   (invariant vrai pour **tout** état légal du domaine **et** indépendant de tout seuil,
   délai ou exception négociable).

> **Garde anti-abus (opposable).** Une préférence de **confort** ou de **sobriété** n'est
> **jamais** une protection impérative. Une inhibition **négociable** (seuil, délai,
> exemption, politique de comportement) relève de la **catégorie B** de
> [`commandabilite.md`](./commandabilite.md) (§5–6.2) : elle exprime une politique
> d'automatisme, qu'un titulaire manuel peut **légitimement** outrepasser. Confondre une
> politique de confort avec une protection de sûreté est la dérive que ce paragraphe
> proscrit.

Les protections impératives sont **communes aux deux régimes** : elles n'appartiennent ni
à Arsenal ni à l'utilisateur, mais au périmètre. Elles ne constituent **pas** une reprise
d'autorité au sens du §5 — elles bornent l'espace des commandes exécutables, quel que soit
le titulaire.

---

## 8. Articulation avec les doctrines voisines

- **[`principes_generaux.md`](./principes_generaux.md) §2** — propriétaire du principe
  *« autorité unique par domaine »*. La présente doctrine en est l'**instanciation** ; elle
  n'en crée pas une seconde. En cas de divergence, §2 fait foi pour l'**unicité** ; la
  présente doctrine fait foi pour la **titularité et sa révocabilité**.
- **[`commandabilite.md`](./commandabilite.md)** — doctrine **distincte** et **dépendance**.
  Elle répond à *« puis-je exécuter maintenant ? »* (capacité d'exécution) ; la présente
  doctrine répond à *« qui décide ? »* (titularité). Les deux axes sont **orthogonaux** :
  la présente doctrine **n'absorbe pas** la commandabilité, et réciproquement. Elle réutilise
  sa distinction catégorie A / catégorie B (§7) sans la redéfinir.
- **[`separation_decision_action.md`](./separation_decision_action.md)** — la séparation
  décision / action reste entière : le changement de **titulaire** de la décision ne
  fusionne jamais les couches. L'écrivain unique (INV-AUT-2) est une couche d'action, jamais
  un décideur.

---

## 9. Ce que la doctrine n'impose PAS

- Elle ne crée **aucun** helper, **aucune** entité, **aucune** UI, **aucun** runtime.
- Elle ne **sur-spécifie** aucun usage local : les variantes de portée, durée et expiration
  sont **offertes par les contrats de domaine**, dans les bornes des invariants (§6).
- Elle ne modifie **aucun** contrat de domaine. Les contrats existants qui affirment une
  souveraineté permanente d'Arsenal (notamment
  [`../../contrats/chauffage/10_souverainete_execution.md`](../../contrats/chauffage/10_souverainete_execution.md)
  et l'invariant *« non modifiable manuellement »* de
  [`../../contrats/climatisation/03_decision_canonique.md`](../../contrats/climatisation/03_decision_canonique.md))
  sont **à réconcilier ultérieurement**, par passe délibérée et documentée, hors de la
  présente doctrine.
- Elle ne **choisit** aucun domaine pilote : elle fournit le **cadre** rendant ce choix et
  ces adaptations décidables.

---

## 10. Statut architectural

Cette doctrine est :

- **transversale** — elle relie observation, décision, action et UI sans appartenir à une
  seule ;
- **structurante** — elle qualifie qui détient l'autorité d'un périmètre et comment cette
  autorité se délègue et se restitue ;
- **non optionnelle** — tout domaine offrant une reprise en main utilisateur doit se
  conformer à ses invariants (§5) et renseigner le cadre commun (§6).

Toute dérogation doit être explicitement justifiée dans le contrat du domaine concerné.

---

## 📎 Documents liés

- [`principes_generaux.md`](./principes_generaux.md) — §2 « Autorité unique par domaine »
  (principe instancié ici).
- [`commandabilite.md`](./commandabilite.md) — capacité d'exécution ; catégories A / B
  (protections impératives, §7).
- [`separation_decision_action.md`](./separation_decision_action.md) — séparation décision /
  action (écrivain unique).
- [`restauration_etat_helpers.md`](./restauration_etat_helpers.md) — persistance au
  redémarrage (§6).
- Chantier d'origine : [`../../audits/04_chantiers/transverses/chantier_autorite_de_domaine.md`](../../audits/04_chantiers/transverses/chantier_autorite_de_domaine.md).

---

*Document normatif Arsenal. Toute dérogation doit être explicitement justifiée dans le
contrat du domaine concerné.*
