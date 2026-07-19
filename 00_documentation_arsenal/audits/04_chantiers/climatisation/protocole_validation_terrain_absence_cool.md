# Protocole de validation terrain — Politique d'absence COOL (C20)

| Champ | Valeur |
|---|---|
| **Chantier** | **C20** — Politique d'absence COOL (Lot 5 — validation terrain) |
| **Domaine** | Climatisation — mode COOL : absence longue, Vacances, veto composite |
| **Statut** | **Protocole ouvert (2026-07-14) — aucune preuve encore recueillie.** Le chantier C20 **n'est pas clôturable** tant que la trace §4 est vide. |
| **Contrat opposable** | [`15_absence_vacances_veto_cool.md`](../../../contrats/climatisation/15_absence_vacances_veto_cool.md) (scénarios §11) |
| **Runtime livré (Lots 1–4)** | contrats mergés #363 ; oracle #364 ; runtime #365 ; dashboard #366 |
| **Registre** | [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (ligne C20, co-commit) |

> **Nature de ce document.** Il **définit les preuves terrain** à recueillir sur l'installation réelle pour valider le comportement runtime, puis **clore** C20. Il **ne modifie aucun runtime/contrat**. Observation **en lecture seule** (Outils de développement + Historique) ; **aucune panne artificielle** n'est requise, sauf les actes opérateur explicites notés (activation Vacances, changement de réglage, reboot volontaire).

---

## 1. Objet

Confirmer, en conditions réelles, que la politique d'absence COOL livrée se comporte conformément au contrat 15 :
- veto **immédiat** sur `binary_sensor.vacances_actives = on` (indépendant de la durée) ;
- qualification d'absence longue à **échéance = début + durée réglable**, en **continuité physique** (robuste au reboot) ;
- application **immédiate** d'un changement du helper de durée ;
- **présence réelle terminale** ;
- **fail-closed** sur valeurs indisponibles/invalides.

> **Avertissement de portée.** Le passage à 14 h supprime le mécanisme causal du veto prématuré (scénario S1) mais **ne garantit pas** le confort thermique au retour. Le **résultat thermique** (température des chambres au retour) reste une observation distincte, non promise par ce lot.

---

## 2. Entités à observer

| Rôle | Entité |
|---|---|
| Autorité COOL | `binary_sensor.autorisation_clim_cool` |
| Veto composite (+ attribut `cause`) | `binary_sensor.clim_veto_absence_vacances` |
| Absence longue qualifiée (+ attributs `debut_absence`, `echeance`, `duree_ecoulee_h`) | `binary_sensor.clim_extinction_absence_prolongee_autorisee` |
| Vacances effectives | `binary_sensor.vacances_actives` |
| Horodatage de début d'absence | `input_datetime.clim_debut_absence` |
| Durée réglable | `input_number.clim_duree_absence_longue` |
| Présence débruitée / canonique | `binary_sensor.presence_confort_thermique_stabilisee` · `binary_sensor.presence_famille_unifiee` |
| Diagnostics | `sensor.clim_raison_decision` · `sensor.clim_verdict_cool` |

> **Instrumentation probatoire (2026-07-19).** Cinq de ces entités n'étaient pas
> historisées — `clim_veto_absence_vacances`, `clim_extinction_absence_prolongee_autorisee`,
> `clim_debut_absence`, `clim_duree_absence_longue`, `clim_verdict_cool` — alors que la
> trace §4 exige l'Historique : les scénarios correspondants n'étaient donc **pas
> exerçables**. Elles sont ajoutées au `recorder.yaml` en **microscope de chantier**
> (Population B, bloc propre à C20, réévaluation **2026-11-16**, retrait dès trace §4
> complète et C20 clôturé). Les événements `set_datetime` / `set_value` restent des
> preuves **complémentaires** : ils datent une écriture, ils ne restituent ni une valeur
> avant/après, ni un attribut.

---

## 2 bis. Qualification de solvabilité probatoire (L1–L5)

> **Échelle.** L1 preuve produite par le runtime · L2 conservée comme état Recorder ou
> reconstructible via les événements · L3 disponible dans la base courante · L4
> récupérable dans une ou plusieurs sauvegardes analysées hors ligne · L5 preuve
> physique, externe ou visuelle nécessitant un opérateur.

| # | Niveau | Justification |
|---|---|---|
| S1 | **L3** | veto historisé |
| S2 | **L3** | extinction, `cause` et autorisation historisés |
| S3 | **L3** | typé « historique » par le protocole |
| S4 | **L3** | `vacances_actives` déjà enregistré |
| S5 | **L3** | marqueurs `homeassistant_start` disponibles hors allowlist |
| S6 | **L3** | l'ancre devient lisible avant/après reboot |
| S7 | **L3** | `echeance` recalculée, attribut historisé |
| S8 | **L3** | idem |
| S9 | **L3** | `clim_raison_decision` déjà enregistré |
| S10 | **L3** | ancre et veto historisés |
| S11 | **L3**, sinon **L5** | aucune panne artificielle n'est demandée ; à défaut d'occurrence naturelle, qualifier différé |
| **S12** | **L5 — opérateur** | **le rendu et l'action d'une tuile ne sont pas une preuve Recorder.** Un appel `set_value` atteste d'une écriture, non de son origine ni de l'absence de logique en UI |

**Rétention.** `purge_keep_days = 30 j` : tout scénario observé doit être consigné dans la
trace §4 **sous 30 jours**. Au-delà, la preuve relève d'une analyse hors ligne sur
sauvegarde (**L4**), canal déjà éprouvé et propriété du dépôt d'audit runtime.

---

## 3. Scénarios (preuves attendues)

> Convention : chaque scénario est **PASS** si l'observation correspond à l'attendu ; sinon **FAIL** (à consigner en §4 avec capture Historique). Un scénario **non exercé** reste **à faire** — jamais présumé PASS.

| # | Situation | Attendu | Nature |
|---|---|---|---|
| **S1** | Longue journée < seuil (ex. seuil 14 h, absence ~10 h), pas de Vacances | `clim_veto_absence_vacances = off` pendant toute l'absence ; COOL reste régi par les autres conditions | terrain |
| **S2** | Absence > seuil, pas de Vacances (ex. ~16 h) | à l'échéance : `clim_extinction_… = on`, `cause = absence_prolongee`, `autorisation_clim_cool = off` | terrain |
| **S3** | Week-end non déclaré (> seuil) | veto maintenu tout le week-end ; reprise au retour | terrain / historique |
| **S4** | Activation Vacances **avant** échéance (départ, `vacances_actives → on`) | veto **immédiat** (`cause = vacances`), **sans attendre** le seuil | terrain (acte opérateur) |
| **S5** | Vacances actives au **démarrage** HA | après boot, `vacances_actives = on` reconstruit ⇒ veto immédiat | terrain (reboot volontaire) |
| **S6** | **Reboot** pendant une absence > seuil | après boot : `clim_debut_absence` conservé, `clim_extinction_… = on` (échéance dépassée) — **pas** de remise à zéro | terrain (reboot volontaire) |
| **S7** | **Réduction** du helper sous la durée déjà écoulée (absence active) | qualification **immédiate** (`echeance` recalculée, `clim_extinction_… → on`) | terrain (acte opérateur) |
| **S8** | **Augmentation** du helper pendant l'absence | `echeance` repoussée ; extinction différée en conséquence | terrain (acte opérateur) |
| **S9** | Vacances **ET** absence longue simultanément vraies | `cause = cumulé` (`sensor.clim_raison_decision = absence_et_vacances` sous besoin COOL) | terrain / historique |
| **S10** | **Retour de présence** (fin d'absence) | `clim_debut_absence` remis à la sentinelle ; `clim_extinction_… = off` ; `vacances_actives = off` ; veto tombe | terrain |
| **S11** | Valeurs indisponibles/invalides (`clim_debut_absence` sentinelle, durée `unknown`) | **fail-closed** : pas d'extinction sur ancre absente ; repli `float(14)` sur durée ; aucune autorisation par défaut au titre de l'absence | historique / observation |
| **S12** | Réglage exposé au dashboard | la tuile « Durée avant extinction (h) » modifie bien `input_number.clim_duree_absence_longue` ; aucune logique en UI | terrain (UI) |

> **Observation thermique complémentaire (non bloquante).** Au retour après une absence longue réelle, relever la température des chambres et le temps de récupération — donnée d'entrée pour un futur arbitrage (durée de préparation C21, anticipation hors Vacances D15). Ne conditionne pas la clôture de C20.

---

## 4. Trace de validation (à remplir)

| # | Date | Résultat (PASS/FAIL) | Observation / preuve (Historique) |
|---|---|---|---|
| S1 | | | |
| S2 | | | |
| S3 | | | |
| S4 | | | |
| S5 | | | |
| S6 | | | |
| S7 | | | |
| S8 | | | |
| S9 | | | |
| S10 | | | |
| S11 | | | |
| S12 | | | |

---

## 5. Critères de clôture C20

- [ ] S1, S2, S4, S6, S7, S10 **PASS** (cœur : veto immédiat Vacances, continuité physique, changement de durée, présence terminale) ;
- [ ] S5, S8, S9, S11, S12 **PASS** ou explicitement **différés/assumés** avec justification
      — **S12 est une preuve L5 opérateur** (§2 bis) : elle ne peut jamais être établie par
      l'Historique et n'est donc pas bloquante à ce titre ;
- [ ] aucun **FAIL** non résolu ;
- [ ] trace §4 remplie ; mise à jour du registre (co-commit) puis clôture en `05_clotures/climatisation/`.

**Tant que ces cases ne sont pas cochées, C20 reste ouvert.** Les Lots 1–4 (contrats, checkers, runtime, dashboard) sont livrés ; seule la **preuve terrain** manque.

---

## 6. Hors périmètre (rappel)

- Dette `_reel` / `input_boolean.clim_blocage_absence_prolongee_actif` (D14) — lot séparé.
- Préparation du retour de Vacances (C21) — dépend de C20.
- Anticipation hors Vacances (D15) — différée.

---

*Protocole de validation terrain — le chantier ne se clôt pas sans preuves.*
