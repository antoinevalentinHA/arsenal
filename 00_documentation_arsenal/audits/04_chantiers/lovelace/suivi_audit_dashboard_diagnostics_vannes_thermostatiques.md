# Suivi de l'audit UI — Dashboard diagnostics vannes thermostatiques

> **Rapport source :** [`audit_dashboard_diagnostics_vannes_thermostatiques.md`](../../01_rapports/lovelace/audit_dashboard_diagnostics_vannes_thermostatiques.md).
> **Nature :** entrée de suivi **purement décisionnelle**. Aucune modification runtime/UI, aucun renommage. Ce suivi consigne l'état post-correction V-1 et trace les points ouverts ; il n'en corrige aucun.
> **État global :** dashboard fonctionnellement sain ; **V-1 corrigé** (axe couleur UI conforme). Restent V-2 et V-3, non ordonnancés.

---

## 1. État des écarts

| # | Sujet | Localisation | Statut |
|---|---|---|---|
| **V-1** | Fond KPI non dégradé en gris indispo | `thermo_plateau_strict_72`, `thermo_plateau_affichage_72`, `thermo_mean_12h_72`, `thermo_variance_12h_72` | ✅ **CORRIGÉ** (patch UI séparé) |
| **V-2** | Seuils `0.02` / `0.05` du verdict codés en UI ; `0.02` dupliqué backend | `thermo_stabilite_12h_status` ↔ `plateaux_stricts.yaml` | ✅ **TRAITÉ** — duplication d'affichage acceptable, documentée (§2) ; dé-doublonnage technique parqué |
| **V-3** | Sous-domaine sans contrat de gouvernance | `00_documentation_arsenal/contrats/` (absence) | ✅ **TRAITÉ** — contrat créé : [`contrats/chauffage/vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) |

---

## 2. V-2 — Seuils de verdict en UI (✅ traité par documentation)

**Décision : duplication d'affichage acceptable.** La carte `thermo_variance_12h_72.yaml` recalcule côté JS un verdict 3 niveaux à partir de la variance brute (`< 0.02` → « Très stable » ; `< 0.05` → « Modérément stable » ; `>= 0.05` → « Instable »). Ce recalcul produit **uniquement** icône, label et couleur — **aucune décision, écriture d'état, consigne ou action chauffage**. C'est une **échelle visuelle**, pas une décision dupliquée.

Caractérisation des deux seuils :
- **`0.02` = miroir du seuil canonique.** Identique au seuil de détection de plateau strict (backend `plateaux_stricts.yaml` + écriture `update_plateaux_thermostatiques.yaml`), **canonisé** par [`contrats/chauffage/vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) (§11). Sa présence en dur dans la carte est un **miroir d'affichage** ; **point de coordination** explicite : toute évolution du `0.02` canonique devra être répercutée sur la carte.
- **`0.05` = palier UI-seulement.** Aucune source backend ni contrat (le `diagnostic_chauffage_stabilite` classe par nombre de cycles/jour, et le `0.05` de `programme.yaml` est sans rapport). C'est un raffinement d'affichage propre à la carte, **non gouverné** (à promouvoir uniquement si on souhaite le contractualiser un jour).

**Pourquoi ne pas dé-dupliquer maintenant.** Il n'existe **aucun capteur backend de verdict variance** `0.02`/`0.05` : la carte est la seule productrice du verdict, elle ne peut donc pas « lire » un verdict déjà calculé. Supprimer le recalcul exigerait soit un porteur backend nouveau (capteur/attribut), soit une réécriture du JS de la carte — donc une modification de `19_button_card_templates/` (et/ou du runtime), **hors d'une passe documentaire** et de **faible valeur** (affichage seul). Le **dé-doublonnage technique est parqué** comme option résiduelle optionnelle.

> Reste : option (b) historique (sourcer les seuils depuis un attribut backend / `input_number` pour une source unique) — **parquée**, non bloquante, faible valeur.

---

## 3. V-3 — Contractualisation du sous-domaine (✅ traité)

Le sous-domaine inclut une **écriture d'état** (`script.reset_plateau_piece` → `input_number.plateau_chambre_*`). Un **contrat de gouvernance** a été créé : [`contrats/chauffage/vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md). Il consolide l'existant (détection, mémoire, writers, reset, frontières, invariants, seuil canonique `0.02`, UI/verdict, relations) **sans modifier le runtime**. La frontière stricte avec la décision chauffage y est posée (le plateau ne décide jamais). **V-2 reste ouvert** (dé-doublonnage des seuils côté cartes UI, hors de cette passe).

---

## 4. Conclusion

V-1 résolu ; le dashboard est conforme sur l'axe couleur UI. **Aucun patch runtime/UI** n'est ouvert par ce suivi. V-2 (arbitrage de sourcing des seuils) et V-3 (rédaction d'un contrat) restent à traiter hors de cette passe. La richesse diagnostique du dashboard est **à préserver**.
