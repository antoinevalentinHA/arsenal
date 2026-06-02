# ==========================================================
# 📋 ARSENAL — BACKLOG PRIORISÉ
#     Domaine : ECS (Eau Chaude Sanitaire)
# ==========================================================

## 📌 Cadre

- **Sources** : `audit_ecs_domaine.md` + `contre_expertise_watchdog_ecs.md` (HEAD `f6efd6a`).
- **Nature** : backlog priorisé des constats résiduels et confirmés de l'audit ECS. **Aucun chantier ouvert.** Pas de calendrier, pas de charge en jours.
- **Interdits respectés** : aucun patch, aucun YAML, aucune correction. Les arbitrages restent ouverts.

### Définitions

- **Bénéfice attendu** : valeur de sûreté / observabilité / dette résorbée.
- **Risque de régression** : probabilité de perturber l'ECS **en production** en exécutant le chantier.
- **Effort relatif** : surface technique + conception (`faible` · `moyen` · `élevé`).
- **ROI** (qualitatif) : bénéfice × levier, rapporté à effort × risque (`élevé` · `moyen` · `faible`).

### Gate doctrinale en amont

> **`ECS-WD-2` conditionne tout traitement du périmètre watchdog.** Tant que l'architecte n'a pas tranché entre doctrine (a) « le watchdog borne le verrou » (statu quo → simple désambiguïsation documentaire `06` §4.2) et (b) « le watchdog borne le processus complet » (→ chantier d'architecture), aucune fiche du registre watchdog n'est actionnable. Cf. `contre_expertise_watchdog_ecs.md` §7.

---

## 🗂️ Fiches

### ECS-WD-2 — Cohérence orchestrateur / watchdog *(post-contre-expertise)*

- **Constat** : l'orchestrateur n'est pas *watchdog-aware* ; à l'étape 7 (boost) il peut ré-appliquer une consigne haute après que le watchdog a rabaissé à 10 °C et libéré le verrou (cycle désinfection > 30 min). Non contractuel, non bloquant.
- **Bénéfice attendu** : **moyen** — cohérence de la fin de cycle en cas d'expiration watchdog ; supprime la fenêtre « consigne haute après dernier rempart ».
- **Risque de régression** : **moyen** — touche la séquence d'exécution du cycle (boost / fin) ; transition sensible.
- **Effort relatif** : **moyen à élevé** — selon doctrine retenue (garde légère dans l'orchestrateur vs refonte de souveraineté watchdog).
- **Prérequis** : **arbitrage doctrinal (a)/(b) rendu** ; alignement éventuel de `06` §4.2.
- **ROI** : **à déterminer après arbitrage.**

### ECS-DESINF-1 — Couverture CI du sous-système désinfection-retour

- **Constat** : invariants les plus critiques du corpus (`09` §2/§3) **non couverts** par les validateurs ; implémentation pourtant conforme.
- **Bénéfice attendu** : **élevé** — barrière anti-régression sur la fonction sanitaire (légitimité `timer.finished`, écrivain souverain unique, absence de `initial`, non-lecture de `remaining`).
- **Risque de régression** : **faible** — ajout de tests CI ; aucun impact runtime.
- **Effort relatif** : **faible à moyen** — nouveaux tests dans un validateur dédié ou existant.
- **Prérequis** : aucun.
- **ROI** : **élevé** — faible effort, fort levier de protection.

### ECS-DESINF-2 — Robustesse du couplage à `mode_maison` *(latent)*

- **Constat** : consommateur `10250000000021` couplé au trigger `Vacances → Normal` ; sûr à 2 modes, fragile à l'ajout d'un 3ᵉ.
- **Bénéfice attendu** : **faible aujourd'hui**, préventif.
- **Risque de régression** : **faible**.
- **Effort relatif** : **faible** — garde CI sur la cardinalité du select, ou trigger plus robuste.
- **ROI** : **moyen** — préventif, peu coûteux.

### ECS-DOC — Hygiène documentaire du corpus contrats ECS

- **ECS-DOC-1** : corriger en lot les en-têtes `Chemin :` (`…/ecs/` → `…/contrats/ecs/`), 12+ fichiers.
- **ECS-DOC-2** : restaurer l'extension `.md` de `10_resilience_et_defaillances` (renommage) — impact réel sur l'indexation `*.md`.
- **Bénéfice attendu** : **moyen** — fiabilité des outils d'indexation / conversion documentaire.
- **Risque de régression** : **nul** (documentaire).
- **Effort relatif** : **faible**.
- **ROI** : **élevé** — corrections triviales, indépendantes de la doctrine.

### ECS-CI — Hygiène des validateurs et workflows

- **ECS-CI-1** : aligner `check_ecs_cycle.py` T04 sur les 7 entités du contrat `§026` + corriger la docstring.
- **ECS-CI-2** : supprimer la continuation antislash de `check_ecs_securite.py` (`yaml_files()`).
- **ECS-CI-3** : uniformiser les workflows (`python3` + `setup-python` épinglé).
- **Bénéfice attendu** : **moyen** — robustesse et lisibilité de la chaîne de validation.
- **Risque de régression** : **faible**.
- **Effort relatif** : **faible**.
- **ROI** : **moyen à élevé**.

---

## 🧭 Ordre indicatif (hors gate watchdog)

1. **ECS-DOC** (trivial, sans condition, débloque l'indexation).
2. **ECS-DESINF-1** (fort levier de protection, faible risque).
3. **ECS-CI** (hygiène de chaîne).
4. **ECS-DESINF-2** (préventif).
5. **ECS-WD-2** — **bloqué** jusqu'à l'arbitrage doctrinal (a)/(b).

*Backlog ECS. Acte documentaire — aucun patch, aucune correction. Domaine ECS non clôturé.*
