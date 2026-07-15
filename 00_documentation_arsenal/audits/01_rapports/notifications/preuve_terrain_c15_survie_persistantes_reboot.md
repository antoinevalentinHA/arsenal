# Preuve terrain — C15, survie des notifications persistantes au reboot

- **Type :** rapport de preuve terrain (historique Recorder), **lecture seule** — aucun runtime, contrat ni checker modifié par cette analyse. Seuls le registre et les plans d'action sont mis à jour (co-commit de clôture).
- **Statut :** **preuve acquise — C15 clôturable.** Réserve du 2026-07-13 (« absence de la séquence décisive ») **levée**.
- **Question posée :** le correctif C15 (NOTIF-03) recrée-t-il effectivement une notification persistante d'état après un redémarrage survenu **pendant** que l'état est actif ?
- **Réponse :** **oui, observé.** Reboot volontaire pendant un cycle lave-vaisselle réel le 2026-07-15 → la persistante `lave_vaisselle_cycle` est recréée **47 s** après le démarrage, sans re-détection intermédiaire.
- **Données :** une sauvegarde Home Assistant non chiffrée (2026-07-15 20:22 UTC, HA 2026.7.2, `exclude_database: false`), base Recorder — **conservée hors dépôt avec les scripts, empreintes SHA-256 et le détail technique** (dépôt privé d'audit runtime, `analyses/cloture_c15_20260715/`). Le présent rapport n'en restitue que la méthode et les verdicts.
- **Voie suivie :** « live contrôlé », exactement celle prévue par [`plan_action_cloture_validation_terrain_c13_c15_c16_c18.md`](../../03_plans_action/transverses/plan_action_cloture_validation_terrain_c13_c15_c16_c18.md) §2/§3 et §6 (ordre d'exécution n° 2) — **aucune instrumentation Recorder**, **aucune panne artificielle** (le cycle est un usage réel, pas une injection).

---

## 1. Contexte — pourquoi cette preuve manquait

L'investigation du 2026-07-13 ([`investigation_historique_cloture_terrain_c16_c15_c13.md`](../transverses/investigation_historique_cloture_terrain_c16_c15_c13.md) §3) concluait à une **absence de preuve suffisante** — au sens strict de sa propre nomenclature §1, c'est-à-dire *preuve absente*, **jamais** *correctif invalidé* :

> « Le déclencheur de re-projection au démarrage **s'exécute bel et bien** […]. Mais **aucun redémarrage n'a coïncidé avec un état actif après le 2026-07-09** […]. Les cas « reboot pendant état actif » présents dans l'historique sont **tous antérieurs** au correctif et illustrent l'**ancien** comportement (notification perdue) : contexte, jamais preuve. »

Il manquait donc une seule chose : **un reboot tombant pendant un état actif, après le correctif**. Elle a été produite délibérément.

## 2. Méthode

- **Contrainte structurelle rappelée** : le Recorder fonctionne en liste blanche et les `input_boolean` d'état (dont le flag de cycle) **ne sont pas historisés**. La preuve repose donc **exclusivement sur les traces `call_service`** (table `events`), captées indépendamment de l'allowlist. C'est précisément ce que le plan §2 anticipait en inscrivant « instrumentation : **NON** (test live direct ; `call_service` create déjà captés) » — aucune entité n'a eu à être ajoutée à `recorder.yaml` pour clore C15.
- **Fenêtre analysée** : ~30 j (2026-06-15 → 2026-07-15), soit de part et d'autre du déploiement du correctif (**2026-07-09**).
- **Reconstruction** : corrélation des marqueurs de redémarrage avec les actes `input_boolean` (marquage du cycle) et `persistent_notification` (projection), pour chaque redémarrage survenu **flag actif**.

## 3. Séquence décisive observée (2026-07-15)

| Horodatage (local) | Acte | Lecture |
|---|---|---|
| 21:09:29 | `input_boolean.turn_on` (flag de cycle) | cycle démarre — détection nominale (30 W / 3 min) |
| 21:09:29 | `persistent_notification.create` | projection sur transition |
| **22:01:30** | **redémarrage Home Assistant** | **reboot volontaire, cycle actif** |
| **22:02:17** | **`persistent_notification.create`** | **re-projection au boot — +47 s** |

Critères de clôture du plan §2, point par point :

| Critère exigé | Observé | Statut |
|---|---|---|
| Cycle réel actif au moment du reboot | `turn_on` à 21:09:29, **aucun** retrait de flag avant le reboot | ✅ |
| Redémarrage HA | 22:01:30 | ✅ |
| La persistante **réapparaît** | `create` à 22:02:17 | ✅ |
| …**après `systeme_stable → on`** | +47 s ≈ le `delay: "00:00:45"` de [`stabilisation_post_demarrage.yaml`](../../../../11_automations/system/stabilisation_post_demarrage.yaml) + surcoût d'exécution | ✅ |
| Flag encore actif | aucun retrait jusqu'à la fin de la fenêtre (22:22) — cycle toujours en cours à la sauvegarde | ✅ |
| Usage réel, aucune panne artificielle | cycle lave-vaisselle nominal | ✅ |

## 4. Exclusion du confondant — re-détection vs survie

Deux histoires produisent la **même** notification à l'écran, et l'observation visuelle seule ne les sépare pas :

- **(a) survie au reboot** — le flag est restauré à `on`, la projection dédiée recrée la notification ;
- **(b) re-détection** — le flag n'est **pas** restauré, [`debut.yaml`](../../../../11_automations/electromenager/lave_vaisselle/debut.yaml) redétecte le cycle (seuil **30 W maintenu 3 min**) et pose le flag, dont la transition déclenche la projection.

Le cas (b) **exige impérativement** un nouvel acte de marquage du flag après le reboot. Or **aucun acte `input_boolean.turn_on` n'existe entre le redémarrage (22:01:30) et la re-création (22:02:17)** — le dernier remonte à 21:09:29, ~52 min avant le reboot.

> ⇒ **(b) est exclu par les données seules ; (a) est établi.** Le flag a été **restauré** par Home Assistant, et la notification recréée par la **seule** projection d'état.

Corroboration indépendante par le délai : **+47 s est incompatible avec (b)** (qui exigerait ≥ 3 min de surconsommation après le boot) et **cohérent avec le jalon `systeme_stable`** (45 s). C'est donc le trigger `systeme_stable → on` qui a porté la re-projection — soit exactement l'**idiome canonique** réclamé par NOTIF-03, et exactement la **course** qu'il neutralise (restore des entités ↔ chargement de l'automation).

## 5. Contrefactuel — avant/après dans la même fenêtre

La fenêtre contient **8 redémarrages survenus flag actif**. Leur répartition tranche seule :

| Reboots flag actif | Fenêtre | Acte post-reboot | Lecture |
|---|---|---|---|
| **7** (2026-06-27) | **pré-correctif** | **aucun acte** | notification **perdue** au reboot = le défaut NOTIF-03 d'origine |
| **1** (2026-07-15) | **post-correctif** | **`create` à +47 s** | notification **recréée** = correctif opérant |

Même base, même entité, même condition de départ (cycle actif) ; **seule la présence du correctif diffère**. La preuve n'est donc pas une observation isolée mais un **avant/après contrôlé** : les 7 occurrences pré-correctif matérialisent le défaut, l'unique occurrence post-correctif matérialise sa correction. Ce sont exactement les cas que le 13/07 devait écarter comme « contexte, jamais preuve » — ils acquièrent ici leur valeur de **témoin négatif**.

## 6. Portée — ce que cette preuve établit et ce qu'elle n'établit pas

- **Établit** : l'idiome canonique (trigger d'état **+** `systeme_stable → on` ; `choose` piloté par le seul état courant ; `mode: restart`) **re-projette effectivement une persistante au boot**, sur le cas `lave_vaisselle_cycle`. C'est le critère du plan §2, qui admet explicitement `lave_vaisselle_cycle` **ou** `buanderie_cycle` comme véhicule de preuve — l'idiome étant **partagé** par toutes les projections corrigées par C15.
- **N'établit pas**, et n'a pas à établir : une vérification terrain instance par instance des autres projections (présence, panne secteur, babysitting, pré-confort, alarme, VMC, voiture, bluetti). Elles restent couvertes par la **validation statique** (`check_notifications_contracts` T1–T6, vert) et par l'identité structurelle de l'idiome. Le protocole n'exigeait pas davantage : **élargir le critère a posteriori serait un déplacement de la cible**, non une exigence de rigueur.
- **Inchangé, hors périmètre** : `panne_internet` (NOTIF-05) demeure une **reprise différée assumée** (décision L4, aucun changement runtime) ; le **durcissement CI** du checker (angles morts §4 du plan d'action notifications) demeure un lot ultérieur **optionnel et non bloquant**.

## 7. Verdict

**Les critères de clôture C15 sont satisfaits ; le confondant est exclu par les données ; le contrefactuel pré-correctif est présent dans la même fenêtre.** La réserve du 2026-07-13 est **levée**. **C15 est clôturé** (registre ⑤).

---

## 8. Constat connexe découvert — hors périmètre de cette preuve

Le contrat normatif [`electromenager.md`](../../../contrats/electromenager.md) est resté en **v1.0 (2026-06-07)** et décrit encore l'architecture **pré-C15** : il attribue le `create` de la persistante à `debut.yaml` et le `dismiss` à `fin.yaml`, qualifie la notification d'événement de **début** (et non de projection d'**état**), et **ne mentionne pas** les projections dédiées `10080000000006` / `10080000000007` dans son inventaire d'automations.

C'est une **dérive contrat ↔ runtime en sens inverse de l'habituel** : ici le runtime est correct et le **contrat est en retard**. Le contrat pose pourtant lui-même « le runtime fait foi ; tout écart d'implémentation est une non-conformité, pas une interprétation ».

> **Ce constat ne conditionne pas la clôture de C15**, qui porte sur le **comportement observé** et dont le critère est intégralement satisfait. Il est consigné ici pour ne pas être perdu et relève d'un **lot documentaire séparé** (réalignement du contrat électroménager sur l'architecture de projection), à ouvrir sur décision propriétaire.

---

*Rapport de preuve — restitue méthode et verdicts. Détail technique, scripts et empreintes : hors dépôt (`arsenal-runtime/analyses/cloture_c15_20260715/`). Cockpit : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C15).*
