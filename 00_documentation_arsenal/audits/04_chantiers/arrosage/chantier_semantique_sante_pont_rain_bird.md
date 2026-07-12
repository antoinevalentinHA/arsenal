# Chantier C18 — Rain Bird : sémantique de santé du pont (qualité radio ≠ santé opérationnelle)

| Champ | Valeur |
|---|---|
| **Chantier** | **C18** — Rain Bird : sémantique de santé du pont |
| **Domaine** | Arrosage — pont `rainbird-esp32` (diagnostic / synthèse de santé) |
| **Statut** | **Actif — Lot 3 (runtime + guard) livré ; validation terrain + clôture (Lot 4) en attente.** Lot 1 (contrat, 03 §6 / 17 §2-§3) + Lot 2 (arbitré, absorbé) + Lot 3 (`pont_sante.yaml` conforme 03 §6.2 — RSSI retiré de l'état ; guard anti-régression C18 + selftest dans le checker résilience) livrés. Écart contrat↔runtime **résorbé**. Restent D-C18-C / D-C18-D ouvertes. |
| **Priorité** | **P3** — aucun incident fonctionnel ; `pont_sante` ne gate rien (impact strictement diagnostic/UI). Non urgent, mais décision requise. |
| **Rapport source (mergé)** | [`audit_rain_bird_sante_pont_qualite_radio.md`](../../01_rapports/arrosage/audit_rain_bird_sante_pont_qualite_radio.md) (PR #342, mergée) |
| **Registre** | [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (ligne C18, co-commit) |

> **Nature de ce document.** Ouverture **formelle** et **gouvernance** du chantier :
> il qualifie les décisions, fixe le périmètre, les invariants, les critères
> d'acceptation et le découpage en lots. Il **ne modifie aucun runtime, contrat,
> checker, UI ou entité** et **ne fige aucune correction**. Chaque lot fera l'objet
> d'un travail dédié, dans son propre périmètre, avec point d'arrêt.

---

## 1. Objet

Résorber la **sur-sévérité** du verdict `sensor.rain_bird_pont_sante`, qui affiche
`degrade` en permanence dès qu'un RSSI est **≤ -75 dBm**, alors que le pont est
**pleinement exploitable** (préconditions `on`, données fraîches, aucun incident).

La cause exacte, établie par l'audit mergé, est un **franchissement de frontière
sémantique** : un seuil de la couche **qualité radio** (-75) est importé dans le
verdict de **santé opérationnelle**, notion que le contrat central
([`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6)
fonde sur la **disponibilité, le lien, l'ACK et la fraîcheur du poll** — **pas** sur
la finesse du signal radio.

Le chantier vise à **restaurer/renforcer la séparation des trois couches** (§4),
**par une décision contractuelle d'abord**, puis une correction runtime minimale.

---

## 2. Distinction fondatrice — qualité radio / exploitabilité runtime / santé

Le dépôt distingue **déjà** trois notions, portées par trois entités. Le chantier
**s'interdit de les confondre** ; c'est l'invariant structurant.

| Couche | Entité(s) | Autorité / seuil | Rôle |
|---|---|---|---|
| **Qualité radio** | `sensor.rain_bird_pont_qualite_wifi`, `…_qualite_ble`, `…_pont_diagnostic_resume` | bon ≥ -67 / acceptable -74..-68 / **faible ≤ -75** | **Information** graduée, neutre — décrit la finesse du lien, sans conséquence opérationnelle propre. |
| **Exploitabilité runtime** | `binary_sensor.arrosage_rain_bird_preconditions_runtime` | radio **exploitable ≥ -90 dBm** + batterie connue (contrat [`10`](../../../contrats/arrosage/10_prerequis_runtime.md)) | **Autorisation** binaire lue par le Run supervisé : « le pont est-il radio-exploitable pour exécuter/observer ? ». |
| **Santé opérationnelle** | `sensor.rain_bird_pont_sante` | (à clarifier — cf. Lot 1) | **Verdict synthétique** de l'état opérationnel réel (disponibilité + fraîcheur, contrat [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6). |

> **Position du chantier.** La séparation existe par construction ; l'anomalie est
> que `pont_sante` **la franchit** en important le seuil qualité -75. La cible
> **préserve ou renforce** cette séparation — elle ne la brouille pas davantage.
> C'est pourquoi un **simple remplacement `-75 → -90`** (qui replierait
> l'exploitabilité dans la santé) **n'est PAS retenu par défaut** : il exige une
> **décision contractuelle explicite** (Lot 1, §6).

---

## 3. Décisions actées (par l'audit mergé + arbitrages opérateur)

1. **Diagnostic confirmé** : confusion **qualité radio ↔ santé opérationnelle** ; le
   seuil -75 appartient à la couche qualité.
2. **L'UI n'est pas en cause** : elle rend fidèlement le verdict backend (aucun lot UI).
3. **`pont_sante` ne gate rien** : la décision V1 (`arrosage_intention` →
   `declenchement`) s'appuie sur `preconditions_runtime` + `pont_donnees_disponibles` ;
   les notifications sur disponibilité/batterie. → Une correction de `pont_sante` a un
   impact **strictement diagnostic/UI + historisation**, **aucune régression arrosage
   possible**.
4. **Méthode : contrat avant runtime.** Toute correction runtime est **subordonnée** à
   une clarification contractuelle préalable (03 §6, réconciliation 17).
5. **Séparation des trois couches préservée/renforcée** (§2) — invariant structurant.
6. **Pas de remplacement `-75 → -90` figé** sans décision contractuelle explicite (§6).
7. **Topologie / obsolescence 08-10 = point connexe, non absorbé** dans le correctif
   principal (§7).

---

## 4. Invariants métier (opposables)

- **INV-C18-1 — Santé = capacité opérationnelle.** Le verdict `pont_sante` qualifie
  l'**état opérationnel** (disponibilité + fraîcheur + exploitabilité radio au sens du
  plancher -90), **jamais** la finesse de qualité radio (-67/-74/-75), qui reste portée
  par la couche qualité.
- **INV-C18-2 — Signaux opérationnels préservés.** `pont_sante` **reste** `indisponible`
  quand les données cœur sont indisponibles, et **`degrade`** en cas de **perte de
  fraîcheur** (`pont_donnees_fraiches = off`). Aucune correction ne doit produire un
  **faux nominal** (radio absente / positive / unknown ⇒ jamais `ok`).
- **INV-C18-3 — Non-gating préservé.** `pont_sante` demeure **diagnostic/UI**, sans
  couplage à une décision, une garde de sûreté ou une exécution — **sauf** décision
  contractuelle explicite le requalifiant (auquel cas la réconciliation 17 le formalise).
- **INV-C18-4 — Séparation des trois couches** (§2) préservée ou renforcée, jamais
  brouillée.
- **INV-C18-5 — Contrat avant runtime.** Aucun runtime `pont_sante` n'est modifié avant
  qu'un contrat n'ait tranché la sémantique retenue.
- **INV-C18-6 — Discipline Arsenal.** Aucun `entity_id`/id/alias inventé ; aucun
  renommage ; un seul writer autoritaire par sortie ; aucun fallback silencieux ; pas de
  correction opportuniste hors périmètre.

---

## 5. Décisions encore ouvertes (à arbitrer)

- **D-C18-A — Option de correction sémantique.** Choisir parmi les options de l'audit
  (§16 du rapport) :
  - **A** — santé = **disponibilité + fraîcheur** seulement (radio hors santé) ;
  - **B** — santé dégrade **sous exploitabilité (-90)** (aligne le gate sur les
    préconditions) — *replie partiellement deux couches* ;
  - **C** — **requalifier les niveaux** : `ok` (stable+frais+exploitable) / `degrade`
    (anomalie réelle **non bloquante** : fraîcheur limite, batterie faible, échecs
    récents) / `indisponible` (précondition non satisfaite) — radio moyenne stable
    **> plancher** reste neutre.
  > **✅ Tranché au Lot 1 — option A** : la **valeur RSSI est retirée** du calcul de
    santé (santé = disponibilité + fraîcheur). B (aligner -90) et C (enrichir `degrade`)
    écartées à ce stade. Justification et sémantique normative :
    [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md)
    §6.2 (D-C18-A).
- **D-C18-B — Réconciliation contrat 17.** Le contrat
  [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 **listait**
  `sensor.rain_bird_pont_sante` comme **entrée de décision**, alors que le runtime
  `intention.yaml` **ne le lit pas** (gate réel = `preconditions_runtime` +
  `pont_donnees_disponibles`).
  > **✅ Réconcilié au Lot 1** : `pont_sante` requalifié **diagnostic, non décisionnel**
    (aligné sur le runtime sûr) ; entrée de décision = **préconditions + disponibilité**.
    Cf. [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §2/§3 et
    [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6.4 (D-C18-B).
- **D-C18-C — Sens positif de `degrade` (option C).** Si l'option C est retenue :
  faut-il **enrichir** `degrade` d'un critère **batterie faible** et/ou **échecs
  récents**, pour lui donner une valeur de signal ? (arbitrage de fond, à cadrer si C).
- **D-C18-D — Topologie / documents 08-10** (§7) : simple **mention de contexte** vs
  **mise à jour** de l'inventaire — arbitrage **distinct** du correctif principal.

---

## 6. Périmètre & lots (nécessité démontrée, ordre imposé)

> **Règle :** ne pas présumer que tous les lots sont nécessaires ; chaque lot est
> justifié ci-dessous. Chaque lot : **branche + PR dédiées**, part d'un `main` propre,
> périmètre strict, contrôles adaptés, **point d'arrêt** avant le suivant.

| Lot | Objet | Nécessité | Dépend de |
|---|---|---|---|
| **Lot 1 — Contrat / clarification normative** | Trancher la sémantique de santé dans [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6 (santé = disponibilité + fraîcheur ; qualité -75 informative ; exploitabilité -90 = autorisation séparée) **et** réconcilier [`17`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 (statut réel de `pont_sante`). Acte D-C18-A et D-C18-B. | **✅ Livré (Lot 1)** — 03 §6.1–§6.4 + 17 §2/§3 amendés ; écart runtime tracé. | — |
| **Lot 2 — Checker CI** | Garde de non-régression sémantique : interdire la réintroduction d'un critère radio non contractuel dans `pont_sante`. | **Décidé (voir §10) : pas de lot autonome.** Guard **replié** dans `check_resilience_integrations_contracts.py`, **co-livré avec le Lot 3** (aucun nouveau workflow/registre ; séquencement respecté). | Lot 1 |
| **Lot 3 — Correction backend minimale + guard** | Modifier [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml) conformément à l'option A (03 §6.2/§6.3) : retirer le gate radio ≤ -75, en **conservant** les gates disponibilité/fraîcheur (INV-C18-2) ; **+ guard anti-régression** (extension du checker résilience) **+ tests**. Une **PR unique verte**. | **✅ Livré (Lot 3)** — état `pont_sante` = disponibilité + fraîcheur (RSSI hors état, attributs préservés) ; guard `C18-pont-sante` + selftest dans `check_resilience_integrations_contracts.py` (étape CI `--selftest`) ; **table de vérité 4 états validée**. **Validation terrain en attente** (Lot 4). | Lot 1 |
| **Lot 4 — Validation sur états réels + clôture** | Vérifier le verdict sur états réels (nominal, perte de fraîcheur, indisponibilité) ; clôturer C18 (registre + trace). | **Nécessaire**. | Lot 3 |

**Lots explicitement NON nécessaires (démontré) :**
- **Diagnostic** — la couche qualité (`pont_qualite_*`, `pont_diagnostic_resume`) est
  **déjà correcte** : aucun lot.
- **UI** — le rendu est **déjà fidèle** (décision actée §3.2) : aucun lot.

**Lot connexe, hors correctif principal (§7) :** mise à jour éventuelle de l'inventaire
08/10 sur la topologie actuelle — **arbitrage distinct** (D-C18-D), **non séquencé** dans
la chaîne 1→4, à décider séparément.

---

## 7. Point connexe — topologie matérielle actuelle & documents 08/10

L'audit a établi (précisions opérateur) une **évolution de topologie** :

- **Antérieure** — décrite **correctement à l'époque** par
  [`08`](../../../contrats/arrosage/08_inventaire_pont_runtime.md) §2 et
  [`10`](../../../contrats/arrosage/10_prerequis_runtime.md) P6/P7 : contrôleur **en
  fosse sous plaque d'acier**, pont ESP32 **dans la petite maison**.
- **Actuelle** — contrôleur **en surface** ; pont ESP32 **au jardin, dans un meuble
  béton**.

**Traitement retenu :**
- les documents 08/10 **ne sont pas erronés** ; ils décrivent la topologie
  **antérieure** et **ne reflètent plus complètement** l'installation actuelle
  (**obsolescence partielle**) ;
- ce constat est **un point connexe**, **explicitement distinct** du correctif
  sémantique : il **n'est pas absorbé** dans les lots 1→4 et **ne conditionne pas** le
  diagnostic (qui tient sur la configuration actuelle : signal stable ~-76 dBm,
  au-dessus du plancher -90) ;
- sa mise à jour éventuelle (D-C18-D) relève d'un **arbitrage propre**, à décider par
  l'opérateur — le chantier le **trace** sans le trancher ni l'imposer.

---

## 8. Critères d'acceptation (chantier)

1. `sensor.rain_bird_pont_sante` **n'est plus `degrade` du seul fait** d'une qualité
   radio moyenne **stable et supérieure au plancher d'exploitabilité (-90 dBm)**.
2. Le verdict **reste `degrade`** sur **perte de fraîcheur** et **`indisponible`** sur
   **données cœur indisponibles** (INV-C18-2).
3. La **séparation des trois couches** (§2) est **préservée ou renforcée** ; aucune
   couche informative n'est repliée dans la santé sans décision contractuelle.
4. La sémantique retenue est **portée par un contrat** (03/17 alignés) **avant** tout
   runtime (INV-C18-5).
5. **Aucune régression** sur gardes, décisions, exécutions et notifications d'arrosage
   (inchangées par construction — `pont_sante` ne les alimente pas).
6. Checkers documentaires et de domaine **verts** (dont la **garde anti-régression**
   anti-RSSI, co-livrée au **Lot 3** — cf. §10).

---

## 9. Gouvernance & points d'arrêt

- Chaque lot : **branche + PR dédiées**, depuis un `main` propre et à jour, périmètre
  strict, contrôles adaptés, **point d'arrêt** avant le lot suivant.
- **Aucun runtime** n'est modifié avant le **merge du Lot 1** (contrat).
- Tout changement d'état du chantier met à jour le **registre dans le même commit**
  (co-commit obligatoire).
- Ce document est la **source faisant foi** du chantier C18 ; il est **indexé** dans
  [`index.md`](../../index.md) (même commit).

---

## 10. Évaluation du Lot 2 (checker CI) — décision

Évaluation menée après merge du Lot 1 (contrat autorité). **Invariant à protéger** :
`sensor.rain_bird_pont_sante` ne dépend d'**aucune valeur RSSI** ; santé = **disponibilité
+ fraîcheur** ; les seuils qualité (-75) et exploitabilité (-90) restent dans leurs couches
([`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6.1–§6.2).

| # | Question | Constat |
|---|---|---|
| 1 | **Risque réel de régression** | **Faible sévérité** (`pont_sante` **non-gating** → une régression n'a **aucun** effet fonctionnel, seulement une tuile mal colorée) mais **récurrence plausible** : la confusion **a déjà eu lieu** (le -75 vient d'un copier du seuil qualité). Tentation documentée, non hypothétique. |
| 2 | **Couverture par les checkers existants** | **Non couvert.** Aucun checker n'inspecte la composition de `pont_sante`. Le **seul** checker touchant le pont — `check_resilience_integrations_contracts.py` — possède déjà des invariants **03 §6** (R6 garde `pont_donnees_fraiches` du script `rain_delay`, R14 doctrine `last_reported` sur `pont_donnees_fraiches.yaml`) et **parse déjà** les fichiers `12_template_sensors/arrosage/` — mais **ne contrôle pas** l'absence de RSSI dans `pont_sante`. |
| 3 | **Contrôle statique : robuste ou trop couplé ?** | **Robuste si ciblé sur le bloc `state:`** (l'invariant = le `state` ne référence ni `_rssi` ni le seuil -75). Un grep naïf du fichier **faux-positiverait** : `pont_sante` **expose légitimement** `wifi_rssi`/`ble_rssi` en **attributs** d'affichage. Le contrôle doit donc distinguer `state` / `attributes` → **parsing YAML structuré**, exactement ce que fait déjà le checker résilience (HALoader). Bas couplage à l'implémentation (n'impose pas *comment* calculer, seulement de *ne pas lire* le RSSI en état). |
| 4 | **Coût de maintenance proportionné ?** | **Checker dédié = disproportionné** : gouvernance C14 (script **+ nouveau workflow** `.github/workflows/contracts_*.yml` + selftest + non-orphelin `check_ci_coverage_registry`) pour **un seul capteur non-gating**. **Extension du checker résilience existant = coût marginal faible** (une règle dans un checker déjà câblé, déjà propriétaire des invariants 03 §6 arrosage — aucun nouveau workflow/registre). |
| 5 | **Les tests du Lot 3 suffisent-ils ?** | Les tests du Lot 3 sont **ponctuels** : ils valident la correction à l'instant T, **sans empêcher** une ré-introduction future. Seul un **guard permanent** prévient la dérive (doctrine C14 : « rejeté par la machine, pas par un relecteur »). |

> **Contrainte de séquencement décisive.** Un guard « `pont_sante.state` sans RSSI » serait
> **rouge** contre le runtime **actuel** (qui dégrade encore sur -75 — écart tracé,
> [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6). Il **ne peut donc pas**
> constituer une **PR autonome verte avant** le Lot 3.

### Décision (Lot 2)

> **Pas de checker CI dédié (PR autonome) — mais un guard permanent, au bon endroit et au
> bon moment.**
>
> - **Écarté** : ouvrir un **checker dédié** en PR autonome (disproportionné pour un capteur
>   non-gating ; et impossible à rendre vert avant le Lot 3).
> - **Retenu** : **replier un guard minimal anti-RSSI dans le checker existant**
>   `check_resilience_integrations_contracts.py` (déjà propriétaire des invariants 03 §6
>   arrosage, déjà câblé en CI via `contracts_resilience_integrations.yml`), **co-livré avec
>   le Lot 3** (même PR : correction runtime **+** guard → CI verte, guard aligné sur le
>   runtime corrigé). Règle : le **bloc `state:`** de `pont_sante.yaml` ne référence ni
>   `bridge_wifi_rssi`/`ble_rssi` ni le seuil `-75`, et référence bien
>   `pont_donnees_disponibles` + `pont_donnees_fraiches`.
>
> Cette voie **n'ajoute aucun artefact de gouvernance** (pas de nouveau workflow/registre),
> donne une **protection anti-régression permanente** (C14), et respecte le **séquencement**
> (le guard n'existe qu'avec le runtime conforme). Le Lot 2 **ne produit donc pas de PR
> séparée** : il est **absorbé dans le Lot 3** comme composant « garde CI » de ce dernier.

**Conséquence sur le découpage :** le Lot 2 « checker » **cesse d'être un lot autonome** ; le
Lot 3 devient **« correction runtime `pont_sante.yaml` + guard anti-régression (extension du
checker résilience) + tests »**, en une PR unique verte.

---

## Renvois

- Rapport d'audit source (mergé) : [`audit_rain_bird_sante_pont_qualite_radio.md`](../../01_rapports/arrosage/audit_rain_bird_sante_pont_qualite_radio.md)
- Autorité « santé du pont » : [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6
- Plancher d'exploitabilité -90 : [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
- Décision V1 (entrée `pont_sante` à réconcilier) : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Inventaire du pont (topologie antérieure) : [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md)
- Producteur du verdict : [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml)
- Cockpit de pilotage : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Index des audits : [`index.md`](../../index.md)
