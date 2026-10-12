# C57 — Électroménager : fin de cycle robuste (redémarrage, rechargement, front manqué)

> **Document source faisant foi du chantier C57.** Le registre
> [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) ne fait que pointer ici.
> Contrat normatif : [`contrats/electromenager.md`](../../../contrats/electromenager.md) v1.1.

## 1. Statut

**Ouvert (2026-10-12) — lot unique implémenté (runtime + contrat v1.1 + CI), validation terrain due.**
Clôture : §9.

## 2. Incident déclencheur (2026-10-11)

Constaté par l'opérateur le 2026-10-12 : notification persistante
« 🍽️ Lave-vaisselle – Cycle en cours » présente depuis 21 h, prise à 0 W.
Flag `input_boolean.lave_vaisselle_cycle` remis à `off` **à la main** par
l'opérateur. Chronologie établie par les traces natives HA (heures locales) :

| Heure | Fait | Preuve |
|---|---|---|
| avant 13:50 | début de cycle, flag `on` | traces `10080000000001` de 13:50, 14:38, 15:22, 15:29, 15:38 : `failed_conditions` (flag déjà `on`) |
| 16:18:08 | flag restauré `on`, `last_changed` remis à l'heure du démarrage | `last_changed` du flag ; `sensor.uptime` = 16:18:32 |
| 16:36 | puissance 17 W → 0 W | trace `10080000000002` (`from 17 to 0`) |
| 16:46:19 | front « < 2 W pendant 10 min » ; garde 45 min **rejetée** (28 min depuis `last_changed`) | trace `10080000000002`, `failed_conditions`, `condition/1` |
| → 2026-10-12 | aucun nouveau front (puissance restée à 0 W) : flag bloqué | état courant |

## 3. Cause racine

Deux défauts combinés, communs dans leur second terme aux deux appareils :

- **D1 — Durée non persistante (lave-vaisselle).** La garde « cycle > 45 min »
  lisait `last_changed` du flag, remis à zéro par tout redémarrage.
- **D2 — Fin sur front unique (lave-vaisselle et buanderie).** La fin dépendait
  d'un seul front `numeric_state` « < 2 W pendant N min ». Ce front est
  **consommé** même quand la condition échoue, et ne se réarme qu'en repassant
  au-dessus du seuil. D2 rend tout rejet ou toute perte de front **définitif**.

Corriger D1 seul ne corrige pas D2 (passage prématuré sous 2 W, rechargement).

### Matrice des scénarios (avant correctif)

| Scénario | Lave-vaisselle | Buanderie | Défaut |
|---|---|---|---|
| Redémarrage en cycle, front bas < 45 min après le démarrage | **bloqué** (incident) | n/a (pas de garde) | D1 + D2 |
| Puissance < 2 W avant 45 min de cycle (programme court, pause) | **bloqué** | n/a | D2 |
| Rechargement des automations alors que la puissance est déjà basse | **bloqué** (front non réarmé) | **bloqué** | D2 |
| Redémarrage / rechargement pendant la fenêtre de confirmation | **bloqué** (exécution tuée) | **bloqué** | D2 |
| Capteur indisponible pendant la confirmation | fin confirmée **sans mesure** | idem | absence de garde |
| Prise muette durablement en fin de cycle | flag `on` (fin non établie — correct) | idem | — |
| Pause > durée basse + confirmation (après 45 min) | fin puis nouveau cycle | idem | seuils (OBS-EM-2) |
| Redémarrage pendant la montée en puissance (3 min) | début manqué, aucun flag | idem | hors périmètre (OBS-EM-3) |

## 4. Conception retenue

Séparation décision / action ([`separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md)) :

| Couche | Entité | Rôle |
|---|---|---|
| Mémoire | `input_datetime.lave_vaisselle_debut_cycle` (sans `initial`, restauré) | début du cycle, écrit par `10080000000001` **avant** le flag |
| Décision | `binary_sensor.lave_vaisselle_fin_cycle_etablie` / `binary_sensor.buanderie_fin_cycle_etablie` | fin établie **sur état** : flag `on` ∧ puissance **mesurée** < 2 W ∧ (lave-vaisselle) durée > 45 min, le tout continu `delay_on` 10 / 15 min |
| Action | `10080000000002` / `10080000000004` (ID et alias inchangés) | déclenchée par la décision + réconciliations `systeme_stable → on` et `automation_reloaded` ; confirmation 5 min inchangée, puis garde « aucune reprise **et** décision toujours `on` » ; extinction du flag **puis** notification |
| UI | projections `10080000000006` / `10080000000007` | **inchangées** |

Propriétés obtenues : un front perdu ou rejeté n'est jamais définitif (la
décision est un niveau, l'action est réveillée à chaque reprise possible) ;
aucune fin sur mesure absente ; une clôture et une notification par cycle.
Seuils inchangés (30/50 W, 2 W, 10/15 min, 45 min, 5/30 W, 5 min).

**Repli de durée.** Si l'horodatage est inconnu (helper jamais écrit, p. ex.
déploiement pendant un cycle), la décision lit `last_changed` du flag, **borne
basse** de la durée réelle : fin retardée au pire de 45 min après le dernier
redémarrage, jamais anticipée, jamais bloquée.

**Écart assumé de calendrier.** Le `delay_on` porte sur la conjonction : en cas de
passage sous 2 W avant 45 min, la fin est établie à début + 55 min (au lieu de
**jamais** avant correctif ; avant correctif, une fin aurait été acceptée dès
début + 45 min si le front était tombé entre la 35ᵉ et la 45ᵉ minute). Une
remontée entre 2 et 5 W (lave-vaisselle) ou 2 et 30 W (buanderie) pendant la
confirmation repousse désormais la fin : plus prudent.

### Interactions vérifiées

- **`systeme_stable`** : simple lecture (déclencheur de réconciliation), comme
  la projection persistante et le pipeline aération (C19). Aucun écrivain ajouté.
- **Notifications** : la projection persistante est déclenchée par l'extinction
  du flag (inchangé) ; le push de fin reste unique (INV-EM-5) ; contenu des
  messages inchangé (C47).
- **Autres automatismes** : `yaourts_3h.yaml` (`10080000000005`, prise placard)
  n'a aucune relation avec les flags ; aucun dashboard, script ni décision hors
  domaine ne lit les flags (vérifié par EM-8 pour les automations et scripts).
- **Recorder / logbook** : aucun ajout (arbitrage opérateur du 2026-10-12, §6).
  `logbook.yaml` liste déjà les automations de début et de fin.

## 5. Alternatives écartées

| Alternative | Motif du rejet |
|---|---|
| Remplacer seulement `last_changed` par un horodatage | ne corrige pas D2 (passage prématuré, rechargement) |
| Réconciliation périodique (`time_pattern`) | sondage permanent ; écrase les 5 traces conservées par automation — détruit la preuve d'une vraie fin ; condition dupliquée |
| Supprimer la garde de 45 min | protection anti-pause calibrée pour la prise |
| Remise à `off` après N heures (chien de garde) | masque l'anomalie, seuil inventé (interdit opérateur, INV-EM-6) |
| Début mémorisé par un template déclenché sur le flag | dépend de l'ordre restauration ↔ chargement au démarrage (course déjà rencontrée en C15) ; l'écriture explicite est auditable |
| Template trigger inline dans l'automation de fin | condition dupliquée (déclencheur + condition) ; rechargement manqué si déjà vrai |
| Deux capteurs (« puissance basse » + « fin établie ») | sémantique de calendrier exacte, mais deux entités de plus par appareil pour un écart ≤ 10 min, et seulement en cas de fin prématurée |

## 6. Arbitrages opérateur

- **2026-10-12 — Aucun ajout au recorder**, même temporaire : le défaut ne
  justifie pas d'augmenter la collecte. Les traces natives et le CI suffisent ;
  la validation terrain (§8) s'appuie sur les traces.
- **2026-10-12 — Périmètre** : lave-vaisselle **et** buanderie (D2 commun), sans
  instrumentation supplémentaire.

## 7. Risques résiduels

- **Sémantique HA non prouvée par le CI** : restauration ou non du `delay_on` au
  démarrage, ordre des déclencheurs. La conception est sûre dans les deux cas
  (restauré `on` ⇒ confirmation puis clôture ; recalculé ⇒ clôture ≤ durée basse
  plus tard) ; à confirmer en terrain.
- **Prise muette** (OBS-EM-4), **pause longue** (OBS-EM-2), **début manqué**
  (OBS-EM-3) : limites documentées au contrat, non traitées.
- **Déploiement en plein cycle** : repli `last_changed` (§4). Déployer de
  préférence flag à `off`.
- **Fréquence de rendu** : la décision du lave-vaisselle lit `now()` (rendu à la
  minute) ; aucun attribut, donc aucun churn recorder.

## 8. Validation terrain (protocole)

Preuves = traces natives des automations `10080000000002` / `10080000000004`
(5 dernières conservées) et état des entités ; aucune instrumentation.

| # | Scénario | Attendu |
|---|---|---|
| T1 | cycle lave-vaisselle nominal | une fin, une notification ; trace `fin_etablie` → turn_off → notification |
| T2 | cycle buanderie nominal | idem |
| T3 | redémarrage HA pendant un cycle lave-vaisselle (opportuniste) | fin établie et clôturée ; aucune fin < 45 min après le début daté |
| T4 | rechargement des automations pendant une fenêtre basse ou de confirmation (opportuniste) | trace `reconciliation_rechargement` suivie de la clôture |

Échelle de solvabilité :
[`solvabilite_probatoire.md`](../../../architecture/03_doctrines/solvabilite_probatoire.md).

## 9. Critères de clôture

- PR mergée, déployée sur le clone runtime et chargée dans HA (états Git ≠
  runtime ≠ HA ≠ terrain, à qualifier séparément) ;
- T1 et T2 constatés ; T3 ou T4 constaté au moins une fois, ou absence motivée
  par décision opérateur ;
- aucun flag resté `on` après une fin établie par la mesure.

## 10. Journal

| Date | Fait |
|---|---|
| 2026-10-12 | Ouverture ; audit (§2–§3), conception validée par l'opérateur, arbitrages §6 ; lot unique : runtime, contrat v1.1, checker `check_electromenager_contracts.py` (EM-1 à EM-8, selftest 9 mutations ; preuve négative sur `main` d'avant correctif : 21 écarts). |
