# ✅ ARSENAL — PASSE CONTRACTUELLE FINALE : chantier préfixes / domaines des automatisations

> **Statut** : passe de cohérence de bout en bout, **lecture + corrections mineures** — clôture du chantier.
> **Date** : 2026-07-03.
> **Périmètre** : doctrine, audit, alignements, correction exceptionnelle, validation runtime, registre, checker CI, workflow, index documentaires (PR #254 → #259).

---

## 🎯 Verdict

**Chantier cohérent.** La doctrine, l'audit, les alignements, la correction
exceptionnelle, le registre, le checker APD et le workflow racontent la même
histoire. Trois écarts mineurs de formulation ont été détectés et **corrigés
dans la présente passe** ; aucun écart de fond. **L'étape 5 ferme le
chantier** — aucune micro-PR supplémentaire n'est nécessaire.

---

## 1. Cohérence contrat / registre / checker — ✅ (1 correction)

- Les 3 classes **ERROR du contrat** sont implémentées : préfixe incohérent
  sans exception → `APD-002` ; exception vers préfixe inexistant → `APD-012` ;
  automatisation sans domaine résolu → `APD-003` (+ `APD-001`, garde
  redondante d'AID-004, **assumée et documentée** comme référence croisée).
- **Aucune règle inventée hors contrat** : `APD-000` est une robustesse
  technique (YAML illisible) ; `APD-010/011/013/014` opérationnalisent la
  propriété contractuelle d'**opposabilité** du registre (une exception
  invérifiable n'est pas opposable) et la spécification propriétaire de
  l'étape 4. Aucun INFO/WARN permanent (exigence « aucune tolérance
  permanente » respectée par l'absence même de tolérances).
- Les identifiants APD du docstring correspondent un à un aux règles émises
  par le code (vérifié par extraction : APD-000..003, 010..014).
- Le registre est **strictement** un registre d'exceptions opposables :
  4 entrées, toutes `panne/internet` (`10120000000022..25`, préfixe
  `1012 system`), justifiées (« remédiation infrastructure/réseau ; dossier =
  classement opérationnel ») et datées (arbitrage 2026-07-03). Bluetti n'y
  figure plus ; une note y trace le retrait et son motif.
- **Correction appliquée** : le § CI du contrat disait encore « CI FUTURE /
  est attendue » alors que la CI existe, et n'énumérait pas les contrôles
  d'hygiène du registre. Actualisé : titre « CI DE COHÉRENCE », référence au
  checker et au workflow, puce « hygiène du registre (ERROR) » ajoutée.
  Le contrat et l'implémentation disent désormais la même chose.

## 2. Terme « transversal » hors doctrine — ✅ (2 clarifications)

Le mot est répandu comme **adjectif** (« à impact inter-domaines ») dans les
contrats et l'architecture — usage légitime, antérieur à la doctrine, qui ne
crée pas de droit sur le futur domaine d'ID. Deux points de contact méritaient
une désambiguïsation explicite, **appliquée sans renommage** :

- `contrats/index.md` — étiquettes « (transversal) » de `poele.md` et
  `aeration_recommandation.md` : **note terminologique ajoutée** sous la
  table (« à impact inter-domaines » ≠ domaine d'ID `transversal`, non créé ;
  ces contrats ont chacun un domaine propriétaire unique).
- `contrats/aeration_blocage_chauffage/README.md` — dossier
  `socle_transversal/` : **note ajoutée** (« transversal » s'entend **au sein
  du domaine** — socle commun aux états m0→m6 ; les automations du socle
  relèvent du préfixe `1001 - aeration`).

Le renommage (`socle partagé`, etc.) a été écarté : le sens est légitime,
et un renommage de dossier casserait liens et historique sans gain normatif.

## 3. Cas invalidation aération — ✅ (rien à corriger)

- `11_automations/aeration/invalidation.yaml` : ID `10010000000031`,
  préfixe `1001` (aeration), en-tête cohérent.
- Contrats vivants à jour (`socle_transversal/10_…` et `12_…` citent le
  nouvel ID).
- Rapport d'opération en statut **close** (Git #257 + runtime validé).
- `10170000000010` : **aucune référence vivante résiduelle** — subsiste
  uniquement dans les historiques assumés (rapport d'audit #255,
  `audits/index.md`, rapport de migration — constats datés).

## 4. Cas disqualification aération — ✅ (rien à corriger)

- Fichier en `11_automations/aeration/disqualification_aeration.yaml`,
  ID `10010000000030` inchangé.
- **Aucune exception au registre** (le déplacement a supprimé la divergence,
  conformément à la préférence « corriger plutôt que consigner »).
- Ancien chemin `ouvertures/…` : aucun lien vivant — références restantes
  uniquement dans changelogs gelés et rapport d'audit (historique assumé).

## 5. Cas Bluetti — ✅ (rien à corriger)

- En-tête : « Sous-systeme concerne : energie_chaudiere (… PAS un domaine
  d'ID …) » + « Domaine d'ID proprietaire : panne (1004) » — clarification
  pure, **aucune mention d'exception ni de registre**.
- Aucune entrée Bluetti au registre.
- Le checker le compte **conforme par présomption** (dossier racine `panne/`
  = domaine du préfixe `1004`), pas par exception — vérifié : 259 présomption
  + 4 exceptions = 263.

## 6. Matrice de couverture CI résiduelle

| Exigence contractuelle | Couverture CI | Statut | Commentaire |
|---|---|---|---|
| Préfixe déclaré (`prefix_id_select`) | `AID-004` + `APD-001` | ✅ couverte | garde redondante croisée, assumée |
| Format d'ID (14 chiffres, chaîne, présence) | `AID-001/002/003` | ✅ couverte | juridiction AID ; APD filtre sans double signalement |
| Unicité globale des IDs | `AID-005` | ✅ couverte | |
| Cohérence préfixe ↔ domaine propriétaire | `APD-002` / `APD-003` | ✅ couverte | présomption dossier racine, réfutable, levée par registre seul |
| Exceptions opposables (hygiène du registre) | `APD-010..014` | ✅ couverte | fichier, ID, cohérence, péremption, doublon |
| Domaine `transversal` non créé | — | ⚪ non automatisée (assumé) | création = décision propriétaire explicite ; le jour venu, AID-004/APD fonctionnent sans modification |
| Interdiction du préfixe opportuniste | indirecte | ⚪ non automatisable (assumé) | l'intention n'est pas machine-vérifiable ; garde-fous indirects : `APD-002` + registre à décision explicite + revue de PR |
| Interdiction de modifier un ID hors procédure exceptionnelle | indirecte | ⚪ partiellement couverte (assumé) | une CI statique sans état de référence ne voit pas un changement d'ID régulier ; garde-fous : revue Git (diff des `id:`), `AID-005` (collisions), procédure documentaire exigée |
| Pas de déduction naïve dossier = vérité absolue | par construction | ✅ couverte | présomption réfutable testée (fixtures étape 4 : une exception valide lève APD-002/003) |

Les trois lignes ⚪ sont **assumées et motivées** : aucune exigence
contractuelle manifestement automatisable n'est laissée sans couverture
ni mention.

## 7. Écarts résiduels

**Aucun écart de fond.** Deux constats d'ordre, sans action requise :

- les historiques (audit #255, migration AID-006, changelogs) conservent
  volontairement les anciens IDs et chemins — c'est leur rôle, aucune
  réécriture effectuée ;
- le domaine `transversal` reste défini par la doctrine et **non créé**
  (aucun ayant droit au corpus) — état conforme à la décision propriétaire.

## 🔒 Clôture

Chaîne complète du chantier : contrat (#254) → audit (#255) → alignement
doux (#256) → correction exceptionnelle d'ID (#257, runtime validé) →
clôture documentaire (#258) → CI de cohérence (#259) → **présente passe
contractuelle finale**. Corpus : 263 automatisations, 259 conformes par
présomption, 4 exceptions opposables, 0 ERROR AID, 0 ERROR APD.

**Chantier clos.**
