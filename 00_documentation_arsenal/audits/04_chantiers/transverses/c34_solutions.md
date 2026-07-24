# C34 — Solutions documentées (livrable 4)

| Champ | Valeur |
|---|---|
| **Objet** | Livrable 4 (et dernier) du chantier [C34](chantier_comportement_reboot_reload_domaines.md) : documenter les **solutions** des chantiers prioritaires du [portefeuille](c34_portefeuille_chantiers.md), **au niveau de détail permettant l'implémentation sans refaire l'analyse**. |
| **Date** | 2026-07-24 |
| **Nature** | **Conception de solutions**, pas d'implémentation. Aucune modification runtime dans ce livrable. Chaque solution reste subordonnée aux **arbitrages propriétaire** signalés. |
| **Ordre** | D1 → P4 → P1 → I1 → A1/A2 → résidus (recommandé au portefeuille §4). |

> **Ce document ne modifie aucun runtime.** Il **spécifie** ce que chaque chantier devra produire.
> L'exécution relève de PR distinctes, sous les arbitrages ci-dessous.

---

## D1 — Doctrine « Comportement au démarrage et au rechargement »

**But** : capitaliser l'apport transverse de C34 en une doctrine **normative et opposable**, dont C34
est devenu le propriétaire (§4 du cadrage : sujet sans propriétaire unique préexistant).

**Livrable** : nouveau document
`00_documentation_arsenal/architecture/03_doctrines/comportement_demarrage_rechargement.md`, statut
« Stable — conforme Arsenal », applicabilité globale. **Spécification de contenu** :

### §1 — Objet et périmètre
Trois familles d'événements (**reboot HA · reload YAML · reload d'intégration**) + phases transitoires
(restauration, indisponibilité, recalcul). Vise les domaines à **action physique**.

### §2 — Invariant
> Une opération **technique** ne doit pas provoquer, **par elle-même**, une activation, coupure,
> révocation, impulsion, rejeu ou changement physique **injustifié** — **sans présumer** que le
> maintien de l'état antérieur soit toujours correct.

### §3 — Les sept qualifications
Reprendre la grille du cadrage §2 (continuité légitime · abstention temporaire · restauration ·
recalcul fonctionnel · révocation de sécurité · action physique indésirable · anomalie diagnostic/UI).
Seule la **6ᵉ** est un défaut ; la **5ᵉ** est parfois obligatoire (alarme).

### §4 — Catalogue des patrons de protection (**cœur de la doctrine**)
Chaque patron : définition + **exemple audité** + quand l'employer. Établis par C34 comme la **vraie**
protection contre les artefacts de recomposition/restauration :

| Patron | Définition | Exemples audités (C34) |
|---|---|---|
| **PAT-1 — Agrégat availability-safe** | agrégat OR rendant `off` (jamais `unavailable`) si une source est indisponible | `mouvement_*` (V3/CA-V3) ; `rain_bird_pont_donnees_disponibles` (V3) |
| **PAT-2 — Réconciliation à quarantaine** | état métier persisté (`business_state`), un `on` **non corroboré** reste `off` | `contact_*` redondants (CA-V3) |
| **PAT-3 — Normalisation hold-last** | source indisponible ⇒ **conserve** le dernier `on`/`off`, jamais `unavailable` | `contact_*` base, `alarme_ouvrants_entree` (V4/CA-V3) |
| **PAT-4 — Verrou/consigne persisté** | `input_boolean`/`input_number` ancrant la décision, réconcilié au boot | `besoin_clim_*_admissible` (V2) ; `arrosage_dernier_effectif` (V3) |
| **PAT-5 — Garde de disponibilité exécutive** | le **script exécutif** re-vérifie la disponibilité et **s'abstient** | VMC `basse_vitesse` (V1) ; `station_1_courte_supervisee` (V3) ; `clim_execution` (V2) |
| **PAT-6 — Rattrapage idempotent deadline-gaté** | ré-assertion d'un état **calculé** (souvent `off`), conditionnée à une échéance persistée | extinctions éclairage (V3) |
| **PAT-7 — Ré-assertion bornée sur front de récupération** | rejouer la décision **persistée** quand l'infra revient, gardé et **borné** | `rearmement_apres_recuperation` clim (V2) |

### §5 — Statut de `input_boolean.systeme_stable` (**correction de racine**)
- `systeme_stable` est posé **+45 s après le `homeassistant start`** (unique producteur
  `stabilisation_post_demarrage`), et **ne retombe qu'au reboot HA**.
- Il est un **garde-fou temporel de boot**, **PAS une immunité de recomposition** : il **ne couvre
  pas** les reloads d'intégration (les entités recomposent sans qu'il ne bascule).
- **Interdiction** de le présenter comme la garde universelle contre les artefacts de reload. La
  protection réelle est **la couche de normalisation (§4)**.

### §6 — Convention des triggers d'action physique (défense en profondeur)
- **Interdit** : déclencher une **action physique** sur `to: <val>` **sans `from:`** à partir d'une
  **entité brute d'intégration** (susceptible de `unavailable → on`).
- **Recommandé** : `from: 'off'` explicite, **même** derrière une entité normalisée (uniformité).
  *Note* : sur une entité normalisée (§4), `to:'on'` et `from:'off'` sont équivalents (elle n'est
  jamais `unavailable`) — la convention est de **cohérence**, la protection venant de la normalisation.

### §7 — Frontière avec la révocation de sécurité
Le **maintien aveugle** de l'état antérieur n'est pas une protection : certains états doivent **ne pas**
être restaurés (alarme — révocation de sécurité). La doctrine renvoie aux contrats de domaine pour ces
cas.

**Preuves manquantes** : aucune (doctrinaire). **Arbitrage** : adoption de la doctrine + de la
convention §6 (opposabilité).

---

## P4 — Déshumidificateur, branche B (§10.6 vague 1) — **le correctif code prêt**

**Rappel** : branche B retenue (ratifier le repli sur OFF, amender le contrat plutôt que le code). Cinq
lots, **détaillés pour implémentation** :

### Lot 1 — `12_template_sensors/deshumidificateur/etat.yaml` (code)
Ajouter une **valeur par défaut** au filtre `float` pour supprimer l'exception de rendu (cause établie
en V1 §9.6/§10.1 : `float` nu ⇒ exception ⇒ entité `unavailable`) :
```jinja
{{ (p_raw | float(0)) > 100 }}
```
Effet : source indisponible ⇒ `0` ⇒ `> 100` faux ⇒ **`off`**, **jamais `unavailable`** — conforme à
la branche B (repli OFF ratifié) et à **PAT-3/PAT-4**. Conserver la garde `invalides` en amont (défense
en profondeur).

### Lot 2 — `contrats/deshumidificateur/guard.md` (contrat)
- **G7** : acter que la source de vérité **ne remonte jamais** `unavailable` sous branche B ⇒ la
  condition de G7 est **structurellement inatteignable en régime établi**. Reformuler : G7 ne
  s'applique qu'à la **fenêtre transitoire** de première évaluation (documentée), non au régime nominal.
- **§9** `last_observed_state` : **amputer** `unknown`/`unavailable` des valeurs possibles en régime
  établi (les conserver pour la seule fenêtre transitoire, si retenue).

### Lot 3 — `contrats/deshumidificateur/deshumidificateur.md` (doctrine de domaine)
Inscrire une **exception explicite** à la doctrine d'ouverture (« gouverner par observation, jamais par
supposition ») : le **repli sur OFF** en cas d'indisponibilité de la prise est **ratifié** (branche B),
en renvoyant à la doctrine D1 §4 (PAT-3). Lever la contradiction active relevée en V1 §10.2.

### Lot 4 — Sort du code rendu inerte (arbitrage propriétaire)
La garde `not in ['unknown','unavailable']` de `forcer_etat`/`reconciliation`/`set_state` devient
**inerte** (la source ne remonte plus l'indisponibilité). **Recommandation** : **conserver et documenter
comme neutralisé** (commentaire « inerte sous branche B — réactivable si retour branche A »), pour
préserver la **réversibilité** vers la branche A. *À trancher.*

### Lot 5 — Checker CI (nouveau)
`scripts/arsenal_contracts/check_source_verite_float_garde.py` : interdire un `| float` **nu** (sans
`(défaut)`) dans un template déclaré **source de vérité**. Workflow dédié (bloquant). Aligne avec la
convention transverse.

### Question ouverte à solder avant/pendant
Vérifier `criteres/humidite_absolue.yaml` et `criteres/humidite_relative.yaml` (même motif `float` nu
aux mêmes lignes, alimentant le décisionnel) : **exposition** au même défaut ? Si oui, les inclure au
Lot 1/Lot 5.

**Preuves manquantes** : aucune (documentaire + code). **Prêt à engager.**

---

## P1 — Sirène : sûreté au redémarrage (Finding A)

**Arbitrage propriétaire (bloquant)** : *un `alarm_control_panel: manual` restauré à `triggered` au
reboot doit-il re-déclencher la sirène ?*

| Option | Pour | Contre |
|---|---|---|
| **(a) Re-sonner** (statu quo) | continuité de l'alerte si intrusion réelle en cours | ré-ignition sur **artefact** de restauration (reboot ≠ nouvelle intrusion) ; sirène = action à conséquence maximale |
| **(b) Ne pas re-sonner sans ré-confirmation** *(recommandé)* | supprime la ré-ignition parasite ; une intrusion réellement en cours **re-déclenche** via les automatisations d'intrusion gardées | un reboot pile pendant une intrusion active perd le son jusqu'à la prochaine détection |

**Solution (option b) — matérialiser « intrusion confirmée » comme état non restauré.** Aligne avec la
**refonte cible déjà documentée** au contrat 50 §9 :
1. Introduire `input_boolean.alarme_intrusion_confirmee` **avec `initial: off`** (donc **jamais
   restauré** `on` au reboot).
2. Les automatisations d'intrusion (`…007`/`…009`/`…032`), à l'instant du déclenchement réel, posent
   ce booléen `on` **en plus** d'appeler `alarm_trigger`.
3. `10020000000011` (sirène) déclenche `to: triggered` **ET** condition
   `input_boolean.alarme_intrusion_confirmee == 'on'` **ET** `mode_test off`.
4. Au reboot : panneau restauré `triggered` mais `alarme_intrusion_confirmee` = `off` (initial) ⇒ **pas
   de ré-ignition**. Une détection réelle post-boot repose le booléen ⇒ sirène nominale.
5. Amender **contrat 70** : ajouter la clause « la sirène n'est pas rejouée sur un `triggered`
   **restauré** au reboot ; la ré-ignition exige une intrusion **confirmée** non restaurée ».
6. Réconcilier le panneau `triggered` orphelin au boot (le sortir vers son état armé après
   stabilisation), pour ne pas laisser un `triggered` figé sans son.

**Preuve manquante** : reboot pendant `triggered` (indéterminable ; à obtenir par occurrence naturelle
ou via **I1**). La solution est **démontrable statiquement** (le booléen `initial: off` ne peut pas être
`on` au boot) — donc **implémentable sans attendre la preuve**.

---

## I1 — Instrumentation probatoire (lève les indéterminables)

**But** : rendre observables les comportements aujourd'hui **indéterminables** (Finding A, ARB-CLIM,
résidus P3), **sans provoquer** reboot/reload/panne — sur le modèle des microscopes Population B
(C20/C22).

**Solution** : ajout **borné** à `recorder.yaml` (dérogation à la parcimonie, cible LTS, **retrait dès
l'indétermination levée**) de :
- `switch.clim_power` + `climate.clim` → caractériser la **réalité physique** de la coupure au reload
  Airstage (ARB-CLIM) : le compresseur s'arrête-t-il, et combien de temps ?
- `alarm_control_panel.alarme_maison` → observer une **restauration `triggered`** en occurrence
  naturelle (Finding A).
- (optionnel) un `input_text.contact_reconciliation_context_*` témoin → observer une restauration de
  `business_state` (résidu P3).

**Protocole** : observation d'occurrences **naturelles** (reboots/reloads subis), horodatage, corrélation
avec les entités décisionnelles. **Aucune panne fabriquée** (R-VERROU-2). Critère de **retrait** :
indétermination levée **et** finding tranché.

**Preuve** : c'est le chantier qui **produit** la preuve.

---

## A1 / A2 — Arbitrages (pas de code)

- **A1 — cycle d'alimentation clim au reload Airstage.** Décision : **tolérer** (le rejeu est un
  recalcul correct ; réalité physique à confirmer par I1) **vs raréfier** les reloads d'intégration
  Airstage (revoir les seuils du watchdog `resilience_integrations`). **Recommandation** : tolérer, puis
  ré-arbitrer après I1 si la coupure physique s'avère réelle et gênante. **Pas un défaut de code.**
- **A2 — asymétrie doctrinale.** Décision : **assumer** (documenter dans D1 §4 que commande-directe et
  consigne-déléguée sont deux stratégies légitimes, la seconde immunisant Arsenal mais déplaçant
  l'opacité côté Netatmo) **vs converger**. **Recommandation** : assumer et documenter.

---

## Résidus (P2, P3) — solutions différées

- **P2 (course visiteur, Finding C)** : ordonner la course boot — faire de `securite_reboot` un
  **prérequis** de l'application (ex. l'application attend un jeton de reconstruction visiteur), **ou**
  `initial: off` sur `presence_visiteur`/`visite_en_cours` (⚠️ arbitrage : effet sur une visite en cours
  au reboot). **Faible priorité** (atteignabilité très faible).
- **P3 (résidus réconciliation)** : couvert par la **convention D1 §6** (défense en profondeur) et
  l'observation **I1**. Pas de correctif dédié tant que le résidu reste indéterminé.

---

## Clôture C34

Ce livrable 4 **complète les quatre critères de clôture** du cadrage §9 :

| Livrable | Statut |
|---|---|
| 1 — Cartographie (4 vagues) | ✅ |
| 2 — Contre-audits (4) | ✅ |
| 3 — Portefeuille | ✅ |
| 4 — Solutions documentées | ✅ (présent document) |

**C34 est prononçable clos** dès le merge de ce livrable : les quatre livrables sont **documentaires** et
**solvables sans preuve terrain** (cadrage §9). Les comportements **indéterminables** (Finding A,
ARB-CLIM, résidus P3) **ne bloquent pas** la clôture — ils sont **qualifiés** et **rattachés** (I1). Les
chantiers issus du portefeuille (**D1, P4, P1, I1, A1/A2**) **poursuivent leur vie propre** hors de C34,
chacun avec son propriétaire et ses lots. **Aucune orientation corrective n'a été exécutée** dans C34 :
le chantier a **cartographié, contre-audité, hiérarchisé et conçu** — l'implémentation est déléguée.
