# CONTRAT ARSENAL — ARROSAGE
## 15 — Canal réservoir sol (observation v0)

**Version contrat :** v0.1
**Statut :** **Normatif — définit les grandeurs d'observation** du **canal
réservoir sol (lent)**. **Observation / diagnostic uniquement**, en deçà de toute
recommandation et de toute action. **Runtime v0 livré :**
`12_template_sensors/arrosage/reservoir_sol.yaml` (PR #103) produit ces grandeurs ;
le contrat reste la référence normative de ce qui doit être observé.

> **Position dans le socle v0.** Ce contrat **dérive** du chapeau
> [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md) (canal
> §3.1) et **dépend** de [`14_qualite_donnees_sol.md`](14_qualite_donnees_sol.md)
> (qualité/confiance des points). Il **matérialise le vocabulaire** du canal
> réservoir sol, **sans** créer le runtime, **sans** décider la recommandation,
> **sans** choisir de seuil hydrique final.

> **Garde-fou de lecture.** Une zone Rain Bird, **trois points de mesure**. Aucune
> grandeur de ce contrat n'est une **décision** : ce sont des **observations
> lentes**. **Pas de score unique**, **pas de seuil chiffré opposable**.

---

## Objet

Définir, comme **cible d'observation v0**, les **grandeurs du réservoir sol** que
le futur runtime exposera : **humidité représentative**, **point le plus sec**,
**hétérogénéité**, **nombre de points frais utilisés**, **état qualitatif du
canal**. Ces grandeurs sont **factuelles et lentes** ; elles **n'émettent aucune
recommandation** et **ne pilotent rien**.

---

## 1. Périmètre & dépendances

- **Sources** : les trois points d'humidité sol (`*_soil_moisture`) d'une **zone
  unique** ([`12`](12_capteurs_humidite_sol.md) §1), filtrés par leur **qualité**
  ([`14`](14_qualite_donnees_sol.md) §2).
- **Amont** : chapeau [`13`](13_observation_hydrique_jardin.md) (canaux, frontière
  v0) ; qualité [`14`](14_qualite_donnees_sol.md) (frais/stale/indisponible/suspect).
- **Aval (hors v0)** : la future couche **recommandation** (non émise), et les
  **autres canaux** (demande climatique, modulateurs) — **autres contrats**.

> **« Points frais utilisables ».** Tous les agrégats de ce contrat se calculent
> sur les **points frais utilisables** au sens de [`14`](14_qualite_donnees_sol.md) :
> **stale** et **indisponible** **n'entrent pas** dans les agrégats ; un point
> **suspect** **n'est pas exclu automatiquement** sans **critère robuste futur**
> ([`14`](14_qualite_donnees_sol.md) §5).

---

## 2. Humidité représentative du réservoir sol

- **Grandeur candidate v0 : médiane des points frais utilisables.**
- **Justification** : plus **robuste** qu'une moyenne simple ; **ne masque pas**
  autant les extrêmes ; **cohérente** avec seulement trois points ; reste une
  **observation**, pas une décision.

**Interdits (opposables) :**
- ❌ ne pas en faire un **score de besoin hydrique** ;
- ❌ ne pas l'utiliser **seule** pour **recommander** l'arrosage ;
- ❌ ne pas l'assimiler à **« le jardin va bien »** ;
- ❌ ne pas en faire une **vérité globale absolue** du jardin.

> La médiane est **une** lecture du réservoir, **toujours** accompagnée du point
> sec (§3), de l'hétérogénéité (§4) et de la qualité (§6).

---

## 3. Point le plus sec

- **Grandeur candidate v0 : minimum des points frais utilisables.**
- **Exposé séparément** de la médiane (jamais fondu dedans).

**Invariants (opposables) :**
- le **minimum seul n'est jamais suffisant** pour déclarer **toute la zone sèche** ;
- le **minimum seul ne déclenche aucun arrosage** ;
- le minimum est un **signal de vulnérabilité / attention / hétérogénéité**.

> Il **pourra plus tard** contribuer à une couche **recommandation**, **mais pas
> en v0** ([`13`](13_observation_hydrique_jardin.md) §2/§4).

---

## 4. Hétérogénéité

- **Grandeur candidate v0 : étendue `max − min`** sur les points frais utilisables.
- **Rôle** : mesurer l'**écart entre points** ; indiquer si le jardin est
  **homogène ou hétérogène** ; **aider à qualifier la confiance** de l'humidité
  représentative (§2).

**Concepts qualitatifs (sans valeur chiffrée normative) :**
`faible` · `modérée` · `forte` · `non qualifiable`.

> **Aucun seuil définitif d'hétérogénéité** n'est fixé ici. Les bornes chiffrées
> restent **exploratoires** (audits/conception,
> [`plan_observation_hydrique_v0`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)),
> proposées **après observation**.

---

## 5. Nombre de points frais utilisés

Le futur runtime **doit rendre visible** le **nombre de points frais** utilisés
dans les agrégats. Lecture conceptuelle (alignée [`14`](14_qualite_donnees_sol.md) §3/§4) :

| Points frais | Lecture du canal |
|---|---|
| **3/3** | lecture **complète** |
| **2/3** | lecture **dégradée** |
| **1/3** | canal **insuffisant** pour une agrégation représentative |
| **0/3** | canal **indisponible** |

> **Le contrat fixe ce qui doit être visible, pas comment.** Les `entity_id` ne
> sont pas figés par ce contrat : la convention runtime est portée par le lot
> d'implémentation (**livré** — `12_template_sensors/arrosage/reservoir_sol.yaml`,
> PR #103). Le contrat définit les grandeurs ; le runtime en choisit la forme.

---

## 6. État qualitatif du canal réservoir sol

Vocabulaire candidat v0, **strictement diagnostic / observation** :

| État | Sens (lecture du canal, **pas** une décision) |
|---|---|
| `complet` | 3/3 points frais et cohérents |
| `degrade` | un point manquant/stale/suspect ; agrégats exploitables avec réserve |
| `insuffisant` | trop peu de points frais pour une lecture représentative |
| `indisponible` | aucun point frais exploitable |
| `heterogene` | points frais mais **étendue forte** (désaccord marqué) |
| `a_verifier` | doute → **lecture humaine souhaitable** (drapeau, [`14`](14_qualite_donnees_sol.md) §7) |

> **Ces états ne sont PAS des recommandations d'arrosage.** Ils ne signifient ni
> **« arroser »**, ni **« ne pas arroser »** : ils **qualifient seulement la
> lecture** du canal réservoir sol.

---

## 7. Relation avec la qualité des données sol (contrat 14)

Le contrat 15 **dépend** du contrat [`14`](14_qualite_donnees_sol.md) :

- les points **stale** **ne sont pas traités comme frais** ;
- les points **indisponibles** **n'entrent pas** dans les agrégats ;
- les points **suspects** **ne sont pas exclus automatiquement** sans **critère
  robuste** ([`14`](14_qualite_donnees_sol.md) §5) ;
- une lecture fondée sur **moins de 3 points** est marquée **dégradée** ou
  **insuffisante** selon le cas (§5/§6) ;
- l'agrégat **expose toujours sa qualité / confiance** (nombre de points frais,
  état du canal).

---

## 8. Relation avec les futurs autres canaux

Le canal réservoir sol **ne décide pas seul**. Il **n'intègre PAS** (autres
contrats / hors v0) :

- ❌ pluie récente ; ❌ pluie prévue ;
- ❌ température ; ❌ saison ; ❌ canicule ;
- ❌ dernier arrosage ; ❌ disponibilité Rain Bird ;
- ❌ recommandation.

> Ces éléments relèvent du **canal demande climatique** et des **modulateurs**
> ([`13`](13_observation_hydrique_jardin.md) §3), dans des contrats futurs.

---

## 9. Relation avec la future recommandation

- le canal réservoir sol fournit des **observations lentes** ;
- il **n'émet pas de recommandation** ;
- il **ne pilote pas Rain Bird** ;
- il **ne crée aucun bouton** ;
- il **ne produit pas** `besoin_hydrique` ;
- il **ne produit pas** `arrosage_recommande`.

---

## 10. Point 2 (note d'observation)

Le **Point 2** a montré une **amplitude de réponse plus faible** lors du test
tuyau ([`12`](12_capteurs_humidite_sol.md) §12, [`14`](14_qualite_donnees_sol.md) §6).
Cette observation est **conservée** ; elle **ne justifie ni calibration, ni
correction, ni déclassement** à ce stade. Elle **doit être observée** dans le plan
v0. La possibilité de **bandes par capteur** reste une **hypothèse future, non
contractuelle**.

---

## 11. Seuils

- **Aucun seuil chiffré définitif** n'est introduit ici.
- Les **seuils exploratoires** restent dans les documents d'**audit/conception**
  ([`confrontation`](../../audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md),
  [`plan_observation_hydrique_v0`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)).
- Les seuils seront **proposés ultérieurement après observation** ; **aucun** ne
  devient **opposable** dans ce contrat.

---

## 12. Non-objectifs (hors périmètre)

- ❌ créer `sensor.jardin_besoin_hydrique`, `sensor.jardin_recommandation_arrosage`,
  `binary_sensor.jardin_arrosage_recommande` ;
- ❌ décider « arroser / ne pas arroser » ;
- ❌ faire d'un **seul point sec** une décision d'arrosage ;
- ❌ faire de la **médiane** une vérité globale absolue ;
- ❌ créer une **moyenne simple** comme vérité du jardin ;
- ❌ calibrer / corriger le **Point 2** ;
- ❌ relier directement l'humidité sol à Rain Bird ;
- ❌ tout runtime / UI / helper / automation / script / template.

---

## Renvois

- Chapeau observation hydrique (frontière v0, canaux) : [`13_observation_hydrique_jardin.md`](13_observation_hydrique_jardin.md)
- Qualité des données sol (dépendance) : [`14_qualite_donnees_sol.md`](14_qualite_donnees_sol.md)
- Capteurs humidité sol (sources, Point 2) : [`12_capteurs_humidite_sol.md`](12_capteurs_humidite_sol.md)
- Observation & preuves : [`06_observation_et_preuves.md`](06_observation_et_preuves.md)
- Plan d'observation v0 (seuils exploratoires) : [`plan_observation_hydrique_v0.md`](../../audits/02_conception/arrosage/plan_observation_hydrique_v0.md)
- Confrontation des avis (médiane/min/hétérogénéité) : [`confrontation_avis_besoin_hydrique.md`](../../audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md)
- Index du domaine : [`README.md`](README.md)
