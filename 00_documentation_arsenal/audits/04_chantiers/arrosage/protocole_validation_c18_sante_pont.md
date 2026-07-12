# Protocole de validation terrain — C18 Lot 4 (santé pont Rain Bird)

| Champ | Valeur |
|---|---|
| **Chantier** | **C18** — Rain Bird : sémantique de santé du pont |
| **Lot** | **Lot 4** — validation terrain du verdict corrigé (Lot 3 mergé, #346) |
| **Statut** | **Protocole prêt à exécuter — trace §6 à remplir par l'opérateur.** C18 **non clôturé** ; **aucune** preuve terrain affirmée tant que la trace n'est pas remplie. |
| **Dossier de chantier** | [`chantier_semantique_sante_pont_rain_bird.md`](chantier_semantique_sante_pont_rain_bird.md) |
| **Runtime concerné** | [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml) · contrat [`03`](../../../contrats/arrosage/03_coexistence_rainbird.md) §6.2 |

> **Nature de ce document.** Protocole **traçable** : il **prépare** la validation terrain,
> **ne modifie aucun runtime** et **ne clôture rien**. Il est **directement exécutable** sur
> l'installation réelle, **sûr et réversible**, et **limité** aux preuves nécessaires à la
> clôture de C18. Tant que la **trace §6** n'est pas remplie, **aucune** preuve terrain n'est
> réputée acquise.

---

## 1. Règles de sûreté (impératives)

- **Aucune panne artificielle.** Ne PAS forcer `off` sur les binaires du pont, ne PAS couper
  MQTT / Wi-Fi / BLE, ne PAS arrêter le pont ni retirer les piles pour « voir » `degrade` /
  `indisponible`.
- **Lecture seule.** N'utiliser que : **Outils de développement → États**, **→ Modèle**
  (rendu sans écriture), et **Historique / Recorder** (consultation).
- **Réversible.** Un **rechargement de configuration** (Paramètres → YAML → *Recharger les
  entités template*) ou un **redémarrage HA** est une action d'exploitation **normale et
  réversible** — c'est le seul « déclenchement » autorisé, et il est **nécessaire** pour que
  le runtime mergé (#346) soit chargé.
- **Non-reproductibilité admise.** Si l'historique ne fournit pas d'épisode réel de `degrade`
  / `indisponible`, ces transitions sont **déclarées non vérifiables sans action intrusive**
  (§4/§6) — **jamais** simulées.

---

## 2. Ce qui est DÉJÀ acquis (validations statiques — ne pas refaire)

| Réf | Preuve statique acquise (depuis le dépôt) |
|---|---|
| **V1** | **Non-régression prouvée** : `sensor.rain_bird_pont_sante` n'est lu par **aucune** garde / intention / exécution / notification déclenchante (seuls consommateurs : UI, recorder, une ligne de texte de notification). → Le changement **ne peut pas** régresser l'arrosage. |
| **V2** | **Chargement config valide** : includes résolus (`check_configuration_includes` PASS). |
| **V3** | **Logique des 4 états validée** (table de vérité) : `inconnu`/`indisponible`/`degrade`/`ok` ; cas `dispo=on, frais=on, RSSI -76 → ok`. |
| **V4** | **Verrou anti-régression vert** : `check_resilience_integrations_contracts.py --selftest` + `✔ C18-pont-sante`. |

Le Lot 4 se concentre donc **uniquement** sur la confirmation **live** de ces déductions.

---

## 3. Prérequis d'exécution

1. La configuration mergée (#346) est **chargée** : *Paramètres → Modules → YAML → Recharger
   les entités template*, **ou** redémarrage HA. (Réversible ; standard.)
2. Se placer dans **Outils de développement**.

---

## 4. Tests

### T1 — Nominal `ok` (preuve principale)

- **Outils de développement → États**, lire :
  - `sensor.rain_bird_pont_sante` → **attendu `ok`** ;
  - `binary_sensor.rain_bird_pont_donnees_disponibles` → attendu `on` ;
  - `binary_sensor.rain_bird_pont_donnees_fraiches` → attendu `on` ;
  - `sensor.rain_bird_bat_bt_2_e9a3_bridge_wifi_rssi` et `…_ble_rssi` → **noter la valeur**
    (attendu ~-76 dBm : démontre que le RSSI **n'affecte plus** la santé) ;
  - attributs de `sensor.rain_bird_pont_sante` → `wifi_rssi` / `ble_rssi` **toujours exposés**
    (diagnostic préservé).
- **Type de preuve : observation terrain (live).**

### T2 — Rendu logique (renfort facultatif de T1)

- **Outils de développement → Modèle**, coller et vérifier que le rendu = `ok` :
  ```jinja
  {% set indispo = ['unknown', 'unavailable', 'none', 'None', ''] %}
  {% set dispo = states('binary_sensor.rain_bird_pont_donnees_disponibles') %}
  {% set frais = states('binary_sensor.rain_bird_pont_donnees_fraiches') %}
  {% if dispo in indispo %}inconnu{% elif dispo != 'on' %}indisponible{% elif frais != 'on' %}degrade{% else %}ok{% endif %}
  ```
- **Type de preuve : observation terrain (rendu).**

### T3 — `degrade` (perte de fraîcheur) — **par historique uniquement**

- **Historique** de `binary_sensor.rain_bird_pont_donnees_fraiches` : chercher un épisode réel
  `off` (le firmware manque parfois des cycles ~1 h). Sur cet intervalle, vérifier que
  `sensor.rain_bird_pont_sante` valait **`degrade`**.
- **Si aucun épisode** dans l'historique disponible → **non vérifiable sans action intrusive**
  (ne rien provoquer). Noter la limite.
- **Type de preuve : historique** (si disponible) **sinon : non vérifiable**.

### T4 — `indisponible` (données cœur absentes) — **par historique uniquement**

- **Historique** de `binary_sensor.rain_bird_pont_donnees_disponibles` : chercher un épisode
  réel `off` (ex. reboot pont, coupure MQTT). Sur cet intervalle, vérifier que
  `sensor.rain_bird_pont_sante` valait **`indisponible`**.
- **Si aucun épisode** → **non vérifiable sans action intrusive**. Noter la limite.
- **Type de preuve : historique** (si disponible) **sinon : non vérifiable**.

### T5 — Non-régression arrosage (contrôle live de confirmation)

- **Outils de développement → États**, vérifier l'état **cohérent et inchangé** de :
  - `binary_sensor.arrosage_rain_bird_preconditions_runtime` (garde runtime) ;
  - `binary_sensor.arrosage_intention` + attributs `motif` / `categorie` ;
  - `sensor.arrosage_dernier_effectif`.
- Aucune de ces entités ne doit avoir changé de comportement **du fait** de la nouvelle valeur
  de `pont_sante` (rappel **V1** : elles ne le lisent pas).
- **Type de preuve : observation terrain (live) + rappel V1 (statique acquise).**

---

## 5. Correspondance avec la clôture

- **T1 réussi** ⇒ **réserve principale levée** ⇒ clôture **définitive** de C18 possible
  (mise à jour de registre : passage en ⑤ Clos récents).
- **T3 / T4** : **suivi opportuniste non bloquant** (logique prouvée V3, verdict non-gating
  V1). Leur absence de preuve historique **ne bloque pas** la clôture ; elle est **documentée**
  comme limite.
- **T5** confirme en live la non-régression déjà prouvée (V1).

---

## 6. Trace (à remplir par l'opérateur)

> Classer chaque ligne dans **un seul** type de preuve : **terrain (live)** · **historique**
> · **statique acquise** · **non vérifiable sans intrusion**.

| Test | Entité(s) | Attendu | Observé | Type de preuve | Verdict (PASS / N/A / limite) |
|---|---|---|---|---|---|
| **T1** nominal | `sensor.rain_bird_pont_sante` (+ dispo/frais/RSSI) | `ok`, dispo/frais `on`, RSSI ~-76 | _à remplir_ | terrain (live) | _à remplir_ |
| **T2** rendu | Modèle (bloc state) | `ok` | _à remplir_ | terrain (rendu) | _à remplir_ |
| **T3** degrade | histo `pont_donnees_fraiches` → `pont_sante` | `degrade` sur épisode `off` | _à remplir_ | historique / non vérifiable | _à remplir_ |
| **T4** indispo | histo `pont_donnees_disponibles` → `pont_sante` | `indisponible` sur épisode `off` | _à remplir_ | historique / non vérifiable | _à remplir_ |
| **T5** non-régression | `preconditions_runtime`, `arrosage_intention` (motif/categorie), `dernier_effectif` | inchangés / cohérents | _à remplir_ | terrain (live) + V1 | _à remplir_ |

> **Tant que cette trace n'est pas remplie et arbitrée, C18 reste `Actif` (non clôturé) et
> aucune preuve terrain n'est affirmée.**

---

## Renvois

- Dossier de chantier : [`chantier_semantique_sante_pont_rain_bird.md`](chantier_semantique_sante_pont_rain_bird.md)
- Rapport d'audit : [`audit_rain_bird_sante_pont_qualite_radio.md`](../../01_rapports/arrosage/audit_rain_bird_sante_pont_qualite_radio.md)
- Contrat (autorité santé, §6.2) : [`03_coexistence_rainbird.md`](../../../contrats/arrosage/03_coexistence_rainbird.md)
- Runtime corrigé : [`pont_sante.yaml`](../../../../12_template_sensors/arrosage/pont_sante.yaml)
- Registre : [`REGISTRE_CHANTIERS.md`](../../REGISTRE_CHANTIERS.md)
