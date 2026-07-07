<!--
Template de Pull Request Arsenal.
Remplir les sections utiles, supprimer les lignes sans objet.
Rappel doctrine : le backend décide, l'UI observe — jamais l'inverse.
-->

## Intention

<!-- Que change cette PR, et pourquoi ? Une intention, pas un journal de commits. -->

## Domaine(s) concerné(s)

<!-- Domaine(s) métier ou transverse(s) touché(s). Lier le contrat de référence si applicable. -->

## Couche(s) touchée(s)

- [ ] **Décision** (template sensors, helpers, admissibilité)
- [ ] **Action** (automatisations, scripts souverains, exécutants bornés)
- [ ] **Diagnostic / observabilité** (vues diagnostic, `recorder.yaml`)
- [ ] **UI** (dashboards Lovelace)
- [ ] Documentation / contrat
- [ ] Outillage / CI

## Impact runtime

<!-- Effet concret sur le système en production : nouveaux états, commandes physiques,
     entités enregistrées, notifications, activation/désactivation d'automatisations.
     « Aucun impact runtime » est une réponse valide et attendue pour un changement
     purement documentaire. -->

## Conformité à la doctrine

- [ ] La séparation **décision / action / diagnostic / UI** est respectée (l'UI observe, elle ne décide pas).
- [ ] **Aucun ID inventé** : toute entité référencée existe réellement.
- [ ] **Aucun renommage d'entité** non justifié et non tracé.
- [ ] Toute nouvelle **exposition externe** (MQTT, API, notification) est une décision explicite.
- [ ] Le changement ne contredit pas le **contrat** du domaine (sinon, le contrat est mis à jour dans la même PR).

## Contrôles

- [ ] CI verte (validation, doctrine, contrats concernés).
- [ ] Checkers / contrats du domaine passés localement le cas échéant.

## Notes

<!-- Points de vigilance, limites connues, suivi éventuel. -->
