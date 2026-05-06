# ARSENAL — MÉCANISME DE CONTEXTE THERMIQUE
## Vacances — Adaptation consigne réduite

**Statut :** Mécanisme de paramétrage contextuel  
**Date :** 2026-04-14

---

## Rôle

Adapter temporairement la consigne réduite chauffage lorsque le contexte Vacances est effectivement actif.

Ce mécanisme sauvegarde la valeur courante de `input_number.chauffage_consigne_reduite`, applique la valeur de `input_number.chauffage_consigne_vacances`, puis restaure la valeur initiale à la sortie du contexte Vacances.

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
| Consigne nominale | `input_number.chauffage_consigne_reduite` |
| Consigne contextuelle | `input_number.chauffage_consigne_vacances` |
| Sauvegarde | `input_number.chauffage_consigne_reduite_sauvegarde` |

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

---

## Entrée en contexte Vacances

Déclencheur : `binary_sensor.vacances_actives` devient `on`, ou réconciliation au démarrage avec Vacances déjà actives.

1. Vérifier que la consigne réduite courante est disponible et valide
2. Vérifier que la consigne Vacances est disponible et valide
3. Vérifier l'état de la sauvegarde (`chauffage_consigne_reduite_sauvegarde`) :
   - si aucune sauvegarde valide (= `0`) : sauvegarder la consigne réduite courante, puis appliquer la consigne Vacances
   - si sauvegarde valide existante (> `0`) : ne pas écraser la sauvegarde — réappliquer la consigne Vacances si `chauffage_consigne_reduite` ≠ `chauffage_consigne_vacances`, sinon abstention

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
