# 📜 Arsenal — Contrat Normatif

**Objet** : Synthèse de santé NAS Imprimerie
**Version** : 1.1
**Date** : 24 avril 2026
**Statut** : normatif
**Portée** : couche de **synthèse interprétative** consommant les signaux déjà exposés par Arsenal pour le site imprimerie

---

## 1. Position dans l'architecture Arsenal

Cette couche vient **après** :

- le contrat payload sonde (`contrat_monitoring_nas_distant_v1.md` v1.0) — acquisition
- le contrat chaîne d'observabilité (`contrat_monitoring_nas_distant.md` v1.0) — transport + santé de chaîne
- les sensors de mesure métier déjà exposés par HA — perception
- le contrat de décision stockage (`nas_stockage_decision.md` v1.0-durci) — décision locale

Elle vient **avant** :

- la couche de décision métier complémentaire (ex : reboot)
- la couche d'alerte / notification
- la couche UI / dashboard

Elle **ne remplace aucune** des couches ci-dessus. Elle en produit une **vue interprétative catégorisée**.

---

## 2. Responsabilités exactes

### 2.1 Ce que la couche de synthèse FAIT

- Consomme les signaux exposés par les couches amont.
- Produit une **classification catégorielle** de l'état du site selon plusieurs axes.
- Produit une **raison canonique** expliquant chaque défaut détecté.
- Expose une **priorité** quand plusieurs défauts coexistent.
- Expose la **vue par axe** (pas d'agrégat booléen unique).

### 2.2 Ce que la couche de synthèse NE FAIT PAS

- Aucune acquisition de donnée brute.
- Aucune émission MQTT.
- Aucune requête réseau, système, ou externe.
- Aucune action (service HA, notification, appel).
- Aucune correction ou lissage de donnée source.
- Aucune logique UI (pas de couleur, pas d'icône conditionnelle, pas de markdown).
- Aucun seuil d'alerte (c'est le rôle de la couche décision, séparée).
- Aucune dépendance vers des entités non listées en section 4.
- Aucun renommage des sensors existants.
- Aucun `unique_id` inventé sans validation préalable.

---

## 3. Frontières strictes

| Couche | Responsabilité | Exemple typique |
|---|---|---|
| Acquisition | mesurer et exposer | `nas_probe.py` remplit `vol_free_pct` |
| Perception (MQTT raw + mesures) | structurer en entités HA | `sensor.nas_imprimerie_free_space_percent` |
| Décision locale | classifier une mesure en enum | `sensor.nas_imprimerie_stockage_etat` |
| **Synthèse (ce contrat)** | **interpréter, prioriser, expliquer globalement** | `sensor.nas_imprimerie_sante_synthese` |
| Décision métier complémentaire | `binary_sensor` par seuil (ex : reboot) | à venir |
| Alerte | notifier sur décision | automation → Telegram / push |
| UI | afficher l'état | Lovelace / cartes |

La synthèse **lit** les couches amont. Elle n'en altère aucune.
Les couches aval **lisent** la synthèse. Elles ne lui demandent rien.

---

## 4. Entrées autorisées

La couche de synthèse peut lire **exclusivement** les entités ci-dessous.
Toute autre lecture est interdite par ce contrat.

### 4.1 Santé de chaîne (3 axes orthogonaux)

- `sensor.nas_imprimerie_sonde_age`
- `sensor.nas_imprimerie_transport_age`
- `sensor.nas_imprimerie_republisher_age`

### 4.2 Connectivité agrégée chaîne

- `binary_sensor.nas_imprimerie_connectivite`

### 4.3 Mesures métier

- `sensor.nas_imprimerie_vpn`
- `sensor.nas_imprimerie_last_emit_age`

> Les sensors `sensor.nas_imprimerie_uptime`, `sensor.nas_imprimerie_free_space` et `sensor.nas_imprimerie_free_space_percent` existent dans Arsenal mais **ne sont pas lus par la synthèse**. L'axe stockage passe désormais par la décision locale (§4.5). L'axe uptime reste à `unknown` tant qu'aucun `binary_sensor` de décision reboot n'existe.

### 4.4 UPS

- `sensor.nas_imprimerie_ups_status`
- `binary_sensor.nas_imprimerie_ups_sur_batterie`

### 4.5 Décisions métier locales

- `sensor.nas_imprimerie_stockage_etat` — produit par le contrat `nas_stockage_decision.md v1.0-durci`

### 4.6 Attributs JSON de la source de vérité brute

- `sensor.nas_imprimerie_raw` (attributs uniquement, pas d'état)
- `sensor.nas_imprimerie_republisher_heartbeat_raw` (attribut `last_publish_action` uniquement, pour diagnostic)

Toute nouvelle entrée DOIT faire l'objet d'une révision explicite de ce contrat (v1.2+).

---

## 5. Sorties à créer

### 5.1 Entité principale de synthèse

**ID logique** : `sensor.nas_imprimerie_sante_synthese`

- `state` : valeur unique issue d'une **enum canonique fermée** (section 7).
- `availability` : faux si **aucune** des entrées de section 4 n'est exploitable. Vrai sinon.
- `attributes` :
  - `axe_connectivite` : sous-état (section 7.2)
  - `axe_vpn` : sous-état (section 7.3)
  - `axe_ups` : sous-état (section 7.4)
  - `axe_stockage` : sous-état (section 7.5)
  - `axe_uptime` : sous-état (section 7.6)
  - `raison` : raison canonique du `state` (section 8)
  - `priorite_active` : rang de priorité du défaut dominant (section 9)
  - `defauts_actifs` : liste ordonnée des axes en défaut, du plus prioritaire au moins prioritaire

### 5.2 Contraintes sur l'état

- `state` est **toujours** un des codes canoniques de section 7.1. Jamais de texte libre, jamais de `null` quand l'entité est disponible.
- `state` ne DOIT PAS être un booléen ou une couleur.
- `state` ne DOIT PAS masquer les sous-états : les 5 `axe_*` restent lisibles indépendamment dans les attributs.

---

## 6. Paramètres normatifs de fraîcheur (cadence 60 s)

Adaptés à la cadence réelle sonde = republisher = 60 s.

| Signal | Seuil nominal | Seuil alerte | Seuil critique | Unité |
|---|---|---|---|---|
| `nas_imprimerie_sonde_age` | < 120 | 120–300 | > 300 | secondes |
| `nas_imprimerie_transport_age` | < 120 | 120–300 | > 300 | secondes |
| `nas_imprimerie_republisher_age` | < 120 | 120–180 | > 180 | secondes |

**Justifications** :

- Sonde et transport : cadence 60 s, tolérance à un cycle raté (120 s), alerte à deux cycles, critique au-delà de cinq cycles ratés.
- Republisher : sa fraîcheur dépend uniquement de l'ordonnanceur DSM local, donc tolérance plus serrée (un cycle + marge). Un `republisher_age > 180 s` signale quasi certainement un problème republisher local, pas un problème chaîne.

Ces seuils sont **internes à ce contrat**. Ils ne modifient pas les seuils de santé brute de chaîne définis par le contrat chaîne v1.0.

---

## 7. États possibles

### 7.1 Enum canonique du `state` de synthèse

| Code | Signification |
|---|---|
| `ok` | tous les axes sont en état nominal |
| `degraded` | au moins un axe est en état d'alerte, aucun n'est critique |
| `critical` | au moins un axe est en état critique |
| `offline` | la chaîne elle-même est rompue : synthèse ne peut statuer sur le site |
| `unknown` | au moins une entrée indispensable est `unavailable` et empêche la classification |

**Règle de non-masquage** : `state` reflète le **pire** sous-état parmi les axes, selon la hiérarchie `offline > critical > unknown > degraded > ok`.

`offline` prime sur `critical` parce que si la chaîne est morte, on ne peut pas affirmer que les mesures métier sont à jour. Préférer honnêtement admettre l'ignorance plutôt que propager un `critical` basé sur des données figées.

### 7.2 Axe `connectivite`

Dérivé des 3 signaux de chaîne + `binary_sensor.nas_imprimerie_connectivite`.

| État | Condition |
|---|---|
| `ok` | les 3 âges chaîne sous seuil nominal ET connectivité `on` |
| `degraded` | au moins un âge en zone alerte, connectivité encore `on` |
| `critical` | au moins un âge > seuil critique OU connectivité `off` |
| `unknown` | l'une des entrées de chaîne est `unavailable` |

### 7.3 Axe `vpn`

Dérivé de `sensor.nas_imprimerie_vpn` (enum `CONNECTED / DISCONNECTED / ERROR`).

| État | Condition |
|---|---|
| `ok` | `CONNECTED` |
| `critical` | `DISCONNECTED` ou `ERROR` |
| `unknown` | `unavailable` ou hors enum |

Pas de palier `degraded` : le VPN est binaire par nature côté Arsenal.

### 7.4 Axe `ups`

Dérivé de `sensor.nas_imprimerie_ups_status` et `binary_sensor.nas_imprimerie_ups_sur_batterie`.

**Enum réellement produite par le pipeline actuel** :

- `ONLINE` — secteur présent, UPS fonctionnel
- `ON_BATTERY` — secteur coupé
- `LOW_BATTERY` — optionnel, seulement si un jour exposé par la sonde
- `OFF` — optionnel, seulement si un jour exposé par la sonde

| État | Condition |
|---|---|
| `ok` | `ONLINE` |
| `degraded` | `ON_BATTERY` (sur batterie, batterie non basse) |
| `critical` | `LOW_BATTERY` ou `OFF` |
| `unknown` | `unavailable` ou hors enum ou `null` |

> **Note de cohérence contractuelle** : le contrat payload v1.0 (`contrat_monitoring_nas_distant_v1.md`) déclare l'enum `OL / OB / LB / OFF`. Le pipeline actuel produit `ONLINE / ON_BATTERY`. Cette divergence devra être résolue soit par une révision v1.1 du contrat payload, soit par un alignement du code de la sonde. La synthèse consomme ce que la chaîne produit réellement à ce jour.

### 7.5 Axe `stockage` (ACTIF en v1.1)

Dérivé **exclusivement** de `sensor.nas_imprimerie_stockage_etat`, produit par le contrat `nas_stockage_decision.md v1.0-durci`.

| Valeur source (`stockage_etat`) | `axe_stockage` |
|---|---|
| `ok` | `ok` |
| `bas` | `degraded` |
| `critique` | `critical` |
| `unknown` | `unknown` |

**Invariants spécifiques** :

- La synthèse ne lit jamais `sensor.nas_imprimerie_free_space_percent`.
- Elle consomme exclusivement la décision locale `sensor.nas_imprimerie_stockage_etat`.
- Toute évolution des seuils stockage est du ressort du contrat de décision stockage, pas de ce contrat.

### 7.6 Axe `uptime`

Dérivé **exclusivement** d'un `binary_sensor` de décision métier à créer ultérieurement (ex : `binary_sensor.nas_imprimerie_reboot_detecte`).

| État | Condition |
|---|---|
| `unknown` | aucun capteur de décision reboot n'existe dans Arsenal à ce jour |

> La détection de reboot nécessite un historique (comparaison avec la valeur précédente d'`uptime`). Cet historique est l'affaire de la couche décision, pas de la synthèse (invariant I-SYNTH-02 — pureté : fonction sans état). Tant que la couche décision n'est pas câblée, cet axe reste à `unknown`. Les états `ok / critical` deviendront disponibles lors de la révision v1.2, après création du capteur de décision reboot.

---

## 8. Raison canonique

L'attribut `raison` est une **chaîne fermée** décrivant le défaut dominant.
Valeurs autorisées :

- `nominal`
- `chaine_degradee`
- `chaine_rompue`
- `vpn_down`
- `vpn_error`
- `ups_on_battery`
- `ups_low_battery`
- `ups_off`
- `stockage_bas`
- `stockage_critique`
- `reboot_detecte`
- `donnees_incompletes`

**Nouveautés v1.1** : `stockage_bas` et `stockage_critique` sont désormais **effectivement produits** par la synthèse, en conséquence de l'activation de l'axe stockage (§7.5).

Invariant I-RAISON-01 : un et un seul code de raison à tout instant. En cas de défauts multiples, c'est le plus prioritaire (section 9) qui gagne. La liste complète reste visible dans `defauts_actifs`.

Invariant I-RAISON-02 : `raison = "nominal"` si et seulement si `state = "ok"`.

---

## 9. Priorités entre défauts

Ordre de priorité **décroissante** (le plus prioritaire en tête) :

1. `chaine_rompue` — sans chaîne, rien d'autre n'est interprétable
2. `donnees_incompletes` — on ne sait pas
3. `ups_low_battery` — extinction imminente, fenêtre d'action très courte
4. `ups_off` — UPS hors service, site non protégé
5. `vpn_down` / `vpn_error` — site coupé du reste de l'infra
6. `stockage_critique` — **effectif en v1.1**
7. `reboot_detecte`
8. `ups_on_battery`
9. `stockage_bas` — **effectif en v1.1**
10. `chaine_degradee`

**Justification** : la chaîne prime sur tout (sans elle pas d'information fiable). `ups_low_battery` prime sur `ups_off` parce qu'il représente une fenêtre d'action encore ouverte — l'opérateur peut intervenir avant la coupure. `ups_off` est un constat d'état non protégé, moins réversible dans l'urgence. Les deux priment sur le VPN parce que la perte d'UPS peut entraîner une extinction non contrôlée du NAS et donc la perte de toute la chaîne. Le VPN prime sur le stockage parce qu'un stockage critique sans VPN est impossible à traiter à distance de toute façon.

---

## 10. Invariants normatifs

### I-SYNTH-01 — Non-masquage orthogonal

La synthèse globale (`state`) NE DOIT JAMAIS empêcher l'accès aux sous-états par axe. Les 5 attributs `axe_*` sont **toujours** lisibles indépendamment. Un consommateur aval (UI, alerte) DOIT pouvoir ignorer `state` et raisonner directement sur les axes s'il le souhaite.

### I-SYNTH-02 — Pureté de la couche

La synthèse NE DOIT déclencher aucune action, notification, requête externe ou écriture. Elle est une fonction pure `(entrées) → (sorties)`.

### I-SYNTH-03 — Aucune correction de source

Si une entrée est incohérente (ex : `vol_free_pct = -5`), la synthèse ne corrige PAS. Elle signale `unknown` sur l'axe concerné et laisse la correction à la couche acquisition.

### I-SYNTH-04 — Pas de dépendance cachée

Toutes les dépendances d'entrée sont listées en section 4. Toute lecture non listée est une violation contractuelle.

### I-SYNTH-05 — Raison canonique obligatoire

Un `state` différent de `ok` DOIT être accompagné d'une `raison` autre que `nominal`. Inversement, `raison = nominal` impose `state = ok`.

### I-SYNTH-06 — Frontière alerte / UI

La synthèse NE contient AUCUNE logique destinée à l'affichage (couleurs, icônes, phrases humaines) ni à l'alerte (priorité push, canal de notification). Ces responsabilités appartiennent à des couches distinctes qui LISENT la synthèse.

### I-SYNTH-07 — Priorité déterministe

En présence de défauts multiples, la résolution de priorité suit strictement l'ordre de section 9. Aucun tirage arbitraire, aucune heuristique.

### I-SYNTH-08 — Respect des couches (ajout v1.1)

La synthèse NE DOIT JAMAIS dériver un axe à partir d'une mesure brute si une décision dédiée existe. Lorsqu'un contrat de décision locale (ex : `nas_stockage_decision.md`) produit une enum catégorielle, la synthèse consomme exclusivement cette enum et n'accède PAS à la mesure brute sous-jacente.

---

## 11. Ce qui est hors scope

- **Valeurs chiffrées des seuils stockage** — appartiennent au contrat de décision stockage (`nas_stockage_decision.md v1.0-durci`).
- **Détection effective de reboot** — appartient à un futur contrat de décision reboot.
- **Alerting (Telegram, push, email)** — appartient à la couche alerte.
- **Rendu UI (cartes Lovelace, couleurs, icônes)** — appartient à la couche UI.
- **Historisation / recorder** — appartient à la gouvernance recorder Arsenal.
- **Extension vers d'autres sites** — ce contrat traite uniquement du site imprimerie. Une généralisation nécessitera un contrat parent.

---

## 12. Versioning du contrat

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-04-24 | Création. Définit la couche de synthèse, 5 axes, enum canonique, raison, priorités, seuils cadence 60 s. |
| 1.0-validée | 2026-04-24 | Alignement sur la réalité du pipeline : axe UPS en `ONLINE / ON_BATTERY` (+ optionnels). Axes `stockage` et `uptime` ramenés à `unknown` tant qu'aucun `binary_sensor` de décision dédié n'existe. Priorité `ups_low_battery` avant `ups_off`. Entrées mesures métier réduites à ce qui est réellement consommé. |
| 1.1 | 2026-04-24 | Activation de l'axe stockage via `sensor.nas_imprimerie_stockage_etat`. Production effective de `stockage_bas` et `stockage_critique` dans `raison`, `priorite_active`, `defauts_actifs`. Ajout de l'invariant I-SYNTH-08 (respect des couches). Dépendance explicite au contrat `nas_stockage_decision.md v1.0-durci`. |
