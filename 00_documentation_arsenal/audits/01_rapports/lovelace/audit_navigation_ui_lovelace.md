# Audit navigation UI Arsenal — Révision v2

**Périmètre** : circulation UI Lovelace — dashboards, vues, badges de navigation, boutons retour, hubs, bandeaux, `navigation_path`, surcharges d'instance.
**Base d'analyse** : dépôt public `antoinevalentinHA/arsenal`, HEAD `41bdc5c` (2026-06-16).
**Nature** : audit en **lecture seule**. Aucun patch runtime, aucune modification de dashboard, aucun renommage. Les corrections runtime (P0/P1) sont **différées à une passe séparée**.
**Statut** : **Révision v2** — corrige et remplace une première passe (v1) invalidée par une erreur méthodologique (voir §1). Les faux positifs de la v1 ne doivent pas être réintroduits.

> **⏩ MISE À JOUR DE CLÔTURE (postérieure à l'audit).** Ce document reste le **constat historique** au HEAD `41bdc5c`, en lecture seule. Les corrections P0/P1 et la normalisation des segments de vue **différées dans les sections ci-dessous ont depuis été intégralement réalisées** ; le bilan figure en **§10 — Clôture du chantier**. Les §0–9 ne sont **pas réécrits** : ils conservent la trace des constats initiaux tels qu'observés.

---

## 0. Verdict en une phrase

L'ossature de navigation Arsenal est **saine et fortement conventionnée** (modèle bi-hub Accueil ⇄ Navigation, badges transverses factorisés, séparation décision/action/diagnostic respectée) ; après résolution des `!include`, il **n'existe aucun cul-de-sac** et le bouton Retour est **contextuel** — les seuls défauts réellement prouvés se réduisent à **un P0** (3 liens cassés vers une clé de dashboard inexistante) et **un P1** (un Retour mal routé), le reste relevant de dette statique sans impact runtime.

---

## 1. Leçon méthodologique (à conserver explicitement)

> **Un audit UI Arsenal ne doit JAMAIS conclure sur les badges, les retours, les culs-de-sac ou les chemins de navigation sans résoudre les `!include` et les surcharges d'instance.**

**Ce que la v1 a fait de travers.** La première passe détectait les boutons de retour en cherchant le **texte littéral** des templates (`template: bouton_accueil_badge_carre`, etc.) **dans le fichier dashboard lui-même**, et testait la présence d'un bloc `badges:` avec une ancre qui ne reconnaissait pas la forme canonique `- badges:` (premier clé de l'item de vue).

**Pourquoi cela casse sur Arsenal.** Arsenal factorise ses badges de navigation dans des **includes partagés** et **surcharge le bouton Retour par instance**. Concrètement, **23 dashboards sur 83** déclarent leurs badges ainsi :

```yaml
views:
  - badges: !include ../includes/badges/diagnostics_systeme.yaml
```

Le contenu réel des badges vit alors dans le fichier inclus, pas dans le dashboard. Une recherche textuelle non résolue voit « aucun badge » là où la page en possède.

**Includes de badges réellement utilisés (résolus) :**

| Include | Badges fournis (effectifs) | Pages |
|---|---|---|
| `18_lovelace/includes/badges/base.yaml` | Accueil + Navigation | 11 |
| `18_lovelace/includes/badges/diagnostics_systeme.yaml` | Accueil + Navigation + **Retour → `/system-dashboard/systeme`** | 10 |
| `18_lovelace/includes/badges/meteo.yaml` | Accueil + Navigation + Paramètres (→ `reglages-meteo`) | 2 |

Ces 23 pages sont **exactement** celles que la v1 a faussement signalées comme culs-de-sac ou comme dépourvues de retour.

**Correction apportée en v2.** Un résolveur YAML charge chaque vue en suivant `!include` (et neutralise `!include_dir_merge_named`, `!secret`), puis recalcule, badge par badge, la cible **effective** selon la priorité : `tap_action.navigation_path` de l'instance > surcharge de l'include > défaut du template. Tous les constats ci-dessous reposent sur cette résolution, recoupée avec le comportement runtime Home Assistant constaté.

> Ce point rejoint le cadrage transverse [`cadrage_ci_includes_lovelace.md`](../../04_chantiers/transverses/cadrage_ci_includes_lovelace.md) (CH-LL-CI-1) : la résolution des `!include` est la condition de validité de tout contrôle de navigation Lovelace.

---

## 2. Distinction de méthode (à appliquer partout)

Chaque constat est étiqueté selon trois niveaux d'évidence, à ne pas confondre :

- **[statique brut]** — observé sur le texte du fichier, sans résolution. **Insuffisant pour conclure** sur la navigation.
- **[statique résolu]** — observé après résolution des `!include` et des surcharges d'instance.
- **[runtime]** — comportement constaté dans Home Assistant.

La v1 a confondu *statique brut* et *runtime* ; la v2 ne conclut que sur *statique résolu* recoupé au *runtime*.

---

## 3. Faux positifs retirés (ne pas réintroduire)

### 3.1 — Culs-de-sac — **RETIRÉ**
**[statique résolu / runtime]** Après résolution des includes : **0 page** sans badge Accueil/Navigation/Retour. **Aucun cul-de-sac strict.**
- `bluetti.yaml`, `ups.yaml` et les diagnostics « système » utilisent `badges: !include …/diagnostics_systeme.yaml` → ils affichent **Accueil + Navigation + Retour → Système** (conforme au runtime).
- `nas.yaml`, `prises.yaml`, `id_automatisations.yaml`, etc. : badges résolus présents.

### 3.2 — Famille météo « sans retour » — **RETIRÉ**
**[statique résolu / runtime]** `meteo_co2.yaml` (et les sœurs concernées) déclarent `- badges: !include ../../includes/badges/base.yaml` → **Accueil + Navigation** en tête de page, **avant** le bandeau météo. La v1 était fausse.

### 3.3 — Sous-arbre voiture « sans retour » — **RETIRÉ**
**[statique résolu / runtime]** `voiture/audi_batterie.yaml` (et les sœurs) déclarent `- badges: !include ../../includes/badges/base.yaml` → **Accueil + Navigation**, puis le bandeau voiture. Pas de cul-de-sac.

### 3.4 — Redondance Accueil ≡ Retour — **RETIRÉ**
**[statique résolu]** Le bouton **Retour est contextuel** : chaque instance/inclusion **surcharge** le `navigation_path` du template vers le **parent**. Le défaut du template (`/arsenal-dashboard/arsenal`) **n'est utilisé par aucune page**. Exemples vérifiés :

| Page | Retour effectif |
|---|---|
| `reglages/chauffage.yaml` | `/chauffage-dashboard/chauffage` |
| `diagnostics/chauffage.yaml` | `/chauffage-dashboard/chauffage` |
| `bluetti.yaml`, `ups.yaml`, … (11 pages) | `/system-dashboard/systeme` |
| `frequence_cardiaque.yaml` | `/sante-dashboard/sante` |

La v1 lisait la **valeur par défaut du template** au lieu de la **surcharge réelle de l'instance**.

---

## 4. Constats conservés (prouvés)

### 4.1 — [runtime] P0 — 3 liens cassés vers la clé inexistante `reglages-dashboard`
**Type : défaut prouvé, à impact runtime.**
- **Fichiers / blocs**
  - `19_button_card_templates/40_dashboards/arsenal/10_action/carte_mode_babysitting.yaml:57` → `hold_action … navigation_path: /reglages-dashboard/maison`
  - `19_button_card_templates/40_dashboards/modes/10_action/carte_vacances_demande_manuelle.yaml:55` → idem
  - `19_button_card_templates/40_dashboards/modes/10_action/carte_mode_babysitting_synthese.yaml:57` → idem
- **Preuve** : la clé `reglages-dashboard` n'existe pas dans `18_lovelace/dashboards.yaml`. La clé réelle est `reglages-maison-dashboard` (l.330), correctement employée en `18_lovelace/dashboards/modes.yaml:15` (`/reglages-maison-dashboard/maison`). Les trois cartes sont instanciées **sans surcharge** du `hold_action` : `carte_mode_babysitting` dans `dashboards/arsenal.yaml:43` ; les deux autres dans `dashboards/modes.yaml:32` et `:38`.
- **Distinction statique/runtime** : ce n'est **pas** un segment de vue inexistant (qui retomberait sur la 1ʳᵉ vue), mais une **clé de dashboard inexistante** → Home Assistant ne peut pas résoudre la page. L'appui long échoue réellement.
- **Gravité : forte** (atteignable depuis l'Accueil), atténuée par le caractère secondaire du geste (hold), le badge « Paramètres » voisin fonctionnant correctement.
- **Correction différée** (passe séparée) : `/reglages-dashboard/maison` → `/reglages-maison-dashboard/maison`.

### 4.2 — [statique, sans impact runtime] Défauts cassés des templates Paramètres/Diagnostics
**Type : hygiène / risque latent — aucun impact runtime aujourd'hui.**
- `bouton_parametres_badge_carre` (défaut `/dashboard-reglages/0`) et `bouton_diagnostics_badge_carre` (défaut `/diagnostics-dashboard/diagnostics`) référencent des **clés inexistantes**.
- **Preuve de non-impact** : la résolution montre que **toutes** les instances surchargent ces cibles ; aucune page n'emprunte le défaut.
- **Risque résiduel** : une future instance oubliant la surcharge produirait un lien cassé silencieux ; l'en-tête documentaire de ces templates décrit ces cibles comme réelles (trompeur — il n'existe pas de « hub diagnostics » unique : le diagnostic est **par domaine**).
- **Gravité : faible** (latent).

### 4.3 — [statique, sans impact runtime] Segments de vue non canoniques (généralisé)
**Type : convention / robustesse — aucun impact runtime (pages mono-vue).**
- Aucun des 83 dashboards ne déclare de `path:` de vue ; 100 % des `navigation_path` internes nommés (ex. `/chauffage-dashboard/chauffage`) ciblent un segment que HA ne trouve pas et **retombe sur l'unique vue**. Correct aujourd'hui.
- **Risque résiduel** : l'ajout d'une 2ᵉ vue à un dashboard ferait diverger les liens profonds.
- **Gravité : faible.**

### 4.4 — [statique, sans impact runtime] Double étiquette de vue `ouvertures-dashboard`
`/ouvertures-dashboard/portes_et_fenetres` (×3) vs `/ouvertures-dashboard/ouvertures` (×1, dans `dashboards/diagnostics/ouvertures.yaml:15`). Même dashboard mono-vue → les deux retombent sur la vue 0. Cosmétique. **Gravité : faible.**

---

## 5. Constat nouveau (issu de la méthode corrigée)

### 5.1 — [runtime] P1 — Bouton Retour mal routé sur `reglages/sommeil.yaml`
**Type : incohérence de chemin — lien valide mais sémantiquement faux.**
- **Fichier / bloc** : `18_lovelace/dashboards/reglages/sommeil.yaml`, badge `bouton_retour_badge_carre`, ligne 15 → `navigation_path: /meteo-bruit-dashboard/bruit`.
- **Constat** : la page « Réglages Sommeil » renvoie, via Retour, vers le dashboard **Bruit (météo)** au lieu de **Sommeil** (`sommeil-dashboard` existe, dashboards.yaml l.106). Le lien **n'est pas cassé** (cible existante), mais il **rompt la convention** « Retour = remonter vers le parent » établie partout ailleurs.
- **Impact utilisateur** : depuis les réglages du sommeil, le retour emmène sur une page sans rapport.
- **Gravité : moyenne-faible** (un seul écart, geste de retour standard).
- **Correction différée** (passe séparée) : `/meteo-bruit-dashboard/bruit` → cible Sommeil. *(Probable copier-coller depuis un gabarit de page météo.)*

---

## 6. Convention Retour — formulation corrigée

La v1 décrivait « Retour = retour à l'Accueil ». **C'est faux.** Formulation correcte, vérifiée par résolution :

- Le template `bouton_retour_badge_carre` porte un **défaut** `/arsenal-dashboard/arsenal`, **jamais utilisé tel quel**.
- Chaque page **surcharge** le Retour vers son **parent logique** (dashboard de domaine, ou Système pour les feuilles système). C'est un vrai « remonter d'un niveau ».
- Le seul écart à cette convention est `reglages/sommeil.yaml` (§5.1).

Cette convention est cohérente avec la référence UI [`ui/navigation.md`](../../../ui/navigation.md) (« Tout dashboard doit permettre un retour vers Arsenal » ; badges purement directionnels, sans action métier).

---

## 7. Respect de l'architecture Arsenal

- **Séparation décision / action / diagnostic / UI** : respectée (réglages et diagnostics = dashboards séparés, atteints par badges dédiés).
- **Accès aux diagnostics** : **bon**, y compris les diagnostics « système » — la v1 les croyait isolés ; ils disposent en réalité de Accueil + Navigation + **Retour → Système** via `diagnostics_systeme.yaml`.
- **Pas de pilotage implicite depuis la supervision** : respecté (badges directionnels uniquement ; `Reboot HA` explicite et protégé par confirmation).
- **Lisibilité sans écran permanent** : **bonne** — pas de friction de cul-de-sac ; toute page offre un retour en badge. Le seul point réel restant est ergonomique et marginal (§5.1).

---

## 8. Recommandations priorisées (révisées)

- **P0** — corriger les **3 `hold_action`** `/reglages-dashboard/maison` → `/reglages-maison-dashboard/maison` (§4.1). *(Passe séparée.)*
- **P1** — corriger le **Retour mal routé** de `reglages/sommeil.yaml` (§5.1) ; fiabiliser les **défauts des templates** Paramètres/Diagnostics (§4.2). *(Passe séparée.)*
- **P2** — trancher la politique de **segment de vue** (déclarer `path:` ou normaliser les `navigation_path`) et unifier la double étiquette de vue `ouvertures-dashboard` (§4.3, §4.4).

---

## 9. Proposition de prochaine passe

1. **Checker Lovelace/navigation avec résolution d'`!include`** (priorité ; **non créé dans cette passe**). Tout contrôle de navigation Arsenal **doit résoudre les includes et les surcharges d'instance** avant de conclure. Le checker devra :
   - charger chaque vue en suivant `!include` ;
   - vérifier que chaque `navigation_path` effectif cible une **clé de dashboard existante** (aurait attrapé `/reglages-dashboard/maison` et les défauts §4.2) ;
   - vérifier la **cohérence du Retour** (cible = parent attendu ; aurait attrapé `reglages/sommeil.yaml`) ;
   - n'émettre un constat « absence de retour » qu'**après** résolution.
2. **Patch P0** une fois le checker en place (3 corrections de clé).
3. **Patch P1** (Retour sommeil + hygiène des défauts de template).

---

## Statut

- Audit **lecture seule** — aucun patch runtime, aucune modification de dashboard dans cette passe.
- **Corrections P0/P1 différées** à une passe d'application séparée.
- Documents liés : [`audit_lovelace_arborescence.md`](audit_lovelace_arborescence.md) (le risque « includes relatifs » y est déjà identifié), hub de domaine [`ui_lovelace.md`](../../../navigation/domaines/ui_lovelace.md), structure include [`18_lovelace.md`](../../../architecture/00_structure_includes/18_lovelace.md).

---

## 10. Clôture du chantier (suites réalisées)

> Addendum **postérieur** à l'audit. Les §0–9 ci-dessus restent le constat d'origine ; cette section enregistre les suites effectivement appliquées, dans des passes séparées et validées en CI. **Le chantier navigation UI Lovelace est clos.**

**Suites réalisées (chronologie) :**

1. **P0 corrigé** (§4.1) — les 3 `hold_action` `/reglages-dashboard/maison` → `/reglages-maison-dashboard/maison`.
2. **Checker `R-LL-NAV-1` créé** — `scripts/arsenal_contracts/check_lovelace_navigation_contracts.py` : résout les `!include` et les surcharges d'instance avant tout constat (la leçon §1, outillée), puis **activé en CI** via `contracts_lovelace_navigation.yml` (push + pull_request).
3. **P1 corrigé** (§5.1) — Retour de `reglages/sommeil.yaml` re-routé vers le parent Sommeil (forme canonique `/sommeil-dashboard`).
4. **Hygiène R5** (§4.2) — en-têtes des templates Paramètres/Diagnostics clarifiés (défaut = **placeholder à surcharger obligatoirement**, non résolvant par dessein). Les valeurs de défaut sont **inchangées** : R5 reste un **warning non bloquant** assumé (dette latente tracée, sans impact runtime puisque toutes les instances surchargent).
5. **Normalisation R4** (§4.3, §4.4, et P2 §8) — résorption complète des segments de vue non canoniques :
   - segments **nommés** historiques : **73 → 0** (passes mécanique A+B+D puis manuelle C+E) ;
   - derniers segments **numériques** `/<dashboard-key>/0` : supprimés.
6. **Durcissement du checker** — R4 est passé de simple constat à **erreur bloquante** : tout `navigation_path` interne ciblant une clé de dashboard existante doit employer la forme canonique **`/<dashboard-key>`**.

**Doctrine finale formalisée (déjà validée — aucune doctrine nouvelle) :**

- Arsenal Lovelace est **mono-vue par dashboard** ; **un domaine fonctionnel = un dashboard**.
- Un dashboard Arsenal **ne dépend d'aucune navigation intra-dashboard**.
- La cible canonique d'un `navigation_path` interne Arsenal est **strictement `/<dashboard-key>`**.
- Les formes **`/<dashboard-key>/<segment>`** et **`/<dashboard-key>/0`** sont **interdites** (erreur R4 bloquante).
- **Aucun `path:`** n'est ajouté aux vues pour justifier une ancienne navigation intra-dashboard.
- Les segments de vue étaient des **reliquats historiques** de l'ancienne grammaire Home Assistant UI multi-vues (anciens dashboards Réglages et Diagnostics multi-vues). **Cette logique multi-vues est abandonnée** ; Arsenal en est sorti.

**Exemption résiduelle assumée** : un segment égal à un `path:` de vue **réellement déclaré** par le dashboard cible reste accepté par le checker (cas unique observé : `imprimerie-nas-dashboard`, qui déclare explicitement `path: nas-imprimerie`). Aucun `path:` n'est ajouté par le checker ; cette exemption ne légitime pas l'ajout de nouvelles vues.

**État final du checker** : `0 erreur`, **R4 = 0**, **R5 ×2** (warnings non bloquants), CI verte.
