# 🚨 ARSENAL — CHANTIER C23 · Alarme — Restitution UI de `triggered` + priorité d'indisponibilité

## 📌 Statut

- **Chantier en cours — patch UI implémenté sur branche, PR à ouvrir** (non mergé ; sans preuve terrain `triggered`/indisponibilité, différée). Ouverture initiale documentaire : PR #391 (mergée), sans patch.
- **Identifiant global** : **C23** (série globale ; aucun identifiant local `CHx` créé)
- **Domaine** : Sécurité / Alarme — restitution UI
- **Priorité** : **P2** — le défaut affecte la **compréhension** de la restitution UI ; le runtime, la décision, les notifications et la chaîne de sûreté restent **sains**.
- **Patch UI** : les 2 cartes sœurs `carte_alarme_decision` / `carte_alarme_intention` portent l'échelle de restitution (branches mutuellement exclusives ; preuve statique 25/25 ; checkers UI verts). Aucune entité/helper/socle, aucune modification runtime/contrat/notification.
- **Changelog** : non créé à ce stade — un changelog est un artefact de release produit sur dépôt de diffs + demande explicite de l'opérateur (doctrine `redaction_changelog.md` §1) ; le changement est tracé par la PR et la ligne du registre.

---

## 1. Source opposable & périmètre exclusif

- **Source opposable** : rapport d'audit mergé [`../../01_rapports/alarme/audit_exposition_diagnostics_alarme.md`](../../01_rapports/alarme/audit_exposition_diagnostics_alarme.md) (PR #390). Les livrables d'étape (Gates A‑D) y sont absorbés.
- **Périmètre exclusif** : les **deux verdicts `PARTIEL`** de l'audit :
  - **ALM‑DIAG‑001** — restitution **claire et non ambiguë** de l'état réel `triggered` ;
  - **ALM‑DIAG‑003** — **priorité de l'indisponibilité** (`unknown`/`unavailable`) sur toute représentation de cohérence ou de divergence.
- Les 11 autres exigences opposables restent **CONFORMES** et hors périmètre.

---

## 2. Fichiers UI concernés (aucune autre surface)

- `19_button_card_templates/40_dashboards/alarme/30_diagnostic/carte_alarme_decision.yaml` (hérite `socle_diagnostic`).
- `19_button_card_templates/40_dashboards/alarme/20_intention/carte_alarme_intention.yaml` (hérite `socle_status`).
- Consommées **uniquement** par `18_lovelace/dashboards/alarme/principal.yaml` (chacune une fois). La logique cohérence/divergence est **dupliquée** entre les deux cartes sœurs.

---

## 3. Comportement cible validé

### Échelle de **priorité de restitution UI**

`1. INDISPONIBILITÉ  >  2. TRIGGERED  >  3. NOOP  >  4. COHÉRENCE  >  5. DIVERGENCE`

- une **indisponibilité interdit** toute affirmation de cohérence **ou** de divergence ;
- **`triggered`** conserve sa **sémantique propre** d'alarme déclenchée ;
- **`NOOP`** est une **abstention valide** ;
- **cohérence et divergence** ne sont évaluées **qu'avec des opérandes disponibles**.

| Niveau | Condition (mutuellement exclusive) | Fond | Libellé / signal |
|---|---|---|---|
| **L1 Indispo** | réel ∈ {`unknown`,`unavailable`} **ou** cible ∈ {`unknown`,`unavailable`} | `rgba(158,158,158,0.1)` | « Indisponible » — aucune cohérence/divergence affirmée |
| **L2 Triggered** | réel == `triggered` | `rgba(244,67,54,0.2)` | « **Alarme déclenchée** » + **icône** `mdi:shield-alert` |
| **L3 NOOP** | cible == `NOOP` | `rgba(158,158,158,0.2)` | « Aucune action » (abstention) |
| **L4 Cohérence** | `(cible ARMED_AWAY ∧ réel armed_away) ∨ (cible DISARMED ∧ réel disarmed)` | `rgba(76,175,80,0.2)` | nominal cohérent |
| **L5 Divergence** | opérandes dispo, réel ≠ cible, réel ≠ `triggered`, cible ≠ `NOOP` | `rgba(244,67,54,0.2)` | échec d'application |

- **Application aux deux cartes** ; sur `carte_alarme_decision`, `NOOP` passe de **vert → gris neutre `rgba(158,158,158,0.2)`** (alignement sémantique du même état entre cartes sœurs).
- **Libellés `state_display` (sans emoji — l'icône porte le signal)** : decision (réel) `triggered`→« Alarme déclenchée », indispo→« Indisponible » ; intention (cible) indispo→« Indisponible ». Icône `triggered` : `mdi:shield-alert` (vérifiée libre et cohérente avec les icônes du domaine).
- **Distinctions garanties** : gris indispo `0.1` ≠ gris neutre NOOP `0.2` ≠ rouge intrusion (libellé + icône) ≠ rouge divergence.

---

## 4. Hors‑périmètre (ne pas traiter dans ce chantier)

O‑3 (palette documentaire `90_ui`), O‑4 (carte pour `binary_sensor.blocage_armement_incoherent`), O‑5 (définition de la « cohérence globale » sous indisponibilité), O‑6 (projection du code décisionnel) ; toute refonte des dashboards/cartes ; **mutualisation** (template partagé, dépendance UI→UI, capteur runtime de divergence, nouvelle entité) ; modification de contrat, runtime, notifications, socles, navigation, identifiants ; dépôt du cadrage méthodologique transverse ; Lot 1 ECS.

---

## 5. Non‑régressions à préserver

- **ALM‑DIAG‑002** (intention) : `state_display` intention inchangé → intention lisible.
- **ALM‑DIAG‑005** (raison) : `label` de la decision inchangé → raison rendue.
- **ALM‑DIAG‑006** (NOOP ≠ indispo) : renforcé (gris indispo `0.1` vs gris neutre `0.2` explicitement distincts).
- **Notifications** (007/009/012/015) : aucun impact.
- **Runtime / décision / sûreté** : aucun impact (UI‑only).
- **Navigation & actions** : `tap/hold/double_tap` restent `none` ; badges intacts.
- **Duplication inter‑cartes** (risque central) : modification **conjointe** des deux cartes, **comparaison explicite en revue** (priorité identique), invariant documenté aux deux en‑têtes (format Arsenal existant). Non‑mutualisation → résidu accepté, à surveiller.

---

## 6. Lots & stop points

- **Lot 0** — ouverture documentaire (présent dossier + registre + index). *(Cette PR.)*
- **Lot 1** — `carte_alarme_decision` : branches L1+L2, `NOOP` neutre, `state_display` (`triggered`/indispo), icône dynamique. **Stop point** : preuves statiques + checkers ; rendu si environnement isolé.
- **Lot 2** — `carte_alarme_intention` : branche L1, `state_display` indispo, échelle alignée. **Stop point** : preuves + **cohérence inter‑cartes** (mêmes verdicts sur les 11 scénarios).
- **Preuve terrain `triggered`/indispo** : **différée** (cf. §7), hors chemin critique de merge.

---

## 7. Protocole de validation sûr

> **Règle de sûreté impérative** : **ne jamais forcer** l'état d'une entité réelle consommée par Arsenal. Surcharger `alarm_control_panel.alarme_maison` (ou un helper réel) via *Outils de développement → États* **émet un `state_changed`** susceptible de déclencher les consommateurs de `triggered` (chaînes sirène/notification). L'absence d'appel à `alarm_control_panel.alarm_trigger` **ne suffit pas**.

1. **Preuve statique exhaustive** — conditions L1–L5 **mutuellement exclusives** et **couvrant** tout le domaine (réel × cible) ; **revue croisée** des deux cartes (priorité identique). Aucun bus HA.
2. **Contrôles YAML & checkers UI** — `yamllint` ; `check_19_button_card_templates_contracts` ; `check_ui_couleurs_contracts` + `check_ui_runtime_colors_contracts` ; `docs_lint`.
3. **Rendu en environnement isolé / prévisualisation** — sans publier **aucun `state_changed`** sur le bus HA (instance de test dédiée sans automations, ou prévisualisation hors bus). **Interdit** : surcharger l'entité réelle ou les helpers réels.
4. **Preuve terrain différée** — à défaut d'environnement isolé, **différer** la preuve du rendu `triggered` (et des indisponibilités) jusqu'à une **occurrence légitime**, **sans** provoquer d'intrusion ni déclencher artificiellement le panneau, ni forcer un état consommable.

**Interdit sans nouvel arbitrage** : créer une **entité de test**. La validation des indisponibilités suit la même règle.

---

## 8. Séquence de gouvernance

Ouverture **documentaire** (ce dossier + `REGISTRE_CHANTIERS.md` + `index.md`) → **puis, en PR distincte**, patch UI (Lots 1‑2) → validation (protocole §7) → clôture. Conforme aux précédents (C20/C22 : ouverture ≠ livraison runtime).

> **La PR d'ouverture ne contient aucun patch** des cartes ni extrait YAML de solution. Le changelog de comportement interviendra **au patch UI**, pas à l'ouverture.

---

## 🔗 Références

- Audit source : [`../../01_rapports/alarme/audit_exposition_diagnostics_alarme.md`](../../01_rapports/alarme/audit_exposition_diagnostics_alarme.md)
- Contrats applicables : [`../../../contrats/alarme/10_modele_etats_et_vocabulaire.md`](../../../contrats/alarme/10_modele_etats_et_vocabulaire.md) · [`../../../contrats/alarme/90_ui.md`](../../../contrats/alarme/90_ui.md)
- Doctrine couleurs : [`../../../ui/couleurs/05_regles.md`](../../../ui/couleurs/05_regles.md) · [`../../../ui/couleurs/02_palette.md`](../../../ui/couleurs/02_palette.md)
