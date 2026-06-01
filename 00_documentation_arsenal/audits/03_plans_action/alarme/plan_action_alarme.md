# ==========================================================
# 🧭 ARSENAL — PLAN D'ACTION / FEUILLE DE ROUTE D'ASSAINISSEMENT
#     Domaine : Sécurité / Alarme
# ==========================================================

## 📌 Cadre

- **Source** : rapport d'audit officiel Alarme (HEAD `4336b1d`).
- **Nature** : feuille de route d'assainissement. Ce document **n'est pas** une proposition de correction : il décrit **quels chantiers** ouvrir, **dans quel ordre**, **avec quelles dépendances, difficultés, risques, prérequis et validations**.
- **Interdits respectés** : aucun code, aucun YAML, aucune correction prescrite. Les arbitrages restent **ouverts** (à trancher par le mainteneur).

### Échelles

- **Difficulté** (effort de conception + surface technique) : `faible` · `moyenne` · `élevée`.
- **Risque** (probabilité de régression ou de perturbation **en production** induite par l'exécution du chantier sur un système de sécurité vivant) : `faible` · `moyen` · `élevé`.
- Les chantiers portant un constat *À confirmer en runtime* sont **gatés** par une validation préalable (Phase 0) avant tout engagement de périmètre.

---

## 🌳 Regroupement par racine commune

Les 14 constats retenus se ramènent à **6 racines**, chacune devenant un chantier. Chaque constat est transformé en **lot** rattaché à un chantier.

| Chantier | Racine commune | Lots (constats) |
|----------|----------------|-----------------|
| **CH-1** | Sémantique des ouvrants d'entrée & confirmation d'intrusion | ALM-CRIT-1, ALM-CRIT-2, ALM-MIN-5 |
| **CH-2** | Cerveau décisionnel : autorité des helpers & propreté logique | ALM-IMP-2, ALM-MIN-4 |
| **CH-3** | Contextes humains & câblage des déclencheurs | ALM-IMP-1, ALM-MIN-1 |
| **CH-4** | Sirène & feedback sonore | ALM-IMP-3, ALM-MIN-2 |
| **CH-5** | Cohérence documentaire & nommage | ALM-DOC-1, ALM-DOC-2, ALM-MIN-3, ALM-MIN-6 |
| **CH-6** | Intégrité du flux clavier (PIN) | ALM-CRIT-3 |

---

## 🔗 Carte des dépendances

```
                 (validation runtime)        (validation runtime)
                          │                          │
   Phase 0  ──►  V1 course détection         V4 entité sirène / durée
                V2 contenu raison réel        V5 PIN réel (test)
                V3 présence en babysitting
                          │
                          ▼
   CH-2 (doctrine helpers) ──► CH-1 (refonte détection/intrusion)
        │                          │
        │                          └── coordination sur l'actionnement sirène ──► CH-4
        ▼
   CH-3 (contextes humains)        CH-6 (PIN)  ── indépendant
        │                                        │
        └──────────────┬───────────────┬─────────┘
                       ▼               ▼
                 CH-5 (cohérence documentaire — reflète le runtime final)
```

- **CH-2 ⟸ amont de CH-1 et CH-3** : la doctrine d'autorité et de nommage des helpers décisionnels doit être stabilisée **avant** de matérialiser un nouvel état (cible §9 « intrusion confirmée ») et **avant** d'ajouter une branche d'inhibition au cerveau. Les deux chantiers éditent le même cerveau → séquencer pour éviter les conflits.
- **CH-1 ⟂ CH-4** : couplage sur la chaîne d'actionnement de la sirène (le lot ALM-MIN-5 et la refonte §9 touchent le même chemin que le coupe-circuit). Coordination requise, pas dépendance stricte.
- **CH-1 dépend d'un domaine externe** : le moteur de réconciliation des contacts redondants (`contrats/ouvertures`). Toute décision sur la frontière des ouvrants d'entrée doit être cohérente avec ce domaine.
- **CH-5 ⟸ aval de CH-1/CH-2/CH-3/CH-4** pour les lots de réalignement contractuel (le contrat documente le runtime). Les lots d'hygiène pure (ALM-DOC-2, ALM-MIN-6) sont **indépendants** et parallélisables immédiatement.
- **CH-6 est indépendant** (chemin clavier isolé ; le badge n'est pas concerné).

---

## 🛠️ Chantiers

### CH-1 — Sémantique des ouvrants d'entrée & confirmation d'intrusion

- **Lots** : ALM-CRIT-1 (ouvrants d'entrée dans le chemin de déclenchement immédiat), ALM-CRIT-2 (garde de fin de délai excluant porte/garage), ALM-MIN-5 (double invocation sirène en fin de délai).
- **Objet (état cible visé)** : une **frontière unique et non ambiguë** entre détection immédiate et détection temporisée pour les ouvrants d'entrée ; un **garde de confirmation d'intrusion représentatif de la voie d'accès réelle** (porte/garage inclus) à l'expiration du délai ; un **chemin d'actionnement sirène unique** en cas d'intrusion confirmée.
- **Arbitrages à trancher** (sans réponse prescrite) : quel signal fait foi pour « intrusion confirmée » ? faut-il matérialiser cet état comme entité persistée (cible §9) ? quelle articulation entre signal permissif brut et contact réconcilié ?
- **Difficulté** : élevée — surface large, interaction avec le domaine ouvertures, refonte de la frontière de détection.
- **Risque** : élevé — modification de la détection d'un système de sécurité en production (faux positifs/négatifs possibles pendant la transition).
- **Prérequis documentaires** : `50_intrusion_detection.md` (dont §9), `51_ouvrants_entree.md` et les contrats renvoyés `contrats/ouvertures/{alarme.md, redondance.md}`, définition de `ouverture_qualifiee_maison` (sémantique aération/M5 à dissocier).
- **Validations runtime nécessaires** : **V1** — latence réelle de la réconciliation des contacts redondants vs chaîne timer (qui gagne la course à l'ouverture porte/garage) ; comportement observé d'une entrée légitime ; couverture effective de la détection de mouvement lorsque l'ouvrant est refermé.
- **Dépendances** : amont = CH-2 (doctrine helpers, si l'état « intrusion confirmée » devient un helper) ; latérale = CH-4 (chaîne sirène) ; externe = domaine ouvertures.

### CH-2 — Cerveau décisionnel : autorité des helpers & propreté logique

- **Lots** : ALM-IMP-2 (autorité/observabilité de `alarme_raison` ; raison décisionnelle jamais publiée), ALM-MIN-4 (variable et condition mortes dans le cerveau).
- **Objet (état cible visé)** : une **autorité d'écriture unique et explicite** pour chaque helper décisionnel (`decision`, `etat_cible`, `raison`) ; une **raison décisionnelle réellement observable** (notamment dans l'alerte d'incohérence) ; un cerveau **sans logique morte**.
- **Arbitrages à trancher** : `alarme_raison` doit-il rester un helper unique (raison décisionnelle) ou se scinder (raison décisionnelle vs dernier événement d'application) ? qui en est l'écrivain canonique ?
- **Difficulté** : moyenne — périmètre contenu (cerveau pur + deux scripts d'application + une automation d'alerte), mais nécessite un arbitrage doctrinal préalable.
- **Risque** : moyen — pas d'action de sécurité directe, mais impact sur l'observabilité du diagnostic d'incident.
- **Prérequis documentaires** : `30_decision_centrale.md`, `40_application_decision.md`, en-têtes des helpers `04_input_texts/alarme/{decision, etat_cible, raison}.yaml`, clause « Position A » (acceptation du warning rafales).
- **Validations runtime nécessaires** : **V2** — contenu réellement affiché par `alarme_raison` en exploitation et dans l'alerte d'incohérence ; confirmation que la raison riche n'apparaît jamais.
- **Dépendances** : aucune amont ; **amont de CH-1 et CH-3** (doctrine et propreté du cerveau avant extension).

### CH-3 — Contextes humains & câblage des déclencheurs

- **Lots** : ALM-IMP-1 (babysitting demi-intégré), ALM-MIN-1 (désynchronisation déclencheurs/entrées du cerveau pour le contexte visite).
- **Objet (état cible visé)** : une **position unique et explicite** sur le rôle des contextes humains (babysitting, visite) — soit inhibiteurs du cerveau, soit non neutralisants du diagnostic, mais **pas les deux à la fois** ; un **alignement strict** entre les déclencheurs de l'application et les entrées réellement consommées par le cerveau ; une **source de vérité unique** pour « visite active ».
- **Arbitrages à trancher** : le babysitting doit-il inhiber l'armement automatique ? quelle entité porte « visite active » (`presence_visiteur` vs `visite_en_cours`) ?
- **Difficulté** : moyenne — extension bornée de la logique décisionnelle + réalignement de déclencheurs.
- **Risque** : moyen — domaine adjacent à la sécurité (occupants vulnérables) ; une intégration mal calibrée peut sur- ou sous-inhiber l'armement.
- **Prérequis documentaires** : `99_hors_perimetre_et_extensions.md` (inhibiteurs), `96_diagnostic_blocage_armement_incoherence.md` (interdiction de dépendre du babysitting), `20/30_…` (contexte visite), contrat Présence (couverture).
- **Validations runtime nécessaires** : **V3** — `presence_famille_securite` couvre-t-elle réellement la présence d'un baby-sitter ? observation conjointe de `presence_visiteur` et `visite_en_cours` en exploitation.
- **Dépendances** : amont = CH-2 (cerveau stabilisé/nettoyé avant ajout d'une branche).

### CH-4 — Sirène & feedback sonore

- **Lots** : ALM-IMP-3 (coupe-circuit sirène : `delay` + entité fantôme), ALM-MIN-2 (double bip de désarmement + absence de garde mode test).
- **Objet (état cible visé)** : un **mécanisme d'extinction de sirène unique, explicite et résilient au redémarrage**, conforme à l'interdiction de gouvernance sur les `delay` de sûreté ; un **feedback sonore de désarmement à émetteur unique**, neutralisé en mode test.
- **Arbitrages à trancher** : l'extinction repose-t-elle sur un mécanisme HA dédié ou sur le seul paramètre de durée côté équipement ? quel est l'émetteur unique du feedback de désarmement ?
- **Difficulté** : faible à moyenne — périmètre localisé, mais l'actionneur est terminal (ne jamais laisser la sirène sans coupe-circuit).
- **Risque** : moyen — toute évolution doit garantir l'arrêt de la sirène en toutes circonstances, y compris après redémarrage.
- **Prérequis documentaires** : `70_sirene_actions_terminales.md`, `00_gouvernance_alarme.md` (interdiction `delay`), documentation Zigbee2MQTT de la sirène.
- **Validations runtime nécessaires** : **V4** — existence réelle de `switch.sirene_alarm` (découverte Z2M) ; valeur de `number.sirene_max_duration` vs `trigger_time: 180` ; comportement d'extinction observé en condition réelle et après redémarrage pendant sirène.
- **Dépendances** : latérale = CH-1 (chaîne d'actionnement sirène commune).

### CH-5 — Cohérence documentaire & nommage

- **Lots** : ALM-DOC-1 (décalage des en-têtes/chemins des contrats 20/30/40 ; contrat « application_decision » de fait absent), ALM-DOC-2 (notification persistante visiteur documentée mais inexistante), ALM-MIN-3 (durée de blocage déclarée 5 min / appliquée 3 min), ALM-MIN-6 (nom de fichier ↔ identifiant d'entité).
- **Objet (état cible visé)** : une **documentation reflétant fidèlement le runtime** (en-têtes et chemins alignés, contrat d'application restauré) ; une **cohérence déclaration ↔ application** pour la durée de blocage ; une **clause visiteur cohérente** avec la réalité ; une **hygiène de nommage** des fichiers du domaine.
- **Arbitrages à trancher** : la durée de blocage de référence est-elle 3 ou 5 minutes ? la notification visiteur doit-elle exister ou la clause être retirée ?
- **Difficulté** : faible — essentiellement documentaire et hygiène ; ALM-MIN-3 comporte une décision de valeur, ALM-MIN-6 un renommage de fichier (sans renommage d'entité).
- **Risque** : faible — pas d'impact sur l'actionnement de sécurité.
- **Prérequis documentaires** : contrats `20/30/40`, `60_delais_et_blocages.md`, `80_notifications_et_feedback.md`.
- **Validations runtime nécessaires** : revue de cohérence après stabilisation des chantiers amont (vérifier que chaque contrat décrit bien le runtime final).
- **Dépendances** : les lots de réalignement contractuel sont **en aval** de CH-1/CH-2/CH-3/CH-4 ; les lots ALM-DOC-2 et ALM-MIN-6 sont **indépendants** et parallélisables sans attendre.

### CH-6 — Intégrité du flux clavier (PIN)

- **Lots** : ALM-CRIT-3 (flux PIN vraisemblablement inopérant).
- **Objet (état cible visé)** : un **chemin clavier PIN fonctionnel de bout en bout**, depuis la saisie jusqu'au routage vers les scripts d'armement/désarmement, avec un contexte de clavier correctement transmis.
- **Arbitrages à trancher** : le constat est-il avéré en exploitation (préalable absolu avant d'engager le chantier) ?
- **Difficulté** : faible à moyenne — chemin localisé, mécanisme bien compris.
- **Risque** : faible à moyen — surface limitée au clavier PIN ; le badge n'est pas concerné. Reste un chemin d'accès de sécurité.
- **Prérequis documentaires** : en-tête normatif de `10_scripts/alarme/clavier.yaml`, mention clavier dans `50_intrusion_detection.md`.
- **Validations runtime nécessaires** : **V5** — test réel d'armement et de désarmement par code PIN sur les deux claviers, pour confirmer ou infirmer l'inopérance.
- **Dépendances** : aucune — exécutable en parallèle.

---

## 🚦 Validations runtime préalables (Phase 0 — porte d'entrée du plan)

Plusieurs chantiers sont **gatés** par une confirmation à chaud. Ces validations conditionnent le périmètre et la priorité.

| Réf | Validation | Gate sur |
|-----|------------|----------|
| **V1** | Course réconciliation contacts vs chaîne timer à l'ouverture porte/garage | CH-1 |
| **V2** | Contenu réel de `alarme_raison` et de l'alerte d'incohérence | CH-2 |
| **V3** | Couverture de présence pendant babysitting ; `presence_visiteur` vs `visite_en_cours` | CH-3 (escalade possible d'ALM-IMP-1) |
| **V4** | Existence de `switch.sirene_alarm` ; durée sirène vs `trigger_time` ; extinction post-reboot | CH-4 |
| **V5** | Test PIN réel sur les deux claviers | CH-6 |

> Tant que V1, V3, V4, V5 ne sont pas tranchées, le périmètre exact (et l'escalade éventuelle d'ALM-IMP-1) reste indéterminé.

---

## 📅 Séquencement recommandé (assainissement)

> Ordonnancement par dépendances et par priorité de sécurité — sans calendrier ni estimation de charge.

1. **Phase 0 — Constatation** : exécuter V1 à V5. Figer les périmètres et confirmer/infirmer les constats *À confirmer en runtime*.
2. **Phase 1 — Sécurité fonctionnelle** : **CH-6** (chemin court, indépendant) et préparation de **CH-1** (le plus structurant et le plus risqué ; à instruire avec soin une fois V1 connue).
3. **Phase 2 — Socle décisionnel** : **CH-2** (doctrine helpers + nettoyage), prérequis de la suite ; puis **CH-3** (contextes humains).
4. **Phase 3 — Actionnement** : **CH-4** (sirène), en coordination avec la chaîne d'actionnement issue de CH-1.
5. **Phase 4 — Cohérence documentaire** : **CH-5**, en aval, pour réaligner les contrats sur le runtime stabilisé (les lots d'hygiène ALM-DOC-2 / ALM-MIN-6 peuvent démarrer dès la Phase 0).

---

## 🧾 Tableau de synthèse des chantiers

| Chantier | Racine | Lots | Difficulté | Risque | Dépend de | Gate runtime |
|----------|--------|------|:----------:|:------:|-----------|--------------|
| CH-1 | Ouvrants d'entrée & intrusion | CRIT-1, CRIT-2, MIN-5 | élevée | élevé | CH-2 (doctrine), domaine ouvertures, ⟂ CH-4 | V1 |
| CH-2 | Cerveau : autorité & propreté | IMP-2, MIN-4 | moyenne | moyen | — | V2 |
| CH-3 | Contextes humains & déclencheurs | IMP-1, MIN-1 | moyenne | moyen | CH-2 | V3 |
| CH-4 | Sirène & feedback | IMP-3, MIN-2 | faible-moyenne | moyen | ⟂ CH-1 | V4 |
| CH-5 | Cohérence documentaire & nommage | DOC-1, DOC-2, MIN-3, MIN-6 | faible | faible | CH-1/2/3/4 (lots de réalignement) | revue finale |
| CH-6 | Flux clavier (PIN) | CRIT-3 | faible-moyenne | faible-moyen | — | V5 |

---

*Fin de la feuille de route d'assainissement. Aucun code, aucun YAML, aucune correction n'est proposé : ce document fixe les chantiers, leurs racines, dépendances, difficultés, risques, prérequis documentaires et validations runtime. Les arbitrages restent ouverts.*
