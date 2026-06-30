# Cadrage — Arrosage : modulation bornée de durée par critères physiques

| Champ | Valeur |
|---|---|
| **Type** | Cadrage / arbitrage de chantier (conception préalable, **sans implémentation**) |
| **Domaine** | Arrosage — durée d'arrosage (combien de temps), modulation par critères physiques |
| **Statut** | **Ouvert en cible doctrinale — NON lançable en runtime à ce stade.** Aucun lot runtime actionnable. Aucune décision finale, aucun seuil, aucun automatisme. |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-06-30 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `f011851` |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun helper, aucune automation, aucun ID d'automation, aucun changement d'entité, aucune modification UI, aucun branchement Rain Bird. Ne fixe aucune règle opposable. |
| **Registre** | Chantier **C11** (proposé) — ② Parqués, cf. [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) |

> **Objet.** Acter que la **modulation de la durée d'arrosage par critères
> physiques** est une **cible doctrinalement légitime mais prématurée en runtime
> actionnable**, formaliser ses **prérequis**, distinguer nettement **« quand
> arroser »** de **« combien de temps arroser »**, poser les **garde-fous
> architecturaux**, et proposer un **séquencement** compatible avec la doctrine
> existante. Ce document **prépare** un futur contrat ; il **n'en tient pas lieu**.

> **Garde-fou de lecture.** Ce document **ne décide rien d'opposable**, **ne crée
> aucun runtime**, **ne fixe aucun seuil**, **ne transforme aucune grandeur
> physique en dose**. La doctrine du domaine prime
> ([`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md)) ; en cas
> de divergence, **les contrats font foi**.

---

## 1. État actuel (constat, sourcé)

| Élément | État réel | Source faisant foi |
|---|---|---|
| **Décision V1 automatique** | **Livrée** (besoin sol → intention → exécution déléguée au Run supervisé), publiée v16.3. **Validation terrain encore incomplète** (arrosage effectif, comportement sur la durée à constater). | [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) · [`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md) §8 |
| **Durée d'arrosage** | **Paramétrable mais fixe** : une valeur opérateur unique (helper borné `[1,60]`), appliquée telle quelle à chaque cycle. **Aucune modulation**. | [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md) · [`17`](../../../contrats/arrosage/17_decision_v1.md) §5 |
| **Canal réservoir sol (lent)** | **Livré** (médiane / point sec / hétérogénéité / qualité). **Capteurs encore à observer/calibrer en sol réel** ; seuils d'humidité **exploratoires**, non contractuels. | [`15_canal_reservoir_sol.md`](../../../contrats/arrosage/15_canal_reservoir_sol.md) · [`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §9 |
| **Canal demande climatique (rapide) — ET₀ / VPD** | **Spécifié, runtime NON livré.** Manque notamment le câblage Tmin/Tmax journaliers fiables. | [`16_canal_demande_climatique.md`](../../../contrats/arrosage/16_canal_demande_climatique.md) |
| **Plan d'observation hydrique v0** | **Encore nécessaire** : courbes de tarissement par régime météo non collectées. | [`plan_observation_hydrique_v0.md`](plan_observation_hydrique_v0.md) |

> **Conséquence.** Le socle d'entrée d'une modulation de durée — un signal sol
> **fiable** et un canal climatique **livré** — n'est **pas encore réuni**. On ne
> peut pas moduler par un signal auquel on n'accorde pas encore confiance.

---

## 2. Distinction structurante — « quand arroser » ≠ « combien de temps arroser »

C'est le pivot de ce cadrage, et la correction qui le motive.

| | **Quand arroser** | **Combien de temps arroser** |
|---|---|---|
| Objet | seuils de **décision** (humidité de déclenchement, hystérésis, fenêtre, cooldown) | **durée** d'un cycle d'arrosage |
| Doctrine | **Lot 4 — calibration** : ET₀/VPD/tendance/tarissement ajustent les *helpers de décision* | **non spécifié** — relève d'un **chantier distinct** (ce document) |
| Statut runtime | décision V1 livrée | durée **paramétrable mais fixe** |
| Source | [`17`](../../../contrats/arrosage/17_decision_v1.md) §6 | — |

> **Le Lot 4 existant ne couvre PAS ce chantier.** Le Lot 4 calibre la **décision**
> (quand). La **modulation de durée** (combien de temps) est un sujet **séparé,
> encore non spécifié**, que la doctrine range aujourd'hui parmi les éléments
> **explicitement différés** : *« modulation climatique sophistiquée »* et
> *« évolutions agronomiques »* ([`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md) §9),
> *« légitimes plus tard, non bloquantes pour la première release »*.

---

## 3. Arbitrage

**Décision de ce cadrage** (propriétaire, documentaire) :

1. **Ouvrir le chantier en cible doctrinale.** La modulation bornée de durée par
   critères physiques est **reconnue légitime** : elle sert la finalité
   d'**optimisation de l'eau** sans compromettre la protection du jardin
   ([`01_metier.md`](../../../contrats/arrosage/01_metier.md)).
2. **Ne PAS ouvrir de lot runtime actionnable maintenant.** Aucun helper, aucune
   automation, aucune entité, aucune UI. Le chantier est **parqué** derrière ses
   prérequis (§5).
3. **Priorité : fermer la validation terrain de C10.** Confirmer que la V1 arrose
   réellement, correctement, sur plusieurs cycles, **avant** d'empiler de la
   sophistication sur une base non vérifiée
   ([`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md) §8).
4. **Puis : livrer le runtime du canal demande climatique** (ET₀/VPD), déjà
   spécifié et autonome ([`16`](../../../contrats/arrosage/16_canal_demande_climatique.md)).
5. **Puis seulement : rédiger un contrat dédié « modulation de durée »** — le
   contrat « besoin / dose » que [`15`](../../../contrats/arrosage/15_canal_reservoir_sol.md) §8
   et [`16`](../../../contrats/arrosage/16_canal_demande_climatique.md) §1 renvoient
   au futur. Aucun runtime avant ce contrat.

> **Pourquoi parquer plutôt que lancer.** Deux prérequis manquent (§5) ; les
> ouvrir dans le désordre violerait la règle « observation avant action »
> ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §1.4) et
> risquerait une modulation **cosmétique** (pilotée par un signal non fiable)
> plutôt que **fondée**.

---

## 4. Doctrine cible (principes du futur contrat, non opposables ici)

Esquisse des invariants que le futur contrat devra porter. **Aucun n'est
opposable tant que le contrat n'est pas écrit.**

1. **Durée de base opérateur.** Le point de référence reste une durée réglée par
   l'opérateur (helper borné existant) ; la modulation **part de** cette base, ne
   la remplace pas.
2. **Modulation bornée.** Un facteur multiplicatif **strictement encadré** (bornes
   basse et haute à fixer au contrat), jamais une durée calculée librement.
3. **Modulation désactivable.** Un interrupteur permet de revenir au comportement
   actuel ; la modulation est une **surcouche optionnelle**.
4. **Retour garanti à durée fixe.** En cas de désactivation, d'indisponibilité ou
   de doute, le système **retombe** sur la durée de base, de façon déterministe.
5. **Observation à blanc avant branchement.** Le facteur est d'abord **exposé en
   diagnostic** (calculé, non appliqué) et observé, sur le modèle « recommandation
   non actionnable » ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §6),
   **avant** toute influence sur la durée réelle.
6. **Données dégradées ⇒ jamais de réduction automatique.** Garde anti-faux-négatif
   ([`04_besoin_hydrique.md`](../../../contrats/arrosage/04_besoin_hydrique.md) §4) :
   une entrée muette ou dégradée **ne raccourcit jamais** l'arrosage par défaut —
   au pire elle laisse la durée de base inchangée.
7. **Priorité au réservoir sol.** Le **déficit du réservoir sol** (signal lent,
   déjà livré) est le **modulateur primaire** ; il prime en cas de tension.
8. **Demande climatique comme modulateur secondaire.** ET₀/VPD **affinent** le
   facteur, ils ne le **fondent** pas seuls ; canaux **jamais fusionnés** en un
   score unique ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §1.6,
   [`16`](../../../contrats/arrosage/16_canal_demande_climatique.md) §5).
9. **Explicabilité obligatoire.** Toute modulation appliquée doit être **lisible**
   (pourquoi la durée est plus longue / plus courte), sur le modèle du `motif` de
   l'intention.

---

## 5. Prérequis (conditions de lançabilité du runtime)

Le chantier ne devient **lançable en runtime** qu'une fois **tous** réunis :

- **P1 — Validation terrain de C10.** Arrosage effectif confirmé et comportement
  sur la durée observé sur plusieurs cycles
  ([`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md) §8).
- **P2 — Capteurs sol fiabilisés.** Observation suffisante du réservoir sol pour
  faire confiance au signal de déficit, avec **courbes de tarissement** collectées
  ([`plan_observation_hydrique_v0.md`](plan_observation_hydrique_v0.md)).
- **P3 — Runtime du canal demande climatique livré.** ET₀/VPD produits et
  qualifiés, Tmin/Tmax câblés ([`16`](../../../contrats/arrosage/16_canal_demande_climatique.md)).
- **P4 — Contrat dédié « modulation de durée » rédigé et figé.** Bornes, signaux,
  priorité réservoir sol > climat, désactivabilité, dégradation, explicabilité
  — **contrat avant runtime**, sans exception.

> Tant que **P1–P4** ne sont pas réunis, ce chantier reste **parqué** : cadrage
> ouvert, runtime fermé.

---

## 6. Exclusions (hors périmètre, opposables au futur chantier)

- ❌ **Calcul agronomique de dose** (ETc, coefficient cultural Kc, bilan hydrique
  fermé) — exclu.
- ❌ **ET₀ → millimètres → minutes** : aucune transformation d'une grandeur
  physique en quantité d'eau puis en durée. *« ET₀ ≠ dose ; elle décrit un climat,
  elle ne commande rien »* ([`16`](../../../contrats/arrosage/16_canal_demande_climatique.md)
  garde-fou de lecture, §4, §8).
- ❌ **Logique physique ouverte** : pas de modèle libre non borné ; uniquement un
  **facteur encadré** autour d'une durée de base.
- ❌ **Multi-zone** (y compris déguisé) : une zone Rain Bird, trois points de
  mesure ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) §1).
- ❌ **Action directe sans phase d'observation** : pas de branchement sur la durée
  réelle avant l'observation à blanc (§4.5).
- ❌ **Complexification de la V1 avant sa validation terrain** : aucun ajout tant
  que C10 n'est pas confirmé sur le terrain.
- ❌ **Branchement Rain Bird, UI, helper, automation, script, template, ID
  d'automation** dans ce document.

---

## 7. Séquencement proposé (compatible doctrine)

```
C10 (validation terrain V1)        ── P1 ──┐
                                            ├─► Contrat « modulation de durée »  ──►  Runtime borné,
Canal demande climatique (ET₀/VPD) ── P3 ──┤        (P4, contrat avant runtime)        désactivable,
Observation sol / tarissement      ── P2 ──┘                                            observé à blanc
                                                                                        puis branché
```

1. **Fermer C10** (terrain) — priorité, déjà au plan d'action.
2. **Livrer le canal demande climatique** — lot net, autonome, déjà spécifié.
3. **Laisser tourner l'observation v0** — courbes de tarissement.
4. **Rédiger le contrat « modulation de durée »** — figer bornes et garde-fous (§4).
5. **Implémenter le facteur borné** — exposé d'abord **en diagnostic** (à blanc),
   branché **ensuite**, désactivable, avec retour garanti à durée fixe.

> Chaque étape reste **auditée avant tout YAML** (contrats avant runtime) et, le
> moment venu, **publiée dans le changelog de sa release** (co-commit), sans
> changelog dédié anticipé.

---

## 8. Renvois

- Décision V1 / calibration Lot 4 (« quand ») : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Mode manuel supervisé / durée bornée : [`11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md)
- Besoin hydrique / garde anti-faux-négatif : [`04_besoin_hydrique.md`](../../../contrats/arrosage/04_besoin_hydrique.md)
- Chapeau observation hydrique / canaux / frontière : [`13_observation_hydrique_jardin.md`](../../../contrats/arrosage/13_observation_hydrique_jardin.md)
- Canal réservoir sol (modulateur primaire) : [`15_canal_reservoir_sol.md`](../../../contrats/arrosage/15_canal_reservoir_sol.md)
- Canal demande climatique ET₀/VPD (modulateur secondaire) : [`16_canal_demande_climatique.md`](../../../contrats/arrosage/16_canal_demande_climatique.md)
- Finalité métier (protéger le jardin, optimiser l'eau) : [`01_metier.md`](../../../contrats/arrosage/01_metier.md)
- Plan d'action vivant arrosage (§8 terrain, §9 différés) : [`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md)
- Plan d'observation hydrique v0 (tarissement) : [`plan_observation_hydrique_v0.md`](plan_observation_hydrique_v0.md)
- Cockpit d'état (chantier C11) : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)

---

*Cadrage de chantier — non normatif, sans implémentation. Acte une cible
doctrinale parquée derrière prérequis ; ne fixe aucune règle opposable. Le futur
contrat « modulation de durée » fera foi une fois rédigé.*
