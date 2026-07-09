# Prompt — session dans le dépôt `ha-airstage`

> À coller comme message d'ouverture d'une session Claude Code ciblant **ton
> dépôt `ha-airstage`** (l'intégration `custom_components/fujitsu_airstage`).
> Contexte issu de l'audit Arsenal
> `audit_ventilation_auto_constructeur_recurrent.md`.

---

## Contexte

Le mode de ventilation (`fan_mode`) de ma clim Fujitsu Airstage **retombe
régulièrement sur `auto`** (le « auto constructeur »), alors qu'une couche
domotique externe (Home Assistant) lui impose en continu une vitesse fixe
(`low` / `medium` / `high`). Cette couche externe corrige la dérive dès qu'elle
la voit, donc le symptôme se manifeste par un **combat / clignotement**
(`auto → low → auto …`) et un **martèlement de l'API**, pas par un `auto`
permanent.

Un audit statique de l'intégration a isolé une **hypothèse forte** : dans
`climate.py`, chaque commande fait un **re-poll immédiat** de l'appareil juste
après l'écriture, sur une **API à cohérence différée** — donc relit l'ANCIENNE
valeur et réexpose `auto`.

```python
# custom_components/fujitsu_airstage/climate.py
async def async_set_fan_mode(self, fan_mode: str) -> None:
    await self._ac.set_fan_speed(HA_FAN_TO_FUJITSU[fan_mode])
    await self.instance.coordinator.async_refresh()   # <-- re-poll immédiat, API pas encore cohérente
```

Le même motif (`await self.instance.coordinator.async_refresh()` immédiatement
après l'écriture) est présent dans **tous** les `async_set_*` / `async_turn_*`
(hvac_mode, temperature, swing, preset) et dans `switch.py`. L'intégration est
`iot_class: local_polling`, intervalles `AIRSTAGE_SYNC_LOCAL_INTERVAL = 60 s` /
`AIRSTAGE_SYNC_INTERVAL = 120 s` (`const.py`).

## Ta mission

1. **Confirmer ou infirmer** l'hypothèse « poll-after-set » en lisant :
   - `custom_components/fujitsu_airstage/climate.py`
     (`async_set_fan_mode`, `async_set_hvac_mode`, `async_update`,
     property `fan_mode`) ;
   - `custom_components/fujitsu_airstage/entity.py`
     (`update_handle_factory`, property `_ac`) ;
   - la lib **`pyairstage`** (`>=2.4.1,<3`) : que renvoie `get_devices()`
     **immédiatement après** `set_fan_speed()` ? Y a-t-il une écriture
     optimiste du cache local, ou uniquement l'état rapporté par l'appareil ?
     La valeur écrite est-elle relue de façon fiable au poll suivant, et sous
     quel délai ?

2. **Vérifier le comportement firmware attendu (M1)** : l'unité remet-elle la
   vitesse de ventilation à `AUTO` lors d'un **changement de mode opératoire**
   (`cool` ↔ `dry` ↔ `heat`) ? Si oui, le documenter — ça explique une partie
   des resets, indépendamment de la course logicielle.

3. **Proposer un correctif minimal et idempotent** côté intégration. Pistes à
   évaluer (ne pas toutes appliquer aveuglément — choisir la plus sûre) :
   - **Mise à jour optimiste** : après un `set_*` réussi, écrire la valeur
     cible dans les paramètres mis en cache du coordinator puis
     `self.async_write_ha_state()`, **sans** re-poll immédiat — pour que
     l'entité reflète tout de suite l'état commandé et ne réexpose pas la
     valeur périmée.
   - **Refresh différé** plutôt qu'immédiat (laisser à l'appareil le temps de
     converger avant de relire), en évitant de bloquer l'appel de service.
   - Traiter le cas où l'appareil **ignore** la commande de vitesse dans
     certains modes (ex. `dry`) — ne pas boucler dessus.

4. **Garde-fous** :
   - Ne pas casser les autres entités qui dépendent du même motif refresh
     (`switch.py`, température, swing, preset) — appliquer le pattern de façon
     cohérente ou le factoriser.
   - Respecter le style du dépôt (codeowners `@danielkaldheim`, `@ohshazbot`),
     rester rebasable proprement sur l'upstream.
   - Ajouter / adapter les **tests** de l'intégration si présents.

5. **Livrable** : un diff ciblé + une note expliquant la cause racine confirmée,
   le correctif retenu et pourquoi, et une procédure de validation runtime
   (mesurer le délai écriture → lecture cohérente, compter les allers-retours
   `auto` par heure avant/après).

## Ce que la couche domotique fait déjà (ne rien attendre d'elle)

Côté Home Assistant, la dérive `auto` est **déjà** rattrapée (triggers dédiés
sur `fan_mode → auto`). Le but ici est de **supprimer la cause à la source**
dans l'intégration, pour arrêter le combat et le martèlement API — pas de
compenser davantage côté domotique.
</content>
