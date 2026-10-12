# Cadrage — Triage des constats de l'audit ergonomie & découvrabilité UI

| Champ | Valeur |
|---|---|
| **Type** | Cadrage de triage (préparation d'arbitrage, **sans décision**) |
| **Domaine** | UI Lovelace Arsenal — ergonomie, découvrabilité, affordance |
| **Statut** | **Ouvert — prépare l'arbitrage propriétaire.** Aucun constat n'est ici qualifié de défaut à corriger. |
| **Version** | 0.2 (cadrage revalidé) |
| **Date** | 2026-09-20 (rédaction) · 2026-10-12 (revalidation, §7) |
| **Dépôt** | `antoinevalentinHA/arsenal` — rédigé @ `e3004ab4` (`main`), revalidé @ `b32f5155` (`main`) |
| **Cadre** | Aucun YAML, aucun patch runtime, aucun contrat modifié. Ne tranche aucun des 13 constats. |
| **Source unique** | [`01_rapports/lovelace/audit_ergonomie_decouvrabilite_ui.md`](../../01_rapports/lovelace/audit_ergonomie_decouvrabilite_ui.md) — constat historique, lecture seule, non arbitré. Ce cadrage ne rouvre pas l'audit et n'en modifie aucune ligne. |

> **Objet.** Organiser les 13 constats du §4 de l'audit ergonomie en une grille
> exploitable pour l'arbitrage propriétaire, avec pour chacun : la doctrine ou
> le contrat à relire avant de trancher, les dépendances avec d'autres
> constats, et les familles de suite envisageables — **sans en privilégier
> une**.

> **Garde-fou de lecture.** Ce document **ne qualifie aucun constat de
> défaut**, **ne propose aucun correctif concret**, **n'ouvre aucun
> chantier**. Un constat qui n'est *pas* retenu à l'arbitrage n'a pas à être
> requalifié ni documenté ailleurs : le silence de l'arbitrage sur un point
> vaut statu quo, pas dette.

---

## 1. Objectif du triage

Permettre à l'arbitrage propriétaire de statuer, pour chacun des 13 constats
§4.1–§4.13 de l'audit, sur l'une de ces familles de suite — **à choisir
librement, constat par constat** :

- **(a) Assumé tel quel** — le constat est réel mais ne justifie pas de
  correctif (cas déjà couvert pour partie par `navigation.md` §6.1 sur les
  73/95 dashboards hors Menu, cf. §5 ci-dessous) ;
- **(b) Clarification documentaire seule** — la doctrine existante répond déjà
  à la question mais ne le dit pas assez explicitement (ex. distinguer
  « invariant volontaire » de « lacune ») ;
- **(c) Correctif UI textuel** — ajout/modification d'un `name`, d'un
  `title`, d'une phrase de restitution, sans nouveau composant ;
- **(d) Correctif UI structurel** — nouveau composant, nouvelle carte, nouvel
  écran (ex. une vue de synthèse) ;
- **(e) Vérification terrain complémentaire avant décision** — le constat
  porte un `[non vérifié]` dans l'audit source et mérite d'être confirmé
  avant tout arbitrage.

Un même constat peut appeler plusieurs familles à la fois (ex. (b) + (c)).

---

## 2. Périmètre (de ce cadrage)

- Reprendre les 13 constats §4.1–§4.13 de l'audit source, sans en altérer la
  formulation ;
- pour chacun, identifier la doctrine/le contrat propriétaire à consulter
  avant arbitrage (point 3 du bootstrap `CLAUDE.md`) ;
- signaler les dépendances entre constats (agir sur l'un peut rendre un autre
  sans objet, ou au contraire l'exiger pour rester cohérent) ;
- signaler les collisions avec des arbitrages **déjà rendus** sur un sujet
  voisin, pour éviter une réouverture non informée.

---

## 3. Hors périmètre (explicite)

- ❌ aucune qualification de « défaut » ou de « non-défaut » ;
- ❌ aucun correctif proposé, aucun YAML, aucun template modifié ;
- ❌ aucune priorisation implicite (l'ordre du tableau §4 suit celui de
  l'audit source, pas une hiérarchie) ;
- ❌ les points déjà listés « explicitement non conclus » par l'audit
  (§6 de l'audit — badge de notification après « Ignorer », conformité
  couleurs vs charte, comportements natifs Home Assistant) restent **hors
  triage** : ils ne sont pas des constats à arbitrer mais des zones que
  l'audit lui-même n'a pas instruites ;
- ❌ aucune ouverture de chantier ni entrée au `REGISTRE_CHANTIERS.md` — ce
  cadrage ne porte sur aucun chantier existant et n'en crée aucun.

---

## 4. Grille de triage

| # | Constat (résumé) | Doctrine / contrat à relire avant arbitrage | Dépendances | Familles de suite envisageables (non exclusives) |
|---|---|---|---|---|
| 4.1 | Icône Menu (grille) sans label ni tooltip — seul chemin vers `navigation-dashboard` | [`ui/navigation.md`](../../../ui/navigation.md) §7 (« invariants ») — ne prescrit aucun label ; `bouton_navigation_badge_carre` | **Racine** : conditionne 4.2, 4.3, 4.4 selon l'audit lui-même (§4.1 : « sa non-découvrabilité conditionne celle de tout le reste ») | (b) si §7 est volontairement muet sur le label ; (c) si un label/tooltip est retenu |
| 4.2 | Badges ⚙/🩺 et bandeaux latéraux non labellisés, généralisés à tout le système | [`ui/navigation.md`](../../../ui/navigation.md) §7 (badges, décrits comme points d'accès « invariants ») et §8 (bandeaux contextuels) — aucun des deux ne prescrit de label | Partage la cause de 4.1 ; toute décision sur 4.1 devrait, par cohérence du patron « généralisé », se poser la même question ici | (a)/(b)/(c) — probablement à trancher **conjointement** avec 4.1, pas isolément |
| 4.3 | Deux grilles de lecture (Menu par domaine / bandeau météo par grandeur) coexistent sans être annoncées comme telles | Aucune doctrine dédiée identifiée dans l'audit source | Conséquence du même déficit de signal textuel que 4.1/4.2 | (b)/(c) |
| 4.4 | 73/95 dashboards (77 %) sans tuile Menu | [`ui/navigation.md`](../../../ui/navigation.md) §6.1 — **autorise explicitement** la non-exposition d'une facette classe C (cas nommé : `ecs-petite-maison-dashboard`) | Conséquence directe de 4.1/4.2, pas un item autonome | (a) forte présomption au vu de §6.1 — mais c'est à l'arbitrage de le confirmer, pas à ce document |
| 4.5 | Ambiguïté d'affordance info / « plus d'infos » / navigation / action (tuile « Secteur » vs « NAS » sur Système, style identique) | [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) — à vérifier si son § « Lisibilité UI » couvre ce cas précis (nature de tuile) ou seulement décision/action | Indépendant de 4.1–4.4 | (b)/(c)/(d) selon ce que dit la doctrine une fois relue |
| 4.6 | Deux actions à conséquence, deux habillages : `Reboot HA` en habillage neutre (icône grise `mdi:restart`, indiscernable d'un lien de navigation avant tap) vs `Reset Calibration Zigbee` en habillage avertissant (fond orangé) — **toutes deux portent une `confirmation:`** ; reste l'absence de signal avant tap pour `Reboot HA` | **⚠️ Arbitrage déjà rendu sur ce point précis** : [`04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md`](../../04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md) §2 septies, entrée `D-NAV-COULEUR` du registre (2026-07-19) — **neutralisation gris volontaire**, « renversement de doctrine assumé » : une couleur chaude a été jugée *inviter* au clic d'une action destructive, le garde-fou retenu étant la `confirmation:` du `tap_action`, pas la couleur | Aucune avec les autres constats §4 | Toute réouverture de 4.6 **collisionne avec un arbitrage déjà rendu** — signalé ici pour que l'arbitrage soit informé, pas pour l'empêcher |
| 4.7 | Collision visuelle commande/décision sur `modes-dashboard` (« Vacances : Désactivé » vs « Vacances : Vacances inactives », styles proches) | [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) § « Lisibilité UI » — **cité nommément par l'audit** comme la règle que ce constat met en tension | Indépendant | (b)/(c)/(d) — c'est le constat le plus directement adossé à une doctrine déjà écrite |
| 4.8 | Titres dupliqués entre dashboard principal / réglages / diagnostics (Aération, Alarme, Chauffage, Climatisation, ECS, VMC, Volets, Ouvertures, Arrosage, Sommeil, Boiler ×3 ; exception : `diagnostics-eclairage-dashboard`) | Aucune doctrine de nommage dédiée identifiée dans l'audit source — à vérifier dans [`ui/README.md`](../../../ui/README.md) / `ui/architecture.md` avant de conclure à une simple omission | Indépendant ; touche potentiellement de nombreux fichiers `dashboards.yaml` si retenu | (c) — candidat le plus « resserré » (changement de `title:` seul) si l'arbitrage le retient, **mais reste à arbitrer**, pas préjugé ici |
| 4.9 | Absence d'état visible sur `ouvertures-dashboard` (nom seul, pas d'état avant tap) et `volets-dashboard` (aucun indicateur d'état) | Aucune doctrine dédiée identifiée ; l'audit lui-même distingue les deux cas (`ouvertures` plus saillant car nommé comme page d'état, `volets` plus défendable car panneau de commande pure) | Deux sous-décisions indépendantes, à ne pas fusionner | (a) pour l'un, (c)/(d) pour l'autre — l'audit invite déjà à les traiter séparément |
| 4.10 | Rupture de langage totale sur la tuile Menu « Énergie » → `/energy` (interface HA native, aucune donnée) | Hors doctrine Arsenal si le comportement relève du cœur Home Assistant — **marge de manœuvre réelle non établie par l'audit** (son §6 le classe déjà « non conclu » côté causes) | Indépendant | (e) d'abord — établir la marge de manœuvre réelle avant toute autre famille |
| 4.11 | Vocabulaire divergent pour une même réalité (« UPS » / « Onduleur » ; « Rec. météo » / « Palmarès météo ») | Aucune charte de vocabulaire identifiée ; à distinguer d'une charte de *couleurs* ([`ui/couleurs/`](../../../ui/couleurs/)), qui ne couvre pas le libellé | Indépendant ; le rapprochement « Lampe Enfants » / « Chambre Enfants » reste `[non vérifié]` dans l'audit source | (c) pour les deux cas confirmés ; (e) pour le rapprochement non vérifié |
| 4.12 | Jargon technique brut exposé (horodatage ISO 8601 NAS, `esp32_critical: 2_proxies_ko`) — **exemple Ping LAN périmé depuis #855** (2026-09-21, ESP32 retirés de Ping LAN), mais la tuile restitue toujours l'attribut `cause` brut, désormais sous la forme `critique_ko: …` / `importante_ko: …` ; exemple NAS inchangé (§7) | Aucune doctrine dédiée ; l'audit cite lui-même un **bon modèle interne directement réutilisable** (Aspirateur, « Dernier motif », §5 de l'audit) comme patron de traduction déjà éprouvé dans le dépôt | Indépendant | (c) — le patron de traduction existe déjà ailleurs dans le système, pas à inventer |
| 4.13 | Absence d'une synthèse « qu'est-ce qui réclame mon attention maintenant » | À vérifier : recoupement possible avec le domaine notifications (chantier C15, clos le 2026-07-15 — cycle de vie des persistantes ; source : [`01_rapports/notifications/audit_notifications_domaine.md`](../../01_rapports/notifications/audit_notifications_domaine.md), la ligne du registre ⑤ sortant à l'échéance de 90 j) avant de conclure à un manque | Indépendant des autres constats §4, mais **potentiellement le plus structurant en effort** (nouveau composant, pas un label) | (e) d'abord (confirmer qu'aucun mécanisme équivalent n'existe déjà) ; (d) seulement ensuite si retenu |

---

## 5. Repères doctrinaux à (re)lire avant tout arbitrage

- [`ui/navigation.md`](../../../ui/navigation.md) §6 (taxonomie A–E), §6.1 (exposition volontairement partielle de la classe C, cas `ecs-petite-maison-dashboard`), §6.5 (exemple de conformité `nas-dashboard`), §7 (badges, points d'accès « invariants ») et §8 (bandeaux contextuels) — reprise **telle quelle** par l'audit, non réinterprétée.
- [`ui/navigation_topology.yaml`](../../../ui/navigation_topology.yaml) — déclaration machine-readable, gardée en CI par `R-LL-NAV-1`.
- [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md) — cité nommément par l'audit pour 4.7 ; à vérifier pour 4.5.
- [`architecture/03_doctrines/commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md) — lu par l'audit en phase de confrontation (méthode §1.2), potentiellement pertinent pour toute famille (d).
- [`ui/couleurs/`](../../../ui/couleurs/) (`02_palette.md`, `02_1_palette_etiquettes.md`, `03_exceptions.md`, `05_regles.md`) — explicitement **hors périmètre de l'audit source** (§6), donc hors périmètre de ce triage aussi ; à instruire séparément si l'arbitrage le juge nécessaire.
- [`04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md`](../../04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md) §2 septies — **arbitrage déjà rendu** et directement opposable au constat 4.6 (voir §4 ci-dessus).
- [`01_rapports/lovelace/audit_navigation_ui_lovelace.md`](../../01_rapports/lovelace/audit_navigation_ui_lovelace.md) — audit antérieur, clos, périmètre structurel distinct (cf. §7 de l'audit ergonomie pour la délimitation).

---

## 6. Confirmation de cadrage

- ✅ **Aucun constat qualifié** de défaut ou de non-défaut ;
- ✅ **aucun correctif proposé** ;
- ✅ **aucun ordre de priorité imposé** — le tableau §4 suit l'ordre de l'audit source ;
- ✅ **aucun chantier ouvert**, aucune entrée `REGISTRE_CHANTIERS.md` ;
- ✅ **une collision avec un arbitrage déjà rendu signalée** (4.6 / `D-NAV-COULEUR`), pour éviter une décision non informée ;
- ✅ **aucun runtime, dashboard, template, contrat, checker ou changelog modifié**.

---

## 7. Revalidation (2026-10-12, `main` @ `b32f5155`)

Le cadrage, rédigé le 2026-09-20 et resté hors dépôt, a été confronté au
dépôt courant avant publication. **Aucune conclusion du triage n'est
modifiée** ; seules des références et des résumés ont été corrigés.

**Vérifié inchangé depuis `e3004ab4`** :

- `ui/navigation.md` et `ui/navigation_topology.yaml` : aucun commit ;
  §6.1 (cas `ecs-petite-maison-dashboard`), §6.5 (`nas-dashboard`, PR #828)
  et §7 (badges « invariants ») conformes aux citations ;
- 95 dashboards déclarés dans `18_lovelace/dashboards.yaml` ; seuls deux
  commits Lovelace depuis (#855 Système, #858 Aspirateur), sans effet sur les
  tuiles du Menu : la répartition 20 / 73 de l'audit reste valable ;
- 4.8 : titres dupliqués toujours présents (`title: Aération`,
  `Climatisation`, `Boiler` ×3 constatés) ;
- 4.12, exemple NAS : champ « Dernier démarrage » inchangé ;
- arbitrage `D-NAV-COULEUR` (4.6) : soldé le 2026-07-19, §2 septies, inchangé ;
- aucun arbitrage, chantier ni document postérieur ne traite l'un des 13
  constats.

**Corrigé dans cette version** :

- 4.2 et §5 : les bandeaux relèvent du §8 de `navigation.md`, pas du §7 ;
- 4.6 : le résumé omettait le second cas de l'audit (`Reset Calibration
  Zigbee`, habillage avertissant) et la `confirmation:` présente sur les deux ;
- 4.8 : Climatisation manquait à la liste ; exception positive ajoutée ;
- 4.12 : l'exemple `esp32_critical: 2_proxies_ko` est périmé depuis #855
  (2026-09-21) ; le motif persiste (attribut `cause` restitué brut,
  `critique_ko: …`) ;
- 4.13 : renvoi au registre pour C15 remplacé par le document source, la
  ligne ⑤ Clos récents arrivant à échéance (90 j après le 2026-07-15).

---

## Liens

- Audit source (constat, lecture seule) : [`01_rapports/lovelace/audit_ergonomie_decouvrabilite_ui.md`](../../01_rapports/lovelace/audit_ergonomie_decouvrabilite_ui.md)
- Audit structurel antérieur (clos, périmètre distinct) : [`01_rapports/lovelace/audit_navigation_ui_lovelace.md`](../../01_rapports/lovelace/audit_navigation_ui_lovelace.md)
- Doctrine navigation : [`ui/navigation.md`](../../../ui/navigation.md) · [`ui/navigation_topology.yaml`](../../../ui/navigation_topology.yaml)
- Doctrine décision/action : [`architecture/03_doctrines/separation_decision_action.md`](../../../architecture/03_doctrines/separation_decision_action.md)
- Doctrine commandabilité : [`architecture/03_doctrines/commandabilite.md`](../../../architecture/03_doctrines/commandabilite.md)
- Arbitrage antérieur pertinent (4.6) : [`04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md`](../../04_chantiers/lovelace/cadrage_couleurs_icones_navigation.md) §2 septies
- Index audits : [`audits/index.md`](../../index.md)

> **Portée.** Cadrage de triage : organise les 13 constats de l'audit
> ergonomie pour l'arbitrage propriétaire. Aucune décision, aucun correctif,
> aucun chantier. L'arbitrage reste entièrement à faire.
