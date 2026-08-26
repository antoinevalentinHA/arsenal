# CONTRAT ARSENAL — ASPIRATEUR
## 03 — Profils métier

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Figer les profils de nettoyage exposés à l'opérateur, les règles
d'écriture qui les réalisent, et le traitement de leurs prérequis matériels.

---

## 1. Table canonique des profils — arrêtée

| Profil métier | Aspiration | Intensité d'eau | Mode de nettoyage *(dérivé, jamais écrit)* | Prérequis matériel |
|---|---|---|---|---|
| **Aspiration normale** | `balanced` | `off` | `vacuum` | — |
| **Aspiration turbo** | `turbo` | `off` | `vacuum` | — |
| **Aspiration maximale** | `max` | `off` | `vacuum` | — |
| **Serpillière moyenne** | `quiet` | `medium` | `vac_and_mop` | serpillière posée |
| **Serpillière intensive** | `quiet` | `high` | `vac_and_mop` | serpillière posée |

**Cinq profils, et cinq seulement.**

> **`ASP-INV-10`** — Un profil demandé qui n'appartient pas à cette table est
> **refusé** au motif `PROFIL_INCONNU`. Il n'est jamais rapproché du profil « le
> plus proche », jamais corrigé, jamais remplacé par un défaut.

---

## 2. `gentle` est exclu

**Fait établi.** `gentle` **n'appartient pas** à la gradation de puissance
d'aspiration : la liste d'aspiration est composée à partir des bits de capacité
de l'appareil, avec un socle `quiet` · `balanced` · `turbo` · `max` auquel
`gentle` est **ajouté ensuite**. Son code protocolaire est par ailleurs
**supérieur** à celui de `max` — le code ne le classe donc pas comme un niveau
faible.

> **`ASP-INV-11`** — `gentle` n'est **jamais** exposé comme profil métier, jamais
> écrit par le domaine, et jamais interprété comme un niveau de puissance.

---

## 3. Le mode de nettoyage est dérivé — et ne doit jamais être écrit

**Fait établi, par lecture du code des versions en service.**

- **En lecture**, le mode de nettoyage n'a **pas d'existence propre** : il est
  **calculé** à partir des réglages bas niveau. Si l'intensité d'eau vaut `off`,
  le mode affiché est `vacuum` ; sinon `vac_and_mop`.
- **En écriture**, sélectionner un mode **n'écrit pas seulement l'eau** :
  l'intégration émet une commande unique qui impose d'un bloc l'aspiration, l'eau
  **et** le parcours — et l'aspiration qu'elle impose est **toujours `balanced`**,
  quelle que soit la valeur précédente.

> **`ASP-INV-12` — interdiction d'écriture du mode.** Le domaine **n'écrit jamais**
> `select.entree_roborock_q7_max_mode_de_nettoyage`. Le mode est **un état
> dérivé** : il se lit, il se **confirme**, il ne se commande pas.
>
> **Justification opposable.** Écrire le mode **après** avoir réglé l'aspiration
> écrase silencieusement le profil d'aspiration. Ce serait exactement le
> « fallback silencieux » que ce contrat proscrit — avec, en prime, une mission
> exécutée sous un profil que l'opérateur n'a pas demandé.

**Deux écritures, disjointes.** Le profil se réalise par **deux réglages
indépendants** — l'**intensité d'eau** et l'**aspiration**. Régler l'eau ne
touche pas l'aspiration. Le mode suit tout seul.

---

## 4. Prérequis matériel des profils avec eau

**Fait établi.** La présence de la serpillière est **observable**
(`binary_sensor.roborock_q7_max_serpilliere_fixee`) et **non commandable** :
poser ou retirer la serpillière est un **geste opérateur physique**.

C'est une **impossibilité physique**, catégorie **A** au sens de
[`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md) §5.

> **`ASP-INV-13`** — Tant que la serpillière est absente, les profils
> **Serpillière moyenne** et **Serpillière intensive** sont **refusés** au motif
> `PREREQUIS_MATERIEL_ABSENT`, avec un motif lisible nommant le geste attendu.
>
> **Symétrie obligatoire** (doctrine `commandabilite.md` §6.1) : aucun chemin —
> ni raccourci, ni UI, ni appel direct au moteur — ne présente ces profils comme
> lançables lorsque le prérequis est absent. Une impossibilité physique n'admet
> **aucun** override.

**Ce que le contrat n'exige pas.** Les autres témoins matériels du dock et du
réservoir sont des **observations** : ils enrichissent le diagnostic
([`08`](08_etats_et_observation.md)) et ne conditionnent, en V1, aucun refus
supplémentaire. Leur promotion en gate exigerait une preuve d'impossibilité
physique, qui n'est pas établie.

---

## 5. Le profil ne se conserve pas d'un cycle au suivant

**Fait établi terrain, reproduit deux fois.**

| Instant | Intensité d'eau / mode |
|---|---|
| Après écriture préparatoire | `off` / `vacuum` |
| **Au lancement** | inchangé |
| Pendant toute la mission | inchangé |
| **Au passage en `returning_home`** | **→ `medium` / `vac_and_mop`** |

La bascule coïncide **à la seconde** avec l'entrée en retour au dock. La
puissance d'aspiration, elle, n'est jamais touchée et reste à la valeur posée.
La **cause interne** de ce rétablissement n'est **pas attribuée** — seul le
**moment** est établi.

Trois règles opposables en découlent :

> **`ASP-INV-14` — écriture avant chaque mission.** L'intensité d'eau **et** la
> puissance d'aspiration sont écrites **explicitement avant chaque lancement**,
> même lorsque l'état courant paraît déjà conforme. Aucune mission ne s'appuie
> sur un réglage hérité du cycle précédent.

> **`ASP-INV-15` — l'état post-cycle ne prouve rien.** L'intensité d'eau et le
> mode lus **après** une mission **ne prouvent pas** le profil utilisé **pendant**
> cette mission. Aucun diagnostic, aucune restitution, aucune trace du domaine ne
> peut conclure sur le profil d'un cycle à partir d'une lecture postérieure à son
> entrée en retour au dock.

> **`ASP-INV-16` — la sélection UI représente l'intention, pas l'appareil.** Le
> profil présenté à l'opérateur est **l'intention qu'il a exprimée**
> ([`05`](05_intention_de_mission.md)). Il n'est **jamais déduit** du profil
> courant remonté par l'appareil, ni recalé sur lui après mission.

**Ce que le terrain rend praticable.** Le réglage posé **avant** le lancement
**tient pendant toute la mission**. C'est ce fait — et lui seul — qui rend la
séquence « régler, confirmer, puis lancer » réalisable
([`07`](07_moteur_de_mission.md)).

---

## 6. Confirmation obligatoire avant la commande

> **`ASP-INV-17`** — Aucun réglage n'est réputé appliqué du seul fait d'avoir été
> demandé. Chaque écriture de profil est suivie d'une **relecture de
> confirmation** ; un réglage non confirmé **refuse la mission** au motif
> `REGLAGE_NON_CONFIRME` — il ne la laisse **jamais** partir sous un profil
> incertain.

La confirmation porte sur :

1. l'**intensité d'eau** effectivement lue ;
2. le **mode dérivé** cohérent avec elle (`off` ⇒ `vacuum`, sinon `vac_and_mop`) —
   contrôle de cohérence, **jamais** une écriture ;
3. la **puissance d'aspiration** effectivement lue.

> **Régimes `unknown` / `unavailable`.** Conformément à
> [`principes_generaux.md`](../../architecture/03_doctrines/principes_generaux.md)
> §6 et §8, une lecture `unknown` ou `unavailable` **ne vaut ni la valeur
> demandée, ni une valeur nominale, ni `false`** : elle vaut **absence de
> confirmation**, et conduit au refus. Le cas est réel sur cet appareil — le
> parcours de lavage de sol a été observé à `unknown`.

---

## 7. Ce que le domaine n'écrit jamais

| Réglage | Statut |
|---|---|
| Mode de nettoyage | **Interdit** — dérivé, et destructeur en écriture (§3) |
| Parcours de lavage de sol | **Non écrit** — n'appartient à aucun profil arrêté ; observé à `unknown`, traité comme tel |
| Nombre de passages via un réglage d'appareil | **Sans objet** — aucune entité ne le porte ; il vit dans la charge utile de la commande ([`04`](04_nombre_de_passages.md)) |

---

## Renvois

- Nombre de passages : [`04_nombre_de_passages.md`](04_nombre_de_passages.md)
- Séquence de lancement : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Refus `PROFIL_INCONNU`, `PREREQUIS_MATERIEL_ABSENT`, `REGLAGE_NON_CONFIRME` : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Doctrine de commandabilité (catégories A / B) : [`commandabilite.md`](../../architecture/03_doctrines/commandabilite.md)
- Index du domaine : [`README.md`](README.md)
