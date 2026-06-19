# ARSENAL — Contrat de résilience des intégrations

**Composant :** `arsenal-ha`
**Version :** v1.1
**Scope :** Détection et relance automatique des intégrations critiques (gel des données et indisponibilité des entités).
**Mode d'application :** report-only — voir §10 et le registre.
**Dépendances :**
- `script.resilience_integration_recover` (action canon)
- `binary_sensor.panne_secteur_en_cours` (inhibition secteur)
- `binary_sensor.contexte_wan_indisponible` (inhibition WAN des intégrations cloud — voir §11)
- Contrat `pannes/internet/30` — contexte de remédiation réseau
- Contrat Notifications
- Registre : `scripts/arsenal_contracts/resilience_integrations_registre.yaml`

---

## 1. Principe fondamental

> Une intégration peut défaillir de deux manières orthogonales :
> ses données peuvent **vieillir** (fraîcheur), ou ses entités peuvent **disparaître** (disponibilité).
> Un détecteur de fraîcheur ne détecte pas une disparition.
> **Un âge figé bas ne vaut jamais preuve de santé.**

Les deux axes doivent exister **séparément**. Aucun ne peut servir de substitut à l'autre.

---

## 2. Définitions opposables

| Terme | Définition |
|---|---|
| **Fraîcheur** | Âge des données, dérivé du `last_updated` le plus récent des membres exploitables du groupe source, plafonné. Mesure le vieillissement. |
| **Disponibilité** | Présence d'au moins un membre exploitable du groupe source. L'**indisponibilité franche** = « 0 membre exploitable » maintenu sur une temporisation. Mesure la disparition. |
| **Recovery** | Procédure de relance déléguée au script canon `resilience_integration_recover` (attempt / reset / block), bornée par backoff et plafond, inhibée en panne secteur. |
| **Chaîne complète** | Intégration possédant tous les maillons des couches diagnostic, décision, action, UI (§4), câblant **les deux** axes : gel silencieux ET indisponibilité franche. |
| **Chaîne orpheline** | Infrastructure de diagnostic et/ou d'action présente, mais **aucune automation de décision** ne la consomme. L'incident est diagnostiqué, jamais traité. **Non conforme.** |
| **Chaîne aveugle** | Automation de décision présente mais ne déclenchant que sur **un seul** axe (typiquement la fraîcheur), ignorant l'indisponibilité franche. **Non conforme.** |
| **Exception documentée** | Intégration dérogeant légitimement au canon d'âge, inscrite au registre avec motif (ex. disponibilité native + action propre). |

---

## 3. Les deux axes — règle de non-substitution

- L'axe **fraîcheur** repose sur un capteur d'âge et un binaire de gel avéré (seuil numérique, débouncé).
- L'axe **disponibilité** repose sur un comptage de membres exploitables du groupe source et un binaire d'indisponibilité franche (débouncé).
- **Interdit :** utiliser l'âge comme preuve de disponibilité. Lorsque tous les membres deviennent indisponibles, l'âge peut se figer sur une dernière valeur basse ; le binaire de gel reste alors `off` et ne déclenche aucune relance. Cet état est couvert par l'axe disponibilité.

---

## 4. Anatomie d'une chaîne complète

**Diagnostic** — groupe source ; capteur d'âge ; binaire gel avéré ; binaire indisponibilité franche ; binaire retour OK ; binaire recovery en cours.
**Décision** — automation déclenchant sur gel **et** indisponibilité **et** fin de backoff **et** retour OK, sous garde `input_boolean.systeme_stable = on`, en `mode: single`, sans `time_pattern`.
**Action** — délégation à `script.resilience_integration_recover` ; timer de backoff dédié ; compteur de tentatives dédié.
**UI** — exposition non trompeuse de l'état des axes et du recovery.

---

## 5. Invariants obligatoires

1. **Fraîcheur** — capteur d'âge dérivé de `last_updated`, plafonné.
2. **Disponibilité** — binaire d'indisponibilité distinct de l'âge, fondé sur comptage de membres exploitables (« 0 membre exploitable » maintenu = indisponibilité confirmée).
3. **Non-substitution** — l'âge ne prouve pas la disponibilité.
4. **Recovery** — convergence vers le script canon unique, jamais une seconde chaîne d'action.
5. **Retour OK** — détecté explicitement, conditionné à un recovery en cours, débouncé.
6. **Backoff** — borné par un cap.
7. **Plafond tentatives** — au-delà du plafond, passage en `block` et arrêt des relances.
8. **Inhibition panne secteur** — aucune tentative pendant `panne_secteur_en_cours = on` ; le reset reste autorisé.
9. **Observabilité** — état des axes, compteur, backoff exposables ; notifications sur attempt/échec/block/retour OK.
10. **Absence de boucle agressive** — `mode: single`, `max_exceeded: silent`, déclenchement sur transition, garde `systeme_stable`.
11. **Support WAN disponible** — une intégration de classe `cloud_wan` ne tente aucun recovery (`op == attempt`) tant que le contexte WAN est indisponible (`binary_sensor.contexte_wan_indisponible = on`). Cette inhibition ne concerne **que** les intégrations `cloud_wan` ; les intégrations `local_lan` n'y sont jamais soumises. Comme pour l'inhibition panne secteur (invariant 8), seul `attempt` est inhibé ; `reset` et `block` restent autorisés.

---

## 6. Interdictions absolues

- Relance non bornée (sans backoff ni plafond).
- Reload pendant une panne secteur active.
- Déclenchement sur un seul axe quand les deux sont requis (chaîne aveugle).
- Infrastructure de diagnostic sans automation consommatrice (chaîne orpheline).
- Appel direct à `homeassistant.reload_config_entry` ou `hassio.addon_restart` **hors** du script canon, **sauf exception inscrite au registre** (§7).
- Tenter un recovery d'une intégration `cloud_wan` pendant un contexte WAN indisponible ou un contexte de remédiation réseau actif (cf. `pannes/internet/30`).
- Coder `binary_sensor.contexte_wan_indisponible` en dur dans une garde globale du script canon : la garde WAN est **paramétrée** (`wan_entity`), pour qu'une intégration `local_lan` ne puisse jamais être inhibée par effet de bord.
- Inhiber une intégration `local_lan` (Airstage, HomeKit, SwitchBot, Synology, Zigbee2MQTT) sur un signal WAN.

---

## 7. Exceptions documentées

Une intégration peut déroger au canon d'âge si elle dispose d'un signal de disponibilité natif et d'une action propre, **à condition d'être inscrite au registre** avec son motif. L'exception ne dispense pas des invariants 6 à 10.

**Zigbee2MQTT** est une exception documentée légitime : disponibilité native via `binary_sensor.zigbee2mqtt_bridge_connection_state`, action `hassio.addon_restart`, backoff et garde anti-boucle maintenus. Le canon d'âge ne s'applique pas. Cette intégration ne doit pas être normalisée dans le canon d'âge.

---

## 8. Chaînes orphelines à arbitrer

**Audi** et **Withings** disposent d'une infrastructure partielle (groupe, capteur d'âge, binaires gel/retour OK/recovery, timer de backoff) mais **sans automation de décision ni compteur de tentatives**. Ce sont des chaînes orphelines, **non conformes**, inscrites au registre comme dettes temporaires à arbitrer. Aucun runtime n'est ajouté pour ces intégrations tant qu'un ID d'automatisation n'est pas fourni : compléter ou décommissionner relève d'un arbitrage ultérieur.

---

## 9. Séparation des couches (mapping dépôt)

| Couche | Emplacement |
|---|---|
| Diagnostic | `02_groups/integrations/`, `12_template_sensors/system/integrations/` |
| Décision | `11_automations/system/reload_integrations/` |
| Action | `10_scripts/system/resilience_integration_recover.yaml` |
| UI | `18_lovelace/` |

---

## 10. Conformité CI et statut d'application

La conformité est vérifiée par `scripts/arsenal_contracts/check_resilience_integrations_contracts.py`, dont la source d'autorité est le registre `resilience_integrations_registre.yaml`. Le checker raisonne par registre, **jamais** par nom de fichier (rappel : `fujitsu.yaml` porte l'intégration Airstage).

Le registre type chaque maillon par un statut fermé : `present`, `absent_non_conforme_temporaire` (dette tolérée en report-only via les exceptions du registre), ou `non_applicable` (hors périmètre pour le mode de l'intégration, jamais une dette). Une dérogation légitime n'est pas un statut de maillon mais un bloc `exception_documentee` au niveau de l'intégration. Le checker lit ces statuts tels quels, sans inférence.

Le contrat s'applique en **mode report-only** : les écarts connus inscrits au registre n'échouent pas la CI ; tout écart **nouveau ou non documenté** échoue dès `STRICT_ON_NEW=1`. La résorption d'une dette se traduit par la suppression de sa ligne d'exception au registre.

---

## 11. Garde réseau WAN (intégrations cloud)

### 11.1 Principe

Une intégration dont le support transite par Internet (**`cloud_wan`**) devient légitimement `unavailable` pendant une panne WAN ou une campagne de remédiation réseau. Dans ce cas, son indisponibilité est un **KO attendu**, pas un dysfonctionnement d'intégration : un recovery (reload de config entry) serait **futile** — le support distant est inatteignable — et consommerait tentatives, backoff et notifications jusqu'au blocage.

Par symétrie stricte avec l'inhibition panne secteur (invariant 8), le recovery des intégrations `cloud_wan` est inhibé tant que le support WAN n'est pas disponible et stabilisé.

### 11.2 Conformité à `pannes/internet/30`

Le contrat `pannes/internet/30` (Contexte de remédiation réseau) impose à tout composant **réseau-dépendant** de bloquer toute action corrective fondée sur une observation réseau pendant un contexte de remédiation actif. L'axe disponibilité des intégrations `cloud_wan` est un tel composant.

**Déclaration explicite (exigée par `pannes/internet/30`) :** pendant un contexte de remédiation réseau, une indisponibilité WAN, ou un retour WAN non encore stabilisé, les recoveries des intégrations `cloud_wan` sont **inhibés**. Les diagnostics (axes fraîcheur/disponibilité) continuent d'observer ; seule l'action de recovery est suspendue.

### 11.3 Signal canon

Le contexte WAN est porté par un binaire diagnostic unique :

> **`binary_sensor.contexte_wan_indisponible`** (`unique_id: contexte_wan_indisponible`)

Il est `on` si une campagne de remédiation réseau est active (`input_boolean.reboot_box_en_cours = on`) **ou** si l'accès externe n'est pas disponible (`binary_sensor.acces_externe != on`, donc `off`/`unknown`/`unavailable`). Il ne repasse `off` qu'après stabilisation du retour WAN (cf. son `delay_off`). Ce binaire décrit un **état système WAN** ; il ne lit ni ne modifie `binary_sensor.panne_secteur_en_cours`, et n'évoque aucune action de recovery. La garde secteur (invariant 8) et la garde WAN sont **complémentaires et indépendantes**.

### 11.4 Contrat de câblage

| Élément | Rôle |
|---|---|
| `meta.inhibition_wan` (registre) | nom canonique du signal WAN : `binary_sensor.contexte_wan_indisponible`. Déclaré **une seule fois**. |
| `classe_reseau` (registre, par intégration) | `cloud_wan` ou `local_lan`. **Seule clé de vérité** ; aucune clé `garde_wan` concurrente. |
| `wan_entity` (paramètre du script canon) | optionnel. Transmis par l'appel `op: attempt` d'une intégration `cloud_wan`, jamais par une `local_lan`. |

**Règles de câblage :**

- Pour une intégration **`cloud_wan`** avec automation active, l'appel `op: attempt` à `script.resilience_integration_recover` transmet `wan_entity: binary_sensor.contexte_wan_indisponible`.
- Pour une intégration **`local_lan`**, l'appel `op: attempt` ne transmet **jamais** `wan_entity`.
- Dans le script canon, la garde WAN est **optionnelle et paramétrée** : elle ne s'arme que si `wan_entity` est défini, inhibe uniquement `op == attempt`, bloque si l'entité transmise est `on`, et ne bloque jamais `reset` ni `block`. Elle ne code jamais le binaire en dur.

**Classification :**

| Classe | Intégrations |
|---|---|
| `cloud_wan` | Netatmo, Overkiz, Audi, Withings |
| `local_lan` | Airstage / Fujitsu, HomeKit, SwitchBot, Synology, Zigbee2MQTT |

Câblage runtime immédiat : Netatmo et Overkiz (cloud actives). Audi et Withings sont `cloud_wan` mais orphelines (§8) — leur classe est enregistrée pour le jour de leur câblage, sans appel à garder aujourd'hui.

### 11.5 Réserve — gardes locales hors périmètre

Cet invariant couvre **exclusivement** le support WAN. Les intégrations `local_lan` ne sont **jamais** inhibées par une panne WAN : Airstage (équipement joignable sur le LAN via `binary_sensor.climatiseur`), HomeKit (pont local), SwitchBot (BLE via proxys ESP32), Synology (NAS LAN) et Zigbee2MQTT (bridge MQTT) conservent un recovery pleinement actif même Internet coupé.

Une éventuelle garde « support **local/LAN** disponible » — qui inhiberait le recovery d'une intégration locale pendant un KO LAN attendu — relèverait d'un **invariant distinct**, non traité ici. Elle utiliserait d'autres signaux (LAN, non WAN) et un autre périmètre d'intégrations. Sa mention ici vaut **réserve explicite**, pas ouverture de chantier.
