# 🏗️ Chantier — Centralisation des palmarès météo (dashboard « Palmarès météo »)

> **Type :** chantier Lovelace / météo. **Document faisant foi** du chantier (pointé par `REGISTRE_CHANTIERS.md`).
> **ID registre :** `C7`. **Statut :** **CLOS (2026-06-18)** — Option B retenue, validée terrain (merge #16). Lots 0→4 exécutés ; voir §9 Clôture.
> **Amont :** audit lecture seule *Températures Min · Max* (Option 3) + cadrage lecture seule *Cible B*. Le présent document **fige** la cible et les décisions ; il ne recopie pas l'intégralité du cadrage.
> **Discipline :** aucune modification runtime/doc tant qu'un lot n'est pas explicitement lancé ; co-commit du registre à chaque changement d'état.

---

## 0. Identité du chantier

| Champ | Valeur |
|---|---|
| ID registre | `C7` *(proposé ; pas de nouvelle série `CH-LL-*` — Q1)* |
| Intitulé | Centralisation des palmarès météo |
| Domaine | lovelace / météo |
| Priorité proposée | **P2** (organisation UI ; ni sécurité ni donnée) |
| Emplacement de ce document | `audits/04_chantiers/lovelace/cadrage_palmares_meteo.md` |
| Cible | **B** — destination météo dédiée « Palmarès météo » regroupant les 3 palmarès |

---

## 1. Cible figée

Créer un dashboard **`Palmarès météo`** regroupant les trois palmarès existants, et nettoyer les pages d'origine.

| Palmarès | Carte (réutilisée verbatim) | Capteur (inchangé) | Origine actuelle → après chantier |
|---|---|---|---|
| Jours les plus chauds | `includes/cartes/palmares_temperature_chaude.yaml` | `sensor.palmares_temperature_journalier_chaud` | `meteo_temperature_min_max.yaml` → **Palmarès météo** |
| Jours les plus froids | `includes/cartes/palmares_temperature_froide.yaml` | `sensor.palmares_temperature_journalier_froid` | `meteo_temperature_min_max.yaml` → **Palmarès météo** |
| Précipitations | `includes/cartes/pluie_palmares.yaml` | `sensor.palmares_pluie_journalier` | `meteo_precipitations.yaml` → **Palmarès météo** |

**État final attendu :** *Min · Max* = état du jour pur (12 KPI) ; *Précipitations* = instantané + graphes 7 j / 52 sem + détection 24 h (palmarès pluie retiré) ; *Palmarès météo* = les 3 palmarès.

---

## 2. Arbitrages tranchés (Q1–Q10)

| Q | Décision actée |
|---|---|
| Q1 — Identifiant / emplacement | Ligne au `REGISTRE_CHANTIERS.md` (ID `C7`) ; ce document dans `04_chantiers/lovelace/`. **Pas** de nouvelle série `CH-LL-*`. |
| Q2 — Clé / titre / icône | `meteo-palmares-dashboard` / **Palmarès météo** / `mdi:trophy`. |
| Q3 — Accès | **Tenter le bandeau**, **gate responsive réel obligatoire**. Échec ⇒ fallback **F1 (badge `mdi:trophy`)**. F3 (hub) écarté en 1ʳᵉ intention. |
| Q4 — SSOT bandeau | Modif de `navigation/meteo.yaml` **autorisée uniquement si** test responsive validé. Bouton thermomètre **inchangé** (→ Température instantanée). |
| Q5 — Ancrage doctrinal | **`navigation/domaines/meteo.md`** (non normatif). **Pas** `contrats/meteo/affichage.md`. |
| Q6 — Contrats palmarès | **Intacts.** UI hors-contrat / extension future ⇒ aucune écriture. Changelog global suffit. |
| Q7 — Accès Min · Max | **Séparé.** Min · Max **non** promu en facette dans ce chantier (évite 506 px + mélange de sujets). |
| Q8 — Précipitations | Conserve instantané + graphes 7 j / 52 sem + détection 24 h ; retrait **du seul** palmarès pluie. |
| Q9 — Renommage Min · Max | **Pas de renommage.** Le nom devient plus juste après extraction. |
| Q10 — Périmètre records | **3 palmarès existants** uniquement. Structure extensible, **sans** emplacements vides pour records futurs. |

---

## 3. Périmètre figé

**Dans le périmètre :** 1 nouveau dashboard + 1 entrée de registre `dashboards.yaml` ; réutilisation verbatim des 3 cartes ; retrait des palmarès des 2 pages d'origine ; accès (bandeau gated, sinon badge) ; note doctrinale légère dans `navigation/domaines/meteo.md` ; traçabilité registre/index/changelog.

**Hors périmètre :** données/capteurs palmarès & extrema ; logique des cartes ; renommage d'entité/carte/clé ; refonte esthétique ; accès *Min · Max* (Audit 1) ; records futurs (hebdo/mensuel/saisonnier) ; toute écriture dans les contrats palmarès ou `affichage.md`.

---

## 4. Fichiers du chantier

### 4.1 Runtime Lovelace

| Fichier | Action | Détail |
|---|---|---|
| `18_lovelace/dashboards/meteo/meteo_palmares.yaml` | **Créer** | header `button_card_templates` ; badges Accueil + Navigation ; `!include ../../includes/navigation/meteo.yaml` ; `section_header`(s) ; **3 `!include` palmarès** |
| `18_lovelace/dashboards.yaml` | **Modifier** | clé `meteo-palmares-dashboard` (`mode: yaml`, `title: Palmarès météo`, `icon: mdi:trophy`, `show_in_sidebar: false`, `filename`) |
| `18_lovelace/includes/navigation/meteo.yaml` | **Modifier — conditionnel** | +1 bouton `mdi:trophy` **uniquement si** gate responsive OK ; `grid-template-columns: 1fr repeat(10, 46px) 1fr` ; bouton `grid-column: 11` |
| `18_lovelace/dashboards/meteo/meteo_temperature_min_max.yaml` | **Modifier** | retirer `section_header "🏆 Palmarès historique"` + 2 `!include` chaud/froid |
| `18_lovelace/dashboards/meteo/meteo_precipitations.yaml` | **Modifier** | retirer la **seule** ligne `!include ../../includes/cartes/pluie_palmares.yaml` |
| 3 cartes palmarès | **Inchangées** | réutilisées verbatim (profondeur d'include identique) |

### 4.2 Documentaire

| Fichier | Action |
|---|---|
| `navigation/domaines/meteo.md` | **Modifier** (léger, non normatif) : note « live vs records » + mention de la destination |
| `audits/REGISTRE_CHANTIERS.md` | **Modifier** : ligne `C7` (ouverture, puis clôture) |
| `audits/index.md` | **Modifier** (Lot 4) : entrée navigation vers ce document |
| `changelog/…` | **Modifier** (Lot 4) : entrée de livraison |
| `contrats/meteo/affichage.md`, `palmares_*`, `pluie_palmares.md` | **NE PAS toucher** |
| `ui/navigation.md`, `ui/pattern_dashboard.md`, `extrema_jour_courant.md` | **NE PAS toucher** |

---

## 5. Lots & séquence

```
Lot 0 (CE DOCUMENT + ligne registre C7)        ← ouverture
  └─ Lot 1  note doctrinale  → navigation/domaines/meteo.md
       └─ Lot 2  runtime : 2a créer → 2b registrer → 2c test URL → 2d accès (gate) → 2e retrait origines EN DERNIER
            └─ Lot 3  validations (yamllint + 3 checkers + rendu réel + responsive)
                 └─ Lot 4  changelog + index + registre → clôture
```

**Invariants de séquence :**
- **2e en dernier** : ne jamais retirer les palmarès des origines avant rendu prouvé de la nouvelle page (pas de fenêtre « records nulle part » ; duplication transitoire tolérée).
- **2d-bandeau** seulement après gate responsive **réel** (Pixel 10 Pro Fold + 1 portrait standard). Échec ⇒ **F1 (badge `mdi:trophy`)**.
- **Co-commit** du registre à l'ouverture (Lot 0) et à la clôture (Lot 4).

---

## 6. Validations

| Contrôle | Commande / méthode | Bloquant |
|---|---|---|
| Includes résolus | `python scripts/arsenal_contracts/check_lovelace_includes_contracts.py` | Oui |
| Navigation (clé / cul-de-sac / chemin canonique) | `python scripts/arsenal_contracts/check_lovelace_navigation_contracts.py` | Oui |
| Liens registre existants | `python scripts/arsenal_contracts/check_registre_chantiers.py` | Discipline |
| Lint | `yamllint` sur fichiers touchés | Selon CI |
| Responsive bandeau (si 2d-bandeau) | Pixel 10 Pro Fold + portrait standard | **Gate** |
| Présence/absence palmarès aux bons endroits ; aller/retour navigation | Vérif visuelle desktop + mobile | Oui |

---

## 7. Risques & vigilance (rappel opérationnel)

| # | Vigilance | Mitigation |
|---|---|---|
| R1 | Bandeau saturé (9 boutons = 414 px ; 10ᵉ = 460 px) | Gate responsive ; fallback F1. Pas de supposition. |
| R2 | Blast radius SSOT `navigation/meteo.yaml` | Valider sur plusieurs pages météo, pas seulement Palmarès. |
| R3 | Fenêtre « records nulle part » | 2e en dernier. |
| R4 | Retrait asymétrique (Min · Max = header + 2 includes ; Précip = 1 include sans header) | Suivre §4.1 à la lettre. |
| R8 | Couleur d'icône `mdi:trophy` hors palette | Reprendre une clé de la doctrine couleurs Arsenal. |

---

## 8. État d'avancement

| Lot | État | Date |
|---|---|---|
| Lot 0 — ouverture (ce doc + registre `C7`) | **fait** | 2026-06-18 |
| Lot 1 — note doctrinale (`navigation/domaines/meteo.md`) | **fait** | 2026-06-18 |
| Lot 2 — runtime (dashboard + accès hub Navigation + nettoyage sources + finition UI) | **fait** | 2026-06-18 |
| Lot 3 — validations (checkers + rendu terrain desktop/mobile) | **fait** | 2026-06-18 |
| Lot 4 — clôture documentaire | **fait** (ce document + registre ⑤) ; changelog **hors périmètre**, traité séparément | 2026-06-18 |

---

## 9. Clôture

**Décision finale : Option B** (accès par le hub Navigation).

- **Option A rejetée** — bouton `Palmarès` dans le bandeau météo : **débordement en mobile portrait** (10 boutons), KO terrain. Le bandeau météo est resté/restauré à **9 boutons** et n'est plus touché.
- **Destination finale** :
  - hub Navigation → bouton **« Rec. météo »** (`mdi:trophy`, zone environnement ; `Système` conservé en bas à droite du groupe Navigation ; `Logs HA`/`Journal` côte à côte côté Système) ;
  - dashboard **« Palmarès météo »** (`/meteo-palmares-dashboard`, clé/titre inchangés).
- **Structure finale** du dashboard — trois sections records :
  - **🌡️ Records de chaleur**
  - **❄️ Records de froid**
  - **🌧️ Records de précipitations**
- **Conséquences** :
  - *Températures Min · Max* ne porte plus les palmarès chaud/froid ;
  - *Précipitations* ne porte plus le palmarès pluie ;
  - les includes palmarès ne portent plus de titre markdown interne (cartes utilisées uniquement par le dashboard dédié).
- **Nature** : composition Lovelace / navigation UI uniquement — **aucun capteur, aucune entité, aucune logique métier modifiés** ; contrats palmarès inchangés.
- **Validation terrain** : desktop + mobile portrait ; **rechargement Lovelace suffisant, sans redémarrage HA**.
- **Intégration** : mergé dans `main` (#16, `0c1eb51f`).

---

*Chantier C7 **clos** le 2026-06-18. Document conservé en trace ; statut faisant foi : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (⑤ Clos récents).*
