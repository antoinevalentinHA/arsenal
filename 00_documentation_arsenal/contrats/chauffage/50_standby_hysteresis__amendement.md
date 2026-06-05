# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — STANDBY & HYSTÉRÉSIS D'EXÉCUTION (V3 PRO) · Amendement : requalification et non-remontée de standby_force
#
# 📌 STATUT :
#   AMENDEMENT au contrat d'application `50_standby_hysteresis.md`
#
# 🎯 OBJET :
#   Requalifier explicitement le statut architectural de
#   `input_boolean.chauffage_standby_force` à la lumière de la
#   doctrine des registres (`01`), et inscrire l'invariant de
#   non-remontée vers le Niveau 1.
#
# 🧱 PRINCIPE DIRECTEUR DE L'AMENDEMENT :
#   Le contrat `50` n'était PAS doctrinalement fautif. Il décrivait
#   déjà le standby comme un verrou post-décision, pré-matériel,
#   subordonné. La dérive ne provenait pas de `50`, mais de la
#   COMPOSITION RUNTIME de `binary_sensor.chauffage_autorise_systeme`,
#   qui faisait remonter ce verrou en cause de Niveau 1.
#
#   Cet amendement confirme `50`, lève l'ambiguïté, et borne
#   explicitement ce que le standby a le droit d'alimenter.
#
# ==========================================================

---

## A1. Statut architectural confirmé et précisé

Le verrou `input_boolean.chauffage_standby_force` est qualifié de
**verrou de stabilisation thermique persisté et observable**.

Cette catégorie est intermédiaire et opposable. Elle se distingue de deux
catégories voisines avec lesquelles il ne doit jamais être confondu :

- Ce n'est **pas un simple mécanisme technique jetable** (un anti-rebond
  éphémère) : le domaine le persiste, l'historise via
  `input_datetime.chauffage_standby_force_changed`, et l'expose en
  diagnostic. Ces propriétés sont légitimes et conservées.

- Ce n'est **pas un état métier causal** au sens Arsenal : il n'est pas une
  cause de décision. Il est une **conséquence** de l'autorisation thermique
  (`sensor.chauffage_autorisation_cible`), traduite mécaniquement en verrou.

> Énoncé opposable : `standby_force` est une **conséquence de stabilisation,
> persistée et observable, jamais une cause décisionnelle**.

---

## A2. Confirmation du positionnement de `50`

Le positionnement déjà établi par `50` est confirmé sans réserve :

- le standby est **post-décision** et **pré-matériel** ;
- il **ne connaît ni la hiérarchie, ni les blocages, ni la présence** ;
- il **applique sans interpréter** une intention déjà décidée ;
- il constitue la **seule hystérésis d'exécution** du système.

La correspondance d'entrée demeure inchangée :

| Autorisation cible | Effet standby        |
|--------------------|----------------------|
| `neutre`           | aucune action        |
| `reduced`          | pose du verrou       |
| `comfort`          | levée du verrou      |

---

## A3. Invariant de non-remontée (application de D3)

> **Règle cardinale (non-remontée).**
> `input_boolean.chauffage_standby_force` ne compose **aucun** capteur de
> Niveau 1. En particulier, il n'entre pas dans la composition de
> `binary_sensor.chauffage_autorise_systeme`.
>
> Le standby, étant une conséquence de l'autorisation thermique, ne peut pas
> remonter se faire évaluer comme une interdiction de sécurité. Toute
> composition d'un capteur de sécurité par le standby constitue une inversion
> de responsabilité (violation de D3) et une régression architecturale.

Justification doctrinale : un état `standby_force = on` signifie « le confort
n'est pas requis » (sobriété, stabilisation). Le présenter comme
`chauffage_autorise_systeme = off` reviendrait à le présenter comme « le
chauffage est interdit » (sécurité). Ces deux significations appartiennent à
des registres irréductibles (D0). Leur fusion produit un diagnostic mensonger
et prive le capteur de sécurité de sa propriété cardinale : être
interprétable sans glose.

---

## A4. Where l'effet de l'autorisation `reduced` est-il porté ?

L'effet thermique de l'autorisation `reduced` est porté **au Niveau 3** de la
décision centrale (régime présence / autorisation cible), avec sa raison
propre `confort_suffisant`. Il n'a **pas** à être porté par une extinction de
`autorise_systeme`.

> Cette information n'est jamais perdue par la non-remontée : elle est déjà
> disponible au Niveau 3 via `sensor.chauffage_autorisation_cible`. Le câblage
> faisant remonter le standby en Niveau 1 était une **duplication** de cette
> information, dont une copie était mal étiquetée (interdiction au lieu de
> sobriété). Le retrait de cette copie ne perd aucune information.

---

## A5. Pilotage et observabilité — invariants conservés

- Le standby est piloté **exclusivement** par l'automation d'application de
  l'autorisation thermique (source : `sensor.chauffage_autorisation_cible`).
  Aucune autre automation, aucun script, aucune UI ne l'écrit.
- L'automation de journalisation du standby est en lecture seule : elle
  observe les transitions et horodate ; elle ne rétroagit jamais sur le
  verrou.
- Le standby reste historisé (`input_datetime.chauffage_standby_force_changed`,
  recorder) et exposé en diagnostic.

---

## A6. Invariants exposés (CI)

- **INV-STANDBY-1** — `standby_force` a un writer unique : l'automation
  d'application de l'autorisation thermique. Aucun autre écrivain.
- **INV-STANDBY-2** — `standby_force` n'entre pas dans la composition de
  `binary_sensor.chauffage_autorise_systeme` (ni d'aucun capteur de Niveau 1).
- **INV-STANDBY-4** — `standby_force` reste historisé et observable.

Note : l'invariant INV-STANDBY-3 (honnêteté de la raison en cas de
composition mixte) envisagé dans la phase d'analyse devient **sans objet** :
il n'était requis que dans l'hypothèse de repli (conservation du câblage
mixte). La désintrication étant retenue, il est abandonné.

---

## A7. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md) · [`01_doctrine_registres.md`](01_doctrine_registres.md)

**Complémentaire de :** [`30_decision_centrale.md`](30_decision_centrale.md) ·
[`70_autorisation_thermostat.md`](70_autorisation_thermostat.md) · [`80_table_decision_canonique.md`](80_table_decision_canonique.md)

**Gouverne directement :** `input_boolean.chauffage_standby_force` et
l'automation d'application de l'autorisation thermique.

---

## A8. Portée

Cet amendement confirme et précise `50` sans en réécrire la doctrine. Il prend
effet avec la publication de `01`, et conditionne l'amendement de `30`
(purification de `autorise_systeme`), qui ne peut être publié avant lui.

# ==========================================================
