# 🧠 ARSENAL — RAPPORT D'ÉCART RUNTIME
## Chauffage — Auto-ajustement courbe : représentativité non câblée (confirmation runtime)

| Champ | Valeur |
|---|---|
| **Type** | Rapport d'écart runtime |
| **Domaine** | Chauffage / Auto-ajustement courbe (pente & parallèle) |
| **Statut** | ✅ Écart confirmé runtime — correction appliquée (cf. clôture) |
| **Version** | 1.0 |
| **Date** | 2026-06-17 |
| **Méthode** | Enquête Recorder en mode `--db` (backup figé), preuve événementielle datée |
| **Autorité de référence** | Le runtime fait foi sur le comportement. |
| **Constat amont** | [`audit_auto_ajustement_courbe.md`](audit_auto_ajustement_courbe.md) — **C-GAP-1 / D-CRIT-1** |

---

## 1. Objet

Confronter au runtime le constat **D-CRIT-1** du rapport d'audit du 2026-06-03 :
*« représentativité thermique non câblée — `input_select.chauffage_representativite_thermique`
écrit mais jamais lu par la décision ».* L'audit avait reclassé ce constat sans le clore par
une preuve comportementale. Le présent rapport apporte cette preuve.

## 2. Rappel du constat antérieur (pour mémoire, non rouvert)

Le rapport d'audit conserve, après revue contradictoire, une position nuancée :

- D-CRIT-1 est **réel** dans sa lettre (le verrou de décision ne lit pas la représentativité).
- Mais le **signal** censé la porter — le proxy `pourcentage_consigne_eco_24h`
  (hystérésis 40/55) — est jugé **faible** (§5.6) : faux positifs (journées douces/ensoleillées
  déclarées représentatives à tort) et faux négatifs (journées froides rares rejetées).
- En conséquence, l'audit avait **rangé au rejeté** le branchement du proxy *tel quel*
  (« filtre médiocre ») et borné la gravité de la dérive (§5.5 : pente quasi-immunisée en climat
  doux, parallèle seul exposé, fortement amorti), **« sans trace d'une dérive observée »** (§5.4–§5.5).

Ce rapport n'infirme aucun de ces raisonnements. Il ajoute un **fait nouveau** que l'audit
n'avait pas : une trace.

## 3. Fait runtime (preuve)

Enquête Recorder en mode `--db` sur le backup figé
`Automatic_backup_2026.6.3_2026-06-17_02.30`, via
`tools/investigations/enquete_courbe_chauffe_historique.py` (lecture seule, corrélation
`chauffage_courbe_cycle_evalue` ↔ `chauffage_adjustment` par `decision_id`).

Ligne décisive (CSV `event_data`) :

```text
2026-06-16T10:00:00+02:00 · real · cycle_actionnable=True · pente 1.8→1.8 refused ·
parallèle 2.0→1.0 applied · representativite_au_cycle=NON_REPRESENTATIF ·
decision_attendue_contrat=abstention_contrat ·
ecart=VIOLATION_§8_applique_hors_representativite · confiance=OBSERVABLE
```

Lecture :

- **Date** : 16/06/2026 10:00 — cycle réel (non simulation).
- **Action réelle** : parallèle **2.0 → 1.0** appliqué (pente inchangée).
- **Représentativité au cycle** : `NON_REPRESENTATIF`.
- **Verdict** : le contrat `75` §7/§8 imposait l'abstention ; le runtime a écrit.

Cohérence temporelle : le backup est antérieur (02:30) au cycle suivant (17/06 10:00),
**absent** du backup — comme attendu. Le 17/06 vu précédemment provenait de l'API live.

## 4. Interprétation

L'écriture observée est une **baisse** du parallèle en période non représentative. C'est
exactement la matérialisation du **biais de chaleur gratuite** décrit en §5.4 du rapport
d'audit (apports non pilotés réchauffant la pièce → écart positif → suggestion de baisse → la
courbe est rabaissée à tort). La « trace » que l'audit notait absente **existe désormais**,
datée et observable.

## 5. Portée — ce que ce rapport établit, et ce qu'il ne règle pas

**Établi :**
- D-CRIT-1 a une **conséquence comportementale réelle**, pas seulement théorique.
- Au moins une **écriture réelle** de la courbe a eu lieu en période non représentative.

**Non réglé (honnêteté épistémique) :**
- La critique §5.6 sur la **qualité du signal** (`pourcentage_consigne_eco_24h`) **reste valide**.
  Sur *ce* cas précis, le proxy était **correct** (il a bien classé la période `NON_REPRESENTATIF`),
  donc une garde câblée aurait bloqué une mauvaise baisse — **un point de donnée en faveur de la
  garde**. Mais un cas favorable ne valide pas le signal en général.
- Le fait runtime du 16/06 est donc un **élément nouveau** susceptible de justifier de
  **revisiter la reclassification** de l'audit (qui avait classé le branchement du proxy au rejeté).
  Cette ré-appréciation appartient à l'arbitre du domaine ; le présent rapport la **consigne**,
  il ne la **tranche pas**.

## 6. Suites

- **Correction de l'écart de conformité** (câblage de la représentativité comme garde bloquante,
  contrat `75` §7/§8) : appliquée — voir
  [`05_clotures/chauffage/cloture_verrou_representativite_courbe.md`](../../05_clotures/chauffage/cloture_verrou_representativite_courbe.md).
- **Observabilité / historisation** (D-CRIT-2, D-CRIT-3) : l'enquête a dû moissonner la table
  `events` faute d'historisation Recorder des termes de décision. Spécification de persistance :
  [`03_plans_action/chauffage/spec_persistance_termes_decision_courbe.md`](../../03_plans_action/chauffage/spec_persistance_termes_decision_courbe.md)
  (concrétise la phase **P3** du plan d'action observabilité).
- **Qualité du signal de représentativité** (§5.6) : non traitée ; reste ouverte, à arbitrer
  à la lumière du §5 ci-dessus.
