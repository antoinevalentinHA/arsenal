# Note de décision — Politique estivale COOL : absence longue, Vacances, préparation du retour (D1–D15)

| Champ | Valeur |
|---|---|
| **Type** | Note de décision / cadrage (conception préalable — **sans implémentation**) |
| **Domaine** | Climatisation — mode COOL : politique d'absence, Vacances, préparation du retour |
| **Statut** | **Décisions D1–D15 actées par le propriétaire d'Arsenal (2026-07-14).** Aucun contrat opposable, aucun runtime. Prépare des contrats et des chantiers ; n'en tient pas lieu. |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-07-14 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ `main` HEAD `15ab991` |
| **Cadre** | Aucun YAML, aucun helper, aucune automation, aucun ID d'entité, aucune modification de contrat/UI/runtime. Ne fixe **aucune règle opposable**. |
| **Rapport d'audit source (mergé, intact)** | [`audit_absence_vacances_chauffage_climatisation_cool.md`](../../01_rapports/transverses/audit_absence_vacances_chauffage_climatisation_cool.md) (PR #361) |
| **Chantiers ouverts** | **C20** [`chantier_politique_absence_cool.md`](../../04_chantiers/climatisation/chantier_politique_absence_cool.md) · **C21** [`chantier_preparation_retour_vacances_cool.md`](../../04_chantiers/climatisation/chantier_preparation_retour_vacances_cool.md) (dépend de C20) |
| **Plan d'action** | [`plan_action_politique_absence_vacances_cool.md`](../../03_plans_action/climatisation/plan_action_politique_absence_vacances_cool.md) |
| **Registre** | [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C20 actif, C21 parqué/dépendant — co-commit) |

> **Nature de ce document.** Il **consigne des décisions** issues d'une chaîne d'études en lecture seule (audit → convergence → correction). Il **ne modifie aucun runtime ni contrat** et ne se substitue à aucun contrat : la formalisation opposable relève des contrats à rédiger dans les chantiers (ordre Arsenal : contrat avant runtime). En cas de divergence future, **le contrat fera foi**.

> **Conservation de l'historique.** Le rapport d'audit mergé (#361) reste **intact** — photographie factuelle de l'état audité au 14 juillet. Les arbitrages postérieurs vivent **ici**, document distinct.

---

## 1. Contexte

Chaîne d'études préalables (toutes en lecture seule) : audit comparatif chauffage/COOL (mergé #361) → étude de convergence → correction du veto Vacances. Le présent document **fige les décisions** qui en résultent et **ouvre les chantiers** correspondants.

**Entités existantes citées (vérifiées, non inventées)** : `binary_sensor.autorisation_clim_cool`, `binary_sensor.clim_extinction_absence_prolongee_autorisee`, `timer.absence_longue_clim`, `binary_sensor.vacances_actives`, `input_datetime.fin_vacances`, `binary_sensor.presence_famille_unifiee`, `binary_sensor.presence_confort_thermique_stabilisee`, `sensor.consigne_clim_appliquee`, `input_number.clim_consigne_absence`, `input_number.clim_consigne_presence`, `sensor.clim_raison_decision`, `sensor.clim_verdict_cool`. Entités doctrinales déclarées mais **non implémentées** (dette) : `input_boolean.clim_blocage_absence_prolongee_actif`, `binary_sensor.clim_blocage_absence_prolongee_reel`.

**Rôles nouveaux (aucun ID proposé — ID à attribuer par le propriétaire d'Arsenal)** : helper de durée d'absence longue ; horodatage de début d'absence ; vérité intermédiaire de veto composite ; vérité opérationnelle de préparation COOL ; helper de durée de préparation ; consigne de préparation ; diagnostic de préparation.

---

## 2. Décisions actées (D1–D15)

### D1 — Veto immédiat des Vacances
Dès `binary_sensor.vacances_actives == on`, les Vacances produisent **immédiatement** un veto COOL, **indépendant** du timer, de la durée d'absence longue et du temps déjà écoulé. Vacances est une **qualification métier explicite**, non confirmée par un seuil temporel.

### D2 — Maintien du rôle métier de l'absence longue
Le mécanisme d'absence longue est **conservé**. Il couvre les longues journées, week-ends non déclarés, départs improvisés, absences multi-jours non qualifiées, oublis du mode Vacances. Il matérialise une **absence prolongée à échéance de retour inconnue**. Il n'est **ni une anomalie historique, ni un substitut de Vacances**.

### D3 — Durée d'absence longue gouvernée
La durée fixe (8 h aujourd'hui, figée dans `timer.absence_longue_clim`) devient un **paramètre opérateur persistant** : helper numérique (ID à attribuer), unité **heures**, **sans `initial:`** (doctrine `restauration_etat_helpers.md`, restauration d'état préservée), exposé au dashboard Réglages climatisation, **UI strictement non décisionnaire**. Préférence de déploiement envisagée : **14 h — non gravée** comme invariant physique ni constante normative. Bornes et granularité à fixer **dans le contrat cible**.

### D4 — Continuité physique de l'absence
La durée représente la **durée physique continue** de l'absence. Un redémarrage HA ne doit **pas** remettre la qualification à zéro arbitrairement. Orientation : **horodatage de début d'absence** (ID à attribuer) → **échéance = horodatage + durée helper** → **recalcul idempotent au boot** → qualification immédiate si l'échéance est dépassée → échéance et durée écoulée **observables**. Le timer actuel peut devenir instrumental ou être remplacé (selon contrat/plan), mais **ne doit plus imposer de remise à zéro au boot**.

### D5 — Application immédiate d'un changement de durée
Si l'opérateur modifie la durée pendant une absence active : **échéance recalculée immédiatement** ; une durée raccourcie sous le temps écoulé **peut qualifier immédiatement** ; une durée allongée **repousse** l'échéance ; le **diagnostic rend ce comportement explicite**.

### D6 — Deux causes de veto, une autorité
Causes de veto : **absence longue qualifiée** et **Vacances actives**. La préparation du retour est une **exception temporaire et bornée**. Formule fonctionnelle cible (non normative) :

```
veto_absence_vacances_effectif =
    (absence_longue_qualifiee OR vacances_actives)
    AND NOT preparation_cool_active
```

Autorité finale **unique** : `binary_sensor.autorisation_clim_cool`. **Aucune décision centrale COOL** analogue au chauffage. La préparation **ne neutralise jamais** les autres conditions/blocages : aération, fenêtres, blocage horaire, température extérieure, indisponibilités, autres gardes indépendantes.

### D7 — Vérité intermédiaire du veto composite
Une **vérité calculée intermédiaire** matérialisant le veto effectif absence/Vacances est retenue comme orientation cible : point **unique testable**, formule contractuelle explicite, observabilité, diagnostic, **pas de duplication** de la logique composite. Elle sera **calculée**, **sans écrivain**, **ID attribué ultérieurement**, et **ne doit pas être confondue** avec la dette `_reel` du blocage d'absence prolongée (D14).

### D8 — Politique thermique pendant les Vacances
Hors préparation : la maison **peut chauffer librement**, **aucun plafond thermique** de confort n'est maintenu, le COOL est **interdit immédiatement** (D1). **Aucune contrainte matérielle documentée** ne justifie aujourd'hui un plafond estival permanent. Le besoin COOL réapparaît **à l'approche du retour prévu**.

### D9 — Préparation du retour de Vacances
Créée dans un **chantier distinct mais coordonné** (C21). Repose sur `binary_sensor.vacances_actives`, `input_datetime.fin_vacances`, une **fenêtre bornée** avant l'échéance, une **vérité opérationnelle de préparation à écrivain unique**, un **recalcul idempotent au boot**, une **politique fail-closed**, un **diagnostic dédié**, et la **présence réelle terminalement souveraine**. Pendant la préparation : les causes absence longue **et** Vacances sont **neutralisées ensemble** ; les autres blocages **restent pleinement applicables**.

### D10 — Consigne dédiée de préparation
Cible retenue : **consigne spécifique de préparation** (ID à attribuer), **troisième contexte thermique** (présence / absence / **préparation**), sans détourner la consigne de présence ni d'absence. Une simple levée vers la **consigne d'absence** est mentionnée comme **variante transitoire, écartée comme cible finale** (elle ne garantit pas le confort d'arrivée).

### D11 — Durée de préparation transitoire et réglable
Première version : durée de préparation **réglable**, **explicitement transitoire** — aucune vitesse de refroidissement suffisamment gouvernée n'existe aujourd'hui ; **aucune promesse** de température exacte à l'heure du retour ; évolution ultérieure possible sur observations terrain.

### D12 — Fin de fenêtre sans retour
À la fin de la fenêtre, sans retour réel : la préparation **s'arrête**, les causes de veto **redeviennent effectives**, le COOL **s'arrête** ; Arsenal **ne climatise pas indéfiniment** une maison vide sur la base d'une échéance dépassée.

### D13 — Modification de `fin_vacances`
Recul pendant préparation active : la préparation **s'arrête**, la nouvelle fenêtre est **recalculée**, réactivable à la nouvelle échéance ; la préparation précédente **ne consomme pas définitivement** le nouveau cycle temporel. Avance : fenêtre **recalculée immédiatement**, préparation possiblement **immédiatement éligible**. La **mémoire anti-répétition protège une fenêtre inchangée**, pas ne bloque une modification explicite de l'échéance.

### D14 — Dette `_reel` / garde opérateur
La dette autour de `input_boolean.clim_blocage_absence_prolongee_actif` et de la vérité `_reel` prévue par la doctrine des blocages reste **hors périmètre principal**. Consignée comme **lot/chantier séparé**. **Ne pas mélanger** au helper de durée, au veto immédiat Vacances, ni à la préparation. Elle est déjà tracée au backlog climatisation et à la vérification registre du 2026-06-17.

### D15 — Anticipation hors Vacances
**Différée.** Le seuil de 14 h réduira certains incidents de longue journée mais **ne garantit pas** le confort après un retour inconnu. Une vraie anticipation hors Vacances exigerait une **nouvelle observation de retour probable** et un **chantier séparé**.

---

## 3. Hiérarchie fonctionnelle cible (combinatoire, sans décision centrale)

| Rang | Régime | Couche | Réalisation |
|---|---|---|---|
| 1 | Présence réelle | terminale | présence ⇒ `vacances_actives off` + extinction off ⇒ veto tombe ; timer annulé |
| 2 | Préparation retour | exception d'autorisation | `preparation_cool_active` ⇒ neutralise `(absence_longue OR vacances)` |
| 3 | Vacances hors préparation | autorisation (cause métier) | `vacances_actives on` ⇒ veto immédiat |
| 4 | Absence longue non qualifiée | autorisation (cause temporelle) | `vacances_actives off` ET échéance dépassée ⇒ veto |
| 5 | Absence ordinaire | sélection consigne/seuils | consignes/seuils **absence** existants |

La hiérarchie reste **purement combinatoire** dans `binary_sensor.autorisation_clim_cool`.

---

## 4. Découpage retenu

- **C20 — Politique d'absence COOL** : veto immédiat Vacances, durée réglable, continuité physique/échéance recalculée, vérité intermédiaire du veto composite, diagnostics des causes, exposition du réglage. **Livrable indépendamment.**
- **C21 — Préparation du retour de Vacances** : fenêtre, vérité opérationnelle à écrivain unique, durée transitoire réglable, consigne dédiée, neutralisation bornée du veto composite, diagnostic, boot, modifications de `fin_vacances`, fin de fenêtre. **Dépend de C20.**
- **Lot séparé (D14)** : conformité blocage `_reel`/garde opérateur — **non intégré** aux deux chantiers.

Ordre Arsenal pour chaque chantier : **contrats → checkers → runtime → dashboard → validation terrain → clôture**.

---

## 5. Ce que ce document ne fait pas

- Ne rédige aucun contrat opposable (à venir dans les chantiers).
- Ne propose aucun ID d'entité.
- Ne modifie ni le rapport d'audit mergé, ni aucun runtime/contrat/UI/checker.
- Ne prétend pas que 14 h garantit le confort : 14 h **supprime le mécanisme causal du veto prématuré** dans certains scénarios ; le **résultat thermique reste à valider en terrain**.

---

*Note de décision — conception préalable, non normative. En cas de divergence future, les contrats font foi.*
