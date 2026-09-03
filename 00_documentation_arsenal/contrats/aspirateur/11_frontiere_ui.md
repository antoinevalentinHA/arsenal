# CONTRAT ARSENAL — ASPIRATEUR
## 11 — Frontière backend / UI

**Version contrat :** v1.0
**Statut :** Normatif — **clause de frontière**
**Objet :** Borner ce que l'UI du domaine aura le droit de faire, **sans la
concevoir**.

> **Ce chapitre ne conçoit aucun dashboard, aucune carte, aucun template.** La
> conception de l'UI Aspirateur relève d'un **lot ultérieur**. Ce chapitre fixe
> les contraintes que ce lot devra respecter — il ne les anticipe pas.

---

## 1. Principe

> **Le backend décide. L'UI rend et sollicite.**

| Backend | UI |
|---|---|
| Valide une intention | **Sollicite** les quatre champs de l'intention |
| Décide du refus et de son motif | **Restitue** le motif tel quel |
| Écrit les réglages et émet la commande | **Appelle le moteur** — jamais l'appareil |
| Qualifie l'issue | **Affiche** l'issue qualifiée |
| Détient les états canoniques | **Projette** les états canoniques |

Cette symétrie est celle de
[`ui/architecture_transverse.md`](../../ui/architecture_transverse.md) ; ce
chapitre l'instancie pour le domaine sans la redéfinir.

---

## 2. Interdits opposables à l'UI du domaine

| Interdit | Motif |
|---|---|
| **Émettre une commande brute** vers le robot — commande de mission, réglage, sélection de carte, interruption, retour à la base | `ASP-INV-31` — écrivain unique |
| **Exposer une entité native d'action** du robot dans Lovelace | `ASP-INV-31` |
| **Dupliquer la table des segments, la table des profils ou les périmètres prédéfinis** | Une source unique par référentiel ([`02`](02_referentiel_cartes_et_pieces.md), [`03`](03_profils_metier.md)) |
| **Recalculer une validation** — appartenance d'un segment à une carte, cohérence multi-carte, admissibilité d'un profil | `ASP-INV-31`, `ASP-IMC-1` — la validation est backend |
| **Décider d'un refus** ou en **reformuler le motif** | [`09`](09_refus_et_diagnostics.md) — le motif est produit par le backend |
| **Déduire l'état du domaine** d'une combinaison de témoins natifs | [`08`](08_etats_et_observation.md) — les états canoniques sont produits par le backend |
| **Restituer un libellé de pièce ou de carte issu du robot** | `ASP-INV-7` |
| **Afficher un index de segment nu** | `ASP-INV-6` |
| **Présenter comme disponible un geste sans sens physique**, ou un profil dont le prérequis matériel est absent | `ASP-INV-13`, `ASP-INV-48` ; [`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md) §6.1 |
| **Recaler la sélection de profil sur le profil courant remonté après mission** | `ASP-INV-16` |
| **Masquer une indisponibilité** derrière un état nominal ou une dernière valeur connue | `ASP-INV-45` |
| **Lire directement le helper de verdict de mission** | L'UI **consomme la projection métier** (`ASP-INV-96`) ; elle ne recalcule ni ne teste la classe du verdict. Cette interdiction est **mécaniquement** garantie, et son ouverture nominative à un lecteur pur ne la relâche pas |
| **Restituer sous un même libellé la mission Arsenal ouverte et la session robot active** | Deux notions, deux autorités, deux rendus ([`08`](08_etats_et_observation.md) §1.1, `ASP-INV-44`) |
| **Adosser la navigation du domaine au verdict** ou à la projection métier | La tuile de navigation restitue une **présence physique** ; elle reste adossée à l'**activité physique** du robot (§3 bis) |

---

## 3. Ce que l'UI doit faire

1. **Solliciter une intention complète** avant de proposer le lancement — les
   quatre champs, sans complétion implicite (`ASP-INV-23`).
2. **Représenter l'intention opérateur**, pas l'état de l'appareil, sur la
   sélection de profil et de passages (`ASP-INV-16`).
3. **Restituer les états canoniques distinctement** — les **dix** du
   chapitre [`08`](08_etats_et_observation.md), sans agrégation de confort
   (`ASP-INV-44`). La **session robot active** se superpose aux neuf autres et se
   rend **séparément**, jamais fondue dans la valeur d'état (`ASP-INV-68`).
4. **Restituer les motifs de refus et d'échec** tels que produits, de façon
   lisible et non tronquée (`ASP-INV-50`).
5. **Isoler l'action de la lecture** — les cartes d'action sont physiquement
   séparées des cartes d'état, conformément à la doctrine UI transverse.
6. **Confirmer explicitement** le lancement d'une mission : c'est une action
   physique sur un équipement mobile, jamais un basculement d'un clic.
7. **Employer l'autorité adaptée à chaque usage** — l'**autorité métier** pour ce
   qui relève de la responsabilité d'Arsenal, l'**autorité native** pour ce qui
   relève de l'activité physique du robot
   ([`08`](08_etats_et_observation.md) §1.1). Les deux peuvent **légitimement
   diverger**, et l'interface ne résorbe pas cette divergence : elle la **rend**.
8. **Restituer les deux notions sous des libellés distincts** — ce qui est rendu
   comme **mission Arsenal** ne porte jamais le libellé de ce qui est rendu comme
   **session robot**. La mission Arsenal se lit sur la **projection métier**
   (`ASP-INV-96`) ; la session robot se lit sur l'attribut orthogonal du
   chapitre [`08`](08_etats_et_observation.md) §1.

---

## 3 bis. Navigation — adossée à l'activité physique

La tuile du domaine dans la navigation Arsenal restitue une **présence physique**.
Sa coloration reste adossée à l'**activité physique du robot** — état canonique et
classe de partition —, **jamais** au verdict ni à la projection métier.

**C'est une décision, pas un état de fait à faire évoluer.** Y substituer la
responsabilité métier changerait la réalité que la couleur donne à lire : un robot
physiquement actif sur une mission externe cesserait d'être signalé, et une mission
Arsenal ouverte robot immobile serait peinte comme une activité. Les deux seraient
faux.

**L'abstention est conservée** : lorsque l'état du domaine est inobservable, le
colorant **s'abstient** plutôt que de peindre un nominal (`ASP-INV-45`).

---

## 4. Ce que ce chapitre ne tranche pas

- **La conception du dashboard Aspirateur** — cartes, disposition, navigation,
  couleurs : **lot ultérieur**.
- **La place du domaine dans la navigation Arsenal** — y compris toute
  réorganisation d'un domaine voisin. Ce point **ne relève pas du métier
  Aspirateur** et n'est **pas** intégré à ce contrat
  ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)).
- **Toute entrée de hub ou de carte des domaines** : la couche navigation est
  **non normative et détachable**, et ce lot ne la modifie pas.

---

## Renvois

- Doctrine UI transverse : [`../../ui/architecture_transverse.md`](../../ui/architecture_transverse.md)
- Référence normative UI : [`../../ui/README.md`](../../ui/README.md)
- États canoniques : [`08_etats_et_observation.md`](08_etats_et_observation.md)
- Refus et diagnostics : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Index du domaine : [`README.md`](README.md)
