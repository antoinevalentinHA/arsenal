# C34 — Vague 2 : audit climatisation et chauffage

| Champ | Valeur |
|---|---|
| **Rapport** | Vague 2 du chantier [C34](../../04_chantiers/transverses/chantier_comportement_reboot_reload_domaines.md) — comportement au redémarrage, au rechargement YAML et au rechargement d'intégration. |
| **Domaines** | Climatisation (Airstage / commande directe) · Chauffage (consignes / Netatmo) |
| **Date** | 2026-07-24 |
| **Nature** | Audit statique, **appuyé sur la preuve runtime L4 existante** (effet établi au reload sur `switch.clim_power`, cf. cadrage §5.6). Aucun reboot, reload ni appel de service provoqué. |
| **Couverture** | **145 fichiers runtime** (climatisation 23+6+43 = 72 ; chauffage 21+8+45 = 74 — 2 de plus que le cadrage). **Chaînes décisives lues intégralement** (décision → exécution → actionneur, boot/reload) ; **inventaire des écrivains physiques complet par recherche exhaustive** ; templates de décision, notifications, compteurs d'énergie et observabilité échantillonnés. |

> **Règle appliquée (identique aux vagues 1, 3, 4).** *Démontré statiquement* exige la chaîne suivie
> jusqu'au service appelé, triggers et conditions lus. Tout point exigeant un reboot/reload provoqué
> est **indéterminable**, jamais « plausible ». La leçon des contre-audits précédents est intégrée :
> **la nature exacte de chaque entité déclencheuse est vérifiée** (brut d'intégration vs template
> normalisé/persisté) avant toute qualification.

---

## 1. Deux architectures opposées

L'audit établit d'emblée une **asymétrie structurelle décisive** entre les deux domaines :

| | Climatisation | Chauffage |
|---|---|---|
| **Actionneur** | **Commande physique directe** par Arsenal : `switch.clim_power`, `climate.clim` (Airstage) | **Aucun actionneur physique piloté par Arsenal** |
| **Écrivains** | 6 scripts (`clim_exec_apply_{cool,dry,heat,off}`, `heat`, `off`), `silence` | **Uniquement** `input_number.set_value` / `input_select.select_option` (consignes, plateaux, modes, courbe) |
| **Effet reboot/reload possible** | **Physique réel** (L4 : coupure + rejeu sur `clim_power`) | **Au niveau des consignes uniquement** ; l'actionnement est délégué à Netatmo (hors périmètre Arsenal) |

**Conséquence de cadrage** : seul le domaine **climatisation** peut produire un effet physique
directement attribuable à Arsenal au reboot/reload. Le **chauffage** en est **structurellement
incapable** (§3).

---

## 2. Climatisation — l'effet L4 au reload, expliqué et qualifié

### 2.1 Chaîne décision → exécution

| Rôle | Composant | Nature |
|---|---|---|
| Admissibilité (verrou persisté) | `input_boolean.besoin_clim_{cool,dry,heat}_admissible` | **helper persisté**, réconcilié au boot |
| Wrapper canonique | `binary_sensor.besoin_clim_cool_admissible` = `is_state(input_boolean…, 'on')` | miroir pur |
| Décision (pure) | `sensor.clim_target_mode` (`cool`/`dry`/`heat`/`off`) | template pur |
| Transit | `automation 10030000000105` (trigger `clim_target_mode`, **condition `systeme_stable == on`**) | relais |
| Exécution (idempotente) | `script.clim_execution` → `clim_exec_apply_{mode}` | availability-gaté, post-condition, retry borné |
| Actionneur | `switch.clim_power`, `climate.clim` (Airstage) | **physique** |
| Garde de cohérence | `automation 10030000000101` (trigger `clim_power`/`climate.clim`/`clim_target_mode`/`start`) | force `off` **uniquement si `target_off`** |
| Ré-assertion post-récupération | `automation 10030000000111` (`rearmement_apres_recuperation`) | **clé du reload** (§2.3) |

### 2.2 Le boot ne pilote pas l'équipement — **démontré statiquement**

Les trois `reconciliation_boot` (cool/dry/heat) déclenchent au `homeassistant start` mais
**réconcilient uniquement le verrou logique** `input_boolean.besoin_clim_*_admissible` — interdiction
explicite : « **Piloter `climate.clim` ou `switch.clim_power`** ». Elles attendent `systeme_stable`
(jusqu'à 5 min) puis n'activent qu'après un **délai gardé de 5 min** sur signaux stables. **Aucune
action physique au boot par cette voie.**

### 2.3 L'effet L4 (coupure + rejeu) — coupure d'origine intégration, rejeu = recalcul Arsenal

**Preuve runtime existante (L4)** : au reload, `switch.clim_power` subit une **coupure + rejeu**,
98,6 % équipement en marche (donc `target_mode = cool`). Le mécanisme est **entièrement expliqué
statiquement** :

1. **La décision reste `cool` pendant le reload.** `clim_target_mode` lit
   `binary_sensor.besoin_clim_cool_admissible`, **wrapper pur d'un `input_boolean` persisté**. Un
   `input_boolean` **n'est ni recréé ni rendu indisponible** par un reload YAML/template ni par un
   reload de l'intégration Airstage (helper HA, hors intégration). Le wrapper reste donc `on`,
   `target_mode` reste **`cool`** de bout en bout.
2. **Arsenal ne coupe donc jamais l'alimentation.** La garde (`10030000000101`) ne force `off` que si
   `target_off` — **faux ici**. `clim_exec_apply_off` n'est appelé que sur `target_off` (garde/exécution)
   ou par `silence` (horaire, non déclenché au reload). **Aucun chemin Arsenal ne coupe `clim_power`
   quand la cible est `cool`.** *Démontré statiquement.*
3. **La coupure est donc d'origine intégration.** `switch.clim_power` est une entité de l'intégration
   **Airstage** ; son reload la rend `unavailable` puis la recompose. L'en-tête de la garde le
   documente : « mises à jour d'entités **non simultanées** côté intégration » (`climate.clim` actif
   avant que `clim_power` ne reflète `on`). **Que le relais physique s'ouvre réellement, ou que seule
   l'entité passe `unavailable`, est indéterminable** (entité `unavailable` ≠ relais ouvert).
4. **Le rejeu est un recalcul fonctionnel Arsenal.** `rearmement_apres_recuperation` (`10030000000111`)
   déclenche **précisément sur la récupération** de `climate.clim`/`switch.clim_power`
   (`from: [unavailable, unknown]`, stabilisé 15 s) ou le `retour_ok_airstage`. Si un échec est latché,
   il **ré-asserte la décision persistée** (`target = cool`) via `clim_execution` → `apply_cool` (qui
   rallume `clim_power` s'il le lit non-`on`). **Gardé** (`systeme_stable`, hors panne secteur, entités
   disponibles) et **borné** (3 tentatives par front). *Démontré statiquement.*

**Qualification §2 — la « qualification non tranchée » du cadrage est levée :**

- **Coupure** : *action physique d'origine intégration Airstage* (reload), **non une décision Arsenal**.
  Réalité physique du relais **indéterminable**. Ce n'est **pas** un défaut au sens de l'invariant C34
  (l'opération technique — le reload — produit l'effet, mais Arsenal ne l'injecte pas).
- **Rejeu** : **recalcul fonctionnel** — ré-établissement de l'état décidé (`cool`) sur front de
  récupération, gardé et borné. **Correct**, non indésirable.

**Résidu honnête (arbitrage, non défaut Arsenal)** : chaque reload de l'intégration Airstage induit
un **cycle bref d'alimentation** de l'équipement (coupure intégration → rejeu Arsenal). Sa nuisance
réelle (le compresseur s'arrête-t-il quelques secondes ?) est **indéterminable** sans instrumentation
physique. À verser au portefeuille comme **question d'arbitrage** (tolérer le cycle vs raréfier le
reload d'intégration), **non comme défaut de code Arsenal**.

### 2.4 Watchdog, guard, silence, ventilation — pas de vecteur physique de boot supplémentaire

- **Guard** (`start`-déclenché) : force `off` **seulement si `target_off`** ; au boot avec cible `cool`
  et entités `unavailable`, la condition `clim_power == 'on'` est fausse ⇒ inerte. *Démontré.*
- **Watchdog** : ré-assertion de la **décision** sur incohérence persistante ≥ 60 s (jamais un forçage
  `off` transitoire) — cohérent avec le retrait documenté d'INV-3. *Démontré.*
- **`silence`** (écrivain `clim_power`) : **non déclenché au boot/reload** (horaire). Hors périmètre.
- **`application_consigne` cool/heat** (`set_temperature`) : ré-applique la **consigne de température**
  au boot — rafraîchit un setpoint, **pas** un cycle d'alimentation. Recalcul fonctionnel, faible impact.

---

## 3. Chauffage — aucun actionneur physique dans Arsenal

### 3.1 Écrivains = consignes uniquement — **démontré statiquement**

La recherche exhaustive des écrivains du domaine chauffage ne trouve **que** des
`input_number.set_value` (consignes, plateaux thermostatiques, paramètres de courbe) et des
`input_select.select_option` (modes, observabilité). **Aucun** `climate.set_temperature`, **aucun**
`switch.turn_*`, **aucun** appel Netatmo de consigne — vérifié **sur tout l'arbre** (`11_automations/`,
`10_scripts/`). Les seules occurrences Netatmo hors climatisation sont **diagnostiques** (âge données,
reboot station sur panne) ou le **watchdog de reload d'intégration**, jamais une écriture de consigne
de chauffe.

**Conséquence** : le domaine chauffage d'Arsenal est **structurellement incapable de produire une
action physique directe** (chauffe, coupure, impulsion) au reboot/reload. Il écrit des **consignes
(helpers)** ; l'**actionnement physique est délégué à Netatmo** (moteur de planning propre, **hors
périmètre des automatisations auditées**).

### 3.2 Comportement au boot — recalcul de consignes, gardé

- `decision_centrale_trigger` (`10240000000001`) porte un trigger `systeme_stable → on` : au boot, la
  **décision centrale chauffage recompute** et **réécrit les consignes** (helpers). Recalcul fonctionnel.
- `correction_demarrage` (`10240000000010`, `systeme_stable`-gardé) rejoue les corrections de **courbe**
  via `chauffage_appliquer_pente` / `_parallele` — écrivains de **helpers de courbe**, pas d'actionneur.
- `autorisation`, `representativite_thermique` : gardés `systeme_stable`, écrivains de helpers/selects.

**Qualification §2/§8** : au reboot/reload, le chauffage Arsenal produit un **recalcul / restauration
de consignes** (helpers), **jamais une action physique**. L'effet physique (chauffe réelle) est
**indéterminable** au sens strict — il relève du **planning Netatmo**, hors périmètre — mais **aucun
vecteur de défaut C34 n'existe dans la couche Arsenal chauffage**. Cohérent avec la preuve L4
(« indéterminable — aucun actionneur physique dans l'allowlist »), **précisé** : ce n'est pas une
lacune d'observabilité, c'est une **absence d'actionneur Arsenal par conception**.

---

## 4. Synthèse par événement et qualification

| Conclusion | Domaine · Événement | Qualification §8 | Grille §2 |
|---|---|---|---|
| Boot ne pilote pas l'équipement (réconciliation = verrou logique) | Clim · Reboot | Démontré statiquement | Abstention / continuité |
| Décision reste `cool` au reload (admissibilité = input_boolean persisté) | Clim · Reload | Démontré statiquement | Continuité légitime |
| Coupure `clim_power` au reload = origine intégration Airstage | Clim · Reload intégr. | **Démontré par preuve runtime L4** + statique (Arsenal ne coupe pas) ; réalité physique **indéterminable** | Action physique d'origine intégration — **pas un défaut Arsenal** |
| Rejeu `clim_power` = ré-assertion de la décision persistée | Clim · Reload intégr. | Démontré statiquement | Recalcul fonctionnel (gardé, borné) |
| Chauffage n'a aucun actionneur physique Arsenal | Chauffage · tous | Démontré statiquement | — (invariant non atteignable) |
| Consignes recomputées au boot (gardé `systeme_stable`) | Chauffage · Reboot | Démontré statiquement | Recalcul / restauration |
| Chauffe physique réelle | Chauffage · tous | **Indéterminable** (Netatmo, hors périmètre) | — |

---

## 5. Convergence transverse

- **La sûreté de la climatisation au reload tient à l'ancrage de la décision sur un `input_boolean`
  persisté**, non à `systeme_stable`. C'est la **même leçon** que le contre-audit de la vague 3 : la
  vraie protection contre les artefacts de reload est la **couche de normalisation/persistance** des
  entités décisionnelles (ici, le verrou d'admissibilité persisté qui empêche `target_mode` de
  basculer `off` pendant un reload), pas la garde `systeme_stable`.
- **L'unique effet physique établi de tout l'audit C34 (L4, `clim_power`) n'est PAS un défaut Arsenal**
  : la coupure est d'origine intégration, le rejeu est un recalcul correct. Le seul résidu est un
  **arbitrage** (tolérer le cycle d'alimentation au reload Airstage), non un correctif de code.
- **Chauffage et climatisation illustrent deux doctrines d'actionnement opposées** : commande directe
  (clim, exposée aux aléas de l'intégration) vs délégation à un planning externe (chauffage, immunisé
  côté Arsenal mais opaque côté Netatmo). Cette asymétrie mérite d'être **nommée au portefeuille**.

---

## 6. Limites probatoires

- **Couverture ciblée** : les chaînes décisives (décision → exécution → actionneur, boot/reload) et
  l'**inventaire complet des écrivains physiques** ont été lus/recherchés ; les ~130 fichiers restants
  (templates de décision, notifications, compteurs d'énergie, observabilité, retry transactionnel) ne
  contiennent **aucun écrivain physique** (climatisation : 6 scripts + `silence` ; chauffage : **zéro**)
  ni vecteur de boot physique — établi par recherche exhaustive, non par lecture intégrale.
- **Réalité physique de la coupure `clim_power`** au reload Airstage : **indéterminable** (entité
  `unavailable` ≠ relais ouvert ; `switch.clim_power` hors allowlist Recorder pour la trajectoire fine).
- **Chauffe physique** : **indéterminable** (planning Netatmo hors périmètre Arsenal).
- La preuve L4 ne distingue pas formellement reload YAML vs reload d'intégration ; l'analyse statique
  montre que **les deux conservent `target_mode = cool`** (admissibilité persistée), donc **aucun des
  deux ne produit de coupure Arsenal** — la coupure observée est cohérente avec le **reload
  d'intégration** (recomposition de `clim_power`).

---

## 7. Suite

Cette vague **n'ouvre aucun sous-chantier correctif** (stop point du cadrage §10). **Vague 2 close en
tant qu'audit.** Au **portefeuille** (livrable 3) : (a) l'**arbitrage** du cycle d'alimentation clim au
reload Airstage (tolérer vs raréfier le reload) — **pas un défaut Arsenal** ; (b) l'**asymétrie
doctrinale** commande-directe (clim) vs consigne-déléguée (chauffage). **Aucun finding de défaut
Arsenal.** Le **contre-audit de la vague 2** (attaquer l'attribution de la coupure, vérifier qu'aucun
chemin Arsenal — retry transactionnel chauffage inclus — ne pilote un actionneur, confronter aux
contrats `09_securite.md` clim et à la doctrine courbe de chauffe) reste à conduire avant le portefeuille.

---

## 8. Contre-audit de la vague 2

### 8.1 Périmètre et méthode

Attaque des conclusions des §1-§7 selon la discipline des contre-audits précédents : recherche des
écrivains **élargie à tout l'arbre** (YAML + `.storage` + dashboards), **vérification de la nature et
des triggers exacts** de chaque automatisation à écrivain physique, confrontation à la persistance
réelle des entités décisionnelles.

### 8.2 Conclusions confirmées — et renforcées

- **Chauffage sans actionneur physique Arsenal — confirmé de façon définitive.** La recherche
  **sur tout l'arbre** de `climate.set_temperature` / `climate.set_hvac_mode` / push Netatmo / toute
  cible `climate.*` **hors climatisation** est **vide**. Aucun chemin Arsenal ne pilote un radiateur ;
  l'actionnement reste **entièrement délégué au planning Netatmo** (hors périmètre). La conclusion du §3
  tient sans réserve.
- **Arsenal ne coupe jamais `clim_power` quand la cible est `cool` — confirmé.** `clim_exec_apply_off`
  (le **seul** appelant qui coupe `switch.clim_power`) n'a **que deux appelants** — `guard.yaml` et
  `execution_mode_cible.yaml` — **tous deux conditionnés à `target_off`**. Aucun autre chemin ne coupe
  l'alimentation.
- **La décision reste `cool` au reload — confirmé au niveau du helper.**
  `input_boolean.besoin_clim_cool_admissible` **ne porte aucun `initial:`** ⇒ il **restaure** son état
  au reboot et **persiste** au reload (helper hors intégration Airstage). L'ancrage de `clim_target_mode`
  sur ce verrou persisté est donc réel : pas de bascule `off` transitoire, garde jamais armée.
- **La ventilation ne rallume ni ne coupe jamais** : `ventilation/application_mode` (`10030000000120`)
  est gardée `clim_actif` (« l'intention ne rallume jamais la clim, contrat §7 ») et n'écrit qu'un
  `fan_mode` sur un équipement **déjà actif** — jamais `clim_power`. Elle est en outre **reload-aware
  par conception** (triggers bornés `from` indispo + note « `systeme_stable` ne couvre que le boot »).

**⇒ La qualification centrale du §2.3 est confirmée** : la coupure `clim_power` au reload est
**d'origine intégration Airstage**, le rejeu est un **recalcul fonctionnel** Arsenal. **Aucun défaut
Arsenal.**

### 8.3 Conclusion corrigée — le §2.4 se trompait sur `silence`

**Le §2.4 affirmait que `silence.yaml` est « horaire, non déclenché au boot/reload » et le rangeait
parmi les écrivains de `clim_power`. Les deux affirmations sont fausses.**

- `silence.yaml` (`10030000000020`) **porte bien un trigger `systeme_stable → on`** (boot/reload) — il
  n'est **pas** horaire.
- Il n'écrit **pas** `switch.clim_power` mais **`switch.clim_quiet_fan`** (interrupteur du ventilateur
  silencieux — confort acoustique), sur une clim **active** uniquement.

**La conclusion du §2.4 survit** (silence **ne coupe pas** l'alimentation), mais **pour une autre
raison que celle donnée** : ce n'est pas qu'il ne se déclenche pas au reload, c'est qu'il **agit sur un
autre interrupteur** que la puissance. Le §2.4 **omettait par ailleurs une écriture physique réelle au
boot** : au `systeme_stable → on`, `silence` **ré-asserte l'état du ventilateur silencieux**
(`clim_quiet_fan`), gardé et idempotent. **Qualification : recalcul fonctionnel — confort seul, aucun
effet sur la puissance ni le mode HVAC.** À ajouter à la cartographie ; **sans conséquence** sur le
verdict « aucun défaut ».

### 8.4 Writers manuels (dashboard) — hors vecteur boot/reload

`18_lovelace/dashboards/climatisation/principal.yaml` expose un contrôle de `switch.clim_power`
(intention utilisateur). **Writer manuel**, ni automatique ni vecteur de boot/reload — même taxinomie
que les vagues 3 et 4. La formulation « écrivains automatiques » du rapport reste exacte.

### 8.5 Note d'actualité — évolution `main` post-audit (#566)

Depuis l'audit, `main` a intégré un changement de **réglages** climatisation (#566 : mode Dry de plein
droit, réordonnancement de la ventilation inter-modes). Il porte sur l'**admissibilité/ordonnancement
des modes**, **non** sur le mécanisme de reload (`clim_power`, garde, `rearmement`, persistance de
l'admissibilité). **Les conclusions de la vague 2 restent valides** sur la base rebasée.

### 8.6 Conséquences pour le portefeuille

- **Verdict inchangé : aucun finding de défaut Arsenal en vague 2.** La confirmation est **renforcée**
  (chauffage définitivement sans actionneur ; `apply_off` prouvé target-off-only).
- **Une micro-observation ajoutée** (non défaut) : `silence` ré-asserte `clim_quiet_fan` au boot —
  recalcul de confort, à porter en cartographie.
- Les deux points portefeuille tiennent : **arbitrage** du cycle d'alimentation clim au reload Airstage,
  et **asymétrie doctrinale** commande-directe (clim) vs consigne-déléguée (chauffage). La **leçon
  transverse** (protection = ancrage sur entité persistée/normalisée, non `systeme_stable`) est
  **confirmée** ici par la persistance du verrou d'admissibilité.
