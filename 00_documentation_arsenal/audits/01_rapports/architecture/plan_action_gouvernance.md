# Plan d'action de gouvernance — Arsenal

**Périmètre** : dépôt `antoinevalentinHA/arsenal`. Dérivé de l'audit consolidé (référence).
**Base d'analyse** : clone local, HEAD `899c172` (2026-06-04).
**Nature** : plan d'action raisonné en coût/bénéfice. **Sélectif, non exhaustif** : il vise les rares travaux à valeur réelle, pas l'homogénéisation du dépôt.
**Méthode complémentaire** : au-delà de l'audit consolidé, exécution locale de validateurs et inspection des déclencheurs CI pour fermer certains angles morts (§1).

---

## 1. Faits nouveaux établis (mise à jour des angles morts de l'audit)

L'audit consolidé signalait que les 62 validateurs n'avaient pas été exécutés et que « gouvernance = outillage, pas efficacité ». Vérifications faites :

1. **Les validateurs se déclenchent à chaque `push` et `pull_request`** (pas de filtre `paths` pour l'échantillon vmc/alarme/batteries) et **passent** au HEAD courant (`check_vmc` exit 0, `check_alarme` exit 0).
2. **Ils sont substantiels, non triviaux.** `check_batteries` vérifie la dérivation `expand(group.batteries)`, l'`unique_id`, un seuil à 28 %. `check_alarme` vérifie des invariants nommés (C2/C3/C4, K1/K2/K3 rattachés au chantier CH-6). → L'angle mort « outillage ≠ efficacité » est **largement refermé** pour les domaines (E).
3. **Distinction critique sur le moteur chauffage.** Les **136 tests** portent sur des **fixtures synthétiques** : ils valident *l'outil* (`tools/arsenal_ci/tests/`), pas la configuration réelle. L'étage de lint sur la **vraie config** ne couvre aujourd'hui **qu'un fichier** : `12_template_sensors/chauffage/autorisation.yaml` (liste `CONFIGS` du workflow, déploiement échelonné assumé : « À étendre fichier par fichier, jamais par glob implicite »).
4. **Aucun run `schedule:`** : la validation est déclenchée par les commits, pas périodiquement.
5. **Exemple de chemin périmé** dans `tools/arsenal_ci/README.md` (`packages/chauffage/autorisation.yaml`, `packages/` est absent) ; le workflow réel pointe, lui, vers un fichier existant.

Ces faits font qu'**aucune action du type « mettre en place / exécuter les validateurs » n'est justifiée** : ils existent, tournent et passent. La valeur se situe ailleurs.

---

## 2. Grille de lecture (préalable à toute action)

Chaque situation est qualifiée avant d'envisager une action :

- **Manque démontré** — un fait du dépôt établit une absence, et cette absence porte sur du code qui **agit** (pas de la perception passive).
- **Risque plausible** — une situation où une divergence silencieuse est concevable, sans preuve qu'elle existe.
- **Choix d'architecture** — une situation cohérente avec une doctrine explicite du dépôt ; **non actionnable** (la toucher serait de l'homogénéisation).

Principe directeur (repris des contraintes) : un domaine **n'a pas vocation** à atteindre uniformément contrat + audit + CI. L'absence d'artefact n'est un problème **que** si elle laisse non gouverné du code qui agit de façon non triviale.

---

## 3. Catalogue d'actions

### Catégorie 1 — Forte valeur, faible risque

#### A1. Étendre la couverture *config réelle* du moteur chauffage
- **État actuel** : moteur éprouvé (136 self-tests verts), mais lint de la vraie config limité à 1 fichier (`autorisation.yaml`) par déploiement échelonné voulu.
- **Qualification** : risque plausible (la force « 136 tests » peut être confondue avec une large couverture de la config, alors qu'elle couvre 1 fichier).
- **Intérêt** : le chauffage est le domaine le plus contractualisé **et** le plus sensible (régulation thermique). Le mécanisme d'extension existe déjà et est prouvé.
- **Bénéfice attendu** : convertir une validation aujourd'hui quasi-symbolique sur la config en couverture réelle, sur le domaine où une régression silencieuse coûte le plus.
- **Coût estimé** : faible et incrémental — ajouter des entrées à la liste `CONFIGS`, fichier par fichier, exactement comme le design le prévoit.
- **Priorité** : **haute.**
- **Justification** : meilleur rapport valeur/coût du dépôt — on capitalise sur l'actif le plus mûr (le moteur) pour combler l'écart le plus conséquent (couverture config du domaine critique), sans rien construire de neuf.

#### A2. Contrat minimal (1 fichier) pour `reveils` et `electromenager`, sous condition
- **État actuel** : catégorie (A), implémentation qui **agit** (6 et 5 automatisations) sans aucun contrat (0 occurrence vérifiée).
- **Qualification** : manque démontré **partiel et conditionnel**.
- **Intérêt** : c'est le seul cas où du code agissant échappe à la « règle d'or » du dépôt.
- **Bénéfice attendu** : rendre explicite la décision encodée dans ces automatisations (déclencheurs, plages, interactions présence/absence).
- **Coût estimé** : faible — un contrat racine court chacun, sur le modèle compact existant (`vmc.md`), **sans** dossier ni CI.
- **Priorité** : moyenne.
- **Justification** : à n'entreprendre **que si** ces automatisations encodent une décision non triviale. Si un `reveils` se réduit à une alarme horaire, le contrat n'apporte rien et l'action **ne doit pas** être menée. La condition fait partie de l'action.

### Catégorie 2 — Forte valeur, mais décision d'architecture requise

#### B1. Statuer sur la validation du domaine `pannes`
- **État actuel** : catégorie (B) — contrats riches (`pannes/internet`, `pannes/secteur`, 9 fichiers) **mais aucun validateur** ; l'implémentation (`11_automations/panne/`, 7 automatisations) **agit en condition de panne** (remédiation réseau, bascule chauffage/ECS).
- **Qualification** : risque plausible, **plus élevé que les autres (B)** car c'est du code de chemin d'échec.
- **Intérêt** : une divergence contrat↔implémentation est la plus dommageable précisément là où le système agit en situation dégradée et rarement testée en conditions réelles.
- **Bénéfice attendu** : verrouiller les invariants de remédiation (ce que le système fait/ne fait pas pendant une panne).
- **Coût estimé** : moyen — définir les invariants automatisables et écrire un validateur ; complexité accrue par le caractère inter-domaines (chauffage/ECS pendant la panne).
- **Priorité** : moyenne-haute, **conditionnée à une décision d'architecture** (quels invariants sont opposables ?).
- **Justification** : valeur réelle, mais le périmètre exact relève d'un arbitrage, pas d'une exécution mécanique.

#### B2. Décider d'une re-validation périodique (`schedule:`)
- **État actuel** : validation déclenchée uniquement par les commits ; aucune exécution périodique.
- **Qualification** : risque plausible (dérive **externe** : une mise à jour HA/intégration renommant une entité ne casse les invariants qu'au prochain push, potentiellement longtemps après).
- **Intérêt** : capter une classe de régressions qui n'a pas de commit déclencheur côté dépôt.
- **Bénéfice attendu** : détection plus tôt d'un décrochage entre la config gouvernée et l'environnement HA réel.
- **Coût estimé** : faible techniquement, mais **change la philosophie CI** (événementielle → périodique) — d'où la décision d'architecture.
- **Priorité** : moyenne.
- **Justification** : le bénéfice dépend de la fréquence réelle des renommages externes ; à arbitrer selon l'expérience opérationnelle de l'auteur, que cet audit ne possède pas.

### Catégorie 3 — Optionnelles

| Action | État | Bénéfice | Coût | Priorité |
|---|---|---|---|---|
| **C1.** Acter par une note courte que le statut (B) « gouverné non automatisé » (sante, imprimerie, bluetti, mouvements) est **légitime** | risque de mauvaise lecture future | évite de retraiter ces domaines comme des manques | très faible | basse |
| **C2.** Corriger l'exemple de chemin périmé dans `tools/arsenal_ci/README.md` | défaut documentaire mineur | exactitude de la doc d'outil | trivial | basse |
| **C3.** Contrat pour `statistiques`/`bluetti`/`mouvements` **uniquement s'ils acquièrent une logique de décision** | perception pure aujourd'hui | nul tant qu'ils restent passifs | — | différé |

### Catégorie 4 — À ne PAS entreprendre (recommandation explicite)

- **D1. Ne pas créer de contrats-parapluie `system` ou `meteo`.** Leur gouvernance est **distribuée** (transverse pour system, par axe pour meteo) — choix d'architecture cohérent avec le pattern 1↔1↔1. Un contrat faîtier ajouterait du coût et réduirait la granularité qui fait la valeur du modèle.
- **D2. Ne pas ajouter contrat/CI aux domaines de perception passive** (`statistiques`, `babyphone`). Il n'y a aucune décision à gouverner ; ce serait de l'homogénéisation pure.
- **D3. Ne pas « remplir » le squelette d'audit `voiture`** (`.gitkeep` vides). Rien ne le déclenche ; fabriquer du contenu d'audit sans problème observé est du travail fictif. Le squelette provisionné est une lecture neutre, pas un manque.
- **D4. Ne pas renommer les dossiers** (`aeration_blocage_chauffage`, `panne`/`pannes`, `cumulus*`) pour cohérence. Aucune règle interne de nommage de dossiers n'existe (`nommage_entites.md` ne porte que sur les entités) → ce n'est pas un défaut démontré. Un renommage casse les `include`/filtres `paths` de CI : **haut risque pour un gain cosmétique.**
- **D5. Ne pas généraliser le moteur de type chauffage aux autres domaines.** Les 62 validateurs par domaine passent et sont substantiels (§1) ; bâtir un moteur d'analyse de graphe par domaine serait un coût disproportionné sans manque démontré.

---

## 4. Synthèse coût/bénéfice

| Action | Qualification | Valeur | Coût | Priorité |
|---|---|---|---|---|
| A1 — étendre `CONFIGS` chauffage | risque plausible | élevée | faible | **haute** |
| A2 — contrat minimal reveils/electromenager (conditionnel) | manque démontré partiel | moyenne | faible | moyenne |
| B1 — validateur `pannes` | risque plausible (chemin d'échec) | élevée | moyen | moyenne-haute* |
| B2 — run périodique `schedule:` | risque plausible (dérive externe) | moyenne | faible* | moyenne |
| C1/C2/C3 — optionnelles | clarification / doc | faible | trivial | basse |
| D1–D5 | choix d'architecture / perception passive | — | (éviter le coût) | — |

`*` priorité et coût conditionnés à une décision d'architecture (B1 : définir les invariants ; B2 : changer la philosophie CI).

**Les deux travaux à plus forte valeur réelle** : **A1** (étendre la couverture config du moteur chauffage — capitalise sur l'actif le plus mûr pour combler l'écart le plus conséquent sur le domaine le plus sensible) et **B1** (verrouiller les invariants de `pannes`, le code de chemin d'échec). Tout le reste est secondaire ou à éviter.

---

## 5. Limites du plan

- Établi à `HEAD 899c172` ; le dépôt évolue quotidiennement.
- A1 suppose que les autres fichiers chauffage sont *destinés* à être lintés par le moteur ; le déploiement échelonné peut au contraire être volontairement borné à `autorisation.yaml` — auquel cas A1 perd sa justification. **À confirmer par l'auteur.**
- A2, B1, B2 dépendent d'informations que l'audit ne possède pas (criticité réelle des automatisations reveils/electromenager ; invariants opposables de `pannes` ; fréquence de la dérive externe). Le plan les pose comme **conditions**, pas comme certitudes.
- La satisfaction effective des contrats par l'implémentation reste, hors domaines exécutés ici, non prouvée — ce qui est précisément l'objet des validateurs existants.
- Aucune action n'est appliquée ; ce document est une aide à la décision, pas une mise en œuvre.

---

*Fin du plan d'action. Document d'aide à la décision, sélectif et coût-conscient.*
