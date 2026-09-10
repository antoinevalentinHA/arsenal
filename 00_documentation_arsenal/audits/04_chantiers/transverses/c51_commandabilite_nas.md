# Chantier TRANSVERSE (C51) — Commandabilité Arsenal → NAS

| Champ | Valeur |
|---|---|
| **Chantier** | Permettre à Home Assistant/Arsenal de demander au NAS, via MQTT, l'exécution des deux opérations métier existantes `AUDIT` et `RELEASE_DIFF`, sans fusionner leurs chaînes, sans big bang sur les tâches DSM actuelles, et sans jamais confondre la transaction de commande et le résultat métier qu'elle produit. |
| **Domaine** | Transverse — dépôts `arsenal` et `arsenal-ha-backup-timeline` ; domaines Home Assistant `arsenal_self` (audit) et `arsenal_nas` (release_diff). |
| **Statut** | **Ouvert (2026-09-08) — volet NAS livré, mergé et validé terrain bout-en-bout (2026-09-09).** Verrou RELEASE_DIFF (Lot 2), durcissement AUDIT + `run_id` corrélable (Lot 3), moteur d'admission transactionnelle (Lot 4 — `admission/bin/admission_core.py`) et listener MQTT NAS (identité dédiée `nas_admission`) livrés, mergés et **validés terrain** pour `AUDIT` et `RELEASE_DIFF`, y compris en concurrence inter-opérations — voir §12.2 « Preuves terrain NAS ». Contrat `nas_transactionnel.md` v1.2.1, vérifié conforme à l'état livré, **non modifié** par ce lot. **Lot 5 (backend Arsenal, pilote `AUDIT` seul) livré, déployé et validé terrain bout-en-bout** (2026-09-09, Home Assistant 2026.9.1) : génération des enveloppes `request_id`/`ts`/`expires_at`/`source`, publication MQTT, corrélation/diagnostic du résultat transactionnel — voir §12.3/§12.4. Preuve du lot fournie : `request_id`/`run_id` corrélés HA↔NAS et NAS↔HA, terminaison transactionnelle `completed`, `wrapper_rc=0`, durée ≈ 33 s, ancrage nettoyé, une seule exécution `AUDIT`, aucune reconnexion MQTT — résultat métier `ok` (0 anomalie) observé **séparément** sur `sensor.arsenal_self_audit_statut`, jamais déduit du verdict transactionnel. Listener MQTT NAS lancé pour cette preuve **manuellement au premier plan** puis arrêté proprement — **hébergement/supervision permanent du listener livré et validé terrain le même jour** (2026-09-09), voir la ligne « Mise à jour » suivante et §12.5. **Lot 6 (backend Arsenal, extension `RELEASE_DIFF`) — livré, déployé et validé terrain (2026-09-09).** Prolonge strictement le patron du Lot 5 : helper transactionnel dédié `input_text.nas_admission_req_release_diff` (jamais partagé avec le helper AUDIT), `script.nas_admission_demander_release_diff` (émission `operation: "RELEASE_DIFF"` fixe), diagnostic dédié `sensor.nas_admission_release_diff_etat_transaction` — voir §12.6/§12.7. Réutilise sans modification le sensor MQTT brut et la couche de corrélation communs (§13.1). AUDIT (Lot 5) **inchangé** par ce lot (zéro octet modifié dans ses fichiers runtime). Preuve terrain fournie (2026-09-09) : `request_id`/`run_id` corrélés HA↔NAS et NAS↔HA, admission ≈ 1 s après `ts`, terminaison transactionnelle `completed`, `wrapper_rc=0`, durée totale `ts`→terminal ≈ 3 min 23 s, ancrage nettoyé, une seule exécution, aucune reconnexion MQTT — résultat métier `ok` observé **séparément** sur `sensor.arsenal_nas_release_diff_statut`, jamais déduit du verdict transactionnel — voir §12.7. **Lot 7 (UI Lovelace) — livré en code, non déployé, non testé terrain (2026-09-09).** Nouvelle section « Commandabilité NAS (C51) » dans `18_lovelace/dashboards/systeme/nas.yaml`, dérivée exclusivement de la documentation UI existante (`ui/pattern_dashboard.md`, `ui/socle_ui/02_action.md`, `ui/socle_ui/07_status.md`, `ui/couleurs/`) et des patrons déjà en usage (`carte_action_arrosage_script`, `arsenal_self_audit_status_card`) : deux boutons de demande confirmés (`script.nas_admission_demander_audit`/`_release_diff`, aucune publication MQTT directe), deux cartes de diagnostic transactionnel (`sensor.nas_admission_audit_etat_transaction`/`_release_diff_etat_transaction`, jamais colorées en vert sur `completed`), et deux cartes de résultat métier strictement séparées (réutilisation de `arsenal_self_audit_status_card` pour AUDIT, nouvelle `arsenal_nas_release_diff_status_card` pour RELEASE_DIFF — sans binary_sensor de fraîcheur/erreur inventé, `arsenal_nas.md` §5.3 n'en déclarant aucun). Aucun backend Lots 5/6 modifié, aucune automation créée, aucun ID d'automatisation inventé (§14) — voir §12.8. Chantier **non clos** : preuve d'usage réel Lovelace absente, preuves de replay/`BUSY`/crash-reprise et dette ACL C52 restent ouvertes — voir §12.1/§12.5/§12.6/§12.7/§12.8. **Correction fonctionnelle du Lot 7, UI Lovelace (2026-09-10) — arbitrage Direction.** L'emplacement retenu au Lot 7 (`18_lovelace/dashboards/systeme/nas.yaml`) était **fonctionnellement faux** : `AUDIT`/`RELEASE_DIFF` sont un service rendu à Arsenal, le NAS n'étant que l'exécutant technique externe de la demande (§4 « Matrice des autorités ») ; la justification initiale (« pas de hub documentaire ⇒ dashboard NAS ») est **rejetée** — l'absence de hub de domaine (`navigation/carte_domaines.md` §3/§6) ne désigne aucun domaine d'accueil par défaut. L'UI C51 est repositionnée dans `18_lovelace/dashboards/systeme/principal.yaml` (dashboard Système), en cohérence avec le diagnostic `arsenal_self_audit_status_card` déjà présent (non déplacé, non réécrit). Les trois templates satellites du Lot 7 restent valides et sont réutilisés ; les deux templates NAS-spécifiques sont déplacés de `40_dashboards/nas/` vers `40_dashboards/system/`. Aucun backend (Lots 5/6) modifié — PR #819 non revert. Voir §12.9. |
| **Priorité** | P2 — aucun risque fonctionnel actuel ; enjeu d'architecture et de gouvernance documentaire avant toute commandabilité. |
| **Ouvert le** | 2026-09-08. |
| **Registre** | Chantier **C51** — ① Actifs, cf. [`../../REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md). **Ce document est la source faisant foi pointée par la ligne.** |
| **Mesure amont** | Audit terrain NAS en lecture seule (2026-09-08, DSM + SSH, aucune écriture) ; synthèse architecturale confrontant Git et terrain (même session) ; HEAD `arsenal` `a317b5b82c91bcbb79b02d787ed2e0ca2386398e` (branche par défaut) ; HEAD `arsenal-ha-backup-timeline` `033b1eff498ebd1107abe516bcca81c01f936f25` (branche `main`), confirmé identique entre le rapport terrain et l'API GitHub au moment de l'audit, `git status`/`diff` vides côté NAS hormis un fichier non suivi hors périmètre. |
| **Mise à jour** | 2026-09-09 — **volet NAS validé terrain bout-en-bout** : listener MQTT NAS opérationnel (identité `nas_admission`), `AUDIT` et `RELEASE_DIFF` admis, `run_id` corrélé, résultat transactionnel MQTT reçu, concurrence inter-opérations démontrée (voir §12.2). **Lot documentaire uniquement** : aucun runtime Arsenal, aucun nouveau contrat, aucun nouveau chantier ouverts par cette mise à jour ; aucun runtime NAS modifié (constat d'un état déjà livré). Prochaine phase : intégration Arsenal/Home Assistant. Voir §12.1/§12.2. |
| **Mise à jour** | 2026-09-09 — **Lot 5, pilote `AUDIT`, livré côté configuration Home Assistant** : `script.nas_admission_demander_audit` (génération `request_id`, ancrage `input_text.nas_admission_req_audit`, `ts`/`expires_at`/`source`, `mqtt.publish` QoS 1 `retain=false` sur `arsenal/nas/admission/command`, attente corrélée du résultat, nettoyage de l'ancrage), capteur MQTT brut `sensor.nas_admission_result_raw` (`arsenal/nas/admission/result`), capteurs de corrélation (`request_id`/`operation`/`run_id`/`transaction_verdict`) et capteur diagnostic `sensor.nas_admission_audit_etat_transaction` (état de la transaction `AUDIT`, filtré/latché sur le canal partagé `AUDIT`+`RELEASE_DIFF`). `RELEASE_DIFF` explicitement hors périmètre de ce lot (vocabulaire fermé §5, émission `operation: "AUDIT"` uniquement). **Non déployé, non testé terrain, aucun appel de test hors UI encore réalisé** : la preuve du Lot 5 n'est pas fournie par cette mise à jour. Aucun contrat modifié, aucune UI Lovelace, aucune automation planifiée. Voir §12.1/§12.3. |
| **Mise à jour** | 2026-09-09 — **Lot documentaire uniquement : preuve terrain du Lot 5 fournie** — `script.nas_admission_demander_audit` déployé et exécuté sur Home Assistant 2026.9.1 : `request_id` `9f88dea3-081e-498c-9fee-22342f99831a`, `run_id` `47f834bc-a193-4411-9716-0e0c35c04018`, `operation` `AUDIT`, `source` `arsenal`, terminaison transactionnelle `completed`, `wrapper_rc` `0`, durée ≈ 33 s, corrélation `request_id`/`run_id` bidirectionnelle HA↔NAS vérifiée, ancrage nettoyé, une seule exécution `AUDIT`, aucune reconnexion MQTT pendant la preuve. Résultat métier **observé séparément** sur `sensor.arsenal_self_audit_statut` (`ok`, 0 anomalie) — `transaction_verdict=completed` n'est à aucun moment assimilé à ce résultat. Listener MQTT NAS lancé manuellement au premier plan pour cette preuve puis arrêté proprement : hébergement/supervision permanent **toujours non livré à ce stade de la journée** (livré séparément le même jour, voir la ligne suivante). Aucun runtime Arsenal ni NAS modifié par cette mise à jour ; contrat `nas_transactionnel.md` corrigé uniquement sur son encart d'état d'implémentation (aucune clause normative touchée). `RELEASE_DIFF` (Lot 6) et UI (Lot 7) toujours non commencés. Voir §12.1/§12.4. |
| **Mise à jour** | 2026-09-09 — **Lot documentaire uniquement : preuve terrain de la supervision permanente du listener NAS fournie** — architecture DSM Task Scheduler (5 minutes, 00:00–23:55) → `admission/bin/mqtt_listener_watchdog.sh` → `admission/bin/mqtt_listener.py`, tâche `Arsenal - MQTT Listener Watchdog (C51)`, dépôt NAS canonique `/volume1/Backups_HA/ha_backup_timeline`, aucun secret inline. Cycle no-op sans doublon (RC0, même PID), fd lock enfant non hérité, `--stop` et réactivation validés terrain, relance automatique après disparition simulée en 4 min 46 s, instance unique laissée active en fin de preuve, connexion broker établie, abonnement `arsenal/nas/admission/command`, aucun secret dupliqué. Transaction `AUDIT` rejouée avec ce listener permanent (`request_id` `0de32d59-262a-49bf-9d88-2f2214f1a5f4`, `run_id` `02a3d516-883f-40ff-a19a-708e48081033`, `completed`/`wrapper_rc=0`, corrélation bidirectionnelle, aucune reconnexion MQTT pendant la transaction) ; résultat métier `ok`/0 anomalie/539 observations patrimoniales **observé séparément**, jamais assimilé au verdict transactionnel. **Hébergement/supervision permanent du listener NAS désormais livré et validé terrain** — seul point non livré restant du volet NAS. Dette mineure d'observabilité consignée (`runtime/mqtt_listener.log` bufferisé tant que le process tourne, non bloquant, aucun chantier ouvert). Aucun runtime Arsenal ni NAS modifié par cette mise à jour documentaire ; contrat `nas_transactionnel.md` corrigé uniquement sur son encart d'état d'implémentation (aucune clause normative touchée). `RELEASE_DIFF` (Lot 6) et UI (Lot 7) toujours non commencés ; dette ACL C52 inchangée. Voir §11.A6/§12.5. |
| **Mise à jour** | 2026-09-09 — **Lot 6, extension `RELEASE_DIFF`, livré côté configuration Home Assistant — code seul, non déployé, non testé terrain.** Prolonge le patron du Lot 5 sans le modifier : `input_text.nas_admission_req_release_diff` (helper dédié, jamais partagé avec le helper AUDIT), `script.nas_admission_demander_release_diff` (precheck, `request_id`, ancrage, `ts`/`expires_at`/`source`, `mqtt.publish` QoS 1 `retain=false` sur le topic commun `arsenal/nas/admission/command`, attente corrélée `request_id`+`operation=="RELEASE_DIFF"`, cleanup systématique), `sensor.nas_admission_release_diff_etat_transaction` (diagnostic filtré/latché sur `RELEASE_DIFF`, symétrique du diagnostic AUDIT). Sensor MQTT brut et couche de corrélation communs **réutilisés sans modification fonctionnelle** (deux commentaires d'en-tête corrigés uniquement, une mention devenue factuellement inexacte du seul consommateur AUDIT). Fenêtres temporelles (`expires_at` 60 s, timeout local HA 15 min) **délibérément identiques** à AUDIT, après audit documentaire des caractéristiques réelles de `release_diff.py` (aucune durée nominale contractualisée ; seul point de mesure terrain disponible, §12.2, montre RELEASE_DIFF achevé 36 s avant AUDIT) — justification consignée dans l'en-tête du script, à réviser après preuve terrain Lot 6 dédiée. AUDIT (Lot 5) **inchangé** (diff nul sur ses fichiers runtime, vérifié). Vérificateur statique ajouté (`scripts/arsenal_contracts/verify_nas_admission_transactionnel_lot6.py`, non câblé à `contracts_all.yml`/au registre de couverture CI — hors périmètre strict de ce lot, cf. §12.6) : preuve négative de détection (mutation injectée puis retirée). Aucun contrat modifié, aucune UI Lovelace, aucune automation planifiée, aucun ID d'automatisation HA inventé (§14 chantier). Voir §12.1/§12.6. |
| **Mise à jour** | 2026-09-09 — **Lot documentaire uniquement : preuve terrain du Lot 6 `RELEASE_DIFF` fournie** — `script.nas_admission_demander_release_diff` déployé et exécuté sur le clone runtime réellement exécuté par Home Assistant (`/config`, fast-forward propre `c01fdcd4`→`4e0059d1` jusqu'au merge de la PR #817 ; un premier fast-forward sur un clone Windows distinct n'était pas le clone exécuté par HA et n'a donc valu aucune preuve) : `request_id` `c49d02fa-1588-46e7-8e4f-27d9a26cf416`, `run_id` `c70c093f-fd37-4889-902e-2ff4310c13bf`, `operation` `RELEASE_DIFF`, admission reçue ≈ 1 s après `ts` (marge restante avant `expires_at` ≈ 59 s, sans confondre l'admission elle-même avec une durée d'exécution), terminaison transactionnelle `completed`, `wrapper_rc` `0`, durée totale `ts`→terminal ≈ 3 min 23 s — **`expires_at` borne l'admission de la demande, pas la durée totale d'une exécution déjà admise** : cette preuve montre précisément une admission dans la fenêtre contractuelle suivie d'une exécution poursuivie au-delà de `expires_at` sans anomalie (contrat §6, §9.5). Corrélation `request_id`/`run_id` bidirectionnelle HA↔NAS vérifiée, ancrage nettoyé, une seule exécution `RELEASE_DIFF`, aucune reconnexion MQTT pendant la transaction (listener permanent, même PID avant/après). Résultat métier observé **séparément** sur `sensor.arsenal_nas_release_diff_derniere_execution`/`sensor.arsenal_nas_release_diff_statut` (`ok`) : `transaction_verdict=completed` n'est à aucun moment assimilé à ce résultat. Aucun runtime Arsenal ni NAS modifié par cette mise à jour ; contrat `nas_transactionnel.md` corrigé uniquement sur son encart d'état d'implémentation (aucune clause normative touchée). UI Lovelace (Lot 7) toujours non commencée, non ouverte par ce lot ; preuves de replay/`BUSY`/crash-reprise et dette ACL C52 inchangées. Voir §12.1/§12.7. |
| **Mise à jour** | 2026-09-09 — **Lot 7, UI Lovelace, livré en code — non déployé, non testé terrain.** Nouvelle section « Commandabilité NAS (C51) » ajoutée à `18_lovelace/dashboards/systeme/nas.yaml` (dashboard NAS existant, aucune nouvelle page créée — `arsenal_self`/`arsenal_nas` restent des contrats système/transverses sans hub de domaine, `navigation/carte_domaines.md` §3/§6) : deux boutons de demande confirmés (`carte_action_nas_admission_demander`, satellite de `socle_action_script_confirme`, appelant exclusivement `script.turn_on` sur `script.nas_admission_demander_audit`/`_release_diff` — aucune publication MQTT, aucun `request_id` généré côté UI), deux cartes de diagnostic transactionnel (`carte_nas_admission_etat_transaction`, satellite de `socle_status_label`, vocabulaire fermé `nas_transactionnel.md` §10 traduit sans jamais colorer `completed` en vert ni l'assimiler à un succès métier), deux cartes de résultat métier strictement séparées (réutilisation de `arsenal_self_audit_status_card` pour AUDIT, nouvelle `arsenal_nas_release_diff_status_card` pour RELEASE_DIFF, construite sur les seules entités `arsenal_nas.md` §5.1, sans binary_sensor de fraîcheur/erreur inventé — §5.3 du même contrat). Conception dérivée exclusivement de la documentation UI existante (`ui/pattern_dashboard.md`, `ui/socle_ui/02_action.md`/`07_status.md`, `ui/couleurs/`) et des patrons déjà en usage dans le dépôt (`carte_action_arrosage_script`, `arsenal_self_audit_status_card`) — aucune convention inventée hors documentation. Aucun backend Lots 5/6 modifié (diff nul vérifié), aucune automation créée, aucun ID d'automatisation inventé (§14), aucun contrat NAS modifié. Voir §12.1/§12.8. |
| **Mise à jour** | 2026-09-10 — **Correction fonctionnelle du Lot 7 (UI Lovelace) — repositionnement Arsenal/Système, sans revert global de la PR #819.** Retrait intégral de la section « Commandabilité NAS (C51) » de `18_lovelace/dashboards/systeme/nas.yaml` ; nouvelle section « Arsenal — Audit & Release Diff (C51) » ajoutée à `18_lovelace/dashboards/systeme/principal.yaml` (dashboard Système), en cohérence avec la carte de résultat métier AUDIT déjà présente (`arsenal_self_audit_status_card`, non déplacée, non réécrite) ; ajout à côté d'elle de la carte de résultat métier RELEASE_DIFF (`arsenal_nas_release_diff_status_card`, livrée au Lot 7 mais jusqu'ici consommée par aucun dashboard). Les deux templates NAS-spécifiques du Lot 7 (`carte_action_nas_admission_demander`, `carte_nas_admission_etat_transaction`) sont déplacés de `19_button_card_templates/40_dashboards/nas/` vers `19_button_card_templates/40_dashboards/system/` (contenu inchangé) ; `nas/README.md` et `system/README.md` mis à jour en conséquence. Libellés UI adaptés pour nommer le service rendu à Arsenal en premier, le NAS en second plan (exécutant) — aucune entité backend renommée. Motif : le Lot 7 avait placé cette UI dans `nas.yaml` au seul motif que `arsenal_self`/`arsenal_nas` n'ont pas de hub de domaine dédié (`navigation/carte_domaines.md` §3/§6) ; cette lecture est corrigée — l'absence de hub ne désigne aucun domaine d'accueil par défaut, et le sens fonctionnel de `AUDIT`/`RELEASE_DIFF` reste Arsenal/Système, le NAS n'étant que l'exécutant technique externe de la demande (§4). Aucun fichier backend (Lots 5/6), script, helper, sensor MQTT, template sensor, automation, secret ou contrat NAS touchés. Voir §11.A10/§12.9. |
| **Mise à jour** | 2026-09-10 — **Décision produit actée : ouverture du Lot 8 — lot documentaire uniquement, aucune exécution.** État cible arbitré : `AUDIT` est déclenché uniquement à la demande depuis Arsenal/Home Assistant via MQTT ; `RELEASE_DIFF` est déclenché uniquement à la demande depuis Arsenal/Home Assistant via MQTT ; l'extraction timeline n'est exécutée que lorsqu'une demande Arsenal en a besoin ; aucune extraction périodique DSM, aucun `AUDIT` automatique DSM, aucun `RELEASE_DIFF` automatique DSM ne subsistent à l'état cible ; le NAS reste moteur d'exécution, Arsenal porte l'initiative. Les mécanismes indépendants de maintenance (watchdog MQTT, `Arsenal - Retention`, `Arsenal - Quarantine Purger`, protections natives DSM) ne sont pas concernés par cette décision. Chantier existant **C51** réutilisé tel quel : aucun nouvel identifiant, aucun nouveau chantier. Séquencement arrêté en six sous-lots 8.1→8.6, détaillé au §12.10 (nouveau) ; complément normatif au §9 (extraction sur demande, règle `rc=77` transitoire puis cible). Le Lot 8 reste **globalement non commencé** : cette mise à jour documente le plan, elle n'exécute aucun lot. Le Lot 9 (clôture documentaire) suit le Lot 8. |

---

## 1. Objet et périmètre

Arsenal doit pouvoir demander au NAS, via MQTT, l'exécution de deux opérations
métier **distinctes**, chacune raccordée à sa chaîne existante :

- **`AUDIT`** — identification du backup pertinent, stabilité démontrée,
  extraction/idempotence, audit patrimonial, publication du résultat ;
- **`RELEASE_DIFF`** — génération des diffs sémantiques inter-releases, sans
  paramètre métier (`--couple` non exposé en V1).

Le diff patrimonial forensic (`ha_backup_timeline_diff.py`, `_diff/`, contrat
[`diff_auto.md`](../../../outils_externes/nas_arsenal/diff/diff_auto.md)) est
**hors périmètre**, sauf contradiction démontrée.

Vocabulaire fermé : `AUDIT` | `RELEASE_DIFF`. Aucune exécution de commande NAS
arbitraire, aucun chemin shell fourni par HA, aucune commande générique
extensible sans contrat.

---

## 2. Arbitrages Direction déjà tranchés (repris tels quels)

Ces points sont **acquis** pour ce chantier et ne sont pas rediscutés par les
lots suivants sans décision explicite contraire :

1. Deux commandes V1 seulement : `AUDIT`, `RELEASE_DIFF`.
2. `RELEASE_DIFF` sans `--couple` ni aucun autre paramètre métier transmis
   par HA en V1.
3. HA est autorité de **demande**. Le NAS reste seul autorité d'**admission**,
   d'**exécution**, de **concurrence** et de **résultat**. `arsenal_self.md`
   et `arsenal_nas.md` ne sont **pas** autorités du résultat métier : ils
   consomment, projettent et diagnostiquent la fraîcheur/disponibilité, sans
   jamais recalculer le verdict.
4. Backend Arsenal décide, UI Lovelace rend — aucune logique de transport
   MQTT dans le bouton.
5. Corrélation `request_id → run_id` obligatoire en V1, pour les deux
   opérations. Le NAS attribue le `run_id` au niveau admission/exécution,
   **avant** l'entrée dans le moteur métier — et non plus, comme aujourd'hui
   pour `release_diff.py`, à l'intérieur du moteur lui-même.
6. `BUSY` explicite et immédiat si l'opération demandée est déjà en cours.
   Aucune coalescence en V1. Aucune file d'attente.
7. Aucun verrou global `AUDIT`/`RELEASE_DIFF` sans invariant partagé
   démontré — les deux opérations peuvent tourner simultanément.
8. La garantie de stabilité du backup (aujourd'hui portée par
   `watch_new_backup.sh`) reste une **responsabilité NAS**, quel que soit le
   sort futur de son implémentation actuelle. Ce chantier contractualise la
   garantie, pas le script qui la porte aujourd'hui.
9. La transaction de commande et le résultat métier sont **formellement
   distincts** et ne sont jamais fusionnés, y compris dans le nommage des
   champs. Une transaction techniquement terminée avec succès peut produire
   un résultat métier en anomalie.
10. L'exclusion mutuelle `RELEASE_DIFF` (absente aujourd'hui — confirmé par
    lecture intégrale de `release_diff.py` et `run_release_diff.sh`, aucun
    verrou, aucun `flock`) est un **prérequis bloquant** avant toute
    activation d'une commande MQTT `RELEASE_DIFF`. Aucune tolérance V1.
11. Aucun ID d'automatisation Home Assistant n'est inventé par ce chantier
    (doctrine [`id_automatisations.md`](../../../architecture/03_doctrines/id_automatisations.md)).
    Les IDs éventuels sont fournis par la Direction au moment de
    l'implémentation runtime.

---

## 3. Terminologie terrain — précision opposable

Formulation à respecter dans toute documentation de transition ou de
décommissionnement issue de ce chantier : il n'existe pas « trois
déclencheurs AUDIT ». Le terrain établit :

- **une tâche d'extraction périodique indépendante** (`Arsenal - Timeline
  Backups HA`, 5 minutes, extraction seule — n'appelle ni l'audit ni la
  publication MQTT) ;
- **deux chemins de déclenchement du pipeline AUDIT** (extraction + audit +
  MQTT) : le watcher (`Arsenal - Pipeline Watcher`, réactif, avec contrôle
  de stabilité) et la tâche directe quotidienne (`Pipeline HA`, 02:45,
  inconditionnelle).

La formulation « trois déclencheurs AUDIT », employée dans une version
antérieure de l'analyse de ce chantier, est erronée et ne doit pas être
reprise.

---

## 4. Matrice des autorités

| Strate | Autorité | Responsabilité | Interdictions |
|---|---|---|---|
| UI Arsenal (Lovelace) | Aucune | Exprimer une intention utilisateur | Ne parle jamais MQTT ; ne porte aucune logique de transport ni de concurrence |
| Backend Arsenal | Demande | Construire la commande, vocabulaire fermé, `request_id` | N'exécute rien ; ne décide jamais du résultat métier |
| Transport MQTT | Aucune | Acheminer commande et état | N'interprète pas le payload ; pas de retain sur le canal commande |
| Admission NAS | Admission | Vocabulaire fermé, déduplication, concurrence, ouverture/fermeture de transaction, attribution du `run_id` | Ne modifie jamais le vocabulaire reçu |
| Moteur AUDIT | Exécution (AUDIT) | Produit le verdict patrimonial existant | Ne décide pas de la concurrence globale |
| Moteur RELEASE_DIFF | Exécution (RELEASE_DIFF) | Produit le diff/résumé existant | Idem ; reste « clos » comme aujourd'hui pour sa sémantique propre |
| Domaine HA `arsenal_self` | Consommation/diagnostic | Expose, qualifie la fraîcheur du résultat AUDIT | Ne recalcule jamais le verdict patrimonial |
| Domaine HA `arsenal_nas` | Consommation/diagnostic | Expose l'état d'exécution RELEASE_DIFF | Ne recalcule jamais le résultat |

---

## 5. Contrat transactionnel commun

Le contrat sémantique (vocabulaire, identité de commande, admission,
idempotence, `BUSY`, corrélation `request_id`↔`run_id`, terminaison
transactionnelle, sécurité minimale) est intégralement porté par
[`contrats/nas_transactionnel.md`](../../../contrats/nas_transactionnel.md).

Ce document de chantier **ne duplique pas** ce contrat. Les spécialisations
moteur restent souveraines dans leurs contrats propres :
[`outils_externes/nas_arsenal/diff/diff_release.md`](../../../outils_externes/nas_arsenal/diff/diff_release.md),
[`diff/release_diff_mqtt.md`](../../../outils_externes/nas_arsenal/diff/release_diff_mqtt.md),
[`audit/audit.md`](../../../outils_externes/nas_arsenal/audit/audit.md),
[`audit/mqtt.md`](../../../outils_externes/nas_arsenal/audit/mqtt.md).

---

## 6. Invariants propres à AUDIT

- Couvre, à la manière de `run_pipeline.sh` : identification du backup
  pertinent, stabilité démontrée, extraction/idempotence, audit,
  publication du résultat. Le périmètre exact (déclenchement systématique
  d'une extraction, ou audit du dernier `versions/` déjà présent) reste à
  confirmer à l'implémentation — voir §14.
- La garantie de stabilité (aujourd'hui : double mesure de taille à 60 s
  d'intervalle) reste NAS, indépendamment de son implémentation actuelle.
- L'atomicité de publication dans `versions/` (rename atomique après
  marqueur de complétude) est préservée sans modification — c'est elle qui
  garantit qu'AUDIT et RELEASE_DIFF ne s'observent jamais en écriture
  partielle l'un l'autre.
- Un identifiant d'exécution corrélable (`run_id`) est créé — n'existe pas
  aujourd'hui dans la chaîne AUDIT.
- Le résultat métier existant (`arsenal_self`, `ok`/`alert`/`error`) n'est
  pas modifié par ce chantier.
- Concurrence AUDIT+AUDIT : non sûre aujourd'hui (verrou `run_audit.sh` non
  atomique, sans détection de PID vivant ; aucun verrou partagé entre
  extraction directe et extraction embarquée dans `run_pipeline.sh`). Une
  commande MQTT AUDIT réutilise et durcit les verrous existants plutôt que
  d'en créer un nouveau et incompatible.

## 7. Invariants propres à RELEASE_DIFF

- Aucune option `--couple` ni aucun autre paramètre métier exposé via MQTT
  en V1 (le mode batch consécutif de `release_diff.py` est seul concerné).
- Exclusion mutuelle RELEASE_DIFF+RELEASE_DIFF : **prérequis bloquant**
  avant activation (voir §2.10) — travail moteur/wrapper indépendant de
  MQTT.
- `run_id` corrélable à `request_id` : le mécanisme `run_id`/`event_id`
  déjà spécifié par `diff_release.md`/`release_diff_mqtt.md` est réutilisé,
  non redéfini ; seule son origine change (admission NAS, avant le moteur,
  au lieu du moteur lui-même).
- Les états métier existants (`ok`/`partial`/`error`, domaine
  `arsenal_nas`) restent inchangés.
- Jamais fusionné avec AUDIT — chaînes métier strictement distinctes.

---

## 8. Politique de concurrence

| Situation | Politique |
|---|---|
| AUDIT demandé, AUDIT déjà en cours | Rejet explicite `BUSY`. Aucune coalescence, aucune file. |
| RELEASE_DIFF demandé, RELEASE_DIFF déjà en cours | Rejet explicite `BUSY`. Aucune coalescence, aucune file. |
| AUDIT demandé, RELEASE_DIFF en cours | Autorisé — aucun invariant partagé démontré ne justifie un verrou global. |
| RELEASE_DIFF demandé, AUDIT en cours | Autorisé — même raison. |

Point de vigilance annexe, hors périmètre strict de ce chantier : la tâche
`Arsenal - Retention` (04:00) modifie `versions/` sans verrou partagé avec
RELEASE_DIFF (03:15) ; aucun chevauchement d'horaire aujourd'hui.

---

## 9. Architecture transitoire et décommissionnements possibles

Aucun big bang. Le canal MQTT s'ajoute comme chemin supplémentaire, sans
toucher aux tâches DSM existantes tant que leur garantie n'est pas reprise
et prouvée en terrain.

| Tâche DSM | Fonction actuelle | Conservation transitoire | Condition de suppression | Mécanisme cible |
|---|---|---|---|---|
| `Arsenal - Timeline Backups HA` (extraction directe, 5 min) | Ingestion continue de `versions/`, alimente aussi RELEASE_DIFF et la rétention | Oui | Décision produit (ingestion continue vs sur-demande), pas seulement technique | AUDIT-via-MQTT (si son périmètre inclut l'extraction) ou déclencheur d'ingestion dédié |
| `Arsenal - Pipeline Watcher` | Déclenchement réactif avec contrôle de stabilité | Oui | Preuve terrain que l'admission NAS porte elle-même la garantie de stabilité | Contrôle de stabilité migré dans la couche admission NAS |
| `Pipeline HA` (02:45, inconditionnel) | Filet de sécurité quotidien | Oui | Preuve qu'un déclenchement planifié MQTT ne laisse aucune fenêtre sans audit | Automatisation Arsenal planifiée émettant `AUDIT` |
| `Arsenal - Release Diff` (03:15) | Déclenchement quotidien inconditionnel | Oui | Verrou RELEASE_DIFF ajouté (§2.10) **et** preuve terrain du chemin MQTT | Automatisation Arsenal planifiée émettant `RELEASE_DIFF` |

`Arsenal - Retention` et `Arsenal - Quarantine Purger` restent hors
périmètre de ce chantier.

**Extraction sur demande — arbitrage du 2026-09-10.** L'extraction timeline
n'est plus conçue comme un flux périodique indépendant : à l'état cible,
elle n'est exécutée que lorsqu'une demande Arsenal (`AUDIT` ou
`RELEASE_DIFF`, via MQTT) en a besoin. Aucune extraction périodique DSM,
aucun `AUDIT` automatique DSM, aucun `RELEASE_DIFF` automatique DSM ne
doivent subsister à l'état cible ; le NAS reste moteur d'exécution, Arsenal
porte l'initiative. Le séquencement de ce basculement est détaillé au
§12.10 (Lot 8, sous-lots 8.1→8.6).

**Règle `rc=77` — transitoire puis cible.** Pendant la coexistence
transitoire décrite par ce tableau, `rc=77` reste un échec transactionnel
`technical_failure` **connu**, résultant d'une collision possible avec
l'ancien mécanisme de déclenchement direct DSM — ce n'est ni un succès, ni
un résultat métier nominal. À l'état cible, une fois le dernier appelant
DSM direct de l'extracteur retiré (§12.10, sous-lot 8.5), une occurrence de
`rc=77` devient **anormale** : aucun concurrent DSM légitime ne doit plus
appeler directement l'extracteur.

---

## 10. Sécurité (invariants minimaux)

- Vocabulaire fermé `AUDIT`/`RELEASE_DIFF`, rien d'autre n'est interprété.
- Aucun argument shell arbitraire transmis par HA.
- Commandes non retenues (`retain=false`) sur le canal de commande —
  contraste assumé avec les topics état, retenus.
- Déduplication applicative (mémoire persistante bornée côté NAS), en sus
  du QoS MQTT.
- Identité MQTT dédiée au canal de commande : **obligatoire**, distincte
  des comptes existants (`nas_audit`, `nas_imprimerie`, `boiler_bridge`,
  `rain_bird_mqtt`) — identité `nas_admission`, opérationnelle et
  effectivement utilisée en terrain pour les preuves AUDIT/RELEASE_DIFF
  (§12.2). Moindre privilège (cantonnement ACL par topic) reste la
  **cible normative** de cette identité dédiée, non garantie aujourd'hui —
  voir constat ci-dessous.
- **Constat terrain (audit broker, 2026-09-09).** Le broker MQTT de
  production est l'add-on officiel HA Mosquitto (`core_mosquitto`),
  authentification par comptes HA locaux, `customize.active = false` :
  aucune ACL par topic active aujourd'hui,
  pour aucun compte. Activer une ACL par topic impose une politique
  explicite globale à tous les comptes du broker, pas seulement au futur
  compte C51 — chantier broker transversal (HA, Zigbee2MQTT, chauffage,
  arrosage), **non ouvert par ce chantier**. Le cantonnement ACL par topic
  de `nas_admission` ne peut donc pas être garanti sans cette migration.
- **Dette explicite.** Identité dédiée sans cantonnement ACL par topic =
  dette de sécurité documentée, non tranchée par ce chantier — voir §13.

---

## 11. Documentation normative — ce que ce chantier modifie

### A. Modifié à l'ouverture (ce lot)

- `contrats/nas_transactionnel.md` *(nouveau)*.
- `contrats/arsenal_nas.md` — statut `proposé/non implémenté` → `actif`
  (démontré, §2.3 déjà correct) ; renvoi vers `nas_transactionnel.md`.
- `contrats/arsenal_self.md` — renvoi vers `nas_transactionnel.md`.
- `contrats/index.md` — ligne pour `nas_transactionnel.md`.
- `outils_externes/nas_arsenal/diff/release_diff_mqtt.md` — statut
  `proposé/non implémenté` → `actif/implémenté` (démontré).
- `outils_externes/nas_arsenal/diff/diff_auto.md` — fréquence 30→5 minutes
  (correction factuelle, même tâche DSM que le terrain) ; un renvoi vers
  la continuation du pipeline AUDIT.
- `outils_externes/nas_arsenal/pipeline_watcher.md` — statut
  `proposition initiale` → `actif/implémenté` ; note de coexistence avec
  les deux autres chemins de déclenchement.
- `architecture/ecosysteme_depots_satellites.md` — fiche manquante pour
  `arsenal-ha-backup-timeline` (absente du registre des dépôts gouvernés).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.

### A2. Lot documentaire intermédiaire (2026-09-09) — après merge NAS local

- Le présent document — Statut, `Mesure amont`/`Mise à jour`, §12.1
  (nouveau).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **non modifié** (toujours v1.1.1) ;
  vérifié conforme à l'état livré.
- Aucun autre contrat, aucune doc runtime, aucune UI, aucun CI touchés par
  ce lot.

### A3. Lot documentaire — preuves terrain NAS (2026-09-09)

- Le présent document — Statut, `Mise à jour`, §10 (identité `nas_admission`),
  §12.1 (Lot 4), §12.2 (nouveau, « Preuves terrain NAS »), §13 (arbitrage
  ACL rendu).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51 ; ligne C52 (référence
  factuelle à l'arbitrage rendu, corrigée en conséquence).
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **non modifié** ; relu et vérifié
  conforme à l'état livré et validé terrain (aucune contradiction
  détectée).
- Aucun runtime Arsenal, aucun runtime NAS, aucune UI, aucun CI touchés
  par ce lot. C51 n'est pas clos.

### A4. Lot 5 — backend Arsenal, pilote AUDIT (2026-09-09)

Premier lot runtime **Arsenal** (dépôt `arsenal`) de ce chantier — tout ce qui
précède (A à A3) était NAS ou documentaire pur.

- Le présent document — Statut, `Mise à jour`, §12.1 (ligne Lot 5), présent
  §12.3 (nouveau).
- `04_input_texts/system/nas_admission/request_id_transactionnels.yaml`
  *(nouveau)* — helper d'ancrage `input_text.nas_admission_req_audit`.
- `10_scripts/system/nas_admission_demander_audit.yaml` *(nouveau)* —
  `script.nas_admission_demander_audit`.
- `14_mqtt_sensors/system/nas_admission_result_raw.yaml` *(nouveau)* —
  transport brut `arsenal/nas/admission/result`.
- `12_template_sensors/system/nas_admission/nas_admission_result_correlation.yaml`
  *(nouveau)* — extraction `request_id`/`operation`/`run_id`/`transaction_verdict`.
- `12_template_sensors/system/nas_admission/nas_admission_audit_etat_transaction.yaml`
  *(nouveau)* — diagnostic AUDIT, filtré/latché sur le canal partagé.
- `contrats/nas_transactionnel.md` — **non modifié** ; ce lot implémente le
  contrat existant (§6, §13), il ne le révise pas.
- Aucun contrat NAS, aucune UI Lovelace, aucune automation planifiée,
  aucun ID d'automatisation HA inventé (§14 chantier) touchés par ce lot.
  `RELEASE_DIFF` explicitement hors périmètre (Lot 6).

### A5. Lot documentaire — preuve terrain du Lot 5 (2026-09-09)

Lot documentaire pur : aucun fichier runtime Arsenal ni NAS touché. Documente
la preuve terrain du Lot 5 (A4), fournie après coup.

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §12.1 (ligne
  Lot 5), §12.3 (lead-in), §12.4 (nouveau, « Preuve terrain Lot 5 »).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **encart d'état d'implémentation corrigé
  uniquement** (la phrase affirmant l'absence de listener MQTT, de backend
  Arsenal de commande et de preuve terrain était devenue factuellement fausse
  au regard de §12.2 et de la présente preuve) ; aucune clause normative
  (§1-§17), aucun vocabulaire, aucun topic, aucune sémantique modifiés ;
  aucune renumérotation ; version du contrat inchangée (aucune règle du
  dépôt n'impose de bump pour une correction d'encart d'état — seul le §17
  du contrat impose une révision versionnée pour une modification du
  vocabulaire fermé, de la grammaire de terminaison ou de la corrélation
  `request_id`↔`run_id`, non concernés ici).
- Aucun runtime Arsenal, aucun runtime NAS, aucune UI, aucun CI touchés par
  ce lot. C51 n'est pas clos.

### A6. Lot documentaire — preuve terrain de la supervision permanente du
listener NAS (2026-09-09)

Lot documentaire pur : aucun fichier runtime Arsenal ni NAS touché par ce
lot lui-même. Documente une preuve terrain fournie après coup, distincte de
celle du Lot 5 (A5) : le mode permanent du listener MQTT NAS, supervisé par
tâche planifiée DSM (`admission/bin/mqtt_listener_watchdog.sh` →
`admission/bin/mqtt_listener.py`, dépôt NAS canonique
`/volume1/Backups_HA/ha_backup_timeline`), déployé et validé terrain.

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §11.A6
  (nouveau), §12.1 (tableau et paragraphe « Non livré »), §12.5 (nouveau,
  « Supervision permanente du listener MQTT NAS »), §13 (item Docker/
  supervision alternative levé).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **encart d'état d'implémentation
  corrigé uniquement** (la phrase affirmant l'hébergement/supervision
  permanent du listener comme non livré était devenue factuellement fausse
  au regard de la présente preuve) ; aucune clause normative (§1-§17),
  aucun vocabulaire, aucun topic, aucune sémantique modifiés ; aucune
  renumérotation ; version du contrat inchangée (même règle qu'au lot A5 :
  aucune règle du dépôt n'impose de bump pour une correction d'encart
  d'état).
- Aucun runtime Arsenal, aucun runtime NAS, aucune UI, aucun CI touchés par
  ce lot. C51 n'est pas clos : `RELEASE_DIFF` (Lot 6) et UI (Lot 7) restent
  non commencés, la dette ACL C52 est inchangée.

### A7. Lot 6 — backend Arsenal, extension RELEASE_DIFF (2026-09-09)

Second lot runtime **Arsenal** (dépôt `arsenal`) de ce chantier. Prolonge le
Lot 5 (A4) à la seconde opération du vocabulaire fermé, sans modifier ses
fichiers.

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §11.A7
  (nouveau), §12.1 (tableau, ligne Lot 6, paragraphe « Non livré »), présent
  §12.6 (nouveau).
- `04_input_texts/system/nas_admission/request_id_transactionnels_release_diff.yaml`
  *(nouveau)* — helper d'ancrage dédié
  `input_text.nas_admission_req_release_diff`.
- `10_scripts/system/nas_admission_demander_release_diff.yaml` *(nouveau)* —
  `script.nas_admission_demander_release_diff`.
- `12_template_sensors/system/nas_admission/nas_admission_release_diff_etat_transaction.yaml`
  *(nouveau)* — diagnostic RELEASE_DIFF, filtré/latché sur le canal partagé,
  symétrique du diagnostic AUDIT du Lot 5.
- `14_mqtt_sensors/system/nas_admission_result_raw.yaml` et
  `12_template_sensors/system/nas_admission/nas_admission_result_correlation.yaml`
  — **réutilisés sans modification fonctionnelle** ; seule une ligne de
  commentaire d'en-tête corrigée dans chacun (mention devenue factuellement
  inexacte d'un unique consommateur AUDIT, désormais consommés par les deux
  scripts) — aucun template, aucun filtre par opération, aucun topic/QoS/
  retain touchés.
- `scripts/arsenal_contracts/verify_nas_admission_transactionnel_lot6.py`
  *(nouveau)* — vérificateur statique autonome (invariants §5/§6/§10/§12 du
  contrat, pour les deux opérations), **non câblé** à
  `.github/workflows/contracts_all.yml` ni à
  `check_ci_coverage_registry.py` : le câblage complet implique une mise à
  jour du registre de couverture CI (`REGISTRE_COUVERTURE_VERIFICATION.md`),
  document hors périmètre strict de ce lot (§1/§13 de la mission Lot 6) —
  laissé en suite explicite, cf. §12.6.
- `10_scripts/system/nas_admission_demander_audit.yaml`,
  `04_input_texts/system/nas_admission/request_id_transactionnels.yaml`
  (helper AUDIT) — **non modifiés** (diff nul, vérifié par
  `git diff --stat` et par le vérificateur statique ci-dessus).
- `contrats/nas_transactionnel.md` — **non modifié** ; ce lot implémente le
  contrat existant (§6, §13, déjà en vigueur pour `RELEASE_DIFF` depuis sa
  fixation), il ne le révise pas ; aucune contradiction normative
  découverte.
- Aucun contrat NAS, aucune UI Lovelace, aucune automation planifiée, aucun
  ID d'automatisation HA inventé (§14 chantier) touchés par ce lot. Aucun
  déploiement, aucune preuve terrain fournie par ce lot (voir §12.6).

### A8. Lot documentaire — preuve terrain du Lot 6 (2026-09-09)

Lot documentaire pur : aucun fichier runtime Arsenal ni NAS touché. Documente
la preuve terrain du Lot 6 (A7), fournie après coup sur le clone réellement
exécuté par Home Assistant (`/config`).

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §12.1
  (tableau, ligne Lot 6), §12.6 (constat de preuve mis à jour), présent
  §12.7 (nouveau, « Preuve terrain Lot 6 »).
- `audits/REGISTRE_CHANTIERS.md` — ligne C51.
- `audits/index.md` — renvoi C51.
- `contrats/nas_transactionnel.md` — **encart d'état d'implémentation
  corrigé uniquement** (la phrase affirmant que `RELEASE_DIFF` côté backend
  Arsenal n'était pas livré était devenue factuellement fausse au regard de
  la présente preuve) ; aucune clause normative (§1-§17), aucun vocabulaire,
  aucun topic, aucune sémantique modifiés ; aucune renumérotation ; version
  du contrat inchangée (même règle qu'aux lots A5/A6 : aucune règle du
  dépôt n'impose de bump pour une correction d'encart d'état).
- Aucun runtime Arsenal, aucun runtime NAS, aucune UI, aucun CI touchés par
  ce lot. C51 n'est pas clos : UI (Lot 7) reste non commencée, preuves de
  replay/`BUSY`/crash-reprise et dette ACL C52 restent ouvertes.

### A9. Lot 7 — UI Lovelace (2026-09-09)

Troisième lot runtime **Arsenal** (dépôt `arsenal`) de ce chantier — UI
uniquement, aucun backend touché (Lots 5/6 inchangés).

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §11.A9
  (nouveau), §12 (tableau, ligne Lot 7), §12.1 (paragraphe « Non livré »),
  présent §12.8 (nouveau).
- `18_lovelace/dashboards/systeme/nas.yaml` — nouvelle section
  « 🗂️ Commandabilité NAS (C51) » : deux boutons de demande confirmés,
  deux cartes de diagnostic transactionnel, deux cartes de résultat
  métier. Aucune autre section modifiée.
- `19_button_card_templates/40_dashboards/nas/10_action/carte_action_nas_admission_demander.yaml`
  *(nouveau)* — satellite de `socle_action_script_confirme`, générique
  AUDIT/RELEASE_DIFF ; appelle exclusivement `script.turn_on` sur le
  script backend désigné par l'instance.
- `19_button_card_templates/40_dashboards/nas/20_diagnostic_transaction/carte_nas_admission_etat_transaction.yaml`
  *(nouveau)* — satellite de `socle_status_label`, générique
  AUDIT/RELEASE_DIFF ; affiche le vocabulaire transactionnel fermé
  (`nas_transactionnel.md` §10) sans jamais lire une entité de résultat
  métier pour se conclure.
- `19_button_card_templates/40_dashboards/system/20_supervision/arsenal_nas_release_diff_status_card.yaml`
  *(nouveau)* — satellite direct de `arsenal_self_audit_status_card`
  (même socle) pour le résultat métier RELEASE_DIFF
  (`sensor.arsenal_nas_release_diff_statut`), sans binary_sensor de
  fraîcheur/erreur inventé (`arsenal_nas.md` §5.3).
- `19_button_card_templates/40_dashboards/nas/README.md` — deux
  familles UI ajoutées (action, diagnostic transactionnel) pour rester
  factuel vis-à-vis des deux fichiers ci-dessus.
- `contrats/nas_transactionnel.md` — **encart d'état d'implémentation
  corrigé uniquement** (la phrase affirmant qu'aucune UI Lovelace
  n'était livrée était devenue factuellement fausse) ; aucune clause
  normative (§1-§17), aucun vocabulaire, aucun topic, aucune sémantique
  modifiés ; aucune renumérotation ; version du contrat inchangée
  (même règle qu'aux lots A5/A6/A8).
- `10_scripts/system/nas_admission_demander_audit.yaml`,
  `10_scripts/system/nas_admission_demander_release_diff.yaml`,
  `12_template_sensors/system/nas_admission/**`,
  `04_input_texts/system/nas_admission/**` — **non modifiés** (Lots 5/6
  intégralement inchangés ; ce lot ne fait que les appeler/les lire
  depuis l'UI).
- Aucun contrat NAS modifié, aucune automation créée, aucun ID
  d'automatisation HA inventé (§14 chantier), aucune publication MQTT
  directe depuis Lovelace. Aucun déploiement, aucune preuve d'usage réel
  fournie par ce lot (voir §12.8).

### A10. Correction Lot 7 — repositionnement fonctionnel de l'UI (2026-09-10)

Correction du merge de la PR #819 (Lot 7, §11.A9/§12.8), après arbitrage
Direction. **Ne revert pas #819** : la PR reste mergée, ce lot corrige
l'emplacement fonctionnel de l'UI qu'elle a livrée. Aucun backend touché
(Lots 5/6 inchangés — diff nul vérifié).

- Le présent document — Statut, `Mise à jour` (nouvelle ligne), §11.A10
  (nouveau), §12.1 (ligne Lot 7 complétée), présent §12.9 (nouveau).
- `18_lovelace/dashboards/systeme/nas.yaml` — retrait intégral de la
  section « 🗂️ Commandabilité NAS (C51) » ajoutée par #819. Aucune autre
  section touchée.
- `18_lovelace/dashboards/systeme/principal.yaml` — nouvelle section
  « 🧠 Arsenal — Audit & Release Diff (C51) » : deux boutons de demande
  confirmés (AUDIT/RELEASE_DIFF), deux cartes de diagnostic
  transactionnel. La carte de résultat métier AUDIT déjà présente
  (`arsenal_self_audit_status_card`) n'est ni déplacée ni réécrite ; la
  carte de résultat métier RELEASE_DIFF (`arsenal_nas_release_diff_status_card`,
  livrée au Lot 7 mais jusqu'ici consommée par aucun dashboard) est
  ajoutée juste après elle.
- `19_button_card_templates/40_dashboards/nas/10_action/carte_action_nas_admission_demander.yaml`
  → déplacé vers
  `19_button_card_templates/40_dashboards/system/50_action_admission_arsenal/`
  (contenu inchangé).
- `19_button_card_templates/40_dashboards/nas/20_diagnostic_transaction/carte_nas_admission_etat_transaction.yaml`
  → déplacé vers
  `19_button_card_templates/40_dashboards/system/51_diagnostic_transaction_arsenal/`
  (contenu inchangé).
- `19_button_card_templates/40_dashboards/nas/README.md` — familles E et F
  (C51 Lot 7) retirées : ces cartes ne relèvent pas du domaine `nas/`
  (diagnostic matériel/logiciel du NAS), mais du domaine
  système/transverse Arsenal.
- `19_button_card_templates/40_dashboards/system/README.md` — nouvelles
  familles F/G documentées pour les templates déjà présents
  (`arsenal_self_audit_status_card`, `arsenal_nas_release_diff_status_card`)
  et pour les deux templates déplacés ; type UI `action` désormais utilisé
  dans ce domaine.
- `audits/REGISTRE_CHANTIERS.md`, `audits/index.md` — ligne C51 complétée
  (correction de l'emplacement documentée en supplément, historique non
  réécrit).
- `contrats/nas_transactionnel.md` — **non modifié** : son encart d'état
  ne nommait déjà aucun chemin de dashboard, aucune correction requise.
- `10_scripts/system/nas_admission_demander_audit.yaml`,
  `10_scripts/system/nas_admission_demander_release_diff.yaml`,
  `12_template_sensors/system/nas_admission/**`,
  `04_input_texts/system/nas_admission/**` — **non modifiés** (Lots 5/6
  intégralement inchangés).
- Aucun contrat NAS modifié, aucune automation créée, aucun ID
  d'automatisation HA inventé (§14 chantier), aucune publication MQTT
  directe depuis Lovelace, aucun secret touché.

### B. Référencés, non modifiés

`outils_externes/nas_arsenal/audit/audit.md`, `audit/mqtt.md`,
`diff/diff_release.md` (contenu substantif — exact pour son périmètre
actuel), `contrats/switchbot_transactionnel.md` (précédent transactionnel
réutilisé), `quarantine_purger.md`, `retention_manager.md` (hors
périmètre).

### C. À modifier au moment des lots runtime

- `diff/diff_release.md` — invariant de concurrence, une fois le verrou
  RELEASE_DIFF effectivement implémenté ; clause « `run_id` attribué par
  l'admission NAS ».
- `schemas_ascii/pipeline_nas_ha.md` — schéma à jour une fois
  l'admission implémentée ; correction de l'invariant I-8 (« la
  concurrence d'extraction est neutralisée par flock », qui surstate déjà
  la réalité aujourd'hui).
- Dérive de nommage `CONTRAT_AUDIT_MQTT.md` (référencée dans
  `publish_audit_mqtt.py` et 6 sensors Arsenal, alors que le contrat réel
  est `audit/mqtt.md`) — hors portée documentaire pure, nécessite de
  toucher `.py`/`.yaml`.
- Extension éventuelle des schémas `arsenal_nas.md`/`arsenal_self.md`/
  `audit/mqtt.md`/`release_diff_mqtt.md` pour porter `run_id`/`request_id`.
- Documentation locale dans `arsenal-ha-backup-timeline` — réévaluée à ce
  moment, non un principe définitif.

### D. À modifier à la clôture

- `audits/REGISTRE_CHANTIERS.md` — passage de ① Actifs à `Clos récent`.
- Le présent document — §15 renseigné.
- `architecture/ecosysteme_depots_satellites.md` — mise à jour de la fiche
  §4.8 si des tâches DSM sont effectivement décommissionnées.

---

## 12. Découpage en lots

| Lot | Dépôt | Objectif | Dépendances | Preuve | STOP | Risque principal |
|---|---|---|---|---|---|---|
| 1 (ce lot) | `arsenal` | Contrat transactionnel + ouverture chantier + corrections factuelles | Arbitrages §2 tranchés | Documents relus/validés, aucune implémentation | Un invariant reste ambigu | Contrat sous-spécifié |
| 2 | `arsenal-ha-backup-timeline` | Verrou RELEASE_DIFF (cycle lecture-calcul-écriture) | Aucune (correctif indépendant de MQTT) | Test de double-exécution simulée sans corruption | Régression de l'idempotence existante | Modifier un moteur en production quotidienne |
| 3 | `arsenal-ha-backup-timeline` | Verrou AUDIT durci + `run_id` corrélable | Lot 1 (forme du run_id) | Exécution de test `request_id`→`run_id` traçable | Casse le contrat MQTT état existant | Toucher `run_audit.sh`, en prod quotidienne |
| 4 | `arsenal-ha-backup-timeline` | Admission NAS minimale, une seule opération pilote | Lots 1–3 | Commande MQTT manuelle → run_id corrélé → résultat identique à un déclenchement DSM | Divergence avec le comportement DSM existant | Concurrence avec les tâches DSM si verrou non partagé |
| 5 | `arsenal` | Backend Arsenal — émission de commande | Lot 4 validé terrain | Appel de test hors UI | Vocabulaire plus large que le contrat | Couplage prématuré à une UI non stabilisée |
| 6 | `arsenal-ha-backup-timeline` + `arsenal` | Extension à la seconde opération | Lot 5 | Idem Lot 4 | Verrou partagé non justifié entre AUDIT et RELEASE_DIFF | Tentation de fusionner les deux chaînes |
| 7 | `arsenal` | UI Lovelace (bouton) | Lots 5–6 | Usage réel *(non fournie — code livré, non déployé, voir §12.8)* | Le bouton porte lui-même une logique MQTT *(écarté — voir §12.8)* | Régression backend décide/UI rend *(écarté par construction — voir §12.8)* |
| 8 | NAS (hors Git) + doc | Décommissionnement conditionnel des tâches DSM | Lots 4–7 + observation terrain | N jours sans écart ancien/nouveau mécanisme | Toute perte de garantie constatée | Décommissionnement prématuré |
| 9 | `arsenal` + `arsenal-ha-backup-timeline` | Clôture documentaire | Lot 8 | Revue documentaire | — | Dette documentaire si sauté |

---

### 12.1 État d'avancement — mise à jour documentaire du 2026-09-09

Lot documentaire intermédiaire uniquement : ne modifie pas le découpage
ci-dessus, ne referme aucun lot, n'ouvre aucun nouveau lot. Documente l'état
réel après le merge du socle transactionnel NAS local dans
`arsenal-ha-backup-timeline`. Vocabulaire de statut : « livré, mergé » /
« livré, mergé, testé » (dépôt) — jamais « déployé » ni « validé terrain »
tant que la preuve terrain correspondante n'existe pas.

| Lot | État | Constat |
|---|---|---|
| 1 | Livré | Contrat `nas_transactionnel.md` (v1.1.1) et ouverture du chantier — inchangé par ce lot. |
| 2 — verrou RELEASE_DIFF | **Livré, mergé** | Exclusion mutuelle robuste, verrou métier `runtime/release_diff.lock`, RC 75 si occupé (chemin legacy), `--run-id` explicite, comportement legacy DSM conservé, aucun paramètre métier libre exposé. Non déployé, non validé terrain. |
| 3 — durcissement AUDIT + `run_id` | **Livré, mergé** | AUDIT commandable via `run_pipeline.sh` (sélection/extraction, contrôle de stabilité, audit, publication, extraction runtime informative), verrou métier `runtime/run_pipeline.lock`, RC 75 si occupé, source instable différée (RC extracteur 3 / pipeline 32) sans faux marquage traité par le watcher, `--run-id` propagé jusqu'au résultat AUDIT, compatibilité avec les déclenchements legacy préservée. Non déployé, non validé terrain. |
| 4 — admission NAS minimale | **Livré, mergé, testé ; preuve du lot fournie terrain (2026-09-09)** | `admission/bin/admission_core.py` mergé : ledger persistant, verrou ledger court, fail-closed si ledger indisponible/corrompu, validation des demandes, opérations V1 (`AUDIT`/`RELEASE_DIFF`), `request_id` durable et identité immuable (`operation`/`ts`/`expires_at`/`source`), verdicts `rejected_precondition`/`rejected_stale`/`rejected_conflict`/`admission_unavailable`/`rejected_busy`, `run_id` UUID4 avec mapping durable request_id→run_id, persistance `admitted` avant wrapper, déduplication durable (aucune réexécution d'un `request_id` connu, replay terminal), réconciliation des `admitted`, terminaison `completed`/`technical_failure`, handoff du vrai verrou métier via fd dynamique hérité (conservé jusqu'à la fin réelle des descendants), validation fail-closed du fd reçu par les wrappers, compatibilité legacy préservée, concurrence même process et multi-process testée en dépôt. **Preuve du lot** (« commande MQTT manuelle → run_id corrélé → résultat identique à un déclenchement DSM ») **fournie terrain** pour `AUDIT` et `RELEASE_DIFF`, via listener MQTT NAS opérationnel (identité `nas_admission`) — voir §12.2. La commande reste **manuelle** (backend Arsenal d'émission, Lot 5, non livré) : la preuve porte sur l'admission/exécution NAS, pas sur une émission Arsenal réelle. |
| 5 — backend Arsenal (émission) | **Livré, déployé, validé terrain, pilote `AUDIT` seul (2026-09-09)** | Génération côté Arsenal des enveloppes `request_id`/`ts`/`expires_at`/`source`, publication MQTT `arsenal/nas/admission/command` (QoS 1, `retain=false`), attente et corrélation du résultat transactionnel, diagnostic AUDIT dédié : livrés en configuration Home Assistant (voir §12.3) et **exécutés en conditions réelles sur Home Assistant 2026.9.1** (voir §12.4, puis rejoué avec le listener permanent au §12.5) — `request_id`/`run_id` corrélés, `completed`/`wrapper_rc=0`, ancrage nettoyé, exécution unique, aucune reconnexion MQTT, résultat métier `ok` observé séparément. `RELEASE_DIFF` explicitement hors périmètre de ce lot. Preuve du lot (« appel de test hors UI ») **fournie**. |
| 6 — extension seconde opération | **Livré, déployé, validé terrain (2026-09-09)** | Helper d'ancrage, script exécutif et diagnostic dédiés à `RELEASE_DIFF`, prolongeant strictement le patron du Lot 5 sans le modifier — livrés en configuration Home Assistant (voir §12.6) puis **exécutés en conditions réelles** sur le clone runtime `/config` (voir §12.7) — `request_id`/`run_id` corrélés, `completed`/`wrapper_rc=0`, admission ≈ 1 s après `ts`, durée totale ≈ 3 min 23 s, ancrage nettoyé, exécution unique, aucune reconnexion MQTT, résultat métier `ok` observé séparément. AUDIT (Lot 5) inchangé (diff nul, vérifié). Preuve du lot (« idem lot 4 ») **fournie**. |
| 7 — UI Lovelace | **Livré (code), non déployé, non testé terrain (2026-09-09) ; emplacement corrigé (2026-09-10)** | Demande AUDIT/RELEASE_DIFF, état transactionnel, résultat métier — voir §12.8. **Repositionnée le 2026-09-10** de `18_lovelace/dashboards/systeme/nas.yaml` vers `18_lovelace/dashboards/systeme/principal.yaml` (dashboard Système) — voir §12.9. Aucun usage réel prouvé. |
| 8 — décommissionnement DSM | Non commencé | Aucun retrait ni rationalisation des anciens déclenchements DSM. |
| 9 — clôture documentaire | Non applicable | Chantier ouvert — aucune clôture. |

**Hébergement/supervision permanent du listener NAS — désormais livré et
validé terrain (2026-09-09)**, voir §12.5 : tâche planifiée DSM Task
Scheduler (watchdog toutes les 5 minutes), cycle no-op sans doublon, arrêt
contrôlé et réactivation prouvés, relance automatique après disparition
simulée en 4 min 46 s, instance unique laissée active. Ce point n'est donc
plus à recenser dans la liste « Non livré » qui suit.

Non livré, à ne pas confondre avec ce qui précède (rappel exhaustif) : ACL
broker par topic (dette C52, acceptée pour la V1 — voir §12.2/§13) ; usage
réel de l'UI de commande NAS (Lot 7, **livré en code, non déployé, non
testé terrain** — voir §12.8) ; déploiement du noyau d'admission validé
comme remplacement définitif des tâches DSM legacy (§9) ; preuves terrain de
replay, de `BUSY` même-opération et de crash-reprise ; retrait ou
rationalisation des anciens déclenchements DSM ; clôture C51.

---

### 12.2 Preuves terrain NAS (2026-09-09)

Invariants utiles démontrés par la campagne terrain bout-en-bout ; le détail
complet des campagnes (commandes, timestamps) n'est pas recopié ici.

- **AUDIT** validé terrain bout-en-bout : admission OK, `run_id` propagé,
  pipeline RC0, verdict métier OK, résultat transactionnel MQTT reçu.
- **RELEASE_DIFF** validé terrain bout-en-bout : admission OK, `run_id`
  propagé, wrapper RC0, résultat métier `status=ok`, résultat
  transactionnel MQTT reçu.
- Corrélation `request_id`↔`run_id` validée ; unicité validée ; locks
  métier libérés correctement.
- Listener MQTT NAS corrigé pour ne plus bloquer la boucle réseau Paho.
- **Concurrence inter-opérations validée** : `RELEASE_DIFF` a été admis
  alors qu'`AUDIT` était encore en cours, avec 36 secondes d'avance sur la
  terminaison de l'AUDIT — aucune reconnexion MQTT observée pendant cette
  preuve, aucun `rejected_busy` entre `AUDIT` et `RELEASE_DIFF`, conforme à
  la politique du §8/contrat §11 (pas de verrou global entre opérations
  distinctes). La concurrence **même-opération** reste arbitrée par
  `admission_core` — non retestée par cette preuve.
- Identité MQTT dédiée `nas_admission` réellement utilisée pour le canal
  de commande.
- Publication du résultat **non bloquante** côté listener : la preuve
  fonctionnelle repose sur la **réception effective** du résultat MQTT par
  un observateur externe, pas sur un PUBACK synchrone — cette preuve
  n'introduit **aucune** nouvelle garantie de PUBACK synchrone.
- Absence d'ACL topic active sur le broker (constat §10) **acceptée pour
  la V1** de ce chantier ; dette maintenue et suivie par **C52** (non
  ouvert par ce lot).

Non couvert par cette campagne, à ne pas déduire de ce qui précède : replay
QoS 1, rejet `BUSY` même-opération, crash-reprise, backend Arsenal
d'émission, UI.

---

### 12.3 Lot 5 — backend Arsenal, pilote AUDIT (2026-09-09)

Premier lot runtime livré côté dépôt `arsenal` (configuration Home
Assistant). Périmètre volontairement restreint à l'opération `AUDIT` seule
— « premier lot pilote » : `RELEASE_DIFF` reste un vocabulaire fermé jamais
émis par ce lot (§5, §14 — aucune extension du vocabulaire).

**Livré, déployé, validé terrain (2026-09-09) — voir §12.4 pour la preuve :**

- `script.nas_admission_demander_audit` — frontière d'émission locale
  couvrant, dans l'ordre : precheck de l'ancrage transactionnel, génération
  d'un `request_id` unique, ancrage dans
  `input_text.nas_admission_req_audit` (helper dédié à `AUDIT`,
  §11.A4), vérification post-écriture, construction `ts`/`expires_at`
  (fraîcheur d'admission, 60 s)/`source`, `mqtt.publish` QoS 1
  `retain=false` sur `arsenal/nas/admission/command` (contrat §13.1/§13.2),
  attente d'un résultat transactionnel **terminal** corrélé sur
  `request_id` **et** `operation == "AUDIT"` (timeout local HA de 15
  minutes, distinct d'un verdict NAS), puis nettoyage systématique de
  l'ancrage — y compris sur timeout.
- `sensor.nas_admission_result_raw` — transport passif du plan résultat
  partagé `arsenal/nas/admission/result` (§13.1 : point d'admission unique,
  aucun topic par opération).
- Capteurs de corrélation `sensor.nas_admission_result_request_id`,
  `_operation`, `_run_id`, `_transaction_verdict` — extraction pure du
  payload, sans filtre par opération (le canal reste partagé).
- `sensor.nas_admission_audit_etat_transaction` — couche diagnostic qui,
  elle, filtre sur `operation == "AUDIT"` et latche le dernier verdict
  `AUDIT` connu (`this.state`), pour ne jamais afficher, comme état AUDIT,
  un verdict appartenant à une transaction `RELEASE_DIFF` observée sur le
  même canal partagé.

**Invariants du contrat respectés par construction :** séparation
transaction/résultat métier (§12 — ce lot ne lit ni n'expose jamais
`sensor.arsenal_self_audit_statut` depuis sa propre logique de conclusion) ;
`admitted` jamais traité comme terminal (§10.2) ; aucun paramètre métier
libre transmis ; aucun ID d'automatisation HA inventé (§14) ; aucune fusion
AUDIT/RELEASE_DIFF.

**Fourni par la preuve terrain du 2026-09-09 :** la preuve du Lot 5
(« appel de test hors UI », §12) — voir le détail complet au §12.4.

**Non fourni par ce lot, ni par sa preuve terrain :** hébergement/supervision
permanent du listener NAS (utilisé manuellement pour cette preuve précise,
puis arrêté — voir §12.4 ; livré séparément depuis, voir §12.5) ; automation
planifiée émettrice ; UI ; `RELEASE_DIFF` (Lot 6, non commencé) ; preuve de
`BUSY`/replay/crash-reprise au niveau du Lot 5.

---

### 12.4 Preuve terrain Lot 5 — pilote AUDIT (2026-09-09)

Preuve du lot 5 (§12, colonne « Preuve » : « appel de test hors UI »),
obtenue sur Home Assistant 2026.9.1.

- Backend réellement appelé : `script.nas_admission_demander_audit`.
- `request_id` : `9f88dea3-081e-498c-9fee-22342f99831a`.
- `run_id` : `47f834bc-a193-4411-9716-0e0c35c04018`.
- `operation` : `AUDIT` ; `source` : `arsenal`.
- `ts` : `2026-09-09T20:49:56Z` ; `expires_at` : `2026-09-09T20:50:56Z`.
- Terminaison transactionnelle : `completed` ; `wrapper_rc` : `0` ; durée
  ≈ 33 s.
- Corrélation `request_id` HA↔NAS : OUI. Corrélation `run_id` NAS↔HA : OUI.
- Résultat transactionnel MQTT reçu par HA : OUI.
- Ancrage (`input_text.nas_admission_req_audit`) nettoyé après réception :
  OUI.
- Une seule exécution `AUDIT` déclenchée par cette preuve : OUI (aucune
  duplication).
- Aucune reconnexion MQTT observée pendant la preuve : OUI.
- **Séparation transaction/résultat métier respectée.** Le verdict
  transactionnel `completed` (contrat §10.2) n'a, à aucun moment de cette
  preuve, été interprété comme un résultat métier favorable. Le résultat
  métier a été observé **séparément**, sur `sensor.arsenal_self_audit_statut`
  : verdict `ok`, 0 anomalie. `transaction_verdict=completed` ne signifie
  jamais `audit métier=ok` — les deux plans restent, dans cette preuve comme
  dans le contrat, disjoints.
- Listener MQTT NAS utilisé pour cette preuve : lancé **manuellement, au
  premier plan**, puis arrêté proprement une fois la preuve obtenue. Ce
  n'est **pas** un déploiement en supervision permanente.

**Non livré par cette preuve, à ne pas déduire de ce qui précède :**
hébergement/supervision permanent du listener NAS pour **cette** preuve
précise (démon/service ad hoc non utilisé ici — livré séparément le même
jour par tâche planifiée DSM, voir §12.5) ; `RELEASE_DIFF` via le backend
Arsenal (Lot 6, non commencé) ; UI Lovelace (Lot 7, non commencé) ; preuve
de `BUSY`/replay/crash-reprise au niveau du Lot 5 ; automation planifiée
émettrice.

---

### 12.5 Supervision permanente du listener MQTT NAS — preuve terrain (2026-09-09)

Preuve terrain distincte de celle du Lot 5 (§12.4) : elle porte sur le mode
d'hébergement et de supervision du listener MQTT NAS lui-même, jusqu'ici
non livré (§12.1, §12.3, §12.4, §13 avant cette preuve).

**Architecture déployée :**

- Tâche DSM Task Scheduler → toutes les 5 minutes (00:00–23:55) →
  `admission/bin/mqtt_listener_watchdog.sh` → `admission/bin/mqtt_listener.py`.
- Dépôt NAS canonique : `/volume1/Backups_HA/ha_backup_timeline`.
- Tâche DSM créée : `Arsenal - MQTT Listener Watchdog (C51)`, utilisateur
  `antoinevalentin`, fréquence 5 minutes.
- Aucun secret inline dans la tâche DSM ; listener lancé depuis le chemin
  canonique.

**Invariants démontrés :**

- Cycle no-op du watchdog : second cycle observé avec RC0, même PID que le
  cycle précédent, aucun doublon de processus.
- Verrou fd du listener non hérité par un éventuel processus enfant.
- Arrêt contrôlé : `--stop` validé terrain après désactivation de la tâche
  DSM.
- Réactivation : un nouveau listener a été relancé correctement après
  réactivation de la tâche.
- Résilience à une disparition simulée du listener : relance automatique
  observée en 4 min 46 s (< 5 min, conforme à la fréquence du watchdog).
- Listener laissé actif en fin de preuve (mode permanent, pas d'arrêt de
  clôture) ; une seule instance en tout temps.
- Connexion au broker MQTT établie, abonnement à
  `arsenal/nas/admission/command` effectif, aucun secret dupliqué.

**Preuve AUDIT rejouée avec ce listener permanent :**

- `request_id` : `0de32d59-262a-49bf-9d88-2f2214f1a5f4`.
- `run_id` : `02a3d516-883f-40ff-a19a-708e48081033`.
- `operation` : `AUDIT` ; terminaison transactionnelle : `completed` ;
  `wrapper_rc` : `0`.
- Corrélation `request_id` HA↔NAS : OUI. Corrélation `run_id` NAS↔HA : OUI.
- Ancrage transactionnel nettoyé : OUI. Une seule exécution : OUI. Aucune
  reconnexion MQTT observée pendant la transaction : OUI.
- **Résultat métier observé séparément** (jamais déduit du verdict
  transactionnel, conformément à l'invariant central du contrat §12) :
  verdict `ok`, 0 anomalie, 539 observations patrimoniales.
  `transaction_verdict=completed` ne signifie ici, comme ailleurs dans ce
  chantier, jamais `audit métier=ok`.

**Dette d'observabilité mineure, non bloquante.** Le fichier
`runtime/mqtt_listener.log` reste bufferisé tant que le processus tourne
(écriture différée, pas de flush en continu). Ceci ne bloque aucune des
preuves ci-dessus ni le fonctionnement transactionnel : c'est une limite de
confort de lecture du log en direct, consignée ici à titre de dette mineure
d'observabilité, sans chantier ni correctif ouverts par la présente preuve.

**Ce que cette preuve livre :** l'hébergement/supervision permanent du
listener MQTT NAS, jusqu'ici seul point non livré du volet NAS (§12.1,
§12.3, §12.4), est désormais **livré et validé terrain**. Le mécanisme de
supervision retenu est la tâche planifiée DSM ci-dessus — cf. §13, item
Docker/supervision alternative, désormais résolu par ce choix.

**Non livré par cette preuve, à ne pas déduire de ce qui précède :**
`RELEASE_DIFF` via le backend Arsenal (Lot 6, non commencé) ; UI Lovelace
(Lot 7, non commencé) ; preuve de `BUSY`/replay/crash-reprise au niveau du
Lot 5 ; ACL broker par topic (dette C52, inchangée) ; retrait ou
rationalisation des anciens déclenchements DSM legacy (§9) ; clôture C51.

---

### 12.6 Lot 6 — backend Arsenal, extension RELEASE_DIFF (2026-09-09)

Second lot runtime livré côté dépôt `arsenal` (configuration Home
Assistant), prolongeant le Lot 5 (§12.3) à la seconde opération du
vocabulaire fermé (§5). Périmètre : `RELEASE_DIFF` uniquement — AUDIT
(Lot 5) n'est pas modifié par ce lot.

**Livré (code, configuration Home Assistant), puis déployé et validé
terrain — voir §12.7 :**

- `script.nas_admission_demander_release_diff` — frontière d'émission
  locale couvrant, dans le même ordre que le Lot 5 : precheck de l'ancrage
  transactionnel **dédié** `input_text.nas_admission_req_release_diff`
  (jamais partagé avec le helper AUDIT), génération d'un `request_id`
  unique, ancrage, vérification post-écriture, construction
  `ts`/`expires_at`/`source`, `mqtt.publish` QoS 1 `retain=false` sur le
  topic **commun** `arsenal/nas/admission/command` (contrat §13.1/§13.2),
  attente d'un résultat transactionnel **terminal** corrélé sur
  `request_id` **et** `operation == "RELEASE_DIFF"` (timeout local HA de
  15 minutes, identique à AUDIT — voir justification ci-dessous), puis
  nettoyage systématique de l'ancrage, y compris sur timeout.
- `input_text.nas_admission_req_release_diff` — helper dédié, fichier
  distinct du helper AUDIT (`request_id_transactionnels.yaml`), pour
  garantir qu'une transaction AUDIT en vol ne bloque jamais localement
  RELEASE_DIFF et réciproquement (aucun verrou/état HA partagé — cohérent
  avec l'absence de verrou global déjà actée §8/contrat §11, et avec la
  concurrence inter-opérations déjà validée terrain côté NAS, §12.2).
- `sensor.nas_admission_release_diff_etat_transaction` — diagnostic
  filtré sur `operation == "RELEASE_DIFF"` et latché (`this.state`),
  strictement symétrique du diagnostic AUDIT du Lot 5, sans réutiliser ni
  modifier son fichier.
- `sensor.nas_admission_result_raw` et les capteurs de corrélation
  (`request_id`/`operation`/`run_id`/`transaction_verdict`) —
  **réutilisés tels quels** (contrat §13.1 : point d'admission unique,
  canal partagé) ; seule une ligne de commentaire d'en-tête corrigée dans
  chacun (mention obsolète d'un unique consommateur AUDIT).

**Fenêtres temporelles — audit préalable et justification (pas une copie
non questionnée).** `diff_release.md` et `release_diff_mqtt.md` ne
chiffrent aucune durée d'exécution nominale pour `release_diff.py`
(job « à la demande », sans heartbeat ni fraîcheur contractualisée) ; le
coût dépend du nombre de couples non idempotents à retraiter, borné par
aucun contrat. Le seul point de mesure terrain disponible (§12.2 : preuve
de concurrence inter-opérations, 2026-09-09) montre RELEASE_DIFF achevant
sa transaction 36 secondes **avant** la terminaison d'AUDIT — dont la
propre preuve mesure ≈ 33 s (§12.4) — sur un run n'ayant vraisemblablement
traité aucun couple nouveau (idempotence quotidienne). Sur cette seule
base, RELEASE_DIFF n'apparaît pas plus lent qu'AUDIT ; mais aucune mesure
terrain n'existe pour un backlog de plusieurs couples non idempotents. En
l'absence de preuve terrain Lot 6 dédiée, `expires_at` (60 s — fenêtre de
fraîcheur d'admission, indépendante de la durée d'exécution, contrat §6)
et le timeout local HA (15 minutes — fenêtre purement locale, non
opposable au NAS) retiennent **prudemment** les mêmes valeurs qu'AUDIT
plutôt qu'une valeur plus courte non justifiée par la seule mesure
ponctuelle disponible. Détail complet consigné dans l'en-tête du script.

**Invariants du contrat respectés par construction :** séparation
transaction/résultat métier (§12 — ce lot ne lit ni n'expose jamais
`sensor.arsenal_nas_release_diff_statut` depuis sa propre logique de
conclusion) ; `admitted` jamais traité comme terminal (§10.2) ; aucun
paramètre métier libre transmis (`--couple` et tout autre paramètre batch
explicitement absents, §2.2/§7 chantier) ; aucun ID d'automatisation HA
inventé (§14) ; aucune fusion AUDIT/RELEASE_DIFF ; aucun verrou local
partagé entre les deux opérations.

**Vérification statique.** `scripts/arsenal_contracts/verify_nas_admission_transactionnel_lot6.py`
(14 tests couvrant : vocabulaire d'opération figé, topic/QoS/retain,
`source` fixe, absence de paramètre métier libre, helpers dédiés et
distincts, cleanup systématique, corrélation `request_id`+`operation`,
`admitted` non terminal, vocabulaire terminal complet, non-lecture du
résultat métier pour conclure, diagnostics filtrés/latchés sans
écrasement croisé, couche partagée non filtrée par opération, absence de
couplage AUDIT↔RELEASE_DIFF) — vert sur l'état livré ; preuve négative
effectuée (mutation d'`operation` injectée puis retirée, détectée par le
test T2). **Non câblé** à `contracts_all.yml`/`check_ci_coverage_registry.py`
(§11.A7) : câblage laissé en suite explicite, hors périmètre strict de ce
lot.

**Non fourni par ce lot lui-même** (code) — fourni séparément par la preuve
terrain du §12.7 : déploiement sur Home Assistant ; appel de test hors UI ;
preuve terrain de corrélation `request_id`/`run_id` pour RELEASE_DIFF au
niveau **Arsenal**. **Toujours non fourni après le §12.7** : preuve de
`BUSY`/replay/crash-reprise au niveau du Lot 6 ; câblage CI du vérificateur
statique dans le registre de couverture ; UI Lovelace (Lot 7, non commencé).

---

### 12.7 Preuve terrain Lot 6 — extension RELEASE_DIFF (2026-09-09)

Preuve du lot 6 (§12, colonne « Preuve » : « idem lot 4 »), obtenue sur le
clone runtime **réellement exécuté par Home Assistant** (`/config`).

**Point de clone.** Un premier fast-forward avait été effectué sur le clone
Windows `C:\dev\arsenal` ; ce clone n'est **pas** celui exécuté par Home
Assistant et ne vaut donc aucune preuve terrain à lui seul. Le clone runtime
réel est `/config` : ancien HEAD `c01fdcd4`, nouveau HEAD `4e0059d1`,
fast-forward propre jusqu'au merge de la PR #817, dépôt runtime final propre
et à jour. Entités chargées : `input_text.nas_admission_req_release_diff`,
`script.nas_admission_demander_release_diff`,
`sensor.nas_admission_release_diff_etat_transaction`. Pré-état métier avant
preuve : `sensor.arsenal_nas_release_diff_statut` = `ok`, dernière exécution
`2026-09-09T18:40:52+00:00`.

**Demande RELEASE_DIFF.**

- `request_id` : `c49d02fa-1588-46e7-8e4f-27d9a26cf416`.
- `ts` : `2026-09-09T22:59:18Z` ; `expires_at` : `2026-09-09T23:00:18Z`.
- `operation` : `RELEASE_DIFF`.

**Admission NAS.**

- `run_id` : `c70c093f-fd37-4889-902e-2ff4310c13bf`.
- `received_at` : `2026-09-09T22:59:19Z` — admission reçue environ 1 seconde
  après `ts`, à l'intérieur de la fenêtre de fraîcheur d'admission (marge
  restante avant `expires_at` de l'ordre de 59 secondes).

**Terminaison transactionnelle.**

- `transaction_verdict` : `completed` ; `wrapper_rc` : `0`.
- `terminal_at` : `2026-09-09T23:02:41Z` — durée totale `ts`→terminal
  ≈ 3 min 23 s.
- **Point conceptuel opposable, déjà fixé au contrat (§6, §9.5) :**
  `expires_at` borne l'**admission** de la demande, pas la durée totale
  d'une exécution déjà admise. Cette preuve terrain illustre précisément
  cette distinction : l'admission a eu lieu dans la fenêtre contractuelle,
  et l'exécution s'est poursuivie au-delà de `expires_at` sans que cela
  constitue une anomalie — l'expression « admission en 59 s » serait une
  formulation incorrecte à ne pas reprendre, la marge de 59 s étant celle
  qui restait avant `expires_at` au moment de l'admission, pas une durée
  d'exécution.

**Corrélation.**

- `request_id` identique HA/NAS : OUI. `run_id` identique NAS/HA : OUI.
- `operation` : `RELEASE_DIFF`. Une seule admission, une seule exécution.
- Diagnostic transactionnel final : `completed`. Helper RELEASE_DIFF
  (`input_text.nas_admission_req_release_diff`) nettoyé après réception :
  OUI.

**Résultat métier — observé séparément, jamais déduit du verdict
transactionnel (invariant central du contrat §12).**

- `sensor.arsenal_nas_release_diff_derniere_execution` =
  `2026-09-09T23:02:35+00:00`.
- `sensor.arsenal_nas_release_diff_statut` = `ok`.
- `transaction_verdict=completed` ne signifie, ici comme ailleurs dans ce
  chantier, jamais `RELEASE_DIFF métier=ok` : les deux faits ont été
  observés séparément.

**Listener MQTT NAS permanent.** PID identique avant/après la transaction
(`25708`) ; aucune reconnexion MQTT observée pendant la transaction ; un
seul processus `mqtt_listener.py` en tout temps — supervision permanente
(§12.5) confirmée stable sous cette seconde opération.

**Ce que cette preuve livre :** le Lot 6 (extension `RELEASE_DIFF` du
backend Arsenal), jusqu'ici livré en code seul (§12.6), est désormais
**déployé et validé terrain**, sur le clone runtime réellement exécuté par
Home Assistant.

**Non livré par cette preuve, à ne pas déduire de ce qui précède :** UI
Lovelace (Lot 7, non commencé à cette date) ; preuves de `BUSY`
même-opération et de crash-reprise au niveau du Lot 6 ; câblage CI du
vérificateur statique dans le registre de couverture ; dette ACL C52
(inchangée) ; clôture C51.

---

### 12.8 Lot 7 — UI Lovelace (2026-09-09)

Troisième lot runtime livré côté dépôt `arsenal`, portant exclusivement sur
l'interface Lovelace — aucun backend touché (Lots 5/6, §12.3/§12.6,
strictement inchangés ; diff nul vérifié sur `10_scripts/system/nas_admission_*`,
`12_template_sensors/system/nas_admission/**`,
`04_input_texts/system/nas_admission/**`).

**Audit préalable (§4/§14 chantier, §12 contrat — dérivation documentaire
obligatoire).** Avant toute écriture, consultation de la documentation UI
existante — [`ui/pattern_dashboard.md`](../../../ui/pattern_dashboard.md)
(structure canonique, géométrie des grilles `R-LL-GRID-1`/`R-LL-GRID-2`),
[`ui/socle_ui/02_action.md`](../../../ui/socle_ui/02_action.md) (socle
`socle_action_script_confirme` — confirmation modale obligatoire, seul
socle Action à l'embarquer nativement),
[`ui/socle_ui/07_status.md`](../../../ui/socle_ui/07_status.md)/`09_diagnostic.md`,
[`ui/couleurs/`](../../../ui/couleurs/README.md) (palette contractuelle,
traitement `unknown`/`unavailable`) — et de l'UI déjà instanciée :
`18_lovelace/dashboards/systeme/nas.yaml` (section « Commandes système »
existante, patron de confirmation déjà en usage pour des actions NAS),
`19_button_card_templates/40_dashboards/system/20_supervision/arsenal_self_audit_status_card.yaml`
(carte de résultat métier AUDIT déjà livrée au Lot 5, jamais consommée
jusqu'ici par aucun dashboard NAS),
`19_button_card_templates/10_generiques/action/carte_action_standard.yaml`
et `19_button_card_templates/40_dashboards/arrosage/10_action/carte_action_arrosage_script.yaml`
(patron « demander un script, confirmation obligatoire »). Aucune
convention n'a été inventée hors de ces sources : la confirmation modale
sur les deux boutons de demande reproduit un patron **omniprésent** dans le
dépôt pour tout déclenchement de script (arrosage, vacances, bonne nuit,
etc.), jamais un réflexe de ce chantier.

**Emplacement retenu (2026-09-09) — corrigé le 2026-09-10, voir §12.9.**
`18_lovelace/dashboards/systeme/nas.yaml` — le
dashboard NAS existant, seul point déjà navigable pour toute commande NAS
(section « Commandes système » y existe déjà pour redémarrage/extinction).
`arsenal_nas` et `arsenal_self` sont des contrats système/transverses
**sans hub de domaine dédié** (`navigation/carte_domaines.md` §3/§6) : aucune
nouvelle page ni aucun nouveau dashboard n'a donc été créé — un ajout de
section à une page existante satisfait strictement « enrichir une page
existante plutôt qu'en créer une nouvelle » (consigne d'audit préalable).

> **Correction (2026-09-10).** Cette lecture est **rejetée par arbitrage
> Direction** : l'absence de hub de domaine dédié ne fait pas du NAS le
> domaine fonctionnel d'accueil de `AUDIT`/`RELEASE_DIFF` — elle signifie
> seulement qu'aucune page dédiée n'existe pour `arsenal_self`/`arsenal_nas`,
> ce qui reste également compatible avec un ajout de section au dashboard
> **Système** (`principal.yaml`). Le sens fonctionnel de ces deux opérations
> est un service rendu à Arsenal, le NAS n'en étant que l'exécutant
> technique externe (§4 « Matrice des autorités »). Voir §12.9 pour
> l'emplacement corrigé et son fondement documentaire.

**Livré :**

- Deux boutons de demande (`carte_action_nas_admission_demander`, satellite
  de `socle_action_script_confirme`) : `script.nas_admission_demander_audit`
  et `script.nas_admission_demander_release_diff`, chacun avec confirmation
  modale dédiée. Chaque bouton appelle exclusivement `script.turn_on` sur
  le script backend désigné — aucun payload MQTT construit ici, aucun
  `request_id`, aucune donnée métier libre (chantier §4 : « Backend Arsenal
  décide, UI Lovelace rend »).
- Deux cartes de diagnostic transactionnel
  (`carte_nas_admission_etat_transaction`, satellite de
  `socle_status_label`) : lisent respectivement
  `sensor.nas_admission_audit_etat_transaction` et
  `sensor.nas_admission_release_diff_etat_transaction`. Le vocabulaire
  transactionnel fermé (`admitted`/`completed`/`technical_failure`, famille
  rejet, `sans_donnee`) y est traduit sans jamais assimiler `completed` à
  un succès métier : `admitted`/`completed` sont rendus dans la même
  couleur bleue (« information/technique », `02_palette.md`), jamais en
  vert (réservé à un état métier favorable) ; le label renvoie
  explicitement vers l'entité de résultat métier séparée.
- Deux cartes de résultat métier, strictement disjointes des précédentes :
  réutilisation de `arsenal_self_audit_status_card` (déjà livrée au Lot 5)
  pour AUDIT, et nouvelle `arsenal_nas_release_diff_status_card` (satellite
  direct du même socle) pour RELEASE_DIFF — construite sur les seules
  entités déclarées par `arsenal_nas.md` §5.1 (`ok`/`partial`/`error`),
  sans inventer de binary_sensor de fraîcheur/erreur que ce contrat
  déclare explicitement absent en V1 (`arsenal_nas.md` §5.3).

**Invariants respectés par construction :** aucune publication MQTT depuis
Lovelace ; aucune reconstruction de payload ; aucun `request_id` généré
côté UI ; aucun paramètre métier libre exposé ; aucune gestion du `BUSY`
dans la carte (le NAS reste seul autorité, §4/§7 contrat) ; AUDIT et
RELEASE_DIFF restent deux instances distinctes des mêmes templates
génériques, jamais fusionnées (§14 chantier) ; aucun ID d'automatisation
inventé ; aucune automation créée ; aucun contrat NAS modifié ; aucun
fichier backend des Lots 5/6 touché.

**Non fourni par ce lot :** déploiement sur Home Assistant ; usage réel
(clic effectif sur les deux boutons, observation du rendu terrain des
couleurs et labels) ; preuve de `BUSY`/replay/crash-reprise au niveau de
l'UI ; dette ACL C52 (inchangée) ; clôture C51 — les critères du §15
restent partiellement ouverts tant que la preuve terrain de ce lot n'est
pas fournie.

---

### 12.9 Correction Lot 7 — repositionnement fonctionnel de l'UI (2026-09-10)

**Constat.** L'emplacement retenu au Lot 7 (§12.8) —
`18_lovelace/dashboards/systeme/nas.yaml` — reposait sur une lecture
erronée de `navigation/carte_domaines.md` §3/§6 : l'absence de hub de
domaine dédié pour `arsenal_self`/`arsenal_nas` (« contrats
système/transverses ... pas de hub de domaine ») a été interprétée comme
une invitation à héberger l'UI dans le seul dashboard NAS déjà navigable,
au lieu d'être lue comme ce qu'elle dit réellement : `arsenal_self` et
`arsenal_nas` sont des domaines **système/transverses Arsenal**, pas des
domaines NAS.

**Arbitrage.** Le sens fonctionnel de `AUDIT` et `RELEASE_DIFF` est un
service rendu à Arsenal : la commande part d'Arsenal, transite par MQTT,
est exécutée par le NAS (exécutant technique externe, jamais autorité de
décision — §4 « Matrice des autorités »), et le résultat revient nourrir
un diagnostic Arsenal déjà existant (`arsenal_self_audit_status_card`,
présent dans le dashboard Système avant même ce chantier) ou une
notification Arsenal (`arsenal_nas`, §1/§2 de son contrat). La
justification « pas de hub documentaire ⇒ dashboard NAS » est **rejetée** :
l'absence de hub ne désigne aucun domaine d'accueil par défaut — elle
signifie seulement qu'aucune page dédiée n'existe, ce qui est compatible
avec un ajout de section à une page **système** existante
(`principal.yaml`) tout autant qu'à une page NAS.

**Emplacement retenu.** `18_lovelace/dashboards/systeme/principal.yaml`
(dashboard Système) — dérivé de `contrats/arsenal_self.md` §1 (« le
dashboard système » y est explicitement cité comme consommateur de
l'auto-supervision Arsenal) et de la présence déjà établie, avant ce
chantier, de `arsenal_self_audit_status_card` à cet endroit précis. Aucune
nouvelle page créée. La carte de résultat métier AUDIT déjà présente
(`arsenal_self_audit_status_card`) n'est ni déplacée ni réécrite ; la
nouvelle section de commande/transaction est insérée en cohérence avec
elle, immédiatement avant.

**Retiré de `nas.yaml` :** la section « 🗂️ Commandabilité NAS (C51) »
entière (deux boutons de demande, deux cartes de diagnostic
transactionnel, deux cartes de résultat métier) ; aucune trace
fonctionnelle C51 n'y subsiste.

**Réutilisé sans modification de contenu :** les trois templates
satellites du Lot 7 (`carte_action_nas_admission_demander`,
`carte_nas_admission_etat_transaction`, `arsenal_nas_release_diff_status_card`)
— techniquement corrects, génériques AUDIT/RELEASE_DIFF, aucune
régression « backend décide / UI rend » introduite par leur
déplacement. `arsenal_nas_release_diff_status_card` vivait déjà dans
`40_dashboards/system/20_supervision/` depuis le Lot 7 (elle n'a jamais
été mal placée) — seul son usage dans un dashboard était absent ; elle
est désormais consommée par `principal.yaml`.

**Déplacés (fichiers de template, contenu inchangé) :**
`carte_action_nas_admission_demander.yaml` et
`carte_nas_admission_etat_transaction.yaml`, de `40_dashboards/nas/` vers
`40_dashboards/system/` — ces cartes ne qualifient jamais la santé du
NAS lui-même (ce que fait le reste de `nas/`), elles portent la demande
et la transaction d'une commande Arsenal exécutée par le NAS.

**Libellés adaptés (UI seule, aucune entité renommée) :** le titre de
section passe de « 🗂️ Commandabilité NAS (C51) » à « 🧠 Arsenal — Audit
& Release Diff (C51) » ; les confirmations de demande nomment l'audit/le
release diff Arsenal en premier, le NAS en second plan (exécutant),
plutôt que l'inverse. Aucune entité backend (`script.*`, `sensor.*`)
renommée — hors périmètre de cette correction.

**Invariants inchangés :** aucune publication MQTT depuis Lovelace ;
aucun `request_id` généré côté UI ; séparation transaction/résultat
métier strictement conservée (la carte de transaction ne lit jamais
l'entité de résultat métier pour se conclure — inchangé) ; AUDIT et
RELEASE_DIFF restent deux instances distinctes, jamais fusionnées (§14) ;
aucun backend Lots 5/6 touché (diff nul vérifié) ; aucune automation
créée ; aucun ID d'automatisation inventé.

**Non fourni par cette correction :** preuve d'usage réel terrain
(inchangé depuis §12.8 — C51 reste ouvert) ; preuves de
replay/`BUSY`/crash-reprise ; dette ACL C52 (inchangée) ; clôture C51.

---

### 12.10 Lot 8 — plan de bascule Arsenal/MQTT pour AUDIT et RELEASE_DIFF, sous-lots 8.1 à 8.6 (2026-09-10)

**Lot documentaire uniquement : ce lot ne modifie aucun runtime, aucun
script NAS, aucune configuration Home Assistant.** Il détaille, sans
l'exécuter, le séquencement arbitré par la décision produit du 2026-09-10
(voir la ligne `Mise à jour` du 2026-09-10 et le complément du §9) : faire
porter par Arsenal, via MQTT, l'initiative des deux opérations `AUDIT` et
`RELEASE_DIFF`, le NAS restant seul moteur d'exécution. Chantier existant
**C51** réutilisé tel quel ; aucun nouvel identifiant, aucun nouveau
chantier.

Le Lot 8 se décompose en six sous-lots, ordonnés, chacun conditionné à une
preuve terrain avant le retrait qu'il documente :

1. **8.1 — `AUDIT` : intégration de la garantie de stabilité.** Intégrer
   dans `run_pipeline.sh` la garantie de stabilité aujourd'hui portée par
   `watch_new_backup.sh` (double mesure de taille à 60 s d'intervalle,
   §6), **sans modifier encore `timeline_extract.lock`**. `watch_new_backup.sh`
   n'est pas retiré à ce sous-lot.
2. **8.2 — retrait de `Arsenal - Pipeline Watcher` et `Pipeline HA`.**
   Après preuve terrain que le nouveau chemin `AUDIT` (8.1) porte seul la
   garantie de stabilité, retirer les deux tâches DSM de déclenchement
   réactif/quotidien du pipeline `AUDIT` (§9, lignes 2 et 3 du tableau).
3. **8.3 — `RELEASE_DIFF` : autonomie par extraction à la demande.** Rendre
   `run_release_diff.sh` autonome en lui ajoutant l'extraction à la
   demande. Pendant la coexistence avec `Arsenal - Timeline Backups HA`
   (extraction périodique, 5 min), cette extraction à la demande utilise
   **impérativement** le même `timeline_extract.lock` que l'extraction
   périodique — aucun verrou distinct, aucune fenêtre de collision non
   couverte.
4. **8.4 — retrait de `Arsenal - Timeline Backups HA`.** Retrait
   uniquement après preuves terrain acquises **pour `AUDIT` (8.1/8.2) ET
   `RELEASE_DIFF` (8.3) autonomes** — les deux chemins doivent être
   prouvés avant ce retrait, pas l'un sans l'autre.
5. **8.5 — requalification de `timeline_extract.lock`.** Après retrait du
   dernier appelant DSM direct de l'extracteur (8.4), `timeline_extract.lock`
   cesse d'être le mécanisme normal de coordination entre extractions
   concurrentes et devient garde-fou / défense en profondeur. C'est à ce
   sous-lot que la règle `rc=77` bascule du régime transitoire (§9) au
   régime cible : une occurrence devient anormale.
6. **8.6 — retrait de `Arsenal - Release Diff` quotidien.** Retrait de la
   tâche DSM quotidienne après preuve terrain du chemin `RELEASE_DIFF` à
   la demande (8.3), dans les conditions déjà posées au §9 (verrou
   d'exclusion mutuelle RELEASE_DIFF, §2.10, et preuve terrain du chemin
   MQTT).

Le **Lot 9**, hors périmètre du présent document, suit le Lot 8 pour la
clôture documentaire du chantier.

**État de ce lot : globalement non commencé.** Aucun sous-lot 8.1 à 8.6
n'est livré à ce stade ; cette mise à jour documente le plan arbitré, elle
n'exécute aucun sous-lot. Voir aussi la ligne `Mise à jour` du 2026-09-10
et le complément du §9.

---

## 13. Vérifications encore nécessaires avant implémentation

*(ne bloquent pas la documentation — bloquent les lots 2+)*

- ACL MQTT réelles sur le broker — **vérifiées (2026-09-09)** : voir §10.
  Point de fait tranché ; **arbitrage rendu** : la dette — identité dédiée
  `nas_admission` sans cantonnement ACL par topic, avec les mesures de
  réduction du risque applicatif déjà présentes (vocabulaire fermé §5,
  validation `admit()`) — est **acceptée pour la V1** de ce chantier, sans
  bloquer l'activation terrain (§12.2). Dette maintenue et suivie par le
  chantier **C52** (non ouvert par ce lot). La migration ACL globale du
  broker reste hors périmètre C51 (cf. C52).
- ~~Accès Docker/Container Manager pour utilisateur non-root, ou mécanisme
  de supervision alternatif du futur listener.~~ **Résolu (2026-09-09)** :
  mécanisme de supervision alternatif retenu et validé terrain — tâche
  planifiée DSM Task Scheduler (watchdog toutes les 5 minutes), sans
  recours à Docker/Container Manager. Voir §12.5.
- Comportement réel de `ha_backup_timeline_extract_v2.py` sous collision
  effective (test à réaliser, pas seulement lecture de code).
- Périmètre exact de l'opération AUDIT via MQTT (§6, premier point).
- Validation du verrou RELEASE_DIFF sous double-exécution simulée réelle.

---

## 14. Interdictions opposables à tout lot futur de C51

- Aucun ID d'automatisation Home Assistant inventé par un lot de ce
  chantier.
- Aucune fusion des chaînes AUDIT et RELEASE_DIFF.
- Aucun verrou global AUDIT/RELEASE_DIFF sans invariant partagé
  nouvellement démontré.
- Aucune confusion entre transaction et résultat métier, y compris dans le
  nommage des champs d'un futur payload.
- Aucune activation d'une commande MQTT RELEASE_DIFF avant que le verrou
  d'exclusion mutuelle (Lot 2) soit livré et prouvé.
- Aucune suppression de tâche DSM sans preuve terrain que sa garantie est
  reprise ailleurs.
- Aucune activation terrain du canal de commande MQTT sans arbitrage
  Direction explicite sur la dette ACL constatée au §10.

---

## 15. Critères de clôture

1. Les quatre tâches DSM du §9 ont chacune une décision explicite
   (conservées, remplacées avec preuve, ou décommissionnées) — pas de
   statu quo non motivé.
2. Le contrat `nas_transactionnel.md` est implémenté et validé terrain pour
   les deux opérations.
3. Le verrou RELEASE_DIFF (Lot 2) et le durcissement AUDIT (Lot 3) sont
   livrés et prouvés.
4. Aucune interdiction du §14 n'a été violée sur l'ensemble des lots.
5. La documentation de catégorie C (§11.C) a été mise à jour au fil des
   lots runtime concernés, sans reste ouvert.

---

*Chantier ouvert le 2026-09-08. Source faisant foi pour la ligne C51 du
registre.*
