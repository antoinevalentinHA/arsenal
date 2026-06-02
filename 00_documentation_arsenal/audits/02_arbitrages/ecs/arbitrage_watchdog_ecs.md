# Note d'arbitrage — Doctrine du watchdog ECS (rendue)

> Type : note d'arbitrage — **décision rendue** (acte terminal de l'arbitrage)
> Portée : sous-système ECS — watchdog de cycle (`timer.ecs_cycle_watchdog`, automation `10250000000008`), contrats `06_temps_timers_watchdogs` et `07_gardiens_et_securite_active`.
> Origine : audit officiel ECS → contre-expertise watchdog → arbitrage architectural.
> Statut : **NORMATIF — ARBITRAGE RENDU — OPPOSABLE.** Tranche la doctrine du watchdog ECS et clôt le périmètre watchdog en gouvernance.
> Référence dépôt : v15.8.8, branche `main` (HEAD `224edae`).
> Principe directeur : *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Décision rendue

L'architecte confirme que **le comportement actuel du runtime ECS est correct et constitue la référence**. La doctrine du watchdog de cycle ECS est arrêtée comme suit, sans ambiguïté.

---

## 2. Doctrine retenue (a) — « Le watchdog borne le verrou »

- Le watchdog ECS **borne le verrou** de cycle (`input_boolean.ecs_cycle_en_cours`).
- À expiration, il **garantit** : le rabaissement de la consigne (vers 10 °C, via le bridge) et la **libération unilatérale du verrou**.
- Il **n'a pas vocation** à interrompre le processus complet ni à empêcher l'orchestrateur (`script.chauffage_ecs_cycle`) de poursuivre son séquencement interne.

Cette doctrine est la transcription fidèle de la définition opérationnelle déjà inscrite au contrat `07` §6 (« Watchdog terminal » : *rabaissement forcé — libération unilatérale du verrou — restauration nominale — indépendance totale des mécanismes temporels secondaires*).

---

## 3. Doctrine rejetée (b) — « Watchdog souverain sur le processus complet »

Explicitement **rejetée**. Le watchdog n'est pas un terminateur de processus. Aucune capacité d'arrêt du script orchestrateur n'est attendue ni requise (et n'existe pas en sémantique Home Assistant pour une automation déclenchée sur `timer.finished`).

---

## 4. Conséquences

- **Aucun chantier runtime watchdog** n'est ouvert ni autorisé.
- **Aucune modification YAML** du watchdog n'est autorisée.
- **Aucun changement de comportement** ECS n'est recherché.
- Le constat dérivé `ECS-WD-2` (l'orchestrateur peut ré-appliquer une consigne haute après passage du watchdog) est **requalifié en comportement assumé** : il n'est plus un défaut, le runtime étant la référence. Voir §7.

---

## 5. Preuves d'alignement (runtime ↔ contrat ↔ CI)

À la date de l'arbitrage, le système était **déjà** aligné sur la doctrine (a) ; seule la prose de `06` §4.2 traînait une formulation ambiguë :

| Plan | Élément | Constat |
|---|---|---|
| Runtime | `11_automations/ecs/consigne_10/watchdog.yaml` (`10250000000008`) | À `timer.finished` : bridge → 10 °C + `turn_off ecs_cycle_en_cours`. Pas d'arrêt de script. |
| Contrat | `07_gardiens_et_securite_active.md` §6 | Périmètre assuré = rabaissement + libération du verrou + restauration. Conforme. |
| CI | `scripts/arsenal_contracts/check_ecs_securite.py` T05 | Vérifie statiquement la libération du verrou (`§07 §6.1`). La doctrine (a) est **déjà protégée par la CI**. |
| Contrat | `06_temps_timers_watchdogs.md` §4.2 | Seul écart : « aucun cycle ne survit à son watchdog » lisible comme « processus ». **Réaligné** par le présent lot. |

---

## 6. Chaîne de traçabilité

```
audit_ecs_domaine.md (ECS-WD-1, qualifié 🔴 Haute)
   └─→ contre_expertise_watchdog_ecs.md (ECS-WD-1 INFIRMÉ comme violation ; doctrine (a) établie sur preuves)
          └─→ arbitrage_watchdog_ecs.md (présent document — décision rendue, doctrine (a) officielle)
                 └─→ 06_temps_timers_watchdogs.md §4.2 (conséquence normative — réalignement)
```

---

## 7. Effets documentaires induits par le présent arbitrage

- `06_temps_timers_watchdogs.md` §4.1/§4.2 : réaligné (« cycle » = verrou ; rejet explicite de (b) ; renvoi à `07` §6 et au présent document).
- `audit_ecs_domaine.md` (bannière `ECS-WD-1`) et `contre_expertise_watchdog_ecs.md` (avenant) : statut « arbitrage rendu ».
- `backlog_ecs.md` : gate doctrinale levée ; `ECS-WD-2` clos (comportement assumé) ; `ECS-WD-2b` runtime **caduc**.
- `index.md` : section `Arbitrages → ECS` + bloc « État du domaine ECS ».

---

## 8. Résidus connus, assumés

- **`ECS-WD-2` — comportement assumé.** La fenêtre théorique (désinfection > 30 min : ré-application d'une consigne haute après libération du verrou) reste **conditionnée à une occurrence non observée**. Conformément au principe directeur, aucune correction runtime n'est entreprise sans preuve forte. Tracé ici pour éviter toute ré-ouverture en audit ultérieur.
- **Référence historique figée.** `changelog/v15/v15_8_7.md` cite l'ancien nom de fichier du contrat de résilience ; les changelogs étant immuables, cette référence reste telle quelle après le renommage `ECS-DOC-2`.

---

*Note d'arbitrage ECS — watchdog. Décision rendue par l'architecte ; transcription documentaire. Acte de gouvernance — aucune modification runtime, YAML ou CI. Domaine ECS non clôturé.*
