# CONTRAT ARSENAL — CLIMATISATION
## 07 — Exécution — Application idempotente

**Version contrat :** v1.2

---

## Rôle

- Lire exclusivement la décision canonique (`sensor.clim_target_mode`)
- Émettre les commandes nécessaires pour amener l'état réel du système climatique en conformité avec la décision canonique

---

## Entrées d'exécution

| Entité | Rôle |
|---|---|
| `sensor.clim_target_mode` | Mode cible — autorité décisionnelle unique |
| `sensor.consigne_clim_appliquee` | Consigne température appliquée selon présence |
| `binary_sensor.clim_silencieux_autorise` | Mode silencieux — plage horaire et présence |

Ces entrées sont lues, jamais produites par la couche Exécution.

---

## Garanties

- N'embarque aucune logique métier
- N'effectue aucun arbitrage
- **N'envoie aucune commande redondante**
- Ne peut ni modifier ni requalifier la décision canonique
- Ne corrige jamais une décision
- N'insiste jamais : aucune boucle de répétition interne ni tentative active de ré-émission — la ré-assertion éventuelle relève exclusivement du Watchdog
- Ne conserve aucune mémoire interne

---

## Conditions de non-émission

Aucune commande n'est envoyée si :
- le mode réel correspond déjà au mode cible,
- la consigne appliquée est déjà correcte,
- l'état observé est cohérent avec la décision.
