# CONTRAT ARSENAL — ASPIRATEUR
## 10 — Raccourcis

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir ce qu'est un raccourci, ce qu'il fait, et surtout ce qu'il
n'a pas le droit d'être.

---

## 1. Définition

> **Un raccourci est un préréglage d'intention.** Il **préremplit** les quatre
> champs d'une intention de mission ([`05`](05_intention_de_mission.md)), puis
> appelle le **moteur commun** ([`07`](07_moteur_de_mission.md)).

**Un raccourci n'est pas un mode de nettoyage, ni une commande, ni une
fonctionnalité distincte.** C'est un gain de gestes, et rien de plus.

> **`ASP-INV-54` — même moteur, même chemin.** Un raccourci traverse **exactement**
> la même validation, la même séquence, les mêmes refus et la même qualification
> d'issue qu'une sélection libre. Il n'existe **aucun** chemin plus court vers
> l'appareil.

---

## 2. Ce qu'un raccourci ne fait jamais

| Interdit | Motif |
|---|---|
| **Émettre directement une commande Roborock** | Violerait l'écrivain unique (`ASP-INV-31`) et contournerait `ASP-IMC-1` |
| **Dupliquer la table des segments** | Le référentiel a **une** source ([`02`](02_referentiel_cartes_et_pieces.md)). Une copie dérive, et une copie dérivée désigne la mauvaise pièce. |
| **Embarquer sa propre logique de profil** | Les profils ont **une** table ([`03`](03_profils_metier.md)) |
| **Contourner les validations de carte** | `ASP-IMC-1` s'applique intégralement ([`06`](06_integrite_mono_carte.md)) |
| **Posséder son propre écrivain** | `ASP-INV-31` |
| **Court-circuiter un refus** | Un raccourci refusé est refusé, avec le même motif lisible ([`09`](09_refus_et_diagnostics.md)) |
| **Composer plusieurs cartes** | `ASP-INV-28` — un raccourci « toute la maison » **n'existe pas** en V1 |

> **`ASP-INV-55` — pas de raccourci multi-carte.** Les trois périmètres métier
> visés sont portés par **trois cartes distinctes**. Un raccourci ne peut donc
> jamais en couvrir plus d'un. « Toute la maison » serait une mission composite —
> ce que la contrainte physique interdit.

---

## 3. Raccourcis attendus — V1

Ces raccourcis découlent directement des périmètres prédéfinis
([`02`](02_referentiel_cartes_et_pieces.md) §3). Chacun fixe **carte** et
**segments** ; **profil** et **passages** restent des champs de l'intention.

| Raccourci | Carte | Segments préremplis |
|---|---|---|
| **RDC complet** | `0` | `0_16` · `0_18` · `0_20` · `0_21` |
| **Étage complet** | `1` | les **huit** segments, `1_22` `WC Étage` incluse |

**Deux périmètres, trois raccourcis.** Le périmètre RDC est exposé **deux
fois** : une fois en aspiration, une fois en serpillière. Un périmètre n'est
pas un raccourci — le chapitre [`02`](02_referentiel_cartes_et_pieces.md) §3 en
recense **cinq**, et il continue de tous les recenser : ce chapitre décide
seulement **lesquels reçoivent un bouton**, et **avec quels réglages par
défaut**.

### 3.1 Réglages par défaut — proposés, jamais imposés

| Raccourci | Périmètre | Profil par défaut | Passages par défaut |
|---|---|---|---|
| **RDC — aspiration complète** | RDC complet | Aspiration normale | 3 passages |
| **RDC — serpillière complète** | RDC complet | Serpillière moyenne | 3 passages |
| **Étage — aspiration complète** | Étage complet | Aspiration normale | 3 passages |

**Correspondance des réglages avec la table canonique du chapitre
[`03`](03_profils_metier.md) §1**, sans vocabulaire parallèle :

| Réglage demandé | Profil canonique | Aspiration | Eau |
|---|---|---|---|
| aspiration moyenne, aucune eau | **Aspiration normale** | `balanced` | `off` |
| aspiration la plus faible, eau moyenne | **Serpillière moyenne** | `quiet` | `medium` |

> **`ASP-INV-56` — le raccourci ne présume ni le profil ni les passages.** Un
> raccourci qui figerait un profil ou un nombre de passages **sans que
> l'opérateur les ait choisis** violerait l'atomicité de l'intention
> (`ASP-INV-23`) et la règle d'écriture avant chaque mission (`ASP-INV-14`).
>
> Un raccourci **peut** proposer un profil et un nombre de passages **par
> défaut** — à condition qu'ils soient **visibles, modifiables avant lancement**,
> et jamais appliqués implicitement.

**Ce que le §3.1 exerce, et ce qu'il ne change pas.** Les réglages ci-dessus
sont la **faculté** déjà ouverte par le second alinéa d'`ASP-INV-56`, et rien
de plus. Ils sont **écrits dans les helpers d'intention**, donc **visibles**
dans la composition et **modifiables** avant tout lancement ; ils ne sont
**jamais** appliqués implicitement à une mission. L'atomicité de l'intention
reste entière : au moment du lancement, les quatre champs sont renseignés et
**l'opérateur les a sous les yeux**.

> **Un raccourci ne lance rien.** Il écrit une composition, et s'arrête. Le
> bouton de lancement demeure l'**unique autorité de lancement**, et il exige
> une confirmation ([`11`](11_frontiere_ui.md) §3.6).

---

## 4. Extension d'un raccourci

> **`ASP-INV-57`** — Créer, modifier ou supprimer un raccourci est un acte
> **contractuel**, pas un ajustement d'interface : il modifie la table du §3, et
> exige une entrée de changelog. Un raccourci qui n'existe pas ici **n'existe
> pas**.

Un nouveau raccourci ne peut porter que des segments **du référentiel V1** et
**d'une seule carte**.

---

## Renvois

- Référentiel et périmètres prédéfinis : [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md)
- Intention de mission : [`05_intention_de_mission.md`](05_intention_de_mission.md)
- Moteur commun : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Frontière UI : [`11_frontiere_ui.md`](11_frontiere_ui.md)
- Index du domaine : [`README.md`](README.md)
