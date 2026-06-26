# Confrontation des avis externes — Besoin hydrique jardin

| Champ | Valeur |
|---|---|
| **Type** | Confrontation d'avis externes (conception, **sans implémentation**) |
| **Domaine** | Arrosage — besoin hydrique jardin, recommandation d'arrosage |
| **Statut** | **Ouvert — synthèse de consultation, à confronter avant contrat runtime.** Aucune décision finale, aucun runtime. |
| **Version** | 0.1 (confrontation) |
| **Date** | 2026-06-26 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `de4b6cb` |
| **Amont** | [`cadrage_besoin_hydrique_decision_arrosage.md`](cadrage_besoin_hydrique_decision_arrosage.md) (ouverture du chantier, PR #99) |
| **Cadre** | Aucun YAML, aucun runtime, aucun seuil opposable. Les seuils cités sont **exploratoires, non normatifs**. |

> **Objet.** Consolider les trois consultations externes (Gemini, Grok, Claude)
> menées avec **le même prompt** : dégager **consensus**, **divergences**,
> **risques**, **doctrine provisoire** et **questions à trancher** avant toute
> passe contractuelle. **Observation avant action.**

> **Garde-fou de lecture.** Ce document **ne décide aucune règle**, **ne fixe
> aucun seuil final**, **ne crée aucun automatisme**. Tous les seuils sont
> **exploratoires**. Une zone Rain Bird, **trois points de mesure**
> ([`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §2).

---

## 1. Contexte

Le chantier « besoin hydrique jardin / recommandation d'arrosage » a été ouvert
(cadrage amont, PR #99). Trois IA (Gemini, Grok, Claude) ont été consultées pour
proposer une **logique agronomique et décisionnelle** — **pas** du code. Ce
document **confronte** leurs réponses pour préparer la future doctrine Arsenal.

Rappels structurants invariants :
- **une seule zone d'arrosage Rain Bird** ; les capteurs « Zone 1/2/3 » sont
  **trois points de mesure** dans cette zone unique, **pas** trois zones ;
- **les capteurs informent, ne déclenchent pas** l'arrosage ;
- observation honnête (ACK ≠ preuve, [`06`](../../../contrats/arrosage/06_observation_et_preuves.md)) ;
- exécution **manuelle supervisée** seule validée à ce jour
  ([`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md)).

---

## 2. Méthode

- **Entrée commune** : le dossier de consultation du cadrage (contexte jardin,
  contraintes Rain Bird, capteurs, observations terrain, paramètres météo).
- **Format de réponse imposé** identique aux trois IA (paramètres
  indispensables/secondaires, grandeur représentative, rôle pluie, logique de
  décision, seuils indicatifs non définitifs, gestion stale/désaccords, prudence
  chaleur, risques, confiance).
- **Interdiction** faite aux IA de produire du YAML / une implémentation HA.
- Cette confrontation **n'arbitre pas** : elle **range** les avis pour décision
  ultérieure de l'opérateur.

---

## 3. Synthèse par IA

### 3.1 Gemini
**Points forts :**
- approche **multifactorielle** sol + météo ;
- distingue **besoin de fond** / **sauvegarde canicule** ;
- recommande **médiane + minimum** ;
- **pluie récente = bloquant / modérateur** ; **pluie prévue = différateur** ;
- **température max prévue** et **jours chauds consécutifs** importants ;
- **saison indispensable** ; **tendance humidité 24 h** utile ;
- propose des **classes de besoin hydrique** ; signale **données insuffisantes**.

**À encadrer :**
- exclusion automatique **trop rapide** d'un capteur jugé aberrant ;
- usage de **2 capteurs** sans assez dégrader la confiance ;
- idée d'**arrosage de rafraîchissement** à cadrer **fortement** ;
- température parfois présentée comme **déclencheur principal** → reformuler en
  **facteur d'amplification / demande climatique**.

### 3.2 Grok
**Points forts :**
- converge sur **médiane / représentatif + minimum** ; insiste sur
  **minimum + tendance** ;
- insiste sur la **fraîcheur** des données ;
- **pluie récente effective** (pas seulement brute) ; **pluie prévue** = différer
  selon **probabilité / cumul / horizon** ;
- **hétérogénéité forte → vérification humaine** ;
- **observation visuelle** des plantes sensibles ;
- **seuils très incertains** ; **ne pas automatiser trop vite** ; raisonnement
  prudent météo/saison.

**À encadrer :**
- « exclusion d'un capteur aberrant » → remplacer par **« donnée suspecte /
  confiance dégradée »** ;
- minimum bas + tendance baisse pertinent, **mais** un minimum bas **en canicule**
  peut **déjà** justifier une alerte même si la tendance est stable ;
- ne pas transformer l'**observation visuelle** en **prérequis bloquant
  systématique**.

### 3.3 Claude
**Apport décisif :**
- **ne pas fusionner** tout dans un score unique ;
- l'humidité sol est un indicateur **lent, en retard, biaisé en profondeur** ;
- le **stress des plantes sensibles** est **précoce, de surface, piloté par
  l'évapotranspiration** ;
- **séparer deux canaux** : (1) **réservoir / sol / lent** ; (2) **demande /
  chaleur / rapide** ;
- ajouter des **modulateurs orthogonaux** : pluie récente effective, pluie prévue
  crédible, qualité des données, dernier arrosage, disponibilité Rain Bird ;
- la **prudence dépend du régime** : frais/humide → prudence = **ne pas arroser** ;
  canicule → prudence = **protéger les plantes sensibles**.

**Recommandations :**
- exposer **trois grandeurs sol** : représentative = **médiane**, point sec =
  **minimum**, hétérogénéité = **max − min** ;
- **pas d'indicateur global unique** destructeur d'information ;
- **un seul point sec ne suffit jamais** à déclarer la zone sèche ;
  **2 points secs / 3** = signal de sécheresse raisonnablement fort ;
- **pluie efficace** croisée avec la **réponse des capteurs sol** ;
- pluie prévue **diffère**, ne **bloque pas** aveuglément ; **en canicule**, ne
  pas différer sur une simple prévision incertaine ;
- température = **proxy de demande / ET**, **pas** indicateur d'eau ;
- aspersion : **timing** important (**tôt le matin**) ;
- capteurs stale/incohérents → **dégradation graduelle**, pas blocage binaire ;
- données insuffisantes → **vérification humaine** recommandée.

**À encadrer :**
- le **canal chaleur** ne doit pas devenir un **automatisme autonome** ;
- l'**« override sensible »** doit rester une **recommandation prudente**, pas une
  commande directe ;
- la **vérification humaine** = un **état de décision**, pas une obligation
  permanente ;
- **ne pas transformer les seuils exploratoires en contrats**.

---

## 4. Consensus / Divergences

### 4.1 Consensus (les trois convergent)

| # | Point de consensus |
|---|---|
| C1 | **Pas de moyenne simple seule** |
| C2 | **Médiane / représentatif + minimum** |
| C3 | **Exposer l'hétérogénéité** (max − min) |
| C4 | Prendre en compte la **fraîcheur** des données |
| C5 | Intégrer **pluie récente** |
| C6 | Intégrer **pluie prévue** |
| C7 | Intégrer **température extérieure, saison, canicule** |
| C8 | **Pas de décision sur humidité instantanée seule** |
| C9 | **Ne pas figer les seuils** maintenant |
| C10 | **Observer plusieurs semaines** |
| C11 | Données **stale / incohérentes → décision dégradée** |
| C12 | **Ne pas automatiser immédiatement** |

### 4.2 Divergences / nuances

| Sujet | Gemini | Grok | Claude |
|---|---|---|---|
| **Structure de la décision** | classes multifactorielles (score implicite) | facteurs prudents, pas de fusion explicite | **canaux séparés** (sol lent / demande rapide) + modulateurs — refus du score unique |
| **Température** | risque de **déclencheur principal** (à reformuler) | facteur de demande | **proxy d'ET, jamais indicateur d'eau** |
| **Capteur suspect** | **exclusion auto** (trop rapide) | « donnée suspecte / confiance dégradée » | **dégradation graduelle**, pas binaire |
| **Minimum bas vs tendance** | minimum comme garde | minimum **+ tendance baisse** | minimum bas **+ canicule** peut déjà alerter même tendance stable |
| **Vérification humaine** | implicite (données insuffisantes) | sur **hétérogénéité forte** + visuel | **état de décision**, non bloquant permanent |
| **Rafraîchissement / canicule** | **arrosage de rafraîchissement** (à cadrer fort) | prudence canicule | **protéger plantes sensibles**, sans automatisme autonome |
| **Observation visuelle** | — | proposée | utile, **pas un prérequis bloquant** |

---

## 5. Seuils exploratoires comparés — **NON NORMATIFS**

> ⚠️ **Aucun de ces seuils n'est retenu, validé, ni opposable.** Ils sont
> rapportés **uniquement** pour comparaison ; ils **ne fixent rien** et **ne
> doivent pas être transformés en contrat** (cf. capteurs non calibrés en sol
> réel, [`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §9).

### 5.1 Humidité sol (bandes)
| Bande | Gemini | Grok | Claude |
|---|---|---|---|
| Très basse | < 35 % | < 25–30 % | < ~30 % |
| Basse | < 42 % | 30–40 % | ~30–40 % |
| Correcte | 45–60 % | 40–60 % | ~40–55 % |
| Élevée | > 65 % | > 60–70 % | > ~55–60 % |

> Claude note que le **Point 2** (amplitude plus faible) pourrait justifier des
> **bandes par capteur** à terme.

### 5.2 Pluie / chaleur (indicatif)
| Paramètre | Gemini | Grok | Claude |
|---|---|---|---|
| Pluie récente significative | > 8 mm / 48 h | > 10–15 mm efficaces / 48 h | ~5–10 mm / 24–48 h (**réponse sol = juge**) |
| Pluie prévue (différante) | > 5 mm / 24 h, prob. > 60 % | > 10 mm probables < 36 h | ≥ ~5 mm proche, prob. élevée |
| Température élevée | > 30 °C | > 28–30 °C | Tmax ≥ ~30 °C |
| Forte chaleur / canicule | > 35 °C **ou** 3 j > 32 °C | plusieurs j > 32–35 °C **+ nuits > 20 °C** | ≥ ~32–34 °C ; canicule **seuils Météo-France Gironde, nuits incluses** |
| Jours sans pluie (été) | — | > 7–10 j | ≥ ~5–7 j |
| Jours chauds consécutifs | importants | — | ≥ 3 j |

---

## 6. Doctrine provisoire Arsenal (proposée, **non normative**)

> **Statut.** Formulation **provisoire** de travail. **Non opposable**, non promue
> en contrat. Sert de base à l'arbitrage et à la future passe contractuelle.

**Principe directeur** (apport Claude, soutenu par le consensus) : le **besoin
hydrique jardin n'est pas une valeur unique**. Il est **structuré en canaux
séparés** + modulateurs, **sans score fusionné** destructeur d'information.

**Canal 1 — réservoir sol (lent) :**
- humidité **représentative = médiane** des 3 points ;
- **point le plus sec = minimum** ;
- **hétérogénéité = max − min** ;
- **fraîcheur** ; **cohérence** ; **tendance / tarissement**.

**Canal 2 — demande climatique (rapide) :**
- saison ; température extérieure actuelle ; **température max prévue** ;
- **chaleur consécutive** ; **nuits chaudes** ; **canicule** ;
- humidex / proxy **ET** éventuel.

**Modulateurs (orthogonaux) :**
- **pluie récente effective** ; **pluie prévue crédible** ;
- **dernier arrosage** ; **disponibilité Rain Bird** ;
- **qualité des données** ; **vérification humaine** si doute.

**Règle de prudence régime-dépendante :** frais/humide → prudence = **ne pas
arroser** ; canicule → prudence = **protéger les plantes sensibles** (sans
automatisme autonome).

**Classes de décision candidates (non contractuelles) :**
`DONNEES_INSUFFISANTES` · `HUMIDE` · `CONFORT` · `A_SURVEILLER` ·
`BESOIN_MODERE` · `BESOIN_MARQUE` · `DIFFERE_PLUIE_PREVUE` ·
`ARROSAGE_DECONSEILLE` · `VERIFICATION_HUMAINE`.

> Ces classes sont **candidates**, à éprouver en observation ; **aucune** n'est
> arrêtée ni câblée.

---

## 7. Risques

| # | Risque | Origine |
|---|---|---|
| RQ1 | **Score unique** fusionné détruit l'information (sol lent vs demande rapide) | écart Gemini/Claude |
| RQ2 | **Température prise pour un indicateur d'eau** au lieu d'un proxy de demande | Gemini (à reformuler) |
| RQ3 | **Exclusion abusive** d'un capteur « aberrant » → perte d'un point sec réel | Gemini/Grok |
| RQ4 | **Moyenne** masque le **point sec** → sous-arrosage local | consensus C2 |
| RQ5 | **Pluie prévue** bloque aveuglément, y compris en canicule | Claude |
| RQ6 | **Pluie brute** sans pluie **efficace** → sur/sous-estimation | Grok/Claude |
| RQ7 | **Données stale** traitées en binaire (blocage) au lieu de dégradation | Claude |
| RQ8 | **Vérification humaine** transformée en obligation permanente | Claude/Grok |
| RQ9 | **Canal chaleur** glissant vers un **automatisme autonome** | Claude |
| RQ10 | **Seuils exploratoires** figés prématurément en contrat | les trois |
| RQ11 | **3 points confondus avec 3 zones** | invariant domaine |
| RQ12 | **Point 2** (amplitude faible) mal interprété (faux « sec » ou faux « ok ») | observation terrain |

---

## 8. Questions ouvertes à trancher avant contrat

1. Quelle **durée de fraîcheur maximale** pour les capteurs sol ?
2. Quelle **fenêtre de tendance** : 6 h, 24 h, multi-jours ?
3. Comment qualifier un capteur **« suspect »** sans exclusion abusive ?
4. Comment identifier une **pluie récente « effective »** ?
5. **Pluie brute seule** ou **pluie + réponse sol** ?
6. Quelle **fenêtre pluie récente** : 24 h, 48 h, 72 h ?
7. Quelle **fenêtre pluie prévue** : 24 h, 36 h, 48 h ?
8. **Une** source météo locale ou **plusieurs** ?
9. Quelle **granularité de saison** ?
10. Quel **seuil exploratoire initial** pour observation, **sans décision auto** ?
11. Comment traiter le **Point 2**, qui répond moins fortement ?
12. Comment éviter qu'**un seul point sec** déclenche l'arrosage de toute la zone ?
13. Comment définir **« demande climatique forte »** ?
14. Comment intégrer les **nuits chaudes** ?
15. Quelle **place pour la vérification humaine** ?
16. Quelle **première cible runtime** : **observation seule** ou **recommandation
    non actionnable** ?

---

## 9. Prochaines étapes proposées

1. **Arbitrage opérateur** des questions §8 (au moins : grandeur représentative,
   fenêtres pluie, fraîcheur, première cible runtime).
2. **Phase d'observation** instrumentée (plusieurs semaines, plusieurs cycles
   météo/arrosage) **avant** tout seuil — cohérent avec
   [`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §9 et
   [`07`](../../../contrats/arrosage/07_phase_0_terrain.md).
3. **Première cible runtime probable = observation / perception seule** (canaux
   sol + demande exposés en lecture), **sans recommandation actionnable**.
4. Puis **recommandation diagnostique non actionnable** (modèle « perception pure,
   ne pilote rien »), avant toute idée d'exécution.
5. **Passe contractuelle** ultérieure : matérialiser la doctrine §6 en contrats
   (trajectoire du cadrage), **après** arbitrage et observation.
6. L'**exécution** reste **manuelle supervisée**
   ([`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md)) ; tout
   **automatisme** demeure **très ultérieur et hors périmètre**.

> **Confirmation.** Aucune règle finale décidée, aucun seuil retenu, aucun
> runtime. Confrontation = matière à arbitrage, **pas** doctrine opposable.

---

## Liens

- Cadrage amont (ouverture du chantier) : [`cadrage_besoin_hydrique_decision_arrosage.md`](cadrage_besoin_hydrique_decision_arrosage.md)
- **Socle v0 aval** : chapeau [`13_observation_hydrique_jardin.md`](../../../contrats/arrosage/13_observation_hydrique_jardin.md) · qualité [`14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md) · [`plan_observation_hydrique_v0.md`](plan_observation_hydrique_v0.md)
- Index audits : [`audits/index.md`](../../index.md)
- Besoin hydrique (perception, référence) : [`contrats/arrosage/04_besoin_hydrique.md`](../../../contrats/arrosage/04_besoin_hydrique.md)
- Observation & preuves : [`contrats/arrosage/06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md)
- Pré-requis runtime : [`contrats/arrosage/10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
- Mode manuel supervisé : [`contrats/arrosage/11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md)
- Capteurs humidité sol (3 points / 1 zone) : [`contrats/arrosage/12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md)
- Domaine arrosage (README) : [`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md)

> **Portée.** Confrontation de trois avis externes pour préparer l'arbitrage et la
> future doctrine du besoin hydrique jardin. Seuils exploratoires non normatifs,
> aucun runtime, aucune automatisation. Observation avant action.
