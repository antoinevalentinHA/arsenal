# CONTRAT ARSENAL — CLIMATISATION
## 09 — Observabilité & Robustesse

**Version contrat :** v1.2

---

## États exposés

| Entité | Rôle |
|---|---|
| `sensor.clim_action_en_cours` | Ce que l'intégration rapporte de l'action de la clim |
| `sensor.clim_raison_decision` | Narration humaine de la décision canonique |

Ces états :
- ne décident rien,
- n'agissent jamais,
- **peuvent diverger temporairement de l'état rapporté par leur source sans constituer un bug**.

Cette tolérance vise un **décalage transitoire**, jamais une **perte structurelle
d'information** : un état d'observabilité ne doit pas absorber `unknown` ou `unavailable`
dans une valeur nominale. Une observation absente se restitue par une **abstention
native**, jamais par un état affirmé.

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
