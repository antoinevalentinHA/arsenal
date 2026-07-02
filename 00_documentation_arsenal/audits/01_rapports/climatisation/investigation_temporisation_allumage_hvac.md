# INVESTIGATION — TEMPORISATION D'ALLUMAGE HVAC (CLIMATISATION)
## Origine, justification et non-obsolescence du délai de stabilisation post-allumage

> **Nature.** Investigation **statique** (runtime, historique Git, contrats,
> intégration Fujitsu), en lecture seule. Objet : comprendre **pourquoi** la
> couche Exécution observe un délai de stabilisation après l'allumage physique,
> avant de conclure quoi que ce soit sur son évolution.
>
> **Statut.** Constats stabilisés. **Aucune modification runtime décidée, aucun
> réglage proposé, aucun YAML / automatisation / script / template / helper /
> dashboard touché.** Seule la documentation est mise en cohérence (contrat
> [`08_execution.md`](../../../contrats/climatisation/08_execution.md) et le
> présent rapport).
>
> **Runtime = référence.** Le délai courant est lu tel qu'il existe dans le
> dépôt ; il n'est ni modifié ni recommandé à la modification.
>
> **Conclusion en une ligne.** Le délai est une **garde de stabilisation
> délibérée et contractualisée** (catégorie A — toujours justifiée) ; son
> **principe** est valide et non obsolète, seule la **valeur** (empirique) reste
> une question ouverte, sans mesure instrumentée à ce jour.

---

## 1. QUESTION D'INVESTIGATION

Le transitoire `dry → cool` observé au démarrage provient de la séquence
d'allumage : `switch.turn_on(clim_power)` → délai → `climate.set_hvac_mode`.
Avant toute évolution, une question devait être tranchée **sur preuve** :

> Le délai de stabilisation post-allumage est-il un mécanisme volontaire
> résolvant un problème réel, ou un reliquat devenu inutile ?

Sous-questions :
- Quand et pourquoi le délai est-il apparu ? A-t-il évolué ?
- Est-il documenté / contractualisé ?
- Est-il un contournement d'un rallumage manquant de l'intégration ?
- Son besoin sous-jacent est-il toujours d'actualité ?

---

## 2. HISTORIQUE DU MÉCANISME (preuve Git)

> ⚠️ Le dépôt était **shallow** (historique tronqué) ; l'enquête a nécessité un
> `git fetch --unshallow` **en lecture seule** pour atteindre l'historique réel
> (1184 commits). Sans cela, `git blame` / `git log --follow` renvoyaient un
> unique commit de frontière trompeur. Ces SHA sont consignés ci-dessous pour
> que l'enquête n'ait **pas** à être refaite.

| Date | Commit | Version | Valeur | Nature |
|---|---|---|---|---|
| 2026-03-23 | `5ce08c13` — « Arsenal v11 beta 5 » | v11 β5 | **`00:00:02`** | **Création** des scripts physiques. Pattern déjà présent : `switch.turn_on(clim_power)` → `delay 2 s` → `set_hvac_mode`. Idempotence basée sur une variable `hvac` **figée** (lue au tout début du script, avant l'allumage). |
| 2026-05-27 | `e0eebaa1` — « climatisation: harden admissibility and HVAC execution stabilization » | **v15.7.3** | **`00:00:02` → `00:00:10`** | **Durcissement de stabilisation** (voir §3). |
| depuis | *(aucun)* | → HEAD | `00:00:10` | `git log -L '37,37:10_scripts/climatisation/cool.yaml'` confirme **exactement 2 révisions** de la ligne : la valeur n'a **jamais** été retouchée depuis. |

Le commit `e0eebaa1` ne se limite pas à changer la valeur — c'est un lot cohérent
appliqué **symétriquement** à `cool.yaml`, `dry.yaml`, `heat.yaml` :

1. `delay 2 s → 10 s` après allumage ;
2. suppression de la variable **figée** `hvac` (lue avant l'allumage) ;
3. remplacement par une **lecture fraîche** `states('climate.clim')` dans la
   condition d'idempotence ;
4. ajout d'une **garde** `climate.clim ∉ [unknown, unavailable]` avant émission.

En parallèle, l'orchestrateur `execution_mode_cible.yaml` voit son délai de
stabilisation **post-commande** (avant qualification de la post-condition)
passer de **5 s → 15 s** dans le **même** commit.

> Lecture : le point corrigé n'était pas seulement « 2 s trop court », mais aussi
> le fait de **décider l'émission HVAC sur un état lu avant l'allumage**
> (potentiellement `off` / `unknown`). Le lot corrige les deux ensemble.

---

## 3. JUSTIFICATION

### 3.1 Justification contractuelle

Le commit `e0eebaa1` **co-modifie le contrat d'exécution** (preuve d'intention).
Le contrat [`08_execution.md`](../../../contrats/climatisation/08_execution.md)
énonce désormais :

- § Garanties : « les scripts physiques appliquent une **garde de stabilisation
  après allumage physique avant émission d'une commande HVAC** » ; « toute
  vérification d'état HVAC après allumage doit reposer sur une **lecture fraîche
  de `climate.clim`, postérieure à la stabilisation** ».
- § Stabilisation post-allumage : les post-conditions ne sont pas évaluées
  immédiatement, « afin de tenir compte des **latences de propagation des
  intégrations climatisation** ».

### 3.2 Justification technique (comportement de l'intégration)

Le contrat de sécurité
[`09_securite.md`](../../../contrats/climatisation/09_securite.md) documente le
phénomène sous-jacent (retrait d'INV-3, v1.5) :

> Lors de l'établissement d'un mode légal, l'intégration met à jour
> `climate.clim` (dérivé de `get_operating_mode`) **avant** `switch.clim_power`
> (dérivé de `get_device_on_off_state`). […] c'est une **phase normale
> d'allumage d'un mode légal**.

Les états dérivés de l'intégration ne sont donc **ni simultanés ni immédiats**
pendant une transition : c'est exactement la latence que la stabilisation
absorbe avant de lire `climate.clim` et de qualifier le résultat.

---

## 4. NON-OBSOLESCENCE (preuve Git + code)

Deux hypothèses d'obsolescence ont été testées et **réfutées** :

1. **« Le délai contourne un rallumage manquant de l'intégration. »** — Réfutée.
   `custom_components/fujitsu_airstage/climate.py` : `async_set_hvac_mode`
   rallume automatiquement l'unité éteinte (`get_device_on_off_state() == OFF →
   turn_on()`) puis applique le mode. `git blame` situe ce bloc au baseline
   `81246d11` (**2026-02-11**), soit **antérieur** à la création des scripts
   (2026-03-23). Le délai n'a **jamais** compensé un rallumage absent.

2. **« L'évolution de l'intégration a supprimé la latence visée. »** — Réfutée.
   L'intégration reste **poll-based** (`DataUpdateCoordinator`, intervalle local
   **60 s** dans `const.py`, `async_refresh()` après chaque commande) ;
   `hvac_mode` dérive de `get_operating_mode()` et l'état power de
   `get_device_on_off_state()` — snapshots non garantis simultanés en
   transition. Le comportement décrit en `09_securite.md` est **toujours
   d'actualité**. Le commit `5b43328d` (« harden runtime error handling ») n'a
   ajouté que de la gestion d'erreur, sans toucher la séquence allumage/mode.

**`pyairstage`** est une dépendance externe (via `manifest.json`), **non
versionnée dans le dépôt** : aucune limitation matérielle spécifique ne peut
être **prouvée localement**. La justification suffisante et prouvée est la
latence côté intégration Home Assistant (poll + refresh + non-atomicité), pas
une contrainte matérielle documentée.

---

## 5. LIMITES CONNUES

À consigner **comme limites**, non comme défauts :

- Le **principe** de stabilisation est considéré comme **valide** (justifié,
  contractualisé, non obsolète).
- La **valeur de 10 s est empirique** : le durcissement `2 s → 10 s` est un
  hardening (« harden … stabilization »), sans mesure de latence documentée.
- **Aucune mesure instrumentée** ne démontre aujourd'hui que 10 s est la valeur
  optimale (ni sur- ni sous-dimensionnée). Le changelog v15.7.3 documente le
  volet admissibilité du commit mais **n'itemise pas** le passage `2 s → 10 s` ;
  la trace explicite reste le contrat + le message de commit + le présent
  rapport.

---

## 6. PHÉNOMÈNE TRANSITOIRE D'ALLUMAGE (connu, non-bug)

La séquence d'allumage (mise sous tension puis application du mode) combinée à
la propagation des états peut faire apparaître **brièvement** le mode
précédemment retenu par l'unité avant le mode demandé :

```text
off → (mise sous tension) → mode retenu momentané (ex. dry) → mode demandé (ex. cool)
```

Ce passage est **transitoire** et relève de la **phase normale d'allumage**. Il
ne constitue **pas** une incohérence décisionnelle Arsenal :
`sensor.clim_target_mode` ne prend jamais cette valeur intermédiaire. Il est
formalisé côté contrat en
[`08_execution.md`](../../../contrats/climatisation/08_execution.md)
(« Phénomène transitoire d'allumage ») ; la cohérence **persistante** reste
couverte par le Watchdog (cf.
[`09_securite.md`](../../../contrats/climatisation/09_securite.md)).

L'effet de bord d'observabilité associé (p. ex. un verdict de diagnostic
ventilation transitant brièvement par `ecart`) est un artefact d'observation
pendant la transition, distinct du principe de stabilisation.

---

## 7. PISTES FUTURES (chantier indépendant, non ouvert)

Un **futur chantier éventuel** — **indépendant** de la présente investigation et
**non ouvert** à ce jour — pourrait :

- **mesurer** précisément les temps de stabilisation via le Recorder (fenêtre
  réelle entre `switch.turn_on` et un `climate.clim` valide/cohérent) ;
- **vérifier** si la valeur de 10 s est correctement dimensionnée (sur- /
  sous-dimensionnement) ;
- **étudier séparément** l'effet de bord d'observabilité (mode retenu
  transitoire) **sans** remettre en cause le principe de stabilisation.

Ces pistes ne conditionnent pas le comportement actuel et ne sont **pas** un
prérequis : elles sont signalées, non ordonnancées.

---

## 8. FICHIERS ET LIGNES CONCERNÉS (référence)

| Fichier | Repère | Rôle dans l'investigation |
|---|---|---|
| `10_scripts/climatisation/cool.yaml` | bloc allumage + `delay` | Délai de stabilisation post-allumage (idem `dry.yaml`, `heat.yaml`) |
| `10_scripts/climatisation/execution_mode_cible.yaml` | stabilisation post-commande | Délai avant qualification de la post-condition (`5 s → 15 s` en `e0eebaa1`) |
| `custom_components/fujitsu_airstage/climate.py` | `async_set_hvac_mode`, `hvac_mode` | Auto-rallumage (baseline `81246d11`) ; mode dérivé de `get_operating_mode` |
| `custom_components/fujitsu_airstage/switch.py` | `AirstagePowerSwitch` | `switch.clim_power` dérivé de `get_device_on_off_state` |
| `custom_components/fujitsu_airstage/const.py` | `AIRSTAGE_SYNC_LOCAL_INTERVAL` | Intervalle de poll local (60 s) |
| `00_documentation_arsenal/contrats/climatisation/08_execution.md` | Stabilisation post-allumage | Justification contractuelle |
| `00_documentation_arsenal/contrats/climatisation/09_securite.md` | Retrait INV-3 (v1.5) | Phase normale d'allumage / non-atomicité |

**Commits de référence :** `5ce08c13` (création, 2 s) · `e0eebaa1` (durcissement
2 s → 10 s, v15.7.3) · `81246d11` (baseline intégration, auto-rallumage).

---

## 9. RENVOIS

- Diagnostic connexe (échec d'exécution) :
  [`diagnostic_clim_execution_echec.md`](diagnostic_clim_execution_echec.md)
- Investigation historique 30 j :
  [`investigation_historique_clim_30j.md`](investigation_historique_clim_30j.md)
- Contrat d'exécution :
  [`08_execution.md`](../../../contrats/climatisation/08_execution.md)
- Contrat de sécurité :
  [`09_securite.md`](../../../contrats/climatisation/09_securite.md)
