# Protocole de caractérisation terrain — C25 · Climatisation distante Audi

| Champ | Valeur |
|---|---|
| **Chantier** | [C25 — Climatisation distante Audi](chantier_commande_climatisation_distante.md). |
| **Nature** | **Protocole documentaire, lecture-guidée.** Exécution manuelle via **Outils de développement → Actions**. |
| **Exécutant** | L'opérateur. Il exécute les essais et remplit la trace (§6). |
| **Statut** | **Faisabilité DÉMONTRÉE (2026-07-21).** Succès terminal E1 confirmé (HA `cooling` + myAudi « Actif », corroboration physique SoC/autonomie). Restent E1b, E2–E5 et E6 pour caractériser périmètre, fin de cycle et refus. |
| **Sécurité** | Aucune dégradation artificielle, manipulation risquée ni panne simulée n'est demandée. |

> **Objectif.** Répondre par des preuves aux inconnues de C25 : le service fonctionne-t-il réellement sur
> ce véhicule, quels paramètres sont acceptés, quelles entités observent un démarrage réel, quelle
> latence, comment se manifeste un refus, et peut-on distinguer honnêtement refus / erreur / absence de
> confirmation. **Ce protocole ne transpose aucun modèle transactionnel et ne fige aucun statut terminal.**

---

## 0. Prérequis & rappels

- **Relever d'abord les `entity_id` runtime réels** avant tout essai : le device Audi, les capteurs
  `climatisation_state` et `remaining_climatisation_time`, et une entité brute stable de l'appareil.
  **Ne rien supposer** : ces identifiants sont des valeurs de registre (dette AUDI-11), pas des valeurs du
  dépôt.
- **Cibler le véhicule via le sélecteur d'appareil** de l'interface Actions (mode UI), sans manipuler
  d'identifiant opaque.
- **Un refus Audi est un résultat métier attendu**, pas un défaut de configuration Arsenal : il doit être
  observé et consigné honnêtement.
- **Un appel sans exception ne prouve rien** (l'intégration absorbe les erreurs). Toute conclusion de
  succès exige une **preuve indépendante de l'émission de l'appel**.

Squelette d'appel (illustratif — l'appareil se sélectionne dans l'interface ; ne pas coder d'identifiant
en dur) :

```yaml
action: audiconnect.start_climate_control
target:
  device_id: <Audi — sélectionner via le sélecteur d'appareil>
data:
  temp_c: 21
  climatisation_mode: comfort
  seat_fl: false
  seat_fr: false
  seat_rl: false
  seat_rr: false
  glass_heating: false
  climatisation_at_unlock: false
```

---

## 1. Relevés à consigner (chaque essai)

Pour **chaque** essai, consigner :

- les `entity_id` runtime exacts observés ;
- l'état initial des entités d'observation ;
- les attributs utiles ;
- l'heure d'émission de l'appel ;
- l'heure de la première transition observable ;
- le résultat dans Home Assistant ;
- le résultat dans myAudi ;
- le constat physique sur le véhicule, si possible ;
- le **niveau de preuve** (voir ci-dessous) ;
- le verdict.

### Niveau de preuve (obligatoire)

Chaque essai porte un niveau de preuve parmi :

- `HA seulement` ;
- `HA + myAudi` ;
- `HA + constat véhicule` ;
- `non confirmé`.

> **Règle de verdict.** Le verdict ne doit **jamais** être « conforme » sur la seule absence d'erreur dans
> Outils de développement. `HA seulement` **n'établit pas** un succès terminal.

---

## 2. Essai E1 — minimal

**Paramètres :** `temp_c` (ex. 21) + `climatisation_mode: comfort` + **tous les booléens à `false`**
(`seat_fl`, `seat_fr`, `seat_rl`, `seat_rr`, `glass_heating`, `climatisation_at_unlock`).

**Question :** le service **démarre-t-il réellement** la climatisation ?

**Succès minimal E1 — exige une preuve indépendante de l'émission de l'appel**, par exemple :

- une transition **crédible** de `climatisation_state` ;
- un `remaining_climatisation_time` **cohérent** ;
- une confirmation **myAudi** ;
- ou un **constat physique** sur le véhicule.

En l'absence d'au moins une de ces preuves, le verdict reste `non confirmé` — jamais « conforme ».

---

## 2 bis. Essai E1b — fin de cycle et retour à l'état initial

Après E1, observer la **fin du cycle nominal** (peut être fusionné avec E1 ou traité séparément).
Relever si possible :

- la **durée annoncée** du cycle ;
- l'**évolution** de `remaining_climatisation_time` ;
- le **retour** de `climatisation_state` à l'état inactif ;
- le **délai** de ce retour ;
- le **comportement lorsque la climatisation s'arrête naturellement** ;
- l'**existence éventuelle d'une commande d'arrêt** — **sans l'utiliser** tant qu'elle n'a pas été
  auditée.

> E1b **n'élargit pas** le chantier à une commande d'arrêt : il se limite à **observer** la fin de cycle
> et à **consigner** l'existence d'un éventuel arrêt, sans l'exercer.

---

## 3. Essais d'options — un par un (jamais groupés)

Ne regrouper **aucune** capacité non encore validée dans un même essai.

- **E2 — mode `economy`** : `temp_c` + `climatisation_mode: economy`, booléens `false`.
- **E3 — siège avant gauche** : ajouter `seat_fl: true` (le reste `false`).
- **E4 — siège avant droit** : ajouter `seat_fr: true` (le reste `false`).
- **E5 — climatisation à l'ouverture** : ajouter `climatisation_at_unlock: true`.

### Prudence spécifique sièges chauffants (E3, E4)

Distinguer **deux questions séparées**, et les consigner distinctement :

1. le backend **accepte-t-il le paramètre** sans erreur visible ?
2. le chauffage du siège est-il **réellement observable ou vérifiable** sur ce véhicule (entité dédiée,
   confirmation myAudi, ou constat physique) ?

> **L'absence de preuve physique ou d'entité dédiée ne vaut pas validation de la capacité.** Un appel sans
> exception est insuffisant, **y compris pour les options** : sans preuve indépendante, le niveau de
> preuve reste `non confirmé`.

---

## 4. Essai E6 — état naturellement incompatible

**Ne provoquer aucun état incompatible.** Exécuter l'essai **lorsqu'un état naturellement incompatible,
connu et sans risque, est disponible** — par exemple lorsque le véhicule **n'est pas branché** ou lorsque
ses **conditions habituelles de climatisation distante ne sont pas réunies**.

**Objectif :** caractériser un **refus réel**, pas fabriquer une panne. Observer **comment se manifeste le
refus**, **sans présumer** que Home Assistant exposera le motif.

---

## 5. Grille d'interprétation honnête

Distinguer trois niveaux, qui ne se confondent pas :

1. **acceptation de l'appel Home Assistant** (aucune exception) — **ne prouve rien** ;
2. **acceptation par le backend Audi** ;
3. **succès terminal de l'action véhicule** (climatisation réellement démarrée).

Consigner, à la lumière des essais, si un statut du type **`not_confirmed` / `timeout`** est plus honnête
qu'un `rejected` — l'intégration **ne semble pas** exposer le motif d'un refus (à confirmer par E6).
**Aucun statut n'est acquis avant le terrain.**

---

## 6. Trace terrain (à remplir par l'opérateur)

| Essai | `entity_id` observés | État initial | Attributs utiles | Heure émission | Heure 1ʳᵉ transition | Résultat HA | Résultat myAudi | Constat véhicule | Niveau de preuve | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 — minimal | `sensor.audi_e_tron_etat_de_charge_local`, `sensor.audi_e_tron_autonomie_local` (`binary_sensor.*_plug_state` **non historisé**) | Branché (**constat opérateur**) ; `chargePurposeReachedAndNotConservationCharging` depuis 18:36:40 | autonomie **29,0 km** | **2026-07-20 18:43:54** | **aucune** | `ERROR audiconnect` — `Cannot startClimatisation, return code 'failed'` ; **motif non exposé** (exception `audi_services.py:990`) | **Échec ~18:45** — `E.PA.VCF.UND.fail_vehicle_timeout` | non relevé | **HA + myAudi** | **Non confirmé — timeout véhicule** ; ni succès terminal, ni refus fonctionnel |
| **E1 — minimal (reprise 2026-07-21)** | « Climatisation state » (device Audi ; `entity_id` runtime exact **non capturé** à l'écran) ; télémétrie SoC / autonomie myAudi | échec 09:48 : **branché, en charge**, 64 %, 21 km → succès observé **débranché** (HA `notReadyForCharging`), 41 %, 12 km | config **minimale** : `temp_c 21`, `comfort`, tous booléens `false` (capture 11:06) ; un appel ultérieur `climatisation_at_unlock: true` **composé** (12:33, résultat non capturé) | **non capturée** (entre 09:51 et 10:44) | **≤ 10:44** (myAudi « Actif ») / **10:49** (HA `cooling`) | `climatisation_state = **cooling**` (10:49) | **Climatiseur « Actif »** (10:44) ; échec antérieur **09:48** `E.PA.VCF.UND.fail_vehicle_timeout (2607210948)` | **Chute SoC 64 %→41 % + autonomie 21→12 km en ~50 min**, cohérente avec une clim stationnaire sur batterie | **HA + myAudi** (+ corroboration physique) | **Succès terminal CONFIRMÉ** — la climatisation a réellement démarré |
| E1b — fin de cycle | | | | | | | | | | |
| E2 — mode economy | | | | | | | | | | |
| E3 — siège avant gauche | | | | | | | | | | |
| E4 — siège avant droit | | | | | | | | | | |
| E5 — clim à l'ouverture | | | | | | | | | | |
| E6 — état incompatible | | | | | | | | | | |

> **Essai E1 du 2026-07-20, consigné le 2026-07-21 — premier essai terrain de C25.**
>
> **Le motif est exposé par le backend, perdu par l'intégration.** myAudi renvoie
> `fail_vehicle_timeout` ; `audiconnect` ne remonte qu'un `return code 'failed'` générique.
> L'hypothèse du §5 est **confirmée** : l'intégration n'expose pas le motif, alors que le backend le
> fournit.
>
> **Le statut honnête est `timeout`, non `rejected`** — exactement ce que le §5 anticipait. Un timeout
> véhicule n'est **ni un succès terminal, ni un refus fonctionnel** : la faisabilité de la fonction
> n'est **pas invalidée** par cet essai.
>
> **Conditions favorables.** Véhicule branché, charge à l'objectif, 29 km d'autonomie. Les hypothèses
> « non branché » et « batterie insuffisante » sont **écartées**.
>
> **Limite de la trace.** `binary_sensor.audi_a3_sportback_e_tron_plug_state` **n'est pas historisé**
> (hors allowlist Recorder) : l'état de branchement n'est pas reconstituable *a posteriori* et repose
> ici sur le **constat opérateur**. La bascule de l'état de charge à `notReadyForCharging` (18:59:05)
> situe le débranchement **après** l'essai.
>
> **Reste à établir** : E1b, E2–E5, et surtout **E6** (état naturellement incompatible), seul essai
> capable de dire si un refus *fonctionnel* se distingue d'un *timeout* dans la remontée.

> **Reprise E1 du 2026-07-21 — faisabilité DÉMONTRÉE.**
>
> **Le niveau 3 de la grille §5 (succès terminal de l'action véhicule) est atteint.** La climatisation
> a **réellement démarré** : `climatisation_state = cooling` en HA (10:49) **et** Climatiseur « Actif »
> dans myAudi (10:44), avec une **corroboration physique indépendante** — la charge est passée de
> **64 % à 41 %** et l'autonomie de **21 à 12 km en ~50 min**, cohérent avec une climatisation
> stationnaire alimentée par la batterie (l'intégration émet `climatisationWithoutHVpower/…WithoutExternalPower: True`).
> La question centrale de E1 (« le service démarre-t-il réellement ? ») est donc tranchée **OUI**, avec
> le **jeu de paramètres minimal** (`temp_c 21`, `comfort`, tous booléens `false`).
>
> **L'intermittence est confirmée et reste d'origine backend.** Le **même matin**, un essai a échoué à
> **09:48** sur le **même** `E.PA.VCF.UND.fail_vehicle_timeout (2607210948)` que E1 la veille, avant que
> les essais suivants n'aboutissent. Un timeout véhicule est donc un **état transitoire**, non une
> incompatibilité de la fonction : la répétition finit par réussir. Ceci **confirme** l'expérience
> opérateur (« Audi capricieux »).
>
> **Piste, non établie (n=1).** L'échec 09:48 est survenu **en charge**, le succès véhicule
> **débranché** (`notReadyForCharging` en HA à 10:49). Une éventuelle corrélation « démarrage refusé
> pendant une session de charge active » est **une hypothèse, pas un fait** — un seul couple
> d'observations, et l'ordre temporel (répétition) suffit à l'expliquer. À ne pas ériger en règle.
>
> **Périmètre de preuve.** L'opérateur rapporte **3 essais concluants** ce matin ; **un seul** est
> étayé par capture indépendante (HA + myAudi ci-dessus), les **deux autres** restent au niveau de
> preuve **opérateur**. Un appel `climatisation_at_unlock: true` a été **composé** à 12:33 (proche de
> E5) mais son **résultat n'est pas capturé** — E5 reste donc **à confirmer**.
>
> **Lecture §5 inchangée sur la remontée.** L'échec 09:48 n'apparaît toujours, côté HA, que comme un
> `failed` générique tandis que myAudi porte le code `fail_vehicle_timeout` : le motif reste **exposé
> par le backend et perdu par l'intégration**. Le statut honnête d'un échec demeure `timeout`, non
> `rejected`.

### Chaîne de détection — vérifiée dans le code vendorisé (2026-07-21)

Vérification directe du code de l'intégration (le dépôt fait foi) :

- **Origine de `climatisation_state`** : valeur **brute renvoyée par le véhicule**, extraite de
  l'endpoint `climater` (chemin MBB, celui réparé avec le scope `mbb`) —
  `custom_components/audiconnect/audi_connect_account.py:906-908`
  (`get_attr(..., "climater.status.climatisationStatusData.climatisationState.content")`). Ce n'est
  **pas** un état calculé par HA : c'est un **témoin côté véhicule**, indépendant de la commande.
  `remaining_climatisation_time` a la même origine (`:923`).
- **Rafraîchissement post-action garanti (succès ET échec)** : `AudiConnectAccount.start_climate_control`
  place la notification de rafraîchissement dans un **`finally`** (`audi_connect_account.py:451-453` →
  `notify(vin, ACTION_CLIMATISATION)`) — le refresh a donc lieu **quel que soit l'aboutissement**. Le
  handler `handle_notification` (`audi_account.py:247-257`) attend **`update_sleep` = 5 s par défaut**
  (`const.py:28`, configurable ; immédiat si l'option `refresh_after_action`) puis déclenche un **refresh
  dédié** (pas l'intervalle de scan).
- **Conséquence** : ~5 s après la commande, `climatisation_state` reflète ce que la voiture rapporte
  réellement — y compris en cas d'échec. Fenêtre courte et prévisible : c'est exactement le témoin
  recherché par INV-CMD-1. *(Le `refresh_vehicle_data` explicite du script devient de ce fait un filet
  redondant mais inoffensif.)*

### Ce qui reste pour verrouiller C25 — mesure, pas code (opérateur)

1. **Valeurs littérales avant → après** : le code **n'énumère pas** les états (chaînes brutes Audi) ;
   seule l'observation fait foi (ex. `off → cooling` / `heating` / `ventilation` / `on`…). À noter au
   littéral.
2. **Latence réelle** : 5 s (`update_sleep`) + temps du refresh + temps de remontée véhicule.
   Chronométrer *commande → changement d'état* pour fixer le **timeout à retenir (avec marge)** ; la
   fenêtre runtime actuelle (~3 min) est large, à confirmer ou resserrer.
3. **Comportement en échec = essai E6** : en état naturellement incompatible (véhicule non branché,
   comme l'essai raté du 2026-07-20), `climatisation_state` **reste-t-il inchangé** ? **Si oui →
   discriminant fiable** (le détecteur est valide). **S'il bouge aussi → basculer sur un autre témoin**
   (`remaining_climatisation_time`). C'est l'essai **E6** du protocole, à moitié réalisé involontairement
   lors du premier test raté — à refaire en notant l'état avant/après.

---

## 7. Décision différée

À la lumière de la trace §6, l'opérateur et l'assistant statueront sur :

- si le chantier mérite une implémentation ;
- quel périmètre fonctionnel est **réellement supporté** ;
- si un contrat de commande est justifié ;
- si une architecture transactionnelle complète est nécessaire ;
- ou si une **solution beaucoup plus simple** suffit.

**Aucune de ces décisions n'est prise avant que la trace §6 ne soit remplie.**

---

## 8. Renvois

- Chantier : [`chantier_commande_climatisation_distante.md`](chantier_commande_climatisation_distante.md).
- Contrat du domaine : [`contrats/voiture.md`](../../../contrats/voiture.md).
- Audit du domaine : [`audits/01_rapports/voiture/audit_domaine_audi.md`](../../01_rapports/voiture/audit_domaine_audi.md).
