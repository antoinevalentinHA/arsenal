# 🛡️ ARSENAL — RAPPORT D'AUDIT · Alarme — Exposition diagnostique vs contrats

## 📌 Métadonnées

- **Statut** : rapport d'audit — **lecture seule, opposable**
- **Domaine** : Sécurité / Alarme — observabilité diagnostique
- **Dépôt** : `antoinevalentinHA/arsenal`
- **Révision du dépôt auditée** : `ccb7ca2`
- **Posture** : audit **strictement documentaire**. Aucun runtime, dashboard, carte, contrat, checker ou notification modifié. Aucune remédiation codée.
- **Autorité normative** : les **contrats fonctionnels** Alarme (`contrats/alarme/`) — *le contrat précède l'implémentation*. La CI **n'est pas** une source d'exigence ; l'implémentation et la doctrine UI **ne créent aucune exigence** absente des contrats.
- **Rapport officiel connexe** (périmètre distinct — logique du domaine, chantiers CH-x, HEAD antérieur) : [`audit_alarme_rapport_officiel.md`](audit_alarme_rapport_officiel.md). Le présent rapport porte sur un **axe distinct** : la conformité de l'**exposition diagnostique** aux contrats.

---

## 🎯 1. Objet & périmètre

**Objet unique :** déterminer si les **états, raisons, autorisations, refus, abstentions, dégradations, indisponibilités et éléments de compréhension** exigés par les contrats Alarme sont (a) effectivement **produits par le runtime**, puis (b) **exposés de manière exploitable** sur le **canal contractuellement imposé** (projection UI, capteur/attribut, ou notification).

**Dans le périmètre :** la chaîne diagnostique de bout en bout — exigence contractuelle → production runtime → exposition → compréhension.

**Hors périmètre :** la justesse/sûreté des décisions (on audite l'**observabilité**, pas la décision), la conformité graphique générale, la performance, la CI (jamais source d'exigence). La doctrine UI Arsenal est mobilisée **uniquement** pour évaluer la restitution correcte d'une projection **déjà exigée** par un contrat — elle ne crée aucune exigence.

---

## 🔬 2. Méthode & chaîne de preuve

Pour chaque exigence diagnostique, la chaîne suivante est établie, chaque maillon étant attesté par une preuve citée :

```
P-C  Contrat normatif (exigence citée, verbatim)
      ↓
P-R  Production runtime (entité → définition ; valeurs ; attributs ; couverture)
      ↓
P-UI Exposition sur le canal exigé (projection UI | capteur/attribut | notification)
      ↓
P-COMP Compréhension (lisibilité, distinction des états, indisponibilité)
```

**Règle d'or :** aucune non-conformité sans base contractuelle démontrable. Le maillon rompu localise la couche fautive et détermine le verdict.

### Typologie des verdicts

`CONFORME` · `PARTIEL` · `NON_CONFORME` · `RUNTIME_MANQUANT` · `CONTRAT_AMBIGU` · `HORS_CONTRAT` (amélioration non exigée, hors chemin de verdict).

### Canaux d'exposition (déterminés par les contrats, non par le confort)

- **Projection UI directe** : `001`, `002`, `003` (`90_ui` : « lecture claire : état réel / intention / divergence »).
- **Disponibilité / constatabilité** (capteur, attribut, helper) : `004`, `005`, `006`, `008`, `010`, `011`.
- **Notification** (contenu contractuel) : `007`, `009`, `012`, `015`.
- **Principe :** un canal supplémentaire **ne peut pas** être imposé au seul motif d'être plus pratique.

---

## 📚 3. Corpus contractuel lu (source d'autorité)

16 documents `contrats/alarme/` lus isolément avant toute ouverture d'implémentation :
`README`, `00_gouvernance_alarme`, `10_modele_etats_et_vocabulaire`, `20_interfaces_contexte_et_helpers`, `30_decision_centrale`, `40_application_decision`, `50_intrusion_detection`, `51_ouvrants_entree`, `60_delais_et_blocages`, `61_watchdog_blocage_armement`, `70_sirene_actions_terminales`, `80_notifications_et_feedback`, `90_ui`, `95_diagnostics_et_coherence`, `96_diagnostic_blocage_armement_incoherence`, `99_hors_perimetre_et_extensions`.

Doctrine UI mobilisée pour P‑COMP (restitution des projections exigées) : `00_documentation_arsenal/README.md` + intégralité de `ui/` (dont `couleurs/05_regles` — priorité d'indisponibilité R6 — et `socle_ui/`).

---

## ⚖️ 4. Arbitrages humains intervenus (par étape de production)

La campagne a été conduite par étapes validées (cadrage → inventaire contractuel → audit runtime → audit UI). Arbitrages retenus :

- **Périmètre couleur (cadrage)** : le conflit documentaire de palette `90_ui` ↔ `ui/couleurs/` reste **périphérique** ; il ne produit un verdict que si la couleur est le **seul** moyen contractuel de distinguer deux états diagnostiques — ce qui n'est jamais le cas en Alarme.
- **Gravité (cadrage)** : l'absence d'un diagnostic n'implique pas l'insûreté de la décision ; pas de rehaussement automatique « domaine de sûreté ».
- **« Surface diagnostique » ≠ fichier `diagnostic.yaml`** : toute surface normalement utilisée pour diagnostiquer le domaine peut satisfaire une projection, sauf emplacement contractuel explicite.
- **Inventaire ramené à 13 exigences opposables** : `ALM-DIAG-001…012` + `015`. IDs **conservés, non renumérotés**.
- **E.2 (`004`)** : le code décisionnel est exigé comme support de diagnostic/audit au niveau **disponibilité/constatabilité + couverture des 7 codes** ; **aucune** projection UI supplémentaire exigée.
- **E.3 (`010`)** : exigence = les `unknown/unavailable` des entités consommées restent **constatables** et ne sont **pas** neutralisés/confondus avec un état métier valide ; ni capteur agrégé, ni raison dédiée, ni carte exigés.
- **E.4 (`014` mode test)** : **non retenue** comme exigence opposable (le contrat impose le comportement distinct du mode test, pas sa restitution) → classée `HORS_CONTRAT — opportunité d'observabilité`, hors verdict.
- **Frontière (`013` visiteur)** : **retirée** du périmètre Alarme (relève du domaine présence/visite) ; conservée comme dépendance consommée.
- **P‑COMP des projections exigées** : lorsqu'un contrat impose déjà une projection UI (`001`, `003`), la doctrine Arsenal applicable à cette projection **participe** à l'évaluation de la compréhension (sans créer d'exigence).

---

## 📋 5. Inventaire final des 13 exigences opposables (IDs inchangés)

| ID | Exigence diagnostique | Catégorie | Canal exigé |
|---|---|---|---|
| **ALM-DIAG-001** | État réel du panneau, lecture claire | état | Projection UI |
| **ALM-DIAG-002** | Intention (`DISARMED/ARMED_AWAY/NOOP`) | état / autorisation‑abstention | Projection UI |
| **ALM-DIAG-003** | Divergence état réel ↔ intention (NOOP toléré) | dégradation | Projection UI |
| **ALM-DIAG-004** | Code décisionnel (7 codes, support diag/audit) | raison / autorisation / refus / abstention | Dispo/constatabilité |
| **ALM-DIAG-005** | Raison humaine alignée sur le code | raison / compréhension | Constatabilité |
| **ALM-DIAG-006** | Distinction NOOP ≠ `unknown/unavailable` | abstention / indispo / compréhension | Constatabilité |
| **ALM-DIAG-007** | État « alarme armée » (notif. persistante unique) | état | Notification |
| **ALM-DIAG-008** | Cohérence système + attribut `raison` | dégradation / raison | Constatabilité |
| **ALM-DIAG-009** | Alerte divergence réel/cible persistante (5 min) | dégradation | Notification critique |
| **ALM-DIAG-010** | Indisponibilités constatables, non neutralisées | indisponibilité | Constatabilité |
| **ALM-DIAG-011** | Incohérence structurelle blocage↔timer + attributs | dégradation / compréhension | Constatabilité + notif. |
| **ALM-DIAG-012** | Notification watchdog (type + états blocage/timer) | dégradation | Notification |
| **ALM-DIAG-015** | Intrusion réelle → notification critique | dégradation critique | Notification critique |

*(Hors périmètre : `013` visiteur — renvoyée présence/visite ; `014` mode test — `HORS_CONTRAT`, sans verdict.)*

---

## 🔧 6. Preuves runtime consolidées (P‑R)

**13/13 exigences PRODUITES · 0 `RUNTIME_MANQUANT`.** Producteurs uniques attestés par recherche.

| ID | Porteur runtime | Définition | Couverture / attributs |
|---|---|---|---|
| 001 | `alarm_control_panel.alarme_maison` | `16_template_alarm_panels/alarme_maison.yaml` (`manual`) | `disarmed/armed_away/triggered` ; `pending` inatteignable (`arming/delay_time: 0`) |
| 002 | `input_text.alarme_etat_cible` | `04_input_texts/alarme/etat_cible.yaml` | 3/3 valeurs ; écrivain unique `decision_centrale.yaml` |
| 003 | opérandes 001 + 002 ; divergence calculée en consommation | — | pas de capteur runtime dédié (non requis) |
| 004 | `input_text.alarme_decision` | `04_input_texts/alarme/decision.yaml` | **7/7 codes** ; écrivain unique |
| 005 | `input_text.alarme_raison` | `04_input_texts/alarme/raison.yaml` | 7 raisons alignées 1:1 |
| 006 | `NOOP` (valeur métier) vs états HA d'indispo | `decision_centrale.yaml` ; `…030` exclut NOOP/unknown/unavailable | distincts au runtime |
| 007 | notif. persistante `alarme_etat` | `11_automations/alarme/notification.yaml` (`…021`) | create/dismiss ; producteur unique |
| 008 | `binary_sensor.alarme_systeme_coherent` + `raison` | `12_template_sensors/alarme/coherence.yaml` | 7 valeurs de `raison` |
| 009 | alerte divergence 5 min | `11_automations/alarme/system/alerte_incoherence.yaml` (`…030`) | `for 5 min` ; notif. critique cible+réel+raison |
| 010 | entités sources natives | panel, présence, timers, booleans | conservent `unknown/unavailable` ; gardes I5 / exclusions |
| 011 | `binary_sensor.blocage_armement_incoherent` | `12_template_sensors/alarme/blocage_armement_incoherent.yaml` | attributs `blocage`, `timer_state`, `type_anomalie` (3/3) |
| 012 | notif. watchdog | `11_automations/alarme/watchdog.yaml` (`…034`) | `type_anomalie` + `blocage` + `timer_state` |
| 015 | notif. critique intrusion | `intrusion/mouvement.yaml` (`…009`), `ouverture/delai_entree_fin.yaml` (`…032`), `ouverture/autres.yaml` (`…007`) | hors test → notif. critique ; test → notif. test (I2) |

**Observations runtime mineures (sans absence de porteur) :** C.1 le capteur de cohérence (008) se replie sur « cohérent » sous indisponibilité d'une source (→ O‑5) ; C.2 `pending` inatteignable par configuration (hors observabilité) ; C.3 pas de capteur de divergence dédié (attendu — 003 est une projection UI).

---

## 🖥️ 7. Preuves d'exposition & de compréhension (P‑UI / P‑COMP)

Surfaces : `alarme-dashboard` (Principal), `diagnostics-alarme-dashboard` (Diagnostic), `reglages-alarme-dashboard` — clés résolues dans `18_lovelace/dashboards.yaml`, navigation résolue.

- **001/002/003** projetés sur le **Principal** : `carte_alarme_decision` (état réel + divergence + raison) et `carte_alarme_intention` (intention + divergence + NOOP). Couleurs vert/rouge/gris neutre **canoniques**.
- **008** exposé sur le **Diagnostic** : `alarme_diagnostic_coherence` (« Système cohérent / Incohérence / **Indisponible** », vert/rouge/gris‑indispo) + `alarme_diagnostic_coherence_raison` (libellés mappés, sans orphelin).
- **004** disponible/constatable (helper) — projection UI non exigée (E.2). **005** rendu dans le label de `carte_alarme_decision`. **006** : NOOP → « Aucune action » + gris neutre, distinct du texte d'indispo.
- **011** constatable (capteur + attributs) ; observabilité de l'événement via la notification watchdog (012) — anomalie transitoire (corrigée ≤ 500 ms), aucune carte exigée.
- **007/009/012/015** évalués sur leur canal notification (contenu, criticité, unicité/identifiant, distinction réel/test) — conformes.

---

## ✅ 8. Matrice finale des verdicts

| ID | Canal exigé | Verdict | Motif |
|---|---|---|---|
| **001** | Projection UI | **PARTIEL** | `triggered` (atteignable) restitué en brut, coloré « divergence » (voire « cohérent ») — intrusion active non explicite |
| **002** | Projection UI | **CONFORME** | intention projetée, 3/3, NOOP distinct |
| **003** | Projection UI | **PARTIEL** | indisponibilité d'un opérande rendue comme divergence rouge / sans état d'indispo (viole R6) |
| **004** | Dispo/constatabilité | **CONFORME** | 7/7 codes produits, constatables ; projection UI non exigée |
| **005** | Constatabilité | **CONFORME** | raison lisible, alignée, rendue en UI |
| **006** | Constatabilité | **CONFORME** | NOOP distinct de l'indispo au niveau texte (contradiction visuelle rattachée à 003) |
| **007** | Notification | **CONFORME** | persistante unique, create/dismiss |
| **008** | Constatabilité | **CONFORME** | capteur + raison exposés, indispo gérée, sans orphelin |
| **009** | Notif. critique | **CONFORME** | alerte 5 min, contenu explicite |
| **010** | Constatabilité | **CONFORME** | indispo constatable, non neutralisée à la source |
| **011** | Constatabilité + notif. | **CONFORME** | capteur + attributs + notification watchdog |
| **012** | Notification | **CONFORME** | 3 champs restitués |
| **015** | Notif. critique | **CONFORME** | critique + distinction réel/test |

**Bilan : 11 CONFORME · 2 PARTIEL (`ALM-DIAG-001`, `ALM-DIAG-003`) · 0 NON_CONFORME · 0 RUNTIME_MANQUANT · 0 CONTRAT_AMBIGU.**
Les deux écarts sont localisés **exclusivement** au maillon **P‑UI/P‑COMP** ; le runtime est sain (13/13).

---

## 🔎 9. Détail des deux écarts PARTIEL

### ALM-DIAG-001 — Restitution insuffisamment explicite de l'intrusion active
- **P‑C :** `90_ui` impose une **lecture claire** de l'**état réel** ; `10` liste `triggered` parmi les états réels.
- **Atteignabilité :** `alarme_maison.yaml` fixe `trigger_time: 180` ⇒ `triggered` **effectivement possible** (`pending`, `arming/delay_time: 0`, reste inatteignable et hors chemin de verdict).
- **Constat (T‑1) :** `carte_alarme_decision.state_display` ne mappe que `armed_away`/`disarmed` ; `triggered` retombe en **libellé brut « triggered »**, coloré **rouge « divergence »** (`cible=ARMED_AWAY`) voire **vert « cohérent »** (`cible=NOOP`). L'intrusion active n'est pas restituée de façon explicite.
- **Non‑substitution :** la notification d'intrusion (`015`) satisfait une exigence **distincte** ; elle ne porte pas la projection d'état réel exigée par `001`.
- **Verdict : PARTIEL.**

### ALM-DIAG-003 — Divergence non fiable sous indisponibilité
- **P‑C :** `90_ui` impose la projection de la **divergence**.
- **Doctrine applicable (P‑COMP) :** `couleurs/05_regles` **R6** — l'indisponibilité **prime** ; `unknown/unavailable` doit être rendu en gris indispo, jamais confondu avec un état valide.
- **Constat (T‑2) :** les branches `state` des deux cartes encodent la divergence par la couleur. Un panneau `unavailable/unknown` avec `cible` armée/désarmée **tombe en rouge « divergence »** (comparaison pourtant non fiable) ; une `cible` indisponible ne déclenche **aucun état visuel d'indispo**.
- **Verdict : PARTIEL** — la doctrine ne crée pas l'exigence (`003` impose déjà la projection) ; elle en détermine la restitution correcte, non atteinte sous indisponibilité.

---

## 🧩 10. Constats techniques rattachés aux verdicts

- **T‑1 (→ 001) :** `carte_alarme_decision.state_display` sans mapping de `triggered` (ni des états hors `armed_away`/`disarmed`) ; coloration de `triggered` dépendante de `cible`.
- **T‑2 (→ 003) :** branches `state` des cartes intention/décision sans priorité d'indisponibilité (R6) : opérande `unknown/unavailable` → rouge divergence ou absence d'état visuel d'indispo.

*(Constats de restitution UI — consignés sans remédiation, le chantier de correction n'étant pas ouvert.)*

---

## 🗂️ 11. Observations hors contrat (hors chemin de conformité)

- **O‑3 — Incohérence documentaire de palette.** `alarme/90_ui.md` déclare des valeurs (`bleu info rgba(144,202,249,0.25)`, `gris unknown rgba(224,224,224,0.2)`) divergentes de `ui/couleurs/` ; **non utilisées** par les cartes (vert/rouge/gris canoniques) → sans effet sur un verdict. Incohérence documentaire.
- **O‑4 — Incohérence blocage sans carte.** `binary_sensor.blocage_armement_incoherent` présent en définition + watchdog ; canal exigé (constatabilité + notification 012) satisfait. Une carte dédiée serait une amélioration non exigée.
- **O‑5 — « Cohérence globale » sous indisponibilité.** `alarme_systeme_coherent` peut valoir « cohérent » quand une source est `unavailable` ; la carte 008 **restitue fidèlement le backend** (aucun écart UI). Arbitrage **documentaire** ouvert : le capteur doit‑il agréger la disponibilité de ses sources ?
- **O‑6 — Code décisionnel non projeté (004).** **Conforme** à l'arbitrage E.2 ; rappelé pour éviter toute requalification.

---

## 🏁 12. Conclusion

La chaîne diagnostique du domaine **Alarme est conforme de bout en bout aux contrats sur 11 des 13 exigences opposables**, chacune sur le **canal contractuellement imposé** (projection UI, capteur/attribut, notification). Le **runtime est intégralement sain** (13/13 produits ; couverture des valeurs et attributs attestée ; producteurs uniques tracés).

**Deux écarts `PARTIEL`, exclusivement au maillon d'exposition/compréhension UI** : la restitution de l'**intrusion active** (`triggered`, `ALM-DIAG-001`) et la restitution de la **divergence sous indisponibilité** (`ALM-DIAG-003`, priorité d'indisponibilité R6). Aucun `NON_CONFORME`, aucun `RUNTIME_MANQUANT`, aucun `CONTRAT_AMBIGU`.

La méthode a tenu ses garde‑fous : distinction stricte exigence / runtime / exposition ; refus des faux positifs (conflit couleur périphérique, carte non exigée, code non projeté, indisponibilité) ; et évaluation de la compréhension **uniquement** là où une projection est **déjà exigée** par les contrats.

---

## 🚧 13. Suites explicitement non encore autorisées

- **Chantier de correction de `ALM-DIAG-001` et `ALM-DIAG-003`** (restitution `triggered` ; priorité d'indisponibilité sur la divergence) : **non autorisé à ce stade**. Son cadrage fera l'objet d'un livrable et d'une validation distincts, **après** consignation de cet audit.
- **Arbitrages documentaires** O‑3 (palette `90_ui`) et O‑5 (définition de la « cohérence globale ») : à trancher séparément, hors de cet audit.
- **Cadrage méthodologique transverse de la campagne** : **non déposé** dans le dépôt à ce stade ; son éventuelle consignation reste un arbitrage distinct, après stabilisation de la méthode et détermination d'un emplacement canonique.

---

*Rapport d'audit lecture seule. Aucune modification runtime, UI ou contractuelle. Identifiants `ALM-DIAG-001…015` conservés.*
