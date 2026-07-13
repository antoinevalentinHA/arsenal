# Plan d'action — clôture de la validation terrain (C13, C15, C16, C18)

- **Type :** plan d'action transverse — **non normatif**, organisationnel. Ne modifie aucun contrat, aucune logique métier, aucun registre, aucun changelog. La seule action *runtime* prévue est une **instrumentation Recorder** (historisation d'entités existantes), sans aucune modification de décision ou d'action.
- **Statut :** proposé, à exécuter par étapes ; aucune clôture prononcée par ce document.
- **Objet :** recueillir les preuves manquantes identifiées par l'investigation historique afin de clôturer, à terme, C13, C15, C16 et C18.
- **Sources faisant foi :** [`investigation_historique_cloture_terrain_c16_c15_c13.md`](../../01_rapports/transverses/investigation_historique_cloture_terrain_c16_c15_c13.md) · [`protocole_validation_c18_sante_pont.md`](../../04_chantiers/arrosage/protocole_validation_c18_sante_pont.md) · [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) · contrats/runtime C13/C15/C16 · `recorder.yaml` · [`audit_recorder_instrumentation_temporaire.md`](../../01_rapports/architecture/audit_recorder_instrumentation_temporaire.md).

---

## 1. Principe

Deux chantiers se closent par **observation directe** (aucune instrumentation) ; deux dépendent d'une **occurrence naturelle** et requièrent une **instrumentation Recorder temporaire minimale** (« microscope » au sens de l'audit recorder). Toute instrumentation ici est **de l'historisation pure** : entités déjà existantes ajoutées à la liste blanche `recorder.yaml`, en Population B justifiée, **sans toucher à aucune automation, sensor, script ou décision**.

## 2. Matrice finale

| Chantier | Preuve manquante | Voie | Instrumentation Recorder | Entités exactes | Condition de clôture (preuve acquise) | Réévaluation / retrait |
|---|---|---|---|---|---|---|
| **C18** | T1 : `pont_sante=ok` malgré RSSI ≤ -75 ; T3/T4 : mapping degrade/indisponible | **T1 en lecture live, T5 dans la même passe** · T3/T4 = occurrence naturelle post-12/07 (**non bloquants**) | **NON** (déjà historisées) | *lecture seule* : `sensor.rain_bird_pont_sante`, `binary_sensor.rain_bird_pont_donnees_disponibles`, `binary_sensor.rain_bird_pont_donnees_fraiches`, `sensor.rain_bird_bat_bt_2_e9a3_bridge_wifi_rssi`, `sensor.rain_bird_bat_bt_2_e9a3_ble_rssi` | **Critère du protocole (repris sans élargissement)** : **T1 réussi ⇒ réserve principale levée ⇒ clôture définitive possible** ; T5 confirme la non-régression ; **T3/T4 non bloquants** ; trace §6 du protocole remplie. *« Aucune preuve terrain affirmée avant trace remplie. »* | — (aucune instrumentation) |
| **C15** | reboot pendant état actif → **recréation** de la persistante | **Live contrôlé** (reboot pendant un **vrai cycle** électroménager) | **NON** (test live direct ; `call_service` create déjà captés) | *observation* : `input_boolean.lave_vaisselle_cycle` **ou** `input_boolean.buanderie_cycle` (actif) ; notif `lave_vaisselle_cycle`/`buanderie_cycle` ; auto `10080000000006`/`10080000000007` ; jalon `systeme_stable` | Cycle réel actif → redémarrage HA → après `systeme_stable→on`, la notification persistante **réapparaît** (observée en UI), flag encore actif | — |
| **C16** | ouverture **et** fermeture **nominales** (dont cas Netatmo absent) | **Occurrence naturelle** (prochaine pluie) + instrumentation | **OUI — 1 entité** | **ajout** : `input_boolean.pluie_en_cours`. *Déjà historisées* : `binary_sensor.pluie_evidence_active`, `binary_sensor.zigbee_pluie_water_leak`, `sensor.pluviometre_precipitation` | 1 épisode réel : évidence→`on` puis `pluie_en_cours`→`on` en ≤ ~1 s (ouverture) ; évidence→`off` puis `pluie_en_cours`→`off` en quelques min, **âge < 3 h ou Netatmo présent** (fermeture **nominale**, pas backstop). Bonus décisif : épisode Netatmo `unavailable` porté par SNZB, fermé nominalement | **Réévaluation propriétaire obligatoire à T0 + 60 j** |
| **C13** | échec d'exécution **persistant réel** → notif créée puis retirée | **Occurrence naturelle** (rare) ; test provoqué = décision propriétaire | **OUI — 2 entités** | **ajout** : `input_boolean.clim_execution_echec`, `counter.clim_execution_retry_count`. *Déjà historisé* : `sensor.clim_target_mode`. Notif `clim_execution_echec`, auto `10030000000121` | Une fenêtre : `clim_execution_echec=on` **et** `retry_count > 2` avec `persistent_notification.create(clim_execution_echec)` ; puis `echec→off` avec `dismiss` | **Réévaluation propriétaire obligatoire à T0 + 120 j** |

> `input_boolean.systeme_stable` **n'est pas ajouté** : la réconciliation au démarrage est un chemin secondaire, hors critère de clôture (ouverture/fermeture nominales pour C16 ; création/retrait pour C13). Périmètre minimal strict.

## 3. Preuves attendues (détail)

- **C18 — T1 en lecture live, avec T5 exécuté dans la même passe de validation.** T1 : lire l'état — `sensor.rain_bird_pont_sante` = `ok`, `…_donnees_disponibles` = `on`, `…_donnees_fraiches` = `on`, RSSI (`…_bridge_wifi_rssi` / `…_ble_rssi`) noté (attendu ~ -76, ≤ -75), attributs RSSI de `pont_sante` toujours exposés. T5 : `binary_sensor.arrosage_rain_bird_preconditions_runtime`, `binary_sensor.arrosage_intention` (+ `motif`/`categorie`), `sensor.arrosage_dernier_effectif` inchangés. **Conformément au protocole, T1 réussi lève la réserve principale et permet la clôture ; T5 confirme la non-régression. T3/T4 restent opportunistes et non bloquants** — ils se rempliront d'eux-mêmes dans un futur backup (entités déjà historisées).
- **C15 — live contrôlé** : pendant un cycle lave-vaisselle **ou** buanderie réel (`input_boolean.*_cycle` = `on`), redémarrer HA ; vérifier que la notification persistante (`lave_vaisselle_cycle` / `buanderie_cycle`) **réapparaît** après stabilisation. Aucune panne artificielle (le cycle est un usage réel, pas une injection).
- **C16 — instrumenté + naturel** : après ajout de `pluie_en_cours` au Recorder, au prochain épisode de pluie réel, extraire le backup et vérifier la corrélation évidence ↔ `pluie_en_cours` (ouverture ≤ ~1 s ; fermeture nominale en quelques min sous seuil backstop 3 h / Netatmo présent).
- **C13 — instrumenté + naturel** : après ajout de `clim_execution_echec` + `retry_count`, à la prochaine occurrence réelle d'échec persistant, reconstruire la séquence (latch + budget épuisé + création ; puis disparition + retrait) depuis ces deux entités et les `call_service` déjà captés.

## 4. Instrumentation Recorder temporaire — périmètre minimal

Trois entités au total, ajoutées à `recorder.yaml` en **liste blanche stricte** (jamais d'inclusion de domaine), en **Population B** (justification Rôle/Utilité/Logbook/Cardinalité/Fréquence ; toutes binaires ou compteur borné, largement sous le seuil opposable de 5 changements/h) :

| Entité | Chantier | Nature | Justification (résumé) | Impact Recorder |
|---|---|---|---|---|
| `input_boolean.pluie_en_cours` | C16 | binaire | prouver l'ouverture/fermeture nominale d'épisode aux côtés de l'évidence déjà historisée | négligeable (quelques changements/jour en pluie, nul sinon) |
| `input_boolean.clim_execution_echec` | C13 | binaire | latch d'échec — condition de création de la notification | négligeable (change uniquement en échec, rare) |
| `counter.clim_execution_retry_count` | C13 | compteur borné | budget de reprise (> 2 = épuisé) — 2ᵉ condition de création | négligeable (incréments rares, groupés à l'échec) |

**Aucune** autre entité. **Aucune** modification métier : ces entités existent déjà ; seule leur *historisation* est ajoutée.

## 5. Gouvernance temporelle (doctrine corrigée)

Chaque bloc instrumenté portera le marqueur `⏳ GOUVERNANCE TEMPORELLE — instrumentation de chantier (microscope)`, dont la **date inscrite est une date de RÉÉVALUATION, jamais une date de suppression impérative**. Doctrine :

1. **Retrait dès acquisition de la preuve et clôture du chantier** — l'instrumentation ne subsiste pas au-delà de son objet.
2. **Maintien tant que le chantier reste actif ET que l'instrumentation reste nécessaire.**
3. **Réévaluation propriétaire obligatoire** à l'échéance : **T0 + 60 j pour C16**, **T0 + 120 j pour C13** (T0 = date d'ajout effectif à `recorder.yaml`).
4. **À l'échéance, décision explicite et tracée**, au choix : *maintien motivé* · *retrait* · *modification de la stratégie de preuve* · *autorisation d'un test provoqué* (C13).
5. **Aucun maintien silencieux au-delà de l'échéance.** Passé la date de réévaluation sans décision datée, l'instrumentation est en défaut de gouvernance (à trancher, pas à supprimer automatiquement).

Format de marqueur prévu (à insérer dans `recorder.yaml` au lot suivant) :

```yaml
    # ⏳ GOUVERNANCE TEMPORELLE — instrumentation de chantier (microscope)
    # Chantier   : <Cxx — objet>
    # Ajouté     : <PR #…, date = T0>
    # Réévaluer  : <T0 + 60 j (C16) / T0 + 120 j (C13)> — RÉÉVALUATION propriétaire
    #              obligatoire (PAS une suppression automatique) : maintien motivé,
    #              retrait, modification de la stratégie de preuve, ou autorisation
    #              d'un test provoqué. Aucun maintien silencieux au-delà.
    # Retrait    : dès preuve acquise et chantier clôturé ; maintien tant que le
    #              chantier est actif ET l'instrumentation nécessaire.
```

**Traçabilité du retrait (mécanisme documentaire)** : (a) le marqueur daté ci-dessus dans `recorder.yaml` ; (b) le présent plan, qui liste chaque instrumentation, sa date T0, sa date de réévaluation et sa condition de retrait, et sert de checklist de campagne.

## 6. Ordre d'exécution recommandé

1. **C18 — T1 en lecture live, avec T5 exécuté dans la même passe de validation** — immédiat, coût nul, zéro instrumentation. Remplir la trace §6 du protocole. Conformément au protocole, T1 réussi lève la réserve principale et permet la clôture ; T5 confirme la non-régression ; T3/T4 restent opportunistes et non bloquants.
2. **C15 — test live contrôlé** — immédiat, zéro instrumentation. Reboot pendant un vrai cycle électroménager, vérifier la réapparition de la persistante. Clôture C15.
3. **C16 — instrumenter** (`pluie_en_cours`) puis attendre la prochaine pluie réelle (jours–semaines).
4. **C13 — instrumenter** (`clim_execution_echec` + `retry_count`) puis attendre un échec persistant réel (rare) ou décision propriétaire de test provoqué.

Rationnel : les deux clôtures sans instrumentation ni attente d'abord ; l'instrumentation minimale ensuite, par fréquence d'occurrence décroissante (pluie > panne clim).

## 7. Ce que ce plan ne fait pas

- **Aucune clôture** de chantier (les statuts du registre restent inchangés jusqu'à preuve acquise et présentée).
- **Aucune modification** de contrat, d'automation, de sensor, de script, de décision ou d'action — instrumentation Recorder uniquement.
- **Aucune modification** de `REGISTRE_CHANTIERS.md` ni de changelog par ce plan.
- **Aucune panne artificielle**, aucun test provoqué sans décision propriétaire explicite (C13).
- Le diff de `recorder.yaml` (blocs C16/C13) est un **lot séparé**, présenté et validé après ce plan.

> **Amélioration séparée (hors de ce lot).** Un futur garde-fou CI pourrait détecter un bloc `⏳ GOUVERNANCE TEMPORELLE` dont la **date de réévaluation est dépassée sans décision datée de prolongation** — et **non** exiger la suppression automatique du microscope. À instruire indépendamment ; non inclus ici.
