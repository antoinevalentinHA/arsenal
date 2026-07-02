# Cadrage — Arrosage : dashboard Diagnostic (explication du raisonnement du domaine)

| Champ | Valeur |
|---|---|
| **Type** | Cadrage / conception préalable (étude), **sans implémentation** |
| **Domaine** | Arrosage — UI / observabilité (dashboard **Diagnostic**) |
| **Statut** | **Ouvert en cible doctrinale — NON implémentable à ce stade.** Aucun lot YAML actionnable. Aucune carte, aucun template, aucune ressource. |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-06-30 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `c6b50c8` |
| **Cadre** | Aucun YAML Lovelace, aucune carte, aucun template / button-card / socle nouveau, aucune ressource, aucune entité, aucune navigation modifiée, aucun runtime. Ne fixe aucune règle opposable. |
| **Registre** | Lien registre **différé** (ce lot d'étude ne modifie aucun document existant — l'inscription au registre se fera, le cas échéant, lors d'une promotion ultérieure, en co-commit). |

> **Principe de synthèse.**
> **Le dashboard Diagnostic constitue la documentation vivante du raisonnement
> du domaine Arrosage.** Il ne sert pas à superviser des capteurs : il sert à
> expliquer **pourquoi le domaine fonctionne comme il fonctionne aujourd'hui**,
> tout en rendant **lisible son évolution future**.

> **Garde-fou de lecture.** Ce document **ne décide rien d'opposable**, **ne crée
> aucun dashboard**, **ne choisit aucune représentation graphique**. Le
> **référentiel UI** ([`ui/couleurs/`](../../../ui/couleurs/),
> [`ui/socle_ui/`](../../../ui/socle_ui/),
> [`ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md)) et les **contrats
> du domaine** ([`contrats/arrosage/README.md`](../../../contrats/arrosage/README.md))
> **font foi** ; en cas de divergence, ils priment.

---

## 1. Constat (sourcé)

| Élément | État réel | Source |
|---|---|---|
| **Dashboards arrosage existants** | `principal.yaml` (`/arrosage-dashboard`, usage) + `reglages.yaml` (`/reglages-arrosage-dashboard`, paramètres). **Pas de `diagnostic.yaml`.** | `18_lovelace/dashboards/arrosage/` |
| **Anomalie de trio** | L'arrosage est le **seul domaine décisionnel sans `diagnostic.yaml`** : aération, alarme, chauffage, climatisation, déshumidificateur, éclairage, ECS, mouvements, ouvertures, VMC, volets en possèdent un. | `18_lovelace/dashboards/*/diagnostic.yaml` |
| **Diagnostic pont Rain Bird** | Vit **côté Système** (`systeme/rain_bird.yaml`, `/diagnostics-rain-bird-dashboard`), navigable depuis `systeme/principal.yaml` — **infrastructure / maintenance**, à laisser là. | `18_lovelace/dashboards/systeme/rain_bird.yaml` ; [`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md) §6.3 |
| **Canal demande climatique (ET₀/VPD/état)** | Livré (lot P3) mais **affiché nulle part** : aucune occurrence dans `18_lovelace/`. | `12_template_sensors/arrosage/demande_climatique.yaml` |

> **Conséquence.** Toute la chaîne de raisonnement du domaine (perception → décision
> → exécution) existe en runtime mais **n'a aucune surface d'explication** dédiée.
> Le cockpit (`principal`) donne le **verdict** et son **motif** ; il n'expose pas la
> **chaîne de preuves** qui y conduit.

---

## 2. Vocation — expliquer le raisonnement **du domaine Arrosage**

Trois dashboards, trois questions distinctes :

| Dashboard | Question à laquelle il répond |
|---|---|
| **Principal** (usage) | Que fait le système ? Quel est le verdict ? Quelle action est possible ? |
| **Réglages** | Quels paramètres gouvernent le système ? |
| **Diagnostic** (proposé) | **Pourquoi le domaine pense-t-il cela ? Quelles observations ont conduit au verdict ? Quelle chaîne logique a été suivie ? Si le comportement surprend, où est la cause ?** |

> **Principe directeur n°1 — raisonnement du domaine, pas de l'implémentation.**
> Le Diagnostic explique le **raisonnement du domaine Arrosage**, **indépendamment
> de la façon dont il est implémenté** (template, capteur, script, automatisation).
> L'utilisateur ne cherche pas à savoir *quel template* a produit un verdict ; il
> cherche à comprendre **pourquoi le domaine** arrive à cette conclusion. Les
> `entity_id` et la mécanique runtime sont des **moyens**, jamais le sujet de la vue.

Exemple :
- *Principal* : « Arrosage suspendu — raison : suspension pluie. »
- *Diagnostic* : « Pluie observée 72 h = 14 mm (> seuil 10 mm, fiabilité confirmée) ;
  pluie prévue = … ; humidité sol médiane = … ; besoin_sol = inactif ; fenêtre = OK ;
  cooldown = OK ; préconditions = OK » → l'utilisateur **voit où** la chaîne bascule.

---

## 3. Principe directeur n°2 — structure par **domaine**, micro-causalité interne

> **Révision d'implémentation ([#225](https://github.com/antoinevalentinHA/arsenal/pull/225), 2026-07-02).**
> La cible initiale ordonnait le dashboard par **étapes de causalité**
> (Observation → Interprétation → Exécution). À l'usage, un classement **par
> domaine** (précipitations, sol, climat, exécution) s'est révélé plus lisible :
> l'utilisateur retrouve « tout ce qui concerne la pluie » au même endroit. Le
> principe causal n'est **pas abandonné**, il est **descendu d'un cran** : l'ordre
> macro est thématique, mais **à l'intérieur de chaque domaine** la lecture reste
> causale (faits observés → conclusion métier). L'interdit **par familles
> techniques / technologies** demeure entier.

Le dashboard est organisé **par domaine** du raisonnement (précipitations, sol,
canal climatique, exécution), **jamais** par familles d'entités ni par
technologies. À l'intérieur de chaque domaine, l'ordre suit la **causalité** :

```
[Domaine]  :  faits observés  →  interprétation / conclusion métier
```

L'utilisateur lit une **histoire logique par sujet**, pas une succession de
capteurs. Chaque information n'a sa place que si elle répond à :

> **Test d'admission.** « Cela aide-t-il à comprendre le **raisonnement** suivi
> **et** le **fonctionnement** du domaine — tel qu'il est aujourd'hui, et tel qu'il
> évoluera ? » Si non, l'information **n'a pas sa place** sur le Diagnostic.

---

## 4. Les deux strates & la règle de migration

### 4.1 Strate A — chaîne active (ce qui décide aujourd'hui)

Les canaux qui **participent effectivement** au raisonnement produisant le verdict
V1 (`binary_sensor.arrosage_intention`, contrat 17 §3).

### 4.2 Strate B — observation à blanc (ce qui éclaire demain)

> **Principe directeur n°3 — la Strate B n'est pas une zone « divers ».**
> Elle accueille **uniquement** les canaux **déjà intégrés au modèle conceptuel du
> domaine** mais qui **ne participent pas encore aux décisions** : *observation
> aujourd'hui, décision demain*. Un capteur simplement « intéressant », sans place
> dans le modèle du domaine, **n'y figure pas**. **ET₀/VPD** en sont l'exemple type
> (canal demande climatique, contrat 16 ; futur modulateur de durée, C11).

### 4.3 Règle d'architecture — migration B → A

> **Principe directeur n°4 (règle opposable au futur dashboard).** Lorsqu'un canal
> passe du statut **« observation »** au statut **« preuve utilisée par une
> décision »**, il **migre de la Strate B vers la Strate A**. La règle vaut pour
> **tous** les futurs canaux du domaine, pas seulement ET₀/VPD. Dans la lecture
> causale (§5), cette migration est un simple **changement de statut** du canal à sa
> position causale : il cesse d'être marqué « observation à blanc » et rejoint la
> chaîne active qui alimente l'Interprétation / la Décision.

---

## 5. Cartographie causale du contenu (sans créer de carte)

Le contenu est posé **le long de la causalité**, chaque canal portant son **statut**
(A actif / B observation à blanc) :

### Observation — *les faits perçus*
- Pluie observée : cumuls 24/48/72 h. **(A)**
- Pluie prévue (présumée, non fait). **(A)**
- Humidité sol : médiane, points frais, qualité de lecture (point sec / hétérogénéité
  comme **explication de la médiane**, pas comme déclencheurs). **(A)**
- **Canal demande climatique : ET₀, VPD, état du canal — explicitement marqués
  « observation à blanc, ne participe pas encore à la décision ; entrera via C11 ».
  (B)**
- ~~Disponibilité / fraîcheur des données pont (substrat d'observation).~~ **(A)**
  > **Décision d'implémentation ([#222](https://github.com/antoinevalentinHA/arsenal/pull/222), 2026-07-02).** Écarté du dashboard livré : `binary_sensor.rain_bird_pont_donnees_disponibles` / `..._fraiches` étaient déjà exposés **à l'identique** sur le cockpit Système Rain Bird (`systeme/rain_bird.yaml`). Pour éviter la duplication (« pont non recopié → lien Système », §2/§7), la section « Observation — Données pont » a été **retirée** : le substrat technique du pont vit uniquement côté Système ; le Diagnostic ne porte que le raisonnement métier. Ce cadrage étant non normatif, la cible §5 est conservée pour mémoire.

### Interprétation — *les observations transformées en états métier*
- `besoin_sol` (médiane < seuil + hystérésis). **(A)**
- `suspension_pluie` (cumuls / prévue vs seuils → on/off, avec fiabilité + motif). **(A)**
- `reservoir_sol_etat` (complet / degrade / insuffisant / indisponible). **(A)**
- Préconditions runtime (pont exploitable) ; fenêtre (dans / hors) ; cooldown
  (écoulé vs intervalle minimal). **(A)**

### Décision — *le verdict*
- `arrosage_intention` : `categorie` (repos / abstention / suspendu / arrose) +
  `motif` dominant. Le motif désigne **quelle interprétation** a gated le verdict. **(A)**

### Exécution — *l'acte et sa preuve*
- Délégation au script Run supervisé ; état station native ; `dernier_effectif`.
- **Honnêteté d'état** (contrat 06) : confirmé / présumé / inconnu, jamais maquillés. **(A)**

### Conséquence — *l'effet observable et le retour de boucle*
- Dernier arrosage prouvé (horodaté sur switch natif) → **nourrit le cooldown**
  (boucle de causalité qui revient à l'Interprétation). **(A)**
- Lien vers la **santé du pont** (Système) — **jamais** dupliquée ici.

> Cette lecture **raconte la logique** du domaine : on descend des faits jusqu'à la
> conséquence, et la conséquence reboucle sur l'observation. Les `entity_id` ne sont
> que le support ; le sujet est la **chaîne**.

---

## 6. Principes UI

> **Principe directeur n°5 — le dashboard ne choisit jamais la représentation.**
> Le dashboard choisit **quels composants afficher** ; il ne choisit **jamais
> comment représenter un état**. La représentation graphique appartient aux
> **templates**, aux **socles** et au **référentiel UI**. Le YAML Lovelace reste un
> **assemblage de composants** : **aucune logique métier, aucune logique graphique,
> aucune duplication de comportement**.

### 6.1 Langage UI à reprendre (recensé, non figé ici)

- **Socles diagnostic** : [`ui/socle_ui/09_diagnostic.md`](../../../ui/socle_ui/09_diagnostic.md)
  — `socle_diagnostic` (XL 88 px, diagnostic décisionnel), `socle_diagnostic_compact`
  et **`socle_diagnostic_compact_readonly_72`** (valeur capteur, strictement non
  interactif). Interdits socle : *aucune logique métier, aucun mapping d'état,
  **aucun `background-color` dynamique*** — « le diagnostic s'exprime par la valeur
  brute, pas par la mise en forme ».
- **Couleurs** : [`ui/couleurs/01_principes.md`](../../../ui/couleurs/01_principes.md)
  — *« Le backend décide. L'UI observe, traduit et rend lisible. »* Palette
  sémantique (OK/KO/WARN/INFO/OFF) ≠ couleurs de structure ; aucune couleur non
  documentée ; aucune couleur calculée par une logique propre à l'UI.
- **Pattern dashboard** : badges (`bouton_accueil/navigation/retour_badge_carre`) →
  `vertical-stack` → `section_header` (includes) → cartes de **synthèse `*_status_72`**
  par étape causale (cf. `climatisation/diagnostic.yaml`). Réutilisation directe.

### 6.2 Lecture obligatoire avant toute implémentation (Principe n°6)

Avant **tout** YAML, lire **intégralement** :
- [`00_documentation_arsenal/ui/couleurs/`](../../../ui/couleurs/) **et tous les
  documents liés / renvoyés** par ce référentiel ;
- [`00_documentation_arsenal/ui/socle_ui/`](../../../ui/socle_ui/) (00 → 11) ;
- [`00_documentation_arsenal/ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md) ;
- **plusieurs dashboards Diagnostic existants** (chauffage, climatisation, VMC,
  ouvertures, …) pour caler le motif exact.

Le futur dashboard devra reprendre **mêmes socles, mêmes templates, mêmes button-card,
mêmes conventions visuelles, mêmes règles de couleurs — aucune nouvelle convention
graphique**. Objectif : qu'il **paraisse avoir toujours fait partie d'Arsenal**.

### 6.3 Surface 100 % lecture

`tap / hold / double_tap = none` partout (socles `readonly`) ; aucun script, aucun
helper, aucun réglage ; **seule** navigation admise : le lien vers la santé pont
(Système).

---

## 7. Cohérence doctrinale

| Doctrine | Respect |
|---|---|
| **Séparation décision / observation** ([`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md)) | ✅ Diagnostic = observation/explication pure, **aucun contrôle** ; il déplie le calcul de l'intention, il ne re-décide pas. |
| **« Le runtime décide, l'UI explique »** ([`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md)) | ✅ poussé à fond : l'UI explique la **chaîne entière**, pas seulement le motif final du cockpit. |
| **Anti-duplication** | ✅ verdict (principal, altitude 1) vs preuves décomposées (diagnostic, altitude 2) ; pont non recopié (lien) ; météo non recopiée (domaine météo propriétaire). |
| **Honnêteté d'observation** ([`06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md)) | ✅ confirmé / présumé / inconnu affichés distinctement, jamais maquillés. |
| **Température = proxy, jamais déclencheur** ([`13`](../../../contrats/arrosage/13_observation_hydrique_jardin.md)) | ✅ ET₀/VPD en Strate B explicitement non-décisionnelle. |
| **Autorité navigation** ([`navigation/carte_domaines.md`](../../../navigation/carte_domaines.md)) | ✅ un seul hub arrosage ; le dashboard complète le trio existant. |

---

## 8. Conclusions explicites

1. **Créer ou non ?** → **Créer `arrosage/diagnostic.yaml`**, comme **explication du
   raisonnement et du fonctionnement du domaine**, structuré par **causalité**.
   Régularise l'anomalie du trio. **Livrable sans nouveau runtime** : toute la chaîne
   (intention, besoin_sol, suspension_pluie, réservoir_sol, préconditions,
   dernier_effectif) existe déjà ; ET₀/VPD existent (P3).

2. **Périmètre exact** → la **chaîne causale** Observation → Interprétation → Décision
   → Exécution → Conséquence (§5), chaque canal portant son **statut A/B**. **Strate B**
   limitée aux canaux **du modèle conceptuel** (ET₀/VPD aujourd'hui). **Exclus** :
   météo brute non explicative, santé pont détaillée (→ lien Système), tout
   contrôle / réglage, tout capteur « intéressant » hors modèle.

3. **Place dans la navigation** → **3ᵉ membre du trio arrosage**
   (`principal / reglages / diagnostic`), enregistré dans `18_lovelace/dashboards.yaml`
   (ex. `/diagnostic-arrosage-dashboard`), surfacé par les badges arrosage comme les
   11 autres domaines, hub `navigation/domaines/arrosage.md` aligné le moment venu.
   **Pas** dans le hub Système (qui garde la santé pont, vers laquelle le Diagnostic
   pointe).

4. **Lots futurs qui l'alimentent** :
   - **Immédiat** : la chaîne causale active (Strate A) — aucun runtime nouveau requis.
   - **C11/P4 → runtime (modulation de durée)** : ET₀/VPD **migrent B → A** (preuve d'un
     verdict de durée), application directe du Principe n°4.
   - **Contrat 06** : enrichir l'Exécution (confirmé / présumé / inconnu, historique).
   - **C11/P2** : tarissement / fiabilisation sol → enrichit la qualité de lecture sol.

> **Garde-fou de méthode.** Aucune implémentation n'est ouverte par ce cadrage. Le
> jour où elle est décidée, elle suivra « référentiel UI lu d'abord, contrats avant
> YAML », réutilisera strictement les socles/templates existants, restera **100 %
> lecture**, et **publiera l'incrément dans le changelog de sa release** (co-commit).

---

## Renvois

- Décision V1 / intention (motif, categorie) : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) · [`05_intention.md`](../../../contrats/arrosage/05_intention.md)
- Observation & preuves (confirmé / présumé / inconnu) : [`06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md)
- Observation hydrique / canaux / température = proxy : [`13_observation_hydrique_jardin.md`](../../../contrats/arrosage/13_observation_hydrique_jardin.md)
- Canal demande climatique (ET₀/VPD) : [`16_canal_demande_climatique.md`](../../../contrats/arrosage/16_canal_demande_climatique.md)
- Cadrage modulation de durée (C11, migration B→A future) : [`cadrage_modulation_duree_arrosage.md`](cadrage_modulation_duree_arrosage.md)
- Plan d'action arrosage (diagnostic pont côté Système, §6.3) : [`plan_action_arrosage.md`](../../03_plans_action/arrosage/plan_action_arrosage.md)
- Référentiel UI — couleurs : [`ui/couleurs/`](../../../ui/couleurs/)
- Référentiel UI — socles : [`ui/socle_ui/`](../../../ui/socle_ui/) (dont [`09_diagnostic.md`](../../../ui/socle_ui/09_diagnostic.md))
- Référentiel UI — pattern dashboard : [`ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md)
- Cockpit d'état : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)

---

*Cadrage de chantier — non normatif, sans implémentation. Acte une cible doctrinale
(dashboard Diagnostic arrosage) et ses principes d'architecture ; ne fixe aucune règle
opposable et ne crée aucun dashboard. Le référentiel UI et les contrats du domaine font
foi.*
