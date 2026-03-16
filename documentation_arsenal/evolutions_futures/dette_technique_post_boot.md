# Dette technique — Reconvergence post-boot
## Domaine : Climatisation

**Identifiée lors de :** audit YAML v1.2  
**Type de dette :** Implémentation Home Assistant (trigger bootstrap)  
**Statut :** corrigée

---

## Symptôme

Certaines entités et automations déclenchées uniquement sur `state`
ne se recalculent pas après redémarrage de Home Assistant.

Après boot, ces objets conservent leur dernière valeur persistée
jusqu'au prochain changement d'état de leurs entrées.

---

## Impact

- Seuils COOL potentiellement incohérents si la présence a changé pendant l'arrêt
- Automations de gouvernance non réévaluées — état possiblement désynchronisé
- Guard potentiellement silencieux sur une situation interdite existant au boot

---

## Composants concernés

### Triggered sensors — recalcul manquant au boot

Les template sensors déclenchés uniquement par `state` ne sont pas évalués
au boot. Leur état restauré peut donc être incohérent avec le contexte courant.
Contrairement aux template sensors non-triggered, qui sont recalculés
automatiquement lors du chargement du moteur de templates.

- `sensor.seuil_allumage_clim_applique`
- `sensor.seuil_extinction_clim_applique`

### Automations de gouvernance — réévaluation manquante au boot

- `automation.clim_gestion_timer_absence_prolongee`
- `automation.mode_maison_gestion_chauffage_clim_hiver`

### Guard — déclenchement manquant sur situation interdite préexistante

- `automation.clim_guard_logique_anti_absurde`

---

## Correction retenue

Les deux mécanismes suivants sont complémentaires et s'appliquent ensemble :

- `homeassistant: start` — force une première évaluation des objets
  déclenchés uniquement par transition `state`, sans garantir l'évaluation continue.
  Sans ce trigger, l'objet n'est jamais évalué si aucune transition ne survient.

- `input_boolean.systeme_stable` — empêche toute action tant que les entités
  ne sont pas stabilisées (après initialisation ou redémarrage).

```
homeassistant: start → première évaluation
        ↓
condition: systeme_stable == on → action exécutée seulement si système prêt
```

### Triggered sensors

Ajouter `platform: homeassistant / event: start` dans le bloc `trigger` :

```yaml
trigger:
  - platform: state
    entity_id:
      - binary_sensor.presence_famille_unifiee
      - input_number.clim_seuil_declenchement_presence
      - input_number.clim_seuil_declenchement_absence
  - platform: homeassistant
    event: start
```

### Automations de gouvernance

Même ajout dans le bloc `trigger`. L'idempotence existante garantit
qu'aucune action parasite n'est émise si l'état est déjà conforme.

Ajouter un délai de stabilisation en début d'action :

```yaml
action:
  - delay: "00:00:05"
  - # reste de l'action inchangé
```

`homeassistant: start` ne garantit pas que toutes les entités soient
immédiatement disponibles. Le délai laisse le state registry et les
intégrations externes terminer leur initialisation.

### Guard

Même ajout dans le bloc `trigger`. Ajouter explicitement la condition
de stabilisation en tête du bloc `condition` :

```yaml
condition:
  - condition: state
    entity_id: input_boolean.systeme_stable
    state: "on"
  # conditions existantes inchangées
```

Garantit que le Guard ne s'évalue pas sur des entités encore
`unavailable` en début de boot. Cette condition empêche le Guard
de s'évaluer pendant la phase d'initialisation où certaines entités
peuvent être `unknown` ou `unavailable`.

---

## Ce qui n'est pas concerné

- `sensor.clim_target_mode` — template pur, recalculé automatiquement au boot
- `automation.clim_transit_decision_execution` — protégé par `systeme_stable`
- `automation.clim_watchdog_coherence_decision_reel` — protégé par `systeme_stable`
- Tous les binary_sensor template non-triggered — recalcul automatique

---

## Note contractuelle

Cette dette ne remet pas en cause le contrat `09_observabilite.md`.  
Le contrat garantit la reconvergence post-boot — cette dette documente
les corrections d'implémentation nécessaires pour l'honorer.
