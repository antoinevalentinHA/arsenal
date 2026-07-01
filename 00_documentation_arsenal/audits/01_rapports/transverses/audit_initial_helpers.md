# Audit préparatoire — Usage de `initial` dans les helpers HA

Statut : audit préparatoire — non opposable
Date : 2026-07-01
Domaine : helpers Home Assistant / restauration d’état
Objet : préparer un contrat normatif et une CI sur l’usage de `initial`
Périmètre : input_number, input_text, input_datetime, input_select, input_boolean, counter
Décision : aucune règle opposable créée par ce document

> Marquage systématique : **[FAIT]** observé · **[INFÉRENCE]** prudente · **[PROPOSITION]** normative (non opposable) · **[DÉCISION]** humaine requise.
> Ce document est un rapport d’audit. Aucune règle n’y est applicable tant qu’un contrat validé ne l’aura pas rendue opposable. Aucun contrat ni CI n’existe à ce stade.

---

## 1. Synthèse

**[FAIT]** 19 occurrences de la clé `initial` sont recensées dans les helpers YAML du dépôt. Aucune ne concerne un `input_boolean`.

**[FAIT]** Arsenal a été piégé à plusieurs reprises par un même mécanisme : sur les helpers `input_*`, poser `initial` **désactive la restauration d’état de Home Assistant** et **reforce** la valeur à chaque redémarrage, écrasant silencieusement un réglage ou un état opérateur. Trois correctifs convergents le 30/06/2026 (arrosage, météo) et un antérieur (déshumidificateur, 17/06/2026) ont retiré ces `initial` sur des paramètres réglables.

**[INFÉRENCE]** Deux usages résiduels de même nature subsistent aujourd’hui (`arrosage_fenetre_debut/fin`, `arsenal_self_audit_stale_threshold_hours`) ; leur traitement n’entre pas dans ce lot.

**[PROPOSITION]** Une doctrine est rédigeable en statut projet ; une CI est envisageable mais seulement partiellement fiable (la distinction « réglable » vs « sentinelle » est sémantique).

---

## 2. Sémantique Home Assistant de `initial`

**[FAIT]** (comportement Home Assistant, confirmé par les commentaires des correctifs du dépôt) :

- `input_number` / `input_text` / `input_datetime` / `input_select` / `input_boolean` : **restaurent leur dernière valeur au redémarrage par défaut**. Poser `initial:` **désactive** cette restauration et **reforce** la valeur à chaque démarrage.
- `counter` : possède une clé `restore` distincte ; `initial` y désigne la valeur de base / de remise à zéro. La persistance est gouvernée par `restore`, pas par la présence de `initial`. **Mécanique différente, danger moindre.**

C’est cette asymétrie qui a piégé Arsenal : sur les helpers `input_*`, `initial` ressemble à une « valeur par défaut » mais agit comme un **écrasement au reboot**.

---

## 3. Cartographie des usages actuels (19 occurrences)

**[FAIT]** Aucune occurrence dans `05_input_booleans/` (les booléens commentent explicitement leur refus d’`initial`). Recensement complet :

| # | Fichier | Domaine | Type | Entité | Valeur | Rôle apparent | Catégorie de rôle |
|---|---|---|---|---|---|---|---|
| 1 | `07_input_datetimes/arrosage/fenetre.yaml:41` | arrosage | input_datetime | `arrosage_fenetre_debut` | `"05:30:00"` | borne fenêtre, « réglable par l'opérateur » | **paramètre réglable** |
| 2 | `…/arrosage/fenetre.yaml:48` | arrosage | input_datetime | `arrosage_fenetre_fin` | `"06:30:00"` | idem | **paramètre réglable** |
| 3 | `03_input_numbers/system/audit_stale_threshold_hours.yaml:39` | arsenal_self | input_number | `arsenal_self_audit_stale_threshold_hours` | `25` | « paramètre humain modifiable depuis l'UI » | **paramètre réglable** |
| 4 | `03_input_numbers/meteo/temperature_jardin_stabilisation.yaml:84` | meteo | input_number | `temperature_jardin_etat_publie` | `-20` | mémoire filtre S(t-1), sentinelle cold-start | mémoire système / sentinelle |
| 5 | `…/temperature_jardin_stabilisation.yaml:94` | meteo | input_number | `temperature_jardin_cible_brute_derniere` | `-20` | mémoire filtre, sentinelle cold-start | mémoire système / sentinelle |
| 6 | `04_input_texts/boiler/request_id_transactionnels.yaml:50/55/60/65` | boiler | input_text | 4× `…request_id…` | `""` | corrélation transactionnelle | mémoire système / transactionnel |
| 7 | `04_input_texts/ecs/cycle_last_action_status.yaml:40` | ecs | input_text | `ecs_cycle_last_action_status` | `""` | statut dernier appel, reset en entrée d'appel | diagnostic transactionnel |
| 8 | `06_input_selects/system/transactions_bots.yaml:31` | system | input_select | (transactions bots) | `none` | état transactionnel neutre | mémoire système / transactionnel |
| 9 | `09_counters/clim_execution_retry_count.yaml:37` | climatisation | counter | `clim_execution_retry_count` | `0` | compteur de retries | compteur (mécanique `restore`) |
| 10 | `09_counters/reboot_box_tentatives.yaml:38` | reseau | counter | (tentatives reboot box) | `0` | compteur | compteur |
| 11-12 | `09_counters/transactions_bots/*.yaml:39` | system | counter | 2× | `0` | compteur transactionnel | compteur |
| 13 | `07_input_datetimes/meteo/palmares_pluie_journalier.yaml:51` | meteo | input_datetime | (palmarès pluie) | `"1970-01-01 00:00:00"` | sentinelle « jamais » | sentinelle |
| 14 | `04_input_texts/sante/cardio_nuit.yaml:9` | sante | input_text | (cardio nuit) | `source_indisponible` | sentinelle indispo au démarrage | sentinelle |
| 15 | `04_input_texts/alarme/badges.yaml:43` | alarme | input_text | (badges) | `"+CA86273E,…"` | liste de badges seed | config / mémoire utilisateur (**ambigu**) |
| 16 | `04_input_texts/alarme/code.yaml:44` | alarme | input_text | (code) | `!secret code_alarme` | code seed depuis secret | config / secret (**ambigu**) |

---

## 4. Chronologie Git des épisodes liés à `initial`

**[FAIT]** Trois correctifs convergents le **30/06/2026**, précédés des `feat` introducteurs :

| Hash | Date | Message | Fichier(s) | Extrait utile | Interprétation |
|---|---|---|---|---|---|
| `2938341` | (introd.) | feat(arrosage): parametre la duree station 1 rain bird (#113) | `03_input_numbers/arrosage/station_1_duree.yaml` | ajout `initial: 2` | **[INFÉRENCE]** Introduction du piège : durée réglable figée par `initial`. |
| `93d71b1` | (introd.) | feat(arrosage): helpers de reglage decision V1 (Lot 2) (#123) | `…/arrosage/decision_v1.yaml` | ajout `initial:` sur seuils | **[INFÉRENCE]** Même piège sur seuils de décision. |
| `89a0087` | 2026-06-17 | fix(deshumidificateur): preserve user RH thresholds | `…/deshumidificateur/cibles.yaml` | `- initial: 78` / `- initial: 73` ; commentaire « Pas d'`initial` : restaure la dernière valeur » | **[FAIT]** Premier retrait documenté : `initial` écrasait les seuils RH utilisateur. |
| `2985696` | 2026-06-30 | fix(arrosage): durée station 1 — retrait du `initial` qui écrasait le réglage au redémarrage | `…/arrosage/station_1_duree.yaml` | `- initial: 2` → commentaire « PAS de clé `initial` : elle DÉSACTIVE la restauration HA » | **[FAIT]** Cœur du piège arrosage nommé explicitement. |
| `6027097` | 2026-06-30 | fix(arrosage): retrait des `initial` sur paramètres de décision V1 et seuils pluie | `…/decision_v1.yaml`, `…/seuils_pluie.yaml` | retrait de 8 `initial` (seuil humidité 30, hystérésis 5, intervalle 24, pluie 5/10/12/5/24) ; réf. « contrat 17 §6 » | **[FAIT]** Généralisation : tous les seuils de décision/pluie réglables. |
| `f011851` | 2026-06-30 | fix(meteo): retrait des `initial` sur paramètres réglables (fraîcheur palmarès, EWMA jardin) | `…/palmares_meteo_fraicheur_jours.yaml`, `…/temperature_jardin_stabilisation.yaml` | retrait `initial: 2 / 0.3 / 0.5` | **[FAIT]** Extension hors arrosage ; **conserve** volontairement les sentinelles `-20` de mémoire filtre. |

**[FAIT]** Le commentaire correctif est déjà **standardisé** dans le dépôt :

> ⚠️ PAS de clé `initial` : elle désactive la restauration HA et reforcerait [le] réglage opérateur. Sans `initial`, HA restaure la dernière valeur réglée.

---

## 5. Mauvais usages identifiés

**[FAIT]** observés dans l’historique · **[INFÉRENCE]** pour les résiduels :

| Cas | Statut | Preuve |
|---|---|---|
| **M1** — `initial` sur paramètre réglable → écrase la restauration/calibration opérateur au reboot | **[FAIT]** | Cœur des 3 fix (seuils, durées, hystérésis, EWMA, seuils RH deshum). |
| **M2** — `initial` comme pseudo-« valeur par défaut » alors que HA restaure déjà | **[FAIT]** | Justifs d’origine « valeurs runtime saines vérifiées » (deshum `89a0087`). |
| **M3** — `initial` résiduel sur bornes de fenêtre arrosage réglables | **[INFÉRENCE]** | `arrosage_fenetre_debut/fin` : header dit « réglable par l'opérateur » **et** pose `initial`. Même classe que M1, non corrigé. |
| **M4** — `initial` résiduel sur seuil de fraîcheur audit modifiable UI | **[INFÉRENCE]** | `arsenal_self_audit_stale_threshold_hours: initial 25`, header « paramètre humain modifiable depuis l'UI ». |
| **M5** — `initial` sur intention/override/verrou (booléen) pouvant déclencher/empêcher une action au reboot | **[FAIT — risque, non réalisé]** | Aucun `input_boolean` n’utilise `initial` aujourd’hui → risque à **verrouiller préventivement**. |
| **M6** — `initial` masquant un vrai problème de `restore`/state | **[INFÉRENCE]** | Non observé directement ; à surveiller. |

---

## 6. Usages légitimes ou tolérables

**[FAIT] / [INFÉRENCE]** — usages à préserver ou tolérer :

- **B1 — Sentinelle cold-start de mémoire/filtre** : `temperature_jardin_etat_publie` / `temperature_jardin_cible_brute_derniere` : `initial -20` — démarrage déterministe voulu, **documenté** in-file (« sentinels -20 cold-start filtre, voulus »).
- **B2 — Statut/ID transactionnel remis au neutre** : `ecs_cycle_last_action_status: ""`, `…request_id…: ""`, `transactions_bots: none` — un état transactionnel *stale* survivant au reboot serait dangereux.
- **B3 — Compteur** : `initial: 0` sur `counter` (persistance gouvernée par `restore`).
- **B4 — Sentinelle « jamais »** : `palmares_pluie_journalier: 1970-01-01`, `cardio_nuit: source_indisponible`.

---

## 7. Proposition de doctrine normative

> **[PROPOSITION]** Projet de contrat — **non opposable** tant que non validé.
>
> **Titre proposé** : Contrat Arsenal — Usage de la clé `initial` dans les helpers HA
> **Statut proposé** : PROJET

### Objectif
Empêcher que `initial` désactive silencieusement la restauration HA et écrase un réglage/état opérateur ou un état persistant utile au redémarrage.

### Périmètre
`input_number`, `input_text`, `input_datetime`, `input_select`, `input_boolean`, `counter`, et tout helper YAML exposant une clé `initial`.

### Invariant principal
**[PROPOSITION]** Sur les helpers `input_*`, l’état persistant restauré par HA est la **vérité par défaut**. `initial` n’est autorisé que lorsqu’un **démarrage à valeur figée est explicitement voulu et documenté** ; il est **interdit** sur tout helper portant un réglage opérateur, une intention utilisateur persistante, un override ou un verrou.

### Définitions
- **Paramètre réglable** : helper dont la valeur est ajustée par l’opérateur (seuil, durée, borne, coefficient).
- **Intention persistante / override / verrou** : booléen ou select portant un choix devant survivre au reboot.
- **Sentinelle cold-start** : valeur neutre voulue au démarrage d’un pipeline (mémoire filtre, état S(t-1)).
- **État transactionnel** : marqueur éphémère devant repartir au neutre à chaque cycle/reboot.

### Règles normatives obligatoires (proposées)
1. **[PROPOSITION]** `initial` **interdit** sur un helper de nature *paramètre réglable*.
2. **[PROPOSITION]** `initial` **interdit** sur `input_boolean` représentant intention/override/verrou (par défaut : tout `input_boolean`).
3. **[PROPOSITION]** `initial` **autorisé** sur sentinelle cold-start / état transactionnel / compteur, **si** justifié in-file.
4. **[PROPOSITION]** Tout `initial` conservé porte une **justification standardisée** (cf. format).
5. **[PROPOSITION]** L’absence d’`initial` sur un réglage doit s’accompagner du repli de lecture côté automation (`float(...)`), déjà pratiqué (`float(0.3)`).

### Cas autorisés
B1 sentinelle cold-start · B2 transactionnel neutre · B3 compteur · B4 sentinelle « jamais ».

### Cas interdits
M1 paramètre réglable · M2 pseudo-défaut · M5 booléen intention/override/verrou.

### Cas nécessitant justification explicite
Config/secret seedé côté UI (badges alarme, code) — **[DÉCISION]** : est-ce éditable par l’opérateur (→ interdit) ou pur seed de config (→ toléré) ?

### Format de justification attendu (proposé, aligné sur l’existant)
```yaml
# initial VOULU — <sentinelle cold-start | transactionnel | compteur | sentinelle-jamais>
# Raison : <pourquoi un démarrage figé est nécessaire>
# Restauration HA volontairement désactivée : oui
```

### Exemples bons / mauvais (issus du dépôt)
- ✅ Bon : `temperature_jardin_etat_publie: initial -20` (sentinelle filtre) ; `ecs_cycle_last_action_status: initial ""` (transactionnel).
- ❌ Mauvais (corrigé) : `arrosage_seuil_humidite_declenchement: initial 30` ; `station_1_duree: initial 2` ; `cave_rh_cible_on: initial 78`.
- ⚠️ Mauvais résiduel : `arrosage_fenetre_debut/fin: initial 05:30/06:30` ; `arsenal_self_audit_stale_threshold_hours: initial 25`.

### Stratégie de migration
Phase 0 doctrine → Phase 1 CI en **WARN** (inventaire) → Phase 2 tag des `initial` légitimes avec justification → Phase 3 traitement des 2 résiduels suspects (hors de ce lot) → Phase 4 bascule **ERROR** sur `input_boolean` puis sur *paramètre réglable*.

### Limites de la CI statique
La distinction « réglable vs sentinelle » est **sémantique** : un scanner voit la présence d’`initial` et le type de helper, **pas** l’intention. La fiabilité repose sur la nature déclarée (headers `NATURE`) + exemptions in-file. → CI = **inventaire + garde-fou**, pas juge d’intention.

---

## 8. Proposition de CI contractuelle

> **[PROPOSITION]** — non implémentée. Aucune CI n’existe à ce stade.

| Élément | Proposition |
|---|---|
| **Nom du script** | `scripts/arsenal_contracts/check_initial_key_contracts.py` |
| **Emplacement** | `scripts/arsenal_contracts/` (convention existante, cf. `check_recorder_contracts.py`) |
| **Workflow** | `.github/workflows/contracts_initial_key.yml` (sur `push` + `pull_request`) — **[DÉCISION]** créer un workflow dédié ou agréger dans un checker transverse existant. |
| **Fichiers scannés** | `03_input_numbers/**`, `04_input_texts/**`, `05_input_booleans/**`, `06_input_selects/**`, `07_input_datetimes/**`, `09_counters/**` |
| **Format de sortie** | `✔/△/•` + `exit 0/1`, identique au checker recorder |
| **Règles testables** | présence d’`initial` par type de helper ; présence d’un header `NATURE: parameter`/« réglable » ; présence du bloc de justification standardisé ; `input_boolean` + `initial` |
| **Sévérité** | transitoire **WARN**, cible **ERROR** (voir matrice) |
| **Faux positifs attendus** | sentinelles/transactionnels/compteurs légitimes (B1–B4) → nécessitent exemption in-file |
| **Stratégie transitoire** | WARN d’abord (inventaire complet des 19), puis ERROR ciblé après tag des légitimes |
| **Exceptions in-file** | marqueur standardisé `# initial VOULU — …` (réutilise la convention existante). **Pas** de sidecar externe. |

---

## 9. Matrice provisoire des règles CI

> **[PROPOSITION]** — matrice de travail, non opposable.

```
Règle HINIT-001
Source normative proposée : Invariant principal + Règle 1 (paramètre réglable)
Description : `initial` présent sur input_number/input_text/input_datetime/input_select
              dont le header NATURE indique un paramètre réglable → signalement.
Type de contrôle : statique — présence `initial` + heuristique NATURE/rôle
Sévérité initiale : WARN
Sévérité cible : ERROR
Faux positifs : sentinelle/transactionnel mal étiqueté ; header NATURE absent
Décision humaine requise : définir le vocabulaire NATURE faisant foi (parameter vs sentinel)

Règle HINIT-002
Source normative proposée : Règle 2 (booléens intention/override/verrou)
Description : tout input_boolean portant `initial` → signalement.
Type de contrôle : statique — présence `initial` dans 05_input_booleans/**
Sévérité initiale : WARN
Sévérité cible : ERROR
Faux positifs : quasi nuls (aujourd'hui 0 occurrence)
Décision humaine requise : confirmer « tout input_boolean interdit d'`initial` » sans exception

Règle HINIT-003
Source normative proposée : Règle 4 (justification obligatoire)
Description : `initial` conservé sans bloc de justification standardisé → signalement.
Type de contrôle : statique — présence `initial` sans marqueur `# initial VOULU —`
Sévérité initiale : WARN
Sévérité cible : WARN (documentaire)
Faux positifs : formats de justification hétérogènes existants
Décision humaine requise : figer le format exact du marqueur

Règle HINIT-004
Source normative proposée : Cas autorisé B3 (compteur)
Description : `counter` avec `initial` → INFO ; vérifier `restore` explicite.
Type de contrôle : statique — présence `initial`/`restore` dans 09_counters/**
Sévérité initiale : INFO
Sévérité cible : INFO
Faux positifs : nuls
Décision humaine requise : exiger ou non `restore:` explicite sur chaque counter

Règle HINIT-005
Source normative proposée : Cas nécessitant justification (config/secret UI)
Description : `initial` sur helper de config/secret potentiellement éditable UI
              (badges alarme, code) → signalement pour arbitrage.
Type de contrôle : statique — liste ciblée + présence `!secret`/valeur seed
Sévérité initiale : WARN
Sévérité cible : DÉCISION (interdit ou toléré)
Faux positifs : dépend de l'éditabilité réelle
Décision humaine requise : trancher éditable-opérateur vs seed-config
```

---

## 10. Décisions humaines nécessaires

**[DÉCISION]** avant création du contrat :
1. Sort-on `counter` du périmètre dur (mécanique `restore` distincte) ?
2. « Tout `input_boolean` interdit d’`initial` » : absolu ou avec exception encadrée ?
3. Traitement des 2 résiduels suspects (`arrosage_fenetre_*`, `arsenal_self_audit_stale_threshold_hours`) : reconnus comme non-conformes dès le contrat, ou laissés au lot correctif ultérieur ?
4. Statut des seeds config/secret (badges, code alarme) : réglage opérateur (interdit) ou config (toléré) ?
5. Vocabulaire `NATURE` faisant foi pour distinguer *parameter* de *sentinelle/transactionnel*.

**[DÉCISION]** avant codage de la CI :
1. Workflow dédié `contracts_initial_key.yml` vs agrégation dans un checker transverse.
2. Format exact et unique du marqueur d’exemption in-file (`# initial VOULU — …`).
3. Seuil de bascule WARN→ERROR (par règle et par type de helper).
4. La CI lit-elle les headers `NATURE` comme source de vérité (fiabilité dépendante de leur présence/qualité) ou reste-t-elle sur la seule présence d’`initial` ?

---

## 11. Conclusion

- **Contrat** : **rédigeable tel quel** en statut *projet*. La doctrine est solidement étayée (3 correctifs convergents, rationale déjà standardisée, contraste bon/mauvais dans un même fichier). Restent des arbitrages de périmètre, pas de manque d’information.
- **CI** : **partiellement fiable seulement**. Un scanner statique **inventorie** `initial` et applique des garde-fous par type de helper, mais **ne peut pas juger l’intention** (réglable vs sentinelle) — d’où WARN + exemptions in-file curées humainement.

Ce document reste un **audit préparatoire non opposable**. Il ne crée ni contrat, ni CI, ni règle applicable. Les passages **[PROPOSITION]** demeurent des propositions et les passages **[DÉCISION]** des arbitrages à trancher avant toute suite.
