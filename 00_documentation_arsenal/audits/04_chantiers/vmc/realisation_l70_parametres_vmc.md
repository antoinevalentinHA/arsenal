# Réalisation L7.0 — propriété des paramètres et migration (C35)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.2 |
| **Lot** | **L7.0 — propriété des paramètres et migration.** Premier lot de correction runtime du chantier |
| **Statut** | **Préparé sur branche.** **Premier lot du chantier à modifier le runtime** |
| **Autorité** | [`arbitrage_propriete_parametres_vmc.md`](arbitrage_propriete_parametres_vmc.md) — arbitrage propriétaire du 2026-07-22 |
| **Verrou levé par** | [`solde_reference_terrain_vmc.md`](solde_reference_terrain_vmc.md) — L5 soldé, séquence probatoire close |
| **Contrat** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.2** — §7.4 bis condition 1, §10.4, §14. **Non modifié par ce lot** |

> **Ce lot n'implémente aucun calcul.** Il détermine **où vit chaque paramètre**
> et **comment les nouveaux helpers quittent l'état `unknown`** — mandat exact
> de L7.0, dont l'arbitrage a fait un préalable **bloquant** à L7.1.

---

## 1. Ce qui est créé

### 1.1 Dix helpers persistants, différenciés par pièce

[`03_input_numbers/vmc/seuils/humidite_par_piece.yaml`](../../../../03_input_numbers/vmc/seuils/humidite_par_piece.yaml)

| Helper | Pièce | Amorce |
|---|---|---|
| `input_number.vmc_seuil_on_sdb_parents` | parents | **74 %** |
| `input_number.vmc_fenetre_sdb_parents` | parents | **20 min** |
| `input_number.vmc_evolution_sdb_parents` | parents | **5 pts** |
| `input_number.vmc_seuil_on_sdb_enfants` | enfants | **74 %** |
| `input_number.vmc_fenetre_sdb_enfants` | enfants | **30 min** |
| `input_number.vmc_evolution_sdb_enfants` | enfants | **5 pts** |

[`03_input_numbers/vmc/bornes_frontiere.yaml`](../../../../03_input_numbers/vmc/bornes_frontiere.yaml)

| Helper | Pièce | Amorce |
|---|---|---|
| `input_number.vmc_borne_basse_sdb_parents` | parents | **50 %** |
| `input_number.vmc_borne_haute_sdb_parents` | parents | **70 %** |
| `input_number.vmc_borne_basse_sdb_enfants` | enfants | **50 %** |
| `input_number.vmc_borne_haute_sdb_enfants` | enfants | **70 %** |

**Les bornes sont des helpers par obligation contractuelle**, non par choix : le
§7.4 bis condition 1 les exige « configurables et **exposables** ».

**Avec `input_number.vmc_duree_min_haute`, déjà existant et inchangé, les onze
helpers arrêtés par l'arbitrage sont en place.** Les valeurs d'amorce sont celles
de la passe 5 — **provisoires et révisables**.

### 1.2 Une automatisation d'initialisation

[`11_automations/vmc/initialisation_parametres.yaml`](../../../../11_automations/vmc/initialisation_parametres.yaml)
— identifiant `10190000000006`, `mode: restart`.

**Le risque n'est pas l'absence d'initialisation : c'est l'initialisation de
trop.** Réinitialiser un helper au motif qu'il a été momentanément
`unavailable` **écraserait un réglage utilisateur sans que rien ne le
signale**. Le mécanisme est donc construit autour de cette interdiction.

**Prédicat d'initialisation.** Un helper est initialisé **si et seulement si**
il est **disponible** — état différent de `unavailable` — **et** que son état
**n'est pas numérique**.

**Attente bornée.** Une entité `unavailable` ne dit rien de sa valeur : elle dit
que la plateforme n'a pas fini de la restaurer. L'automatisation attend donc que
plus aucun helper ne soit indisponible, **au plus cinq minutes**
(`continue_on_timeout: true` — l'attente est **bornée, jamais bloquante**),
avant d'évaluer quoi que ce soit. Le déclencheur d'état exige en outre **deux
minutes de persistance** : une indisponibilité passagère ne déclenche **rien**.

**Sémantique retenue — `unknown` et `unavailable` ne sont pas traités de la
même manière**, et c'est délibéré.

| Situation du helper | Comportement | Motif |
|---|---|---|
| **`unavailable`** | **jamais d'écriture** | cet état ne dit rien de la valeur : il dit que la plateforme n'a pas fini de restaurer l'entité |
| **`unknown` persistant, l'entité étant par ailleurs disponible** | **initialisation, après la persistance de deux minutes et l'attente bornée** | c'est le cas **normal** d'un helper nouvellement déclaré, sans état à restaurer |
| **État numérique**, égal ou non à l'amorce | **conservation absolue** | une valeur, d'amorce ou d'utilisateur, fait autorité |
| **Indisponibilité temporaire puis restauration numérique** | **aucune réinitialisation** | pendant l'épisode l'état est `unavailable`, donc exclu ; après, il est numérique, donc exclu également |

> **Pourquoi `unknown` doit être retenu.** L'exclure rendrait le mécanisme
> inopérant : un helper nouvellement déclaré, sans clé `initial:` et sans état
> à restaurer, **vaut précisément `unknown`**. Aucun ne pourrait alors jamais
> sortir de cet état, et la machine resterait non calculable — exactement le
> point de migration bloquant que L7.0 doit lever.
>
> **Ce qui protège l'utilisateur n'est donc pas l'exclusion de `unknown`, mais
> la conjonction de trois gardes** : `unavailable` toujours exclu, deux minutes
> de persistance exigées avant tout déclenchement, et attente bornée avant
> évaluation.

> **Ce n'est pas un repli déguisé.** Un repli s'applique **à chaque évaluation**
> et **masque** l'indisponibilité. Cette initialisation s'exécute **une fois**,
> sur un helper **sans valeur**, après une attente bornée, et laisse ensuite la
> main.

> **Un helper n'est jamais réinitialisé au seul motif qu'il a été
> temporairement indisponible.** C'est l'invariant central du mécanisme, et il
> est **testé** (§5).

### 1.3 Une trace, parce que la bascule ne doit pas être subie

L'automatisation publie une notification persistante énumérant les paramètres
initialisés et **rappelant la valeur du seuil historique global
`input_number.vmc_seuil_on`**, qui n'est pas modifié.

**Motif.** Ce paramètre était **global** ; il devient **différencié par pièce**.
L'arbitrage exige que ce devenir soit **explicite**, « sans écrasement
silencieux ». La valeur historique ne peut pas être connue à l'écriture — L5 a
établi que **ce helper n'est pas historisé** — mais elle est **lisible à
l'exécution**, et c'est là qu'elle est restituée.

---

## 2. Ce qui n'est délibérément pas fait

| Élément | Report | Motif |
|---|---|---|
| **Constantes `A`, `B`, `H`** | **L7.4** — engagement opposable au §2 bis | L'invariant de propriété interdit tout doublon : l'exposition doit être portée **par l'entité qui calcule**. Cette entité n'existe pas encore. Créer les constantes maintenant, ailleurs, produirait exactement le doublon proscrit |
| **Exposition UI des nouveaux helpers** | **L7.7** | **Le §10.4 impose que toute frontière exposée soit celle que le système consomme.** Ces helpers ne sont encore consommés par rien : les afficher créerait **la non-conformité même que L6 a documentée** sur `vmc_seuil_off` |
| **Suppression de `vmc_seuil_off`** | **L7.7** | Il est référencé par le capteur d'intégrité et par deux vues. Le supprimer ici casserait ses consommateurs, qui relèvent du lot final |
| **Retrait de `vmc_seuil_on`** | **L7.1 / L7.3** | Toujours consommé par `haute_vitesse_requise.yaml` et `intention.yaml`. Le retirer maintenant casserait la décision en vigueur |
| **Tout calcul** | **L7.1 et suivants** | Mandat explicite : « aucun calcul ne doit être implémenté avant d'avoir déterminé où vit chaque paramètre » |

> **L7.0 est strictement additif.** Aucune entité n'est supprimée, renommée ni
> modifiée. Aucun comportement existant n'est altéré : la décision en vigueur
> continue de fonctionner exactement comme avant.

---

## 2 bis. `A`, `B` et `H` — engagement opposable pour L7.4

Le report de ces trois coefficients ne doit rien laisser d'ouvert quant à leur
statut. **Cinq engagements sont pris ici, opposables à L7.4 :**

| # | Engagement |
|---|---|
| **1** | `A`, `B` et `H` seront des **constantes versionnées**, portées par un fichier du dépôt et modifiables **uniquement par commit**, donc **sous revue et avec trace** |
| **2** | Elles seront **différenciées par pièce** — un jeu pour la salle de bain parents, un jeu pour la salle de douche enfants —, la différenciation étant établie sur preuves par la passe 5 |
| **3** | Chacune sera **définie une seule fois**. Aucune valeur ne sera répétée dans un second fichier, fût-ce pour l'affichage |
| **4** | Elles seront **exposées par l'entité calculatrice de L7.4**, sous forme d'attributs — l'exposition lisant la définition unique, jamais une copie. C'est ce que le §10.2 exigences 20 à 24 et le §10.4 imposent, et c'est la seule forme qui n'introduise pas de doublon |
| **5** | Elles ne seront **jamais dupliquées dans des helpers**, ni **remplacées par un repli silencieux** : une constante absente ou illisible rend la frontière **non calculable**, état exposé (§4.4 bis, §10.2 exigence 24) qui **ne vaut jamais libération** |

> **Motif, rappelé pour que l'engagement soit lisible sans remonter à
> l'arbitrage.** Ce sont des **choix de calibration**, non des réglages
> d'usage. Les loger dans des curseurs les rendrait modifiables **hors Git,
> sans revue, sans trace**, et potentiellement **en contradiction avec les
> preuves de L2b**.

**Ce que cet engagement n'anticipe pas** : la **forme technique** du fichier de
constantes, qui relève de L7.4 et de l'architecture de l'entité calculatrice.
Seul le **statut** des valeurs est fixé ici.

---

## 3. Invariants de propriété — contrôle

| Invariant | Respect |
|---|---|
| **Une seule définition autoritative par valeur** | ✅ Chaque helper est déclaré une fois ; aucune valeur n'est dupliquée |
| **Aucun doublon helper / constante** | ✅ Les coefficients ne sont pas créés, précisément pour ne pas les dupliquer (§2) |
| **Aucun repli numérique silencieux** | ✅ Aucun `\| float(défaut)` n'est introduit. La sortie d'`unknown` est une écriture **unique et tracée**, pas un repli |
| **Aucun writer permanent** | ✅ La seule écriture est conditionnée à l'absence de valeur, condition qui ne peut plus être satisfaite après le premier passage. Interdiction inscrite dans les en-têtes des deux fichiers de helpers |
| **Absence de clé `initial:`** | ✅ Conforme à la doctrine du dépôt |
| **`S > borne haute`** | ✅ 74 > 70 pour les deux pièces. L'invariant est **documenté dans l'en-tête** ; son **contrôle automatique** relève du capteur d'intégrité, donc de L7.7 |

---

## 4. État du système après ce lot

**Le comportement du runtime est inchangé.** Les dix helpers existent, sont
initialisés et ne sont **consommés par personne**. La décision en vigueur —
`HR ≥ vmc_seuil_on` **ET** `aération favorable`, **OU** CO₂ haut — est
identique à ce qu'elle était.

> **Cet état est transitoire et assumé.** Il n'est **pas** une non-conformité au
> §10.4 : un helper non exposé en UI n'est pas une « frontière exposée à
> l'utilisateur ». C'est précisément pourquoi l'exposition est reportée à L7.7
> plutôt qu'ajoutée ici par commodité.

**Les six écarts contractuels du §2 du chantier demeurent entiers.** L7.0 ne
résorbe aucun d'entre eux : il en prépare la résorption.

---

## 5. Tests du mécanisme d'initialisation

Un checker dédié est ajouté :
[`scripts/arsenal_contracts/check_vmc_initialisation_contracts.py`](../../../../scripts/arsenal_contracts/check_vmc_initialisation_contracts.py),
exécuté par `contracts_vmc_initialisation.yml` (bloquant, non filtré).

**Il ne contrôle pas un texte : il contrôle un comportement.** Le prédicat Jinja
est **extrait du fichier YAML contrôlé**, puis **évalué** avec un `states()`
simulé contre les scénarios ci-dessous.

> **Aucune logique n'est reproduite dans le test.** Une copie du prédicat dans
> le checker le rendrait aveugle à toute dérive du fichier contrôlé — c'est
> précisément le mode de défaillance qu'il doit exclure.

| Scénario | Attendu | Résultat |
|---|---|---|
| **A.** `unavailable` | **jamais d'écriture** | ✅ |
| **B.** `unknown` persistant, entité disponible | **initialisation** | ✅ |
| **C.** numérique égal à l'amorce | conservation | ✅ |
| **C bis.** numérique **différent** de l'amorce | conservation | ✅ |
| **C ter.** numérique hors plage d'amorce | conservation | ✅ |
| **D.** épisode `unavailable` puis restauration numérique | **aucune réinitialisation, aux trois instants** | ✅ |
| **E.** disponible, chaîne vide | initialisation | ✅ |
| **E bis.** disponible, état non numérique quelconque | initialisation | ✅ |
| Croisé — seul le helper sans valeur est retenu, jamais les neuf autres | — | ✅ |
| **Amorçabilité** — déploiement neuf, les 10 helpers à `unknown` | **les 10 sont amorçables** | ✅ |

**Le scénario D est joué comme une séquence**, aux trois instants de l'épisode —
avant, pendant, après. Le prédicat étant sans mémoire, c'est la seule
démonstration recevable : si l'un des trois instants retenait le helper, une
valeur utilisateur serait écrasée après une simple panne.

**Le contrôle d'amorçabilité est le symétrique du précédent** : il démontre que
la garde ne va pas trop loin. Un déploiement neuf, où les dix helpers valent
`unknown`, doit les amorcer **tous** — sans quoi la machine resterait non
calculable.

**Quatre gardes structurelles s'y ajoutent** : attente **bornée** (`timeout`
**et** `continue_on_timeout`), **persistance** exigée sur le déclencheur d'état,
**absence de repli numérique silencieux**, **écriture conditionnée** à un besoin
réel, et **table d'amorce complète** — tout helper déclaré doit être amorçable
et surveillé, faute de quoi il resterait sans valeur.

**Auto-test à trois mutants**, exécuté par le workflow : un prédicat qui
réinitialise sur `unavailable`, un prédicat à repli numérique, et le prédicat
réel confronté aux deux pièges — il ne doit retenir ni l'un ni l'autre. Un
checker qui ne détecterait pas ces mutants serait un checker aveugle.

---

## 5 bis. Contrôles exécutés

**86 checkers `arsenal_contracts` exécutés.** Tous passent, dont les neuf
directement concernés : structure `03_input_numbers` (7 tests, en-tête et balise
NATURE compris), clé `initial`, identifiants d'automatisation, préfixe par
domaine, intégrité de la source des préfixes, **contrat VMC**, **initialisation
VMC** (nouveau), paramètres invalides, notifications.

Le **registre de couverture CI** est mis à jour en conséquence — checkers 85 →
**86**, workflows 90 → **91**, `contracts_*` 84 → **85**, nouvelle famille
« VMC — initialisation des paramètres » — et son propre checker anti-dérive
passe, auto-test compris.

Les trois fichiers runtime créés sont **valides au parseur YAML**.

> **Deux échecs de checkers sont constatés et sont ANTÉRIEURS à ce lot** —
> vérifié en les rejouant sur `main` sans les modifications :
> `check_lovelace_no_inline_templating_contracts` (auto-test sensible au
> séparateur de chemin Windows) et `check_vacances_contracts` (définition
> introuvable). **Ils ne sont ni causés ni aggravés par ce lot**, et sont **hors
> périmètre** de C35.

**Les huit gates documentaires passent.**

---

## 6. Ce que ce lot ne fait pas

- il **ne modifie `/config`** ni aucun runtime en exploitation : le dépôt
  `C:\dev\arsenal` est le miroir versionné, son déploiement est un acte distinct ;
- il **ne recalibre rien** : les amorces sont les valeurs de la passe 5,
  **provisoires** ;
- il **n'implémente aucun calcul**, aucune machine hystérétique, aucune
  frontière ;
- il **ne supprime ni ne renomme aucune entité** ;
- il **n'expose rien en UI** ;
- il **ne résorbe aucun des six écarts** contractuels ;
- il **ne clôt pas C35**.

---

## 7. Prochain jalon

**L7.1 — besoins locaux et paramètres par pièce.** Son préalable est levé : la
propriété des paramètres est fixée et les helpers sont initialisables.

Rappel de la séquence arrêtée : **L7.0 → L7.1 → L7.2 → L7.3 → L7.4 → L7.5 →
L7.6 → L7.7**, avec L7.7 obligatoire et final.
