# CONTRAT ARSENAL — ASPIRATEUR
## 04 — Nombre de passages

**Version contrat :** v1.0
**Statut :** Normatif — antérieur au runtime
**Objet :** Figer les valeurs de passages exposées, leur encodage, et l'invariant
qui protège contre la confusion de conventions.

---

## 1. Trois valeurs, et trois seulement

| Valeur exposée | Encodage dans la charge utile | Niveau de preuve |
|---|---|---|
| **`×1`** | **absence du champ `repeat`** | **Preuve terrain** — essai T1 |
| **`×2`** | `repeat: 2` | **Preuve terrain** — essai T2 |
| **`×3`** | `repeat: 3` | **Déduction protocolaire**, cohérente avec la sémantique de comptage établie et avec la capacité `×3` offerte par l'application officielle sur cet appareil — **non testée par Arsenal**, **acceptée explicitement par l'opérateur** |

> **`ASP-INV-18`** — Toute valeur de passages hors `{×1, ×2, ×3}` est **refusée**
> au motif `PASSAGES_HORS_CONTRAT`. Elle n'est jamais bornée au plus proche,
> jamais arrondie, jamais ramenée à un défaut.

> **Honnêteté du niveau de preuve.** Le contrat **n'affirme pas** que `×3` a été
> vérifié sur le terrain. Il **assume** une déduction, et l'inscrit comme telle.
> Un futur essai qui la contredirait invaliderait cette ligne — et elle seule.

---

## 2. La convention est une sémantique de **comptage**

**Fait établi terrain.** `repeat: 2` produit **deux passages**. La comparaison
T1 / T2 sur la même cible est sans ambiguïté : durée de nettoyage `× 1,89` pour
une surface finale identique.

> **`ASP-INV-19` — jamais de transposition de convention.** La commande de
> nettoyage **zoné** porte une convention **décalée**, où `0` vaut un seul
> nettoyage. Cette convention **ne s'applique pas** à la commande segmentée et
> **ne doit jamais y être transposée**. Toute lecture, toute documentation, tout
> futur runtime qui écrirait `repeat: 1` pour obtenir deux passages, ou `repeat: 0`
> pour en obtenir un, est **non conforme**.

**Pourquoi cet invariant existe.** Une passe antérieure de l'audit **avait commis
exactement cette erreur** : appliquer la convention zonée à la commande
segmentée. Le terrain l'a corrigée. L'invariant est écrit pour que la correction
ne se reperde pas.

---

## 3. Comment se lit une preuve de passages

**Enseignement de méthode, opposable au diagnostic du domaine.**

- **La durée est le discriminant du nombre de passages.**
- **La surface est le discriminant du périmètre.**

La surface mesure l'**aire couverte** : repasser sur une zone déjà comptabilisée
**n'y ajoute rien**. Une surface qui plafonne pendant que la durée continue de
croître **est** la signature d'un repassage, pas une anomalie.

> **`ASP-INV-20`** — Aucun diagnostic du domaine ne conclut au nombre de passages
> effectué à partir de la surface de nettoyage. Le domaine **n'affirme pas** un
> nombre de passages réalisé : il rappelle le nombre **demandé**, qui est une
> propriété de l'intention ([`05`](05_intention_de_mission.md)).

---

## 4. Le nombre de passages est indépendant du profil

**Fait établi.** Aucune entité du registre ne porte le nombre de passages — ni
active, ni désactivée. Il n'est **pas** réglable par une entité : il vit **dans
la charge utile de la commande**.

> **`ASP-INV-21`** — Le nombre de passages est une **composante à part entière de
> l'intention de mission**, au même titre que la carte, les segments et le profil
> ([`05`](05_intention_de_mission.md)). Il n'est ni dérivé du profil, ni attaché à
> un périmètre, ni mémorisé par l'appareil.

**Corollaire.** Un profil ne « contient » jamais un nombre de passages, et un
raccourci qui fixe les deux les fixe comme **deux champs distincts** d'une même
intention ([`10`](10_raccourcis.md)).

---

## 5. Dépendance assumée — ce que coûte cette voie

Le nombre de passages n'est atteignable que par la **commande segmentée directe**
([`07`](07_moteur_de_mission.md)) : le service Home Assistant de nettoyage par
pièces **ne porte pas ce champ**. Le contrat **assume** cette dépendance, et en
écrit les contreparties :

| Contrepartie | Conséquence contractuelle |
|---|---|
| Aucune résolution d'areas, aucun contrôle de carte active, aucune borne vérifiée, aucun message d'erreur intelligible n'est apporté par la couche d'exposition | **Toutes ces garanties sont réimplémentées côté Arsenal** — c'est l'objet des chapitres [`06`](06_integrite_mono_carte.md), [`07`](07_moteur_de_mission.md) et [`09`](09_refus_et_diagnostics.md) |
| Le contrat de la commande protocolaire n'est garanti ni par Home Assistant ni par l'appareil : **il peut changer sans préavis** | Le domaine **ne présume jamais** l'acceptation d'un réglage : il **confirme** ([`03`](03_profils_metier.md) §6) et **qualifie l'issue** ([`07`](07_moteur_de_mission.md) §4) |
| La **structure de la charge utile est déterminante** — la forme **enveloppée** est celle validée sur le terrain ; une forme **nue** est documentée comme **échouant en silence** | La forme enveloppée est **la seule admise** ([`07`](07_moteur_de_mission.md) §3) |

---

## Renvois

- Voie technique retenue et séquence : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Intention de mission : [`05_intention_de_mission.md`](05_intention_de_mission.md)
- Refus `PASSAGES_HORS_CONTRAT` : [`09_refus_et_diagnostics.md`](09_refus_et_diagnostics.md)
- Index du domaine : [`README.md`](README.md)
