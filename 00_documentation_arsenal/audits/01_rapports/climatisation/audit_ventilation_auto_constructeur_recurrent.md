# AUDIT — VENTILATION CLIM : LE « AUTO CONSTRUCTEUR » SE REMET RÉGULIÈREMENT
## Chaîne intention → recommandation → application → réel, et origine de la dérive vers `auto`

> **Nature.** Audit **statique** de la chaîne de ventilation de la
> climatisation (Modèle B, single-writer), mené à partir de la structure du
> dépôt (aucune exécution de Home Assistant, aucun accès au Recorder de
> l'incident). L'analyse porte sur la logique de code : intention →
> recommandation → résolution/application → réel → diagnostic, et sur
> l'intégration `custom_components/fujitsu_airstage`.
>
> **Statut.** Constats stabilisés. **Aucune modification fonctionnelle
> décidée, aucun réglage proposé, aucun contrat / automatisation / YAML
> runtime touché.** Ce document est une pièce de navigation ; le statut du
> chantier vit dans `REGISTRE_CHANTIERS.md`.
>
> **Conclusion en une ligne.** La chaîne de ventilation Arsenal est **saine**
> et **défend déjà explicitement** la dérive vers le `auto` constructeur (trois
> triggers dédiés). Arsenal n'est donc **pas l'origine** du `auto` : il en est
> la **mitigation**. L'origine est **côté intégration / appareil**, et le
> levier le plus net et corrigeable est une **course « poll-after-set » sur une
> API à cohérence différée** dans `climate.py` (`async_set_fan_mode` re-poll
> immédiatement l'appareil après l'écriture et relit fréquemment l'ancienne
> valeur `auto`). Un correctif appartient au dépôt **ha-airstage**, pas à
> Arsenal.

---

## 1. SYMPTÔME

- En pilotage automatique de la ventilation (`input_select.clim_fan_mode_cible`
  = **Auto Arsenal**), le mode de ventilation réel de la clim **retombe
  régulièrement sur `auto`** (le « auto constructeur » Fujitsu), au lieu de
  tenir la vitesse résolue (`low` / `medium` / `high`, ou `quiet` en plage
  silencieuse).
- Le symptôme est **récurrent** (« se remet régulièrement »), pas permanent :
  la vitesse résolue est bien appliquée, puis `auto` réapparaît, en boucle.

---

## 2. CHAÎNE AUDITÉE (rappel d'architecture, Modèle B)

| Rôle | Entité / fichier | Autorité |
|------|------------------|----------|
| Intention | `input_select.clim_fan_mode_cible` (`06_input_selects/climatisation/fan_mode_cible.yaml`) | Utilisateur |
| Recommandation | `sensor.clim_fan_mode_recommande` (`12_.../ventilation/fan_mode_recommande.yaml`) | Perception pure (grille `x` + latches + caps) |
| Résolution / application | automation **`10030000000120`** (`11_.../ventilation/application_mode.yaml`) → `script.clim_set_fan_mode` (`10_scripts/climatisation/set_fan_mode.yaml`) → `climate.set_fan_mode` | **Autorité unique fan_mode** |
| Domaine silence | automation **`10030000000020`** (`11_.../silence.yaml`) → `switch.clim_quiet_fan` | **Autorité unique quiet** |
| Réel | `sensor.clim_mode_de_ventilation_local` (`12_.../ventilation/etat.yaml`) = `state_attr('climate.clim','fan_mode')` normalisé | Perception pure |
| Diagnostic | `sensor.clim_ventilation_diagnostic` (`12_.../ventilation/diagnostic.yaml`) | Perception pure |

Contrats de référence : `12_ventilation_intention`, `14_recommandation_ventilation`.

---

## 3. CONSTATS

### VENT-AUTO-1 — Arsenal défend DÉJÀ la dérive `auto` (trois triggers dédiés) — *sain*

La dérive vers le `auto` constructeur est un cas **explicitement anticipé** par
le code Arsenal. Deux autorités le rattrapent :

1. **Hors plage silencieuse** — automation `10030000000120`, trigger **P3** :
   ```yaml
   - platform: state
     entity_id: climate.clim
     attribute: fan_mode
     to: "auto"
   ```
   → re-résout et réémet `low` / `medium` / `high` (jamais `auto`). Le commentaire
   du fichier documente précisément ce cas (« Dérive vers le "auto" constructeur
   (P3) : événement d'ATTRIBUT pur … le auto Fujitsu subsistait indéfiniment »).

2. **En plage silencieuse** — automation `10030000000020` (silence), trigger
   miroir `fan_mode to: "auto"` → réasserte `switch.clim_quiet_fan` (le quiet).

3. Deux filets de reprise supplémentaires dans `10030000000120` : **P1**
   (`climate.clim from: "off"`, allumage) et **P2** (`from: unavailable/unknown`,
   reprise Airstage).

Le diagnostic lui-même (`diagnostic.yaml`) qualifie `auto_fujitsu` de **« cas
résiduel/legacy »**. **Conclusion : Arsenal n'introduit jamais `auto` et le
corrige activement dès qu'il apparaît.** La chaîne de résolution est conforme au
single-writer (l'intention n'est jamais réécrite, le quiet n'est jamais piloté
hors du domaine silence).

### VENT-AUTO-2 — Origine M1 : reset matériel Fujitsu au changement de mode opératoire — *hors code Arsenal*

Les scripts d'exécution de mode (`clim_exec_apply_cool/dry/heat`, ex.
`10_scripts/climatisation/cool.yaml`) émettent **`climate.set_hvac_mode`** et
**ne réémettent jamais** le fan_mode — c'est **voulu** (doctrine single-writer :
le fan appartient à `10030000000120`).

Or les unités **Fujitsu Airstage remettent la vitesse de ventilation à AUTO à
chaque changement de mode opératoire** (`cool` ↔ `dry` ↔ `heat`). Donc à chaque
bascule de mode **qui n'est pas `off → X`** (donc **non captée par P1**), le fan
tombe sur `auto` côté appareil. Ce reset est **inévitable côté firmware** ; il
est rattrapé par **P3** (VENT-AUTO-1), mais reste **visible transitoirement** et
se répète à la fréquence des bascules de mode.

### VENT-AUTO-3 — Origine M2 (levier principal) : course « poll-after-set » sur API à cohérence différée — *corrigeable dans ha-airstage*

Dans `custom_components/fujitsu_airstage/climate.py` :

```python
async def async_set_fan_mode(self, fan_mode: str) -> None:
    await self._ac.set_fan_speed(HA_FAN_TO_FUJITSU[fan_mode])
    await self.instance.coordinator.async_refresh()   # <-- re-poll immédiat
```

Le même motif (`await self.instance.coordinator.async_refresh()` **immédiatement
après l'écriture**) est présent dans **tous** les `async_set_*` / `async_turn_*`
(mode, température, swing, preset, switches).

L'API Airstage est **à cohérence différée** (`iot_class: local_polling`,
intervalle `AIRSTAGE_SYNC_LOCAL_INTERVAL = 60 s` / `AIRSTAGE_SYNC_INTERVAL =
120 s`, cf. `const.py`) : l'unité intérieure ne **rapporte** son nouvel état
qu'après un délai. Le refresh immédiat qui suit l'écriture relit donc
**fréquemment l'ANCIENNE valeur** (`auto`), que l'intégration réexpose aussitôt
comme `fan_mode` de `climate.clim`.

Effet en cascade, cohérent avec le symptôme « se remet régulièrement » :

1. Arsenal résout et envoie `low` → `set_fan_speed(low)` ;
2. `async_refresh()` immédiat → l'appareil renvoie encore `auto` (état pas
   encore reconverti) → `climate.clim.fan_mode = auto` ;
3. cette transition d'attribut `→ auto` **redéclenche P3** → nouvelle écriture
   `low` → nouveau refresh → nouvelle lecture périmée `auto` → **combat rapproché
   (flapping)** et **martèlement de l'API** ;
4. l'utilisateur voit `auto` « régulièrement ».

C'est **le** point corrigeable dans l'intégration : au lieu de re-poller une API
non encore cohérente, adopter une **mise à jour optimiste** de l'état local
(écrire la valeur cible dans les paramètres mis en cache + `async_write_ha_state()`),
ou **différer** le refresh d'assez pour laisser l'unité converger.

> **Statut de preuve.** VENT-AUTO-1 et VENT-AUTO-2 sont **certains** (lecture de
> code + comportement firmware documenté). VENT-AUTO-3 est une **hypothèse
> forte et étayée** par le motif de code (refresh immédiat après écriture sur
> une API de polling), mais la sémantique exacte de cohérence de `pyairstage`
> (`>=2.4.1,<3`, dépendance pip non vendorée) **n'a pas été vérifiée en
> runtime**. À **confirmer par relevé** (voir §5).

### VENT-AUTO-4 — Amplification : P3 sans anti-rebond `for:` — *arbitrage de robustesse, pas un défaut*

Le trigger **P3** (`fan_mode to: "auto"`) n'a **pas** de `for:`, contrairement au
trigger de recommandation (`for: "00:00:15"`). Couplé à M2 (VENT-AUTO-3), chaque
lecture périmée `auto` déclenche une **ré-écriture immédiate**, ce qui alimente
le flapping. Un `for:` court (5–10 s) sur P3 laisserait l'appareil se stabiliser
avant réaction — au prix d'un léger retard sur les corrections **légitimes**.
C'est un **arbitrage de tuning** à décider **seulement si** le correctif M2 ne
suffit pas ; ce n'est pas un défaut de la chaîne.

---

## 4. VERDICT

- **Chaîne de ventilation Arsenal : conforme.** Single-writer respecté, dérive
  `auto` déjà défendue (P3 hors silence, miroir en silence, P1/P2 en reprise).
  **Aucun bug Arsenal à l'origine du symptôme.**
- **Origine réelle : intégration / appareil.**
  - **M2 (VENT-AUTO-3)** — course *poll-after-set* dans `ha-airstage/climate.py`
    — est le **levier le plus net et corrigeable**, et explique la **récurrence**
    et le **flapping**.
  - **M1 (VENT-AUTO-2)** — reset firmware au changement de mode — est
    **inévitable** côté appareil ; son effet visible est **amplifié** par M2.
- **Le correctif appartient au dépôt `ha-airstage`**, pas à Arsenal. Un prompt de
  session dédié est fourni en **Annexe A**.

---

## 5. CONFIRMATION RUNTIME RECOMMANDÉE (avant tout correctif)

À relever dans le Recorder / les traces HA pour valider M2 :

1. **Corréler** chaque passage de `climate.clim.fan_mode` à `auto` avec :
   - un appel récent à `climate.set_fan_mode` (Arsenal), et/ou
   - un `climate.set_hvac_mode` immédiatement antérieur (test de M1).
2. **Mesurer le délai** entre l'écriture `set_fan_speed(low/medium/high)` et le
   retour de `fan_mode` à la valeur cible sur le poll suivant. Un retour à `auto`
   **juste après** l'écriture (< intervalle de poll) signe M2.
3. **Compter** les allers-retours `auto → low → auto` par heure (mesure du
   flapping et du martèlement API).
4. **Isoler M1** : les resets `auto` surviennent-ils **uniquement** après une
   bascule de mode opératoire, ou **aussi** hors bascule (→ M2 pur) ?

---

## Annexe A — Prompt pour une session dans le dépôt `ha-airstage`

Voir le fichier jumeau : [`prompt_session_ha_airstage_fan_auto.md`](prompt_session_ha_airstage_fan_auto.md).
</content>
</invoke>
