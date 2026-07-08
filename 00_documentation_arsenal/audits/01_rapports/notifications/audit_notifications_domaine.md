# 🔔 ARSENAL — AUDIT — Domaine transverse **Notifications**

> **Trace d'audit documentaire, lecture seule.** Aucune correction runtime dans cette passe : ni automation, ni template, ni script, ni Lovelace, ni contrat, ni checker modifiés.
> Principe : le runtime fait foi ; toute affirmation est tracée à une preuve du dépôt.
> Convention : **[FAIT]** observé dans le dépôt · **[HYP]** hypothèse dépendant d'un comportement HA non instrumenté ici · **[RECO]** recommandation.
> Source normative : [`../../../contrats/notifications.md`](../../../contrats/notifications.md). Vérification mécanique existante : `scripts/arsenal_contracts/check_notifications_contracts.py` (workflow `contracts_notifications.yml`).

---

## Verdict

Le domaine est **structurellement sain sur son canal d'émission, et partiellement non conforme sur le cycle de vie des notifications persistantes.**

Deux résultats dominants :

1. **[FAIT] Canal mobile : discipline intacte, gravité nulle.** Aucun sous-système n'appelle un service `notify.*` en dur : les **76 sites d'appel** (46 fichiers) passent tous par la couche d'abstraction centrale `script.notification_envoyer{,_famille,_avance}`. L'indirection promise par [`10_scripts/system/notifications_mobiles.yaml`](../../../../10_scripts/system/notifications_mobiles.yaml) est respectée à 100 %.

2. **[FAIT] Persistantes : l'invariant de recalculabilité après redémarrage est violé sur un sous-ensemble de notifications d'état.** Le contrat exige qu'une notification persistante soit **recréable à partir du seul état courant après un redémarrage complet** (§ « Test de recalculabilité forte », § « Robustesse & cohérence »). Or Home Assistant **ne restaure pas** les notifications `persistent_notification.create` au redémarrage : elles doivent donc être **recréées par une automatisation de démarrage**. Le dépôt possède l'idiome canonique pour cela — le trigger proxy `input_boolean.systeme_stable → on` — et l'applique correctement à plusieurs états (bouclage, clim, chauffage confort, vacances). Mais **plusieurs projections d'état ne l'utilisent pas**, dont deux à trou **structurellement garanti**.

**Gravité globale : P2** (conformité contractuelle + observabilité UI), avec **deux points P1** ciblés (présence, mode panne secteur). Aucune rupture fonctionnelle : les états métier et leurs automatisations restent corrects ; c'est leur **projection UI** qui disparaît silencieusement après un reboot. La sévérité est celle d'un **écart de conformité et d'observabilité**, pas d'un défaut de commande.

---

## 1. Périmètre & méthode

- **Périmètre :** `10_scripts/` + `11_automations/`, tous usages de `persistent_notification.create/dismiss` et de `script.notification_envoyer*`, croisés avec le contrat `notifications.md` et le checker.
- **Méthode :** inventaire mécanique (grep) → recensement par `notification_id` (create ↔ dismiss ↔ re-création boot) → lecture ciblée des cas porteurs → contrôle du comportement HA de restauration.
- **Compteurs [FAIT] :** `persistent_notification.create/dismiss` = **52 occurrences / 32 fichiers** ; `script.notification_envoyer*` = **76 occurrences / 46 fichiers** ; services `notify.*` en dur hors couche d'abstraction = **0**.

**Mécanique HA, socle de l'audit [FAIT].** Les notifications créées par `persistent_notification.create` vivent en mémoire (`hass.data`), **non persistées** dans `.storage`. Après un redémarrage, la liste est vide. Une notification persistante représentant un état durable **doit donc être recréée au démarrage** si l'état est encore vrai — sinon l'état est vrai mais sa notification est absente (**trou silencieux**). Arsenal a formalisé ce besoin via `input_boolean.systeme_stable → on` (posé par [`11_automations/system/stabilisation_post_demarrage.yaml`](../../../../11_automations/system/stabilisation_post_demarrage.yaml)), déjà utilisé comme signal de reconstruction post-boot dans le domaine chauffage et l'audit panne secteur.

---

## 2. Ce qui est sain (à préserver)

- **[FAIT] Abstraction du canal mobile.** `notification_envoyer` (cible dynamique), `_famille` (deux téléphones), `_avance` (data Android). Cibles résolues par `input_text.telephone_*_notify`, jamais de service notify codé en dur. Un changement de smartphone/app ne touche aucun YAML métier. **0 contournement constaté.**
- **[FAIT] Idiome de re-création au démarrage correctement appliqué.** Modèle de référence : [`11_automations/bouclage/notification.yaml`](../../../../11_automations/bouclage/notification.yaml) — trigger `switch.prise_bouclage` **+** `systeme_stable → on`, recalcul sans condition depuis l'état courant, `mode: restart`, paire create/dismiss propre. Même idiome sain sur `clim_mode_actif`, `clim_execution_echec` (chantier C13), `chauffage_mode_confort`, `contexte_vacances`/`projection_vacances`.
- **[FAIT] Couverture format du checker.** Emoji de tête (persistant **et** mobile), séparateur `–` vs `—`, verbes interdits en titre, fonctions temporelles dans le bloc create, unicité d'`id` sur seuil ≥ 4 fichiers : correctement testés (T1–T6).

---

## 3. Constats

Codes stables `NOTIF-xx`. La colonne « Nature » distingue **DUR** (trou structurellement garanti), **RACY** (re-création non garantie, dépend d'une course restore/chargement), **PROBABLE-OK** (auto-guérison probable via reconnexion d'intégration), **SÉMANTIQUE** (événement déguisé / unicité).

| Code | Notification(s) | Fichier | Écart | Nature | Prio |
|---|---|---|---|---|---|
| **NOTIF-01** | `presence_valentin`, `presence_constance` | `11_automations/presence/notification_presence.yaml` | Aucune re-création boot ; la branche `create` exige `trigger.from_state == 'not_home'`, impossible à satisfaire au restore → **jamais recréée**. **Aggravant** : l'entête revendique « 🔄 ROBUSTESSE RELOAD — Recalculable à partir du seul état courant ». | DUR | **P1** |
| **NOTIF-02** | `mode_panne_secteur` | create délégué : `10_scripts/system/coupure_secteur.yaml` ; entrée : `11_automations/panne/secteur/activation_mode_panne.yaml` | La création est **couplée à l'action d'entrée** gardée par idempotence (`panne_secteur_active == off`). Au reboot pendant une panne, l'état restauré `on` **fait échouer la garde** → l'entrée n'est pas rejouée → notif jamais recréée. Frappe précisément pendant une coupure réelle (HA secouru Bluetti/UPS). | DUR | **P1** |
| **NOTIF-03** | `mode_babysitting_actif`, `chauffage_pre_confort_vacances`, `lave_vaisselle_cycle`, `buanderie_cycle`, `alarme_etat` | `modes/babysitting/notification_persistante.yaml`, `chauffage/pre_confort_vacances/notification.yaml`, `electromenager/lave_vaisselle/debut.yaml`, `electromenager/buanderie/debut.yaml`, `alarme/notification.yaml` | Projections d'état sourcées sur un `input_boolean`/`alarm_control_panel` **persisté**, déclenchées sur transition **sans** trigger `systeme_stable`. Re-création au boot **non garantie** (course entre le restore et le chargement de l'automation) alors que l'idiome canonique existe et est utilisé ailleurs. | RACY | **P2** |
| **NOTIF-04** | `voiture_etat_charge`, `energie_chaudiere_bluetti` | `voiture/notification_etat_charge.yaml`, `panne/secteur/alerte_bluetti.yaml` | Même absence de trigger `systeme_stable`, **mais** source = entité d'intégration (`sensor`/`binary_sensor`) qui repasse `unavailable → valeur` à la reconnexion post-boot → la transition `to:` se rejoue **probablement** → auto-guérison probable, hors idiome canonique. | PROBABLE-OK | P3 |
| **NOTIF-05** | `panne_internet`, `vmc_non_conformite_decision` | `panne/internet/reconciliation_demarrage.yaml` (+ remediation), `vmc/alerte_nc_decision.yaml` | Re-création **partielle/différée** : la réconciliation internet ne fait que *dismiss* si l'accès est rétabli ; si la panne persiste au boot, reconstruction seulement via la détection nominale (`to:off for 5min`), retardée et couplée à une relance de campagne reboot box. VMC : re-création seulement si le capteur rejoue `to:off for 3min`. | RACY/partiel | P2 |
| **NOTIF-06** | *(sans `notification_id`)* saison, ECS verrou levé, simulation auto-ajustement | `system/saisons.yaml`, `ecs/reset_verrou_cycle.yaml`, `chauffage/courbe_de_chauffe/auto_ajustement.yaml` | **Événements déguisés en persistant** : messages décrivant une **transition/action passée** (« **X** a **Y** », « Verrou cycle **levé** … a été remis à OFF », « Ajustements **proposés** … Aucun changement n'a été appliqué »). De plus **aucun `notification_id`** → **non-dismissables** et **empilables** (viole § « Identité & unicité » et § « Interdiction de référence au passé »). | SÉMANTIQUE | P2 |

### Détails porteurs

**NOTIF-01 — présence (le constat le plus net).** [FAIT] La branche de création (`11_automations/presence/notification_presence.yaml:98-112`) est gardée par `trigger.from_state.state == 'not_home'`. Un redémarrage ne produit pas de transition *depuis* `not_home` (le `from` est `None` au restore) : la condition ne peut jamais être vraie au boot. Les `notification_id` `presence_valentin`/`presence_constance` n'apparaissent dans **aucun** autre fichier (pas de reconstruction ailleurs). L'entête (`:51-54`) affirme pourtant la recalculabilité reload : **contradiction documentaire/implémentation à trancher**.

**NOTIF-02 — mode panne secteur (le plus insidieux).** [FAIT] `activation_mode_panne.yaml:101-116` possède bien un trigger boot `ha_start` (`systeme_stable → on`), mais sa condition impose `panne_secteur_active == off`. Cet `input_boolean` est restauré `on` si HA reboote pendant la panne → la garde bloque la ré-entrée → l'action déléguée `script.mode_panne_coupure_secteur` (qui porte le `create`) n'est pas rejouée. La garde d'idempotence est **correcte** pour éviter de re-déclencher l'ECS de secours ; le défaut est **architectural** : la *signalisation* (notification) est couplée à l'*action d'entrée* au lieu d'être une projection d'état indépendante (cf. modèle bouclage). [RECO] Extraire la notif `mode_panne_secteur` dans une automation de projection dédiée `panne_secteur_active → {create/dismiss}` + `systeme_stable → on`, sur le modèle de `alarme/notification.yaml` corrigé.

**NOTIF-06 — événements déguisés + absence d'id.** [FAIT] `system/saisons.yaml:74-78` : `create` sans id, message `**{{ input_select.saison }}** a **{{ saison_calculee }}**` = transition de saison, non-dismissable, une nouvelle instance empilée à chaque changement. [FAIT] `ecs/reset_verrou_cycle.yaml:58-64` : titre « 🔄 ECS – Verrou cycle **levé** », message « le verrou **a été remis à OFF** automatiquement » = action passée. [FAIT] `chauffage/courbe_de_chauffe/auto_ajustement.yaml:197-207` : « Ajustements **proposés** … Aucun changement n'a été appliqué » = compte-rendu de calcul ; le bloc voisin émet aussi `now().strftime(...)` (`:195`, dans un `event:`, hors persistant). [RECO] Ces trois cas sont des **événements**, pas des états : les requalifier en push mobile (`script.notification_envoyer`) ou en logbook, et retirer le `persistent_notification.create`.

---

## 4. Couverture du checker — angles morts

Le checker `check_notifications_contracts.py` vérifie **la forme** ; il ne couvre pas **la structure ni la sémantique** du cycle de vie. Angles morts constatés, tous illustrés par les constats ci-dessus :

- **[FAIT] Pas de détection de re-création boot manquante** — l'invariant central (recalculabilité après restart) n'est pas testé. NOTIF-01/02/03 passent le checker.
- **[FAIT] Pas de détection d'`id` absent** — T5 signale un `id` présent dans ≥ 4 fichiers, mais **pas l'absence d'`id`** (non-dismissable + empilable). NOTIF-06 passe le checker.
- **[FAIT] Pas de détection d'événement déguisé par le lexique du message** — T3 ne filtre que des verbes de **titre** (liste courte : « relance », « arrêt »… — sans « levé », « proposé », « remis ») et T4 ne cherche que des **fonctions** temporelles (`now()`, `strftime`…) dans le bloc create, pas les formulations au passé du corps. NOTIF-06 passe le checker.

[RECO] Extensions candidates (non appliquées) : (a) flaguer tout `persistent_notification.create` **sans** `notification_id` ; (b) flaguer un `create` de projection d'état **sans** trigger `systeme_stable`/`homeassistant start` dans le même fichier (heuristique, WARN) ; (c) élargir le lexique de titre et l'étendre au message. À arbitrer — certaines relèvent d'une analyse sémantique difficile à automatiser sans faux positifs.

---

## 5. Axes non audités dans cette passe (honnêteté de périmètre)

- **Nature état↔événement des émetteurs *mobiles*** (inversion de canal : un état durable poussé en mobile, ou un événement projeté en persistant). Le canal mobile a été vérifié sur la **discipline d'abstraction** (0 bypass), **pas** exhaustivement sur la correspondance nature/canal des 76 sites d'appel.
- **Conformité du *corps* des messages** au-delà des titres (le checker et cet audit se concentrent sur titres, ids et cycle de vie).
- **Contenu dynamique Jinja des titres** (`{{ … }}`) : exempté par le contrat et le checker, non vérifiable statiquement.

---

## 6. Priorisation des suites (aucune appliquée — arbitrage propriétaire requis)

**P1 — trous structurellement garantis :**
1. **NOTIF-01** présence : ajouter un trigger `systeme_stable → on` recalculant `presence_*` depuis `person.*` (ou aligner l'entête sur la réalité si le comportement est assumé).
2. **NOTIF-02** mode panne secteur : découpler la notif `mode_panne_secteur` de l'action d'entrée gardée → projection d'état dédiée sur `panne_secteur_active`.

**P2 — re-création non garantie / sémantique :**
3. **NOTIF-03** : ajouter `systeme_stable → on` aux 5 projections `input_boolean`/alarme (babysitting, pré-confort, lave-vaisselle, buanderie, alarme) — alignement sur l'idiome bouclage.
4. **NOTIF-06** : requalifier les 3 « événements déguisés » en mobile/logbook, retirer le persistant sans id.
5. **NOTIF-05** : décider si `panne_internet`/`vmc` doivent reconstruire l'état au boot ou si la reprise différée est assumée.

**P3 — faible risque :**
6. **NOTIF-04** : aligner voiture/bluetti sur l'idiome canonique par cohérence (auto-guérison probable, non garantie).

**Durcissement CI (optionnel) :** extensions checker §4 (a)/(b)/(c).

---

## 7. Statut

- Audit : **lecture seule** — aucun runtime, contrat, checker ou workflow modifié.
- Domaine : **non clôturé** ; constats `NOTIF-01…06` ouverts, arbitrage propriétaire requis avant toute correction.
- Suites : ne maintiennent pas l'audit ouvert ; un chantier dédié pourra les porter.
