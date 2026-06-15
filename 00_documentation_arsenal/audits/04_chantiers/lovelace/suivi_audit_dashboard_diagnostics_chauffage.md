# Suivi de l'audit UI — Dashboard diagnostics chauffage

> **Rapport source :** [`audit_dashboard_diagnostics_chauffage.md`](../../01_rapports/lovelace/audit_dashboard_diagnostics_chauffage.md).
> **Base :** dépôt `antoinevalentinHA/arsenal`, HEAD `80995113` (2026-06-15).
> **Nature :** entrée de suivi **purement décisionnelle**. Aucune modification runtime, aucun patch UI, aucune retouche `18_lovelace/` ni `19_button_card_templates/`, aucun renommage. Ce suivi **consigne** les points ouverts ; il n'en corrige aucun.
> **État global :** dashboard jugé **sain** (cf. rapport). Aucun item ci-dessous n'est urgent ni ordonnancé. Cette entrée existe pour que les points différés soient **tracés**, pas pour ouvrir un chantier de refonte.

---

## 1. Arbitrages ouverts

| # | Sujet | Localisation | Statut | Risque runtime |
|---|---|---|---|---|
| **IMPORTANT-1** | Seuils de classification `0.4` / `0.5` codés en dur dans l'UI | `chauffage_reglage_courbe_diag_72.yaml` | **ouvert — différé** | nul (carte diagnostique, aucune décision) |
| **IMPORTANT-2** | Surcouche « incohérence → rouge » promise par le narratif mais non exposée (`coherent` calculé puis non consommé) | narratif de `chauffage_registres_raison.yaml` ↔ brique `chauffage_diagnostic_global_compact` | **ouvert — différé** | nul (dette déjà tracée verbatim, hors périmètre CH-6) |

### IMPORTANT-1 — options (non tranchées)
- (a) Documenter explicitement l'exception (seuils d'affichage fixés en UI, assumés).
- (b) Sourcer `0.4` / `0.5` depuis un `input_number` ou un attribut backend, par alignement avec le pattern `arsenal_threshold_*`.
- **Aucune urgence** tant que les tolérances backend restent stables.

### IMPORTANT-2 — options (non tranchées)
- (a) **Correction éditoriale** du narratif de l'en-tête de `chauffage_registres_raison.yaml` pour ne plus promettre une surcouche que la brique compacte n'expose pas — relèverait de la procédure « correction éditoriale simple » (fichier / texte à chercher / texte de remplacement / justification / vérification), **pas** d'un patch.
- (b) **Implémentation** de la surcouche rouge (brancher `coherent`) — vrai chantier UI à cadrer séparément, **hors** de cette passe documentaire.
- **Note de périmètre :** (a) touche `19_button_card_templates/` (commentaire d'en-tête) et (b) touche la logique UI — **les deux sont hors du périmètre de la présente passe documentaire** et ne doivent pas être engagés ici.

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
