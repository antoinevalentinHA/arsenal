# CONTRAT ARSENAL — ARROSAGE
## 02 — Régimes opérateur

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir les régimes opérateur du domaine `arrosage`, leur sens, le
décideur actif et le rôle du Rain Bird dans chacun.

---

## 1. Principe

Un **régime** est un contexte global, choisi par l'opérateur (ou projeté par un
contexte comme les vacances), qui détermine **qui décide de l'arrosage** et
**quel rôle joue le Rain Bird**. Le régime est une **entrée** de la couche
intention ([`05_intention.md`](05_intention.md)), jamais une couche de perception.

> **Invariant cardinal.** Aucun régime « normal » ne laisse le jardin sans
> aucune autorité d'arrosage. Le seul régime qui supprime toute autorité est
> « **Arrêt total** », explicitement marqué comme dangereux en absence.

> **Deux modes matériels Rain Bird** sous-tendent ces régimes :
> - **`Auto`** — programme interne minimal **actif** : c'est le mode **légitime
>   et par défaut** des régimes de coexistence et de secours (R1, R2, R4), celui
>   qui permet au filet de survie d'opérer ;
> - **`Off`** — programme interne **neutralisé** : réservé au **seul** régime
>   Arsenal exclusif (R3), **jamais** un défaut.

---

## 2. Les cinq régimes

| Régime | Décideur principal | Rôle Rain Bird | Sûr en absence ? |
|---|---|---|:--:|
| **R1 — Arsenal prioritaire** | Arsenal (HA) | Secours dormant, fenêtres disjointes | ✅ |
| **R2 — Vacances / Secours Rain Bird** | Rain Bird (programme minimal gouverné) | En `Auto` — autorité de secours **assumée** et active | ✅ |
| **R3 — Arsenal exclusif** | Arsenal (HA) seul | **Neutralisé** (`mode Off`) — explicite et borné | ⚠️ conditionnel |
| **R4 — Arsenal suspendu** | Personne **temporairement** côté Arsenal | Secours autonome **toujours actif** | ✅ |
| **R5 — Arrêt total** | Personne | **Tout coupé** | ❌ **dangereux** |

---

## 3. Définition normative de chaque régime

### R1 — Arsenal prioritaire (régime nominal)

Arsenal décide de l'arrosage selon le besoin hydrique optimisé. Le Rain Bird
**conserve son programme interne minimal** mais ses créneaux de secours sont
**disjoints** des fenêtres Arsenal et **dormants** tant qu'Arsenal renouvelle le
dead-man switch (`rain_delay`, voir
[`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)).

- Décideur : **Arsenal**.
- Rain Bird : présent, dormant, prêt à reprendre.
- C'est le régime **par défaut souhaité**.

### R2 — Vacances / Secours Rain Bird

Régime d'absence prolongée. Arsenal **délègue volontairement** l'arrosage au
programme minimal du Rain Bird, qui devient l'**autorité de secours assumée**.
Arsenal peut continuer à observer et à compléter, mais **n'est plus le garant
unique**.

- Décideur : **Rain Bird** (programme minimal gouverné).
- Rain Bird : en `Auto`, autorité de secours **active** (programme minimal).
- Se projette typiquement depuis le contexte d'absence
  ([`vacances.md`](../vacances.md)).

> Ce régime matérialise la doctrine : *« Rain Bird sauve le jardin si Arsenal
> disparaît »* — ici, Arsenal ne disparaît pas mais **se met volontairement en
> retrait** au profit du secours.

### R3 — Arsenal exclusif (`mode Off` Rain Bird)

Arsenal est **seul maître** ; la programmation interne du Rain Bird est
**neutralisée** (`mode Off`). C'est un régime **explicite, choisi, borné** —
**jamais** une doctrine par défaut.

- Décideur : **Arsenal seul**.
- Rain Bird : **neutralisé** — plus aucun filet autonome.
- ⚠️ **Conditionnellement sûr** : tant qu'Arsenal est vivant, le jardin est
  servi ; **si Arsenal tombe dans ce régime, le secours est absent**. À réserver
  à des situations surveillées (présence, intervention, test).

> **Interdit doctrinal.** `mode Off` ne doit **jamais** être l'état par défaut
> ni un effet de bord silencieux d'une automation. Sa pose est un acte explicite
> et son maintien doit être surveillé.

### R4 — Arsenal suspendu

Arsenal **cesse temporairement de décider** (maintenance, doute, capteurs
indisponibles, intervention manuelle), **sans neutraliser le Rain Bird**. Le
filet de survie autonome **reste actif**.

- Décideur côté Arsenal : **en pause**.
- Rain Bird : **secours autonome toujours actif**.

> **Invariant — « suspendu » ≠ « plus aucun arrosage ».** « Arsenal suspendu »
> signifie *Arsenal ne pilote plus*, **pas** *le jardin n'est plus arrosé*. Le
> Rain Bird continue de protéger le jardin. C'est précisément ce qui distingue
> R4 de R5.

### R5 — Arrêt total

**Toute** autorité d'arrosage est coupée : Arsenal **et** secours Rain Bird.
Régime **distinct, explicite et dangereux**.

- Décideur : **personne**.
- Rain Bird : **coupé**.
- ❌ **Dangereux en absence** : aucun arrosage de secours. À réserver à un
  besoin matériel impératif (coupure d'eau, gel, travaux), en **présence** et
  pour une **durée surveillée**.

> **Garde normative.** R5 doit être **impossible à atteindre par inadvertance** :
> il exige un acte opérateur explicite, doit être **signalé** de façon visible, et
> sa persistance en contexte d'absence
> ([`vacances.md`](../vacances.md)) doit être traitée comme une **anomalie**
> (alerte), pas comme un état nominal.

---

## 4. Matrice de sécurité (synthèse)

| Si Arsenal disparaît pendant… | Conséquence jardin |
|---|---|
| R1 — Arsenal prioritaire | Secours Rain Bird reprend (dead-man switch) → **protégé** |
| R2 — Vacances / secours | Rain Bird déjà aux commandes → **protégé** |
| R3 — Arsenal exclusif | **Aucun secours** → **à risque** (régime surveillé uniquement) |
| R4 — Arsenal suspendu | Secours Rain Bird actif → **protégé** |
| R5 — Arrêt total | Rien → **jardin en danger** |

> La reprise automatique du secours en R1/R4 est le cœur du contrat de
> coexistence : elle repose sur la **non-reconduction du dead-man switch**
> (voir [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)).

---

## 5. Invariants des régimes

1. Le **régime est une entrée** de l'intention, jamais une perception ni une
   preuve.
2. **R4 ≠ R5** : « Arsenal suspendu » conserve le secours Rain Bird ; « Arrêt
   total » le supprime.
3. **R3 et R5 sont les seuls régimes potentiellement non sûrs en absence** ; ils
   exigent un acte explicite, sont bornés et signalés.
4. `mode Off` (R3) n'est **jamais** un défaut ni un effet de bord.
5. Le régime par défaut **souhaité** est **R1 — Arsenal prioritaire**.
6. La transition vers un régime non sûr (R3/R5) **pendant un contexte d'absence**
   est une **anomalie** à signaler.

---

## Renvois

- Coexistence et dead-man switch : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Intention (consomme le régime) : [`05_intention.md`](05_intention.md)
- Régime d'absence (projection) : [`vacances.md`](../vacances.md)
- Index du domaine : [`README.md`](README.md)
