# ✅ ARSENAL — CLÔTURE DE CHANTIER

## Climatisation / Ventilation — Résolution du « auto constructeur » récurrent (dérive `fan_mode → auto`)

| Champ | Valeur |
|---|---|
| **Type** | Clôture — cause racine corrigée à la source + validation terrain |
| **Domaine** | Climatisation / Ventilation — intégration `fujitsu_airstage` |
| **Statut** | ✅ CLÔTURÉ — correctif M2 appliqué (dépôt `ha_airstage`), vendoré dans Arsenal, **confirmé terrain (utilisateur) le 2026-07-17** |
| **Version** | 1.0 |
| **Date** | 2026-07-17 |
| **Chantier** | Hors numérotation C — sujet **audit-driven**, correctif **hors Arsenal** (intégration). Jamais entré en ① Actifs (aucune modification runtime Arsenal décidée) |
| **Audit source** | [`audit_ventilation_auto_constructeur_recurrent.md`](../../01_rapports/climatisation/audit_ventilation_auto_constructeur_recurrent.md) |
| **Prompt jumeau** | [`prompt_session_ha_airstage_fan_auto.md`](../../01_rapports/climatisation/prompt_session_ha_airstage_fan_auto.md) |

---

## 1. Objet

Clore le sujet « le mode de ventilation de la clim se remet régulièrement sur le
`auto` constructeur ». L'audit statique avait établi que la **chaîne Arsenal est
saine** (elle défend déjà la dérive, elle n'en est pas l'origine) et que le
**levier corrigeable** était une course *poll-after-set* dans l'intégration
`fujitsu_airstage`, à corriger **dans le dépôt `ha_airstage`**, pas dans Arsenal.

Ce document acte que le correctif a été **réalisé côté intégration**, qu'il est
**vendoré** dans Arsenal, et qu'il est **validé en conditions réelles** par
l'utilisateur.

## 2. Cause racine — VENT-AUTO-3 (M2) : d'« hypothèse forte » à **confirmée**

L'audit posait M2 comme *hypothèse forte et étayée, non vérifiée en runtime*
(§3, statut de preuve). Le levier était le re-poll immédiat après écriture, sur
une API à cohérence différée (`iot_class: local_polling`) :

```python
# AVANT (motif d'origine, repris dans tous les async_set_* / async_turn_*)
async def async_set_fan_mode(self, fan_mode: str) -> None:
    await self._ac.set_fan_speed(HA_FAN_TO_FUJITSU[fan_mode])
    await self.instance.coordinator.async_refresh()   # relit l'ANCIEN "auto"
```

La lecture périmée `auto` réexposée en `climate.clim.fan_mode` **redéclenchait
P3** → nouvelle écriture → nouvelle lecture périmée → **combat rapproché
(flapping)** et **martèlement de l'API**. Le symptôme « se remet régulièrement »
signait cette boucle. La disparition du symptôme après suppression du re-poll
immédiat **confirme M2** : ce que l'audit qualifiait d'hypothèse est désormais
**établi par le résultat terrain**.

## 3. Correctif appliqué (côté intégration, vendoré dans Arsenal)

Piste retenue parmi celles proposées au prompt jumeau (§3) : **mise à jour
optimiste** plutôt que refresh différé. Après un `set_*` réussi, la valeur
commandée est écrite dans le cache du coordinator et les listeners sont
notifiés — **sans re-poll immédiat** ; le prochain poll *planifié* (au-delà de
la fenêtre de convergence de l'unité) réconcilie sans lecture périmée précoce.

```python
# APRÈS (custom_components/fujitsu_airstage/climate.py)
async def async_set_fan_mode(self, fan_mode: str) -> None:
    await self._ac.set_fan_speed(HA_FAN_TO_FUJITSU[fan_mode])
    self.apply_optimistic_update(
        {constants.ACParameter.FAN_SPEED: HA_FAN_TO_FUJITSU[fan_mode]}
    )
```

- **Point de patch** : `apply_optimistic_update()` factorisé dans
  [`entity.py`](../../../../custom_components/fujitsu_airstage/entity.py), appliqué de
  façon cohérente dans [`climate.py`](../../../../custom_components/fujitsu_airstage/climate.py)
  (fan, hvac, température, swing, preset) **et**
  [`switch.py`](../../../../custom_components/fujitsu_airstage/switch.py) (energy save,
  quiet, powerful…), conformément au garde-fou « ne pas casser les autres
  entités qui dépendent du même motif ».
- **Traçabilité fork** : documenté dans
  [`PATCHES_ARSENAL.md`](../../../../custom_components/fujitsu_airstage/PATCHES_ARSENAL.md)
  (« Écriture optimiste locale au lieu de `poll-after-set` … supprimant le
  flapping de la vitesse de ventilation »). Fork `antoinevalentinHA/ha_airstage`,
  branche `arsenal-stable`.

## 4. Validation terrain

- **Preuve** : confirmation utilisateur, **2026-07-17** — « plus de problème avec
  la ventilation de la clim qui se mettait en “auto constructeur” régulièrement ;
  des modifications ont été faites dans le dépôt HA Airstage ».
- **Ce que cela vaut** : c'est exactement la confirmation runtime réclamée au §5
  de l'audit (« CONFIRMATION RUNTIME RECOMMANDÉE avant tout correctif »),
  observée **après** déploiement du correctif — disparition du symptôme récurrent
  (plus de retombées régulières sur `auto`, plus de combat/clignotement).
- **Portée** : validation qualitative par observation d'usage. Elle **n'exige
  pas** de relevé Recorder chiffré (allers-retours `auto`/heure avant-après) pour
  clore : la récurrence était le symptôme, sa disparition durable est le critère.

## 5. Ce qui reste en place (volontairement) — mitigations Arsenal conservées

Le correctif supprime la **cause** (M2) ; il ne rend pas les filets Arsenal
inutiles. **Aucune simplification de la chaîne Arsenal n'est emportée par cette
clôture** :

- **Trigger P3** (`climate.clim` attribute `fan_mode` → `auto`) dans
  [`application_mode.yaml`](../../../../11_automations/climatisation/ventilation/application_mode.yaml)
  **conservé** : il défend le reset firmware **M1** (VENT-AUTO-2 — l'unité Fujitsu
  remet la vitesse à `AUTO` à chaque changement de mode opératoire `cool ↔ dry ↔
  heat`), **inévitable côté appareil** et **indépendant** de M2.
- **Miroir en plage silencieuse** (automation `10030000000020`) et filets de
  reprise **P1** (allumage) / **P2** (reprise Airstage) **conservés**.
- **VENT-AUTO-4** (ajout d'un `for:` court sur P3) **non appliqué** : c'était un
  arbitrage de tuning « seulement si le correctif M2 ne suffit pas ». M2 suffit →
  arbitrage clos sans action, P3 reste sans anti-rebond.

## 6. Statut

✅ **CLÔTURÉ.** Cause racine M2 corrigée à la source (`ha_airstage`), vendorée et
documentée dans Arsenal, symptôme récurrent disparu (validation terrain
utilisateur 2026-07-17). Chaîne de ventilation Arsenal **inchangée** (filets M1
conservés). Descend en ⑤ Clos récents au registre.

*Aucun runtime, contrat ou YAML Arsenal modifié par cette clôture (le correctif
vit dans l'intégration vendorée ; ce document est documentaire).*
