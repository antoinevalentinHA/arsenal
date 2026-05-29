# Audit du domaine Chauffage — Arsenal

**Type :** audit structurel préventif (aucun bug actif identifié au lancement)
**Périmètre :** domaine Chauffage (runtime + documentation), relations inter-domaines incluses
**Statut :** rapport final — verdicts vérifiés sur le runtime courant
**Source de vérification :** dépôt `github.com/antoinevalentinHA/arsenal`, branche `main` (état du 29/05/2026)
**Date :** 29/05/2026

---

## Note de provenance et de vérification

Les trois points qui restaient en suspens (intrication `standby_force`, branche `blocage_aeration_en_cours`, renommage `stabilisation_absence`) ont été **tranchés sur l'état courant du dépôt**, par lecture directe des fichiers décisionnels — sans relancer d'audit complet ni recharger l'archive entière. Les références de ligne ci-dessous correspondent à la branche `main` au 29/05/2026.

Classement des constats : **`[établi]`** (preuve directe sur le runtime courant), **`[écarté]`** (faux positif éliminé), **`[ouvert]`** (dette réelle non encore traitée).

---

## 1. Compréhension du domaine

Le domaine Chauffage pilote une chaudière via un pont MQTT (`boiler bridge`, Optolink/MQTT). Ce n'est pas un thermostat : c'est une **machine de décision contractuelle** dont la sortie unique est une consigne (`comfort` / `reduced` / `neutre`) accompagnée d'une **raison métier** explicite.

Quatre couches strictement séparées, conformes au modèle Arsenal :

- **Perception** — capteurs d'état (programme, températures, présence, ouvertures, poêle, géofencing).
- **Autorisation** — `binary_sensor.chauffage_autorise_systeme` et `sensor.chauffage_autorisation_cible` (qui peut retourner `comfort`, `neutre` ou `reduced`).
- **Décision** — `script.chauffage_decision_centrale`, **cerveau unique** en `mode: restart`.
- **Application** — `script.chauffage_appliquer_consigne`, **seul écrivain** de la consigne vers le pont.

Invariant fondateur : **aucune décision sans cause référencée** ; la `raison` est calculée localement et transmise telle quelle, jamais recalculée en aval. `[établi]`

---

## 2. Architecture générale

### 2.1 Points solides

- **Autorité de décision unique.** `chauffage_decision_centrale`, seul point d'entrée canonique du domaine consigne, `mode: restart` garantissant « une seule décision à la fois ». `[établi]`
- **Frontière d'exécution nette.** `chauffage_appliquer_consigne`, seul écrivain matériel. `[établi]`
- **Gardes explicites et hiérarchisées :**

  | Garde | Condition | Contournable par override |
  |-------|-----------|---------------------------|
  | G1 | Anti-rebond géoloc actif | Oui |
  | G2 | Pont (`boiler_bridge_online`) offline | **Non** |
  | G3 | Programme `unknown` | Oui |
  | G4 | `desired_mode == neutre` (STOP propre) | **Non** |
  | G5 | `desired_mode == prog_actuel` (idempotence) | **Non** |

  G2 évaluée au bon niveau, G5 « zéro appel inutile », anti-rebond systématique « zéro oscillation ». `[établi]`

- **Normalisation défensive** de `prog_actuel` (`comfort`/`reduced`/`unknown`), repli explicite. `[établi]`

### 2.2 Fragilité architecturale — la couche « Niveau 1 sécurité système » a collapsé

Constat structurant, vérifié sur `main`.

Le refactor de désintrication a correctement sorti `standby_force` de la composition de `binary_sensor.chauffage_autorise_systeme` (**D1 — soldé**, voir §4.1). **Mais** il a laissé `input_boolean.chauffage_blocage_aeration` comme **seule** entrée du `state:` de ce capteur :

```
# 12_template_sensors/chauffage/autorisation.yaml (l.56-57)
state: >
  {{ is_state('input_boolean.chauffage_blocage_aeration', 'off') }}
```

Le commentaire du fichier l'assume explicitement : `blocage_aeration` est « seule cause d'autorisation » (l.69). Conséquence : `autorise_systeme == off` ⟺ `blocage_aeration == on`. La couche d'autorisation « Niveau 1 sécurité système » n'est donc plus qu'un **alias** d'un unique verrou de stabilisation — ce qui produit le défaut D2 ci-dessous et vide de sens la raison `chauffage_non_autorise`. `[établi]`

---

## 3. Documentation ↔ Runtime

- **Isomorphisme contrat / cerveau.** Le contrat `30_decision_centrale.md` décrit §0–7 normatifs et §8–14 reflet d'implémentation ; la table des raisons correspond aux deux cascades. `[établi]`
- **Double cascade miroir.** Le script `decision_centrale` produit la `reason` ; `sensor.chauffage_raison_calculee` (`diagnostic/raison.yaml`) la **re-produit** via une cascade Jinja équivalente. Miroir diagnostique sans lecture croisée — pas de dépendance circulaire, mais **deux sources à maintenir synchronisées** : toute divergence d'ordre ou de condition est une régression silencieuse → candidat CI `R-MIRROR-1`. `[établi]`
- **Divergence contrat↔runtime sur le nom d'une raison (D3 résiduel).** Le runtime émet désormais `stabilisation_absence`, mais le contrat central `30_decision_centrale.md` porte **encore** `absence_protection_thermique`. Voir §7. `[ouvert]`

---

## 4. Runtime

### 4.1 D1 — désintrication `standby_force` : SOLDÉ

`autorise_systeme.state` ne dépend plus que de `blocage_aeration` (l.56-57). `standby_force` ne subsiste qu'en `attributes:` (l.76-77), commenté « exposé à titre informatif uniquement — NE conditionne PAS l'autorisation système » (l.72-75). La causalité menteuse `standby → chauffage_non_autorise` est éliminée. `[établi]`

### 4.2 D2 — branche `blocage_aeration_en_cours` : VRAIE branche morte (défaut actif)

**Mécanisme, vérifié sur `main`.** Dans la cascade `reason` de `10_scripts/chauffage/decision_centrale.yaml` :

```
l.245-247  {% elif not is_state('binary_sensor.chauffage_autorise_systeme','on') %}
              chauffage_non_autorise          # Niveau 1
l.249-251  {% elif aeration_episode_en_cours AND aeration_confirmee %}
              aeration_en_cours               # Niveau 2a (atteignable)
l.253-254  {% elif is_state('input_boolean.chauffage_blocage_aeration','on') %}
              blocage_aeration_en_cours       # Niveau 2b — INATTEIGNABLE
```

Comme `not autorise_systeme on` ⟺ `blocage_aeration on`, et que le Niveau 1 (l.245) **précède** la branche 2b (l.253) dans la même chaîne `elif`, le Niveau 1 court-circuite systématiquement dès que `blocage_aeration` est actif. La branche 2b ne peut jamais être atteinte. Le miroir `diagnostic/raison.yaml` reproduit le même défaut (l.80-81 vs l.90-91). `[établi]`

**Impact.** Le `desired_mode` est `reduced` dans les deux branches (`decision_centrale.yaml` l.201-202 et l.208-209) → **aucun impact thermique**. Le défaut est **diagnostique/observabilité** : un blocage post-aération s'affiche « Interdit — sécurité système » (`chauffage_non_autorise`) au lieu de « post-aération » (`blocage_aeration_en_cours`). C'est exactement la causalité menteuse corrigée pour `standby_force`, **recréée pour `blocage_aeration`**.

**Note.** `aeration_en_cours` (Niveau 2a) reste atteignable : un épisode d'aération confirmé peut être actif alors que le verrou `blocage_aeration` (post-aération) est encore `off`. Seule la 2b est morte.

**Correctifs (à arbitrer côté doctrine, non prescrits) :**
- *Option doctrinalement cohérente* — traiter `blocage_aeration` comme une cause de **Niveau 2** (limite), pas de Niveau 1 : la retirer de la composition de `autorise_systeme`, exactement comme `standby_force`. La branche 2b redevient vivante. Mais alors `autorise_systeme` n'a plus aucune entrée et `chauffage_non_autorise` devient à son tour mort — il faut décider si la couche Niveau 1 doit accueillir de **vraies** causes d'interdiction système, ou être retirée.
- *Option minimale* — réordonner pour placer 2b avant le Niveau 1 ; mais cela ne fait que déplacer le problème (le Niveau 1 deviendrait mort), donc l'option doctrinale est préférable.

### 4.3 Sous-système retry transactionnel — souveraineté

`11_automations/chauffage/retry_transactionnel/` ré-appelle `script.chauffage_appliquer_consigne` directement (via `mode_session`), sans repasser par le cerveau. Défendable (ré-application d'une décision déjà prise), mais c'est un **second appelant** de la frontière d'exécution alors que le contrat présente la décision centrale comme « seul appelant légitime ». À contractualiser comme exception bornée. `[ouvert]`

### 4.4 Risques de divergence comportementale (refactor `standby_force`)

| Réf | Risque | Statut |
|-----|--------|--------|
| R-DIV-1 | Désync transitoire `standby_force` ↔ `autorisation_cible` | **Correction, pas régression** — qualifier nommément en table de vérité |
| R-DIV-2 | Course de convergence au reload | Faible — robustesse restart native |
| R-DIV-3 | Lecteur cross-domaine s'appuyant sur `autorise_systeme=off` comme proxy standby | **Écarté** (aucun lecteur cross-domaine) |
| R-DIV-4 | Statistique éco impactée | **Écarté** (éco ancré sur `sensor.programme_chauffage`) |

`[établi]`

### 4.5 Dépendances inter-domaines

- `binary_sensor.boiler_bridge_online` — **externe** (domaine boiler), dépendance attendue, gardée par G2. `[établi]`
- La **climatisation** lit `input_boolean.chauffage_blocage_aeration` et la consigne appliquée locale ; couplages documentés côté clim mais **sans document transversal Arsenal** les recensant. Angle mort pour les refactors chauffage. `[ouvert]`

---

## 5. UI

- **Consommateurs uniques de la vérité métier :** 4 briques pivots consomment `sensor.chauffage_raison_calculee` — `carte_chauffage_synthese`, `carte_chauffage_decision`, `carte_chauffage_intention`, `chauffage_diagnostic_global_compact`. `[établi]`
- **Capteurs diagnostics non exposés.** `autorisation_cible` et `autorise_systeme` ne sont jamais consommés en UI : **choix architectural cohérent** (l'UI lit la vérité via `raison`/`mode`), pas un défaut. `[écarté]` comme manque.
- **Conséquence de D2 visible en UI.** Comme la branche 2b est morte, **aucune** des 4 briques n'affichera jamais l'état « post-aération » : l'utilisateur voit « Interdit — sécurité système » à la place. Le correctif UI n'est donc pas à faire en UI — il est en amont (§4.2). `[établi]`
- **Lecture seule** respectée (aucun calcul métier côté UI). `[établi]`

---

## 6. Observabilité

- **Bifurcation journalisation** formalisée : Logbook v2.1 (récit) vs system_log v1.1 (debug). « Le Logbook raconte, le debug trace, l'état prouve. » `[établi]`
- **Notifications hors script `restart`** : automation dédiée, idempotente, reconstructible. `[établi]`
- **Raison toujours observable**, override `confort_force` prioritaire en lisibilité. `[établi]`
- **Réserve.** La fiabilité de l'observabilité est entamée par D2 : la raison observée est fausse pour le cas blocage post-aération. C'est précisément le genre de défaut que l'observabilité est censée empêcher.

---

## 7. Sémantique

- **S1 / D3 — renommage `absence_protection_thermique` → `stabilisation_absence` : quasi soldé.** La branche émet un `comfort` actif (stabilisation d'absence), pas une protection passive — le renommage est justifié par la structure du runtime. Propagation vérifiée sur `main` :
  - **Runtime** : `decision_centrale.yaml`, `diagnostic/raison.yaml`, `diagnostic_thermique/absence/duree_stabilisation.yaml` → migrés. ✓
  - **UI** : les 4 briques pivots → migrées. ✓
  - **Contrats** : `15_capteurs/08_capteurs_inertie_absence.md`, `72_offsets_thermiques_lecture_physique.md` → migrés. ✓
  - **Résiduel `[ouvert]`** : le contrat central `00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md` porte **encore** `absence_protection_thermique` → divergence contrat↔runtime à corriger.
  - Changelogs `v11_1_3.md` / `v12_1.md` : conservent l'ancien nom **à juste titre** (historique figé, ne pas réécrire).
- **S2 — registres UI aplatis.** Causes hétérogènes (sécurité / stabilisation / contexte majeur) traitées d'un bloc « Bloqué ». `[ouvert]`
- **S3 — `confort_suffisant`** : présent comme libellé, à promouvoir en catégorie. `[ouvert]`
- **Dette mineure** : nomenclature `offsets/protection_absence/` conserve « protection ». Acceptée.

---

## 8. Tests

- **Suite structurelle étage 1** : taxonomie exécutable (`registres_entites.yaml`), test cardinal **R-CI-1** (`composes` vs `reads`), double fixture (`autorisation_pre_phase3` doit violer / `post_phase3` doit passer), **META-2** bloquant, ~50 tests verts. `[établi]`
- **Limite.** Couverture **structurelle/contractuelle**, pas comportementale. **Elle ne détecte pas D2** : aucun test d'atteignabilité de branche ni d'iso-comportement. C'est la démonstration concrète du trou de couverture. `[établi]`
- **Invariants candidats non implémentés** : `R-VOC-1/2`, **`R-COV-1` (atteignabilité — couvrirait D2)**, `R-REG-MIX-1`, `R-MIRROR-1`, `INV-30-1..6`, `INV-STANDBY-1/2/4`, `INV-D1/D3`. `[ouvert]`

---

## 9. CI

- **GitHub Actions opérationnel** (dépôt `antoinevalentinHA/arsenal`). Étage 1 chauffage en place : parseur neutre, règles porteuses de doctrine, graphe immuable, dépendances unidirectionnelles. `[établi]`
- **Couverture limitée — confirmée.** L'étage 1 garde contre la réintroduction de motifs structurels (ex. `standby_force` dans `state:`) mais ne couvre ni l'atteignabilité des branches (→ D2 passe au travers), ni la synchronisation des cascades miroir, ni l'iso-comportement. L'étage 2 reste à construire, et **D2 en est le cas d'usage justificatif n°1**. `[ouvert]`

---

## 10. Dette technique (synthèse priorisée, verdicts fermes)

| # | Dette | Nature | Gravité | Statut |
|---|-------|--------|---------|--------|
| D1 | Intrication `standby_force` dans `autorise_systeme` | Architecture / sémantique | Haute | **Soldé** ✓ |
| D2 | Branche `blocage_aeration_en_cours` inatteignable + `chauffage_non_autorise` mensonger | Runtime (branche morte / observabilité) | **Moyenne–Haute** | **Ouvert** |
| D3 | `30_decision_centrale.md` porte encore `absence_protection_thermique` | Doc↔runtime | Basse–Moyenne | **Ouvert** (reste 1 fichier) |
| D4 | Registres UI aplatis (S2) + `confort_suffisant` sans catégorie (S3) | UI / lisibilité | Moyenne | Ouvert |
| D5 | Double cascade miroir non gardée par CI | Régression silencieuse | Moyenne | Ouvert |
| D6 | Étage 2 CI absent (atteignabilité, iso-comportement, miroir) | Tests / CI | Moyenne | Ouvert |
| D7 | Retry = 2ᵉ appelant de `appliquer_consigne` non contractualisé | Souveraineté | Basse–Moyenne | Ouvert |
| D8 | Pas de document transversal des dépendances inter-domaines | Gouvernance | Basse | Ouvert |
| D9 | Nomenclature `offsets/protection_absence/` | Cosmétique | Basse | Acceptée |

Faux positifs écartés : R-DIV-3, R-DIV-4 ; « capteurs diagnostics non exposés en UI » ; distinction `neutre` thermique vs météo en UI (trou doctrinalement assumé).

---

## 11. Plan d'amélioration

**Priorité 1 — D2 (cohérence causale, le seul défaut runtime actif)**
1. Arbitrer la doctrine : `blocage_aeration` est-il une cause de Niveau 1 (interdiction système) ou de Niveau 2 (limite) ? La réponse cohérente avec le traitement de `standby_force` est **Niveau 2**.
2. Si Niveau 2 : retirer `blocage_aeration` de la composition de `autorise_systeme`, ce qui ranime la branche 2b — et **décider du sort de la couche Niveau 1** (lui donner de vraies causes d'interdiction, ou la retirer avec `chauffage_non_autorise`).
3. Valider par table de vérité avant/après : seul le **nom de la raison** doit changer pour le cas blocage aération ; le `desired_mode` doit rester `reduced` (iso-comportement thermique).

**Priorité 2 — Verrouillage CI étage 2**
4. Implémenter `R-COV-1` (atteignabilité de branche) : il aurait attrapé D2 ; il empêchera sa récurrence et tout futur masquage.
5. Implémenter `R-MIRROR-1` (synchronisation des deux cascades) — meilleur rapport valeur/effort.
6. Implémenter l'iso-comportement (`INV-30-5`) et la non-remontée conséquence→cause (`INV-D1/D3`).

**Priorité 3 — Soldes**
7. D3 : aligner `30_decision_centrale.md` sur `stabilisation_absence` (1 fichier, sans toucher les changelogs).
8. D4 : éclater les registres UI. D7 : contractualiser le retry. D8 : créer `dependances_inter_domaines.md`.

Discipline commune : commit atomique, réversible, iso-comportement prouvé hors-ligne avant application ; pas de modification d'ordre/seuil/garde hors périmètre.

---

## 12. Score global

| Axe | Appréciation |
|-----|--------------|
| Architecture (couches, autorité unique, gardes) | **Très solide** |
| Documentation ↔ Runtime | **Solide** — 1 divergence de nom résiduelle (D3) |
| Runtime | **Solide** — 1 branche morte / raison mensongère (D2), sans impact thermique |
| UI | **Solide** — dette de lisibilité (D4) + symptôme de D2 |
| Observabilité | **Solide** — entamée ponctuellement par D2 |
| Sémantique | **Bon** — renommage quasi abouti |
| Tests | **Moyen** — structurel correct, comportemental absent |
| CI | **Moyen** — étage 1 solide, étage 2 manquant |

**Verdict global : architecture mature et gouvernée, nettement au-dessus d'un domaine HA comparable.** Le seul défaut runtime actif (D2) est sans conséquence thermique, localisé, et entièrement réversible. Les faiblesses sont nommées et bornées, pas systémiques. La dette principale est en CI (couverture comportementale), pas dans l'architecture.

---

## 13. Synthèse exécutive

Le domaine Chauffage est un système de décision contractuel mûr : autorité unique (`chauffage_decision_centrale`, `mode: restart`), frontière d'exécution nette (`chauffage_appliquer_consigne`), gardes hiérarchisées G1–G5, traçabilité métier systématique, observabilité bien séparée (Logbook v2.1 / system_log v1.1).

La désintrication de `standby_force` (D1) est **soldée**. Mais elle a laissé `blocage_aeration` comme **seule** entrée de `autorise_systeme`, ce qui fait collapser la couche « Niveau 1 sécurité système » en simple alias d'un verrou de stabilisation. Effet de bord vérifié : la branche de raison `blocage_aeration_en_cours` est **inatteignable** (D2), le Niveau 1 la court-circuitant et affichant `chauffage_non_autorise` à la place. Le comportement thermique reste correct (`reduced` des deux côtés) ; c'est la **cause affichée** qui ment — la même causalité menteuse que celle corrigée pour `standby_force`, recréée pour `blocage_aeration`.

Le renommage sémantique `stabilisation_absence` (D3) est propagé partout sauf le contrat central `30_decision_centrale.md` — une seule correction documentaire à faire. La CI étage 1 verrouille bien le structurel mais ne teste pas le comportemental : c'est elle qui a laissé passer D2, et l'invariant d'atteignabilité `R-COV-1` est exactement le garde-fou manquant.

**Action immédiate recommandée :** trancher la doctrine de `blocage_aeration` (Niveau 1 vs Niveau 2), corriger D2 en conséquence, puis implémenter `R-COV-1` pour verrouiller. Tout le reste est de la dette bornée et planifiable.
