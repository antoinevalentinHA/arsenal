# 🔌 ARSENAL — AUDIT — Domaine transverse **Résilience des intégrations**

> **Trace d'audit documentaire, lecture seule.** Aucune correction runtime : ni script, ni automation, ni registre, ni contrat, ni checker modifiés.
> Convention : **[FAIT]** observé · **[HYP]** hypothèse · **[RECO]** recommandation.
> Source normative : [`../../../contrats/resilience_integrations.md`](../../../contrats/resilience_integrations.md) (v1.1, NORMATIF). Vérification mécanique : `scripts/arsenal_contracts/check_resilience_integrations_contracts.py` (autorité = `resilience_integrations_registre.yaml`, workflow `contracts_resilience_integrations.yml`).

---

## Verdict

**Domaine exemplaire — conformité runtime intégrale sur les invariants audités ; seules des dettes auto-déclarées et arbitrées subsistent.** Le script canon de reprise et les 7 automations de décision respectent l'ensemble du contrat : deux axes orthogonaux, gardes de sûreté paramétrées, délégation à une action unique, câblage WAN correct. La CI tourne en **report-only avec `STRICT_ON_NEW=1` réellement armé** — les dettes documentées sont tolérées, tout écart **nouveau** échouerait.

**[FAIT] Script canon (`resilience_integration_recover`) conforme.** Garde panne secteur et garde WAN **paramétrées** (`wan_entity`, jamais codée en dur) n'inhibant que `op=attempt` (jamais `reset`/`block`) ; incident confirmé = gel **OU** indisponibilité (non-substitution §3) ; succès = âge < ok **ET** indisponibilité levée (deux axes) ; backoff borné `min((n+1)·10, cap)` ; plafond 5 → `block` ; action unique (reload_entry / addon_restart).

**[FAIT] Couche décision (7/7 automations) conforme.** Chacune des 6 chaînes à canon d'âge (Netatmo, Airstage, HomeKit, Overkiz, SwitchBot, Synology) déclenche sur les **deux axes** (`gel_avere_<X>` **et** `indisponibilite_franche_<X>`) — aucune chaîne aveugle (§6) ; sous garde `systeme_stable`, `mode: single`, `max_exceeded: silent`, sans `time_pattern` ; délègue au canon. Zigbee2MQTT = exception native documentée (disponibilité bridge + `addon_restart` inline).

**[FAIT] Câblage WAN parfait (§11).** Les 2 `cloud_wan` (Netatmo, Overkiz) transmettent `wan_entity: binary_sensor.contexte_wan_indisponible` sur `op=attempt` ; les 4 `local_lan` (Airstage, HomeKit, SwitchBot, Synology) ne le transmettent **jamais** — aucune fuite qui inhiberait une intégration locale sur un signal WAN.

**Gravité globale : P3.** Aucun écart de conformité runtime ; les constats sont des dettes déclarées à arbitrer et un point documentaire.

---

## 1. Périmètre & méthode

- **Périmètre :** contrat + registre `resilience_integrations_registre.yaml`, script canon `10_scripts/system/resilience_integration_recover.yaml`, les 7 automations `11_automations/system/reload_integrations/`, capteurs d'âge `12_template_sensors/system/integrations/`.
- **Méthode :** lecture du contrat, du registre et du script canon → recensement des invariants sémantiques de la couche décision (deux axes, gardes, délégation, câblage WAN) → exécution du checker en modes `report` et `STRICT_ON_NEW=1` → vérification de l'invariant de fraîcheur (`last_reported`).

**Modèle [FAIT].** Deux axes orthogonaux non substituables : **fraîcheur** (âge dérivé du `last_reported` le plus récent — liveness) et **disponibilité** (comptage de membres exploitables). Recovery via **script canon unique** (attempt/reset/block), inhibé en panne secteur (inv 8) et — pour les `cloud_wan` — en contexte WAN indisponible (inv 11).

---

## 2. Ce qui est sain (à préserver)

- **[FAIT] Invariant de fraîcheur respecté.** `12_template_sensors/system/integrations/age_des_donnees.yaml` dérive l'âge de `last_reported` (`:45,48`) et documente explicitement le refus de `last_updated`/`last_changed` (`:18-25`) — évite les faux gels sur intégration saine mais « calme » (inv 1).
- **[FAIT] Report-only honnête.** Le checker sépare `present` / `absent_non_conforme_temporaire` (dette) / `non_applicable` (hors périmètre). Résultat : **97 PASS / 8 DETTE / 1 EXCEPTION / 1 WARN / 0 FAIL**. `STRICT_ON_NEW=1` est posé dans le workflow (`contracts_resilience_integrations.yml:12`) : un écart nouveau bloquerait — la garde anti-régression revendiquée **existe réellement**.
- **[FAIT] Exception modèle.** Zigbee2MQTT (`disponibilite_native`) est correctement traité en exception documentée, conservant backoff/plafond/anti-boucle/garde `systeme_stable`.

---

## 3. Constats

| Code | Objet | Écart | Prio |
|---|---|---|---|
| **RESIL-01** | Chaînes orphelines Audi & Withings (dette §8 auto-déclarée) | Infrastructure diagnostic présente, mais **aucune automation de décision, aucun compteur, aucun axe disponibilité**. Conséquence : un gel/indisponibilité d'Audi ou de Withings est **diagnostiqué mais jamais traité** (pas de recovery automatique). Inscrites au registre comme dettes report-only à arbitrer (compléter ou décommissionner). | P3 |
| **RESIL-02** | Overkiz — pertinence runtime à confirmer (registre WARN) | Le registre porte `a_confirmer_runtime` : seuil de gel 90 min et comptage des membres exploitables du groupe (entités d'état `binary_sensor`/`number`/`water_heater`) **à valider sur données réelles**. | P3 |
| **RESIL-03** | Commentaire d'en-tête Netatmo périmé | L'en-tête de `netatmo.yaml` annonce un seuil « ≥ 45 min » alors que le code (et le registre) utilisent **70**. Cosmétique, pas d'impact runtime. | P3 |

### Détail — RESIL-01 & couplage inter-domaines

[FAIT] Registre : Audi et Withings ont `automation`, `compteur_tentatives`, `binaire_indisponibilite` en `absent_non_conforme_temporaire`, `mode: orpheline_a_arbitrer`. Le checker les compte en DETTE (report-only), pas en FAIL.

[HYP → à arbitrer] **Couplage avec l'audit Santé.** `Withings` est la **source unique** du domaine Santé ([`../sante/audit_sante_domaine.md`](../sante/audit_sante_domaine.md)). Sa chaîne de résilience étant **orpheline**, un gel Withings n'est **pas auto-récupéré** — ce qui prolonge la fenêtre de données périmées et **aggrave `SANTE-01`** (cécité à la fraîcheur : le cache `_local` persiste la dernière valeur). Compléter la chaîne Withings (automation de décision + axe disponibilité) atténuerait les deux constats à la fois. À arbitrer conjointement.

---

## 4. Axes non audités dans cette passe (honnêteté de périmètre)

- **Le comptage réel des « membres exploitables »** par groupe source (axe disponibilité) : logique des binaires `indisponibilite_franche_*` non dépliée capteur par capteur ; l'audit s'est concentré sur la décision et le canon.
- **Le comportement runtime** (déclenchement réel d'un recovery, backoff observé) : non observé ; audit statique.
- **La cohérence seuils registre ↔ automations** au-delà des cas vus : déléguée au checker (R6 « seuils alignés » vert).

---

## 5. Priorisation des suites (aucune appliquée — arbitrage propriétaire requis)

**P3 :**
1. **RESIL-01** : arbitrer Audi & Withings (compléter la chaîne — automation décision + compteur + axe disponibilité — ou décommissionner). Prioriser **Withings** pour le bénéfice croisé sur `SANTE-01`.
2. **RESIL-02** : valider sur données réelles le seuil Overkiz (90) et le comptage de membres, puis retirer le `a_confirmer_runtime`.
3. **RESIL-03** : corriger le commentaire d'en-tête Netatmo (70).

---

## 6. Statut

- Audit : **lecture seule** — aucun runtime, registre, contrat ou checker modifié.
- Domaine : **exemplaire, non clôturé** ; constats `RESIL-01…03` ouverts (dettes déclarées + doc), arbitrage propriétaire requis.
