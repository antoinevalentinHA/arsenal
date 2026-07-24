# C34 — Portefeuille de chantiers (livrable 3)

| Champ | Valeur |
|---|---|
| **Objet** | Livrable 3 du chantier [C34](chantier_comportement_reboot_reload_domaines.md) : consolider **chaque risque confirmé** des quatre vagues d'audit et de leurs contre-audits, le **rattacher à un chantier** (existant ou nouveau), avec **propriétaire, lots et preuves manquantes qualifiées**. |
| **Date** | 2026-07-24 |
| **Nature** | Synthèse **hiérarchisante et orientante**, sans code ni correctif. Les **solutions** relèvent du **livrable 4** (distinct). |
| **Entrées** | [vague 1](../../01_rapports/transverses/c34_vague1_audit_vmc_deshumidificateur.md) · [vague 2](../../01_rapports/transverses/c34_vague2_audit_climatisation_chauffage.md) · [vague 3](../../01_rapports/transverses/c34_vague3_audit_arrosage_eclairage.md) · [vague 4](../../01_rapports/transverses/c34_vague4_audit_alarme.md) |

> **Ce document ne corrige rien et ne tranche aucun arbitrage propriétaire.** Il **rattache** et
> **hiérarchise**. Toute orientation corrective détaillée est renvoyée au livrable 4.

---

## 1. Résultat d'ensemble

Sur **sept domaines à action physique × trois familles d'événements**, l'audit consolidé établit
qu'**aucun défaut d'action physique indésirable n'est démontré** au sens de l'invariant C34. Les
findings initiaux les plus alarmants (recomposition de capteurs) ont été **réfutés ou réduits** par
les contre-audits, qui ont établi que les entités consommées sont **structurellement immunisées**
contre `unavailable → on`. Ne subsistent que :

- **un finding à conséquence élevée mais atteignabilité rare** (sirène, reboot pendant `triggered`) ;
- **des résidus à faible atteignabilité** (course visiteur ; chemins de réconciliation) ;
- **un lot correctif déjà décidé** (déshumidificateur, branche B — issu de la vague 1) ;
- **deux arbitrages** (cycle d'alimentation clim au reload ; asymétrie doctrinale) ;
- **une correction de racine doctrinale** (la protection réelle = couche de normalisation/persistance,
  non `systeme_stable`) — **le principal apport transverse**.

---

## 2. Registre consolidé des findings

| ID | Source | Domaine | Mécanisme | Qualif. §2 | Preuve §8 | Gravité | Atteignabilité | Statut |
|---|---|---|---|---|---|---|---|---|
| **A** | V4 | alarme | Sirène `10020000000011` (`to: triggered`, **sans garde `systeme_stable`**) rejouée si le panneau `manual` **restaure `triggered`** au reboot | action physique indésirable (candidate) | démontré statiquement (guard-gap) ; **effet indéterminable** | **élevée** (sirène) | **rare** (reboot pendant alarme active) | **survivant — mécanisme distinct (RestoreEntity), non réfuté** |
| **C** | V4 | alarme | `presence_visiteur`/`visite_en_cours` **sans `initial:`** restaurés + **course** non ordonnée sur `systeme_stable→on` ⇒ désarmement transitoire | action physique indésirable (candidate) | mécanisme démontré ; effet indéterminable | moyenne | **très faible** (exige incohérence amont : armé + visiteur `on`) | **survivant borné** |
| **B** | V4 | alarme | Intrusion ouverture `10020000000007` (`to:'on'` **sans `from:`**) | — | **réduit** au contre-audit V3 | faible | **très faible** (résidu réconciliation) | **réduit — contacts = templates jamais `unavailable`** |
| **E1** | V3 | éclairage | Allumages séjour/garage (`to:'on'` **sans `from:`**) | — | **réfuté** au contre-audit V3 (même racine que B) | faible (éclairage) | résiduelle | **réfuté comme artefact de recomposition** |
| **L1-DESHUM** | V1 | déshum. | `etat.yaml` absorbe l'indisponibilité en `false` (`float` nu non gardé) ⇒ G7 franchi (105 occ./30 j, preuve L4) | écart contrat→lacune, requalifié | démontré (statique + runtime L4) | confort (faux arrêts) | avérée (mensuel) | **lot correctif décidé — branche B (§10.6 V1)** |
| **ARB-CLIM** | V2 | clim | Cycle d'alimentation `clim_power` au **reload d'intégration Airstage** (coupure intégration + rejeu Arsenal) | recalcul (rejeu) ; coupure d'origine intégration | L4 + statique ; **réalité physique indéterminable** | à établir | à chaque reload Airstage | **arbitrage — pas un défaut Arsenal** |
| **ASYM-DOCTRINE** | V2 | clim/chauffage | Commande directe (clim) vs consigne déléguée à Netatmo (chauffage) | — | démontré statiquement | — | — | **observation doctrinale** |
| **DOCTRINE-NORM** | V2+V3 | transverse | La protection réelle contre la recomposition = **couche de normalisation/persistance**, **non** `systeme_stable` (borné au reboot HA, non érigé en invariant) | — | démontré statiquement (transverse) | — | — | **apport doctrinal central** |
| **DETTE-ECL** | V3 | éclairage | 27 automatisations / 7 contrats — complétude contractuelle partielle | — | — | — | — | **dette documentaire** |

---

## 3. Rattachements (risque → chantier · propriétaire · lots · preuves manquantes)

### P1 — Finding A (sirène non gardée au reboot) — **priorité la plus haute**

- **Rattachement** : **nouveau chantier correctif** « Alarme — sûreté sirène au redémarrage » (domaine
  alarme), sous C34 comme déclencheur.
- **Propriétaire** : opérateur (arbitrage de sûreté requis).
- **Arbitrage préalable (bloquant)** : *un panneau `alarm_control_panel: manual` restauré à `triggered`
  au reboot **doit-il** re-déclencher la sirène ?* Deux doctrines possibles — re-sonner (continuité de
  l'alerte) vs. exiger une ré-confirmation d'intrusion (anti-ré-ignition parasite). **Non tranché.**
- **Lots proposés** :
  - **L1** — trancher la doctrine ci-dessus.
  - **L2** — selon L1 : soit garde `systeme_stable` sur `10020000000011`, soit réconciliation du panneau
    au boot (sortir `triggered` avant réarmement sirène), soit gate sur un état « intrusion confirmée »
    **non restauré**. Aligner le contrat `70_sirene_actions_terminales.md` (couvre la reboot-safety de
    l'**extinction**, pas de la **ré-ignition**).
  - **L3** — preuve.
- **Preuves manquantes qualifiées** : occurrence d'un **reboot pendant état `triggered`** + comportement
  de restauration du panneau `manual` (émission d'un événement `to: triggered`). **Indéterminable** sans
  provoquer un reboot ; à obtenir par occurrence naturelle **ou** par le chantier d'instrumentation (I1).

### P2 — Finding C (désarmement transitoire visiteur)

- **Rattachement** : **[D-PRES](../../REGISTRE_CHANTIERS.md)** (dette de modélisation de la présence)
  **ou** lot alarme dédié.
- **Propriétaire** : opérateur.
- **Lots proposés** : **L1** — ordonner la course boot (un seul écrivain, ou `securite_reboot` **avant**
  l'application) **ou** poser `initial: off` sur `presence_visiteur`/`visite_en_cours` (⚠️ effet sur la
  reconstruction d'une visite en cours — arbitrage). **L2** — preuve.
- **Preuves manquantes** : reboot avec état **incohérent** amont (armé + visiteur `on`). **Indéterminable**
  (atteignabilité très faible ; ne bloque pas).

### P3 — Findings B & E1 (résidus de réconciliation)

- **Rattachement** : **sous-système de réconciliation des ouvertures** (`12_template_sensors/ouvertures/`)
  / D-PRES.
- **Propriétaire** : opérateur.
- **Lots proposés** : **L1** — caractériser la **restauration du `business_state`** d'un
  `input_text.contact_reconciliation_context_*` au reboot (peut-il restaurer `on` alors que l'entité était
  `off` ?). **Défense en profondeur** possible : convention `from: 'off'` sur les triggers d'action
  physique (redondante avec la normalisation, mais uniforme).
- **Preuves manquantes** : reload d'intégration Zigbee **provoqué** (interdit C34) **ou** instrumentation
  (I1). **Faible priorité** (mécanisme réfuté/réduit ; résidu indéterminable).

### P4 — Lot correctif déshumidificateur (branche B) — **le seul correctif code déjà décidé**

- **Rattachement** : **vague 1, §10.6** (branche B retenue) — chantier existant, **prêt à implémenter**.
- **Propriétaire** : opérateur (arbitrages 4/2 restants).
- **Lots** (rappel §10.6) : (1) valeur par défaut au `float` de `etat.yaml` ; (2) `guard.md` — G7 amputé ;
  (3) `deshumidificateur.md` — exception à la doctrine d'observation ; (4) sort du code inerte (supprimer
  vs conserver documenté) ; (5) checker CI interdisant un `float` nu non gardé sur une source de vérité.
- **Preuves manquantes** : **aucune** — documentaire + code, solvable sans preuve terrain.

### A1 — Arbitrage cycle d'alimentation clim au reload Airstage

- **Rattachement** : **nouveau** « Climatisation — coût du reload d'intégration » (arbitrage), ou backlog
  climatisation.
- **Propriétaire** : opérateur.
- **Arbitrage** : **tolérer** le cycle bref (coupure intégration + rejeu Arsenal) **vs raréfier** les
  reloads d'intégration Airstage (le watchdog `resilience_integrations` en déclenche sur panne). **Pas un
  défaut de code Arsenal.**
- **Preuves manquantes** : **réalité physique** de la coupure (le compresseur s'arrête-t-il ?) —
  `switch.clim_power` **hors allowlist Recorder** ⇒ **indéterminable** sans instrumentation (I1).

### A2 — Asymétrie doctrinale commande-directe vs consigne-déléguée

- **Rattachement** : **doctrine** (architecture).
- **Propriétaire** : opérateur.
- **Lot** : **nommer et documenter** l'asymétrie (clim = commande directe, exposée aux aléas de
  l'intégration ; chauffage = consigne déléguée à Netatmo, immunisée côté Arsenal mais **opaque** côté
  Netatmo). Décider si elle est **assumée** ou **à converger**.

### D1 — Invariant de démarrage/rechargement — **apport doctrinal central**

- **Rattachement** : **nouvelle doctrine** « Comportement au démarrage et au rechargement » (le sujet
  consolidé dont C34 est devenu propriétaire).
- **Propriétaire** : opérateur.
- **Lots proposés** :
  - **L1** — graver que la **protection contre les artefacts de recomposition** repose sur la **couche de
    normalisation/persistance** (agrégats OR, réconciliation à quarantaine, normalisation *hold-last*,
    verrous d'admissibilité persistés), **démontrée** sur alarme (contacts/mouvements), éclairage,
    climatisation (verrou d'admissibilité).
  - **L2** — graver que **`systeme_stable` est borné au reboot HA** et **ne couvre pas** les reloads
    d'intégration ; il ne doit **pas** être présenté comme la garde universelle.
  - **L3** — statuer sur une **convention transverse** (ex. `from: 'off'` sur les triggers d'action
    physique) comme défense en profondeur uniforme.
- **Preuves manquantes** : **aucune** — doctrinaire.

### I1 — Chantier d'instrumentation probatoire (pour les indéterminables)

- **Rattachement** : **nouveau** chantier d'instrumentation (prévu par le cadrage §8/§9).
- **Propriétaire** : opérateur.
- **Lot** : historiser (allowlist Recorder, bornée) un **actionneur physique propre** et les entités
  décisives — `switch.clim_power` (ARB-CLIM), le panneau `alarm_control_panel.alarme_maison` (Finding A),
  les contextes de réconciliation (P3) — pour **lever** les indéterminables sans provoquer de panne.
- **Preuves manquantes** : c'est le chantier qui **produit** la preuve. **Aucun reboot/reload/panne
  provoqué** ; observation d'occurrences naturelles.

### Dette — complétude contractuelle éclairage (DETTE-ECL)

- **Rattachement** : **backlog éclairage** (documentaire). Non prioritaire ; hors invariant C34.

---

## 4. Hiérarchie

**A > C > (B, E1 résidus)** pour les findings de sûreté ; **P4 (déshum. branche B)** est le **seul
correctif code prêt** ; **D1 (invariant doctrinal)** est l'**apport le plus structurant** et
conditionne la valeur durable de C34 ; **I1 (instrumentation)** débloque tous les indéterminables ;
**A1/A2** sont des arbitrages, non des défauts.

**Ordre d'engagement recommandé** : **D1** (grave la doctrine, capitalise l'audit) → **P4** (correctif
déjà décidé, sans preuve manquante) → **P1/L1** (arbitrage sirène) → **I1** (instrumentation pour
A/ARB-CLIM/P3) → arbitrages A1/A2 → résidus P2/P3.

---

## 5. Ce qui n'est **pas** retenu

- **E1** (éclairage) — **réfuté** comme artefact de recomposition.
- **B** (alarme) — **réduit** à un résidu de réconciliation indéterminable (à ne **pas** traiter comme
  « recomposition de capteur brut »).
- La **garde `systeme_stable` comme protection contre les reloads** — **infirmée** (bornée au reboot).
- Tout **effet physique climatisation** comme défaut Arsenal — **innocenté** (coupure d'origine
  intégration, rejeu = recalcul).

---

## 6. Clôture C34

Après ce portefeuille (livrable 3), il reste le **livrable 4 — solutions documentées** pour les
chantiers prioritaires (au niveau de détail permettant l'implémentation sans refaire l'analyse). Les
**quatre critères de clôture** du cadrage §9 restent **documentaires** ; **aucun ne dépend d'une panne
provoquée**. Les comportements **indéterminables** (A, ARB-CLIM, résidus P3) ne bloquent pas la clôture :
ils sont **qualifiés** et renvoyés au chantier d'instrumentation **I1**.
