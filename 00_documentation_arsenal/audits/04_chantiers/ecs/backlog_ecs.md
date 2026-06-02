# ==========================================================
# 📋 ARSENAL — BACKLOG PRIORISÉ
#     Domaine : ECS (Eau Chaude Sanitaire)
# ==========================================================

## 📌 Cadre

- **Sources** : `audit_ecs_domaine.md` + `contre_expertise_watchdog_ecs.md` (HEAD `f6efd6a`) ; `arbitrage_watchdog_ecs.md` ; `audit_ecs_offsets.md` (HEAD `372b8d7`).
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
- **ECS-OFF-5** *(audit Offsets)* : verrouiller en CI les paramètres contractuels `11` §10 (alpha, zone morte, buckets, plage durée) et le format du résumé figé — aujourd'hui déclarés « rupture de contrat » mais non testés.
- **Bénéfice attendu** : **moyen** — robustesse et lisibilité de la chaîne de validation ; protection des invariants d'apprentissage.
- **Risque de régression** : **faible**.
- **Effort relatif** : **faible**.
- **ROI** : **moyen à élevé**.

### ECS-OFF-1 — Observabilité de la trajectoire d'apprentissage *(CLOS — réalisé)*

- **Statut** : **résorbé** — chantier d'observabilité livré et committé. Justifié par l'état réel du dépôt.
- **Livré** : historisation `recorder` (`ecs_off_*`, `ecs_temperature_max_reelle_figee`, `ecs_duree_dernier_cycle_figee`, `ecs_autocorrect_active`, `ecs_dernier_ajustement`, `ecs_resume_dernier_cycle_fige`) ; cartes `ecs_apprentissage_offsets.yaml` (synthèse lecture seule) et `ecs_apprentissage_courbes.yaml` (trajectoire offsets + consigne/Tmax) ; section « Apprentissage des offsets » dans `dashboards/diagnostics/ecs.yaml`.
- **Constat d'origine** (conservé pour traçabilité) : offsets et données d'apprentissage non historisés → trajectoire invisible, dérive lente / biais indétectables.
- **Effet de bord** : les risques assumés `ECS-OFF-3` (transitoire d'aberration) et `ECS-OFF-7` (convergence lente) deviennent **surveillables** sur les courbes.
- **Réserve** : aucune (l'historique se densifie naturellement avec les cycles ; propriété runtime inhérente, sans action documentaire).

### Risques assumés *(hors backlog actionnable — réf. contrat `11` §11)*

- **ECS-OFF-3** : absence de rejet d'aberration sur `tmax` ; dérive cumulative **bornée par le clamp**, transitoire d'un cycle possible. Mitigation = runtime → **gated preuve forte**, non ouverte.
- **ECS-OFF-7** : convergence par bucket inégale (`desinfection` rare). Comportement de gain-scheduling assumé.
- *Jonction* : un cycle de désinfection tronqué par le watchdog (`ECS-WD-2`, assumé) est le cas-type de cycle « valide mais non représentatif » d'OFF-3.

### Dettes documentaires *(résorbées par la consolidation Offsets — réf. contrat `11`)*

- **ECS-OFF-2** (§3.3, portée réelle de `valide`), **ECS-OFF-4** (§6.1, asymétrie de zone morte), **ECS-OFF-6** (§11, amorçage depuis `unknown`), **ECS-OFF-8** (§11, correcteur sans mémoire d'erreur) — **traités** par alignement du contrat `11`.

---

## 🧭 Ordre indicatif (post-arbitrage)

1. **ECS-DOC** — ✅ traité (lot de clôture doctrinale).
2. **ECS-WD** — ✅ résolu par arbitrage (doctrine (a)) ; `ECS-WD-2` clos (comportement assumé), `ECS-WD-2b` caduc.
3. **ECS-DESINF-1** (fort levier de protection, faible risque) — reste à traiter via le chantier CI.
4. **ECS-CI** + **ECS-OFF-5** (hygiène de chaîne + verrouillage des paramètres d'apprentissage `11` §10) — chantier CI.
5. **ECS-DESINF-2** *(variante garde CI uniquement)* — préventif, dans le chantier CI.
6. **ECS-OFF-1** (observabilité de l'apprentissage) — ✅ **réalisé** (recorder + cartes + section diagnostics).

> Reliquat actionnable = **un seul chantier**, distinct et ultérieur, sans item runtime ouvert :
> - **Chantier « Durcissement CI ECS »** : `ECS-DESINF-1`, `ECS-DESINF-2` (garde), `ECS-CI-1/2/3`, **+ `ECS-OFF-5`**.
>
> Réalisés : observabilité `ECS-OFF-1`, hygiène doc `ECS-DOC-1/2`, watchdog (arbitrage).
> Risques assumés (`ECS-OFF-3`, `ECS-OFF-7`, `ECS-WD-2`) et dettes documentaires (`ECS-OFF-2/4/6/8`) : voir ci-dessus et contrat `11` §11.

*Backlog ECS. Acte documentaire — aucun patch, aucune correction. Domaine ECS non clôturé.*
