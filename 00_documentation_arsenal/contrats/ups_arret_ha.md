# Contrat UPS / Arrêt Home Assistant
**Domaine :** Infrastructure  
**Version :** v1.0  
**Statut :** Projet  
**Dernière révision :** 2026-04-24

---

## 1. Objet

Déclencher un arrêt propre de Home Assistant lorsque l'UPS alimente
l'infrastructure sur batterie et que l'autonomie résiduelle devient
insuffisante pour garantir un fonctionnement sûr du Raspberry Pi.

---

## 2. Périmètre

### 2.1 Sources d'entrée autorisées

| Entité | Rôle dans le contrat |
|---|---|
| `sensor.ups_code_d_etat` | Flags NUT — référence brute (informatif) |
| `sensor.ups_autonomie_de_la_batterie` | Autonomie résiduelle en secondes |
| `sensor.ups_autonomie_de_la_batterie_faible` | Seuil d'alerte bas natif UPS (informatif) |
| `binary_sensor.critere_ups_sur_batterie` | Critère CD — UPS sur batterie |
| `binary_sensor.critere_ups_batterie_faible` | Critère SBF — batterie faible UPS |

### 2.2 Action autorisée

| Service | Déclenchement |
|---|---|
| `hassio.host_shutdown` | Arrêt propre du Raspberry Pi / Home Assistant |

Ce contrat n'autorise **aucune action** sur le NAS, l'UPS, la box,
la fibre, le switch ou la borne Deco.

---

## 3. Critères de décision

### 3.1 Coupure durable (CD)

> `binary_sensor.critere_ups_sur_batterie` **= `on` de façon continue pendant ≥ 60 s**

Délégué à l'automation via `for: "00:01:00"`. Ce critère n'est pas
encodé en template sensor — conforme au contrat Template Sensors UPS v1.0.

### 3.2 Autonomie HA critique (AHC)

> `sensor.ups_autonomie_de_la_batterie` **< 600 s** (< 10 min)

Seuil jugé insuffisant pour garantir un fonctionnement sûr du Raspberry Pi.
Il est volontairement inférieur au seuil ANC (1 800 s) du contrat NAS,
ce qui assure que le NAS est arrêté en premier lors d'une coupure longue.

### 3.3 Batterie faible UPS (SBF)

> `binary_sensor.critere_ups_batterie_faible` **= `on`**

Réutilisation directe du sensor défini dans le contrat Template Sensors UPS v1.0.
SBF est prioritaire sur AHC : sa vérification déclenche la décision
indépendamment du seuil AHC.

---

## 4. Règle de décision

```
ARRÊT HA ← CD  AND  ( AHC  OR  SBF )
```

| CD | AHC | SBF | Décision |
|:---:|:---:|:---:|---|
| ✗ | — | — | ✗ Pas d'action (secteur présent ou coupure < 60 s) |
| ✓ | ✗ | ✗ | ✗ Attente — autonomie encore confortable |
| ✓ | ✓ | ✗ | ✓ **Arrêt HA** |
| ✓ | ✗ | ✓ | ✓ **Arrêt HA** |
| ✓ | ✓ | ✓ | ✓ **Arrêt HA** |

---

## 5. Invariants

| # | Invariant |
|---|---|
| I-1 | Aucun arrêt HA immédiat au passage sur batterie — le délai CD de 60 s est obligatoire |
| I-2 | Le critère temporel CD appartient exclusivement à l'automation via `for: "00:01:00"` |
| I-3 | Tout état `unavailable` ou `unknown` sur une source interdit l'arrêt par défaut — jamais de déclenchement sur données absentes |
| I-4 | L'arrêt HA est terminal : aucune action postérieure ne peut être attendue ou garantie par Arsenal |
| I-5 | Le NAS est hors périmètre — son arrêt est géré par le contrat UPS / Arrêt NAS v1.1 ; ce contrat ne le supervise pas |

---

## 6. Relation avec le contrat UPS / Arrêt NAS

La cohérence entre les deux contrats repose sur l'écart de seuils :

| Contrat | Critère autonomie | Seuil |
|---|---|---|
| UPS / Arrêt NAS v1.1 | ANC | < 1 800 s (< 30 min) |
| UPS / Arrêt HA v1.0 | AHC | < 600 s (< 10 min) |

Cet écart de 1 200 s garantit que, dans le cas nominal, le NAS est arrêté
bien avant que HA n'atteigne son propre seuil critique.

SBF étant partagé entre les deux contrats, un déclenchement SBF simultané
est possible. L'ordre d'exécution NAS → HA n'est garanti que si le NAS a
eu le temps de s'arrêter entre les deux décisions. Ce risque est documenté
comme résiduel — il n'est pas géré par ce contrat.

---

## 7. Exclusions explicites

Ce contrat ne pilote pas et ne déclenche pas :

- l'arrêt du NAS,
- l'arrêt ou le délestage de l'UPS,
- l'arrêt du réseau (switch, box, fibre, Deco),
- le redémarrage de Home Assistant,
- toute notification post-arrêt,
- toute orchestration après `hassio.host_shutdown`.

---

## 8. Références

| Document | Lien |
|---|---|
| Contrat UPS / Arrêt NAS | `contrat_ups_arret_nas_v1.1.md` |
| Contrat Template Sensors UPS | `contrat_template_sensors_ups_v1.0.md` |
