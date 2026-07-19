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
   live aux heures concernées.
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
