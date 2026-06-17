# BACKLOG — DETTES RÉSIDUELLES CLIMATISATION & HYSTÉRÉSIS

> Sources : audit climatisation (D1–D13), audit hystérésis transverse (H1–H3),
> runtime du dépôt. Échelle : P0 = incident probable · P1 = correction recommandée ·
> P2 = amélioration utile · P3 = cosmétique.
>
> **Backlog de travail : ne liste que les dettes encore ouvertes.** Les items soldés
> D1, D2, D3, D4, D6, D7, D8, D9 ont été retirés ; **H1 (déshumidificateur — seuils
> inversés) est résolu et retiré** (durcissement structurel des plages). Leur historique
> fait foi ailleurs — changelogs v15.8.4 / v15.8.5, audits sources
> (`audits/01_rapports/climatisation/audit_climatisation_arsenal.md`,
> `audits/04_chantiers/transverses/hysteresis_5_domaines.md`), registre *Clos récents*
> (pour H1) et git. Ce document n'est pas un registre historique.

## Note de cadrage

Aucun incident fonctionnel n'est ouvert : il ne subsiste **aucun P0 inconditionnel**.
Depuis la résolution de **H1** (durcissement structurel des plages, `max(OFF)=74 < min(ON)=75`),
il ne subsiste **plus aucun P0 conditionnel** non plus.
Tout le reste relève de gouvernance, d'explicabilité ou de maintenabilité — pas de panne.

---

## Classification et estimation, dette par dette

### P2 — améliorations utiles

**D5 — Notification d'échec persistant non matérialisée**
- Type : gouvernance (contrat 08 vs runtime). Proba incident : faible (échec infra
  prolongé). Impact : un échec d'exécution reste silencieux. Complexité faible (notif,
  ou corriger le contrat). Régression faible. **P2.**

**D13 — Couverture CI partielle** (reliquat étroit)
- Type : gouvernance. La CI fige **déjà** l'admissibilité (portes 1/2), l'extinction COOL
  (sens `<=`), la consommation des admissibles par `clim_raison_decision`, la carte
  `status_72` (F5) et la délégation de cohérence de `carte_clim_decision` (F6) — protections
  livrées en v15.8.4, présentes dans `check_climatisation_admissibilite_contracts.py` et
  `check_climatisation_seuils_cool_contracts.py`.
- **Reliquat réel : aucun test de non-régression sur `clim_bloquee` (F2/D3) ni
  `clim_action_en_cours` (F3/D7).** Proba incident : nulle directe.
- Complexité faible (deux assertions à ajouter). Régression nulle. **P2** — complète le
  filet CI sur les deux derniers artefacts d'observabilité non couverts.

**H2 — VMC : seuils OFF morts mais validés**
- Type : **gouvernance** (faux sens de contrôle). Proba incident : nulle (le verrou
  temporel de 15 min fonctionne). Impact : un réglage UI validé sans effet réel.
  Énergie : marginale (run-on temporel ≠ vraie hystérésis). Complexité faible (câbler
  `seuil_off` à la libération, ou supprimer le paramètre + sa validation). Régression
  faible. **P2.**

**H3a — Aération : seuil unique sans bande morte**
- Type : bug potentiel / explicabilité. Proba : oscillation de la recommandation si bruit
  autour de `ha_min`/`dt_min`. Impact : scintillement d'un signal **consultatif** (+ jitter
  propagé à la voie HR de la VMC, amorti par son verrou). Énergie : faible. Complexité
  moyenne (ajouter deadband/mémoire). Régression moyenne (modifie le comportement de
  recommandation). **P2.**
- *Pré-chantier : confirmer d'abord si `tentative_en_grace` amortit déjà en aval.*

**D-tuile — Polarité de `clim_synthese_status_72` (reportée)**
- Type : explicabilité / maintenabilité. Défaut de modèle du template partagé (concerne
  aussi HEAT) ; `clim_maintien_cool` est une entité fantôme. Complexité moyenne.
  Régression faible (UI). **P2**, en attente de l'observation runtime post-déploiement déjà
  prévue.

**D10 — Duplication humidex DRY + organisation de fichiers**
- Type : maintenabilité. Impact : confusion, capteur quasi-orphelin. Complexité faible.
  Régression faible. **P2/P3.**

### P3 — cosmétique / à laisser tel quel

**H3b — Aération : helpers d'hystérésis déclaratifs non câblés** — gouvernance/cosmétique.
Les supprimer (ou les câbler avec H3a). **P3.**

**D11 — Dérive sémantique `chauffage_clim_active_en_hiver`** — maintenabilité (nommage).
Le renommer casserait des références (régression) ; **laisser tel quel** ou clarifier en
commentaire. **P3.**

**D12 — Divers** : IDs d'automation hétérogènes, plage `clim_offset_off` à −3, doc fantôme
`clim_etat_reel`. Sans danger. **P3 — laisser tel quel** (nettoyage opportuniste seulement).

**DRY — bande morte −1 codée en dur** (audit hystérésis §2bis) — lisibilité. **P3.**

**Contrat 05 — « aucun deadlock thermique »** désormais vrai depuis le fix. Réalignement
doc trivial. **P3.**

**Chauffage** — système modulant par conception. **Aucun chantier** ; la grille ON/OFF ne
s'applique pas. Laisser tel quel.

---

## Backlog unique

| Priorité | Dette | Type | Risque | Bénéfice | Effort |
|---|---|---|---|---|---|
| P2 | D5 — notif échec persistant | Gouvernance | Échec exécution silencieux | Visibilité des pannes | Faible |
| P2 | D13 — CI partielle | Gouvernance | Filet incomplet (`clim_bloquee` F2, `clim_action_en_cours` F3) | Fige les 2 derniers artefacts | Faible |
| P2 | H2 — VMC seuils OFF morts | Gouvernance | Réglage UI sans effet | Contrôle réel ou param supprimé | Faible |
| P2 | H3a — aération sans deadband | Bug potentiel | Oscillation recommandation | Stabilité du conseil | Moyen |
| P2 | D-tuile — polarité status_72 | Explicabilité | Tuile diagnostic inversée | Diagnostic COOL/HEAT correct | Moyen |
| P2/P3 | D10 — duplication humidex DRY | Maintenabilité | Confusion capteur orphelin | Domaine DRY lisible | Faible |
| P3 | H3b — helpers hystérésis aération morts | Gouvernance | Faux signal de réglage | Cohérence UI | Faible |
| P3 | D11 — nom `…active_en_hiver` | Maintenabilité | Compréhension future | Sémantique claire | Faible (doc) |
| P3 | D12 — IDs / offset / doc fantôme | Cosmétique | Friction maintenance | Hygiène | Faible |
| P3 | DRY deadband −1 en dur | Maintenabilité | Non paramétrable | Lisibilité | Faible |
| P3 | Contrat 05 « aucun deadlock » | Gouvernance/doc | Contrat daté | Cohérence doc | Trivial |
| — | Chauffage (modulant) | — | — | Ne rien forcer | Nul |

---

## Lecture stratégique

- **Dernier filet à compléter : D13** — la CI couvre déjà admissibilité, extinction COOL,
  raison, `status_72` et cohérence ; il ne reste qu'à couvrir `clim_bloquee` et
  `clim_action_en_cours`.
- **Tout le reste (P3) peut rester tel quel** sans dette opérationnelle : à nettoyer
  seulement de façon opportuniste, jamais comme chantier dédié.
- **Pré-vérifications avant tout chantier P2** (sans en faire un audit) : l'amortissement
  `tentative_en_grace` en aval de l'aération, et la cohérence `vmc_duree_min_haute` ↔
  `vmc_duree_haute_vitesse`. Tant que non confirmées, H3a et H2 restent des estimations.
