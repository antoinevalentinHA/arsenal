# Cadrage — Besoin hydrique jardin / décision d'arrosage recommandée

| Champ | Valeur |
|---|---|
| **Type** | Cadrage de chantier (conception préalable, **sans implémentation**) |
| **Domaine** | Arrosage — besoin hydrique jardin, recommandation d'arrosage |
| **Statut** | **Ouvert — cadrage / consultation externe à confronter avant contrat runtime.** Aucune décision finale, aucun runtime. |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-06-26 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `28ebbf3` |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun helper, aucun seuil. Ne fixe aucune règle opposable. |

> **Objet.** Ouvrir proprement le chantier **« besoin hydrique jardin »** et sa
> **recommandation d'arrosage** : poser le problème, recenser les données, lister
> les risques de fausse décision, et **préparer une consultation externe**
> (Claude / Gemini / Grok) **avant** toute passe contractuelle. Doctrine du
> domaine : **observation avant action** ([`06`](../../../contrats/arrosage/06_observation_et_preuves.md),
> [`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md)).

> **Garde-fou de lecture.** Ce document **ne décide rien**, **ne crée aucun
> automatisme d'arrosage**, **ne fixe aucun seuil hydrique final**. Il prépare la
> réflexion. **Aucune automatisation d'arrosage dans ce chantier.**

---

## 1. Objectif du chantier

Construire, à terme et **par étapes documentaires**, une **recommandation
d'arrosage** explicable et prudente pour le jardin, fondée sur le **besoin
hydrique jardin** (perception, [`04`](../../../contrats/arrosage/04_besoin_hydrique.md))
et non sur une humidité instantanée isolée.

- **Observer et recommander avant d'agir** : la cible immédiate est une
  **recommandation**, pas un déclenchement.
- **Priorité** : préserver le jardin (finalité F1, [`01`](../../../contrats/arrosage/01_metier.md)),
  **pas** optimiser au millilitre.
- **Explicabilité** : toute future décision doit être lisible (pourquoi arroser /
  ne pas arroser), prudente et contrôlable.

---

## 2. Périmètre (de ce cadrage)

- Poser le **problème décisionnel** du besoin hydrique jardin ;
- recenser **données disponibles** et **données manquantes** ;
- formaliser un **dossier de consultation IA** (entrée commune Claude/Gemini/Grok) ;
- définir une **grille de confrontation** des avis ;
- esquisser une **trajectoire contractuelle** (contrats futurs probables) **sans
  les écrire**.

> **Une zone Rain Bird, trois points de mesure.** Le système Rain Bird n'a
> **qu'une seule zone / station d'arrosage** par aspersion. Les capteurs nommés
> « Zone 1 / 2 / 3 » sont **trois points de mesure d'humidité** dans cette **zone
> unique**, **pas** trois zones d'arrosage indépendantes
> ([`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §2). Toute la
> réflexion porte donc sur **une décision unique** d'arrosage, informée par
> **trois points**.

---

## 3. Hors périmètre (explicite)

- ❌ **aucun automatisme d'arrosage** (ni direct, ni différé) ;
- ❌ **aucun seuil hydrique final** ; **aucune calibration** déduite ;
- ❌ **aucun runtime** : pas de capteur, helper, automation, script, template, UI ;
- ❌ **aucun déclenchement sur humidité instantanée seule** ;
- ❌ **aucune règle** ignorant la **pluie récente** et la **pluie prévue** ;
- ❌ **les capteurs d'humidité ne déclenchent pas l'arrosage** — ils l'**informent** ;
- ❌ aucune modification Rain Bird bridge / Zigbee2MQTT / capteurs ;
- ❌ l'**automatisme éventuel** (arrosage déclenché par Arsenal) est **très
  ultérieur** et **explicitement hors périmètre immédiat** (subordonné Phase 0,
  [`07`](../../../contrats/arrosage/07_phase_0_terrain.md), et à une décision de
  gouvernance).

---

## 4. Données disponibles (acquises / observables aujourd'hui)

| Donnée | Source | État |
|---|---|---|
| Humidité sol — **Point 1 / 2 / 3** | capteurs Zigbee ([`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md)) | **disponible** (3 points publient ; réponse à l'eau validée) |
| Température sol — Point 1 / 2 / 3 | capteurs Zigbee | disponible (observation secondaire) |
| **Fraîcheur** des mesures d'humidité (âge) | attribut capteur | disponible (à qualifier comme garde stale) |
| Dernier arrosage **Rain Bird** | `active_station` + Stop/Run supervisés ([`06`](../../../contrats/arrosage/06_observation_et_preuves.md), [`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md)) | **partiel** — niveau de preuve confirmé/présumé/inconnu (ACK ≠ preuve hydraulique) |
| Pluie récente | signaux pluie / météo ([`volets_pluie`](../../../contrats/volets_pluie.md), [`meteo`](../../../contrats/meteo/README.md)) | disponible (à brancher conceptuellement) |
| Pluie prévue (court terme) | prévision météo | disponible |
| Température actuelle / max prévue | météo | disponible |
| Humidité air / humidex | météo | disponible (rôle à discuter) |
| Saison / période | calendrier | disponible |
| Contexte jardin (mature, dense, sous-bois, partiellement ombragé, Bordeaux) | connaissance terrain | **qualitatif**, fixe |

---

## 5. Données manquantes / à définir

- **Humidité sol représentative** de la zone : médiane ? moyenne ? **minimum**
  (point le plus sec) ? — **à définir**, ne pas trancher par une moyenne simple.
- **Point le plus sec** : définition et rôle (garde anti-sous-arrosage).
- **Hétérogénéité** entre points : seuil d'alerte de désaccord, interprétation.
- **Tendance** d'humidité sol (cinétique de séchage) : non encore historisée.
- **Dernier arrosage manuel** (tuyau) : **non observable** automatiquement —
  faut-il un renseignement manuel ? (helper futur, hors lot).
- **Durée / intensité de chaleur** (canicule, ETP) : grandeur à formaliser.
- **Seuils** (tous) : **aucun seuil hydrique final à ce stade**.
- **Calibration** des sondes en sol réel : à observer sur durée (24–48 h puis
  plusieurs cycles, [`12`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) §9)
  **avant** toute correction.

---

## 6. Risques de fausse décision (à cadrer pour l'expertise)

- **R1 — Humidité instantanée trompeuse** : une mesure ponctuelle (sonde
  fraîchement arrosée, ou point atypique) conclut à tort « sol humide / sec ».
- **R2 — Moyenne aveuglante** : une moyenne simple **masque le point le plus
  sec** → sous-arrosage d'une partie de la zone.
- **R3 — Ignorer la pluie prévue** : arroser juste avant une pluie → **sur-arrosage**
  (gaspillage + risque racinaire), F2 ([`01`](../../../contrats/arrosage/01_metier.md)).
- **R4 — Ignorer la pluie récente** : arroser un sol déjà détrempé.
- **R5 — Donnée `stale`** : décider sur une mesure périmée (sonde muette) → la
  direction de défaillance impose de **ne jamais conclure « humide » par défaut**
  ([`04`](../../../contrats/arrosage/04_besoin_hydrique.md) §4).
- **R6 — Désaccord entre points** non géré : conclusion arbitraire.
- **R7 — Forte chaleur sous-pondérée** : canicule → besoin réel sous-estimé.
- **R8 — Confusion 3 points = 3 zones** : raisonner comme s'il y avait trois
  arrosages indépendants (faux, §2).
- **R9 — Sur-confiance capteur** : traiter une sonde non calibrée comme une vérité
  absolue.

---

## 7. Points à soumettre à expertise externe

1. Quelle **grandeur représentative** d'humidité pour **une zone à trois points**
   (médiane / moyenne / **minimum** / combinaison) ?
2. Quel **rôle** et quelle **priorité** pour la **pluie prévue** vs **pluie
   récente** dans la décision ?
3. Comment intégrer **fraîcheur** et **tendance** plutôt que l'instantané ?
4. Comment **pondérer la chaleur** (température max, durée, ETP) prudemment ?
5. Comment gérer le **désaccord entre points** (hétérogénéité) ?
6. Comment gérer les **données `stale` / indisponibles** sans priver le jardin ?
7. Quelle **logique agronomique** pour un **jardin mature, dense, type sous-bois,
   partiellement ombragé, à Bordeaux** (climat océanique, étés chauds) ?
8. Quels **garde-fous** rendraient une recommandation **prudente et explicable** ?

---

## 8. Dossier de consultation IA (entrée commune)

> **Règle de consultation.** Claude, Gemini et Grok reçoivent **le même dossier
> d'entrée** et répondent au **même format** (§9). **Interdiction explicite de
> proposer du YAML, du code, ou une implémentation Home Assistant.** On demande
> une **logique agronomique et décisionnelle**, **pas** un code.

### 8.1 Contexte jardin
Jardin **mature, dense, esprit sous-bois, partiellement ombragé**, à **Bordeaux**
(climat océanique aquitain : étés chauds et secs possibles, pluies réparties).
Objectif : **préserver le jardin**, pas optimiser au millilitre.

### 8.2 Contraintes Rain Bird
- **Une seule zone / station d'arrosage** par aspersion (pas de zonage fin).
- Pont Rain Bird **opérationnel** mais santé possible **`degrade`** (exploitable
  si préconditions runtime `on`).
- **Stop supervisé** et **Station 1 courte supervisée** **validés terrain**
  (commande manuelle supervisée, [`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md) §9).
- Observation d'arrosage **partielle** : `active_station` n'est pas une preuve
  hydraulique ; niveaux **confirmé / présumé / inconnu**
  ([`06`](../../../contrats/arrosage/06_observation_et_preuves.md)).

### 8.3 Capteurs disponibles
- **Trois points de mesure** d'humidité + température sol (Zigbee), **dans la zone
  unique** (pas trois zones).
- Réponse à l'eau **validée fonctionnellement** ; **non calibrés en sol réel** ;
  fraîcheur de mesure exposée.

### 8.4 Observations terrain déjà acquises
- Réponse nette à un apport d'eau (test tuyau) : +21 à +38 points d'humidité selon
  le point ; **Point 2 réagit moins fortement** (cause non tranchée).
- Aucune base de seuil ; **valeurs initiales ≠ seuils**.

### 8.5 Paramètres météo envisagés
Pluie récente, pluie prévue (court terme), température actuelle, température max
prévue, durée/intensité de chaleur, humidité air / humidex (rôle à discuter),
saison.

### 8.6 Demande adressée aux IA
Proposer une **logique de décision agronomique** : quelles grandeurs, comment les
combiner, quel rôle pour la pluie, comment être **prudent** (anti-sur-arrosage
**et** anti-sous-arrosage), comment gérer incertitude et données périmées — **sans
aucun code ni YAML**.

---

## 9. Format de réponse imposé (commun aux trois IA)

Chaque IA répond selon **la même structure**, pour permettre la confrontation :

1. **Paramètres indispensables** (et pourquoi) ;
2. **Paramètres secondaires** ;
3. **Grandeur d'humidité représentative** retenue (médiane / moyenne / min /…) + justification ;
4. **Rôle de la pluie récente** et **de la pluie prévue** ;
5. **Logique de décision** (texte, arbre de décision conceptuel — **pas de code**) ;
6. **Seuils indicatifs éventuels** (clairement marqués **non définitifs**) ;
7. **Gestion des données `stale`** et des **désaccords entre points** ;
8. **Prudence forte chaleur** ;
9. **Risques identifiés** par l'IA ;
10. **Degré de confiance** (auto-évaluation).

---

## 10. Grille de confrontation des avis

À remplir après réception des trois réponses (une colonne par IA) :

| Critère de comparaison | Claude | Gemini | Grok |
|---|---|---|---|
| Paramètres jugés **indispensables** | | | |
| Paramètres **secondaires** | | | |
| **Règles** proposées | | | |
| **Seuils** proposés (non définitifs) | | | |
| Rôle de la **pluie prévue** | | | |
| Rôle de la **pluie récente** | | | |
| Rôle de l'**humidité minimale** (point sec) | | | |
| **Médiane / moyenne / minimum** retenu | | | |
| Gestion des **données `stale`** | | | |
| Gestion des **désaccords entre points** | | | |
| **Prudence fortes chaleurs** | | | |
| **Risques** identifiés | | | |
| **Degré de confiance** | | | |

> **Critères de sélection / synthèse.** On privilégiera l'avis (ou la synthèse)
> qui : (a) **prend en compte la pluie prévue ET récente** ; (b) **ne masque pas
> le point le plus sec** ; (c) **gère explicitement les données périmées** ;
> (d) reste **prudent en forte chaleur** ; (e) produit une décision **explicable**.
> Un avis qui ignore l'un de ces points est **disqualifié** sur ce critère.

---

## 11. Trajectoire contractuelle (probable, NON implémentée)

Esquisse de la suite documentaire ; **aucun** de ces contrats n'est écrit ici.
Ordre indicatif, **observation → recommandation → (très ultérieurement) action** :

1. **Pluie récente** — perception (fenêtre, cumul) ;
2. **Pluie prévue** — perception (court terme) ;
3. **Capteur global humidité jardin** — agrégation des 3 points (grandeur
   représentative à arbitrer : médiane / min /…) ;
4. **Point sec / point représentatif** — perception de l'hétérogénéité ;
5. **Besoin hydrique jardin** — perception synthétique
   ([`04`](../../../contrats/arrosage/04_besoin_hydrique.md) à matérialiser) ;
6. **Recommandation d'arrosage** — diagnostic explicable (sur le modèle de la
   recommandation ventilation clim : perception pure, ne pilote rien) ;
7. **Garde-fous** — anti-sur-arrosage / anti-sous-arrosage, prudence chaleur,
   gestion `stale` ;
8. **Notification / cockpit** — observabilité de la recommandation ;
9. **Script manuel recommandé** (éventuel) — exécution **manuelle supervisée**
   ([`11`](../../../contrats/arrosage/11_mode_manuel_supervise.md)), jamais
   automatique ;
10. **Automatisme éventuel** — **très ultérieur**, **hors périmètre immédiat**,
    subordonné à la clôture Phase 0 ([`07`](../../../contrats/arrosage/07_phase_0_terrain.md)) et à une décision de gouvernance explicite.

> Cette trajectoire **n'engage rien** : elle oriente la consultation et la future
> passe contractuelle. **Consultation externe à confronter avant contrat runtime.**

---

## 12. Confirmation de cadrage

- ✅ **Aucune règle finale décidée** ; **aucun seuil hydrique final** ;
- ✅ **aucune automatisation d'arrosage** introduite ;
- ✅ **aucun runtime** touché (doc seule) ;
- ✅ les **capteurs informent**, ne **déclenchent pas** l'arrosage ;
- ✅ **une zone Rain Bird, trois points de mesure** — invariant rappelé partout ;
- ✅ **observation avant action**.

---

## Liens

- **Confrontation des avis externes (Gemini/Grok/Claude)** : [`confrontation_avis_besoin_hydrique.md`](confrontation_avis_besoin_hydrique.md)
- Index audits : [`audits/index.md`](../../index.md)
- Besoin hydrique (perception, référence) : [`contrats/arrosage/04_besoin_hydrique.md`](../../../contrats/arrosage/04_besoin_hydrique.md)
- Observation & preuves : [`contrats/arrosage/06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md)
- Phase 0 terrain : [`contrats/arrosage/07_phase_0_terrain.md`](../../../contrats/arrosage/07_phase_0_terrain.md)
- Pré-requis runtime : [`contrats/arrosage/10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
- Mode manuel supervisé : [`contrats/arrosage/11_mode_manuel_supervise.md`](../../../contrats/arrosage/11_mode_manuel_supervise.md)
- Capteurs humidité sol (3 points / 1 zone) : [`contrats/arrosage/12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md)
- Domaine arrosage (README) : [`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md)

> **Portée.** Cadrage de chantier : pose le problème du besoin hydrique jardin et
> prépare la consultation externe. Aucune règle, aucun seuil, aucun runtime,
> aucune automatisation. Observation avant action.
