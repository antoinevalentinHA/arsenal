# Chantier C18 — Rain Bird : sémantique de santé du pont (qualité radio ≠ santé opérationnelle)

| Champ | Valeur |
|---|---|
| **Chantier** | **C18** — Rain Bird : sémantique de santé du pont |
| **Domaine** | Arrosage — pont `rainbird-esp32` (diagnostic / synthèse de santé) |
| **Statut** | **Ouvert — gouvernance.** Périmètre, invariants, critères et lots définis ; **aucun runtime livré**. Première étape = **décision contractuelle** (Lot 1). |
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
  > Préférence d'audit : **A ou C** (préservent la séparation) plutôt que **B**.
    **Non tranché** — décision opérateur au Lot 1.
- **D-C18-B — Réconciliation contrat 17.** Le contrat
  [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 **liste**
  `sensor.rain_bird_pont_sante` comme **entrée de décision**, alors que le runtime
  `intention.yaml` **ne le lit pas** (documenté « non bloquant »). Décision : **retirer
  pont_sante des entrées de décision** (aligner le contrat sur le runtime sûr) **ou**
  formaliser un couplage explicite (peu probable — irait contre INV-C18-3).
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
| **Lot 1 — Contrat / clarification normative** | Trancher la sémantique de santé dans [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6 (santé = disponibilité + fraîcheur + exploitabilité -90 ; qualité -75 informative) **et** réconcilier [`17`](../../../contrats/arrosage/17_decision_v1.md) §2/§3.6 (statut réel de `pont_sante`). Acte D-C18-A et D-C18-B. | **Nécessaire** (contrat avant runtime). | — |
| **Lot 2 — Checker CI** | Garde de non-régression sémantique : interdire la réintroduction d'un critère radio non contractuel dans `pont_sante` ; verrouiller la sémantique du Lot 1. | **Conditionnel** — selon la précision exigée par le Lot 1 (à décider à l'issue du Lot 1). | Lot 1 |
| **Lot 3 — Correction backend minimale** | Modifier [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml) conformément à l'option actée : retirer/replacer le gate radio ≤ -75, en **conservant** les gates disponibilité/fraîcheur (INV-C18-2). | **Nécessaire** (résout le symptôme). | Lot 1 |
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
6. Checkers documentaires et de domaine **verts** (dont, le cas échéant, la garde du
   Lot 2).

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

## Renvois

- Rapport d'audit source (mergé) : [`audit_rain_bird_sante_pont_qualite_radio.md`](../../01_rapports/arrosage/audit_rain_bird_sante_pont_qualite_radio.md)
- Autorité « santé du pont » : [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6
- Plancher d'exploitabilité -90 : [`10_prerequis_runtime.md`](../../../contrats/arrosage/10_prerequis_runtime.md)
- Décision V1 (entrée `pont_sante` à réconcilier) : [`17_decision_v1.md`](../../../contrats/arrosage/17_decision_v1.md)
- Inventaire du pont (topologie antérieure) : [`08_inventaire_pont_runtime.md`](../../../contrats/arrosage/08_inventaire_pont_runtime.md)
- Producteur du verdict : [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml)
- Cockpit de pilotage : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
- Index des audits : [`index.md`](../../index.md)
