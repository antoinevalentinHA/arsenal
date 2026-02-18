# Plan d’action radio — suppression des états fantômes (capteurs Aqara ouverture)

## 0) Périmètre
- Capteurs prioritaires :
  - `capteur_fenetre_parents_milieu` (0x00158d000587d91a)  → lien faible (LQI 60) vers son parent
  - `capteur_porte_garage` (0x00158d008b319385) → parent actuel `prise_bouclage` (LQI 72)
- Routeurs/prises impliqués (IDs Zigbee) :
  - `prise_lampe_parents` = 0xa4c138e56ee153be
  - `prise_bouclage` = 0xa4c138f6ad627b65
  - `prise_deshumidificateur` = 0xa4c1385aaeecb9a4
  - `prise_palier` = 0xa4c13872a2197bca
  - `prise_cage_escalier_rdc` = 0xa4c138ec49f8db47
  - `prise_box` = 0xa4c1384ccc351a40
  - `prise_sejour_placard` = 0xa4c13887d731b878
  - `sirene` = 0x0015bc0041009f14
  - `Coordinator` = 0xfc4d6afffe4fcc75

---

## 1) Pré-conditions (à faire une seule fois, avant toute manip)
1. Vérifier que les routeurs cibles ne rebootent pas / ne sont jamais coupés :
   - `prise_lampe_parents`
   - `prise_bouclage`
   - `prise_deshumidificateur`
   - `sirene`
2. Si une de ces prises est sur interrupteur mural / multiprise “à risque” :
   - sécuriser l’alimentation (sinon fantômes garantis à terme).
3. Préparer une vérification post-join :
   - produire un nouveau dump routes (ou map Zigbee2MQTT) après chaque reapair,
   - confirmer la ligne `capteur --> routeur : LQI`.

---

## 2) Action A — Chambre parentale : sécuriser le capteur faible
### Cible
- Fixer `capteur_fenetre_parents_milieu` sur `prise_lampe_parents`.

### Pendant le join (fenêtre parents milieu)
- Garder ON :
  - `Coordinator`
  - `prise_lampe_parents`
- Couper temporairement (concurrents backbone, ordre de priorité) :
  1) `prise_palier`
  2) `prise_cage_escalier_rdc`
  3) `prise_box`
  4) `prise_sejour_placard`

### Exécution
1. Débrancher les concurrents listés.
2. Attendre ~90 s (stabilisation mesh).
3. Mettre Zigbee2MQTT en mode appairage.
4. Reset + appairage de `capteur_fenetre_parents_milieu`.
5. Vérifier immédiatement que la route montre :
   - `0x00158d000587d91a --> 0xa4c138e56ee153be : (LQI attendu >= 80 idéalement)`
6. Rebrancher les routeurs coupés, un par un, en laissant ~60 s entre chaque.

### Critère de succès (7 jours)
- Aucun `unavailable` sur ce capteur.
- Aucun changement de parent.
- Aucun “ouvert bloqué” ou “fermé bloqué”.

---

## 3) Action B — Porte du garage : test A/B pour éliminer le parentage comme cause
### État actuel (snapshot)
- `capteur_porte_garage` → `prise_bouclage` : 72
- Cluster cave très fort : `prise_bouclage` ⇄ `prise_deshumidificateur` : 218

### Test B1 (minimal) : quitter `prise_bouclage` sans viser la sirène
Objectif : voir si le parent actuel est le problème.
- Garder ON : tout (dont `sirene`, `prise_deshumidificateur`)
- Couper temporairement :
  1) `prise_bouclage` uniquement

Exécution
1. Débrancher `prise_bouclage`.
2. Attendre ~90 s.
3. Appairer `capteur_porte_garage`.
4. Vérifier le nouveau parent (route `0x00158d008b319385 --> ... : LQI`).
5. Rebrancher `prise_bouclage`.

Décision
- Si stabilité s’améliore (plus de fantômes) : garder ce nouveau parent (pas besoin de sirène).
- Si aucun changement : passer au Test B2.

### Test B2 (ciblé) : forcer la porte garage sur la sirène
Objectif : parent = `sirene`.
- Garder ON :
  - `Coordinator`
  - `sirene`
- Couper temporairement (cluster cave aspirateur) :
  1) `prise_bouclage`
  2) `prise_deshumidificateur`

Optionnel si nécessaire (si elle n’accroche toujours pas la sirène) :
  3) `prise_palier`
  4) `prise_cage_escalier_rdc`

Exécution
1. Débrancher les prises listées (ordre ci-dessus).
2. Attendre ~90 s.
3. Appairer `capteur_porte_garage`.
4. Vérifier immédiatement que la route montre :
   - `0x00158d008b319385 --> 0x0015bc0041009f14 : (LQI)`
5. Rebrancher les prises coupées, une par une (~60 s entre chaque).

Critère de succès (7 jours)
- Aucun `unavailable`.
- Aucun changement de parent.
- Zéro état fantôme.

---

## 4) Post-contrôle (obligatoire)
Après chaque reapair :
1. Refaire un dump routes / map Zigbee2MQTT.
2. Confirmer par ligne :
   - Chambre parents milieu : `0x00158d000587d91a --> 0xa4c138e56ee153be : ...`
   - Porte garage : `0x00158d008b319385 --> (parent réel) : ...`
3. Si le parent n’est pas celui visé :
   - ne pas recommencer en boucle,
   - ajuster uniquement la liste des concurrents à couper (prochaine itération).

---

## 5) Règle d’exploitation (anti-retour des fantômes)
- Ne jamais couper au quotidien les routeurs qui servent de parents aux capteurs critiques :
  - `prise_lampe_parents`
  - parent final retenu pour `capteur_porte_garage` (à confirmer après tests)
- Si un parent est sur une prise sujette à coupure : déplacer le parent (ou sécuriser l’alimentation), sinon les fantômes reviendront.