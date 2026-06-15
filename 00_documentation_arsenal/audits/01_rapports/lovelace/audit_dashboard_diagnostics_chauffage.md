# Audit UI — Dashboard diagnostics chauffage

> **Périmètre :** dépôt `antoinevalentinHA/arsenal`, HEAD `80995113` (2026-06-15). Dashboard `18_lovelace/dashboards/diagnostics/chauffage.yaml` + sous-dashboard `18_lovelace/dashboards/diagnostics/thermique_chauffage.yaml`, leurs cartes incluses, leurs templates `button-card`, la table canonique `chauffage_registres_raison`, les socles hérités, et la doctrine couleur UI.
> **Nature :** audit **exclusivement documentaire**. Aucun patch, aucun diff, aucune modification runtime, aucune retouche `18_lovelace/` ni `19_button_card_templates/`, aucun renommage. Les deux arbitrages identifiés sont consignés, **pas corrigés** dans cette passe.
> **Référence couleur opposable :** [`02_palette.md`](../../../ui/couleurs/02_palette.md) + [`03_exceptions.md`](../../../ui/couleurs/03_exceptions.md) + [`05_regles.md`](../../../ui/couleurs/05_regles.md). La palette transmise dans la consigne d'origine **n'est pas** la référence normative du dépôt (cf. §4, faux-problème F5).
> **Complément :** ce rapport couvre la **couche UI**. La couche capteurs/observabilité du même sous-domaine est traitée par [`audit_diagnostics_thermiques_chauffage.md`](../chauffage/audit_diagnostics_thermiques_chauffage.md). Suivi des arbitrages ouverts : [`suivi_audit_dashboard_diagnostics_chauffage.md`](../../04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_chauffage.md).
> **Méthode :** clone réel (`git status` → working tree clean), lecture intégrale du périmètre, extraction systématique des valeurs `rgba()`, traçage `entity_id` → définition, vérification de cohérence libellés UI ↔ sorties capteurs, vérification de résolution des cibles de navigation.

---

## 1. Résumé exécutif

| Indicateur | Valeur |
|---|---|
| Vues auditées | 2 (1 dashboard principal + 1 sous-dashboard thermique) |
| Sections (dashboard principal) | 7, structure linéaire `vertical-stack` + `section_header` |
| Sections (sous-dashboard thermique) | 5 cartes markdown |
| Templates `button-card` inspectés | 11 (+ 2 socles diagnostic) |
| Valeurs `rgba()` sémantiques distinctes | 5, **toutes canoniques** |
| Couleurs hors charte | **0** |
| Références d'entités mortes | **0** (12 capteurs sources tracés et résolus) |
| Cibles de navigation non résolues | **0** (3 dashboards cibles déclarés) |
| Tuiles interactives (action ≠ none) | **0** — lecture seule stricte |

**Niveau global : SAIN.** Conformité couleur intégrale contre la doctrine réelle du dépôt, distinction OFF-volontaire / indisponibilité respectée partout, priorité indisponibilité câblée, cohérence diagnostic↔runtime vérifiée, séparation diagnostic/action stricte, densité fonctionnelle.

**Patch runtime immédiat : aucun justifié.** Deux points relèvent d'**arbitrages différés** (non urgents), deux de **confort** (facultatifs). Tous consignés ci-dessous, aucun traité dans cette passe.

---

## 2. Cartographie

### 2.1 Dashboard principal — `diagnostics/chauffage.yaml`
Une vue, un `vertical-stack` rythmé par `section_header`. Badges de navigation : Accueil · Navigation · Retour → `/chauffage-dashboard/chauffage` · Vannes thermostatiques → `/diagnostics-vannes-dashboard/…` · Diagnostics thermiques → `/diagnostics-thermiques-dashboard/…`.

| # | Section | Carte(s) | Template / include | Entités clés |
|---|---|---|---|---|
| 1 | Mode économique | `bar-card` 24h / 7j | `barres_mode_reduit_chauffage` | `sensor.pourcentage_consigne_eco_{24h,7j}_proxy` |
| 2 | État global | tuile synthèse | `chauffage_diagnostic_global_compact` ← `socle_diagnostic_compact` + `chauffage_registres_raison` | `programme_chauffage`, `chauffage_mode_calcule`, `chauffage_raison_calculee` |
| 3 | Météo | grid 2 | `meteo_chauffage_actuelle_72` · `meteo_favorable_chauffage_72` | `temperature_jardin`, seuils ext ON/OFF, `meteo_favorable_chauffage` |
| 4 | Poêle | tuile diagnostic | `poele_en_fonction_72` | `poele_en_fonction` (+ corroborations) |
| 5 | Aération | grid 2 + conditionnel | `carte_timer_status` · ΔT *ou* `aeration_reference_thermique_72` | `timer.aeration_*`, `chauffage_blocage_aeration` |
| 6 | Réglage thermique | grid 2 | `chauffage_reglage_courbe_diag_72` (`global` / `tendance_24h`) | `ecart_consigne_moyenne_{24h,froid,doux}` |
| 7 | Auto-ajustement courbe | tuile statut | `chauffage_auto_courbe_status_72` (`last`) | `chauffage_reglages_auto`, `courbe_auto_simulation`, `chauffage_last_adjustment` |

### 2.2 Sous-dashboard — `diagnostics/thermique_chauffage.yaml`
Une vue, retour → `/diagnostics-chauffage-dashboard/…`. Cinq cartes markdown : Interprétation (sémaphores emoji), Contexte (dump d'états bruts), Reprise/Arrêt, Oscillateur (+ check cohérence D2×D3≈1440), Inertie.

### 2.3 Dépendances communes
`carte_base_v2` (socles), `chauffage_registres_raison` (table couleur/libellé unique consommée par héritage), `carte_timer_status` (transverse), `aeration_reference_thermique_72` (emprunté au domaine aération). Aucune dépendance circulaire détectée.

---

## 3. Constats validés

1. **Conformité couleur intégrale.** Toutes les valeurs sémantiques du périmètre sont canoniques : `rgba(158,158,158,0.2)`, `rgba(76,175,80,0.2)`, `rgba(33,150,243,0.2)`, `rgba(158,158,158,0.1)`, `rgba(255,152,0,0.2)`. Les seules autres `rgba()` (`rgba(0,0,0,0.08)`, `rgba(255,255,255,0.80)`…) sont des ombres CSS du `bar-card`, pas des couleurs sémantiques. Zéro couleur hors charte.
2. **Distinction OFF-volontaire vs indisponibilité respectée partout.** Gris neutre `0.2` (inactif/repos) et gris indispo `0.1` (`unknown`/`unavailable`) systématiquement séparés (`chauffage_auto_courbe_status_72`, `poele_en_fonction_72`, `meteo_chauffage_actuelle_72`, `aeration_reference_thermique_72`). Conforme à [`05_regles.md`](../../../ui/couleurs/05_regles.md).
3. **Priorité indisponibilité câblée.** Chaque calcul de fond teste `UNAV` en tête avant toute logique métier → l'indispo prime (R6).
4. **Source de couleur unique.** `chauffage_diagnostic_global_compact` ne contient aucune map inline : tout est délégué à `chauffage_registres_raison`, dont l'en-tête cite explicitement la palette.
5. **Cohérence diagnostic↔runtime vérifiée.** Les sous-chaînes matchées par la carte interprétation correspondent exactement aux sorties des capteurs : `regulation` → « très stable / correcte / instable » ; `stabilite` → « très stable / correcte / nervosité » ; `reprise` → « rapide / modérée / lente » ; `inertie` → « très bonne / normale / dissipatif ». Aucun libellé orphelin.
6. **Layering brut↔synthèse = observabilité, pas redondance.** L'oscillateur affiche `amplitude_oscillation` / `nombre_cycles_jour` bruts ; `regulation`/`stabilite` en publient le verdict interprété. Même signal, deux niveaux de lecture.
7. **Dégradation gracieuse.** Les cartes reprise/oscillateur/inertie encapsulent un macro `num`/`intv` mappant `unknown/unavailable/none/''` → `n/a`. Aucune erreur Jinja bloquante possible.
8. **Navigation saine.** Les 3 cibles (`diagnostics-chauffage`, `diagnostics-vannes`, `diagnostics-thermiques`) sont déclarées dans `18_lovelace/dashboards.yaml` et pointent vers des fichiers existants.
9. **Séparation diagnostic/action respectée.** 100 % des tuiles sont `action: none`. Aucune carte ne déclenche de service.

---

## 4. Faux problèmes — à NE PAS corriger

- **F1 — « Dashboard trop dense ».** Faux. Densité = brut + synthèse complémentaires (§3.6). Ne pas dédupliquer oscillateur vs régulation/stabilité.
- **F2 — « `unknown` / `unavailable` mal distingués ».** Faux. La doctrine impose de les traiter à l'identique (les deux → gris indispo `0.1`). Unification volontaire ; ne pas les séparer.
- **F3 — « 2ᵉ segment de `navigation_path` sans path de vue ».** Faux problème. Sur tout le dépôt, seul un dashboard déclare des paths de vue ; le style maison est mono-vue avec fallback index-0 de Home Assistant. Segment inerte mais inoffensif ; ne pas ajouter de `path:`.
- **F4 — « Macros `num`/`intv` dupliquées entre cartes markdown ».** Faux problème. Home Assistant isole le scope Jinja par carte markdown : une factorisation imposerait une mécanique disproportionnée pour un gain nul. Laisser.
- **F5 — Palette de la consigne d'origine.** **Non normative.** Elle mélange palette principale et palettes d'exception, et se trompe sur l'indispo :

  | Rôle | Consigne d'origine | Doctrine réelle ([`02_palette.md`](../../../ui/couleurs/02_palette.md)) | Lecture |
  |---|---|---|---|
  | Bleu info | `rgba(144,202,249,0.25)` | `rgba(33,150,243,0.2)` | la consigne donne le bleu **thermique** (Exception 2), pas l'info |
  | Jaune attention | `rgba(255,193,7,0.25)` | `rgba(255,235,59,0.2)` | la consigne donne le jaune **renforcé** (Exception 6) |
  | Orange warn | `rgba(255,152,0,0.25)` | `rgba(255,152,0,0.2)` | opacité d'exception, pas la principale |
  | Gris indispo | `rgba(224,224,224,0.2)` | `rgba(158,158,158,0.1)` | valeur **absente de la charte** |

  Auditer contre la consigne aurait produit des **faux positifs partout**. Référence opposable = [`02_palette.md`](../../../ui/couleurs/02_palette.md) + [`03_exceptions.md`](../../../ui/couleurs/03_exceptions.md).
- **F6 — `bar-card` rempli en bleu `0.2`.** Conforme (bleu info canonique ; l'Exception 5 autoriserait même davantage). Ne pas « corriger ».

---

## 5. Arbitrages ouverts (différés — non traités ici)

### IMPORTANT-1 — Seuils de classification codés en dur dans l'UI
`chauffage_reglage_courbe_diag_72.yaml` classe « Trop chaud / Trop froid / Déséquilibre / Cohérent » à partir de seuils littéraux `0.4` / `0.5` inscrits dans le template (`label` et `styles.card`).
- **Tension doctrinale :** le pattern maison fait l'inverse — `regulation.yaml` et `stabilite.yaml` possèdent ET publient leurs seuils en backend (`arsenal_threshold_*`), et `meteo_chauffage_actuelle_72` lit ses seuils depuis `input_number.chauffage_seuil_ext_{on,off}`.
- **Portée :** carte diagnostique pure (aucune décision) → ce n'est pas une violation de « le backend décide », mais une logique de classification implicite côté UI, exposée à une dérive silencieuse si la tolérance backend évolue.
- **Statut :** documenté dans l'en-tête du template (« Les seuils sont fixes dans le template (UI) ») → choix assumé, pas accident.

### IMPORTANT-2 — Surcouche « incohérence → rouge » promise mais non exposée en runtime
L'en-tête de `chauffage_registres_raison.yaml` déclare que les surcouches indispo (gris `0.1`) ET incohérence (rouge) sont « portées PAR LES BRIQUES ».
- **Preuve :** la brique consommatrice `chauffage_diagnostic_global_compact` calcule une variable `coherent` puis ne la lit jamais. Elle est annotée « Code mort préexistant … n'est lu par aucun champ. Dette UI distincte, signalée et NON traitée dans CH-6 ». Résultat : aucune carte du périmètre ne produit jamais de rouge d'incohérence (le rouge `rgba(244,67,54,0.2)` est absent du périmètre).
- **Conséquence :** écart contrat↔runtime réel — le narratif promet une capacité que le runtime n'expose pas. Ce n'est **pas un bug caché** : c'est de la dette explicitement tracée.

---

## 6. Recommandations différées (confort — facultatives)

### CONFORT-3 — Finition asymétrique dans le sous-dashboard thermique
`diagnostic_thermique_contexte` est la seule des 5 cartes thermiques à afficher des états bruts (`{{ states('input_select.…') }}`) sans dégradation `n/a`, là où interprétation / reprise / oscillateur / inertie traitent toutes l'indispo proprement. Carte markdown sans fond coloré → la doctrine couleur ne s'applique pas *stricto sensu*, mais la finition est inégale (un `unavailable` s'affichera littéralement).

### CONFORT-4 — La CI couleur ne couvre pas les cartes réelles
`scripts/arsenal_contracts/check_ui_couleurs_contracts.py` valide uniquement la cohérence des **documents** de doctrine (présence/unicité des valeurs canoniques dans les fichiers Markdown de la charte) ; il ne scanne aucun `.yaml` de carte. La conformité couleur des cartes (aujourd'hui parfaite, §3.1) repose donc sur la discipline manuelle, non garantie dans le temps par la CI. Observation d'outillage, pas défaut du dashboard.

---

## 7. Conformité couleur & logique d'états — synthèse

**Palette :** conforme à 100 % (§3.1). **Hiérarchie sémantique** (R1–R6) : respectée, indispo testée en tête partout.

| État attendu | Encodage observé | Verdict |
|---|---|---|
| OFF volontaire | gris neutre `rgba(158,158,158,0.2)` | conforme |
| Normal / nominal | vert `rgba(76,175,80,0.2)` ou bleu info selon nature observable | conforme |
| Attention | orange `rgba(255,152,0,0.2)` | conforme |
| Anomalie (rouge) | jamais émis dans le périmètre | cf. IMPORTANT-2 |
| Indisponibilité technique | gris indispo `rgba(158,158,158,0.1)` (prioritaire) | conforme |
| Donnée inconnue | confondue avec indispo **par doctrine** (F2) | conforme (intentionnel) |

Seul le registre rouge/anomalie n'a aucun chemin actif → objet d'IMPORTANT-2, pas un oubli de palette.

---

## 8. Conclusion

Dashboard diagnostics chauffage **sain** : conforme à la charte couleur réelle du dépôt, sans référence morte, navigation résolue, séparation diagnostic/action stricte, densité fonctionnelle à préserver.

**Aucun patch runtime immédiat n'est justifié.** Les deux points IMPORTANT sont des arbitrages d'architecture/dette à trancher hors de cette passe (suivi : [`suivi_audit_dashboard_diagnostics_chauffage.md`](../../04_chantiers/lovelace/suivi_audit_dashboard_diagnostics_chauffage.md)). Les deux points CONFORT sont facultatifs et sans urgence. Tout le reste (§4) est explicitement à préserver.
