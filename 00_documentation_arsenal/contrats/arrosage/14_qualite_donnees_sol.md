# CONTRAT ARSENAL — ARROSAGE
## 14 — Qualité des données sol (socle transverse v0)

**Version contrat :** v0.1
**Statut :** **Normatif — socle transverse de qualité/confiance** des trois points
d'humidité sol. Définit **le mécanisme** (états, agrégation, dégradation de
confiance), **pas les valeurs finales** (durées de fraîcheur, seuils). Aucune
entité runtime n'est créée par ce lot.

> **Garde-fou de lecture.** Ce contrat **ne fixe aucune durée de fraîcheur
> chiffrée**, **aucun seuil chiffré définitif**, **n'exclut aucun capteur
> automatiquement**, **ne calibre rien**. Il **borne la confiance**, en deçà de
> toute recommandation ([`13`](13_observation_hydrique_jardin.md)).

---

## Objet

Poser le **socle de qualité des données** consommé par toute la couche
d'observation hydrique : qualifier **chaque point** (frais / stale / indisponible /
suspect) et la **qualité agrégée** du canal sol (complète / dégradée / insuffisante
/ incohérente / vérification humaine). C'est la **fondation diagnostic** du
chapeau [`13`](13_observation_hydrique_jardin.md) : sans confiance qualifiée,
aucune observation n'est exploitable, et **a fortiori** aucune recommandation
future.

---

## 1. Sources concernées

**Humidité sol (les trois points de mesure d'une zone unique) :**
- `sensor.jardin_humidite_sol_zone_1_soil_moisture`
- `sensor.jardin_humidite_sol_zone_2_soil_moisture`
- `sensor.jardin_humidite_sol_zone_3_soil_moisture`

**Températures sol associées** (`sensor.jardin_humidite_sol_zone_{1,2,3}_temperature`)
— utiles comme **observation secondaire** uniquement, **jamais comme déclencheurs**
([`12`](12_capteurs_humidite_sol.md), [`13`](13_observation_hydrique_jardin.md) §3).

> Rappel : « Zone 1/2/3 » = **points de mesure**, pas zones d'arrosage. Les
> `entity_id` Zone 2/3 restent à confirmer au relevé formel
> ([`12`](12_capteurs_humidite_sol.md) §4).

---

## 2. États par point

Chaque point reçoit **un état de qualité** :

| État | Sens |
|---|---|
| **frais** | mesure récente et exploitable |
| **stale** | mesure **ancienne** : exploitable avec **confiance dégradée**, **jamais** traitée comme fraîche |
| **indisponible** | `unknown` / `unavailable` / absente : aucune valeur utile |
| **suspect** | mesure présente mais **douteuse** (§5) : confiance dégradée, **exclue des agrégats seulement si un critère robuste futur** le justifie |

> **Mécanisme, pas valeur.** La **frontière frais / stale** est définie par un
> **âge de mesure** (fraîcheur exposée par la sonde, [`12`](12_capteurs_humidite_sol.md) §5) ;
> **la durée chiffrée n'est PAS figée** dans ce contrat tant qu'elle n'est pas
> validée par observation ([`plan_observation_hydrique_v0`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)).

---

## 3. Qualité agrégée (canal sol)

| Qualité agrégée | Sens |
|---|---|
| **complète** | trois points frais et cohérents |
| **dégradée** | un point manquant/stale/suspect ; agrégats encore exploitables avec réserve |
| **insuffisante** | trop peu de points frais pour une lecture fiable du canal sol |
| **incohérente** | points frais mais en **contradiction forte** (hétérogénéité anormale) |
| **vérification humaine recommandée** | drapeau de diagnostic (§7) : la lecture humaine est **souhaitable** |

> L'agrégation **doit rendre visible le nombre de points frais utilisés** (§4).

---

## 4. Invariants

1. **Pas de fallback silencieux** vers `unknown` comme **valeur utile** : une
   donnée absente est **indisponible**, jamais une valeur exploitable par défaut.
2. Une donnée **stale reste une donnée ancienne**, **pas** une valeur fraîche.
3. Une donnée **suspecte n'est pas exclue automatiquement** sans **critère
   robuste** (§5).
4. **Un seul capteur stale dégrade la confiance** (qualité ≥ **dégradée**).
5. **Deux capteurs stale** rendent le canal sol **insuffisant ou très dégradé**.
6. **Trois capteurs stale** rendent le canal sol **indisponible pour décision**.
7. L'agrégation **rend visible le nombre de points frais** réellement utilisés.
8. Aucune de ces qualifications **n'émet de recommandation** ni **ne déclenche
   d'action** (frontière v0, [`13`](13_observation_hydrique_jardin.md) §2/§4).

---

## 5. Capteur suspect (concept documentaire)

Un point est **candidat « suspect »** si l'on observe (concepts, **sans seuil
chiffré définitif**) :

- une **valeur physiquement impossible** ;
- une **variation très brutale** non expliquée par pluie ou arrosage ;
- un **capteur figé** (valeur immobile anormalement longtemps) ;
- une **contradiction forte** avec les autres points ;
- une **divergence persistante** (à observer dans la durée).

> **Suspect ≠ exclu.** « Suspect » qualifie une **confiance dégradée / donnée à
> surveiller**, **pas** une exclusion automatique. L'exclusion d'un point d'un
> agrégat **n'est admissible** qu'au travers d'un **critère robuste futur**,
> validé par observation — **non défini ici**.

---

## 6. Point 2 — observation à suivre (sans correction)

Au test tuyau ([`12`](12_capteurs_humidite_sol.md) §12), les amplitudes de réponse
ont divergé :

| Point | Écart humidité observé |
|---|---|
| Point 1 | **+36,80** |
| Point 2 | **+21,43** |
| Point 3 | **+37,60** |

Le **Point 2** a montré une **amplitude plus faible**. Conclusion **prudente** :

- **observation à suivre** ;
- **ne pas calibrer maintenant** ;
- **ne pas corriger maintenant** ;
- **ne pas déclasser maintenant** (ce n'est pas un « suspect » en l'état) ;
- **possibles bandes par capteur** à **étudier plus tard** (peut refléter un
  placement / une zone différente plutôt qu'un défaut).

---

## 7. Vérification humaine (diagnostic, pas action)

La **vérification humaine** est un **drapeau de diagnostic** : il **indique que la
lecture humaine est souhaitable** (données insuffisantes, incohérence, doute).

En **v0**, explicitement :
- ce **n'est pas** une action automatique ;
- ce **n'est pas** un prérequis bloquant ;
- ce **n'est pas** une recommandation d'arrosage ;
- c'est **seulement** un drapeau indiquant qu'une lecture humaine est souhaitable.

---

## Renvois

- Chapeau observation hydrique (frontière v0) : [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md)
- Canal réservoir sol (consommateur des points frais) : [`15_canal_reservoir_sol.md`](15_canal_reservoir_sol.md)
- Capteurs humidité sol (sources, fraîcheur, Point 2) : [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md)
- Observation & preuves (honnêteté d'état) : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Plan d'observation v0 (fenêtres de fraîcheur à confirmer) : [`plan_observation_hydrique_v0.md`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)
- Confrontation des avis (qualité/confiance) : [`confrontation_avis_besoin_hydrique.md`](../../audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md)
- Index du domaine : [`README.md`](README.md)
