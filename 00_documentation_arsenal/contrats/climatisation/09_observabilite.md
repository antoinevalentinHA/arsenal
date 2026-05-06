# CONTRAT ARSENAL — CLIMATISATION
## 09 — Observabilité & Robustesse

**Version contrat :** v1.2

---

## États exposés

| Entité | Rôle |
|---|---|
| `sensor.clim_action_en_cours` | Ce que fait réellement la clim |
| `sensor.clim_raison_decision` | Narration humaine de la décision canonique |

Ces états :
- ne décident rien,
- n'agissent jamais,
- **peuvent diverger temporairement de l'état réel sans constituer un bug**.

Aucun état d'observabilité n'est requis pour le fonctionnement du système.

---

## Robustesse & Déterminisme

Après :
- redémarrage HA,
- reload de templates,
- indisponibilité temporaire,

le système :
- recalcule la décision,
- reconverge automatiquement,
- sans mémoire implicite,
- sans action spéciale post-boot.

À contexte identique :
- la décision est identique,
- l'état final du système est identique (latence d'exécution mise à part).
