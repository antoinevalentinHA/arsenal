# ARSENAL — MÉCANISME DE CONTEXTE THERMIQUE
## Vacances — Adaptation consigne réduite

**Statut :** Mécanisme de paramétrage contextuel  
**Date :** 2026-04-14

---

## Rôle

Adapter temporairement la consigne réduite chauffage lorsque le contexte Vacances est effectivement actif **et que la saison courante est une saison de chauffe**.

Ce mécanisme sauvegarde la valeur courante de `input_number.chauffage_consigne_reduite`, applique la valeur de `input_number.chauffage_consigne_vacances`, puis restaure la valeur initiale à la sortie du contexte Vacances.

La surcote Vacances vise exclusivement la protection du bâti pendant les périodes de chauffe. En été, le chauffage ne chauffe pas : la surcote n'a aucun effet thermique et ne fait que dégrader la lisibilité de la consigne réduite affichée. Elle est donc conditionnée à la saison (cf. § *Conditionnement saisonnier*).

---

## Nature

- Application de contexte thermique
- Surcouche de paramétrage
- Mécanisme réversible
- Mécanisme idempotent
- Aucune logique décisionnelle autonome

---

## Principe

Le contexte Vacances ne modifie pas la nature de la décision chauffage.

Le moteur chauffage continue à raisonner en `confort` / `réduite`.

Seule la valeur numérique portée par `input_number.chauffage_consigne_reduite` est temporairement adaptée pendant la durée effective du contexte Vacances.

---

### Interaction avec le domaine Chauffage

La modification de `input_number.chauffage_consigne_reduite` peut entraîner,
via les mécanismes du domaine Chauffage, une réapplication de la consigne
actuellement active.

Cette réapplication est réalisée exclusivement par les automatismes du
domaine Chauffage et n’est jamais pilotée directement par le présent
mécanisme.

---

## Entités concernées

| Rôle | Entité |
|------|--------|
| Vérité métier amont | `binary_sensor.vacances_actives` |
| Contexte saisonnier amont | `input_select.saison` |
| Consigne nominale | `input_number.chauffage_consigne_reduite` |
| Consigne contextuelle | `input_number.chauffage_consigne_vacances` |
| Sauvegarde | `input_number.chauffage_consigne_reduite_sauvegarde` |

`input_select.saison` est consommé en lecture seule comme source de vérité métier unique. Toute valeur autre que `Été` (y compris `unknown`/`unavailable`) laisse le comportement nominal actif — fail-safe orienté vers la protection du bâti.

`input_number.chauffage_consigne_reduite_sauvegarde` doit avoir `min: 0`. La valeur `0` est une sentinelle de non-sauvegarde — elle n'est jamais interprétée comme une consigne valide. Une sauvegarde est considérée valide si et seulement si sa valeur est strictement positive.

---

## Invariants

- Aucune modification hors contexte Vacances actif
- Aucune décision chauffage produite
- Aucune interaction avec le boiler bridge
- Aucune publication MQTT
- Aucune modification de `input_select.chauffage_dernier_mode_decide`
- Toute application doit avoir un chemin de restauration explicite
- Aucune application de la consigne Vacances sans sauvegarde préalable effective
- Aucune resauvegarde d'une valeur déjà adaptée
- Aucune surcote Vacances en vigueur pendant la saison `Été`

---

## Entrée en contexte Vacances

Déclencheur : `binary_sensor.vacances_actives` devient `on`, ou réconciliation au démarrage avec Vacances déjà actives.

0. Évaluer la saison (`input_select.saison`) :
   - si saison `Été` : appliquer le § *Conditionnement saisonnier* (garantir l'absence de surcote), puis arrêter — les étapes suivantes ne s'appliquent pas
   - sinon : poursuivre le comportement nominal ci-dessous
1. Vérifier que la consigne réduite courante est disponible et valide
2. Vérifier que la consigne Vacances est disponible et valide
3. Vérifier l'état de la sauvegarde (`chauffage_consigne_reduite_sauvegarde`) :
   - si aucune sauvegarde valide (= `0`) : sauvegarder la consigne réduite courante, puis appliquer la consigne Vacances
   - si sauvegarde valide existante (> `0`) : ne pas écraser la sauvegarde — réappliquer la consigne Vacances si `chauffage_consigne_reduite` ≠ `chauffage_consigne_vacances`, sinon abstention

---

## Conditionnement saisonnier

La surcote Vacances n'est en vigueur que pendant les saisons de chauffe. En saison `Été`, le mécanisme garantit l'**absence** de surcote :

- si une sauvegarde valide existe (`chauffage_consigne_reduite_sauvegarde > 0`) : restaurer `input_number.chauffage_consigne_reduite` depuis la sauvegarde, puis remettre la sauvegarde à `0` (même effet qu'une sortie de contexte) ;
- sinon (sauvegarde `= 0`) : abstention, aucune surcote n'était en vigueur ;
- si la sauvegarde est indisponible (`unknown`/`unavailable`) : abstention stricte, trace locale.

Ce conditionnement s'évalue à l'entrée en contexte Vacances et lors de la réconciliation au démarrage. La réconciliation au démarrage suffit à ramener la consigne réduite à sa valeur nominale lorsqu'une surcote héritée d'une saison de chauffe subsiste à l'entrée en été.

> **Limitation connue (assumée) :** un changement de saison survenant *pendant* un contexte Vacances actif, sans redémarrage ni nouvelle entrée en contexte, n'est pas réévalué immédiatement. L'impact est nul en pratique : la transition vers l'été laisse une surcote sans effet thermique (le chauffage ne chauffe pas), et la prochaine réconciliation au démarrage la corrige.

---

## Sortie du contexte Vacances

Déclencheur : `binary_sensor.vacances_actives` devient `off`, ou réconciliation au démarrage avec Vacances inactives.

1. Vérifier qu'une sauvegarde valide existe (`chauffage_consigne_reduite_sauvegarde > 0`) — si absente ou invalide : abstention de restauration, trace locale autorisée
2. Restaurer `input_number.chauffage_consigne_reduite` depuis la sauvegarde
3. Remettre `input_number.chauffage_consigne_reduite_sauvegarde` à `0`

---

## Robustesse

- Le mécanisme est sans dérive au redémarrage
- Une réexécution ne corrompt pas la sauvegarde
- Aucune restauration n'invente une valeur
- En cas de sauvegarde absente ou invalide : abstention stricte de restauration, trace locale autorisée

---

## Interdictions absolues

- Forcer `confort` via ce mécanisme
- Appeler `chauffage_appliquer_consigne`
- Injecter une logique métier locale
- Utiliser `input_select.mode_maison` comme source de vérité à la place de `binary_sensor.vacances_actives`
- Appliquer la consigne Vacances sans sauvegarde préalable effective
- Restaurer une valeur arbitraire

---

## Doctrine

Vacances adapte la consigne réduite.  
Vacances ne change pas le moteur chauffage.  
La surcote Vacances protège le bâti en saison de chauffe, pas en été.
