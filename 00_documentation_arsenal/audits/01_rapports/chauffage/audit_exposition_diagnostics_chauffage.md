# ♨️ ARSENAL — RAPPORT D'AUDIT · Chauffage — Exposition diagnostique vs contrats

## 📌 Métadonnées

- **Statut** : rapport d'audit documentaire — **lecture seule, descriptif et non normatif**. Ce document **ne crée aucune exigence** et n'a **aucune valeur opposable** : les contrats restent les seules exigences opposables.
- **Domaine** : Chauffage — observabilité diagnostique / dashboards
- **Dépôt** : `antoinevalentinHA/arsenal`
- **Révision auditée** : `1d432e3`
- **Posture** : audit **strictement documentaire**. Aucun runtime, capteur, automation, script, template, `recorder.yaml`, dashboard, carte, contrat ou checker modifié. Aucune remédiation codée. **Aucun chantier runtime n'est ouvert.**
- **Autorité normative** : les **contrats fonctionnels Chauffage** ([`contrats/chauffage/`](../../../contrats/chauffage/)) — *le contrat précède l'implémentation*.

### Précision d'autorité

- Les **contrats Chauffage** (et, pour la visibilité des paramètres invalides, le contrat transverse [`parametres_invalides.md`](../../../contrats/parametres_invalides.md)) sont l'**unique autorité normative**. Ce rapport ne s'y substitue pas et n'ajoute aucune exigence.
- Les identifiants **`CH-DIAG-*`** sont **purement structurants** : ils organisent la lecture de l'audit ; ils **ne constituent pas des exigences** et ne créent aucune obligation nouvelle. Les exigences réelles restent portées, exclusivement, par les contrats cités.
- La **CI n'est pas source d'exigence**. Le **runtime existant** ne devient pas normatif par sa seule existence.
- La **doctrine UI** Arsenal (`ui/couleurs/`) est mobilisée **uniquement** pour évaluer la restitution correcte d'une projection **déjà exigée** par un contrat — elle **ne crée aucune exigence** (précédent Alarme). Une **amélioration UI non exigée ne dégrade jamais un verdict contractuel**.
- Ce rapport porte l'**axe exposition diagnostique** ; il est **distinct** des rapports Chauffage existants (auto-ajustement de courbe, blocage post-aération, diagnostics thermiques, dashboards diagnostics), qu'il **cite en connexe sans les réécrire**.
- **Toute conclusion est bornée à l'exposition diagnostique auditée** : ni la justesse des décisions, ni le runtime, ne sont jugés ici.

### Précédent méthodologique

La méthode (chaîne de preuve, typologie de canaux, discipline anti-wishlist) reprend les précédents **Alarme** [`audit_exposition_diagnostics_alarme.md`](../alarme/audit_exposition_diagnostics_alarme.md) et **ECS** [`audit_exposition_diagnostics_ecs.md`](../ecs/audit_exposition_diagnostics_ecs.md), **sans transposition** : aucun type de diagnostic, canal, entité, gravité ni verdict n'est reporté depuis ces domaines. L'inventaire est **entièrement dérivé des contrats Chauffage**.

---

## 🎯 1. Objet & périmètre

**Objet unique** : déterminer si les diagnostics **exigés (explicitement ou implicitement) par les contrats Chauffage** — la raison de la décision, l'intention, l'état réel, les blocages, l'indisponibilité d'exécution, l'abstention, les paramètres invalides — sont (a) **produits par le runtime**, puis (b) **exposés de façon exploitable et fidèle** sur le **canal contractuellement imposé**, de sorte qu'un opérateur puisse comprendre **pourquoi le chauffage chauffe, ne chauffe pas, réduit, attend ou s'abstient**.

**Dans le périmètre** : la chaîne diagnostique de bout en bout — exigence contractuelle → production runtime → exposition (dashboard / carte / notification / canal global) → compréhension ; la **fidélité** des dashboards à la décision réelle ; la restitution des **indisponibilités** et des **paramètres invalides** sans fallback trompeur ; le maintien d'une UI **purement représentative**.

**Hors périmètre** : la justesse/sûreté des décisions (on audite l'**observabilité**, pas la décision), la conformité graphique/navigation générale, la performance, la CI (jamais source d'exigence), et **l'architecture décisionnelle, les contrats et le runtime en tant que tels**. Les écarts purement internes au runtime, à la CI ou à la documentation, **sans conséquence sur un diagnostic exposé**, sont consignés au plus comme observations secondaires (§11). **Ce rapport ne recommande, ne justifie et n'autorise aucune modification du runtime, des contrats ou de la CI. Les suites directement issues de ses constats sont exclusivement UI** (§14).

---

## 🔬 2. Méthode & chaîne de preuve

Pour chaque besoin diagnostique, la chaîne suivante est établie, chaque maillon attesté par une preuve citée :

```
P-C    Contrat normatif (exigence citée)
        ↓
P-R    Production runtime (porteur, écrivains, valeurs, unicité)
        ↓
P-EXPO Exposition sur le canal exigé (projection UI | notification | canal global)
        ↓
P-COMP Compréhension (lisibilité, fidélité, distinction des états, indisponibilité)
```

**Règle d'or** : aucune non-conformité sans base contractuelle démontrable ; le maillon rompu localise la couche fautive et détermine le verdict. **Une exigence non portée par un contrat ne produit jamais de verdict `PARTIEL`/`NON_CONFORME`** : elle est classée observation.

**Typologie des verdicts** : `CONFORME` · `PARTIEL` · `NON_CONFORME` · `RUNTIME_MANQUANT` · `CONTRAT_AMBIGU` · `HORS_CONTRAT` (amélioration/constat non exigé, hors chemin de verdict et **hors bilan chiffré**).

**Typologie des constats non-verdict** (pour discipline de classement) : **écart contractuel** (une exigence de contrat n'est pas satisfaite au canal exigé) · **dette UI** (défaut de restitution d'une projection, sans exigence de contrat spécifiquement violée) · **duplication de logique** (l'UI recalcule/recopie un verdict ou un seuil du backend) · **observation hors contrat** (aucune exigence contractuelle en jeu).

**Canaux d'exposition (déterminés par les contrats, non par le confort)** :
- **Projection UI** : raison, intention, état réel, blocages, verdicts de diagnostic (contrats `07`, `90`, `vannes`, `76`).
- **Notification** : notification persistante Confort (contrat `92`).
- **Canal global** : visibilité des paramètres invalides (contrat transverse `parametres_invalides`, couches 3 & 4 — **per-domaine explicitement interdit**).

---

## 📚 3. Corpus contractuel lu (source d'autorité)

Contrats Chauffage créant un besoin d'exposition, lus isolément avant ouverture du runtime UI :

- [`07_capteurs_diagnostics_structurants.md`](../../../contrats/chauffage/15_capteurs/07_capteurs_diagnostics_structurants.md) — **explicite** : miroirs de gouvernance `sensor.chauffage_raison_calculee` (« référence explicative canonique … dashboards de diagnostic »), `sensor.chauffage_mode_calcule` (« recalculer le mode attendu … afin de diagnostiquer la décision centrale réelle, détecter toute divergence »), écarts `sensor.ecart_consigne_confort` / `…_instantane`.
- [`90_semantique_thermique.md`](../../../contrats/chauffage/90_semantique_thermique.md) §11 (« raison dominante … **affichable en UI**, utilisée en diagnostic ») + §12 (interdictions sémantiques : ne pas confondre blocage/reduced, standby/attente, absence/reduced, **neutre/erreur**, comfort/présence).
- [`92_ui_notifications_persistantes.md`](../../../contrats/chauffage/92_ui_notifications_persistantes.md) — **explicite** : notification persistante Confort, source **exclusive** `sensor.programme_chauffage`, reconstructible post-reboot.
- [`vannes_thermostatiques_plateaux.md`](../../../contrats/chauffage/vannes_thermostatiques_plateaux.md) §11/§12 — **explicite** : verdict de stabilité, affichage, reset ; **V-2 ouvert** (seuils de verdict `0.02`/`0.05` dupliqués côté UI).
- [`76_observabilite_auto_ajustement_courbe.md`](../../../contrats/chauffage/76_observabilite_auto_ajustement_courbe.md) — **explicite** : observabilité de la courbe (déjà audité — **renvoi**, non ré-ouvert ; étanchéité INV-2 gardée en CI).
- [`30_decision_centrale.md`](../../../contrats/chauffage/30_decision_centrale.md) §10 + [`30…__amendement.md`](../../../contrats/chauffage/30_decision_centrale__amendement.md) (INV-30-6 : **cohérence des miroirs en tant qu'invariant CI** — le contrat n'impose pas une carte de divergence en UI), [`40_blocages.md`](../../../contrats/chauffage/40_blocages.md), [`80_table_decision_canonique.md`](../../../contrats/chauffage/80_table_decision_canonique.md), `45/46` aération — **implicites** : comprendre *pourquoi* (blocages, régime, exécution).
- [`parametres_invalides.md`](../../../contrats/parametres_invalides.md) (transverse) — **explicite** : visibilité **globale** des paramètres invalides ; couche 4 UI **conditionnelle**, per-domaine **interdit**.

---

## 📋 4. Inventaire des besoins diagnostiques audités (IDs `CH-DIAG-*` — structurants uniquement)

> Les identifiants ci-dessous **structurent l'audit** et **ne créent aucune exigence**. Chaque ligne renvoie au(x) contrat(s) qui porte(nt) réellement l'exigence ; en l'absence de contrat, il n'y a pas de besoin opposable (le point est traité en observation).

| ID | Besoin diagnostique audité | Canal exigé | Base contractuelle |
|---|---|---|---|
| **CH-DIAG-01** | Raison dominante (le « pourquoi » : chauffe / réduit / attend / s'abstient) | Projection UI | `07` (raison_calculee) · `90` §11 |
| **CH-DIAG-02** | Intention calculée exposée | Projection UI | `07` (mode_calcule) |
| **CH-DIAG-03** | État réel du chauffage (programme) | Projection UI | `90` · `92` |
| **CH-DIAG-04** | État Confort → notification persistante reconstructible | Notification | `92` |
| **CH-DIAG-05** | Capacité d'exécution / indisponibilité du bridge boiler | Projection UI | `30` §7 (garde G2) — implicite |
| **CH-DIAG-06** | Blocages actifs restitués (aération, post-aération, fenêtre, poêle, Vacances) | Projection UI | `40` · `45/46` · `80` · `07` |
| **CH-DIAG-07** | Verdict de stabilité des vannes thermostatiques | Projection UI | `vannes` §12 |
| **CH-DIAG-08** | Restitution correcte de l'**indisponibilité** sur les projections exigées (01/02/03) | P-COMP | `90` §12 (non-confusion sémantique) + doctrine UI appliquée à une projection **déjà exigée** |
| **CH-DIAG-09** | Écarts à la consigne exposés (diagnostic de réglage) | Projection UI / constatabilité | `07` (ecart_consigne_*) |
| **CH-DIAG-10** | Paramètres invalides visibles sans fallback trompeur | Canal global | `parametres_invalides` (couches 1→4) |
| **CH-DIAG-11** | Qualité thermique / diagnostics thermiques | Projection UI | `07` (08–11) — **renvoi**, déjà audité (hors chiffrage) |
| **CH-DIAG-12** | Observabilité de l'auto-ajustement de courbe | Projection UI | `76` — **renvoi**, déjà audité (hors chiffrage) |

**Note sur la divergence intention ↔ état réel.** Aucun contrat n'exige une **restitution UI** d'un verdict de divergence : `INV-30-6` porte la **cohérence des miroirs** comme **invariant CI**, non comme carte. La divergence est donc traitée en **observation hors contrat** (§10.4, O-1), pas comme un besoin opposable.

---

## 🔧 5. Production runtime (P-R)

| ID | Porteur runtime | Définition | Cohérence avec le contrat examiné |
|---|---|---|---|
| 01 | `sensor.chauffage_raison_calculee` | `12_template_sensors/chauffage/diagnostic/raison.yaml` | **Miroir strict** de la cascade `reason` du cerveau (`10_scripts/chauffage/decision_centrale.yaml` L239-280) ; **12 jetons** émis, `chauffage_non_autorise` **jamais** émis (branche N1 retirée en CH-2) ; cohérence gardée en CI (R-MIRROR-1) |
| 02 | `sensor.chauffage_mode_calcule` | `12_template_sensors/chauffage/diagnostic/mode.yaml` | recalcul indépendant du mode attendu (Confort/Neutre/Eco) ; **aucune entité de « cohérence » backend** n'est produite (la divergence n'est pas matérialisée) |
| 03 | `sensor.programme_chauffage` | plateforme boiler | état réel matériel |
| 04 | `persistent_notification` `chauffage_mode_confort` | `11_automations/chauffage/notification.yaml` (id `…019`) | create/dismiss sur `programme_chauffage == Confort` + reconstruction `systeme_stable → on` |
| 05 | `sensor.boiler_bridge_sante` / `binary_sensor.boiler_bridge_online` | domaine boiler (consommé) | capacité d'exécution (garde G2) |
| 06 | tokens de raison (aération/fenêtre/poêle/Vacances) + `input_boolean.chauffage_blocage_aeration`, `binary_sensor.poele_en_fonction`, timers aération | runtime décisionnel + aération | blocages actifs observables |
| 07 | `sensor.vannes_thermostatiques_stabilite_globale` | `12_template_sensors/chauffage/vannes_thermostatiques/stabilite_globale.yaml` | verdict très_stable/à_surveiller/instable/indisponible |
| 09 | `sensor.ecart_consigne_moyenne_24h` / `…_froid` / `…_doux` | `12_template_sensors/chauffage/ecart_consigne/` | écarts thermiques bruts (pas de verdict backend) |
| 10 | `binary_sensor.parametres_invalides_chauffage` → `group.parametres_invalides_domaines` → `binary_sensor.parametres_invalides_global` | `12_template_sensors/system/integrite_reglages/chauffage.yaml` ; `02_groups/parametres_invalides.yaml:34` ; `…/global.yaml` | sentinelle fail-closed produite, agrégée |
| 11/12 | famille diagnostics thermiques + observabilité courbe | `12_template_sensors/chauffage/diagnostic_thermique/*`, `…/courbe_*` | **déjà audités** (rapports dédiés) — renvoi |

**Constat borné (P-R) :** **les producteurs diagnostiques nécessaires au périmètre audité sont présents et cohérents avec les contrats examinés** — en particulier la raison dominante (`raison_calculee`) et l'intention (`mode_calcule`), dont la cohérence est gardée en CI (R-MIRROR-1, R-ISO-1). Sur ce périmètre, **aucun besoin diagnostique audité n'est `RUNTIME_MANQUANT`** : les écarts constatés se situent au maillon **P-EXPO / P-COMP** (l'UI). Ce constat **ne préjuge pas** de la santé du runtime en dehors de l'exposition auditée.

---

## 🖥️ 6. Exposition & compréhension (P-EXPO / P-COMP)

### 6.1 Deux surfaces, une source vive

L'UI expose le « pourquoi » via des *button-card templates* (`19_button_card_templates/40_dashboards/chauffage/`) qui lisent la **source vive** `sensor.chauffage_raison_calculee` — **jamais** le helper post-ACK `input_text.chauffage_raison` (non exposé, cf. §11). Le rendu (icône/libellé/couleur) est centralisé dans une **table canonique** `chauffage_registres_raison` (`…/00_donnees/chauffage_registres_raison.yaml`), qui mappe **exactement les 12 jetons vivants** — sans `chauffage_non_autorise` (correct).

- **Surface diagnostic** (`18_lovelace/dashboards/chauffage/diagnostic.yaml`) : « État global » = `chauffage_diagnostic_global_compact` (consomme la table). **Restitution exemplaire** : les 3 sources requises (`programme_chauffage`, `mode_calcule`, `raison_calculee`) sont testées contre `UNAV = [unknown, unavailable, undefined, null, none, '']` (L82) → une indisponibilité bascule en **gris indispo prioritaire** `rgba(158,158,158,0.1)` (L89-90, 142). Jeton vivant → libellé/couleur de la table.
- **Surface principale** (`18_lovelace/dashboards/chauffage/principal.yaml`) : `carte_chauffage_synthese` (L38), `carte_chauffage_intention` (L58), `carte_chauffage_decision` (L62). C'est là que se situe l'écart central de restitution de l'indisponibilité (§8).

### 6.2 Canaux non-UI

- **CH-DIAG-04** (notif Confort) : `notification.yaml` — persistante unique, create/dismiss, reconstruite via `systeme_stable → on`. Conforme au contrat `92`.
- **CH-DIAG-10** (params invalides) : la sentinelle chauffage est **déclarée dans le groupe** (`02_groups/parametres_invalides.yaml:34`) ; l'alerte conditionnelle globale (couche 4) est **incluse en tête** des deux dashboards principaux (`18_lovelace/dashboards/arsenal.yaml:19`, `…/navigation.yaml:19`). La **visibilité est donc assurée par le canal global exigé** ; l'absence de carte per-domaine sur les dashboards Chauffage est **conforme** (le contrat l'**interdit** : « Pas de lien direct vers un domaine spécifique »).

---

## ✅ 7. Matrice finale des verdicts

| ID | Canal | Verdict | Motif |
|---|---|---|---|
| **CH-DIAG-01** | Projection UI | **CONFORME** | miroir fidèle (12/12, CI R-MIRROR-1), table 12/12, indispo prioritaire correcte sur « État global » |
| **CH-DIAG-02** | Projection UI | **CONFORME** | l'**intention** (`mode_calcule`) est exposée et libellée (principal + « État global ») ; aucune restitution de divergence n'est exigée par contrat (→ §10.4, hors verdict) |
| **CH-DIAG-03** | Projection UI | **CONFORME** | `programme_chauffage` exposé (principal + diagnostic + historique) |
| **CH-DIAG-04** | Notification | **CONFORME** | persistante unique, reconstructible (contrat `92`) |
| **CH-DIAG-05** | Projection UI | **CONFORME** | capacité d'exécution (`boiler_bridge_sante`) exposée (diagnostic) |
| **CH-DIAG-06** | Projection UI | **CONFORME** | blocages restitués via tokens raison + cartes aération/poêle |
| **CH-DIAG-07** | Projection UI | **CONFORME** | verdict stabilité exposé (`carte_etat_interprete`, indispo `0.1`) ; duplication de seuils UI = **V-2**, observation (→ §10.2) |
| **CH-DIAG-08** | P-COMP | **PARTIEL** | **écart central démontré (F1)** : sur la surface **principale**, l'indisponibilité d'une projection exigée est restituée en état métier valide (brut / gris neutre / **faux rouge d'incohérence**) — confusion sémantique (`90` §12) |
| **CH-DIAG-09** | Projection UI | **CONFORME** | les **écarts à la consigne** sont exposés ; le contrat n'exige **aucun verdict centralisé** « trop chaud/froid » — l'interprétation par seuils côté UI est une **observation** (→ §10.2) |
| **CH-DIAG-10** | Canal global | **CONFORME** | visible via sentinelle globale ; per-domaine correctement absent |
| **CH-DIAG-11** | Projection UI | **Renvoi** *(hors chiffrage)* | diagnostics thermiques — rapport dédié ; note connexe : `diagnostic_thermique_contexte` sans garde indispo (→ §10.5) |
| **CH-DIAG-12** | Projection UI | **Renvoi** *(hors chiffrage)* | observabilité courbe — rapport dédié + étanchéité INV-2 CI |

**Bilan chiffré (sur 10 besoins diagnostiques audités, CH-DIAG-01…10) : 9 CONFORME · 1 PARTIEL (`CH-DIAG-08`) · 0 NON_CONFORME · 0 RUNTIME_MANQUANT · 0 CONTRAT_AMBIGU.**
Les besoins **CH-DIAG-11** et **CH-DIAG-12** sont des **renvois** vers des audits dédiés et **ne sont pas chiffrés** dans le bilan.

**Écart UI central réellement démontré :** la **mauvaise restitution de l'indisponibilité sur la surface principale** (`CH-DIAG-08` / F1). C'est le **seul** écart au sens verdict ; il est **strictement UI** et **sans conséquence fonctionnelle sur le chauffage**. Les autres points relevés (fraîcheur, reconstruction, duplication) sont des **observations** classées au §10, **sans dégrader aucun verdict contractuel**.

---

## 🩺 8. Écart central démontré — F1 (→ CH-DIAG-08)

**Nature :** dette UI de restitution d'une projection **déjà exigée** (confusion sémantique proscrite par `90` §12), **strictement UI**, **sans conséquence fonctionnelle** sur le chauffage (aucune décision, aucune commande n'en dépend).

- **P-C :** la raison (`07`, `90` §11) et l'intention (`07`) sont des projections **exigées** ; `90` §12 proscrit la **confusion sémantique** (« neutre ≠ erreur »). La doctrine UI (`ui/couleurs/`, priorité d'indisponibilité) en détermine la restitution correcte : `unknown/unavailable` doit être rendu en gris indispo, **jamais confondu** avec un état métier valide.
- **Constat (démontré) :** trois cartes de la surface principale n'ont **aucune détection d'indisponibilité** :
  - `carte_chauffage_intention.yaml` — aucune branche `UNAV` ; un état `unavailable` retombe en **libellé brut** (`return intention`, L78) et **aucune règle `state`** ne matche (L81-95, pas de `operator: default`) → pas de gris indispo. **La carte la moins défensive.**
  - `carte_chauffage_synthese.yaml` — aucune branche `UNAV` ; `unavailable` retombe en state « Inconnu » (L143), label brut `Régime unavailable` (L222, **fuite de l'état brut**) et couleur **gris neutre `0.2`** via `operator: default` (L319-322) → **l'indisponibilité est confondue avec le repos nominal**.
  - `carte_chauffage_decision.yaml` — un `mode_calcule` `unavailable` rend `coherent = false` (L76-81) → carte **ROUGE** `rgba(244,67,54,0.2)` (L87-89) : **une simple indisponibilité est présentée comme une incohérence décisionnelle** (le cas le plus trompeur ; conceptuellement analogue à `ALM-DIAG-003`).
- **Contraste :** la surface **diagnostic** (`chauffage_diagnostic_global_compact`, L82/89) restitue l'indisponibilité **correctement** (gris prioritaire). L'écart est une **asymétrie principale ↔ diagnostic** de restitution UI, pas une lacune de production ni une lacune du domaine.
- **Portée :** aucune conséquence fonctionnelle — le chauffage décide et exécute indépendamment de ce rendu. L'enjeu est la **lisibilité opérateur** sous indisponibilité.
- **Verdict : PARTIEL** (au maillon P-COMP, strictement UI).

---

## 🗂️ 9. Points conformes (rappel)

- **Le « pourquoi » est exposé et fidèle** : `raison_calculee` est un miroir strict gardé en CI (R-MIRROR-1) ; la table canonique couvre **12/12** jetons vivants ; la carte « État global » (surface diagnostic) restitue l'indisponibilité **correctement** (gris prioritaire). Les états « attend » (`presence_on` → « Attente »), « s'abstient » (`confort_suffisant`), « réduit » et « bloqué » sont **nommés** conformément à la sémantique `90`.
- **L'intention est exposée** (`mode_calcule`, principal + « État global »).
- **L'UI utilise la source vive** `raison_calculee` (toujours fraîche), **jamais** le helper post-ACK `input_text.chauffage_raison` → aucune raison périmée n'est exposée.
- **Notification Confort** conforme (`92`), **capacité d'exécution** visible, **blocages** restitués, **verdict vannes** et **diagnostics thermiques** exposés avec indispo `0.1`.
- **Écarts à la consigne** exposés (diagnostic de réglage).
- **Paramètres invalides** visibles via le **canal global** exigé ; per-domaine correctement absent.
- **UI purement représentative** : aucune écriture de décision ; la seule action est `script.reset_plateau_piece` (vannes), **action utilisateur bornée et contractuelle** (`vannes` §8).

---

## 🗒️ 10. Observations (hors chemin de verdict)

Ces points **ne dégradent aucun verdict contractuel**. Ils sont classés par nature et **ne portent aucune suite runtime**.

### 10.1 Reconstruction UI d'un verdict décisionnel (duplication de logique — fidélité)

Cas où l'UI **recalcule un verdict** décisionnel au lieu de lire une vérité backend, susceptible de **diverger** du backend si celui-ci évolue (aucun effet de bord : lecture seule) :

- `carte_chauffage_decision.yaml` L76-81 — **recalcule la cohérence intention ↔ réel** en JS (verdict de divergence reconstruit ; aucune entité backend de cohérence n'existe).
- `carte_chauffage_synthese.yaml` L82-143 — **réordonne la priorité métier** (brûleur > override > sécurité > contexte > stabilisation > nominal) en JS, au lieu de lire une raison unique.

> Gravité : **fidélité** (risque de divergence de verdict). Recoupe **IMPORTANT-2** de [`audit_dashboard_diagnostics_chauffage.md`](../lovelace/audit_dashboard_diagnostics_chauffage.md). Aucun contrat n'exige de restitution de divergence (cf. §10.4) → **observation**, pas un écart.

### 10.2 Duplication de seuils / interprétation visuelle (gravité moindre)

Cas où l'UI **recopie un seuil** d'interprétation, sans recomposer un verdict décisionnel du moteur :

- `chauffage_reglage_courbe_diag_72.yaml` — seuils d'interprétation `±0.4` / `±0.5` **codés en dur** (« Trop chaud / Trop froid / Déséquilibre / Sous-chauffe ») appliqués à des écarts bruts. Le contrat `07` n'exige **aucun** verdict centralisé de ce type → **observation** (pas de dégradation de `CH-DIAG-09`).
- `meteo_chauffage_actuelle_72.yaml` — comparaison ON/OFF (`ext < seuilOn` / `ext ≥ seuilOff`) colorée côté UI à partir des helpers de seuil (affichage indicatif).
- Seuils de réglage recomposés à l'affichage (`consigne ± offset`) dans `reglages_seuils_temperature_interieure.yaml` et `reglages_seuils_protection_geofencing.yaml`.
- Vannes : duplication `0.02`/`0.05` côté UI = **V-2** (déjà tracé au contrat `vannes` §11).

> Gravité : **moindre** (interprétation visuelle, pas de verdict de moteur reconstruit). Recoupe **IMPORTANT-1** (audit dashboard) et **V-2** (audit vannes). **Observation** doctrinale (« backend décide, UI observe »), non exigée stricto sensu par un contrat d'exposition.

### 10.3 Branche UI périmée — F2 (dette UI de fraîcheur)

- `carte_chauffage_synthese.yaml` mappe le jeton `chauffage_non_autorise` à **trois endroits** — state « Interdit (sécurité) » (L91-93), label « Interdit — sécurité système » (L172-174) et **couleur rouge** (L250-257) — alors que ce jeton **n'est plus émis depuis CH-2** (`raison_calculee` L74-125 ne le produit pas). La table canonique `chauffage_registres_raison` est **déjà propre** ; seule cette carte non migrée conserve la branche.
- **Effet :** branches **inatteignables** — aucun affichage erroné ne se produit. **Dette UI de fraîcheur**, strictement sur la carte.
- **Périmètre :** le constat est **borné à la branche UI**. Un commentaire runtime portant le même jeton existe par ailleurs, mais **le runtime est hors périmètre** : ce rapport **ne le juge pas et ne propose aucune modification runtime** (§14).

### 10.4 Surcouche rouge d'incohérence non exposée — O-1 (observation hors contrat)

- L'en-tête de `chauffage_registres_raison` mentionne une surcouche rouge d'incohérence portée par les briques ; `chauffage_diagnostic_global_compact` calcule `coherent` (L97-104) mais ne le lit jamais (code mort assumé). **Aucun contrat n'impose une carte/verdict de divergence en UI** (`INV-30-6` = invariant CI, pas UI) → **HORS_CONTRAT**. Identique à **IMPORTANT-2**. Rappelé pour éviter toute requalification en non-conformité.

### 10.5 Cartes secondaires sans garde d'indisponibilité — F4 (dette UI mineure)

- `diagnostic_thermique_contexte.yaml` affiche les états **bruts** (y compris `unavailable`) ; `barres_mode_reduit_chauffage.yaml` et `courbe_auto_confiance.yaml` n'ont **pas de garde**. Restitution mineure, hors chemin de compréhension décisionnelle centrale.

---

## 🧩 11. Observations secondaires (sans effet sur un diagnostic exposé)

- `input_text.chauffage_raison` (écrit par le bras exécutif uniquement sur ACK `applied`) **n'est exposé sur aucune surface** — l'UI consomme le miroir vif `raison_calculee`. Aucun risque « raison périmée en UI ». Trace interne, **hors périmètre exposition et hors périmètre runtime**.
- `chauffage_synthese_blocage_aeration_xl.yaml` n'est **référencé par aucun dashboard** (potentiellement orphelin) — à confirmer hors de ce rapport.
- `carte_chauffage_decision.yaml` documente en en-tête l'entité `sensor.chauffage_etat_reel` (**non définie** au dépôt) ; le site d'appel (`principal.yaml:61`) injecte `sensor.programme_chauffage`. Divergence d'en-tête sans effet fonctionnel.

---

## 🚧 12. Frontières de domaine

- **Boiler** : `sensor.boiler_bridge_sante`, `binary_sensor.boiler_bridge_online` — possédés par [`contrats/boiler/`](../../../contrats/boiler/) ; le Chauffage **consomme** (CH-DIAG-05).
- **Paramètres invalides** : couches 2-4 (`group`, sentinelle globale, alerte UI) — possédées par [`parametres_invalides.md`](../../../contrats/parametres_invalides.md) ; le Chauffage **fournit** sa sentinelle de couche 1 (CH-DIAG-10).
- **Diagnostics thermiques / courbe / vannes** : sous-domaines déjà audités — [`audit_diagnostics_thermiques_chauffage.md`](audit_diagnostics_thermiques_chauffage.md), [`audit_auto_ajustement_courbe.md`](audit_auto_ajustement_courbe.md), [`audit_dashboard_diagnostics_chauffage.md`](../lovelace/audit_dashboard_diagnostics_chauffage.md), [`audit_dashboard_diagnostics_vannes_thermostatiques.md`](../lovelace/audit_dashboard_diagnostics_vannes_thermostatiques.md).

---

## 🏁 13. Conclusion

Sur l'axe **exposition diagnostique vs contrats**, et **strictement borné à cet axe**, le domaine Chauffage apparaît **globalement conforme** : la raison de la décision (le « pourquoi »), l'intention, l'état réel, les blocages, la capacité d'exécution, la notification Confort, les écarts à la consigne et la visibilité des paramètres invalides sont **exposés sur le canal contractuellement imposé**. **Les producteurs diagnostiques nécessaires au périmètre audité sont présents et cohérents avec les contrats examinés** — aucun besoin audité n'est `RUNTIME_MANQUANT`. Un opérateur peut, sur la surface **diagnostic**, comprendre pourquoi le chauffage chauffe, réduit, attend ou s'abstient, avec une restitution correcte de l'indisponibilité.

**Un seul écart au sens verdict**, `PARTIEL`, **strictement UI** et **sans conséquence fonctionnelle** :
- **CH-DIAG-08 (F1) — restitution défaillante de l'indisponibilité sur la surface principale** : trois cartes décisionnelles rendent une indisponibilité comme un état métier valide (libellé brut / gris neutre confondu avec le repos / **faux rouge d'incohérence**), là où la surface diagnostic est exemplaire.

**Observations** (aucun verdict dégradé) : reconstruction UI d'un verdict de divergence et réordonnancement de priorité (§10.1, fidélité) ; duplication de seuils d'interprétation (§10.2, moindre) ; branche UI périmée `chauffage_non_autorise` (§10.3, fraîcheur, inatteignable) ; surcouche rouge non exposée (§10.4, hors contrat) ; cartes secondaires sans garde (§10.5). Aucun `NON_CONFORME`, aucun `CONTRAT_AMBIGU`.

La méthode a tenu ses garde-fous : distinction stricte exigence / production / exposition, et **écart contractuel / dette UI / duplication de logique / observation hors contrat** ; refus des faux positifs (per-domaine des paramètres invalides **correctement absent** ; surcouche rouge **non exigée** ; helper `chauffage_raison` non exposé donc hors sujet) ; aucune dégradation de verdict au motif d'une amélioration UI non exigée ; et évaluation de la compréhension **uniquement** là où une projection est **déjà exigée** par les contrats.

---

## 🚧 14. Suites éventuelles — bornées à l'UI, explicitement non autorisées

**Principe :** ce rapport **ne recommande, ne justifie et n'autorise aucune modification du runtime, des contrats ou de la CI** ; il n'ouvre aucun chantier et ne propose aucune modification fonctionnelle. Les suites directement issues de ses constats sont **exclusivement UI**, et chacune requiert une autorisation distincte :

- correction de **CH-DIAG-08 / F1** (garde d'indisponibilité sur `carte_chauffage_intention` / `…_synthese` / `…_decision`) — **UI seule** ;
- nettoyage de la branche UI périmée `chauffage_non_autorise` (§10.3) — **carte UI seule** ; le commentaire runtime homonyme **reste hors périmètre et n'est pas visé** ;
- arbitrage de la reconstruction/duplication UI (§10.1/§10.2) — recoupe **IMPORTANT-1**, **IMPORTANT-2**, **V-2**, **UI seule** ;
- gardes d'indisponibilité des cartes secondaires (§10.5) — **UI seule**.

**Les remédiations proposées par ce rapport sont strictement limitées aux dashboards et à l'exposition UI. Toute évolution runtime éventuelle relèverait d'un autre objet, d'une autre preuve et d'une décision indépendante.**

---

*Rapport d'audit documentaire, lecture seule, descriptif et non normatif. Aucune modification runtime, UI, Recorder ou contractuelle. Identifiants `CH-DIAG-01…12` structurants, non renumérotés, sans valeur d'exigence.*
