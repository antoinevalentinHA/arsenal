# ARSENAL — Contrat de résilience des intégrations

**Composant :** `arsenal-ha`
**Version :** v1.0
**Scope :** Détection et relance automatique des intégrations critiques (gel des données et indisponibilité des entités).
**Mode d'application :** report-only — voir §10 et le registre.
**Dépendances :**
- `script.resilience_integration_recover` (action canon)
- `binary_sensor.panne_secteur_en_cours` (inhibition)
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

---

## 6. Interdictions absolues

- Relance non bornée (sans backoff ni plafond).
- Reload pendant une panne secteur active.
- Déclenchement sur un seul axe quand les deux sont requis (chaîne aveugle).
- Infrastructure de diagnostic sans automation consommatrice (chaîne orpheline).
- Appel direct à `homeassistant.reload_config_entry` ou `hassio.addon_restart` **hors** du script canon, **sauf exception inscrite au registre** (§7).

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
