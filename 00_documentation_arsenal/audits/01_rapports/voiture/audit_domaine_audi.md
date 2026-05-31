# 🚗 ARSENAL — AUDIT DU DOMAINE AUDI — **VERSION FINALE (réconciliée runtime)**

> Version finale, supersède les deux précédentes. Constats réconciliés avec le runtime Home Assistant.
> Principe respecté : le runtime fait foi ; toute affirmation est tracée à une preuve (dépôt ou test runtime) ; le mécanisme non observé n'est pas affirmé.

---

## Verdict global

**Le domaine Audi fonctionne correctement au runtime.** La couche de stabilisation, le snapshot atomique de pleine charge, la corrélation thermique, l'archivage mensuel et les dashboards sont opérationnels. Les prédictions de panne du rapport initial (AUDI-01, 02, 03-distance, 09, 10) étaient **erronées** : le registre d'entités compensait des écarts de nommage que le dépôt seul ne pouvait révéler.

Les sujets qui subsistent ne sont **pas des bugs visibles** ; ce sont des dettes de **gouvernance documentaire**, de **qualité du checker contractuel**, de **reproductibilité dépôt → runtime**, et un **nettoyage recorder**.

---

## Tableau de statut final

| ID | Constat | Statut final | Gravité | Preuve |
|---|---|---|---|---|
| **AUDI-11** | Reproductibilité dépôt → runtime non garantie | **Confirmé (enseignement principal)** | 🟠 Majeur | Runtime + dépôt |
| AUDI-04 | Ouvrants/sécurité hors contrat | Confirmé | 🟠 Moyen | Runtime + dépôt |
| AUDI-05 | Angle mort du checker CI | Confirmé | 🟠 Moyen | Dépôt |
| AUDI-03 | Lignes recorder fantômes (partie recorder) | Confirmé par test runtime | 🟡 Faible | Runtime |
| AUDI-06 | Dashboard batterie + libellé « hebdomadaire » | Mineur | 🟡 Faible | Dépôt |
| AUDI-07 | ID automatisation à 14 chiffres | Mineur | 🟡 Faible | Dépôt |
| AUDI-08 | Statistique température sans `unique_id` | Mineur | ⚪ Info | Dépôt |
| AUDI-01 | Divergence `entity_id` / `unique_id` | Invalidé (fonctionnel) | ⚫ Clos | Runtime |
| AUDI-02 | Naming statistique `etron`/`e_tron` | Invalidé (fonctionnel) → cas de AUDI-11 | ⚫ Clos | Runtime |
| AUDI-03 | « Distance non historisée » | Invalidé | ⚫ Clos | Runtime |
| AUDI-09 | Plafond `max: 100` | Invalidé | ⚫ Clos | Runtime |
| AUDI-10 | Sémantique `primary_engine_percent` | Invalidé | ⚫ Clos | Runtime |

---

## Constats actifs

### AUDI-11 — Reproductibilité dépôt → runtime non garantie — **MAJEUR (enseignement principal)**

- **Description** : le runtime dépend d'un état du registre d'entités **non représenté dans le dépôt**. Pour certaines entités, l'`entity_id` réel diffère de celui qu'un déploiement à blanc depuis le dépôt générerait par défaut (slug du `name`, ou clé de configuration). Un redéploiement neuf (reprise après sinistre, migration, instance vierge) ne reproduirait donc **pas** le runtime fonctionnel sans intervention.

- **Preuve (divergence — établie)** :
  - Statistique autonomie : runtime `entity_id = sensor.autonomie_audi_e_tron_mensuelle`, `friendly_name = "Autonomie Audi etron Mensuelle"`. Le `name` du dépôt (`13_sensor_platforms/statistics/voiture/autonomie.yaml:39` → « Autonomie Audi etron Mensuelle ») slugifie en `…_etron_mensuelle`, **différent** de l'`entity_id` runtime `…_e_tron_mensuelle`.
  - Compteurs distance : runtime `sensor.distance_audi_e_tron_mensuelle` (=1009.0) / `…_annuelle` (=4817.0), alors que `utility_meter.yaml:261,268` définit les clés `audi_e_tron_distance_mois` / `…_an` (l'`entity_id` d'un utility_meter dérive de la clé), **différentes**.

- **Limite de preuve (mécanisme — NON établi)** : les données démontrent la divergence dépôt ↔ runtime et le risque de reproductibilité, mais **pas le mécanisme** qui l'a produite. Plusieurs causes sont compatibles avec les observations (entity_id figé à la création sous un `name`/clé antérieur puis YAML édité ensuite ; renommage en UI ; migration). Le mécanisme exact n'a pas été observé et n'est donc pas affirmé.

- **Impact** : la chaîne d'archivage mensuel et les cartes batterie/distance reposent sur un état du registre non versionné. C'est un risque de **reprise après sinistre et de gouvernance**, pas un dysfonctionnement courant — mais il contredit le principe Arsenal « le dépôt est la vérité ».

### AUDI-04 — Sous-système ouvrants/sécurité hors contrat — **MOYEN (dette documentaire)**

- **Description** : portes (×4), fenêtres (×4), coffre verrouillé, toit ouvrant existent au runtime et alimentent `audi_securite.yaml`, sans aucune mention dans le contrat `voiture.md`.
- **Preuve** : runtime (entités exposées) ; `12_template_sensors/voiture/ouvertures/**` ; `18_lovelace/dashboards/voiture/audi_securite.yaml:53-141` ; recherche ouvrants dans `voiture.md` = 0 occurrence.
- **Impact** : dette **documentaire**. Un pan réel du domaine échappe à la gouvernance normative et n'est pas testé par le checker.

### AUDI-05 — Angle mort du checker contractuel — **MOYEN**

- **Description** : `check_voiture_contracts.py` valide par `unique_id` et ne vérifie jamais la concordance avec l'`entity_id` réellement consommé, ni la statistique, ni le recorder, ni les ouvrants.
- **Preuve** : `scripts/arsenal_contracts/check_voiture_contracts.py` (T03 `is_declared_as_unique_id` ; T04 regex `sensor\.\w+_local` seule) + `.github/workflows/contracts_voiture.yml`.
- **Impact** : c'est précisément l'outil qui aurait dû détecter AUDI-11 et AUDI-03 (recorder). La CI reste verte malgré les dettes réelles.

### AUDI-03 (partie recorder) — Lignes recorder fantômes — **FAIBLE (confirmé runtime)**

- **Description** : `recorder.yaml:415-417` référence trois entités inexistantes.
- **Preuve (runtime, test direct)** : `sensor.audi_a3_sportback_e_tron_range_local`, `…_charging_state_local`, `…_primary_engine_percent_local` → tous **`unknown`** au runtime. Ce sont les formes `unique_id` des capteurs locaux, dont les `entity_id` réels sont en `audi_e_tron_*_local`.
- **Impact** : trois inclusions recorder mortes (sans effet, à purger). La partie « distance non historisée » du constat initial est invalidée (lignes 419-420 correctes).

### Mineurs
- **AUDI-06** : libellé « Moyenne hebdomadaire (km) » sur un capteur à fenêtre 31 j — `18_lovelace/dashboards/voiture/audi_batterie.yaml:57`. Faible.
- **AUDI-07** : `id: "10150000000005"` à 14 chiffres vs 13 ailleurs — `11_automations/voiture/notification_etat_charge.yaml`. Faible.
- **AUDI-08** : statistique `temperature_charge.yaml` sans `unique_id` — non gérable en UI ; asymétrie avec son jumeau autonomie. Info.

### Clos (invalidés au runtime)
- **AUDI-01** — capteurs locaux `audi_e_tron_*_local` présents et alimentés. Subsiste au plus une dette cosmétique (le `unique_id` ne décrit pas l'entité consommée), sans incidence.
- **AUDI-02** — `sensor.autonomie_audi_e_tron_mensuelle` existe (valeur 32.05), consommateurs OK. Cas particulier de AUDI-11.
- **AUDI-09** — runtime 23-34 km, plafond 100 jamais approché.
- **AUDI-10** — `primary_engine_percent` = 72 % cohérent avec un SoC batterie PHEV.

---

## Recommandations finales

### 🟠 Importante
1. **Restaurer la reproductibilité (AUDI-11)** — aligner le dépôt sur le runtime de façon qu'un déploiement neuf reproduise les `entity_id` fonctionnels, soit en ajustant les `name:`/clés, soit en déclarant des `entity_id:` explicites. Concerne au moins : statistique autonomie mensuelle, compteurs distance mensuel/annuel.
2. **Renforcer le checker (AUDI-05)** — résoudre `name → slug` / clé → `entity_id` et vérifier que chaque `entity_id` consommé est effectivement produit ; idéalement, comparer le dépôt à un export du registre. Étendre la couverture aux ouvrants et au recorder.
3. **Statuer sur les ouvrants (AUDI-04)** — les contractualiser dans `voiture.md` ou les exclure explicitement du périmètre.

### 🟢 Confort
4. Purger `recorder.yaml:415-417` (AUDI-03, fantômes confirmés).
5. Corriger le libellé « hebdomadaire » → « mensuelle » (AUDI-06).
6. Ajouter un `unique_id` à la statistique température (AUDI-08).
7. Harmoniser l'ID `10150000000005` sur 13 chiffres (AUDI-07).

### ⚫ Aucune action
- AUDI-01, AUDI-02, AUDI-09, AUDI-10.

---

## Enseignement de l'audit

Le domaine est sain en exploitation. Le seul enseignement de fond — et il est réel — est que **sa santé runtime n'est pas entièrement garantie par le dépôt** : un écart non versionné existe entre la configuration et le registre, que le checker contractuel ne sait pas voir, et qu'une reprise à blanc révélerait. Le reste relève de la documentation et du nettoyage. Pour un système dont la doctrine est « le dépôt est la vérité », fermer l'écart de reproductibilité (AUDI-11) et donner au checker les moyens de le détecter (AUDI-05) sont les deux actions à plus forte valeur.
