# ARSENAL — Boiler Guard · Contrat normatif

<!-- audit:scope=doc -->

**Composant :** `arsenal-boiler-guard`
**Version normative de ce document :** v1.1 · **Version terrain déployée : v1.3**
**Scope :** Résilience locale du Raspberry Pi boiler bridge
**Dossier :** `/homeassistant/00_documentation_arsenal/outils_externes/boiler_pi/`
**Dernière mise à jour :** 2026-04-07 (voir note de convergence C48 ci-dessous)

---

## 0. Note de convergence (C48, 2026-09-06)

Depuis la migration Boiler Bridge → Boilerack (technique, close et validée
terrain), le guard a été retargeté sans changement de ses 3 axes ni de sa
logique d'escalade :

- **Service protégé par défaut : `boilerack.service`** (historiquement
  `boiler_bridge.service` — voir §7). Le guard ne cible plus le service
  désactivé.
- **Rôle inchangé : supervision externe locale du Pi**, indépendante de la
  **garde fonctionnelle HA composée** (`contrats/chauffage/30_decision_centrale__amendement_garde_execution.md`)
  — les deux gardes évaluent des signaux différents, à des couches
  différentes, et ne se substituent pas l'une à l'autre.
- **Le probe `vclient`/`vcontrold` de l'Axe 3 (§2) ne constitue pas une
  preuve de santé complète de Boilerack.** Il valide la chaîne locale
  partagée (`vclient → vcontrold → Optolink → chaudière`), pas le diagnostic
  agrégé propre à Boilerack (`<prefix>/bridge/telemetry_status`,
  `chain.status`/`chain.cause` — cf.
  [`migration_boiler_bridge_vers_boilerack.md`](../../architecture/chauffage/migration_boiler_bridge_vers_boilerack.md)
  §3), que ce guard ne lit pas.
- **Limites connues, explicitement parquées** (chantier
  [`c48_convergence_documentaire_boilerack.md`](../../audits/04_chantiers/chauffage/c48_convergence_documentaire_boilerack.md),
  Axe C — aucun développement n'est engagé ici) : panne propre de Boilerack
  non détectée directement par ce guard · `RC_PROBE` · sous-axe MQTT 3b ·
  escalade/reboot du guard.

---

## 1. Rôle et périmètre

Le guard est un outil d'infrastructure locale exécuté sur le Raspberry Pi boiler bridge.

Son rôle est d'évaluer périodiquement si le service protégé (§7) remplit encore sa mission, et d'agir localement en cas de défaillance, selon une escalade progressive et déterministe.

**Ce que le guard n'est pas :**

- Il n'est pas un contrat MQTT — il n'interagit pas avec les topics boiler.
- Il n'est pas un superviseur Home Assistant — il ne dépend pas de HA pour fonctionner.
- Il n'est pas un oracle de santé global — il évalue uniquement les axes définis ci-dessous, et ne constitue pas une preuve de santé complète du service protégé (voir §0).

**Invariant absolu :** le guard est plus simple que le système qu'il protège. Toute complexification du guard est un signal de mauvaise conception.

---

## 2. Axes d'évaluation

Le guard évalue trois axes indépendants. Chaque axe a une cause propre et une action propre.

### Axe 1 — Vie

**Question :** le Pi et son guard sont-ils encore vivants ?

**Mécanisme :** watchdog kernel (`bcm2835_wdt`), indépendant du guard applicatif. Si le guard lui-même se bloque, le watchdog provoque un reboot automatique.

**Couverture :** blocage kernel, deadlock profond, freeze système.

**Ne couvre pas :** réseau dégradé, bridge KO — ces cas relèvent des axes 2 et 3.

---

### Axe 2 — Réseau

**Question :** le Pi a-t-il encore une connectivité réseau locale exploitable ?

**Test :** ping gateway locale. La gateway est la cible canonique — indépendante du broker MQTT, indépendante de Home Assistant.

**Interprétation :** gateway injoignable = réseau Pi KO. Ce test ne dit rien sur l'état du broker ou de HA.

---

### Axe 3 — Mission

**Question :** la chaîne locale boiler bridge est-elle encore capable d'assurer sa fonction ?

**Test canonique :**

```
vclient -h localhost -p 3002 getTempKist
```

Ce probe est identique à celui utilisé par le bridge pour publier `vcontrold_status` et `optolink_status`. Aucune divergence de diagnostic entre bridge et guard.

**Critères de succès (tous requis) :**

| Critère | Détail |
|---------|--------|
| Retour dans le délai | Réponse obtenue en moins de 5 secondes |
| Code retour nominal | `vclient` retourne 0 |
| Valeur parseable | Premier champ numérique de la dernière ligne extractible |
| Valeur dans la plage plausible | Valeur comprise entre 0 et 100 °C |

**Format de sortie vclient attendu :**

```
getTempKist:
20.500000 Grad Celsius
```

Le guard extrait `20.500000` via `tail -n 1 | awk '{print $1}'`.

**Ce que ce test valide de bout en bout :** vclient → vcontrold → Optolink → chaudière → réponse valide.

**Ce que ce test ne valide pas :** MQTT, réseau, Home Assistant. Ces éléments sont hors périmètre de l'Axe 3.

---

## 3. Comportements — séquence d'escalade

### Cas 1 — Axe 3 KO, Axe 2 OK

Réseau fonctionnel, chaîne locale ne produit plus de réponse valide sur test canonique.

```
→ restart service <service protégé>   (cible par défaut : boilerack.service — §7)
→ délai de grâce : 90 secondes
→ re-test Axe 3
→ si KO : reboot Pi (un seul reboot logiciel par cycle d'évaluation)
→ pas de retry infini
```

### Cas 2 — Axe 2 KO

Gateway injoignable.

```
→ restart interface réseau (wlan0)
→ délai : 30 secondes
→ re-test Axe 2
→ si KO : reboot Pi
→ pas d'étape intermédiaire supplémentaire
```

### Cas 3 — Blocage profond (Axe 1)

Guard lui-même bloqué ou kernel figé.

```
→ watchdog kernel reprend la main
→ reboot automatique
```

---

## 4. Limites absolues

Ces limites sont non négociables. Toute évolution qui les contredit invalide le contrat.

| Limite | Rationale |
|--------|-----------|
| Pas de boucle de restart | Évite l'amplification de pannes |
| Pas de retry au-delà de la séquence spécifiée | Déterminisme garanti |
| Pas de décision de coupure physique | Le Pi ne décide jamais de sa propre coupure |
| Pas de dépendance à HA pour fonctionner | Autonomie locale complète |
| Un seul reboot logiciel autorisé par cycle d'évaluation | Borne le nombre d'actions par run |

---

## 5. Fréquence d'évaluation

Période nominale : **3 minutes** entre deux cycles (mesurée depuis la fin du cycle précédent).

Implémentation : systemd timer avec `OnUnitInactiveSec=3min` — garantit l'absence de chevauchement entre cycles même en cas d'exécution longue (restart service + délai de grâce).

Délai au boot : `OnBootSec=3min` — laisse le bridge démarrer avant le premier cycle d'évaluation.

---

## 6. Ce que Home Assistant observe

HA observe le résultat du guard, pas son fonctionnement interne.

**Depuis la migration vers Boilerack, ces signaux sont publiés sous le
préfixe déployé `boilerack/*`** (historiquement `boiler/*`, décrit ainsi par
le contrat MQTT du prédécesseur — cf. [`mqtt.md`](mqtt.md)) :

| Signal | Interprétation |
|--------|---------------|
| `boilerack/bridge/online = online` + heartbeat actif | Écrivain nominal |
| Silence sur `boilerack/bridge/heartbeat` > 60 secondes | État dégradé (cf. [`mqtt.md`](mqtt.md) §2.6, historique — les seuils de garde composée HA sont normatifs dans `contrats/chauffage/30_decision_centrale__amendement_garde_execution.md`) |
| `boilerack/bridge/online = offline` | Écrivain déconnecté |

**Frontière d'autorité :** le Pi agit, HA constate. HA peut déclencher une alerte sur silence prolongé mais ne pilote pas les actions du guard.

---

## 7. Implémentation de référence

| Élément | Valeur |
|---------|--------|
| Script | `/home/pi/boiler-bridge/boiler_guard.sh` |
| Service systemd | `boiler-guard.service` |
| Timer systemd | `boiler-guard.timer` |
| Version courante | v1.1 (ce document) · **v1.3 (terrain déployé, §0)** |
| Service protégé | **`boilerack.service`** (cible par défaut depuis le Lot 1 guard/systemd, C48) — historiquement `boiler_bridge.service` |
| Interface réseau | `wlan0` (à vérifier sur le Pi cible) |
| Gateway | `192.168.1.1` (à vérifier sur le Pi cible) |

**Dépendances externes du script :**

| Outil | Usage | Statut |
|-------|-------|--------|
| `ping` | Test Axe 2 | Standard |
| `ip` | Restart interface | Standard |
| `timeout` | Borne temporelle probe | Standard |
| `vclient` | Probe Axe 3 | `/usr/bin/vclient` |
| `awk` | Parsing sortie vclient + comparaison plage | Standard |
| `grep` | Validation regex valeur numérique | Standard |
| `logger` | Journalisation (`journalctl -t boiler-guard`) | Standard |
| `bc` | ~~Comparaison plage~~ | **Supprimé en v1.1** |

---

## 8. Journalisation

Tous les événements sont journalisés via `logger -t boiler-guard`.

Consultation :

```bash
journalctl -t boiler-guard -f
journalctl -t boiler-guard -n 50 --no-pager
```

Messages normalisés :

| Message | Signification |
|---------|--------------|
| `NOMINAL: réseau OK, mission OK (getTempKist=X)` | Cycle nominal |
| `AXE2_KO: gateway injoignable — restart interface réseau` | Axe 2 KO, tentative restart |
| `AXE2_OK: réseau rétabli après restart interface` | Axe 2 rétabli |
| `AXE2_KO: réseau toujours KO après restart interface — reboot` | Reboot pour Axe 2 |
| `AXE3_KO: probe mission en échec (code=N)` | Axe 3 KO, tentative restart service |
| `AXE3_OK: mission rétablie après restart service` | Axe 3 rétabli |
| `AXE3_KO: probe toujours en échec après restart service — reboot` | Reboot pour Axe 3 |

**Codes retour `probe_mission` :**

| Code | Cause |
|------|-------|
| 0 | Succès |
| 1 | vclient timeout ou code retour non nul |
| 2 | Valeur non parseable |
| 3 | Valeur hors plage [0 ; 100] |

---

## 9. Changelog

| Version | Date | Modification |
|---------|------|-------------|
| v1.0 | 2026-04-07 | Version initiale — 3 axes, escalade progressive, systemd timer |
| v1.1 | 2026-04-07 | Suppression dépendance `bc` — comparaison plage via `awk` |
| v1.2–v1.3 | non datée dans ce document (cf. §0) | Lot 1 guard/systemd (C48) : retargetage du service protégé par défaut vers `boilerack.service` (historiquement `boiler_bridge.service`). Aucun changement des 3 axes ni de la logique d'escalade. Détail non tenu par ce document normatif — source : chantier [`c48_convergence_documentaire_boilerack.md`](../../audits/04_chantiers/chauffage/c48_convergence_documentaire_boilerack.md). |

---

## 10. Points ouverts

| Réf | Description | Criticité | Statut |
|-----|-------------|-----------|--------|
| OPEN-G01 | Plage plausible Axe 3 [0 ; 100] °C — à affiner après observation baseline | Basse | Ouvert |
| OPEN-G03 | Watchdog kernel — configuration `watchdog.conf` non versionnée | Basse | Ouvert |
