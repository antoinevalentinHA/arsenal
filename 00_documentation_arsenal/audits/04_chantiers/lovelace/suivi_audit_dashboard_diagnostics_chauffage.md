# Suivi de l'audit UI — Dashboard diagnostics chauffage

> **Rapport source :** [`audit_dashboard_diagnostics_chauffage.md`](../../01_rapports/lovelace/audit_dashboard_diagnostics_chauffage.md).
> **Base :** dépôt `antoinevalentinHA/arsenal`, HEAD `80995113` (2026-06-15).
> **Nature :** entrée de suivi **purement décisionnelle**. Aucune modification runtime, aucun patch UI, aucune retouche `18_lovelace/` ni `19_button_card_templates/`, aucun renommage. Ce suivi **consigne** les points ouverts ; il n'en corrige aucun.
> **État global :** dashboard jugé **sain** (cf. rapport). Aucun item ci-dessous n'est urgent ni ordonnancé. Cette entrée existe pour que les points différés soient **tracés**, pas pour ouvrir un chantier de refonte.

---

## 1. Arbitrages (soldés)

| # | Sujet | Localisation | Statut | Risque runtime |
|---|---|---|---|---|
| **IMPORTANT-1** | Seuils de classification `0.4` / `0.5` codés en dur dans l'UI | `chauffage_reglage_courbe_diag_72.yaml` | ✅ **TRAITÉ** — duplication d'affichage acceptable (§IMPORTANT-1) ; sourcing UI parqué | nul (carte diagnostique, aucune décision) |
| **IMPORTANT-2** | Surcouche « incohérence → rouge » promise par le narratif mais non exposée (`coherent` calculé puis non consommé) | narratif de `chauffage_registres_raison.yaml` ↔ brique `chauffage_diagnostic_global_compact` | ✅ **TRAITÉ** — éditorial (a) fait, suivi réaligné ; surcouche (b) parquée (§IMPORTANT-2) | nul (dette déjà tracée verbatim, hors périmètre CH-6) |

### IMPORTANT-1 — ✅ traité (décision)

**Duplication d'affichage acceptable.** Les seuils `0.4` / `0.5` de `chauffage_reglage_courbe_diag_72.yaml` produisent **uniquement** labels, couleurs et verdict visuel (« Trop chaud/froid », « Sous/Sur-chauffe », `warn`/`ok`/`indispo`) — **aucune décision, écriture d'état ou action chauffage** (carte diagnostique). Aucune source canonique unique à dupliquer : des valeurs `0.4`/`0.5` existent ailleurs en backend mais pour des usages distincts (inertie, pente/parallèle suggérées, autorisation cible). Le **sourcing UI** des seuils (option historique (b), alignement `arsenal_threshold_*`) est **parqué** : il toucherait `19_button_card_templates/`, hors passe documentaire et de faible valeur (affichage seul).

### IMPORTANT-2 — ✅ traité (décision)

**Éditorial (a) déjà fait.** L'en-tête de `chauffage_registres_raison.yaml` est corrigé : il indique désormais que la surcouche « incohérence → rouge » est **PRÉVUE mais non exposée** (`coherent` calculé dans `chauffage_diagnostic_global_compact` mais consommé par aucun champ — dette UI distincte, différée). Le commentaire inline de la brique compacte le confirme. La **sur-promesse narrative a disparu** ; ce suivi est réaligné en conséquence.

**Implémentation (b) parquée.** Brancher `coherent` sur un champ (surcouche rouge réelle) est un **vrai chantier UI optionnel**, risque nul, déjà tracé verbatim dans les fichiers. **Non engagé ici** (toucherait la logique UI). Aucun patch UI requis pour solder IMPORTANT-2 côté documentaire.

---

## 2. Recommandations différées (confort)

| # | Sujet | Localisation | Statut |
|---|---|---|---|
| **CONFORT-3** | Finition asymétrique : seule carte thermique sans dégradation `n/a` | `diagnostic_thermique_contexte.yaml` | différé — facultatif |
| **CONFORT-4** | CI couleur valide la doctrine documentaire mais ne scanne pas les cartes Lovelace / button-card réelles | `scripts/arsenal_contracts/check_ui_couleurs_contracts.py` | différé — facultatif |

CONFORT-4 est le seul item potentiellement **outillage** (un futur garde-fou anti-dérive scannant les `rgba()` des cartes contre la charte) ; il ne touche ni le dashboard ni les templates.

---

## 3. Conclusion

Aucun item n'appelle d'action immédiate. **Aucun patch runtime, aucun patch UI** n'est ouvert par ce suivi. Les deux arbitrages IMPORTANT restent à trancher hors de cette passe ; les deux CONFORT sont facultatifs. La densité diagnostique du dashboard est **à préserver**.
