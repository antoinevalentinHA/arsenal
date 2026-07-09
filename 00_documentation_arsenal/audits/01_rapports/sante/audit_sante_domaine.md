# 🫀 ARSENAL — AUDIT — Domaine **Santé** (cardio nocturne + sommeil, source Withings)

> **Trace d'audit documentaire, lecture seule.** Aucune correction runtime : ni script, ni automation, ni template, ni dashboard, ni contrat, ni checker modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse dépendant d'un comportement Withings/HA non instrumenté ici · **[RECO]** recommandation.
> Sources normatives : [`../../../contrats/sante/cardio_nuit.md`](../../../contrats/sante/cardio_nuit.md) (v2.1, NORMATIF), [`sommeil.md`](../../../contrats/sante/sommeil.md) (v1.0, NORMATIF). **Aucun checker, aucun workflow** ne couvre ce domaine.

---

## Verdict

**Cœur de consolidation fidèle aux contrats, mais domaine sensible fragilisé par trois écarts P2 et sans aucun garde-fou mécanique.** Le noyau (source cardio unique, bornes physiologiques, capteurs métier, invariant « anomalie impossible sur nuit invalide », sole-writer du snapshot cardio) est **conforme et bien construit**. Mais l'audit relève, sur un domaine **santé** fraîchement promu en NORMATIF :

1. **[FAIT] Cécité à la fraîcheur de la source (P2).** La chaîne lit des caches `_local` qui **persistent la dernière valeur et masquent l'indisponibilité** ; aucune garde de récence ne vérifie que la donnée provient de la nuit écoulée. Une valeur périmée (nuit J-1) peut être **consolidée comme nuit courante** — côté cardio, elle pollue la baseline 7 j qui sert à détecter les anomalies.
2. **[FAIT] 4 violations réelles de la frontière de consommation (P2).** Trois cartes du dashboard sommeil et une carte cardio lisent directement des entités **interdites** (caches `_local`, helper snapshot) — faute d'entité conforme exposée pour le besoin UI.
3. **[FAIT] Zéro couverture CI (P2).** Aucun checker ne garde les 7 violations énumérées au §9 cardio ni les invariants INV-SOM-1..7. Les 4 violations ci-dessus **auraient été captées** par un checker.

**Gravité globale : P2.** Aucun **P1** : le domaine **n'actionne rien** et **n'émet aucune alerte santé** (les alertes sont hors périmètre par design — cf. SANTE-05). Les écarts dégradent la **justesse du signal** et l'**observabilité**, pas la sûreté physique.

> **Note de recadrage.** La photographie de couverture normative (état daté 2026-06-07) classait `sante` en « contrats DRAFT / renvoi mort ». C'est **périmé** : `cardio_nuit.md` a été promu **v2.1 NORMATIF** le 2026-06-07 (renvoi mort `CONTRAT_ALERTE_SANTE.md` retiré) et `sommeil.md` réécrit en **v1.0 NORMATIF** aligné sur le runtime réel. Le présent audit porte donc sur des contrats **opposables**, pas des brouillons.

---

## 1. Périmètre & méthode

- **Périmètre :** `10_scripts/sante/`, `11_automations/sante/`, `12_template_sensors/sante/`, `13_sensor_platforms/statistics/sante/`, dashboards `18_lovelace/dashboards/{sante,sommeil}/` + `includes/cartes/sante/`, croisés avec les 2 contrats.
- **Méthode :** lecture intégrale des deux contrats et du cœur runtime (consolidation cardio + sommeil, capteurs métier, caches `_local`) → recensement des violations de frontière de consommation (INV-SOM-1, cardio §2/§6/§9) sur tout le dépôt → analyse des chemins de fraîcheur/idempotence.

**Architecture [FAIT].** Source unique = montre Withings (Sleep Analyzer / ScanWatch). Chaîne : natif Withings (cloud instable) → cache `_local` (anti-`unknown`) → agrégat/gate (sommeil) ou lecture directe (cardio) → **consolidation matinale** dans des helpers snapshot → capteurs métier dérivés → UI. Deux consolidations distinctes : `script.consolider_cardio_nuit` (via `cardio_consolidation.yaml`) et `sommeil_consolidation.yaml`.

---

## 2. Ce qui est sain (à préserver)

- **[FAIT] Cardio — sole-writer & invariants.** Seul `10_scripts/sante/cardio_nuit.yaml` écrit les 7 helpers snapshot cardio (vérifié sur tout le dépôt). Bornes physiologiques [35 ; 90] appliquées ; `historique_7j` alimenté **uniquement** sur nuit valide ; mémoire `cardio_anomalie_nuit_precedente` **préservée** sur nuit invalide (continuité §5.3) ; `binary_sensor.cardio_anomalie` **ne peut pas être ON si `cardio_nuit_valide=off`** (invariant §5.3 respecté) ; baseline `cardio_baseline_7j` exige ≥ 4 entrées (§4.2).
- **[FAIT] Sommeil — consolidation gardée & idempotente-au-succès.** `sommeil_consolidation.yaml` : gate `sommeil_donnees_exploitables` + **double validation interne** avant écriture ; idempotence clé sur `sommeil_derniere_nuit_date` écrite **seulement en cas de succès** → **retry 09/10/11h jusqu'au succès** (INV-SOM-3/4).
- **[FAIT] Canal mobile propre.** L'unique notification du domaine (`notification_batterie_montre.yaml`) passe par `script.notification_envoyer` avec titre emoji conforme au contrat notifications.
- **[FAIT] Honnêteté des contrats.** `sommeil.md` documente ses dettes (DETTE-SOM-1..4) et disclaim explicitement la fraîcheur (INV-SOM-7) ; `cardio_nuit.md` déclare hors périmètre les alertes santé.

---

## 3. Constats

Codes stables `SANTE-xx`.

| Code | Objet | Écart | Prio |
|---|---|---|---|
| **SANTE-01** | Cécité à la fraîcheur de la source | Les caches `_local` **persistent la dernière valeur** et **masquent l'indisponibilité** (`capteurs_locaux.yaml`, `*withings_state_int`/`_float_*` → `{{ old }}`). Aucune garde de récence ne vérifie que la donnée est bien de la nuit écoulée. Une valeur périmée, **plausible et « stable » par immobilité**, est consolidée comme nuit courante. Touche **les deux chaînes** ; côté cardio elle **pollue `historique_7j`/baseline**. | **P2** |
| **SANTE-02** | 4 violations réelles de la frontière de consommation | Dashboards lisant des entités **interdites**, faute d'entité conforme exposée : `sommeil/principal.yaml:64/84/96` → caches `_local` réveils/ronflements (INV-SOM-1/§10) ; `includes/cartes/sante/graph_cardio_nuit.yaml:37` → helper `input_number.cardio_nuit_moyenne` (cardio §2/§6/§9). | **P2** |
| **SANTE-03** | Zéro couverture CI sur domaine normatif sensible | Aucun `check_sante_*.py`, aucun workflow. Les 7 violations §9 cardio et les invariants INV-SOM-1..7 sont **non gardés** ; les violations SANTE-02 seraient captées par un checker. | **P2** |
| **SANTE-04** | Cardio : idempotence « first-attempt-wins » | L'idempotence de `cardio_consolidation.yaml` est clé sur `cardio_nuit_horodatage`, écrit **inconditionnellement** à chaque run (valide **ou** invalide) → **pas de retry** : la première tentative du jour verrouille la journée. Asymétrie avec le sommeil (retry-jusqu'au-succès). | P3 |
| **SANTE-05** | Détection sans escalade (design à arbitrer) | Une anomalie cardiaque nocturne **confirmée** (`binary_sensor.cardio_anomalie`, `confirmation=true`) ne déclenche **aucune notification** — seule la **batterie faible** notifie. Alertes santé hors périmètre par design ; `cardio_anomalie` n'est qu'un « input candidat » pour un contrat d'alerte inexistant. | P3 |

### Détails porteurs

**SANTE-01 — fraîcheur.** [FAIT] `withings_average_heart_rate_local` (`capteurs_locaux.yaml:92-96`) renvoie `{{ old }}` (dernière valeur, défaut 0) quand la source native est `unavailable`. Conséquence dans `10_scripts/sante/cardio_nuit.yaml` : `source_indisponible` (valeur `none`) est **quasi inatteignable** (le cache renvoie toujours un nombre), et `stable_30_minutes` (`(now − last_changed)/60 ≥ 30`) est **satisfait par l'immobilité** d'une valeur non rafraîchie. [HYP] Au trigger `09:00` (`cardio_consolidation.yaml:42`), si Withings n'a pas encore publié la nuit, le script fige la FC d'hier comme nuit courante (`valide=on`), l'ajoute à `historique_7j` (doublon) et fausse la baseline — dégradant la détection d'anomalie, seul livrable du domaine. Le sommeil partage la cécité au niveau du gate (mais son retry et sa borne `total≥4` l'atténuent). [RECO] Garde de récence : lire la disponibilité/`last_changed` de l'entité **native** (non masquée) et exiger une mise à jour postérieure à minuit local avant de consolider ; ou requalifier `source_indisponible` sur la native.

**SANTE-02 — frontière sans path conforme (racine commune).** [FAIT] Les 4 lectures interdites sont vérifiées au fichier. **Racine :** le contrat interdit les couches amont mais **n'expose aucune entité conforme** pour ces besoins UI légitimes — il n'existe **pas** de snapshot Couche 3 pour les indicateurs secondaires (réveils, ronflements) que le contrat inscrit pourtant au périmètre (§1), ni de **capteur numérique de FC** exposé pour tracer l'historique (les 3 sensors autorisés sont qualitatif/écart/binaire). [RECO] Deux options par cas : (a) **exposer l'entité sanctionnée** (snapshot Couche 3 pour réveils/ronflements ; `sensor.cardio_nuit_moyenne` miroir du helper) et rebrancher les cartes dessus ; ou (b) **carve-out explicite** « UI/diagnostic » (comme §11 sommeil pour les capteurs couleur) actant ces lectures. À trancher par le propriétaire — soit la frontière est corrigée, soit elle est amendée.

**SANTE-03 — CI absente.** [FAIT] `ls scripts/arsenal_contracts/ | grep sante` = vide. [RECO] `check_sante_contracts.py` candidat : sole-writer des helpers cardio ; non-consommation externe des entités interdites (INV-SOM-1 §10, cardio §2) — aurait capté SANTE-02 ; `cardio_anomalie` OFF si `cardio_nuit_valide=off` ; baseline ≥ 4 entrées ; `historique_7j` écrit seulement sur nuit valide (là où c'est statiquement vérifiable).

**SANTE-04 / SANTE-05 — bords.** [FAIT] SANTE-04 : `cardio_nuit_horodatage` écrit hors du `choose` (`cardio_nuit.yaml:174-178`), donc à chaque run ; une première tentative invalide (démarrage à froid `0`, `hors_plage`, ou pré-sync) bloque l'arrivée réelle. [RECO] Clé d'idempotence sur consolidation **valide** uniquement (aligner sur le sommeil). [FAIT] SANTE-05 : aucune automation ne consomme `binary_sensor.cardio_anomalie` pour notifier ; `notification_batterie_montre.yaml` notifie un seul destinataire sur transition→`low`. [RECO] Décision propriétaire : escalade d'une anomalie **confirmée** (contrat d'alerte santé dédié), ou statu quo assumé.

---

## 4. Axes non audités dans cette passe (honnêteté de périmètre)

- **Les familles respiration / activité** (`withings_*respiratory*`, steps, calories, distance) et leurs statistiques : hors des deux contrats audités (ni sommeil interdit, ni source cardio) — non traitées.
- **Le groupe `02_groups/integrations/withings.yaml`** référence des entités Couche 0 natives : non-violation au sens strict (agrégation statique, ni UI ni décision), mais **vecteur latent** de contournement si le groupe venait à être affiché/décisionnel — à surveiller.
- **Le comportement réel Withings** (délais de publication post-réveil, fréquence de sync) : non observé runtime ; l'audit est statique.

---

## 5. Priorisation des suites (aucune appliquée — arbitrage propriétaire requis)

**P2 :**
1. **SANTE-03** : créer `check_sante_contracts.py` (garde les invariants + capte SANTE-02) — plus fort levier, sans risque runtime.
2. **SANTE-02** : par cas, exposer l'entité conforme **ou** amender le contrat (carve-out UI) ; rebrancher les 4 cartes.
3. **SANTE-01** : garde de récence sur la source (native, non masquée) avant consolidation.

**P3 :**
4. **SANTE-04** : idempotence cardio sur consolidation valide (retry-jusqu'au-succès).
5. **SANTE-05** : arbitrer l'escalade d'une anomalie cardiaque confirmée.

---

## 6. Statut

- Audit : **lecture seule** — aucun runtime, contrat, checker, workflow ou dashboard modifié.
- Domaine : **non clôturé** ; constats `SANTE-01…05` ouverts, arbitrage propriétaire requis avant toute correction.
- Suites : ne maintiennent pas l'audit ouvert ; un chantier dédié pourra les porter.
