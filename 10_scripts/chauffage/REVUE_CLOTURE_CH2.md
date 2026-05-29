# Revue de clôture — Chantier CH-2 (Correctif D2 + alignement contrat)

**Type :** revue d'architecture de clôture (gouvernance de dette) — décision GO/NO-GO
**Objet :** documenter le passage du **NO-GO initial** au **GO confirmé** après lecture du runtime réel.
**Sources de vérité :** `plan_action_chauffage_arsenal.md` (29/05/2026) ; `CHANGELOG_CH1.md` (CH-1 clos) ; **runtime du dépôt public `antoinevalentinHA/arsenal`, branche `main`, lu le 2026-05-29**.
**Périmètre :** gates de risque R1 → R7 de la revue initiale. CH-1 clos et non rediscuté ; arbitrages tranchés (disposition (a), `blocage_aeration = Niveau 2`, fixture canonique) non rouverts.
**Date :** 2026-05-29
**Révision :** intègre la lecture runtime de `decision_centrale.yaml`, `autorisation.yaml`, `diagnostic/{raison,mode}.yaml`, `decision_centrale_trigger.yaml`, la région CI `tools/arsenal_ci/decision/` (+ self-tests) et le contrat `30_decision_centrale.md`.

---

## 1. Décision

> **Verdict initial : NO-GO.** **Verdict après lecture du runtime : GO.**

Le NO-GO initial ne signalait pas un défaut du plan : il interdisait de conclure sans le runtime. Trois inconnues porteuses (R1, R2, R3) ne pouvaient être tranchées sur les seuls artefacts fournis. La lecture du runtime les a résolues, chacune **favorablement** et avec une action désormais **définie**. Il subsiste **une seule réserve** — un choix d'architecture sur le fail-safe de `autorise_systeme` — **bornée et non bloquante** (cf. §5).

---

## 2. Méthode

Audit gate par gate, instruit directement sur le runtime du dépôt public (source de vérité désignée), et non sur des pièces jointes. Chaque gate a produit un constat factuel ; les références de ligne ci-dessous renvoient à l'état `main` lu le 2026-05-29.

---

## 3. Synthèse des gates R1 → R7

| Gate | Question | Résultat | Statut |
|------|----------|----------|--------|
| **R1** | `desired_mode` dépend-il de `autorise_systeme` ? Le cas blocage reste-t-il `reduced` ? | Dépendance réelle (l.201), mais cas blocage `reduced` **avant et après** via la branche 4 (filet). Iso-comportement nominal **prouvé**. | **Fermé — favorable** |
| **R2** | Composition de `autorise_systeme` ; `blocage` seul pilote off ? `autorise` peut-il rester off après retrait ? | `state = is_state(blocage,'off')` — **terme unique** (biconditionnel). `blocage` **seul** pilote off ; après retrait, `autorise` ne peut plus être off (constante). Suppression N1 **sans orphelinage**. | **Fermé — favorable** |
| **R3** | Cycle de vie de `AX-D2` ; fixture vs verdict runtime. | `AXIOMES_D2` **partagé** par le self-test fixture et le verdict runtime (`cli_decision` l.54). Découplage étroit requis ; la suite de tests garde elle-même contre la suppression globale. | **Fermé — périmètre CI défini** |
| **R5** | Recensement exhaustif des lecteurs de `autorise_systeme`. | **5 lecteurs runtime**, tous **intra-domaine** ; **aucun lecteur cross-domaine** ; aucun lecteur d'attribut. Surface bornée et connue. | **Fermé — favorable** |
| **R6** | `stabilisation_absence` : jeton réel ? niveau ? contradiction avec suppression N1 ? | Jeton **réel** confirmé (cerveau, miroir, fixture, CI, UI). **Niveau 3** (confort d'opportunité, `comfort`). **Aucune** contradiction avec la suppression N1 (découplage total). | **Fermé — favorable** |
| **R7** | `diagnostic/mode.yaml` : formule, consommation, avant/après, consommateurs aval. | Lit `autorise` en l.78 ; sortie nominale **invariante** (`Eco→Eco`). **Puits** (CI + 4 briques UI, aucune automation) → **aucune régression de contrôle possible**. | **Fermé — favorable** |

**Écart de modèle (issu de R3).** La revue initiale supposait une détection **structurelle** de D2 ; CH-1 a établi qu'elle est **axiome-portée** (le test de bascule `test_lot_2_3` prouve : sans axiome, la branche blocage redevient atteignable). Cet écart est la racine de la tâche de découplage d'axiome (§4, §6) — il n'invalide pas CH-1, il en tire la conséquence pour CH-2.

**Pourquoi le NO-GO tombe.** R1 (iso-comportement), R2 (composition/orphelinage) et R3 (axiome faux) étaient les trois moteurs du NO-GO. Le runtime montre : iso-comportement nominal garanti par la branche 4 ; `blocage` pilote off unique → suppression N1 sûre ; et un découplage d'axiome étroit, déjà cadré, gardé par les tests. Les inconnues sont levées.

---

## 4. Périmètre CH-2 corrigé (vs plan)

La lecture runtime corrige et complète le périmètre du plan sur quatre points :

1. **Suppression N1 dans `desired_mode` AUSSI.** Le plan déclarait `desired_mode` (l.201-209) **inchangé**. C'est **factuellement incorrect** : `autorise_systeme` devenant constant, la branche N1 de `desired_mode` (l.201) devient **morte**. Elle doit être supprimée, comme dans `reason`, le miroir et `mode.yaml` — sinon recréation d'une pathologie de type D2 dans le cerveau et divergence du squelette `desired_mode`/`reason`.
2. **Fichiers CI à intégrer au périmètre.** Le plan ne listait ni `cli_decision.py` ni `axiomes.py` ni le snapshot `G2`. Le correctif runtime **falsifie l'axiome** `AX-D2` côté runtime : ces fichiers doivent changer dans le **même commit** (cf. §6).
3. **Trigger `autorise_systeme` conservé.** Il devient inerte (autorise constant) mais reste un **hook de sécurité réservé** (contrat `30_..._amendement.md` l.157-158) ; redondant avec le trigger dédié `chauffage_blocage_aeration` → pas de décision périmée. **À ne pas supprimer.**
4. **Contrat 30 : D3 = un seul renommage de cellule** (`absence_protection_thermique → stabilisation_absence`, l.203) + statut Niveau 1 réservé + ajout recommandé `3b` au §Niveau 3.

---

## 5. Distinction fixture ROUGE / runtime VERT

Les deux cibles permanentes de `R-COV-1`, réparties **par plan** (jamais un artefact qui change de couleur) :

- **Fixture (self-test) — ROUGE à perpétuité.** `test_lot_2_3` applique `R-COV-1` à la fixture gelée `d2_reason_pre_correction.yaml` **sous l'axiome `AX-D2`** ; la branche blocage y est dominée → violation attendue, nommant `blocage_aeration_en_cours` / `chauffage_non_autorise` / `AX-D2`. La fixture est verrouillée SHA256 (`test_lot_2_6`) et immuable. Un passage au **vert** = régression du vérificateur, jamais du chauffage.
- **Runtime (verdict) — VERT après correctif.** Après CH-2, `autorise_systeme` est constant et la branche N1 retirée ; l'axiome devient **faux** sur le runtime. Le verdict (`cli_decision`) doit évaluer le runtime **sans axiome** (`A=()`) → couverture purement structurelle → **vert**. Un retour au **rouge** = régression réelle du domaine.

Garde-fou intrinsèque : vider/supprimer `AXIOMES_D2` globalement ferait **échouer** le self-test fixture — la suite détecte donc d'elle-même toute perte du contrôle positif. La bonne action est le **découplage** (changer la seule invocation runtime), pas la suppression de la constante.

---

## 6. Décision restante — fail-safe `unknown` / `unavailable`

**Unique réserve.** Elle se prend **au moment de réécrire le `state:`** de `autorisation.yaml`, pas en audit supplémentaire.

État des lieux : aujourd'hui `state = is_state(blocage,'off')` porte un **fail-safe implicite** — `blocage` à `unavailable`/`unknown` rend `autorise` off, donc `reduced` conservateur. C'est le **seul** endroit qui traite l'état dégradé : ni la branche 4 (`blocage == 'on'`) ni aucune autre ne le rattrapent.

Deux issues, à trancher explicitement :

- **Option A — constante `true`.** `autorise_systeme` devient un hook réservé pur. Simple, mais l'état dégradé **n'est plus conservateur** (il tombe dans la cascade → potentiellement `comfort` via géoloc/présence).
- **Option B — prédicat conservant le repli.** `autorise` on sauf `blocage` dégradé : conserve le `reduced` défensif sur capteur indisponible, sans recoupler le cas nominal.

**Critère de choix :** « capteur `blocage` aveugle » est-il un état où le système doit réduire par prudence ? Réponse = architecture, pas vérification. La réserve est **bornée** (seul l'edge dégradé, rare) et **non bloquante** pour la correction nominale. La décision retenue doit être reflétée **identiquement** dans `desired_mode`, `mode.yaml` et le miroir (via leur dépendance commune à `autorise`), et **consignée** dans la table avant/après (ligne `blocage ∈ {unavailable, unknown}`).

---

## 7. Liste des fichiers à modifier

### Runtime (configuration Home Assistant)

| Fichier | Modification | Origine |
|---------|--------------|---------|
| `10_scripts/chauffage/decision_centrale.yaml` | Suppression de la branche N1 dans `desired_mode` (l.201) **et** dans `reason` (l.246). Branche 4 conservée. `desired_mode` non « inchangé » contrairement au plan. | R1 / R2 |
| `12_template_sensors/chauffage/autorisation.yaml` | `state` (l.56-57) : retrait du terme `blocage`. **Décision fail-safe `unknown/unavailable` requise** (Option A vs B, §6). Attributs (l.67-87) inchangés (observabilité). | R2 / §6 |
| `12_template_sensors/chauffage/diagnostic/raison.yaml` | Suppression de la branche N1 (l.80), **symétrique**, **même commit** (R-MIRROR-1). | R5 / R-MIRROR-1 |
| `12_template_sensors/chauffage/diagnostic/mode.yaml` | Suppression de la branche N1 (l.78), parallélisme. Sûr (puits). | R7 |

### Outillage CI (`tools/arsenal_ci/`)

| Fichier | Modification | Origine |
|---------|--------------|---------|
| `decision/cli_decision.py` | Invocation runtime de `R-COV-1` en `A=()` (l.54) ; retrait de l'import `AXIOMES_D2` devenu inutile côté CLI. | R3 |
| `decision/axiomes.py` | **Conserver** `AX_D2`/`AXIOMES_D2` (requis par le self-test fixture) ; requalifier la **provenance** en prémisse de fixture gelée (la composition citée disparaît). | R3 |
| `tests/test_lot_2_7.py` | `G2` (`test_g2_snapshot_cloture_ch1`) re-snapshoté : `R-COV-1 == 0` sur le runtime corrigé (ou clôture). Même commit que la correction runtime. | R3 / clôture |

### Contrat / documentation

| Fichier | Modification | Origine |
|---------|--------------|---------|
| `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` | §10 ligne « Inhibition géofencing » (l.203) : `absence_protection_thermique → stabilisation_absence` (D3). §Niveau 1 : statut **catégorie réservée sans cause active**. §10 ligne `chauffage_non_autorise` : marquée **réservée / non émise**. Recommandé : §Niveau 3, ajout `3b — Inhibition géofencing → comfort (stabilisation_absence)`. | R6 |
| `00_documentation_arsenal/contrats/chauffage/ci/registres_entites.yaml` | Note de rôle de `autorise_systeme` (gate actif → hook réservé). **Optionnel**, non bloquant. | R5 |

### À NE PAS modifier

- Fixture `tools/arsenal_ci/tests/fixtures/decision/d2_reason_pre_correction.yaml` (gelée, SHA256).
- `tests/test_lot_2_3.py` (contrôle positif) ; manifeste `tests/test_lot_2_6.py`.
- `tests/test_lot_2_5.py` (smoke live, conçu CH-2-robuste — survit tel quel).
- `11_automations/chauffage/decision_centrale_trigger.yaml` — trigger `autorise_systeme` **conservé** (hook sécurité réservé).
- Changelogs gelés (`v11_1_3.md`, `v12_1.md`) — jamais réécrits ; le critère « plus aucune occurrence de `absence_protection_thermique` » se lit **« surface contrat/runtime »**, pas littéralement partout.

---

## 8. Critères d'acceptation avant commit

1. **Table de vérité avant/après** portant `autorise_systeme` en **colonne explicite** et `desired_mode` calculé par la **formule réelle** ; `desired_mode` **identique ligne à ligne**, à l'unique exception assumée de l'edge `blocage ∈ {unavailable, unknown}` selon la décision fail-safe (§6).
2. **Cas blocage post-aération** : raison `chauffage_non_autorise → blocage_aeration_en_cours` ; `desired_mode == reduced` **inchangé**.
3. **`R-COV-1` runtime corrigé (`A=()`) → VERT** ; **`R-COV-1` fixture (`A={AX-D2}`) → ROUGE** ; **`R-MIRROR-1` → VERT** ; **étage 1 → VERT**.
4. **`G2` re-snapshoté cohérent** (`R-COV-1 == 0` sur le runtime corrigé).
5. **Contrat 30 aligné** : `stabilisation_absence` présent ; `absence_protection_thermique` absent de la surface contrat ; Niveau 1 documenté réservé.
6. **Edge `unknown/unavailable`** : comportement **explicitement décidé et consigné** (Option A ou B), reflété **identiquement** dans `desired_mode`, `mode.yaml` et le miroir.
7. **Suppression N1 symétrique** vérifiée dans les **4** cascades (`desired_mode`, `reason`, miroir `raison`, `mode`) ; squelette `desired_mode`/`reason` toujours aligné.
8. **Commit atomique et réversible** ; fixture jamais réécrite ; changelogs jamais réécrits ; aucune modification d'ordre, de seuil ou de garde hors périmètre.
9. **Bascule `ARSENAL_CI_ENFORCE` → bloquant** uniquement **après** verdict runtime vert et table avant/après validée.

---

## 9. Verdict final

> **GO.**

Les trois moteurs du NO-GO initial (R1, R2, R3) sont levés par la lecture du runtime, favorablement et avec un bon de travail défini (§7). La distinction fixture rouge / runtime vert est cadrée et auto-gardée par la suite de tests (§5). La seule réserve restante — le fail-safe `unknown/unavailable` de `autorise_systeme` (§6) — est une décision d'architecture bornée et non bloquante, à acter au moment de réécrire le `state:`.

Sous réserve du respect des critères d'acceptation (§8), **CH-2 est autorisé à l'implémentation**.

---

## Signature

**Architecte de revue (CH-2)** — revue contradictoire conduite sur le runtime réel, gates R1→R7 clos.
Date : 2026-05-29.

Validation opérateur : ____________________  (Antoine) — date : __________

*Document de clôture, à archiver aux côtés de `plan_action_chauffage_arsenal.md` et `CHANGELOG_CH1.md`. À figer après validation ; toute évolution ultérieure relève d'une nouvelle révision, non d'une réécriture.*
