# Cadrage contractuel — Présence confort thermique stabilisée

| Champ | Valeur |
|---|---|
| **Type** | Cadrage contractuel (préalable, sans implémentation) |
| **Domaine** | Climatisation / Présence — interface de stabilisation COOL |
| **Statut** | **Proposé — non opposable, non implémenté** |
| **Version** | 0.1 (cadrage) |
| **Date** | 2026-06-15 |
| **Dépôt** | `antoinevalentinHA/arsenal` @ HEAD `84066894` |
| **Signal cadré** | `binary_sensor.presence_confort_thermique_stabilisee` |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun contrat existant modifié. Ne ratifie pas la valeur de tenue `T`. |

> **Objet :** cadrer un **signal d'interface de présence**, stabilisé contre les faux-absents courts, destiné aux **seules décisions COOL** de la climatisation démontrées vulnérables. Document destiné à devenir un contrat (ou une section du contrat présence) **après ratification** ; il n'est pas opposable en l'état.

---

## 1. Rôle du signal

Fournir aux seules décisions COOL clim une image de présence **immunisée contre les faux-absents courts** de `binary_sensor.presence_famille_unifiee`, sans modifier la présence ni la logique de décision clim. C'est un **confinement** à l'interface confort, au plus près des consommateurs vulnérables (incident révélateur + jumeau du 15/06, classe « glitch court »).

## 2. Source unique

- Source **unique et exclusive** : `binary_sensor.presence_famille_unifiee`, en **lecture seule**.
- Aucune autre entrée (ni `person.*`, GPS/Wi-Fi, `presence_famille`, `presence_famille_securite`, alarme).

## 3. Sémantique

Hystérésis **asymétrique** :
- **Montée** : `on` sans latence ajoutée dès que `unifiee` est `on` (confort rétabli immédiatement au retour).
- **Descente** : `off` seulement après une absence **continue** de `unifiee` pendant une tenue `T`.
- **Glitch court** : toute séquence `on → off → on` dont la phase `off` dure **moins que `T`** ne produit aucune bascule `off`.

> `T` **non fixée ici** (arbitrage différé, §15 ; cf. note de calibration). Le contrat fixe la forme, pas le réglage.

## 4. Invariants

- **I1 — Source exclusive** : dérive uniquement de `unifiee`.
- **I2 — Sur-ensemble à la montée** : `unifiee = on` ⟹ signal = `on`.
- **I3 — Descente justifiée** : signal = `off` ⟹ `unifiee` resté `off` en continu ≥ `T`.
- **I4 — Jamais en avance sur l'absence** : retard à la descente uniquement.
- **I5 — Lecture seule** : n'altère ni `unifiee`, ni `presence_famille_securite`, ni l'alarme, ni aucun maillon clim.
- **I6 — Confort sans latence au retour** (corollaire d'I2).
- **I7 — Neutralité sécurité** : aucune sémantique de sécurité ; jamais consommé par sécurité/alarme.
- **I8 — Dérivabilité** : reconstructible depuis l'historique de `unifiee` et `T`.
- **I9 — Confinement** : seuls les consommateurs du §6 le lisent.

## 5. Non-buts

- Pas un signal de présence de référence ni de sécurité ; ne remplace pas `unifiee`.
- Pas un remodelage de la présence ; pas un correctif de la cause racine (GPS/Wi-Fi).
- Pas une modification de `besoin`/`admissibilite`/`target_mode`.
- Pas un élargissement au chauffage, DRY, HEAT, silence, absence prolongée, vacances, jardin, diagnostics, UI, recorder.
- Pas un choix de `T`.

## 6. Consommateurs autorisés (périmètre minimal validé)

Cinq fichiers COOL rebranchent leur **point de lecture de présence** (échange de référence, sans changement de logique) :

1. `12_template_sensors/climatisation/seuils_on_off/cool/on.yaml`
2. `12_template_sensors/climatisation/seuils_on_off/cool/off.yaml`
3. `12_template_sensors/climatisation/decision/consigne.yaml`
4. `11_automations/climatisation/cool/maj_consignes/absence.yaml`
5. `11_automations/climatisation/cool/maj_consignes/presence.yaml`

> (1)(2) : rebrancher **et** la liste `entity_id:` (déclencheur du template) **et** la lecture d'état. (4)(5) : bouger **ensemble** (symétrie présence/absence).

## 7. Consommateurs explicitement interdits

Tout ce qui n'est pas au §6, en particulier : fichiers **sécurité/alarme** ; `presence_famille_securite` ; définition de `presence_famille_unifiee` ; chaîne **COOL interne** (`besoin_clim_cool*`, `*admissible*`, `clim_target_mode`, `autorisation/cool.yaml`) ; `autorisation/dry.yaml`, `autorisation/heat.yaml`, `blocages/absence_longue.yaml`, `cool/start_timer_absence.yaml`, `silence/autorisation.yaml` ; **chauffage** ; éclairage jardin, modes vacances, diagnostics, UI/Lovelace, `recorder.yaml`, fixtures/registres CI.

## 8. Interaction avec la climatisation

Seul point d'entrée : les cinq lectures de présence du §6. La chaîne `besoin`/`admissibilite`/`target_mode` est inchangée et reçoit seulement des seuils/consigne plus stables. **Cohabitation assumée** : `autorisation/cool.yaml` continue de voir la présence via `absence_prolongee` (timer-gardée, hors périmètre) ; sur les drops courts les deux notions ne se contredisent pas (timer), sur les absences réelles elles convergent après `T`/timer (point à valider, §13 R-D).

## 9. Interaction avec le chauffage

**Aucune.** Le chauffage reste intégralement sur `presence_famille_unifiee`. Le signal ne doit apparaître dans aucun fichier chauffage (décision séparée, §15).

## 10. Interaction avec la sécurité / alarme

**Aucune, dans les deux sens** (I7). La sécurité influe sur `unifiee` comme aujourd'hui ; le signal hérite de cette influence sans la modifier ni la réinjecter. Timelines `presence_famille_securite`, alarme, gating High Accuracy : inchangées (V5).

## 11. Interaction avec `binary_sensor.presence_famille_unifiee`

`unifiee` est la source unique (§2) et reste **strictement inchangé** (définition, délais, sources, et tous ses consommateurs actuels). Le nouveau signal est strictement en aval : `on` suit `unifiee` (I2), `off` retarde de `T` (I3). On ajoute une dérivation parallèle ; on ne repointe pas les autres consommateurs de `unifiee`.

## 12. Interaction avec `binary_sensor.presence_famille_securite`

**Aucune interaction directe.** Le signal ne lit ni n'altère `securite`, qui demeure la vérité de sécurité brute consommée par l'alarme. Résidu connu **non aggravé** : `unifiee` mélange déjà `securite` en amont (couplage confort↔sécurité préexistant) ; ce cadrage n'y touche pas (§15).

## 13. Risques de régression

- **R-A — Latence de descente** : absence réelle basculée en absence avec ≤ `T` de retard → sur-refroidissement borné (∝ `T`).
- **R-B — Rebranchement incomplet** (parmi les 5) → protection partielle. Mitigation : checker CI (§14 V4).
- **R-C — Asymétrie présence/absence** si (4)(5) ne bougent pas ensemble.
- **R-D — Double notion de présence dans COOL** (stabilisée vs `absence_prolongee` brute timer-gardée) — à valider (§8).
- **R-E — Intégrité `target_mode`** : entrée lissée → valider l'absence de nouveau blocage (rappel D8 du 30/05) et le franchissement ON/OFF.
- **R-F — Couplage résiduel confort↔sécurité** : hérité, non aggravé, non résolu.
- **R-G — Tenue trop longue** : court déplacement réel masqué pendant `T` (borné).

## 14. Critères de validation

- **V1 — Fonctionnel** : `unifiee off < T` ⟹ aucune variation de `seuil_allumage/extinction_clim_applique` ni `consigne_clim_appliquee`, aucun `target_mode → off`. Mesure : ré-exécution de l'observation météo post-déploiement ⟹ épisodes en régime cool < `T` → **0 impact** (vs 2/2 référence).
- **V2 — Préservation** : `unifiee off > T` bascule toujours en absence sous `T + ε`.
- **V3 — Conformité sémantique** : I2 et I3 vérifiables sur historique.
- **V4 — Confinement** : seuls les 5 fichiers du §6 référencent le signal ; aucun fichier du §7 (checker CI).
- **V5 — Non-interférence** : `securite`, alarme, High Accuracy, définition `unifiee`, chaîne `besoin/admissibilite/target_mode` inchangés (contrôle de portée du diff).
- **V6 — Intégrité COOL** : aucun nouveau blocage ; COOL atteint ON et OFF sous l'entrée lissée.

## 15. Points restant à arbitrer

Valeur de `T` (cf. note de calibration) ; comportement de repli sur `unavailable`/`unknown` ; instantanéité de montée ; extension éventuelle DRY/HEAT/`absence_longue` ; adoption chauffage ; découplage confort↔sécurité ; historisation recorder du nouveau signal ; ratification et rattachement au contrat `presence.md`.

---

## Liens

- Hub présence : [`navigation/domaines/presence.md`](../../../navigation/domaines/presence.md)
- Hub climatisation : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
- Index audits : [`audits/index.md`](../../index.md)
- Contrat présence (référence, **non modifié**) : [`contrats/presence.md`](../../../contrats/presence.md)
- Note de calibration `T` : [`note_calibration_tenue_T_presence_confort_thermique.md`](note_calibration_tenue_T_presence_confort_thermique.md)
- Inventaire de périmètre : [`inventaire_consommateurs_presence_famille_unifiee.md`](inventaire_consommateurs_presence_famille_unifiee.md)

**Rattachement amont (à publier — hors dépôt à ce stade, consolidation présence distincte) :** cadrage de dette de modélisation de la présence ; cartographie des familles de solutions ; dispositif d'observation des pertes de présence. *(Liens volontairement non posés tant que ces documents ne sont pas dans le dépôt.)*

> **Portée.** Cadrage d'un signal d'interface confinant l'effet des faux-absents courts sur les seules décisions COOL clim. Aucune solution générale, aucun YAML, aucun réglage. Clim interne, chauffage, alarme, `securite` et `unifiee` intacts par construction.
