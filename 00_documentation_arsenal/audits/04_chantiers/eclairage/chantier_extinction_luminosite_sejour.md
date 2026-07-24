# Chantier C22 — Éclairage séjour : extinction sur luminosité réelle

**Domaine :** éclairage — séjour
**Statut :** runtime livré (PR #368, mergé 2026-07-15) — **validation terrain en attente**
**Contrat de référence :** [`eclairage/sejour.md`](../../../contrats/eclairage/sejour.md) (v1.1.0)
**Actionneur unique :** `switch.prise_lampe_sejour`

> Chantier issu d'une observation utilisateur, pas d'un audit de domaine.
> Livraison ciblée qui **comble un angle mort** sans refonte du domaine.
> **Un seul changement de comportement**, désactivé par défaut.

---

## 1. Problème — angle mort de l'extinction

Le séjour ne disposait que d'**un seul axe d'extinction : l'absence**.

- Allumage `10070000000014` : sur mouvement, **si `sensor.periode_meteo ∈ {crepuscule, nuit, aube}`** (période sombre).
- Extinction `10070000000015` : uniquement lorsque la **deadline d'absence** est atteinte (mouvement `off`).

Conséquence : en **présence continue**, une lampe allumée pendant une période
sombre **reste allumée même en plein jour**, l'éclairage devenant inutile.
Le cycle nominal n'a aucun moyen de l'éteindre tant que quelqu'un est présent.

`sensor.periode_meteo` est **astronomique / saisonnier**, pas une mesure de
lumière réelle : à midi il est « jour » aussi bien sous un ciel couvert d'hiver
que plein soleil d'été, alors que la luminosité diffère d'un facteur ~100.
Le bon signal pour « l'éclairage est-il inutile ? » est la **lumière réelle**.

---

## 2. Décision de conception (arbitrage propriétaire)

**Capteur retenu :** `sensor.luminosite_garage_illuminance` — **unique capteur de
luminosité de l'installation**, déjà employé comme autorité par le domaine
garage (`binary_sensor.garage_allumage_auto_autorise`). Réutilisé ici comme
**proxy d'ambiance** pour le séjour.

**Option retenue — « garder période + extinction lux » :** l'allumage reste
inchangé (piloté par `periode_meteo`) ; on ajoute **uniquement** une extinction
sur **seuil lux unique**.

Options écartées :

| Option | Écartée car |
|--------|-------------|
| Tout passer au lux, **2 seuils** (hystérésis allumage/extinction) | crée une **bande morte** entre les deux seuils que le **bandeau d'autorisation binaire** (motif garage) ne sait pas représenter ⇒ casse l'UI d'autorisation. |
| Seuil unique + **anti-rebond temporel** (deadline persistée) | robuste, mais ajoute une causalité temporelle superflue ici (voir §2 bis). |

### 2 bis. Pourquoi pas d'hystérésis

Le besoin d'hystérésis n'existe que si **allumage ET extinction** sont pilotés
par le même seuil lux. Ici, **l'allumage reste période-gaté** : « période
sombre » et « forte luminosité » étant quasi mutuellement exclusifs, les deux
automations ne s'opposent pas en régime courant. De plus, l'allumage exige une
**transition** de `binary_sensor.mouvement_sejour` vers `on` : après une
extinction par luminosité, il ne se ré-arme pas tant que le mouvement reste
`on`. Le risque de battement est donc **négligeable, sans hystérésis dédiée**.

---

## 3. Périmètre livré — PR #368

- **Helper** `input_number.sejour_seuil_luminosite_extinction_auto` — seuil lux
  réglable (0–2000, pas 10). **Défaut 0 = fonctionnalité neutralisée** (défaut
  sûr, non intrusif tant que non calibré).
- **Autorité de décision** `binary_sensor.sejour_extinction_luminosite_autorisee` —
  `state = seuil > 0 ET luminosité réelle > seuil`. Ne pilote rien.
- **Automation `10070000000035`** « Éclairage - Séjour - Extinction luminosité » —
  éteint via `script.sejour_off` (autorité d'action canonique), avec rattrapage
  boot (90 s) / reload (10 s).
- **UI** — réglages éclairage : slider de seuil + tuile lecture-seule de
  l'autorisation, sous la section Séjour.
- **Contrat** `eclairage/sejour.md` v1.0.0 → **v1.1.0** (§2 diagramme, §3
  entités, **§6bis** dédié, §7 réécrit).
- **CI** — test **T13** ajouté à `check_eclairage_sejour_contracts.py`
  (présence, délégation `script.sejour_off`, pas de `turn_on`, pas d'écriture
  de deadline).

---

## 4. Conformité à la doctrine

- **Séparation décision / action / UI** : le `binary_sensor` **décide**,
  l'automation **applique** (via le script), l'UI **observe**.
- **I1 — actionneur unique** : extinction déléguée à `script.sejour_off`,
  aucun pilotage direct de `switch.prise_lampe_sejour`.
- **I2 — source de vérité unique** : lecture directe de l'état du switch,
  aucun état logique parallèle.
- **I3 — séparation allumage / extinction** : automation distincte et
  indépendante.
- **I5 — autorisation explicite** : `input_boolean.sejour_auto_light = on`
  vérifié au moment de l'action.
- **Aucun ID inventé** : `10070000000035` libre (préfixe `1007` = éclairage),
  unicité vérifiée ; toutes les entités référencées existent.

Checkers verts en local : `check_eclairage_sejour_contracts` (dont T13),
`check_03_input_numbers_contracts`, `check_automation_ids_contracts`,
`check_automation_prefix_domain_contracts`, `check_ci_coverage_registry`.

---

## 5. Validation terrain — en attente (condition de clôture)

C22 **ne se clôt pas** tant que ces points ne sont pas tranchés en réel :

1. **Qualité du proxy garage** (point dur) — le capteur est **physiquement dans
   le garage**. Il n'est un proxy fidèle de la luminosité du séjour **que s'il
   voit la lumière extérieure**. À confirmer par observation de la valeur lux
   live aux heures concernées. **✅ Soldé (2026-07-20)** — voir le relevé ci-dessous.
2. **Calibration du seuil** — relever la luminosité aux moments gênants, régler
   le seuil **au-dessus du niveau d'aube** et **sous celui du plein jour**.
   Tant que le seuil reste à 0, aucun changement de comportement.
3. **Non-régression allumage** — vérifier qu'une extinction par luminosité ne
   provoque pas de ré-allumage indésirable (attendu : non, car allumage
   période-gaté + transition de mouvement requise).

> **Instrumentation probatoire posée (2026-07-19).** Les points 1 et 2 exigent la
> **courbe lux jour/nuit**, or `sensor.luminosite_garage_illuminance` **n'était pas
> historisé** (absent de l'allowlist `recorder.yaml` — angle mort non anticipé ici).
> Un **microscope recorder** (Population B, dérogation fréquence présomptive) a été
> ajouté sur le modèle C20 ; cible d'analyse = **long-term statistics** (min/mean/max
> horaires, non purgées). **Retrait dès seuil calibré ET C22 clôturé.** La
> calibration attend l'accumulation de quelques cycles jour/nuit.

### 5 bis. Relevé de calibration (2026-07-20) — point 1 soldé, point 2 en cours

**Source** : `statistics` (LTS horaires) et `statistics_short_term` de
`sensor.luminosite_garage_illuminance`, lecture seule de la base recorder. Plage
**2026-07-19 18:00 → 2026-07-20 20:20** : 26 relevés horaires, 315 points 5 min.

**Point 1 — le capteur voit bien la lumière extérieure : soldé.** La courbe est une
signature solaire, bornée par deux repères indépendants : décollage du plancher à **06:35**
(lever du soleil **06:36**) et retour au plancher à **21:40** (coucher **21:41**). Le palier
nocturne est **plat à 1,0 lx sur ~9 h**, sans une seule excursion. **Arbitrage propriétaire
(2026-07-20)** : le garage est fenêtré et sensible à la luminosité extérieure ; l'éclairage
du séjour ne l'atteint pas. Le critère du point 1 est donc rempli.

**Point 2 — calibration : valeur de départ proposée `50` lx.** Régimes mesurés :

| Régime | Plage observée |
|---|---|
| nuit (21:40 → 06:35) | **1,0 lx** constant |
| aube | 06:35 décollage · 5 lx (07:00) · 20 lx (08:00) · 42-56 lx (09:00) |
| plein jour | 60 → 254 lx, **creux nuageux 33-43 lx** (11:00-11:35) |
| crépuscule | 44 lx (19:00) → 14 lx (20:15) |

**Limite structurelle relevée** : le creux nuageux de midi (min **33 lx**) **chevauche**
l'aube de 9 h (42-56 lx). Aucun seuil unique ne sépare proprement les deux régimes — c'est
une propriété du site, non un défaut du capteur. À `50`, l'autorisation s'établit vers
**09:05** puis retombe par intermittence sous les passages nuageux : sans conséquence
fonctionnelle (elle n'allume rien, le défaut est fail-safe).

**Le point 2 n'est pas soldé.** Un seul cycle jour/nuit, en juillet, sous une seule météo.
Le capteur suivant l'extérieur, un seuil calé en été sera **trop haut en hiver**. Laisser
accumuler quelques cycles de météo variée avant de figer. **Le helper reste à `0`
(désactivé) : aucun changement de comportement à ce stade.**

### 5 ter. Mise à jour de calibration (2026-07-24) — 5 cycles, météo variée

**Source** : base recorder fraîche `arsenal-runtime/snapshots/database/recorder_v17_0_3.db`
(hors dépôt gouverné), lecture seule. Plage **2026-07-19 → 2026-07-24**, 8 188 points de
`sensor.luminosite_garage_illuminance`. L'accumulation demandée par le §5bis est faite, la
météo variant bien : **ensoleillé** (07-21, pic **627 lx**) et **couverts** (07-22 / 07-24,
pics 254 / 179 lx ; **midi couvert du 07-22 descendu à 14 lx**).

| Jour | nuit | pic | aube 07-09h | midi 11-15h (min) |
|---|---|---|---|---|
| 07-20 | 1 | 310 | 6 → 106 | 33-310 (**33**) |
| 07-21 | 1 | **627** | 6 → 79 | 37-627 (37) |
| 07-22 | 1 | 254 | 5 → 49 | 14-153 (**14**) |
| 07-23 | 1 | 240 | 5 → 41 | 43-154 (43) |
| 07-24 | 2 | 179 | 5 → 42 | — |

**Constats.**
- **Plancher nuit stable** à 1-2 lx tous les jours ; borne basse nette.
- **Chevauchement aube ↔ midi nuageux confirmé et aggravé** : le 07-22 midi (14 lx) est plus
  sombre qu'une aube claire (49 lx) ⇒ **aucun seuil unique ne sépare** les deux régimes
  (propriété du site ; le §5bis relevait 33 lx, on descend à 14). **Sans conséquence** : le
  défaut est **fail-safe** — l'autorité ne fait qu'*autoriser l'extinction* ; sous le seuil
  elle retombe et **n'allume rien**.
- **Établissement matinal de l'autorité par seuil** (franchissement stable, 09-19 h) : **40 lx**
  ≈ 08:00 (couverture jour 92-100 %) · **50 lx** ≈ 08:09-09:05 (81-97 %) · **60 lx +**
  plus tardif et plus conservateur. Les « retombées » nuageuses sont fréquentes mais
  **fonctionnellement neutres** (fail-safe).

**Point 2 — provisoirement calibré (été).** Un **seuil d'été ≈ 50 lx** est **défendable sur
données** (5 cycles variés contre 1 au 07-20) : il établit l'autorité en milieu de matinée
tous les jours et retient légitimement l'autorité en régime couvert sombre. **Réserve
saisonnière maintenue** : données de **juillet seulement** — en hiver l'ambiance plus basse
rendra 50 lx rarement franchi (fonction peu active, **sans danger**, fail-safe) ; un seuil
d'hiver plus bas, ou l'acceptation d'un seuil « surtout actif l'été », **reste à trancher**.
**Le helper reste à `0` tant que l'activation n'est pas décidée (cf. §5 quater).**

### 5 quater. Protocole d'activation (point 3 — non-régression allumage)

> **Nature.** Procédure **opérateur** d'activation de l'extinction sur luminosité et de
> vérification de la **non-régression allumage** (point 3 du §5). L'activation **change le
> comportement runtime** ; le helper à `0` est l'état neutre de repli. **Aucune simulation,
> aucun forçage d'état** : on active la vraie fonction et on observe.

**Préconditions.**
- Séjour au repos ; **journée** (l'autorité ne s'établit qu'après ~08:00-09:00).
- `sensor.luminosite_garage_illuminance` alimenté (non `unavailable`) ;
  `binary_sensor.sejour_extinction_luminosite_autorisee` observable ; helper initial = `0`.

**Activation — service HA (jamais « Set State » : transitoire et écrasé).**
- Outils de développement → Actions : `input_number.set_value` sur
  `input_number.sejour_seuil_luminosite_extinction_auto`, **valeur `50`** (ou la valeur d'été
  retenue). L'autorité devient alors calculable (`seuil > 0`).

**Observations (sur quelques jours de météo variée).**
1. **Autorité** — `sejour_extinction_luminosite_autorisee` passe `on` en milieu de matinée
   quand `lux > seuil`, `off` la nuit et en régime couvert sombre. Cohérent avec la courbe §5ter.
2. **Extinction réelle** — autorité `on` **et** lampe séjour allumée en **présence + plein jour**
   (l'angle mort visé) ⇒ l'automation `10070000000035` délègue à `script.sejour_off` : la lampe
   s'éteint. Horodater.
3. **Non-régression (point 3, le cœur)** — après une extinction par luminosité, **vérifier
   l'absence de ré-allumage indésirable**. Attendu **non** : l'allumage est **période-gaté +
   transition de mouvement requise** (`sejour.md` §6bis/§7). Consigner tout ré-allumage dans
   les 5 min suivant une extinction luminosité.
4. **Fail-safe** — sous les passages nuageux, l'autorité retombe `off` **sans rien allumer**.

**Garde-fou / arrêt immédiat.** Boucle extinction ↔ ré-allumage, **ou** extinction non désirée
(présence, ambiance perçue sombre) ⇒ **repli** : `input_number.set_value` du helper à **`0`**
(désactive, comportement d'origine restauré instantanément).

**Clôture.** Quelques jours sans ré-allumage indésirable ⇒ **point 3 soldé**. Avec le point 1
(proxy ✅) et le point 2 (été provisoire), **C22 devient clôturable sous la seule réserve
hiver** — à **parquer** (réévaluation en saison froide) ou à lever par accumulation hivernale.

---

## 6. Risques résiduels / dettes

- **Proxy garage** — si le capteur ne suit pas l'ambiance du séjour, la
  fonctionnalité sera peu utile ; piste future : corréler avec un autre signal
  ou ajouter un capteur dédié séjour (hors périmètre de ce chantier).
- **Absence d'hystérésis** — assumée (cf. §2 bis) ; à ré-examiner **seulement**
  si un battement réel est observé au seuil.

---

## 7. Traçabilité

- **PR :** #368 « Éclairage séjour : extinction sur luminosité réelle » (squash, 2026-07-15).
- **Contrat :** [`eclairage/sejour.md`](../../../contrats/eclairage/sejour.md) v1.1.0 (§6bis, §7).
- **Runtime :** `input_number.sejour_seuil_luminosite_extinction_auto`,
  `binary_sensor.sejour_extinction_luminosite_autorisee`, automation `10070000000035`.
- **CI :** `check_eclairage_sejour_contracts.py` (T13).
