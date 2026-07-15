# Plan d'action — Suites de l'audit Notifications (cycle de vie des persistantes)

> **NON NORMATIF — boussole de livraison.** Ce document **oriente le chantier C15** issu de l'audit
> [`audit_notifications_domaine.md`](../../01_rapports/notifications/audit_notifications_domaine.md).
> Il ne définit aucune règle : la **source normative** reste le contrat
> [`notifications.md`](../../../contrats/notifications.md) et le cockpit d'état reste le registre, ligne **C15**
> ([`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)).
>
> **Vivant** : à relire avant chaque lot, à mettre à jour après chaque lot, à clôturer quand les constats sont soldés.
>
> **✅ PLAN CLOS (2026-07-15).** NOTIF-01→06 soldés (L1→L5 appliqués ou décidés) **et validation terrain acquise**
> (§5) : C15 est **clôturé** au registre (⑤). Le domaine transverse des notifications est déclaré **re-conforme**.
> Subsiste, **hors périmètre et non bloquant** : le durcissement CI du checker (§4, lot ultérieur optionnel) et
> la reprise différée assumée de `panne_internet` (L4, décision actée, aucun changement runtime).

## 1. Cadre

- **Origine** : audit statique lecture seule. Verdict — canal mobile **sain** (0 contournement) ; cycle de vie des
  **persistantes partiellement non conforme** : HA ne restaure pas les `persistent_notification` au reboot, l'idiome
  canonique de re-création (`input_boolean.systeme_stable → on`) existe (bouclage, clim, chauffage confort, vacances)
  mais **manque à plusieurs projections d'état**.
- **Arbitrage propriétaire (2026-07-09)** : correction des deux P1 ; **inclusion des P2/P3** (NOTIF-03→06) dans le chantier.
- **Doctrine appliquée** : une **projection d'état** est recalculable au boot depuis le seul état courant ; un **événement**
  se restitue en mobile/logbook, jamais en persistant sans état associé (contrat § « Canaux autorisés », § « Événement déguisé »).

## 2. Idiome cible (référence)

Modèle canonique de projection d'état — [`bouclage/notification.yaml`](../../../../11_automations/bouclage/notification.yaml) :

- **trigger** = entité source **+** `input_boolean.systeme_stable → on` ;
- **action** = `choose` piloté par le **seul état courant** (create si vrai / dismiss sinon), jamais par `trigger.from_state` ;
- `mode: restart`.

`systeme_stable` est posé ~45 s après le démarrage par
[`system/stabilisation_post_demarrage.yaml`](../../../../11_automations/system/stabilisation_post_demarrage.yaml) : il garantit que le
restore des entités est terminé avant la re-projection (évite la course restore/chargement de NOTIF-03).

## 3. Lots

| Lot | Constat | Prio | Nature de la correction | Statut |
|---|---|---|---|---|
| **L1** | NOTIF-01 présence | P1 | Automation rendue **trigger-agnostique** : re-projette `presence_valentin`/`presence_constance` depuis l'état courant de `person.*` sur tout trigger, dont `systeme_stable → on`. L'en-tête « recalculable » devient **vrai**. | ✅ appliqué |
| **L1** | NOTIF-02 mode panne secteur | P1 | **Découplage** : la notif `mode_panne_secteur` sort du script d'action gardé et devient une **projection dédiée** de `input_boolean.panne_secteur_active` (create/dismiss + `systeme_stable`). Recréée au boot même en pleine coupure. | ✅ appliqué |
| **L2** | NOTIF-03 (babysitting, pré-confort, alarme) | P2 | Ajout du trigger `systeme_stable → on` aux 3 projections d'état déjà state-driven. | ✅ appliqué |
| **L2** | NOTIF-03 (lave-vaisselle, buanderie) | P2 | Ces automations sont des **détections** (garde `cycle == off`), pas des projections : ajout naïf impossible. La persistante est **extraite** en projection dédiée de `input_boolean.*_cycle`. `debut`/`fin` conservent la détection, le flag et le push mobile de fin. | ✅ appliqué |
| **L3** | NOTIF-06 (saison, verrou ECS, simulation courbe) | P2 | **Événements déguisés** requalifiés : `persistent_notification.create` retiré, information restituée en **mobile** (saison, verrou ECS) ou **logbook + event** (simulation courbe, déjà présents). | ✅ appliqué |
| **L4** | NOTIF-05 VMC | P2 | Projection state-driven : ajout du trigger `systeme_stable → on`. | ✅ appliqué |
| **L4** | NOTIF-05 panne_internet | P2 | **Décision : reprise différée assumée.** La notif `panne_internet` est **intrinsèquement couplée à la campagne de remédiation active** (« Remédiation automatique active ») — ce n'est pas une projection pure de `acces_externe`. La recréer seule au boot mentirait sur l'état de campagne. La re-détection nominale (`to:off for 5min`) rétablit notif **et** campagne. Pas de changement runtime. | ✅ décidé |
| **L5** | NOTIF-04 (voiture, bluetti) | P3 | Cohérence : voiture → ajout trigger `systeme_stable`. Bluetti → persistante restructurée en projection de `bluetti_alerte_active`, le **push mobile reste gardé sur la transition** (événement). | ✅ appliqué |

## 4. Angles morts du checker (durcissement CI — différé, non bloquant)

L'audit §4 relève que `check_notifications_contracts.py` vérifie **la forme**, pas **la structure** du cycle de vie.
Extensions candidates, **non appliquées** (à arbitrer — risque de faux positifs) :

- (a) flaguer tout `persistent_notification.create` **sans** `notification_id` (attrape les événements déguisés type NOTIF-06) ;
- (b) heuristique WARN : `create` de projection d'état **sans** trigger `systeme_stable`/`homeassistant start` dans le même fichier ;
- (c) élargir le lexique de titre interdit et l'étendre au corps du message.

Le point (a) est le plus sûr (peu de faux positifs) et le plus utile comme garde-fou anti-régression. À décider en lot ultérieur.

## 5. Validation

- **Statique** : `check_notifications_contracts.py` vert + `yamllint` propre (les IDs neufs `10040000000004`,
  `10080000000006`, `10080000000007` respectent le préfixe de domaine, `max+1`).
- **Terrain — ✅ ACQUISE (2026-07-15)** : reboot volontaire pendant un **cycle lave-vaisselle réel** → la persistante
  `lave_vaisselle_cycle` est **recréée 47 s après le démarrage** (≈ le `delay: "00:00:45"` de `systeme_stable`),
  **sans aucun `input_boolean.turn_on` intercalé** — le flag a donc été *restauré*, pas redétecté par `debut.yaml`
  (seuil 30 W / 3 min), ce qui **exclut le confondant de re-détection par les données seules**. La même fenêtre
  contient le **contrefactuel** : 7 reboots pré-correctif survenus cycle actif, tous suivis d'**aucun acte**
  (notification perdue = le défaut d'origine). Réserve du 2026-07-13 **levée**.
  Preuve : [`preuve_terrain_c15_survie_persistantes_reboot.md`](../../01_rapports/notifications/preuve_terrain_c15_survie_persistantes_reboot.md).
  **Portée** : établit l'idiome canonique sur le véhicule de preuve admis par le protocole (`lave_vaisselle_cycle`
  **ou** `buanderie_cycle`), l'idiome étant partagé par toutes les projections corrigées ; les autres instances
  restent couvertes par la validation statique, comme prévu — sans exigence terrain propre à chacune.

## 6. Règles de mise à jour

- Co-commit du registre C15 à chaque changement d'état.
- Ne pas y inscrire les commits (ce n'est pas un changelog).
- Clôturer ce plan quand NOTIF-01→06 sont soldés (terrain inclus) et déclarer le domaine transverse re-conforme.

---

*Plan d'action vivant — non normatif. Source normative : [`notifications.md`](../../../contrats/notifications.md). Cockpit : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md) (C15).*
