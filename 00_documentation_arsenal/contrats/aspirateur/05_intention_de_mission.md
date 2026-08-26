# CONTRAT ARSENAL — ASPIRATEUR
## 05 — Intention de mission

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir l'**intention de mission** comme objet **complet, atomique et
opposable**, et la séparer strictement de sa validation et de son exécution.

---

## 1. Trois objets strictement distincts

| Objet | Question | Couche | Contrat |
|---|---|---|---|
| **Intention** | *Que demande l'opérateur ?* | Décision (portée par l'opérateur) | ce document |
| **Validation** | *Cette demande peut-elle aboutir, ici et maintenant ?* | Décision (portée par Arsenal) | [`06`](06_integrite_mono_carte.md), [`09`](09_refus_et_diagnostics.md) |
| **Exécution** | *Réglages, émission, qualification de l'issue* | Action | [`07`](07_moteur_de_mission.md) |

> **`ASP-INV-22` — invariant de non-confusion.** Une intention n'est **pas** une
> autorisation : elle peut être parfaitement formée et néanmoins refusée. Une
> autorisation n'est **pas** une exécution : elle peut être acquise et la mission
> échouer. Le domaine ne présente jamais l'un pour l'autre.

Cette séparation reprend la doctrine besoin → intention → exécution du domaine
arrosage ([`../arrosage/05_intention.md`](../arrosage/05_intention.md)) et la
séparation décision / action
([`separation_decision_action.md`](../../architecture/03_doctrines/separation_decision_action.md)).

---

## 2. Composition d'une intention — quatre champs, tous obligatoires

Une intention de mission (`‹intention_courante›`, conceptuel) est **complète**
lorsqu'elle porte, simultanément :

| Champ | Domaine de valeurs | Contrat |
|---|---|---|
| **Carte** | Une carte du référentiel V1 — `0` RDC, `1` Étage, `2` Annexe | [`02`](02_referentiel_cartes_et_pieces.md) |
| **Segments** | Une **ou plusieurs** paires `‹carte›_‹segment›` du référentiel, **toutes de la carte désignée** | [`02`](02_referentiel_cartes_et_pieces.md), [`06`](06_integrite_mono_carte.md) |
| **Profil** | L'un des **cinq** profils arrêtés | [`03`](03_profils_metier.md) |
| **Passages** | `×1`, `×2` ou `×3` | [`04`](04_nombre_de_passages.md) |

> **`ASP-INV-23` — atomicité.** Le moteur ne reçoit **jamais** une intention
> partielle. Une demande à laquelle il manque un champ est **refusée**, jamais
> complétée par un défaut, jamais complétée par « la dernière valeur utilisée »,
> jamais complétée par l'état courant de l'appareil.

**Pourquoi l'atomicité, et pas la complétion.** Compléter une intention
reviendrait à décider à la place de l'opérateur, sur une base invisible pour lui.
Une mission lancée sous un profil ou un nombre de passages **hérités** est
précisément l'accident que ce domaine existe pour empêcher
([`03`](03_profils_metier.md) §5).

---

## 3. La carte est une désignation, jamais une déduction

> **`ASP-INV-24`** — La carte de l'intention est **désignée explicitement par
> l'opérateur**. Elle n'est **jamais** déduite :
>
> - ni de la position physique supposée du robot ;
> - ni de la carte actuellement sélectionnée sur l'appareil ;
> - ni de l'appartenance des segments demandés — c'est l'inverse qui est vrai :
>   les segments sont **validés contre** la carte désignée
>   ([`06`](06_integrite_mono_carte.md)).

**Fait établi.** Le sélecteur de carte exprime une **sélection**, pas une
**localisation** : après transport manuel du robot de l'Étage jusqu'à sa base au
RDC, le sélecteur est **resté sur `Étage`**. Il ne se recale pas de lui-même.

---

## 4. Régimes des entrées de l'intention

Conformément à
[`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
§6, chaque entrée de l'intention est traitée dans ses trois régimes :

| Entrée | Valeur nominale | Valeur absente | Valeur incohérente |
|---|---|---|---|
| Carte | Carte du référentiel | Refus `SELECTION_VIDE` | Refus `CARTE_NON_CONFIRMEE` ou `SEGMENT_INCONNU` selon le cas |
| Segments | ≥ 1 paire du référentiel | Refus `SELECTION_VIDE` | Refus `SEGMENT_INCONNU` (hors référentiel) ou `SELECTION_MULTI_CARTE` (cartes mêlées) |
| Profil | L'un des cinq | Refus `PROFIL_INCONNU` | Refus `PROFIL_INCONNU` |
| Passages | `×1` / `×2` / `×3` | Refus `PASSAGES_HORS_CONTRAT` | Refus `PASSAGES_HORS_CONTRAT` |

> **`ASP-INV-25`** — **Aucune entrée absente ou incohérente ne produit un
> comportement par défaut.** `unknown` et `unavailable` ne valent **ni `false`,
> ni une valeur nominale, ni une valeur de substitution**
> ([`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
> §8). Ils valent **absence**, et l'absence refuse.

---

## 5. Une intention est instantanée, jamais persistante

> **`ASP-INV-26`** — Une intention vaut **pour une mission**. Elle n'est ni un
> réglage durable, ni un profil attaché à une pièce, ni une préférence mémorisée
> par l'appareil.

**Fait établi.** L'expérience opérateur de l'application officielle redéfinit la
carte, les pièces, l'aspiration, l'eau et le nombre de passages **à chaque
nouvelle préparation** de nettoyage : aucun profil persistant par pièce n'y est
exposé. Le contrat s'aligne sur cette réalité — **sans affirmer** qu'un tel
profil persistant n'existe pas techniquement dans l'appareil, ce qui n'est pas
établi.

**Conséquence.** Le domaine peut **restituer** la dernière intention lancée à
titre de trace ([`08`](08_etats_et_observation.md)) ; il ne la **rejoue jamais**
implicitement.

---

## 6. Ce que l'intention ne fait pas

- ❌ elle **ne sélectionne pas** la carte sur l'appareil — c'est une étape
  d'exécution ([`07`](07_moteur_de_mission.md)) ;
- ❌ elle **n'écrit aucun réglage** ;
- ❌ elle **n'émet aucune commande** ;
- ❌ elle **ne garantit pas** son propre aboutissement — la validation lui est
  postérieure et peut la refuser ;
- ❌ elle **n'est pas** un état de l'appareil, et ne se relit jamais depuis lui.

---

## Renvois

- Référentiel de désignation : [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md)
- Intégrité mono-carte : [`06_integrite_mono_carte.md`](06_integrite_mono_carte.md)
- Moteur et séquence : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Catalogue des refus : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Raccourcis (préremplissage d'intention) : [`10_raccourcis.md`](10_raccourcis.md)
- Index du domaine : [`README.md`](README.md)
