# CONTRAT ARSENAL — ARROSAGE
## 05 — Intention d'arrosage

**Version contrat :** v0.1
**Statut :** Normatif — antérieur au runtime
**Objet :** Définir l'**intention d'arrosage** comme couche de **décision sous
régime**, strictement distincte du besoin et de l'exécution.

---

## 1. Trois objets strictement distincts

| Objet | Question | Couche | Contrat |
|---|---|---|---|
| **Besoin** | *La zone mérite-t-elle de l'eau ?* | Perception | [`04_besoin_hydrique.md`](04_besoin_hydrique.md) |
| **Intention** | ***Arsenal doit-il agir maintenant ?*** | **Décision** | ce document |
| **Exécution** | *Commande Rain Bird / ESP32* | Action (runtime futur) | hors lot |

> **Invariant de non-confusion.** Un besoin n'est **pas** une intention : une
> zone peut mériter de l'eau (besoin élevé) sans qu'Arsenal doive agir
> maintenant (hors fenêtre, proximité d'un créneau de secours, pont dégradé,
> restriction active). De même, une intention n'est **pas** une exécution : elle
> exprime ce qu'Arsenal **veut faire**, l'exécution étant l'acte matériel
> ultérieur, gouverné et observé.

Cette séparation reprend la doctrine besoin → admissibilité → décision de la
climatisation
([`climatisation/05_decision_candidats.md`](../climatisation/05_decision_candidats.md),
[`climatisation/06_doctrine_blocages.md`](../climatisation/06_doctrine_blocages.md)).

---

## 2. Entrées de l'intention

L'intention (`‹intention_arrosage_zone›`, conceptuel) est produite **par zone**,
à partir de :

| Entrée | Rôle dans la décision |
|---|---|
| **Régime opérateur** ([`02_regimes.md`](02_regimes.md)) | Détermine si Arsenal a **le droit** de décider (R1/R3 oui ; R2 délégué au secours ; R4/R5 non). |
| **Besoin hydrique** ([`04_besoin_hydrique.md`](04_besoin_hydrique.md)) | Condition nécessaire : pas de besoin → pas d'intention d'arroser. |
| **Fenêtres horaires** | Arsenal n'agit que dans `‹fenetre_arsenal›` (disjointe du secours). |
| **Proximité du secours Rain Bird** | Cooldown avant/après les créneaux de secours → abstention ([`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)). |
| **Restrictions** | Une restriction active **annule** l'intention exécutable. |
| **Santé du pont** | Pont dégradé → abstention, laisser le secours opérer (jamais forcer une commande incertaine). |
| **Cycle récent** | Un arrosage récent (confirmé **ou présumé**) **inhibe** une nouvelle intention immédiate (anti-acharnement). |
| **Inconnues critiques** | Besoin inconnu, mapping zone non confirmé, observation ambiguë → **prudence** explicite. |

---

## 3. Règle de décision (qualitative, non figée)

> L'intention d'arroser une zone **n'est active que si TOUTES** les conditions
> suivantes sont réunies :

1. le **régime** autorise Arsenal à décider (R1 ou R3) ;
2. le **besoin** de la zone est suffisant ;
3. l'instant est **dans une fenêtre Arsenal**, hors cooldown de secours ;
4. **aucune restriction** active ;
5. le **pont est sain** assez pour exécuter et observer ;
6. **pas de cycle récent** sur la zone (anti-acharnement) ;
7. **aucune inconnue critique** non gérée.

Si l'une manque, l'intention est **inactive** — et la cause doit rester
**explicable** (motif dominant, sur le modèle de
[`aeration_recommandation.md`](../aeration_recommandation.md)).

---

## 4. Abstention vs blocage — direction de défaillance

L'**abstention** d'Arsenal (intention inactive) ne signifie **jamais** que le
jardin n'est pas arrosé : elle **rend la main au secours** Rain Bird selon le
régime et le calendrier.

> **Invariant.** L'intention Arsenal ne doit **jamais** se transformer en une
> garde qui coupe **aussi** le secours. Quand Arsenal s'abstient, le filet de
> survie reste disponible (sauf régimes R3/R5 explicitement non sûrs). Cf.
> direction de défaillance de
> [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md) §5.

---

## 5. Ce que l'intention NE fait PAS

- ❌ elle **ne lit pas** les capteurs bruts pour refaire le besoin (elle
  **consomme** le besoin de [`04_besoin_hydrique.md`](04_besoin_hydrique.md)) ;
- ❌ elle **n'exécute pas** : aucune commande Rain Bird/ESP32 n'est émise par
  cette couche (exécution = runtime futur, hors lot) ;
- ❌ elle **ne neutralise pas** le secours Rain Bird ;
- ❌ elle **ne présente pas** un arrosage présumé comme confirmé
  ([`06_observation_et_preuves.md`](06_observation_et_preuves.md)).

---

## 6. Invariants de l'intention

1. **Besoin ≠ intention ≠ exécution** : trois objets distincts, jamais
   confondus.
2. L'intention est **par zone** et **conditionnée au régime**.
3. L'intention active exige **toutes** les conditions de §3 ; toute abstention
   est **explicable** (motif dominant).
4. L'abstention **rend la main au secours**, elle ne coupe jamais le jardin.
5. Un **cycle récent** (confirmé ou présumé) **inhibe** une nouvelle intention
   (anti-acharnement).
6. Une **inconnue critique** non gérée conduit à l'**abstention prudente**, pas à
   une exécution optimiste.
7. **Aucun seuil, durée, ID ou `entity_id` n'est figé** : tout est conceptuel
   jusqu'à la Phase 0.

---

## Renvois

- Besoin hydrique : [`04_besoin_hydrique.md`](04_besoin_hydrique.md)
- Régimes : [`02_regimes.md`](02_regimes.md)
- Coexistence / cooldown / direction de défaillance : [`03_coexistence_rainbird.md`](03_coexistence_rainbird.md)
- Observation & preuves : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Décision/admissibilité (modèle climatisation) : [`climatisation/05_decision_candidats.md`](../climatisation/05_decision_candidats.md)
- Motif dominant (modèle aération) : [`aeration_recommandation.md`](../aeration_recommandation.md)
- Index du domaine : [`README.md`](README.md)
