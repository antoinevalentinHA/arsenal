# Audit Arsenal — Reload-flap des chaînes de `binary_sensor` template

> Type : rapport d'audit transverse — consignation (aucune remédiation dans cette PR).
> Portée : tous les `binary_sensor` template chaînés de `12_template_sensors/` et leurs consommateurs déclenchés par état dans `11_automations/` et `10_scripts/`.
> Mode : lecture seule — aucun runtime, contrat, CI ni UI modifié ; aucun patch produit dans cette PR.
> Référence dépôt : branche `main`, HEAD `f08ea6c` (2026-08-10).
> Origine : incident du 2026-08-09 (trace confirmée, cf. §1). Correctif du domaine `vacances` déjà mergé séparément (PR #681) et **exclu** du présent périmètre à traiter.
> Limite de méthode : audit conduit sur l'état committé de `main`. Le runtime Home Assistant n'a **pas** été observé ; « comportement au reload » = comportement déduit des sources + sémantique HA. Un point clé (émission ou non d'un état `unavailable` intermédiaire au tear-down d'une entité template) est **dépendant de la version HA** et est signalé comme tel là où il change la conclusion.

---

## 1. Contexte — l'incident déclencheur

Le 2026-08-09 à 22:44, un simple **rechargement des templates** (Dev Tools → « Reload template entities », sans redémarrage HA) a déclenché un **cycle de désinfection ECS** (montée haute du ballon, ~25 min). La trace de l'automatisation `ECS - Désinfection fin vacances` (`10250000000021`) confirme : déclenchée par état de `input_select.mode_maison` à **22:44:37**, branche de lancement exécutée, fin à 23:09:32.

Chaîne causale établie :

```
RELOAD templates
  └─ binary_sensor.vacances_planifiees_actives → unknown (transitoire)
       └─ is_state(...,'on') = False
            └─ binary_sensor.vacances_demandees  ON → OFF  (front descendant RÉEL)
                 └─ automation "Fin projection auto"  (trigger vacances_demandees → off)
                      └─ input_select.mode_maison : "Vacances" → "Normal"
                           └─ automation "ECS - Désinfection fin vacances" (trigger retour)
                                └─ script.chauffage_ecs_cycle mode desinfection 🔥
```

Le correctif `vacances` (gardes `availability:` + `for:`) est mergé et **hors périmètre** de la remédiation restante.

---

## 2. Le mécanisme générique (« reload-flap »)

Les `binary_sensor` template sont fréquemment **chaînés** : un template parent lit un **enfant template** via `is_state('binary_sensor.X','on')`, `states('binary_sensor.X') == 'on'`, `in [...]`, etc.

Ces idiomes **écrasent `unknown`/`unavailable` en `False`**. Or, au rechargement des templates, chaque entité template est détruite puis recréée et passe transitoirement par `unknown`. Un parent **non gardé** produit alors un **vrai front descendant `off`** (et non un simple `unknown`) — front qui est **actionnable** par un trigger `platform: state`.

**Signature dangereuse** = les deux conditions réunies :
- **(A)** template parent chaînant un enfant template via `is_state/==/in`, **sans clé `availability:`** ;
- **(B)** consommateur avec trigger `platform: state` `to: "off"` / `to: "on"` (ou `from/to`) sur ce parent, exécutant une **action conséquente** (service physique, appel de script pilotant du matériel, changement de mode). Un usage en **condition seule** n'est pas dangereux ; une notification/log est mineure.

**La parade** (déjà appliquée sur `vacances_*`) : une clé `availability:` sur le parent, keyée sur la disponibilité de ses enfants template :

```yaml
availability: >
  {{ states('binary_sensor.<enfant>') not in ['unknown', 'unavailable'] }}
```

Quand un enfant est indisponible, le parent passe à **`unavailable`** au lieu de `off` ; un trigger `to: "off"` ne se déclenche pas sur `→ unavailable`, et l'indisponibilité **remonte proprement la chaîne**.

---

## 3. Méthode

- 3 agents lecture seule en parallèle, partitionnés par domaine consommateur (ECS/chauffage/VMC/déshu/arrosage ; climatisation/voiture/bluetti/alarme/éclairage ; modes/imprimerie/système).
- Extraction des triggers `platform: state` avec `to:`, résolution de chaque entité vers sa définition template, vérification (A) chaînage-sans-`availability` et (B) action conséquente non gardée (`for:`, `availability:`, `from:`, stabilisation + relecture live).
- **Vérification manuelle** des trouvailles physiques directement dans les sources (cette étape a nuancé la sévérité de P1, cf. §4).

Repères de volumétrie : 435 fichiers template, ~1362 entités, ~100 portent déjà un `availability:`, 98 fichiers chaînent via `is_state('(binary_sensor|sensor).…`.

---

## 4. Trouvailles physiques (parade `availability` absente)

### P1 — `bouclage_autorise` → `switch.prise_bouclage` (pompe de bouclage ECS)

- **Template** : `12_template_sensors/bouclage/bouclage_autorise.yaml:43` — lit `binary_sensor.ecs_disponible` et `binary_sensor.presence_famille_securite` (deux templates) via `== 'on'`. **Pas d'`availability`.**
- **Consommateurs** :
  - `11_automations/bouclage/auto_extinction.yaml:42` — trigger `from:"on" to:"off"` → `switch.turn_off` sur `switch.prise_bouclage` (l.63).
  - `11_automations/bouclage/auto_demarrage.yaml:44` — trigger `from:"off" to:"on"` → `switch.turn_on` (l.64).
- **Verdict (vérifié, nuancé)** : ce n'est **pas** un cyclage certain. Les gardes `from:` protègent partiellement : si HA insère un état `unavailable` intermédiaire au tear-down, le `off` transitoire est atteint depuis `unavailable` → `auto_extinction` (`from:"on"`) **ne matche pas** ; mais le front de récupération `off→on` matche `auto_demarrage` → **réactuation possible du relais**. Si HA **n'insère pas** d'`unavailable` intermédiaire (`on→off→on` direct), les **deux** fronts matchent → cyclage `off` puis `on` du relais. Comportement **dépendant de la version HA**.
- **Sévérité : PHYSIQUE.** C'est le trou latent le plus net : actionneur physique, template flap-prone, protégé uniquement par `from:` (plus faible que `availability`/`for:`).
- **Parade** : `availability:` sur `bouclage_autorise`, keyée sur `ecs_disponible` **et** `presence_famille_securite`.

### P2 — `arrosage_intention` → script d'arrosage (électrovanne station 1)

- **Template** : `12_template_sensors/arrosage/intention.yaml:57` — lit `arrosage_besoin_sol`, `arrosage_suspension_pluie`, `arrosage_rain_bird_preconditions_runtime`, `rain_bird_pont_donnees_disponibles` (templates) via `is_state(...,'on')`. **Pas d'`availability`.**
- **Consommateur** : `11_automations/arrosage/declenchement.yaml` — trigger `to:"on"` **sans `from:` ni `for:`** ; condition `intention == 'on'` ; action `script.arrosage_rain_bird_station_1_courte_supervisee`.
- **Verdict** : le front de récupération `→on` relance le script. **Blast-radius borné par le template lui-même** (`cooldown_ok`, `fenetre_ok`, script `mode: single`) : ne peut relancer que **dans la fenêtre d'arrosage et hors cooldown**. Réel mais **fenêtre étroite**.
- **Sévérité : PHYSIQUE (secondaire).**
- **Parade** : `availability:` sur `arrosage_intention`, keyée sur `arrosage_besoin_sol` / `arrosage_suspension_pluie` (et les autres enfants template lus).

### P3 — `clim_target_mode` → `clim_mode_commande` → « Clim Guard » → extinction clim

- **Template** : `12_template_sensors/climatisation/decision/mode_target.yaml:36` — `sensor` (hors signature binaire stricte) lisant `besoin_clim_cool/dry/heat_admissible` (templates) via `is_state(...)` avec `{% else %} off`. **Pas d'`availability`.**
- **Relais** : `12_template_sensors/climatisation/decision/mode_commande.yaml` — possède une `availability:` fail-safe, mais qui **accepte `off` comme valeur valide** → un `off` collapsé est publié.
- **Consommateur** : `11_automations/climatisation/guard.yaml:117` — trigger `platform: state` (nu) sur `sensor.clim_mode_commande` ; condition `clim_active` + `mode_commande == 'off'`, gardée par `input_boolean.systeme_stable` ; action `script.clim_exec_apply_off` (l.154) → extinction physique de la clim.
- **Verdict** : possible mais **bien atténué** — garde `systeme_stable`, `mode: restart` + relecture live à l'exécution (course de timing), helpers `besoin_clim_*_admissible` persistants (récupération quasi-immédiate). **Le moins certain des trois.**
- **Sévérité : PHYSIQUE (course, atténuée).**
- **Parade** : `availability:` sur `clim_target_mode`, keyée sur les trois `besoin_clim_*_admissible`, pour qu'il devienne `unavailable` (et non `off`) au reload — le fail-safe de `mode_commande` s'abstiendrait alors.

---

## 5. MODE / MINEUR (indirect, auto-corrigé)

- **`presence_famille_unifiee`** (`12_template_sensors/presence/global.yaml`, chaîné, sans `availability`) → `11_automations/chauffage/decision_centrale_trigger.yaml` + `11_automations/climatisation/cool/horodatage_absence.yaml` : protégés par `delay:` + relecture live → recalcul consigne / horodatage éphémère, **pas d'action physique erronée confirmée**. Durcissement possible (non requis) : `availability:` sur `presence_famille_unifiee`.
- **`autorisation_clim_cool/heat/dry`** (`12_template_sensors/climatisation/autorisation/*.yaml`, chaînés, sans `availability`) → `11_automations/climatisation/{cool,heat,dry}/admissibilite.yaml` (`to:"off"`) → basculent des `input_boolean.besoin_clim_*_admissible` (flags internes, **pas de service physique**). Effet physique seulement **indirect** via P3. Mise à `off` au reload en partie **intentionnelle** (branche « besoin indisponible »).
- **Flags d'aération** : `tentative_aeration_en_grace` → `aeration/invalidation.yaml` ; `fenetres_maison_fermees_stable` → `aeration/disqualification_aeration.yaml` — basculent des `input_boolean` internes. Effet chauffage seulement indirect.

---

## 6. Confirmé sûr

- **Bluetti** (tout le cluster), **VMC** (`coherence`, `conformite_decision`, `haute_vitesse_commandee`), **déshumidificateur** (`for: 5min` + self-hold), **coupure/panne secteur** (`from:` + `for:` bornés, rejet des états `restored`) : déjà `availability:`, ou `for:` dépassant le transitoire, ou pas d'enfant template.
- **Alarme** (`application_decision_centrale.yaml`) : **NOOP-safe par construction** — l'écrasement pousse présence *et* absence vers `off` → décision `ABSENCE_NON_STABLE` → `NOOP` (bloqué par le garde `cible in ['DISARMED','ARMED_AWAY']`) ; `delay_on 5min` sur l'absence.
- **Éclairage jardin** : `from:'on'` + correctif reload explicitement commenté (extinction), directions `to:'on'` = sens sûr (le reload pousse vers `off`).
- **Voiture** (`restitution_climatisation_active`) : action = notification + `input_select` (« ne pilote pas le véhicule »).
- **Point d'ordre** : `binary_sensor.coupure_secteur` a une `availability:` mais keyée sur un `sensor` réel plutôt que sur son enfant template `critere_ups_sur_batterie` — non exploité (consommateurs gardés par `from:`), mais à noter si un durcissement de cohérence est souhaité.

---

## 7. Résultat transverse notable

**Aucun autre writer de `input_select.mode_maison` n'est déclenché par un `binary_sensor` template.** Les autres writers (`modes/normal.yaml`, `climatisation/modes.yaml`) sont déclenchés par `input_select.mode_maison` / `input_boolean` (non collapsants). Le chemin catastrophique « reload → fin de vacances fantôme → action physique » était **unique à `vacances_*`**, déjà corrigé.

---

## 8. Statut & suite

- **Statut** : consigné, **remédiation non appliquée** (décision : garder en audit).
- **Reste à traiter** (parade uniforme, faible risque, une clé `availability:` par parent) : **P1 bouclage**, **P2 arrosage**, **P3 clim-guard** — par ordre de netteté. Les items §5 sont optionnels (durcissement), les items §6 ne nécessitent rien.
- **Test empirique complémentaire suggéré** (runtime) : au prochain reload de templates, vérifier dans le logbook/historique un éventuel front sur `switch.prise_bouclage` (P1) — c'est le discriminant qui tranche la dépendance-version évoquée en §4.
