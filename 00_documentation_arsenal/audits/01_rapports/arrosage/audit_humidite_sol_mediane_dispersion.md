# Audit — Humidité du sol : médiane vs dispersion des sondes

| Champ | Valeur |
|---|---|
| **Type** | Audit **statique, lecture seule** — observabilité hydrique (canal réservoir sol) |
| **Domaine** | Arrosage — humidité du sol (6 points de mesure, zone Rain Bird unique) |
| **Statut** | **Ouvert — diagnostic + recommandations sans code.** Aucun runtime, aucun seuil, aucune action. |
| **Version** | 0.1 |
| **Déclencheur** | Constat terrain Antoine : la médiane (21,3 %) ne rend pas visible l'effet d'un arrosage réel du matin ; forte dispersion entre sondes. |
| **Contrats normatifs de référence** | [`12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md), [`14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md), [`15_canal_reservoir_sol.md`](../../../contrats/arrosage/15_canal_reservoir_sol.md), [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) |

> **Garde-fou de lecture.** Ce rapport **ne fixe aucun seuil**, **ne modifie aucun
> fichier runtime / YAML / Lovelace / helper / template / script / automation /
> recorder / customize**, **n'invente aucun `entity_id`** et **ne renomme rien**.
> Les seuils évoqués sont des **hypothèses d'audit**, jamais des décisions
> d'implémentation. Toute suite d'implémentation reste à **arbitrer par Antoine**.

---

## 1. Résumé exécutif

1. **La médiane est mathématiquement correcte** : `(20,22 + 22,34) / 2 = 21,28 ≈
   21,3`. Le calcul runtime ([`reservoir_sol.yaml`](../../../../12_template_sensors/arrosage/reservoir_sol.yaml)) reproduit exactement cette valeur sur
   les 6 points frais.
2. **Le problème signalé n'est pas un problème d'algorithme de décision, mais un
   problème d'observabilité.** Avec seulement 2 sondes sur 6 réellement mouillées
   (zones 1 et 3), la médiane — par construction robuste aux extrêmes — **reste
   ancrée sur l'amas sec** et bouge peu : c'est le comportement **attendu et
   voulu** par le contrat 15 §2, pas une anomalie.
3. **Pour la décision, la médiane joue correctement son rôle protecteur.** Sur les
   valeurs fournies, `médiane = 21,3 % < seuil 30 %` ⇒ `binary_sensor.arrosage_besoin_sol = on`
   (besoin franc). Une **moyenne** simple donnerait `32,9 %`, soit **au-dessus du
   seuil** — elle masquerait le besoin en se laissant tirer par les 2 sondes
   humides. La médiane est donc **le bon indicateur de décision** ici.
4. **Le vrai manque est double** : (a) les indicateurs de dispersion **existent
   déjà en backend** (`minimum`, `heterogeneite`, `points_frais`) mais **ne sont
   affichés sur aucun dashboard** ; (b) les **valeurs par sonde** (zone 1..6) ne
   sont **ni historisées ni affichées**, rendant impossible de *voir* qu'un
   arrosage a mouillé 2 points sur 6.
5. **Divergence de nommage batterie zones 4/5/6 confirmée** (`sensor.sol_jardin_zone_{4,5,6}_battery`
   vs `sensor.jardin_humidite_sol_zone_{1,2,3}_battery`) — déjà relevée et assumée
   verbatim par le contrat 12 §5 ; **aucune action de renommage recommandée**.
6. **Recommandation de fond** : **conserver la médiane comme indicateur de
   décision**, et **compléter l'observabilité** (afficher min / hétérogénéité,
   exposer les sondes individuellement, tracer un delta avant/après). Ne **pas**
   piloter l'arrosage sur une sonde extrême. Ne **rien** implémenter avant une
   **période d'observation terrain** et un **arbitrage explicite**.

---

## 2. Données analysées

Contexte terrain fourni (non relevé par l'audit, pris comme entrée) :

```text
Médiane annoncée : 21.3

sensor.jardin_humidite_sol_zone_1_soil_moisture = 47.66
sensor.jardin_humidite_sol_zone_2_soil_moisture = 22.34
sensor.jardin_humidite_sol_zone_3_soil_moisture = 73.32
sensor.jardin_humidite_sol_zone_4_soil_moisture = 20.22
sensor.jardin_humidite_sol_zone_5_soil_moisture = 16.85
sensor.jardin_humidite_sol_zone_6_soil_moisture = 17.18
```

Série triée : `16.85 · 17.18 · 20.22 · 22.34 · 47.66 · 73.32`

| Statistique | Valeur | Existe en backend ? | Affichée dashboard ? |
|---|---|---|---|
| Médiane | **21,28 → 21,3 %** | ✅ `sensor.jardin_humidite_sol_mediane` | ✅ cockpit (mini-graph) + entrée décision |
| Minimum | **16,85 %** | ✅ `sensor.jardin_humidite_sol_minimum` | ❌ **non affiché** |
| Maximum | 73,32 % | ❌ (implicite dans hétérogénéité) | ❌ |
| Moyenne | 32,93 % | ❌ (volontairement absent, contrats 15 §12) | ❌ |
| Étendue max−min (hétérogénéité) | **56,47 → 56,5 %** | ✅ `sensor.jardin_humidite_sol_heterogeneite` | ❌ **non affichée** |
| Points frais utilisés | 6 (si toutes fraîches) | ✅ `sensor.jardin_humidite_sol_points_frais` | ✅ Diagnostic |
| Nb sondes < seuil 30 % | 4 (zones 2,4,5,6) | ❌ **inexistant** | ❌ |
| Écart médiane↔max | 52,0 | ❌ inexistant | ❌ |
| Écart médiane↔min | 4,45 | ❌ inexistant | ❌ |
| Delta par sonde avant/après | — | ❌ inexistant | ❌ |

> **Note de cohérence.** La médiane runtime ne se calcule **que sur les points
> frais** (dernier `last_reported` < 6 h, cf. §3 du runtime). La valeur 21,3
> suppose les 6 points frais au moment du relevé — hypothèse compatible avec les
> 6 valeurs numériques fournies.

---

## 3. Cartographie des fichiers existants

Type : **contrat** (normatif documentaire) · **runtime** (YAML actif HA) · **UI**
(Lovelace) · **observabilité** (recorder / historisation) · **registre** (index) ·
**conception/plan** (audit non normatif).

### 3.1 Contrats (documentaire normatif)

| Chemin | Rôle réel | Type | Zones 1-6 | Médiane | Min/Max/Dispersion/Cohérence |
|---|---|---|---|---|---|
| [`contrats/arrosage/12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md) | Relevé factuel des sondes + doctrine d'observation ; table de mapping ; divergence batterie 4/5/6 | contrat | ✅ (6, table §6) | non (perception) | mention hétérogénéité §12 (test tuyau) |
| [`contrats/arrosage/14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md) | Socle qualité : frais/stale/indispo/suspect ; qualité agrégée | contrat | ✅ (6, §1) | non | états `incohérente` (hétérogénéité anormale) §3 |
| [`contrats/arrosage/15_canal_reservoir_sol.md`](../../../contrats/arrosage/15_canal_reservoir_sol.md) | Définit les grandeurs d'observation : médiane, min, hétérogénéité, points frais, état | contrat | ✅ (6, §1) | ✅ candidate §2 | ✅ min §3, hétérogénéité §4, état `heterogene`/`a_verifier` §6 |
| [`contrats/arrosage/17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) | Décision V1 : médiane + état → besoin → intention → délégation script | contrat | non (via agrégats) | ✅ entrée §2 | état réservoir consommé §3 |
| [`contrats/arrosage/04_besoin_hydrique.md`](../../../contrats/arrosage/04_besoin_hydrique.md) | Perception conceptuelle du besoin ; garde anti-faux-négatif | contrat | non | oui (conceptuel) | non |
| [`contrats/arrosage/06_observation_et_preuves.md`](../../../contrats/arrosage/06_observation_et_preuves.md) | Honnêteté d'état (switch ≠ ACK) | contrat | non | non | non |

### 3.2 Runtime (template sensors / helpers)

| Chemin | Rôle réel | Type | Zones 1-6 | Médiane | Min/Max/Dispersion |
|---|---|---|---|---|---|
| [`12_template_sensors/arrosage/reservoir_sol.yaml`](../../../../12_template_sensors/arrosage/reservoir_sol.yaml) | **Cœur** du sujet : liste JSON des valeurs fraîches → médiane, minimum, hétérogénéité (max−min), points frais, état qualitatif | runtime | ✅ (6, liste `pts`) | ✅ `_mediane` | ✅ `_minimum`, `_heterogeneite` |
| [`12_template_sensors/arrosage/besoin_sol.yaml`](../../../../12_template_sensors/arrosage/besoin_sol.yaml) | `binary_sensor.arrosage_besoin_sol` : médiane sous seuil + hystérésis ; attribut `motif` | runtime | non (médiane) | ✅ consomme | non |
| [`03_input_numbers/arrosage/decision_v1.yaml`](../../../../03_input_numbers/arrosage/decision_v1.yaml) | Seuil déclenchement (défaut 30 %), hystérésis (5 %), cooldown (24 h) | runtime | non | seuil comparé à médiane | non |
| [`12_template_sensors/arrosage/intention.yaml`](../../../../12_template_sensors/arrosage/intention.yaml) | Intention V1 (agrège besoin + conditions) | runtime | non | indirect | non |

### 3.3 UI (Lovelace)

| Chemin | Rôle réel | Type | Zones 1-6 | Médiane | Min/Max/Dispersion |
|---|---|---|---|---|---|
| [`18_lovelace/dashboards/arrosage/principal.yaml`](../../../../18_lovelace/dashboards/arrosage/principal.yaml) | Cockpit : intention + **mini-graph médiane 72 h** + commande manuelle | UI | ❌ | ✅ (graphe) | ❌ |
| [`18_lovelace/dashboards/arrosage/diagnostic.yaml`](../../../../18_lovelace/dashboards/arrosage/diagnostic.yaml) | Diagnostic : état réservoir sol + points frais + besoin sol (`motif`) | UI | ❌ | ❌ (via besoin) | ❌ (ni min ni hétérogénéité) |
| [`18_lovelace/dashboards/arrosage/reglages.yaml`](../../../../18_lovelace/dashboards/arrosage/reglages.yaml) | Réglages des helpers de décision | UI | ❌ | seuil | ❌ |

### 3.4 Observabilité (recorder)

| Chemin | Rôle réel | Type | Constat |
|---|---|---|---|
| [`recorder.yaml`](../../../../recorder.yaml) | Historisation | observabilité | **Historisés** : `_mediane`, `_minimum`, `_heterogeneite`, `_points_frais`, `reservoir_sol_etat`, `besoin_sol`, `intention`. **NON historisés** : les 6 `*_soil_moisture` bruts (exclus par doctrine, contrat 12 §13). |

### 3.5 Périmètres transverses & registres

| Chemin | Rôle réel | Type | Zones 1-6 |
|---|---|---|---|
| [`02_groups/batteries.yaml`](../../../../02_groups/batteries.yaml) + [`01_customize/batteries.yaml`](../../../../01_customize/batteries.yaml) | Supervision batterie (dont divergence 4/5/6) | observabilité | ✅ (batteries) |
| [`02_groups/connectivite/zigbee_lqi.yaml`](../../../../02_groups/connectivite/zigbee_lqi.yaml) + customize | Supervision linkquality | observabilité | ✅ (LQI) |
| [`audits/02_conception/arrosage/plan_observation_hydrique_v0.md`](../../02_conception/arrosage/plan_observation_hydrique_v0.md) | Plan d'apprentissage v0 (cinétique, Point 2, pluie efficace, hétérogénéité) | conception | ✅ |
| [`audits/02_conception/arrosage/confrontation_avis_besoin_hydrique.md`](../../02_conception/arrosage/confrontation_avis_besoin_hydrique.md) | Consensus externe : médiane + min, hétérogénéité, pas de moyenne | conception | ✅ |
| [`audits/index.md`](../../index.md) + [`audits/REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) | Navigation / cockpit d'état | registre | — |

---

## 4. Cohérence des entités zones 1 à 6

Relevé **verbatim** depuis le contrat 12 §5/§6 et le runtime — **aucune
normalisation, aucun renommage, aucun `entity_id` inventé**.

### 4.1 Humidité (homogène)

`sensor.jardin_humidite_sol_zone_{1,2,3,4,5,6}_soil_moisture` — schéma **homogène**
pour les 6 points ; tous consommés par la liste `pts` du runtime.

### 4.2 Température (homogène, secondaire)

`sensor.jardin_humidite_sol_zone_{1..6}_temperature` — schéma **homogène** ;
zones 4/5/6 **confirmées au relevé** (contrat 12 §5). **Non consommées** par les
agrégats ni le recorder (observation secondaire, jamais déclencheur).

### 4.3 Linkquality (homogène)

`sensor.jardin_humidite_sol_zone_{1..6}_linkquality` — schéma **homogène** ;
intégrées à `group.zigbee_linkquality_all`.

### 4.4 Batterie — ⚠️ **DIVERGENCE DE NOMMAGE confirmée** (relevée, non normalisée)

| Points | `entity_id` batterie (verbatim) | Schéma |
|---|---|---|
| 1, 2, 3 | `sensor.jardin_humidite_sol_zone_1_battery`, `..._zone_2_battery`, `..._zone_3_battery` | `jardin_humidite_sol_zone_N` |
| 4, 5, 6 | `sensor.sol_jardin_zone_4_battery`, `sensor.sol_jardin_zone_5_battery`, `sensor.sol_jardin_zone_6_battery` | **`sol_jardin_zone_N`** (ordre inversé, sans `humidite`) |

> Divergence **déjà documentée** (contrat 12 §5 « ⚠️ Divergence de nommage
> batterie — relevée, non normalisée » et §13). Les `entity_id` sont utilisés
> **verbatim** ; le dépôt fait le **choix explicite de ne pas renommer** (doctrine
> README « aucun `entity_id` relevé n'est normalisé »). **Cet audit confirme ce
> choix** : aucune action de renommage recommandée (risque > bénéfice).

### 4.5 Calibration (interdite au runtime auto)

`number.jardin_humidite_sol_zone_1_celsius_degree_calibration` /
`..._fahrenheit_degree_calibration` — **relevés zone 1**, **dérivés zones 2/3**,
non relevés au-delà. **Interdits au pilotage automatique** (contrat 12 §8).

### 4.6 Agrégats dérivés (entités Arsenal)

| `entity_id` | Rôle |
|---|---|
| `sensor.jardin_humidite_sol_valeurs_fraiches` | Source de vérité interne (liste JSON des valeurs fraîches) |
| `sensor.jardin_humidite_sol_mediane` | Médiane des points frais (≥ 2) — **entrée décision** |
| `sensor.jardin_humidite_sol_minimum` | Point le plus sec (≥ 1) — **diagnostic, non affiché** |
| `sensor.jardin_humidite_sol_heterogeneite` | Étendue max−min (≥ 2) — **diagnostic, non affiché** |
| `sensor.jardin_humidite_sol_points_frais` | Nombre de points frais (0..6) |
| `sensor.jardin_reservoir_sol_etat` | État qualitatif (`complet`/`degrade`/`insuffisant`/`indisponible`) |
| `binary_sensor.arrosage_besoin_sol` | Besoin sol (médiane < seuil + hystérésis) ; attribut `motif` |

> **Écarts de nommage à noter** (sans action) : l'état qualitatif runtime **n'émet
> pas** les libellés `heterogene` / `a_verifier` prévus au contrat 15 §6 (choix
> assumé du runtime : aucun seuil d'hétérogénéité robuste n'existe en v0). Le
> vocabulaire est donc fondé **uniquement sur le nombre de points frais**, pas sur
> la dispersion — ce qui contribue directement au manque d'observabilité (§6).

---

## 5. Analyse de la médiane

### 5.1 Justesse mathématique — ✅ correcte

`n = 6` (pair) ⇒ médiane = moyenne des 2 valeurs centrales de la série triée =
`(20,22 + 22,34) / 2 = 21,28`, arrondi à `21,3`. Le runtime applique exactement
`(vals[n//2 - 1] + vals[n//2]) / 2 | round(1)`. **Aucun défaut de calcul.**

### 5.2 Ce que la médiane masque ici

La médiane est un **estimateur de position centrale robuste** : elle **ignore
délibérément** l'amplitude des extrêmes. Avec la distribution actuelle
(4 sondes « basses » 16,85–22,34 · 2 sondes « hautes » 47,66 / 73,32), la valeur
centrale tombe **au cœur de l'amas sec**. Conséquences :

- elle **ne reflète pas** que 2 points ont fortement réagi à l'arrosage ;
- elle **ne bouge quasiment pas** tant que l'arrosage ne mouille pas ≥ 3 sondes
  (il faut basculer la **majorité** pour déplacer la médiane) ;
- elle **écrase la bimodalité** : rien dans la seule valeur `21,3` ne dit qu'il
  existe deux populations très différentes.

### 5.3 Adaptée à un jardin très hétérogène ?

**Pour la décision : oui, par conception.** C'est précisément le rôle de la
médiane de ne pas se laisser tirer par 1–2 sondes atypiques (contrat 15 §2 :
« plus robuste qu'une moyenne simple ; ne masque pas autant les extrêmes »).
**Pour la lecture humaine / diagnostic : non, seule.** Une médiane isolée est
**illisible** sur un terrain bimodal — d'où le besoin de l'accompagner **toujours**
du minimum, de l'hétérogénéité et de la qualité (ce que le contrat 15 §2 exige
déjà : « une lecture du réservoir, **toujours** accompagnée du point sec, de
l'hétérogénéité et de la qualité »).

### 5.4 Adaptée si seules 1 ou 2 sondes voient l'arrosage ?

**Non pour *visualiser* l'arrosage** — c'est le nœud du constat d'Antoine. Un
arrosage qui ne touche que 2/6 points **ne peut pas** déplacer une médiane sur 6.
Deux lectures possibles, **à départager par le terrain** (§7) :
- soit l'arrosage **ne couvre pas** physiquement les zones 4/5/6 (problème de
  couverture Rain Bird ou d'implantation des sondes) ;
- soit les zones 4/5/6 sont **réellement déficitaires** et la médiane basse est
  **le bon signal** (le jardin a globalement soif malgré 2 points détrempés).

### 5.5 Trop conservatrice pour voir un arrosage récent ?

**Pour l'affichage : oui.** L'observation du 2026-07-05 (plan v0 §3 bis) l'illustre
déjà : sur un arrosage réel de 35 min, la **médiane n'a monté que de +4,5 pts**
(26,1 → 30,6), avec percolation lente. La médiane est **structurellement inerte** —
utile pour décider, **pauvre pour rendre visible** l'effet immédiat d'un apport.

### 5.6 Conserver la médiane comme indicateur de décision robuste ?

**Oui.** Vérification sur les données fournies :

| Indicateur candidat | Valeur | vs seuil 30 % | Verdict besoin |
|---|---|---|---|
| **Médiane** | 21,3 % | **< 30** | `on` (arrose) ✅ protecteur |
| Moyenne | 32,9 % | > 30 | `off` (n'arrose pas) ❌ masque le besoin |
| Minimum | 16,85 % | < 30 | `on` mais sur-réactif (1 sonde) ❌ |
| Maximum | 73,32 % | > 30 | `off` sur 1 sonde détrempée ❌ |

La médiane est **le seul des quatre** à déclencher l'arrosage quand la **majorité**
du jardin est sèche, **sans** se laisser piéger par les 2 sondes humides. C'est
l'argument central pour **la conserver comme entrée de décision** et **la
compléter** — pas la remplacer.

### 5.7 Quatre lectures à distinguer

| Axe | Verdict |
|---|---|
| **Justesse mathématique** | ✅ correcte |
| **Représentativité agronomique** | ⚠️ discutable sur terrain bimodal — dépend de la couverture réelle (§7) |
| **Utilité décisionnelle** | ✅ bonne (robuste, protectrice) |
| **Lisibilité utilisateur** | ❌ insuffisante seule — d'où le constat |

---

## 6. Analyse de dispersion

```text
min = 16.85 · max = 73.32
étendue (hétérogénéité) = 56.47   → très forte
groupe sec        : zones 5 (16.85), 6 (17.18), 4 (20.22)
groupe intermédiaire : zone 2 (22.34)
groupe humide     : zones 1 (47.66), 3 (73.32)
```

- **Étendue de 56,5 points** sur une échelle 0–100 : dispersion **majeure**. Le
  `sensor.jardin_humidite_sol_heterogeneite` **vaut déjà 56,5** en backend — mais
  **n'est visible nulle part**.
- **Distribution bimodale** : 4 points groupés bas (16–22), 2 points hauts
  (48, 73), rien entre 22 et 48. La médiane à 21,3 **siège dans le cluster bas**.
- **Nombre de sondes < seuil 30 %** : **4 sur 6** (zones 2, 4, 5, 6). Indicateur
  **inexistant** aujourd'hui, très parlant : « 4 points sur 6 sous le seuil ».
- **Écart médiane↔max = 52** (immense) ; **écart médiane↔min = 4,45** (faible) →
  signe que la médiane est **collée au bas** de la distribution.

**Une telle dispersion rend-elle nécessaire un indicateur de cohérence ?** —
**Oui, en observabilité/diagnostic** (pas en pilotage). Sans indicateur de
dispersion **affiché**, l'utilisateur voit une médiane basse et stable et conclut
à tort « l'arrosage n'a rien fait », alors que 2 points ont bondi. Les briques
existent déjà (hétérogénéité, minimum) : **le manque est leur exposition**, plus
un éventuel « nombre de sondes sous seuil » et un « delta avant/après ».

> **Rappel doctrinal.** Le contrat 15 §4/§11 et le 14 §5 **interdisent tout seuil
> d'hétérogénéité chiffré opposable** en v0. Un indicateur de dispersion reste donc
> **diagnostic** ; il ne doit **pas** devenir un critère de blocage/déclenchement
> sans validation. Les bornes `faible/modérée/forte` restent **exploratoires**.

---

## 7. Hypothèses terrain (implantation des sondes)

> **Hypothèses, pas certitudes.** À départager par observation (§11). Aucune ne
> justifie une correction ou une calibration à ce stade (contrats 12 §9, 14 §5/§6).

### 7.1 Grille d'analyse d'implantation (à remplir au terrain)

Pour **chaque** point 1..6 : proximité d'un arroseur · zone directement aspergée ?
· ombre / plein soleil · sol compact / meuble / drainant · profondeur d'insertion
· qualité du contact sonde-sol · pente / ruissellement · bordure / massif /
pelouse · proximité mur / haie / arbre / gouttière / stagnation · capteur trop
exposé ou trop isolé · zone réellement arrosée vs zone représentative du besoin.

### 7.2 Classification actuelle (hypothèses)

| Sonde | Valeur | Hypothèse (à confirmer) |
|---|---|---|
| Zone 3 | 73,32 | Très humide — proche d'un point d'apport, creux, ombre, ou sol peu drainant / stagnation. |
| Zone 1 | 47,66 | Humide — capte probablement bien l'arrosage. |
| Zone 2 | 22,34 | Intermédiaire — cf. « Point 2 » historiquement moins réactif (contrat 14 §6 : +21,43 au test tuyau vs +36,8 / +37,6) ; zone plus drainante ou placement différent **possible**, **non tranché**. |
| Zone 4 | 20,22 | Sèche — capte peu l'arrosage **ou** zone réellement déficitaire. |
| Zone 5 | 16,85 | La plus sèche — idem ; vérifier aspersion et contact sonde-sol. |
| Zone 6 | 17,18 | Sèche — idem. |

### 7.3 Question ouverte structurante

Les zones 4/5/6 sont-elles **hors de portée de l'arrosage** (couverture Rain Bird
inégale / sondes mal placées) **ou** dans une **partie réellement plus sèche** du
jardin ? Les deux ont la **même signature** (valeur basse) mais des **implications
opposées** : la première appelle un repositionnement, la seconde valide la médiane
basse comme signal correct. **Indiscernable sans observer un cycle complet**
(arrosage → cinétique par point). Rappel : **une seule zone Rain Bird, 6 points de
mesure** — il n'y a pas de pilotage par sonde possible ni prévu (contrat 12 §2).

---

## 8. Risques architecturaux

| # | Risque | Gravité | Commentaire |
|---|---|---|---|
| R1 | **Piloter/bloquer l'arrosage sur une sonde extrême** (min ou max) | Élevé | Violerait contrat 15 §3 (« minimum seul ne déclenche aucun arrosage ») et 12 §12. Le min à 16,85 ne doit **pas** forcer un arrosage ; le max à 73 ne doit **pas** l'inhiber. |
| R2 | **Introduire un seuil d'hétérogénéité chiffré opposable** | Élevé | Interdit v0 (contrats 14 §5, 15 §4/§11). Tout seuil = **hypothèse d'audit**, jamais implémentation. |
| R3 | **Basculer la décision de la médiane vers la moyenne** pour « voir » l'arrosage | Élevé | Régression : la moyenne (32,9) masquerait le besoin ici. Contrat 15 §12 l'interdit explicitement. |
| R4 | **Historiser les 6 bruts** sans gouvernance | Moyen | Contredit la doctrine « bruts hors recorder » (contrat 12 §13) ; coût cardinalité recorder. À arbitrer (fenêtre temporaire d'observation ?). |
| R5 | **Renommer la batterie 4/5/6** pour « uniformiser » | Moyen | Casserait `group.batteries` / customize ; doctrine README = verbatim. **Ne pas faire.** |
| R6 | **Confondre observabilité et décision** | Moyen | Ajouter des indicateurs de diagnostic ne doit **pas** les brancher dans la chaîne besoin→intention sans contrat. |
| R7 | **Fabriquer un « sol humide » par défaut** si sondes muettes | Élevé | Garde anti-faux-négatif (contrats 04 §4, 17 §4 inv.6) : médiane indisponible ⇒ besoin `off` (abstention), jamais optimisme. À préserver. |

---

## 9. Recommandations d'observabilité (sans code)

Chaque indicateur : **objectif · intérêt · risque · domaine · priorité · statut**.
Domaine ∈ {décision, diagnostic, UI, historique}. Priorité P0/P1/P2.
Statut ∈ {à étudier, à valider terrain, à exclure du pilotage auto pour l'instant}.

| Indicateur | Objectif | Intérêt | Risque | Domaine | Priorité | Statut |
|---|---|---|---|---|---|---|
| **Afficher le minimum** (`_minimum`, existe) | Rendre visible le point le plus sec | Élevé — déjà calculé + historisé, coût quasi nul | Faible (lecture seule) | UI/diagnostic | **P0** | à étudier (UI) |
| **Afficher l'hétérogénéité** (`_heterogeneite`, existe) | Rendre visible la dispersion (56,5 !) | Élevé — révèle la bimodalité masquée | Faible | UI/diagnostic | **P0** | à étudier (UI) |
| **Médiane + min + max sur le même graphe** (bande) | Voir la médiane *dans* son enveloppe | Élevé — l'arrosage de 2 sondes devient visible via le max | Faible | UI | **P0** | à étudier |
| **Nombre de sondes < seuil** | « 4/6 sous le seuil » — lecture instantanée | Moyen-élevé | Moyen — ne pas en faire un déclencheur (R1) | diagnostic | **P1** | à valider terrain / exclure du pilotage auto |
| **Delta médiane avant/après arrosage** | Quantifier l'effet d'un cycle | Élevé — répond directement au constat | Moyen — définition « avant » à cadrer | diagnostic/historique | **P1** | à valider terrain |
| **Delta par sonde avant/après** | Voir *quelles* sondes ont réagi | Élevé — départage couverture vs déficit (§7.3) | Moyen — nécessite historiser les bruts (R4) | diagnostic/historique | **P1** | à valider terrain |
| **Exposer les 6 sondes individuellement** (UI et/ou historique) | Voir la distribution réelle | Élevé — cœur du diagnostic terrain | Moyen — cardinalité recorder (R4) ; fenêtre temporaire possible | UI/historique | **P1** | à étudier (arbitrage recorder) |
| **Diagnostic « distribution hétérogène »** (libellé `heterogene`/`a_verifier` du contrat 15 §6) | Nommer la bimodalité | Moyen | Élevé — exige un seuil (R2) ⇒ exploratoire | diagnostic | **P2** | à étudier (après observation) |
| **Diagnostic « sonde possiblement mal placée »** | Signaler une sonde durablement divergente | Moyen | Élevé — critère robuste requis (contrat 14 §5) | diagnostic | **P2** | à valider terrain / exclure pilotage |
| **Diagnostic « zone possiblement non couverte par arrosage »** | Signaler un point qui ne réagit jamais | Moyen | Élevé — nécessite corrélation arrosage↔réponse | diagnostic | **P2** | à valider terrain |
| **Détection « arrosage visible par ≥ N sondes »** | Confirmer qu'un cycle a « pris » | Moyen | Moyen — N arbitraire (hypothèse) | diagnostic | **P2** | à étudier |

> **Priorité de fond.** Les **P0** sont à **coût quasi nul** (les grandeurs
> existent déjà en backend et au recorder) : il ne « manque » que leur **mise en
> vue**. Ils répondent à ~80 % du constat sans toucher à la décision.

---

## 10. Recommandation sur l'algorithme de décision (avis prudent)

1. **Conserver la médiane** comme mesure représentative du réservoir sol et
   **entrée de décision** (contrats 15 §2, 17 §2). Elle est robuste, protectrice,
   et se comporte correctement sur le cas fourni (déclenche à bon escient).
2. **Ne pas piloter sur la moyenne.** Sur ce jeu de données, la moyenne (32,9 %)
   **masquerait** le besoin. La moyenne reste **proscrite** (contrat 15 §12).
3. **Ne pas déclencher ni bloquer sur une sonde extrême.** Min et max restent des
   **signaux de diagnostic**, jamais des déclencheurs (contrat 15 §3, R1).
4. **Distinguer nettement décision et diagnostic de distribution.** La décision
   reste sur `médiane + seuil + hystérésis + garde anti-faux-négatif` ; la
   dispersion enrichit la **lecture**, sans entrer dans la chaîne besoin→intention
   sans contrat dédié.
5. **Attendre une période d'observation** après tout repositionnement éventuel des
   sondes **avant** de recalibrer quoi que ce soit (contrats 12 §9, 14 §6 ; plan
   v0 §4). Un cycle complet arrosage→cinétique par point est nécessaire pour
   trancher couverture vs déficit (§7.3).
6. **Aucun nouveau pilotage automatique** sans validation architecturale (contrat
   15 §9, 17 §7).

**Synthèse** : le sujet est **P0 d'observabilité**, **pas** une refonte
d'algorithme. Conserver la médiane, l'entourer d'indicateurs de dispersion déjà
disponibles, observer, puis seulement arbitrer d'éventuels indicateurs P1/P2.

---

## 11. Points nécessitant observation terrain

- [ ] Suivre un **cycle complet** arrosage → réponse **par sonde** (pas seulement
      la médiane) : quelles sondes montent, de combien, en combien de temps.
- [ ] Départager pour zones 4/5/6 : **hors couverture arrosage** vs **zone
      réellement plus sèche** (§7.3).
- [ ] Caractériser le **Point 2 / zone 2** (moins réactive : zone vs défaut —
      contrat 14 §6, plan v0 §2.2) sur plusieurs apports.
- [ ] Observer la **cinétique de séchage** par point et par régime météo (le pic
      d'humidité post-arrosage arrive **≥ 1 h** après la fin de l'eau, plan v0
      §3 bis).
- [ ] Confirmer les **fenêtres de fraîcheur** réelles (paramètre 6 h provisoire du
      runtime, contrat 14).
- [ ] Vérifier **contact sonde-sol / profondeur** des sondes basses avant toute
      conclusion « déficit ».

---

## 12. Liste stricte des fichiers lus

> Lecture seule — aucun de ces fichiers n'a été modifié.

1. `12_template_sensors/arrosage/reservoir_sol.yaml`
2. `12_template_sensors/arrosage/besoin_sol.yaml`
3. `03_input_numbers/arrosage/decision_v1.yaml`
4. `18_lovelace/dashboards/arrosage/principal.yaml`
5. `18_lovelace/dashboards/arrosage/diagnostic.yaml`
6. `recorder.yaml` (extrait — bloc humidité sol)
7. `00_documentation_arsenal/contrats/arrosage/12_capteurs_humidite_sol.md`
8. `00_documentation_arsenal/contrats/arrosage/14_qualite_donnees_sol.md`
9. `00_documentation_arsenal/contrats/arrosage/15_canal_reservoir_sol.md`
10. `00_documentation_arsenal/contrats/arrosage/17_decision_v1.md`
11. `00_documentation_arsenal/audits/02_conception/arrosage/plan_observation_hydrique_v0.md`
12. `00_documentation_arsenal/audits/index.md`

Fichiers **repérés** dans la cartographie mais **non ouverts en détail** (cités
d'après grep/index, hors périmètre de lecture approfondie) : contrats arrosage
04/05/06/13/16, `intention.yaml`, `reglages.yaml`, `02_groups/batteries.yaml`,
`01_customize/batteries.yaml`, `confrontation_avis_besoin_hydrique.md`.

---

## 13. Confirmation — aucun fichier runtime modifié

**Confirmé.** Cet audit est **strictement lecture seule**. Aucune modification n'a
été apportée à un fichier **runtime, YAML, Lovelace, helper, template sensor,
script, automation, recorder ou customize**. **Aucun `entity_id` inventé**, **aucun
renommage / accentuation / normalisation** d'entité existante. **Aucun seuil
runtime créé.** Le seul fichier **créé** est **ce rapport documentaire** :
`00_documentation_arsenal/audits/01_rapports/arrosage/audit_humidite_sol_mediane_dispersion.md`.

> **Suite documentaire suggérée (non faite, à arbitrer)** : ajouter une ligne de
> renvoi vers ce rapport dans [`audits/index.md`](../../index.md) (section
> « Rapports → Arrosage ») — modification d'un fichier existant, laissée à la
> décision d'Antoine pour respecter la consigne « ne modifier aucun fichier ».

---

## Renvois

- Canal réservoir sol (grandeurs d'observation) : [`15_canal_reservoir_sol.md`](../../../contrats/arrosage/15_canal_reservoir_sol.md)
- Qualité des données sol : [`14_qualite_donnees_sol.md`](../../../contrats/arrosage/14_qualite_donnees_sol.md)
- Capteurs humidité sol (relevé, divergence batterie, Point 2) : [`12_capteurs_humidite_sol.md`](../../../contrats/arrosage/12_capteurs_humidite_sol.md)
- Décision V1 (médiane consommée) : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Plan d'observation hydrique v0 : [`plan_observation_hydrique_v0.md`](../../02_conception/arrosage/plan_observation_hydrique_v0.md)
- Index des audits : [`index.md`](../../index.md)
