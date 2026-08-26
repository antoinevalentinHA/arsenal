# CONTRAT ARSENAL — ASPIRATEUR
## 09 — Refus et diagnostics

**Version contrat :** v1.0
**Statut :** Normatif — **catalogue opposable**
**Objet :** Fixer les motifs de refus et d'échec du domaine, leur vocabulaire
canonique, et l'exigence d'intelligibilité.

---

## 1. Principe

> **`ASP-INV-50` — un refus est un livrable.** Toute demande qui n'aboutit pas
> produit un **motif lisible**, nommant **ce qui manque** et, lorsque c'est un
> geste, **quel geste est attendu**. Un refus muet, un bouton inerte ou une
> commande avalée sans trace sont **non conformes**.

> **`ASP-INV-51` — aucun fallback silencieux.** Aucun motif de refus ne peut
> être contourné par une valeur de repli, une troncature du périmètre, un profil
> de substitution ou une seconde tentative implicite. Le refus **arrête** la
> séquence.

**Deux natures, à ne pas confondre.**

| Nature | Moment | Sens |
|---|---|---|
| **Refus** | **Avant** émission | La mission **n'a pas été lancée** |
| **Échec** | **Après** émission | La mission a été lancée et **n'a pas abouti** comme attendu |

Les présenter identiquement serait mentir sur ce que l'appareil a fait.

---

## 2. Catalogue des refus (avant émission)

Les codes ci-dessous sont un **vocabulaire de diagnostic** du domaine — au sens
des codes décisionnels du domaine alarme
([`../alarme/10_modele_etats_et_vocabulaire.md`](../alarme/10_modele_etats_et_vocabulaire.md)).
Ils ne sont **ni des entités, ni des identifiants Home Assistant**.

| Code | Déclenché quand | Contrat portant la règle |
|---|---|---|
| `SELECTION_VIDE` | L'intention ne porte aucun segment, ou un champ obligatoire manque | [`05`](05_intention_de_mission.md) |
| `SEGMENT_INCONNU` | Un segment demandé n'appartient pas au référentiel V1 — **y compris** un segment présent dans la carte mais hors référentiel | [`02`](02_referentiel_cartes_et_pieces.md) |
| `SELECTION_MULTI_CARTE` | Les segments demandés relèvent de plusieurs cartes | [`06`](06_integrite_mono_carte.md) |
| `CARTE_NON_CONFIRMEE` | La carte n'a pas été sélectionnée, la sélection n'a pas été confirmée, les pièces exposées ne concordent pas avec le référentiel, ou la carte active est illisible | [`06`](06_integrite_mono_carte.md) |
| `PROFIL_INCONNU` | Le profil demandé n'appartient pas aux cinq profils arrêtés | [`03`](03_profils_metier.md) |
| `PASSAGES_HORS_CONTRAT` | Le nombre de passages n'est ni `×1`, ni `×2`, ni `×3` | [`04`](04_nombre_de_passages.md) |
| `PREREQUIS_MATERIEL_ABSENT` | Un profil avec eau est demandé alors que la serpillière est absente | [`03`](03_profils_metier.md) |
| `ROBOT_INDISPONIBLE` | L'état machine vaut `device_offline`, ou une entité décisive vaut `unknown` / `unavailable` | [`07`](07_moteur_de_mission.md) §5.0, §5.2 |
| `ETAT_NON_QUALIFIE` | L'état machine porte une valeur que ce contrat ne classe pas — **classe N** de la partition | [`07`](07_moteur_de_mission.md) §5.0, `ASP-INV-60` |
| `ERREUR_EQUIPEMENT` | L'état machine vaut `error`, **ou** l'un des deux témoins d'erreur n'est pas à sa valeur nominale — `none` pour l'aspirateur, `ok` pour le dock | [`07`](07_moteur_de_mission.md) §5.2 |
| `MISSION_DEJA_OUVERTE` | L'état machine est en **classe A** — `cleaning`, `segment_cleaning`, `zoned_cleaning`, `paused`, `returning_home`, `docking` | [`07`](07_moteur_de_mission.md) §5.0, [`08`](08_etats_et_observation.md) §3.1 |
| `SESSION_INACHEVEE` | L'état machine est en **classe R** (repos admissible) **et** le témoin de session vaut `on` | [`07`](07_moteur_de_mission.md) §5.4, [`08`](08_etats_et_observation.md) §3.1, arbitrage `ARB-2` |
| `REGLAGE_NON_CONFIRME` | Une écriture d'intensité d'eau ou d'aspiration n'a pas été confirmée par relecture | [`03`](03_profils_metier.md) §6 |

> **`ASP-INV-65` — le catalogue est total sur l'état machine.** Les motifs
> `MISSION_DEJA_OUVERTE`, `ERREUR_EQUIPEMENT`, `ROBOT_INDISPONIBLE`,
> `ETAT_NON_QUALIFIE` et `SESSION_INACHEVEE` **couvrent toutes** les valeurs
> possibles de l'état machine, sans recouvrement : la partition de
> [`07`](07_moteur_de_mission.md) §5.0 est exhaustive par construction, et
> l'ordre d'arbitrage de [`08`](08_etats_et_observation.md) §3.1 rend le motif
> **déterministe**. Aucun état ne produit deux motifs ; aucun n'en produit zéro.

> **`ASP-INV-52` — extension gouvernée.** Ajouter un code de refus implique la
> mise à jour de ce catalogue, du chapitre qui porte la règle, et une entrée de
> changelog. Un motif de refus qui n'existe pas ici **n'existe pas**.

---

## 3. Catalogue des échecs (après émission)

| Code | Déclenché quand | Ce qu'il ne dit pas |
|---|---|---|
| `CANAL_INDISPONIBLE` | La demande n'est pas parvenue à Home Assistant | **Ne qualifie pas** la commande Roborock — elle peut être parfaitement valide |
| `COMMANDE_REJETEE` | La commande a été refusée à l'émission | Ne dit rien d'un problème de canal |
| `TRANSITION_NON_OBSERVEE` | La commande a été acceptée, mais aucune transition d'état attendue n'a été observée dans la fenêtre retenue | **Ne conclut ni au succès ni à l'immobilité** : il constate une absence de preuve |
| `MISSION_INTERROMPUE` | La mission s'est arrêtée avant son terme, hors geste opérateur | Ne présume pas la cause |
| `ERREUR_EN_MISSION` | Une erreur robot ou dock est survenue en cours de mission | — |

> **La fenêtre d'observation de `TRANSITION_NON_OBSERVEE` n'est pas chiffrée par
> ce contrat.** Aucun précédent ni arbitrage ne fonde une valeur ; la fixer ici
> serait inventer un seuil
> ([`13`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md), `ARB-3`).

---

## 4. Qualité d'un motif lisible

Un motif est **intelligible** lorsqu'il permet à l'opérateur de savoir **quoi
faire ensuite**, sans lire ce contrat ni ouvrir un journal.

| Exigence | Illustration de ce qui est attendu |
|---|---|
| **Nommer l'objet en cause** | La pièce, la carte, le profil ou le réglage concerné — sous son **libellé canonique Arsenal** ([`02`](02_referentiel_cartes_et_pieces.md) §5) |
| **Nommer le manque** | « la carte n'a pas été confirmée », et non « erreur de validation » |
| **Nommer le geste attendu**, quand il y en a un | Poser la serpillière ; arrêter la session ouverte ; réessayer plus tard |
| **Ne pas exposer de mécanique interne** | Ni index de segment nu, ni nom d'entité, ni code protocolaire |

> **`ASP-INV-53`** — Un motif de refus **ne restitue jamais** un libellé de pièce
> ou de carte provenant directement du robot (`ASP-INV-7`), ni un index de
> segment nu (`ASP-INV-6`).

---

## 5. Ce qu'un diagnostic ne fait jamais

- ❌ **Conclure sur le profil d'un cycle** à partir d'une lecture postérieure à
  son entrée en retour au dock (`ASP-INV-15`).
- ❌ **Conclure sur le nombre de passages réalisé** à partir de la surface
  (`ASP-INV-20`).
- ❌ **Conclure à l'invalidité d'une commande** sur la seule foi d'une erreur de
  transport (`ASP-INV-37`).
- ❌ **Présenter une acceptation comme un démarrage** (`ASP-INV-38`).
- ❌ **Traiter `unknown` ou `unavailable`** comme `false` ou comme une valeur
  nominale (`ASP-INV-45`).
- ❌ **Requalifier une décision** : le diagnostic observe, il ne décide pas
  ([`separation_decision_action.md`](../../architecture/03_doctrines/separation_decision_action.md)).

---

## Renvois

- Séquence et issues : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- États et autorité des témoins : [`08_etats_et_observation.md`](08_etats_et_observation.md)
- Frontière UI (restitution du motif) : [`11_frontiere_ui.md`](11_frontiere_ui.md)
- Arbitrages : [`13_hors_perimetre_arbitrages_et_questions_ouvertes.md`](13_hors_perimetre_arbitrages_et_questions_ouvertes.md)
- Index du domaine : [`README.md`](README.md)
