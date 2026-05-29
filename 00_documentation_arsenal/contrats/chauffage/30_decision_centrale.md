# ARSENAL — Contrat Normatif Central
## Chauffage — Décision Centrale V3

**Statut :** Contrat normatif central — opposable  
**Rôle :** Cerveau métier du domaine Chauffage · Point d'entrée canonique de décision  
**Subordonné à :** `contrats/chauffage/00_gouvernance_chauffage.md`  
**Complémentaire de :** `20_triggers_decisionnels.md` · `70_autorisation_thermostat.md` · `80_table_decision_canonique.md`  
**Références boiler :** `contrats/boiler/CONTRAT_BOILER_SOCLE_TRANSACTIONNEL.md` · `outils_externes/boiler_pi/AUDIT_CHAINE_MQTT_ACK_ECS.md`  
**Date :** 2026-04-07

---

## 0. Principes normatifs fondamentaux

La Décision Centrale est un système de décision souverain soumis aux invariants suivants :

- aucune action sans cause explicite
- aucune reprise par simple levée d'un blocage
- aucune oscillation de régime autorisée
- abstention par défaut en absence de besoin valide
- une autorisation n'est jamais une décision

Toute implémentation doit respecter ces principes indépendamment de sa forme technique.

---

## 1. Autorité et opposabilité

Ce document définit l'algorithme métier officiel de décision thermique du sous-système Chauffage Arsenal.

Il est **opposable** à toute implémentation : scripts, automatismes, capteurs décisionnels, interfaces utilisateur.

Toute divergence entre ce contrat et le YAML constitue une erreur critique de conception.

---

## 2. Rôle fondamental

La Décision Centrale est :

- l'unique autorité habilitée à décider un changement de programme chauffage,
- le point de convergence de toutes les causes thermiques et contextuelles,
- la source officielle de toute intention d'application,
- le seul appelant légitime de `script.chauffage_appliquer_consigne`.

Elle peut uniquement : ordonner `comfort`, ordonner `reduced`, ou refuser volontairement toute action.

Elle ne peut jamais : régler une consigne, produire une hypothèse thermique, accéder à une couche matérielle, produire une décision implicite.

### Nature de la décision

La décision produite est une **intention de changement de régime**. Elle ne constitue pas une preuve d'exécution.

L'exécution réelle est confirmée uniquement par la couche transactionnelle aval (ACK boiler).

---

## 3. Périmètre couvert

**Inclus :** arbitrage confort / sobriété, hiérarchie des causes métier, production d'une décision explicite, abstention volontaire, traçabilité métier.

**Exclu :** calcul primaire des besoins thermiques, estimation d'inertie, réglage des consignes, pilotage matériel, logique UI.

**Note :** ce script consomme des vérités amont déjà calculées par des capteurs contractuels (`sensor.chauffage_autorisation_cible`, `binary_sensor.chauffage_autorise_systeme`, `binary_sensor.fenetre_ouverte_maison_avec_delai`, `input_boolean.pre_confort_actif_calcule`). Il n'en est pas la source.

---

## 4. Hiérarchie officielle des causes (doctrine)

Aucune cause de niveau inférieur ne peut contredire un niveau supérieur.

### Niveau 0 — Override opérateur

`input_boolean.mode_confort_chauffage`

Impose `comfort`. Écrase toute logique métier inférieure, sans contourner les gardes techniques non négociables (bridge offline, idempotence G5).

### Niveau 1 — Interdictions système

`binary_sensor.chauffage_autorise_systeme`

**Catégorie réservée sans cause active depuis CH-2 (désintrication D2, Option A).** Le capteur est un hook réservé, constant `on` : aucune interdiction de sécurité système n'est actuellement composée, donc cette branche n'est pas évaluable et la raison `chauffage_non_autorise` n'est plus émise. La sémantique reste posée pour une future cause Niveau 1 : si elle existe, elle imposera `reduced` en stop hiérarchique (aucune autre cause évaluée). Le blocage post-aération relève du Niveau 2 (`blocage_aeration_en_cours`), jamais de ce niveau.

### Niveau 2 — Contextes majeurs

Aération en cours confirmée, blocage aération, fenêtres ouvertes (avec délai), mode maison = Vacances, poêle actif.

Effets :
- aération confirmée / blocage aération / fenêtres ouvertes / poêle actif → `reduced`
- mode maison = Vacances → `reduced`, **sauf exception normative explicite** : pré-confort retour vacances actif (`input_boolean.pre_confort_actif_calcule`) → `comfort`

### Niveau 3 — Confort d'opportunité

**3a — Présence réelle :** `binary_sensor.presence_famille_unifiee` → délégation à `sensor.chauffage_autorisation_cible`.

Valeurs possibles : `comfort`, `neutre`, `reduced`.

La présence n'est jamais une décision — elle délègue. L'autorisation `neutre` produit une abstention stricte.

**3b — Inhibition géofencing :** en absence de présence réelle, `input_boolean.chauffage_inhibition_geofencing` peut imposer `comfort` comme protection thermique (raison `stabilisation_absence`). Toute interdiction de niveau 1 ou 2 l'écrase immédiatement.

**3c — Défaut :** `reduced`.

---

## 5. Règles décisionnelles fondamentales

### Abstention (principe cardinal)

L'abstention est l'état nominal du système. Une décision n'est valide que si une cause métier identifiable la fonde, qu'aucune interdiction supérieure ne s'y oppose, et qu'aucun garde-fou d'abstention ne l'annule. Sinon : le système refuse d'agir.

> La Décision Centrale ne cherche jamais à agir. Elle cherche à ne pas agir tant que cela n'est pas nécessaire.

### Statut du mode `neutre`

Le mode `neutre` n'est pas un régime thermique. Il représente une absence de décision.

Conséquences : il ne déclenche aucune action, il ne modifie aucun état, il formalise une abstention volontaire du système.

Il constitue un état valide et stable.

### Hystérésis décisionnelle

La levée d'un blocage ne constitue jamais, à elle seule, un motif suffisant de reprise. Une reprise en `comfort` n'est possible que si la réévaluation métier complète le justifie indépendamment. Respect strict de l'inertie thermique. Zéro oscillation autorisée.

---

## 6. Garde-fous d'abstention (doctrine)

Aucune action métier n'est produite si : programme inconnu, autorisation = `neutre`, mode déjà actif, anti-rebond actif.

> Une autorisation sans besoin produit une abstention stricte.

La disponibilité du bridge (`binary_sensor.boiler_bridge_online`) constitue un garde-fou d'exécution distinct, évalué après la décision métier. Voir §7.

---

## 7. Garde d'exécution — Disponibilité du système

La disponibilité du système d'exécution est une condition préalable à toute exécution descendante. Elle est évaluée via `binary_sensor.boiler_bridge_online`.

Règles :

- cette garde ne participe pas à la décision métier,
- elle conditionne uniquement la capacité d'exécution,
- elle est évaluée après la finalisation complète de `desired_mode` et `reason`,
- elle est non contournable.

Conséquence : une décision valide peut être produite mais non exécutée. La décision et l'exécution sont deux événements distincts.

---

## 8. Séquence d'exécution

```
START
  │
  ├─ G1  Anti-rebond actif ET pas override ? → STOP
  ├─ SET variables : prog_actuel / desired_mode / reason
  ├─ G3  Programme unknown ET pas override ? → STOP
  ├─ G4  desired_mode == neutre ? → STOP
  ├─ G5  desired_mode == prog_actuel ? → STOP
  ├─ G2  Bridge offline ? → STOP
  │
  └─ EXÉCUTION
       → script.chauffage_appliquer_consigne (consigne, raison)
       → timer.chauffage_geoloc_antirebond (start)
```

---

## 9. Gardes

| Garde | Condition | Contournable par override |
|-------|-----------|--------------------------|
| G1 | Anti-rebond actif | Oui |
| G3 | Programme unknown | Oui |
| G4 | `desired_mode == neutre` | Non |
| G5 | `desired_mode == prog_actuel` | Non |
| G2 | Bridge offline | Non |

---

## 10. Traçabilité métier

Chaque décision produit : une action observable, une raison métier explicite, un logbook cohérent.

La raison est calculée localement et transmise à `chauffage_appliquer_consigne` — elle n'est jamais recalculée en aval.

| Contexte | Raison |
|----------|--------|
| Override opérateur | `confort_force` |
| Système non autorisé (catégorie réservée — non émise depuis CH-2) | `chauffage_non_autorise` |
| Aération en cours confirmée | `aeration_en_cours` |
| Blocage aération actif | `blocage_aeration_en_cours` |
| Fenêtre ouverte (avec délai) | `fenetre_ouverte_maison` |
| Mode vacances + pré-confort actif | `pre_confort_vacances` |
| Mode vacances (sans pré-confort) | `mode_maison_vacances` |
| Poêle actif | `poele_actif` |
| Présence + cible = comfort | `besoin_thermique` |
| Présence + cible = neutre | `presence_on` |
| Présence + cible = reduced | `confort_suffisant` |
| Inhibition géofencing | `stabilisation_absence` |
| Absence (défaut) | `absence` |

---

## 11. Notifications (invariant UI)

- Jamais dans un script `mode: restart`.
- Toujours via automation dédiée, idempotente et reconstructible après redémarrage.

---

## 12. Interdictions formelles

La Décision Centrale ne doit jamais : appeler directement le matériel, modifier une consigne, recalculer une vérité matérielle, court-circuiter la hiérarchie.

---

## 13. Invariants non négociables

- Une seule décision à la fois — mode `restart`
- Zéro appel inutile — G5 idempotence
- Zéro oscillation — anti-rebond systématique
- Normalisation locale robuste de `prog_actuel` avec repli explicite sur `unknown`
- Zéro reprise par simple levée de blocage
- Zéro décision sans cause référencée

Toute violation constitue une régression critique et une rupture de gouvernance.

---

## 14. Portée et stabilité

Ce contrat est central, stable long terme, versionné explicitement, et opposable à toute implémentation.

Il constitue le **cerveau normatif officiel du Chauffage Arsenal V3**.
