# CONTRAT ARSENAL — CLIMATISATION
## Index du dossier

**Domaine :** Climatisation résidentielle
**Version contrat :** v1.4
**Statut :** Stable — aligné runtime Arsenal v15.x

---

## Structure du dossier

| Fichier / dossier | Contenu |
|---|---|
| [`01_finalite.md`](01_finalite.md) | Finalité du système, états exclusifs, objectifs |
| [`02_architecture.md`](02_architecture.md) | Couches Arsenal, invariants globaux de déclenchement |
| [`03_decision_canonique.md`](03_decision_canonique.md) | Objet `sensor.clim_target_mode`, pureté, déterminisme, consommation exclusive des besoins admissibles |
| [`04_entrees_metier.md`](04_entrees_metier.md) | Températures, humidex, présence, contraintes physiques |
| [`05_decision_candidats.md`](05_decision_candidats.md) | Production des besoins admissibles par mode (verrou de requalification) |
| [`06_doctrine_blocages.md`](06_doctrine_blocages.md) | Doctrine opérateur des blocages, classification, gardes et invariants |
| [`07_arbitrage_politique.md`](07_arbitrage_politique.md) | Politique d'arbitrage active, hiérarchie des modes |
| [`08_execution.md`](08_execution.md) | Application idempotente du mode cible |
| [`09_securite.md`](09_securite.md) | Guards et Watchdog |
| [`10_observabilite.md`](10_observabilite.md) | États explicatifs, robustesse, déterminisme post-redémarrage |
| [`11_perimetre_exclu.md`](11_perimetre_exclu.md) | Ce que le système ne fait pas |
| [`12_ventilation_intention.md`](12_ventilation_intention.md) | Ventilation (`fan_mode`) — intention persistante (Modèle B), single-writer, résolution, origine de pilotage, convergence |
| [`13_intensite_besoin_froid.md`](13_intensite_besoin_froid.md) | Intensité du besoin de froid — couche perception (capteur numérique + ordinal), référence `seuil_extinction_clim_applique`, garde anti-gel, sans pilotage matériel |
| [`capteurs/`](capteurs/README.md) | Documentation détaillée des capteurs implémentant les couches du système |

---

### Dossier `capteurs/`

Ce dossier contient la documentation technique détaillée des capteurs Home Assistant
implémentant les différentes couches du système (besoins, admissibilité, autorisations, blocages, décision, cohérence, etc.).

Il constitue la traduction concrète du contrat en entités.

| Sous-dossier | Rôle |
|---|---|
| `besoins/` | Capteurs exprimant les besoins thermiques bruts |
| `admissibilite/` | Capteurs d'admissibilité décisionnelle |
| `autorisations/` | Capteurs d'autorisation d'exécution |
| `blocages/` | Capteurs de blocage et contraintes |
| `seuils_et_franchissements/` | Capteurs de seuils et franchissements |
| `decision/` | Capteurs décisionnels, explicatifs et de lecture locale |
| `coherence/` | Capteur de cohérence décision / réel |

---

## Chaîne logique

```
Finalité
  └─ Architecture (couches)
       └─ Entrées métier
            └─ Besoins (bruts — hystérésis thermique / hygrométrique)
                 └─ Admissibilité (verrou de requalification)
                      └─ Décision canonique (sensor.clim_target_mode)
                           └─ Arbitrage (politique active)
                                └─ Exécution (idempotente)
                                     └─ Sécurité (Guards / Watchdog — voie orthogonale)
                                          └─ Observabilité (lecture seule)
```

---

## Principe de séparation des couches

| Couche | Objet | Règle |
|---|---|---|
| Besoin brut | `binary_sensor.besoin_clim_*` | Fait physique pur — indépendant de l'autorisation |
| Admissibilité | `binary_sensor.besoin_clim_*_admissible` | Verrou de requalification — naît sur front montant du besoin sous autorisation active |
| Décision | `sensor.clim_target_mode` | Consomme exclusivement les besoins admissibles |

Un besoin brut ne peut jamais être consommé directement par la Décision.
Un besoin préexistant à une interdiction ne devient jamais admissible par simple retour de l'autorisation.

---

⚠️ Principe Arsenal fondamental
La couche Exécution ne modifie jamais la décision.
Elle applique uniquement `sensor.clim_target_mode`.
