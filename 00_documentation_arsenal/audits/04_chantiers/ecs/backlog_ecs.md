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

### Décision doctrinale rendue (gate levée)

> **Arbitrage rendu — doctrine (a) « le watchdog borne le verrou ».** Le runtime est déclaré référence ; la doctrine (b) « souverain sur le processus complet » est **rejetée** ; **aucun chantier runtime watchdog**. Le périmètre watchdog est clos en gouvernance. Voir `00_documentation_arsenal/audits/02_arbitrages/ecs/arbitrage_watchdog_ecs.md`. Le volet documentaire (`06` §4.2) est réaligné par le lot de clôture doctrinale.

---

## 🗂️ Fiches

### ECS-WD-2 — Cohérence orchestrateur / watchdog *(CLOS — comportement assumé)*

- **Statut** : **clos par arbitrage** (`arbitrage_watchdog_ecs.md`). Le runtime étant déclaré référence sous doctrine (a), la ré-application possible d'une consigne haute après passage du watchdog (cycle désinfection > 30 min) **n'est plus un défaut** mais une **caractéristique assumée** du domaine.
- **Volet runtime (`ECS-WD-2b`)** : **CADUC** — doctrine (b) rejetée, aucun chantier runtime autorisé.
- **Réouverture** : conditionnée à une **preuve forte** (occurrence réelle observée d'une désinfection > 30 min produisant l'effet), non à une hypothèse théorique. Tracé pour éviter une ré-ouverture en audit.

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

### ECS-DOC — Hygiène documentaire du corpus contrats ECS  *(TRAITÉ — lot de clôture doctrinale)*

- **ECS-DOC-1** *(traité)* : en-têtes `Chemin :` réalignés `…/ecs/` → `…/contrats/ecs/` sur les **11 fichiers** concernés.
- **ECS-DOC-2** *(traité)* : extension `.md` restaurée pour `10_resilience_et_defaillances` (option 1 — fichier unique ; migration dossier non relancée). Impact réel sur l'indexation `*.md` résorbé.
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

## 🧭 Ordre indicatif (post-arbitrage)

1. **ECS-DOC** — ✅ traité (lot de clôture doctrinale).
2. **ECS-WD** — ✅ résolu par arbitrage (doctrine (a)) ; `ECS-WD-2` clos (comportement assumé), `ECS-WD-2b` caduc.
3. **ECS-DESINF-1** (fort levier de protection, faible risque) — reste à traiter via le chantier CI.
4. **ECS-CI** (hygiène de chaîne) — reste à traiter via le chantier CI.
5. **ECS-DESINF-2** *(variante garde CI uniquement)* — préventif, dans le chantier CI.

> Reliquat actionnable = un seul **chantier « Durcissement CI ECS »** (`ECS-DESINF-1`, `ECS-DESINF-2` garde, `ECS-CI-1/2/3`), distinct et ultérieur. Aucun item runtime ouvert.

*Backlog ECS. Acte documentaire — aucun patch, aucune correction. Domaine ECS non clôturé.*
