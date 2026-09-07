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

## Déploiement

<!-- Merger sur `main` ne met à jour ni le clone runtime (`/homeassistant/`, doctrine
     `architecture/03_doctrines/git.md` ; `/config` est l'alias runtime Home Assistant
     de cette même racine, cf. `check_lovelace_includes_contracts.py`), ni ce qui est
     chargé dans Home Assistant. Quatre états distincts : merge Git → mise à jour du
     clone runtime → application effective dans Home Assistant → validation terrain.
     Déclarer explicitement l'absence de déploiement plutôt que de laisser la section
     vide. -->

- [ ] **Déploiement runtime requis**
- [ ] **Déploiement runtime : aucun** (le changement peut être présent dans le clone
      après merge, mais n'exige aucune application au runtime Home Assistant et n'en
      modifie pas le comportement fonctionnel — doc, CI, outillage)

<!-- Si déploiement requis : opérations nommées et vérifiables. Une formulation vague
     (« pull sur HA », « reload si nécessaire », « redémarrer au besoin », « vérifier
     que ça marche ») laisse cette section incomplète — et visible comme telle. -->

**Cible du déploiement :** <!-- par défaut le dépôt `/homeassistant/` (= `/config` côté
alias runtime HA) ; préciser si un autre composant est concerné (ex. configuration
Zigbee2MQTT, pont satellite) -->

**Fichiers / composants concernés :**

**Ordre des opérations**, si plusieurs :

**Mode d'application Home Assistant** — choisir le mode **le moins intrusif** qui
suffit à appliquer correctement le changement, pas le plus commode :
- [ ] Aucun reload nécessaire
- [ ] Reload ciblé — préciser l'élément concerné (ex. `automation.reload`,
      `script.reload`, ou tout autre reload de domaine nommé sous Outils de
      développement > YAML) :
- [ ] Reload d'un domaine ou d'une intégration — préciser lequel :
- [ ] Redémarrage complet Home Assistant — **à ne cocher que si aucun reload ciblé ou
      de domaine/intégration ne suffit ; justifier pourquoi ci-dessous, jamais par
      commodité ou par défaut :**
- [ ] Autre mécanisme (préciser — ex. contenu YAML d'un dashboard Lovelace : ouvrir le
      dashboard concerné → menu ⋮ → Actualiser ; ressource JS Lovelace : hard reload
      navigateur pour la cohérence du cache (`contrats/ressources_lovelace.md` INV-11) ;
      déclenchement manuel d'une automatisation sans déclencheur ; `deploy.sh` sur un
      pont satellite) :

**Précondition(s) éventuelle(s) :**

**Action(s) manuelle(s) éventuelle(s) après déploiement :**

**Validation post-déploiement attendue :** <!-- entité(s) précise(s) et état attendu,
ex. « recharger X, puis vérifier que l'entité Y passe à Z » -->

**Rollback**, si le changement présente un risque opérationnel : <!-- sinon « non
applicable » -->

## Conformité à la doctrine

- [ ] La séparation **décision / action / diagnostic / UI** est respectée (l'UI observe, elle ne décide pas).
- [ ] **Aucun ID inventé** : les IDs d'automatisations sont pré-attribués, et toute entité référencée existe réellement.
- [ ] **Aucun renommage d'entité** non justifié et non tracé.
- [ ] Toute nouvelle **exposition externe** (MQTT, API, notification) est une décision explicite.
- [ ] Le changement ne contredit pas le **contrat** du domaine (sinon, le contrat est mis à jour dans la même PR).

## Contrôles

- [ ] CI verte (validation, doctrine, contrats concernés).
- [ ] Checkers / contrats du domaine passés localement le cas échéant.

## Notes

<!-- Points de vigilance, limites connues, suivi éventuel. -->
