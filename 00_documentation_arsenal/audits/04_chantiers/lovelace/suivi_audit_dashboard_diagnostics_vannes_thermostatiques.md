# Suivi de l'audit UI — Dashboard diagnostics vannes thermostatiques

> **Rapport source :** [`audit_dashboard_diagnostics_vannes_thermostatiques.md`](../../01_rapports/lovelace/audit_dashboard_diagnostics_vannes_thermostatiques.md).
> **Nature :** entrée de suivi **purement décisionnelle**. Aucune modification runtime/UI, aucun renommage. Ce suivi consigne l'état post-correction V-1 et trace les points ouverts ; il n'en corrige aucun.
> **État global :** dashboard fonctionnellement sain ; **V-1 corrigé** (axe couleur UI conforme). Restent V-2 et V-3, non ordonnancés.

---

## 1. État des écarts

| # | Sujet | Localisation | Statut |
|---|---|---|---|
| **V-1** | Fond KPI non dégradé en gris indispo | `thermo_plateau_strict_72`, `thermo_plateau_affichage_72`, `thermo_mean_12h_72`, `thermo_variance_12h_72` | ✅ **CORRIGÉ** (patch UI séparé) |
| **V-2** | Seuils `0.02` / `0.05` du verdict codés en UI ; `0.02` dupliqué backend | `thermo_stabilite_12h_status` ↔ `plateaux_stricts.yaml` | **ouvert — différé** |
| **V-3** | Sous-domaine sans contrat de gouvernance | `00_documentation_arsenal/contrats/` (absence) | ✅ **TRAITÉ** — contrat créé : [`contrats/chauffage/vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) |

---

## 2. V-2 — Seuils de verdict en UI (différé)

Options non tranchées :
- (a) Documenter explicitement l'exception (seuils de verdict assumés en UI).
- (b) Sourcer `0.02` / `0.05` depuis un attribut backend / `input_number`, et **dé-dupliquer** le `0.02` partagé avec la détection plateau, pour une source unique de vérité.

Aucune urgence tant que le critère backend de stabilité reste stable. Toute action toucherait `19_button_card_templates/` (et/ou le runtime) → **hors de la passe documentaire**.

---

## 3. V-3 — Contractualisation du sous-domaine (✅ traité)

Le sous-domaine inclut une **écriture d'état** (`script.reset_plateau_piece` → `input_number.plateau_chambre_*`). Un **contrat de gouvernance** a été créé : [`contrats/chauffage/vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md). Il consolide l'existant (détection, mémoire, writers, reset, frontières, invariants, seuil canonique `0.02`, UI/verdict, relations) **sans modifier le runtime**. La frontière stricte avec la décision chauffage y est posée (le plateau ne décide jamais). **V-2 reste ouvert** (dé-doublonnage des seuils côté cartes UI, hors de cette passe).

---

## 4. Conclusion

V-1 résolu ; le dashboard est conforme sur l'axe couleur UI. **Aucun patch runtime/UI** n'est ouvert par ce suivi. V-2 (arbitrage de sourcing des seuils) et V-3 (rédaction d'un contrat) restent à traiter hors de cette passe. La richesse diagnostique du dashboard est **à préserver**.
