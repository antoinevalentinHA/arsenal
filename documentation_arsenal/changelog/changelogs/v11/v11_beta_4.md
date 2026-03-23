# Arsenal — Changelog v11 beta 4
_20 mars 2026_

---

## Résumé

La v11 beta 4 transforme le pipeline ECS sur trois axes :

- fin de cycle implicite → événement canonique (`ecs_fin_cycle_signal`)
- lecture temporelle → lecture physique (signature thermique)
- température partielle → référence post-inertie (`ecs_temperature_max_reelle_figee`)

Le système devient déterministe, physiquement ancré, temporellement opposable.

La séparation décision / observation / exécution est strictement renforcée.

| Indicateur | Valeur |
|---|---|
| Fichiers ajoutés | +69 |
| Fichiers supprimés | -3 |
| Fichiers modifiés | 21 |
| Domaines touchés | ECS, Scripts, Timers, Template Sensors, Documentation |

---

## Évolution majeure — Fin de cycle ECS canonique

La fin d'un cycle ECS n'est plus implicite ni basée sur la fin thermique brute.

Elle est désormais définie par un timer d'inertie post-cycle (15 min), suivi du gel des données et de l'émission du signal canonique `ecs_fin_cycle_signal`.

**Aucune logique ne doit, dans aucun cas, considérer un cycle ECS comme terminé avant l'émission de `ecs_fin_cycle_signal`. Toute logique s'appuyant sur la fin thermique brute est désormais invalide.**

Conséquences :

- toutes les logiques post-cycle sont décalées après inertie
- la fin exploitable du cycle devient un événement unique et opposable
- disparition des interprétations locales ou anticipées

---

## Ancrage physique — Abandon des heuristiques temporelles

Le système abandonne les heuristiques temporelles (délais arbitraires) au profit de mesures physiques :

- signature thermique réelle pour qualifier la chauffe
- inertie thermique pour valider la fin de cycle

Les décisions ne reposent plus sur des délais, mais sur des états physiques observés.

### Signature thermique de chauffe

Ajout du capteur `sensor.ecs_signature_thermique_chauffe` pour qualifier le démarrage réel de la chauffe (`indeterminee` / `insuffisante`).

Remplacement du déclenchement naïf par une lecture physique dans l'orchestrateur :

- ❌ ancien : delta après 90s
- ✅ nouveau : lecture de la signature thermique

Conditions de boost : signature = `insuffisante` **et** écart cible ≥ 1,0 °C.

---

## Ajustement du boost ECS

Augmentation du boost secondaire : `+1 °C → +5 °C`.

Le boost reste non bloquant, piloté par l'orchestrateur, validé par ACK.

---

## Référence thermique réelle post-cycle

Remplacement de `ecs_temperature_max_figee` par `ecs_temperature_max_reelle_figee`.

La température de référence inclut désormais l'inertie thermique post-cycle et est capturée après stabilisation complète.

---

## Auto-correction des offsets — fiabilisation

- utilisation de `tmax_reference` (post-inertie)
- ajout d'un re-clamp après quantification — aucune sortie hors bornes possible
- `alpha = 0.25` explicitement identifié comme paramètre contractuel

---

## Nouvelle couche temporelle — Timer d'inertie post-cycle

Ajout de `timer.fenetre_inertie_chauffe_ecs` (`restore: true`, 15 min).

Rôle : stabilisation thermique, référence de fin de cycle, déclencheur du gel final.

Hiérarchie temporelle mise à jour :
```
Watchdog > Timer bouclage > Timer inertie post-cycle > Timer stabilisation
```

---

## Réalignement des gardiens

Les gardiens post-cycle ne se déclenchent plus après la fin thermique brute, mais uniquement après inertie écoulée et signal canonique émis.

---

## Renforcement documentaire

Nouveaux contrats : pipeline global ECS, fin de cycle, signal canonique, inertie post-cycle, signature thermique, référence thermique post-inertie.

Refontes : offsets (réécriture complète), timers et watchdogs (nouvelle section 6 — timer d'inertie), journalisation, `ecs_cycle_session_close`, `ecs_cycle_session_open`.

`09_invariants_et_interdictions.md` : trois nouveaux invariants absolus liés au signal canonique et au gel final.

---

## Nettoyage

Suppressions : `10_automations/ecs/signal_fin_cycle.yaml`, `10_automations/ecs/log/fin.yaml`, `documentation_arsenal/contrats/ecs/10_resilience_et_defaillances.md` (remplacé par un dossier).

---

## Points de vigilance

- Toute logique post-cycle doit désormais dépendre de `ecs_fin_cycle_signal`
- Toute analyse thermique doit utiliser la référence post-inertie (`ecs_temperature_max_reelle_figee`)
- Toute décision de boost repose sur la signature thermique, pas le temps

---

## Lecture système

Avant :

- fin de cycle implicite
- décisions basées sur délais
- données partielles

Après :

- fin de cycle canonique
- décisions basées sur états physiques observés
- données stabilisées post-inertie

Le système devient déterministe et auditable.